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

"""Derive what the Data Migration & Validation tab can honestly claim.

Aggregate counts and per-type findings only -- per-object detail belongs to the
Overview and Dependencies tabs. Every value traces to a registry field, to the
DDL those fields point at, or to the coverage snapshot in ``type_coverage``.
Row counts and byte sizes appear nowhere: the registry has neither, which is
precisely what the tab's inventory scripts exist to obtain.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .data_types_scan import TypeUsage, aggregate_usage, scan_ddl
from .loaders.registry_loader import iter_in_scope_non_missing, load_registry_entries
from .testing_readiness import normalize_dialect
from .type_coverage import TypeCoverage, coverage_for

# Dialects with a reviewed inventory script. An allow-list, because a script for
# an unlisted dialect would be invented SQL.
INVENTORY_SCRIPT_DIALECTS = frozenset({"sqlserver", "redshift"})


@dataclass(frozen=True)
class TypeFinding:
    """A coverage row, with how much this project uses it when that is known."""

    coverage: TypeCoverage
    usage: TypeUsage | None


@dataclass(frozen=True)
class DataMigrationReadiness:
    """Everything the tab renders from, or ``has_project_state=False``."""

    has_project_state: bool
    source_dialect: str
    dialect_key: str
    table_count: int
    view_count: int
    scanned_tables: int
    distinct_type_count: int
    clean_type_count: int
    findings: tuple[TypeFinding, ...]
    has_inventory_scripts: bool


def _object_type(entry: dict) -> str:
    return (entry.get("source", {}).get("objectType") or "").strip().lower()


def _source_path(entry: dict) -> str:
    return (entry.get("files", {}).get("source", {}).get("path") or "").strip()


def _resolve(project_root: Path, raw_path: str) -> Path | None:
    """Locate a captured source file, or ``None`` when it is not readable.

    Registry paths are project-relative (``source/tables/dbo.Orders.sql``) and
    the registry lives at ``<projectRoot>/registry/``, so the project root is
    the registry's parent. An absolute path is honoured as given.
    """
    if not raw_path:
        return None
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return candidate if candidate.is_file() else None


def _scan_tables(tables: list[dict], project_root: Path) -> list[tuple[str, ...]]:
    """Column types per table, one entry per table the scan could read.

    A table whose DDL is missing, unreadable, or yields no recognizable column
    contributes no entry: it lowers scan coverage rather than inventing a type.
    """
    scanned: list[tuple[str, ...]] = []
    for entry in tables:
        path = _resolve(project_root, _source_path(entry))
        if path is None:
            continue
        try:
            ddl = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        types = scan_ddl(ddl)
        if types:
            scanned.append(types)
    return scanned


def _reference_findings(coverage: tuple[TypeCoverage, ...]) -> tuple[TypeFinding, ...]:
    """The per-dialect table with no project usage attached to it."""
    return tuple(TypeFinding(row, None) for row in coverage if not row.is_clean)


def load_data_migration_readiness(
    registry_dir: Path | str | None,
    source_dialect: str = "",
) -> DataMigrationReadiness:
    """Read migration readiness from the registry at *registry_dir*.

    Always returns an instance. Dialect fields are populated even without a
    registry, so a CSV-only run still renders the coverage table as per-dialect
    reference and still resolves whether an inventory script exists.
    """
    dialect_key = normalize_dialect(source_dialect)
    coverage = coverage_for(dialect_key)
    dialect_fields = {
        "source_dialect": source_dialect or "",
        "dialect_key": dialect_key,
        "has_inventory_scripts": dialect_key in INVENTORY_SCRIPT_DIALECTS,
    }

    entries: list[dict] = []
    if registry_dir and Path(registry_dir).is_dir():
        entries = load_registry_entries(Path(registry_dir))

    if not entries:
        return DataMigrationReadiness(
            has_project_state=False,
            table_count=0,
            view_count=0,
            scanned_tables=0,
            distinct_type_count=0,
            clean_type_count=0,
            findings=_reference_findings(coverage),
            **dialect_fields,
        )

    in_scope = list(iter_in_scope_non_missing(entries))
    tables = [e for e in in_scope if _object_type(e) == "table"]
    views = [e for e in in_scope if _object_type(e) == "view"]

    scanned = _scan_tables(tables, Path(registry_dir).parent)
    usage = aggregate_usage(scanned)
    by_name = {row.type_name: row for row in coverage}

    # A scanned type with no coverage row is neither a finding nor clean: the
    # scan resolved a name the snapshot cannot speak for, and saying nothing
    # about it is the only honest option.
    findings = tuple(
        TypeFinding(by_name[item.type_name], item)
        for item in usage
        if item.type_name in by_name and not by_name[item.type_name].is_clean
    )
    clean_type_count = sum(
        1 for item in usage if item.type_name in by_name and by_name[item.type_name].is_clean
    )

    return DataMigrationReadiness(
        has_project_state=True,
        table_count=len(tables),
        view_count=len(views),
        scanned_tables=len(scanned),
        distinct_type_count=len(usage),
        clean_type_count=clean_type_count,
        # Two different empty states. Nothing scanned means the coverage table is
        # still worth showing as per-dialect reference; a scan that found only
        # clean types means the honest answer is "nothing needs a decision", and
        # a reference table there would read as a project finding.
        findings=findings if scanned else _reference_findings(coverage),
        **dialect_fields,
    )
