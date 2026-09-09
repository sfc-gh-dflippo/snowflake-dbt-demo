"""GATE A (judgement half) — DOES THE IR CARRY EVERYTHING THE SOURCE DOCUMENT NEEDS?

This module is the harness on both sides of an agentic verifier. It does NOT contain the judgement;
it makes the judgement checkable. Three subcommands:

    pack   build a blind evidence bundle + the deterministically raised obligation set
    score  ingest a verifier's answers, verify every citation, adjudicate, write the ledger
    run    pack, invoke a configured verifier command, score

WHY A MODEL AND NOT A RULE — the measured justification, not an argument
-----------------------------------------------------------------------
`element-id-fit/declared_vs_identified.py` reported `lost=0` on all four blind platforms INCLUDING
the two that emitted nothing, and on DataStage it balanced `declared=4 identified=4` over a document
holding FIVE elements. The missing one held every derivation in the job. Its denominator is the
identification sweep's own output, so an element the sweep never declared cannot be reported as lost.

`coverage_gate.py` fixed that half by deriving its denominator from the SOURCE DOCUMENT. It is on the
driver's path at stage 3d and it reports COVERAGE COMPLETE, exit 0, on all four blind documents today.
So what is left is the question neither can ask: is there something in this file that MATTERS and is
not in the IR? That needs a reader.

THIS FILE DOES NOT DUPLICATE coverage_gate.py. It imports it and calls its counters, and it embeds its
report verbatim as evidence. If the counting rule changes there, it changes here.

WHAT IT RAISES, deterministically, BEFORE any verifier is invoked
----------------------------------------------------------------
Four obligation families, and the denominator is the document in every one of them:

  EL:<id>   one per source element under coverage_gate's per-platform counting rule.
  LK:<id>   one per LINK the document declares, under a rule read off the platform table's
            `edge_policy` (EXPLICIT_EDGE_ELEMENTS / COLLAPSE_FIELD_EDGES / pin_pairs). Elements were
            counted and edges never were: DataStage lost 3 of 3 and the ledger said lost=0.
  RS:<sig>  one per RESIDUE CLASS — content the element rule and the link rule do not account for.
            This is the known-unknown set, and it is where an entire family (SSIS control-flow
            executables, a Kettle database connection, DataStage job parameters) can be invisible to
            a gate that only counts elements. Consumes an external identification inventory when one
            is supplied (--inventory), and computes its own from the document when one is not.
  IX:<id>   one per IR node/edge that NO document obligation matched. The other direction: an IR that
            states something the document does not. On the frozen DataStage fixture two of three
            edges are of this kind.

THE BAR IS OBLIGATIONS DISCHARGED. IT IS NEVER A SCORE.
-------------------------------------------------------
Measured in this project: the fit score ROSE as elements were lost (0 lost 84.8%, 6 lost 89.9%). A
number the loop can move is not a bar. So:

  * the raised set is recomputed from the document every iteration and cannot shrink;
  * an obligation with no answer is OUTSTANDING, never silently discharged;
  * an answer naming an obligation that was not raised is REJECTED;
  * `raised == discharged + outstanding` is asserted and printed;
  * no percentage appears in the verdict.

CITATION VERIFICATION — the mechanical form of "never adjudicate from priors"
----------------------------------------------------------------------------
A sub-agent in this project asserted that Informatica `||` propagates NULL — backwards, and in the
same direction as the engine's own bug. Gate B then measured that handing a verifier primary sources
bought CALIBRATION rather than detection: the naive arm was right and unearnedly so.

For Gate A the primary source is the document itself, so the response is checkable rather than
exhortative: every verdict-changing claim must carry `doc_locus` (a line number) and `doc_quote`, and
the scorer RE-READS that line. A claim whose quote is not there is QUARANTINED — it cannot discharge
an obligation and cannot raise a finding. Claims declaring `basis: PRIOR` are quarantined by
construction and printed, so an uncalibrated verifier that happens to be right is visible as such.

LEGITIMATE ABSENCE VERSUS REAL LOSS
-----------------------------------
`ABSENT_BY_TABLE_RULE` is accepted ONLY when the platform table really declares a collapse for that
kind. Otherwise the scorer DOWNGRADES it to ABSENT_SILENTLY_DROPPED and says so. The loop must not be
able to talk a loss into a design decision — that is the same move as the fit score rewarding loss.

PROVENANCE
----------
Nothing here patches a deterministic file. Output is a sidecar carrying `provenance: MODEL`, plus a
loop record stating WHY the loop stopped — CONVERGED, EXHAUSTED_ITERATIONS or NO_PROGRESS — because
*converged* and *gave up* looking identical is the same conflation as exit 0 versus exit 3.

THE CONVERGENCE LOOP, AND WHY TURNING IT ON NEEDED THREE PROPERTIES FIRST
------------------------------------------------------------------------
`run --max-iterations N` packs, calls the verifier and scores up to N times, carrying the previous
UNRESOLVED list forward from iteration 2 on. `--max-iterations 1` is the single-pass control arm.

A LOOP THAT RE-ASKS UNTIL NOTHING IS OUTSTANDING IS A GATE THAT CANNOT FAIL: iterating toward
convergence is optimising for a clean ledger, which is the same move as the fit score that rose while
elements were lost. Four gates in this project were found incapable of failing, each caught by
disbelieving a good number. So the loop reports three things it could hide, all in `gateA-loop-run.json`
and all on stdout:

  * the DENOMINATOR is asserted identical across every iteration — ids and order, recomputed from the
    document each time — and a run whose raised set moves is aborted as a GATE DEFECT (exit 1), not
    reported as a verdict. See `denominator_drift`;
  * every verdict change is counted BY DIRECTION and BY FAMILY — `TOWARD_DISCHARGED`,
    `TOWARD_OUTSTANDING`, `LATERAL`. A delta alone cannot tell a second look that CORRECTED the first
    from one PRESSURED into agreeing with the carried-forward list: both show `outstanding` falling.
    Reversals all running one way is printed as the pressure reading. See `flip_report`;
  * convergence on iteration 3 is printed as distinct from convergence on iteration 1, because exit 0
    says the same thing about both and they are not equally trustworthy.

BATCHING THE VERIFIER CALL — the large-doc cliff, and why raising the cap was rejected
----------------------------------------------------------------------------------------
MEASURED (PHASES.md cap 5b, Alteryx `LoadDim.yxmd`): one verifier call answered every ELEMENT
obligation inside its output-token budget and then exhausted that budget trying to APPEND LINK,
RESIDUE and IR_UNMATCHED into the SAME re-emitted response — ELEMENT 100%, everything after it 0%,
root cause `CLAUDE_CODE_MAX_OUTPUT_TOKENS=16384` plus single-shot re-emission of a cumulative verdict.
Raising the cap was measured and rejected: on the same call shape it trades one failure (truncation)
for another (stall), not for a call that fits — it moves the cliff, it does not remove it.

`batched-run` removes the APPEND instead. `plan_batches` splits the raised set at FAMILY boundaries —
ELEMENT, then LINK, then RESIDUE, then IR_UNMATCHED, the exact order the cliff failed at — optionally
sub-chunking a family that is itself too large with `--batch-size`. Each batch gets its own isolated
verifier call over a view whose `obligations.json` holds ONLY that batch (built the same way
`isolated_model_call` always builds a view; only the obligation set handed to it changes) and writes
its own bounded fragment, `verdict.batch<N>.json` — never a cumulative re-emit, so there is nothing
left for the append to happen to.

THE MERGE RULE (see `merge_batch_fragments`): every successful batch's `claims` are concatenated,
untouched, into one verdict — a claim answered inside a batch is not re-interpreted by having been
batched. A batch with no usable fragment (timeout, no verdict, bad JSON) contributes NOTHING: never a
manufactured claim standing in for a missing answer. Its obligations fall through to `score()`'s own
unanswered path and are scored OUTSTANDING, exactly as an obligation a single verifier stayed silent
on already is — batching does not invent a new way to pass. What it adds is `gateA-batch-merge.json`,
which says which OUTSTANDING obligations are that way because a model judged them unresolved and which
are that way because the call that owned them never answered at all — a distinction the pre-batching
ledger could not draw.

THE DENOMINATOR IS CHECKED BEFORE ANY CALL: `plan_batches_from_bundle` asserts the concatenation of
every batch's obligation ids equals the packed raised set, in order, exactly once each, and raises
(exit 1, a planner defect, never a verdict about the document) if it does not. `score()` then still
recomputes the FULL raised set from the document independently, same as a single-shot run — batching
changes what one verifier call SEES, never what the scorer counts against.

`batched-run` is single-pass (`score()` runs once). Composing it with the iterate-to-convergence loop
in `run` — batching inside every iteration rather than instead of iterating — is the natural next step
and is NOT implemented here; each of `run`'s three convergence guarantees (stable denominator,
directional flip report, distinct CONVERGED-on-iteration-N) would need to hold across a batched pass
too, and that is worth its own measurement rather than an assumption carried over for free.

EXIT CODES — the driver's vocabulary, deliberately not widened
--------------------------------------------------------------
  0  every raised obligation discharged
  3  OBLIGATIONS OUTSTANDING — the unresolved list is handed over in the ledger and the sidecar.
     Degradation, not failure: output exists and provably does not account for the input.
  1  the gate could not run (unreadable input, no counting rule, no link rule, malformed verdict).
     NOT an obligation verdict. Disambiguated on stdout exactly as the loss ledger and coverage_gate
     are: a real verdict always contains a " ledger        :" line. Two loop-specific cases print
     their own marker so the driver can tell them from a plain verdict, because by then a ledger line
     has already been printed: DENOMINATOR DRIFT (exit 1, the whole run is UNMEASURED) and LOOP
     ABORTED (the last complete iteration's ledger stands; convergence is UNMEASURED).
  2  usage
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import coverage_gate  # noqa: E402  the deterministic half. Imported, never reimplemented.

W = 96

# ---------------------------------------------------------------------------------------------
# THE RESIDUE RULES. Which tags/records the element rule and the link rule account for, per
# platform, stated as data and PRINTED in the bundle. Everything else in the document is residue and
# is put to the verifier as a materiality question. A platform with no entry here gets exit 1 rather
# than an invented denominator -- an invented denominator is how the ledger this gate replaces came
# to report lost=0 on a tree with no output in it.
# ---------------------------------------------------------------------------------------------

RESIDUE_RULES = {
    "SqlServerIntegrationServices": {
        "element_tags": ["component"],
        "link_tags": ["path"],
        "rule": "dtsx.residue.v1",
    },
    "InformaticaPowerCenter": {
        "element_tags": ["INSTANCE"],
        "link_tags": ["CONNECTOR"],
        "rule": "infa.residue.v1",
    },
    "PentahoDataIntegration": {
        "element_tags": ["step"],
        "link_tags": ["hop"],
        "rule": "ktr.residue.v1",
    },
    "IbmInfoSphereDataStage": {
        "rule": "dsx.residue.v1",
    },
    "alteryx": {
        "element_tags": ["Node"],
        "link_tags": ["Connection"],
        "rule": "yxmd.residue.v1",
    },
}

# LINK RULES, one per platform, each read off the table's own edge_policy rather than invented here.
LINK_RULES = {
    "SqlServerIntegrationServices": (
        "dtsx.path.v1",
        "one link per <path> element. id = @refId, label = @name. @startId and @endId name an "
        "OUTPUT and an INPUT, not a component -- `<component refId>.Outputs[<name>]` -- so the "
        "endpoint is the refId prefix before `.Outputs[...]` / `.Inputs[...]`, and an id in any "
        "other shape is left unresolved rather than guessed. Control-flow PrecedenceConstraints are "
        "NOT links under this rule and fall to the residue family instead.",
    ),
    "InformaticaPowerCenter": (
        "infa.connector.distinct.v1",
        "the table declares element_edges_from=COLLAPSE_FIELD_EDGES with "
        "collapse_connectors_by=DISTINCT_FROMINSTANCE_TOINSTANCE, so one link per DISTINCT "
        "(@FROMINSTANCE, @TOINSTANCE) pair over CONNECTOR elements. The field pairs collapsed into "
        "each link are counted and reported.",
    ),
    "PentahoDataIntegration": (
        "ktr.hop.v1",
        "one link per <hop>. from = <from>, to = <to>, and <enabled> is carried through because a "
        "disabled hop is a stated fact about the graph.",
    ),
    "IbmInfoSphereDataStage": (
        "dsx.pinpair.v1",
        "a .dsx has no link object: one logical link is TWO pin records naming each other through "
        "Partner. The table's edge_policy.pin_pairs declares which OLEType classes are the OUTPUT "
        "half, and exactly that half is counted. from = the stage whose OutputPins list contains "
        "this pin's Identifier; to = the stage whose InputPins list contains its Partner. Both "
        "endpoints are STATED by the document, not inferred from the identifier's shape.",
    ),
    "alteryx": (
        "yxmd.connection.v1",
        "one link per <Connection> element. from = Origin/@ToolID, to = Destination/@ToolID. "
        "Origin/@Connection and Destination/@Connection name the port (e.g. Output/Input) and are "
        "carried in the stated text; they are not separate links under this rule.",
    ),

}


# ---------------------------------------------------------------------------------------------
# THE RESIDUE CRITERION — one text, two consumers, and the reason it exists is a measurement.
#
# MEASURED, not suspected. Five independent verifier calls over ONE byte-identical SSIS bundle answered
# `RS:Executable/ConnectionManagers` MATERIAL_AND_ABSENT four times and IMMATERIAL once, which flipped
# the whole gate's exit code between 3 and 0 on the same input. Across the four rounds on disk, 4 of 24
# repeated RESIDUE questions carry more than one verdict word while every ELEMENT / LINK / IR_UNMATCHED
# verdict held.
#
# AND THE DIAGNOSIS IS NOT "the model is inconsistent". Reading the four unstable pairs side by side,
# the two answers cite THE SAME LINES and state THE SAME FACTS; what differs is the rule applied to
# them. Three rules were never written down anywhere:
#
#   1. THE FRAME OF REFERENCE. One verifier judged materiality against what the IR owes; another
#      against the migrated pipeline's end behaviour, and reasoned that because dbt keeps connections
#      in a config layer "outside the model contract", a dropped connection binding "does not change
#      what the model computes" -> IMMATERIAL. Both readings are defensible and nothing chose between
#      them, so the answer was a coin flip.
#   2. PRECEDENCE ON A MIXED CLASS. A residue class holds several things at once (`transformation/info`
#      holds an identity, five log tables and run tuning). Two verifiers agreed the identity IS carried
#      on the IR node and the rest is engine telemetry, then split REPRESENTED_ELSEWHERE vs IMMATERIAL
#      on which half names the answer.
#   3. WHETHER TO DEFER. When the loss a residue class names is one an ELEMENT or LINK obligation
#      already reports, nothing said whether to repeat it or hand it off.
#
# So the fix is a stated criterion, not more context and not a softer word: the previews are not the
# constraint (every one of these verdicts cites document lines the preview does not contain, so the
# verifier was reading the whole document), and an escape hatch cannot help a verifier that is not
# short of evidence.
#
# DISCLOSED, because it is the confound a reader should weigh: this text was written AFTER four rounds
# of verdicts were on disk, and each of its three rules resolves its unstable case toward the answer the
# historical majority gave. The rules are stated as rules and are derived from what this gate is for,
# but "would an independently-written criterion have stabilised them the same way" is not measured.
#
# ONE STRING, TWO CONSUMERS -- `PROMPT.md` and every RS obligation's own `question` field. Two
# hand-typed copies would drift, and a criterion the instructions state and the obligation does not is
# the shape of the staging error `findings/43` recorded.
# ---------------------------------------------------------------------------------------------

RESIDUE_CRITERION = """The element rule and the link rule do not account for this content. Does it \
matter for a faithful migration? Answer these in order and take the FIRST word that fits; the ORDER is \
the criterion, and without it two readings of the same lines give opposite words.

1. NAME THE PART THAT COULD CHANGE BEHAVIOUR. A residue class usually holds several things at once — \
an identity, some editor state, some engine tuning. Say in one clause which part of it could change \
what the migrated pipeline does, and answer the rest of this list about THAT part. If no part of it \
could, that is the answer: IMMATERIAL, with the reason.
2. DOES A FIELD OF ir.json CARRY THAT PART? Then REPRESENTED_ELSEWHERE, naming the field. This ranks \
ABOVE IMMATERIAL: a class whose behavioural part the IR does carry is represented, not irrelevant.
3. NOTHING IN THE IR CARRIES IT. Would a migration built from ir.json ALONE read or write different \
data, produce different column contents, or run its steps in a different order or under different \
conditions than this document states? Then MATERIAL_AND_ABSENT, with a citation and what_breaks. THE \
FRAME IS ir.json ALONE, and it is stated because it is where two readings diverge: that the target \
platform has a configuration layer in which a human could restore the fact LATER does not make the \
fact immaterial. It makes it absent and repairable, and naming it is this gate's job.
4. Nothing carries it and no such difference follows: IMMATERIAL, with the reason.
5. YOU KNOW IT IS UNREPRESENTED AND CANNOT DECIDE 3 FROM THIS DIRECTORY: UNVERIFIABLE, naming in \
`reason` the evidence that would decide it. This is scored OUTSTANDING and reported as UNDECIDED \
rather than as a loss. It is the honest answer when the bundle cannot settle the question, and it is \
not a free pass — it leaves the obligation on the handover list.

ONE OBLIGATION, ONE ANSWER, and no deferring. If the loss you find is one another obligation in this \
set also reports, say so in `reason` and still answer THIS obligation on its own content. The ledger \
counts obligations, not distinct defects."""


def _local(tag):
    """Local name of a tag, from EITHER spelling.

    ElementTree hands back `{namespace}tag`; the RAW TEXT of the same document spells it `DTS:tag`.
    The first version handled only the first form, so every line-number hint for an SSIS `.dtsx` came
    back 0 -- a whole platform's residue obligations arrived with no locus while the code that
    computed them looked correct. Both separators, one function.
    """
    return tag.split("}")[-1].split(":")[-1]


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _wrap(s, n):
    return coverage_gate._wrap(s, n)


# THE SIDECAR IS NOW A MUTABLE INPUT, AND THAT REOPENS THE STALENESS HOLE `table_is_current` CLOSED.
#
# `table_is_current` and `ir_is_current_with_table` stamp the PLATFORM TABLE, because when they were
# written the table was the only input that moved. It is not any more: `<doc>.ai.json` used to be
# hand-authored and effectively frozen, and it is now produced by a model call, so it changes between
# runs. MEASURED, during this run: the SSIS and DataStage sidecars were rewritten at 15:15:20 UTC by a
# concurrent producer, four minutes after five Gate A bundles were packed at 15:00 -- and the SSIS one
# takes that tree's blocking-EWI count from 1 to 0 while the DataStage one turns `CTransformerStage`
# into a real `ExpressionTransformation`. A bundle packed before that describes a pipeline that no
# longer exists, in exactly the direction this project has already been bitten by: it manufactures a
# false alarm.
#
# Same shape as the table check and the same limitation, stated rather than dressed up: mtime is the
# only ordering evidence these files carry and copying one resets it, so this DETECTS the clear-cut
# case and can miss staleness. When it fires it is right.
def sidecar_freshness(doc_path, against_path, against_label, prev=None):
    """Stamp every `<doc>.ai*.json` beside `doc_path` and order them against `against_path`.

    Returns a dict safe to embed in a manifest. `sidecars` is [] when the document has none, and
    `<against_label>_is_current_with_sidecars` is then None -- never silently True, for the same
    reason `table_changed_since_previous_pack` is None on a first pack.
    """
    import glob
    doc_path = os.path.abspath(doc_path)
    found = sorted(glob.glob(doc_path + ".ai*.json"))
    against_mtime = (os.path.getmtime(against_path) if os.path.exists(against_path) else None)
    if against_mtime is None and os.path.isdir(against_path or ""):
        against_mtime = None
    rows, stale = [], []
    for p in found:
        m = os.path.getmtime(p)
        current = None if against_mtime is None else against_mtime >= m
        rows.append({"file": os.path.basename(p), "sha256": _sha(p)[:16],
                     "mtime_utc": datetime.fromtimestamp(m, timezone.utc).isoformat(timespec="seconds"),
                     against_label + "_is_current_with_it": current})
        if current is False:
            stale.append(os.path.basename(p))
    prev_by_name = {r["file"]: r.get("sha256") for r in (prev or [])}
    moved = [r["file"] for r in rows
             if r["file"] in prev_by_name and prev_by_name[r["file"]] != r["sha256"]]
    return {
        "sidecars": rows,
        "stale_against_" + against_label: stale,
        against_label + "_is_current_with_sidecars": (None if not rows or against_mtime is None
                                                      else not stale),
        "sidecars_changed_since_previous_pack": (None if not prev_by_name else sorted(moved)),
        "_how": ("Every `<doc>.ai*.json` beside the source document is hashed and its mtime compared "
                 "against the %s. Model-authored sidecars decide element kinds and lowered SQL, so a "
                 "%s older than one describes a pipeline the current sidecar would not produce. "
                 "The direction is the same as the table check: a stale bundle manufactures a FALSE "
                 "ALARM rather than hiding a defect. LIMITATION: mtime is the only ordering evidence "
                 "these files carry and copying one resets it, so this detects the clear-cut case and "
                 "can miss staleness; when it fires it is right." % (against_label, against_label)),
    }


class GateAError(Exception):
    """Raised for every could-not-run condition. Always exit 1, never an obligation verdict."""


# ---------------------------------------------------------------------------------------------
# READING THE DOCUMENT. Two front ends, matching the two document models the platform tables
# declare: an XML tree and a .dsx BEGIN/END record stream. Both produce LINE NUMBERS, because a line
# number is the citation vocabulary the scorer verifies against and a claim that cannot be located in
# the file cannot be checked.
# ---------------------------------------------------------------------------------------------

def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


class XmlDoc:
    """An XML document with a parent map and a best-effort line number per element.

    ElementTree exposes `sourceline` only from lxml, which is not a dependency here, so line numbers
    come from a single forward scan that pairs each `<tag` occurrence with the elements of that tag
    in document order. That is exact for well-formed documents that do not put two same-named tags on
    one line, and it is announced as best-effort rather than asserted -- the SCORER never trusts it:
    it re-reads the line the VERIFIER cites, not the line this computed.
    """

    def __init__(self, path):
        self.path = path
        self.lines = read_lines(path)
        try:
            self.tree = ET.parse(path)
        except Exception as ex:
            raise GateAError("source document is not readable as XML: %s: %s"
                             % (type(ex).__name__, ex))
        self.root = self.tree.getroot()
        self.parent = {}
        for p in self.root.iter():
            for c in list(p):
                self.parent[id(c)] = p
        self.order = list(self.root.iter())
        self.lineno = {}
        pending = {}
        for i, ln in enumerate(self.lines, start=1):
            for m in re.finditer(r"<([A-Za-z_][\w.:-]*)", ln):
                pending.setdefault(_local(m.group(1)), []).append(i)
        seen = {}
        for e in self.order:
            t = _local(e.tag)
            k = seen.get(t, 0)
            seen[t] = k + 1
            got = pending.get(t) or []
            self.lineno[id(e)] = got[k] if k < len(got) else 0

    def path_of(self, e):
        parts = []
        cur = e
        while cur is not None:
            parts.append(_local(cur.tag))
            cur = self.parent.get(id(cur))
        return "/".join(reversed(parts))

    def attrs(self, e):
        return {_local(k): v for k, v in e.attrib.items()}

    def text_preview(self, e, n=240):
        try:
            raw = ET.tostring(e, encoding="unicode")
        except Exception:
            raw = ""
        raw = re.sub(r"\s+", " ", raw).strip()
        return raw if len(raw) <= n else raw[:n] + " …[truncated]"


class DsxBlock:
    __slots__ = ("kind", "props", "start", "end", "parent", "index", "children")

    def __init__(self, kind, start, parent, index):
        self.kind = kind
        self.props = {}
        self.start = start
        self.end = start
        self.parent = parent
        self.index = index
        self.children = []


class DsxDoc:
    """Independent BEGIN/END block scanner over the .dsx TEXT, with parent links and line numbers.

    Deliberately does NOT go through the framework's docmodel/dsxdoc. Those are the projection the
    identification sweep queries; borrowing them would reintroduce the coupling this gate exists to
    break. coverage_gate.count_datastage takes the same decision for the same reason and this scanner
    is its parent-aware sibling -- it has to be, because a link's endpoints are stated on the STAGE
    records (OutputPins / InputPins) and a flat scan cannot reach them.
    """

    PROP = coverage_gate.DSX_PROP
    BEGIN = coverage_gate.DSX_BEGIN
    END = coverage_gate.DSX_END
    HEREDOC = coverage_gate.DSX_HEREDOC

    def __init__(self, path):
        self.path = path
        self.lines = read_lines(path)
        self.blocks = []
        stack = []
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            lineno = i + 1
            i += 1
            if self.HEREDOC.match(line):
                # A multi-line value whose body is free text and can contain the word BEGIN.
                while i < len(self.lines) and self.lines[i].strip() != "=+=+=+=":
                    i += 1
                i += 1
                continue
            m = self.BEGIN.match(line)
            if m:
                b = DsxBlock(m.group(1), lineno, stack[-1] if stack else None, len(self.blocks))
                self.blocks.append(b)
                if stack:
                    stack[-1].children.append(b)
                stack.append(b)
                continue
            m = self.END.match(line)
            if m:
                if stack and stack[-1].kind == m.group(1):
                    stack[-1].end = lineno
                    stack.pop()
                continue
            m = self.PROP.match(line)
            if m and stack:
                stack[-1].props.setdefault(m.group(1), m.group(2))
        self.records = [b for b in self.blocks if b.kind == "DSRECORD"]

    def preview(self, b, n=6):
        got = self.lines[b.start - 1: min(b.end, b.start - 1 + n)]
        out = " | ".join(x.strip() for x in got if x.strip())
        return out if len(out) <= 300 else out[:300] + " …[truncated]"


def load_doc(platform, path):
    if platform == "IbmInfoSphereDataStage":
        return DsxDoc(path)
    return XmlDoc(path)


# ---------------------------------------------------------------------------------------------
# RAISING THE LINK OBLIGATIONS. One rule per platform, each read off the table's own edge_policy so
# the gate is not carrying a second, private opinion about how a platform declares an edge.
# ---------------------------------------------------------------------------------------------

SSIS_PIN = re.compile(r"^(?P<owner>.*)\.(?:Outputs|Inputs)\[[^\]]*\]$")


def _ssis_owner(pin_id):
    """`Package\\DFT\\OLE_SRC CUSTOMER.Outputs[OLE DB Source Output]` -> the component refId.

    A MEASURED DEFECT IN THIS GATE, fixed before a verifier ever saw the question. The first version
    took startId/endId as component ids, which they are not: a path names an OUTPUT and an INPUT, and
    the component refId is the prefix. So all three SSIS links came out unmatched and all three of the
    IR's CORRECT edges were raised as possible fabrications -- a gate handing a verifier three false
    alarms on a document with nothing wrong with its edges. Exactly the failure mode the false-positive
    control exists to catch, caught here by disbelieving a suspiciously bad number instead.

    The suffix stripped is the one the format states (`.Outputs[...]` / `.Inputs[...]`); anything else
    is returned untouched so an unrecognised spelling stays visibly unmatched rather than being
    guessed into a match.
    """
    m = SSIS_PIN.match(pin_id or "")
    return m.group("owner") if m else pin_id


def links_ssis(doc, table):
    out = []
    for e in doc.order:
        if _local(e.tag) != "path":
            continue
        a = doc.attrs(e)
        src, dst = a.get("startId"), a.get("endId")
        out.append({
            "id": a.get("refId") or a.get("name"),
            "label": a.get("name"),
            "from": _ssis_owner(src), "to": _ssis_owner(dst),
            "line": doc.lineno.get(id(e), 0),
            "stated": ("path[@refId=%r] startId=%r endId=%r; the component refId is the prefix "
                       "before `.Outputs[...]` / `.Inputs[...]`, so this link runs %r -> %r"
                       % (a.get("refId"), src, dst, _ssis_owner(src), _ssis_owner(dst))),
        })
    return out


def links_informatica(doc, table):
    """DISTINCT (FROMINSTANCE, TOINSTANCE) over CONNECTOR, which is what the table declares.

    The field pairs each link collapses are COUNTED and carried, because collapsing 12 connectors to
    3 links is itself a lossy reading and a gate that hides the ratio hides the loss.
    """
    seen = {}
    for e in doc.order:
        if _local(e.tag) != "CONNECTOR":
            continue
        a = doc.attrs(e)
        key = (a.get("FROMINSTANCE"), a.get("TOINSTANCE"))
        rec = seen.setdefault(key, {
            "id": "%s->%s" % key,
            "label": None,
            "from": key[0], "to": key[1],
            "line": doc.lineno.get(id(e), 0),
            "field_pairs": [],
        })
        rec["field_pairs"].append("%s.%s -> %s.%s"
                                  % (a.get("FROMINSTANCE"), a.get("FROMFIELD"),
                                     a.get("TOINSTANCE"), a.get("TOFIELD")))
    out = []
    for rec in seen.values():
        rec["stated"] = ("%d CONNECTOR element(s) collapsed to this one link: %s"
                         % (len(rec["field_pairs"]), "; ".join(rec["field_pairs"])))
        out.append(rec)
    return out


def links_pentaho(doc, table):
    out = []
    for e in doc.order:
        if _local(e.tag) != "hop":
            continue
        f = (e.findtext("from") or "").strip()
        t = (e.findtext("to") or "").strip()
        en = (e.findtext("enabled") or "").strip()
        out.append({
            "id": "%s->%s" % (f, t), "label": None, "from": f, "to": t,
            "line": doc.lineno.get(id(e), 0),
            "stated": "hop from=%r to=%r enabled=%r" % (f, t, en),
            "enabled": en,
        })
    return out


def links_datastage(doc, table):
    """The pin-pair rule, with BOTH endpoints read off stage records rather than inferred.

    A .dsx states no link object. The table's edge_policy.pin_pairs declares which OLEType classes are
    the OUTPUT half; exactly that half is counted, or every link would be emitted twice. The endpoints
    are the stages whose OutputPins / InputPins LISTS name the two pins -- stated facts. Deriving the
    owner from the identifier's shape (V0S1P1 -> V0S1) would be an inference about a naming convention
    the format does not promise, and this gate does not get to guess a denominator.
    """
    pp = ((table.get("edge_policy") or {}).get("pin_pairs") or {})
    outputs = set(pp.get("output_classes") or [])
    marker = pp.get("marker_attr") or "Partner"
    klass = pp.get("class_attr") or "OLEType"
    if not outputs:
        raise GateAError("platform table declares no edge_policy.pin_pairs.output_classes, so there "
                         "is no stated rule for which half of a pin pair is the link. Gate A will "
                         "not pick one.")
    owner_of_out, owner_of_in, by_id = {}, {}, {}
    for r in doc.records:
        ident = r.props.get("Identifier")
        if ident:
            by_id[ident] = r
        for pin in (r.props.get("OutputPins") or "").split():
            owner_of_out[pin] = r
        for pin in (r.props.get("InputPins") or "").split():
            owner_of_in[pin] = r
    out = []
    unclassified = []
    for r in doc.records:
        if marker not in r.props:
            continue
        cls = r.props.get(klass)
        if cls not in outputs:
            if cls not in set(pp.get("input_classes") or []):
                # A closed class list that silently drops an unlisted class is exactly how the
                # zero-edge defect happened. Reported, not dropped.
                unclassified.append("%s [%s=%s] at line %d"
                                    % (r.props.get("Identifier"), klass, cls, r.start))
            continue
        partner = r.props.get(marker)
        src = owner_of_out.get(r.props.get("Identifier"))
        dst = owner_of_in.get(partner)
        out.append({
            "id": r.props.get("Identifier"),
            "label": r.props.get("Name"),
            "partner": partner,
            "from": (src.props.get("Identifier") if src else None),
            "to": (dst.props.get("Identifier") if dst else None),
            "line": r.start,
            "stated": ("output pin %r (%s) Partner=%r; from = the stage declaring OutputPins %r "
                       "(%s); to = the stage declaring InputPins %r (%s)"
                       % (r.props.get("Identifier"), cls, partner,
                          r.props.get("Identifier"),
                          (src.props.get("Name") if src else "NO STAGE DECLARES IT"),
                          partner,
                          (dst.props.get("Name") if dst else "NO STAGE DECLARES IT"))),
        })
    return out, unclassified


def links_alteryx(doc, table):
    """One link per <Connection>, endpoints from Origin/Destination @ToolID."""
    out = []
    for e in doc.order:
        if _local(e.tag) != "Connection":
            continue
        origin = dest = None
        o_port = d_port = None
        for ch in list(e):
            tag = _local(ch.tag)
            a = {_local(k): v for k, v in ch.attrib.items()}
            if tag == "Origin":
                origin = a.get("ToolID")
                o_port = a.get("Connection")
            elif tag == "Destination":
                dest = a.get("ToolID")
                d_port = a.get("Connection")
        out.append({
            "id": "%s->%s" % (origin, dest),
            "label": None,
            "from": origin,
            "to": dest,
            "line": doc.lineno.get(id(e), 0),
            "stated": ("Connection Origin@ToolID=%r Connection=%r -> "
                       "Destination@ToolID=%r Connection=%r"
                       % (origin, o_port, dest, d_port)),
        })
    return out



LINKERS = {
    "SqlServerIntegrationServices": links_ssis,
    "InformaticaPowerCenter": links_informatica,
    "PentahoDataIntegration": links_pentaho,
    "IbmInfoSphereDataStage": links_datastage,
    "alteryx": links_alteryx,
}


# ---------------------------------------------------------------------------------------------
# RAISING THE RESIDUE OBLIGATIONS -- the known-unknown set.
#
# A node is STRUCTURAL when some descendant of it is accounted for by the element or link rule: the
# document root, an SSIS <pipeline>, a Kettle <order>. Recursing through those and stopping at the
# first node that accounts for nothing is what keeps the residue list at the size of a document's
# top-level sections instead of the size of its tag census. Grouped by tag path so 4 connection
# managers are one question rather than four.
# ---------------------------------------------------------------------------------------------

RESIDUE_GROUP_CAP = 60


def residue_xml(doc, platform, element_tags, link_tags):
    accounted = set()
    for e in doc.order:
        if _local(e.tag) in set(element_tags) | set(link_tags):
            for d in e.iter():
                accounted.add(id(d))
    structural = set()
    for e in doc.order:
        if id(e) in accounted:
            continue
        if any(id(d) in accounted for d in e.iter()):
            structural.add(id(e))
    groups = {}
    for e in doc.order:
        if id(e) in accounted or id(e) in structural:
            continue
        p = doc.parent.get(id(e))
        if p is not None and not (id(p) in structural or id(p) in accounted):
            continue                      # not a residue ROOT; its ancestor already carries it
        sig = doc.path_of(e)
        g = groups.setdefault(sig, {"signature": sig, "count": 0, "loci": [], "previews": []})
        g["count"] += 1
        if len(g["loci"]) < 3:
            g["loci"].append(doc.lineno.get(id(e), 0))
            g["previews"].append(doc.text_preview(e))
    return groups, accounted, structural


def residue_dsx(doc, element_ids, links):
    """DSX residue, grouped by (block kind, OLEType). A record is accounted when the element rule
    counted it (it states a StageType) or the link rule counted it (it is the OUTPUT half of a pin
    pair). The INPUT half is residue on purpose: it is the same logical link seen from the other end
    and whether anything is lost by reading only one half is a judgement, not a rule.

    AND THE PAIRING IS NOW STATED IN THE OBLIGATION, which is a MEASURED fix rather than a tidy-up.
    Ten independent verifier calls over two byte-identical bundles were split on these two classes
    every time, and reading the reasons shows why: the record has TWO candidate answers to "which part
    of this could change behaviour" -- the Partner reference that anchors a link endpoint, and its own
    column subrecords. Four calls named the endpoint, one named the columns, and the split follows the
    choice exactly. The endpoint is already the subject of the paired `LK:` obligation, and nothing in
    the residue obligation said so, so each verifier re-derived the relationship from
    `edge_policy.pin_pairs` and scoped the question differently. Naming the paired obligation removes
    the choice without deciding the judgement: whether the columns state anything the output half does
    not is still open both ways.
    """
    pair_of = {}
    for lk in links:
        # `id` is the OUTPUT pin's Identifier and `partner` names the INPUT pin, so the input half's
        # own obligation is found by inverting the link rule rather than by parsing an identifier.
        if lk.get("partner"):
            pair_of[lk["partner"]] = ("LK:%s" % lk["id"], lk.get("label"))
    link_ids = {lk["id"] for lk in links}
    groups = {}
    for b in doc.blocks:
        if b.kind == "DSSUBRECORD":
            continue                      # a property/column subrecord, inside its record's subtree
        ident = b.props.get("Identifier")
        if b.kind == "DSRECORD" and (ident in element_ids or ident in link_ids):
            continue
        if b.kind == "DSJOB":
            continue                      # the container every record hangs off; structural
        sig = "%s[%s=%s]" % (b.kind, "OLEType", b.props.get("OLEType"))
        g = groups.setdefault(sig, {"signature": sig, "count": 0, "loci": [], "previews": [],
                                    "paired": []})
        g["count"] += 1
        if ident in pair_of:
            lk_id, label = pair_of[ident]
            g["paired"].append("%s is the INPUT half of the pin pair whose OUTPUT half is raised as "
                               "%s (label %r)" % (ident, lk_id, label))
        if len(g["loci"]) < 3:
            g["loci"].append(b.start)
            g["previews"].append(doc.preview(b))
    return groups


# ---------------------------------------------------------------------------------------------
# THE RAISED SET. Computed from the document, the table and the IR -- never from the verifier's
# answer, and recomputed on every iteration so the denominator cannot shrink under a loop.
# ---------------------------------------------------------------------------------------------

def strip_commentary(obj, removed):
    """Remove every `_`-prefixed key from the platform table before it enters the bundle.

    NOT a giveaway scrub dressed up as hygiene -- although it is also that. Those keys are the table
    author's prose ABOUT their own rules: the producer's self-report, which is the class of evidence
    Gate B's staging deliberately withheld ("the header is not evidence"). The verifier reasons from
    the DECLARED RULES and from the document. Applied symmetrically to every arm, so the bundle for a
    table with a defect and the bundle for the same table with the defect fixed differ only in rules.
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and k.startswith("_"):
                removed.append(k)
                continue
            out[k] = strip_commentary(v, removed)
        return out
    if isinstance(obj, list):
        return [strip_commentary(v, removed) for v in obj]
    return obj


def find_line_hints(lines, needle, cap=3):
    if not needle:
        return []
    got = []
    for i, ln in enumerate(lines, start=1):
        if needle in ln:
            got.append(i)
            if len(got) >= cap:
                break
    return got


def raise_obligations(table, table_path, doc_path, ir_path, out_root, emit_log, inventory_path):
    platform = table.get("platform")
    if platform not in coverage_gate.COUNTERS:
        raise GateAError("no source-element counting rule for platform %r in coverage_gate.RULES. "
                         "Gate A will not guess a denominator." % platform)
    if platform not in LINK_RULES:
        raise GateAError("no LINK rule for platform %r. Elements without edges is the measured "
                         "blind spot this gate exists to close, so a missing link rule is a "
                         "could-not-run, not a clean sheet." % platform)
    if platform not in RESIDUE_RULES:
        raise GateAError("no residue rule for platform %r." % platform)

    try:
        elements, el_caveats = coverage_gate.COUNTERS[platform](doc_path)
    except Exception as ex:
        raise GateAError("source document unreadable by counting rule %s: %s: %s"
                         % (coverage_gate.RULES[platform][0], type(ex).__name__, ex))
    doc = load_doc(platform, doc_path)
    lines = doc.lines

    link_caveats = []
    lk = LINKERS[platform](doc, table)
    links, unclassified = lk if isinstance(lk, tuple) else (lk, [])
    if unclassified:
        link_caveats.append("UNCLASSIFIED LINK RECORDS under %s -- a class the table's pin_pairs does "
                            "not enumerate: %s. These are NOT counted as links and are NOT residue "
                            "either; they are reported so an unlisted class is loud rather than "
                            "invisible." % (LINK_RULES[platform][0], "; ".join(unclassified)))

    try:
        with open(ir_path, "r", encoding="utf-8") as fh:
            ir = json.load(fh)
    except Exception as ex:
        raise GateAError("IR unreadable: %s: %s" % (type(ex).__name__, ex))
    nodes = ir.get("nodes") or []
    edges = ir.get("edges") or []

    # ---- match, using coverage_gate's OWN match rule, imported ----------------------------------
    index = {}
    for n in nodes:
        for k in coverage_gate.ir_keys(n):
            index.setdefault(k, []).append(n)
    dispatch = table.get("kind_dispatch") or {}

    obligations = []
    el_node = {}
    matched_nodes = set()
    for el in elements:
        node = None
        for cand in (el.eid, el.name):
            if coverage_gate.norm(cand) in index:
                node = index[coverage_gate.norm(cand)][0]
                break
        if node is not None:
            matched_nodes.add(id(node))
        el_node[el.eid] = node
        d = dispatch.get(el.kind) if isinstance(dispatch.get(el.kind), dict) else None
        hints = find_line_hints(lines, el.eid) or find_line_hints(lines, el.name)
        obligations.append({
            "id": "EL:%s" % el.eid,
            "family": "ELEMENT",
            "source_element": el.eid,
            "name": el.name,
            "kind": el.kind,
            "stated_at": el.where,
            "line_hints": hints,
            # THE TABLE'S OWN WORDS ABOUT THIS KIND, verbatim, because the difference between "the
            # table has no entry for this kind" and "the table maps it and the sweep missed it" is
            # the difference between an engine gap and our gap -- and the verifier cannot tell them
            # apart without seeing which one the table states.
            "table_says": ({
                "declared_in_kind_dispatch": True,
                "ir_kind": d.get("ir_kind"), "degrade_to": d.get("degrade_to"),
                "role": d.get("role"), "collapse": d.get("collapse"),
            } if d is not None else {"declared_in_kind_dispatch": False}),
            "ir_match": None if node is None else {
                "node_id": node.get("id"), "node_type": node.get("type"),
                "modelName": node.get("modelName"),
                "element_kind": (node.get("element") or {}).get("$kind"),
                "fields": sorted((node.get("element") or {}).keys()),
            },
            "question": ("Does the IR carry this source element? If yes, which IR field carries it. "
                         "If no, WHY: no slot in the contract, no rule to read it, silently dropped, "
                         "or legitimately absent because the platform table declares a collapse."),
        })

    # ---- links ---------------------------------------------------------------------------------
    def node_id_for(el_key):
        n = el_node.get(el_key)
        if n is not None:
            return n.get("id")
        cand = index.get(coverage_gate.norm(el_key))
        return cand[0].get("id") if cand else None

    el_kind_by_key = {}
    for el in elements:
        for k in (el.eid, el.name):
            if k:
                el_kind_by_key.setdefault(coverage_gate.norm(k), el.kind)

    edge_pairs = {}
    for e in edges:
        edge_pairs.setdefault((e.get("from"), e.get("to")), []).append(e)
    matched_edges = set()
    for lk in links:
        want = (node_id_for(lk.get("from")), node_id_for(lk.get("to")))
        hit = edge_pairs.get(want) if all(want) else None
        if hit:
            matched_edges.add(id(hit[0]))
        # LABEL IS NOT A MATCH KEY, on purpose. On the frozen DataStage fixture the fabricated edge
        # V0S1 -> job carries the RIGHT LABEL and the wrong endpoints. Accepting a label match would
        # have marked that link satisfied and hidden the fabrication in the same breath.
        label_only = [e for e in edges
                      if lk.get("label") and e.get("label") == lk.get("label")
                      and (e.get("from"), e.get("to")) != want]
        obligations.append({
            "id": "LK:%s" % lk.get("id"),
            "family": "LINK",
            "label": lk.get("label"),
            "from": lk.get("from"), "to": lk.get("to"),
            "stated_at": "line %d" % (lk.get("line") or 0),
            "line_hints": [lk.get("line")] if lk.get("line") else [],
            "document_states": lk.get("stated"),
            "expected_ir_edge": {"from": want[0], "to": want[1]},
            # THE ENDPOINT KINDS, because a link can be legitimately absent for the same reason an
            # element can. Informatica's CUSTOMER Source Definition is collapse-declared, so the link
            # CUSTOMER -> SQ_CUSTOMER has no IR edge BY DESIGN. Without the kinds here the scorer
            # downgraded that correct answer to ABSENT_SILENTLY_DROPPED -- the gate manufacturing a
            # loss out of a design decision, which is the exact confusion it exists to prevent.
            "from_kind": el_kind_by_key.get(coverage_gate.norm(lk.get("from"))),
            "to_kind": el_kind_by_key.get(coverage_gate.norm(lk.get("to"))),
            "ir_match": ({"from": hit[0].get("from"), "to": hit[0].get("to"),
                          "label": hit[0].get("label")} if hit else None),
            "same_label_different_endpoints": [
                {"from": e.get("from"), "to": e.get("to"), "label": e.get("label")}
                for e in label_only],
            "question": ("Does the IR carry this link as an edge? Matching is on ENDPOINTS, never on "
                         "label. If an edge carries this link's label with different endpoints, say "
                         "what that edge asserts and whether the document states it."),
        })

    # ---- residue -------------------------------------------------------------------------------
    rr = RESIDUE_RULES[platform]
    if platform == "IbmInfoSphereDataStage":
        rgroups = residue_dsx(doc, {el.eid for el in elements}, links)
    else:
        rgroups, _, _ = residue_xml(doc, platform, rr["element_tags"], rr["link_tags"])
    truncated = False
    items = sorted(rgroups.values(), key=lambda g: (-g["count"], g["signature"]))
    if len(items) > RESIDUE_GROUP_CAP:
        truncated = True
        items = items[:RESIDUE_GROUP_CAP]
    for g in items:
        # WHERE THE CRITERION WAS NOT ENOUGH, and the measurement said so. On both DataStage pin-half
        # classes the criterion left step 1 -- "name the part that could change behaviour" -- with two
        # candidate answers, because the record holds a link endpoint AND its own columns, and the
        # endpoint is the paired `LK:` obligation's question by construction of the link rule. Five
        # calls split 4/1 on which part to judge. This SCOPES step 1 for exactly that case and decides
        # nothing else: it names the obligation that owns the endpoint and points step 1 at what is
        # left. It is not the criterion's no-deferral rule being relaxed -- that rule forbids
        # DISCHARGING because another obligation reports the same loss, and this says which part of the
        # record is this obligation's subject in the first place.
        paired = g.get("paired") or []
        question = RESIDUE_CRITERION
        extra = {}
        if paired:
            # PRESENT ONLY WHEN IT SAYS SOMETHING, and that is a measurement-hygiene decision rather
            # than a style one. An always-present `paired_obligations: []` changes the bytes of every
            # residue obligation on every platform, which would make the before/after replication of a
            # platform whose QUESTION did not change look like a changed question. The pairing is
            # already visible where it matters -- in the question text -- so the field is added only
            # where there is a pairing to state.
            extra["paired_obligations"] = paired
            question += ("\n\nSCOPE OF THIS OBLIGATION, because this class is one half of a two-part "
                         "fact: " + "; ".join(paired) + ". The link's endpoints and label are that "
                         "obligation's question and answering them here would answer one fact twice, "
                         "so under step 1 the part to judge is what THIS record states that the "
                         "output half does not — its own column subrecords in particular. Say "
                         "whether those state anything the paired output pin does not, and answer "
                         "about that. If they state nothing extra, that is step 1's short answer.")
        obligations.append(dict({
            "id": "RS:%s" % g["signature"],
            "family": "RESIDUE",
            "signature": g["signature"],
            "occurrences": g["count"],
            "line_hints": g["loci"],
            "previews": g["previews"],
            "source": "GATE_A_DOCUMENT_CENSUS",
            # THE CRITERION, not a restatement of the question. What was here before was "does it
            # matter for a faithful migration?" plus a list of three words -- a judgement with no
            # stated rule, which five replications of one bundle measured as a coin flip on the class
            # where two rules both fit. RESIDUE_CRITERION states the rule and the order; `question`
            # is it verbatim, plus the scope note above where this class is half of a two-part fact.
            "question": question,
        }, **extra))

    inventory_note = None
    if inventory_path:
        # An external identification inventory classifies every record element / excluded / Unknown
        # Object. When it exists, its Unknown Objects are raised as residue obligations of their own,
        # so the verifier reasons over KNOWN unknowns instead of having to find them; when it does
        # not, the census above stands in for it. Consumed, never required.
        try:
            with open(inventory_path, "r", encoding="utf-8") as fh:
                inv = json.load(fh)
        except Exception as ex:
            raise GateAError("--inventory given but unreadable: %s: %s" % (type(ex).__name__, ex))
        unknowns = [r for r in (inv.get("records") or inv.get("entries") or [])
                    if str(r.get("classification") or r.get("class") or "").upper()
                    in ("UNKNOWN_OBJECT", "UNKNOWN OBJECT", "UNKNOWN")]
        for u in unknowns:
            sig = str(u.get("signature") or u.get("id") or u.get("where"))
            obligations.append({
                "id": "RS:INVENTORY:%s" % sig,
                "family": "RESIDUE",
                "signature": sig,
                "occurrences": int(u.get("count") or 1),
                "line_hints": u.get("line_hints") or ([u["line"]] if u.get("line") else []),
                "previews": [u.get("preview")] if u.get("preview") else [],
                "source": "IDENTIFICATION_INVENTORY",
                # THE SAME CRITERION. An inventory-sourced residue obligation is the same KIND of
                # question as a census-sourced one, and it used to be asked with a one-line "does it
                # matter?" -- less determinate than the census version it sits beside. Two texts for
                # one question is how a criterion silently applies to half a family.
                "question": ("The identification inventory classified this as an Unknown Object. "
                             + RESIDUE_CRITERION),
            })
        inventory_note = ("consumed %s: %d record(s), %d classified Unknown Object"
                          % (os.path.basename(inventory_path),
                             len(inv.get("records") or inv.get("entries") or []), len(unknowns)))

    # ---- the IR side: anything the document did not account for ---------------------------------
    for n in nodes:
        if id(n) in matched_nodes:
            continue
        obligations.append({
            "id": "IX:NODE:%s" % n.get("id"),
            "family": "IR_UNMATCHED",
            "node": {"id": n.get("id"), "type": n.get("type"), "modelName": n.get("modelName"),
                     "element_kind": (n.get("element") or {}).get("$kind"),
                     "unsupported": (n.get("element") or {}).get("_unsupported"),
                     "name": (n.get("element") or {}).get("Name")},
            "question": ("No source element under the counting rule matched this IR node. Is it "
                         "justified by a table rule (a container the table's role_to_node_type "
                         "declares), or does it assert something the document does not state?"),
        })
    for e in edges:
        if id(e) in matched_edges:
            continue
        obligations.append({
            "id": "IX:EDGE:%s->%s" % (e.get("from"), e.get("to")),
            "family": "IR_UNMATCHED",
            "edge": {"from": e.get("from"), "to": e.get("to"), "label": e.get("label")},
            "question": ("No link the document declares matched this IR edge on endpoints. Does the "
                         "document state this connection? If it does not, the IR is asserting a "
                         "dataflow that does not exist."),
        })

    return {
        "platform": platform,
        "counting_rule": coverage_gate.RULES[platform][0],
        "counting_rule_text": coverage_gate.RULES[platform][1],
        "link_rule": LINK_RULES[platform][0],
        "link_rule_text": LINK_RULES[platform][1],
        "residue_rule": rr["rule"],
        "caveats": list(el_caveats) + link_caveats
        + (["RESIDUE GROUPS TRUNCATED at %d; the document declares more classes than that and the "
            "remainder is UNASKED. A truncation is announced rather than silently applied."
            % RESIDUE_GROUP_CAP] if truncated else []),
        "inventory": inventory_note,
        "counts": {
            "ELEMENT": sum(1 for o in obligations if o["family"] == "ELEMENT"),
            "LINK": sum(1 for o in obligations if o["family"] == "LINK"),
            "RESIDUE": sum(1 for o in obligations if o["family"] == "RESIDUE"),
            "IR_UNMATCHED": sum(1 for o in obligations if o["family"] == "IR_UNMATCHED"),
        },
        "obligations": obligations,
    }


# ---------------------------------------------------------------------------------------------
# PACK — the blind evidence bundle.
#
# findings/43 records a staging error that made six verifiers answer a question ADJACENT to the one
# intended: only `models/` was staged, so `dbt_project.yml` was invisible and one finding was false.
# The counter-measure is not care, it is a manifest: every file in the bundle with its size and
# sha256, plus an explicit list of what was withheld and why. A staging mistake then shows up in the
# record instead of being reconstructed from memory afterwards.
# ---------------------------------------------------------------------------------------------

WITHHELD = [
    ("findings/, CONFIDENCE.yml, DESIGN.md, tickets/",
     "they contain the answers, and several name this exact defect"),
    ("the driver log and any stage-4 verdict",
     "a previous gate's conclusion is not evidence about the document"),
    ("*.ai.json producer sidecar",
     "the producer's own account of what it could not read -- the self-report Gate B withheld for "
     "the same reason: a model's claim about itself is not evidence"),
    ("the platform table's _-prefixed commentary keys",
     "the table author's prose about their own rules, same class of self-report"),
    # ADDED WHEN THE VERIFIER BECAME A PROCESS INSTEAD OF AN INSTRUCTED SUB-AGENT.
    ("MANIFEST.json — it is staged for SCORING and never handed to the verifier",
     "it carries `inputs.table`, `inputs.document`, `inputs.ir` and `output_root` as ABSOLUTE PATHS. "
     "Under instruction-only isolation those were private by convention; handed to a process with a "
     "Read tool they are a map to findings/, which holds the answers. The verifier's view is built "
     "from the manifest's own produced list MINUS this file"),
    ("the harness's own configuration: CLAUDE.md files, auto-memory, skills, plugins, hooks, MCP "
     "servers and custom agents",
     "the model call runs with those disabled. This is not hygiene: the project's auto-memory records "
     "'a packed blind bundle can predate its own platform table' -- one of the findings a Gate A "
     "verifier is being asked to reach on its own -- so an inherited memory file is an answer key"),
]

# NOT withheld -- REPLACED, and the distinction matters because a manifest that claims to withhold a
# field still present in the bundle undermines every other claim it makes. MEASURED: the withheld list
# said `table_version` was withheld while platform_table.json line 3 plainly carried one.
REPLACED = [
    ("the platform table's table_version string -> a content hash",
     "the real string names the arm in a paired control and would settle the experiment by metadata. "
     "It is REPLACED rather than removed, because a table with no version at all is a different "
     "artifact from the one the pipeline reads, and the field is still present in the bundle"),
]

PROMPT = """# Gate A — does the IR carry everything this source document needs?

You are a verification agent. Everything you may rely on is in THIS DIRECTORY. Do not open any file
outside it, do not search the wider repository, and do not consult a previous conclusion about this
document — there is none in here on purpose.

## What you are given

| file | what it is |
|---|---|
| `source_document.*` | the source ETL document, verbatim |
| `source_document.lines.txt` | the same bytes, one `NNNNN: ` line number per line. THIS is the citation vocabulary |
| `platform_table.json` | the platform table's declared RULES: levels, `kind_dispatch`, `edge_policy`, `no_slot_facts`, `residue` |
| `ir.json` | the intermediate representation the pipeline produced from that document |
| `coverage_gate.report.txt` | the deterministic half's report — source-element to emitted-model coverage, with its exit code |
| `obligations.json` | the obligations raised FROM THE DOCUMENT. Your job is to answer every one |
| `SOURCE_FORMAT_REFERENCE.md` | format facts, each marked [PRIMARY] / [COMMON] / [UNCONFIRMED] |

## The question, per obligation

**ELEMENT** — does the IR carry this source element? If yes, name the IR field that carries it. If no,
say **why**: no slot in the contract, no rule read it, silently dropped, or legitimately absent
because the table declares a `collapse` for its kind.

**LINK** — does the IR carry this link as an edge? Endpoints, not label. An edge with the right label
and the wrong endpoints asserts a dataflow the document may not state; say so.

**RESIDUE** — the element and link rules do not account for this content. `obligations.json` states the
criterion and the ORDER to apply it in, per obligation, and it is repeated here so the instructions and
the question cannot disagree:

@RESIDUE_CRITERION@

**IR_UNMATCHED** — the IR states this node/edge and no document obligation matched it. Is it justified
by a table rule, or is the IR asserting something the document does not say?

### Two verdicts for "carried, but not faithfully" — use them rather than prose

An earlier verifier found an element whose IR node existed but whose payload did not match the document,
answered `PRESENT` because that was literally true, and left the finding in its `reason` — where a scorer
counting verdict words reads the bundle as clean. So:

- **`PRESENT_MISREPRESENTED`** — the IR carries it and a field's content does **not** correspond to what
  the document states. Needs `ir_field`, a citation of what the document says, and `what_breaks`. This is
  scored as OUTSTANDING; it is a real fidelity loss and it must not hide behind `PRESENT`.
- **`PRESENT_MODEL_SUPPLIED`** — the IR carries it, and the payload plainly did not come from the
  document: an expression in the target's dialect where the document states another language, a kind the
  document does not name. This **discharges** the obligation — a model supplying a lowered expression for
  a dialect no engine translator handles is the intended fallback, not a defect — but it is reported
  separately, because content read from the document and content authored by a model are different
  fidelity claims and this is the only place that says which one you are looking at.

If what you found is neither — the IR is faithful — answer `PRESENT` and move on. Do not reach for a
qualifier to look thorough.

## The answer format — write exactly this JSON to `verdict.json` in this directory

```json
{
  "verifier": "a short id for yourself",
  "claims": [
    {
      "obligation_id": "EL:V0S2",
      "verdict": "ABSENT_SILENTLY_DROPPED",
      "basis": "DOCUMENT",
      "doc_locus": 130,
      "doc_quote": "StageType \\"CTransformerStage\\"",
      "ir_field": null,
      "reason": "one or two sentences, concrete",
      "what_breaks": "only for absences and MATERIAL_AND_ABSENT: what the migration gets wrong"
    }
  ],
  "notes": ["free prose, never scored"]
}
```

Vocabulary, and nothing outside it:

- ELEMENT / LINK: `PRESENT`, `PRESENT_MISREPRESENTED`, `PRESENT_MODEL_SUPPLIED`,
  `ABSENT_BY_TABLE_RULE`, `ABSENT_NO_SLOT`, `ABSENT_NO_RULE_TO_READ_IT`,
  `ABSENT_SILENTLY_DROPPED`, `UNVERIFIABLE`
- RESIDUE: `IMMATERIAL`, `REPRESENTED_ELSEWHERE`, `MATERIAL_AND_ABSENT`, `UNVERIFIABLE`
- IR_UNMATCHED: `JUSTIFIED_BY_TABLE`, `FABRICATED`, `UNVERIFIABLE`
- `basis`: `DOCUMENT`, `TABLE`, `IR`, `COVERAGE_GATE`, or `PRIOR`

## How you will be scored, so there are no surprises

1. **Every obligation in `obligations.json` must appear in `claims`.** An unanswered obligation is
   scored OUTSTANDING. Silence cannot pass.
2. **Citations are re-read.** `doc_locus` is a line number in `source_document.lines.txt` and
   `doc_quote` must be a substring of that line (leading/trailing whitespace ignored). If it is not,
   the claim is QUARANTINED: it cannot discharge an obligation and cannot raise a finding. Quote a
   short exact fragment, not a paraphrase.
3. **`basis: PRIOR` is quarantined by construction.** If you know something about this file format
   that the bundle does not state, you may say it — declare `PRIOR` and it will be printed as an
   unsourced remark rather than counted. This is deliberate: a verifier that is right from memory
   cannot be trusted on the next document.
4. **`ABSENT_BY_TABLE_RULE` is checked against the table.** If `kind_dispatch` does not declare a
   `collapse` for that kind, your claim is downgraded to `ABSENT_SILENTLY_DROPPED` and the downgrade
   is printed. Do not use it to explain an absence away.
5. **`PRESENT` requires an `ir_field`.** "It is in there somewhere" is not an answer to *which field
   carries it*, and the field name is checked against `ir.json`.
6. **`UNVERIFIABLE` on a RESIDUE obligation requires a `reason` naming what would decide it.** It is
   scored OUTSTANDING and printed under UNDECIDED, separately from losses, and counted on the ledger
   line — so it is neither a pass nor a reported defect. `UNVERIFIABLE` with nothing said about what
   evidence is missing is QUARANTINED.
7. There is **no score**. The verdict is obligations discharged versus outstanding. Reporting nothing
   does not make it pass, and reporting everything as broken does not make it thorough — a false
   alarm on correct output teaches a reviewer to ignore the gate.

## When two explanations fit, name both

A previous verifier reported three facts the platform table declares as never raised by any obligation.
A live run raises exactly those three: **its bundle predated them.** The finding was true of the bundle
and false of the pipeline, and the verifier saw the trap afterwards — *"from inside the bundle those two
hypotheses are indistinguishable ... the hard constraint forbids the one check that would separate them.
I stated it as a live gap; the correct phrasing was 'either the obligation set does not raise these or
this bundle predates them, and I cannot tell which from here.'"*

So: **when two hypotheses fit the evidence in the bundle and nothing in the bundle can separate them,
say so and name both.** Do not pick the more alarming one. This is a reporting standard, not a courtesy —
it is the difference between a finding and a false alarm, and a gate that raises false alarms gets ignored.

`obligations.json` carries a `bundle_freshness` block for exactly this case. If
`ir_is_current_with_table` is **false**, the IR in this bundle was produced before the platform table's
last change, so a table fact nothing raises may simply postdate the IR. Read it before you call anything
a gap.

Read the document before you read anything else. The IR and the coverage report are the *claims* about
it; the document is the only thing in here that is evidence.
"""

# THE ONE PLACE THE CRITERION IS INTERPOLATED, and the reason it is a marker substitution rather than a
# `%s` or an f-string: PROMPT holds a JSON example full of braces and a `%` would have to be escaped, so
# the cheap formatting is the one that silently corrupts the answer schema. A missing marker is a hard
# failure at import rather than a bundle whose instructions quietly lost the criterion.
if "@RESIDUE_CRITERION@" not in PROMPT:
    raise AssertionError("PROMPT lost its @RESIDUE_CRITERION@ marker: the instructions and the "
                         "obligation would then state different criteria, which is the staging defect "
                         "findings/43 recorded in another form.")
PROMPT = PROMPT.replace("@RESIDUE_CRITERION@", RESIDUE_CRITERION)

FORMAT_REFERENCE = """# Source-format reference

Neutral reference material about the FILE FORMATS. It says nothing about any particular document and
identifies no defect. Items marked **[PRIMARY]** were confirmed against a vendor artifact or a real
export in this project; **[COMMON]** is widely-stated behaviour not confirmed here; **[UNCONFIRMED]**
means exactly that — if your verdict rests on one, say so.

## SSIS `.dtsx`

- **[PRIMARY]** Data-flow components are `<component>` elements carrying `componentClassID`, inside
  `<pipeline>`, inside a data-flow task's `<ObjectData>`.
- **[PRIMARY]** Data-flow edges are `<path>` elements with `startId` / `endId` pointing at component
  output/input `refId`s.
- **[PRIMARY]** Control flow is `<DTS:Executable>` elements; ordering between them is
  `<DTS:PrecedenceConstraint>`. These are a DIFFERENT level from data-flow components.
- **[COMMON]** `<DTS:ConnectionManager>` holds the connection string a source or destination resolves
  through; the component itself names the manager, not the server.

## Informatica PowerCenter XML

- **[PRIMARY]** A `MAPPING` declares `INSTANCE` elements (the occurrences) and `CONNECTOR` elements
  (field-level links, `FROMINSTANCE/FROMFIELD` → `TOINSTANCE/TOFIELD`).
- **[PRIMARY]** `SOURCE`, `TARGET` and `TRANSFORMATION` are DEFINITIONS, declared outside the mapping
  and referenced by instances. A definition and its instance are two different objects.
- **[COMMON]** There is no element-level edge object: element edges only exist as a DISTINCT over
  connector field pairs.

## Pentaho `.ktr`

- **[PRIMARY]** `<step>` elements are the units of work; `<hop>` elements inside `<order>` are the
  edges, and a hop names no columns.
- **[COMMON]** `<connection>` declares the database; a `TableInput` step names the connection, not the
  server.
- **[COMMON]** The `<info>` block carries transformation-level settings, including logging tables and
  parameters.

## IBM DataStage `.dsx`

- **[PRIMARY]** A `.dsx` is a flat `BEGIN`/`END` keyword stream. `DSRECORD` blocks are objects;
  `DSSUBRECORD` blocks are properties and columns. Grouping of subrecords is POSITIONAL: a section
  takes the name of the scalar key preceding the first subrecord, so a marker-less record's holder is
  named after whatever key came last.
- **[PRIMARY]** A record's class is `OLEType`. A stage record additionally states `StageType`.
- **[PRIMARY]** There is no link object. One logical link is TWO pin records naming each other through
  `Partner`, and each stage lists its pins in `OutputPins` / `InputPins`.
- **[PRIMARY]** `OLEType` spelling varies between exports: `CCustomInput`/`CCustomOutput`,
  `CustomInput`/`CustomOutput`, `CTrxInput`/`CTrxOutput`, `CJSActivityInput`/`CJSActivityOutput` all
  occur for pins.
- **[COMMON]** `#Param#` and `#Set.Param#` are job-parameter references resolved from a parameter-set
  block, which may not be in the same export.
- **[UNCONFIRMED]** NULL behaviour of DataStage BASIC's `:` concatenation operator.

## The target

- **[PRIMARY]** dbt resolves `ref()` between models and `source()` against a declared `sources.yml`.
  A model referencing an undeclared source does not compile.
"""


def pack(args):
    try:
        with open(args.table, "r", encoding="utf-8") as fh:
            table = json.load(fh)
    except Exception as ex:
        raise GateAError("platform table unreadable: %s: %s" % (type(ex).__name__, ex))

    # THE TABLE'S HASH, TAKEN BEFORE ANY OTHER WORK, so `table_is_current` below is a diff across the
    # WHOLE pack -- identification, the coverage-gate run, every file written -- rather than two calls
    # to _sha() a microsecond apart, which is what it used to be and which could only ever say `true`.
    table_sha_at_start = _sha(args.table)

    raised = raise_obligations(table, args.table, args.doc, args.ir, args.out_root,
                               args.emit_log, args.inventory)

    bundle = os.path.abspath(args.bundle)
    os.makedirs(bundle, exist_ok=True)

    # AND THE HASH THIS BUNDLE WAS LAST PACKED AGAINST, read before the manifest is overwritten. This
    # is the check the MEASURED false alarm actually needed: a bundle is a SNAPSHOT, and when the same
    # bundle directory is re-packed after the table moved, "the table declares a fact no obligation
    # raises" changes meaning without anything in the directory saying so.
    prev_table_sha = None
    prev_sidecars = None
    _prev_m = os.path.join(bundle, "MANIFEST.json")
    if os.path.isfile(_prev_m):
        try:
            with open(_prev_m, "r", encoding="utf-8") as fh:
                _prev = json.load(fh)
            prev_table_sha = (_prev.get("inputs") or {}).get("table_sha256")
            prev_sidecars = ((_prev.get("freshness") or {}).get("sidecars") or {}).get("sidecars")
        except Exception:
            prev_table_sha = None
            prev_sidecars = None

    # A PREVIOUS ANSWER IN THE BUNDLE IS A LEAK, and the worst kind: a verifier that reads last
    # round's verdict.json is not blind, it is agreeing. So packing CLEARS prior answers by default
    # and says which files it removed.
    #
    # A real loop iteration is the one case where the previous unresolved list SHOULD be visible --
    # that is what makes it a loop rather than a re-run. `--carry-forward` keeps it, under a name that
    # cannot be mistaken for evidence about the document. The default is blind because the expensive
    # mistake is the silent one.
    cleared = []
    carried = None
    # `PREVIOUS_UNRESOLVED.json` IS FIRST so a stale one from an earlier loop cannot survive a pack that
    # is NOT carrying forward. It is removed, then rewritten from this bundle's own sidecar when
    # `--carry-forward` is set -- so the carried list always belongs to the iteration that just ran, and
    # a blind iteration 1 never inherits an open list from a previous run of the loop.
    for stale in ("PREVIOUS_UNRESOLVED.json", "verdict.json", "gateA-sidecar.json",
                  "gateA-loop.json", "verifier-run.json"):
        sp = os.path.join(bundle, stale)
        if not os.path.isfile(sp):
            continue
        if args.carry_forward and stale == "gateA-sidecar.json":
            with open(sp, "r", encoding="utf-8") as fh:
                prev = json.load(fh)
            carried = os.path.join(bundle, "PREVIOUS_UNRESOLVED.json")
            with open(carried, "w", encoding="utf-8") as fh:
                json.dump({"_note": "the PREVIOUS iteration's unresolved obligations, carried "
                                    "forward on purpose. This is a claim by an earlier verifier, "
                                    "NOT evidence about the document. Re-establish anything you "
                                    "rely on from the document itself.",
                           "iteration": prev.get("loop", {}).get("iteration"),
                           "unresolved": prev.get("unresolved") or []}, fh, indent=1)
        os.remove(sp)
        cleared.append(stale)

    # the document, twice: verbatim and line-numbered
    ext = os.path.splitext(args.doc)[1] or ".txt"
    shutil.copyfile(args.doc, os.path.join(bundle, "source_document" + ext))
    lines = read_lines(args.doc)
    with open(os.path.join(bundle, "source_document.lines.txt"), "w", encoding="utf-8") as fh:
        for i, ln in enumerate(lines, start=1):
            fh.write("%5d: %s\n" % (i, ln))

    removed = []
    projected = strip_commentary(table, removed)
    projected["table_version"] = "sha256:" + _sha(args.table)[:16]
    with open(os.path.join(bundle, "platform_table.json"), "w", encoding="utf-8") as fh:
        json.dump(projected, fh, indent=1, sort_keys=False)

    shutil.copyfile(args.ir, os.path.join(bundle, "ir.json"))

    # coverage_gate's report, produced by RUNNING IT, not by describing it.
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            cg_rc = coverage_gate.main([args.table, args.doc, args.ir, args.out_root]
                                       + (["--emit-log", args.emit_log] if args.emit_log else []))
    except SystemExit as ex:                     # it returns rather than exits, but be safe
        cg_rc = int(ex.code or 0)
    with open(os.path.join(bundle, "coverage_gate.report.txt"), "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
        fh.write("\n[coverage_gate.py exit code: %s]\n" % cg_rc)

    # ---- FRESHNESS, and why the obvious check is not the load-bearing one ---------------------
    #
    # MEASURED as a false alarm. A round-2 verifier reported three `no_slot_facts` as declared by the
    # table and never raised by any obligation. A live run raises exactly those three: ITS BUNDLE
    # PREDATED THEM. The finding was true of the bundle and false of the pipeline, and the verifier
    # named the trap itself: "from inside the bundle those two hypotheses are indistinguishable. 'The
    # table declares a fact and no obligation raises it' reads identically whether the pipeline has a
    # gap or the bundle predates the fix, and the hard constraint forbids the one check that would
    # separate them."
    #
    # The bundle isolation that makes this gate trustworthy is exactly what stops a verifier checking.
    # So the PACKER checks and writes the answer in, which costs no isolation at all.
    #
    # TWO checks, and they are not the same:
    #
    #   table_is_current      the table as this bundle records it, DIFFED against the live file after
    #                         all packing work is done. It answers "did the artifact I am describing
    #                         move while I was describing it", and -- with
    #                         `table_changed_since_previous_pack` -- "did it move since the last time
    #                         this bundle was built". The manifest already carried
    #                         `inputs.table_sha256` and NOTHING compared it to anything; a hash nobody
    #                         diffs is a decoration.
    #   ir_is_current_with_table  THE ONE THAT MATTERS. The IR was produced by an earlier run against
    #                         whatever the table said THEN; the table is packed as it is NOW. If the
    #                         table is newer than the IR, the bundle can show a table declaring facts
    #                         the IR never had a chance to honour, which is precisely the false alarm
    #                         above. Compared on mtime because that is the only ordering evidence the
    #                         artifacts carry -- stated as such, not dressed up as provenance.
    #
    # DIRECTION, worth recording: this staleness is SAFE. A stale bundle makes the pipeline look WORSE
    # than it is, manufacturing false alarms rather than hiding defects. Every other stale-artifact
    # instance in this project hid one. That asymmetry is the reason to fix it by ADDING a line to the
    # bundle rather than by relaxing the isolation.
    live_table_sha = _sha(args.table)
    ir_mtime = os.path.getmtime(args.ir)
    table_mtime = os.path.getmtime(args.table)
    freshness = {
        # A REAL DIFF, and it can be False: start-of-pack bytes versus end-of-pack bytes.
        "table_is_current": live_table_sha == table_sha_at_start,
        "table_sha256_at_pack_start": table_sha_at_start[:16],
        "table_sha256_now": live_table_sha[:16],
        # None = this bundle had no previous pack to compare against. Never silently False.
        "table_changed_since_previous_pack": (None if prev_table_sha is None
                                              else prev_table_sha != live_table_sha),
        "previous_pack_table_sha256": (prev_table_sha or "")[:16] or None,
        "ir_is_current_with_table": ir_mtime >= table_mtime,
        "ir_mtime_utc": datetime.fromtimestamp(ir_mtime, timezone.utc).isoformat(timespec="seconds"),
        "table_mtime_utc": datetime.fromtimestamp(table_mtime,
                                                  timezone.utc).isoformat(timespec="seconds"),
        "_how": ("`table_is_current` diffs the platform table's bytes at the START of packing against "
                 "the same file after the document, the projected table, the IR and the coverage-gate "
                 "report were all staged; FALSE means the table moved underneath this bundle and "
                 "nothing in it can be trusted to describe one state. "
                 "`table_changed_since_previous_pack` compares against the hash the PREVIOUS pack of "
                 "this same bundle recorded, and is null when there was no previous pack -- a bundle "
                 "is a snapshot, and the same directory re-packed after the table changed is a "
                 "different experiment. `ir_is_current_with_table` is the load-bearing one: it says "
                 "whether the IR in this bundle was produced at or after the platform table's last "
                 "change. When it is FALSE, a table fact that no obligation raises may simply postdate "
                 "the IR -- report both hypotheses, do not pick the alarming one. LIMITATION, stated "
                 "because it makes this check a detector of the clear-cut case rather than a "
                 "guarantee: mtime is the only ordering evidence these artifacts carry, and COPYING "
                 "an IR resets it, so this can read `true` for an IR that was in fact generated "
                 "against an older table. It can therefore miss staleness; when it fires, it is "
                 "right."),
    }
    # THE SIDECAR HALF. Added because the table is no longer the only mutable input -- see
    # `sidecar_freshness` for the measurement that forced it. Nested under its own key so nothing
    # reading `freshness["table_is_current"]` changes meaning.
    freshness["sidecars"] = sidecar_freshness(args.doc, args.ir, "ir", prev=prev_sidecars)

    raised_out = dict(raised)
    # THE VERIFIER READS obligations.json; it does not read MANIFEST.json. A freshness note that lives
    # only in the manifest is a note nobody acts on, which is the same defect as a gate off the path.
    raised_out["bundle_freshness"] = freshness
    with open(os.path.join(bundle, "obligations.json"), "w", encoding="utf-8") as fh:
        json.dump(raised_out, fh, indent=1)
    with open(os.path.join(bundle, "PROMPT.md"), "w", encoding="utf-8") as fh:
        fh.write(PROMPT)
    with open(os.path.join(bundle, "SOURCE_FORMAT_REFERENCE.md"), "w", encoding="utf-8") as fh:
        fh.write(FORMAT_REFERENCE)

    manifest = {
        "gate": "A",
        "freshness": freshness,
        "packed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform": raised["platform"],
        "counting_rule": raised["counting_rule"],
        "link_rule": raised["link_rule"],
        "residue_rule": raised["residue_rule"],
        "raised": raised["counts"],
        "commentary_keys_stripped": sorted(set(removed)),
        "withheld": [{"what": w, "why": y} for w, y in WITHHELD],
        "replaced_not_withheld": [{"what": w, "why": y} for w, y in REPLACED],
        # PRIVATE TO SCORING, not to the bundle's reader: the real inputs, so a result can be traced
        # back to the exact table and document that produced it.
        "inputs": {
            "table": os.path.abspath(args.table), "table_sha256": _sha(args.table),
            "document": os.path.abspath(args.doc), "document_sha256": _sha(args.doc),
            "ir": os.path.abspath(args.ir), "ir_sha256": _sha(args.ir),
            "output_root": os.path.abspath(args.out_root),
            "coverage_gate_exit": cg_rc,
            # THE DEPENDENCY'S OWN HASH. This gate IMPORTS coverage_gate and calls its counters, so
            # its counting rule is part of the denominator -- and it is edited by other work. Drift
            # between packing and scoring would mean the verifier answered one question and the scorer
            # graded another, which is the adjacent-verification hazard inside the gate. Recorded here
            # and checked at score time, because a dependency you cannot detect changing is a
            # dependency you are not measuring.
            "coverage_gate_sha256": _sha(os.path.join(HERE, "coverage_gate.py")),
        },
        "files": [],
    }
    # WHAT PACK WROTE, not whatever is lying in the directory.
    #
    # MEASURED: the manifest listed `verdict.STALE-...json`, a file set aside by hand after packing, and
    # then the file was moved -- so the manifest advertised a bundle member that did not exist. A
    # manifest whose contents you cannot verify by looking is worse than no manifest, because the whole
    # point of it is that the staging is auditable after the fact (findings/43). So the list is the
    # KNOWN produced set, and anything else present is reported separately rather than absorbed.
    produced = ["source_document" + ext, "source_document.lines.txt", "platform_table.json",
                "ir.json", "coverage_gate.report.txt", "obligations.json", "PROMPT.md",
                "SOURCE_FORMAT_REFERENCE.md"]
    if carried:
        produced.append("PREVIOUS_UNRESOLVED.json")
    for f in produced:
        fp = os.path.join(bundle, f)
        if os.path.isfile(fp):
            manifest["files"].append({"file": f, "bytes": os.path.getsize(fp),
                                      "sha256": _sha(fp)[:16]})
        else:
            manifest["files"].append({"file": f, "MISSING": True})
    strays = sorted(f for f in os.listdir(bundle)
                    if os.path.isfile(os.path.join(bundle, f))
                    and f not in produced and f != "MANIFEST.json")
    manifest["unexpected_files"] = strays
    with open(os.path.join(bundle, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)

    print("=" * W)
    print(" GATE A — evidence bundle packed")
    print("=" * W)
    print(" bundle        : %s" % bundle)
    print(" platform      : %s" % raised["platform"])
    print(" rules         : elements %s | links %s | residue %s"
          % (raised["counting_rule"], raised["link_rule"], raised["residue_rule"]))
    print(" raised        : %d obligation(s)  ELEMENT=%d LINK=%d RESIDUE=%d IR_UNMATCHED=%d"
          % (sum(raised["counts"].values()), raised["counts"]["ELEMENT"], raised["counts"]["LINK"],
             raised["counts"]["RESIDUE"], raised["counts"]["IR_UNMATCHED"]))
    if raised["inventory"]:
        print(" inventory     : %s" % raised["inventory"])
    else:
        print(" inventory     : none supplied — residue computed by this gate's own document census")
    print(" stripped      : %d commentary key name(s) from the platform table" % len(set(removed)))
    print(" freshness     : ir_is_current_with_table=%s  (ir %s, table %s)"
          % (freshness["ir_is_current_with_table"], freshness["ir_mtime_utc"],
             freshness["table_mtime_utc"]))
    if not freshness["ir_is_current_with_table"]:
        print("                 *** THE IR PREDATES THE PLATFORM TABLE. A table fact that no")
        print("                 obligation raises may postdate the IR rather than being a gap. This")
        print("                 staleness is SAFE IN DIRECTION -- it manufactures false alarms rather")
        print("                 than hiding defects -- but re-run identification before acting on one.")
    print("                 table_is_current=%s  (start %s -> now %s)"
          % (freshness["table_is_current"], freshness["table_sha256_at_pack_start"],
             freshness["table_sha256_now"]))
    if not freshness["table_is_current"]:
        print("                 *** THE PLATFORM TABLE CHANGED WHILE THIS BUNDLE WAS BEING PACKED.")
        print("                 The obligations and the staged table may describe different states.")
        print("                 Re-pack; do not score this bundle.")
    if freshness["table_changed_since_previous_pack"]:
        print("                 *** THE TABLE CHANGED SINCE THIS BUNDLE WAS LAST PACKED (%s -> %s)."
              % (freshness["previous_pack_table_sha256"], freshness["table_sha256_now"]))
        print("                 A bundle is a snapshot. Any earlier verdict in this directory answered")
        print("                 a different question and has been cleared rather than carried.")
    _sc = freshness["sidecars"]
    print("                 sidecars=%d  ir_is_current_with_sidecars=%s"
          % (len(_sc["sidecars"]), _sc["ir_is_current_with_sidecars"]))
    for _r in _sc["sidecars"]:
        print("                   %s  %s  %s" % (_r["sha256"], _r["mtime_utc"], _r["file"]))
    if _sc["stale_against_ir"]:
        print("                 *** THE IR PREDATES A MODEL-AUTHORED SIDECAR: %s."
              % ", ".join(_sc["stale_against_ir"]))
        print("                 Sidecars decide element kinds and lowered SQL, so this bundle describes")
        print("                 a pipeline the current sidecar would not produce. Re-emit, then re-pack.")
        print("                 Direction is the same as the table case: it manufactures a FALSE ALARM")
        print("                 rather than hiding a defect, which is why it is reported and not fatal.")
    if _sc["sidecars_changed_since_previous_pack"]:
        print("                 *** A SIDECAR CHANGED SINCE THIS BUNDLE WAS LAST PACKED: %s."
              % ", ".join(_sc["sidecars_changed_since_previous_pack"]))
    if cleared:
        print(" cleared       : %s — a previous answer in the bundle is a leak, not context"
              % ", ".join(cleared))
    if carried:
        print(" carried fwd   : PREVIOUS_UNRESOLVED.json (--carry-forward): a loop iteration may see")
        print("                 last round's open list, labelled as a claim rather than as evidence")
    for c in raised["caveats"]:
        print("-" * W)
        for chunk in _wrap(c, W - 2):
            print(" %s" % chunk)
    print("-" * W)
    print(" next          : hand %s to a verifier; it writes verdict.json beside the bundle files."
          % os.path.join(bundle, "PROMPT.md"))
    print("                 then: gate_a.py score --bundle %s --verdict %s"
          % (bundle, os.path.join(bundle, "verdict.json")))
    return 0


# ---------------------------------------------------------------------------------------------
# SCORE — ingest the verifier's answers and adjudicate.
#
# Every mechanism here exists because of something this project measured, not because it seemed
# prudent: the raised set is recomputed (the fit score rose as elements were lost), unanswered is
# OUTSTANDING (a loop that can only pass is a slower yes), citations are re-read (a sub-agent asserted
# a dialect rule backwards), ABSENT_BY_TABLE_RULE is checked against the table (a legitimate absence
# and a silent drop look identical from the outside), and the stop reason is recorded (converged and
# gave up must not look the same).
# ---------------------------------------------------------------------------------------------

# TWO VERDICTS ADDED BECAUSE THE FIRST VOCABULARY COULD NOT EXPRESS ITS OWN FINDING.
#
# MEASURED: a verifier found an element whose IR node exists but whose payload does not correspond to
# what the document states. It answered PRESENT -- literally correct -- and wrote: "the ELEMENT
# vocabulary has no word for 'carried but misrepresented', and because the node matched an obligation it
# never reaches the IR_UNMATCHED family where FABRICATED lives ... a scorer counting verdict words alone
# will read this bundle as clean." A gate whose verdict words cannot express its own finding is scored
# as PASSING, which is this project's central failure mode one level up -- the same shape as a closed
# 888-member issue enum forcing a wrong answer, and as an exit code that could not tell success from
# silent loss.
#
#   PRESENT_MISREPRESENTED  carried, and wrong. OUTSTANDING: a real fidelity loss that must not be able
#                           to hide behind PRESENT.
#   PRESENT_MODEL_SUPPLIED  carried, and the payload came from a MODEL rather than from the document.
#                           DISCHARGED -- tier 2 supplying a lowered expression for a dialect no engine
#                           translator handles is the ladder working as designed, and failing on it is
#                           the gate that cries wolf. But it is a DIFFERENT FIDELITY CLAIM, and
#                           tier-2 content currently ships with no marker, so this is the one place in
#                           the chain that says so. Reported as a provenance flag on the ledger line;
#                           discharging it SILENTLY would reopen the gap in the other direction.
ELEMENT_LINK_VERDICTS = {"PRESENT", "PRESENT_MISREPRESENTED", "PRESENT_MODEL_SUPPLIED",
                         "ABSENT_BY_TABLE_RULE", "ABSENT_NO_SLOT",
                         "ABSENT_NO_RULE_TO_READ_IT", "ABSENT_SILENTLY_DROPPED", "UNVERIFIABLE"}
RESIDUE_VERDICTS = {"IMMATERIAL", "REPRESENTED_ELSEWHERE", "MATERIAL_AND_ABSENT", "UNVERIFIABLE"}
IRX_VERDICTS = {"JUSTIFIED_BY_TABLE", "FABRICATED", "UNVERIFIABLE"}
ALLOWED = {"ELEMENT": ELEMENT_LINK_VERDICTS, "LINK": ELEMENT_LINK_VERDICTS,
           "RESIDUE": RESIDUE_VERDICTS, "IR_UNMATCHED": IRX_VERDICTS}
DISCHARGING = {"PRESENT", "PRESENT_MODEL_SUPPLIED", "ABSENT_BY_TABLE_RULE", "IMMATERIAL",
               "REPRESENTED_ELSEWHERE", "JUSTIFIED_BY_TABLE"}
# Discharged, and never silent. A discharge that carries a fidelity qualifier gets its own line.
PROVENANCE_FLAGGED = {"PRESENT_MODEL_SUPPLIED"}
# OUTSTANDING, and never read as a loss. Gate B returned `UNVERIFIABLE` on a DataStage `:` concat rather
# than guessing, because its dialect sheet had no entry, and `findings/49` recorded that as the
# calibration mechanism working. Gate A's RESIDUE family had the same word in its vocabulary and did not
# OFFER it at the point of the question, so its verifiers chose between two materiality answers when
# neither was established. The word now appears in the criterion -- and because a verdict that costs
# nothing gets used for everything, it carries a bar in the scorer and a heading of its own in the
# report, so a run that abstains its way to repeatability is visible rather than quiet.
UNDECIDED_VERDICTS = {"UNVERIFIABLE"}
BASES = {"DOCUMENT", "TABLE", "IR", "COVERAGE_GATE", "PRIOR"}
# A verdict that changes what the gate reports must be sourced. PRESENT and the *absences* both do.
NEEDS_CITATION = {"PRESENT", "PRESENT_MISREPRESENTED", "PRESENT_MODEL_SUPPLIED",
                  "ABSENT_NO_SLOT", "ABSENT_NO_RULE_TO_READ_IT",
                  "ABSENT_SILENTLY_DROPPED", "ABSENT_BY_TABLE_RULE", "MATERIAL_AND_ABSENT",
                  "REPRESENTED_ELSEWHERE", "IMMATERIAL", "FABRICATED", "JUSTIFIED_BY_TABLE"}
# ... except where the evidence is NOT in the document. An IR-side fabrication is established by the
# document's SILENCE, and you cannot cite a line that is not there; a table-rule absence is
# established by the table. Both are checked against their own artifact instead, below.
CITATION_EXEMPT = {"FABRICATED", "JUSTIFIED_BY_TABLE", "ABSENT_BY_TABLE_RULE"}

# The four families, in the order every ledger line prints them, with the short tags the obligation ids
# carry. Named once because the loop reports flips PER FAMILY and a hand-typed second copy of this list
# would be the thing that silently drops a family from the flip table.
FAMILIES = ("ELEMENT", "LINK", "RESIDUE", "IR_UNMATCHED")
FAMILY_TAG = {"ELEMENT": "EL", "LINK": "LK", "RESIDUE": "RS", "IR_UNMATCHED": "IX"}


def verify_citation(lines, claim):
    """Re-read the cited line. Returns (ok, detail)."""
    loc = claim.get("doc_locus")
    quote = (claim.get("doc_quote") or "").strip()
    if loc in (None, "", 0):
        return False, "no doc_locus"
    try:
        n = int(loc)
    except Exception:
        return False, "doc_locus %r is not a line number" % loc
    if not quote:
        return False, "no doc_quote"
    if n < 1 or n > len(lines):
        return False, "doc_locus %d is outside the document (1..%d)" % (n, len(lines))
    if quote in lines[n - 1]:
        return True, "line %d" % n
    # One tolerance, and only one: a quote that lands within two lines of the citation. A verifier
    # counting lines by eye off a 9000-line file will be off by one; a verifier inventing a quote
    # will not be off by two. Recorded as OFF_BY when it fires, never silently accepted.
    for d in (-2, -1, 1, 2):
        m = n + d
        if 1 <= m <= len(lines) and quote in lines[m - 1]:
            return True, "OFF_BY %+d (quote is at line %d, cited %d)" % (d, m, n)
    # THE MESSAGE, AND WHY IT IS NOT COSMETIC. It used to truncate both strings to 60 characters, so
    # when the difference sat past character 60 the failure read as
    #   quote '<TARGETLOADORDER ORDER="1" TARGETINSTANCE="CUSTOMER_SUMMARY"' is not at line 68,
    #   which reads '<TARGETLOADORDER ORDER="1" TARGETINSTANCE="CUSTOMER_SUMMARY"'
    # -- two strings that are identical as printed. MEASURED on a real Informatica run: the verifier had
    # written `CUSTOMER_SUMMARY" />` where the document has `CUSTOMER_SUMMARY"/>`, one space, and the
    # quarantine was CORRECT. The diagnostic sent a reader looking for a scorer bug instead. A gate whose
    # failure message makes a right decision look like a defect costs the same reviewer time as a wrong
    # decision, so the first differing character is now named and neither string is clipped before it.
    line = lines[n - 1].strip()
    at = next((i for i in range(max(len(quote), len(line)))
               if quote[i:i + 1] != line[i:i + 1]), min(len(quote), len(line)))
    return False, ("quote is not at line %d. first difference at character %d: quoted %r vs line %r "
                   "(quote %r, line %r)"
                   % (n, at + 1, quote[at:at + 12], line[at:at + 12],
                      quote[:120], line[:120]))


def table_declares_collapse(table, kind):
    d = (table.get("kind_dispatch") or {}).get(kind)
    return isinstance(d, dict) and isinstance(d.get("collapse"), dict)


IDENT = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")


def ir_field_names(ir):
    """Every field name that really occurs in this IR, at any depth."""
    names = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                names.add(k)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(ir)
    names.update(("nodes", "edges"))
    return names


def ir_field_check(ir, field):
    """Does the claimed `ir_field` name a field that exists in this IR? -> (ok, what matched)

    A MEASURED DEFECT IN THIS GATE'S SCORER, and a false-positive-generating one. The first version
    did `field.split(".")[-1]`, which assumes the answer is a bare dotted path. A verifier answered

        nodes[id='.../V0S4'].element.TableName = 'CUSTOMER_SUMMARY' (element.$kind = 'Target...')

    -- a correct, richer answer -- and the last dot-segment came out as
    `TableName = 'CUSTOMER_SUMMARY' (element.$kind = 'TargetTransformation')`, which of course
    matches no field, so FOUR correct PRESENT claims were quarantined and reported as unanswered.
    A gate discarding right answers because they were too informative is the same class of failure as
    a gate flagging correct output: both teach the reader to ignore it.

    So: pull every IDENTIFIER out of the claim and require at least one to be a real field name of
    this IR. That still catches the thing the check is for -- an answer naming only fields that do not
    exist -- and the identifier that satisfied it is PRINTED, so "which field carries it" stays
    answerable by a reader rather than taken on trust.
    """
    if not field:
        return False, None
    real = ir_field_names(ir)
    toks = [t for t in IDENT.findall(str(field))]
    hits = [t for t in toks if t in real]
    if hits:
        return True, ", ".join(sorted(set(hits)))
    return False, None

def score(args, collect=None):
    bundle = os.path.abspath(args.bundle)
    mpath = os.path.join(bundle, "MANIFEST.json")
    if not os.path.isfile(mpath):
        raise GateAError("no MANIFEST.json in %s — pack the bundle first" % bundle)
    with open(mpath, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    inp = manifest["inputs"]

    drift = []
    # AND AS BOOLEANS, not only as prose. The manifest carried `inputs.table_sha256` from the day it
    # existed and nothing ever diffed it; a hash nobody compares is a decoration. `pack` now answers
    # "did it move while I was packing" and this answers the other half -- "has it moved since" --
    # because a bundle can be scored days after it was built, and by then the packer's answer is about
    # a state that no longer exists.
    currency = {}
    for key, path in (("table_sha256", inp["table"]), ("document_sha256", inp["document"]),
                      ("ir_sha256", inp["ir"]),
                      ("coverage_gate_sha256", os.path.join(HERE, "coverage_gate.py"))):
        want = inp.get(key)
        label = key.replace("_sha256", "") + "_is_current"
        if not want or not os.path.exists(path):
            currency[label] = None          # never silently True
            continue
        currency[label] = _sha(path) == want
        if not currency[label]:
            drift.append("%s changed since the bundle was packed (%s)"
                         % (os.path.basename(path), key))

    with open(inp["table"], "r", encoding="utf-8") as fh:
        table = json.load(fh)
    # RECOMPUTED, not read back from obligations.json. The denominator has to come from the document
    # on every iteration or a loop could shrink it by editing the file it is judged against.
    raised = raise_obligations(table, inp["table"], inp["document"], inp["ir"],
                              inp["output_root"], args.emit_log, args.inventory)
    by_id = {o["id"]: o for o in raised["obligations"]}
    lines = read_lines(inp["document"])
    with open(inp["ir"], "r", encoding="utf-8") as fh:
        ir = json.load(fh)

    try:
        with open(args.verdict, "r", encoding="utf-8") as fh:
            verdict = json.load(fh)
    except Exception as ex:
        raise GateAError("verifier answer unreadable: %s: %s" % (type(ex).__name__, ex))
    claims = verdict.get("claims")
    if not isinstance(claims, list):
        raise GateAError("verifier answer has no `claims` array")

    rows = {}            # obligation id -> adjudicated record
    rejected = []        # answers naming an obligation that was not raised
    quarantined = []     # answers that cannot count, with the reason
    downgrades = []

    for c in claims:
        oid = c.get("obligation_id")
        o = by_id.get(oid)
        if o is None:
            rejected.append((oid, "no such obligation was raised from this document"))
            continue
        v = (c.get("verdict") or "").strip().upper()
        fam = o["family"]
        if v not in ALLOWED[fam]:
            quarantined.append((oid, "verdict %r is not in the %s vocabulary" % (v, fam)))
            continue
        basis = (c.get("basis") or "").strip().upper()
        if basis not in BASES:
            quarantined.append((oid, "basis %r is not declared" % basis))
            continue
        if basis == "PRIOR":
            # QUARANTINED BY CONSTRUCTION. Gate B measured that a verifier working from priors can be
            # right; the problem is that it is right unearnedly, so the next case is a coin flip.
            quarantined.append((oid, "basis PRIOR: asserted from the verifier's own knowledge rather "
                                     "than from the bundle. Printed, never counted."))
            continue

        note = []
        # -- the checks that stop a verdict being talked into existence ---------------------------
        if v == "ABSENT_BY_TABLE_RULE":
            # Checked against the table, in BOTH families. An element is legitimately absent when its
            # own kind is collapse-declared; a LINK is legitimately absent when an ENDPOINT's kind is,
            # because a folded element takes its edges with it.
            kinds = ([o.get("kind")] if fam == "ELEMENT"
                     else [o.get("from_kind"), o.get("to_kind")] if fam == "LINK" else [])
            ok = any(table_declares_collapse(table, k) for k in kinds if k)
            if not ok:
                v = "ABSENT_SILENTLY_DROPPED"
                downgrades.append((oid, "ABSENT_BY_TABLE_RULE -> ABSENT_SILENTLY_DROPPED: the "
                                        "platform table declares no collapse for %s, so this "
                                        "absence is not a design decision"
                                    % (", ".join(repr(k) for k in kinds if k) or "this obligation")))
                note.append("DOWNGRADED from ABSENT_BY_TABLE_RULE")
        if v in ("PRESENT", "PRESENT_MISREPRESENTED", "PRESENT_MODEL_SUPPLIED"):
            fld = c.get("ir_field")
            if not fld:
                quarantined.append((oid, "%s with no ir_field: 'which field carries it' is the "
                                         "question, and it is unanswered" % v))
                continue
            ok, matched = ir_field_check(ir, fld)
            if not ok:
                quarantined.append((oid, "PRESENT naming ir_field %r: not one identifier in it is a "
                                         "field name that occurs anywhere in ir.json" % fld))
                continue
            note.append("ir_field resolved on: %s" % matched)
        if v == "FABRICATED":
            if fam != "IR_UNMATCHED":
                quarantined.append((oid, "FABRICATED is only a verdict about an IR-side obligation"))
                continue
        if v in ("MATERIAL_AND_ABSENT", "PRESENT_MISREPRESENTED") \
                and not (c.get("what_breaks") or "").strip():
            quarantined.append((oid, "%s with no `what_breaks`: a claim of harm with no stated "
                                     "consequence is prose" % v))
            continue
        # THE BAR ON THE ESCAPE HATCH, and it exists because of the trap the escape hatch opens.
        # RESIDUE_CRITERION now OFFERS `UNVERIFIABLE` at the point of the question -- step 5, for the
        # case where the bundle genuinely cannot settle materiality. A verifier answering every residue
        # class `UNVERIFIABLE` would be perfectly repeatable and perfectly useless, which is the same
        # failure as one answering every class `IMMATERIAL`: a gate incapable of saying anything. So the
        # word costs something -- name the evidence that would decide it, or the claim does not count.
        # NOT the same check as `what_breaks` above: that one guards a claim of harm, this one guards a
        # claim of ignorance, and this project has been bitten by both being free.
        if v == "UNVERIFIABLE" and fam == "RESIDUE" and not (c.get("reason") or "").strip():
            quarantined.append((oid, "UNVERIFIABLE with no `reason`: the criterion asks which evidence "
                                     "would decide it, and an undecided verdict that says nothing is "
                                     "silence with a word on it"))
            continue

        cit_ok, cit_detail = True, "not required for %s" % v
        if v in NEEDS_CITATION and v not in CITATION_EXEMPT:
            cit_ok, cit_detail = verify_citation(lines, c)
            if not cit_ok:
                quarantined.append((oid, "citation failed: %s" % cit_detail))
                continue

        prev = rows.get(oid)
        if prev is not None:
            # Two answers to one obligation. Keeping the first and reporting the second is the only
            # option that cannot be gamed by ordering.
            quarantined.append((oid, "second answer to an obligation already answered %r; ignored"
                                    % prev["verdict"]))
            continue
        rows[oid] = {
            "obligation_id": oid, "family": fam, "verdict": v, "basis": basis,
            "doc_locus": c.get("doc_locus"), "doc_quote": c.get("doc_quote"),
            "citation": cit_detail, "ir_field": c.get("ir_field"),
            "reason": (c.get("reason") or "").strip(),
            "what_breaks": (c.get("what_breaks") or "").strip(),
            "notes": note,
        }

    unanswered = [oid for oid in by_id if oid not in rows]
    discharged = [r for r in rows.values() if r["verdict"] in DISCHARGING]
    outstanding = [r for r in rows.values() if r["verdict"] not in DISCHARGING]
    n_raised = len(by_id)
    n_out = len(outstanding) + len(unanswered)
    balances = n_raised == len(discharged) + n_out
    return _report_and_write(args, bundle, manifest, raised, rows, rejected, quarantined,
                            downgrades, unanswered, discharged, outstanding, n_raised, n_out,
                            balances, verdict, drift, currency, collect=collect)


# ---------------------------------------------------------------------------------------------
# THE LOOP'S TWO MEASUREMENTS, as pure functions over the adjudicated state.
#
# A LOOP THAT RE-ASKS UNTIL NOTHING IS OUTSTANDING IS A GATE THAT CANNOT FAIL. Iterating toward
# convergence is, stated plainly, optimising for a clean ledger -- and four gates in this project have
# already been found incapable of failing, each one caught by disbelieving a good number. So turning the
# loop on is only defensible alongside the two things that make its output readable as evidence rather
# than as pressure, and both of them are computed here rather than asserted in prose:
#
#   `denominator_drift` -- the loop must not be able to touch the DENOMINATOR. Obligations are raised
#       deterministically from the document before any verifier runs, so the set of raised ids must be
#       IDENTICAL across every iteration of a run. If iteration 2 can add or drop one, every ledger in
#       the run is measuring a different question and the convergence is an artefact of arithmetic.
#       That is a bigger finding than the loop, so it aborts the run rather than being noted.
#
#   `flip_report` -- the DIRECTION of every verdict change, per family, counted separately. A delta
#       alone cannot distinguish a second look that CORRECTED the first from a second look that was
#       PRESSURED into agreeing: both show outstanding falling. A correcting second look produces flips
#       in BOTH directions; if every flip runs toward discharge, the honest reading is that the loop is
#       pressuring the verifier, and the report says so in those words.
# ---------------------------------------------------------------------------------------------

def denominator_drift(records):
    """Did the raised set move between iterations? Returns a list of drifts, empty when it did not.

    Compared against ITERATION 1 rather than pairwise, so a drift that appears at iteration 2 and
    persists is reported once per iteration instead of once, and an obligation that leaves at 2 and
    returns at 3 cannot cancel itself out.
    """
    if len(records) < 2:
        return []
    base_scored = list(records[0].get("scored_ids") or [])
    base_set = set(base_scored)
    out = []
    for r in records[1:]:
        got = list(r.get("scored_ids") or [])
        added = [o for o in got if o not in base_set]
        dropped = [o for o in base_scored if o not in set(got)]
        if added or dropped:
            out.append({"iteration": r.get("iteration"), "added": added, "dropped": dropped,
                        "raised_at_iteration_1": len(base_scored), "raised_now": len(got)})
    return out


def packed_vs_scored_drift(record):
    """Within ONE iteration: was the verifier asked the same question the scorer graded?

    `pack` writes obligations.json and `score` recomputes the raised set from the document. Those are
    the same function called twice, so they agree -- unless something between them moved, which is the
    adjacent-verification hazard living inside the gate rather than outside it. Checked because "they
    cannot disagree" is the kind of claim this project has measured wrong four times.
    """
    packed, scored = list(record.get("packed_ids") or []), list(record.get("scored_ids") or [])
    if packed == scored:
        return None
    return {"iteration": record.get("iteration"),
            "only_in_the_verifier_s_question_set": [o for o in packed if o not in set(scored)],
            "only_in_the_scorer_s_set": [o for o in scored if o not in set(packed)]}


def flip_direction(was, now):
    """One obligation's verdict change, classified by DIRECTION. None when the word did not change."""
    if was == now:
        return None
    if was not in DISCHARGING and now in DISCHARGING:
        return "TOWARD_DISCHARGED"
    if was in DISCHARGING and now not in DISCHARGING:
        return "TOWARD_OUTSTANDING"
    # The word changed and the discharge state did not: PRESENT -> PRESENT_MODEL_SUPPLIED, or
    # ABSENT_NO_RULE_TO_READ_IT -> ABSENT_SILENTLY_DROPPED. Reported separately because it is a
    # RE-CLASSIFICATION rather than a reversal, and rolling it into either direction would inflate that
    # direction's count with changes that moved no obligation across the bar.
    return "LATERAL"


def flip_report(prev_verdicts, now_verdicts, families):
    """Per-family flip counts plus every flip itemised, for one iteration against the previous one."""
    flips = []
    for oid in now_verdicts:
        if oid not in prev_verdicts:
            continue                       # denominator drift; reported by its own check, not here
        d = flip_direction(prev_verdicts[oid], now_verdicts[oid])
        if d:
            flips.append({"obligation_id": oid, "family": families.get(oid, "?"),
                          "from": prev_verdicts[oid], "to": now_verdicts[oid], "direction": d})
    by_fam = {fam: {"TOWARD_DISCHARGED": 0, "TOWARD_OUTSTANDING": 0, "LATERAL": 0}
              for fam in FAMILIES}
    for f in flips:
        if f["family"] in by_fam:
            by_fam[f["family"]][f["direction"]] += 1
    tot = {k: sum(by_fam[fam][k] for fam in FAMILIES)
           for k in ("TOWARD_DISCHARGED", "TOWARD_OUTSTANDING", "LATERAL")}
    reversals = tot["TOWARD_DISCHARGED"] + tot["TOWARD_OUTSTANDING"]
    return {
        "flips": sorted(flips, key=lambda f: (f["family"], f["obligation_id"])),
        "by_family": by_fam,
        "totals": tot,
        # TRUE when every reversal ran the same way. Not a verdict on its own -- a one-obligation flip
        # is trivially one-directional -- which is why the count sits beside it everywhere it is printed.
        "one_directional": reversals > 0 and (tot["TOWARD_DISCHARGED"] == 0
                                              or tot["TOWARD_OUTSTANDING"] == 0),
        "reversals": reversals,
    }


def _packed_obligation_ids(bundle):
    """The ids as the VERIFIER was handed them, read back out of the bundle it read."""
    with open(os.path.join(bundle, "obligations.json"), "r", encoding="utf-8") as fh:
        return [o["id"] for o in (json.load(fh).get("obligations") or [])]


def _stop_reason(loop_path, iteration, max_iterations, n_out, history=None):
    """WHY THE LOOP STOPPED, recorded rather than inferred.

    Otherwise `converged` and `gave up` look identical downstream, which is the same conflation as
    exit 0 versus exit 3 and as "the ledger found loss" versus "the ledger could not run" -- both of
    which already bit this project.

    `history` IS PASSED IN BY THE LOOP AND READ OFF DISK BY A STANDALONE `score`, and the difference is
    a bug the loop surfaced rather than a preference. `pack` CLEARS `gateA-loop.json` -- correctly: a
    previous answer in the bundle is a leak. But a real loop re-packs between iterations, so reading the
    history from that file inside a loop reads it back as EMPTY every time, and `NO_PROGRESS` -- which
    is defined by comparison with the previous iteration -- could then never fire. The loop therefore
    holds the history itself; nothing else about the file changes.
    """
    if history is None:
        history = []
        if os.path.isfile(loop_path):
            try:
                with open(loop_path, "r", encoding="utf-8") as fh:
                    history = json.load(fh).get("iterations") or []
            except Exception:
                history = []
    else:
        history = list(history)
    history = [h for h in history if h.get("iteration") != iteration]
    history.append({"iteration": iteration, "outstanding": n_out,
                    "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    history.sort(key=lambda h: h["iteration"])
    prev = [h for h in history if h["iteration"] < iteration]
    if n_out == 0:
        reason = "CONVERGED"
        detail = "every raised obligation is discharged"
    elif max_iterations is not None and iteration >= max_iterations:
        reason = "EXHAUSTED_ITERATIONS"
        detail = ("the iteration bound %d was reached with %d obligation(s) still outstanding. This "
                  "is a FAIL with a handover list, not a convergence." % (max_iterations, n_out))
    elif prev and n_out >= prev[-1]["outstanding"]:
        reason = "NO_PROGRESS"
        detail = ("outstanding went %d -> %d across iteration %d. The loop is not converging; the "
                  "handover list is final unless the inputs change."
                  % (prev[-1]["outstanding"], n_out, iteration))
    else:
        reason = "OPEN"
        detail = ("%d outstanding after iteration %d of %s; another iteration is permitted"
                  % (n_out, iteration, max_iterations if max_iterations is not None else "unbounded"))
    return {"iterations": history, "iteration": iteration, "max_iterations": max_iterations,
            "outstanding": n_out, "stop_reason": reason, "stop_detail": detail}


def _report_and_write(args, bundle, manifest, raised, rows, rejected, quarantined, downgrades,
                      unanswered, discharged, outstanding, n_raised, n_out, balances, verdict,
                      drift=(), currency=None, collect=None):
    loop = _stop_reason(os.path.join(bundle, "gateA-loop.json"), args.iteration,
                        args.max_iterations, n_out,
                        history=getattr(args, "loop_history", None))

    print("=" * W)
    print(" GATE A — IR COMPLETENESS (agentic half)")
    print("=" * W)
    print(" bundle        : %s" % bundle)
    print(" platform      : %s   [table sha256 %s]"
          % (raised["platform"], manifest["inputs"]["table_sha256"][:16]))
    print(" document      : %s" % manifest["inputs"]["document"])
    print(" verifier      : %s" % (verdict.get("verifier") or "UNNAMED"))
    print(" RULES         : elements %s | links %s | residue %s"
          % (raised["counting_rule"], raised["link_rule"], raised["residue_rule"]))
    print(" coverage_gate : exit %s (the deterministic half, embedded in the bundle verbatim)"
          % manifest["inputs"]["coverage_gate_exit"])
    if drift:
        # NOT fatal, and NOT silent. The verifier answered questions built from the inputs as they
        # were; if an input has moved the two halves are describing different states, and a reader has
        # to know that before reading a single verdict below.
        print(" *** INPUT DRIFT — the verifier was asked about inputs that have since changed:")
        for d in drift:
            print("     %s" % d)
        print("     The verdicts below were produced against the PACKED state. Re-pack and re-run")
        print("     before treating this ledger as current.")
    if currency:
        print(" currency      : " + "  ".join(
            "%s=%s" % (k.replace("_is_current", ""), v) for k, v in sorted(currency.items())))
    print("-" * W)
    print(" %-38s %-9s %-26s %s" % ("obligation", "family", "verdict", "citation"))
    print("-" * W)
    for oid in [o["id"] for o in raised["obligations"]]:
        r = rows.get(oid)
        if r is None:
            print(" %-38s %-9s %-26s %s"
                  % (coverage_gate._cliptail(oid, 38),
                     coverage_gate._clip(by_family(raised, oid), 9), "UNANSWERED",
                     "no answer — scored OUTSTANDING"))
            continue
        print(" %-38s %-9s %-26s %s"
              % (coverage_gate._cliptail(oid, 38), coverage_gate._clip(r["family"], 9),
                 r["verdict"], r["citation"]))
        if r["ir_field"]:
            print("        carried by : %s" % r["ir_field"])
        if r["reason"]:
            for chunk in _wrap(r["reason"], W - 10):
                print("        %s" % chunk)
        if r["what_breaks"]:
            for chunk in _wrap("BREAKS: " + r["what_breaks"], W - 10):
                print("        %s" % chunk)
        for n in r["notes"]:
            print("        *** %s" % n)
    print("-" * W)
    if downgrades:
        print(" DOWNGRADED CLAIMS — a legitimate absence has to be declared by the table, not asserted:")
        for oid, why in downgrades:
            for chunk in _wrap("%s: %s" % (oid, why), W - 6):
                print("     %s" % chunk)
    if quarantined:
        print(" QUARANTINED CLAIMS — could not count, and why. These do NOT discharge anything:")
        for oid, why in quarantined:
            for chunk in _wrap("%s: %s" % (oid, why), W - 6):
                print("     %s" % chunk)
    if rejected:
        print(" REJECTED ANSWERS — an obligation this document never raised:")
        for oid, why in rejected:
            print("     %s: %s" % (oid, why))
    print("-" * W)
    # THE LEDGER LINE. The driver disambiguates "the gate ran and found work" from "the gate could not
    # run" on this string, exactly as it already does for the loss ledger and coverage_gate.
    flagged = [r for r in discharged if r["verdict"] in PROVENANCE_FLAGGED]
    # OUTSTANDING, AND NOT A CLAIM OF LOSS. `UNVERIFIABLE` is the criterion's step 5: the verifier knows
    # the content is unrepresented and cannot decide from this bundle whether behaviour depends on it.
    # It does NOT discharge -- it stays on the handover list, which is the whole point -- but rolling it
    # into `outstanding` and stopping there reports an undecided question as a found defect, and the
    # ledger's readers act on that number. Counted here and printed under its own heading.
    undecided = [r for r in outstanding if r["verdict"] in UNDECIDED_VERDICTS]
    if undecided:
        print(" UNDECIDED — the verifier declined to guess. OUTSTANDING, and NOT a reported loss:")
        for r in undecided:
            print("     %s [%s] : %s" % (r["obligation_id"], r["family"], r["verdict"]))
            for chunk in _wrap(r["reason"] or "(no reason given)", W - 10):
                print("        %s" % chunk)
        print("     Each of these says the bundle cannot settle the question and names what would.")
        print("     They are on the handover list because unanswered is not clean; they are printed")
        print("     apart from the losses because a guess and an abstention are different results and")
        print("     one integer cannot carry both.")
        print("-" * W)
    if flagged:
        # DISCHARGED, AND NEVER SILENT. The obligation is met -- the element IS carried -- but the
        # payload came from a model rather than from the document, and tier-2 content currently ships
        # with no marker of its own, so this is the only place in the chain that states the difference.
        print(" PROVENANCE — carried, but NOT read from the source document:")
        for r in flagged:
            print("     %s : %s" % (r["obligation_id"], r["verdict"]))
            for chunk in _wrap(r["reason"] or "(no reason given)", W - 10):
                print("        %s" % chunk)
        print("     These DISCHARGE their obligation: a model supplying a lowered expression for a")
        print("     dialect no engine translator handles is the fallback ladder working as designed.")
        print("     They are printed because model-authored and document-read content are different")
        print("     fidelity claims and nothing else in the chain distinguishes them here.")
        print("-" * W)
    print(" ledger        : raised=%d discharged=%d outstanding=%d quarantined=%d rejected=%d "
          "model_supplied=%d undecided=%d balances=%s"
          % (n_raised, len(discharged), n_out, len(quarantined), len(rejected), len(flagged),
             len(undecided), balances))
    print(" by family     : " + "  ".join(
        "%s %d/%d" % (fam,
                      sum(1 for r in discharged if r["family"] == fam),
                      raised["counts"][fam])
        for fam in FAMILIES))
    print(" NO SCORE IS REPORTED. The bar is obligations discharged; a percentage is a number the")
    print("                 loop can move, and this project measured one rising as elements were lost.")
    print(" loop          : iteration %d of %s — stop reason %s"
          % (loop["iteration"],
             loop["max_iterations"] if loop["max_iterations"] is not None else "unbounded",
             loop["stop_reason"]))
    for chunk in _wrap(loop["stop_detail"], W - 18):
        print("                 %s" % chunk)

    # ---- sidecar, MODEL provenance, never a patch to a deterministic file ------------------------
    sidecar_path = args.sidecar or os.path.join(bundle, "gateA-sidecar.json")
    sidecar = {
        "gate": "A",
        "provenance": "MODEL",
        "_provenance_note": ("Every entry below was produced by a MODEL reading the source document, "
                             "not by a deterministic rule. It is a SIDECAR: nothing here is written "
                             "into the IR, into an emitted model, into the platform table or into "
                             "coverage_gate.py's inputs, so engine-derived and model-derived "
                             "statements stay distinguishable."),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bundle": bundle,
        "document": manifest["inputs"]["document"],
        "document_sha256": manifest["inputs"]["document_sha256"],
        "platform": raised["platform"],
        "verifier": verdict.get("verifier"),
        "ledger": {"raised": n_raised, "discharged": len(discharged), "outstanding": n_out,
                   "quarantined": len(quarantined), "rejected": len(rejected),
                   "model_supplied": len(flagged), "undecided": len(undecided),
                   "balances": balances},
        "provenance_flagged": [dict(r, provenance="MODEL") for r in flagged],
        # OUTSTANDING AND UNDECIDED, listed separately as well as counted. `unresolved` below is the
        # handover list and these are on it; a reader triaging that list has to be able to tell "the
        # gate found this broken" from "the gate could not tell", and both are in there.
        "undecided": [dict(r, provenance="MODEL") for r in undecided],
        "loop": loop,
        "input_drift": list(drift),
        # The booleans behind that list. `null` means the artifact is not on disk to compare, which is
        # a third answer and is never collapsed into False.
        "input_currency": dict(currency or {}),
        "discharged": [dict(r, provenance="MODEL") for r in discharged],
        "unresolved": ([dict(r, provenance="MODEL") for r in outstanding]
                       + [{"obligation_id": oid, "family": by_family(raised, oid),
                           "verdict": "UNANSWERED", "provenance": "MODEL",
                           "reason": "the verifier did not answer this obligation"}
                          for oid in unanswered]),
        "quarantined": [{"obligation_id": oid, "why": why} for oid, why in quarantined],
        "rejected": [{"obligation_id": oid, "why": why} for oid, why in rejected],
        "notes": verdict.get("notes") or [],
    }
    with open(sidecar_path, "w", encoding="utf-8") as fh:
        json.dump(sidecar, fh, indent=1)
    with open(os.path.join(bundle, "gateA-loop.json"), "w", encoding="utf-8") as fh:
        json.dump(loop, fh, indent=1)
    print(" sidecar       : %s   [provenance MODEL, %d unresolved]"
          % (sidecar_path, len(sidecar["unresolved"])))
    print("-" * W)
    # ---- WHAT THE LOOP NEEDS BACK, and why it is handed over rather than re-derived ---------------
    # The loop above this has to answer three questions the printed report cannot be parsed for
    # reliably: did the DENOMINATOR move between iterations, which obligations changed verdict and in
    # WHICH DIRECTION, and what the stop reason was. Re-deriving any of that by scraping stdout would be
    # the adjacent-verification trap inside the gate -- measuring a copy of the answer instead of the
    # answer. So the adjudicated state is handed back by reference, from the same variables the report
    # was printed from.
    if collect is not None:
        collect.update({
            "iteration": args.iteration,
            "raised_ids": [o["id"] for o in raised["obligations"]],
            "families": {o["id"]: o["family"] for o in raised["obligations"]},
            # EVERY obligation gets a word, and an unanswered one gets `UNANSWERED` rather than being
            # absent -- a missing key would make "not answered this time" indistinguishable from "not
            # raised this time", which is exactly the confusion the denominator assert exists to catch.
            "verdicts": dict({oid: "UNANSWERED" for oid in [o["id"] for o in raised["obligations"]]},
                             **{oid: r["verdict"] for oid, r in rows.items()}),
            "ledger": {"raised": n_raised, "discharged": len(discharged), "outstanding": n_out,
                       "quarantined": len(quarantined), "rejected": len(rejected),
                       "model_supplied": len(flagged), "undecided": len(undecided),
                       "balances": balances},
            "by_family_raised": dict(raised["counts"]),
            "by_family_discharged": {fam: sum(1 for r in discharged if r["family"] == fam)
                                     for fam in FAMILIES},
            "outstanding_ids": ([r["obligation_id"] for r in outstanding] + list(unanswered)),
            "loop": loop,
            "drift": list(drift),
        })
    if not balances:
        # An arithmetic impossibility, so it is a gate defect and not a verdict about the document.
        raise GateAError("LEDGER DOES NOT BALANCE: raised=%d discharged=%d outstanding=%d. This is a "
                         "defect in Gate A, not a finding about the input."
                         % (n_raised, len(discharged), n_out))
    if n_out:
        print(" VERDICT: FAIL — %d obligation(s) OUTSTANDING. The IR does not provably account for"
              % n_out)
        print("          everything this document states. Unresolved list handed over above and in")
        print("          the sidecar. (exit 3)")
        for r in outstanding:
            print("     *** %s [%s] : %s" % (r["obligation_id"], r["family"], r["verdict"]))
        for oid in unanswered:
            print("     *** %s : UNANSWERED" % oid)
        return 3
    print(" VERDICT: every raised obligation is discharged — the IR accounts for every element, link")
    print("          and residue class this document states, and asserts nothing it does not (exit 0)")
    return 0


def by_family(raised, oid):
    for o in raised["obligations"]:
        if o["id"] == oid:
            return o["family"]
    return "?"


# ---------------------------------------------------------------------------------------------
# THE VERIFIER, AS A REAL MODEL CALL — and the isolation had to become MECHANICAL to survive it.
#
# Every Gate A verdict recorded so far came from a sub-agent that was TOLD to read only the bundle.
# `findings/48` says so plainly: "`claude` is not on PATH here, so the ten runs behind this document
# were sub-agent invocations against packed bundles". Instruction-only isolation was adequate for a
# sub-agent inside this conversation. It is NOT adequate for a headless CLI holding a Read tool and a
# filesystem, for two reasons that are properties of the harness rather than of the model:
#
#   1. MANIFEST.json carries the absolute paths of the real table, document, IR and output tree. From
#      any one of them `findings/` is two directory levels away, and `findings/48` IS the answer key.
#      So the verifier's view is built from the manifest's own produced list MINUS the manifest.
#   2. A CLI inherits CLAUDE.md files, auto-memory, skills, plugins, hooks and MCP servers. This
#      project's auto-memory contains the sentence "a packed blind bundle can predate its own platform
#      table, so a correct verifier raises a false alarm" -- which is one of the findings a Gate A
#      verifier is supposed to reach on its own. So the call runs with all of that disabled.
#
# Three layers, and none of them is a request:
#
#   * the VIEW: a directory outside $HOME holding copies of exactly the bundle files a reader may see.
#     It is the process's working directory, so a relative path cannot escape and there is no repo
#     around it to stumble into.
#   * DENY RULES: reads, greps and globs under $HOME are refused by the harness, as are Bash, WebFetch,
#     WebSearch and Task. Measured, not assumed -- a probe asked for a file under $HOME and was denied,
#     and a test in gate_a_test.py asserts the settings this function writes.
#   * the TOOL SET: restricted to Read, Grep, Glob and Write.
#
# The seam stays a shell command on purpose (`--verifier-cmd`), so a CLI, an API call or a sub-agent
# remain interchangeable. This function is one implementation of it, invoked as
# `gate_a.py verifier --bundle {bundle} --verdict {verdict}`, and it is swappable: --cli, --model and
# --verifier-timeout all move without touching the gate.
#
# WHAT IT DELIBERATELY DOES NOT DO: it adds NOTHING to the instructions in the bundle's PROMPT.md.
# `findings/48` had to disclose that round 2's pass on the `getYear() + 1900` trap was confounded by a
# hand-added methodological warning in one prompt. Here the prompt is the bundle's, a test asserts it
# carries no arithmetic/epoch/offset/unit warning, and the CLI prompt below only says where to read and
# where to write. The trap is therefore measured unprompted.
# ---------------------------------------------------------------------------------------------

# Never staged for the verifier. Everything else pack produced is.
# `gateA-loop-run.json` is here for the same reason `verdict.json` is, and it is the loop's version of
# the same hazard: it holds EVERY previous iteration's verdict words plus the flip table. A verifier
# that read it would not be answering the document, it would be negotiating with its own last answer.
VIEW_EXCLUDE = ("MANIFEST.json", "verdict.json", "gateA-sidecar.json", "gateA-loop.json",
                "gateA-loop-run.json", "verifier-run.json", "settings.json")

# CITATIONS ARE RE-READ AGAINST THE ORIGINAL, so these two are staged byte-for-byte and never rewritten.
# A redaction inside them would move a line's content and quarantine correct claims.
VIEW_VERBATIM = ("source_document", "source_document.lines.txt")


def _redact_paths(text):
    """Replace this machine's absolute paths with a marker. Returns (text, [what was replaced]).

    FOUND BY THIS GATE'S OWN TEST, and it is a real hole rather than a tidy-up.
    `coverage_gate.report.txt` is embedded in the bundle verbatim as evidence -- and it prints the
    absolute path of the document, the IR and the output tree. Under instruction-only isolation that
    cost nothing. Handed to a process with a Read tool it is a route to this very file, whose module
    docstring states the frozen fixture's planted defect in so many words. The deny rules already
    refuse everything under $HOME; this closes the same hole a second, independent way, because an
    isolation that rests on one mechanism is an isolation you have not tested.
    """
    hits = []
    home = os.path.realpath(os.path.expanduser("~"))
    # HERE is .../ai/plugin/skills/migration/migrate-objects/actions/etl-aifirst/scripts -- seven
    # levels down from the ai/ subtree root that fixtures (and everything else this gate reads) live
    # under. Longest first, so the repo root is replaced before the home directory inside it.
    repo_root = HERE
    for _ in range(7):
        repo_root = os.path.dirname(repo_root)
    for path, label in sorted(((repo_root, "<repo-root>"),
                               (HERE, "<gate-directory>"), (home, "<home>")),
                              key=lambda p: -len(p[0])):
        if path and path in text:
            text = text.replace(path, label)
            hits.append(label)
    return text, hits

# Substance lives in PROMPT.md, inside the bundle, where it is auditable after the fact. This says
# where to read and where to write, and nothing about how to reason.
CLI_PROMPT = """You are Gate A's verification agent. Your entire evidence base is THIS DIRECTORY.

1. Read `PROMPT.md` here. It states the question, the answer vocabulary and how you are scored. Follow
   it exactly.
2. Read `obligations.json`. Answer EVERY obligation in it. An obligation you do not answer is scored
   OUTSTANDING, so silence is not a safe default in either direction.
3. Write your answer as JSON to `./verdict.json` in this directory, in the schema `PROMPT.md` gives.
   That file is your only output: anything you print instead of writing it is discarded.

Hard constraints: read no file outside this directory — attempts are refused by the harness, and a
refused read is evidence about the harness and not about the document. Do not reason about a wider
repository; there is none reachable. Every verdict-changing claim needs the `doc_locus` / `doc_quote`
pair, and the scorer re-reads that line.
"""

# The harness-level half of the isolation. Deny beats allow, and the view lives outside $HOME by
# construction (asserted below), so denying $HOME does not deny the evidence.
def _view_settings():
    return {
        "permissions": {
            "deny": ["Read(~/**)", "Grep(~/**)", "Glob(~/**)",
                     "Bash", "WebFetch", "WebSearch", "Task", "Edit", "NotebookEdit"],
            "allow": ["Read(./**)", "Grep(./**)", "Glob(./**)", "Write(./verdict.json)"],
        },
    }


def build_verifier_view(bundle, view, extra_exclude=()):
    """Stage the reader-facing bundle files into `view`. Returns (staged, excluded).

    Built from MANIFEST.json's `files` list -- the KNOWN PRODUCED SET -- rather than from
    os.listdir, for the same reason the manifest itself is: a directory listing absorbs whatever
    happens to be lying there, and a bundle that has been scored once holds a verdict and a sidecar.
    A stray file is not staged and is reported.
    """
    home = os.path.realpath(os.path.expanduser("~"))
    if os.path.realpath(view).startswith(home + os.sep):
        # The deny rules refuse $HOME. A view inside it would either be unreadable to the verifier or
        # force the deny list open, and a hole cut in the blindness to make the run work is exactly
        # the trade this gate exists to refuse.
        raise GateAError("the verifier view %s is inside $HOME, where the isolation rules deny reads. "
                         "Use --view-root outside $HOME (the default is the system temp dir)." % view)
    mpath = os.path.join(bundle, "MANIFEST.json")
    if not os.path.isfile(mpath):
        raise GateAError("no MANIFEST.json in %s — pack the bundle first" % bundle)
    with open(mpath, "r", encoding="utf-8") as fh:
        produced = [f["file"] for f in (json.load(fh).get("files") or [])]
    excl = tuple(VIEW_EXCLUDE) + tuple(extra_exclude)
    os.makedirs(view, exist_ok=True)
    staged, excluded = [], []
    for f in produced:
        src = os.path.join(bundle, f)
        if f in excl:
            excluded.append(f)
            continue
        if not os.path.isfile(src):
            excluded.append("%s (listed by the manifest and not on disk)" % f)
            continue
        entry = {"file": f, "bytes": os.path.getsize(src), "sha256": _sha(src)[:16]}
        dst = os.path.join(view, f)
        # A manifest entry may be a NESTED relative path -- Gate B stages a whole emitted dbt project
        # -- so the view mirrors the bundle's shape rather than flattening it. Flattening would collide
        # two models with the same basename in different directories.
        os.makedirs(os.path.dirname(dst) or view, exist_ok=True)
        if f.startswith("source_document"):
            shutil.copyfile(src, dst)
            with open(src, "r", encoding="utf-8", errors="replace") as fh:
                body = fh.read()
            _, hits = _redact_paths(body)
            if hits:
                # NOT redacted, and said out loud: the document is the citation vocabulary and moving
                # a byte in it quarantines correct claims. If a source document ever really carries
                # this machine's paths, that is a fact about the corpus and it belongs in the record.
                entry["UNREDACTED_PATHS_IN_A_VERBATIM_FILE"] = hits
        else:
            with open(src, "r", encoding="utf-8", errors="replace") as fh:
                body = fh.read()
            body, hits = _redact_paths(body)
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(body)
            if hits:
                entry["redacted"] = hits
                entry["sha256_as_staged"] = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
        staged.append(entry)
    # Withheld whether or not the manifest happens to list them: MANIFEST.json never is, and a
    # previous round's verdict or sidecar is present exactly when this bundle has been scored before.
    for f in excl:
        if f not in excluded and os.path.isfile(os.path.join(bundle, f)):
            excluded.append(f)
    return staged, excluded


def isolated_model_call(gate, bundle, verdict_dest, cli_prompt, *, cli=None, model=None,
                        timeout=900, view=None, view_root=None, keep_view=False,
                        max_budget_usd=None, extra_exclude=(), record_name="verifier-run.json",
                        what="a verification model call over an isolated bundle view",
                        obligations_override=None):
    """Run ONE headless model call whose whole world is a view of `bundle`. Returns the run record.

    SHARED BY GATE A AND GATE B on purpose. The isolation is the part that makes either gate's result
    mean anything, and two copies of it would drift -- `findings/43`'s staging error was one gate's
    staging being wrong in a way nobody could reconstruct afterwards. One implementation, one set of
    tests, one run record format.

    `obligations_override`, when given, replaces the view's `obligations.json` with this object AFTER
    staging and BEFORE the call -- the seam batching uses to hand one call ONE BATCH of the raised set
    rather than all of it, without touching the real bundle or PROMPT.md. The `staged` audit entry for
    `obligations.json` is corrected to describe what was actually shown, not what pack() wrote, because
    an isolation record that lists the wrong bytes for the one file batching changes is worse than no
    record at all.
    """
    cli = cli or os.environ.get("GATE_VERIFIER_CLI") or "claude"
    resolved = shutil.which(cli) or (cli if os.path.isfile(cli) else None)
    if resolved is None:
        raise GateAError("verifier CLI %r not found. Pass --cli /path/to/claude or set "
                         "GATE_VERIFIER_CLI. A gate that cannot reach its verifier is UNMEASURED, "
                         "which is a different claim from clean." % cli)

    bundle = os.path.abspath(bundle)
    view = (os.path.abspath(view) if view else
            os.path.join(view_root or tempfile.gettempdir(),
                         "gate%s-view-%s-%d" % (gate, os.path.basename(bundle.rstrip(os.sep)),
                                                os.getpid())))
    if os.path.isdir(view):
        shutil.rmtree(view)
    staged, excluded = build_verifier_view(bundle, view, extra_exclude=extra_exclude)

    if obligations_override is not None:
        override_path = os.path.join(view, "obligations.json")
        with open(override_path, "w", encoding="utf-8") as fh:
            json.dump(obligations_override, fh, indent=1)
        for entry in staged:
            if entry["file"] == "obligations.json":
                entry["bytes"] = os.path.getsize(override_path)
                entry["sha256"] = _sha(override_path)[:16]
                entry["overridden_for_batching"] = True

    settings_path = os.path.join(view, "settings.json")
    with open(settings_path, "w", encoding="utf-8") as fh:
        json.dump(_view_settings(), fh, indent=1)

    argv = [resolved, "-p", cli_prompt,
            "--tools", "Read,Grep,Glob,Write",
            "--settings", settings_path,
            "--permission-mode", "acceptEdits",
            # ALL INHERITED CONFIGURATION OFF. CLAUDE.md, auto-memory, skills, plugins, hooks, MCP
            # servers and custom agents. This is a blindness requirement, not tidiness: this project's
            # own auto-memory states one of the findings a verifier is meant to reach unaided.
            "--safe-mode",
            "--output-format", "json"]
    if model:
        argv += ["--model", model]
    if max_budget_usd:
        argv += ["--max-budget-usd", str(max_budget_usd)]

    started = datetime.now(timezone.utc)
    t0 = time.time()
    try:
        proc = subprocess.run(argv, cwd=view, capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=timeout)
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as ex:
        rc, out, err, timed_out = 124, (ex.stdout or ""), (ex.stderr or ""), True
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", "replace")
    elapsed = round(time.time() - t0, 1)

    try:
        meta = json.loads(out)
    except Exception:
        meta = {}

    produced_verdict = os.path.join(view, "verdict.json")
    dest = os.path.abspath(verdict_dest)
    wrote, verdict_source = False, None
    if os.path.isfile(produced_verdict):
        try:
            with open(produced_verdict, "r", encoding="utf-8") as fh:
                json.load(fh)
            shutil.copyfile(produced_verdict, dest)
            wrote, verdict_source = True, "verdict.json written in the view"
        except Exception as ex:
            verdict_source = "verdict.json in the view is not JSON: %s" % ex

    record = {
        "gate": gate,
        "what": what,
        "cli": resolved,
        "argv": argv[:1] + ["-p", "<CLI_PROMPT>"] + argv[3:],
        "model_requested": model,
        "model_used": sorted((meta.get("modelUsage") or {}).keys()) or None,
        "model_usage": meta.get("modelUsage"),
        "input_tokens": sum((u.get("inputTokens") or u.get("input_tokens") or 0)
                            for u in (meta.get("modelUsage") or {}).values()),
        "output_tokens": sum((u.get("outputTokens") or u.get("output_tokens") or 0)
                             for u in (meta.get("modelUsage") or {}).values()),
        "cache_read_input_tokens": sum((u.get("cacheReadInputTokens") or
                                        u.get("cache_read_input_tokens") or 0)
                                       for u in (meta.get("modelUsage") or {}).values()),
        "cache_creation_input_tokens": sum((u.get("cacheCreationInputTokens") or
                                            u.get("cache_creation_input_tokens") or 0)
                                           for u in (meta.get("modelUsage") or {}).values()),
        "started_utc": started.isoformat(timespec="seconds"),
        "elapsed_s": elapsed,
        "exit_code": rc,
        "timed_out": timed_out,
        "session_id": meta.get("session_id"),
        "num_turns": meta.get("num_turns"),
        "total_cost_usd": meta.get("total_cost_usd"),
        "permission_denials": meta.get("permission_denials"),
        # AND WHAT THAT FIELD DOES NOT MEAN, because an empty list here reads exactly like "the
        # verifier never tried to leave the view" and it is NOT that claim. MEASURED with a probe:
        # a call under these same settings was told to read `~/.claude/CLAUDE.md` and
        # `~/.claude/settings.json`, BOTH READS WERE REFUSED by the harness -- and
        # `permission_denials` came back `[]`. So the deny rules work and this field does not record
        # them. Ten Gate A/B calls reported `[]`; that is evidence about the field, not about the
        # isolation. The isolation's evidence is the VIEW (this record lists every file it held) plus
        # `_view_settings()`, which a test asserts.
        "_permission_denials_means": ("EMPTY DOES NOT MEAN NO ATTEMPT. A probe under these settings "
                                     "had two $HOME reads refused by the harness and this field "
                                     "still came back []. Read the `isolation.staged` list for what "
                                     "the verifier could see; do not read this field as a negative "
                                     "result."),
        "stderr_tail": (err or "")[-2000:],
        "result_text_tail": (meta.get("result") or out or "")[-2000:],
        "verdict_written": wrote,
        "verdict_source": verdict_source,
        "verdict_path": dest if wrote else None,
        # THE AUDITABLE PART, and findings/43's lesson: a staging mistake has to land in the record
        # rather than be reconstructed from memory afterwards.
        "isolation": {
            "view": view,
            "cwd_of_the_call": view,
            "staged": staged,
            "excluded_from_the_view": excluded,
            "settings": _view_settings(),
            "tools": "Read,Grep,Glob,Write",
            "inherited_configuration": "disabled via --safe-mode (CLAUDE.md, auto-memory, skills, "
                                       "plugins, hooks, MCP servers, custom agents)",
            "prompt_added_by_this_wrapper": cli_prompt,
            "_note": ("The wrapper adds NO reasoning instruction. Round 2's pass on the getYear trap "
                      "was confounded by a hand-added warning in one prompt; the only instructions "
                      "here are the bundle's PROMPT.md plus where to read and where to write."),
        },
    }
    with open(os.path.join(bundle, record_name), "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1)

    print("-" * W)
    print(" verifier      : %s  [%s]" % (resolved, ", ".join(record["model_used"] or ["model?"])))
    print(" view          : %s   [%d file(s) staged, %d withheld: %s]"
          % (view, len(staged), len(excluded), ", ".join(excluded) or "none"))
    print(" call          : exit %s in %ss%s  turns=%s cost=%s"
          % (rc, elapsed, "  *** TIMED OUT" if timed_out else "", meta.get("num_turns"),
             meta.get("total_cost_usd")))
    print(" run record    : %s" % os.path.join(bundle, record_name))
    if not keep_view:
        shutil.rmtree(view, ignore_errors=True)
        print(" view removed  : the run record above lists every file it held, with hashes")
    if not wrote:
        raise GateAError("the verifier wrote no usable verdict.json (%s). exit=%s%s"
                         % (verdict_source or "no file produced", rc,
                            "; TIMED OUT" if timed_out else ""))
    print(" verdict       : %s" % dest)
    return record


def verifier(args):
    """One implementation of --verifier-cmd: a headless model call over an isolated bundle view."""
    isolated_model_call("A", args.bundle, args.verdict, CLI_PROMPT, cli=args.cli, model=args.model,
                        timeout=args.verifier_timeout, view=args.view, view_root=args.view_root,
                        keep_view=args.keep_view, max_budget_usd=args.max_budget_usd,
                        what="the verifier half of Gate A, as a real model call")
    return 0


# ---------------------------------------------------------------------------------------------
# BATCHING — see the module docstring section of the same name for the measured cliff this answers
# and the merge rule. Everything below is the implementation of that rule: plan the batches, run one
# isolated call per batch, merge the fragments, and never let a partial failure pass for silence.
# ---------------------------------------------------------------------------------------------

def _obligation_ids_in_families_order(obligations):
    """Cover `obligations` exactly once each, ordered by FAMILIES (within-family encounter order)."""
    grouped = {fam: [] for fam in FAMILIES}
    unknown = []
    for o in obligations:
        fam = o.get("family")
        if fam in grouped:
            grouped[fam].append(o["id"])
        else:
            unknown.append("%s(%s)" % (o.get("id"), fam))
    if unknown:
        raise GateAError(
            "BATCH PLAN SAW UNKNOWN FAMILY ON: %s. Known families are %s."
            % (unknown, list(FAMILIES)))
    return [oid for fam in FAMILIES for oid in grouped[fam]]


def plan_batches(obligations, batch_size=None):
    """Split `obligations` into bounded batches at FAMILY boundaries, in FAMILIES order.

    This is the boundary the measured cliff actually failed at: one call answered every ELEMENT
    obligation inside its budget and only exhausted it trying to APPEND the next family into the same
    re-emitted response. One call per family removes exactly that append. `batch_size`, when given,
    additionally splits a family that is itself larger than it into fixed-size chunks, so a single
    family on a bigger document cannot reproduce the same cliff one level down.

    Family order is always FAMILIES (ELEMENT -> LINK -> RESIDUE -> IR_UNMATCHED), never first-seen
    discovery order: an interleaved obligations list still batches ELEMENT before LINK. Within a
    family, encounter order from the input is preserved. Unknown families are a planner defect.

    Returns a list of batches, each `{"index", "family", "chunk", "obligation_ids", "obligations"}`,
    in the order they should be called. The caller (`plan_batches_from_bundle`) asserts the
    concatenation of every batch's `obligation_ids` equals the raised set exactly once each in
    FAMILIES order -- the honest denominator this function must not be able to violate by
    construction, and is checked rather than trusted because a planner defect must read as a
    could-not-run, not as a clean sheet.
    """
    grouped = {fam: [] for fam in FAMILIES}
    unknown = []
    for o in obligations:
        fam = o.get("family")
        if fam in grouped:
            grouped[fam].append(o)
        else:
            unknown.append("%s(%s)" % (o.get("id"), fam))
    if unknown:
        raise GateAError(
            "BATCH PLAN SAW UNKNOWN FAMILY ON: %s. Known families are %s."
            % (unknown, list(FAMILIES)))
    batches = []
    for fam in FAMILIES:
        items = grouped[fam]
        if not items:
            continue
        size = batch_size if (batch_size and batch_size > 0) else len(items)
        for start in range(0, len(items), size):
            chunk = items[start:start + size]
            batches.append({
                "index": len(batches),
                "family": fam,
                "chunk": start // size,
                "obligation_ids": [o["id"] for o in chunk],
                "obligations": chunk,
            })
    return batches


def _assert_honest_denominator(obligations, batches):
    """The batch plan must cover the raised set exactly once each, in FAMILIES order. Never trusted."""
    want = _obligation_ids_in_families_order(obligations)
    got = [oid for b in batches for oid in b["obligation_ids"]]
    if got == want:
        return
    want_set, got_set = set(want), set(got)
    missing = [i for i in want if i not in got_set]
    extra = [i for i in got if i not in want_set]
    dupes = sorted({i for i in got if got.count(i) > 1})
    raise GateAError(
        "BATCH PLAN DOES NOT COVER THE RAISED SET EXACTLY ONCE EACH: %d raised, %d planned "
        "(missing=%s extra=%s duplicated=%s). This is a defect in the batch planner, not a verdict "
        "about the document." % (len(want), len(got), missing, extra, dupes))


def plan_batches_from_bundle(bundle, batch_size=None):
    """Read the packed `obligations.json`, plan its batches, and assert the denominator before any
    verifier is called. Returns (packed, batches)."""
    with open(os.path.join(bundle, "obligations.json"), "r", encoding="utf-8") as fh:
        packed = json.load(fh)
    obligations = packed.get("obligations") or []
    batches = plan_batches(obligations, batch_size=batch_size)
    _assert_honest_denominator(obligations, batches)
    return packed, batches


def _batch_obligations_payload(packed, batch):
    """The obligations.json ONE batch's verifier is shown: same shape pack() writes, `obligations`
    narrowed to this batch, and a `batch` block naming the narrowing so a verifier reading this file on
    its own is never left guessing whether it is looking at the whole document's obligations."""
    payload = dict(packed)
    payload["obligations"] = batch["obligations"]
    payload["counts"] = {fam: sum(1 for o in batch["obligations"] if o["family"] == fam)
                         for fam in FAMILIES}
    payload["batch"] = {
        "index": batch["index"], "family": batch["family"], "chunk": batch["chunk"],
        "obligations_in_this_batch": len(batch["obligation_ids"]),
        "obligations_in_the_full_raised_set": len(packed.get("obligations") or []),
        "_note": ("This obligations.json is ONE BATCH of the document's full raised set, staged this "
                 "way so one verifier call's answer stays inside its output-token budget. Answer "
                 "every obligation THIS file lists and nothing else -- exactly as a single-shot run "
                 "would, just over a narrower question set. The obligations NOT in this batch are "
                 "each the subject of a separate, equally isolated call."),
    }
    return payload


def _run_one_batch(bundle, batch, packed, *, cli, model, timeout, view_root, keep_view,
                   max_budget_usd):
    """One bounded, isolated verifier call over ONE batch's obligations. Returns a fragment record.

    Never raises for an ORDINARY verifier failure (timeout, no verdict, malformed JSON) -- that is a
    LOUD, NAMED batch failure the caller reports and the merge accounts for, not a could-not-run for
    the whole gate: the other batches' answers are still real evidence, and discarding them because
    one call misbehaved would be a bigger loss than reporting the gap honestly.
    """
    bundle = os.path.abspath(bundle)
    frag_verdict_path = os.path.join(bundle, "verdict.batch%d.json" % batch["index"])
    view = os.path.join(view_root or tempfile.gettempdir(),
                        "gateA-batch%d-view-%s-%d" % (batch["index"],
                                                      os.path.basename(bundle.rstrip(os.sep)),
                                                      os.getpid()))
    override = _batch_obligations_payload(packed, batch)
    try:
        record = isolated_model_call(
            "A", bundle, frag_verdict_path, CLI_PROMPT, cli=cli, model=model, timeout=timeout,
            view=view, view_root=view_root, keep_view=keep_view, max_budget_usd=max_budget_usd,
            record_name="verifier-run.batch%d.json" % batch["index"],
            what="Gate A batch %d (family=%s chunk=%d, %d obligation(s))"
                 % (batch["index"], batch["family"], batch["chunk"], len(batch["obligation_ids"])),
            obligations_override=override)
    except GateAError as ex:
        return {"batch": batch, "verdict_path": frag_verdict_path, "verdict": None,
                "error": str(ex), "run_record": None}
    try:
        with open(frag_verdict_path, "r", encoding="utf-8") as fh:
            verdict = json.load(fh)
    except Exception as ex:
        return {"batch": batch, "verdict_path": frag_verdict_path, "verdict": None,
                "error": "batch %d verdict fragment unreadable: %s: %s"
                        % (batch["index"], type(ex).__name__, ex), "run_record": record}
    return {"batch": batch, "verdict_path": frag_verdict_path, "verdict": verdict,
            "error": None, "run_record": record}


def merge_batch_fragments(packed, batches, fragments):
    """Combine every batch's verdict fragment into ONE verdict, plus an audit record naming any batch
    that did not answer. See the module docstring's BATCHING section for the merge rule this
    implements: concatenate successful batches' in-scope claims; a failed batch contributes nothing;
    a claim whose obligation_id is not in that batch's obligation_ids is dropped (never allowed to
    discharge another batch's unanswered set).
    Returns (merged_verdict, audit_record).
    """
    if len(fragments) != len(batches):
        raise GateAError(
            "BATCH MERGE FRAGMENT COUNT MISMATCH: %d fragment(s) for %d batch(es). This is a defect "
            "in the batch runner, not a verdict about the document."
            % (len(fragments), len(batches)))
    combined_claims = []
    batch_report = []
    verifier_ids = []
    ok = failed = 0
    for frag in fragments:
        b = frag["batch"]
        err = frag["error"]
        claims = None
        if err is None:
            v = frag["verdict"] or {}
            c = v.get("claims")
            if not isinstance(c, list):
                err = "batch %d verdict fragment has no `claims` array" % b["index"]
            else:
                claims = c
        if err is not None:
            failed += 1
            batch_report.append({"index": b["index"], "family": b["family"], "chunk": b["chunk"],
                                 "obligation_ids": b["obligation_ids"], "status": "BATCH_FAILED",
                                 "error": err})
            continue
        ok += 1
        owned = set(b["obligation_ids"])
        kept = 0
        dropped = []
        for c in claims:
            oid = c.get("obligation_id")
            if oid not in owned:
                dropped.append(oid)
                continue
            combined_claims.append(dict(c, _batch_index=b["index"], _batch_family=b["family"]))
            kept += 1
        vid = (frag["verdict"] or {}).get("verifier")
        if vid:
            verifier_ids.append(str(vid))
        rr = frag.get("run_record") or {}
        row = {"index": b["index"], "family": b["family"], "chunk": b["chunk"],
               "obligation_ids": b["obligation_ids"], "status": "ANSWERED",
               "claims_written": kept, "verifier": vid,
               "cost_usd": rr.get("total_cost_usd"), "elapsed_s": rr.get("elapsed_s"),
               "input_tokens": rr.get("input_tokens"), "output_tokens": rr.get("output_tokens"),
               "cache_read_input_tokens": rr.get("cache_read_input_tokens"),
               "cache_creation_input_tokens": rr.get("cache_creation_input_tokens")}
        if dropped:
            row["claims_dropped_out_of_batch"] = dropped
        batch_report.append(row)
    merged = {
        "verifier": ("BATCHED[" + ",".join(verifier_ids) + "]") if verifier_ids
                    else "BATCHED[no successful batch]",
        "claims": combined_claims,
        "notes": ["merged from %d batch(es) covering %d obligation(s) total: %d answered, %d failed"
                 % (len(fragments), len(packed.get("obligations") or []), ok, failed)],
    }
    audit = {
        "gate": "A",
        "batches": batch_report,
        "batches_ok": ok,
        "batches_failed": failed,
        "raised_total": len(packed.get("obligations") or []),
        "merge_rule": ("Concatenate every successful batch's in-scope `claims` -- a claim counts "
                      "only when its obligation_id is in that batch's obligation_ids; out-of-batch "
                      "ids are dropped so one call cannot discharge another batch's unanswered set. "
                      "A batch with no usable fragment contributes NOTHING: never a manufactured "
                      "claim standing in for a missing answer. Its obligations fall through to "
                      "score()'s own unanswered path and are scored OUTSTANDING -- the same fate as "
                      "an obligation a single verifier stayed silent on. What batching adds is which "
                      "OUTSTANDING obligations are that way because a model judged them unresolved, "
                      "and which are that way because the call that owned them never answered at "
                      "all: `batches` above keeps the two apart."),
    }
    return merged, audit


def batched_run(args):
    """Pack once, batch the verifier across multiple bounded calls, merge, score. Single pass --
    `run --max-iterations N` is the iterate-to-convergence loop; composing the two is future work, see
    the module docstring's BATCHING section."""
    bundle = os.path.abspath(args.bundle)
    rc = pack(args)
    if rc:
        raise GateAError("pack failed with %d" % rc)
    packed, batches = plan_batches_from_bundle(bundle, batch_size=getattr(args, "batch_size", None))

    print("#" * W)
    print(" GATE A -- BATCHED VERIFIER CALLS")
    print("#" * W)
    print(" %d obligation(s) split into %d batch(es):"
          % (len(packed.get("obligations") or []), len(batches)))
    for b in batches:
        print("   batch %d  family=%-12s chunk=%d  %d obligation(s)"
              % (b["index"], b["family"], b["chunk"], len(b["obligation_ids"])))

    parallelism = max(1, int(getattr(args, "parallelism", 4) or 4))
    print(" parallelism   : %d worker(s) (bounded; results merge in batch-index order)" % parallelism)
    fragments_by_index = {}
    with ThreadPoolExecutor(max_workers=parallelism, thread_name_prefix="gateA") as pool:
        future_to_batch = {}
        for b in batches:
            print("-" * W)
            print(" batch %d/%d  family=%s  chunk=%d  (%d obligation(s)) -- queued"
                  % (b["index"] + 1, len(batches), b["family"], b["chunk"],
                     len(b["obligation_ids"])))
            future = pool.submit(
                _run_one_batch, bundle, b, packed, cli=args.cli, model=args.model,
                timeout=args.verifier_timeout, view_root=args.view_root,
                keep_view=args.keep_view, max_budget_usd=args.max_budget_usd)
            future_to_batch[future] = b
        for future in as_completed(future_to_batch):
            b = future_to_batch[future]
            try:
                frag = future.result()
            except Exception as ex:
                frag = {"batch": b, "verdict_path": None, "verdict": None,
                        "error": "parallel worker raised %s: %s" % (type(ex).__name__, ex),
                        "run_record": None}
            fragments_by_index[b["index"]] = frag
            state = "FAILED" if frag["error"] else "answered"
            print(" batch %d/%d  family=%s -- %s" %
                  (b["index"] + 1, len(batches), b["family"], state))
            if frag["error"]:
                print(" *** BATCH %d FAILED: %s" % (b["index"], frag["error"]))
                print("     obligation(s) affected (scored OUTSTANDING below, NOT silently dropped): %s"
                      % ", ".join(b["obligation_ids"]))
    fragments = [fragments_by_index[b["index"]] for b in batches]

    merged, audit = merge_batch_fragments(packed, batches, fragments)
    audit_path = os.path.join(bundle, "gateA-batch-merge.json")
    with open(audit_path, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1)

    if batches and audit["batches_ok"] == 0:
        # EVERY batch failed -- missing CLI, auth failure, or every call simply erroring out. There
        # is no verifier verdict for ANY obligation, so this is a could-not-run condition, not a
        # verdict: scoring an empty merge would report every obligation OUTSTANDING for a document
        # nothing actually examined. Raise before score() runs so no ledger line is ever printed --
        # the same contract the plain (non-batched) could-not-run path already gives the driver.
        print("#" * W)
        print(" *** ALL %d BATCH(ES) FAILED -- named above, one at a time." % len(batches))
        print("     No verifier verdict was produced for ANY obligation. See %s." % audit_path)
        raise GateAError(
            "all %d batch(es) failed -- no verifier verdict was produced for any obligation; see %s"
            % (len(batches), audit_path))

    if audit["batches_failed"]:
        print("#" * W)
        print(" *** %d OF %d BATCH(ES) FAILED -- named above, one at a time." % (audit["batches_failed"],
                                                                                 len(batches)))
        print("     Their obligations have no claim to adjudicate and score OUTSTANDING below, for a")
        print("     DIFFERENT reason than a model judging them unresolved. See gateA-batch-merge.json.")

    merged_path = os.path.join(bundle, "verdict.json")
    with open(merged_path, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=1)
    print(" merge record  : %s" % audit_path)

    args.verdict = merged_path
    args.sidecar = getattr(args, "sidecar", None)
    args.iteration = getattr(args, "iteration", 1) or 1
    args.max_iterations = getattr(args, "max_iterations", 1) or 1
    return score(args)


DENOMINATOR_DRIFT_MARKER = "*** GATE A DEFECT: DENOMINATOR DRIFT"
LOOP_ABORTED_MARKER = "*** GATE A LOOP ABORTED"


def _one_pass(args, bundle, verdict_path):
    """Pack, call the verifier, score. Returns (rc, collect, packed_ids, call_seconds, run_record)."""
    rc = pack(args)
    if rc:
        raise GateAError("pack failed with %d" % rc)
    packed_ids = _packed_obligation_ids(bundle)
    if not args.verifier_cmd:
        print("-" * W)
        print(" NO --verifier-cmd GIVEN. The bundle is packed and the gate stops here rather than")
        print(" pretending a verdict. This is not a pass: an unrun gate is UNMEASURED, which is a")
        print(" different claim from clean, and conflating them is the defect this project keeps")
        print(" finding. Exit 1 (could not run).")
        raise GateAError("no verifier configured; bundle packed at %s" % bundle)
    cmd = args.verifier_cmd.replace("{bundle}", bundle).replace("{verdict}", verdict_path)
    print("-" * W)
    print(" verifier      : %s" % cmd)
    t0 = time.time()
    proc = subprocess.run(cmd, shell=True)
    call_s = round(time.time() - t0, 1)
    if proc.returncode != 0:
        raise GateAError("verifier command exited %d" % proc.returncode)
    if not os.path.isfile(verdict_path):
        raise GateAError("verifier command wrote no %s" % verdict_path)
    args.verdict = verdict_path
    collect = {}
    rc = score(args, collect=collect)
    # The default verifier writes this; a stand-in `--verifier-cmd` need not, and the fields are then
    # reported as null rather than as zero. A fabricated cost is worse than an absent one.
    run_record = {}
    rr = os.path.join(bundle, "verifier-run.json")
    if os.path.isfile(rr):
        try:
            with open(rr, "r", encoding="utf-8") as fh:
                run_record = json.load(fh)
        except Exception:
            run_record = {}
    return rc, collect, packed_ids, call_s, run_record


def _archive_iteration(bundle, iteration):
    """Keep each iteration's verdict, sidecar, obligations and run record.

    In a SUBDIRECTORY, and that is load-bearing rather than tidy: `build_verifier_view` stages the
    manifest's produced file list, which is flat, so nothing under here can reach a verifier's view --
    and an archive of previous ANSWERS reaching the next iteration's view is precisely the leak that
    makes a loop into an agreement.
    """
    dest = os.path.join(bundle, "iterations", "iter%d" % iteration)
    os.makedirs(dest, exist_ok=True)
    kept = []
    for f in ("obligations.json", "verdict.json", "gateA-sidecar.json", "verifier-run.json",
              "PREVIOUS_UNRESOLVED.json"):
        src = os.path.join(bundle, f)
        if os.path.isfile(src):
            shutil.copyfile(src, os.path.join(dest, f))
            kept.append(f)
    return dest, kept


def run(args):
    bundle = os.path.abspath(args.bundle)
    verdict_path = os.path.join(bundle, "verdict.json")
    max_it = args.max_iterations if (args.max_iterations and args.max_iterations > 0) else 1
    asked_carry_forward = bool(getattr(args, "carry_forward", False))
    records = []            # one entry per completed iteration
    history = []            # what `_stop_reason` compares against; the loop owns it, see that function
    rc = 0
    aborted = None
    t_run = time.time()

    for it in range(1, max_it + 1):
        args.iteration = it
        # ITERATION 1 IS BLIND, EVERY LATER ITERATION IS NOT, and that asymmetry is the loop. Packing
        # clears the previous answer by default because a verifier reading last round's verdict is
        # agreeing rather than verifying; `--carry-forward` keeps the previous UNRESOLVED list only, in a
        # file named so it cannot be mistaken for evidence about the document. Without it a second pass
        # is a re-run and measures verifier variance, not convergence.
        args.carry_forward = asked_carry_forward or it > 1
        args.loop_history = list(history)
        if max_it > 1:
            print("#" * W)
            print(" GATE A LOOP — ITERATION %d of %d%s"
                  % (it, max_it, "" if it == 1 else "   [previous unresolved list carried forward]"))
            print("#" * W)
        try:
            rc, collect, packed_ids, call_s, run_record = _one_pass(args, bundle, verdict_path)
        except GateAError as ex:
            if not records:
                raise            # nothing was ever scored: the plain could-not-run case, unchanged
            # A FAILURE PART-WAY THROUGH A LOOP IS A THIRD STATE the single-pass gate did not have, and
            # it must not read as either of the other two. A ledger line has already been printed, so
            # the driver would otherwise report the last completed iteration as if it were final. Say
            # what happened, keep the last complete ledger, and mark the convergence UNMEASURED.
            aborted = "iteration %d could not run: %s" % (it, ex)
            print("#" * W)
            print(" %s AFTER ITERATION %d OF %d" % (LOOP_ABORTED_MARKER, it - 1, max_it))
            print(" %s" % aborted)
            print(" The ledger from iteration %d above still stands -- it was scored in full. What is"
                  % (it - 1))
            print(" UNMEASURED is convergence: this run cannot say whether another pass would have")
            print(" closed the outstanding list, and it is not reporting that it would not.")
            break

        rec = {"iteration": it, "packed_ids": packed_ids, "scored_ids": collect["raised_ids"],
               "verdicts": collect["verdicts"], "families": collect["families"],
               "ledger": collect["ledger"], "by_family_raised": collect["by_family_raised"],
               "by_family_discharged": collect["by_family_discharged"],
               "outstanding_ids": collect["outstanding_ids"],
               "stop_reason": collect["loop"]["stop_reason"],
               "stop_detail": collect["loop"]["stop_detail"],
               "carry_forward": args.carry_forward,
               "exit_code": rc,
               "verifier_seconds": call_s,
               "model_call": {"cost_usd": run_record.get("total_cost_usd"),
                              "elapsed_s": run_record.get("elapsed_s"),
                              "num_turns": run_record.get("num_turns"),
                              "model_used": run_record.get("model_used"),
                              "session_id": run_record.get("session_id")},
               "input_drift": collect["drift"]}
        rec["flips"] = (flip_report(records[-1]["verdicts"], rec["verdicts"], rec["families"])
                        if records else None)
        records.append(rec)
        history = collect["loop"]["iterations"]
        _archive_iteration(bundle, it)

        # ---- THE DENOMINATOR, CHECKED BEFORE ANYTHING ELSE IS BELIEVED --------------------------
        same_pass = packed_vs_scored_drift(rec)
        across = denominator_drift(records)
        if same_pass or across:
            print("#" * W)
            print(" %s" % DENOMINATOR_DRIFT_MARKER)
            print("#" * W)
            print(" Obligations are raised DETERMINISTICALLY from the document before any verifier")
            print(" runs, so the raised set must be identical in every iteration of one run AND")
            print(" identical between the set the verifier was ASKED and the set the scorer GRADED.")
            print(" One of those does not hold, so a ledger above is measuring a different question")
            print(" than another, and a fall in outstanding here is arithmetic, not convergence.")
            for d in across:
                print("   iteration %s: raised %d -> %d" % (d["iteration"], d["raised_at_iteration_1"],
                                                            d["raised_now"]))
                for oid in d["added"]:
                    print("     ADDED at iteration %s   : %s" % (d["iteration"], oid))
                for oid in d["dropped"]:
                    print("     DROPPED at iteration %s : %s" % (d["iteration"], oid))
            if same_pass:
                print("   iteration %s: the verifier's question set and the scorer's differ"
                      % same_pass["iteration"])
                for oid in same_pass["only_in_the_verifier_s_question_set"]:
                    print("     asked but not graded : %s" % oid)
                for oid in same_pass["only_in_the_scorer_s_set"]:
                    print("     graded but not asked : %s" % oid)
            print(" This is a DEFECT IN GATE A OR A MOVING INPUT, not a finding about the document.")
            print(" Reported as could-not-run (exit 1) so nothing downstream reads it as a verdict.")
            _write_loop_record(bundle, records, max_it, t_run, aborted,
                               denominator_drift=across, packed_vs_scored=same_pass)
            raise GateAError(
                "the raised set is not stable: %s — see the DENOMINATOR DRIFT block above"
                % " and ".join(
                    ([("it changed between iterations of one run (iteration %s)"
                       % ", ".join(str(d["iteration"]) for d in across))] if across else [])
                    + (["the verifier was asked a different set from the one the scorer graded "
                        "(iteration %s)" % same_pass["iteration"]] if same_pass else [])))

        stop = rec["stop_reason"]
        if stop != "OPEN":
            break               # CONVERGED, NO_PROGRESS or EXHAUSTED_ITERATIONS: all terminal

    _report_loop(records, max_it, t_run, aborted)
    _write_loop_record(bundle, records, max_it, t_run, aborted)
    return rc


def _loop_totals(records, t_run):
    costs = [r["model_call"]["cost_usd"] for r in records if r["model_call"]["cost_usd"] is not None]
    return {"iterations_used": len(records),
            "wall_clock_s": round(time.time() - t_run, 1),
            "verifier_seconds": round(sum(r["verifier_seconds"] for r in records), 1),
            # None, not 0, when no iteration reported one: a stand-in verifier has no cost and saying
            # `$0.00` would read as a measurement.
            "model_cost_usd": (round(sum(costs), 4) if costs else None),
            "model_calls_with_a_cost": len(costs)}


def _report_loop(records, max_it, t_run, aborted):
    """The loop's own report: the ledger at every iteration, and the DIRECTION of every flip."""
    if not records:
        return
    tot = _loop_totals(records, t_run)
    print("#" * W)
    print(" GATE A LOOP — %d ITERATION(S) OF %d" % (len(records), max_it))
    print("#" * W)
    for r in records:
        led = r["ledger"]
        print(" iteration %d    : raised=%d discharged=%d outstanding=%d quarantined=%d "
              "model_supplied=%d  stop=%s%s"
              % (r["iteration"], led["raised"], led["discharged"], led["outstanding"],
                 led["quarantined"], led["model_supplied"], r["stop_reason"],
                 "  [carry-forward]" if r["carry_forward"] else "  [blind]"))
    # ---- THE DENOMINATOR ASSERTION, PRINTED WHETHER OR NOT IT FIRED --------------------------------
    # A check that speaks only on failure cannot be seen to have run, and this project has shipped four
    # gates that could not fail. So the passing case gets a line too.
    ids = records[0]["scored_ids"]
    print(" denominator   : IDENTICAL across all %d iteration(s) — %d obligation(s), sha256 %s"
          % (len(records), len(ids),
             hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()[:16]))
    print("                 asserted, not assumed: the raised set is recomputed from the document")
    print("                 every iteration and compared against iteration 1's, ids and order.")
    # ---- FLIPS, BY DIRECTION AND BY FAMILY --------------------------------------------------------
    if len(records) == 1:
        print(" flips         : none measurable — one iteration. A flip is a change BETWEEN")
        print("                 iterations, so a single pass reports no direction rather than zero.")
    for r in records[1:]:
        f = r["flips"]
        t = f["totals"]
        print(" flips %d->%d     : TOWARD_DISCHARGED %d  TOWARD_OUTSTANDING %d  LATERAL %d"
              % (r["iteration"] - 1, r["iteration"], t["TOWARD_DISCHARGED"],
                 t["TOWARD_OUTSTANDING"], t["LATERAL"]))
        for fam in FAMILIES:
            c = f["by_family"][fam]
            if any(c.values()):
                print("                 %-4s %-13s ->discharged %d  ->outstanding %d  lateral %d"
                      % (FAMILY_TAG[fam], fam, c["TOWARD_DISCHARGED"], c["TOWARD_OUTSTANDING"],
                         c["LATERAL"]))
        for x in f["flips"]:
            print("                   %s [%s] %s -> %s  (%s)"
                  % (x["obligation_id"], FAMILY_TAG.get(x["family"], "?"), x["from"], x["to"],
                     x["direction"]))
        if f["one_directional"]:
            # THE READING THAT MATTERS, and it is the reason direction is counted at all. A delta cannot
            # tell a correction from a capitulation; both show `outstanding` falling.
            print("                 *** EVERY ONE OF THESE %d REVERSAL(S) RAN ONE WAY. A second look"
                  % f["reversals"])
            print("                 that CORRECTS the first produces flips in both directions; a")
            print("                 second look that is being PRESSURED produces them in one. Read")
            print("                 this iteration as the latter until something rules it out.")
        elif f["reversals"]:
            print("                 %d reversal(s), in BOTH directions — consistent with a second"
                  % f["reversals"])
            print("                 look correcting the first rather than agreeing with it.")
    last = records[-1]
    print(" FINAL         : raised=%d discharged=%d outstanding=%d  stop=%s  iterations=%d of %d"
          % (last["ledger"]["raised"], last["ledger"]["discharged"], last["ledger"]["outstanding"],
             "ABORTED" if aborted else last["stop_reason"], len(records), max_it))
    print(" cost          : %s over %d model call(s) with a recorded cost;"
          % ("$%.4f" % tot["model_cost_usd"] if tot["model_cost_usd"] is not None else "unrecorded",
             tot["model_calls_with_a_cost"]))
    print("                 %ss in the verifier, %ss wall clock for the whole loop."
          % (tot["verifier_seconds"], tot["wall_clock_s"]))
    if len(records) > 1 and last["ledger"]["outstanding"] == 0:
        # THE THING THE DRIVER HAS TO BE ABLE TO SEE. A run that needed three passes to reach a clean
        # ledger is not as trustworthy as one that was clean immediately, and an exit code of 0 says
        # the same thing about both.
        print(" *** CONVERGED ON ITERATION %d, NOT ON ITERATION 1. The ledger is clean and it took"
              % len(records))
        print("     %d passes to get there, so %d earlier pass(es) of the same verifier on the same"
              % (len(records), len(records) - 1))
        print("     bundle disagreed with this one. Exit 0 cannot carry that distinction; this line")
        print("     is where it is carried.")


def _write_loop_record(bundle, records, max_it, t_run, aborted,
                       denominator_drift=None, packed_vs_scored=None):
    """The loop's machine-readable record. Never staged for a verifier (see VIEW_EXCLUDE)."""
    path = os.path.join(bundle, "gateA-loop-run.json")
    doc = {
        "gate": "A",
        "provenance": "MODEL judgements, DETERMINISTIC bookkeeping",
        "_what": ("One entry per iteration of ONE `gate_a.py run`. `flips` is the DIRECTION of every "
                  "verdict change against the previous iteration, per family, because a fall in "
                  "`outstanding` cannot by itself distinguish a second look that corrected the first "
                  "from one that was pressured into agreeing with the carried-forward open list."),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "max_iterations": max_it,
        "totals": _loop_totals(records, t_run),
        "final": ({"ledger": records[-1]["ledger"],
                   "stop_reason": "ABORTED" if aborted else records[-1]["stop_reason"],
                   "outstanding_ids": records[-1]["outstanding_ids"],
                   "converged_on_iteration": (len(records)
                                              if records[-1]["ledger"]["outstanding"] == 0
                                              else None)}
                  if records else None),
        "aborted": aborted,
        "denominator": {
            "identical_across_iterations": not (denominator_drift or packed_vs_scored),
            "raised_ids": records[0]["scored_ids"] if records else [],
            "drift_across_iterations": denominator_drift or [],
            "verifier_versus_scorer": packed_vs_scored,
        },
        "iterations": records,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
    print(" loop record   : %s" % path)
    return path


def main(argv):
    ap = argparse.ArgumentParser(prog="gate_a.py", add_help=True,
                                 description="Gate A — agentic IR-completeness gate.")
    sub = ap.add_subparsers(dest="cmd")

    def add_pack_args(p):
        p.add_argument("table")
        p.add_argument("doc")
        p.add_argument("ir")
        p.add_argument("out_root")
        p.add_argument("--bundle", required=True)
        p.add_argument("--emit-log", dest="emit_log", default=None)
        p.add_argument("--inventory", default=None)
        p.add_argument("--carry-forward", dest="carry_forward", action="store_true",
                       help="keep the previous iteration's unresolved list in the bundle, labelled "
                            "as a prior claim. Off by default: a fresh verifier must be blind. "
                            "`run` sets it for iterations 2+ regardless; passing it makes even "
                            "iteration 1 see whatever a previous run left, which is rarely wanted.")

    p = sub.add_parser("pack")
    add_pack_args(p)

    p = sub.add_parser("score")
    p.add_argument("--bundle", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--sidecar", default=None)
    p.add_argument("--iteration", type=int, default=1)
    p.add_argument("--max-iterations", dest="max_iterations", type=int, default=3)
    p.add_argument("--emit-log", dest="emit_log", default=None)
    p.add_argument("--inventory", default=None)

    p = sub.add_parser("run")
    add_pack_args(p)
    p.add_argument("--verifier-cmd", dest="verifier_cmd", default=None)
    p.add_argument("--sidecar", default=None)
    p.add_argument("--iteration", type=int, default=1)
    # THE CONVERGENCE LOOP'S BOUND, and `1` is the SINGLE-PASS CONTROL rather than a degraded mode.
    # Every measurement of what the loop buys needs both arms of the same comparison run through the
    # same code, so turning the loop off has to be a supported setting and not a code edit.
    p.add_argument("--max-iterations", dest="max_iterations", type=int, default=3,
                   help="iterate up to this many times, stopping early on CONVERGED or NO_PROGRESS. "
                        "1 = one pass, the control arm. Default 3.")

    # ONE IMPLEMENTATION OF THE --verifier-cmd SEAM, not a replacement for it. Point the seam at this:
    #   --verifier-cmd 'python3 gate_a.py verifier --bundle {bundle} --verdict {verdict}'
    p = sub.add_parser("verifier", help="run the bundle past a headless model call over an isolated "
                                        "view of it, and write the verdict")
    p.add_argument("--bundle", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--cli", default=None,
                   help="the CLI to invoke (default: $GATE_VERIFIER_CLI, else `claude`)")
    p.add_argument("--model", default=None)
    p.add_argument("--max-budget-usd", dest="max_budget_usd", default=None)
    p.add_argument("--verifier-timeout", dest="verifier_timeout", type=int, default=900)
    p.add_argument("--view", default=None,
                   help="exact directory to stage the verifier's view in. Must be outside $HOME")
    p.add_argument("--view-root", dest="view_root", default=None,
                   help="parent for the generated view directory (default: the system temp dir)")
    p.add_argument("--keep-view", dest="keep_view", action="store_true",
                   help="leave the view on disk for audit. The run record lists it either way")

    # BATCHING (SNOW-3956446 / I-26) — the same isolated-call machinery as `verifier`, run once per
    # batch instead of once for the whole raised set. See the module docstring's BATCHING section.
    p = sub.add_parser("batched-run", help="pack, then batch the verifier across multiple bounded "
                                           "isolated calls (family boundaries, optionally chunked), "
                                           "merge the fragments honestly, and score. Single pass -- "
                                           "see `run` for the iterate-to-convergence loop.")
    add_pack_args(p)
    p.add_argument("--cli", default=None,
                   help="the CLI to invoke per batch (default: $GATE_VERIFIER_CLI, else `claude`)")
    p.add_argument("--model", default=None)
    p.add_argument("--max-budget-usd", dest="max_budget_usd", default=None)
    p.add_argument("--verifier-timeout", dest="verifier_timeout", type=int, default=900)
    p.add_argument("--view-root", dest="view_root", default=None,
                   help="parent for each batch's generated view directory (default: system temp dir)")
    p.add_argument("--keep-view", dest="keep_view", action="store_true",
                   help="leave every batch's view on disk for audit")
    p.add_argument("--batch-size", dest="batch_size", type=int, default=None,
                   help="further split a family larger than this into fixed-size chunks. Default: "
                        "one batch per family, no further splitting -- the boundary the measured "
                        "cliff actually failed at. Override with --batch-size or "
                        "$AIFIRST_GATEA_BATCH_SIZE.")
    p.add_argument("--parallelism", type=int,
                   default=int(os.environ.get("AIFIRST_GATE_PARALLELISM", "4")),
                   help="bounded concurrent verifier calls. Default 4 (or "
                        "$AIFIRST_GATE_PARALLELISM).")
    p.add_argument("--sidecar", default=None)
    p.add_argument("--iteration", type=int, default=1)
    p.add_argument("--max-iterations", dest="max_iterations", type=int, default=1,
                   help="passed through to score() for the loop bookkeeping fields; batched-run "
                        "itself is single-pass. Default 1.")

    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help(sys.stderr)
        return 2
    try:
        if args.cmd == "pack":
            return pack(args)
        if args.cmd == "score":
            return score(args)
        if args.cmd == "verifier":
            return verifier(args)
        if args.cmd == "batched-run":
            return batched_run(args)
        return run(args)
    except GateAError as ex:
        # ONE exit code for every could-not-run condition, and it is not an obligation verdict. The
        # driver tells the two apart by the absence of the " ledger        :" line, the same way it
        # already tells "the loss ledger found loss" from "the loss ledger could not run".
        sys.stderr.write("GATE A COULD NOT RUN: %s\n" % ex)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
