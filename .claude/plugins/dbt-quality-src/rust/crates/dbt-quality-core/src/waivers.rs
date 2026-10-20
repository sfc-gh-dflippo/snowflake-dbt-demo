//! User-authored waivers: exclude a rule for a file, a line, or a path glob.
//!
//! - `-- dbt-quality: ignore <ids>` on the reported line or the line above it
//! - `-- dbt-quality: ignore-file <ids>` anywhere in the file
//! - an `ignore:` entry in `.dbt-quality.yml`
//!
//! `*` in place of a rule list means every rule. A waived suggestion is dropped.

use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

use crate::discovery::{fnmatch, AuditConfig, ProjectContext};
use crate::model::Suggestion;
use crate::rx;
use crate::sqlutil::py_splitlines;

pub const ALL_RULES: &str = "*";

fn directive() -> &'static regex::Regex {
    rx!(r"(?i)dbt-quality[ \t]*:[ \t]*(ignore-file|ignore)[ \t]*[=:]?[ \t]*([A-Za-z0-9\-,* \t]*)")
}

#[derive(Debug, Clone, Default)]
pub struct FileWaivers {
    pub file_rules: BTreeSet<String>,
    pub line_rules: BTreeMap<u32, BTreeSet<String>>,
}

fn matches(rules: &BTreeSet<String>, rule_id: &str) -> bool {
    !rules.is_empty() && (rules.contains(ALL_RULES) || rules.contains(&rule_id.to_uppercase()))
}

impl FileWaivers {
    pub fn waives(&self, rule_id: &str, line: Option<u32>) -> bool {
        if matches(&self.file_rules, rule_id) {
            return true;
        }
        line.and_then(|l| self.line_rules.get(&l)).is_some_and(|r| matches(r, rule_id))
    }
}

fn parse_rule_list(raw: &str) -> BTreeSet<String> {
    rx!(r"[,\s]+").split(raw).map(|t| t.trim().to_uppercase()).filter(|t| !t.is_empty()).collect()
}

const COMMENT_OPENERS: &[&str] = &["--", "/*", "{#", "#"];

fn is_trailing(line: &str, pos: usize) -> bool {
    let before = &line[..pos];
    for op in COMMENT_OPENERS {
        let head = before.split(op).next().unwrap_or("");
        if before.contains(op) && head.trim().is_empty() {
            return false;
        }
    }
    !before.trim().is_empty()
}

pub fn parse_waivers(text: &str) -> FileWaivers {
    let mut w = FileWaivers::default();
    let lines = py_splitlines(text);
    for (i, line) in lines.iter().enumerate() {
        let Some(c) = directive().captures(line) else { continue };
        let rules = parse_rule_list(&c[2]);
        if rules.is_empty() {
            continue;
        }
        if c[1].eq_ignore_ascii_case("ignore-file") {
            w.file_rules.extend(rules);
            continue;
        }
        let mut targets = vec![i as u32 + 1];
        if !is_trailing(line, c.get(0).unwrap().start())
            && let Some(j) = (i + 1..lines.len()).find(|j| !lines[*j].trim().is_empty()) {
                targets.push(j as u32 + 1);
            }
        for t in targets {
            w.line_rules.entry(t).or_default().extend(rules.iter().cloned());
        }
    }
    w
}

/// Replace waiver directives with equal-length spaces, so a waiver naming a
/// rule id is not read as a conversion marker.
pub fn blank_directives(text: &str) -> String {
    directive().replace_all(text, |c: &regex::Captures| " ".repeat(c[0].len())).into_owned()
}

/// The path forms a waiver may name for one suggestion; project-relative first.
pub fn candidate_paths(s: &Suggestion, project: Option<&ProjectContext>) -> Vec<String> {
    if s.file.is_empty() {
        return vec![];
    }
    let raw = s.file.clone();
    let mut forms = vec![raw.clone()];
    if let Some(prefix) = project.map(|p| p.relative_root.as_str()).filter(|p| !p.is_empty() && *p != ".") {
        let pre = format!("{prefix}/");
        if let Some(rest) = raw.strip_prefix(&pre) {
            forms.insert(0, rest.to_string());
        } else {
            forms.push(format!("{prefix}/{raw}"));
        }
    }
    let mut seen = BTreeSet::new();
    forms.into_iter().filter(|f| !f.is_empty() && seen.insert(f.clone())).collect()
}

fn config_waives(config: Option<&AuditConfig>, rule_id: &str, paths: &[String]) -> bool {
    let Some(c) = config else { return false };
    c.ignores.iter().any(|e| matches(&e.rule_set(), rule_id) && e.paths.iter().any(|pat| paths.iter().any(|p| fnmatch(p, pat))))
}

pub fn file_waivers(project: &ProjectContext, relative: &str) -> FileWaivers {
    if let Some(w) = project.waiver_cache.borrow().get(relative) {
        return w.clone();
    }
    let path = project.root.join(relative);
    let w = if path.is_file() {
        std::fs::read(&path).map(|b| parse_waivers(&String::from_utf8_lossy(&b))).unwrap_or_default()
    } else {
        FileWaivers::default()
    };
    project.waiver_cache.borrow_mut().insert(relative.to_string(), w.clone());
    w
}

pub fn is_waived(s: &Suggestion, project: Option<&ProjectContext>, config: Option<&AuditConfig>) -> bool {
    let paths = candidate_paths(s, project);
    if config_waives(config, &s.rule_id, &paths) {
        return true;
    }
    let Some(project) = project else { return false };
    let Some(relative) = paths.first() else { return false };
    if Path::new(relative).is_absolute() {
        return false;
    }
    file_waivers(project, relative).waives(&s.rule_id, s.line)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn directive_forms() {
        let w = parse_waivers("-- dbt-quality: ignore SSC-EWI-DBTSQL0002\n\nselect 1  -- dbt-quality: ignore *\nx\n-- dbt-quality: ignore-file ssc-ewi-dbtdoc0002");
        assert!(w.waives("SSC-EWI-DBTSQL0002", Some(1)));
        assert!(w.waives("SSC-EWI-DBTSQL0002", Some(3)));
        assert!(w.waives("ANY", Some(3)));
        assert!(!w.waives("ANY", Some(4)));
        assert!(w.waives("SSC-EWI-DBTDOC0002", None));
    }

    #[test]
    fn blank_keeps_length() {
        let t = "x -- dbt-quality: ignore SSC-EWI-DBTSQL0002\ny";
        assert_eq!(blank_directives(t).len(), t.len());
        assert!(!blank_directives(t).contains("SSC"));
    }
}
