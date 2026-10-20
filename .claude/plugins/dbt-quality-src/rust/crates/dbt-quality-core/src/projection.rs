//! Output columns of a dbt model's outer SELECT.
//!
//! Input: raw model SQL with Jinja. Output: one `Projection` per item in the
//! first top-level SELECT list, with byte spans into the raw text.
//! Method: blank Jinja, comments and strings (offsets stay the same), then
//! scan by parenthesis depth. Names and literals are read from the raw text.
//! Simplification: the outer SELECT is the first SELECT at depth 0. A
//! top-level UNION is not followed; only its first branch is read.

use std::sync::LazyLock;

use regex::Regex;

use crate::jinja::blank_jinja;
use crate::sqlutil::{find_line_number, floor_char, match_paren, strip_comments_and_strings};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ProjectionKind {
    /// A checkable expression with a known output name.
    Named,
    /// `*` or `t.*`.
    Star,
    /// No alias and not a plain column reference.
    Unaliased,
    /// Only Jinja, e.g. `{{ dbt_utils.star(...) }}`.
    Jinja,
}

#[derive(Debug, Clone)]
pub struct Projection {
    pub kind: ProjectionKind,
    /// Output name. Exact when quoted, else as written.
    pub alias: Option<String>,
    pub alias_quoted: bool,
    /// Raw alias text, quotes included.
    pub alias_raw: Option<String>,
    /// Raw `AS` keyword, for casing. `None` for implicit aliases.
    pub as_keyword: Option<String>,
    /// The expression without an outer cast or collation.
    pub inner: String,
    /// Type of an outer `CAST(.. AS t)`, `TRY_CAST` or `::t`.
    pub cast_type: Option<String>,
    /// Literal of a trailing `COLLATE '..'` or an outer `COLLATE(x, '..')`.
    pub collation: Option<String>,
    /// Byte range of the projection code, from first to last code character.
    pub span: (usize, usize),
    pub line: u32,
}

const KEYWORDS: &[&str] = &[
    "END", "NULL", "TRUE", "FALSE", "AND", "OR", "NOT", "IS", "IN", "LIKE", "ILIKE", "BETWEEN", "THEN", "ELSE", "WHEN",
    "CASE", "DISTINCT", "OVER", "ASC", "DESC", "FIRST", "LAST", "NULLS",
];

static IDENT: LazyLock<Regex> = LazyLock::new(|| Regex::new(r#"^(?:[A-Za-z_][A-Za-z0-9_$]*|"[^"]*")$"#).unwrap());
static COLUMN_REF: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r#"^(?:(?:[A-Za-z_][A-Za-z0-9_$]*|"[^"]*")\s*\.\s*)*([A-Za-z_][A-Za-z0-9_$]*|"[^"]*")$"#).unwrap()
});
static TRAILING_COLLATE: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?i)\bCOLLATE\s*'[^']*'\s*$").unwrap());

/// Offsets-preserving mask. Comments and string contents become spaces.
/// Jinja bytes become `~`, so Jinja counts as code but holds no words or brackets.
pub fn mask(raw: &str) -> String {
    let blanked = blank_jinja(raw);
    let marked: Vec<u8> = raw.bytes().zip(blanked.bytes()).map(|(r, b)| if r != b { b'~' } else { r }).collect();
    strip_comments_and_strings(&String::from_utf8_lossy(&marked))
}

/// Projections of the first top-level SELECT, or empty when none is found.
pub fn projections(raw: &str) -> Vec<Projection> {
    let m = mask(raw);
    let Some((start, end)) = select_list(&m) else { return vec![] };
    split_depth0(&m, start, end, b',').into_iter().filter_map(|(s, e)| parse(raw, &m, s, e)).collect()
}

/// Byte range of the outer SELECT list in the mask.
pub fn select_list(m: &str) -> Option<(usize, usize)> {
    let words = depth0_words(m, 0, m.len());
    let sel = words.iter().position(|(_, w)| w.eq_ignore_ascii_case("SELECT"))?;
    let mut start = words[sel].0 + 6;
    let mut i = sel + 1;
    while let Some((p, w)) = words.get(i) {
        let w = w.to_ascii_uppercase();
        if w == "DISTINCT" || w == "ALL" {
            start = p + w.len();
            i += 1;
        } else if w == "TOP" {
            start = words.get(i + 1).map_or(p + 3, |(q, n)| q + n.len());
            i += 2;
        } else {
            break;
        }
    }
    let end = words[i..]
        .iter()
        .find(|(_, w)| ["FROM", "WHERE", "GROUP", "QUALIFY", "UNION", "ORDER", "LIMIT"].iter().any(|k| w.eq_ignore_ascii_case(k)))
        .map_or_else(|| m[start..].find(';').map_or(m.len(), |e| start + e), |(p, _)| *p);
    Some((start, end))
}

/// Words at depth 0 in `m[start..end]`, as `(offset, text)`.
fn depth0_words(m: &str, start: usize, end: usize) -> Vec<(usize, &str)> {
    let b = m.as_bytes();
    let (mut out, mut depth, mut i) = (vec![], 0i32, start);
    while i < end {
        match b[i] {
            b'(' | b'[' | b'{' => depth += 1,
            b')' | b']' | b'}' => depth -= 1,
            b'"' | b'\'' => {
                let q = b[i];
                i += 1;
                while i < end && b[i] != q {
                    i += 1;
                }
            }
            c if c.is_ascii_alphabetic() || c == b'_' => {
                let s = i;
                while i < end && (b[i].is_ascii_alphanumeric() || b[i] == b'_' || b[i] == b'$') {
                    i += 1;
                }
                let prev_dot = s > 0 && b[s - 1] == b'.';
                if depth == 0 && !prev_dot {
                    out.push((s, &m[s..i]));
                }
                continue;
            }
            _ => {}
        }
        i += 1;
    }
    out
}

/// Split `m[start..end]` on a byte at depth 0.
fn split_depth0(m: &str, start: usize, end: usize, delim: u8) -> Vec<(usize, usize)> {
    let b = m.as_bytes();
    let (mut out, mut depth, mut seg) = (vec![], 0i32, start);
    let mut i = start;
    while i < end {
        match b[i] {
            b'(' | b'[' | b'{' => depth += 1,
            b')' | b']' | b'}' => depth -= 1,
            b'"' | b'\'' => {
                let q = b[i];
                i += 1;
                while i < end && b[i] != q {
                    i += 1;
                }
            }
            c if c == delim && depth == 0 => {
                out.push((seg, i));
                seg = i + 1;
            }
            _ => {}
        }
        i += 1;
    }
    out.push((seg, end));
    out
}

/// Trim ASCII whitespace from a mask range. Masked comments are spaces, so they trim too.
fn trim(m: &str, s: usize, e: usize) -> (usize, usize) {
    let b = m.as_bytes();
    let (mut s, mut e) = (s, e);
    while s < e && b[s].is_ascii_whitespace() {
        s += 1;
    }
    while e > s && b[e - 1].is_ascii_whitespace() {
        e -= 1;
    }
    (s, e)
}

fn raw_at(raw: &str, s: usize, e: usize) -> String {
    raw[floor_char(raw, s)..floor_char(raw, e)].to_string()
}

fn ident_name(raw_ident: &str) -> (String, bool) {
    match raw_ident.strip_prefix('"').and_then(|s| s.strip_suffix('"')) {
        Some(inner) => (inner.to_string(), true),
        None => (raw_ident.to_string(), false),
    }
}

fn parse(raw: &str, m: &str, s: usize, e: usize) -> Option<Projection> {
    let (cs, ce) = trim(m, s, e);
    if cs >= ce {
        return None;
    }
    let line = find_line_number(raw, cs);
    let mut p = Projection {
        kind: ProjectionKind::Unaliased,
        alias: None,
        alias_quoted: false,
        alias_raw: None,
        as_keyword: None,
        inner: String::new(),
        cast_type: None,
        collation: None,
        span: (cs, ce),
        line,
    };
    let code = &m[cs..ce];
    if code.bytes().all(|c| c == b'~' || c.is_ascii_whitespace()) {
        p.kind = ProjectionKind::Jinja;
        return Some(p);
    }
    if code == "*" || code.ends_with(".*") {
        p.kind = ProjectionKind::Star;
        return Some(p);
    }
    // Explicit alias: the last depth-0 `AS` followed only by one identifier.
    let mut expr_end = ce;
    if let Some((as_pos, _)) = depth0_words(m, cs, ce).into_iter().rev().find(|(_, w)| w.eq_ignore_ascii_case("AS")) {
        let (ns, ne) = trim(m, as_pos + 2, ce);
        let name_raw = raw_at(raw, ns, ne);
        if IDENT.is_match(&name_raw) {
            p.as_keyword = Some(raw_at(raw, as_pos, as_pos + 2));
            set_alias(&mut p, &name_raw);
            expr_end = trim(m, cs, as_pos).1;
        }
    }
    if p.alias.is_none() {
        let code_raw = raw_at(raw, cs, ce);
        if let Some(c) = COLUMN_REF.captures(&code_raw) {
            // Bare column reference: dbt names the output after the last part.
            set_alias(&mut p, &c[1]);
            p.alias_raw = None;
        } else if let Some(&(ws, w)) = depth0_words(m, cs, ce).last() {
            // Implicit alias: `expr name`, where `name` ends the projection.
            let before = m[cs..ws].trim_end();
            let implicit = ws + w.len() == ce
                && before.len() < ws - cs
                && !before.is_empty()
                && !before.ends_with(|c: char| "+-*/|=<>,.:(".contains(c))
                && !KEYWORDS.iter().any(|k| w.eq_ignore_ascii_case(k));
            if implicit {
                set_alias(&mut p, w);
                expr_end = cs + before.len();
            }
        }
        // A quoted implicit alias, e.g. `a + 1 "X"`.
        if p.alias.is_none()
            && code.ends_with('"')
            && let Some(q) = m[cs..ce - 1].rfind('"')
        {
            let before = m[cs..cs + q].trim_end();
            if !before.is_empty() && before.len() < q {
                set_alias(&mut p, &raw_at(raw, cs + q, ce));
                expr_end = cs + before.len();
            }
        }
    }
    if p.alias.is_none() {
        p.inner = raw_at(raw, cs, ce);
        return Some(p);
    }
    p.kind = ProjectionKind::Named;
    let (mut es, mut ee) = (cs, expr_end);
    // Trailing `COLLATE '<x>'`.
    if let Some(mt) = TRAILING_COLLATE.find(&m[es..ee]) {
        let lit = raw_at(raw, es + mt.start(), es + mt.end());
        p.collation = lit.split('\'').nth(1).map(str::to_string);
        ee = trim(m, es, es + mt.start()).1;
    } else if let Some(inner) = outer_call(m, es, ee, "COLLATE") {
        // Function form `COLLATE(x, '<c>')`.
        let parts = split_depth0(m, inner.0, inner.1, b',');
        if parts.len() == 2 {
            p.collation = Some(raw_at(raw, parts[1].0, parts[1].1).trim().trim_matches('\'').to_string());
            (es, ee) = trim(m, parts[0].0, parts[0].1);
        }
    }
    // Outer cast.
    if let Some(inner) = outer_call(m, es, ee, "CAST").or_else(|| outer_call(m, es, ee, "TRY_CAST")) {
        if let Some((as_pos, _)) = depth0_words(m, inner.0, inner.1).into_iter().rev().find(|(_, w)| w.eq_ignore_ascii_case("AS")) {
            p.cast_type = Some(collapse(&raw_at(raw, as_pos + 2, inner.1)));
            (es, ee) = trim(m, inner.0, as_pos);
        }
    } else if let Some(pos) = rfind_depth0(m, es, ee, "::") {
        p.cast_type = Some(collapse(&raw_at(raw, pos + 2, ee)));
        ee = trim(m, es, pos).1;
    }
    p.inner = raw_at(raw, es, ee);
    Some(p)
}

fn set_alias(p: &mut Projection, raw_name: &str) {
    let (name, quoted) = ident_name(raw_name);
    p.alias = Some(name);
    p.alias_quoted = quoted;
    p.alias_raw = Some(raw_name.to_string());
}

fn collapse(s: &str) -> String {
    crate::sqlutil::collapse_ws(s).replace("( ", "(").replace(" )", ")").replace(", ", ",")
}

/// When `m[s..e]` is exactly `NAME( ... )`, return the argument range.
fn outer_call(m: &str, s: usize, e: usize, name: &str) -> Option<(usize, usize)> {
    let head = &m[s..e];
    if head.len() <= name.len() || !head[..name.len()].eq_ignore_ascii_case(name) {
        return None;
    }
    let open = s + name.len() + (head[name.len()..].len() - head[name.len()..].trim_start().len());
    if m.as_bytes().get(open) != Some(&b'(') {
        return None;
    }
    let close = match_paren(&m[..e], open)?;
    (close + 1 == e).then_some((open + 1, close))
}

fn rfind_depth0(m: &str, s: usize, e: usize, needle: &str) -> Option<usize> {
    let b = m.as_bytes();
    let (mut depth, mut found, mut i) = (0i32, None, s);
    while i < e {
        match b[i] {
            b'(' | b'[' | b'{' => depth += 1,
            b')' | b']' | b'}' => depth -= 1,
            _ if depth == 0 && m[i..e].starts_with(needle) => {
                found = Some(i);
                i += needle.len();
                continue;
            }
            _ => {}
        }
        i += 1;
    }
    found
}

#[cfg(test)]
mod tests {
    use super::*;

    fn one(sql: &str) -> Vec<Projection> {
        projections(sql)
    }

    #[test]
    fn reads_alias_cast_and_collation_after_a_cte() {
        let sql = "with a as (select x as y from t)\nselect\n  cast(a.id as number(10, 0)) As ID,\n  name collate 'en-ci' as NAME, -- note, here\n  amount::decimal(18,2) amount,\n  a.code,\n  \"Mixed\" as \"Mixed\"\nfrom {{ ref('a') }} a";
        let p = one(sql);
        assert_eq!(p.len(), 5, "{p:#?}");
        assert_eq!(p[0].alias.as_deref(), Some("ID"));
        assert_eq!(p[0].as_keyword.as_deref(), Some("As"));
        assert_eq!(p[0].cast_type.as_deref(), Some("number(10,0)"));
        assert_eq!(p[0].inner, "a.id");
        assert_eq!(p[0].line, 3);
        assert_eq!(p[1].collation.as_deref(), Some("en-ci"));
        assert_eq!(p[1].inner, "name");
        assert_eq!(p[2].alias.as_deref(), Some("amount"));
        assert!(p[2].as_keyword.is_none());
        assert_eq!(p[2].cast_type.as_deref(), Some("decimal(18,2)"));
        assert_eq!(p[3].alias.as_deref(), Some("code"));
        assert!(p[3].alias_raw.is_none());
        assert_eq!(p[4].alias.as_deref(), Some("Mixed"));
        assert!(p[4].alias_quoted);
        assert_eq!(&sql[p[1].span.0..p[1].span.1], "name collate 'en-ci' as NAME");
    }

    #[test]
    fn function_collate_nested_cast_and_jinja() {
        let sql = "select distinct\n  collate(cast(x as varchar(5)), 'en-ci-rtrim') as X,\n  cast(coalesce(cast(y as int), 0) as int) as Y,\n  {{ dbt_utils.star(ref('a')) }},\n  coalesce({{ var('d') }}, 'a, b') as Z,\n  a + b,\n  t.*\nfrom t";
        let p = one(sql);
        assert_eq!(p[0].collation.as_deref(), Some("en-ci-rtrim"));
        assert_eq!(p[0].cast_type.as_deref(), Some("varchar(5)"));
        assert_eq!(p[0].inner, "x");
        assert_eq!(p[1].cast_type.as_deref(), Some("int"));
        assert_eq!(p[1].inner, "coalesce(cast(y as int), 0)");
        assert_eq!(p[2].kind, ProjectionKind::Jinja);
        assert_eq!(p[3].alias.as_deref(), Some("Z"));
        assert_eq!(p[4].kind, ProjectionKind::Unaliased);
        assert_eq!(p[5].kind, ProjectionKind::Star);
        assert_eq!(p.len(), 6);
    }

    #[test]
    fn case_end_without_alias_is_unaliased() {
        let p = one("select case when a then 1 else 2 end from t");
        assert_eq!(p[0].kind, ProjectionKind::Unaliased);
        let p = one("select case when a then 1 end flag, 'x' \"Q\" from t");
        assert_eq!(p[0].alias.as_deref(), Some("flag"));
        assert_eq!(p[1].alias.as_deref(), Some("Q"));
    }
}
