"""Citation gate (layer ③) for the enrichment critics — asymmetric by design.

A positive-contradiction (mode a) is hard-gated on a harness-verifiable span: the gate re-resolves
the cited fact and confirms the contradiction, so a fabricated critique is dropped toward ACCEPT.
An absence-of-support (mode b) is NOT hard-gatable (no span verifies a negative), so it becomes a
bounded REVISE that escalates to a human at budget-exhaustion. A REJECT that is not a verifiable
mode-a contradiction is coerced to a bounded REVISE — the gate never hard-blocks on an unverifiable
claim. This module makes ZERO model calls.
"""
from __future__ import annotations

import enum
import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field

from critic_index import ObjectIndex, canon_table
from critic_normalize import normalize
from manifest import classify_rejections

_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*")


class CitationType(enum.StrEnum):
    # The mode-a citation contract shared with prompts/critics/verdict-contract.md; one source of
    # truth so a typo in a comparison (or an emitted label) can't silently downgrade a REJECT.
    INVENTED_LITERAL = "invented_literal"
    DECLARED_ENUM = "declared_enum"
    FK_PARENT_MISMATCH = "fk_parent_mismatch"


@dataclass
class VerdictEntry:
    kind: str
    table: str | None
    columns: list
    verdict: str
    mode: str | None
    citation: dict
    feedback: str


@dataclass
class Verdict:
    ok: bool
    error: str = ""
    envelope_sig: str | None = None
    verdicts: list = field(default_factory=list)


def parse_verdict(text: object) -> Verdict:
    try:
        doc = json.loads(text)
    except (json.JSONDecodeError, TypeError, RecursionError) as exc:
        # RecursionError: a deeply nested array is malformed input, not a harness bug, and the caller's
        # contract is a Verdict carrying the reason -- not a traceback out of the enrich phase.
        return Verdict(False, f"verdict is not valid JSON: {exc}")
    if not isinstance(doc, dict):
        return Verdict(False, "verdict is not a JSON object")
    raw = doc.get("verdicts")
    if not isinstance(raw, list):
        return Verdict(False, "verdict 'verdicts' is missing or not a list")
    entries: list = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict) or "verdict" not in entry:
            return Verdict(False, f"verdict entry {index} is malformed (needs a 'verdict' field)")
        cols = entry.get("columns")
        if not isinstance(cols, list):
            cols = [entry["column"]] if entry.get("column") is not None else []
        entries.append(VerdictEntry(
            kind=entry.get("kind", ""),
            table=entry.get("table"),
            columns=cols,
            verdict=str(entry.get("verdict", "")).strip().upper(),
            mode=(str(entry["mode"]).strip().lower() if entry.get("mode") is not None else None),
            citation=entry.get("citation") if isinstance(entry.get("citation"), dict) else {},
            feedback=str(entry.get("feedback", "")),
        ))
    return Verdict(True, "", doc.get("envelope_sig"), entries)


class GateAction(enum.StrEnum):
    # The gate's outcome vocabulary. run_pipeline branches on these and _SEVERITY orders them, so a
    # bare literal here would silently route a decision to the wrong arm (or drop out of _SEVERITY).
    DROP = "drop"            # fabricated critique: discard it, the enrichment survives
    REVISE = "revise"        # unverifiable claim: bounded re-prompt of the fragment
    REJECT = "reject"        # verified mode-a contradiction: hard block
    ESCALATE = "escalate"    # a human must look (value cycle / unknown verdict label)
    ACCEPT_ALL = "accept_all"


@dataclass
class GateDecision:
    action: GateAction
    report: dict
    message: str
    record_values: list = field(default_factory=list)


_SEVERITY = {GateAction.ESCALATE: 3, GateAction.REJECT: 2, GateAction.REVISE: 1}


def _revise_detail(e: VerdictEntry, reason: str) -> dict:
    return {"kind": e.kind, "table": e.table, "columns": e.columns,
            "mode": "b", "reason": reason, "feedback": e.feedback}


def _adjudicate_reject(e: VerdictEntry, index: ObjectIndex) -> tuple[GateAction, dict]:
    # Only a harness-verifiable mode-a contradiction can hard-gate; everything else -> bounded REVISE.
    if e.mode != "a" or not e.citation:
        return GateAction.REVISE, _revise_detail(e, "reject_without_verifiable_mode_a_citation")
    # Normalized like `verdict` and `mode`: an off-case label is a producer slip, and leaving it raw would
    # silently demote the only verifiable REJECT classes to unverifiable_citation_type.
    ctype = str(e.citation.get("type") or "").strip().lower()
    table = e.table
    col = e.columns[0] if e.columns else None
    lit = e.citation.get("literal")
    if ctype in (CitationType.INVENTED_LITERAL, CitationType.DECLARED_ENUM):
        # No literal cited: nothing to verify either way. Without this, an empty literal is vacuously
        # "grounded" (DROP, with an audit line claiming a match) or vacuously out-of-domain (hard REJECT).
        # Emptiness is judged after normalize, so a numeric or boolean literal still counts as cited.
        if not normalize(lit):
            return GateAction.REVISE, _revise_detail(e, "citation_missing_literal")
    if ctype == CitationType.INVENTED_LITERAL:
        if index.literal_grounded_in_cell(table, col, lit):
            return GateAction.DROP, {"kind": e.kind, "table": table, "column": col, "literal": lit,
                                     "why": "cited literal is grounded in source"}
        return GateAction.REJECT, {"kind": e.kind, "table": table, "column": col, "literal": lit,
                                   "citation": CitationType.INVENTED_LITERAL, "feedback": e.feedback}
    if ctype == CitationType.DECLARED_ENUM:
        # Both the domain test and the membership test are the backbone's, so the two layers cannot
        # disagree on whether this column has a declared domain or on what is in it.
        if index.is_declared_enum(table, col) and not index.literal_in_declared_domain(table, col, lit):
            return GateAction.REJECT, {"kind": e.kind, "table": table, "column": col, "literal": lit,
                                       "citation": CitationType.DECLARED_ENUM, "feedback": e.feedback}
        return GateAction.DROP, {"kind": e.kind, "table": table, "column": col, "literal": lit,
                                 "why": "literal is within the declared domain / no domain to contradict"}
    if ctype == CitationType.FK_PARENT_MISMATCH:
        ct, cc = e.citation.get("child_table"), e.citation.get("child_col")
        proposed = e.citation.get("proposed_parent_table")
        parent = canon_table(proposed).casefold()
        if not parent:  # no parent named -> nothing to verify; fail-safe to bounded REVISE, never drop
            return GateAction.REVISE, _revise_detail(e, "fk_citation_missing_proposed_parent")
        mined = [normalize(c.get("detail")) for c in index.cell_constraints(ct, cc)
                 if c.get("kind") in ("fk", "join_edge")]
        if not mined:
            return GateAction.REVISE, _revise_detail(e, "fk_no_mined_edge_to_verify")
        # Identifier-boundary match, not substring: a degenerate name canonicalizes to "", which is a
        # substring of every edge and would DROP the critique unconditionally. The child's own name is
        # deliberately still eligible -- a self-referencing FK is legitimate, and excluding it would turn
        # one into a hard REJECT, which this gate may only ever do on a verified contradiction.
        if any(parent in _IDENT.findall(m) for m in mined):
            return GateAction.DROP, {"kind": e.kind, "child": f"{ct}.{cc}", "proposed_parent": proposed,
                                     "why": "proposed parent matches a mined edge"}
        return GateAction.REJECT, {"kind": e.kind, "child": f"{ct}.{cc}", "proposed_parent": proposed,
                                   "citation": CitationType.FK_PARENT_MISMATCH, "mined_edges": mined,
                                   "feedback": e.feedback}
    return GateAction.REVISE, _revise_detail(e, "unverifiable_citation_type")


def apply_gate(verdict: Verdict, index: ObjectIndex,
               previously_rejected: Callable[[str | None, str | None, object], bool]) -> GateDecision:
    """Adjudicate a parsed critic verdict into one gate action for the whole envelope.

    Each non-ACCEPT entry is adjudicated independently, then the most severe outcome wins
    (escalate > reject > revise); DROPs are recorded but never escalate. `previously_rejected`
    answers whether a (table, column, literal) has already been rejected in an earlier round, which
    turns a repeat REJECT into an escalate rather than another loop. Its signature is the one
    manifest.classify_rejections declares -- the literal is whatever the citation carried (a number
    or a bool is still a cited value), and one declared shape is what lets the same predicate serve
    this path and the backbone-stop. Returns ACCEPT_ALL when nothing is actionable. `record_values`
    is the caller's to persist -- the gate holds no state.
    """
    actions: list = []      # [(GateAction, detail)]
    dropped: list = []
    record_values: list = []
    for e in verdict.verdicts:
        if e.verdict == "ACCEPT":
            continue
        if e.verdict == "REJECT":
            kind, detail = _adjudicate_reject(e, index)
        elif e.verdict == "REVISE":
            kind, detail = GateAction.REVISE, _revise_detail(e, "absence_of_support")
        else:
            kind, detail = GateAction.ESCALATE, {"kind": e.kind, "reason": "unknown_verdict_label",
                                                 "label": e.verdict, "feedback": e.feedback}
        if kind == GateAction.DROP:
            dropped.append(detail)
            continue
        if kind == GateAction.REJECT:
            # Same helper the backbone-stop consumes, over this path's own data shape: an fk
            # mismatch carries no `literal`, so it records nothing and cannot read as a repeat.
            cycle, recorded = classify_rejections(
                [(detail.get("table"), detail.get("column"), detail.get("literal"))],
                previously_rejected)
            record_values.extend(recorded)
            if cycle:
                actions.append((GateAction.ESCALATE, {**detail, "reason": "value_cycle"}))
                continue
            actions.append((GateAction.REJECT, detail))
        else:
            actions.append((kind, detail))

    if not actions:
        return GateDecision(GateAction.ACCEPT_ALL,
                            {"reason": "critic_accept", "dropped": dropped},
                            "critic verdict: all entries accepted", record_values)
    # Picked from `actions` rather than by searching _SEVERITY for the key holding the max value, which
    # only resolves to the right action while every severity is distinct.
    action = max(actions, key=lambda a: _SEVERITY[a[0]])[0]  # GateAction, so f-strings emit its value
    report = {"reason": f"critic_{action}", "entries": [d for _, d in actions], "dropped": dropped}
    message = f"critic {action}: {len(actions)} actionable verdict(s); see enrichment-report.json"
    return GateDecision(action, report, message, record_values)
