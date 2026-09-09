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

"""Auto-dispatch loaders: prefer registry when available, fall back to CSV."""

from __future__ import annotations

from pathlib import Path

from ..models.code_unit import TopLevelCodeUnit
from ..models.object_reference import ObjectReference
from ..na_utils import NA_VALUES
from ..services.report_finder import ReportFinder
from .code_units_loader import load_code_units
from .object_references_loader import load_object_references, load_missing_references
from .registry_loader import (
    load_code_units_from_registry,
    load_object_references_from_registry,
    load_missing_references_from_registry,
)


def _resolve_registry_path(registry_dir: str | Path) -> Path | None:
    """Resolve explicit registry path (must be provided by caller)."""
    candidate = Path(registry_dir)
    return candidate if candidate.is_dir() else None


def _normalize_code_unit_id(code_unit_id: str) -> str:
    """Normalize code unit IDs for joining registry <-> CSV.

    Removes brackets, parameter signatures, N/A segments, and lowercases.
    This ensures ``[N/A].[dbo].[Table]`` (CSV) matches ``[dbo].[Table]``
    (registry with N/A stripping) after normalization.
    """
    if not code_unit_id:
        return ""
    normalized = code_unit_id.replace("[", "").replace("]", "")
    if "(" in normalized:
        normalized = normalized[:normalized.index("(")]
    parts = [p for p in normalized.split(".") if p.strip() and p.strip() not in NA_VALUES]
    return ".".join(parts).strip().lower()


def _merge_registry_with_csv_code_units(
    registry_units: list[TopLevelCodeUnit],
    csv_units: list[TopLevelCodeUnit],
) -> list[TopLevelCodeUnit]:
    """Prefer registry units but supplement missing CSV-only fields.

    Registry is authoritative about WHICH objects to include (respects inScope,
    isMissing, and objectType filters). CSV provides supplemental field data:
    - conversion_status: CSV has more detail (Success/Partial/NotSupported)
    - Metrics: lines_of_code, ewi_count, etc. (registry hardcodes to 0)
    - Structural: Registry preferred for dependencies, deployment order
    """

    csv_by_id: dict[str, TopLevelCodeUnit] = {}
    csv_by_norm: dict[str, TopLevelCodeUnit] = {}
    for u in csv_units:
        if u.code_unit_id:
            csv_by_id[u.code_unit_id] = u
            csv_by_norm[_normalize_code_unit_id(u.code_unit_id)] = u

    merged: list[TopLevelCodeUnit] = []

    for r in registry_units:
        c = csv_by_id.get(r.code_unit_id) or csv_by_norm.get(_normalize_code_unit_id(r.code_unit_id))
        if not c:
            # Registry object with no CSV match - keep registry data as-is
            merged.append(r)
            continue

        # Merge: prefer CSV for status/metrics, registry for structure
        merged.append(
            TopLevelCodeUnit(
                code_unit_id=r.code_unit_id or c.code_unit_id,
                code_unit_name=r.code_unit_name or c.code_unit_name,
                category=r.category or c.category,
                file_name=r.file_name or c.file_name,
                code_unit=r.code_unit or c.code_unit,
                # Prefer registry for structural info
                deployment_order=r.deployment_order or c.deployment_order,
                has_missing_dependencies=r.has_missing_dependencies
                if r.deployment_order
                else c.has_missing_dependencies,
                # Prefer CSV for status (has more detail: Success/Partial/NotSupported)
                conversion_status=c.conversion_status or r.conversion_status,
                # Prefer CSV for metrics (registry hardcodes to 0)
                lines_of_code=c.lines_of_code or r.lines_of_code,
                ewi_count=c.ewi_count or r.ewi_count,
                fdm_count=c.fdm_count or r.fdm_count,
                prf_count=c.prf_count or r.prf_count,
                highest_ewi_severity=c.highest_ewi_severity or r.highest_ewi_severity,
                line_number=c.line_number or r.line_number,
            )
        )

    # NOTE: CSV-only objects are intentionally NOT added. Registry is authoritative
    # about which objects should be included (respects inScope, isMissing, objectType).
    # If registry is partial/incomplete, the caller should use load_code_units() directly.

    return merged


def load_code_units_auto(
    reports_dir: str | Path,
    registry_dir: str | Path,
) -> tuple[list[TopLevelCodeUnit], str]:
    """Load code units (registry preferred, CSV supplements missing fields).

    Args:
        reports_dir: Explicit reports directory for CSV discovery.
        registry_dir: Explicit registry directory.
    """
    finder = ReportFinder(reports_dir)
    csv_path = finder.find_code_units()
    registry_path = _resolve_registry_path(registry_dir)

    if registry_path is not None:
        registry_units = load_code_units_from_registry(registry_path)
        if csv_path is not None:
            csv_units = load_code_units(csv_path)
            return _merge_registry_with_csv_code_units(registry_units, csv_units), "registry+csv"
        return registry_units, "registry"

    if csv_path is not None:
        return load_code_units(csv_path), "csv"

    return [], "none"


def load_object_references_auto(
    reports_dir: str | Path,
    registry_dir: str | Path,
) -> tuple[list[ObjectReference], str]:
    """Load object references from registry if available, else CSV."""
    finder = ReportFinder(reports_dir)
    registry_path = _resolve_registry_path(registry_dir)
    if registry_path is not None:
        return load_object_references_from_registry(registry_path), "registry"

    csv_path = finder.find_object_references()
    if csv_path is not None:
        return load_object_references(csv_path), "csv"

    return [], "none"


def load_missing_references_auto(
    reports_dir: str | Path,
    registry_dir: str | Path,
) -> tuple[list[ObjectReference], str]:
    """Load missing references from registry if available, else CSV."""
    finder = ReportFinder(reports_dir)
    registry_path = _resolve_registry_path(registry_dir)
    if registry_path is not None:
        return load_missing_references_from_registry(registry_path), "registry"

    csv_path = finder.find_object_references()
    if csv_path is not None:
        return load_missing_references(csv_path), "csv"

    return [], "none"
