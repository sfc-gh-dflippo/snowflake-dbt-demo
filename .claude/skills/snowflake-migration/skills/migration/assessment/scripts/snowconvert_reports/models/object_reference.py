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

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectReference:
    """A single row from ObjectReferences.*.csv."""

    caller_full_name: str
    caller_code_unit: str
    referenced_full_name: str
    referenced_element_type: str
    relation_type: str
    line: str
    file_name: str

    @property
    def is_missing_reference(self) -> bool:
        return self.referenced_element_type == "MISSING"

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> "ObjectReference":
        return ObjectReference(
            caller_full_name=row.get("Caller_CodeUnit_FullName", "").strip(),
            caller_code_unit=row.get("Caller_CodeUnit", "").strip(),
            referenced_full_name=row.get("Referenced_Element_FullName", "").strip(),
            referenced_element_type=row.get("Referenced_Element_Type", "").strip(),
            relation_type=row.get("Relation_Type", "").strip(),
            line=row.get("Line", "").strip(),
            file_name=row.get("FileName", "").strip(),
        )

    @staticmethod
    def from_registry_dependency(
        caller_name: str,
        caller_type: str,
        caller_file: str,
        dep: dict,
        id_to_name: dict[str, str],
    ) -> list["ObjectReference"]:
        """Build ObjectReference(s) from a registry ``dependsOn`` entry.

        Each *relationTypes* value in *dep* produces one ObjectReference.
        """
        dep_id = dep.get("id") or ""
        ref_name = id_to_name.get(dep_id, dep_id)
        is_missing = dep.get("isMissing", False)
        ref_type = "MISSING" if is_missing else ""
        relation_types = dep.get("relationTypes", [])

        results: list[ObjectReference] = []
        for rel in relation_types:
            results.append(
                ObjectReference(
                    caller_full_name=caller_name,
                    caller_code_unit=f"CREATE {caller_type}",
                    referenced_full_name=ref_name,
                    referenced_element_type=ref_type,
                    relation_type=rel,
                    line="0",
                    file_name=caller_file,
                )
            )
        return results
