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

"""Registry conversion status, shared by every reader that needs it.

The waves synthesizer and the testing-readiness reader both have to answer
"did this code unit convert cleanly?", and ETL units answer it differently
from SQL units — their SnowConvert issues hang off ``parts[*]`` rather than
the top-level ``issues`` array. One implementation here is what keeps the
two readers from drifting apart.
"""

from __future__ import annotations

STATUS_SUCCESS = "Success"
STATUS_REQUIRE_ATTENTION = "Require Attention"
STATUS_PENDING = "Pending Conversion"
STATUS_NOT_SUPPORTED = "Not Supported"
STATUS_MISSING = "Missing"


def is_etl(entry: dict) -> bool:
    return entry.get("kind") == "etl"


def aggregate_etl_issues(entry: dict) -> list[dict]:
    """Concatenate ``parts[*].issues`` for an ETL entry.

    Top-level ``entry.issues`` is empty for ETL; the SnowConvert EWIs / FDMs
    raised during conversion are attached per-part. Used by
    ``map_conversion_status`` so an ETL with conversion gaps surfaces as
    "Require Attention" instead of "Success".
    """
    out: list[dict] = []
    for part in entry.get("parts") or []:
        if not isinstance(part, dict):
            continue
        for issue in part.get("issues") or []:
            if isinstance(issue, dict):
                out.append(issue)
    return out


def map_conversion_status(entry: dict) -> str:
    """Map registry conversion status + issue presence to the UI status value.

    Rules:
    - ``isMissing == true`` → "Missing" (takes precedence)
    - ``conversion.status == "pending"`` and no issues  → "Pending Conversion"
    - ``conversion.status == "pending"`` and issues > 0 → "Require Attention"
    - ``conversion.status == "completed"`` and issues > 0 → "Require Attention"
    - ``conversion.status == "completed"`` and no issues → "Success"
    - otherwise: "Require Attention" if issues else "Pending Conversion"

    For ETL units, "issues" includes ``parts[*].issues`` since the
    SnowConvert conversion attaches gaps per-part.
    """
    if entry.get("isMissing"):
        return STATUS_MISSING

    conv = (
        entry.get("codeStatus", {}).get("conversion", {}).get("status", "") or ""
    ).strip().lower()
    issues = entry.get("issues") or []
    if is_etl(entry):
        issues = list(issues) + aggregate_etl_issues(entry)
    has_issues = bool(issues)

    if conv == "pending":
        return STATUS_REQUIRE_ATTENTION if has_issues else STATUS_PENDING
    if conv == "completed":
        return STATUS_REQUIRE_ATTENTION if has_issues else STATUS_SUCCESS
    return STATUS_REQUIRE_ATTENTION if has_issues else STATUS_PENDING
