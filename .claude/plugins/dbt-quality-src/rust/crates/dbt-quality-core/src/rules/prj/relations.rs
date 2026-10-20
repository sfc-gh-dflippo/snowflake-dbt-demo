//! Relation read classification shared by project and literal SQL rules.
use std::collections::{BTreeMap, BTreeSet};

use serde_json::json;

use super::shared::*;
use crate::discovery::{root_relative, source_decls, PortfolioContext, ProjectContext};
use crate::model::{effort, Suggestion};
use crate::rx;
use crate::sqlutil::{extract_ctes, line_col, region_at, sql_regions};

pub const LOCATION_FIX: &str = "Remove the location-variable uses. Keep declarations needed by remaining value reads. Use a literal database for one environment, or a target.name if/elif expression with an else branch of invalid_database; keep schema literal. Use the targets already defined in profiles.yml (otherwise dev, qa and prod are examples to fill in). Get real per-target database and schema values from the owner or original connection; an empty or placeholder default is not a real location (PRJ0013 owns self-named defaults). Any old key passed through --vars no longer affects these location uses; it may still supply remaining value reads. Check that the target orchestration already uses maps to the right database; no orchestration change is needed.";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Form { Var, Literal, Source, This }

#[derive(Debug, Clone)]
pub struct Read {
    pub project: usize,
    pub model: Option<usize>,
    pub file: String,
    pub line: u32,
    pub table: String,
    pub location: Location,
    pub form: Form,
    pub stage: bool,
    pub stage_suffix: Option<String>,
    pub vars: Vec<String>,
    pub writers: Vec<Node>,
    pub candidates: Vec<Node>,
    pub cycle: Vec<Node>,
    pub provisional: bool,
}

fn part(value: Part) -> LocPart {
    LocPart { value, var: None, raw: None, quoted: false }
}

fn relation_parts(raw: &str) -> Option<Vec<&str>> {
    let raw = raw.trim();
    let names: Vec<_> = rx!(r#""(?:[^"]|"")+"|[A-Za-z_][A-Za-z0-9_$]*"#).find_iter(raw).collect();
    let mut end = 0;
    for (index, name) in names.iter().enumerate() {
        if raw[end..name.start()] != *if index == 0 { "" } else { "." } { return None; }
        end = name.end();
    }
    (end == raw.len() && !names.is_empty()).then(|| names.into_iter().map(|name| name.as_str()).collect())
}

fn invalid_location(raw: &str) -> Location {
    let unknown = || part(Part::Unknown(format!("invalid relation location `{raw}`; expected one to three identifier parts")));
    Location { database: unknown(), schema: unknown(), identifier: unknown() }
}

pub fn read_location(p: &ProjectContext, parts: &[RelPart]) -> Location {
    let mut resolved = vec![];
    for item in parts {
        match item {
            RelPart::Ident(s) => resolved.push(resolve_part(p, Some(s), Part::Target, None)),
            RelPart::Var { key, default } => {
                let loc = resolve_var_part(p, key, default.as_deref());
                if let Some(raw) = loc.raw.as_deref().filter(|_| matches!(loc.value, Part::Known(_))) {
                    let Some(names) = relation_parts(raw) else {
                        return invalid_location(raw);
                    };
                    for name in names {
                        let mut resolved_part = resolve_part(p, Some(name), Part::Target, None);
                        resolved_part.var = Some(key.clone());
                        resolved.push(resolved_part);
                    }
                } else {
                    resolved.push(loc);
                }
            }
        }
    }
    if resolved.len() > 3 {
        let raw = resolved.iter().map(|loc| loc.raw.as_deref().unwrap_or("<unresolved>")).collect::<Vec<_>>().join(".");
        return invalid_location(&raw);
    }
    let unknown = || part(Part::Unknown("relation location is incomplete".into()));
    let identifier = resolved.pop().unwrap_or_else(unknown);
    let schema = resolved.pop().unwrap_or_else(|| part(Part::Target));
    let database = resolved.pop().unwrap_or_else(|| part(Part::Target));
    Location { database, schema, identifier }
}

fn relation_keyword_offsets(sql: &str) -> BTreeSet<usize> {
    let regions = sql_regions(sql);
    let mut query_scopes = vec![true];
    let mut offsets = BTreeSet::new();
    for token in rx!(r#""(?:[^"]|"")*"|\$\$[\s\S]*?\$\$|[A-Za-z_][A-Za-z0-9_$]*|[();]"#).find_iter(sql) {
        if region_at(&regions, token.start()).is_some() { continue; }
        match token.as_str().to_ascii_lowercase().as_str() {
            "(" => query_scopes.push(false),
            ")" if query_scopes.len() > 1 => { query_scopes.pop(); }
            ";" => { query_scopes = vec![true]; }
            "select" | "delete" | "merge" | "update" | "copy" => { *query_scopes.last_mut().unwrap() = true; }
            "from" | "join" | "using" if *query_scopes.last().unwrap() => { offsets.insert(token.start()); }
            _ => {}
        }
    }
    offsets
}

pub fn literal_reads(text: &str) -> Vec<VarRelationRead> {
    let Some(sql_body) = crate::jinja::try_blank_jinja(text) else { return vec![]; };
    let relation_keywords = relation_keyword_offsets(&sql_body);
    let regions = sql_regions(text);
    let configs = super::shared::config_ranges(text);
    let var_reads = var_relation_reads(text);
    let ctes: BTreeSet<_> = extract_ctes(text).into_iter().map(|c| c.name.to_lowercase()).collect();
    let mut out = vec![];
    for c in rx!(r#"(?i)\b(?:from|join|using)\s+(@?(?:"(?:[^"\n]|"")+"|[A-Za-z_][A-Za-z0-9_$]*)(?:\.(?:"(?:[^"\n]|"")+"|[A-Za-z_][A-Za-z0-9_$]*))*(?:/[^\s'"),;]*)?)"#).captures_iter(text) {
        let m = c.get(1).unwrap();
        let start = c.get(0).unwrap().start();
        if !relation_keywords.contains(&start) || sql_body[start..m.end()] != text[start..m.end()] { continue; }
        if region_at(&regions, m.start()).is_some() || configs.iter().any(|&(a,b)| a <= m.start() && m.start() < b) || var_reads.iter().any(|r| r.start <= m.start() && m.start() < r.end) { continue; }
        let stage = m.as_str().starts_with('@');
        let body = m.as_str().trim_start_matches('@').split('/').next().unwrap();
        if ctes.contains(&body.to_lowercase()) { continue; }
        if rx!(r"(?i)^snowflake\.(account_usage|organization_usage)|\.information_schema\b|^information_schema\b|^(table|lateral|values)\.").is_match(body) { continue; }
        let Some(names) = relation_parts(body) else { continue; };
        let parts = names.into_iter().map(|name| RelPart::Ident(name.into())).collect();
        out.push(VarRelationRead { match_start: start, start: m.start(), end: m.end(), line: line_col(text, m.start()).0, parts, stage, text: m.as_str().into() });
    }
    out
}

fn reads(pf: &PortfolioContext) -> Vec<Read> {
    let mut out = vec![];
    for (pi, p) in pf.projects.iter().enumerate() {
        for src in super::project_sources(p).into_iter().filter(|s| !s.yaml) {
            let model = p.models.iter().position(|m| m.relative_path == src.file && !m.is_python);
            for (form, tokens) in [(Form::Var, var_relation_reads(&src.text)), (Form::Literal, literal_reads(&src.text))] {
                for token in tokens {
                    let location = read_location(p, &token.parts);
                    let table = location.identifier.key().unwrap_or_else(|| token.table().unwrap_or("<unresolved table>").to_string());
                    out.push(Read { project: pi, model, file: src.file.clone(), line: token.line, table, location, form, stage: token.stage, stage_suffix: token.stage_suffix().map(String::from), vars: token.vars().into_iter().map(String::from).collect(), writers: vec![], candidates: vec![], cycle: vec![], provisional: false });
                }
            }
        }
        let decls = source_decls(p);
        for call in call_sites(p).into_iter().filter(|c| c.kind == CallKind::Source) {
            let matches: Vec<_> = decls.iter().flat_map(|d| d.tables.iter().filter(|t| d.name == call.name && Some(&t.name) == call.table.as_ref()).map(move |t| (d,t))).collect();
            if let [(decl, table)] = matches.as_slice() {
                let location = resolve_location(p, decl, table);
                out.push(Read { project: pi, model: call.model, file: call.file, line: call.line, table: location.identifier.key().unwrap_or_else(|| table.name.clone()), location, form: Form::Source, stage: false, stage_suffix: None, vars: vec![], writers: vec![], candidates: vec![], cycle: vec![], provisional: false });
            }
        }
        for (mi, m) in p.models.iter().enumerate().filter(|(_,m)| !m.is_python) {
            let regions = sql_regions(&m.raw);
            for (span, guarded) in &m.jinja.this_reads {
                let start = span.start_offset as usize;
                if region_at(&regions, start).is_some() || (*guarded && m.materialization() == "incremental") { continue; }
                if let Some(rel) = model_relation(p,m) {
                    out.push(Read { project: pi, model: Some(mi), file: m.relative_path.clone(), line: m.line_of(start), table: rel.location.identifier.key().unwrap_or_else(|| m.name.clone()), location: rel.location, form: Form::This, stage: false, stage_suffix: None, vars: vec![], writers: vec![(pi,mi)], candidates: vec![], cycle: vec![(pi,mi)], provisional: false });
                }
            }
        }
    }
    out
}

pub fn analyze(pf: &PortfolioContext) -> Vec<Read> {
    let mut reads = reads(pf);
    let index = producers(pf);
    let mut graph = RefGraph::build(pf, true);
    let existing_refs = RefGraph::build(pf, true);
    for read in &mut reads {
        if read.stage || read.form == Form::This || matches!(read.location.identifier.value, Part::Unknown(_)) { continue; }
        for &node in index.get(&read.table).into_iter().flatten() {
            let relation = model_relation(&pf.projects[node.0], &pf.projects[node.0].models[node.1]).unwrap();
            match compare_locations(&[&read.location, &relation.physical], node.0 == read.project) {
                LocationMatch::Equal => read.writers.push(node),
                LocationMatch::IdenticalPlaceholder => { read.writers.push(node); read.provisional = true; }
                LocationMatch::Unresolved(_) => read.candidates.push(node),
                LocationMatch::Different(_) => {}
            }
        }
        // Converter annotations establish intended self-identity, not a resolved physical location.
        if read.writers.is_empty() && let Some(mi) = read.model {
            let model = &pf.projects[read.project].models[mi];
            let marker = format!("'{}'", read.table);
            let declared_self = model.raw.lines().any(|line| line.starts_with("--") && line.contains(&marker) && (line.contains("Self-referencing table") || line.contains("USED AS BOTH SOURCE AND TARGET")));
            if declared_self {
                read.writers = read.candidates.iter().copied().filter(|&node| node.0 == read.project && (node == (read.project, mi) || existing_refs.path(node, (read.project, mi)).is_some())).collect();
                read.provisional = !read.writers.is_empty();
            }
        }
        if read.writers.len() == 1 && let Some(mi) = read.model {
            graph.upstream.entry((read.project,mi)).or_default().insert(read.writers[0]);
        }
    }
    for read in &mut reads {
        if let Some(mi) = read.model {
            for &node in &read.writers {
                let path = if node == (read.project,mi) { Some(vec![node]) } else if read.provisional { existing_refs.path(node, (read.project,mi)) } else { graph.path(node, (read.project,mi)) };
                if let Some(path) = path { read.cycle = path; break; }
            }
        }
    }
    reads
}

pub fn source_advice(p: &ProjectContext, loc: &Location, table: &str, stage_suffix: Option<&str>) -> String {
    let db = loc.database.known();
    let schema = loc.schema.known().unwrap_or("<real_schema>");
    let block = db.map_or_else(|| "<schema_or_db_schema>".into(), |db| source_block_for(db, schema, &project_locations(p)));
    let file = source_decls(p).into_iter().find(|d| {
        let other = resolve_source_location(p,d);
        other.database.known() == db && db.is_some() && other.schema.known() == loc.schema.known()
    }).map_or_else(|| root_relative(p,"models/sources.yml"), |d| root_relative(p,&d.file));
    let (targets, found) = target_values(p, db);
    let identifier = loc.identifier.known().unwrap_or(table);
    let table = logical_identifier(identifier);
    let mut yaml = render_source_location(&block, schema, &targets, [loc.database.quoted, loc.schema.quoted, loc.identifier.quoted]);
    yaml.push_str(&format!("    tables:\n      - name: {}\n        identifier: {}\n", yaml_scalar(&table), yaml_scalar(&template_literal(identifier))));
    if let Some(suffix) = stage_suffix {
        let stage = |db: &str| template_literal(&format!("@{}.{}.{}{suffix}", sql_identifier(db, loc.database.quoted), sql_identifier(schema, loc.schema.quoted), sql_identifier(identifier, loc.identifier.quoted)));
        yaml.push_str("        external:\n          location: |-\n");
        match targets.as_slice() {
            [(_, db)] => yaml.push_str(&format!("            {}\n", stage(db))),
            _ => {
                for (index, (target, db)) in targets.iter().enumerate() {
                    let keyword = if index == 0 { "if" } else { "elif" };
                    yaml.push_str(&format!("            {{%- {keyword} target.name == {} -%}} {}\n", serde_json::to_string(target).unwrap(), stage(db)));
                }
                yaml.push_str(&format!("            {{%- else -%}} {}\n            {{%- endif -%}}\n", stage("invalid_database")));
            }
        }
        yaml.push_str("          file_format: '<owner-provided file format>'\n");
    }
    let stage_check = if stage_suffix.is_some() { "Before changing this stage read, confirm its lifetime and location with the owner. A session-local temporary stage populated by PUT is not automatically interchangeable with a persistent external-table source; retain that workflow unless a compatible storage and lifecycle migration is confirmed. Only after that confirmation, use the following source example. " } else { "" };
    let mut advice = format!("{stage_check}In `{file}`, use one source block per database.schema, named `{block}`, and read `{{{{ source('{block}', '{table}') }}}}`. Do not append to a placeholder raw block unless it is renamed to this same location. {LOCATION_FIX}\n```yaml\n{yaml}```");
    if !found { advice.push_str(" The dev/qa/prod target names are examples; fill in the real profile targets and their databases."); }
    if stage_suffix.is_some() {
        advice.push_str(" Declare an external-table source for the stage (preserve any path suffix). Add to packages.yml:\n```yaml\npackages:\n  - package: dbt-labs/dbt_external_tables\n    version: '<compatible pinned version>'\n```\nRun `dbt deps` then `dbt run-operation stage_external_sources` before querying the source. Set the external location consistently with the already-selected target database. Package compatibility with native EXECUTE DBT PROJECT remains unverified; validate it in the actual runtime before adopting this change.");
    }
    advice
}

#[cfg(test)]
#[path = "relation_tests.rs"]
mod tests;

pub fn enforce_ownership(all: &mut Vec<Suggestion>, pf: &PortfolioContext) {
    let cycle_sites: BTreeSet<(String, String)> = all.iter().filter(|s| s.rule_id.ends_with("PRJ0022")).flat_map(|s| {
        s.context.get("read_sites").and_then(|v| v.as_array()).into_iter().flatten().filter_map(|v| v.as_str()).map(|site| (s.project.clone(),site.to_string()))
    }).collect();
    all.retain(|s| {
        if !s.rule_id.ends_with("SQL0006") { return true; }
        let file = pf.projects.iter().find(|p| p.label == s.project).map_or_else(|| s.file.clone(), |p| root_relative(p,&s.file));
        !cycle_sites.contains(&(s.project.clone(),format!("{file}:{}",s.line.unwrap_or(1))))
    });
}

fn path(pf: &PortfolioContext, node: Node) -> String { root_relative(&pf.projects[node.0], &pf.projects[node.0].models[node.1].relative_path) }

fn read_label(p: &ProjectContext, read: &Read) -> String {
    let location = [&read.location.database, &read.location.schema, &read.location.identifier].into_iter().map(|loc| {
        match &loc.value {
            Part::Known(value) | Part::Placeholder(value) if loc.quoted => format!("\"{}\"", value.replace('"', "\"\"")),
            Part::Known(value) | Part::Placeholder(value) => value.clone(),
            Part::Target => "<target>".into(),
            Part::Unknown(reason) => format!("<unresolved: {reason}>"),
        }
    }).collect::<Vec<_>>().join(".");
    format!("{}:{} ({}{location}{})", root_relative(p,&read.file), read.line, if read.stage { "@" } else { "" }, read.stage_suffix.as_deref().unwrap_or(""))
}

pub fn findings(pf: &PortfolioContext, cycles: bool) -> Vec<Suggestion> {
    let reads = analyze(pf);
    let owned_lines: BTreeSet<_> = reads.iter().filter(|r| !r.cycle.is_empty()).map(|r| (r.project,r.file.clone(),r.line)).collect();
    let mut groups: BTreeMap<(usize,String),Vec<&Read>> = BTreeMap::new();
    for read in &reads {
        let owned = if cycles { !read.cycle.is_empty() } else {
            !owned_lines.contains(&(read.project, read.file.clone(),read.line)) && (read.form == Form::Var || (read.stage && read.model.is_none()) || (read.form == Form::Source && !read.writers.is_empty()))
        };
        if owned { groups.entry((read.project,read.table.clone())).or_default().push(read); }
    }
    groups.into_iter().map(|((pi,table), group)| {
        let p = &pf.projects[pi];
        let first = group[0];
        let sites: Vec<_> = group.iter().map(|r| format!("{}:{}", root_relative(p,&r.file), r.line)).collect();
        let nodes: BTreeSet<_> = group.iter().flat_map(|r| r.writers.iter().chain(&r.candidates).copied()).collect();
        let paths: Vec<_> = nodes.iter().map(|&n| path(pf,n)).collect();
        let proofs: Vec<_> = group.iter().filter(|r| !r.cycle.is_empty()).map(|r| {
            r.cycle.windows(2).map(|edge| {
                let p = &pf.projects[edge[0].0];
                let target = &pf.projects[edge[1].0].models[edge[1].1];
                let sites = call_sites(p).into_iter().filter(|c| c.model == Some(edge[0].1) && c.kind == CallKind::Ref && c.name == target.name).map(|c| c.site).collect::<Vec<_>>();
                format!("{} -> {} ({})", path(pf,edge[0]),path(pf,edge[1]), if sites.is_empty() { "proposed relation-read edge".into() } else { sites.join(", ") })
            }).collect::<Vec<_>>().join("; ")
        }).collect();
        let proof = if cycles { format!(" Dependency proof: {}.", if proofs.iter().all(String::is_empty) { "reader is its own producer".into() } else { proofs.join("; ") }) } else { String::new() };
        let mut classes = BTreeSet::new();
        let mut advice = vec![];
        let mut location_fix = false;
        for read in &group {
            let text = if cycles {
                classes.insert("cycle");
                let node = read.cycle[0];
                let model = &pf.projects[node.0].models[node.1];
                let chain = read.cycle.iter().map(|&n| path(pf,n)).collect::<Vec<_>>().join(" -> ");
                let convert = if model.materialization() == "table" { " Convert materialized='table' to materialized='incremental'." } else { " Use incremental materialization for prior-state reads." };
                let cross = read.cycle.iter().any(|n| n.0 != pi);
                let separate = if cross { format!(" This cycle includes proposed relation-read edges on the merged graph. While the projects stay separate, read the other project's table through a source: {} Once merged, relocate the logic as follows.", source_advice(p,&read.location,&table,None)) } else { String::new() };
                format!("Read {}:{} closes the dependency chain (existing refs and proposed relation-read edges): {chain}.{separate} Move this read and all SQL depending on it downstream into `{}`, refactoring it into a CTE. Read `{{{{ this }}}}` there only inside `{{% if is_incremental() %}} ... {{% else %}} ... {{% endif %}}`. The non-incremental/full-refresh branch must have no prior state: use an empty CTE with the same typed columns (`select ... where false`) or skip the join. Remove the staging self-read and any source entry pointing at the producer's own table; neither a new dependency edge nor an external source is the fix for that own-table read.{convert} Choose unique_key and incremental_strategy from the original mapping's update strategy and target load settings: update/upsert uses merge; truncate-and-reload that needs prior state needs a full overwrite while still incremental. The vendored Fusion adapter and inspected Python dbt-snowflake adapter revision support insert_overwrite for whole-table replacement, not partition replacement; verify the installed adapter version before selecting that strategy.", root_relative(p,&read.file), read.line, path(pf,node))
            } else if read.stage {
                classes.insert("stage"); source_advice(p,&read.location,&table,read.stage_suffix.as_deref())
            } else if read.writers.len() > 1 {
                classes.insert("multiwriter"); "Several models write this relation; resolve the PRJ0020 multi-writer finding before replacing these reads. Do not choose an arbitrary writer.".into()
            } else if let Some(&node) = read.writers.first() {
                if node.0 == pi {
                    classes.insert("same_project"); format!("Read `{{{{ ref('{}') }}}}` from producer `{}`. Remove any source entry for that model-owned relation.",pf.projects[node.0].models[node.1].name,path(pf,node))
                } else {
                    classes.insert("cross_project"); format!("After the merge, read `{{{{ ref('{}') }}}}` from `{}`; the merged dependency graph was checked for cycles. While separate: {}",pf.projects[node.0].models[node.1].name,path(pf,node),source_advice(p,&read.location,&table,None))
                }
            } else if !read.candidates.is_empty() {
                classes.insert("unresolved"); format!("The identifier matches candidate producers, but database/schema equality is unresolved; do not choose a producer from the table name alone. {LOCATION_CHECK} If equality is confirmed, check the ref graph including proposed relation edges; use the same-project producer's ref or a ref after merging projects only if acyclic, and PRJ0022 relocation if cyclic. Several confirmed writers belong to PRJ0020. Otherwise, or while projects remain separate: {}",source_advice(p,&read.location,&table,None))
            } else {
                classes.insert("external"); source_advice(p,&read.location,&table,None)
            };
            location_fix |= text.contains(LOCATION_FIX);
            advice.push(format!("Read {}: {}", read_label(p, read), text.replace(LOCATION_FIX, "")));
        }
        let caveat = if group.iter().any(|r| r.provisional) { format!(" Physical locations are not proven: identical generated placeholders or an explicit converter self-read annotation establish only generated intent. Recheck the real locations before editing; if they differ this is not a producer match. {LOCATION_CHECK}") } else { String::new() };
        let vars: BTreeSet<_> = group.iter().flat_map(|r| r.vars.iter().cloned()).collect();
        let var_note = if vars.is_empty() { String::new() } else { format!(" Remove location variables {} from these reads entirely. An undeclared variable with no default goes away with the read, so dbt no longer fails on it here; PRJ0016 still owns any remaining non-relation read.",vars.iter().cloned().collect::<Vec<_>>().join(", ")) };
        let location_note = if location_fix || !vars.is_empty() { format!("\n{LOCATION_FIX}") } else { String::new() };
        Suggestion::new(if cycles { "SSC-EWI-DBTPRJ0022" } else { "SSC-EWI-DBTPRJ0021" },format!("`{table}`: {} relation read(s), class {}: {}. Producer paths (candidates where unresolved): {}.{proof}{caveat}",group.len(),classes.iter().copied().collect::<Vec<_>>().join("/"),sites.join(", "),if paths.is_empty() { "none found".into() } else { paths.join(", ") }))
            .in_project(p).file(&first.file).line(first.line).evidence(sites.join(" / "))
            .remediation(format!("Change all {} reads of `{table}` at {}.\n{}{var_note}{location_note}{caveat}",group.len(),sites.join(", "),advice.join("\n")))
            .effort(effort::MEDIUM).ctx("table",json!(table)).ctx("class",json!(classes.iter().copied().collect::<Vec<_>>().join("/"))).ctx("read_sites",json!(sites)).ctx("producer_files",json!(paths)).ctx("vars",json!(vars))
    }).collect()
}
