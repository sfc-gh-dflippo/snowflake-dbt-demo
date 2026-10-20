//! EWI marker injection.
//!
//! Markers use SnowConvert's line form:
//!
//! - SQL: `--** SSC-EWI-DBTINC0002 - <name>: <subject> **`
//! - YAML and Python: `# ** SSC-EWI-DBTINC0002 - <name>: <subject> **`
//!
//! The engine blanks owned markers before rules run, so the finding set does
//! not change when markers are present. Line numbers shift by the number of
//! marker lines above a finding. A write removes the owned markers in scope
//! and inserts the current set in one pass, so a second run changes nothing
//! and `remove` restores the original bytes. A run filtered by `rule_ids`
//! removes and inserts only the markers of those rules.
//!
//! Writes go only to regular files whose canonical path is inside the root.
//! The walker does not descend into symlinked directories.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};
use std::process::Command;

use serde::Serialize;

use crate::discovery::{build_portfolio, EXCLUDED_DIRS};
use crate::engine::run_audit;
use crate::model::{level_rank, meta, Suggestion};
use crate::report::LintPaths;
use crate::rx;

/// The dbt-quality code shape. SnowConvert's own `SSC-EWI-DBT0001` has no
/// three-letter pack and does not match.
pub fn owned_code() -> &'static regex::Regex {
    rx!(r"SSC-(?:EWI|FDM|PRF)-DBT[A-Z]{3}\d{4}")
}

/// The owned-marker line shape: prefix, then an owned code, then ` - `.
/// This is the only marker predicate; blanking and removal both use it.
fn owned_line() -> &'static regex::Regex {
    rx!(r"^[ \t]*(?:--\*\*|# \*\*) (SSC-(?:EWI|FDM|PRF)-DBT[A-Z]{3}\d{4}) - .*\*\*[ \t]*$")
}

/// The owned code of a marker line (BOM and line ending excluded), else `None`.
fn marker_code(line: &str) -> Option<&str> {
    owned_line().captures(line.trim_start_matches('\u{feff}').trim_end_matches(['\n', '\r'])).map(|c| c.get(1).unwrap().as_str())
}

fn is_marker_line(line: &str) -> bool {
    marker_code(line).is_some()
}

/// True for a line that holds only a converter marker: a comment or a
/// `!!!RESOLVE EWI!!!` block that carries a SnowConvert EWI or FDM code.
fn is_converter_marker_line(line: &str) -> bool {
    let body = line.trim_start_matches('\u{feff}').trim();
    let comment = ["--", "/*", "#", "!!!"].iter().any(|start| body.starts_with(start));
    comment && !is_marker_line(line)
        && (crate::provenance::ewi_pattern().is_match(body)
            || crate::provenance::fdm_pattern().is_match(body)
            || crate::provenance::resolve_ewi_pattern().is_match(body))
}

/// Replace owned marker lines with spaces, keeping offsets and newlines.
pub fn blank_owned_markers(text: &str) -> String {
    if !text.contains("-DBT") {
        return text.to_string();
    }
    text.split_inclusive('\n')
        .map(|line| {
            if is_marker_line(line) {
                line.chars().map(|ch| if matches!(ch, '\n' | '\r' | '\u{feff}') { ch } else { ' ' }).collect()
            } else {
                line.to_string()
            }
        })
        .collect()
}

#[derive(Debug, Clone)]
pub struct AnnotateOptions {
    pub rule_ids: Vec<String>,
    pub min_level: String,
    pub dry_run: bool,
    pub remove: bool,
    pub allow_dirty: bool,
}

impl Default for AnnotateOptions {
    fn default() -> Self {
        AnnotateOptions { rule_ids: vec![], min_level: "information".into(), dry_run: true, remove: false, allow_dirty: false }
    }
}

#[derive(Debug, Default, Serialize)]
pub struct AnnotateOutcome {
    pub diff: String,
    pub files_changed: usize,
    pub markers: usize,
    pub files: Vec<String>,
    pub written: bool,
}

#[derive(Clone, Copy, PartialEq)]
enum Syntax {
    Sql,
    Hash,
}

fn syntax_for(path: &Path) -> Option<Syntax> {
    match path.extension()?.to_str()?.to_lowercase().as_str() {
        "sql" => Some(Syntax::Sql),
        "yml" | "yaml" | "py" => Some(Syntax::Hash),
        _ => None,
    }
}

fn vendored(path: &Path, root: &Path) -> bool {
    path.strip_prefix(root)
        .unwrap_or(path)
        .components()
        .any(|c| matches!(c.as_os_str().to_str(), Some(n) if ["dbt_packages", "target", "logs"].contains(&n)))
}

/// The subject named by the rule's `marker_subject`, else the evidence, else the file stem.
fn subject(s: &Suggestion) -> String {
    let named = meta(&s.rule_id)
        .and_then(|m| m.marker_subject)
        .and_then(|k| s.context.get(k).map(crate::sqlutil::py_str).or_else(|| (k == "evidence").then(|| s.evidence.clone())));
    let raw = named.filter(|v| !v.trim().is_empty()).or_else(|| (!s.evidence.trim().is_empty()).then(|| s.evidence.clone())).unwrap_or_else(|| {
        Path::new(&s.file).file_stem().map(|f| f.to_string_lossy().to_string()).unwrap_or_default()
    });
    // A marker must never open or close a Jinja tag, or it would change how
    // the rest of the file tokenizes.
    let one = crate::sqlutil::collapse_ws(&raw)
        .replace("**", "*")
        .replace("{{", "{ {")
        .replace("}}", "} }")
        .replace("{%", "{ %")
        .replace("%}", "% }")
        .replace("{#", "{ #")
        .replace("#}", "# }");
    if one.chars().count() > 60 {
        format!("{}…", one.chars().take(59).collect::<String>().trim_end())
    } else {
        one
    }
}

fn marker_text(s: &Suggestion, syntax: Syntax, indent: &str) -> String {
    let name = meta(&s.rule_id).map_or(s.title.as_str(), |m| m.name);
    let subj = subject(s);
    let body = if subj.is_empty() { format!("{} - {name}", s.rule_id) } else { format!("{} - {name}: {subj}", s.rule_id) };
    match syntax {
        Syntax::Sql => format!("{indent}--** {body} **"),
        Syntax::Hash => format!("{indent}# ** {body} **"),
    }
}

/// Byte ranges occupied by Jinja tags, expressions, or comments.
fn jinja_tag_starts(text: &str) -> Vec<(usize, usize)> {
    use minijinja::machinery::{tokenize, Token, WhitespaceConfig};
    let mut ranges: Vec<(usize, usize)> = vec![];
    let mut data: Vec<(usize, usize)> = vec![];
    for t in tokenize(text, false, Default::default(), WhitespaceConfig::default()) {
        let Ok((tok, span)) = t else { return vec![] };
        if let Token::TemplateData(_) = tok {
            data.push((span.start_offset as usize, span.end_offset as usize));
        }
    }
    let mut pos = 0;
    for (a, b) in data {
        if a > pos {
            ranges.push((pos, a));
        }
        pos = b;
    }
    if pos < text.len() {
        ranges.push((pos, text.len()));
    }
    ranges
}

/// Remove owned markers accepted by `drop`, then add `inserts` above their targets.
/// The keys in `inserts` are 1-based line numbers in the current text.
/// Keep a UTF-8 BOM at the start of the file.
fn rewrite(text: &str, inserts: &BTreeMap<usize, Vec<String>>, eol: &str, drop: &dyn Fn(&str) -> bool) -> String {
    let (bom, text) = match text.strip_prefix('\u{feff}') {
        Some(rest) => ("\u{feff}", rest),
        None => ("", text),
    };
    let mut out = String::with_capacity(text.len() + inserts.len() * 80);
    out.push_str(bom);
    let mut pending: Vec<&String> = vec![];
    for (i, line) in text.split_inclusive('\n').enumerate() {
        if let Some(ms) = inserts.get(&(i + 1)) {
            pending.extend(ms.iter());
        }
        if marker_code(line).is_some_and(drop) {
            continue;
        }
        for m in pending.drain(..) {
            out.push_str(m);
            out.push_str(eol);
        }
        out.push_str(line);
    }
    for m in pending {
        if out.len() > bom.len() && !out.ends_with('\n') {
            out.push_str(eol);
        }
        out.push_str(m);
        out.push_str(eol);
    }
    out
}

/// Remove owned markers that `drop` accepts from a file that is not UTF-8.
/// Marker lines are ASCII, so each line is checked on its own bytes.
fn remove_markers_bytes(bytes: &[u8], drop: &dyn Fn(&str) -> bool) -> Vec<u8> {
    let mut out = Vec::with_capacity(bytes.len());
    for line in bytes.split_inclusive(|b| *b == b'\n') {
        if std::str::from_utf8(line).ok().and_then(marker_code).is_some_and(drop) {
            continue;
        }
        out.extend_from_slice(line);
    }
    out
}

fn line_starts(text: &str) -> Vec<usize> {
    std::iter::once(0).chain(text.match_indices('\n').map(|(i, _)| i + 1)).collect()
}

/// Plan the markers for one file's findings: (target line -> marker lines).
fn plan_file(text: &str, syntax: Syntax, yaml: bool, findings: &[&Suggestion]) -> BTreeMap<usize, Vec<String>> {
    let starts = line_starts(text);
    let lines: Vec<&str> = text.split('\n').collect();
    let tags = if syntax == Syntax::Sql { jinja_tag_starts(&blank_owned_markers(text)) } else { vec![] };
    let owners = if yaml { block_scalar_owners(&lines) } else { vec![] };
    let mut plan: BTreeMap<usize, Vec<String>> = BTreeMap::new();
    for s in findings {
        let mut line = (s.line.unwrap_or(1).max(1) as usize).min(lines.len().max(1));
        // A marker above a line that starts inside a Jinja tag would break the
        // template; move it to the line where the tag opens.
        if let Some(&off) = starts.get(line - 1)
            && let Some((a, _)) = tags.iter().find(|(a, b)| *a < off && off < *b) {
                line = starts.partition_point(|s| *s <= *a);
            }
        // A marker inside a YAML block scalar would become part of the value;
        // move it to the line of the key that owns the scalar.
        if let Some(Some(owner)) = owners.get(line - 1) {
            line = owner + 1;
        }
        // Skip past our markers and converter markers, so a new marker lands
        // above real content and never above another marker.
        while line < lines.len() && {
            let current = lines[line - 1].trim_end_matches('\r');
            is_marker_line(current) || is_converter_marker_line(current)
        } {
            line += 1;
        }
        let target = lines.get(line - 1).copied().unwrap_or("");
        let indent: String = target.chars().take_while(|c| *c == ' ' || *c == '\t').collect();
        let m = marker_text(s, syntax, &indent);
        let entry = plan.entry(line).or_default();
        if !entry.contains(&m) {
            entry.push(m);
        }
    }
    plan
}

/// For each 0-based line, the 0-based line of the key that owns the YAML
/// block scalar (`|` or `>`) the line is inside, else `None`.
fn block_scalar_owners(lines: &[&str]) -> Vec<Option<usize>> {
    let header = rx!(r"^[ \t]*(?:[^#\s].*:|-)[ \t]+[|>][-+0-9]*[ \t]*(?:#.*)?$");
    let indent = |l: &str| l.len() - l.trim_start_matches([' ', '\t']).len();
    let mut out = vec![None; lines.len()];
    let mut open: Option<(usize, usize)> = None;
    for (i, raw) in lines.iter().enumerate() {
        let l = raw.trim_end_matches('\r');
        if let Some((owner, ind)) = open {
            if l.trim().is_empty() || indent(l) > ind {
                out[i] = Some(owner);
                continue;
            }
            open = None;
        }
        if header.is_match(l) {
            open = Some((i, indent(l)));
        }
    }
    out
}

fn unified_diff(path: &str, old: &str, new: &str) -> String {
    similar::TextDiff::from_lines(old, new).unified_diff().context_radius(2).header(&format!("a/{path}"), &format!("b/{path}")).to_string()
}

/// The file names that `report` writes.
pub const REPORT_FILES: [&str; 2] = ["dbt-audit-suggestions.json", "dbt-audit-report.html"];

/// Rules whose finding is an existing converter marker (`!!!RESOLVE EWI!!!`,
/// `SSC-EWI-*`, `SSC-FDM-*`). `annotate` does not mark these findings.
pub const CONVERTER_MARKER_RULES: [&str; 3] = ["SSC-EWI-DBTMIG0001", "SSC-EWI-DBTMIG0002", "SSC-FDM-DBTMIG0003"];

/// Refuse to write when the git tree under `root` has uncommitted changes, or
/// when `root` is not in a git repository. The report files are ignored.
pub fn check_clean(root: &Path) -> Result<(), String> {
    check_one(root)?;
    // Nested repositories and submodules hold their own changes.
    for repo in nested_repos(root) {
        check_one(&repo)?;
    }
    Ok(())
}

/// Directories under `root` (not `root` itself) that hold a `.git` entry.
fn nested_repos(root: &Path) -> Vec<PathBuf> {
    let mut out = vec![];
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&d) else { continue };
        for e in rd.flatten() {
            let Ok(ft) = e.file_type() else { continue };
            let n = e.file_name();
            if !ft.is_dir() || ft.is_symlink() || n == ".git" {
                continue;
            }
            let p = e.path();
            if p.join(".git").exists() {
                out.push(p.clone());
            }
            stack.push(p);
        }
    }
    out.sort();
    out
}

fn check_one(root: &Path) -> Result<(), String> {
    let out = Command::new("git").arg("-C").arg(root).args(["status", "--porcelain", "--", "."]).output();
    match out {
        Ok(o) if o.status.success() => {
            // The report files may sit in the tree; they are not user changes.
            let dirty = String::from_utf8_lossy(&o.stdout)
                .lines()
                .filter(|l| l.len() > 3)
                .any(|l| !REPORT_FILES.iter().any(|f| Path::new(l[3..].trim_matches('"')).file_name().is_some_and(|n| n == *f)));
            if !dirty {
                Ok(())
            } else {
                Err(format!(
                    "refusing to write: {} has uncommitted changes. Commit or stash them, or pass allow_dirty.",
                    root.display()
                ))
            }
        }
        _ => Err(format!("refusing to write: {} is not in a git repository. Pass allow_dirty to write anyway.", root.display())),
    }
}

fn all_files(root: &Path) -> Vec<PathBuf> {
    let mut out = vec![];
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&d) else { continue };
        for e in rd.flatten() {
            let p = e.path();
            let n = e.file_name().to_string_lossy().to_string();
            let Ok(ft) = e.file_type() else { continue };
            if ft.is_symlink() && p.is_dir() {
                continue;
            }
            if ft.is_dir() {
                if !EXCLUDED_DIRS.contains(&n.as_str()) && !n.starts_with('.') {
                    stack.push(p);
                }
            } else if syntax_for(&p).is_some() {
                out.push(p);
            }
        }
    }
    out.sort();
    out
}

pub fn annotate(root: &Path, opts: &AnnotateOptions) -> Result<AnnotateOutcome, String> {
    let root = std::fs::canonicalize(root).map_err(|e| format!("{}: {e}", root.display()))?;
    if !opts.dry_run && !opts.allow_dirty {
        check_clean(&root)?;
    }
    // file -> findings targeting it
    let mut by_file: BTreeMap<PathBuf, Vec<Suggestion>> = BTreeMap::new();
    let wanted: Vec<String> = opts.rule_ids.iter().map(|r| r.to_uppercase()).collect();
    let drop = |code: &str| wanted.is_empty() || wanted.iter().any(|w| w == code);
    if !opts.remove {
        let mut portfolio = build_portfolio(&root);
        if portfolio.projects.is_empty() {
            return Err(format!("No dbt_project.yml found under {}", root.display()));
        }
        let result = run_audit(&mut portfolio);
        let paths = LintPaths::new(&root);
        let threshold = level_rank(&opts.min_level.to_lowercase()).min(2);
        for s in result.suggestions.into_iter().filter(|s| !s.suppressed) {
            if level_rank(&s.level).min(2) > threshold || (!wanted.is_empty() && !wanted.contains(&s.rule_id)) {
                continue;
            }
            if meta(&s.rule_id).is_some_and(|m| m.scope == "portfolio") {
                continue;
            }
            // These rules report a converter marker that is already in the file.
            // A second marker above it would duplicate the EWI, so the report
            // counts the finding and annotate writes nothing for it.
            if CONVERTER_MARKER_RULES.contains(&s.rule_id.as_str()) {
                continue;
            }
            let Some(abs) = paths.absolute(&s) else { continue };
            if syntax_for(&abs).is_none() || vendored(&abs, &root) {
                continue;
            }
            by_file.entry(abs).or_default().push(s);
        }
    }
    let mut out = AnnotateOutcome::default();
    for path in all_files(&root) {
        // Never write through a link to a file outside the root.
        if !std::fs::canonicalize(&path).is_ok_and(|c| c.starts_with(&root)) {
            continue;
        }
        let Ok(bytes) = std::fs::read(&path) else { continue };
        let text = match String::from_utf8(bytes) {
            Ok(t) => t,
            Err(e) => {
                // Not UTF-8: remove owned markers only, byte for byte.
                let old = e.into_bytes();
                let new = remove_markers_bytes(&old, &drop);
                if new != old {
                    let rel = crate::discovery::display_path(path.strip_prefix(&root).unwrap_or(&path));
                    out.files_changed += 1;
                    out.diff.push_str(&unified_diff(&rel, &String::from_utf8_lossy(&old), &String::from_utf8_lossy(&new)));
                    out.files.push(rel);
                    if !opts.dry_run {
                        std::fs::write(&path, new).map_err(|e| format!("{}: {e}", path.display()))?;
                    }
                }
                continue;
            }
        };
        let findings: Vec<&Suggestion> = by_file.get(&path).map(|v| v.iter().collect()).unwrap_or_default();
        if findings.is_empty() && !text.split_inclusive('\n').any(is_marker_line) {
            continue;
        }
        let syntax = syntax_for(&path).unwrap();
        let yaml = path.extension().is_some_and(|e| e != "py");
        let eol = if text.contains("\r\n") { "\r\n" } else { "\n" };
        let plan = plan_file(&text, syntax, yaml && syntax == Syntax::Hash, &findings);
        let new = rewrite(&text, &plan, eol, &drop);
        if new == text {
            continue;
        }
        let rel = crate::discovery::display_path(path.strip_prefix(&root).unwrap_or(&path));
        out.markers += plan.values().map(Vec::len).sum::<usize>();
        out.files_changed += 1;
        out.diff.push_str(&unified_diff(&rel, &text, &new));
        out.files.push(rel);
        if !opts.dry_run {
            std::fs::write(&path, new).map_err(|e| format!("{}: {e}", path.display()))?;
        }
    }
    out.written = !opts.dry_run && out.files_changed > 0;
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn owned_markers_round_trip() {
        let original = "{{ config(\n  pre_hook=\"x\"\n) }}\nselect 1\n";
        let mut plan = BTreeMap::new();
        plan.insert(1, vec!["--** SSC-EWI-DBTINC0002 - Delete-and-load: this **".to_string()]);
        let all = |_: &str| true;
        let marked = rewrite(original, &plan, "\n", &all);
        assert!(marked.starts_with("--** SSC-EWI-DBTINC0002"));
        assert_eq!(rewrite(&marked, &plan, "\n", &all), marked, "second run changes nothing");
        assert_eq!(rewrite(&marked, &BTreeMap::new(), "\n", &all), original, "remove restores the bytes");
        assert_eq!(blank_owned_markers(&marked).len(), marked.len());
    }

    #[test]
    fn subjects_never_carry_jinja_delimiters() {
        let s = Suggestion::new("SSC-EWI-DBTSQL0007", "m").evidence("from {{ source('a','b') }} c, {{");
        let m = marker_text(&s, Syntax::Sql, "");
        assert!(!m.contains("{{") && !m.contains("}}"), "{m}");
    }

    #[test]
    fn snowconvert_codes_are_not_owned() {
        assert!(!owned_code().is_match("SSC-EWI-DBT0001"));
        assert!(owned_code().is_match("SSC-PRF-DBTINC0017"));
        assert!(!is_marker_line("--** SSC-EWI-SSIS0001 - x **"));
    }

    #[test]
    fn marker_inside_jinja_moves_to_tag_start() {
        let text = "{{ config(\n  pre_hook=\"delete\"\n) }}\nselect 1\n";
        let tags = jinja_tag_starts(text);
        assert!(!tags.is_empty());
        let starts = line_starts(text);
        let off = starts[1];
        assert!(tags.iter().any(|(a, b)| *a < off && off < *b));
    }

    #[test]
    fn markers_skip_yaml_block_scalars() {
        let lines = ["models:", "  - name: a", "    config:", "      pre_hook: |", "        delete from x", "", "        where 1=1", "    columns: []"];
        let owners = block_scalar_owners(&lines);
        assert_eq!(owners[4], Some(3));
        assert_eq!(owners[6], Some(3));
        assert_eq!(owners[7], None);
        assert_eq!(owners[3], None);
    }

    #[test]
    fn one_predicate_for_blank_and_remove() {
        let user = "--** note: see SSC-EWI-DBTINC0002 **\nselect 1\n";
        assert_eq!(blank_owned_markers(user), user, "a user comment is not blanked");
        assert_eq!(rewrite(user, &BTreeMap::new(), "\n", &|_| true), user, "and not removed");
    }

    #[test]
    fn rule_filter_keeps_other_markers() {
        let text = "--** SSC-EWI-DBTSQL0007 - a: b **\n--** SSC-EWI-DBTINC0002 - c: d **\nselect 1\n";
        let only = |c: &str| c == "SSC-EWI-DBTSQL0007";
        assert_eq!(rewrite(text, &BTreeMap::new(), "\n", &only), "--** SSC-EWI-DBTINC0002 - c: d **\nselect 1\n");
    }

    #[cfg(unix)]
    fn git(root: &Path, args: &[&str]) {
        let ok = Command::new("git")
            .arg("-C")
            .arg(root)
            .args(["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"])
            .args(args)
            .output()
            .unwrap()
            .status
            .success();
        assert!(ok, "git {args:?}");
    }

    #[cfg(unix)]
    fn commit(root: &Path) {
        git(root, &["add", "-A"]);
        git(root, &["commit", "-q", "--allow-empty", "-m", "x"]);
    }

    #[test]
    fn remove_handles_non_utf8_files() {
        let t = crate::testing::TempProject::new(&[("models/a.sql", "select 1\n")]);
        let root = std::fs::canonicalize(t.path()).unwrap();
        let body: &[u8] = b"select '\xff\xfe' as x\n";
        let mut marked = b"--** SSC-EWI-DBTSQL0007 - Implicit join: a **\n".to_vec();
        marked.extend_from_slice(body);
        std::fs::write(root.join("models/l1.sql"), &marked).unwrap();
        std::fs::write(root.join("models/clean.sql"), body).unwrap();
        let o = annotate(&root, &AnnotateOptions { remove: true, dry_run: false, allow_dirty: true, ..Default::default() }).unwrap();
        assert_eq!(o.files, ["models/l1.sql"]);
        assert_eq!(std::fs::read(root.join("models/l1.sql")).unwrap(), body);
        assert_eq!(std::fs::read(root.join("models/clean.sql")).unwrap(), body);
    }

    #[cfg(unix)]
    #[test]
    fn check_clean_sees_nested_repos() {
        let t = crate::testing::TempProject::new(&[("models/a.sql", "select 1\n"), ("vendor/x/f.sql", "select 1\n")]);
        let root = std::fs::canonicalize(t.path()).unwrap();
        let nested = root.join("vendor/x");
        git(&nested, &["init", "-q"]);
        commit(&nested);
        git(&root, &["init", "-q"]);
        std::fs::write(root.join(".gitignore"), "vendor/\n").unwrap();
        commit(&root);
        assert!(check_clean(&root).is_ok());
        std::fs::write(nested.join("f.sql"), "select 2\n").unwrap();
        let e = check_clean(&root).unwrap_err();
        assert!(e.contains("vendor/x"), "{e}");
    }

    #[cfg(unix)]
    fn finding_set(t: &crate::testing::TempProject) -> Vec<(String, String)> {
        let mut v: Vec<(String, String)> = t.audit().into_iter().map(|s| (s.rule_id, s.file)).collect();
        v.sort();
        v
    }

    #[cfg(unix)]
    #[test]
    fn annotate_end_to_end() {
        use crate::testing::TempProject;
        let read = |p: &Path| std::fs::read(p).unwrap();
        let bad = "select a.x\nfrom a, b\nwhere a.id = b.id\n";
        let t = TempProject::new(&[
            ("models/a.sql", bad),
            ("models/b.sql", &bad.replace('\n', "\r\n")),
            ("models/c.sql", "\u{feff}select * from a, b\n"),
        ]);
        let root = std::fs::canonicalize(t.path()).unwrap();
        let outside = TempProject::new(&[("x.sql", bad)]);
        std::os::unix::fs::symlink(outside.path().join("x.sql"), root.join("models/ext.sql")).unwrap();
        std::os::unix::fs::symlink(outside.path(), root.join("models/extdir")).unwrap();
        std::os::unix::fs::symlink(root.join("models"), root.join("models/loop")).unwrap();
        git(&root, &["init", "-q"]);
        commit(&root);
        let files = ["models/a.sql", "models/b.sql", "models/c.sql"];
        let original: Vec<Vec<u8>> = files.iter().map(|f| read(&root.join(f))).collect();
        let outside_bytes = read(&outside.path().join("x.sql"));
        let before = finding_set(&t);
        assert!(before.iter().filter(|(r, _)| r == "SSC-EWI-DBTSQL0007").count() >= 3, "{before:?}");
        let write = AnnotateOptions { dry_run: false, ..Default::default() };

        // Refuse writes when the tree has changes, but ignore generated report files.
        t.write("models/new.sql", "select 1\n");
        assert!(annotate(&root, &write).is_err());
        std::fs::remove_file(root.join("models/new.sql")).unwrap();
        t.write("dbt-audit-suggestions.json", "{}");
        t.write("dbt-audit-report.html", "");

        // A dry run writes nothing.
        let dry = annotate(&root, &AnnotateOptions::default()).unwrap();
        assert!(dry.files_changed >= 3 && !dry.written);
        assert_eq!(files.iter().map(|f| read(&root.join(f))).collect::<Vec<_>>(), original);

        let w = annotate(&root, &write).unwrap();
        assert!(w.written);
        assert!(!w.files.iter().any(|f| f.contains("ext")), "{:?}", w.files);
        assert_eq!(read(&outside.path().join("x.sql")), outside_bytes, "no write outside the root");
        let b = String::from_utf8(read(&root.join("models/b.sql"))).unwrap();
        assert!(b.contains("--** SSC-EWI-DBTSQL0007") && b.replace("\r\n", "").find('\n').is_none(), "CRLF kept: {b:?}");
        let c = String::from_utf8(read(&root.join("models/c.sql"))).unwrap();
        assert!(c.starts_with("\u{feff}--** SSC-") && c.contains("--** SSC-EWI-DBTSQL0007"), "BOM kept first: {c:?}");

        // A second run changes nothing, and the finding set is unchanged.
        commit(&root);
        let marked: Vec<Vec<u8>> = files.iter().map(|f| read(&root.join(f))).collect();
        let again = annotate(&root, &write).unwrap();
        assert_eq!(again.files_changed, 0, "{}", again.diff);
        assert_eq!(files.iter().map(|f| read(&root.join(f))).collect::<Vec<_>>(), marked);
        assert_eq!(finding_set(&t), before);

        // Remove restores the original bytes.
        annotate(&root, &AnnotateOptions { remove: true, ..write }).unwrap();
        assert_eq!(files.iter().map(|f| read(&root.join(f))).collect::<Vec<_>>(), original);
    }

    #[test]
    fn converter_markers_are_counted_but_not_marked_again() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/ewi_estate");
        let mut portfolio = build_portfolio(&root);
        let found: Vec<String> = run_audit(&mut portfolio).suggestions.into_iter().map(|s| s.rule_id).collect();
        for code in CONVERTER_MARKER_RULES {
            assert!(found.iter().any(|f| f == code), "fixture must report {code}");
        }
        let dry = annotate(&root, &AnnotateOptions::default()).unwrap();
        assert!(!dry.written && dry.markers > 0);
        for code in CONVERTER_MARKER_RULES {
            assert!(!dry.diff.lines().any(|l| l.starts_with('+') && l.contains(code)), "{code} marker added:\n{}", dry.diff);
        }
        // Other migration findings still get a marker.
        assert!(dry.diff.lines().any(|l| l.starts_with('+') && l.contains("SSC-EWI-DBTMIG0004")), "{}", dry.diff);
        // No added marker sits directly above another marker line.
        let lines: Vec<&str> = dry.diff.lines().collect();
        for (i, line) in lines.iter().enumerate() {
            let Some(added) = line.strip_prefix('+') else { continue };
            if line.starts_with("+++") || !is_marker_line(added) { continue; }
            let next = lines[i + 1..].iter().find(|l| !l.starts_with('+') || !is_marker_line(&l[1..]));
            if let Some(next) = next.and_then(|l| l.strip_prefix(' ')) {
                assert!(!is_converter_marker_line(next), "marker above a converter marker:\n{added}\n{next}");
            }
        }
    }

    #[test]
    fn new_markers_go_below_converter_markers() {
        let text = "--** SSC-FDM-TS0001 - COLLATION NOT SUPPORTED **\n-- SSC-EWI-0073 - review\nselect a.x from a, b\n";
        let mut s = Suggestion::new("SSC-EWI-DBTSQL0007", "x");
        s.line = Some(1);
        let plan = plan_file(text, Syntax::Sql, false, &[&s]);
        assert_eq!(plan.keys().copied().collect::<Vec<_>>(), [3], "marker goes above the code line");
        assert!(is_converter_marker_line("  !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - x ***/!!!"));
        assert!(!is_converter_marker_line("select 1 -- SSC-EWI-0073 - inline"));
        assert!(!is_converter_marker_line("--** SSC-EWI-DBTSQL0007 - ours: x **"));
    }
}
