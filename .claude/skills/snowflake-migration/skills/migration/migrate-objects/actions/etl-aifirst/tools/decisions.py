"""The 23 blind-run decisions, reclassified — with machine checks.

Lab tool (not runtime). Usage:
  python3 decisions.py <Informatica MappingForTest.XML>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
_PLATFORMS = Path(__file__).resolve().parent.parent / "platforms"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from emit import Emitter, scan
from identify import Identification, load_table

DETERMINED, TABLE, RESIDUE = "DETERMINED", "TABLE", "RESIDUE"

if len(sys.argv) < 2:
    raise SystemExit("usage: python3 decisions.py <Informatica MappingForTest.XML>")

XML = sys.argv[1]
table = load_table(str(_PLATFORMS / "platform_informatica.json"))
idn = Identification(table, XML)
em = Emitter(idn)
ir = em.emit()
nodes = {n["id"]: n for n in ir["nodes"]}



# --- element addressing ---------------------------------------------------
# FRAMEWORK CHANGE 66 (c) (this file): every reference below was a bare instance
# name -- nodes["INCR_SALARY"], idn.elements["SALARY_RTRTRANS"]. Declaring
# structure.key_scope on this platform makes the element key MAPPING-scoped
# ("MappingForTest\\INCR_SALARY"), and this file went down with
# `KeyError: 'INCR_SALARY'`. It was the loudest half of the trap that kept the
# scope on hold.
#
# Resolving by LAST SEGMENT rather than by rewriting 20 literals is deliberate:
# these 23 decisions are about an element's DISPLAY identity, not about how the
# key happens to be composed, so the file should not have to change again the next
# time a scope is added or removed. Ambiguity RAISES -- two elements sharing a
# last segment inside one document is exactly the collision key_scope exists to
# represent, and silently picking one would reintroduce it here.

def eid(short: str) -> str:
    """The full element key whose last path segment is `short`."""
    hits = [k for k in idn.elements if k.rsplit("\\", 1)[-1] == short]
    if len(hits) != 1:
        raise KeyError(f"{short!r} resolves to {len(hits)} element(s): {hits}")
    return hits[0]


def node(short: str) -> dict:
    return nodes[eid(short)]


def leaf(key: str) -> str:
    """The display half of an element key, for comparing against a source name."""
    return key.rsplit("\\", 1)[-1]


def outcol(short, col_name):
    for c in node(short)["element"].get("OutputColumns", []):
        if c["Name"] == col_name:
            return c
    return None


def incols(short):
    return [c["Name"] for c in node(short)["element"].get("InputColumns", [])]


# --- check bodies ---------------------------------------------------------

def chk_degraded_kinds():
    """#4, and THE CHECK ITSELF WAS THE DEFECT -- twice rewritten, for opposite
    reasons, and the second time is what this note records.

    ROUND 1 (degrade_to landed). The decision used to be "emit $kind: null and let
    the hydrator keep the node out of the graph". That was measured to drop every
    edge touching the node -- 3 of Informatica's 5, 19 of 19 on DataStage -- so the
    choice changed to degrade_to and the check was rewritten to assert four halves
    together for BOTH `SALARY_RTRTRANS` (Router) and `MyReportTable` (Target
    Definition), which were then both unsupported.

    ROUND 2 (this one). `kind_dispatch['Target Definition']` was later WIDENED --
    ir_kind null -> TargetTransformation, with element_fields.TableName REQUIRED,
    for the recorded reason that TargetTranslatorBase substitutes YOUR_DB plus a
    fallback schema when the table is null. The widening is correct and measured
    (`MyReportTable` now carries TableName='MyReportTable' at SOURCE). The CHECK was
    never updated, so it went on asserting that a supported kind must be degraded
    and reported the one CHECK FAILURE in this file -- a false alarm about a
    deliberate improvement. Pre-existing and Informatica-only, exactly as reported.

    WHAT IT ASSERTS NOW, AND WHY IT IS TABLE-DRIVEN. Hardcoding "these two are
    unsupported" is what went stale, so the expectation is now READ FROM
    kind_dispatch for each element's own kind, and the two directions are asserted
    separately:

      REFUSED (ir_kind null, degrade_to set) -- Router. The node must carry the
        degrade_to class, still name its NATIVE kind in _unsupported, still have a
        MISSING element.$kind obligation (so degrading earns no fit credit), and the
        census must still say NotSupported.
      PROMOTED (ir_kind set, every `required` element_fields entry populated) --
        Target Definition. The node must carry the MAPPED class, must NOT carry
        _unsupported, and must have a satisfied element.$kind.
      DECLINED (ir_kind set, a `required` entry did NOT resolve) -- the same kind on
        a document that buries its table name. emit_node must degrade, and this
        branch asserts that it did. This is where round 1's protection lives now: a
        node emitted with the mapped class WITHOUT its required payload satisfies
        neither branch and fails, which is exactly the "silently upgraded to
        supported" case the original check was written to catch.

    NEGATIVE-TESTED: with `TableName` deleted from the emitted element and $kind left
    at TargetTransformation -- the silent upgrade, constructed directly -- this check
    reports FAIL on the DECLINED branch. Verified by executing it."""
    import fit
    scored = fit.score(em.slots)
    parts, ok = [], True
    for short in ("SALARY_RTRTRANS", "MyReportTable"):
        node_id = eid(short)
        el = nodes[node_id]["element"]
        native = idn.elements[node_id].kind_raw
        d = table["kind_dispatch"].get(native, {})
        status = scored["elements"][node_id]["status"]
        kind_missing = any(s.path == "element.$kind" and s.provenance == "MISSING"
                           for s in scored["elements"][node_id]["slots"])
        if d.get("ir_kind") is None:
            good = (el["$kind"] == d.get("degrade_to")
                    and el.get("_unsupported") == native
                    and kind_missing and status == "NotSupported")
            shape = (f"REFUSED[{native}] -> {el['$kind']} "
                     f"_unsupported={el.get('_unsupported')!r} "
                     f"$kind-slot-MISSING={kind_missing} census={status}")
        else:
            required = [f for f, spec in (d.get("element_fields") or {}).items()
                        if spec.get("required")]
            present = [f for f in required if el.get(f)]
            if present == required:
                # PROMOTED, with the payload that makes promotion safe.
                good = (el["$kind"] == d["ir_kind"]
                        and el.get("_unsupported") is None
                        and not kind_missing and status != "NotSupported")
                shape = (f"PROMOTED[{native}] -> {el['$kind']} "
                         f"_unsupported={el.get('_unsupported')!r} "
                         f"$kind-slot-MISSING={kind_missing} census={status} "
                         f"required={required} populated={present}")
            else:
                # DECLINED: the table maps this kind but a required field did not
                # resolve, so emit_node must degrade rather than emit a hollow class.
                # Asserted so that a promotion with a MISSING required field -- the
                # silent upgrade -- cannot pass by falling into a branch that is
                # satisfied by anything.
                good = (el["$kind"] == d.get("degrade_to")
                        and kind_missing and status == "NotSupported")
                shape = (f"DECLINED[{native}] -> {el['$kind']} (table maps "
                         f"{d['ir_kind']}, required={required} populated={present}, so it "
                         f"must degrade to {d.get('degrade_to')}) "
                         f"$kind-slot-MISSING={kind_missing} census={status}")
        ok = ok and good
        parts.append(f"{short}: {shape}")
    return ok, "; ".join(parts)


def chk_case_insensitive():
    """#19: the Router MID_SALARY condition writes `the_salary`; the declared port
    is THE_SALARY. Resolution against the closed port-name set must normalise it.
    The Router is NotSupported so this never reaches the IR — exercise the
    resolver directly."""
    rtr = idn.elements[eid("SALARY_RTRTRANS")]
    by_lower = {p.name.lower(): p for p in rtr.ports}
    cond = next(g["expression"] for g in rtr.groups if g["name"] == "MID_SALARY")
    resolved = []
    for kind, lex in scan(cond):
        t = by_lower.get(lex.lower()) if kind == "ident" else None
        resolved.append(t.name if t else lex)
    got = "".join(resolved)
    return got == "NEW_SALARY < 1500 AND THE_SALARY > 500", got


DECISIONS = [
    # n, baseline rating, short title, bucket, mechanism, check
    (1, "ARBITRARY", "modelName for every node", TABLE,
     "naming_policy.informatica.modelname.v2 -- v1 asserted 'incr_salary'. The name is "
     "MAPPING-qualified since structure.key_scope was declared, for the measured "
     "six-element loss recorded in that entry; name_from=ELEMENT_KEY, so the model name "
     "follows the key rather than a second, disagreeing scope",
     lambda: (node("INCR_SALARY")["modelName"] == "mappingfortest_incr_salary",
              node("INCR_SALARY")["modelName"])),
    (2, "ARBITRARY", "modelName for the collapsed source node", TABLE,
     "naming_policy.collapsed_source_named_after=SOURCE_QUALIFIER_INSTANCE",
     lambda: (node("SQ_EMPLOYEE")["modelName"] == "mappingfortest_sq_employee",
              node("SQ_EMPLOYEE")["modelName"])),
    (3, "ARBITRARY", "which instance the collapsed source node is named after", TABLE,
     "kind_dispatch['Source Definition'].collapse; the LINK is structural "
     "(ASSOCIATED_SOURCE_INSTANCE), the CHOICE is table",
     lambda: ([leaf(a) for a in idn.elements[eid("SQ_EMPLOYEE")].absorbed] == ["EMPLOYEE"],
              str(idn.elements[eid("SQ_EMPLOYEE")].absorbed))),
    (4, "ARBITRARY", "$kind spelling for the two kinds the table refuses or gates", TABLE,
     "kind_dispatch, read per element rather than hardcoded: Router is REFUSED (ir_kind=null, "
     "degrade_to=UnsupportedTransformation -- the engine's OWN class for an identified element it "
     "cannot translate, so still no spelling is invented, and the census gate reads the MISSING "
     "element.$kind slot rather than the emitted string, so it stays NotSupported). Target "
     "Definition is PROMOTED (ir_kind=TargetTransformation) and the check asserts its REQUIRED "
     "element_fields are populated -- promotion without the payload is the silent upgrade the "
     "original form of this check existed to catch",
     lambda: chk_degraded_kinds()),
    (5, "ARBITRARY", "node type value 'target'", TABLE,
     "role_to_node_type; INSTANCE/@TYPE is structural, the mapping is table, and the "
     "table records the downstream defect explicitly",
     lambda: (node("MyReportTable")["type"] == "target", node("MyReportTable")["type"])),
    (6, "ARBITRARY", "ordering of OutputColumns", TABLE,
     "port_policy.output_column_order=TRANSFORMFIELD_DOCUMENT_ORDER",
     lambda: ([c["Name"] for c in node("INCR_SALARY")["element"]["OutputColumns"]]
              == ["NAME", "THE_SALARY", "NEW_SALARY"],
              str([c["Name"] for c in node("INCR_SALARY")["element"]["OutputColumns"]]))),
    (7, "ARBITRARY", "whether to include Scale: 0 explicitly", TABLE,
     "port_policy.emit_scale_when_zero",
     lambda: ("Scale" in outcol("INCR_SALARY", "NAME"), "Scale present")),
    (8, "ARBITRARY", "Router group name as the edge label", TABLE,
     "edge_policy.label_source=OUTPUT_GROUP_NAME_WHEN_PRESENT; the VALUE is read from "
     "TRANSFORMFIELD/@GROUP of the source port, the policy is table",
     lambda: (next(e for e in ir["edges"]
                   if e["from"] == eid("SALARY_RTRTRANS"))["label"] == "HIGH_SALARY"
              and all("label" not in e for e in ir["edges"]
                      if e["from"] != eid("SALARY_RTRTRANS")),
              "HIGH_SALARY on 1 edge, absent on 4")),

    (9, "PLAUSIBLE", "InputColumns: upstream field vs local port name", TABLE,
     "port_policy.input_column_naming=UPSTREAM_FIELD; both facts are structural, "
     "the choice is table",
     lambda: (incols("INCR_SALARY") == ["NAME", "SALARY"], str(incols("INCR_SALARY")))),
    (10, "PLAUSIBLE", "rewriting port references to the upstream projected name", DETERMINED,
     "connector graph + closed port-name set; no policy involved",
     lambda: (outcol("INCR_SALARY", "THE_SALARY")["Expression"] == "SALARY"
              and outcol("EXPTRANS", "NAME")["Expression"] == "NAME1"
              and outcol("EXPTRANS1", "op1")["Expression"] == "NEW_NAME",
              "THE_SALARY<-SALARY, NAME<-NAME1, op1<-NEW_NAME")),
    (11, "PLAUSIBLE", "inlining SALARY_TMP", TABLE,
     "port_policy.inline_local_variables; DETECTION of PORTTYPE='LOCAL VARIABLE' is "
     "structural, the decision to inline is table",
     lambda: (outcol("INCR_SALARY", "NEW_SALARY")["Expression"] == "(SALARY*0.13) + SALARY",
              outcol("INCR_SALARY", "NEW_SALARY")["Expression"])),
    (12, "PLAUSIBLE", "dropping SALARY_TMP from OutputColumns", TABLE,
     "port_policy.drop_local_variables_from_outputs",
     lambda: (outcol("INCR_SALARY", "SALARY_TMP") is None, "absent")),
    (13, "PLAUSIBLE", "EXPTRANS.Description = '<No description>'", TABLE,
     "default_value_policy.literal_default_on_unconnected_input; DETECTION "
     "(input port with no inbound CONNECTOR, non-ERROR default) is structural",
     lambda: (outcol("EXPTRANS", "Description")["Expression"] == "'<No description>'",
              outcol("EXPTRANS", "Description")["Expression"])),
    (14, "PLAUSIBLE", "excluding Description from EXPTRANS.InputColumns", DETERMINED,
     "InputColumns are generated FROM inbound connectors, so an unconnected port "
     "cannot appear; no exclusion rule is needed",
     lambda: (incols("EXPTRANS") == ["NAME1"], str(incols("EXPTRANS")))),
    (15, "PLAUSIBLE", "keeping || for string concatenation", RESIDUE,
     "dialect table FLAGS the NULL divergence mechanically; what to emit instead "
     "is a model decision",
     lambda: (outcol("EXPTRANS", "NEW_NAME")["Expression"] == "NAME1 || '!!!'",
              "flagged RESIDUE, emitted literally")),
    (16, "PLAUSIBLE", "COALESCE-wrapping the synthesised default-group condition", RESIDUE,
     "GROUP[@TYPE='OUTPUT/DEFAULT'] is DETECTED structurally; deriving its condition "
     "incl. NULL routing needs Router semantics",
     lambda: (any(s.path.startswith("!router_default_group") for s in em.slots),
              "detected and reported as RESIDUE")),
    (17, "PLAUSIBLE", "carrying Informatica-native type names", TABLE,
     "type_vocabulary.carry=INFORMATICA_NATIVE",
     lambda: (outcol("INCR_SALARY", "NEW_SALARY")["DataType"] == "double",
              outcol("INCR_SALARY", "NEW_SALARY")["DataType"])),
    (18, "PLAUSIBLE", "SQ Informatica port types vs SOURCEFIELD SQL Server types", TABLE,
     "type_vocabulary.collapsed_source_type_from=SOURCE_QUALIFIER_TRANSFORMFIELD",
     lambda: (outcol("SQ_EMPLOYEE", "NAME")["DataType"] == "string",
              outcol("SQ_EMPLOYEE", "NAME")["DataType"] + " (not varchar)")),
    (19, "PLAUSIBLE", "normalising the_salary to THE_SALARY", DETERMINED,
     "case-insensitive match against the closed port-name set; port_policy records "
     "the case-insensitivity, the normalised value is structural",
     chk_case_insensitive),
    (20, "PLAUSIBLE", "leaving Description and desc unquoted", TABLE,
     "a Snowflake reserved-word list is a lookup, not a judgement — but NO such table "
     "entry was written in this spike, so this is TABLE-in-principle only",
     None),

    (21, "CONFIDENT", "element-level edge set", DETERMINED,
     "DISTINCT (FROMINSTANCE, TOINSTANCE) over CONNECTOR",
     lambda: (len(ir["edges"]) == 5 and len(idn.field_edges) == 13,
              f"{len(idn.field_edges)} connectors -> {len(ir['edges'])} edges")),
    (22, "CONFIDENT", "which ports are inputs of each node", DETERMINED,
     "filter CONNECTOR on TOINSTANCE",
     lambda: ("DEPARTMENT" not in incols("INCR_SALARY"),
              "DEPARTMENT structurally absent from INCR_SALARY inputs")),
    (23, "CONFIDENT", "the arithmetic of NEW_SALARY", DETERMINED,
     "textual substitution of the LOCAL VARIABLE expression",
     lambda: ("(SALARY*0.13) + SALARY" == outcol("INCR_SALARY", "NEW_SALARY")["Expression"],
              outcol("INCR_SALARY", "NEW_SALARY")["Expression"])),
]


def main() -> int:
    counts = {DETERMINED: 0, TABLE: 0, RESIDUE: 0}
    prior = {}
    failures = []
    print("=" * 100)
    print("THE 23 DECISIONS, RECLASSIFIED   (check = EXECUTED against the emitted IR)")
    print("=" * 100)
    print(f"{'#':>3} {'was':<10} {'now':<11} {'chk':<5} decision")
    print("-" * 100)
    for n, was, title, bucket, mech, check in DECISIONS:
        counts[bucket] += 1
        prior.setdefault(was, {DETERMINED: 0, TABLE: 0, RESIDUE: 0})
        prior[was][bucket] += 1
        if check is None:
            status, evidence = "n/a", "no check"
        else:
            ok, evidence = check()
            status = "PASS" if ok else "FAIL"
            if not ok:
                failures.append((n, evidence))
        print(f"{n:>3} {was:<10} {bucket:<11} {status:<5} {title}")
        print(f"    mechanism: {mech}")
        print(f"    evidence : {evidence}")
    print("-" * 100)
    print(f"DETERMINED {counts[DETERMINED]}   TABLE {counts[TABLE]}   RESIDUE {counts[RESIDUE]}"
          f"   (total {sum(counts.values())})")
    print(f"mechanised = DETERMINED + TABLE = {counts[DETERMINED] + counts[TABLE]}/23")
    print()
    print("by baseline rating:")
    for was in ("ARBITRARY", "PLAUSIBLE", "CONFIDENT"):
        d = prior[was]
        tot = sum(d.values())
        print(f"  {was:<10} n={tot:<3} -> DETERMINED {d[DETERMINED]}  TABLE {d[TABLE]}  "
              f"RESIDUE {d[RESIDUE]}")
    print()
    if failures:
        print(f"CHECK FAILURES ({len(failures)}):")
        for n, ev in failures:
            print(f"  #{n}: {ev}")
        return 1
    checked = sum(1 for d in DECISIONS if d[5] is not None)
    print(f"ALL {checked} CHECKS PASS  ({23 - checked} decision has no executable check)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
