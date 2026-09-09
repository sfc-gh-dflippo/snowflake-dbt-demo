"""Self-contained HTML assessment report for the SAS migration skill.

Renders the assessment dict (from ``AssessmentReporter.generate_assessment``) as
a single-file report styled after the SnowConvert AI assessment multi-report: a
dark navy sidebar with the Snowflake / SnowConvert AI logos and vertical nav,
and a light content area with KPI cards, distribution charts, a complexity x
volume matrix, the dependency DAG, and per-file detail. No third-party Python
deps. Everything renders offline except the dependency diagram, which uses the
Mermaid CDN when opened in a browser (an edges table is the offline fallback).
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Dict, List

PRIMARY = "#29B5E8"
PRIMARY_DARK = "#005C8F"
SIDEBAR = "#102E46"
MUTED = "#64748B"
BORDER = "#E2E8F0"
SEV = {"LOW": "#16a34a", "MEDIUM": "#f59e0b", "HIGH": "#ef4444"}
TIER_COLOR = {"TIER_1_SQL": "#29B5E8", "TIER_2_SP": "#005C8F", "TIER_3_PYSPARK": "#102E46"}
TIER_LABEL = {
    "TIER_1_SQL": "Tier 1 · SQL",
    "TIER_2_SP": "Tier 2 · Stored Proc",
    "TIER_3_PYSPARK": "Tier 3 · PySpark",
}
TIER_APPROACH = {
    "TIER_1_SQL": "Pure SQL — CTAS + CTEs + window functions",
    "TIER_2_SP": "Snowflake stored procedures (Snowflake Scripting)",
    "TIER_3_PYSPARK": "PySpark / Snowpark notebook",
}
# Each translation tier maps to a plain-language conversion-effort level so a
# reader who doesn't know the SQL/SP/PySpark taxonomy can still read the mix.
EFFORT_LABEL = {"TIER_1_SQL": "Low effort", "TIER_2_SP": "Medium effort", "TIER_3_PYSPARK": "High effort"}
EFFORT_TARGET = {"TIER_1_SQL": "SQL", "TIER_2_SP": "Stored proc", "TIER_3_PYSPARK": "PySpark"}
EFFORT_SEV = {"TIER_1_SQL": "LOW", "TIER_2_SP": "MEDIUM", "TIER_3_PYSPARK": "HIGH"}

CODE_BLOCK_DEF = (
    "A code block is one parsed SAS unit — a PROC step, DATA step, or macro definition. "
    "%LET, LIBNAME, comments, and macro calls are not counted."
)

_ASSETS = Path(__file__).parent / "assets"


def _load_logo(name: str) -> str:
    """Return the inline SVG for a bundled logo, sized by CSS (inline width stripped)."""
    path = _ASSETS / name
    try:
        svg = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    return re.sub(r'(<svg[^>]*?)\s+style="[^"]*"', r"\1", svg, count=1)


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _pct(n: int, total: int) -> float:
    return (n / total * 100) if total else 0.0


def _kpi(value, label, accent=PRIMARY, hint="") -> str:
    title = f' title="{_e(hint)}"' if hint else ""
    return (
        f'<div class="kpi"{title}><div class="kpi-val" style="color:{accent}">{_e(value)}</div>'
        f'<div class="kpi-label">{_e(label)}</div></div>'
    )


def _bars(dist: Dict[str, int], order: List[str], colors: Dict[str, str], total: int) -> str:
    rows = []
    for key in order:
        count = dist.get(key, 0)
        pct = _pct(count, total)
        rows.append(
            '<div class="bar-row">'
            f'<div class="bar-label">{_e(key.title())}</div>'
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width:{pct:.1f}%;background:{colors.get(key, PRIMARY)}"></div></div>'
            f'<div class="bar-val">{count} · {pct:.0f}%</div>'
            '</div>'
        )
    return '\n'.join(rows)


def _tier_donut(tier_dist: Dict[str, int], total: int) -> str:
    stops, acc = [], 0.0
    for key in ("TIER_1_SQL", "TIER_2_SP", "TIER_3_PYSPARK"):
        pct = _pct(tier_dist.get(key, 0), total)
        if pct <= 0:
            continue
        stops.append(f"{TIER_COLOR[key]} {acc:.2f}% {acc + pct:.2f}%")
        acc += pct
    gradient = ", ".join(stops) if stops else f"{BORDER} 0% 100%"
    legend = "".join(
        f'<div class="lg"><span class="dot" style="background:{TIER_COLOR[k]}"></span>'
        f'{_e(EFFORT_LABEL[k])} · {_e(EFFORT_TARGET[k])} <b>{tier_dist.get(k, 0)}</b></div>'
        for k in ("TIER_1_SQL", "TIER_2_SP", "TIER_3_PYSPARK")
    )
    return (
        '<div class="donut-wrap">'
        f'<div class="donut" style="background:conic-gradient({gradient})">'
        f'<div class="donut-hole"><span>{total}</span><small>files</small></div></div>'
        f'<div class="donut-legend">{legend}</div>'
        '</div>'
    )


def _findings(assessment: Dict) -> List[str]:
    p = assessment["portfolio_summary"]
    total = assessment["metadata"]["total_files"]
    tier = p["tier_distribution"]
    higher = tier.get("TIER_2_SP", 0) + tier.get("TIER_3_PYSPARK", 0)
    high_cx = p["complexity_distribution"].get("HIGH", 0)
    ext = len(assessment["dependency_graph"].get("external_inputs", []))
    edges = len(assessment["dependency_graph"].get("edges", []))
    macros = p["block_type_distribution"].get("MACRO_DEF", 0)
    out = []
    if total:
        out.append(
            f"{tier.get('TIER_1_SQL', 0)} of {total} files "
            f"({_pct(tier.get('TIER_1_SQL', 0), total):.0f}%) are Tier-1 — convertible to pure Snowflake SQL."
        )
    if higher:
        out.append(f"{higher} file(s) need a procedural rewrite (stored procedure or PySpark).")
    else:
        out.append("No files require stored-procedure or PySpark rewrites in this portfolio.")
    if high_cx:
        out.append(f"{high_cx} file(s) are HIGH complexity — plan for extra review and testing.")
    if ext:
        out.append(f"{ext} external source table(s) are referenced but not created in scope — provision or ingest them first.")
    if edges:
        out.append(f"{edges} cross-file dependency edge(s) detected — migrate producers before consumers (see Dependencies).")
    if macros:
        out.append(f"{macros} macro definition(s) found — factor shared macros into reusable Snowflake objects.")
    files = assessment.get("files", [])
    if files:
        top = max(files, key=lambda f: f.get("complexity_score", 0))
        out.append(f"Highest-scoring file: <code>{_e(top['filename'])}</code> (score {top['complexity_score']}).")
    return out


def render_html(assessment: Dict, mermaid_str: str = "") -> str:
    meta = assessment["metadata"]
    p = assessment["portfolio_summary"]
    files = assessment.get("files", [])
    graph = assessment.get("dependency_graph", {})
    total = meta["total_files"]
    tier = p["tier_distribution"]
    higher_tier = tier.get("TIER_2_SP", 0) + tier.get("TIER_3_PYSPARK", 0)
    high_cx = p["complexity_distribution"].get("HIGH", 0)

    snowflake_logo = _load_logo("snowflake_logo.svg")
    snowconvert_logo = _load_logo("snowconvert_ai_logo.svg")

    kpis = "".join([
        _kpi(total, "SAS files"),
        _kpi(f"{p['total_lines']:,}", "Lines of code"),
        _kpi(f"{p['total_blocks']:,}", "Code blocks", hint=CODE_BLOCK_DEF),
        _kpi(f"{_pct(tier.get('TIER_1_SQL', 0), total):.0f}%", "SQL-ready (Tier 1)", "#16a34a"),
        _kpi(higher_tier, "Need procedural rewrite", PRIMARY_DARK),
        _kpi(high_cx, "High complexity", SEV["HIGH"] if high_cx else MUTED),
    ])

    complexity_bars = _bars(p["complexity_distribution"], ["LOW", "MEDIUM", "HIGH"], SEV, total)
    volume_bars = _bars(p["volume_distribution"], ["LOW", "MEDIUM", "HIGH"], SEV, total)
    donut = _tier_donut(tier, total)
    findings = "".join(f"<li>{f}</li>" for f in _findings(assessment))

    block_rows = "".join(
        f"<tr><td>{_e(bt)}</td><td class='num'>{c}</td></tr>"
        for bt, c in sorted(p["block_type_distribution"].items(), key=lambda x: -x[1])
    )
    func_rows = "".join(
        f"<tr><td>{_e(fn)}</td><td class='num'>{c}</td></tr>"
        for fn, c in list(p.get("function_usage", {}).items())[:20]
    ) or "<tr><td colspan='2' class='muted'>No common SAS functions detected.</td></tr>"

    tier_rows = "".join(
        f"<tr><td><span class='chip' style='background:{TIER_COLOR[k]}'></span>{_e(TIER_LABEL[k])}</td>"
        f"<td class='num'>{tier.get(k, 0)}</td><td class='num'>{_pct(tier.get(k, 0), total):.0f}%</td>"
        f"<td><span class='pill' style='background:{SEV[EFFORT_SEV[k]]}'>{_e(EFFORT_LABEL[k])}</span></td>"
        f"<td>{_e(TIER_APPROACH[k])}</td></tr>"
        for k in ("TIER_1_SQL", "TIER_2_SP", "TIER_3_PYSPARK")
    )

    matrix = {}
    for f in files:
        matrix[(f["complexity_level"], f["volume_level"])] = matrix.get((f["complexity_level"], f["volume_level"]), 0) + 1
    matrix_rows = ""
    for cl in ("LOW", "MEDIUM", "HIGH"):
        cells = ""
        for vl in ("LOW", "MEDIUM", "HIGH"):
            n = matrix.get((cl, vl), 0)
            cells += f"<td class='num' style='{'background:#eef6fb' if n else ''}'>{n}</td>"
        matrix_rows += f"<tr><th class='rowhead' style='color:{SEV[cl]}'>{cl} complexity</th>{cells}</tr>"

    file_rows = ""
    for f in sorted(files, key=lambda x: x["complexity_score"], reverse=True):
        file_rows += (
            "<tr>"
            f"<td><code>{_e(f['filename'])}</code></td>"
            f"<td class='num'>{f['lines']}</td>"
            f"<td class='num'>{f['blocks']}</td>"
            f"<td class='num'>{f['complexity_score']}</td>"
            f"<td><span class='pill' style='background:{SEV.get(f['complexity_level'], MUTED)}'>{_e(f['complexity_level'])}</span></td>"
            f"<td><span class='pill' style='background:{SEV.get(f['volume_level'], MUTED)}'>{_e(f['volume_level'])}</span></td>"
            f"<td><span class='chip' style='background:{TIER_COLOR.get(f['primary_tier'], MUTED)}'></span>{_e(TIER_LABEL.get(f['primary_tier'], f['primary_tier']))}</td>"
            f"<td>{_e(f['confidence'])}</td>"
            "</tr>"
        )

    edges = graph.get("edges", [])
    edge_rows = "".join(
        f"<tr><td><code>{_e(ed['from'])}</code></td><td><code>{_e(ed['to'])}</code></td><td><code>{_e(ed.get('via', ''))}</code></td></tr>"
        for ed in edges
    ) or "<tr><td colspan='3' class='muted'>No cross-file dependencies detected.</td></tr>"
    ext_inputs = graph.get("external_inputs", [])
    ext_list = "".join(f"<li><code>{_e(x)}</code></li>" for x in ext_inputs[:200]) or "<li class='muted'>None — every referenced table is produced within scope.</li>"
    ext_more = f"<p class='muted'>… and {len(ext_inputs) - 200} more.</p>" if len(ext_inputs) > 200 else ""

    inventory = graph.get("data_source_inventory", [])
    inv_rows = "".join(
        f"<tr><td><code>{_e(r['source'])}</code></td><td>{_e(r['engine'])}</td>"
        f"<td class='num'>{r['tables']}</td><td>{_e(r['direction'])}</td></tr>"
        for r in inventory
    ) or "<tr><td colspan='4' class='muted'>No external source libraries detected — every referenced table is local WORK or produced within scope.</td></tr>"

    n_nodes = len(graph.get("nodes", []))
    if not mermaid_str.strip():
        mermaid_block = '<p class="muted">No dependency graph generated.</p>'
    elif n_nodes > 40 or len(edges) > 60:
        mermaid_block = (
            f'<p class="muted">The dependency graph is large ({n_nodes} nodes, {len(edges)} edges) — '
            'an inline diagram would be unreadable here. Use the edges table below, or open '
            '<code>dependency_dag.mmd</code> in a Mermaid viewer for the full graph.</p>'
        )
    else:
        mermaid_block = f'<pre class="mermaid">{_e(mermaid_str)}</pre>'

    nav_items = [
        ("overview", "Overview"),
        ("tiers", "Complexity &amp; Tiers"),
        ("deps", "Dependencies"),
        ("files", "Per-File Detail"),
        ("funcs", "Functions"),
    ]
    nav = "".join(
        f'<button class="{"active" if i == 0 else ""}" data-tab="{tid}">{label}</button>'
        for i, (tid, label) in enumerate(nav_items)
    )

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SAS → Snowflake Migration Assessment · SnowConvert AI</title>
<style>
:root {{ --primary:{PRIMARY}; --primary-dark:{PRIMARY_DARK}; --sidebar:{SIDEBAR}; --muted:{MUTED}; --border:{BORDER}; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; height:100%; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:#0f2233; background:#f8fafc; }}
.app {{ display:flex; min-height:100vh; }}
/* Sidebar */
.side {{ width:230px; flex:0 0 230px; background:#fff; color:#334155; display:flex; flex-direction:column; border-right:1px solid var(--border); }}
.brand {{ padding:22px 20px 16px; border-bottom:1px solid var(--border); }}
.brand .sf svg {{ width:132px; height:auto; display:block; }}
.brand .sc {{ margin-top:14px; }}
.brand .sc svg {{ width:132px; height:auto; display:block; }}
.brand .tagline {{ margin-top:14px; font-size:12px; color:{MUTED}; line-height:1.5; }}
.badge {{ display:inline-block; background:#EAF6FD; color:{PRIMARY_DARK}; font-weight:700; font-size:10px; letter-spacing:.4px; padding:3px 9px; border-radius:10px; margin-top:12px; }}
.side nav {{ padding:10px 10px; display:flex; flex-direction:column; gap:2px; }}
.side .navlabel {{ font-size:10px; letter-spacing:1.2px; text-transform:uppercase; color:#94a3b8; padding:10px 14px 6px; }}
.side nav button {{ text-align:left; background:none; border:0; color:#334155; padding:9px 14px; font-size:14px; cursor:pointer; border-radius:8px; }}
.side nav button:hover {{ background:#f1f5f9; color:#0f2233; }}
.side nav button.active {{ background:#EAF6FD; color:{PRIMARY_DARK}; font-weight:600; }}
.side .foot {{ margin-top:auto; padding:16px 20px; font-size:11px; color:#94a3b8; border-top:1px solid var(--border); }}
/* Main */
.main {{ flex:1; min-width:0; background:#f8fafc; }}
.pagehead {{ padding:26px 34px 2px; display:flex; align-items:flex-end; justify-content:space-between; gap:16px; }}
.pagehead h1 {{ margin:0; font-size:21px; color:#102E46; font-weight:700; }}
.pagehead .meta {{ color:var(--muted); font-size:12px; text-align:right; }}
.content {{ padding:16px 34px 60px; max-width:1180px; }}
.kpis {{ display:grid; grid-template-columns:repeat(6,1fr); gap:14px; margin-bottom:24px; }}
.kpi {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:16px; box-shadow:0 1px 3px rgba(16,46,70,.05); }}
.kpi-val {{ font-size:25px; font-weight:700; line-height:1; }}
.kpi-label {{ margin-top:6px; font-size:12px; color:var(--muted); }}
.tab {{ display:none; }} .tab.active {{ display:block; }}
.card {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:20px 22px; margin-bottom:18px; box-shadow:0 1px 3px rgba(16,46,70,.05); }}
.card h2 {{ margin:0 0 14px; font-size:15px; color:{PRIMARY_DARK}; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
.bar-row {{ display:grid; grid-template-columns:120px 1fr 92px; align-items:center; gap:10px; margin:8px 0; font-size:13px; }}
.bar-track {{ background:#eef2f6; border-radius:6px; height:14px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:6px; }}
.bar-val {{ text-align:right; color:var(--muted); font-variant-numeric:tabular-nums; }}
.donut-wrap {{ display:flex; align-items:center; gap:22px; }}
.donut {{ width:150px; height:150px; border-radius:50%; position:relative; flex:0 0 auto; }}
.donut-hole {{ position:absolute; inset:26px; background:#fff; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.donut-hole span {{ font-size:30px; font-weight:700; color:{SIDEBAR}; }}
.donut-hole small {{ color:var(--muted); font-size:11px; }}
.donut-legend .lg {{ font-size:13px; margin:7px 0; }}
.dot,.chip {{ display:inline-block; width:11px; height:11px; border-radius:3px; margin-right:7px; vertical-align:middle; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--border); }}
th {{ color:var(--muted); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.3px; }}
td.num,th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.rowhead {{ text-align:left; font-weight:650; }}
code {{ background:#f1f5f9; padding:1px 6px; border-radius:4px; font-size:12px; }}
.pill {{ color:#fff; padding:2px 9px; border-radius:20px; font-size:11px; font-weight:650; }}
.muted {{ color:var(--muted); }}
.caption {{ font-size:12px; line-height:1.5; margin:12px 0 0; }}
ul.findings {{ margin:0; padding-left:20px; }} ul.findings li {{ margin:7px 0; font-size:14px; }}
.mermaid {{ background:#fff; border:1px dashed var(--border); border-radius:10px; padding:16px; overflow:auto; }}
.scroll {{ max-height:520px; overflow:auto; }}
footer {{ color:var(--muted); font-size:12px; padding:22px 0 0; border-top:1px solid var(--border); margin-top:20px; }}
</style></head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand">
      <div class="sf">{snowflake_logo}</div>
      <div class="sc">{snowconvert_logo}</div>
      <div class="tagline">SAS → Snowflake migration assessment</div>
      <span class="badge">PREVIEW</span>
    </div>
    <div class="navlabel">Assessment</div>
    <nav>{nav}</nav>
    <div class="foot">Generated {_e(meta['generated_at'][:19])}<br>Tool v{_e(meta['tool_version'])}</div>
  </aside>
  <main class="main">
    <div class="pagehead">
      <h1>SAS → Snowflake Migration Assessment</h1>
      <div class="meta">{total} SAS files · {p['total_lines']:,} lines<br>Not SnowConvert / AIM registry</div>
    </div>
    <div class="content">
      <div class="kpis">{kpis}</div>

      <section class="tab active" id="overview">
        <div class="card"><h2>Key findings</h2><ul class="findings">{findings}</ul></div>
        <div class="grid2">
          <div class="card"><h2>Conversion effort mix</h2>{donut}
            <p class="muted caption">Effort tier by conversion target — Low = SQL, Medium = stored procedure, High = PySpark / Snowpark.</p></div>
          <div class="card"><h2>Block types</h2><table><thead><tr><th>Block type</th><th class="num">Count</th></tr></thead><tbody>{block_rows}</tbody></table>
            <p class="muted caption">{_e(CODE_BLOCK_DEF)}</p></div>
        </div>
        <div class="grid2">
          <div class="card"><h2>Complexity distribution</h2>{complexity_bars}</div>
          <div class="card"><h2>Volume distribution</h2>{volume_bars}</div>
        </div>
      </section>

      <section class="tab" id="tiers">
        <div class="card"><h2>Translation tiers</h2>
          <table><thead><tr><th>Tier</th><th class="num">Files</th><th class="num">Share</th><th>Effort</th><th>Recommended approach</th></tr></thead><tbody>{tier_rows}</tbody></table>
        </div>
        <div class="card"><h2>Complexity × Volume matrix</h2>
          <table><thead><tr><th></th><th class="num">Low volume</th><th class="num">Medium volume</th><th class="num">High volume</th></tr></thead><tbody>{matrix_rows}</tbody></table>
        </div>
      </section>

      <section class="tab" id="deps">
        <div class="card"><h2>Dependency graph</h2>{mermaid_block}</div>
        <div class="card"><h2>Data source inventory ({len(inventory)})</h2>
          <table><thead><tr><th>Source</th><th>Engine / Type</th><th class="num">Tables</th><th>Direction</th></tr></thead><tbody>{inv_rows}</tbody></table>
          <p class="muted caption">External libraries the module reads from or writes to, aggregated by library. Local WORK, unqualified, and SAS dictionary datasets are excluded. Engine / type is shown when a LIBNAME or CONNECT declares it; libraries resolved at runtime via <code>%assign_libname</code> appear as “External SAS library”.</p>
        </div>
        <div class="grid2">
          <div class="card"><h2>Dependency edges ({len(edges)})</h2><div class="scroll"><table><thead><tr><th>Producer</th><th>Consumer</th><th>Via table</th></tr></thead><tbody>{edge_rows}</tbody></table></div></div>
          <div class="card"><h2>External source tables ({len(ext_inputs)})</h2><div class="scroll"><ul>{ext_list}</ul>{ext_more}</div></div>
        </div>
      </section>

      <section class="tab" id="files">
        <div class="card"><h2>Per-file detail ({total} files, sorted by complexity score)</h2>
          <div class="scroll"><table><thead><tr><th>File</th><th class="num">Lines</th><th class="num">Blocks</th><th class="num">Score</th>
          <th>Complexity</th><th>Volume</th><th>Tier</th><th>Confidence</th></tr></thead><tbody>{file_rows}</tbody></table></div>
        </div>
      </section>

      <section class="tab" id="funcs">
        <div class="card"><h2>SAS functions used</h2>
          <table><thead><tr><th>Function</th><th class="num">Occurrences</th></tr></thead><tbody>{func_rows}</tbody></table>
        </div>
      </section>

      <footer>Preview — generated by the SAS-to-Snowflake assessment skill (SnowConvert AI, tool v{_e(meta['tool_version'])}).
      Estimates are heuristic and intended for planning; validate against a sample conversion before committing to a plan.</footer>
    </div>
  </main>
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  // Mermaid must render while the Dependencies tab is visible — a diagram
  // rendered inside a display:none container gets a zero-size, broken SVG.
  // So disable startOnLoad and render lazily the first time the tab is shown.
  var mermaidDone = false;
  function renderDeps() {{
    if (mermaidDone || !window.mermaid) return;
    mermaidDone = true;
    try {{ mermaid.run({{ nodes: document.querySelectorAll('#deps .mermaid') }}); }} catch (e) {{}}
  }}
  if (window.mermaid) {{ mermaid.initialize({{ startOnLoad: false, theme: 'base',
    themeVariables: {{ primaryColor: '#eaf6fd', primaryBorderColor: '{PRIMARY}', lineColor: '#64748B', fontSize: '13px' }} }}); }}
  document.querySelectorAll('.side nav button').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.querySelectorAll('.side nav button').forEach(function (x) {{ x.classList.remove('active'); }});
      document.querySelectorAll('.tab').forEach(function (x) {{ x.classList.remove('active'); }});
      b.classList.add('active');
      document.getElementById(b.dataset.tab).classList.add('active');
      if (b.dataset.tab === 'deps') renderDeps();
    }});
  }});
</script>
</body></html>"""
