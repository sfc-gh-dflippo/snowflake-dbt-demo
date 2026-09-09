"""THE TIER-2/TIER-3 SIDECAR PRODUCER — the model step, as a real model call.

WHY THIS MODULE EXISTS
----------------------
`findings/41` proved a MECHANISM: a `<document>.ai.json` sidecar carries model-authored
payload into the IR with `MODEL` provenance, the engine renders it, and stage 4 marks it
`SSC-AI-ASSISTED` / `SSC-AI-AUTHORED`. Every fidelity number in that finding is an UPPER
BOUND, because the model step was performed inline by an assistant reading the Java and
writing the SQL. `CONFIDENCE.yml` records exactly that under
`the-model-step-was-performed-inline-not-by-a-model-call`.

This module replaces the assistant with a process. Nothing about the schema changes: the
output is byte-compatible with the hand-authored file at
`poc/blind-run/inputs/pentaho/customer_summary_fullname_birthyear.ktr.ai.json`, which is both
the schema and the quality baseline.

WHY THE NAME. The artifact is called "the sidecar" in `emit.py:_load_sidecar`, in findings/41
and in the implementation plan; this is the thing that produces it. Same `<noun>_<noun>.py`
shape as `coverage_gate.py` and `gate_a.py`, and it deliberately does NOT start with `ai_`,
because `ai_fill.py` CONSUMES a sidecar and this PRODUCES one — two stages that must not be
confused in a log.

THE TWO-PASS DESIGN, AND WHY IT IS THE SAFETY PROPERTY
-----------------------------------------------------
A naive producer would ask a model about every element. This one runs identification and
emission FIRST, WITH THE SIDECAR SUPPRESSED, and asks the model only about the elements the
DETERMINISTIC PATH DECLINED. That is not an optimisation:

  * it makes "tier 1 still wins where tier 1 works" STRUCTURAL rather than a promise. An
    element the table maps and whose payload a rule reads is never put to a model, so a model
    cannot regress it;
  * it makes the CONFIDENCE item `tier-3-must-not-become-why-tier-1-never-improves`
    ANSWERABLE. The census prints the deterministic reason for every request, so a closeable
    producer gap ("our Pentaho port_policy does not read TableOutput's <fields>") reads
    differently from a genuine impossibility ("no engine translator lowers Janino Java"), in
    the request itself, before a model is invoked.

Suppression is done by replacing `Emitter._load_sidecar` for the census pass only. `emit.py`
is NOT edited: it is owned elsewhere, and a census that depended on an edit there would be
measuring a modified pipeline.

WHAT THE MODEL IS GIVEN, AND WHAT IT IS DELIBERATELY NOT GIVEN
--------------------------------------------------------------
Per element, one call, narrow on purpose:

  * the element's own SOURCE FRAGMENT (`Identification.source_text`, the same text the IR
    already carries as `_unsupported_body`);
  * its native kind, its role, and the platform name;
  * the target dialect (Snowflake) and the dbt reference idiom;
  * the platform's SEMANTICS SHEET — the table's `dialect` and `expression_syntax` blocks;
  * for a tier-3 request, the model names of its immediate neighbours in the IR, so a
    `ref()` resolves.

NOT the whole document, NOT the rest of the pipeline, NOT the platform table's rules, NOT any
finding, and NOT the hand-authored sidecar. Two reasons, and the second is the load-bearing
one: a narrow prompt is testable, and a model with filesystem access could READ the baseline
it is being measured against. The default command therefore runs with `--tools ""`, which is a
measurement-integrity requirement and not a cost saving — it is the same reasoning as Gate A's
blind bundle.

`--semantics rules` (the default) STRIPS every `_`-prefixed key from the semantics sheet before
it is shown, exactly as `gate_a.strip_commentary` does and for exactly the same reason: those
keys are the table author's prose ABOUT their own rules, which is a self-report rather than
evidence. It matters here more than in Gate A, because one of those comments quotes the blind
DataStage document's own derivations verbatim. `--semantics full` includes them and exists so
the sensitivity can be MEASURED rather than argued about; `--semantics none` withholds the
sheet entirely.

MALFORMED MEANS NO SIDECAR. NOT A PARTIAL ONE.
---------------------------------------------
A half-written entry is worse than no entry, and the reason is a measured safety rule rather
than tidiness: `emit.py` promotes a sidecar `$kind` WITHOUT re-checking that kind's required
payload, so a sidecar naming `FilterTransformation` with no `FilterConditions` reaches the
hydrator, and `AiFirstProducerIrHydrator.HydrateElement`'s `RequiredString` then throws and
LOSES THE WHOLE DOCUMENT. Upstream of that, `FilterTranslator`'s base substitutes `WHERE TRUE`
for an empty predicate and logs a warning — a filter that silently returns every row.

So validation happens HERE, before anything is written:

  1. the response must be a JSON object. One tolerance, recorded and counted, never silent:
     a ```json fence is stripped, because unfencing is lossless and throwing away a correct
     answer over formatting would make the measurement about the harness. Anything else fails.
  2. `$kind`, when present, must be one of the FIVE the hydrator's switch accepts. A sixth
     name is the failure this project keeps finding — a closed vocabulary meeting something
     outside it — and it fails loudly here instead of at hydration.
  3. the required payload for the resulting kind must be present and non-empty. `$kind` is the
     model's, the requirement is the hydrator's.
  4. every non-`_` key must be a field the hydrator or `emit.py` actually reads. An invented
     field name is a silent no-op otherwise.
  5. `OutputColumns[]` entries need a non-empty `Name`; `Expression`, when present, must be a
     non-empty string.
  6. an entry that supplies nothing usable is a failure, not an empty success.

A model may ABSTAIN with `{"_abstain": "<reason>"}`. That is a WELL-FORMED answer meaning
"leave this element to the deterministic path", it is counted and printed, and it is the one
thing that is not a hard failure — because refusing to write the other four entries over one
element the model cannot help would degrade elements tier 1 handled. A malformed response is
still a hard failure and writes nothing at all.

WHAT THIS DOES NOT DO
---------------------
It does not weaken any safety rule, it does not touch `emit.py`, `ai_fill.py`,
`coverage_gate.py`, `gate_a.py` or the driver, and it does not decide the degradation verdict.
It writes one input artifact. Whether the SQL it contains is right is measured by `diff`
against the baseline, by `variance`, and by the driver's own stage 4 — never asserted here.

Subcommands
-----------
  census    print the deterministic gap list for a document. NO model call.
  produce   census, then one model call per gap, then validate, then write the sidecar.
  diff      field-by-field agreement between a produced sidecar and a baseline.
  variance  N calls on ONE element; report whether the answer is stable.

Exit codes
  0  produced (or censused, or diffed)
  1  could not run, or a malformed response — NO sidecar written
  2  usage
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from datetime import datetime, timezone
from identify import CONTAINER_ROLES
from source_sql import modelsql_has_verb

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK = HERE  # remapped: identify modules live alongside gates in scripts/
for _p in (HERE, FRAMEWORK):
    if _p not in sys.path:
        sys.path.insert(0, _p)

W = 96

# ---------------------------------------------------------------------------------------------
# THE OUTPUT CONTRACT, READ OFF THE HYDRATOR RATHER THAN INVENTED HERE.
#
# Source: Producer/AiFirstProducerIrHydrator.cs, `HydrateElement`'s `kind switch` and
# `HydrateColumns`. Five arms, and `RequiredString` is what makes a payload REQUIRED -- it
# throws, and a throw at hydration costs the whole document rather than one element. Kept as
# data so the producer's refusal and the hydrator's throw cannot drift apart silently; if that
# switch gains an arm, this table is the one place to add it.
# ---------------------------------------------------------------------------------------------

KIND_CONTRACT = {
    "SourceQualifier": {
        "required": (),
        # TableName is optional on table-mapped sources (SqlCommand / generators may
        # honestly have none). A model-owned TIER2_KIND SourceQualifier must name it:
        # the hydrator copies it into sourceRelationsByNodeId, which fills FROM and
        # ObjectReferences SELECT - FROM.
        "optional": ("TableName", "SchemaName", "Database"),
        "means": "a read from a relation; TableName fills FROM and ObjectReferences SELECT - FROM",
        "renders": "`SELECT <columns> FROM <relation>`",
    },
    "ExpressionTransformation": {
        "required": (),
        "optional": (),
        "means": "a projection that computes columns; the work is in OutputColumns",
        "renders": "a FLAT `SELECT <expr> AS <name>, ...` over one upstream. No `GROUP BY`, no "
                   "`DISTINCT`, no `QUALIFY`, no join",
    },
    "FilterTransformation": {
        "required": ("FilterConditions",),
        "optional": (),
        "means": "a row filter; FilterConditions is a Snowflake boolean predicate",
        "renders": "`SELECT ... WHERE <FilterConditions>`. A `WHERE` cannot hold a window "
                   "function, so no `ROW_NUMBER`-style dedup",
    },
    "TargetTransformation": {
        "required": ("TableName",),
        "optional": ("SchemaName", "Database"),
        "means": "a write to a relation",
        "renders": "a write, with `TableName` interpolated into `config(alias=...)`",
    },
    "UnsupportedTransformation": {
        "required": (),
        "optional": (),
        "means": "an honest placeholder: projects NULLs and carries a blocking EWI",
        "renders": "`null AS <col>` per output column, plus a blocking EWI",
    },
}

# WHAT NO KIND ABOVE CAN RENDER, STATED BECAUSE OMITTING IT PRODUCED WRONG ANSWERS THREE TIMES.
# MEASURED on one blind Alteryx document and one blind Informatica mapping. Asked to lower an
# aggregate, a model answered `ExpressionTransformation` with `SUM(...)`/`AVG(...)`/`COUNT(...)` in
# OutputColumns -- a flat SELECT, so the GROUP BY simply vanished. Asked to lower a dedup, another
# answered `FilterTransformation` with `ROW_NUMBER() OVER (...) = 1` as the predicate, and said in
# its own reasoning that it expected a QUALIFY; a WHERE cannot hold a window function, so that model
# does not execute. Both answers reasoned correctly about the SQL and wrongly about what the
# RENDERER would do with the payload, which is not something the source fragment or the semantics
# sheet can tell them. The same model, given the translator source to read, chose a whole ModelSql
# body for the same element and explained exactly this. So it is a missing sentence in the question,
# not a limit of the answerer.
NO_KIND_RENDERS = (
    "aggregation (`GROUP BY`), de-duplication (`DISTINCT` or `QUALIFY ROW_NUMBER`), a join of two "
    "upstreams, a set operation (`UNION`), or a multi-output router"
)

# Keys legal at the top of a sidecar ENTRY regardless of kind. `ModelSql` and `OutputColumns`
# are read by ai_fill.py and emit.py respectively; `InputColumns` by the hydrator.
ENTRY_STRUCTURAL_KEYS = {"$kind", "ModelSql", "OutputColumns", "InputColumns"}
COLUMN_KEYS = {"Name", "Expression", "DataType", "Precision", "Scale", "$kind"}

# Every payload string KIND_CONTRACT lets a kind carry (FilterConditions, TableName,
# SchemaName, Database), READ OFF THE TABLE rather than listed by hand -- a kind gaining a new
# required or optional string field would otherwise reach the quoted-identifier check in
# `validate` only if someone remembered to add it there too. `FilterConditions` is interpolated
# straight into a `WHERE` clause exactly like `ModelSql` is into a `SELECT`, so a quoted
# mixed-case column name there is the identical Snowflake-folding hazard.
PAYLOAD_STRING_FIELDS = sorted({f for spec in KIND_CONTRACT.values()
                                for f in spec["required"] + spec["optional"]})

# Container roles. A container node carries `$kind: null` BY DESIGN -- it is the orchestration
# unit, not a model -- and asking a model to invent a data-flow class for a Kettle
# <transformation> or a DSJOB would fabricate a model the pipeline does not want. Shared with
# emit.py via identify.CONTAINER_ROLES so the two gates cannot drift apart again.


class ProducerError(Exception):
    """Every could-not-run and every malformed response. Always exit 1, never a partial file."""


class ProducerValidationError(ProducerError):
    """A parse or validation failure for ONE response -- retryable. Raised only by
    `parse_response`/`validate`, never by `invoke`. The distinction is what lets `_ask_one`
    spend up to `--attempts` model calls correcting a malformed ANSWER while still failing a
    request promptly on a could-not-run failure (auth, exec, timeout): retrying a system failure
    N times burns N times the cost for the same outcome, while retrying a bad answer with the
    validation error attached is the one case a second call can plausibly fix."""


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _wrap(s, n):
    """Local, on purpose. `coverage_gate._wrap` and `gate_a.strip_commentary` do the same job and
    were imported at first; both files are actively owned by another agent, and importing a
    PRIVATE helper across an ownership boundary means a rename over there silently breaks the
    producer here. `ai_fill.is_degraded` stays imported because sharing THAT definition is the
    point -- the fill stage and the producer must not disagree about which models are unusable --
    and it is a documented interface rather than a formatting helper."""
    import textwrap
    return textwrap.wrap(str(s), n) or [""]


def strip_commentary(obj, removed=None):
    """Remove every `_`-prefixed key. The rule, and the reasoning, are `gate_a.strip_commentary`'s:
    those keys are the table author's prose ABOUT their own rules -- a self-report, not evidence.
    Re-stated here rather than imported for the ownership reason above; if the two ever disagree
    the difference is visible in one diff instead of hidden behind an import."""
    if removed is None:
        removed = []
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


# ---------------------------------------------------------------------------------------------
# THE CENSUS — what the DETERMINISTIC path declined, and why, per element.
#
# Runs identification + emission with the sidecar SUPPRESSED, then reads the slot ledger. The
# ledger is the right source and the IR is not: the IR shows a degraded node, while the ledger
# states WHICH obligation was declined and by WHICH named rule -- the difference between "no
# engine translator lowers this dialect" and "our port_policy does not read that subtree".
# ---------------------------------------------------------------------------------------------

TIER2_KIND = "KIND_AND_PAYLOAD"     # the table maps this native kind to nothing
TIER2_PAYLOAD = "PAYLOAD_ONLY"      # the table maps the kind; a required field did not resolve
TIER3_BODY = "MODEL_BODY"           # the engine emitted a model and it is unusable


def _deterministic_pass(table_path, doc_path):
    """(identification, emitter, ir) with the sidecar suppressed. Stdout captured.

    `Emitter._load_sidecar` is replaced for this call only. emit.py is NOT edited -- a census
    that needed an edit in a file another agent owns would be measuring a modified pipeline,
    and the suppression has to be visible in THIS module for a reader to trust the numbers.
    """
    from identify import Identification, load_table
    import emit as emitmod

    original = emitmod.Emitter._load_sidecar
    emitmod.Emitter._load_sidecar = lambda self: {}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            table = load_table(table_path)
            idn = Identification(table, doc_path)
            em = emitmod.Emitter(idn)
            ir = em.emit()
    except Exception as ex:
        raise ProducerError("the deterministic pass failed on this document, so there is no gap "
                            "list to ask about: %s: %s" % (type(ex).__name__, ex))
    finally:
        emitmod.Emitter._load_sidecar = original
    return table, idn, em, ir


def _model_files(tree):
    """modelName -> the dbt model name a `ref()` must actually use, read off the TREE.

    A MEASURED DEFECT IN THIS PRODUCER, caught on its first live run and fixed before any
    measurement was recorded from it. The IR's `modelName` is `read_customer`; the file the
    emitter writes is `models/staging/stg_raw__read_customer.sql`, and dbt resolves `ref()` on
    the FILE STEM. So the prompt told the model to write `{{ ref('read_customer') }}`, the model
    did exactly as instructed, and the result was `dbt1005: Ref not found` -- a dangling
    reference manufactured by the harness and then blamed on the model. The hand-authored
    baseline uses `{{ ref('int_derive_fullname_and_birthyear') }}`, with the prefix, which is
    what a correct instruction looks like.

    The prefixes are `ai_fill.py`'s own match list (`int_`, `stg_raw__`, `*__<name>`), so the
    resolution here and the fill's cannot disagree. Read from the artifact rather than
    reconstructed from a naming rule, for the reason this project keeps rediscovering: the
    artifact is the fact and the rule is a claim about it.
    """
    from pathlib import Path
    PRUNED = ("target", "dbt_internal_packages")
    if not tree or not os.path.isdir(tree):
        return {}
    stems = sorted({p.stem for p in Path(tree).rglob("*.sql")
                    if not any(part in PRUNED for part in p.parts)})
    return stems


def _degraded_excerpt(paths, cap=1400):
    """WHAT THE ENGINE ACTUALLY PRODUCED for this element, verbatim.

    MEASURED, and it is the sharpest single result of this whole exercise. Round 1 told the model
    only that the model was "degraded" and offered an optional `ModelSql`; on Pentaho's
    `Filter BirthYear` the model DECLINED it, twice, on a byte-identical prompt -- entirely
    reasonably, because from inside the source document its payload IS enough. What it could not
    know is that `FilterTranslator` throws ENG-020 on the SPACE in the upstream step's name, which
    is a fact about the ENGINE and appears nowhere in the .ktr. The hand-authored baseline knew it
    and supplied a tier-3 body; the model had no way to.

    The engine's own EWI in its own output is that missing evidence, and it is evidence rather
    than a hint: it is a diagnostic about THIS element, produced by the thing that failed. Same
    move gate_a.py makes when it embeds coverage_gate's report verbatim instead of describing it.
    """
    out = []
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        body = "\n".join(ln for ln in t.splitlines() if not ln.strip().startswith("--"))
        out.append("/* %s */\n%s" % (p.name, body.strip()[:cap]))
    return "\n\n".join(out)


def _resolve_dbt_name(model_name, stems):
    """The stem `ref()` takes, or None when the tree holds no model for this element.

    THE FALLBACK USED TO BE `return model_name`, AND IT REINTRODUCED THE EXACT DEFECT THE
    DOCSTRING ABOVE DESCRIBES. An element the emitter declined writes no file, so no stem
    matches, so the prompt instructed the model to reference the bare `modelName` -- and the
    dangling-ref check could not fire, because the fabricated name was in the `known` set it
    checks against. Measured on Alteryx pass 7: element 4 had no model when the producer ran,
    the authored join was told to write `{{ ref('m_4') }}`, the next emit named that same model
    `stg_raw__m_4` once tier 2 supplied its TableName, and dbt stopped at
    `dbt1005: Ref 'm_4' not found`. A harness that guesses a name it could have declined to
    supply turns its own gap into the model's error.
    """
    if not model_name:
        return None
    for s in stems:
        if s in (model_name, f"int_{model_name}", f"stg_raw__{model_name}") \
                or s.endswith(f"__{model_name}"):
            return s
    return None


def _neighbours(ir, node_id, stems=()):
    """({upstream}, {downstream}) — for a tier-3 ref(). `dbt_model` is the name ref() takes."""
    by_id = {n["id"]: n for n in ir["nodes"]}
    up, down = [], []
    for e in ir.get("edges") or []:
        if e.get("to") == node_id and e.get("from") in by_id:
            up.append(by_id[e["from"]])
        if e.get("from") == node_id and e.get("to") in by_id:
            down.append(by_id[e["to"]])

    def names(ns):
        out = []
        for n in ns:
            mn = n.get("modelName")
            el = n.get("element") or {}
            # EACH UPSTREAM'S OUTPUT COLUMNS TRAVEL WITH IT, AND OMITTING THEM PRODUCED SQL THAT
            # SNOWFLAKE REJECTED. A tier-3 body is often a merge of several upstreams, and a model
            # told only the upstreams' NAMES has no way to know their SHAPES. MEASURED on the Order
            # Enrichment union: the two branches are the online and retail order feeds, 8 columns
            # each, differing in exactly one -- online has `ShipDate` and no `StoreNumber`, retail
            # the reverse. The model authored the same 9 columns from BOTH branches, which is the
            # only thing it could have done, and Snowflake answered
            # `dbt0227: No column STORENUMBER found`.
            out.append({"modelName": mn,
                        "dbt_model": _resolve_dbt_name(mn, stems),
                        "element": el.get("Name"),
                        "$kind": el.get("$kind"),
                        "columns": [c.get("Name") for c in (el.get("OutputColumns") or [])
                                    if isinstance(c, dict) and c.get("Name")]})
        return out
    return names(up), names(down)


def _resolve_element(idn, em, el_by_name, node):
    """(el, name) for the IR node's identification element, or (None, None).

    STABLE IDENTITY. `node["id"]` is the exact key `emit_node` iterated off
    `idn.elements.items()` under (see `emit()`'s `[self.emit_node(n, el) for n, el in
    self.idn.elements.items()]`), so it is ALWAYS a hit in `idn.elements` for a genuine
    node -- unlike `element.Name`/`modelName`, which are `ir_element_name(el)`/
    `model_name(el)` and diverge from `em.element_name(el)` the moment a platform's
    naming_policy sanitizes them. MEASURED on Alteryx: `element_name()` for a ToolID-`1`
    tool is the bare id `"1"`, but `sanitize_element_name` (needed because `"1"` is not a
    legal SQL correlation name) turns `element.Name`/`modelName` into `"m_1"` -- so the
    old Name-keyed lookup missed every one of 113 nodes and called the whole document
    orphaned. Resolve off the id first; the Name/modelName aliases -- the pre-fix lookup
    -- are a fallback only, for a platform where the id might legitimately not be a
    census-time `idn.elements` key, so a genuine orphan still surfaces instead of being
    hidden by a partial alias match.
    """
    el = idn.elements.get(node.get("id"))
    if el is not None:
        return el, em.element_name(el)
    el_json = node.get("element") or {}
    for key in (el_json.get("Name"), node.get("modelName")):
        el = el_by_name.get(key)
        if el is not None:
            return el, key
    return None, None


def census(table_path, doc_path, tree=None):
    """The gap list. One request per element the deterministic path could not represent."""
    table, idn, em, ir = _deterministic_pass(table_path, doc_path)

    # element display name -> the ledger's reasons for declining it
    stems = _model_files(tree)
    declined = {}
    for s in em.slots:
        if s.provenance != "MISSING":
            continue
        declined.setdefault(s.element, []).append((s.path, s.detail or s.where or ""))

    el_by_name = {}
    for el in idn.elements.values():
        el_by_name[em.element_name(el)] = el

    requests = []
    # SCD73: IR nodes with no identification element must not vanish from the census.
    # Containers are listed under containers_excluded; orphans get their own audible list.
    orphans = []
    # Elements the emitter named a model for and never wrote a file for. Collected in the tier-3
    # sweep below, printed beside the orphans, and outside this stage's reach either way.
    modelless = []
    elements_total = 0
    containers_excluded = []
    for node in ir["nodes"]:
        el_json = node.get("element") or {}
        el, name = _resolve_element(idn, em, el_by_name, node)
        if el is None:
            label = el_json.get("Name") or node.get("id") or "<unnamed>"
            orphans.append(str(label))
            continue
        role = getattr(el, "role", None)
        if role in CONTAINER_ROLES:
            # BY DESIGN, not a gap. The container is the orchestration unit; a data-flow class
            # for it would fabricate a model. Recorded in the printed census so the exclusion
            # is auditable rather than invisible.
            containers_excluded.append(name)
            continue
        elements_total += 1

        dispatch = idn.dispatch_for(el)
        table_kind = dispatch.get("ir_kind")
        reasons = declined.get(name, [])
        kind_declined = [d for p, d in reasons if p == "element.$kind"]

        need_kind = el_json.get("$kind") in (None, "UnsupportedTransformation")
        missing_fields = []
        for r in kind_declined:
            m = re.search(r"required payload did not resolve[^:]*:\s*(.+?)\.\s", r + " ")
            if m:
                for part in m.group(1).split(","):
                    fld = part.strip().split(" ")[0]
                    if fld:
                        missing_fields.append(fld)

        want = None
        if need_kind and missing_fields:
            # The table HAS a kind for this element and refused it for want of a payload. The
            # narrow request -- supply the field -- is strictly better than asking for a kind,
            # because the table's mapping is a stated platform fact and the model's would be an
            # assertion.
            want = {"shape": TIER2_PAYLOAD, "kind": table_kind, "fields": sorted(set(missing_fields))}
        elif need_kind:
            # A kind absent from kind_dispatch is the same refusal as supported=false:
            # no translator, no hydrator door. Only explicit supported=true may ask for
            # $kind. Otherwise the C# census scores a hydrator class with no EWI as Success.
            table_supported = dispatch.get("supported") is True
            fields = [] if table_supported else ["ModelSql"]
            want = {"shape": TIER2_KIND, "kind": None, "fields": fields}

        if want is not None:
            up, down = _neighbours(ir, node["id"], stems)
            table_supported = dispatch.get("supported") is True
            requests.append({
                "element": name,
                "node_id": node["id"],
                "model_name": node.get("modelName"),
                "native_kind": getattr(el, "kind_raw", None),
                "role": role,
                "shape": want["shape"],
                "expected_kind": want["kind"],
                "needed_fields": want["fields"],
                "table_supported": table_supported,
                "deterministic_reasons": kind_declined,
                "source_text": idn.source_text(el) or el_json.get("_unsupported_body") or "",
                "upstream": up,
                "downstream": down,
                "emitted_columns": [c.get("Name") for c in (el_json.get("OutputColumns") or [])],
            })

    # ---- tier 3: models the ENGINE emitted and could not make usable ---------------------------
    # `ai_fill.is_degraded` is IMPORTED, never reimplemented. Same discipline gate_a.py applies
    # to coverage_gate's counters: if the definition of "degraded" changes there it changes here,
    # and the fill stage and the producer cannot disagree about which models need a body.
    if tree:
        import ai_fill
        by_model = {}
        for node in ir["nodes"]:
            mn = node.get("modelName")
            if mn:
                by_model.setdefault(mn, node)
        already = {r["element"] for r in requests}
        from pathlib import Path
        # THE SAME PRUNE THE DRIVER APPLIES, AND FOR THE SAME MEASURED REASON. `dbt compile`
        # writes its own copy of every model under `target/compiled/models` and vendors two dbt
        # packages under `dbt_internal_packages/`, each with its own models. Without the prune the
        # census reported `stg_raw__read_customer.sql` TWICE -- the model and dbt's copy of it --
        # so the request said "2 degraded models" for one, and on a re-inspected tree the count
        # would have kept growing. aifirst-migrate.sh carries the identical prune with the
        # identical note; ai_fill.py does not, and gets away with it only because it runs before
        # dbt ever has.
        PRUNED = ("target", "dbt_internal_packages")
        sqls = [p for p in Path(tree).rglob("*.sql")
                if not any(part in PRUNED for part in p.parts)]
        for mn, node in sorted(by_model.items()):
            el_json = node.get("element") or {}
            # Same stable-identity resolution as the tier-2 sweep above -- so a degraded
            # Alteryx model is not silently dropped from the tier-3 sweep the way it was
            # dropped from tier-2, for the same sanitized element.Name reason.
            el, name = _resolve_element(idn, em, el_by_name, node)
            if el is None or getattr(el, "role", None) in CONTAINER_ROLES:
                continue
            # DEDUPED, and the duplicate was real: `stg_raw__read_customer` satisfies BOTH
            # `stem in (..., f"stg_raw__{mn}")` and `stem.endswith(f"__{mn}")`, so the first
            # version reported the same file twice and would have printed "2 degraded models"
            # for one. Small, and exactly the shape of a count nobody checks.
            hits = sorted({p for p in sqls
                           if p.stem in (mn, f"int_{mn}", f"stg_raw__{mn}")
                           or p.stem.endswith(f"__{mn}")})
            if not hits:
                # SAME TREATMENT AS AN ORPHAN NODE, AND FOR THE SAME REASON: not a gap this stage
                # can close, and not one it may hide either.
                #
                # MEASURED on the blind Alteryx pass. Two `DbFileOutput` targets produced NO model
                # file, deterministic Gate A returned 11/13 with exit 3, and the census said
                # nothing about either of them -- because `bad` is empty both when the model is
                # FINE and when there is no model AT ALL, and those are opposite facts. So the two
                # worst elements in the document were the two the fill ladder never asked about.
                #
                # NOT raised as a request, deliberately: `ai_fill` writes into an EXISTING file and
                # reports a missing one as `no_target`. Asking a model for a body nothing can apply
                # would spend a call to produce an entry that silently goes nowhere, which is worse
                # than the silence it replaces. Closing it properly means teaching the fill stage
                # where a model file belongs -- the layer directory the emitter would have chosen
                # from the element's role -- and that is emitter naming logic, not a fill concern.
                modelless.append("%s (model %r was never written)" % (name, mn))
                continue
            bad = [p for p in hits
                   if "SSC-AI-AUTHORED" not in p.read_text(encoding="utf-8", errors="replace")
                   and ai_fill.is_degraded(p.read_text(encoding="utf-8", errors="replace"))]
            if not bad:
                continue
            up, down = _neighbours(ir, node["id"], stems)
            existing = next((r for r in requests if r["element"] == name), None)
            if existing is not None:
                existing["also_needs_model_body"] = True
                existing["degraded_files"] = [p.name for p in bad]
                existing["degraded_text"] = _degraded_excerpt(bad)
                continue
            requests.append({
                "element": name,
                "node_id": node["id"],
                "model_name": mn,
                "native_kind": getattr(el, "kind_raw", None),
                "role": getattr(el, "role", None),
                "shape": TIER3_BODY,
                "expected_kind": el_json.get("$kind"),
                "needed_fields": ["ModelSql"],
                "table_supported": idn.dispatch_for(el).get("supported") is True,
                "deterministic_reasons": [
                    "the engine emitted %s and ai_fill.is_degraded reports it unusable "
                    "(a blocking EWI, or a SELECT that projects nothing)"
                    % ", ".join(p.name for p in bad)],
                "source_text": idn.source_text(el) or el_json.get("_unsupported_body") or "",
                "upstream": up,
                "downstream": down,
                "emitted_columns": [c.get("Name") for c in (el_json.get("OutputColumns") or [])],
                "degraded_files": [p.name for p in bad],
                "degraded_text": _degraded_excerpt(bad),
            })
            already.add(name)

    return {
        "platform": table.get("platform"),
        "document": os.path.abspath(doc_path),
        "document_sha256": _sha(doc_path),
        "table": os.path.abspath(table_path),
        "elements_total": elements_total,
        "containers_excluded": containers_excluded,
        "orphans_unidentified": orphans,
        "modelless_elements": modelless,
        "tree": os.path.abspath(tree) if tree else None,
        "requests": requests,
        "ir": ir,
    }


# ---------------------------------------------------------------------------------------------
# THE PROMPT. One element, one call.
#
# Every clause here is either the OUTPUT CONTRACT or a fact about the element. There is
# deliberately NO warning about any specific construct: the two known traps in the blind
# Pentaho document -- `BirthDate.getYear() + 1900` (Java's getYear() returns year MINUS 1900,
# so the lowering is YEAR(BirthDate), NOT YEAR(BirthDate) + 1900) and Java `+` rendering a null
# operand as the text "null" -- are MEASUREMENTS, and a prompt that names them measures the
# prompt instead of the model. If a warning is ever added, it must be added here, in the
# committed text, so a reader can see it and discount the number.
#
# `_semantic_divergence` IS in the contract, because the baseline sidecar uses it and the
# question "does the model record the divergence" is unanswerable if the field does not exist.
# That is a schema fact, not a hint about which divergence to look for -- and it is a genuine
# sensitivity, recorded in the report rather than assumed away.
# ---------------------------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a migration engineer lowering ONE element of an ETL document to Snowflake SQL. "
    "You reply with a single JSON object and nothing else: no prose before or after it, no "
    "markdown code fence, no explanation outside the JSON."
)

DOC_FIELDS = """\
Documentation fields. These are for a human reviewer and are NOT read as IR fields. Every one
is optional, and each must be a string:

| field | what goes in it |
|---|---|
| `_source_expression` | the source expression you lowered, verbatim |
| `_source_dialect` | the language the source expression is written in |
| `_source_form` | the source construct you read, verbatim, when it is not an expression |
| `_reasoning` | why this lowering is equivalent to the source, when that is not obvious |
| `_semantic_divergence` | REQUIRED WHENEVER the Snowflake form you wrote does not behave identically to the source form on some input. State the divergence, which behaviour you chose, and what the alternative would have been. Do not silently pick one. |
| `_tier` | `2` if you supplied a payload the engine will render, `3` if you wrote a whole model body |
| `_why_tier_3` | only for `ModelSql`: why the engine could not render this element |
"""


def semantics_sheet(table, mode):
    """The platform's semantics sheet: the table's own `dialect` + `expression_syntax` blocks.

    `rules` strips `_`-prefixed keys. Not hygiene: `platform_datastage.json`'s
    `dialect._comment` quotes the blind document's two derivations verbatim, and
    `platform_pentaho.json`'s says which of Kettle's four expression languages diverges. Those
    are the table author's prose about their own rules -- the self-report class of evidence Gate
    B withheld and `gate_a.strip_commentary` removes -- and showing them would put part of the
    answer in the question.
    """
    if mode == "none":
        return None
    sheet = {k: table.get(k) for k in ("dialect", "expression_syntax") if table.get(k)}
    if mode == "full":
        return sheet
    return strip_commentary(sheet)


def build_prompt(req, platform, sheet):
    kinds = []
    for k, spec in KIND_CONTRACT.items():
        rq = ", ".join(spec["required"]) or "—"
        kinds.append("| `%s` | %s | %s | %s |"
                     % (k, rq, spec["means"], spec["renders"]))

    parts = [
        "# Lower one ETL element to Snowflake",
        "",
        "## The element",
        "",
        "| | |",
        "|---|---|",
        "| source platform | `%s` |" % platform,
        "| element name | `%s` |" % req["element"],
        "| native kind | `%s` |" % req["native_kind"],
        "| role | `%s` |" % (req["role"] or "(unstated)"),
        "| target | Snowflake, emitted as a dbt model |",
        "",
        "## Its source fragment, verbatim",
        "",
        "```",
        req["source_text"].rstrip() or "(the front end supplied no fragment for this element)",
        "```",
        "",
    ]

    if sheet:
        parts += [
            "## What the platform table declares about this platform's expression semantics",
            "",
            "```json",
            json.dumps(sheet, indent=1),
            "```",
            "",
            "`syntactically_identical_semantically_divergent` lists operators that LOOK the same in "
            "both languages and do not behave the same. An empty or absent entry is not a promise "
            "that there is no divergence — it means the table records none.",
            "",
        ]

    parts += ["## What to produce", ""]

    if req["shape"] == TIER2_PAYLOAD:
        parts += [
            "The platform table already maps this native kind to the IR element kind "
            "**`%s`**. The engine's translators will render it. What no deterministic rule "
            "could read is the payload:" % req["expected_kind"],
            "",
        ] + ["- **`%s`** — required. %s" % (f, KIND_CONTRACT.get(req["expected_kind"], {}).get("means", ""))
             for f in req["needed_fields"]] + [
            "",
            "Do NOT restate `$kind`: the table's mapping is a stated platform fact and yours would "
            "be an assertion. Supply the payload field(s) and nothing structural.",
            "",
        ]
    elif req["shape"] == TIER2_KIND and req.get("table_supported") is not True:
        parts += [
            "This native kind is **not table-supported** (explicit `supported=false`, or "
            "absent from `kind_dispatch`). It has no Snowflake translator and `ir_kind` is "
            "null. Do NOT name a `$kind`. A hydrator class would report the element as converted "
            "and hide that refusal. If you can lower it, write the whole model body as `ModelSql` "
            "— Snowflake SQL in dbt syntax, and it must contain a `SELECT` or `WITH`: dbt "
            "compiles a model from a query, it cannot compile a procedure call or a bare "
            "mutation. **When the source statement is a procedure invocation (`EXEC` / "
            "`EXECUTE` / `CALL`), that is NOT a `ModelSql` candidate — abstain** with "
            "`{\"_abstain\": \"<reason>\"}` rather than writing a `CALL`/`EXECUTE` body; the "
            "element keeps its honest placeholder instead of a `.sql` file dbt cannot run.",
            "",
        ]
    elif req["shape"] == TIER2_KIND:
        parts += [
            "The platform table maps this native kind to NO IR element kind, so the element is "
            "currently an honest placeholder that projects NULLs. If you can lower it, name the IR "
            "element kind it really is and supply that kind's payload.",
            "",
            "| `$kind` | required payload | what it means | what its translator RENDERS |",
            "|---|---|---|---|",
        ] + kinds + [
            "",
            "**Read the RENDERS column before choosing.** Your payload is rendered by the "
            "translator named in that column and by nothing else: an expression you supply is "
            "placed where that translator places expressions, not where the SQL you have in mind "
            "would need it. No kind above renders %s. If this element needs any of those, none of "
            "these kinds can express it — supply a whole model body in the `ModelSql` FIELD and "
            "say why in `_why_tier_3`." % NO_KIND_RENDERS,
            "",
            # MEASURED, 2026-08-28 Alteryx: the previous wording ended "answer with `ModelSql`",
            # and all four elements that needed one -- a Join, a Union, a Unique and a Summarize --
            # read that literally and answered `"$kind": "ModelSql"` WITH a correct body beside it.
            # `validate` rejected the whole answer because ModelSql is not in the closed kind
            # vocabulary, and the rejection text listed the legal kinds without saying where the
            # body belonged. On retry all four ABSTAINED, three of them stating that "ModelSql is
            # not in the accepted vocabulary" -- the error message had taught them the body was
            # unavailable. Four correct SQL bodies were discarded over one field's value.
            "**`ModelSql` is a FIELD, never a `$kind`.** `$kind` must be one of the kinds in the "
            "table above and nothing else. When no kind fits, leave `$kind` as the kind this "
            "element already has (or `UnsupportedTransformation`) and put the whole body in the "
            "separate `ModelSql` field. Answering `\"$kind\": \"ModelSql\"` is rejected, and it "
            "throws away the body you wrote with it.",
            "",
            "**If you cannot supply a kind's required payload, do not name that kind.** A "
            "`FilterTransformation` with no `FilterConditions` becomes `WHERE TRUE` downstream, "
            "which silently returns every row and looks like a clean migration.",
            "",
            "For a projection, the work is `OutputColumns`: one entry per output column, each "
            "`{\"Name\": ..., \"Expression\": \"<Snowflake SQL>\"}`. Omit `Expression` for a column "
            "that passes through unchanged. Expressions are used VERBATIM — nothing downstream "
            "translates them, so they must already be valid Snowflake.",
            "",
        ]
    else:
        parts += [
            "The engine emitted a model for this element and the model is unusable: %s"
            % "; ".join(req["deterministic_reasons"]),
            "",
            "Write the whole model body as `ModelSql` — Snowflake SQL in dbt syntax, and it "
            "must contain a `SELECT` or `WITH`. If the source statement is a procedure "
            "invocation (`EXEC`/`EXECUTE`/`CALL`), that is NOT a `ModelSql` candidate — "
            "abstain instead of writing a `CALL`/`EXECUTE` body dbt cannot compile.",
            "",
        ]

    if req.get("degraded_text"):
        parts += [
            "### What the engine produced for this element, verbatim",
            "",
            "This is the output the migration ships if you supply nothing better. Its diagnostic "
            "is the engine's own account of what went wrong, and the failure may be an ENGINE "
            "limitation that a correct payload does NOT fix — in which case a whole `ModelSql` "
            "body is the only thing that helps.",
            "",
            "```sql",
            req["degraded_text"],
            "```",
            "",
        ]

    up = [u for u in req["upstream"] if u.get("dbt_model")]
    # An upstream the representation carries but the emitter wrote no model for. Silently
    # dropping it would leave the "reads from outside the pipeline" line below claiming
    # something false about a node that has a real predecessor.
    unresolved = [u for u in req["upstream"] if not u.get("dbt_model")]
    down = [d for d in req["downstream"] if d.get("dbt_model")]
    if req["shape"] == TIER3_BODY or up or unresolved:
        parts += ["### The models around this one, so a reference resolves", ""]
        for u in up:
            line = ("- upstream: element `%s` is the dbt model `%s` — reference it as "
                    "`{{ ref('%s') }}`" % (u["element"], u["dbt_model"], u["dbt_model"]))
            # The upstream's COLUMNS, stated with it. Without this a merge of several upstreams
            # can only be guessed at, and the guess Snowflake rejects is the plausible one: the
            # same column list selected from every branch.
            if u.get("columns"):
                line += "\n  and it projects exactly these %d column(s): %s" % (
                    len(u["columns"]), ", ".join("`%s`" % c for c in u["columns"]))
            parts.append(line)
        for u in unresolved:
            parts.append("- upstream WITH NO MODEL: element `%s` feeds this one, but the "
                         "emitter wrote no model file for it, so there is NO name a `ref()` "
                         "can take. Do not invent one. If this element cannot be written "
                         "without reading that upstream, abstain and say so."
                         % (u.get("element") or u.get("modelName") or "?"))
        if not up and not unresolved:
            parts.append("- no upstream model: this element reads from outside the pipeline. "
                         "Reference the external relation as `{{ source('raw', '<TABLE>') }}` "
                         "and the declaration will be generated from your SQL.")
        for d in down:
            parts.append("- downstream: element `%s` is the dbt model `%s` and will select from "
                         "this one" % (d["element"], d["dbt_model"]))
        parts += [
            "",
            "**The `ref()` names above are exact and already carry whatever layer prefix the "
            "emitter used.** A name not in that list resolves to nothing and the project does "
            "not compile. Copy them character for character; do not add or strip a prefix.",
            "",
        ]
        # THE HETEROGENEOUS-MERGE RULE, RAISED ONLY WHEN THE UPSTREAMS ACTUALLY DISAGREE. Stating it
        # unconditionally would spend prompt on every single-input element; stating it never produced
        # SQL Snowflake rejected. The condition is the finding: two or more upstreams whose column
        # sets are not identical.
        col_sets = [frozenset(u["columns"]) for u in up if u.get("columns")]
        if len(col_sets) > 1 and len(set(col_sets)) > 1:
            union_all = sorted(set().union(*col_sets))
            missing = {}
            for u in up:
                if not u.get("columns"):
                    continue
                absent = [c for c in union_all if c not in set(u["columns"])]
                if absent:
                    missing[u["dbt_model"]] = absent
            parts += [
                "### These upstreams DO NOT have the same columns — read this before writing a merge",
                "",
                "Selecting a column from an upstream that does not have it does not merely produce "
                "the wrong rows: the project FAILS TO RUN. Snowflake answers "
                "`No column <NAME> found`, the model errors, and every model downstream of it is "
                "skipped.",
                "",
            ]
            for model, absent in sorted(missing.items()):
                parts.append("- `%s` DOES NOT HAVE: %s"
                             % (model, ", ".join("`%s`" % c for c in absent)))
            parts += [
                "",
                "Where a branch lacks a column the merged output must carry, project an explicitly "
                "typed NULL for it (`CAST(NULL AS <type>) AS <name>`) so every branch of the set "
                "operation has the same shape in the same order. That is what the source tool does "
                "when it aligns fields by name across inputs with different schemas — the column "
                "survives with no value, rather than the branch losing it or the SQL failing.",
                "",
            ]
        if req["shape"] == TIER3_BODY and req.get("emitted_columns"):
            parts.append("The engine resolved these output columns for this element: %s"
                         % ", ".join("`%s`" % c for c in req["emitted_columns"] if c))
            parts.append("")

    # THE FOLDING RULE BELONGS TO BOTH SHAPES: whatever writes SQL needs it, so it sits in the
    # shared tail rather than a tier-specific section.
    parts += [
        "**Write column identifiers UNQUOTED.** Snowflake folds unquoted identifiers to UPPERCASE "
        "and matches double-quoted ones EXACTLY, and every upstream model emits its projections "
        "unquoted — so the relations you read from carry `ORDERSTATUS`, not `OrderStatus`. Writing "
        "`\"OrderStatus\"` asks for a column that does not exist, and the error names the two "
        "spellings one line apart: `No column OrderStatus found. Available are ...ORDERSTATUS`.",
        "",
        "## The answer",
        "",
        "One JSON object. Its keys, and no others:",
        "",
        "```json",
        json.dumps(_schema_example(req), indent=2),
        "```",
        "",
        DOC_FIELDS,
        "",
        "If you cannot lower this element at all, answer exactly "
        "`{\"_abstain\": \"<one sentence saying what stopped you>\"}`. That leaves the element to "
        "the deterministic path, which is a correct outcome. Do not guess a payload to avoid "
        "abstaining — a wrong predicate is worse than an honest placeholder.",
        "",
        "Reply with the JSON object only.",
    ]
    return "\n".join(parts)


def _schema_example(req):
    ex = {}
    if req["shape"] == TIER2_PAYLOAD:
        for f in req["needed_fields"]:
            ex[f] = "<Snowflake %s>" % f
    elif req["shape"] == TIER2_KIND:
        if req.get("table_supported") is not True:
            ex["ModelSql"] = "<a single Snowflake SELECT in dbt syntax>"
        else:
            ex["$kind"] = "<one of the kinds in the table above>"
            ex["OutputColumns"] = [{"Name": "<column>", "Expression": "<Snowflake SQL>"}]
            ex["TableName"] = "<unqualified relation; required when $kind is SourceQualifier>"
            ex["ModelSql"] = ("<OPTIONAL escape hatch. A whole Snowflake SELECT when no kind "
                              "above can render this element. Omit $kind if you use this.>")
    else:
        ex["ModelSql"] = "<a single Snowflake SELECT in dbt syntax>"
    if req.get("also_needs_model_body") and "ModelSql" not in ex:
        ex["ModelSql"] = ("<OPTIONAL. Only if the payload above will not be enough — the engine "
                          "already failed to render this element once. A whole model body.>")
    ex["_tier"] = "2"
    ex["_source_expression"] = "<the source you read, verbatim>"
    return ex


# ---------------------------------------------------------------------------------------------
# THE MODEL CALL. Swappable, following gate_a.py's `--verifier-cmd` precedent exactly.
#
# The prompt goes on STDIN and the answer comes back on STDOUT. Not argv: a source fragment is
# 2.5 kB of XML on the DataStage element and argv quoting is the wrong place to discover a
# limit. Any command with that contract works, which is what makes the default swappable rather
# than merely configurable -- `--model-cmd "cat /tmp/canned.json"` is a valid stub and the
# negative tests use exactly that.
#
# The default is the Claude CLI in headless print mode, so no API key handling lives here.
# `--tools ""` is NOT a cost measure: a model that can read files can read the hand-authored
# baseline it is being measured against, and the whole point of a narrow per-element prompt is
# that its inputs are known. `--system-prompt` replaces the CLI's own preamble for the same
# reason -- a 60 kB agent system prompt is 60 kB of instructions nobody writing this measurement
# chose.
# ---------------------------------------------------------------------------------------------

DEFAULT_MODEL_CMD = (
    'claude -p --output-format json --tools "" --strict-mcp-config --disable-slash-commands '
    '--no-session-persistence --system-prompt {system}'
)


def invoke(cmd, prompt, timeout=300):
    """(text, meta). Raises ProducerError for every failure to obtain a response.

    `{system}` in the command is replaced by the shell-quoted system prompt, so the caller
    controls it in one place. A command that does not use it simply does not get one.
    """
    import shlex
    real = cmd.replace("{system}", shlex.quote(SYSTEM_PROMPT))
    try:
        proc = subprocess.run(real, shell=True, input=prompt, capture_output=True,
                              text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ProducerError("the model command did not answer within %ds. NOTHING is written: an "
                            "unavailable model leaves the deterministic path exactly as it was."
                            % timeout)
    except Exception as ex:
        raise ProducerError("the model command could not be run (%s: %s). NOTHING is written."
                            % (type(ex).__name__, ex))
    if proc.returncode != 0:
        raise ProducerError("the model command exited %d. NOTHING is written. stderr: %s"
                            % (proc.returncode, (proc.stderr or "").strip()[:400]))
    out = proc.stdout or ""
    if not out.strip():
        raise ProducerError("the model command exited 0 and wrote nothing. Exit 0 with no output "
                            "is the silent-success shape this project keeps finding, so it is a "
                            "hard failure here.")
    meta = {}
    # The CLI's --output-format json envelope, when that is the command. Unwrapped rather than
    # assumed: a stub command returns the bare answer and must keep working.
    try:
        env = json.loads(out)
    except Exception:
        env = None
    if isinstance(env, dict) and "result" in env and "type" in env:
        if env.get("is_error"):
            raise ProducerError("the model reported an error: %s"
                               % str(env.get("result"))[:400])
        meta = {
            "models": sorted((env.get("modelUsage") or {}).keys()),
            "cost_usd": env.get("total_cost_usd"),
            "num_turns": env.get("num_turns"),
            "stop_reason": env.get("stop_reason"),
            "session_id": env.get("session_id"),
        }
        out = env.get("result") or ""
        if not out.strip():
            raise ProducerError("the model returned an empty result inside a success envelope.")
    return out, meta


FENCE_OPEN = re.compile(r"```(?:json)?\s*", re.S)


def parse_response(text):
    """(object, tolerances). Raises ProducerError on anything that is not a JSON object.

    ONE tolerance, counted and printed: a ```json fence is stripped. Unfencing is lossless, and
    a harness that discards a correct answer over formatting is measuring itself. Everything
    else -- prose, a JSON array, a truncated object, two objects -- is a hard failure, because
    each of those means the answer's SHAPE is not the contract and guessing at intent is how a
    half-written sidecar gets written.

    The fenced body is located by BALANCED-BRACE decoding (`json.JSONDecoder.raw_decode`
    starting at the fence's first `{`), not by a `{.*?}` regex: `ModelSql`/`FilterConditions`
    routinely carry `{{ ref('x') }}` Jinja, and a non-greedy regex stops at the FIRST `}` it
    meets -- inside the Jinja -- truncating the object before the real close.
    """
    tolerances = []
    raw = text.strip()
    try:
        obj = json.loads(raw)
    except Exception:
        m = FENCE_OPEN.search(raw)
        brace = raw.find("{", m.end()) if m else -1
        if brace == -1:
            raise ProducerValidationError("the response is not JSON and contains no ```json object. First "
                                "200 chars: %r" % raw[:200])
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw, brace)
        except Exception as ex:
            raise ProducerValidationError("the response's fenced block is not valid JSON (%s: %s)"
                                % (type(ex).__name__, ex))
        tolerances.append("UNFENCED: the answer arrived inside a ```json fence and was stripped")
    if not isinstance(obj, dict):
        raise ProducerValidationError("the response is valid JSON of type %s; the contract is a single "
                            "object" % type(obj).__name__)
    return obj, tolerances


def _quoted_case_sensitive_refs(sql, known_columns):
    """Double-quoted identifiers in `sql` that name a known column in a case Snowflake will not match.

    SNOWFLAKE FOLDS UNQUOTED IDENTIFIERS TO UPPERCASE AND MATCHES QUOTED ONES EXACTLY. The engine
    emits its projections UNQUOTED (`OrderID AS OrderID`), so the relations upstream of a
    model-authored body carry `ORDERID`, `ORDERSTATUS`, and so on. A body that writes
    `"OrderStatus"` is therefore asking for a column that does not exist, and the mixed case makes it
    read like a match to anyone reviewing it.

    MEASURED on Order Enrichment: three authored models quoted mixed-case (`int_m_5` in a WHERE,
    `int_m_7` in a join projection, `int_m_8` in a rename) and dbt answered

        No column OrderStatus found. Available are M_3.ORDERSTATUS, M_3.ORDERDATE, ...

    which names the column it could not find and the near-identical one it has, one line apart.

    Only names that MATCH A KNOWN COLUMN case-insensitively are reported. A quoted identifier that
    corresponds to nothing upstream may be a deliberately case-sensitive name from somewhere else,
    and guessing about it would turn this into a style rule.
    """
    if not sql or not known_columns:
        return []
    folded = {c.upper(): c for c in known_columns if c}
    out = []
    for quoted in re.findall(r'"([A-Za-z_][A-Za-z0-9_$]*)"', str(sql)):
        # An already-uppercase quoted name matches the folded column, so it is correct as written.
        if quoted.upper() == quoted:
            continue
        if quoted.upper() in folded and quoted not in out:
            out.append(quoted)
    return out


def validate(entry, req):
    """(cleaned_entry, notes) or raise ProducerError. `None` means the model abstained.

    Everything checked here is checked because the alternative is a downstream failure that is
    worse: an unknown `$kind` costs the whole document at hydration, a missing required payload
    costs it too or becomes `WHERE TRUE`, and an invented field name is a silent no-op that
    looks like a filled entry.
    """
    notes = []
    body_answer = False
    if "_abstain" in entry and len(
            [k for k in entry if not k.startswith("_")]) == 0:
        return None, ["ABSTAINED: %s" % str(entry.get("_abstain"))[:300]]

    kind = entry.get("$kind")
    # TIER2_KIND prose says "answer with ModelSql" when no hydrator kind can render
    # (join / GROUP BY / UNION / router). Models obey by setting $kind to "ModelSql".
    # That name is not a hydrator arm; it is the FIELD ai_fill reads. Coerce.
    if kind == "ModelSql":
        sql = entry.get("ModelSql")
        if isinstance(sql, str) and sql.strip():
            entry.pop("$kind", None)
            kind = None
            body_answer = True
        else:
            raise ProducerValidationError(
                "the response names $kind 'ModelSql' but supplies no ModelSql body. "
                "Put the SELECT in the ModelSql field and omit $kind.")
    if kind is not None:
        if not isinstance(kind, str) or kind not in KIND_CONTRACT:
            # A BODY IS NOT THROWN AWAY OVER THE LABEL ON IT.
            #
            # MEASURED, 2026-08-28 Alteryx: the Join, Union, Unique and Summarize elements each
            # answered `"$kind": "ModelSql"` AND supplied a correct `ModelSql` body -- a real
            # GROUP BY with SUM/AVG/COUNT, a real two-upstream join with aliases. The old code
            # rejected all four outright, and because the rejection text merely listed the legal
            # kinds, every one of them abstained on retry, three saying "ModelSql is not in the
            # accepted vocabulary". Four correct bodies were lost, and the fill loop could never
            # converge because the question had no legal answer in the form the model was given.
            #
            # `ModelSql` is a payload FIELD, so a body plus a non-kind label is an unambiguous
            # tier-3 answer wearing the wrong hat. Dropping `$kind` -- rather than substituting
            # one -- is the conservative repair: `effective_kind` then falls back to the request's
            # `expected_kind`, so the TABLE's classification stands and the model has not
            # re-classified anything. Exactly the shape the accepted tier-3 entries already have,
            # which carry a body and no `$kind` at all.
            body = entry.get("ModelSql")
            body_answer = isinstance(body, str) and bool(body.strip())
            if body_answer:
                notes.append(
                    "$kind was %r, which is not a kind; the response also carried a ModelSql "
                    "body, so $kind was DROPPED and the body kept as a tier-3 answer. The "
                    "table's own classification (%r) stands."
                    % (kind, req.get("expected_kind")))
                entry = {k: v for k, v in entry.items() if k != "$kind"}
                kind = None
            else:
                raise ProducerValidationError(
                    "the response names $kind %r. The hydrator's switch accepts exactly %s and "
                    "throws NotSupportedException on anything else, which loses the whole "
                    "document. A name outside a closed vocabulary is this project's central "
                    "failure shape, so it fails here instead. If no kind fits this element, "
                    "`ModelSql` is a FIELD and not a $kind: leave $kind as the element's "
                    "existing kind (or UnsupportedTransformation) and put the whole model body "
                    "in the separate `ModelSql` field."
                    % (kind, ", ".join(sorted(KIND_CONTRACT))))
        if req["shape"] == TIER2_PAYLOAD and kind != req["expected_kind"]:
            raise ProducerValidationError(
                "the response overrides $kind to %r on an element the platform table maps to %r. "
                "The request asked for a payload, not a re-classification: the table's mapping is "
                "a stated platform fact and this would replace it with an assertion."
                % (kind, req["expected_kind"]))
        if req.get("table_supported") is not True:
            raise ProducerValidationError(
                "the response overrides $kind to %r on an element the platform table declares "
                "supported=false. A structural re-classification would mask that refusal as a "
                "hydrator Success. Supply ModelSql if you can lower the element; do not name a "
                "$kind." % kind)

    # QUOTED MIXED-CASE IDENTIFIERS ARE REJECTED: it is a checkable contradiction against the
    # columns the upstreams actually carry, and the failure it produces is a dbt error whose two
    # halves differ only in case.
    known = []
    for u in (req.get("upstream") or []):
        known.extend(u.get("columns") or [])
    known.extend(req.get("emitted_columns") or [])
    suspect = []
    texts = [entry.get("ModelSql")]
    texts += [c.get("Expression") for c in (entry.get("OutputColumns") or [])
              if isinstance(c, dict)]
    texts += [entry.get(f) for f in PAYLOAD_STRING_FIELDS]
    for text in texts:
        for name in _quoted_case_sensitive_refs(text, known):
            if name not in suspect:
                suspect.append(name)
    if suspect:
        raise ProducerError(
            "the response double-quotes %s. Snowflake folds UNQUOTED identifiers to UPPERCASE and "
            "matches QUOTED ones exactly, and the upstream models emit their projections unquoted, "
            "so those columns are %s in the relation. A quoted mixed-case name therefore resolves to "
            "nothing -- dbt reports `No column <Name> found. Available are ...<NAME>`, naming the "
            "column it wants and the one it has, differing only in case. Write these identifiers "
            "UNQUOTED."
            % (", ".join('`"%s"`' % s for s in suspect),
               ", ".join("`%s`" % s.upper() for s in suspect)))

    effective_kind = kind or req.get("expected_kind")
    contract = KIND_CONTRACT.get(effective_kind or "", {"required": (), "optional": ()})

    # THE SAFETY RULE, UNWEAKENED -- AND SCOPED TO THE CASE IT IS ABOUT.
    #
    # The requirement is on WHOEVER SUPPLIES THE KIND. When the MODEL names the kind, it owns
    # that kind's payload: a sidecar `$kind` reaches `emit.py` which promotes it WITHOUT
    # re-checking required-ness, and the hydrator's `RequiredString` then throws and loses the
    # whole document. When the TABLE named the kind, the payload came from a table rule and is
    # already in the IR, so demanding it again from the model would be asking it to restate a
    # deterministic fact.
    #
    # MEASURED, on the first live run, and it is exactly the kind of false alarm this project
    # keeps catching: the check fired on `Write CUSTOMER_SUMMARY`, a TIER-3 request that asked
    # only for `ModelSql`. `TableName` was absent from the response because
    # `ktr_table_output_table` had ALREADY read it from the document -- the producer refused a
    # correct answer and wrote no sidecar for the other three elements either. A validator that
    # rejects right answers is worse than one that is lax, because it makes the measurement
    # about the harness.
    # `body_answer` means the kind was DROPPED above and the request is being answered with a
    # whole model body, so the kind in force is the TABLE's, not the model's. Demanding that
    # kind's payload here would be the same false alarm this block already records: refusing a
    # correct answer because the harness asked the wrong question.
    model_owns_kind = (kind is not None or req["shape"] == TIER2_KIND) and not body_answer
    if model_owns_kind:
        for f in contract["required"]:
            v = entry.get(f)
            if not (isinstance(v, str) and v.strip()):
                harm = ("FilterTranslator's shared base substitutes WHERE TRUE for an empty "
                        "predicate and records it only as a log warning, so the model would "
                        "silently return every row"
                        if f == "FilterConditions" else
                        "TargetTranslator uses it to name the relation being written, and "
                        "AiFirstProducerIrHydrator.RequiredString throws on its absence, which "
                        "loses the whole document rather than one element")
                raise ProducerValidationError(
                    "the response asserts $kind %r and supplies %s = %r. A model that names a "
                    "kind owns that kind's required payload: %s."
                    % (effective_kind, f, v, harm))
        if req["shape"] == TIER2_KIND and effective_kind == "SourceQualifier":
            v = entry.get("TableName")
            if not (isinstance(v, str) and v.strip()):
                raise ProducerValidationError(
                    "SourceQualifier without TableName emits a dangling FROM and "
                    "header-only ObjectReferences. Name the relation this element reads.")

    allowed = (ENTRY_STRUCTURAL_KEYS | set(contract["required"]) | set(contract["optional"]))
    for k in entry:
        if k.startswith("_"):
            continue
        if k not in allowed:
            raise ProducerValidationError(
                "the response carries field %r, which nothing reads. Legal fields for $kind %r "
                "are %s. An unread field looks like a filled entry and is a no-op, so it is a "
                "failure rather than a warning."
                % (k, effective_kind, ", ".join(sorted(allowed))))

    if req["shape"] == TIER2_PAYLOAD:
        for f in req["needed_fields"]:
            v = entry.get(f)
            if not (isinstance(v, str) and v.strip()):
                raise ProducerValidationError("the request asked for %s and the response supplies %r" % (f, v))

    cols = entry.get("OutputColumns")
    if cols is not None:
        if not isinstance(cols, list) or not cols:
            raise ProducerValidationError("OutputColumns must be a non-empty array; got %r" % (cols,))
        seen = set()
        for i, c in enumerate(cols):
            if not isinstance(c, dict):
                raise ProducerValidationError("OutputColumns[%d] is %s, not an object" % (i, type(c).__name__))
            for k in c:
                if k not in COLUMN_KEYS:
                    raise ProducerValidationError("OutputColumns[%d] carries %r; legal keys are %s"
                                        % (i, k, ", ".join(sorted(COLUMN_KEYS))))
            nm = c.get("Name")
            if not (isinstance(nm, str) and nm.strip()):
                raise ProducerValidationError("OutputColumns[%d] has no usable Name (%r)" % (i, nm))
            if nm.lower() in seen:
                # emit.py merges supplied columns into a by-name dict, so a duplicate SILENTLY
                # wins and the earlier expression disappears. Loud instead.
                raise ProducerValidationError("OutputColumns names %r twice; emit.py merges by name, so the "
                                    "second would silently replace the first" % nm)
            seen.add(nm.lower())
            ex = c.get("Expression")
            if ex is not None and not (isinstance(ex, str) and ex.strip()):
                raise ProducerValidationError("OutputColumns[%d] (%s) has an empty Expression. Omit the key "
                                    "for a passthrough column rather than emitting an empty "
                                    "expression." % (i, nm))
        if effective_kind is None:
            raise ProducerValidationError("OutputColumns supplied with no $kind. emit.py only merges "
                                "model-authored columns when the element has an ir_kind, so these "
                                "would be silently discarded.")

    sql = entry.get("ModelSql")
    if sql is not None:
        if not (isinstance(sql, str) and sql.strip()):
            raise ProducerValidationError("ModelSql is present and empty")
        if "!!!RESOLVE EWI!!!" in sql:
            raise ProducerValidationError("ModelSql carries the engine's blocking-EWI marker, so the fill "
                                "would replace a degraded model with a degraded model")
        if not modelsql_has_verb(sql):
            raise ProducerValidationError(
                "ModelSql has no SELECT/WITH statement dbt can compile as a model body. "
                "A body whose only verb is EXEC/EXECUTE/CALL/INSERT/UPDATE/DELETE/MERGE is "
                "not an authored dbt model -- ai_fill writes ModelSql as a model file "
                "verbatim and dbt has no query to run. If the source statement is a "
                "procedure invocation, abstain instead: "
                '{"_abstain": "<one sentence>"}. The element keeps its placeholder.')
        refs = set(re.findall(r"\{\{\s*ref\s*\(\s*['\"]([^'\"]+)['\"]", sql))
        known = {u["dbt_model"] for u in req["upstream"] if u.get("dbt_model")}
        known |= {d["dbt_model"] for d in req["downstream"] if d.get("dbt_model")}
        dangling = sorted(refs - known)
        if dangling:
            # NOT a hard failure, and the distinction is deliberate: this is WRONG, not
            # MALFORMED, and `dbt compile` (stage 4) is the thing that reads SQL. Recorded so a
            # dangling ref is a MEASURED failure mode rather than a silent one.
            notes.append("DANGLING REF: ModelSql references %s, which is not a model name this "
                         "element's neighbours carry (%s). dbt1005 at compile time."
                         % (", ".join(repr(d) for d in dangling),
                            ", ".join(sorted(known)) or "none"))

    if not any(k in entry for k in ("$kind", "ModelSql", "OutputColumns")
               ) and not (set(entry) & (set(contract["required"]) | set(contract["optional"]))):
        raise ProducerValidationError("the response supplies no $kind, no ModelSql, no OutputColumns and no "
                            "payload field. An entry that carries nothing is a failure, not an "
                            "empty success -- it would add a sidecar key that changes nothing "
                            "while reading as a filled one.")
    return entry, notes


# ---------------------------------------------------------------------------------------------
# PRODUCE. Census, one call per gap, validate, then write -- in that order, and the order is the
# atomicity: nothing reaches disk until every request has a valid entry or a recorded abstention.
# ---------------------------------------------------------------------------------------------

WHAT_THIS_IS = (
    "TIER 2/TIER 3 of the fallback ladder: the MODEL-AUTHORED sidecar for this document, "
    "produced by a real model call rather than inline by an assistant. Every value here was "
    "written by the model named in _produced_by after reading ONLY the element's own source "
    "fragment, its native kind, the target dialect and the platform's semantics sheet. NONE of "
    "it is read from the document by a deterministic rule, which is why the emitter records all "
    "of it as MODEL provenance rather than SOURCE. It is UNVERIFIED: nothing here compiled it, "
    "ran it, or compared it against source behaviour."
)


def _slug(element):
    """The one filename-safe form of an element name, shared by the dump writer and the resume
    lookup so the two sides of a rerun always agree on where a response lives."""
    return re.sub(r"[^A-Za-z0-9]+", "_", str(element)).strip("_")


def _retry_prompt(prompt0, error):
    """The correction ask for attempt 2+. `prompt0` -- the ORIGINAL, attempt-1 prompt -- is
    reused VERBATIM and only a correction section is appended: the element's source fragment,
    contract and evidence must not drift between attempts, only the model's answer should. Built
    from `prompt0` every time, not from the previous retry prompt, so a third attempt does not
    accumulate two stale error sections behind the current one."""
    return "\n".join([
        prompt0,
        "",
        "## Your previous answer was rejected",
        "",
        "This is the SAME element, SAME source fragment and SAME contract as above. Do not",
        "change what you are answering -- fix only the problem below. Validation said:",
        "",
        "```",
        str(error).strip(),
        "```",
        "",
        "Reply again with a single JSON object per the contract above, or "
        "`{\"_abstain\": \"<one sentence>\"}` if you now believe this element genuinely cannot "
        "be lowered. Reply with the JSON object only.",
    ])


def _ask_one(r, platform, sheet, model_cmd, timeout, attempts, prompt0):
    """Everything about one request that a model call touches, and NOTHING ELSE: no print, no
    file write. Safe to run off the main thread because it has no shared state -- `r` is this
    request's own dict, and the return value is handed back to the caller to print, dump and
    aggregate SERIALLY, in census order, so a fast request never prints ahead of a slow one that
    is earlier in the list.

    NEVER RAISES. Every attempt -- its prompt, the raw text (if any), and the error (if any) --
    is captured in the returned `attempts` list, so the caller can persist all of it regardless
    of the outcome. A `ProducerValidationError` (the ANSWER was wrong) is retried, with the
    validation error appended to the ORIGINAL prompt, up to `attempts` times. A plain
    `ProducerError` from `invoke` (could not run: exec failure, timeout, a non-zero exit, an
    error envelope) is NOT retried -- it is the could-not-run/auth/system class this project
    keeps finding, and retrying it blindly would spend `attempts` calls to relearn the same
    fact once. `entry is None` with `terminal_error` unset means a WELL-FORMED abstention, not a
    failure; `entry is None` with `terminal_error` set means every attempt was exhausted.
    """
    records = []
    prompt = prompt0
    entry, notes, tol, meta = None, [], [], {}
    last_error = None
    for i in range(1, attempts + 1):
        rec = {"attempt": i, "prompt": prompt}
        try:
            text, meta = invoke(model_cmd, prompt, timeout=timeout)
        except ProducerError as ex:
            rec["text"], rec["meta"], rec["error"] = None, {}, str(ex)
            records.append(rec)
            last_error = str(ex)
            meta = {}
            break  # could-not-run: not this request's to retry
        rec["text"], rec["meta"] = text, meta
        try:
            obj, tol = parse_response(text)
            entry, notes = validate(obj, r)
        except ProducerValidationError as ex:
            rec["error"] = str(ex)
            records.append(rec)
            last_error = str(ex)
            entry = None
            if i < attempts:
                prompt = _retry_prompt(prompt0, str(ex))
                continue
            break  # attempts exhausted, still invalid
        rec["error"] = None
        records.append(rec)
        last_error = None
        break  # a valid entry OR a well-formed abstention -- both are success
    terminal_error = last_error if entry is None and last_error else None
    return {"element": r["element"], "attempts": records, "entry": entry,
            "notes": notes or [], "tolerances": tol or [], "meta": meta,
            "terminal_error": terminal_error}


def _resume_lookup(dump_dir, r, prompt):
    """A previously dumped response for this EXACT request, reusable with no model call, or
    `None`. The exact-prompt check is the whole safety property: the dumped prompt's bytes must
    equal the prompt this run just built for this element, or the response is never reused --
    silently or otherwise. If the platform table, the source document, or `build_prompt` itself
    changed since the dump was written, the byte comparison fails and the request is asked
    fresh. Only attempt 1 is ever a candidate: a retry prompt (attempt 2+) carries the PRIOR
    run's specific validation error baked in, so it can never equal a freshly built prompt.

    Checks this producer's current per-attempt naming first, then the flat legacy naming an
    older cut used (no `.attemptN.` infix), so a dump directory written before `--attempts`
    existed is still resumable without a naming migration.
    """
    slug = _slug(r["element"])
    candidates = [
        (os.path.join(dump_dir, slug + ".attempt1.prompt.md"),
         os.path.join(dump_dir, slug + ".attempt1.response.txt")),
        (os.path.join(dump_dir, slug + ".prompt.md"),
         os.path.join(dump_dir, slug + ".response.txt")),
    ]
    for prompt_path, response_path in candidates:
        try:
            with open(prompt_path, encoding="utf-8") as fh:
                old_prompt = fh.read()
        except OSError:
            continue
        if old_prompt != prompt:
            continue  # STALE — not byte-identical, never trusted regardless of content
        try:
            with open(response_path, encoding="utf-8") as fh:
                old_text = fh.read()
        except OSError:
            continue
        try:
            obj, tol = parse_response(old_text)
            entry, notes = validate(obj, r)
        except ProducerValidationError:
            continue  # the dumped response was itself invalid — ask fresh, do not reuse it
        return {"element": r["element"], "entry": entry, "notes": notes, "tolerances": tol,
                "meta": {}, "terminal_error": None, "resumed_from": response_path,
                "attempts": [{"attempt": 1, "prompt": prompt, "text": old_text, "error": None,
                              "resumed": True}]}
    return None


def _dump_attempts(dump_dir, element, outcome):
    """Every attempt's prompt/response/error, one file per attempt -- MAIN THREAD ONLY, so a
    dump directory is never read by `_resume_lookup` in one process while another thread could
    still be writing into it. Named so `_resume_lookup` can always find attempt 1 on a later
    rerun; attempt 1 is additionally mirrored to the flat legacy names, which cost nothing to
    write and are what an older dump directory (and `_resume_lookup`'s fallback branch) expects.
    """
    os.makedirs(dump_dir, exist_ok=True)
    slug = _slug(element)
    for rec in outcome.get("attempts") or []:
        base = os.path.join(dump_dir, "%s.attempt%d" % (slug, rec["attempt"]))
        with open(base + ".prompt.md", "w", encoding="utf-8") as fh:
            fh.write(rec.get("prompt") or "")
        with open(base + ".response.txt", "w", encoding="utf-8") as fh:
            fh.write(rec.get("text") or "")
        err_path = base + ".error.txt"
        err = rec.get("error")
        if err:
            with open(err_path, "w", encoding="utf-8") as fh:
                fh.write(err)
        elif os.path.exists(err_path):
            # A rerun that now succeeds on an attempt number that previously failed must not
            # leave a stale error file sitting beside a fresh, valid response.
            os.remove(err_path)
        if rec["attempt"] == 1:
            with open(os.path.join(dump_dir, slug + ".prompt.md"), "w", encoding="utf-8") as fh:
                fh.write(rec.get("prompt") or "")
            with open(os.path.join(dump_dir, slug + ".response.txt"), "w", encoding="utf-8") as fh:
                fh.write(rec.get("text") or "")


def produce(args):
    cen = census(args.table, args.doc, tree=args.tree)
    if getattr(args, "only", None):
        # NARROWING THE ASK, not the census. The full gap list is still computed and printed, so
        # a narrowed run cannot read as "the document only had one gap" -- that conflation is how
        # a partial measurement becomes a claim about the whole document. Exists because one
        # element failing validation should be retryable without re-paying for the other three,
        # and because a negative test needs to drive ONE request with one canned answer.
        keep = [r for r in cen["requests"] if args.only.lower() in r["element"].lower()]
        cen["_narrowed_from"] = [r["element"] for r in cen["requests"]]
        cen["requests"] = keep
    table = json.load(open(args.table, encoding="utf-8"))
    sheet = semantics_sheet(table, args.semantics)
    platform = cen["platform"]

    print("=" * W)
    print(" SIDECAR PRODUCER — the model step, as a model call")
    print("=" * W)
    print(" document      : %s" % cen["document"])
    print(" platform      : %s   [table %s]" % (platform, os.path.basename(cen["table"])))
    print(" elements      : %d non-container element(s); %d container(s) excluded by role (%s)"
          % (cen["elements_total"], len(cen["containers_excluded"]),
             ", ".join(cen["containers_excluded"]) or "none"))
    if cen.get("orphans_unidentified"):
        print(" *** ORPHAN IR NODE(S) with no identification element — not gaps, not "
              "containers, and NOT silently omitted from the census: %s"
              % ", ".join(cen["orphans_unidentified"]))
    if cen.get("modelless_elements"):
        print(" *** NO MODEL FILE AT ALL for %d element(s), so the fill ladder cannot reach them "
              "and this run does NOT improve them: %s"
              % (len(cen["modelless_elements"]), ", ".join(cen["modelless_elements"])))
    print(" tree          : %s" % (cen["tree"] or "NONE — tier-3 requests are NOT raised without "
                                                 "an emitted tree to read"))
    print(" semantics     : %s" % args.semantics)
    print(" model cmd     : %s" % args.model_cmd)
    print("-" * W)
    if not cen["requests"]:
        print(" NO GAPS. The deterministic path represented every element of this document, so a")
        print(" model is not asked anything and no sidecar is written. This is TIER 1 WINNING, not")
        print(" a failure to produce: a sidecar entry for an element the engine already renders")
        print(" could only make it worse, and emit.py would not read it anyway.")
        print(" requests      : 0")
        return 0

    if cen.get("_narrowed_from"):
        print(" *** NARROWED by --only %r: %d of %d request(s) will be asked. The other(s) are"
              % (args.only, len(cen["requests"]), len(cen["_narrowed_from"])))
        print("     STILL GAPS and are simply not asked about in this run: %s"
              % ", ".join(e for e in cen["_narrowed_from"]
                          if e not in {r["element"] for r in cen["requests"]}))
    print(" %d request(s) — the deterministic path declined these and nothing else:"
          % len(cen["requests"]))
    for r in cen["requests"]:
        print("   %-34s %-16s %s" % (r["element"][:34], r["shape"],
                                     ", ".join(r["needed_fields"]) or "$kind + OutputColumns"))
        for why in r["deterministic_reasons"]:
            for chunk in _wrap(why, W - 8):
                print("        %s" % chunk)
    print("-" * W)

    parallelism = max(1, int(getattr(args, "parallelism", 4) or 4))
    attempts = max(1, int(getattr(args, "attempts", 3) or 3))
    resume = bool(getattr(args, "resume", True)) and bool(args.dump_prompts)
    print(" parallelism   : %d worker(s) (bounded; results merge in census order)" % parallelism)
    print(" attempts      : %d per request; resume=%s" % (attempts, "on" if resume else "off"))

    entries, abstained, notes_all, tolerances_all, metas, failed = {}, [], [], [], [], []
    prompts = {r["element"]: build_prompt(r, platform, sheet) for r in cen["requests"]}

    # RESUME IS A MAIN-THREAD, PRE-DISPATCH LOOKUP: an element is only skipped if a previously
    # dumped attempt-1 prompt is BYTE-IDENTICAL to the prompt just built for it here, so a resumed
    # entry is never trusted against a table, document or contract that has since changed.
    resumed = {}
    if resume:
        for r in cen["requests"]:
            hit = _resume_lookup(args.dump_prompts, r, prompts[r["element"]])
            if hit:
                resumed[r["element"]] = hit
        if resumed:
            print(" resumed       : %d of %d request(s) reused from %s — no model call"
                  % (len(resumed), len(cen["requests"]), args.dump_prompts))
    to_ask = [r for r in cen["requests"] if r["element"] not in resumed]

    # BOUNDED CONCURRENCY, ORDERED MERGE. Model invocation + parse + validate run off the main
    # thread -- `_ask_one` touches no shared state and NEVER RAISES -- but every print, every
    # dump-prompts write and every aggregation below happens on the main thread, walking
    # `cen["requests"]` in the SAME order the serial code did. So a request that finishes first
    # never prints or is written ahead of an earlier one, and calling `.result()` on request N
    # can never be skipped by an earlier request's exception, because none of them raise --
    # `produce()` drains every future, in order, regardless of which ones failed internally.
    with ThreadPoolExecutor(max_workers=parallelism, thread_name_prefix="sidecarProducer") as pool:
        futures = {r["element"]: pool.submit(_ask_one, r, platform, sheet, args.model_cmd,
                                              args.timeout, attempts, prompts[r["element"]])
                   for r in to_ask}
        for r in cen["requests"]:
            element = r["element"]
            prompt = prompts[element]
            if element in resumed:
                print(" asking about  : %s   [RESUMED — no model call]" % element)
                outcome = resumed[element]
            else:
                print(" asking about  : %s" % element)
                outcome = futures[element].result()
                if args.dump_prompts:
                    _dump_attempts(args.dump_prompts, element, outcome)

            meta = outcome["meta"]
            tol = outcome["tolerances"]
            notes = outcome["notes"]
            entry = outcome["entry"]
            n_attempts = len(outcome["attempts"])
            terminal_error = outcome["terminal_error"]

            metas.append(meta)
            print("   [%d char prompt, sha256 %s]" % (len(prompt), _sha_text(prompt)[:12]))
            if n_attempts > 1:
                print("   [%d attempt(s)]" % n_attempts)

            if terminal_error:
                print("   *** FAILED after %d attempt(s): %s" % (n_attempts, terminal_error))
                failed.append({"element": element, "error": terminal_error, "attempts": n_attempts})
                continue

            for t in tol:
                print("   *** %s" % t)
                tolerances_all.append("%s: %s" % (element, t))
            for n in notes:
                print("   *** %s" % n)
                notes_all.append("%s: %s" % (element, n))
            if entry is None:
                abstained.append(element)
                continue
            entry = dict(entry)
            entry["_produced"] = {
                "shape": r["shape"],
                "asked_for": r["needed_fields"] or ["$kind", "OutputColumns"],
                "native_kind": r["native_kind"],
                "deterministic_reason": r["deterministic_reasons"],
                "prompt_sha256": _sha_text(prompt),
                "model": meta.get("models"),
                "notes": notes,
                "tolerances": tol,
                "attempts": n_attempts,
            }
            entries[element] = entry

    if failed:
        # THE ALL-OR-NOTHING RULE, UNCHANGED BY RETRY: one request exhausting every attempt is
        # still refused exactly like the old single-attempt raise was -- NOTHING is written, and
        # every OTHER request's now-durable attempt records stay on disk under --dump-prompts so
        # a rerun (with --resume) does not re-pay for what already succeeded.
        print("-" * W)
        print(" %d of %d request(s) FAILED after %d attempt(s) each. NOTHING is written: the "
              "all-or-nothing rule" % (len(failed), len(cen["requests"]), attempts))
        print(" does not weaken because some requests succeeded.")
        for f in failed:
            print("   *** %s: %s" % (f["element"], f["error"]))
        if args.dump_prompts:
            os.makedirs(args.dump_prompts, exist_ok=True)
            fail_path = os.path.join(args.dump_prompts, "_failures.json")
            with open(fail_path, "w", encoding="utf-8") as fh:
                json.dump({"failed": failed, "attempts": attempts}, fh, indent=2)
                fh.write("\n")
            print(" failures      : %s" % os.path.abspath(fail_path))
        return 1

    if not entries:
        print("-" * W)
        print(" NO ENTRIES. Every request abstained (%s). No sidecar is written — an empty sidecar"
              % ", ".join(abstained))
        print(" and no sidecar are the same input, and writing one would claim a model was")
        print(" consulted usefully.")
        return 0

    models = sorted({m for meta in metas for m in (meta.get("models") or [])})
    cost = sum(m.get("cost_usd") or 0 for m in metas)
    out = {
        "_what_this_is": WHAT_THIS_IS,
        "_produced_by": {
            "producer": "sidecar_producer.py",
            "contract": "sidecar.model.v1",
            "model": models or ["UNREPORTED — the model command returned no metadata"],
            "model_cmd": args.model_cmd,
            "semantics_sheet": args.semantics,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "document_sha256": cen["document_sha256"],
            "platform": platform,
            "requests": len(cen["requests"]),
            "entries": len(entries),
            "abstained": abstained,
            "total_cost_usd": round(cost, 6) if cost else None,
            "_verification": ("NONE. Nothing in this pipeline compiled, executed or compared any "
                              "value here against source behaviour. Treat every expression as "
                              "unverified."),
        },
        "elements": entries,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print("-" * W)
    print(" model         : %s" % ", ".join(models or ["UNREPORTED"]))
    print(" entries       : %d written, %d abstained%s"
          % (len(entries), len(abstained),
             (" (%s)" % ", ".join(abstained)) if abstained else ""))
    if tolerances_all:
        print(" tolerances    : %d response(s) needed unfencing" % len(tolerances_all))
    if notes_all:
        print(" notes         : %d — WRONG but not MALFORMED, so recorded rather than refused:"
              % len(notes_all))
        for n in notes_all:
            for chunk in _wrap(n, W - 8):
                print("        %s" % chunk)
    if cost:
        print(" cost          : $%.4f" % cost)
    print(" sidecar       : %s" % os.path.abspath(args.out))
    return 0


# ---------------------------------------------------------------------------------------------
# DIFF — the produced sidecar against the hand-authored baseline, field by field.
#
# The bar is AGREEMENT PER FIELD with the disagreements printed in full, not a score. Same
# reason gate_a.py refuses to print a percentage: a number over a denominator the comparison
# chooses is a number the comparison can move. Every field of the union of both entries is
# reported, so a field the model omitted and a field it invented are both visible.
# ---------------------------------------------------------------------------------------------

def _norm_sql(s):
    """Whitespace-insensitive, case-insensitive on keywords only via upper(). Deliberately NOT
    a SQL parser: an equality that depends on a normaliser nobody checked is worse than a
    literal one, so the normaliser does exactly two things and both are printed."""
    return re.sub(r"\s+", " ", str(s)).strip()


def _cols(entry):
    return {str(c.get("Name", "")).lower(): c for c in (entry.get("OutputColumns") or [])}


def diff(args):
    got = json.load(open(args.produced, encoding="utf-8")).get("elements") or {}
    want = json.load(open(args.baseline, encoding="utf-8")).get("elements") or {}
    print("=" * W)
    print(" SIDECAR QUALITY DIFF — model-authored against hand-authored")
    print("=" * W)
    print(" produced      : %s" % os.path.abspath(args.produced))
    print(" baseline      : %s" % os.path.abspath(args.baseline))
    print(" NORMALISATION : whitespace collapsed. Nothing else. Case, parenthesisation and")
    print("                 function choice are compared LITERALLY, so an equivalent expression")
    print("                 spelled differently reads as a MISMATCH and is printed in full for a")
    print("                 human to judge. A semantic comparator would need a SQL engine, and a")
    print("                 hand-written one would be the thing under test.")
    print("-" * W)

    rows = []
    payload_fields = ("FilterConditions", "TableName", "SchemaName", "Database", "$kind")
    for el in sorted(set(got) | set(want)):
        g, w = got.get(el), want.get(el)
        if g is None:
            rows.append((el, "ELEMENT", "ABSENT_FROM_PRODUCED", "", ""))
            continue
        if w is None:
            rows.append((el, "ELEMENT", "ABSENT_FROM_BASELINE", "", ""))
            continue
        for f in payload_fields:
            if f not in g and f not in w:
                continue
            gv, wv = g.get(f), w.get(f)
            verdict = ("MATCH" if _norm_sql(gv) == _norm_sql(wv)
                       else "ONLY_PRODUCED" if wv is None
                       else "ONLY_BASELINE" if gv is None else "MISMATCH")
            rows.append((el, f, verdict, gv, wv))
        gc, wc = _cols(g), _cols(w)
        for cn in sorted(set(gc) | set(wc)):
            gv = (gc.get(cn) or {}).get("Expression")
            wv = (wc.get(cn) or {}).get("Expression")
            if cn not in gc:
                rows.append((el, "OutputColumns[%s]" % cn, "ONLY_BASELINE", None, wv))
            elif cn not in wc:
                rows.append((el, "OutputColumns[%s]" % cn, "ONLY_PRODUCED", gv, None))
            else:
                rows.append((el, "OutputColumns[%s].Expression" % cn,
                             "MATCH" if _norm_sql(gv) == _norm_sql(wv) else "MISMATCH", gv, wv))
        if "ModelSql" in g or "ModelSql" in w:
            gv, wv = g.get("ModelSql"), w.get("ModelSql")
            verdict = ("MATCH" if _norm_sql(gv) == _norm_sql(wv)
                       else "ONLY_PRODUCED" if wv is None
                       else "ONLY_BASELINE" if gv is None else "MISMATCH")
            rows.append((el, "ModelSql", verdict, gv, wv))
        for f in ("_semantic_divergence", "_reasoning", "_source_expression"):
            gp, wp = f in g, f in w
            if gp or wp:
                rows.append((el, f, "BOTH_PRESENT" if gp and wp
                             else "ONLY_PRODUCED" if gp else "ONLY_BASELINE",
                             (str(g.get(f))[:400] if gp else None),
                             (str(w.get(f))[:400] if wp else None)))

    counts = {}
    for _, _, v, _, _ in rows:
        counts[v] = counts.get(v, 0) + 1
    cur = None
    for el, f, v, gv, wv in rows:
        if el != cur:
            print(" %s" % el)
            cur = el
        print("   %-46s %s" % (f[:46], v))
        if v in ("MISMATCH", "ONLY_PRODUCED", "ONLY_BASELINE"):
            if gv is not None:
                for chunk in _wrap("produced: " + _norm_sql(gv)[:600], W - 8):
                    print("        %s" % chunk)
            if wv is not None:
                for chunk in _wrap("baseline: " + _norm_sql(wv)[:600], W - 8):
                    print("        %s" % chunk)
            if v == "MISMATCH" and gv is not None and wv is not None:
                sm = difflib.SequenceMatcher(None, _norm_sql(gv), _norm_sql(wv))
                print("        similarity: %.2f" % sm.ratio())
    print("-" * W)
    print(" comparisons   : " + "  ".join("%s %d" % (k, counts[k]) for k in sorted(counts)))
    hard = [r for r in rows if r[2] in ("MISMATCH", "ONLY_BASELINE", "ABSENT_FROM_PRODUCED")]
    print(" DISAGREEMENTS : %d of %d comparison(s). NO PERCENTAGE IS REPORTED: the denominator is"
          % (len(hard), len(rows)))
    print("                 a set this comparison chose, so a rate here would be a number the")
    print("                 comparison can move. The count and the list are the result.")
    return 0


# ---------------------------------------------------------------------------------------------
# VARIANCE — N calls, one element, same prompt. Is the answer the same one twice?
#
# This is not a nice-to-have. A tier-2 payload that changes between runs makes the migration
# IRREPRODUCIBLE: the same source document yields different SQL, so a reviewer who approved run
# 1 has not approved run 2, and the sidecar's whole claim to being "inspectable, diffable and
# replayable" (findings/41) rests on the FILE being replayable rather than the call. Instability
# is therefore a finding either way -- it argues the file must be committed, not regenerated.
# ---------------------------------------------------------------------------------------------

def variance(args):
    cen = census(args.table, args.doc, tree=args.tree)
    table = json.load(open(args.table, encoding="utf-8"))
    sheet = semantics_sheet(table, args.semantics)
    reqs = [r for r in cen["requests"]
            if args.element is None or args.element.lower() in r["element"].lower()]
    if not reqs:
        raise ProducerError("no request matches element %r. This document raises: %s"
                            % (args.element, ", ".join(r["element"] for r in cen["requests"])
                               or "nothing"))
    print("=" * W)
    print(" SIDECAR VARIANCE — %d run(s) per element, identical prompt" % args.runs)
    print("=" * W)
    print(" document      : %s" % cen["document"])
    print(" semantics     : %s   model cmd: %s" % (args.semantics, args.model_cmd))
    rc = 0
    all_runs = {}
    for r in reqs:
        prompt = build_prompt(r, cen["platform"], sheet)
        print("-" * W)
        print(" element       : %s   [%s, prompt sha256 %s]"
              % (r["element"], r["shape"], _sha_text(prompt)[:12]))
        runs = []
        for i in range(args.runs):
            try:
                text, meta = invoke(args.model_cmd, prompt, timeout=args.timeout)
                obj, tol = parse_response(text)
                entry, notes = validate(obj, r)
                runs.append({"run": i + 1, "ok": True, "entry": entry, "notes": notes,
                             "tolerances": tol, "model": meta.get("models"),
                             "cost": meta.get("cost_usd")})
                print("   run %d/%d: OK%s" % (i + 1, args.runs,
                                              " [%s]" % "; ".join(tol) if tol else ""))
            except ProducerError as ex:
                runs.append({"run": i + 1, "ok": False, "error": str(ex)})
                print("   run %d/%d: FAILED — %s" % (i + 1, args.runs, str(ex)[:200]))
        all_runs[r["element"]] = runs

        good = [x for x in runs if x["ok"] and x["entry"] is not None]
        print("   runs usable : %d of %d  (abstained %d, failed %d)"
              % (len(good), len(runs),
                 sum(1 for x in runs if x["ok"] and x["entry"] is None),
                 sum(1 for x in runs if not x["ok"])))
        if not good:
            rc = 1
            continue
        # ALSO REPORT THE SHAPE OF THE ANSWER, not only its fields. Which fields a run supplies
        # at all is itself unstable -- on Pentaho's derive step 2 of 5 runs added a whole tier-3
        # ModelSql and 1 of 5 listed six output columns instead of two -- and a per-field table
        # cannot show that, because a field only appears in it once some run produced it.
        shapes = {}
        for x in good:
            key = "|".join(sorted(k for k in x["entry"] if not k.startswith("_")))
            ncols = len(x["entry"].get("OutputColumns") or [])
            shapes.setdefault("%s  [%d output column(s)]" % (key, ncols), 0)
            shapes["%s  [%d output column(s)]" % (key, ncols)] += 1
        print("   ANSWER SHAPE                               %s  %d distinct over %d run(s)"
              % ("STABLE" if len(shapes) == 1 else "*** UNSTABLE", len(shapes), len(good)))
        for k, n in sorted(shapes.items(), key=lambda kv: -kv[1]):
            print("        %s x%d  %s" % ("=" if len(shapes) == 1 else "-", n, k))
        # Per-field stability. Reported field by field rather than as one "identical" flag,
        # because $kind stable with a drifting predicate and both drifting are different facts
        # and only the first is survivable.
        fields = set()
        for x in good:
            fields |= {k for k in x["entry"] if not k.startswith("_") and k != "OutputColumns"}
        for x in good:
            for c in (x["entry"].get("OutputColumns") or []):
                fields.add("OutputColumns[%s]" % str(c.get("Name")).lower())
        for f in sorted(fields):
            vals = []
            for x in good:
                if f.startswith("OutputColumns["):
                    # ABSENT and PASSTHROUGH ARE DIFFERENT FACTS, and the first version of this
                    # reporter collapsed them. `_norm_sql(None)` is the string "None" whether the
                    # column is missing from the entry entirely or present with no Expression, so
                    # a run that dropped four columns and a run that passed them through read as
                    # IDENTICAL -- and this table printed `OutputColumns[firstname] STABLE x5`
                    # over five runs in which one entry listed six columns and four listed two.
                    # A variance reporter that under-reports variance is the same defect class as
                    # a gate that cannot fail, committed in the tool written to detect it.
                    nm = f[len("OutputColumns["):-1]
                    col = _cols(x["entry"]).get(nm)
                    if col is None:
                        vals.append("<COLUMN ABSENT FROM THIS RUN>")
                    elif col.get("Expression") is None:
                        vals.append("<PASSTHROUGH, no expression>")
                    else:
                        vals.append(_norm_sql(col.get("Expression")))
                elif f not in x["entry"]:
                    vals.append("<FIELD ABSENT FROM THIS RUN>")
                else:
                    vals.append(_norm_sql(x["entry"].get(f)))
            distinct = sorted(set(vals))
            print("   %-42s %s  %d distinct value(s) over %d run(s)"
                  % (f[:42], "STABLE" if len(distinct) == 1 else "*** UNSTABLE",
                     len(distinct), len(good)))
            for d in distinct:
                print("        %s x%d  %s" % ("=" if len(distinct) == 1 else "-",
                                              vals.count(d), d[:200]))
        div = sum(1 for x in good if "_semantic_divergence" in x["entry"])
        print("   _semantic_divergence recorded in %d of %d usable run(s)" % (div, len(good)))
    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            json.dump(all_runs, fh, indent=1)
        print("-" * W)
        print(" runs saved    : %s" % os.path.abspath(args.save))
    return rc


def main(argv):
    ap = argparse.ArgumentParser(prog="sidecar_producer.py",
                                 description="Tier-2/tier-3 sidecar producer — a real model call.")
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("table")
        p.add_argument("doc")
        p.add_argument("--tree", default=None,
                       help="an emitted output root. Tier-3 (ModelSql) requests are raised ONLY "
                            "with this: whether a model is unusable is a fact about the artifact, "
                            "and ai_fill.is_degraded is what decides it.")
        p.add_argument("--semantics", choices=("rules", "full", "none"), default="rules")
        p.add_argument("--model-cmd", dest="model_cmd", default=DEFAULT_MODEL_CMD)
        p.add_argument("--timeout", type=int, default=300)

    p = sub.add_parser("census", help="the deterministic gap list. No model call.")
    common(p)

    p = sub.add_parser("produce")
    common(p)
    p.add_argument("--out", required=True)
    p.add_argument("--only", default=None,
                   help="ask only about requests whose element name contains this substring. The "
                        "full census is still computed and printed.")
    p.add_argument("--dump-prompts", dest="dump_prompts", default=None,
                   help="write every prompt to this directory. The prompt is the experiment; a "
                        "measurement whose question nobody can read is not reproducible.")
    p.add_argument("--parallelism", type=int,
                   default=int(os.environ.get("AIFIRST_AUTHORING_PARALLELISM", "4")),
                   help="bounded worker count for concurrent model calls (min 1). Requests stay "
                        "isolated and results still merge in census order.")
    p.add_argument("--attempts", type=int, default=3,
                   help="model calls per request before it counts as a terminal failure. Only a "
                        "malformed/invalid ANSWER is retried, with the validation error appended "
                        "to the original prompt; a could-not-run failure (exec, timeout, "
                        "non-zero exit) is never retried.")
    p.add_argument("--resume", dest="resume", action="store_true", default=True,
                   help="with --dump-prompts, reuse a prior run's dumped attempt-1 response for "
                        "an element whose freshly built prompt is byte-identical to the one "
                        "dumped for it (default on).")
    p.add_argument("--no-resume", dest="resume", action="store_false",
                   help="always call the model, even where --dump-prompts holds a reusable "
                        "response for the current prompt.")

    p = sub.add_parser("diff")
    p.add_argument("produced")
    p.add_argument("baseline")

    p = sub.add_parser("variance")
    common(p)
    p.add_argument("--element", default=None, help="substring of the element name; default all")
    p.add_argument("--runs", type=int, default=5)
    p.add_argument("--save", default=None)

    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help(sys.stderr)
        return 2
    try:
        if args.cmd == "census":
            cen = census(args.table, args.doc, tree=args.tree)
            print("=" * W)
            print(" SIDECAR CENSUS — what the DETERMINISTIC path declined")
            print("=" * W)
            print(" document      : %s" % cen["document"])
            print(" platform      : %s" % cen["platform"])
            print(" elements      : %d non-container; containers excluded by role: %s"
                  % (cen["elements_total"], ", ".join(cen["containers_excluded"]) or "none"))
            print(" tree          : %s" % (cen["tree"] or "NONE — no tier-3 requests raised"))
            if cen.get("modelless_elements"):
                print(" *** NO MODEL FILE for: %s" % ", ".join(cen["modelless_elements"]))
            print(" requests      : %d" % len(cen["requests"]))
            for r in cen["requests"]:
                print("-" * W)
                print(" %s" % r["element"])
                print("   native kind : %s   role %s   model %s"
                      % (r["native_kind"], r["role"], r["model_name"]))
                print("   shape       : %s   asks for: %s"
                      % (r["shape"], ", ".join(r["needed_fields"]) or "$kind + OutputColumns"))
                for why in r["deterministic_reasons"]:
                    for chunk in _wrap("why: " + why, W - 6):
                        print("     %s" % chunk)
                print("   source text : %d char(s)%s"
                      % (len(r["source_text"]),
                         "" if r["source_text"] else "  *** EMPTY — the model would be asked to "
                                                     "lower nothing"))
            return 0
        if args.cmd == "produce":
            return produce(args)
        if args.cmd == "diff":
            return diff(args)
        return variance(args)
    except ProducerError as ex:
        sys.stderr.write("SIDECAR PRODUCER FAILED: %s\n" % ex)
        sys.stderr.write("NO SIDECAR WAS WRITTEN. The deterministic path is unchanged.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
