#!/usr/bin/env python3
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

"""Read and write assessment metadata from the command line.

``SKILL.md`` cannot import a module, only run a command, so this exists to give
the skill a door in both directions. It holds no logic of its own: every rule —
merge, length cap, the fallback order — lives in
``snowconvert_reports.services.assessment_metadata``, so importing that module
directly gets identical guarantees.
"""

import argparse
import sys
from pathlib import Path

_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports.services.assessment_metadata import (  # noqa: E402
    read_assessment_metadata,
    resolve_assessment_name,
    write_assessment_metadata,
)
from snowconvert_reports.loaders.project_config import read_project_name  # noqa: E402

UNSET_DISPLAY = "(unset)"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read or write the name shown on a generated assessment report."
    )
    parser.add_argument(
        "--project-dir",
        required=True,
        type=Path,
        help="project root; assessment.json is read/written beneath it",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--show-assessment-name",
        action="store_true",
        help="print the current name state; writes nothing",
    )
    mode.add_argument(
        "--set-assessment-name",
        metavar="NAME",
        help="store NAME as the report's assessment name",
    )
    args = parser.parse_args()

    if args.show_assessment_name:
        # Stable `key: value` lines so SKILL.md can branch without parsing JSON.
        # `resolved` is the same call generate_multi_report.py makes, so the
        # default offered at the prompt cannot disagree with the rendered title.
        stored = str(
            read_assessment_metadata(args.project_dir).get("assessmentName", "")
        ).strip()
        print(f"assessmentName: {stored or UNSET_DISPLAY}")
        print(f"projectName:    {read_project_name(args.project_dir) or UNSET_DISPLAY}")
        print(f"resolved:       {resolve_assessment_name(args.project_dir) or UNSET_DISPLAY}")
        return

    name = args.set_assessment_name.strip()
    if not name:
        print("Error: --set-assessment-name requires a non-empty name", file=sys.stderr)
        sys.exit(1)

    # Replacing rather than merging is data loss, so say so — but the write still
    # succeeds, which is why this warns instead of exiting non-zero.
    target = args.project_dir / "artifacts" / "assessment" / "assessment.json"
    if target.is_file() and not read_assessment_metadata(args.project_dir):
        print(
            f"Warning: could not parse existing {target}; it will be replaced, not merged",
            file=sys.stderr,
        )

    try:
        write_assessment_metadata(args.project_dir, assessmentName=name)
    except OSError as exc:
        print(f"Error: could not write {target}: {exc}", file=sys.stderr)
        sys.exit(1)

    stored = read_assessment_metadata(args.project_dir).get("assessmentName", name)
    print(f"Stored assessment name: {stored}")


if __name__ == "__main__":
    main()
