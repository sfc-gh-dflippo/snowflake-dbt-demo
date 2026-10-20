//! The audit runner: dispatches detectors by scope, resolves anchors, applies
//! waivers and migration-tier suppression, and records skipped rules.

use std::panic::{catch_unwind, AssertUnwindSafe};
use std::path::Path;

use serde_json::{json, Value};

use crate::anchors::resolve_position;
use crate::discovery::{AuditConfig, ModelFile, PortfolioContext, ProjectContext};
use crate::model::{level_rank, tier, RuleMeta, Suggestion, RULES};
use crate::provenance::classify;
use crate::waivers::is_waived;

pub type ModelFn = fn(&ModelFile, &ProjectContext) -> Vec<Suggestion>;
pub type ProjectFn = fn(&ProjectContext) -> Vec<Suggestion>;
pub type PortfolioFn = fn(&PortfolioContext) -> Vec<Suggestion>;

#[derive(Clone, Copy)]
pub enum Detect {
    Model(ModelFn),
    Project(ProjectFn),
    Portfolio(PortfolioFn),
}

impl Detect {
    pub fn scope(&self) -> &'static str {
        match self {
            Detect::Model(_) => "model",
            Detect::Project(_) => "project",
            Detect::Portfolio(_) => "portfolio",
        }
    }
}

/// A rule implementation: its code and the function that detects it. All
/// other metadata lives in `rules/<PACK>.json`.
#[derive(Clone, Copy)]
pub struct Detector {
    pub code: &'static str,
    pub detect: Detect,
}

#[derive(Debug, Clone)]
pub struct SkippedRule {
    pub rule_id: String,
    pub title: String,
    pub reason: String,
}

#[derive(Debug, Default)]
pub struct AuditResult {
    pub suggestions: Vec<Suggestion>,
    pub skipped: Vec<SkippedRule>,
    pub projects: Vec<Value>,
    pub errors: Vec<String>,
}

impl AuditResult {
    pub fn active(&self) -> impl Iterator<Item = &Suggestion> {
        self.suggestions.iter().filter(|s| !s.suppressed)
    }
}

pub fn detector(code: &str) -> Option<&'static Detector> {
    crate::rules::DETECTORS.iter().find(|d| d.code == code)
}

fn project_info(p: &ProjectContext) -> Value {
    json!({
        "name": p.name,
        "label": p.label,
        "path": p.relative_root,
        "model_count": p.model_count(),
        "macro_count": p.macros.iter().map(|m| m.macros.len()).sum::<usize>(),
        "provenance": {
            "is_migration": p.provenance.is_migration,
            "confidence": p.provenance.confidence,
            "source_platform": p.provenance.source_platform,
            "signals": p.provenance.signals,
        },
    })
}

fn sorted_rules() -> Vec<&'static RuleMeta> {
    let mut r: Vec<&RuleMeta> = RULES.iter().filter(|r| r.status == "active").collect();
    r.sort_by_key(|r| r.code);
    r
}

fn run<F: FnOnce() -> Vec<Suggestion>>(f: F) -> Result<Vec<Suggestion>, String> {
    catch_unwind(AssertUnwindSafe(f)).map_err(|e| {
        e.downcast_ref::<String>().cloned().or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string())).unwrap_or_else(|| "panic".into())
    })
}

pub fn run_audit(portfolio: &mut PortfolioContext) -> AuditResult {
    let mut result = AuditResult::default();
    for p in &mut portfolio.projects {
        p.provenance = classify(p);
        result.errors.extend(p.read_errors.iter().cloned());
        result.projects.push(project_info(p));
    }
    let portfolio = &*portfolio;
    let config = &portfolio.config;
    for meta in sorted_rules() {
        if config.disabled_rules.iter().any(|d| d == meta.code) {
            result.skipped.push(skip(meta, "disabled in .dbt-quality.yml"));
            continue;
        }
        let Some(d) = detector(meta.code) else { continue };
        match d.detect {
            Detect::Portfolio(f) => collect(&mut result, meta, run(|| f(portfolio)), None, config),
            Detect::Project(_) | Detect::Model(_) => {
                for p in &portfolio.projects {
                    match d.detect {
                        Detect::Project(f) => collect(&mut result, meta, run(|| f(p)), Some(p), config),
                        Detect::Model(f) => {
                            for m in &p.models {
                                collect(&mut result, meta, run(|| f(m, p)), Some(p), config);
                            }
                        }
                        Detect::Portfolio(_) => unreachable!(),
                    }
                }
            }
        }
    }
    crate::rules::prj::relations::enforce_ownership(&mut result.suggestions, portfolio);
    finish(&mut result, portfolio);
    result
}

/// Run only the model-scoped rules for one file. Other scopes are reported
/// as skipped, not passed.
pub fn run_single_file(portfolio: &mut PortfolioContext, target: &Path) -> AuditResult {
    let mut result = AuditResult::default();
    let resolved = std::fs::canonicalize(target).unwrap_or_else(|_| target.to_path_buf());
    let mut located = None;
    for (pi, p) in portfolio.projects.iter_mut().enumerate() {
        p.provenance = classify(p);
        if let Some(mi) = p.models.iter().position(|m| std::fs::canonicalize(&m.path).is_ok_and(|c| c == resolved)) {
            located = Some((pi, mi));
            break;
        }
    }
    let Some((pi, mi)) = located else { return result };
    let p = &portfolio.projects[pi];
    let m = &p.models[mi];
    result.projects.push(project_info(p));
    let config = &portfolio.config;
    for meta in sorted_rules() {
        if config.disabled_rules.iter().any(|d| d == meta.code) {
            result.skipped.push(skip(meta, "disabled in .dbt-quality.yml"));
            continue;
        }
        let Some(d) = detector(meta.code) else { continue };
        let Detect::Model(f) = d.detect else {
            result.skipped.push(skip(meta, &format!("{}-scoped: needs the whole project, run `dbt-audit`", d.detect.scope())));
            continue;
        };
        collect(&mut result, meta, run(|| f(m, p)), Some(p), config);
    }
    finish(&mut result, portfolio);
    result
}

#[cfg(test)]
thread_local! {
    /// Number of exact duplicates removed by `finish`. Tests detect duplicate findings with this count.
    static DROPPED: std::cell::Cell<usize> = const { std::cell::Cell::new(0) };
}

/// Make file paths root-relative, drop exact duplicates and sort.
fn finish(result: &mut AuditResult, portfolio: &PortfolioContext) {
    for s in &mut result.suggestions {
        if let Some(p) = portfolio.projects.iter().find(|p| !s.project_path.is_empty() && p.relative_root == s.project_path) {
            s.file = crate::discovery::root_relative(p, &s.file);
        }
    }
    let mut seen = std::collections::HashSet::new();
    let before = result.suggestions.len();
    result.suggestions.retain(|s| {
        seen.insert((s.rule_id.clone(), s.project.clone(), s.file.clone(), s.line, s.message.clone()))
    });
    #[cfg(test)]
    DROPPED.with(|d| d.set(d.get() + before - result.suggestions.len()));
    #[cfg(not(test))]
    let _ = before;
    result.suggestions.sort_by(sort_key);
}

fn skip(meta: &RuleMeta, reason: &str) -> SkippedRule {
    SkippedRule { rule_id: meta.code.into(), title: meta.name.into(), reason: reason.into() }
}

fn collect(
    result: &mut AuditResult,
    meta: &RuleMeta,
    produced: Result<Vec<Suggestion>, String>,
    project: Option<&ProjectContext>,
    config: &AuditConfig,
) {
    let produced = match produced {
        Ok(p) => p,
        Err(e) => {
            result.errors.push(format!("rule {} failed: {e}", meta.code));
            result.skipped.push(skip(meta, &format!("rule error: {e}")));
            return;
        }
    };
    for mut s in produced {
        if let Some(p) = project
            && s.project.is_empty() {
                s.project = p.name.clone();
            }
        let (line, column) = resolve_position(&s, project);
        s.line = Some(line);
        s.column = column;
        if is_waived(&s, project, Some(config)) {
            continue;
        }
        apply_suppression(&mut s, project);
        if let Some(p) = project
            && s.project_path.is_empty() {
                if s.project == p.name {
                    s.project = p.label.clone();
                }
                s.project_path = p.relative_root.clone();
            }
        result.suggestions.push(s);
    }
}

fn apply_suppression(s: &mut Suggestion, project: Option<&ProjectContext>) {
    if s.tier != tier::ARCHITECTURE {
        return;
    }
    let Some(p) = project else { return };
    let v = &p.provenance;
    if !v.is_migration {
        return;
    }
    if v.covers(&s.file) || s.file.is_empty() {
        s.suppressed = true;
        s.suppressed_reason = v.suppression_reason();
    }
}

fn sort_key(a: &Suggestion, b: &Suggestion) -> std::cmp::Ordering {
    (level_rank(&a.level), &a.category, &a.rule_id, &a.project, &a.file, a.line.unwrap_or(0)).cmp(&(
        level_rank(&b.level),
        &b.category,
        &b.rule_id,
        &b.project,
        &b.file,
        b.line.unwrap_or(0),
    ))
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use crate::discovery::build_portfolio;
    use crate::model::Suggestion;
    use crate::testing::TempProject;

    use super::*;

    fn key(s: &Suggestion) -> (String, String, String, Option<u32>, String) {
        (s.rule_id.clone(), s.project.clone(), s.file.clone(), s.line, s.message.clone())
    }

    #[test]
    fn colliding_names_get_path_labels_and_root_relative_files() {
        let y = "name: same\nversion: '1.0'\nprofile: p\nvars:\n  k: 1\n";
        let t = TempProject::new(&[("a/dbt_project.yml", y), ("b/dbt_project.yml", y), ("a/models/x.sql", "select 1"), ("b/models/y.sql", "select 1")]);
        let f = t.findings("SSC-EWI-DBTPRJ0017");
        let got: Vec<(&str, &str)> = f.iter().map(|s| (s.project.as_str(), s.file.as_str())).collect();
        assert_eq!(got, [("same (a)", "a/dbt_project.yml"), ("same (b)", "b/dbt_project.yml")]);
        // Unique names keep the bare name; a root project keeps its plain paths.
        let t = TempProject::new(&[("models/x.sql", "select 1"), ("dbt_project.yml", y)]);
        assert!(t.findings("SSC-EWI-DBTPRJ0017").iter().all(|s| s.project == "same" && s.file == "dbt_project.yml"));
    }

    #[test]
    fn finish_drops_exact_duplicates() {
        let t = TempProject::new(&[("models/x.sql", "select 1")]);
        let p = build_portfolio(t.path());
        let s = Suggestion::new("SSC-EWI-DBTPRJ0017", "m").file("dbt_project.yml").line(3);
        let mut r = AuditResult { suggestions: vec![s.clone(), s.clone(), s.line(4)], ..Default::default() };
        finish(&mut r, &p);
        assert_eq!(r.suggestions.len(), 2);
    }

    /// Rule pairs whose advice contradicts or repeats each other for one defect.
    /// One rule owns each defect, so the pair must never share a (project, file,
    /// line) with a common subject. Every rule here fires on an estate fixture.
    const CONFLICTS: &[(&str, &str)] = &[
        ("PRJ0014", "PRJ0017"),
        ("PRJ0009", "INC0019"),
        ("MAC0010", "PRJ0009"),
        ("MAC0010", "INC0019"),
        ("SQL0006", "PRJ0021"),
        ("PRJ0009", "PRJ0021"),
        ("SQL0006", "PRJ0022"),
        ("PRJ0021", "PRJ0022"),
    ];
    const SYNTHETIC_ONLY: &[(&str, &str)] = &[("PRJ0016", "PRJ0021")];

    /// Rule pairs that must not both report one model, at any line. TST0002
    /// owns "no key test"; TST0012 reports key columns only when a key exists.
    /// TST0004 owns untested key columns on a fact model, so TST0012 skips facts.
    const MODEL_CONFLICTS: &[(&str, &str)] = &[("TST0002", "TST0012"), ("TST0004", "TST0012")];

    /// The vars a finding is about. Empty means the location alone is the subject.
    fn subject(s: &Suggestion) -> HashSet<String> {
        let mut out: HashSet<String> = HashSet::new();
        for k in ["vars", "session_vars"] {
            if let Some(a) = s.context.get(k).and_then(|v| v.as_array()) {
                out.extend(a.iter().filter_map(|v| v.as_str()).map(String::from));
            }
        }
        out
    }

    /// Every (pair, location) where both rules of a CONFLICTS pair report one subject.
    fn clashes(all: &[Suggestion]) -> Vec<String> {
        let mut out = vec![];
        for (a, b) in CONFLICTS.iter().chain(SYNTHETIC_ONLY) {
            for x in all.iter().filter(|s| s.rule_id.ends_with(a)) {
                for y in all.iter().filter(|s| s.rule_id.ends_with(b)) {
                    let (sx, sy) = (subject(x), subject(y));
                    let same_subject = sx.is_empty() || sy.is_empty() || !sx.is_disjoint(&sy);
                    if (&x.project, &x.file, x.line) == (&y.project, &y.file, y.line) && same_subject {
                        out.push(format!("{a}/{b} at {}:{:?}", x.file, x.line));
                    }
                }
            }
        }
        for (a, b) in MODEL_CONFLICTS {
            for x in all.iter().filter(|s| s.rule_id.ends_with(a)) {
                for y in all.iter().filter(|s| s.rule_id.ends_with(b)) {
                    if let Some(m) = x.context.get("model")
                        && (&x.project, &x.file) == (&y.project, &y.file)
                        && Some(m) == y.context.get("model")
                    {
                        out.push(format!("{a}/{b} on model {m} in {}", x.file));
                    }
                }
            }
        }
        out
    }

    /// Rules where one file may repeat a remediation: each finding is its own edit.
    fn per_line(rule_id: &str) -> bool {
        crate::model::meta(rule_id).is_some_and(|m| m.per_line)
    }

    /// Findings that share (rule, file, remediation) with an earlier one, outside per-line rules.
    fn semantic_dups(all: &[Suggestion]) -> Vec<String> {
        let mut seen = HashSet::new();
        all.iter()
            .filter(|s| !s.suppressed && !per_line(&s.rule_id))
            .filter(|s| !seen.insert((s.rule_id.clone(), s.file.clone(), s.remediation.clone())))
            .map(|s| format!("{} {}:{:?}", s.rule_id, s.file, s.line))
            .collect()
    }

    fn check_estate(rel: &str, projects: usize) -> AuditResult {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures").join(rel);
        let mut p = build_portfolio(&root);
        assert_eq!(p.projects.len(), projects);
        DROPPED.with(|d| d.set(0));
        let r = run_audit(&mut p);
        assert_eq!(DROPPED.with(|d| d.get()), 0, "a detector emitted an exact duplicate in {rel}");
        let mut seen = HashSet::new();
        let dups: Vec<_> = r.suggestions.iter().map(key).filter(|k| !seen.insert(k.clone())).collect();
        assert!(dups.is_empty(), "duplicate findings: {dups:?}");
        let c = clashes(&r.suggestions);
        assert!(c.is_empty(), "conflicting advice in {rel}: {c:?}");
        let d = semantic_dups(&r.suggestions);
        assert!(d.is_empty(), "same rule, file and remediation repeat in {rel} (declare `per_line` if intended): {d:?}");
        r
    }

    #[test]
    fn conflict_guard_catches_each_pair() {
        for (a, b) in CONFLICTS.iter().chain(SYNTHETIC_ONLY) {
            let x = Suggestion::new(&format!("SSC-EWI-DBT{a}"), "x").file("m.sql").line(3);
            let y = Suggestion::new(&format!("SSC-EWI-DBT{b}"), "y").file("m.sql").line(3);
            assert_eq!(clashes(&[x.clone(), y.clone()]).len(), 1, "{a}/{b} not caught");
            assert!(clashes(&[x, y.line(4)]).is_empty());
        }
        for (a, b) in MODEL_CONFLICTS {
            let m = |c: &str, l: u32, model: &str| Suggestion::new(&format!("SSC-EWI-DBT{c}"), "x").file("_models.yml").line(l).ctx("model", json!(model));
            assert_eq!(clashes(&[m(a, 4, "orders"), m(b, 7, "orders")]).len(), 1, "{a}/{b} not caught");
            assert!(clashes(&[m(a, 4, "orders"), m(b, 7, "customers")]).is_empty());
        }
        // Var rollups clash only on a shared var.
        let v = |c: &str, k: &str| Suggestion::new(c, "v").file("dbt_project.yml").line(5).ctx("vars", json!([k]));
        assert!(clashes(&[v("SSC-EWI-DBTPRJ0014", "a"), v("SSC-EWI-DBTPRJ0017", "b")]).is_empty());
        assert_eq!(clashes(&[v("SSC-EWI-DBTPRJ0014", "a"), v("SSC-EWI-DBTPRJ0017", "a")]).len(), 1);
        let d = Suggestion::new("SSC-EWI-DBTPRJ0017", "m").file("dbt_project.yml").line(3).remediation("r");
        assert_eq!(semantic_dups(&[d.clone(), d.line(9)]).len(), 1);
    }

    #[test]
    fn synthetic_relation_conflicts_are_nonvacuous() {
        assert!(!std::hint::black_box(SYNTHETIC_ONLY).is_empty());
        let t = TempProject::new(&[("macros/naming.sql","{% macro generate_schema_name(custom_schema_name, node) %}{{ custom_schema_name }}{% endmacro %}"),("models/r.sql","{{ config(schema=var('schema','S')) }} select * from {{ var('missing') }}.S.T\nselect {{ var('value') }} as value\nselect * from DB.S.EXTERNAL"),("models/p.sql","{{ config(schema=var('s','S')) }} select 1"),("models/cycle.sql","{{ config(database='DB',schema='S',alias='C') }} select * from DB.S.C")]);
        let mut pf = build_portfolio(t.path());
        let r = run_audit(&mut pf);
        assert!(clashes(&r.suggestions).is_empty(),"{:?}",clashes(&r.suggestions));
        for (a,b) in SYNTHETIC_ONLY.iter().chain(&[("PRJ0009","PRJ0021"),("SQL0006","PRJ0021"),("SQL0006","PRJ0022"),("PRJ0021","PRJ0022")]) {
            assert!(r.suggestions.iter().any(|s| s.rule_id.ends_with(a)),"{a}");
            assert!(r.suggestions.iter().any(|s| s.rule_id.ends_with(b)),"{b}");
        }
    }

    #[test]
    fn conflict_rules_fire_on_fixtures() {
        let mut fired: HashSet<String> = HashSet::new();
        for (rel, n) in [("cisco_estate", 4), ("snowconvert/Informatica", 20), ("ewi_estate", 0)] {
            let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures").join(rel);
            let mut p = build_portfolio(&root);
            if n > 0 {
                assert_eq!(p.projects.len(), n);
            }
            fired.extend(run_audit(&mut p).suggestions.iter().map(|s| s.rule_id[11..].to_string()));
        }
        for (a, b) in CONFLICTS.iter().chain(MODEL_CONFLICTS) {
            assert!(fired.contains(*a) && fired.contains(*b), "{a}/{b}: a rule never fires, so the guard is vacuous");
        }
    }

    #[test]
    fn ewi_estate_has_no_semantic_duplicates() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/ewi_estate");
        let r = run_audit(&mut build_portfolio(&root));
        let d = semantic_dups(&r.suggestions);
        assert!(d.is_empty(), "{d:?}");
        // ewi native_core fct_orders is where TST0004 and TST0012 used to repeat each other.
        let c = clashes(&r.suggestions);
        assert!(c.is_empty(), "conflicting advice in ewi_estate: {c:?}");
    }

    #[test]
    fn cisco_estate_has_no_duplicate_findings() {
        let r = check_estate("cisco_estate", 4);
        assert!(r.suggestions.iter().filter(|s| !s.file.starts_with('<') && !s.file.is_empty()).all(|s| s.file.starts_with("cisco_")));
    }

    #[test]
    fn informatica_has_no_duplicate_or_conflicting_findings() {
        check_estate("snowconvert/Informatica", 20);
    }
}
