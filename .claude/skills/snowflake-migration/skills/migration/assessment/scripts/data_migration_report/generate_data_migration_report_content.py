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

"""Render the Data Migration & Validation tab from a ``DataMigrationReadiness``.

Presentation only: every count arrives already derived and every string already
written (see ``content.py``). Each block is conditional -- a section with
nothing to say about this project is not rendered rather than rendered empty.

Returns ``(html, css, js)``. The JS is scoped vanilla and adds no reactive
state to the report's Vue instance; it delegates from ``document`` so a
re-render cannot strand its listeners.
"""

from __future__ import annotations

import html
from collections.abc import Iterable, Sequence
from pathlib import Path

from snowconvert_reports.data_migration_readiness import (
    DataMigrationReadiness,
    TypeFinding,
)

from .content import (
    ANSWER_NO,
    ANSWER_YES,
    BOTTLENECK_TITLE,
    BOTTLENECKS,
    CLEAN_TYPES_SENTENCE,
    COPY_LABEL,
    DIALECT_DISPLAY_NAMES,
    DIALECT_LINKS,
    DOWNLOAD_LABEL,
    FINDINGS_HEADERS,
    FINDINGS_LEDE,
    FINDINGS_TITLE,
    FINDINGS_USED_IN_HEADER,
    KNOW_YOUR_DATA_LEDE,
    KNOW_YOUR_DATA_TITLE,
    MATRIX_COL_LABELS,
    MATRIX_ROW_LABELS,
    MIGRATION_LABELS,
    NO_SCRIPTS_ITEMS,
    NO_SCRIPTS_LEDE,
    NO_SCRIPTS_TITLE,
    PICKER_RESET,
    PULL_QUESTION,
    READING_TITLE,
    REFERENCE_TABLE_NOTE,
    SCAN_COVERAGE_SENTENCE,
    SCRIPT_NOTES,
    SCRIPT_TITLES,
    SCRIPTS_LEDE,
    SCRIPTS_TITLE,
    SHARED_LINKS,
    STRIP_LABEL,
    STRIP_POINTER,
    SUGGESTIONS,
    SUGGESTIONS_TITLE,
    TAB_LEDE,
    TILE_TABLES,
    TILE_TABLES_NOTE,
    TILE_VIEWS,
    TILE_VIEWS_NOTE,
    TOPOLOGY_CELLS,
    TOPOLOGY_LEDE,
    TOPOLOGY_TITLE,
    UNLOAD_QUESTION,
    VALIDATION_BODY,
    VALIDATION_LABELS,
    VALIDATION_TITLE,
    WORKER_OPTIONS,
    WORKER_TITLE,
    DocLink,
    Suggestion,
    TopologyCell,
)

# Alpine/Vue directive and CSS hook; kept out of an f-string so the braces
# survive intact.
_TAB_OPEN = (
    '<div class="tab-content" id="data-migration-phase" '
    ':class="{active: activeTab === \'data-migration\'}">'
)

_SQL_DIR = Path(__file__).parent / "sql"
_SCRIPT_KINDS = ("table_inventory", "data_type_inventory")

# What a run with no registry resolves to: dialect unknown, so no project claim
# and no inventory script, but the topology and validation guidance still hold.
NO_PROJECT_STATE = DataMigrationReadiness(
    has_project_state=False,
    source_dialect="",
    dialect_key="",
    table_count=0,
    view_count=0,
    scanned_tables=0,
    distinct_type_count=0,
    clean_type_count=0,
    findings=(),
    has_inventory_scripts=False,
)


def _dialect_name(readiness: DataMigrationReadiness) -> str:
    return DIALECT_DISPLAY_NAMES.get(
        readiness.dialect_key, html.escape(readiness.source_dialect)
    )


def _plural(count: int, noun: str) -> str:
    return noun if count == 1 else f"{noun}s"


def _card(title: str, body: Iterable[str], anchor: str, lede: str = "") -> str:
    lede_html = f'<p class="dmv-card-lede">{lede}</p>' if lede else ""
    return f"""
        <div class="dmv-card" id="{anchor}">
            <div class="dmv-card-title">{title}</div>
            {lede_html}
            {"".join(part for part in body if part)}
        </div>"""


def _tile(value: int, name: str, note: str) -> str:
    return f"""
                <div class="dmv-tile">
                    <div class="dmv-tile-value">{value}</div>
                    <div class="dmv-tile-name">{name}</div>
                    <div class="dmv-tile-note">{note}</div>
                </div>"""


def _strip(readiness: DataMigrationReadiness) -> str:
    """Table and view counts. Not rendered when the registry held neither."""
    if not readiness.has_project_state:
        return ""
    if not (readiness.table_count or readiness.view_count):
        return ""

    tiles = [_tile(readiness.table_count, TILE_TABLES, TILE_TABLES_NOTE)]
    if readiness.view_count:
        tiles.append(_tile(readiness.view_count, TILE_VIEWS, TILE_VIEWS_NOTE))

    return f"""
        <div class="dmv-strip" id="dmv-scope">
            <div class="dmv-strip-label">{STRIP_LABEL}</div>
            <div class="dmv-tiles">{"".join(tiles)}
            </div>
            <div class="dmv-strip-note">{STRIP_POINTER}</div>
        </div>"""


def _status_pill(kind: str, value: str, label: str) -> str:
    return f'<span class="dmv-pill-status dmv-{kind}--{value.replace(" ", "-")}">{label}</span>'


def _findings_table(findings: Sequence[TypeFinding], show_usage: bool) -> str:
    headers = list(FINDINGS_HEADERS)
    if show_usage:
        headers.insert(1, FINDINGS_USED_IN_HEADER)
    head = "".join(f"<th>{header}</th>" for header in headers)

    rows = []
    for finding in findings:
        coverage = finding.coverage
        usage_cell = ""
        if show_usage and finding.usage is not None:
            usage = finding.usage
            usage_cell = (
                f'<td class="dmv-cell-usage">{usage.column_count} '
                f'{_plural(usage.column_count, "column")}'
                f"<span>{usage.table_count} "
                f'{_plural(usage.table_count, "table")}</span></td>'
            )
        elif show_usage:
            usage_cell = '<td class="dmv-cell-usage">&mdash;</td>'
        rows.append(
            f"""
                    <tr>
                        <td class="dmv-cell-type"><code>{coverage.type_name}</code></td>{usage_cell}
                        <td class="dmv-cell-target"><code>{coverage.snowflake_type}</code></td>
                        <td>{_status_pill("migration", coverage.migration, MIGRATION_LABELS[coverage.migration])}</td>
                        <td>{_status_pill("validation", coverage.validation, VALIDATION_LABELS[coverage.validation])}</td>
                        <td class="dmv-cell-note">{coverage.note}</td>
                    </tr>"""
        )

    return f"""
            <table class="dmv-types">
                <thead><tr>{head}</tr></thead>
                <tbody>{"".join(rows)}
                </tbody>
            </table>"""


def _scan_coverage_line(readiness: DataMigrationReadiness) -> str:
    """How much of the project the scan actually read. Never rounded up."""
    return SCAN_COVERAGE_SENTENCE.format(
        scanned=readiness.scanned_tables,
        total=readiness.table_count,
        noun=_plural(readiness.table_count, "table"),
    )


def _findings(readiness: DataMigrationReadiness) -> str:
    if not readiness.findings:
        return ""

    scanned = readiness.has_project_state and readiness.scanned_tables > 0
    parts = [_findings_table(readiness.findings, show_usage=scanned)]

    if not scanned:
        parts.append(f'<div class="dmv-note">{REFERENCE_TABLE_NOTE}</div>')
        return _card(
            FINDINGS_TITLE, parts, anchor="dmv-type-findings", lede=FINDINGS_LEDE
        )

    if readiness.clean_type_count:
        clean = CLEAN_TYPES_SENTENCE.format(
            clean=readiness.clean_type_count,
            noun=_plural(readiness.clean_type_count, "type"),
        )
        parts.append(f'<p class="dmv-clean">{clean}</p>')
    parts.append(f'<div class="dmv-note">{_scan_coverage_line(readiness)}</div>')

    return _card(FINDINGS_TITLE, parts, anchor="dmv-type-findings", lede=FINDINGS_LEDE)


def _all_clean(readiness: DataMigrationReadiness) -> str:
    """The scan ran and found nothing to decide -- worth saying, once."""
    if readiness.findings or not readiness.scanned_tables:
        return ""
    count = readiness.distinct_type_count
    return (
        f'<div class="dmv-note" id="dmv-types-clean">Every one of the {count} column '
        f'{_plural(count, "type")} read from your DDL maps cleanly for both '
        f"migration and validation. {_scan_coverage_line(readiness)}</div>"
    )


def _read_sql(dialect_key: str, kind: str) -> str:
    path = _SQL_DIR / f"{dialect_key}_{kind}.sql"
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def _scripts(readiness: DataMigrationReadiness) -> str:
    """Collapsed, copyable inventory scripts for an allow-listed dialect."""
    if not readiness.has_inventory_scripts:
        return _card(
            NO_SCRIPTS_TITLE,
            [
                '<ul class="dmv-list">'
                + "".join(f"<li>{item}</li>" for item in NO_SCRIPTS_ITEMS)
                + "</ul>"
            ],
            anchor="dmv-gather",
            lede=NO_SCRIPTS_LEDE,
        )

    blocks = []
    for kind in _SCRIPT_KINDS:
        sql = _read_sql(readiness.dialect_key, kind)
        if not sql:
            continue
        pre_id = f"dmv-sql-{kind.replace('_', '-')}"
        filename = f"{readiness.dialect_key}_{kind}.sql"
        blocks.append(
            f"""
            <details class="dmv-script">
                <summary>
                    <span class="dmv-script-title">{SCRIPT_TITLES[kind]}</span>
                    <span class="dmv-script-note">{SCRIPT_NOTES[kind]}</span>
                </summary>
                <div class="dmv-script-actions">
                    <button type="button" class="dmv-btn" data-dmv-copy="{pre_id}">{COPY_LABEL}</button>
                    <button type="button" class="dmv-btn" data-dmv-download="{pre_id}" data-dmv-filename="{filename}">{DOWNLOAD_LABEL}</button>
                </div>
                <pre class="dmv-sql" id="{pre_id}" v-pre>{html.escape(sql)}</pre>
            </details>"""
        )

    if not blocks:
        return ""
    return _card(SCRIPTS_TITLE, blocks, anchor="dmv-scripts", lede=SCRIPTS_LEDE)


def _pill_row(axis: str, question: str) -> str:
    return f"""
            <div class="dmv-question">
                <span class="dmv-question-text">{question}</span>
                <span class="dmv-answers">
                    <button type="button" class="dmv-pill" data-dmv-axis="{axis}" data-dmv-value="yes">{ANSWER_YES}</button>
                    <button type="button" class="dmv-pill" data-dmv-axis="{axis}" data-dmv-value="no">{ANSWER_NO}</button>
                </span>
            </div>"""


def _matrix_cell(cell: TopologyCell) -> str:
    return f"""
                    <td class="dmv-quad" data-dmv-unload="{'yes' if cell.unload else 'no'}" data-dmv-pull="{'yes' if cell.pull else 'no'}">
                        <div class="dmv-quad-title">{cell.title}</div>
                        <div class="dmv-quad-body">{cell.body}</div>
                        <div class="dmv-quad-eff">{cell.efficiency}</div>
                    </td>"""


def _matrix() -> str:
    by_key = {(cell.unload, cell.pull): cell for cell in TOPOLOGY_CELLS}
    rows = []
    for row_index, unload in enumerate((True, False)):
        cells = "".join(_matrix_cell(by_key[(unload, pull)]) for pull in (True, False))
        rows.append(
            f"""
                <tr>
                    <th scope="row">{MATRIX_ROW_LABELS[row_index]}</th>{cells}
                </tr>"""
        )
    headers = "".join(f"<th scope='col'>{label}</th>" for label in MATRIX_COL_LABELS)
    return f"""
            <table class="dmv-matrix" id="dmv-topology-matrix">
                <thead><tr><td></td>{headers}</tr></thead>
                <tbody>{"".join(rows)}
                </tbody>
            </table>"""


def _bullet_card(title: str, items: Iterable[Suggestion]) -> str:
    body = "".join(
        f'<div class="dmv-item"><div class="dmv-item-title">{item.title}</div>'
        f'<div class="dmv-item-body">{item.body}</div></div>'
        for item in items
    )
    return f'<div class="dmv-sub"><div class="dmv-sub-title">{title}</div>{body}</div>'


def _topology() -> str:
    return _card(
        TOPOLOGY_TITLE,
        [
            f"""
            <div class="dmv-picker" id="dmv-picker">
                {_pill_row("unload", UNLOAD_QUESTION)}
                {_pill_row("pull", PULL_QUESTION)}
                <button type="button" class="dmv-reset" data-dmv-reset="1">{PICKER_RESET}</button>
            </div>""",
            _matrix(),
            _bullet_card(WORKER_TITLE, WORKER_OPTIONS),
            f'<div class="dmv-sub"><div class="dmv-sub-title">{BOTTLENECK_TITLE}</div>'
            + '<ul class="dmv-list">'
            + "".join(f"<li>{item}</li>" for item in BOTTLENECKS)
            + "</ul></div>",
        ],
        anchor="dmv-topology",
        lede=TOPOLOGY_LEDE,
    )


def _suggestions(readiness: DataMigrationReadiness) -> str:
    items = SUGGESTIONS.get(readiness.dialect_key)
    if not items:
        return ""
    return _card(
        SUGGESTIONS_TITLE.format(dialect=_dialect_name(readiness)),
        [_bullet_card("", items)],
        anchor="dmv-suggestions",
    )


def _validation() -> str:
    return _card(
        VALIDATION_TITLE,
        [f"<p class='dmv-para'>{para}</p>" for para in VALIDATION_BODY],
        anchor="dmv-validation-differs",
    )


def _links(readiness: DataMigrationReadiness) -> str:
    links: list[DocLink] = [*DIALECT_LINKS.get(readiness.dialect_key, ()), *SHARED_LINKS]
    body = "".join(
        f'<li><a href="{link.url}" target="_blank" rel="noopener">{link.label}</a></li>'
        for link in links
    )
    return _card(READING_TITLE, [f'<ul class="dmv-links">{body}</ul>'], anchor="dmv-reading")


def generate_data_migration_html_content(
    readiness: DataMigrationReadiness | None = None,
) -> tuple[str, str, str]:
    """Build the Data Migration & Validation tab. Returns ``(html, css, js)``.

    ``None`` is treated as a run with no registry, which is also what a CSV-only
    run produces.
    """
    if readiness is None:
        readiness = NO_PROJECT_STATE

    blocks = [
        f"""
        <div class="dmv-header">
            <h1 class="dmv-title">Data Migration &amp; Validation</h1>
            <p class="dmv-lede">{TAB_LEDE}</p>
        </div>""",
        _strip(readiness),
        f"""
        <div class="dmv-section">
            <h2 class="dmv-section-title">{KNOW_YOUR_DATA_TITLE}</h2>
            <p class="dmv-section-lede">{KNOW_YOUR_DATA_LEDE}</p>
        </div>""",
        _findings(readiness),
        _all_clean(readiness),
        _scripts(readiness),
        _topology(),
        _suggestions(readiness),
        _validation(),
        _links(readiness),
    ]

    body = "".join(block for block in blocks if block)
    return f"{_TAB_OPEN}{body}\n    </div>", DATA_MIGRATION_CSS, DATA_MIGRATION_JS


DATA_MIGRATION_CSS = """
        /* Data Migration & Validation tab (scoped to #data-migration-phase) */
        #data-migration-phase .dmv-header { margin-bottom: 28px; }
        #data-migration-phase .dmv-title {
            font-size: 1.875rem;
            font-weight: 800;
            color: #102E46;
            margin-bottom: 12px;
        }
        #data-migration-phase .dmv-lede {
            color: #64748B;
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 78ch;
        }
        #data-migration-phase .dmv-strip {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 28px;
        }
        #data-migration-phase .dmv-strip-label,
        #data-migration-phase .dmv-sub-title {
            font-size: 0.7rem;
            font-weight: 700;
            color: #64748B;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        #data-migration-phase .dmv-tiles { display: flex; gap: 10px; flex-wrap: wrap; }
        #data-migration-phase .dmv-tile {
            flex: 1 1 180px;
            border-radius: 10px;
            padding: 12px 14px;
            background: #F0F9FF;
            border: 1px solid #BAE6FD;
        }
        #data-migration-phase .dmv-tile-value {
            font-size: 1.5rem;
            font-weight: 800;
            line-height: 1.1;
            color: #0369A1;
        }
        #data-migration-phase .dmv-tile-name { font-size: 0.78rem; font-weight: 600; color: #102E46; }
        #data-migration-phase .dmv-tile-note { font-size: 0.72rem; color: #64748B; }
        #data-migration-phase .dmv-strip-note { margin-top: 12px; font-size: 0.83rem; color: #64748B; }
        #data-migration-phase .dmv-section { margin: 0 0 18px 0; }
        #data-migration-phase .dmv-section-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #102E46;
            margin-bottom: 8px;
        }
        #data-migration-phase .dmv-section-lede {
            color: #64748B;
            font-size: 0.95rem;
            line-height: 1.6;
            max-width: 82ch;
        }
        #data-migration-phase .dmv-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }
        #data-migration-phase .dmv-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #102E46;
            margin-bottom: 6px;
        }
        #data-migration-phase .dmv-card-lede {
            font-size: 0.88rem;
            color: #64748B;
            line-height: 1.55;
            margin: 0 0 16px 0;
            max-width: 82ch;
        }
        #data-migration-phase .dmv-types { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
        #data-migration-phase .dmv-types th {
            text-align: left;
            padding: 7px 8px;
            border-bottom: 1px solid #E2E8F0;
            font-size: 0.66rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        #data-migration-phase .dmv-types td {
            padding: 9px 8px;
            border-bottom: 1px solid #F1F5F9;
            color: #334155;
            vertical-align: top;
        }
        #data-migration-phase .dmv-types tr:last-child td { border-bottom: none; }
        #data-migration-phase .dmv-types code {
            font-size: 0.75rem;
            color: #102E46;
            background: #F8FAFC;
            border-radius: 4px;
            padding: 1px 5px;
        }
        #data-migration-phase .dmv-cell-usage { white-space: nowrap; color: #475569; }
        #data-migration-phase .dmv-cell-usage span { display: block; color: #94A3B8; font-size: 0.72rem; }
        #data-migration-phase .dmv-cell-note { color: #64748B; line-height: 1.5; min-width: 24ch; }
        #data-migration-phase .dmv-pill-status {
            display: inline-block;
            white-space: nowrap;
            border-radius: 999px;
            padding: 2px 9px;
            font-size: 0.7rem;
            font-weight: 600;
            border: 1px solid transparent;
        }
        #data-migration-phase .dmv-migration--supported,
        #data-migration-phase .dmv-validation--supported {
            background: #F0FDF4; border-color: #BBF7D0; color: #15803D;
        }
        #data-migration-phase .dmv-validation--schema-only,
        #data-migration-phase .dmv-validation--drift,
        #data-migration-phase .dmv-validation--no-row-comparison,
        #data-migration-phase .dmv-validation--not-documented {
            background: #FFFBEB; border-color: #FDE68A; color: #B45309;
        }
        #data-migration-phase .dmv-migration--unsupported,
        #data-migration-phase .dmv-validation--unsupported {
            background: #FEF2F2; border-color: #FECACA; color: #B91C1C;
        }
        #data-migration-phase .dmv-clean { font-size: 0.83rem; color: #64748B; margin: 14px 0 0 0; }
        #data-migration-phase .dmv-note {
            margin-top: 14px;
            border-left: 3px solid #29B5E8;
            border-radius: 0 8px 8px 0;
            background: #F0F9FF;
            padding: 12px 14px;
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.55;
        }
        #data-migration-phase .dmv-script {
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            margin-bottom: 10px;
            background: #F8FAFC;
        }
        #data-migration-phase .dmv-script summary {
            cursor: pointer;
            padding: 11px 14px;
            display: flex;
            flex-wrap: wrap;
            gap: 4px 10px;
            align-items: baseline;
        }
        #data-migration-phase .dmv-script-title { font-size: 0.85rem; font-weight: 700; color: #102E46; }
        #data-migration-phase .dmv-script-note { font-size: 0.78rem; color: #64748B; }
        #data-migration-phase .dmv-script-actions { display: flex; gap: 8px; padding: 0 14px 10px 14px; }
        #data-migration-phase .dmv-btn {
            font: inherit;
            font-size: 0.74rem;
            font-weight: 600;
            color: #0369A1;
            background: #FFFFFF;
            border: 1px solid #BAE6FD;
            border-radius: 6px;
            padding: 5px 11px;
            cursor: pointer;
        }
        #data-migration-phase .dmv-btn:hover { background: #F0F9FF; }
        #data-migration-phase .dmv-sql {
            margin: 0;
            padding: 14px;
            overflow-x: auto;
            background: #102E46;
            color: #E2E8F0;
            border-radius: 0 0 8px 8px;
            font-size: 0.73rem;
            line-height: 1.5;
            white-space: pre;
        }
        #data-migration-phase .dmv-picker { margin-bottom: 18px; }
        #data-migration-phase .dmv-question {
            display: flex;
            flex-wrap: wrap;
            gap: 8px 14px;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            margin-bottom: 8px;
            background: #F8FAFC;
        }
        #data-migration-phase .dmv-question-text { font-size: 0.85rem; color: #334155; max-width: 62ch; }
        #data-migration-phase .dmv-answers { display: flex; gap: 6px; }
        #data-migration-phase .dmv-pill {
            font: inherit;
            font-size: 0.75rem;
            font-weight: 600;
            color: #475569;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 999px;
            padding: 5px 13px;
            cursor: pointer;
            white-space: nowrap;
        }
        #data-migration-phase .dmv-pill[aria-pressed="true"] {
            background: #29B5E8;
            border-color: #29B5E8;
            color: #FFFFFF;
        }
        #data-migration-phase .dmv-reset {
            font: inherit;
            font-size: 0.72rem;
            color: #64748B;
            background: none;
            border: none;
            padding: 2px 0;
            cursor: pointer;
            text-decoration: underline;
            visibility: hidden;
        }
        #data-migration-phase .dmv-picker--answered .dmv-reset { visibility: visible; }
        #data-migration-phase .dmv-matrix { width: 100%; border-collapse: separate; border-spacing: 8px; }
        #data-migration-phase .dmv-matrix thead th {
            font-size: 0.68rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            text-align: left;
            padding: 0 8px;
        }
        #data-migration-phase .dmv-matrix tbody th {
            width: 16%;
            font-size: 0.72rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            text-align: left;
            vertical-align: middle;
        }
        #data-migration-phase .dmv-quad {
            width: 42%;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 13px 15px;
            background: #F8FAFC;
            vertical-align: top;
            transition: opacity 0.15s ease;
        }
        #data-migration-phase .dmv-quad-title { font-size: 0.88rem; font-weight: 700; color: #102E46; }
        #data-migration-phase .dmv-quad-body {
            font-size: 0.79rem;
            color: #475569;
            line-height: 1.5;
            margin: 5px 0 8px 0;
        }
        #data-migration-phase .dmv-quad-eff { font-size: 0.75rem; font-weight: 600; color: #0369A1; }
        #data-migration-phase .dmv-quad--active {
            background: #F0F9FF;
            border: 2px solid #29B5E8;
            padding: 12px 14px;
        }
        #data-migration-phase .dmv-quad--dim { opacity: 0.45; }
        #data-migration-phase .dmv-sub { margin-top: 20px; }
        #data-migration-phase .dmv-item { margin-bottom: 11px; }
        #data-migration-phase .dmv-item-title { font-size: 0.83rem; font-weight: 700; color: #102E46; }
        #data-migration-phase .dmv-item-body { font-size: 0.81rem; color: #475569; line-height: 1.55; }
        #data-migration-phase .dmv-item code,
        #data-migration-phase .dmv-cell-note code {
            font-size: 0.76rem;
            background: #F1F5F9;
            border-radius: 4px;
            padding: 1px 4px;
        }
        #data-migration-phase .dmv-list { margin: 0 0 0 18px; padding: 0; }
        #data-migration-phase .dmv-list li {
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.55;
            margin-bottom: 5px;
        }
        #data-migration-phase .dmv-para {
            font-size: 0.88rem;
            color: #475569;
            line-height: 1.65;
            margin: 0 0 12px 0;
            max-width: 82ch;
        }
        #data-migration-phase .dmv-para:last-child { margin-bottom: 0; }
        #data-migration-phase .dmv-links { margin: 0 0 0 18px; padding: 0; }
        #data-migration-phase .dmv-links li { font-size: 0.85rem; margin-bottom: 6px; }
        #data-migration-phase .dmv-links a { color: #0369A1; }
"""


# Delegated from `document` so a Vue re-render cannot strand the listeners, and
# scoped by `data-dmv-*` hooks so nothing here touches the report's own state.
# The SQL is read back out of the <pre> rather than carried a second time as a
# JS string literal, which makes what the customer copies identical to what the
# page shows by construction.
DATA_MIGRATION_JS = """
        (function () {
            const TAB = 'data-migration-phase';
            const answers = { unload: '', pull: '' };

            function sqlText(id) {
                const pre = document.getElementById(id);
                return pre ? pre.textContent : '';
            }

            function flash(button, label) {
                const original = button.textContent;
                button.textContent = label;
                setTimeout(function () { button.textContent = original; }, 1200);
            }

            function download(id, filename) {
                const blob = new Blob([sqlText(id)], { type: 'text/plain;charset=utf-8;' });
                const link = document.createElement('a');
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            }

            function paint() {
                const root = document.getElementById(TAB);
                if (!root) { return; }
                const complete = answers.unload !== '' && answers.pull !== '';
                const picker = root.querySelector('#dmv-picker');
                if (picker) { picker.classList.toggle('dmv-picker--answered', complete); }
                root.querySelectorAll('.dmv-pill').forEach(function (pill) {
                    const on = answers[pill.dataset.dmvAxis] === pill.dataset.dmvValue;
                    pill.setAttribute('aria-pressed', on ? 'true' : 'false');
                });
                root.querySelectorAll('.dmv-quad').forEach(function (quad) {
                    const hit = complete
                        && quad.dataset.dmvUnload === answers.unload
                        && quad.dataset.dmvPull === answers.pull;
                    quad.classList.toggle('dmv-quad--active', hit);
                    quad.classList.toggle('dmv-quad--dim', complete && !hit);
                });
            }

            document.addEventListener('click', function (event) {
                const target = event.target;
                if (!target || !target.closest) { return; }

                const pill = target.closest('.dmv-pill');
                if (pill) {
                    const axis = pill.dataset.dmvAxis;
                    answers[axis] = answers[axis] === pill.dataset.dmvValue
                        ? ''
                        : pill.dataset.dmvValue;
                    paint();
                    return;
                }

                if (target.closest('[data-dmv-reset]')) {
                    answers.unload = '';
                    answers.pull = '';
                    paint();
                    return;
                }

                const copy = target.closest('[data-dmv-copy]');
                if (copy) {
                    const text = sqlText(copy.dataset.dmvCopy);
                    if (navigator.clipboard) {
                        navigator.clipboard.writeText(text).then(function () {
                            flash(copy, 'Copied');
                        });
                    }
                    return;
                }

                const save = target.closest('[data-dmv-download]');
                if (save) {
                    download(save.dataset.dmvDownload, save.dataset.dmvFilename);
                }
            });
        })();
"""
