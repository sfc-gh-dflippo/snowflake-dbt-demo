//! Reads `rules/*.json`, validates every record, and generates the static
//! `RULES` table. A metadata error fails the build and names the file and code.

use std::collections::BTreeSet;
use std::fmt::Write as _;
use std::path::{Path, PathBuf};

use serde_json::{Map, Value};

/// Read field requirements, allowed values, and length limits from
/// `rules/schema.json` (`$defs.rule`).
struct Schema {
    required: Vec<String>,
    allowed: Vec<String>,
    enums: Vec<(String, Vec<String>)>,
    max_len: Vec<(String, usize)>,
}

fn load_schema(path: &Path) -> Schema {
    let text = std::fs::read_to_string(path).unwrap_or_else(|e| panic!("cannot read {}: {e}", path.display()));
    let doc: Value = serde_json::from_str(&text).unwrap_or_else(|e| fail(path, "-", &format!("invalid JSON: {e}")));
    let rule = &doc["$defs"]["rule"];
    let Some(props) = rule["properties"].as_object() else { fail(path, "-", "missing `$defs.rule.properties`") };
    let required: Vec<String> = rule["required"].as_array().map(|a| a.iter().filter_map(Value::as_str).map(String::from).collect()).unwrap_or_default();
    if required.is_empty() {
        fail(path, "-", "missing `$defs.rule.required`");
    }
    let strs = |v: &Value| -> Vec<String> { v.as_array().map(|a| a.iter().filter_map(Value::as_str).map(String::from).collect()).unwrap_or_default() };
    Schema {
        allowed: props.keys().cloned().collect(),
        enums: props.iter().filter(|(_, v)| v.get("enum").is_some()).map(|(k, v)| (k.clone(), strs(&v["enum"]))).collect(),
        max_len: props.iter().filter_map(|(k, v)| v["maxLength"].as_u64().map(|n| (k.clone(), n as usize))).collect(),
        required,
    }
}

fn fail(file: &Path, code: &str, msg: &str) -> ! {
    panic!("rule metadata error in {} ({code}): {msg}", file.display());
}

fn s<'a>(r: &'a Map<String, Value>, k: &str) -> &'a str {
    r.get(k).and_then(Value::as_str).unwrap_or("")
}

fn validate(schema: &Schema, file: &Path, pack: &str, r: &Map<String, Value>, seen: &mut BTreeSet<String>) {
    let code = s(r, "code").to_string();
    for k in &schema.required {
        if !r.contains_key(k) {
            fail(file, &code, &format!("missing required field `{k}`"));
        }
    }
    for k in r.keys() {
        if !schema.allowed.contains(k) {
            fail(file, &code, &format!("unknown field `{k}`"));
        }
    }
    for k in schema.required.iter().filter(|k| *k != "number") {
        if r[k].as_str().is_none_or(str::is_empty) {
            fail(file, &code, &format!("`{k}` must be a non-empty string"));
        }
    }
    for (k, allowed) in &schema.enums {
        if let Some(v) = r.get(k)
            && !v.as_str().is_some_and(|v| allowed.iter().any(|a| a == v)) {
                fail(file, &code, &format!("`{k}` must be one of {allowed:?}"));
            }
    }
    // SSC-(EWI|FDM|PRF)-DBT<PACK><NNNN>
    let parts: Vec<&str> = code.split('-').collect();
    let ok = parts.len() == 3
        && parts[0] == "SSC"
        && parts[2].len() == 10
        && parts[2].starts_with("DBT")
        && parts[2][3..6].chars().all(|c| c.is_ascii_uppercase())
        && parts[2][6..].chars().all(|c| c.is_ascii_digit());
    if !ok {
        fail(file, &code, "code must match SSC-{EWI|FDM|PRF}-DBT<PACK><NNNN>");
    }
    if parts[1] != s(r, "kind") {
        fail(file, &code, "`kind` disagrees with the code");
    }
    if &parts[2][3..6] != pack {
        fail(file, &code, "pack letters disagree with the file name");
    }
    let number: u64 = parts[2][6..].parse().unwrap();
    if r["number"].as_u64() != Some(number) {
        fail(file, &code, "`number` disagrees with the code");
    }
    for (k, n) in &schema.max_len {
        if s(r, k).chars().count() > *n {
            fail(file, &code, &format!("`{k}` is longer than {n} characters"));
        }
    }
    for k in ["per_line"] {
        if let Some(v) = r.get(k)
            && !v.is_boolean() {
                fail(file, &code, &format!("`{k}` must be a boolean"));
            }
    }
    for k in ["anti_patterns", "principles"] {
        if let Some(v) = r.get(k)
            && !v.as_array().is_some_and(|a| a.iter().all(Value::is_string)) {
                fail(file, &code, &format!("`{k}` must be a list of strings"));
            }
    }
    for (k, fields) in [("examples", &["title", "bad", "good"][..]), ("references", &["title", "url"][..])] {
        if let Some(v) = r.get(k) {
            let ok = v.as_array().is_some_and(|a| {
                a.iter().all(|e| {
                    e.as_object().is_some_and(|o| {
                        o.len() == fields.len() && fields.iter().all(|f| o.get(*f).is_some_and(Value::is_string))
                    })
                })
            });
            if !ok {
                fail(file, &code, &format!("`{k}` entries must have exactly {fields:?}"));
            }
        }
    }
    if !seen.insert(code.clone()) {
        fail(file, &code, "duplicate code");
    }
}

fn strs(v: Option<&Value>) -> String {
    let items: Vec<String> = v
        .and_then(Value::as_array)
        .map(|a| a.iter().filter_map(Value::as_str).map(|x| format!("{x:?}")).collect())
        .unwrap_or_default();
    format!("&[{}]", items.join(", "))
}

fn main() {
    let dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap()).join("../../../rules");
    println!("cargo:rerun-if-changed={}", dir.display());
    let mut files: Vec<PathBuf> = std::fs::read_dir(&dir)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", dir.display()))
        .flatten()
        .map(|e| e.path())
        .filter(|p| p.extension().is_some_and(|e| e == "json") && p.file_name().unwrap() != "schema.json")
        .collect();
    files.sort();

    let schema_path = dir.join("schema.json");
    println!("cargo:rerun-if-changed={}", schema_path.display());
    let schema = load_schema(&schema_path);
    let mut seen = BTreeSet::new();
    let mut out = String::from("pub static RULES: &[RuleMeta] = &[\n");
    for file in &files {
        println!("cargo:rerun-if-changed={}", file.display());
        let pack = file.file_stem().unwrap().to_string_lossy().to_string();
        let text = std::fs::read_to_string(file).unwrap();
        let doc: Value = serde_json::from_str(&text).unwrap_or_else(|e| fail(file, "-", &format!("invalid JSON: {e}")));
        if doc.get("pack").and_then(Value::as_str) != Some(pack.as_str()) {
            fail(file, "-", "top-level `pack` must equal the file name");
        }
        let Some(rules) = doc.get("rules").and_then(Value::as_array) else {
            fail(file, "-", "missing `rules` list");
        };
        let mut last = 0;
        for r in rules {
            let Some(r) = r.as_object() else { fail(file, "-", "rule record must be an object") };
            validate(&schema, file, &pack, r, &mut seen);
            let n = r["number"].as_u64().unwrap();
            if n <= last {
                fail(file, s(r, "code"), "records must be sorted by `number`");
            }
            last = n;
            let examples: Vec<String> = r
                .get("examples")
                .and_then(Value::as_array)
                .map(|a| {
                    a.iter()
                        .map(|e| format!("Example {{ title: {:?}, bad: {:?}, good: {:?} }}", e["title"].as_str().unwrap(), e["bad"].as_str().unwrap(), e["good"].as_str().unwrap()))
                        .collect()
                })
                .unwrap_or_default();
            let references: Vec<String> = r
                .get("references")
                .and_then(Value::as_array)
                .map(|a| a.iter().map(|e| format!("Reference {{ title: {:?}, url: {:?} }}", e["title"].as_str().unwrap(), e["url"].as_str().unwrap())).collect())
                .unwrap_or_default();
            let json = serde_json::to_string(r).unwrap();
            writeln!(
                out,
                "    RuleMeta {{ code: {:?}, pack: {:?}, number: {n}, kind: {:?}, name: {:?}, short_description: {:?}, long_description: {:?}, remediation: {:?}, level: {:?}, severity: {:?}, tier: {:?}, scope: {:?}, effort: {:?}, per_line: {}, anti_patterns: {}, principles: {}, marker_subject: {:?}, examples: &[{}], references: &[{}], since: {:?}, status: {:?}, json: {:?} }},",
                s(r, "code"), pack, s(r, "kind"), s(r, "name"), s(r, "short_description"), s(r, "long_description"),
                s(r, "remediation"), s(r, "level"), s(r, "severity"), s(r, "tier"), s(r, "scope"), s(r, "effort"),
                r.get("per_line").and_then(Value::as_bool).unwrap_or(false),
                strs(r.get("anti_patterns")), strs(r.get("principles")),
                r.get("marker_subject").and_then(Value::as_str),
                examples.join(", "), references.join(", "), s(r, "since"),
                r.get("status").and_then(Value::as_str).unwrap_or("active"), json,
            )
            .unwrap();
        }
    }
    out.push_str("];\n");
    let dest = PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("rules_meta.rs");
    std::fs::write(dest, out).unwrap();
}
