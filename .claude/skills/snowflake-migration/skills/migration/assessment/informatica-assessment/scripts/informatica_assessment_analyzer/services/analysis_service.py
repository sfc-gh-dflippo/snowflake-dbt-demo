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

"""AnalysisService — exports workflow analysis to JSON."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ..models import WorkflowAnalysis


class AnalysisService:
    """Handles JSON export of workflow analysis results."""

    @staticmethod
    def export_to_json(
        workflows: Dict[str, WorkflowAnalysis],
        output_path: str,
        conversion_mode: str = "dbt",
    ) -> None:
        """Export all workflow analyses to a single JSON file.

        Output structure:
        {
            "summary": {...},
            "workflows": [...]
        }
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Build summary
        total_workflows = len(workflows)
        total_mappings = sum(len(w.mappings) for w in workflows.values())
        total_components = sum(w.total_components for w in workflows.values())
        total_ewis = sum(w.total_ewi_count for w in workflows.values())
        total_fdms = sum(w.total_fdm_count for w in workflows.values())
        total_prfs = sum(w.total_prf_count for w in workflows.values())

        # Aggregate status
        status_totals: Dict[str, int] = {}
        for w in workflows.values():
            for status, count in w.status_summary.items():
                status_totals[status] = status_totals.get(status, 0) + count

        # Aggregate subtypes
        subtype_totals: Dict[str, int] = {}
        for w in workflows.values():
            for subtype, count in w.subtype_summary.items():
                subtype_totals[subtype] = subtype_totals.get(subtype, 0) + count

        data = {
            "summary": {
                "generated_at": datetime.now().isoformat(),
                "technology": "InformaticaPowerCenter",
                "conversion_mode": conversion_mode,
                "total_workflows": total_workflows,
                "total_mappings": total_mappings,
                "total_components": total_components,
                "total_ewis": total_ewis,
                "total_fdms": total_fdms,
                "total_prfs": total_prfs,
                "status_totals": status_totals,
                "subtype_totals": subtype_totals,
            },
            "workflows": [w.to_dict() for w in sorted(workflows.values(), key=lambda x: x.path)],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Exported analysis to: {output_file}")
