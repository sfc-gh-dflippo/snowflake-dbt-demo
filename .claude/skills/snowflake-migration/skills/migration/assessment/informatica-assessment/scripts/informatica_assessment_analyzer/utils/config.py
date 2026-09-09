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

"""Configuration constants for Informatica assessment analyzer."""

# Component subtypes to exclude from analysis (structural elements only).
# These are infrastructure elements that don't represent meaningful ETL logic.
EXCLUDED_COMPONENT_SUBTYPES = frozenset(
    {
        "Scheduler",
    }
)

# Informatica transformation types that represent source data entry points.
SOURCE_TYPES = frozenset(
    {
        "Source Definition",
        "Source Qualifier",
    }
)

# Informatica transformation types that represent data destinations.
DESTINATION_TYPES = frozenset(
    {
        "Target Definition",
    }
)

# Informatica transformation types that represent data processing logic.
TRANSFORM_TYPES = frozenset(
    {
        "Expression",
        "Lookup Procedure",
        "Filter",
        "Joiner",
        "Aggregator",
        "Sorter",
        "Rank",
        "Router",
        "Normalizer",
        "Sequence",
        "Update Strategy",
        "Union",
        "Custom Transformation",
        "Java Transformation",
        "SQL Transformation",
        "Stored Procedure",
        "XML Generator",
        "XML Parser",
        "HTTP Transformation",
        "Transaction Control",
        "External Procedure",
    }
)

# Workflow-level task types (control flow).
WORKFLOW_TASK_TYPES = frozenset(
    {
        "SESSION",
        "Session",
        "Timer",
        "START",
        "Start",
        "Command",
        "Decision",
        "Assignment",
        "Event Wait",
        "Event Raise",
        "Email",
        "Link",
        "Control",
    }
)
