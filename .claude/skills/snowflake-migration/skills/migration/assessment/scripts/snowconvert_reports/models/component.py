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

"""ETL Component model — represents a component with attached issues from ETL.Elements.csv."""

from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict, Any

from .etl_issue import Issue


@dataclass
class Component:
    """A component from ETL.Elements.csv with attached issues.

    Used by both SSIS (scai_assessment_analyzer) and Informatica
    (informatica_assessment_analyzer).
    """

    full_name: str
    file_name: str
    technology: str
    category: str
    subtype: str
    status: str
    entry_kind: str
    additional_info: str
    issues: List[Issue] = field(default_factory=list)
    sql_task_details: Optional[Dict[str, Any]] = field(default=None)

    def count_issues_by_type(self, issue_type: str) -> int:
        return sum(1 for issue in self.issues if issue.issue_type == issue_type)

    def unique_issues_by_type(self, issue_type: str) -> Set[str]:
        return {issue.code for issue in self.issues if issue.issue_type == issue_type}

    @property
    def ewi_count(self) -> int:
        return self.count_issues_by_type("EWI")

    @property
    def fdm_count(self) -> int:
        return self.count_issues_by_type("FDM")

    @property
    def prf_count(self) -> int:
        return self.count_issues_by_type("PRF")

    @property
    def unique_ewis(self) -> Set[str]:
        return self.unique_issues_by_type("EWI")

    @property
    def unique_fdms(self) -> Set[str]:
        return self.unique_issues_by_type("FDM")

    @property
    def unique_prfs(self) -> Set[str]:
        return self.unique_issues_by_type("PRF")

    def to_dict(self, override_category: str = None) -> dict:
        result = {
            "full_name": self.full_name,
            "category": override_category or self.category,
            "subtype": self.subtype,
            "status": self.status,
            "entry_kind": self.entry_kind,
            "additional_info": self.additional_info,
            "issue_counts": {
                "ewis": self.ewi_count,
                "fdms": self.fdm_count,
                "prfs": self.prf_count,
            },
            "issues": [issue.to_dict() for issue in self.issues],
        }

        if self.sql_task_details:
            result["sql_task_details"] = self.sql_task_details

        return result
