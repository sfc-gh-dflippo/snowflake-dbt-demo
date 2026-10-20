//! Project discovery and context construction.
//!
//! Find `dbt_project.yml` files under a root and build the rule contexts.
//! Model `config()` values override folder config from `dbt_project.yml`.
//! Skip dependency and generated directories, including `dbt_packages/` and `target/`.

use std::cell::RefCell;
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

use indexmap::IndexMap;
use serde_json::{Map, Value};

use crate::graph::Graph;
use crate::jinja::{summarize, JinjaSummary};
use crate::provenance::ProvenanceVerdict;
use crate::sqlutil::{
    extract_config, extract_macro_calls, extract_macro_defs, extract_refs, extract_sources, find_line_number,
    strip_all, Config, MacroCall, MacroDef,
};
use crate::waivers::{blank_directives, FileWaivers};

pub const EXCLUDED_DIRS: &[&str] = &[
    "dbt_packages", "target", "logs", "node_modules", ".git", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".ruff_cache", "dbt_modules", "site-packages", ".tox", "build", "dist",
];

pub fn layer_alias(segment: &str) -> Option<&'static str> {
    Some(match segment {
        "bronze" | "staging" | "stg" | "raw" => "bronze",
        "silver" | "intermediate" | "int" => "silver",
        "gold" | "marts" | "mart" | "presentation" => "gold",
        _ => return None,
    })
}

pub const CONFIG_SEARCH_LIMIT: usize = 8;
pub const CONFIG_NAMES: &[&str] = &[".dbt-quality.yml", ".dbt-quality.yaml"];

#[derive(Debug, Clone, Default)]
pub struct IgnoreRule {
    pub paths: Vec<String>,
    pub rules: Vec<String>,
}

impl IgnoreRule {
    pub fn rule_set(&self) -> std::collections::BTreeSet<String> {
        self.rules.iter().map(|r| r.trim().to_uppercase()).filter(|r| !r.is_empty()).collect()
    }
}

#[derive(Debug, Clone)]
pub struct AuditConfig {
    pub micro_project_threshold: i64,
    pub ephemeral_fanout_threshold: i64,
    pub passthrough_chain_threshold: i64,
    pub column_doc_coverage: f64,
    pub macro_model_ratio: f64,
    pub duplicate_block_threshold: i64,
    pub duplicate_block_min_lines: i64,
    pub max_cluster_columns: i64,
    pub migration_mode: String,
    pub migration_paths: Vec<String>,
    pub disabled_rules: Vec<String>,
    pub ignores: Vec<IgnoreRule>,
    /// scai DDL roots or files. Absolute after load.
    pub ddl_paths: Vec<PathBuf>,
    /// `type_compare: strict` compares normalized type text exactly.
    pub type_compare_strict: bool,
    /// Values for `<%TOKEN%>` and `${TOKEN}` in DDL database names.
    pub ddl_bindings: std::collections::BTreeMap<String, String>,
    /// Parsed DDL for `ddl_paths`. Empty when no paths are set.
    pub ddl: std::sync::Arc<crate::ddl::DdlIndex>,
}

impl Default for AuditConfig {
    fn default() -> Self {
        AuditConfig {
            micro_project_threshold: 5,
            ephemeral_fanout_threshold: 3,
            passthrough_chain_threshold: 3,
            column_doc_coverage: 0.8,
            macro_model_ratio: 0.5,
            duplicate_block_threshold: 3,
            duplicate_block_min_lines: 4,
            max_cluster_columns: 4,
            migration_mode: "auto".into(),
            migration_paths: vec![],
            disabled_rules: vec![],
            ignores: vec![],
            ddl_paths: vec![],
            type_compare_strict: false,
            ddl_bindings: Default::default(),
            ddl: Default::default(),
        }
    }
}

fn str_list(v: Option<&Value>) -> Vec<String> {
    match v {
        Some(Value::String(s)) => vec![s.clone()],
        Some(Value::Array(a)) => a.iter().map(crate::sqlutil::py_str).collect(),
        _ => vec![],
    }
}

impl AuditConfig {
    /// Load the nearest `.dbt-quality.yml` at or above `root`, else defaults.
    pub fn load(root: &Path) -> Self {
        let mut config = AuditConfig::default();
        let Some(path) = find_config(root) else { return config };
        let Ok(text) = read_source(&path, false) else { return config };
        let Ok(Value::Object(data)) = load_yaml_str(&text) else { return config };

        if let Some(Value::Object(t)) = data.get("thresholds") {
            for (k, v) in t {
                let i = v.as_i64();
                let f = v.as_f64();
                match k.as_str() {
                    "micro_project_threshold" => config.micro_project_threshold = i.unwrap_or(config.micro_project_threshold),
                    "ephemeral_fanout_threshold" => config.ephemeral_fanout_threshold = i.unwrap_or(config.ephemeral_fanout_threshold),
                    "passthrough_chain_threshold" => config.passthrough_chain_threshold = i.unwrap_or(config.passthrough_chain_threshold),
                    "column_doc_coverage" => config.column_doc_coverage = f.unwrap_or(config.column_doc_coverage),
                    "macro_model_ratio" => config.macro_model_ratio = f.unwrap_or(config.macro_model_ratio),
                    "duplicate_block_threshold" => config.duplicate_block_threshold = i.unwrap_or(config.duplicate_block_threshold),
                    "duplicate_block_min_lines" => config.duplicate_block_min_lines = i.unwrap_or(config.duplicate_block_min_lines),
                    "max_cluster_columns" => config.max_cluster_columns = i.unwrap_or(config.max_cluster_columns),
                    _ => {}
                }
            }
        }
        if let Some(Value::Object(m)) = data.get("migration") {
            if let Some(Value::String(mode)) = m.get("mode") {
                config.migration_mode = mode.clone();
            }
            config.migration_paths = str_list(m.get("paths"));
        }
        config.disabled_rules = str_list(data.get("disabled_rules"));
        let base = path.parent().unwrap_or(Path::new("."));
        config.ddl_paths = str_list(data.get("ddl_paths")).iter().map(|p| base.join(p)).collect();
        config.type_compare_strict = matches!(data.get("type_compare"), Some(Value::String(s)) if s == "strict");
        if let Some(Value::Object(b)) = data.get("ddl_bindings") {
            config.ddl_bindings = b.iter().map(|(k, v)| (k.clone(), crate::sqlutil::py_str(v))).collect();
        }
        config.ddl = std::sync::Arc::new(crate::ddl::DdlIndex::load(&config.ddl_paths));
        if let Some(Value::Array(items)) = data.get("ignore") {
            for item in items {
                let Value::Object(o) = item else { continue };
                let pick = |a: &str, b: &str| o.get(a).filter(|v| crate::sqlutil::truthy(Some(v))).or(o.get(b)).cloned();
                let paths = pick("paths", "path");
                let rules = pick("rules", "rule");
                let ok = |v: &Option<Value>| matches!(v, None | Some(Value::String(_)) | Some(Value::Array(_)) | Some(Value::Null));
                if !ok(&paths) || !ok(&rules) {
                    continue;
                }
                let e = IgnoreRule {
                    paths: str_list(paths.as_ref()).into_iter().filter(|p| !p.trim().is_empty()).collect(),
                    rules: str_list(rules.as_ref()).into_iter().filter(|r| !r.trim().is_empty()).collect(),
                };
                if !e.paths.is_empty() && !e.rules.is_empty() {
                    config.ignores.push(e);
                }
            }
        }
        config
    }
}

fn find_config(root: &Path) -> Option<PathBuf> {
    let mut cur = root.to_path_buf();
    for _ in 0..=CONFIG_SEARCH_LIMIT {
        for n in CONFIG_NAMES {
            let c = cur.join(n);
            if c.is_file() {
                return Some(c);
            }
        }
        if cur.join(".git").exists() {
            return None;
        }
        cur = cur.parent()?.to_path_buf();
    }
    None
}

/// Convert a parsed YAML value into JSON, stringifying non-string keys.
pub fn yaml_to_json(v: &dbt_yaml::Value) -> Value {
    use dbt_yaml::Value as Y;
    match v {
        Y::Null(_) => Value::Null,
        Y::Bool(b, _) => Value::Bool(*b),
        Y::Number(n, _) => {
            if let Some(i) = n.as_i64() {
                Value::from(i)
            } else if let Some(u) = n.as_u64() {
                Value::from(u)
            } else {
                n.as_f64().and_then(serde_json::Number::from_f64).map(Value::Number).unwrap_or(Value::Null)
            }
        }
        Y::String(s, _) => Value::String(s.clone()),
        Y::Sequence(s, _) => Value::Array(s.iter().map(yaml_to_json).collect()),
        Y::Mapping(m, _) => {
            let mut out = Map::new();
            for (k, v) in m {
                let key = match yaml_to_json(k) {
                    Value::String(s) => s,
                    other => crate::sqlutil::py_str(&other),
                };
                out.insert(key, yaml_to_json(v));
            }
            Value::Object(out)
        }
        Y::Tagged(t, _) => yaml_to_json(&t.value),
        Y::Timestamp(t, _) => Value::String(t.to_string()),
    }
}

pub fn load_yaml_str(text: &str) -> Result<Value, String> {
    if text.trim().is_empty() {
        return Ok(Value::Object(Map::new()));
    }
    let v: dbt_yaml::Value = dbt_yaml::from_str(text).map_err(|e| e.to_string())?;
    Ok(match yaml_to_json(&v) {
        Value::Null => Value::Object(Map::new()),
        other => other,
    })
}

/// Load a YAML file as a mapping. Non-mapping documents become empty maps.
fn load_yaml(path: &Path) -> (Map<String, Value>, Option<String>) {
    match read_source(path, false) {
        Err(e) => (Map::new(), Some(format!("{}: {e}", path.display()))),
        Ok(t) => match load_yaml_str(&t) {
            Ok(Value::Object(m)) => (m, None),
            Ok(_) => (Map::new(), None),
            Err(e) => (Map::new(), Some(format!("{}: {e}", path.display()))),
        },
    }
}

/// Read a project file for the rules, with owned markers blanked. With
/// `lossy`, invalid UTF-8 becomes U+FFFD; without it, invalid UTF-8 is an error.
/// Every reader of model or project text that rules see must use this.
pub fn read_source(path: &Path, lossy: bool) -> std::io::Result<String> {
    let text = if lossy { String::from_utf8_lossy(&std::fs::read(path)?).into_owned() } else { std::fs::read_to_string(path)? };
    Ok(crate::annotate::blank_owned_markers(&text))
}

fn read_text(path: &Path) -> (String, Option<String>) {
    match read_source(path, true) {
        Ok(t) => (t, None),
        Err(e) => (String::new(), Some(format!("{}: {e}", path.display()))),
    }
}

#[derive(Debug)]
pub struct ModelFile {
    pub path: PathBuf,
    pub relative_path: String,
    pub name: String,
    pub raw: String,
    pub stripped: String,
    pub without_directives: String,
    pub own_config: Config,
    pub effective_config: Config,
    pub folder_config: Config,
    pub layer: String,
    pub segments: Vec<String>,
    pub refs: Vec<String>,
    pub sources: Vec<(String, String)>,
    pub macro_calls: Vec<MacroCall>,
    pub is_python: bool,
    pub jinja: JinjaSummary,
}

impl ModelFile {
    pub fn materialization(&self) -> String {
        self.effective_config.get("materialized").map(crate::sqlutil::py_str).unwrap_or_default()
    }
    pub fn is_incremental(&self) -> bool {
        self.materialization() == "incremental"
    }
    pub fn line_of(&self, pos: usize) -> u32 {
        find_line_number(&self.raw, pos)
    }
}

#[derive(Debug)]
pub struct MacroFile {
    pub path: PathBuf,
    pub relative_path: String,
    pub raw: String,
    pub macros: Vec<MacroDef>,
    pub jinja: JinjaSummary,
}

#[derive(Debug)]
pub struct ProjectContext {
    pub root: PathBuf,
    pub name: String,
    /// The display name: `name`, or `name (relative_root)` when names collide.
    pub label: String,
    pub relative_root: String,
    pub project_yml: Map<String, Value>,
    /// The `dbt_project.yml` text, for anchors and placeholder scans.
    pub project_yml_text: String,
    pub packages: Map<String, Value>,
    pub models: Vec<ModelFile>,
    pub macros: Vec<MacroFile>,
    pub schema_models: IndexMap<String, Map<String, Value>>,
    pub schema_sources: IndexMap<String, String>,
    pub source_defs: Vec<Map<String, Value>>,
    /// The project-relative YAML file of each entry in `source_defs`.
    pub source_def_files: Vec<String>,
    pub snapshot_files: Vec<(PathBuf, String)>,
    pub singular_tests: Vec<(PathBuf, String)>,
    pub loose_sql: Vec<(PathBuf, String)>,
    pub graph: Graph,
    pub config: AuditConfig,
    pub provenance: ProvenanceVerdict,
    pub read_errors: Vec<String>,
    pub waiver_cache: RefCell<BTreeMap<String, FileWaivers>>,
}

impl ProjectContext {
    pub fn model_count(&self) -> usize {
        self.models.len()
    }
    pub fn model_by_name(&self, name: &str) -> Option<&ModelFile> {
        self.models.iter().find(|m| m.name == name)
    }
    pub fn schema_def(&self, name: &str) -> Option<&Map<String, Value>> {
        self.schema_models.get(name)
    }
}

#[derive(Debug)]
pub struct PortfolioContext {
    pub root: PathBuf,
    pub projects: Vec<ProjectContext>,
    pub config: AuditConfig,
    pub read_errors: Vec<String>,
}

fn excluded(name: &str) -> bool {
    EXCLUDED_DIRS.contains(&name) || name.starts_with('.')
}

/// Walk `root` and skip `EXCLUDED_DIRS`. Call `f(dir, file, name)` for each
/// non-directory entry. Skip a directory if its canonical path already
/// appears in the current ancestor chain; this prevents symlink cycles.
fn walk(root: &Path, mut f: impl FnMut(&Path, PathBuf, &str)) {
    let canon = |p: &Path| std::fs::canonicalize(p).unwrap_or_else(|_| p.to_path_buf());
    let mut stack = vec![(root.to_path_buf(), vec![canon(root)])];
    while let Some((cur, chain)) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&cur) else { continue };
        for e in rd.flatten() {
            let p = e.path();
            let name = e.file_name().to_string_lossy().to_string();
            if p.is_dir() {
                let c = canon(&p);
                if !excluded(&name) && !chain.contains(&c) {
                    let mut next = chain.clone();
                    next.push(c);
                    stack.push((p, next));
                }
            } else {
                f(&cur, p, &name);
            }
        }
    }
}

/// Find files recursively, excluding `EXCLUDED_DIRS`.
/// Supply lowercase suffixes with a leading dot.
pub fn iter_files(root: &Path, suffixes: &[&str]) -> Vec<PathBuf> {
    let mut out = vec![];
    walk(root, |_, p, _| {
        let ext = p.extension().map(|e| format!(".{}", e.to_string_lossy().to_lowercase())).unwrap_or_default();
        if suffixes.contains(&ext.as_str()) {
            out.push(p);
        }
    });
    out.sort();
    out
}

/// Every directory under `root` containing a `dbt_project.yml`.
pub fn find_projects(root: &Path) -> Vec<PathBuf> {
    let mut found = vec![];
    walk(root, |dir, _, name| {
        if name == "dbt_project.yml" {
            found.push(dir.to_path_buf());
        }
    });
    found.sort();
    found.dedup();
    found
}

/// Resolve the `models:` tree of `dbt_project.yml` for a model's path segments.
pub fn resolve_folder_config(project_yml: &Map<String, Value>, project_name: &str, segments: &[String]) -> Config {
    let Some(Value::Object(tree)) = project_yml.get("models") else { return Config::new() };
    let mut node = match tree.get(project_name) {
        Some(Value::Object(n)) => n,
        _ => {
            let cands: Vec<&Map<String, Value>> =
                tree.iter().filter(|(k, _)| !k.starts_with('+')).filter_map(|(_, v)| v.as_object()).collect();
            if cands.len() != 1 {
                return Config::new();
            }
            cands[0]
        }
    };
    let mut resolved = Config::new();
    for (k, v) in node {
        if let Some(k) = k.strip_prefix('+') {
            resolved.insert(k.trim_start_matches('+').to_string(), v.clone());
        }
    }
    for seg in segments {
        let Some(Value::Object(child)) = node.get(seg) else { break };
        node = child;
        for (k, v) in node {
            if let Some(k) = k.strip_prefix('+') {
                resolved.insert(k.trim_start_matches('+').to_string(), v.clone());
            }
        }
    }
    resolved
}

pub fn infer_layer(segments: &[String]) -> String {
    segments.iter().find_map(|s| layer_alias(&s.to_lowercase())).unwrap_or("").to_string()
}

fn path_list(project_yml: &Map<String, Value>, keys: &[&str], default: &str) -> Vec<String> {
    for k in keys {
        let v = project_yml.get(*k);
        if crate::sqlutil::truthy(v) {
            return str_list(v);
        }
    }
    vec![default.to_string()]
}

pub fn display_path(path: &Path) -> String {
    #[cfg(windows)]
    { path.to_string_lossy().replace('\\', "/") }
    #[cfg(not(windows))]
    { path.to_string_lossy().into_owned() }
}

fn rel(path: &Path, base: &Path) -> String {
    display_path(path.strip_prefix(base).unwrap_or(path))
}

pub fn build_project_context(project_root: &Path, audit_root: &Path, config: &AuditConfig) -> ProjectContext {
    let (project_yml, error) = load_yaml(&project_root.join("dbt_project.yml"));
    let project_yml_text = read_source(&project_root.join("dbt_project.yml"), false).unwrap_or_default();
    let name = match project_yml.get("name") {
        Some(v) if crate::sqlutil::truthy(Some(v)) => crate::sqlutil::py_str(v),
        _ => project_root.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default(),
    };
    let relative_root = match project_root.strip_prefix(audit_root) {
        Ok(p) if p.as_os_str().is_empty() => ".".to_string(),
        Ok(p) => display_path(p),
        Err(_) => display_path(project_root),
    };
    let mut ctx = ProjectContext {
        root: project_root.to_path_buf(),
        name: name.clone(),
        label: name.clone(),
        relative_root,
        project_yml,
        project_yml_text,
        packages: Map::new(),
        models: vec![],
        macros: vec![],
        schema_models: IndexMap::new(),
        schema_sources: IndexMap::new(),
        source_defs: vec![],
        source_def_files: vec![],
        snapshot_files: vec![],
        singular_tests: vec![],
        loose_sql: vec![],
        graph: Graph::default(),
        config: config.clone(),
        provenance: ProvenanceVerdict::default(),
        read_errors: vec![],
        waiver_cache: RefCell::new(BTreeMap::new()),
    };
    if let Some(e) = error {
        ctx.read_errors.push(e);
    }
    let pkg_path = project_root.join("packages.yml");
    let (packages, pkg_err) = load_yaml(&pkg_path);
    ctx.packages = packages;
    if let Some(e) = pkg_err.filter(|_| pkg_path.is_file()) {
        ctx.read_errors.push(e);
    }

    let model_paths = path_list(&ctx.project_yml, &["model-paths", "source-paths"], "models");
    for dir in model_paths.iter().map(|p| project_root.join(p)) {
        if !dir.is_dir() {
            continue;
        }
        for path in iter_files(&dir, &[".sql", ".py"]) {
            let (raw, err) = read_text(&path);
            if let Some(e) = err {
                ctx.read_errors.push(e);
                continue;
            }
            let segments: Vec<String> = path
                .strip_prefix(&dir)
                .unwrap()
                .parent()
                .map(|p| p.components().map(|c| c.as_os_str().to_string_lossy().to_string()).collect())
                .unwrap_or_default();
            let is_sql = path.extension().is_some_and(|e| e == "sql");
            let own_config = if is_sql { extract_config(&raw) } else { Config::new() };
            let folder_config = resolve_folder_config(&ctx.project_yml, &name, &segments);
            let mut effective = folder_config.clone();
            effective.extend(own_config.clone());
            let relative_path = rel(&path, project_root);
            let jinja = if is_sql { summarize(&raw, &relative_path) } else { JinjaSummary::default() };
            ctx.models.push(ModelFile {
                name: path.file_stem().unwrap().to_string_lossy().to_string(),
                relative_path,
                stripped: strip_all(&raw),
                without_directives: blank_directives(&raw),
                own_config,
                folder_config,
                effective_config: effective,
                layer: infer_layer(&segments),
                refs: extract_refs(&raw),
                sources: extract_sources(&raw),
                macro_calls: extract_macro_calls(&raw),
                is_python: path.extension().is_some_and(|e| e == "py"),
                segments,
                raw,
                path,
                jinja,
            });
        }
        for path in iter_files(&dir, &[".yml", ".yaml"]) {
            let (data, err) = load_yaml(&path);
            if let Some(e) = err {
                ctx.read_errors.push(e);
                continue;
            }
            let relative = rel(&path, project_root);
            if let Some(Value::Array(models)) = data.get("models") {
                for e in models {
                    if let Value::Object(o) = e
                        && let Some(n) = o.get("name").filter(|v| crate::sqlutil::truthy(Some(v))) {
                            let n = crate::sqlutil::py_str(n);
                            ctx.schema_models.insert(n.clone(), o.clone());
                            ctx.schema_sources.insert(n, relative.clone());
                        }
                }
            }
            if let Some(Value::Array(sources)) = data.get("sources") {
                for o in sources.iter().filter_map(|s| s.as_object().cloned()) {
                    ctx.source_defs.push(o);
                    ctx.source_def_files.push(relative.clone());
                }
            }
        }
    }

    for d in path_list(&ctx.project_yml, &["macro-paths"], "macros") {
        let dir = project_root.join(d);
        if !dir.is_dir() {
            continue;
        }
        for path in iter_files(&dir, &[".sql"]) {
            let (raw, err) = read_text(&path);
            if let Some(e) = err {
                ctx.read_errors.push(e);
                continue;
            }
            let relative_path = rel(&path, project_root);
            ctx.macros.push(MacroFile {
                macros: extract_macro_defs(&raw),
                jinja: summarize(&raw, &relative_path),
                relative_path,
                raw,
                path,
            });
        }
    }
    for d in path_list(&ctx.project_yml, &["snapshot-paths"], "snapshots") {
        let dir = project_root.join(d);
        if dir.is_dir() {
            for path in iter_files(&dir, &[".sql"]) {
                let raw = read_text(&path).0;
                ctx.snapshot_files.push((path, raw));
            }
        }
    }
    for d in path_list(&ctx.project_yml, &["test-paths"], "tests") {
        let dir = project_root.join(d);
        if dir.is_dir() {
            for path in iter_files(&dir, &[".sql"]) {
                let raw = read_text(&path).0;
                ctx.singular_tests.push((path, raw));
            }
        }
    }
    for extra in ["macros_sql", "scripts", "sql", "orchestration", "etl_configuration"] {
        let dir = project_root.join(extra);
        if dir.is_dir() {
            for path in iter_files(&dir, &[".sql"]) {
                let raw = read_text(&path).0;
                ctx.loose_sql.push((path, raw));
            }
        }
    }
    ctx.graph = Graph::from_models(&ctx.models);
    ctx
}

/// Give each project whose name is not unique the label `name (relative_root)`.
pub fn set_labels(projects: &mut [ProjectContext]) {
    let names: Vec<String> = projects.iter().map(|p| p.name.clone()).collect();
    for p in projects.iter_mut() {
        p.label = if names.iter().filter(|n| **n == p.name).count() > 1 {
            format!("{} ({})", p.name, p.relative_root)
        } else {
            p.name.clone()
        };
    }
}

/// A project-relative path as a path relative to the audit root.
pub fn root_relative(project: &ProjectContext, file: &str) -> String {
    let pre = &project.relative_root;
    if file.is_empty() || pre.is_empty() || pre == "." || file.starts_with('<') || Path::new(file).is_absolute()
        || file.starts_with(&format!("{pre}/"))
    {
        return file.to_string();
    }
    format!("{pre}/{file}")
}

/// One table of a [`SourceDecl`].
#[derive(Debug, Clone)]
pub struct SourceTableDecl {
    pub name: String,
    /// 1-based line of the table's `name:`.
    pub line: u32,
    /// The `identifier:` as written, if set; dbt defaults it to `name`.
    pub identifier: Option<String>,
    /// `quoting.identifier` on the table, overriding the source's.
    pub quote_identifier: Option<bool>,
}

/// One `sources:` entry with its position, for findings that must cite
/// `path:line`. Values are the raw YAML strings, so `{{ var(..) }}` is kept.
#[derive(Debug, Clone)]
pub struct SourceDecl {
    /// Index into `ProjectContext::source_defs`.
    pub index: usize,
    pub name: String,
    /// Project-relative YAML file.
    pub file: String,
    /// 1-based line of the source's `name:`.
    pub line: u32,
    pub database: Option<String>,
    pub schema: Option<String>,
    /// `quoting.database` / `quoting.schema` / `quoting.identifier` on the source.
    pub quoting: [Option<bool>; 3],
    pub tables: Vec<SourceTableDecl>,
}

/// A `- ` list item found by [`yaml_list_items`]: its first line index and
/// the line index one past its end.
struct YamlItem {
    start: usize,
    end: usize,
}

fn indent_of(l: &str) -> usize {
    l.len() - l.trim_start().len()
}

fn yaml_blank(l: &str) -> bool {
    let t = l.trim();
    t.is_empty() || t.starts_with('#')
}

/// The list items under the key line `key_line` (a `key:` whose value is a
/// block list), as line ranges.
fn yaml_list_items(lines: &[&str], key_line: usize) -> Vec<YamlItem> {
    let key_indent = indent_of(lines[key_line]);
    let mut items: Vec<YamlItem> = vec![];
    let mut item_indent = None;
    let mut i = key_line + 1;
    while i < lines.len() {
        let l = lines[i];
        if yaml_blank(l) {
            i += 1;
            continue;
        }
        let ind = indent_of(l);
        let dash = l.trim_start().starts_with("- ") || l.trim() == "-";
        if ind < key_indent || (ind == key_indent && !dash) {
            break;
        }
        match item_indent {
            None if dash => item_indent = Some(ind),
            None => break,
            _ => {}
        }
        if dash && Some(ind) == item_indent {
            if let Some(last) = items.last_mut() {
                last.end = i;
            }
            items.push(YamlItem { start: i, end: lines.len() });
        } else if ind < item_indent.unwrap() {
            break;
        }
        i += 1;
    }
    if let Some(last) = items.last_mut() {
        last.end = last.end.min(i);
    }
    items
}

/// The line index of `key:` directly inside the item (on its dash line, or at
/// the item's content indent).
fn yaml_item_key(lines: &[&str], item: &YamlItem, key: &str) -> Option<usize> {
    let first = lines[item.start];
    let content = indent_of(first) + 2;
    let re = regex::Regex::new(&format!(r#"^[ \t]*(?:-[ \t]+)?["']?{}["']?[ \t]*:"#, regex::escape(key))).ok()?;
    (item.start..item.end).find(|&i| {
        let l = lines[i];
        let at_item = if i == item.start { true } else { indent_of(l) == content && !l.trim_start().starts_with('-') };
        at_item && re.is_match(l)
    })
}

fn bool_at(o: &Map<String, Value>, path: &[&str]) -> Option<bool> {
    let mut v = o.get(path[0])?;
    for k in &path[1..] {
        v = v.get(*k)?;
    }
    v.as_bool()
}

fn str_at(o: &Map<String, Value>, k: &str) -> Option<String> {
    o.get(k).filter(|v| crate::sqlutil::truthy(Some(v))).map(crate::sqlutil::py_str)
}

/// Every `sources:` entry of `p` with the line of its name and of each
/// table. Lines come from a text scan of each sources file, paired in order
/// with the parsed entries; a scan that does not line up with the parse falls
/// back to the first `- name: X` line, or line 1.
pub fn source_decls(p: &ProjectContext) -> Vec<SourceDecl> {
    let mut out = vec![];
    let mut files: Vec<&String> = p.source_def_files.iter().collect();
    files.dedup();
    for file in files {
        let text = read_source(&p.root.join(file), true).unwrap_or_default();
        let lines: Vec<&str> = text.lines().collect();
        let items = lines
            .iter()
            .position(|l| crate::rx!(r#"^["']?sources["']?[ \t]*:[ \t]*(?:#.*)?$"#).is_match(l))
            .map(|k| yaml_list_items(&lines, k))
            .unwrap_or_default();
        let defs: Vec<usize> = (0..p.source_defs.len()).filter(|&i| &p.source_def_files[i] == file).collect();
        for (n, &di) in defs.iter().enumerate() {
            let d = &p.source_defs[di];
            let name = str_at(d, "name").unwrap_or_default();
            let item = items.get(n).filter(|_| items.len() == defs.len());
            let name_line = item.and_then(|it| yaml_item_key(&lines, it, "name")).or_else(|| {
                let re = regex::Regex::new(&format!(r#"^[ \t]*-[ \t]*name[ \t]*:[ \t]*["']?{}["']?[ \t]*$"#, regex::escape(&name))).ok()?;
                lines.iter().position(|l| re.is_match(l))
            });
            let table_items = item
                .and_then(|it| yaml_item_key(&lines, it, "tables"))
                .map(|k| yaml_list_items(&lines, k))
                .unwrap_or_default();
            let tables: Vec<SourceTableDecl> = match d.get("tables") {
                Some(Value::Array(a)) => a
                    .iter()
                    .enumerate()
                    .filter_map(|(ti, t)| {
                        let o = t.as_object()?;
                        let tname = str_at(o, "name")?;
                        let line = table_items
                            .get(ti)
                            .filter(|_| table_items.len() == a.len())
                            .and_then(|it| yaml_item_key(&lines, it, "name"))
                            .or(name_line);
                        Some(SourceTableDecl {
                            name: tname,
                            line: line.map_or(1, |l| l as u32 + 1),
                            identifier: str_at(o, "identifier"),
                            quote_identifier: bool_at(o, &["quoting", "identifier"]),
                        })
                    })
                    .collect(),
                _ => vec![],
            };
            out.push(SourceDecl {
                index: di,
                name,
                file: file.clone(),
                line: name_line.map_or(1, |l| l as u32 + 1),
                database: str_at(d, "database"),
                schema: str_at(d, "schema"),
                quoting: [bool_at(d, &["quoting", "database"]), bool_at(d, &["quoting", "schema"]), bool_at(d, &["quoting", "identifier"])],
                tables,
            });
        }
    }
    out
}

pub fn build_portfolio(root: &Path) -> PortfolioContext {
    build_portfolio_with_ddl(root, &[])
}

/// `build_portfolio`, but a non-empty `ddl` replaces the configured `ddl_paths`.
pub fn build_portfolio_with_ddl(root: &Path, ddl: &[PathBuf]) -> PortfolioContext {
    let root = std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf());
    let mut config = AuditConfig::load(&root);
    if !ddl.is_empty() {
        config.ddl_paths = ddl.iter().map(|p| std::path::absolute(p).unwrap_or_else(|_| p.clone())).collect();
        config.ddl = std::sync::Arc::new(crate::ddl::DdlIndex::load(&config.ddl_paths));
    }
    let mut projects: Vec<ProjectContext> = find_projects(&root).iter().map(|p| build_project_context(p, &root, &config)).collect();
    set_labels(&mut projects);
    PortfolioContext { root, projects, config, read_errors: vec![] }
}

/// Python `fnmatch.fnmatch` on POSIX: `*` and `?` match any character
/// including `/`, `[...]` is a character class.
pub fn fnmatch(name: &str, pattern: &str) -> bool {
    let mut re = String::from("(?s)^");
    let chars: Vec<char> = pattern.chars().collect();
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        i += 1;
        match c {
            '*' => re.push_str(".*"),
            '?' => re.push('.'),
            '[' => {
                let mut j = i;
                if j < chars.len() && chars[j] == '!' {
                    j += 1;
                }
                if j < chars.len() && chars[j] == ']' {
                    j += 1;
                }
                while j < chars.len() && chars[j] != ']' {
                    j += 1;
                }
                if j >= chars.len() {
                    re.push_str("\\[");
                } else {
                    let mut stuff: String = chars[i..j].iter().collect::<String>().replace('\\', "\\\\");
                    i = j + 1;
                    if let Some(rest) = stuff.strip_prefix('!') {
                        stuff = format!("^{rest}");
                    } else if stuff.starts_with('^') {
                        stuff = format!("\\{stuff}");
                    }
                    re.push('[');
                    re.push_str(&stuff);
                    re.push(']');
                }
            }
            c => re.push_str(&regex::escape(&c.to_string())),
        }
    }
    re.push('$');
    regex::Regex::new(&re).is_ok_and(|r| r.is_match(name))
}

#[cfg(test)]
mod tests {
    use super::fnmatch;

    #[test]
    fn fnmatch_matches_python() {
        assert!(fnmatch("models/a/b.sql", "models/*"));
        assert!(fnmatch("models/a.sql", "*.sql"));
        assert!(!fnmatch("models/a.sql", "*.yml"));
        assert!(fnmatch("x1", "x[0-9]"));
    }
}
