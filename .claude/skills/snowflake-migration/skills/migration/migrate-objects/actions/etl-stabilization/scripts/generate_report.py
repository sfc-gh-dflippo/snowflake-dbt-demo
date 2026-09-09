#!/usr/bin/env python3
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generate an HTML report from ETL fixer artifacts.

Usage:
    python generate_report.py <unit_folder> [--template <path>]

Arguments:
    unit_folder     Path to the converted ETL unit folder
    --template      (Optional) Path to HTML template. Defaults to
                    {SKILL_DIR}/reference/templates/report-template.html

Output:
    <unit_folder>/stabilization/report.html
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from html import escape

from path_resolver import report_path, stabilization_root


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _load_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _md_to_html_simple(md: str) -> str:
    """Minimal markdown-to-HTML for rendering inside collapsible sections."""
    lines = md.split("\n")
    html_lines: list[str] = []
    in_table = False
    in_code = False
    in_list = False

    for line in lines:
        if line.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="{escape(lang)}">')
                in_code = True
            continue

        if in_code:
            html_lines.append(escape(line))
            continue

        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c) <= {"-", ":", " "} for c in cells):
                continue
            if not in_table:
                html_lines.append("<table>")
                tag = "th"
                in_table = True
            else:
                tag = "td"
            row = "".join(f"<{tag}>{escape(c)}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue
        elif in_table:
            html_lines.append("</table>")
            in_table = False

        if stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:]
            content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
            content = re.sub(r"`(.+?)`", r"<code>\1</code>", content)
            html_lines.append(f"<li>{content}</li>")
            continue
        elif in_list and not stripped.startswith("- "):
            html_lines.append("</ul>")
            in_list = False

        if stripped.startswith("### "):
            html_lines.append(f"<h4>{escape(stripped[4:])}</h4>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h3>{escape(stripped[3:])}</h3>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h3>{escape(stripped[2:])}</h3>")
        elif stripped:
            content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            content = re.sub(r"`(.+?)`", r"<code>\1</code>", content)
            html_lines.append(f"<p>{content}</p>")

    if in_table:
        html_lines.append("</table>")
    if in_list:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append("</code></pre>")

    return "\n".join(html_lines)


def _build_stat_card(number: str | int, label: str, css_class: str = "") -> str:
    num_cls = f"number {css_class}" if css_class else "number"
    return (
        f'<div class="stat-card">'
        f'<div class="{num_cls}">{number}</div>'
        f'<div class="label">{escape(str(label))}</div>'
        f"</div>"
    )


def _build_details(summary: str, content: str) -> str:
    return f"<details><summary>{escape(summary)}</summary>\n{content}\n</details>"


def _status_badge(status: str) -> str:
    css_map = {
        "test-passed": "badge-pass",
        "fixed": "badge-pass",
        "dbt-fixed": "badge-pass",
        "completed": "badge-pass",
        "skipped": "badge-skip",
        "pending": "badge-skip",
        "failed": "badge-fail",
        "needs-user": "badge-new",
    }
    css = css_map.get(status, "")
    return f'<span class="badge {css}">{escape(status)}</span>'


_EXCLUDED_DIRS = {"stabilization", "target", "dbt_packages", "logs"}


def _count_ewi_markers(unit_path: Path) -> int:
    """Count remaining !!!RESOLVE EWI!!! markers in source SQL files.

    Excludes metadata, dbt build artifacts, and dependency directories.
    """
    count = 0
    for sql_file in unit_path.glob("**/*.sql"):
        if _EXCLUDED_DIRS & set(sql_file.relative_to(unit_path).parts):
            continue
        try:
            text = sql_file.read_text(encoding="utf-8", errors="replace")
            count += text.count("!!!RESOLVE EWI!!!")
        except OSError:
            pass
    return count


def _collect_test_reports(meta_dir: Path) -> list[tuple[str, str]]:
    """Collect all test_report.md files from the tests directory.

    Returns list of (label, markdown_content) tuples.
    """
    reports: list[tuple[str, str]] = []
    tests_dir = meta_dir / "tests"
    if not tests_dir.is_dir():
        return reports

    for report_file in sorted(tests_dir.rglob("test_report.md")):
        rel = report_file.relative_to(tests_dir)
        parts = list(rel.parts)
        if len(parts) >= 2:
            label = f"{parts[0].title()}: {parts[1]}"
        else:
            label = str(rel)
        content = report_file.read_text(encoding="utf-8", errors="replace")
        reports.append((label, content))

    return reports


def _get_dbt_model_count(scan: dict, project_name: str) -> int:
    """Get model count from scan.json for a dbt project."""
    for proj in scan.get("dbt_projects", []):
        if proj.get("name") == project_name:
            return proj.get("model_count", 0)
    return 0


def generate_report(unit_path: Path, template_path: Path) -> Path:
    stab_root = stabilization_root(unit_path)

    planning_directory = stab_root / "planning"
    tracking_directory = stab_root / "tracking"

    scan = _load_json(planning_directory / "scan.json") or {}
    session = _load_json(tracking_directory / "progress.json") or {}
    roadmap_md = _load_text(planning_directory / "ROADMAP.md") or ""
    pkg_orch_context_md = _load_text(planning_directory / "orchestration-context.md") or ""
    pkg_dbt_context_md = _load_text(planning_directory / "dbt-context.md") or ""
    pkg_context_md = pkg_orch_context_md
    if pkg_dbt_context_md:
        pkg_context_md += "\n\n---\n\n" + pkg_dbt_context_md
    fix_log_md = _load_text(tracking_directory / "fix-log.md") or ""
    state_md = _load_text(tracking_directory / "STATE.md") or ""

    template = template_path.read_text(encoding="utf-8")

    unit_name = scan.get("unit_name", unit_path.name)
    source_file = scan.get("source_definition_path", "N/A")
    platform_id = scan.get("platform_id", "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    elements = session.get("elements", [])
    dbt_projects = session.get("dbt_projects", [])
    phases = session.get("roadmap", {}).get("phases", [])

    total_elements = len([e for e in elements if not e.get("is_statement_level")])
    _PASSING_STATUSES = {"test-passed", "fixed", "no-fix-needed"}
    elements_passed = len([
        e for e in elements
        if not e.get("is_statement_level") and e.get("status") in _PASSING_STATUSES
    ])

    total_dbt = len(dbt_projects)

    total_initial_ewi = sum(
        len(e.get("initial_issues", []))
        for e in elements
        if not e.get("is_statement_level")
    )

    total_phases = len(phases)
    # Report generation is the last step of the final-validation phase and runs
    # before complete-phase marks it done. Treat all phases as completed since
    # the report is only generated when every prior phase has finished.
    phases_completed = total_phases

    remaining_ewi = _count_ewi_markers(unit_path)

    test_reports = _collect_test_reports(stab_root)

    # --- Build HTML sections (use counter for stable numbering) ---
    section_num = 0

    # Header
    header_html = f"""
<h1>ETL Migration Report</h1>
<p><strong>Unit:</strong> <code>{escape(unit_name)}</code></p>
<p><strong>Source:</strong> <code>{escape(source_file)}</code></p>
<p><strong>Platform:</strong> {escape(platform_id)}</p>
<p><strong>Generated:</strong> {escape(timestamp)}</p>
"""

    # Section: Executive Summary
    section_num += 1
    summary_cards = '<div class="stats-grid">\n'
    summary_cards += _build_stat_card(total_elements, "Orchestration Elements")
    summary_cards += _build_stat_card(total_dbt, "dbt Projects")
    summary_cards += _build_stat_card(total_initial_ewi, "Initial EWI/FDM Issues")
    summary_cards += _build_stat_card(
        remaining_ewi,
        "Remaining EWI Markers",
        "delta-pass" if remaining_ewi == 0 else "delta-fail",
    )
    summary_cards += _build_stat_card(
        f"{phases_completed}/{total_phases}", "Phases Completed"
    )
    summary_cards += _build_stat_card(
        f"{elements_passed}/{total_elements}",
        "Elements Passing",
        "delta-pass" if elements_passed == total_elements else "",
    )
    summary_cards += "</div>\n"
    summary_html = f"\n<h2>{section_num}. Executive Summary</h2>\n" + summary_cards

    # Section: Phase Summary
    section_num += 1
    phase_rows = ""
    for p in phases:
        pnum = p.get("phase", "?")
        pname = escape(p.get("name", ""))
        pgoal = escape(p.get("goal", ""))
        status = p.get("status", "pending")
        if status != "completed":
            status = "completed"
        pstatus = _status_badge(status)
        phase_rows += f"<tr><td>{pnum}</td><td>{pname}</td><td>{pgoal}</td><td>{pstatus}</td></tr>\n"

    phase_html = f"""
<h2>{section_num}. Phase Summary</h2>
<table>
<tr><th>#</th><th>Phase</th><th>Goal</th><th>Status</th></tr>
""" + phase_rows + "</table>\n"

    # Section: Element Status
    section_num += 1
    elem_rows = ""
    for e in elements:
        if e.get("is_statement_level"):
            continue
        ename = escape(e.get("name", ""))
        estmt = escape(e.get("statement", ""))
        estatus = _status_badge(e.get("status", "pending"))
        issues = e.get("initial_issues", [])
        issue_str = ", ".join(
            f'<code>{escape(i.get("code", ""))}</code>' for i in issues
        ) or "clean"
        ephase = e.get("phase", "—")
        estrategy = escape(e.get("test_strategy", "—") or "—")
        reason = escape(e.get("reason", ""))
        elem_rows += (
            f"<tr><td>{ename}</td><td>{estmt}</td><td>{issue_str}</td>"
            f"<td>{estatus}</td><td>{ephase}</td><td>{estrategy}</td>"
            f"<td>{reason}</td></tr>\n"
        )

    element_html = f"""
<h2>{section_num}. Orchestration Elements</h2>
<table>
<tr><th>Element</th><th>Statement</th><th>Issues</th><th>Status</th><th>Phase</th><th>Strategy</th><th>Notes</th></tr>
""" + elem_rows + "</table>\n"

    # Section: dbt Projects
    dbt_section = ""
    if dbt_projects:
        section_num += 1
        dbt_rows = ""
        for proj in dbt_projects:
            pname = escape(proj.get("name", ""))
            pstatus = _status_badge(proj.get("status", "pending"))
            nodes = proj.get("nodes", [])
            node_count = len(nodes)

            if node_count > 0:
                nodes_fixed = len([n for n in nodes if n.get("status") == "fixed"])
                models_col = f"{nodes_fixed}/{node_count}"
            else:
                model_count = _get_dbt_model_count(scan, proj.get("name", ""))
                models_col = str(model_count) if model_count > 0 else "—"

            dbt_rows += (
                f"<tr><td>{pname}</td><td>{pstatus}</td>"
                f"<td>{models_col}</td></tr>\n"
            )

        dbt_section = f"""
<h2>{section_num}. dbt Projects</h2>
<table>
<tr><th>Project</th><th>Status</th><th>Models</th></tr>
""" + dbt_rows + "</table>\n"

        for proj in dbt_projects:
            nodes = proj.get("nodes", [])
            if not nodes:
                continue
            pname = escape(proj.get("name", ""))
            node_rows = ""
            for n in nodes:
                nname = escape(n.get("name", ""))
                npath = escape(n.get("path", ""))
                nstatus = _status_badge(n.get("status", "pending"))
                node_rows += f"<tr><td>{nname}</td><td><code>{npath}</code></td><td>{nstatus}</td></tr>\n"
            dbt_section += _build_details(
                f"{pname} — Model Details",
                f'<table><tr><th>Model</th><th>Path</th><th>Status</th></tr>\n{node_rows}</table>',
            )

    # Section: Test Results
    test_section = ""
    if test_reports:
        section_num += 1
        test_section = f"\n<h2>{section_num}. Test Results</h2>\n"
        for label, content in test_reports:
            test_section += _build_details(label, _md_to_html_simple(content))
            test_section += "\n"

    # Section: Fix Log
    fix_section = ""
    if fix_log_md:
        section_num += 1
        fix_section = f"""
<h2>{section_num}. Fix Log</h2>
{_build_details("View Fix Log", _md_to_html_simple(fix_log_md))}
"""

    # Section: Artifacts
    section_num += 1
    roadmap_section = ""
    if roadmap_md:
        roadmap_section = _build_details(
            "ROADMAP.md", _md_to_html_simple(roadmap_md)
        )

    context_section = ""
    if pkg_context_md:
        context_section = _build_details(
            "orchestration-context.md / dbt-context.md", _md_to_html_simple(pkg_context_md)
        )

    state_section = ""
    if state_md:
        state_section = _build_details("STATE.md", _md_to_html_simple(state_md))

    artifacts_section = f"""
<h2>{section_num}. Artifacts</h2>
{roadmap_section}
{context_section}
{state_section}
"""

    # Section: File reference
    section_num += 1
    file_ref_rows = ""
    artifact_files = [
        ("artifacts/planning/scan.json", "Unit scan output"),
        ("artifacts/tracking/session_status.json", "Element-level tracking"),
        ("artifacts/planning/ROADMAP.md", "Phase plan"),
        ("artifacts/planning/orchestration-context.md", "Orchestration structural understanding"),
        ("artifacts/planning/dbt-context.md", "dbt project analysis"),
        ("artifacts/tracking/STATE.md", "Resumption bookmark"),
        ("artifacts/tracking/fix_log.md", "Append-only fix record"),
    ]
    for fname, desc in artifact_files:
        fpath = stab_root / fname
        exists = "✓" if fpath.exists() else "✗"
        file_ref_rows += (
            f"<tr><td><code>{escape(fname)}</code></td>"
            f"<td>{desc}</td><td>{exists}</td></tr>\n"
        )

    file_ref = f"""
<h2>{section_num}. File Reference</h2>
<table>
<tr><th>File</th><th>Description</th><th>Present</th></tr>
{file_ref_rows}
</table>
"""

    # Assemble final HTML
    body_content = (
        header_html
        + summary_html
        + phase_html
        + element_html
        + dbt_section
        + test_section
        + fix_section
        + artifacts_section
        + file_ref
    )

    final_html = template.split("<body>")[0] + "<body>\n" + body_content + "\n</body>\n</html>"

    final_html = final_html.replace(
        "<title>ETL Fixer Report — <unit_name></title>",
        f"<title>ETL Migration Report — {escape(unit_name)}</title>",
    )

    output_path = report_path(unit_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_html, encoding="utf-8")
    print(f"Report generated: {output_path}")
    return output_path


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    unit_folder = Path(sys.argv[1])
    if not unit_folder.is_dir():
        print(f"Error: {unit_folder} is not a directory", file=sys.stderr)
        sys.exit(1)

    template_path = None
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--template" and i + 1 < len(sys.argv):
            template_path = Path(sys.argv[i + 1])
            break

    if template_path is None:
        skill_dir = Path(__file__).resolve().parent.parent
        template_path = skill_dir / "reference" / "templates" / "report-template.html"

    if not template_path.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    generate_report(unit_folder, template_path)


if __name__ == "__main__":
    main()
