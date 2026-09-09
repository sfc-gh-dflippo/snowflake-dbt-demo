"""Reproducible multi-platform identify/emit runs over shipped fixtures.

Usage: python3 runall.py <outdir>

Optional env:
  AIFIRST_FIXTURES      override fixtures root (default: ai/tests/etl-aifirst/fixtures)
  AIFIRST_ENGINE_TESTS  optional TestAssemblies root for Informatica/DataStage engine fixtures
"""

from __future__ import annotations

import io
import json
import os
import sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

# Allow importing identify/emit from sibling scripts/
_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import fit
from emit import Emitter
from identify import Identification, load_table
from fixture_paths import engine_tests_root, fixtures_root

FX = fixtures_root()
ENG = engine_tests_root()
PLATFORMS = Path(__file__).resolve().parent.parent / "platforms"


def _plat(name: str) -> str:
    return str(PLATFORMS / name)


def _runs() -> list[tuple[str, str, str]]:
    runs: list[tuple[str, str, str]] = []
    if ENG is not None:
        inf = ENG / "TestsSourceCode/SourceCode/EtlToDbt/Informatica/Expression/MappingForTest.XML"
        ds = ENG / "Parsers/TestAssemblies/DataStage/DsxParser.Tests/Assets/MaskDemo.dsx"
        # Also accept layout used by some worktrees
        if not ds.is_file():
            ds = ENG / "DataStage/DsxParser.Tests/Assets/MaskDemo.dsx"
        if inf.is_file():
            runs.append(("inf", _plat("platform_informatica.json"), str(inf)))
        if ds.is_file():
            runs.append(("ds", _plat("platform_datastage.json"), str(ds)))

    runs.extend(
        [
            ("ssis", _plat("platform_ssis.json"), str(FX / "inputs/input/DerivedColumn.dtsx")),
            # ORDER IS LOAD-BEARING — see historical note in orch runall.py (ktr-a/ktr-b DataRows).
            (
                "ktr-a",
                _plat("platform_pentaho.json"),
                str(FX / "inputs/inputs/pentaho/safe-stop-gen-rows.ktr"),
            ),
            (
                "ktr-b",
                _plat("platform_pentaho.json"),
                str(FX / "inputs/inputs/pentaho/sample_trans.ktr"),
            ),
            ("adf-a", _plat("platform_adf.json"), str(FX / "inputs/inputs/adf/myPipeline.json")),
            ("adf-b", _plat("platform_adf.json"), str(FX / "inputs/inputs/adf/adf_First_Pipeline.json")),
        ]
    )
    return runs


RUNS = _runs()


def one(table_path, doc_path):
    table = load_table(table_path)
    idn = Identification(table, doc_path)
    em = Emitter(idn)
    ir = em.emit()
    buf = io.StringIO()
    with redirect_stdout(buf):
        fit.report(idn, em, ir)
    return ir, buf.getvalue()


def main():
    if len(sys.argv) != 2:
        print("usage: python3 runall.py <outdir>", file=sys.stderr)
        sys.exit(2)
    outdir = Path(sys.argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    names = Counter()
    for slug, table, doc in RUNS:
        if not Path(doc).is_file():
            print(f"SKIP {slug}: missing {doc}")
            continue
        ir, report = one(table, doc)
        (outdir / f"{slug}-ir.json").write_text(json.dumps(ir, indent=2), encoding="utf-8")
        (outdir / f"{slug}-report.txt").write_text(report, encoding="utf-8")
        for n in ir.get("nodes", []):
            mn = n.get("modelName")
            if mn:
                names[mn] += 1
        print(f"{slug}: wrote IR + report")
    print("modelName census:", dict(names))


if __name__ == "__main__":
    main()
