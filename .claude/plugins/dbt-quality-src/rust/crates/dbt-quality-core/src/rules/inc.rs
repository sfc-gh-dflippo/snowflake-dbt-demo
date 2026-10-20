//! INC rules: load patterns and incremental correctness.

use regex::Regex;
use serde_json::{json, Value};

use std::collections::{BTreeSet, HashMap};

use crate::discovery::{ModelFile, ProjectContext};
use crate::jinja::{summarize, Lit};
use crate::engine::{Detect, Detector};
use crate::model::{effort, level, Suggestion};
use crate::sqlutil::{config_hooks, py_repr, py_str, span, strip_comments_and_strings, truthy};
use crate::{frx, rx};

const INC0001: &str = "SSC-EWI-DBTINC0001";
const INC0002: &str = "SSC-EWI-DBTINC0002";
const INC0003: &str = "SSC-EWI-DBTINC0003";
const INC0004: &str = "SSC-PRF-DBTINC0004";
const INC0005: &str = "SSC-PRF-DBTINC0005";
const INC0006: &str = "SSC-PRF-DBTINC0006";
const INC0007: &str = "SSC-FDM-DBTINC0007";
const INC0008: &str = "SSC-EWI-DBTINC0008";
const INC0009: &str = "SSC-PRF-DBTINC0009";
const INC0010: &str = "SSC-EWI-DBTINC0010";
const INC0011: &str = "SSC-FDM-DBTINC0011";
const INC0012: &str = "SSC-FDM-DBTINC0012";
const INC0013: &str = "SSC-PRF-DBTINC0013";
const INC0015: &str = "SSC-EWI-DBTINC0015";
const INC0016: &str = "SSC-EWI-DBTINC0016";
const INC0017: &str = "SSC-PRF-DBTINC0017";
const INC0018: &str = "SSC-EWI-DBTINC0018";
const INC0019: &str = "SSC-EWI-DBTINC0019";
const INC0020: &str = "SSC-EWI-DBTINC0020";
const INC0021: &str = "SSC-FDM-DBTINC0021";

pub const DETECTORS: &[Detector] = &[
    Detector { code: INC0001, detect: Detect::Model(truncate_and_load) },
    Detector { code: INC0002, detect: Detect::Model(delete_and_load) },
    Detector { code: INC0003, detect: Detect::Project(folder_hook_dml) },
    Detector { code: INC0004, detect: Detect::Model(manual_incremental) },
    Detector { code: INC0005, detect: Detect::Model(full_reload) },
    Detector { code: INC0006, detect: Detect::Model(no_incremental_guard) },
    Detector { code: INC0007, detect: Detect::Model(no_unique_key) },
    Detector { code: INC0008, detect: Detect::Model(no_strategy) },
    Detector { code: INC0009, detect: Detect::Model(no_watermark) },
    Detector { code: INC0010, detect: Detect::Model(hook_writes_elsewhere) },
    Detector { code: INC0011, detect: Detect::Model(merge_exclude_mismatch) },
    Detector { code: INC0012, detect: Detect::Model(append_on_mutable) },
    Detector { code: INC0013, detect: Detect::Model(unbounded_scan) },
    Detector { code: INC0015, detect: Detect::Project(external_loader) },
    Detector { code: INC0016, detect: Detect::Project(update_this_pre_hook) },
    Detector { code: INC0017, detect: Detect::Project(hook_forces_materialization) },
    Detector { code: INC0018, detect: Detect::Project(copy_into_stage_hook) },
    Detector { code: INC0019, detect: Detect::Project(runtime_hook_sql) },
    Detector { code: INC0020, detect: Detect::Project(hook_scope_mismatch) },
    Detector { code: INC0021, detect: Detect::Model(incremental_branch_columns) },
];

const VALID_STRATEGIES: [&str; 5] = ["append", "delete+insert", "insert_overwrite", "merge", "microbatch"];

fn truncate_pattern() -> &'static Regex {
    rx!(r"(?i)\btruncate\s+(?:table\s+)?(?:if\s+exists\s+)?(.{0,120})")
}
fn delete_pattern() -> &'static Regex {
    rx!(r"(?i)\bdelete\s+from\s+(.{0,120})")
}
fn drop_pattern() -> &'static Regex {
    rx!(r"(?i)\bdrop\s+table\s+(?:if\s+exists\s+)?(.{0,120})")
}
fn insert_pattern() -> &'static Regex {
    rx!(r"(?i)\b(insert\s+into|merge\s+into)\s+(.{0,120})")
}
fn this_pattern() -> &'static Regex {
    rx!(r"(?i)\{\{\s*this\s*\}\}")
}
fn is_incremental_pattern() -> &'static Regex {
    rx!(r"(?i)\bis_incremental\s*\(\s*\)")
}
fn date_window_pattern() -> &'static Regex {
    rx!(r"(?i)\b(?:dateadd|date_sub|date_add|datediff|current_date|current_timestamp|sysdate|getdate)\b")
}
fn date_predicate_pattern() -> &'static Regex {
    rx!(r#"(?i)\b(?:where|and)\s+[\w."]*(?:date|dt|day|ts|timestamp|updated|modified|created|load)[\w."]*\s*(?:>=|>)"#)
}
fn incremental_block() -> &'static Regex {
    rx!(r"(?is)\{%-?\s*if\s+is_incremental\s*\(\s*\)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}")
}

/// Keep the first `n` characters.
fn head(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

fn cfg_lower(model: &ModelFile, key: &str, default: &str) -> String {
    model.effective_config.get(key).map(py_str).unwrap_or_else(|| default.to_string()).to_lowercase()
}

fn reads_stream(model: &ModelFile) -> bool {
    if rx!(r"(?i)metadata\$action|metadata\$isupdate|metadata\$row_id|\bstream\b").is_match(&model.stripped) {
        return true;
    }
    model.refs.iter().chain(std::iter::once(&model.name)).any(|n| n.to_lowercase().contains("stream"))
}

fn is_microbatch(model: &ModelFile) -> bool {
    cfg_lower(model, "incremental_strategy", "") == "microbatch"
}

/// The relation a DML statement targets, from the text after its verb.
fn dml_target(text: &str) -> String {
    let text = text.trim();
    if text.starts_with("{{") {
        return match text.find("}}") {
            Some(c) => text[..c + 2].to_string(),
            None => text.to_string(),
        };
    }
    match rx!(r#"^[\w.$"`\[\]]+"#).find(text) {
        Some(m) => m.as_str().to_string(),
        None => text.to_string(),
    }
}

fn targets_self(text: &str, model: &ModelFile) -> bool {
    let target = dml_target(text);
    if this_pattern().is_match(&target) {
        return true;
    }
    let normalized = target.trim().trim_matches(|c| "();\"'`[]".contains(c)).to_lowercase();
    if normalized == "this" {
        return true;
    }
    normalized.rsplit('.').next().unwrap_or("") == model.name.to_lowercase()
}

/// Line of `key=` inside the model's `config(` call, or the `config(` line.
fn config_key_line(model: &ModelFile, key: &str) -> Option<u32> {
    let start = rx!(r"(?i)\{\{-?\s*config\s*\(|dbt\.config\s*\(").find(&model.raw).map_or(0, |m| m.start());
    let pat = regex::escape(key).replace(r"\-", "[-_]").replace('_', "[-_]");
    let re = Regex::new(&format!(r"\b{pat}\s*=")).ok()?;
    match re.find(&model.raw[start..]) {
        Some(m) => Some(crate::sqlutil::line_col(&model.raw, start + m.start()).0),
        None => crate::anchors::config_position(model).map(|(l, _)| l),
    }
}

// INC0001, INC0002 and INC0010 read only the model's own `config()` hooks. A folder
// `+pre-hook`/`+post-hook` is reported once at `dbt_project.yml` by INC0003, so a model
// that only inherits a hook is not reported against a file that has no hook.
fn truncate_and_load(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for (key, body) in config_hooks(&model.own_config) {
        let evidence = format!("{key}=\"{}\"", head(body.trim(), 180));
        for m in truncate_pattern().captures_iter(&body) {
            if !targets_self(&m[1], model) {
                continue;
            }
            out.push(
                Suggestion::new(INC0001, format!(
                    "`{key}` truncates a relation that appears to be this model's target. Check full identity and hook timing; a later failure can leave data missing, depending on adapter transaction behavior."))
                .file(&model.relative_path)
                .line_opt(config_key_line(model, &key))
                .evidence(evidence.clone())
                .remediation("Confirm the target and intended load contract before removing the hook. For full replacement, use the adapter's supported table materialization and verify its failure behavior; do not assume an atomic multi-statement rebuild. For change-only loads, design an incremental filter and strategy with a tested key where required. Check first-build and full-refresh behavior.")
                .effort(effort::MEDIUM),
            );
        }
        for m in drop_pattern().captures_iter(&body) {
            if !targets_self(&m[1], model) {
                continue;
            }
            out.push(
                Suggestion::new(INC0001, format!(
                    "`{key}` drops a relation that appears to be this model's target. Check physical identity and whether the drop conflicts with the materialization or leaves a missing table after failure."))
                .file(&model.relative_path)
                .line_opt(config_key_line(model, &key))
                .evidence(evidence.clone())
                .remediation(format!("Remove the hook. Use `dbt build --full-refresh --select {}` when the relation needs rebuilding.", model.name))
                .effort(effort::LOW),
            );
        }
    }
    out
}

fn delete_and_load(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for (key, body) in config_hooks(&model.own_config) {
        for m in delete_pattern().captures_iter(&body) {
            if !targets_self(&m[1], model) {
                continue;
            }
            let reads_sibling = rx!(r"\bref\s*\(").is_match(&body);
            let mut message = format!("`{key}` deletes rows from a relation that appears to be this model's target. This side effect is not a separate model node; transaction behavior depends on the adapter.");
            if reads_sibling {
                message.push_str(" The hook also contains `ref()`. Hook refs can register dependencies; verify that this ref is visible during parsing.");
            }
            out.push(
                Suggestion::new(INC0002, message)
                    .file(&model.relative_path)
                    .line_opt(config_key_line(model, &key))
                    .evidence(format!("{key}=\"{}\"", head(body.trim(), 220)))
                    .remediation("First identify which rows the hook deletes and how they are reloaded. Consider `delete+insert` with a tested `unique_key` for matched-key replacement, or a supported merge design for updates. Stock merge does not automatically delete rows because a soft-delete flag exists. Preserve deletion and rejection semantics explicitly, and verify adapter transaction and retry behavior; replacing a hook does not guarantee one transaction.")
                    .effort(effort::MEDIUM)
                    .ctx("reads_sibling_model", reads_sibling),
            );
        }
    }
    out
}

fn hook_writes_elsewhere(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for (key, body) in config_hooks(&model.own_config) {
        for m in insert_pattern().captures_iter(&body) {
            let target = dml_target(&m[2]);
            if targets_self(&m[2], model) {
                continue;
            }
            out.push(
                Suggestion::new(INC0010, format!(
                    "`{key}` runs `{}` against `{}`, a relation this model does not otherwise produce.",
                    m[1].to_lowercase(),
                    target.trim_matches(|c| "();".contains(c))))
                .file(&model.relative_path)
                .line_opt(config_key_line(model, &key))
                .evidence(format!("{key}=\"{}\"", head(body.trim(), 180)))
                .remediation("Verify the target's owner and physical location. Model business transformations separately when that expresses their dependencies and tests. For audit or control writes, preserve required per-model timing and results. Use on-run-end only if run-level logging is equivalent; its presence is not a success gate and it can run for commands other than builds.")
                .effort(effort::MEDIUM),
            );
        }
        for (name, entry) in macro_closure(project, &body) {
            for (verb, target) in macro_writes(entry.body) {
                if this_pattern().is_match(&target) || targets_self(&target, model) {
                    continue;
                }
                out.push(
                    Suggestion::new(INC0010, format!(
                        "`{key}` calls macro `{name}`, which runs `{verb}` against `{}`, a relation this model does not otherwise produce.",
                        target.trim_matches(|c| "();".contains(c))))
                    .file(&model.relative_path)
                    .line_opt(config_key_line(model, &key))
                    .evidence(format!("{key}=\"{}\"", head(body.trim(), 180)))
                    .remediation("Verify the target's owner and physical location. Model business transformations separately when that expresses their dependencies and tests. For audit or control writes, preserve required per-model timing and results. Use on-run-end only if run-level logging is equivalent; its presence is not a success gate and it can run for commands other than builds.")
                    .effort(effort::MEDIUM)
                    .ctx("macro", json!(name)),
                );
            }
        }
    }
    out
}

fn walk_hooks(node: &Value, path: &mut Vec<String>, out: &mut Vec<(String, String, String)>) {
    let Value::Object(map) = node else { return };
    for (key, value) in map {
        if ["+pre-hook", "+post-hook", "+pre_hook", "+post_hook"].contains(&key.as_str()) {
            let bodies: Vec<&Value> = match value {
                Value::Array(a) => a.iter().collect(),
                v => vec![v],
            };
            for body in bodies {
                let scope = if path.is_empty() { "<project root>".to_string() } else { path.join("/") };
                out.push((scope, key.clone(), py_str(body)));
            }
        } else if !key.starts_with('+') {
            path.push(key.clone());
            walk_hooks(value, path, out);
            path.pop();
        }
    }
}

fn call_pattern() -> &'static Regex {
    rx!(r"(?i)(?:^|;|%\}|\}\})\s*call\s+\S")
}

/// True when a converter marker for folder hooks appears in the project text.
fn has_folder_hook_marker(p: &ProjectContext) -> bool {
    let hit = |t: &str| t.contains("SSC-EWI-INF0039") || t.contains("SSC-EWI-INF0038");
    hit(&p.project_yml_text) || p.models.iter().any(|m| hit(&m.raw)) || p.macros.iter().any(|m| hit(&m.raw))
}

fn folder_hook_dml(project: &ProjectContext) -> Vec<Suggestion> {
    let mut hooks = vec![];
    if let Some(models) = project.project_yml.get("models") {
        walk_hooks(models, &mut vec![], &mut hooks);
    }
    let has_marker = has_folder_hook_marker(project);
    let mut out = vec![];
    for (scope_path, key, body) in hooks {
        let stripped = strip_comments_and_strings(&body);
        let verb = if truncate_pattern().is_match(&stripped) {
            "`truncate`"
        } else if drop_pattern().is_match(&stripped) {
            "`drop`"
        } else if delete_pattern().is_match(&stripped) {
            "`delete`"
        } else if insert_pattern().is_match(&stripped) {
            "`insert`/`merge`"
        } else if call_pattern().is_match(&stripped) {
            "`call`"
        } else {
            continue;
        };
        let call_only = verb == "`call`";
        let mut keys = vec![json!("models")];
        keys.extend(scope_path.split('/').map(|s| json!(s)));
        keys.push(json!(key));
        out.push(
            Suggestion::new(INC0003, format!(
                "A folder-level `{key}` on `{scope_path}` can run {verb} for each selected model that inherits it. Shared writes may depend on execution order."))
            .file("dbt_project.yml")
            .ctx("yaml_keys", Value::Array(keys))
            .evidence(format!("{key}: {}", head(body.trim(), 200)))
            .level(if call_only && !has_marker { level::INFORMATION } else { level::WARNING })
            .remediation("Move one-time work out of a folder hook. Choose an explicit operation or a narrowly scoped, idempotent hook with the required ordering. Run-level hooks can run for compile or test commands too; verify command timing before moving destructive SQL there. Check the original procedure's run-once contract and preserve it deliberately.")
            .effort(effort::MEDIUM),
        );
    }
    out
}

fn manual_incremental(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let mat = model.materialization();
    if model.is_python || (mat != "table" && !mat.is_empty()) {
        return vec![];
    }
    if mat.is_empty() && model.raw.trim().is_empty() {
        return vec![];
    }
    if is_incremental_pattern().is_match(&model.raw) {
        return vec![];
    }
    let Some(m) = date_predicate_pattern().find(&model.stripped) else { return vec![] };
    if !date_window_pattern().is_match(&model.stripped) {
        return vec![];
    }
    vec![Suggestion::new(INC0004, "This model has a rolling date-window filter and is a table or has no explicit materialization. Verify effective materialization and whether retaining only that window is intentional.")
        .file(&model.relative_path)
        .span(span(&model.stripped, m.start(), m.end()))
        .evidence(m.as_str().trim())
        .remediation("Keep a deliberate rolling snapshot if that is the contract. For retained history, consider incremental materialization and a suitable key/strategy. The example `where updated_at > (select max(updated_at) from {{ this }})` is incomplete: handle an empty or all-null target, tied timestamps, late arrivals, and updates. Guard target reads with `{% if is_incremental() %}` and provide a valid first-build/full-refresh path. Add an absolute floor only if it preserves outage recovery and backfills.")
        .effort(effort::MEDIUM)]
}

fn full_reload(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    if rx!(r"(?i)(_full_reload|_full_refresh|_truncate_load|_trunc_load|_reload|_rebuild)$").is_match(&model.name) {
        out.push(
            Suggestion::new(INC0005, format!("`{}` has a full-reload-style suffix. The name alone does not prove how it loads data; review the effective materialization.", model.name))
                .file(&model.relative_path)
                .evidence(model.name.clone())
                .remediation("Assess whether the source supports incremental processing. If rows carry a reliable updated-at timestamp or an immutable event time, convert to `materialized='incremental'`. If a full rebuild is required, drop the suffix and say why in the model description so the choice reads as deliberate.")
                .effort(effort::MEDIUM),
        );
    }
    if model.effective_config.get("full_refresh") == Some(&Value::Bool(true)) {
        out.push(
            Suggestion::new(INC0005, "`full_refresh: true` forces a full rebuild on every run.")
                .file(&model.relative_path)
                .evidence("full_refresh=True")
                .remediation(format!("Remove `full_refresh: true`. Trigger a rebuild on demand with `dbt build --full-refresh --select {}` instead of making every run a full refresh.", model.name))
                .effort(effort::LOW),
        );
    }
    out
}

fn no_incremental_guard(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() || model.is_python || is_microbatch(model) || reads_stream(model) {
        return vec![];
    }
    // INC0008 owns a model with no strategy: it reports the missing guard too.
    if is_incremental_pattern().is_match(&model.raw) || strategy_unset(model) {
        return vec![];
    }
    vec![Suggestion::new(INC0006, "This incremental model has no detected `is_incremental()` guard. Check compiled SQL and external checkpoints before concluding that it scans the full source.")
        .file(&model.relative_path)
        .evidence("materialized='incremental'; no is_incremental() call found")
        .remediation("Check whether a filter, external checkpoint, or source contract already limits the input. If a reliable change column is available, a guarded filter may help. This sketch is incomplete and must not be copied without handling an empty/all-null target, equal timestamps, late data, and updates:\n\n```sql\n{% if is_incremental() %}\nwhere <change_column> > (select max(<change_column>) from {{ this }})\n{% endif %}\n```\n\nProvide a valid first-build/full-refresh path. If no safe change-tracking contract exists, retain or adopt full replacement rather than inventing a watermark.")
        .effort(effort::LOW)]
}

fn no_unique_key(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() {
        return vec![];
    }
    // An unset strategy is INC0008's finding; do not assume the adapter default here.
    if strategy_unset(model) {
        return vec![];
    }
    let strategy = cfg_lower(model, "incremental_strategy", "merge");
    if strategy != "merge" && strategy != "delete+insert" {
        return vec![];
    }
    if has_unique_key(model) {
        return vec![];
    }
    vec![Suggestion::new(INC0007, format!("`{strategy}` with no `unique_key` appends, so a restated row duplicates on reprocessing."))
        .file(&model.relative_path)
        .evidence(format!("incremental_strategy='{strategy}'; unique_key absent"))
        .remediation("Confirm the business grain and null policy, then configure the required `unique_key`, such as `unique_key='order_id'` or a composite list. Add primary-key or equivalent uniqueness/not-null tests and run them. Tests validate their inputs when executed; standard Snowflake PRIMARY KEY metadata does not enforce uniqueness.")
        .effort(effort::LOW)]
}

fn strategy_unset(model: &ModelFile) -> bool {
    matches!(model.effective_config.get("incremental_strategy"), None | Some(Value::Null))
}

fn has_unique_key(model: &ModelFile) -> bool {
    truthy(model.effective_config.get("unique_key"))
}

fn unset_evidence(model: &ModelFile) -> String {
    let mut parts = vec!["incremental_strategy absent"];
    if !has_unique_key(model) {
        parts.push("unique_key absent");
    }
    if !is_incremental_pattern().is_match(&model.raw) {
        parts.push("no is_incremental() guard");
    }
    parts.join("; ")
}

fn unset_remediation(model: &ModelFile) -> String {
    if !has_unique_key(model) && !is_incremental_pattern().is_match(&model.raw) {
        return "This model has no explicit strategy, no `unique_key` and no `is_incremental()` guard. Check the adapter default, compiled filter, and original load contract; absence of a guard does not prove a full scan. For full replacement, consider `materialized='table'` (or `+materialized: table`). For change loads, choose a supported strategy, a tested key where required, and a safe filter on a real source column.".to_string();
    }
    "State the intended strategy and verify adapter support: `merge` for matched-key updates/inserts, `append` for intentional row retention, or `delete+insert` for matched-key replacement. dbt-snowflake `insert_overwrite` replaces the whole table, not individual partitions. Preserve the original load semantics.".to_string()
}

fn no_strategy(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() {
        return vec![];
    }
    match model.effective_config.get("incremental_strategy") {
        None | Some(Value::Null) => vec![Suggestion::new(INC0008, "`incremental_strategy` is unset, so the load uses the adapter default.")
            .file(&model.relative_path)
            .evidence(unset_evidence(model))
            .remediation(unset_remediation(model))
            .effort(effort::LOW)],
        Some(v) => {
            let s = py_str(v);
            if VALID_STRATEGIES.contains(&s.to_lowercase().as_str()) {
                return vec![];
            }
            vec![Suggestion::new(INC0008, format!("`incremental_strategy='{s}'` is not one of dbt-snowflake's built-in strategies."))
                .level(level::WARNING)
                .file(&model.relative_path)
                .evidence(format!("incremental_strategy='{s}'"))
                .remediation(format!("Check the installed adapter and any custom strategy macro. Built-in names recognized by this linter are: {}. A custom strategy can be valid; verify its implementation rather than replacing it solely because it is not on this list.", VALID_STRATEGIES.join(", ")))
                .effort(effort::LOW)]
        }
    }
}

fn no_watermark(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() || !is_incremental_pattern().is_match(&model.raw) {
        return vec![];
    }
    if reads_stream(model) || is_microbatch(model) {
        return vec![];
    }
    let mut out = vec![];
    for m in incremental_block().captures_iter(&model.raw) {
        let whole = m.get(0).unwrap();
        let body = &m[1];
        if this_pattern().is_match(body) {
            continue;
        }
        out.push(
            Suggestion::new(INC0009, "This incremental branch has no detected `{{ this }}` reference. Check whether an external checkpoint or another filter already implements the change-tracking contract.")
                .file(&model.relative_path)
                .span(span(&model.raw, whole.start(), whole.end()))
                .evidence(head(body.trim(), 200))
                .remediation("If the target is the intended checkpoint, derive a safe filter from it. The following sketch needs explicit handling for an empty/all-null target and equal timestamps:\n\n```sql\nwhere updated_at > (select max(updated_at) from {{ this }})\n```\n\nChoose any lookback from the late-arrival contract, include updates, and deduplicate/reprocess with a suitable key and strategy. Validate first builds, full refreshes, outages, and backfills before replacing an existing checkpoint.")
                .effort(effort::LOW),
        );
    }
    out
}

fn unbounded_scan(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() || reads_stream(model) || is_microbatch(model) {
        return vec![];
    }
    let mut out = vec![];
    for m in incremental_block().captures_iter(&model.raw) {
        let whole = m.get(0).unwrap();
        let body = &m[1];
        if !this_pattern().is_match(body) {
            continue;
        }
        let has_floor = date_window_pattern().is_match(body)
            || rx!(r"'\d{4}-\d{2}-\d{2}'").is_match(body)
            || rx!(r"\bvar\s*\(").is_match(body);
        if has_floor {
            continue;
        }
        out.push(
            Suggestion::new(INC0013, "This incremental branch references the target but has no detected independent date or variable bound. Measure pruning; this branch does not establish what the first run scans.")
                .file(&model.relative_path)
                .span(span(&model.raw, whole.start(), whole.end()))
                .evidence(head(body.trim(), 180))
                .remediation("Inspect query pruning before adding a second predicate. This seven-day example is illustrative and can lose outage or backfill rows; use it only when the retention/recovery contract permits that bound:\n\n```sql\nwhere updated_at > (select max(updated_at) from {{ this }})\n  and updated_at >= dateadd(day, -7, current_date())\n```\n\nChoose a bound that preserves late arrivals, outages, and backfills. Make recovery overrides explicit and test them. Also handle empty-target watermarks and equal timestamps; a variable alone does not make this example safe.")
                .effort(effort::LOW),
        );
    }
    out
}

fn merge_exclude_mismatch(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let excluded = model.effective_config.get("merge_exclude_columns");
    if !truthy(excluded) {
        return vec![];
    }
    let excluded = excluded.unwrap();
    // A macro can generate the column list, so the names would be absent from the text.
    let body = rx!(r"\{\{-?\s*config\s*\([\s\S]*?\)\s*-?\}\}").replace_all(&model.raw, "");
    let macro_call = frx!(r"(?i)\{\{-?\s*(?!config|ref|source|var|env_var|this|target|is_incremental)[a-z_][\w.]*\s*\(");
    if macro_call.is_match(&body).unwrap_or(false) {
        return vec![];
    }
    let columns: Vec<Value> = match excluded {
        Value::Array(a) => a.clone(),
        v => vec![v.clone()],
    };
    let listing = py_repr(&Value::Array(columns.clone()));
    let mut out = vec![];
    for column in &columns {
        let name = py_str(column).trim().to_string();
        if name.is_empty() {
            continue;
        }
        let found = Regex::new(&format!(r"(?i)\b{}\b", regex::escape(&name)))
            .map(|r| r.is_match(&model.stripped))
            .unwrap_or(false);
        if found {
            continue;
        }
        out.push(
            Suggestion::new(INC0011, format!("`merge_exclude_columns` lists `{name}`, which this model does not appear to select."))
                .file(&model.relative_path)
                .line_opt(config_key_line(model, "merge_exclude_columns"))
                .evidence(format!("merge_exclude_columns={listing}"))
                .remediation(format!("Inspect the compiled projection and existing target column before changing `{name}`. `merge_exclude_columns` controls updates, not whether the input provides insert values. Preserve defaults and generated columns. Select an appropriate value or remove the exclusion only after confirming both insert and update behavior; do not add a timestamp merely to satisfy this scan."))
                .effort(effort::LOW),
        );
    }
    out
}

fn append_on_mutable(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if !model.is_incremental() || cfg_lower(model, "incremental_strategy", "") != "append" {
        return vec![];
    }
    let re = rx!(r"(?i)\b(?:as\s+)?(updated_at|updated_date|modified_at|modified_date|last_modified|status|order_status|is_active|is_current|is_deleted|valid_to|dbt_valid_to|effective_to|end_date)\b");
    let Some(m) = re.captures(&model.stripped) else { return vec![] };
    let whole = m.get(0).unwrap();
    vec![Suggestion::new(INC0012, format!("This model selects `{}` while using `append`, which never updates existing rows.", &m[1]))
        .file(&model.relative_path)
        .span(span(&model.stripped, whole.start(), whole.end()))
        .evidence(whole.as_str().trim())
        .remediation("If rows can change, switch to `incremental_strategy='merge'` with the business `unique_key`. If the model is an immutable event stream and the column is only carried through, say so in the model description so the append is reviewable.")
        .effort(effort::MEDIUM)]
}

fn external_loader(project: &ProjectContext) -> Vec<Suggestion> {
    let names: std::collections::BTreeSet<String> = project.models.iter().map(|m| m.name.to_lowercase()).collect();
    if names.is_empty() {
        return vec![];
    }
    let mut out = vec![];
    for (path, raw) in &project.loose_sql {
        let stripped = strip_comments_and_strings(raw);
        if !rx!(r"(?i)\bcreate\s+(or\s+replace\s+)?(task|procedure)\b").is_match(&stripped) {
            continue;
        }
        for m in insert_pattern().captures_iter(&stripped) {
            let target = dml_target(&m[2]);
            let target = target.trim_matches(|c| "();\"'`".contains(c)).rsplit('.').next().unwrap_or("").to_lowercase();
            if !names.contains(&target) {
                continue;
            }
            let relative = path.strip_prefix(&project.root).unwrap_or(path).display().to_string();
            let fname = path.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            let whole = m.get(0).unwrap();
            let model_file = project.models.iter().find(|mf| mf.name.to_lowercase() == target).map(|mf| {
                let line = crate::anchors::config_position(mf).map_or(1, |(l, _)| l);
                format!("{}:{line}", crate::discovery::root_relative(project, &mf.relative_path))
            });
            out.push(
                Suggestion::new(INC0015, format!("`{fname}` has a task/procedure write whose final relation name matches model `{target}`. Confirm database, schema, alias, and quoting before concluding that both write one table."))
                    .file(relative)
                    .span(span(&stripped, whole.start(), whole.end()))
                    .evidence(head(whole.as_str().trim(), 160))
                    .remediation("Confirm full physical identity and the intended load order first. If both write the same relation, agree on one owner or a documented coordinated-write contract. Move business loading into the model where appropriate, or treat an externally owned relation as a source. Do not remove a model based on its name alone.")
                    .effort(effort::HIGH)
                    .ctx("related_files", json!(model_file.into_iter().collect::<Vec<_>>())),
            );
        }
    }
    out
}

// ---- Hook helpers shared by INC0010 and INC0016..INC0020 ----

struct MacroEntry<'a> {
    file: &'a str,
    raw: &'a str,
    body: &'a str,
}

/// Names a hook or macro body calls. Falls back to a regex when Jinja does not parse.
fn called_names(body: &str) -> Vec<String> {
    let summary = summarize(body, "hook");
    let raw: Vec<String> = if summary.parse_error.is_some() {
        rx!(r"([A-Za-z_][\w.]*)\s*\(").captures_iter(body).map(|c| c[1].to_string()).collect()
    } else {
        summary.calls.iter().map(|c| c.name.clone()).collect()
    };
    // Strip a package prefix: `pkg.macro` resolves to `macro`.
    raw.into_iter().map(|n| n.rsplit('.').next().unwrap_or("").to_string()).collect()
}

fn macro_index(p: &ProjectContext) -> HashMap<String, MacroEntry<'_>> {
    let mut idx = HashMap::new();
    for mf in &p.macros {
        for m in &mf.macros {
            idx.entry(m.name.to_lowercase()).or_insert(MacroEntry { file: &mf.relative_path, raw: &mf.raw, body: &m.body });
        }
    }
    idx
}

/// Follow a hook's macro calls, including calls from those macros.
/// Visit each macro once to prevent cycles.
fn macro_closure<'a>(p: &'a ProjectContext, body: &str) -> Vec<(String, MacroEntry<'a>)> {
    let idx = macro_index(p);
    let mut seen = BTreeSet::new();
    let mut order = vec![];
    let mut queue = called_names(body);
    while let Some(name) = queue.pop() {
        let key = name.to_lowercase();
        if !seen.insert(key.clone()) {
            continue;
        }
        if let Some(e) = idx.get(&key) {
            queue.extend(called_names(e.body));
            order.push(key);
        }
    }
    order.sort();
    let mut idx = idx;
    order.into_iter().filter_map(|k| idx.remove(&k).map(|e| (k, e))).collect()
}

/// Write statements in a macro body: (verb, target text).
fn macro_writes(body: &str) -> Vec<(String, String)> {
    let mut out = vec![];
    for m in insert_pattern().captures_iter(body) {
        out.push((m[1].to_lowercase().split_whitespace().collect::<Vec<_>>().join(" "), dml_target(&m[2])));
    }
    for m in delete_pattern().captures_iter(body) {
        out.push(("delete".to_string(), dml_target(&m[1])));
    }
    for m in rx!(r"(?i)\bupdate\s+([^\s;]+)\s+set\b").captures_iter(body) {
        out.push(("update".to_string(), dml_target(&m[1])));
    }
    out
}

/// A hook string and its source location.
struct Hook {
    file: String,
    key: String,
    body: String,
    /// `yaml_keys` for a folder hook; `None` for a model hook.
    yaml_keys: Option<Vec<Value>>,
}

impl Hook {
    fn is_pre(&self) -> bool {
        self.key.contains("pre")
    }
    fn anchor(&self, s: Suggestion) -> Suggestion {
        match &self.yaml_keys {
            Some(k) => s.ctx("yaml_keys", Value::Array(k.clone())),
            None => s,
        }
    }
}

/// Hooks defined on models and folders in `dbt_project.yml`, each listed once.
fn all_hooks(p: &ProjectContext) -> Vec<Hook> {
    let mut out = vec![];
    for m in &p.models {
        for (key, body) in config_hooks(&m.own_config) {
            out.push(Hook { file: m.relative_path.clone(), key, body, yaml_keys: None });
        }
    }
    let mut folder = vec![];
    if let Some(models) = p.project_yml.get("models") {
        walk_hooks(models, &mut vec![], &mut folder);
    }
    for (scope, key, body) in folder {
        let mut keys = vec![json!("models")];
        if scope != "<project root>" {
            keys.extend(scope.split('/').map(|s| json!(s)));
        }
        keys.push(json!(key));
        out.push(Hook { file: "dbt_project.yml".into(), key, body, yaml_keys: Some(keys) });
    }
    out
}

fn update_this_pre_hook(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for h in all_hooks(p).iter().filter(|h| h.is_pre()) {
        let stripped = strip_comments_and_strings(&h.body);
        let hit = rx!(r"(?i)\bupdate\s+(?:\{\{\s*this\s*\}\}|this\b)\s+set\b").is_match(&h.body)
            || rx!(r"(?is)\bupdate\s+\{\{\s*this\s*\}\}").is_match(&stripped);
        if !hit {
            continue;
        }
        out.push(h.anchor(
            Suggestion::new(INC0016, format!("`{}` updates this model's own relation before materialization. Verify adapter transaction behavior and whether a later failure leaves the update committed.", h.key))
                .file(&h.file)
                .evidence(format!("{}=\"{}\"", h.key, head(h.body.trim(), 200)))
                .remediation("Consider expressing matched-key changes in an incremental merge with a tested `unique_key`. Preserve the original predicates and values, then verify adapter transaction and retry behavior. A hook-to-materialization rewrite does not guarantee that every surrounding statement shares one transaction.")
                .effort(effort::MEDIUM),
        ));
    }
    out
}

fn hook_forces_materialization(p: &ProjectContext) -> Vec<Suggestion> {
    let mut seen = BTreeSet::new();
    let mut out = vec![];
    for m in &p.models {
        for (key, body) in config_hooks(&m.effective_config) {
            for r in crate::sqlutil::extract_refs(&body) {
                if r == m.name || !seen.insert(r.clone()) {
                    continue;
                }
                let Some(target) = p.model_by_name(&r) else { continue };
                let default = target.folder_config.get("materialized").map(py_str).unwrap_or_default();
                let mat = target.materialization();
                if default != "ephemeral" || (mat != "view" && mat != "table") {
                    continue;
                }
                out.push(
                    Suggestion::new(INC0017, format!("`{r}` is referenced in a hook of `{}` and builds as a {mat} despite its ephemeral folder default. The scan does not prove the hook caused that override.", m.name))
                        .file(&target.relative_path)
                        .evidence(format!("materialized='{mat}'; folder default 'ephemeral'; referenced by {key} of {}", m.name))
                        .remediation("Check why the model needs a standalone relation. If the read can move into model SQL without changing timing or results, consider restoring ephemeral. If the hook needs a physical table or view, keep the materialization and document the reason; ephemeral has no standalone relation.")
                        .effort(effort::LOW)
                        .ctx("hook_model", json!(m.name)),
                );
            }
        }
    }
    out
}

fn copy_into_stage_hook(p: &ProjectContext) -> Vec<Suggestion> {
    let copy = rx!(r"(?i)\bcopy\s+into\s+@");
    let mut out = vec![];
    for h in all_hooks(p) {
        let mut via = vec![];
        if copy.is_match(&h.body) {
            via.push(None);
        }
        via.extend(macro_closure(p, &h.body).into_iter().filter(|(_, e)| copy.is_match(e.body)).map(|(n, _)| Some(n)));
        for v in via {
            let how = match &v {
                Some(n) => format!("calls macro `{n}`, which runs `COPY INTO @...`"),
                None => "runs `COPY INTO @...`".to_string(),
            };
            out.push(h.anchor(
                Suggestion::new(INC0018, format!("`{}` {how}, an unload side effect that is not a separately selectable model node. The stage can be internal or external.", h.key))
                    .file(&h.file)
                    .evidence(format!("{}=\"{}\"", h.key, head(h.body.trim(), 180)))
                    .remediation("dbt supports unload hooks. Keep one when its timing and retry contract are correct, or move it to explicitly ordered orchestration after the required successful build. An on-run-end hook alone is not a success gate. Validate failure handling, duplicate exports, overwrite behavior, and which results must succeed before publishing files.")
                    .effort(effort::MEDIUM),
            ));
        }
    }
    out
}

fn is_var_call(text: &str) -> bool {
    rx!(r"^\s*(?:\{\{\s*)?var\s*\(").is_match(text)
}

fn lit_names(l: &Lit, out: &mut Vec<String>) {
    match l {
        Lit::Expr(t) | Lit::Str(t) => out.push(t.trim().to_string()),
        Lit::List(v) => v.iter().for_each(|i| lit_names(i, out)),
        _ => {}
    }
}

/// Advice for INC0019's non-location run-time hook overrides.
pub(crate) const OVERRIDE_FIX: &str = "These vars can supply run-time overrides through `--vars`; the pattern alone does not prove converter ownership. Do not inline them blindly. Check the caller and each read's default. Replace a read with its default only when no required override is lost. Otherwise keep the `var()` reads and document their caller and allowed values.";

fn hook_location_advice(p: &ProjectContext, text: &str) -> Option<String> {
    use super::prj::{relations, shared};
    let reads = shared::var_relation_reads(text);
    if reads.is_empty() { return None; }
    Some(reads.iter().map(|r| {
        let location = relations::read_location(p,&r.parts);
        let table = location.identifier.key().unwrap_or_else(|| "<table>".into());
        relations::source_advice(p,&location,&table,r.stage_suffix())
    }).collect::<Vec<_>>().join(" "))
}

fn runtime_hook_sql(p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    // One finding per project: every model repeats the same generated hook pattern.
    let mut hits: Vec<(&str, u32, String, String)> = vec![];
    for m in &p.models {
        let bound: BTreeSet<&str> = m
            .jinja
            .sets
            .iter()
            .filter(|s| matches!(&s.value, Lit::Expr(t) if is_var_call(t)))
            .map(|s| s.target.as_str())
            .collect();
        for call in m.jinja.calls_named("config") {
            for (k, v) in &call.kwargs {
                if !matches!(k.as_str(), "pre_hook" | "post_hook" | "pre-hook" | "post-hook") {
                    continue;
                }
                let mut exprs = vec![];
                lit_names(v, &mut exprs);
                for e in exprs {
                    if bound.contains(e.as_str()) || is_var_call(&e) || hook_location_advice(p,&e).is_some() {
                        hits.push((m.relative_path.as_str(), call.span.start_line, k.clone(), e));
                    }
                }
            }
        }
    }
    if let Some((file, line, k, e)) = hits.first() {
        let files: Vec<&str> = hits.iter().map(|h| h.0).collect::<BTreeSet<_>>().into_iter().collect();
        out.push(
            Suggestion::new(
                INC0019,
                format!(
                    "{} hook(s) in {} model(s) take their SQL from run-time variables (first: `{k}={e}`), so review the supplied values as well as the project code.",
                    hits.len(),
                    files.len()
                ),
            )
            .file(*file)
            .line(*line)
            .evidence(format!("{k}={e}"))
            .remediation(hits.iter().map(|h| hook_location_advice(p,&h.3).unwrap_or_else(|| OVERRIDE_FIX.into())).collect::<BTreeSet<_>>().into_iter().collect::<Vec<_>>().join(" "))
            .effort(effort::MEDIUM)
            .ctx("var_name", json!(e))
            .ctx("files", json!(files)),
        );
    }
    for h in all_hooks(p).into_iter().filter(|h| h.yaml_keys.is_some()) {
        if is_var_call(&h.body) || hook_location_advice(p,&h.body).is_some() {
            out.push(h.anchor(
                Suggestion::new(INC0019, format!("`{}` takes its SQL from a run-time variable, so review the supplied value as well as the project code.", h.key))
                    .file(&h.file)
                    .evidence(format!("{}: {}", h.key, head(h.body.trim(), 160)))
                    .remediation(hook_location_advice(p,&h.body).unwrap_or_else(|| OVERRIDE_FIX.into()))
                    .effort(effort::MEDIUM)
                    .ctx("var_name", json!(h.body.trim())),
            ));
        }
    }
    out
}

fn hook_scope_mismatch(p: &ProjectContext) -> Vec<Suggestion> {
    let scope_cmp = rx!(r#"(?i)variable_scope\s*=\s*['"]\{\{\s*variable_scope\s*\}\}['"]"#);
    let prefix = rx!(r"(?i)GetRunScopePrefix\s*\(\s*\)\s*\|\|");
    let orchestration = p.loose_sql.iter().any(|(_, t)| prefix.is_match(t));
    let mut seen = BTreeSet::new();
    let mut out = vec![];
    for h in all_hooks(p) {
        for (name, e) in macro_closure(p, &h.body) {
            if !seen.insert(name.clone()) || !rx!(r"(?i)control").is_match(e.body) {
                continue;
            }
            let Some(m) = scope_cmp.find(e.raw) else { continue };
            if !e.body.contains(m.as_str()) {
                continue;
            }
            let (lvl, how) = if orchestration {
                (level::WARNING, "while orchestration SQL matches `GetRunScopePrefix() || <scope>`")
            } else {
                (level::INFORMATION, "and no orchestration SQL is visible to confirm the scope format")
            };
            out.push(
                Suggestion::new(INC0020, format!("Hook macro `{name}` matches the control table on the raw `variable_scope`, {how}."))
                    .file(e.file)
                    .span(span(e.raw, m.start(), m.end()))
                    .level(lvl)
                    .evidence(m.as_str())
                    .remediation("Confirm the application's GetRunScopePrefix contract and the stored control-table values. Build the same scope on both sides without double-prefixing: apply the prefix in the macro or pass a confirmed prefixed value from orchestration. This is a local migration convention, not a generic dbt scope rule.")
                    .effort(effort::MEDIUM)
                    .ctx("macro", json!(name)),
            );
        }
    }
    out
}

/// Normalized top-level select-list names of a SQL fragment, or `None` when unusable.
fn select_names(text: &str) -> Option<BTreeSet<String>> {
    let text = rx!(r"(?s)\{#.*?#\}").replace_all(text, "");
    let text = strip_comments_and_strings(&text);
    let lower = text.to_lowercase();
    let (mut depth, mut start, mut end) = (0i32, None, lower.len());
    let b = lower.as_bytes();
    let mut i = 0;
    let word = |i: usize, w: &str| {
        lower[i..].starts_with(w)
            && (i == 0 || !(b[i - 1].is_ascii_alphanumeric() || b[i - 1] == b'_'))
            && b.get(i + w.len()).is_none_or(|c| !(c.is_ascii_alphanumeric() || *c == b'_'))
    };
    while i < b.len() {
        match b[i] {
            b'(' | b'{' => depth += 1,
            b')' | b'}' => depth -= 1,
            _ if depth == 0 && start.is_none() && word(i, "select") => start = Some(i + 6),
            _ if depth == 0 && start.is_some() && word(i, "from") => {
                end = i;
                break;
            }
            _ => {}
        }
        i += 1;
    }
    let list = text.get(start?..end)?;
    let (mut depth, mut cur, mut items) = (0i32, String::new(), vec![]);
    for c in list.chars() {
        match c {
            '(' | '{' | '[' => depth += 1,
            ')' | '}' | ']' => depth -= 1,
            ',' if depth == 0 => {
                items.push(std::mem::take(&mut cur));
                continue;
            }
            _ => {}
        }
        cur.push(c);
    }
    items.push(cur);
    let mut names = BTreeSet::new();
    for item in items {
        let item = item.trim();
        if item.is_empty() || item.contains('*') {
            return None; // Ceiling: a star hides the column list, so skip the model.
        }
        let name = match rx!(r#"(?is)\bas\s+["`]?(\w+)["`]?\s*$"#).captures(item) {
            Some(c) => c[1].to_string(),
            None => rx!(r#"["`]?(\w+)["`]?\s*$"#).captures(item)?[1].to_string(),
        };
        names.insert(name.to_lowercase());
    }
    Some(names)
}

fn incremental_branch_columns(model: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    let mut out = vec![];
    let tag = rx!(r"(?i)\{%-?\s*(if|elif|else|endif)\b[^%]*-?%\}");
    for (sp, cond) in &model.jinja.ifs {
        if !is_incremental_pattern().is_match(cond) {
            continue;
        }
        let Some(text) = model.raw.get(sp.start_offset as usize..sp.end_offset as usize) else { continue };
        let (mut depth, mut else_at, mut ok) = (0, None, true);
        let mut true_start = 0;
        let mut end_at = text.len();
        for m in tag.captures_iter(text) {
            let whole = m.get(0).unwrap();
            match m[1].to_lowercase().as_str() {
                "if" => {
                    depth += 1;
                    if depth == 1 {
                        true_start = whole.end();
                    }
                }
                "elif" if depth == 1 => ok = false,
                "else" if depth == 1 && else_at.is_none() => else_at = Some(whole),
                "endif" => {
                    depth -= 1;
                    if depth == 0 {
                        end_at = whole.start();
                        break;
                    }
                }
                _ => {}
            }
        }
        let Some(e) = else_at else { continue };
        if !ok {
            continue;
        }
        let (Some(a), Some(b)) = (select_names(&text[true_start..e.start()]), select_names(&text[e.end()..end_at])) else { continue };
        if a == b {
            continue;
        }
        let only_a: Vec<_> = a.difference(&b).cloned().collect();
        let only_b: Vec<_> = b.difference(&a).cloned().collect();
        out.push(
            Suggestion::new(INC0021, "The `is_incremental()` and `else` branches select different columns, so the incremental run writes a different shape than the full run.")
                .file(&model.relative_path)
                .span(span(&model.raw, sp.start_offset as usize, sp.end_offset as usize))
                .evidence(format!("incremental only: [{}]; full only: [{}]", only_a.join(", "), only_b.join(", ")))
                .remediation("Check compiled branch columns, types, and effective on_schema_change behavior. Prefer a stable projection with only the filter inside `{% if is_incremental() %}` when both paths should have one schema. Keep intentional differences only with a tested schema-evolution and backfill contract; added columns do not automatically backfill historical rows.")
                .effort(effort::LOW),
        );
    }
    out
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const INC: &str = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}\nselect id, updated_at from {{ ref('s') }}\n{% if is_incremental() %}\nwhere updated_at > (select max(updated_at) from {{ this }}) and updated_at >= dateadd(day, -7, current_date())\n{% endif %}\n";

    fn count(files: &[(&str, &str)], code: &str) -> usize {
        TempProject::new(files).findings(code).len()
    }

    #[test]
    fn inherited_folder_hook_is_reported_at_dbt_project_only() {
        let yml = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    silver:\n      +pre-hook: \"truncate table {{ this }}\"\n      +post-hook: \"delete from {{ this }} where 1 = 1\"\n";
        let files = [("dbt_project.yml", yml), ("models/silver/x.sql", "{{ config(materialized='table') }}\nselect 1 as id")];
        let t = TempProject::new(&files);
        // The model has no hook of its own, so no model-level finding points at it.
        for code in ["SSC-EWI-DBTINC0001", "SSC-EWI-DBTINC0002", "SSC-EWI-DBTINC0010"] {
            assert!(t.findings(code).is_empty(), "{code} must not report an inherited folder hook");
        }
        let folder = t.findings("SSC-EWI-DBTINC0003");
        assert_eq!(folder.len(), 2);
        assert!(folder.iter().all(|s| s.file == "dbt_project.yml"));
        // A model's own hook is still reported against the model.
        let own = "{{ config(pre_hook=\"truncate table {{ this }}\") }}\nselect 1 as id";
        let t = TempProject::new(&[("dbt_project.yml", yml), ("models/silver/x.sql", own)]);
        assert_eq!(t.findings("SSC-EWI-DBTINC0001").len(), 1);
    }

    #[test]
    fn folder_drop_hook_is_reported() {
        let yml = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    +pre-hook: \"drop table if exists {{ this }}\"\n";
        assert_eq!(count(&[("dbt_project.yml", yml), ("models/x.sql", "select 1")], "SSC-EWI-DBTINC0003"), 1);
    }

    #[test]
    fn inc0001() {
        let bad = "{{ config(pre_hook=\"truncate table {{ this }}\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0001"), 1);
        assert_eq!(count(&[("models/x.sql", "select 1 as id")], "SSC-EWI-DBTINC0001"), 0);
    }

    #[test]
    fn inc0002() {
        let bad = "{{ config(post_hook=\"delete from {{ this }} where d < 1\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0002"), 1);
        assert_eq!(count(&[("models/x.sql", "select 1 as id")], "SSC-EWI-DBTINC0002"), 0);
    }

    #[test]
    fn inc0003() {
        let bad = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    stg:\n      +pre-hook: \"truncate table t\"\n";
        let ok = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    stg:\n      +pre-hook: \"select 1\"\n";
        assert_eq!(count(&[("dbt_project.yml", bad), ("models/x.sql", "select 1")], "SSC-EWI-DBTINC0003"), 1);
        assert_eq!(count(&[("dbt_project.yml", ok), ("models/x.sql", "select 1")], "SSC-EWI-DBTINC0003"), 0);
    }

    #[test]
    fn inc0004() {
        let bad = "{{ config(materialized='table') }}\nselect * from t where created_at >= dateadd(day, -3, current_date())";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-PRF-DBTINC0004"), 1);
        assert_eq!(count(&[("models/x.sql", "{{ config(materialized='table') }}\nselect 1 as id")], "SSC-PRF-DBTINC0004"), 0);
    }

    #[test]
    fn inc0005() {
        assert_eq!(count(&[("models/orders_full_reload.sql", "select 1 as id")], "SSC-PRF-DBTINC0005"), 1);
        assert_eq!(count(&[("models/orders.sql", "select 1 as id")], "SSC-PRF-DBTINC0005"), 0);
    }

    #[test]
    fn inc0006() {
        let bad = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-PRF-DBTINC0006"), 1);
        assert_eq!(count(&[("models/x.sql", INC)], "SSC-PRF-DBTINC0006"), 0);
    }

    #[test]
    fn inc0007() {
        let bad = "{{ config(materialized='incremental', incremental_strategy='merge') }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-FDM-DBTINC0007"), 1);
        assert_eq!(count(&[("models/x.sql", INC)], "SSC-FDM-DBTINC0007"), 0);
    }

    #[test]
    fn inc0008() {
        let bad = "{{ config(materialized='incremental', unique_key='id') }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0008"), 1);
        assert_eq!(count(&[("models/x.sql", INC)], "SSC-EWI-DBTINC0008"), 0);
        // With no strategy, INC0008 owns the defect: INC0006 and INC0007 stay silent.
        let bare = "{{ config(materialized='incremental') }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bare)], "SSC-EWI-DBTINC0008"), 1);
        assert_eq!(count(&[("models/x.sql", bare)], "SSC-PRF-DBTINC0006"), 0);
        assert_eq!(count(&[("models/x.sql", bare)], "SSC-FDM-DBTINC0007"), 0);
    }

    #[test]
    fn inc0009() {
        let bad = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}\nselect 1 as id\n{% if is_incremental() %}\nwhere id > 5\n{% endif %}";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-PRF-DBTINC0009"), 1);
        assert_eq!(count(&[("models/x.sql", INC)], "SSC-PRF-DBTINC0009"), 0);
    }

    #[test]
    fn inc0010() {
        let bad = "{{ config(post_hook=\"insert into audit.log select 1\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0010"), 1);
        assert_eq!(count(&[("models/x.sql", "select 1 as id")], "SSC-EWI-DBTINC0010"), 0);
    }

    #[test]
    fn inc0011() {
        let bad = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge', merge_exclude_columns=['created_at']) }}\nselect 1 as id";
        let ok = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge', merge_exclude_columns=['created_at']) }}\nselect 1 as id, current_timestamp() as created_at";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-FDM-DBTINC0011"), 1);
        assert_eq!(count(&[("models/x.sql", ok)], "SSC-FDM-DBTINC0011"), 0);
    }

    #[test]
    fn inc0012() {
        let bad = "{{ config(materialized='incremental', incremental_strategy='append') }}\nselect id, status from t";
        let ok = "{{ config(materialized='incremental', incremental_strategy='append') }}\nselect id from t";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-FDM-DBTINC0012"), 1);
        assert_eq!(count(&[("models/x.sql", ok)], "SSC-FDM-DBTINC0012"), 0);
    }

    #[test]
    fn inc0013() {
        let bad = "{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}\nselect 1 as id\n{% if is_incremental() %}\nwhere id > (select max(id) from {{ this }})\n{% endif %}";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-PRF-DBTINC0013"), 1);
        assert_eq!(count(&[("models/x.sql", INC)], "SSC-PRF-DBTINC0013"), 0);
    }

    #[test]
    fn inc0015() {
        let proc = "create or replace procedure p() as begin insert into orders select 1; end;";
        assert_eq!(count(&[("models/orders.sql", "select 1 as id"), ("scripts/p.sql", proc)], "SSC-EWI-DBTINC0015"), 1);
        assert_eq!(count(&[("models/orders.sql", "select 1 as id"), ("scripts/p.sql", "select 1")], "SSC-EWI-DBTINC0015"), 0);
    }

    #[test]
    fn inc0015_shows_model_file() {
        let proc = "create or replace procedure p() as begin insert into orders select 1; end;";
        let t = TempProject::new(&[("models/orders.sql", "\n{{ config(materialized='table') }}\nselect 1 as id"), ("scripts/p.sql", proc)]);
        let f = &t.findings("SSC-EWI-DBTINC0015")[0];
        assert_eq!(f.context["related_files"], serde_json::json!(["models/orders.sql:2"]));
    }

    const CTRL_MACRO: &str = "{% macro m_update(variable_name, variable_scope) %}\nupdate public.control_variables set v = 1 where variable_name = '{{ variable_name }}' and variable_scope = '{{ variable_scope }}'\n{% endmacro %}\n{% macro wrap(a) %}{{ m_update(a, 'Package') }}{% endmacro %}";

    #[test]
    fn inc0003_call() {
        let yml = |h: &str| format!("name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    stg:\n      +pre-hook: \"{h}\"\n");
        let t = TempProject::new(&[("dbt_project.yml", &yml("CALL p.proc(1)")), ("models/x.sql", "select 1")]);
        let f = t.findings("SSC-EWI-DBTINC0003");
        assert_eq!((f.len(), f[0].level.as_str()), (1, "information"));
        let t = TempProject::new(&[("dbt_project.yml", &yml("CALL p.proc(1)")), ("models/x.sql", "-- SSC-EWI-INF0039 x\nselect 1")]);
        assert_eq!(t.findings("SSC-EWI-DBTINC0003")[0].level, "warning");
    }

    #[test]
    fn inc0010_macro() {
        let bad = "{{ config(pre_hook=\"{{ wrap('x') }}\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad), ("macros/m.sql", CTRL_MACRO)], "SSC-EWI-DBTINC0010"), 1);
        assert_eq!(count(&[("models/x.sql", bad), ("macros/m.sql", "{% macro wrap(a) %}select 1{% endmacro %}")], "SSC-EWI-DBTINC0010"), 0);
        let cyc = "{% macro wrap(a) %}{{ wrap(a) }}{% endmacro %}";
        assert_eq!(count(&[("models/x.sql", bad), ("macros/m.sql", cyc)], "SSC-EWI-DBTINC0010"), 0);
    }

    #[test]
    fn inc0016() {
        let bad = "{{ config(pre_hook=\"update {{ this }} set a = 1\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0016"), 1);
        let ok = "{{ config(post_hook=\"update {{ this }} set a = 1\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", ok)], "SSC-EWI-DBTINC0016"), 0);
    }

    #[test]
    fn inc0017() {
        let yml = "name: demo\nversion: '1.0'\nprofile: demo\nmodels:\n  demo:\n    intermediate:\n      +materialized: ephemeral\n";
        let hooked = "{{ config(pre_hook=\"select count(*) from {{ ref('int_a') }}\") }}\nselect 1 as id";
        let forced = "{{ config(materialized='view') }}\nselect 1 as id";
        let files = |a: &'static str| vec![("dbt_project.yml", yml), ("models/marts/m.sql", hooked), ("models/intermediate/int_a.sql", a)];
        assert_eq!(count(&files(forced), "SSC-PRF-DBTINC0017"), 1);
        assert_eq!(count(&files("select 1 as id"), "SSC-PRF-DBTINC0017"), 0);
    }

    #[test]
    fn inc0018() {
        let m = "{% macro copy_into_stage(p) %}{% do run_query(\"COPY INTO @\" ~ p ~ \" FROM {{ this }}\") %}{% endmacro %}";
        let bad = "{{ config(post_hook=\"{{ copy_into_stage('s') }}\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad), ("macros/m.sql", m)], "SSC-EWI-DBTINC0018"), 1);
        let direct = "{{ config(post_hook=\"copy into @s/x from {{ this }}\") }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", direct)], "SSC-EWI-DBTINC0018"), 1);
        assert_eq!(count(&[("models/x.sql", "select 1 as id")], "SSC-EWI-DBTINC0018"), 0);
    }

    #[test]
    fn inc0019() {
        let bad = "{% set pre_sql = var('k_pre_sql','') %}{% if pre_sql != '' %}{{ config(pre_hook=pre_sql) }}{% endif %}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-EWI-DBTINC0019"), 1);
        assert_eq!(count(&[("models/x.sql", bad), ("models/y.sql", bad)], "SSC-EWI-DBTINC0019"), 1);
        let ok = "{% set pre_sql = 'select 1' %}{{ config(pre_hook=pre_sql) }}\nselect 1 as id";
        assert_eq!(count(&[("models/x.sql", ok)], "SSC-EWI-DBTINC0019"), 0);
    }

    #[test]
    fn inc0020() {
        let bad = "{{ config(pre_hook=\"{{ wrap('x') }}\") }}\nselect 1 as id";
        let f = TempProject::new(&[("models/x.sql", bad), ("macros/m.sql", CTRL_MACRO)]).findings("SSC-EWI-DBTINC0020");
        assert_eq!((f.len(), f[0].level.as_str()), (1, "information"));
        let orch = "create function f() as 'select 1 where variable_scope = GetRunScopePrefix() || s';";
        let f = TempProject::new(&[("models/x.sql", bad), ("macros/m.sql", CTRL_MACRO), ("etl_configuration/f.sql", orch)]).findings("SSC-EWI-DBTINC0020");
        assert_eq!(f[0].level, "warning");
        let ok = "{% macro wrap(a) %}update public.control_variables set v = 1 where variable_scope = '{{ prefix ~ a }}'{% endmacro %}";
        assert_eq!(count(&[("models/x.sql", bad), ("macros/m.sql", ok)], "SSC-EWI-DBTINC0020"), 0);
    }

    #[test]
    fn inc0021() {
        let bad = "{% if is_incremental() %}\nselect id, a from t where a > 1\n{% else %}\nselect id, b from t\n{% endif %}";
        assert_eq!(count(&[("models/x.sql", bad)], "SSC-FDM-DBTINC0021"), 1);
        let ok = "{% if is_incremental() %}\nselect id, a from t where a > 1\n{% else %}\nselect id, a as a from t\n{% endif %}";
        assert_eq!(count(&[("models/x.sql", ok)], "SSC-FDM-DBTINC0021"), 0);
    }

    #[test]
    fn hook_findings_point_at_config_key_line() {
        let cfg = "-- header\n{{ config(\n    materialized='incremental',\n    pre_hook=\"truncate table {{ this }}\",\n    post_hook=\"delete from {{ this }} where d < 1\",\n    merge_exclude_columns=['never_here'],\n) }}\n\n{{ config(post_hook=\"x\") }}\nselect 1 as id\n";
        let cfg = cfg.replace("{{ config(post_hook=\"x\") }}\n", "");
        let ins = "{{ config(\n    post_hook=\"insert into audit.load_log select 1\"\n) }}\nselect 1 as id\n";
        let t = TempProject::new(&[("models/x.sql", &cfg), ("models/y.sql", ins)]);
        assert_eq!(t.findings("SSC-EWI-DBTINC0001")[0].line, Some(4));
        assert_eq!(t.findings("SSC-EWI-DBTINC0002")[0].line, Some(5));
        assert_eq!(t.findings("SSC-FDM-DBTINC0011")[0].line, Some(6));
        assert_eq!(t.findings("SSC-EWI-DBTINC0010")[0].line, Some(2));
    }
}
