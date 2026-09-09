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

"""WorkflowTrackingService — manages PENDING/DONE state for AI analysis workflow."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from informatica_assessment_analyzer.services.analysis_validator_service import (
    AnalysisValidatorService,
)


class WorkflowTrackingService:
    """Manages the AI analysis state for Informatica workflows."""

    @staticmethod
    def get_pending(json_file_path: str) -> Optional[List[Dict]]:
        """Get first workflow with PENDING AI analysis status.

        Returns list with one dict {'name': ..., 'path': ...} or empty list.
        """
        data = WorkflowTrackingService._load(json_file_path)
        workflows = data.get("workflows", [])

        for wf in workflows:
            ai = wf.get("ai_analysis", {})
            if not ai or ai.get("status", "PENDING") == "PENDING":
                return [{"name": wf.get("name"), "path": wf.get("path")}]

        return []

    @staticmethod
    def update_workflow(
        json_file_path: str,
        workflow_path: str,
        ai_status: Optional[str] = None,
        ai_analysis_text: Optional[str] = None,
        classification: Optional[str] = None,
    ) -> bool:
        """Update AI analysis fields for a workflow.

        Returns True if workflow was found and updated.

        Raises:
            ValueError: If classification is not in VALID_CLASSIFICATIONS.
        """
        if classification:
            is_valid, error = AnalysisValidatorService.validate_classification(
                classification
            )
            if not is_valid:
                raise ValueError(error)

        data = WorkflowTrackingService._load(json_file_path)
        workflows = data.get("workflows", [])

        for wf in workflows:
            if wf.get("path") == workflow_path:
                if "ai_analysis" not in wf:
                    wf["ai_analysis"] = {}

                ai = wf["ai_analysis"]
                if ai_status:
                    ai["status"] = ai_status
                if ai_analysis_text:
                    ai["analysis"] = ai_analysis_text
                if classification:
                    ai["classification"] = classification

                WorkflowTrackingService._save(json_file_path, data)
                return True

        return False

    @staticmethod
    def update_ai_summary(json_file_path: str, summary_path: str) -> None:
        """Set the AI summary HTML path in the summary section."""
        data = WorkflowTrackingService._load(json_file_path)
        if "summary" not in data:
            data["summary"] = {}
        data["summary"]["ai_summary"] = summary_path
        WorkflowTrackingService._save(json_file_path, data)

    @staticmethod
    def get_statistics(json_file_path: str) -> Dict:
        """Get analysis progress statistics."""
        data = WorkflowTrackingService._load(json_file_path)
        workflows = data.get("workflows", [])

        total = len(workflows)
        pending = 0
        reviewed = 0
        classifications: Dict[str, int] = {}

        for wf in workflows:
            ai = wf.get("ai_analysis", {})
            status = ai.get("status", "PENDING")
            if status == "PENDING":
                pending += 1
            elif status == "DONE":
                reviewed += 1

            cls_val = ai.get("classification", "")
            if cls_val:
                classifications[cls_val] = classifications.get(cls_val, 0) + 1

        has_custom = sum(
            1
            for wf in workflows
            if wf.get("flags", {}).get("has_custom_transforms", False)
        )

        return {
            "total": total,
            "pending": pending,
            "reviewed": reviewed,
            "with_custom_transforms": has_custom,
            "classifications": classifications,
        }

    @staticmethod
    def get_summary_for_llm(json_file_path: str) -> str:
        """Generate a consolidated text summary for LLM consumption."""
        data = WorkflowTrackingService._load(json_file_path)
        summary = data.get("summary", {})
        workflows = data.get("workflows", [])

        lines = []
        lines.append("=== INFORMATICA ASSESSMENT SUMMARY ===")
        lines.append(f"Total Workflows: {summary.get('total_workflows', 0)}")
        lines.append(f"Total Mappings: {summary.get('total_mappings', 0)}")
        lines.append(f"Total Components: {summary.get('total_components', 0)}")
        lines.append(f"Total EWIs: {summary.get('total_ewis', 0)}")
        lines.append(f"Total FDMs: {summary.get('total_fdms', 0)}")
        lines.append("")

        stats = WorkflowTrackingService.get_statistics(json_file_path)
        lines.append(f"Analysis Progress: {stats['reviewed']}/{stats['total']} done")
        lines.append("")

        # Per-workflow summaries
        for wf in workflows:
            ai = wf.get("ai_analysis", {})
            status_icon = "✓" if ai.get("status") == "DONE" else "○"
            name = wf.get("name", "Unknown")
            cls_val = ai.get("classification", "Unclassified")
            lines.append(f"{status_icon} {name} [{cls_val}]")
            if ai.get("analysis"):
                # First 100 chars of analysis
                preview = ai["analysis"][:100].replace("\n", " ")
                lines.append(f"  {preview}...")

        return "\n".join(lines)

    @staticmethod
    def _load(json_file_path: str) -> Dict:
        path = Path(json_file_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save(json_file_path: str, data: Dict) -> None:
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
