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

"""InformaticaAssessmentAnalyzer — main orchestrator for Informatica assessment."""

import sys
from pathlib import Path
from typing import Dict

# Add shared scripts to path for snowconvert_reports
_scripts_dir = str(Path(__file__).resolve().parents[3] / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports import IssueEffortService

from .models import WorkflowAnalysis
from .repositories import ElementRepository, IssueRepository
from .services import (
    AnalysisService,
    ComponentOrganizerService,
)
from .utils.config import EXCLUDED_COMPONENT_SUBTYPES


class InformaticaAssessmentAnalyzer:
    """Orchestrates the full Informatica assessment pipeline.

    Pipeline:
    1. Load components from ETL.Elements.csv (filtered to InformaticaPowerCenter)
    2. Load and attach issues from ETL.Issues.csv
    3. Organize components into WorkflowAnalysis structures
    4. Export to JSON
    """

    def __init__(
        self,
        elements_file: str,
        issues_file: str,
        source_dir: str = None,
    ):
        self.elements_file = elements_file
        self.issues_file = issues_file
        self.workflows: Dict[str, WorkflowAnalysis] = {}

        self.issue_effort_service = IssueEffortService.from_bundled_reference()
        self.organizer_service = ComponentOrganizerService()
        self.analysis_service = AnalysisService()

    def analyze(self) -> None:
        """Run the full analysis pipeline."""
        components_by_key, excluded_count = self._load_elements()
        print(
            f"Total components loaded: {len(components_by_key)} "
            f"(excluded: {excluded_count})"
        )

        matched, not_matched = self._load_issues(components_by_key)
        print(f"Issues matched: {matched}, not matched: {not_matched}")

        self.workflows = self._organize_by_workflows(components_by_key)
        print(f"Workflows organized: {len(self.workflows)}")

    def _load_elements(self):
        repository = ElementRepository(
            self.elements_file,
            EXCLUDED_COMPONENT_SUBTYPES,
            technology_filter="InformaticaPowerCenter",
        )
        return repository.load_components()

    def _load_issues(self, components_by_key):
        repository = IssueRepository(self.issues_file, self.issue_effort_service)
        return repository.load_and_attach_issues(components_by_key)

    def _organize_by_workflows(self, components_by_key):
        return self.organizer_service.organize_by_workflows(components_by_key)

    def export_to_json(self, output_path: str, conversion_mode: str = "dbt") -> None:
        """Export analysis results to JSON."""
        self.analysis_service.export_to_json(self.workflows, output_path, conversion_mode)
