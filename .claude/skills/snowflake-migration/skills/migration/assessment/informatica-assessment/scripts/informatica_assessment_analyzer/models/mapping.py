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

"""Mapping model — represents an Informatica PowerCenter mapping (data flow pipeline)."""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from snowconvert_reports import Component
from ..utils import sanitize_filename


@dataclass
class Mapping:
    """A mapping within a workflow, containing transformation components.

    Analogous to SSIS DataFlow — a pipeline from sources through transformations
    to targets within an Informatica mapping.
    """

    name: str
    full_path: str
    components: List[Component] = field(default_factory=list)
    dag_file: Optional[str] = None

    @property
    def total_components(self) -> int:
        return len(self.components)

    def _aggregate_by_field(self, field_getter) -> Dict[str, int]:
        summary: Dict[str, int] = defaultdict(int)
        for component in self.components:
            key = field_getter(component)
            if key and key.upper() != "N/A":
                summary[key] += 1
        return dict(summary)

    @property
    def status_summary(self) -> Dict[str, int]:
        return self._aggregate_by_field(
            lambda c: c.status if c.status.upper() != "N/A" else None
        )

    @property
    def subtype_summary(self) -> Dict[str, int]:
        return self._aggregate_by_field(lambda c: c.subtype)

    def _aggregate_unique_issues(self, issue_type: str) -> Set[str]:
        codes: Set[str] = set()
        for component in self.components:
            codes.update(component.unique_issues_by_type(issue_type))
        return codes

    @property
    def total_ewi_count(self) -> int:
        return sum(c.ewi_count for c in self.components)

    @property
    def total_fdm_count(self) -> int:
        return sum(c.fdm_count for c in self.components)

    @property
    def total_prf_count(self) -> int:
        return sum(c.prf_count for c in self.components)

    @property
    def unique_ewis(self) -> Set[str]:
        return self._aggregate_unique_issues("EWI")

    @property
    def unique_fdms(self) -> Set[str]:
        return self._aggregate_unique_issues("FDM")

    @property
    def unique_prfs(self) -> Set[str]:
        return self._aggregate_unique_issues("PRF")

    @property
    def not_supported_components(self) -> List[Component]:
        return [c for c in self.components if c.status == "NotSupported"]

    @property
    def unique_not_supported_types(self) -> Set[str]:
        return {c.subtype for c in self.not_supported_components}

    def calculate_conversion_rate(self) -> Dict[str, float]:
        if self.total_components == 0:
            return {"success_rate": 0.0, "partial_rate": 0.0, "not_supported_rate": 0.0}

        status_counts = self.status_summary
        total = self.total_components
        return {
            "success_rate": round((status_counts.get("Success", 0) / total) * 100, 2),
            "partial_rate": round((status_counts.get("Partial", 0) / total) * 100, 2),
            "not_supported_rate": round(
                (status_counts.get("NotSupported", 0) / total) * 100, 2
            ),
        }

    def get_dag_filename(self, workflow_path: str) -> str:
        """Generate the expected DAG HTML filename for this mapping."""
        workflow_sanitized = sanitize_filename(workflow_path)
        mapping_sanitized = sanitize_filename(self.name)
        return f"{workflow_sanitized}__{mapping_sanitized}_mapping.html"

    def to_dict(self, workflow_path: str = None) -> dict:
        result = {
            "name": self.name,
            "full_path": self.full_path,
            "metrics": {
                "total_components": self.total_components,
                "conversion_rates": self.calculate_conversion_rate(),
                "status_summary": self.status_summary,
                "subtype_summary": self.subtype_summary,
                "issue_counts": {
                    "total_ewis": self.total_ewi_count,
                    "total_fdms": self.total_fdm_count,
                    "total_prfs": self.total_prf_count,
                    "unique_ewis": sorted(self.unique_ewis),
                    "unique_fdms": sorted(self.unique_fdms),
                    "unique_prfs": sorted(self.unique_prfs),
                },
                "not_supported_components": {
                    "total_count": len(self.not_supported_components),
                    "component_types": sorted(self.unique_not_supported_types),
                },
            },
            "components": [c.to_dict() for c in self.components],
        }

        if workflow_path:
            result["dag_file"] = f"dags/{self.get_dag_filename(workflow_path)}"
        elif self.dag_file:
            result["dag_file"] = self.dag_file

        return result
