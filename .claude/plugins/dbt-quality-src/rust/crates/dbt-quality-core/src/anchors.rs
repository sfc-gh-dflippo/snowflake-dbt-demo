//! Line and column locations for suggestions without a location.
//!
//! Derive a column only from a matched byte offset. If no anchor can be
//! resolved, use line 1 with no column.

use crate::discovery::{ModelFile, ProjectContext};
use crate::model::Suggestion;
use crate::rx;
use crate::sqlutil::line_col;

const CONFIG_CATEGORIES: &[&str] = &["MAT", "INC", "OPS"];
const YAML_CATEGORIES: &[&str] = &["TST", "DOC"];

pub fn config_position(model: &ModelFile) -> Option<(u32, u32)> {
    if let Some(m) = rx!(r"(?i)\{\{\s*config\s*\(|dbt\.config\s*\(").find(&model.raw) {
        return Some(line_col(&model.raw, m.start()));
    }
    first_statement_position(model)
}

pub fn first_statement_position(model: &ModelFile) -> Option<(u32, u32)> {
    rx!(r"(?im)^[ \t]*(with|select)\b").captures(&model.raw).map(|c| line_col(&model.raw, c.get(1).unwrap().start()))
}

fn yaml_key_position(text: &str, key: &str, start: usize) -> Option<(u32, u32)> {
    let re = regex::Regex::new(&format!(r#"(?im)^[ \t]*-[ \t]*name[ \t]*:[ \t]*["']?({})["']?[ \t]*$"#, regex::escape(key))).ok()?;
    re.captures(&text[start..]).map(|c| line_col(text, start + c.get(1).unwrap().start()))
}

fn read(project: &ProjectContext, relative: &str) -> Option<String> {
    crate::discovery::read_source(&project.root.join(relative), true).ok()
}

pub fn yaml_model_position(project: &ProjectContext, model: &str) -> Option<(u32, u32)> {
    let text = read(project, project.schema_sources.get(model)?)?;
    yaml_key_position(&text, model, 0)
}

pub fn yaml_column_position(project: &ProjectContext, model: &str, column: &str) -> Option<(u32, u32)> {
    let text = read(project, project.schema_sources.get(model)?)?;
    let re = regex::Regex::new(&format!(r#"(?im)^[ \t]*-[ \t]*name[ \t]*:[ \t]*["']?({})["']?[ \t]*$"#, regex::escape(model))).ok()?;
    let mm = re.captures(&text)?;
    let after = mm.get(0).unwrap().end();
    let end = rx!(r"(?m)^[ \t]{0,4}-[ \t]*name[ \t]*:").find(&text[after..]).map_or(text.len(), |m| after + m.start());
    yaml_key_position(&text[..end], column, after).or_else(|| Some(line_col(&text, mm.get(1).unwrap().start())))
}

pub fn project_yml_position(project: &ProjectContext, keys: &[String]) -> Option<(u32, u32)> {
    let text = read(project, "dbt_project.yml")?;
    let mut pos = 0;
    let mut found = None;
    for key in keys {
        let re = regex::Regex::new(&format!(r#"(?m)^[ \t]*["']?\+?({})["']?[ \t]*:"#, regex::escape(key))).ok()?;
        let Some(c) = re.captures(&text[pos..]) else { break };
        found = Some(line_col(&text, pos + c.get(1).unwrap().start()));
        pos += c.get(0).unwrap().end();
    }
    found
}

fn or_line_one(f: Option<(u32, u32)>) -> (u32, Option<u32>) {
    f.map_or((1, None), |(l, c)| (l, Some(c)))
}

fn model_name_for(s: &Suggestion, project: &ProjectContext) -> String {
    if let Some(n) = s.context.get("model").and_then(|v| v.as_str()).filter(|n| !n.is_empty()) {
        return n.to_string();
    }
    let declared: Vec<&String> = project.schema_sources.iter().filter(|(_, src)| **src == s.file).map(|(n, _)| n).collect();
    if declared.len() == 1 { declared[0].clone() } else { String::new() }
}

/// Best available `(line, column)` for a suggestion.
pub fn resolve_position(s: &Suggestion, project: Option<&ProjectContext>) -> (u32, Option<u32>) {
    if s.column.is_some() {
        return (s.line.filter(|l| *l != 0).unwrap_or(1), s.column);
    }
    if let Some(l) = s.line.filter(|l| *l != 0) {
        return (l, None);
    }
    let Some(project) = project else { return (1, None) };
    if s.file.is_empty() {
        return (1, None);
    }
    let target = &s.file;
    if target.ends_with(".yml") || target.ends_with(".yaml") {
        if target.ends_with("dbt_project.yml") {
            let keys: Vec<String> = match s.context.get("yaml_keys") {
                Some(serde_json::Value::String(k)) => vec![k.clone()],
                Some(serde_json::Value::Array(a)) if !a.is_empty() => a.iter().map(crate::sqlutil::py_str).collect(),
                _ => vec!["models".into()],
            };
            return or_line_one(project_yml_position(project, &keys));
        }
        let model = model_name_for(s, project);
        if !model.is_empty() {
            if let Some(col) = s.context.get("column_name").and_then(|v| v.as_str()).filter(|c| !c.is_empty()) {
                return or_line_one(yaml_column_position(project, &model, col));
            }
            return or_line_one(yaml_model_position(project, &model));
        }
        return (1, None);
    }
    let Some(model) = project.models.iter().find(|m| &m.relative_path == target) else { return (1, None) };
    if YAML_CATEGORIES.contains(&s.category.as_str()) || CONFIG_CATEGORIES.contains(&s.category.as_str()) {
        return or_line_one(config_position(model));
    }
    or_line_one(first_statement_position(model))
}
