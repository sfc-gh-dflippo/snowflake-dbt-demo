"""Shared helpers for etl-stabilization script tests."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = TESTS_DIR / "fixtures"


def run_script(script_name: str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SCRIPTS_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *args],
        capture_output=True,
        text=True,
        env=env,
        check=check,
    )


def run_track_status(*args: str) -> subprocess.CompletedProcess:
    return run_script("track_status.py", *args)


def write_json(path: Path, data: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def minimal_scan(*, source_file_path: str | None = "/sanitized/source.xml") -> dict:
    return {
        "unit_name": "wf_op_ar_accomprice",
        "unit_path": "/sanitized/unit",
        "orchestration_file": None,
        "source_file_path": source_file_path,
        "platform_id": "informatica",
        "statements": [
            {
                "name": "public.wf_op_ar_accomprice",
                "elements": [
                    {"name": "el_fixed_a", "issues": []},
                    {"name": "el_fixed_b", "issues": []},
                    {"name": "el_needs_user", "issues": []},
                ],
            }
        ],
        "dbt_projects": [{"name": "m_op_ar_accomprice", "path": "m_op_ar_accomprice"}],
    }


def base_session(*, unit_path: str = "/sanitized/unit") -> dict:
    """Sanitized session shaped like wf_op_ar_accomprice (credentials stripped)."""
    return {
        "migration_object": "wf_op_ar_accomprice",
        "migration_object_path": unit_path,
        "orchestration_file": None,
        "orchestration_file_hash": None,
        "source_file_path": "/sanitized/source.xml",
        "platform_id": "informatica",
        "started_at": "2026-08-18T00:00:00+00:00",
        "last_updated": "2026-08-18T00:00:00+00:00",
        "elements": [
            {
                "name": "el_fixed_a",
                "statement": "public.wf_op_ar_accomprice",
                "status": "fixed",
                "phase": 1,
                "test_strategy": "isolated",
            },
            {
                "name": "el_fixed_b",
                "statement": "public.wf_op_ar_accomprice",
                "status": "fixed",
                "phase": 1,
                "test_strategy": "isolated",
            },
            {
                "name": "el_needs_user",
                "statement": "public.wf_op_ar_accomprice",
                "status": "needs-user",
                "phase": 1,
                "test_strategy": "grouped:inf0058_dg1",
                "reason": "stage path needs-user",
            },
        ],
        "dbt_projects": [
            {"name": "m_op_ar_accomprice", "path": "m_op_ar_accomprice", "status": "pending", "nodes": []},
        ],
        "dbt_nodes": [],
        "test_environment": {"database": "TEST_DB", "schema": "TEST_SCHEMA"},
        "roadmap": {
            "phases": [
                {
                    "phase": 1,
                    "name": "Orchestration",
                    "goal": "fix orch",
                    "scope": "orchestration",
                    "status": "in_progress",
                    "decisions": [],
                    "parallel_safe": False,
                    "depends_on": [],
                },
                {
                    "phase": 2,
                    "name": "dbt",
                    "goal": "fix dbt",
                    "scope": "dbt",
                    "status": "pending",
                    "decisions": [],
                    "parallel_safe": False,
                    "depends_on": [1],
                },
            ]
        },
    }
