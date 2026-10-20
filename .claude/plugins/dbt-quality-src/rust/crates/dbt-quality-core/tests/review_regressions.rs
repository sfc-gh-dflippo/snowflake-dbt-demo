use dbt_quality_core::jinja::summarize;
use dbt_quality_core::model::Suggestion;
use dbt_quality_core::testing::TempProject;
use regex::Regex;

const SOURCES: &str = "SSC-EWI-DBTPRJ0019";
const MODELS: &str = "SSC-EWI-DBTPRJ0020";

fn diagnostic(finding: &Suggestion) -> String {
    format!("{}\n{}\n{}\n{:?}", finding.message, finding.evidence, finding.remediation, finding.context)
}

fn diagnostics(findings: &[Suggestion]) -> String {
    findings.iter().map(diagnostic).collect::<Vec<_>>().join("\n")
}

fn advice(findings: &[Suggestion]) -> String {
    findings.iter().map(|finding| finding.remediation.as_str()).collect::<Vec<_>>().join("\n")
}

fn has_any(text: &str, words: &[&str]) -> bool {
    let lower = text.to_lowercase();
    words.iter().any(|word| lower.contains(word))
}

fn clauses(text: &str) -> impl Iterator<Item = &str> {
    text.split([';', '\n']).flat_map(|line| line.split(". "))
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct ReadCall {
    kind: String,
    args: Vec<String>,
}

fn has_site(text: &str, site: &str) -> bool {
    Regex::new(&format!(r"(^|[^A-Za-z0-9_./:-]){}($|[^A-Za-z0-9_/:-])", regex::escape(site))).unwrap().is_match(text)
}

fn read_call(code: &str) -> Result<ReadCall, String> {
    let parsed = summarize(&format!("{{{{ {code} }}}}"), "remediation.sql");
    let [call] = parsed.calls.as_slice() else { return Err(format!("not one literal read: {code}")); };
    let args: Option<Vec<String>> = call.args.iter().map(|arg| arg.as_str().map(str::to_string)).collect();
    let args = args.ok_or_else(|| format!("nonliteral read: {code}"))?;
    if parsed.parse_error.is_some() || !call.kwargs.is_empty() || !matches!((call.name.as_str(), args.len()), ("source", 2) | ("ref", 1 | 2)) {
        return Err(format!("unsupported read: {code}"));
    }
    Ok(ReadCall { kind: call.name.clone(), args })
}

// This recognizes only the report's explicit `old` to `new` at sites format
// and `old` unchanged at sites. Other prose is an error, not inferred ownership.
fn target_at(text: &str, site: &str, original: &str) -> Result<Option<ReadCall>, String> {
    let original = read_call(original)?;
    let mapping = Regex::new(r"`((?:source|ref)\([^`]+\))`\s+(?:to\s+`((?:source|ref)\([^`]+\))`|unchanged)\s+at\s+([A-Za-z0-9_./:-]+(?:,\s*[A-Za-z0-9_./:-]+)*)").unwrap();
    let mut target = None;
    for clause in clauses(text).filter(|clause| has_site(clause, site)) {
        if has_any(clause, &["do not", "don't", "never", "example", "instead of"]) {
            return Err(format!("non-instruction at {site}: {clause}"));
        }
        let mut matched = false;
        for pair in mapping.captures_iter(clause).filter(|pair| has_site(&pair[3], site)) {
            matched = true;
            if read_call(&pair[1])? != original || target.is_some() {
                return Err(format!("wrong original or multiple mappings at {site}: {clause}"));
            }
            target = Some(match pair.get(2) {
                Some(new) => read_call(new.as_str())?,
                None => original.clone(),
            });
        }
        if !matched {
            return Err(format!("unsupported call-site advice at {site}: {clause}"));
        }
    }
    Ok(target)
}

fn removes_member(text: &str, member: &str) -> bool {
    // Strip only the prohibited verbs, not their clause or other operations.
    let prohibition = Regex::new(r"(?i)\b(?:do not|don't|never)\s+(?:remove|delete|drop|coalesce)(?:\s+(?:or|and)\s+(?:remove|delete|drop|coalesce))*").unwrap();
    let action = Regex::new(r"(?i)\b(?:remove|delete|drop|coalesce)\b").unwrap();
    clauses(text).any(|clause| {
        let affirmative = prohibition.replace_all(clause, "prohibited");
        action.find_iter(&affirmative).any(|verb| {
            let object = affirmative[verb.end()..].split([',', ';']).next().unwrap_or_default();
            let object = object.split("prohibited").next().unwrap_or_default();
            let object = object.split(" but ").next().unwrap_or_default();
            object.contains(member) || has_any(object, &["these table definitions", "all declarations", "other files", "both writers"])
        })
    })
}

fn keeps_block(text: &str, name: &str, site: &str, final_name: &str) -> bool {
    clauses(text).any(|clause| {
        let clause = clause.trim();
        (clause.starts_with("Keep ") || clause.starts_with("Retain "))
            && clause.contains(&format!("`{name}`")) && has_site(clause, site)
            && if name == final_name { !clause.contains("rename") } else { clause.contains(&format!("rename it to `{final_name}`")) }
    })
}

#[test]
fn oracle_exact_sites_and_original_calls_determine_each_rewrite() {
    let text = "Change `ref('a', 'x')` to `ref('a_new')` at a/use.sql:1, and `ref('b', 'x')` to `ref('b_new')` at b/use.sql:10.";
    assert_eq!(target_at(text, "a/use.sql:1", "ref('a','x')").unwrap(), Some(read_call("ref('a_new')").unwrap()));
    assert_eq!(target_at(text, "b/use.sql:10", "ref('b','x')").unwrap(), Some(read_call("ref('b_new')").unwrap()));
    assert_eq!(target_at(text, "b/use.sql:1", "ref('b','x')").unwrap(), None);
    assert!(!has_site("other/a/use.sql:1", "a/use.sql:1"));
    assert!(!has_site("a/use.sql:10", "a/use.sql:1"));
    assert!(target_at(text, "a/use.sql:1", "ref('b','x')").is_err());
    assert_eq!(target_at("Keep `source('raw', 't')` unchanged at use.sql:1.", "use.sql:1", "source('raw','t')").unwrap(), Some(read_call("source('raw','t')").unwrap()));
}

#[test]
fn oracle_rejects_ambiguous_negated_and_unsupported_rewrites() {
    for text in [
        "Do not change `ref('x')` to `ref('bad')` at use.sql:1.",
        "For example `ref('x')` to `ref('bad')` at use.sql:1.",
        "Change `ref('x')` to `ref(var('new'))` at use.sql:1.",
        "Change `ref('x')` to `ref('y')` at use.sql:1; change `ref('x')` to `ref('z')` at use.sql:1.",
        "Use `ref('y')` at use.sql:1.",
        "Change `ref('x')` to `ref('y')` near use.sql:1.",
    ] {
        assert!(target_at(text, "use.sql:1", "ref('x')").is_err(), "{text}");
    }
    assert!(read_call("ref()").is_err());
    assert!(read_call("ref('x', version=2)").is_err());
}

#[test]
fn oracle_prohibition_does_not_hide_another_members_deletion() {
    assert!(!removes_member("Do not delete or coalesce `w`.", "`w`"));
    assert!(!removes_member("Delete `x`, but do not remove `w`.", "`w`"));
    assert!(removes_member("Do not delete `x`, but remove `w`.", "`w`"));
    assert!(removes_member("Retain every declaration. Delete models/a.yml:6.", "models/a.yml:6"));
    assert!(removes_member("Keep both writers. Delete the other files.", "models/m_C/z.sql"));
}

#[test]
fn f1_single_source_block_reports_both_duplicate_table_sites() {
    let project = TempProject::new(&[
        ("models/s.yml", "version: 2\nsources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: t\n      - name: t\n"),
        ("models/r.sql", "select * from {{ source('raw', 't') }}"),
    ]);
    let findings = project.findings(SOURCES);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let finding = &findings[0];
    assert_eq!(finding.context["case"].as_str(), Some("duplicate_table"), "{finding:#?}");
    assert_eq!(finding.context["class"].as_str(), Some("consolidate"), "{finding:#?}");
    assert!(finding.message.contains("raw.t"), "{finding:#?}");
    for site in ["models/s.yml:7", "models/s.yml:8"] {
        assert!(has_site(&finding.message, site), "missing repeated-table site {site}: {finding:#?}");
    }
    let remediation = &finding.remediation;
    assert!(has_any(remediation, &["remove", "delete", "drop"]) && has_any(remediation, &["redundant", "repeated", "duplicate"]), "{remediation}");
    assert!(has_any(remediation, &["table"]) && has_any(remediation, &["keep", "retain"]), "{remediation}");
    assert!(!removes_member(remediation, "`raw`"), "remove a duplicate table entry, not its only source block: {remediation}");
}

fn assert_distinct_source_identifiers_preserved(project: &TempProject, declarations: [&str; 2], readers: [&str; 2]) {
    let findings = project.findings(SOURCES);
    assert!(!findings.is_empty(), "conflicting logical table names need a finding");
    let output = diagnostics(&findings);
    let remediation = advice(&findings);
    for site in declarations.into_iter().chain(readers) {
        assert!(has_site(&output, site), "missing declaration/read ownership for {site}: {output}");
    }
    if findings.iter().any(|finding| finding.context["class"].as_str() == Some("unresolved")) {
        assert!(remediation.contains("Retain every distinct physical relation") && remediation.contains("preserve each identifier"), "unresolved advice must retain the definitions: {remediation}");
        assert!(remediation.contains("Do not delete or coalesce"), "{remediation}");
        for declaration in declarations {
            let file = declaration.rsplit_once(':').unwrap().0;
            assert!(!removes_member(&remediation, file), "contradictory deletion of {declaration}: {remediation}");
        }
        assert!(!removes_member(&remediation, "`orders`"), "{remediation}");
        assert!(!remediation.contains("` to `"), "unresolved ownership must not redirect reads: {remediation}");
        return;
    }
    assert!(findings.iter().all(|finding| matches!(finding.context["class"].as_str(), Some("consolidate" | "rename"))), "{findings:#?}");
    let mut targets = vec![];
    for (reader, declaration, identifier) in [(readers[0], declarations[0], "ORDERS_A"), (readers[1], declarations[1], "ORDERS_B")] {
        let target = target_at(&remediation, reader, "source('raw', 'orders')").unwrap().expect("reader needs a rewrite or explicit unchanged ownership");
        assert_eq!(target.kind, "source", "{target:?}");
        let rendered = format!("source('{}', '{}')", target.args[0], target.args[1]);
        assert!(clauses(&remediation).any(|clause| {
            let clause = clause.trim();
            (clause.starts_with("Keep ") || clause.starts_with("Retain "))
                && clause.contains(&rendered) && clause.contains(identifier) && has_site(clause, declaration)
        }), "require an explicit retained destination -> original declaration -> identifier association for {reader}; diagnostics alone do not establish it: {remediation}");
        targets.push(target);
    }
    assert_ne!(targets[0], targets[1], "distinct physical relations cannot have the same destination: {remediation}");
}

#[test]
fn f2_same_logical_table_preserves_distinct_physical_identifiers() {
    let project = TempProject::new(&[
        ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
        ("a/models/s.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_A\n"),
        ("a/models/r.sql", "select * from {{ source('raw', 'orders') }}"),
        ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
        ("b/models/s.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_B\n"),
        ("b/models/r.sql", "select * from {{ source('raw', 'orders') }}"),
    ]);
    assert_distinct_source_identifiers_preserved(&project, ["a/models/s.yml:6", "b/models/s.yml:6"], ["a/models/r.sql:1", "b/models/r.sql:1"]);
}

#[test]
fn f2_tables_moved_into_kept_block_preserve_distinct_identifiers() {
    let project = TempProject::new(&[
        ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
        ("a/models/s.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: customers\n"),
        ("a/models/r.sql", "select * from {{ source('raw', 'customers') }} a join {{ source('raw', 'customers') }} b on a.id = b.id"),
        ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
        ("b/models/s.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_A\n"),
        ("b/models/r.sql", "select * from {{ source('raw', 'orders') }}"),
        ("c/dbt_project.yml", "name: c\nversion: '1.0'\nprofile: p\n"),
        ("c/models/s.yml", "sources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: orders\n        identifier: ORDERS_B\n"),
        ("c/models/r.sql", "select * from {{ source('raw', 'orders') }}"),
    ]);
    assert_distinct_source_identifiers_preserved(&project, ["b/models/s.yml:6", "c/models/s.yml:6"], ["b/models/r.sql:1", "c/models/r.sql:1"]);
}

#[test]
fn f3_alias_reader_is_not_redirected_to_a_removed_source_table() {
    let project = TempProject::new(&[
        ("models/a.yml", "sources:\n  - name: alpha\n    database: DB\n    schema: S\n    tables:\n      - name: w\n      - name: x\n"),
        ("models/b.yml", "sources:\n  - name: beta\n    database: DB\n    schema: S\n    tables:\n      - name: oldw\n        identifier: w\n"),
        ("models/r.sql", "select * from {{ source('alpha', 'x') }} a join {{ source('alpha', 'x') }} b on a.id = b.id"),
        ("models/u.sql", "select * from {{ source('beta', 'oldw') }}"),
        ("models/w.sql", "{{ config(database='DB', schema='S') }} select 1 as k"),
    ]);
    let findings = project.findings(SOURCES);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let finding = &findings[0];
    let output = diagnostic(finding);
    for site in ["models/a.yml:2", "models/b.yml:2", "models/u.sql:1"] {
        assert!(has_site(&output, site), "missing alias/read ownership at {site}: {output}");
    }
    assert_eq!(finding.context["case"].as_str(), Some("alias"), "{finding:#?}");
    let remediation = &finding.remediation;
    if finding.context["class"].as_str() == Some("unresolved") {
        assert!(remediation.contains("Keep the existing source declarations") || remediation.contains("Retain every distinct physical relation"), "{remediation}");
        for member in ["`w`", "`oldw`", "models/a.yml", "models/b.yml"] {
            assert!(!removes_member(remediation, member), "unresolved ownership cannot remove {member}: {remediation}");
        }
        assert!(!remediation.contains("` to `"), "{remediation}");
        return;
    }
    assert_eq!(finding.context["class"].as_str(), Some("consolidate"), "{finding:#?}");
    let target = target_at(remediation, "models/u.sql:1", "source('beta','oldw')").unwrap().expect("alias reader needs an explicit destination");
    if target.kind == "source" {
        assert_eq!(target.args[1], "w", "the retained alpha.w, not an invented table, owns the read: {target:?}");
        assert!(keeps_block(remediation, "alpha", "models/a.yml:2", &target.args[0]), "destination must name the retained alpha block: {remediation}");
        assert!(!removes_member(remediation, "`w`") && !removes_member(remediation, "models/a.yml"), "reader destination is removed: {remediation}");
    } else {
        assert_eq!(target, read_call("ref('w')").unwrap(), "{remediation}");
        assert!(output.contains("models/w.sql"), "replacement ref must identify its producer: {output}");
    }
}

#[test]
fn f4_canonical_source_name_does_not_collide_with_another_location() {
    let project = TempProject::new(&[
        ("models/a.yml", "version: 2\nsources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: t\n"),
        ("models/b.yml", "version: 2\nsources:\n  - name: raw\n    database: DB\n    schema: S\n    tables:\n      - name: u\n"),
        ("models/c.yml", "version: 2\nsources:\n  - name: s\n    database: OTHER_DB\n    schema: OTHER_S\n    tables:\n      - name: t\n"),
        ("models/raw_use.sql", "select * from {{ source('raw', 't') }}"),
        ("models/existing_use.sql", "select * from {{ source('s', 't') }}"),
    ]);
    let findings = project.findings(SOURCES);
    let finding = findings.iter().find(|finding| {
        let output = diagnostic(finding);
        has_site(&output, "models/a.yml:3") && has_site(&output, "models/b.yml:3")
    }).expect("the raw blocks need consolidation or an explicit unresolved collision");
    let output = diagnostics(&findings);
    let remediation = advice(&findings);
    if finding.context["class"].as_str() == Some("unresolved") {
        assert!(has_site(&output, "models/c.yml:3") && has_any(&output, &["collision", "occupied", "conflict"]), "{output}");
        assert!(remediation.contains("Keep the existing source declarations and calls"), "{remediation}");
        for member in ["models/a.yml", "models/b.yml", "models/c.yml", "`raw`", "`s`"] {
            assert!(!removes_member(&remediation, member), "unresolved collision cannot delete {member}: {remediation}");
        }
        assert!(!remediation.contains("` to `"), "unresolved collision cannot redirect calls: {remediation}");
        return;
    }
    assert!(matches!(finding.context["class"].as_str(), Some("consolidate" | "rename")), "{finding:#?}");
    let target = target_at(&remediation, "models/raw_use.sql:1", "source('raw','t')").unwrap().or_else(|| {
        (keeps_block(&remediation, "raw", "models/a.yml:3", "raw") && remediation.contains("No `source()` call changes"))
            .then(|| read_call("source('raw','t')").unwrap())
    }).expect("rewrite or explicit unchanged raw reader");
    assert_eq!(target.kind, "source", "{target:?}");
    assert_eq!(target.args[1], "t", "{target:?}");
    assert!(keeps_block(&remediation, "raw", "models/a.yml:3", &target.args[0]), "raw read needs its retained declaration: {remediation}");
    if target.args[0] == "s" {
        let existing = target_at(&remediation, "models/existing_use.sql:1", "source('s','t')").unwrap().expect("occupied s requires a coordinated rename");
        assert_eq!(existing.kind, "source", "{existing:?}");
        assert_ne!(existing.args[0], "s", "different locations cannot both retain s: {remediation}");
        assert_eq!(existing.args[1], "t", "{existing:?}");
        assert!(keeps_block(&remediation, "s", "models/c.yml:3", &existing.args[0]), "existing reader must follow its own retained declaration: {remediation}");
    }
}

#[test]
fn f5_string_literal_whitespace_is_not_copy_equivalence() {
    let project = TempProject::new(&[
        ("models/m_A/x.sql", "select 'a  b' as value"),
        ("models/m_B/x.sql", "select 'a b' as value"),
    ]);
    let findings = project.findings(MODELS);
    assert!(!findings.is_empty(), "different SQL still has a duplicate model name");
    let output = diagnostics(&findings);
    for path in ["models/m_A/x.sql:1", "models/m_B/x.sql:1"] {
        assert!(has_site(&output, path), "{output}");
    }
    assert!(findings.iter().all(|finding| matches!(finding.context["class"].as_str(), Some("rename" | "merge" | "unresolved"))), "literal contents cannot be discarded as an identical copy: {output}");
    assert!(has_any(&advice(&findings), &["rename", "combine", "preserve", "do not delete"]), "{output}");

    let layout_only = TempProject::new(&[
        ("models/m_A/x.sql", "select 'a  b' as value"),
        ("models/m_B/x.sql", "-- same literal, different layout\nselect\n  'a  b'   as value"),
    ]);
    let copies = layout_only.findings(MODELS);
    assert_eq!(copies.len(), 1, "{copies:#?}");
    assert_eq!(copies[0].context["class"].as_str(), Some("consolidate"), "layout whitespace outside the literal is still ignorable: {copies:#?}");
}

#[test]
fn f6_mixed_name_and_relation_component_keeps_both_obligations() {
    let project = TempProject::new(&[
        ("models/m_A/x.sql", "{{ config(alias='T') }} select 1 as k"),
        ("models/m_B/x.sql", "{{ config(alias='U') }} select 2 as k"),
        ("models/m_C/z.sql", "{{ config(alias='T') }} select 3 as k"),
    ]);
    let findings = project.findings(MODELS);
    assert!(!findings.is_empty(), "both name and relation collisions need findings");
    let output = diagnostics(&findings);
    for site in ["models/m_A/x.sql:1", "models/m_B/x.sql:1", "models/m_C/z.sql:1"] {
        assert!(has_site(&output, site), "missing component member {site}: {output}");
    }
    assert!(findings.iter().all(|finding| finding.context["class"].as_str().is_some_and(|class| class != "consolidate")), "different writer logic must not be deleted as copies: {output}");
    assert!(output.contains(".T") || output.contains("`T`") || output.contains("'T'"), "the pinned T collision must be identified: {output}");
    let remediation = advice(&findings);
    if findings.iter().any(|finding| finding.context["class"].as_str() == Some("unresolved")) {
        assert!(remediation.contains("Keep all writers") || remediation.contains("Retain all writers") || remediation.contains("Preserve every writer"), "{remediation}");
        for writer in ["models/m_A/x.sql", "models/m_B/x.sql", "models/m_C/z.sql"] {
            assert!(!removes_member(&remediation, writer), "unresolved collision cannot discard {writer}: {remediation}");
        }
        assert!(has_any(&remediation, &["resolve", "confirm", "check"]), "{remediation}");
        return;
    }
    assert!(clauses(&remediation).any(|clause| {
        clause.contains("rename `models/m_B/x.sql` to `") && !has_any(clause, &["do not", "don't", "never"])
    }), "duplicate x needs an affirmative name-level resolution: {remediation}");
    let merge = findings.iter().any(|finding| {
        let members = finding.context["members"].as_array();
        let owns_writers = ["models/m_A/x.sql:1", "models/m_C/z.sql:1"].iter().all(|site| {
            members.is_some_and(|members| members.iter().any(|member| member.as_str() == Some(*site)))
        });
        owns_writers && clauses(&finding.remediation).any(|clause| {
            let clause = clause.trim();
            (clause.starts_with("Combine ") || clause.starts_with("Merge ") || clause.starts_with("Also merge "))
                && has_any(clause, &["keeping every writer", "preserv", "union all"])
                && (finding.context["class"].as_str() == Some("merge") || (clause.contains("models/m_A/x.sql") && clause.contains("models/m_C/z.sql")))
        })
    });
    assert!(merge, "require an affirmative, T-writer-specific merge obligation, not a mention of merge: {output}");
}

#[test]
fn f7_qualified_ref_to_kept_package_is_not_redirected_to_local_copy() {
    let project = TempProject::new(&[
        ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
        ("a/models/x.sql", "select 1 as k"),
        ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
        ("b/models/x.sql", "select 2 as k"),
        ("b/models/use.sql", "select * from {{ ref('a', 'x') }}"),
    ]);
    let findings = project.findings(MODELS);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let finding = &findings[0];
    assert_eq!(finding.context["class"].as_str(), Some("rename"), "{finding:#?}");
    assert_eq!(finding.context["cross_project"].as_bool(), Some(true), "{finding:#?}");
    for path in ["a/models/x.sql:1", "b/models/x.sql:1"] {
        assert!(has_site(&finding.message, path), "{finding:#?}");
    }
    assert!(finding.remediation.contains("b__x.sql"), "the b copy still needs renaming: {finding:#?}");
    if let Some(target) = target_at(&finding.remediation, "b/models/use.sql:1", "ref('a','x')").unwrap() {
        assert!(target == read_call("ref('a','x')").unwrap() || target == read_call("ref('x')").unwrap(), "kept-package read cannot move to b__x: {finding:#?}");
    }
}

#[test]
fn f7_qualified_refs_to_renamed_package_are_accounted_for_estate_wide() {
    let project = TempProject::new(&[
        ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: p\n"),
        ("a/models/x.sql", "select 1 as k"),
        ("a/models/use_b.sql", "select *\nfrom {{ ref('b', 'x') }}"),
        ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: p\n"),
        ("b/models/x.sql", "select 2 as k"),
        ("b/models/local_use.sql", "select * from {{ ref('x') }}"),
        ("c/dbt_project.yml", "name: c\nversion: '1.0'\nprofile: p\n"),
        ("c/models/report.sql", "select 3 as k"),
        ("c/models/schema.yml", "version: 2\nmodels:\n  - name: report\n    description: \"Reads {{ ref('b', 'x') }}\"\n"),
        ("c/macros/read_b.sql", "{% macro read_b() %}\nselect * from {{ ref('b', 'x') }}\n{% endmacro %}"),
    ]);
    let findings = project.findings(MODELS);
    assert_eq!(findings.len(), 1, "{findings:#?}");
    let finding = &findings[0];
    assert_eq!(finding.context["class"].as_str(), Some("rename"), "{finding:#?}");
    assert_eq!(finding.context["cross_project"].as_bool(), Some(true), "{finding:#?}");
    assert!(finding.remediation.contains("b__x.sql"), "{finding:#?}");
    for site in ["a/models/use_b.sql:2", "b/models/local_use.sql:1", "c/models/schema.yml:4", "c/macros/read_b.sql:2"] {
        let original = if site == "b/models/local_use.sql:1" { "ref('x')" } else { "ref('b','x')" };
        let target = target_at(&finding.remediation, site, original).unwrap().expect("renamed-package reader needs its update");
        assert!(target == read_call("ref('b__x')").unwrap() || target == read_call("ref('b','b__x')").unwrap(), "wrong ownership at {site}: {target:?}");
    }
}
