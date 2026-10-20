//! Tallies and the `suggestions.json` contract (schema 3.0), plus the lint
//! line format the editor task parses.

use std::collections::{BTreeMap, BTreeSet};
use std::io::Read;
use std::path::{Component, Path, PathBuf};

use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};

use crate::discovery::{find_projects, ModelFile, PortfolioContext, ProjectContext};
use crate::engine::AuditResult;
use crate::model::{effort_rank, level, lint_token, meta, severity, Suggestion, RULES};
use crate::rx;

pub const SCHEMA_VERSION: &str = "3.0";

fn level_penalty(l: &str) -> f64 {
    match l {
        level::ERROR => 10.0,
        level::WARNING => 4.0,
        level::INFORMATION => 1.0,
        _ => 0.0,
    }
}

pub const CATEGORY_WEIGHT: &[(&str, f64)] = &[
    ("INC", 1.5), ("MIG", 1.4), ("TST", 1.2), ("COL", 1.2), ("SQL", 1.0), ("PRJ", 1.0),
    ("MAT", 0.9), ("MAC", 0.7), ("ARC", 0.6), ("OPS", 0.6), ("DOC", 0.4),
];

pub fn category_label(c: &str) -> &str {
    match c {
        "PRJ" => "Project structure & fragmentation",
        "INC" => "Load patterns & incremental",
        "SQL" => "Query construction",
        "MAC" => "Macro discipline",
        "MAT" => "Materialization fitness",
        "TST" => "Testing & constraints",
        "DOC" => "Documentation",
        "ARC" => "Architecture & lineage",
        "MIG" => "Migration debt",
        "COL" => "Column contract vs scai DDL",
        "OPS" => "Operational hygiene",
        other => other,
    }
}

fn category_weight(c: &str) -> f64 {
    CATEGORY_WEIGHT.iter().find(|(k, _)| *k == c).map_or(1.0, |(_, w)| *w)
}

/// Round a display value to a fixed number of decimal places.
/// Exact ties round away from zero, unlike Python's ties-to-even rule.
fn round_to(x: f64, digits: i32) -> f64 {
    let f = 10f64.powi(digits);
    (x * f).round() / f
}

fn per_model(total: usize, model_count: usize) -> f64 {
    if model_count == 0 { 0.0 } else { round_to(total as f64 / model_count as f64, 2) }
}

pub fn tally(suggestions: &[&Suggestion], model_count: usize) -> Value {
    let active: Vec<&&Suggestion> = suggestions.iter().filter(|s| !s.suppressed).collect();
    let count = |f: &dyn Fn(&Suggestion) -> bool| active.iter().filter(|s| f(s)).count();
    let counts = json!({
        "error": count(&|s| s.level == level::ERROR),
        "warning": count(&|s| s.level == level::WARNING),
        "information": count(&|s| s.level == level::INFORMATION),
        "critical": count(&|s| s.severity == severity::CRITICAL),
        "high": count(&|s| s.severity == severity::HIGH),
        "medium": count(&|s| s.severity == severity::MEDIUM),
        "low": count(&|s| s.severity == severity::LOW),
        "suppressed": suggestions.iter().filter(|s| s.suppressed).count(),
        "total": active.len(),
    });
    let mut cats: BTreeSet<String> = CATEGORY_WEIGHT.iter().map(|(c, _)| c.to_string()).collect();
    cats.extend(active.iter().map(|s| s.category.clone()));
    let categories: Vec<Value> = cats
        .iter()
        .map(|c| {
            let of = |l: &str| active.iter().filter(|s| &s.category == c && s.level == l).count();
            let (e, w, i) = (of(level::ERROR), of(level::WARNING), of(level::INFORMATION));
            json!({
                "category": c, "label": category_label(c), "error": e, "warning": w, "information": i,
                "total": e + w + i, "per_model": per_model(e + w + i, model_count),
            })
        })
        .collect();
    json!({ "counts": counts, "per_model": per_model(active.len(), model_count), "categories": categories })
}

pub fn rank_remediation(suggestions: &[Suggestion], limit: usize) -> Vec<Value> {
    let mut groups: BTreeMap<&str, Vec<&Suggestion>> = BTreeMap::new();
    let mut order: Vec<&str> = vec![];
    for s in suggestions.iter().filter(|s| !s.suppressed) {
        if !groups.contains_key(s.rule_id.as_str()) {
            order.push(&s.rule_id);
        }
        groups.entry(&s.rule_id).or_default().push(s);
    }
    let mut ranked: Vec<(f64, Value)> = order
        .iter()
        .map(|rid| {
            let items = &groups[rid];
            let mut worst = items[0];
            for s in items.iter().skip(1) {
                if level_penalty(&s.level) > level_penalty(&worst.level) {
                    worst = s;
                }
            }
            let lw = match level_penalty(&worst.level) {
                0.0 => 1.0,
                p => p,
            };
            let impact = lw * category_weight(&worst.category) * (1.0 + items.len().min(25) as f64 / 25.0);
            let effort = items.iter().map(|s| effort_rank(&s.effort)).min().unwrap_or(2) as f64;
            let priority = round_to(impact / effort, 3);
            let m = meta(rid);
            let files: BTreeSet<&str> = items.iter().map(|s| s.file.as_str()).filter(|f| !f.is_empty()).collect();
            let v = json!({
                "rule_id": rid,
                "title": m.map_or(worst.title.as_str(), |m| m.name),
                "rationale": m.map_or("", |m| m.long_description),
                "category": worst.category,
                "category_label": category_label(&worst.category),
                "level": worst.level,
                "tier": worst.tier,
                "effort": worst.effort,
                "count": items.len(),
                "priority": priority,
                "remediation": worst.remediation,
                "affected_files": files.into_iter().take(10).collect::<Vec<_>>(),
                "example": { "file": worst.file, "line": worst.line, "message": worst.message, "evidence": worst.evidence },
            });
            (priority, v)
        })
        .collect();
    // Most findings first; priority, then rule code, break ties.
    ranked.sort_by(|a, b| {
        b.1["count"].as_u64().cmp(&a.1["count"].as_u64())
            .then_with(|| b.0.partial_cmp(&a.0).unwrap())
            .then_with(|| a.1["rule_id"].as_str().cmp(&b.1["rule_id"].as_str()))
    });
    ranked.into_iter().take(limit).map(|(_, v)| v).collect()
}

pub fn now_iso() -> String {
    let secs = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0) as i64;
    let (days, rem) = (secs.div_euclid(86400), secs.rem_euclid(86400));
    // Civil-from-days (Howard Hinnant).
    let z = days + 719468;
    let era = z.div_euclid(146097);
    let doe = z - era * 146097;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = yoe + era * 400 + if m <= 2 { 1 } else { 0 };
    format!("{y:04}-{m:02}-{d:02}T{:02}:{:02}:{:02}+00:00", rem / 3600, rem % 3600 / 60, rem % 60)
}

pub fn build_report(result: &AuditResult, root: &str) -> Value {
    let total_models: usize = result.projects.iter().map(|p| p["model_count"].as_u64().unwrap_or(0) as usize).sum();
    let all: Vec<&Suggestion> = result.suggestions.iter().collect();
    let overall = tally(&all, total_models);
    let per_project: Vec<Value> = result
        .projects
        .iter()
        .map(|p| {
            let name = p["label"].as_str().or(p["name"].as_str()).unwrap_or("");
            let mine: Vec<&Suggestion> = result.suggestions.iter().filter(|s| s.project == name).collect();
            let mut o = p.as_object().cloned().unwrap_or_default();
            o.insert("tally".into(), tally(&mine, p["model_count"].as_u64().unwrap_or(0) as usize));
            Value::Object(o)
        })
        .collect();
    let suppressed: Vec<&Suggestion> = result.suggestions.iter().filter(|s| s.suppressed).collect();
    let mut by_rule = Map::new();
    let mut by_reason = Map::new();
    for s in &suppressed {
        let n = by_rule.get(&s.rule_id).and_then(Value::as_u64).unwrap_or(0);
        by_rule.insert(s.rule_id.clone(), (n + 1).into());
        let n = by_reason.get(&s.suppressed_reason).and_then(Value::as_u64).unwrap_or(0);
        by_reason.insert(s.suppressed_reason.clone(), (n + 1).into());
    }
    let mut summary = json!({
        "project_count": result.projects.len(),
        "model_count": total_models,
        "rules_registered": RULES.iter().filter(|r| r.status == "active").count(),
        "rules_skipped": result.skipped.len(),
    });
    for (k, v) in overall.as_object().unwrap() {
        summary[k] = v.clone();
    }
    let mut catalog: Vec<_> = RULES.iter().collect();
    catalog.sort_by_key(|r| r.code);
    json!({
        "schema_version": SCHEMA_VERSION,
        "generated": now_iso(),
        "root": root,
        "summary": summary,
        "projects": per_project,
        "remediation": rank_remediation(&result.suggestions, 20),
        "suggestions": result.suggestions.iter().map(Suggestion::to_json).collect::<Vec<_>>(),
        "suppressed": {
            "count": suppressed.len(),
            "by_rule": by_rule,
            "by_reason": by_reason,
            "reason": suppressed.first().map_or("", |s| s.suppressed_reason.as_str()),
            "note": if suppressed.is_empty() { "" } else {
                "Architecture-tier suggestions were withheld because these models are mechanically converted lift-and-shift output. They are opportunities for a later modernisation pass, not defects introduced by this team, and they do not affect the score."
            },
        },
        "skipped_checks": result.skipped.iter().map(|s| json!({"rule_id": s.rule_id, "title": s.title, "reason": s.reason})).collect::<Vec<_>>(),
        "errors": result.errors,
        "rule_catalog": catalog.iter().map(|m| json!({
            "rule_id": m.code, "title": m.name, "category": m.pack, "category_label": category_label(m.pack),
            "tier": m.tier, "default_level": m.level,
            "rationale": m.long_description, "short_description": m.short_description,
        })).collect::<Vec<_>>(),
    })
}

/// Source limits apply to HTML snapshots, not to the audit reader.
pub const HTML_MODEL_FILE_BYTES: usize = 256 * 1024;
pub const HTML_MODEL_TOTAL_BYTES: usize = 4 * 1024 * 1024;
pub const HTML_MODEL_FILE_COUNT: usize = 100;
pub const HTML_SCHEMA_VERSION: &str = "1.0";

/// HTML options do not change the findings JSON contract.
#[derive(Debug, Clone)]
pub struct HtmlReportOptions {
    pub include_models: bool,
    pub categories: Vec<String>,
    pub min_level: String,
}

impl Default for HtmlReportOptions {
    fn default() -> Self {
        Self { include_models: false, categories: vec![], min_level: level::INFORMATION.into() }
    }
}

/// Add HTML-only data to an already filtered report. The original is unchanged.
///
/// Only files that returned findings refer to are listed: each finding's own
/// file, files named in its context, or the project `dbt_project.yml` when the
/// finding has no file. `finding_files` has one list per returned suggestion,
/// each entry `{id, line}`. An empty list means evidence only.
/// `finding_models` keeps the first id (or null) for older consumers.
pub fn build_html_report(report: &Value, portfolio: &PortfolioContext, options: &HtmlReportOptions) -> Value {
    let mut output = report.clone();
    let root = std::fs::canonicalize(&portfolio.root).ok();
    let findings = report["suggestions"].as_array().map(Vec::as_slice).unwrap_or_default();
    // Root-relative model path -> discovered owners, to refuse ambiguous files.
    let mut model_owners = BTreeMap::<String, Vec<(&ProjectContext, &ModelFile)>>::new();
    for project in &portfolio.projects {
        for model in &project.models {
            model_owners.entry(root_file(project, &model.relative_path)).or_default().push((project, model));
        }
    }
    let mut files = BTreeMap::<String, (String, Value)>::new();
    let mut finding_files = Vec::with_capacity(findings.len());
    let (mut included_files, mut included_bytes) = (0, 0);
    for finding in findings {
        let mut refs: Vec<(String, Option<u64>)> = vec![];
        let own = finding["file"].as_str().unwrap_or("");
        let hinted = finding["project_path"].as_str().filter(|path| !path.is_empty());
        if !own.is_empty() && !own.starts_with('<') {
            refs.push((own.to_string(), finding["line"].as_u64()));
        }
        for value in finding["context"].as_object().into_iter().flat_map(|context| context.values()) {
            for item in value.as_array().map_or_else(|| vec![value], |items| items.iter().collect()) {
                let Some(text) = item.as_str() else { continue };
                let (path, line) = match text.rsplit_once(':') {
                    Some((path, line)) if line.parse::<u64>().is_ok() => (path, line.parse().ok()),
                    _ => (text, None),
                };
                if REPORT_FILE_EXTENSIONS.iter().any(|ext| path.to_ascii_lowercase().ends_with(&format!(".{ext}"))) {
                    refs.push((path.to_string(), line));
                }
            }
        }
        let owner = |path: &str| -> Option<&ProjectContext> {
            hinted.and_then(|hint| portfolio.projects.iter().find(|p| p.relative_root == hint))
                .filter(|p| p.relative_root == "." || path.starts_with(&format!("{}/", p.relative_root)))
                .or_else(|| portfolio.projects.iter()
                    .filter(|p| p.relative_root == "." || path.starts_with(&format!("{}/", p.relative_root)))
                    .max_by_key(|p| p.relative_root.len()))
        };
        // A finding that names no file is about its project: show dbt_project.yml.
        let names_file = !refs.is_empty();
        // Context paths can be project-relative; make them root-relative.
        let mut resolved: Vec<(String, Option<u64>)> = vec![];
        for (path, line) in refs {
            let candidates = [Some(path.clone()), hinted.filter(|hint| *hint != ".").map(|hint| format!("{hint}/{path}"))];
            let found = candidates.into_iter().flatten().find(|candidate| {
                root.as_deref().is_some_and(|root| root.join(candidate).is_file()) && owner(candidate).is_some()
            });
            let Some(file) = found else { continue };
            // Keep each distinct line of a file. A reference with a line replaces one without.
            if let Some(slot) = resolved.iter_mut().find(|(seen, seen_line)| *seen == file && (seen_line.is_none() || line.is_none() || *seen_line == line)) {
                if slot.1.is_none() {
                    slot.1 = line;
                }
            } else {
                resolved.push((file, line));
            }
        }
        if !names_file
            && let Some(project) = hinted.and_then(|hint| portfolio.projects.iter().find(|p| p.relative_root == hint)) {
                resolved.push((root_file(project, "dbt_project.yml"), None));
            }
        let mut links = vec![];
        for (file, line) in resolved {
            let Some(project) = owner(&file) else { continue };
            let entry = files.entry(file.clone()).or_insert_with(|| {
                let in_project = file.strip_prefix(&format!("{}/", project.relative_root)).unwrap_or(&file).to_string();
                let identity = serde_json::to_vec(&(&project.relative_root, &file)).unwrap();
                let id = format!("model-{:x}", Sha256::digest(identity));
                let owners = model_owners.get(&file).map_or(0, Vec::len);
                let audited = match model_owners.get(&file).map(Vec::as_slice) {
                    Some([(_, model)]) => Some(model.raw.as_str()),
                    _ if in_project == "dbt_project.yml" => Some(project.project_yml_text.as_str()),
                    _ => None,
                };
                let safe = root.as_deref().ok_or("unavailable_root").and_then(|root| safe_report_file(root, project, &in_project));
                let source = if owners > 1 {
                    source_status("ambiguous", "More than one discovered project owns this file.")
                } else if let Err(status) = &safe {
                    source_status(status, source_status_message(status))
                } else if !options.include_models {
                    source_status("not_included", "File text was not included. Select a local file to view an unverified copy.")
                } else if included_files >= HTML_MODEL_FILE_COUNT {
                    source_status("file_count_limit", "The report reached the 100-file source limit.")
                } else {
                    match model_snapshot(safe.as_ref().unwrap(), audited, HTML_MODEL_TOTAL_BYTES - included_bytes) {
                        Ok(snapshot) => {
                            included_files += 1;
                            included_bytes += snapshot["byte_length"].as_u64().unwrap() as usize;
                            snapshot
                        }
                        Err(status) => source_status(status, source_status_message(status)),
                    }
                };
                let lower = in_project.to_ascii_lowercase();
                let language = if lower.ends_with(".py") { "python" } else if lower.ends_with(".sql") { "sql" } else if lower.ends_with(".sh") { "shell" } else { "yaml" };
                let linkable = owners <= 1 && safe.is_ok();
                (id.clone(), json!({
                    "id": id, "project": project.label, "project_path": project.relative_root,
                    "file": file, "model_path": in_project,
                    // The absolute path on the audit machine. Sharing the report shares this path.
                    "path": crate::discovery::display_path(&project.root.join(&in_project)),
                    "language": language, "linkable": linkable, "source": source,
                }))
            });
            if entry.1["linkable"] == true {
                // A whole-file reference (no line, or line 1) opens at the first code line, not a header comment.
                let line = match line {
                    None | Some(1) if !file.ends_with(".yml") && !file.ends_with(".yaml") => entry.1["source"]["text"].as_str().and_then(first_code_line).or(line),
                    _ => line,
                };
                links.push(json!({"id": entry.0, "line": line}));
            }
        }
        finding_files.push(links);
    }
    let finding_models: Vec<Value> = finding_files.iter().map(|links| links.first().map_or(Value::Null, |link| link["id"].clone())).collect();
    // Excluded and ambiguous files have no link, so they are not listed at all.
    files.retain(|_, (_, entry)| entry["linkable"] == true);
    let models: Map<String, Value> = files.into_values().collect();
    let active = findings.iter().filter(|finding| finding["suppressed"] != true).count();
    let all_active = report["summary"]["counts"]["total"].as_u64().unwrap_or(0);
    let all_suppressed = report["summary"]["counts"]["suppressed"].as_u64().unwrap_or(0);
    output["html"] = json!({
        "schema_version": HTML_SCHEMA_VERSION,
        "filters": { "categories": options.categories, "min_level": options.min_level },
        "counts": {
            "all_audit": { "returned": all_active + all_suppressed, "active": all_active, "suppressed": all_suppressed },
            "returned": { "returned": findings.len(), "active": active, "suppressed": findings.len() - active },
        },
        "include_models": options.include_models,
        "models": models, "finding_files": finding_files, "finding_models": finding_models,
        "limits": { "per_file_bytes": HTML_MODEL_FILE_BYTES, "total_bytes": HTML_MODEL_TOTAL_BYTES, "files": HTML_MODEL_FILE_COUNT },
        "included": { "files": included_files, "bytes": included_bytes },
        "source_notice": if options.include_models {
            "This report includes the text of files that findings refer to. Sharing the report shares that text. Findings describe the audit snapshot, not later edits."
        } else {
            "File text is not included. Selected local files need an explicit association and remain unverified."
        },
    });
    output
}

/// A project-relative path as a root-relative path.
fn root_file(project: &ProjectContext, path: &str) -> String {
    if project.relative_root == "." { path.to_string() } else { format!("{}/{}", project.relative_root, path) }
}

fn source_status(status: &str, message: &str) -> Value {
    json!({ "status": status, "message": message, "alignment": "unverified", "editable": false })
}

fn source_status_message(status: &str) -> &'static str {
    match status {
        "unsafe_path" => "The model path is outside the audit or project root, or is not an exact safe model path.",
        "symlink" => "Model snapshots do not follow symbolic links.",
        "non_model" => "Configuration, profiles, and non-model files are not included.",
        "not_regular" => "Only regular model files can be included.",
        "invalid_utf8" => "The model is not valid UTF-8. No replacement text was included.",
        "binary" => "The model contains unsupported control bytes. It was not included.",
        "file_size_limit" => "The model exceeds the 256 KiB source limit. It was not truncated.",
        "total_size_limit" => "The model would exceed the 4 MiB report source limit. It was not truncated.",
        "changed_during_read" => "The model changed while its snapshot was read. It was not included.",
        _ => "The model source is unavailable. Only the finding evidence can be shown.",
    }
}

fn clean_relative(path: &str, allow_root: bool) -> bool {
    if allow_root && path == "." {
        return true;
    }
    !path.is_empty() && !path.contains(['\\', ':', '\0']) && !Path::new(path).is_absolute()
        && path.split('/').all(|part| !part.is_empty() && part != "." && part != "..")
}

/// File types the report can show for a finding.
const REPORT_FILE_EXTENSIONS: [&str; 5] = ["sql", "py", "yml", "yaml", "sh"];

/// The first line that is not blank and not only a comment, 1-based.
fn first_code_line(text: &str) -> Option<u64> {
    let mut in_block = false;
    for (index, line) in text.lines().enumerate() {
        let line = line.trim();
        if in_block {
            in_block = !(line.contains("*/") || line.contains("#}"));
            continue;
        }
        if line.is_empty() || line.starts_with("--") || line.starts_with('#') {
            continue;
        }
        if line.starts_with("/*") || line.starts_with("{#") {
            in_block = !(line.contains("*/") || line.contains("#}"));
            continue;
        }
        return Some(index as u64 + 1);
    }
    None
}

fn safe_report_file(root: &Path, project: &ProjectContext, in_project: &str) -> Result<PathBuf, &'static str> {
    if !clean_relative(&project.relative_root, true) || !clean_relative(in_project, false) {
        return Err("unsafe_path");
    }
    let project_path = if project.relative_root == "." { root.to_path_buf() } else { root.join(&project.relative_root) };
    let path = project_path.join(in_project);
    if project.root != project_path {
        return Err("unsafe_path");
    }
    // Profiles and secret stores can hold credentials; findings about them
    // keep their redacted evidence only. Hidden and generated trees stay out.
    let excluded = in_project.split('/').any(|part| {
        let lower = part.to_ascii_lowercase();
        let stem = lower.split('.').next().unwrap_or("");
        part.starts_with('.') || matches!(stem, "profiles" | "profile" | "credentials" | "secrets")
            || crate::discovery::EXCLUDED_DIRS.contains(&lower.as_str())
    });
    let allowed = path.extension().and_then(|ext| ext.to_str())
        .is_some_and(|ext| REPORT_FILE_EXTENSIONS.contains(&ext.to_ascii_lowercase().as_str()));
    if excluded || !allowed {
        return Err("non_model");
    }
    // Check each component before canonicalization; an in-root link is also refused.
    let mut component_path = root.to_path_buf();
    for component in path.strip_prefix(root).map_err(|_| "unsafe_path")?.components() {
        let Component::Normal(name) = component else { return Err("unsafe_path") };
        component_path.push(name);
        let metadata = std::fs::symlink_metadata(&component_path).map_err(|_| "unavailable")?;
        if metadata.file_type().is_symlink() {
            return Err("symlink");
        }
    }
    let canonical_project = std::fs::canonicalize(&project_path).map_err(|_| "unavailable")?;
    let canonical = std::fs::canonicalize(&path).map_err(|_| "unavailable")?;
    if !canonical_project.starts_with(root) || !canonical.starts_with(&canonical_project) || canonical != path {
        return Err("unsafe_path");
    }
    let metadata = std::fs::symlink_metadata(&canonical).map_err(|_| "unavailable")?;
    if !metadata.is_file() {
        return Err("not_regular");
    }
    Ok(canonical)
}

fn model_snapshot(path: &Path, audited: Option<&str>, remaining: usize) -> Result<Value, &'static str> {
    let file = std::fs::File::open(path).map_err(|_| "unavailable")?;
    let before = file.metadata().map_err(|_| "unavailable")?;
    if !before.is_file() {
        return Err("not_regular");
    }
    if before.len() > HTML_MODEL_FILE_BYTES as u64 {
        return Err("file_size_limit");
    }
    if before.len() > remaining as u64 {
        return Err("total_size_limit");
    }
    let limit = HTML_MODEL_FILE_BYTES.min(remaining);
    let mut bytes = Vec::new();
    (&file).take(limit as u64 + 1).read_to_end(&mut bytes).map_err(|_| "unavailable")?;
    if bytes.len() > limit {
        return Err(if limit < HTML_MODEL_FILE_BYTES { "total_size_limit" } else { "file_size_limit" });
    }
    let after = file.metadata().map_err(|_| "unavailable")?;
    if after.len() != before.len() || bytes.len() as u64 != after.len() || before.modified().ok() != after.modified().ok() {
        return Err("changed_during_read");
    }
    let original = std::str::from_utf8(&bytes).map_err(|_| "invalid_utf8")?;
    if bytes.iter().any(|byte| *byte < 0x20 && !matches!(*byte, b'\t' | b'\r' | b'\n')) || bytes.contains(&0x7f) {
        return Err("binary");
    }
    // `audited` is the text the rules read, when the audit kept it. Other
    // files were read for this report only, so their alignment is `current`.
    let alignment = match audited {
        Some(audited) if crate::annotate::blank_owned_markers(original) == audited => "verified",
        Some(_) => "stale",
        None => "current",
    };
    let bom = original.starts_with('\u{feff}');
    let text = original.strip_prefix('\u{feff}').unwrap_or(original);
    let crlf = text.as_bytes().windows(2).filter(|pair| *pair == b"\r\n").count();
    let lf = text.bytes().filter(|byte| *byte == b'\n').count() - crlf;
    let cr = text.bytes().filter(|byte| *byte == b'\r').count() - crlf;
    let newline = match (crlf > 0, lf > 0, cr > 0) {
        (false, false, false) => "none", (true, false, false) => "crlf",
        (false, true, false) => "lf", (false, false, true) => "cr", _ => "mixed",
    };
    Ok(json!({
        "status": if alignment == "stale" { "stale" } else { "included" },
        "alignment": alignment,
        "message": if alignment == "stale" { "File text changed after the audit. Finding locations are not verified." }
            else if newline == "mixed" { "Mixed line endings: view only. The original bytes can be downloaded." }
            else if newline == "cr" { "CR-only line endings: view only. Finding lines are not suitable for this code view." }
            else if alignment == "current" { "File text was read when the report was generated. Edits require a new audit." }
            else { "File text matches the audited source. Edits require a new audit." },
        "text": text, "encoding": "utf-8", "bom": bom, "newline": newline,
        "final_newline": text.ends_with(['\r', '\n']), "line_count": text.split('\n').count(),
        "byte_length": bytes.len(), "sha256": format!("{:x}", Sha256::digest(&bytes)),
        "editable": newline != "mixed" && newline != "cr",
    }))
}

// ---------------------------------------------------------------------------
// Lint output
// ---------------------------------------------------------------------------

pub const LINT_HINT_LIMIT: usize = 140;

pub fn one_line(t: &str) -> String {
    t.split_whitespace().collect::<Vec<_>>().join(" ")
}

pub fn fix_hint(remediation: &str) -> String {
    let text = one_line(&rx!(r"(?s)```.*?```").replace_all(remediation, ""));
    if text.is_empty() {
        return String::new();
    }
    let sentence = text.split(". ").next().unwrap_or("").trim_end_matches(['.', ' ']).to_string();
    if sentence.chars().count() > LINT_HINT_LIMIT {
        let cut: String = sentence.chars().take(LINT_HINT_LIMIT - 1).collect();
        return format!("{}\u{2026}", cut.trim_end());
    }
    sentence
}

/// Resolves a suggestion's path relative to the lint root.
pub struct LintPaths {
    root: std::path::PathBuf,
    projects: Vec<std::path::PathBuf>,
    /// Project name -> project roots with that name (names can repeat).
    by_name: BTreeMap<String, Vec<std::path::PathBuf>>,
}

impl LintPaths {
    pub fn new(root: &Path) -> Self {
        let root = std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf());
        let projects = find_projects(&root);
        let mut by_name: BTreeMap<String, Vec<std::path::PathBuf>> = BTreeMap::new();
        for p in &projects {
            let text = std::fs::read_to_string(p.join("dbt_project.yml")).unwrap_or_default();
            let name = crate::discovery::load_yaml_str(&text)
                .ok()
                .and_then(|v| v.get("name").filter(|n| crate::sqlutil::truthy(Some(n))).map(crate::sqlutil::py_str))
                .unwrap_or_else(|| p.file_name().map(|f| f.to_string_lossy().to_string()).unwrap_or_default());
            by_name.entry(name).or_default().push(p.clone());
        }
        LintPaths { root, projects, by_name }
    }

    /// The file a suggestion names, resolved against its own project first.
    fn own_project_file(&self, s: &Suggestion) -> Option<std::path::PathBuf> {
        let roots = self.by_name.get(&s.project)?;
        roots.iter().map(|r| r.join(&s.file)).find(|c| c.is_file())
    }

    fn rel(&self, p: &Path) -> String {
        let r = std::fs::canonicalize(p).unwrap_or_else(|_| p.to_path_buf());
        crate::discovery::display_path(r.strip_prefix(&self.root).unwrap_or(p))
    }

    fn fallback(&self) -> String {
        self.projects
            .iter()
            .map(|p| p.join("dbt_project.yml"))
            .find(|c| c.is_file())
            .map_or_else(|| "dbt_project.yml".into(), |c| self.rel(&c))
    }

    /// Absolute path of the file a suggestion targets, if it exists.
    pub fn absolute(&self, s: &Suggestion) -> Option<std::path::PathBuf> {
        if s.file.is_empty() {
            return None;
        }
        let c = Path::new(&s.file);
        if c.is_absolute() {
            return c.is_file().then(|| c.to_path_buf());
        }
        // Findings carry root-relative paths.
        if self.root.join(&s.file).is_file() {
            return Some(self.root.join(&s.file));
        }
        if let Some(own) = self.own_project_file(s) {
            return Some(own);
        }
        if let Some(project) = self.projects.iter().find(|p| p.join(&s.file).is_file()) {
            return Some(project.join(&s.file));
        }
        let direct = self.root.join(&s.file);
        direct.is_file().then_some(direct)
    }

    pub fn relative(&self, s: &Suggestion) -> String {
        if s.file.is_empty() {
            return self.fallback();
        }
        let c = Path::new(&s.file);
        if c.is_absolute() {
            return if c.is_file() { self.rel(c) } else { self.fallback() };
        }
        if self.root.join(&s.file).is_file() {
            return s.file.clone();
        }
        if let Some(own) = self.own_project_file(s) {
            return self.rel(&own);
        }
        if let Some(project) = self.projects.iter().find(|p| p.join(&s.file).is_file()) {
            return self.rel(&project.join(&s.file));
        }
        if self.root.join(&s.file).is_file() {
            return s.file.clone();
        }
        self.fallback()
    }
}

/// `path:line:col:endLine:endCol: level: [RULE] message -> fix`
pub fn lint_line(s: &Suggestion, paths: &LintPaths) -> String {
    let line = s.line.filter(|l| *l != 0).unwrap_or(1);
    let col = s.column.filter(|c| *c != 0).unwrap_or(1);
    let mut out = format!(
        "{}:{line}:{col}:{}:{}: {}: [{}] {}",
        paths.relative(s),
        s.end_line.filter(|l| *l != 0).unwrap_or(line),
        s.end_column.filter(|c| *c != 0).unwrap_or(col),
        lint_token(&s.level),
        s.rule_id,
        one_line(&s.message)
    );
    let hint = fix_hint(&s.remediation);
    if !hint.is_empty() {
        out.push_str(&format!(" -> {hint}."));
    }
    out
}

pub fn lint_record(s: &Suggestion, paths: &LintPaths) -> Value {
    let line = s.line.filter(|l| *l != 0).unwrap_or(1);
    let col = s.column.filter(|c| *c != 0).unwrap_or(1);
    json!({
        "file": paths.relative(s), "line": line, "column": col,
        "end_line": s.end_line.filter(|l| *l != 0).unwrap_or(line),
        "end_column": s.end_column.filter(|c| *c != 0).unwrap_or(col),
        "severity": lint_token(&s.level), "level": s.level, "code": s.rule_id,
        "message": one_line(&s.message), "remediation": one_line(&s.remediation),
    })
}

#[cfg(test)]
mod html_source_tests {
    use super::*;
    use crate::discovery::build_portfolio;
    use crate::testing::TempProject;

    #[test]
    fn whole_file_links_skip_header_comments() {
        assert_eq!(first_code_line("-- note\n\n/* a\n b */\n{# c #}\nselect 1"), Some(6));
        assert_eq!(first_code_line("#!/bin/sh\n# run\ndbt run"), Some(3));
        assert_eq!(first_code_line("select 1"), Some(1));
        assert_eq!(first_code_line("-- only a comment"), None);
        assert!(REPORT_FILE_EXTENSIONS.contains(&"sh"));
    }

    #[test]
    fn finding_files_keep_every_line_and_show_shell_scripts() {
        let t = TempProject::new(&[
            ("models/x.sql", "-- header\nselect 1\nunion\nselect 2\nfrom t"),
            ("models/y.sql", "-- header\nselect 3"),
            ("run.sh", "#!/bin/sh\ndbt run\ndbt test"),
        ]);
        let portfolio = build_portfolio(t.path());
        let finding = json!({"project_path": ".", "file": "models/x.sql", "line": 3,
            "context": {"related_files": ["models/x.sql:5", "models/x.sql", "models/y.sql:1", "run.sh:2", "run.sh:3"]}});
        let report = json!({"suggestions": [finding], "summary": {"counts": {"total": 1, "suppressed": 0}}});
        let html = build_html_report(&report, &portfolio, &HtmlReportOptions { include_models: true, ..Default::default() });
        let models = &html["html"]["models"];
        let links: Vec<(String, Option<u64>)> = html["html"]["finding_files"][0].as_array().unwrap().iter()
            .map(|link| (models[link["id"].as_str().unwrap()]["file"].as_str().unwrap().to_string(), link["line"].as_u64()))
            .collect();
        assert_eq!(links, vec![
            ("models/x.sql".into(), Some(3)),
            ("models/x.sql".into(), Some(5)),
            ("models/y.sql".into(), Some(2)),
            ("run.sh".into(), Some(2)),
            ("run.sh".into(), Some(3)),
        ]);
    }

    fn report_for(portfolio: &PortfolioContext, include_models: bool) -> Value {
        let suggestions: Vec<Value> = portfolio.projects.iter().flat_map(|project| {
            project.models.iter().map(|model| json!({
                "project_path": project.relative_root,
                "file": if project.relative_root == "." { model.relative_path.clone() }
                    else { format!("{}/{}", project.relative_root, model.relative_path) },
            }))
        }).collect();
        let report = json!({"suggestions": suggestions, "summary": {"counts": {"total": suggestions.len(), "suppressed": 0}}});
        build_html_report(&report, portfolio, &HtmlReportOptions { include_models, ..Default::default() })
    }

    fn sources(report: &Value) -> Vec<&Value> {
        report["html"]["models"].as_object().unwrap().values().map(|model| &model["source"]).collect()
    }

    #[test]
    fn remediation_orders_by_finding_count() {
        // INC has the higher category weight, so the old priority order put it first.
        let mut suggestions = vec![Suggestion::new("SSC-EWI-DBTINC0001", "x")];
        suggestions.extend((0..3).map(|_| Suggestion::new("SSC-EWI-DBTDOC0001", "x")));
        let ranked = rank_remediation(&suggestions, 20);
        let order: Vec<_> = ranked.iter().map(|item| (item["rule_id"].as_str().unwrap(), item["count"].as_u64().unwrap())).collect();
        assert_eq!(order, [("SSC-EWI-DBTDOC0001", 3), ("SSC-EWI-DBTINC0001", 1)]);
    }

    #[test]
    fn defaults_do_not_include_text_or_hashes_and_keep_count_scopes() {
        let project = TempProject::new(&[("models/a.sql", "select 1 as original_only")]);
        let portfolio = build_portfolio(project.path());
        let report = json!({
            "summary": {"counts": {"total": 8, "suppressed": 4}},
            "suggestions": [
                {"project_path": ".", "file": "models/a.sql"},
                {"project_path": ".", "file": "models/a.sql", "suppressed": true},
            ],
        });
        let options = HtmlReportOptions { categories: vec!["SQL".into()], min_level: "warning".into(), ..Default::default() };
        let html = build_html_report(&report, &portfolio, &options);
        assert!(report.get("html").is_none());
        assert_eq!(html["suggestions"], report["suggestions"]);
        assert_eq!(html["html"]["filters"], json!({"categories": ["SQL"], "min_level": "warning"}));
        assert_eq!(html["html"]["counts"]["all_audit"], json!({"returned": 12, "active": 8, "suppressed": 4}));
        assert_eq!(html["html"]["counts"]["returned"], json!({"returned": 2, "active": 1, "suppressed": 1}));
        assert!(!html.to_string().contains("original_only"));
        let source = sources(&html)[0];
        assert_eq!(source["status"], "not_included");
        assert!(source.get("sha256").is_none() && source.get("text").is_none());
        assert!(html["html"]["finding_models"][0].is_string());
        assert_eq!(html["html"]["finding_models"][0], html["html"]["finding_models"][1]);
    }

    #[test]
    fn exact_identities_distinguish_projects_basenames_and_unicode() {
        let project = TempProject::new(&[
            ("one/dbt_project.yml", "name: same\n"), ("two/dbt_project.yml", "name: same\n"),
            ("one/models/left/orders.sql", "select 1"), ("one/models/right/orders.sql", "select 2"),
            ("two/models/left/orders.sql", "select 3"), ("two/models/\u{e9}tude.sql", "select '\u{e9}'"),
        ]);
        let portfolio = build_portfolio(project.path());
        let html = report_for(&portfolio, true);
        let ids: BTreeSet<_> = html["html"]["finding_models"].as_array().unwrap().iter().map(|id| id.as_str().unwrap()).collect();
        assert_eq!(ids.len(), 4);
        assert_eq!(html["html"]["included"]["files"], 4);
        for model in html["html"]["models"].as_object().unwrap().values() {
            assert!(!model["file"].as_str().unwrap().contains('\\'));
            assert_eq!(model["source"]["alignment"], "verified");
            let path = model["path"].as_str().unwrap();
            assert!(Path::new(path).is_absolute() && path.ends_with(model["file"].as_str().unwrap()), "{path}");
        }
        let other = TempProject::new(&[
            ("one/dbt_project.yml", "name: same\n"), ("two/dbt_project.yml", "name: same\n"),
            ("one/models/left/orders.sql", "select 1"), ("one/models/right/orders.sql", "select 2"),
            ("two/models/left/orders.sql", "select 3"), ("two/models/\u{e9}tude.sql", "select '\u{e9}'"),
        ]);
        // Model ids do not depend on the audit root; full paths do.
        let moved = report_for(&build_portfolio(other.path()), true);
        let keys = |report: &Value| report["html"]["models"].as_object().unwrap().keys().cloned().collect::<Vec<_>>();
        assert_eq!(keys(&html), keys(&moved));
        assert_ne!(html["html"]["models"], moved["html"]["models"]);
    }

    #[test]
    fn source_round_trip_preserves_markers_bom_and_newlines() {
        for original in [
            "\u{feff}--** SSC-EWI-DBTSQL0007 - Existing marker **\r\nselect '\u{e9}'\r\n",
            "--** SSC-EWI-DBTSQL0007 - Existing marker **\nselect 1",
            "select 1\n", "select 1\r\n", "select 1\r", "select 1\nfrom t\r\n", "",
        ] {
            let project = TempProject::new(&[("models/a.sql", original)]);
            let portfolio = build_portfolio(project.path());
            let html = report_for(&portfolio, true);
            let source = sources(&html)[0];
            let recovered = format!("{}{}", if source["bom"] == true { "\u{feff}" } else { "" }, source["text"].as_str().unwrap());
            assert_eq!(recovered.as_bytes(), original.as_bytes());
            assert_eq!(source["sha256"], format!("{:x}", Sha256::digest(original.as_bytes())));
            assert_eq!(source["status"], "included");
            assert_eq!(source["alignment"], "verified");
            assert_eq!(source["final_newline"], original.ends_with(['\r', '\n']));
            assert_eq!(source["editable"], source["newline"] != "mixed" && source["newline"] != "cr");
        }
    }

    #[test]
    fn changed_missing_invalid_and_binary_sources_are_not_verified() {
        let project = TempProject::new(&[("models/a.sql", "select 1")]);
        let portfolio = build_portfolio(project.path());
        project.write("models/a.sql", "select 2");
        let html = report_for(&portfolio, true);
        assert_eq!(sources(&html)[0]["status"], "stale");
        assert_eq!(sources(&html)[0]["alignment"], "stale");
        for (bytes, status) in [(&b"select \xff"[..], "invalid_utf8"), (&b"select \0"[..], "binary"), (&b"select \x01"[..], "binary")] {
            std::fs::write(project.path().join("models/a.sql"), bytes).unwrap();
            let lossy_portfolio = build_portfolio(project.path());
            let html = report_for(&lossy_portfolio, true);
            assert_eq!(sources(&html)[0]["status"], status);
            assert!(sources(&html)[0].get("text").is_none());
        }
        std::fs::remove_file(project.path().join("models/a.sql")).unwrap();
        let html = report_for(&portfolio, true);
        assert!(html["html"]["finding_files"][0].as_array().unwrap().is_empty(), "a deleted file is not replaced by another file");
        assert!(html["html"]["finding_models"][0].is_null());
    }

    #[test]
    fn findings_show_project_files_but_never_profiles() {
        let project = TempProject::new(&[
            ("models/a.sql", "select 1"), ("profiles.yml", "password: private_sentinel\n"),
            ("models/profiles.py", "private_sentinel"), ("macros/a.sql", "{% macro m() %}macro_text{% endmacro %}"),
            ("models/_models.yml", "version: 2\nmodels:\n  - name: a\n"), (".secrets/x.yml", "private_sentinel"),
        ]);
        let portfolio = build_portfolio(project.path());
        let report = json!({"summary": {"counts": {"total": 9, "suppressed": 0}}, "suggestions": [
            {"project_path": ".", "file": "profiles.yml", "evidence": "password: [REDACTED]"},
            {"project_path": ".", "file": "models/profiles.py"}, {"project_path": ".", "file": ".secrets/x.yml"},
            {"project_path": ".", "file": "macros/a.sql", "line": 1},
            {"project_path": ".", "file": "models/_models.yml", "line": 3},
            {"project_path": ".", "file": ""},
            {"project_path": ".", "file": "dbt_project.yml", "context": {"members": ["models/a.sql:1", "models/_models.yml:3"]}},
            {"project_path": ".", "file": "a.sql"}, {"project_path": ".", "file": "models\\a.sql"},
        ]});
        let html = build_html_report(&report, &portfolio, &HtmlReportOptions { include_models: true, ..Default::default() });
        let files = |index: usize| -> Vec<(String, Value)> {
            html["html"]["finding_files"][index].as_array().unwrap().iter().map(|link| {
                (html["html"]["models"][link["id"].as_str().unwrap()]["file"].as_str().unwrap().to_string(), link["line"].clone())
            }).collect()
        };
        for index in [0, 1, 2, 7, 8] {
            assert!(files(index).is_empty(), "finding {index} must be evidence only: {:?}", files(index));
        }
        assert_eq!(files(3), [("macros/a.sql".to_string(), json!(1))]);
        assert_eq!(files(4), [("models/_models.yml".to_string(), json!(3))]);
        assert_eq!(files(5), [("dbt_project.yml".to_string(), Value::Null)], "a project finding shows dbt_project.yml");
        assert_eq!(files(6).iter().map(|(file, _)| file.as_str()).collect::<Vec<_>>(), ["dbt_project.yml", "models/a.sql", "models/_models.yml"]);
        assert_eq!(files(6)[2].1, json!(3), "context line numbers are kept");
        let text = html.to_string();
        assert!(!text.contains("private_sentinel") && text.contains("[REDACTED]"));
        assert!(text.contains("macro_text"));
        let yaml = &html["html"]["models"][html["html"]["finding_files"][4][0]["id"].as_str().unwrap()];
        assert_eq!(yaml["language"], "yaml");
        assert_eq!(yaml["source"]["alignment"], "current", "schema YAML was not kept by the audit");
        let project_yml = &html["html"]["models"][html["html"]["finding_files"][5][0]["id"].as_str().unwrap()];
        assert_eq!(project_yml["source"]["alignment"], "verified", "dbt_project.yml text is kept by the audit");
        // Models with no returned finding are not embedded.
        assert_eq!(html["html"]["models"].as_object().unwrap().len(), 4);
    }

    #[test]
    fn non_models_and_ambiguous_findings_remain_evidence_only() {
        let project = TempProject::new(&[
            ("models/a.sql", "select 1"), ("profiles.yml", "password: private_sentinel\n"),
            ("models/profiles.py", "private_sentinel"),
        ]);
        let portfolio = build_portfolio(project.path());
        let mut html = report_for(&portfolio, true);
        html["suggestions"] = json!([
            {"project_path": ".", "file": "profiles.yml", "evidence": "password: [REDACTED]"},
            {"project_path": ".", "file": "models/profiles.py"},
            {"project_path": ".", "file": "a.sql"}, {"project_path": ".", "file": "models\\a.sql"},
        ]);
        let html = build_html_report(&html, &portfolio, &HtmlReportOptions { include_models: true, ..Default::default() });
        assert!(html["html"]["finding_models"].as_array().unwrap().iter().all(Value::is_null));
        assert!(!html.to_string().contains("private_sentinel"));
        assert!(html.to_string().contains("[REDACTED]"));
        assert!(html["html"]["models"].as_object().unwrap().values().all(|model| !model["file"].as_str().unwrap().contains("profiles")));
    }

    #[test]
    fn duplicate_discovery_and_nested_ownership_are_ambiguous() {
        for files in [
            vec![("dbt_project.yml", "name: outer\nmodel-paths: [models, models]\n"), ("models/a.sql", "select 1")],
            vec![("dbt_project.yml", "name: outer\n"), ("models/inner/dbt_project.yml", "name: inner\n"), ("models/inner/models/a.sql", "select 1")],
        ] {
            let project = TempProject::new(&files);
            let html = report_for(&build_portfolio(project.path()), true);
            assert!(sources(&html).iter().all(|source| source["status"] == "ambiguous"));
            assert!(html["html"]["finding_models"].as_array().unwrap().iter().all(Value::is_null));
            assert_eq!(html["html"]["included"]["files"], 0);
        }
    }

    #[test]
    fn rejects_absolute_parent_and_windows_path_spellings() {
        for path in ["../a.sql", "/a.sql", "C:/a.sql", "C:\\a.sql", "\\\\host\\a.sql", "models/../a.sql", "models//a.sql", "models/./a.sql"] {
            assert!(!clean_relative(path, false), "{path}");
        }
        let project = TempProject::new(&[
            ("outer/dbt_project.yml", "name: outer\nmodel-paths: [../shared]\n"), ("shared/a.sql", "select 1"),
        ]);
        let html = report_for(&build_portfolio(project.path()), true);
        assert!(html["html"]["models"].as_object().unwrap().is_empty(), "{}", html["html"]["models"]);
        assert!(html["html"]["finding_models"][0].is_null());
    }

    #[cfg(unix)]
    #[test]
    fn symlink_files_directories_and_in_root_profiles_are_rejected() {
        use std::os::unix::fs::symlink;
        let project = TempProject::new(&[("models/a.sql", "select 1"), ("profiles.yml", "private_sentinel")]);
        let outside = TempProject::new(&[("models/a.sql", "outside_sentinel")]);
        symlink(project.path().join("profiles.yml"), project.path().join("models/profile_link.sql")).unwrap();
        symlink(outside.path().join("models/a.sql"), project.path().join("models/outside.sql")).unwrap();
        symlink(outside.path().join("models"), project.path().join("models/directory")).unwrap();
        let html = report_for(&build_portfolio(project.path()), true);
        // Only the regular model is listed; the three links are evidence only.
        let listed: Vec<_> = html["html"]["models"].as_object().unwrap().values().map(|model| model["file"].as_str().unwrap()).collect();
        assert_eq!(listed, ["models/a.sql"]);
        assert_eq!(html["html"]["finding_files"].as_array().unwrap().iter().filter(|links| links.as_array().unwrap().is_empty()).count(), 3);
        assert_eq!(html["html"]["included"]["files"], 1);
        assert!(!html.to_string().contains("private_sentinel"));
        assert!(!html.to_string().contains("outside_sentinel"));
    }

    #[test]
    fn real_audit_keeps_profiles_redacted_and_links_model_findings() {
        let project = TempProject::new(&[
            ("models/a.sql", "select a.id from a, b where a.id = b.id\n"),
            ("profiles.yml", "demo:\n  outputs:\n    dev:\n      type: snowflake\n      password: private_profile_sentinel\n"),
        ]);
        let mut portfolio = build_portfolio(project.path());
        let result = crate::engine::run_audit(&mut portfolio);
        let report = build_report(&result, ".");
        assert!(report.get("html").is_none());
        let html = build_html_report(&report, &portfolio, &HtmlReportOptions { include_models: true, ..Default::default() });
        assert!(!html.to_string().contains("private_profile_sentinel"));
        let findings = html["suggestions"].as_array().unwrap();
        let links = html["html"]["finding_models"].as_array().unwrap();
        assert_eq!(findings.len(), links.len());
        let model_index = findings.iter().position(|finding| finding["rule_id"] == "SSC-EWI-DBTSQL0007").unwrap();
        assert!(links[model_index].is_string());
        for (finding, link) in findings.iter().zip(links) {
            if finding["file"] == "profiles.yml" { assert!(link.is_null()); }
        }
    }

    #[test]
    fn special_files_and_absolute_model_roots_are_not_included() {
        let project = TempProject::new(&[("models/a.sql", "select 1")]);
        let portfolio = build_portfolio(project.path());
        std::fs::remove_file(project.path().join("models/a.sql")).unwrap();
        std::fs::create_dir(project.path().join("models/a.sql")).unwrap();
        let html = report_for(&portfolio, true);
        assert!(html["html"]["finding_files"][0].as_array().unwrap().is_empty(), "a directory is not shown as a file");
        assert!(html["html"]["finding_models"][0].is_null());
        let outside = TempProject::new(&[("models/a.sql", "outside_source_sentinel")]);
        let outside_path = crate::discovery::display_path(&outside.path().join("models"));
        project.write("dbt_project.yml", &format!("name: demo\nmodel-paths: [{}]\n", serde_json::to_string(&outside_path).unwrap()));
        let html = report_for(&build_portfolio(project.path()), true);
        assert!(html["html"]["finding_files"].as_array().unwrap().iter().flat_map(|links| links.as_array().unwrap())
            .all(|link| html["html"]["models"][link["id"].as_str().unwrap()]["file"] != outside_path.as_str()));
        assert!(!html.to_string().contains("outside_source_sentinel"));
    }

    #[test]
    fn enforces_file_total_and_count_limits_without_truncation() {
        let project = TempProject::new(&[("models/a.sql", "select 1")]);
        let portfolio = build_portfolio(project.path());
        let max_file = " ".repeat(HTML_MODEL_FILE_BYTES);
        project.write("models/a.sql", &max_file);
        let html = report_for(&portfolio, true);
        assert_eq!(sources(&html)[0]["byte_length"], HTML_MODEL_FILE_BYTES);
        project.write("models/a.sql", &(max_file.clone() + " "));
        let html = report_for(&portfolio, true);
        assert_eq!(sources(&html)[0]["status"], "file_size_limit");
        assert!(sources(&html)[0].get("text").is_none());
        for index in 0..=HTML_MODEL_TOTAL_BYTES / HTML_MODEL_FILE_BYTES {
            project.write(&format!("models/b{index:03}.sql"), &max_file);
        }
        let html = report_for(&build_portfolio(project.path()), true);
        assert_eq!(html["html"]["included"]["bytes"], HTML_MODEL_TOTAL_BYTES);
        assert_eq!(html["html"]["included"]["files"], 16);
        assert!(sources(&html).iter().any(|source| source["status"] == "total_size_limit"));
        let small = TempProject::new(&[("models/a.sql", "select 1")]);
        for index in 0..HTML_MODEL_FILE_COUNT {
            small.write(&format!("models/b{index:03}.py"), "pass\n");
        }
        let html = report_for(&build_portfolio(small.path()), true);
        assert_eq!(html["html"]["included"]["files"], HTML_MODEL_FILE_COUNT);
        assert_eq!(sources(&html).iter().filter(|source| source["status"] == "file_count_limit").count(), 1);
    }
}
