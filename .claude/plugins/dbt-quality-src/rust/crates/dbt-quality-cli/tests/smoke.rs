//! Run the built CLI on a temporary project.

use std::process::Command;

use dbt_quality_core::testing::TempProject;

#[test]
fn cli_smoke() {
    let bin = env!("CARGO_BIN_EXE_dbt-quality");
    let t = TempProject::new(&[("models/a.sql", "select a.x\nfrom a, b\nwhere a.id = b.id\n")]);

    let rules = Command::new(bin).args(["rules", "--format", "json"]).output().unwrap();
    assert!(rules.status.success());
    let list: serde_json::Value = serde_json::from_slice(&rules.stdout).unwrap();
    assert!(list.as_array().unwrap().len() > 100);

    let lint = Command::new(bin).arg("lint").arg(t.path()).args(["--format", "json"]).output().unwrap();
    assert!(lint.status.success());
    assert!(String::from_utf8_lossy(&lint.stdout).contains("SSC-EWI-DBTSQL0007"));

    let audit = Command::new(bin).arg("audit").arg(t.path()).arg("--stdout").arg("-q").output().unwrap();
    assert!(audit.status.success());
    let report: serde_json::Value = serde_json::from_slice(&audit.stdout).unwrap();
    assert!(report["suggestions"].as_array().is_some_and(|s| !s.is_empty()));

    // Not a git repository: a write refuses, a dry run prints the diff.
    let dry = Command::new(bin).arg("annotate").arg(t.path()).output().unwrap();
    assert!(dry.status.success() && String::from_utf8_lossy(&dry.stdout).contains("+--** SSC-EWI-DBTSQL0007"));
    let w = Command::new(bin).arg("annotate").arg(t.path()).arg("--write").output().unwrap();
    assert!(!w.status.success());
}

#[test]
fn paths_and_error_exit_work_across_platforms() {
    let bin = env!("CARGO_BIN_EXE_dbt-quality");
    let project = TempProject::new(&[
        ("models/folder with spaces/left/orders.sql", "select 1 as id"),
        ("models/folder with spaces/right/orders.sql", "select 2 as id"),
    ]);
    let audit = Command::new(bin).arg("audit").arg(project.path()).args(["--stdout", "--quiet", "--fail-on-error"]).output().unwrap();
    assert_eq!(audit.status.code(), Some(1));
    let report: serde_json::Value = serde_json::from_slice(&audit.stdout).unwrap();
    let duplicate = report["suggestions"].as_array().unwrap().iter()
        .find(|finding| finding["rule_id"] == "SSC-EWI-DBTPRJ0020").unwrap();
    assert_eq!(duplicate["level"], "error");
    let file = duplicate["file"].as_str().unwrap();
    assert!(file.starts_with("models/folder with spaces/"), "{file}");
    assert!(!file.contains('\\'), "{file}");
    let lint = Command::new(bin).arg("lint").arg(project.path()).args(["--strict", "--format", "json"]).output().unwrap();
    assert_eq!(lint.status.code(), Some(1));
    let tasks = Command::new(bin).arg("setup-tasks").arg(project.path()).output().unwrap();
    assert!(tasks.status.success());
    let config: serde_json::Value = serde_json::from_str(&std::fs::read_to_string(project.path().join(".vscode/tasks.json")).unwrap()).unwrap();
    assert_eq!(config["tasks"][0]["type"], "process");
}

#[test]
fn include_models_requires_html_and_keeps_json_source_free() {
    let bin = env!("CARGO_BIN_EXE_dbt-quality");
    let project = TempProject::new(&[("models/a.sql", "-- original_source_sentinel\nselect 1 as id\n")]);
    let rejected = Command::new(bin).arg("audit").arg(project.path()).args(["--include-models", "--stdout"]).output().unwrap();
    assert!(!rejected.status.success());
    assert!(String::from_utf8_lossy(&rejected.stderr).contains("--html"));
    assert!(!project.path().join("dbt-audit-suggestions.json").exists());
    let html_path = project.path().join("report.html");
    let audit = Command::new(bin).arg("audit").arg(project.path())
        .args(["--include-models", "--stdout", "--quiet", "--category", "sql", "--min-level", "warning", "--html"])
        .arg(&html_path).output().unwrap();
    assert!(audit.status.success(), "{}", String::from_utf8_lossy(&audit.stderr));
    assert!(html_path.is_file());
    assert!(String::from_utf8_lossy(&audit.stderr).contains("Sharing this report shares that text"));
    let report: serde_json::Value = serde_json::from_slice(&audit.stdout).unwrap();
    assert_eq!(report["schema_version"], "3.0");
    assert!(report.get("html").is_none());
    assert!(!String::from_utf8_lossy(&audit.stdout).contains("original_source_sentinel"));
    assert!(report["suggestions"].as_array().unwrap().iter().all(|finding| finding["category"] == "SQL" && finding["level"] != "information"));
}

#[test]
fn fix_columns_uses_scai_ddl() {
    let bin = env!("CARGO_BIN_EXE_dbt-quality");
    let ddl = concat!(env!("CARGO_MANIFEST_DIR"), "/../../tests/fixtures/scai/sample_store");
    let project = TempProject::new(&[(
        "models/store/categories.sql",
        "select\n  categoryid as CategoryID,\n  categoryname as CategoryName,\n  description as Description,\n  createddate as CreatedDate\nfrom {{ ref('stg_categories') }}\n",
    )]);
    let lint = Command::new(bin).arg("lint").arg(project.path()).args(["--format", "json", "--ddl", ddl]).output().unwrap();
    assert!(String::from_utf8_lossy(&lint.stdout).contains("SSC-EWI-DBTCOL0006"), "{}", String::from_utf8_lossy(&lint.stdout));
    let dry = Command::new(bin).arg("fix-columns").arg(project.path()).args(["--ddl", ddl]).output().unwrap();
    assert!(dry.status.success(), "{}", String::from_utf8_lossy(&dry.stderr));
    assert!(String::from_utf8_lossy(&dry.stdout).contains("COLLATE 'EN-CI-AS' as CategoryName"), "{}", String::from_utf8_lossy(&dry.stdout));
    let w = Command::new(bin).arg("fix-columns").arg(project.path()).args(["--ddl", ddl, "--write", "--allow-dirty"]).output().unwrap();
    assert!(w.status.success());
    let again = Command::new(bin).arg("fix-columns").arg(project.path()).args(["--ddl", ddl, "--format", "json"]).output().unwrap();
    let files: serde_json::Value = serde_json::from_slice(&again.stdout).unwrap();
    assert_eq!(files[0]["status"], "ok", "{files}");
}
