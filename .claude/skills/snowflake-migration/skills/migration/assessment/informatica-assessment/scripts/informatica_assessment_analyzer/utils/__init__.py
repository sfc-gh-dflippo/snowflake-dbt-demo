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

"""Informatica-specific utility functions. The sanitize_filename here handles XML paths (backslashes, dots) rather than URL-encoded .dtsx paths."""

from .config import EXCLUDED_COMPONENT_SUBTYPES


def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename.

    Replaces path separators, spaces, and special characters with underscores.
    """
    result = name.replace("\\", "_").replace("/", "_").replace(" ", "_")
    result = result.replace(".", "_").replace(":", "_")
    # Remove consecutive underscores
    while "__" in result:
        result = result.replace("__", "_")
    return result.strip("_")


__all__ = ["sanitize_filename", "EXCLUDED_COMPONENT_SUBTYPES"]
