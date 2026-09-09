"""Anti-patterns report tab content (Option A: buckets-first drill-down).

Renders the "Anti-Patterns" tab from an anti-patterns-<timestamp>.json artifact
produced by `scai assessment anti-patterns`. Returns (content_html, js, css)
strings that generate_multi_report.py drops into the multi-tab report. Uses only
stdlib.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Customer-facing bucket labels, keyed on bucket id (overrides the JSON label so
# the report wording stays "Risks"-free regardless of the artifact producer).
_BUCKET_LABEL = {
    "performance_risks": "Performance",
    "architecture_security": "Architecture & Security",
    "behavior_semantic": "Behavior & Semantic",
}

# Hover copy explaining what each category means, shown on the bucket metric cards.
_BUCKET_TOOLTIP = {
    "performance_risks": "Patterns that scale poorly on Snowflake — row-by-row logic, "
    "unbounded scans, and similar performance concerns. Click to filter the tables below.",
    "architecture_security": "Constructs that don't map cleanly to Snowflake's architecture "
    "or raise security/permission concerns and need redesign. Click to filter the tables below.",
    "behavior_semantic": "Patterns whose runtime behavior or semantics can differ on Snowflake "
    "and may change results if migrated verbatim. Click to filter the tables below.",
}

# Hover copy for the top-level KPI cards.
_KPI_TOOLTIP = {
    "scanned": "Total code units analyzed for anti-patterns.",
    "affected": "Code units where at least one anti-pattern was detected.",
    "distinct": "Number of distinct anti-pattern types detected across the project.",
    "occurrences": "Total anti-pattern instances across all code units.",
}

# Severity ordering, most dangerous first — drives the code-unit "worst wins"
# badge and the severity filter option order.
_SEV_ORDER = ("critical", "high", "medium", "low")
_SEV_RANK = {s: len(_SEV_ORDER) - i for i, s in enumerate(_SEV_ORDER)}

# Severity palette — badges use bg/text/border; bar uses screenshot mid-tone accents.
_SEV_STYLES: Dict[str, Dict[str, str]] = {
    "critical": {"bg": "#FEE2E2", "text": "#991B1B", "border": "#FECACA", "bar": "#E15766"},
    "high": {"bg": "#FEF3C7", "text": "#B17E03", "border": "#FDE68A", "bar": "#F2CC54"},
    "medium": {"bg": "#E0F2FE", "text": "#0369A1", "border": "#BAE6FD", "bar": "#4A82E7"},
    "low": {"bg": "#F1F5F9", "text": "#475569", "border": "#E2E8F0", "bar": "#C6CCD9"},
}


def _bar_color(priority: str) -> str:
    return _SEV_STYLES.get(priority, {}).get("bar", "#64748B")


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _bucket_label(bucket: str, fallback: str = "") -> str:
    return _esc(_BUCKET_LABEL.get(bucket, fallback or bucket))


def _max_severity(flags: List[Dict]) -> str:
    best, best_rank = "", -1
    for x in flags:
        pr = x.get("priority", "") or ""
        rank = _SEV_RANK.get(pr, 0)
        if rank > best_rank:
            best, best_rank = pr, rank
    return best


def generate_anti_patterns_html_content(anti_patterns_json_path) -> Tuple[str, str, str]:
    data = json.loads(Path(anti_patterns_json_path).read_text(encoding="utf-8"))
    summary = data.get("summary", {}) or {}
    flags = data.get("flags", []) or []
    code_units = data.get("code_units", []) or []
    return _render_content(summary, flags, code_units), _JS, _CSS


_AP_PAGE_INTRO = (
    "Patterns that convert cleanly but may perform poorly or behave differently on Snowflake. "
    "Findings are grouped by category and priority from SnowConvert issue codes already recorded on your code units."
)

_AP_H1 = (
    '<h1 style="font-size: 1.875rem; font-weight: 800; color: #102E46; margin-bottom: 8px;">'
    'Anti-patterns</h1>'
)
_AP_INTRO = (
    f'<p style="color: #64748B; font-size: 1rem; line-height: 1.6; margin-bottom: 24px;">'
    f'{_esc(_AP_PAGE_INTRO)}</p>'
)
_AP_H2 = 'style="font-size: 1.35rem; font-weight: 700; color: #102E46; margin: 48px 0 16px;"'


def _render_page_header() -> str:
    return f'<div class="ap-page-header">{_AP_H1}{_AP_INTRO}</div>'


def _render_content(summary: Dict, flags: List[Dict], code_units: List[Dict]) -> str:
    if not flags:
        return (
            '<div id="anti-patterns-report">'
            + _render_page_header()
            + '<div class="ap-empty">No migration anti-patterns were detected in this project.</div>'
            + '</div>'
        )
    return (
        '<div id="anti-patterns-report">'
        + _render_page_header()
        + _render_kpis(summary)
        + _render_bucket_cards(summary.get("by_bucket", []))
        + _render_priority_bar(summary.get("by_priority", []))
        + _render_flag_catalog(flags)
        + _render_code_unit_table(code_units, flags)
        + '</div>'
    )


def _render_kpis(summary: Dict) -> str:
    cards = (
        ("scanned", "Code units scanned", summary.get("total_code_units_scanned", 0)),
        ("affected", "Code units affected", summary.get("code_units_with_findings", 0)),
        ("distinct", "Distinct anti-patterns", summary.get("total_flags_detected", 0)),
        ("occurrences", "Total occurrences", summary.get("total_occurrences", 0)),
    )
    items = "".join(
        f'<div class="effort-card" data-tooltip="{_esc(_KPI_TOOLTIP.get(key, ""))}">'
        f'<div class="effort-card-num">{_esc(value)}</div>'
        f'<div class="effort-card-lbl">{_esc(label)}</div>'
        f'</div>'
        for key, label, value in cards
    )
    return f'<div class="effort-cards ap-kpis">{items}</div>'


def _render_bucket_cards(by_bucket: List[Dict]) -> str:
    cards = []
    for b in by_bucket:
        affected = int(b.get("code_units_affected", 0) or 0)
        distinct = int(b.get("distinct_flags", 0) or 0)
        occ = int(b.get("total_occurrences", 0) or 0)
        if not (affected or distinct or occ):  # hide categories with nothing detected
            continue
        bucket = _esc(b.get("bucket", ""))
        cards.append(
            f'<div class="effort-card ap-bucket-card" data-bucket="{bucket}" role="button" tabindex="0" '
            f'data-tooltip="{_esc(_BUCKET_TOOLTIP.get(b.get("bucket", ""), ""))}" '
            f'onclick="apToggleBucket(this)">'
            f'<div class="effort-card-num">{affected}</div>'
            f'<div class="effort-card-lbl">{_bucket_label(b.get("bucket", ""), b.get("label", ""))}</div>'
            f'<div class="effort-card-lbl">{distinct} anti-patterns &middot; {occ} occurrences</div>'
            '</div>'
        )
    if not cards:
        return '<div class="ap-bucket-empty">No anti-patterns were detected in any category.</div>'
    return (
        '<div class="ap-bucket-caption">Filter by category</div>'
        '<div class="effort-cards ap-bucket-grid" data-role="buckets">' + "".join(cards) + '</div>'
    )


def _render_priority_bar(by_priority: List[Dict]) -> str:
    if not by_priority:
        return ""
    segments = []
    legend = []
    for p in by_priority:
        sev = p.get("priority", "") or ""
        pr = _esc(sev)
        bar_color = _bar_color(sev)
        label = _esc(p.get("label", pr))
        count = int(p.get("code_units_affected", 0) or 0)
        if count > 0:
            segments.append(
                f'<div class="ap-prio-seg ap-prio-{pr}" '
                f'style="flex:{count} 1 0;min-width:8px;background:{bar_color};" '
                f'title="{label}: {count} code units"></div>'
            )
        legend.append(
            f'<span class="ap-prio-legend">'
            f'<span class="ap-dot ap-prio-{pr}" style="background:{bar_color};"></span>'
            f'{label}: <strong>{_esc(p.get("code_units_affected", 0))}</strong></span>'
        )
    return (
        '<div class="ap-priority"><div class="ap-prio-bar">'
        + "".join(segments)
        + '</div><div class="ap-prio-legends">'
        + "".join(legend)
        + '</div></div>'
    )


def _render_flag_catalog(flags: List[Dict]) -> str:
    rows = []
    for i, f in enumerate(flags):
        bucket = _esc(f.get("bucket", ""))
        pr = _esc(f.get("priority", ""))
        rows.append(
            f'<tr class="ap-cat-row" data-bucket="{bucket}" onclick="apToggleFlagRow({i})">'
            f'<td class="ap-cat-name"><span class="expand-icon">&#9656;</span>{_esc(f.get("title", ""))}</td>'
            f'<td class="ctr ap-cat-sev"><span class="badge {pr}">{pr.title()}</span></td>'
            f'<td class="num">{_esc(f.get("code_units_affected", 0))}</td>'
            f'<td class="num">{_esc(f.get("total_occurrences", 0))}</td>'
            f'</tr>'
            f'<tr class="details-row" id="ap-flag-details-{i}"><td colspan="4">'
            f'<div class="ap-flag-body">'
            f'<div class="ap-block ap-what"><h4>What it is</h4><p>{_esc(f.get("what_it_is", ""))}</p></div>'
            f'<div class="ap-block ap-why"><h4>Why it was flagged</h4><p>{_esc(f.get("why_flagged", ""))}</p></div>'
            f'<div class="ap-block ap-rec"><h4>Snowflake recommendation</h4><p>{_esc(f.get("snowflake_recommendation", ""))}</p></div>'
            f'<a class="ap-doc-ref" href="{_esc(f.get("doc_url", ""))}" target="_blank" rel="noopener">'
            f'Reference: {_esc(f.get("code", ""))}</a>'
            f'</div>'
            f'</td></tr>'
        )
    return (
        f'<h2 {_AP_H2}>Flag catalog</h2>'
        '<div class="effort-table-wrap">'
        '<table class="effort-table"><thead><tr>'
        '<th>Anti-pattern</th><th class="ctr">Severity</th>'
        '<th class="num">Code units</th><th class="num">Occurrences</th>'
        '</tr></thead>'
        '<tbody data-role="flags">' + "".join(rows) + '</tbody></table></div>'
    )


def _occ_label(count: Any) -> str:
    n = int(count or 0)
    return f"{n} occurrence" if n == 1 else f"{n} occurrences"


def _filter_panel(kind: str, label: str, options_html: str) -> str:
    return (
        '<div class="ap-filter">'
        f'<button type="button" class="ap-filter-btn" onclick="apToggleFilterPanel(\'{kind}\', event)">'
        f'{label}<span class="ap-filter-count" id="ap-count-{kind}"></span>'
        '<span class="ap-caret">&#9662;</span></button>'
        f'<div class="ap-filter-panel" id="ap-panel-{kind}">'
        f'<div class="ap-filter-list">{options_html}</div>'
        '<div class="ap-filter-foot"><button type="button" class="ap-filter-clear" '
        f'onclick="apClearFilter(\'{kind}\')">Clear</button></div>'
        '</div></div>'
    )


def _render_cu_filters(flags: List[Dict], code_units: List[Dict]) -> str:
    types = sorted({cu.get("object_type", "") for cu in code_units if cu.get("object_type")})
    type_opts = "".join(
        f'<label class="ap-filter-opt"><input type="checkbox" class="ap-filter-cb" '
        f'data-kind="type" value="{_esc(t)}" onchange="apOnFilterChange()"/>{_esc(t)}</label>'
        for t in types
    )
    present_sev = {f.get("priority", "") for f in flags}
    sev_opts = "".join(
        f'<label class="ap-filter-opt"><input type="checkbox" class="ap-filter-cb" '
        f'data-kind="sev" value="{s}" onchange="apOnFilterChange()"/>'
        f'<span class="ap-dot ap-prio-{s}"></span>{s.title()}</label>'
        for s in _SEV_ORDER if s in present_sev
    )
    seen: set = set()
    ap_opts = []
    for f in flags:
        code = f.get("code", "")
        if code in seen:
            continue
        seen.add(code)
        ap_opts.append(
            f'<label class="ap-filter-opt"><input type="checkbox" class="ap-filter-cb" '
            f'data-kind="ap" value="{_esc(code)}" onchange="apOnFilterChange()"/>'
            f'{_esc(f.get("title", code))}</label>'
        )
    return (
        '<div class="ap-filters">'
        '<input class="ap-search" type="text" placeholder="Search code units by name&hellip;" '
        'oninput="apSearchCodeUnits(this.value)"/>'
        + _filter_panel("type", "Type", type_opts)
        + _filter_panel("sev", "Severity", sev_opts)
        + _filter_panel("ap", "Anti-pattern", "".join(ap_opts))
        + '</div>'
    )


def _render_code_unit_table(code_units: List[Dict], flags: List[Dict]) -> str:
    code_to_title = {f.get("code"): f.get("title", "") for f in flags}
    rows = []
    for i, cu in enumerate(code_units):
        cu_flags = cu.get("flags", [])
        buckets = " ".join(sorted({_esc(x.get("bucket", "")) for x in cu_flags}))
        severities = " ".join(sorted({_esc(x.get("priority", "")) for x in cu_flags}))
        codes = " ".join(sorted({_esc(x.get("code", "")) for x in cu_flags}))
        max_sev = _esc(_max_severity(cu_flags))
        name = cu.get("name", "")
        schema = cu.get("schema", "")
        obj_type = cu.get("object_type", "")
        canonical = f"{schema}.{name}" if schema else (name or cu.get("id", ""))

        chips = "".join(
            f'<span class="ap-chip {_esc(x.get("priority", ""))}">'
            f'{_esc(code_to_title.get(x.get("code"), x.get("code", "")))}</span>'
            for x in cu_flags
        )
        detail_items = "".join(
            f'<li class="ap-detail-item">'
            f'<span class="ap-chip {_esc(x.get("priority", ""))}">'
            f'{_esc(code_to_title.get(x.get("code"), x.get("code", "")))}</span>'
            f'<span class="ap-detail-occ">{_esc(_occ_label(x.get("count", 0)))}</span></li>'
            for x in cu_flags
        )
        rows.append(
            f'<tr class="ap-cu-row" data-buckets="{buckets}" data-severities="{severities}" '
            f'data-codes="{codes}" data-type="{_esc(obj_type)}" data-name="{_esc(name).lower()}" '
            f'onclick="apToggleCodeUnit({i})">'
            f'<td class="ap-cu-name"><span class="expand-icon">&#9656;</span>{_esc(name)}</td>'
            f'<td class="ap-cu-type">{_esc(obj_type)}</td>'
            f'<td class="ctr ap-cu-sev"><span class="badge {max_sev}">{max_sev.title()}</span></td>'
            f'<td class="ap-cu-chips-cell">{chips}</td>'
            f'</tr>'
            f'<tr class="details-row ap-cu-detail" id="ap-cu-details-{i}"><td colspan="4">'
            f'<div class="ap-cu-details">'
            f'<div class="ap-cu-canonical"><span>Canonical name</span> {_esc(canonical)}</div>'
            f'<div class="ap-cu-detail-aps"><span class="ap-cu-detail-title">Anti-patterns</span>'
            f'<ul class="ap-detail-list">{detail_items}</ul></div>'
            f'</div></td></tr>'
        )
    return (
        f'<h2 {_AP_H2}>Affected code units</h2>'
        + _render_cu_filters(flags, code_units)
        + '<div class="effort-table-wrap ap-table-scroll"><table class="effort-table sticky"><thead><tr>'
        '<th class="ap-col-name">Code unit</th><th class="ap-col-type">Type</th>'
        '<th class="ap-col-sev ctr">Severity</th><th class="ap-col-aps">Anti-patterns</th>'
        '</tr></thead>'
        '<tbody data-role="code-units">' + "".join(rows) + '</tbody></table></div>'
    )


_JS = """
var apActiveBucket = null;
var apSearchTerm = '';
var apTypeFilter = [];
var apSevFilter = [];
var apApFilter = [];

function apToggleBucket(card) {
    var bucket = card.getAttribute('data-bucket');
    apActiveBucket = (apActiveBucket === bucket) ? null : bucket;
    document.querySelectorAll('#anti-patterns-report .ap-bucket-card').forEach(function (c) {
        c.classList.toggle('ap-selected', c.getAttribute('data-bucket') === apActiveBucket);
    });
    apApplyFilter();
}
function apReadFilters() {
    apTypeFilter = [];
    apSevFilter = [];
    apApFilter = [];
    document.querySelectorAll('#anti-patterns-report .ap-filter-cb:checked').forEach(function (cb) {
        var kind = cb.getAttribute('data-kind');
        if (kind === 'type') { apTypeFilter.push(cb.value); }
        else if (kind === 'sev') { apSevFilter.push(cb.value); }
        else if (kind === 'ap') { apApFilter.push(cb.value); }
    });
    apUpdateCount('type', apTypeFilter.length);
    apUpdateCount('sev', apSevFilter.length);
    apUpdateCount('ap', apApFilter.length);
}
function apUpdateCount(kind, n) {
    var el = document.getElementById('ap-count-' + kind);
    if (el) { el.textContent = n ? ' (' + n + ')' : ''; }
}
function apOnFilterChange() { apReadFilters(); apApplyFilter(); }
function apClearFilter(kind) {
    document.querySelectorAll('#anti-patterns-report .ap-filter-cb[data-kind="' + kind + '"]').forEach(function (cb) {
        cb.checked = false;
    });
    apOnFilterChange();
}
function apToggleFilterPanel(kind, ev) {
    if (ev) { ev.stopPropagation(); }
    var panel = document.getElementById('ap-panel-' + kind);
    var wasOpen = panel && panel.classList.contains('open');
    document.querySelectorAll('#anti-patterns-report .ap-filter-panel').forEach(function (p) { p.classList.remove('open'); });
    if (panel && !wasOpen) { panel.classList.add('open'); }
}
document.addEventListener('click', function (e) {
    if (!e.target || !e.target.closest || !e.target.closest('#anti-patterns-report .ap-filter')) {
        document.querySelectorAll('#anti-patterns-report .ap-filter-panel').forEach(function (p) { p.classList.remove('open'); });
    }
});
function apContainsAny(attrVal, selected) {
    if (!selected.length) { return true; }
    var items = (attrVal || '').split(' ');
    for (var i = 0; i < selected.length; i++) {
        if (items.indexOf(selected[i]) !== -1) { return true; }
    }
    return false;
}
function apApplyFilter() {
    document.querySelectorAll('#anti-patterns-report .ap-cat-row').forEach(function (row) {
        apSetRowVisible(row, !apActiveBucket || row.getAttribute('data-bucket') === apActiveBucket);
    });
    document.querySelectorAll('#anti-patterns-report .ap-cu-row').forEach(function (row) {
        var buckets = (row.getAttribute('data-buckets') || '').split(' ');
        var matchesBucket = !apActiveBucket || buckets.indexOf(apActiveBucket) !== -1;
        var matchesSearch = !apSearchTerm || (row.getAttribute('data-name') || '').indexOf(apSearchTerm) !== -1;
        var matchesType = !apTypeFilter.length || apTypeFilter.indexOf(row.getAttribute('data-type') || '') !== -1;
        var matchesSev = apContainsAny(row.getAttribute('data-severities'), apSevFilter);
        var matchesAp = apContainsAny(row.getAttribute('data-codes'), apApFilter);
        apSetRowVisible(row, matchesBucket && matchesSearch && matchesType && matchesSev && matchesAp);
    });
}
function apSetRowVisible(row, show) {
    row.style.display = show ? '' : 'none';
    var details = row.nextElementSibling;
    if (!show && details && details.classList.contains('details-row')) {
        details.classList.remove('show');
        row.classList.remove('open');
    }
}
function apToggleFlagRow(i) {
    var details = document.getElementById('ap-flag-details-' + i);
    if (!details) { return; }
    var open = details.classList.toggle('show');
    var row = details.previousElementSibling;
    if (row) { row.classList.toggle('open', open); }
}
function apToggleCodeUnit(i) {
    var details = document.getElementById('ap-cu-details-' + i);
    if (!details) { return; }
    var open = details.classList.toggle('show');
    var row = details.previousElementSibling;
    if (row) { row.classList.toggle('open', open); }
}
function apSearchCodeUnits(term) {
    apSearchTerm = (term || '').toLowerCase();
    apApplyFilter();
}
// Effort-card tooltips (KPIs + buckets) — follow cursor, mirrors the dependencies tab.
(function () {
    var tip = null;
    var SEL = '#anti-patterns-report .effort-card[data-tooltip]';
    function place(evt) {
        if (!tip) { return; }
        var x = Math.max(8, Math.min(evt.clientX + 14, window.innerWidth - tip.offsetWidth - 8));
        var y = Math.max(8, Math.min(evt.clientY + 14, window.innerHeight - tip.offsetHeight - 8));
        tip.style.left = x + 'px';
        tip.style.top = y + 'px';
    }
    document.addEventListener('mouseover', function (e) {
        var card = e.target.closest && e.target.closest(SEL);
        if (!card) { return; }
        if (tip) { tip.remove(); }
        tip = document.createElement('div');
        tip.className = 'metric-tooltip-cursor-dynamic';
        tip.textContent = card.getAttribute('data-tooltip') || '';
        document.body.appendChild(tip);
        place(e);
    });
    document.addEventListener('mousemove', function (e) { if (tip) { place(e); } });
    document.addEventListener('mouseout', function (e) {
        var card = e.target.closest && e.target.closest(SEL);
        if (card && tip) { tip.remove(); tip = null; }
    });
})();
"""

def _severity_css() -> str:
    lines = []
    for sev, style in _SEV_STYLES.items():
        accent = style["bar"]
        lines.append(
            f"#anti-patterns-report .ap-prio-{sev}, "
            f"#anti-patterns-report .ap-dot.ap-prio-{sev} "
            f"{{ background: {accent}; }}"
        )
        lines.append(
            f"#anti-patterns-report .badge.{sev}, "
            f"#anti-patterns-report .ap-chip.{sev} "
            f"{{ background: {style['bg']}; color: {style['text']}; "
            f"border-color: {style['border']}; }}"
        )
    return "\n".join(lines)


_CSS = (
    """
/* KPI + category cards reuse shared .effort-cards / .effort-card from the document head */
#anti-patterns-report .effort-card[data-tooltip] { cursor: help; }
#anti-patterns-report .ap-bucket-caption { font-size: 12px; font-weight: 600; color: #5D6A85; text-transform: uppercase; letter-spacing: 0.04em; margin: 18px 0 8px; }
#anti-patterns-report .ap-bucket-card { cursor: pointer; }
#anti-patterns-report .ap-bucket-card.ap-selected { border-color: var(--sf-blue); box-shadow: 0 0 0 2px var(--sf-blue); }
#anti-patterns-report .ap-bucket-empty { padding: 16px; margin: 8px 0; border: 1px dashed var(--border-color); border-radius: 8px; background: #f8fafc; color: var(--text-secondary); }
/* Severity distribution bar — mid-tone accents (between pastel fills and deep bar) */
#anti-patterns-report .ap-priority { margin-top: 18px; }
#anti-patterns-report .ap-prio-bar { display: flex; gap: 2px; height: 14px; border-radius: 7px; overflow: hidden; background: var(--border-color); }
#anti-patterns-report .ap-prio-seg { min-width: 0; }
"""
    + _severity_css()
    + """
#anti-patterns-report .ap-prio-legends { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 8px; font-size: 12px; color: var(--text-secondary); }
#anti-patterns-report .ap-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; }
/* Filter bar (mirrors the dependencies-tab .filters panel) */
#anti-patterns-report .ap-filters { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; background: #EEF6F7; border: 1px solid #CFECEF; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; }
#anti-patterns-report .ap-search { flex: 1 1 260px; padding: 8px 12px; border: 1px solid #B6D5F3; border-radius: 6px; font-size: 14px; background: #FCFFFE; }
#anti-patterns-report .ap-search:focus { outline: none; border-color: #005C8F; }
#anti-patterns-report .ap-filter { position: relative; }
#anti-patterns-report .ap-filter-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 12px; border: 1px solid #B6D5F3; border-radius: 6px; background: #FCFFFE; font-size: 13px; color: #005C8F; font-weight: 600; cursor: pointer; }
#anti-patterns-report .ap-filter-btn:hover { background: #E1F0F3; }
#anti-patterns-report .ap-filter-count { color: var(--sf-blue); font-weight: 700; }
#anti-patterns-report .ap-caret { font-size: 10px; color: var(--text-secondary); }
#anti-patterns-report .ap-filter-panel { display: none; position: absolute; z-index: 50; top: calc(100% + 6px); left: 0; min-width: 220px; max-width: 340px; background: #fff; border: 1px solid #D5DAE4; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.12); padding: 8px; }
#anti-patterns-report .ap-filter-panel.open { display: block; }
#anti-patterns-report .ap-filter-list { max-height: 260px; overflow: auto; }
#anti-patterns-report .ap-filter-opt { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px; font-size: 13px; color: #2A3342; cursor: pointer; }
#anti-patterns-report .ap-filter-opt:hover { background: #f1f5f9; }
#anti-patterns-report .ap-filter-foot { display: flex; justify-content: flex-end; border-top: 1px solid var(--border-color); margin-top: 6px; padding-top: 6px; }
#anti-patterns-report .ap-filter-clear { padding: 5px 10px; font-size: 12px; border: 1px solid var(--border-color); border-radius: 6px; background: #fff; color: var(--sf-dark-blue); cursor: pointer; }
#anti-patterns-report .ap-table-scroll { max-height: 560px; overflow: auto; }
#anti-patterns-report .effort-table { table-layout: fixed; }
#anti-patterns-report .ap-cat-row { cursor: pointer; }
#anti-patterns-report .ap-cat-name { font-weight: 600; }
#anti-patterns-report .ap-cat-sev { white-space: nowrap; }
#anti-patterns-report .expand-icon { display: inline-block; margin-right: 8px; transition: transform 0.15s; color: var(--sf-dark-blue); }
#anti-patterns-report .ap-cat-row.open .expand-icon,
#anti-patterns-report .ap-cu-row.open .expand-icon { transform: rotate(90deg); }
#anti-patterns-report .ap-cu-row { cursor: pointer; }
#anti-patterns-report .ap-col-name { width: 38%; }
#anti-patterns-report .ap-col-type { width: 16%; }
#anti-patterns-report .ap-col-sev { width: 14%; }
#anti-patterns-report .ap-col-aps { width: 32%; }
#anti-patterns-report .ap-cu-name { font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#anti-patterns-report .ap-cu-type { color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#anti-patterns-report .ap-cu-sev { white-space: nowrap; }
#anti-patterns-report .ap-cu-chips-cell { white-space: normal; }
#anti-patterns-report .ap-cu-chips-cell .ap-chip { margin: 2px 6px 2px 0; }
/* Expandable detail rows (shared by catalog + code units) */
#anti-patterns-report .details-row { display: none; }
#anti-patterns-report .details-row.show { display: table-row; }
#anti-patterns-report .details-row > td { background: #f8fafc; }
#anti-patterns-report .ap-flag-body { padding: 6px 4px 10px; }
#anti-patterns-report .ap-block { border-left: 4px solid #005C8F; padding: 6px 12px; margin-top: 10px; background: #fff; }
#anti-patterns-report .ap-block h4 { margin: 0 0 4px; font-size: 13px; }
#anti-patterns-report .ap-block p { margin: 0; }
#anti-patterns-report .ap-block.ap-rec { border-left-color: #10b981; }
#anti-patterns-report .ap-block.ap-why { border-left-color: #FF9F36; }
#anti-patterns-report .ap-doc-ref { display: inline-block; margin-top: 10px; font-size: 12px; color: var(--sf-dark-blue); }
#anti-patterns-report .ap-cu-details { padding: 6px 4px; }
#anti-patterns-report .ap-cu-canonical { font-size: 13px; color: var(--text-primary); }
#anti-patterns-report .ap-cu-canonical span { color: var(--text-secondary); text-transform: uppercase; font-size: 11px; letter-spacing: 0.04em; margin-right: 6px; }
#anti-patterns-report .ap-cu-detail-aps { margin-top: 10px; }
#anti-patterns-report .ap-cu-detail-title { display: block; color: var(--text-secondary); text-transform: uppercase; font-size: 11px; letter-spacing: 0.04em; margin-bottom: 6px; }
#anti-patterns-report .ap-detail-list { list-style: none; margin: 0; padding: 0; }
#anti-patterns-report .ap-detail-item { display: flex; align-items: center; gap: 10px; padding: 3px 0; }
#anti-patterns-report .ap-detail-occ { font-size: 12px; color: var(--text-secondary); }
/* Badges + chips — palette generated from _SEV_STYLES */
#anti-patterns-report .ap-empty { padding: 40px; text-align: center; color: var(--text-secondary); }
#anti-patterns-report .badge,
#anti-patterns-report .ap-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid transparent;
  white-space: nowrap;
}
"""
)
