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

"""Render the Testing tab from a ``TestingReadiness``.

Presentation only: every count arrives already derived, and every string
already written (see ``content.py``). Each block is conditional — a section
that has nothing to say about this project is not rendered rather than
rendered empty.
"""

from __future__ import annotations

import html
import json
from collections.abc import Iterable, Sequence

from snowconvert_reports.testing_readiness import TestingReadiness

from .content import (
    ABSENCE_MESSAGE,
    BLOCKED_KICKER,
    CAP_MESSAGE,
    CURRENT_KICKER,
    DATA_VALIDATION_POINTER,
    DIALECT_CAVEATS,
    ETL_GATE,
    ETL_LADDER,
    ETL_LADDER_TITLE,
    ETL_PRECONDITION_NOTE,
    ETL_PRECONDITIONS,
    GAP_MESSAGE,
    MATRIX_HEADERS,
    NEXT_KICKER,
    NOTHING_TO_TEST,
    PICKER_HEADING,
    PICKER_HINT,
    PRECONDITION_AFFIRMATIONS,
    PROC_LADDER,
    PROC_LADDER_TITLE,
    PROC_PRECONDITION_NOTE,
    PROC_PRECONDITIONS,
    PROVEN,
    REACHED_KICKER,
    SUMMARY_BUYS_LABEL,
    SUMMARY_NEXT,
    SUMMARY_UNTESTED_LABEL,
    TAB_LEDE,
    UNLOCK_KICKER,
    UNSUPPORTED_PROC_STATEMENT,
    LadderGate,
    LadderTier,
    Precondition,
)

# Alpine directive and CSS hook; kept out of an f-string so the braces survive.
_TAB_OPEN = (
    '<div class="tab-content" id="testing-phase" '
    ':class="{active: activeTab === \'testing\'}">'
)

_CODE_UNIT_NOUN = "procedures and functions"
_CODE_UNIT_NOUN_WITH_SCRIPTS = "procedures, functions, and scripts"
_ETL_NOUN = "ETL units"

# What a run with no registry resolves to: no project-specific claim, and the
# procedure ladder still shown as guidance since no dialect ruled it out.
NO_PROJECT_STATE = TestingReadiness(
    has_project_state=False,
    source_dialect="",
    dialect_key="",
    code_units=None,
    etl_units=None,
    includes_scripts=False,
    proc_testing_supported=True,
)


def _code_unit_noun(includes_scripts: bool) -> str:
    return _CODE_UNIT_NOUN_WITH_SCRIPTS if includes_scripts else _CODE_UNIT_NOUN


def _tile(variant: str, value: int, name: str, note: str) -> str:
    return f"""
                <div class="tst-tile tst-tile--{variant}">
                    <div class="tst-tile-value">{value}</div>
                    <div class="tst-tile-name">{name}</div>
                    <div class="tst-tile-note">{note}</div>
                </div>"""


def _strip(readiness: TestingReadiness) -> str:
    """The "what's testable today" tiles.

    Counts testability, not test progress: the assessment report normally runs
    right after conversion, when nothing has been tested yet, so "388 ready to
    test" is the actionable number and "0 tested" would be noise.
    """
    buckets = readiness.code_units or readiness.etl_units
    if buckets is None:
        return ""

    counted_noun = (
        _code_unit_noun(readiness.includes_scripts)
        if readiness.code_units
        else _ETL_NOUN
    )
    tiles = [
        _tile("ready", buckets.ready, "Ready to test", "converted, no issues"),
        _tile("fix", buckets.needs_fix, "Fix conversion first", "EWI or FDM present"),
        _tile("blocked", buckets.blocked, "Not testable yet", "pending or not supported"),
    ]
    if readiness.code_units and readiness.etl_units:
        etl = readiness.etl_units
        tiles.append(
            _tile("etl", etl.total, "ETL units", f"{etl.ready} ready to test")
        )

    return f"""
        <div class="tst-strip">
            <div class="tst-strip-label">What&rsquo;s testable today <span>&middot; {counted_noun}</span></div>
            <div class="tst-tiles">{"".join(tiles)}
            </div>
            {_progress(readiness)}
        </div>"""


def _progress(readiness: TestingReadiness) -> str:
    """Test progress, only for families that actually report some.

    ETL progress reads ``stabilization`` and code-unit progress reads
    ``testing``; both arrive pre-resolved as ``tested``.
    """
    lines = []
    code = readiness.code_units
    if code and code.tested:
        noun = _code_unit_noun(readiness.includes_scripts)
        lines.append(f"{code.tested} of {code.total} {noun} tested")
    etl = readiness.etl_units
    if etl and etl.tested:
        lines.append(f"{etl.tested} of {etl.total} ETL units stabilized")

    if not lines:
        return ""
    return f'<div class="tst-progress">{" &middot; ".join(lines)}</div>'


def _precondition(item: Precondition) -> str:
    met = item.status == PROVEN
    return f"""
                    <li class="tst-pre-item{' tst-pre-met' if met else ''}">
                        <span class="tst-pre-mark">{"&#10003;" if met else "&bull;"}</span>{item.text}
                        <span class="tst-pre-state">{PRECONDITION_AFFIRMATIONS[item.status]}</span>
                    </li>"""


def _gate_row(ladder: str, gate: LadderGate) -> str:
    """The gate's reason reaches the DOM as an attribute rather than a JS string,
    so the sentence has exactly one home in ``content.py``."""
    input_id = f"tst-{ladder}-gate-{gate.key}"
    return f"""
                    <li class="tst-pre-item tst-pre-gate">
                        <input type="checkbox" id="{input_id}" data-tst-gate="{gate.cap_tier_key}"
                               data-tst-reason="{html.escape(gate.cap_reason)}">
                        <label for="{input_id}">{gate.label}</label>
                        <span class="tst-pre-detail">{gate.detail}</span>
                    </li>"""


def _preconditions(
    ladder: str,
    label: str,
    items: Sequence[Precondition],
    note: str,
    gate: LadderGate | None = None,
) -> str:
    rows = "".join(_precondition(item) for item in items)
    if gate is not None:
        rows += _gate_row(ladder, gate)
    return f"""
            <div class="tst-pre">
                <div class="tst-pre-label">{label}</div>
                <ul class="tst-pre-list">{rows}
                </ul>
                <p>{note}</p>
            </div>"""


def _picker(ladder: str, tiers: Sequence[LadderTier]) -> str:
    """One checkbox per rung that needs something.

    The labels are the matrix's "What you provide" column re-phrased, so the
    list and the ladder are one thing read two ways.
    """
    rows = []
    for tier in tiers:
        if not tier.requirement:
            continue
        input_id = f"tst-{ladder}-req-{tier.key}"
        rows.append(
            f"""
                    <li>
                        <input type="checkbox" id="{input_id}" data-tst-req="{tier.key}">
                        <label for="{input_id}">{tier.requirement}</label>
                    </li>"""
        )
    return f"""
            <div class="tst-picker">
                <div class="tst-picker-label">{PICKER_HEADING}<span>{PICKER_HINT}</span></div>
                <ul class="tst-picker-list">{"".join(rows)}
                </ul>
            </div>"""


def _stepper(tiers: Sequence[LadderTier]) -> str:
    """Rungs with empty kickers: which one is reached is a client-side question."""
    steps = "".join(
        f"""
                <div class="tst-step" data-tst-tier="{tier.key}">
                    <div class="tst-step-kicker"></div>
                    <div class="tst-step-name">{tier.name}</div>
                    <div class="tst-step-sub">{tier.qualifier}</div>
                </div>"""
        for tier in tiers
    )
    return f'<div class="tst-stepper">{steps}\n            </div>'


def _summary() -> str:
    """Filled by JS from the highlighted matrix row, so the prose has one home."""
    return '<div class="tst-summary" data-tst-summary hidden></div>'


def _message() -> str:
    return '<div class="tst-message" data-tst-message hidden></div>'


def _matrix(tiers: Sequence[LadderTier]) -> str:
    headers = "".join(f"<th>{h}</th>" for h in MATRIX_HEADERS)
    rows = "".join(
        f"""
                    <tr data-tst-tier="{tier.key}">
                        <td class="tst-cell-tier">{tier.name}<span>{tier.qualifier}</span></td>
                        <td>{tier.provides}</td>
                        <td>{tier.buys}</td>
                        <td class="tst-cell-gap">{tier.untested}</td>
                    </tr>"""
        for tier in tiers
    )
    return f"""
            <table class="tst-matrix">
                <thead><tr>{headers}</tr></thead>
                <tbody>{rows}
                </tbody>
            </table>"""


def _card(title: str, body: Iterable[str], anchor: str, ladder: str = "") -> str:
    scope = f' data-tst-ladder="{ladder}"' if ladder else ""
    return f"""
        <div class="tst-card" id="{anchor}"{scope}>
            <div class="tst-card-title">{title}</div>
            {"".join(part for part in body if part)}
        </div>"""


def _proc_ladder(readiness: TestingReadiness) -> str:
    caveat = DIALECT_CAVEATS.get(readiness.dialect_key)
    return _card(
        PROC_LADDER_TITLE,
        [
            _preconditions(
                "proc",
                "Required before any procedure/function testing",
                PROC_PRECONDITIONS,
                PROC_PRECONDITION_NOTE,
            ),
            _picker("proc", PROC_LADDER),
            _stepper(PROC_LADDER),
            _summary(),
            _matrix(PROC_LADDER),
            _message(),
            f'<div class="tst-caveat">{caveat}</div>' if caveat else "",
        ],
        anchor="tst-proc-ladder",
        ladder="proc",
    )


def _unsupported_proc(readiness: TestingReadiness) -> str:
    dialect = html.escape(readiness.source_dialect) or "this"
    return _card(
        PROC_LADDER_TITLE,
        [
            f'<div class="tst-note">{UNSUPPORTED_PROC_STATEMENT.format(dialect=dialect)}</div>'
        ],
        anchor="tst-proc-unsupported",
    )


def _etl_ladder() -> str:
    return _card(
        ETL_LADDER_TITLE,
        [
            _preconditions(
                "etl",
                "Required before any ETL testing",
                ETL_PRECONDITIONS,
                ETL_PRECONDITION_NOTE,
                gate=ETL_GATE,
            ),
            _picker("etl", ETL_LADDER),
            _stepper(ETL_LADDER),
            _summary(),
            _matrix(ETL_LADDER),
            _message(),
        ],
        anchor="tst-etl-ladder",
        ladder="etl",
    )


def generate_testing_html_content(
    readiness: TestingReadiness | None = None,
) -> tuple[str, str, str]:
    """Build the Testing tab. Returns ``(html, css, js)``.

    ``readiness`` is a ``TestingReadiness``; ``None`` is treated as a run with
    no registry, which is also what a CSV-only run produces.
    """
    if readiness is None:
        readiness = NO_PROJECT_STATE

    has_state = readiness.has_project_state
    # No registry means no project state to gate on, so both ladders render as
    # guidance. They assert no rung either way, so nothing here depends on
    # registry contents beyond deciding which ladders are relevant at all.
    show_proc = readiness.code_units is not None or not has_state
    show_etl = readiness.etl_units is not None or not has_state

    blocks = [
        f"""
        <div class="tst-header">
            <h1 class="tst-title">Testing</h1>
            <p class="tst-lede">{TAB_LEDE}</p>
        </div>""",
        _strip(readiness) if has_state else "",
    ]

    if show_proc:
        blocks.append(
            _proc_ladder(readiness)
            if readiness.proc_testing_supported
            else _unsupported_proc(readiness)
        )
    if show_etl:
        blocks.append(_etl_ladder())
    if has_state and not show_proc and not show_etl:
        blocks.append(f'<div class="tst-note">{NOTHING_TO_TEST}</div>')

    blocks.append(f'<div class="tst-pointer">{DATA_VALIDATION_POINTER}</div>')

    body = "".join(block for block in blocks if block)
    return f"{_TAB_OPEN}{body}\n    </div>", TESTING_CSS, TESTING_JS


TESTING_CSS = """
        /* Testing phase tab (scoped to #testing-phase) */
        #testing-phase .tst-header { margin-bottom: 28px; }
        #testing-phase .tst-title {
            font-size: 1.875rem;
            font-weight: 800;
            color: #102E46;
            margin-bottom: 12px;
        }
        #testing-phase .tst-lede {
            color: #64748B;
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 78ch;
        }
        #testing-phase .tst-strip {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 24px;
        }
        #testing-phase .tst-strip-label {
            font-size: 0.7rem;
            font-weight: 700;
            color: #64748B;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        #testing-phase .tst-strip-label span { font-weight: 500; letter-spacing: 0.02em; }
        #testing-phase .tst-tiles { display: flex; gap: 10px; flex-wrap: wrap; }
        #testing-phase .tst-tile {
            flex: 1 1 160px;
            border-radius: 10px;
            padding: 12px 14px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
        }
        #testing-phase .tst-tile-value { font-size: 1.5rem; font-weight: 800; line-height: 1.1; color: #475569; }
        #testing-phase .tst-tile-name { font-size: 0.78rem; font-weight: 600; color: #334155; }
        #testing-phase .tst-tile-note { font-size: 0.72rem; color: #64748B; }
        #testing-phase .tst-tile--ready { background: #F0FDF4; border-color: #BBF7D0; }
        #testing-phase .tst-tile--ready .tst-tile-value { color: #15803D; }
        #testing-phase .tst-tile--ready .tst-tile-name { color: #166534; }
        #testing-phase .tst-tile--ready .tst-tile-note { color: #4D7C5A; }
        #testing-phase .tst-tile--fix { background: #FFFBEB; border-color: #FDE68A; }
        #testing-phase .tst-tile--fix .tst-tile-value { color: #B45309; }
        #testing-phase .tst-tile--fix .tst-tile-name { color: #92400E; }
        #testing-phase .tst-tile--fix .tst-tile-note { color: #A16207; }
        #testing-phase .tst-progress {
            margin-top: 12px;
            font-size: 0.85rem;
            color: #475569;
        }
        #testing-phase .tst-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }
        #testing-phase .tst-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #102E46;
            margin-bottom: 16px;
        }
        #testing-phase .tst-pre {
            background: #F8FAFC;
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 16px;
        }
        #testing-phase .tst-pre-label {
            font-size: 0.68rem;
            font-weight: 700;
            color: #475569;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        #testing-phase .tst-pre ul { margin: 0 0 8px 18px; padding: 0; }
        #testing-phase .tst-pre li,
        #testing-phase .tst-pre p {
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.55;
            margin: 0 0 4px 0;
        }
        #testing-phase .tst-stepper { display: flex; align-items: stretch; margin-bottom: 16px; }
        #testing-phase .tst-step {
            flex: 1;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 10px 12px;
            min-width: 0;
        }
        #testing-phase .tst-step:first-child { border-radius: 8px 0 0 8px; }
        #testing-phase .tst-step:last-child { border-radius: 0 8px 8px 0; }
        #testing-phase .tst-step--current { background: #F0F9FF; border: 2px solid #29B5E8; }
        #testing-phase .tst-step-kicker {
            font-size: 0.58rem;
            font-weight: 800;
            color: #94A3B8;
            letter-spacing: 0.05em;
        }
        #testing-phase .tst-step--current .tst-step-kicker { color: #0369A1; }
        #testing-phase .tst-step-name {
            font-size: 0.82rem;
            font-weight: 700;
            color: #475569;
            margin-top: 3px;
        }
        #testing-phase .tst-step--current .tst-step-name { color: #102E46; }
        #testing-phase .tst-step-sub { font-size: 0.72rem; color: #94A3B8; }
        #testing-phase .tst-step--current .tst-step-sub { color: #64748B; }
        #testing-phase .tst-matrix { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
        #testing-phase .tst-matrix th {
            text-align: left;
            padding: 7px 8px;
            border-bottom: 1px solid #E2E8F0;
            font-size: 0.66rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        #testing-phase .tst-matrix th:first-child { width: 18%; }
        #testing-phase .tst-matrix td {
            padding: 9px 8px;
            border-bottom: 1px solid #F1F5F9;
            color: #334155;
            vertical-align: top;
        }
        #testing-phase .tst-matrix tr:last-child td { border-bottom: none; }
        #testing-phase .tst-matrix .tst-cell-tier { font-weight: 600; color: #102E46; }
        #testing-phase .tst-matrix .tst-cell-tier span { display: block; font-weight: 400; color: #94A3B8; }
        #testing-phase .tst-matrix .tst-cell-gap { color: #64748B; }
        #testing-phase .tst-row--current { background: #F0F9FF; }
        #testing-phase .tst-row--current .tst-cell-tier { font-weight: 700; }
        #testing-phase .tst-note,
        #testing-phase .tst-caveat {
            margin-top: 14px;
            border-left: 3px solid #94A3B8;
            border-radius: 0 8px 8px 0;
            background: #F8FAFC;
            padding: 12px 14px;
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.55;
        }
        #testing-phase .tst-caveat { border-left-color: #29B5E8; background: #F0F9FF; }
        #testing-phase .tst-pointer { font-size: 0.9rem; color: #64748B; }
        #testing-phase .tst-pre-list { list-style: none; margin: 0 0 8px 0; padding: 0; }
        #testing-phase .tst-pre-item {
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.6;
            margin-bottom: 4px;
        }
        #testing-phase .tst-pre-mark { color: #94A3B8; font-weight: 700; margin-right: 6px; }
        #testing-phase .tst-pre-met .tst-pre-mark { color: #15803D; }
        #testing-phase .tst-pre-state {
            display: inline-block;
            margin-left: 6px;
            font-size: 0.7rem;
            color: #64748B;
        }
        #testing-phase .tst-pre-met .tst-pre-state {
            color: #15803D;
            background: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 999px;
            padding: 1px 8px;
        }
        #testing-phase .tst-pre-gate label { color: #92400E; }
        #testing-phase .tst-pre-detail {
            flex-basis: 100%;
            font-size: 0.76rem;
            color: #94A3B8;
        }
        #testing-phase .tst-picker { margin-bottom: 16px; }
        #testing-phase .tst-picker-label {
            font-size: 0.68rem;
            font-weight: 700;
            color: #475569;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        #testing-phase .tst-picker-label span {
            text-transform: none;
            font-weight: 400;
            letter-spacing: 0;
            color: #94A3B8;
            margin-left: 8px;
        }
        #testing-phase .tst-picker-list { list-style: none; margin: 0; padding: 0; }
        #testing-phase .tst-picker-list li,
        #testing-phase .tst-pre-gate {
            display: flex;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 8px;
        }
        #testing-phase .tst-picker-list label,
        #testing-phase .tst-pre-gate label {
            font-size: 0.83rem;
            color: #334155;
            cursor: pointer;
        }
        #testing-phase .tst-picker-list input,
        #testing-phase .tst-pre-gate input { accent-color: #29B5E8; cursor: pointer; }
        #testing-phase .tst-picker-list input:checked + label { font-weight: 600; color: #102E46; }
        /* Reserved so a neutral stepper is the same height as an answered one. */
        #testing-phase .tst-step-kicker { min-height: 0.72rem; }
        #testing-phase .tst-step--reached { background: #F0FDF4; border-color: #BBF7D0; }
        #testing-phase .tst-step--reached .tst-step-kicker { color: #15803D; }
        #testing-phase .tst-step--reached .tst-step-name { color: #166534; }
        #testing-phase .tst-step--blocked { background: #FFFBEB; border: 1px dashed #FDE68A; }
        #testing-phase .tst-step--blocked .tst-step-kicker { color: #B45309; }
        #testing-phase .tst-step--blocked .tst-step-name { color: #92400E; }
        #testing-phase .tst-step--locked { opacity: 0.55; }
        #testing-phase .tst-row--locked { opacity: 0.55; }
        #testing-phase .tst-summary {
            margin: 0 0 16px 0;
            border-left: 3px solid #29B5E8;
            border-radius: 0 8px 8px 0;
            background: #F0F9FF;
            padding: 12px 14px;
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.6;
        }
        #testing-phase .tst-message {
            margin-top: 14px;
            border-left: 3px solid #94A3B8;
            border-radius: 0 8px 8px 0;
            background: #F8FAFC;
            padding: 12px 14px;
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.55;
        }
        #testing-phase .tst-message--gap,
        #testing-phase .tst-message--cap {
            border-left-color: #F59E0B;
            background: #FFFBEB;
            color: #92400E;
        }
"""


# The JS needs the kicker lexicon and three message templates, which are prose
# and live in content.py. Everything else it reads from the DOM: rung order and
# identity from data-tst-tier, rung names from the step labels, requirement names
# from the picker labels, and the summary from the matrix row it highlights.
# `</` is broken up so no copy edit can close the script tag early.
_LADDER_COPY = json.dumps(
    {
        "reached": REACHED_KICKER,
        "current": CURRENT_KICKER,
        "next": NEXT_KICKER,
        "unlock": UNLOCK_KICKER,
        "blocked": BLOCKED_KICKER,
        "buysLabel": SUMMARY_BUYS_LABEL,
        "untestedLabel": SUMMARY_UNTESTED_LABEL,
        "summaryNext": SUMMARY_NEXT,
        "gap": GAP_MESSAGE,
        "cap": CAP_MESSAGE,
        "absence": ABSENCE_MESSAGE,
    }
).replace("</", "<\\/")


TESTING_JS = """
        (function () {
            const COPY = __LADDER_COPY__;

            /**
             * Highest rung whose every required predecessor is ticked, then
             * capped by the gate. The ladder is cumulative, so a gap below a
             * rung blocks it. `capIndex` is -1 when nothing caps; the return is
             * -1 when the ladder sits below its own first rung.
             */
            function reachedIndex(required, ticked, capIndex) {
                let reached = -1;
                for (let i = 0; i < required.length; i += 1) {
                    if (required[i] && !ticked[i]) { break; }
                    reached = i;
                }
                if (capIndex >= 0 && reached > capIndex) { return capIndex; }
                return reached;
            }

            function text(node) { return node ? node.textContent.trim() : ''; }

            function read(card) {
                const steps = Array.prototype.slice.call(card.querySelectorAll('.tst-step'));
                const keys = steps.map(function (step) { return step.dataset.tstTier; });
                const boxes = {};
                card.querySelectorAll('[data-tst-req]').forEach(function (box) {
                    boxes[box.dataset.tstReq] = box;
                });
                return {
                    card: card,
                    steps: steps,
                    keys: keys,
                    gate: card.querySelector('[data-tst-gate]'),
                    names: steps.map(function (step) {
                        return text(step.querySelector('.tst-step-name'));
                    }),
                    required: keys.map(function (key) { return key in boxes; }),
                    ticked: keys.map(function (key) {
                        return key in boxes && boxes[key].checked;
                    }),
                    labels: keys.map(function (key) {
                        return key in boxes
                            ? text(card.querySelector('label[for="' + boxes[key].id + '"]'))
                            : '';
                    })
                };
            }

            function resolve(ladder) {
                const gate = ladder.gate;
                const capIndex = gate && !gate.checked
                    ? ladder.keys.indexOf(gate.dataset.tstGate)
                    : -1;
                const access = reachedIndex(ladder.required, ladder.ticked, -1);
                const reached = reachedIndex(ladder.required, ladder.ticked, capIndex);
                return {
                    neutral: ladder.ticked.indexOf(true) === -1 && !(gate && gate.checked),
                    access: access,
                    reached: reached,
                    capped: capIndex >= 0 && access > reached
                };
            }

            function kicker(index, state) {
                if (state.capped && index > state.reached && index <= state.access) {
                    return COPY.blocked;
                }
                if (index < state.reached) { return COPY.reached; }
                if (index === state.reached) { return COPY.current; }
                if (index === state.reached + 1) { return COPY.next; }
                return COPY.unlock;
            }

            function paintSteps(ladder, state) {
                ladder.steps.forEach(function (step, index) {
                    const label = state.neutral ? '' : kicker(index, state);
                    step.querySelector('.tst-step-kicker').textContent = label;
                    step.classList.toggle('tst-step--reached', label === COPY.reached);
                    step.classList.toggle('tst-step--current', label === COPY.current);
                    step.classList.toggle('tst-step--blocked', label === COPY.blocked);
                    step.classList.toggle('tst-step--locked', label === COPY.unlock);
                });
            }

            function row(ladder, index) {
                if (index < 0 || index >= ladder.keys.length) { return null; }
                return ladder.card.querySelector('tr[data-tst-tier="' + ladder.keys[index] + '"]');
            }

            function paintRows(ladder, state) {
                ladder.keys.forEach(function (key, index) {
                    const tr = row(ladder, index);
                    if (!tr) { return; }
                    tr.classList.toggle(
                        'tst-row--current', !state.neutral && index === state.reached);
                    tr.classList.toggle(
                        'tst-row--locked', !state.neutral && index > state.reached);
                });
            }

            function fill(node, markup, tone) {
                node.innerHTML = markup;
                node.hidden = !markup;
                if (tone !== undefined) { node.className = 'tst-message ' + tone; }
            }

            function paintSummary(ladder, state) {
                const panel = ladder.card.querySelector('[data-tst-summary]');
                if (!panel) { return; }
                const tr = state.neutral ? null : row(ladder, state.reached);
                if (!tr) { fill(panel, ''); return; }
                const lines = [
                    '<strong>' + COPY.buysLabel + ':<\\/strong> ' + tr.cells[2].innerHTML,
                    '<strong>' + COPY.untestedLabel + ':<\\/strong> ' + tr.cells[3].innerHTML
                ];
                const next = ladder.labels[state.reached + 1];
                if (next) { lines.push(COPY.summaryNext.replace('{requirement}', next)); }
                fill(panel, lines.join('<br>'));
            }

            function highestTickedAbove(ladder, index) {
                for (let i = ladder.ticked.length - 1; i > index; i -= 1) {
                    if (ladder.ticked[i]) { return i; }
                }
                return -1;
            }

            /** The cap is the harder constraint, so it wins when a gap also holds. */
            function message(ladder, state) {
                if (state.neutral) { return ['', '']; }
                if (state.capped) {
                    return [COPY.cap
                        .replace('{reached}', ladder.names[state.access])
                        .replace('{reason}', ladder.gate.dataset.tstReason),
                    'tst-message--cap'];
                }
                if (state.reached < 0) {
                    return [COPY.absence
                        .replace('{tier}', ladder.names[0])
                        .replace('{requirement}', ladder.labels[0]),
                    'tst-message--cap'];
                }
                const gap = highestTickedAbove(ladder, state.access);
                if (gap < 0) { return ['', '']; }
                return [COPY.gap
                    .replace('{ticked}', ladder.names[gap])
                    .replace('{missing}', ladder.labels[state.access + 1]),
                'tst-message--gap'];
            }

            function paint(card) {
                const ladder = read(card);
                const state = resolve(ladder);
                paintSteps(ladder, state);
                paintRows(ladder, state);
                paintSummary(ladder, state);
                const node = card.querySelector('[data-tst-message]');
                if (node) {
                    const parts = message(ladder, state);
                    fill(node, parts[0], parts[1]);
                }
            }

            // `change` rather than `click`: it bubbles, fires for keyboard
            // space, and does not double-fire when a label forwards to its input.
            document.addEventListener('change', function (event) {
                const target = event.target;
                if (!target || !target.closest) { return; }
                if (!target.matches('[data-tst-req], [data-tst-gate]')) { return; }
                const card = target.closest('[data-tst-ladder]');
                if (card) { paint(card); }
            });

            // The reached-rung rule is the only logic here not visible in the
            // markup, so it is exposed for direct testing.
            window.snowconvertTestingLadder = { reachedIndex: reachedIndex };
        })();
""".replace("__LADDER_COPY__", _LADDER_COPY)
