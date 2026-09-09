"""Generate JSON reports from CheckResult data."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import CheckResult


def results_to_json(results: list[CheckResult]) -> str:
    """Serialize check results to JSON string (excludes unresolved and sibling_context — written separately)."""
    data = []
    for r in results:
        d = asdict(r)
        d.pop("unresolved", None)
        d.pop("sibling_context", None)
        data.append(d)
    return json.dumps(data, indent=2)


def save_json_report(results: list[CheckResult], output_path: Path) -> None:
    """Save check results as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(results_to_json(results), encoding="utf-8")
