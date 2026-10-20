//! Index of Snowflake table DDL written by scai (SnowConvert AI).
//!
//! Input: scai project roots, `snowflake/` folders, or single `.sql` files.
//! Output: a `DdlIndex` keyed by upper-case table name. Each column keeps its
//! raw type text, normalized type, collation, nullability, and source line.
//! Side effects: none. A file that does not parse becomes a `DdlError`.

use std::collections::{BTreeMap, HashMap};
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

use regex::Regex;
use sqlparser::ast::{ColumnOption, ObjectName, Statement};
use sqlparser::dialect::SnowflakeDialect;
use sqlparser::parser::Parser;

#[derive(Debug, Clone, PartialEq)]
pub struct DdlColumn {
    /// Exact text when quoted in the DDL, else upper case.
    pub name: String,
    pub quoted: bool,
    /// The type as the DDL writes it, e.g. `NVARCHAR(100)`.
    pub raw_type: String,
    pub normalized_type: String,
    pub collation: Option<String>,
    pub not_null: bool,
    pub line: u32,
}

#[derive(Debug, Clone)]
pub struct DdlTable {
    pub database: Option<String>,
    pub schema: Option<String>,
    pub name: String,
    pub columns: Vec<DdlColumn>,
    /// Absolute path of the DDL file.
    pub file: PathBuf,
    pub line: u32,
}

impl DdlTable {
    pub fn column(&self, name: &str) -> Option<&DdlColumn> {
        self.columns.iter().find(|c| c.name.eq_ignore_ascii_case(name))
    }
}

#[derive(Debug, Clone)]
pub struct DdlError {
    pub file: PathBuf,
    pub line: u32,
    pub message: String,
}

#[derive(Debug, Clone, Default)]
pub struct DdlIndex {
    pub by_table: HashMap<String, Vec<DdlTable>>,
    pub errors: Vec<DdlError>,
}

impl DdlIndex {
    pub fn is_empty(&self) -> bool {
        self.by_table.is_empty() && self.errors.is_empty()
    }

    pub fn tables(&self, name: &str) -> &[DdlTable] {
        self.by_table.get(&name.to_uppercase()).map_or(&[], Vec::as_slice)
    }

    /// Read every path. A directory is walked for `.sql` files under a `table` folder.
    pub fn load(paths: &[PathBuf]) -> Self {
        let mut index = DdlIndex::default();
        for p in paths {
            let files = if p.is_dir() { table_files(p) } else { vec![p.clone()] };
            for f in files {
                match std::fs::read_to_string(&f) {
                    Ok(text) => index.add_file(&f, &text),
                    Err(e) => index.errors.push(DdlError { file: f, line: 0, message: e.to_string() }),
                }
            }
            index.cross_check_registry(p);
        }
        index
    }

    /// Parse one file and add its CREATE TABLE statements.
    pub fn add_file(&mut self, file: &Path, text: &str) {
        let text = prepare(text);
        let folder_db = folder_database(file);
        let mut use_db: Option<String> = None;
        for (start, stmt) in split_statements(&text) {
            let base_line = text[..start].matches('\n').count() as u32;
            if let Some(c) = USE_DB.captures(stmt) {
                use_db = Some(unquote(&c[1]));
                continue;
            }
            if !CREATE_TABLE.is_match(stmt) {
                continue;
            }
            let lead = stmt.len() - stmt.trim_start().len();
            let lead_lines = stmt[..lead].matches('\n').count() as u32;
            match Parser::parse_sql(&SnowflakeDialect {}, stmt) {
                Ok(parsed) => {
                    for s in parsed {
                        if let Statement::CreateTable(ct) = s {
                            let (db, schema, name) = split_name(&ct.name);
                            let columns = ct
                                .columns
                                .iter()
                                .map(|c| {
                                    let raw_type = c.data_type.to_string().replace(TS_MARK, "(").replace(", ", ",");
                                    let collation = c.options.iter().find_map(|o| match &o.option {
                                        ColumnOption::Collation(n) => Some(object_text(n)),
                                        _ => None,
                                    });
                                    let not_null = c.options.iter().any(|o| matches!(o.option, ColumnOption::NotNull));
                                    let quoted = c.name.quote_style.is_some();
                                    DdlColumn {
                                        name: if quoted { c.name.value.clone() } else { c.name.value.to_uppercase() },
                                        quoted,
                                        normalized_type: normalize_type(&raw_type),
                                        raw_type,
                                        collation,
                                        not_null,
                                        line: base_line + c.name.span.start.line.max(1) as u32,
                                    }
                                })
                                .collect();
                            let table = DdlTable {
                                database: db.or_else(|| use_db.clone()).or_else(|| folder_db.clone()),
                                schema,
                                name: name.clone(),
                                columns,
                                file: file.to_path_buf(),
                                line: base_line + lead_lines + 1,
                            };
                            self.by_table.entry(name.to_uppercase()).or_default().push(table);
                        }
                    }
                }
                Err(e) => self.errors.push(DdlError {
                    file: file.to_path_buf(),
                    line: base_line + lead_lines + 1,
                    message: e.to_string(),
                }),
            }
        }
    }

    /// Compare parsed columns with `registry/*.json` `signature.columns`.
    /// A difference is a `DdlError` so the user sees scai/parser drift.
    fn cross_check_registry(&mut self, root: &Path) {
        let Ok(rd) = std::fs::read_dir(root.join("registry")) else { return };
        let root = std::fs::canonicalize(root).unwrap_or_else(|_| root.to_path_buf());
        for e in rd.flatten() {
            let Ok(text) = std::fs::read_to_string(e.path()) else { continue };
            let Ok(v) = serde_json::from_str::<serde_json::Value>(&text) else { continue };
            if v["source"]["objectType"] != "table" {
                continue;
            }
            let Some(rel) = v["files"]["converted"]["path"].as_str() else { continue };
            let file = root.join(rel);
            let expected: Vec<String> = v["signature"]["columns"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(|c| c["targetName"].as_str().or(c["name"].as_str()))
                .map(str::to_uppercase)
                .collect();
            let file_c = std::fs::canonicalize(&file).unwrap_or(file.clone());
            let Some(t) = self
                .by_table
                .values()
                .flatten()
                .find(|t| std::fs::canonicalize(&t.file).is_ok_and(|f| f == file_c))
            else {
                continue;
            };
            let got: Vec<String> = t.columns.iter().map(|c| c.name.to_uppercase()).collect();
            if !expected.is_empty() && got != expected {
                let line = t.line;
                self.errors.push(DdlError {
                    file: t.file.clone(),
                    line,
                    message: format!("parsed columns {got:?} differ from registry signature {expected:?}"),
                });
            }
        }
    }
}

/// `.sql` files below a folder named `table`.
fn table_files(root: &Path) -> Vec<PathBuf> {
    let mut out = vec![];
    let mut stack = vec![(root.to_path_buf(), false)];
    while let Some((dir, under_table)) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&dir) else { continue };
        for e in rd.flatten() {
            let p = e.path();
            let name = e.file_name().to_string_lossy().to_string();
            if p.is_dir() {
                if !name.starts_with('.') && name != "target" {
                    stack.push((p, under_table || name.eq_ignore_ascii_case("table")));
                }
            } else if under_table && name.to_lowercase().ends_with(".sql") {
                out.push(p);
            }
        }
    }
    out.sort();
    out
}

/// `<db>` in `snowflake/<db>/<schema>/table/<file>`. `database_unspecified` maps to `None`.
fn folder_database(file: &Path) -> Option<String> {
    let parts: Vec<String> = file.components().map(|c| c.as_os_str().to_string_lossy().to_string()).collect();
    let n = parts.len();
    if n >= 5 && parts[n - 2].eq_ignore_ascii_case("table") && parts[n - 5].eq_ignore_ascii_case("snowflake") {
        let db = &parts[n - 4];
        return (!db.eq_ignore_ascii_case("database_unspecified")).then(|| db.clone());
    }
    None
}

static BIND_SNOW: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"<%([^%>]+)%>").unwrap());
static BIND_SRC: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\$\{([^}]+)\}").unwrap());
static COLLATE_LIT: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?i)\bCOLLATE\s+'([^']*)'").unwrap());
/// The sqlparser fork rejects `TIMESTAMP_NTZ(3)`. `prepare` renames it to the
/// custom type `TIMESTAMP_NTZ__P(3)`; `add_file` restores the name.
const TS_MARK: &str = "__P(";
static TS_PRECISION: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?i)\b(TIMESTAMP_(?:NTZ|LTZ|TZ))\s*\(").unwrap());
static USE_DB: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r#"(?is)^\s*USE\s+DATABASE\s+("[^"]+"|[A-Za-z0-9_$]+)\s*$"#).unwrap());
static CREATE_TABLE: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"(?is)^(?:\s|--[^\n]*\n|/\*.*?\*/)*CREATE\s+(?:OR\s+REPLACE\s+)?(?:(?:LOCAL|GLOBAL|TEMP|TEMPORARY|VOLATILE|TRANSIENT|HYBRID)\s+)*TABLE\b")
        .unwrap()
});

/// Remove the BOM. Replace binding tokens with their name. Rewrite
/// `COLLATE '<x>'` as `COLLATE "<x>"` so the parser reads an identifier.
/// Rename `TIMESTAMP_xTZ(n)` (see `TS_MARK`).
/// Every replacement is one line, so line numbers stay correct.
fn prepare(text: &str) -> String {
    let text = text.trim_start_matches('\u{feff}');
    let sanitize = |s: &str| s.chars().map(|c| if c.is_ascii_alphanumeric() || c == '_' { c } else { '_' }).collect::<String>();
    let text = BIND_SNOW.replace_all(text, |c: &regex::Captures| sanitize(&c[1]));
    let text = BIND_SRC.replace_all(&text, |c: &regex::Captures| sanitize(&c[1]));
    let text = COLLATE_LIT.replace_all(&text, |c: &regex::Captures| format!("COLLATE \"{}\"", &c[1]));
    TS_PRECISION.replace_all(&text, |c: &regex::Captures| format!("{}{TS_MARK}", &c[1])).into_owned()
}

/// Split on top-level `;`. Skip quotes, `$$` blocks and comments.
/// Return `(byte offset, statement text)` for each non-blank statement.
fn split_statements(text: &str) -> Vec<(usize, &str)> {
    let b = text.as_bytes();
    let mut out = vec![];
    let (mut i, mut start) = (0, 0);
    while i < b.len() {
        match b[i] {
            b'\'' | b'"' => {
                let q = b[i];
                i += 1;
                while i < b.len() {
                    if b[i] == q {
                        if i + 1 < b.len() && b[i + 1] == q {
                            i += 2;
                            continue;
                        }
                        break;
                    }
                    if b[i] == b'\\' && q == b'\'' {
                        i += 1;
                    }
                    i += 1;
                }
            }
            b'-' if b.get(i + 1) == Some(&b'-') => {
                while i < b.len() && b[i] != b'\n' {
                    i += 1;
                }
            }
            b'/' if b.get(i + 1) == Some(&b'*') => {
                i = text[i + 2..].find("*/").map_or(b.len(), |e| i + 2 + e + 1);
            }
            b'$' if b.get(i + 1) == Some(&b'$') => {
                i = text[i + 2..].find("$$").map_or(b.len(), |e| i + 2 + e + 1);
            }
            b';' => {
                out.push((start, &text[start..i]));
                start = i + 1;
            }
            _ => {}
        }
        i += 1;
    }
    out.push((start, &text[start.min(b.len())..]));
    out.retain(|(_, s)| !s.trim().is_empty());
    out
}

fn unquote(s: &str) -> String {
    s.strip_prefix('"').and_then(|s| s.strip_suffix('"')).map_or_else(|| s.to_uppercase(), str::to_string)
}

fn object_text(n: &ObjectName) -> String {
    n.0.iter().filter_map(|p| p.as_ident()).map(|i| i.value.clone()).collect::<Vec<_>>().join(".")
}

fn split_name(n: &ObjectName) -> (Option<String>, Option<String>, String) {
    let parts: Vec<String> = n
        .0
        .iter()
        .filter_map(|p| p.as_ident())
        .map(|i| if i.quote_style.is_some() { i.value.clone() } else { i.value.to_uppercase() })
        .collect();
    match parts.as_slice() {
        [d, s, t] => (Some(d.clone()), Some(s.clone()), t.clone()),
        [s, t] => (None, Some(s.clone()), t.clone()),
        [t] => (None, None, t.clone()),
        _ => (None, None, parts.last().cloned().unwrap_or_default()),
    }
}

/// Map type spellings to one Snowflake form. Keep arguments.
/// `NVARCHAR(10)` -> `VARCHAR(10)`, `INT` -> `NUMBER(38,0)`, `DATETIME` -> `TIMESTAMP_NTZ`.
pub fn normalize_type(t: &str) -> String {
    let t: String = t.to_uppercase().split_whitespace().collect::<Vec<_>>().join(" ");
    let (base, args) = match t.find('(') {
        Some(i) => (t[..i].trim().to_string(), t[i..].replace(' ', "")),
        None => (t.trim().to_string(), String::new()),
    };
    let base = match base.as_str() {
        "NVARCHAR" | "NVARCHAR2" | "VARCHAR2" | "CHAR" | "NCHAR" | "CHARACTER" | "CHARACTER VARYING" | "CHAR VARYING"
        | "STRING" | "TEXT" | "NTEXT" => "VARCHAR",
        "INT" | "INTEGER" | "BIGINT" | "SMALLINT" | "TINYINT" | "BYTEINT" => return "NUMBER(38,0)".into(),
        "DECIMAL" | "NUMERIC" => "NUMBER",
        "DOUBLE" | "DOUBLE PRECISION" | "REAL" | "FLOAT4" | "FLOAT8" => "FLOAT",
        "DATETIME" | "TIMESTAMP" | "TIMESTAMPNTZ" | "TIMESTAMP WITHOUT TIME ZONE" => "TIMESTAMP_NTZ",
        "TIMESTAMPLTZ" => "TIMESTAMP_LTZ",
        "TIMESTAMPTZ" | "TIMESTAMP WITH TIME ZONE" => "TIMESTAMP_TZ",
        "BOOL" => "BOOLEAN",
        "VARBINARY" => "BINARY",
        other => return format!("{other}{args}"),
    };
    format!("{base}{args}")
}

/// True when two type texts name the same Snowflake type.
/// `strict` compares the normalized text. Otherwise a side with no
/// arguments matches any arguments, e.g. `TIMESTAMP_NTZ` = `TIMESTAMP_NTZ(3)`.
pub fn types_compatible(a: &str, b: &str, strict: bool) -> bool {
    let (a, b) = (normalize_type(a), normalize_type(b));
    if a == b {
        return true;
    }
    if strict {
        return false;
    }
    let base = |s: &str| s.split('(').next().unwrap_or("").to_string();
    base(&a) == base(&b) && (!a.contains('(') || !b.contains('('))
}

/// Text type family, where collation applies.
pub fn is_text_type(normalized: &str) -> bool {
    normalized.starts_with("VARCHAR")
}

/// Resolve binding tokens in a database or schema name.
pub fn resolve_binding(value: &str, bindings: &BTreeMap<String, String>) -> String {
    let v = BIND_SNOW.replace_all(value, |c: &regex::Captures| bindings.get(&c[1]).cloned().unwrap_or_else(|| c[1].to_string()));
    BIND_SRC.replace_all(&v, |c: &regex::Captures| bindings.get(&c[1]).cloned().unwrap_or_else(|| c[1].to_string())).into_owned()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixtures() -> PathBuf {
        Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/scai")
    }

    #[test]
    fn tasktracker_tables_parse_and_match_the_registry() {
        let idx = DdlIndex::load(&[fixtures().join("tasktracker")]);
        assert!(idx.errors.is_empty(), "{:?}", idx.errors);
        let t = &idx.tables("tasks")[0];
        assert_eq!(t.schema.as_deref(), Some("DBO"));
        assert_eq!(t.database.as_deref(), Some("tasktracker"));
        assert_eq!(t.columns.len(), 9);
        let c = t.column("CreatedAt").unwrap();
        assert_eq!(c.raw_type, "TIMESTAMP_NTZ(3)");
        assert!(c.not_null);
        assert_eq!(c.line, 8);
        assert_eq!(t.column("Title").unwrap().raw_type, "VARCHAR(200)");
        assert_eq!(idx.by_table.len(), 3, "views and functions are not tables");
    }

    #[test]
    fn sample_store_keeps_collation_identity_and_use_database() {
        let idx = DdlIndex::load(&[fixtures().join("sample_store")]);
        assert!(idx.errors.is_empty(), "{:?}", idx.errors);
        let t = &idx.tables("ORDERS")[0];
        assert_eq!(t.database.as_deref(), Some("SAMPLESTOREDB"));
        assert_eq!(t.schema.as_deref(), Some("STORE"));
        let s = t.column("status").unwrap();
        assert_eq!(s.raw_type, "NVARCHAR(100)");
        assert_eq!(s.normalized_type, "VARCHAR(100)");
        assert_eq!(s.collation.as_deref(), Some("EN-CI-AS"));
        assert_eq!(t.column("OrderID").unwrap().normalized_type, "NUMBER(38,0)");
        assert_eq!(idx.by_table.len(), 5);
    }

    #[test]
    fn binding_script_yields_only_its_table() {
        let idx = DdlIndex::load(&[fixtures().join("bindings/target_deploy.sql")]);
        assert!(idx.errors.is_empty(), "{:?}", idx.errors);
        let t = &idx.tables("customer_reviews")[0];
        assert_eq!(t.database.as_deref(), Some("E2E_TARGET_DATABASE"));
        assert_eq!(t.column("review_date").unwrap().raw_type, "TIMESTAMP_NTZ");
    }

    #[test]
    fn ssis_scai_output_parses() {
        let idx = DdlIndex::load(&[fixtures().join("../snowconvert/SSIS")]);
        assert!(idx.errors.is_empty(), "{:?}", idx.errors);
        let t = &idx.tables("DimPromotion")[0];
        assert_eq!(t.column("EnglishPromotionName").unwrap().collation.as_deref(), Some("EN-CI-AS"));
        assert!(idx.by_table.len() > 10);
    }

    #[test]
    fn bad_file_is_an_error_not_a_panic() {
        let mut idx = DdlIndex::default();
        idx.add_file(Path::new("x.sql"), "USE DATABASE D;\n\nCREATE TABLE s.t (a INT,, b);\nCREATE TABLE s.u (a INT);");
        assert_eq!(idx.errors.len(), 1);
        assert_eq!(idx.errors[0].line, 3);
        assert_eq!(idx.tables("U").len(), 1);
    }

    #[test]
    fn quoted_names_and_semicolons_in_comments() {
        let mut idx = DdlIndex::default();
        idx.add_file(Path::new("x.sql"), "CREATE TABLE \"MixedCase\" (\n  \"colA\" TEXT, -- a; b\n  b INT /* ; */\n);");
        assert!(idx.errors.is_empty(), "{:?}", idx.errors);
        let t = &idx.tables("mixedcase")[0];
        assert_eq!(t.name, "MixedCase");
        assert_eq!(t.columns[0].name, "colA");
        assert!(t.columns[0].quoted);
        assert_eq!(t.columns[1].line, 3);
    }

    #[test]
    fn registry_drift_is_reported() {
        let dir = std::env::temp_dir().join(format!("dbtq-ddl-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(dir.join("snowflake/d/s/table")).unwrap();
        std::fs::create_dir_all(dir.join("registry")).unwrap();
        std::fs::write(dir.join("snowflake/d/s/table/t.sql"), "CREATE TABLE s.t (a INT);").unwrap();
        std::fs::write(
            dir.join("registry/1.json"),
            r#"{"source":{"objectType":"table"},"files":{"converted":{"path":"snowflake/d/s/table/t.sql"}},"signature":{"columns":[{"targetName":"a"},{"targetName":"b"}]}}"#,
        )
        .unwrap();
        let idx = DdlIndex::load(std::slice::from_ref(&dir));
        let _ = std::fs::remove_dir_all(&dir);
        assert_eq!(idx.errors.len(), 1, "{:?}", idx.errors);
        assert!(idx.errors[0].message.contains("registry"));
    }

    #[test]
    fn type_normalization() {
        assert!(types_compatible("NVARCHAR(100)", "varchar(100)", true));
        assert!(types_compatible("DECIMAL(18, 2)", "NUMBER(18,2)", true));
        assert!(types_compatible("INT", "BIGINT", true));
        assert!(types_compatible("TIMESTAMP_NTZ", "DATETIME", true));
        assert!(types_compatible("TIMESTAMP_NTZ", "TIMESTAMP_NTZ(3)", false));
        assert!(!types_compatible("TIMESTAMP_NTZ", "TIMESTAMP_NTZ(3)", true));
        assert!(!types_compatible("VARCHAR(10)", "VARCHAR(20)", false));
        assert!(!types_compatible("DATE", "TIMESTAMP_NTZ", false));
    }

    #[test]
    fn bindings_resolve() {
        let b = BTreeMap::from([("db".to_string(), "PROD".to_string())]);
        assert_eq!(resolve_binding("<%db%>", &b), "PROD");
        assert_eq!(resolve_binding("${db}_X", &b), "PROD_X");
    }
}
