"""Tests for check_sync_leaks.py (PR-4)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import base_session, run_script, write_json

PROFILES_WITH_LEAKS = """\
m_op_ar_accomprice:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: preprod_joel
      user: "{{ env_var('SNOWFLAKE_USER', 'cortex_code') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD', '') }}"
      database: TEST_DB
      schema: ETL_FIX_P2_ARACR
      warehouse: COMPUTE_WH
      role: SYSADMIN
      threads: 1
"""

PROFILES_CLEAN = """\
m_op_ar_accomprice:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
"""


class TestCheckSyncLeaks(unittest.TestCase):
    def test_profiles_yml_with_credentials_and_etl_fix_schema_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, base_session())
            profiles = Path(tmp) / "profiles.yml"
            profiles.write_text(PROFILES_WITH_LEAKS, encoding="utf-8")

            result = run_script("check_sync_leaks.py", str(status_path), str(profiles))
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("profiles.yml", result.stdout)
            self.assertRegex(result.stdout, r"profiles\.yml:\d+: matched ")
            self.assertTrue(
                "account" in result.stdout or "preprod_joel" in result.stdout,
                result.stdout,
            )
            self.assertIn("ETL_FIX_P2_ARACR", result.stdout)

    def test_clean_files_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status_path = Path(tmp) / "session_status.json"
            session = base_session()
            session["test_environment"] = {"database": "TEST_DB", "schema": "TEST_SCHEMA"}
            write_json(status_path, session)
            profiles = Path(tmp) / "profiles.yml"
            profiles.write_text(PROFILES_CLEAN, encoding="utf-8")
            model = Path(tmp) / "model.sql"
            model.write_text("SELECT 1 AS id;\n", encoding="utf-8")

            result = run_script(
                "check_sync_leaks.py", str(status_path), str(profiles), str(model)
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("no leaks found in 2 files", result.stdout)


if __name__ == "__main__":
    unittest.main()
