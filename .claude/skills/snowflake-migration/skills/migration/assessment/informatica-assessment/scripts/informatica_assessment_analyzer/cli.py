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

"""CLI for Informatica assessment analyzer."""

import json
import sys
import traceback
from pathlib import Path

from .analyzer import InformaticaAssessmentAnalyzer
from .services import (
    AnalysisValidatorService,
    WorkflowTrackingService,
)


def handle_informatica_commands():
    """Handle Informatica analysis JSON reading commands."""
    if len(sys.argv) < 4:
        print(
            "Usage: python -m informatica_assessment_analyzer "
            "informatica <json_file> <command> [args]"
        )
        print("\nCommands:")
        print("  pending                        - List the first pending workflow")
        print("  update <workflow_path> [opts]   - Update workflow AI analysis")
        print("    --ai-status <status>         - Set AI analysis status (PENDING/DONE)")
        print("    --ai-analysis <text>         - Set AI analysis text")
        print(
            "    --classification <type>      - Set classification "
            "(Ingestion/Data Transformation/Configuration & Control)"
        )
        print("  ai-summary <relative_path>     - Set summary.ai_summary HTML path")
        print("  summary                        - Print consolidated summary for LLM")
        print("  stats                          - Show statistics")
        sys.exit(1)

    json_file = sys.argv[2]
    command = sys.argv[3]

    try:
        if command == "pending":
            pending = WorkflowTrackingService.get_pending(json_file)
            if pending and len(pending) > 0:
                print(
                    f"Name: {pending[0]['name']} | "
                    f"Relative Path: {pending[0]['path']}"
                )
            else:
                print("No pending workflows found")
                sys.exit(1)
            return

        elif command == "update" and len(sys.argv) > 4:
            workflow_path = sys.argv[4]
            ai_status = None
            ai_analysis_text = None
            classification = None

            i = 5
            while i < len(sys.argv):
                if sys.argv[i] == "--ai-status" and i + 1 < len(sys.argv):
                    ai_status = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--ai-analysis" and i + 1 < len(sys.argv):
                    ai_analysis_text = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--classification" and i + 1 < len(sys.argv):
                    classification = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1

            # Validate ai_analysis structure if provided and status is DONE
            if ai_analysis_text and ai_status == "DONE":
                is_valid, error_message = AnalysisValidatorService.validate_and_report(
                    ai_analysis_text, workflow_path
                )
                if not is_valid:
                    print(error_message, file=sys.stderr)
                    sys.exit(1)

            if WorkflowTrackingService.update_workflow(
                json_file,
                workflow_path,
                ai_status,
                ai_analysis_text,
                classification,
            ):
                print(f"Updated: {workflow_path}")
            else:
                print(f"Workflow not found: {workflow_path}", file=sys.stderr)
                sys.exit(1)
            return

        elif command == "ai-summary" and len(sys.argv) > 4:
            summary_path = sys.argv[4]
            WorkflowTrackingService.update_ai_summary(json_file, summary_path)
            print(f"Updated summary.ai_summary: {summary_path}")
            return

        elif command == "summary":
            summary_payload = WorkflowTrackingService.get_summary_for_llm(json_file)
            print(summary_payload)
            return

        elif command == "stats":
            stats = WorkflowTrackingService.get_statistics(json_file)
            print(f"Total Workflows: {stats['total']}")
            print(f"AI Analysis - Pending: {stats['pending']}")
            print(f"AI Analysis - Done: {stats['reviewed']}")
            print(f"With Custom Transforms: {stats['with_custom_transforms']}")
            print(f"\nClassifications:")
            for cls_name, count in stats.get("classifications", {}).items():
                print(f"  {cls_name}: {count}")
            return

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) > 1 and sys.argv[1] == "informatica":
        handle_informatica_commands()
        return

    if len(sys.argv) < 4:
        print(
            "Usage: python -m informatica_assessment_analyzer "
            "<elements_csv> <issues_csv> <output_folder> "
            "[--source-dir <path>] [--conversion-mode dbt|scripting]"
        )
        print(
            "       python -m informatica_assessment_analyzer "
            "informatica <json_file> <command> [args]"
        )
        print("\nAnalysis mode:")
        print(
            "  python -m informatica_assessment_analyzer "
            "ETL.Elements.csv ETL.Issues.csv ./output"
        )
        print(
            "  python -m informatica_assessment_analyzer "
            "ETL.Elements.csv ETL.Issues.csv ./output --source-dir ./xml_sources"
        )
        print("\nInformatica Analysis mode:")
        print(
            "  python -m informatica_assessment_analyzer "
            "informatica <json_file> pending"
        )
        print(
            "  python -m informatica_assessment_analyzer "
            "informatica <json_file> update <path> --ai-status DONE"
        )
        print(
            "  python -m informatica_assessment_analyzer "
            "informatica <json_file> ai-summary summary.html"
        )
        print(
            "  python -m informatica_assessment_analyzer "
            "informatica <json_file> summary"
        )
        print(
            "  python -m informatica_assessment_analyzer "
            "informatica <json_file> stats"
        )
        sys.exit(1)

    elements_file = sys.argv[1]
    issues_file = sys.argv[2]
    output_folder = sys.argv[3]

    # Optional source dir for XML enrichment
    source_dir = None
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            source_dir = sys.argv[idx + 1]

    # Optional conversion mode (dbt or scripting)
    conversion_mode = "dbt"
    if "--conversion-mode" in sys.argv:
        idx = sys.argv.index("--conversion-mode")
        if idx + 1 < len(sys.argv):
            val = sys.argv[idx + 1]
            if val not in ("dbt", "scripting"):
                print(
                    f"Error: --conversion-mode must be 'dbt' or 'scripting', got '{val}'",
                    file=sys.stderr,
                )
                sys.exit(1)
            conversion_mode = val

    output_json = Path(f"{output_folder}/informatica_assessment_analysis.json")

    try:
        analyzer = InformaticaAssessmentAnalyzer(
            elements_file, issues_file, source_dir
        )
        analyzer.analyze()
        analyzer.export_to_json(str(output_json), conversion_mode)

        print(f"\nInformatica assessment analysis saved to: {output_json}")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
