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

import json
from pathlib import Path

from ..models import IssueEstimationEntry, ObjectEstimation, SeverityBaseline
from .csv_reader import load_csv_as


def load_issues_estimation_json(
    json_path: str | Path,
) -> tuple[dict[str, IssueEstimationEntry], dict[str, SeverityBaseline]]:
    """Load IssuesEstimation.*.json, returning issue_map and severity_map."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issue_map = {}
    for entry_dict in data.get("Issues", []):
        entry = IssueEstimationEntry.from_dict(entry_dict)
        issue_map[entry.code] = entry

    severity_map = {}
    for entry_dict in data.get("Severities", []):
        entry = SeverityBaseline.from_dict(entry_dict)
        severity_map[entry.severity] = entry

    return issue_map, severity_map


def load_object_estimations(csv_path: str | Path) -> list[ObjectEstimation]:
    """Load TopLevelObjectsEstimation.*.csv."""
    return load_csv_as(csv_path, ObjectEstimation.from_csv_row)
