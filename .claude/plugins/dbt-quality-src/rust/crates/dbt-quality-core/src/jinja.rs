//! Jinja structure extracted from dbt's minijinja fork.
//!
//! The parser AST borrows the source. Return an owned summary so callers
//! can keep each call's arguments, span, and control-flow context.

use minijinja::machinery::ast::{self, CallArg, Expr, Stmt};
use minijinja::machinery::{parse, tokenize, Span as JSpan, Token, WhitespaceConfig};
use minijinja::value::Value;

/// A 1-based line and column range, plus byte offsets into the source.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, serde::Serialize)]
pub struct Span {
    pub start_line: u32,
    pub start_col: u32,
    pub start_offset: u32,
    pub end_line: u32,
    pub end_col: u32,
    pub end_offset: u32,
}

impl From<JSpan> for Span {
    fn from(s: JSpan) -> Self {
        Span {
            start_line: s.start_line,
            start_col: s.start_col + 1,
            start_offset: s.start_offset,
            end_line: s.end_line,
            end_col: s.end_col + 1,
            end_offset: s.end_offset,
        }
    }
}

/// A literal argument value, or source text in `Expr` for a non-literal expression.
#[derive(Clone, Debug, PartialEq, serde::Serialize)]
pub enum Lit {
    Str(String),
    Num(f64),
    Bool(bool),
    None,
    List(Vec<Lit>),
    Map(Vec<(String, Lit)>),
    /// A non-literal expression; holds its source text.
    Expr(String),
}

impl Lit {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            Lit::Str(s) => Some(s),
            _ => None,
        }
    }
}

#[derive(Clone, Debug, serde::Serialize)]
pub struct CallSite {
    /// Dotted callee, e.g. `var`, `config`, `adapter.dispatch`, `dbt_utils.star`.
    pub name: String,
    pub args: Vec<Lit>,
    pub kwargs: Vec<(String, Lit)>,
    pub span: Span,
    /// Number of enclosing `{% if %}` / `{% for %}` blocks.
    pub control_depth: u32,
    /// Source text of each enclosing `{% if %}` condition, outermost first.
    pub conditions: Vec<String>,
    /// Name of the enclosing `{% macro %}`, if any.
    pub in_macro: Option<String>,
}

impl CallSite {
    pub fn kwarg(&self, k: &str) -> Option<&Lit> {
        self.kwargs.iter().find(|(n, _)| n == k).map(|(_, v)| v)
    }
}

#[derive(Clone, Debug, serde::Serialize)]
pub struct MacroDef {
    pub name: String,
    pub kind: String,
    pub params: Vec<String>,
    pub span: Span,
    /// Source text of the body.
    pub body: String,
}

#[derive(Clone, Debug, serde::Serialize)]
pub struct SetStmt {
    pub target: String,
    pub value: Lit,
    pub span: Span,
}

#[derive(Clone, Debug, Default, serde::Serialize)]
pub struct JinjaSummary {
    pub calls: Vec<CallSite>,
    pub macros: Vec<MacroDef>,
    pub sets: Vec<SetStmt>,
    /// Spans and conditions of `{% if %}` blocks.
    pub ifs: Vec<(Span, String)>,
    /// Executable `this` expressions and whether their branch requires is_incremental().
    pub this_reads: Vec<(Span, bool)>,
    /// Set when the template fails to parse; the summary is then empty.
    pub parse_error: Option<String>,
}

impl JinjaSummary {
    pub fn calls_named<'a>(&'a self, name: &'a str) -> impl Iterator<Item = &'a CallSite> + 'a {
        self.calls.iter().filter(move |c| c.name == name)
    }
}

/// Parse `source` with dbt's Jinja syntax and return a summary.
pub fn summarize(source: &str, filename: &str) -> JinjaSummary {
    let ws = WhitespaceConfig::default();
    match parse(source, filename, Default::default(), ws) {
        Ok(stmt) => {
            let mut w = Walker { src: source, out: JinjaSummary::default(), depth: 0, conds: vec![], mac: None, incremental: false };
            w.stmt(&stmt);
            w.out
        }
        Err(e) => JinjaSummary { parse_error: Some(e.to_string()), ..Default::default() },
    }
}

struct Walker<'s> {
    src: &'s str,
    out: JinjaSummary,
    depth: u32,
    conds: Vec<String>,
    mac: Option<String>,
    incremental: bool,
}

fn requires_incremental(expr: &Expr) -> bool {
    match expr {
        Expr::Call(call) => dotted(&call.expr).as_deref() == Some("is_incremental") && call.args.is_empty(),
        Expr::BinOp(op) if matches!(op.op, ast::BinOpKind::ScAnd) => requires_incremental(&op.left) || requires_incremental(&op.right),
        _ => false,
    }
}

fn slice(src: &str, s: JSpan) -> String {
    src.get(s.start_offset as usize..s.end_offset as usize).unwrap_or("").to_string()
}

pub fn expr_span(e: &Expr) -> JSpan {
    match e {
        Expr::Var(x) => x.span,
        Expr::Const(x) => x.span,
        Expr::Slice(x) => x.span,
        Expr::UnaryOp(x) => x.span,
        Expr::BinOp(x) => x.span,
        Expr::IfExpr(x) => x.span,
        Expr::Filter(x) => x.span,
        Expr::Test(x) => x.span,
        Expr::GetAttr(x) => x.span,
        Expr::GetItem(x) => x.span,
        Expr::Call(x) => x.span,
        Expr::List(x) => x.span,
        Expr::Map(x) => x.span,
        Expr::Tuple(x) => x.span,
    }
}

/// Dotted name of a callee, when it is a plain path.
pub fn dotted(e: &Expr) -> Option<String> {
    match e {
        Expr::Var(v) => Some(v.id.to_string()),
        Expr::GetAttr(g) => dotted(&g.expr).map(|p| format!("{p}.{}", g.name)),
        _ => None,
    }
}

fn const_lit(v: &Value) -> Lit {
    if v.is_none() || v.is_undefined() {
        return Lit::None;
    }
    if let Some(s) = v.as_str() {
        return Lit::Str(s.to_string());
    }
    if v.is_number() {
        return Lit::Num(f64::try_from(v.clone()).unwrap_or(0.0));
    }
    if v.kind() == minijinja::value::ValueKind::Bool {
        return Lit::Bool(v.is_true());
    }
    Lit::Expr(v.to_string())
}

impl<'s> Walker<'s> {
    fn lit(&self, e: &Expr) -> Lit {
        match e {
            Expr::Const(c) => const_lit(&c.value),
            Expr::List(l) => Lit::List(l.items.iter().map(|i| self.lit(i)).collect()),
            Expr::Tuple(l) => Lit::List(l.items.iter().map(|i| self.lit(i)).collect()),
            Expr::Map(m) => Lit::Map(
                m.keys
                    .iter()
                    .zip(&m.values)
                    .map(|(k, v)| {
                        let key = match self.lit(k) {
                            Lit::Str(s) => s,
                            _ => slice(self.src, expr_span(k)),
                        };
                        (key, self.lit(v))
                    })
                    .collect(),
            ),
            _ => Lit::Expr(slice(self.src, expr_span(e))),
        }
    }

    fn stmts(&mut self, v: &[Stmt]) {
        for s in v {
            self.stmt(s);
        }
    }

    fn stmt(&mut self, s: &Stmt) {
        match s {
            Stmt::Template(t) => self.stmts(&t.children),
            Stmt::EmitExpr(e) => {
                if let Expr::Var(var) = &e.expr && var.id == "this" {
                    self.out.this_reads.push((e.span.into(), self.incremental));
                }
                self.expr(&e.expr);
            }
            Stmt::EmitRaw(_) | Stmt::Comment(_) => {}
            Stmt::ForLoop(f) => {
                self.expr(&f.iter);
                if let Some(x) = &f.filter_expr {
                    self.expr(x);
                }
                self.depth += 1;
                self.stmts(&f.body);
                self.stmts(&f.else_body);
                self.depth -= 1;
            }
            Stmt::IfCond(i) => {
                self.expr(&i.expr);
                // An `elif` expression span starts at the keyword; drop it.
                let cond = crate::rx!(r"^\s*(?:el)?if\s+").replace(&slice(self.src, expr_span(&i.expr)), "").into_owned();
                self.out.ifs.push((i.span.into(), cond.clone()));
                self.depth += 1;
                self.conds.push(cond.clone());
                let previous = self.incremental;
                self.incremental |= requires_incremental(&i.expr);
                self.stmts(&i.true_body);
                self.incremental = previous;
                self.conds.pop();
                self.conds.push(format!("not ({cond})"));
                self.stmts(&i.false_body);
                self.conds.pop();
                self.depth -= 1;
            }
            Stmt::WithBlock(w) => {
                for (_, v) in &w.assignments {
                    self.expr(v);
                }
                self.stmts(&w.body);
            }
            Stmt::Set(x) => {
                self.expr(&x.expr);
                let target = slice(self.src, expr_span(&x.target));
                let value = self.lit(&x.expr);
                self.out.sets.push(SetStmt { target, value, span: x.span.into() });
            }
            Stmt::SetBlock(x) => self.stmts(&x.body),
            Stmt::AutoEscape(x) => self.stmts(&x.body),
            Stmt::FilterBlock(x) => {
                self.expr(&x.filter);
                self.stmts(&x.body);
            }
            Stmt::Block(b) => self.stmts(&b.body),
            Stmt::Import(_) | Stmt::FromImport(_) | Stmt::Extends(_) | Stmt::Include(_) => {}
            Stmt::Macro((m, kind, _)) => {
                let body = match (m.body.first(), m.body.last()) {
                    (Some(_), Some(_)) => slice(self.src, m.span),
                    _ => String::new(),
                };
                self.out.macros.push(MacroDef {
                    name: m.name.to_string(),
                    kind: format!("{kind:?}").to_lowercase(),
                    params: m.args.iter().map(|a| slice(self.src, expr_span(a))).collect(),
                    span: m.span.into(),
                    body,
                });
                let prev = self.mac.replace(m.name.to_string());
                let (d, c) = (self.depth, std::mem::take(&mut self.conds));
                self.depth = 0;
                let incremental = std::mem::replace(&mut self.incremental, false);
                for d in &m.defaults {
                    self.expr(d);
                }
                self.stmts(&m.body);
                self.depth = d;
                self.incremental = incremental;
                self.conds = c;
                self.mac = prev;
            }
            Stmt::CallBlock(c) => {
                self.call(&c.call);
                self.stmts(&c.macro_decl.body);
            }
            Stmt::Continue(_) | Stmt::Break(_) => {}
            Stmt::Do(d) => self.expr(&d.expr),
        }
    }

    fn call(&mut self, c: &ast::Spanned<ast::Call>) {
        let name = dotted(&c.expr).unwrap_or_else(|| slice(self.src, expr_span(&c.expr)));
        let mut args = vec![];
        let mut kwargs = vec![];
        for a in &c.args {
            match a {
                CallArg::Pos(e) => args.push(self.lit(e)),
                CallArg::Kwarg(k, e) => kwargs.push((k.to_string(), self.lit(e))),
                CallArg::PosSplat(e) | CallArg::KwargSplat(e) => args.push(self.lit(e)),
            }
        }
        self.out.calls.push(CallSite {
            name,
            args,
            kwargs,
            span: c.span.into(),
            control_depth: self.depth,
            conditions: self.conds.clone(),
            in_macro: self.mac.clone(),
        });
        if !matches!(c.expr, Expr::Var(_)) {
            self.expr(&c.expr);
        }
        for a in &c.args {
            match a {
                CallArg::Pos(e) | CallArg::Kwarg(_, e) | CallArg::PosSplat(e) | CallArg::KwargSplat(e) => self.expr(e),
            }
        }
    }

    fn expr(&mut self, e: &Expr) {
        match e {
            Expr::Var(_) | Expr::Const(_) => {}
            Expr::Slice(s) => {
                self.expr(&s.expr);
                for x in [&s.start, &s.stop, &s.step].into_iter().flatten() {
                    self.expr(x);
                }
            }
            Expr::UnaryOp(u) => self.expr(&u.expr),
            Expr::BinOp(b) => {
                self.expr(&b.left);
                self.expr(&b.right);
            }
            Expr::IfExpr(i) => {
                self.expr(&i.test_expr);
                self.expr(&i.true_expr);
                if let Some(f) = &i.false_expr {
                    self.expr(f);
                }
            }
            Expr::Filter(f) => {
                if let Some(x) = &f.expr {
                    self.expr(x);
                }
                for a in &f.args {
                    if let CallArg::Pos(x) | CallArg::Kwarg(_, x) = a {
                        self.expr(x);
                    }
                }
            }
            Expr::Test(t) => self.expr(&t.expr),
            Expr::GetAttr(g) => self.expr(&g.expr),
            Expr::GetItem(g) => {
                self.expr(&g.expr);
                self.expr(&g.subscript_expr);
            }
            Expr::Call(c) => self.call(c),
            Expr::List(l) => l.items.iter().for_each(|i| self.expr(i)),
            Expr::Tuple(l) => l.items.iter().for_each(|i| self.expr(i)),
            Expr::Map(m) => {
                m.keys.iter().for_each(|i| self.expr(i));
                m.values.iter().for_each(|i| self.expr(i));
            }
        }
    }
}

/// Returns `source` with every Jinja tag, expression and comment replaced by
/// spaces (newlines kept), so byte offsets and line numbers still line up.
/// Falls back to the input unchanged when the template does not tokenize.
pub fn blank_jinja(source: &str) -> String {
    try_blank_jinja(source).unwrap_or_else(|| source.to_string())
}

pub fn try_blank_jinja(source: &str) -> Option<String> {
    let mut out = source.as_bytes().to_vec();
    let mut data = vec![false; out.len()];
    for tok in tokenize(source, false, Default::default(), WhitespaceConfig::default()) {
        let (tok, span) = tok.ok()?;
        if let Token::TemplateData(_) = tok {
            for b in &mut data[span.start_offset as usize..span.end_offset as usize] {
                *b = true;
            }
        }
    }
    for (i, b) in out.iter_mut().enumerate() {
        if !data[i] && *b != b'\n' && *b != b'\r' {
            *b = b' ';
        }
    }
    String::from_utf8(out).ok()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn finds_sentinel_var_and_gated_config() {
        let src = "{% if var('full', false) %}{{ config(materialized='table') }}{% endif %}\nselect {{ var('k','k') }}";
        let s = summarize(src, "m.sql");
        assert!(s.parse_error.is_none(), "{:?}", s.parse_error);
        let cfg = s.calls_named("config").next().unwrap();
        assert_eq!(cfg.control_depth, 1);
        assert_eq!(cfg.conditions, vec!["var('full', false)".to_string()]);
        let sentinel: Vec<_> = s.calls_named("var").filter(|c| c.args.len() == 2 && c.args[0] == c.args[1]).collect();
        assert_eq!(sentinel.len(), 1);
        assert_eq!(sentinel[0].span.start_line, 2);
    }

    #[test]
    fn macro_calls_in_hook_strings_parse_as_templates() {
        let src = r#"{{ config(pre_hook="{{ log_run('x') }} delete from {{ this }}") }}"#;
        let s = summarize(src, "m.sql");
        let hook = s.calls_named("config").next().unwrap().kwarg("pre_hook").unwrap().as_str().unwrap().to_string();
        let inner = summarize(&hook, "hook");
        assert_eq!(inner.calls_named("log_run").count(), 1);
    }

    #[test]
    fn blank_keeps_offsets() {
        let src = "select {{ x(\"{{ y }}\") }} from t -- {# c #}";
        let b = blank_jinja(src);
        assert_eq!(b.len(), src.len());
        assert!(b.starts_with("select ") && b.contains(" from t -- "));
        assert!(!b.contains('{'));
    }

    #[test]
    fn macros_are_listed() {
        let s = summarize("{% macro m(a, b=1) %}{{ var('x') }}{% endmacro %}", "x.sql");
        assert_eq!(s.macros[0].name, "m");
        assert_eq!(s.calls[0].in_macro.as_deref(), Some("m"));
    }
}
