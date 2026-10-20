//! ARC rules: architecture and lineage conventions.

use std::collections::{BTreeMap, BTreeSet};

use serde_json::{json, Map, Value};

use crate::discovery::{ModelFile, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural, Suggestion};
use crate::rx;
use crate::sqlutil::{py_str, ref_pattern, source_pattern, span};

/// Byte range of the first `source(src, tbl)` call, or of any `source()` call when `want` is None.
fn source_call(raw: &str, want: Option<&(String, String)>) -> Option<(usize, usize)> {
    source_pattern()
        .captures_iter(raw)
        .find(|c| want.is_none_or(|w| c[1] == w.0 && c[2] == w.1))
        .map(|c| {
            let m = c.get(0).unwrap();
            (m.start(), m.end())
        })
}

/// Byte range of the first `ref()` call to `name`.
fn ref_call(raw: &str, name: &str) -> Option<(usize, usize)> {
    ref_pattern()
        .captures_iter(raw)
        .find(|c| c.get(2).or(c.get(1)).is_some_and(|g| g.as_str() == name))
        .map(|c| {
            let m = c.get(0).unwrap();
            (m.start(), m.end())
        })
}

const UNKNOWN_LAYER: &str = "SSC-EWI-DBTARC0001";
const SOURCE_OUTSIDE_STAGING: &str = "SSC-EWI-DBTARC0003";
const DUPLICATE_STAGING: &str = "SSC-EWI-DBTARC0004";
const LAYER_CROSSING: &str = "SSC-EWI-DBTARC0005";
const STAGING_LOGIC: &str = "SSC-EWI-DBTARC0006";
const DUPLICATE_TAGS: &str = "SSC-EWI-DBTARC0007";

const ALIASES: &str = "bronze, gold, int, intermediate, mart, marts, presentation, raw, silver, staging, stg";

pub const DETECTORS: &[Detector] = &[
    Detector { code: UNKNOWN_LAYER, detect: Detect::Model(unknown_layer) },
    Detector { code: SOURCE_OUTSIDE_STAGING, detect: Detect::Model(source_outside_staging) },
    Detector { code: DUPLICATE_STAGING, detect: Detect::Project(duplicate_staging) },
    Detector { code: LAYER_CROSSING, detect: Detect::Model(layer_crossing) },
    Detector { code: STAGING_LOGIC, detect: Detect::Model(staging_logic) },
    Detector { code: DUPLICATE_TAGS, detect: Detect::Project(duplicate_tags) },
];

fn rank(layer: &str) -> Option<u8> {
    match layer {
        "bronze" => Some(0),
        "silver" => Some(1),
        "gold" => Some(2),
        _ => None,
    }
}

fn title(s: &str) -> String {
    let mut c = s.chars();
    c.next().map(|f| f.to_uppercase().collect::<String>() + &c.as_str().to_lowercase()).unwrap_or_default()
}

fn unknown_layer(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.layer.is_empty() {
        return vec![];
    }
    let location = model.segments.join("/");
    let msg = if location.is_empty() {
        "This model sits directly in `models/`, outside the recognized layer folders. It can still inherit project configuration.".to_string()
    } else {
        format!("This model sits in `models/{location}`, which is not a recognized layer folder. It can still inherit project configuration.")
    };
    let shown = if location.is_empty() { "models/ root" } else { &location };
    vec![Suggestion::new(UNKNOWN_LAYER, msg)
        .file(&model.relative_path)
        .evidence(format!("path segments: {shown}"))
        .remediation(format!(
            "Under the local layer policy, use `bronze/` for source-aligned staging, `silver/` for business-logic intermediates, and `gold/` for consumer-facing marts. Recognized aliases are {ALIASES}. Before moving the model, check inherited configuration and selectors. Document an intentional alternative layout."
        ))
        .effort(effort::MEDIUM)]
}

fn source_outside_staging(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if model.layer == "bronze" || model.layer.is_empty() || model.sources.is_empty() {
        return vec![];
    }
    let labels: Vec<String> = model.sources.iter().map(|s| format!("{}.{}", s.0, s.1)).collect();
    let quoted: Vec<String> = labels.iter().map(|l| format!("`{l}`")).collect();
    let mut s = Suggestion::new(
        SOURCE_OUTSIDE_STAGING,
        format!(
            "This {} model calls `source()` on {} directly, bypassing the staging layer.",
            title(&model.layer),
            quoted.join(", ")
        ),
    )
    .file(&model.relative_path);
    if let Some((a, b)) = source_call(&model.raw, None) {
        s = s.span(span(&model.raw, a, b));
    }
    vec![s
        .evidence(labels.join(", "))
        .remediation("Add a dedicated staging model for each source table and `ref()` it here. Staging is where renaming, casting, and light cleaning belong.")
        .effort(effort::MEDIUM)
        .ctx("sources", json!(labels))]
}

fn duplicate_staging(project: &ProjectContext) -> Vec<Suggestion> {
    let mut by_source: BTreeMap<(String, String), Vec<&ModelFile>> = BTreeMap::new();
    for m in project.models.iter().filter(|m| m.layer == "bronze") {
        for s in &m.sources {
            by_source.entry(s.clone()).or_default().push(m);
        }
    }
    let mut out = vec![];
    for (source, models) in by_source {
        // A model that calls one source twice counts once; paths keep same-named files apart.
        let names: Vec<String> =
            models.iter().map(|m| crate::discovery::root_relative(project, &m.relative_path)).collect::<BTreeSet<_>>().into_iter().collect();
        if names.len() < 2 {
            continue;
        }
        let label = format!("{}.{}", source.0, source.1);
        let mut files: Vec<&ModelFile> = models.clone();
        files.sort_by(|a, b| a.relative_path.cmp(&b.relative_path));
        files.dedup_by(|a, b| a.relative_path == b.relative_path);
        let line_of = |m: &ModelFile| source_call(&m.raw, Some(&source)).map(|(a, _)| m.line_of(a)).unwrap_or(1);
        let related: Vec<String> = files[1..]
            .iter()
            .map(|m| format!("{}:{}", crate::discovery::root_relative(project, &m.relative_path), line_of(m)))
            .collect();
        let first = files[0];
        let mut s = Suggestion::new(
                DUPLICATE_STAGING,
                format!("Source `{label}` has {} staging models: {}.", names.len(), names.join(", ")),
            )
            .file(&first.relative_path);
        if let Some((a, b)) = source_call(&first.raw, Some(&source)) {
            s = s.span(span(&first.raw, a, b));
        }
        out.push(
            s.evidence(format!("{label} -> {}", names.join(", ")))
            .remediation("Under the local layer policy, prefer one source-aligned staging model and `ref()` it downstream. Check that the copies use the same source and preserve required cleaning before consolidating. Put consumer-specific shapes in silver, or document why separate staging models are needed.")
            .effort(effort::MEDIUM)
            .ctx("models", json!(names))
            .ctx("related_files", json!(related)),
        );
    }
    out
}

fn layer_crossing(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(own) = rank(&model.layer) else { return vec![] };
    let mut out = vec![];
    for parent_name in project.graph.parent_names(&model.name) {
        let Some(parent) = project.model_by_name(&parent_name) else { continue };
        let Some(pr) = rank(&parent.layer) else { continue };
        if pr <= own {
            continue;
        }
        let mut s = Suggestion::new(
                LAYER_CROSSING,
                format!(
                    "This {} model depends on `{parent_name}` in the downstream {} layer.",
                    title(&model.layer),
                    parent.layer
                ),
            )
            .file(&model.relative_path);
        if let Some((a, b)) = ref_call(&model.raw, &parent_name) {
            s = s.span(span(&model.raw, a, b));
        }
        let parent_file = format!("{}:1", crate::discovery::root_relative(project, &parent.relative_path));
        out.push(
            s.evidence(format!("{}.{parent_name} -> {}.{}", parent.layer, model.layer, model.name))
            .remediation(format!(
                "Invert the dependency: move the shared logic into the earlier layer so both can read it, or move `{}` into `{}/` if it belongs downstream.",
                model.name, parent.layer
            ))
            .effort(effort::HIGH)
            .ctx("related_files", json!([parent_file])),
        );
    }
    out
}

fn staging_logic(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if model.layer != "bronze" || model.is_python {
        return vec![];
    }
    let mut issues = vec![];
    if rx!(r"(?i)\bjoin\b").is_match(&model.stripped) {
        issues.push("a join");
    }
    if rx!(r"(?i)\bgroup\s+by\b").is_match(&model.stripped)
        && rx!(r"(?i)\b(sum|count|avg|min|max|median|listagg)\s*\(").is_match(&model.stripped)
    {
        issues.push("an aggregation");
    }
    if issues.is_empty() {
        return vec![];
    }
    vec![Suggestion::new(STAGING_LOGIC, format!("This staging model contains {}.", issues.join(" and ")))
        .file(&model.relative_path)
        .evidence(issues.join(", "))
        .remediation("Prefer a source-aligned staging model for renaming, casting, and light cleaning. Move business joins and aggregation to a silver `int_` model when that fits the data flow. Keep justified source-reconstruction joins in a documented base model.")
        .effort(effort::MEDIUM)]
}

fn walk(node: &Value, path: &[String], inherited: &BTreeSet<String>, out: &mut Vec<Suggestion>) {
    let Value::Object(map) = node else { return };
    let own = ["+tags", "tags"]
        .iter()
        .filter_map(|k| map.get(*k))
        .find(|v| crate::sqlutil::truthy(Some(v)));
    let own_set: BTreeSet<String> = match own {
        Some(Value::Array(a)) => a.iter().map(py_str).collect(),
        Some(v) => [py_str(v)].into_iter().collect(),
        None => BTreeSet::new(),
    };
    let redundant: Vec<String> = own_set.intersection(inherited).cloned().collect();
    if !redundant.is_empty() {
        let location = if path.is_empty() { "<project root>".to_string() } else { path.join("/") };
        let mut keys = vec![json!("models")];
        keys.extend(path.iter().map(|p| json!(p)));
        keys.push(json!("tags"));
        let sorted: Vec<Value> = own_set.iter().map(|t| json!(t)).collect();
        let tags: Vec<String> = redundant.iter().map(|t| format!("`{t}`")).collect();
        out.push(
            Suggestion::new(
                DUPLICATE_TAGS,
                format!(
                    "`{location}` re-declares {} it already inherits from its parent: {}.",
                    plural(redundant.len(), "tag"),
                    tags.join(", ")
                ),
            )
            .file("dbt_project.yml")
            .ctx("yaml_keys", Value::Array(keys))
            .evidence(format!("{location} +tags: {}", py_str(&Value::Array(sorted))))
            .remediation(format!(
                "Remove {} from `{location}`. Tags accumulate down the tree, so the parent declaration already applies here.",
                redundant.join(", ")
            ))
            .effort(effort::LOW),
        );
    }
    let next: BTreeSet<String> = inherited.union(&own_set).cloned().collect();
    for (k, v) in map {
        if !k.starts_with('+') {
            let mut p = path.to_vec();
            p.push(k.clone());
            walk(v, &p, &next, out);
        }
    }
}

fn duplicate_tags(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    let empty = Value::Object(Map::new());
    let models = project.project_yml.get("models").filter(|v| crate::sqlutil::truthy(Some(v))).unwrap_or(&empty);
    walk(models, &[], &BTreeSet::new(), &mut out);
    out
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    // A stale manifest whose edges disagree with the SQL. The audit must ignore it.
    const STALE_MANIFEST: &str = r#"{"nodes":{
      "model.demo.stg_a":{"name":"stg_a","depends_on":{"nodes":[]}},
      "model.demo.fct_b":{"name":"fct_b","depends_on":{"nodes":["model.demo.stg_a"]}}},
      "child_map":{"model.demo.stg_a":["model.demo.fct_b"],"model.demo.fct_b":[]}}"#;

    #[test]
    fn unknown_layer() {
        let t = TempProject::new(&[("models/misc/x.sql", "select 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0001").len(), 1);
        let t = TempProject::new(&[("models/staging/x.sql", "select 1")]);
        assert!(t.findings("SSC-EWI-DBTARC0001").is_empty());
    }

    #[test]
    fn source_outside_staging() {
        let sql = "select * from {{ source('s', 't') }}";
        let t = TempProject::new(&[("models/silver/x.sql", sql)]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0003").len(), 1);
        let t = TempProject::new(&[("models/staging/x.sql", sql)]);
        assert!(t.findings("SSC-EWI-DBTARC0003").is_empty());
    }

    #[test]
    fn duplicate_staging() {
        let sql = "select * from {{ source('s', 't') }}";
        let t = TempProject::new(&[("models/staging/a.sql", sql), ("models/staging/b.sql", sql)]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0004").len(), 1);
        let t = TempProject::new(&[("models/staging/a.sql", sql)]);
        assert!(t.findings("SSC-EWI-DBTARC0004").is_empty());
        let twice = format!("{sql} union all {sql}");
        let t = TempProject::new(&[("models/staging/a.sql", twice.as_str())]);
        assert!(t.findings("SSC-EWI-DBTARC0004").is_empty());
    }

    #[test]
    fn layer_crossing() {
        let up = "select * from {{ ref('fct_b') }}";
        let t = TempProject::new(&[("models/staging/stg_a.sql", up), ("models/marts/fct_b.sql", "select 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0005").len(), 1);
        let t = TempProject::new(&[("models/staging/stg_a.sql", up), ("models/staging/fct_b.sql", "select 1")]);
        assert!(t.findings("SSC-EWI-DBTARC0005").is_empty());
    }

    #[test]
    fn layer_crossing_ignores_manifest() {
        let up = "select * from {{ ref('fct_b') }}";
        let t = TempProject::new(&[
            ("models/staging/stg_a.sql", up),
            ("models/marts/fct_b.sql", "select 1"),
            ("target/manifest.json", STALE_MANIFEST),
        ]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0005").len(), 1);
        let t = TempProject::new(&[
            ("models/staging/stg_a.sql", "select 1"),
            ("models/marts/fct_b.sql", "select 1"),
            ("target/manifest.json", STALE_MANIFEST),
        ]);
        assert!(t.findings("SSC-EWI-DBTARC0005").is_empty());
    }

    #[test]
    fn staging_logic() {
        let t = TempProject::new(&[("models/staging/x.sql", "select * from a join b on a.i = b.i")]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0006").len(), 1);
        let t = TempProject::new(&[("models/staging/x.sql", "select * from a")]);
        assert!(t.findings("SSC-EWI-DBTARC0006").is_empty());
    }

    #[test]
    fn duplicate_tags() {
        let yml = |inner: &str| {
            format!("name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    +tags: [a]\n    silver:\n      +tags: [{inner}]\n")
        };
        let t = TempProject::new(&[("dbt_project.yml", &yml("a, b"))]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0007").len(), 1);
        let t = TempProject::new(&[("dbt_project.yml", &yml("b"))]);
        assert!(t.findings("SSC-EWI-DBTARC0007").is_empty());
    }

    #[test]
    fn source_outside_staging_points_at_call() {
        let sql = "-- source() used here\nselect 1\nfrom {{ source('s', 't') }}";
        let t = TempProject::new(&[("models/silver/x.sql", sql)]);
        assert_eq!(t.findings("SSC-EWI-DBTARC0003")[0].line, Some(3));
    }

    #[test]
    fn duplicate_staging_lines_and_related() {
        let a = "select\n  id\nfrom {{ source('s', 't') }}";
        let b = "select * from {{ source('s', 't') }}";
        let t = TempProject::new(&[("models/staging/a.sql", a), ("models/staging/b.sql", b)]);
        let f = &t.findings("SSC-EWI-DBTARC0004")[0];
        assert_eq!(f.line, Some(3));
        assert_eq!(f.context["related_files"], serde_json::json!(["models/staging/b.sql:1"]));
    }

    #[test]
    fn layer_crossing_points_at_ref() {
        let up = "select *\nfrom {{ ref('fct_b') }}";
        let t = TempProject::new(&[("models/staging/stg_a.sql", up), ("models/marts/fct_b.sql", "select 1")]);
        let f = &t.findings("SSC-EWI-DBTARC0005")[0];
        assert_eq!(f.line, Some(2));
        assert_eq!(f.context["related_files"], serde_json::json!(["models/marts/fct_b.sql:1"]));
    }
}
