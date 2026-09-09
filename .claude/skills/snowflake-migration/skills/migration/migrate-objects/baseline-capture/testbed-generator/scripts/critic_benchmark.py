"""Benchmark harness for the enrichment critics — offline-deterministic (CI-green) by default.

Scores a frozen seeded-fault set two ways:
  residue=False -> backbone-only ablation (the baseline; isolates the residue's marginal lift).
  residue=True  -> backbone + replayed critic verdicts (the canned residue double from cases.json).
The live path (--run-live) is the seam a future live-residue runner (not run in CI) plugs into; it
makes model calls. One diffable JSON report: per-type coverage + per-layer catch counts + false-REJECT count.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from critic_index import load_index  # noqa: E402
from critic_backbone import CheckStatus, run_backbone  # noqa: E402
from critic_gate import GateAction, parse_verdict, apply_gate  # noqa: E402


def _never(_t, _c, _v):
    return False


def _outcome(case, index, *, residue, run_live):
    envelope = case["envelope"]
    if any(c.status == CheckStatus.FAIL for c in run_backbone(envelope, index)):
        return "reject", "backbone"
    if not residue:
        return "accept", "none"
    if run_live:
        raise NotImplementedError("live residue path requires an agent runner (not run in CI)")
    verdict = parse_verdict(json.dumps(case.get("verdict") or {"verdicts": []}))
    if not verdict.ok:
        return "escalate", "residue"
    decision = apply_gate(verdict, index, _never)
    # "accept"/"reject"/"escalate" below are the benchmark's own outcome vocabulary, compared against
    # cases.json `expected_action` -- deliberately not GateAction, which names the gate's decisions.
    if decision.action == GateAction.ACCEPT_ALL:
        return "accept", "none"
    return decision.action, "residue"


def score(cases_dir: str | Path, *, residue: bool = True, run_live: bool = False) -> dict:
    root = Path(cases_dir)
    view = json.loads((root / "unsolved-view.json").read_text(encoding="utf-8"))
    index = load_index(str(root / "artifacts"), view)
    cases = json.loads((root / "cases.json").read_text(encoding="utf-8"))

    per_type: dict = {}
    layers = {"backbone": 0, "residue": 0}
    false_rejects = 0
    results = []
    for case in cases:
        outcome, layer = _outcome(case, index, residue=residue, run_live=run_live)
        caught = outcome != "accept"
        pt = per_type.setdefault(case["type"], {"seeded_total": 0, "seeded_caught": 0,
                                                "clean_total": 0, "clean_ok": 0})
        if case["bucket"] == "seeded":
            pt["seeded_total"] += 1
            if caught:
                pt["seeded_caught"] += 1
                if layer in layers:
                    layers[layer] += 1
        else:
            pt["clean_total"] += 1
            if caught:
                false_rejects += 1
            else:
                pt["clean_ok"] += 1
        results.append({"id": case["id"], "type": case["type"], "bucket": case["bucket"],
                        "layer": case.get("layer", "na"), "expected": case["expected_action"],
                        "outcome": outcome, "ok": outcome == case["expected_action"]})
    return {"residue": residue, "total": len(cases), "per_type": per_type,
            "layers": layers, "false_rejects": false_rejects, "cases": results}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="critic_benchmark")
    ap.add_argument("--set", required=True, help="fixture dir with artifacts/, unsolved-view.json, cases.json")
    ap.add_argument("--no-residue", action="store_true", help="backbone-only ablation baseline")
    ap.add_argument("--run-live", action="store_true", help="author residue live (a future live-residue runner; not CI)")
    ap.add_argument("--out", default=None, help="write the JSON report here")
    a = ap.parse_args(argv)
    report = score(a.set, residue=not a.no_residue, run_live=a.run_live)
    text = json.dumps(report, indent=2)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
