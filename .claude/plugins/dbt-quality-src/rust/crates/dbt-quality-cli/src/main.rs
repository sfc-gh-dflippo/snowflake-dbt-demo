//! `dbt-quality` command-line interface.
//!
//! Commands: `audit`, `lint`, `rules`, `validate`,
//! `setup-tasks`, `annotate`, `fix-columns`, and `mcp`. Human-readable output goes to stderr.
//! Findings do not fail the command unless an error-exit option is set.

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use clap::{Parser, Subcommand};
use dbt_quality_core::annotate::{annotate, AnnotateOptions};
use dbt_quality_core::discovery::{build_portfolio, build_portfolio_with_ddl, find_projects};
use dbt_quality_core::fix_columns::{fix_columns, FixOptions};
use dbt_quality_core::engine::{run_audit, run_single_file};
use dbt_quality_core::model::{level, level_rank, meta, RULES};
use dbt_quality_core::report::{build_html_report, build_report, category_label, lint_line, lint_record, HtmlReportOptions, LintPaths};
use dbt_quality_core::{catalog, html, tasks};
use serde_json::{json, Value};

mod mcp;

#[derive(Parser)]
#[command(name = "dbt-quality", version, about = "Audit dbt projects for anti-patterns and produce a quality assessment.")]
struct Cli {
    #[command(subcommand)]
    command: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    /// Run the audit and write suggestions JSON (and optionally the HTML report).
    Audit {
        #[arg(default_value = ".")]
        root: PathBuf,
        /// Write suggestions JSON here.
        #[arg(short, long)]
        out: Option<PathBuf>,
        /// Emit suggestions JSON on stdout.
        #[arg(long)]
        stdout: bool,
        /// Write the HTML report here.
        #[arg(long)]
        html: Option<PathBuf>,
        /// Include model text in HTML. Sharing the report shares this source text.
        #[arg(long, requires = "html")]
        include_models: bool,
        /// Limit to categories, e.g. INC.
        #[arg(short, long)]
        category: Vec<String>,
        #[arg(long, default_value = "information")]
        min_level: String,
        /// Exit 1 if any error-level suggestion is found.
        #[arg(long)]
        fail_on_error: bool,
        /// Plain output (accepted for compatibility; output is always plain).
        #[arg(long)]
        simple: bool,
        /// Suppress the console summary.
        #[arg(short, long)]
        quiet: bool,
        /// scai DDL root or file for the COL rules. Replaces `ddl_paths`.
        #[arg(long)]
        ddl: Vec<PathBuf>,
    },
    /// Emit suggestions in a linter format an editor can parse.
    Lint {
        #[arg(default_value = ".")]
        root: PathBuf,
        /// text | json
        #[arg(long = "format", default_value = "text")]
        format: String,
        #[arg(long, default_value = "information")]
        min_level: String,
        /// Exit 1 if any error-level suggestion is found.
        #[arg(long)]
        strict: bool,
        /// scai DDL root or file for the COL rules. Replaces `ddl_paths`.
        #[arg(long)]
        ddl: Vec<PathBuf>,
    },
    /// List the rules. `--format markdown` writes the rule catalog.
    Rules {
        /// table | json | markdown
        #[arg(long = "format", default_value = "table")]
        format: String,
        /// Show one rule's full record.
        #[arg(long)]
        code: Option<String>,
        #[arg(long)]
        simple: bool,
    },
    /// Validate one model file and report suggestions.
    Validate {
        #[arg(env = "FILE_PATH")]
        path: String,
        #[arg(long)]
        simple: bool,
        #[arg(long)]
        strict: bool,
    },
    /// Add the dbt-quality lint tasks to the project's .vscode/tasks.json.
    SetupTasks {
        #[arg(default_value = ".")]
        path: PathBuf,
    },
    /// Write EWI markers for findings into the dbt files (dry run by default).
    Annotate {
        #[arg(default_value = ".")]
        root: PathBuf,
        /// Only these rule codes. Markers of other rules stay in place.
        #[arg(long = "rule")]
        rule_ids: Vec<String>,
        #[arg(long, default_value = "information")]
        min_level: String,
        /// Write the files. Without this, print the diff only.
        #[arg(long)]
        write: bool,
        /// Remove dbt-quality markers (only those of the --rule codes, when given) instead of writing new ones.
        #[arg(long)]
        remove: bool,
        /// Write even when the git tree has uncommitted changes.
        #[arg(long)]
        allow_dirty: bool,
    },
    /// Cast model output columns to the scai DDL type and collation (dry run by default).
    FixColumns {
        #[arg(default_value = ".")]
        root: PathBuf,
        /// scai DDL root or file. Replaces `ddl_paths`.
        #[arg(long)]
        ddl: Vec<PathBuf>,
        /// Only models whose root-relative path matches this glob.
        #[arg(long)]
        select: Vec<String>,
        /// Write the files. Without this, print the diff only.
        #[arg(long)]
        write: bool,
        /// Write even when the git tree has uncommitted changes.
        #[arg(long)]
        allow_dirty: bool,
        /// text | json
        #[arg(long = "format", default_value = "text")]
        format: String,
    },
    /// Run the MCP server on stdio. The MCP client starts this command.
    Mcp,
}

fn filter_suggestions(report: &mut Value, category: &[String], min_level: &str) {
    let wanted: Vec<String> = category.iter().map(|c| c.to_uppercase()).collect();
    let threshold = level_rank(&min_level.to_lowercase()).min(2);
    let list = report["suggestions"].as_array().cloned().unwrap_or_default();
    report["suggestions"] = Value::Array(
        list.into_iter()
            .filter(|s| wanted.is_empty() || wanted.iter().any(|w| s["category"] == w.as_str()))
            .filter(|s| level_rank(s["level"].as_str().unwrap_or("")).min(2) <= threshold)
            .collect(),
    );
}

fn print_summary(report: &Value, destination: Option<&Path>) {
    let s = &report["summary"];
    let c = &s["counts"];
    eprintln!("{:<36} {:>6} {:>8} {:>12} {:>10}", "Category", "Error", "Warning", "Information", "Per model");
    for e in s["categories"].as_array().into_iter().flatten() {
        if e["total"] == 0 {
            continue;
        }
        let n = |k: &str| if e[k] == 0 { "-".to_string() } else { e[k].to_string() };
        eprintln!(
            "{:<36} {:>6} {:>8} {:>12} {:>10.2}",
            e["label"].as_str().unwrap_or(""),
            n("error"),
            n("warning"),
            n("information"),
            e["per_model"].as_f64().unwrap_or(0.0)
        );
    }
    eprintln!();
    eprintln!("Projects: {}   Models: {}", s["project_count"], s["model_count"]);
    eprintln!("Suggestions: {} — {} error, {} warning, {} information", c["total"], c["error"], c["warning"], c["information"]);
    eprintln!("Severity: {} critical, {} high, {} medium, {} low", c["critical"], c["high"], c["medium"], c["low"]);
    eprintln!("Per model: {:.2}", s["per_model"].as_f64().unwrap_or(0.0));
    eprintln!("Rules skipped: {}", s["rules_skipped"]);
    if c["suppressed"].as_u64().unwrap_or(0) > 0 {
        eprintln!("Suppressed (lift-and-shift): {} architecture suggestion(s)", c["suppressed"]);
    }
    if let Some(d) = destination {
        eprintln!("\nSuggestions written to {}", d.display());
    }
    let top: Vec<&Value> = report["remediation"].as_array().into_iter().flatten().take(5).collect();
    if !top.is_empty() {
        eprintln!("\nMost frequent findings");
        for i in top {
            eprintln!("  {}  {}  ({}, effort {})", i["rule_id"].as_str().unwrap_or(""), i["title"].as_str().unwrap_or(""), i["count"], i["effort"].as_str().unwrap_or(""));
        }
    }
}

fn no_projects(root: &Path) -> bool {
    find_projects(&std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf())).is_empty()
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match cli.command {
        Cmd::Audit { root, out, stdout, html: html_out, include_models, category, min_level, fail_on_error, simple: _, quiet, ddl } => {
            let root = std::fs::canonicalize(&root).unwrap_or(root);
            if no_projects(&root) {
                eprintln!("No dbt_project.yml found under {}", root.display());
                return ExitCode::from(1);
            }
            let mut portfolio = build_portfolio_with_ddl(&root, &ddl);
            let result = run_audit(&mut portfolio);
            let mut report = build_report(&result, &root.to_string_lossy());
            filter_suggestions(&mut report, &category, &min_level);
            let payload = serde_json::to_string_pretty(&report).unwrap();
            let dest = out.unwrap_or_else(|| root.join("dbt-audit-suggestions.json"));
            if stdout {
                println!("{payload}");
            } else if let Err(e) = std::fs::write(&dest, &payload) {
                eprintln!("cannot write {}: {e}", dest.display());
                return ExitCode::from(1);
            }
            if let Some(h) = html_out {
                let options = HtmlReportOptions {
                    include_models,
                    categories: category.iter().map(|value| value.to_uppercase()).collect(),
                    min_level: match level_rank(&min_level.to_lowercase()).min(2) {
                        0 => "error", 1 => "warning", _ => "information",
                    }.into(),
                };
                let html_report = build_html_report(&report, &portfolio, &options);
                if include_models {
                    eprintln!("The HTML report includes model text. Sharing this report shares that text.");
                }
                if let Err(e) = std::fs::write(&h, html::render(&html_report)) {
                    eprintln!("cannot write {}: {e}", h.display());
                    return ExitCode::from(1);
                }
            }
            if !quiet {
                print_summary(&report, (!stdout).then_some(dest.as_path()));
            }
            if fail_on_error && report["summary"]["counts"]["error"].as_u64().unwrap_or(0) > 0 {
                return ExitCode::from(1);
            }
            ExitCode::SUCCESS
        }
        Cmd::Lint { root, format, min_level, strict, ddl } => {
            if no_projects(&root) {
                eprintln!("No dbt_project.yml found under {}", root.display());
                return ExitCode::SUCCESS;
            }
            let mut portfolio = build_portfolio_with_ddl(&root, &ddl);
            let result = run_audit(&mut portfolio);
            let threshold = level_rank(&min_level.to_lowercase()).min(2);
            let active: Vec<_> = result.active().filter(|s| level_rank(&s.level).min(2) <= threshold).collect();
            let paths = LintPaths::new(&root);
            if format.eq_ignore_ascii_case("json") {
                let recs: Vec<Value> = active.iter().map(|s| lint_record(s, &paths)).collect();
                println!("{}", serde_json::to_string_pretty(&recs).unwrap());
            } else {
                for s in &active {
                    println!("{}", lint_line(s, &paths));
                }
            }
            if strict && active.iter().any(|s| s.level == level::ERROR) {
                return ExitCode::from(1);
            }
            ExitCode::SUCCESS
        }
        Cmd::Rules { format, code, simple: _ } => {
            if let Some(code) = code {
                let Some(m) = meta(&code) else {
                    eprintln!("unknown rule {code}");
                    return ExitCode::from(1);
                };
                println!("{}", serde_json::to_string_pretty(&serde_json::from_str::<Value>(m.json).unwrap()).unwrap());
                return ExitCode::SUCCESS;
            }
            match format.as_str() {
                "markdown" => print!("{}", catalog::markdown()),
                "json" => {
                    let list: Vec<Value> = catalog::sorted()
                        .iter()
                        .map(|m| json!({"code": m.code, "name": m.name, "short_description": m.short_description, "kind": m.kind, "level": m.level}))
                        .collect();
                    println!("{}", serde_json::to_string_pretty(&list).unwrap());
                }
                _ => {
                    eprintln!("{} registered rules", RULES.len());
                    eprintln!("{:<20} {:<36} {:<13} {:<12} Title", "ID", "Category", "Tier", "Level");
                    for m in catalog::sorted() {
                        eprintln!(
                            "{:<20} {:<36} {:<13} {:<12} {}",
                            m.code,
                            category_label(m.pack),
                            m.tier,
                            m.level,
                            m.name
                        );
                    }
                }
            }
            ExitCode::SUCCESS
        }
        Cmd::Validate { path, simple: _, strict } => {
            let path = match path.strip_prefix('$') {
                Some(var) => std::env::var(var).unwrap_or(path.clone()),
                None => path,
            };
            let target = PathBuf::from(path);
            let ext = target.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
            if !target.is_file() || !(ext == "sql" || ext == "py") {
                return ExitCode::SUCCESS;
            }
            let abs = std::fs::canonicalize(&target).unwrap_or(target.clone());
            let Some(project_root) = abs.ancestors().skip(1).find(|d| d.join("dbt_project.yml").is_file()) else {
                return ExitCode::SUCCESS;
            };
            let mut portfolio = build_portfolio(project_root);
            let result = run_single_file(&mut portfolio, &target);
            let active: Vec<_> = result.active().collect();
            if active.is_empty() {
                return ExitCode::SUCCESS;
            }
            eprintln!("{}", target.file_name().unwrap().to_string_lossy());
            for s in &active {
                eprintln!("{:<12} {:<20} {:>5}  {}", s.level, s.rule_id, s.line.map_or("-".into(), |l| l.to_string()), s.message);
            }
            if strict && active.iter().any(|s| s.level == level::ERROR) {
                return ExitCode::from(1);
            }
            ExitCode::SUCCESS
        }
        Cmd::SetupTasks { path } => match tasks::setup_tasks(&path) {
            Ok(msg) => {
                println!("{msg}");
                ExitCode::SUCCESS
            }
            Err(msg) => {
                eprintln!("{msg}");
                ExitCode::from(1)
            }
        },
        Cmd::Annotate { root, rule_ids, min_level, write, remove, allow_dirty } => {
            let opts = AnnotateOptions { rule_ids, min_level, dry_run: !write, remove, allow_dirty };
            match annotate(&root, &opts) {
                Ok(out) => {
                    print!("{}", out.diff);
                    eprintln!(
                        "{} marker(s) in {} file(s){}",
                        out.markers,
                        out.files_changed,
                        if opts.dry_run { " (dry run; pass --write to apply)" } else { "" }
                    );
                    ExitCode::SUCCESS
                }
                Err(e) => {
                    eprintln!("{e}");
                    ExitCode::from(1)
                }
            }
        }
        Cmd::FixColumns { root, ddl, select, write, allow_dirty, format } => {
            let opts = FixOptions { ddl, select, write, allow_dirty };
            match fix_columns(&root, &opts) {
                Ok(out) => {
                    if format.eq_ignore_ascii_case("json") {
                        println!("{}", serde_json::to_string_pretty(&out.files).unwrap());
                    } else {
                        print!("{}", out.diff);
                        for f in &out.files {
                            for w in &f.warnings {
                                eprintln!("{}: {w}", f.path);
                            }
                        }
                    }
                    let changed = out.files.iter().filter(|f| f.changed).count();
                    let edits: usize = out.files.iter().map(|f| f.edits.len()).sum();
                    eprintln!(
                        "{edits} column edit(s) in {changed} of {} matched model(s){}",
                        out.files.len(),
                        if write { "" } else { " (dry run; pass --write to apply)" }
                    );
                    ExitCode::SUCCESS
                }
                Err(e) => {
                    eprintln!("{e}");
                    ExitCode::from(1)
                }
            }
        }
        Cmd::Mcp => {
            mcp::serve();
            ExitCode::SUCCESS
        }
    }
}
