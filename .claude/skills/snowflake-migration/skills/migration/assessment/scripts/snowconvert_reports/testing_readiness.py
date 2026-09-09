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

"""Derive what the Testing tab can honestly claim, from the code unit registry.

Aggregate counts only — the Testing tab answers "what can we test, and how
well", which per-object detail belongs to the Overview and Waves tabs. Every
value here traces to a registry field; nothing is inferred beyond the rules
documented on each helper.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .conversion_status import (
    STATUS_REQUIRE_ATTENTION,
    STATUS_SUCCESS,
    is_etl,
    map_conversion_status,
)
from .loaders.registry_loader import iter_in_scope_non_missing, load_registry_entries

# Object types whose behavior is verified by comparing output against the
# source. Tables and views carry no logic to output-test — they are covered by
# the Data Migration & Validation phase instead.
OUTPUT_TESTED_OBJECT_TYPES = frozenset({"procedure", "function"})

# Capture/validate is not implemented for these source dialects yet. Kept as a
# deny-list so an unenumerated future dialect keeps its ladder instead of
# silently inheriting a false "not supported" claim.
UNSUPPORTED_PROC_DIALECTS = frozenset({"postgres"})

# Free-text dialect spellings (SnowConvert's ``SourceLanguage``, SCAI's
# ``sourceLanguage``) collapsed onto one key per platform.
_DIALECT_ALIASES = {
    "transact": "sqlserver",
    "transactsql": "sqlserver",
    "tsql": "sqlserver",
    "mssql": "sqlserver",
    "microsoftsqlserver": "sqlserver",
    "sqlserver": "sqlserver",
    "amazonredshift": "redshift",
    "redshift": "redshift",
    "postgresql": "postgres",
    "postgres": "postgres",
    "teradata": "teradata",
    "oracle": "oracle",
}

# ETL units have no `deploy` task: they finish at stabilization, while every
# other code unit finishes at testing (`NON_DEPLOYING_TYPES` /
# `non_deploying_done_field` in ai/crates/mcp-server/src/registry.rs). Reading
# `testing.status` for an ETL unit would report zero progress forever.
_ETL_TERMINAL_STAGE = "stabilization"
_CODE_TERMINAL_STAGE = "testing"


@dataclass(frozen=True)
class UnitBuckets:
    """Testability of one family of code units, as counts."""

    total: int
    ready: int
    needs_fix: int
    blocked: int
    tested: int


@dataclass(frozen=True)
class TestingReadiness:
    """Everything the Testing tab renders from, or `has_project_state=False`."""

    has_project_state: bool
    source_dialect: str
    dialect_key: str
    code_units: UnitBuckets | None
    etl_units: UnitBuckets | None
    includes_scripts: bool
    proc_testing_supported: bool


def normalize_dialect(source_dialect: str) -> str:
    """Collapse a free-text dialect name onto a canonical key ("" if unknown)."""
    slug = re.sub(r"[^a-z0-9]", "", (source_dialect or "").lower())
    return _DIALECT_ALIASES.get(slug, slug)


def _is_script(entry: dict) -> bool:
    return entry.get("kind") == "script"


def _is_output_tested_code_unit(entry: dict) -> bool:
    """Procedures, functions, and script units (BTEQ today).

    Scripts fold in here rather than getting a bucket of their own: they are
    verified by the same terminal `runTests` task as procedures, so a separate
    bucket would add a section with no distinct guidance behind it.
    """
    if is_etl(entry):
        return False
    if _is_script(entry):
        return True
    obj_type = (entry.get("source", {}).get("objectType") or "").strip().lower()
    return obj_type in OUTPUT_TESTED_OBJECT_TYPES


def _stage_completed(entry: dict, stage: str) -> bool:
    status = (
        entry.get("codeStatus", {}).get(stage, {}).get("status", "") or ""
    ).strip().lower()
    return status == "completed"


def _bucket(entries: list[dict], terminal_stage: str) -> UnitBuckets | None:
    """Count *entries* by testability. ``None`` when the family is empty."""
    if not entries:
        return None

    ready = needs_fix = blocked = tested = 0
    for entry in entries:
        status = map_conversion_status(entry)
        if status == STATUS_SUCCESS:
            ready += 1
        elif status == STATUS_REQUIRE_ATTENTION:
            needs_fix += 1
        else:
            blocked += 1
        if _stage_completed(entry, terminal_stage):
            tested += 1

    return UnitBuckets(
        total=len(entries),
        ready=ready,
        needs_fix=needs_fix,
        blocked=blocked,
        tested=tested,
    )


def load_testing_readiness(
    registry_dir: Path | str | None,
    source_dialect: str = "",
) -> TestingReadiness:
    """Read testing readiness from the registry at *registry_dir*.

    Always returns an instance. Dialect fields are populated even without a
    registry, so a CSV-only run still resolves proc-testing support — without
    them, a PostgreSQL project would wrongly be offered a procedure ladder.
    ``has_project_state`` is False when there is no registry to read, which is
    a different state from a registry that holds only tables and views (state
    known, nothing to output-test).
    """
    dialect_key = normalize_dialect(source_dialect)
    dialect_fields = {
        "source_dialect": source_dialect or "",
        "dialect_key": dialect_key,
        "proc_testing_supported": dialect_key not in UNSUPPORTED_PROC_DIALECTS,
    }

    entries: list[dict] = []
    if registry_dir and Path(registry_dir).is_dir():
        entries = load_registry_entries(Path(registry_dir))

    if not entries:
        return TestingReadiness(
            has_project_state=False,
            code_units=None,
            etl_units=None,
            includes_scripts=False,
            **dialect_fields,
        )

    in_scope = list(iter_in_scope_non_missing(entries))
    code_entries = [e for e in in_scope if _is_output_tested_code_unit(e)]
    etl_entries = [e for e in in_scope if is_etl(e)]

    return TestingReadiness(
        has_project_state=True,
        code_units=_bucket(code_entries, _CODE_TERMINAL_STAGE),
        etl_units=_bucket(etl_entries, _ETL_TERMINAL_STAGE),
        includes_scripts=any(_is_script(e) for e in code_entries),
        **dialect_fields,
    )
