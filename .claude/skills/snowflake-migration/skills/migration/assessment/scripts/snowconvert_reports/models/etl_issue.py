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

"""Shared Issue model for ETL components.

This is the single Issue class used by all ETL assessment analyzers (SSIS,
Informatica, and future tools). Follows the Open-Closed Principle: open for
extension via optional fields with defaults, closed for modification of the
core interface.

Design decisions:
- frozen=True: Issues are immutable value objects (identity by content)
- Optional fields with defaults: allows different ETL tools to populate
  only the fields they need without breaking the interface contract
- issue_type as @property: derived from code prefix (Single Responsibility)
- Convenience properties (is_ewi, is_fdm, is_prf): follow Interface
  Segregation — consumers check what they need without parsing strings
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Issue:
    """A conversion issue attached to an ETL component.

    Core fields (required by all tools):
        code: Issue code (e.g. SSC-EWI-INF0001)
        effort_hours: Estimated manual effort
        severity: Issue severity level

    Extension fields (optional, tool-specific):
        name: Short issue name (used by SSIS)
        description: Detailed description
        component_full_name: Parent component reference (used by SSIS for key lookup)
    """

    code: str
    effort_hours: float
    severity: str
    name: str = ""
    description: str = ""
    component_full_name: str = ""

    @property
    def issue_type(self) -> str:
        """Derive issue type from code prefix (EWI, FDM, PRF)."""
        if "EWI" in self.code:
            return "EWI"
        elif "FDM" in self.code:
            return "FDM"
        elif "PRF" in self.code:
            return "PRF"
        return "UNKNOWN"

    @property
    def is_ewi(self) -> bool:
        return self.issue_type == "EWI"

    @property
    def is_fdm(self) -> bool:
        return self.issue_type == "FDM"

    @property
    def is_prf(self) -> bool:
        return self.issue_type == "PRF"

    @staticmethod
    def classify_issue_type(code: str) -> str:
        """Derive issue type from the issue code prefix."""
        code_upper = code.upper()
        if "EWI" in code_upper:
            return "EWI"
        if "FDM" in code_upper:
            return "FDM"
        if "PRF" in code_upper:
            return "PRF"
        return "EWI"

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "type": self.issue_type,
            "description": self.description or self.name,
            "severity": self.severity,
            "effort_hours": self.effort_hours,
        }
