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

from dataclasses import dataclass

from ..na_utils import NA_VALUES


def _safe_int(val: str) -> int:
    val = val.strip() if val else ""
    try:
        return int(val) if val else 0
    except ValueError:
        return 0


@dataclass(frozen=True)
class TopLevelCodeUnit:
    """A single row from TopLevelCodeUnits.csv."""

    code_unit_id: str
    code_unit_name: str
    category: str
    file_name: str
    code_unit: str
    deployment_order: str
    has_missing_dependencies: bool
    conversion_status: str
    lines_of_code: int
    ewi_count: int
    fdm_count: int
    prf_count: int
    highest_ewi_severity: str
    line_number: int = 0

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> "TopLevelCodeUnit":
        deployment_raw = row.get("Deployment Order", "").strip()
        has_missing = "*" in deployment_raw
        clean_order = deployment_raw.replace("*", "")

        return TopLevelCodeUnit(
            code_unit_id=row.get("CodeUnitId", "").strip(),
            code_unit_name=row.get("CodeUnitName", "").strip(),
            category=row.get("Category", "").strip(),
            file_name=row.get("FileName", "").strip(),
            code_unit=row.get("CodeUnit", "").strip(),
            deployment_order=clean_order,
            has_missing_dependencies=has_missing,
            conversion_status=row.get(
                "ConversionStatus", row.get("Conversion", "")
            ).strip(),
            lines_of_code=_safe_int(
                row.get("Lines of Code", row.get("LinesOfCode", "0"))
            ),
            ewi_count=_safe_int(row.get("EWI Count", "0")),
            fdm_count=_safe_int(row.get("FDM Count", "0")),
            prf_count=_safe_int(row.get("PRF Count", "0")),
            highest_ewi_severity=row.get("HighestEWISeverity", "").strip(),
            line_number=_safe_int(row.get("LineNumber", "0")),
        )

    @staticmethod
    def from_registry_entry(entry: dict) -> "TopLevelCodeUnit":
        """Build a TopLevelCodeUnit from a SnowConvert registry JSON entry."""
        source = entry.get("source", {})
        db = source.get("database", "")
        schema = source.get("schema", "")
        name = source.get("name", "")
        obj_type = source.get("objectType", "").upper()

        def _bracket(ident: str) -> str:
            ident = (ident or "").strip()
            if not ident:
                return "[]"
            if ident.startswith("[") and ident.endswith("]"):
                return ident
            return f"[{ident}]"

        parts = [
            _bracket(v)
            for v in (db, schema, name)
            if v.strip() not in NA_VALUES and v.strip("[] ") not in NA_VALUES
        ]
        code_unit_id = ".".join(parts) if parts else "[]"
        file_path = entry.get("files", {}).get("source", {}).get("path", "")
        rank = str(entry.get("planning", {}).get("topologicalRank", 0))
        deps = entry.get("dependencies", {})
        has_missing = deps.get("hasTransitiveMissingDependencies", False)
        status = entry.get("codeStatus", {}).get("assessment", {}).get("status", "")

        return TopLevelCodeUnit(
            code_unit_id=code_unit_id,
            code_unit_name=name,
            category=obj_type,
            file_name=file_path,
            code_unit=f"CREATE {obj_type}",
            deployment_order=rank,
            has_missing_dependencies=has_missing,
            conversion_status=status,
            lines_of_code=0,
            ewi_count=0,
            fdm_count=0,
            prf_count=0,
            highest_ewi_severity="",
            line_number=0,
        )
