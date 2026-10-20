//! Shared helpers for the merge-collision rules (PRJ0019-PRJ0022) and the
//! location advice of PRJ0009 and SQL0006.
//!
//! - Where a source or model points: [`resolve_location`], [`model_relation`],
//!   compared with [`compare_locations`].
//! - Calls and model dependencies: [`call_sites`], [`producers`], [`RefGraph`].
//! - Relation names built from `var()`: [`var_relation_reads`].
//! - The recommended source block: [`source_block_for`] and
//!   [`render_source_location`]. Every rule that names a source block uses
//!   these, so two findings about one table never name different blocks.
//!
//! Location values are compared case-insensitively unless quoted, as
//! Snowflake does for unquoted identifiers.

use std::collections::{BTreeMap, BTreeSet, VecDeque};

use serde_json::Value;

use super::{declared_vars, lit_text, project_sources, var_reads};
use crate::discovery::{root_relative, source_decls, ModelFile, PortfolioContext, ProjectContext, SourceDecl, SourceTableDecl};
use crate::jinja::Lit;
use crate::provenance::PLACEHOLDER_VALUES;
use crate::rx;
use crate::sqlutil::{line_col, match_paren, py_str, region_at, sql_regions, strip_comments_collapse};

// ---- Location values ----

/// One part of a location (database, schema, or identifier) after resolving
/// `var()` and `env_var()` defaults.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Part {
    /// A literal, or a var or env var whose value or default is one.
    Known(String),
    /// A generated placeholder such as `YOUR_DB`.
    Placeholder(String),
    /// Not set, so dbt uses the target's database or schema.
    Target,
    /// No usable value; the text says why.
    Unknown(String),
}

/// A [`Part`] and its source information.
#[derive(Debug, Clone)]
pub struct LocPart {
    pub value: Part,
    /// The `var()` key the value came from.
    pub var: Option<String>,
    /// The value as written, if set.
    pub raw: Option<String>,
    /// Compare case-sensitively: quoted with `"`, or `quoting:` is true.
    pub quoted: bool,
}

impl LocPart {
    pub fn known(&self) -> Option<&str> {
        match &self.value {
            Part::Known(s) => Some(s),
            _ => None,
        }
    }

    /// The value for comparison and map keys: upper-cased unless quoted.
    pub fn key(&self) -> Option<String> {
        match &self.value {
            Part::Known(s) | Part::Placeholder(s) => Some(if self.quoted { s.clone() } else { s.to_uppercase() }),
            _ => None,
        }
    }

    fn describe(&self, what: &str) -> String {
        let from = self.var.as_ref().map_or(String::new(), |v| format!(" (from var `{v}`)"));
        match &self.value {
            Part::Known(s) => format!("`{s}`{from}"),
            Part::Placeholder(s) => format!("the placeholder `{s}`{from}"),
            Part::Target => format!("not set, so the target {what}"),
            Part::Unknown(r) => r.clone(),
        }
    }
}

/// The resolved database, schema, and identifier of a source table or model.
#[derive(Debug, Clone)]
pub struct Location {
    pub database: LocPart,
    pub schema: LocPart,
    pub identifier: LocPart,
}

impl Location {
    fn parts(&self) -> [(&'static str, &LocPart); 3] {
        [("database", &self.database), ("schema", &self.schema), ("identifier", &self.identifier)]
    }

    /// `DB.SCHEMA.IDENT` when all three parts are known.
    pub fn known(&self) -> Option<(String, String, String)> {
        Some((self.database.known()?.to_string(), self.schema.known()?.to_string(), self.identifier.known()?.to_string()))
    }
}

/// How a group of locations compares.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LocationMatch {
    /// Resolved, and the same relation.
    Equal,
    /// Every declaration carries the same generated placeholders: the same
    /// as generated, to be rechecked once real values are set.
    IdenticalPlaceholder,
    /// Resolved, and different relations; the text names the parts.
    Different(String),
    /// Mixed, missing or unresolvable values; the text says why.
    Unresolved(String),
}

/// How to check an unresolved or placeholder location, for finding text.
pub const LOCATION_CHECK: &str = "To check, read the `vars:` in each `dbt_project.yml` and the targets in `profiles.yml`, or run `dbt compile` against the real target and compare the `database`, `schema` and `relation_name` of each node in `target/manifest.json`.";

fn classify(s: &str) -> (Part, bool) {
    let t = s.trim();
    let quoted = rx!(r#"^"(?:[^"]|"")*"$"#).is_match(t);
    let t = if quoted { t[1..t.len() - 1].replace("\"\"", "\"") } else { t.to_string() };
    let part = if t.is_empty() {
        Part::Unknown("empty".into())
    } else if PLACEHOLDER_VALUES.iter().any(|p| p.eq_ignore_ascii_case(&t)) {
        Part::Placeholder(t.to_string())
    } else {
        Part::Known(t.to_string())
    };
    (part, quoted)
}

/// Every `env_var('KEY'[, 'default'])` call with a literal key: (key, default,
/// start, end).
pub fn env_var_reads(text: &str) -> Vec<(String, Option<String>, usize, usize)> {
    rx!(r#"\benv_var\(\s*(?:'([^']+)'|"([^"]+)")\s*(?:,\s*(?:'([^']*)'|"([^"]*)"))?\s*\)"#)
        .captures_iter(text)
        .map(|c| {
            let m = c.get(0).unwrap();
            let key = c.get(1).or(c.get(2)).unwrap().as_str().to_string();
            (key, c.get(3).or(c.get(4)).map(|d| d.as_str().to_string()), m.start(), m.end())
        })
        .collect()
}

/// The value of `var(key, default)` in project `p`: a declared `vars:` value
/// wins over the call's default, as in dbt.
pub fn resolve_var(p: &ProjectContext, key: &str, default: Option<&str>) -> Part {
    resolve_var_part(p, key, default).value
}

pub fn resolve_var_part(p: &ProjectContext, key: &str, default: Option<&str>) -> LocPart {
    let declared = declared_vars(p).into_iter().find(|(k, _, _)| k == key).map(|(_, v, _)| v);
    let raw = match declared {
        Some(Value::Null) => Err(format!("var `{key}` is null under `vars:`")),
        Some(Value::String(s)) if s.trim().is_empty() => Err(format!("var `{key}` is '' under `vars:`")),
        Some(Value::String(s)) => Ok(s),
        Some(other) => Ok(py_str(&other)),
        None => match default {
            Some(d) if !d.trim().is_empty() => Ok(d.to_string()),
            Some(_) => Err(format!("var `{key}` defaults to ''")),
            None => Err(format!("var `{key}` is not declared and has no default")),
        },
    };
    match raw {
        Ok(raw) => {
            let (value, quoted) = classify(&raw);
            LocPart { value, var: Some(key.into()), raw: Some(raw), quoted }
        }
        Err(reason) => LocPart { value: Part::Unknown(reason), var: Some(key.into()), raw: None, quoted: false },
    }
}

/// Resolve one location part as written (`raw`), or `absent` when unset.
/// A whole-value `var()` or `env_var()` resolves through its default; any
/// other Jinja is unknown.
pub fn resolve_part(p: &ProjectContext, raw: Option<&str>, absent: Part, quoting: Option<bool>) -> LocPart {
    let Some(raw) = raw.map(str::trim).filter(|r| !r.is_empty()) else {
        return LocPart { value: absent, var: None, raw: None, quoted: quoting == Some(true) };
    };
    let inner = rx!(r"^\{\{-?\s*(.*?)\s*-?\}\}$").captures(raw).map_or(raw, |c| c.get(1).unwrap().as_str()).trim();
    let whole_call = |name: &str| inner.starts_with(&format!("{name}(")) && match_paren(inner, name.len()) == Some(inner.len() - 1);
    let (value, var, quoted) = if whole_call("var") {
        let r = var_reads(inner).into_iter().next();
        match r {
            Some(r) => {
                let resolved = resolve_var_part(p, &r.key, r.default.as_deref());
                (resolved.value, resolved.var, resolved.quoted)
            }
            None => (Part::Unknown(format!("`{raw}` has a var() with a non-literal name")), None, false),
        }
    } else if whole_call("env_var") {
        match env_var_reads(inner).into_iter().next() {
            Some((_, Some(d), _, _)) if !d.trim().is_empty() => {
                let (value, quoted) = classify(&d);
                (value, None, quoted)
            }
            Some((k, _, _, _)) => (Part::Unknown(format!("env var `{k}` is read at run time and has no default")), None, false),
            None => (Part::Unknown(format!("`{raw}` has an env_var() with a non-literal name")), None, false),
        }
    } else if raw.contains("{{") || raw.contains("{%") || inner.contains('(') {
        (Part::Unknown(format!("`{raw}` is set by a Jinja expression")), None, false)
    } else {
        let (v, q) = classify(raw);
        (v, None, q)
    };
    LocPart { value, var, raw: Some(raw.to_string()), quoted: quoted || quoting == Some(true) }
}

/// Where a source table points. A missing `schema:` is the source name and a
/// missing `identifier:` is the table name, as in dbt; a missing `database:`
/// is the target database.
pub fn resolve_location(p: &ProjectContext, decl: &SourceDecl, table: &SourceTableDecl) -> Location {
    Location {
        database: resolve_part(p, decl.database.as_deref(), Part::Target, decl.quoting[0]),
        schema: resolve_part(p, decl.schema.as_deref(), Part::Known(decl.name.clone()), decl.quoting[1]),
        identifier: resolve_part(p, table.identifier.as_deref(), Part::Known(table.name.clone()), table.quote_identifier.or(decl.quoting[2])),
    }
}

/// Where a whole source block points, for comparing two blocks by database
/// and schema alone: the identifier is `*`, equal for every block.
pub fn resolve_source_location(p: &ProjectContext, decl: &SourceDecl) -> Location {
    Location {
        database: resolve_part(p, decl.database.as_deref(), Part::Target, decl.quoting[0]),
        schema: resolve_part(p, decl.schema.as_deref(), Part::Known(decl.name.clone()), decl.quoting[1]),
        identifier: LocPart { value: Part::Known("*".into()), var: None, raw: None, quoted: false },
    }
}

enum PartMatch {
    Equal,
    Placeholder,
    Different,
    Unresolved,
}

fn compare_part(a: &LocPart, b: &LocPart, same_project: bool) -> PartMatch {
    match (&a.value, &b.value) {
        (Part::Known(_), Part::Known(_)) => {
            if a.key() == b.key() { PartMatch::Equal } else { PartMatch::Different }
        }
        (Part::Placeholder(x), Part::Placeholder(y)) if x.eq_ignore_ascii_case(y) => PartMatch::Placeholder,
        _ if a.var.is_some() && a.var == b.var => PartMatch::Equal,
        (Part::Target, Part::Target) if same_project => PartMatch::Equal,
        _ => PartMatch::Unresolved,
    }
}

/// Compare a group of locations. `same_project` is true when they all belong
/// to one project, so an unset database or schema is the same target.
/// Same literal or same var name counts as equal. A part that differs between
/// resolved values makes the group `Different`, whatever the other parts are.
pub fn compare_locations(locs: &[&Location], same_project: bool) -> LocationMatch {
    let Some(first) = locs.first() else { return LocationMatch::Equal };
    let (mut different, mut unresolved, mut placeholder) = (BTreeSet::new(), vec![], false);
    for other in &locs[1..] {
        for ((what, a), (_, b)) in first.parts().into_iter().zip(other.parts()) {
            match compare_part(a, b, same_project) {
                PartMatch::Equal => {}
                PartMatch::Placeholder => placeholder = true,
                PartMatch::Different => {
                    different.insert(format!("{what} {} vs {}", a.describe(what), b.describe(what)));
                }
                PartMatch::Unresolved => {
                    let r = format!("{what} is {} in one and {} in another", a.describe(what), b.describe(what));
                    if !unresolved.contains(&r) {
                        unresolved.push(r);
                    }
                }
            }
        }
    }
    if !different.is_empty() {
        LocationMatch::Different(different.into_iter().collect::<Vec<_>>().join("; "))
    } else if !unresolved.is_empty() {
        LocationMatch::Unresolved(unresolved.join("; "))
    } else if placeholder {
        LocationMatch::IdenticalPlaceholder
    } else {
        LocationMatch::Equal
    }
}

// ---- Source declarations across the estate ----

/// Every source declaration of every project, by project index.
pub fn estate_source_decls(pf: &PortfolioContext) -> Vec<Vec<SourceDecl>> {
    pf.projects.iter().map(source_decls).collect()
}

/// `path:line` of a source declaration, root-relative.
pub fn decl_site(p: &ProjectContext, decl: &SourceDecl) -> String {
    format!("{}:{}", root_relative(p, &decl.file), decl.line)
}

// ---- Call sites ----

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CallKind {
    Ref,
    Source,
}

/// One `ref()` or `source()` call.
#[derive(Debug, Clone)]
pub struct CallRef {
    pub kind: CallKind,
    /// `ref`: the package of a two-argument ref.
    pub package: Option<String>,
    /// `ref`: the model; `source`: the source name.
    pub name: String,
    /// `source`: the table.
    pub table: Option<String>,
    /// Project-relative file.
    pub file: String,
    /// Root-relative `path:line`.
    pub site: String,
    pub line: u32,
    /// Index into `p.models` when a model makes the call.
    pub model: Option<usize>,
    /// The caller's top-level `m_*` folder.
    pub m_folder: Option<String>,
    /// The caller's tags.
    pub tags: Vec<String>,
}

/// The first folder named `m_*` (any case) on a model's path.
pub fn m_folder(m: &ModelFile) -> Option<String> {
    m.segments.iter().find(|s| s.to_lowercase().starts_with("m_")).cloned()
}

/// A model's tags from folder config and every `config(tags=...)`.
pub fn model_tags(m: &ModelFile) -> Vec<String> {
    let mut out: Vec<String> = vec![];
    let mut add = |s: String| {
        if !s.is_empty() && !out.contains(&s) {
            out.push(s);
        }
    };
    for cfg in [&m.folder_config, &m.own_config] {
        match cfg.get("tags") {
            Some(Value::Array(a)) => a.iter().map(py_str).for_each(&mut add),
            Some(v @ Value::String(_)) => add(py_str(v)),
            _ => {}
        }
    }
    for c in m.jinja.calls_named("config") {
        match c.kwarg("tags") {
            Some(Lit::List(v)) => v.iter().filter_map(|l| l.as_str()).for_each(|s| add(s.to_string())),
            Some(Lit::Str(s)) => add(s.clone()),
            _ => {}
        }
    }
    out
}

fn regex_calls(text: &str, yaml: bool, mut f: impl FnMut(CallKind, Option<String>, String, Option<String>, u32)) {
    let regions = if yaml { vec![] } else { sql_regions(text) };
    let skip = |pos: usize| {
        if yaml {
            let ls = text[..pos].rfind('\n').map_or(0, |i| i + 1);
            text[ls..pos].trim_start().starts_with('#')
        } else {
            region_at(&regions, pos) == Some(crate::sqlutil::Region::JinjaComment)
        }
    };
    for c in crate::sqlutil::ref_pattern().captures_iter(text) {
        let pos = c.get(0).unwrap().start();
        if skip(pos) {
            continue;
        }
        let (pkg, name) = match c.get(2) {
            Some(n) => (Some(c[1].to_string()), n.as_str().to_string()),
            None => (None, c[1].to_string()),
        };
        f(CallKind::Ref, pkg, name, None, line_col(text, pos).0);
    }
    for c in crate::sqlutil::source_pattern().captures_iter(text) {
        let pos = c.get(0).unwrap().start();
        if !skip(pos) {
            f(CallKind::Source, None, c[1].to_string(), Some(c[2].to_string()), line_col(text, pos).0);
        }
    }
}

/// Every `ref()` and `source()` call in project `p`: model SQL through the
/// Jinja parse (regex when it failed), plus YAML, macros, tests and other
/// SQL by regex. Calls in SQL comments count, because dbt renders them; calls
/// in `{# #}` and YAML `#` comments do not.
pub fn call_sites(p: &ProjectContext) -> Vec<CallRef> {
    let mut out = vec![];
    let model_files: BTreeSet<&str> = p.models.iter().map(|m| m.relative_path.as_str()).collect();
    for (mi, m) in p.models.iter().enumerate() {
        let (folder, tags) = (m_folder(m), model_tags(m));
        let mut push = |kind, package, name, table, line: u32| {
            out.push(CallRef {
                kind,
                package,
                name,
                table,
                file: m.relative_path.clone(),
                site: format!("{}:{line}", root_relative(p, &m.relative_path)),
                line,
                model: Some(mi),
                m_folder: folder.clone(),
                tags: tags.clone(),
            })
        };
        if m.is_python || m.jinja.parse_error.is_some() {
            regex_calls(&m.raw, false, &mut push);
            continue;
        }
        for c in m.jinja.calls.iter().filter(|c| c.name == "ref" || c.name == "source") {
            let args: Vec<&str> = c.args.iter().filter_map(|a| a.as_str()).collect();
            if args.len() != c.args.len() || args.is_empty() {
                continue;
            }
            let line = c.span.start_line;
            match (c.name.as_str(), args.as_slice()) {
                ("ref", [n]) => push(CallKind::Ref, None, n.to_string(), None, line),
                ("ref", [pk, n]) => push(CallKind::Ref, Some(pk.to_string()), n.to_string(), None, line),
                ("source", [s, t]) => push(CallKind::Source, None, s.to_string(), Some(t.to_string()), line),
                _ => {}
            }
        }
    }
    for src in project_sources(p).into_iter().filter(|s| !model_files.contains(s.file.as_str())) {
        let file = src.file.clone();
        regex_calls(&src.text, src.yaml, |kind, package, name, table, line| {
            out.push(CallRef {
                kind,
                package,
                name,
                table,
                site: format!("{}:{line}", root_relative(p, &file)),
                file: file.clone(),
                line,
                model: None,
                m_folder: None,
                tags: vec![],
            })
        });
    }
    out
}

// ---- Models and the relations they write ----

/// The relation a model writes, as configured.
#[derive(Debug, Clone)]
pub struct ModelRelation {
    pub location: Location,
    pub physical: Location,
    /// True when `alias` is set, so the relation does not follow the file name.
    pub pinned: bool,
}

/// The configured value of `key` on a model: its own `config()` first (the
/// first call that sets it), then folder config from `dbt_project.yml`.
fn model_config_raw(m: &ModelFile, key: &str) -> Option<String> {
    for c in m.jinja.calls_named("config") {
        if let Some(v) = c.kwarg(key) {
            return Some(match v {
                Lit::Str(s) => s.clone(),
                other => lit_text(other),
            });
        }
    }
    m.folder_config.get(key).filter(|v| !v.is_null()).map(py_str)
}

/// Accept only a complete, unconditional identity macro; never execute project code.
fn identity_naming(p: &ProjectContext, key: &str) -> bool {
    let name = format!("generate_{key}_name");
    let definitions: Vec<_> = p.macros.iter().filter(|file| file.raw.contains(&name)).collect();
    let [file] = definitions.as_slice() else { return false; };
    if file.jinja.parse_error.is_some() { return false; }
    let mut compact: String = file.raw.chars().filter(|c| !c.is_whitespace()).collect();
    let identity = |key: &str| format!("{{%macrogenerate_{key}_name(custom_{key}_name,node)%}}{{{{custom_{key}_name}}}}{{%endmacro%}}");
    if compact.matches(&identity(key)).count() != 1 { return false; }
    for key in ["database", "schema", "alias"] { compact = compact.replace(&identity(key), ""); }
    compact.is_empty()
}

fn physical_part(p: &ProjectContext, m: &ModelFile, key: &str, configured: &LocPart) -> LocPart {
    let naming = format!("generate_{key}_name");
    let overridden = p.macros.iter().any(|file| file.raw.contains(&naming));
    let custom_resolution = !p.packages.is_empty() || p.project_yml.contains_key("dispatch")
        || model_config_raw(m, "catalog_name").is_some();
    let identity = identity_naming(p, key);
    let verified = !custom_resolution && (identity && model_config_raw(m, key).is_some()
        || (key != "schema" && !overridden));
    if verified && configured.known().is_some() {
        configured.clone()
    } else {
        LocPart { value: Part::Unknown(format!("physical {key} requires verified naming semantics; config is not a rendered relation")), var: None, raw: configured.raw.clone(), quoted: configured.quoted }
    }
}

/// Configured identity is used only for possible model/model collisions.
/// Physical identity requires verified naming semantics; the default schema
/// prefix and arbitrary overrides are unresolved without target evidence.
/// `None` for ephemeral models, which write no relation.
pub fn model_relation(p: &ProjectContext, m: &ModelFile) -> Option<ModelRelation> {
    if m.materialization() == "ephemeral" {
        return None;
    }
    let alias = model_config_raw(m, "alias");
    let pinned = alias.as_deref().is_some_and(|a| !a.trim().is_empty());
    let location = Location {
        database: resolve_part(p, model_config_raw(m, "database").as_deref(), Part::Target, None),
        schema: resolve_part(p, model_config_raw(m, "schema").as_deref(), Part::Target, None),
        identifier: resolve_part(p, alias.as_deref(), Part::Known(m.name.clone()), None),
    };
    let physical = Location {
        database: physical_part(p, m, "database", &location.database),
        schema: physical_part(p, m, "schema", &location.schema),
        identifier: physical_part(p, m, "alias", &location.identifier),
    };
    Some(ModelRelation { location, physical, pinned })
}

/// A model: (project index, model index).
pub type Node = (usize, usize);

/// Models by the identifier they write (upper-cased unless quoted), across
/// the estate. Models whose identifier does not resolve are left out.
pub fn producers(pf: &PortfolioContext) -> BTreeMap<String, Vec<Node>> {
    let mut out: BTreeMap<String, Vec<Node>> = BTreeMap::new();
    for (pi, p) in pf.projects.iter().enumerate() {
        for (mi, m) in p.models.iter().enumerate() {
            if let Some(k) = model_relation(p, m).and_then(|r| r.location.identifier.key()) {
                out.entry(k).or_default().push((pi, mi));
            }
        }
    }
    out
}

/// `ref()` edges between models: each model points at the models it reads.
#[derive(Debug, Default)]
pub struct RefGraph {
    pub upstream: BTreeMap<Node, BTreeSet<Node>>,
}

impl RefGraph {
    /// Build the graph. A `ref('x')` resolves to the caller's project first;
    /// with `merged`, a name the project lacks may resolve across projects.
    /// Package-qualified calls honor the package. Ambiguous names supply no
    /// proof edge until the duplicate-model ownership is resolved.
    pub fn build(pf: &PortfolioContext, merged: bool) -> Self {
        let mut by_name: BTreeMap<String, Vec<Node>> = BTreeMap::new();
        for (pi, p) in pf.projects.iter().enumerate() {
            for (mi, m) in p.models.iter().enumerate() {
                by_name.entry(m.name.to_lowercase()).or_default().push((pi, mi));
            }
        }
        let mut g = RefGraph::default();
        for (pi, p) in pf.projects.iter().enumerate() {
            for call in call_sites(p).into_iter().filter(|c| c.kind == CallKind::Ref) {
                let Some(mi) = call.model else { continue };
                let all = by_name.get(&call.name.to_lowercase()).map_or(&[][..], |v| v.as_slice());
                let hits: Vec<Node> = if let Some(package) = call.package {
                    all.iter().copied().filter(|n| pf.projects[n.0].name == package && (merged || n.0 == pi)).collect()
                } else {
                    let local: Vec<Node> = all.iter().copied().filter(|n| n.0 == pi).collect();
                    if !local.is_empty() || !merged { local } else { all.to_vec() }
                };
                if hits.len() == 1 {
                    g.upstream.entry((pi,mi)).or_default().extend(hits);
                }
            }
        }
        g
    }

    /// The `ref()` chain by which `from` depends on `to`, `from` first, or
    /// `None` when it does not.
    pub fn path(&self, from: Node, to: Node) -> Option<Vec<Node>> {
        let mut prev: BTreeMap<Node, Node> = BTreeMap::new();
        let mut queue = VecDeque::from([from]);
        while let Some(n) = queue.pop_front() {
            for &u in self.upstream.get(&n).into_iter().flatten() {
                if u == from || prev.contains_key(&u) {
                    continue;
                }
                prev.insert(u, n);
                if u == to {
                    let mut chain = vec![u];
                    while let Some(&p) = prev.get(chain.last().unwrap()) {
                        chain.push(p);
                    }
                    chain.reverse();
                    return Some(chain);
                }
                queue.push_back(u);
            }
        }
        None
    }
}

/// A model's SQL with comments removed and whitespace collapsed, for an
/// identical-copy test.
pub fn normalized_sql(m: &ModelFile) -> String {
    strip_comments_collapse(&m.raw)
}

// ---- Relation names built from var() ----

/// One dotted part of a relation token.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RelPart {
    Var { key: String, default: Option<String> },
    Ident(String),
}

/// A relation or stage name in a SQL body that is built from `var()`, such as
/// `{{ var('db') }}.{{ var('schema') }}.T`, `{{ var('tgt') }}.T`, or
/// `@{{ var('stage_db') }}.S.STAGE/path`.
#[derive(Debug, Clone)]
pub struct VarRelationRead {
    /// Includes FROM/JOIN/USING for literal findings; otherwise the relation start.
    pub match_start: usize,
    pub start: usize,
    pub end: usize,
    /// 1-based line of `start`.
    pub line: u32,
    pub parts: Vec<RelPart>,
    pub stage: bool,
    pub text: String,
}

impl VarRelationRead {
    pub fn stage_suffix(&self) -> Option<&str> {
        self.stage.then(|| self.text.find('/').map_or("", |start| &self.text[start..]))
    }

    pub fn vars(&self) -> Vec<&str> {
        self.parts.iter().filter_map(|p| if let RelPart::Var { key, .. } = p { Some(key.as_str()) } else { None }).collect()
    }

    /// The last part when it is a literal: the table or stage name.
    pub fn table(&self) -> Option<&str> {
        match self.parts.last() {
            Some(RelPart::Ident(s)) => Some(s.trim_matches('"')),
            _ => None,
        }
    }
}

/// Byte ranges of every `config(...)` call, hooks included.
pub(super) fn config_ranges(text: &str) -> Vec<(usize, usize)> {
    rx!(r"\bconfig\s*\(")
        .find_iter(text)
        .filter_map(|m| match_paren(text, m.end() - 1).map(|c| (m.start(), c + 1)))
        .collect()
}

/// Every relation or stage name built from `var()` in the SQL `text` of one
/// project file. Shared by PRJ0016 and PRJ0021 so they agree on which lines
/// are relation reads. Not reported:
/// - tokens in SQL comments (including tokens glued to `--`), `{# #}`, or
///   string literals;
/// - `config(...)` arguments, so the model's own alias and schema and its
///   `pre_hook`/`post_hook` strings (INC0019) are left alone; tokens in
///   `{% %}` are never matched;
/// - a lone `{{ var() }}` that is not after FROM, JOIN, INTO, UPDATE, TABLE,
///   USING or MERGE, which fills a value, not a relation;
/// - names with no `var()` part, which SQL0006 owns.
pub fn var_relation_reads(text: &str) -> Vec<VarRelationRead> {
    const VAR: &str = r#"\{\{-?\s*var\(\s*(?:'[^']*'|"[^"]*")\s*(?:,\s*(?:'[^']*'|"[^"]*"|[^)'"]*))?\)\s*-?\}\}"#;
    const IDENT: &str = r#""(?:[^"\n]|"")+"|[A-Za-z_][A-Za-z0-9_$]*"#;
    static TOKEN: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| {
        let part = format!("(?:{VAR}|{IDENT})");
        regex::Regex::new(&format!(r#"(@)?{part}(?:\.{part})*(?:/[^\s'"),;]*)?"#)).unwrap()
    });
    static PART: std::sync::LazyLock<regex::Regex> = std::sync::LazyLock::new(|| regex::Regex::new(&format!("{VAR}|{IDENT}")).unwrap());
    let regions = sql_regions(text);
    let configs = config_ranges(text);
    let mut out = vec![];
    for m in TOKEN.find_iter(text) {
        let tok = m.as_str();
        if !tok.contains("{{") {
            continue;
        }
        let (start, end) = (m.start(), m.end());
        if region_at(&regions, start).is_some() || configs.iter().any(|&(a, b)| a <= start && start < b) {
            continue;
        }
        let stage = tok.starts_with('@');
        let body = tok.trim_start_matches('@');
        let body = body.find('/').map_or(body, |i| &body[..i]);
        let mut parts = vec![];
        for pm in PART.find_iter(body) {
            let s = pm.as_str();
            if s.starts_with("{{") {
                if let Some(r) = var_reads(s).into_iter().next() {
                    parts.push(RelPart::Var { key: r.key, default: r.default });
                }
            } else {
                parts.push(RelPart::Ident(s.to_string()));
            }
        }
        if !parts.iter().any(|p| matches!(p, RelPart::Var { .. })) {
            continue;
        }
        if parts.len() == 1 && !stage {
            let before = text[..start].trim_end();
            let word = before.rsplit(|c: char| !c.is_ascii_alphanumeric() && c != '_').next().unwrap_or("");
            let relation_kw = ["from", "join", "into", "update", "table", "using", "merge"].iter().any(|k| word.eq_ignore_ascii_case(k));
            if !relation_kw {
                continue;
            }
        }
        out.push(VarRelationRead { match_start: start, start, end, line: line_col(text, start).0, parts, stage, text: tok.to_string() });
    }
    out
}

// ---- Source blocks and the location policy ----

fn ident_name(s: &str) -> String {
    s.trim_matches('"').to_lowercase().chars().map(|c| if c.is_ascii_alphanumeric() || c == '_' { c } else { '_' }).collect()
}

/// The source block name for `db.schema` under the location policy: one block
/// per database.schema, named after the schema in lower case, or
/// `<db>_<schema>` when another database in `locations` (the project's
/// [`project_locations`]) has a schema of the same name.
pub fn source_block_for(db: &str, schema: &str, locations: &BTreeSet<(String, String)>) -> String {
    let clash = locations.iter().any(|(d, s)| s.eq_ignore_ascii_case(schema) && !d.eq_ignore_ascii_case(db));
    if clash { format!("{}_{}", ident_name(db), ident_name(schema)) } else { ident_name(schema) }
}

/// Every resolved external `(DATABASE, SCHEMA)` a project reads, upper-cased:
/// source declarations, `var()`-built relation reads, and literal
/// `db.schema.table` names after FROM or JOIN. PRJ0019, PRJ0021 and SQL0006
/// pass this to [`source_block_for`], so they name the same block.
pub fn project_locations(p: &ProjectContext) -> BTreeSet<(String, String)> {
    let mut out = BTreeSet::new();
    let mut add = |d: &str, s: &str| {
        out.insert((d.trim_matches('"').to_uppercase(), s.trim_matches('"').to_uppercase()));
    };
    for decl in source_decls(p) {
        let db = resolve_part(p, decl.database.as_deref(), Part::Target, None);
        let sc = resolve_part(p, decl.schema.as_deref(), Part::Known(decl.name.clone()), None);
        if let (Some(d), Some(s)) = (db.known(), sc.known()) {
            add(d, s);
        }
    }
    for m in p.models.iter().filter(|m| !m.is_python) {
        // Every part before the table or stage name: `db.schema`, or one var
        // that holds `db.schema`.
        for r in var_relation_reads(&m.raw) {
            let n = r.parts.len().saturating_sub(1);
            let vals: Option<Vec<String>> = r.parts[..n]
                .iter()
                .map(|x| match x {
                    RelPart::Ident(s) => Some(s.clone()),
                    RelPart::Var { key, default } => match resolve_var(p, key, default.as_deref()) {
                        Part::Known(v) => Some(v),
                        _ => None,
                    },
                })
                .collect();
            let Some(vals) = vals.filter(|v| !v.is_empty()) else { continue };
            if let [d, s] = vals.join(".").split('.').collect::<Vec<_>>()[..] {
                add(d, s);
            }
        }
        for c in rx!(r"(?i)\b(?:from|join)\s+([A-Za-z_][A-Za-z0-9_$]*)\.([A-Za-z_][A-Za-z0-9_$]*)\.[A-Za-z_][A-Za-z0-9_$]*\b").captures_iter(&m.stripped) {
            add(&c[1], &c[2]);
        }
    }
    out
}

/// Read targets from `p`'s profile in `profiles.yml` beside `dbt_project.yml`.
/// Return them in file order with a flag that identifies them as profile targets.
/// Otherwise, return example targets `dev`, `qa`, and `prod`.
pub fn target_names(p: &ProjectContext) -> (Vec<String>, bool) {
    let path = p.root.join("profiles.yml");
    let text = crate::discovery::read_source(&path, true).unwrap_or_default();
    let found = crate::discovery::load_yaml_str(&text).ok().and_then(|v| {
        let profiles = v.as_object()?.clone();
        let want = p.project_yml.get("profile").map(py_str);
        let prof = want.as_ref().and_then(|w| profiles.get(w)).or_else(|| {
            let cands: Vec<&Value> = profiles.iter().filter(|(k, _)| *k != "config").map(|(_, v)| v).collect();
            cands.first().copied().filter(|_| cands.len() == 1)
        })?;
        let outs = prof.get("outputs")?.as_object()?;
        Some(outs.keys().cloned().collect::<Vec<_>>()).filter(|v| !v.is_empty())
    });
    match found {
        Some(t) => (t, true),
        None => (vec!["dev".into(), "qa".into(), "prod".into()], false),
    }
}

/// `(target, database)` pairs for [`render_source_location`]: the known
/// database for a single target, else a `<database for T>` placeholder per
/// target for the agent to fill in from the owner. Never a guess.
pub fn target_values(p: &ProjectContext, known_db: Option<&str>) -> (Vec<(String, String)>, bool) {
    let (targets, from_profile) = target_names(p);
    let vals = match (targets.as_slice(), known_db) {
        ([t], Some(db)) => vec![(t.clone(), db.to_string())],
        _ => targets.iter().map(|t| (t.clone(), format!("<database for {t}>"))).collect(),
    };
    (vals, from_profile)
}

/// The YAML for source block `block` under the location policy: a literal
/// `database:` for a single environment, else a `target.name` if/elif block
/// whose `else` is `invalid_database` to expose an unknown target.
/// `schema:` is a literal. Never emits `var()`.
pub fn yaml_scalar(value: &str) -> String {
    if rx!(r"^[A-Za-z_][A-Za-z0-9_]*$").is_match(value)
        && !["null", "true", "false", "yes", "no", "on", "off"].contains(&value.to_ascii_lowercase().as_str()) {
        value.to_string()
    } else {
        serde_json::to_string(value).unwrap()
    }
}

pub fn template_literal(value: &str) -> String {
    if value.contains(['\n', '\r']) || value.contains("{{") || value.contains("{%"){ 
        format!("{{{{ {} }}}}", serde_json::to_string(value).unwrap())
    } else {
        value.to_string()
    }
}

pub fn sql_identifier(value: &str, quoted: bool) -> String {
    if quoted { format!("\"{}\"", value.replace('"', "\"\"")) } else { value.to_string() }
}

pub fn logical_identifier(value: &str) -> String {
    if rx!(r"^[A-Za-z_][A-Za-z0-9_]*$").is_match(value) { return value.to_string(); }
    let encoded = value.as_bytes().iter().map(|byte| format!("{byte:02x}")).collect::<String>();
    format!("relation_{encoded}")
}

pub fn render_source_location(block: &str, schema: &str, targets: &[(String, String)], quoting: [bool; 3]) -> String {
    let mut y = format!("sources:\n  - name: {}\n", yaml_scalar(block));
    match targets {
        [(_, db)] => y.push_str(&format!("    database: {}\n", yaml_scalar(&template_literal(db)))),
        _ => {
            y.push_str("    database: |\n");
            for (i, (t, db)) in targets.iter().enumerate() {
                let kw = if i == 0 { "if" } else { "elif" };
                y.push_str(&format!("      {{%- {kw} target.name == {} -%}} {}\n", serde_json::to_string(t).unwrap(), template_literal(db)));
            }
            y.push_str("      {%- else -%} invalid_database\n      {%- endif -%}\n");
        }
    }
    y.push_str(&format!("    schema: {}\n    quoting:\n      database: {}\n      schema: {}\n      identifier: {}\n", yaml_scalar(&template_literal(schema)), quoting[0], quoting[1], quoting[2]));
    y
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::discovery::build_portfolio;
    use crate::testing::TempProject;

    const HEAD: &str = "name: demo\nversion: '1.0'\nprofile: demo\n";

    fn pf(t: &TempProject) -> PortfolioContext {
        build_portfolio(t.path())
    }

    #[test]
    fn source_decls_have_lines() {
        let y = "version: 2\n\nsources:\n  - name: raw\n    database: \"{{ var('db', 'RAW_DB') }}\"\n    tables:\n      - name: orders\n      - name: users\n        identifier: USR\n\n  - name: erp # second\n    schema: ERP\n    tables:\n      - name: raw\n";
        let t = TempProject::new(&[("models/s.yml", y), ("models/a.sql", "select 1")]);
        let pf = pf(&t);
        let d = source_decls(&pf.projects[0]);
        assert_eq!(d.len(), 2);
        assert_eq!((d[0].name.as_str(), d[0].line, d[0].file.as_str()), ("raw", 4, "models/s.yml"));
        assert_eq!(d[0].database.as_deref(), Some("{{ var('db', 'RAW_DB') }}"));
        assert_eq!(d[0].tables.iter().map(|t| t.line).collect::<Vec<_>>(), vec![7, 8]);
        assert_eq!(d[0].tables[1].identifier.as_deref(), Some("USR"));
        // A table named like a source does not take the source's line.
        assert_eq!((d[1].name.as_str(), d[1].line, d[1].tables[0].line), ("erp", 11, 14));
    }

    #[test]
    fn resolves_vars_env_vars_and_defaults() {
        let y = format!("{HEAD}vars:\n  set: PROD_DB\n  empty: ''\n");
        let t = TempProject::new(&[("dbt_project.yml", &y), ("models/a.sql", "select 1")]);
        let pf = pf(&t);
        let p = &pf.projects[0];
        let r = |raw: &str| resolve_part(p, Some(raw), Part::Target, None).value;
        assert_eq!(r("{{ var('set', 'X') }}"), Part::Known("PROD_DB".into()));
        assert_eq!(r("{{ var('d', 'RAW') }}"), Part::Known("RAW".into()));
        assert_eq!(r("var('d', 'YOUR_DB')"), Part::Placeholder("YOUR_DB".into()));
        assert!(matches!(r("{{ var('empty', 'X') }}"), Part::Unknown(s) if s.contains("''")));
        assert!(matches!(r("{{ var('nope') }}"), Part::Unknown(s) if s.contains("no default")));
        assert_eq!(r("{{ env_var('DBT_DB', 'ENV_DB') }}"), Part::Known("ENV_DB".into()));
        assert!(matches!(r("{{ env_var('DBT_DB') }}"), Part::Unknown(s) if s.contains("run time")));
        assert!(matches!(r("{{ var('a') ~ '_x' }}"), Part::Unknown(s) if s.contains("expression")));
        assert_eq!(r("\"MiXed\""), Part::Known("MiXed".into()));
        assert!(resolve_part(p, Some("\"MiXed\""), Part::Target, None).quoted);
        assert_eq!(resolve_part(p, None, Part::Target, None).value, Part::Target);
    }

    fn loc(db: Part, schema: Part, ident: Part) -> Location {
        let lp = |value| LocPart { value, var: None, raw: None, quoted: false };
        Location { database: lp(db), schema: lp(schema), identifier: lp(ident) }
    }

    #[test]
    fn compares_locations() {
        let k = |s: &str| Part::Known(s.into());
        let ph = |s: &str| Part::Placeholder(s.into());
        let a = loc(k("RAW"), k("SALES"), k("orders"));
        assert_eq!(compare_locations(&[&a, &loc(k("raw"), k("sales"), k("ORDERS"))], false), LocationMatch::Equal);
        assert!(matches!(compare_locations(&[&a, &loc(k("RAW"), k("ERP"), k("ORDERS"))], false), LocationMatch::Different(s) if s.contains("schema")));
        let p1 = loc(ph("YOUR_DB"), ph("YOUR_SCHEMA"), k("T"));
        assert_eq!(compare_locations(&[&p1, &p1.clone()], false), LocationMatch::IdenticalPlaceholder);
        // Mixed placeholder and real value.
        assert!(matches!(compare_locations(&[&p1, &loc(k("RAW"), ph("YOUR_SCHEMA"), k("T"))], false), LocationMatch::Unresolved(_)));
        // An unset database is the same target only within one project.
        let t1 = loc(Part::Target, k("raw"), k("T"));
        assert_eq!(compare_locations(&[&t1, &t1.clone()], true), LocationMatch::Equal);
        assert!(matches!(compare_locations(&[&t1, &t1.clone()], false), LocationMatch::Unresolved(s) if s.contains("target database")));
        // A differing identifier decides even when the database is unresolved.
        assert!(matches!(compare_locations(&[&t1, &loc(Part::Target, k("raw"), k("U"))], false), LocationMatch::Different(_)));
        // Same var name counts as equal even when its value is unknown.
        let mut v1 = loc(Part::Unknown("var `db` defaults to ''".into()), k("S"), k("T"));
        v1.database.var = Some("db".into());
        assert_eq!(compare_locations(&[&v1, &v1.clone()], false), LocationMatch::Equal);
        // Quoted identifiers compare case-sensitively.
        let mut q = loc(k("RAW"), k("SALES"), k("Orders"));
        q.identifier.quoted = true;
        assert!(matches!(compare_locations(&[&a, &q], false), LocationMatch::Different(_)));
    }

    #[test]
    fn source_location_defaults() {
        let y = "sources:\n  - name: raw\n    tables:\n      - name: orders\n  - name: erp\n    database: YOUR_DB\n    schema: YOUR_SCHEMA\n    tables:\n      - name: x\n        identifier: X_T\n";
        let t = TempProject::new(&[("models/s.yml", y), ("models/a.sql", "select 1")]);
        let pf = pf(&t);
        let p = &pf.projects[0];
        let d = source_decls(p);
        let l = resolve_location(p, &d[0], &d[0].tables[0]);
        assert_eq!((l.database.value.clone(), l.schema.known(), l.identifier.known()), (Part::Target, Some("raw"), Some("orders")));
        let l = resolve_location(p, &d[1], &d[1].tables[0]);
        assert_eq!((l.database.value, l.identifier.known()), (Part::Placeholder("YOUR_DB".into()), Some("X_T")));
    }

    #[test]
    fn call_sites_with_positions() {
        let a = "{{ config(tags=['m_A']) }}\nselect *\nfrom {{ ref('b') }}\njoin {{ source('raw', 'orders') }} o\n{# {{ ref('gone') }} #}\n";
        let y = format!("{HEAD}models:\n  demo:\n    m_A:\n      +tags: ['folder_tag']\n");
        let t = TempProject::new(&[
            ("dbt_project.yml", &y),
            ("models/m_A/staging/a.sql", a),
            ("models/b.sql", "select 1"),
            ("models/s.yml", "models:\n  - name: b\n    data_tests:\n      - relationships:\n          to: ref('a')\n# to: ref('commented')\n"),
            ("macros/x.sql", "{% macro x() %}{{ ref('b', v=2) }}{{ ref('b') }}{% endmacro %}"),
        ]);
        let pf = pf(&t);
        let c = call_sites(&pf.projects[0]);
        let refs: Vec<(String, u32)> = c.iter().filter(|c| c.kind == CallKind::Ref).map(|c| (c.name.clone(), c.line)).collect();
        assert!(refs.contains(&("b".into(), 3)), "{refs:?}");
        assert!(refs.contains(&("a".into(), 5)), "{refs:?}");
        assert!(!refs.iter().any(|r| r.0 == "gone" || r.0 == "commented"), "{refs:?}");
        let src = c.iter().find(|c| c.kind == CallKind::Source).unwrap();
        assert_eq!((src.name.as_str(), src.table.as_deref(), src.site.as_str()), ("raw", Some("orders"), "models/m_A/staging/a.sql:4"));
        assert_eq!(src.m_folder.as_deref(), Some("m_A"));
        assert!(src.tags.contains(&"m_A".to_string()) && src.tags.contains(&"folder_tag".to_string()), "{:?}", src.tags);
        assert!(c.iter().any(|c| c.file == "macros/x.sql" && c.model.is_none()));
    }

    #[test]
    fn normalized_sql_ignores_comments_only() {
        let t = TempProject::new(&[
            ("models/a.sql", "-- one\nselect a,  b\n/* x */ from t where s = 'a--b'\n"),
            ("models/b.sql", "select a, b from t {# c #} where s = 'a--b'"),
            ("models/c.sql", "select a, b from t where s = 'a--c'"),
        ]);
        let pf = pf(&t);
        let n: Vec<String> = pf.projects[0].models.iter().map(normalized_sql).collect();
        let by = |name: &str| n[pf.projects[0].models.iter().position(|m| m.name == name).unwrap()].clone();
        assert_eq!(by("a"), by("b"));
        assert_ne!(by("a"), by("c"));
    }

    #[test]
    fn model_relations_and_pinning() {
        let y = format!("{HEAD}vars:\n  t: ORDERS_T\nmodels:\n  demo:\n    marts:\n      +schema: MART\n");
        let t = TempProject::new(&[
            ("dbt_project.yml", &y),
            ("models/marts/a.sql", "{{ config(alias=var('t'), database=var('db', 'YOUR_DB')) }}\nselect 1"),
            ("models/b.sql", "select 1"),
            ("models/e.sql", "{{ config(materialized='ephemeral') }}\nselect 1"),
        ]);
        let pf = pf(&t);
        let p = &pf.projects[0];
        let m = |n: &str| p.models.iter().find(|m| m.name == n).unwrap();
        let a = model_relation(p, m("a")).unwrap();
        assert!(a.pinned);
        assert_eq!(a.location.identifier.known(), Some("ORDERS_T"));
        assert_eq!(a.location.identifier.var.as_deref(), Some("t"));
        assert_eq!(a.location.database.value, Part::Placeholder("YOUR_DB".into()));
        assert_eq!(a.location.schema.known(), Some("MART"));
        let b = model_relation(p, m("b")).unwrap();
        assert!(!b.pinned);
        assert_eq!((b.location.identifier.known(), b.location.schema.value.clone()), (Some("b"), Part::Target));
        assert!(model_relation(p, m("e")).is_none());
        let pr = producers(&pf);
        assert_eq!(pr.get("ORDERS_T").map(Vec::len), Some(1));
        assert_eq!(pr.get("B").map(Vec::len), Some(1));
    }

    #[test]
    fn ref_graph_per_project_and_merged() {
        let t = TempProject::new(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
            ("a/models/stg.sql", "select 1"),
            ("a/models/int.sql", "select * from {{ ref('stg') }}"),
            ("a/models/mart.sql", "select * from {{ ref('int') }}"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
            ("b/models/use.sql", "select * from {{ ref('mart') }}"),
        ]);
        let pf = pf(&t);
        let node = |p: &str, m: &str| {
            let pi = pf.projects.iter().position(|x| x.name == p).unwrap();
            (pi, pf.projects[pi].models.iter().position(|x| x.name == m).unwrap())
        };
        let g = RefGraph::build(&pf, false);
        assert_eq!(g.path(node("a", "mart"), node("a", "stg")), Some(vec![node("a", "mart"), node("a", "int"), node("a", "stg")]));
        assert_eq!(g.path(node("a", "stg"), node("a", "mart")), None);
        assert_eq!(g.path(node("b", "use"), node("a", "mart")), None);
        let merged = RefGraph::build(&pf, true);
        assert_eq!(merged.path(node("b", "use"), node("a", "stg")).map(|c| c.len()), Some(4));
    }

    #[test]
    fn var_relation_reads_finds_relations_only() {
        let sql = "{{ config(alias=var('t'), post_hook=\"insert into {{ var('h') }}.LOG select 1\") }}\n\
select a.x, '{{ var('v') }}' as lit, {{ var('n') }} as n\n\
from {{ var('db') }}.{{ var('schema') }}.ORDERS a\n\
join {{ var('m_X_SLSORDVWDB') }}.\"Mixed\" b on 1 = 1\n\
join {{ var('tgt') }} c on 1 = 1\n\
join RAW.SALES.LIT d on 1 = 1\n\
--NBCM.KEYFROM{{ var('m_X_SLSORDVWDB') }}.GLUED\n\
/* {{ var('db') }}.IN_BLOCK */\n\
copy into x from @{{ var('stage_db') }}.LAND.STG/path/file.csv\n\
{% set q = var('db') ~ '.T' %}\n";
        let r = var_relation_reads(sql);
        let got: Vec<(u32, Vec<&str>, Option<&str>, bool)> = r.iter().map(|x| (x.line, x.vars(), x.table(), x.stage)).collect();
        assert_eq!(
            got,
            vec![
                (3, vec!["db", "schema"], Some("ORDERS"), false),
                (4, vec!["m_X_SLSORDVWDB"], Some("Mixed"), false),
                (5, vec!["tgt"], None, false),
                (9, vec!["stage_db"], Some("STG"), true),
            ],
            "{r:#?}"
        );
    }

    #[test]
    fn source_blocks_and_rendering() {
        let mut locs = BTreeSet::new();
        locs.insert(("RAW".to_string(), "SALES".to_string()));
        assert_eq!(source_block_for("RAW", "SALES", &locs), "sales");
        locs.insert(("ARCHIVE".to_string(), "SALES".to_string()));
        assert_eq!(source_block_for("RAW", "Sales", &locs), "raw_sales");
        assert_eq!(source_block_for("OTHER", "ERP", &locs), "erp");

        let y = render_source_location("sales", "SALES", &[("dev".into(), "raw_dev".into()), ("qa".into(), "raw_qa".into()), ("prod".into(), "raw_prod".into())], [false; 3]);
        assert_eq!(
            y,
            "sources:\n  - name: sales\n    database: |\n      {%- if target.name == \"dev\" -%} raw_dev\n      {%- elif target.name == \"qa\" -%} raw_qa\n      {%- elif target.name == \"prod\" -%} raw_prod\n      {%- else -%} invalid_database\n      {%- endif -%}\n    schema: SALES\n    quoting:\n      database: false\n      schema: false\n      identifier: false\n"
        );
        assert!(crate::discovery::load_yaml_str(&y).is_ok());
        let lit = render_source_location("sales", "SALES", &[("prod".into(), "RAW".into())], [false; 3]);
        assert!(lit.contains("    database: RAW\n") && !lit.contains("target.name"));
        for s in [&y, &lit] {
            assert!(!s.contains("var(") && !s.contains("--target"));
        }
    }

    #[test]
    fn targets_from_profile_or_examples() {
        let prof = "demo:\n  target: dev\n  outputs:\n    dev:\n      type: snowflake\n    prod:\n      type: snowflake\n";
        let t = TempProject::new(&[("models/a.sql", "select 1"), ("profiles.yml", prof)]);
        let with = pf(&t);
        assert_eq!(target_names(&with.projects[0]), (vec!["dev".to_string(), "prod".to_string()], true));
        let (v, _) = target_values(&with.projects[0], Some("RAW"));
        assert_eq!(v[1], ("prod".to_string(), "<database for prod>".to_string()));
        let t = TempProject::new(&[("models/a.sql", "select 1")]);
        let without = pf(&t);
        assert!(!target_names(&without.projects[0]).1);
        assert_eq!(target_names(&without.projects[0]).0.len(), 3);
    }

    fn fixture(rel: &str) -> PortfolioContext {
        build_portfolio(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures").join(rel))
    }

    /// One `raw` block per project, compared as PRJ0019 will.
    fn raw_blocks(pf: &PortfolioContext) -> (Vec<String>, LocationMatch) {
        let decls = estate_source_decls(pf);
        let mut sites = vec![];
        let mut locs = vec![];
        for (pi, ds) in decls.iter().enumerate() {
            for d in ds.iter().filter(|d| d.name == "raw") {
                sites.push(decl_site(&pf.projects[pi], d));
                locs.push(resolve_source_location(&pf.projects[pi], d));
            }
        }
        let refs: Vec<&Location> = locs.iter().collect();
        (sites, compare_locations(&refs, false))
    }

    #[test]
    fn fixture_sources_resolve_as_planned() {
        // cisco: 4 identical placeholder blocks at line 3, so consolidate with the caveat.
        let (sites, m) = raw_blocks(&fixture("cisco_estate"));
        assert_eq!(sites.len(), 4);
        assert!(sites.iter().all(|s| s.ends_with("/models/sources.yml:3")), "{sites:?}");
        assert_eq!(m, LocationMatch::IdenticalPlaceholder);
        // Informatica: 20 blocks, also YOUR_DB/YOUR_SCHEMA.
        let (sites, m) = raw_blocks(&fixture("snowconvert/Informatica"));
        assert_eq!(sites.len(), 20);
        assert_eq!(m, LocationMatch::IdenticalPlaceholder);
        // ewi: no database across 4 projects, so the target decides: unresolved.
        let (sites, m) = raw_blocks(&fixture("ewi_estate"));
        assert_eq!(sites.len(), 4);
        assert!(matches!(m, LocationMatch::Unresolved(ref r) if r.contains("target database")), "{m:?}");
    }

    #[test]
    fn fixture_cisco_relations_and_reads() {
        let pf = fixture("cisco_estate");
        let find = |name: &str| {
            pf.projects.iter().enumerate().find_map(|(pi, p)| p.models.iter().position(|m| m.name == name).map(|mi| (pi, mi))).unwrap()
        };
        // Only the name duplicates write one relation twice; the alias vars
        // of the other sc_override_* groups resolve to distinct tables.
        let multi: Vec<String> = producers(&pf).into_iter().filter(|(_, v)| v.len() > 1).map(|(k, _)| k).collect();
        assert_eq!(multi, vec!["MT_RSTD_BKGS_BY_QUARTER", "STG_RAW__SQ_MT_RSTD_BKGS_MEASURE", "STG_RAW__SQ_WI2_RSTD_BKGS_ORDER_MTH"]);
        // The self-read: the staging model reads the table its mart writes,
        // and the mart refs the staging model.
        let (prod, stg) = (find("WI_BKGS_MSR_ANNUITY_PRDT_AMORZ_12"), find("stg_raw__SQ_12_WI_BKGS_MSR_ANNUITY_PRDT_AMORZ"));
        let p = &pf.projects[stg.0];
        let reads = var_relation_reads(&p.models[stg.1].raw);
        assert!(reads.iter().any(|r| r.line == 29 && r.table() == Some("WI_BKGS_MSR_ANNUITY_PRDT_AMORZ")), "{reads:?}");
        let rel = model_relation(p, &p.models[prod.1]).unwrap();
        assert_eq!((rel.location.identifier.key().as_deref(), rel.pinned), (Some("WI_BKGS_MSR_ANNUITY_PRDT_AMORZ"), true));
        assert_eq!(RefGraph::build(&pf, false).path(prod, stg), Some(vec![prod, stg]));
        // Reads glued to `--` in a comment are skipped.
        let (gp, gm) = find("stg_raw__SQ_WI_PRODUCT_HWSW_ANNUITY_TMP1");
        assert!(var_relation_reads(&pf.projects[gp].models[gm].raw).is_empty());
        // The cross-project read of MT_RSTD_BKGS_MSR_ANNUITY in audit_cost.
        let (ap, am) = find("stg_raw__SQ_3_AUDIT_SERVICE_ANNUALISED_ANNUITY");
        assert!(var_relation_reads(&pf.projects[ap].models[am].raw).iter().any(|r| r.line == 63 && r.table() == Some("MT_RSTD_BKGS_MSR_ANNUITY")));
    }

    #[test]
    fn project_locations_feed_block_names() {
        let y = format!("{HEAD}vars:\n  db: ARCHIVE\n");
        let t = TempProject::new(&[
            ("dbt_project.yml", &y),
            ("models/s.yml", "sources:\n  - name: sales\n    database: RAW\n    tables:\n      - name: o\n"),
            ("models/a.sql", "select * from {{ var('db') }}.SALES.T join OTHER.ERP.X on 1=1"),
        ]);
        let pf = pf(&t);
        let l = project_locations(&pf.projects[0]);
        assert!(l.contains(&("RAW".into(), "SALES".into())) && l.contains(&("ARCHIVE".into(), "SALES".into())) && l.contains(&("OTHER".into(), "ERP".into())), "{l:?}");
        assert_eq!(source_block_for("RAW", "SALES", &l), "raw_sales");
    }
}
