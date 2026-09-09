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


class ReportFinder:
    """Discover SnowConvert report files from explicit directories.

    This class intentionally avoids directory-structure assumptions.
    - Pass a reports directory that directly contains report files for CSV lookups.
    - Pass a registry directory directly to use registry discovery helpers.
    """

    def __init__(self, reports_dir: str | Path):
        base_dir = Path(reports_dir)
        if base_dir.is_file():
            base_dir = base_dir.parent

        self.base_dir = base_dir
        self.reports_dir = base_dir

    def find(self, base_name: str, extension: str = "csv") -> Optional[Path]:
        """Find the most recent report file matching ``{base_name}.*.{extension}``."""
        matches = self.find_all(base_name, extension)
        return matches[0] if matches else None

    def find_all(self, base_name: str, extension: str = "csv") -> list[Path]:
        """Find all matching report files, newest first."""
        if not self.reports_dir.is_dir():
            return []

        pattern = f"{base_name}.*.{extension}"
        return sorted(
            self.reports_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def find_elements(self) -> Optional[Path]:
        return self.find("Elements")

    def find_issues(self) -> Optional[Path]:
        return self.find("Issues")

    def find_code_units(self) -> Optional[Path]:
        return self.find("TopLevelCodeUnits")

    def find_object_references(self) -> Optional[Path]:
        return self.find("ObjectReferences")

    def find_partition_membership(self) -> Optional[Path]:
        return self.find("PartitionMembership")

    def find_issues_estimation_json(self) -> Optional[Path]:
        return self.find("IssuesEstimation", extension="json")

    def find_toplevel_objects_estimation(self) -> Optional[Path]:
        return self.find("TopLevelObjectsEstimation")

    def find_issues_aggregate(self) -> Optional[Path]:
        return self.find("IssuesEstimationAggregate")

    def find_effort_formula(self) -> Optional[Path]:
        return self.find("EffortEstimationFormula")

    def find_registry_dir(self) -> Optional[Path]:
        """Return *base_dir* when it is an explicit registry dir with JSON files."""
        if (
            self.base_dir.is_dir()
            and self.base_dir.name == "registry"
            and any(self.base_dir.glob("*.json"))
        ):
            return self.base_dir
        return None

    def has_registry(self) -> bool:
        return self.find_registry_dir() is not None
