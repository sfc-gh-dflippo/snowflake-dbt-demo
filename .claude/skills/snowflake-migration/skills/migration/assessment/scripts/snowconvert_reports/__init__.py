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

"""snowconvert_reports -- shared data access layer for SnowConvert assessment reports."""

from .na_utils import NA_VALUES, is_na, sanitize_na, strip_na_identifier
from .models import (
    IssueRecord,
    Element,
    TopLevelCodeUnit,
    ObjectReference,
    PartitionMember,
    IssueEstimationEntry,
    SeverityBaseline,
    ObjectEstimation,
    Issue,
    Component,
    ETLComponent,
    ETLIssue,
)
from .loaders import (
    read_csv_rows,
    load_csv_as,
    load_elements,
    load_issues,
    load_code_units,
    load_object_references,
    load_missing_references,
    load_partition_membership,
    load_issues_estimation_json,
    load_object_estimations,
    # Registry loaders
    load_registry_entries,
    build_id_to_name_map,
    load_code_units_from_registry,
    load_object_references_from_registry,
    load_missing_references_from_registry,
    load_exclusion_findings_from_registry,
    # Unified (auto-dispatch) loaders
    load_code_units_auto,
    load_object_references_auto,
    load_missing_references_auto,
)
from .services import (
    IssueEffortService,
    ReportFinder,
)
from .conversion_status import (
    STATUS_MISSING,
    STATUS_NOT_SUPPORTED,
    STATUS_PENDING,
    STATUS_REQUIRE_ATTENTION,
    STATUS_SUCCESS,
    aggregate_etl_issues,
    is_etl,
    map_conversion_status,
)
from .testing_readiness import (
    TestingReadiness,
    UnitBuckets,
    load_testing_readiness,
    normalize_dialect,
)
from .data_types_scan import TypeUsage, aggregate_usage, scan_ddl
from .type_coverage import TypeCoverage, coverage_for
from .data_migration_readiness import (
    DataMigrationReadiness,
    TypeFinding,
    load_data_migration_readiness,
)
from .repositories import (
    ElementRepository,
    IssueRepository,
)

__all__ = [
    # N/A utilities
    "NA_VALUES",
    "is_na",
    "sanitize_na",
    "strip_na_identifier",
    # Models
    "IssueRecord",
    "Element",
    "TopLevelCodeUnit",
    "ObjectReference",
    "PartitionMember",
    "IssueEstimationEntry",
    "SeverityBaseline",
    "ObjectEstimation",
    "Issue",
    "Component",
    "ETLComponent",
    "ETLIssue",
    # Loaders
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
    "load_exclusion_findings_from_registry",
    # Unified (auto-dispatch) loaders
    "load_code_units_auto",
    "load_object_references_auto",
    "load_missing_references_auto",
    # Services
    "IssueEffortService",
    "ReportFinder",
    # Repositories
    "ElementRepository",
    "IssueRepository",
    # Registry conversion status
    "STATUS_MISSING",
    "STATUS_NOT_SUPPORTED",
    "STATUS_PENDING",
    "STATUS_REQUIRE_ATTENTION",
    "STATUS_SUCCESS",
    "aggregate_etl_issues",
    "is_etl",
    "map_conversion_status",
    # Testing readiness
    "TestingReadiness",
    "UnitBuckets",
    "load_testing_readiness",
    "normalize_dialect",
    # Data migration readiness
    "DataMigrationReadiness",
    "TypeCoverage",
    "TypeFinding",
    "TypeUsage",
    "aggregate_usage",
    "coverage_for",
    "load_data_migration_readiness",
    "scan_ddl",
]
