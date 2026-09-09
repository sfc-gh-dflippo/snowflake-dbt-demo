#!/usr/bin/env python3
"""Post-process generated test YAMLs to add modifies_data and affected_tables.

Combines two sources:
  1. Regex extraction of tables from INSERT/UPDATE/DELETE/MERGE in YAML steps
  2. Transitive table dependencies from CUR, supplied by the caller via
     ``--extra-tables`` (the agent obtains these from the ``query_registry``
     MCP tool with ``include_dependencies=true``).

TODO(SNOW-3443831): this script is a stopgap until ``scai test baseline``
populates ``modifies_data`` / ``affected_tables`` directly. Remove once
that lands.

Usage:
  python enrich_yamls.py <project_root> <object_name> [--extra-tables FQN[,FQN...]]

Example:
  python enrich_yamls.py /path/to/dutchie "dbo.GetFF(INT,INT,VARCHAR)" \
    --extra-tables "dbo.Customers,dbo.Orders"
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

_DML_RE = re.compile(
    r"\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM|MERGE\s+INTO)\s+"
    r"(?:\[?(\w+)\]?\.)?(\[?\w+\]?)",
    re.IGNORECASE,
)


def _tables_from_steps(steps: list[dict]) -> list[str]:
    """Extract table names from DML statements in source/target query steps."""
    tables: list[str] = []
    seen: set[str] = set()
    for step in steps:
        for key in ("source_query", "target_query"):
            sql = step.get(key, "") or ""
            for m in _DML_RE.finditer(sql):
                schema, table = m.group(1), m.group(2)
                table = table.strip("[]")
                fqn = f"{schema}.{table}" if schema else table
                upper = fqn.upper()
                if upper not in seen:
                    seen.add(upper)
                    tables.append(fqn)
    return tables


def _parse_extra_tables(raw: str | None) -> list[str]:
    """Parse a comma-separated FQN list from --extra-tables, dropping blanks."""
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def enrich(
    project_root: Path,
    object_name: str,
    extra_tables: list[str] | None = None,
) -> int:
    """Find and enrich all test YAMLs for the given object. Returns count."""
    artifacts = project_root / "artifacts"
    if not artifacts.exists():
        print(f"No artifacts directory at {artifacts}", file=sys.stderr)
        return 0

    yaml_files = sorted(artifacts.rglob("*/test/*.yml"))
    if object_name:
        yaml_files = [f for f in yaml_files if object_name in str(f)]

    extra = list(extra_tables or [])
    count = 0

    for yml_path in yaml_files:
        with open(yml_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

        validation = data.get("validation", {})
        steps = validation.get("steps", [])
        if not steps:
            continue

        step_tables = _tables_from_steps(steps)

        seen: set[str] = set()
        affected: list[str] = []
        for t in step_tables + extra:
            upper = t.upper()
            if upper not in seen:
                seen.add(upper)
                affected.append(t)

        validation["modifies_data"] = bool(affected)
        validation["affected_tables"] = affected
        data["validation"] = validation

        with open(yml_path, "w", encoding="utf-8") as fh:
            yaml.dump(data, fh, default_flow_style=False, sort_keys=False)

        count += 1
        print(f"  enriched: {yml_path.name} (tables: {affected})")

    return count


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("object_name")
    parser.add_argument(
        "--extra-tables",
        default="",
        help=(
            "Comma-separated FQNs of additional write-dependency tables "
            "(typically obtained by the agent via the query_registry MCP tool "
            "with include_dependencies=true)."
        ),
    )
    args = parser.parse_args()

    extras = _parse_extra_tables(args.extra_tables)
    n = enrich(args.project_root, args.object_name, extras)
    print(f"\nEnriched {n} YAML file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
