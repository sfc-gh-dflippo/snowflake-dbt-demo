//! Spikes S3/S4: parse every fixture template and lex it as Snowflake SQL.
use dbt_quality_core::jinja::{blank_jinja, summarize};
use dbt_sql_utils::tokens::sql_lex_tokens;

fn walk(dir: &std::path::Path, out: &mut Vec<std::path::PathBuf>) {
    for e in std::fs::read_dir(dir).unwrap().flatten() {
        let p = e.path();
        let n = p.file_name().unwrap().to_string_lossy().to_string();
        if p.is_dir() && !["target", "dbt_packages", "logs"].contains(&n.as_str()) {
            walk(&p, out);
        } else if n.ends_with(".sql") {
            out.push(p);
        }
    }
}

fn main() {
    let root = std::env::args().nth(1).expect("root");
    let mut files = vec![];
    walk(root.as_ref(), &mut files);
    let (mut bad_j, mut bad_l, mut calls) = (0, 0, 0);
    for f in &files {
        let src = std::fs::read_to_string(f).unwrap();
        let s = summarize(&src, &f.to_string_lossy());
        if let Some(e) = &s.parse_error {
            bad_j += 1;
            eprintln!("JINJA {}: {e}", f.display());
        }
        calls += s.calls.len();
        // Lex the SQL with Jinja blanked to spaces (keeps offsets).
        let blanked = blank_jinja(&src);
        match sql_lex_tokens(&blanked, dbt_frontend_common::Dialect::Snowflake) {
            Some(t) => { let _ = t.len(); }
            None => { bad_l += 1; eprintln!("LEX {}", f.display()); }
        }
    }
    println!("files={} jinja_errors={bad_j} lex_failures={bad_l} calls={calls}", files.len());
}

