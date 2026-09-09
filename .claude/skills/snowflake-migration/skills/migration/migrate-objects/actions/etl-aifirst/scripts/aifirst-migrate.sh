#!/usr/bin/env bash
# SPIKE 5 — the process boundary: one command, source document in, dbt tree out, HONEST exit code.
#
# WHY THIS EXISTS. Measured before writing it, both halves of the chain exit 0 on degraded output:
#
#   python3 main.py <informatica multi-mapping doc>   -> exit 0, and silently loses 6 of 9 elements
#   aifirst-migrate --no-shim <ir> <out>              -> exit 0, emits an unresolvable sentinel
#                                                        and silently drops 4 columns
#
# So a caller that checks `$?` learns nothing about fidelity. That is exactly ENG-009's shape — the
# engine's own `void Main` exiting 0 after a crash — reproduced on both sides of our own chain.
#
# The element-loss detector DOES exist (declared_vs_identified.py) but it is a SEPARATE script over a
# fixed canonical set. Nothing obliges a caller to run it, and it does not look at the document being
# migrated. A gate off the path is not a gate.
#
# EXIT CODE VOCABULARY. The point of this driver is that "it ran" and "it produced good output" are
# different questions and need different answers:
#
#   0  migrated, no degradation detected
#   3  MIGRATED WITH DEGRADATION — output exists and is loudly incomplete (element loss,
#      unresolved markers in the artifact, model-authored models, SQL a parser rejects, NO ETL
#      LINEAGE, NO REPORT/ASSESSMENT ARTIFACTS, an EMPTY DIAGNOSTIC CHANNEL, or a TASK GRAPH that
#      is absent, names nothing from the input document, points at a dbt project that is not
#      there, names a PREDECESSOR TASK nothing creates, or has NO ROOT at all). NOT a claim that
#      the output runs: three of the
#      four blind trees carry a compile error at this exit code. "Runnable, not trustworthy" was the
#      original wording here and it overstated the case for exactly the reason ai_fill's
#      "RUNNABLE, NOT VERIFIED" stamp did. This is the code that does not exist today and is the
#      whole point.
#   1  failed — no usable output
#   2  usage error
#
# Deliberately NOT collapsing 3 into 0 (which hides it) or into 1 (which throws away real work).
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK="$HERE"
if [ -z "${AIFIRST_EMITTER:-}" ]; then
  echo "usage: set AIFIRST_EMITTER to the AiFirstEtl producer dll (e1 Snowflake.SnowConvert.AiFirstEtl)" >&2
  # exit 2: usage / unresolvable input — producer DLL must be provided before any stage runs
  exit 2
fi
EMITTER="$AIFIRST_EMITTER"
if [ ! -f "$EMITTER" ]; then
  echo "usage: AIFIRST_EMITTER does not name a readable file: $EMITTER" >&2
  # exit 2: usage / unresolvable input — path set but not a readable file
  exit 2
fi

# --no-shim is passed through to the emitter. It exists to DEMONSTRATE the degradation path: with the
# SSIS semantics shim off, the same document emits an unresolvable sentinel and drops 4 columns, which
# is precisely the case a caller must be able to distinguish from success.
EMIT_FLAGS=""
if [ "${1:-}" = "--no-shim" ]; then EMIT_FLAGS="--no-shim"; shift; fi

# --inspect-only runs STAGE 4 ALONE against a tree that already exists, without regenerating it.
#
# WHY IT EXISTS: every gate in stage 4 has to be negative-tested — shown firing when the thing it
# checks is absent AND staying quiet when it is present. This project has shipped three gates that
# could not fail and caught them only by disbelieving a good number. Without this flag a negative test
# has to re-implement the gate's expressions outside the script, which tests the copy and not the
# gate: the adjacent-verification trap. With it, the test deletes an artifact from a real tree and
# runs THE SHIPPED CODE over it.
INSPECT_ONLY=0
if [ "${1:-}" = "--inspect-only" ]; then INSPECT_ONLY=1; shift; fi

SYNTHESIZE_TABLE=0
PLATFORM_ID=""
if [ "${1:-}" = "--platform" ]; then
  if [ "$INSPECT_ONLY" = "1" ] || [ $# -ne 4 ] || [ -z "${2:-}" ]; then
    echo "usage: aifirst-migrate.sh [--no-shim] --platform <platform-identity> <source-document> <output-root>" >&2
    exit 2
  fi
  SYNTHESIZE_TABLE=1
  PLATFORM_ID="$2"
  DOC="$3"
  OUT="$4"
elif [ $# -ne 3 ]; then
  echo "usage: aifirst-migrate.sh [--no-shim] [--inspect-only] <platform-table.json> <source-document> <output-root>" >&2
  # exit 2: usage — wrong argc, fail before stages run
  exit 2
else
  TABLE="$1"
  DOC="$2"
  OUT="$3"
fi
# ---- ONE PRUNE EXPRESSION, USED BY EVERY TREE WALK BELOW ----------------------------------------
# MEASURED, on the first negative test of the new gates: re-inspecting an already-compiled tree
# reported `models with NO columns : 12` and `dbt projects with SQL errors : 2` on a tree the same
# script had just called clean. Cause: `dbt compile` writes `dbt_internal_packages/dbt-snowflake` and
# `.../dbt-adapters`, each of which carries its OWN dbt_project.yml and its own models/*.sql. A fresh
# run never saw them because stage 3 does `rm -rf "$OUT"` first, so the finds ran before dbt existed.
#
# That made stage 4 NOT IDEMPOTENT: the same tree scored differently depending on whether dbt had run
# over it. A gate whose verdict depends on the order it is invoked in cannot be negative-tested, and
# would have silently flipped the day anything re-inspected a tree.
#
# `target/` is pruned for the same reason: it holds dbt's own compiled copies of every model, which
# would double every model count.
PRUNE=( -name dbt_internal_packages -prune -o -name target -prune -o )
# MOVED HERE FROM STAGE 4b, AND THE MOVE IS ITSELF A CAUGHT DEFECT. Defined below its first use, the
# column-less-model check at stage 4 expanded `${PRUNE[@]}` under `set -u`, printed
# `PRUNE[@]: unbound variable` from inside a `$(...)`, so `find` never ran, the loop never iterated,
# and the check reported `models with NO columns : 0` on every tree. A gate that cannot fire, produced
# while adding gates, visible only because the clean-tree exit-0 test surfaced the stderr line.

# ABSOLUTISED, AND IT IS A MEASURED FOOTGUN AND NOT A TIDY-UP. Stage 1 runs `cd "$FRAMEWORK"` before
# handing the table and the document to identify.py, so a RELATIVE table path resolves against the
# framework directory instead of the caller's. Measured: invoking this script with
# `gateA-fixtures/platform_datastage_before_transformer_sweep.json` — a path that exists, from the
# directory the script lives in — produced `FileNotFoundError` inside the ledger and **exit 1, a failed
# migration**, on an input that was perfectly fine. Exit 1 means "no usable output"; the correct answer
# to a path this script cannot resolve is a USAGE error, before any stage runs.
_INPUTS=(DOC)
if [ "$SYNTHESIZE_TABLE" = "0" ]; then _INPUTS=(TABLE DOC); fi
for _v in "${_INPUTS[@]}"; do
  declare -n _ref="$_v"
  _p="$_ref"
  if [ ! -f "$_p" ] || [ ! -r "$_p" ]; then
    echo "usage: $_v does not name a readable file: $_p" >&2
    # exit 2: usage — unresolvable input path, fail before stages run
    exit 2
  fi
  _ref="$(cd "$(dirname "$_p")" && pwd)/$(basename "$_p")"
done
unset -n _ref

GATE_BUNDLES="${AIFIRST_GATE_BUNDLES:-$OUT.gates}"
if [ "$SYNTHESIZE_TABLE" = "1" ]; then
  STAGE0_EVIDENCE="$GATE_BUNDLES/stage0"
  rm -rf "$STAGE0_EVIDENCE"
  AUTHOR_CLI="${AIFIRST_TABLE_AUTHOR_CLI:-${AIFIRST_VERIFIER_CLI:-claude}}"
  if python3 "$HERE/author_platform_table.py" "$PLATFORM_ID" --checked-in >/dev/null; then
    echo "-- stage 0: use checked-in platform table"
    if ! python3 "$HERE/author_platform_table.py" "$PLATFORM_ID" "$DOC" "$STAGE0_EVIDENCE" \
         --retain-checked-in; then
      echo "   FAILED: checked-in platform table could not be retained" >&2
      rm -rf "$OUT"
      # exit 1: failed migration — a named platform had a table, but Stage 0 could not keep it
      exit 1
    fi
  else
    echo "-- stage 0: author provisional platform table"
    # RESEARCH IS A SEPARATE TRUST DOMAIN, BEFORE THE EXECUTABLE TABLE IS WRITTEN.
    # The researcher may browse and may write only a bounded, cited dossier. The table author
    # remains offline and can write only platform_table.json / authoring_notes.md; deterministic
    # validation remains the acceptance oracle. If search/fetch is unavailable or the dossier is
    # unusable, author_platform_table.py records that fact and falls back to source + prior art.
    STAGE0_RESEARCH_ARGS=()
    if [ "${AIFIRST_TABLE_WEB_RESEARCH:-1}" != "0" ]; then
      STAGE0_RESEARCH_ARGS=(
        --web-research
        --research-timeout "${AIFIRST_TABLE_RESEARCH_TIMEOUT:-600}"
      )
    fi
    if ! python3 "$HERE/author_platform_table.py" "$PLATFORM_ID" "$DOC" "$STAGE0_EVIDENCE" \
         --cli "$AUTHOR_CLI" --timeout "${AIFIRST_TABLE_AUTHOR_TIMEOUT:-900}" \
         --max-attempts "${AIFIRST_TABLE_AUTHOR_ATTEMPTS:-4}" \
         "${STAGE0_RESEARCH_ARGS[@]}"; then
      echo "   FAILED: no platform table passed deterministic acceptance" >&2
      rm -rf "$OUT"
      # exit 1: failed migration — Stage 0 produced no usable table; later stages cannot run
      exit 1
    fi
  fi
  TABLE="$STAGE0_EVIDENCE/accepted-platform-table.json"
  if [ ! -f "$TABLE" ]; then
    echo "   FAILED: accepted platform table is missing" >&2
    rm -rf "$OUT"
    # exit 1: failed migration — Stage 0 claimed success without an accepted table artifact
    exit 1
  fi
  echo "   accepted table: $TABLE"
  TABLE_PLATFORM="$PLATFORM_ID"
else
  TABLE_PLATFORM="$(basename "$TABLE" .json | sed 's/^platform_//')"
fi

# COVERAGE MEASURABILITY, ANNOUNCED HERE INSTEAD OF DISCOVERED AT STAGE 3D.
# MEASURED: a blind Informatica run authored its table under the identity `informatica`, ran for
# forty minutes, and reported COVERAGE UNMEASURED at stage 3d because coverage_gate.RULES keys the
# denominator as `InformaticaPowerCenter`. Nothing between the two said so. The identity is a free
# string, the keys are not uniformly cased, and the failure surfaces after every expensive stage has
# already run -- so the same typo costs the same forty minutes every time it is made.
# Not fatal, deliberately: `platform_adf.json` is checked in and ADF has no counting rule yet, so a
# hard failure here would refuse a table this repository ships. UNMEASURED stays a legal outcome.
# What it must not stay is a SURPRISE, and a near miss printed next to the identity that produced it
# is the difference between a typo and forty minutes.
COVERAGE_ADVISORY=$(python3 - "$HERE" "$TABLE" <<'PY'
import difflib
import json
import sys

sys.path.insert(0, sys.argv[1])
from coverage_gate import RULES

identity = (json.load(open(sys.argv[2], encoding="utf-8")).get("platform") or "").strip()
if identity in RULES:
    sys.exit(0)
near = difflib.get_close_matches(identity, list(RULES), n=1, cutoff=0.4)
print("*** COVERAGE WILL BE UNMEASURED -- the table states platform %r, which has no "
      "source-element counting rule." % identity)
if near:
    print("    Did you mean %r? Gate A keys its denominator by this exact string." % near[0])
print("    Rules exist for: %s." % ", ".join(sorted(RULES)))
PY
)
if [ -n "$COVERAGE_ADVISORY" ]; then printf '%s\n' "$COVERAGE_ADVISORY" | sed 's/^/   /'; fi
# XXXXXX required on GNU mktemp (Linux); macOS mktemp accepts the same form.
IR="$(mktemp -t aifirst-ir.XXXXXX).json"
EMITLOG="$(mktemp -t aifirst-emit.XXXXXX).log"
degraded=0

# MOVED UP OUT OF STAGE 3e, AND THE MOVE IS THE WHOLE REASON STAGE 4d CAN BE NEGATIVE-TESTED.
# This was defined at stage 3e, inside the block `--inspect-only` skips. Stage 4d compares the IR
# against the tree and therefore needs the IR in BOTH modes -- and under `--inspect-only` the `$IR`
# temp path does not even exist (mktemp creates `aifirst-ir.XXXX` and the `.json` is appended after,
# so `$IR` names a file nothing ever wrote). So a full run STASHES the representation beside the gate
# bundles and stage 4d reads the stash, which makes `--inspect-only` able to re-inspect a tree with
# the same representation the run used. Without that, every stage-4d negative test would have to
# re-implement the gate outside the script: the adjacent-verification trap this flag exists to avoid.
# The assignment has no side effects; `mkdir -p` stays where it was.
GATE_BUNDLES="${AIFIRST_GATE_BUNDLES:-$OUT.gates}"
INTEGRITY_IR="$GATE_BUNDLES/integrity/ir.json"

echo "=============================================================="
echo " AI-first migration: $(basename "$DOC")"
echo "=============================================================="

if [ "$INSPECT_ONLY" = "1" ]; then
  if [ ! -d "$OUT" ]; then
    echo "usage: --inspect-only needs an existing tree at $OUT" >&2
    rm -f "$IR" "$EMITLOG"
    # exit 2: usage — unresolvable input before stages (not "failed migration / no usable output")
    exit 2
  fi
  echo "-- stages 1-3d SKIPPED (--inspect-only): inspecting the tree already at $OUT"
fi

if [ "$INSPECT_ONLY" = "0" ]; then

# ---- STAGE 1: identification, WITH the loss ledger on THIS document ------------------------------
# The ledger runs on the document being migrated, not on a canonical set, and its verdict gates
# stage 2 rather than being advisory.
echo "-- stage 1: identify"
LEDGER=$(cd "$FRAMEWORK" && python3 - "$TABLE" "$DOC" <<'PY' 2>&1
import io, sys
from contextlib import redirect_stdout
from identify import Identification, load_table
buf = io.StringIO()
with redirect_stdout(buf):
    idn = Identification(load_table(sys.argv[1]), sys.argv[2])
a = idn.accounting()
# `declared` CHANGED MEANING UNDER THIS LINE AND THE LINE BECAME A FALSE ALARM.
#
# The exhaustive-census pass redefined accounting()["declared"] from "nodes the level queries
# matched" to "every record in the document", preserving the old number as `level_matched`. This
# line printed `declared=%d ... identified=%d`, so on CustomerSummaryDerive.dsx it rendered
# `declared=52 ... identified=5` -- which reads as 47 LOST. RE-MEASURED, not reworded from the
# report: records 52, level_matched 5, keyless 0, identified 5, excluded 46, unknown 1, lost 0,
# balances True. Nothing is lost; 46 records are excluded by a named table rule and 1 is an
# inventoried unknown object.
#
# Every term of the census is printed rather than a chosen subset, because the whole reason
# `declared` misled is that one number was shown and the identity it belongs to was not.
# THE GATE BELOW IS UNCHANGED AND IS STILL CORRECT: `lost` keeps its meaning ("identified, then
# silently overwritten by a later record with the same key") and `balances` is now strictly
# stronger than it was.
print("records=%d level_matched=%d keyless=%d identified=%d excluded=%d unknown=%d lost=%d balances=%s"
      % (a["records"], a["level_matched"], a["keyless"], a["identified"],
         a["excluded"], a["unknown"], a["lost"], a["balances"]))
sys.exit(1 if (a["lost"] or not a["balances"]) else 0)
PY
)
LEDGER_RC=$?
echo "   ledger: $LEDGER"
# Distinguish "the ledger RAN and found loss" from "the ledger could not run at all". The first
# version of this driver conflated them: a missing source file exited non-zero and was reported as
# "*** ELEMENTS LOST ***", which is a false and alarming claim about a document that was never read.
# Exit code alone cannot tell them apart, so the ledger's stdout shape is what disambiguates —
# a real verdict always contains "lost=".
if ! printf '%s' "$LEDGER" | grep -q "lost="; then
  echo "   FAILED: the loss ledger could not run on this document — cause above, not element loss" >&2
  rm -f "$IR" "$EMITLOG"
  # exit 1: hard fail — no usable output (ledger never produced a verdict shape)
  exit 1
fi
if [ $LEDGER_RC -ne 0 ]; then
  echo "   *** ELEMENTS LOST at identification — fidelity is already compromised ***"
  degraded=1
fi

# ---- STAGE 2: representation -------------------------------------------------------------------
echo "-- stage 2: represent"
if ! (cd "$FRAMEWORK" && python3 main.py "$TABLE" "$DOC" "$IR") >/dev/null 2>&1; then
  echo "   FAILED: identification did not produce a representation" >&2
  rm -f "$IR" "$EMITLOG"
  # exit 1: hard fail — no usable IR / tree
  exit 1
fi
echo "   ir: $(wc -c <"$IR" | tr -d ' ') bytes"

# ---- STAGE 3: emission -------------------------------------------------------------------------
# Emitter stdout is CAPTURED, not discarded. It prints one OK/SUBST/EMPTY/THREW line per node, and
# that is the only place a per-node translator failure is stated. Gate A (stage 3d) reads it to tell
# "the translator threw on this element" apart from "nothing ever asked the translator about it" --
# two causes of the same missing model that need different fixes.
echo "-- stage 3: emit"
rm -rf "$OUT"
if ! dotnet "$EMITTER" $EMIT_FLAGS "$IR" "$OUT" "$DOC" >"$EMITLOG" 2>&1; then
  echo "   FAILED: emission produced no usable tree" >&2
  sed -n '1,40p' "$EMITLOG" >&2
  rm -f "$IR" "$EMITLOG"
  # exit 1: hard fail — emission produced no usable tree
  exit 1
fi
files=$(find "$OUT" -type f 2>/dev/null | wc -l | tr -d ' ')
models=$(find "$OUT" -name '*.sql' -path '*models*' 2>/dev/null | wc -l | tr -d ' ')
echo "   wrote: $files file(s), $models model(s)"
# THE EMITTER'S OWN ACCOUNT OF THE THREE NEW ARTIFACTS, echoed here because $EMITLOG is deleted at the
# end and these are the only lines that state the CAUSE when stage 4 later reports a zero. Stage 4
# still counts from the artifact, not from these lines — this is diagnosis, not the measurement.
sed -n '/^orchestration:/,$p' "$EMITLOG" \
  | grep -E "^orchestration|^  container|^  dbt dir|^orch sql|^lineage rows|^  lineage|^issue rows|^element rows|^  report|^  WARN" \
  | sed 's/^/   | /'

# ---- STAGE 3a: ETL.Elements metadata census ------------------------------------------------------
# The producer writes graph nodes (and not-in-graph Unsupported). Native ETL.Elements also
# carries N/A rows for Package/Path/ConnectionManager and Mapping/Workflow/Session. Those
# records are already in the identification census; Status=N/A keeps conversion-rate exclusions.
echo "-- stage 3a: ETL.Elements metadata census"
ELEMENTS_CENSUS=$(python3 "$HERE/etl_elements_census.py" "$TABLE" "$DOC" "$OUT" 2>&1) || true
printf '%s\n' "$ELEMENTS_CENSUS" | sed 's/^/   | /'
if ! printf '%s' "$ELEMENTS_CENSUS" | grep -q "metadata rows:"; then
  echo "   *** ETL.Elements metadata census did not run — graph rows are unchanged."
  degraded=1
fi

# ---- STAGE 3b: TIER 3 — fill what the engine could not render ------------------------------------
# Ordered deliberately BEFORE stage 4, not after. Stage 4 decides the verdict from the artifact, so
# running the fill first means the verdict describes what actually shipped. Running it after would
# report degradation the shipped tree no longer has.
#
# It cannot inflate the result: ai_fill only overwrites a model that already carries a blocking EWI
# or projects no columns, and it stamps every file it writes. Engine-rendered models are untouched.
echo "-- stage 3b: ai-fill (tier 3)"
# Verdict-line contract (same shape as issues/loss ledger): ai_fill ALWAYS prints
# `authoring : needed=<N> filled=<M>[ skipped=...]`, including the no-sidecar path.
# Without this, a missing sidecar returned early, the driver discarded stdout with
# `|| true`, and unaddressed degradation never raised degraded=1 from this stage.
AIFILL=$(python3 "$HERE/ai_fill.py" "$IR" "$DOC.ai.json" "$OUT" 2>&1) || true
printf '%s\n' "$AIFILL" | sed 's/^/   | /'
# needed>0 and filled=0 => authoring was required and nothing was written (no-sidecar
# or empty ModelSql). needed=0 and filled=0 is a clean no-op — do NOT treat as degrade.
if printf '%s\n' "$AIFILL" | grep -qE 'authoring[[:space:]]*:[[:space:]]*needed=[1-9][0-9]*[[:space:]]+filled=0'; then
  echo "   *** AUTHORING UNFILLED — degraded models remain and stage 3b wrote none."
  echo "       (Typical cause: no sidecar / skipped=no-sidecar. Not a claim that AI ran.)"
  degraded=1
fi

# ---- STAGE 3c: declare the sources the models reference ------------------------------------------
# One missing declaration was the difference between a tree that parses and one that does not.
# MEASURED: `dbt parse` on an emitted Pentaho tree failed with exactly ONE error --
# "Source 'raw.CUSTOMER' not found in project" -- and everything else parsed clean.
echo "-- stage 3c: declare sources"
for proj in $(find "$OUT" -name 'dbt_project.yml' -exec dirname {} \; 2>/dev/null); do
  python3 "$HERE/emit_sources_yml.py" "$proj" || true
done

# ---- STAGE 3c2: RE-EMIT LINEAGE OVER THE TREE THAT ACTUALLY SHIPPED ----------------------------
# NAMED 3c2 AND NOT 3e SO THE PRINTED ORDER MATCHES THE EXECUTION ORDER. It runs between 3c and 3d,
# and a label that sorts after 3d while printing before it is the kind of small inconsistency that
# makes a log unreadable when two people are reading it for different reasons.
# WHY THIS STAGE EXISTS, MEASURED. The Pentaho tree contains `stg_raw__read_customer` with a live
# `source('raw','CUSTOMER')` call and there was NO ObjectReferences row for it. The emitter builds
# lineage from the IR, and `ai_fill.py` writes tier-3 model bodies at stage 3b -- AFTER the emitter
# ran -- so every model-authored artifact was absent from the graph it belongs to. Lineage described
# the tree the emitter INTENDED, not the tree on disk.
#
# It is a second pass and not a reordering because the two orderings are mutually exclusive: ai_fill
# decides what to fill by reading the emitted tree, so it cannot run first. LINEAGE ONLY -- ETL.Issues
# and ETL.Elements come from what the engine's translators registered during translation, and
# re-running them from a process that did no translation would replace two populated reports with
# placeholders.
#
# Ordered BEFORE stage 4, which counts ObjectReferences rows out of the artifact.
echo "-- stage 3c2: re-emit lineage over the filled tree"
RELINEAGE=$(dotnet "$EMITTER" --relineage "$IR" "$OUT" "$DOC" 2>&1)
RELINEAGE_RC=$?
printf '%s\n' "$RELINEAGE" | grep -E "^lineage rows|^  lineage|^  report|^  WARN" | sed 's/^/   /'
if [ $RELINEAGE_RC -ne 0 ]; then
  # NOT exit 1: the tree and its models are unaffected. What is stale is one report, and stage 4
  # counts that report from the artifact, so the consequence is measured there rather than asserted
  # here. Same wording discipline as COVERAGE UNMEASURED.
  echo "   *** LINEAGE NOT RE-EMITTED — the shipped tree's own edges were not re-read, so any"
  echo "       model-authored model is missing from ObjectReferences. The rows from stage 3 are"
  echo "       still there; they describe the tree BEFORE the tier-3 fill."
  printf '%s\n' "$RELINEAGE" | sed -n '1,10p' | sed 's/^/   | /'
  degraded=1
fi

# C# --relineage only adds SourceQualifier.TableName and ref()/source() in
# SSC-AI-AUTHORED models. Table-refused Execute SQL Tasks carry the statement
# on SqlStatementSource / source_sql and often author a bare FROM or CALL.
# Without this pass, ssis-execsql ObjectReferences stays the one-line placeholder.
echo "-- stage 3c2b: source_sql ObjectReferences"
SRC_SQL=$(python3 "$HERE/source_sql.py" "$IR" "$OUT" "$DOC" 2>&1)
SRC_SQL_RC=$?
printf '%s\n' "$SRC_SQL" | sed 's/^/   /'
if [ $SRC_SQL_RC -ne 0 ]; then
  # SAME SHAPE AS STAGE 3c2's OWN FAILURE, above: merge_object_references rewrites
  # ObjectReferences.*.csv wholesale, so a failure here can leave it stale or truncated
  # while stage 4 still counts rows out of the artifact.
  echo "   *** SOURCE-SQL LINEAGE NOT MERGED — the refused-task ObjectReferences rows this"
  echo "       stage exists to add may be missing; pre-existing rows from stage 3/3c2 keep"
  echo "       the report non-empty."
  degraded=1
fi

# ---- STAGE 3d: GATE A — does the output COVER the input? -----------------------------------------
# ON THE PATH, and that placement is the point. findings/37 recorded that this project's earlier
# gates were side scripts nobody was obliged to run; the loss ledger in stage 1 was moved onto the
# path for the same reason. A gate off the path is not a gate.
#
# WHY IT IS A SEPARATE QUESTION FROM STAGE 1. The stage-1 ledger's ELEMENT denominator is the
# identification sweep's own output, so an element the sweep never declared cannot be reported as
# lost. RE-MEASURED on this DataStage document under the current census (the number recorded here
# before was `declared=4 identified=4 lost=0 balances=True`, and `declared` has since been
# redefined, so that literal no longer reproduces):
#   gateA-fixtures/CustomerSummaryDerive_NoTransformer.dsx
#     records=41 level_matched=4 keyless=0 identified=4 excluded=36 unknown=1 lost=0 balances=True
# FOUR elements identified over a file holding FIVE, with the Transformer stage -- the one holding
# every derivation in the job -- absent from the IR and from the element ledger's own denominator.
# The census makes the gap VISIBLE now (it is the `unknown=1`), which strengthens the argument
# rather than weakening it: the sweep still does not produce an element for it, so the coverage
# question is still unanswered by stage 1. Gate A counts the source document itself, by a rule it
# prints, and never calls identify.py. That independence is the whole mechanism.
#
# Ordered AFTER 3b/3c for the reason stage 3b gives: the verdict must describe what actually shipped.
echo "-- stage 3d: gate A, DETERMINISTIC half (source-element coverage)"
COVERAGE=$(python3 "$HERE/coverage_gate.py" "$TABLE" "$DOC" "$IR" "$OUT" --emit-log "$EMITLOG" 2>&1)
COVERAGE_RC=$?
printf '%s\n' "$COVERAGE" | sed 's/^/   /'
# Same disambiguation the loss ledger needed, for the same reason: "the gate ran and found a hole"
# and "the gate could not run" are opposite claims and the exit code alone cannot tell them apart.
# A real verdict always contains a "coverage      :" line.
if ! printf '%s' "$COVERAGE" | grep -q "^ coverage      :"; then
  # NOT exit 1. The tree exists and may be perfectly good; what is missing is the CHECK. Reporting
  # unmeasured coverage as a failed migration would be as false as reporting it as a clean one, and
  # exit 3 already means "output exists, not trustworthy" -- which is exactly the state.
  echo "   *** COVERAGE UNMEASURED — Gate A could not run on this document. This is NOT a claim"
  echo "       that elements were lost, and NOT a claim that they were not. Cause above."
  degraded=1
elif [ $COVERAGE_RC -ne 0 ]; then
  echo "   *** SOURCE ELEMENTS WITH NO MODEL — the output does not cover the input ***"
  degraded=1
fi

# ---- STAGE 3e: GATE A, JUDGEMENT half — is something in the DOCUMENT missing from the IR? --------
# THE OTHER HALF OF THE SAME GATE, and the reason it exists is a measured hole in the half above.
# 3d's denominator is a RULE: it asks, for every element the table's own queries matched, whether the
# IR carries it. A record no rule reads cannot appear in that denominator, so 3d reported
# `coverage complete, exit 0` on a DataStage document whose `CTransformerStage` -- the stage holding
# every derivation in the job -- had no IR node and no model. This half asks the question a rule
# structurally cannot: is there something in this file that MATTERS and is not in the IR? That is a
# reading task, so it is a model call, and it is scored against criteria fixed before it first ran
# (findings/47).
#
# WHY IT IS ORDERED HERE. It CONSUMES 3d's report (embedded in the bundle verbatim as evidence, so the
# judgement half can tell "the translator threw" from "nothing ever asked") and the IR, and it must
# run before stage 4 for the same reason 3b does: the verdict has to describe what actually shipped.
#
# THE BUNDLE DIRECTORY IS OUTSIDE $OUT, AND THAT IS NOT TIDINESS. Gate A stages the document, the
# table, the IR and 3d's report; Gate B stages THE WHOLE EMITTED PROJECT. Inside $OUT those copies
# would be counted a second time by every stage-4 grep -- models, EWI markers, MODEL-AUTHORED headers,
# lineage rows -- so the artifact gates would score the bundle as if it were output. It also has to
# SURVIVE, because it holds the sidecar and the loop record, and `rm -rf "$OUT"` at stage 3 does not
# spare subdirectories.
# (`GATE_BUNDLES` itself is now assigned once, above the --inspect-only block, because stage 4d needs
# it in both modes. This line is deliberately left as a no-op re-assignment of the same expression so
# that the paragraph above still sits beside the definition it explains.)
GATE_BUNDLES="${AIFIRST_GATE_BUNDLES:-$OUT.gates}"
mkdir -p "$GATE_BUNDLES"
# THE ONE THING THIS STAGE CANNOT SUPPLY ITSELF. `--verifier-cmd` is a SHELL COMMAND on purpose, so a
# CLI, an HTTP call or a sub-agent are interchangeable at the seam; the gate never learns which it got.
# With none configured the gate exits 1 and is reported UNMEASURED -- deliberately, and not as a pass.
# An unrun gate reported as clean is the defect this project keeps finding, and `claude` is not on PATH
# on this machine, so the default below is a path and not a bare name.
# BUILT IN TWO STEPS, AND THE NEGATIVE TEST IS THE ONLY REASON THIS IS NOT ONE LINE. Written as
# `${AIFIRST_GATEA_VERIFIER_CMD-python3 ... --bundle {bundle} --verdict {verdict} ...}`, bash ENDS the
# parameter expansion at the first `}` -- the one closing `{bundle}` -- so the default was truncated
# mid-flag and the remainder became literal text appended to it. Measured: with the variable set to
# empty (the UNMEASURED negative test) the gate still received ` --verdict <path> --verifier-timeout
# 1800}`, ran it, and reported `/bin/sh: --verdict: command not found`. The gate's UNMEASURED report
# was right for the wrong reason, which is the failure mode where a negative test passes and the
# mechanism it was testing is broken.
GATEA_VERIFIER_DEFAULT="python3 -u $HERE/gate_a.py verifier --bundle {bundle} --verdict {verdict} --verifier-timeout 1800"
GATEB_VERIFIER_DEFAULT="python3 -u $HERE/gate_b.py verifier --bundle {bundle} --verdict {verdict} --verifier-timeout 1800"
if [ -n "${AIFIRST_VERIFIER_CLI:-}" ]; then
  GATEA_VERIFIER_DEFAULT="$GATEA_VERIFIER_DEFAULT --cli $AIFIRST_VERIFIER_CLI"
  GATEB_VERIFIER_DEFAULT="$GATEB_VERIFIER_DEFAULT --cli $AIFIRST_VERIFIER_CLI"
fi
# `-` and not `:-`: set-but-empty means "deliberately no verifier", which the gate reports as
# UNMEASURED. Unset means "use the default".
GATEA_VERIFIER="${AIFIRST_GATEA_VERIFIER_CMD-$GATEA_VERIFIER_DEFAULT}"
# THE CONVERGENCE LOOP IS ON, AND THE BOUND IS A KNOB BECAUSE THE MEASUREMENT NEEDS BOTH ARMS.
# Before this, stage 3e passed `--max-iterations 3` to a `run` that made exactly ONE pass -- so the
# bound was advertised and never used, and 6 of 10 gate runs stopped `OPEN` at iteration 1 of 3 with
# obligations a second pass was permitted to discharge and never asked to.
#
# WHY THE KNOB, AND NOT A HARD 3. "What does the loop change" is only answerable by running the same
# code with the loop off, so `AIFIRST_GATEA_MAX_ITERATIONS=1` is a supported setting rather than a code
# edit. It is also the honest fallback if the loop is ever found to be pressuring the verifier: the
# single-pass arm stays one environment variable away.
GATEA_MAX_ITER="${AIFIRST_GATEA_MAX_ITERATIONS:-3}"
echo "-- stage 3e: gate A, JUDGEMENT half (a model reads the document against the IR)"
# Real workloads cannot fit a whole gate in one verifier call. Batching + bounded parallelism is the
# default; `run` is retained only as an explicit diagnostic/control arm.
GATEA_MODE="${AIFIRST_GATEA_MODE:-batched-run}"
if [ "$GATEA_MODE" = "batched-run" ]; then
  # batched-run drives the model CLI itself (--cli), not an external --verifier-cmd.
  GATEA_BATCH_ARGS=()
  if [ -n "${AIFIRST_GATEA_BATCH_SIZE:-}" ]; then
    GATEA_BATCH_ARGS+=(--batch-size "$AIFIRST_GATEA_BATCH_SIZE")
  fi
  GATEA_CLI="${AIFIRST_VERIFIER_CLI:-claude}"
  GATEA=$(python3 -u "$HERE/gate_a.py" batched-run "$TABLE" "$DOC" "$IR" "$OUT" \
            --bundle "$GATE_BUNDLES/gateA" --emit-log "$EMITLOG" \
            --cli "$GATEA_CLI" --verifier-timeout 900 \
            --parallelism "${AIFIRST_GATE_PARALLELISM:-4}" \
            ${GATEA_BATCH_ARGS[@]+"${GATEA_BATCH_ARGS[@]}"} 2>&1)
else
  GATEA=$(python3 -u "$HERE/gate_a.py" run "$TABLE" "$DOC" "$IR" "$OUT" \
            --bundle "$GATE_BUNDLES/gateA" --emit-log "$EMITLOG" \
            --verifier-cmd "$GATEA_VERIFIER" --max-iterations "$GATEA_MAX_ITER" 2>&1)
fi
GATEA_RC=$?
printf '%s\n' "$GATEA" | sed 's/^/   /'
# THE SAME DISAMBIGUATION STAGES 1, 3d AND 5 ALREADY DO, BY STDOUT SHAPE AND NOT BY EXIT CODE.
# "the gate ran and found obligations outstanding" and "the gate could not run" are OPPOSITE claims,
# and one integer cannot carry both. A real Gate A verdict always prints a " ledger        :" line.
#
# THE LOOP ADDS A THIRD AND A FOURTH STATE, and both are checked BEFORE the ledger line, because by the
# time either happens a ledger line has already been printed and would otherwise be read as final:
#
#   DENOMINATOR DRIFT  the raised set moved between iterations of one run. Obligations are raised
#                      deterministically from the document, so this is a GATE DEFECT or a moving input,
#                      and every ledger in the run is measuring a different question. UNMEASURED.
#   LOOP ABORTED       an iteration after the first could not run. The last complete iteration's
#                      ledger stands and is reported; what is unmeasured is CONVERGENCE. Reported as
#                      the ledger says, plus a line saying the loop did not finish.
if printf '%s' "$GATEA" | grep -q "GATE A DEFECT: DENOMINATOR DRIFT"; then
  echo "   *** IR COMPLETENESS UNMEASURED — Gate A's DENOMINATOR MOVED between iterations of one run."
  echo "       Obligations are raised deterministically from the document before any verifier runs, so"
  echo "       the raised set must be identical every iteration. It was not, which makes each ledger"
  echo "       above a different question and any fall in outstanding arithmetic rather than"
  echo "       convergence. This is a defect in the gate or a moving input, NOT a finding about the"
  echo "       document, and it is not a claim either way about representation. Detail above."
  degraded=1
elif ! printf '%s' "$GATEA" | grep -q "^ ledger        :"; then
  # NOT exit 1. The tree exists and may be perfectly good; what is missing is the JUDGEMENT. Reporting
  # an unrun gate as a failed migration would be as false as reporting it as a clean one.
  echo "   *** IR COMPLETENESS UNMEASURED — Gate A's judgement half could not run on this document."
  echo "       This is NOT a claim that the document is fully represented, and NOT a claim that it"
  echo "       is not. No verifier configured, or the verifier produced no usable verdict. Cause"
  echo "       above. Set AIFIRST_GATEA_VERIFIER_CMD (it receives {bundle} and must write {verdict})."
  degraded=1
else
  if printf '%s' "$GATEA" | grep -q "GATE A LOOP ABORTED"; then
    echo "   *** GATE A CONVERGENCE UNMEASURED — the loop stopped part-way through. The last complete"
    echo "       iteration's ledger above was scored in full and stands; what this run cannot say is"
    echo "       whether a further pass would have closed the outstanding list. Cause above."
    degraded=1
  fi
  if [ $GATEA_RC -ne 0 ]; then
    echo "   *** OBLIGATIONS OUTSTANDING — the IR does not provably account for everything this"
    echo "       document states. The unresolved list is above and in $GATE_BUNDLES/gateA."
    degraded=1
  elif printf '%s' "$GATEA" | grep -q "CONVERGED ON ITERATION [2-9], NOT ON ITERATION 1"; then
    # A CLEAN LEDGER THAT TOOK MORE THAN ONE PASS IS NOT THE SAME RESULT AS ONE THAT WAS CLEAN
    # IMMEDIATELY, and exit 0 says the same thing about both. Earlier passes of the SAME verifier over
    # the SAME bundle left obligations outstanding that this one discharged, so at least one pass was
    # wrong and nothing here establishes which. That is an instability in the judgement, and this
    # driver's channel for "the run completed and something about it is not trustworthy" is `degraded`.
    #
    # DELIBERATELY NOT SILENT AND DELIBERATELY NOT A FAILURE. Collapsing it into the clean exit 0 is
    # the smoothing this gate exists to refuse; treating it as element loss would overstate it.
    echo "   *** GATE A CONVERGED LATE — every obligation is discharged, and it took more than one"
    echo "       pass. An earlier pass of the same verifier over the same bundle disagreed with the"
    echo "       one that closed it, so the judgement is unstable even though the ledger is clean."
    echo "       A run clean on iteration 1 is a stronger result than this one; see the loop record"
    echo "       in $GATE_BUNDLES/gateA/gateA-loop-run.json for the flip direction per family."
    degraded=1
  fi
fi

# ---- STAGE 3e2: GATE B — does the generated SQL DO what the source element says? ------------------
# NAMED 3e2 AND NOT 3f SO THE PRINTED ORDER MATCHES THE EXECUTION ORDER, the same convention 3c2 uses.
#
# A DIFFERENT QUESTION FROM EVERY GATE ABOVE, and the measured proof that it cannot be a rule: the
# SSIS and the Informatica derive models both contain the BYTE-IDENTICAL string
# `FirstName || ' ' || MiddleName || ' ' || LastName AS FullName`, and one of them is wrong. SSIS `+`
# propagates NULL and so does Snowflake `||`; Informatica `||` does NOT, so the same generated line
# silently turns a name with a NULL middle name into NULL. No diff, linter, parser or compile step can
# separate those two, because there is nothing structurally different about them. The discriminator is
# the semantics of the platform each came from, which is a reading task.
#
# ORDERED AFTER 3e because it is the next question in the same direction -- 3e asks whether the IR
# carries what the document states, this asks whether the SQL DOES what it states -- and BEFORE stage
# 4 for the reason above: its bundle holds a copy of the whole emitted project.
GATEB_VERIFIER="${AIFIRST_GATEB_VERIFIER_CMD-$GATEB_VERIFIER_DEFAULT}"
echo "-- stage 3e2: gate B (intent parity — a model reads the SQL against the source element)"
# No dialect reference sheet ships with this action. Default to the self-contained arm; callers
# that provide a sheet can still opt into sourced explicitly.
GATEB_ARM="${AIFIRST_GATEB_ARM:-naive}"
GATEB_MODE="${AIFIRST_GATEB_MODE:-batched-run}"
if [ "$GATEB_MODE" = "batched-run" ]; then
  GATEB=$(python3 -u "$HERE/gate_b.py" batched-run "$DOC" "$OUT"             --bundle "$GATE_BUNDLES/gateB" --arm "$GATEB_ARM"             --platform "$TABLE_PLATFORM"             --cli "${AIFIRST_VERIFIER_CLI:-claude}" --verifier-timeout 900             --parallelism "${AIFIRST_GATE_PARALLELISM:-4}"             --expression-batch-size "${AIFIRST_GATEB_EXPRESSION_BATCH_SIZE:-8}"             --model-batch-size "${AIFIRST_GATEB_MODEL_BATCH_SIZE:-12}" 2>&1)
else
  GATEB=$(python3 -u "$HERE/gate_b.py" run "$DOC" "$OUT"             --bundle "$GATE_BUNDLES/gateB" --arm "$GATEB_ARM"             --platform "$TABLE_PLATFORM"             --verifier-cmd "$GATEB_VERIFIER" --max-iterations 3 2>&1)
fi
GATEB_RC=$?
printf '%s\n' "$GATEB" | sed 's/^/   /'
if ! printf '%s' "$GATEB" | grep -q "^ ledger        :"; then
  echo "   *** INTENT PARITY UNMEASURED — Gate B could not run on this tree. This is NOT a claim"
  echo "       that the generated SQL does what the document says, and NOT a claim that it does"
  echo "       not. No verifier configured, no emitted project, or no usable verdict. Cause above."
  echo "       Set AIFIRST_GATEB_VERIFIER_CMD (it receives {bundle} and must write {verdict})."
  degraded=1
elif [ $GATEB_RC -ne 0 ]; then
  echo "   *** INTENT PARITY NOT ESTABLISHED — obligations outstanding: a generated column whose"
  echo "       behaviour differs from the source element on a stated input, or one nothing could"
  echo "       verify. NOT a claim the tree fails to run; three of four trees run and diverge."
  degraded=1
fi
# ---- STASH THE REPRESENTATION FOR STAGE 4d --------------------------------------------------------
# `rm -f "$IR"` at the end of this script deletes the only copy of the representation, and stage 4d's
# whole question is "did the IR reach the dbt". Copied here, at the end of the generating block, so
# the stash is the representation the tree was ACTUALLY emitted from and not one regenerated later
# from possibly-changed inputs -- which is the stale-bundle hazard `table_is_current` exists for.
mkdir -p "$(dirname "$INTEGRITY_IR")"
cp "$IR" "$INTEGRITY_IR" 2>/dev/null || true

fi  # end of the stages-1-to-3d block skipped by --inspect-only

# ---- STAGE 4: post-flight — is the ARTIFACT trustworthy? ---------------------------------------
# Distinct from "did it run". Counts the engine's own honest-degradation markers plus our producer
# sentinel. A tree full of !!!RESOLVE EWI!!! is a successful run and an untrustworthy artifact.
echo "-- stage 4: inspect artifact"
ewis=$(grep -rl "!!!RESOLVE EWI!!!" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
sentinels=$(grep -rl "__PRODUCER_EXPRESSION_NOT_CONVERTED__" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
# TIER-3 FILLS ARE A DEGRADATION SIGNAL, and this line was missing on the first run of the
# ladder — which produced exactly the defect this project keeps cataloguing, in the stage
# written to prevent it. Three of four Pentaho models were MODEL-AUTHORED and UNVERIFIED, and
# because ai_fill legitimately clears the other three signals (no EWI, no sentinel, columns
# present), the verdict came out "no degradation detected (exit 0)".
#
# A tier-3 model is SQL that nothing in this stage has checked against source behaviour — or
# against a parser, or against a warehouse. That is the textbook meaning of exit 3: output exists
# and is not trustworthy. Counting it as
# clean would make the ladder a way to launder unverified output into a green result — strictly
# worse than the placeholder it replaced, because a placeholder is obviously incomplete.
#
# DELIBERATELY NOT CALLED "RUNNABLE". ai_fill's stamp used to say so and it was measured false (the
# Pentaho fill referenced a source no sources.yml declared and `dbt compile` failed). Whether the
# tree runs is asked below, once, by dbt itself — not asserted here by a grep that counts files.
authored=$(grep -rl "SSC-AI-AUTHORED" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
# TIER 2 WAS INVISIBLE HERE, AND THE UNDERCOUNT WAS MEASURED.
#
# This line counted `SSC-AI-AUTHORED` only, which is TIER 3 -- a model wrote the whole model body.
# TIER 2 is a model supplying the PAYLOAD (an expression, a predicate, an element kind) that the
# ENGINE's translators then render, and it shipped with no marker at all. MEASURED on
# poc/blind-run/runU/pentaho: `int_derive_fullname_and_birthyear.sql` carried
# `FirstName || ' ' || MiddleName || ' ' || LastName AS FullName` and `YEAR(BirthDate) AS BirthYear`,
# both authored by a model from Java the .ktr states, and this stage reported
# `MODEL-AUTHORED (unverified) : 2` for a tree in which 3 of 4 models hold model-authored content.
#
# COUNTED SEPARATELY, NOT ADDED TOGETHER, because the two are different fidelity positions: tier 2
# has been through the engine's translators and its writers, tier 3 has not. Collapsing them into one
# number would lose the distinction the marker exists to record. BOTH feed the degradation verdict,
# because in neither case has anything compared the SQL against source behaviour.
#
# A file can only be one of the two: ai_fill overwrites a tier-2-stamped file when it replaces the
# body, so its tier-3 header is the only one left. Measured on Pentaho: `Filter BirthYear` is tier 2
# for its predicate and tier 3 after FilterTranslator threw, and its file carries tier 3 alone.
assisted=$(grep -rl "SSC-AI-ASSISTED" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
# A model has columns if ANYTHING sits between SELECT and FROM. The first version of this test looked
# for ` AS ` or `*`, which counted a perfectly good staging model as column-less: a source projection
# emits bare column names with no aliases. That was a FALSE POSITIVE in the degradation detector — it
# reported SSIS as degraded when SSIS was fine. A gate that cries wolf is as bad as one that sleeps.
#
# AND IT CRIED WOLF A SECOND TIME, FOR A SECOND REASON, MEASURED THE DAY THE SIDECARS BECAME
# MODEL-AUTHORED. The check was `sed -n '/^SELECT$/,/^FROM$/p'`, which needs `SELECT` and `FROM`
# UPPERCASE and alone on a line. Every engine translator emits uppercase, so it never fired. A model
# writes `select` / `from`; the sed range then never matches, the extracted body is empty, and a
# correct six-column model is counted column-less. Verified by uppercasing the same file and watching
# the check pass.
#
# THE PART THAT MAKES IT A DEFECT AND NOT A ROUGH EDGE: `ai_fill.is_degraded` asks the same question
# over the same bytes with `re.I` and answers `is_degraded=False`. Two implementations of "does this
# model project columns" disagreed, and the driver's — the one that decides the exit code — was the
# wrong one. So this is now ONE regex, the same one ai_fill uses (`^\s*SELECT\s*$ ... ^\s*FROM\s*$`,
# case-insensitive, EVERY pair and not just the first, because a correct CTE once masked a column-less
# outer projection). Python and not sed because BSD sed has no case-insensitive address.
empty=$(python3 - "$OUT" <<'PY'
import os, re, sys
PRUNE = {"dbt_internal_packages", "target"}
n = 0
for base, dirs, files in os.walk(sys.argv[1]):
    dirs[:] = [d for d in dirs if d not in PRUNE]
    if "models" not in base.split(os.sep):
        continue
    for f in files:
        if not f.endswith(".sql"):
            continue
        try:
            sql = open(os.path.join(base, f), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        # Mirrors ai_fill.is_degraded's column half EXACTLY, minus the EWI signal, which stage 4
        # counts separately as `ewis`.
        bodies = re.findall(r"^\s*SELECT\s*$(.*?)^\s*FROM\s*$", sql, re.S | re.M | re.I)
        tail = sql.rstrip().rsplit("\n", 1)[-1].strip().upper()
        if any(not b.strip() for b in bodies) or tail in ("SELECT", "FROM"):
            n += 1
print(n)
PY
)
echo "   files with blocking EWI      : $ewis"
echo "   files with producer sentinel : $sentinels"
echo "   models with NO columns       : $empty"
echo "   MODEL-AUTHORED (unverified)  : $authored   [tier 3: a model wrote the whole model body]"
echo "   MODEL-ASSISTED (unverified)  : $assisted   [tier 2: the engine rendered it from a model-supplied payload]"

# ---- SNOW-3979042 Phase 1c: MARKER/REPORT RECONCILIATION -----------------------------------------
# SOURCED FROM $EMITLOG RATHER THAN RE-DERIVED FROM DISK, and that is a deliberate departure from
# the rest of this stage's "count from the artifact" rule, not an oversight of it. The other counts
# above (ewis, sentinels, empty, authored, assisted) are things this script can re-derive itself
# with a plain grep because the signal IS the artifact. This check cannot be re-derived that way: it
# needs the same stem -> element-id match ProducerReports.cs already computes for lineage
# (ResolveStem's ambiguity-broken-by-shortest-match rule) plus the in-memory registration list
# (issuesByComponent) behind ETL.Elements/ETL.Issues, neither of which survives into the CSVs on
# disk. Re-implementing that match rule here in bash/python would be a SECOND, independently-drifting
# copy of the same fuzzy heuristic -- exactly the "two sources of truth for one fact" ProducerReports
# already avoids for ETL.Issues by having the report loop itself record what it kept. Trusting the
# emitter's own "RECONCILE FAIL" lines here is therefore the same trust this driver already extends
# to $EMITLOG elsewhere on this path (coverage_gate.py and gate A both take --emit-log "$EMITLOG"),
# not a new adjacent-verification trap.
reconcile_line=$(grep -E "^reconcile   :" "$EMITLOG" | tail -1)
[ -n "$reconcile_line" ] && echo "   $reconcile_line"
reconcile_fails=$(grep -c "RECONCILE FAIL" "$EMITLOG" 2>/dev/null || true)
reconcile_fails=${reconcile_fails:-0}
if [ "$reconcile_fails" != "0" ]; then
  echo "   *** MARKER/REPORT MISMATCH — $reconcile_fails inline !!!RESOLVE EWI!!! marker(s) do not"
  echo "       reconcile against ETL.Elements.NA.csv / ETL.Issues.NA.csv for their element. The"
  echo "       marker is truth; see the RECONCILE FAIL lines below for which report has not caught up."
  grep "RECONCILE FAIL" "$EMITLOG" | sed 's/^/   | /'
  degraded=1
fi

# ---- STAGE 4b: THE THREE FEATURES NOTHING WAS COUNTING ------------------------------------------
# WHY THESE ARE HERE. Measured on the four runS trees: 186 files each, and ZERO lineage rows, ZERO
# report/assessment artifacts, and TWO EWI instances across all four trees combined. dbt models had
# four gates; these three had none, and a feature with no gate is a feature nobody notices is missing.
# That is this project's own "a gate off the path is not a gate" finding, applied to itself.
#
# EACH IS COUNTED FROM THE ARTIFACT, not from the emitter's stdout. The emitter prints these numbers
# too, but the emitter is the thing under test: reading its own claim back would be the
# adjacent-verification trap this project keeps walking into. `Reports/` is where a real SnowConvert
# run puts them (measured: poc/blind-run/runA/*/out/Reports).

REPORTS_DIR="$OUT/Reports"

# --- lineage. The header line is not a row, and an empty inventory writes a ONE-LINE PLACEHOLDER
# ("No object references found") which is a successful write of nothing. Both cases must read as zero.
lineage_rows=0
lineage_file=$(find "$REPORTS_DIR" -name 'ObjectReferences.*.csv' 2>/dev/null | head -1)
if [ -n "$lineage_file" ]; then
  # Count only lines that look like data: contain a comma AND are not the header.
  # NOT `grep -c ',' || echo 0`: `grep -c` PRINTS 0 and EXITS 1 on no match, so the `||` appends a
  # second 0 and the variable becomes the two-line string "0\n0", which then fails `[` with
  # "integer expression expected" — measured, on the Informatica tree, in the first run of this gate.
  lineage_rows=$( { grep -c ',' "$lineage_file" 2>/dev/null || true; } | head -1)
  lineage_rows=${lineage_rows:-0}
  lineage_rows=$((lineage_rows > 0 ? lineage_rows - 1 : 0))
fi
echo "   ETL LINEAGE rows             : $lineage_rows"

# --- report/assessment artifacts. Counted as POPULATED, not as present: a placeholder file is the
# exact failure mode this gate exists to catch, and it is indistinguishable from a real report by
# `test -f`. A report is populated when it has a header plus at least one comma-bearing data line.
reports_present=0
reports_populated=0
reports_placeholder=0
if [ -d "$REPORTS_DIR" ]; then
  for r in "$REPORTS_DIR"/*.csv "$REPORTS_DIR"/*.json; do
    [ -f "$r" ] || continue
    reports_present=$((reports_present + 1))
    rows=$( { grep -c ',' "$r" 2>/dev/null || true; } | head -1)
    rows=${rows:-0}
    if [ "$rows" -gt 1 ]; then
      reports_populated=$((reports_populated + 1))
    else
      reports_placeholder=$((reports_placeholder + 1))
    fi
  done
fi
# A placeholder is REPORTED but not itself a degradation: "No ETL issues to report" on a document
# with no issues is the truth. Only ALL of them being placeholders means the reporting side is dead.
echo "   REPORT artifacts             : $reports_populated populated, $reports_placeholder placeholder, of $reports_present present"

# --- total EWI/FDM. Distinct from the "files with blocking EWI" count above, which counts FILES and
# only the blocking marker. This counts every issue INSTANCE of either kind, in the models and in the
# issues report. See findings/47 for why the number is small and why it is not padded: the engine's
# not-supported vocabulary has exactly two members and both are platform-named (ENG-017), so a third
# platform cannot emit an honest one and the count is CAPPED, not suppressed.
ewi_instances=$(grep -roh "SSC-EWI-[A-Z0-9]*" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
fdm_instances=$(grep -roh "SSC-FDM-[A-Z0-9]*" "$OUT" 2>/dev/null | wc -l | tr -d ' ')
issue_total=$((ewi_instances + fdm_instances))
echo "   EWI/FDM instances            : $issue_total ($ewi_instances EWI, $fdm_instances FDM)"

# --- STAGE 4c: does the ORCHESTRATION SQL name anything from the INPUT DOCUMENT? -----------------
# THE DEFECT THIS CATCHES, MEASURED. Every one of the four runS trees emitted a BYTE-IDENTICAL
# orchestration file (md5 eb7f92d6f569a48a1d15008ef5781521) at
# Output/ETL/DerivedColumn/DerivedColumn.sql, whose body reads
# `---- Start block 'Package\Data Flow Task'` and `EXECUTE DBT PROJECT public.Data_Flow_Task`.
# `Package\Data Flow Task` is an SSIS control-flow path; `DerivedColumn` is an SSIS component name.
# A DataStage DSJOB called CustomerSummaryDerive shipped that file, and so did a Pentaho
# transformation called customer_summary_fullname_birthyear. Neither name appeared in it.
#
# It passed every gate we had, because every gate asked about the DBT half. The stated goal weighs
# "Snowflake task graphs" equally with dbt, and the task-graph half was a constant.
#
# THE RULE, and it is deliberately weak: at least one token of the source document's own name must
# appear in the orchestration SQL. Weak because a strong rule would need a per-platform notion of
# what the unit of work is, and this driver must not acquire one silently. Weak is enough — a
# hardcoded constant passes NO version of this test.
orch_files=$(find "$OUT/Output/ETL" -maxdepth 2 -name '*.sql' 2>/dev/null | wc -l | tr -d ' ')
DOC_STEM=$(basename "$DOC"); DOC_STEM="${DOC_STEM%.*}"
# Tokens of 4+ chars, so that "m_" or "of" cannot match by accident.
DOC_TOKENS=$(printf '%s' "$DOC_STEM" | tr -cs 'A-Za-z0-9' '\n' | awk 'length($0)>=4')
DOC_TOKEN_COUNT=$(printf '%s\n' "$DOC_TOKENS" | grep -c '[^[:space:]]' || true)
# MAJORITY, not "at least one", AND THE NEGATIVE TEST IS WHY.
#
# The first version of this gate required ONE token of the document name to appear, and it PASSED when
# the old hardcoded constant was planted back into the SSIS tree. Cause: the constant is the string
# `DerivedColumn`, and the SSIS blind document is called
# `CustomerSummary_DerivedColumn_ConditionalSplit.dtsx` — the constant was named after this very
# document, so one of the three tokens matched by coincidence. A gate that a hardcoded constant passes
# is worth nothing, and only planting the constant back revealed it.
#
# Ceiling division: 1 of 1, 2 of 3, 2 of 4. The constant supplies 1 of 3 on SSIS and 0 on every other
# platform, so it fails everywhere now.
DOC_TOKENS_NEEDED=$(( (DOC_TOKEN_COUNT + 1) / 2 ))
orch_named=0
orch_dangling=0
# --- THE SIBLING REFERENCE THIS GATE WAS NOT CHECKING, AND THE DEFECT THAT PROVES IT MATTERED.
#
# `EXECUTE DBT PROJECT public.<x>` and `AFTER public.<y>` are the only two kinds of NAME a task graph
# emits, and only the first was checked. MEASURED on runZ0: our SSIS unit SQL was ONE statement,
#   CREATE OR REPLACE TASK public.customersummary_derivedcolumn_conditionalsplit_dft_load_customer_summary
#   ... AFTER public.customersummary_derivedcolumn_conditionalsplit
# and NOTHING in the tree created `public.customersummary_derivedcolumn_conditionalsplit`. The engine's
# own output for the same document creates it first, as a no-op `AS SELECT 1` root. So the file declared
# a child of a task that does not exist: `ALTER TASK ... RESUME` on it fails, and the graph can never
# run. It passed every gate here because the dbt-project name was right and nobody asked about the
# predecessor.
#
# TWO INDEPENDENT CONDITIONS, both structural — no vocabulary, no token guessing:
#   1. every `AFTER <schema>.<name>` must name a task some orchestration file in this tree CREATEs.
#      Resolved TREE-WIDE and not per file, because that is the real semantics: a Snowflake task is an
#      account-level object, so a predecessor created by any file in the migration satisfies the clause.
#   2. the tree must contain at least one ROOT task — a CREATE TASK with no AFTER. A graph in which
#      every task has a predecessor has no entry point regardless of whether the names resolve.
#
# COMPARED CASE-INSENSITIVELY because unquoted Snowflake identifiers are, and the two sides are
# produced by different code paths (`FormatRootTaskName` for the root, `GetPredecessorNames` for the
# child) — a gate that assumed they agreed on case would be testing the emitter's spelling, not the
# graph.
orch_after_refs=0
orch_after_dangling=0
orch_task_creates=0
orch_after_clauses=0
if [ "$orch_files" -gt 0 ]; then
  ORCH_SQL_FILES=$(find "$OUT/Output/ETL" -maxdepth 2 -name '*.sql' 2>/dev/null)
  ORCH_CREATED=$(grep -hoiE 'CREATE +(OR +REPLACE +)?TASK +[A-Za-z0-9_$]+\.[A-Za-z0-9_$]+' \
                   $ORCH_SQL_FILES 2>/dev/null \
                 | sed -E 's/^.*[Tt][Aa][Ss][Kk][[:space:]]+//' | tr '[:upper:]' '[:lower:]' | sort -u)
  orch_task_creates=$(printf '%s\n' "$ORCH_CREATED" | grep -c '[^[:space:]]' || true)
  for f in $(find "$OUT/Output/ETL" -maxdepth 2 -name '*.sql' 2>/dev/null); do
    hits=0
    for tok in $DOC_TOKENS; do
      if grep -qi -- "$tok" "$f"; then hits=$((hits + 1)); fi
    done
    [ "$hits" -ge "$DOC_TOKENS_NEEDED" ] && orch_named=$((orch_named + 1))

    # SECOND, INDEPENDENT CONDITION, AND THE ONLY NON-HEURISTIC ONE IN THIS GATE.
    # `EXECUTE DBT PROJECT public.<name>` has to name a dbt project that EXISTS beside the unit SQL.
    # No vocabulary, no token guessing: either the directory is there or the statement cannot run.
    # The old constant emitted `public.Data_Flow_Task` on all four platforms while the models lived in
    # `DFT_Load_Customer_Summary`, `CustomerSummaryDerive` and `customer_summary_fullname_birthyear`,
    # so it fails this one on every platform including SSIS -- which is what makes the pair of
    # conditions stronger than either alone.
    for proj in $(grep -o "EXECUTE DBT PROJECT [A-Za-z0-9_]*\.[A-Za-z0-9_]*" "$f" 2>/dev/null \
                  | sed 's/.*\.//'); do
      if [ ! -d "$(dirname "$f")/$proj" ]; then
        orch_dangling=$((orch_dangling + 1))
        echo "   dangling EXECUTE DBT PROJECT: '$proj' has no directory beside $(basename "$f")"
      fi
    done

    # THIRD CONDITION: the AFTER targets. `AFTER` must be followed by a QUALIFIED name for the match to
    # fire, which is what keeps English prose in a comment ("runs AFTER stage 4") out of the reference
    # list. A comma-separated predecessor list is one clause and several references, so the clause count
    # and the reference count are tracked separately -- the clause count is what gives the root count.
    #
    # `sed 's/[[:space:]]+//g'` AND NOT `tr -d '[:space:]'`, AND THE NEGATIVE TEST IS THE ONLY REASON
    # THIS LINE IS RIGHT. `tr` deletes the NEWLINES BETWEEN grep's matches too, so a file with two AFTER
    # clauses yielded ONE token: the first negative test (plant a second task whose AFTER names nothing)
    # reported the dangling reference as
    # `public.customersummary_derivedcolumn_conditionalsplitpublic.no_such_root` and counted `1
    # predecessor reference(s) examined` where there were two. The gate still FIRED -- a concatenation of
    # two names resolves to nothing -- so a positive-only test would have passed while the coverage
    # number it prints was false and a REAL second reference was never checked. sed is per-line.
    clauses=$(grep -coiE 'AFTER[[:space:]]+[A-Za-z0-9_$]+\.[A-Za-z0-9_$]+' "$f" 2>/dev/null || true)
    orch_after_clauses=$((orch_after_clauses + ${clauses:-0}))
    for ref in $(grep -hoiE 'AFTER[[:space:]]+[A-Za-z0-9_$]+\.[A-Za-z0-9_$]+([[:space:]]*,[[:space:]]*[A-Za-z0-9_$]+\.[A-Za-z0-9_$]+)*' "$f" 2>/dev/null \
                 | sed -E 's/^[Aa][Ff][Tt][Ee][Rr][[:space:]]+//' | sed -E 's/[[:space:]]+//g' | tr ',' '\n' \
                 | tr '[:upper:]' '[:lower:]' | grep '[^[:space:]]'); do
      orch_after_refs=$((orch_after_refs + 1))
      if ! printf '%s\n' "$ORCH_CREATED" | grep -qxF -- "$ref"; then
        orch_after_dangling=$((orch_after_dangling + 1))
        echo "   dangling AFTER: '$ref' in $(basename "$f") names a task NOTHING in this tree creates"
      fi
    done
  done
fi
echo "   orchestration SQL files      : $orch_files"
if [ "$orch_files" = "0" ]; then
  # NOT a SQL error and NOT a coverage hole. The tree has models and no task graph, which is exactly
  # what the emitter says when the IR names no orchestration container. Same wording discipline as
  # COVERAGE UNMEASURED: state the absence, claim nothing about what a present one would have said.
  echo "   *** TASK GRAPH ABSENT — no orchestration SQL was emitted for this document."
  echo "       The dbt half exists; the Snowflake-task half does not. This is NOT a claim that"
  echo "       one could not be built, and NOT a claim that the models are wrong."
  degraded=1
else
  echo "   orchestration names input    : $orch_named of $orch_files file(s) name >= $DOC_TOKENS_NEEDED of $DOC_TOKEN_COUNT token(s) of '$DOC_STEM'"
  if [ "$orch_named" != "$orch_files" ]; then
    echo "   *** TASK GRAPH DOES NOT NAME THE INPUT — $((orch_files - orch_named)) of $orch_files"
    echo "       orchestration file(s) name fewer than half the tokens of '$DOC_STEM'. A task graph"
    echo "       that names nothing from the source document is a constant, not a translation."
    degraded=1
  fi
  if [ "$orch_dangling" != "0" ]; then
    echo "   *** TASK GRAPH REFERENCES A PROJECT THAT IS NOT THERE — $orch_dangling dangling"
    echo "       EXECUTE DBT PROJECT statement(s). The task cannot run: it names a dbt project with"
    echo "       no directory. This is the shape a hardcoded orchestration constant always has."
    degraded=1
  fi
  # THE CHECK'S OWN COVERAGE, PRINTED WITH THE VERDICT. Same discipline as `models the SQL gate read`
  # in the dbt block below: "0 dangling" over 0 references examined and "0 dangling" over 3 are
  # opposite facts, and only the second is evidence. A tree whose AFTER clauses this gate never found
  # would otherwise read as a clean task graph.
  echo "   task graph refs              : $orch_task_creates task(s) created, $orch_after_clauses AFTER clause(s), $orch_after_refs predecessor reference(s) examined"
  if [ "$orch_after_dangling" != "0" ]; then
    echo "   *** TASK GRAPH AFTER TARGET MISSING — $orch_after_dangling of $orch_after_refs predecessor"
    echo "       reference(s) name a task nothing in this tree creates. The child task cannot be"
    echo "       resumed: ALTER TASK ... RESUME requires its predecessor to exist. NOT a claim that"
    echo "       the AFTER is wrong — the reference may be exactly right and its TARGET missing, which"
    echo "       is what this was on every platform before the root task was emitted."
    degraded=1
  fi
  if [ "$orch_task_creates" -gt 0 ] && [ "$orch_after_clauses" -ge "$orch_task_creates" ]; then
    echo "   *** TASK GRAPH HAS NO ROOT — $orch_task_creates task(s) created and $orch_after_clauses"
    echo "       carry an AFTER clause, so every task in this tree has a predecessor and the DAG has"
    echo "       no entry point. Snowflake's task-graph idiom is one root with no predecessor and"
    echo "       children hanging off it (measured against the engine's own output, runA). This fires"
    echo "       independently of whether the names resolve."
    degraded=1
  fi
fi

if [ "$lineage_rows" = "0" ]; then
  echo "   *** NO ETL LINEAGE — zero ObjectReferences rows. The dbt tree states its own edges as"
  echo "       ref() calls, but nothing downstream (impact analysis, the Code Unit Registry, the"
  echo "       assessment) can read them. NOT a claim that the models are wrong."
  degraded=1
fi
if [ "$reports_populated" = "0" ]; then
  echo "   *** NO REPORT/ASSESSMENT ARTIFACTS — $reports_present file(s) present, none with data"
  echo "       rows. A one-line placeholder CSV is a successful write of nothing, and reads"
  echo "       identically to 'there was nothing to report' unless the rows are counted."
  degraded=1
fi
if [ "$issue_total" = "0" ]; then
  echo "   *** DIAGNOSTIC CHANNEL EMPTY — not one EWI or FDM instance in the tree or the reports."
  echo "       This is reported as an ABSENCE, not as a defect in the models, and deliberately not"
  echo "       as a claim that the conversion was clean. MEASURED REFERENCE, the engine's own Run A"
  echo "       on these same two documents: SSIS 4 issue rows (4x SSC-EWI-SSIS0009, one per"
  echo "       component), Informatica 0. So a small number here is not automatically wrong — but a"
  echo "       ZERO means nothing in this path flagged anything, and the size of that hole is what"
  echo "       the replacement issue framework has to fill. Do not close this by adding codes: the"
  echo "       engine's not-supported vocabulary has exactly two members and both are"
  echo "       platform-named (ENG-017), so a third platform cannot emit an honest one."
  degraded=1
fi

# THE ONLY NON-HEURISTIC SIGNAL IN THIS STAGE. Every check above is a grep I invented; this one
# asks a real SQL parser.
#
# IT MUST BE `compile`, NOT `parse`, AND THIS WAS MEASURED THE WRONG WAY FIRST.
# The first version ran `dbt parse` and reported 0 failures on ALL FOUR platforms -- including
# trees whose models begin with `!!!RESOLVE EWI!!!` and end on a dangling `FROM`. `parse` resolves
# refs, sources and Jinja; it never looks at the SQL. So the gate ran clean while answering a
# NARROWER question than the one it was added to answer -- the adjacent-verification hazard, walked
# into while building a gate to fix a measurement problem. It was caught only because 0-of-4 was
# implausible.
#
# `dbt compile` in dbt-fusion does static SQL analysis and needs no warehouse connection, which is
# what makes this usable against the placeholder credentials the engine emits. On the same SSIS tree
# it reports `dbt0101: mismatched input '!'` and the dangling FROM, and skips the downstream models.
parse_fail=0
sql_unverified=0
if command -v dbt >/dev/null 2>&1; then
  for proj in $(find "$OUT" "${PRUNE[@]}" -name 'dbt_project.yml' -print 2>/dev/null | xargs -n1 dirname); do
    # Captured to a variable, NOT piped. `set -o pipefail` is on at the top of this script, so
    # `dbt compile | grep -q` returns DBT's non-zero status rather than grep's match, and the `if`
    # silently never fires. First version of this check reported 0 failures on all four platforms
    # for exactly that reason, while the same command run by hand printed three errors.
    out=$(cd "$proj" && dbt compile --profiles-dir . 2>&1)
    # ANY dbt error counts, EXCEPT a connection error. This is a denylist of one, and the
    # inversion is deliberate.
    #
    # THE FIRST VERSION ALLOWLISTED TWO CODES -- dbt0101 (SQL syntax) and dbt1000 (connection) --
    # and reported DataStage as having ZERO SQL errors. Its actual failure was
    # `dbt1005: Ref 'int_NOT_FOUND' not found in project`: the engine emitting its
    # NotFoundPlaceholder because a translator could not resolve an upstream model name. Being
    # neither of the two known codes, it fell through both branches and read as SUCCESS.
    #
    # That is the THIRD hole in this one gate (after `parse` not inspecting SQL, and `pipefail`
    # swallowing grep's match) and it is the same shape as the defect this whole project is about:
    # a CLOSED VOCABULARY treating anything it does not recognise as nothing. An allowlist of error
    # codes cannot be complete, so it must not be the thing that decides success.
    #
    # dbt1000 stays excluded on evidence, not convenience: it is an ADBC "password is empty" against
    # the PLACEHOLDER CREDENTIALS the engine emits by design, and an incremental mart must introspect
    # its target relation to compile at all. Counting it would punish the one platform whose SQL is
    # valid and reward trees too broken to reach a connection.
    errs=$(printf '%s' "$out" | grep -cE '^[[:space:]]*error:')
    conn=$(printf '%s' "$out" | grep -cE 'dbt1000')
    # HOW MUCH SQL THE GATE ACTUALLY LOOKED AT. dbt writes one file under
    # target/compiled/models per model it analysed, so this is the gate's own coverage and
    # it is the FOURTH hole found in this one check.
    #
    # MEASURED, and it is the reason this line exists: the dbt1000 exclusion above was
    # justified on "an incremental mart must introspect its target relation to compile at
    # all", which is true — but dbt connects to the warehouse BEFORE analysing any SQL as
    # soon as a model references a real relation. Before the source-relation fix, the SSIS
    # tree reported two dbt0101 errors and NO dbt1000, because the dangling `FROM` needed no
    # connection. After the fix, the same tree reports dbt1000 and NOTHING ELSE — and
    # `models compiled: 0`. NEGATIVE-TESTED: overwriting a model in the fixed tree with the
    # literal text `SELECT !!!broken` still produced dbt1000 as the only error. So "no other
    # error found" would have been a claim about SQL that nothing read.
    #
    # PENTAHO ALREADY HAD THIS, BEFORE ANY CHANGE HERE: its tier-3 staging fill emitted a
    # real source() call, so it compiled 0 models and scored "0 SQL errors" — a green light
    # on an unread tree. Making the other three platforms' output CORRECT is what turned a
    # one-platform hole into a four-platform one, which is the strongest possible argument
    # that the gate and not the output was wrong.
    #
    # NOT counted as a SQL ERROR (parse_fail), because the SQL may be perfectly good; what
    # is missing is the CHECK. Same treatment, and same wording, as COVERAGE UNMEASURED in
    # stage 3d: degraded=1, and the reason stated as neither a pass nor a fail.
    declared_models=$(find "$proj/models" -name '*.sql' 2>/dev/null | wc -l | tr -d ' ')
    compiled_models=$(find "$proj/target/compiled/models" -name '*.sql' 2>/dev/null | wc -l | tr -d ' ')
    if [ "$errs" -gt 0 ] && [ "$errs" -ne "$conn" ]; then
      parse_fail=$((parse_fail + 1))
      echo "   compile errors in $(basename "$proj"): $(printf '%s' "$out" \
        | grep -oE 'dbt[0-9]{4}' | sort -u | tr '\n' ' ')"
      echo "   models the SQL gate read : $compiled_models of $declared_models"
    elif [ "$conn" -gt 0 ] && [ "$compiled_models" -lt "$declared_models" ]; then
      sql_unverified=$((sql_unverified + 1))
      echo "   *** SQL UNVERIFIED in $(basename "$proj") — dbt reached the warehouse"
      echo "       connection (placeholder credentials) after analysing only"
      echo "       $compiled_models of $declared_models model(s), so the remaining SQL was NEVER READ."
      echo "       This is NOT a claim that it is broken, and NOT a claim that it is not."
    elif [ "$conn" -gt 0 ]; then
      echo "   note: $(basename "$proj") compiled all $declared_models model(s) and then needed"
      echo "         a warehouse connection (placeholder credentials) — no other error found"
    fi
  done
  echo "   dbt projects with SQL errors : $parse_fail"
  echo "   dbt projects SQL-UNVERIFIED  : $sql_unverified"
else
  echo "   dbt projects with SQL errors : (dbt not on PATH — UNCHECKED)"
fi
[ "$ewis" != "0" ] || [ "$sentinels" != "0" ] || [ "$empty" != "0" ] || [ "$authored" != "0" ] || [ "$assisted" != "0" ] || [ "$parse_fail" != "0" ] || [ "$sql_unverified" != "0" ] && degraded=1

# ==================================================================================================
# ---- STAGE 4d: STRUCTURAL INTEGRITY — DID THE IR REACH THE DBT? ----------------------------------
# NEW STAGE, ADDED WHOLE. Nothing above this line was changed except two things, both stated where
# they happen: `GATE_BUNDLES` is assigned once above the --inspect-only block instead of inside it,
# and a full run stashes the representation to `$INTEGRITY_IR`.
#
# THE QUESTION NOTHING ELSE IN THIS SCRIPT ASKS. The owner named three kinds of gap it is GOOD for us
# to detect, and the third is that the generated models "lack structural integrity -- we lost
# information either in the IR or in the dbt". Every gate on this path answers the FIRST clause:
#
#   stage 1     did the document's records reach the identification sweep?
#   stage 3d    does the output cover the source elements a rule found?
#   stage 3e    is something in the DOCUMENT missing from the IR?           (a model reads)
#   stage 3e2   does the generated SQL DO what the document says?           (a model reads)
#   stage 4     does the tree carry degradation markers, and does it compile?
#
# None of them compares the IR to the tree. Gate A never opens a model; Gate B never opens the IR;
# stage 4 counts markers and compares the tree to nothing. So a node the hydrator accepted, a column
# the IR carries, an edge the graph resolved and a predicate a translator was handed can each vanish
# between the two and every line above this one is unchanged.
#
# MEASURED, ON THIS PROJECT'S OWN SHIPPED OUTPUT. poc/blind-run/runZ5-final/ssis carries
# `int_cspl_filter_birthyear.sql` whose six columns are all `null AS <name>`, whose ref() to the
# upstream derive model is absent, and which contains no WHERE clause at all -- while the IR for that
# same run carries `FilterConditions: "BirthYear >= 1990"`. Exit 3 was reported for the EWI marker.
# Nothing said the predicate had not reached the SQL, and a predicate that silently keeps every row
# is the difference between a filter and no filter.
#
# WHY IT IS DETERMINISTIC AND NOT A MODEL CALL. That is the point of it: it costs nothing, it runs on
# every migration, and its answers are reproducible -- so unlike stages 3e and 3e2 it can be
# negative-tested by planting the loss and watching it fire, which is exactly what
# integrity_gate_test.py does for all four classes plus both directions of the node check.
#
# WHY IT IS ORDERED HERE. After stage 4 because stage 4 counts markers by grepping the whole tree and
# this stage writes nothing into it, so the order cannot change stage 4's numbers; before stage 5
# because stage 5 writes a report INTO the tree and this stage's model inventory must not see it.
# It runs in BOTH modes, including --inspect-only, which is how its negative tests plant a loss in a
# real tree and run THE SHIPPED CODE over it.
echo "-- stage 4d: structural integrity (did the IR reach the dbt?)"
INTEGRITY=$(python3 "$HERE/integrity_gate.py" "$INTEGRITY_IR" "$OUT" \
              --platform "$TABLE_PLATFORM" \
              --json "$(dirname "$INTEGRITY_IR")/integrity.json" 2>&1)
INTEGRITY_RC=$?
printf '%s\n' "$INTEGRITY" | sed 's/^/   /'
# THE SAME DISAMBIGUATION STAGES 1, 3d, 3e AND 5 ALREADY DO, BY STDOUT SHAPE AND NOT BY EXIT CODE.
# "the gate ran and found information lost" and "the gate could not run" are OPPOSITE claims and one
# integer cannot carry both. A real verdict always prints an " integrity     :" line; every
# could-not-run path in the gate withholds it deliberately, including the one that refuses a
# zero-node representation rather than scoring it a clean 0/0.
if ! printf '%s' "$INTEGRITY" | grep -q "^ integrity     :"; then
  # NOT exit 1. The tree exists and may be perfectly good; what is missing is the COMPARISON.
  echo "   *** STRUCTURAL INTEGRITY UNMEASURED — nothing compared the representation to the tree."
  echo "       This is NOT a claim that the IR reached the dbt, and NOT a claim that it did not."
  echo "       No stashed representation, an unparseable one, one carrying no nodes at all, or a"
  echo "       ledger that did not balance. Cause above."
  degraded=1
elif [ $INTEGRITY_RC -ne 0 ]; then
  echo "   *** INFORMATION LOST BETWEEN THE IR AND THE DBT — the representation carries nodes,"
  echo "       columns, edges or payload values that no artifact in this tree does, itemised above."
  echo "       NOT a claim that the tree fails to run: an absent ref() compiles clean and a"
  echo "       substituted predicate runs and returns every row."
  degraded=1
fi
# AN EMPTY DENOMINATOR IS NOT A CLEAN RESULT, AND IT IS A SEPARATE SIGNAL FROM LOSS. A class that
# raised no obligation prints `<class> 0/0`, which reads identically to a class that discharged
# everything. Measured on the frozen DataStage arm: `columns 0/0` over an IR whose four nodes all
# carry an empty OutputColumns. The gate names it; this turns it into degradation, because a
# migration in which one whole class of integrity was never checked is exactly "output exists and is
# not trustworthy". NOT counted as loss — the loss, if any, is upstream in the IR.
if printf '%s' "$INTEGRITY" | grep -q "RAISED NOTHING"; then
  echo "   *** ONE INTEGRITY CLASS RAISED NOTHING — see above. The representation states no"
  echo "       obligation of that class, so its 0/0 is an EMPTY DENOMINATOR and not a pass."
  degraded=1
fi
# ---- END STAGE 4d --------------------------------------------------------------------------------

# ==================================================================================
# ---- STAGE 4e: DID THE GENERATED SQL ACTUALLY RUN? -------------------------------
#
# THE GAP THIS CLOSES, AND IT IS THE OLDEST ONE IN THE PROJECT. Every run before this
# reported `SQL UNVERIFIED -- 0 of 4 models`, and stage 4b's own comments record why: the
# engine emits a dbt project that is a TEMPLATE. `profiles.yml` ships `account: ACCOUNT`,
# `role: ROLE`; `dbt_project.yml` ships `name: YOUR_PROJECT_NAME`. So dbt reached the
# warehouse, failed against the literal string "ACCOUNT", and never analysed a line of SQL.
# Nothing this project has generated had ever been executed by anything.
#
# WHAT THIS STAGE CLAIMS: the SQL RUNS -- Snowflake parses it, relations resolve, the DAG
# builds in dependency order. WHAT IT DOES NOT CLAIM: that the SQL is RIGHT. No row is
# compared against a source system; behavioural parity is out of scope by owner decision.
# Those are different questions and only the first is bought here. A tree that runs is not
# a tree that is correct, and stage 4e must never be read as a parity result.
#
# OPT-IN, AND UNMEASURED IS NOT A PASS. Without --snowflake-connection this stage prints
# EXECUTION UNMEASURED and sets degraded=1 -- the same treatment as COVERAGE UNMEASURED in
# stage 3d and STRUCTURAL INTEGRITY UNMEASURED in stage 4d, for the same reason: an
# unexecuted tree is exactly the state exit 3 exists to describe. It is NOT exit 0.
#
# THE STAGE RUNS ON A COPY. It stages the project into a temp dir, binds a real profile
# there, and leaves the emitted tree byte-identical -- it hashes every model before and
# after and refuses to run if one differs. So stage 4b's "as-emitted" measurement stays a
# claim about the tree that actually shipped, measured twice: 4b with the placeholders it
# was emitted with (honest UNVERIFIED), 4e with credentials bound.
echo "-- stage 4e: execution (did the generated SQL run in Snowflake?)"
if [ -z "${AIFIRST_SNOWFLAKE_CONN:-}" ]; then
  echo "   EXECUTION UNMEASURED -- no AIFIRST_SNOWFLAKE_CONN set, so nothing ran the SQL."
  echo "       This is NOT a claim that the SQL runs, and NOT a claim that it does not."
  echo "       Set AIFIRST_SNOWFLAKE_CONN to a named connection in ~/.snowflake to measure it."
  degraded=1
else
  EXEC_OUT=$(python3 "$HERE/execute_gate.py" "$OUT" --connection "$AIFIRST_SNOWFLAKE_CONN" 2>&1)
  EXEC_RC=$?
  printf '%s\n' "$EXEC_OUT"
  # Same stdout-shape disambiguation every other stage needs, for the same reason: "it ran
  # and something failed" and "it could not run" are opposite claims one exit code cannot
  # separate. A real verdict always prints an `execution    :` line.
  if ! printf '%s' "$EXEC_OUT" | grep -q "execution    :"; then
    echo "   *** EXECUTION UNMEASURED -- the stage did not reach a verdict. Cause above."
    degraded=1
  elif [ $EXEC_RC -ne 0 ]; then
    echo "   *** EXECUTION FAILED -- the generated SQL did not run clean. This is a finding,"
    echo "       not an absence: Snowflake was reached and it rejected something."
    degraded=1
  fi
fi
# ---- END STAGE 4e ----------------------------------------------------------------
# ==================================================================================
# ==================================================================================================

# ==================================================================================
# ---- STAGE 5: THIS MIGRATOR'S OWN ISSUE FRAMEWORK --------------------------------
# NEW STAGE, ADDED WHOLE. Nothing above this line was changed. Everything between this
# banner and the matching END banner is self-contained, so it can be moved or dropped
# without touching stage 4's checks.
#
# WHY IT IS HERE AND NOT A SEPARATE SCRIPT. Stage 4's diagnostic-channel check says it
# in its own words: a ZERO means nothing in this path flagged anything, "and the size of
# that hole is what the replacement issue framework has to fill". A framework that fills
# it only when someone remembers to run it fills nothing -- this project's own finding is
# that a gate off the path is not a gate, and it has now been paid for by the loss ledger,
# by gate A, and by the tier-3 fill that laundered unverified output into an exit 0.
#
# WHY IT IS A REPLACEMENT AND NOT AN EXTENSION OF THE ENGINE'S VOCABULARY. The engine's
# not-supported vocabulary has exactly two members and both name a platform, so a third
# platform cannot emit an honest one; and 33 of the engine's issue TEXTS assert
# source-platform runtime behaviour, which on an unsupported platform is a guess
# presented as a diagnostic. This stage's codes are platform-neutral and
# content-addressed, and its texts are checked at mint time against a rule that refuses
# claims about what the source platform does.
#
# WHY IT RUNS AFTER STAGE 4 AND NOT BEFORE. Stage 4 counts the engine's markers by
# grepping the whole tree. This stage WRITES a report into the tree. Running it first
# would make stage 4's numbers depend on it, which is the non-idempotency stage 4's own
# prune expression exists to prevent. Its report also lives in a SUBDIRECTORY of Reports/
# for the same reason: the report gate globs that directory one level deep.
#
# ORDERED BEFORE `rm -f "$IR"` because the representation is one of its inputs.
echo "-- stage 5: issue framework (ours, not the engine's)"
# $INTEGRITY_IR, NOT $IR. Under --inspect-only, stages 1-3d (the only place anything ever writes
# to `$IR`) are skipped, so `$IR` still names the placeholder mktemp path from line 111 that
# nothing wrote -- exactly the state the stage 4d comment above describes. `$INTEGRITY_IR` is the
# stash stage 3d/3e write beside the gate bundles for this same reason (line 490) and that stage
# 4d already reads in both modes (line 961); this stage needs the same fix so its
# representation-side detectors run against the tree's actual representation instead of silently
# skipping with "representation unreadable" on every --inspect-only invocation.
ISSUES=$(python3 "$HERE/issues/stage.py" "$TABLE" "$DOC" "$INTEGRITY_IR" "$OUT" \
         --engine-issues="${issue_total:-unknown}" \
         --gate-b-issues="$GATE_BUNDLES/gateB/AiFirstIssues/issues.json" 2>&1)
ISSUES_RC=$?
printf '%s\n' "$ISSUES" | sed 's/^/   /'
# Same disambiguation the loss ledger and gate A needed, for the same reason: "the stage
# ran and found issues" and "the stage could not run" are opposite claims that one exit
# code cannot tell apart. A real verdict always prints an "issues        :" line.
if ! printf '%s' "$ISSUES" | grep -q "issues        :"; then
  echo "   *** ISSUES UNMEASURED — the issue framework could not run on this document."
  echo "       This is NOT a claim that there were no issues, and NOT a claim that there"
  echo "       were. Cause above. Exit 3 already means output exists and is not"
  echo "       trustworthy, which is exactly the state of an unmeasured tree."
  degraded=1
elif [ $ISSUES_RC -ne 0 ]; then
  echo "   *** ISSUES RECORDED — AIM findings merged into product Reports/ETL.Issues*.csv"
  echo "       (typed defs under Reports/AiFirstIssues/issues.json + types-cited.json)."
  echo "       Foreign dialect engine codes are stripped from ETL.Issues on this platform."
  degraded=1
fi
# ---- END STAGE 5 -----------------------------------------------------------------
# ==================================================================================

rm -f "$IR" "$EMITLOG"
echo "--------------------------------------------------------------"
if [ "$degraded" -ne 0 ]; then
  echo " VERDICT: MIGRATED WITH DEGRADATION (exit 3)"
  echo "   Output exists and is loudly incomplete. Do not read exit 0 into this."
  # exit 3: degraded — output exists and is loudly incomplete (not a clean 0, not a hard-fail 1)
  exit 3
fi
echo " VERDICT: migrated, no degradation detected (exit 0)"
# exit 0: clean — no degradation detected
exit 0
