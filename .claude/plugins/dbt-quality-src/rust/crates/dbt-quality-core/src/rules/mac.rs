//! MAC rules: macro discipline.

use std::collections::{BTreeMap, BTreeSet, HashMap};

use indexmap::IndexMap;
use serde_json::{json, Value};

use crate::discovery::{root_relative, MacroFile, ModelFile, PortfolioContext, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural_irregular, Suggestion};
use crate::sqlutil::*;
use crate::waivers::is_waived;
use crate::{frx, rx};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTMAC0001", detect: Detect::Project(mac0001) },
    Detector { code: "SSC-EWI-DBTMAC0002", detect: Detect::Project(mac0002) },
    Detector { code: "SSC-EWI-DBTMAC0003", detect: Detect::Project(mac0003) },
    Detector { code: "SSC-EWI-DBTMAC0004", detect: Detect::Project(mac0004) },
    Detector { code: "SSC-EWI-DBTMAC0005", detect: Detect::Project(mac0005) },
    Detector { code: "SSC-EWI-DBTMAC0006", detect: Detect::Project(mac0006) },
    Detector { code: "SSC-EWI-DBTMAC0007", detect: Detect::Project(mac0007) },
    Detector { code: "SSC-EWI-DBTMAC0008", detect: Detect::Model(mac0008) },
    Detector { code: "SSC-EWI-DBTMAC0009", detect: Detect::Model(mac0009) },
    Detector { code: "SSC-EWI-DBTMAC0010", detect: Detect::Portfolio(mac0010_estate) },
    Detector { code: "SSC-EWI-DBTMAC0011", detect: Detect::Model(mac0011) },
    Detector { code: "SSC-EWI-DBTMAC0012", detect: Detect::Project(mac0012) },
    Detector { code: "SSC-PRF-DBTMAC0013", detect: Detect::Portfolio(mac0013) },
    Detector { code: "SSC-EWI-DBTMAC0014", detect: Detect::Portfolio(mac0014) },
    Detector { code: "SSC-EWI-DBTMAC0015", detect: Detect::Portfolio(mac0015) },
    Detector { code: "SSC-EWI-DBTMAC0016", detect: Detect::Portfolio(mac0016) },
    Detector { code: "SSC-EWI-DBTMAC0017", detect: Detect::Portfolio(mac0017) },
    Detector { code: "SSC-FDM-DBTMAC0018", detect: Detect::Portfolio(mac0018) },
];

fn logic_markers() -> &'static regex::Regex {
    rx!(r"(?i)\{%-?\s*(?:if|for|set|do|call)\b")
}

/// Collapse whitespace runs to one space without trimming (Python `re.sub(r"\s+", " ")`).
fn squash(s: &str) -> String {
    rx!(r"\s+").replace_all(s, " ").into_owned()
}

fn head(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

type Sites = HashMap<String, Vec<(String, u32)>>;

/// Macro calls on the right side of `{% set x = name(...) %}`. The shared
/// call scan reads only `{{ name(` and `{% do name(`.
fn set_calls(raw: &str) -> Vec<(String, u32)> {
    rx!(r"\{%-?\s*set\s+[A-Za-z_][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*\s*=\s*((?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*)\s*\(")
        .captures_iter(raw)
        .filter_map(|c| {
            let name = c.get(1).unwrap().as_str();
            let bare = name.rsplit('.').next().unwrap();
            let low = bare.to_lowercase();
            (!JINJA_BUILTINS.contains(&low.as_str()) && !JINJA_BUILTINS.contains(&name.to_lowercase().as_str()))
                .then(|| (name.to_string(), find_line_number(raw, c.get(0).unwrap().start())))
        })
        .collect()
}

fn all_call_sites(project: &ProjectContext) -> Sites {
    let mut sites: Sites = HashMap::new();
    for m in &project.models {
        for c in &m.macro_calls {
            sites.entry(c.bare.clone()).or_default().push((m.relative_path.clone(), c.line));
        }
        for (name, line) in set_calls(&m.raw) {
            let bare = name.rsplit('.').next().unwrap().to_string();
            sites.entry(bare).or_default().push((m.relative_path.clone(), line));
        }
    }
    for f in &project.macros {
        for c in extract_macro_calls(&f.raw) {
            sites.entry(c.bare).or_default().push((f.relative_path.clone(), c.line));
        }
        for (name, line) in set_calls(&f.raw) {
            let bare = name.rsplit('.').next().unwrap().to_string();
            sites.entry(bare).or_default().push((f.relative_path.clone(), line));
        }
    }
    let text = py_str(&Value::Object(project.project_yml.clone()));
    for c in extract_macro_calls(&text) {
        sites.entry(c.bare).or_default().push(("dbt_project.yml".into(), 0));
    }
    for (_p, raw) in &project.snapshot_files {
        for c in extract_macro_calls(raw) {
            sites.entry(c.bare).or_default().push(("snapshots".into(), c.line));
        }
    }
    sites
}

fn macro_sig(d: &MacroDef) -> String {
    format!("{{% macro {}({}) %}}", d.name, d.args.join(", "))
}

fn mac0001(project: &ProjectContext) -> Vec<Suggestion> {
    let macro_count: usize = project.macros.iter().map(|f| f.macros.len()).sum();
    let model_count = project.model_count();
    if model_count == 0 || macro_count == 0 {
        return vec![];
    }
    let ratio = macro_count as f64 / model_count as f64;
    if ratio < project.config.macro_model_ratio {
        return vec![];
    }
    let mut defs: Vec<(&str, u32)> =
        project.macros.iter().flat_map(|f| f.macros.iter().map(move |m| (f.relative_path.as_str(), m.line))).collect();
    defs.sort();
    let related: Vec<String> = defs.iter().map(|(f, l)| format!("{f}:{l}")).collect();
    vec![Suggestion::new(
        "SSC-EWI-DBTMAC0001",
        format!(
            "{macro_count} macros for {model_count} models (ratio {ratio:.2}) meets or exceeds the local {:.2} review threshold.",
            project.config.macro_model_ratio
        ),
    )
    .file(defs[0].0)
    .line(defs[0].1)
    .ctx("related_files", json!(related))
    .evidence(format!("{macro_count} macros / {model_count} models"))
    .remediation(
        "Review whether the macros improve readability, testing, or reuse. Inline trivial wrappers only when that makes callers clearer. Check dynamic and external callers before deleting a macro. Consider a model for a reusable query when its materialization and parameter needs fit; the ratio alone does not prove poor design.",
    )
    .effort(effort::MEDIUM)]
}

fn mac0002(project: &ProjectContext) -> Vec<Suggestion> {
    let sites = all_call_sites(project);
    let mut out = vec![];
    for f in &project.macros {
        for m in &f.macros {
            let external: Vec<&(String, u32)> = sites
                .get(&m.name)
                .map(|v| v.iter().filter(|(p, _)| *p != f.relative_path).collect())
                .unwrap_or_default();
            if external.len() != 1 {
                continue;
            }
            if logic_markers().is_match(&m.body) && significant_lines(&m.body) > 10 {
                continue;
            }
            let (cp, cl) = external[0];
            out.push(
                Suggestion::new(
                    "SSC-EWI-DBTMAC0002",
                    format!("`{}` has exactly one external caller: `{cp}:{cl}`.", m.name),
                )
                .file(f.relative_path.clone())
                .span(span(&f.raw, m.start, m.end))
                .evidence(macro_sig(m))
                .remediation(format!(
                    "Consider inlining the body at `{cp}` if the extra indirection obscures the logic. Keep a single-caller macro when its name, testability, dispatch, or interface is useful. Check external and dynamic callers before deletion."
                ))
                .effort(effort::LOW)
                .ctx("caller", json!(cp))
                .ctx("caller_line", json!(cl))
                .ctx("related_files", json!([format!("{cp}:{cl}")])),
            );
        }
    }
    out
}

fn mac0003(project: &ProjectContext) -> Vec<Suggestion> {
    let sites = all_call_sites(project);
    let mut out = vec![];
    for f in &project.macros {
        for m in &f.macros {
            if rx!(r"^(snowflake__|default__|dbt_|generate_(schema|database|alias)_name$|get_custom_|test_|ref$|source$)")
                .is_match(&m.name)
            {
                continue;
            }
            if sites.get(&m.name).is_some_and(|v| !v.is_empty()) {
                continue;
            }
            out.push(
                Suggestion::new("SSC-EWI-DBTMAC0003", format!("`{}` has no detected callers in this project.", m.name))
                    .file(f.relative_path.clone())
                    .span(span(&f.raw, m.start, m.end))
                    .evidence(macro_sig(m))
                    .remediation(
                        "Check dynamic calls, package entry points, hooks, and explicit run-operation use before deleting the macro. Remove it only if it is unused. Otherwise document the caller this static scan cannot see.",
                    )
                    .effort(effort::LOW),
            );
        }
    }
    out
}

fn mac0004(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for f in &project.macros {
        for m in &f.macros {
            let body = m.body.trim();
            if body.is_empty() || logic_markers().is_match(body) {
                continue;
            }
            if significant_lines(body) > 2 {
                continue;
            }
            if strip_all(body).trim().chars().count() > 120 {
                continue;
            }
            let delegate = rx!(r"^\{\{-?\s*((?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*)\s*\([^{}]*\)\s*-?\}\}$")
                .captures(rx!(r"^-?%\}|\{%-?$").replace_all(body, "").trim())
                .map(|c| c[1].to_string());
            let msg = match &delegate {
                Some(d) => format!("`{}` only passes its arguments to `{d}`. It adds no logic of its own.", m.name),
                None => format!("`{}` wraps a single short expression with no branching or conditional logic.", m.name),
            };
            out.push(
                Suggestion::new("SSC-EWI-DBTMAC0004", msg)
                .file(f.relative_path.clone())
                .span(span(&f.raw, m.start, m.end))
                .evidence(head(&squash(body), 140))
                .remediation(
                    "Consider inlining if the macro adds indirection without a useful name or interface. Keep short macros that express a shared business rule, improve readability, or support dispatch. Body length alone is not a defect.",
                )
                .effort(effort::LOW),
            );
        }
    }
    out
}

fn mac0005(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for f in &project.macros {
        for m in &f.macros {
            if !rx!(r"(?i)\bselect\b[\s\S]{0,400}?\bfrom\b").is_match(&strip_all(&m.body)) {
                continue;
            }
            if rx!(r"^(snowflake__|default__|create_|drop_|grant_|apply_|refresh_)").is_match(&m.name) {
                continue;
            }
            out.push(
                Suggestion::new(
                    "SSC-EWI-DBTMAC0005",
                    format!(
                        "`{}` emits a full `select ... from` query, hiding the model's core logic outside the model file.",
                        m.name
                    ),
                )
                .file(f.relative_path.clone())
                .span(span(&f.raw, m.start, m.end))
                .evidence(head(&squash(m.body.trim()), 180))
                .remediation(
                    "Inspect the compiled SQL and the macro's parameters. Consider a model when the query represents a reusable dataset with a stable grain. Choose its materialization from cost, testing, and operational needs; ephemeral is one option. Keep a query-generating macro when parameterization makes that the clearer interface.",
                )
                .effort(effort::MEDIUM),
            );
        }
    }
    out
}

fn mac0006(project: &ProjectContext) -> Vec<Suggestion> {
    let re = frx!(r"(?i)\b(from|join)\s+((?!\{\{|\{%)[A-Za-z_][\w$]*(?:\.[A-Za-z_][\w$]*){1,2})\b");
    let mut out = vec![];
    for f in &project.macros {
        for m in &f.macros {
            let stripped = strip_all(&m.body);
            for c in re.captures_iter(&stripped).flatten() {
                let whole = c.get(0).unwrap();
                let reference = c.get(2).unwrap().as_str();
                let lower = reference.to_lowercase();
                if ["information_schema.", "snowflake.", "table."].iter().any(|p| lower.starts_with(p)) {
                    continue;
                }
                out.push(
                    Suggestion::new(
                        "SSC-EWI-DBTMAC0006",
                        format!(
                            "`{reference}` in `{}` is a literal relation name, bypassing `ref()` and hiding the dependency from dbt.",
                            m.name
                        ),
                    )
                    .file(f.relative_path.clone())
                    .span(span(&f.raw, m.body_start + whole.start(), m.body_start + whole.end()))
                    .evidence(whole.as_str().trim())
                    .remediation(format!(
                        "Verify the physical relation, then pass it as an argument: `{{{{ {}(ref('the_model')) }}}}` for a dbt-owned model, or use `source()` for an external input. The call records the appropriate dependency and resolves configured locations. Check producer ownership and cycles before adding a ref.",
                        m.name
                    ))
                    .effort(effort::MEDIUM),
                );
            }
        }
    }
    out
}

fn depth(defined: &BTreeMap<String, (&str, &MacroDef)>, name: &str, seen: &BTreeSet<String>) -> (usize, Vec<String>) {
    if seen.contains(name) || !defined.contains_key(name) {
        return (0, vec![]);
    }
    let (_p, m) = defined[name];
    let (mut best, mut best_chain) = (0usize, vec![]);
    for call in extract_macro_calls(&m.body) {
        let child = call.bare;
        if !defined.contains_key(&child) {
            continue;
        }
        let mut s2 = seen.clone();
        s2.insert(name.to_string());
        let (cd, cc) = depth(defined, &child, &s2);
        if cd + 1 > best {
            best = cd + 1;
            best_chain = std::iter::once(child).chain(cc).collect();
        }
    }
    (best, best_chain)
}

fn mac0007(project: &ProjectContext) -> Vec<Suggestion> {
    let mut defined: BTreeMap<String, (&str, &MacroDef)> = BTreeMap::new();
    for f in &project.macros {
        for m in &f.macros {
            defined.insert(m.name.clone(), (f.relative_path.as_str(), m));
        }
    }
    let mut out = vec![];
    for (name, (path, m)) in &defined {
        let (levels, chain) = depth(&defined, name, &BTreeSet::new());
        if levels < 2 {
            continue;
        }
        let full: Vec<String> = std::iter::once(name.clone()).chain(chain).collect();
        let joined = full.join(" -> ");
        out.push(
            Suggestion::new("SSC-EWI-DBTMAC0007", format!("`{name}` has a macro call chain with {levels} edges: {joined}."))
                .file(*path)
                .line(m.line)
                .evidence(joined)
                .remediation(
                    "Collapse thin pass-through macros into their caller so the SQL is reachable in fewer hops. Keep layers only when each encapsulates a distinct decision, such as dialect dispatch.",
                )
                .effort(effort::MEDIUM)
                .ctx("chain", json!(full)),
        );
    }
    out
}

fn mac0008(model: &ModelFile, _project: &ProjectContext) -> Vec<Suggestion> {
    if model.is_python {
        return vec![];
    }
    if significant_lines(&model.raw) < 5 {
        return vec![];
    }
    let body = rx!(r"\{\{-?\s*config\s*\([\s\S]*?\)\s*-?\}\}").replace_all(&model.raw, "").into_owned();
    let sql_lines = significant_lines(&strip_all(&body));
    let body_lines = significant_lines(&body);
    let jinja_lines = body_lines.saturating_sub(sql_lines);
    let sets = set_calls(&body);
    let user_calls: Vec<&str> = model
        .macro_calls
        .iter()
        .map(|c| c.name.as_str())
        .chain(sets.iter().map(|(n, _)| n.as_str()))
        .filter(|n| !n.starts_with("dbt_"))
        .collect();
    if (jinja_lines as f64) / (body_lines.max(1) as f64) < 0.5 || user_calls.len() < 2 {
        return vec![];
    }
    let names: BTreeSet<&str> = user_calls.iter().copied().collect();
    let distinct = names.len();
    let evidence = names.into_iter().take(6).collect::<Vec<_>>().join(", ");
    vec![Suggestion::new(
        "SSC-EWI-DBTMAC0008",
        format!(
            "{jinja_lines} of {body_lines} body lines are Jinja, with {} to {}. Inspect compiled SQL and whether the abstraction makes the transformation harder to review.",
            plural_irregular(user_calls.len(), "non-dbt_ macro call", "non-dbt_ macro calls"),
            plural_irregular(distinct, "macro", "macros")
        ),
    )
    .file(model.relative_path.clone())
    .line(1)
    .evidence(evidence)
    .remediation(
        "Move the core transformation back into SQL and keep macros at the edges: shared predicates, column lists, or audit-column blocks. If the generation is dynamic, add a comment with a representative compiled output so readers understand intent without running dbt.",
    )
    .effort(effort::HIGH)]
}

fn mac0009(model: &ModelFile, _project: &ProjectContext) -> Vec<Suggestion> {
    if model.is_python {
        return vec![];
    }
    let hash = rx!(r"(?i)\b(?:hash|md5(?:_binary)?|sha1(?:_binary)?|sha2(?:_binary)?)\s*\(");
    let fk = rx!(r"(?i)\b[\w$]*(?:_id|_key)\b");
    let mut out = vec![];
    for m in hash.find_iter(&model.stripped) {
        let open = m.end() - 1;
        let Some(close) = match_paren(&model.stripped, open) else { continue };
        let expr = &model.stripped[m.start()..=close];
        if !fk.is_match(expr) {
            continue;
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTMAC0009",
                "A hash expression contains key-shaped column names. Review its identity semantics and measured join or pruning behavior.",
            )
            .file(model.relative_path.clone())
            .span(span(&model.raw, m.start(), close + 1))
            .evidence(head(&squash(expr), 140))
            .remediation(
                "Verify which columns define identity and where the hash is used. Inspect query profiles before attributing a performance problem to hashing. Consider original-key joins only when they preserve identity, null handling, and data types. Do not replace a hash with naive concatenation; delimiters, nulls, and collisions need a deliberate encoding contract. Add appropriate relationship tests.",
            )
            .effort(effort::LOW),
        );
    }
    out
}

type Blocks = IndexMap<String, Vec<(String, u32)>>;

/// Every sliding window of meaningful SQL lines, keyed by normalised text.
fn sql_blocks(project: &ProjectContext) -> Blocks {
    let window_size = project.config.duplicate_block_min_lines;
    let mut blocks: Blocks = IndexMap::new();
    if window_size >= 1 {
        let w = window_size as usize;
        for model in &project.models {
            if model.is_python {
                continue;
            }
            let masked = mask_scaffolding(&restore_refs(&model.stripped, &model.raw));
            let meaningful: Vec<(u32, &str)> = py_splitlines(&masked)
                .into_iter()
                .enumerate()
                .map(|(i, l)| (i as u32 + 1, l.trim()))
                .filter(|(_, l)| !l.is_empty())
                .collect();
            if meaningful.len() < w {
                continue;
            }
            for start in 0..=(meaningful.len() - w) {
                let window = &meaningful[start..start + w];
                let text = window.iter().map(|(_, l)| *l).collect::<Vec<_>>().join(" ");
                if text.chars().count() < 80 {
                    continue;
                }
                let key = squash(&text).to_lowercase();
                blocks.entry(key).or_default().push((model.relative_path.clone(), window[0].0));
            }
        }
    }
    blocks
}

/// Blank `{{ config(...) }}` calls and `{% ... %}` tags, keeping line numbers.
/// Converters emit these as boilerplate. PRJ0009, INC0019 and MAT0008 own them.
fn mask_scaffolding(text: &str) -> String {
    let blank = |m: &regex::Captures| m[0].chars().map(|c| if c == '\n' { c } else { ' ' }).collect::<String>();
    let t = rx!(r"(?s)\{\{-?\s*config\s*\(.*?\)\s*-?\}\}").replace_all(text, blank);
    rx!(r"(?s)\{%.*?%\}").replace_all(&t, blank).into_owned()
}

/// Copy string literals back from the raw text. The blanking makes every
/// `ref('x')`, `var('x')` and `'X' as flag` equal, so blocks that read
/// different models or emit different constants would get one key.
/// Offsets do not change, because the blanking keeps the length.
fn restore_refs(stripped: &str, raw: &str) -> String {
    let mut out = stripped.to_string();
    for m in rx!(r#"'[^'\n]*'|"[^"\n]*""#).find_iter(stripped) {
        if raw.is_char_boundary(m.start()) && raw.is_char_boundary(m.end()) {
            out.replace_range(m.range(), &raw[m.range()]);
        }
    }
    out
}

/// True when a window holds only a pass-through select list: identifiers,
/// `alias.col` and `x as y` items, commas, `select [distinct]`, parentheses,
/// and a bare `from <relation> [as alias]` with no join or filter.
/// No logic sits in such a block.
fn is_pass_through(key: &str) -> bool {
    const KW: &[&str] = &["where", "join", "left", "right", "inner", "outer", "full", "cross", "group", "order", "union", "having", "qualify", "limit", "on", "lateral"];
    let body = rx!(r#"\bfrom\s+(\{\{.*?\}\}|[\w."]+)(?:\s+(?:as\s+)?([\w"]+))?"#).replace_all(key, |c: &regex::Captures| match c.get(2) {
        Some(a) if KW.contains(&a.as_str()) => format!(", {}", a.as_str()),
        _ => ",".to_string(),
    });
    // A relation at a window edge (`... from` / `{{ ref(..) }} ) select ...`) is not logic.
    let body = rx!(r"\bfrom\s*$").replace(&body, "");
    let body = rx!(r#"\{\{\s*(?:ref|source)\s*\([^)]*\)\s*\}\}"#).replace_all(&body, ",");
    // A function call or operator is logic.
    if rx!(r"\w\s*\(|[-+*/|=<>]").is_match(&body) {
        return false;
    }
    let body = rx!(r"[()]|\bselect\s+(?:distinct\s+)?").replace_all(&body, ",");
    let item = rx!(r#"^[\w"]+(?:\.[\w"]+)?(?:\s+(?:as\s+)?[\w"]+)?$"#);
    body.split(',').map(str::trim).all(|i| i.is_empty() || item.is_match(i))
}

/// One repeated window: its anchor, every (project, file, line) hit, and its text.
struct Win {
    anchor: (usize, String),
    line: u32,
    hits: Vec<(usize, String, u32)>,
    key: String,
    cross: bool,
}

/// One finding per (anchor file, contiguous region). A cross-project window
/// replaces the per-project windows with the same text, because its file set
/// contains theirs. Overlapping windows in one anchor file merge, whatever
/// their file sets; the finding lists the union of files.
fn mac0010_estate(p: &PortfolioContext) -> Vec<Suggestion> {
    let threshold = p.config.duplicate_block_threshold;
    let w = p.config.duplicate_block_min_lines.max(1) as u32;
    let mut all: IndexMap<String, Vec<(usize, String, u32)>> = IndexMap::new();
    for (pi, project) in p.projects.iter().enumerate() {
        for (key, hits) in sql_blocks(project) {
            all.entry(key).or_default().extend(hits.into_iter().map(|(f, l)| (pi, f, l)));
        }
    }
    let mut wins: Vec<Win> = vec![];
    for (key, hits) in all {
        // Pass-through column lists are not extracted: the fix is to keep them
        // as generated, or to consolidate the models themselves.
        if is_pass_through(&key) {
            continue;
        }
        let projects: BTreeSet<usize> = hits.iter().map(|h| h.0).collect();
        if projects.len() >= 2 {
            let (pi, f, l) = hits[0].clone();
            wins.push(Win { anchor: (pi, f), line: l, hits, key, cross: true });
            continue;
        }
        let files: BTreeSet<&String> = hits.iter().map(|h| &h.1).collect();
        if (files.len() as i64) >= threshold {
            let (pi, f, l) = hits[0].clone();
            wins.push(Win { anchor: (pi, f), line: l, hits, key, cross: false });
        }
    }
    wins.sort_by(|a, b| (&a.anchor, a.line).cmp(&(&b.anchor, b.line)));
    // (first window of the region, last window line, window count)
    let mut regions: Vec<(Win, u32, usize)> = vec![];
    for win in wins {
        match regions.last_mut() {
            // A gap shorter than one window (a changed column) does not split the block.
            Some((r, last, n)) if r.anchor == win.anchor && win.line <= *last + 2 * w => {
                *last = (*last).max(win.line);
                r.hits.extend(win.hits);
                r.cross |= win.cross;
                *n += 1;
            }
            _ => {
                let l = win.line;
                regions.push((win, l, 1));
            }
        }
    }
    // One finding per (anchor file, scope): the regions of one file are one edit pass.
    type Region = (Win, u32, usize);
    let mut groups: IndexMap<((usize, String), bool), Vec<Region>> = IndexMap::new();
    for r in regions {
        groups.entry((r.0.anchor.clone(), r.0.cross)).or_default().push(r);
    }
    let mut out = vec![];
    for (((api, afile), cross), regs) in groups {
        // Each hit is its own occurrence. Merge only hits that sit in one
        // contiguous run (the same rule as the region merge above).
        let mut lines: BTreeMap<(usize, String), BTreeSet<u32>> = BTreeMap::new();
        for (r, _, _) in &regs {
            for (pi, f, l) in &r.hits {
                lines.entry((*pi, f.clone())).or_default().insert(*l);
            }
        }
        let mut per_file: BTreeMap<(usize, String), Vec<(u32, u32)>> = BTreeMap::new();
        for (k, ls) in lines {
            let rs = per_file.entry(k).or_default();
            for l in ls {
                match rs.last_mut() {
                    Some((_, b)) if l <= *b + 1 + w => *b = (*b).max(l + w - 1),
                    _ => rs.push((l, l + w - 1)),
                }
            }
        }
        let anchor_ranges = per_file.get(&(api, afile.clone())).cloned().unwrap_or_default();
        let detail: Vec<_> = anchor_ranges.iter().map(|(a, b)| json!({"lines": format!("{a}-{b}")})).collect();
        let locs: Vec<String> = per_file
            .iter()
            .map(|((pi, f), rs)| {
                let rs: Vec<String> = rs.iter().map(|(a, b)| format!("{a}-{b}")).collect();
                format!("{}:{}", root_relative(&p.projects[*pi], f), rs.join(","))
            })
            .collect();
        let related: Vec<String> = per_file
            .iter()
            .filter_map(|((pi, f), rs)| rs.first().map(|(a, _)| format!("{}:{a}", root_relative(&p.projects[*pi], f))))
            .collect();
        let projects: BTreeSet<usize> = per_file.keys().map(|k| k.0).collect();
        let pnames: Vec<&str> = projects.iter().map(|i| p.projects[*i].label.as_str()).collect();
        let shown = format!("{}{}", locs.iter().take(5).cloned().collect::<Vec<_>>().join(", "), if locs.len() > 5 { " ..." } else { "" });
        let lines: Vec<String> = anchor_ranges.iter().map(|(a, b)| format!("{a}-{b}")).collect();
        let what = if lines.len() == 1 { format!("An identical SQL block (lines {})", lines[0]) } else { format!("{} identical SQL blocks (lines {})", lines.len(), lines.join(", ")) };
        let project = &p.projects[api];
        let (appear, repeat) = if lines.len() == 1 { ("appears", "repeats") } else { ("appear", "repeat") };
        let (msg, fix) = if cross {
            (
                format!("{what} {appear} in {} models across {} projects ({shown}).", locs.len(), projects.len()),
                "Verify that the repeated blocks have the same meaning and ownership before sharing them. Use a package macro for parameterized expressions. For a shared dataset, choose an appropriate model materialization and configure supported cross-project dependencies. Cross-project refs and ephemeral reuse are not interchangeable in every runtime.",
            )
        } else {
            (
                format!("{what} {repeat} in {} models ({shown}).", locs.len()),
                "Extract the block when one definition improves maintenance without hiding different business meanings. Consider a macro for shared expressions or a model for a reusable dataset. Choose ephemeral only when its testing and performance limits fit the callers.",
            )
        };
        let windows: usize = regs.iter().map(|r| r.2).sum();
        let mut s = Suggestion::new("SSC-EWI-DBTMAC0010", msg)
            .line(anchor_ranges.first().map_or(regs[0].0.line, |r| r.0))
            .file(afile)
            .in_project(project)
            .evidence(head(&regs[0].0.key, 200))
            .remediation(fix)
            .effort(effort::MEDIUM)
            .ctx("repeated_in", json!(locs))
            .ctx("related_files", json!(related))
            .ctx("regions", json!(detail))
            .ctx("windows", json!(windows));
        if cross {
            s = s.ctx("cross_project", json!(true)).ctx("projects", json!(pnames));
        }
        if !is_waived(&s, Some(project), Some(&p.config)) {
            out.push(s);
        }
    }
    out
}

fn mac0011(model: &ModelFile, _project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for c in rx!(r"(?i)\{%-?\s*macro\s+([A-Za-z_]\w*)").captures_iter(&model.raw) {
        let g = c.get(1).unwrap();
        let name = g.as_str();
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTMAC0011",
                format!("`{name}` is defined inside a model file. Move shared macro definitions to a configured macro path."),
            )
            .file(model.relative_path.clone())
            .span(span(&model.raw, g.start(), g.end()))
            .evidence(c.get(0).unwrap().as_str().trim())
            .remediation(format!("Move it to `<configured macro path>/{name}.sql` (`macros/` by default). Keep the model file focused on its output query and verify the callers after the move."))
            .effort(effort::LOW),
        );
    }
    out
}

fn mac0012(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for f in &project.macros {
        if f.macros.len() != 1 {
            continue;
        }
        let m = &f.macros[0];
        let stem = f.path.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();
        if stem == m.name {
            continue;
        }
        let fname = f.path.file_name().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTMAC0012",
                format!("`{fname}` contains one macro named `{}`. Matching the filename to the macro is the local navigation convention, not a dbt requirement.", m.name),
            )
            .file(f.relative_path.clone())
            .span(span(&f.raw, m.start, m.end))
            .evidence(format!("{fname} -> {}()", m.name))
            .remediation(format!("Rename the file to `{}.sql`.", m.name))
            .effort(effort::LOW),
        );
    }
    out
}

// ---------------------------------------------------------------------------
// Estate-wide macro rules (MAC0013-MAC0018)
// ---------------------------------------------------------------------------

struct Em<'a> {
    project: &'a ProjectContext,
    file: &'a MacroFile,
    def: &'a crate::sqlutil::MacroDef,
}

impl Em<'_> {
    fn at(&self) -> (u32, u32) {
        line_col(&self.file.raw, self.def.start)
    }
    fn param_names(&self) -> Vec<String> {
        self.def
            .args
            .iter()
            .filter_map(|a| rx!(r"^\s*\*{0,2}([A-Za-z_]\w*)").captures(a).map(|c| c[1].to_string()))
            .collect()
    }
}

fn estate_macros(p: &PortfolioContext) -> Vec<Em<'_>> {
    let mut out = vec![];
    for project in &p.projects {
        for file in &project.macros {
            for def in &file.macros {
                out.push(Em { project, file, def });
            }
        }
    }
    out
}

/// A call from a model to a macro, by bare name.
struct Site<'a> {
    project: &'a ProjectContext,
    model: &'a ModelFile,
    line: u32,
    pos: usize,
}

fn model_sites(p: &PortfolioContext) -> HashMap<String, Vec<Site<'_>>> {
    let mut out: HashMap<String, Vec<Site>> = HashMap::new();
    for project in &p.projects {
        for model in &project.models {
            for c in &model.macro_calls {
                out.entry(c.bare.clone()).or_default().push(Site { project, model, line: c.line, pos: c.start });
            }
        }
    }
    out
}

/// True when byte `pos` lies inside a `config(...)` call, i.e. a hook argument.
fn in_config(model: &ModelFile, pos: usize) -> bool {
    model
        .jinja
        .calls_named("config")
        .any(|c| (c.span.start_offset as usize) <= pos && pos <= c.span.end_offset as usize)
}

fn site_json(s: &Site) -> Value {
    json!({"project": s.project.label, "file": root_relative(s.project, &s.model.relative_path), "line": s.line})
}

fn strip_macro_comments(s: &str) -> String {
    let s = rx!(r"(?s)\{#.*?#\}").replace_all(s, " ");
    rx!(r"--[^\n]*").replace_all(&s, " ").into_owned()
}

fn norm_body(s: &str) -> String {
    squash(strip_macro_comments(s).trim()).to_lowercase()
}

/// Keep a suggestion unless an inline or configured waiver covers it.
fn keep(p: &PortfolioContext, project: &ProjectContext, s: Suggestion) -> Option<Suggestion> {
    let s = s.in_project(project);
    (!is_waived(&s, Some(project), Some(&p.config))).then_some(s)
}

fn mac0013(p: &PortfolioContext) -> Vec<Suggestion> {
    let sites = model_sites(p);
    let mut out = vec![];
    for em in estate_macros(p) {
        let body = strip_macro_comments(&em.def.body);
        let body = rx!(r"^\s*-?%\}").replace(&body, "");
        let body = rx!(r"\{%-?\s*$").replace(&body, "");
        let body = squash(body.trim());
        let Some(m) = rx!(r"(?is)^\(\s*select\s+(max|min|any_value)\s*\(.*?\)\s+from\s+.*?\bwhere\b(.*)\)$").captures(&body)
        else {
            continue;
        };
        let params = em.param_names();
        let where_part = m.get(2).map_or("", |g| g.as_str());
        let uses_param = rx!(r"\{\{[^}]*\}\}")
            .find_iter(where_part)
            .any(|t| params.iter().any(|a| rx!(r"[A-Za-z_]\w*").find_iter(t.as_str()).any(|w| w.as_str() == a)));
        if !uses_param {
            continue;
        }
        let callers: Vec<&Site> = sites
            .get(&em.def.name)
            .map(|v| v.iter().filter(|s| in_select_list(&s.model.raw, s.pos)).collect())
            .unwrap_or_default();
        if callers.is_empty() {
            continue;
        }
        let name = &em.def.name;
        let s = Suggestion::new(
            "SSC-PRF-DBTMAC0013",
            format!(
                "Macro `{name}` returns a scalar subquery (`{}`) and {} select {}; inspect correlation and the query plan before assuming repeated lookup work.",
                m[1].to_uppercase(),
                callers.len(),
                if callers.len() == 1 { "list calls it" } else { "lists call it" },
            ),
        )
        .file(em.file.relative_path.clone())
        .at(em.at())
        .evidence(head(&body, 200))
        .effort(effort::MEDIUM)
        .ctx("macro", name.as_str())
        .ctx("caller_count", json!(callers.len()))
        .ctx("callers", json!(callers.iter().take(10).map(|s| site_json(s)).collect::<Vec<_>>()));
        out.extend(keep(p, em.project, s));
    }
    out
}

/// True when the last clause keyword before `pos` is `select`.
fn in_select_list(raw: &str, pos: usize) -> bool {
    let head = &raw[..floor_char(raw, pos)];
    rx!(r"(?i)\b(select|from|where|join|group\s+by|having|qualify|order\s+by|on)\b")
        .find_iter(head)
        .last()
        .is_some_and(|m| m.as_str().eq_ignore_ascii_case("select"))
}

fn mac0014(p: &PortfolioContext) -> Vec<Suggestion> {
    let sites = model_sites(p);
    let macros = estate_macros(p);
    // callee name -> macros that call it
    let mut callers_of: HashMap<String, BTreeSet<String>> = HashMap::new();
    for em in &macros {
        for c in extract_macro_calls(&em.def.body) {
            callers_of.entry(c.bare).or_default().insert(em.def.name.clone());
        }
    }
    let mut out = vec![];
    for em in &macros {
        let body = norm_body(&em.def.body);
        if !rx!(r"\b(?:run_query|statement|adapter\.execute)\s*\(|\{%-?\s*call\s+statement\b").is_match(&body) {
            continue;
        }
        let Some(effect) = rx!(
            r#"\b(?:insert\s+(?:overwrite\s+)?into|update\s+(?:\{\{.*?\}\}|\S+)\s+set|delete\s+from|merge\s+into|truncate\s+table|truncate\s+(?:\{\{|\w+\.)|use\s+(?:warehouse|role|schema|database)\b|alter\s+session|execute\s+immediate)"#
        )
        .find(&body) else {
            continue;
        };
        let mut seen: BTreeSet<String> = BTreeSet::from([em.def.name.clone()]);
        let mut queue = vec![em.def.name.clone()];
        while let Some(n) = queue.pop() {
            for c in callers_of.get(&n).into_iter().flatten() {
                if seen.insert(c.clone()) {
                    queue.push(c.clone());
                }
            }
        }
        let callers: Vec<&Site> = seen
            .iter()
            .flat_map(|n| sites.get(n).into_iter().flatten())
            .filter(|s| !in_config(s.model, s.pos))
            .collect();
        if callers.is_empty() {
            continue;
        }
        let name = &em.def.name;
        let s = Suggestion::new(
            "SSC-EWI-DBTMAC0014",
            format!(
                "Macro `{name}` runs `{}` through run_query/statement and is called from {} model {}, directly or through other macros.",
                effect.as_str(),
                callers.len(),
                if callers.len() == 1 { "call site" } else { "call sites" },
            ),
        )
        .file(em.file.relative_path.clone())
        .at(em.at())
        .evidence(head(effect.as_str(), 200))
        .effort(effort::MEDIUM)
        .ctx("macro", name.as_str())
        .ctx("statement", effect.as_str())
        .ctx("caller_count", json!(callers.len()))
        .ctx("callers", json!(callers.iter().take(10).map(|s| site_json(s)).collect::<Vec<_>>()));
        out.extend(keep(p, em.project, s));
    }
    out
}

const NAME_MACROS: &[&str] = &["generate_schema_name", "generate_alias_name", "generate_database_name"];

fn mac0015(p: &PortfolioContext) -> Vec<Suggestion> {
    let defs: Vec<Em> = estate_macros(p).into_iter().filter(|e| NAME_MACROS.contains(&e.def.name.as_str())).collect();
    let mut out = vec![];
    for em in &defs {
        let name = em.def.name.as_str();
        let body = norm_body(&em.def.body);
        let same: Vec<&Em> = defs.iter().filter(|o| o.def.name == name).collect();
        let owners: BTreeSet<&str> = same.iter().map(|o| o.project.name.as_str()).collect();
        let bodies: BTreeSet<String> = same.iter().map(|o| norm_body(&o.def.body)).collect();
        let others: Vec<&str> = owners.iter().copied().filter(|n| *n != em.project.name).collect();
        let mut msg = format!(
            "Project `{}` defines `{name}`, which can affect relation naming across its resources. Check root-project delegation, resource support, and branch behavior before consolidation.",
            em.project.name
        );
        if bodies.len() > 1 {
            msg.push_str(&format!(
                " {} projects in the estate define it with {} different bodies (also in: {}).",
                owners.len(),
                bodies.len(),
                others.join(", ")
            ));
        }
        let s = Suggestion::new("SSC-EWI-DBTMAC0015", msg)
            .file(em.file.relative_path.clone())
            .at(em.at())
            .evidence(head(&body, 200))
            .effort(effort::MEDIUM)
            .ctx("macro", name)
            .ctx("differing_bodies", json!(bodies.len() > 1))
            .ctx("projects", json!(owners));
        out.extend(keep(p, em.project, s));
    }
    out
}

fn mac0016(p: &PortfolioContext) -> Vec<Suggestion> {
    // (project index, name, kind label, file, byte offset, normalised body)
    let mut defs: Vec<(&ProjectContext, String, &MacroFile, usize, String)> = vec![];
    for em in estate_macros(p) {
        if rx!(r"^get_incremental_\w+_sql$").is_match(&em.def.name) {
            defs.push((em.project, em.def.name.clone(), em.file, em.def.start, norm_body(&em.def.body)));
        }
    }
    for project in &p.projects {
        for file in &project.macros {
            for m in rx!(r"(?i)\{%-?\s*materialization\s+([A-Za-z_]\w*)").captures_iter(&file.raw) {
                let g = m.get(1).unwrap();
                let body = file.raw[g.end()..].split("endmaterialization").next().unwrap_or("");
                defs.push((project, format!("materialization {}", g.as_str()), file, g.start(), norm_body(body)));
            }
        }
    }
    let mut out = vec![];
    for (project, name, file, pos, body) in &defs {
        let same: Vec<_> = defs.iter().filter(|d| &d.1 == name).collect();
        let owners: BTreeSet<&str> = same.iter().map(|d| d.0.name.as_str()).collect();
        if owners.len() < 2 {
            continue;
        }
        let identical = same.iter().all(|d| &d.4 == body);
        let others: Vec<&str> = owners.iter().copied().filter(|n| *n != project.name).collect();
        let s = Suggestion::new(
            "SSC-EWI-DBTMAC0016",
            format!(
                "`{name}` is defined in {} projects ({}); the copies have {} bodies.",
                owners.len(),
                owners.iter().copied().collect::<Vec<_>>().join(", "),
                if identical { "identical" } else { "different" }
            ),
        )
        .file(file.relative_path.clone())
        .at(line_col(&file.raw, *pos))
        .evidence(head(body, 200))
        .effort(effort::MEDIUM)
        .ctx("macro", name.as_str())
        .ctx("identical_bodies", json!(identical))
        .ctx("projects", json!(owners))
        .ctx("other_projects", json!(others));
        out.extend(keep(p, project, s));
    }
    out
}

fn mac0017(p: &PortfolioContext) -> Vec<Suggestion> {
    let sites = model_sites(p);
    let mut out = vec![];
    for project in &p.projects {
        for file in &project.macros {
            for call in file.jinja.calls_named("var") {
                let Some(mname) = call.in_macro.as_deref() else { continue };
                let foreign: Vec<&Site> = sites
                    .get(mname)
                    .map(|v| {
                        v.iter()
                            .filter(|s| {
                                s.project.name != project.name
                                    && !s.project.macros.iter().any(|f| f.macros.iter().any(|d| d.name == mname))
                            })
                            .collect()
                    })
                    .unwrap_or_default();
                if foreign.is_empty() {
                    continue;
                }
                let var = match call.args.first() {
                    Some(crate::jinja::Lit::Str(s)) => s.clone(),
                    Some(crate::jinja::Lit::Expr(s)) => s.clone(),
                    _ => String::new(),
                };
                let users: BTreeSet<&str> = foreign.iter().map(|s| s.project.label.as_str()).collect();
                let s = Suggestion::new(
                    "SSC-EWI-DBTMAC0017",
                    format!(
                        "Macro `{mname}` reads `var('{var}')` and models of {} other {} call it ({}); the var has one name for every caller.",
                        users.len(),
                        if users.len() == 1 { "project" } else { "projects" },
                        users.iter().copied().collect::<Vec<_>>().join(", ")
                    ),
                )
                .file(file.relative_path.clone())
                .at((call.span.start_line, call.span.start_col))
                .evidence(head(&collapse_ws(&strip_span(&file.raw, call.span.start_offset, call.span.end_offset)), 200))
                .effort(effort::MEDIUM)
                .ctx("var_name", var.as_str())
                .ctx("macro", mname)
                .ctx("caller_projects", json!(users))
                .ctx("callers", json!(foreign.iter().take(10).map(|s| site_json(s)).collect::<Vec<_>>()));
                out.extend(keep(p, project, s));
            }
        }
    }
    out
}

fn strip_span(raw: &str, start: u32, end: u32) -> String {
    let (s, e) = (floor_char(raw, start as usize), floor_char(raw, (end as usize).max(start as usize)));
    raw[s..e].to_string()
}

/// Normalised argument text of the call whose name ends at `end`.
fn call_args(raw: &str, end: usize) -> Option<String> {
    let rest = &raw[end..];
    let open = end + (rest.len() - rest.trim_start().len());
    let close = match_paren(raw, open)?;
    Some(collapse_ws(&raw[open + 1..close]))
}

fn mac0018(p: &PortfolioContext) -> Vec<Suggestion> {
    // bare name -> (project, file, line, args)
    let mut calls: HashMap<String, Vec<(&ProjectContext, String, u32, String)>> = HashMap::new();
    for project in &p.projects {
        for m in &project.models {
            for c in &m.macro_calls {
                if let Some(a) = call_args(&m.raw, c.end) {
                    calls.entry(c.bare.clone()).or_default().push((project, m.relative_path.clone(), c.line, a));
                }
            }
        }
        for f in &project.macros {
            for c in extract_macro_calls(&f.raw) {
                if let Some(a) = call_args(&f.raw, c.end) {
                    calls.entry(c.bare).or_default().push((project, f.relative_path.clone(), c.line, a));
                }
            }
        }
    }
    let mut out = vec![];
    for em in estate_macros(p) {
        let name = &em.def.name;
        let body = strip_macro_comments(&em.def.body);
        let Some(param) = em.param_names().into_iter().find(|a| {
            let a = regex::escape(a);
            let access = format!(r"(?is)\{{%-?\s*(?:for|if|elif)\b[^%]*?\b{a}(?:\.(?:get|items|keys|values)\s*\(|\[)");
            let iter = format!(r"(?is)\{{%-?\s*for\b[^%]*?\bin\s+[^%(]*?\b{a}\b");
            regex::Regex::new(&access).is_ok_and(|r| r.is_match(&body)) || regex::Regex::new(&iter).is_ok_and(|r| r.is_match(&body))
        }) else {
            continue;
        };
        // Own definition lines are not call sites.
        let mine: Vec<_> = calls
            .get(name)
            .map(|v| v.iter().filter(|c| !(c.0.name == em.project.name && c.1 == em.file.relative_path && c.2 == em.def.line)).collect())
            .unwrap_or_default();
        let distinct: BTreeSet<&str> = mine.iter().map(|c| c.3.as_str()).collect();
        if mine.len() < 2 || distinct.len() < 2 {
            continue;
        }
        let s = Suggestion::new(
            "SSC-FDM-DBTMAC0018",
            format!(
                "Macro `{name}` loops or branches on argument `{param}`, and {} call sites pass {} different argument sets. Compare resolved values and compiled SQL; different argument text need not produce different output.",
                mine.len(),
                distinct.len()
            ),
        )
        .file(em.file.relative_path.clone())
        .at(em.at())
        .evidence(head(distinct.iter().next().copied().unwrap_or(""), 200))
        .effort(effort::MEDIUM)
        .ctx("macro", name.as_str())
        .ctx("parameter", param.as_str())
        .ctx("call_site_count", json!(mine.len()))
        .ctx("distinct_argument_sets", json!(distinct.len()))
        .ctx(
            "call_sites",
            json!(mine
                .iter()
                .take(10)
                .map(|c| json!({"project": c.0.name, "file": c.1, "line": c.2}))
                .collect::<Vec<_>>()),
        );
        out.extend(keep(p, em.project, s));
    }
    out
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const LONG_SQL: &str = "select\n  coalesce(a_very_long_column_name_one, 0) as a_very_long_column_name_one,\n  a_very_long_column_name_two,\n  a_very_long_column_name_three,\n  a_very_long_column_name_four\nfrom {{ ref('src') }}\n";

    fn n(t: &TempProject, code: &str) -> usize {
        t.findings(code).len()
    }

    #[test]
    fn mac_set_calls_count_as_callers() {
        let m = ("macros/h.sql", "{% macro h(x) %}{{ x }}{% endmacro %}");
        let t = TempProject::new(&[m, ("models/a.sql", "{% set r = h('a') %}\nselect {{ r }}")]);
        assert_eq!(n(&t, "SSC-EWI-DBTMAC0003"), 0);
        let f = t.findings("SSC-EWI-DBTMAC0002");
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].context["related_files"][0], "models/a.sql:1");
        let t = TempProject::new(&[m, ("models/a.sql", "{% set r = h('a') %}\nselect {{ h('b') }}")]);
        assert_eq!(n(&t, "SSC-EWI-DBTMAC0002"), 0);
    }

    #[test]
    fn mac0002_related_file_uses_caller_line() {
        let m = ("macros/h.sql", "{% macro h(x) %}{{ x }}{% endmacro %}");
        let t = TempProject::new(&[m, ("models/a.sql", "-- header\nselect\n  1,\n  {{ h('a') }}\nfrom t")]);
        let f = t.findings("SSC-EWI-DBTMAC0002");
        assert_eq!(f[0].context["related_files"][0], "models/a.sql:4", "{f:?}");
        let t = TempProject::new(&[m, ("models/a.sql", "-- header\n{% set r = h('a') %}\nselect {{ r }}")]);
        let f = t.findings("SSC-EWI-DBTMAC0002");
        assert_eq!(f[0].context["related_files"][0], "models/a.sql:2", "{f:?}");
    }

    #[test]
    fn mac0001_points_at_macro_files() {
        let t = TempProject::new(&[("models/a.sql", "select 1"), ("macros/m.sql", "{% macro m() %}1{% endmacro %}")]);
        let f = t.findings("SSC-EWI-DBTMAC0001");
        assert_eq!(f[0].context["related_files"][0], "macros/m.sql:1", "{f:?}");
        assert!(!f[0].file.ends_with('/'), "{f:?}");
    }

    #[test]
    fn mac0004_delegation_message() {
        let t = TempProject::new(&[("macros/a.sql", "{% macro a(x) %}{{ b(x) }}{% endmacro %}")]);
        let f = t.findings("SSC-EWI-DBTMAC0004");
        assert!(f[0].message.contains("passes its arguments to `b`"), "{f:?}");
    }

    #[test]
    fn mac0008_counts_set_calls() {
        let src = "{% set a = m1('x') %}\n{% set b = m2('y') %}\n{% set c = m1('z') %}\n{% set d = 4 %}\nselect 1\n";
        let t = TempProject::new(&[("models/a.sql", src)]);
        let f = t.findings("SSC-EWI-DBTMAC0008");
        assert_eq!(f.len(), 1);
        assert!(f[0].message.contains("3 non-dbt_ macro calls to 2 macros"), "{f:?}");
        assert_eq!(f[0].line, Some(1));
    }

    #[test]
    fn mac0010_lists_all_files() {
        let t = TempProject::new(&[("models/a.sql", LONG_SQL), ("models/b.sql", LONG_SQL), ("models/c.sql", LONG_SQL)]);
        let f = t.findings("SSC-EWI-DBTMAC0010");
        assert_eq!(f[0].context["related_files"].as_array().unwrap().len(), 3, "{f:?}");
    }

    #[test]
    fn mac0001() {
        let c = "SSC-EWI-DBTMAC0001";
        let t = TempProject::new(&[("models/a.sql", "select 1"), ("macros/m.sql", "{% macro m() %}1{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("models/a.sql", "select 1"), ("models/b.sql", "select 2"), ("models/c.sql", "select 3")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0002() {
        let c = "SSC-EWI-DBTMAC0002";
        let m = ("macros/helper.sql", "{% macro helper(x) %}{{ x }} + 1{% endmacro %}");
        let t = TempProject::new(&[m, ("models/a.sql", "select {{ helper(1) }}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[m, ("models/a.sql", "select {{ helper(1) }}"), ("models/b.sql", "select {{ helper(2) }}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0003() {
        let c = "SSC-EWI-DBTMAC0003";
        let t = TempProject::new(&[("macros/helper.sql", "{% macro helper(x) %}{{ x }}{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("macros/snowflake__helper.sql", "{% macro snowflake__helper(x) %}{{ x }}{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0004() {
        let c = "SSC-EWI-DBTMAC0004";
        let t = TempProject::new(&[("macros/cents.sql", "{% macro cents(x) %}{{ x }} * 100{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("macros/cents.sql", "{% macro cents(x) %}{% if x %}{{ x }}{% endif %}{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0005() {
        let c = "SSC-EWI-DBTMAC0005";
        let t = TempProject::new(&[("macros/q.sql", "{% macro q(r) %}select a, b from {{ r }}{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("macros/create_q.sql", "{% macro create_q(r) %}select a, b from {{ r }}{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0006() {
        let c = "SSC-EWI-DBTMAC0006";
        let t = TempProject::new(&[("macros/q.sql", "{% macro q() %}select a from raw.sales.orders{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("macros/q.sql", "{% macro q() %}select a from information_schema.tables{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0007() {
        let c = "SSC-EWI-DBTMAC0007";
        let t = TempProject::new(&[
            ("macros/a.sql", "{% macro a() %}{{ b() }}{% endmacro %}"),
            ("macros/b.sql", "{% macro b() %}{{ c() }}{% endmacro %}"),
            ("macros/c.sql", "{% macro c() %}{{ d() }}{% endmacro %}"),
            ("macros/d.sql", "{% macro d() %}1{% endmacro %}"),
        ]);
        assert!(n(&t, c) >= 1);
        let t = TempProject::new(&[
            ("macros/a.sql", "{% macro a() %}{{ b() }}{% endmacro %}"),
            ("macros/b.sql", "{% macro b() %}1{% endmacro %}"),
        ]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0008() {
        let c = "SSC-EWI-DBTMAC0008";
        let heavy = "{% do m1() %}\n{% do m2() %}\n{% set c = 3 %}\n{% set d = 4 %}\nselect 1\n";
        let t = TempProject::new(&[("models/a.sql", heavy)]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("models/a.sql", "select\n a,\n b,\n c,\n d\nfrom t\n")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0009() {
        let c = "SSC-EWI-DBTMAC0009";
        let t = TempProject::new(&[("models/a.sql", "select md5(customer_id || order_id) as k from t")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("models/a.sql", "select md5(name || city) as diff from t")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0010() {
        let c = "SSC-EWI-DBTMAC0010";
        let t = TempProject::new(&[("models/a.sql", LONG_SQL), ("models/b.sql", LONG_SQL), ("models/c.sql", LONG_SQL)]);
        // Every window of one repeated block merges into one finding.
        assert_eq!(n(&t, c), 1);
        // Converter config() headers are not compared.
        let hdr = "{{ config(\n tags=['a'],\n database=var('d'),\n schema=var('s'),\n alias=var('a')\n) }}\n{{ config(materialized='table') }}\nselect 1";
        let t = TempProject::new(&[("models/a.sql", hdr), ("models/b.sql", hdr), ("models/c.sql", hdr)]);
        assert_eq!(n(&t, c), 0);
        let t = TempProject::new(&[("models/a.sql", LONG_SQL), ("models/b.sql", LONG_SQL)]);
        assert_eq!(n(&t, c), 0);
        // A pass-through select list is not a macro candidate.
        let cols = "select\n  t.a_very_long_column_name_one as a_very_long_column_name_one,\n  a_very_long_column_name_two,\n  a_very_long_column_name_three,\n  a_very_long_column_name_four,\n  a_very_long_column_name_five,\n  a_very_long_column_name_six\n";
        let t = TempProject::new(&[("models/a.sql", cols), ("models/b.sql", cols), ("models/c.sql", cols)]);
        assert_eq!(n(&t, c), 0);
        assert!(super::is_pass_through("select a, t.b as b, c,"));
        assert!(!super::is_pass_through("a, b, coalesce(c, 0) as c"));
        // cisco MT_BKGS_COST_MEASURE1 shape: a list that ends in a bare `from`.
        assert!(super::is_pass_through("acquisition_order_origin_cd, acquisition_role from {{ ref('stg_raw__sq_x') }} ) select sd.a as a,"));
        // Informatica shape: `from <source> as <alias>`.
        assert!(super::is_pass_through("a, b, c from source_3 as sd"));
        assert!(super::is_pass_through("sd.a as a, sd.b as b, sd.c as c from"));
        assert!(super::is_pass_through("{{ ref('stg_x') }} ) select sd.k as k,"));
        assert!(!super::is_pass_through("a, b from t where a = 1"));
        assert!(!super::is_pass_through("a, b from t join u on t.id = u.id"));
        // Lists over different models are not one block.
        let over = |m: &str| format!("select\n  coalesce(a_very_long_column_name_one, 0) as one,\n  a_very_long_column_name_two,\n  a_very_long_column_name_three,\n  a_very_long_column_name_four\nfrom {{{{ ref('{m}') }}}}\nwhere 1 = 1\n");
        let t = TempProject::new(&[("models/a.sql", &over("m1")), ("models/b.sql", &over("m2")), ("models/c.sql", &over("m3"))]);
        let f = t.findings(c);
        assert_eq!(f.len(), 1, "{f:?}");
        // Windows that hold the `ref()` line differ, so the block stops before it.
        assert_eq!(f[0].context["regions"][0]["lines"], "1-5", "{f:?}");
        let t = TempProject::new(&[("models/a.sql", &over("m1")), ("models/b.sql", &over("m1")), ("models/c.sql", &over("m1"))]);
        assert_eq!(t.findings(c)[0].context["regions"][0]["lines"], "1-7");
    }

    #[test]
    fn mac0010_two_occurrences_in_one_file() {
        let c = "SSC-EWI-DBTMAC0010";
        let filler = "select 1 as x1,\n2 as x2,\n3 as x3,\n4 as x4,\n5 as x5,\n6 as x6,\n7 as x7,\n8 as x8,\n9 as x9,\n10 as x10,\n11 as x11,\n12 as x12\n";
        let twice = format!("{LONG_SQL}union all\n{filler}union all\n{LONG_SQL}");
        let t = TempProject::new(&[("models/a.sql", &twice), ("models/b.sql", LONG_SQL), ("models/c.sql", LONG_SQL)]);
        let f = t.findings(c);
        assert_eq!(f.len(), 1, "{f:?}");
        let regions: Vec<String> = f[0].context["regions"].as_array().unwrap().iter().map(|r| r["lines"].as_str().unwrap().to_string()).collect();
        assert_eq!(regions.len(), 2, "{regions:?}");
        let anchor = f[0].context["repeated_in"].as_array().unwrap().iter().map(|v| v.as_str().unwrap().to_string()).find(|l| l.contains("models/a.sql")).unwrap();
        assert!(anchor.ends_with(&regions.join(",")), "{anchor} vs {regions:?}");
        for r in &regions {
            assert!(f[0].message.contains(r.as_str()), "{}", f[0].message);
        }
    }

    #[test]
    fn mac0011() {
        let c = "SSC-EWI-DBTMAC0011";
        let t = TempProject::new(&[("models/a.sql", "{% macro inline_helper() %}1{% endmacro %}\nselect 1")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("models/a.sql", "select 1")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0012() {
        let c = "SSC-EWI-DBTMAC0012";
        let t = TempProject::new(&[("macros/other.sql", "{% macro real_name() %}1{% endmacro %}")]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[("macros/real_name.sql", "{% macro real_name() %}1{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    fn two(a: &[(&str, &str)], b: &[(&str, &str)]) -> TempProject {
        let mut files: Vec<(String, String)> = vec![];
        for (pre, set) in [("a", a), ("b", b)] {
            files.push((format!("{pre}/dbt_project.yml"), format!("name: {pre}\nversion: '1.0'\nprofile: demo\n")));
            for (p, c) in set.iter() {
                files.push((format!("{pre}/{p}"), c.to_string()));
            }
        }
        let refs: Vec<(&str, &str)> = files.iter().map(|(p, c)| (p.as_str(), c.as_str())).collect();
        TempProject::new(&refs)
    }

    #[test]
    fn mac0010_cross_project() {
        let c = "SSC-EWI-DBTMAC0010";
        let t = two(&[("models/a.sql", LONG_SQL)], &[("models/b.sql", LONG_SQL)]);
        let f = t.findings(c);
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].context["cross_project"], true);
        let t = two(&[("models/a.sql", LONG_SQL)], &[("models/b.sql", "select 1")]);
        assert_eq!(n(&t, c), 0);
        // A cross-project block covers the per-project repeats of the same text.
        let three = [("models/a.sql", LONG_SQL), ("models/b.sql", LONG_SQL), ("models/c.sql", LONG_SQL)];
        let f = two(&three, &[("models/d.sql", LONG_SQL)]).findings(c);
        assert_eq!(f.len(), 1, "{f:?}");
        assert_eq!(f[0].context["repeated_in"].as_array().unwrap().len(), 4);
    }

    const LOOKUP: &str = "{% macro lookup_rate(code) %}\n(select max(rate) from {{ ref('rates') }} where currency = {{ code }})\n{% endmacro %}";

    #[test]
    fn mac0013() {
        let c = "SSC-PRF-DBTMAC0013";
        let t = TempProject::new(&[
            ("macros/lookup_rate.sql", LOOKUP),
            ("models/m.sql", "select o.id, {{ lookup_rate('o.currency') }} as rate from {{ ref('orders') }} o"),
        ]);
        assert_eq!(n(&t, c), 1);
        assert_eq!(t.findings(c)[0].context["caller_count"], 1);
        let t = TempProject::new(&[("macros/lookup_rate.sql", LOOKUP), ("models/m.sql", "select 1")]);
        assert_eq!(n(&t, c), 0);
        let t = TempProject::new(&[
            ("macros/lookup_rate.sql", LOOKUP),
            ("models/m.sql", "select 1 from {{ ref('o') }} where x = {{ lookup_rate('1') }}"),
        ]);
        assert_eq!(n(&t, c), 0);
    }

    const DML: &str = "{% macro log_run() %}{% do run_query(\"insert into audit.runs values (1)\") %}{% endmacro %}";

    #[test]
    fn mac0014() {
        let c = "SSC-EWI-DBTMAC0014";
        let t = TempProject::new(&[("macros/l.sql", DML), ("models/m.sql", "{{ log_run() }}\nselect 1")]);
        assert_eq!(n(&t, c), 1);
        let wrap = "{% macro outer() %}{{ log_run() }}{% endmacro %}";
        let t = TempProject::new(&[("macros/l.sql", DML), ("macros/o.sql", wrap), ("models/m.sql", "{{ outer() }} select 1")]);
        assert_eq!(n(&t, c), 1);
        let sel = "{% macro cols() %}{% set r = run_query('select 1') %}{% endmacro %}";
        let t = TempProject::new(&[("macros/c.sql", sel), ("models/m.sql", "{{ cols() }} select 1")]);
        assert_eq!(n(&t, c), 0);
        let t = TempProject::new(&[("macros/l.sql", DML), ("models/m.sql", "{{ config(pre_hook=\"{{ log_run() }}\") }} select 1")]);
        assert_eq!(n(&t, c), 0);
        let t = TempProject::new(&[("macros/l.sql", DML), ("models/m.sql", "select 1")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0015() {
        let c = "SSC-EWI-DBTMAC0015";
        let one = "{% macro generate_schema_name(custom, node) %}{{ custom }}{% endmacro %}";
        let t = TempProject::new(&[("macros/g.sql", one)]);
        assert_eq!(n(&t, c), 1);
        assert_eq!(t.findings(c)[0].context["differing_bodies"], false);
        let other = "{% macro generate_schema_name(custom, node) %}{{ target.schema }}_{{ custom }}{% endmacro %}";
        let t = two(&[("macros/g.sql", one)], &[("macros/g.sql", other)]);
        let f = t.findings(c);
        assert_eq!(f.len(), 2);
        assert_eq!(f[0].context["differing_bodies"], true);
        let t = TempProject::new(&[("macros/g.sql", "{% macro helper() %}1{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0016() {
        let c = "SSC-EWI-DBTMAC0016";
        let m = "{% macro get_incremental_update_only_sql(arg_dict) %}merge into x{% endmacro %}";
        let t = two(&[("macros/s.sql", m)], &[("macros/s.sql", m)]);
        assert_eq!(n(&t, c), 2);
        assert_eq!(t.findings(c)[0].context["identical_bodies"], true);
        let t = two(&[("macros/s.sql", m)], &[("macros/s.sql", "{% macro other() %}1{% endmacro %}")]);
        assert_eq!(n(&t, c), 0);
    }

    const VARMAC: &str = "{% macro mp_filter(x) %}{{ x }} + {{ var('mp_min') }}{% endmacro %}";

    #[test]
    fn mac0017() {
        let c = "SSC-EWI-DBTMAC0017";
        let t = two(&[("macros/mp.sql", VARMAC)], &[("models/m.sql", "select {{ mp_filter('id') }} as v")]);
        let f = t.findings(c);
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].context["var_name"], "mp_min");
        let t = two(&[("macros/mp.sql", VARMAC), ("models/m.sql", "select {{ mp_filter('id') }}")], &[("models/n.sql", "select 1")]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn mac0018() {
        let c = "SSC-FDM-DBTMAC0018";
        let m = "{% macro mp(src) %}{% for c in src.get('cols', []) %}{{ c }},{% endfor %}id{% endmacro %}";
        let t = TempProject::new(&[
            ("macros/mp.sql", m),
            ("models/a.sql", "select {{ mp({'cols': ['a']}) }} from t"),
            ("models/b.sql", "select {{ mp({'cols': ['b', 'c']}) }} from t"),
        ]);
        assert_eq!(n(&t, c), 1);
        let t = TempProject::new(&[
            ("macros/mp.sql", m),
            ("models/a.sql", "select {{ mp({'cols': ['a']}) }} from t"),
            ("models/b.sql", "select {{ mp({'cols': ['a']}) }} from t"),
        ]);
        assert_eq!(n(&t, c), 0);
    }
}
