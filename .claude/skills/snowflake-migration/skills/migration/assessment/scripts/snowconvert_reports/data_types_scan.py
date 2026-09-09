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

"""Extract data-type usage from captured CREATE TABLE DDL.

A bounded extractor, not a parser. The registry carries no column or type
fields, so the DDL each in-scope table points at is the only in-project carrier
of column types. Anything this cannot resolve -- computed columns, table-valued
or nested types, a file it cannot read -- yields nothing, because the report
names the volume inventory script as authoritative and a wrong type is worse
than an absent one.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

# Qualifiers between CREATE and TABLE vary by dialect (MULTISET, SET VOLATILE,
# GLOBAL TEMPORARY, OR REPLACE), so they are counted rather than enumerated.
_CREATE_TABLE = re.compile(r"\bCREATE\s+(?:\w+\s+){0,3}?TABLE\b", re.IGNORECASE)

# Stripped before anything else: a comma inside a comment splits the column
# list and shifts every later item, which reports a column *name* as a type.
_COMMENTS = re.compile(r"--[^\n]*|/\*.*?\*/", re.DOTALL)

# An item in the column list that declares something other than a column.
_NOT_A_COLUMN = re.compile(
    r"^(?:CONSTRAINT|PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK|INDEX|KEY|"
    r"PERIOD\s+FOR|EXCLUDE|LIKE)\b",
    re.IGNORECASE,
)

_QUOTED_NAME = re.compile(r'^(?:\[[^\]]*\]|"[^"]*"|`[^`]*`|[A-Za-z_][\w$@#]*)')

# A computed column puts an expression where a type belongs. The word boundary
# matters: `ASSET` is a type name, not `AS` followed by an expression.
_COMPUTED = re.compile(r"^AS\b", re.IGNORECASE)

# Types whose name is more than one word. Longest first so a prefix match cannot
# claim a shorter name than the DDL actually spells out.
_MULTI_WORD_TYPES: tuple[str, ...] = tuple(
    sorted(
        (
            "INTERVAL YEAR TO MONTH",
            "INTERVAL DAY TO SECOND",
            "TIMESTAMP WITHOUT TIME ZONE",
            "TIMESTAMP WITH TIME ZONE",
            "TIME WITHOUT TIME ZONE",
            "TIME WITH TIME ZONE",
            "CHARACTER VARYING",
            "BINARY VARYING",
            "DOUBLE PRECISION",
        ),
        key=len,
        reverse=True,
    )
)


@dataclass(frozen=True)
class TypeUsage:
    """How much one normalized type name is used across the scanned tables."""

    type_name: str
    table_count: int
    column_count: int


def _column_region(ddl: str) -> str:
    """The text between the parentheses of the first ``CREATE TABLE``.

    Walks to the matching close paren so nested type arguments and
    parenthesised CHECK expressions do not end the region early. Single-quoted
    literals are skipped whole, since a DEFAULT value may contain a paren.
    """
    match = _CREATE_TABLE.search(ddl)
    if not match:
        return ""
    start = ddl.find("(", match.end())
    if start < 0:
        return ""

    depth = 0
    in_string = False
    for index in range(start, len(ddl)):
        char = ddl[index]
        if in_string:
            in_string = char != "'"
            continue
        if char == "'":
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return ddl[start + 1 : index]
    return ""


def _split_items(region: str) -> list[str]:
    """Split a column region on its top-level commas."""
    items: list[str] = []
    depth = 0
    in_string = False
    current: list[str] = []
    for char in region:
        if in_string:
            current.append(char)
            in_string = char != "'"
            continue
        if char == "'":
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            items.append("".join(current))
            current = []
            continue
        current.append(char)
    items.append("".join(current))
    return [item.strip() for item in items if item.strip()]


def _normalize_type(text: str) -> str:
    """Reduce a type region to an uppercase base name ("" if there is none).

    Delimiters go first: a bracketed type (``[int]``) would otherwise be split
    to nothing by the argument split. Length and precision arguments are then
    dropped, so ``DATETIME2(7)`` matches the ``DATETIME2`` coverage row, whose
    note states where the precision caveat applies -- accurate without parsing
    precision.
    """
    undelimited = re.sub(r"[\[\]\"`]", " ", text)
    words = " ".join(re.split(r"\(", undelimited, maxsplit=1)[0].upper().split())
    if not words:
        return ""
    for candidate in _MULTI_WORD_TYPES:
        if words == candidate or words.startswith(candidate + " "):
            return candidate
    return words.split(" ", 1)[0].rsplit(".", 1)[-1]


def scan_ddl(ddl: str) -> tuple[str, ...]:
    """Normalized type name of each column in the first ``CREATE TABLE``."""
    types: list[str] = []
    for item in _split_items(_column_region(_COMMENTS.sub(" ", ddl))):
        if _NOT_A_COLUMN.match(item):
            continue
        name = _QUOTED_NAME.match(item)
        if not name:
            continue
        rest = item[name.end() :].strip()
        if not rest or _COMPUTED.match(rest):
            continue
        normalized = _normalize_type(rest)
        if normalized:
            types.append(normalized)
    return tuple(types)


def aggregate_usage(tables: Iterable[Sequence[str]]) -> tuple[TypeUsage, ...]:
    """Roll per-table type names up into per-type counts.

    Ordered by column count descending, then by name, so the findings table is
    stable across runs and leads with the type the project uses most.
    """
    columns: Counter[str] = Counter()
    tables_using: Counter[str] = Counter()
    for types in tables:
        columns.update(types)
        tables_using.update(set(types))

    return tuple(
        TypeUsage(
            type_name=name,
            table_count=tables_using[name],
            column_count=columns[name],
        )
        for name in sorted(columns, key=lambda n: (-columns[n], n))
    )
