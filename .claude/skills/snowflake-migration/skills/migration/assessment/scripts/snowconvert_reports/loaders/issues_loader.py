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

from pathlib import Path
from typing import Optional

from ..models import IssueRecord
from .csv_reader import load_csv_as


def load_issues(
    csv_path: str | Path,
    *,
    filter_code: Optional[str] = None,
) -> list[IssueRecord]:
    """Load issues from Issues.csv, optionally filtering by issue code."""

    def factory(row: dict[str, str]) -> IssueRecord | None:
        record = IssueRecord.from_csv_row(row)
        if filter_code and record.code != filter_code:
            return None
        return record

    return load_csv_as(csv_path, factory)
