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

"""Owns ``{project_dir}/artifacts/assessment/assessment.json``.

That file carries the name displayed on a generated assessment report, so a
report shared outside the team identifies the engagement it came from.

Read paths return ``{}`` / ``""`` rather than raising: the name is an optional
display value, and a report must still generate when it is unavailable.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..loaders.project_config import read_project_name

ASSESSMENT_METADATA_RELPATH = Path("artifacts") / "assessment" / "assessment.json"

# Two clean lines in the 248px sidebar, which leaves ~200px of text at 0.875rem.
# Bounds a paste accident; every realistic answer is far shorter.
MAX_VALUE_LENGTH = 60


def read_assessment_metadata(project_dir: Optional[Path]) -> Dict[str, Any]:
    """Return the stored metadata, or ``{}`` if it cannot be read as an object."""
    if not project_dir:
        return {}
    path = Path(project_dir) / ASSESSMENT_METADATA_RELPATH
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def write_assessment_metadata(project_dir: Path, **fields: Any) -> None:
    """Merge ``fields`` into the stored metadata, creating the file if needed.

    Merges rather than overwrites so keys written by other steps survive — the
    file is expected to grow. Normalization lives here rather than in the CLI so
    an ``import`` gets the same guarantees a command-line call does.

    Note ``**fields`` maps keyword names straight to JSON keys, which is why
    callers pass ``assessmentName=`` — the artifacts in this skill are camelCase.
    """
    path = Path(project_dir) / ASSESSMENT_METADATA_RELPATH
    merged = read_assessment_metadata(project_dir)
    for key, value in fields.items():
        merged[key] = (
            str(value).strip()[:MAX_VALUE_LENGTH] if value is not None else ""
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")


def resolve_assessment_name(project_dir: Optional[Path]) -> str:
    """The name a report should display: stored name, else project name, else ``""``.

    The third step is not a branch — it is what falls out when both sources come
    up empty, which is what makes "generate without either value" succeed
    structurally rather than by wrapping call sites in ``try``/``except``.
    """
    stored = str(read_assessment_metadata(project_dir).get("assessmentName", "")).strip()
    if stored:
        return stored
    return read_project_name(project_dir)
