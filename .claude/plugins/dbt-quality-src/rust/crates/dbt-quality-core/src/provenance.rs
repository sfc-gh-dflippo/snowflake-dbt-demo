//! Migration provenance: whether a project is mechanically converted output.
//!
//! The verdict suppresses ARCHITECTURE-tier rules for converted code.
//! Detection combines weighted signals; one weak signal is not enough.

use std::collections::BTreeSet;

use crate::discovery::{fnmatch, ProjectContext};
use crate::rx;

pub fn ewi_pattern() -> &'static regex::Regex {
    rx!(r"(?i)SSC-EWI-[A-Z]*\d+")
}
pub fn fdm_pattern() -> &'static regex::Regex {
    rx!(r"(?i)SSC-FDM-[A-Z]*\d+")
}
pub fn resolve_ewi_pattern() -> &'static regex::Regex {
    rx!(r"(?i)!!!RESOLVE\s+EWI!!!")
}
pub fn needs_user_pattern() -> &'static regex::Regex {
    rx!(r"(?i)--\s*NEEDS-USER:")
}
pub fn etl_control_column_pattern() -> &'static regex::Regex {
    rx!(r"(?i)\betl_dml_operation__\b")
}
pub fn dd_constant_pattern() -> &'static regex::Regex {
    rx!(r"(?i)'DD_(INSERT|UPDATE|DELETE|REJECT)'")
}

pub const PLACEHOLDER_VALUES: &[&str] =
    &["YOUR_PROJECT_NAME", "YOUR_PROFILE_NAME", "your_project_name", "your_profile_name", "YOUR_DB", "YOUR_SCHEMA"];

fn marker_text_pattern() -> &'static regex::Regex {
    rx!(r"(?im)(SSC-(?:EWI|FDM)-[A-Z]*\d+)\s*[-:]\s*(.+?)\s*(?:\*+/+!*|\*\*|$)")
}
fn needs_user_text_pattern() -> &'static regex::Regex {
    rx!(r"(?im)--\s*NEEDS-USER:\s*(.+?)\s*(?:\*+/+!*|\*\*|$)")
}

fn line_end(raw: &str, pos: usize) -> usize {
    raw[pos..].find('\n').map_or(raw.len(), |i| pos + i)
}

/// The description SnowConvert wrote on the marker line at `pos`.
pub fn marker_text(raw: &str, pos: usize) -> String {
    let end = line_end(raw, pos);
    marker_text_pattern().captures(&raw[pos..end]).map(|c| c[2].trim().to_string()).unwrap_or_default()
}

pub fn needs_user_text(raw: &str, pos: usize) -> String {
    let end = line_end(raw, pos);
    needs_user_text_pattern().captures(&raw[pos..end]).map(|c| c[1].trim().to_string()).unwrap_or_default()
}

#[derive(Debug, Clone)]
pub struct ProvenanceVerdict {
    pub is_migration: bool,
    pub forced: bool,
    pub score: i32,
    pub confidence: String,
    pub signals: Vec<String>,
    pub source_platform: String,
    pub migrated_files: BTreeSet<String>,
}

impl Default for ProvenanceVerdict {
    fn default() -> Self {
        ProvenanceVerdict {
            is_migration: false,
            forced: false,
            score: 0,
            confidence: "none".into(),
            signals: vec![],
            source_platform: String::new(),
            migrated_files: BTreeSet::new(),
        }
    }
}

impl ProvenanceVerdict {
    pub fn suppression_reason(&self) -> String {
        if self.forced {
            return "migration mode forced via .dbt-quality.yml".into();
        }
        let n = self.signals.len().min(3);
        format!("lift-and-shift provenance detected: {}", self.signals[..n].join("; "))
    }

    pub fn covers(&self, relative_path: &str) -> bool {
        if !self.is_migration {
            return false;
        }
        if self.forced || self.confidence == "high" {
            return true;
        }
        self.migrated_files.contains(relative_path)
    }
}

const THRESHOLD: i32 = 4;

pub fn classify(project: &ProjectContext) -> ProvenanceVerdict {
    let mut v = ProvenanceVerdict::default();
    let config = &project.config;
    if config.migration_mode == "lift_and_shift" {
        v.is_migration = true;
        v.forced = true;
        v.confidence = "high".into();
        v.score = 99;
        v.signals.push("migration.mode set to lift_and_shift".into());
        return v;
    }
    if config.migration_mode == "native" {
        v.signals.push("migration.mode set to native; provenance detection skipped".into());
        return v;
    }
    for pat in &config.migration_paths {
        for m in &project.models {
            if fnmatch(&m.relative_path, pat) {
                v.migrated_files.insert(m.relative_path.clone());
            }
        }
    }
    if !v.migrated_files.is_empty() {
        v.score += 4;
        v.signals.push(format!("{} model(s) matched migration.paths in .dbt-quality.yml", v.migrated_files.len()));
    }
    if project.root.join(".scai/config/project.yml").is_file() {
        v.score += 4;
        v.signals.push(".scai/config/project.yml present (conversion project root)".into());
    }
    if rx!(r"(?i)(^|/)Output/ETL/").is_match(&project.relative_root.replace('\\', "/")) {
        v.score += 3;
        v.signals.push("project sits under an Output/ETL/{Package}/{DataFlow} layout".into());
    }
    let mut ewi = BTreeSet::new();
    let mut control = BTreeSet::new();
    for m in &project.models {
        let t = if m.without_directives.is_empty() { &m.raw } else { &m.without_directives };
        if ewi_pattern().is_match(t) || fdm_pattern().is_match(t) || resolve_ewi_pattern().is_match(t) || needs_user_pattern().is_match(t) {
            ewi.insert(m.relative_path.clone());
        }
        if etl_control_column_pattern().is_match(&m.raw) || dd_constant_pattern().is_match(&m.raw) {
            control.insert(m.relative_path.clone());
        }
    }
    if !ewi.is_empty() {
        v.score += 4;
        v.signals.push(format!("{} model(s) carry SSC-EWI/SSC-FDM conversion markers", ewi.len()));
        v.migrated_files.extend(ewi);
    }
    if !control.is_empty() {
        v.score += 3;
        v.signals.push(format!("{} model(s) use ETL control flags (etl_dml_operation__ / DD_* constants)", control.len()));
        v.migrated_files.extend(control);
    }
    let stg_raw: Vec<String> =
        project.models.iter().filter(|m| rx!(r"(?i)^stg_raw__").is_match(&m.name)).map(|m| m.relative_path.clone()).collect();
    if !stg_raw.is_empty() {
        v.score += 3;
        v.signals.push(format!("{} model(s) use the generated stg_raw__ prefix", stg_raw.len()));
        v.migrated_files.extend(stg_raw);
    }
    let etl: Vec<String> = project
        .models
        .iter()
        .filter(|m| rx!(r"(?i)^(int_)?(SQ|EXP|FIL|LKP|JNR|RTR|SRT|NRM|MPLT|UPDTRANS)[_\d]").is_match(&m.name))
        .map(|m| m.relative_path.clone())
        .collect();
    if !etl.is_empty() {
        v.score += 2;
        v.signals.push(format!(
            "{} model(s) named after ETL transformation instances (SQ_/EXP_/FIL_/LKP_/JNR_/RTR_/SRT_/NRM_/MPLT_/UPDTRANS...)",
            etl.len()
        ));
        v.migrated_files.extend(etl);
    }
    if project_yml_has_placeholder(project) {
        v.score += 3;
        v.signals.push("dbt_project.yml contains unresolved converter placeholders".into());
    }
    v.source_platform = infer_platform(project);
    v.is_migration = v.score >= THRESHOLD;
    v.confidence = if v.score >= 7 {
        "high"
    } else if v.score >= THRESHOLD {
        "medium"
    } else if v.score > 0 {
        "low"
    } else {
        "none"
    }
    .into();
    if v.is_migration && v.migrated_files.is_empty() {
        v.confidence = "high".into();
    }
    v
}

/// Whether any parsed `dbt_project.yml` key or value holds a placeholder.
pub fn project_yml_has_placeholder(project: &ProjectContext) -> bool {
    let text = serde_json::to_string(&project.project_yml).unwrap_or_default();
    PLACEHOLDER_VALUES.iter().any(|p| text.contains(p))
}

fn infer_platform(project: &ProjectContext) -> String {
    let combined: String = project
        .models
        .iter()
        .take(60)
        .map(|m| m.raw.chars().take(4000).collect::<String>())
        .collect::<Vec<_>>()
        .join("\n");
    if rx!(r"(?i)SSC-(EWI|FDM)-INF").is_match(&combined) {
        return "Informatica PowerCenter".into();
    }
    if rx!(r"(?i)SSC-(EWI|FDM)-SSIS").is_match(&combined) {
        return "SQL Server Integration Services".into();
    }
    if etl_control_column_pattern().is_match(&combined) || dd_constant_pattern().is_match(&combined) {
        return "Informatica PowerCenter".into();
    }
    String::new()
}
