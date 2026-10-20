//! DOC rules: documentation coverage.

use serde_json::{json, Map, Value};

use crate::discovery::{ModelFile, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural, severity, Suggestion};
use crate::sqlutil::{py_str, truthy};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTDOC0001", detect: Detect::Model(doc0001) },
    Detector { code: "SSC-EWI-DBTDOC0002", detect: Detect::Model(doc0002) },
    Detector { code: "SSC-EWI-DBTDOC0003", detect: Detect::Project(doc0003) },
    Detector { code: "SSC-EWI-DBTDOC0004", detect: Detect::Project(doc0004) },
];

/// Python `str(d.get(key, "")).strip()` is non-empty.
fn has_text(d: &Map<String, Value>, key: &str) -> bool {
    d.get(key).map(py_str).is_some_and(|s| !s.trim().is_empty())
}

fn doc0001(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(def) = project.schema_def(&model.name) else { return vec![] };
    if def.is_empty() || has_text(def, "description") {
        return vec![];
    }
    let sev = if model.layer == "gold" { severity::MEDIUM } else { severity::LOW };
    let file = project
        .schema_sources
        .get(&model.name)
        .cloned()
        .unwrap_or_else(|| model.relative_path.clone());
    vec![Suggestion::new(
        "SSC-EWI-DBTDOC0001",
        format!("`{}` has no description in the schema YAML.", model.name),
    )
    .severity(sev)
    .file(file)
    .ctx("model", json!(model.name))
    .evidence(format!("{}: description absent", model.name))
    .remediation(format!(
        "Add a description with the actual row grain, purpose, and refresh schedule. Replace the illustrative daily cadence and authority claim below with verified facts:\n\n```yaml\n  - name: {}\n    description: |\n      One row per <entity>. Refreshed daily.\n      Use this as the source of truth for <purpose>.\n```",
        model.name
    ))
    .effort(effort::LOW)]
}

fn doc0002(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(def) = project.schema_def(&model.name) else { return vec![] };
    let columns: Vec<&Map<String, Value>> = match def.get("columns") {
        Some(Value::Array(a)) => a.iter().filter_map(|c| c.as_object()).collect(),
        _ => vec![],
    };
    if columns.len() < 3 {
        return vec![];
    }
    let documented = columns.iter().filter(|c| has_text(c, "description")).count();
    let ratio = documented as f64 / columns.len() as f64;
    let threshold = project.config.column_doc_coverage;
    if ratio >= threshold {
        return vec![];
    }
    let undocumented: Vec<String> = columns
        .iter()
        .filter(|c| !has_text(c, "description"))
        .map(|c| c.get("name").map(py_str).unwrap_or_else(|| "None".into()))
        .collect();
    let mut evidence = format!(
        "undocumented: {}",
        undocumented.iter().take(8).cloned().collect::<Vec<_>>().join(", ")
    );
    if undocumented.len() > 8 {
        evidence.push_str(" ...");
    }
    let file = project
        .schema_sources
        .get(&model.name)
        .cloned()
        .unwrap_or_else(|| model.relative_path.clone());
    vec![Suggestion::new(
        "SSC-EWI-DBTDOC0002",
        format!(
            "{} of {} columns documented ({:.0}%), below the {:.0}% threshold.",
            documented,
            columns.len(),
            ratio * 100.0,
            threshold * 100.0
        ),
    )
    .file(file)
    .ctx("model", json!(model.name))
    .ctx("column_name", json!(undocumented.first().cloned().unwrap_or_default()))
    .evidence(evidence)
    .remediation(
        "Document columns whose meaning is not obvious from the name first: amounts, dates, flags, and codes. For shared definitions, use a `docs` block and reference with `description: \"{{ doc('column_name') }}\"`.",
    )
    .effort(effort::MEDIUM)
    .ctx("undocumented", json!(undocumented))]
}

fn doc0003(project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    let decls = crate::discovery::source_decls(project);
    for (si, source) in project.source_defs.iter().enumerate() {
        let decl = decls.iter().find(|d| d.index == si);
        let file = project.source_def_files[si].clone();
        let name = source.get("name").map(py_str).unwrap_or_else(|| "unknown".into());
        if !has_text(source, "description") {
            out.push(
                Suggestion::new("SSC-EWI-DBTDOC0003", format!("Source `{name}` has no description."))
                    .file(file.clone())
                    .line(decl.map_or(1, |d| d.line))
                    .evidence(format!("source {name}: description absent"))
                    .remediation(
                        "Record the upstream system, its owner, and the expected arrival schedule. If freshness monitoring is needed, configure a suitable loaded-at signal and freshness thresholds, then schedule the freshness check. A description or configuration block alone does not run the check.",
                    )
                    .effort(effort::LOW),
            );
        }
        let undescribed: Vec<String> = match source.get("tables") {
            Some(Value::Array(a)) => a
                .iter()
                .filter_map(|t| t.as_object())
                .filter(|t| !has_text(t, "description"))
                .map(|t| t.get("name").map(py_str).unwrap_or_else(|| "None".into()))
                .collect(),
            _ => vec![],
        };
        if !undescribed.is_empty() {
            // Cite the first undescribed table's `name:` line.
            let line = decl
                .and_then(|d| d.tables.iter().find(|t| t.name == undescribed[0]).or(d.tables.first()).map(|t| t.line).or(Some(d.line)))
                .unwrap_or(1);
            let more = if undescribed.len() > 6 { " ..." } else { "" };
            let head = undescribed.iter().take(6).cloned().collect::<Vec<_>>().join(", ");
            out.push(
                Suggestion::new(
                    "SSC-EWI-DBTDOC0003",
                    format!(
                        "{} in source `{}` {} descriptions: {}{}.",
                        plural(undescribed.len(), "table"),
                        name,
                        if undescribed.len() == 1 { "lacks" } else { "lack" },
                        head,
                        more
                    ),
                )
                .file(file.clone())
                .line(line)
                .evidence(head)
                .remediation("Describe each source table so its grain is stated once, at the boundary.")
                .effort(effort::LOW),
            );
        }
    }
    out
}

fn doc0004(project: &ProjectContext) -> Vec<Suggestion> {
    if project.model_count() == 0 {
        return vec![];
    }
    if project.project_yml.get("models").is_some_and(has_persist_docs) {
        return vec![];
    }
    let documented = project.schema_models.values().filter(|d| has_text(d, "description")).count();
    if documented == 0 {
        return vec![];
    }
    vec![Suggestion::new(
        "SSC-EWI-DBTDOC0004",
        format!(
            "{} {} descriptions, but no enabling `persist_docs` setting was found under project-level `models:`. Check model-level settings and existing database comments.",
            plural(documented, "model"),
            if documented == 1 { "has" } else { "have" }
        ),
    )
    .file("dbt_project.yml")
    .evidence("no +persist_docs under models:")
    .remediation(format!(
        "After checking effective model settings, enable comment persistence where supported:\n\n```yaml\nmodels:\n  {}:\n    +persist_docs:\n      relation: true\n      columns: true\n```\n\nRebuild the affected models to write supported comments. Check relation and column quoting, materialization support, and whether each consumer tool displays those comments.",
        project.name
    ))
    .effort(effort::LOW)
    .ctx("documented_models", json!(documented))]
}

fn has_persist_docs(node: &Value) -> bool {
    let Value::Object(map) = node else { return false };
    for (key, value) in map {
        if key == "+persist_docs" || key == "persist_docs" {
            match value {
                Value::Object(o) => {
                    if o.values().any(|v| truthy(Some(v))) {
                        return true;
                    }
                }
                v if truthy(Some(v)) => return true,
                _ => {}
            }
        } else if has_persist_docs(value) {
            return true;
        }
    }
    false
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const ROOT_YML: &str = "name: demo\nversion: '1.0'\nprofile: p\n";

    #[test]
    fn doc0001_fires_and_clean() {
        let bad = TempProject::new(&[
            ("models/a.sql", "select 1"),
            ("models/schema.yml", "version: 2\nmodels:\n  - name: a\n    columns: []\n"),
        ]);
        assert_eq!(bad.findings("SSC-EWI-DBTDOC0001").len(), 1);
        let ok = TempProject::new(&[
            ("models/a.sql", "select 1"),
            ("models/schema.yml", "version: 2\nmodels:\n  - name: a\n    description: one row per x\n"),
        ]);
        assert!(ok.findings("SSC-EWI-DBTDOC0001").is_empty());
    }

    #[test]
    fn doc0002_fires_and_clean() {
        let cols = |d: &str| {
            format!(
                "version: 2\nmodels:\n  - name: a\n    description: d\n    columns:\n      - name: x\n        description: {d}\n      - name: y\n        description: {d}\n      - name: z\n        description: {d}\n"
            )
        };
        let bad = TempProject::new(&[("models/a.sql", "select 1"), ("models/schema.yml", &cols("''"))]);
        assert_eq!(bad.findings("SSC-EWI-DBTDOC0002").len(), 1);
        let ok = TempProject::new(&[("models/a.sql", "select 1"), ("models/schema.yml", &cols("text"))]);
        assert!(ok.findings("SSC-EWI-DBTDOC0002").is_empty());
    }

    #[test]
    fn doc0003_fires_and_clean() {
        let bad = TempProject::new(&[
            ("models/a.sql", "select 1"),
            ("models/src.yml", "version: 2\nsources:\n  - name: raw\n    tables:\n      - name: t\n"),
        ]);
        let f = bad.findings("SSC-EWI-DBTDOC0003");
        assert_eq!(f.len(), 2);
        // Cite the YAML file and the `name:` lines, not the models folder.
        assert!(f.iter().all(|s| s.file == "models/src.yml"), "{f:?}");
        assert_eq!(f[0].line, Some(3));
        assert_eq!(f[1].line, Some(5));
        let ok = TempProject::new(&[
            ("models/a.sql", "select 1"),
            (
                "models/src.yml",
                "version: 2\nsources:\n  - name: raw\n    description: d\n    tables:\n      - name: t\n        description: d\n",
            ),
        ]);
        assert!(ok.findings("SSC-EWI-DBTDOC0003").is_empty());
    }

    #[test]
    fn doc0004_fires_and_clean() {
        let schema = "version: 2\nmodels:\n  - name: a\n    description: d\n";
        let bad = TempProject::new(&[
            ("dbt_project.yml", ROOT_YML),
            ("models/a.sql", "select 1"),
            ("models/schema.yml", schema),
        ]);
        assert_eq!(bad.findings("SSC-EWI-DBTDOC0004").len(), 1);
        let ok = TempProject::new(&[
            (
                "dbt_project.yml",
                "name: demo\nversion: '1.0'\nprofile: p\nmodels:\n  demo:\n    +persist_docs:\n      relation: true\n      columns: true\n",
            ),
            ("models/a.sql", "select 1"),
            ("models/schema.yml", schema),
        ]);
        assert!(ok.findings("SSC-EWI-DBTDOC0004").is_empty());
    }
}
