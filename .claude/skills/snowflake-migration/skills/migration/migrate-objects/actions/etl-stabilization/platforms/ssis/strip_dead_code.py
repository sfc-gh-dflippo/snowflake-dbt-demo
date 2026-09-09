#!/usr/bin/env python3
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

"""Strip ScriptTask dead code from SnowConvert orchestration SQL files.

Removes commented-out C#/XML boilerplate and base64 binary data from SSIS0004
ScriptTask blocks, keeping only the ScriptMain.cs business logic.

Usage:
    python strip_dead_code.py <orchestration_sql_file>

The file is modified in-place. Run after scan_unit.py and backup (Steps 2-3), before fixing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Matches: !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - <description> ***/!!!
RE_SSIS0004_MARKER = re.compile(
    r"^(\s*)!!!RESOLVE EWI!!!\s*/\*\*\*\s*(SSC-EWI-SSIS0004\s*-\s*.*?)\s*\*\*\*/!!!\s*$"
)

# Matches: --</Executable>
RE_EXECUTABLE_CLOSE = re.compile(r"^\s*--</Executable>\s*$")

# Matches: --<Executable ExecutableType="Microsoft.ScriptTask" ...>
RE_EXECUTABLE_OPEN = re.compile(
    r'^(\s*--<Executable\s+ExecutableType="Microsoft\.ScriptTask".*)$'
)

# Matches: <ProjectItem Name="ScriptMain.cs" ...>
RE_SCRIPTMAIN_START = re.compile(
    r'^\s*--\s*<ProjectItem\s+Name="ScriptMain\.cs"'
)

# Matches: </ProjectItem>
RE_PROJECTITEM_END = re.compile(r"</ProjectItem>\s*$")


def strip_scripttask_blocks(sql: str) -> str:
    """Strip ScriptTask boilerplate from orchestration SQL, keeping ScriptMain.cs."""
    lines = sql.splitlines(keepends=True)
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        m = RE_SSIS0004_MARKER.match(line)
        if m:
            indent = m.group(1)
            ewi_text = m.group(2).strip()
            # Replace !!!RESOLVE EWI!!! with --** annotation
            result.append(f"{indent}--** {ewi_text} **\n")
            i += 1
            # Process the block until --</Executable>
            i = _process_scripttask_block(lines, i, result)
        else:
            result.append(line)
            i += 1

    return "".join(result)


def _process_scripttask_block(
    lines: list[str], start: int, result: list[str]
) -> int:
    """Process lines inside a ScriptTask block, keeping only key content.

    Returns the index after the block (past --</Executable>).
    """
    i = start
    while i < len(lines):
        line = lines[i]

        # Keep --<Executable ExecutableType="Microsoft.ScriptTask" ...>
        if RE_EXECUTABLE_OPEN.match(line):
            result.append(line)
            i += 1
            continue

        # Keep --</Executable> (end of block)
        if RE_EXECUTABLE_CLOSE.match(line):
            result.append(line)
            i += 1
            return i

        # Keep ScriptMain.cs content
        if RE_SCRIPTMAIN_START.match(line):
            i = _extract_scriptmain(lines, i, result)
            continue

        # Skip everything else (boilerplate)
        i += 1

    print(
        f"Warning: ScriptTask block starting near line {start} has no --</Executable> close tag.",
        file=sys.stderr,
    )
    return i


def _extract_scriptmain(
    lines: list[str], start: int, result: list[str]
) -> int:
    """Extract ScriptMain.cs content from ProjectItem tags.

    Keeps all lines from <ProjectItem Name="ScriptMain.cs"...> through </ProjectItem>.
    Returns index after the closing </ProjectItem>.
    """
    i = start
    while i < len(lines):
        line = lines[i]
        result.append(line)
        if RE_PROJECTITEM_END.search(line):
            i += 1
            return i
        i += 1
    return i


def strip_file(path: Path) -> None:
    """Strip ScriptTask blocks from an orchestration SQL file in-place."""
    content = path.read_text(encoding="utf-8")
    stripped = strip_scripttask_blocks(content)
    if stripped != content:
        path.write_text(stripped, encoding="utf-8")
        original_lines = len(content.splitlines())
        stripped_lines = len(stripped.splitlines())
        print(f"Stripped: {path.name} ({original_lines} -> {stripped_lines} lines)")
    else:
        print(f"No ScriptTask blocks found: {path.name}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python strip_dead_code.py <orchestration_sql_file>", file=sys.stderr)
        sys.exit(1)

    sql_path = Path(sys.argv[1])
    if not sql_path.is_file():
        print(f"Error: '{sql_path}' not found", file=sys.stderr)
        sys.exit(1)

    strip_file(sql_path)


if __name__ == "__main__":
    main()
