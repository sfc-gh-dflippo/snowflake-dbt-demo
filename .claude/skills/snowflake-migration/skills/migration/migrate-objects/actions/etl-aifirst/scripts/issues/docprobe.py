"""DOCUMENT PROBES: how many output branches does the document declare for an element?

WHY A SEPARATE, PER-PLATFORM PROBE
----------------------------------
The multi-output-branching issue cannot be seen from the representation alone. The
representation carries one outbound edge; the question is whether the DOCUMENT declared
more. So the count has to come from the file, by a rule stated in the output, exactly as
the coverage gate derives its element baseline from the file rather than from the sweep
that is under test. A count derived from the thing being checked cannot detect what that
thing never saw.

WHAT IS DELIBERATELY NOT COUNTED
--------------------------------
Error outputs and outputs the document marks as unconnected. Both would make the probe
cry wolf: a two-branch element whose second branch goes nowhere in the source has not
lost a data path when the representation carries one edge, and reporting it as a loss
would be a false positive in a detector whose whole value is that it does not produce
them. Measured: the one conditional split in the four blind documents declares two
outputs, of which the default one is marked unconnected -- so this probe reports one
branch for it and the detector correctly stays quiet.

A PLATFORM WITH NO RULE HERE RETURNS None, NOT ZERO. Zero would read as "no branches
declared" and make the detector claim a collapse that nothing measured.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET


def _local(tag: str) -> str:
    return tag.split("}")[-1]


def _att(el) -> dict:
    return {_local(k): v for k, v in el.attrib.items()}


BRANCH_RULES = {
    "SqlServerIntegrationServices": (
        "dtsx.output-branch.v1",
        "one branch per <output> child of a <component>'s <outputs>, EXCLUDING "
        "@isErrorOut='true' and @dangling='true'. Keyed by the component's @refId and "
        "@name.",
    ),
    "InformaticaPowerCenter": (
        "infa.group.v1",
        "one branch per GROUP child of a TRANSFORMATION that carries an @EXPRESSION. A "
        "transformation with no GROUP children declares no branching under this rule.",
    ),
    "PentahoDataIntegration": (
        "ktr.hop.v1",
        "one branch per <hop> whose <from> is this step's <name> and whose <enabled> is "
        "Y. Keyed by step name.",
    ),
    "IbmInfoSphereDataStage": (
        "dsx.outputpins.v1",
        "one branch per identifier listed in the record's OutputPins property. Keyed by "
        "the record's Identifier and Name.",
    ),
}


def _ssis(path):
    out = {}
    root = ET.parse(path).getroot()
    for comp in root.iter():
        if _local(comp.tag) != "component":
            continue
        a = _att(comp)
        n = 0
        for o in comp.iter():
            if _local(o.tag) != "output":
                continue
            oa = _att(o)
            if oa.get("isErrorOut") == "true" or oa.get("dangling") == "true":
                continue
            n += 1
        rec = {"branches": n, "evidence": f"component[@refId={a.get('refId')!r}]"}
        for k in (a.get("refId"), a.get("name")):
            if k:
                out[k.casefold()] = rec
    return out


def _informatica(path):
    out = {}
    root = ET.parse(path).getroot()
    for t in root.iter():
        if _local(t.tag) != "TRANSFORMATION":
            continue
        a = _att(t)
        n = sum(1 for g in t.iter()
                if _local(g.tag) == "GROUP" and _att(g).get("EXPRESSION"))
        rec = {"branches": n, "evidence": f"TRANSFORMATION[@NAME={a.get('NAME')!r}]"}
        if a.get("NAME"):
            out[a["NAME"].casefold()] = rec
    return out


def _pentaho(path):
    out = {}
    root = ET.parse(path).getroot()
    for hop in root.iter():
        if _local(hop.tag) != "hop":
            continue
        frm = to = enabled = None
        for c in hop:
            if _local(c.tag) == "from":
                frm = (c.text or "").strip()
            elif _local(c.tag) == "to":
                to = (c.text or "").strip()
            elif _local(c.tag) == "enabled":
                enabled = (c.text or "").strip()
        if not frm or (enabled or "Y").upper() != "Y":
            continue
        rec = out.setdefault(frm.casefold(),
                             {"branches": 0, "evidence": f"hop[from={frm!r}]"})
        rec["branches"] += 1
        rec["evidence"] = f"hop[from={frm!r}] -> {to!r} (and any siblings)"
    return out


_DSREC = re.compile(r"BEGIN DSRECORD(.*?)END DSRECORD", re.S)
_PROP = re.compile(r'^\s*(\w+)\s+"(.*)"\s*$', re.M)


def _datastage(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    out = {}
    for block in _DSREC.findall(text):
        props = dict(_PROP.findall(block))
        pins = props.get("OutputPins")
        if pins is None:
            continue
        n = len([p for p in re.split(r"[\s,]+", pins) if p])
        rec = {"branches": n,
               "evidence": f"DSRECORD Identifier={props.get('Identifier')!r} "
                           f"OutputPins={pins!r}"}
        for k in (props.get("Identifier"), props.get("Name")):
            if k:
                out[k.casefold()] = rec
    return out


_PROBES = {
    "SqlServerIntegrationServices": _ssis,
    "InformaticaPowerCenter": _informatica,
    "PentahoDataIntegration": _pentaho,
    "IbmInfoSphereDataStage": _datastage,
}


def declared_branches(platform: str, doc_path: str):
    """(rule_id, rule_text, {element-key -> {branches, evidence}}) or (None, None, None)
    when this platform has no rule here -- which is reported as unmeasured, never as
    zero."""
    if platform not in _PROBES:
        return None, None, None
    rule_id, rule_text = BRANCH_RULES[platform]
    try:
        return rule_id, rule_text, _PROBES[platform](doc_path)
    except (OSError, ET.ParseError) as exc:
        return rule_id, f"{rule_text} [PROBE FAILED: {exc}]", None
