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

"""Reads project-level facts from ``{project_dir}/.scai/config/project.yml``.

``project.yml`` is written and owned by scai (``scai init``), so this module only
reads it. Kept separate from the assessment-metadata service because that owns a
different file; a module named for one file should not reach into another.
"""

from pathlib import Path
from typing import Optional

PROJECT_CONFIG_RELPATH = Path(".scai") / "config" / "project.yml"


def _read_flat_yaml_value(project_dir: Optional[Path], key: str) -> str:
    """Scan ``project.yml`` for ``key`` in a flat ``key: value`` document.

    A line reader rather than a YAML parse because PyYAML is not available —
    ``assessment/pyproject.toml`` declares ``dependencies = []``. Returns ``""``
    on every failure so callers never need a ``try``/``except``.
    """
    if not project_dir:
        return ""
    yml = Path(project_dir) / PROJECT_CONFIG_RELPATH
    if not yml.exists():
        return ""
    try:
        for line in yml.read_text(encoding="utf-8-sig").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or ":" not in stripped:
                continue
            candidate, _, value = stripped.partition(":")
            if candidate.strip() == key:
                return value.strip().strip('"').strip("'")
    except OSError:
        return ""
    return ""


def read_project_name(project_dir: Optional[Path]) -> str:
    """Read ``project_name``; ``""`` when unavailable for any reason."""
    return _read_flat_yaml_value(project_dir, "project_name")
