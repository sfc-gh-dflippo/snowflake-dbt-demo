//! SQL and Jinja text helpers shared by all rule packs.
//!
//! These text helpers do not require SQL to compile. Stripping functions
//! replace text with spaces and preserve byte offsets into the original text.
//!
//! Offsets count bytes. Columns count Unicode characters.

use std::sync::LazyLock;

use regex::{Captures, Regex};
use serde_json::Value;
use sha2::{Digest, Sha256};

/// A compiled `regex::Regex`, built once.
#[macro_export]
macro_rules! rx {
    ($re:expr) => {{
        static R: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| regex::Regex::new($re).unwrap());
        &*R
    }};
}

/// A compiled `fancy_regex::Regex` (lookaround support), built once.
#[macro_export]
macro_rules! frx {
    ($re:expr) => {{
        static R: std::sync::LazyLock<fancy_regex::Regex> =
            std::sync::LazyLock::new(|| fancy_regex::Regex::new($re).unwrap());
        &*R
    }};
}

/// Replace every non-newline character in `s` with a space, keeping length in bytes.
fn blank(s: &str) -> String {
    s.bytes().map(|b| if b == b'\n' { '\n' } else { ' ' }).collect()
}

/// Blank a quoted literal, keeping its quotes.
fn blank_quoted(s: &str) -> String {
    let n = s.len();
    format!("{}{}{}", &s[..1], " ".repeat(n - 2), &s[n - 1..])
}

/// Blank out SQL comments and string literals, preserving offsets and newlines.
pub fn strip_comments_and_strings(sql: &str) -> String {
    let s = rx!(r"(?s)/\*.*?\*/").replace_all(sql, |c: &Captures| blank(&c[0]));
    let s = rx!(r"--[^\n]*").replace_all(&s, |c: &Captures| blank(&c[0]));
    let s = rx!(r"'[^'\n]*'").replace_all(&s, |c: &Captures| blank_quoted(&c[0]));
    let s = rx!(r#""[^"\n]*""#).replace_all(&s, |c: &Captures| blank_quoted(&c[0]));
    s.into_owned()
}

/// Blank `{% %}` and `{# #}` blocks, leaving `{{ }}` expressions in place.
pub fn strip_jinja(sql: &str) -> String {
    let s = rx!(r"(?s)\{%.*?%\}").replace_all(sql, |c: &Captures| blank(&c[0]));
    let s = rx!(r"(?s)\{#.*?#\}").replace_all(&s, |c: &Captures| blank(&c[0]));
    s.into_owned()
}

pub fn strip_all(sql: &str) -> String {
    strip_jinja(&strip_comments_and_strings(sql))
}

/// Clamp a byte offset to a char boundary at or before it.
pub fn floor_char(s: &str, mut i: usize) -> usize {
    i = i.min(s.len());
    while i > 0 && !s.is_char_boundary(i) {
        i -= 1;
    }
    i
}

/// 1-based line number for a byte offset.
pub fn find_line_number(content: &str, pos: usize) -> u32 {
    let pos = floor_char(content, pos);
    content[..pos].bytes().filter(|b| *b == b'\n').count() as u32 + 1
}

/// 1-based `(line, column)` for a byte offset; the column counts characters.
pub fn line_col(content: &str, pos: usize) -> (u32, u32) {
    let pos = floor_char(content, pos);
    let line_start = content[..pos].rfind('\n').map(|i| i + 1).unwrap_or(0);
    (find_line_number(content, pos), content[line_start..pos].chars().count() as u32 + 1)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TextSpan {
    pub line: u32,
    pub column: u32,
    pub end_line: u32,
    pub end_column: u32,
}

/// Position of a match, with the end clamped to the start line. A zero-width
/// match is widened to one character.
pub fn span(content: &str, start: usize, end: usize) -> TextSpan {
    let start = floor_char(content, start);
    let (line, column) = line_col(content, start);
    let line_end = content[start..].find('\n').map(|i| i + start).unwrap_or(content.len());
    let mut stop = end.max(start + 1).min(line_end);
    while stop < content.len() && !content.is_char_boundary(stop) {
        stop += 1;
    }
    let width = content[start..stop.max(start)].chars().count() as u32;
    TextSpan { line, column, end_line: line, end_column: column + width }
}

/// Read a span from the original text, collapse whitespace, and limit it to 200 characters.
pub fn raw_span(raw: &str, start: usize, end: usize) -> String {
    raw_span_limit(raw, start, end, 200)
}

pub fn raw_span_limit(raw: &str, start: usize, end: usize, limit: usize) -> String {
    let (start, end) = (floor_char(raw, start), floor_char(raw, end.max(start)));
    let collapsed = collapse_ws(&raw[start..end]);
    collapsed.chars().take(limit).collect()
}

/// Collapse runs of whitespace to one space and trim.
pub fn collapse_ws(s: &str) -> String {
    s.split_whitespace().collect::<Vec<_>>().join(" ")
}

/// Index of the `)` matching the `(` at `open`, or `None`.
pub fn match_paren(text: &str, open: usize) -> Option<usize> {
    let b = text.as_bytes();
    if open >= b.len() || b[open] != b'(' {
        return None;
    }
    let mut depth = 0i32;
    for (i, &c) in b.iter().enumerate().skip(open) {
        if c == b'(' {
            depth += 1;
        } else if c == b')' {
            depth -= 1;
            if depth == 0 {
                return Some(i);
            }
        }
    }
    None
}

/// Split on `delim`, ignoring delimiters nested in brackets. Parts are trimmed
/// and empty parts dropped.
pub fn split_top_level(text: &str, delim: char) -> Vec<String> {
    let mut parts = vec![];
    let mut depth = 0i32;
    let mut cur = String::new();
    for ch in text.chars() {
        if "([{".contains(ch) {
            depth += 1;
        } else if ")]}".contains(ch) {
            depth -= 1;
        }
        if ch == delim && depth == 0 {
            parts.push(std::mem::take(&mut cur));
        } else {
            cur.push(ch);
        }
    }
    parts.push(cur);
    parts.into_iter().map(|p| p.trim().to_string()).filter(|p| !p.is_empty()).collect()
}

/// Best-effort literal conversion; unparseable values stay as raw text.
pub fn parse_value(raw: &str) -> Value {
    let raw = raw.trim();
    let b = raw.as_bytes();
    if b.len() >= 2 && b[0] == b[b.len() - 1] && (b[0] == b'"' || b[0] == b'\'') {
        return Value::String(raw[1..raw.len() - 1].to_string());
    }
    match raw {
        "true" | "True" => return Value::Bool(true),
        "false" | "False" => return Value::Bool(false),
        _ => {}
    }
    if rx!(r"^-?\d+$").is_match(raw)
        && let Ok(n) = raw.parse::<i64>() {
            return Value::from(n);
        }
    if raw.starts_with('[') && raw.ends_with(']') && raw.len() >= 2 {
        return Value::Array(split_top_level(&raw[1..raw.len() - 1], ',').iter().map(|p| parse_value(p)).collect());
    }
    Value::String(raw.to_string())
}

pub type Config = serde_json::Map<String, Value>;

/// Collect keyword arguments from every `config(...)` call in a model.
/// Later calls override earlier values.
pub fn extract_config(raw: &str) -> Config {
    let mut config = Config::new();
    let balance = strip_comments_and_strings(raw);
    for m in rx!(r"\bconfig\s*\(").find_iter(&balance) {
        let open = m.start() + balance[m.start()..].find('(').unwrap();
        let Some(close) = match_paren(&balance, open) else { continue };
        let body = &raw[open + 1..close];
        for part in split_top_level(body, ',') {
            let Some((k, v)) = part.split_once('=') else { continue };
            let k = k.trim();
            if rx!(r"^[A-Za-z_][A-Za-z0-9_]*$").is_match(k) {
                config.insert(k.to_string(), parse_value(v));
            }
        }
    }
    config
}

/// Render a config value the way Python's `str()` would for the common shapes.
pub fn py_str(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Bool(true) => "True".into(),
        Value::Bool(false) => "False".into(),
        Value::Null => "None".into(),
        Value::Number(n) => n.to_string(),
        Value::Array(a) => format!("[{}]", a.iter().map(py_repr).collect::<Vec<_>>().join(", ")),
        Value::Object(o) => format!(
            "{{{}}}",
            o.iter().map(|(k, v)| format!("{}: {}", py_repr(&Value::String(k.clone())), py_repr(v))).collect::<Vec<_>>().join(", ")
        ),
    }
}

/// Python `repr()` for JSON-shaped values.
pub fn py_repr(v: &Value) -> String {
    match v {
        Value::String(s) => {
            if s.contains('\'') && !s.contains('"') {
                format!("\"{s}\"")
            } else {
                format!("'{}'", s.replace('\\', "\\\\").replace('\'', "\\'"))
            }
        }
        other => py_str(other),
    }
}

/// Python truthiness of a config value.
pub fn truthy(v: Option<&Value>) -> bool {
    match v {
        None | Some(Value::Null) => false,
        Some(Value::Bool(b)) => *b,
        Some(Value::String(s)) => !s.is_empty(),
        Some(Value::Number(n)) => n.as_f64() != Some(0.0),
        Some(Value::Array(a)) => !a.is_empty(),
        Some(Value::Object(o)) => !o.is_empty(),
    }
}

/// All hook bodies in a config, as `(key, body)` pairs.
pub fn config_hooks(config: &Config) -> Vec<(String, String)> {
    let mut out = vec![];
    for key in ["pre_hook", "pre-hook", "post_hook", "post-hook"] {
        match config.get(key) {
            None | Some(Value::Null) => {}
            Some(Value::Array(a)) => out.extend(a.iter().map(|i| (key.to_string(), py_str(i)))),
            Some(v) => out.push((key.to_string(), py_str(v))),
        }
    }
    out
}

pub fn ref_pattern() -> &'static Regex {
    rx!(r#"\bref\s*\(\s*['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?\s*\)"#)
}

pub fn source_pattern() -> &'static Regex {
    rx!(r#"\bsource\s*\(\s*['"]([^'"]+)['"]\s*,\s*['"]([^'"]+)['"]\s*\)"#)
}

pub fn extract_refs(raw: &str) -> Vec<String> {
    ref_pattern().captures_iter(raw).map(|c| c.get(2).or(c.get(1)).unwrap().as_str().to_string()).collect()
}

pub fn extract_sources(raw: &str) -> Vec<(String, String)> {
    source_pattern().captures_iter(raw).map(|c| (c[1].to_string(), c[2].to_string())).collect()
}

const CTE_STOPWORDS: &[&str] = &[
    "select", "from", "where", "and", "or", "not", "case", "when", "then", "else", "end", "as", "on",
    "join", "inner", "left", "right", "full", "outer", "cross", "union", "all", "group", "order", "by",
    "having", "limit", "with", "insert", "update", "delete", "cast", "over", "partition", "qualify",
    "distinct", "using", "values", "recursive",
];

#[derive(Debug, Clone)]
pub struct Cte {
    pub name: String,
    pub body: String,
    /// Bounds of the CTE name.
    pub start: usize,
    pub end: usize,
    /// Offset of the body's opening paren.
    pub open: usize,
    pub close: usize,
}

/// CTEs in stripped SQL. `start`/`end` bound the name.
pub fn extract_ctes(stripped: &str) -> Vec<Cte> {
    let mut out = vec![];
    for c in rx!(r"(?i)\b([A-Za-z_][A-Za-z0-9_]*)\s+AS\s*\(").captures_iter(stripped) {
        let name = c.get(1).unwrap();
        if CTE_STOPWORDS.contains(&name.as_str().to_lowercase().as_str()) {
            continue;
        }
        let whole = c.get(0).unwrap();
        let open = whole.end() - 1;
        let Some(close) = match_paren(stripped, open) else { continue };
        out.push(Cte {
            name: name.as_str().to_string(),
            body: stripped[open + 1..close].to_string(),
            start: whole.start(),
            end: name.end(),
            open,
            close,
        });
    }
    out
}

#[derive(Debug, Clone)]
pub struct Subquery {
    pub body: String,
    pub start: usize,
    pub end: usize,
    pub keyword: String,
    pub depth: usize,
    pub open: usize,
    pub close: usize,
}

/// Derived-table subqueries: a parenthesised SELECT directly after FROM/JOIN,
/// excluding the incremental watermark.
pub fn find_derived_subqueries(stripped: &str) -> Vec<Subquery> {
    let mut out = vec![];
    for c in rx!(r"(?i)\b(from|join)\s*\(").captures_iter(stripped) {
        let m = c.get(0).unwrap();
        let open = m.end() - 1;
        let Some(close) = match_paren(stripped, open) else { continue };
        let body = &stripped[open + 1..close];
        if !rx!(r"(?i)\bselect\b").is_match(body) || is_watermark_subquery(body) {
            continue;
        }
        out.push(Subquery {
            body: body.trim().to_string(),
            start: m.start(),
            end: m.end(),
            keyword: c[1].to_lowercase(),
            depth: count_nested_selects(body),
            open,
            close,
        });
    }
    out
}

pub fn is_watermark_subquery(body: &str) -> bool {
    if !rx!(r"(?i)\bmax\s*\(").is_match(body) {
        return false;
    }
    rx!(r"\{\{\s*this\s*\}\}").is_match(body) || body.to_lowercase().contains("this")
}

pub fn count_nested_selects(body: &str) -> usize {
    rx!(r"(?i)\bselect\b").find_iter(body).count()
}

pub fn normalize_sql(sql: &str) -> String {
    let t = strip_comments_and_strings(sql);
    collapse_ws(&t).to_lowercase()
}

pub fn fingerprint(sql: &str) -> String {
    let h = Sha256::digest(normalize_sql(sql).as_bytes());
    h.iter().take(8).map(|b| format!("{b:02x}")).collect()
}

/// Non-blank, non-comment-only lines.
pub fn significant_lines(sql: &str) -> usize {
    py_splitlines(sql).iter().filter(|l| {
        let t = l.trim();
        !t.is_empty() && !t.starts_with("--")
    }).count()
}

/// Python `str.splitlines()` for `\n`, `\r\n` and `\r`.
pub fn py_splitlines(s: &str) -> Vec<&str> {
    let mut out = vec![];
    let b = s.as_bytes();
    let (mut start, mut i) = (0, 0);
    while i < b.len() {
        match b[i] {
            b'\n' => {
                out.push(&s[start..i]);
                i += 1;
                start = i;
            }
            b'\r' => {
                out.push(&s[start..i]);
                i += if b.get(i + 1) == Some(&b'\n') { 2 } else { 1 };
                start = i;
            }
            _ => i += 1,
        }
    }
    if start < b.len() {
        out.push(&s[start..]);
    }
    out
}

#[derive(Debug, Clone)]
pub struct MacroDef {
    pub name: String,
    pub args: Vec<String>,
    pub body: String,
    pub line: u32,
    /// Bounds of the macro name.
    pub start: usize,
    pub end: usize,
    pub body_start: usize,
}

pub fn macro_def_pattern() -> &'static Regex {
    rx!(r"(?i)\{%-?\s*macro\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)")
}

pub fn test_def_pattern() -> &'static Regex {
    rx!(r"(?i)\{%-?\s*test\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
}

pub fn extract_macro_defs(raw: &str) -> Vec<MacroDef> {
    let mut out = vec![];
    for c in macro_def_pattern().captures_iter(raw) {
        let m = c.get(0).unwrap();
        let body = match raw[m.end()..].find("endmacro") {
            Some(i) => &raw[m.end()..m.end() + i],
            None => &raw[m.end()..],
        };
        let name = c.get(1).unwrap();
        out.push(MacroDef {
            name: name.as_str().to_string(),
            args: split_top_level(&c[2], ','),
            body: body.to_string(),
            line: find_line_number(raw, m.start()),
            start: name.start(),
            end: name.end(),
            body_start: m.end(),
        });
    }
    out
}

pub const JINJA_BUILTINS: &[&str] = &[
    "config", "ref", "source", "var", "env_var", "this", "target", "is_incremental", "log", "return",
    "run_query", "adapter", "exceptions", "modules", "builtins", "dbt_version", "invocation_id",
    "selected_resources", "graph", "print", "tojson", "fromjson", "toyaml", "fromyaml", "zip", "set",
    "range", "length", "loop", "dict", "list", "str", "int", "float", "bool", "none", "true", "false",
    "if", "for", "endif", "endfor", "macro", "endmacro", "test", "endtest", "snapshot", "endsnapshot",
    "materialization", "endmaterialization", "call", "endcall", "statement", "endstatement", "do",
    "else", "elif", "and", "or", "not", "in", "is", "with",
];

#[derive(Debug, Clone)]
pub struct MacroCall {
    pub name: String,
    pub bare: String,
    pub line: u32,
    pub start: usize,
    pub end: usize,
}

/// Calls to probable user macros, excluding Jinja and dbt built-ins.
pub fn extract_macro_calls(raw: &str) -> Vec<MacroCall> {
    let mut out = vec![];
    for c in rx!(r"\{[{%]-?\s*(?:do\s+)?((?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*)\s*\(").captures_iter(raw) {
        let g = c.get(1).unwrap();
        let name = g.as_str();
        let bare = name.rsplit('.').next().unwrap();
        if JINJA_BUILTINS.contains(&bare.to_lowercase().as_str()) || JINJA_BUILTINS.contains(&name.to_lowercase().as_str()) {
            continue;
        }
        out.push(MacroCall {
            name: name.to_string(),
            bare: bare.to_string(),
            line: find_line_number(raw, c.get(0).unwrap().start()),
            start: g.start(),
            end: g.end(),
        });
    }
    out
}

/// `LazyLock` re-export for rule packs that build patterns at runtime.
pub type Lazy<T> = LazyLock<T>;

/// What a byte range of SQL text is, from [`sql_regions`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Region {
    /// `-- ...` or `/* ... */`.
    Comment,
    /// `{# ... #}`.
    JinjaComment,
    /// `'...'`, with `''` as an escaped quote.
    Str,
}

/// Comment and string-literal ranges of `sql`, in order. Quote-aware, so a
/// `--` inside `'a--b'` is not a comment and a `'` inside a comment does not
/// open a string. Double-quoted identifiers are skipped over, not reported.
/// Jinja `{{ }}` and `{% %}` are code, rendered before the SQL is read: their
/// quotes are Jinja strings, so `{{ var('x') }}` is never a SQL string, and
/// `'{{ var('x') }}'` is one SQL string.
pub fn sql_regions(sql: &str) -> Vec<(usize, usize, Region)> {
    let b = sql.as_bytes();
    let mut out = vec![];
    let mut i = 0;
    let find = |from: usize, pat: &[u8]| b[from..].windows(pat.len()).position(|w| w == pat).map(|p| from + p);
    let is_jinja = |i: usize| b[i] == b'{' && matches!(b.get(i + 1), Some(b'{') | Some(b'%'));
    // The end of the `{{ }}` or `{% %}` block starting at `i`.
    let skip_jinja = |i: usize| {
        let close: &[u8] = if b[i + 1] == b'{' { b"}}" } else { b"%}" };
        let mut j = i + 2;
        while j < b.len() && !b[j..].starts_with(close) {
            if b[j] == b'\'' || b[j] == b'"' {
                let q = b[j];
                j += 1;
                while j < b.len() && b[j] != q {
                    j += if b[j] == b'\\' { 2 } else { 1 };
                }
            }
            j += 1;
        }
        (j + 2).min(b.len())
    };
    while i < b.len() {
        match b[i] {
            b'-' if b.get(i + 1) == Some(&b'-') => {
                let end = b[i..].iter().position(|&c| c == b'\n').map_or(b.len(), |p| i + p);
                out.push((i, end, Region::Comment));
                i = end;
            }
            b'/' if b.get(i + 1) == Some(&b'*') => {
                let end = find(i + 2, b"*/").map_or(b.len(), |p| p + 2);
                out.push((i, end, Region::Comment));
                i = end;
            }
            b'{' if b.get(i + 1) == Some(&b'#') => {
                let end = find(i + 2, b"#}").map_or(b.len(), |p| p + 2);
                out.push((i, end, Region::JinjaComment));
                i = end;
            }
            b'{' if is_jinja(i) => i = skip_jinja(i),
            b'\'' => {
                let mut j = i + 1;
                while j < b.len() {
                    if is_jinja(j) {
                        j = skip_jinja(j);
                        continue;
                    }
                    if b[j] == b'\'' {
                        if b.get(j + 1) == Some(&b'\'') {
                            j += 2;
                            continue;
                        }
                        break;
                    }
                    j += 1;
                }
                let end = (j + 1).min(b.len());
                out.push((i, end, Region::Str));
                i = end;
            }
            b'"' => {
                i = b[i + 1..].iter().position(|&c| c == b'"').map_or(b.len(), |p| i + p + 2);
            }
            _ => i += 1,
        }
    }
    out
}

/// The region containing byte `pos`, if any.
pub fn region_at(regions: &[(usize, usize, Region)], pos: usize) -> Option<Region> {
    let i = regions.partition_point(|r| r.1 <= pos);
    regions.get(i).filter(|r| r.0 <= pos).map(|r| r.2)
}

/// `sql` with SQL and Jinja comments removed and whitespace collapsed. String
/// literals and case are kept, so two models compare equal only when they
/// differ in comments and layout alone.
pub fn strip_comments_collapse(sql: &str) -> String {
    fn jinja_end(sql: &str, start: usize) -> usize {
        let bytes = sql.as_bytes();
        let close: &[u8] = if bytes[start + 1] == b'{' { b"}}" } else { b"%}" };
        let mut end = start + 2;
        while end < bytes.len() && !bytes[end..].starts_with(close) {
            end = if matches!(bytes[end], b'\'' | b'"') { quoted_end(sql, end, false) } else { end + 1 };
        }
        (end + 2).min(bytes.len())
    }
    fn quoted_end(sql: &str, start: usize, skip_jinja: bool) -> usize {
        let bytes = sql.as_bytes();
        let quote = bytes[start];
        let mut end = start + 1;
        while end < bytes.len() {
            if skip_jinja && (bytes[end..].starts_with(b"{{") || bytes[end..].starts_with(b"{%")) {
                end = jinja_end(sql, end);
            } else if bytes[end] == b'\\' {
                end = (end + 2).min(bytes.len());
            } else if bytes[end] == quote {
                end += 1;
                if bytes.get(end) != Some(&quote) {
                    return end;
                }
                end += 1;
            } else {
                end += 1;
            }
        }
        end
    }
    let mut out = String::with_capacity(sql.len());
    let mut at = 0;
    let mut space = false;
    let mut template_end = 0;
    while at < sql.len() {
        let rest = &sql[at..];
        let template = at < template_end;
        let comment_end = if !template && rest.starts_with("--") {
            Some(rest.find('\n').unwrap_or(rest.len()))
        } else if !template && rest.starts_with("/*") {
            Some(rest[2..].find("*/").map_or(rest.len(), |end| end + 4))
        } else if !template && rest.starts_with("{#") {
            Some(rest[2..].find("#}").map_or(rest.len(), |end| end + 4))
        } else {
            None
        };
        if let Some(end) = comment_end {
            at += end;
            space = true;
            continue;
        }
        let ch = rest.chars().next().unwrap();
        if ch.is_whitespace() {
            space = true;
            at += ch.len_utf8();
            continue;
        }
        if space && !out.is_empty() {
            out.push(' ');
        }
        space = false;
        let end = if matches!(ch, '\'' | '"' | '`') {
            quoted_end(sql, at, !template)
        } else if !template && (rest.starts_with("{{") || rest.starts_with("{%")) {
            template_end = jinja_end(sql, at);
            at + 2
        } else if let Some(body) = rest.strip_prefix("$$") {
            at + body.find("$$").map_or(rest.len(), |end| end + 4)
        } else {
            at + ch.len_utf8()
        };
        out.push_str(&sql[at..end]);
        at = end;
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn strip_keeps_offsets() {
        let s = "select 'a' -- c\n/* x\ny */ from t";
        let t = strip_all(s);
        assert_eq!(t.len(), s.len());
        assert_eq!(find_line_number(&t, t.find("from").unwrap()), 3);
    }

    #[test]
    fn config_values() {
        let c = extract_config("{{ config(materialized='table', cluster_by=['a','b'], full_refresh=true, n=3) }}");
        assert_eq!(c["materialized"], "table");
        assert_eq!(c["cluster_by"], serde_json::json!(["a", "b"]));
        assert_eq!(c["full_refresh"], true);
        assert_eq!(c["n"], 3);
    }

    #[test]
    fn span_clamps_and_widens() {
        let s = "ab\ncd";
        assert_eq!(span(s, 0, 5), TextSpan { line: 1, column: 1, end_line: 1, end_column: 3 });
        assert_eq!(span(s, 3, 3), TextSpan { line: 2, column: 1, end_line: 2, end_column: 2 });
    }

    #[test]
    fn normalization_preserves_literal_whitespace_and_escapes() {
        for literal in ["'a  b'", "'a\tb\nc'", "'it''s  --not a comment'", r"'it\'s  /*not a comment*/'", "'caf\u{e9}  value'", "'unfinished  value"] {
            let sql = format!("  select\n{literal}  ");
            assert_eq!(strip_comments_collapse(&sql), format!("select {literal}{}", if literal.ends_with('\'') { "" } else { "  " }));
        }
        assert_ne!(strip_comments_collapse("select 'a  b'"), strip_comments_collapse("select 'a b'"));
        assert_eq!(strip_comments_collapse("select /* layout */ 'a  b' -- end\n"), "select 'a  b'");
    }

    #[test]
    fn normalization_preserves_quoted_identifiers_and_dollar_strings() {
        for quoted in [r#""a  b""#, r#""a""  --b""#, r#""a\"  /*b*/""#, "`a  b`", "$$a  ' --b\n/*c*/$$"] {
            assert_eq!(strip_comments_collapse(&format!(" \nselect   {quoted}\nfrom t ")), format!("select {quoted} from t"));
        }
        assert_ne!(strip_comments_collapse(r#"select "a  b""#), strip_comments_collapse(r#"select "a b""#));
    }

    #[test]
    fn normalization_preserves_template_strings_inside_and_outside_literals() {
        for expression in ["{{ var('x', 'a  b') }}", "'{{ var('x', 'a  b') }}'", r#"{{ var("x", "a  }} b") }}"#] {
            assert_eq!(strip_comments_collapse(&format!("select\n{expression} /* layout */ as value")), format!("select {expression} as value"));
        }
        assert_ne!(strip_comments_collapse("select {{ var('x', 'a  b') }}"), strip_comments_collapse("select {{ var('x', 'a b') }}"));
    }

    #[test]
    fn regions_are_quote_aware() {
        let s = "select 'a--b', \"x--y\" -- tail 'q\n/* it's */ {{ var('k') }} '{{ var('d') }}' {# c #} 'it''s'";
        let r = sql_regions(s);
        let kinds: Vec<(&str, Region)> = r.iter().map(|&(a, b, k)| (&s[a..b], k)).collect();
        assert_eq!(
            kinds,
            vec![
                ("'a--b'", Region::Str),
                ("-- tail 'q", Region::Comment),
                ("/* it's */", Region::Comment),
                ("'{{ var('d') }}'", Region::Str),
                ("{# c #}", Region::JinjaComment),
                ("'it''s'", Region::Str),
            ]
        );
        assert_eq!(region_at(&r, s.find("{{ var('k')").unwrap()), None);
        assert_eq!(region_at(&r, s.find("tail").unwrap()), Some(Region::Comment));
        assert_eq!(strip_comments_collapse("a -- x\n  b /* y */ 'c -- d'"), "a b 'c -- d'");
    }
}
