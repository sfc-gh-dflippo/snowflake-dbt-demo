"""Tests for scan_unit.py placeholder detection in sources.yml (PR-3)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR))
from scan_unit import PLACEHOLDER_VALUES, assess_dbt_health  # noqa: E402


def _write_project(root: Path, *, dbt_project: str, sources: str | None) -> Path:
    (root / "models").mkdir(parents=True)
    (root / "dbt_project.yml").write_text(dbt_project, encoding="utf-8")
    if sources is not None:
        (root / "models" / "sources.yml").write_text(sources, encoding="utf-8")
    return root


class TestAssessDbtHealthSourcesPlaceholders(unittest.TestCase):
    def test_sources_yml_your_schema_your_db_sets_has_placeholder_config(self) -> None:
        self.assertIn("YOUR_SCHEMA", PLACEHOLDER_VALUES)
        self.assertIn("YOUR_DB", PLACEHOLDER_VALUES)

        with tempfile.TemporaryDirectory() as tmp:
            project = _write_project(
                Path(tmp) / "m_last_run_date",
                dbt_project=(
                    "name: m_last_run_date\n"
                    "profile: m_last_run_date\n"
                    "version: '1.0.0'\n"
                ),
                sources=(
                    "version: 2\n"
                    "sources:\n"
                    "  - name: raw\n"
                    "    schema: \"{{ var('m_last_run_date_schema', 'YOUR_SCHEMA') }}\"\n"
                    "    database: \"{{ var('m_last_run_date_database', 'YOUR_DB') }}\"\n"
                    "    tables:\n"
                    "      - name: BATCH_INSTANCE\n"
                ),
            )
            health = assess_dbt_health(project)
            self.assertTrue(health["has_placeholder_config"])
            issues = " ".join(health["health_issues"])
            self.assertIn("sources.yml", issues)
            self.assertTrue(
                "YOUR_SCHEMA" in issues or "YOUR_DB" in issues,
                health["health_issues"],
            )

    def test_clean_sources_yml_does_not_flag_placeholder_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = _write_project(
                Path(tmp) / "m_clean",
                dbt_project="name: m_clean\nprofile: m_clean\nversion: '1.0.0'\n",
                sources=(
                    "version: 2\n"
                    "sources:\n"
                    "  - name: raw\n"
                    "    schema: ANALYTICS\n"
                    "    database: PROD_DB\n"
                    "    tables:\n"
                    "      - name: T\n"
                ),
            )
            health = assess_dbt_health(project)
            self.assertFalse(health["has_placeholder_config"])


if __name__ == "__main__":
    unittest.main()
