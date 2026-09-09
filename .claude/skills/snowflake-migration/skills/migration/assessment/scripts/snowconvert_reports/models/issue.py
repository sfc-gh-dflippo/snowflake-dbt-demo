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


@dataclass(frozen=True)
class IssueRecord:
    """A single row from SnowConvert Issues.csv."""

    session_id: str
    severity: str
    code: str
    name: str
    description: str
    parent_file: str
    line: int
    column: int
    code_unit_database: str
    code_unit_schema: str
    code_unit_package: str
    code_unit_name: str
    code_unit_id: str
    code_unit: str
    code_unit_size: str
    source_language: str
    migration_id: str
    component_full_name: str = ""

    @property
    def issue_type(self) -> str:
        for prefix in ("EWI", "FDM", "PRF"):
            if prefix in self.code:
                return prefix
        return "UNKNOWN"

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> "IssueRecord":
        def safe_int(val: str) -> int:
            val = val.strip() if val else ""
            try:
                return int(val) if val else 0
            except ValueError:
                return 0

        return IssueRecord(
            session_id=row.get("SessionID", "").strip(),
            severity=row.get("Severity", "").strip(),
            code=row.get("Code", "").strip(),
            name=row.get("Name", "").strip(),
            description=row.get("Description", "").strip(),
            parent_file=row.get("ParentFile", row.get("ParentFileName", "")).strip(),
            line=safe_int(row.get("Line", "0")),
            column=safe_int(row.get("Column", "0")),
            code_unit_database=row.get("CodeUnitDatabase", "").strip(),
            code_unit_schema=row.get("CodeUnitSchema", "").strip(),
            code_unit_package=row.get("CodeUnitPackage", "").strip(),
            code_unit_name=row.get("CodeUnitName", "").strip(),
            code_unit_id=row.get("Code Unit Id", row.get("CodeUnitId", "")).strip(),
            code_unit=row.get("Code Unit", row.get("CodeUnit", "")).strip(),
            code_unit_size=row.get("Code Unit Size", row.get("CodeUnitSize", "")).strip(),
            source_language=row.get("SourceLanguage", "").strip(),
            migration_id=row.get("MigrationID", row.get("MigrationId", "")).strip(),
            component_full_name=row.get("ComponentFullName", "").strip(),
        )
