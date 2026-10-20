use dbt_quality_core::discovery::{build_portfolio, load_yaml_str, source_decls};
use dbt_quality_core::model::Suggestion;
use dbt_quality_core::rules::prj::shared::resolve_location;
use dbt_quality_core::testing::TempProject;
use serde_json::Value;

const RELATIONS: &str = "SSC-EWI-DBTPRJ0021";
const CYCLES: &str = "SSC-EWI-DBTPRJ0022";
const EMPTY_VARS: &str = "SSC-EWI-DBTPRJ0014";
const SINGLE_TARGET: &str = "demo:\n  target: dev\n  outputs:\n    dev:\n      type: snowflake\n      database: DB\n      schema: DEV\n";

fn source_yaml(finding: &Suggestion) -> &str {
    finding.remediation.split("```yaml\n").skip(1)
        .map(|block| block.split("```").next().unwrap())
        .find(|block| load_yaml_str(block).is_ok_and(|value| value["sources"].is_array()))
        .expect("source remediation must include parseable source YAML")
}

fn assert_source_identity(yaml: &str, expected: (&str, &str, &str)) {
    let value = load_yaml_str(yaml).unwrap();
    let source = &value["sources"][0];
    let logical_table = source["tables"][0]["name"].as_str().unwrap();
    assert!(!logical_table.is_empty());
    assert!(logical_table.chars().all(|ch| ch.is_ascii_alphanumeric() || ch == '_'), "use a logical table name, not the dotted physical identifier: {yaml}");
    let project = TempProject::new(&[("models/sources.yml", yaml), ("models/r.sql", "select 1")]);
    let portfolio = build_portfolio(project.path());
    let context = &portfolio.projects[0];
    let declarations = source_decls(context);
    assert_eq!(declarations.len(), 1, "{yaml}");
    assert_eq!(declarations[0].tables.len(), 1, "{yaml}");
    let location = resolve_location(context, &declarations[0], &declarations[0].tables[0]);
    assert_eq!(location.known(), Some((expected.0.into(), expected.1.into(), expected.2.into())), "{yaml}");
    for part in [&location.database, &location.schema, &location.identifier] {
        assert!(part.quoted, "case-sensitive physical components need quoting, not just YAML string delimiters: {yaml}");
    }
}

fn rule<'a>(findings: &'a [Suggestion], code: &str) -> Vec<&'a Suggestion> {
    findings.iter().filter(|finding| finding.rule_id == code).collect()
}

#[test]
fn default_schema_prefix_does_not_prove_a_producer_or_cycle() {
    for read in ["{{ var('db', 'DB') }}.S.T", "DB.S.T", "{{ source('raw', 'T') }}"] {
        let sql = format!("select * from {read}");
        let project = TempProject::new(&[
            ("profiles.yml", SINGLE_TARGET),
            ("models/p.sql", "{{ config(database='DB', schema='S', alias='T') }} select * from {{ ref('r') }}"),
            ("models/r.sql", &sql),
            ("models/sources.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: T\n"),
        ]);
        let findings = project.audit();
        assert!(rule(&findings, CYCLES).is_empty(), "config schema S writes DEV_S under default naming, not S: {findings:#?}");
        for finding in rule(&findings, RELATIONS) {
            assert!(matches!(finding.context["class"].as_str(), Some("external" | "unresolved")), "{finding:#?}");
        }
        for finding in findings.iter().filter(|finding| finding.rule_id == RELATIONS || finding.rule_id.ends_with("SQL0006")) {
            assert!(!finding.remediation.contains("ref('p')"), "must not redirect DB.S.T to DB.DEV_S.T: {finding:#?}");
        }
        if read.contains("var(") {
            assert_eq!(rule(&findings, RELATIONS).len(), 1, "the unproven read still needs location advice");
        }
    }
}

#[test]
fn explicit_naming_evidence_allows_a_producer_without_requiring_unsafe_inference() {
    let project = TempProject::new(&[
        ("profiles.yml", SINGLE_TARGET),
        ("macros/names.sql", "{% macro generate_database_name(custom_database_name, node) %}DB{% endmacro %}\n{% macro generate_schema_name(custom_schema_name, node) %}S{% endmacro %}\n{% macro generate_alias_name(custom_alias_name, node) %}T{% endmacro %}"),
        ("models/p.sql", "{{ config(database='DB', schema='S', alias='T') }} select 1 as id"),
        ("models/r.sql", "{{ config(materialized='ephemeral') }} select * from {{ var('db', 'DB') }}.S.T"),
    ]);
    let findings = project.findings(RELATIONS);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let finding = &findings[0];
    assert!(finding.context["producer_files"].as_array().unwrap().iter().any(|path| path == "models/p.sql"), "the physical producer or its unresolved candidate must be retained: {finding:#?}");
    match finding.context["class"].as_str() {
        Some("same_project") => assert!(finding.remediation.contains("ref('p')"), "{finding:#?}"),
        Some("unresolved") => {
            assert!(!finding.remediation.contains("ref('p')"), "unsupported naming evaluation must not redirect the read: {finding:#?}");
            assert!(finding.remediation.contains("compile") || finding.remediation.contains("confirm"), "unresolved naming needs a confirmation step: {finding:#?}");
        }
        other => panic!("explicit naming is a proven producer or an unresolved candidate, not {other:?}: {finding:#?}"),
    }
}

#[test]
fn quoted_var_parts_round_trip_through_source_yaml() {
    let project = TempProject::new(&[
        ("profiles.yml", SINGLE_TARGET),
        ("models/r.sql", r#"select * from {{ var('db', '"db.part"') }}."s.part"."orders.part""#),
    ]);
    let findings = project.findings(RELATIONS);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    assert_source_identity(source_yaml(&findings[0]), ("db.part", "s.part", "orders.part"));
}

#[test]
fn quoted_literal_parts_round_trip_through_source_yaml() {
    let project = TempProject::new(&[
        ("profiles.yml", SINGLE_TARGET),
        ("models/r.sql", r#"select * from "db"."s"."orders""#),
    ]);
    let findings = project.findings("SSC-EWI-DBTSQL0006");
    assert_eq!(findings.len(), 1, "{findings:#?}");
    assert_source_identity(source_yaml(&findings[0]), ("db", "s", "orders"));
}

#[test]
fn quoted_stage_parts_survive_each_rendered_target_branch() {
    let project = TempProject::new(&[
        ("profiles.yml", "demo:\n  target: dev\n  outputs:\n    dev:\n      database: DEV_DB\n    prod:\n      database: PROD_DB\n"),
        ("models/r.sql", r#"select * from @{{ var('db', '"db.part"') }}."s.part"."stage.part"/path"#),
    ]);
    let findings = project.findings(RELATIONS);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let yaml = source_yaml(&findings[0]);
    let value = load_yaml_str(yaml).unwrap();
    let source = &value["sources"][0];
    let database = source["database"].as_str().unwrap();
    let stage = source["tables"][0]["external"]["location"].as_str().unwrap();
    let environment = minijinja::Environment::new();
    for target in ["dev", "prod", "unknown"] {
        let context = minijinja::context!(target => minijinja::context!(name => target));
        let rendered_database = environment.render_str(database, context.clone(), &[]).unwrap();
        let rendered_stage = environment.render_str(stage, context, &[]).unwrap();
        let physical_database = rendered_database.trim().trim_matches('"');
        if target == "unknown" {
            assert_eq!(physical_database, "invalid_database", "{yaml}");
        }
        let quoted_database = format!("\"{}\"", physical_database.replace('"', "\"\""));
        let expected = format!("@{quoted_database}.\"s.part\".\"stage.part\"/path");
        let unquoted_sentinel = "@invalid_database.\"s.part\".\"stage.part\"/path";
        assert!(rendered_stage.trim() == expected || (target == "unknown" && rendered_stage.trim() == unquoted_sentinel), "target {target}: quoted dotted components must remain single SQL identifiers: {rendered_stage:?}; YAML: {yaml}");
        let mut rendered = value.clone();
        rendered["sources"][0]["database"] = Value::String(rendered_database.clone());
        let rendered_yaml = serde_json::to_string(&rendered).unwrap();
        assert_source_identity(&rendered_yaml, (physical_database, "s.part", "stage.part"));
    }
}

#[test]
fn location_only_empty_vars_delegate_instead_of_requesting_values() {
    let project = TempProject::new(&[
        ("dbt_project.yml", "name: demo\nversion: '1.0'\nprofile: demo\nvars:\n  relation_db: ''\n  config_schema: ''\n"),
        ("models/r.sql", "select * from {{ var('relation_db') }}.S.T"),
        ("models/p.sql", "{{ config(schema=var('config_schema')) }} select 1 as id"),
    ]);
    let findings = project.audit();
    assert!(rule(&findings, EMPTY_VARS).is_empty(), "location-only vars must not also be populated: {findings:#?}");
    assert_eq!(rule(&findings, RELATIONS).len(), 1, "{findings:#?}");
    assert_eq!(rule(&findings, "SSC-EWI-DBTPRJ0009").len(), 1, "{findings:#?}");
}

#[test]
fn mixed_empty_var_retains_value_read_and_scopes_relation_removal() {
    let project = TempProject::new(&[
        ("dbt_project.yml", "name: demo\nversion: '1.0'\nprofile: demo\nvars:\n  shared: ''\n  location_only: ''\n"),
        ("models/r.sql", "select * from {{ var('shared') }}.S.T\nunion all select * from {{ var('location_only') }}.S.U\n"),
        ("models/value.sql", "select\n  {{ var('shared') }} as business_value\n"),
    ]);
    let findings = project.audit();
    let empty = rule(&findings, EMPTY_VARS);
    assert_eq!(empty.len(), 1, "a genuine empty value use remains actionable: {findings:#?}");
    assert_eq!(empty[0].context["vars"], serde_json::json!(["shared"]), "{:#?}", empty[0]);
    let reads = empty[0].context["reads"].as_array().unwrap();
    assert!(!reads.is_empty());
    assert!(reads.iter().all(|read| read["var"] == "shared" && read["read_at"] == "models/value.sql:2"), "PRJ0014 must point only at retained value uses: {reads:#?}");
    let relation = rule(&findings, RELATIONS);
    assert_eq!(relation.len(), 2, "{findings:#?}");
    let shared = relation.iter().find(|finding| finding.context["vars"].as_array().is_some_and(|vars| vars.iter().any(|var| var == "shared"))).unwrap();
    assert_eq!(shared.context["read_sites"], serde_json::json!(["models/r.sql:1"]));
    let advice = shared.remediation.to_lowercase();
    assert!(advice.contains("non-relation") || advice.contains("value read") || advice.contains("value use"), "shared variable removal needs an explicit retained-value-use qualification: {shared:#?}");
    assert!(advice.split(['.', ';', '\n']).any(|clause| {
        (clause.contains("retain") || clause.contains("keep") || clause.contains("do not delete"))
            && (clause.contains("shared") || clause.contains("non-relation") || clause.contains("value") || clause.contains("declaration"))
    }), "relation migration must explicitly retain the shared declaration needed by the value read: {shared:#?}");
}

#[test]
fn project_placeholders_delegate_location_policy_without_runtime_override_retention() {
    let project = TempProject::new(&[
        ("dbt_project.yml", "name: demo\nversion: '1.0'\nprofile: demo\nvars:\n  location_db: YOUR_DB\n"),
        ("models/r.sql", "select * from {{ var('location_db') }}.S.T"),
    ]);
    let findings = project.findings("SSC-EWI-DBTPRJ0005");
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let advice = findings[0].remediation.to_lowercase();
    assert!(advice.contains("location"), "{advice}");
    assert!(["prj0009", "prj0021", "prj0022"].iter().any(|rule| advice.contains(rule)) || advice.contains("target.name"), "delegate to location policy: {advice}");
    assert!(advice.contains("target") && advice.contains("orchestration"), "existing-target verification and orchestration policy must be explicit: {advice}");
    assert!(!advice.contains("silently drops the override") && !advice.contains("expecting the real value via"), "superseded override-retention policy: {advice}");
}
