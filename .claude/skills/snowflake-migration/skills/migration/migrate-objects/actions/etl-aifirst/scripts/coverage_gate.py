"""GATE A (deterministic half) — SOURCE-ELEMENT-TO-EMITTED-MODEL COVERAGE.

WHY THIS EXISTS, as a measurement rather than an argument
---------------------------------------------------------
`declared_vs_identified.py` reported `lost=0` on all four blind platforms, INCLUDING two that
emitted nothing at all, and on the DataStage job it balanced identified-equals-matched over a
document holding FIVE elements. That is not a bug in its arithmetic; it is the shape of its
question. Its ELEMENT denominator is the identification sweep's own output, so an element the sweep
never declared cannot be reported as lost. A gate whose baseline is derived from the thing it is
checking cannot detect what that thing never saw.

    findings/43-gate-b-results.md:
      source stages : CTransformerStage x1, PxFilter x1, PxOdbc x2   (4 stages + DSJOB = 5)
      IR nodes      : DSJOB, SourceQualifier, FilterTransformation, TargetTransformation   (4)

    RE-MEASURED, because the recorded ledger line no longer reproduces. That line read
    `declared=4 keyless=0 identified=4 lost=0 balances=True`, and the exhaustive-census pass
    redefined `declared` from "nodes the level queries matched" to "every record in the document"
    (the old number survives as `level_matched`). Current output for the same fixture,
    gateA-fixtures/CustomerSummaryDerive_NoTransformer.dsx:

      records=41 level_matched=4 keyless=0 identified=4 excluded=36 unknown=1 lost=0 balances=True

    The argument is STRONGER under the new semantics, not weaker: the missing stage is now visible
    in the census as `unknown=1` instead of being absent from every number. But it is still not an
    ELEMENT, still produces no IR node and still no model, so `lost=0` continues to be true and
    continues to say nothing about coverage. That is the gap this gate exists to measure.

So THIS gate derives its baseline from the SOURCE DOCUMENT, by a per-platform rule stated in its own
output, with no call into identify.py, emit.py or any platform-table xpath. The independence is the
entire point: if the baseline came from the sweep this file would be a slower copy of the ledger.

WHAT IT ANSWERS, per source element
-----------------------------------
  1. is the element present in the IR as a node?
  2. did it produce a dbt model file on disk?
  3. if not, WHY — one of a closed vocabulary, each read off an artifact and not guessed:
       NOT_IDENTIFIED         absent from the IR entirely. Sub-classified by whether its kind is in
                              the platform table's kind_dispatch: if it IS, the table is fine and
                              the SWEEP missed it (a level-query gap); if it is NOT, the table has
                              no entry for this kind at all.
       ABSORBED_BY_TABLE_RULE absent from the IR BY DESIGN — the table declares `collapse` for this
                              kind, so it was folded into a host element. Declared, not lost.
       NO_IR_KIND             in the IR, but the table maps its kind to ir_kind:null with no
                              degrade_to, so the hydrator has no door onto it.
       DEGRADED               in the IR carrying the table's degrade_to class instead of its real
                              one.
       TRANSLATOR_THREW       the emitter logged THREW for this node.
       TRANSLATOR_EMPTY       the emitter logged EMPTY (no ISqlQueryForDbt) for this node.
       NO_MODEL_UNEXPLAINED   in the IR, mapped, no model, and the emitter log does not say why
                              (or was not captured). Stated as unexplained rather than dressed up.

EXIT CODES — the driver's vocabulary, deliberately not widened
--------------------------------------------------------------
  0  every source element under the declared rule produced a model
  3  COVERAGE INCOMPLETE — at least one source element produced no model. Degradation, not failure:
     output exists and provably does not cover the input.
  1  the gate could not run (document unreadable, IR unreadable, no counting rule for the platform,
     or the counting rule found ZERO source elements -- an empty denominator is UNMEASURED, not
     COVERED, so it fails closed here rather than falling through to exit 0).
     NOT a coverage verdict. The driver distinguishes the two by stdout shape, exactly as it already
     does for the loss ledger.
  2  usage

DEGRADED-BUT-COVERED DOES NOT DRIVE THIS EXIT CODE, on purpose. A degraded element that still
emitted a model is a real degradation, and the driver's stage 4 already catches it from the artifact
(blocking EWI / sentinel / no-columns / MODEL-AUTHORED). Scoring it here as well would make this
gate answer two questions and make its verdict unreadable. Degradation is PRINTED as a note so it
is visible; the exit code stays on the one question this gate exists to answer: coverage.

Usage:
  python3 coverage_gate.py <platform-table.json> <source-document> <ir.json> <output-root>
                           [--emit-log FILE]
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------------------------
# COUNTING RULES. One per platform, each SIMPLE and EXPLICIT, and each printed in the report so a
# reader can re-run it by hand against the file. No rule infers an element from topology, from a
# hop list, or from anything the document does not state directly -- if a platform's element set
# were not determinable from the document alone, the honest output is a failure, not a heuristic.
# --------------------------------------------------------------------------------------------

RULES = {
    "SqlServerIntegrationServices": (
        "dtsx.componentclassid.v1",
        "one element per <component> element carrying a `componentClassID` attribute. "
        "id = @refId, name = @name, kind = @componentClassID. Control-flow <Executable> "
        "elements are NOT counted by this rule.",
    ),
    "InformaticaPowerCenter": (
        "infa.instance.v1",
        "one element per INSTANCE element. id = name = @NAME, kind = @TRANSFORMATION_TYPE. "
        "SEE THE CAVEAT PRINTED BELOW when the document contains a WORKFLOW.",
    ),
    "PentahoDataIntegration": (
        "ktr.step.v1",
        "one element per <step> element. id = name = <name> child text, kind = <type> child "
        "text. The <info> transformation block itself is NOT counted by this rule.",
    ),
    "IbmInfoSphereDataStage": (
        "dsx.stagetype.v1",
        "one element per DSRECORD block containing a `StageType \"...\"` property. "
        "id = the block's `Identifier`, name = its `Name`, kind = its `StageType`. "
        "DSJOB, link records (CTrxInput/CTrxOutput/CustomInput/CustomOutput) and the "
        "CJobDefn root record state no StageType and are NOT counted by this rule.",
    ),
    "alteryx": (
        "yxmd.node.toolid.v1",
        "one element per <Node> element carrying a `ToolID` attribute. "
        "id = @ToolID, name = GuiSettings/@Plugin (fallback @ToolID), kind = GuiSettings/@Plugin. "
        "Connections and configuration children are NOT counted by this rule.",
    ),
}


class Element:
    __slots__ = ("eid", "name", "kind", "where")

    def __init__(self, eid, name, kind, where):
        self.eid = eid
        self.name = name
        self.kind = kind
        self.where = where


def _local(tag):
    return tag.split("}")[-1]


def count_ssis(path):
    root = ET.parse(path).getroot()
    out = []
    for e in root.iter():
        if _local(e.tag) != "component":
            continue
        ccid = None
        for k, v in e.attrib.items():
            if _local(k) == "componentClassID":
                ccid = v
        if ccid is None:
            continue
        att = {_local(k): v for k, v in e.attrib.items()}
        out.append(Element(att.get("refId") or att.get("name"), att.get("name"), ccid,
                           "component[@refId=%r]" % att.get("refId")))
    return out, []


def count_informatica(path):
    root = ET.parse(path).getroot()
    out = []
    caveats = []
    if any(_local(e.tag) == "WORKFLOW" for e in root.iter()):
        # MEASURED, not assumed. On the repo's own WF_PARAMFILE_MULTI_SESSION.XML a WORKFLOW's
        # children are TASKINSTANCE / SESSION / TASK -- NOT INSTANCE -- so this rule does not in
        # fact pick up control-flow instances there. Kept as a flag rather than deleted because it
        # was checked on exactly one workflow export; what a different one spells is unverified.
        caveats.append(
            "NOTE: this document contains a WORKFLOW. `infa.instance.v1` counts EVERY INSTANCE "
            "element. On the one workflow export checked (WF_PARAMFILE_MULTI_SESSION.XML) a "
            "WORKFLOW declares session instances as TASKINSTANCE, not INSTANCE, so the rule stayed "
            "mapping-scoped by itself -- but that is one document, not a guarantee. Read the "
            "element list below before trusting the denominator.")
    for e in root.iter():
        if _local(e.tag) != "INSTANCE":
            continue
        att = {_local(k): v for k, v in e.attrib.items()}
        out.append(Element(att.get("NAME"), att.get("NAME"),
                           att.get("TRANSFORMATION_TYPE"), "INSTANCE[@NAME=%r]" % att.get("NAME")))
    return out, caveats


def count_pentaho(path):
    root = ET.parse(path).getroot()
    out = []
    for e in root.iter():
        if _local(e.tag) != "step":
            continue
        name = (e.findtext("name") or "").strip()
        kind = (e.findtext("type") or "").strip()
        out.append(Element(name, name, kind, "step[name=%r]" % name))
    return out, []


DSX_PROP = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s+"(.*)"\s*$')
DSX_BEGIN = re.compile(r"^\s*BEGIN\s+(\S+)\s*$")
DSX_END = re.compile(r"^\s*END\s+(\S+)\s*$")
DSX_HEREDOC = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s+=\+=\+=\+=\s*$')


def count_datastage(path):
    """Independent block scanner over the .dsx TEXT.

    Deliberately does NOT go through docmodel/dsxdoc. Those are the projection the identification
    sweep queries; borrowing them would reintroduce the coupling this gate exists to break. A .dsx
    is a flat BEGIN/END keyword stream and needs nothing more than a stack to read.
    """
    out = []
    stack = []           # list of (kind, props dict, line no)
    lineno = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        lineno = i + 1
        i += 1
        m = DSX_HEREDOC.match(line)
        if m:
            # Multi-line value. Its body is free text and can contain the word BEGIN, so it is
            # skipped wholesale rather than scanned.
            while i < len(lines) and lines[i].strip() != "=+=+=+=":
                i += 1
            i += 1
            continue
        m = DSX_BEGIN.match(line)
        if m:
            stack.append([m.group(1), {}, lineno])
            continue
        m = DSX_END.match(line)
        if m:
            if stack and stack[-1][0] == m.group(1):
                kind, props, start = stack.pop()
                if kind == "DSRECORD" and "StageType" in props:
                    out.append(Element(props.get("Identifier"), props.get("Name"),
                                       props["StageType"],
                                       "%s:%d DSRECORD[Identifier=%r]"
                                       % (os.path.basename(path), start,
                                          props.get("Identifier"))))
            continue
        m = DSX_PROP.match(line)
        if m and stack:
            stack[-1][1].setdefault(m.group(1), m.group(2))
    return out, []


def count_alteryx(path):
    """Independent count of Alteryx canvas tools from the .yxmd XML.

    Deliberately does NOT go through identify.py. A .yxmd lists tools as <Node ToolID="...">
    with GuiSettings/@Plugin naming the tool kind. Connections are separate and not counted.
    """
    root = ET.parse(path).getroot()
    out = []
    for e in root.iter():
        if _local(e.tag) != "Node":
            continue
        att = {_local(k): v for k, v in e.attrib.items()}
        tid = att.get("ToolID")
        if tid is None:
            continue
        plugin = None
        for child in list(e):
            if _local(child.tag) == "GuiSettings":
                plugin = {_local(k): v for k, v in child.attrib.items()}.get("Plugin")
                break
        out.append(Element(tid, plugin or tid, plugin or "Unknown",
                           "Node[@ToolID=%r]" % tid))
    return out, []


COUNTERS = {
    "SqlServerIntegrationServices": count_ssis,
    "InformaticaPowerCenter": count_informatica,
    "PentahoDataIntegration": count_pentaho,
    "IbmInfoSphereDataStage": count_datastage,
    "alteryx": count_alteryx,
}


# --------------------------------------------------------------------------------------------
# the artifacts side
# --------------------------------------------------------------------------------------------

MODEL_SKIP = ("dbt_internal_packages", "target")


def find_models(out_root):
    """Every model the emitter actually wrote. `dbt_internal_packages` carries a `models` directory
    of ADAPTER MACROS and `target/compiled` carries copies of our own models; counting either would
    inflate coverage with files no source element produced."""
    found = []
    for dirpath, dirnames, filenames in os.walk(out_root):
        dirnames[:] = [d for d in dirnames if d not in MODEL_SKIP]
        if "models" not in dirpath.split(os.sep):
            continue
        for f in filenames:
            if f.endswith(".sql"):
                found.append(os.path.join(dirpath, f))
    return sorted(found)


def norm(s):
    return (s or "").strip().lower()


def ir_keys(node):
    """Every string by which a source element could legitimately be recognised as this node."""
    keys = set()
    nid = node.get("id") or ""
    keys.add(norm(nid))
    for sep in ("\\", "/"):
        if sep in nid:
            keys.add(norm(nid.rsplit(sep, 1)[-1]))
    el = node.get("element") or {}
    keys.add(norm(el.get("Name")))
    keys.discard("")
    return keys


def model_for(model_name, model_files):
    """A model file belongs to a node when its stem is the node's modelName, optionally behind an
    emitter-applied layer prefix (`stg_raw__`, `int_`, ...). Matched by suffix with a `_` boundary
    rather than an enumerated prefix list, because the prefix set is the emitter's business and this
    gate must not encode it. Ambiguity is reported, never resolved silently."""
    if not model_name:
        return []
    mn = norm(model_name)
    hits = []
    for p in model_files:
        stem = norm(os.path.splitext(os.path.basename(p))[0])
        if stem == mn or (stem.endswith(mn) and stem[: -len(mn)].endswith("_")):
            hits.append(p)
    return hits


EMIT_STATUS = re.compile(r"^\s+(EMPTY|SUBST|THREW)\s+(.*)$")


def parse_emit_log(path, node_ids):
    """The emitter prints one `OK/SUBST/EMPTY/THREW` line per node. Node ids contain spaces and
    backslashes, so the line is matched against the KNOWN ids rather than split on whitespace.

    LONGEST id first, and the remainder must be whitespace-delimited. The first version took the
    first id that prefixed the line, and on DataStage every id starts with the job id
    `CustomerSummaryDerive` -- so both `.../V0S3` and `.../V0S4` were attributed to the JOB node and
    the two real statuses vanished. A parser that silently collapses two facts into one is exactly
    the failure mode this gate was written to catch, in the gate itself."""
    status = {}
    detail = {}
    if not path or not os.path.exists(path):
        return status, detail
    ordered = sorted([n for n in node_ids if n], key=len, reverse=True)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = EMIT_STATUS.match(line.rstrip("\n"))
            if not m:
                continue
            rest = m.group(2)
            for nid in ordered:
                if rest.startswith(nid) and (len(rest) == len(nid)
                                             or rest[len(nid)].isspace()):
                    status[nid] = m.group(1)
                    detail[nid] = rest[len(nid):].strip()
                    break
    return status, detail


# --------------------------------------------------------------------------------------------

def main(argv):
    emit_log = None
    if "--emit-log" in argv:
        k = argv.index("--emit-log")
        emit_log = argv[k + 1] if len(argv) > k + 1 else None
        argv = argv[:k] + argv[k + 2:]
    if len(argv) != 4:
        sys.stderr.write("usage: coverage_gate.py <platform-table.json> <source-document> "
                         "<ir.json> <output-root> [--emit-log FILE]\n")
        return 2
    table_path, doc_path, ir_path, out_root = argv

    try:
        with open(table_path, "r", encoding="utf-8") as fh:
            table = json.load(fh)
    except Exception as ex:
        sys.stderr.write("GATE A COULD NOT RUN: platform table unreadable: %s\n" % ex)
        return 1
    platform = table.get("platform")
    if platform not in COUNTERS:
        # THE HONEST FAILURE. No fallback counter, no "count everything with an id" heuristic --
        # an invented denominator is how the ledger this gate replaces came to report lost=0 on a
        # tree with no output in it.
        sys.stderr.write(
            "GATE A COULD NOT RUN: no source-element counting rule for platform %r. This gate "
            "will not guess a denominator; add an explicit rule to RULES/COUNTERS or accept that "
            "coverage is UNMEASURED on this platform.\n" % platform)
        return 1
    try:
        elements, caveats = COUNTERS[platform](doc_path)
    except Exception as ex:
        sys.stderr.write("GATE A COULD NOT RUN: source document unreadable by rule %s: %s: %s\n"
                         % (RULES[platform][0], type(ex).__name__, ex))
        return 1
    if not elements:
        # A parse that finds ZERO source elements is NOT a clean 0/0 pass. Left unchecked, the
        # loop below builds an empty `rows` list, `holes` stays empty, and the verdict below reads
        # "coverage complete" -- exactly the silent-success defect this gate exists to catch,
        # just moved one level up from the loss ledger into its replacement. A WORKFLOW-only
        # Informatica export (INSTANCE-less) or a zero-<step> Pentaho transformation hits this:
        # the document parsed fine and there is genuinely nothing to measure, so the honest
        # answer is UNMEASURED, not COVERED.
        for c in caveats:
            sys.stderr.write("NOTE: %s\n" % c)
        sys.stderr.write(
            "GATE A COULD NOT RUN: counting rule %s found ZERO source elements in %s. Coverage is "
            "UNMEASURED, not complete -- an empty denominator would trivially satisfy \"every "
            "element produced a model\". Treated as a gate failure, not a coverage verdict.\n"
            % (RULES[platform][0], doc_path))
        return 1
    try:
        with open(ir_path, "r", encoding="utf-8") as fh:
            ir = json.load(fh)
        nodes = ir.get("nodes") or []
    except Exception as ex:
        sys.stderr.write("GATE A COULD NOT RUN: IR unreadable: %s: %s\n" % (type(ex).__name__, ex))
        return 1

    models = find_models(out_root)
    node_ids = [n.get("id") or "" for n in nodes]
    status, detail = parse_emit_log(emit_log, node_ids)
    dispatch = table.get("kind_dispatch") or {}
    rule_id, rule_text = RULES[platform]

    index = {}
    for n in nodes:
        for k in ir_keys(n):
            index.setdefault(k, []).append(n)

    # NON-UNIQUE SOURCE IDS, and the reason this block exists rather than a comment.
    # `infa.instance.v1` keys on @NAME, and a multi-mapping export repeats the SAME names in every
    # MAPPING: WF_PARAMFILE_MULTI_SESSION.XML declares tableA / SQ_tableA / tableC three times
    # each. Without this block all nine source elements matched the three surviving IR nodes and the
    # gate reported 9/9 COVERED on the very document the loss ledger scores `identified=3 lost=6`.
    # A gate that goes green on a two-thirds loss is worse than no gate.
    #
    # What is done about it is PROVABLE rather than heuristic: an IR node can be the representation
    # of at most one source element, so if K source elements share an id and only M < K IR nodes
    # carry it, then K - M of them have no representation. Which of the K survived is NOT
    # determinable from these artifacts, and the gate says so instead of picking one.
    groups = {}
    for el in elements:
        dd = dispatch.get(el.kind)
        if isinstance(dd, dict) and isinstance(dd.get("collapse"), dict):
            # A collapse kind is DECLARED never to become a node, so its absence from the IR is not
            # evidence of anything and the K-vs-M argument does not apply to it. Left in the
            # ambiguity groups it would have shadowed the true reason: on the multi-session document
            # all three `tableA` Source Definitions read ID_NOT_UNIQUE, which blamed the absorbed
            # element for a loss that belongs to the Source Qualifier that absorbed it.
            continue
        groups.setdefault(norm(el.eid), []).append(el)
    consumed = {}
    ambiguous = {}
    for key, group in groups.items():
        avail = index.get(key) or []
        if len(group) > 1 and len(avail) < len(group):
            ambiguous[key] = (len(group), len(avail))

    rows = []
    matched_nodes = set()
    for el in elements:
        key = norm(el.eid)
        d = dispatch.get(el.kind) if isinstance(dispatch.get(el.kind), dict) else None
        if key in ambiguous:
            k, m = ambiguous[key]
            taken = consumed.get(key, 0)
            consumed[key] = taken + 1
            avail = index.get(key) or []
            if taken >= len(avail):
                rows.append((el, None, [], "ID_NOT_UNIQUE",
                             "%d source elements share the id %r under %s and only %d IR node(s) "
                             "carry that key, so at least %d of them have NO representation. Which "
                             "ones survived is not determinable from these artifacts -- the gate "
                             "will not pick one." % (k, el.eid, rule_id, m, k - m)))
                continue
            node = avail[taken]
        else:
            node = None
            for cand in (el.eid, el.name):
                if norm(cand) in index:
                    node = index[norm(cand)][0]
                    break
        if node is None:
            if d is not None and isinstance(d.get("collapse"), dict):
                rows.append((el, None, [], "ABSORBED_BY_TABLE_RULE",
                             "table declares collapse into %s -- absent from the IR BY DESIGN, "
                             "not lost" % d["collapse"].get("into")))
            elif d is not None:
                rows.append((el, None, [], "NOT_IDENTIFIED",
                             "kind IS in kind_dispatch (ir_kind=%s degrade_to=%s) so the TABLE is "
                             "not the gap -- the identification SWEEP never produced this element"
                             % (d.get("ir_kind"), d.get("degrade_to"))))
            else:
                rows.append((el, None, [], "NOT_IDENTIFIED",
                             "kind %r is ABSENT from kind_dispatch entirely" % el.kind))
            continue
        matched_nodes.add(id(node))
        found = model_for(node.get("modelName"), models)
        el_kind = (node.get("element") or {}).get("$kind")
        degrade_to = d.get("degrade_to") if d else None
        if found:
            if el_kind is None:
                rows.append((el, node, found, "COVERED",
                             "model present; IR $kind is null (node carries _unsupported)"))
            elif el_kind == "UnsupportedTransformation" or (
                    degrade_to and el_kind == degrade_to and d.get("ir_kind") != el_kind):
                # Two different situations, and stating them the same way was misleading: a kind the
                # table MAPS and that fell back, versus a kind the table never mapped at all and
                # whose only representation IS degrade_to. Both leave a placeholder model; only the
                # first is a regression against a supported class.
                if d is None or d.get("ir_kind") is None:
                    note = ("the node exists only as UnsupportedTransformation -- "
                            "the model is a placeholder, not a conversion")
                else:
                    note = ("model present but the node fell back from its mapped class %r to the "
                            "table's degrade_to class %r" % (d.get("ir_kind"), degrade_to))
                rows.append((el, node, found, "COVERED_DEGRADED", note))
            else:
                rows.append((el, node, found, "COVERED", ""))
            continue
        st = status.get(node.get("id"))
        if st == "THREW":
            why = ("TRANSLATOR_THREW", "emitter log: %s" % detail.get(node.get("id"), ""))
        elif st == "EMPTY":
            why = ("TRANSLATOR_EMPTY",
                   "emitter log: no ISqlQueryForDbt from %s"
                   % (detail.get(node.get("id")) or "translation"))
        elif el_kind is None and d is not None and not degrade_to:
            why = ("NO_IR_KIND",
                   "table maps kind %r to ir_kind:null with no degrade_to -- the hydrator has no "
                   "door onto it" % el.kind)
        elif el_kind is None:
            why = ("NO_IR_KIND",
                   "node is in the IR with $kind null (%s)"
                   % ((node.get("element") or {}).get("_unsupported") or "no _unsupported marker"))
        elif degrade_to and el_kind == degrade_to and d.get("ir_kind") != el_kind:
            why = ("DEGRADED", "node degraded to %r and no model was written" % degrade_to)
        else:
            why = ("NO_MODEL_UNEXPLAINED",
                   "in the IR as %r, mapped, no model file, and the emitter log %s"
                   % (el_kind, "does not mention this node"
                      if emit_log else "was not captured (--emit-log not given)"))
        rows.append((el, node, [], why[0], why[1]))

    # ---- report ----------------------------------------------------------------------------
    W = 96
    print("=" * W)
    print(" GATE A — SOURCE-ELEMENT COVERAGE (deterministic half)")
    print("=" * W)
    print(" platform      : %s   [table %s]" % (platform, table.get("table_version")))
    print(" document      : %s" % doc_path)
    print(" COUNTING RULE : %s" % rule_id)
    for i, chunk in enumerate(_wrap(rule_text, W - 18)):
        print("                 %s" % chunk)
    print(" MATCH RULE    : a source element is the IR node whose id, id-last-segment (split on")
    print("                 '\\' or '/') or element.Name equals its id or name, case-folded. A")
    print("                 model belongs to a node when the file stem is the node's modelName,")
    print("                 optionally behind a `<prefix>_` the emitter added.")
    print(" IR            : %s   [%d node(s)]" % (ir_path, len(nodes)))
    print(" emitted models: %d file(s) under %s" % (len(models), out_root))
    if emit_log:
        print(" emitter log   : %s   [%d node status line(s)]" % (emit_log, len(status)))
    for c in caveats:
        print("-" * W)
        for chunk in _wrap(c, W - 2):
            print(" %s" % chunk)
    if ambiguous:
        print("-" * W)
        for key, (k, m) in sorted(ambiguous.items()):
            for chunk in _wrap("ID NOT UNIQUE under %s: %d source elements share the id %r and %d "
                               "IR node(s) carry it. Coverage for that id is reported as "
                               "UNRESOLVABLE below, not as covered." % (rule_id, k, key, m), W - 2):
                print(" %s" % chunk)
    print("-" * W)
    print(" %-28s %-24s %-6s %-6s %s" % ("source element", "kind", "in IR", "model", "verdict"))
    print("-" * W)
    holes = []
    degraded = []
    for el, node, found, verdict, why in rows:
        label = el.eid if el.eid == el.name or not el.name else "%s (%s)" % (el.eid, el.name)
        print(" %-28s %-24s %-6s %-6s %s"
              % (_cliptail(label, 28), _clip(el.kind, 24),
                 "yes" if node is not None else "NO",
                 "yes" if found else "NO", verdict))
        if why:
            for chunk in _wrap(why, W - 8):
                print("        %s" % chunk)
        if found:
            for p in found:
                print("        model: %s" % os.path.relpath(p, out_root))
            if len(found) > 1:
                print("        AMBIGUOUS: %d files matched modelName %r -- coverage counted once, "
                      "but the match rule did not discriminate" % (len(found), node.get("modelName")))
        else:
            print("        at %s" % el.where)
        if verdict in ("COVERED", "COVERED_DEGRADED", "ABSORBED_BY_TABLE_RULE"):
            if verdict == "COVERED_DEGRADED":
                degraded.append(el)
        else:
            holes.append((el, verdict, why))

    extra = [n for n in nodes if id(n) not in matched_nodes]
    print("-" * W)
    covered = len(rows) - len(holes)
    print(" coverage      : %d/%d source element(s) accounted for under %s"
          % (covered, len(rows), rule_id))
    if degraded:
        print(" note          : %d element(s) COVERED_DEGRADED — a model exists but carries the"
              % len(degraded))
        print("                 table's degrade_to class. Not scored here; stage 4 scores the")
        print("                 artifact. Listed so it is not invisible.")
    if extra:
        # NOT counted as coverage either way. These are nodes the sweep produced that the counting
        # rule does not call elements (a job, a package container, a data-flow task). Printing them
        # is what keeps the two denominators honest against each other.
        print(" IR nodes with no source element under this rule (NOT scored):")
        for n in extra:
            print("     %s   type=%s modelName=%s $kind=%s"
                  % (n.get("id"), n.get("type"), n.get("modelName"),
                     (n.get("element") or {}).get("$kind")))
    print("-" * W)
    if holes:
        print(" VERDICT: COVERAGE INCOMPLETE — %d source element(s) produced no model (exit 3)"
              % len(holes))
        for el, verdict, why in holes:
            print("     *** %s [%s] : %s" % (el.eid, el.kind, verdict))
        return 3
    print(" VERDICT: coverage complete — every source element under %s produced a model (exit 0)"
          % rule_id)
    return 0


def _clip(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def _cliptail(s, n):
    """Clip from the LEFT. An SSIS refId is `Package\\DFT Load Customer Summary\\OLE_SRC CUSTOMER`
    and the discriminating part is the tail, so clipping from the right produced four rows that all
    read `Package\\DFT Load Cust…` -- a table in which every element looks like every other."""
    s = s or ""
    return s if len(s) <= n else "…" + s[-(n - 1):]


def _wrap(s, n):
    words = (s or "").split()
    out, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out or [""]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
