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

"""Detect test-environment / credential leaks before syncing fixes back.

Usage:
    python check_sync_leaks.py <session_status.json> <file1> [<file2> ...]

Exit 1 if any leak is found; exit 0 with a one-line summary otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ETL_FIX_RE = re.compile(r"ETL_FIX_P\d+_\w+")
CREDENTIAL_KEY_RE = re.compile(
    r"^\s*(password|account|authenticator|private_key_path)\s*:\s*(.*?)\s*$"
)
PLACEHOLDER_VALUE_RE = re.compile(r"^(YOUR_|your_)")
ENV_VAR_RE = re.compile(r"\{\{\s*env_var\s*\(")


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _is_placeholder_credential(value: str) -> bool:
    stripped = value.strip().strip("\"'")
    if not stripped:
        return True
    if PLACEHOLDER_VALUE_RE.match(stripped):
        return True
    if ENV_VAR_RE.search(stripped):
        return True
    return False


def check_file(path: Path, database: str, schema: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    is_profiles = path.name == "profiles.yml"
    for i, line in enumerate(text.splitlines(), 1):
        if database and database in line:
            hits.append((i, database))
        if schema and schema in line:
            hits.append((i, schema))
        etl_match = ETL_FIX_RE.search(line)
        if etl_match:
            hits.append((i, etl_match.group(0)))
        if is_profiles:
            cred = CREDENTIAL_KEY_RE.match(line)
            if cred and not _is_placeholder_credential(cred.group(2)):
                hits.append((i, cred.group(1) + ":"))
    return hits


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: python check_sync_leaks.py <session_status.json> <file1> [<file2> ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    status_path = Path(sys.argv[1])
    if not status_path.is_file():
        print(f"Error: '{status_path}' not found", file=sys.stderr)
        sys.exit(1)

    session = load_json(status_path)
    test_env = session.get("test_environment") or {}
    database = test_env.get("database") or ""
    schema = test_env.get("schema") or ""

    files = [Path(p) for p in sys.argv[2:]]
    any_hits = False
    for path in files:
        if not path.is_file():
            print(f"Error: '{path}' not found", file=sys.stderr)
            sys.exit(1)
        for line_no, pattern in check_file(path, database, schema):
            print(f"{path}:{line_no}: matched '{pattern}'")
            any_hits = True

    if any_hits:
        sys.exit(1)

    print(f"no leaks found in {len(files)} files")


if __name__ == "__main__":
    main()
