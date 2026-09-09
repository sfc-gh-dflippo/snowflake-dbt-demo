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
class PartitionMember:
    """A single row from PartitionMembership.csv."""

    object_name: str
    partition_number: int
    is_root: bool
    is_leaf: bool
    is_picked_scc: bool
    category: str
    file_name: str
    technology: str
    conversion_status: str
    subtype: str
    partition_type: str

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> "PartitionMember":
        def parse_bool(val: str) -> bool:
            return val.strip().lower() == "true"

        partition_str = row.get(
            "partition_number", row.get("partition", "")
        ).strip()

        return PartitionMember(
            object_name=row.get("object", "").strip(),
            partition_number=int(partition_str) if partition_str.isdigit() else 0,
            is_root=parse_bool(row.get("is_root", "")),
            is_leaf=parse_bool(row.get("is_leaf", "")),
            is_picked_scc=parse_bool(row.get("is_picked_scc", "")),
            category=row.get("category", "").strip(),
            file_name=row.get("file_name", "").strip(),
            technology=row.get("technology", "").strip(),
            conversion_status=row.get("conversion_status", "").strip(),
            subtype=row.get("subtype", "").strip(),
            partition_type=row.get("partition_type", "regular").strip(),
        )
