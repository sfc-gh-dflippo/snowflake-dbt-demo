# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

"""Load and render Extended Events workload-insights artifacts."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

_SCHEMA_VERSION = 2
_SOURCE = "extended_events"
_MAPPING_FIELDS = ("summary", "kpis", "long_running", "errors")
_SEQUENCE_FIELDS = (
    "duration_histogram",
    "daily",
    "statement_mix",
    "statement_groups",
    "apps",
    "users",
    "connection_context",
)
_COLORS = [
    "#1E6FD9",
    "#29B5E8",
    "#B3BCCB",
    "#2E9E64",
    "#F0B429",
    "#8B1A1A",
    "#E8843C",
]
# Duration buckets read fastest-to-slowest, so the strip runs green to red in the
# same order the histogram lists them.
_BUCKET_COLORS = [
    "#2E9E64",
    "#1E6FD9",
    "#F0B429",
    "#E8843C",
    "#D9534F",
]


def is_sql_server(source_dialect: str) -> bool:
    """Return whether the multi-report dialect token is SQL Server."""
    return source_dialect == "Transact"


def _is_mapping_sequence(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(row, dict) for row in value)


def load_workload_insights(path: Path) -> Optional[dict[str, Any]]:
    """Load a strict schema-v2 Extended Events artifact."""
    try:
        with Path(path).open(encoding="utf-8") as stream:
            payload = json.load(stream)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Warning: Could not load workload insights data: {exc}", file=sys.stderr)
        return None

    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != _SCHEMA_VERSION
        or payload.get("source") != _SOURCE
    ):
        print(
            "Warning: Could not load workload insights data: unsupported schema or source",
            file=sys.stderr,
        )
        return None

    valid = all(isinstance(payload.get(field), dict) for field in _MAPPING_FIELDS)
    valid = valid and all(
        _is_mapping_sequence(payload.get(field)) for field in _SEQUENCE_FIELDS
    )
    long_running = payload.get("long_running")
    errors = payload.get("errors")
    valid = (
        valid
        and isinstance(long_running, dict)
        and all(
            _is_mapping_sequence(long_running.get(field))
            for field in ("by_type", "top")
        )
    )
    valid = (
        valid
        and isinstance(errors, dict)
        and _is_mapping_sequence(errors.get("event_mix"))
    )
    if not valid:
        print(
            "Warning: Could not load workload insights data: invalid schema shape",
            file=sys.stderr,
        )
        return None
    return payload


def _esc(value: Any) -> str:
    return html.escape(str(value)) if value is not None else ""


def _text(value: Any) -> str:
    return _esc(value).replace("·", "&middot;")


def _num(value: Any, default: float = 0.0) -> float:
    """Coerce a JSON number; missing, null, or junk becomes default."""
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _fmt_int(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return _esc(value)


def _fmt_number(value: Any, digits: int = 1) -> str:
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return _esc(value)


def _fmt_pct(value: Any) -> str:
    return f"{_fmt_number(value)}%"


def _fmt_day(value: Any) -> str:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo:
            parsed = parsed.astimezone(timezone.utc)
        return parsed.strftime("%b %d, %Y")
    except (TypeError, ValueError):
        return _esc(value) or "Not available"


def _day_tick(value: Any) -> str:
    """Format a capture day as a short axis tick (month and year live in the title)."""
    day = _parse_day(value)
    return f"{day:%d %b}" if day else (_esc(value) or "")


def _day_axis_title(daily: Sequence[Mapping[str, Any]]) -> str:
    days = [day for day in (_parse_day(row.get("day")) for row in daily) if day]
    if not days:
        return "Day of capture"
    first, last = min(days), max(days)
    if (first.year, first.month) == (last.year, last.month):
        span = f"{first:%B %Y}"
    elif first.year == last.year:
        span = f"{first:%B} – {last:%B} {last.year}"
    else:
        span = f"{first:%B %Y} – {last:%B %Y}"
    return f"Day of capture ({span})"


def _parse_day(value: Any) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _fmt_duration(value: Any) -> str:
    try:
        milliseconds = float(value)
    except (TypeError, ValueError):
        return _esc(value)
    if milliseconds >= 60_000:
        return f"{milliseconds / 60_000:.1f} min"
    return f"{milliseconds:,.1f} ms"


def _safe_json(value: Any) -> str:
    serialized = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (
        serialized.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _header() -> str:
    return """
<header class="wi-header">
  <h1>Discovery</h1>
  <p class="wi-notice"><strong>Disclaimer:</strong> Captured Extended Events data,
  including SQL statement text, is used for <strong>reporting only</strong>.
  Statement text is read only to classify the type of query
  (for example SELECT, Call, or INSERT). It is <strong>not stored</strong> in
  the assessment artifact and is <strong>not shown</strong> in this report
  &mdash; no query text, parameters, or error messages appear here.</p>
  <p class="wi-blurb">Insights from the SQL Server <strong>Extended Events</strong>
  capture provided for this project. Each row in the capture is
  <strong>one statement execution</strong> &mdash; not an aggregate &mdash; so durations
  and counts describe individual runs rather than averaged query shapes.</p>
</header>"""


def _summary(payload: Mapping[str, Any]) -> str:
    summary = payload["summary"]
    databases = ", ".join(_esc(item) for item in summary.get("databases", []))
    day_count = len(payload["daily"])
    day_word = "day" if day_count == 1 else "days"
    return f"""
<div class="wi-summary">
  <div><strong>Database</strong><br>{databases or "Not available"}</div>
  <div><strong>Capture window</strong><br>{_fmt_day(summary.get("first_seen"))}
    &ndash; {_fmt_day(summary.get("last_seen"))} &middot; {day_count} {day_word}</div>
  <div><strong>Capture filters</strong><br>{_text(summary.get("capture_filters"))}</div>
</div>"""


def _kpis(payload: Mapping[str, Any]) -> str:
    kpis = payload["kpis"]
    cards = [
        ("Total events", _fmt_int(kpis.get("total_events"))),
        ("User executions", _fmt_int(kpis.get("user_executions"))),
        ("Sub-second", _fmt_pct(kpis.get("sub_second_pct"))),
        ("Executions &gt; 5 s", _fmt_int(kpis.get("executions_over_5s"))),
        ("Error rate", _fmt_pct(kpis.get("error_rate_pct"))),
    ]
    body = "".join(
        f'<div class="wi-kpi"><span class="wi-kpi-value">{value}</span>'
        f'<span class="wi-kpi-label">{label}</span></div>'
        for label, value in cards
    )
    return f'<div class="wi-kpis">{body}</div>'


def _section(title: str, body: str) -> str:
    return f"""
<section class="wi-section">
  <h2>{title}</h2>
  {body}
</section>"""


def _chart(chart_id: str, *, tall: bool = False) -> str:
    class_name = "wi-chart-frame wi-chart-frame-tall" if tall else "wi-chart-frame"
    return f'<div class="{class_name}"><canvas id="{chart_id}"></canvas></div>'


def _duration_section(payload: Mapping[str, Any]) -> str:
    histogram = payload["duration_histogram"]
    max_count = max((_num(row.get("executions")) for row in histogram), default=0)
    rows = []
    insights = []
    for index, row in enumerate(histogram):
        count = _num(row.get("executions"))
        width = 100 * count / max_count if max_count else 0
        color = _BUCKET_COLORS[index % len(_BUCKET_COLORS)]
        rows.append(
            '<div class="wi-bucket-row">'
            f'<span class="wi-bucket-label">{_esc(row.get("bucket"))}</span>'
            '<span class="wi-bucket-track">'
            f'<span class="wi-bucket-bar" '
            f'style="width:{width:.1f}%;background:{color}"></span></span>'
            f'<span class="wi-bucket-count">{_fmt_int(count)}</span>'
            f"<strong>{_fmt_pct(row.get('pct'))}</strong></div>"
        )
        insights.append(
            '<div class="wi-insight">'
            f'<div class="wi-insight-value" style="color:{color}">'
            f"{_fmt_pct(row.get('pct'))}</div>"
            f'<div class="wi-insight-label">{_esc(row.get("bucket"))}</div>'
            f'<div class="wi-insight-sub">{_fmt_int(count)} executions</div></div>'
        )
    body = f"""
<div class="wi-insights">{"".join(insights)}</div>
<div class="wi-grid-2">
  <div class="wi-card"><h3>Bucket breakdown &mdash; captured user executions</h3>
    {"".join(rows)}
  </div>
  <div class="wi-card"><h3>Duration bucket distribution (log scale)</h3>
    {_chart("wi-chart-histogram")}
  </div>
</div>
<p class="wi-callout"><strong>Capture floor:</strong> the session records nothing below
0.5 s, so faster statements are absent by design. Read the sub-second share as a
floor, not a total.</p>"""
    return _section("Query performance histogram &mdash; duration buckets", body)


def _timeline_section(payload: Mapping[str, Any]) -> str:
    daily = payload["daily"]
    peak = max(daily, key=lambda row: row.get("executions", 0), default={})
    quiet = min(daily, key=lambda row: row.get("executions", 0), default={})
    executions = _num(payload["kpis"].get("user_executions"))
    average = executions / len(daily) if daily else 0
    body = f"""
<div class="wi-card"><h3>Executions per day &mdash; stacked by duration bucket</h3>
  {_chart("wi-chart-daily", tall=True)}
</div>
<div class="wi-stat-grid">
  <div class="wi-stat"><span>Peak day</span><strong>{_fmt_int(peak.get("executions", 0))}</strong>
    <small>{_esc(peak.get("day"))}</small></div>
  <div class="wi-stat"><span>Quietest day</span><strong>{_fmt_int(quiet.get("executions", 0))}</strong>
    <small>{_esc(quiet.get("day"))}</small></div>
  <div class="wi-stat"><span>Average per day</span><strong>{_fmt_number(average)}</strong>
    <small>{_fmt_int(executions)} executions / {len(daily)} days</small></div>
</div>
<div class="wi-card"><h3>Executions and errors across the window</h3>
  {_chart("wi-chart-timeline")}
</div>"""
    return _section("Query execution timeline", body)


def _table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    head = "".join(f"<th>{header}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    if not body:
        body = (
            f'<tr><td colspan="{len(headers)}" class="wi-empty-row">'
            "No rows were recorded for this section.</td></tr>"
        )
    return (
        '<div class="wi-table-wrap"><table><thead><tr>'
        f"{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def _classification_section(payload: Mapping[str, Any]) -> str:
    mix = payload["statement_mix"]
    mix_total = sum(_num(row.get("executions")) for row in mix)
    rows = [
        [
            _esc(row.get("statement_type")),
            _fmt_int(row.get("executions")),
            _fmt_pct(row.get("pct")),
        ]
        for row in mix
    ]
    body = f"""
<div class="wi-grid-2">
  <div class="wi-card"><h3>Statement types ({_fmt_int(mix_total)} executions)</h3>
    {_chart("wi-chart-types")}</div>
  <div class="wi-card"><h3>Statement groups</h3>{_chart("wi-chart-groups")}</div>
</div>
<div class="wi-card"><h3>Statement type distribution</h3>
  {_table(["Statement type", "Count", "% share"], rows)}
</div>"""
    return _section("Query type &amp; workload classification", body)


def _connections_section(payload: Mapping[str, Any]) -> str:
    rows = [
        [
            f"<strong>{_esc(row.get('user'))}</strong> &middot; "
            f'<span class="wi-mono">{_esc(row.get("app"))}</span>',
            f"{_fmt_int(row.get('executions'))} ({_fmt_pct(row.get('pct'))})",
        ]
        for row in payload["connection_context"]
    ]
    body = f"""
<div class="wi-grid-2">
  <div class="wi-card"><h3>Top applications (client_app_name)</h3>
    {_chart("wi-chart-apps")}</div>
  <div class="wi-card"><h3>Top users (username)</h3>
    {_chart("wi-chart-users")}</div>
</div>
<div class="wi-card"><h3>User and connection context</h3>
  {_table(["User &middot; application", "Captured executions"], rows)}
</div>"""
    return _section("Applications &amp; users", body)


def _long_running_section(payload: Mapping[str, Any]) -> str:
    long_running = payload["long_running"]
    total = long_running.get("total", 0)
    rows = [
        [
            _fmt_int(row.get("rank")),
            f"<strong>{_fmt_duration(row.get('duration_ms'))}</strong>",
            _fmt_number(row.get("cpu_ms")),
            f"{_num(row.get('cpu_share')) * 100:.0f}%",
            _fmt_int(row.get("reads")),
            _fmt_int(row.get("writes")),
            _fmt_int(row.get("rows")),
            _esc(row.get("statement_type")),
        ]
        for row in long_running.get("top", [])
    ]
    bands = [
        ("5 &ndash; 10 s", long_running.get("band_5_10"), "#E8843C", ""),
        ("10 &ndash; 30 s", long_running.get("band_10_30"), "#D9534F", ""),
        (
            "Over 30 s",
            long_running.get("band_over_30"),
            "#8B1A1A",
            f" &middot; max is {_fmt_duration(long_running.get('max_duration_ms'))}",
        ),
    ]
    band_total = sum(_num(count) for _, count, _, _ in bands)
    band_tiles = "".join(
        f'<div class="wi-stat"><span>{label}</span>'
        f'<strong style="color:{color}">{_fmt_int(count)}</strong>'
        f"<small>{_fmt_pct(100 * _num(count) / band_total if band_total else 0)}"
        f" of long-runners{suffix}</small></div>"
        for label, count, color, suffix in bands
    )
    body = f"""
<p class="wi-danger-callout"><strong>{_fmt_int(total)} executions</strong> ran longer
than 5 seconds &mdash; {_fmt_pct(long_running.get("pct_of_executions"))} of the
captured workload.</p>
<div class="wi-stat-grid">{band_tiles}</div>
<div class="wi-card"><h3>Long executions (&gt; 5 s) by statement type</h3>
  {_chart("wi-chart-long")}</div>
<div class="wi-card"><h3>Longest captured executions &mdash; top 10 of
{_fmt_int(total)} past 5 seconds</h3>
  <div class="wi-long-table">
    {_table(["#", "Duration", "CPU ms", "CPU share", "Reads", "Writes", "Rows", "Statement"], rows)}
  </div>
</div>"""
    return _section("Long-running query analysis (&gt; 5 seconds)", body)


def _errors_section(payload: Mapping[str, Any]) -> str:
    errors = payload["errors"]
    kpis = payload["kpis"]
    body = f"""
<div class="wi-grid-2">
  <div class="wi-card"><h3>Severity overview</h3>
    <div class="wi-tiles">
      <div class="wi-tile">
        <div class="wi-tile-value" style="color:#D9534F">{_fmt_int(errors.get("count"))}</div>
        <div class="wi-tile-label">Captured error events</div>
        <div class="wi-tile-sub">severity &ge; {_fmt_int(errors.get("severity_floor"))}</div>
      </div>
      <div class="wi-tile">
        <div class="wi-tile-value" style="color:#F0B429">{_fmt_pct(kpis.get("error_rate_pct"))}</div>
        <div class="wi-tile-label">Trace error ratio</div>
        <div class="wi-tile-sub">{_fmt_int(errors.get("count"))} errors / {_fmt_int(kpis.get("total_events"))} events</div>
      </div>
    </div>
  </div>
  <div class="wi-card"><h3>Captured event mix</h3>
    {_chart("wi-chart-event-mix")}</div>
</div>"""
    return _section("Error &amp; exception analysis", body)


def _chart_data(payload: Mapping[str, Any]) -> dict[str, Any]:
    histogram = payload["duration_histogram"]
    daily = payload["daily"]
    statement_mix = payload["statement_mix"]
    statement_groups = payload["statement_groups"]
    apps = payload["apps"]
    users = payload["users"]
    long_by_type = payload["long_running"]["by_type"]
    event_mix = payload["errors"]["event_mix"]
    return {
        "histo": {
            "labels": [row.get("bucket") for row in histogram],
            "values": [row.get("executions") for row in histogram],
        },
        "dayAxis": _day_axis_title(daily),
        "daily": {
            "labels": [row.get("day") for row in daily],
            "ticks": [_day_tick(row.get("day")) for row in daily],
            "lt1": [row.get("lt1") for row in daily],
            "s1_10": [row.get("s1_10") for row in daily],
            "s10_30": [row.get("s10_30") for row in daily],
            "gt30": [row.get("gt30") for row in daily],
            "executions": [row.get("executions") for row in daily],
            "errors": [row.get("errors") for row in daily],
        },
        "types": {
            "labels": [row.get("statement_type") for row in statement_mix],
            "values": [row.get("executions") for row in statement_mix],
        },
        "groups": {
            "labels": [row.get("group") for row in statement_groups],
            "values": [row.get("executions") for row in statement_groups],
        },
        "apps": {
            "labels": [row.get("app") for row in apps],
            "values": [row.get("executions") for row in apps],
        },
        "users": {
            "labels": [row.get("user") for row in users],
            "values": [row.get("executions") for row in users],
        },
        "longByType": {
            "labels": [row.get("statement_type") for row in long_by_type],
            "values": [row.get("executions") for row in long_by_type],
        },
        "eventMix": {
            "labels": [row.get("event") for row in event_mix],
            "values": [row.get("count") for row in event_mix],
        },
    }


def _copy_script_js() -> str:
    """Copy handler for the empty-state capture script, same pattern as DMV SQL."""
    return """
(function() {
document.addEventListener("click", function(event) {
  const button = event.target && event.target.closest && event.target.closest("[data-wi-copy]");
  if (!button) return;
  const source = document.getElementById(button.getAttribute("data-wi-copy"));
  if (!source) return;
  const text = source.innerText || source.textContent || "";
  const original = button.textContent;
  const flash = function() {
    button.textContent = "Copied";
    setTimeout(function() { button.textContent = original; }, 1500);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(flash).catch(function() {
      const area = document.createElement("textarea");
      area.value = text;
      document.body.appendChild(area);
      area.select();
      document.execCommand("copy");
      document.body.removeChild(area);
      flash();
    });
  }
});
})();
"""


def workload_insights_chart_js(payload: Optional[Mapping[str, Any]]) -> str:
    """Return chart bootstrap JavaScript for emission after the Vue mount."""
    if not payload or not payload.get("found"):
        return _copy_script_js()
    data = _safe_json(_chart_data(payload))
    colors = _safe_json(_COLORS)
    bucket_colors = _safe_json(_BUCKET_COLORS)
    return f"""
(function() {{
const D={data};
const PAL={colors};
const axes={{color:"#64748B"}};
const barOptions={{indexAxis:"y",responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{display:false}}}},
  scales:{{x:{{beginAtZero:true,grid:{{color:"#E2E8F0"}},...axes}},
  y:{{grid:{{display:false}}}}}}}};
const histogramDisplay=D.histo.values.map(value => value === 0 ? null : value);
const bucketColors={bucket_colors};
const dayScales=(yTitle,stacked=false) => ({{
  x:{{stacked:stacked,ticks:{{maxRotation:60,font:{{size:9}}}},grid:{{display:false}},
  title:{{display:true,text:D.dayAxis,...axes}}}},
  y:{{stacked:stacked,beginAtZero:true,grid:{{color:"#E2E8F0"}},
  title:{{display:true,text:yTitle,...axes}}}}}});
window.renderWorkloadInsightsCharts=function() {{
const charts=window.__workloadInsightsCharts || {{}};
if(Object.keys(charts).length) {{
  Object.values(charts).forEach(chart => chart.resize());
  return;
}}
const make=(id,config) => {{
  const canvas=document.getElementById(id);
  if(canvas) charts[id]=new Chart(canvas,config);
}};
make("wi-chart-histogram",{{
  type:"bar",data:{{labels:D.histo.labels,datasets:[{{label:"Executions",
  data:histogramDisplay,backgroundColor:bucketColors,borderRadius:4}}]}},
  options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
  scales:{{x:{{grid:{{display:false}}}},y:{{type:"logarithmic",min:0.8,
  title:{{display:true,text:"Executions (log scale)",...axes}}}}}}}}}});
make("wi-chart-daily",{{
  type:"bar",data:{{labels:D.daily.ticks,datasets:[
  {{label:"< 1 s",data:D.daily.lt1,backgroundColor:"#2E9E64",stack:"s"}},
  {{label:"1 – 10 s",data:D.daily.s1_10,backgroundColor:"#1E6FD9",stack:"s"}},
  {{label:"10 – 30 s",data:D.daily.s10_30,backgroundColor:"#F0B429",stack:"s"}},
  {{label:"> 30 s",data:D.daily.gt30,backgroundColor:"#D9534F",stack:"s"}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{position:"top",labels:{{boxWidth:12,padding:10}}}}}},
  scales:dayScales("Executions",true)}}}});
make("wi-chart-timeline",{{
  type:"line",data:{{labels:D.daily.ticks,datasets:[
  {{label:"Executions",data:D.daily.executions,borderColor:"#29B5E8",
  backgroundColor:"rgba(41,181,232,.15)",fill:true,tension:.3}},
  {{label:"Errors",data:D.daily.errors,borderColor:"#D9534F",
  backgroundColor:"rgba(217,83,79,.12)",fill:true,tension:.3}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{position:"bottom",labels:{{boxWidth:12,padding:14}}}}}},
  scales:dayScales("Events")}}}});
for(const [id,src] of [["wi-chart-types",D.types],["wi-chart-groups",D.groups],["wi-chart-event-mix",D.eventMix]]){{
  const total=src.values.reduce((sum,value) => sum + (value || 0),0);
  const labels=src.labels.map((label,index) => total
    ? `${{label}} (${{(100*(src.values[index] || 0)/total).toFixed(1)}}%)`
    : label);
  make(id,{{type:"doughnut",
  data:{{labels:labels,datasets:[{{data:src.values,backgroundColor:PAL,
  borderColor:"#fff",borderWidth:2}}]}},
  options:{{responsive:true,maintainAspectRatio:false,cutout:"55%",
  plugins:{{legend:{{position:"bottom",
  labels:{{boxWidth:11,padding:9,font:{{size:11}}}}}}}}}}}});
}}
make("wi-chart-apps",{{
  type:"bar",data:{{labels:D.apps.labels,datasets:[{{data:D.apps.values,
  backgroundColor:"#FF9F36",borderRadius:4}}]}},options:barOptions}});
make("wi-chart-users",{{
  type:"bar",data:{{labels:D.users.labels,datasets:[{{data:D.users.values,
  backgroundColor:"#29B5E8",borderRadius:4}}]}},options:barOptions}});
make("wi-chart-long",{{
  type:"bar",data:{{labels:D.longByType.labels,datasets:[{{data:D.longByType.values,
  backgroundColor:PAL,borderRadius:4}}]}},
  options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
  scales:{{x:{{grid:{{display:false}}}},y:{{beginAtZero:true,grid:{{color:"#E2E8F0"}},
  title:{{display:true,text:"Count",...axes}}}}}}}}}});
window.__workloadInsightsCharts=charts;
}};
}})();"""


_SESSION_SQL = """-- SUGGESTED STARTER SCRIPT — review every value below with your DBA
-- before you run it. These are defaults that fit a typical host, not
-- a guarantee for this instance. This capture uses CPU and disk; it
-- is not free. Needs permission to create a server event session.
--
-- REQUIRED before execute:
--   * Replace YourDatabase in all three database_name predicates with
--     the one database you want to profile.
--   * Replace &lt;dedicated volume&gt; in the target filename with a path on
--     a volume that is not a data or log disk.
--   * If a session named WorkloadReport_XE already exists, change that
--     name in the CREATE statement and in the commented START / STOP
--     statements.
--   * CREATE only defines the session. Uncomment and run START when you
--     want capture to begin.
--
-- Review and change as needed (suggested values):
--   Session name            WorkloadReport_XE
--   Duration threshold      500000 microseconds (0.5 s). Raise to write
--                           less; lowering it costs more CPU and disk.
--   Filters                 one database, is_system = 0, no SSMS /
--                           telemetry, error severity >= 11. Removing
--                           the database predicate traces the instance.
--   filename                path + base name on a dedicated volume, not
--                           data or log disks.
--   max_file_size           200 MB per file
--   max_rollover_files      5  (1 GB cap at the default file size).
--                           Confirm more than that is free.
--   MAX_MEMORY              8192 KB. Keep this from competing with the
--                           buffer pool.
--   MAX_DISPATCH_LATENCY    30 seconds
--   STARTUP_STATE           OFF (session does not return after a
--                           restart; set ON only if you want it to)
--   MEMORY_PARTITION_MODE   Not set, which is right for a typical host.
--                           On a busy many-core server, partitioning
--                           buffers PER_CPU reduces contention when many
--                           queries finish at once. It splits MAX_MEMORY
--                           across cores, so raise MAX_MEMORY (16-32 MB)
--                           if you turn it on — 8192 KB spread over many
--                           cores drops more events.
--
-- Do not change:
--   The three events and their ACTION lists, or this report loses
--   columns. EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS — do not
--   switch to NO_EVENT_LOSS (that can stall user queries).

-- Create the session
CREATE EVENT SESSION [WorkloadReport_XE] ON SERVER

-- Event 1: ad-hoc SQL statements completed
ADD EVENT sqlserver.sql_statement_completed(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.client_hostname,
        sqlserver.session_id
    )
    WHERE (
        [duration] &gt;= 500000 -- microseconds, so 0.5 s
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] &lt;&gt; N'SQLServerCEIP'
        AND [sqlserver].[username] &lt;&gt; N'NT SERVICE\\SQLTELEMETRY'
        AND [sqlserver].[client_app_name] &lt;&gt; N'Microsoft SQL Server Management Studio'
    )
),

-- Event 2: stored procedure and RPC calls completed
ADD EVENT sqlserver.rpc_completed(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.client_hostname,
        sqlserver.session_id
    )
    WHERE (
        [duration] &gt;= 500000
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] &lt;&gt; N'SQLServerCEIP'
        AND [sqlserver].[username] &lt;&gt; N'NT SERVICE\\SQLTELEMETRY'
        AND [sqlserver].[client_app_name] &lt;&gt; N'Microsoft SQL Server Management Studio'
    )
),

-- Event 3: application and query errors
ADD EVENT sqlserver.error_reported(
    ACTION(
        sqlserver.database_name,
        sqlserver.username,
        sqlserver.client_app_name,
        sqlserver.session_id,
        sqlserver.sql_text
    )
    WHERE (
        [severity] &gt;= 11
        AND [sqlserver].[is_system] = 0
        AND [sqlserver].[database_name] = N'YourDatabase'
        AND [sqlserver].[client_app_name] &lt;&gt; N'Microsoft SQL Server Management Studio'
    )
)

-- Target: binary rollover files on disk. Point this at a volume that is
-- not a data or log disk; SQL Server appends its own suffix and .xel.
ADD TARGET package0.event_file(
    SET filename = N'&lt;dedicated volume&gt;\\XETraces\\WorkloadReport_XE',
    max_file_size = (200),   -- MB per file
    max_rollover_files = (5) -- 1 GB total at the default size
)
WITH (
    MAX_MEMORY = 8192 KB,                          -- session RAM cap
    EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS, -- do not change to NO_EVENT_LOSS
    MAX_DISPATCH_LATENCY = 30 SECONDS,             -- flush cadence
    STARTUP_STATE = OFF                            -- does not return after restart
    -- On a busy many-core host, add the line below and raise MAX_MEMORY
    -- to 16-32 MB first:
    -- , MEMORY_PARTITION_MODE = PER_CPU
);
GO

-- CREATE leaves the session stopped. Uncomment and run this to start
-- capture. Nothing is recorded until you do.
--
-- ALTER EVENT SESSION [WorkloadReport_XE] ON SERVER STATE = START;
-- GO

-- After you have collected data for the time you need, copy every .xel
-- file off the server, then run the statement below to stop the session.
-- Leaving it running keeps using CPU and disk. Use the same session name
-- as CREATE / START.
--
-- ALTER EVENT SESSION [WorkloadReport_XE] ON SERVER STATE = STOP;
-- GO"""

_HOW_TO_STEPS = [
    (
        "Start a workload capture on the database",
        "SQL Server keeps no history of past queries, so nothing can be reported "
        "until a capture is running. The script below creates a "
        "<strong>SQL Server Extended Events</strong> session on a single "
        "database; it does not start until you uncomment START. While it runs, "
        "it records each completed user statement and stored-procedure call "
        "that meets the duration filter &mdash; duration, CPU, reads, writes, "
        "rows, application, and user &mdash; plus errors at severity 11 or "
        "higher. Statement text is used only to classify the query type. "
        "Treat it as a starter, not a one-size-fits-all run: change the "
        "settings that do not fit this host. "
        "The three events and their <code>ACTION</code> lists must stay, "
        "or this report loses columns.",
        "",
    ),
    (
        "Let it run while the database handles real traffic",
        "The capture only records what happens after it starts, so leave it on "
        "long enough to be representative &mdash; around 30 days is a good "
        "target, though a shorter window still works. It writes a series of "
        "<code>.xel</code> files; copy all of them off the server when you are "
        "done, <strong>then stop the session</strong> (the stop statement is "
        "at the end of the script, commented out so it does not run with the "
        "start).",
        "",
    ),
    (
        "Re-run the assessment, then regenerate this report",
        "Re-run the assessment and give it the folder or files when the Discovery "
        "step asks for them, or run the command yourself:",
        "scai assessment workload-insights --input /path/to/capture.xel",
    ),
]

_HOW_TO_UNLOCKS = [
    "The capture window, the database covered, and the filters the capture used",
    "Total events, user executions, sub-second share, and error rate",
    "How execution times are distributed across duration buckets",
    "Executions and errors per day across the whole window",
    "The mix of statement types and groups making up the workload",
    "Which applications and users drive the captured work",
    "The longest executions, with CPU, reads, writes, and rows",
]


_HOW_TO_CONFIG = """
<p class="wi-dba-note"><strong>A DBA should own this capture.</strong> Have a DBA
set the values, confirm it is safe to run on this instance, and start it. Watch
the server once it is running &mdash; CPU, disk space, and waits &mdash; and stop
the session if anything degrades.</p>
<p class="wi-config-lead">This capture uses CPU and disk. It is reasonable on a
typical host with the defaults below, but it is <strong>not free</strong> and
it can compete with the database if those knobs are set too aggressively. Do
not switch <code>EVENT_RETENTION_MODE</code> to <code>NO_EVENT_LOSS</code>
&mdash; that can stall user queries.</p>
<div class="wi-config">
  <div class="wi-config-card">
    <h4>You can change these to fit the capture</h4>
    <ul>
      <li><strong>Session name</strong> &mdash; default is <code>WorkloadReport_XE</code>.
      Change it if another session already uses that name; keep the same name
      in the create and start statements.</li>
      <li><strong>Duration threshold</strong> &mdash; default is 0.5 s
      (<code>[duration] &gt;= 500000</code>, in microseconds). Raise it to write
      less; lowering it captures more and costs more CPU and disk.</li>
      <li><strong>Filters</strong> &mdash; default is one database, no system
      work, no SSMS / telemetry, and errors at severity &ge; 11. Tighten or
      loosen as needed. Removing the database predicate traces the whole
      instance and is usually too wide.</li>
    </ul>
  </div>
  <div class="wi-config-card wi-config-careful">
    <h4>Set these carefully &mdash; they affect the database</h4>
    <ul>
      <li><strong><code>filename</code></strong> &mdash; replace
      <code>&lt;dedicated volume&gt;</code> with a path on a volume that has
      space and is not a data or log disk. SQL Server appends its own suffix
      and <code>.xel</code>.</li>
      <li><strong><code>max_file_size</code></strong> (200 MB) and
      <strong><code>max_rollover_files</code></strong> (5) &mdash; together they
      cap disk at 1 GB. Confirm more than that is free before starting. Smaller
      caps use less disk; larger caps keep more history.</li>
      <li><strong><code>MAX_MEMORY</code></strong> (8,192 KB) &mdash; how much
      RAM the session may hold. Raising it buffers more events; leaving it low
      keeps it from competing with the buffer pool.</li>
      <li><strong><code>MAX_DISPATCH_LATENCY</code></strong> (30 seconds) &mdash;
      how soon events flush to disk. Lower it to write sooner; higher it to
      batch more.</li>
      <li><strong><code>STARTUP_STATE</code></strong> (OFF) &mdash; the session
      does not come back after a service restart. Set <code>ON</code> only if
      you want it to resume automatically, and still stop it when the capture
      window ends.</li>
      <li><strong><code>MEMORY_PARTITION_MODE</code></strong> &mdash; not set,
      which is right for a typical host. On a busy many-core server, set
      <code>PER_CPU</code> (commented in the script) to reduce contention when
      many queries finish at once, and raise <code>MAX_MEMORY</code> to
      16&ndash;32 MB first. Leaving 8,192 KB with <code>PER_CPU</code> drops
      more events.</li>
    </ul>
  </div>
</div>"""


def _how_to() -> str:
    session_sql = (
        '<details class="wi-howto-sql"><summary>Show the capture script</summary>'
        '<div class="wi-script-actions">'
        '<button type="button" class="wi-copy-btn" data-wi-copy="wi-session-sql">'
        "Copy</button></div>"
        f'<pre id="wi-session-sql">{_SESSION_SQL}</pre></details>'
    )
    steps = "".join(
        f'<div class="journey-card wi-step"><div class="journey-badge">{number}</div>'
        f'<div class="journey-card-body"><h3>{title}</h3><p>{copy}</p>'
        + (f"<pre>{command}</pre>" if command else "")
        + ((_HOW_TO_CONFIG + session_sql) if number == 1 else "")
        + "</div></div>"
        for number, (title, copy, command) in enumerate(_HOW_TO_STEPS, start=1)
    )
    unlocks = "".join(f"<li>{item}</li>" for item in _HOW_TO_UNLOCKS)
    return f"""
<p class="wi-empty-notice"><strong>No workload capture in this project yet.</strong>
This phase is <strong>optional</strong> &mdash; the rest of the assessment does not
depend on it.</p>
<h2 class="wi-how-to-title">How to capture workload data</h2>
<div class="journey-grid wi-how-to">{steps}</div>
<h2 class="wi-how-to-title">What a capture adds to this report</h2>
<ul class="wi-unlocks">{unlocks}</ul>"""


def render_workload_insights_tab_html(
    payload: Optional[Mapping[str, Any]],
) -> str:
    """Render inner Workload Insights HTML from artifact values."""
    if not payload or not payload.get("found"):
        return f'<div id="workload-insights-report" v-pre>{_header()}{_how_to()}</div>'
    return f"""<div id="workload-insights-report" v-pre>
{_header()}
{_summary(payload)}
{_kpis(payload)}
{_duration_section(payload)}
{_timeline_section(payload)}
{_classification_section(payload)}
{_connections_section(payload)}
{_long_running_section(payload)}
{_errors_section(payload)}
</div>"""


def workload_insights_css() -> str:
    """Return tab-scoped Workload Insights styles."""
    return """
#workload-insights-report { color: #102E46; }
#workload-insights-report .wi-header h1 {
  margin: 0 0 12px; font-size: 1.875rem; font-weight: 800; color: #102E46;
}
#workload-insights-report .wi-notice {
  color: #374151; background: #F3F4F6; border: 1px solid #D1D5DB;
  border-left: 4px solid #9CA3AF; border-radius: 6px; padding: 10px 12px;
  font-size: 0.78rem; line-height: 1.45; margin: 0 0 12px;
}
#workload-insights-report .wi-blurb { color: #64748B; font-size: 1.1rem; margin: 0; }
#workload-insights-report .wi-summary {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 16px; margin: 24px 0; color: #64748B; font-size: 0.85rem;
}
#workload-insights-report .wi-kpis {
  display: grid; grid-template-columns: repeat(5, 1fr); border: 1px solid #E2E8F0;
  border-radius: 12px; overflow: hidden;
}
#workload-insights-report .wi-kpi {
  display: flex; flex-direction: column; text-align: center; padding: 18px 10px;
  border-right: 1px solid #E2E8F0;
}
#workload-insights-report .wi-kpi:last-child { border-right: 0; }
#workload-insights-report .wi-kpi-value { font-size: 1.35rem; font-weight: 800; }
#workload-insights-report .wi-kpi-label {
  color: #64748B; font-size: 0.68rem; text-transform: uppercase;
}
#workload-insights-report .wi-section { margin: 44px 0; }
#workload-insights-report .wi-section h2 {
  font-size: 1.5rem; font-weight: 700; color: #102E46; margin: 0 0 20px;
}
#workload-insights-report .wi-insights {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 14px; margin-bottom: 20px;
}
#workload-insights-report .wi-insight {
  border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px 16px;
  text-align: center; min-width: 0;
}
#workload-insights-report .wi-insight-value {
  font-size: 1.75rem; font-weight: 900; line-height: 1; margin-bottom: 5px;
}
#workload-insights-report .wi-insight-label {
  color: #64748B; font-size: 0.7rem; text-transform: uppercase;
  letter-spacing: 0.4px;
}
#workload-insights-report .wi-insight-sub {
  color: #64748B; font-size: 0.72rem; margin-top: 4px;
}
#workload-insights-report .wi-tiles {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;
}
#workload-insights-report .wi-tile {
  background: #F8FAFC; border-radius: 8px; padding: 16px; text-align: center;
  min-width: 0;
}
#workload-insights-report .wi-tile-value { font-size: 1.9rem; font-weight: 800; }
#workload-insights-report .wi-tile-label {
  color: #64748B; font-size: 0.75rem; margin-top: 4px;
}
#workload-insights-report .wi-tile-sub { color: #64748B; font-size: 0.7rem; }
#workload-insights-report .wi-card {
  border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px 22px;
  margin-bottom: 16px; min-width: 0;
}
#workload-insights-report .wi-card h3 {
  color: #64748B; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.6px; margin: 0 0 14px;
}
#workload-insights-report .wi-grid-2 {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px;
}
#workload-insights-report .wi-chart-frame { position: relative; height: 290px; }
#workload-insights-report .wi-chart-frame-tall { height: 340px; }
#workload-insights-report .wi-bucket-row {
  display: flex; align-items: center; gap: 12px; padding: 10px; margin-bottom: 8px;
  background: #F8FAFC; border-radius: 8px;
}
#workload-insights-report .wi-bucket-label { width: 120px; font-weight: 700; }
#workload-insights-report .wi-bucket-track {
  flex: 1; height: 24px; overflow: hidden; background: #E8ECF2; border-radius: 6px;
}
#workload-insights-report .wi-bucket-bar {
  display: block; height: 100%; background: #29B5E8; border-radius: 6px;
}
#workload-insights-report .wi-bucket-count { width: 60px; text-align: right; }
#workload-insights-report .wi-callout,
#workload-insights-report .wi-danger-callout,
#workload-insights-report .wi-empty-notice {
  border-radius: 8px; padding: 13px 17px; margin: 0 0 18px;
  font-size: 0.83rem; line-height: 1.55;
}
#workload-insights-report .wi-callout { background: #FEF9E7; border-left: 4px solid #FF9F36; }
#workload-insights-report .wi-danger-callout { background: #FDEDEC; border-left: 4px solid #D9534F; }
#workload-insights-report .wi-empty-notice { background: #F0F9FF; border: 1px solid #BAE6FD; }
#workload-insights-report .wi-stat-grid {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px;
  margin-bottom: 16px;
}
#workload-insights-report .wi-stat-grid-2 { grid-template-columns: repeat(2, 1fr); }
#workload-insights-report .wi-stat {
  display: flex; flex-direction: column; text-align: center; padding: 18px;
  border: 1px solid #E2E8F0; border-radius: 10px;
}
#workload-insights-report .wi-stat strong { font-size: 1.7rem; }
#workload-insights-report .wi-stat small { color: #64748B; }
#workload-insights-report .wi-table-wrap {
  overflow-x: auto; border: 1px solid #E2E8F0; border-radius: 8px;
}
#workload-insights-report table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
#workload-insights-report th {
  padding: 10px 13px; text-align: left; background: #F8FAFC; white-space: nowrap;
}
#workload-insights-report td { padding: 9px 13px; border-top: 1px solid #E2E8F0; }
#workload-insights-report td:not(:first-child),
#workload-insights-report th:not(:first-child) { text-align: right; }
#workload-insights-report .wi-long-table th:last-child,
#workload-insights-report .wi-long-table td:last-child { text-align: left; }
#workload-insights-report .wi-mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#workload-insights-report .wi-how-to-title {
  font-size: 1.35rem; font-weight: 700; color: #102E46; margin: 40px 0 16px;
}
#workload-insights-report .wi-how-to { margin: 0; }
#workload-insights-report .wi-step { align-items: flex-start; cursor: default; }
#workload-insights-report .wi-step:hover {
  border-color: #E2E8F0; box-shadow: none; transform: none;
}
#workload-insights-report .wi-step pre {
  white-space: pre-wrap; overflow-wrap: anywhere; background: #F8FAFC;
  border-radius: 6px; padding: 10px 12px; margin: 10px 0 0;
  font-size: 0.82rem; color: #102E46;
}
#workload-insights-report .wi-howto-sql { margin-top: 12px; }
#workload-insights-report .wi-script-actions { display: flex; gap: 8px; margin: 10px 0 8px; }
#workload-insights-report .wi-copy-btn {
  font: inherit; font-size: 0.74rem; font-weight: 600; color: #0369A1;
  background: #FFFFFF; border: 1px solid #BAE6FD; border-radius: 6px;
  padding: 5px 11px; cursor: pointer;
}
#workload-insights-report .wi-copy-btn:hover { background: #F0F9FF; }
#workload-insights-report .wi-dba-note {
  color: #7F2A26; background: #FDEDEC; border: 1px solid #F1C4C1;
  border-left: 4px solid #D9534F; border-radius: 6px; padding: 10px 12px;
  font-size: 0.85rem; line-height: 1.55; margin: 14px 0 0;
}
#workload-insights-report .wi-config-lead {
  color: #64748B; font-size: 0.88rem; line-height: 1.55; margin: 12px 0 14px;
}
#workload-insights-report .wi-config {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 0 0 12px;
}
#workload-insights-report .wi-config-card {
  background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px 16px;
}
#workload-insights-report .wi-config-careful {
  background: #FEF9E7; border-color: #FDE68A;
}
#workload-insights-report .wi-config-card h4 {
  margin: 0 0 8px; font-size: 0.82rem; font-weight: 700; color: #102E46;
}
#workload-insights-report .wi-config-card ul {
  margin: 0; padding-left: 18px; color: #475569; font-size: 0.8rem; line-height: 1.55;
}
#workload-insights-report .wi-config-card li { margin: 0 0 8px; }
#workload-insights-report .wi-config-card li:last-child { margin-bottom: 0; }
#workload-insights-report .wi-howto-sql summary {
  cursor: pointer; font-size: 0.85rem; font-weight: 600; color: #11567F;
}
#workload-insights-report .wi-howto-sql pre {
  max-height: 320px; overflow: auto; white-space: pre; line-height: 1.5;
}
#workload-insights-report .wi-unlocks {
  margin: 0; padding-left: 22px; list-style: disc outside;
  color: #64748B; font-size: 0.9rem; line-height: 1.9;
}
@media (max-width: 1000px) {
  #workload-insights-report .wi-kpis { grid-template-columns: repeat(2, 1fr); }
  #workload-insights-report .wi-grid-2,
  #workload-insights-report .wi-stat-grid,
  #workload-insights-report .wi-config { grid-template-columns: 1fr; }
}
"""
