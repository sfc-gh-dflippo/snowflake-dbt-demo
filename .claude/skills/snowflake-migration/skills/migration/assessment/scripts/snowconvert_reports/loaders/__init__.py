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

from .csv_reader import read_csv_rows, load_csv_as
from .elements_loader import load_elements
from .issues_loader import load_issues
from .code_units_loader import load_code_units
from .object_references_loader import load_object_references, load_missing_references
from .partition_loader import load_partition_membership
from .estimation_loader import load_issues_estimation_json, load_object_estimations
from .registry_loader import (
    load_registry_entries,
    build_id_to_name_map,
    iter_in_scope_non_missing,
    load_code_units_from_registry,
    load_object_references_from_registry,
    load_missing_references_from_registry,
    load_missing_dependencies_by_object,
    load_exclusion_findings_from_registry,
)
from .waves_from_registry import (
    synthesize_waves_json,
    write_synthesized_waves_json,
    overlay_real_waves_json,
    write_merged_waves_json,
)
from .unified_loader import (
    load_code_units_auto,
    load_object_references_auto,
    load_missing_references_auto,
)
from .project_config import PROJECT_CONFIG_RELPATH, read_project_name

__all__ = [
    "read_csv_rows",
    "load_csv_as",
    "load_elements",
    "load_issues",
    "load_code_units",
    "load_object_references",
    "load_missing_references",
    "load_partition_membership",
    "load_issues_estimation_json",
    "load_object_estimations",
    # Registry loaders
    "load_registry_entries",
    "build_id_to_name_map",
    "iter_in_scope_non_missing",
    "load_code_units_from_registry",
    "load_object_references_from_registry",
    "load_missing_references_from_registry",
    "load_missing_dependencies_by_object",
    "load_exclusion_findings_from_registry",
    # Registry → waves JSON synthesizer
    "synthesize_waves_json",
    "write_synthesized_waves_json",
    "overlay_real_waves_json",
    "write_merged_waves_json",
    # Unified (auto-dispatch) loaders
    "load_code_units_auto",
    "load_object_references_auto",
    "load_missing_references_auto",
    "PROJECT_CONFIG_RELPATH",
    "read_project_name",
]
