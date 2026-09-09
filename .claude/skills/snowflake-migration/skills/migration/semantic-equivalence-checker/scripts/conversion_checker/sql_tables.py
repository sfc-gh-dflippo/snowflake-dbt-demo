"""Table extraction from SQL text.

Replaces the external ``infa_lineage.sql_tables`` dependency, which is not
available inside the plugin. Only ``extract_tables_from_sql`` was ever used by
the comparator; ``normalize_table_name`` was imported but never called.

The comparator feeds Informatica Source Qualifier / Lookup SQL Override text
here and consumes ``t[1]`` — the bare table name, uppercased — so it can be set
-compared against ``_normalize_name()`` output from the dbt side.
"""

from __future__ import annotations

import re

import sqlglot
from sqlglot import exp

# Informatica SQ Overrides are Teradata SQL on this engagement. Parsing with the
# Teradata dialect first avoids false negatives on vendor syntax (QUALIFY, SEL,
# etc.); the generic parse is a fallback for text Teradata mode rejects.
_DIALECTS: tuple[str | None, ...] = ("teradata", None)

# Fallback for SQL neither dialect can parse — Informatica overrides are often
# fragments or carry PowerCenter placeholders that are not valid SQL at all.
_FROM_JOIN_RE = re.compile(
    r"\b(?:FROM|JOIN)\s+((?:[A-Za-z_][\w$#]*\.){0,2}[A-Za-z_][\w$#]*)",
    re.IGNORECASE,
)


def _clean(part: str | None) -> str:
    return (part or "").strip().strip('"').strip("'").strip("[]").upper()


def _write_targets(tree: exp.Expression) -> set[str]:
    """Tables the statement writes to, so they are not reported as reads."""
    targets: set[str] = set()
    for node_type in (exp.Insert, exp.Update, exp.Delete, exp.Merge):
        for node in tree.find_all(node_type):
            target = node.this
            # INSERT INTO t (cols) wraps the table in a Schema node.
            if isinstance(target, exp.Schema):
                target = target.this
            if isinstance(target, exp.Table):
                targets.add(_clean(target.name))
    return targets


def _cte_names(tree: exp.Expression) -> set[str]:
    """CTE aliases are not physical tables and must not surface as sources."""
    return {_clean(cte.alias_or_name) for cte in tree.find_all(exp.CTE)}


def _parse(sql: str) -> exp.Expression | None:
    for dialect in _DIALECTS:
        try:
            statements = sqlglot.parse(sql, read=dialect)
        except Exception:
            continue
        parsed = [s for s in statements if s is not None]
        if parsed:
            # Wrap multi-statement text so one walk covers every statement.
            return parsed[0] if len(parsed) == 1 else exp.Semicolon(expressions=parsed)
    return None


def _extract_via_regex(sql: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw in _FROM_JOIN_RE.findall(sql):
        parts = [p for p in raw.split(".") if p]
        table = _clean(parts[-1])
        schema = _clean(parts[-2]) if len(parts) > 1 else ""
        if table and table not in seen:
            seen.add(table)
            found.append((schema, table))
    return found


def extract_tables_from_sql(sql: str | None) -> list[tuple[str, str]]:
    """Return ``(schema, TABLE)`` pairs for every table the SQL reads.

    Names are uppercased and unquoted. CTE aliases and write targets are
    excluded so only physical reads are reported. Order is first-appearance and
    duplicates are collapsed. Unparseable SQL degrades to a FROM/JOIN regex scan
    rather than returning nothing, because a missed source reads downstream as a
    conversion gap that is not real.
    """
    if not sql or not sql.strip():
        return []

    tree = _parse(sql)
    if tree is None:
        return _extract_via_regex(sql)

    excluded = _cte_names(tree) | _write_targets(tree)

    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for table in tree.find_all(exp.Table):
        name = _clean(table.name)
        if not name or name in excluded or name in seen:
            continue
        seen.add(name)
        # sqlglot puts the schema in `db` and the database/catalog in `catalog`.
        found.append((_clean(table.db) or _clean(table.catalog), name))

    # A statement that only writes (no reads) legitimately yields nothing; a
    # parse that found no Table nodes at all means the parse was useless.
    if not found and not excluded:
        return _extract_via_regex(sql)
    return found
