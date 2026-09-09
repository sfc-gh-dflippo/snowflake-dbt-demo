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
class Element:
    """A single row from SnowConvert Elements.csv."""

    full_name: str
    file_name: str
    technology: str
    category: str
    subtype: str
    status: str
    entry_kind: str
    additional_info: str

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> "Element":
        return Element(
            full_name=row.get("FullName", "").strip(),
            file_name=row.get("FileName", "").strip(),
            technology=row.get("Technology", "").strip(),
            category=row.get("Category", "").strip(),
            subtype=row.get("Subtype", "").strip(),
            status=row.get("Status", "").strip(),
            entry_kind=row.get("Entry Kind", "").strip(),
            additional_info=row.get("Additional Info", "").strip(),
        )
