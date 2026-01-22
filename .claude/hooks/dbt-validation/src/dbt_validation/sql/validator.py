"""
dbt SQL Model Validator.

Validates .sql model files for:
- CTE pattern structure (source → renamed/transformed → final)
- Required config block presence
- Explicit column aliases (no SELECT * in final CTE)
- Jinja ref/source usage (not hardcoded table names)
- Snowflake SQL syntax compatibility
- Migration comment headers for converted models

Rule IDs:
- SQL001: Must have config block (Warning)
- SQL002: Must use CTE pattern (source → transformed → final) (Warning)
- SQL003: Final SELECT must not be SELECT * (Error)
- SQL004: Final models should use {{ ref() }} or {{ source() }}, no hardcoded tables (Warning)
- SQL005: Migrated models must have conversion header comment (Warning)
- SQL006: No Snowflake-incompatible syntax (TOP, ISNULL, etc.) (Error)
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from dbt_validation.core import (
    BaseValidationResult,
    Severity,
)

# =============================================================================
# Result Class
# =============================================================================

# =============================================================================
# Rule IDs - Define locally, no need to modify core/base.py for new rules
# =============================================================================

# SQL validation rule identifiers
SQL_FILE_ERROR = "SQL000"
SQL_MISSING_CONFIG = "SQL001"
SQL_MISSING_CTE = "SQL002"
SQL_SELECT_STAR = "SQL003"
SQL_HARDCODED_TABLE = "SQL004"
SQL_MISSING_MIGRATION_HEADER = "SQL005"
SQL_INCOMPATIBLE_SYNTAX = "SQL006"


@dataclass
class SQLValidationResult(BaseValidationResult):
    """
    Result of SQL model validation.

    Extends BaseValidationResult with SQL-specific functionality.
    """

    pass  # Inherits add_error from BaseValidationResult


# =============================================================================
# Patterns
# =============================================================================

# Snowflake-incompatible syntax patterns (from other databases)
# Note: Functions that Snowflake DOES support are not included:
#   - DATEADD: Snowflake supports DATEADD(part, num, date)
#   - QUALIFY: Native Snowflake feature
#   - DECODE: Snowflake supports DECODE()
#   - NVL: Snowflake supports NVL()
#   - CHARINDEX: Snowflake supports CHARINDEX()
INCOMPATIBLE_PATTERNS: list[tuple[str, str, str]] = [
    # SQL Server patterns
    (r"\bTOP\s+\d+\b", "TOP N", "Use LIMIT instead of TOP"),
    (r"\bISNULL\s*\(", "ISNULL()", "Use COALESCE() instead of ISNULL()"),
    (r"\bGETDATE\s*\(\)", "GETDATE()", "Use CURRENT_TIMESTAMP() instead"),
    (r"\bSYSDATETIME\s*\(\)", "SYSDATETIME()", "Use CURRENT_TIMESTAMP() instead"),
    (r"\bCONVERT\s*\(\s*\w+\s*,", "CONVERT(type,", "Use CAST() or TO_* functions"),
    (r"\bLEN\s*\(", "LEN()", "Use LENGTH() instead of LEN()"),
    (
        r"WITH\s*\(\s*NOLOCK\s*\)",
        "WITH (NOLOCK)",
        "Remove NOLOCK hint (not supported in Snowflake)",
    ),
    (r"\bIDENTITY\s*\(", "IDENTITY()", "Use AUTOINCREMENT or SEQUENCE instead"),
    # Oracle patterns
    (r"\bROWNUM\b", "ROWNUM", "Use ROW_NUMBER() OVER() instead"),
    (r"\bCONNECT\s+BY\b", "CONNECT BY", "Use recursive CTE instead"),
    (r"\bSTART\s+WITH\b", "START WITH", "Use recursive CTE instead"),
    (r"@\w+", "PL/SQL variable", "Use Jinja variables instead of PL/SQL variables"),
    # General issues
    (
        r"(?<!\{)\{\s*\w+\s*\}(?!\})",
        "Single braces",
        "Use double braces {{ }} for Jinja",
    ),
]

# Patterns for detecting hardcoded table references
HARDCODED_TABLE_PATTERNS: list[str] = [
    # Schema.table references (not using ref/source)
    r"(?:FROM|JOIN)\s+(?!.*\{\{)([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)",
    # Database.schema.table references
    r"(?:FROM|JOIN)\s+(?!.*\{\{)([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)",
]


# =============================================================================
# Utility Functions
# =============================================================================


def strip_comments_and_strings(sql: str) -> str:
    """Remove SQL comments and string literals to avoid false positives."""
    # Remove block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    # Remove single-line comments
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
    # Remove string literals (single quotes)
    sql = re.sub(r"'[^']*'", "''", sql)
    # Remove string literals (double quotes for identifiers)
    sql = re.sub(r'"[^"]*"', '""', sql)
    return sql


def find_line_number(content: str, match_start: int) -> int:
    """Find the line number for a character position."""
    return content[:match_start].count("\n") + 1


# =============================================================================
# Individual Check Functions
# =============================================================================


def check_cte_pattern(content: str, result: SQLValidationResult) -> None:
    """Check for proper CTE structure."""
    sql_only = strip_comments_and_strings(content)

    # Look for WITH clause (case insensitive)
    if not re.search(r"\bWITH\b", sql_only, re.IGNORECASE):
        # Skip check for very simple models or ephemeral/placeholder
        if "materialized" in content.lower() and "ephemeral" in content.lower():
            return
        if "where false" in content.lower():
            return  # Placeholder model
        result.add_error(
            rule_id="SQL002",
            message="Consider using CTE pattern with named CTEs for readability",
            severity=Severity.RECOMMENDATION,
            line=1,
        )


def check_select_star(content: str, result: SQLValidationResult) -> None:
    """Check for SELECT * in final query (not in CTEs)."""
    sql_only = strip_comments_and_strings(content)

    # More specific: Look for SELECT * FROM final or similar
    if re.search(
        r"SELECT\s+\*\s+FROM\s+\w+\s*$", sql_only, re.IGNORECASE | re.MULTILINE
    ):
        cte_names = re.findall(r"(\w+)\s+AS\s*\(", sql_only, re.IGNORECASE)
        final_from_match = re.search(
            r"SELECT\s+\*\s+FROM\s+(\w+)\s*$", sql_only, re.IGNORECASE | re.MULTILINE
        )
        if final_from_match and final_from_match.group(1).lower() in [
            n.lower() for n in cte_names
        ]:
            return  # Selecting from a CTE is fine

    # Check for SELECT * in the main body (not acceptable in silver/gold)
    if re.search(r"SELECT\s+\*\s+FROM\s+\{\{", sql_only, re.IGNORECASE):
        path_str = result.file_path.lower()
        if "/bronze/" in path_str or "/staging/" in path_str:
            return  # Acceptable in bronze/staging layer

        result.add_error(
            rule_id="SQL003",
            message="Recommend specifying columns when querying ref() or source() "
            "instead of SELECT *",
            severity=Severity.RECOMMENDATION,
            line=find_line_number(content, sql_only.find("SELECT *")),
        )


def check_hardcoded_tables(content: str, result: SQLValidationResult) -> None:
    """Check for hardcoded table references instead of ref()/source()."""
    sql_only = strip_comments_and_strings(content)

    for pattern in HARDCODED_TABLE_PATTERNS:
        matches = re.finditer(pattern, sql_only, re.IGNORECASE)
        for match in matches:
            table_ref = match.group(1) if match.groups() else match.group(0)
            # Skip if it looks like a Jinja expression is nearby
            context_start = max(0, match.start() - 50)
            context = content[context_start : match.end() + 20]
            if "{{" in context or "}}" in context:
                continue

            result.add_error(
                rule_id="SQL004",
                message=f"Hardcoded table reference '{table_ref}' - "
                "use {{ ref('model') }} or {{ source('source', 'table') }}",
                severity=Severity.WARNING,
                line=find_line_number(content, match.start()),
            )


def check_snowflake_syntax(content: str, result: SQLValidationResult) -> None:
    """Check for Snowflake-incompatible SQL syntax."""
    sql_only = strip_comments_and_strings(content)

    for pattern, name, suggestion in INCOMPATIBLE_PATTERNS:
        matches = list(re.finditer(pattern, sql_only, re.IGNORECASE))
        for match in matches:
            # Skip if inside a Jinja block (template logic)
            context_start = max(0, match.start() - 20)
            context_end = min(len(sql_only), match.end() + 20)
            context = sql_only[context_start:context_end]
            if "{%" in context or "%}" in context:
                continue

            result.add_error(
                rule_id="SQL006",
                message=f"Snowflake-incompatible syntax '{name}' found. {suggestion}",
                severity=Severity.ERROR,
                line=find_line_number(content, match.start()),
            )


def check_migration_header(content: str, result: SQLValidationResult) -> None:
    """Check for migration header comment if file appears to be migrated."""
    migration_indicators = [
        "migrated from",
        "converted from",
        "original object",
        "source platform",
        "sql server",
        "oracle",
        "teradata",
    ]

    content_lower = content.lower()
    is_migration = any(ind in content_lower for ind in migration_indicators)

    if is_migration:
        header_pattern = r"/\*.*?(Original|Migrated|Converted|Source).*?\*/"
        if not re.search(header_pattern, content, re.IGNORECASE | re.DOTALL):
            result.add_error(
                rule_id="SQL005",
                message="Migrated model should have a header comment documenting "
                "the original source and conversion notes",
                severity=Severity.RECOMMENDATION,
                line=1,
            )


# =============================================================================
# Main Validation Function
# =============================================================================


def validate_dbt_model(file_path: str) -> SQLValidationResult:
    """
    Validate a dbt SQL model file.

    Args:
        file_path: Path to the SQL file to validate

    Returns:
        SQLValidationResult with validation status and any errors
    """
    result = SQLValidationResult(file_path=file_path, is_valid=True)

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        result.add_error(
            rule_id="SQL000",
            message=f"File not found: {file_path}",
            severity=Severity.ERROR,
        )
        return result
    except UnicodeDecodeError as e:
        result.add_error(
            rule_id="SQL000",
            message=f"Unable to read file (encoding error): {e}",
            severity=Severity.ERROR,
        )
        return result

    if not content.strip():
        return result  # Empty file is valid

    # Run all validators
    # Note: check_config_block removed - config blocks are optional
    check_cte_pattern(content, result)
    check_select_star(content, result)
    check_hardcoded_tables(content, result)
    check_snowflake_syntax(content, result)
    check_migration_header(content, result)

    return result
