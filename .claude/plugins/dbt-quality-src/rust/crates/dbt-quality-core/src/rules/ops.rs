//! OPS rules: operational checks and observability.

use std::path::{Path, PathBuf};

use serde_json::{json, Value};

use crate::discovery::ProjectContext;
use crate::engine::{Detect, Detector};
use crate::model::{effort, level, Suggestion};
use crate::sqlutil::{py_str, span, strip_comments_and_strings, truthy};
use crate::{frx, rx};

const ARTIFACTS: &str = "SSC-EWI-DBTOPS0001";
const CREDENTIALS: &str = "SSC-EWI-DBTOPS0002";
const EVALUATOR: &str = "SSC-EWI-DBTOPS0003";
const RUN_NOT_BUILD: &str = "SSC-EWI-DBTOPS0004";

pub const DETECTORS: &[Detector] = &[
    Detector { code: ARTIFACTS, detect: Detect::Project(artifacts_contradiction) },
    Detector { code: CREDENTIALS, detect: Detect::Project(credentials) },
    Detector { code: EVALUATOR, detect: Detect::Project(evaluator_config) },
    Detector { code: RUN_NOT_BUILD, detect: Detect::Project(run_not_build) },
    Detector { code: "SSC-EWI-DBTOPS0005", detect: Detect::Project(instrumentation_hooks) },
    Detector { code: "SSC-EWI-DBTOPS0006", detect: Detect::Project(run_hooks_with_work) },
    Detector { code: "SSC-EWI-DBTOPS0007", detect: Detect::Portfolio(runtime_vars) },
];

fn as_list(v: &Value) -> Vec<&Value> {
    match v {
        Value::Array(a) => a.iter().collect(),
        v => vec![v],
    }
}

fn walk_instrumented(node: &Value, path: &mut Vec<String>, out: &mut Vec<(Vec<String>, String)>) {
    let Value::Object(map) = node else { return };
    let hook = ["+post-hook", "+post_hook"].iter().find_map(|k| map.get(*k).map(|v| (*k, v)));
    if let Some((key, v)) = hook {
        let table = map.get("+materialized").map(py_str).as_deref() == Some("table");
        let reg = as_list(v).into_iter().map(py_str).find(|h| rx!(r"\bm_register_\w+").is_match(h));
        let mart = path.last().is_some_and(|p| p.to_lowercase().contains("mart"));
        if let (true, Some(h), false) = (table, reg, mart) {
            let mut p = path.clone();
            p.push(key.to_string());
            out.push((p, h));
        }
    }
    for (k, v) in map {
        if !k.starts_with('+') {
            path.push(k.clone());
            walk_instrumented(v, path, out);
            path.pop();
        }
    }
}

fn instrumentation_hooks(project: &ProjectContext) -> Vec<Suggestion> {
    let mut found = vec![];
    if let Some(models) = project.project_yml.get("models") {
        walk_instrumented(models, &mut vec!["models".to_string()], &mut found);
    }
    found
        .into_iter()
        .map(|(keys, hook)| {
            let scope = keys[..keys.len() - 1].join("/");
            Suggestion::new("SSC-EWI-DBTOPS0005", format!("`{scope}` combines an `m_register_*` post-hook with `+materialized: table`. Review the hook's actual work and the intended materialization."))
                .file("dbt_project.yml")
                .evidence(hook.trim().to_string())
                .remediation("Inspect the metrics macro and each model's effective materialization. Remove temporary instrumentation only after preserving required validation evidence. Restore the intended materializations. Consider run-level logging only if it preserves the required per-model information and timing; keep justified production metrics.")
                .effort(effort::MEDIUM)
                .ctx("yaml_keys", json!(keys))
        })
        .collect()
}

fn run_hooks_with_work(project: &ProjectContext) -> Vec<Suggestion> {
    let work = rx!(r"(?i)^\s*(create|alter|drop|insert|update|delete|merge|grant|revoke|truncate|copy|call|put|use)\b");
    let work_in = rx!(r"(?i)\b(create|alter|drop|insert\s+into|update\s+\S+\s+set|delete\s+from|merge\s+into|grant|revoke|truncate|copy\s+into|call)\b");
    let mut out = vec![];
    for key in ["on-run-start", "on-run-end"] {
        let Some(v) = project.project_yml.get(key) else { continue };
        for h in as_list(v) {
            let text = py_str(h);
            let t = text.trim();
            if t.is_empty() || t.contains("dbt_artifacts.") {
                continue;
            }
            let (lvl, how) = if work.is_match(t) {
                (level::WARNING, "runs".to_string())
            } else if let Some(c) = rx!(r"^\{\{-?\s*([A-Za-z_][\w.]*)\s*\(").captures(t) {
                let name = c[1].rsplit('.').next().unwrap_or("").to_string();
                let body = project
                    .macros
                    .iter()
                    .flat_map(|m| m.macros.iter())
                    .find(|m| m.name == name)
                    .map(|m| strip_comments_and_strings(&m.body));
                if !body.is_some_and(|b| work_in.is_match(&b)) {
                    continue;
                }
                (level::INFORMATION, format!("calls macro `{name}`, which runs"))
            } else {
                continue;
            };
            out.push(
                Suggestion::new("SSC-EWI-DBTOPS0006", format!("`{key}` {how} DDL or DML."))
                    .level(lvl)
                    .file("dbt_project.yml")
                    .evidence(t.chars().take(200).collect::<String>())
                    .remediation("Prefer models for business transformations with dependencies and tests. Keep justified setup, grants, or logging in hooks and document side effects and retries. An explicit `dbt run-operation` can handle a separate administrative action, but orchestration must order it; it does not create a model node.")
                    .effort(effort::MEDIUM)
                    .ctx("yaml_keys", json!([key])),
            );
        }
    }
    out
}

fn runtime_vars(p: &crate::discovery::PortfolioContext) -> Vec<Suggestion> {
    let exec = rx!(r"(?i)\bEXECUTE\s+DBT\s+PROJECT\b");
    let direct = rx!(r"(?i)--vars\s*'+\s*\|\|\s*([A-Za-z_][\w.]*)\s*(\()?");
    let mut out = vec![];
    for path in crate::discovery::iter_files(&p.root, &[".sql"]) {
        let Some(text) = read_text(&path) else { continue };
        if !exec.is_match(&text) {
            continue;
        }
        for c in direct.captures_iter(&text) {
            let name = &c[1];
            let is_call = c.get(2).is_some();
            let assigned = format!(r"(?i)\b{}\b[^;:=]*:=\s*[A-Za-z_][\w.]*\s*\(", regex::escape(name));
            if !is_call && !regex::Regex::new(&assigned).is_ok_and(|r| r.is_match(&text)) {
                continue;
            }
            let m = c.get(0).unwrap();
            let rel = crate::discovery::display_path(path.strip_prefix(&p.root).unwrap_or(&path));
            let mut s = Suggestion::new("SSC-EWI-DBTOPS0007", format!("`{rel}` builds `--vars` for `EXECUTE DBT PROJECT` from a function result at run time."))
                .file(rel)
                .span(span(&text, m.start(), m.end()))
                .evidence(m.as_str())
                .remediation("Use declared defaults for stable inputs. Keep necessary per-run variables with documented meaning, validation, and a non-secret audit record. Serialize them with a structured format and check command quoting. dbt supports runtime variables; this finding asks for reproducibility, not their removal.")
                .effort(effort::MEDIUM)
                .ctx("var_name", json!(name));
            if let Some(pr) = p.projects.first() {
                s = s.project(pr.label.clone());
            }
            out.push(s);
            break;
        }
    }
    out
}

/// Read a file like Python `read_text`: lossy UTF-8 and universal newlines.
fn read_text(path: &Path) -> Option<String> {
    let text = crate::discovery::read_source(path, true).ok()?;
    Some(text.replace("\r\n", "\n").replace('\r', "\n"))
}

/// Find a config key anywhere in a nested tree. Return its value.
fn find_flag(node: &Value, key: &str) -> Value {
    if let Value::Object(map) = node {
        for (k, v) in map {
            if k.trim_start_matches('+') == key {
                return v.clone();
            }
            let found = find_flag(v, key);
            if !found.is_null() {
                return found;
            }
        }
    }
    Value::Null
}

fn declared_packages(project: &ProjectContext) -> Vec<String> {
    match project.packages.get("packages") {
        Some(Value::Array(a)) => a
            .iter()
            .filter_map(|p| p.as_object())
            .map(|p| {
                let s = p.get("package").map(py_str).unwrap_or_default();
                s.rsplit('/').next().unwrap_or("").to_string()
            })
            .collect(),
        _ => vec![],
    }
}

fn artifacts_contradiction(project: &ProjectContext) -> Vec<Suggestion> {
    if !declared_packages(project).iter().any(|p| p == "dbt_artifacts") {
        return vec![];
    }
    let hooks: Vec<Value> = match project.project_yml.get("on-run-end") {
        Some(Value::Array(a)) => a.clone(),
        Some(v) if truthy(Some(v)) => vec![v.clone()],
        _ => vec![],
    };
    let has_hook = hooks.iter().any(|h| py_str(h).contains("dbt_artifacts"));
    let artifacts_enabled = project
        .project_yml
        .get("models")
        .and_then(|m| m.get("dbt_artifacts"))
        .filter(|n| n.is_object())
        .map(|n| find_flag(n, "enabled"))
        .unwrap_or(Value::Null);

    if has_hook && artifacts_enabled == Value::Bool(false) {
        return vec![Suggestion::new(
            ARTIFACTS,
            "An `enabled: false` setting was found under `dbt_artifacts` while its upload hook is active. Check effective configuration; enabled raw sources with disabled marts can be valid.",
        )
        .file("dbt_project.yml")
        .ctx("yaml_keys", json!(["models", "dbt_artifacts", "enabled"]))
        .evidence("on-run-end references dbt_artifacts; models.dbt_artifacts.+enabled: false")
        .remediation(
            "Check the installed package's configuration and upload tables first. A sources-only setup can be valid with marts disabled. If required upload tables are absent, enable and build the required resources. To disable uploads entirely, remove the hook. Do not enable every package model just to silence this finding.",
        )
        .effort(effort::LOW)];
    }
    if has_hook {
        return vec![];
    }
    let shown = if hooks.is_empty() { "absent".to_string() } else { py_str(&Value::Array(hooks)) };
    vec![Suggestion::new(ARTIFACTS, "`dbt_artifacts` is installed but has no `on-run-end` upload hook.")
        .level(level::INFORMATION)
        .file("dbt_project.yml")
        .ctx("yaml_keys", json!(["on-run-end"]))
        .evidence(format!("packages include dbt_artifacts; on-run-end: {shown}"))
        .remediation(
            "Add the hook to `dbt_project.yml`:\n\n```yaml\non-run-end:\n  - \"{{ dbt_artifacts.upload_results(results) }}\"\n```\n\n\
             Create the required package tables first. If uploads should run only in production, use the actual deployment target names and verify the hook's command timing and result handling.",
        )
        .effort(effort::LOW)]
}

fn credentials(project: &ProjectContext) -> Vec<Suggestion> {
    let re = frx!(
        r#"(?mi)^\s*(password|private_key_passphrase|token|secret|access_key)\s*:\s*(?!\s*$)(?!["']?\s*(?:\{\{|\$))\S"#
    );
    let mut out = vec![];
    for name in ["profiles.yml", "profiles.yaml", "dbt_project.yml"] {
        let path = project.root.join(name);
        if !path.is_file() {
            continue;
        }
        let Some(content) = read_text(&path) else { continue };
        let Ok(Some(caps)) = re.captures(&content) else { continue };
        let g = caps.get(1).unwrap();
        out.push(
            Suggestion::new(CREDENTIALS, format!("`{name}` contains a literal `{}` value.", g.as_str()))
                .file(name)
                .span(span(&content, g.start(), g.end()))
                .evidence(format!("{}: <redacted>", g.as_str()))
                .remediation(
                    "Replace the literal value with an environment variable: \
                     `password: \"{{ env_var('SNOWFLAKE_PASSWORD') }}\"`. \
                     For secrets in profiles.yml, consider a `DBT_ENV_SECRET_*` variable supported by dbt; do not use secret-prefixed variables in model SQL or project configuration. Configure key-pair authentication through the supported dbt adapter profile if needed. If a real credential was exposed, rotate it and review Git history; this scan does not prove the value was committed.",
                )
                .effort(effort::MEDIUM),
        );
    }
    out
}

fn evaluator_config(project: &ProjectContext) -> Vec<Suggestion> {
    if !declared_packages(project).iter().any(|p| p == "dbt_project_evaluator") {
        return vec![];
    }
    let variables = project.project_yml.get("vars").filter(|v| truthy(Some(v)));
    let ev = variables.and_then(|v| v.get("dbt_project_evaluator"));
    if let Some(Value::Object(o)) = ev
        && truthy(o.get("primary_key_test_macros")) {
            return vec![];
        }
    let vars_text = match variables {
        Some(v) => py_str(v),
        None => "{}".to_string(),
    };
    if vars_text.contains("primary_key_test_macros") {
        return vec![];
    }
    vec![Suggestion::new(
        EVALUATOR,
        "`dbt_project_evaluator` is installed but `primary_key_test_macros` is not configured in `vars`.",
    )
    .file("dbt_project.yml")
    .ctx("yaml_keys", json!(["vars"]))
    .ctx("related_files", json!(package_line(project, "dbt_project_evaluator").map(|l| vec![format!("packages.yml:{l}")]).unwrap_or_default()))
    .evidence("vars.dbt_project_evaluator.primary_key_test_macros absent")
    .remediation(
        "Check the installed evaluator defaults first. If they miss the key tests your project uses, extend `primary_key_test_macros` under `vars: dbt_project_evaluator:`. Preserve required defaults; the example is not a complete replacement for every project:\n\n\
         ```yaml\nvars:\n  dbt_project_evaluator:\n    primary_key_test_macros:\n      \
         [[\"dbt_constraints.test_primary_key\"],\n       \
         [\"dbt_constraints.test_unique_key\", \"dbt.test_not_null\"],\n       \
         [\"dbt.test_unique\", \"dbt.test_not_null\"]]\n```",
    )
    .effort(effort::LOW)]
}

/// 1-based line in `packages.yml` that names `package`.
fn package_line(project: &ProjectContext, package: &str) -> Option<u32> {
    let text = read_text(&project.root.join("packages.yml"))?;
    text.lines().position(|l| l.contains(package)).map(|i| i as u32 + 1)
}

/// `text` with each `#` comment replaced by spaces, so byte offsets stay the same.
fn mask_hash_comments(text: &str) -> String {
    text.split_inclusive('\n')
        .map(|line| match line.find('#') {
            Some(i) => {
                let tail: String = line[i..].chars().map(|c| if c == '\n' { c } else { ' ' }).collect();
                format!("{}{}", &line[..i], tail)
            }
            None => line.to_string(),
        })
        .collect()
}

/// Files in `dir` whose extension is one of `exts`, sorted by name.
fn files_with_ext(dir: &Path, exts: &[&str]) -> Vec<PathBuf> {
    let Ok(rd) = std::fs::read_dir(dir) else { return vec![] };
    let mut v: Vec<PathBuf> = rd
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| {
            p.file_name()
                .and_then(|n| n.to_str())
                .is_some_and(|n| exts.iter().any(|x| n.ends_with(&format!(".{x}"))))
        })
        .collect();
    v.sort();
    v
}

fn run_not_build(project: &ProjectContext) -> Vec<Suggestion> {
    let root = &project.root;
    let wf = root.join(".github/workflows");
    let mut candidates = files_with_ext(root, &["yml"]);
    candidates.extend(files_with_ext(root, &["yaml"]));
    candidates.extend(files_with_ext(&wf, &["yml"]));
    candidates.extend(files_with_ext(&wf, &["yaml"]));
    candidates.extend(files_with_ext(root, &["sh"]));
    candidates.push(root.join("Makefile"));

    let run = rx!(r"\bdbt\s+run\b");
    let test = rx!(r"\bdbt\s+test\b");
    let mut out = vec![];
    for path in candidates {
        let fname = path.file_name().and_then(|n| n.to_str()).unwrap_or("").to_string();
        if !path.is_file() || ["dbt_project.yml", "packages.yml", "profiles.yml"].contains(&fname.as_str()) {
            continue;
        }
        let Some(raw) = read_text(&path) else { continue };
        // Comments do not run commands. A Makefile and YAML also use `#` comments.
        let content = mask_hash_comments(&raw);
        let Some(m) = run.find(&content) else { continue };
        if !test.is_match(&content) {
            continue;
        }
        let relative = crate::discovery::display_path(path.strip_prefix(root).unwrap_or(&path));
        out.push(
            Suggestion::new(RUN_NOT_BUILD, format!("`{fname}` runs `dbt run` and `dbt test` as separate steps."))
                .file(relative.clone())
                .span(span(&content, m.start(), m.end()))
                .ctx("related_files", json!([format!("{relative}:{}", span(&content, m.start(), m.end()).line)]))
                .evidence(m.as_str())
                .remediation(
                    "Consider `dbt build` to run selected models and tests in dependency order. Error-severity test failures can skip dependent nodes, subject to selection and multi-parent rules. Preserve required separate steps and failure handling. A successful build does not prove all business logic correct.",
                )
                .effort(effort::LOW),
        );
    }
    out
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const PROJ_HOOK_OFF: &str = "name: demo\nversion: '1.0'\nprofile: demo\non-run-end:\n  - \"{{ dbt_artifacts.upload_results(results) }}\"\nmodels:\n  dbt_artifacts:\n    +enabled: false\n";
    const PROJ_HOOK_ON: &str = "name: demo\nversion: '1.0'\nprofile: demo\non-run-end:\n  - \"{{ dbt_artifacts.upload_results(results) }}\"\n";
    const PKG_ART: &str = "packages:\n  - package: brooklyn-data/dbt_artifacts\n    version: 2.0.0\n";
    const PKG_EVAL: &str = "packages:\n  - package: dbt-labs/dbt_project_evaluator\n    version: 1.0.0\n";

    #[test]
    fn ops0001_fires() {
        let t = TempProject::new(&[("dbt_project.yml", PROJ_HOOK_OFF), ("packages.yml", PKG_ART)]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0001").len(), 1);
        let t = TempProject::new(&[("packages.yml", PKG_ART)]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0001").len(), 1);
    }

    #[test]
    fn ops0001_clean() {
        let t = TempProject::new(&[("dbt_project.yml", PROJ_HOOK_ON), ("packages.yml", PKG_ART)]);
        assert!(t.findings("SSC-EWI-DBTOPS0001").is_empty());
    }

    #[test]
    fn ops0002_fires() {
        let t = TempProject::new(&[("profiles.yml", "demo:\n  outputs:\n    dev:\n      password: hunter2\n")]);
        let f = t.findings("SSC-EWI-DBTOPS0002");
        assert_eq!(f.len(), 1);
    }

    #[test]
    fn ops0002_clean() {
        let t = TempProject::new(&[("profiles.yml", "demo:\n  outputs:\n    dev:\n      password: \"{{ env_var('PW') }}\"\n")]);
        assert!(t.findings("SSC-EWI-DBTOPS0002").is_empty());
    }

    #[test]
    fn ops0003_fires() {
        let t = TempProject::new(&[("packages.yml", PKG_EVAL)]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0003").len(), 1);
    }

    #[test]
    fn ops0003_clean() {
        let proj = "name: demo\nversion: '1.0'\nprofile: demo\nvars:\n  dbt_project_evaluator:\n    primary_key_test_macros: [[\"dbt.test_unique\"]]\n";
        let t = TempProject::new(&[("dbt_project.yml", proj), ("packages.yml", PKG_EVAL)]);
        assert!(t.findings("SSC-EWI-DBTOPS0003").is_empty());
    }

    #[test]
    fn ops0004_fires() {
        let t = TempProject::new(&[("ci.sh", "dbt run\ndbt test\n")]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0004").len(), 1);
    }

    #[test]
    fn ops0005() {
        let y = |m: &str| format!("name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    staging:\n      +materialized: {m}\n      +post-hook:\n        - \"{{{{ m_register_post_exec_metrics(this.name) }}}}\"\n");
        let t = TempProject::new(&[("dbt_project.yml", &y("table"))]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0005").len(), 1);
        let t = TempProject::new(&[("dbt_project.yml", &y("view"))]);
        assert!(t.findings("SSC-EWI-DBTOPS0005").is_empty());
    }

    #[test]
    fn ops0006() {
        let y = |h: &str| format!("name: demo\nversion: '1.0'\nprofile: demo\non-run-end:\n  - \"{h}\"\n");
        let t = TempProject::new(&[("dbt_project.yml", &y("insert into a.b select 1"))]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0006").len(), 1);
        let t = TempProject::new(&[("dbt_project.yml", &y("{{ log_it() }}")), ("macros/m.sql", "{% macro log_it() %}insert into a.b select 1{% endmacro %}")]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0006").len(), 1);
        let t = TempProject::new(&[("dbt_project.yml", &y("{{ dbt_artifacts.upload_results(results) }}"))]);
        assert!(t.findings("SSC-EWI-DBTOPS0006").is_empty());
    }

    #[test]
    fn ops0007() {
        let bad = "LET v VARCHAR := public.BuildVars('x');\nLET a VARCHAR := 'build --vars ''' || v || '''';\nEXECUTE DBT PROJECT p ARGS=:a;";
        let t = TempProject::new(&[("orch/p.sql", bad)]);
        assert_eq!(t.findings("SSC-EWI-DBTOPS0007").len(), 1);
        let t = TempProject::new(&[("orch/p.sql", "EXECUTE DBT PROJECT p ARGS='build';")]);
        assert!(t.findings("SSC-EWI-DBTOPS0007").is_empty());
    }

    #[test]
    fn ops0004_clean() {
        let t = TempProject::new(&[("ci.sh", "dbt build\n")]);
        assert!(t.findings("SSC-EWI-DBTOPS0004").is_empty());
    }

    #[test]
    fn ops0003_shows_packages_line() {
        let t = TempProject::new(&[("packages.yml", PKG_EVAL)]);
        let f = t.findings("SSC-EWI-DBTOPS0003");
        assert_eq!(f[0].context["related_files"], serde_json::json!(["packages.yml:2"]));
    }

    #[test]
    fn ops0004_skips_comment_line() {
        let sh = "#!/bin/sh\n# automation uses dbt run + dbt test separately\ndbt run --target prod\ndbt test --target prod\n";
        let t = TempProject::new(&[("run_prod.sh", sh)]);
        let f = t.findings("SSC-EWI-DBTOPS0004");
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].line, Some(3));
        assert_eq!(f[0].context["related_files"], serde_json::json!(["run_prod.sh:3"]));
        let t = TempProject::new(&[("run.sh", "# dbt run then dbt test\ndbt build\n")]);
        assert!(t.findings("SSC-EWI-DBTOPS0004").is_empty());
    }
}
