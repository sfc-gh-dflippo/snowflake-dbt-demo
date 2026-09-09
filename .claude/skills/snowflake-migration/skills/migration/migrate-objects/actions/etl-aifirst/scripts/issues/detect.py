"""DETECTORS: what a run OBSERVED, read off the representation, the artifact and the
document. Each one is a proposal to the inventory, not a write.

THE DISCIPLINE EVERY DETECTOR FOLLOWS
-------------------------------------
It states what it READ and where it read it. It never states what the source platform
would have done. That is not a style preference: a sweep of the engine's own catalogue
found 33 texts asserting source-platform runtime behaviour, all of them in the two ETL
dialects, and the worst asks a reviewer to verify a consequence of a premise about a
platform this pipeline has never run. On an unsupported platform such a premise is a
guess wearing the clothes of a diagnostic.

So a detector's output is of the form "the document declares X, the representation
carries Y, the artifact contains Z", with the field or file each was read from recorded
on the instance. What that MEANS for the customer's data is left to a reviewer, who has
the source system and we do not.

RELATION TO PROVENANCE, WHICH THIS IS NOT
-----------------------------------------
`SSC-AI-AUTHORED` and the MODEL provenance class answer "who produced this artifact".
These detectors answer "what went wrong". A model-authored model with no issues and an
engine-rendered model with three are both possible and both real. One detector here does
read the AI-authored stamp -- but for the REASON recorded in it, which is a statement
about what the renderer could not do, not for the authorship, which the stamp already
carries and this framework does not restate.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import docprobe

# Markers this framework READS from the artifact but must never WRITE into it: a
# separate gate counts these strings across the whole output tree, so echoing one into
# our own report would corrupt that gate's measurement. Same file, two readers, one of
# them counting -- the reason this list exists at all.
BLOCKING_MARKER = "!!!RESOLVE" + " EWI!!!"
PRODUCER_SENTINEL = "__PRODUCER_EXPRESSION" + "_NOT_CONVERTED__"
AUTHORED_MARKER = "SSC-AI-" + "AUTHORED"

CONTAINER_ROLES = {"TASK", "JOB", "UNIT_OF_WORK", "CONTAINER", "PACKAGE"}


@dataclass
class Finding:
    """One observation. `proposal` is the TYPE it argues for; the rest is the INSTANCE."""
    proposal: dict
    element: str = ""
    element_id: str = ""
    native_kind: str = ""
    detail: str = ""
    evidence: str = ""
    location: str = ""
    detector: str = ""


@dataclass
class RunInputs:
    platform: str
    table: dict
    doc_path: str
    ir: dict | None
    out_root: Path
    notes: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ small helpers
def _kind_entry(table: dict, kind: str) -> dict:
    return (table.get("kind_dispatch") or {}).get(kind) or {}


def _node_keys(node: dict) -> set[str]:
    keys = set()
    nid = node.get("id") or ""
    if nid:
        keys.add(nid.casefold())
        keys.add(re.split(r"[\\/]", nid)[-1].casefold())
    name = (node.get("element") or {}).get("Name")
    if name:
        keys.add(str(name).casefold())
    return keys


def _cols(el: dict, which: str) -> list[dict]:
    return el.get(which) or []


def _models(out_root: Path) -> list[Path]:
    """Every emitted model, with dbt's own copies pruned.

    `target/` holds dbt's compiled duplicate of every model and
    `dbt_internal_packages/` ships whole vendored dbt projects. Counting either doubles
    every number and makes a re-inspection of the same tree score differently from the
    first pass -- measured on this driver's other gates before the prune existed.
    """
    out = []
    for p in out_root.rglob("*.sql"):
        parts = set(p.parts)
        if "target" in parts or "dbt_internal_packages" in parts:
            continue
        if "models" not in parts:
            continue
        out.append(p)
    return out


def _model_for(node: dict, models: list[Path]) -> Path | None:
    mn = node.get("modelName")
    if not mn:
        return None
    for m in models:
        if m.stem in (mn, f"int_{mn}", f"stg_raw__{mn}") or m.stem.endswith(f"__{mn}"):
            return m
    return None


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


# =====================================================================================
# REPRESENTATION DETECTORS -- read from the IR the producer emitted, plus the platform
# table's own declaration of what it maps.
# =====================================================================================
def detect_unrepresented_elements(run: RunInputs) -> list[Finding]:
    """A node the representation has no member for.

    Two shapes, kept as two signatures because a reviewer does different things about
    them: an element that CONTAINS others (no model can exist for it, its children are
    carried flat), and a leaf element that carries data (a model exists and is hollow).
    """
    found = []
    for node in (run.ir or {}).get("nodes", []):
        el = node.get("element") or {}
        native = el.get("_unsupported")
        if not native or el.get("$kind") is not None:
            continue
        role = (_kind_entry(run.table, native).get("role") or "").upper()
        container = role in CONTAINER_ROLES
        if container:
            proposal = {
                "category": "REPR", "construct": "element:containment-scope",
                "reason": "no-vocabulary-member",
                "title": "Element kind with no member in the representation for a "
                         "containment scope",
                "text": "The document declares an element of kind '{kind}' named "
                        "'{element}' that contains other elements. The representation "
                        "this migration uses is a flat graph of data-flow elements with "
                        "no member for an element that contains others, so it is "
                        "carried as an unrepresented node: no model is generated from "
                        "it, and whatever it declares about the elements inside it is "
                        "not carried. {detail}",
                "impact": "output-incomplete",
                "distinguisher": "the element contains other elements, so no model can "
                                 "exist for it at all; the leaf case has a model that "
                                 "is hollow.",
            }
            detail = f"the declared role for this kind is {role!r}."
        else:
            proposal = {
                "category": "REPR", "construct": "element:transformation",
                "reason": "no-vocabulary-member",
                "title": "Element kind with no member in the representation, and it "
                         "carries data",
                "text": "The document declares an element of kind '{kind}' named "
                        "'{element}' that sits on a data path. The representation this "
                        "migration uses has no member for that kind, so the element is "
                        "carried as an unrepresented node and any artifact generated "
                        "for it names no columns and computes nothing. {detail}",
                "impact": "output-absent",
                "distinguisher": "a leaf element on a data path, as opposed to a "
                                 "containment scope: here a model exists and is hollow, "
                                 "rather than no model existing at all.",
            }
            detail = f"the declared role for this kind is {role or 'unset'!r}."
        found.append(Finding(
            proposal=proposal, element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""), native_kind=str(native),
            detail=detail,
            evidence=f"IR node element.$kind is null and element._unsupported="
                     f"{native!r}; platform table kind_dispatch[{native!r}]"
                     f".ir_kind is null",
            detector="unrepresented_elements"))
    return found


def detect_degraded_to_catch_all(run: RunInputs) -> list[Finding]:
    """A node carrying the table's fallback class instead of a class for its own kind.

    Distinct from the case above: the node IS in the graph with its edges intact, which
    is why the fallback exists, and the loss is everything the kind meant.
    """
    found = []
    for node in (run.ir or {}).get("nodes", []):
        el = node.get("element") or {}
        kind = el.get("$kind") or ""
        native = el.get("_unsupported")
        # A sidecar can overwrite $kind (ExpressionTransformation passthrough) while the
        # platform table still refuses the native kind. That is the same loss as the
        # catch-all class: the node is in the graph, the kind's payload is not.
        authored = any((m.get("path") or "") == "element.$kind"
                       for m in (node.get("modelAuthored") or []))
        if "Unsupported" not in kind and not authored:
            continue
        entry = _kind_entry(run.table, native or "")
        found.append(Finding(
            proposal={
                "category": "REPR", "construct": "element:transformation",
                "reason": "degraded-to-catch-all-class",
                "title": "Element carried under a fallback class, not one for its own "
                         "kind",
                "text": "Element '{element}' of kind '{kind}' is carried in the "
                        "representation under the fallback class '{detail}' rather than "
                        "a class for its own kind. Its position in the graph and its "
                        "edges are kept; what the kind itself declares is not carried, "
                        "so an artifact generated from it names its columns and "
                        "computes none of their values.",
                "impact": "output-incomplete",
                "distinguisher": "the node reaches the representation and keeps its "
                                 "edges under a fallback class. The no-vocabulary-member "
                                 "types describe a node with no class at all, which is "
                                 "a different repair: one needs a class, this one needs "
                                 "the kind's payload.",
            },
            element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""), native_kind=str(native or "unknown"),
            detail=kind,
            evidence=f"IR node element.$kind={kind!r}; platform table "
                     f"kind_dispatch[{native!r}].degrade_to={entry.get('degrade_to')!r}",
            detector="degraded_to_catch_all"))
    return found


def detect_unmapped_role(run: RunInputs) -> list[Finding]:
    """A node whose 'type' is the table's own placeholder for a role it does not map."""
    placeholder = ((run.table.get("role_to_node_type") or {})
                   .get("unmapped_role_node_type") or "unknown")
    found = []
    for node in (run.ir or {}).get("nodes", []):
        if node.get("type") != placeholder:
            continue
        el = node.get("element") or {}
        native = el.get("_unsupported") or el.get("$kind") or "unknown"
        found.append(Finding(
            proposal={
                "category": "REPR", "construct": "element:role",
                "reason": "no-vocabulary-member",
                "title": "Element role not named by the representation's node-type "
                         "vocabulary",
                "text": "Element '{element}' of kind '{kind}' has a role this "
                        "migration's node-type vocabulary does not name, so its node "
                        "carries the placeholder type '{detail}'. A consumer that "
                        "branches on node type therefore takes the same path for this "
                        "element as for one whose role it could not determine.",
                "impact": "output-unverified",
                "distinguisher": "the KIND is mapped and the ROLE is not, so the "
                                 "element's payload is carried correctly and only its "
                                 "classification is missing. The other "
                                 "no-vocabulary-member types lose the payload.",
            },
            element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""), native_kind=str(native),
            detail=placeholder,
            evidence=f"IR node type={placeholder!r}, which the platform table declares "
                     f"as role_to_node_type.unmapped_role_node_type",
            detector="unmapped_role"))
    return found


def detect_column_less_elements(run: RunInputs) -> list[Finding]:
    """A node with no columns on either side.

    Conservative on purpose: a source with no INPUT columns is normal and a target with
    no OUTPUT columns is normal, so only an element with neither fires. A wider rule
    would report every source and target on every platform.
    """
    found = []
    for node in (run.ir or {}).get("nodes", []):
        el = node.get("element") or {}
        if el.get("$kind") is None and el.get("_unsupported"):
            continue  # already reported as unrepresented; not a second issue
        if _cols(el, "InputColumns") or _cols(el, "OutputColumns"):
            continue
        found.append(Finding(
            proposal={
                "category": "SHAPE", "construct": "element:column-set",
                "reason": "not-declared-by-document",
                "title": "No column metadata for an element",
                "text": "Element '{element}' of kind '{kind}' is represented with no "
                        "input columns and no output columns. The document states none "
                        "at the place this migration's rule looks for them, so nothing "
                        "generated from this element can name a column and a generated "
                        "artifact for it can only project a placeholder. {detail}",
                "impact": "output-incomplete",
                "distinguisher": "seed",
            },
            element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""),
            native_kind=str(el.get("_unsupported") or el.get("$kind") or "unknown"),
            detail="Both column lists are empty in the representation.",
            evidence="IR node element.InputColumns and element.OutputColumns are both "
                     "empty or absent",
            detector="column_less_elements"))
    return found


def detect_columns_without_a_recipe(run: RunInputs) -> list[Finding]:
    """An output column the representation cannot produce a value for.

    The rule, entirely inside the representation and platform-neutral: for a node that
    is not a source, an output column that is (a) not available from any upstream node's
    outputs and (b) carries no expression, has a value nothing in the representation
    states. Sources are excluded because their columns come from a relation and not from
    an upstream node.

    This is what "an expression dialect with no lowering" looks like from the artifact
    side, and it is stated that way -- as a missing recipe -- rather than as a claim
    about which dialect the source used, which the instance records separately as an
    observed kind.
    """
    ir = run.ir or {}
    nodes = {n.get("id"): n for n in ir.get("nodes", [])}
    upstream: dict[str, set[str]] = {}
    for e in ir.get("edges", []) or []:
        upstream.setdefault(e.get("to"), set()).add(e.get("from"))
    # Edge endpoints may be stated in the document's own id space rather than the node
    # id space, so resolve by the same key set the coverage gate matches on.
    keymap = {}
    for nid, n in nodes.items():
        for k in _node_keys(n):
            keymap[k] = nid

    def resolve(ref):
        return keymap.get(str(ref).casefold()) or keymap.get(
            re.split(r"[\\/]", str(ref))[-1].casefold())

    found = []
    for nid, node in nodes.items():
        if node.get("type") == "source":
            continue
        el = node.get("element") or {}
        if el.get("$kind") is None and el.get("_unsupported"):
            continue  # unrepresented: already reported, once, as itself
        ups = set()
        for ref in upstream.get(nid, set()) | {
                r for k, v in upstream.items() if resolve(k) == nid for r in v}:
            rid = resolve(ref)
            if rid and rid in nodes:
                ups |= {c.get("Name") for c in
                        _cols(nodes[rid].get("element") or {}, "OutputColumns")}
        if not ups:
            continue  # nothing upstream resolved: not evidence about this column
        own_in = {c.get("Name") for c in _cols(el, "InputColumns")}
        for col in _cols(el, "OutputColumns"):
            name = col.get("Name")
            if col.get("Expression") or name in ups or name in own_in:
                continue
            found.append(Finding(
                proposal={
                    "category": "EXPR", "construct": "column:value-derivation",
                    "reason": "not-carried-into-representation",
                    "title": "An output column has no derivation in the representation",
                    "text": "Element '{element}' of kind '{kind}' declares the output "
                            "column '{detail}', which is not among the columns "
                            "available from its upstream elements, and the "
                            "representation carries no expression for it. The value of "
                            "that column is produced by something the representation "
                            "does not state, so a generated artifact can name the "
                            "column and cannot compute it.",
                    "impact": "output-incomplete",
                    "distinguisher": "here the derivation text never reached the "
                                     "representation at all, so there is nothing to "
                                     "lower; the no-lowering type covers text that WAS "
                                     "read and has no path to the target dialect. The "
                                     "repairs differ: one needs an extraction rule, the "
                                     "other needs a translator.",
                },
                element=str(el.get("Name") or nid), element_id=str(nid),
                native_kind=str(el.get("_unsupported") or el.get("$kind") or "unknown"),
                detail=str(name),
                evidence=f"IR: output column {name!r} absent from upstream output "
                         f"columns {sorted(x for x in ups if x)!r} and carries no "
                         f"Expression",
                detector="columns_without_a_recipe"))
    return found


def detect_missing_predicate(run: RunInputs) -> list[Finding]:
    """A row-selection element the representation carries no condition for."""
    found = []
    for node in (run.ir or {}).get("nodes", []):
        el = node.get("element") or {}
        kind = el.get("$kind") or ""
        if "Filter" not in kind:
            continue
        conds = el.get("FilterConditions")
        if isinstance(conds, str):
            has = bool(conds.strip())
        else:
            has = bool(conds)
        if has:
            continue
        found.append(Finding(
            proposal={
                "category": "PRED", "construct": "predicate:row-filter",
                "reason": "not-extractable-by-any-rule",
                "title": "Row-selection condition not obtained by any extraction rule",
                "text": "Element '{element}' of kind '{kind}' is represented as a "
                        "row-selection step and the representation carries no condition "
                        "for it. No extraction rule in this migration obtained one from "
                        "the document. A row-selection step with no condition must not "
                        "be generated as one that keeps every row, because that changes "
                        "which rows reach the output while looking correct, so no "
                        "selection is generated here at all. {detail}",
                "impact": "output-incomplete",
                "distinguisher": "seed",
            },
            element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""),
            native_kind=str(el.get("_unsupported") or kind),
            detail="The representation's condition field is empty.",
            evidence="IR node element.FilterConditions is empty or absent",
            detector="missing_predicate"))
    return found


def detect_branch_collapse(run: RunInputs) -> list[Finding]:
    """The document declares more connected output branches than the graph carries."""
    rule_id, rule_text, declared = docprobe.declared_branches(run.platform, run.doc_path)
    if rule_id is None:
        run.notes.append(f"branch probe: no rule for platform {run.platform!r} — "
                         f"branch collapse UNMEASURED on this document (not reported "
                         f"as zero)")
        return []
    if declared is None:
        run.notes.append(f"branch probe [{rule_id}]: FAILED — {rule_text}")
        return []
    run.notes.append(f"branch probe [{rule_id}]: {len(declared)} element(s) probed")

    ir = run.ir or {}
    outdeg: dict[str, int] = {}
    keymap = {}
    for n in ir.get("nodes", []):
        for k in _node_keys(n):
            keymap[k] = n.get("id")
    for e in ir.get("edges", []) or []:
        src = keymap.get(str(e.get("from")).casefold()) or e.get("from")
        outdeg[src] = outdeg.get(src, 0) + 1

    found = []
    for node in ir.get("nodes", []):
        el = node.get("element") or {}
        rec = None
        for k in _node_keys(node):
            if k in declared:
                rec = declared[k]
                break
        if not rec or rec["branches"] < 2:
            continue
        carried = outdeg.get(node.get("id"), 0)
        if carried >= rec["branches"]:
            continue
        found.append(Finding(
            proposal={
                "category": "SHAPE", "construct": "element:multi-output-branching",
                "reason": "branches-collapsed-in-representation",
                "title": "Fewer output branches in the representation than the document "
                         "declares",
                "text": "The document declares {detail} for element '{element}' of kind "
                        "'{kind}'. The representation carries fewer of them. The "
                        "branches that are not carried, and the conditions the document "
                        "states for them, are absent from the output, and nothing "
                        "generated here refers to them.",
                "impact": "output-incomplete",
                "distinguisher": "seed",
            },
            element=str(el.get("Name") or node.get("id")),
            element_id=str(node.get("id") or ""),
            native_kind=str(el.get("_unsupported") or el.get("$kind") or "unknown"),
            detail=f"{rec['branches']} connected output branch(es) under rule "
                   f"{rule_id}, of which the representation carries {carried}",
            evidence=f"{rule_id} at {rec['evidence']}; IR out-degree {carried}",
            detector="branch_collapse"))
    return found


# =====================================================================================
# ARTIFACT DETECTORS -- read from the emitted tree. Counted from the files, never from
# the emitter's own account of what it did.
# =====================================================================================
def detect_unresolvable_references(run: RunInputs) -> list[Finding]:
    """A generated reference naming a unit that is not in the output."""
    models = _models(run.out_root)
    by_project: dict[Path, set[str]] = {}
    for m in models:
        proj = m
        while proj.parent != proj and proj.name != "models":
            proj = proj.parent
        by_project.setdefault(proj.parent, set()).add(m.stem)
    found = []
    for m in models:
        proj = m
        while proj.parent != proj and proj.name != "models":
            proj = proj.parent
        known = by_project.get(proj.parent, set())
        text = m.read_text(encoding="utf-8", errors="replace")
        for ref in re.findall(r"ref\(\s*['\"]([^'\"]+)['\"]\s*\)", text):
            if ref in known:
                continue
            found.append(Finding(
                proposal={
                    "category": "REF", "construct": "reference:upstream-element",
                    "reason": "reference-does-not-resolve",
                    "title": "A generated reference names a unit that is not in the "
                             "output",
                    "text": "A generated artifact for element '{element}' references "
                            "the unit '{detail}', and no generated unit of that name is "
                            "present in the output. The reference cannot resolve, so "
                            "the artifact cannot run as generated. This states a defect "
                            "in the generated output and claims nothing about the "
                            "document.",
                    "impact": "output-absent",
                    "distinguisher": "seed",
                },
                element=m.stem, element_id=_rel(m, run.out_root),
                native_kind="", detail=ref,
                evidence=f"{_rel(m, run.out_root)} references {ref!r}; the project at "
                         f"{_rel(proj.parent, run.out_root)} declares "
                         f"{len(known)} model(s) and none of that name",
                location=_rel(m, run.out_root),
                detector="unresolvable_references"))
    return found


def detect_edges_absent_from_artifact(run: RunInputs) -> list[Finding]:
    """An edge the representation carries that the generated artifact does not.

    The representation states the graph; the artifact states it again as references. If
    the downstream artifact never names the upstream one, the lineage the document
    declared is not in the output -- so the models exist and the graph does not.
    """
    ir = run.ir or {}
    models = _models(run.out_root)
    nodes = {n.get("id"): n for n in ir.get("nodes", [])}
    keymap = {}
    for nid, n in nodes.items():
        for k in _node_keys(n):
            keymap[k] = nid
    found = []
    for e in ir.get("edges", []) or []:
        src = keymap.get(str(e.get("from")).casefold())
        dst = keymap.get(str(e.get("to")).casefold())
        if not src or not dst:
            continue
        smodel = _model_for(nodes[src], models)
        dmodel = _model_for(nodes[dst], models)
        if not smodel or not dmodel:
            continue
        text = dmodel.read_text(encoding="utf-8", errors="replace")
        refs = set(re.findall(r"ref\(\s*['\"]([^'\"]+)['\"]\s*\)", text))
        if smodel.stem in refs:
            continue
        el = nodes[dst].get("element") or {}
        found.append(Finding(
            proposal={
                "category": "REF", "construct": "reference:upstream-element",
                "reason": "edge-absent-from-artifact",
                "title": "An edge in the representation is not present in the generated "
                         "artifact",
                "text": "The representation carries an edge from '{detail}' into "
                        "element '{element}', and the generated artifact for "
                        "'{element}' names no reference to the artifact generated for "
                        "the upstream element. Both artifacts exist and the edge "
                        "between them does not, so the generated graph is not the graph "
                        "the representation states.",
                "impact": "output-incomplete",
                "distinguisher": "the reference is ABSENT, not dangling. A dangling "
                                 "reference fails loudly when the artifact is compiled; "
                                 "a missing one compiles cleanly and quietly drops the "
                                 "upstream element out of the graph, which no compile "
                                 "step will report.",
            },
            element=str(el.get("Name") or dst), element_id=str(dst),
            native_kind=str(el.get("_unsupported") or el.get("$kind") or "unknown"),
            detail=str((nodes[src].get("element") or {}).get("Name") or src),
            evidence=f"{_rel(dmodel, run.out_root)} references {sorted(refs)!r}, which "
                     f"does not include {smodel.stem!r}",
            location=_rel(dmodel, run.out_root),
            detector="edges_absent_from_artifact"))
    return found


def detect_renderer_failures(run: RunInputs) -> list[Finding]:
    """A generated model carrying a blocking marker: the renderer raised on this element.

    The marker itself is the engine's, and on a platform the engine supports it is
    accurate. It is recorded here because on a platform the engine does NOT support
    there is no lawful marker to emit -- the not-supported vocabulary has two members
    and both name a platform -- so this is the type that has to carry the same fact when
    the engine's own channel cannot.
    """
    found = []
    for m in _models(run.out_root):
        text = m.read_text(encoding="utf-8", errors="replace")
        if BLOCKING_MARKER not in text and PRODUCER_SENTINEL not in text:
            continue
        which = ("a blocking unresolved-issue marker" if BLOCKING_MARKER in text
                 else "a producer expression sentinel")
        found.append(Finding(
            proposal={
                "category": "EMIT", "construct": "model:rendered-output",
                "reason": "renderer-raised-an-error",
                "title": "A generated model carries a marker that stops it from being "
                         "used",
                "text": "The generated artifact '{element}' carries {detail}. The "
                        "renderer did not produce usable output for this element, and "
                        "the marker is in the file so that anything compiling it fails "
                        "rather than running it. Nothing here establishes what the "
                        "artifact should have contained.",
                "impact": "output-absent",
                "distinguisher": "this is about the RENDERER, not the representation: "
                                 "the element was represented and the step that writes "
                                 "the artifact failed. The representation-side types "
                                 "describe elements that never got that far.",
            },
            element=m.stem, element_id=_rel(m, run.out_root), native_kind="",
            detail=which,
            evidence=f"{_rel(m, run.out_root)} contains {which}",
            location=_rel(m, run.out_root),
            detector="renderer_failures"))
    return found


def detect_filled_models(run: RunInputs) -> list[Finding]:
    """A model a model wrote because the renderer produced nothing usable.

    THE ISSUE IS THE REASON IN THE STAMP, NOT THE AUTHORSHIP. Authorship is provenance
    and the stamp already carries it; restating it here would put one fact on two axes.
    What is recorded is the reason the fill was needed -- a statement about what the
    renderer could not do -- with the reason text quoted verbatim from the stamp so a
    reviewer can see the claim as written.
    """
    found = []
    for m in _models(run.out_root):
        text = m.read_text(encoding="utf-8", errors="replace")
        if AUTHORED_MARKER not in text:
            continue
        reason = ""
        for line in text.splitlines():
            if line.strip().startswith("-- Reason"):
                reason = line.split(":", 1)[-1].strip()
                break
        found.append(Finding(
            proposal={
                "category": "EMIT", "construct": "model:rendered-output",
                "reason": "no-usable-output-from-the-renderer",
                "title": "The renderer produced no usable artifact for an element and a "
                         "model wrote one instead",
                "text": "The renderer produced no usable artifact for element "
                        "'{element}', so one was written by a model. The reason recorded "
                        "at the time was: {detail}. Nothing in this migration has "
                        "compiled that artifact against the target, run it, or compared "
                        "it with the behaviour of the element it stands in for.",
                "impact": "output-unverified",
                "distinguisher": "a marker-carrying model is unusable and says so; this "
                                 "one is usable-looking and unverified, which is the "
                                 "harder review problem and a different action for a "
                                 "reviewer.",
            },
            element=m.stem, element_id=_rel(m, run.out_root), native_kind="",
            detail=reason or "(no reason recorded in the stamp)",
            evidence=f"{_rel(m, run.out_root)} carries the model-authored stamp",
            location=_rel(m, run.out_root),
            detector="filled_models"))
    return found


REPRESENTATION_DETECTORS = (
    detect_unrepresented_elements,
    detect_degraded_to_catch_all,
    detect_unmapped_role,
    detect_column_less_elements,
    detect_columns_without_a_recipe,
    detect_missing_predicate,
    detect_branch_collapse,
)

ARTIFACT_DETECTORS = (
    detect_unresolvable_references,
    detect_edges_absent_from_artifact,
    detect_renderer_failures,
    detect_filled_models,
)


def run_detectors(run: RunInputs) -> tuple[list[Finding], list[str]]:
    """Every detector that CAN run, with a line per detector saying whether it did.

    A detector that could not run is reported, never silently skipped: "no findings"
    and "never looked" are opposite claims and a count alone renders them identically.
    """
    findings, log = [], []
    have_ir = bool((run.ir or {}).get("nodes"))
    have_tree = run.out_root.is_dir()
    for det in REPRESENTATION_DETECTORS:
        if not have_ir:
            log.append(f"  {det.__name__:34} SKIPPED — no representation to read")
            continue
        got = det(run)
        findings.extend(got)
        log.append(f"  {det.__name__:34} {len(got)} finding(s)")
    for det in ARTIFACT_DETECTORS:
        if not have_tree:
            log.append(f"  {det.__name__:34} SKIPPED — no output tree to read")
            continue
        if det is detect_edges_absent_from_artifact and not have_ir:
            log.append(f"  {det.__name__:34} SKIPPED — needs the representation")
            continue
        got = det(run)
        findings.extend(got)
        log.append(f"  {det.__name__:34} {len(got)} finding(s)")
    return findings, log


def load_run(table_path: str, doc_path: str, ir_path: str,
             out_root: str) -> RunInputs:
    table = json.loads(Path(table_path).read_text(encoding="utf-8"))
    ir = None
    notes = []
    try:
        ir = json.loads(Path(ir_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        notes.append(f"representation unreadable at {ir_path} ({exc}); "
                     f"representation-side detectors will not run and their absence is "
                     f"NOT a claim that there was nothing to find")
    return RunInputs(platform=table.get("platform", "unknown"), table=table,
                     doc_path=doc_path, ir=ir, out_root=Path(out_root), notes=notes)
