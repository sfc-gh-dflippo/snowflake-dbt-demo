"""Build and load workflow manifest mapping XML paths to DBT model paths."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


def _find_xml(xml_dir: Path, wf_name: str) -> Path | None:
    """Find XML file for a workflow in the XML directory.

    Matches files ending with 'wf_NAME.xml' (exact suffix match, not substring).
    """
    # Exact suffix match: filename must end with wf_NAME.xml
    wf_upper = wf_name.upper() if wf_name.upper().startswith("WF_") else f"WF_{wf_name.upper()}"
    exact_suffix = f"_{wf_upper}.xml"

    for f in xml_dir.iterdir():
        if f.suffix.lower() == ".xml" and f.stem.upper().endswith(f"_{wf_upper}"):
            return f

    # Also try without the folder prefix separator (some files use wf_NAME directly)
    for pattern in [f"*_{wf_name}.xml", f"*_{wf_name}.XML"]:
        matches = list(xml_dir.glob(pattern))
        if matches:
            return matches[0]

    return None


def dbt_model_candidates(dbt_dir: Path, dbt_model_name: str) -> list[Path]:
    """Every ``.sql`` in the ``_wf`` directory for ``dbt_model_name``, sorted.

    An Informatica workflow's N pipelines become N models in one ``_wf`` directory,
    so this is frequently more than one file and only one of them is the primary.
    """
    matches = list(dbt_dir.rglob(f"{dbt_model_name}/*.sql"))
    if not matches:
        dbt_lower = dbt_model_name.lower()
        for d in dbt_dir.rglob("*_wf"):
            if d.is_dir() and d.name.lower() == dbt_lower:
                matches = list(d.glob("*.sql"))
                break
    return sorted(matches)


def _find_dbt_model(dbt_dir: Path, dbt_model_name: str) -> Path | None:
    """The primary model for ``dbt_model_name``, but only when it is unambiguous.

    Returns the path when the ``_wf`` directory holds exactly one model. Returns
    ``None`` both when nothing matched and when several models matched, because a
    directory with siblings does not say which one is primary and it is frequently
    *not* the model named after the directory. Callers that need to tell those two
    cases apart should ask :func:`dbt_model_candidates`.

    Picking the first glob match here would resolve the ambiguity silently and
    compare against an arbitrary file, which produces a confident verdict about the
    wrong model.

    Args:
        dbt_dir: Root dbt models directory
        dbt_model_name: e.g. 'EL_OOD_ORG_SOB_COMPANY_wf'
    """
    candidates = dbt_model_candidates(dbt_dir, dbt_model_name)
    return candidates[0] if len(candidates) == 1 else None


def _get_git_commit(repo_dir: Path) -> str | None:
    """Get the HEAD commit hash for a git repo."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H %ai %s"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def build_manifest(
    mapping_csv: Path,
    xml_dir: Path,
    dbt_dir: Path,
) -> dict:
    """Build manifest from a workflow-to-model mapping CSV.

    Uses the mapping CSV as the authoritative workflow list.

    Args:
        mapping_csv: CSV with 'Informatica Workflow Name' and 'DBT Model Name' columns
        xml_dir: Directory of Informatica XML exports
        dbt_dir: Root dbt models directory

    Returns:
        Dict with '_preamble' metadata and wf_name -> {xml_path, dbt_path, dbt_model_name}
    """
    manifest: dict[str, dict] = {}

    # Record which commit of the dbt repo the pairing was built against, so a
    # verdict can be traced back to the model revision it was made about.
    dbt_repo_commit = _get_git_commit(dbt_dir)
    manifest["_preamble"] = {
        "dbt_repo_commit": dbt_repo_commit,
        "xml_dir": str(xml_dir),
        "dbt_dir": str(dbt_dir),
        "mapping_csv": str(mapping_csv),
    }

    with open(mapping_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            infa_name = row.get("Informatica Workflow Name", "").strip()
            dbt_model = row.get("DBT Model Name", "").strip()

            if not infa_name:
                continue

            # Normalize workflow name to wf_ prefix
            if not infa_name.lower().startswith("wf_"):
                wf_name = "wf_" + infa_name
            else:
                wf_name = infa_name

            # Find XML
            xml_path = _find_xml(xml_dir, wf_name)

            # Find DBT model. Ambiguity is carried forward rather than resolved
            # here, so the caller can stop and ask instead of comparing an
            # arbitrary sibling.
            dbt_path = _find_dbt_model(dbt_dir, dbt_model) if dbt_model else None
            candidates = dbt_model_candidates(dbt_dir, dbt_model) if dbt_model else []

            entry = {
                "xml_path": str(xml_path) if xml_path else None,
                "dbt_path": str(dbt_path) if dbt_path else None,
                "dbt_model_name": dbt_model,
            }
            if dbt_path is None and len(candidates) > 1:
                entry["dbt_candidates"] = [str(c) for c in candidates]
            manifest[wf_name.lower()] = entry

    return manifest


def save_manifest(manifest: dict, output_path: Path) -> None:
    """Save manifest to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def load_manifest(manifest_path: Path) -> dict[str, dict]:
    """Load manifest from JSON file. Strips _preamble for workflow iteration."""
    with open(manifest_path, encoding="utf-8") as f:
        raw = json.load(f)
    # Strip preamble so callers can iterate workflows directly
    return {k: v for k, v in raw.items() if k != "_preamble"}


def get_testable_workflows(manifest: dict[str, dict]) -> list[str]:
    """Return workflow names that have both XML and DBT paths."""
    return [
        wf for wf, info in manifest.items()
        if wf != "_preamble" and info.get("xml_path") and info.get("dbt_path")
    ]

