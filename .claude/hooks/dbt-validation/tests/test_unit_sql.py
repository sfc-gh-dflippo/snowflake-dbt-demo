"""
Unit tests for sql/ modules - cte_rules.py, naming_rules.py, syntax_rules.py, validator.py helpers.

Tests SQL analysis functions without file I/O.
"""

from __future__ import annotations

from dbt_validation.sql.cte_rules import (
    categorize_cte,
    check_cte_patterns,
    extract_cte_names,
)
from dbt_validation.sql.naming_rules import (
    check_naming_conventions,
    infer_layer_from_path,
)
from dbt_validation.sql.syntax_rules import (
    check_for_platform,
    check_snowflake_syntax,
)
from dbt_validation.sql.validator import (
    find_line_number,
    strip_comments_and_strings,
)

# =============================================================================
# CTE Rules Tests (cte_rules.py)
# =============================================================================


class TestExtractCTENames:
    """Tests for extract_cte_names function."""

    def test_simple_ctes(self) -> None:
        sql = "WITH source AS (SELECT 1), final AS (SELECT 2) SELECT * FROM final"
        names = extract_cte_names(sql)
        assert "source" in names
        assert "final" in names

    def test_no_ctes(self) -> None:
        sql = "SELECT * FROM table"
        assert extract_cte_names(sql) == []

    def test_filters_sql_keywords(self) -> None:
        sql = "WITH source AS (SELECT * FROM raw WHERE id > 0) SELECT * FROM source"
        names = extract_cte_names(sql)
        assert "SELECT" not in [n.upper() for n in names]
        assert "WHERE" not in [n.upper() for n in names]


class TestCategorizeCTE:
    """Tests for categorize_cte function."""

    def test_import_patterns(self) -> None:
        assert categorize_cte("source") == "import"
        assert categorize_cte("src_customers") == "import"
        assert categorize_cte("raw_orders") == "import"
        assert categorize_cte("stg_orders") == "import"

    def test_final_patterns(self) -> None:
        assert categorize_cte("final") == "final"
        assert categorize_cte("result") == "final"
        assert categorize_cte("output") == "final"

    def test_logical_patterns(self) -> None:
        assert categorize_cte("filtered_orders") == "logical"
        assert categorize_cte("joined_data") == "logical"
        assert categorize_cte("aggregated_totals") == "logical"

    def test_unknown_pattern(self) -> None:
        assert categorize_cte("my_custom_cte") == "unknown"


class TestCheckCTEPatterns:
    """Tests for check_cte_patterns function."""

    def test_valid_structure(self) -> None:
        sql = """
        WITH source AS (SELECT * FROM raw),
        transformed AS (SELECT id FROM source),
        final AS (SELECT * FROM transformed)
        SELECT * FROM final
        """
        result = check_cte_patterns(sql)
        assert result.has_ctes is True
        assert result.has_import_cte is True
        assert result.has_final_cte is True
        assert result.is_valid is True

    def test_no_ctes_suggests_pattern(self) -> None:
        result = check_cte_patterns("SELECT * FROM table")
        assert result.has_ctes is False
        assert len(result.suggestions) > 0

    def test_flags_generic_names(self) -> None:
        sql = "WITH cte1 AS (SELECT 1), cte2 AS (SELECT 2) SELECT * FROM cte2"
        result = check_cte_patterns(sql)
        assert any("generic name" in issue.lower() for issue in result.issues)


# =============================================================================
# Naming Rules Tests (naming_rules.py)
# =============================================================================


class TestInferLayerFromPath:
    """Tests for infer_layer_from_path function."""

    def test_bronze_layer(self) -> None:
        assert infer_layer_from_path("models/bronze/stg_orders.sql") == "bronze"

    def test_staging_layer(self) -> None:
        assert infer_layer_from_path("models/staging/stg_orders.sql") == "staging"

    def test_silver_layer(self) -> None:
        assert infer_layer_from_path("models/silver/int_orders.sql") == "silver"

    def test_intermediate_layer(self) -> None:
        assert (
            infer_layer_from_path("models/intermediate/int_orders.sql")
            == "intermediate"
        )

    def test_gold_layer(self) -> None:
        assert infer_layer_from_path("models/gold/dim_customers.sql") == "gold"

    def test_marts_layer(self) -> None:
        assert infer_layer_from_path("models/marts/fct_orders.sql") == "marts"

    def test_unknown_path(self) -> None:
        assert infer_layer_from_path("macros/my_macro.sql") is None


class TestCheckNamingConventions:
    """Tests for check_naming_conventions function."""

    def test_valid_bronze_naming(self) -> None:
        result = check_naming_conventions(
            "stg_sqlserver__customers",
            file_path="models/bronze/stg_sqlserver__customers.sql",
        )
        assert result.is_valid is True

    def test_valid_gold_dim_naming(self) -> None:
        result = check_naming_conventions(
            "dim_customers", file_path="models/gold/dim_customers.sql"
        )
        assert result.is_valid is True

    def test_valid_gold_fct_naming(self) -> None:
        result = check_naming_conventions(
            "fct_order_lines", file_path="models/gold/fct_order_lines.sql"
        )
        assert result.is_valid is True

    def test_invalid_gold_naming(self) -> None:
        result = check_naming_conventions(
            "customers", file_path="models/gold/customers.sql"
        )
        assert result.is_valid is False
        assert result.suggestion is not None


# =============================================================================
# Syntax Rules Tests (syntax_rules.py)
# =============================================================================


class TestCheckSnowflakeSyntax:
    """Tests for check_snowflake_syntax function."""

    def test_valid_snowflake_sql(self) -> None:
        sql = """
        SELECT customer_id, COALESCE(name, 'Unknown') AS name,
               CURRENT_TIMESTAMP() AS loaded_at
        FROM customers LIMIT 100
        """
        result = check_snowflake_syntax(sql)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_sqlserver_top_detected(self) -> None:
        result = check_snowflake_syntax("SELECT TOP 10 * FROM customers")
        assert result.is_valid is False
        assert any("TOP" in e["pattern"] for e in result.errors)

    def test_sqlserver_isnull_detected(self) -> None:
        result = check_snowflake_syntax("SELECT ISNULL(name, 'default') FROM t")
        assert result.is_valid is False
        assert any("ISNULL" in e["pattern"] for e in result.errors)

    def test_sqlserver_getdate_detected(self) -> None:
        result = check_snowflake_syntax("SELECT GETDATE() AS current_time")
        assert result.is_valid is False
        assert any("GETDATE" in e["pattern"] for e in result.errors)

    def test_oracle_rownum_detected(self) -> None:
        result = check_snowflake_syntax("SELECT * FROM t WHERE ROWNUM <= 10")
        assert result.is_valid is False
        assert any("ROWNUM" in e["pattern"] for e in result.errors)

    def test_oracle_decode_allowed(self) -> None:
        """DECODE is supported in Snowflake."""
        result = check_snowflake_syntax(
            "SELECT DECODE(status, 1, 'Active', 'Inactive') FROM t"
        )
        assert result.is_valid is True

    def test_mysql_backticks_detected(self) -> None:
        result = check_snowflake_syntax("SELECT `customer_id` FROM `customers`")
        assert result.is_valid is False
        assert any("Backtick" in e["pattern"] for e in result.errors)

    def test_ignores_patterns_in_strings(self) -> None:
        sql = "SELECT 'Use GETDATE() for time' AS hint FROM dual"
        result = check_snowflake_syntax(sql)
        assert not any("GETDATE" in e.get("pattern", "") for e in result.errors)

    def test_ignores_patterns_in_comments(self) -> None:
        sql = "-- Don't use ISNULL()\nSELECT COALESCE(name, 'x') FROM t"
        result = check_snowflake_syntax(sql)
        assert not any("ISNULL" in e.get("pattern", "") for e in result.errors)


class TestCheckForPlatform:
    """Tests for check_for_platform function."""

    def test_sqlserver_patterns(self) -> None:
        result = check_for_platform(
            "SELECT TOP 10 *, ISNULL(name, 'X') FROM t", "sqlserver"
        )
        assert result.is_valid is False
        assert len(result.errors) >= 2

    def test_oracle_patterns(self) -> None:
        result = check_for_platform("SELECT * FROM t WHERE ROWNUM <= 10", "oracle")
        assert result.is_valid is False

    def test_unknown_platform(self) -> None:
        result = check_for_platform("SELECT TOP 10 * FROM t", "unknown_db")
        assert result.is_valid is True  # No patterns for unknown platform


# =============================================================================
# Validator Helper Tests (validator.py)
# =============================================================================


class TestStripCommentsAndStrings:
    """Tests for strip_comments_and_strings function."""

    def test_removes_block_comments(self) -> None:
        sql = "SELECT /* comment */ * FROM table"
        result = strip_comments_and_strings(sql)
        assert "comment" not in result
        assert "SELECT" in result

    def test_removes_single_line_comments(self) -> None:
        sql = "SELECT * -- comment\nFROM table"
        result = strip_comments_and_strings(sql)
        assert "comment" not in result
        assert "SELECT" in result

    def test_removes_string_literals(self) -> None:
        sql = "SELECT * FROM table WHERE col = 'value'"
        result = strip_comments_and_strings(sql)
        assert "value" not in result
        assert "SELECT" in result


class TestFindLineNumber:
    """Tests for find_line_number function."""

    def test_first_line(self) -> None:
        assert find_line_number("line1\nline2\nline3", 0) == 1

    def test_second_line(self) -> None:
        assert find_line_number("line1\nline2\nline3", 6) == 2

    def test_third_line(self) -> None:
        assert find_line_number("line1\nline2\nline3", 12) == 3
