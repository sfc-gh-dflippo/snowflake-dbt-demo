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

"""Shared IssueRepository — loads issues from ETL.Issues.csv and attaches to components.

Follows Open-Closed Principle: the Issue construction uses the shared Issue class
with optional fields (name, component_full_name have defaults). Each ETL tool
populates what it needs without requiring separate repository implementations.
"""

from pathlib import Path
from typing import Dict, Tuple

from ..loaders import read_csv_rows
from ..models import Issue, Component


class IssueRepository:
    """Loads issues from ETL.Issues.csv and attaches them to components.

    Args:
        file_path: Path to ETL.Issues.csv
        issue_effort_service: Service that provides get_effort_and_severity(code)
    """

    def __init__(self, file_path: str, issue_effort_service):
        self.file_path = Path(file_path)
        self.issue_effort_service = issue_effort_service

    def load_and_attach_issues(
        self, components_by_key: Dict[Tuple[str, str], Component]
    ) -> Tuple[int, int]:
        """Load issues from CSV and attach to matching components.

        Returns:
            Tuple of (matched_count, not_matched_count)
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Issues file not found: {self.file_path}")

        matched = 0
        not_matched = 0

        for row in read_csv_rows(self.file_path):
            component_full_name = row.get("ComponentFullName", "").strip()
            if not component_full_name:
                continue

            issue_code = row.get("Code", "").strip()
            effort_hours, severity = self.issue_effort_service.get_effort_and_severity(
                issue_code
            )

            issue = Issue(
                code=issue_code,
                effort_hours=effort_hours,
                severity=severity,
                name=row.get("Name", "").strip(),
                description=row.get("Description", "").strip(),
                component_full_name=component_full_name,
            )

            parent_file_name = row.get("ParentFileName", "").strip()
            component_key = (parent_file_name, component_full_name)

            if component_key in components_by_key:
                components_by_key[component_key].issues.append(issue)
                matched += 1
            else:
                not_matched += 1

        return matched, not_matched
