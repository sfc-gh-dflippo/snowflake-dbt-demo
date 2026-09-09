#!/usr/bin/env python3
"""Emit `models/sources.yml` for an emitted dbt project.

WHY THIS EXISTS. Measured, not assumed: `dbt parse` on an emitted tree fails with exactly one
error --

    error: dbt1005: Source 'raw.CUSTOMER' not found in project. Searched for 'CUSTOMER'
      --> models/staging/stg_raw__read_customer.sql:12:4

-- and nothing else. The project config, the profiles, every other model and every `ref()`
parse clean. So the whole tree was one missing declaration away from parsing, and every
"emitted N models" figure this project has reported was measuring EMISSION, not runnability.
That distinction was invisible until a parser was actually run.

The engine's own output does emit `models/sources.yml`; the AI-first chain did not.

WHY IT SCANS THE MODELS RATHER THAN THE IR. The declaration has to agree with what the SQL
references, and the SQL is the ground truth for that -- some of it is engine-rendered, some
model-authored at tier 3, and a source name can enter from either. Deriving the list from the
IR instead would let the two disagree, which is the failure this whole project keeps finding:
two artifacts that each look right and do not match. Scanning the emitted `source()` calls
makes disagreement structurally impossible.

Deliberately NOT invented here: database and schema. dbt resolves an undeclared source schema
to the source's `name`, and asserting a database would state a destination the migration has
not chosen -- the same reasoning that keeps `dbo` out of a target's SchemaName.

Usage:  emit_sources_yml.py <project-root>
Exit:   0 wrote or nothing to do; 1 could not write
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# `{{ source('raw', 'CUSTOMER') }}` in either quote style, whitespace-tolerant.
SOURCE_CALL = re.compile(
    r"""\{\{\s*source\s*\(\s*(['"])(?P<src>[^'"]+)\1\s*,\s*(['"])(?P<tbl>[^'"]+)\3\s*\)\s*\}\}"""
)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: emit_sources_yml.py <project-root>", file=sys.stderr)
        return 1
    root = Path(argv[1])
    models = root / "models"
    if not models.is_dir():
        print(f"   sources.yml: no models/ under {root} — nothing to do")
        return 0

    found: dict[str, set[str]] = defaultdict(set)
    for sql in sorted(models.rglob("*.sql")):
        for m in SOURCE_CALL.finditer(sql.read_text(encoding="utf-8", errors="replace")):
            found[m.group("src")].add(m.group("tbl"))

    if not found:
        print("   sources.yml: no source() calls in any model — nothing to declare")
        return 0

    out = models / "sources.yml"
    if out.exists() and "SSC-AI-FIRST-GENERATED" not in out.read_text(encoding="utf-8"):
        # Never clobber a declaration the engine wrote. If the engine starts emitting one,
        # this stage must become a no-op rather than a silent overwrite.
        print(f"   sources.yml: {out.name} already exists and is not ours — left untouched")
        return 0

    lines = [
        "# SSC-AI-FIRST-GENERATED — declares the sources the emitted models actually reference.",
        "# Derived by scanning source() calls in models/, so it cannot disagree with the SQL.",
        "# database/schema are deliberately omitted: dbt defaults an undeclared source schema to",
        "# the source name, and naming a database here would assert a destination the migration",
        "# has not chosen.",
        "version: 2",
        "sources:",
    ]
    for src in sorted(found):
        lines.append(f"  - name: {src}")
        lines.append("    tables:")
        for tbl in sorted(found[src]):
            lines.append(f"      - name: {tbl}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = sum(len(v) for v in found.values())
    print(f"   sources.yml: declared {total} table(s) across {len(found)} source(s) -> "
          f"{out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
