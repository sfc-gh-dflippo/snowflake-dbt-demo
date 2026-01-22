"""
Snowflake SQL Syntax Rules for dbt models.

Checks for Snowflake-incompatible syntax from other databases:
- SQL Server: TOP, ISNULL, GETDATE, CONVERT, LEN, etc.
- Oracle: ROWNUM, CONNECT BY, SYSDATE, etc.
- Teradata: SEL (short SELECT), etc.
- MySQL: LIMIT offset syntax, backticks, IFNULL, etc.

Functions that ARE supported in Snowflake (not flagged):
- DATEADD, QUALIFY, DECODE, NVL, CHARINDEX

Also checks for dbt-specific patterns like ref() and source() usage.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# =============================================================================
# Result Class
# =============================================================================


@dataclass
class SnowflakeSyntaxResult:
    """Result of Snowflake syntax validation."""

    is_valid: bool = True
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)

    def add_error(self, pattern: str, suggestion: str, line: int | None = None) -> None:
        """Add an error."""
        self.is_valid = False
        self.errors.append(
            {
                "pattern": pattern,
                "suggestion": suggestion,
                "line": line,
            }
        )

    def add_warning(
        self, pattern: str, suggestion: str, line: int | None = None
    ) -> None:
        """Add a warning."""
        self.warnings.append(
            {
                "pattern": pattern,
                "suggestion": suggestion,
                "line": line,
            }
        )


# =============================================================================
# Pattern Definitions
# =============================================================================

# SQL Server incompatible patterns
SQL_SERVER_PATTERNS = [
    {
        "pattern": r"\bTOP\s+\d+\b",
        "name": "TOP N",
        "suggestion": "Use LIMIT instead: SELECT ... LIMIT N",
        "severity": "error",
    },
    {
        "pattern": r"\bISNULL\s*\(",
        "name": "ISNULL()",
        "suggestion": "Use COALESCE(column, default) instead of ISNULL()",
        "severity": "error",
    },
    {
        "pattern": r"\bGETDATE\s*\(\)",
        "name": "GETDATE()",
        "suggestion": "Use CURRENT_TIMESTAMP() instead of GETDATE()",
        "severity": "error",
    },
    {
        "pattern": r"\bSYSDATETIME\s*\(\)",
        "name": "SYSDATETIME()",
        "suggestion": "Use CURRENT_TIMESTAMP() instead of SYSDATETIME()",
        "severity": "error",
    },
    {
        "pattern": r"\bGETUTCDATE\s*\(\)",
        "name": "GETUTCDATE()",
        "suggestion": "Use CURRENT_TIMESTAMP() or CONVERT_TIMEZONE() instead",
        "severity": "error",
    },
    {
        "pattern": r"\bCONVERT\s*\(\s*\w+\s*,",
        "name": "CONVERT(type, value)",
        "suggestion": "Use CAST(value AS type) or TRY_CAST() instead",
        "severity": "error",
    },
    {
        "pattern": r"\bCHARINDEX\s*\(",
        "name": "CHARINDEX()",
        "suggestion": "Use POSITION(substring IN string) or CHARINDEX() (Snowflake supports it)",
        "severity": "warning",
    },
    {
        "pattern": r"\bLEN\s*\(",
        "name": "LEN()",
        "suggestion": "Use LENGTH() instead of LEN()",
        "severity": "error",
    },
    {
        "pattern": r"\bDATEPART\s*\(",
        "name": "DATEPART()",
        "suggestion": "Use DATE_PART() or EXTRACT() instead",
        "severity": "error",
    },
    {
        "pattern": r"\bDATENAME\s*\(",
        "name": "DATENAME()",
        "suggestion": "Use TO_CHAR() or DAYNAME()/MONTHNAME() instead",
        "severity": "error",
    },
    {
        "pattern": r"WITH\s*\(\s*NOLOCK\s*\)",
        "name": "WITH (NOLOCK)",
        "suggestion": "Remove NOLOCK hint - not applicable in Snowflake",
        "severity": "error",
    },
    {
        "pattern": r"\bIDENTITY\s*\(\s*\d+",
        "name": "IDENTITY(seed, increment)",
        "suggestion": "Use AUTOINCREMENT or CREATE SEQUENCE instead",
        "severity": "error",
    },
    {
        "pattern": r"@@\w+",
        "name": "@@variable",
        "suggestion": "Use Snowflake system functions or Jinja variables instead",
        "severity": "error",
    },
    {
        "pattern": r"\bSTUFF\s*\(",
        "name": "STUFF()",
        "suggestion": "Use INSERT() or string concatenation instead",
        "severity": "error",
    },
]

# Oracle incompatible patterns
# Note: DECODE and NVL are supported in Snowflake and not flagged
ORACLE_PATTERNS = [
    {
        "pattern": r"\bROWNUM\b",
        "name": "ROWNUM",
        "suggestion": "Use ROW_NUMBER() OVER() instead of ROWNUM",
        "severity": "error",
    },
    {
        "pattern": r"\bCONNECT\s+BY\b",
        "name": "CONNECT BY",
        "suggestion": "Use recursive CTE instead of CONNECT BY",
        "severity": "error",
    },
    {
        "pattern": r"\bSTART\s+WITH\b",
        "name": "START WITH",
        "suggestion": "Use recursive CTE instead of START WITH",
        "severity": "error",
    },
    {
        "pattern": r"\bLEVEL\b(?!\s*=)",
        "name": "LEVEL pseudo-column",
        "suggestion": "Use recursive CTE with explicit level column instead",
        "severity": "warning",
    },
    {
        "pattern": r"\bSYSDATE\b",
        "name": "SYSDATE",
        "suggestion": "Use CURRENT_DATE() or CURRENT_TIMESTAMP() instead",
        "severity": "error",
    },
    {
        "pattern": r"\bSYSTIMESTAMP\b",
        "name": "SYSTIMESTAMP",
        "suggestion": "Use CURRENT_TIMESTAMP() instead",
        "severity": "error",
    },
    {
        "pattern": r"\bTO_DATE\s*\([^,]+\)",
        "name": "TO_DATE without format",
        "suggestion": "Specify format explicitly: TO_DATE(string, format)",
        "severity": "warning",
    },
    {
        "pattern": r"\+\s*\d+(?!\.\d)",
        "name": "Date arithmetic with + N",
        "suggestion": "Use DATEADD(day, N, date) instead of date + N",
        "severity": "warning",
    },
]

# Teradata patterns
# Note: QUALIFY is supported in Snowflake and not flagged
TERADATA_PATTERNS = [
    {
        "pattern": r"\bSEL\b",
        "name": "SEL (short SELECT)",
        "suggestion": "Use full SELECT keyword instead of SEL",
        "severity": "error",
    },
    {
        "pattern": r"\bSAMPLE\s+\d+",
        "name": "SAMPLE N",
        "suggestion": "Use SAMPLE(N ROWS) or TABLESAMPLE() instead",
        "severity": "warning",
    },
]

# MySQL patterns
MYSQL_PATTERNS = [
    {
        "pattern": r"`\w+`",
        "name": "Backtick identifiers",
        "suggestion": "Use double quotes for identifiers instead of backticks",
        "severity": "error",
    },
    {
        "pattern": r"\bLIMIT\s+\d+\s*,\s*\d+",
        "name": "LIMIT offset, count",
        "suggestion": "Use LIMIT count OFFSET offset instead",
        "severity": "error",
    },
    {
        "pattern": r"\bIFNULL\s*\(",
        "name": "IFNULL()",
        "suggestion": "Use COALESCE() or NVL() instead of IFNULL()",
        "severity": "error",
    },
]


# =============================================================================
# Utility Functions
# =============================================================================


def strip_strings_and_comments(sql: str) -> str:
    """Remove string literals and comments to avoid false positives."""
    # Remove block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    # Remove single-line comments
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
    # Remove string literals
    sql = re.sub(r"'[^']*'", "''", sql)
    sql = re.sub(r'"[^"]*"', '""', sql)
    return sql


def find_line_number(content: str, position: int) -> int:
    """Find line number for a character position."""
    return content[:position].count("\n") + 1


def get_platform_patterns(platform: str) -> list[dict]:
    """Get patterns specific to a source platform."""
    platform_map = {
        "sqlserver": SQL_SERVER_PATTERNS,
        "sql_server": SQL_SERVER_PATTERNS,
        "mssql": SQL_SERVER_PATTERNS,
        "oracle": ORACLE_PATTERNS,
        "teradata": TERADATA_PATTERNS,
        "mysql": MYSQL_PATTERNS,
    }
    return platform_map.get(platform.lower(), [])


# =============================================================================
# Check Functions
# =============================================================================


def check_snowflake_syntax(sql: str) -> SnowflakeSyntaxResult:
    """
    Check SQL for Snowflake-incompatible syntax.

    Args:
        sql: The SQL content to analyze

    Returns:
        SnowflakeSyntaxResult with errors and warnings
    """
    result = SnowflakeSyntaxResult()

    # Clean SQL for pattern matching
    sql_clean = strip_strings_and_comments(sql)

    # Combine all patterns
    all_patterns = (
        SQL_SERVER_PATTERNS + ORACLE_PATTERNS + TERADATA_PATTERNS + MYSQL_PATTERNS
    )

    for check in all_patterns:
        pattern = check["pattern"]
        severity = check["severity"]

        if severity == "ok":
            continue  # Skip patterns that indicate correct usage

        matches = list(re.finditer(pattern, sql_clean, re.IGNORECASE))

        for match in matches:
            line = find_line_number(sql, match.start())

            if severity == "error":
                result.add_error(
                    pattern=check["name"],
                    suggestion=check["suggestion"],
                    line=line,
                )
            elif severity == "warning":
                result.add_warning(
                    pattern=check["name"],
                    suggestion=check["suggestion"],
                    line=line,
                )

    return result


def check_for_platform(sql: str, platform: str) -> SnowflakeSyntaxResult:
    """
    Check SQL for patterns from a specific platform.

    Args:
        sql: The SQL content to analyze
        platform: Source platform to check for (sqlserver, oracle, etc.)

    Returns:
        SnowflakeSyntaxResult focused on that platform
    """
    result = SnowflakeSyntaxResult()
    sql_clean = strip_strings_and_comments(sql)

    patterns = get_platform_patterns(platform)

    for check in patterns:
        if check["severity"] == "ok":
            continue

        matches = list(re.finditer(check["pattern"], sql_clean, re.IGNORECASE))

        for match in matches:
            line = find_line_number(sql, match.start())

            if check["severity"] == "error":
                result.add_error(
                    pattern=check["name"],
                    suggestion=check["suggestion"],
                    line=line,
                )
            else:
                result.add_warning(
                    pattern=check["name"],
                    suggestion=check["suggestion"],
                    line=line,
                )

    return result
