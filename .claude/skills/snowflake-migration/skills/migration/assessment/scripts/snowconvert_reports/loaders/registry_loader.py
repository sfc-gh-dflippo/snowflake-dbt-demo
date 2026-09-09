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

"""Load SnowConvert data from the registry (flat directory of JSON files)."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

from ..models.code_unit import TopLevelCodeUnit
from ..models.object_reference import ObjectReference
from ..na_utils import NA_VALUES, is_na

VALID_OBJECT_TYPES = {"table", "view", "procedure", "function"}


def _bracket(ident: str) -> str:
    """Ensure an identifier is bracketed, avoiding double-bracketing."""
    ident = (ident or "").strip()
    if not ident:
        return "[]"
    if ident.startswith("[") and ident.endswith("]"):
        return ident
    return f"[{ident}]"


def _entry_full_name(entry: dict) -> str:
    """Build a bracketed identifier from an entry's source (or target) block.

    Falls back to the ``target`` block when ``source`` is absent (e.g. for
    Snowflake-side UDF helpers that have no source counterpart).

    N/A-valued parts (database, schema, name) are omitted so that
    ``[N/A].[dbo].[MyTable]`` becomes ``[dbo].[MyTable]``.

    ETL units (``kind == "etl"``) have no ``source.database/schema/name``;
    their natural identifier is ``files.source.path`` (e.g. the ``.dtsx`` /
    ``.xml`` definition file). Returning the path here lets dependency-edge
    UUID resolution (``build_id_to_name_map``) round-trip ETL units the
    same way SQL units round-trip via ``[db].[schema].[name]``.
    """
    if entry.get("kind") == "etl":
        path = (
            entry.get("files", {}).get("source", {}).get("path", "") or ""
        ).strip()
        if path:
            return path
    block = entry.get("source") or entry.get("target") or {}
    parts = [
        _bracket(v)
        for v in (block.get("database", ""), block.get("schema", ""), block.get("name", ""))
        if not is_na(v) and not is_na(v.strip("[]"))
    ]
    return ".".join(parts) if parts else "[]"


def iter_in_scope_non_missing(entries: list[dict]):
    """Yield entries that are in-scope and not missing."""
    for entry in entries:
        if not entry.get("inScope", False):
            continue
        if entry.get("isMissing", False):
            continue
        yield entry


def load_registry_entries(registry_dir: Path | str) -> list[dict]:
    """Parse all JSON files in *registry_dir*, skipping malformed ones."""
    registry_dir = Path(registry_dir)
    entries: list[dict] = []
    for path in sorted(registry_dir.glob("*.json")):
        try:
            with path.open(encoding="utf-8") as f:
                entries.append(json.load(f))
        except (json.JSONDecodeError, OSError) as exc:
            warnings.warn(f"Skipping malformed registry file {path.name}: {exc}")
    return entries


def build_id_to_name_map(entries: list[dict]) -> dict[str, str]:
    """Build a registry-ID -> ``[DB].[Schema].[Name]`` lookup."""
    mapping: dict[str, str] = {}
    for entry in entries:
        entry_id = entry.get("id") or ""
        if not entry_id:
            continue
        mapping[entry_id] = _entry_full_name(entry)

    return mapping


def load_code_units_from_registry(registry_dir: Path) -> list[TopLevelCodeUnit]:
    """Load in-scope, non-missing code units of valid object types."""
    entries = load_registry_entries(registry_dir)
    units: list[TopLevelCodeUnit] = []
    for entry in iter_in_scope_non_missing(entries):
        obj_type = entry.get("source", {}).get("objectType", "").lower()
        if obj_type not in VALID_OBJECT_TYPES:
            continue
        units.append(TopLevelCodeUnit.from_registry_entry(entry))
    return units


def _iter_unit_dep_specs(entry: dict):
    """Yield ``dependsOn`` entries for a code unit, including those nested
    inside ``parts[*]``.

    SQL units carry their references on the top-level
    ``dependencies.dependsOn`` array. ETL units (``kind == "etl"``) leave
    that array empty and instead store references inside each
    ``parts[i].dependencies.dependsOn``; one referenced object typically
    repeats across many parts. Yielding both shapes lets the caller dedupe
    once and treat ETL units the same way as SQL units in the report.
    """
    seen: set[tuple[str, str, bool]] = set()
    sources: list[list[dict]] = []
    sources.append(entry.get("dependencies", {}).get("dependsOn", []) or [])
    for part in entry.get("parts", []) or []:
        if not isinstance(part, dict):
            continue
        sources.append(part.get("dependencies", {}).get("dependsOn", []) or [])

    for deps in sources:
        for dep in deps:
            if not isinstance(dep, dict):
                continue
            dep_id = dep.get("id") or ""
            is_missing = bool(dep.get("isMissing", False))
            rel_types = tuple(dep.get("relationTypes", []) or [""])
            for rel in rel_types:
                key = (dep_id, rel, is_missing)
                if key in seen:
                    continue
                seen.add(key)
                # Yield a single-relation copy so downstream emits one
                # ObjectReference per (dep, relation_type) pair.
                yield {
                    "id": dep_id,
                    "isMissing": is_missing,
                    "relationTypes": [rel] if rel else [],
                }


def load_object_references_from_registry(
    registry_dir: Path | str,
) -> list[ObjectReference]:
    """Load all object references by flattening ``dependsOn`` arrays.

    For ETL units (``kind == "etl"``), references nested under
    ``parts[*].dependencies.dependsOn`` are also included and deduped per
    ``(dep_id, relation_type)`` so the rendered report shows one row per
    unique downstream dependency rather than one row per part.
    """
    entries = load_registry_entries(registry_dir)
    id_map = build_id_to_name_map(entries)

    refs: list[ObjectReference] = []
    for entry in iter_in_scope_non_missing(entries):
        caller_name = _entry_full_name(entry)
        caller_type = entry.get("source", {}).get("objectType", "").upper()
        caller_file = entry.get("files", {}).get("source", {}).get("path", "")

        for dep in _iter_unit_dep_specs(entry):
            refs.extend(
                ObjectReference.from_registry_dependency(
                    caller_name, caller_type, caller_file, dep, id_map
                )
            )
    return refs


def load_missing_references_from_registry(
    registry_dir: Path,
) -> list[ObjectReference]:
    """Load only references whose target is missing (``isMissing=True``)."""
    all_refs = load_object_references_from_registry(registry_dir)
    return [r for r in all_refs if r.is_missing_reference]


def _strip_prefix(patterns: list[str], prefix: str) -> str | None:
    """Return the suffix of the first pattern starting with *prefix*, else ``None``."""
    for pattern in patterns:
        if pattern.startswith(prefix):
            return pattern[len(prefix) :]
    return None


def load_exclusion_findings_from_registry(registry_dir: Path | str) -> dict:
    """Rebuild object-exclusion category lists from each entry's
    ``codeStatus.assessment.exclusion`` array.

    Mirrors the trimmed ``object_exclusion_analysis_*.json`` registry-mode
    contract (``detail_location: "registry"``): once a run's findings are
    confirmed persisted to the registry, the JSON stops carrying the
    per-category arrays this function reconstructs, so
    ``generate_multi_report.py`` must read them from here instead.

    ``duplicate``/``version_conflict`` findings encode their group key inside
    ``matchedPatterns`` as a literal ``"duplicate_group: {FullName}"`` /
    ``"version_group: {BaseName}"`` string (written by
    ``ObjectExclusionService.BuildFindingsByObjectId`` on the .NET side) —
    stripping the known prefix recovers the key used to regroup findings that
    belong to the same duplicate/version-conflict group.
    """
    entries = load_registry_entries(registry_dir)
    refs = load_object_references_from_registry(registry_dir)

    depends_on: dict[str, list[str]] = {}
    depended_by: dict[str, list[str]] = {}
    for ref in refs:
        callers = depends_on.setdefault(ref.caller_full_name, [])
        if ref.referenced_full_name not in callers:
            callers.append(ref.referenced_full_name)
        referenced = depended_by.setdefault(ref.referenced_full_name, [])
        if ref.caller_full_name not in referenced:
            referenced.append(ref.caller_full_name)

    temp_staging: list[dict] = []
    deprecated: list[dict] = []
    testing: list[dict] = []
    duplicate_groups: dict[str, dict] = {}
    version_groups: dict[str, dict] = {}

    for entry in iter_in_scope_non_missing(entries):
        findings = ((entry.get("codeStatus") or {}).get("assessment") or {}).get(
            "exclusion"
        ) or []
        if not findings:
            continue

        full_name = _entry_full_name(entry)
        source = entry.get("source") or entry.get("target") or {}
        base_obj = {
            "full_name": full_name,
            "schema": source.get("schema", ""),
            "type": (source.get("objectType") or "").upper(),
            "source_file": entry.get("files", {}).get("source", {}).get("path", ""),
            "dependencies": {
                "depends_on": depends_on.get(full_name, []),
                "depended_by": depended_by.get(full_name, []),
            },
        }

        for finding in findings:
            category = finding.get("category")
            patterns = finding.get("matchedPatterns") or []
            obj = {**base_obj, "matched_patterns": patterns}

            if category == "temp_staging":
                temp_staging.append(obj)
            elif category == "deprecated_legacy":
                deprecated.append(obj)
            elif category == "testing":
                testing.append(obj)
            elif category == "duplicate":
                key = _strip_prefix(patterns, "duplicate_group: ") or full_name
                group = duplicate_groups.setdefault(
                    key, {"full_name": key, "primary": None, "duplicates": []}
                )
                if finding.get("isPrimary"):
                    group["primary"] = obj
                else:
                    group["duplicates"].append(obj)
            elif category == "version_conflict":
                key = _strip_prefix(patterns, "version_group: ") or full_name
                group = version_groups.setdefault(
                    key,
                    {"base_name": key, "all_versions": [], "production_version": None},
                )
                group["all_versions"].append(obj)
                if finding.get("isRecommendedVersion"):
                    group["production_version"] = obj

    for group in version_groups.values():
        group["version_count"] = len(group["all_versions"])

    return {
        "temp_staging": temp_staging,
        "deprecated": deprecated,
        "testing": testing,
        "duplicates": list(duplicate_groups.values()),
        "version_analysis": {
            "version_groups": list(version_groups.values()),
            "total_version_conflicts": len(version_groups),
        },
    }


def load_missing_dependencies_by_object(
    registry_dir: Path | str,
) -> dict[str, list[str]]:
    """Load missing dependencies grouped by object.

    Returns a dict mapping code_unit_id to list of missing dependency names.
    For ETL units (``kind == "etl"``), missing references inside
    ``parts[*].dependencies.dependsOn`` are also collected so the report's
    "missing deps" section attributes them to the parent ETL unit instead of
    silently dropping them.

    Example:
        {
            '[DB].[Schema].[Table1]': ['[DB].[Schema].[MissingView]'],
            '[DB].[Schema].[Proc1]': ['[OtherDB].[Schema].[MissingTable]', ...]
        }
    """
    entries = load_registry_entries(registry_dir)
    id_map = build_id_to_name_map(entries)

    missing_by_object: dict[str, list[str]] = {}

    for entry in iter_in_scope_non_missing(entries):
        caller_name = _entry_full_name(entry)

        missing_deps: list[str] = []
        for dep in _iter_unit_dep_specs(entry):
            if dep.get("isMissing", False):
                dep_id = dep.get("id") or ""
                dep_name = id_map.get(dep_id, dep_id)
                if dep_name and dep_name not in missing_deps:
                    missing_deps.append(dep_name)

        if missing_deps:
            missing_by_object[caller_name] = sorted(missing_deps)

    return missing_by_object
