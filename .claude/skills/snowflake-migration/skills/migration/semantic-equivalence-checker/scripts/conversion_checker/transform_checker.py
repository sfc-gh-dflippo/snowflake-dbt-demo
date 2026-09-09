"""Stage 2: Deterministic transformation logic comparison using sqlglot ASTs."""

from __future__ import annotations

import sqlglot
import sqlparse
from sqlglot import exp

from .models import ColumnTransform, TransformCheck, Join, JoinClause

# Audit columns excluded from transform comparison
_AUDIT_PREFIXES = ("EDW_", "EDWSF_")
_AUDIT_COLUMNS = {
    "EDW_CREATE_DTM", "EDW_CREATE_USER", "EDW_UPDATE_DTM", "EDW_UPDATE_USER",
    "EDWSF_CREATE_DTM", "EDWSF_CREATE_USER", "EDWSF_UPDATE_DTM", "EDWSF_UPDATE_USER",
    "EDWSF_BATCH_ID", "EDWSF_SOURCE_DELETED_FLAG",
    "CURRENT_TIMESTAMP(0)", "CURRENT_TIMESTAMP", "USER", "CURRENT_USER",
    "SYSDATE", "CURRENT_DATE",
}

# TD→SF function equivalences for normalization
_FUNC_MAP = {
    "USER": "CURRENT_USER",
    "DATE": "CURRENT_DATE",
    "TIME": "CURRENT_TIME",
}

# INFA join type → SQL join type
_JOIN_TYPE_MAP = {
    "NORMAL": "INNER",
    "MASTER OUTER": "LEFT",
    "DETAIL OUTER": "RIGHT",
    "FULL OUTER": "FULL",
}


def _is_audit_column(name: str) -> bool:
    upper = name.upper()
    return upper in _AUDIT_COLUMNS or any(upper.startswith(p) for p in _AUDIT_PREFIXES)


def extract_column_expressions(sql: str, dialect: str = "teradata") -> dict[str, str]:
    """Parse SQL and extract {ALIAS: expression_string} for each SELECT column.

    For UNION ALL, uses the first SELECT branch.
    Returns uppercase alias keys.
    """
    try:
        parsed = sqlglot.parse(sql, read=dialect)
    except (sqlglot.errors.ParseError, sqlglot.errors.TokenError):
        # Strip comments (including malformed nested /* */) and retry
        try:
            cleaned = sqlparse.format(sql, strip_comments=True)
            parsed = sqlglot.parse(cleaned, read=dialect)
        except (sqlglot.errors.ParseError, sqlglot.errors.TokenError):
            try:
                parsed = sqlglot.parse(cleaned)
            except Exception:
                return {}

    if not parsed:
        return {}

    stmt = parsed[0]

    # Handle UNION ALL — get first SELECT branch
    if isinstance(stmt, exp.Union):
        stmt = stmt.this  # first branch

    if not isinstance(stmt, exp.Select):
        return {}

    columns: dict[str, str] = {}
    for expr_node in stmt.expressions:
        alias_node = expr_node.args.get("alias")
        if alias_node:
            alias = alias_node.this.upper() if hasattr(alias_node.this, "upper") else str(alias_node.this).upper()
            # The expression is everything except the alias
            inner = expr_node.this if hasattr(expr_node, "this") else expr_node
            columns[alias] = inner.sql(dialect="teradata").upper()
        elif isinstance(expr_node, exp.Column):
            col_name = expr_node.name.upper()
            columns[col_name] = expr_node.sql(dialect="teradata").upper()
        else:
            # Anonymous expression without alias — use sql repr as key
            sql_repr = expr_node.sql(dialect="teradata").upper()
            columns[sql_repr] = sql_repr

    return columns


def normalize_expr_str(expr_str: str) -> str:
    """Normalize an expression string for comparison.

    - Uppercase
    - Strip table qualifiers (T.COL → COL)
    - Map TD functions to SF equivalents
    """
    upper = expr_str.strip().upper()

    # Parse with sqlglot for AST-level normalization
    try:
        parsed = sqlglot.parse_one(upper, read="teradata")
    except (sqlglot.errors.ParseError, Exception):
        # Can't parse — fall back to string comparison
        return upper

    # Unwrap CAST(literal AS type) → literal for comparison
    if isinstance(parsed, exp.Cast) and isinstance(parsed.this, exp.Literal):
        parsed = parsed.this

    # Strip table qualifiers from all column references
    for col in parsed.find_all(exp.Column):
        if col.table:
            col.set("table", None)

    # Map function names
    for func in parsed.find_all(exp.Func):
        func_name = type(func).__name__.upper()
        # Handle Anonymous functions (user-defined or unmapped)
        if isinstance(func, exp.Anonymous):
            name = func.this.upper() if isinstance(func.this, str) else str(func.this).upper()
            if name in _FUNC_MAP:
                func.set("this", _FUNC_MAP[name])
        else:
            # For known function nodes, check if they map
            sql_name = func.sql_name().upper() if hasattr(func, "sql_name") else ""
            if sql_name in _FUNC_MAP:
                # Replace with mapped version — create Anonymous node
                pass  # sqlglot typed nodes are harder to swap; rely on string match

    # Handle USER → CURRENT_USER equivalence at string level
    result = parsed.sql(dialect="teradata").upper()

    # Handle bare USER → CURRENT_USER() (TD allows without parens)
    if result.strip() == "USER":
        result = "CURRENT_USER()"

    # Normalize CURRENT_USER without parens to CURRENT_USER()
    if result.strip() == "CURRENT_USER":
        result = "CURRENT_USER()"

    return result


def compare_column_expressions(
    infa_cols: dict[str, str],
    dbt_cols: dict[str, str],
) -> TransformCheck:
    """Compare INFA and DBT column expressions by target column name.

    Filters out audit columns before comparison.
    """
    # Filter audit columns
    infa_filtered = {k: v for k, v in infa_cols.items() if not _is_audit_column(k)}
    dbt_filtered = {k: v for k, v in dbt_cols.items() if not _is_audit_column(k)}

    matches = 0
    differences = 0
    missing = 0
    columns: list[ColumnTransform] = []

    for col_name, infa_expr in infa_filtered.items():
        if col_name not in dbt_filtered:
            missing += 1
            columns.append(ColumnTransform(
                column=col_name,
                status="MISSING_IN_DBT",
                infa_expr=infa_expr,
                dbt_expr="",
            ))
            continue

        dbt_expr = dbt_filtered[col_name]
        infa_norm = normalize_expr_str(infa_expr)
        dbt_norm = normalize_expr_str(dbt_expr)

        if infa_norm == dbt_norm:
            matches += 1
            columns.append(ColumnTransform(
                column=col_name,
                status="MATCH",
                infa_expr=infa_expr,
                dbt_expr=dbt_expr,
            ))
        else:
            differences += 1
            columns.append(ColumnTransform(
                column=col_name,
                status="DIFFERENT",
                infa_expr=infa_expr,
                dbt_expr=dbt_expr,
            ))

    # Check for extra columns in DBT
    for col_name in dbt_filtered:
        if col_name not in infa_filtered:
            columns.append(ColumnTransform(
                column=col_name,
                status="MISSING_IN_INFA",
                infa_expr="",
                dbt_expr=dbt_filtered[col_name],
            ))

    if differences == 0 and missing == 0:
        status = "PASS"
    elif matches > 0:
        status = "PARTIAL"
    else:
        status = "FAIL"

    return TransformCheck(
        status=status,
        matches=matches,
        differences=differences,
        missing=missing,
        columns=columns,
    )


def compare_joins(infa_joins: list[Join], dbt_joins: list[JoinClause]) -> dict:
    """Compare INFA Joiner transforms against DBT JOIN clauses."""
    infa_count = len(infa_joins)
    dbt_count = len(dbt_joins)

    if infa_count != dbt_count:
        return {
            "status": "FAIL",
            "infa_count": infa_count,
            "dbt_count": dbt_count,
            "detail": f"Join count mismatch: INFA has {infa_count}, DBT has {dbt_count}",
        }

    # Compare join types (order-independent would be ideal but keep simple for now)
    for i, (infa_j, dbt_j) in enumerate(zip(infa_joins, dbt_joins)):
        infa_type = _JOIN_TYPE_MAP.get(infa_j.join_type.upper(), infa_j.join_type.upper())
        dbt_type = dbt_j.join_type.upper()
        if infa_type != dbt_type:
            return {
                "status": "FAIL",
                "detail": f"Join {i+1} type mismatch: INFA={infa_j.join_type}→{infa_type}, DBT={dbt_type}",
                "infa_count": infa_count,
                "dbt_count": dbt_count,
            }

    return {"status": "PASS", "infa_count": infa_count, "dbt_count": dbt_count}


def compare_filters(infa_filters: list[str], dbt_wheres: list[str]) -> dict:
    """Compare INFA filter conditions against DBT WHERE clauses."""
    if not infa_filters and not dbt_wheres:
        return {"status": "PASS", "detail": "No filters on either side"}

    if len(infa_filters) != len(dbt_wheres):
        return {
            "status": "FAIL",
            "infa_count": len(infa_filters),
            "dbt_count": len(dbt_wheres),
            "detail": f"Filter count mismatch: INFA={len(infa_filters)}, DBT={len(dbt_wheres)}",
        }

    # Normalize and compare each filter
    for i, (infa_f, dbt_f) in enumerate(zip(infa_filters, dbt_wheres)):
        infa_norm = normalize_expr_str(infa_f)
        dbt_norm = normalize_expr_str(dbt_f)
        if infa_norm != dbt_norm:
            return {
                "status": "FAIL",
                "detail": f"Filter {i+1} differs: INFA='{infa_f}' vs DBT='{dbt_f}'",
            }

    return {"status": "PASS"}


# ──────────────────────────────────────────────────────────────
# Hook SQL comparison (Pre/Post SQL content)
# ──────────────────────────────────────────────────────────────

import re as _re

# Statements that are TD-only housekeeping (no SF equivalent)
_TD_ONLY_PATTERNS = _re.compile(
    r"^\s*(COLLECT\s+STAT|CALL\s+COLLECT_STATS)",
    _re.IGNORECASE,
)

# SF-only housekeeping (no TD equivalent) — matches schema-qualified procs too
# Also matches OOD patterns: INSERT INTO X SELECT * FROM {{this}}, DROP TABLE {{this}}
# The named procedures are real routines from the source estates this checker was
# built against; they stay because that is what the pattern has to match.
_SF_ONLY_PATTERNS = _re.compile(
    r"(RUN_CREV_AUDITS|COLLECT_STATS_WRAP"
    r"|INSERT\s+INTO\s+\S+\s+SELECT\s+\*\s+FROM\s+\{\{this\}\}"
    r"|DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?\{\{this\}\})",
    _re.IGNORECASE,
)


def classify_statement(sql: str) -> str:
    """Classify a SQL statement by type. Uses sqlglot AST first, regex fallback."""
    stripped = sql.strip()
    if not stripped:
        return "OTHER"

    # Try sqlglot classification first
    try:
        parsed = sqlglot.parse_one(stripped)
        type_map = {
            "Insert": "INSERT",
            "Update": "UPDATE",
            "Delete": "DELETE",
            "Merge": "MERGE",
            "Select": "SELECT",
            "Create": "CREATE",
            "Drop": "DROP",
            "Command": "CALL",
        }
        cls_name = type(parsed).__name__
        if cls_name in type_map:
            return type_map[cls_name]
    except Exception:
        pass

    # Regex fallback for unparseable statements
    upper = stripped.upper()
    if upper.startswith("DELETE"):
        return "DELETE"
    if upper.startswith("TRUNCATE"):
        return "TRUNCATE"
    if upper.startswith("INSERT"):
        return "INSERT"
    if upper.startswith("UPDATE"):
        return "UPDATE"
    if upper.startswith("MERGE"):
        return "MERGE"
    if _re.search(r"^COLLECT\s+STAT", upper):
        return "COLLECT_STATS"
    if upper.startswith("CALL") or upper.startswith("EXECUTE") or upper.startswith("EXEC "):
        return "CALL"
    if upper.startswith("SELECT") or upper.startswith("SEL "):
        return "SELECT"
    if upper.startswith("CREATE"):
        return "CREATE"
    return "OTHER"


def _normalize_hook_sql(sql: str) -> str:
    """Normalize a hook SQL statement for comparison: strip comments, DB prefixes, uppercase, collapse whitespace."""
    # Strip all SQL comments (--,  /* */, including malformed nested ones)
    normalized = sqlparse.format(sql, strip_comments=True).strip().upper()
    # Strip $$ variable prefixes ($$STGDB., $$FINLGLDB., etc.)
    normalized = _re.sub(r"\$\$\w+\.", "", normalized)
    # Strip Jinja var() database refs (case-insensitive since text is uppercased)
    normalized = _re.sub(r"\{\{\s*var\([^)]+\)\s*\}\}\.\w+\.", "", normalized, flags=_re.IGNORECASE)
    # Collapse whitespace
    normalized = _re.sub(r"\s+", " ", normalized).strip()
    # Remove trailing ALL from DELETE (TD syntax: DELETE FROM x ALL)
    normalized = _re.sub(r"\bALL\s*$", "", normalized).strip()
    return normalized


def _extract_where_from_delete(sql: str) -> str:
    """Extract WHERE clause from a DELETE statement."""
    match = _re.search(r"\bWHERE\b\s+(.+)", sql, _re.IGNORECASE | _re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_select_from_insert(sql: str) -> str:
    """Extract the SELECT body from an INSERT...SELECT statement."""
    match = _re.search(
        r"\bSELECT\b\s+(.+)",
        sql,
        _re.IGNORECASE | _re.DOTALL,
    )
    return match.group(0).strip() if match else ""


def _parse_update_ast(sql: str, dialect: str) -> dict | None:
    """Parse an UPDATE statement and extract target, SET columns, WHERE clause.

    Handles both Teradata and Snowflake UPDATE syntax via sqlglot AST.
    Returns dict with keys: target, set_columns (dict col→expr), where_expr, or None on failure.
    """
    normalized = _normalize_hook_sql(sql)
    # Strip remaining Jinja {{ this }} / {{ var(...) }} placeholders for parsing
    normalized = _re.sub(r"\{\{[^}]*\}\}", "TGT_TABLE", normalized)
    try:
        parsed = sqlglot.parse_one(normalized, read=dialect)
    except (sqlglot.errors.ParseError, sqlglot.errors.TokenError):
        try:
            parsed = sqlglot.parse_one(normalized)
        except Exception:
            return None

    if not isinstance(parsed, exp.Update):
        return None

    # Extract target table name
    table_node = parsed.find(exp.Table)
    target = table_node.name.upper() if table_node else ""

    # Extract SET assignments: {COLUMN_NAME: expression_string}
    set_columns: dict[str, str] = {}
    set_exprs = parsed.args.get("expressions") or []
    for item in set_exprs:
        if isinstance(item, exp.EQ):
            left = item.this
            right = item.expression
            if isinstance(left, exp.Column):
                col_name = left.name.upper()
                if not _is_audit_column(col_name):
                    set_columns[col_name] = normalize_expr_str(right.sql(dialect=dialect))

    # Extract WHERE clause
    where_node = parsed.find(exp.Where)
    where_expr = normalize_expr_str(where_node.this.sql(dialect=dialect)) if where_node else ""

    return {"target": target, "set_columns": set_columns, "where_expr": where_expr}


def _compare_update_statements(infa_sql: str, dbt_sql: str) -> dict:
    """Compare INFA (Teradata) and DBT (Snowflake) UPDATE statements.

    Returns dict with 'status' (MATCH/DIFFERENT/UNRESOLVED) and optional 'detail'.
    """
    infa_parsed = _parse_update_ast(infa_sql, "teradata")
    dbt_parsed = _parse_update_ast(dbt_sql, "snowflake")

    if not infa_parsed or not dbt_parsed:
        side = "both" if not infa_parsed and not dbt_parsed else ("INFA" if not infa_parsed else "DBT")
        return {"status": "UNRESOLVED", "detail": f"Could not parse UPDATE on {side} side"}

    if not infa_parsed["set_columns"] and not dbt_parsed["set_columns"]:
        return {"status": "UNRESOLVED", "detail": "Could not extract SET columns from either side"}

    # Compare SET columns (ignoring audit columns)
    infa_cols = infa_parsed["set_columns"]
    dbt_cols = dbt_parsed["set_columns"]

    missing_in_dbt = set(infa_cols.keys()) - set(dbt_cols.keys())
    missing_in_infa = set(dbt_cols.keys()) - set(infa_cols.keys())
    common = set(infa_cols.keys()) & set(dbt_cols.keys())

    if missing_in_dbt or missing_in_infa:
        detail = []
        if missing_in_dbt:
            detail.append(f"Columns in INFA but not DBT: {sorted(missing_in_dbt)}")
        if missing_in_infa:
            detail.append(f"Columns in DBT but not INFA: {sorted(missing_in_infa)}")
        return {"status": "DIFFERENT", "detail": "; ".join(detail)}

    # Compare expressions for common columns
    diff_cols = []
    for col in sorted(common):
        if infa_cols[col] != dbt_cols[col]:
            diff_cols.append(col)

    if diff_cols:
        return {"status": "DIFFERENT", "detail": f"SET expression differs for: {diff_cols}"}

    # Compare WHERE clauses
    if infa_parsed["where_expr"] and dbt_parsed["where_expr"]:
        if infa_parsed["where_expr"] != dbt_parsed["where_expr"]:
            return {"status": "DIFFERENT", "detail": "WHERE clause differs"}

    return {"status": "MATCH"}


def compare_hook_statements(
    infa_stmts: list[str],
    dbt_stmts: list[str],
) -> tuple[bool, list[dict], list[dict]]:
    """Compare pre/post hook SQL statements content.

    Returns:
        (equivalent, matched_pairs, unresolved)
        - equivalent: True if all significant statements match
        - matched_pairs: list of {infa_sql, dbt_sql, status, stmt_type}
        - unresolved: list of {section, reason, infa_sql, dbt_sql} for LLM
    """
    # Filter out TD-only and SF-only housekeeping
    # Strip Jinja before classifying so {{ref(...)}} UPDATE... classifies correctly
    def _classify_stripped(sql: str) -> str:
        stripped = _re.sub(r"\{\{[^}]*\}\}", "", sql).strip()
        return classify_statement(stripped) if stripped else classify_statement(sql)

    infa_significant = [(s, _classify_stripped(s)) for s in infa_stmts
                        if not _TD_ONLY_PATTERNS.match(s.strip())]
    dbt_significant = [(s, _classify_stripped(s)) for s in dbt_stmts
                       if not _SF_ONLY_PATTERNS.search(s.strip())]

    matched_pairs: list[dict] = []
    unresolved: list[dict] = []

    # Match by statement type (DELETE↔DELETE/TRUNCATE, INSERT↔INSERT)
    infa_remaining = list(infa_significant)
    dbt_remaining = list(dbt_significant)

    # DELETE ↔ DELETE or TRUNCATE (TD "DELETE FROM x ALL" == SF "TRUNCATE TABLE x")
    for i, (infa_sql, infa_type) in enumerate(list(infa_remaining)):
        if infa_type not in ("DELETE", "TRUNCATE"):
            continue
        infa_norm = _normalize_hook_sql(infa_sql)
        # Check if it's a full-table delete (no WHERE) → matches TRUNCATE
        infa_where = _extract_where_from_delete(infa_norm)

        for j, (dbt_sql, dbt_type) in enumerate(list(dbt_remaining)):
            if dbt_type not in ("DELETE", "TRUNCATE"):
                continue
            dbt_norm = _normalize_hook_sql(dbt_sql)
            dbt_where = _extract_where_from_delete(dbt_norm)

            # Full delete (no WHERE) matches TRUNCATE
            if not infa_where and dbt_type == "TRUNCATE":
                matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                      "status": "MATCH", "stmt_type": "DELETE/TRUNCATE"})
                infa_remaining.remove((infa_sql, infa_type))
                dbt_remaining.remove((dbt_sql, dbt_type))
                break

            # Both have WHERE — compare the WHERE clauses
            if infa_where and dbt_where:
                infa_w_norm = normalize_expr_str(infa_where)
                dbt_w_norm = normalize_expr_str(dbt_where)
                if infa_w_norm == dbt_w_norm:
                    matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                          "status": "MATCH", "stmt_type": "DELETE"})
                else:
                    matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                          "status": "DIFFERENT", "stmt_type": "DELETE"})
                infa_remaining.remove((infa_sql, infa_type))
                dbt_remaining.remove((dbt_sql, dbt_type))
                break

    # INSERT ↔ INSERT
    for i, (infa_sql, infa_type) in enumerate(list(infa_remaining)):
        if infa_type != "INSERT":
            continue
        infa_select = _extract_select_from_insert(_normalize_hook_sql(infa_sql))

        for j, (dbt_sql, dbt_type) in enumerate(list(dbt_remaining)):
            if dbt_type != "INSERT":
                continue
            dbt_select = _extract_select_from_insert(_normalize_hook_sql(dbt_sql))

            # Try to parse and compare column expressions
            try:
                infa_cols = extract_column_expressions(infa_select, dialect="teradata")
                dbt_cols = extract_column_expressions(dbt_select, dialect="snowflake")

                if infa_cols and dbt_cols:
                    # Compare columns
                    all_match = True
                    for col_name, infa_expr in infa_cols.items():
                        if col_name in dbt_cols:
                            if normalize_expr_str(infa_expr) != normalize_expr_str(dbt_cols[col_name]):
                                all_match = False
                                break
                        else:
                            all_match = False
                            break

                    if all_match and len(infa_cols) == len(dbt_cols):
                        matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                              "status": "MATCH", "stmt_type": "INSERT"})
                        # Flag behavioral difference: DBT adds QUALIFY/ROW_NUMBER dedup
                        dbt_upper = dbt_sql.upper()
                        infa_upper = infa_sql.upper()
                        if ("QUALIFY" in dbt_upper or "ROW_NUMBER" in dbt_upper) and \
                           "QUALIFY" not in infa_upper and "ROW_NUMBER" not in infa_upper:
                            unresolved.append({"section": "pre_sql",
                                               "reason": "DBT adds QUALIFY/ROW_NUMBER dedup not present in INFA (behavioral difference for non-unique data)",
                                               "infa_sql": infa_sql, "dbt_sql": dbt_sql})
                    else:
                        # Could not fully resolve — mark as unresolved for LLM
                        unresolved.append({"section": "pre_sql",
                                           "reason": "INSERT SELECT columns differ",
                                           "infa_sql": infa_sql, "dbt_sql": dbt_sql})
                else:
                    # Parse failed on one side — unresolved
                    side = "INFA" if not infa_cols else "DBT"
                    unresolved.append({"section": "pre_sql",
                                       "reason": f"Could not parse INSERT SELECT body ({side} side)",
                                       "infa_sql": infa_sql, "dbt_sql": dbt_sql})
            except Exception as e:
                unresolved.append({"section": "pre_sql",
                                   "reason": f"Parse error comparing INSERT bodies: {type(e).__name__}: {str(e)[:100]}",
                                   "infa_sql": infa_sql, "dbt_sql": dbt_sql})

            infa_remaining.remove((infa_sql, infa_type))
            dbt_remaining.remove((dbt_sql, dbt_type))
            break

    # UPDATE ↔ UPDATE (TD: UPDATE alias FROM tbl alias, ... SET ... WHERE ...)
    #                   (SF: UPDATE tbl alias SET ... FROM ... WHERE ...)
    for i, (infa_sql, infa_type) in enumerate(list(infa_remaining)):
        if infa_type != "UPDATE":
            continue

        for j, (dbt_sql, dbt_type) in enumerate(list(dbt_remaining)):
            if dbt_type != "UPDATE":
                continue

            match_result = _compare_update_statements(infa_sql, dbt_sql)
            if match_result["status"] == "MATCH":
                matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                      "status": "MATCH", "stmt_type": "UPDATE"})
            elif match_result["status"] == "DIFFERENT":
                matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                      "status": "DIFFERENT", "stmt_type": "UPDATE",
                                      "detail": match_result.get("detail", "")})
            else:
                unresolved.append({"section": "pre_sql",
                                   "reason": match_result.get("detail", "Could not parse UPDATE"),
                                   "infa_sql": infa_sql, "dbt_sql": dbt_sql})
            infa_remaining.remove((infa_sql, infa_type))
            dbt_remaining.remove((dbt_sql, dbt_type))
            break

    # CREATE ↔ CREATE (TD: CREATE VOLATILE TABLE, SF: CREATE TEMPORARY TABLE)
    for i, (infa_sql, infa_type) in enumerate(list(infa_remaining)):
        if infa_type != "CREATE":
            continue
        for j, (dbt_sql, dbt_type) in enumerate(list(dbt_remaining)):
            if dbt_type != "CREATE":
                continue
            # Extract table names and compare
            infa_tbl = _re.search(r"CREATE\s+(?:VOLATILE|TEMPORARY|TEMP)?\s*TABLE\s+(\S+)",
                                  infa_sql, _re.IGNORECASE)
            dbt_tbl = _re.search(r"CREATE\s+(?:VOLATILE|TEMPORARY|TEMP)?\s*TABLE\s+(\S+)",
                                 dbt_sql, _re.IGNORECASE)
            if infa_tbl and dbt_tbl:
                infa_name = infa_tbl.group(1).split(".")[-1].upper()
                dbt_name = dbt_tbl.group(1).split(".")[-1].upper()
                status = "MATCH" if infa_name == dbt_name else "DIFFERENT"
                matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                      "status": status, "stmt_type": "CREATE"})
            else:
                matched_pairs.append({"infa_sql": infa_sql, "dbt_sql": dbt_sql,
                                      "status": "MATCH", "stmt_type": "CREATE"})
            infa_remaining.remove((infa_sql, infa_type))
            dbt_remaining.remove((dbt_sql, dbt_type))
            break

    # Any remaining unmatched significant statements → unresolved
    for infa_sql, infa_type in infa_remaining:
        unresolved.append({"section": "pre_sql",
                           "reason": f"No matching {infa_type} on DBT side",
                           "infa_sql": infa_sql, "dbt_sql": ""})
    for dbt_sql, dbt_type in dbt_remaining:
        unresolved.append({"section": "pre_sql",
                           "reason": f"No matching {dbt_type} on INFA side",
                           "infa_sql": "", "dbt_sql": dbt_sql})

    # Determine equivalence
    has_diff = any(p["status"] == "DIFFERENT" for p in matched_pairs)
    equivalent = not has_diff and not unresolved

    return equivalent, matched_pairs, unresolved
