//! SQL rules: query construction and shape.

use std::collections::BTreeMap;
use indexmap::IndexMap;

use serde_json::json;

use crate::discovery::{ModelFile, PortfolioContext, ProjectContext};
use crate::engine::{Detect, Detector};
use crate::model::{effort, plural_irregular, Suggestion};
use crate::sqlutil::*;
use crate::waivers::is_waived;
use std::ops::Not;
use crate::{frx, rx};

pub const DETECTORS: &[Detector] = &[
    Detector { code: "SSC-EWI-DBTSQL0001", detect: Detect::Project(sql0001) },
    Detector { code: "SSC-EWI-DBTSQL0002", detect: Detect::Portfolio(sql0002_estate) },
    Detector { code: "SSC-EWI-DBTSQL0003", detect: Detect::Model(sql0003) },
    Detector { code: "SSC-EWI-DBTSQL0004", detect: Detect::Model(sql0004) },
    Detector { code: "SSC-EWI-DBTSQL0005", detect: Detect::Model(sql0005) },
    Detector { code: "SSC-EWI-DBTSQL0006", detect: Detect::Model(sql0006) },
    Detector { code: "SSC-EWI-DBTSQL0007", detect: Detect::Model(sql0007) },
    Detector { code: "SSC-FDM-DBTSQL0008", detect: Detect::Model(sql0008) },
    Detector { code: "SSC-EWI-DBTSQL0009", detect: Detect::Model(sql0009) },
    Detector { code: "SSC-EWI-DBTSQL0010", detect: Detect::Model(sql0010) },
    Detector { code: "SSC-EWI-DBTSQL0011", detect: Detect::Model(sql0011) },
    Detector { code: "SSC-EWI-DBTSQL0012", detect: Detect::Model(sql0012) },
    Detector { code: "SSC-EWI-DBTSQL0013", detect: Detect::Model(sql0013) },
    Detector { code: "SSC-EWI-DBTSQL0014", detect: Detect::Model(sql0014) },
];

/// Minimum normalised length for a subquery to be worth reporting.
const MIN_SUBQUERY_LENGTH: usize = 60;

fn window_fn() -> &'static regex::Regex {
    rx!(r"(?i)\b(row_number|rank|dense_rank|ntile|lag|lead|first_value|last_value)\s*\(")
}

/// Stripped text from `start`, at most `len` bytes, cut on a char boundary.
fn slice_from(s: &str, start: usize, len: usize) -> &str {
    let a = floor_char(s, start);
    let b = floor_char(s, a.saturating_add(len));
    &s[a..b]
}

/// Cut `s` to at most `n` chars at a whitespace boundary. Never end inside a
/// `{{ ... }}` call. Append ` ...` when text is removed.
fn token_cut(s: &str, n: usize) -> String {
    if s.chars().count() <= n {
        return s.to_string();
    }
    let mut cut: String = s.chars().take(n).collect();
    if let Some(i) = cut.rfind(' ') {
        cut.truncate(i);
    }
    if let (Some(o), c) = (cut.rfind("{{"), cut.rfind("}}"))
        && c.is_none_or(|c| c < o) {
            cut.truncate(o);
        }
    format!("{} ...", cut.trim_end())
}

fn sql0001(project: &ProjectContext) -> Vec<Suggestion> {
    struct Hit<'a> {
        model: &'a ModelFile,
        sq: Subquery,
    }
    let mut occ: BTreeMap<String, Vec<Hit>> = BTreeMap::new();
    for model in &project.models {
        if model.is_python {
            continue;
        }
        for sq in find_derived_subqueries(&model.stripped) {
            if normalize_sql(&sq.body).chars().count() < MIN_SUBQUERY_LENGTH {
                continue;
            }
            occ.entry(fingerprint(&sq.body)).or_default().push(Hit { model, sq });
        }
    }
    let mut out = vec![];
    for (digest, hits) in &occ {
        let mut names: Vec<String> = hits.iter().map(|h| h.model.name.clone()).collect();
        names.sort();
        names.dedup();
        let reused = names.len() > 1;
        // One finding per (fingerprint, file): repeats in one model are one edit.
        let mut by_file: IndexMap<&str, Vec<&Hit>> = IndexMap::new();
        for h in hits {
            by_file.entry(h.model.relative_path.as_str()).or_default().push(h);
        }
        for group in by_file.values() {
            let h = group[0];
            let (m, sq) = (h.model, &h.sq);
            let sites: Vec<u32> = group.iter().map(|g| find_line_number(&g.model.stripped, g.sq.start)).collect();
            let times = if sites.len() > 1 {
                format!(" It occurs {} times in this model (lines {}); lift it once and reference it each time.", sites.len(), sites.iter().map(|l| l.to_string()).collect::<Vec<_>>().join(", "))
            } else {
                String::new()
            };
            let evidence = format!("{} ( {} )", sq.keyword, token_cut(&raw_span_limit(&m.raw, sq.open + 1, sq.close, usize::MAX), 200));
            let base = |msg: String| {
                Suggestion::new("SSC-EWI-DBTSQL0001", msg)
                    .file(&m.relative_path)
                    .span(span(&m.stripped, sq.start, sq.end))
                    .evidence(evidence.clone())
                    .project(&project.name)
                    .ctx("fingerprint", digest.as_str())
                    .ctx("sites", json!(sites))
            };
            if reused {
                let others: Vec<&String> = names.iter().filter(|n| **n != m.name).collect();
                out.push(
                    base(format!(
                        "The same subquery body appears in {} models: {}.{times}",
                        names.len(),
                        names.join(", ")
                    ))
                    .remediation(
                        "Extract this into an ephemeral model so there is one definition \
and dbt tracks the dependency:\n\n```sql\n-- models/silver/int_<describe_the_logic>.sql\n\
{{ config(materialized='ephemeral') }}\n<the subquery body>\n```\n\nThen replace each \
subquery with `{{ ref('int_<describe_the_logic>') }}`. Ephemeral materializes as a CTE at \
compile time, adding no extra relation. Consider storing the result when measured repeated work justifies the refresh and storage costs; the local reuse threshold is not an execution-count guarantee.",
                    )
                    .effort(effort::MEDIUM)
                    .ctx("also_in", json!(others))
                    .ctx("reuse_count", names.len()),
                );
            } else {
                out.push(
                    base(format!("This model has an inline derived-table subquery in `{}`. Move it into a named CTE.{times}", sq.keyword))
                        .remediation(
                            "Lift it into a named CTE so the step is self-describing:\n\n\
```sql\nwith <descriptive_name> as (\n    <the subquery body>\n)\nselect ... from \
<descriptive_name>\n```\n\nName it for what it produces, not for its position. Consider a separate model when reuse, testing, or ownership warrants that boundary; ephemeral is one materialization option.",
                        )
                        .effort(effort::LOW)
                        .ctx("reuse_count", 1),
                );
            }
        }
    }
    out
}

/// Keep the per-project findings and add the cross-project comparison.
fn sql0002_estate(p: &PortfolioContext) -> Vec<Suggestion> {
    let mut out = vec![];
    for project in &p.projects {
        for s in sql0002(project) {
            let s = s.in_project(project);
            if !is_waived(&s, Some(project), Some(&p.config)) {
                out.push(s);
            }
        }
    }
    let min_lines = p.config.duplicate_block_min_lines;
    // PRJ0020 tells the agent to delete these identical copies, so their CTEs
    // are not a second, shared-logic finding here.
    let deleted: std::collections::BTreeSet<(usize, usize)> = crate::rules::prj::model_dup_groups(p)
        .into_iter()
        .filter(|g| g.class == crate::rules::prj::DupClass::Consolidate)
        .flat_map(|g| g.members.into_iter().skip(1))
        .collect();
    let mut groups: BTreeMap<String, Vec<(&ProjectContext, &ModelFile, Cte)>> = BTreeMap::new();
    for (pi, project) in p.projects.iter().enumerate() {
        for (mi, model) in project.models.iter().enumerate().filter(|(_, m)| !m.is_python) {
            if deleted.contains(&(pi, mi)) {
                continue;
            }
            for cte in extract_ctes(&model.stripped) {
                if (significant_lines(&cte.body) as i64) >= min_lines {
                    groups.entry(fingerprint(&cte.body)).or_default().push((project, model, cte));
                }
            }
        }
    }
    for (digest, hits) in &groups {
        let mut labels: Vec<String> = hits.iter().map(|(p, m, _)| format!("{}:{}", p.label, m.name)).collect();
        labels.sort();
        labels.dedup();
        let projects: std::collections::BTreeSet<&str> = hits.iter().map(|(p, _, _)| p.label.as_str()).collect();
        if projects.len() < 2 {
            continue;
        }
        for (project, m, cte) in hits {
            let related: Vec<String> = hits
                .iter()
                .filter(|(op, o, _)| !(op.label == project.label && o.relative_path == m.relative_path))
                .map(|(op, o, c)| {
                    format!("{}/{}:{}", op.label, o.relative_path, find_line_number(&o.stripped, c.start))
                })
                .collect();
            let mine = format!("{}:{}", project.label, m.name);
            let others: Vec<&str> =
                labels.iter().filter(|l| **l != mine).map(String::as_str).collect();
            let s = Suggestion::new(
                "SSC-EWI-DBTSQL0002",
                format!(
                    "CTE `{}` has the same normalized body as a CTE in {} across {} projects: {}.",
                    cte.name,
                    plural_irregular(others.len(), "other model", "other models"),
                    projects.len(),
                    others.join(", ")
                ),
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, cte.start, cte.end))
            .evidence(raw_span(&m.stripped, cte.start, cte.start + cte.body.len()))
            .remediation(
                "Confirm shared meaning and ownership first. Consider a shared package macro for parameterized expressions, or a model with a suitable materialization for a shared dataset. Verify supported cross-project dependency configuration before using refs between projects; do not assume a cross-project ephemeral model can be reused in every runtime.",
            )
            .effort(effort::MEDIUM)
            .in_project(project)
            .ctx("fingerprint", digest.as_str())
            .ctx("repeated_in", json!(labels))
            .ctx("cross_project", json!(true))
            .ctx("projects", json!(projects))
            .ctx("related_files", json!(related));
            if !is_waived(&s, Some(project), Some(&p.config)) {
                out.push(s);
            }
        }
    }
    out
}

fn sql0002(project: &ProjectContext) -> Vec<Suggestion> {
    let threshold = project.config.duplicate_block_threshold;
    let min_lines = project.config.duplicate_block_min_lines;
    let mut groups: BTreeMap<String, Vec<(&ModelFile, Cte)>> = BTreeMap::new();
    for model in &project.models {
        if model.is_python {
            continue;
        }
        for cte in extract_ctes(&model.stripped) {
            if (significant_lines(&cte.body) as i64) < min_lines {
                continue;
            }
            groups.entry(fingerprint(&cte.body)).or_default().push((model, cte));
        }
    }
    let mut out = vec![];
    for (digest, hits) in &groups {
        let mut names: Vec<String> = hits.iter().map(|(m, _)| m.name.clone()).collect();
        names.sort();
        names.dedup();
        if names.len() < 2 {
            continue;
        }
        let target = if names.len() as i64 >= threshold { "a macro" } else { "an ephemeral model" };
        for (m, cte) in hits {
            let others: Vec<&str> =
                names.iter().filter(|n| **n != m.name).map(|n| n.as_str()).collect();
            let related: Vec<String> = hits
                .iter()
                .filter(|(o, _)| o.relative_path != m.relative_path)
                .map(|(o, c)| format!("{}:{}", o.relative_path, find_line_number(&o.stripped, c.start)))
                .collect();
            out.push(
                Suggestion::new(
                    "SSC-EWI-DBTSQL0002",
                    format!(
                        "CTE `{}` has the same normalized body as a CTE in {}: {}.",
                        cte.name,
                        plural_irregular(names.len() - 1, "other model", "other models"),
                        others.join(", ")
                    ),
                )
                .file(&m.relative_path)
                .span(span(&m.stripped, cte.start, cte.end))
                .evidence(raw_span(&m.stripped, cte.start, cte.start + cte.body.len()))
                .remediation(format!(
                    "The local reuse heuristic suggests {target}. Confirm shared meaning first, then choose a model for a reusable dataset or a macro for parameterized expressions and column lists. Select the materialization from measured cost, testing, and operational needs rather than count alone."
                ))
                .effort(effort::MEDIUM)
                .project(&project.name)
                .ctx("fingerprint", digest.as_str())
                .ctx("repeated_in", json!(names))
                .ctx("related_files", json!(related)),
            );
        }
    }
    out
}

fn sql0003(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    find_derived_subqueries(&m.stripped)
        .into_iter()
        .filter(|sq| sq.depth >= 2)
        .map(|sq| {
            Suggestion::new(
                "SSC-EWI-DBTSQL0003",
                format!(
                    "This subquery has {} nested `select` levels; sequential CTEs read top-down.",
                    sq.depth
                ),
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, sq.start, sq.end))
            .evidence(raw_span(&m.raw, sq.start, sq.start + sq.body.len() + 20))
            .remediation(
                "Flatten the nesting into sequential CTEs, one per logical step, so the model \
reads in logical dependency order, not guaranteed physical execution order. Select from each CTE while debugging to inspect intermediate results.",
            )
            .effort(effort::MEDIUM)
        })
        .collect()
}

fn sql0004(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python || rx!(r"(?i)\bqualify\b").is_match(&m.stripped) {
        return vec![];
    }
    let mut out = vec![];
    for sq in find_derived_subqueries(&m.stripped) {
        let Some(w) = window_fn().captures(&sq.body) else { continue };
        let Some(rel) = m.stripped[sq.start..].find('(') else { continue };
        let Some(close) = match_paren(&m.stripped, sq.start + rel) else { continue };
        if !rx!(r"(?i)\bwhere\b").is_match(slice_from(&m.stripped, close, 400)) {
            continue;
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTSQL0004",
                format!(
                    "`{}()` is computed in a subquery filtered by an outer `where`; `qualify` \
does this in one step.",
                    w[1].to_lowercase()
                ),
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, sq.start, sq.end))
            .evidence(raw_span_limit(&m.raw, sq.start, close + 1, 180))
            .remediation(
                "Replace the wrapper with QUALIFY:\n\n```sql\nselect ...\nfrom {{ ref('upstream') }}\n\
qualify row_number() over (\n    partition by customer_id order by updated_at desc\n) = 1\n```\n\n\
Preserve the original projection and filter timing when moving the predicate. Make the `ORDER BY` deterministic: add keys that uniquely break ties rather than copying the illustrative timestamp order unchanged.",
            )
            .effort(effort::LOW),
        );
    }
    out
}

fn sql0005(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python || m.layer == "bronze" {
        return vec![];
    }
    let mut out = vec![];
    for mt in rx!(r"(?i)\bselect\s+\*").find_iter(&m.stripped) {
        // A star over a CTE is the documented passthrough; only ref/source reads count.
        if !rx!(r"\bfrom\s+\{\{").is_match(slice_from(&m.stripped, mt.end(), 120)) {
            continue;
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTSQL0005",
                "`select *` reads from a `ref` or `source`, so the output schema changes \
whenever upstream columns change.",
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, mt.start(), mt.end()))
            .evidence(raw_span(&m.raw, mt.start(), mt.end() + 80))
            .remediation(
                "List the columns explicitly. For a wide passthrough where that is impractical, \
use `{{ dbt_utils.star(from=ref('upstream'), except=['col_to_drop']) }}` so the expansion is at \
least resolved at compile time and visible in the compiled SQL. A generated column list can still change when upstream columns change; it does not freeze the schema.",
            )
            .effort(effort::LOW),
        );
    }
    out
}

fn sql0006(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    use super::prj::{relations, shared};
    if m.is_python { return vec![]; }
    relations::literal_reads(&m.raw).into_iter().filter(|r| r.stage || r.parts.len() >= 2).map(|r| {
        let location = relations::read_location(p, &r.parts);
        let table = location.identifier.key().unwrap_or_else(|| "<table>".into());
        let writers: Vec<_> = p.models.iter().filter(|model| shared::model_relation(p,model).is_some_and(|rel| matches!(shared::compare_locations(&[&location,&rel.physical],true),shared::LocationMatch::Equal))).collect();
        let advice = match writers.as_slice() {
            [writer] if !r.stage => format!("Read `{{{{ ref('{}') }}}}` from producer `{}` after checking that this dependency is acyclic; a prior-state cycle needs PRJ0022 relocation instead.",writer.name,crate::discovery::root_relative(p,&writer.relative_path)),
            many if many.len() > 1 && !r.stage => "Resolve the PRJ0020 multi-writer finding before choosing a producer; do not pick an arbitrary ref.".into(),
            _ => {
                let candidate = p.models.iter().any(|model| shared::model_relation(p, model).is_some_and(|rel| rel.location.identifier.key().as_deref() == Some(&table) && matches!(shared::compare_locations(&[&location, &rel.physical], true), shared::LocationMatch::Unresolved(_))));
                let note = if candidate && !r.stage { "A configured model identifier matches, but its physical relation is unresolved: config.schema is not the rendered schema. Confirm naming semantics and target location before choosing a ref; otherwise use the external source below. " } else { "" };
                format!("{note}{}", relations::source_advice(p,&location,&table,r.stage_suffix()))
            },
        };
        Suggestion::new("SSC-EWI-DBTSQL0006",format!("`{}` is a literal relation read without a ref/source dependency at this site. It does not use dbt location configuration here.",r.text))
            .file(&m.relative_path).span(span(&m.raw,r.match_start,r.end)).evidence(raw_span(&m.raw,r.match_start,r.end)).remediation(advice).effort(effort::LOW)
    }).collect()
}

fn sql0007(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    rx!(
        r"(?i)\bfrom\s+(?:\{\{[^}]*\}\}|[A-Za-z_][\w.$]*)(?:\s+(?:as\s+)?[A-Za-z_]\w*)?\s*,\s*(?:\{\{|[A-Za-z_])"
    )
    .find_iter(&m.stripped)
    .map(|mt| {
        Suggestion::new(
            "SSC-EWI-DBTSQL0007",
            "Comma-separated `from` clause; a missing predicate silently produces a cross join.",
        )
        .file(&m.relative_path)
        .span(span(&m.stripped, mt.start(), mt.end()))
        .evidence(raw_span(&m.raw, mt.start(), mt.end()))
        .remediation(
            "Use explicit `JOIN ... ON` syntax so the join condition sits with the join. Write \
`CROSS JOIN` deliberately when a cartesian product is intended.",
        )
        .effort(effort::LOW)
    })
    .collect()
}

fn sql0008(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    rx!(r"(?i)order\s+by\s*\(\s*select\s+null\s*\)|order\s+by\s+(?:1|null)\s*\)")
        .find_iter(&m.stripped)
        .filter(|mt| {
            let from = floor_char(&m.stripped, mt.start().saturating_sub(200));
            window_fn().is_match(&m.stripped[from..mt.end()])
        })
        .map(|mt| {
            Suggestion::new(
                "SSC-FDM-DBTSQL0008",
                "The window `order by` is a placeholder; which row survives deduplication is \
not defined by a meaningful ordering and can differ between runs.",
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, mt.start(), mt.end()))
            .evidence(raw_span(&m.raw, mt.start(), mt.end()))
            .remediation(
                "Supply a real ordering that breaks ties deterministically. Use the updated-at \
timestamp plus the primary key as a tiebreaker:\n\n```sql\nqualify row_number() over (\n    \
partition by customer_id\n    order by updated_at desc, source_row_id\n) = 1\n```\n\nIf this is \
converted code, the placeholder was left for a human to resolve and the correct column has to \
come from the source system.",
            )
            .effort(effort::MEDIUM)
        })
        .collect()
}

fn sql0009(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    extract_ctes(&m.stripped)
        .into_iter()
        .filter(|c| rx!(r"(?i)^(cte|tmp|temp|tbl|t|q|a|b|x|y|s|d|sub|src\d*)\d*$").is_match(&c.name))
        .map(|c| {
            Suggestion::new(
                "SSC-EWI-DBTSQL0009",
                format!("CTE `{}` has a generic name; rename it for what the step produces.", c.name),
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, c.start, c.end))
            .evidence(format!("{} as (...)", c.name))
            .remediation(
                "Rename it after what it produces: `orders_with_customer`, \
`deduplicated_events`, `daily_totals`. Import CTEs can take the upstream name.",
            )
            .effort(effort::LOW)
        })
        .collect()
}

fn sql0010(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    let mut out = vec![];
    for c in extract_ctes(&m.stripped) {
        // References inside the CTE's own body (recursion) do not count as use.
        let outside = format!("{}{}", &m.stripped[..c.start], &m.stripped[c.close + 1..]);
        let re = regex::Regex::new(&format!(r"(?i)\b{}\b", regex::escape(&c.name))).unwrap();
        if re.is_match(&outside) {
            continue;
        }
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTSQL0010",
                format!("CTE `{}` is defined but never referenced in this model.", c.name),
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, c.start, c.end))
            .evidence(format!("{} as (...)", c.name))
            .remediation(
                "Delete it if it is leftover, or wire it into the final select if the omission \
is a bug. Check the intended data flow before adding a missing join or deleting an import.",
            )
            .effort(effort::LOW),
        );
    }
    out
}

fn sql0011(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python || m.layer == "bronze" || m.materialization() == "ephemeral" {
        return vec![];
    }
    if !extract_ctes(&m.stripped).is_empty() || rx!(r"(?i)\bwhere\s+false\b").is_match(&m.stripped) {
        return vec![];
    }
    // The incremental watermark guard (`select max(..) from {{ this }}`) is
    // the standard idiom, not query logic. Blank it and keep byte offsets.
    let mut text = m.stripped.clone().into_bytes();
    for hit in rx!(r"(?is)\{%-?\s*if\s+is_incremental\s*\(\s*\)\s*-?%\}.*?\{%-?\s*endif\s*-?%\}").find_iter(&m.raw) {
        for b in text.iter_mut().take(hit.end()).skip(hit.start()) {
            if b.is_ascii() && *b != b'\n' {
                *b = b' ';
            }
        }
    }
    let text = String::from_utf8_lossy(&text).into_owned();
    let checks: [(&regex::Regex, &str); 4] = [
        (rx!(r"(?i)\bjoin\b"), "a join"),
        (rx!(r"(?i)\b(sum|count|avg|min|max|median|listagg)\s*\("), "an aggregate"),
        (rx!(r"(?i)\bover\s*\("), "a window function"),
        (rx!(r"(?i)\b(union|intersect|except)\b"), "a set operation"),
    ];
    let mut complexity = vec![];
    let mut first: Option<usize> = None;
    for (re, label) in checks {
        if let Some(hit) = re.find(&text) {
            complexity.push(label);
            first = Some(first.map_or(hit.start(), |f| f.min(hit.start())));
        }
    }
    if complexity.is_empty() {
        return vec![];
    }
    vec![Suggestion::new(
        "SSC-EWI-DBTSQL0011",
        format!("This model contains {} but no named CTEs.", complexity.join(" and ")),
    )
    .file(&m.relative_path)
    .line_opt(first.map(|f| find_line_number(&m.stripped, f)))
    .evidence(complexity.join(", "))
    .remediation(
        "Break the query into named CTEs, one per step, ending with a final select:\n\n```sql\n\
with orders as (\n    select * from {{ ref('stg_orders') }}\n),\ndaily_totals as (\n    select \
order_date, sum(amount) as total_amount\n    from orders\n    group by order_date\n)\nselect * \
from daily_totals\n```\n\nName each CTE for what it produces. While debugging you can then \
select from any single step.",
    )
    .effort(effort::LOW)]
}

fn sql0012(m: &ModelFile, p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    let mut out = vec![];
    for r in frx!(r"(?i)\bunion\b(?!\s+all\b)").find_iter(&m.stripped) {
        let Ok(mt) = r else { continue };
        out.push(
            Suggestion::new(
                "SSC-EWI-DBTSQL0012",
                "`union` performs duplicate-elimination work on every row; `union all` skips \
that cost.",
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, mt.start(), mt.end()))
            .evidence(raw_span(&m.raw, mt.start(), mt.end()))
            .remediation(format!(
                "Use `union all` when both inputs should be retained. Keep `union` only when \
distinct combined rows are the intended business result.{}",
                if p.provenance.is_migration {
                    " This model is converted code, so `union` copies the source SQL. Change it only after a \
comparison confirms equivalent rows and duplicate semantics on representative inputs. Matching one row count alone does not prove the change is safe."
                } else {
                    ""
                }
            ))
            .effort(effort::LOW),
        );
    }
    out
}

fn sql0013(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python {
        return vec![];
    }
    rx!(r"(?i)\bselect\s+distinct\b")
        .find_iter(&m.stripped)
        .map(|mt| {
            Suggestion::new(
                "SSC-EWI-DBTSQL0013",
                "`select distinct` performs duplicate-elimination work and may hide an upstream \
grain problem that `qualify` would make explicit.",
            )
            .file(&m.relative_path)
            .span(span(&m.stripped, mt.start(), mt.end()))
            .evidence(raw_span(&m.raw, mt.start(), mt.end()))
            .remediation(
                "Keep `distinct` when all projected rows must be deduplicated and no row-selection \
rule exists. Otherwise, fix the upstream grain or use `qualify row_number() over (partition by \
business_key order by updated_at desc) = 1` with the correct key and deterministic ordering. That example selects one row per key, not distinct projected rows; it is equivalent only when the business grain and tie-break contract support it.",
            )
            .effort(effort::LOW)
        })
        .collect()
}

/// `ref`/`source` key as `a.b`, from literal arguments.
fn edge_key(c: &crate::jinja::CallSite) -> String {
    let parts: Vec<String> = c
        .args
        .iter()
        .map(|a| match a {
            crate::jinja::Lit::Str(s) | crate::jinja::Lit::Expr(s) => s.clone(),
            other => format!("{other:?}"),
        })
        .collect();
    format!("{}:{}", c.name, parts.join("."))
}

fn execute_only(cond: &str) -> bool {
    let c = cond.trim();
    let c = c.strip_prefix("not (").and_then(|x| x.strip_suffix(')')).unwrap_or(c);
    c.trim() == "execute"
}

fn sql0014(m: &ModelFile, _p: &ProjectContext) -> Vec<Suggestion> {
    if m.is_python || m.jinja.parse_error.is_some() {
        return vec![];
    }
    let edges = || m.jinja.calls.iter().filter(|c| (c.name == "ref" || c.name == "source") && c.in_macro.is_none());
    let unconditional: std::collections::BTreeSet<String> =
        edges().filter(|c| c.control_depth == 0).map(edge_key).collect();
    let declared: std::collections::BTreeSet<String> = rx!(r"(?i)depends_on:\s*\{\{\s*(ref|source)\s*\(([^)]*)\)\s*\}\}")
        .captures_iter(&m.raw)
        .map(|c| {
            let args: Vec<&str> = rx!(r#"'([^']*)'|"([^"]*)""#)
                .captures_iter(&c[2])
                .map(|a| a.get(1).or(a.get(2)).map_or("", |g| g.as_str()))
                .collect();
            format!("{}:{}", c[1].to_lowercase(), args.join("."))
        })
        .collect();
    // One finding per model: every missing edge is one line in one comment block.
    // edge key -> (shown edge, call text, guard, position, conditions)
    type Edge = (String, String, String, (u32, u32), Vec<String>);
    let mut missing: indexmap::IndexMap<String, Edge> = indexmap::IndexMap::new();
    for c in edges().filter(|c| c.control_depth > 0) {
        let loop_depth = c.control_depth as usize > c.conditions.len();
        if !loop_depth && c.conditions.iter().all(|x| execute_only(x)) {
            continue;
        }
        let key = edge_key(c);
        if unconditional.contains(&key) || declared.contains(&key) {
            continue;
        }
        // The same edge in both arms of one `if` exists in every render.
        let complement = |a: &str, b: &str| a == format!("not ({b})") || b == format!("not ({a})");
        if let Some(last) = c.conditions.last() {
            let prefix = &c.conditions[..c.conditions.len() - 1];
            if edges().any(|o| {
                std::ptr::eq(o, c).not()
                    && edge_key(o) == key
                    && o.control_depth == c.control_depth
                    && o.conditions.len() == c.conditions.len()
                    && o.conditions[..o.conditions.len() - 1] == *prefix
                    && complement(last, o.conditions.last().unwrap())
            }) {
                continue;
            }
        }
        let shown = key.replacen(':', "(", 1) + ")";
        let evidence = collapse_ws(&strip_span_text(&m.raw, c.span.start_offset, c.span.end_offset));
        let guard = if c.conditions.is_empty() {
            "a `{% for %}` loop".to_string()
        } else {
            format!("`{{% if {} %}}`", c.conditions.join(" and "))
        };
        missing.entry(key).or_insert((shown, evidence, guard, (c.span.start_line, c.span.start_col), c.conditions.clone()));
    }
    let Some(first) = missing.values().next() else { return vec![] };
    let lines: Vec<String> = missing.values().map(|v| format!("-- depends_on: {}", v.1)).collect();
    let parts: Vec<String> = missing.values().map(|v| format!("`{}` under {} (line {})", v.0, v.2, v.3 .0)).collect();
    vec![Suggestion::new(
        "SSC-EWI-DBTSQL0014",
        format!(
            "{} edge(s) sit under a condition, so the DAG depends on the render; no `-- depends_on:` comment declares them: {}.",
            missing.len(),
            parts.join("; ")
        ),
    )
    .file(&m.relative_path)
    .at(first.3)
    .remediation(format!(
        "If these are required dependencies, add the SQL-comment hints below near the model top and retain the intended branches. Verify parsing and execution for supported variable/target combinations. This detector excludes execute-only guards, but that exclusion does not prove they expose every dependency.\n\n```sql\n{}\n```",
        lines.join("\n")
    ))
    .evidence(lines.join("; "))
    .effort(effort::LOW)
    .ctx("model", m.name.as_str())
    .ctx("edges", json!(missing.values().map(|v| json!({"edge": v.0, "line": v.3 .0, "conditions": v.4})).collect::<Vec<_>>()))]
}

fn strip_span_text(raw: &str, start: u32, end: u32) -> String {
    let (s, e) = (floor_char(raw, start as usize), floor_char(raw, (end as usize).max(start as usize)));
    raw[s..e].to_string()
}

#[cfg(test)]
mod tests {
    use crate::testing::TempProject;

    const BIG: &str = "select customer_id, sum(amount) as total_amount, count(*) as n from {{ ref('orders') }} where status = 'done' group by customer_id";

    fn one(path: &str, sql: &str) -> TempProject {
        TempProject::new(&[(path, sql)])
    }

    fn n(t: &TempProject, code: &str) -> usize {
        t.findings(code).len()
    }

    #[test]
    fn sql0001() {
        let c = "SSC-EWI-DBTSQL0001";
        let t = one("models/a.sql", &format!("select * from (\n{BIG}\n) x"));
        assert_eq!(n(&t, c), 1);
        assert_eq!(t.findings(c)[0].context["reuse_count"], 1);
        let t = TempProject::new(&[
            ("models/a.sql", &format!("select * from ({BIG}) x")),
            ("models/b.sql", &format!("select 1 from ({BIG}) y")),
        ]);
        assert_eq!(n(&t, c), 2);
        assert_eq!(t.findings(c)[0].context["reuse_count"], 2);
        // The same body twice in one model is one finding that lists both sites.
        let t = one("models/a.sql", &format!("select * from (\n{BIG}\n) x\nunion all\nselect * from (\n{BIG}\n) y"));
        let f = t.findings(c);
        assert_eq!(f.len(), 1, "{f:?}");
        assert_eq!(f[0].context["sites"].as_array().unwrap().len(), 2);
        assert!(f[0].message.contains("2 times"), "{}", f[0].message);
        let msg = &one("models/a.sql", &format!("select * from (\n{BIG}\n) x")).findings(c)[0].message.clone();
        assert!(msg.contains("derived-table subquery") && msg.contains("named CTE"), "{msg}");
        let t = one("models/a.sql", "with a as (select 1) select * from (select 1) x");
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn sql0002() {
        let c = "SSC-EWI-DBTSQL0002";
        let body = "select a,\n b,\n c,\n d,\n e\n from {{ ref('x') }}\n where a > 1";
        let t = TempProject::new(&[
            ("models/a.sql", &format!("with shared as ({body}) select * from shared")),
            ("models/b.sql", &format!("with shared as ({body}) select a from shared")),
        ]);
        assert_eq!(n(&t, c), 2);
        for f in t.findings(c) {
            let rel = f.context["related_files"].as_array().unwrap();
            assert_eq!(rel.len(), 1, "{rel:?}");
            let other = if f.file.ends_with("a.sql") { "b.sql:1" } else { "a.sql:1" };
            assert!(rel[0].as_str().unwrap().ends_with(other), "{rel:?}");
        }
        let t = TempProject::new(&[
            ("models/a.sql", &format!("with shared as ({body}) select * from shared")),
            ("models/b.sql", "with other as (select 1) select * from other"),
        ]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn sql0003() {
        let c = "SSC-EWI-DBTSQL0003";
        let t = one("models/a.sql", "select * from (select * from (select 1 as a) y) x");
        assert_eq!(n(&t, c), 1);
        let t = one("models/a.sql", "with a as (select 1 as a) select * from a");
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn sql0004() {
        let c = "SSC-EWI-DBTSQL0004";
        let sql = "select * from (select *, row_number() over (partition by id order by ts desc) rn from t) x where rn = 1";
        assert_eq!(n(&one("models/a.sql", sql), c), 1);
        let ok = "select * from t qualify row_number() over (partition by id order by ts desc) = 1";
        assert_eq!(n(&one("models/a.sql", ok), c), 0);
    }

    #[test]
    fn sql0005() {
        let c = "SSC-EWI-DBTSQL0005";
        assert_eq!(n(&one("models/silver/a.sql", "select * from {{ ref('x') }}"), c), 1);
        assert_eq!(n(&one("models/silver/a.sql", "with s as (select 1 a) select * from s"), c), 0);
    }

    #[test]
    fn sql0006() {
        let c = "SSC-EWI-DBTSQL0006";
        assert_eq!(n(&one("models/a.sql", "select a from raw.public.orders"), c), 1);
        assert_eq!(n(&one("models/a.sql", "select a from {{ ref('orders') }}"), c), 0);
    }

    #[test]
    fn sql0007() {
        let c = "SSC-EWI-DBTSQL0007";
        assert_eq!(n(&one("models/a.sql", "select 1 from orders o, customers c where o.id = c.id"), c), 1);
        assert_eq!(n(&one("models/a.sql", "select 1 from orders o join customers c on o.id = c.id"), c), 0);
    }

    #[test]
    fn sql0008() {
        let c = "SSC-FDM-DBTSQL0008";
        let sql = "select * from t qualify row_number() over (partition by id order by (select null)) = 1";
        assert_eq!(n(&one("models/a.sql", sql), c), 1);
        let ok = "select * from t qualify row_number() over (partition by id order by ts desc) = 1";
        assert_eq!(n(&one("models/a.sql", ok), c), 0);
    }

    #[test]
    fn sql0009() {
        let c = "SSC-EWI-DBTSQL0009";
        assert_eq!(n(&one("models/a.sql", "with t1 as (select 1 a) select * from t1"), c), 1);
        assert_eq!(n(&one("models/a.sql", "with daily_totals as (select 1 a) select * from daily_totals"), c), 0);
    }

    #[test]
    fn sql0010() {
        let c = "SSC-EWI-DBTSQL0010";
        let sql = "with used as (select 1 a), dead as (select 2 b) select * from used";
        assert_eq!(n(&one("models/a.sql", sql), c), 1);
        assert_eq!(n(&one("models/a.sql", "with used as (select 1 a) select * from used"), c), 0);
    }

    #[test]
    fn sql0011() {
        let c = "SSC-EWI-DBTSQL0011";
        assert_eq!(n(&one("models/silver/a.sql", "select a, count(*) from t group by a"), c), 1);
        assert_eq!(n(&one("models/silver/a.sql", "select a from t"), c), 0);
        // The finding points at the set operation, not the first select.
        let t = one("models/silver/a.sql", "select distinct a\nfrom t\nunion\nselect a from u");
        assert_eq!(t.findings(c)[0].line, Some(3));
        // An incremental watermark guard is not an aggregate to structure.
        let inc = "select a, ts from t\n{% if is_incremental() %}\nwhere ts > (select max(ts) from {{ this }})\n{% endif %}";
        assert_eq!(n(&one("models/silver/a.sql", inc), c), 0);
    }

    #[test]
    fn sql0012() {
        let c = "SSC-EWI-DBTSQL0012";
        assert_eq!(n(&one("models/a.sql", "select 1 union select 2"), c), 1);
        assert_eq!(n(&one("models/a.sql", "select 1 union all select 2"), c), 0);
    }

    #[test]
    fn sql0012_converted_text() {
        let mig = crate::testing::TempProject::new(&[
            (".dbt-quality.yml", "migration:\n  mode: lift_and_shift\n"),
            ("models/a.sql", "select 1 union select 2"),
        ]);
        let r = &mig.findings("SSC-EWI-DBTSQL0012")[0].remediation;
        assert!(r.contains("converted code") && r.contains("row count"), "{r}");
        let r = &one("models/a.sql", "select 1 union select 2").findings("SSC-EWI-DBTSQL0012")[0].remediation.clone();
        assert!(!r.contains("converted code"), "{r}");
    }

    #[test]
    fn sql0013() {
        let c = "SSC-EWI-DBTSQL0013";
        assert_eq!(n(&one("models/a.sql", "select distinct a from t"), c), 1);
        assert_eq!(n(&one("models/a.sql", "select a from t"), c), 0);
    }

    #[test]
    fn sql0002_cross_project() {
        let c = "SSC-EWI-DBTSQL0002";
        let body = "select a,\n b,\n c,\n d,\n e\n from {{ ref('x') }}\n where a > 1";
        let q = format!("with shared as ({body}) select * from shared");
        let t = TempProject::new(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: d\n"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: d\n"),
            ("a/models/m1.sql", &q),
            ("b/models/m2.sql", &q),
        ]);
        let f = t.findings(c);
        assert_eq!(f.len(), 2);
        assert!(f.iter().all(|s| s.context["cross_project"] == true));
        assert!(f.iter().all(|s| s.context["related_files"].as_array().unwrap().len() == 1));
        let t = TempProject::new(&[
            ("a/dbt_project.yml", "name: a\nversion: '1.0'\nprofile: d\n"),
            ("b/dbt_project.yml", "name: b\nversion: '1.0'\nprofile: d\n"),
            ("a/models/m1.sql", &q),
            ("b/models/m2.sql", "select 1"),
        ]);
        assert_eq!(n(&t, c), 0);
    }

    #[test]
    fn sql0014() {
        let c = "SSC-EWI-DBTSQL0014";
        let cond = "{% if var('use_b') %}select * from {{ ref('b') }}{% else %}select * from {{ ref('a') }}{% endif %}";
        // Two missing edges in one model give one finding with both lines.
        let f = one("models/m.sql", cond).findings(c);
        assert_eq!(f.len(), 1);
        assert!(f[0].remediation.contains("ref('a')") && f[0].remediation.contains("ref('b')"), "{}", f[0].remediation);
        let twice = format!("{cond}\n{{% if var('z') %}}{{{{ ref('b') }}}}{{% endif %}}");
        assert_eq!(one("models/m.sql", &twice).findings(c)[0].remediation.matches("ref('b')").count(), 1);
        let decl = format!("-- depends_on: {{{{ ref('a') }}}}\n-- depends_on: {{{{ ref('b') }}}}\n{cond}");
        assert_eq!(n(&one("models/m.sql", &decl), c), 0);
        let exec = "{% if execute %}select * from {{ ref('b') }}{% endif %}";
        assert_eq!(n(&one("models/m.sql", exec), c), 0);
        let both = "{% if is_incremental() %}select * from {{ ref('b') }}{% else %}select * from {{ ref('b') }} where 1=1{% endif %}";
        assert_eq!(n(&one("models/m.sql", both), c), 0);
        let uncond = "select * from {{ ref('b') }} {% if var('x') %} join {{ ref('b') }} on 1=1 {% endif %}";
        assert_eq!(n(&one("models/m.sql", uncond), c), 0);
        let el = "{% if var('a', '') != '' %}select 1{% elif var('b', '') != '' %}select 2{% else %}select * from {{ ref('b') }}{% endif %}";
        let f = one("models/m.sql", el).findings(c);
        assert!(f.len() == 1 && !f[0].message.contains("(if "), "{}", f[0].message);
        assert_eq!(super::token_cut("from x where {{ var('abc') }} and y", 24), "from x where ...");
        let lp = "{% for t in ['a'] %}select * from {{ ref('b') }}{% endfor %}";
        assert_eq!(n(&one("models/m.sql", lp), c), 1);
    }
}
