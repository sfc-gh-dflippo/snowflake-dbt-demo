//! TST rules: testing and constraint coverage.

use std::collections::BTreeSet;

use serde_json::{json, Map, Value};

use crate::discovery::{ModelFile, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural, severity, Suggestion};
use crate::rx;
use crate::sqlutil::{py_str, truthy};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTTST0001", detect: Detect::Project(tst0001) },
    Detector { code: "SSC-EWI-DBTTST0002", detect: Detect::Model(tst0002) },
    Detector { code: "SSC-EWI-DBTTST0003", detect: Detect::Model(tst0003) },
    Detector { code: "SSC-EWI-DBTTST0004", detect: Detect::Model(tst0004) },
    Detector { code: "SSC-EWI-DBTTST0005", detect: Detect::Model(tst0005) },
    Detector { code: "SSC-EWI-DBTTST0006", detect: Detect::Project(tst0006) },
    Detector { code: "SSC-EWI-DBTTST0007", detect: Detect::Project(tst0007) },
    Detector { code: "SSC-EWI-DBTTST0008", detect: Detect::Project(tst0008) },
    Detector { code: "SSC-EWI-DBTTST0009", detect: Detect::Project(tst0009) },
    Detector { code: "SSC-EWI-DBTTST0010", detect: Detect::Project(tst0010) },
    Detector { code: "SSC-EWI-DBTTST0012", detect: Detect::Model(tst0012) },
];

type Def = Map<String, Value>;

const PRIMARY_KEY_TESTS: &[&str] = &["dbt_constraints.primary_key", "primary_key"];
const UNIQUE_KEY_TESTS: &[&str] = &["dbt_constraints.unique_key", "unique_key", "unique"];
const FOREIGN_KEY_TESTS: &[&str] = &["dbt_constraints.foreign_key", "foreign_key", "relationships"];

fn is_key_constraint(n: &str) -> bool {
    PRIMARY_KEY_TESTS.contains(&n) || UNIQUE_KEY_TESTS.contains(&n) || FOREIGN_KEY_TESTS.contains(&n)
}

fn is_key_column(name: &str) -> bool {
    rx!(r"(?i)^(?:.*_id|.*_key|id|.*_sk|fk_.*|.*_fk)$").is_match(name)
}

fn test_name(t: &Value) -> Option<String> {
    match t {
        Value::String(s) => Some(s.clone()),
        Value::Object(o) => o.keys().next().cloned(),
        _ => None,
    }
}

/// Python `list(x)` on a YAML value: arrays give items, mappings give keys.
fn as_list(v: &Value) -> Vec<Value> {
    match v {
        Value::Array(a) => a.clone(),
        Value::Object(o) => o.keys().map(|k| Value::String(k.clone())).collect(),
        _ => vec![],
    }
}

fn tests_of(node: &Def) -> Vec<Value> {
    if truthy(node.get("tests")) {
        as_list(&node["tests"])
    } else {
        node.get("data_tests").map(as_list).unwrap_or_default()
    }
}

fn columns_of(def: &Def) -> Vec<&Def> {
    match def.get("columns") {
        Some(Value::Array(a)) => a.iter().filter_map(|c| c.as_object()).collect(),
        _ => vec![],
    }
}

fn column_has_key_test(column: &Def) -> bool {
    let (mut uniq, mut nn) = (false, false);
    for t in tests_of(column) {
        let Some(n) = test_name(&t) else { continue };
        if PRIMARY_KEY_TESTS.contains(&n.as_str())
            || n == "dbt_constraints.unique_key"
            || n == "unique_key"
            || FOREIGN_KEY_TESTS.contains(&n.as_str())
        {
            return true;
        }
        if n == "unique" {
            uniq = true;
        } else if n == "not_null" {
            nn = true;
        }
    }
    uniq && nn
}

fn model_level_key_covers(def: &Def, column: &str) -> bool {
    let want = column.to_lowercase();
    for t in tests_of(def) {
        let Value::Object(o) = &t else { continue };
        let Some(name) = o.keys().next() else { continue };
        if !is_key_constraint(name) {
            continue;
        }
        let Some(Value::Object(mut cfg)) = o.get(name).cloned() else { continue };
        if let Some(Value::Object(args)) = cfg.get("arguments").cloned() {
            cfg = args;
        }
        for single in ["column_name", "fk_column_name"] {
            if cfg.get(single).map(py_str).unwrap_or_default().to_lowercase() == want {
                return true;
            }
        }
        for multi in ["column_names", "fk_column_names"] {
            if let Some(Value::Array(a)) = cfg.get(multi)
                && a.iter().any(|v| py_str(v).to_lowercase() == want) {
                    return true;
                }
        }
    }
    false
}

fn has_any_key_test(def: &Def) -> bool {
    for t in tests_of(def) {
        if let Some(n) = test_name(&t)
            && (PRIMARY_KEY_TESTS.contains(&n.as_str()) || UNIQUE_KEY_TESTS.contains(&n.as_str())) {
                return true;
            }
    }
    columns_of(def).into_iter().any(column_has_key_test)
}

fn col_name(c: &Def) -> String {
    c.get("name").map(py_str).unwrap_or_default()
}

fn schema_file(m: &ModelFile, p: &ProjectContext) -> String {
    p.schema_sources.get(&m.name).cloned().unwrap_or_else(|| m.relative_path.clone())
}

fn rel(p: &ProjectContext, path: &std::path::Path) -> String {
    crate::discovery::display_path(path.strip_prefix(&p.root).unwrap_or(path))
}

fn fname(path: &std::path::Path) -> String {
    path.file_name().map(|s| s.to_string_lossy().into_owned()).unwrap_or_default()
}

/// Grain check: the first query returns duplicate keys.
/// The second query counts rows with any NULL key column.
fn grain_check(model: &str, cols: &str) -> String {
    let nulls: Vec<String> = cols.split(',').map(|c| format!("{} is null", c.trim())).collect();
    format!("select {cols}, count(*) from {{{{ ref('{model}') }}}} group by {cols} having count(*) > 1;\nselect count(*) from {{{{ ref('{model}') }}}} where {}", nulls.join(" or "))
}

/// Entity part of a key column or a model name: `hashed_customer_id` -> `hashed_customer`, `dim_customers` -> `customer`.
fn entity(name: &str) -> String {
    let n = name.to_lowercase();
    let n = rx!(r"^(?:dim|dimension|fct|fact|stg|int|fk)_").replace(&n, "");
    let n = rx!(r"_(?:id|key|sk|fk)$").replace(&n, "");
    n.strip_suffix('s').unwrap_or(&n).to_string()
}

/// FK test example for `col` on model `own`. Never points at `own`.
/// Match the column's entity to another model's entity by suffix.
/// If the parent's key has a different name, set the flag so the example
/// tells the reader to check the values first.
fn fk_example(col: &str, own: &str, p: &ProjectContext) -> (String, bool) {
    let e = entity(col);
    let same = |me: &str| !me.is_empty() && (e == me || e.ends_with(&format!("_{me}")));
    if same(&entity(own)) {
        return (format!("`{col}` resembles model `{own}`'s own entity name. Do not infer a foreign key to another model from that name alone. If the values are independently unique, consider this unique-key test after checking the data:\n\n```yaml\n      - name: {col}\n        data_tests:\n          - dbt_constraints.unique_key\n```"), false);
    }
    let parents: Vec<_> = p.models.iter().filter(|m| m.name != own && same(&entity(&m.name))).collect();
    // Prefer a dimension, then a gold model, then any match.
    let parent = parents.iter().find(|m| rx!(r"(?i)^dim").is_match(&m.name)).or(parents.iter().find(|m| m.layer == "gold")).or(parents.first());
    let (table, key) = match parent {
        Some(m) => {
            let keys: Vec<String> = p.schema_def(&m.name).map(columns_of).unwrap_or_default().into_iter().map(col_name).filter(|c| is_key_column(c)).collect();
            let key = keys.iter().find(|k| k.eq_ignore_ascii_case(col)).or(keys.first()).cloned().unwrap_or_else(|| "<parent_key>".into());
            (format!("ref('{}')", m.name), key)
        }
        None => ("ref('<parent_model>')".into(), "<parent_key>".into()),
    };
    let yaml = format!("```yaml\n      - name: {col}\n        data_tests:\n          - dbt_constraints.foreign_key:\n              pk_table_name: {table}\n              pk_column_name: {key}\n```");
    if !key.starts_with('<') && !key.eq_ignore_ascii_case(col) {
        return (format!("{yaml}\n\n`{col}` and `{key}` have different names. Check that `{col}` holds `{key}` values before you add this test."), true);
    }
    (yaml, false)
}

/// `"<path>:1"` for each model, for the report's file tabs.
fn model_files(p: &ProjectContext) -> Vec<String> {
    p.models.iter().map(|m| format!("{}:1", m.relative_path)).collect()
}

fn tst0001(p: &ProjectContext) -> Vec<Suggestion> {
    if p.model_count() == 0 {
        return vec![];
    }
    let yaml_tests: usize = p
        .schema_models
        .values()
        .map(|d| tests_of(d).len() + columns_of(d).iter().map(|c| tests_of(c).len()).sum::<usize>())
        .sum();
    if yaml_tests > 0 || !p.singular_tests.is_empty() {
        return vec![];
    }
    // Prefer a downstream model: it joins or aggregates most often.
    let name = p.models.iter().find(|m| m.layer == "gold").or(p.models.first()).map_or("<model>", |m| m.name.as_str());
    vec![Suggestion::new(
        "SSC-EWI-DBTTST0001",
        format!("This project has {} models and no detected YAML tests or test files.", p.model_count()),
    )
    .file("dbt_project.yml")
    .line(1)
    .ctx("related_files", json!(model_files(p)))
    .evidence("no tests in schema YAML; no files under tests/")
    .remediation(format!(
        "Start with models used in joins or aggregations, where duplicate keys can multiply results. For example, for `{name}`, find the grain first. The first query must return no rows and the second must return 0:\n\n```sql\n{check}\n```\n\nAdd the key only when both checks pass:\n\n```yaml\nmodels:\n  - name: {name}\n    columns:\n      - name: <key_column>\n        data_tests:\n          - dbt_constraints.primary_key\n```\n\nThen test verified relationships from facts to dimensions. Run `dbt build` with the intended test selection. Passing tests check their declared assertions, not all business logic. `SSC-EWI-DBTTST0006` tracks the coverage that follows.",
        check = grain_check(name, "<key_column>"),
    ))
    .effort(effort::MEDIUM)]
}

fn tst0002(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    let Some(def) = p.schema_def(&m.name).filter(|d| !d.is_empty()) else { return vec![] };
    if has_any_key_test(def) {
        return vec![];
    }
    let sev = if m.layer == "bronze" { severity::LOW } else { severity::MEDIUM };
    let candidates: Vec<String> = columns_of(def)
        .into_iter()
        .filter(|c| is_key_column(&c.get("name").map(py_str).unwrap_or_default()))
        .map(col_name)
        .collect();
    let src = p.schema_sources.get(&m.name).cloned().unwrap_or_else(|| "schema yml".into());
    let name = &m.name;
    let check = |cols: &str| grain_check(name, cols);
    // Column names do not prove the grain. Name candidates, never assert a key.
    let (msg, fix) = match candidates.as_slice() {
        [] => (
            format!("Model `{name}` has no primary or unique key test, and no column has a key-shaped name."),
            format!("Find the columns that define one row of `{name}`. Check a candidate set with:\n\n```sql\n{}\n```\n\nIf the first query returns no rows and the second returns 0, declare the set as the key:\n\n```yaml\n  - name: {name}\n    data_tests:\n      - dbt_constraints.primary_key:\n          arguments:\n            column_names: [col_a, col_b]\n```", check("col_a, col_b")),
        ),
        [c] => (
            format!("Model `{name}` has no primary or unique key test. `{c}` is its only key-shaped column, so it is a candidate key."),
            format!("Check that `{c}` is unique before you declare it:\n\n```sql\n{}\n```\n\nIf the first query returns no rows and the second returns 0, add the test:\n\n```yaml\n  - name: {name}\n    columns:\n      - name: {c}\n        data_tests:\n          - dbt_constraints.primary_key\n```\n\nIf the first returns rows, `{c}` is not the grain. Find the columns that define one row and declare them at model level with `column_names: [col_a, col_b]`.", check(c)),
        ),
        cs => {
            let list = cs.join(", ");
            let queries: Vec<String> = cs.iter().take(5).map(|c| check(c)).collect();
            (
                format!("Model `{name}` has no primary or unique key test. It has {} key-shaped columns ({list}). The names do not establish the row grain or prove that the other columns are foreign keys.", cs.len()),
                format!("Decide the grain of `{name}` first. A column is unique and not null when its first query returns no rows and its second returns 0:\n\n```sql\n{}\n```\n\nPut `dbt_constraints.primary_key` on the column (or the model-level `column_names: [...]` set) that defines one row. Put `dbt_constraints.foreign_key` on each column that points at another model.", queries.join(";\n")),
            )
        }
    };
    vec![Suggestion::new("SSC-EWI-DBTTST0002", msg)
        .severity(sev)
        .file(schema_file(m, p))
        .ctx("model", json!(m.name))
        .evidence(format!("schema entry in {src}; key-shaped columns: {}", if candidates.is_empty() { "none".to_string() } else { candidates.join(", ") }))
        .remediation(fix)
        .effort(effort::LOW)
        .ctx("candidate_columns", json!(candidates))]
}

fn tst0003(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !rx!(r"(?i)^(?:dim|dimension)_").is_match(&m.name) {
        return vec![];
    }
    let Some(def) = p.schema_def(&m.name).filter(|d| !d.is_empty()) else { return vec![] };
    let mut all = tests_of(def);
    for c in columns_of(def) {
        all.extend(tests_of(c));
    }
    let declared: BTreeSet<Option<String>> = all.iter().map(test_name).collect();
    let names: Vec<String> = declared.iter().flatten().cloned().collect();
    let has = |n: &str| declared.contains(&Some(n.to_string()));
    if has("dbt_constraints.primary_key") {
        return vec![];
    }
    let base = Suggestion::new("SSC-EWI-DBTTST0003", "")
        .file(schema_file(m, p))
        .ctx("model", json!(m.name))
        .effort(effort::LOW);
    let mut s = base.clone();
    // `SSC-EWI-DBTTST0005` reports a column with `unique` + `not_null` more precisely.
    let column_pair = columns_of(def).iter().any(|c| {
        let n: BTreeSet<String> = tests_of(c).iter().filter_map(test_name).collect();
        n.contains("unique") && n.contains("not_null")
    });
    if column_pair && !PRIMARY_KEY_TESTS.iter().any(|n| has(n)) {
        return vec![];
    }
    if PRIMARY_KEY_TESTS.iter().any(|n| has(n)) || (has("unique") && has("not_null")) {
        s.message = "This dimension has key tests but no explicit `dbt_constraints.primary_key` test. Check existing package-generated metadata before changing working tests.".into();
        return vec![s
            .evidence(format!("tests present: {}", names.join(", ")))
            .remediation("If local policy requires an explicit package primary key, use dbt_constraints.primary_key after confirming equivalent filters, severity, and null handling. The package can also generate metadata from built-in tests. Creation depends on materialization, settings, and privileges; standard-table PK/FK/UNIQUE metadata is not enforced.")];
    }
    s.message = "This dimension has no primary key test.".into();
    let ev = if names.is_empty() { "none".to_string() } else { names.join(", ") };
    vec![s
        .evidence(format!("tests present: {ev}"))
        .remediation("Add `dbt_constraints.primary_key` on the dimension's surrogate or natural key. Facts joining to this dimension depend on that key being unique.")]
}

fn tst0004(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !rx!(r"(?i)^(?:fct|fact)_").is_match(&m.name) {
        return vec![];
    }
    let Some(def) = p.schema_def(&m.name).filter(|d| !d.is_empty()) else { return vec![] };
    let columns = columns_of(def);
    let key_columns: Vec<String> = columns
        .iter()
        .filter(|c| is_key_column(&col_name(c)))
        .map(|c| col_name(c))
        .collect();
    if key_columns.is_empty() {
        return vec![];
    }
    let mut untested: Vec<String> = vec![];
    for c in columns {
        let name = col_name(c);
        if !key_columns.contains(&name) {
            continue;
        }
        let names: Vec<Option<String>> = tests_of(c).iter().map(test_name).collect();
        let any = |set: &[&str]| names.iter().flatten().any(|n| set.contains(&n.as_str()));
        if any(FOREIGN_KEY_TESTS) || any(PRIMARY_KEY_TESTS) || model_level_key_covers(def, &name) {
            continue;
        }
        untested.push(name);
    }
    if untested.is_empty() {
        return vec![];
    }
    let n = untested.len();
    let fk = fk_example(&untested[0], &m.name, p);
    vec![Suggestion::new(
        "SSC-EWI-DBTTST0004",
        format!(
            "{} {} a foreign-key test: {}.",
            plural(n, "key-shaped column"),
            if n == 1 { "lacks" } else { "lack" },
            untested.join(", ")
        ),
    )
    .file(schema_file(m, p))
    .ctx("model", json!(m.name))
    .ctx("column_name", json!(untested[0]))
    .evidence(format!("untested key columns: {}", untested.join(", ")))
    .remediation(format!(
        "Add a foreign-key test per dimension reference:\n\n{}\n\n{}",
        fk.0,
        if fk.1 {
            "If that check passes and unmatched rows are expected, confirm parent-key uniqueness and the null policy too. Use a sentinel only when an intentional matching dimension row exists. Do not assume -1 is valid. Check version-specific test argument syntax."
        } else {
            "Confirm the parent key and null policy. For expected unmatched rows, use a sentinel only when an intentional matching dimension row exists. Do not assume -1 is valid. Check version-specific test argument syntax."
        }
    ))
    .effort(effort::MEDIUM)
    .ctx("untested_columns", json!(untested))]
}

fn tst0005(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    let Some(def) = p.schema_def(&m.name) else { return vec![] };
    let mut out = vec![];
    for c in columns_of(def) {
        let names: BTreeSet<String> = tests_of(c).iter().filter_map(test_name).collect();
        let cn = col_name(c);
        let base = |msg: String, ev: String, rem: String| {
            Suggestion::new("SSC-EWI-DBTTST0005", msg)
                .file(schema_file(m, p))
                .ctx("model", json!(m.name))
                .evidence(ev)
                .remediation(rem)
                .effort(effort::LOW)
                .ctx("column_name", json!(cn))
        };
        if names.contains("unique") && names.contains("not_null") {
            out.push(base(
                format!("Model `{}`: `{cn}` uses `unique` + `not_null` rather than `dbt_constraints.primary_key`.", m.name),
                format!("{cn}: unique + not_null"),
                format!("If the local package style is required, replace the tests on `{cn}` with `- dbt_constraints.primary_key` after preserving their assertion scope and configuration. Built-in tests are valid, and the package may already generate metadata from them."),
            ));
        } else if names.contains("relationships") {
            out.push(base(
                format!("Model `{}`: `{cn}` uses `relationships` rather than `dbt_constraints.foreign_key`.", m.name),
                format!("{cn}: relationships"),
                "If the local package style is required, use `dbt_constraints.foreign_key` with verified `pk_table_name` and `pk_column_name` values. Preserve filters, null policy, and severity. Built-in relationships tests can already generate package metadata. Use test argument syntax supported by the installed dbt version.".into(),
            ));
        }
    }
    out
}

/// The schema YAML files that hold model entries, else the models.
fn tst0006_files(p: &ProjectContext) -> Vec<String> {
    let yml: BTreeSet<String> = p.schema_sources.values().map(|f| format!("{f}:1")).collect();
    if yml.is_empty() { model_files(p) } else { yml.into_iter().collect() }
}

fn tst0006(p: &ProjectContext) -> Vec<Suggestion> {
    let total = p.model_count();
    if total < 5 {
        return vec![];
    }
    let empty = Def::new();
    let tested = p.models.iter().filter(|m| has_any_key_test(p.schema_def(&m.name).unwrap_or(&empty))).count();
    let ratio = tested as f64 / total as f64;
    if ratio >= 0.6 {
        return vec![];
    }
    vec![Suggestion::new(
        "SSC-EWI-DBTTST0006",
        format!(
            "{tested} of {total} models ({:.0}%) have a primary or unique key test.",
            ratio * 100.0
        ),
    )
    .file("dbt_project.yml")
    .line(1)
    .ctx("related_files", json!(tst0006_files(p)))
    .evidence(format!("{tested}/{total} models with PK/UK tests"))
    .remediation(if tst0001(p).is_empty() {
        "Start with consumer-facing dimensions and facts, then review upstream models. Confirm each grain before adding key tests and test verified relationships. Document intentional keyless models; the coverage threshold is local policy."
    } else {
        // TST0001 owns the first step on a project with no tests.
        "This project has no tests, so `SSC-EWI-DBTTST0001` owns the first step: follow it, then use this finding to track coverage. Start with consumer-facing dimensions and facts, then review upstream models. Confirm each grain before adding key tests and test verified relationships. Document intentional keyless models; the coverage threshold is local policy."
    })
    .effort(effort::HIGH)
    .ctx("tested", json!(tested))
    .ctx("total", json!(total))]
}

fn line_at(raw: &str, pos: usize) -> u32 {
    raw[..pos].matches('\n').count() as u32 + 1
}

/// First line that is not blank and not a `--` or `{# #}` comment line.
fn first_code_line(raw: &str) -> u32 {
    let mut in_block = false;
    for (i, l) in raw.lines().enumerate() {
        let t = l.trim();
        if in_block {
            if t.contains("#}") || t.contains("*/") {
                in_block = false;
            }
            continue;
        }
        if t.is_empty() || t.starts_with("--") {
            continue;
        }
        if t.starts_with("{#") || t.starts_with("/*") {
            in_block = !(t.contains("#}") || t.contains("*/"));
            continue;
        }
        return i as u32 + 1;
    }
    1
}

fn tst0007(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for (path, raw) in &p.singular_tests {
        if raw.contains("{% test") || raw.contains("{%- test") {
            continue;
        }
        let body = raw.trim();
        let simple = rx!(r"(?i)\bfrom\b").find_iter(body).count() == 1
            && !rx!(r"(?i)\bjoin\b").is_match(body)
            && rx!(r"(?i)\bis\s+null\b|\bhaving\s+count\s*\(\s*\*\s*\)\s*>\s*1\b").is_match(body);
        if !simple {
            continue;
        }
        let ev: String = rx!(r"\s+").replace_all(body, " ").chars().take(160).collect();
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTTST0007",
                format!("`{}` looks like a built-in generic test written as a singular SQL file.", fname(path)),
            )
            .file(rel(p, path))
            .line(first_code_line(raw))
            .evidence(ev)
            .remediation("Compare the assertion with a generic test such as not_null, unique, or accepted_values. Replace it only when results and configuration are equivalent. Define reusable custom logic in a test block under tests/generic or macros. Keep a singular test when the business assertion is specific.")
            .effort(effort::LOW),
        );
    }
    out
}

fn nested_flag(node: &Value, key: &str) -> bool {
    match node {
        Value::Object(o) => o.iter().any(|(k, v)| (k == key && truthy(Some(v))) || nested_flag(v, key)),
        _ => false,
    }
}

fn tst0008(p: &ProjectContext) -> Vec<Suggestion> {
    let set = |k: &str| p.project_yml.get(k).filter(|v| truthy(Some(v))).cloned().unwrap_or(Value::Object(Map::new()));
    let flagged = |v: &Value| nested_flag(v, "+store_failures") || nested_flag(v, "store_failures");
    if flagged(&set("tests")) || flagged(&set("data_tests")) || p.model_count() == 0 {
        return vec![];
    }
    // The root-level form needs no project key, so a later rename (PRJ0005) cannot break it.
    vec![Suggestion::new(
        "SSC-EWI-DBTTST0008",
        "`dbt_project.yml` sets no enabling `store_failures` under `data_tests:` or `tests:`. Check test-specific settings and CLI flags before concluding that failures are not stored.",
    )
    .file("dbt_project.yml")
    .evidence("no +store_failures under data_tests: or tests:")
    .remediation(
        "If broad failure storage is appropriate, put the config at the root of `data_tests:`. Review sensitive columns, schema permissions, access, and retention first:\n\n```yaml\ndata_tests:\n  +store_failures: true\n  +schema: test_failures\n```\n\nUse per-test settings when broad storage is unnecessary. Stored results replace the prior failures for the same test; they are not a failure history.",
    )
    .effort(effort::LOW)]
}

fn tst0009(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for (path, raw) in &p.snapshot_files {
        if !raw.contains("{% snapshot") && !raw.contains("{%- snapshot") {
            continue;
        }
        let mut missing: Vec<String> = vec![];
        if !rx!(r"\bunique_key\s*=").is_match(raw) {
            missing.push("unique_key".into());
        }
        match rx!(r#"\bstrategy\s*=\s*['"](\w+)['"]"#).captures(raw) {
            None => missing.push("strategy".into()),
            Some(c) => {
                let s = c[1].to_lowercase();
                if s == "timestamp" && !rx!(r"\bupdated_at\s*=").is_match(raw) {
                    missing.push("updated_at (required by the timestamp strategy)".into());
                }
                if s == "check" && !rx!(r"\bcheck_cols\s*=").is_match(raw) {
                    missing.push("check_cols (required by the check strategy)".into());
                }
            }
        }
        if missing.is_empty() {
            continue;
        }
        let pos = rx!(r#"\bstrategy\s*="#).find(raw).or_else(|| rx!(r"\bconfig\s*\(").find(raw)).or_else(|| rx!(r"\{%-?\s*snapshot").find(raw));
        let line = pos.map_or(1, |m| line_at(raw, m.start()));
        let stem = path.file_stem().map(|s| s.to_string_lossy().into_owned()).unwrap_or_default();
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTTST0009",
                format!("SQL snapshot `{stem}` has no detected local settings for: {}. Check inherited and version-specific configuration.", missing.join(", ")),
            )
            .file(rel(p, path))
            .line(line)
            .evidence(missing.join(", "))
            .remediation("Verify effective snapshot configuration, including inherited settings in dbt_project.yml, before adding values. This scan does not resolve that inheritance. If values are truly missing, adapt this legacy SQL example to the installed dbt version and intended hard-delete policy:\n\n```sql\n{{ config(\n    unique_key='customer_id',\n    strategy='timestamp',\n    updated_at='updated_at',\n    invalidate_hard_deletes=True\n) }}\n```\n\nPrefer the timestamp strategy when the source has a reliable modification timestamp; use `check` with an explicit `check_cols` list only when it does not.")
            .effort(effort::LOW),
        );
    }
    out
}

fn tst0010(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    // One finding per folder: the fix is one schema YAML file per folder.
    let mut by_dir: std::collections::BTreeMap<String, Vec<&ModelFile>> = Default::default();
    for m in p.models.iter().filter(|m| !p.schema_models.contains_key(&m.name)) {
        let dir = std::path::Path::new(&m.relative_path).parent().map(crate::discovery::display_path).unwrap_or_default();
        by_dir.entry(dir).or_default().push(m);
    }
    for (dir, models) in by_dir {
        let names: Vec<&str> = models.iter().map(|m| m.name.as_str()).collect();
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTTST0010",
                format!(
                    "{} in `{dir}/` {} no detected schema YAML property entry: {}. Singular tests or SQL-level configuration can still exist.",
                    plural(names.len(), "model"),
                    if names.len() == 1 { "has" } else { "have" },
                    names.join(", ")
                ),
            )
            .file(models[0].relative_path.clone())
            .line(1)
            .ctx("related_files", json!(models.iter().map(|m| format!("{}:1", m.relative_path)).collect::<Vec<_>>()))
            .evidence(format!("absent from all schema files: {}", names.join(", ")))
            .remediation(format!("Add an entry for each listed model to a schema YAML file in `{dir}/` (create `{dir}/_models.yml` if the folder has none). Give each a useful description, column metadata, and tests that fit the verified grain. Do not invent a key just to fill the entry."))
            .effort(effort::LOW)
            .ctx("models", json!(names)),
        );
    }
    let names: BTreeSet<&str> = p.models.iter().map(|m| m.name.as_str()).collect();
    for (name, src) in &p.schema_sources {
        if names.contains(name.as_str()) {
            continue;
        }
        out.push(
            Suggestion::new("SSC-EWI-DBTTST0010", format!("Schema YAML declares model `{name}`, but no matching model was discovered. Check enabled state, model versions, scan scope, and renames."))
                .file(src.clone())
                .evidence(format!("{name} declared in {src}"))
                .remediation("Confirm that the entry is obsolete before deleting it. Otherwise correct its name, restore a missing model, or adjust the discovery scope. dbt diagnostics vary by resource and version; absence from this scan is not proof of a parse error.")
                .effort(effort::LOW),
        );
    }
    out
}

fn tst0012(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    let Some(def) = p.schema_def(&m.name).filter(|d| !d.is_empty()) else { return vec![] };
    // TST0002 owns a model with no key test at all.
    if !has_any_key_test(def) {
        return vec![];
    }
    // TST0004 owns key columns on a fact model.
    if rx!(r"(?i)^(?:fct|fact)_").is_match(&m.name) {
        return vec![];
    }
    let columns = columns_of(def);
    if columns.is_empty() {
        return vec![];
    }
    let mut untested: Vec<String> = vec![];
    for c in columns {
        let name = col_name(c);
        if name.is_empty() || !is_key_column(&name) {
            continue;
        }
        if column_has_key_test(c) || model_level_key_covers(def, &name) {
            continue;
        }
        untested.push(name);
    }
    if untested.is_empty() {
        return vec![];
    }
    let n = untested.len();
    vec![Suggestion::new(
        "SSC-EWI-DBTTST0012",
        format!(
            "Model `{}`: {} {} no constraint test: {}.",
            m.name,
            plural(n, "key-shaped column"),
            if n == 1 { "has" } else { "have" },
            untested.join(", ")
        ),
    )
    .file(schema_file(m, p))
    .ctx("model", json!(m.name))
    .ctx("column_name", json!(untested[0]))
    .evidence(format!("untested key columns: {}", untested.join(", ")))
    .remediation(format!(
        "The model already has a key test, but names alone do not establish the other columns' roles. Confirm each meaning and test the data before selecting a key test. A column pointing at another table gets `dbt_constraints.foreign_key`; a second unique column gets `dbt_constraints.unique_key`:\n\n{}\n\nFor a composite key, declare it once at model level with `column_names: [col_a, col_b]` rather than per column.",
        fk_example(&untested[0], &m.name, p).0
    ))
    .effort(effort::LOW)
    .ctx("untested_columns", json!(untested))]
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const STG: (&str, &str) = ("models/stg/x.sql", "select 1 as customer_id");
    fn n(t: &TempProject, c: &str) -> usize {
        t.findings(&format!("SSC-EWI-DBTTST{c}")).len()
    }
    fn yml(body: &str) -> String {
        format!("version: 2\nmodels:\n{body}")
    }

    #[test]
    fn t0001() {
        let t = TempProject::new(&[STG]);
        assert_eq!(n(&t, "0001"), 1);
        let f = &t.findings("SSC-EWI-DBTTST0001")[0];
        assert_eq!(f.file, "dbt_project.yml");
        assert_eq!(f.context["related_files"], serde_json::json!(["models/stg/x.sql:1"]));
        let t = TempProject::new(&[STG, ("tests/a.sql", "select 1")]);
        assert_eq!(n(&t, "0001"), 0);
    }

    #[test]
    fn t0001_grain_first_and_t0006_cross_ref() {
        let files: Vec<(String, String)> = (0..5).map(|i| (format!("models/m{i}.sql"), "select 1".to_string())).collect();
        let r: Vec<(&str, &str)> = files.iter().map(|(a, b)| (a.as_str(), b.as_str())).collect();
        let t = TempProject::new(&r);
        let one = &t.findings("SSC-EWI-DBTTST0001")[0].remediation;
        assert!(one.find("having count(*) > 1").unwrap() < one.find("dbt_constraints.primary_key").unwrap(), "{one}");
        assert!(one.contains("is null"), "{one}");
        assert!(t.findings("SSC-EWI-DBTTST0006")[0].remediation.contains("SSC-EWI-DBTTST0001"));
    }

    #[test]
    fn fk_example_never_self() {
        let d = ("models/dim_customers.sql", "select 1 as hashed_customer_id");
        let y = yml("  - name: dim_customers\n    columns:\n      - name: id\n        tests: [dbt_constraints.primary_key]\n      - name: hashed_customer_id\n");
        let f = TempProject::new(&[d, ("models/s.yml", &y)]).findings("SSC-EWI-DBTTST0012");
        assert!(f[0].remediation.contains("dbt_constraints.unique_key") && !f[0].remediation.contains("pk_table_name: ref('dim_customers')"), "{}", f[0].remediation);
        // A real parent in the project is named, with its key column.
        let y = yml("  - name: dim_customer\n    columns:\n      - name: customer_id\n        tests: [dbt_constraints.primary_key]\n  - name: fct_orders\n    columns:\n      - name: customer_id\n");
        let t = TempProject::new(&[("models/dim_customer.sql", "select 1 as customer_id"), ("models/fct_orders.sql", "select 1 as customer_id"), ("models/s.yml", &y)]);
        let r = &t.findings("SSC-EWI-DBTTST0004")[0].remediation;
        assert!(r.contains("pk_table_name: ref('dim_customer')") && r.contains("pk_column_name: customer_id"), "{r}");
        assert!(!r.contains("different names") && !r.contains("If that check passes"), "{r}");
        // No candidate parent: placeholders, never a fixture name.
        let f = ("models/fct_a.sql", "select 1 as zone_id");
        let y = yml("  - name: fct_a\n    columns:\n      - name: zone_id\n");
        let r = &TempProject::new(&[f, ("models/s.yml", &y)]).findings("SSC-EWI-DBTTST0004")[0].remediation;
        assert!(r.contains("ref('<parent_model>')") && !r.contains("dim_customers"), "{r}");
        assert!(!r.contains("different names") && !r.contains("If that check passes"), "{r}");
        // Parent key has a different name: check the values first, and the ghost-key advice waits for that check.
        let y = yml("  - name: dim_customer\n    columns:\n      - name: customer_sk\n        tests: [dbt_constraints.primary_key]\n  - name: fct_orders\n    columns:\n      - name: customer_id\n");
        let t = TempProject::new(&[("models/dim_customer.sql", "select 1 as customer_sk"), ("models/fct_orders.sql", "select 1 as customer_id"), ("models/s.yml", &y)]);
        let r = &t.findings("SSC-EWI-DBTTST0004")[0].remediation;
        assert!(r.contains("pk_column_name: customer_sk") && r.contains("`customer_id` and `customer_sk` have different names. Check that `customer_id` holds `customer_sk` values before you add this test."), "{r}");
        assert!(r.contains("If that check passes and unmatched rows are expected"), "{r}");
    }

    #[test]
    fn t0012_skips_fact_models() {
        // TST0004 owns key columns on a fact model; TST0012 stays silent so one line has one owner.
        let f = ("models/fct_x.sql", "select 1 as x_id, 1 as customer_id");
        let y = yml("  - name: fct_x\n    columns:\n      - name: x_id\n        tests: [dbt_constraints.primary_key]\n      - name: customer_id\n");
        let t = TempProject::new(&[f, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0004"), 1);
        assert_eq!(n(&t, "0012"), 0);
    }

    #[test]
    fn grain_check_nulls_every_key_column() {
        let y = yml("  - name: x\n    columns:\n      - name: other\n");
        let f = TempProject::new(&[STG, ("models/s.yml", &y)]).findings("SSC-EWI-DBTTST0002");
        let r = &f[0].remediation;
        assert!(r.contains("where col_a is null or col_b is null"), "{r}");
        assert!(r.contains("If the first query returns no rows and the second returns 0") && !r.contains("Both queries"), "{r}");
    }

    #[test]
    fn t0002() {
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0002"), 1);
        // Two key-shaped columns: name both as candidates, assert neither.
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n      - name: order_id\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        let f = t.findings("SSC-EWI-DBTTST0002");
        assert!(f[0].message.contains("customer_id, order_id") && f[0].remediation.contains("having count(*) > 1"), "{f:?}");
        assert!(!f[0].remediation.contains("- name: customer_id"), "{}", f[0].remediation);
        assert!(f[0].remediation.contains("where customer_id is null"), "{}", f[0].remediation);
        assert_eq!(n(&t, "0012"), 0, "TST0002 owns a model with no key test");
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n        tests: [dbt_constraints.primary_key]\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0002"), 0);
    }

    #[test]
    fn t0003() {
        let d = ("models/dim_a.sql", "select 1 as a_id");
        let y = yml("  - name: dim_a\n    columns:\n      - name: a_id\n        tests: [unique, not_null]\n");
        let t = TempProject::new(&[d, ("models/s.yml", &y)]);
        // TST0005 reports the column pair; TST0003 does not repeat it.
        assert_eq!(n(&t, "0003"), 0);
        assert_eq!(n(&t, "0005"), 1);
        let y = yml("  - name: dim_a\n    columns:\n      - name: a_id\n        tests: [primary_key]\n");
        let t = TempProject::new(&[d, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0003"), 1);
        let y = yml("  - name: dim_a\n    columns:\n      - name: a_id\n");
        let t = TempProject::new(&[d, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0003"), 1);
        let y = yml("  - name: dim_a\n    columns:\n      - name: a_id\n        tests: [dbt_constraints.primary_key]\n");
        let t = TempProject::new(&[d, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0003"), 0);
    }

    #[test]
    fn t0004() {
        let f = ("models/fct_a.sql", "select 1 as a_id");
        let y = yml("  - name: fct_a\n    columns:\n      - name: a_id\n");
        let t = TempProject::new(&[f, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0004"), 1);
        let y = yml("  - name: fct_a\n    tests:\n      - dbt_constraints.foreign_key:\n          arguments:\n            column_names: [A_ID]\n    columns:\n      - name: a_id\n");
        let t = TempProject::new(&[f, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0004"), 0);
    }

    #[test]
    fn t0005() {
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n        tests: [unique, not_null]\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0005"), 1);
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n        tests: [not_null]\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0005"), 0);
    }

    #[test]
    fn t0006() {
        let files: Vec<(String, String)> = (0..5).map(|i| (format!("models/m{i}.sql"), "select 1".to_string())).collect();
        let r: Vec<(&str, &str)> = files.iter().map(|(a, b)| (a.as_str(), b.as_str())).collect();
        let t = TempProject::new(&r);
        assert_eq!(n(&t, "0006"), 1);
        let f = &t.findings("SSC-EWI-DBTTST0006")[0];
        assert_ne!(f.file, "models/");
        assert_eq!(f.context["related_files"].as_array().map(Vec::len), Some(5));
        let mut y = String::from("version: 2\nmodels:\n");
        for i in 0..5 {
            y += &format!("  - name: m{i}\n    columns:\n      - name: id\n        tests: [dbt_constraints.primary_key]\n");
        }
        let mut r2 = r.clone();
        r2.push(("models/s.yml", &y));
        assert_eq!(n(&TempProject::new(&r2), "0006"), 0);
    }

    #[test]
    fn t0007() {
        let t = TempProject::new(&[STG, ("tests/a.sql", "select * from {{ ref('x') }} where id is null")]);
        assert_eq!(n(&t, "0007"), 1);
        let t = TempProject::new(&[STG, ("tests/a.sql", "select * from a join b on a.id = b.id where a.id is null")]);
        assert_eq!(n(&t, "0007"), 0);
        // An exact row-count assertion has no generic-test equivalent.
        let t = TempProject::new(&[STG, ("tests/a.sql", "select count(*) from {{ ref('x') }} having count(*) <> 42")]);
        assert_eq!(n(&t, "0007"), 0);
        let t = TempProject::new(&[STG, ("tests/a.sql", "select id from {{ ref('x') }} group by id having count(*) > 1")]);
        assert_eq!(n(&t, "0007"), 1);
    }

    #[test]
    fn t0008() {
        let t = TempProject::new(&[STG]);
        assert_eq!(n(&t, "0008"), 1);
        let p = "name: demo\nversion: '1.0'\nprofile: demo\ntests:\n  demo:\n    +store_failures: true\n";
        let t = TempProject::new(&[STG, ("dbt_project.yml", p)]);
        assert_eq!(n(&t, "0008"), 0);
        let p = "name: demo\nversion: '1.0'\nprofile: demo\ndata_tests:\n  +store_failures: true\n";
        assert_eq!(n(&TempProject::new(&[STG, ("dbt_project.yml", p)]), "0008"), 0);
        // A placeholder project name never reaches the remediation.
        let p = "name: YOUR_PROJECT_NAME\nversion: '1.0'\nprofile: demo\n";
        let f = TempProject::new(&[STG, ("dbt_project.yml", p)]).findings("SSC-EWI-DBTTST0008");
        assert!(!f[0].remediation.contains("YOUR_PROJECT_NAME") && f[0].remediation.contains("data_tests:\n  +store_failures: true"));
    }

    #[test]
    fn t0009() {
        let t = TempProject::new(&[STG, ("snapshots/s.sql", "{% snapshot s %}{{ config(strategy='timestamp') }}select 1{% endsnapshot %}")]);
        assert_eq!(n(&t, "0009"), 1);
        let ok = "{% snapshot s %}{{ config(unique_key='id', strategy='timestamp', updated_at='u') }}select 1{% endsnapshot %}";
        let t = TempProject::new(&[STG, ("snapshots/s.sql", ok)]);
        assert_eq!(n(&t, "0009"), 0);
    }

    #[test]
    fn t0010() {
        let t = TempProject::new(&[STG]);
        assert_eq!(n(&t, "0010"), 1);
        // A grouped folder finding shows every model it names.
        let t = TempProject::new(&[STG, ("models/stg/y.sql", "select 1")]);
        let f = &t.findings("SSC-EWI-DBTTST0010")[0];
        assert_eq!(f.line, Some(1));
        assert_eq!(f.context["related_files"], serde_json::json!(["models/stg/x.sql:1", "models/stg/y.sql:1"]));
        let y = yml("  - name: x\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0010"), 0);
    }

    #[test]
    fn t0012() {
        let y = yml("  - name: x\n    columns:\n      - name: order_id\n        tests: [dbt_constraints.primary_key]\n      - name: customer_id\n      - name: other\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0012"), 1);
        assert!(t.findings("SSC-EWI-DBTTST0012")[0].message.starts_with("Model `x`"));
        let y = yml("  - name: x\n    columns:\n      - name: customer_id\n        tests: [unique, not_null]\n");
        let t = TempProject::new(&[STG, ("models/s.yml", &y)]);
        assert_eq!(n(&t, "0012"), 0);
    }

    #[test]
    fn tst0007_and_tst0009_skip_header_comments() {
        let t = TempProject::new(&[
            ("models/a.sql", "select 1 as id"),
            ("tests/assert_x.sql", "-- TST007: header\nselect count(*)\nfrom {{ ref('a') }}\nwhere id is null"),
            ("snapshots/snp.sql", "-- TST009: header\n{% snapshot snp %}\n\n{{ config(\n    target_schema='s',\n    unique_key='id',\n    strategy='timestamp'\n) }}\nselect 1\n{% endsnapshot %}"),
        ]);
        let f = t.findings("SSC-EWI-DBTTST0007");
        assert_eq!(f[0].line, Some(2), "{f:?}");
        let f = t.findings("SSC-EWI-DBTTST0009");
        assert_eq!(f[0].line, Some(7), "{f:?}");
    }
}
