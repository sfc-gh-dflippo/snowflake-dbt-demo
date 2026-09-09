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

"""WorkflowAnalysis — top-level container for an Informatica workflow or standalone mapping.

Analogous to SSIS PackageAnalysis. Groups components by:
- workflow_tasks: Control-flow-level tasks (Session, Timer, Start, etc.)
- mappings: Data-flow-level pipelines (Source → Transforms → Target)
- source_definitions: Folder-level source declarations
- target_definitions: Folder-level target declarations
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from snowconvert_reports import Component
from .mapping import Mapping
from ..utils import sanitize_filename


@dataclass
class WorkflowAnalysis:
    """Top-level analysis container for one Informatica workflow/mapping file."""

    name: str
    path: str  # file_name from ETL.Elements.csv
    technology: str  # 'InformaticaPowerCenter'
    workflow_tasks: List[Component] = field(default_factory=list)
    mappings: Dict[str, Mapping] = field(default_factory=dict)
    source_definitions: List[Component] = field(default_factory=list)
    target_definitions: List[Component] = field(default_factory=list)
    has_workflow_declaration: bool = False
    workflow_dag_file: Optional[str] = None

    @property
    def all_components(self) -> List[Component]:
        components = list(self.source_definitions)
        components.extend(self.target_definitions)
        components.extend(self.workflow_tasks)
        for mapping in self.mappings.values():
            components.extend(mapping.components)
        return components

    @property
    def execution_components(self) -> List[Component]:
        """Components that represent executable work (workflow tasks + mapping transforms)."""
        components = list(self.workflow_tasks)
        for mapping in self.mappings.values():
            components.extend(mapping.components)
        return components

    @property
    def total_components(self) -> int:
        return len(self.all_components)

    @property
    def total_source_definitions(self) -> int:
        return len(self.source_definitions)

    @property
    def total_target_definitions(self) -> int:
        return len(self.target_definitions)

    @property
    def total_workflow_tasks(self) -> int:
        return len(self.workflow_tasks)

    @property
    def total_mapping_components(self) -> int:
        return sum(len(m.components) for m in self.mappings.values())

    def _aggregate_execution_field(self, field_getter) -> Dict[str, int]:
        summary: Dict[str, int] = defaultdict(int)
        for component in self.execution_components:
            key = field_getter(component)
            if key and key.upper() != "N/A":
                summary[key] += 1
        return dict(summary)

    @property
    def status_summary(self) -> Dict[str, int]:
        return self._aggregate_execution_field(
            lambda c: c.status if c.status.upper() != "N/A" else None
        )

    @property
    def subtype_summary(self) -> Dict[str, int]:
        return self._aggregate_execution_field(lambda c: c.subtype)

    def _count_issues_by_type(self, issue_type: str) -> int:
        return sum(c.count_issues_by_type(issue_type) for c in self.all_components)

    def _aggregate_unique_issues(self, issue_type: str) -> Set[str]:
        codes: Set[str] = set()
        for component in self.all_components:
            codes.update(component.unique_issues_by_type(issue_type))
        return codes

    @property
    def total_ewi_count(self) -> int:
        return self._count_issues_by_type("EWI")

    @property
    def total_fdm_count(self) -> int:
        return self._count_issues_by_type("FDM")

    @property
    def total_prf_count(self) -> int:
        return self._count_issues_by_type("PRF")

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
        return [c for c in self.execution_components if c.status == "NotSupported"]

    @property
    def unique_not_supported_types(self) -> Set[str]:
        return {c.subtype for c in self.not_supported_components}

    def calculate_conversion_rate(self) -> Dict[str, float]:
        total = len(self.execution_components)
        if total == 0:
            return {"success_rate": 0.0, "partial_rate": 0.0, "not_supported_rate": 0.0}

        status_counts = self.status_summary
        return {
            "success_rate": round((status_counts.get("Success", 0) / total) * 100, 2),
            "partial_rate": round((status_counts.get("Partial", 0) / total) * 100, 2),
            "not_supported_rate": round(
                (status_counts.get("NotSupported", 0) / total) * 100, 2
            ),
        }

    def calculate_complexity(self) -> Dict:
        severity_frequency: Dict[str, int] = defaultdict(int)
        total_effort = 0.0

        for component in self.all_components:
            for issue in component.issues:
                severity_frequency[issue.severity.capitalize()] += 1
                total_effort += issue.effort_hours

        complexity_level = self._determine_complexity_level(
            self.total_ewi_count, dict(severity_frequency)
        )

        return {
            "severityFrequency": dict(severity_frequency),
            "totalEffortHours": round(total_effort, 1),
            "complexity": complexity_level,
        }

    def _determine_complexity_level(
        self, ewi_count: int, severity_freq: Dict[str, int]
    ) -> str:
        """Multi-factor complexity scoring.

        Considers: structural size (mappings, components), issue severity,
        and flags (custom transforms, SQL overrides).
        """
        score = 0

        # Factor 1: Structural size (mappings and execution components)
        num_mappings = len(self.mappings)
        total_exec = len(self.execution_components)
        if total_exec > 50 or num_mappings > 10:
            score += 3
        elif total_exec > 20 or num_mappings > 5:
            score += 2
        elif total_exec > 5 or num_mappings > 2:
            score += 1

        # Factor 2: Issue severity distribution
        critical_count = severity_freq.get("Critical", 0)
        high_count = severity_freq.get("High", 0)
        if critical_count >= 10:
            score += 3
        elif critical_count > 0 or high_count >= 5:
            score += 2
        elif high_count > 0 or severity_freq.get("Medium", 0) > 5:
            score += 1

        # Factor 3: Custom transforms / SQL overrides
        flags = self.calculate_flags()
        if flags.get("has_custom_transforms"):
            score += 2
        if flags.get("has_sql_override"):
            score += 1

        # Map score to complexity level
        if score >= 7:
            return "Very Complex"
        if score >= 5:
            return "Complex"
        if score >= 3:
            return "Medium"
        if score >= 1:
            return "Easy"
        return "Very Easy"

    def get_unique_issues(self) -> Dict[str, List[Dict]]:
        details: Dict[str, List[Dict]] = defaultdict(list)
        seen_issues: Set[str] = set()

        for component in self.all_components:
            for issue in component.issues:
                issue_key = f"{issue.code}|{issue.description}"
                if issue_key not in seen_issues:
                    seen_issues.add(issue_key)
                    details[issue.issue_type].append(
                        {
                            "code": issue.code,
                            "description": issue.description,
                            "severity": issue.severity,
                        }
                    )

        return dict(details)

    def calculate_flags(self) -> Dict[str, bool]:
        """Calculate workflow flags based on component analysis."""
        has_custom_transforms = any(
            component.subtype in ("Custom Transformation", "Java Transformation")
            for component in self.all_components
        )
        has_sql_override = any(
            '"sqlOverride":true' in (component.additional_info or "")
            for component in self.all_components
        )
        return {
            "has_custom_transforms": has_custom_transforms,
            "has_sql_override": has_sql_override,
        }

    def get_workflow_dag_filename(self) -> str:
        """Get the workflow-level DAG filename."""
        path_sanitized = sanitize_filename(self.path)
        return f"{path_sanitized}__workflow.html"

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "path": self.path,
            "technology": self.technology,
            "flags": self.calculate_flags(),
            "metrics": {
                "total_components": self.total_components,
                "total_source_definitions": self.total_source_definitions,
                "total_target_definitions": self.total_target_definitions,
                "total_workflow_tasks": self.total_workflow_tasks,
                "total_mapping_components": self.total_mapping_components,
                "total_mappings": len(self.mappings),
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
                "not_supported_elements": {
                    "total_count": len(self.not_supported_components),
                    "component_types": sorted(self.unique_not_supported_types),
                },
                "workflow_complexity": self.calculate_complexity(),
            },
            "issue_details": self.get_unique_issues(),
            "source_definitions": [
                c.to_dict("Source Definition") for c in self.source_definitions
            ],
            "target_definitions": [
                c.to_dict("Target Definition") for c in self.target_definitions
            ],
            "workflow_tasks": [c.to_dict() for c in self.workflow_tasks],
            "mappings": [
                m.to_dict(workflow_path=self.path)
                for m in sorted(self.mappings.values(), key=lambda x: x.full_path)
            ],
        }

        if self.workflow_tasks:
            result["workflow_dag_file"] = f"dags/{self.get_workflow_dag_filename()}"
        elif self.workflow_dag_file:
            result["workflow_dag_file"] = self.workflow_dag_file

        return result
