//! COL rules: model output columns against the scai Snowflake DDL.
//!
//! Input: `AuditConfig::ddl` (parsed from `ddl_paths`) and the model SQL.
//! The rules report nothing when no DDL is configured.

use serde_json::{json, Value};

use crate::ddl::{is_text_type, types_compatible, DdlColumn, DdlTable};
use crate::discovery::{AuditConfig, ModelFile, PortfolioContext, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::Suggestion;
use crate::projection::{projections, Projection, ProjectionKind};
use crate::sqlutil::{py_str, Config};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTCOL0001", detect: Detect::Model(col0001) },
    Detector { code: "SSC-EWI-DBTCOL0002", detect: Detect::Model(col0002) },
    Detector { code: "SSC-EWI-DBTCOL0003", detect: Detect::Model(col0003) },
    Detector { code: "SSC-EWI-DBTCOL0004", detect: Detect::Model(col0004) },
    Detector { code: "SSC-EWI-DBTCOL0005", detect: Detect::Model(col0005) },
    Detector { code: "SSC-EWI-DBTCOL0006", detect: Detect::Model(col0006) },
    Detector { code: "SSC-EWI-DBTCOL0007", detect: Detect::Portfolio(col0007) },
];

pub enum TableMatch<'a> {
    None,
    Ambiguous(Vec<&'a DdlTable>),
    One(&'a DdlTable),
}

fn cfg_str(cfg: &Config, key: &str) -> Option<String> {
    cfg.get(key).filter(|v| !v.is_null()).map(py_str).filter(|s| !s.trim().is_empty())
}

/// True when the model config has `enabled=false`.
pub fn is_disabled(cfg: &Config) -> bool {
    matches!(cfg.get("enabled"), Some(Value::Bool(false))) || cfg_str(cfg, "enabled").is_some_and(|s| s.eq_ignore_ascii_case("false"))
}

/// Find the DDL table for a relation name. `schema` and `database` config
/// choose between tables with the same name. When the filter removes every
/// candidate (for example a custom `generate_schema_name`), all candidates stay.
pub fn match_table<'a>(name: &str, cfg: &Config, config: &'a AuditConfig) -> TableMatch<'a> {
    let name = cfg_str(cfg, "alias").unwrap_or_else(|| name.to_string());
    let all: Vec<&DdlTable> = config.ddl.tables(&name).iter().collect();
    let resolve = |k: &str| cfg_str(cfg, k).map(|v| crate::ddl::resolve_binding(&v, &config.ddl_bindings).to_uppercase());
    let (schema, db) = (resolve("schema"), resolve("database"));
    let same = |want: &Option<String>, got: &Option<String>| match (want, got) {
        (Some(w), Some(g)) => w.eq_ignore_ascii_case(g),
        _ => true,
    };
    let picked: Vec<&DdlTable> = all.iter().copied().filter(|t| same(&schema, &t.schema) && same(&db, &t.database)).collect();
    let set = if picked.is_empty() { all } else { picked };
    match set.len() {
        0 => TableMatch::None,
        1 => TableMatch::One(set[0]),
        _ => TableMatch::Ambiguous(set),
    }
}

/// Snowflake name of an identifier: exact when quoted, else upper case.
pub fn resolved(name: &str, quoted: bool) -> String {
    if quoted { name.to_string() } else { name.to_uppercase() }
}

/// One output column with its DDL column, when names match.
pub struct Checked<'a> {
    pub projection: Projection,
    pub column: Option<&'a DdlColumn>,
}

pub struct Analysis<'a> {
    pub table: &'a DdlTable,
    pub items: Vec<Checked<'a>>,
    /// True when `*`, Jinja-only or unaliased items hide output names.
    pub names_unknown: bool,
}

impl Analysis<'_> {
    pub fn missing(&self) -> Vec<&DdlColumn> {
        if self.names_unknown {
            return vec![];
        }
        self.table
            .columns
            .iter()
            .filter(|c| !self.items.iter().any(|i| i.column.is_some_and(|m| std::ptr::eq(m, *c))))
            .collect()
    }
}

/// Match one model's outer SELECT to its DDL table.
pub fn analyze<'a>(model: &ModelFile, config: &'a AuditConfig) -> Option<Analysis<'a>> {
    if model.is_python || config.ddl.by_table.is_empty() || is_disabled(&model.effective_config) {
        return None;
    }
    let TableMatch::One(table) = match_table(&model.name, &model.effective_config, config) else { return None };
    let ps = projections(&model.raw);
    if ps.is_empty() {
        return None;
    }
    let names_unknown = ps.iter().any(|p| p.kind != ProjectionKind::Named);
    let items = ps
        .into_iter()
        .map(|p| {
            let column = p.alias.as_ref().and_then(|a| {
                let want = resolved(a, p.alias_quoted);
                table.columns.iter().find(|c| c.name == want)
            });
            Checked { projection: p, column }
        })
        .collect();
    Some(Analysis { table, items, names_unknown })
}

/// True when the cast type differs from the DDL type, or there is no cast.
pub fn needs_type(p: &Projection, c: &DdlColumn, strict: bool) -> bool {
    p.cast_type.as_ref().is_none_or(|t| !types_compatible(t, &c.raw_type, strict))
}

/// True when a text column's collation differs from the DDL collation.
pub fn needs_collation(p: &Projection, c: &DdlColumn) -> bool {
    is_text_type(&c.normalized_type) && !p.collation.as_deref().unwrap_or("").eq_ignore_ascii_case(c.collation.as_deref().unwrap_or(""))
}

fn ddl_ref(t: &DdlTable, line: u32) -> String {
    format!("{}:{}", t.file.display(), line)
}

fn table_label(t: &DdlTable) -> String {
    [t.database.as_deref(), t.schema.as_deref(), Some(t.name.as_str())].into_iter().flatten().collect::<Vec<_>>().join(".")
}

fn base(code: &str, msg: String, model: &ModelFile, table: &DdlTable, line: u32) -> Suggestion {
    Suggestion::new(code, msg)
        .file(model.relative_path.clone())
        .line(line)
        .ctx("model", json!(model.name))
        .ctx("ddl_table", json!(table_label(table)))
        .ctx("ddl_file", json!(table.file.display().to_string()))
}

fn col0001(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    if model.is_python || is_disabled(&model.effective_config) {
        return vec![];
    }
    let TableMatch::Ambiguous(ts) = match_table(&model.name, &model.effective_config, &project.config) else { return vec![] };
    let names: Vec<String> = ts.iter().map(|t| table_label(t)).collect();
    vec![Suggestion::new(
        "SSC-EWI-DBTCOL0001",
        format!("`{}` matches {} scai DDL tables: {}.", model.name, ts.len(), names.join(", ")),
    )
    .file(model.relative_path.clone())
    .line(1)
    .ctx("model", json!(model.name))
    .evidence(ts.iter().map(|t| ddl_ref(t, t.line)).collect::<Vec<_>>().join("; "))]
}

fn col0002(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(a) = analyze(model, &project.config) else { return vec![] };
    let line = a.items.first().map_or(1, |i| i.projection.line);
    a.missing()
        .into_iter()
        .map(|c| {
            base(
                "SSC-EWI-DBTCOL0002",
                format!("`{}` has no output column `{}` from {}.", model.name, c.name, table_label(a.table)),
                model,
                a.table,
                line,
            )
            .ctx("column_name", json!(c.name))
            .evidence(format!("{} {}", ddl_ref(a.table, c.line), c.raw_type))
        })
        .collect()
}

/// A DDL column equal to `alias` after ignoring case, quotes and underscores.
fn near_match<'a>(alias: &str, t: &'a DdlTable) -> Option<&'a DdlColumn> {
    let key = |s: &str| s.replace('_', "").to_uppercase();
    t.columns.iter().find(|c| key(&c.name) == key(alias))
}

fn col0003(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(a) = analyze(model, &project.config) else { return vec![] };
    a.items
        .iter()
        .filter(|i| i.column.is_none() && i.projection.kind == ProjectionKind::Named)
        .map(|i| {
            let alias = i.projection.alias.clone().unwrap_or_default();
            let mut msg = format!("Output column `{alias}` is not in {}.", table_label(a.table));
            if let Some(n) = near_match(&alias, a.table) {
                msg.push_str(&format!(" Did you mean `{}`?", n.name));
            }
            base("SSC-EWI-DBTCOL0003", msg, model, a.table, i.projection.line)
                .ctx("column_name", json!(alias))
                .evidence(ddl_ref(a.table, a.table.line))
        })
        .collect()
}

fn col0004(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(a) = analyze(model, &project.config) else { return vec![] };
    a.items
        .iter()
        .filter(|i| i.projection.kind != ProjectionKind::Named)
        .map(|i| {
            let what = match i.projection.kind {
                ProjectionKind::Star => "`*`",
                ProjectionKind::Jinja => "a Jinja-only item",
                _ => "an expression with no alias",
            };
            base(
                "SSC-EWI-DBTCOL0004",
                format!("The outer SELECT of `{}` has {what}, so its columns cannot be checked against {}.", model.name, table_label(a.table)),
                model,
                a.table,
                i.projection.line,
            )
        })
        .collect()
}

fn col0005(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let strict = project.config.type_compare_strict;
    let Some(a) = analyze(model, &project.config) else { return vec![] };
    a.items
        .iter()
        .filter_map(|i| i.column.map(|c| (i, c)))
        .filter(|(i, c)| needs_type(&i.projection, c, strict))
        .map(|(i, c)| {
            let msg = match &i.projection.cast_type {
                Some(t) => format!("`{}` is cast to `{t}`; the DDL type is `{}`.", c.name, c.raw_type),
                None => format!("`{}` has no explicit cast; the DDL type is `{}`.", c.name, c.raw_type),
            };
            base("SSC-EWI-DBTCOL0005", msg, model, a.table, i.projection.line)
                .ctx("column_name", json!(c.name))
                .evidence(format!("{} {}", ddl_ref(a.table, c.line), c.raw_type))
        })
        .collect()
}

fn col0006(model: &ModelFile, project: &ProjectContext) -> Vec<Suggestion> {
    let Some(a) = analyze(model, &project.config) else { return vec![] };
    a.items
        .iter()
        .filter_map(|i| i.column.map(|c| (i, c)))
        .filter(|(i, c)| needs_collation(&i.projection, c))
        .map(|(i, c)| {
            let want = c.collation.as_deref().map_or("no collation".to_string(), |s| format!("'{s}'"));
            let got = i.projection.collation.as_deref().map_or("no collation".to_string(), |s| format!("'{s}'"));
            base("SSC-EWI-DBTCOL0006", format!("`{}` has {got}; the DDL has {want}.", c.name), model, a.table, i.projection.line)
                .ctx("column_name", json!(c.name))
                .evidence(format!("{} {}", ddl_ref(a.table, c.line), c.raw_type))
        })
        .collect()
}

fn col0007(portfolio: &PortfolioContext) -> Vec<Suggestion> {
    portfolio
        .config
        .ddl
        .errors
        .iter()
        .map(|e| {
            let file = e.file.strip_prefix(&portfolio.root).unwrap_or(&e.file).display().to_string();
            Suggestion::new("SSC-EWI-DBTCOL0007", format!("scai DDL not read: {}", e.message))
                .file(file)
                .line(e.line.max(1))
                .evidence(e.message.clone())
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const DDL: &str = "USE DATABASE SHOP;\nCREATE OR REPLACE TABLE store.Orders (\n    OrderID INT IDENTITY(1,1) ORDER NOT NULL,\n    Status NVARCHAR(100) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 ***/ NULL DEFAULT ('Pending'),\n    OrderDate TIMESTAMP_NTZ(3) NULL\n)\nCOMMENT = '{ \"origin\": \"sf_sc\" }';\n";

    fn project(model: &str) -> TempProject {
        TempProject::new(&[
            (".dbt-quality.yml", "ddl_paths: [scai]\n"),
            ("scai/snowflake/shop/store/table/orders.sql", DDL),
            ("models/orders.sql", model),
        ])
    }

    fn codes(t: &TempProject) -> Vec<(String, Option<u32>)> {
        t.audit()
            .into_iter()
            .filter(|s| s.rule_id.contains("DBTCOL"))
            .map(|s| (s.rule_id[14..].to_string(), s.line))
            .collect()
    }

    #[test]
    fn clean_model_has_no_findings() {
        let t = project(
            "select\n  cast(id as int) as orderid,\n  cast(s as nvarchar(100)) collate 'en-ci-as' as status,\n  cast(d as timestamp_ntz(3)) as OrderDate\nfrom {{ ref('x') }}",
        );
        assert_eq!(codes(&t), vec![]);
    }

    #[test]
    fn each_rule_fires_on_its_case() {
        let t = project("select\n  id::float as orderid,\n  s as status,\n  d as order_date,\n  price * qty\nfrom {{ ref('x') }}");
        let mut got = codes(&t);
        got.sort();
        assert_eq!(
            got,
            vec![
                ("0003".into(), Some(4)),
                ("0004".into(), Some(5)),
                ("0005".into(), Some(2)),
                ("0005".into(), Some(3)),
                ("0006".into(), Some(3)),
            ],
            "COL0002 is silent while an unaliased item hides names"
        );
        let s = t.findings("SSC-EWI-DBTCOL0003");
        assert!(s[0].message.contains("Did you mean `ORDERDATE`"), "{}", s[0].message);
    }

    #[test]
    fn missing_column_and_quoted_case() {
        let t = project("select cast(id as int) as \"OrderID\" from t");
        let mut got: Vec<String> = codes(&t).into_iter().map(|(c, _)| c).collect();
        got.sort();
        assert_eq!(got, vec!["0002", "0002", "0002", "0003"]);
    }

    #[test]
    fn ambiguity_disabled_models_and_no_config() {
        let t = TempProject::new(&[
            (".dbt-quality.yml", "ddl_paths: [scai]\n"),
            ("scai/snowflake/shop/a/table/orders.sql", "CREATE TABLE a.orders (x INT);"),
            ("scai/snowflake/shop/b/table/orders.sql", "CREATE TABLE b.orders (x INT);"),
            ("models/orders.sql", "select 1 as y from t"),
            ("models/b/orders_b.sql", "{{ config(alias='orders', schema='B') }}\nselect 1 as y from t"),
            ("models/off/orders_c.sql", "{{ config(alias='orders', enabled=false) }}\nselect 1 as y from t"),
        ]);
        let all: Vec<_> = t.audit().into_iter().filter(|s| s.rule_id.contains("DBTCOL")).map(|s| (s.rule_id, s.file)).collect();
        assert!(all.contains(&("SSC-EWI-DBTCOL0001".into(), "models/orders.sql".into())), "{all:?}");
        assert!(all.iter().any(|(c, f)| c.ends_with("0003") && f.ends_with("orders_b.sql")), "{all:?}");
        assert!(!all.iter().any(|(_, f)| f.ends_with("orders_c.sql")), "{all:?}");
        let none = TempProject::new(&[("models/orders.sql", "select 1 as y from t")]);
        assert!(none.audit().iter().all(|s| !s.rule_id.contains("DBTCOL")));
    }

    #[test]
    fn unreadable_ddl_is_reported_once() {
        let t = TempProject::new(&[
            (".dbt-quality.yml", "ddl_paths: [scai]\n"),
            ("scai/snowflake/d/s/table/bad.sql", "CREATE TABLE s.bad (a INT,,);"),
            ("models/m.sql", "select 1 as a from t"),
        ]);
        let f = t.findings("SSC-EWI-DBTCOL0007");
        assert_eq!(f.len(), 1);
        assert!(f[0].file.ends_with("bad.sql"), "{}", f[0].file);
    }
}
