#!/usr/bin/env python3
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Track ETL fixer session status across elements.

Essential commands (always used):
    python track_status.py init <scan.json>
    python track_status.py update <session_status.json> <element_name> --status <status> [--reason <reason>]
    python track_status.py set-test-env <session_status.json> <database> <schema>
    python track_status.py init-roadmap <session_status.json> --phases-json '<json>'
    python track_status.py init-roadmap <session_status.json> --phases-file <path>
    python track_status.py start-phase <session_status.json> <phase_num>
    python track_status.py assign-phases <session_status.json> --phase <N> --elements <csv>  --strategy <strategy>
    python track_status.py assign-phases <session_status.json> --phase <N> --elements-file <path> --strategy <strategy>
    python track_status.py batch-assign-phases <session_status.json> --assignments-file <path>
    python track_status.py update-state <session_status.json> --current-phase <N> --phase-status <text> --next-action <text>
    python track_status.py complete-phase <session_status.json> <phase_num>
    python track_status.py validate-phase <session_status.json> <phase_num> [--list-test-files]

Situational commands (error recovery, dbt):
    python track_status.py add-phase <session_status.json> --phase <N> --name <name> --goal <goal> --scope <scope>
    python track_status.py add-decision <session_status.json> --phase <N> --decision <text>
    python track_status.py update-dbt <session_status.json> <project_name> --status <status> [--reason <reason>]
    python track_status.py init-dbt <session_status.json> <project_name> <dbt_project_path>
    python track_status.py assign-dbt-phase <session_status.json> --phase <N> --project <name>
    python track_status.py update-dbt-node <session_status.json> <project_name> <node_name> --status <status> [--reason <reason>]
"""
from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from path_resolver import (
    fix_log_path,
    phase_dir_candidates,
    report_path,
    resolve_phase_dir,
    stabilization_root,
    tests_dir,
)

VALID_STATUSES = {"pending", "in_progress", "fixed", "skipped", "needs-user", "failed", "no-fix-needed", "orch-tested", "proc-tested", "test-passed", "test-failed", "auto-fixed-needs-review"}

TERMINAL_STATUSES = {
    "fixed", "test-passed", "test-failed", "no-fix-needed",
    "skipped", "needs-user", "auto-fixed-needs-review", "failed",
}

VALID_SKIP_REASONS = {"disabled-in-source", "container-only", "file-io-noop", "dbt-dependency", "external-dependency"}

VALID_DBT_STATUSES = {"pending", "in_progress", "dbt-fixed", "dbt-failed", "dbt-tested", "skipped", "test-passed", "test-failed"}

# "unverified": the node compiled but its source-derived semantic tests could not be run
# (no warehouse available). Deliberately distinct from "fixed" -- a compile-only pass is not
# evidence of correctness. See dbt-fixer/SKILL.md Step 2.3.
VALID_DBT_NODE_STATUSES = {"pending", "passing", "fixed", "failed", "skipped", "test-passed", "test-failed", "unverified"}

VALID_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"in_progress", "fixed", "skipped", "needs-user", "failed", "no-fix-needed", "orch-tested", "proc-tested", "test-passed", "test-failed", "auto-fixed-needs-review"},
    "in_progress": {"fixed", "skipped", "needs-user", "failed", "no-fix-needed", "orch-tested", "proc-tested", "test-passed", "test-failed", "auto-fixed-needs-review"},
    "orch-tested": {"fixed", "failed", "needs-user", "no-fix-needed", "test-passed", "test-failed", "auto-fixed-needs-review", "in_progress"},
    "proc-tested": {"fixed", "failed", "needs-user", "no-fix-needed", "test-passed", "test-failed", "auto-fixed-needs-review", "in_progress"},
    "fixed": {"test-passed", "test-failed", "in_progress"},
    "test-passed": {"in_progress"},
    "test-failed": {"in_progress", "fixed", "needs-user"},
    "needs-user": {"in_progress", "fixed", "skipped", "auto-fixed-needs-review"},
    "auto-fixed-needs-review": {"in_progress", "test-passed", "test-failed", "needs-user"},
    "failed": {"in_progress", "fixed"},
    "skipped": {"in_progress"},
    "no-fix-needed": {"test-passed", "in_progress"},
}


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """Write JSON atomically: temp file + os.replace prevents corruption."""
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(
            dir=str(path.parent), suffix=".tmp", prefix=path.stem
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, str(path))
    except BaseException:
        if tmp is not None:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise


@contextlib.contextmanager
def _locked(status_path: Path):
    lock_path = status_path.with_suffix(status_path.suffix + ".lock")
    with open(lock_path, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int(value: str, label: str) -> int:
    try:
        return int(value)
    except ValueError:
        print(f"Error: {label} must be an integer, got '{value}'", file=sys.stderr)
        sys.exit(1)


def _file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

def cmd_init(scan_path: Path) -> None:
    scan = load_json(scan_path)

    elements: list[dict] = []
    for stmt in scan["statements"]:
        if stmt["elements"]:
            for el in stmt["elements"]:
                entry: dict = {
                    "name": el["name"],
                    "statement": stmt["name"],
                    "status": "pending",
                    "initial_issues": [
                        {"code": iss["code"], "description": iss.get("description", "")}
                        for iss in el.get("issues", [])
                    ],
                    "has_dbt_project": el.get("has_dbt_project", False),
                }
                entry["phase"] = None
                entry["test_strategy"] = None
                if el.get("linked_dbt_project"):
                    entry["linked_dbt_project"] = el["linked_dbt_project"]
                elements.append(entry)
        else:
            stmt_issues = [
                {"code": iss["code"], "description": iss.get("description", "")}
                for iss in stmt.get("issues", [])
            ]
            elements.append({
                "name": stmt["name"],
                "statement": stmt["name"],
                "status": "pending",
                "is_statement_level": True,
                "initial_issues": stmt_issues,
                "has_dbt_project": stmt.get("has_dbt_project", False),
                "phase": None,
                "test_strategy": None,
            })

    dbt_projects = [
        {"name": p["name"], "path": p["path"], "status": "pending"}
        for p in scan.get("dbt_projects", [])
    ]

    orch_file = scan.get("orchestration_file")
    orch_hash = None
    if orch_file:
        orch_path = Path(orch_file)
        if orch_path.is_file():
            orch_hash = _file_hash(orch_path)

    source_file_path = scan.get("source_file_path")
    platform_id = scan.get("platform_id")
    if platform_id is None and "platform_id" not in scan:
        # Backward compat: old scan results created before multi-platform support
        platform_id = "ssis"

    ts = now_iso()
    session = {
        "migration_object": scan["unit_name"],
        "migration_object_path": scan["unit_path"],
        "orchestration_file": orch_file,
        "orchestration_file_hash": orch_hash,
        "source_file_path": source_file_path,
        "platform_id": platform_id,
        "started_at": ts,
        "last_updated": ts,
        "elements": elements,
        "dbt_projects": dbt_projects,
    }

    out_dir = scan_path.parent.parent / "tracking"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "session_status.json"
    save_json(out_path, session)
    print(f"Session initialized: {out_path}")
    print(f"  Elements: {len(elements)}")
    print(f"  dbt projects: {len(dbt_projects)}")


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

def cmd_update(status_path: Path, element_name: str, status: str, reason: str | None) -> None:
    if status not in VALID_STATUSES:
        print(f"Error: invalid status '{status}'. Valid: {', '.join(sorted(VALID_STATUSES))}", file=sys.stderr)
        sys.exit(1)

    with _locked(status_path):
        session = load_json(status_path)
        found = None
        for el in session["elements"]:
            if el["name"] == element_name:
                found = el
                break

        if found is None:
            print(f"Error: element '{element_name}' not found", file=sys.stderr)
            sys.exit(1)

        current = found["status"]
        allowed = VALID_TRANSITIONS.get(current)
        if allowed and status not in allowed:
            print(f"Warning: unusual transition '{current}' -> '{status}' for '{element_name}'", file=sys.stderr)

        # Validate needs-user requires reason
        if status == "needs-user" and reason is None:
            print("Error: 'needs-user' status requires --reason documenting prior fix attempts", file=sys.stderr)
            sys.exit(1)

        # Validate skipped requires valid reason
        if status == "skipped":
            if reason is None:
                print("Error: 'skipped' status requires --reason. Valid: " + ", ".join(sorted(VALID_SKIP_REASONS)), file=sys.stderr)
                sys.exit(1)
            if reason not in VALID_SKIP_REASONS:
                print(f"Error: invalid skip reason '{reason}'. Valid skip reasons: " + ", ".join(sorted(VALID_SKIP_REASONS)), file=sys.stderr)
                sys.exit(1)

        found["status"] = status
        if reason is not None:
            found["reason"] = reason
        elif "reason" in found and status not in ("skipped", "failed", "needs-user", "test-failed", "orch-tested"):
            del found["reason"]

        session["last_updated"] = now_iso()
        save_json(status_path, session)
    print(f"Updated '{element_name}' -> {status}")


# ---------------------------------------------------------------------------
# set-test-env
# ---------------------------------------------------------------------------

def cmd_set_test_env(status_path: Path, database: str, schema: str) -> None:
    session = load_json(status_path)
    session["test_environment"] = {
        "database": database,
        "schema": schema,
    }
    session["last_updated"] = now_iso()
    save_json(status_path, session)
    print(f"Test environment set: {database}.{schema}")


# ---------------------------------------------------------------------------
# init-roadmap
# ---------------------------------------------------------------------------

def cmd_init_roadmap(status_path: Path, phases_json: str) -> None:
    session = load_json(status_path)
    if "roadmap" in session:
        print("Error: roadmap already exists in session. Use complete-phase or add-decision to update.", file=sys.stderr)
        sys.exit(1)

    phases = json.loads(phases_json)
    roadmap_phases = []
    for p in phases:
        phase_data = {
            "phase": p["phase"],
            "name": p["name"],
            "goal": p["goal"],
            "scope": p["scope"],
            "status": "pending",
            "decisions": [],
            "parallel_safe": p.get("parallel_safe", False),
            "depends_on": p.get("depends_on", []),
        }
        roadmap_phases.append(phase_data)

    session["roadmap"] = {
        "phases": roadmap_phases,
        "created_at": now_iso(),
    }
    session["last_updated"] = now_iso()
    save_json(status_path, session)

    print(f"Roadmap initialized with {len(roadmap_phases)} phases")


# ---------------------------------------------------------------------------
# complete-phase
# ---------------------------------------------------------------------------

def _phase_has_rglob(pkg_path: str, phase_num: int, pattern: str) -> bool:
    return any(
        path.is_dir() and any(path.rglob(pattern))
        for path in phase_dir_candidates(pkg_path, phase_num)
    )


def _validate_orch_artifacts(session: dict, phase_num: int, pkg_path: str) -> list[str]:
    """Return a list of validation errors for an orchestration phase.

    Batch-agent filenames (`baseline_batch_*.md`, `batch_*.md`,
    `learnings_batch_*.md`, `apply_report.md`) are one valid layout, not a
    required one: a main-session run writes `tracking/fix-log.md` instead.
    Phase dirs may be `phase-{N}` or `phase_{N}`.
    """
    errors: list[str] = []

    if pkg_path:
        has_batch_layout = (
            _phase_has_rglob(pkg_path, phase_num, "baseline_batch_*.md")
            or _phase_has_rglob(pkg_path, phase_num, "batch_*.md")
            or _phase_has_rglob(pkg_path, phase_num, "learnings_batch_*.md")
            or _phase_has_rglob(pkg_path, phase_num, "apply_report.md")
        )
        has_fix_log = fix_log_path(pkg_path).is_file()
        if not has_batch_layout and not has_fix_log:
            phase_directory = resolve_phase_dir(pkg_path, phase_num)
            errors.append(
                f"Missing phase artifacts: no batch reports under {phase_directory} "
                f"and {fix_log_path(pkg_path)} not found"
            )
    else:
        errors.append("Missing artifact: migration_object_path not set in session; cannot locate phase artifacts")

    phase_elements = [el for el in session["elements"] if el.get("phase") == phase_num]
    non_terminal = [el["name"] for el in phase_elements if el["status"] not in TERMINAL_STATUSES]
    if non_terminal:
        errors.append(
            f"Elements not in terminal status ({', '.join(non_terminal)}): "
            f"all elements must be resolved before completing phase"
        )

    return errors


def _dbt_project_dir(session: dict, pkg_path: str, project: str) -> Path | None:
    """Resolve a dbt project directory from session `dbt_projects[].path`."""
    rel = None
    for proj in session.get("dbt_projects", []):
        if proj.get("name") == project:
            rel = proj.get("path")
            break
    if not rel:
        rel = project
    path = Path(rel)
    if path.is_absolute():
        return path
    if pkg_path:
        return Path(pkg_path) / rel
    return None


def _top_level_yaml_scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent != 0:
            continue
        content = line.strip()
        if content.startswith(prefix):
            value = content[len(prefix):].strip().strip("'\"")
            return value or None
    return None


def _first_level_yaml_mapping_keys(text: str, section: str) -> list[str]:
    keys: list[str] = []
    in_section = False
    child_indent: int | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        content = line.strip()
        if indent == 0:
            in_section = content == f"{section}:" or content.startswith(f"{section}:")
            child_indent = None
            continue
        if not in_section:
            continue
        if child_indent is None:
            child_indent = indent
        if indent < child_indent:
            in_section = False
            continue
        if indent != child_indent:
            continue
        if ":" not in content:
            continue
        key = content.split(":", 1)[0].strip().strip("'\"")
        if not key or key.startswith("+"):
            continue
        keys.append(key)
    return keys


def _check_dbt_project_yml_sanity(project_path: Path) -> list[str]:
    """Structural sanity checks independent of placeholder-scanning (scan_unit.py's job).

    Catches a specific, deterministic class of incomplete-bootstrap bug: the `models:`
    block's key must match the project's own `name:` — if not, +materialized config
    for the real project silently never applies to any model.
    """
    errors: list[str] = []
    dbt_project_yml = project_path / "dbt_project.yml"
    if not dbt_project_yml.is_file():
        return errors
    try:
        text = dbt_project_yml.read_text(encoding="utf-8")
    except OSError:
        return errors
    name = _top_level_yaml_scalar(text, "name")
    models_keys = _first_level_yaml_mapping_keys(text, "models")
    if name and models_keys and name not in models_keys:
        errors.append(
            f"{dbt_project_yml}: models: key(s) {models_keys} do not match name: '{name}' "
            f"— placeholder rename incomplete (expected a 'models: {name}:' block)"
        )
    return errors


def _dbt_project_yml_sanity_errors(session: dict, phase_num: int, pkg_path: str) -> list[str]:
    dbt_nodes = session.get("dbt_nodes", [])
    projects = sorted({
        node.get("project")
        for node in dbt_nodes
        if node.get("phase") == phase_num and node.get("project")
    })
    errors: list[str] = []
    for project in projects:
        project_dir = _dbt_project_dir(session, pkg_path, project)
        if project_dir:
            errors.extend(_check_dbt_project_yml_sanity(project_dir))
    return errors


def _validate_dbt_artifacts(session: dict, phase_num: int, pkg_path: str) -> list[str]:
    """Return a list of validation errors for a dbt phase.

    Checks per dbt project assigned to this phase:
    - stabilization/tests/dbt/{PROJECT}/seeds/ has at least 1 .csv
    - stabilization/tests/dbt/{PROJECT}/tests/ has at least 1 .sql
    - stabilization/tests/dbt/{PROJECT}/test_report.md exists
    - dbt_learnings_{project}.md exists in phase dir
    - All dbt nodes assigned to this phase have terminal status
    - dbt_project.yml `models:` top-level key matches `name:` (incomplete bootstrap)
    """
    errors: list[str] = []

    dbt_nodes = session.get("dbt_nodes", [])
    projects = {node.get("project") for node in dbt_nodes if node.get("phase") == phase_num and node.get("project")}

    if not projects:
        errors.append(f"No dbt projects found assigned to phase {phase_num}")
        return errors

    for project in sorted(projects):
        if pkg_path:
            stab_tests_dir = tests_dir(pkg_path)
            seeds_directory = stab_tests_dir / "dbt" / project / "seeds"
            tests_directory = stab_tests_dir / "dbt" / project / "tests"
            report_file = stab_tests_dir / "dbt" / project / "test_report.md"
            learnings_name = f"dbt_learnings_{project}.md"
            learnings_file = next(
                (
                    candidate / learnings_name
                    for candidate in phase_dir_candidates(pkg_path, phase_num)
                    if (candidate / learnings_name).is_file()
                ),
                resolve_phase_dir(pkg_path, phase_num) / learnings_name,
            )

            if not seeds_directory.is_dir() or not any(seeds_directory.glob("*.csv")):
                errors.append(f"Missing dbt artifact: {seeds_directory} has no .csv seed files")
            if not tests_directory.is_dir() or not any(tests_directory.glob("*.sql")):
                errors.append(f"Missing dbt artifact: {tests_directory} has no .sql test files")
            if not report_file.is_file():
                errors.append(f"Missing dbt artifact: {report_file} not found")
            if not learnings_file.is_file() and not fix_log_path(pkg_path).is_file():
                errors.append(f"Missing dbt artifact: {learnings_file} not found")
            project_dir = _dbt_project_dir(session, pkg_path, project)
            if project_dir:
                errors.extend(_check_dbt_project_yml_sanity(project_dir))
        else:
            errors.append("Missing artifact: migration_object_path not set in session; cannot locate dbt test artifacts")

    node_terminal_statuses = TERMINAL_STATUSES | {"passing", "unverified"}
    non_terminal_nodes = [
        node["name"]
        for node in dbt_nodes
        if node.get("phase") == phase_num and node.get("status") not in node_terminal_statuses
    ]
    if non_terminal_nodes:
        errors.append(
            f"dbt nodes not in terminal status ({', '.join(non_terminal_nodes)}): "
            f"all dbt nodes must be resolved before completing phase"
        )

    return errors


def _validate_dataflow_proc_artifacts(session: dict, phase_num: int, pkg_path: str) -> list[str]:
    """Return a list of validation errors for a dataflow-proc (Snowflake Scripting) phase.

    A converted mapping procedure assigned to this phase is tracked as an element.
    Checks per procedure:
    - stabilization/tests/proc/{PROC}/test_report.md exists
    - All procedures assigned to this phase have terminal status
    """
    errors: list[str] = []

    phase_elements = [el for el in session["elements"] if el.get("phase") == phase_num]
    if not phase_elements:
        errors.append(f"No mapping procedures found assigned to phase {phase_num}")
        return errors

    if pkg_path:
        stab_tests_dir = tests_dir(pkg_path)
        for el in phase_elements:
            report_file = stab_tests_dir / "proc" / el["name"] / "test_report.md"
            if not report_file.is_file():
                errors.append(f"Missing proc artifact: {report_file} not found")
    else:
        errors.append("Missing artifact: migration_object_path not set in session; cannot locate proc test artifacts")

    non_terminal = [el["name"] for el in phase_elements if el["status"] not in TERMINAL_STATUSES]
    if non_terminal:
        errors.append(
            f"Mapping procedures not in terminal status ({', '.join(non_terminal)}): "
            f"all procedures must be resolved before completing phase"
        )

    return errors


def _phase_scope(session: dict, phase_num: int) -> str:
    phases = session.get("roadmap", {}).get("phases", [])
    phase_data = next((p for p in phases if p["phase"] == phase_num), None)
    explicit_scope = (phase_data or {}).get("scope")
    if explicit_scope:
        return explicit_scope

    if any(node.get("phase") == phase_num for node in session.get("dbt_nodes", [])):
        return "dbt"

    return "orchestration"


def _validate_phase_artifacts(session: dict, phase_num: int) -> list[str]:
    """Return validation errors for a phase based on its scope.

    Dispatches to the appropriate validator:
    - orchestration (default) → _validate_orch_artifacts
    - dbt → _validate_dbt_artifacts
    - dataflow-proc → _validate_dataflow_proc_artifacts
    - final-validation → checks all elements terminal + artifacts/report.html
    """
    scope = _phase_scope(session, phase_num)
    pkg_path = session.get("migration_object_path", "")

    if scope == "dbt":
        return _validate_dbt_artifacts(session, phase_num, pkg_path)

    if scope == "dataflow-proc":
        return _validate_dataflow_proc_artifacts(session, phase_num, pkg_path)

    if scope in ("final-validation", "validation"):
        errors: list[str] = []
        non_terminal = [
            el["name"] for el in session["elements"] if el["status"] not in TERMINAL_STATUSES
        ]
        if non_terminal:
            errors.append(
                f"Elements not in terminal status across all phases ({', '.join(non_terminal)}): "
                f"final-validation requires all elements resolved"
            )
        if pkg_path:
            report = report_path(pkg_path)
            if not report.is_file():
                errors.append(f"Missing artifact: {report} not found")
        else:
            errors.append("Missing artifact: migration_object_path not set; cannot locate report.html")
        return errors

    # Default: orchestration
    return _validate_orch_artifacts(session, phase_num, pkg_path)


def cmd_complete_phase(status_path: Path, phase_num: int) -> None:
    session = load_json(status_path)
    if "roadmap" not in session:
        print("Error: no roadmap in session. Run init-roadmap first.", file=sys.stderr)
        sys.exit(1)

    found = None
    for phase in session["roadmap"]["phases"]:
        if phase["phase"] == phase_num:
            found = phase
            break

    if found is None:
        print(f"Error: phase {phase_num} not found in roadmap", file=sys.stderr)
        sys.exit(1)

    if found["status"] == "completed":
        print(f"Error: phase {phase_num} is already completed", file=sys.stderr)
        sys.exit(1)

    errors = _validate_phase_artifacts(session, phase_num)
    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    found["status"] = "completed"
    found["completed_at"] = now_iso()
    session["last_updated"] = now_iso()
    save_json(status_path, session)

    print(f"Phase {phase_num} marked as completed")


# ---------------------------------------------------------------------------
# start-phase
# ---------------------------------------------------------------------------

def cmd_start_phase(status_path: Path, phase_num: int) -> None:
    session = load_json(status_path)
    if "roadmap" not in session:
        print("Error: no roadmap in session. Run init-roadmap first.", file=sys.stderr)
        sys.exit(1)

    found = None
    for phase in session["roadmap"]["phases"]:
        if phase["phase"] == phase_num:
            found = phase
            break

    if found is None:
        print(f"Error: phase {phase_num} not found in roadmap", file=sys.stderr)
        sys.exit(1)

    found["started_at"] = now_iso()
    found["status"] = "in_progress"
    session["last_updated"] = now_iso()
    save_json(status_path, session)
    print(f"Phase {phase_num} started")


# ---------------------------------------------------------------------------
# update-state
# ---------------------------------------------------------------------------

def _generate_state_md(session: dict, current_phase: int, phase_status: str, next_action: str) -> str:
    roadmap = session.get("roadmap", {})
    phases = roadmap.get("phases", [])
    total_phases = len(phases)
    current_phase_name = ""
    for p in phases:
        if p["phase"] == current_phase:
            current_phase_name = p["name"]
            break

    total_elements = len(session["elements"])
    completed_statuses = {"test-passed", "fixed", "skipped", "no-fix-needed"}
    completed_count = sum(1 for el in session["elements"] if el["status"] in completed_statuses)
    pct = int(completed_count / total_elements * 100) if total_elements > 0 else 0
    filled = pct // 10
    bar = "\u2588" * filled + "\u2591" * (10 - filled)

    ewi_count = sum(1 for el in session["elements"] if el.get("initial_issues"))
    clean_count = total_elements - ewi_count
    dbt_count = len(session.get("dbt_projects", []))

    decisions = []
    for p in phases:
        for d in p.get("decisions", []):
            decisions.append(f"- Phase {p['phase']}: {d}")

    blockers = session.get("blockers", [])

    lines = [
        f"# State: {session['migration_object']}",
        "",
        "## Current Position",
        f"Phase: {current_phase} of {total_phases} ({current_phase_name})",
        f"Status: {phase_status}",
        f"Last activity: {session['last_updated'][:10]}",
        "",
        f"Progress: [{bar}] {pct}%",
        "",
        "## Migration Unit",
        f"{total_elements} elements ({ewi_count} EWI, {clean_count} clean) | {dbt_count} dbt projects",
        "",
        "## Decisions",
    ]
    if decisions:
        lines.extend(decisions)
    else:
        lines.append("(none yet)")
    lines.append("")
    lines.append("## Blockers")
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("## Session Continuity")
    lines.append(f"Last session: {now_iso()[:19]}")
    lines.append(f"Next action: {next_action}")
    lines.append("")

    return "\n".join(lines)


def cmd_update_state(status_path: Path, current_phase: int, phase_status: str, next_action: str) -> None:
    with _locked(status_path):
        session = load_json(status_path)
        if "roadmap" not in session:
            print("Error: no roadmap in session. Run init-roadmap first.", file=sys.stderr)
            sys.exit(1)
        session["last_updated"] = now_iso()
        if "planning_completed_at" not in session:
            session["planning_completed_at"] = now_iso()
        save_json(status_path, session)

        state_md = _generate_state_md(session, current_phase, phase_status, next_action)
        state_dir = status_path.parent
        state_path = state_dir / "STATE.md"
        state_path.write_text(state_md, encoding="utf-8")

    print(f"STATE.md generated: {state_path}")


# ---------------------------------------------------------------------------
# add-phase
# ---------------------------------------------------------------------------

def cmd_add_phase(status_path: Path, phase_num: int, name: str, goal: str, scope: str,
                   parallel_safe: bool = False, depends_on: list[int] | None = None) -> None:
    session = load_json(status_path)
    if "roadmap" not in session:
        print("Error: no roadmap in session. Run init-roadmap first.", file=sys.stderr)
        sys.exit(1)

    for phase in session["roadmap"]["phases"]:
        if phase["phase"] == phase_num:
            print(f"Error: phase {phase_num} already exists in roadmap", file=sys.stderr)
            sys.exit(1)

    session["roadmap"]["phases"].append({
        "phase": phase_num,
        "name": name,
        "goal": goal,
        "scope": scope,
        "status": "pending",
        "decisions": [],
        "parallel_safe": parallel_safe,
        "depends_on": depends_on or [],
    })
    session["roadmap"]["phases"].sort(key=lambda p: p["phase"])

    session["last_updated"] = now_iso()
    save_json(status_path, session)

    print(f"Phase {phase_num} ({name}) added to roadmap")


# ---------------------------------------------------------------------------
# add-decision
# ---------------------------------------------------------------------------

def cmd_add_decision(status_path: Path, phase_num: int, decision: str) -> None:
    session = load_json(status_path)
    if "roadmap" not in session:
        print("Error: no roadmap in session. Run init-roadmap first.", file=sys.stderr)
        sys.exit(1)

    found = None
    for phase in session["roadmap"]["phases"]:
        if phase["phase"] == phase_num:
            found = phase
            break

    if found is None:
        print(f"Error: phase {phase_num} not found in roadmap", file=sys.stderr)
        sys.exit(1)

    found["decisions"].append(decision)
    session["last_updated"] = now_iso()
    save_json(status_path, session)

    print(f"Decision added to phase {phase_num}")


# ---------------------------------------------------------------------------
# assign-phases
# ---------------------------------------------------------------------------

def cmd_assign_phases(status_path: Path, phase: int, element_names: list[str], strategy: str) -> None:
    with _locked(status_path):
        session = load_json(status_path)
        updated = 0
        for el in session["elements"]:
            if el["name"] in element_names:
                el["phase"] = phase
                el["test_strategy"] = strategy
                updated += 1

        if updated == 0:
            print("Warning: no elements matched the provided names", file=sys.stderr)
            sys.exit(1)

        session["last_updated"] = now_iso()
        save_json(status_path, session)

    print(f"Assigned {updated} elements to phase {phase} with strategy '{strategy}'")


# ---------------------------------------------------------------------------
# assign-dbt-phase
# ---------------------------------------------------------------------------

def cmd_assign_dbt_phase(status_path: Path, phase: int, project: str) -> None:
    with _locked(status_path):
        session = load_json(status_path)
        updated = 0
        for node in session.get("dbt_nodes", []):
            if node.get("project") == project:
                node["phase"] = phase
                updated += 1

        if updated == 0:
            print(f"Warning: no dbt_nodes found for project '{project}'", file=sys.stderr)
            sys.exit(1)

        session["last_updated"] = now_iso()
        save_json(status_path, session)
    print(f"Assigned {updated} dbt nodes in project '{project}' to phase {phase}")


# ---------------------------------------------------------------------------
# batch-assign-phases
# ---------------------------------------------------------------------------

def cmd_batch_assign_phases(status_path: Path, assignments_json: str) -> None:
    """Assign elements to multiple phases in a single atomic operation."""
    try:
        assignments = json.loads(assignments_json)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in assignments: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(assignments, list):
        print("Error: assignments must be a JSON array", file=sys.stderr)
        sys.exit(1)

    for i, entry in enumerate(assignments):
        for key in ("phase", "elements", "strategy"):
            if key not in entry:
                print(f"Error: assignment[{i}] missing required key '{key}'", file=sys.stderr)
                sys.exit(1)

    with _locked(status_path):
        session = load_json(status_path)

        roadmap_phases = {p["phase"] for p in session.get("roadmap", {}).get("phases", [])}
        if roadmap_phases:
            for i, entry in enumerate(assignments):
                if entry["phase"] not in roadmap_phases:
                    print(f"Warning: assignment[{i}] references phase {entry['phase']} which does not exist in roadmap (available: {sorted(roadmap_phases)})", file=sys.stderr)

        total_updated = 0
        for entry in assignments:
            phase = entry["phase"]
            element_set = set(entry["elements"])
            strategy = entry["strategy"]
            for el in session["elements"]:
                if el["name"] in element_set:
                    el["phase"] = phase
                    el["test_strategy"] = strategy
                    total_updated += 1

        if total_updated == 0:
            print("Warning: no elements matched any provided names", file=sys.stderr)
            sys.exit(1)

        session["last_updated"] = now_iso()
        save_json(status_path, session)

    print(f"Batch-assigned {total_updated} elements across {len(assignments)} phases")


# ---------------------------------------------------------------------------
# validate-phase
# ---------------------------------------------------------------------------

def cmd_validate_phase(status_path: Path, phase_num: int, list_test_files: bool = False) -> None:
    session = load_json(status_path)

    scope = _phase_scope(session, phase_num)

    if scope == "dbt":
        _validate_dbt_phase(session, status_path, phase_num, list_test_files)
        return

    phase_els = [e for e in session["elements"] if e.get("phase") == phase_num]
    if not phase_els:
        print(f"Error: no elements assigned to phase {phase_num}", file=sys.stderr)
        sys.exit(1)

    ewi_count = 0
    line_count = 0
    orch_file = session.get("orchestration_file")
    if orch_file and Path(orch_file).is_file():
        content = Path(orch_file).read_text(encoding="utf-8", errors="replace")
        ewi_count = len(re.findall(r"!!!RESOLVE EWI!!!", content))
        line_count = len(content.splitlines())

    status_counts: dict[str, int] = {}
    for el in phase_els:
        s = el["status"]
        status_counts[s] = status_counts.get(s, 0) + 1

    fixed = status_counts.get("fixed", 0) + status_counts.get("test-passed", 0) + status_counts.get("no-fix-needed", 0)
    needs_user = status_counts.get("needs-user", 0) + status_counts.get("auto-fixed-needs-review", 0)
    failed = status_counts.get("failed", 0) + status_counts.get("test-failed", 0)
    pending = status_counts.get("pending", 0) + status_counts.get("in_progress", 0)
    skipped = status_counts.get("skipped", 0)

    print(f"=== Phase {phase_num} Validation ===")
    print(f"Orchestration file: {line_count} lines, {ewi_count} EWI markers (file-wide, not phase-scoped)")
    print(f"Elements: {len(phase_els)} total")
    print(f"  Fixed/passed: {fixed}")
    print(f"  Needs-user:   {needs_user}")
    print(f"  Failed:       {failed}")
    print(f"  Pending:      {pending}")
    print(f"  Skipped:      {skipped}")

    if list_test_files:
        pkg_path = session.get("migration_object_path", "")
        test_directory = (tests_dir(pkg_path) / "orchestration") if pkg_path else None
        seen: set[str] = set()
        found: list[str] = []
        for el in phase_els:
            strategy = el.get("test_strategy") or ""
            if strategy.startswith("grouped:"):
                group_name = strategy.split(":", 1)[1]
                short_name = f"grouped_{group_name}"
            else:
                short_name = el["name"].rsplit(".", 1)[-1]
            fname = f"{short_name}.sql"
            if fname in seen:
                continue
            seen.add(fname)
            if test_directory:
                matches = sorted(test_directory.rglob(fname))
                if not matches:
                    found.append(f"{fname}: (not found)")
                elif len(matches) == 1:
                    found.append(str(matches[0]))
                else:
                    found.append(
                        f"{fname}: {len(matches)} candidates — "
                        f"{', '.join(str(m) for m in matches)} (verify)"
                    )
        print(f"\nTest files ({len(found)}):")
        for f in found:
            print(f"  {f}")

    ok = failed == 0 and pending == 0
    if ok:
        print("PASS: All elements resolved.")
    else:
        reasons = []
        if pending > 0:
            reasons.append(f"{pending} elements still pending")
        if failed > 0:
            reasons.append(f"{failed} elements failed")
        print(f"FAIL: {'; '.join(reasons)}")
        sys.exit(1)


def _validate_dbt_phase(session: dict, status_path: Path, phase_num: int, list_test_files: bool) -> None:
    pkg_path = session.get("migration_object_path", "")
    dbt_nodes = [n for n in session.get("dbt_nodes", []) if n.get("phase") == phase_num]
    if not dbt_nodes:
        print(f"Error: no dbt nodes assigned to phase {phase_num}", file=sys.stderr)
        sys.exit(1)

    status_counts: dict[str, int] = {}
    for node in dbt_nodes:
        s = node["status"]
        status_counts[s] = status_counts.get(s, 0) + 1

    fixed = (
        status_counts.get("fixed", 0)
        + status_counts.get("test-passed", 0)
        + status_counts.get("no-fix-needed", 0)
        + status_counts.get("passing", 0)
        + status_counts.get("unverified", 0)
    )
    needs_user = status_counts.get("needs-user", 0) + status_counts.get("auto-fixed-needs-review", 0)
    failed = status_counts.get("failed", 0) + status_counts.get("test-failed", 0)
    pending = status_counts.get("pending", 0) + status_counts.get("in_progress", 0)

    print(f"=== Phase {phase_num} Validation (dbt) ===")
    print(f"dbt nodes: {len(dbt_nodes)} total")
    print(f"  Fixed/passed: {fixed}")
    print(f"  Needs-user:   {needs_user}")
    print(f"  Failed:       {failed}")
    print(f"  Pending:      {pending}")

    if list_test_files:
        projects = sorted({n.get("project") for n in dbt_nodes if n.get("project")})
        stab_tests_dir = tests_dir(pkg_path) if pkg_path else None
        for project in projects:
            if stab_tests_dir:
                project_tests = stab_tests_dir / "dbt" / project / "tests"
                for f in sorted(project_tests.glob("*.sql")) if project_tests.is_dir() else []:
                    print(f"  {f}")

    yml_errors = _dbt_project_yml_sanity_errors(session, phase_num, pkg_path) if pkg_path else []
    for err in yml_errors:
        print(f"Error: {err}", file=sys.stderr)

    ok = failed == 0 and pending == 0 and not yml_errors
    if ok:
        print("PASS: All dbt nodes resolved.")
    else:
        reasons = []
        if pending > 0:
            reasons.append(f"{pending} nodes still pending")
        if failed > 0:
            reasons.append(f"{failed} nodes failed")
        if yml_errors:
            reasons.append(f"{len(yml_errors)} dbt_project.yml sanity error(s)")
        print(f"FAIL: {'; '.join(reasons)}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# update-dbt
# ---------------------------------------------------------------------------

def cmd_update_dbt(status_path: Path, project_name: str, status: str, reason: str | None) -> None:
    if status not in VALID_DBT_STATUSES:
        print(f"Error: invalid dbt status '{status}'. Valid: {', '.join(sorted(VALID_DBT_STATUSES))}", file=sys.stderr)
        sys.exit(1)

    with _locked(status_path):
        session = load_json(status_path)
        dbt_projects = session.get("dbt_projects", [])

        found = None
        for proj in dbt_projects:
            if proj["name"] == project_name:
                found = proj
                break

        if found is None:
            print(f"Error: dbt project '{project_name}' not found", file=sys.stderr)
            sys.exit(1)

        found["status"] = status
        if reason is not None:
            found["reason"] = reason
        elif "reason" in found and status not in ("dbt-failed", "skipped"):
            del found["reason"]

        session["last_updated"] = now_iso()
        save_json(status_path, session)
    print(f"Updated dbt project '{project_name}' -> {status}")


# ---------------------------------------------------------------------------
# init-dbt
# ---------------------------------------------------------------------------

def cmd_init_dbt(status_path: Path, project_name: str, dbt_project_path: Path) -> None:
    with _locked(status_path):
        session = load_json(status_path)
        dbt_projects = session.get("dbt_projects", [])

        found = None
        for proj in dbt_projects:
            if proj["name"] == project_name:
                found = proj
                break

        if found is None:
            print(f"Error: dbt project '{project_name}' not found in session", file=sys.stderr)
            sys.exit(1)

        models_dir = dbt_project_path / "models"
        nodes: list[dict] = []
        if models_dir.is_dir():
            for sql_file in sorted(models_dir.rglob("*.sql")):
                rel = str(sql_file.relative_to(dbt_project_path))
                node_name = sql_file.stem
                nodes.append({
                    "name": node_name,
                    "path": rel,
                    "status": "pending",
                })

        found["nodes"] = nodes
        # Also populate top-level dbt_nodes for validation queries
        top_nodes = session.setdefault("dbt_nodes", [])
        # Remove existing nodes for this project (idempotent)
        top_nodes[:] = [n for n in top_nodes if n.get("project") != project_name]
        for node in nodes:
            top_nodes.append({
                "name": node["name"],
                "path": node["path"],
                "status": node["status"],
                "project": project_name,
                "phase": None,
            })
        session["last_updated"] = now_iso()
        save_json(status_path, session)
    print(f"Initialized {len(nodes)} dbt nodes for project '{project_name}'")


# ---------------------------------------------------------------------------
# update-dbt-node
# ---------------------------------------------------------------------------

def cmd_update_dbt_node(status_path: Path, project_name: str, node_name: str, status: str, reason: str | None) -> None:
    if status not in VALID_DBT_NODE_STATUSES:
        print(f"Error: invalid dbt node status '{status}'. Valid: {', '.join(sorted(VALID_DBT_NODE_STATUSES))}", file=sys.stderr)
        sys.exit(1)

    with _locked(status_path):
        session = load_json(status_path)
        proj = None
        for p in session.get("dbt_projects", []):
            if p["name"] == project_name:
                proj = p
                break
        if proj is None:
            print(f"Error: dbt project '{project_name}' not found", file=sys.stderr)
            sys.exit(1)

        nodes = proj.get("nodes", [])
        found = None
        for node in nodes:
            if node["name"] == node_name:
                found = node
                break
        if found is None:
            print(f"Error: node '{node_name}' not found in project '{project_name}'", file=sys.stderr)
            sys.exit(1)

        found["status"] = status
        if reason is not None:
            found["reason"] = reason
        elif "reason" in found and status not in ("failed", "skipped", "unverified"):
            del found["reason"]

        for top_node in session.get("dbt_nodes", []):
            if top_node.get("project") == project_name and top_node.get("name") == node_name:
                top_node["status"] = status
                if reason is not None:
                    top_node["reason"] = reason
                elif "reason" in top_node and status not in ("failed", "skipped", "unverified"):
                    del top_node["reason"]
                break

        session["last_updated"] = now_iso()
        save_json(status_path, session)
    print(f"Updated node '{node_name}' in '{project_name}' -> {status}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py init <scan.json>", file=sys.stderr)
            sys.exit(1)
        scan_path = Path(sys.argv[2])
        if not scan_path.is_file():
            print(f"Error: '{scan_path}' not found", file=sys.stderr)
            sys.exit(1)
        cmd_init(scan_path)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python track_status.py update <session_status.json> <element_name> --status <status> [--reason <reason>]", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        element_name = sys.argv[3]

        status = None
        reason = None
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                reason = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if status is None:
            print("Error: --status is required", file=sys.stderr)
            sys.exit(1)

        cmd_update(status_path, element_name, status, reason)

    elif command == "set-test-env":
        if len(sys.argv) < 5:
            print("Usage: python track_status.py set-test-env <session_status.json> <database> <schema>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        cmd_set_test_env(status_path, sys.argv[3], sys.argv[4])

    elif command == "init-roadmap":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py init-roadmap <session_status.json> --phases-json '<json>' | --phases-file <path>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        phases_json = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--phases-json" and i + 1 < len(sys.argv):
                phases_json = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--phases-file" and i + 1 < len(sys.argv):
                phases_file = Path(sys.argv[i + 1])
                if not phases_file.is_file():
                    print(f"Error: phases file '{phases_file}' not found", file=sys.stderr)
                    sys.exit(1)
                phases_json = phases_file.read_text(encoding="utf-8").strip()
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if phases_json is None:
            print("Error: --phases-json or --phases-file is required", file=sys.stderr)
            sys.exit(1)

        cmd_init_roadmap(status_path, phases_json)

    elif command == "assign-phases":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py assign-phases <session_status.json> --phase <N> --elements <csv> --strategy <strategy>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        phase = None
        element_names: list[str] = []
        strategy = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--phase" and i + 1 < len(sys.argv):
                phase = parse_int(sys.argv[i + 1], "phase")
                i += 2
            elif sys.argv[i] == "--elements" and i + 1 < len(sys.argv):
                element_names = [n.strip() for n in sys.argv[i + 1].split(",") if n.strip()]
                i += 2
            elif sys.argv[i] == "--elements-file" and i + 1 < len(sys.argv):
                elements_file = Path(sys.argv[i + 1])
                if not elements_file.is_file():
                    print(f"Error: elements file '{elements_file}' not found", file=sys.stderr)
                    sys.exit(1)
                element_names = [n.strip() for n in elements_file.read_text(encoding="utf-8").splitlines() if n.strip()]
                i += 2
            elif sys.argv[i] == "--strategy" and i + 1 < len(sys.argv):
                strategy = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if phase is None:
            print("Error: --phase is required", file=sys.stderr)
            sys.exit(1)
        if not element_names:
            print("Error: --elements or --elements-file is required", file=sys.stderr)
            sys.exit(1)
        if strategy is None:
            print("Error: --strategy is required", file=sys.stderr)
            sys.exit(1)

        cmd_assign_phases(status_path, phase, element_names, strategy)

    elif command == "assign-dbt-phase":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py assign-dbt-phase <session_status.json> --phase <N> --project <name>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        phase = None
        project = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--phase" and i + 1 < len(sys.argv):
                phase = parse_int(sys.argv[i + 1], "phase")
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                project = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if phase is None or project is None:
            print("Error: --phase and --project are required", file=sys.stderr)
            sys.exit(1)

        cmd_assign_dbt_phase(status_path, phase, project)

    elif command == "batch-assign-phases":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py batch-assign-phases <session_status.json> --assignments-file <path> | --assignments-json '<json>'", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        assignments_json = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--assignments-file" and i + 1 < len(sys.argv):
                assignments_file = Path(sys.argv[i + 1])
                if not assignments_file.is_file():
                    print(f"Error: assignments file '{assignments_file}' not found", file=sys.stderr)
                    sys.exit(1)
                assignments_json = assignments_file.read_text(encoding="utf-8").strip()
                i += 2
            elif sys.argv[i] == "--assignments-json" and i + 1 < len(sys.argv):
                assignments_json = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if assignments_json is None:
            print("Error: --assignments-file or --assignments-json is required", file=sys.stderr)
            sys.exit(1)

        cmd_batch_assign_phases(status_path, assignments_json)

    elif command == "update-state":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py update-state <session_status.json> --current-phase <N> --phase-status <text> --next-action <text>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        current_phase = None
        phase_status = None
        next_action = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--current-phase" and i + 1 < len(sys.argv):
                current_phase = parse_int(sys.argv[i + 1], "current-phase")
                i += 2
            elif sys.argv[i] == "--phase-status" and i + 1 < len(sys.argv):
                phase_status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--next-action" and i + 1 < len(sys.argv):
                next_action = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if current_phase is None or phase_status is None or next_action is None:
            print("Error: --current-phase, --phase-status, and --next-action are all required", file=sys.stderr)
            sys.exit(1)

        cmd_update_state(status_path, current_phase, phase_status, next_action)

    elif command == "start-phase":
        if len(sys.argv) < 4:
            print("Usage: python track_status.py start-phase <session_status.json> <phase_num>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        phase_num = parse_int(sys.argv[3], "phase_num")
        cmd_start_phase(status_path, phase_num)

    elif command == "complete-phase":
        if len(sys.argv) < 4:
            print("Usage: python track_status.py complete-phase <session_status.json> <phase_num>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        phase_num = parse_int(sys.argv[3], "phase_num")
        cmd_complete_phase(status_path, phase_num)

    elif command == "validate-phase":
        if len(sys.argv) < 4:
            print("Usage: python track_status.py validate-phase <session_status.json> <phase_num> [--list-test-files]", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        phase_num = parse_int(sys.argv[3], "phase_num")
        list_test_files = "--list-test-files" in sys.argv[4:]
        cmd_validate_phase(status_path, phase_num, list_test_files=list_test_files)

    elif command == "add-phase":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py add-phase <session_status.json> --phase <N> --name <name> --goal <goal> --scope <scope> [--parallel-safe] [--depends-on <csv>]", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        phase_num = None
        name = None
        goal = None
        scope = None
        parallel_safe = False
        depends_on: list[int] = []
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--phase" and i + 1 < len(sys.argv):
                phase_num = parse_int(sys.argv[i + 1], "phase")
                i += 2
            elif sys.argv[i] == "--name" and i + 1 < len(sys.argv):
                name = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--goal" and i + 1 < len(sys.argv):
                goal = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--scope" and i + 1 < len(sys.argv):
                scope = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--parallel-safe":
                parallel_safe = True
                i += 1
            elif sys.argv[i] == "--depends-on" and i + 1 < len(sys.argv):
                depends_on = [int(x.strip()) for x in sys.argv[i + 1].split(",") if x.strip()]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if phase_num is None or name is None or goal is None or scope is None:
            print("Error: --phase, --name, --goal, and --scope are all required", file=sys.stderr)
            sys.exit(1)

        cmd_add_phase(status_path, phase_num, name, goal, scope, parallel_safe, depends_on)

    elif command == "add-decision":
        if len(sys.argv) < 3:
            print("Usage: python track_status.py add-decision <session_status.json> --phase <N> --decision <text>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)

        phase_num = None
        decision = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--phase" and i + 1 < len(sys.argv):
                phase_num = parse_int(sys.argv[i + 1], "phase")
                i += 2
            elif sys.argv[i] == "--decision" and i + 1 < len(sys.argv):
                decision = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if phase_num is None or decision is None:
            print("Error: --phase and --decision are required", file=sys.stderr)
            sys.exit(1)

        cmd_add_decision(status_path, phase_num, decision)

    elif command == "update-dbt":
        if len(sys.argv) < 4:
            print("Usage: python track_status.py update-dbt <session_status.json> <project_name> --status <status> [--reason <reason>]", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        project_name = sys.argv[3]

        status = None
        reason = None
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                reason = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if status is None:
            print("Error: --status is required", file=sys.stderr)
            sys.exit(1)

        cmd_update_dbt(status_path, project_name, status, reason)

    elif command == "init-dbt":
        if len(sys.argv) < 5:
            print("Usage: python track_status.py init-dbt <session_status.json> <project_name> <dbt_project_path>", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        cmd_init_dbt(status_path, sys.argv[3], Path(sys.argv[4]))

    elif command == "update-dbt-node":
        if len(sys.argv) < 5:
            print("Usage: python track_status.py update-dbt-node <session_status.json> <project_name> <node_name> --status <status> [--reason <reason>]", file=sys.stderr)
            sys.exit(1)
        status_path = Path(sys.argv[2])
        if not status_path.is_file():
            print(f"Error: '{status_path}' not found", file=sys.stderr)
            sys.exit(1)
        project_name = sys.argv[3]
        node_name = sys.argv[4]

        status = None
        reason = None
        i = 5
        while i < len(sys.argv):
            if sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                reason = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: unexpected argument '{sys.argv[i]}'", file=sys.stderr)
                sys.exit(1)

        if status is None:
            print("Error: --status is required", file=sys.stderr)
            sys.exit(1)

        cmd_update_dbt_node(status_path, project_name, node_name, status, reason)

    else:
        print(f"Error: unknown command '{command}'", file=sys.stderr)
        print(f"Run without arguments to see usage.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
