//! Standalone assessment report with local source tools and an optional CDN chart.
//! Shared-report sandboxes can block scripts. The static findings remain readable.

use std::fmt::Write as _;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

use crate::model::{RuleMeta, RULES};

const CSS: &str = include_str!("report.css");
const SCRIPT: &str = include_str!("report.js");
pub const CHART_URL: &str = "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.js";
pub const CHART_INTEGRITY: &str = "sha384-G436+Z2nlA8+PNoeRvWdxKbvOf8E/y+lYxqht2iBwNHTQDV5CJr3+AGVj8fGZi5t";

pub fn esc(text: &str) -> String {
    let mut output = String::with_capacity(text.len());
    for character in text.chars() {
        match character {
            '&' => output.push_str("&amp;"), '<' => output.push_str("&lt;"), '>' => output.push_str("&gt;"),
            '"' => output.push_str("&quot;"), '\'' => output.push_str("&#39;"), other => output.push(other),
        }
    }
    output
}

fn inline(text: &str) -> String {
    let mut output = String::new();
    for (index, part) in text.split('`').enumerate() {
        if index % 2 == 1 {
            let _ = write!(output, "<code>{}</code>", esc(part));
        } else {
            let escaped = esc(part);
            let mut bold = false;
            for (index, segment) in escaped.split("**").enumerate() {
                if index > 0 { output.push_str(if bold { "</strong>" } else { "<strong>" }); bold = !bold; }
                output.push_str(segment);
            }
            if bold { output.push_str("</strong>"); }
        }
    }
    output
}

/// Render fenced code, bullet lists, paragraphs, inline code, and bold text.
/// Raw HTML is escaped. References use validated structured URLs instead.
pub fn markdown(text: &str) -> String {
    let mut output = String::new();
    let mut paragraph: Vec<&str> = vec![];
    let mut list = false;
    let mut lines = text.lines().peekable();
    let flush = |output: &mut String, paragraph: &mut Vec<&str>| {
        if !paragraph.is_empty() {
            let _ = write!(output, "<p>{}</p>", inline(&paragraph.join(" ")));
            paragraph.clear();
        }
    };
    while let Some(line) = lines.next() {
        let trimmed = line.trim_start();
        if let Some(language) = trimmed.strip_prefix("```") {
            flush(&mut output, &mut paragraph);
            if list { output.push_str("</ul>"); list = false; }
            let mut code = vec![];
            for line in lines.by_ref() {
                if line.trim_start().starts_with("```") { break; }
                code.push(line);
            }
            let _ = write!(output, "<pre><code class=\"lang-{}\">{}</code></pre>", esc(language.trim()), esc(&code.join("\n")));
        } else if let Some(item) = trimmed.strip_prefix("- ").or_else(|| trimmed.strip_prefix("* ")) {
            flush(&mut output, &mut paragraph);
            if !list { output.push_str("<ul>"); list = true; }
            let _ = write!(output, "<li>{}</li>", inline(item));
        } else if trimmed.is_empty() {
            flush(&mut output, &mut paragraph);
            if list { output.push_str("</ul>"); list = false; }
        } else {
            if list { output.push_str("</ul>"); list = false; }
            paragraph.push(trimmed);
        }
    }
    flush(&mut output, &mut paragraph);
    if list { output.push_str("</ul>"); }
    output
}

fn text(value: &Value) -> String {
    match value { Value::String(text) => text.clone(), Value::Null => String::new(), other => other.to_string() }
}

fn badge(kind: &str, value: &str) -> String {
    let class: String = value.chars().filter(char::is_ascii_lowercase).collect();
    format!("<span class=\"badge {kind}-{class}\">{}</span>", esc(value))
}

/// Accept only absolute HTTPS references without credentials or parser repairs.
pub fn safe_reference_url(value: &str) -> bool {
    if value.chars().any(|character| character.is_whitespace() || character.is_control() || character == '\\') { return false; }
    let bytes = value.as_bytes();
    for (index, byte) in bytes.iter().enumerate() {
        if *byte == b'%' && !(bytes.get(index + 1).is_some_and(u8::is_ascii_hexdigit) && bytes.get(index + 2).is_some_and(u8::is_ascii_hexdigit)) { return false; }
    }
    let Ok(parsed) = url::Url::parse(value) else { return false };
    value.starts_with("https://") && parsed.scheme() == "https" && parsed.host_str().is_some()
        && parsed.username().is_empty() && parsed.password().is_none()
}

fn rule_doc(rule: &RuleMeta) -> String {
    let mut output = format!("<details class=\"rule-card\" id=\"{}\"><summary>{} - {}</summary><div class=\"rule-body\">{}<p>{}</p>{}<h4>Remediation</h4>{}",
        esc(rule.code), esc(rule.code), esc(rule.name), badge("level", rule.level), esc(rule.short_description), markdown(rule.long_description), markdown(rule.remediation));
    for example in rule.examples {
        let _ = write!(output, "<h4>{}</h4><p>Review the rule guidance and conditions before using this alternative.</p><p>Example</p><pre><code>{}</code></pre><p>Alternative to consider</p><pre><code>{}</code></pre>", esc(example.title), esc(example.bad), esc(example.good));
    }
    output.push_str("<h4>References</h4><ul class=\"reference-list\">");
    for reference in rule.references {
        if safe_reference_url(reference.url) {
            let _ = write!(output, "<li><a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a></li>", esc(reference.url), esc(reference.title));
        } else { let _ = write!(output, "<li>{} (link unavailable)</li>", esc(reference.title)); }
    }
    output.push_str("</ul></div></details>");
    output
}

fn json_block(value: &Value) -> String {
    serde_json::to_string(value).unwrap().replace('&', "\\u0026").replace('<', "\\u003c").replace('>', "\\u003e")
        .replace('\u{2028}', "\\u2028").replace('\u{2029}', "\\u2029")
}

fn base64(bytes: &[u8]) -> String {
    const ALPHABET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut output = String::new();
    for chunk in bytes.chunks(3) {
        let bits = ((chunk[0] as u32) << 16) | ((chunk.get(1).copied().unwrap_or(0) as u32) << 8) | chunk.get(2).copied().unwrap_or(0) as u32;
        output.push(ALPHABET[(bits >> 18) as usize] as char);
        output.push(ALPHABET[((bits >> 12) & 63) as usize] as char);
        output.push(if chunk.len() > 1 { ALPHABET[((bits >> 6) & 63) as usize] as char } else { '=' });
        output.push(if chunk.len() > 2 { ALPHABET[(bits & 63) as usize] as char } else { '=' });
    }
    output
}

fn static_findings(findings: &[&Value]) -> String {
    if findings.is_empty() { return "<p>No returned findings in this section.</p>".into(); }
    let mut output = String::from("<div class=\"table-wrap\"><table><thead><tr><th>Level / severity</th><th>Project / file</th><th>Finding and evidence</th></tr></thead><tbody>");
    for finding in findings {
        let code = text(&finding["rule_id"]);
        let _ = write!(output, "<tr><td>{}{}</td><td class=\"location\">{}<br><code>{}:{}</code></td><td class=\"message\"><a href=\"#{}\">{}</a><p>{}</p><details><summary>Evidence and remediation</summary><pre><code>{}</code></pre>{}</details></td></tr>",
            badge("level", &text(&finding["level"])), badge("severity", &text(&finding["severity"])), esc(&text(&finding["project"])), esc(&text(&finding["file"])), esc(&text(&finding["line"])), esc(&code), esc(&code), esc(&text(&finding["message"])), esc(&text(&finding["evidence"])), markdown(&text(&finding["remediation"])));
    }
    output.push_str("</tbody></table></div>");
    output
}

/// Render the normal report or the HTML-only payload from `build_html_report`.
pub fn render(report: &Value) -> String {
    let summary = &report["summary"];
    let counts = &summary["counts"];
    let findings = report["suggestions"].as_array().map(Vec::as_slice).unwrap_or_default();
    let active: Vec<_> = findings.iter().filter(|finding| finding["suppressed"] != true).collect();
    let suppressed: Vec<_> = findings.iter().filter(|finding| finding["suppressed"] == true).collect();
    // HTML parsing normalizes CRLF. Hash the bytes browsers execute on every OS.
    let script = SCRIPT.replace("\r\n", "\n").replace('\r', "\n");
    let script_hash = base64(&Sha256::digest(script.as_bytes()));
    let policy = format!("default-src 'none'; script-src 'sha256-{script_hash}' {CHART_URL}; script-src-attr 'none'; style-src 'unsafe-inline'; img-src 'none'; font-src 'none'; connect-src 'none'; form-action 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; worker-src 'none'");
    // Embed only what report.js reads. The static HTML already holds the
    // rule catalog, projects, and top fixes, so they are not repeated here.
    let fired: std::collections::BTreeSet<&str> = findings.iter().filter_map(|finding| finding["rule_id"].as_str()).collect();
    let payload = json!({
        "suggestions": report["suggestions"], "summary": {"categories": summary["categories"]}, "html": report["html"],
        "rules": RULES.iter().filter(|rule| fired.contains(rule.code)).map(|rule| (rule.code.to_string(), json!({
            "rationale": rule.long_description, "examples": rule.examples,
            "references": rule.references.iter().filter(|reference| safe_reference_url(reference.url)).collect::<Vec<_>>(),
        }))).collect::<serde_json::Map<_, _>>(),
    });
    let metadata = json!({
        "generated": report["generated"], "intent": "Review dbt audit findings and model source snapshots",
        "root": report["root"], "generator": format!("dbt-quality {}", crate::VERSION),
        "command": "dbt-quality audit <root> --html <file> [--include-models]",
        "filters": report["html"]["filters"], "source_limits": report["html"]["limits"],
        "dataSources": [{"type": "audit", "root": report["root"], "source": "dbt project files"}],
        "libraries": [{"name": "Chart.js", "version": "4.4.4", "url": CHART_URL, "integrity": CHART_INTEGRITY, "license": "MIT", "bytes": 205475}],
        "sections": (["overview", "categories", "projects", "remediation", "findings", "suppressed", "checks", "rules"].iter()
            .map(|id| json!({"id": id, "producerNotes": "Generated from the audit snapshot; re-run dbt-quality to refresh."})).collect::<Vec<_>>()),
        "provenance": report.get("provenance"),
    });
    let mut output = format!("<!doctype html><html lang=\"en\" data-theme=\"auto\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><meta name=\"snowflake-source\" content=\"cortex-agent-authored\"><meta name=\"referrer\" content=\"no-referrer\"><meta http-equiv=\"Content-Security-Policy\" content=\"{}\"><title>dbt quality assessment</title><script type=\"application/json\" id=\"snowflake-report-metadata\">{}</script><style>{CSS}</style></head><body><a class=\"skip-link\" href=\"#main\">Skip to report</a><div class=\"layout\"><aside class=\"sidebar\"><div class=\"brand\">dbt quality</div><nav aria-label=\"Report sections\">", esc(&policy), json_block(&metadata));
    for (id, label) in [("overview", "Overview"), ("findings", "Findings"), ("suppressed", "Suppressed"), ("checks", "Skipped checks"), ("rules", "Rule reference")] {
        let _ = write!(output, "<a href=\"#{id}\">{label}</a>");
    }
    output.push_str("</nav><label for=\"theme\">Theme</label><select id=\"theme\" aria-label=\"Theme\"><option value=\"auto\">Auto</option><option value=\"light\">Light</option><option value=\"dark\">Dark</option></select><p class=\"muted\">A saved audit snapshot. No live dbt execution.</p></aside><main id=\"main\"><section id=\"overview\"><div class=\"eyebrow\">Project assessment</div><h1>dbt quality assessment</h1>");
    let _ = write!(output, "<p class=\"muted\"><code>{}</code><br>Generated {}</p>", esc(&text(&report["root"])), esc(&text(&report["generated"])));
    output.push_str("<p id=\"script-status\" class=\"notice\">Interactive controls need JavaScript. If scripts are blocked, use the static findings and rule reference below.</p><div class=\"tiles\">");
    for (label, value) in [("Projects", &summary["project_count"]), ("Models", &summary["model_count"]), ("Active findings", &counts["total"]), ("Errors", &counts["error"]), ("Warnings", &counts["warning"]), ("Suppressed", &counts["suppressed"])] {
        let _ = write!(output, "<div class=\"tile\"><div class=\"value\">{}</div><div class=\"label\">{label}</div></div>", esc(&text(value)));
    }
    let _ = write!(output, "</div><p class=\"muted\">Summary cards, category totals, and top findings cover the entire audit. The returned list contains {} active and {} suppressed findings after command filters.</p><p class=\"notice\">{} skipped checks and {} read or rule errors. Skipped checks are not passed checks.</p></section>", active.len(), suppressed.len(), report["skipped_checks"].as_array().map_or(0, Vec::len), report["errors"].as_array().map_or(0, Vec::len));
    output.push_str("<section id=\"categories\"><h2>Category breakdown</h2><p id=\"chart-status\" class=\"muted\">The optional chart needs CDN access. The category table does not.</p><div id=\"chart-box\" class=\"chart-box\" hidden><canvas id=\"category-chart\" role=\"img\" aria-label=\"Active findings by category; exact values are in the following table\"></canvas></div><div class=\"table-wrap\"><table><thead><tr><th>Category</th><th>Errors</th><th>Warnings</th><th>Information</th><th>Total</th></tr></thead><tbody>");
    for category in summary["categories"].as_array().into_iter().flatten() {
        let _ = write!(output, "<tr><td>{}</td><td class=\"n\">{}</td><td class=\"n\">{}</td><td class=\"n\">{}</td><td class=\"n\">{}</td></tr>", esc(&text(&category["label"])), esc(&text(&category["error"])), esc(&text(&category["warning"])), esc(&text(&category["information"])), esc(&text(&category["total"])));
    }
    output.push_str("</tbody></table></div></section><section id=\"projects\"><h2>Projects</h2><div class=\"table-wrap\"><table><thead><tr><th>Project</th><th>Path</th><th>Models</th><th>Active findings</th></tr></thead><tbody>");
    for project in report["projects"].as_array().into_iter().flatten() {
        let _ = write!(output, "<tr><td>{}</td><td><code>{}</code></td><td>{}</td><td>{}</td></tr>", esc(&text(project.get("label").unwrap_or(&project["name"]))), esc(&text(&project["path"])), esc(&text(&project["model_count"])), esc(&text(&project["tally"]["counts"]["total"])));
    }
    output.push_str("</tbody></table></div></section><section id=\"remediation\"><h2>Top findings</h2><p class=\"muted\">Rules with the most active findings in the entire audit. Check each recommendation against the model's intended behavior.</p>");
    for item in report["remediation"].as_array().into_iter().flatten().take(5) {
        let _ = write!(output, "<article class=\"card\"><h3><a href=\"#{}\">{}</a> - {}</h3><p>{} findings; effort {}.</p>{}</article>", esc(&text(&item["rule_id"])), esc(&text(&item["rule_id"])), esc(&text(&item["title"])), esc(&text(&item["count"])), esc(&text(&item["effort"])), markdown(&text(&item["remediation"])));
    }
    output.push_str("</section><section id=\"findings\"><h2>Findings</h2>");
    let filters = &report["html"]["filters"];
    let filter_note = if filters.is_object() {
        let names: Vec<&str> = filters["categories"].as_array().into_iter().flatten().filter_map(Value::as_str).map(crate::report::category_label).collect();
        format!("Command filters: categories {}; minimum level {}.", if names.is_empty() { "all".into() } else { names.join(", ") }, text(&filters["min_level"]))
    } else { "Command filter provenance is unavailable for this legacy payload.".into() };
    let _ = write!(output, "<p class=\"muted\">{}</p>", esc(&filter_note));
    // Source text is shown inside each finding; this notice says what is embedded.
    let notice = report["html"]["source_notice"].as_str().unwrap_or("File text is not included in this report.");
    let _ = write!(output, "<p class=\"notice\">{} Edits change a browser copy only; download and apply the file, then run the audit again.</p>", esc(notice));
    output.push_str(FINDING_CONTROLS);
    output.push_str("<div class=\"static-findings\"><h3>Active returned findings</h3>");
    output.push_str(&static_findings(&active));
    output.push_str("</div></section><section id=\"suppressed\"><h2>Suppressed findings</h2>");
    let _ = write!(output, "<p>{} suppressed across the entire audit; {} returned after command filters. Suppressed findings do not count as active defects.</p>{}", esc(&text(&counts["suppressed"])), suppressed.len(), static_findings(&suppressed));
    output.push_str("</section><section id=\"checks\"><h2>Skipped checks and read errors</h2>");
    let skipped = report["skipped_checks"].as_array().map(Vec::as_slice).unwrap_or_default();
    let errors = report["errors"].as_array().map(Vec::as_slice).unwrap_or_default();
    if skipped.is_empty() && errors.is_empty() {
        output.push_str("<p>All checks completed. No files had read errors.</p>");
    } else {
        output.push_str("<p>These checks did not complete. Do not interpret missing findings as a passing result.</p>");
    }
    if !skipped.is_empty() {
        output.push_str("<div class=\"table-wrap\"><table><thead><tr><th>Rule</th><th>Reason</th></tr></thead><tbody>");
        for check in skipped {
            let _ = write!(output, "<tr><td>{}</td><td>{}</td></tr>", esc(&text(&check["rule_id"])), esc(&text(&check["reason"])));
        }
        output.push_str("</tbody></table></div>");
    }
    if !errors.is_empty() {
        output.push_str("<h3>Read or rule errors</h3><ul>");
        for error in errors { let _ = write!(output, "<li>{}</li>", esc(&text(error))); }
        output.push_str("</ul>");
    }
    output.push_str("</section><section id=\"rules\"><h2>Rule reference</h2><p>Rules with at least one returned finding. Run <code>dbt-quality rules</code> for the full catalog.</p>");
    let mut rules: Vec<_> = RULES.iter().filter(|rule| fired.contains(rule.code)).collect(); rules.sort_by_key(|rule| rule.code);
    if rules.is_empty() { output.push_str("<p>No rules have returned findings.</p>"); }
    for rule in rules { output.push_str(&rule_doc(rule)); }
    output.push_str("</section><footer><p>Source tools run locally in this document. No source is sent to a service. Chart.js 4.4.4 (MIT) loads from jsDelivr with a pinned integrity hash. CDN code runs in this page and is not isolated from report data. Shared Snowflake report sandboxes can block CDN assets or scripts; use the static views there.</p></footer></main></div>");
    output.push_str(DETAIL_DIALOG);
    let _ = writeln!(output, "<script type=\"application/json\" id=\"report-data\">{}</script><script id=\"chart-library\" async src=\"{CHART_URL}\" integrity=\"{CHART_INTEGRITY}\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script><script id=\"report-script\">{script}</script></body></html>", json_block(&payload));
    output
}

const FINDING_CONTROLS: &str = r#"<div class="interactive"><div class="filters">
<label class="search" for="finding-search">Search returned findings<input id="finding-search" type="search" placeholder="Rule, path, project, message, or evidence"></label>
<label for="filter-project">Project<select id="filter-project"><option value="">All projects</option></select></label>
<label for="filter-pack">Category<select id="filter-pack"><option value="">All categories</option></select></label>
<label for="filter-level">Level<select id="filter-level"><option value="">All levels</option><option>error</option><option>warning</option><option>information</option></select></label>
<label for="filter-severity">Severity<select id="filter-severity"><option value="">All severities</option><option>critical</option><option>high</option><option>medium</option><option>low</option></select></label>
<label for="filter-scope">View<select id="filter-scope"><option value="active">Active findings</option><option value="suppressed">Suppressed findings</option></select></label>
<label for="filter-sort">Sort<select id="filter-sort"><option value="level">Level</option><option value="severity">Severity</option><option value="file">File path</option><option value="project">Project</option><option value="rule_id">Rule code</option></select></label>
</div><div class="toolbar"><button id="reset-filters">Reset filters</button><p id="result-count" role="status" aria-live="polite"></p></div>
<div id="empty-findings" class="empty" hidden>No findings match these filters. Reset filters or change the search.</div>
<div id="finding-table" class="table-wrap"><table><thead><tr><th><span class="sr-only">Details</span></th><th>Level / severity</th><th>Project / file</th><th>Finding</th></tr></thead><tbody id="finding-rows"></tbody></table></div>
<div class="toolbar pager"><button id="previous-page">Previous</button><span id="page-count"></span><button id="next-page">Next</button></div></div>"#;

const DETAIL_DIALOG: &str = r#"<dialog id="finding-dialog" class="dialog" aria-labelledby="detail-title"><div class="dialog-inner"><div class="dialog-head"><h2 id="detail-title">Finding detail</h2><button id="close-detail" aria-label="Close finding detail">Close</button></div><p id="detail-location" class="muted"></p><p id="detail-message"></p><button id="copy-path">Copy path</button><div class="detail-grid"><div><h3>Evidence</h3><pre id="detail-evidence" class="evidence"></pre><details><summary>Rule guidance and examples</summary><h3>Why this matters</h3><p id="detail-rationale"></p><h3>Remediation</h3><pre id="detail-remediation"></pre><div id="detail-examples"></div><h3>References</h3><ul id="detail-references" class="reference-list"></ul></details></div><div><h3 id="source-title">Model source</h3><div id="source-files" class="file-tabs" role="group" aria-label="Files for this finding" hidden></div><p id="source-status" class="notice"></p><div class="toolbar"><button id="choose-file">Choose local model</button><label id="model-file-label" for="model-file">Local model file<input id="model-file" type="file" accept=".sql,.py"></label></div><div id="source-controls" hidden><div class="toolbar"><button id="edit-copy">Edit a copy</button><button id="copy-source">Copy source</button><button id="download-copy" class="primary">Download copy</button><button id="reset-copy" disabled>Reset copy</button><button id="preview-changes">Preview changes</button></div><p id="edit-state" class="source-state" role="status"></p><p id="source-window" class="muted"></p><div class="toolbar"><button id="previous-lines">Previous lines</button><button id="focus-line">Finding line</button><button id="next-lines">Next lines</button></div><div id="source-view" class="code-view" tabindex="0" role="region" aria-label="Original model source with line numbers"></div><label for="source-editor" class="muted">Edited model copy</label><textarea id="source-editor" class="source-editor" spellcheck="false" maxlength="262144" aria-label="Edited model copy" hidden></textarea><pre id="change-preview" class="diff" hidden></pre></div><div id="copy-fallback-box" hidden><label for="copy-fallback">Select and copy this text</label><textarea id="copy-fallback" class="copy-fallback" readonly></textarea></div><p id="action-status" role="status" aria-live="polite"></p></div></div></div></dialog>"#;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn markdown_fences_and_escapes() {
        let html = markdown("Use `x<y`.\n\n```sql\nselect 1 < 2\n```\n- a **b**");
        assert!(html.contains("<code>x&lt;y</code>"));
        assert!(html.contains("<pre><code class=\"lang-sql\">select 1 &lt; 2</code></pre>"));
        assert!(html.contains("<li>a <strong>b</strong></li>"));
    }

    #[test]
    fn references_reject_unsafe_urls() {
        for value in ["javascript:alert(1)", "//example.com/x", "http://example.com", "https://name:secret@example.com", "https://example.com/a b", "https://example.com/\\a", "https://example.com/%zz", "https://example.com/%a", "https:\n//example.com", "https:example.com"] {
            assert!(!safe_reference_url(value), "{value}");
        }
        assert!(safe_reference_url("https://docs.getdbt.com/reference/dbt-jinja-functions/ref#advanced-ref-usage"));
    }

    #[test]
    fn script_data_is_inert_and_csp_hashes_exact_bytes() {
        let attack = "</script><img src=x onerror=alert(1)>\u{2028}";
        let report = json!({"root": attack, "summary": {"counts": {}}, "suggestions": [{"rule_id": "unknown", "file": attack, "evidence": attack, "level": "error", "message": attack}], "errors": [attack], "html": {"models": {"x": {"file": attack, "source": {"text": attack}}}}});
        let html = render(&report);
        assert!(!html.contains(attack));
        assert!(html.contains("\\u003c/script\\u003e"));
        let emitted_script = html.split("<script id=\"report-script\">").nth(1).unwrap().split("</script>").next().unwrap();
        assert!(!emitted_script.contains('\r'));
        assert!(html.contains(&format!("sha256-{}", base64(&Sha256::digest(emitted_script)))));
        assert!(html.contains("script-src-attr &#39;none&#39;"));
        assert!(html.contains("base-uri &#39;none&#39;"));
        assert!(!SCRIPT.contains("innerHTML"));
        assert!(!SCRIPT.contains("eval("));
        assert!(!SCRIPT.contains("fetch("));
        assert!(!SCRIPT.contains("createWritable"));
        assert_eq!(html.matches("<script id=\"report-script\">").count(), 1);
        assert_eq!(html.matches("src=\"https://").count(), 1);
    }

    #[test]
    fn static_view_separates_suppression_and_has_all_rules() {
        let html = render(&json!({"suggestions": [{"message": "ACTIVE_SENTINEL"}, {"message": "SUPPRESSED_SENTINEL", "suppressed": true}]}));
        let active = html.split("<div class=\"static-findings\">").nth(1).unwrap().split("<section id=\"suppressed\">").next().unwrap();
        assert!(active.contains("ACTIVE_SENTINEL"));
        assert!(!active.contains("SUPPRESSED_SENTINEL"));
        assert_eq!(html.matches("class=\"rule-card\"").count(), 0);
        assert!(html.contains("No rules have returned findings."));
        assert!(html.contains("name=\"viewport\""));
        assert!(html.contains("aria-labelledby=\"detail-title\""));
    }

    #[test]
    fn embedded_payload_holds_only_script_inputs() {
        let code = RULES[0].code;
        let html = render(&json!({"rule_catalog": [{"rationale": "CATALOG_SENTINEL"}], "remediation": [{"title": "FIX_SENTINEL"}],
            "summary": {"categories": [{"category": "SQL"}]}, "suggestions": [{"rule_id": code}]}));
        let data = html.split("id=\"report-data\">").nth(1).unwrap().split("</script>").next().unwrap();
        let payload: Value = serde_json::from_str(data).unwrap();
        let keys: Vec<_> = payload.as_object().unwrap().keys().cloned().collect();
        assert_eq!(keys, ["suggestions", "summary", "html", "rules"]);
        assert_eq!(payload["rules"].as_object().unwrap().keys().collect::<Vec<_>>(), [code]);
        assert!(!data.contains("CATALOG_SENTINEL") && !data.contains("FIX_SENTINEL"));
        assert_eq!(html.matches("class=\"rule-card\"").count(), 1);
        assert!(html.contains(&format!("class=\"rule-card\" id=\"{code}\"")));
    }

    #[test]
    fn base64_known_vectors() {
        assert_eq!(base64(b""), ""); assert_eq!(base64(b"f"), "Zg==");
        assert_eq!(base64(b"fo"), "Zm8="); assert_eq!(base64(b"foo"), "Zm9v");
    }
}
