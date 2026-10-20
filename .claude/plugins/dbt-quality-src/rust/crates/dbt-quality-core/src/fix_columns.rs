//! Rewrite model output columns to the scai DDL type and collation.
//!
//! Input: a dbt root, the scai DDL (config or override), and model globs.
//! Output: one `FileFix` per matched model, plus a unified diff.
//! Side effect: with `write`, changed model files are overwritten.
//! Scope: retype and collate only. Missing and extra columns become warnings.

use std::path::{Path, PathBuf};

use serde::Serialize;

use crate::discovery::{build_portfolio_with_ddl, fnmatch, ModelFile, ProjectContext};
use crate::projection::{projections, ProjectionKind};
use crate::rules::col::{analyze, is_disabled, match_table, needs_collation, needs_type, TableMatch};

#[derive(Debug, Default)]
pub struct FixOptions {
    /// Replaces `ddl_paths` when not empty.
    pub ddl: Vec<PathBuf>,
    /// fnmatch globs on the root-relative model path. Empty selects every model.
    pub select: Vec<String>,
    pub write: bool,
    pub allow_dirty: bool,
}

#[derive(Debug, Serialize, Clone)]
pub struct Edit {
    pub line: u32,
    pub column: String,
    /// `retype`, `collate`, or `retype_and_collate`.
    pub kind: String,
    pub before: String,
    pub after: String,
}

#[derive(Debug, Serialize, Clone)]
pub struct FileFix {
    pub path: String,
    pub ddl_table: Option<String>,
    pub ddl_file: Option<String>,
    /// `changed`, `ok`, `no_ddl`, `ambiguous`, `placeholder`, or `skipped`.
    pub status: String,
    pub changed: bool,
    pub edits: Vec<Edit>,
    pub warnings: Vec<String>,
    #[serde(skip)]
    pub new_text: Option<String>,
}

#[derive(Debug, Default, Serialize)]
pub struct FixOutcome {
    pub files: Vec<FileFix>,
    #[serde(skip)]
    pub diff: String,
}

/// Fix one model's text. `status` says why nothing changed.
pub fn fix_model(model: &ModelFile, project: &ProjectContext) -> FileFix {
    let mut out = FileFix {
        path: model.relative_path.clone(),
        ddl_table: None,
        ddl_file: None,
        status: "no_ddl".into(),
        changed: false,
        edits: vec![],
        warnings: vec![],
        new_text: None,
    };
    let config = &project.config;
    if is_disabled(&model.effective_config) {
        out.status = "placeholder".into();
        return out;
    }
    match match_table(&model.name, &model.effective_config, config) {
        TableMatch::None => return out,
        TableMatch::Ambiguous(ts) => {
            out.status = "ambiguous".into();
            out.warnings.push(format!("{} DDL tables match", ts.len()));
            return out;
        }
        TableMatch::One(t) => {
            out.ddl_table = Some(t.name.clone());
            out.ddl_file = Some(t.file.display().to_string());
        }
    }
    let Some(a) = analyze(model, config) else {
        out.status = "skipped".into();
        out.warnings.push("no outer SELECT list found".into());
        return out;
    };
    let strict = config.type_compare_strict;
    let raw = &model.raw;
    let mut pieces: Vec<((usize, usize), String, Edit)> = vec![];
    for item in &a.items {
        let p = &item.projection;
        match (p.kind.clone(), item.column) {
            (ProjectionKind::Named, None) => out.warnings.push(format!("extra_in_model: {}", p.alias.as_deref().unwrap_or(""))),
            (ProjectionKind::Named, Some(c)) => {
                let (t, k) = (needs_type(p, c, strict), needs_collation(p, c));
                if !t && !k {
                    continue;
                }
                let ty = if t { c.raw_type.clone() } else { p.cast_type.clone().unwrap_or_else(|| c.raw_type.clone()) };
                let collate = c.collation.as_ref().filter(|_| crate::ddl::is_text_type(&c.normalized_type)).map(|s| format!(" COLLATE '{s}'")).unwrap_or_default();
                let alias = p.alias_raw.clone().unwrap_or_else(|| p.alias.clone().unwrap_or_default());
                let as_kw = p.as_keyword.clone().unwrap_or_else(|| "AS".into());
                let after = format!("CAST({} AS {ty}){collate} {as_kw} {alias}", p.inner);
                let kind = match (t, k) {
                    (true, true) => "retype_and_collate",
                    (true, false) => "retype",
                    _ => "collate",
                };
                let before = raw[p.span.0..p.span.1].to_string();
                let edit = Edit { line: p.line, column: c.name.clone(), kind: kind.into(), before, after: after.clone() };
                pieces.push((p.span, after, edit));
            }
            _ => out.warnings.push(format!("unchecked item at line {}", p.line)),
        }
    }
    for c in a.missing() {
        out.warnings.push(format!("missing_in_model: {}", c.name));
    }
    if pieces.is_empty() {
        out.status = "ok".into();
        return out;
    }
    let mut new = String::with_capacity(raw.len() + 64);
    let mut last = 0;
    for ((s, e), text, _) in &pieces {
        new.push_str(&raw[last..*s]);
        new.push_str(text);
        last = *e;
    }
    new.push_str(&raw[last..]);
    // Scan the new text again. Skip the file if the output column names changed.
    let names = |sql: &str| projections(sql).into_iter().map(|p| p.alias).collect::<Vec<_>>();
    if names(&new) != names(raw) {
        out.status = "skipped".into();
        out.warnings.push("rewrite changed the output columns; file left unchanged".into());
        return out;
    }
    out.edits = pieces.into_iter().map(|(_, _, e)| e).collect();
    out.status = "changed".into();
    out.changed = true;
    out.new_text = Some(new);
    out
}

/// Fix every selected model under `root`.
pub fn fix_columns(root: &Path, opts: &FixOptions) -> Result<FixOutcome, String> {
    if opts.write && !opts.allow_dirty {
        crate::annotate::check_clean(root)?;
    }
    let portfolio = build_portfolio_with_ddl(root, &opts.ddl);
    if portfolio.config.ddl.is_empty() {
        return Err("no scai DDL found: set ddl_paths in .dbt-quality.yml or pass --ddl".into());
    }
    let mut out = FixOutcome::default();
    for p in &portfolio.projects {
        for m in &p.models {
            let rel = crate::discovery::root_relative(p, &m.relative_path);
            if !opts.select.is_empty() && !opts.select.iter().any(|g| fnmatch(&rel, g)) {
                continue;
            }
            let mut f = fix_model(m, p);
            f.path = rel;
            if f.status == "no_ddl" {
                continue;
            }
            if let Some(new) = &f.new_text {
                out.diff.push_str(&similar::TextDiff::from_lines(&m.raw, new).unified_diff().context_radius(2).header(&format!("a/{}", f.path), &format!("b/{}", f.path)).to_string());
                if opts.write {
                    std::fs::write(&m.path, new).map_err(|e| format!("{}: {e}", m.path.display()))?;
                }
            }
            out.files.push(f);
        }
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::testing::TempProject;

    const DDL: &str = "CREATE TABLE store.Orders (\n  OrderID INT,\n  Status NVARCHAR(100) COLLATE 'EN-CI-AS',\n  Total NUMBER(18,2)\n);";

    fn project(model: &str) -> TempProject {
        TempProject::new(&[("scai/snowflake/d/store/table/orders.sql", DDL), ("models/orders.sql", model)])
    }

    fn run(t: &TempProject) -> FixOutcome {
        fix_columns(t.path(), &FixOptions { ddl: vec![t.path().join("scai")], write: true, allow_dirty: true, ..Default::default() }).unwrap()
    }

    #[test]
    fn rewrites_type_and_collation_and_is_idempotent() {
        let t = project(
            "with x as (select 1 as a)\nselect\n  orderid::bigint as OrderID, -- id\n  {{ trim('s') }} status,\n  cast(t as float) As \"TOTAL\",\n  o.extra\nfrom {{ ref('src') }} o",
        );
        let out = run(&t);
        let f = &out.files[0];
        assert_eq!(f.status, "changed", "{f:?}");
        assert_eq!(f.edits.iter().map(|e| e.kind.as_str()).collect::<Vec<_>>(), vec!["retype_and_collate", "retype"]);
        let text = std::fs::read_to_string(t.path().join("models/orders.sql")).unwrap();
        assert!(text.contains("  orderid::bigint as OrderID, -- id\n"), "compatible type stays: {text}");
        assert!(text.contains("  CAST({{ trim('s') }} AS NVARCHAR(100)) COLLATE 'EN-CI-AS' AS status,\n"), "{text}");
        assert!(text.contains("  CAST(t AS NUMBER(18,2)) As \"TOTAL\",\n"), "{text}");
        assert!(f.warnings.iter().any(|w| w == "extra_in_model: extra"), "{:?}", f.warnings);
        assert!(out.diff.contains("+  CAST(t AS NUMBER(18,2))"));
        let again = run(&t);
        assert_eq!(again.files[0].status, "ok", "{:?}", again.files[0]);
        assert!(again.diff.is_empty());
    }

    #[test]
    fn collate_only_keeps_the_cast_and_dry_run_writes_nothing() {
        let t = project("select cast(s as varchar(100)) collate 'x' as status from t");
        let out = fix_columns(t.path(), &FixOptions { ddl: vec![t.path().join("scai")], ..Default::default() }).unwrap();
        assert_eq!(out.files[0].edits[0].kind, "collate");
        assert_eq!(out.files[0].edits[0].after, "CAST(s AS varchar(100)) COLLATE 'EN-CI-AS' as status");
        assert!(std::fs::read_to_string(t.path().join("models/orders.sql")).unwrap().contains("collate 'x'"));
        assert!(out.files[0].warnings.iter().any(|w| w == "missing_in_model: ORDERID"));
    }

    #[test]
    fn no_ddl_is_an_error() {
        let t = TempProject::new(&[("models/m.sql", "select 1 as a")]);
        assert!(fix_columns(t.path(), &FixOptions::default()).is_err());
    }
}
