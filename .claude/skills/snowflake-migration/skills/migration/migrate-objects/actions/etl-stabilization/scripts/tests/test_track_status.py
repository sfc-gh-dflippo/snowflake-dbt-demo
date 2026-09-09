"""Acceptance tests for track_status.py (PR-1, PR-2, PR-3, PR-5)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from helpers import (
    SCRIPTS_DIR,
    base_session,
    load_json,
    minimal_scan,
    run_track_status,
    write_json,
)


class TestPr1InitSourceFilePath(unittest.TestCase):
    def test_init_copies_source_file_path_from_scan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            scan_path = unit / "planning" / "scan.json"
            write_json(scan_path, minimal_scan(source_file_path="/sanitized/source.xml"))

            result = run_track_status("init", str(scan_path))
            self.assertEqual(result.returncode, 0, result.stderr)

            session = load_json(unit / "tracking" / "session_status.json")
            self.assertEqual(session.get("source_file_path"), "/sanitized/source.xml")


class TestPr1UsageStartPhase(unittest.TestCase):
    def test_bare_invocation_usage_includes_start_phase(self) -> None:
        result = run_track_status()
        self.assertNotEqual(result.returncode, 0)
        combined = result.stdout + result.stderr
        self.assertIn("start-phase", combined)
        self.assertIn("session_status.json", combined)


class TestPr1ValidatePhaseBreakdown(unittest.TestCase):
    def test_validate_phase_prints_needs_user_distinctly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, base_session())

            result = run_track_status("validate-phase", str(status_path), "1")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Needs-user:   1", result.stdout)
            self.assertIn("Fixed/passed: 2", result.stdout)
            self.assertIn("PASS:", result.stdout)


class TestPr1ListTestFiles(unittest.TestCase):
    def test_list_test_files_uses_tests_orchestration_not_phase_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            stmt = "public.wf_op_ar_accomprice"
            orch_tests = unit / "stabilization" / "tests" / "orchestration" / stmt
            orch_tests.mkdir(parents=True)
            (orch_tests / "el_fixed_a.sql").write_text("SELECT 1;\n", encoding="utf-8")
            (orch_tests / "grouped_inf0058_dg1.sql").write_text("SELECT 1;\n", encoding="utf-8")
            # decoy in the old (wrong) phase-dir location
            decoy = unit / "stabilization" / "phases" / "phase-1" / stmt
            decoy.mkdir(parents=True)
            (decoy / "el_fixed_a.sql").write_text("SELECT decoy;\n", encoding="utf-8")

            session = base_session(unit_path=str(unit))
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "validate-phase", str(status_path), "1", "--list-test-files"
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("tests/orchestration/", result.stdout)
            self.assertNotIn("phases/phase-1/", result.stdout)
            self.assertGreaterEqual(result.stdout.count("el_fixed_a.sql"), 1)

    def test_list_test_files_finds_schema_short_name_layout(self) -> None:
        """Real agent output: tests/orchestration/<schema>/<last_dot_segment>.sql."""
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            public = unit / "stabilization" / "tests" / "orchestration" / "public"
            public.mkdir(parents=True)
            files = [
                "s_m_last_run_date.sql",
                "wk_pl_acr_booking_fact.sql",
                "s_m_fl_tmp_bookings_services_upd.sql",
                "s_GEN_PARAMETER_FILE.sql",
                "s_m_pl_acr_booking_fact_trans_point_upd.sql",
                "wf_bs_facts_fl_to_pl.sql",
            ]
            for name in files:
                (public / name).write_text("SELECT 1;\n", encoding="utf-8")

            session = base_session(unit_path=str(unit))
            session["elements"] = [
                {
                    "name": "public.wf_bs_facts_fl_to_pl",
                    "statement": "public.wf_bs_facts_fl_to_pl",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_bs_facts_fl_to_pl.s_m_pl_acr_booking_fact_trans_point_upd",
                    "statement": "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_s_m_pl_acr_booking_fact_trans_point_upd",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_bs_facts_fl_to_pl.s_GEN_PARAMETER_FILE",
                    "statement": "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_s_GEN_PARAMETER_FILE",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_bs_facts_fl_to_pl.s_m_fl_tmp_bookings_services_upd",
                    "statement": "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_s_m_fl_tmp_bookings_services_upd",
                    "status": "skipped",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_bs_facts_fl_to_pl.wk_pl_acr_booking_fact",
                    "statement": "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_wk_pl_acr_booking_fact",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_bs_facts_fl_to_pl.s_m_last_run_date",
                    "statement": "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_s_m_last_run_date",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "validate-phase", str(status_path), "1", "--list-test-files"
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Test files (6):", result.stdout)
            for name in files:
                self.assertIn(name, result.stdout)
            self.assertNotIn("(not found)", result.stdout)
            # Old dotted-statement / fully-qualified-name construction must not be used
            self.assertNotIn(
                "public.f_Warehouse_presentation_wf_bs_facts_fl_to_pl_s_m_last_run_date/",
                result.stdout,
            )

    def test_list_test_files_reports_all_short_name_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            orch = unit / "stabilization" / "tests" / "orchestration"
            (orch / "public").mkdir(parents=True)
            (orch / "other_schema").mkdir(parents=True)
            (orch / "public" / "s_m_last_run_date.sql").write_text("SELECT 1;\n", encoding="utf-8")
            (orch / "other_schema" / "s_m_last_run_date.sql").write_text("SELECT 2;\n", encoding="utf-8")

            session = base_session(unit_path=str(unit))
            session["elements"] = [
                {
                    "name": "f_Warehouse_presentation.wf_a.s_m_last_run_date",
                    "statement": "public.wf_a_s_m_last_run_date",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
                {
                    "name": "f_Warehouse_presentation.wf_b.s_m_last_run_date",
                    "statement": "public.wf_b_s_m_last_run_date",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "validate-phase", str(status_path), "1", "--list-test-files"
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("2 candidates", result.stdout)
            self.assertIn("(verify)", result.stdout)
            self.assertIn("public/s_m_last_run_date.sql", result.stdout.replace("\\", "/"))
            self.assertIn("other_schema/s_m_last_run_date.sql", result.stdout.replace("\\", "/"))

    def test_list_test_files_reports_missing_short_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            (unit / "stabilization" / "tests" / "orchestration").mkdir(parents=True)
            session = base_session(unit_path=str(unit))
            session["elements"] = [
                {
                    "name": "f_Warehouse_presentation.wf.s_missing",
                    "statement": "public.wf_s_missing",
                    "status": "fixed",
                    "phase": 1,
                    "test_strategy": "isolated",
                },
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "validate-phase", str(status_path), "1", "--list-test-files"
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("s_missing.sql: (not found)", result.stdout)


class TestPr1UnverifiedDoesNotBlockComplete(unittest.TestCase):
    def test_unverified_dbt_node_does_not_block_complete_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "m_op_ar_accomprice"
            tests_root = unit / "stabilization" / "tests" / "dbt" / project
            (tests_root / "seeds").mkdir(parents=True)
            (tests_root / "tests").mkdir(parents=True)
            (tests_root / "seeds" / "seed.csv").write_text("id\n1\n", encoding="utf-8")
            (tests_root / "tests" / "test_x.sql").write_text("SELECT 1;\n", encoding="utf-8")
            (tests_root / "test_report.md").write_text("# report\n", encoding="utf-8")
            learnings = unit / "stabilization" / "phases" / "phase-2"
            learnings.mkdir(parents=True)
            (learnings / f"dbt_learnings_{project}.md").write_text("# learnings\n", encoding="utf-8")

            session = base_session(unit_path=str(unit))
            session["dbt_nodes"] = [
                {
                    "name": "stg_raw",
                    "path": "models/staging/stg_raw.sql",
                    "status": "unverified",
                    "project": project,
                    "phase": 2,
                }
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status("complete-phase", str(status_path), "2")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("marked as completed", result.stdout)


class TestPr2AssignDbtPhase(unittest.TestCase):
    def test_assign_dbt_phase_sets_phase_on_matching_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = base_session()
            session["dbt_nodes"] = [
                {"name": "n1", "path": "models/n1.sql", "status": "pending", "project": "m_op_ar_accomprice", "phase": None},
                {"name": "n2", "path": "models/n2.sql", "status": "pending", "project": "m_op_ar_accomprice", "phase": None},
                {"name": "other", "path": "models/o.sql", "status": "pending", "project": "m_other", "phase": None},
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "assign-dbt-phase", str(status_path), "--phase", "2", "--project", "m_op_ar_accomprice"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Assigned 2 dbt nodes", result.stdout)

            saved = load_json(status_path)
            by_name = {n["name"]: n for n in saved["dbt_nodes"]}
            self.assertEqual(by_name["n1"]["phase"], 2)
            self.assertEqual(by_name["n2"]["phase"], 2)
            self.assertIsNone(by_name["other"]["phase"])

    def test_assign_dbt_phase_listed_in_usage(self) -> None:
        result = run_track_status()
        combined = result.stdout + result.stderr
        self.assertIn("assign-dbt-phase", combined)

    def test_validate_phase_dbt_scope_does_not_require_elements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = base_session()
            session["elements"] = []  # dbt-scope phases have zero orchestration elements
            session["dbt_nodes"] = [
                {"name": "n1", "path": "models/n1.sql", "status": "fixed", "project": "m_op_ar_accomprice", "phase": 2},
                {"name": "n2", "path": "models/n2.sql", "status": "unverified", "project": "m_op_ar_accomprice", "phase": 2},
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status("validate-phase", str(status_path), "2")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotIn("no elements assigned", result.stderr)
            self.assertIn("Validation (dbt)", result.stdout)
            self.assertIn("PASS: All dbt nodes resolved.", result.stdout)

    def test_validate_phase_infers_dbt_from_assigned_nodes_when_scope_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = base_session()
            session["elements"] = []
            session["roadmap"]["phases"][1].pop("scope")
            session["dbt_nodes"] = [
                {
                    "name": "n1",
                    "path": "models/n1.sql",
                    "status": "fixed",
                    "project": "m_op_ar_accomprice",
                    "phase": 2,
                }
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status("validate-phase", str(status_path), "2")

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotIn("no elements assigned", result.stderr)
            self.assertIn("Validation (dbt)", result.stdout)
            self.assertIn("PASS: All dbt nodes resolved.", result.stdout)

    def test_update_dbt_node_syncs_top_level_dbt_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = base_session()
            session["dbt_projects"] = [
                {
                    "name": "m_op_ar_accomprice",
                    "path": "m_op_ar_accomprice",
                    "status": "pending",
                    "nodes": [{"name": "n1", "path": "models/n1.sql", "status": "pending"}],
                }
            ]
            session["dbt_nodes"] = [
                {"name": "n1", "path": "models/n1.sql", "status": "pending", "project": "m_op_ar_accomprice", "phase": 2},
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status(
                "update-dbt-node", str(status_path), "m_op_ar_accomprice", "n1",
                "--status", "unverified", "--reason", "no warehouse",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = load_json(status_path)
            self.assertEqual(saved["dbt_nodes"][0]["status"], "unverified")
            self.assertEqual(saved["dbt_projects"][0]["nodes"][0]["status"], "unverified")


class TestPr5ConcurrentUpdates(unittest.TestCase):
    def test_concurrent_update_dbt_node_both_survive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = base_session()
            session["dbt_projects"] = [
                {
                    "name": "m_op_ar_accomprice",
                    "path": "m_op_ar_accomprice",
                    "status": "pending",
                    "nodes": [
                        {"name": "node_a", "path": "models/a.sql", "status": "pending"},
                        {"name": "node_b", "path": "models/b.sql", "status": "pending"},
                    ],
                }
            ]
            session["dbt_nodes"] = [
                {"name": "node_a", "path": "models/a.sql", "status": "pending", "project": "m_op_ar_accomprice", "phase": 2},
                {"name": "node_b", "path": "models/b.sql", "status": "pending", "project": "m_op_ar_accomprice", "phase": 2},
            ]
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            env = os.environ.copy()
            env["PYTHONPATH"] = str(SCRIPTS_DIR) + os.pathsep + env.get("PYTHONPATH", "")

            def update(node: str, status: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    [
                        sys.executable, str(SCRIPTS_DIR / "track_status.py"),
                        "update-dbt-node", str(status_path), "m_op_ar_accomprice", node,
                        "--status", status,
                    ],
                    capture_output=True, text=True, env=env,
                )

            with ThreadPoolExecutor(max_workers=2) as pool:
                futs = [
                    pool.submit(update, "node_a", "fixed"),
                    pool.submit(update, "node_b", "unverified"),
                ]
                results = [f.result() for f in futs]

            for r in results:
                self.assertEqual(r.returncode, 0, r.stderr)

            saved = load_json(status_path)
            by_name = {n["name"]: n["status"] for n in saved["dbt_nodes"]}
            self.assertEqual(by_name["node_a"], "fixed")
            self.assertEqual(by_name["node_b"], "unverified")
            nested = {n["name"]: n["status"] for n in saved["dbt_projects"][0]["nodes"]}
            self.assertEqual(nested["node_a"], "fixed")
            self.assertEqual(nested["node_b"], "unverified")


def _write_dbt_complete_phase_artifacts(unit: Path, project: str) -> None:
    tests_root = unit / "stabilization" / "tests" / "dbt" / project
    (tests_root / "seeds").mkdir(parents=True)
    (tests_root / "tests").mkdir(parents=True)
    (tests_root / "seeds" / "seed.csv").write_text("id\n1\n", encoding="utf-8")
    (tests_root / "tests" / "test_x.sql").write_text("SELECT 1;\n", encoding="utf-8")
    (tests_root / "test_report.md").write_text("# report\n", encoding="utf-8")
    learnings = unit / "stabilization" / "phases" / "phase-2"
    learnings.mkdir(parents=True)
    (learnings / f"dbt_learnings_{project}.md").write_text("# learnings\n", encoding="utf-8")


def _dbt_session_for_project(unit: Path, project: str) -> dict:
    session = base_session(unit_path=str(unit))
    session["dbt_projects"] = [
        {"name": project, "path": project, "status": "pending", "nodes": []}
    ]
    session["dbt_nodes"] = [
        {
            "name": "stg_raw",
            "path": "models/staging/stg_raw.sql",
            "status": "unverified",
            "project": project,
            "phase": 2,
        }
    ]
    return session


class TestPr3DbtProjectYmlSanity(unittest.TestCase):
    def test_complete_phase_fails_when_models_key_is_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            _write_dbt_complete_phase_artifacts(unit, project)
            (unit / project).mkdir(parents=True)
            (unit / project / "dbt_project.yml").write_text(
                "name: foo\n"
                "profile: snowflake_test\n"
                "models:\n"
                "  YOUR_PROJECT_NAME:\n"
                "    staging:\n"
                "      +materialized: view\n",
                encoding="utf-8",
            )
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, _dbt_session_for_project(unit, project))

            result = run_track_status("complete-phase", str(status_path), "2")
            self.assertNotEqual(result.returncode, 0)
            combined = result.stderr + result.stdout
            self.assertIn("dbt_project.yml", combined)
            self.assertIn("YOUR_PROJECT_NAME", combined)
            self.assertIn("name: 'foo'", combined)

    def test_complete_phase_passes_when_models_key_matches_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            _write_dbt_complete_phase_artifacts(unit, project)
            (unit / project).mkdir(parents=True)
            (unit / project / "dbt_project.yml").write_text(
                "name: foo\n"
                "profile: foo\n"
                "models:\n"
                "  foo:\n"
                "    staging:\n"
                "      +materialized: view\n"
                "    intermediate:\n"
                "      +materialized: ephemeral\n"
                "    marts:\n"
                "      +materialized: incremental\n",
                encoding="utf-8",
            )
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, _dbt_session_for_project(unit, project))

            result = run_track_status("complete-phase", str(status_path), "2")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("marked as completed", result.stdout)

    def test_complete_phase_infers_dbt_from_assigned_nodes_when_scope_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            _write_dbt_complete_phase_artifacts(unit, project)
            session = _dbt_session_for_project(unit, project)
            session["elements"] = []
            session["roadmap"]["phases"][1].pop("scope")
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status("complete-phase", str(status_path), "2")

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("marked as completed", result.stdout)

    def test_complete_phase_skips_check_when_dbt_project_yml_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            _write_dbt_complete_phase_artifacts(unit, project)
            (unit / project).mkdir(parents=True)
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, _dbt_session_for_project(unit, project))

            result = run_track_status("complete-phase", str(status_path), "2")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotIn("models: key", result.stderr + result.stdout)

    def test_validate_phase_fails_on_models_key_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            (unit / project).mkdir(parents=True)
            (unit / project / "dbt_project.yml").write_text(
                "name: foo\nmodels:\n  YOUR_PROJECT_NAME:\n    +materialized: view\n",
                encoding="utf-8",
            )
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, _dbt_session_for_project(unit, project))

            result = run_track_status("validate-phase", str(status_path), "2")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("YOUR_PROJECT_NAME", result.stderr + result.stdout)


class TestCompletePhaseArtifactLayout(unittest.TestCase):
    def test_complete_phase_dbt_finds_learnings_under_underscore_phase_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            project = "foo"
            tests_root = unit / "stabilization" / "tests" / "dbt" / project
            (tests_root / "seeds").mkdir(parents=True)
            (tests_root / "tests").mkdir(parents=True)
            (tests_root / "seeds" / "seed.csv").write_text("id\n1\n", encoding="utf-8")
            (tests_root / "tests" / "test_x.sql").write_text("SELECT 1;\n", encoding="utf-8")
            (tests_root / "test_report.md").write_text("# report\n", encoding="utf-8")
            underscore = unit / "stabilization" / "phases" / "phase_2"
            underscore.mkdir(parents=True)
            (underscore / f"dbt_learnings_{project}.md").write_text("# learnings\n", encoding="utf-8")

            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, _dbt_session_for_project(unit, project))

            result = run_track_status("complete-phase", str(status_path), "2")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("marked as completed", result.stdout)

    def test_complete_phase_orch_accepts_fix_log_instead_of_batch_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            tracking = unit / "stabilization" / "tracking"
            tracking.mkdir(parents=True)
            (tracking / "fix-log.md").write_text("# fixes applied in main session\n", encoding="utf-8")
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, base_session(unit_path=str(unit)))

            result = run_track_status("complete-phase", str(status_path), "1")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotIn("baseline_batch_", result.stderr)
            self.assertIn("marked as completed", result.stdout)

    def test_complete_phase_orch_finds_batch_files_under_underscore_phase_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            phase = unit / "stabilization" / "phases" / "phase_1"
            phase.mkdir(parents=True)
            (phase / "baseline_batch_1.md").write_text("# baseline\n", encoding="utf-8")
            (phase / "batch_1.md").write_text("# batch\n", encoding="utf-8")
            (phase / "learnings_batch_1.md").write_text("# learnings\n", encoding="utf-8")
            (phase / "apply_report.md").write_text("# apply\n", encoding="utf-8")
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, base_session(unit_path=str(unit)))

            result = run_track_status("complete-phase", str(status_path), "1")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("marked as completed", result.stdout)

    def test_complete_phase_orch_still_requires_terminal_elements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unit = Path(tmp)
            tracking = unit / "stabilization" / "tracking"
            tracking.mkdir(parents=True)
            (tracking / "fix-log.md").write_text("# fixes\n", encoding="utf-8")
            session = base_session(unit_path=str(unit))
            session["elements"][0]["status"] = "pending"
            status_path = Path(tmp) / "session_status.json"
            write_json(status_path, session)

            result = run_track_status("complete-phase", str(status_path), "1")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not in terminal status", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
