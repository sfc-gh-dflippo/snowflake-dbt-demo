"""GATE B (intent parity) — DOES THE GENERATED SQL DO WHAT THE SOURCE ELEMENT SAYS?

Gate A asks whether the IR carries what the document states. This asks the next question, about the
artifact rather than the representation: for each thing the emitter wrote, what does the source element
say, what does the SQL do, and are those the same for every input? Three subcommands plus one scorer
for the pre-registered falsifiability case:

    pack     build a blind evidence bundle from the EMITTED PROJECT + the source document
    verifier hand that bundle to a model call, isolated by gate_a's own machinery
    score    ingest the answers, re-read every citation, adjudicate, emit divergences as issues
    run      pack, verify, score
    falsify  score the disqualifying case across two scored bundles

WHY A MODEL AND NOT A RULE — the measured justification
------------------------------------------------------
Both the SSIS and the Informatica derive models contain the BYTE-IDENTICAL string

    FirstName || ' ' || MiddleName || ' ' || LastName AS FullName

and one of them is wrong. SSIS `+` propagates NULL and so does Snowflake `||`, so that lowering is
faithful; Informatica `||` does NOT propagate NULL, so the same generated line silently turns a name
with a NULL middle name into NULL. No structural check, diff, linter or compiler can tell those two
apart, because there is nothing structurally different about them. The discriminator is the semantics
of the platform each came from, which is a reading task.

`findings/43` measured six hand-staged verifier runs against criteria fixed in advance
(`findings/42`) and they got it right 4 of 4 -- DIVERGENT on Informatica, EQUIVALENT on SSIS, with
both SSIS arms refusing the Informatica rule explicitly. This module is that method as code.

WHAT IT RAISES, deterministically, BEFORE any verifier is invoked
----------------------------------------------------------------
Three families, and the denominator is the EMITTED ARTIFACT in every one of them, parsed rather than
described:

  EX:<model>#<column>  one per output column the generated SQL names. THE UNIT OF THE JUDGEMENT, and
                       it is a column rather than a model because a model verdict conflates
                       expressions: the Informatica derive model carries the concat divergence AND an
                       invalid function, and the Pentaho one carries a real divergence AND the
                       `getYear() + 1900` false-positive trap. A per-model roll-up cannot score either
                       pair, and the pre-registered disqualifying case is about ONE column.
  MD:<model>           one per emitted model: row shape, materialization, whether its refs resolve,
                       whether it is a placeholder rather than SQL.
  TREE:dag             one for the model set as a whole. `findings/42` TEST 5 exists because a
                       DataStage tree came back with 3 models, 2 of them blocking placeholders and 0
                       edges, and per-model verdicts read as though the tree were complete.

THE BAR IS OBLIGATIONS DISCHARGED. IT IS NEVER A SCORE.
-------------------------------------------------------
Same as Gate A, for the same measured reason (the fit score ROSE as elements were lost):

  * the raised set is recomputed from the staged artifact every iteration and cannot shrink;
  * an obligation with no answer is OUTSTANDING, never silently discharged;
  * an answer naming an obligation that was not raised is REJECTED;
  * `raised == discharged + outstanding` is asserted and printed;
  * no percentage appears in the verdict.

SOURCING BUYS CALIBRATION, AND THAT IS NOW MECHANICAL
-----------------------------------------------------
`findings/43` TEST 6 went against the design's claim: both the sourced and the naive arm caught the
concat case, so primary sources are NOT load-bearing for detection. What differed was calibration --
the sourced verifiers refused to assert rules the sheet did not cover, the naive ones asserted from
memory with "I am confident on this rule" and were right unearnedly. An uncalibrated verifier that
happens to be right is a verifier you cannot trust on the next case.

So the mechanism here is not an exhortation to be careful. Every claim declares a `basis`, and:

  * `SHEET_PRIMARY` / `SHEET_COMMON` must carry a `sheet_quote` that the scorer RE-READS in the staged
    reference sheet. A claim that says it rests on a primary source and cannot quote one is not sourced;
  * `DOCUMENT` and `SQL` must carry a locus and quote that the scorer re-reads in the document or in
    the staged model file;
  * `PRIOR` is QUARANTINED BY CONSTRUCTION and printed. Right-from-memory is visible and never counted.

In the naive arm (`--arm naive`, no sheet staged) a dialect rule can only be declared `PRIOR`, so the
naive arm's detections are printed and discharge nothing. That is the measured finding turned into a
property of the harness rather than a paragraph in a report.

WHAT A DIVERGENCE HAS TO CARRY
------------------------------
`findings/42`: "DIVERGENT was defined as requiring a concrete input on which source and generated SQL
differ." So a DIVERGENT claim needs `failing_input` and `differs_as` -- what each side yields for that
input -- or it is quarantined as prose. Prose about migration risk is what this gate is trying to
replace.

WHERE THE OUTPUT GOES
---------------------
Divergences are the FDM/EWI content the engine cannot produce for a platform it does not support, so
they are emitted into the issue framework's inventory (`issues/`) as proposals classified through its
own `classify()`, plus an instance artifact in the shape `issues/stage.py` writes. NOT a private
format: a diagnostic in a format nothing downstream reads is a diagnostic nobody acts on, which is the
same defect as a gate off the path. The type text is platform-NEUTRAL because the framework's text rule
refuses a type that asserts what a source platform does; the platform-specific fact lives on the
instance, where it is read off the document.

EXIT CODES — the driver's vocabulary, deliberately not widened
--------------------------------------------------------------
  0  every raised obligation discharged: every generated column accounted for, no divergence found
  3  OBLIGATIONS OUTSTANDING -- divergences, unverifiable columns or unanswered obligations. The list
     is handed over in the ledger and the sidecar. Degradation, not failure.
  1  the gate could not run (no emitted project, unreadable input, malformed verdict). NOT an
     obligation verdict. Disambiguated on stdout exactly as Gate A and coverage_gate are: a real
     verdict always contains a " ledger        :" line.
  2  usage
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import gate_a  # noqa: E402  the isolation, the citation checker and the loop record. Never re-written.

W = 96
_sha = gate_a._sha
_wrap = gate_a._wrap
read_lines = gate_a.read_lines


class GateBError(Exception):
    """Every could-not-run condition. Always exit 1, never an obligation verdict."""


# ---------------------------------------------------------------------------------------------
# STAGING THE EMITTED PROJECT.
#
# `findings/43` recorded the experiment defect that shaped this: "I staged only `models/`, so the
# verifiers never saw `dbt_project.yml` or `profiles.yml` -- which do exist in our trees." One finding
# was false as a result and the materialization question was unanswerable. So the whole emitted project
# is staged, and what is left out is DECLARED with a reason rather than omitted quietly.
# ---------------------------------------------------------------------------------------------

EXCLUDED_DIRS = [
    ("dbt_internal_packages", "dbt's own vendored adapter macros. Not generated from this document, "
                              "identical in every tree, and ~16 files that would swamp the 4 that are "
                              "ours"),
    ("target", "dbt compile output, i.e. a previous tool run's conclusion about these models rather "
               "than the models"),
    ("logs", "a previous run's log"),
    ("etl_configuration", "framework scaffolding emitted identically for every conversion; not "
                          "derived from this document"),
    # WITHHELD FROM THE VERIFIER, NOT WAIVED. These two stay out of the bundle because they are not
    # derived from the document and would swamp what is -- but "not derived from this document" was
    # read as "nothing here can be wrong", and an Alteryx run shipped four ssis_*.sql files through
    # this exclusion (runs/m1-ready-2026-08-19). Whether a framework file names the right platform is
    # now the integrity gate's SCAFFOLD class, which reads the tree this gate declines to stage.
    ("etl_instrumentation", "same: framework scaffolding, not derived from this document. Its "
                            "platform provenance is checked by integrity_gate.py's SCAFFOLD class"),
]

WITHHELD = [
    ("findings/, CONFIDENCE.yml, DESIGN.md, tickets/",
     "they contain the answers, and several name the exact divergence this gate is scored on"),
    ("the *.ai.json producer sidecar",
     "the producer's own account of what it authored and why. findings/43 withheld it on the "
     "principle that a model's claim about itself is not evidence -- and the strongest result in that "
     "test was Gate B finding a divergence the sidecar records, WITHOUT seeing the sidecar"),
    ("Gate A's bundle, obligations and verdicts",
     "a previous gate's conclusion is not evidence about the artifact"),
    ("MANIFEST.json — staged for SCORING and never handed to the verifier",
     "it carries absolute paths back to the repository, and the falsifiability probe: which model and "
     "column the disqualifying case is scored on. Telling the verifier where the test is would settle "
     "it by metadata"),
    ("the harness's own configuration: CLAUDE.md, auto-memory, skills, plugins, hooks, MCP servers",
     "disabled for the call. Not hygiene: the project's auto-memory and instruction files name "
     "findings a verifier is supposed to reach on its own"),
]

# THE PRE-REGISTERED DISQUALIFYING CASE, as a string rather than as an intention. Computed at pack time,
# recorded ONLY in MANIFEST.json (which the verifier never sees), and scored by `falsify`.
PROBE_EXPRESSION = "FirstName || ' ' || MiddleName || ' ' || LastName"

# One column per line is this emitter's format. `AS <ident>` at the end of a line, with the expression
# being everything before it. A model whose SELECT list is not in that shape raises no EX obligations
# and SAYS SO, rather than being silently reported as a model with no columns -- an empty denominator
# reported as clean is the defect this project keeps finding.
ALIAS = re.compile(r"^\s*(?P<expr>.+?)\s+AS\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*)\s*,?\s*$",
                   re.IGNORECASE)
REF = re.compile(r"\{\{\s*ref\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}")
SOURCE = re.compile(r"\{\{\s*source\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}")
# The engine's blocking placeholder marker, spelled in pieces so this file is not itself counted by the
# neighbouring stage that greps the tree for it.
BLOCKING = "!!!RESOLVE" + " EWI!!!"


def find_project(out_root):
    """The emitted dbt project inside an output tree. Returns (project_dir, [others]).

    Raises rather than guessing when there is none: an output root with no project is a
    could-not-run, and a gate that reports a missing artifact as a clean one is the failure mode this
    project has already measured four times.
    """
    hits = []
    for base, dirs, files in os.walk(out_root):
        if "dbt_project.yml" in files and os.path.isdir(os.path.join(base, "models")):
            hits.append(base)
        dirs[:] = [d for d in dirs if d not in ("target", "dbt_internal_packages", "logs")]
    if not hits:
        raise GateBError("no emitted dbt project under %s (looked for a dbt_project.yml beside a "
                         "models/ directory). Gate B has nothing to verify, which is UNMEASURED and "
                         "not clean." % out_root)
    hits.sort(key=len)
    return hits[0], hits[1:]


def stage_project(project, bundle):
    """Copy the emitted project into the bundle. Returns (staged relpaths, excluded [(what, why)])."""
    staged, excluded = [], []
    skip = {d for d, _ in EXCLUDED_DIRS}
    for base, dirs, files in os.walk(project):
        pruned = [d for d in dirs if d in skip]
        for d in pruned:
            excluded.append((os.path.relpath(os.path.join(base, d), project),
                             dict(EXCLUDED_DIRS)[d]))
        dirs[:] = [d for d in dirs if d not in skip]
        for f in sorted(files):
            src = os.path.join(base, f)
            rel = os.path.join("project", os.path.relpath(src, project))
            dst = os.path.join(bundle, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            staged.append(rel)
    return staged, excluded


def parse_model(text):
    """What this file states, read off the bytes. Returns a dict of deterministic facts."""
    lines = text.split("\n")
    cols = []
    for i, ln in enumerate(lines, start=1):
        if " AS " not in ln.upper():
            continue
        m = ALIAS.match(ln)
        if not m:
            continue
        expr = m.group("expr").strip()
        # `FROM {{ ref(...) }} AS alias` and `FROM {{ source(...) }} AS alias` are table aliases, not
        # output columns. Excluded on the expression's shape, and the exclusion is reported.
        if expr.startswith("{{") or expr.lower().startswith("source_data"):
            continue
        cols.append({"column": m.group("alias"), "expression": expr, "sql_line": i})
    return {
        "output_columns": cols,
        "refs": sorted(set(REF.findall(text))),
        "sources": sorted(set("%s.%s" % (a, b) for a, b in SOURCE.findall(text))),
        "lines": len(lines),
        "contains_blocking_placeholder": BLOCKING in text,
        "materialization_config_present": "{{ config(" in text,
    }


# ---------------------------------------------------------------------------------------------
# RAISING. The denominator is the emitted artifact, parsed. Not a count the verifier can move, and not
# a count our own identification sweep produced -- `findings/43` measured a ledger whose denominator was
# its own output reporting lost=0 on a document that had lost the stage holding every derivation.
# ---------------------------------------------------------------------------------------------

def raise_obligations(bundle, doc_path, project_rel_models):
    """Read the STAGED artifact back off disk and raise one obligation per generated column.

    Re-read from the bundle rather than from the output tree, so `score` recomputes exactly what the
    verifier was asked -- the raised set has to be reproducible from the bundle alone.
    """
    obligations, notes = [], []
    expression_id_counts = {}
    for rel in project_rel_models:
        path = os.path.join(bundle, rel)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        facts = parse_model(text)
        model = os.path.splitext(os.path.basename(rel))[0]
        obligations.append({
            "id": "MD:%s" % model,
            "family": "MODEL",
            "model": model,
            "sql_file": rel,
            "lines": facts["lines"],
            "refs": facts["refs"],
            "sources": facts["sources"],
            "output_columns": [c["column"] for c in facts["output_columns"]],
            "contains_blocking_placeholder": facts["contains_blocking_placeholder"],
            "materialization_config_present": facts["materialization_config_present"],
            "question": ("Taken as a whole: does this model produce the row set the source element it "
                         "was generated from states? Row shape, the relation it reads, whether its "
                         "refs resolve to a model in this project, and whether it is SQL at all."),
        })
        if not facts["output_columns"]:
            notes.append("%s names no output column under the `<expr> AS <alias>` rule, so it raises "
                         "no per-column obligation. Its MD: obligation still asks what it produces -- "
                         "an empty denominator reported as clean is the defect this project keeps "
                         "finding." % rel)
        for c in facts["output_columns"]:
            base_id = "EX:%s#%s" % (model, c["column"])
            occurrence = expression_id_counts.get(base_id, 0) + 1
            expression_id_counts[base_id] = occurrence
            obligation_id = base_id
            if occurrence > 1:
                # UNION branches legitimately project the same alias more than once. The alias-only
                # id made those obligations collide and caused batched Gate B to abort before any
                # verifier call. Keep the first id stable and disambiguate repeats by source line.
                obligation_id = "%s@L%s" % (base_id, c["sql_line"])
                if occurrence > 2:
                    obligation_id += ".%d" % occurrence
            obligations.append({
                "id": obligation_id,
                "family": "EXPRESSION",
                "model": model,
                "sql_file": rel,
                "output_column": c["column"],
                "generated_expression": c["expression"],
                "sql_line": c["sql_line"],
                "question": ("Find the source element and the expression in the document that this "
                             "generated column came from. State what the document's expression "
                             "computes and what this SQL computes. Are they the same for EVERY input? "
                             "If not, name an input on which they differ and say what each side "
                             "yields."),
            })
    obligations.append({
        "id": "TREE:dag",
        "family": "TREE",
        "models": [os.path.splitext(os.path.basename(r))[0] for r in project_rel_models],
        "question": ("The model set as a whole. Does a path exist from the relation the document's "
                     "source element reads to the model that writes its target? Does every ref() "
                     "resolve to a model present in this project? Is any model a placeholder rather "
                     "than SQL? A per-model verdict on a disconnected tree reads as though the tree "
                     "were complete, which is how a previous run reported 3 models and 0 edges as "
                     "though it had a pipeline."),
    })
    counts = {}
    for o in obligations:
        counts[o["family"]] = counts.get(o["family"], 0) + 1
    for fam in ("EXPRESSION", "MODEL", "TREE"):
        counts.setdefault(fam, 0)
    return {"obligations": obligations, "counts": counts, "notes": notes,
            "document": os.path.basename(doc_path)}


PROMPT = """# Gate B — does the generated SQL do what the source element says?

You are a verification agent. Everything you may rely on is in THIS DIRECTORY. Do not open any file
outside it, do not search a wider repository, and do not look for a previous conclusion about this
migration — there is none in here on purpose.

## What you are given

| file | what it is |
|---|---|
| `source_document.*` | the source ETL document, verbatim |
| `source_document.lines.txt` | the same bytes with `NNNNN: ` line numbers. THIS is the citation vocabulary for the document |
| `project/**` | the EMITTED dbt project, whole: `dbt_project.yml`, `profiles.yml`, every model, macros, any `sources.yml` |
| `obligations.json` | the obligations raised from the emitted SQL. Your job is to answer every one |
| `DIALECT_REFERENCE.md` | dialect semantics, each item marked [PRIMARY] / [COMMON] / [UNCONFIRMED]. **May be absent** — if it is, see `basis` below |

## The question, per obligation

**EXPRESSION** — one per generated output column. Find the expression in the *document* that this
column came from. State what that expression computes and what the SQL computes. Then:

- **`EQUIVALENT`** — the two produce the same value for every input. Say why, concretely.
- **`DIVERGENT`** — there is an input on which they differ. You must name that input and say what each
  side yields for it. A divergence with no failing input is prose, and it is quarantined as prose.
- **`UNVERIFIABLE`** — you cannot establish either. Honest, and it discharges nothing.

**MODEL** — the model as a whole: row shape, the relation it reads, whether its `ref()`s resolve within
this project, whether it is SQL at all. `EQUIVALENT` / `DIVERGENT` / `UNVERIFIABLE`.
**A model whose column is DIVERGENT is itself DIVERGENT.** A roll-up that reads clean over a divergent
column is rejected — an earlier verifier's finding lived only in prose under a clean verdict, and a
scorer counting verdict words read that bundle as clean.

**TREE** — the model set. `INTACT` / `BROKEN` / `UNVERIFIABLE`.

## The answer format — write exactly this JSON to `verdict.json` in this directory

```json
{
  "verifier": "a short id for yourself",
  "claims": [
    {
      "obligation_id": "EX:int_der_add_fullname_birthyear#FullName",
      "verdict": "DIVERGENT",
      "basis": "SHEET_PRIMARY",
      "source_locus": 279,
      "source_quote": "FirstName + \\" \\" + MiddleName",
      "sql_quote": "FirstName || ' ' || MiddleName",
      "sheet_quote": "does not propagate NULL",
      "source_says": "what the document's expression computes",
      "sql_says": "what the generated SQL computes",
      "failing_input": "FirstName='John', MiddleName=NULL, LastName='Smith'",
      "differs_as": "source yields 'John  Smith'; the SQL yields NULL",
      "reason": "one or two sentences, concrete"
    }
  ],
  "notes": ["free prose, never scored"]
}
```

Vocabulary, and nothing outside it:

- EXPRESSION / MODEL: `EQUIVALENT`, `DIVERGENT`, `UNVERIFIABLE`
- TREE: `INTACT`, `BROKEN`, `UNVERIFIABLE`
- `basis`: `SHEET_PRIMARY`, `SHEET_COMMON`, `DOCUMENT`, `SQL`, `PRIOR`

## How you will be scored, so there are no surprises

1. **Every obligation in `obligations.json` must appear in `claims`.** An unanswered obligation is
   scored OUTSTANDING. Silence is not a safe default in either direction.
2. **Citations are re-read.** `source_quote` must be a substring of line `source_locus` of
   `source_document.lines.txt`; `sql_quote` must be a substring of the model file the obligation names;
   `sheet_quote` must be a substring of `DIALECT_REFERENCE.md`. A quote that is not there QUARANTINES
   the claim: it discharges nothing and raises nothing. Quote short exact fragments.
3. **`basis: PRIOR` is quarantined by construction.** If you know a dialect rule that the reference
   sheet does not state — or the sheet is not in this directory at all — you may still say it: declare
   `PRIOR` and it is printed as an unsourced remark rather than counted. This is deliberate and it is
   not a trick. A previous test measured that a verifier working from memory caught the same defects as
   one given primary sources and was *right unearnedly*; a verifier that cannot show its source cannot
   be trusted on the next document. Being visibly unsourced is the point.
4. **`DIVERGENT` needs `failing_input` and `differs_as`.** A concrete input on which the two differ.
5. **A `DIVERGENT` column forces its model to `DIVERGENT`.** Consistency is checked.
6. There is **no score**. The verdict is obligations discharged versus outstanding. Finding nothing
   does not make it pass and flagging everything does not make it thorough: a false alarm on correct
   output teaches a reviewer to ignore the gate, which is worse than silence because that channel is
   how real risk gets reported.

## Two things that are not evidence, and one reporting rule

**A model's header is not evidence about the model.** If a generated file states its own status —
"AUTHORED", "RUNNABLE", "VERIFIED", a reason, a provenance line — that is a claim by whatever wrote it,
about itself. A previous verifier was right to point out that a header reading `RUNNABLE, NOT VERIFIED`
sat above SQL that could not compile. Judge the SQL.

**A comment naming a platform is not evidence about the platform.** A placeholder marker may name the
wrong source system entirely; that is a fact about the emitter, and worth reporting as one.

**When two hypotheses fit the evidence in this directory and nothing in here can separate them, say so
and name both.** Do not pick the more alarming one. A previous verifier reported three facts as
declared-but-never-raised when its bundle simply predated them, and said afterwards: *"the correct
phrasing was 'either the obligation set does not raise these or this bundle predates them, and I cannot
tell which from here.'"* That is the difference between a finding and a false alarm.

Read the document and the SQL before anything else. They are the only two things in here that are
evidence; everything else is a claim about them.
"""

DEFAULT_REFERENCE = os.path.abspath(os.path.join(HERE, "..", "..", "blind-run", "gateB",
                                                 "DIALECT_REFERENCE.md"))

# Substance lives in PROMPT.md, inside the bundle, where it is auditable. This says where to read and
# where to write, and nothing about how to reason -- the same rule Gate A's wrapper follows, and for the
# same measured reason.
CLI_PROMPT = """You are Gate B's verification agent. Your entire evidence base is THIS DIRECTORY.

1. Read `PROMPT.md` here. It states the question, the answer vocabulary and how you are scored. Follow
   it exactly.
2. Read `obligations.json`. Answer EVERY obligation in it. An obligation you do not answer is scored
   OUTSTANDING, so silence is not a safe default in either direction.
3. Write your answer as JSON to `./verdict.json` in this directory, in the schema `PROMPT.md` gives.
   That file is your only output: anything you print instead of writing it is discarded.

Hard constraints: read no file outside this directory — attempts are refused by the harness, and a
refused read is evidence about the harness and not about the artifact. Do not reason about a wider
repository; there is none reachable. Every citation you give is re-read by the scorer.
"""


def pack(args):
    doc = os.path.abspath(args.doc)
    out_root = os.path.abspath(args.out_root)
    if not os.path.isfile(doc):
        raise GateBError("source document unreadable: %s" % doc)
    if not os.path.isdir(out_root):
        raise GateBError("no output tree at %s. Gate B has nothing to verify, which is UNMEASURED "
                         "and not clean." % out_root)
    doc_sha_at_start = _sha(doc)
    project, others = find_project(out_root)

    bundle = os.path.abspath(args.bundle)
    prev_project_sha = None
    prev_sidecars = None
    _prev_m = os.path.join(bundle, "MANIFEST.json")
    if os.path.isfile(_prev_m):
        try:
            with open(_prev_m, "r", encoding="utf-8") as fh:
                _prev = json.load(fh)
            prev_project_sha = (_prev.get("inputs") or {}).get("project_sha256")
            prev_sidecars = ((_prev.get("freshness") or {}).get("sidecars") or {}).get("sidecars")
        except Exception:
            prev_project_sha = None
            prev_sidecars = None
    # A PREVIOUS ANSWER IN THE BUNDLE IS A LEAK, and the worst kind: a verifier that reads last round's
    # verdict is not verifying, it is agreeing.
    cleared = []
    for stale in ("verdict.json", "gateB-sidecar.json", "gateB-loop.json", "verifier-run.json"):
        sp = os.path.join(bundle, stale)
        if os.path.isfile(sp):
            os.remove(sp)
            cleared.append(stale)
    if os.path.isdir(os.path.join(bundle, "project")):
        shutil.rmtree(os.path.join(bundle, "project"))
    os.makedirs(bundle, exist_ok=True)

    staged_project, excluded = stage_project(project, bundle)
    ext = os.path.splitext(doc)[1] or ".txt"
    shutil.copyfile(doc, os.path.join(bundle, "source_document" + ext))
    lines = read_lines(doc)
    with open(os.path.join(bundle, "source_document.lines.txt"), "w", encoding="utf-8") as fh:
        for i, ln in enumerate(lines, start=1):
            fh.write("%5d: %s\n" % (i, ln))

    # THE ARM. `findings/43` TEST 6 measured that the sheet buys calibration, not detection, so both
    # arms stay runnable and the difference stays measurable rather than assumed.
    ref = os.path.abspath(args.reference or DEFAULT_REFERENCE)
    ref_staged = None
    if args.arm == "sourced":
        if not os.path.isfile(ref):
            raise GateBError("--arm sourced needs a reference sheet; %s is not there. Running the "
                             "sourced arm without one would silently BE the naive arm." % ref)
        shutil.copyfile(ref, os.path.join(bundle, "DIALECT_REFERENCE.md"))
        ref_staged = "DIALECT_REFERENCE.md"

    models = [r for r in staged_project
              if r.startswith(os.path.join("project", "models")) and r.endswith(".sql")]
    models.sort()
    if not models:
        raise GateBError("the emitted project at %s contains no model .sql files" % project)
    raised = raise_obligations(bundle, doc, models)

    # ---- FRESHNESS, same two questions Gate A asks and for the same measured reason ---------------
    doc_sha = _sha(doc)
    project_sha = _sha_tree(project)
    newest_model = max(os.path.getmtime(os.path.join(bundle, m)) for m in models)
    doc_mtime = os.path.getmtime(doc)
    freshness = {
        "document_is_current": doc_sha == doc_sha_at_start,
        "project_changed_since_previous_pack": (None if prev_project_sha is None
                                                else prev_project_sha != project_sha),
        "previous_pack_project_sha256": (prev_project_sha or "")[:16] or None,
        "emitted_project_is_newer_than_document": newest_model >= doc_mtime,
        "_how": ("`document_is_current` diffs the source document at the start of packing against the "
                 "same file after staging; FALSE means it moved underneath this bundle. "
                 "`project_changed_since_previous_pack` compares the emitted tree's content hash "
                 "against the hash THIS bundle recorded last time, and is null when there was no "
                 "previous pack -- a bundle is a snapshot, and the same directory re-packed after the "
                 "emitter changed is a different experiment. "
                 "`emitted_project_is_newer_than_document` says whether the SQL in here was generated "
                 "at or after the document's last change; when it is FALSE the models may not "
                 "correspond to the document at all, and a divergence you find could be an artefact "
                 "of that rather than of the lowering. Report both hypotheses, do not pick the "
                 "alarming one. LIMITATION: mtime is the only ordering evidence these artifacts "
                 "carry, and copying a file resets it, so this can read `true` for output generated "
                 "from an older document. It can miss staleness; when it fires, it is right."),
    }
    # THE SIDECAR HALF, shared with Gate A rather than reimplemented. It matters MORE here than there:
    # Gate A reads the IR, Gate B reads the EMITTED SQL, and a model-authored `<doc>.ai*.json` is
    # exactly what decides that SQL's content. A tree emitted before the current sidecar is a tree
    # whose divergences may already have been fixed. The comparison is against the newest staged model
    # rather than the document, for the same reason.
    freshness["sidecars"] = gate_a.sidecar_freshness(doc, os.path.join(bundle, models[-1]),
                                                     "emitted_project", prev=prev_sidecars)
    # `newest_model` is the real ordering evidence, not the last model alphabetically. Recomputed here
    # so the shared helper stays a pure function of two paths.
    for _r in freshness["sidecars"]["sidecars"]:
        _m = os.path.join(os.path.dirname(doc), _r["file"])
        _cur = newest_model >= os.path.getmtime(_m) if os.path.exists(_m) else None
        _r["emitted_project_is_current_with_it"] = _cur
    freshness["sidecars"]["stale_against_emitted_project"] = sorted(
        r["file"] for r in freshness["sidecars"]["sidecars"]
        if r["emitted_project_is_current_with_it"] is False)
    freshness["sidecars"]["emitted_project_is_current_with_sidecars"] = (
        None if not freshness["sidecars"]["sidecars"]
        else not freshness["sidecars"]["stale_against_emitted_project"])

    raised_out = dict(raised)
    raised_out["bundle_freshness"] = freshness
    with open(os.path.join(bundle, "obligations.json"), "w", encoding="utf-8") as fh:
        json.dump(raised_out, fh, indent=1)
    with open(os.path.join(bundle, "PROMPT.md"), "w", encoding="utf-8") as fh:
        fh.write(PROMPT)

    # THE PRE-REGISTERED PROBE, recorded here and NOWHERE the verifier can read. It is computed from
    # the artifact rather than named by hand, so it cannot quietly drift onto a different column.
    probe = None
    for o in raised["obligations"]:
        if o["family"] == "EXPRESSION" and PROBE_EXPRESSION in o.get("generated_expression", ""):
            probe = {"obligation_id": o["id"], "expression": o["generated_expression"],
                     "sql_file": o["sql_file"], "output_column": o["output_column"],
                     "_why": ("findings/42 TEST 1, the disqualifying case. This exact string is "
                              "emitted for two different source platforms and is correct for one of "
                              "them. Recorded in the manifest only: the verifier never sees which "
                              "column the test is on, because telling it would settle the experiment "
                              "by metadata.")}
            break

    produced = ["source_document" + ext, "source_document.lines.txt", "obligations.json", "PROMPT.md"]
    if ref_staged:
        produced.append(ref_staged)
    produced += staged_project
    manifest = {
        "gate": "B",
        "arm": args.arm,
        "freshness": freshness,
        "packed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform_hint": args.platform or "(not supplied; the verifier is not told)",
        "raised": raised["counts"],
        "raising_notes": raised["notes"],
        "withheld": [{"what": w, "why": y} for w, y in WITHHELD],
        "excluded_from_the_staged_project": [{"what": w, "why": y} for w, y in excluded],
        "other_projects_in_this_tree": others,
        "falsifiability_probe": probe,
        # PRIVATE TO SCORING. Absolute paths live here and this file is never staged for the verifier.
        "inputs": {
            "document": doc, "document_sha256": doc_sha,
            "output_root": out_root, "project": project, "project_sha256": project_sha,
            "reference_sheet": ref if ref_staged else None,
            "reference_sha256": _sha(ref) if ref_staged else None,
        },
        "files": [],
    }
    for f in produced:
        fp = os.path.join(bundle, f)
        if os.path.isfile(fp):
            manifest["files"].append({"file": f, "bytes": os.path.getsize(fp),
                                      "sha256": _sha(fp)[:16]})
        else:
            manifest["files"].append({"file": f, "MISSING": True})
    known = set(produced) | {"MANIFEST.json"}
    strays = []
    for base, dirs, files in os.walk(bundle):
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), bundle)
            if rel not in known:
                strays.append(rel)
    manifest["unexpected_files"] = sorted(strays)
    with open(os.path.join(bundle, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)

    print("=" * W)
    print(" GATE B — intent-parity bundle packed")
    print("=" * W)
    print(" bundle        : %s" % bundle)
    print(" document      : %s" % doc)
    print(" project       : %s" % project)
    print(" arm           : %s%s" % (args.arm,
                                     "" if ref_staged else "  (no reference sheet staged: a dialect "
                                                           "rule can only be declared PRIOR, and "
                                                           "PRIOR discharges nothing)"))
    print(" raised        : %d obligation(s)  EXPRESSION=%d MODEL=%d TREE=%d"
          % (sum(raised["counts"].values()), raised["counts"]["EXPRESSION"],
             raised["counts"]["MODEL"], raised["counts"]["TREE"]))
    print(" staged        : %d project file(s); excluded %d directory class(es): %s"
          % (len(staged_project), len(excluded), ", ".join(sorted({w for w, _ in excluded})) or "none"))
    print(" freshness     : emitted_project_is_newer_than_document=%s  document_is_current=%s"
          % (freshness["emitted_project_is_newer_than_document"], freshness["document_is_current"]))
    if not freshness["emitted_project_is_newer_than_document"]:
        print("                 *** THE EMITTED SQL PREDATES THE DOCUMENT. A divergence found here may")
        print("                 be an artefact of that rather than of the lowering. Re-emit first.")
    if freshness["project_changed_since_previous_pack"]:
        print("                 *** THE EMITTED PROJECT CHANGED SINCE THIS BUNDLE WAS LAST PACKED.")
        print("                 A bundle is a snapshot; the previous answer has been cleared.")
    _sc = freshness["sidecars"]
    print("                 sidecars=%d  emitted_project_is_current_with_sidecars=%s"
          % (len(_sc["sidecars"]), _sc["emitted_project_is_current_with_sidecars"]))
    for _r in _sc["sidecars"]:
        print("                   %s  %s  %s" % (_r["sha256"], _r["mtime_utc"], _r["file"]))
    if _sc["stale_against_emitted_project"]:
        print("                 *** THE EMITTED SQL PREDATES A MODEL-AUTHORED SIDECAR: %s."
              % ", ".join(_sc["stale_against_emitted_project"]))
        print("                 The sidecar decides the lowered SQL, so a divergence found in this")
        print("                 bundle may already be fixed in the tree the current sidecar produces.")
        print("                 Re-emit, then re-pack. Reported and not fatal because the direction is")
        print("                 a FALSE ALARM rather than a hidden defect.")
    if _sc["sidecars_changed_since_previous_pack"]:
        print("                 *** A SIDECAR CHANGED SINCE THIS BUNDLE WAS LAST PACKED: %s."
              % ", ".join(_sc["sidecars_changed_since_previous_pack"]))
    if cleared:
        print(" cleared       : %s — a previous answer in the bundle is a leak, not context"
              % ", ".join(cleared))
    for n in raised["notes"]:
        print("-" * W)
        for chunk in _wrap(n, W - 2):
            print(" %s" % chunk)
    print("-" * W)
    print(" next          : gate_b.py verifier --bundle %s --verdict %s"
          % (bundle, os.path.join(bundle, "verdict.json")))
    return 0


def _sha_tree(root):
    """One content hash over an emitted project: relative path + bytes, in sorted order."""
    import hashlib
    h = hashlib.sha256()
    for base, dirs, files in sorted(os.walk(root)):
        dirs[:] = sorted(d for d in dirs if d not in {d0 for d0, _ in EXCLUDED_DIRS})
        for f in sorted(files):
            p = os.path.join(base, f)
            h.update(os.path.relpath(p, root).encode("utf-8"))
            h.update(_sha(p).encode("ascii"))
    return h.hexdigest()


def verifier(args):
    """One implementation of --verifier-cmd, using Gate A's isolation unchanged."""
    gate_a.isolated_model_call(
        "B", args.bundle, args.verdict, CLI_PROMPT, cli=args.cli, model=args.model,
        timeout=args.verifier_timeout, view=args.view, view_root=args.view_root,
        keep_view=args.keep_view, max_budget_usd=args.max_budget_usd,
        extra_exclude=("gateB-sidecar.json", "gateB-loop.json"),
        what="the verifier half of Gate B, as a real model call")
    return 0


# ---------------------------------------------------------------------------------------------
# DEFAULT BATCHING + BOUNDED PARALLELISM
# LoadDim proved that a whole gate is not a viable unit: 861 obligations timed out at 1800 seconds.
# Defaults: EXPRESSION=8, MODEL=12, TREE=1, with four concurrent isolated calls.
# ---------------------------------------------------------------------------------------------
GATE_B_FAMILIES = ("EXPRESSION", "MODEL", "TREE")


def plan_batches(obligations, expression_batch_size=8, model_batch_size=12):
    grouped = {fam: [] for fam in GATE_B_FAMILIES}
    unknown = []
    for obligation in obligations:
        fam = obligation.get("family")
        if fam in grouped:
            grouped[fam].append(obligation)
        else:
            unknown.append("%s(%s)" % (obligation.get("id"), fam))
    if unknown:
        raise GateBError("BATCH PLAN SAW UNKNOWN FAMILY ON: %s" % unknown)
    sizes = {"EXPRESSION": max(1, expression_batch_size),
             "MODEL": max(1, model_batch_size), "TREE": 1}
    batches = []
    for fam in GATE_B_FAMILIES:
        items, size = grouped[fam], sizes[fam]
        for start in range(0, len(items), size):
            chunk = items[start:start + size]
            batches.append({"index": len(batches), "family": fam, "chunk": start // size,
                            "obligation_ids": [o["id"] for o in chunk], "obligations": chunk})
    wanted = [o["id"] for fam in GATE_B_FAMILIES for o in grouped[fam]]
    got = [oid for batch in batches for oid in batch["obligation_ids"]]
    if got != wanted or len(got) != len(set(got)):
        raise GateBError("BATCH PLAN DOES NOT COVER THE RAISED SET EXACTLY ONCE EACH")
    return batches


def _batch_payload(packed, batch):
    payload = dict(packed)
    payload["obligations"] = batch["obligations"]
    payload["counts"] = {fam: sum(o["family"] == fam for o in batch["obligations"])
                         for fam in GATE_B_FAMILIES}
    payload["batch"] = {"index": batch["index"], "family": batch["family"],
                        "chunk": batch["chunk"],
                        "obligations_in_this_batch": len(batch["obligation_ids"]),
                        "obligations_in_full_raised_set": len(packed.get("obligations") or []),
                        "_note": "Answer every obligation in this batch and nothing outside it."}
    return payload


def _run_one_batch(bundle, batch, packed, args):
    verdict_path = os.path.join(bundle, "verdict.batch%d.json" % batch["index"])
    view = os.path.join(args.view_root or tempfile.gettempdir(),
                        "gateB-batch%d-view-%s-%d" %
                        (batch["index"], os.path.basename(bundle.rstrip(os.sep)), os.getpid()))
    try:
        record = gate_a.isolated_model_call(
            "B", bundle, verdict_path, CLI_PROMPT, cli=args.cli, model=args.model,
            timeout=args.verifier_timeout, view=view, view_root=args.view_root,
            keep_view=args.keep_view, max_budget_usd=args.max_budget_usd,
            extra_exclude=("gateB-sidecar.json", "gateB-loop.json"),
            record_name="verifier-run.batch%d.json" % batch["index"],
            what="Gate B batch %d (family=%s chunk=%d, %d obligation(s))" %
                 (batch["index"], batch["family"], batch["chunk"], len(batch["obligation_ids"])),
            obligations_override=_batch_payload(packed, batch))
    except gate_a.GateAError as ex:
        return {"batch": batch, "verdict": None, "error": str(ex), "run_record": None}
    try:
        with open(verdict_path, "r", encoding="utf-8") as fh:
            verdict = json.load(fh)
    except Exception as ex:
        return {"batch": batch, "verdict": None,
                "error": "verdict fragment unreadable: %s: %s" % (type(ex).__name__, ex),
                "run_record": record}
    return {"batch": batch, "verdict": verdict, "error": None, "run_record": record}


def merge_batch_fragments(packed, batches, fragments):
    if len(batches) != len(fragments):
        raise GateBError("BATCH MERGE FRAGMENT COUNT MISMATCH")
    claims, report, verifier_ids = [], [], []
    ok = failed = 0
    for fragment in fragments:
        batch, error = fragment["batch"], fragment["error"]
        rows = None
        if error is None:
            rows = (fragment["verdict"] or {}).get("claims")
            if not isinstance(rows, list):
                error = "batch %d verdict has no claims array" % batch["index"]
        if error:
            failed += 1
            report.append({"index": batch["index"], "family": batch["family"],
                           "chunk": batch["chunk"], "obligation_ids": batch["obligation_ids"],
                           "status": "BATCH_FAILED", "error": error})
            continue
        ok += 1
        owned, kept, dropped = set(batch["obligation_ids"]), 0, []
        for claim in rows:
            oid = claim.get("obligation_id")
            if oid not in owned:
                dropped.append(oid)
            else:
                claims.append(dict(claim, _batch_index=batch["index"],
                                   _batch_family=batch["family"]))
                kept += 1
        verifier = (fragment["verdict"] or {}).get("verifier")
        if verifier:
            verifier_ids.append(str(verifier))
        rr = fragment.get("run_record") or {}
        row = {"index": batch["index"], "family": batch["family"],
               "chunk": batch["chunk"], "obligation_ids": batch["obligation_ids"],
               "status": "ANSWERED", "claims_written": kept, "verifier": verifier,
               "elapsed_s": rr.get("elapsed_s"), "cost_usd": rr.get("total_cost_usd"),
               "input_tokens": rr.get("input_tokens"), "output_tokens": rr.get("output_tokens"),
               "cache_read_input_tokens": rr.get("cache_read_input_tokens"),
               "cache_creation_input_tokens": rr.get("cache_creation_input_tokens")}
        if dropped:
            row["claims_dropped_out_of_batch"] = dropped
        report.append(row)
    merged = {"verifier": ("BATCHED[" + ",".join(verifier_ids) + "]") if verifier_ids
                           else "BATCHED[no successful batch]",
              "claims": claims,
              "notes": ["merged from %d bounded batch(es): %d answered, %d failed" %
                        (len(batches), ok, failed)]}
    audit = {"gate": "B", "batches": report, "batches_ok": ok,
             "batches_failed": failed, "raised_total": len(packed.get("obligations") or []),
             "merge_rule": "Only in-batch claims are retained; failed batches contribute no claims "
                           "and remain OUTSTANDING during score()."}
    return merged, audit


def batched_run(args):
    """Pack Gate B once, verify bounded chunks concurrently, merge in index order, and score."""
    rc = pack(args)
    if rc:
        return rc
    bundle = os.path.abspath(args.bundle)
    with open(os.path.join(bundle, "obligations.json"), "r", encoding="utf-8") as fh:
        packed = json.load(fh)
    batches = plan_batches(packed.get("obligations") or [], args.expression_batch_size,
                           args.model_batch_size)
    parallelism = max(1, int(args.parallelism or 4))
    print("#" * W)
    print(" GATE B -- DEFAULT BATCHED + PARALLEL VERIFIER CALLS")
    print("#" * W)
    print(" obligations   : %d across %d batch(es)" %
          (len(packed.get("obligations") or []), len(batches)))
    print(" batch sizes   : EXPRESSION=%d MODEL=%d TREE=1" %
          (args.expression_batch_size, args.model_batch_size))
    print(" parallelism   : %d worker(s)" % parallelism)
    fragments_by_index = {}
    with ThreadPoolExecutor(max_workers=parallelism, thread_name_prefix="gateB") as pool:
        future_to_batch = {pool.submit(_run_one_batch, bundle, batch, packed, args): batch
                           for batch in batches}
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                fragment = future.result()
            except Exception as ex:
                fragment = {"batch": batch, "verdict": None,
                            "error": "parallel worker raised %s: %s" %
                                     (type(ex).__name__, ex), "run_record": None}
            fragments_by_index[batch["index"]] = fragment
            print(" batch %d/%d  family=%s  n=%d -- %s" %
                  (batch["index"] + 1, len(batches), batch["family"],
                   len(batch["obligation_ids"]),
                   ("FAILED: %s" % fragment["error"]) if fragment["error"] else "answered"))
    fragments = [fragments_by_index[batch["index"]] for batch in batches]
    merged, audit = merge_batch_fragments(packed, batches, fragments)
    audit_path = os.path.join(bundle, "gateB-batch-merge.json")
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
        raise GateBError(
            "all %d batch(es) failed -- no verifier verdict was produced for any obligation; see %s"
            % (len(batches), audit_path))

    verdict_path = os.path.join(bundle, "verdict.json")
    with open(verdict_path, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=1)
    print(" merge record  : %s" % audit_path)
    args.verdict = verdict_path
    return score(args)


# ---------------------------------------------------------------------------------------------
# SCORE. Every mechanism here exists because of something measured, not because it seemed prudent.
# ---------------------------------------------------------------------------------------------

EXPR_MODEL_VERDICTS = {"EQUIVALENT", "DIVERGENT", "UNVERIFIABLE"}
TREE_VERDICTS = {"INTACT", "BROKEN", "UNVERIFIABLE"}
ALLOWED = {"EXPRESSION": EXPR_MODEL_VERDICTS, "MODEL": EXPR_MODEL_VERDICTS, "TREE": TREE_VERDICTS}
DISCHARGING = {"EQUIVALENT", "INTACT"}
BASES = {"SHEET_PRIMARY", "SHEET_COMMON", "DOCUMENT", "SQL", "PRIOR"}
SHEET_BASES = {"SHEET_PRIMARY", "SHEET_COMMON"}

LLM_FIELD_MAX_LEN = 2000


def sanitize_llm_field(v, max_len=LLM_FIELD_MAX_LEN):
    """`verdict.json` is model output read off a document/SQL file that may itself be adversarial
    (prompt injection). This is the one place free-text verifier fields enter `rows`, which is the
    sole source for the console report, `gateB-sidecar.json`, and `issues.csv` -- so stripping
    control/ANSI bytes here (log-line forgery) and a leading `=+-@` (spreadsheet formula injection)
    here covers all three sinks without re-sanitizing at each one."""
    if not isinstance(v, str):
        return v
    cleaned = "".join(ch for ch in v if ch > "\x1f" and ch != "\x7f")[:max_len]
    if cleaned and cleaned[0] in "=+-@":
        cleaned = "'" + cleaned
    return cleaned


def _quote_in_file(path, quote):
    if not quote:
        return False, "no quote given"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            body = fh.read()
    except Exception as ex:
        return False, "%s unreadable: %s" % (os.path.basename(path), ex)
    if quote.strip() in body:
        return True, os.path.basename(path)
    # ONE tolerance, and only one: whitespace runs collapsed. A verifier re-typing an indented SQL
    # fragment will differ in spaces; a verifier inventing one will not match either way.
    if " ".join(quote.split()) in " ".join(body.split()):
        return True, "%s (whitespace-normalised)" % os.path.basename(path)
    return False, "%r is not in %s" % (quote[:60], os.path.basename(path))


def score(args):
    bundle = os.path.abspath(args.bundle)
    mpath = os.path.join(bundle, "MANIFEST.json")
    if not os.path.isfile(mpath):
        raise GateBError("no MANIFEST.json in %s — pack the bundle first" % bundle)
    with open(mpath, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    inp = manifest["inputs"]

    # Currency as booleans, never silently true. Same reasoning as Gate A: a bundle can be scored days
    # after it was built, by which time the packer's answer is about a state that no longer exists.
    currency = {}
    drift = []
    for label, path, want in (("document", inp["document"], inp.get("document_sha256")),
                              ("emitted_project", inp["project"], inp.get("project_sha256"))):
        if not want or not os.path.exists(path):
            currency[label + "_is_current"] = None
            continue
        now = _sha(path) if os.path.isfile(path) else _sha_tree(path)
        currency[label + "_is_current"] = now == want
        if now != want:
            drift.append("%s changed since the bundle was packed" % label)

    models = [f["file"] for f in manifest["files"]
              if f["file"].startswith(os.path.join("project", "models"))
              and f["file"].endswith(".sql")]
    # RECOMPUTED from the staged artifact, not read back from obligations.json: a loop must not be able
    # to shrink its own denominator by editing the file it is judged against.
    raised = raise_obligations(bundle, inp["document"], sorted(models))
    by_id = {o["id"]: o for o in raised["obligations"]}
    lines = read_lines(inp["document"])
    sheet = os.path.join(bundle, "DIALECT_REFERENCE.md")
    have_sheet = os.path.isfile(sheet)

    try:
        with open(args.verdict, "r", encoding="utf-8") as fh:
            verdict = json.load(fh)
    except Exception as ex:
        raise GateBError("verifier answer unreadable: %s: %s" % (type(ex).__name__, ex))
    claims = verdict.get("claims")
    if not isinstance(claims, list):
        raise GateBError("verifier answer has no `claims` array")

    rows, rejected, quarantined, unsourced = {}, [], [], []
    for c in claims:
        oid = c.get("obligation_id")
        o = by_id.get(oid)
        if o is None:
            rejected.append((oid, "no such obligation was raised from this artifact"))
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
        note = []
        if basis == "PRIOR":
            # QUARANTINED BY CONSTRUCTION, and this is THE measured mechanism of this gate.
            # findings/43: the naive arm caught the concat case from memory and was right unearnedly.
            # Printed so that being right-without-a-source is visible; never counted.
            unsourced.append((oid, v, sanitize_llm_field((c.get("reason") or "")[:400])))
            quarantined.append((oid, "basis PRIOR: a dialect or format rule asserted from the "
                                     "verifier's own knowledge rather than from the bundle. Printed, "
                                     "never counted."))
            continue
        if basis in SHEET_BASES:
            if not have_sheet:
                unsourced.append((oid, v, "claimed %s in an arm with no reference sheet staged"
                                  % basis))
                quarantined.append((oid, "basis %s but no DIALECT_REFERENCE.md is in this bundle: the "
                                         "claim rests on memory and is a PRIOR by another name"
                                    % basis))
                continue
            ok, detail = _quote_in_file(sheet, c.get("sheet_quote"))
            if not ok:
                quarantined.append((oid, "basis %s and the sheet_quote does not resolve: %s"
                                    % (basis, detail)))
                continue
            note.append("sheet_quote resolved in %s" % detail)

        # THE DOCUMENT CITATION. Required for every verdict, including EQUIVALENT: "these are the same"
        # with no statement of what the document says is not an answer to what the source element does.
        cit_ok, cit_detail = gate_a.verify_citation(lines, {"doc_locus": c.get("source_locus"),
                                                           "doc_quote": c.get("source_quote")})
        if not cit_ok:
            quarantined.append((oid, "source citation failed: %s" % cit_detail))
            continue

        # THE SQL CITATION, re-read in the model file the obligation names.
        if fam in ("EXPRESSION", "MODEL"):
            ok, detail = _quote_in_file(os.path.join(bundle, o["sql_file"]), c.get("sql_quote"))
            if not ok:
                quarantined.append((oid, "sql_quote does not resolve: %s" % detail))
                continue
            note.append("sql_quote resolved in %s" % detail)

        if v in ("DIVERGENT", "BROKEN"):
            if not (c.get("failing_input") or "").strip() and v == "DIVERGENT":
                quarantined.append((oid, "DIVERGENT with no `failing_input`: findings/42 defines a "
                                         "divergence as requiring a concrete input on which the two "
                                         "differ. Without one it is prose."))
                continue
            if not (c.get("differs_as") or "").strip():
                quarantined.append((oid, "%s with no `differs_as`: what each side yields is the whole "
                                         "claim" % v))
                continue

        prev = rows.get(oid)
        if prev is not None:
            quarantined.append((oid, "second answer to an obligation already answered %r; ignored"
                                % prev["verdict"]))
            continue
        rows[oid] = {
            "obligation_id": oid, "family": fam, "verdict": v, "basis": basis,
            "model": o.get("model"), "output_column": o.get("output_column"),
            "sql_file": o.get("sql_file"), "generated_expression": o.get("generated_expression"),
            "source_locus": sanitize_llm_field(c.get("source_locus")),
            "source_quote": sanitize_llm_field(c.get("source_quote")),
            "sql_quote": sanitize_llm_field(c.get("sql_quote")),
            "sheet_quote": sanitize_llm_field(c.get("sheet_quote")),
            "citation": cit_detail,
            "source_says": sanitize_llm_field((c.get("source_says") or "").strip()),
            "sql_says": sanitize_llm_field((c.get("sql_says") or "").strip()),
            "failing_input": sanitize_llm_field((c.get("failing_input") or "").strip()),
            "differs_as": sanitize_llm_field((c.get("differs_as") or "").strip()),
            "reason": sanitize_llm_field((c.get("reason") or "").strip()),
            "notes": note,
        }

    # ---- THE ROLL-UP CONSISTENCY CHECK ----------------------------------------------------------
    # MEASURED, one level up: a verifier found a real defect, answered with the clean word because it
    # was literally true, and left the finding in prose -- where a scorer counting verdict words reads
    # the bundle as clean. A model cannot be EQUIVALENT over a column that is DIVERGENT.
    inconsistent = []
    for oid, r in sorted(rows.items()):
        if r["family"] != "MODEL":
            continue
        div = [c for c, cr in rows.items()
               if cr["family"] == "EXPRESSION" and cr["model"] == r["model"]
               and cr["verdict"] == "DIVERGENT"]
        if div and r["verdict"] != "DIVERGENT":
            inconsistent.append((oid, "answered %s while %d of its own columns are DIVERGENT (%s). "
                                      "The roll-up is forced to DIVERGENT: a finding that hides under "
                                      "a clean model verdict is invisible to a scorer counting words."
                                 % (r["verdict"], len(div), ", ".join(sorted(div)))))
            r["verdict"] = "DIVERGENT"
            r["notes"].append("FORCED to DIVERGENT by a divergent column")

    unanswered = [oid for oid in by_id if oid not in rows]
    discharged = [r for r in rows.values() if r["verdict"] in DISCHARGING]
    outstanding = [r for r in rows.values() if r["verdict"] not in DISCHARGING]
    n_raised = len(by_id)
    n_out = len(outstanding) + len(unanswered)
    balances = n_raised == len(discharged) + n_out
    divergences = [r for r in outstanding if r["verdict"] in ("DIVERGENT", "BROKEN")]

    issues = emit_issues(args, manifest, divergences, bundle) if not args.no_issues else None
    return _report_and_write(args, bundle, manifest, raised, rows, rejected, quarantined, unsourced,
                             inconsistent, unanswered, discharged, outstanding, divergences,
                             n_raised, n_out, balances, verdict, drift, currency, issues, have_sheet)


# ---------------------------------------------------------------------------------------------
# EMISSION — into the issue framework's inventory, not into a private format.
#
# Gate B's output IS the functional-difference content the engine cannot produce for a platform it does
# not support. A diagnostic in a shape nothing downstream reads is a diagnostic nobody acts on, which is
# the same defect as a gate off the path. So every surviving divergence goes through the framework's own
# `classify()` and is written as a PROPOSAL, which is the concurrency-safe half of its propose/promote
# split -- a proposing agent has no write access to types/ and needs no coordination.
#
# THE CONSTRAINT THAT SHAPES THE TEXT, and it is the framework's and not mine: a TYPE may not name a
# platform or assert what a source platform does. Gate B's findings are exactly claims about source
# semantics, so the type says what was OBSERVED about the two expressions and the INSTANCE carries the
# platform and the rule. `issues/textrule.py` refuses the alternative at mint time, and its own docstring
# explains why: a sweep found 33 engine issue texts asserting source-platform runtime behaviour, every
# one of them in the two ETL dialects.
# ---------------------------------------------------------------------------------------------

DIVERGENCE_TYPES = {
    # keyed by the shape of the finding, chosen deterministically from the claim
    "value": {
        "category": "SEM",
        "construct": "column:value-derivation",
        "reason": "lowered-expression-differs-on-some-input",
        "title": "A lowered expression and the document's expression differ for a stated input",
        "text": "Column '{element}' was generated from an expression the document states for element "
                "of kind '{kind}'. A verification pass identified an input for which the generated "
                "expression and the document's expression do not yield the same value, and recorded "
                "that input and both results. Nothing here executed either side. {detail}",
        "impact": "output-incorrect",
        "note": "Raised by Gate B, a reading pass over the emitted SQL beside the source document. "
                "The measured case that motivates the type: one generated string is emitted for two "
                "different source platforms and is faithful for one of them, so no structural check, "
                "diff or compiler can separate the two. The instance record carries the platform, the "
                "cited dialect rule and the failing input.",
        "distinguisher": "This is not a construct the representation failed to carry and not a "
                         "predicate no rule could read: the construct WAS carried and WAS lowered, and "
                         "the lowering's result differs from the document's for an input the record "
                         "names. A reviewer acts on it by comparing two expressions, not by supplying "
                         "a missing one.",
    },
    "function": {
        "category": "SEM",
        "construct": "column:value-derivation",
        "reason": "lowered-expression-names-no-target-function",
        "title": "A lowered expression names a function the target dialect does not define",
        "text": "Column '{element}' was generated from an expression the document states for element "
                "of kind '{kind}'. The generated expression names a function that is not defined in "
                "the target dialect, so the generated model cannot run as written. This states a "
                "defect in the generated output and claims nothing about the document. {detail}",
        "impact": "output-absent",
        "note": "Cheap for a rule to catch as well, and recorded as its own type precisely so that the "
                "expensive semantic type is not diluted by it. findings/42 scored this one low for "
                "that reason while noting that missing it would still be bad.",
        "distinguisher": "The generated text is not runnable at all, rather than runnable with a "
                         "different result. A reviewer fixes it by naming a function that exists; the "
                         "value-divergence type needs a semantic decision instead.",
    },
    "shape": {
        "category": "SHAPE",
        "construct": "element:column-set",
        "reason": "generated-row-set-differs-from-declared",
        "title": "The generated row set does not match what the document declares for the element",
        "text": "The generated artifact for '{element}' of kind '{kind}' produces a row set that does "
                "not correspond to what the document declares: columns, row count or a routing "
                "decision. A verification pass recorded an input on which the two differ. {detail}",
        "impact": "output-incomplete",
        "note": "Distinct from a missing column list: here a column set exists and states something "
                "the document does not, which is why it is a divergence rather than an absence.",
        "distinguisher": "The representation carried a column set and the generated SQL projects a "
                         "different one; the column-metadata type covers an element for which no "
                         "column set was declared at all.",
    },
    "reference": {
        "category": "REF",
        "construct": "reference:upstream-element",
        "reason": "reference-does-not-resolve",
        "title": "A generated reference names a unit that is not in the output",
        "text": "A generated artifact for element '{element}' references the unit '{detail}', and no "
                "generated unit of that name is present in the output. The reference cannot resolve, "
                "so the artifact cannot run as generated. This states a defect in the generated output "
                "and claims nothing about the document.",
        "impact": "output-absent",
        "note": "Seeded from two measured engine causes with one symptom; Gate B reaches the same type "
                "from the artifact side by reading the ref graph.",
        "distinguisher": "seed-compatible: same signature as the seeded reference type, so it REUSES "
                         "rather than minting.",
    },
}

# Which type a divergence is, decided from the claim's own words rather than by asking the verifier to
# classify -- the framework's rule is that classification happens at the inventory, and a verifier
# choosing its own issue code is how a 888-member enum grows a 889th member.
def classify_divergence(r):
    blob = " ".join((r.get("reason") or "", r.get("differs_as") or "", r.get("sql_says") or "",
                     r.get("source_says") or "")).lower()
    if r["family"] == "TREE" or "does not resolve" in blob or "no such model" in blob:
        return "reference"
    if ("no such function" in blob or "not a snowflake function" in blob
            or "does not exist in snowflake" in blob or "not defined in snowflake" in blob
            or "unknown function" in blob):
        return "function"
    if ("row count" in blob or "column" in blob and "missing" in blob or "row set" in blob
            or "projects" in blob):
        return "shape"
    return "value"


def emit_issues(args, manifest, divergences, bundle):
    """Propose every surviving divergence into the issue inventory. Returns a record, never raises."""
    out = {"inventory_root": None, "instances": [], "proposed": [], "refused": [],
           "classification": []}
    try:
        sys.path.insert(0, HERE)
        from issues.inventory import Inventory
        from issues.textrule import lint
    except Exception as ex:
        out["refused"].append({"why": "the issue framework is not importable: %s" % ex})
        return out
    root = os.path.abspath(args.inventory_root
                           or os.environ.get("AIM_ISSUE_INVENTORY")
                           or os.path.join(HERE, "issue-inventory"))
    out["inventory_root"] = root
    inv = Inventory(root)
    platform = manifest.get("platform_hint") or "(unstated)"
    document = os.path.basename(manifest["inputs"]["document"])

    for r in divergences:
        shape = classify_divergence(r)
        proto = DIVERGENCE_TYPES[shape]
        proposal = dict(proto)
        proposal["first_observed"] = "gate_b.py %s / %s" % (document, r["obligation_id"])
        # CLASSIFY FIRST, and record what it was compared against -- "no existing type matched" has to
        # be an inspectable claim rather than an assertion.
        cls = inv.classify(proposal)
        best = (cls["considered"] or [{}])[0]
        out["classification"].append({
            "obligation_id": r["obligation_id"], "shape": shape, "verdict": cls["verdict"],
            "id": cls["id"] or cls["computed_id"], "rule": cls["rule"],
            "nearest": best.get("id"), "nearest_score": best.get("score"),
        })
        tid = cls["id"] or cls["computed_id"]
        try:
            res = inv.propose(proposal, by="gate_b:%s" % (manifest.get("arm") or "sourced"))
            out["proposed"].append({"id": res["id"], "path": res["path"], "shape": shape})
        except Exception as ex:
            out["refused"].append({"obligation_id": r["obligation_id"],
                                   "why": "%s: %s" % (type(ex).__name__, ex)})
            continue
        # THE INSTANCE, in the shape issues/stage.py writes, so a downstream reader needs no new format.
        detail = ("Input %s: %s. Source: %s SQL: %s"
                  % (r.get("failing_input") or "(none stated)", r.get("differs_as") or "",
                     r.get("source_says") or "", r.get("sql_says") or ""))
        text = " ".join(proto["text"].replace("{element}", str(r.get("output_column")
                                                              or r.get("model")))
                        .replace("{kind}", str(r.get("model")))
                        .replace("{detail}", detail).split())
        ilint = lint(text, scope="instance")
        inst = {
            "code": tid,
            "category": proto["category"], "construct": proto["construct"],
            "reason": proto["reason"], "impact": proto["impact"],
            "platform": platform, "document": document,
            "element_id": r["obligation_id"], "element": r.get("output_column") or r.get("model"),
            "observed_kind": r.get("model"),
            "detail": detail,
            "evidence": "document line %s %r | SQL %r%s"
                        % (r.get("source_locus"), r.get("source_quote"), r.get("sql_quote"),
                           (" | sheet %r" % r["sheet_quote"]) if r.get("sheet_quote") else ""),
            "location": r.get("sql_file"),
            "detector": "gate_b:verifier",
            "text": text,
            "text_lint": ilint["verdict"],
            "text_lint_findings": [x["rule"] for x in ilint["findings"]],
        }
        if ilint["verdict"] == "REJECT":
            # The template passed the type rule; the FILLED text did not. Recorded as a refusal, because
            # shipping it would be the exact defect the rule exists to stop.
            out["refused"].append({"obligation_id": r["obligation_id"],
                                   "why": "instance text failed the text rule: "
                                          + "; ".join(x["rule"] for x in ilint["findings"])})
            continue
        out["instances"].append(inst)

    dest = os.path.join(bundle, "AiFirstIssues")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "issues.json"), "w", encoding="utf-8") as fh:
        json.dump({"gate": "B", "platform": platform, "document": document,
                   "provenance": "MODEL",
                   "_note": "Instances proposed by Gate B. The TYPE ids were obtained from the issue "
                            "framework's own classify(); the types themselves are PROPOSALS awaiting "
                            "the single writer's promote(). Nothing here was minted by this gate.",
                   "instances": out["instances"], "refused": out["refused"],
                   "classification": out["classification"]}, fh, indent=2)
    import csv
    cols = ["code", "category", "construct", "reason", "impact", "platform", "document",
            "element_id", "element", "observed_kind", "detail", "evidence", "location", "detector",
            "text"]
    with open(os.path.join(dest, "issues.csv"), "w", encoding="utf-8", newline="") as fh:
        # QUOTE_ALL: every field is model-authored prose read off a source document, and a value that
        # happens to start with =, +, -, or @ opens as a formula in a spreadsheet reader unless it is
        # unconditionally quoted -- unquoted numeric-looking fields are exactly how CSV formula
        # injection reaches a reviewer who opens this file in Excel/Sheets.
        w = csv.writer(fh, quoting=csv.QUOTE_ALL)
        w.writerow(cols)
        for i in out["instances"]:
            w.writerow([i.get(c, "") for c in cols])
    out["artifact"] = dest
    return out


def _report_and_write(args, bundle, manifest, raised, rows, rejected, quarantined, unsourced,
                      inconsistent, unanswered, discharged, outstanding, divergences,
                      n_raised, n_out, balances, verdict, drift, currency, issues, have_sheet):
    loop = gate_a._stop_reason(os.path.join(bundle, "gateB-loop.json"), args.iteration,
                               args.max_iterations, n_out)
    print("=" * W)
    print(" GATE B — INTENT PARITY (agentic)")
    print("=" * W)
    print(" bundle        : %s" % bundle)
    print(" document      : %s" % manifest["inputs"]["document"])
    print(" project       : %s" % manifest["inputs"]["project"])
    print(" arm           : %s   [reference sheet %s]"
          % (manifest.get("arm"), "staged" if have_sheet else "NOT staged"))
    print(" verifier      : %s" % (verdict.get("verifier") or "UNNAMED"))
    if drift:
        print(" *** INPUT DRIFT — the verifier was asked about inputs that have since changed:")
        for d in drift:
            print("     %s" % d)
        print("     The verdicts below were produced against the PACKED state. Re-pack before")
        print("     treating this ledger as current.")
    print(" currency      : " + "  ".join("%s=%s" % (k.replace("_is_current", ""), v)
                                          for k, v in sorted(currency.items())))
    print("-" * W)
    print(" %-52s %-12s %-13s %s" % ("obligation", "verdict", "basis", "citation"))
    print("-" * W)
    for oid in [o["id"] for o in raised["obligations"]]:
        r = rows.get(oid)
        if r is None:
            print(" %-52s %-12s %-13s %s"
                  % (oid[:52], "UNANSWERED", "-", "no answer — scored OUTSTANDING"))
            continue
        print(" %-52s %-12s %-13s %s" % (oid[:52], r["verdict"], r["basis"], r["citation"]))
        for label, key in (("source", "source_says"), ("sql", "sql_says"),
                           ("input", "failing_input"), ("differs", "differs_as"),
                           ("why", "reason")):
            if r.get(key):
                for chunk in _wrap("%-8s %s" % (label + ":", r[key]), W - 10):
                    print("        %s" % chunk)
        for n in r["notes"]:
            print("        *** %s" % n)
    print("-" * W)
    if inconsistent:
        print(" ROLL-UP FORCED — a model cannot be clean over a column that is not:")
        for oid, why in inconsistent:
            for chunk in _wrap("%s: %s" % (oid, why), W - 6):
                print("     %s" % chunk)
    if unsourced:
        # PRINTED, NEVER COUNTED. findings/43 measured a verifier being right from memory; this is the
        # place that makes that visible instead of rewarding it.
        print(" UNSOURCED REMARKS — asserted from the verifier's own knowledge. Printed, not counted:")
        for oid, v, why in unsourced:
            for chunk in _wrap("%s would have been %s: %s" % (oid, v, why), W - 6):
                print("     %s" % chunk)
    if quarantined:
        print(" QUARANTINED CLAIMS — could not count, and why. These discharge NOTHING:")
        for oid, why in quarantined:
            for chunk in _wrap("%s: %s" % (oid, why), W - 6):
                print("     %s" % chunk)
    if rejected:
        print(" REJECTED ANSWERS — an obligation this artifact never raised:")
        for oid, why in rejected:
            print("     %s: %s" % (oid, why))
    print("-" * W)
    print(" ledger        : raised=%d discharged=%d outstanding=%d divergent=%d quarantined=%d "
          "rejected=%d unsourced=%d balances=%s"
          % (n_raised, len(discharged), n_out, len(divergences), len(quarantined), len(rejected),
             len(unsourced), balances))
    print(" by family     : " + "  ".join(
        "%s %d/%d" % (fam, sum(1 for r in discharged if r["family"] == fam), raised["counts"][fam])
        for fam in ("EXPRESSION", "MODEL", "TREE")))
    print(" NO SCORE IS REPORTED. The bar is obligations discharged; a percentage is a number the")
    print("                 loop can move, and this project measured one rising as elements were lost.")
    print(" loop          : iteration %d of %s — stop reason %s"
          % (loop["iteration"],
             loop["max_iterations"] if loop["max_iterations"] is not None else "unbounded",
             loop["stop_reason"]))
    for chunk in _wrap(loop["stop_detail"], W - 18):
        print("                 %s" % chunk)
    if issues is not None:
        print(" issues        : %d instance(s) proposed into %s"
              % (len(issues["instances"]), issues.get("inventory_root")))
        for c in issues["classification"]:
            print("     %-30s %-14s %s (nearest %s at %s)"
                  % (c["obligation_id"][:30], c["verdict"], c["id"], c["nearest"],
                     c["nearest_score"]))
        if issues["refused"]:
            print("     *** %d finding(s) REFUSED by the framework — observed and NOT recorded, so the"
                  % len(issues["refused"]))
            print("     count above is a floor:")
            for r in issues["refused"]:
                for chunk in _wrap(str(r), W - 8):
                    print("       %s" % chunk)
        if issues.get("artifact"):
            print("     artifact  : %s/issues.csv (+ issues.json)" % issues["artifact"])

    sidecar_path = args.sidecar or os.path.join(bundle, "gateB-sidecar.json")
    sidecar = {
        "gate": "B",
        "provenance": "MODEL",
        "_provenance_note": ("Every entry below was produced by a MODEL reading the source document "
                             "beside the generated SQL, not by a deterministic rule. It is a SIDECAR: "
                             "nothing here is written into an emitted model, into the IR or into any "
                             "deterministic input, so engine-derived and model-derived statements stay "
                             "distinguishable."),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bundle": bundle,
        "arm": manifest.get("arm"),
        "document": manifest["inputs"]["document"],
        "document_sha256": manifest["inputs"]["document_sha256"],
        "project": manifest["inputs"]["project"],
        "verifier": verdict.get("verifier"),
        "ledger": {"raised": n_raised, "discharged": len(discharged), "outstanding": n_out,
                   "divergent": len(divergences), "quarantined": len(quarantined),
                   "rejected": len(rejected), "unsourced": len(unsourced), "balances": balances},
        "loop": loop,
        "input_drift": list(drift),
        "input_currency": currency,
        "discharged": [dict(r, provenance="MODEL") for r in discharged],
        "unresolved": ([dict(r, provenance="MODEL") for r in outstanding]
                       + [{"obligation_id": oid, "verdict": "UNANSWERED", "provenance": "MODEL",
                           "reason": "the verifier did not answer this obligation"}
                          for oid in unanswered]),
        "divergences": [dict(r, provenance="MODEL") for r in divergences],
        "quarantined": [{"obligation_id": oid, "why": why} for oid, why in quarantined],
        "unsourced_remarks": [{"obligation_id": oid, "would_have_been": v, "why": why}
                              for oid, v, why in unsourced],
        "rejected": [{"obligation_id": oid, "why": why} for oid, why in rejected],
        "roll_up_forced": [{"obligation_id": oid, "why": why} for oid, why in inconsistent],
        "issues": issues,
        "notes": verdict.get("notes") or [],
    }
    with open(sidecar_path, "w", encoding="utf-8") as fh:
        json.dump(sidecar, fh, indent=1)
    with open(os.path.join(bundle, "gateB-loop.json"), "w", encoding="utf-8") as fh:
        json.dump(loop, fh, indent=1)
    print(" sidecar       : %s   [provenance MODEL, %d unresolved]"
          % (sidecar_path, len(sidecar["unresolved"])))
    print("-" * W)
    if not balances:
        raise GateBError("LEDGER DOES NOT BALANCE: raised=%d discharged=%d outstanding=%d. This is a "
                         "defect in Gate B, not a finding about the input."
                         % (n_raised, len(discharged), n_out))
    if n_out:
        print(" VERDICT: FAIL — %d obligation(s) OUTSTANDING, %d of them divergences. The generated"
              % (n_out, len(divergences)))
        print("          SQL does not provably do what the document states. List handed over above")
        print("          and in the sidecar. (exit 3)")
        for r in outstanding:
            print("     *** %s [%s] : %s" % (r["obligation_id"], r["family"], r["verdict"]))
        for oid in unanswered:
            print("     *** %s : UNANSWERED" % oid)
        return 3
    print(" VERDICT: every raised obligation is discharged — every generated column was matched to a")
    print("          source expression and no divergence was found on any stated input.")
    print("          NOT a claim of correctness: nothing here compiled or ran anything. (exit 0)")
    return 0


def run(args):
    rc = pack(args)
    if rc:
        return rc
    bundle = os.path.abspath(args.bundle)
    verdict_path = os.path.join(bundle, "verdict.json")
    if not args.verifier_cmd:
        print("-" * W)
        print(" NO --verifier-cmd GIVEN. The bundle is packed and the gate stops here rather than")
        print(" pretending a verdict. This is not a pass: an unrun gate is UNMEASURED, which is a")
        print(" different claim from clean. Exit 1 (could not run).")
        raise GateBError("no verifier configured; bundle packed at %s" % bundle)
    cmd = args.verifier_cmd.replace("{bundle}", bundle).replace("{verdict}", verdict_path)
    print("-" * W)
    print(" verifier      : %s" % cmd)
    proc = subprocess.run(cmd, shell=True)
    if proc.returncode != 0:
        raise GateBError("verifier command exited %d" % proc.returncode)
    if not os.path.isfile(verdict_path):
        raise GateBError("verifier command wrote no %s" % verdict_path)
    args.verdict = verdict_path
    return score(args)


# ---------------------------------------------------------------------------------------------
# THE FALSIFIABILITY TEST, AS CODE.
#
# `findings/42` fixed this before any verifier returned, and `findings/43` scored it by hand. The
# outcome table is reproduced here EXACTLY, including the ordering of the two failure modes, because
# over-flagging is the worse one:
#
#   Informatica DIVERGENT + SSIS EQUIVALENT   PASS. Two identical strings discriminated by the
#                                             semantics of the platform each came from.
#   both EQUIVALENT                           FAIL, disqualifying. Gate B is not ready, and it fails
#                                             in the same direction as the engine's own bug.
#   both DIVERGENT                            FAIL. Over-flagging, and WORSE than the miss: a gate that
#                                             flags correct output teaches reviewers to ignore it, and
#                                             that channel is how real risk gets reported.
#   either UNVERIFIABLE                       PARTIAL. Honest, and does not deliver the central value.
#
# The probe column is not named here. It is computed at pack time from the emitted artifact and stored
# in each bundle's MANIFEST.json, so this scorer reads which column to score rather than being told,
# and the verifier never sees which column the test is on.
# ---------------------------------------------------------------------------------------------

def falsify(args):
    def load(bundle, label):
        b = os.path.abspath(bundle)
        try:
            with open(os.path.join(b, "MANIFEST.json"), "r", encoding="utf-8") as fh:
                man = json.load(fh)
            with open(os.path.join(b, "gateB-sidecar.json"), "r", encoding="utf-8") as fh:
                side = json.load(fh)
        except Exception as ex:
            raise GateBError("%s bundle not packed and scored: %s" % (label, ex))
        probe = man.get("falsifiability_probe")
        if not probe:
            raise GateBError("%s bundle has no falsifiability probe: the emitted SQL does not contain "
                             "%r, so the disqualifying case is NOT PRESENT in this artifact and "
                             "cannot be scored. That is a change in the input, not a pass."
                             % (label, PROBE_EXPRESSION))
        claims = {r["obligation_id"]: r for r in side["discharged"] + side["unresolved"]}
        r = claims.get(probe["obligation_id"])
        q = [x for x in side.get("quarantined") or [] if x["obligation_id"] == probe["obligation_id"]]
        return {"label": label, "bundle": b, "probe": probe, "claim": r, "quarantined": q,
                "arm": man.get("arm"), "verifier": side.get("verifier")}

    infa = load(args.informatica, "informatica")
    ssis = load(args.ssis, "ssis")

    print("=" * W)
    print(" GATE B — THE PRE-REGISTERED DISQUALIFYING CASE (findings/42 TEST 1)")
    print("=" * W)
    print(" the probe      : %r" % PROBE_EXPRESSION)
    identical = infa["probe"]["expression"] == ssis["probe"]["expression"]
    print(" byte-identical : %s   [informatica %s | ssis %s]"
          % (identical, infa["probe"]["obligation_id"], ssis["probe"]["obligation_id"]))
    if not identical:
        print(" *** THE TWO GENERATED EXPRESSIONS ARE NOT IDENTICAL ANY MORE. The test's whole point is")
        print("     that a structural check cannot separate them; if they differ, this is no longer the")
        print("     same experiment and the result below does not mean what findings/42 scored.")
    print("-" * W)
    verdicts = {}
    for side in (infa, ssis):
        r, q = side["claim"], side["quarantined"]
        v = (r or {}).get("verdict") or ("QUARANTINED" if q else "UNANSWERED")
        verdicts[side["label"]] = v
        print(" %-13s %-12s arm=%-8s verifier=%s"
              % (side["label"], v, side["arm"], side["verifier"]))
        if r:
            for label, key in (("basis", "basis"), ("input", "failing_input"),
                               ("differs", "differs_as"), ("sheet", "sheet_quote"),
                               ("why", "reason")):
                if r.get(key):
                    for chunk in _wrap("%-8s %s" % (label + ":", r[key]), W - 8):
                        print("       %s" % chunk)
        for x in q:
            for chunk in _wrap("QUARANTINED: %s" % x["why"], W - 8):
                print("       %s" % chunk)
    print("-" * W)
    i, s = verdicts["informatica"], verdicts["ssis"]
    # Mentioning NULL is not the verdict, but a DIVERGENT that is right for the wrong reason is worth
    # separating from one that named the asymmetry the test is about.
    names_null = "null" in json.dumps(infa["claim"] or {}).lower()
    if i == "DIVERGENT" and s == "EQUIVALENT":
        outcome, detail = "PASS", ("the same generated string was discriminated by the semantics of "
                                  "the platform each came from — the thing no structural check can do")
        if not names_null:
            detail += (". NOTE: the informatica divergence does not mention NULL, so it may be right "
                       "for a different reason. Read the claim above before relying on this")
    elif i == "EQUIVALENT" and s == "EQUIVALENT":
        outcome, detail = "FAIL — DISQUALIFYING", ("both EQUIVALENT. Gate B is not ready, and it fails "
                                                  "in the same direction as the engine's own bug")
    elif i == "DIVERGENT" and s == "DIVERGENT":
        outcome, detail = "FAIL — OVER-FLAGGING", ("both DIVERGENT. This is the WORSE failure: a gate "
                                                  "that flags correct output teaches reviewers to "
                                                  "ignore it, and that channel is how real risk is "
                                                  "reported")
    elif "UNVERIFIABLE" in (i, s):
        outcome, detail = "PARTIAL", ("honest, and it does not deliver the gate's central value")
    else:
        outcome, detail = "FAIL", ("informatica=%s ssis=%s: neither the pass condition nor a recognised "
                                  "failure mode. An unanswered or quarantined probe is not a pass"
                                  % (i, s))
    print(" OUTCOME: %s" % outcome)
    for chunk in _wrap(detail, W - 10):
        print("          %s" % chunk)
    print(" scored against findings/42 TEST 1, whose outcome table was fixed before any verifier ran")
    print("-" * W)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"probe": PROBE_EXPRESSION, "byte_identical": identical,
                       "informatica": {k: infa[k] for k in ("bundle", "arm", "verifier", "probe",
                                                            "claim", "quarantined")},
                       "ssis": {k: ssis[k] for k in ("bundle", "arm", "verifier", "probe", "claim",
                                                     "quarantined")},
                       "verdicts": verdicts, "outcome": outcome, "detail": detail,
                       "informatica_reason_names_null": names_null,
                       "scored_against": "findings/42-gate-b-falsifiability-criteria.md TEST 1"},
                      fh, indent=1)
        print(" record        : %s" % args.out)
    return 0 if outcome == "PASS" else 3


def main(argv):
    ap = argparse.ArgumentParser(prog="gate_b.py",
                                 description="Gate B — agentic intent-parity gate.")
    sub = ap.add_subparsers(dest="cmd")

    def add_pack_args(p):
        p.add_argument("doc")
        p.add_argument("out_root")
        p.add_argument("--bundle", required=True)
        p.add_argument("--reference", default=None,
                       help="the dialect reference sheet (default: blind-run/gateB/DIALECT_REFERENCE.md)")
        p.add_argument("--arm", choices=("sourced", "naive"), default="sourced",
                       help="sourced stages the reference sheet; naive stages none, so a dialect rule "
                            "can only be declared PRIOR and PRIOR discharges nothing")
        p.add_argument("--platform", default=None,
                       help="recorded on emitted issue instances. NOT staged for the verifier")

    def add_score_args(p):
        p.add_argument("--sidecar", default=None)
        p.add_argument("--iteration", type=int, default=1)
        p.add_argument("--max-iterations", dest="max_iterations", type=int, default=3)
        p.add_argument("--inventory-root", dest="inventory_root", default=None)
        p.add_argument("--no-issues", dest="no_issues", action="store_true",
                       help="score without proposing into the issue inventory")

    p = sub.add_parser("pack")
    add_pack_args(p)

    p = sub.add_parser("score")
    p.add_argument("--bundle", required=True)
    p.add_argument("--verdict", required=True)
    add_score_args(p)

    p = sub.add_parser("run")
    add_pack_args(p)
    add_score_args(p)
    p.add_argument("--verifier-cmd", dest="verifier_cmd", default=None)

    p = sub.add_parser("batched-run", help="default: bounded family batches, verified in parallel")
    add_pack_args(p)
    add_score_args(p)
    p.add_argument("--cli", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--max-budget-usd", dest="max_budget_usd", default=None)
    p.add_argument("--verifier-timeout", dest="verifier_timeout", type=int, default=900)
    p.add_argument("--view-root", dest="view_root", default=None)
    p.add_argument("--keep-view", dest="keep_view", action="store_true")
    p.add_argument("--expression-batch-size", dest="expression_batch_size", type=int,
                   default=int(os.environ.get("AIFIRST_GATEB_EXPRESSION_BATCH_SIZE", "8")))
    p.add_argument("--model-batch-size", dest="model_batch_size", type=int,
                   default=int(os.environ.get("AIFIRST_GATEB_MODEL_BATCH_SIZE", "12")))
    p.add_argument("--parallelism", type=int,
                   default=int(os.environ.get("AIFIRST_GATE_PARALLELISM", "4")))

    p = sub.add_parser("verifier")
    p.add_argument("--bundle", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--cli", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--max-budget-usd", dest="max_budget_usd", default=None)
    p.add_argument("--verifier-timeout", dest="verifier_timeout", type=int, default=1800)
    p.add_argument("--view", default=None)
    p.add_argument("--view-root", dest="view_root", default=None)
    p.add_argument("--keep-view", dest="keep_view", action="store_true")

    p = sub.add_parser("falsify", help="score the pre-registered disqualifying case")
    p.add_argument("--informatica", required=True)
    p.add_argument("--ssis", required=True)
    p.add_argument("--out", default=None)

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
        if args.cmd == "falsify":
            return falsify(args)
        return run(args)
    except (GateBError, gate_a.GateAError) as ex:
        # ONE exit code for every could-not-run condition, and it is not an obligation verdict. The
        # driver tells the two apart by the absence of the " ledger        :" line.
        sys.stderr.write("GATE B COULD NOT RUN: %s\n" % ex)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
