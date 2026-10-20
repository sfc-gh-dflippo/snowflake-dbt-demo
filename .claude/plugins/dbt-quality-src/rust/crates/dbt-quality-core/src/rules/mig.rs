//! MIG rules: unresolved conversion issues in migrated projects.

use serde_json::{json, Value};

use crate::annotate::owned_code;
use crate::discovery::{ModelFile, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural, Suggestion};
use crate::provenance::{
    dd_constant_pattern, etl_control_column_pattern, ewi_pattern, fdm_pattern, marker_text,
    needs_user_pattern, needs_user_text, resolve_ewi_pattern,
};
use crate::rx;
use crate::sqlutil::{py_str, span};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTMIG0001", detect: Detect::Model(resolve_ewi) },
    Detector { code: "SSC-EWI-DBTMIG0002", detect: Detect::Model(ewi_marker) },
    Detector { code: "SSC-FDM-DBTMIG0003", detect: Detect::Model(fdm_marker) },
    Detector { code: "SSC-EWI-DBTMIG0004", detect: Detect::Model(needs_user) },
    Detector { code: "SSC-FDM-DBTMIG0005", detect: Detect::Model(control_column) },
    Detector { code: "SSC-EWI-DBTMIG0006", detect: Detect::Project(scaffolding) },
    Detector { code: "SSC-EWI-DBTMIG0007", detect: Detect::Project(etl_names) },
    Detector { code: "SSC-EWI-DBTMIG0008", detect: Detect::Project(placeholder_models) },
    Detector { code: "SSC-EWI-DBTMIG0009", detect: Detect::Project(generic_strategy) },
];

fn take_chars(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

/// Text of the line that holds `start`, up to `end`'s line end.
fn line_around(raw: &str, start: usize, end: usize) -> &str {
    let ls = raw[..start].rfind('\n').map_or(0, |i| i + 1);
    let le = raw[end..].find('\n').map_or(raw.len(), |i| end + i);
    &raw[ls..le]
}

/// True when dbt-quality wrote the marker code at `start`.
fn line_no(text: &str, pos: usize) -> u32 {
    text[..pos].matches('\n').count() as u32 + 1
}

/// First line that is not blank and not a `--` comment.
fn first_code_line(raw: &str) -> u32 {
    raw.lines()
        .position(|l| {
            let t = l.trim();
            !t.is_empty() && !t.starts_with("--")
        })
        .map_or(1, |i| i as u32 + 1)
}

fn is_owned_at(text: &str, start: usize) -> bool {
    owned_code().find_at(text, start).is_some_and(|m| m.start() == start)
}

fn scan_text(m: &ModelFile) -> &str {
    if m.without_directives.is_empty() { &m.raw } else { &m.without_directives }
}

fn resolve_ewi(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let mut out = vec![];
    let hits: Vec<(regex::Match, String)> =
        resolve_ewi_pattern().find_iter(&m.raw).map(|mt| (mt, marker_text(&m.raw, mt.end()))).collect();
    // A bare marker (no vendor text) only repeats what the described markers already report.
    let any_described = hits.iter().any(|(_, v)| !v.is_empty());
    for (mt, vendor) in hits {
        if any_described && vendor.is_empty() {
            continue;
        }
        let context = take_chars(&m.raw[mt.start()..], 260);
        let msg = if vendor.is_empty() {
            "This model contains an `!!!RESOLVE EWI!!!` marker for incomplete conversion. If the unresolved text remains executable, it can block compilation; inspect the marked region.".to_string()
        } else {
            vendor.clone()
        };
        out.push(
            Suggestion::new("SSC-EWI-DBTMIG0001", msg)
                .file(&m.relative_path)
                .span(span(&m.raw, mt.start(), mt.end()))
                .evidence(rx!(r"\s+").replace_all(&context, " ").trim())
                .remediation(format!(
                    "Review the original expression and marker, then implement equivalent Snowflake logic. Use `dbt compile --select {}` to inspect rendering, then run the affected model and tests in a controlled target and compare source behavior. Remove the marker only after verification.{}",
                    m.name,
                    // ABORT() stops the source session; a model cannot stop a run.
                    if vendor.to_uppercase().contains("ABORT()") {
                        " For `ABORT()`, put the abort condition in a singular test under `tests/` (default `severity: error`), so `dbt build` fails and skips the downstream models. Keep the expression that the converter set to NULL out of the model. The test runs after the model builds, so the model's table already holds the rows. If the target must not be written, test the condition on the upstream model, so `dbt build` skips this model."
                    } else {
                        ""
                    }
                ))
                .effort(effort::HIGH)
                .ctx("vendor_text", !vendor.is_empty()),
        );
    }
    out
}

/// Shared body of MIG0002 and MIG0003.
fn marker_findings(
    m: &ModelFile,
    pat: &regex::Regex,
    code_id: &str,
    skip_resolve: bool,
    ev_len: usize,
    default_msg: &dyn Fn(&str) -> String,
    remediation: &dyn Fn(&str, &str) -> String,
) -> Vec<Suggestion> {
    let text = scan_text(m);
    // Per (code, text): index in `out` and the length of the line that holds the code.
    let mut seen: std::collections::HashMap<(String, String), (usize, usize)> = Default::default();
    let mut out = vec![];
    for mt in pat.find_iter(text) {
        if is_owned_at(text, mt.start()) {
            continue;
        }
        let code = mt.as_str().to_uppercase();
        if skip_resolve {
            let from = m.raw[..mt.start()]
                .char_indices()
                .rev()
                .nth(39)
                .map_or(0, |(i, _)| i);
            if resolve_ewi_pattern().is_match(&m.raw[from..mt.start()]) {
                continue;
            }
        }
        let vendor = marker_text(&m.raw, mt.start());
        // Prose that mentions a code is a longer line than the real marker line.
        let tail = line_around(&m.raw, mt.start(), mt.end()).len();
        let key = (code.clone(), vendor.clone());
        let replace = match seen.get(&key) {
            Some(&(_, old_tail)) if tail >= old_tail => continue,
            Some(&(i, _)) => Some(i),
            None => None,
        };
        let msg = if vendor.is_empty() { default_msg(&code) } else { vendor.clone() };
        let ev = take_chars(line_around(&m.raw, mt.start(), mt.end()).trim(), ev_len);
        let finding =
            Suggestion::new(code_id, msg)
                .file(&m.relative_path)
                .span(span(&m.raw, mt.start(), mt.end()))
                .evidence(ev)
                .remediation(remediation(&code, &vendor))
                .effort(effort::MEDIUM)
                .ctx("code", code)
                .ctx("vendor_text", !vendor.is_empty());
        match replace {
            Some(i) => {
                out[i] = finding;
                seen.insert(key, (i, tail));
            }
            None => {
                seen.insert(key, (out.len(), tail));
                out.push(finding);
            }
        }
    }
    out
}

fn ewi_marker(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    marker_findings(
        m,
        ewi_pattern(),
        "SSC-EWI-DBTMIG0002",
        true,
        200,
        &|c| format!("This model carries a `{c}` conversion marker. Review its text and verification evidence before deciding whether work remains."),
        &|c, _| match c {
            // SnowConvert writes SSC-EWI-0001 when it cannot parse the source; the statement is not converted.
            "SSC-EWI-0001" => "The converter could not parse the source at the quoted line and column. Find the original statement and confirm what was omitted or left untranslated, then rewrite it in Snowflake SQL. Compile to inspect rendering, run the affected model and tests in a controlled target, and compare source behavior. Remove the marker after verification.".to_string(),
            _ => "Look up the code in the conversion tool's EWI reference and verify the model against the source system's output. Remove the marker once the output is verified, and add a test to pin the validated behaviour.".to_string(),
        },
    )
}

fn fdm_marker(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    marker_findings(
        m,
        fdm_pattern(),
        "SSC-FDM-DBTMIG0003",
        false,
        220,
        &|c| format!("The `{c}` marker records a potential behavior difference from the source platform. Check the marker text, converter version, validation evidence, and any existing sign-off."),
        &|c, v| fdm_remediation(c, v),
    )
}

/// Remediation per FDM code. Each text follows the marker text that SnowConvert
/// writes for the code. An unknown code gets neutral advice.
fn fdm_remediation(code: &str, vendor: &str) -> String {
    const SIGN: &str = " Record the decision in the model description and note the sign-off beside the marker.";
    let v = vendor.to_uppercase();
    let fix = match code {
        // A no-op needs no decision and no sign-off.
        "SSC-FDM-TS0029" => {
            return "`SET NOCOUNT` has no effect in Snowflake. Delete the marker. No sign-off is needed.".into();
        }
        // The decision and its record are in the text, so it skips the shared prefix and suffix.
        "SSC-FDM-TS0010" => {
            return "In a dbt run, `current_database()` returns the session database, which is normally `{{ target.database }}`. If the original read the caller's database, no change is needed: record the decision in the model description and delete the marker. Only if the model must name the database it writes to, and that differs from the session database, replace the call with `{{ this.database }}` and delete the marker.".into();
        }
        "SSC-FDM-INF0058" => "Confirm this code's meaning from its marker text and converter version. If it describes a same-table read/write split into staging and a mart, verify full physical identity and load semantics. A staging view does not capture prior state, and a new ref can close a dependency cycle; use PRJ0022 for guarded prior-state relocation where applicable. Do not add an `order by`; it does not restore build order or prior-state semantics.",
        "SSC-FDM-INF0029" => "Confirm this code's meaning from its marker text and converter version. If it concerns sequential TargetLoadOrder replaced by `UNION ALL`, compare reads, writes, deletes, rejects, duplicates, and overwrite settings. Absence of cross-pipeline reads alone does not prove equivalence. Preserve the load order through an explicit design without creating multiple writers for one table. An `order by` does not restore load order.",
        "SSC-FDM-INF0003" => "The source `IIF` had no false value, so the model returns NULL in that case. Check the original mapping: Informatica defaults the false value by the true value's data type (0, an empty string, or NULL). Set the same default explicitly in the `iff()` call.",
        "SSC-FDM-TS0001" => "Snowflake does not support this collation. Compare and sort results on this column against the source system. If they differ, add an explicit `collate` on the column, or normalise the value (for example `upper()`) where it is compared.",
        "SSC-FDM-0007" => "The model references an object that was not in the conversion input. Find where the original code creates it (often a temp table in a calling procedure). Model that step in dbt and `ref()` it, or declare it as a source.",
        _ if v.contains("ORDER") || v.contains("DETERMINIS") => "The marker reports an ordering or tie-break difference. Add an `order by` (or a `qualify` tie-break) on columns that make the row order deterministic. `SSC-EWI-DBTSQL0008` findings often pair with this marker.",
        _ => "Read the marker text and the original mapping or procedure. Compare the model's output with the source system's output for the case the marker describes.",
    };
    format!("Decide whether the difference is acceptable. {fix}{SIGN}")
}

fn needs_user(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let mut out = vec![];
    for mt in needs_user_pattern().find_iter(&m.raw) {
        let le = m.raw[mt.end()..].find('\n').map_or(m.raw.len(), |i| mt.end() + i);
        let vendor = needs_user_text(&m.raw, mt.start());
        let msg = if vendor.is_empty() {
            "An unresolved `NEEDS-USER` marker records an incomplete required conversion step.".to_string()
        } else {
            vendor.clone()
        };
        out.push(
            Suggestion::new("SSC-EWI-DBTMIG0004", msg)
                .file(&m.relative_path)
                .span(span(&m.raw, mt.start(), mt.end()))
                .evidence(take_chars(m.raw[mt.start()..le].trim(), 200))
                .remediation("Complete the described step and delete the marker.")
                .effort(effort::MEDIUM)
                .ctx("vendor_text", !vendor.is_empty()),
        );
    }
    out
}

fn control_column(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let Some(mt) = etl_control_column_pattern()
        .find(&m.stripped)
        .or_else(|| dd_constant_pattern().find(&m.stripped))
    else {
        return vec![];
    };
    vec![Suggestion::new(
        "SSC-FDM-DBTMIG0005",
        "This model references an ETL DML-decision column or `DD_*` constant from the source pipeline.",
    )
    .file(&m.relative_path)
    .span(span(&m.stripped, mt.start(), mt.end()))
    .evidence(mt.as_str())
    .remediation("Map insert, update, delete, and reject behavior explicitly before removing the control column. A supported merge with a tested unique_key can handle inserts and updates, but stock merge does not infer deletes from a flag. Keep rejection filters and choose an explicit deletion or agreed soft-delete contract. Drop the column only after verifying equivalent results and downstream expectations.")
    .effort(effort::HIGH)]
}

fn etl_names(p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let re = rx!(r"(?i)^(int_)?(SQ|EXP|FIL|LKP|JNR|RTR|SRT|NRM|MPLT|UPDTRANS)[_\d]");
    let affected: Vec<&ModelFile> = p.models.iter().filter(|m| re.is_match(&m.name)).collect();
    if affected.is_empty() {
        return vec![];
    }
    let mut names: Vec<String> = affected.iter().map(|m| m.name.clone()).collect();
    names.sort();
    let n = names.len();
    let msg = format!(
        "{} {} ETL transformation-instance prefixes: {}{}.",
        plural(n, "model"),
        if n == 1 { "retains" } else { "retain" },
        names[..n.min(6)].join(", "),
        if n > 6 { " ..." } else { "" }
    );
    let mut files: Vec<&ModelFile> = affected.clone();
    files.sort_by(|a, b| a.name.cmp(&b.name));
    let related: Vec<String> =
        files[1..]
            .iter()
            .map(|m| format!("{}:{}", crate::discovery::root_relative(p, &m.relative_path), first_code_line(&m.raw)))
            .collect();
    vec![Suggestion::new("SSC-EWI-DBTMIG0007", msg)
        .file(&files[0].relative_path)
        .line(first_code_line(&files[0].raw))
        .ctx("related_files", json!(related))
        .evidence(names[..n.min(10)].join(", "))
        .remediation("Rename models for their business purpose when that improves navigation. Review model boundaries separately rather than collapsing every transformation chain. Use alias if the physical relation name must remain stable, but update ref() calls, selectors, tests, and orchestration that use the resource name; alias does not preserve those references.")
        .effort(effort::HIGH)
        .ctx("models", json!(names))]
}

fn scaffolding(p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let re = rx!(r"(?i)stabilization_test");
    let mut hits: Vec<String> = vec![];
    let mut lines: Vec<Option<u32>> = vec![];
    if re.is_match(&py_str(&Value::Object(p.project_yml.clone()))) {
        hits.push("dbt_project.yml".into());
        lines.push(re.find(&p.project_yml_text).map(|m| line_no(&p.project_yml_text, m.start())));
    }
    for (path, raw) in &p.singular_tests {
        if let Some(mt) = re.find(raw) {
            hits.push(crate::discovery::display_path(path.strip_prefix(&p.root).unwrap_or(path)));
            lines.push(Some(line_no(raw, mt.start())));
        }
    }
    for m in &p.models {
        if let Some(mt) = re.find(&m.raw) {
            hits.push(m.relative_path.clone());
            lines.push(Some(line_no(&m.raw, mt.start())));
        }
    }
    if hits.is_empty() {
        return vec![];
    }
    let n = hits.len();
    let msg = format!(
        "{} {} conversion-stabilization scaffolding: {}{}.",
        plural(n, "location"),
        if n == 1 { "still carries" } else { "still carry" },
        hits[..n.min(5)].join(", "),
        if n > 5 { " ..." } else { "" }
    );
    let related: Vec<String> = hits[1..]
        .iter()
        .zip(&lines[1..])
        .map(|(h, l)| format!("{}:{}", crate::discovery::root_relative(p, h), l.unwrap_or(1)))
        .collect();
    vec![Suggestion::new("SSC-EWI-DBTMIG0006", msg)
        .file(&hits[0])
        .line_opt(lines[0])
        .ctx("related_files", json!(related))
        .evidence(hits[..n.min(8)].join(", "))
        .remediation("Review which stabilization checks still provide required evidence. Retire temporary scaffolding only after preserving that evidence and adding appropriate key, relationship, and business-rule tests. Tests validate declared assertions when run; they do not prove every future input correct. See Testing & constraints findings for a starting point.")
        .effort(effort::MEDIUM)
        .ctx("locations", json!(hits))]
}

/// Line of the placeholder marker or `where false`, else the first code line.
fn placeholder_line(m: &ModelFile) -> u32 {
    for re in [
        rx!(r"(?im)^\s*--\s*status:\s*placeholder"),
        rx!(r"(?im)^\s*--\s*awaiting\s+logic\s+conversion"),
        rx!(r"(?im)^\s*--\s*todo:\s*(implement|convert)"),
        rx!(r"(?i)\bwhere\s+false\b"),
    ] {
        if let Some(mt) = re.find(&m.raw) {
            let ws = mt.as_str().len() - mt.as_str().trim_start().len();
            return line_no(&m.raw, mt.start() + ws);
        }
    }
    first_code_line(&m.raw)
}

fn is_placeholder(m: &ModelFile) -> String {
    if let Some(tags) = m.effective_config.get("tags").filter(|v| crate::sqlutil::truthy(Some(v))) {
        let list: Vec<Value> = match tags {
            Value::Array(a) => a.clone(),
            other => vec![other.clone()],
        };
        for t in &list {
            if rx!(r"(?i)^placeholder$").is_match(py_str(t).trim()) {
                return format!("tags={}", py_str(&Value::Array(list.clone())));
            }
        }
    }
    for re in [
        rx!(r"(?im)^\s*--\s*status:\s*placeholder"),
        rx!(r"(?im)^\s*--\s*awaiting\s+logic\s+conversion"),
        rx!(r"(?im)^\s*--\s*todo:\s*(implement|convert)"),
    ] {
        if let Some(mt) = re.find(&m.raw) {
            return mt.as_str().trim().to_string();
        }
    }
    if let Some(mt) = rx!(r"(?i)\bwhere\s+false\b").find(&m.stripped) {
        return mt.as_str().trim().to_string();
    }
    String::new()
}

fn placeholder_models(p: &ProjectContext) -> Vec<Suggestion> {
    if !p.provenance.is_migration {
        return vec![];
    }
    let found: Vec<(&ModelFile, String)> = p
        .models
        .iter()
        .map(|m| (m, is_placeholder(m)))
        .filter(|(_, e)| !e.is_empty())
        .collect();
    if found.is_empty() {
        return vec![];
    }
    let total = p.models.len();
    let pct = (total - found.len()) as f64 / total as f64 * 100.0;
    let rounded: f64 = format!("{pct:.1}").parse().unwrap_or(pct);
    found
        .iter()
        .map(|(m, ev)| {
            Suggestion::new(
                "SSC-EWI-DBTMIG0008",
                "This model matches a conversion-placeholder pattern. Verify its compiled SQL and output; a tag alone does not prove an empty result.",
            )
            .file(&m.relative_path)
            .line(placeholder_line(m))
            .evidence(take_chars(ev, 160))
            .remediation("Review whether the empty result or placeholder tag is intentional. Complete the original logic and compare representative outputs, or explicitly exclude the unfinished model and handle its consumers. Do not delete dependencies merely to make a build pass; document why an intentionally empty model is valid.")
            .effort(effort::HIGH)
            .ctx("completion_percentage", json!(rounded))
            .ctx("placeholder_count", found.len())
            .ctx("model_total", total)
        })
        .collect()
}

/// `delete_only` is exempt until SCJ-P07 renames it.
fn generic_strategy(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for m in &p.models {
        let v = m.own_config.get("incremental_strategy").map(py_str).unwrap_or_default();
        if matches!(v.as_str(), "update_only" | "insert_only") {
            out.push(
                Suggestion::new("SSC-EWI-DBTMIG0009", format!("Model `{}` sets the generic incremental strategy `{v}`.", m.name))
                    .file(m.relative_path.clone())
                    .evidence(format!("incremental_strategy={v}"))
                    .ctx("strategy", json!(v))
                    .ctx("model", json!(m.name)),
            );
        }
    }
    let t = &p.project_yml_text;
    for c in rx!(r#"(?m)^[ \t]*\+?incremental_strategy[ \t]*:[ \t]*["']?(update_only|insert_only)\b"#).captures_iter(t) {
        let g = c.get(1).unwrap();
        out.push(
            Suggestion::new("SSC-EWI-DBTMIG0009", format!("Folder config sets the generic incremental strategy `{}`.", g.as_str()))
                .file("dbt_project.yml")
                .span(span(t, g.start(), g.end()))
                .evidence(format!("+incremental_strategy: {}", g.as_str()))
                .ctx("strategy", json!(g.as_str())),
        );
    }
    for mf in &p.macros {
        for c in rx!(r"\bmacro\s+get_incremental_(update_only|insert_only)_sql\b").captures_iter(&mf.raw) {
            let g = c.get(0).unwrap();
            out.push(
                Suggestion::new("SSC-EWI-DBTMIG0009", format!("Macro `{}` defines the generic incremental strategy `{}`.", g.as_str().trim_start_matches("macro").trim(), &c[1]))
                    .file(mf.relative_path.clone())
                    .span(span(&mf.raw, g.start(), g.end()))
                    .evidence(g.as_str())
                    .ctx("strategy", json!(&c[1])),
            );
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const CFG: (&str, &str) = (".dbt-quality.yml", "migration:\n  mode: lift_and_shift\n");
    const EWI: &str = "SSC-EWI-DBTMIG0002";

    fn proj(sql: &str) -> TempProject {
        TempProject::new(&[CFG, ("models/stg/x.sql", sql)])
    }

    #[test]
    fn mig0001() {
        let t = proj("select 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - bad ***/");
        assert_eq!(t.findings("SSC-EWI-DBTMIG0001").len(), 1);
        assert!(proj("select 1").findings("SSC-EWI-DBTMIG0001").is_empty());
    }

    #[test]
    fn mig0002() {
        let t = proj("select 1 -- SSC-EWI-SSIS0004 - control flow\n");
        assert_eq!(t.findings(EWI).len(), 1);
        assert!(proj("select 1").findings(EWI).is_empty());
    }

    #[test]
    fn mig0002_ignores_owned_code() {
        let t = proj("select 1 -- see SSC-EWI-DBTMIG0001 here\nselect 2 -- SSC-EWI-DBT0001 - x\n");
        let f = t.findings(EWI);
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].context["code"], "SSC-EWI-DBT0001");
    }

    #[test]
    fn mig0003() {
        let t = proj("select 1 -- SSC-FDM-0006 - order differs\n");
        assert_eq!(t.findings("SSC-FDM-DBTMIG0003").len(), 1);
        assert!(proj("select 1").findings("SSC-FDM-DBTMIG0003").is_empty());
    }

    #[test]
    fn mig0003_remediation_per_code() {
        let fix = |sql: &str| proj(sql).findings("SSC-FDM-DBTMIG0003")[0].remediation.clone();
        let same = fix("select 1 -- SSC-FDM-INF0058 - TABLE 'T' IS USED AS BOTH SOURCE AND TARGET\n");
        assert!(same.contains("staging") && same.contains("Do not add an `order by`"), "{same}");
        let seq = fix("select 1 -- SSC-FDM-INF0029 - INFORMATICA LOADS TARGETS SEQUENTIALLY\n");
        assert!(seq.contains("UNION ALL") && seq.contains("load order"), "{seq}");
        let ord = fix("select 1 -- SSC-FDM-0099 - ROW ORDER MAY DIFFER\n");
        assert!(ord.contains("order by"), "{ord}");
        let unk = fix("select 1 -- SSC-FDM-0099 - SOMETHING ELSE\n");
        assert!(!unk.contains("order by") && unk.contains("original mapping"), "{unk}");
    }

    #[test]
    fn mig0003_ewi_codes() {
        let fix = |sql: &str| proj(sql).findings("SSC-FDM-DBTMIG0003")[0].remediation.clone();
        let nc = fix("select 1 -- SSC-FDM-TS0029 - SET NOCOUNT STATEMENT IS COMMENTED OUT\n");
        assert!(nc.contains("No sign-off is needed") && !nc.contains("sign-off beside"), "{nc}");
        let db = fix("select 1 -- SSC-FDM-TS0010 - CURRENT DATABASE FUNCTION\n");
        assert!(db.contains("no change is needed") && db.contains("{{ this.database }}"), "{db}");
        assert!(!db.contains("sign-off beside") && !db.starts_with("Decide whether"), "{db}");
        let co = fix("select 1 -- SSC-FDM-TS0001 - COLLATION NOT SUPPORTED\n");
        assert!(co.contains("collate"), "{co}");
        let dep = fix("select 1 -- SSC-FDM-0007 - MISSING DEPENDENT OBJECT\n");
        assert!(dep.contains("declare it as a source"), "{dep}");
    }

    #[test]
    fn mig0001_abort_caveat() {
        let t = proj("select 1 !!!RESOLVE EWI!!! /*** SSC-EWI-INF0060 - ABORT() FUNCTION IS NOT SUPPORTED ***/");
        let r = &t.findings("SSC-EWI-DBTMIG0001")[0].remediation;
        assert!(r.contains("singular test") && r.contains("already holds the rows"), "{r}");
        let r = &proj("select 1 !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - bad ***/").findings("SSC-EWI-DBTMIG0001")[0].remediation;
        assert!(!r.contains("ABORT"), "{r}");
    }

    #[test]
    fn mig0002_unparsed_source() {
        let t = proj("select 1 -- SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE 3 COLUMN 1\n");
        let r = &t.findings(EWI)[0].remediation;
        assert!(r.contains("could not parse") && r.contains("rewrite it in Snowflake SQL"), "{r}");
        assert!(!proj("select 1 -- SSC-EWI-SSIS0004 - x\n").findings(EWI)[0].remediation.contains("could not parse"));
    }

    #[test]
    fn mig0003_ignores_owned_code() {
        let t = proj("select 1 -- SSC-FDM-DBTSQL0008 note\n");
        assert!(t.findings("SSC-FDM-DBTMIG0003").is_empty());
    }

    #[test]
    fn mig0004() {
        let t = proj("select 1\n-- NEEDS-USER: finish this\n");
        assert_eq!(t.findings("SSC-EWI-DBTMIG0004").len(), 1);
        assert!(proj("select 1").findings("SSC-EWI-DBTMIG0004").is_empty());
    }

    #[test]
    fn mig0005() {
        let t = proj("select * from t where etl_dml_operation__ <> 'x'");
        assert_eq!(t.findings("SSC-FDM-DBTMIG0005").len(), 1);
        assert!(proj("select 1").findings("SSC-FDM-DBTMIG0005").is_empty());
    }

    #[test]
    fn mig0006() {
        let t = TempProject::new(&[CFG, ("models/stg/x.sql", "select 1"), ("tests/stabilization_test_x.sql", "select 1 -- stabilization_test")]);
        assert_eq!(t.findings("SSC-EWI-DBTMIG0006").len(), 1);
        assert!(proj("select 1").findings("SSC-EWI-DBTMIG0006").is_empty());
    }

    #[test]
    fn mig0007() {
        let t = TempProject::new(&[CFG, ("models/stg/SQ_emp.sql", "select 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTMIG0007").len(), 1);
        assert!(proj("select 1").findings("SSC-EWI-DBTMIG0007").is_empty());
    }

    #[test]
    fn mig0008() {
        let t = proj("-- Status: placeholder\nselect 1");
        let f = t.findings("SSC-EWI-DBTMIG0008");
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].context["completion_percentage"], 0.0);
        assert!(proj("select 1").findings("SSC-EWI-DBTMIG0008").is_empty());
    }

    #[test]
    fn mig0009() {
        let c = "{{ config(materialized='incremental', incremental_strategy='update_only') }}\nselect 1";
        assert_eq!(TempProject::new(&[("models/a.sql", c)]).findings("SSC-EWI-DBTMIG0009").len(), 1);
        let m = TempProject::new(&[("macros/s.sql", "{% macro get_incremental_insert_only_sql(a) %}x{% endmacro %}")]);
        assert_eq!(m.findings("SSC-EWI-DBTMIG0009").len(), 1);
        let ok = "{{ config(materialized='incremental', incremental_strategy='delete_only') }}\nselect 1";
        assert!(TempProject::new(&[("models/a.sql", ok)]).findings("SSC-EWI-DBTMIG0009").is_empty());
    }

    #[test]
    fn mig0001_skips_bare_marker_when_described_exist() {
        let t = proj("-- note: !!!RESOLVE EWI!!!\nselect\n  !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - bad ***/!!! x\n");
        let f = t.findings("SSC-EWI-DBTMIG0001");
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].line, Some(3));
    }

    #[test]
    fn mig0002_prefers_marker_line_over_prose() {
        let t = proj("-- SSC-EWI-INF0001 has no description here, so it falls back\n-- SSC-EWI-INF0001 marker\nselect 1\n");
        let f = t.findings(EWI);
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].line, Some(2));
    }

    #[test]
    fn mig0007_lists_every_model() {
        let t = TempProject::new(&[CFG, ("models/stg/SQ_a.sql", "select 1"), ("models/stg/EXP_b.sql", "select 1")]);
        let f = &t.findings("SSC-EWI-DBTMIG0007")[0];
        assert_eq!(f.line, Some(1));
        assert_eq!(f.context["related_files"], serde_json::json!(["models/stg/SQ_a.sql:1"]));
    }

    #[test]
    fn mig0007_skips_header_comment() {
        let t = TempProject::new(&[CFG, ("models/stg/SQ_a.sql", "-- note\nselect 1"), ("models/stg/EXP_b.sql", "-- note\n\nselect 1")]);
        let f = &t.findings("SSC-EWI-DBTMIG0007")[0];
        assert_eq!(f.line, Some(3));
        assert_eq!(f.context["related_files"], serde_json::json!(["models/stg/SQ_a.sql:2"]));
    }

    #[test]
    fn mig0008_points_at_marker() {
        let t = proj("-- header\n-- status: placeholder\nselect 1\nwhere false");
        assert_eq!(t.findings("SSC-EWI-DBTMIG0008")[0].line, Some(2));
        let t = proj("-- header\nselect 1\nwhere false");
        assert_eq!(t.findings("SSC-EWI-DBTMIG0008")[0].line, Some(3));
    }

    #[test]
    fn mig0006_points_at_tag_lines() {
        let yml = "name: demo\nprofile: demo\nmodels:\n  demo:\n    +tags: [\"stabilization_test\"]\n";
        let t = TempProject::new(&[CFG, ("dbt_project.yml", yml), ("models/stg/x.sql", "select 1"), ("tests/t.sql", "-- header\n-- tags: stabilization_test\nselect 1")]);
        let f = &t.findings("SSC-EWI-DBTMIG0006")[0];
        assert_eq!(f.file, "dbt_project.yml");
        assert_eq!(f.line, Some(5));
        assert_eq!(f.context["related_files"], serde_json::json!(["tests/t.sql:2"]));
    }
}
