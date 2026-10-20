//! MAT rules: materialization checks.

use serde_json::{json, Map, Value};

use crate::discovery::{ModelFile, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural, Suggestion};
use crate::sqlutil::{py_repr, py_str, truthy};

/// Line of the first `key=` argument in the model's SQL, if any.
fn config_key_line(model: &ModelFile, key: &str) -> Option<u32> {
    let re = regex::Regex::new(&format!(r"\b{}\s*=", regex::escape(key))).ok()?;
    re.find_iter(&model.raw)
        .find(|m| {
            let ls = model.raw[..m.start()].rfind('\n').map_or(0, |i| i + 1);
            !model.raw[ls..m.start()].contains("--")
        })
        .map(|m| model.line_of(m.start()))
}

/// `dbt_project.yml` line of the deepest folder entry that sets `+key` for the model.
fn folder_key_line(model: &ModelFile, project: &ProjectContext, key: &str) -> Option<u32> {
    let Some(Value::Object(tree)) = project.project_yml.get("models") else { return None };
    let (root_key, mut node) = match tree.get(&project.name) {
        Some(Value::Object(n)) => (project.name.clone(), n),
        _ => {
            let c: Vec<(&String, &Map<String, Value>)> =
                tree.iter().filter(|(k, _)| !k.starts_with('+')).filter_map(|(k, v)| v.as_object().map(|o| (k, o))).collect();
            if c.len() != 1 {
                return None;
            }
            (c[0].0.clone(), c[0].1)
        }
    };
    let plus = format!("+{key}");
    let mut path = vec!["models".to_string(), root_key];
    let mut best = node.contains_key(&plus).then(|| path.clone());
    for seg in &model.segments {
        let Some(Value::Object(child)) = node.get(seg) else { break };
        node = child;
        path.push(seg.clone());
        if node.contains_key(&plus) {
            best = Some(path.clone());
        }
    }
    let mut keys = best?;
    keys.push(key.to_string());
    crate::anchors::project_yml_position(project, &keys).map(|(l, _)| l)
}

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-PRF-DBTMAT0001", detect: Detect::Model(ephemeral_fanout) },
    Detector { code: "SSC-PRF-DBTMAT0002", detect: Detect::Model(single_use_model) },
    Detector { code: "SSC-PRF-DBTMAT0004", detect: Detect::Model(clustering) },
    Detector { code: "SSC-EWI-DBTMAT0006", detect: Detect::Model(redundant_config) },
    Detector { code: "SSC-EWI-DBTMAT0007", detect: Detect::Project(no_folder_default) },
    Detector { code: "SSC-EWI-DBTMAT0008", detect: Detect::Model(config_gated_on_var) },
];

/// Report a `config()` call nested under an `{% if %}` that reads `var()`.
fn config_gated_on_var(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let var_sets: Vec<&str> = model
        .jinja
        .sets
        .iter()
        .filter(|s| matches!(&s.value, crate::jinja::Lit::Expr(e) if e.contains("var(")))
        .map(|s| s.target.as_str())
        .collect();
    for call in model.jinja.calls_named("config") {
        // INC0019 reports conditions that control hooks only. This rule checks conditions that control the build.
        let keys: Vec<&str> = call.kwargs.iter().map(|(k, _)| k.as_str()).filter(|k| MATERIALIZATION_KEYS.contains(k)).collect();
        if keys.is_empty() {
            continue;
        }
        for cond in &call.conditions {
            let via_set = var_sets.iter().find(|t| {
                crate::rx!(r"[A-Za-z_][A-Za-z0-9_]*").find_iter(cond).any(|m| m.as_str() == **t)
            });
            if !crate::rx!(r"\bvar\s*\(").is_match(cond) && via_set.is_none() {
                continue;
            }
            let cond = cond.trim();
            return vec![Suggestion::new(
                "SSC-EWI-DBTMAT0008",
                format!("`config()` in `{}` only applies when `{cond}`.", crate::discovery::root_relative(project, &model.relative_path)),
            )
            .file(&model.relative_path)
            .line(call.span.start_line)
            .evidence(format!("{{% if {cond} %}} ... config(...)"))
            .remediation(gated_remediation(&keys, &crate::discovery::root_relative(project, &model.relative_path)))
            .effort(effort::MEDIUM)
            .ctx("model", json!(model.name))];
        }
    }
    vec![]
}

/// Config keys that change what a model builds or how it loads.
const MATERIALIZATION_KEYS: &[&str] =
    &["materialized", "incremental_strategy", "unique_key", "enabled", "full_refresh", "on_schema_change", "transient"];

fn gated_remediation(keys: &[&str], file: &str) -> String {
    format!(
        "In `{file}`, review conditional `{}` settings in the `{{% if %}}` block. If they should be stable, use an unconditional `config()` or folder-level `+key:` settings. dbt permits variable-driven configuration; keep intentional conditions, document their inputs, and validate each supported branch.",
        keys.join("`, `")
    )
}

fn model_children(model: &ModelFile, project: &ProjectContext) -> Vec<String> {
    project
        .graph
        .child_names(&model.name)
        .into_iter()
        .filter(|c| project.model_by_name(c).is_some())
        .collect()
}

fn ephemeral_fanout(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let mat = model.materialization();
    if mat != "ephemeral" && mat != "view" {
        return vec![];
    }
    let children = model_children(model, project);
    if (children.len() as i64) < project.config.ephemeral_fanout_threshold {
        return vec![];
    }
    let mut sorted = children.clone();
    sorted.sort();
    let shown = sorted.iter().take(5).cloned().collect::<Vec<_>>().join(", ");
    let more = if children.len() > 5 { " ..." } else { "" };
    vec![Suggestion::new(
        "SSC-PRF-DBTMAT0001",
        format!(
            "This `{mat}` model has {n} detected downstream consumers ({shown}{more}). That can repeat query work; the count is not a measured execution count.",
            n = children.len()
        ),
    )
    .file(&model.relative_path)
    .evidence(format!("materialized='{mat}', {} downstream models", children.len()))
    .remediation(
        "Inspect representative query plans and build costs. Consider `table` or `incremental` when storing a shared result reduces repeated work enough to justify refresh and storage costs. Keep `view` or `ephemeral` when their cost and freshness fit the workload; consumer count alone does not decide.",
    )
    .effort(effort::LOW)
    .ctx("downstream", json!(sorted))]
}

fn single_use_model(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    if model.layer != "silver" && !model.layer.is_empty() {
        return vec![];
    }
    if model.is_python {
        return vec![];
    }
    let children = model_children(model, project);
    if children.len() != 1 {
        return vec![];
    }
    let empty = Map::new();
    let def = project.schema_def(&model.name).unwrap_or(&empty);
    if truthy(def.get("description"))
        && (truthy(def.get("tests")) || truthy(def.get("data_tests")) || truthy(def.get("columns")))
    {
        return vec![];
    }
    let c = &children[0];
    vec![Suggestion::new(
        "SSC-PRF-DBTMAT0002",
        format!("This model has one detected consumer, `{c}`, and lacks the scanned combination of a description with tests or column metadata."),
    )
    .file(&model.relative_path)
    .evidence(format!("1 detected consumer ({c}); description-plus-test/column metadata condition not met"))
    .remediation(format!(
        "Review whether this model provides a useful testing, ownership, or debugging boundary. If not, consider a named CTE in `{c}`. Otherwise document its role and add suitable tests. `ephemeral` preserves a dbt node without a standalone relation, but has testing and performance limits."
    ))
    .effort(effort::MEDIUM)
    .ctx("consumer", json!(c))]
}

fn clustering(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let mat = model.materialization();
    if mat != "table" && mat != "incremental" {
        return vec![];
    }
    let cb = model.effective_config.get("cluster_by");
    if !truthy(cb) {
        return vec![];
    }
    let columns = match cb.unwrap() {
        Value::Array(a) => a.clone(),
        other => vec![other.clone()],
    };
    let maximum = project.config.max_cluster_columns;
    if (columns.len() as i64) <= maximum {
        return vec![];
    }
    vec![Suggestion::new(
        "SSC-PRF-DBTMAT0004",
        format!(
            "`cluster_by` lists {} columns, above the local review threshold of {maximum}. Measure the workload benefit before changing the key.",
            columns.len()
        ),
    )
    .file(&model.relative_path)
    .line_opt(config_key_line(model, "cluster_by"))
    .evidence(format!("cluster_by={}", py_str(&Value::Array(columns))))
    .remediation(
        "Inspect `system$clustering_information()` and representative query profiles. Consider selective filters and frequently used join, grouping, or sorting columns. Compare pruning benefits with clustering maintenance costs; do not drop a key solely because it exceeds the local column-count threshold.",
    )
    .effort(effort::LOW)]
}

fn redundant_config(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let mut redundant: Vec<&String> = model
        .own_config
        .iter()
        .filter(|(k, v)| model.folder_config.get(*k) == Some(*v))
        .map(|(k, _)| k)
        .collect();
    if redundant.is_empty() {
        return vec![];
    }
    redundant.sort();
    let n = redundant.len();
    let keys = redundant.iter().map(|k| k.as_str()).collect::<Vec<_>>().join(", ");
    let ev = redundant
        .iter()
        .map(|k| format!("{k}={}", py_repr(&model.own_config[*k])))
        .collect::<Vec<_>>()
        .join(", ");
    let related: Vec<String> = redundant
        .iter()
        .filter_map(|k| folder_key_line(model, project, k))
        .collect::<std::collections::BTreeSet<_>>()
        .into_iter()
        .map(|l| format!("{}:{l}", crate::discovery::root_relative(project, "dbt_project.yml")))
        .collect();
    vec![Suggestion::new(
        "SSC-EWI-DBTMAT0006",
        format!(
            "{} {keys} {} the `dbt_project.yml` folder default.",
            plural(n, "config key"),
            if n == 1 { "repeats" } else { "repeat" }
        ),
    )
    .file(&model.relative_path)
    .line_opt(config_key_line(model, redundant[0]))
    .ctx("related_files", json!(related))
    .evidence(ev)
    .remediation(
        "Compare effective configuration before removing repeated settings. Scalar values may inherit from the folder, but hooks and other cumulative settings need separate review. Remove a model-level entry only when the resulting behavior stays the same; retain intentional overrides.",
    )
    .effort(effort::LOW)]
}

fn has_mat(m: &Map<String, Value>) -> bool {
    m.keys().any(|k| k.starts_with("+materialized"))
}

fn no_folder_default(project: &ProjectContext) -> Vec<Suggestion> {
    let mut layers: Vec<&String> = project.models.iter().filter_map(|m| m.segments.first()).collect();
    layers.sort();
    layers.dedup();
    if layers.is_empty() {
        return vec![];
    }
    let empty = Map::new();
    let tree = project.project_yml.get("models").and_then(Value::as_object).unwrap_or(&empty);
    let node: &Map<String, Value> = match tree.get(&project.name).and_then(Value::as_object) {
        Some(n) => n,
        None => {
            let cands: Vec<&Map<String, Value>> = tree
                .iter()
                .filter(|(k, _)| !k.starts_with('+'))
                .filter_map(|(_, v)| v.as_object())
                .collect();
            if cands.len() == 1 { cands[0] } else { &empty }
        }
    };
    let node_has = has_mat(node);
    let unconfigured: Vec<&str> = layers
        .iter()
        .filter(|l| !node.get(l.as_str()).and_then(Value::as_object).is_some_and(has_mat) && !node_has)
        .map(|l| l.as_str())
        .collect();
    if unconfigured.is_empty() {
        return vec![];
    }
    let list = unconfigured.join(", ");
    let n = unconfigured.len();
    vec![Suggestion::new(
        "SSC-EWI-DBTMAT0007",
        format!(
            "{} {} no `+materialized` default in `dbt_project.yml`: {list}.",
            plural(n, "folder"),
            if n == 1 { "has" } else { "have" }
        ),
    )
    .file("dbt_project.yml")
    .evidence(format!("no +materialized for: {list}"))
    .remediation(format!(
        "In `dbt_project.yml`, add a `+materialized:` default under each listed folder, for example:\n\n```yaml\nmodels:\n  {}:\n    {}:\n      +materialized: view\n```\n\nPick the value per folder (`view`, `table`, `incremental` or `ephemeral`). Individual models then override only where they differ. If every subfolder of a listed folder already sets `+materialized`, no change is needed.",
        project.name, unconfigured[0]
    ))
    .effort(effort::LOW)]
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;
    use serde_json::json;

    fn fan(view: bool, n: usize) -> TempProject {
        let a = if view { "{{ config(materialized='view') }}\nselect 1 as x" } else { "{{ config(materialized='table') }}\nselect 1 as x" };
        let mut files = vec![("models/a.sql", a)];
        let names = ["b", "c", "d"];
        let paths = ["models/b.sql", "models/c.sql", "models/d.sql"];
        for i in 0..n {
            let _ = names[i];
            files.push((paths[i], "select * from {{ ref('a') }}"));
        }
        TempProject::new(&files)
    }

    #[test]
    fn mat0001_fires() {
        assert_eq!(fan(true, 3).findings("SSC-PRF-DBTMAT0001").len(), 1);
    }
    #[test]
    fn mat0001_clean() {
        assert!(fan(false, 3).findings("SSC-PRF-DBTMAT0001").is_empty());
    }

    fn single(schema: &str) -> TempProject {
        TempProject::new(&[
            ("models/a.sql", "select 1 as x"),
            ("models/b.sql", "select * from {{ ref('a') }}"),
            ("models/schema.yml", schema),
        ])
    }
    #[test]
    fn mat0002_fires() {
        assert_eq!(single("version: 2\nmodels: []\n").findings("SSC-PRF-DBTMAT0002").len(), 1);
    }
    #[test]
    fn mat0002_clean() {
        let s = "version: 2\nmodels:\n  - name: a\n    description: d\n    columns:\n      - name: x\n";
        assert!(single(s).findings("SSC-PRF-DBTMAT0002").is_empty());
    }

    #[test]
    fn mat0004_fires() {
        let t = TempProject::new(&[("models/a.sql", "{{ config(materialized='table', cluster_by=['a','b','c','d','e']) }}\nselect 1")]);
        assert_eq!(t.findings("SSC-PRF-DBTMAT0004").len(), 1);
    }
    #[test]
    fn mat0004_clean() {
        let t = TempProject::new(&[("models/a.sql", "{{ config(materialized='table', cluster_by=['a','b']) }}\nselect 1")]);
        assert!(t.findings("SSC-PRF-DBTMAT0004").is_empty());
    }

    #[test]
    fn mat0008_fires() {
        let t = TempProject::new(&[("models/a.sql", "{% if var('full', false) %}\n{{ config(materialized='table') }}\n{% endif %}\nselect 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTMAT0008").len(), 1);
        let t = TempProject::new(&[("models/a.sql", "{% set f = var('full', false) %}\n{% if f %}{{ config(materialized='table') }}{% endif %}\nselect 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTMAT0008").len(), 1);
    }
    #[test]
    fn mat0008_clean() {
        let t = TempProject::new(&[("models/a.sql", "{{ config(materialized='table') }}\nselect {% if var('x', 1) %}1{% else %}2{% endif %}")]);
        assert!(t.findings("SSC-EWI-DBTMAT0008").is_empty());
        // Unconditional materialization; the gated config sets hooks only (SnowConvert shape).
        let hooks = "{% set pre_sql = var('p', '') %}\n{{ config(materialized='table') }}\n{% if pre_sql != '' %}\n{{ config(pre_hook=pre_sql) }}\n{% endif %}\nselect 1";
        assert!(TempProject::new(&[("models/a.sql", hooks)]).findings("SSC-EWI-DBTMAT0008").is_empty());
    }

    const PROJ: &str = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    silver:\n      +materialized: table\n";
    #[test]
    fn mat0006_fires() {
        let t = TempProject::new(&[("dbt_project.yml", PROJ), ("models/silver/a.sql", "{{ config(materialized='table') }}\nselect 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTMAT0006").len(), 1);
    }
    #[test]
    fn mat0006_points_at_key_and_folder() {
        let sql = "{{ config(\n  materialized='table'\n) }}\nselect 1";
        let t = TempProject::new(&[("dbt_project.yml", PROJ), ("models/silver/a.sql", sql)]);
        let f = &t.findings("SSC-EWI-DBTMAT0006")[0];
        assert_eq!(f.line, Some(2));
        assert_eq!(f.context["related_files"], json!(["dbt_project.yml:7"]));
    }
    #[test]
    fn mat0006_skips_comment_line() {
        let sql = "-- trigger: config(materialized='table') repeats\n{{ config(materialized='table') }}\nselect 1";
        let t = TempProject::new(&[("dbt_project.yml", PROJ), ("models/silver/a.sql", sql)]);
        assert_eq!(t.findings("SSC-EWI-DBTMAT0006")[0].line, Some(2));
    }
    #[test]
    fn mat0004_points_at_cluster_by() {
        let sql = "{{ config(\n  materialized='table',\n  cluster_by=['a','b','c','d','e']\n) }}\nselect 1";
        let t = TempProject::new(&[("models/a.sql", sql)]);
        assert_eq!(t.findings("SSC-PRF-DBTMAT0004")[0].line, Some(3));
    }
    #[test]
    fn mat0006_clean() {
        let t = TempProject::new(&[("dbt_project.yml", PROJ), ("models/silver/a.sql", "{{ config(materialized='view') }}\nselect 1")]);
        assert!(t.findings("SSC-EWI-DBTMAT0006").is_empty());
    }

    #[test]
    fn mat0007_fires() {
        let t = TempProject::new(&[("models/silver/a.sql", "select 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTMAT0007").len(), 1);
    }
    #[test]
    fn mat0007_clean() {
        let t = TempProject::new(&[("dbt_project.yml", PROJ), ("models/silver/a.sql", "select 1")]);
        assert!(t.findings("SSC-EWI-DBTMAT0007").is_empty());
    }
}
