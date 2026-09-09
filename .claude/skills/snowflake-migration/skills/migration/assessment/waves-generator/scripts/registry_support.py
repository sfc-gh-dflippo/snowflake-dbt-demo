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

"""Helpers for registry-native waves/dependency analysis."""

from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, Iterable, List

_scripts_dir = str(Path(__file__).resolve().parent.parent.parent / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports.na_utils import (
    NA_VALUES as _NA_VALUES,
    is_na,
    sanitize_na,
    strip_na_identifier,
)

VALID_OBJECT_TYPES = {"TABLE", "VIEW", "PROCEDURE", "FUNCTION", "EXTERNAL TABLE"}


def bracket_identifier(identifier: str) -> str:
    """Return a bracketed SQL identifier without double-bracketing."""
    identifier = (identifier or "").strip()
    if not identifier:
        return "[]"
    if identifier.startswith("[") and identifier.endswith("]"):
        return identifier
    return f"[{identifier}]"


def registry_object_type(entry: Dict[str, Any]) -> str:
    """Return normalized object type from a registry entry."""
    return entry.get("source", {}).get("objectType", "").strip().upper()


def build_callable_suffix(entry: Dict[str, Any]) -> str:
    """Build ``(TYPE,TYPE)`` suffix for procedures/functions."""
    if registry_object_type(entry) not in {"PROCEDURE", "FUNCTION"}:
        return ""

    arguments = (
        entry.get("signature", {})
        .get("parameters", {})
        .get("arguments", [])
    )
    types = [(arg.get("type") or "").strip() for arg in arguments]
    return f"({','.join(types)})"


def build_registry_object_id(entry: Dict[str, Any]) -> str:
    """Build waves-compatible object ID from a registry entry.

    Output format: ``[database].[schema].[name]`` for tables/views and
    ``[database].[schema].[name](TYPE,...)`` for procedures/functions.

    N/A source properties (database, schema, name) are omitted.
    """
    source = entry.get("source", {})
    raw_db = source.get("database", "")
    raw_schema = source.get("schema", "")
    raw_name = source.get("name", "")
    parts = [
        bracket_identifier(v)
        for v in (raw_db, raw_schema, raw_name)
        if not is_na(v) and not is_na(v.strip("[]"))
    ]
    base = ".".join(parts) if parts else "[]"
    return f"{base}{build_callable_suffix(entry)}"


def load_registry_entries(registry_dir: str | Path) -> List[Dict[str, Any]]:
    """Load all registry entries from a flat JSON directory."""
    registry_path = Path(registry_dir)
    entries: List[Dict[str, Any]] = []
    for path in sorted(registry_path.glob("*.json")):
        try:
            with path.open(encoding="utf-8") as handle:
                entries.append(json.load(handle))
        except (OSError, json.JSONDecodeError) as exc:
            warnings.warn(f"Skipping malformed registry file {path.name}: {exc}")
    return entries


def iter_in_scope_entries(entries: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    """Yield in-scope registry entries."""
    for entry in entries:
        if entry.get("inScope", False):
            yield entry


def is_deployable_entry(entry: Dict[str, Any]) -> bool:
    """Return whether a registry entry is a deployable SQL object."""
    if entry.get("kind") != "databaseObject":
        return False
    if entry.get("isMissing", False):
        return False
    if not entry.get("inScope", False):
        return False
    return registry_object_type(entry) in VALID_OBJECT_TYPES


def _compute_conversion_status(entry: Dict[str, Any]) -> str:
    """Map registry codeStatus + issues to waves-compatible conversion status.

    Registry semantics (vs CSV ConversionStatus):
    - conversion.status = "pending" → "Pending Conversion" (not yet converted)
    - conversion.status = "completed":
      - No issues or empty issues → "Success"
      - Has issues (SSC-EWI, SSC-FDM, etc.) → "Require Attention"
    - conversion.status in ("notsupported", "not_supported", "NotSupported", "failed") → "Not Supported"
    - Fallback: assessment.status or raw conversion.status
    """
    code_status = entry.get("codeStatus", {})
    conversion_raw = (
        code_status.get("conversion", {}).get("status", "")
    ).strip().lower()
    assessment_raw = (
        code_status.get("assessment", {}).get("status", "")
    ).strip().lower()
    issues = entry.get("issues") or []

    if conversion_raw == "pending":
        return "Pending Conversion"

    if conversion_raw == "failed":
        return "Not Supported"

    if conversion_raw == "completed":
        if not issues:
            return "Success"
        return "Require Attention"

    # Fallback: assessment failed (non-missing) → Not Supported
    if assessment_raw == "failed" and not entry.get("isMissing", False):
        return "Not Supported"

    # Preserve known CSV-style values if registry uses them
    if conversion_raw in ("success", "partial", "action required"):
        return conversion_raw.title()

    return "Unknown"


def entry_to_object_info(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Build graph/object metadata from a deployable registry entry."""
    obj_type = registry_object_type(entry)
    return {
        "category": obj_type,
        "code_unit": f"CREATE {obj_type}",
        "file_name": entry.get("files", {}).get("source", {}).get("path", ""),
        "line_number": "0",
        "conversion_status": _compute_conversion_status(entry),
        "deployment_order": str(entry.get("planning", {}).get("topologicalRank", "")),
    }


def build_id_to_entry_map(entries: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Map registry file IDs to full entries."""
    id_to_entry: Dict[str, Dict[str, Any]] = {}
    for entry in entries:
        entry_id = (entry.get("id") or "").strip()
        if entry_id:
            id_to_entry[entry_id] = entry
    return id_to_entry


def build_id_to_object_name_map(entries: Iterable[Dict[str, Any]]) -> Dict[str, str]:
    """Map registry IDs to waves-compatible object identifiers."""
    id_to_name: Dict[str, str] = {}
    for entry in entries:
        entry_id = (entry.get("id") or "").strip()
        if entry_id:
            id_to_name[entry_id] = build_registry_object_id(entry)
    return id_to_name


def missing_dependency_name(dep: Dict[str, Any], fallback_index: int) -> str:
    """Return a deterministic name for a missing dependency."""
    dep_id = (dep.get("id") or "").strip()
    if dep_id:
        return dep_id
    return f"MISSING_DEPENDENCY_{fallback_index:04d}"


def sync_planning_wave_to_registry(
    output_folder: Path,
    registry_dir: str | Path,
) -> Dict[str, int]:
    """Read partition_membership.csv and stamp planning.wave on each registry entry.
    """
    partition_csv = output_folder / "partition_membership.csv"
    if not partition_csv.exists():
        print("Warning: partition_membership.csv not found; skipping registry sync")
        return {"updated": 0, "skipped": 0, "missing_in_registry": 0}

    registry_path = Path(registry_dir)
    entries = load_registry_entries(registry_path)
    name_to_id: Dict[str, str] = {}
    for entry in entries:
        entry_id = (entry.get("id") or "").strip()
        if entry_id:
            name_to_id[build_registry_object_id(entry)] = entry_id

    updated = skipped = missing = 0
    with partition_csv.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            object_name = row.get("object", "")
            try:
                wave = int(row["partition_number"])
            except (KeyError, ValueError):
                skipped += 1
                continue
            entry_id = name_to_id.get(object_name)
            if not entry_id:
                missing += 1
                continue
            entry_path = registry_path / f"{entry_id}.json"
            try:
                with entry_path.open(encoding="utf-8") as f:
                    entry = json.load(f)
            except (OSError, json.JSONDecodeError) as exc:
                warnings.warn(f"Could not read {entry_path.name}: {exc}")
                skipped += 1
                continue
            entry.setdefault("planning", {})["wave"] = wave
            with entry_path.open("w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, sort_keys=True)
                f.write("\n")
            updated += 1

    print(
        f"Synced planning.wave to {updated} registry entries "
        f"({missing} CSV rows had no matching registry entry, "
        f"{skipped} CSV rows skipped)"
    )
    return {"updated": updated, "skipped": skipped, "missing_in_registry": missing}


def build_missing_objects(entries: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Capture in-scope registry entries excluded from graph analysis."""
    missing_objects: Dict[str, Dict[str, Any]] = {}
    for entry in iter_in_scope_entries(entries):
        object_id = build_registry_object_id(entry)
        obj_type = registry_object_type(entry)

        if entry.get("isMissing", False):
            reason = "Registry entry marked missing"
        elif entry.get("kind") != "databaseObject":
            reason = f"Unsupported kind: {sanitize_na(entry.get('kind'))}"
        elif obj_type not in VALID_OBJECT_TYPES:
            reason = f"Unsupported object type: {sanitize_na(obj_type)}"
        else:
            continue

        missing_objects[object_id] = {
            "category": sanitize_na(obj_type),
            "code_unit": f"CREATE {obj_type}" if obj_type else "",
            "file_name": entry.get("files", {}).get("source", {}).get("path", ""),
            "line_number": "0",
            "conversion_status": (
                entry.get("codeStatus", {}).get("conversion", {}).get("status", "")
            ),
            "exclusion_reason": reason,
        }
    return missing_objects
