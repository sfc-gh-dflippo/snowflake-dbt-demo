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

"""Shared N/A sentinel detection and sanitization utilities."""

from __future__ import annotations

import re

NA_VALUES = frozenset({"N/A", "n/a", "NA", "na", ""})

_NA_SEGMENT_RE = re.compile(r"\[N/A\]\.")


def is_na(value: str | None) -> bool:
    """Return True if *value* is None, empty, or a common N/A sentinel."""
    if value is None:
        return True
    return str(value).strip() in NA_VALUES


def sanitize_na(value: str | None, fallback: str = "-") -> str:
    """Replace N/A-like values with *fallback*."""
    return fallback if is_na(value) else str(value).strip()


def strip_na_identifier(identifier: str) -> str:
    """Remove ``[N/A].`` segments from a multi-part SQL identifier.

    ``[N/A].[dbo].[MyTable]`` → ``[dbo].[MyTable]``
    """
    if not identifier:
        return identifier
    return _NA_SEGMENT_RE.sub("", identifier)
