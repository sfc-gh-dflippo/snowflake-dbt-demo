use super::*;
use crate::discovery::build_portfolio;
use crate::testing::TempProject;

const HEAD: &str = "name: demo\nversion: '1.0'\nprofile: demo\n";

const IDENTITY_NAMES: &str = "{% macro generate_database_name(custom_database_name, node) %}{{ custom_database_name }}{% endmacro %}\n{% macro generate_schema_name(custom_schema_name, node) %}{{ custom_schema_name }}{% endmacro %}\n{% macro generate_alias_name(custom_alias_name, node) %}{{ custom_alias_name }}{% endmacro %}";

#[test]
fn r7_configured_schema_is_not_physical_evidence() {
    for naming in ["", "{% macro generate_schema_name(custom_schema_name, node) %}{{ 'OTHER_' ~ custom_schema_name }}{% endmacro %}"] {
        let t = TempProject::new(&[("dbt_project.yml",HEAD),("profiles.yml","demo:\n  target: dev\n  outputs:\n    dev:\n      type: snowflake\n      database: DB\n      schema: DEV\n"),("macros/naming.sql",naming),("models/p.sql","{{ config(database='DB',schema='S',alias='T') }} select * from {{ ref('r') }}"),("models/r.sql","select * from {{ var('db','DB') }}.S.T\nunion all select * from DB.S.T")]);
        let f = t.findings("SSC-EWI-DBTPRJ0021");
        assert_eq!(f[0].context["class"], "unresolved");
        assert!(t.findings("SSC-EWI-DBTPRJ0022").is_empty());
        assert!(!t.findings("SSC-EWI-DBTSQL0006")[0].remediation.contains("Read `{{ ref('p') }}"));
    }
}

#[test]
fn r7_verified_naming_proves_physical_relation() {
    let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("models/p.sql","{{ config(database='DB',schema='S',alias='T') }} select * from {{ ref('r') }}"),("models/r.sql","select * from {{ var('db','DB') }}.S.T")]);
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0022").len(), 1);
}

#[test]
fn r7_source_and_stage_preserve_quoted_parts() {
    for (raw, expected, quoted) in [
        (r#""db"."s"."orders""#, ["db", "s", "orders"], true),
        (r#""db.dot"."s.dot"."ord""ers""#, ["db.dot", "s.dot", "ord\"ers"], true),
        ("db.s.orders", ["DB", "S", "ORDERS"], false),
    ] {
        for stage in [false, true] {
            let sql = format!("select * from {}{raw}{}", if stage { "@" } else { "" }, if stage { "/path" } else { "" });
            let t = TempProject::new(&[("profiles.yml","demo:\n  outputs:\n    dev:\n      database: DB\n"),("models/r.sql",&sql)]);
            let pf = build_portfolio(t.path());
            let tokens = literal_reads(&sql);
            assert_eq!(tokens.len(), 1);
            let loc = read_location(&pf.projects[0], &tokens[0].parts);
            let advice = source_advice(&pf.projects[0], &loc, loc.identifier.known().unwrap(), tokens[0].stage_suffix());
            let yaml = advice.split("```yaml\n").nth(1).unwrap().split("```").next().unwrap();
            let parsed = crate::discovery::load_yaml_str(yaml).unwrap();
            let source = &parsed["sources"][0];
            let table = &source["tables"][0];
            for (key, value, expected) in [("database",&source["database"],expected[0]),("schema",&source["schema"],expected[1]),("identifier",&table["identifier"],expected[2])] {
                assert_eq!(source["quoting"][key], quoted, "{advice}");
                let value = value.as_str().unwrap();
                assert_eq!(if quoted { value.to_string() } else { value.to_uppercase() }, expected, "{advice}");
            }
            assert!(rx!(r"^[A-Za-z_][A-Za-z0-9_]*$").is_match(table["name"].as_str().unwrap()));
            if stage {
                let rendered = table["external"]["location"].as_str().unwrap();
                let parts = relation_parts(rendered.strip_prefix('@').unwrap().strip_suffix("/path").unwrap()).unwrap();
                let preserved = read_location(&pf.projects[0], &parts.iter().map(|part| RelPart::Ident((*part).into())).collect::<Vec<_>>());
                assert_eq!(compare_locations(&[&loc,&preserved],true), LocationMatch::Equal);
            }
        }
    }
}

#[test]
fn r7_quoted_rendering_preserves_target_branches() {
    let t = TempProject::new(&[("profiles.yml","demo:\n  outputs:\n    'dev\"quoted': {}\n    prod: {}\n"),("models/r.sql",r#"select * from @{{ var('db', '"db.dot"') }}."s.dot"."ord""ers"/path"#)]);
    let pf = build_portfolio(t.path());
    let token = var_relation_reads(&pf.projects[0].models[0].raw).pop().unwrap();
    let loc = read_location(&pf.projects[0], &token.parts);
    assert_eq!(loc.known().unwrap(), ("db.dot".into(), "s.dot".into(), "ord\"ers".into()));
    let advice = source_advice(&pf.projects[0], &loc, "unused", token.stage_suffix());
    let yaml = advice.split("```yaml\n").nth(1).unwrap().split("```").next().unwrap();
    let value = crate::discovery::load_yaml_str(yaml).unwrap();
    let source = &value["sources"][0];
    let environment = minijinja::Environment::new();
    for target in ["dev\"quoted", "prod", "unknown"] {
        let context = minijinja::context!(target => minijinja::context!(name => target));
        let db = environment.render_str(source["database"].as_str().unwrap(), context.clone(), &[]).unwrap();
        assert_eq!(db, if target == "unknown" { "invalid_database".into() } else { format!("<database for {target}>") });
        let stage = environment.render_str(source["tables"][0]["external"]["location"].as_str().unwrap(), context, &[]).unwrap();
        let parts = relation_parts(stage.strip_prefix('@').unwrap().strip_suffix("/path").unwrap()).unwrap();
        let location = read_location(&pf.projects[0], &parts.into_iter().map(|part| RelPart::Ident(part.into())).collect::<Vec<_>>());
        assert_eq!(location.known().unwrap(), (db, "s.dot".into(), "ord\"ers".into()));
        assert!(location.database.quoted && location.schema.quoted && location.identifier.quoted);
    }
}

#[test]
fn r7_cisco_empty_location_vars_have_one_owner() {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/cisco_estate");
    let mut pf = build_portfolio(&root);
    let report = crate::engine::run_audit(&mut pf);
    let relations: Vec<_> = report.suggestions.iter().filter(|finding| finding.rule_id.ends_with("PRJ0021") || finding.rule_id.ends_with("PRJ0022")).collect();
    assert!(relations.len() >= 87);
    let checked: BTreeSet<_> = relations.iter().flat_map(|relation| relation.context["vars"].as_array().unwrap().iter().map(|key| (relation.project.clone(), key.as_str().unwrap().to_string()))).collect();
    for declaration in report.suggestions.iter().filter(|finding| finding.rule_id.ends_with("PRJ0014")) {
        assert_eq!(declaration.context["scope"], "value_reads");
        for (project, key) in checked.iter().filter(|(project, _)| project == &declaration.project) {
            assert!(!declaration.context["vars"].as_array().unwrap().contains(&json!(key)), "{project}: {key}");
        }
    }
    assert!(checked.len() >= 50, "checked {}", checked.len());
}

#[test]
fn r7_empty_vars_delegate_by_use_across_files() {
    let t = TempProject::new(&[("dbt_project.yml","name: demo\nversion: '1.0'\nvars:\n  location: ''\n  mixed: ''\n  configured: ''\n"),("models/a.sql","select * from {{ var('location') }}.S.T join {{ var('mixed') }}.S.U on true"),("models/z.sql","{{ config(schema=var('configured')) }} select 1 where value = {{ var('mixed') }}")]);
    let f = t.findings("SSC-EWI-DBTPRJ0014");
    assert_eq!(f.len(),1);
    assert_eq!(f[0].context["vars"],json!(["mixed"]));
    assert_eq!(f[0].context["scope"],"value_reads");
    assert!(f[0].evidence.contains("models/z.sql"));
    assert!(f[0].remediation.contains("Do not delete"));
    let relation = t.findings("SSC-EWI-DBTPRJ0021");
    assert!(relation.iter().all(|finding| finding.remediation.contains("remaining value reads")));
}

#[test]
fn relation_classes_and_location_mismatch() {
    let producer = "{{ config(database='DB',schema='S',alias='T') }} select 1";
    let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("dbt_project.yml",HEAD),("models/p.sql",producer),("models/r.sql","select * from {{ var('db', 'DB') }}.S.T\nunion all select * from {{ var('db','DB') }}.S.T")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert_eq!(f.len(),1);
    assert_eq!(f[0].context["class"],"same_project");
    assert!(f[0].remediation.contains("Change all 2 reads"));
    assert!(f[0].remediation.contains("ref('p')"));
    let t = TempProject::new(&[("dbt_project.yml",HEAD),("models/p.sql",producer),("models/r.sql","select * from {{ var('db', 'OTHER') }}.S.T")]);
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0021")[0].context["class"],"external");
    let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("dbt_project.yml",HEAD),("models/p.sql",producer),("models/q.sql",producer),("models/r.sql","select * from {{ var('db', 'DB') }}.S.T")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert_eq!(f[0].context["class"],"multiwriter");
    assert!(f[0].remediation.contains("PRJ0020"));
    let t = TempProject::new(&[("a/macros/naming.sql",IDENTITY_NAMES),("a/dbt_project.yml",HEAD),("a/models/p.sql",producer),("b/dbt_project.yml","name: b\nversion: '1.0'\nprofile: demo"),("b/models/r.sql","select * from {{ var('db','DB') }}.S.T")]);
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0021")[0].context["class"],"cross_project");
}

#[test]
fn cycle_forms_and_incremental_guard() {
    for read in ["{{ var('db','DB') }}.S.T", "DB.S.T", "{{ source('s','T') }}"] {
        let sql = format!("select * from {read}");
        let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("dbt_project.yml",HEAD),("models/p.sql","{{ config(database='DB',schema='S',alias='T',materialized='table') }} select * from {{ ref('r') }}"),("models/r.sql",&sql),("models/s.yml","sources:\n  - name: s\n    database: DB\n    schema: S\n    tables:\n      - name: T")]);
        let f = t.findings("SSC-EWI-DBTPRJ0022");
        assert_eq!(f.len(),1,"{read}");
        for needle in ["p.sql", "r.sql", "{{ this }}", "is_incremental()", "full-refresh", "materialized='incremental'"] { assert!(f[0].remediation.contains(needle),"{needle}"); }
        assert!(t.findings("SSC-EWI-DBTPRJ0021").is_empty());
        assert!(t.findings("SSC-EWI-DBTSQL0006").is_empty());
    }
    let t = TempProject::new(&[("models/p.sql","{{ config(materialized='incremental') }}\n{% if is_incremental() %} select * from {{ this }} {% else %} select 1 {% endif %}")]);
    assert!(t.findings("SSC-EWI-DBTPRJ0022").is_empty());
    let t = TempProject::new(&[("models/p.sql","{{ config(materialized='incremental') }}\nselect * from {{ this }}")]);
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0022").len(),1);
}

#[test]
fn proposed_cross_project_edges_close_cycle() {
    let t = TempProject::new(&[("a/macros/naming.sql",IDENTITY_NAMES),("b/macros/naming.sql",IDENTITY_NAMES),("a/dbt_project.yml",HEAD),("a/models/a.sql","{{ config(database='DB',schema='S',alias='A') }} select * from {{ var('db','DB') }}.S.B"),("b/dbt_project.yml","name: b\nversion: '1.0'\nprofile: demo"),("b/models/b.sql","{{ config(database='DB',schema='S',alias='B') }} select * from {{ var('db','DB') }}.S.A")]);
    let f = t.findings("SSC-EWI-DBTPRJ0022");
    assert_eq!(f.len(),2);
    assert!(f.iter().all(|s| s.remediation.contains("proposed relation-read edges") && s.remediation.contains("While the projects stay separate")));
}

#[test]
fn external_stage_policy_and_literal_alignment() {
    let t = TempProject::new(&[("models/v.sql","select * from {{ var('db','DB') }}.LAND.T"),("models/l.sql","select * from DB.LAND.T"),("models/st.sql","select * from @{{ var('db','DB') }}.LAND.ST/path"),("macros/stage.sql","{% macro stage() %} select * from @DB.LAND.ST {% endmacro %}")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert!(f.iter().any(|s| s.context["class"] == "stage" && s.remediation.contains("stage_external_sources") && s.remediation.contains("EXECUTE DBT PROJECT remains unverified")));
    assert!(f.iter().any(|s| s.remediation.contains("source('land', 'T')")));
    assert!(t.findings("SSC-EWI-DBTSQL0006").iter().any(|s| s.remediation.contains("source('land', 'T')")));
    for s in f { for bad in ["var(","--target","with its default"] { assert!(!s.remediation.contains(bad),"{bad}: {}",s.remediation); } }
}

#[test]
fn ownership_and_empty_undeclared_vars() {
    let t = TempProject::new(&[("models/r.sql","{{ config(database=var('db','')) }} select * from {{ var('missing') }}.S.T\nselect {{ var('missing') }} as value"),("models/p.sql","{{ config(schema=var('s','')) }} select 1")]);
    let f = t.findings("SSC-EWI-DBTPRJ0016");
    assert_eq!(f.len(),1); assert_eq!(f[0].line,Some(2));
    let f = t.findings("SSC-EWI-DBTPRJ0021"); assert_eq!(f.len(),1); assert!(f[0].remediation.contains("no longer fails"));
    let f = t.findings("SSC-EWI-DBTPRJ0009"); assert_eq!(f.len(),1); assert!(f[0].file.ends_with("p.sql")); assert!(!f[0].remediation.contains("with its default"));
    let t = TempProject::new(&[("models/r.sql","--select * from {{ var('db') }}.S.T\n{{ config(pre_hook=\"select * from {{ var('db','DB') }}.S.T\") }}\nselect {{ var('value', 1) }} as v")]);
    assert!(t.findings("SSC-EWI-DBTPRJ0021").is_empty());
    assert!(t.findings("SSC-EWI-DBTINC0019")[0].remediation.contains("source('s', 'T')"));
}

#[test]
fn source_regressions_single_block_and_identifiers() {
    let t = TempProject::new(&[("models/s.yml","sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: t\n      - name: t\n"),("models/r.sql","select * from {{ source('raw','t') }}")]);
    let f = t.findings("SSC-EWI-DBTPRJ0019"); assert_eq!(f.len(),1); assert!(f[0].remediation.contains("redundant repeated table entry"));
    let t = TempProject::new(&[("a/dbt_project.yml",HEAD),("b/dbt_project.yml","name: b\nversion: '1.0'\nprofile: demo"),("a/models/s.yml","sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_A"),("b/models/s.yml","sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_B")]);
    let f = t.findings("SSC-EWI-DBTPRJ0019"); assert_eq!(f.len(),1); assert_eq!(f[0].context["class"],"unresolved"); assert!(f[0].remediation.contains("Do not delete or coalesce"));
}

#[test]
fn mixed_literal_prefix_and_default_do_not_hide_reads() {
    let t = TempProject::new(&[("models/r.sql","select * from DB.S.{{ var('table','T') }}\nselect {{ var('table') }} as value")]);
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0021").len(),1);
    assert!(t.findings("SSC-EWI-DBTSQL0006").is_empty());
    assert_eq!(t.findings("SSC-EWI-DBTPRJ0016").len(),1);
}

#[test]
fn review_quoted_vars_preserve_relation_identity() {
    let producer = "{{ config(database='DB',schema='S',alias='T') }} select 1";
    for (head, read) in [
        (HEAD, r#"select * from {{ var('db', '"db"') }}.S.T"#),
        ("name: demo\nversion: '1.0'\nvars:\n  db: '\"db\"'\n", "select * from {{ var('db') }}.S.T"),
        (HEAD, r#"select * from {{ var('db', '"EXTRA.DB"') }}.S.T"#),
        (HEAD, r#"select * from {{ var('location', '"db"."S"') }}.T"#),
    ] {
        let t = TempProject::new(&[("dbt_project.yml",head),("models/p.sql",producer),("models/r.sql",read)]);
        let f = t.findings("SSC-EWI-DBTPRJ0021");
        assert_eq!(f[0].context["class"], "external", "{read}");
        assert!(!f[0].remediation.contains("ref('p')"));
        assert!(t.findings("SSC-EWI-DBTPRJ0022").is_empty());
    }
}

#[test]
fn review_relation_parts_never_discard_extra_components() {
    let t = TempProject::new(&[("models/p.sql","{{ config(database='DB',schema='S',alias='T') }} select 1"),("models/r.sql","select * from {{ var('db','EXTRA.DB') }}.S.T")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert_ne!(f[0].context["class"], "same_project");
    assert!(!f[0].remediation.contains("Read `{{ ref('p') }}"));
    let pf = build_portfolio(t.path());
    let loc = read_location(&pf.projects[0], &[RelPart::Ident("EXTRA".into()), RelPart::Ident("DB".into()), RelPart::Ident("S".into()), RelPart::Ident("T".into())]);
    assert!(loc.known().is_none());
}

#[test]
fn review_source_quoted_defaults_stay_different() {
    for database in [r#"{{ var('db', '"db"') }}"#, r#"{{ env_var('DB', '"db"') }}"#] {
        let yaml = format!("sources:\n  - name: raw\n    database: >-\n      {database}\n    schema: S\n    tables:\n      - name: T\n");
        let t = TempProject::new(&[("models/s.yml",&yaml),("models/p.sql","{{ config(database='DB',schema='S',alias='T') }} select * from {{ source('raw','T') }}")]);
        let pf = build_portfolio(t.path());
        let reads = analyze(&pf);
        let read = reads.iter().find(|r| r.form == Form::Source).unwrap();
        assert!(read.writers.is_empty() && read.candidates.is_empty(), "{database}: {read:?}");
        assert!(t.findings("SSC-EWI-DBTPRJ0022").is_empty());
    }
}

#[test]
fn review_literal_reads_ignore_jinja_text() {
    for text in [
        "{% set label = 'from DB.S.T' %}\nselect 1",
        "{{ log('join DB.S.T') }}\nselect 1",
        "{% if 'from DB.S.T' %} select 1 {% endif %}",
        "{# from DB.S.T #}\nselect 1",
        "select 'from DB.S.T' as label",
        "{% set label = 'from DB.S.T' ",
        "{{ 'from DB.S.T' + ",
    ] {
        assert!(literal_reads(text).is_empty(), "{text}");
        let sql = format!("{{{{ config(database='DB',schema='S',alias='T') }}}}\n{text}");
        let t = TempProject::new(&[("models/p.sql",&sql)]);
        assert!(t.findings("SSC-EWI-DBTSQL0006").is_empty(), "{text}");
        assert!(t.findings("SSC-EWI-DBTPRJ0022").is_empty(), "{text}");
    }
    for text in ["{% macro read() %} select * from DB.S.T {% endmacro %}", "{% if enabled %} select * from DB.S.T {% endif %}"] {
        assert_eq!(literal_reads(text).len(), 1, "{text}");
    }
}

#[test]
fn review_grouped_advice_maps_each_site_to_location() {
    let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("models/p.sql","{{ config(database='A',schema='S',alias='T') }} select 1"),("models/r.sql","select * from {{ var('db','A') }}.S.T\nunion all select * from {{ var('db','B') }}.S.T\nunion all select * from {{ var('db','C') }}.S.T")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert_eq!(f.len(),1);
    let remediation = &f[0].remediation;
    for (line, location, remedy) in [(1,"A.S.T","ref('p')"),(2,"B.S.T","source('b_s', 'T')"),(3,"C.S.T","source('c_s', 'T')")] {
        let label = format!("models/r.sql:{line} ({location}):");
        let section = remediation.split(&label).nth(1).unwrap_or_else(|| panic!("Missing {label}: {remediation}"));
        let section = section.split("\nRead ").next().unwrap();
        assert!(section.contains(remedy), "{label}: {section}");
        if line > 1 { assert!(!section.contains("ref('p')")); }
    }
    assert_eq!(remediation.matches(LOCATION_FIX).count(), 1);
}

#[test]
fn review_incremental_guards_are_executable_and_branch_specific() {
    for (body, guarded) in [
        ("{# {% if is_incremental() %} #}\nselect * from {{ this }}", false),
        ("{% set label = '{% if is_incremental() %}' %}\nselect * from {{ this }}", false),
        ("{% if\n is_incremental()\n %}\nselect * from {{ this }}\n{% else %} select 1 {% endif %}", true),
        ("{% if is_incremental() and enabled %} select * from {{ this }} {% endif %}", true),
        ("{% if enabled and (is_incremental()) %} select * from {{ this }} {% endif %}", true),
        ("{% if is_incremental() or enabled %} select * from {{ this }} {% endif %}", false),
        ("{% if not is_incremental() %} select * from {{ this }} {% endif %}", false),
        ("{% if is_incremental() %} select 1 {% else %} select * from {{ this }} {% endif %}", false),
        ("{% if enabled %} select 1 {% elif is_incremental() and ready %} select * from {{ this }} {% endif %}", true),
        ("{% if is_incremental() %}{% if enabled %} select 1 {% else %} select * from {{ this }} {% endif %}{% endif %}", true),
        ("{% if is_incremental() %}{% macro m() %} select * from {{ this }} {% endmacro %}{% endif %}", false),
    ] {
        let sql = format!("{{{{ config(materialized='incremental') }}}}\n{body}");
        let t = TempProject::new(&[("models/p.sql",&sql)]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0022").is_empty(), guarded, "{body}");
    }
}

#[test]
fn review_stage_location_tracks_targets_and_suffix() {
    let t = TempProject::new(&[("dbt_project.yml",HEAD),("profiles.yml","demo:\n  outputs:\n    dev:\n      database: DEV_DB\n    prod:\n      database: PROD_DB\n"),("models/r.sql","select * from @{{ var('db','DEV_DB') }}.LAND.ST/path")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    let advice = &f[0].remediation;
    assert!(!advice.contains("location: '@DEV_DB"), "{advice}");
    assert!(advice.contains("@<database for dev>.LAND.ST/path"), "{advice}");
    assert!(advice.contains("@<database for prod>.LAND.ST/path"), "{advice}");
    assert!(advice.contains("EXECUTE DBT PROJECT remains unverified"));
}

#[test]
fn review_quoted_identity_controls_and_unresolved_sites() {
    for (producer_db, read_db, class) in [("db", "\"DB\"", "same_project"), ("db", "\"db\"", "external"), ("\"EXTRA.DB\"", "\"EXTRA.DB\"", "same_project")] {
        let producer = format!("{{{{ config(database='{producer_db}',schema='S',alias='T') }}}} select 1");
        let read = format!("select * from {{{{ var('db','{read_db}') }}}}.S.T");
        let t = TempProject::new(&[("macros/naming.sql",IDENTITY_NAMES),("models/p.sql",&producer),("models/r.sql",&read)]);
        assert_eq!(t.findings("SSC-EWI-DBTPRJ0021")[0].context["class"],class,"{producer_db}: {read_db}");
    }
    let t = TempProject::new(&[("models/p.sql","{{ config(database='A',schema='S',alias='T') }} select 1"),("models/r.sql","select * from {{ var('first') }}.S.T\nunion all select * from {{ var('second') }}.S.T")]);
    let f = t.findings("SSC-EWI-DBTPRJ0021");
    assert_eq!(f.len(),1);
    for (line, key) in [(1,"first"),(2,"second")] {
        let label = format!("models/r.sql:{line} (<unresolved: var `{key}` is not declared and has no default>.S.T):");
        let section = f[0].remediation.split(&label).nth(1).unwrap().split("\nRead ").next().unwrap();
        assert!(section.contains("do not choose a producer from the table name alone"));
    }
}

#[test]
fn review_stage_literal_hook_and_rendered_mapping() {
    for (sql, rule) in [("select * from @DEV_DB.LAND.ST/path", "SSC-EWI-DBTSQL0006"), ("{{ config(pre_hook=\"select * from @{{ var('db','DEV_DB') }}.LAND.ST/path\") }} select 1", "SSC-EWI-DBTINC0019")] {
        let t = TempProject::new(&[("dbt_project.yml",HEAD),("profiles.yml","demo:\n  outputs:\n    dev:\n      database: DEV_DB\n    prod:\n      database: PROD_DB\n"),("models/r.sql",sql)]);
        let f = t.findings(rule);
        let yaml = f[0].remediation.split("```yaml\n").nth(1).unwrap().split("```").next().unwrap();
        let value = crate::discovery::load_yaml_str(yaml).unwrap();
        let source = &value["sources"][0];
        let database = source["database"].as_str().unwrap();
        let location = source["tables"][0]["external"]["location"].as_str().unwrap();
        let environment = minijinja::Environment::new();
        for target in ["dev", "prod", "unknown"] {
            let context = minijinja::context!(target => minijinja::context!(name => target));
            let database = environment.render_str(database, context.clone(), &[]).unwrap();
            let location = environment.render_str(location, context, &[]).unwrap();
            assert_eq!(location, format!("@{database}.LAND.ST/path"));
        }
    }
}

#[test]
fn expression_from_is_not_a_relation() {
    for sql in [
        "select extract(year from orders_base.order_date), extract(quarter from orders_base.order_date), extract(month from orders_base.order_date)",
        "select extract(year from coalesce(orders_base.order_date, current_date()))",
        "select trim('x' from customer.name), substring(customer.name from customer.offset)",
    ] {
        assert!(literal_reads(sql).is_empty(), "{sql}");
        let t = TempProject::new(&[("models/r.sql",sql)]);
        assert!(t.findings("SSC-EWI-DBTSQL0006").is_empty(), "{sql}");
    }
    for sql in [
        "select extract(year from orders_base.order_date) from DB.S.ORDERS orders_base",
        "select coalesce((select max(order_date) from DB.S.ORDERS), current_date())",
        "select * from (select extract(year from o.order_date) as year from DB.S.ORDERS o) nested",
        "select * from DB.S.ORDERS o join (select * from DB.S.CUSTOMERS) c on true",
        "{% macro m() %} select extract(year from o.dt) from DB.S.ORDERS o {% endmacro %}",
    ] {
        let reads = literal_reads(sql);
        assert!(!reads.is_empty(), "{sql}");
        assert!(reads.iter().all(|read| read.text.starts_with("DB.S.")), "{sql}: {reads:?}");
        if sql.contains("DB.S.CUSTOMERS") { assert_eq!(reads.len(),2); }
    }
}

#[test]
fn literal_span_includes_relation_keyword() {
    for (sql, line, column, end_column, evidence) in [
        ("select *\nfrom analytics.staging.archived_orders",2,1,39,"from analytics.staging.archived_orders"),
        ("SELECT *\nFROM analytics.raw_visits",2,1,26,"FROM analytics.raw_visits"),
        ("select * from cte\n  JOIN analytics.raw_visits v on true",2,3,28,"JOIN analytics.raw_visits"),
    ] {
        let t = TempProject::new(&[("models/r.sql",sql)]);
        let findings = t.findings("SSC-EWI-DBTSQL0006");
        assert_eq!(findings.len(),1);
        assert_eq!(findings[0].line,Some(line));
        assert_eq!(findings[0].column,Some(column));
        assert_eq!(findings[0].end_column,Some(end_column));
        assert_eq!(findings[0].evidence,evidence);
        let read = literal_reads(sql).pop().unwrap();
        assert_eq!(&sql[read.start..read.end],read.text);
    }
}

#[test]
fn temporary_stage_advice_is_conditional() {
    let sql = "{% macro log() %}{% set query %} CREATE TEMPORARY STAGE TMP; PUT file://log @TMP; select * from @TMP {% endset %}{% do run_query(query) %}{% endmacro %}";
    let t = TempProject::new(&[("macros/log.sql",sql)]);
    let findings = t.findings("SSC-EWI-DBTPRJ0021");
    assert_eq!(findings.len(),1);
    for text in ["confirm its lifetime and location with the owner", "retain that workflow", "Only after that confirmation", "EXECUTE DBT PROJECT remains unverified"] {
        assert!(findings[0].remediation.contains(text),"{text}");
    }
}

#[test]
fn cisco_cycle_and_cross_project_candidates() {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/cisco_estate");
    let pf = build_portfolio(&root);
    let f = findings(&pf,true);
    assert!(f.iter().any(|s| s.remediation.contains("WI_BKGS_MSR_ANNUITY_PRDT_AMORZ_12.sql") && s.remediation.contains("{{ this }}") && s.remediation.contains("full-refresh")));
    let f = findings(&pf,false);
    for project in ["cisco_audit_cost", "cisco_bookings_order_month"] { assert!(f.iter().any(|s| s.project_path == project && s.context["table"] == "MT_RSTD_BKGS_MSR_ANNUITY"),"{project}"); }
    assert!(f.iter().any(|s| s.context["class"] == "external"));
}
