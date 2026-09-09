"""Unit tests for the SAS -> Code Unit Registry emitter (stdlib only, fast).

Run from the tool dir:
    python3 -m unittest discover -s tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Make the tool dir importable so `sas_analyzer` resolves when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sas_analyzer.cur_emitter import (  # noqa: E402
    CurEmitter,
    canonical_name,
    macro_arguments,
    object_type_from_sql,
    unit_id,
)

PROC_MACRO = """%macro score(minval=0, label);
  data WORK.scored;
    set STG.region;
    if amount > &minval then flag=1;
    retain running_total;
  run;
%mend score;
"""

PURE_SQL = """proc sql;
  create table WORK.region as select * from STG.region_raw;
quit;
"""

REQUIRED_KEYS = {
    "id", "schemaVersion", "kind", "inScope", "isMissing",
    "source", "target", "files", "dependencies", "codeStatus",
    "signature", "extensions", "planning", "updatedAt",
}


class HelperTests(unittest.TestCase):
    def test_canonical_and_id_deterministic(self):
        self.assertEqual(canonical_name("score_customers"), "SAS.SCORE_CUSTOMERS")
        self.assertEqual(unit_id("score_customers"), unit_id("score_customers"))
        self.assertNotEqual(unit_id("a"), unit_id("b"))

    def test_object_type_from_sql(self):
        self.assertEqual(object_type_from_sql("CREATE OR REPLACE PROCEDURE p() ..."), "procedure")
        self.assertEqual(object_type_from_sql("create function f() ..."), "function")
        self.assertEqual(object_type_from_sql("CREATE TABLE t AS SELECT 1"), "table")
        self.assertEqual(object_type_from_sql("CREATE VIEW v AS SELECT 1"), "view")
        self.assertIsNone(object_type_from_sql("SELECT 1"))

    def test_macro_arguments(self):
        args = macro_arguments(PROC_MACRO)
        names = [a["name"] for a in args]
        self.assertEqual(names, ["minval", "label"])
        # minval has a default -> not required; label has none -> required
        by_name = {a["name"]: a for a in args}
        self.assertFalse(by_name["minval"]["required"])
        self.assertTrue(by_name["label"]["required"])

    def test_macro_arguments_none(self):
        self.assertEqual(macro_arguments("data x; run;"), [])


class RegisterSourcesTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "project"
        self.src = Path(self._tmp.name) / "sas"
        self.src.mkdir(parents=True)
        (self.src / "score_customers.sas").write_text(PROC_MACRO, encoding="utf-8")
        (self.src / "build_region.sas").write_text(PURE_SQL, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _register(self):
        emitter = CurEmitter(self.root)
        return emitter, emitter.register_sources(
            sorted(self.src.glob("*.sas")), source_root=self.src, target_schema="ANALYTICS.SAS_OUT"
        )

    def test_scaffold_and_entries_written(self):
        emitter, entries = self._register()
        self.assertTrue((self.root / ".scai").is_dir())
        self.assertEqual(len(entries), 2)
        files = sorted(p.name for p in emitter.registry_dir.glob("*.json"))
        self.assertEqual(len(files), 2)

    def test_entry_shape_matches_contract(self):
        _, entries = self._register()
        for entry in entries:
            self.assertEqual(REQUIRED_KEYS - set(entry), set(), f"missing keys in {entry['id']}")
            self.assertEqual(entry["kind"], "databaseObject")
            self.assertEqual(entry["source"]["platform"], "sas")
            self.assertEqual(entry["schemaVersion"], 1)
            self.assertEqual(entry["target"]["database"], "ANALYTICS")
            self.assertEqual(entry["target"]["schema"], "SAS_OUT")
            self.assertTrue(entry["files"]["source"]["checksum"])

    def test_object_type_inference(self):
        _, entries = self._register()
        by_name = {e["source"]["name"]: e for e in entries}
        self.assertEqual(by_name["score_customers"]["source"]["objectType"], "procedure")
        self.assertEqual(by_name["build_region"]["source"]["objectType"], "table")

    def test_dependency_edges(self):
        # score_customers reads STG.region; build_region creates WORK.region.
        # These do not overlap, so add an explicit cross-file dependency:
        (self.src / "score_customers.sas").write_text(
            PROC_MACRO.replace("STG.region", "WORK.region"), encoding="utf-8"
        )
        _, entries = self._register()
        by_name = {e["source"]["name"]: e for e in entries}
        dep_ids = [d["id"] for d in by_name["score_customers"]["dependencies"]["dependsOn"]]
        self.assertIn(unit_id("build_region"), dep_ids)
        self.assertIn(unit_id("score_customers"), by_name["build_region"]["dependencies"]["requiredBy"])
        self.assertGreaterEqual(by_name["score_customers"]["planning"]["topologicalRank"], 1)

    def test_idempotent(self):
        emitter, _ = self._register()
        first = {p.name: p.read_text() for p in emitter.registry_dir.glob("*.json")}
        emitter.register_sources(
            sorted(self.src.glob("*.sas")), source_root=self.src, target_schema="ANALYTICS.SAS_OUT"
        )
        second = {p.name: p.read_text() for p in emitter.registry_dir.glob("*.json")}
        self.assertEqual(set(first), set(second))  # same ids/filenames


class AttachConvertedTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "project"
        self.src = Path(self._tmp.name) / "sas"
        self.src.mkdir(parents=True)
        (self.src / "score_customers.sas").write_text(PROC_MACRO, encoding="utf-8")
        (self.src / "build_region.sas").write_text(PURE_SQL, encoding="utf-8")
        (self.src / "big_model.sas").write_text(PROC_MACRO, encoding="utf-8")
        self.emitter = CurEmitter(self.root)
        self.emitter.register_sources(
            sorted(self.src.glob("*.sas")), source_root=self.src, target_schema="ANALYTICS.SAS_OUT"
        )
        (self.root / "snowflake").mkdir(exist_ok=True)
        (self.root / "snowflake" / "score_customers.sql").write_text(
            "CREATE OR REPLACE PROCEDURE score_customers(MINVAL FLOAT) RETURNS STRING LANGUAGE SQL AS $$ BEGIN RETURN 'ok'; END; $$;",
            encoding="utf-8",
        )
        (self.root / "snowflake" / "build_region.sql").write_text(
            "CREATE OR REPLACE TABLE ANALYTICS.SAS_OUT.build_region AS SELECT 1;", encoding="utf-8"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def _state(self):
        return {
            "metadata": {"target_schema": "ANALYTICS.SAS_OUT"},
            "files": {
                "score_customers.sas": {"status": "complete", "tier": "2-SP", "output_file": "snowflake/score_customers.sql"},
                "build_region.sas": {"status": "complete", "tier": "1-SQL", "output_file": "snowflake/build_region.sql"},
                "big_model.sas": {"status": "complete", "tier": "3-PYSPARK", "output_file": "snowflake/big_model.py"},
            },
        }

    def test_attach_sets_converted_and_status(self):
        updated = self.emitter.attach_converted_from_state(self._state())
        names = {e["source"]["name"] for e in updated}
        self.assertEqual(names, {"score_customers", "build_region"})  # pyspark skipped
        by_name = {e["source"]["name"]: e for e in updated}
        proc = by_name["score_customers"]
        self.assertEqual(proc["target"]["objectType"], "procedure")
        self.assertEqual(proc["files"]["converted"]["path"], "snowflake/score_customers.sql")
        self.assertTrue(proc["files"]["converted"]["checksum"])
        self.assertEqual(proc["codeStatus"]["conversion"]["status"], "completed")
        self.assertEqual(by_name["build_region"]["target"]["objectType"], "table")

    def test_pyspark_left_source_only(self):
        self.emitter.attach_converted_from_state(self._state())
        entry = json.loads((self.emitter.registry_dir / f"{unit_id('big_model')}.json").read_text())
        self.assertNotIn("converted", entry["files"])
        self.assertNotIn("conversion", entry["codeStatus"])

    def test_incomplete_skipped(self):
        state = self._state()
        state["files"]["score_customers.sas"]["status"] = "converted"  # not complete
        updated = self.emitter.attach_converted_from_state(state)
        self.assertNotIn("score_customers", {e["source"]["name"] for e in updated})


if __name__ == "__main__":
    unittest.main()
