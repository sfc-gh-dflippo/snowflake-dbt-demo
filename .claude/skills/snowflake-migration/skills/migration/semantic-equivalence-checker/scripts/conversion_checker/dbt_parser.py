"""Parse DBT model SQL files into DbtModel dataclass.

Uses regex for Jinja extraction and sqlglot for SQL parsing.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import sqlglot
from sqlglot import exp

from .models import CTE, DbtModel, JoinClause

_log = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Jinja extraction (regex-based)
# ──────────────────────────────────────────────────────────────

_CONFIG_BLOCK_RE = re.compile(
    r"\{\{\s*config\s*\((.*?)\)\s*\}\}", re.DOTALL
)
_REF_RE = re.compile(r"\{\{\s*ref\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}")
_SOURCE_RE = re.compile(
    r"\{\{\s*source\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}"
)
# Matches {{ var('DB') }}.SCHEMA.TABLE_NAME (extracts TABLE_NAME)
_VAR_TABLE_RE = re.compile(
    r"\{\{\s*var\s*\([^)]+\)\s*\}\}\.\w+\.(\w+)"
)
_CONFIG_PARAM_RE = re.compile(
    r"""(\w+)\s*=\s*(?:'([^']*)'|"([^"]*)"|(\w+\([^)]*\))|(\w+))""",
    re.DOTALL,
)


def _parse_config(raw: str) -> dict[str, str]:
    """Parse the contents of a config() block into key-value pairs."""
    result: dict[str, str] = {}
    # Handle multi-line config with var() calls
    for m in _CONFIG_PARAM_RE.finditer(raw):
        key = m.group(1)
        val = m.group(2) or m.group(3) or m.group(4) or m.group(5) or ""
        result[key] = val
    return result


def _extract_hooks(config: dict[str, str], key: str) -> list[str]:
    """Extract pre_hook or post_hook SQL list from config dict."""
    raw = config.get(key, "")
    if not raw:
        return []
    statements = [s.strip() for s in raw.split(";") if s.strip()]
    return statements


def _extract_hooks_from_raw(raw_config: str, key: str) -> list[str]:
    """Extract pre_hook/post_hook from raw config text, handling list syntax.

    Handles: pre_hook=["sql1", "sql2"] with multi-line SQL strings.
    """
    # Find key=[...] pattern with bracket-depth matching
    pattern = re.compile(rf"\b{key}\s*=\s*\[", re.IGNORECASE)
    match = pattern.search(raw_config)
    if not match:
        return []

    # Find the matching close bracket
    start = match.end()
    depth = 1
    i = start
    while i < len(raw_config) and depth > 0:
        if raw_config[i] == "[":
            depth += 1
        elif raw_config[i] == "]":
            depth -= 1
        i += 1

    list_content = raw_config[start:i-1]

    # Extract string literals from the list (handling multi-line strings)
    hooks: list[str] = []
    in_string = False
    quote_char = ""
    current: list[str] = []

    j = 0
    while j < len(list_content):
        ch = list_content[j]
        if not in_string:
            if ch in ('"', "'"):
                in_string = True
                quote_char = ch
                current = []
            # Skip commas and whitespace between strings
        else:
            # Check for end of string
            if ch == quote_char:
                hooks.append("".join(current).strip())
                in_string = False
            else:
                current.append(ch)
        j += 1

    return [h for h in hooks if h]


def _extract_refs(sql: str) -> list[str]:
    """Extract all ref() model names."""
    return _REF_RE.findall(sql)


def _extract_sources(sql: str) -> list[tuple[str, str]]:
    """Extract all source() references as (source_name, table_name)."""
    return _SOURCE_RE.findall(sql)


def _extract_var_tables(sql: str) -> list[str]:
    """Extract table names from {{ var('DB') }}.SCHEMA.TABLE patterns."""
    return _VAR_TABLE_RE.findall(sql)


# ──────────────────────────────────────────────────────────────
# Jinja resolution (deterministic substitution)
# ──────────────────────────────────────────────────────────────

def resolve_jinja(
    sql: str,
    sources_lookup: dict[str, dict[str, str]] | None = None,
    vars_lookup: dict[str, str] | None = None,
) -> str:
    """Resolve Jinja source/var/ref calls in DBT SQL to concrete Snowflake identifiers.

    Args:
        sql: Raw DBT SQL with Jinja
        sources_lookup: {source_name: {table_name: "DB.SCHEMA.TABLE"}}
        vars_lookup: {var_name: "VALUE"}

    Returns:
        SQL with Jinja replaced by resolved FQNs. Unresolvable refs left as table name only.
    """
    result = sql
    sources_lookup = sources_lookup or {}
    vars_lookup = vars_lookup or {}

    # Resolve {{ source('X', 'Y') }} → DB.SCHEMA.Y
    def _replace_source(m):
        src_name, tbl_name = m.group(1), m.group(2)
        if src_name in sources_lookup and tbl_name in sources_lookup[src_name]:
            return sources_lookup[src_name][tbl_name]
        return tbl_name  # fallback to bare table name

    result = _SOURCE_RE.sub(_replace_source, result)

    # Resolve {{ var('X') }} → VALUE
    def _replace_var(m):
        var_name = m.group(1)
        return vars_lookup.get(var_name, var_name)

    result = re.compile(r"\{\{\s*var\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}").sub(_replace_var, result)

    # Resolve {{ ref('X') }} → X (just the model name, which IS the table name)
    result = _REF_RE.sub(r"\1", result)

    # Resolve {{ this }} → __THIS__ placeholder
    result = re.sub(r"\{\{\s*this\s*\}\}", "__THIS__", result)

    # Strip Jinja comments and block tags only
    result = re.sub(r"\{#.*?#\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{%.*?%\}", "", result, flags=re.DOTALL)

    return result


# ──────────────────────────────────────────────────────────────
# SQL parsing (sqlglot)
# ──────────────────────────────────────────────────────────────

def _strip_jinja(sql: str) -> str:
    """Replace Jinja expressions with SQL-parseable placeholders.

    Handles nested {{ }} inside config blocks (e.g., {{ config(pre_hook="{{ this }}") }})
    by counting brace depth instead of using non-greedy regex.
    """
    # Replace ref('X') with just X
    result = _REF_RE.sub(r"\1", sql)
    # Replace source('a', 'b') with b
    result = _SOURCE_RE.sub(r"\2", result)
    # Replace Jinja comments {# ... #}
    result = re.sub(r"\{#.*?#\}", "", result, flags=re.DOTALL)
    # Replace Jinja block tags {% ... %}
    result = re.sub(r"\{%.*?%\}", "", result, flags=re.DOTALL)
    # Replace {{ ... }} blocks by brace-depth matching
    result = _strip_brace_blocks(result)
    return result


def _strip_brace_blocks(text: str) -> str:
    """Replace {{ ... }} blocks with placeholder, respecting nesting."""
    output: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if i + 1 < n and text[i] == "{" and text[i + 1] == "{":
            # Start of Jinja block — find matching close by counting depth
            depth = 1
            j = i + 2
            while j < n and depth > 0:
                if j + 1 < n and text[j] == "{" and text[j + 1] == "{":
                    depth += 1
                    j += 2
                elif j + 1 < n and text[j] == "}" and text[j + 1] == "}":
                    depth -= 1
                    j += 2
                else:
                    j += 1
            output.append("'__JINJA__'")
            i = j
        else:
            output.append(text[i])
            i += 1
    return "".join(output)


def _parse_sql_structure(
    sql: str, dialect: str = "snowflake"
) -> tuple[list[str], list[JoinClause], list[str], list[CTE]]:
    """Parse SQL using sqlglot AST and extract columns, joins, where clauses, CTEs.

    Returns (columns, joins, where_clauses, ctes).
    Falls back to empty results on parse failure.
    """
    columns: list[str] = []
    joins: list[JoinClause] = []
    where_clauses: list[str] = []
    ctes: list[CTE] = []

    try:
        parsed = sqlglot.parse_one(sql, read=dialect)
    except (sqlglot.errors.ParseError, sqlglot.errors.TokenError):
        try:
            parsed = sqlglot.parse_one(sql)
        except Exception as e:
            _log.debug("sqlglot parse failed for SQL structure: %s", e)
            return columns, joins, where_clauses, ctes

    # Extract CTEs
    for cte_node in parsed.find_all(exp.CTE):
        cte_name = cte_node.alias or ""
        cte_sql = cte_node.this.sql(dialect=dialect) if cte_node.this else ""
        if cte_name:
            ctes.append(CTE(name=cte_name, sql=cte_sql))

    # Find the outermost SELECT (after CTEs)
    select_node = parsed.find(exp.Select)
    if select_node:
        # Extract columns
        for col_node in select_node.expressions:
            alias = col_node.alias
            if alias:
                columns.append(alias.upper())
            elif isinstance(col_node, exp.Column):
                columns.append(col_node.name.upper())
            else:
                # Use the generated SQL's last identifier as name
                col_sql = col_node.sql(dialect=dialect)
                parts = re.findall(r"\w+", col_sql)
                if parts:
                    columns.append(parts[-1].upper())

    # Extract JOINs
    for join_node in parsed.find_all(exp.Join):
        join_kind = join_node.args.get("kind", "") or ""
        join_side = join_node.args.get("side", "") or ""
        join_type = f"{join_side} {join_kind}".strip().upper() or "INNER"

        table_node = join_node.find(exp.Table)
        table_name = table_node.name if table_node else ""
        if table_node and table_node.args.get("db"):
            table_name = f"{table_node.args['db'].name}.{table_name}"

        on_node = join_node.args.get("on")
        condition = on_node.sql(dialect=dialect) if on_node else ""
        joins.append(JoinClause(join_type=join_type, table=table_name, condition=condition))

    # Extract WHERE
    where_node = parsed.find(exp.Where)
    if where_node:
        where_sql = where_node.this.sql(dialect=dialect)
        if where_sql:
            where_clauses.append(where_sql)

    return columns, joins, where_clauses, ctes


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────

def parse_dbt_model(
    sql_path: Path,
    sources_lookup: dict[str, dict[str, str]] | None = None,
    vars_lookup: dict[str, str] | None = None,
) -> DbtModel:
    """Parse a DBT model SQL file and return a DbtModel dataclass.

    If sources_lookup/vars_lookup are provided, Jinja is resolved to concrete
    Snowflake identifiers before parsing. Hooks and raw_sql will contain resolved SQL.
    """
    raw_sql = sql_path.read_text(encoding="utf-8")
    name = sql_path.stem

    # Resolve Jinja if lookups provided
    resolved_sql = resolve_jinja(raw_sql, sources_lookup, vars_lookup) if (sources_lookup or vars_lookup) else raw_sql

    # Extract config — use brace-depth matching for nested {{ }} inside config
    config: dict[str, str] = {}
    raw_config_text = ""
    config_start = re.search(r"\{\{\s*config\s*\(", raw_sql)
    if config_start:
        # Find the matching close by tracking parens depth (for the config() call)
        paren_depth = 1
        i = config_start.end()
        while i < len(raw_sql) and paren_depth > 0:
            if raw_sql[i] == "(":
                paren_depth += 1
            elif raw_sql[i] == ")":
                paren_depth -= 1
            i += 1
        raw_config_text = raw_sql[config_start.end():i-1]
        config = _parse_config(raw_config_text)

    materialization = config.get("materialized", "")
    incremental_strategy = config.get("incremental_strategy") or None
    pre_hooks = _extract_hooks(config, "pre_hook")
    post_hooks = _extract_hooks(config, "post_hook")
    # Fallback to raw parsing for list-style hooks
    if not pre_hooks and raw_config_text:
        pre_hooks = _extract_hooks_from_raw(raw_config_text, "pre_hook")
    if not post_hooks and raw_config_text:
        post_hooks = _extract_hooks_from_raw(raw_config_text, "post_hook")
    target_table = config.get("alias", name)

    # Resolve hooks if lookups provided
    if sources_lookup or vars_lookup:
        pre_hooks = [resolve_jinja(h, sources_lookup, vars_lookup) for h in pre_hooks]
        post_hooks = [resolve_jinja(h, sources_lookup, vars_lookup) for h in post_hooks]

    # Extract source references from body only (exclude config block hooks)
    if config_start:
        # Skip past the closing '}}' of the config block
        body_start = raw_sql.find("}}", i)
        body_sql = raw_sql[body_start + 2:] if body_start != -1 else raw_sql
    else:
        body_sql = raw_sql
    refs = _extract_refs(body_sql)
    sources = _extract_sources(body_sql)
    var_tables = _extract_var_tables(body_sql)
    source_tables = sorted(set(
        refs + [tbl for _, tbl in sources] + var_tables
    ))

    # Parse SQL structure using sqlglot AST (use resolved SQL for better parsing)
    clean_sql = _strip_jinja(resolved_sql)
    clean_sql = re.sub(r"'__JINJA__'", "", clean_sql, count=1).strip()

    columns, join_clauses, where_clauses, ctes = _parse_sql_structure(clean_sql)

    return DbtModel(
        name=name,
        file_path=str(sql_path),
        materialization=materialization,
        incremental_strategy=incremental_strategy,
        pre_hooks=pre_hooks,
        post_hooks=post_hooks,
        source_tables=source_tables,
        target_table=target_table,
        columns_selected=columns,
        where_clauses=where_clauses,
        join_clauses=join_clauses,
        ctes=ctes,
        raw_sql=resolved_sql,
    )
