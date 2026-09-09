#!/usr/bin/env python3
"""TIER 3 of the fallback ladder: fill models the engine could not render.

WHY THIS STAGE EXISTS
---------------------
Leaning on SnowConvert's IR and translators made them a GATE on generation. Three
things terminate in a NULL-projecting placeholder rather than a migration:

  * an element kind the IR vocabulary cannot name (a multi-output router today);
  * a payload no deterministic rule can scrape AND no tier-2 sidecar field can carry;
  * a REPRESENTATION THE ENGINE REFUSES TO RENDER -- a correct FilterTransformation
    that ENG-020 throws on because the upstream step name contains a space.

On a platform SnowConvert does not support, every one of those is the expected case,
not the exception. So "nothing" was the normal output of a migrator whose entire
premise is that something imperfect beats nothing.

Tier 3 is the floor: if the model can write the SQL for a node, that SQL ships.

WHAT THIS DELIBERATELY IS NOT
-----------------------------
It is NOT a way to make the artifact look better. Three constraints keep it honest:

 1. It only ever replaces a model that is ALREADY DEGRADED -- one carrying a blocking
    EWI, or projecting no columns. A model the engine rendered successfully is never
    touched, so tier 1 always wins where tier 1 works. Verified by refusing to write
    unless the existing file fails that test.
 2. Every file it writes is stamped SSC-AI-AUTHORED with the reason and the source
    element. A reviewer can tell at a glance which models came from the engine's
    translators and which from a model, and nothing downstream can confuse them.
 3. It does NOT clear the degradation verdict. These models are UNVERIFIED -- nothing
    here compiles them, runs them, or compares them against the source system -- which
    is exactly what exit 3 means. Turning a tier-3 fill into an exit 0 would be the
    silent-success defect this project keeps finding.

VERDICT LINE (driver contract)
------------------------------
Always prints one machine-readable line the driver greps:

  authoring : needed=<N> filled=<M>[ skipped=<reason>]

`needed` is how many on-disk models are NOT a clean engine result: either still
degraded (blocking EWI or empty projection) and unauthored, OR already carrying
SSC-AI-AUTHORED from an earlier fill. The second half is deliberate -- an authored
model is UNVERIFIED, never CLEAN, so it counts toward `needed` for as long as it
sits in the tree. Excluding it (as an earlier version of this count did) let a
successful fill erase its own degraded verdict: the moment a model was authored it
stopped being degraded text, `needed` fell to 0 on the next measurement, and a
verdict that exists to say "a human still has to look at this" read as a clean
no-op instead. Measured BEFORE any fill, on every path including no-sidecar --
otherwise the no-sidecar early return hid unaddressed degradation from the driver
(lifecycle-showcase / Alteryx fixture).
`filled` is how many files THIS invocation wrote. `skipped=no-sidecar` when the
sidecar file is absent (filled stays 0). needed=0 and filled=0 is the only clean
no-op; needed>0 -- whether filled is 0 or not, since authored models keep counting
-- is the driver's signal to set degraded=1. filled>0 can never zero out `needed`
within the same run or a later one.

WHAT THE STAMP MUST NOT SAY
---------------------------
The stamp used to assert "RUNNABLE, NOT VERIFIED". The second half was true and the
FIRST HALF WAS MEASURED FALSE: the Pentaho fill referenced source('raw','CUSTOMER') in
a project carrying no sources.yml and `dbt compile` failed outright. A marker asserting
a property nobody checked is the same defect as an exit code asserting a success nobody
checked, and it appeared in the line whose entire purpose is honesty. The stamp now
states PROVENANCE (who wrote this) and the ABSENCE of verification, and claims nothing
about whether the SQL runs -- because this script cannot know, and stage 4 asks a real
parser instead.

Usage:  ai_fill.py <ir.json> <sidecar.ai.json> <output-root>
Exit:   0 always (a fill is opportunistic; nothing here is a failure condition)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "SSC-AI-AUTHORED"
# Split, for the reason `issues/detect.py` splits the same two strings: a gate counts these
# markers across the whole output tree, so a script that reads them must not be a file that
# contains them.
BLOCKING_MARKER = "!!!RESOLVE" + " EWI!!!"
PRODUCER_SENTINEL = "__PRODUCER_EXPRESSION" + "_NOT_CONVERTED__"


def is_degraded(sql: str) -> bool:
    """True when the engine's own output for this model is unusable.

    Three signals, all taken from the artifact rather than from the run: a blocking EWI, the
    producer's unconverted-expression sentinel, or a SELECT that projects nothing. The column
    test looks at EVERY select/from pair, not the first -- a defect measured earlier in this
    project, where a correct CTE masked a column-less outer projection.

    THE SENTINEL WAS MISSING AND IT COST A RUN. `issues/detect.py` calls a model unusable on
    BLOCKING_MARKER **or** PRODUCER_SENTINEL; this function tested only the first. Measured on
    Alteryx pass 7: `int_m_5` carried a full column list and `WHERE
    <the producer's sentinel>`, so this returned False, tier 1 won, and the sidecar's tier-3
    body for that element was declined -- while stage 5 of the SAME run reported the file as
    carrying "a marker that stops it from being used". Two stages of one pipeline disagreeing
    about one file, and the one holding the replacement was the one that said it was fine.
    """
    return degradation_signal(sql) is not None


def degradation_signal(sql: str) -> str | None:
    """WHICH signal fired, in words, or None. The stamp names it rather than guessing.

    The provenance header used to assert it had replaced "a blocking EWI or no projected
    columns" whatever the real reason was. With a third signal that sentence would be wrong a
    third of the time, in the one line whose entire job is to be accurate about what happened.
    """
    if BLOCKING_MARKER in sql:
        return "a blocking EWI"
    if PRODUCER_SENTINEL in sql:
        return "the producer's unconverted-expression sentinel"
    for body in re.findall(r"^\s*SELECT\s*$(.*?)^\s*FROM\s*$", sql,
                           re.S | re.M | re.I):
        if not body.strip():
            return "a SELECT that projects nothing"
    # A trailing bare SELECT or FROM with nothing after it at all.
    tail = sql.rstrip().rsplit("\n", 1)[-1].strip().upper()
    if tail in ("SELECT", "FROM"):
        return "a bare %s with nothing after it" % tail
    return None


def _count_needed(models: list[Path]) -> int:
    """Models that are not a clean engine result: still degraded and unauthored, or
    already SSC-AI-AUTHORED (authored is UNVERIFIED, never clean, so it stays counted
    rather than dropping out the moment a fill stamps the marker -- see the module
    docstring's VERDICT LINE section for the defect this closes)."""
    n = 0
    for path in models:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if MARKER in text or is_degraded(text):
            n += 1
    return n


def _emit_verdict(needed: int, filled: int, skipped: str | None = None) -> None:
    # Single grep target for aifirst-migrate.sh stage 3b. Keep the key stable.
    extra = f" skipped={skipped}" if skipped else ""
    print(f"   authoring : needed={needed} filled={filled}{extra}")


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[-2], file=sys.stderr)
        return 0
    ir_path, sidecar_path, out_root = Path(argv[1]), Path(argv[2]), Path(argv[3])

    models = list(out_root.rglob("*.sql"))
    needed = _count_needed(models)

    if not sidecar_path.is_file():
        print("   ai-fill: no sidecar for this document — nothing to fill")
        _emit_verdict(needed, filled=0, skipped="no-sidecar")
        return 0

    sidecar = (json.loads(sidecar_path.read_text(encoding="utf-8")).get("elements")
               or {})
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    nodes = (ir.get("pipeline") or ir).get("nodes", [])

    # SIDECAR IDENTITY -> modelName. A sidecar is normally keyed by the emitter's raw
    # element name (for Alteryx, ToolID "94"), while the IR's display Name/modelName is
    # sanitized ("m_94"). The old display-name-only map therefore rejected every tier-3
    # Alteryx entry even though the producer had matched it to this exact node by node.id.
    # Keep all three exact aliases: stable raw node identity first, then the two historical
    # display aliases. Values are only model names; an alias never changes which file wins.
    by_name = {}
    for node in nodes:
        model_name = node.get("modelName")
        element = node.get("element") or {}
        for alias in (node.get("id"), element.get("Name"), model_name):
            if alias not in (None, ""):
                by_name[str(alias)] = model_name

    filled, skipped_intact, no_target = [], [], []

    for el_name, entry in sidecar.items():
        sql = entry.get("ModelSql")
        if not sql:
            continue
        model_name = by_name.get(el_name)
        if not model_name:
            no_target.append(el_name)
            continue
        # Match on the emitter's model name, allowing the layer prefixes it adds.
        hits = [m for m in models
                if m.stem in (model_name, f"int_{model_name}", f"stg_raw__{model_name}")
                or m.stem.endswith(f"__{model_name}")]
        if not hits:
            no_target.append(f"{el_name} (no file for model {model_name!r})")
            continue

        for path in hits:
            existing = path.read_text(encoding="utf-8")
            if MARKER in existing:
                continue
            signal = degradation_signal(existing)
            if signal is None:
                # TIER 1 WON. Leave it alone and say so.
                skipped_intact.append(path.name)
                continue
            reason = (entry.get("_why_tier_3")
                      or "the engine produced no usable model for this element")
            # dbt evaluates Jinja even inside SQL comments. Model-authored provenance can quote
            # the broken engine SQL (including {{ ref(...) }}), and writing that quote verbatim
            # makes an otherwise valid replacement fail before dbt reaches its body. The reason
            # is explanatory metadata, not executable code: neutralize Jinja delimiters and keep
            # every physical line commented without changing the authored SQL body.
            reason = str(reason).replace("{{", "{ {").replace("}}", "} }")
            reason = reason.replace("\r\n", "\n").replace("\r", "\n")
            reason = "\n--                  ".join(reason.split("\n"))
            # GAP 3: the status line used to read "RUNNABLE, NOT VERIFIED", and
            # RUNNABLE WAS MEASURED FALSE. The Pentaho tier-3 model referenced
            # source('raw','CUSTOMER') in a project with no sources.yml, so
            # `dbt compile` failed outright -- the marker asserted a property nobody
            # had checked, which is precisely the defect class this project exists to
            # catalogue, committed inside the one line whose job is to be honest.
            #
            # Stage 3c now emits sources.yml, so that particular failure is closed.
            # The wording still does not come back, because this script CANNOT know
            # the model runs: it writes a file and never compiles it, never connects
            # to a warehouse, and never compares a row against the source system. The
            # replacement therefore states only what is established here -- who wrote
            # it, and what has not been checked. Whether it compiles is stage 4's
            # question and stage 4 answers it separately, with a parser.
            header = (
                f"-- {MARKER}: this model was written by a MODEL, not by SnowConvert's translators.\n"
                f"-- Source element : {el_name}\n"
                f"-- Reason         : {reason}\n"
                f"-- Provenance     : model-authored SQL. NOT read from the source document and NOT\n"
                f"--                  produced by a SnowConvert translator.\n"
                f"-- Verification   : NONE. Not compiled, not executed, and not compared against\n"
                f"--                  source behaviour by this stage. Review before use.\n"
                f"-- Replaced       : an engine model carrying {signal}.\n")
            path.write_text(header + sql + "\n", encoding="utf-8")
            filled.append(path.name)

    if filled:
        print(f"   ai-fill: wrote {len(filled)} model(s) the engine could not render: "
              + ", ".join(sorted(filled)))
    if skipped_intact:
        print(f"   ai-fill: left {len(skipped_intact)} engine-rendered model(s) untouched "
              f"(tier 1 wins): " + ", ".join(sorted(skipped_intact)))
    if no_target:
        # Loud, because a sidecar entry naming an element that does not exist in the IR
        # is a typo in the model's output, and silently ignoring it would hide a
        # mis-keyed fill as "nothing needed doing".
        print(f"   ai-fill: WARNING {len(no_target)} sidecar entr(ies) matched no IR "
              f"element or model file: " + "; ".join(no_target))
    if not (filled or skipped_intact or no_target):
        print("   ai-fill: sidecar carries no ModelSql — nothing to fill")
    _emit_verdict(needed, filled=len(filled))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
