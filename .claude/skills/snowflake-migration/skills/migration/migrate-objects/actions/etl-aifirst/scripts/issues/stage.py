#!/usr/bin/env python3
"""THE STAGE. Runs on the path, writes issues into the artifact, contributes a verdict.

WHY IT IS A STAGE AND NOT A SCRIPT SOMEONE REMEMBERS TO RUN
-----------------------------------------------------------
This project's own finding, paid for twice: a gate off the path is not a gate. The
element-loss ledger and the coverage gate were both side scripts nobody was obliged to
run, and both were moved onto the driver for exactly this reason. An issue framework
that only records issues when someone thinks to invoke it records nothing on the day it
matters.

So this runs inside the driver, it writes into the emitted tree, and its verdict feeds
the driver's exit code:

    0  no issues recorded, and every detector that could run did
    3  issues recorded, or a finding was refused -- degradation, in the driver's
       vocabulary: output exists and is not trustworthy
    1  the stage could not run at all. NOT an issue verdict, and the driver tells the
       two apart by stdout shape (a real verdict always prints an " issues        :"
       line) rather than by the exit code, which cannot distinguish them
    2  usage

WHAT IT WRITES INTO THE TREE, AND ONE TRAP THAT SHAPED IT
---------------------------------------------------------
`Reports/AiFirstIssues/` -- typed inventory only: `issues.json` (full AIM instances) and
`types-cited.json` (type definitions), so a reader can resolve an `AIM-*` code without
this repository. **Product instance list (owner 2026-08-13):** `Reports/ETL.Issues*.csv`
— AIM rows coexist there with any dialect-correct engine EWI/FDM; foreign-platform engine
codes are stripped. Do **not** emit a parallel `issues.csv` here; that would duplicate
(and be superseded by) the assessment CSV.

THE TRAP: another stage of the same driver counts the engine's own markers by grepping
the whole output tree. A report that quoted those markers verbatim would inflate that
count, and the tree would then score differently depending on whether this stage had run
-- the same non-idempotency that made a re-inspected tree report twelve column-less
models on a tree the driver had just called clean. So every string written under the
output root goes through `scrub()`, and the report lives in a SUBDIRECTORY of Reports/
rather than beside the other CSVs, because the neighbouring gate globs that directory
one level deep.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from issues import signature as sigmod                                  # noqa: E402
from issues.detect import load_run, run_detectors                       # noqa: E402
from issues.inventory import (Inventory, NearDuplicateWithoutDistinguisher,  # noqa: E402
                              PlatformAssertionRefused)
from issues.seed import SEEDS, seed                                     # noqa: E402
from issues.textrule import TEXT_RULE_VERSION, lint                     # noqa: E402
from issues.etl_issues_coexist import (                                 # noqa: E402
    rewrite_etl_issues_for_coexistence,
    scrub,
)

DEFAULT_INVENTORY = Path(__file__).resolve().parent.parent / "issue-inventory"

# scrub() imported from etl_issues_coexist (shared with ETL.Issues write path).

def ensure_seeded(inv: Inventory) -> list[str]:
    """Mint any seed the inventory is missing. Idempotent, and silent when complete."""
    missing = []
    for s in SEEDS:
        sid, _, _ = sigmod.signature_id(s["category"], s["construct"], s["reason"])
        if sid not in inv.types:
            missing.append(s)
    if not missing:
        return []
    before = set(inv.types)
    seed(inv)
    return sorted(set(inv.types) - before)


def render(type_rec: dict, finding) -> str:
    """Fill the type's text for this instance, then lint the RESULT.

    The template passed the type-scope rule at mint time; the filled text can still fail
    the instance-scope rule, because the values come from the document and a native
    element kind next to a behaviour verb would be a claim. Checked here rather than
    assumed.
    """
    text = type_rec["text"]
    for key, val in (("{element}", finding.element), ("{kind}", finding.native_kind),
                     ("{detail}", finding.detail)):
        text = text.replace(key, str(val))
    return " ".join(text.split())


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True)
             for a in argv[1:] if a.startswith("--")}
    if len(args) != 4:
        print("usage: stage.py <platform-table.json> <source-document> <ir.json> "
              "<output-root> [--inventory=DIR] [--engine-issues=N] "
              "[--gate-b-issues=PATH] [--audit]",
              file=sys.stderr)
        return 2

    table_path, doc_path, ir_path, out_root = args
    inv_root = Path(flags.get("--inventory") or
                    os.environ.get("AIM_ISSUE_INVENTORY") or DEFAULT_INVENTORY)

    if not Path(table_path).is_file():
        print(f"   ISSUES UNMEASURED: no platform table at {table_path}",
              file=sys.stderr)
        return 1
    if not Path(out_root).is_dir():
        print(f"   ISSUES UNMEASURED: no output tree at {out_root}", file=sys.stderr)
        return 1

    inv = Inventory(inv_root)
    seeded = ensure_seeded(inv)
    types_before = len(inv.types)

    print(f"   framework     : {sigmod.SIG_VERSION} / {TEXT_RULE_VERSION}")
    print(f"   inventory     : {inv_root} [{types_before} type(s) before this run]")
    if seeded:
        print(f"   seeded        : {len(seeded)} type(s) minted from prior measurements: "
              f"{', '.join(seeded)}")

    run = load_run(table_path, doc_path, ir_path, out_root)
    findings, detlog = run_detectors(run)
    for line in run.notes:
        print(f"   note          : {line}")
    for line in detlog:
        print(f"   {line}")

    # ---- CLASSIFY EVERY FINDING BEFORE ANY OF THEM IS RECORDED ---------------------
    instances = []
    refused = []
    actions = {"REUSED_EXACT": 0, "REUSED_NEAR": 0, "MINTED": 0, "MINT_RACED": 0}
    minted_detail = []
    for f in findings:
        try:
            res = inv.classify_or_mint(dict(f.proposal), by=f"detector:{f.detector}")
        except (PlatformAssertionRefused, NearDuplicateWithoutDistinguisher) as exc:
            refused.append({"detector": f.detector, "element": f.element,
                            "why": f"{type(exc).__name__}: {exc}"})
            continue
        actions[res["action"]] += 1
        tid = res["id"]
        if res["action"] == "MINTED":
            cand = res["classification"]["considered"]
            minted_detail.append(
                f"{tid} <- {f.detector}: nearest existing type "
                + (f"{cand[0]['id']} at {cand[0]['score']}" if cand
                   else "(inventory empty)")
                + f"; distinguisher: {f.proposal.get('distinguisher', '') or '(none)'}")
        text = render(inv.types[tid], f)
        ilint = lint(text, scope="instance")
        instances.append({
            "code": tid,
            "category": inv.types[tid]["signature"]["category"],
            "construct": inv.types[tid]["signature"]["construct"],
            "reason": inv.types[tid]["signature"]["reason"],
            "impact": inv.types[tid]["impact"],
            "platform": run.platform,
            "document": Path(doc_path).name,
            "element_id": f.element_id,
            "element": f.element,
            "observed_kind": f.native_kind,
            "detail": f.detail,
            "evidence": f.evidence,
            "location": f.location,
            "detector": f.detector,
            "text": text,
            "text_lint": ilint["verdict"],
            "text_lint_findings": [x["rule"] for x in ilint["findings"]],
        })
        if ilint["verdict"] == "REJECT":
            # The template passed at mint time; the FILLED text did not. Recorded and
            # counted as a refusal, because shipping it would be the exact defect the
            # rule exists to stop.
            refused.append({"detector": f.detector, "element": f.element,
                            "why": "instance text failed the text rule: "
                                   + "; ".join(x["rule"] for x in ilint["findings"])})
            instances.pop()

    gb = Path(flags.get("--gate-b-issues") or "")
    if gb.is_file():
        redirects = inv.promote(by="stage5:gate-b").get("redirects") or {}
        extra = json.loads(gb.read_text(encoding="utf-8")).get("instances") or []
        # A Gate B instance's `code` was serialized before this promote() ran, so a
        # proposal that got redirected to a near-duplicate existing type still carries
        # its stale pre-promotion id -- remap it or `types-cited.json` silently drops it.
        for x in extra:
            if isinstance(x, dict) and x.get("code") in redirects:
                x["code"] = redirects[x["code"]]
        seen = {(i.get("code"), i.get("element_id")) for i in instances}
        instances.extend(x for x in extra
                         if isinstance(x, dict)
                         and (x.get("code"), x.get("element_id")) not in seen)

    # ---- THE ARTIFACT --------------------------------------------------------------
    dest = Path(out_root) / "Reports" / "AiFirstIssues"
    dest.mkdir(parents=True, exist_ok=True)
    # No issues.csv — product instance rows live in ETL.Issues*.csv (coexistence rewrite below).
    cited = sorted({i["code"] for i in instances if i.get("code")})
    (dest / "issues.json").write_text(
        scrub(json.dumps({"framework": sigmod.SIG_VERSION,
                          "text_rule": TEXT_RULE_VERSION,
                          "platform": run.platform,
                          "document": Path(doc_path).name,
                          "instances": instances,
                          "refused": refused}, indent=2)) + "\n",
        encoding="utf-8")
    (dest / "types-cited.json").write_text(
        scrub(json.dumps({tid: inv.types[tid] for tid in cited if tid in inv.types},
                         indent=2, sort_keys=True)) + "\n", encoding="utf-8")

    # ---- THE VERDICT ---------------------------------------------------------------
    per_type: dict[str, int] = {}
    for i in instances:
        per_type[i["code"]] = per_type.get(i["code"], 0) + 1
    print(f"   issues        : {len(instances)} instance(s) across {len(per_type)} "
          f"type(s)")
    if not instances and not refused:
        # A ZERO IS AN ABSENCE, NOT A CLEARANCE, and it is said here rather than left to
        # be inferred. The same discipline the neighbouring stages use for UNMEASURED
        # coverage and for an absent task graph: state what was and was not established.
        print("   note          : 0 issues from the detectors listed above. That is NOT "
              "a claim that the output is correct — nothing in this stage compiles it, "
              "runs it, or compares it with the source system. It says only that these "
              "detectors found nothing.")
    for tid, n in sorted(per_type.items(), key=lambda kv: (-kv[1], kv[0])):
        rec = inv.types.get(tid)
        if rec is None:
            print(f"     {tid} x{n:<3} [untyped] instance whose type is not in this inventory")
            continue
        print(f"     {tid} x{n:<3} [{rec['impact']}] {rec['title']}")
    print(f"   classified    : {actions['REUSED_EXACT']} reused an existing type "
          f"exactly, {actions['REUSED_NEAR']} redirected to a near duplicate, "
          f"{actions['MINTED']} minted, {actions['MINT_RACED']} lost a mint race to an "
          f"identical type")
    for line in minted_detail:
        print(f"     mint: {line}")
    if refused:
        print(f"   *** {len(refused)} FINDING(S) REFUSED — observed and NOT recorded, so "
              f"the count above is a floor")
        for r in refused:
            print(f"       {r['detector']} / {r['element']}: {r['why'][:160]}")
    print(f"   artifact      : {dest}/issues.json + types-cited.json (instance list -> ETL.Issues, not a parallel issues.csv)")

    # ---- PRODUCT ETL.Issues COEXISTENCE (owner 2026-08-13) -------------------------
    coexist = rewrite_etl_issues_for_coexistence(
        out_root,
        platform=run.platform,
        document_name=Path(doc_path).name,
        aim_instances=instances,
    )
    print(
        "   etl.issues    : coexistence rewrite -> "
        f"{coexist['total']} row(s) "
        f"(kept_engine={coexist['kept_engine']}, "
        f"dropped_bleed={coexist['dropped_bleed']}, "
        f"aim_added={coexist['aim_added']})"
    )
    if coexist["dropped_bleed"]:
        print(
            "   etl.issues    : stripped foreign dialect code(s): "
            + ", ".join(coexist["dropped_codes"])
        )
    print(f"   etl.issues    : {coexist['path']}")

    eng = flags.get("--engine-issues")
    if eng not in (None, True):
        # DIRECTLY THE HOLE THE NEIGHBOURING STAGE REPORTS. It counts the engine's own
        # markers in the tree and states that a zero means nothing in this path flagged
        # anything. This line says how much of that hole is now filled, and by what.
        print(f"   engine channel: {eng} engine issue instance(s) in this tree; this "
              f"framework recorded {len(instances)}")

    bad_ids = inv.stability_check()
    if bad_ids:
        print(f"   *** INVENTORY IDS DO NOT MATCH THEIR OWN SIGNATURES: {bad_ids}")
        return 3

    if flags.get("--audit"):
        print()
        for line in inv.audit():
            print(f"   {line}")

    if instances or refused:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
