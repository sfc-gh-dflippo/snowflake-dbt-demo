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

from typing import Optional

from ..models import IssueEstimationEntry


class IssueEffortService:
    """Unified issue effort and severity lookup.

    Supports two initialization paths:
    - ``from_json_file(path)`` for runtime IssuesEstimation.*.json files
    - ``from_bundled_reference()`` for the bundled issues_ref.json
    """

    def __init__(self, issue_map: dict[str, IssueEstimationEntry]):
        self._issue_map = issue_map

    @classmethod
    def from_json_file(cls, json_path: str) -> "IssueEffortService":
        """Load from any IssuesEstimation-format JSON file."""
        from ..loaders import load_issues_estimation_json

        issue_map, _ = load_issues_estimation_json(json_path)
        return cls(issue_map)

    @classmethod
    def from_bundled_reference(cls) -> "IssueEffortService":
        """Load from the bundled issues_ref.json shipped with the library."""
        from pathlib import Path

        data_path = Path(__file__).parent.parent / "data" / "issues_ref.json"
        return cls.from_json_file(str(data_path))

    def get_effort_hours(self, issue_code: str) -> float:
        """Get manual effort in hours for an issue code.

        EWI codes: ManualEffort is in minutes, divided by 60.
        Other codes: ManualEffort is already in hours.
        """
        entry = self._issue_map.get(issue_code)
        if not entry or entry.manual_effort < 0:
            return 0.0
        if "EWI" in issue_code:
            return entry.manual_effort / 60.0
        return entry.manual_effort

    def get_severity(self, issue_code: str) -> str:
        """Get severity level for an issue code."""
        entry = self._issue_map.get(issue_code)
        return entry.severity if entry else "Unknown"

    def get_effort_and_severity(self, issue_code: str) -> tuple[float, str]:
        """Get both effort (hours) and severity."""
        return self.get_effort_hours(issue_code), self.get_severity(issue_code)

    def get_entry(self, issue_code: str) -> Optional[IssueEstimationEntry]:
        """Get the full estimation entry for an issue code."""
        return self._issue_map.get(issue_code)
