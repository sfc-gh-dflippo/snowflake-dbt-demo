"""Single source of truth for all stabilization artifact paths.

This module provides the path resolver for the visible stabilization/ folder.

All scripts MUST use these functions instead of assembling paths ad hoc.
"""
from pathlib import Path


def stabilization_root(code_unit_dir: str | Path) -> Path:
    """Return the root stabilization directory for a code unit.

    Args:
        code_unit_dir: Path to the ETL code unit directory

    Returns:
        Path to {code_unit_dir}/stabilization/

    This is the ONLY location for all stabilization artifacts.
    No files should be written outside this directory.
    """
    return Path(code_unit_dir) / "stabilization"


def planning_dir(code_unit_dir: str | Path) -> Path:
    """Return the planning artifacts directory."""
    return stabilization_root(code_unit_dir) / "planning"


def tracking_dir(code_unit_dir: str | Path) -> Path:
    """Return the tracking artifacts directory."""
    return stabilization_root(code_unit_dir) / "tracking"


def phases_dir(code_unit_dir: str | Path) -> Path:
    """Return the phases directory."""
    return stabilization_root(code_unit_dir) / "phases"


def phase_dir(code_unit_dir: str | Path, phase_num: int) -> Path:
    """Return the canonical phase directory (hyphenated `phase-{N}`)."""
    return phases_dir(code_unit_dir) / f"phase-{phase_num}"


def phase_dir_candidates(code_unit_dir: str | Path, phase_num: int) -> tuple[Path, ...]:
    """Hyphen (`phase-N`) is canonical; underscore (`phase_N`) is still read."""
    root = phases_dir(code_unit_dir)
    candidates = (root / f"phase-{phase_num}", root / f"phase_{phase_num}")
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        key = path.resolve() if path.exists() else path
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return tuple(unique)


def resolve_phase_dir(code_unit_dir: str | Path, phase_num: int) -> Path:
    """Existing phase dir, preferring a populated `phase-N` then `phase_N`."""
    candidates = phase_dir_candidates(code_unit_dir, phase_num)
    existing = [path for path in candidates if path.is_dir()]
    if not existing:
        return candidates[0]
    populated = [path for path in existing if any(path.iterdir())]
    return populated[0] if populated else existing[0]


def original_backup_dir(code_unit_dir: str | Path) -> Path:
    """Return the original backup directory."""
    return stabilization_root(code_unit_dir) / "original"


def tests_dir(code_unit_dir: str | Path) -> Path:
    """Return the tests directory."""
    return stabilization_root(code_unit_dir) / "tests"


def report_path(code_unit_dir: str | Path) -> Path:
    """Return the path to the final HTML report."""
    return stabilization_root(code_unit_dir) / "report.html"


# Specific file paths
def scan_results_path(code_unit_dir: str | Path) -> Path:
    """Return path to scan results JSON."""
    return planning_dir(code_unit_dir) / "scan.json"


def orchestration_context_path(code_unit_dir: str | Path) -> Path:
    """Return path to orchestration context markdown."""
    return planning_dir(code_unit_dir) / "orchestration-context.md"


def dbt_context_path(code_unit_dir: str | Path) -> Path:
    """Return path to dbt context markdown."""
    return planning_dir(code_unit_dir) / "dbt-context.md"


def source_excerpts_path(code_unit_dir: str | Path) -> Path:
    """Return path to source excerpts markdown."""
    return planning_dir(code_unit_dir) / "source-excerpts.md"


def roadmap_path(code_unit_dir: str | Path) -> Path:
    """Return path to ROADMAP markdown."""
    return planning_dir(code_unit_dir) / "ROADMAP.md"


def state_path(code_unit_dir: str | Path) -> Path:
    """Return path to STATE markdown."""
    return tracking_dir(code_unit_dir) / "STATE.md"


def progress_json_path(code_unit_dir: str | Path) -> Path:
    """Return path to progress JSON (session_status.json)."""
    return tracking_dir(code_unit_dir) / "progress.json"


def fix_log_path(code_unit_dir: str | Path) -> Path:
    """Return path to fix log markdown."""
    return tracking_dir(code_unit_dir) / "fix-log.md"
