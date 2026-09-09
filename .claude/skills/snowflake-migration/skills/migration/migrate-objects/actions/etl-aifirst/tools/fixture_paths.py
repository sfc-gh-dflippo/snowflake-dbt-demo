"""Resolve shipped fixtures without machine-absolute paths."""
from __future__ import annotations

import os
from pathlib import Path

# tools/ -> etl-aifirst -> actions -> migrate-objects -> migration -> skills -> plugin -> ai
_AI_ROOT = Path(__file__).resolve().parents[7]
_DEFAULT_FIXTURES = _AI_ROOT / "tests" / "etl-aifirst" / "fixtures"


def fixtures_root() -> Path:
    override = os.environ.get("AIFIRST_FIXTURES")
    return Path(override) if override else _DEFAULT_FIXTURES


def engine_tests_root() -> Path | None:
    """Optional external SnowConvert TestAssemblies root (not shipped)."""
    override = os.environ.get("AIFIRST_ENGINE_TESTS")
    return Path(override) if override else None
