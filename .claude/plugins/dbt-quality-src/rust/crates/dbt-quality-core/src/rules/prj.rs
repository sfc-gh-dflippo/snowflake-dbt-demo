//! PRJ rules: project structure and fragmentation.

use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;
use std::process::Command;

use serde_json::{json, Map, Value};

use crate::discovery::{PortfolioContext, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, level, plural, severity, Suggestion};
use crate::provenance::PLACEHOLDER_VALUES;
use crate::anchors::project_yml_position;
use crate::rx;
use crate::sqlutil::{line_col, py_str, span, strip_comments_and_strings};

pub mod shared;
pub(crate) mod relations;

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTPRJ0001", detect: Detect::Portfolio(prj0001) },
    Detector { code: "SSC-EWI-DBTPRJ0002", detect: Detect::Portfolio(prj0002) },
    Detector { code: "SSC-EWI-DBTPRJ0003", detect: Detect::Portfolio(prj0003) },
    Detector { code: "SSC-EWI-DBTPRJ0004", detect: Detect::Project(prj0004) },
    Detector { code: "SSC-EWI-DBTPRJ0005", detect: Detect::Project(prj0005) },
    Detector { code: "SSC-EWI-DBTPRJ0006", detect: Detect::Portfolio(prj0006) },
    Detector { code: "SSC-EWI-DBTPRJ0007", detect: Detect::Project(prj0007) },
    Detector { code: "SSC-EWI-DBTPRJ0008", detect: Detect::Project(prj0008) },
    Detector { code: "SSC-EWI-DBTPRJ0009", detect: Detect::Project(prj0009) },
    Detector { code: "SSC-EWI-DBTPRJ0010", detect: Detect::Project(prj0010) },
    Detector { code: "SSC-EWI-DBTPRJ0011", detect: Detect::Project(prj0011) },
    Detector { code: "SSC-EWI-DBTPRJ0012", detect: Detect::Portfolio(prj0012) },
    Detector { code: "SSC-EWI-DBTPRJ0013", detect: Detect::Project(prj0013) },
    Detector { code: "SSC-EWI-DBTPRJ0014", detect: Detect::Project(prj0014) },
    Detector { code: "SSC-EWI-DBTPRJ0015", detect: Detect::Project(prj0015) },
    Detector { code: "SSC-EWI-DBTPRJ0016", detect: Detect::Project(prj0016) },
    Detector { code: "SSC-EWI-DBTPRJ0017", detect: Detect::Project(prj0017) },
    Detector { code: "SSC-EWI-DBTPRJ0018", detect: Detect::Project(prj0018) },
    Detector { code: "SSC-EWI-DBTPRJ0019", detect: Detect::Portfolio(prj0019) },
    Detector { code: "SSC-EWI-DBTPRJ0020", detect: Detect::Portfolio(prj0020) },
    Detector { code: "SSC-EWI-DBTPRJ0021", detect: Detect::Portfolio(prj0021) },
    Detector { code: "SSC-EWI-DBTPRJ0022", detect: Detect::Portfolio(prj0022) },
];

const EXPECTED_PACKAGES: &[(&str, &str)] = &[
    ("dbt_constraints", "Snowflake-Labs/dbt_constraints"),
    ("dbt_semantic_view", "Snowflake-Labs/dbt_semantic_view"),
];
const COMMITTED_ARTIFACT_DIRS: &[&str] = &["target", "logs", "dbt_packages"];

/// Render a version string as plain text, including Python list representations.
fn fmt_ver(raw: &str) -> String {
    let t = raw.trim();
    if !(t.starts_with('[') && t.ends_with(']')) {
        return raw.to_string();
    }
    let inner = &t[1..t.len() - 1];
    let mut items = vec![];
    let (mut cur, mut quote) = (String::new(), None::<char>);
    for c in inner.chars() {
        match quote {
            Some(q) if c == q => quote = None,
            Some(_) => cur.push(c),
            None if c == '\'' || c == '"' => quote = Some(c),
            None if c == ',' => items.push(std::mem::take(&mut cur)),
            None => cur.push(c),
        }
    }
    if !cur.trim().is_empty() || !items.is_empty() {
        items.push(cur);
    }
    items.iter().map(|s| s.trim()).collect::<Vec<_>>().join(",")
}

fn packages_list(project: &ProjectContext) -> Vec<&Value> {
    match project.packages.get("packages") {
        Some(Value::Array(a)) => a.iter().collect(),
        _ => vec![],
    }
}

/// `file` under `project`, relative to the portfolio root.
fn root_rel(project: &ProjectContext, file: &str) -> String {
    match project.relative_root.as_str() {
        "" | "." => file.to_string(),
        r => format!("{r}/{file}"),
    }
}

/// 1-based line of the first line in `text` that contains `needle`.
fn line_with(text: &str, needle: &str) -> Option<u32> {
    text.lines().position(|l| l.contains(needle)).map(|i| i as u32 + 1)
}

fn packages_text(project: &ProjectContext) -> String {
    std::fs::read_to_string(project.root.join("packages.yml")).unwrap_or_default()
}

fn prj0001(p: &PortfolioContext) -> Vec<Suggestion> {
    let threshold = p.config.micro_project_threshold;
    let mut out = vec![];
    if p.projects.len() < 2 {
        return out;
    }
    for project in &p.projects {
        let count = project.model_count();
        if count as i64 > threshold {
            continue;
        }
        let sev = if count <= 2 { severity::MEDIUM } else { severity::LOW };
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTPRJ0001",
                format!(
                    "Project `{}` has {} model{}, at or below the local {}-model consolidation threshold.",
                    project.name,
                    count,
                    if count == 1 { "" } else { "s" },
                    threshold
                ),
            )
            .severity(sev)
            .project(project.label.clone())
            .file(format!("{}/dbt_project.yml", project.relative_root))
            .evidence(format!("{} model(s) in {}", count, project.relative_root))
            .remediation(
                "Consider consolidation when the models share ownership and a release schedule. Separate projects can retain lineage through supported cross-project dependencies; check the deployed runtime. Use ref() for actual model dependencies rather than treating project size as proof of fragmentation.",
            )
            .effort(effort::HIGH)
            .ctx("model_count", json!(count)),
        );
    }
    out
}

/// Project names that share sources, and the `(source, table)` pairs they share.
type SharedSources = (BTreeSet<String>, Vec<(String, String)>);

fn prj0002(p: &PortfolioContext) -> Vec<Suggestion> {
    let mut out = vec![];
    if p.projects.len() < 2 {
        return out;
    }
    // Insertion-ordered: source -> project names.
    let mut by_source: Vec<((String, String), BTreeSet<String>)> = vec![];
    for project in &p.projects {
        for model in &project.models {
            for s in &model.sources {
                match by_source.iter_mut().find(|(k, _)| k == s) {
                    Some((_, set)) => {
                        set.insert(project.name.clone());
                    }
                    None => by_source.push((s.clone(), BTreeSet::from([project.name.clone()]))),
                }
            }
        }
    }
    let mut shared: Vec<SharedSources> = vec![];
    for (source, names) in by_source {
        if names.len() > 1 {
            match shared.iter_mut().find(|(k, _)| *k == names) {
                Some((_, v)) => v.push(source),
                None => shared.push((names, vec![source])),
            }
        }
    }
    for (names, mut sources) in shared {
        let names: Vec<String> = names.into_iter().collect();
        sources.sort();
        let labels: Vec<String> = sources.iter().map(|s| format!("{}.{}", s.0, s.1)).take(5).collect();
        let total: usize =
            p.projects.iter().filter(|x| names.contains(&x.name)).map(|x| x.model_count()).sum();
        let mut related: Vec<String> = vec![];
        for project in p.projects.iter().filter(|x| names.contains(&x.name)) {
            for d in crate::discovery::source_decls(project) {
                for t in &d.tables {
                    if sources.iter().any(|(sn, tn)| *sn == d.name && *tn == t.name) {
                        related.push(format!("{}:{}", root_rel(project, &d.file), t.line));
                    }
                }
            }
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTPRJ0002",
                format!(
                    "{} projects ({}) use the same logical {} names ({}{}). Verify physical source identity; shared input alone does not create a model dependency.",
                    names.len(),
                    names.join(", "),
                    plural(sources.len(), "source"),
                    labels.join(", "),
                    if sources.len() > 5 { " ..." } else { "" }
                ),
            )
            .file("<portfolio>")
            .evidence(format!("shared sources: {}", labels.join(", ")))
            .remediation(format!(
                "Review these {} projects and {} models for shared source ownership. Compare database, schema, identifier, and quoting before consolidating definitions. Keep intentional project boundaries; express actual model dependencies with configured refs, not an ordering dependency between independent readers.",
                names.len(),
                total
            ))
            .effort(effort::HIGH)
            .ctx("projects", json!(names))
            .ctx("related_files", json!(related)),
        );
    }
    out
}

fn prj0003(p: &PortfolioContext) -> Vec<Suggestion> {
    if p.projects.len() < 3 {
        return vec![];
    }
    let mut versions: Vec<(String, BTreeSet<String>)> = vec![];
    for project in &p.projects {
        for pkg in packages_list(project) {
            let Value::Object(o) = pkg else { continue };
            if !crate::sqlutil::truthy(o.get("package")) {
                continue;
            }
            let name = py_str(&o["package"]);
            let ver = o.get("version").map(py_str).unwrap_or_else(|| "unpinned".into());
            match versions.iter_mut().find(|(k, _)| *k == name) {
                Some((_, s)) => {
                    s.insert(ver);
                }
                None => versions.push((name, BTreeSet::from([ver]))),
            }
        }
    }
    let drifted: Vec<(String, Vec<String>)> = versions
        .into_iter()
        .filter(|(_, v)| v.len() > 1)
        .map(|(n, v)| (n, v.into_iter().collect()))
        .collect();
    let mut msg = format!(
        "These {} projects maintain separate `dbt_project.yml` and package configuration",
        p.projects.len()
    );
    if drifted.is_empty() {
        msg.push('.');
    } else {
        let parts: Vec<String> = drifted
            .iter()
            .take(3)
            .map(|(n, v)| format!("{n} ({})", v.iter().map(|x| fmt_ver(x)).collect::<Vec<_>>().join(" vs ")))
            .collect();
        msg.push_str(&format!(
            ". {} {} already at different versions: {}.",
            plural(drifted.len(), "package"),
            if drifted.len() == 1 { "is" } else { "are" },
            parts.join("; ")
        ));
    }
    let mut drift = Map::new();
    for (n, v) in &drifted {
        drift.insert(n.clone(), json!(v));
    }
    let mut related: Vec<String> = vec![];
    for project in &p.projects {
        let text = packages_text(project);
        let lines: Vec<String> = drifted
            .iter()
            .filter_map(|(n, _)| line_with(&text, n))
            .map(|l| format!("{}:{l}", root_rel(project, "packages.yml")))
            .collect();
        if lines.is_empty() {
            related.push(format!("{}:1", root_rel(project, "dbt_project.yml")));
        }
        related.extend(lines);
    }
    let root_name = p.root.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
    vec![Suggestion::new("SSC-EWI-DBTPRJ0003", msg)
        .file("<portfolio>")
        .evidence(format!("{} dbt_project.yml files under {}", p.projects.len(), root_name))
        .remediation("Consider consolidation when configuration and release ownership match. Otherwise review differing package versions for compatibility, align versions where appropriate, and retain package-lock.yml after dbt deps. Different versions are not automatically wrong.")
        .effort(effort::HIGH)
        .ctx("version_drift", Value::Object(drift))
        .ctx("related_files", json!(related))]
}

/// `(tracked, ignored)` from git; `tracked` is `None` when git cannot answer.
fn git_status(root: &Path, path: &Path) -> (Option<bool>, bool) {
    let git = |args: &[&str]| Command::new("git").arg("-C").arg(root).args(args).arg(path).output();
    let probe = Command::new("git").arg("-C").arg(root).args(["rev-parse", "--git-dir"]).output();
    if !matches!(probe, Ok(ref o) if o.status.success()) {
        return (None, false);
    }
    let tracked = match git(&["ls-files", "--error-unmatch"]) {
        Ok(o) => o.status.success(),
        Err(_) => return (None, false),
    };
    let ignored = match git(&["check-ignore", "--"]) {
        Ok(o) => match o.status.code() {
            Some(0) => true,
            Some(1) => false,
            _ => return (None, false),
        },
        Err(_) => return (None, false),
    };
    (Some(tracked), ignored)
}

fn prj0004(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for name in ["profiles.yml", "profiles.yaml"] {
        let path = project.root.join(name);
        if !path.is_file() {
            continue;
        }
        let (tracked, ignored) = git_status(&project.root, &path);
        let (lvl, message) = if tracked == Some(true) {
            (level::WARNING, format!("`{name}` is tracked in git inside the project directory."))
        } else if ignored {
            (level::INFORMATION, format!("`{name}` is present in the project directory but is git-ignored."))
        } else if tracked == Some(false) {
            (
                level::WARNING,
                format!("`{name}` is present in the project directory and is not covered by `.gitignore`, so it can be committed."),
            )
        } else {
            (level::WARNING, format!("`{name}` is present in the project directory."))
        };
        let mut rem = String::from(
            "Prefer `~/.dbt/profiles.yml` or a profiles directory supported by the installed dbt runtime. Keep only a redacted `profiles.yml.sample` in the repository.",
        );
        if tracked == Some(true) {
            rem.push_str(&format!(
                " Review `git rm --cached {name}` to stop tracking the file. If a real credential was exposed, rotate it and follow the incident process. Removing the file from the index or rotating a credential does not erase Git history."
            ));
        } else {
            rem.push_str(" If it is not already, add it to `.gitignore`.");
        }
        out.push(
            Suggestion::new("SSC-EWI-DBTPRJ0004", message)
                .level(lvl)
                .file(name)
                .evidence(format!("{name} found at project root"))
                .remediation(rem)
                .effort(effort::LOW),
        );
    }
    out
}

fn prj0005(project: &ProjectContext) -> Vec<Suggestion> {
    let hay = [
        ("dbt_project.yml", py_str(&Value::Object(project.project_yml.clone())), project.project_yml_text.clone()),
        ("packages.yml", py_str(&Value::Object(project.packages.clone())), packages_text(project)),
    ];
    let mut out = vec![];
    for (filename, text, raw) in hay {
        let found: Vec<&str> = PLACEHOLDER_VALUES
            .iter()
            .copied()
            .filter(|p| text.contains(p))
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect();
        if found.is_empty() {
            continue;
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTPRJ0005",
                format!(
                    "`{}` contains converter placeholder {}: {}.",
                    filename,
                    plural(found.len(), "value"),
                    found.join(", ")
                ),
            )
            .file(filename)
            .line_opt(found.iter().filter_map(|f| line_with(&raw, f)).min())
            .evidence(found.join(", "))
            .remediation("Replace project/profile placeholders with real names. Location overrides, including `sc_override_*_db`/`_schema`, belong to PRJ0009/PRJ0021/PRJ0022: replace location uses with literal or target-driven source locations, verify the existing target maps to the correct database, and do not change orchestration calls. Old runtime keys no longer affect removed location uses. Keep declarations and runtime inputs needed by remaining non-location value reads; remove a declaration only after all its uses are gone.")
            .effort(effort::LOW),
        );
    }
    out
}

fn prj0006(p: &PortfolioContext) -> Vec<Suggestion> {
    let mut hits: Vec<(String, String, crate::sqlutil::TextSpan)> = vec![];
    for project in &p.projects {
        for (path, raw) in &project.loose_sql {
            let stripped = strip_comments_and_strings(raw);
            for m in rx!(r"(?i)\bEXECUTE\s+DBT\s+PROJECT\b").find_iter(&stripped) {
                let rel = crate::discovery::display_path(path.strip_prefix(&p.root).unwrap_or(path));
                hits.push((project.label.clone(), rel, span(&stripped, m.start(), m.end())));
            }
        }
    }
    if hits.len() < 2 {
        return vec![];
    }
    let files: Vec<String> = hits.iter().map(|h| h.1.clone()).collect::<BTreeSet<_>>().into_iter().collect();
    let related: Vec<String> = hits.iter().map(|h| format!("{}:{}", h.1, h.2.line)).collect();
    let (pname, path, pos) = hits[0].clone();
    vec![Suggestion::new(
        "SSC-EWI-DBTPRJ0006",
        format!(
            "{} `EXECUTE DBT PROJECT` invocations appear across {}; verify whether the {} project executions through a task graph.",
            hits.len(),
            plural(files.len(), "orchestration script"),
            if files.len() == 1 { "script chains" } else { "scripts chain" }
        ),
    )
    .project(pname)
    .file(path)
    .span(pos)
    .evidence(format!("EXECUTE DBT PROJECT found in: {}", files.iter().take(5).cloned().collect::<Vec<_>>().join(", ")))
    .remediation("Consider merging projects that form one pipeline with shared ownership. A dbt build runs selected resources in dependency order, with independent branches able to run concurrently. Task graphs can validly order separate projects and external dependencies; keep and document that contract when the boundary is intentional.")
    .effort(effort::HIGH)
    .ctx("occurrence_count", json!(hits.len()))
    .ctx("related_files", json!(related))]
}

fn prj0007(project: &ProjectContext) -> Vec<Suggestion> {
    if project.model_count() == 0 {
        return vec![];
    }
    let declared: BTreeSet<String> = packages_list(project)
        .into_iter()
        .filter_map(|p| p.as_object())
        .map(|o| {
            let s = o.get("package").map(py_str).unwrap_or_default();
            s.rsplit('/').next().unwrap_or("").to_string()
        })
        .collect();
    let missing: Vec<&str> =
        EXPECTED_PACKAGES.iter().filter(|(s, _)| !declared.contains(*s)).map(|(_, c)| *c).collect();
    if missing.is_empty() {
        return vec![];
    }
    let decl = if declared.is_empty() { "none".to_string() } else { declared.iter().cloned().collect::<Vec<_>>().join(", ") };
    vec![Suggestion::new("SSC-EWI-DBTPRJ0007", format!("`packages.yml` does not declare: {}.", missing.join(", ")))
        .file("packages.yml")
        .evidence(format!("declared: {decl}"))
        .remediation("If the local baseline applies, select compatible versions of the missing packages and run `dbt deps`. The ranges below are examples; validate runtime support:\n\n```yaml\npackages:\n  - package: Snowflake-Labs/dbt_constraints\n    version: [\">=1.0.0\", \"<2.0.0\"]\n  - package: Snowflake-Labs/dbt_semantic_view\n    version: [\">=1.0.0\", \"<2.0.0\"]\n```\n\n`dbt_constraints` can generate constraint metadata from tests on supported table models. Standard Snowflake PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints are not enforced. Keep tests running, especially for RELY metadata. `dbt_semantic_view` supplies a materialization; explicit semantic-view definitions are still required.")
        .effort(effort::LOW)
        .ctx("missing", json!(missing))]
}

fn prj0008(project: &ProjectContext) -> Vec<Suggestion> {
    let gi = project.root.join(".gitignore");
    let text = if gi.is_file() {
        std::fs::read(&gi).map(|b| String::from_utf8_lossy(&b).into_owned()).unwrap_or_default()
    } else {
        String::new()
    };
    let present: Vec<&str> = COMMITTED_ARTIFACT_DIRS
        .iter()
        .copied()
        .filter(|n| project.root.join(n).is_dir() && !text.contains(n))
        .collect();
    if present.is_empty() {
        return vec![];
    }
    let one = present.len() == 1;
    let list = present.iter().map(|n| format!("{n}/")).collect::<Vec<_>>().join("\n");
    vec![Suggestion::new(
        "SSC-EWI-DBTPRJ0008",
        format!(
            "Generated director{} {} {} present without detected `.gitignore` coverage. This scan does not prove Git tracks them.",
            if one { "y" } else { "ies" },
            present.join(", "),
            if one { "is" } else { "are" }
        ),
    )
    .file(".gitignore")
    .evidence(format!("unignored: {}", present.join(", ")))
    .remediation(format!("Add to `.gitignore`:\n\n```\n{list}\n```\n\nThen `git rm -r --cached` any that are already tracked."))
    .effort(effort::LOW)]
}

// ---- Parameter rules (PRJ0009-PRJ0018) ----

/// One text file of a project: SQL or YAML, with a project-relative path.
struct Src {
    file: String,
    text: String,
    yaml: bool,
}

fn project_sources(p: &ProjectContext) -> Vec<Src> {
    let rel = |path: &Path| path.strip_prefix(&p.root).map(crate::discovery::display_path).unwrap_or_default();
    let mut out: Vec<Src> = vec![];
    for path in crate::discovery::iter_files(&p.root, &[".sql", ".yml", ".yaml"]) {
        let name = path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
        let yaml = !name.ends_with(".sql");
        if name.starts_with('.') || ["profiles.yml", "packages.yml", "dependencies.yml", "selectors.yml"].contains(&name.as_str()) {
            continue;
        }
        let nested = path.ancestors().skip(1).take_while(|a| *a != p.root.as_path()).any(|a| a.join("dbt_project.yml").is_file());
        if nested {
            continue;
        }
        if let Ok(text) = crate::discovery::read_source(&path, true) {
            out.push(Src { file: rel(&path), text, yaml });
        }
    }
    out
}

fn lit_text(l: &crate::jinja::Lit) -> String {
    use crate::jinja::Lit;
    match l {
        Lit::Str(s) | Lit::Expr(s) => s.clone(),
        Lit::List(v) => v.iter().map(lit_text).collect::<Vec<_>>().join(" "),
        Lit::Map(v) => v.iter().map(|(_, x)| lit_text(x)).collect::<Vec<_>>().join(" "),
        _ => String::new(),
    }
}

struct VarRead {
    key: String,
    has_default: bool,
    default: Option<String>,
    pos: usize,
    end: usize,
}

/// Every `var('key'[, default])` call with a literal key.
fn var_reads(text: &str) -> Vec<VarRead> {
    let mut out = vec![];
    for c in rx!(r#"\bvar\(\s*(?:'([^']+)'|"([^"]+)")\s*(,)?"#).captures_iter(text) {
        let m = c.get(0).unwrap();
        let key = c.get(1).or(c.get(2)).unwrap().as_str().to_string();
        let has_default = c.get(3).is_some();
        let mut default = None;
        if has_default {
            let rest = text[m.end()..].trim_start();
            if let Some(q) = rest.chars().next().filter(|q| *q == '\'' || *q == '"') {
                default = rest[1..].find(q).map(|i| rest[1..1 + i].to_string());
            }
        }
        out.push(VarRead { key, has_default, default, pos: m.start(), end: m.end(), });
    }
    out
}

fn has_dynamic_var(text: &str) -> bool {
    rx!(r#"\bvar\(\s*[^'"\s)]"#).is_match(text)
}

/// True when `pos` lies in a hook string (`pre-hook`, `post_hook`, `on-run-*`).
fn in_hook(s: &Src, pos: usize) -> bool {
    let hook = rx!(r"(?i)hook|on-run");
    if !s.yaml {
        let from = crate::sqlutil::floor_char(&s.text, pos.saturating_sub(400));
        let seg = &s.text[from..pos];
        return seg.rfind("config(").is_some_and(|i| hook.is_match(&seg[i..]));
    }
    let lines: Vec<&str> = s.text.lines().collect();
    let line_no = s.text[..pos].matches('\n').count();
    let indent = |l: &str| l.len() - l.trim_start().len();
    let mut cur = indent(lines[line_no]);
    if hook.is_match(lines[line_no].split(':').next().unwrap_or("")) {
        return true;
    }
    for l in lines[..line_no].iter().rev() {
        if l.trim().is_empty() || l.trim_start().starts_with('#') {
            continue;
        }
        let i = indent(l);
        if i < cur {
            if hook.is_match(l.split(':').next().unwrap_or("")) {
                return true;
            }
            cur = i;
        }
    }
    false
}

fn snippet(text: &str, pos: usize, end: usize) -> String {
    crate::sqlutil::collapse_ws(&text[pos..end.min(text.len())]).chars().take(120).collect()
}

fn site(s: Suggestion, src: &Src, pos: usize, end: usize) -> Suggestion {
    s.file(src.file.clone()).span(span(&src.text, pos, end)).evidence(snippet(&src.text, pos, end))
}

fn vars_block(p: &ProjectContext) -> Map<String, Value> {
    match p.project_yml.get("vars") {
        Some(Value::Object(m)) => m.clone(),
        _ => Map::new(),
    }
}

fn package_names(p: &ProjectContext) -> BTreeSet<String> {
    let mut names = BTreeSet::new();
    for pk in packages_list(p).into_iter().filter_map(|x| x.as_object()) {
        for k in ["package", "git", "local"] {
            if let Some(v) = pk.get(k) {
                let last = py_str(v).trim_end_matches(".git").rsplit('/').next().unwrap_or("").to_string();
                names.insert(last.replace('-', "_"));
                names.insert(last);
            }
        }
    }
    names
}

fn is_scope_block(p: &ProjectContext, pkgs: &BTreeSet<String>, key: &str, v: &Value) -> bool {
    v.is_object() && (key == p.name || pkgs.contains(key))
}

/// Vars that apply to this project: top-level scalars plus its own scope block.
fn declared_vars(p: &ProjectContext) -> Vec<(String, Value, Vec<String>)> {
    let pkgs = package_names(p);
    let mut out: Vec<(String, Value, Vec<String>)> = vec![];
    for (k, v) in vars_block(p) {
        if is_scope_block(p, &pkgs, &k, &v) {
            if k == p.name {
                for (ik, iv) in v.as_object().unwrap() {
                    out.push((ik.clone(), iv.clone(), vec!["vars".into(), k.clone(), ik.clone()]));
                }
            }
        } else {
            out.push((k.clone(), v, vec!["vars".into(), k]));
        }
    }
    out
}

fn norm(v: &Value) -> String {
    match v {
        Value::Null => "null".into(),
        Value::String(s) => s.trim().to_string(),
        Value::Bool(b) => b.to_string(),
        other => other.to_string(),
    }
}

fn is_empty_value(v: &Value) -> bool {
    matches!(v, Value::Null) || matches!(v, Value::String(s) if s.trim().is_empty())
}

fn read_remediation_note() -> &'static str {
    "Declare the value under `vars:` or pass it with `--vars`."
}

fn prj0009(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    let call = rx!(r"\b(?:env_)?var\s*\(");
    for src in project_sources(p) {
        if src.yaml {
            for m in rx!(r"(?m)^[ \t]*(?:-[ \t]*)?\+?(database|schema|identifier|alias)[ \t]*:[ \t]*(.+)$").captures_iter(&src.text) {
                let (key, val) = (m.get(1).unwrap().as_str(), m.get(2).unwrap());
                if call.is_match(val.as_str()) {
                    let g = m.get(0).unwrap();
                    // PRJ0013 owns a self-named default in the same call; point at it.
                    let own_default = var_reads(val.as_str()).iter().any(|r| r.default.as_deref() == Some(r.key.as_str()));
                    out.push((own_default, site(
                        Suggestion::new("SSC-EWI-DBTPRJ0009", format!("`{key}` is read from a var, so the relation location depends on the run's vars."))
                            .ctx("location_key", json!(key)),
                        &src, g.start() + g.as_str().find(key).unwrap_or(0), g.end(),
                    )));
                }
            }
        }
    }
    // One finding per project for model configs: converters repeat the pattern in every model.
    let mut hits: Vec<(&crate::discovery::ModelFile, (u32, u32), String, String)> = vec![];
    for m in &p.models {
        for c in m.jinja.calls_named("config") {
            if shared::var_relation_reads(&m.raw).iter().any(|r| r.line == c.span.start_line) { continue; }
            for (k, v) in &c.kwargs {
                if ["database", "schema", "alias"].contains(&k.as_str()) && call.is_match(&lit_text(v)) {
                    hits.push((m, (c.span.start_line, c.span.start_col), k.clone(), lit_text(v)));
                }
            }
        }
    }
    if let Some((m, at, k, v)) = hits.first() {
        let files: Vec<&str> = hits.iter().map(|h| h.0.relative_path.as_str()).collect::<BTreeSet<_>>().into_iter().collect();
        out.push((false,
            Suggestion::new(
                "SSC-EWI-DBTPRJ0009",
                format!(
                    "{} `config()` location key(s) in {} model(s) are read from vars (first: `{k}={v}`), so the relation location depends on the run's vars.",
                    hits.len(),
                    files.len()
                ),
            )
            .file(m.relative_path.clone())
            .at(*at)
            .evidence(format!("{k}={v}"))
            .ctx("location_key", json!(k))
            .ctx("model", json!(m.name))
            .ctx("files", json!(files)),
        ));
    }
    out.into_iter()
        .map(|(own_default, s)| {
            let note = if own_default {
                " The same location call also uses its own name as the default; `SSC-EWI-DBTPRJ0013` owns that fix. Make both changes in one edit of this expression."
            } else {
                ""
            };
            s.remediation(format!("{}{note}", relations::LOCATION_FIX))
        })
        .collect()
}

fn prj0010(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for src in project_sources(p) {
        let mut seen = BTreeSet::new();
        for re in [
            rx!(r"(?s)\{%-?\s*(?:el)?if\b(?:[^%]|%[^}])*?\btarget\.name\b"),
            rx!(r"\bif\s+target\.name\b|\btarget\.name\s*(?:==|!=|\bin\b|\bnot\s+in\b)"),
        ] {
            for m in re.find_iter(&src.text) {
                let t = m.as_str();
                let rel = t.find("target.name").unwrap_or(0);
                let pos = m.start() + rel;
                if !seen.insert(line_col(&src.text, pos).0) {
                    continue;
                }
                out.push(site(
                    Suggestion::new("SSC-EWI-DBTPRJ0010", "The code branches on `target.name`, so it renders differently per target."),
                    &src, pos, pos + "target.name".len(),
                ));
            }
        }
    }
    out
}

fn prj0011(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for src in project_sources(p) {
        if src.yaml {
            for m in rx!(r"(?m)^[ \t]*[^#\n]*?\benv_var\s*\(.*$").find_iter(&src.text) {
                let pos = m.start() + m.as_str().find("env_var").unwrap_or(0);
                out.push(site(Suggestion::new("SSC-EWI-DBTPRJ0011", "A config value reads `env_var()`, so it depends on the process environment."), &src, pos, m.end()));
            }
        }
    }
    for m in &p.models {
        for c in m.jinja.calls_named("config") {
            for (k, v) in &c.kwargs {
                if lit_text(v).contains("env_var(") {
                    out.push(
                        Suggestion::new("SSC-EWI-DBTPRJ0011", format!("`config({k}=...)` reads `env_var()`, so it depends on the process environment."))
                            .file(m.relative_path.clone())
                            .at((c.span.start_line, c.span.start_col))
                            .evidence(format!("{k}={}", lit_text(v)))
                            .ctx("model", json!(m.name)),
                    );
                }
            }
        }
    }
    out
}

fn yaml_line(p: &ProjectContext, key: &str) -> Option<u32> {
    let re = regex::Regex::new(&format!(r#"(?m)^[ \t]+["']?({})["']?[ \t]*:"#, regex::escape(key))).ok()?;
    re.captures(&p.project_yml_text).map(|c| line_col(&p.project_yml_text, c.get(1).unwrap().start()).0)
}

fn prj0012(pf: &PortfolioContext) -> Vec<Suggestion> {
    let mut by_var: std::collections::BTreeMap<String, Vec<(usize, String)>> = Default::default();
    for (i, p) in pf.projects.iter().enumerate() {
        for (k, v, _) in declared_vars(p) {
            if !v.is_object() {
                by_var.entry(k).or_default().push((i, norm(&v)));
            }
        }
    }
    let mut out = vec![];
    for (name, uses) in by_var {
        let values: BTreeSet<&String> = uses.iter().map(|u| &u.1).collect();
        if uses.len() < 2 || values.len() < 2 {
            continue;
        }
        let first = &pf.projects[uses[0].0];
        let rel = |p: &ProjectContext| if p.relative_root == "." { "dbt_project.yml".to_string() } else { format!("{}/dbt_project.yml", p.relative_root) };
        let label = |i: usize| {
            let n = &pf.projects[i].name;
            if pf.projects.iter().filter(|q| &q.name == n).count() > 1 { pf.projects[i].relative_root.clone() } else { n.clone() }
        };
        let projects: Vec<String> = uses.iter().map(|u| label(u.0)).collect();
        let detail = uses.iter().map(|u| format!("{}={}", label(u.0), u.1)).collect::<Vec<_>>().join(", ");
        let mut s = Suggestion::new(
            "SSC-EWI-DBTPRJ0012",
            format!("Var `{name}` has {} different defaults across {}: {detail}.", values.len(), plural(projects.len(), "project")),
        )
        .project(first.label.clone())
        .file(rel(first))
        .evidence(detail.clone())
        .ctx("var_name", json!(name))
        .ctx("projects", json!(projects))
        .ctx("values", Value::Object(uses.iter().map(|u| (label(u.0), json!(u.1))).collect()));
        if let Some(l) = yaml_line(first, &name) {
            s = s.line(l);
        }
        out.push(s);
    }
    out
}

fn prj0013(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for src in project_sources(p) {
        for r in var_reads(&src.text) {
            if r.default.as_deref() == Some(r.key.as_str()) && !in_hook(&src, r.pos) {
                out.push(site(
                    Suggestion::new("SSC-EWI-DBTPRJ0013", format!("`var('{0}', '{0}')` uses its own name as the default, so an unset var yields the text `{0}`.", r.key))
                        .ctx("var_name", json!(r.key)),
                    &src, r.pos, r.end,
                ));
            }
        }
    }
    out
}

fn value_var_reads(src: &Src) -> Vec<VarRead> {
    let mut locations: Vec<(usize, usize)> = if src.yaml { vec![] } else {
        shared::var_relation_reads(&src.text).into_iter().map(|read| (read.start, read.end)).collect()
    };
    if !src.yaml {
        for (start, end) in shared::config_ranges(&src.text) {
            let open = start + src.text[start..end].find('(').unwrap() + 1;
            let mut offset = open;
            for argument in crate::sqlutil::split_top_level(&src.text[open..end - 1], ',') {
                let Some(relative) = src.text[offset..end].find(&argument) else { continue; };
                let begin = offset + relative;
                offset = begin + argument.len();
                if argument.split_once('=').is_some_and(|(key, _)| ["database", "schema", "alias"].contains(&key.trim())) {
                    locations.push((begin, offset));
                }
            }
        }
    }
    let regions = if src.yaml { vec![] } else { crate::sqlutil::sql_regions(&src.text) };
    var_reads(&src.text).into_iter().filter(|read| {
        if locations.iter().any(|&(start, end)| start <= read.pos && read.pos < end) { return false; }
        if src.yaml {
            let before = &src.text[..read.pos];
            let line = before.rsplit('\n').next().unwrap_or("");
            if line.trim_start().starts_with('#') { return false; }
            let mut indentation = usize::MAX;
            for line in before.lines().rev() {
                if line.trim().is_empty() || line.trim_start().starts_with('#') { continue; }
                let indent = line.len() - line.trim_start().len();
                if indent >= indentation { continue; }
                indentation = indent;
                if let Some((key, _)) = line.trim_start().trim_start_matches("- ").split_once(':') {
                    return !["database", "schema", "identifier", "alias"].contains(&key.trim().trim_start_matches('+'));
                }
            }
            true
        } else {
            !matches!(crate::sqlutil::region_at(&regions, read.pos), Some(crate::sqlutil::Region::Comment | crate::sqlutil::Region::JinjaComment))
        }
    }).collect()
}

fn prj0014(p: &ProjectContext) -> Vec<Suggestion> {
    let sources: Vec<Src> = project_sources(p);
    let mut hits = vec![];
    for (k, v, keys) in declared_vars(p) {
        if !is_empty_value(&v) {
            continue;
        }
        let Some((src, r)) = sources
            .iter()
            .filter(|s| s.file != "dbt_project.yml")
            .find_map(|s| value_var_reads(s).into_iter().find(|r| r.key == k).map(|r| (s, r)))
        else {
            continue;
        };
        let marker = sources.iter().any(|s| s.text.contains("SSC-FDM-DS0006") && s.text.contains(&format!("'{k}'")));
        let at = format!("{}:{}", src.file, line_col(&src.text, r.pos).0);
        hits.push((k, v.is_null(), at, marker, keys));
    }
    // One finding per project: the fix is one edit of the `vars:` block.
    if hits.is_empty() {
        return vec![];
    }
    let names: Vec<&str> = hits.iter().map(|h| h.0.as_str()).collect();
    let marker = hits.iter().any(|h| h.3);
    let note = if marker { " An `SSC-FDM-DS0006` marker confirms the converter left some of them empty." } else { "" };
    let evidence: Vec<String> = hits
        .iter()
        .map(|(k, null, at, _, keys)| {
            let decl = project_yml_position(p, keys).map_or(String::new(), |(l, _)| format!(" (dbt_project.yml:{l})"));
            format!("{k}: {}{decl} read at {at}", if *null { "null" } else { "''" })
        })
        .collect();
    vec![Suggestion::new(
        "SSC-EWI-DBTPRJ0014",
        format!("{} var(s) are declared empty under `vars:` but remaining value reads require them: {}.{note}", hits.len(), names.join(", ")),
    )
    .file("dbt_project.yml")
    .evidence(evidence.join("; "))
    .remediation("Set a real value for the listed remaining value reads under `vars:` or through the existing runtime value-input contract. Do not delete these declarations while those value reads remain. PRJ0009/PRJ0021/PRJ0022 own location uses of the same keys: replace those uses with target-driven locations, not runtime location overrides; no orchestration-call change is needed.")
    .ctx("scope", json!("value_reads"))
    .ctx("vars", json!(names))
    .ctx("reads", json!(hits.iter().map(|h| json!({"var": h.0, "read_at": h.2, "fdm_marker": h.3})).collect::<Vec<_>>()))
    .ctx("fdm_marker", json!(marker))
    .ctx("yaml_keys", json!(["vars"]))]
}

const SESSION_VARS: &[&str] = &[
    "SESSSTARTTIME", "WORKFLOWSTARTTIME", "SESSIONSTARTTIME", "SYSDATE", "SYSTIMESTAMP", "PMSESSIONNAME",
    "PMWORKFLOWNAME", "PMFOLDERNAME", "PMMAPPINGNAME", "PMREPOSITORYSERVICENAME", "PMINTEGRATIONSERVICENAME",
    "PMREPOSITORYUSERNAME", "PMWORKFLOWRUNID", "PMSESSIONRUNID", "PMWORKFLOWRUNINSTANCENAME",
];

fn prj0015(p: &ProjectContext) -> Vec<Suggestion> {
    let read = read_vars(p);
    let mut out = vec![];
    for (k, v, keys) in declared_vars(p) {
        let placeholder = is_empty_value(&v) || matches!(&v, Value::String(s) if s.starts_with("1753-01-01"));
        if !placeholder || !SESSION_VARS.contains(&k.to_uppercase().as_str()) {
            continue;
        }
        // An unread var is PRJ0017's finding; its value does not matter here.
        if read.as_ref().is_some_and(|r| !r.contains(&k)) {
            continue;
        }
        out.push(
            Suggestion::new("SSC-EWI-DBTPRJ0015", format!("Informatica session var `{k}` is declared with the placeholder `{}`.", norm(&v)))
                .file("dbt_project.yml")
                .evidence(format!("{k}: {}", norm(&v)))
                .ctx("var_name", json!(k))
                .ctx("yaml_keys", json!(keys)),
        );
    }
    out
}

fn prj0016(p: &ProjectContext) -> Vec<Suggestion> {
    let declared: BTreeSet<String> = declared_vars(p).into_iter().map(|d| d.0).collect();
    let mut out = vec![];
    for src in project_sources(p) {
        let reads = var_reads(&src.text);
        let relations = if src.yaml { vec![] } else { shared::var_relation_reads(&src.text) };
        for r in &reads {
            let mut guards = vec![];
            for tag in rx!(r"\{%-?\s*(if|elif|else|endif)\b(.*?)\s*-?%\}").captures_iter(&src.text[..r.pos]) {
                let positive = tag[2].contains("!= ''") && var_reads(&tag[2]).iter().any(|v| v.key == r.key && v.has_default);
                match &tag[1] {
                    "if" => guards.push(positive),
                    "elif" | "else" => { if let Some(last) = guards.last_mut() { *last = tag[1] == *"elif" && positive; } }
                    "endif" => { guards.pop(); }
                    _ => {}
                }
            }
            // A default elsewhere is not evidence that this read is guarded.
            if declared.contains(&r.key) || r.has_default || guards.contains(&true) || relations.iter().any(|rel| rel.start <= r.pos && r.pos < rel.end) {
                continue;
            }
            out.push(site(
                Suggestion::new(
                    "SSC-EWI-DBTPRJ0016",
                    format!("Var `{}` is read here with no default or detected project declaration. Check parent/package inputs, `--vars`, and version-supported vars.yml before concluding that dbt has no value. {}", r.key, read_remediation_note()),
                )
                .ctx("var_name", json!(r.key)),
                &src, r.pos, r.end,
            ));
        }
    }
    out
}

/// Every var key the project reads, or `None` when a dynamic `var(x)` hides some reads.
fn read_vars(p: &ProjectContext) -> Option<BTreeSet<String>> {
    let sources = project_sources(p);
    if sources.iter().any(|s| has_dynamic_var(&s.text)) {
        return None;
    }
    let mut read: BTreeSet<String> = sources.iter().flat_map(|s| var_reads(&s.text)).map(|r| r.key).collect();
    read.extend(var_reads(&p.project_yml_text).into_iter().map(|r| r.key));
    Some(read)
}

fn prj0017(p: &ProjectContext) -> Vec<Suggestion> {
    let Some(read) = read_vars(p) else { return vec![] };
    // An installed package reads its own vars, for example `dbt_artifacts_schema`.
    let pkgs = package_names(p);
    let pkg_var = |k: &str| pkgs.iter().any(|n| !n.is_empty() && k.starts_with(&format!("{n}_")));
    let unread: Vec<(String, Vec<String>)> = declared_vars(p)
        .into_iter()
        .filter(|(k, _, _)| !read.contains(k) && !pkg_var(k))
        .map(|(k, _, keys)| (k, keys))
        .collect();
    if unread.is_empty() {
        return vec![];
    }
    // One finding per project: the fix is one edit of the `vars:` block.
    // Converter-emitted Informatica built-ins form a named group; a person may keep them on purpose.
    let (session, other): (Vec<&(String, Vec<String>)>, Vec<_>) =
        unread.iter().partition(|(k, _)| SESSION_VARS.contains(&k.to_uppercase().as_str()));
    let names = |v: &[&(String, Vec<String>)]| v.iter().map(|(k, _)| k.clone()).collect::<Vec<String>>();
    let mut msg = format!("{} var(s) under `vars:` have no detected literal-key reads in this project", unread.len());
    if !other.is_empty() {
        msg += &format!(": {}", names(&other).join(", "));
    }
    if !session.is_empty() {
        msg += &format!(
            "{}Informatica session built-ins (the converter emits these on purpose): {}",
            if other.is_empty() { ": " } else { ". " },
            names(&session).join(", ")
        );
    }
    msg.push('.');
    let evidence: Vec<String> = unread
        .iter()
        .map(|(k, keys)| project_yml_position(p, keys).map_or(k.clone(), |(l, _)| format!("{k} (dbt_project.yml:{l})")))
        .collect();
    vec![Suggestion::new("SSC-EWI-DBTPRJ0017", msg)
        .file("dbt_project.yml")
        .evidence(format!("vars: {}", evidence.join(", ")))
        .ctx("vars", json!(names(&other)))
        .ctx("session_vars", json!(names(&session)))
        .ctx("yaml_keys", json!(["vars"]))]
}

fn prj0018(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    let pkgs = package_names(p);
    let top: Vec<(String, Value)> = vars_block(p).into_iter().filter(|(k, v)| !is_scope_block(p, &pkgs, k, v)).collect();
    for (scope, block) in vars_block(p).iter().filter(|(k, v)| is_scope_block(p, &pkgs, k, v)) {
        for (k, v) in block.as_object().unwrap() {
            if let Some((_, tv)) = top.iter().find(|(tk, _)| tk == k)
                && norm(tv) != norm(v) {
                    out.push(
                        Suggestion::new("SSC-EWI-DBTPRJ0018", format!("Var `{k}` is declared as `{}` at top level and `{}` under `{scope}`.", norm(tv), norm(v)))
                            .file("dbt_project.yml")
                            .evidence(format!("{k}: {} / {scope}.{k}: {}", norm(tv), norm(v)))
                            .ctx("var_name", json!(k))
                            .ctx("scope", json!(scope))
                            .ctx("yaml_keys", json!(["vars", scope, k])),
                    );
                }
        }
    }
    // Duplicate keys inside `vars:` are lost by the YAML parser, so read the text.
    let lines: Vec<&str> = p.project_yml_text.lines().collect();
    if let Some(start) = lines.iter().position(|l| l.trim_end() == "vars:") {
        let mut seen: std::collections::BTreeMap<String, String> = Default::default();
        let mut indent = None;
        for (i, l) in lines.iter().enumerate().skip(start + 1) {
            if l.trim().is_empty() || l.trim_start().starts_with('#') {
                continue;
            }
            let ind = l.len() - l.trim_start().len();
            if ind == 0 {
                break;
            }
            if *indent.get_or_insert(ind) != ind {
                continue;
            }
            let Some((k, v)) = l.trim().split_once(':') else { continue };
            let k = k.trim().trim_matches(|c| c == '"' || c == '\'').to_string();
            let v = v.trim().trim_matches(|c| c == '"' || c == '\'').to_string();
            match seen.get(&k) {
                Some(old) if *old != v => out.push(
                    Suggestion::new("SSC-EWI-DBTPRJ0018", format!("Var `{k}` is declared twice under `vars:` with values `{old}` and `{v}`; the YAML parser keeps one."))
                        .file("dbt_project.yml")
                        .line((i + 1) as u32)
                        .evidence(format!("{k}: {old} / {v}"))
                        .ctx("var_name", json!(k)),
                ),
                Some(_) => {}
                None => {
                    seen.insert(k, v);
                }
            }
        }
    }
    out
}

// ---- Merge-collision rules (PRJ0019-PRJ0021) ----

/// Union-find over `0..n`, for grouping findings into one defect each.
struct Dsu(Vec<usize>);

impl Dsu {
    fn new(n: usize) -> Self {
        Dsu((0..n).collect())
    }

    fn find(&mut self, i: usize) -> usize {
        let mut r = i;
        while self.0[r] != r {
            r = self.0[r];
        }
        self.0[i] = r;
        r
    }

    fn union(&mut self, a: usize, b: usize) {
        let (ra, rb) = (self.find(a), self.find(b));
        if ra != rb {
            self.0[ra.max(rb)] = ra.min(rb);
        }
    }

    /// The groups of two or more members, each in index order.
    fn groups(&mut self) -> Vec<Vec<usize>> {
        let mut g: BTreeMap<usize, Vec<usize>> = BTreeMap::new();
        for i in 0..self.0.len() {
            let r = self.find(i);
            g.entry(r).or_default().push(i);
        }
        g.into_values().filter(|v| v.len() > 1).collect()
    }
}

/// The location advice for a kept or renamed source block, under the
/// location policy: `database:` a literal or a `target.name` if/elif block,
/// `schema:` a literal, no vars. Empty when the entry already sets both as
/// literals. Starts with a space.
fn source_location_fix(p: &ProjectContext, d: &crate::discovery::SourceDecl, block: &str, loc: &shared::Location) -> String {
    let raws = [d.database.as_deref(), d.schema.as_deref()];
    let mut vars: Vec<String> = vec![];
    for r in raws.iter().flatten() {
        for v in var_reads(r) {
            if !vars.contains(&v.key) {
                vars.push(v.key);
            }
        }
    }
    let literal = |r: Option<&str>| r.is_some_and(|r| !r.contains("{{") && !r.contains("{%"));
    let (db, schema) = (loc.database.known(), loc.schema.known());
    if vars.is_empty() && db.is_some() && schema.is_some() && literal(raws[0]) && literal(raws[1]) {
        return String::new();
    }
    let (targets, from_profile) = shared::target_values(p, db);
    let block = if schema.is_some() { block.to_string() } else { "<schema in lower case>".to_string() };
    let yaml = shared::render_source_location(&block, schema.unwrap_or("<schema>"), &targets, [loc.database.quoted, loc.schema.quoted, d.quoting[2].unwrap_or(false)]);
    let mut t = format!(
        " Set the block's location with literals, not vars: `database:` a literal for one environment, or a `target.name` if/elif block whose `else` is `invalid_database` so an unknown target fails; `schema:` a literal:\n\n```yaml\n{yaml}```\n\n"
    );
    if !from_profile {
        t.push_str("The targets `dev`, `qa` and `prod` are examples: use the project's real target names. ");
    }
    if db.is_none() || schema.is_none() {
        t.push_str("The current values are placeholders, empty or unset, so get the real database and schema for each target from the owner or the original connection; do not guess. ");
    } else if targets.iter().any(|(_, v)| v.starts_with('<')) {
        t.push_str("Fill in each target's database from the owner; do not guess. ");
    }
    if !vars.is_empty() {
        let list = vars.iter().map(|v| format!("`{v}`")).collect::<Vec<_>>().join(", ");
        let (them, has) = if vars.len() == 1 { ("that var", "that key no longer has") } else { ("those vars", "those keys no longer have") };
        t.push_str(&format!(
            "This removes the var{} {list} from the location. If orchestration passes {them} through `--vars`, {has} any effect, so check that the target the orchestration already runs with maps to the right database above; the orchestration call does not change.",
            if vars.len() == 1 { "" } else { "s" }
        ));
    }
    t.trim_end().to_string()
}

/// One `sources:` entry of the estate, for PRJ0019.
struct EstateSource {
    pi: usize,
    d: crate::discovery::SourceDecl,
    /// Root-relative path of the YAML file.
    path: String,
    /// Root-relative `path:line` of the entry's `name:`.
    site: String,
    /// The block's database and schema.
    loc: shared::Location,
    /// Each table's resolved location, in `d.tables` order.
    tables: Vec<shared::Location>,
    /// The `source()` calls in its project that read one of its tables.
    reads: Vec<shared::CallRef>,
}

/// How PRJ0019 describes a group.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SrcCase {
    /// One source name declared in two or more entries.
    SameName,
    /// The same (source, table) declared twice in one project.
    DuplicateTable,
    /// Different source names whose tables resolve to one relation.
    Alias,
}

fn prj0019(pf: &PortfolioContext) -> Vec<Suggestion> {
    use shared::{call_sites, compare_locations, decl_site, model_relation, producers, project_locations, resolve_location, resolve_source_location, source_block_for, var_relation_reads, CallKind, LocationMatch, Part, LOCATION_CHECK};
    let calls: Vec<Vec<shared::CallRef>> = pf.projects.iter().map(call_sites).collect();
    let mut srcs: Vec<EstateSource> = vec![];
    for (pi, p) in pf.projects.iter().enumerate() {
        for d in crate::discovery::source_decls(p) {
            if d.name.is_empty() {
                continue;
            }
            let reads = calls[pi]
                .iter()
                .filter(|c| c.kind == CallKind::Source && c.name.eq_ignore_ascii_case(&d.name) && c.table.as_ref().is_some_and(|t| d.tables.iter().any(|x| x.name.eq_ignore_ascii_case(t))))
                .cloned()
                .collect();
            let tables = d.tables.iter().map(|t| resolve_location(p, &d, t)).collect();
            srcs.push(EstateSource { pi, path: crate::discovery::root_relative(p, &d.file), site: decl_site(p, &d), loc: resolve_source_location(p, &d), tables, reads, d });
        }
    }
    srcs.sort_by(|a, b| (&a.path, a.d.line).cmp(&(&b.path, b.d.line)));
    let mut dsu = Dsu::new(srcs.len());
    // (a) and (b): one source name in two or more entries.
    let mut by_name: BTreeMap<String, Vec<usize>> = BTreeMap::new();
    for (i, s) in srcs.iter().enumerate() {
        by_name.entry(s.d.name.to_lowercase()).or_default().push(i);
    }
    for v in by_name.values() {
        for &b in &v[1..] {
            dsu.union(v[0], b);
        }
    }
    // (c): tables of different source names that resolve to one relation.
    // Each pair is ((entry, table), (entry, table)).
    let mut by_ident: BTreeMap<String, Vec<(usize, usize)>> = BTreeMap::new();
    for (i, s) in srcs.iter().enumerate() {
        for (ti, l) in s.tables.iter().enumerate() {
            if let Some(k) = l.identifier.key() {
                by_ident.entry(k).or_default().push((i, ti));
            }
        }
    }
    let mut aliases: Vec<((usize, usize), (usize, usize))> = vec![];
    for v in by_ident.values() {
        for (k, &a) in v.iter().enumerate() {
            for &b in &v[k + 1..] {
                if srcs[a.0].d.name.eq_ignore_ascii_case(&srcs[b.0].d.name) {
                    continue;
                }
                let m = compare_locations(&[&srcs[a.0].tables[a.1], &srcs[b.0].tables[b.1]], srcs[a.0].pi == srcs[b.0].pi);
                if matches!(m, LocationMatch::Equal | LocationMatch::IdenticalPlaceholder) {
                    dsu.union(a.0, b.0);
                    aliases.push((a, b));
                }
            }
        }
    }
    let written = producers(pf);
    // Find the model that may write table `ti` in entry `e`. Return the match
    // strength: Equal, IdenticalPlaceholder, or Unresolved. Unresolved means
    // the identifier matches but the database or schema cannot be compared.
    // Exclude models whose locations differ.
    let writer = |e: usize, ti: usize| -> Option<(String, LocationMatch)> {
        let mut best: Option<(u8, String, LocationMatch)> = None;
        for &(pi, mi) in written.get(&srcs[e].tables[ti].identifier.key()?)? {
            let p = &pf.projects[pi];
            let Some(rel) = model_relation(p, &p.models[mi]) else { continue };
            let m = compare_locations(&[&srcs[e].tables[ti], &rel.physical], pi == srcs[e].pi);
            let rank = match &m {
                LocationMatch::Equal => 0,
                LocationMatch::IdenticalPlaceholder => 1,
                LocationMatch::Unresolved(_) => 2,
                LocationMatch::Different(_) => continue,
            };
            if best.as_ref().is_none_or(|b| rank < b.0) {
                best = Some((rank, crate::discovery::root_relative(p, &p.models[mi].relative_path), m));
            }
        }
        best.map(|(_, path, m)| (path, m))
    };
    let tname = |e: usize, t: usize| format!("`{}.{}`", srcs[e].d.name, srcs[e].d.tables[t].name);
    let estate_names: BTreeSet<String> = srcs.iter().map(|s| s.d.name.to_lowercase()).collect();

    // Fold the entries of `cl` (one location) into one block named `final`
    // (or the kept entry's name), skipping calls at `ambiguous` sites.
    // Returns (kept entry, final name, text).
    let fold = |cl: &[usize], final_name: Option<&str>, ambiguous: &BTreeSet<String>| -> (usize, String, String) {
        let kept = cl.iter().copied().enumerate().max_by_key(|&(pos, i)| (srcs[i].reads.len(), std::cmp::Reverse(pos))).unwrap().1;
        let k = &srcs[kept];
        let fin = final_name.unwrap_or(&k.d.name).to_string();
        let mut have: BTreeSet<String> = k.d.tables.iter().map(|t| t.name.to_lowercase()).collect();
        let mut table_map: BTreeMap<(usize, String), String> = BTreeMap::new();
        let mut steps: Vec<String> = vec![];
        let mut quote_overrides: Vec<String> = vec![];
        let mut in_both: Vec<String> = vec![];
        // Tables that are a model's relation: (table, producer, as generated).
        let mut dropped: Vec<(String, String, bool)> = vec![];
        // Tables with a producer's name whose location can't be compared.
        let mut check: Vec<(String, String, String)> = vec![];
        // A table that a source() call reads stays, or the call would break.
        let read = |e: usize, t: &str| {
            srcs[e].reads.iter().any(|c| c.table.as_ref().is_some_and(|x| x.eq_ignore_ascii_case(t)))
                || srcs[e].d.tables.iter().enumerate().filter(|(_,table)| table.name.eq_ignore_ascii_case(t)).any(|(ti,_)| {
                    aliases.iter().any(|&(a,b)| {
                        let other = if a == (e,ti) { Some(b) } else if b == (e,ti) { Some(a) } else { None };
                        other.is_some_and(|(entry,table)| srcs[entry].reads.iter().any(|c| c.table.as_ref().is_some_and(|name| name.eq_ignore_ascii_case(&srcs[entry].d.tables[table].name))))
                    })
                })
        };
        let mut classify = |e: usize, ti: usize| -> bool {
            let t = &srcs[e].d.tables[ti].name;
            match writer(e, ti) {
                Some((path, m @ (LocationMatch::Equal | LocationMatch::IdenticalPlaceholder))) if !read(e, t) => {
                    dropped.push((format!("`{t}`"), path, m == LocationMatch::IdenticalPlaceholder));
                    true
                }
                Some((path, LocationMatch::Unresolved(why))) => {
                    check.push((format!("`{t}`"), path, why));
                    false
                }
                _ => false,
            }
        };
        for ti in 0..k.d.tables.len() {
            classify(kept, ti);
        }
        for &o in cl.iter().filter(|&&o| o != kept) {
            let mut moved: Vec<String> = vec![];
            for (ti, t) in srcs[o].d.tables.iter().enumerate() {
                let lower = t.name.to_lowercase();
                let alias = aliases.iter().find_map(|&(a, b)| {
                    if a == (o, ti) && b.0 == kept {
                        Some(b.1)
                    } else if b == (o, ti) && a.0 == kept {
                        Some(a.1)
                    } else {
                        None
                    }
                });
                if let Some(kt) = alias {
                    table_map.insert((o, lower), k.d.tables[kt].name.clone());
                    continue;
                }
                if let Some(kt) = k.d.tables.iter().find(|x| x.name.eq_ignore_ascii_case(&t.name)) {
                    in_both.push(format!("`{}`", kt.name));
                    table_map.insert((o, lower), kt.name.clone());
                    continue;
                }
                if !have.insert(lower.clone()) {
                    continue;
                }
                if classify(o, ti) {
                    have.remove(&lower);
                    continue;
                }
                moved.push(format!("`{}`", t.name));
                let quoted = srcs[o].d.quoting[2].unwrap_or(false);
                if t.quote_identifier.is_none() && quoted != k.d.quoting[2].unwrap_or(false) {
                    quote_overrides.push(format!("  - name: {}\n    quoting:\n      identifier: {quoted}\n", shared::yaml_scalar(&t.name)));
                }
            }
            steps.push(if moved.is_empty() {
                format!("delete the `{}` entry at {}", srcs[o].d.name, srcs[o].site)
            } else {
                format!("move {} from {} into it, then delete that entry", moved.join(", "), srcs[o].site)
            });
        }
        let rename = if fin != k.d.name { format!(" and rename it to `{fin}`") } else { String::new() };
        let mut t = format!("Keep the `{}` entry at {} as the single declaration{rename}.", k.d.name, k.site);
        if k.d.tables.iter().enumerate().any(|(i, table)| k.d.tables[..i].iter().any(|other| other.name.eq_ignore_ascii_case(&table.name))) {
            t.push_str(" Within the kept block, remove each redundant repeated table entry, retaining the first definition and merging compatible tests/descriptions; do not delete the source block.");
        }
        if !steps.is_empty() {
            t.push_str(&format!(" For the others: {}.", steps.join("; ")));
            t.push_str(" Preserve the kept block's identifier quoting and every table's explicit quoting override.");
        }
        if !quote_overrides.is_empty() {
            t.push_str(&format!(" Before moving these tables, add these explicit identifier-quoting overrides to their existing definitions under `{fin}` so the kept block's different default does not change their physical identity. Retain their identifiers and all other table properties; this fragment is not a replacement table list:\n\n```yaml\ntables:\n{}```\n\n", quote_overrides.join("")));
        }
        in_both.sort();
        in_both.dedup();
        if !in_both.is_empty() {
            t.push_str(&format!(
                " {} {} declared in more than one entry: keep the kept entry's definition and carry over any `identifier`, description, tests or freshness the deleted one has.",
                in_both.join(", "),
                if in_both.len() == 1 { "is" } else { "are" }
            ));
        }
        if !dropped.is_empty() {
            let list: Vec<String> = dropped.iter().map(|(t, p, _)| format!("{t} (written by {p})")).collect();
            let (them, each) = if dropped.len() == 1 { ("it", "it is the relation that model writes") } else { ("them", "each is the relation its model writes") };
            t.push_str(&format!(
                " Remove {} from the sources rather than keeping or moving {them}, because {each}. The PRJ0021 or PRJ0022 finding on each reader gives the producer's path and says how to read it instead of a source entry.",
                list.join(", ")
            ));
            let generated: Vec<&str> = dropped.iter().filter(|d| d.2).map(|d| d.0.as_str()).collect();
            if !generated.is_empty() {
                t.push_str(&format!(
                    " {} {} that relation only as generated (the same placeholder database and schema): confirm once the real locations are set, and keep any that turn out to be a different table.",
                    generated.join(", "),
                    if generated.len() == 1 { "matches" } else { "match" }
                ));
            }
        }
        if !check.is_empty() {
            let list: Vec<String> = check.iter().map(|(t, p, why)| format!("{t} and {p} ({why})")).collect();
            t.push_str(&format!(
                " These tables have the name of a table a model writes, but they can't be shown to be one relation: {}. Check the database and schema of each first; if it is the model's relation, remove it from the sources and read it as the PRJ0021 or PRJ0022 finding on each reader says, otherwise keep it as above.",
                list.join("; ")
            ));
        }
        // source() calls that change.
        let mut changes: BTreeMap<(String, String), BTreeSet<String>> = BTreeMap::new();
        let mut any_read = false;
        for &o in cl {
            for c in &srcs[o].reads {
                any_read = true;
                if ambiguous.contains(&c.site) {
                    continue;
                }
                let tb = c.table.clone().unwrap_or_default();
                let new_t = if o == kept { tb.clone() } else { table_map.get(&(o, tb.to_lowercase())).cloned().unwrap_or_else(|| tb.clone()) };
                if c.name != fin || new_t != tb {
                    changes.entry((format!("`source('{}', '{tb}')`", c.name), format!("`source('{fin}', '{new_t}')`"))).or_default().insert(c.site.clone());
                }
            }
        }
        if !changes.is_empty() {
            let list: Vec<String> = changes.into_iter().map(|((a, b), s)| format!("{a} to {b} at {}", s.into_iter().collect::<Vec<_>>().join(", "))).collect();
            t.push_str(&format!(" Change these `source()` calls: {}.", list.join("; ")));
        } else if any_read {
            t.push_str(&format!(" No `source()` call changes: every call already reads `{fin}`."));
        } else {
            t.push_str(" No model calls `source()` on these entries, so no call changes.");
        }
        (kept, fin, t)
    };

    let mut out = vec![];
    let mut groups = dsu.groups();
    for (i, src) in srcs.iter().enumerate() {
        let mut names = BTreeSet::new();
        if src.d.tables.iter().any(|t| !names.insert(t.name.to_lowercase())) && !groups.iter().any(|g| g.contains(&i)) {
            groups.push(vec![i]);
        }
    }
    for g in groups {
        let mut conflicts = vec![];
        let tables: Vec<_> = g.iter().flat_map(|&i| srcs[i].d.tables.iter().enumerate().map(move |(ti,t)| (i,ti,t))).collect();
        for (pos, &(i, ti, table)) in tables.iter().enumerate() {
            for &(j, tj, other) in &tables[pos + 1..] {
                if table.name.eq_ignore_ascii_case(&other.name) && matches!(compare_locations(&[&srcs[i].loc, &srcs[j].loc], srcs[i].pi == srcs[j].pi), LocationMatch::Equal | LocationMatch::IdenticalPlaceholder) && !matches!(compare_locations(&[&srcs[i].tables[ti], &srcs[j].tables[tj]], srcs[i].pi == srcs[j].pi), LocationMatch::Equal | LocationMatch::IdenticalPlaceholder) {
                    conflicts.push(format!("`{}` at {}:{} and {}:{}", table.name, srcs[i].path,table.line,srcs[j].path,other.line));
                }
            }
        }
        if !conflicts.is_empty() {
            let anchor = &srcs[g[0]];
            out.push(Suggestion::new("SSC-EWI-DBTPRJ0019",format!("Source table names have differing or unresolved physical identifiers/locations: {}. Equal source-block locations do not prove table identity.",conflicts.join("; ")))
                .in_project(&pf.projects[anchor.pi]).file(&anchor.d.file).line(anchor.d.line)
                .ctx("class",json!("unresolved")).ctx("source",json!(anchor.d.name))
                .remediation(format!("Do not delete or coalesce these table definitions: {}. Retain every distinct physical relation under a collision-free logical table name in the appropriate database.schema block; preserve each identifier. Map each project's source calls to its own declaration. Reads requiring owner confirmation: {}. If multiple declarations in that project claim a call, ask the owner which physical relation it means before redirecting it. {LOCATION_CHECK} {}",conflicts.join("; "),g.iter().flat_map(|&i| srcs[i].reads.iter().map(|c| c.site.clone())).collect::<BTreeSet<_>>().into_iter().collect::<Vec<_>>().join(", "),relations::LOCATION_FIX)));
            continue;
        }
        let projects: BTreeSet<usize> = g.iter().map(|&i| srcs[i].pi).collect();
        let mut names: Vec<String> = vec![];
        for &i in &g {
            if !names.iter().any(|n| n.eq_ignore_ascii_case(&srcs[i].d.name)) {
                names.push(srcs[i].d.name.clone());
            }
        }
        let sites: Vec<String> = g.iter().map(|&i| srcs[i].site.clone()).collect();
        // (b) the same (source, table) twice in one project.
        let mut tsites: BTreeMap<(usize, String, String), (String, Vec<String>)> = BTreeMap::new();
        for &i in &g {
            for t in &srcs[i].d.tables {
                let e = tsites.entry((srcs[i].pi, srcs[i].d.name.to_lowercase(), t.name.to_lowercase())).or_insert_with(|| (format!("`{}.{}`", srcs[i].d.name, t.name), vec![]));
                e.1.push(format!("{}:{}", srcs[i].path, t.line));
            }
        }
        let dup_tables: Vec<String> = tsites.into_values().filter(|(_, v)| v.len() > 1).map(|(n, v)| format!("{n} ({})", v.join(", "))).collect();
        let pairs: Vec<String> = aliases.iter().filter(|(a, _)| g.contains(&a.0)).map(|&(a, b)| format!("{} and {}", tname(a.0, a.1), tname(b.0, b.1))).collect();
        let case = if !dup_tables.is_empty() {
            SrcCase::DuplicateTable
        } else if names.len() > 1 {
            SrcCase::Alias
        } else {
            SrcCase::SameName
        };
        let locs: Vec<&shared::Location> = g.iter().map(|&i| &srcs[i].loc).collect();
        let same_project = projects.len() == 1;
        let overall = compare_locations(&locs, same_project);

        let subject = if names.len() == 1 { format!("Source `{}` is", names[0]) } else { format!("Sources {} are", names.iter().map(|n| format!("`{n}`")).collect::<Vec<_>>().join(", ")) };
        let mut msg = format!("{subject} declared in {} entries: {}.", g.len(), sites.join(", "));
        let cross_name = by_name.values().any(|v| {
            let ps: BTreeSet<usize> = v.iter().filter(|i| g.contains(i)).map(|&i| srcs[i].pi).collect();
            ps.len() > 1
        });
        if cross_name {
            msg.push_str(" They are in different projects, so the names collide once the projects are merged.");
        } else if case == SrcCase::SameName {
            msg.push_str(" dbt accepts a source split across entries while no table repeats, but each database.schema should have one block.");
        }
        if !dup_tables.is_empty() {
            msg.push_str(&format!(
                " The same table is declared twice in one project: {}. dbt Fusion warns and keeps the first definition; dbt Core rejects the project with a duplicate source error (checked in the v1.10.0 source).",
                dup_tables.join(", ")
            ));
        }
        if !pairs.is_empty() {
            msg.push_str(&format!(" These tables resolve to one relation under different source names: {}.", pairs.join(", ")));
        }
        let shown = |p: &shared::LocPart| match &p.value {
            Part::Known(s) | Part::Placeholder(s) => format!("`{s}`"),
            Part::Target => "the target".to_string(),
            Part::Unknown(_) => "unknown".to_string(),
        };
        let first = &srcs[g[0]].loc;
        msg.push_str(&match &overall {
            LocationMatch::Equal => format!(" They resolve to one location, {}.{}.", shown(&first.database), shown(&first.schema)),
            LocationMatch::IdenticalPlaceholder => format!(
                " Every entry carries the same generated placeholders ({}.{}), so they match only as generated.",
                shown(&first.database),
                shown(&first.schema)
            ),
            LocationMatch::Different(why) => format!(" They point at different locations: {why}."),
            LocationMatch::Unresolved(why) => format!(" Whether they point at one location can't be resolved: {why}."),
        });

        let mut locations: BTreeSet<(String, String)> = BTreeSet::new();
        for &pi in &projects {
            locations.extend(project_locations(&pf.projects[pi]));
        }
        let block_name = |e: usize| -> Option<String> {
            let l = &srcs[e].loc;
            Some(source_block_for(l.database.known()?, l.schema.known()?, &locations))
        };
        let mut occupied = vec![];
        for &i in &g {
            if let Some(name) = block_name(i) {
                for (j, s) in srcs.iter().enumerate() {
                    if !g.contains(&j) && s.d.name == name && !matches!(compare_locations(&[&srcs[i].loc, &s.loc], srcs[i].pi == s.pi), LocationMatch::Equal | LocationMatch::IdenticalPlaceholder) {
                        occupied.push(s.site.clone());
                    }
                }
            }
        }
        if !occupied.is_empty() {
            let anchor = &srcs[g[0]];
            out.push(Suggestion::new("SSC-EWI-DBTPRJ0019",format!("Source blocks {} have a canonical-name collision with an existing different location at {}.",sites.join(", "),occupied.join(", ")))
                .in_project(&pf.projects[anchor.pi]).file(&anchor.d.file).line(anchor.d.line).ctx("class",json!("unresolved"))
                .remediation(format!("Keep the existing source declarations and calls; do not redirect reads into the occupied name. Resolve this naming collision with the owner before consolidating: coordinate a collision-free name and every affected source call for {} and {}. {LOCATION_CHECK}",sites.join(", "),occupied.join(", "))));
            continue;
        }
        let none: BTreeSet<String> = BTreeSet::new();
        let any_reads = g.iter().any(|&i| !srcs[i].reads.is_empty());
        let var_note = if !any_reads && projects.iter().any(|&pi| pf.projects[pi].models.iter().any(|m| !m.is_python && !var_relation_reads(&m.raw).is_empty())) {
            " The models of these projects build table names from vars instead of calling `source()`; PRJ0021 covers those reads."
        } else {
            ""
        };
        let (anchor, class, rem) = match &overall {
            LocationMatch::Equal | LocationMatch::IdenticalPlaceholder => {
                let placeholder = overall == LocationMatch::IdenticalPlaceholder;
                let fin = if placeholder { None } else { block_name(g[0]) };
                let (kept, fin, mut t) = fold(&g, fin.as_deref(), &none);
                t.push_str(&source_location_fix(&pf.projects[srcs[kept].pi], &srcs[kept].d, &fin, &srcs[kept].loc));
                if placeholder {
                    t.push_str(&format!(
                        " Once the real schema is known, name the block after it in lower case (`<database>_<schema>` if another database has a schema of that name) and change the `source('{fin}', ...)` calls to match. If the real per-project locations differ, rename instead: one block per database.schema. {LOCATION_CHECK}"
                    ));
                }
                t.push_str(var_note);
                (kept, "consolidate", t)
            }
            LocationMatch::Different(_) => {
                // One cluster per location; each becomes one block.
                let mut cd = Dsu::new(g.len());
                for a in 0..g.len() {
                    for b in a + 1..g.len() {
                        let m = compare_locations(&[&srcs[g[a]].loc, &srcs[g[b]].loc], srcs[g[a]].pi == srcs[g[b]].pi);
                        if matches!(m, LocationMatch::Equal | LocationMatch::IdenticalPlaceholder) {
                            cd.union(a, b);
                        }
                    }
                }
                let mut clusters: BTreeMap<usize, Vec<usize>> = BTreeMap::new();
                for (a, &e) in g.iter().enumerate() {
                    let r = cd.find(a);
                    clusters.entry(r).or_default().push(e);
                }
                // A call that two clusters both read is ambiguous.
                let mut claims: BTreeMap<String, BTreeSet<usize>> = BTreeMap::new();
                for (ci, cl) in clusters.values().enumerate() {
                    for &e in cl {
                        for c in &srcs[e].reads {
                            claims.entry(c.site.clone()).or_default().insert(ci);
                        }
                    }
                }
                let ambiguous: BTreeSet<String> = claims.into_iter().filter(|(_, v)| v.len() > 1).map(|(k, _)| k).collect();
                let mut taken: BTreeSet<String> = estate_names.iter().filter(|n| !names.iter().any(|m| m.eq_ignore_ascii_case(n))).cloned().collect();
                let mut parts: Vec<String> = vec![];
                for cl in clusters.values() {
                    let e = cl[0];
                    let base = block_name(e).unwrap_or_else(|| {
                        let tag = if same_project {
                            Path::new(&srcs[e].d.file).parent().and_then(|d| d.file_name()).map_or_else(|| "entry".to_string(), |f| f.to_string_lossy().to_lowercase())
                        } else {
                            project_prefix(pf, srcs[e].pi)
                        };
                        format!("{}_{tag}", srcs[e].d.name)
                    });
                    let fin = free_name(&base, &taken);
                    taken.insert(fin.to_lowercase());
                    let (kept, fin, mut t) = fold(cl, Some(&fin), &ambiguous);
                    t.push_str(&source_location_fix(&pf.projects[srcs[kept].pi], &srcs[kept].d, &fin, &srcs[kept].loc));
                    parts.push(t);
                }
                let mut t = format!("Give each location its own block, named after its schema in lower case (`<database>_<schema>` when two databases share a schema name). {}", parts.join(" "));
                if !ambiguous.is_empty() {
                    t.push_str(&format!(
                        " These `source()` calls name a table more than one of the entries declares, so read each caller and point it at the block it needs: {}.",
                        ambiguous.into_iter().collect::<Vec<_>>().join(", ")
                    ));
                }
                (g[0], "rename", t)
            }
            LocationMatch::Unresolved(_) => {
                let t = format!(
                    "Do not merge or rename these entries until their locations are checked. {LOCATION_CHECK} If they resolve to one database.schema, keep one block (the entry most `source()` calls read) and move the other entries' tables into it. If they differ, give each location its own block named after its schema in lower case (`<database>_<schema>` when two databases share a schema name) and change each project's `source('<old>', ...)` calls. Either way, set `database:` to a literal or a `target.name` if/elif block whose `else` is `invalid_database`, and `schema:` to a literal, not a var; get the real database for each target from the owner or the original connection rather than guessing.{var_note}"
                );
                (g[0], "unresolved", t)
            }
        };
        let a = &srcs[anchor];
        let case_s = match case {
            SrcCase::SameName => "same_name",
            SrcCase::DuplicateTable => "duplicate_table",
            SrcCase::Alias => "alias",
        };
        out.push(
            Suggestion::new("SSC-EWI-DBTPRJ0019", msg)
                .in_project(&pf.projects[a.pi])
                .file(a.d.file.clone())
                .line(a.d.line)
                .evidence(sites.join(" / "))
                .remediation(rem)
                .effort(effort::LOW)
                .ctx("source_name", json!(a.d.name))
                .ctx("case", json!(case_s))
                .ctx("class", json!(class))
                .ctx("members", json!(sites))
                .ctx("cross_project", json!(projects.len() > 1)),
        );
    }
    out
}

/// How a group of PRJ0020 models is fixed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum DupClass {
    /// The SQL is identical apart from comments and whitespace: keep one copy.
    Consolidate,
    /// Different SQL writing one pinned relation: combine the writers.
    Merge,
    /// Different SQL, relation not pinned to one table: give each a name.
    Rename,
    /// Mixed name and relation collisions need coordinated ownership decisions.
    Unresolved,
}

/// Models that collide by name, or write one relation, as one defect.
#[derive(Debug, Clone)]
pub(crate) struct DupGroup {
    /// Sorted by root-relative path; the first is kept.
    pub members: Vec<shared::Node>,
    pub class: DupClass,
    /// True when two members of one project share a name, so dbt cannot load it.
    pub same_project_name: bool,
    /// True when the members span more than one project.
    pub cross_project: bool,
    /// For `Merge`: the members write one relation only as generated
    /// (placeholder locations).
    pub placeholder: bool,
}

/// The PRJ0020 groups of the estate: connected components over "same model
/// name" and "same relation" (equal or identical-placeholder location).
pub(crate) fn model_dup_groups(pf: &PortfolioContext) -> Vec<DupGroup> {
    use shared::{compare_locations, model_relation, normalized_sql, LocationMatch, Node};
    let nodes: Vec<Node> = pf.projects.iter().enumerate().flat_map(|(pi, p)| (0..p.models.len()).map(move |mi| (pi, mi))).collect();
    let rels: Vec<Option<shared::ModelRelation>> = nodes.iter().map(|&(pi, mi)| model_relation(&pf.projects[pi], &pf.projects[pi].models[mi])).collect();
    let mut parent: Vec<usize> = (0..nodes.len()).collect();
    fn find(parent: &mut [usize], i: usize) -> usize {
        let mut r = i;
        while parent[r] != r {
            r = parent[r];
        }
        parent[i] = r;
        r
    }
    fn union(parent: &mut [usize], a: usize, b: usize) {
        let (ra, rb) = (find(parent, a), find(parent, b));
        if ra != rb {
            parent[ra.max(rb)] = ra.min(rb);
        }
    }
    let mut by_name: std::collections::BTreeMap<String, Vec<usize>> = Default::default();
    let mut by_ident: std::collections::BTreeMap<String, Vec<usize>> = Default::default();
    for (i, &(pi, mi)) in nodes.iter().enumerate() {
        by_name.entry(pf.projects[pi].models[mi].name.to_lowercase()).or_default().push(i);
        if let Some(k) = rels[i].as_ref().and_then(|r| r.location.identifier.key()) {
            by_ident.entry(k).or_default().push(i);
        }
    }
    // Compared as in the merged project, so an unset database or schema is the
    // one target for every member.
    let same_rel = |a: usize, b: usize| match (&rels[a], &rels[b]) {
        (Some(x), Some(y)) => matches!(
            compare_locations(&[&x.location, &y.location], true),
            LocationMatch::Equal | LocationMatch::IdenticalPlaceholder
        ),
        _ => false,
    };
    for v in by_name.values() {
        for &b in &v[1..] {
            union(&mut parent, v[0], b);
        }
    }
    for v in by_ident.values() {
        for (k, &a) in v.iter().enumerate() {
            for &b in &v[k + 1..] {
                if same_rel(a, b) {
                    union(&mut parent, a, b);
                }
            }
        }
    }
    let mut comps: std::collections::BTreeMap<usize, Vec<usize>> = Default::default();
    for i in 0..nodes.len() {
        let r = find(&mut parent, i);
        comps.entry(r).or_default().push(i);
    }
    let path = |i: usize| crate::discovery::root_relative(&pf.projects[nodes[i].0], &pf.projects[nodes[i].0].models[nodes[i].1].relative_path);
    let mut out = vec![];
    for mut c in comps.into_values().filter(|c| c.len() > 1) {
        c.sort_by_key(|&i| path(i));
        let model = |i: usize| &pf.projects[nodes[i].0].models[nodes[i].1];
        let projects: BTreeSet<usize> = c.iter().map(|&i| nodes[i].0).collect();
        let same_project_name = c.iter().enumerate().any(|(k, &a)| c[k + 1..].iter().any(|&b| nodes[a].0 == nodes[b].0 && model(a).name.eq_ignore_ascii_case(&model(b).name)));
        let sql: BTreeSet<String> = c.iter().map(|&i| normalized_sql(model(i))).collect();
        let all_same_rel = c.iter().all(|&b| same_rel(c[0], b) || b == c[0]);
        let names: BTreeSet<String> = c.iter().map(|&i| model(i).name.to_lowercase()).collect();
        let pinned = c.iter().any(|&i| rels[i].as_ref().is_some_and(|r| r.pinned));
        let mixed_relations = !all_same_rel && c.iter().enumerate().any(|(k, &a)| c[k + 1..].iter().any(|&b| same_rel(a, b)));
        let class = if mixed_relations {
            DupClass::Unresolved
        } else if sql.len() == 1 {
            DupClass::Consolidate
        } else if all_same_rel && (pinned || names.len() > 1) {
            DupClass::Merge
        } else {
            DupClass::Rename
        };
        let placeholder = class == DupClass::Merge && {
            let locs: Vec<&crate::rules::prj::shared::Location> = c.iter().filter_map(|&i| rels[i].as_ref().map(|r| &r.location)).collect();
            compare_locations(&locs, true) == LocationMatch::IdenticalPlaceholder
        };
        out.push(DupGroup {
            members: c.iter().map(|&i| nodes[i]).collect(),
            class,
            same_project_name,
            cross_project: projects.len() > 1,
            placeholder,
        });
    }
    out
}

/// The line of a model's `alias=` setting, else 1.
fn alias_line(m: &crate::discovery::ModelFile) -> u32 {
    rx!(r"\balias\s*=").find(&m.raw).map_or(1, |x| m.line_of(x.start()))
}

/// A name for a renamed copy that no model of the estate uses yet.
fn free_name(base: &str, taken: &BTreeSet<String>) -> String {
    let mut n = base.to_string();
    let mut k = 2;
    while taken.contains(&n.to_lowercase()) {
        n = format!("{base}_{k}");
        k += 1;
    }
    n
}

/// A prefix that tells project `pi` apart: its name when that is unique and
/// not a placeholder, else its folder name.
fn project_prefix(pf: &PortfolioContext, pi: usize) -> String {
    let p = &pf.projects[pi];
    let unique = pf.projects.iter().filter(|q| q.name.eq_ignore_ascii_case(&p.name)).count() == 1;
    if unique && !PLACEHOLDER_VALUES.iter().any(|v| v.eq_ignore_ascii_case(&p.name)) {
        return p.name.clone();
    }
    p.root.file_name().map(|f| f.to_string_lossy().to_string()).filter(|f| !f.is_empty()).unwrap_or_else(|| p.name.clone())
}

fn prj0020(pf: &PortfolioContext) -> Vec<Suggestion> {
    use shared::{call_sites, m_folder, model_relation, model_tags, CallKind, CallRef, Node, LOCATION_CHECK};
    let model = |n: Node| &pf.projects[n.0].models[n.1];
    let path = |n: Node| crate::discovery::root_relative(&pf.projects[n.0], &model(n).relative_path);
    let calls: Vec<Vec<CallRef>> = pf.projects.iter().map(call_sites).collect();
    let mut taken: BTreeSet<String> = pf.projects.iter().flat_map(|p| p.models.iter().map(|m| m.name.to_lowercase())).collect();
    // Explicit packages own their refs even when another project makes the call.
    let refs_to = |pi: usize, name: &str| -> Vec<(usize, &CallRef)> {
        calls.iter().enumerate().flat_map(|(caller, calls)| calls.iter().map(move |c| (caller, c))).filter(|&(caller, c)| {
            c.kind == CallKind::Ref && c.name.eq_ignore_ascii_case(name)
                && c.package.as_ref().map_or(caller == pi, |package| package.eq_ignore_ascii_case(&pf.projects[pi].name))
        }).collect()
    };
    let ref_code = |c: &CallRef, name: &str| c.package.as_ref().map_or_else(|| format!("ref('{name}')"), |package| format!("ref('{package}', '{name}')"));
    let relation = |n: Node| {
        model_relation(&pf.projects[n.0], model(n)).map_or_else(|| "<unresolved relation>".to_string(), |rel| {
            let shown = |part: &shared::LocPart, what: &str| match &part.value {
                shared::Part::Known(value) | shared::Part::Placeholder(value) => value.clone(),
                shared::Part::Target => format!("<target {what}>"),
                shared::Part::Unknown(_) => part.var.as_ref().map_or_else(|| format!("<{what}>"), |var| format!("<var {var}>")),
            };
            format!("{}.{}.{}", shown(&rel.location.database, "database"), shown(&rel.location.schema, "schema"), shown(&rel.location.identifier, "identifier"))
        })
    };
    let mut out = vec![];
    for g in model_dup_groups(pf) {
        let keep = g.members[0];
        let site = |n: Node| format!("{}:{}", path(n), if model_relation(&pf.projects[n.0], model(n)).is_some_and(|r| r.pinned) { alias_line(model(n)) } else { 1 });
        let sites: Vec<String> = g.members.iter().map(|&n| site(n)).collect();
        let names: BTreeSet<&str> = g.members.iter().map(|&n| model(n).name.as_str()).collect();
        let first_name = model(keep).name.clone();
        let subject = if names.len() == 1 { format!("Model `{first_name}`") } else { format!("Models {}", names.iter().map(|n| format!("`{n}`")).collect::<Vec<_>>().join(", ")) };
        let why = if g.same_project_name {
            " Two of them are in one project, so dbt refuses to load it until one is renamed or removed."
        } else if g.cross_project && names.len() == 1 {
            " They are in different projects, so the names collide once the projects are merged."
        } else {
            ""
        };
        let (anchor, msg, rem, level) = match g.class {
            DupClass::Consolidate => {
                let drop: Vec<Node> = g.members[1..].to_vec();
                let mut moved: Vec<String> = vec![];
                for &n in &drop {
                    for (_, c) in refs_to(n.0, &model(n).name) {
                        if c.package.is_some() || !model(n).name.eq_ignore_ascii_case(&first_name) {
                            moved.push(format!("`{}` to `ref('{first_name}')` at {}", ref_code(c, &c.name), c.site));
                        }
                    }
                }
                let refs = if moved.is_empty() {
                    "No `ref()` call changes: every copy has the kept model's name.".to_string()
                } else {
                    format!("Then change these `ref()` calls: {}.", moved.join(", "))
                };
                (
                    drop[0],
                    format!("{subject} is defined {} times with the same SQL apart from comments and whitespace: {}.{why}", g.members.len(), sites.join(", ")),
                    format!("Keep `{}` and delete {}. {refs}", path(keep), drop.iter().map(|&n| format!("`{}`", path(n))).collect::<Vec<_>>().join(", ")),
                    if g.same_project_name { level::ERROR } else { level::WARNING },
                )
            }
            DupClass::Merge => {
                let relation = relation(keep);
                let tables: Vec<String> = g.members.iter().filter(|&&n| model(n).materialization() == "table").map(|&n| path(n)).collect();
                let overwrite = if tables.is_empty() {
                    String::new()
                } else {
                    format!(" {} {} `materialized='table'`, so each run rebuilds the whole table and the last writer to run replaces the others' rows.", tables.join(", "), if tables.len() == 1 { "is" } else { "are" })
                };
                let mut refs: Vec<String> = vec![];
                for &n in &g.members {
                    refs.extend(refs_to(n.0, &model(n).name).iter().map(|(_, c)| c.site.clone()));
                }
                refs.sort();
                refs.dedup();
                let refs = if refs.is_empty() { "No `ref()` call reads them.".to_string() } else { format!("Point these `ref()` calls at the combined model: {}.", refs.join(", ")) };
                let ph = if g.placeholder { format!(" The location is the same only as generated (placeholder values); if the real per-model locations differ, rename instead. {LOCATION_CHECK}") } else { String::new() };
                (
                    keep,
                    format!(
                        "{} models write one relation, `{relation}`: {}.{why} dbt Fusion stops at parse with \"dbt found two resources with the database relation\" when two models write one relation.{overwrite}",
                        g.members.len(),
                        sites.join(", ")
                    ),
                    format!(
                        "Combine the writers into one model that writes `{relation}`, keeping every writer's logic (for example a `union all` of their selects, or one CTE per writer), then delete the other files. Check the original workflow's load order and truncate settings first, so the combined model loads the rows the last run of the workflow left. {refs}{ph}"
                    ),
                    if g.same_project_name { level::ERROR } else { level::WARNING },
                )
            }
            DupClass::Rename => {
                let kept_name = first_name.clone();
                let mut lines: Vec<String> = vec![];
                let mut ambiguous: Vec<String> = vec![];
                // The first member keeps its name; a later member whose name an
                // earlier member already uses is renamed.
                let mut seen: BTreeSet<String> = BTreeSet::from([kept_name.to_lowercase()]);
                let renamed: Vec<Node> = g.members[1..].iter().copied().filter(|&n| !seen.insert(model(n).name.to_lowercase())).collect();
                for &n in &renamed {
                    let m = model(n);
                    let same_project = g.members.iter().filter(|&&x| x.0 == n.0 && model(x).name.eq_ignore_ascii_case(&m.name)).count() > 1;
                    let prefix = if same_project {
                        m_folder(m).or_else(|| m.segments.last().cloned()).unwrap_or_else(|| project_prefix(pf, n.0))
                    } else {
                        project_prefix(pf, n.0)
                    };
                    let new = free_name(&format!("{prefix}__{}", m.name), &taken);
                    taken.insert(new.to_lowercase());
                    let new_path = crate::discovery::display_path(&Path::new(&path(n)).with_file_name(format!("{new}.{}", Path::new(&m.relative_path).extension().map_or("sql".into(), |e| e.to_string_lossy().to_string()))));
                    // Which ref() calls mean this copy.
                    let copies: Vec<Node> = g.members.iter().copied().filter(|&x| x.0 == n.0 && model(x).name.eq_ignore_ascii_case(&m.name)).collect();
                    let marks = |x: Node| {
                        let mut s: BTreeSet<String> = model_tags(model(x)).into_iter().filter(|t| t.to_lowercase().starts_with("m_")).map(|t| t.to_lowercase()).collect();
                        if let Some(f) = m_folder(model(x)) {
                            s.insert(f.to_lowercase());
                        }
                        s
                    };
                    let mut moving: std::collections::BTreeMap<(String, String), Vec<String>> = Default::default();
                    for (caller_project, c) in refs_to(n.0, &m.name) {
                        if c.package.as_ref().is_some_and(|package| pf.projects.iter().filter(|p| p.name.eq_ignore_ascii_case(package)).count() != 1) {
                            ambiguous.push(format!("`{}` at {} (package name has multiple owners)", ref_code(c, &c.name), c.site));
                            continue;
                        }
                        let owns_call = if copies.len() == 1 {
                            true
                        } else if caller_project != n.0 {
                            ambiguous.push(format!("`{}` at {} (the owning package has multiple copies)", ref_code(c, &c.name), c.site));
                            false
                        } else {
                            let mut caller: BTreeSet<String> = c.tags.iter().filter(|t| t.to_lowercase().starts_with("m_")).map(|t| t.to_lowercase()).collect();
                            if let Some(f) = &c.m_folder {
                                caller.insert(f.to_lowercase());
                            }
                            let hits: Vec<Node> = copies.iter().copied().filter(|&x| !marks(x).is_disjoint(&caller)).collect();
                            match hits.as_slice() {
                                [h] => *h == n,
                                _ => {
                                    ambiguous.push(format!("`{}` at {}", ref_code(c, &c.name), c.site));
                                    false
                                }
                            }
                        };
                        if owns_call {
                            moving.entry((ref_code(c, &c.name), ref_code(c, &new))).or_default().push(c.site.clone());
                        }
                    }
                    let refs = if moving.is_empty() {
                        "no `ref()` call changes".to_string()
                    } else {
                        let mappings: Vec<String> = moving.into_iter().map(|((old, new), mut sites)| {
                            sites.sort();
                            sites.dedup();
                            format!("`{old}` to `{new}` at {}", sites.join(", "))
                        }).collect();
                        format!("change {}", mappings.join("; change "))
                    };
                    lines.push(format!("rename `{}` to `{new_path}` and {refs}", path(n)));
                }
                ambiguous.sort();
                ambiguous.dedup();
                let amb = if ambiguous.is_empty() {
                    String::new()
                } else {
                    format!(" These `ref()` calls could mean either copy (package ownership or the owning project's `m_*` folder and tags are ambiguous): {}; read each caller and point it at the copy it needs.", ambiguous.join(", "))
                };
                let alias_note = if g.members.iter().any(|&n| model_relation(&pf.projects[n.0], model(n)).is_some_and(|r| r.pinned)) {
                    " A copy with `alias` keeps writing its table; the others' tables take the new name."
                } else {
                    " Renaming a model also renames the table it builds."
                };
                (
                    renamed.first().copied().unwrap_or(keep),
                    format!("{subject} is defined {} times with different SQL: {}.{why}", g.members.len(), sites.join(", ")),
                    format!("Keep `{}` as `{kept_name}`. Then {}.{amb}{alias_note}", path(keep), lines.join("; ")),
                    if g.same_project_name { level::ERROR } else { level::WARNING },
                )
            }
            DupClass::Unresolved => {
                let writers: Vec<String> = g.members.iter().map(|&n| format!("{} writes `{}`", site(n), relation(n))).collect();
                (
                    keep,
                    format!("{subject} has connected name and relation collisions: {}.{why} Renaming duplicate names alone does not resolve the shared writer relations.", writers.join("; ")),
                    format!("Retain all writers and their logic: {}. Resolve both the duplicate model names and the shared relation writers with the owner before renaming or deleting files. Do not delete copies or assume a filename rename changes a pinned alias. Confirm each writer's database, schema, alias and load semantics; combine same-relation writer logic into one model only after confirming the intended output, then choose unique names and map callers to their owners. {LOCATION_CHECK}", writers.join("; ")),
                    if g.same_project_name { level::ERROR } else { level::WARNING },
                )
            }
        };
        let p = &pf.projects[anchor.0];
        let m = model(anchor);
        let class = match g.class {
            DupClass::Consolidate => "consolidate",
            DupClass::Merge => "merge",
            DupClass::Rename => "rename",
            DupClass::Unresolved => "unresolved",
        };
        out.push(
            Suggestion::new("SSC-EWI-DBTPRJ0020", msg)
                .in_project(p)
                .file(m.relative_path.clone())
                .line(if g.class == DupClass::Merge { alias_line(m) } else { 1 })
                .level(level)
                .evidence(sites.join(" / "))
                .remediation(rem)
                .effort(effort::LOW)
                .ctx("model", json!(m.name))
                .ctx("class", json!(class))
                .ctx("members", json!(sites))
                .ctx("cross_project", json!(g.cross_project)),
        );
    }
    out
}

fn prj0021(pf: &PortfolioContext) -> Vec<Suggestion> {
    relations::findings(pf, false)
}

fn prj0022(pf: &PortfolioContext) -> Vec<Suggestion> {
    relations::findings(pf, true)
}

#[cfg(test)]
mod tests {
    use std::collections::BTreeSet;

    use crate::testing::TempProject;

    const M: &str = "select 1";

    fn sub(n: &str, models: usize, extra: &[(String, String)]) -> Vec<(String, String)> {
        let mut v = vec![(format!("{n}/dbt_project.yml"), format!("name: {n}\nversion: '1.0'\nprofile: p\n"))];
        for i in 0..models {
            v.push((format!("{n}/models/m{i}.sql"), M.into()));
        }
        v.extend(extra.iter().cloned());
        v
    }
    fn proj(parts: Vec<Vec<(String, String)>>) -> TempProject {
        let all: Vec<(String, String)> = parts.into_iter().flatten().collect();
        let refs: Vec<(&str, &str)> = all.iter().map(|(a, b)| (a.as_str(), b.as_str())).collect();
        TempProject::new(&refs)
    }

    #[test]
    fn prj0001() {
        let t = proj(vec![sub("a", 1, &[]), sub("b", 7, &[])]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0001").len(), 1);
        let t = proj(vec![sub("a", 6, &[]), sub("b", 7, &[])]);
        assert!(t.findings("SSC-EWI-DBTPRJ0001").is_empty());
    }

    #[test]
    fn prj0002() {
        let m = ("models/s.sql".to_string(), "select * from {{ source('raw','t') }}".to_string());
        let mk = |n: &str| sub(n, 0, &[(format!("{n}/{}", m.0), m.1.clone())]);
        let t = proj(vec![mk("a"), mk("b")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0002").len(), 1);
        let other = vec![("b/models/s.sql".to_string(), "select * from {{ source('raw','u') }}".to_string())];
        let t = proj(vec![mk("a"), sub("b", 0, &other)]);
        assert!(t.findings("SSC-EWI-DBTPRJ0002").is_empty());
    }

    #[test]
    fn prj0002_related_files() {
        let src = "version: 2\nsources:\n  - name: raw\n    tables:\n      - name: t\n";
        let mk = |n: &str| {
            sub(n, 0, &[
                (format!("{n}/models/s.sql"), "select * from {{ source('raw','t') }}".to_string()),
                (format!("{n}/models/_sources.yml"), src.to_string()),
            ])
        };
        let f = proj(vec![mk("a"), mk("b")]).findings("SSC-EWI-DBTPRJ0002");
        assert_eq!(f[0].context["related_files"], serde_json::json!(["a/models/_sources.yml:5", "b/models/_sources.yml:5"]));
    }

    #[test]
    fn prj0003_related_files() {
        let pk = |v: &str| format!("packages:\n  - package: dbt-labs/dbt_utils\n    version: {v}\n");
        let mk = |n: &str, v: &str| sub(n, 0, &[(format!("{n}/packages.yml"), pk(v))]);
        let f = proj(vec![mk("a", "1.0.0"), mk("b", "1.1.0"), sub("c", 0, &[])]).findings("SSC-EWI-DBTPRJ0003");
        assert_eq!(f[0].context["related_files"], serde_json::json!(["a/packages.yml:2", "b/packages.yml:2", "c/dbt_project.yml:1"]));
    }

    #[test]
    fn prj0005_placeholder_line() {
        let t = TempProject::new(&[("dbt_project.yml", "name: demo\nversion: '1.0'\nprofile: \"YOUR_PROFILE_NAME\"\nmodels: {}\n")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0005")[0].line, Some(3));
    }

    #[test]
    fn prj0006_related_files() {
        let t = TempProject::new(&[("orchestration/t.sql", "select 1;\nEXECUTE DBT PROJECT db.s.p1;\nEXECUTE DBT PROJECT db.s.p2;")]);
        let f = t.findings("SSC-EWI-DBTPRJ0006");
        assert_eq!(f[0].context["related_files"], serde_json::json!(["orchestration/t.sql:2", "orchestration/t.sql:3"]));
    }

    #[test]
    fn prj0003() {
        let t = proj(vec![sub("a", 6, &[]), sub("b", 6, &[]), sub("c", 6, &[])]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0003").len(), 1);
        let t = proj(vec![sub("a", 6, &[]), sub("b", 6, &[])]);
        assert!(t.findings("SSC-EWI-DBTPRJ0003").is_empty());
    }

    #[test]
    fn prj0004() {
        let t = TempProject::new(&[("profiles.yml", "demo: {}\n")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0004").len(), 1);
        let t = TempProject::new(&[("models/a.sql", M)]);
        assert!(t.findings("SSC-EWI-DBTPRJ0004").is_empty());
    }

    #[test]
    fn prj0005() {
        let t = TempProject::new(&[("dbt_project.yml", "name: YOUR_PROJECT_NAME\nprofile: p\n")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0005").len(), 1);
        let t = TempProject::new(&[("models/a.sql", M)]);
        assert!(t.findings("SSC-EWI-DBTPRJ0005").is_empty());
    }

    #[test]
    fn prj0006() {
        let s = "execute dbt project db.s.p1;\nEXECUTE DBT PROJECT db.s.p2;";
        let t = TempProject::new(&[("orchestration/t.sql", s)]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0006").len(), 1);
        let t = TempProject::new(&[("orchestration/t.sql", "EXECUTE DBT PROJECT db.s.p1;")]);
        assert!(t.findings("SSC-EWI-DBTPRJ0006").is_empty());
    }

    #[test]
    fn prj0007() {
        let t = TempProject::new(&[("models/a.sql", M), ("packages.yml", "packages:\n  - package: dbt-labs/dbt_utils\n    version: 1.0.0\n")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0007").len(), 1);
        let pk = "packages:\n  - package: Snowflake-Labs/dbt_constraints\n    version: 1.0.0\n  - package: Snowflake-Labs/dbt_semantic_view\n    version: 1.0.0\n";
        let t = TempProject::new(&[("models/a.sql", M), ("packages.yml", pk)]);
        assert!(t.findings("SSC-EWI-DBTPRJ0007").is_empty());
    }

    #[test]
    fn prj0008() {
        let t = TempProject::new(&[("models/a.sql", M), ("target/x.json", "{}")]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0008").len(), 1);
        let t = TempProject::new(&[("models/a.sql", M), ("target/x.json", "{}"), (".gitignore", "target/\n")]);
        assert!(t.findings("SSC-EWI-DBTPRJ0008").is_empty());
    }

    fn cnt(t: &TempProject, c: &str) -> usize {
        t.findings(c).len()
    }

    fn pv(yml: &str, files: &[(&str, &str)]) -> TempProject {
        let mut v = vec![("dbt_project.yml", yml)];
        v.extend_from_slice(files);
        TempProject::new(&v)
    }

    const HEAD: &str = "name: demo\nversion: '1.0'\nprofile: demo\n";

    #[test]
    fn new_prj0009() {
        let t = TempProject::new(&[("models/s.yml", "sources:\n  - name: raw\n    schema: \"{{ var('s') }}\"\n"), ("models/a.sql", "{{ config(alias=var('a')) }}\nselect 1"), ("models/b.sql", "{{ config(alias=var('b')) }}\nselect 1")]);
        // One finding for the YAML key, one aggregate for both model configs.
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0009"), 2);
        let c = TempProject::new(&[("models/s.yml", "sources:\n  - name: raw\n    schema: RAW\n"), ("models/a.sql", "{{ config(alias='a') }}\nselect 1")]);
        assert_eq!(cnt(&c, "SSC-EWI-DBTPRJ0009"), 0);
    }

    #[test]
    fn prj0009_points_at_prj0013() {
        let t = TempProject::new(&[("models/s.yml", "sources:\n  - name: raw\n    schema: \"{{ var('InputSchema', 'InputSchema') }}\"\n"), ("models/a.sql", "select 1")]);
        let f: Vec<_> = t.findings("SSC-EWI-DBTPRJ0009");
        assert!(f[0].remediation.contains("SSC-EWI-DBTPRJ0013"), "{}", f[0].remediation);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0013"), 1);
        let t = TempProject::new(&[("models/s.yml", "sources:\n  - name: raw\n    schema: \"{{ var('s') }}\"\n"), ("models/a.sql", "select 1")]);
        assert!(t.findings("SSC-EWI-DBTPRJ0009")[0].remediation.contains("invalid_database"));
    }

    #[test]
    fn new_prj0010() {
        let t = TempProject::new(&[("models/a.sql", "{% if target.name == 'prod' %}select 1{% else %}select 2{% endif %}")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0010"), 1);
        assert_eq!(cnt(&TempProject::new(&[("models/a.sql", "select 1")]), "SSC-EWI-DBTPRJ0010"), 0);
    }

    #[test]
    fn new_prj0011() {
        let y = format!("{HEAD}models:\n  demo:\n    +database: \"{{{{ env_var('D') }}}}\"\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select 1")]), "SSC-EWI-DBTPRJ0011"), 1);
        let t = TempProject::new(&[("models/a.sql", "{{ config(schema=env_var('S')) }}\nselect 1")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0011"), 1);
        assert_eq!(cnt(&TempProject::new(&[("models/a.sql", "select 1")]), "SSC-EWI-DBTPRJ0011"), 0);
    }

    #[test]
    fn new_prj0012() {
        let a = format!("{HEAD}vars:\n  s: \"100\"\n");
        let b = format!("{HEAD}vars:\n  s: 200\n");
        let t = TempProject::new(&[("a/dbt_project.yml", &a), ("b/dbt_project.yml", &b), ("a/models/x.sql", "select 1"), ("b/models/x.sql", "select 1")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0012"), 1);
        let b = format!("{HEAD}vars:\n  s: 100\n");
        let t = TempProject::new(&[("a/dbt_project.yml", &a), ("b/dbt_project.yml", &b), ("a/models/x.sql", "select 1"), ("b/models/x.sql", "select 1")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0012"), 0);
    }

    #[test]
    fn new_prj0013() {
        let t = TempProject::new(&[("models/a.sql", "select '{{ var('r', 'r') }}'")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0013"), 1);
        let c = TempProject::new(&[("models/a.sql", "select '{{ var('r', 'x') }}'"), ("models/b.sql", "{{ config(post_hook=\"x {{ var('h', 'h') }}\") }}select 1")]);
        assert_eq!(cnt(&c, "SSC-EWI-DBTPRJ0013"), 0);
    }

    #[test]
    fn new_prj0014() {
        let y = format!("{HEAD}vars:\n  d: ''\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select '{{ var('d') }}'")]), "SSC-EWI-DBTPRJ0014"), 1);
        let y2 = format!("{HEAD}vars:\n  d: ''\n  e: null\n");
        let f = pv(&y2, &[("models/a.sql", "select '{{ var('d') }}', '{{ var('e') }}'")]).findings("SSC-EWI-DBTPRJ0014");
        assert_eq!(f.len(), 1);
        assert!(f[0].message.contains("d, e"), "{}", f[0].message);
        let y = format!("{HEAD}vars:\n  d: x\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select '{{ var('d') }}'")]), "SSC-EWI-DBTPRJ0014"), 0);
    }

    #[test]
    fn new_prj0015() {
        let y = format!("{HEAD}vars:\n  SESSSTARTTIME: \"1753-01-01 00:00:00\"\n  PMFOLDERNAME: null\n");
        let reads = [("models/a.sql", "select '{{ var(\"SESSSTARTTIME\") }}', '{{ var(\"PMFOLDERNAME\") }}'")];
        assert_eq!(cnt(&pv(&y, &reads), "SSC-EWI-DBTPRJ0015"), 2);
        // Unread vars belong to PRJ0017 only, so the two rules never disagree on one line.
        assert_eq!(cnt(&pv(&y, &[]), "SSC-EWI-DBTPRJ0015"), 0);
        assert_eq!(cnt(&pv(&y, &[]), "SSC-EWI-DBTPRJ0017"), 1);
        let y = format!("{HEAD}vars:\n  SESSSTARTTIME: \"2024-01-01\"\n");
        assert_eq!(cnt(&pv(&y, &[]), "SSC-EWI-DBTPRJ0015"), 0);
    }

    #[test]
    fn new_prj0016() {
        let t = TempProject::new(&[("models/a.sql", "select {{ var('k') }}")]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0016"), 1);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0016")[0].level, "warning");
        for d in ["''", "'x'", "none", "var('j', 1)"] {
            let t = TempProject::new(&[("models/a.sql", &format!("select {{{{ var('k', {d}) }}}}") as &str)]);
            assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0016"), 0, "default {d}");
        }
        let g = "{% if var('k', '') != '' %}{{ var('k') }}{% else %}select 1{% endif %}";
        assert_eq!(cnt(&TempProject::new(&[("models/a.sql", g)]), "SSC-EWI-DBTPRJ0016"), 0);
        let y = format!("{HEAD}vars:\n  k: 1\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select {{ var('k') }}")]), "SSC-EWI-DBTPRJ0016"), 0);
        let y = format!("{HEAD}vars:\n  demo:\n    k: 1\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select {{ var('k') }}")]), "SSC-EWI-DBTPRJ0016"), 0);
    }

    #[test]
    fn prj0017_skips_package_vars() {
        let y = format!("{HEAD}vars:\n  dbt_artifacts_schema: S\n");
        let pk = "packages:\n  - package: brooklyn-data/dbt_artifacts\n    version: 2.0.0\n";
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select 1"), ("packages.yml", pk)]), "SSC-EWI-DBTPRJ0017"), 0);
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select 1")]), "SSC-EWI-DBTPRJ0017"), 1);
    }

    #[test]
    fn new_prj0017() {
        let y = format!("{HEAD}vars:\n  k: 1\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select 1")]), "SSC-EWI-DBTPRJ0017"), 1);
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select {{ var('k') }}")]), "SSC-EWI-DBTPRJ0017"), 0);
        // Many unread vars give one finding that lists each var and its line.
        let y = format!("{HEAD}vars:\n  a: 1\n  b: 2\n  PMFOLDERNAME: x\n");
        let f = pv(&y, &[("models/a.sql", "select 1")]).findings("SSC-EWI-DBTPRJ0017");
        assert_eq!(f.len(), 1);
        assert!(f[0].message.contains("a, b") && f[0].message.contains("built-ins") && f[0].message.contains("PMFOLDERNAME"));
        assert!(f[0].evidence.contains("b (dbt_project.yml:"), "{}", f[0].evidence);
    }

    #[test]
    fn new_prj0019() {
        // Same name across projects, same literal location: consolidate.
        let src = |t: &str| format!("sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: {t}\n");
        let t = proj(vec![
            sub("a", 0, &[("a/models/s.yml".into(), src("x"))]),
            sub("b", 0, &[("b/models/s.yml".into(), src("y")), ("b/models/r.sql".into(), "select * from {{ source('raw', 'y') }}".into())]),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0019");
        assert_eq!(f.len(), 1);
        let s = &f[0];
        assert_eq!((s.context["class"].as_str(), s.context["case"].as_str()), (Some("consolidate"), Some("same_name")));
        assert!(s.message.contains("a/models/s.yml:2") && s.message.contains("b/models/s.yml:2") && s.message.contains("collide"), "{}", s.message);
        // The entry with the most source() reads is kept, and the block is
        // named after its schema, so the one call changes.
        assert_eq!((s.file.as_str(), s.line), ("b/models/s.yml", Some(2)));
        let r = &s.remediation;
        assert!(r.contains("Keep the `raw` entry at b/models/s.yml:2 as the single declaration and rename it to `s`"), "{r}");
        assert!(r.contains("move `x` from a/models/s.yml:2 into it"), "{r}");
        assert!(r.contains("`source('raw', 'y')` to `source('s', 'y')` at b/models/r.sql:1"), "{r}");
        // Already literal: no location advice.
        assert!(!r.contains("target.name"), "{r}");
        // Clean: different names, different tables.
        let other = "sources:\n  - name: erp\n    tables:\n      - name: x\n".to_string();
        let t = proj(vec![sub("a", 0, &[("a/models/s.yml".into(), src("x"))]), sub("b", 0, &[("b/models/s.yml".into(), other)])]);
        assert!(t.findings("SSC-EWI-DBTPRJ0019").is_empty());
        // Clean: one entry per name in one project.
        assert_eq!(cnt(&files(&[("models/s.yml", &src("x")), ("models/a.sql", M)]), "SSC-EWI-DBTPRJ0019"), 0);
    }

    #[test]
    fn prj0019_within_project_split_and_duplicate_table() {
        let a = "sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: orders\n      - name: users\n";
        let b = "sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: orders\n      - name: items\n";
        let t = files(&[
            ("models/a/_s.yml", a),
            ("models/b/_s.yml", b),
            ("models/x.sql", "select * from {{ source('raw', 'items') }} join {{ source('raw', 'items') }} using (k)"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0019");
        assert_eq!(f.len(), 1, "{f:#?}");
        let s = &f[0];
        assert_eq!((s.level.as_str(), s.context["case"].as_str(), s.context["class"].as_str()), ("warning", Some("duplicate_table"), Some("consolidate")));
        assert!(s.message.contains("`raw.orders` (models/a/_s.yml:6, models/b/_s.yml:6)") && s.message.contains("dbt Fusion warns"), "{}", s.message);
        // b has the reads, so b is kept; a's `users` moves and `orders` is in both.
        assert!(s.remediation.contains("Keep the `raw` entry at models/b/_s.yml:2"), "{}", s.remediation);
        assert!(s.remediation.contains("move `users` from models/a/_s.yml:2") && s.remediation.contains("`orders` is declared in more than one entry"), "{}", s.remediation);
        // Split across files with no repeated table: the same_name case.
        let c = "sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: other\n";
        let t = files(&[("models/a/_s.yml", a), ("models/c/_s.yml", c)]);
        let s = &t.findings("SSC-EWI-DBTPRJ0019")[0];
        assert_eq!(s.context["case"].as_str(), Some("same_name"));
        assert!(s.message.contains("dbt accepts a source split across entries"), "{}", s.message);
    }

    #[test]
    fn prj0019_alias_under_another_name() {
        let t = files(&[
            ("models/a.yml", "sources:\n  - name: erp\n    database: RAW\n    schema: SALES\n    tables:\n      - name: orders\n"),
            ("models/b.yml", "sources:\n  - name: sales\n    database: raw\n    tables:\n      - name: ord\n        identifier: ORDERS\n"),
            ("models/r.sql", "select * from {{ source('erp', 'orders') }}"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0019");
        assert_eq!(f.len(), 1, "{f:#?}");
        let s = &f[0];
        assert_eq!((s.context["case"].as_str(), s.context["class"].as_str()), (Some("alias"), Some("consolidate")));
        assert!(s.message.contains("`erp.orders` and `sales.ord`"), "{}", s.message);
        // erp is read, so kept and named `sales` (its schema); the call moves.
        assert!(s.remediation.contains("Keep the `erp` entry at models/a.yml:2 as the single declaration and rename it to `sales`"), "{}", s.remediation);
        assert!(s.remediation.contains("`source('erp', 'orders')` to `source('sales', 'orders')` at models/r.sql:1"), "{}", s.remediation);
    }

    #[test]
    fn prj0019_rename_when_locations_differ() {
        let y = |db: &str| format!("sources:\n  - name: raw\n    database: {db}\n    schema: SALES\n    tables:\n      - name: orders\n");
        let t = proj(vec![
            sub("a", 0, &[("a/models/s.yml".into(), y("RAW_A")), ("a/models/r.sql".into(), "select * from {{ source('raw', 'orders') }}".into())]),
            sub("b", 0, &[("b/models/s.yml".into(), y("RAW_B")), ("b/models/r.sql".into(), "select 1\nfrom {{ source('raw', 'orders') }}".into())]),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0019");
        assert_eq!(f.len(), 1, "{f:#?}");
        let s = &f[0];
        assert_eq!(s.context["class"].as_str(), Some("rename"));
        assert!(s.message.contains("different locations") && s.message.contains("RAW_A") && s.message.contains("RAW_B"), "{}", s.message);
        let r = &s.remediation;
        // Same schema name in two databases: `<db>_<schema>`.
        assert!(r.contains("rename it to `raw_a_sales`") && r.contains("rename it to `raw_b_sales`"), "{r}");
        assert!(r.contains("`source('raw', 'orders')` to `source('raw_a_sales', 'orders')` at a/models/r.sql:1"), "{r}");
        assert!(r.contains("`source('raw', 'orders')` to `source('raw_b_sales', 'orders')` at b/models/r.sql:2"), "{r}");
    }

    #[test]
    fn prj0019_unresolved_and_var_defaults() {
        // No database in two projects: each takes its own target, so unresolved.
        let y = "sources:\n  - name: raw\n    tables:\n      - name: orders\n";
        let t = proj(vec![sub("a", 0, &[("a/models/s.yml".into(), y.into())]), sub("b", 0, &[("b/models/s.yml".into(), y.into())])]);
        let s = &t.findings("SSC-EWI-DBTPRJ0019")[0];
        assert_eq!(s.context["class"].as_str(), Some("unresolved"));
        assert!(s.message.contains("can't be resolved") && s.message.contains("target database"), "{}", s.message);
        assert!(s.remediation.contains("Do not merge or rename") && s.remediation.contains("target/manifest.json"), "{}", s.remediation);
        // var() and env_var() defaults resolve to one location: consolidate,
        // and the var is replaced by the target.name block.
        let a = "sources:\n  - name: raw\n    database: \"{{ var('raw_db', 'RAW') }}\"\n    schema: S\n    tables:\n      - name: x\n";
        let b = "sources:\n  - name: raw\n    database: \"{{ env_var('RAW_DB', 'RAW') }}\"\n    schema: S\n    tables:\n      - name: y\n";
        let t = proj(vec![sub("a", 0, &[("a/models/s.yml".into(), a.into())]), sub("b", 0, &[("b/models/s.yml".into(), b.into())])]);
        let s = &t.findings("SSC-EWI-DBTPRJ0019")[0];
        assert_eq!(s.context["class"].as_str(), Some("consolidate"));
        assert!(s.message.contains("one location, `RAW`.`S`"), "{}", s.message);
        let r = &s.remediation;
        assert!(r.contains("removes the var `raw_db`") && r.contains("`--vars`") && r.contains("orchestration call does not change"), "{r}");
        assert!(r.contains("{%- if target.name == \"dev\" -%} <database for dev>") && r.contains("{%- else -%} invalid_database"), "{r}");
        assert!(r.contains("are examples"), "{r}");
        assert!(!r.contains("var(") && !r.contains("--target"), "{r}");
    }

    fn prj0019_quoting_round_trip(kept_quoted: bool, moved_quoted: bool, kept_override: Option<bool>, moved_override: Option<bool>) {
        use crate::discovery::{build_portfolio, load_yaml_str, source_decls};
        use super::shared::{compare_locations, resolve_location, LocationMatch};
        use serde_json::{json, Value};

        let source = |table: &str, quoted: bool, table_override: Option<bool>| {
            let table_override = table_override.map(|value| format!("        quoting: {{identifier: {value}}}\n")).unwrap_or_default();
            format!("sources:\n  - name: raw\n    database: \"{{{{ var('db', 'DB') }}}}\"\n    schema: S\n    quoting: {{identifier: {quoted}}}\n    tables:\n      - name: {table}\n{table_override}")
        };
        let kept_yaml = source("orders", kept_quoted, kept_override);
        let moved_yaml = source("returns", moved_quoted, moved_override);
        let project = files(&[
            ("models/a.yml", &kept_yaml),
            ("models/b.yml", &moved_yaml),
            ("profiles.yml", "demo:\n  target: dev\n  outputs:\n    dev: {type: snowflake, database: DB, schema: S}\n"),
        ]);
        let before = build_portfolio(project.path());
        let declarations = source_decls(&before.projects[0]);
        let original: Vec<_> = declarations.iter().map(|decl| resolve_location(&before.projects[0], decl, &decl.tables[0])).collect();
        let findings = project.findings("SSC-EWI-DBTPRJ0019");
        assert_eq!(findings.len(), 1, "{findings:#?}");
        assert_eq!(findings[0].context["class"], "consolidate", "{findings:#?}");
        let remediation = &findings[0].remediation;
        assert!(remediation.contains("Keep the `raw` entry at models/a.yml:2"), "{remediation}");
        assert!(remediation.contains("move `returns` from models/b.yml:2 into it"), "{remediation}");
        let emitted: Vec<_> = remediation.split("```yaml\n").skip(1).map(|part| load_yaml_str(part.split("```").next().unwrap()).unwrap()).collect();
        let mut consolidated = emitted.iter().find(|yaml| yaml.get("sources").is_some()).expect("emitted source location").clone();
        let mut tables = vec![load_yaml_str(&kept_yaml).unwrap()["sources"][0]["tables"][0].clone(), load_yaml_str(&moved_yaml).unwrap()["sources"][0]["tables"][0].clone()];
        for patch in emitted.iter().filter_map(|yaml| yaml.get("tables").and_then(Value::as_array)).flatten() {
            let table = tables.iter_mut().find(|table| table["name"] == patch["name"]).expect("moved table quote override");
            table.as_object_mut().unwrap().extend(patch.as_object().unwrap().clone());
        }
        consolidated["sources"][0]["tables"] = json!(tables);
        let applied = files(&[("models/merged.yml", &serde_json::to_string(&consolidated).unwrap())]);
        let after = build_portfolio(applied.path());
        let merged = source_decls(&after.projects[0]);
        assert_eq!(merged.len(), 1);
        assert_eq!(merged[0].tables.len(), 2);
        for (index, table) in merged[0].tables.iter().enumerate() {
            let actual = resolve_location(&after.projects[0], &merged[0], table);
            assert_eq!(compare_locations(&[&original[index], &actual], false), LocationMatch::Equal, "{}: {remediation}", table.name);
            assert_eq!(actual.identifier.quoted, original[index].identifier.quoted, "{}: {remediation}", table.name);
        }
        assert_eq!(merged[0].quoting[2], Some(kept_quoted), "{remediation}");
        assert_eq!(merged[0].tables[0].quote_identifier, kept_override);
        if moved_override.is_some() {
            assert_eq!(merged[0].tables[1].quote_identifier, moved_override);
        }
    }

    #[test]
    fn prj0019_quoting_round_trip_inherited_lowercase_identifiers() {
        prj0019_quoting_round_trip(true, true, None, None);
    }

    #[test]
    fn prj0019_quoting_round_trip_explicit_false_overrides() {
        prj0019_quoting_round_trip(true, true, Some(false), Some(false));
    }

    #[test]
    fn prj0019_quoting_round_trip_moved_inherited_defaults() {
        prj0019_quoting_round_trip(true, false, None, None);
        prj0019_quoting_round_trip(false, true, None, None);
    }

    #[test]
    fn prj0019_quoting_round_trip_moved_explicit_overrides() {
        prj0019_quoting_round_trip(true, false, None, Some(true));
        prj0019_quoting_round_trip(false, true, None, Some(false));
    }

    #[test]
    fn prj0019_placeholders_consolidate_with_caveat() {
        let y = |t: &str| format!("sources:\n  - name: raw\n    schema: YOUR_SCHEMA\n    database: YOUR_DB\n    tables:\n      - name: {t}\n");
        let t = proj(vec![sub("a", 0, &[("a/models/s.yml".into(), y("x"))]), sub("b", 0, &[("b/models/s.yml".into(), y("y"))])]);
        let s = &t.findings("SSC-EWI-DBTPRJ0019")[0];
        assert_eq!(s.context["class"].as_str(), Some("consolidate"));
        assert!(s.message.contains("same generated placeholders (`YOUR_DB`.`YOUR_SCHEMA`)"), "{}", s.message);
        let r = &s.remediation;
        assert!(r.contains("Keep the `raw` entry at a/models/s.yml:2 as the single declaration.") && r.contains("move `y` from b/models/s.yml:2"), "{r}");
        assert!(r.contains("If the real per-project locations differ, rename instead") && r.contains("do not guess"), "{r}");
        assert!(r.contains("No model calls `source()`"), "{r}");
        assert!(!r.contains("var(") && !r.contains("--target"), "{r}");
    }

    #[test]
    fn prj0019_drops_tables_a_model_writes() {
        let y = |t: &str| format!("sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: {t}\n      - name: w\n");
        let v = "sources:\n  - name: raw\n    database: RAW\n    schema: S\n    tables:\n      - name: v\n";
        let naming = "{% macro generate_schema_name(custom_schema_name, node) %}{{ custom_schema_name }}{% endmacro %}";
        let a = || ("a/models/s.yml".to_string(), y("x"));
        let ar = || ("a/models/r.sql".to_string(), "select * from {{ source('raw', 'x') }}".to_string());
        // `w` is in both entries and only its name matches a model, whose
        // database and schema are the target's: kept, with a check note.
        let t = proj(vec![sub("a", 0, &[a(), ar()]), sub("b", 0, &[("b/models/s.yml".into(), y("y")), ("b/models/w.sql".into(), "select 1 as c".into())])]);
        let r = &t.findings("SSC-EWI-DBTPRJ0019")[0].remediation;
        assert!(r.contains("move `y` from b/models/s.yml:2") && !r.contains("Remove `"), "{r}");
        assert!(r.contains("can't be shown to be one relation: `w` and b/models/w.sql (database is `RAW`"), "{r}");
        // Verified identity schema naming writes RAW.S.v, so the unused source is dropped.
        let w = "{{ config(database='RAW', schema='S') }}\nselect 1 as c";
        let t = proj(vec![sub("a", 0, &[a(), ar()]), sub("b", 0, &[("b/macros/naming.sql".into(), naming.into()), ("b/models/s.yml".into(), v.into()), ("b/models/v.sql".into(), w.into())])]);
        let r = &t.findings("SSC-EWI-DBTPRJ0019")[0].remediation;
        assert!(r.contains("Remove `v` (written by b/models/v.sql) from the sources rather than keeping or moving it, because it is the relation that model writes"), "{r}");
        assert!(r.contains("delete the `raw` entry at b/models/s.yml:2") && !r.contains("only as generated"), "{r}");
        // Same name in another database: another table, moved without a note.
        let w = "{{ config(database='OTHER', schema='S') }}\nselect 1 as c";
        let t = proj(vec![sub("a", 0, &[a(), ar()]), sub("b", 0, &[("b/models/s.yml".into(), v.into()), ("b/models/v.sql".into(), w.into())])]);
        let r = &t.findings("SSC-EWI-DBTPRJ0019")[0].remediation;
        assert!(r.contains("move `v` from") && !r.contains("Remove `v`") && !r.contains("`v` and b/models/v.sql"), "{r}");
        // Still read through source(): moved, not dropped.
        let w = "{{ config(database='RAW', schema='S') }}\nselect 1 as c";
        let t = proj(vec![
            sub("a", 0, &[a(), ar()]),
            sub("b", 0, &[("b/models/s.yml".into(), v.into()), ("b/models/v.sql".into(), w.into()), ("b/models/u.sql".into(), "select * from {{ source('raw', 'v') }}".into())]),
        ]);
        let r = &t.findings("SSC-EWI-DBTPRJ0019")[0].remediation;
        assert!(r.contains("move `v` from") && !r.contains("Remove `v`"), "{r}");
        // A table of the kept entry that a model writes is removed as well.
        let t = proj(vec![
            sub("a", 0, &[a(), ar(), ("a/macros/naming.sql".into(), naming.into()), ("a/models/w.sql".into(), "{{ config(database='RAW', schema='S') }}\nselect 1 as c".into())]),
            sub("b", 0, &[("b/models/s.yml".into(), v.into())]),
        ]);
        let r = &t.findings("SSC-EWI-DBTPRJ0019")[0].remediation;
        assert!(r.contains("Remove `w` (written by a/models/w.sql)") && r.contains("move `v` from"), "{r}");
    }

    #[test]
    fn prj0019_fixtures() {
        let run = |rel: &str| {
            let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures").join(rel);
            let mut p = crate::discovery::build_portfolio(&root);
            crate::engine::run_audit(&mut p).suggestions.into_iter().filter(|s| s.rule_id.ends_with("PRJ0019")).collect::<Vec<_>>()
        };
        let c = run("cisco_estate");
        assert_eq!(c.len(), 1, "{c:#?}");
        assert_eq!((c[0].context["class"].as_str(), c[0].file.as_str(), c[0].line), (Some("consolidate"), "cisco_audit_cost/models/sources.yml", Some(3)));
        let r = &c[0].remediation;
        assert!(r.contains("only as generated") || c[0].message.contains("only as generated"), "{}", c[0].message);
        assert!(r.contains("PRJ0021 covers those reads") && r.contains("If the real per-project locations differ"), "{r}");
        // Configured placeholders do not prove the rendered producer schema.
        assert!(r.contains("can't be shown to be one relation"), "{r}");
        assert!(!r.contains("Remove `MT_RSTD_BKGS_MSR_ANNUITY`"), "{r}");
        assert!(r.contains("`WI_BKGS_MSR_ANNUITY_PRDT_AMORZ` and cisco_services_annuity/models/m_MT_RSTD_BKGS_MSR_ANNUITY/marts/WI_BKGS_MSR_ANNUITY_PRDT_AMORZ_12.sql"), "{r}");
        assert!(r.contains("`MT_PRODUCT_HWSW_ANNUITY_PDT`") && r.contains("from cisco_services_annuity/models/sources.yml:3 into it"), "{r}");
        let i = run("snowconvert/Informatica");
        assert_eq!((i.len(), i[0].context["class"].as_str()), (1, Some("consolidate")), "{i:#?}");
        let e = run("ewi_estate");
        assert_eq!((e.len(), e[0].context["class"].as_str()), (1, Some("unresolved")), "{e:#?}");
        // The location policy: no var-driven location, no orchestration advice.
        for s in c.iter().chain(&i).chain(&e) {
            assert!(!s.remediation.contains("var(") && !s.remediation.contains("--target"), "{}", s.remediation);
        }
    }

    #[test]
    fn new_prj0020() {
        // Identical copies across projects: one finding, delete the second.
        let t = proj(vec![sub("a", 1, &[]), sub("b", 1, &[])]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1);
        assert_eq!((f[0].file.as_str(), f[0].level.as_str(), f[0].context["class"].as_str()), ("b/models/m0.sql", "warning", Some("consolidate")));
        assert!(f[0].message.contains("a/models/m0.sql:1") && f[0].message.contains("b/models/m0.sql:1"), "{}", f[0].message);
        assert!(f[0].remediation.contains("Keep `a/models/m0.sql` and delete `b/models/m0.sql`") && f[0].remediation.contains("No `ref()` call changes"), "{}", f[0].remediation);
        // Clean: different names, nothing shared.
        let t = proj(vec![sub("a", 1, &[]), sub("b", 0, &[("b/models/z.sql".into(), "select 1".into())])]);
        assert!(t.findings("SSC-EWI-DBTPRJ0020").is_empty());
    }

    fn files(f: &[(&str, &str)]) -> TempProject {
        TempProject::new(f)
    }

    #[test]
    fn prj0020_rename_within_project_maps_refs_by_folder() {
        let t = files(&[
            ("models/m_A/staging/stg_x.sql", "{{ config(tags=['m_A']) }}\nselect 1 as a"),
            ("models/m_B/staging/stg_x.sql", "{{ config(tags=['m_B']) }}\nselect 2 as b"),
            ("models/m_A/marts/a_out.sql", "{{ config(tags=['m_A']) }}\nselect * from {{ ref('stg_x') }}"),
            ("models/m_B/marts/b_out.sql", "{{ config(tags=['m_B']) }}\nselect *\nfrom {{ ref('stg_x') }}"),
            ("models/shared.sql", "select * from {{ ref('stg_x') }}"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        let s = &f[0];
        assert_eq!((s.level.as_str(), s.context["class"].as_str(), s.file.as_str()), ("error", Some("rename"), "models/m_B/staging/stg_x.sql"));
        assert!(s.message.contains("dbt refuses to load it"), "{}", s.message);
        let r = &s.remediation;
        assert!(r.contains("rename `models/m_B/staging/stg_x.sql` to `models/m_B/staging/m_B__stg_x.sql`"), "{r}");
        assert!(r.contains("`ref('m_B__stg_x')` at models/m_B/marts/b_out.sql:3"), "{r}");
        assert!(!r.contains("a_out.sql"), "the m_A ref stays: {r}");
        assert!(r.contains("could mean either copy") && r.contains("models/shared.sql:1"), "{r}");
    }

    #[test]
    fn prj0020_rename_across_projects_lists_refs() {
        let t = TempProject::new(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
            ("a/models/stg.sql", "select 1 as a"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
            ("b/models/stg.sql", "select 2 as b"),
            ("b/models/use.sql", "select * from {{ ref('stg') }}"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1);
        assert_eq!((f[0].level.as_str(), f[0].file.as_str()), ("warning", "b/models/stg.sql"));
        assert!(f[0].message.contains("collide once the projects are merged"), "{}", f[0].message);
        assert!(f[0].remediation.contains("to `b/models/b__stg.sql`") && f[0].remediation.contains("`ref('b__stg')` at b/models/use.sql:1"), "{}", f[0].remediation);
    }

    #[test]
    fn prj0020_qualified_refs_follow_owner_not_caller_folder() {
        let t = files(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
            ("a/models/m_A/x.sql", "select 1 as a"),
            ("a/models/m_A/use_b.sql", "select * from {{ ref('b', 'x') }}"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
            ("b/models/m_B/x.sql", "select 2 as b"),
            ("b/models/m_B/use_a.sql", "select * from {{ ref('a', 'x') }}"),
            ("b/models/local_use.sql", "select * from {{ ref('x') }}"),
            ("b/macros/external.sql", "{% macro external() %}{{ ref('outside', 'x') }}{% endmacro %}"),
            ("c/dbt_project.yml", "name: c\nversion: '1.0'\nprofile: p\n"),
            ("c/macros/read_b.sql", "{% macro read_b() %}\n{{ ref('b', 'x') }}\n{% endmacro %}"),
            ("c/models/schema.yml", "models:\n  - name: report\n    description: \"{{ ref('b', 'x') }}\"\n"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        let rem = &f[0].remediation;
        assert!(rem.contains("`ref('b', 'x')` to `ref('b', 'b__x')` at a/models/m_A/use_b.sql:1, c/macros/read_b.sql:2, c/models/schema.yml:3"), "{rem}");
        assert!(rem.contains("`ref('x')` to `ref('b__x')` at b/models/local_use.sql:1"), "{rem}");
        assert!(!rem.contains("use_a.sql") && !rem.contains("external.sql"), "{rem}");
    }

    #[test]
    fn prj0020_qualified_external_ref_cannot_infer_duplicate_owner_from_folder() {
        let t = files(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
            ("a/models/m_B/use_b.sql", "select * from {{ ref('b', 'x') }}"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
            ("b/models/m_A/x.sql", "select 1 as a"),
            ("b/models/m_B/x.sql", "select 2 as b"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        let rem = &f[0].remediation;
        assert!(rem.contains("`ref('b', 'x')` at a/models/m_B/use_b.sql:1 (the owning package has multiple copies)"), "{rem}");
        assert!(!rem.contains("`ref('b', 'm_B__x')`"), "{rem}");
    }

    #[test]
    fn prj0020_consolidate_accounts_for_qualified_refs_to_dropped_package() {
        let t = files(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
            ("a/models/x.sql", "select 1 as a"),
            ("a/models/read_b.sql", "select * from {{ ref('b', 'x') }}"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
            ("b/models/x.sql", "select 1 as a"),
            ("b/models/read_a.sql", "select * from {{ ref('a', 'x') }}"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        assert_eq!(f[0].context["class"], "consolidate");
        assert!(f[0].remediation.contains("`ref('b', 'x')` to `ref('x')` at a/models/read_b.sql:1"), "{f:#?}");
        assert!(!f[0].remediation.contains("read_a.sql"), "{f:#?}");
    }

    #[test]
    fn prj0020_mixed_component_reports_each_writer_without_deletion_advice() {
        let t = files(&[
            ("models/m_A/x.sql", "{{ config(alias='T') }} select 1 as k"),
            ("models/m_B/x.sql", "{{ config(alias='U') }} select 2 as k"),
            ("models/m_C/z.sql", "{{ config(alias='T') }} select 3 as k"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        assert_eq!(f[0].context["class"], "unresolved");
        for (path, relation) in [("m_A/x", "T"), ("m_B/x", "U"), ("m_C/z", "T")] {
            assert!(f[0].message.contains(&format!("models/{path}.sql:1 writes `<target database>.<target schema>.{relation}`")), "{f:#?}");
        }
        assert!(f[0].remediation.contains("Retain all writers and their logic") && f[0].remediation.contains("before renaming or deleting"), "{f:#?}");
    }

    #[test]
    fn prj0020_merge_same_name_pinned_relation() {
        let y = format!("{HEAD}vars:\n  t: OUT_T\n");
        let t = pv(&y, &[
            ("models/m_A/out.sql", "{{ config(materialized='table',\n  alias=var('t')) }}\nselect 1 as a"),
            ("models/m_B/out.sql", "{{ config(materialized='table',\n  alias=var('t')) }}\nselect 2 as a"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1);
        let s = &f[0];
        assert_eq!((s.level.as_str(), s.context["class"].as_str(), s.line), ("error", Some("merge"), Some(2)));
        assert!(s.message.contains("models/m_A/out.sql:2") && s.message.contains("models/m_B/out.sql:2") && s.message.contains("OUT_T"), "{}", s.message);
        assert!(s.message.contains("materialized='table'") && s.message.contains("dbt Fusion stops at parse"), "{}", s.message);
        assert!(s.remediation.contains("Combine the writers") && s.remediation.contains("load order and truncate"), "{}", s.remediation);
    }

    #[test]
    fn prj0020_merge_different_names_one_relation() {
        let t = files(&[
            ("models/w1.sql", "{{ config(alias='HIER') }}\nselect 1 as a"),
            ("models/w2.sql", "{{ config(alias='hier') }}\nselect 2 as a"),
            ("models/w3.sql", "{{ config(alias='OTHER') }}\nselect 3 as a"),
            ("models/r.sql", "select * from {{ ref('w2') }}"),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0020");
        assert_eq!(f.len(), 1, "{f:#?}");
        let s = &f[0];
        assert_eq!((s.level.as_str(), s.context["class"].as_str(), s.file.as_str()), ("warning", Some("merge"), "models/w1.sql"));
        assert!(s.message.starts_with("2 models write one relation") && !s.message.contains("w3"), "{}", s.message);
        assert!(s.remediation.contains("models/r.sql:1"), "{}", s.remediation);
        // Placeholder locations merge only as generated.
        let y = format!("{HEAD}vars:\n  d: YOUR_DB\n");
        let t = pv(&y, &[
            ("models/w1.sql", "{{ config(alias='HIER', database=var('d')) }}\nselect 1 as a"),
            ("models/w2.sql", "{{ config(alias='HIER', database=var('d')) }}\nselect 2 as a"),
        ]);
        assert!(t.findings("SSC-EWI-DBTPRJ0020")[0].remediation.contains("only as generated"));
    }

    #[test]
    fn sql0002_skips_copies_prj0020_deletes() {
        let m = "with base as (\n  select a,\n    b,\n    c,\n    d\n  from t\n)\nselect * from base";
        let t = proj(vec![
            sub("a", 0, &[("a/models/x.sql".into(), m.into())]),
            sub("b", 0, &[("b/models/x.sql".into(), m.into())]),
        ]);
        assert_eq!(cnt(&t, "SSC-EWI-DBTPRJ0020"), 1);
        assert!(t.findings("SSC-EWI-DBTSQL0002").iter().all(|s| s.context.get("cross_project").is_none()));
        // A different model still shares the CTE across projects.
        let t = proj(vec![
            sub("a", 0, &[("a/models/x.sql".into(), m.into())]),
            sub("b", 0, &[("b/models/y.sql".into(), m.into())]),
        ]);
        assert!(t.findings("SSC-EWI-DBTSQL0002").iter().any(|s| s.context.get("cross_project").is_some()));
    }

    #[test]
    fn prj0020_cisco_groups() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/cisco_estate");
        let mut p = crate::discovery::build_portfolio(&root);
        let f: Vec<_> = crate::engine::run_audit(&mut p).suggestions.into_iter().filter(|s| s.rule_id.ends_with("PRJ0020")).collect();
        let got: Vec<(&str, &str, &str)> = f.iter().map(|s| (s.context["model"].as_str().unwrap(), s.context["class"].as_str().unwrap(), s.level.as_str())).collect();
        assert_eq!(
            got.iter().copied().collect::<BTreeSet<_>>(),
            BTreeSet::from([
                ("MT_RSTD_BKGS_BY_QUARTER1", "merge", "error"),
                ("stg_raw__SQ_WI2_RSTD_BKGS_ORDER_MTH", "rename", "error"),
                ("stg_raw__SQ_MT_RSTD_BKGS_MEASURE", "rename", "warning"),
            ]),
            "{f:#?}"
        );
        let wi2 = f.iter().find(|s| s.context["model"] == "stg_raw__SQ_WI2_RSTD_BKGS_ORDER_MTH").unwrap();
        // The m_WI_RSTD_BKGS_MEASURE copy is renamed and its own caller moves; the m_WI2 caller stays.
        assert!(wi2.remediation.contains("WI_RSTD_BKGS_MEASURE_ORDER_MTH2.sql:221"), "{}", wi2.remediation);
        assert!(!wi2.remediation.contains("WI2_RSTD_BKGS_ORDER_MTH1.sql:120"), "{}", wi2.remediation);
        let x = f.iter().find(|s| s.context["model"] == "stg_raw__SQ_MT_RSTD_BKGS_MEASURE").unwrap();
        assert!(x.remediation.contains("WI1_RSTD_BKGS_BY_QUARTER1.sql:80"), "{}", x.remediation);
    }

    #[test]
    fn prj0020_informatica_groups() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/snowconvert/Informatica");
        let mut p = crate::discovery::build_portfolio(&root);
        let f: Vec<_> = crate::engine::run_audit(&mut p).suggestions.into_iter().filter(|s| s.rule_id.ends_with("PRJ0020")).collect();
        // Every project is named YOUR_PROJECT_NAME, so a rename uses the project folder.
        assert!(f.iter().all(|s| !s.remediation.contains("YOUR_PROJECT_NAME__")), "{f:#?}");
        // The CORP and NON_CORP copies pin one alias: one relation once merged.
        let q = f.iter().find(|s| s.context["model"] == "MT_RSTD_BKGS_BY_QUARTER1").unwrap();
        assert_eq!((q.context["class"].as_str(), q.level.as_str()), (Some("merge"), "warning"), "{q:#?}");
        let x = f.iter().find(|s| s.context["model"] == "stg_raw__SQ_MT_RSTD_BKGS_MEASURE").unwrap();
        assert!(x.remediation.contains("m_WI1_RSTD_BKGS_BY_QUARTER__stg_raw__SQ_MT_RSTD_BKGS_MEASURE"), "{}", x.remediation);
    }

    #[test]
    fn new_prj0021() {
        let prod = ("a/models/orders_out.sql".to_string(), "{{ config(alias=var('t')) }}\nselect 1".to_string());
        let ayml = "name: a\nversion: '1.0'\nprofile: p\nvars:\n  t: ORDERS_T\n".to_string();
        let cons = ("b/models/use.sql".to_string(), "select * from {{ var('db') }}.ORDERS_T o".to_string());
        let t = TempProject::new(&[
            ("a/dbt_project.yml", ayml.as_str()), (prod.0.as_str(), prod.1.as_str()),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"), (cons.0.as_str(), cons.1.as_str()),
        ]);
        let f = t.findings("SSC-EWI-DBTPRJ0021");
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].file, "b/models/use.sql");
        assert_eq!(f[0].context["class"], "unresolved");
        assert!(f[0].context["producer_files"].to_string().contains("orders_out.sql"));
        let clean = "select * from {{ ref('orders_out') }} o, 'x.ORDERS_T' as s";
        let t = TempProject::new(&[
            ("a/dbt_project.yml", ayml.as_str()), (prod.0.as_str(), prod.1.as_str()),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"), ("b/models/use.sql", clean),
        ]);
        assert!(t.findings("SSC-EWI-DBTPRJ0021").is_empty());
    }

    #[test]
    fn new_prj0018() {
        let y = format!("{HEAD}vars:\n  k: 1\n  demo:\n    k: 2\n");
        assert_eq!(cnt(&pv(&y, &[("models/a.sql", "select {{ var('k') }}")]), "SSC-EWI-DBTPRJ0018"), 1);
        let y = format!("{HEAD}vars:\n  k: 1\n  k: 2\n");
        assert_eq!(cnt(&pv(&y, &[]), "SSC-EWI-DBTPRJ0018"), 1);
        let y = format!("{HEAD}vars:\n  k: 1\n  demo:\n    k: 1\n");
        assert_eq!(cnt(&pv(&y, &[]), "SSC-EWI-DBTPRJ0018"), 0);
    }
}
