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

"""Shared ElementRepository — loads ETL components from ETL.Elements.csv.

Follows Open-Closed Principle: parameterized via constructor (technology_filter,
excluded_subtypes) rather than requiring subclasses per ETL tool. New ETL tools
(DataStage, Talend, etc.) use the same class with different filter parameters.
"""

from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from ..loaders import load_elements
from ..models import Component


class ElementRepository:
    """Loads components from ETL.Elements.csv with optional filtering.

    Args:
        file_path: Path to ETL.Elements.csv
        excluded_subtypes: Component subtypes to exclude from results
        technology_filter: If set, only load elements matching this technology
            (e.g. "InformaticaPowerCenter"). None means load all technologies.
    """

    def __init__(
        self,
        file_path: str,
        excluded_subtypes: Set[str] = None,
        technology_filter: Optional[str] = None,
    ):
        self.file_path = Path(file_path)
        self.excluded_subtypes = excluded_subtypes or set()
        self.technology_filter = technology_filter

    def load_components(self) -> Tuple[Dict[Tuple[str, str], Component], int]:
        """Load and filter components from the CSV.

        Returns:
            Tuple of (components_by_key dict, excluded_count)
            where key is (file_name, full_name).
        """
        elements = load_elements(self.file_path)

        components_by_key = {}
        excluded_count = 0

        for elem in elements:
            if not elem.full_name or not elem.file_name:
                continue
            if self.technology_filter and elem.technology != self.technology_filter:
                continue
            if elem.subtype in self.excluded_subtypes:
                excluded_count += 1
                continue

            component = Component(
                full_name=elem.full_name,
                file_name=elem.file_name,
                technology=elem.technology,
                category=elem.category,
                subtype=elem.subtype,
                status=elem.status,
                entry_kind=elem.entry_kind,
                additional_info=elem.additional_info,
            )
            component_key = (elem.file_name, elem.full_name)
            components_by_key[component_key] = component

        return components_by_key, excluded_count
