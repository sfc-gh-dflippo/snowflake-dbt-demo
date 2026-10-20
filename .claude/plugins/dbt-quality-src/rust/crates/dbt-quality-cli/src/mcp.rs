//! `dbt-quality mcp`: the MCP server (stdio, newline-delimited JSON-RPC 2.0).
//!
//! The caller chooses the audit root (`path`) and output directory (`out_dir`).
//! `files` must resolve inside the audit root. `report` writes findings JSON
//! and optional HTML into `out_dir`, which defaults to a temporary directory.
//! Model source in HTML requires `include_models: true` and uses a bounded
//! reader. This option does not limit what the audit reader can access.
//! `annotate` and `fix_columns` write project source only with `dry_run: false`.
//!
//! The server implements JSON-RPC directly. See `vendor/DBT_PIN.md`.

use std::io::{BufRead, Write};
use std::path::{Path, PathBuf};

use dbt_quality_core::annotate::{annotate, AnnotateOptions};
use dbt_quality_core::discovery::build_portfolio_with_ddl;
use dbt_quality_core::fix_columns::{fix_columns, FixOptions};
use dbt_quality_core::engine::run_audit;
use dbt_quality_core::model::{level_rank, meta, RULES};
use dbt_quality_core::report::{build_html_report, build_report, lint_record, HtmlReportOptions, LintPaths};
use dbt_quality_core::{catalog, html, DBT_PIN_SHA, DBT_PIN_VERSION, VERSION};
use serde_json::{json, Value};

const PROTOCOL: &str = "2025-06-18";

fn tools() -> Value {
    let level = json!({"type": "string", "enum": ["error", "warning", "information"]});
    let ddl = json!({"type": "array", "items": {"type": "string"}, "description": "scai DDL roots or .sql files for the COL rules. Replaces `ddl_paths` in .dbt-quality.yml."});
    json!([
        {
            "name": "report",
            "description": "Audit a dbt project or a directory of projects. Writes the suggestions JSON and (by default) the HTML report into out_dir, and returns their paths plus the counts. Writes nothing into `path` unless out_dir points there.",
            "inputSchema": {"type": "object", "required": ["path"], "properties": {
                "path": {"type": "string", "description": "dbt project, or a directory containing several. Caller-chosen; the server does not restrict it."},
                "out_dir": {"type": "string", "description": "Existing or creatable directory for the reports, anywhere. Relative paths resolve against the server's working directory. Default: <system temp>/dbt-quality/<hash of path>."},
                "category": {"type": "array", "items": {"type": "string"}, "description": "Limit the emitted suggestions to these packs, e.g. INC."},
                "min_level": level,
                "html": {"type": "boolean", "default": true},
                "include_models": {"type": "boolean", "default": false, "description": "Include bounded model source text in HTML. Requires html=true. Sharing the report shares this text."},
                "ddl": ddl
            }}
        },
        {
            "name": "findings",
            "description": "Return active findings as JSON (one record per finding: file, line, column, code, level, message, remediation).",
            "inputSchema": {"type": "object", "required": ["path"], "properties": {
                "path": {"type": "string"},
                "rule_ids": {"type": "array", "items": {"type": "string"}},
                "files": {"type": "array", "items": {"type": "string"}, "description": "Paths relative to `path`."},
                "min_level": level,
                "ddl": ddl
            }}
        },
        {
            "name": "annotate",
            "description": "Write EWI markers (`--** SSC-EWI-DBT... - <name>: <subject> **`) above each finding. Returns a unified diff. `path` is caller-chosen and is not restricted. Dry run by default: nothing is written unless dry_run=false. With dry_run=false it writes only files inside `path` (symlinks out of `path` are skipped), and refuses when the git tree has uncommitted changes (the two report files excepted) unless allow_dirty=true. Each run first removes the dbt-quality markers in scope: with rule_ids, only the markers of those rules; without, every dbt-quality marker. remove=true only removes them.",
            "inputSchema": {"type": "object", "required": ["path"], "properties": {
                "path": {"type": "string"},
                "rule_ids": {"type": "array", "items": {"type": "string"}},
                "min_level": level,
                "dry_run": {"type": "boolean", "default": true},
                "remove": {"type": "boolean", "default": false},
                "allow_dirty": {"type": "boolean", "default": false}
            }}
        },
        {
            "name": "fix_columns",
            "description": "Cast model output columns to the type and collation of the matching scai Snowflake DDL table. Returns one record per matched model (status, edits, warnings) and a unified diff. Dry run by default. With dry_run=false it writes the changed models and refuses when the git tree has uncommitted changes unless allow_dirty=true. Missing and extra columns are only reported as warnings.",
            "inputSchema": {"type": "object", "required": ["path"], "properties": {
                "path": {"type": "string"},
                "ddl": ddl,
                "select": {"type": "array", "items": {"type": "string"}, "description": "Globs on the root-relative model path."},
                "dry_run": {"type": "boolean", "default": true},
                "allow_dirty": {"type": "boolean", "default": false}
            }}
        },
        {
            "name": "rules",
            "description": "List rules (code, name, short_description, kind, level), filtered by pack or kind. With `code`, return that rule's full metadata record including remediation and examples.",
            "inputSchema": {"type": "object", "properties": {
                "code": {"type": "string"},
                "pack": {"type": "string"},
                "kind": {"type": "string", "enum": ["EWI", "FDM", "PRF"]}
            }}
        },
        {
            "name": "version",
            "description": "The server version and the pinned dbt version and commit.",
            "inputSchema": {"type": "object", "properties": {}}
        }
    ])
}

fn s<'a>(a: &'a Value, k: &str) -> Option<&'a str> {
    a.get(k).and_then(Value::as_str)
}

fn strs(a: &Value, k: &str) -> Vec<String> {
    a.get(k).and_then(Value::as_array).map(|v| v.iter().filter_map(Value::as_str).map(String::from).collect()).unwrap_or_default()
}

fn root_of(a: &Value) -> Result<PathBuf, String> {
    let p = s(a, "path").ok_or("`path` is required")?;
    std::fs::canonicalize(p).map_err(|e| format!("{p}: {e}"))
}

/// Resolve `p` (absolute or relative to `root`) and require it inside `root`.
fn inside(root: &Path, p: &str) -> Result<PathBuf, String> {
    let cand = if Path::new(p).is_absolute() { PathBuf::from(p) } else { root.join(p) };
    // The directory may not exist yet; canonicalize its nearest existing ancestor.
    let mut existing = cand.clone();
    let mut tail = vec![];
    while !existing.exists() {
        tail.push(existing.file_name().map(|f| f.to_owned()).ok_or("invalid path")?);
        existing = existing.parent().ok_or("invalid path")?.to_path_buf();
    }
    let mut resolved = std::fs::canonicalize(&existing).map_err(|e| e.to_string())?;
    for t in tail.into_iter().rev() {
        if t == ".." {
            return Err(format!("{p}: `..` is not allowed"));
        }
        resolved.push(t);
    }
    if !resolved.starts_with(root) {
        return Err(format!("{p} is outside {}", root.display()));
    }
    Ok(resolved)
}

/// A scratch directory for one root's reports, outside the audited tree.
fn default_out_dir(root: &Path) -> PathBuf {
    use std::hash::{Hash, Hasher};
    let mut h = std::collections::hash_map::DefaultHasher::new();
    root.hash(&mut h);
    std::env::temp_dir().join("dbt-quality").join(format!("{:016x}", h.finish()))
}

/// String array argument as paths.
fn paths_of(a: &Value, key: &str) -> Vec<PathBuf> {
    strs(a, key).into_iter().map(PathBuf::from).collect()
}

fn call(name: &str, a: &Value) -> Result<Value, String> {
    match name {
        "version" => Ok(json!({"dbt_quality": VERSION, "dbt_version": DBT_PIN_VERSION, "dbt_commit": DBT_PIN_SHA, "rules": RULES.len()})),
        "rules" => {
            if let Some(code) = s(a, "code") {
                let m = meta(&code.to_uppercase()).ok_or_else(|| format!("unknown rule {code}"))?;
                return serde_json::from_str(m.json).map_err(|e| e.to_string());
            }
            let pack = s(a, "pack").map(str::to_uppercase);
            let kind = s(a, "kind").map(str::to_uppercase);
            Ok(Value::Array(
                catalog::sorted()
                    .into_iter()
                    .filter(|m| pack.as_deref().is_none_or(|p| m.pack == p) && kind.as_deref().is_none_or(|k| m.kind == k))
                    .map(|m| json!({"code": m.code, "name": m.name, "short_description": m.short_description, "kind": m.kind, "level": m.level}))
                    .collect(),
            ))
        }
        "report" => {
            let include_models = match a.get("include_models") {
                None => false,
                Some(Value::Bool(value)) => *value,
                Some(_) => return Err("`include_models` must be a boolean".into()),
            };
            let emit_html = a.get("html").and_then(Value::as_bool).unwrap_or(true);
            if include_models && !emit_html {
                return Err("`include_models: true` requires `html: true`. Model source is only included in HTML.".into());
            }
            let root = root_of(a)?;
            let out = match s(a, "out_dir") {
                Some(d) => PathBuf::from(d),
                None => default_out_dir(&root),
            };
            let mut portfolio = build_portfolio_with_ddl(&root, &paths_of(a, "ddl"));
            if portfolio.projects.is_empty() {
                return Err(format!("No dbt_project.yml found under {}", root.display()));
            }
            let result = run_audit(&mut portfolio);
            let mut report = build_report(&result, &root.to_string_lossy());
            let wanted: Vec<String> = strs(a, "category").iter().map(|c| c.to_uppercase()).collect();
            let threshold = level_rank(s(a, "min_level").unwrap_or("information")).min(2);
            let list = report["suggestions"].as_array().cloned().unwrap_or_default();
            report["suggestions"] = Value::Array(
                list.into_iter()
                    .filter(|x| wanted.is_empty() || wanted.iter().any(|w| x["category"] == w.as_str()))
                    .filter(|x| level_rank(x["level"].as_str().unwrap_or("")).min(2) <= threshold)
                    .collect(),
            );
            std::fs::create_dir_all(&out).map_err(|e| format!("{}: {e}", out.display()))?;
            let out = std::fs::canonicalize(&out).map_err(|e| format!("{}: {e}", out.display()))?;
            let json_path = out.join("dbt-audit-suggestions.json");
            std::fs::write(&json_path, serde_json::to_string_pretty(&report).unwrap()).map_err(|e| e.to_string())?;
            let mut res = json!({"json": json_path, "counts": report["summary"]["counts"], "per_model": report["summary"]["per_model"],
                "skipped": report["skipped_checks"].as_array().map_or(0, Vec::len), "remediation_top": report["remediation"].as_array().map(|r| r.iter().take(5).map(|x| json!({"rule_id": x["rule_id"], "title": x["title"], "count": x["count"]})).collect::<Vec<_>>())});
            if emit_html {
                let html_path = out.join("dbt-audit-report.html");
                let options = HtmlReportOptions {
                    include_models, categories: wanted,
                    min_level: match threshold { 0 => "error", 1 => "warning", _ => "information" }.into(),
                };
                let html_report = build_html_report(&report, &portfolio, &options);
                std::fs::write(&html_path, html::render(&html_report)).map_err(|e| e.to_string())?;
                res["html"] = json!(html_path);
            }
            Ok(res)
        }
        "findings" => {
            let root = root_of(a)?;
            let files: Vec<PathBuf> = strs(a, "files").iter().map(|f| inside(&root, f)).collect::<Result<_, _>>()?;
            let mut portfolio = build_portfolio_with_ddl(&root, &paths_of(a, "ddl"));
            let result = run_audit(&mut portfolio);
            let paths = LintPaths::new(&root);
            let ids: Vec<String> = strs(a, "rule_ids").iter().map(|r| r.to_uppercase()).collect();
            let threshold = level_rank(s(a, "min_level").unwrap_or("information")).min(2);
            let recs: Vec<Value> = result
                .active()
                .filter(|x| level_rank(&x.level).min(2) <= threshold)
                .filter(|x| ids.is_empty() || ids.contains(&x.rule_id))
                .filter(|x| files.is_empty() || paths.absolute(x).is_some_and(|p| files.iter().any(|f| p.starts_with(f))))
                .map(|x| lint_record(x, &paths))
                .collect();
            Ok(json!({"count": recs.len(), "findings": recs}))
        }
        "fix_columns" => {
            let root = root_of(a)?;
            let opts = FixOptions {
                ddl: paths_of(a, "ddl"),
                select: strs(a, "select"),
                write: !a.get("dry_run").and_then(Value::as_bool).unwrap_or(true),
                allow_dirty: a.get("allow_dirty").and_then(Value::as_bool).unwrap_or(false),
            };
            let out = fix_columns(&root, &opts)?;
            Ok(json!({"files": out.files, "diff": out.diff, "written": opts.write}))
        }
        "annotate" => {
            let root = root_of(a)?;
            let opts = AnnotateOptions {
                rule_ids: strs(a, "rule_ids"),
                min_level: s(a, "min_level").unwrap_or("information").to_string(),
                dry_run: a.get("dry_run").and_then(Value::as_bool).unwrap_or(true),
                remove: a.get("remove").and_then(Value::as_bool).unwrap_or(false),
                allow_dirty: a.get("allow_dirty").and_then(Value::as_bool).unwrap_or(false),
            };
            let out = annotate(&root, &opts)?;
            Ok(json!({"dry_run": opts.dry_run, "written": out.written, "files_changed": out.files_changed, "markers": out.markers, "files": out.files, "diff": out.diff}))
        }
        other => Err(format!("unknown tool {other}")),
    }
}

fn handle(req: &Value) -> Option<Value> {
    let id = req.get("id").cloned();
    let method = req.get("method").and_then(Value::as_str).unwrap_or("");
    let result = match method {
        "initialize" => {
            let asked = req.pointer("/params/protocolVersion").and_then(Value::as_str).unwrap_or(PROTOCOL);
            Ok(json!({
                "protocolVersion": asked,
                "capabilities": {"tools": {"listChanged": false}},
                "serverInfo": {"name": "dbt-quality", "version": VERSION},
                "instructions": "dbt-quality detects dbt anti-patterns and writes EWI markers. report writes into a scratch out_dir, not the project. Loop: report -> annotate (dry_run) -> approve -> annotate (dry_run=false) -> fix each marker (call rules with its code for remediation and examples) -> report again."
            }))
        }
        "ping" => Ok(json!({})),
        "tools/list" => Ok(json!({"tools": tools()})),
        "tools/call" => {
            let name = req.pointer("/params/name").and_then(Value::as_str).unwrap_or("");
            let args = req.pointer("/params/arguments").cloned().unwrap_or(json!({}));
            let r = std::panic::catch_unwind(|| call(name, &args)).unwrap_or_else(|_| Err("internal error".into()));
            Ok(match r {
                Ok(v) => json!({"content": [{"type": "text", "text": serde_json::to_string_pretty(&v).unwrap()}], "structuredContent": if v.is_object() { v.clone() } else { json!({"result": v}) }, "isError": false}),
                Err(e) => json!({"content": [{"type": "text", "text": e}], "isError": true}),
            })
        }
        m if m.starts_with("notifications/") => return None,
        _ => Err(json!({"code": -32601, "message": format!("method not found: {method}")})),
    };
    let id = id?;
    Some(match result {
        Ok(r) => json!({"jsonrpc": "2.0", "id": id, "result": r}),
        Err(e) => json!({"jsonrpc": "2.0", "id": id, "error": e}),
    })
}

/// Answer JSON-RPC requests from stdin on stdout until stdin closes.
pub fn serve() {
    let stdin = std::io::stdin();
    let mut stdout = std::io::stdout().lock();
    for line in stdin.lock().lines() {
        let Ok(line) = line else { break };
        if line.trim().is_empty() {
            continue;
        }
        let resp = match serde_json::from_str::<Value>(&line) {
            Ok(Value::Array(batch)) => {
                let out: Vec<Value> = batch.iter().filter_map(handle).collect();
                (!out.is_empty()).then(|| Value::Array(out))
            }
            Ok(req) => handle(&req),
            Err(e) => Some(json!({"jsonrpc": "2.0", "id": null, "error": {"code": -32700, "message": e.to_string()}})),
        };
        if let Some(r) = resp {
            let _ = writeln!(stdout, "{r}");
            let _ = stdout.flush();
        }
    }
}
