"""
Integration tests for sql/validator.py - SQL model validation with file fixtures.

Tests the validate_dbt_model function with actual files.
"""

from __future__ import annotations

from pathlib import Path

from dbt_validation.sql import validate_dbt_model


class TestSQL002CTEPattern:
    """Integration tests for SQL002 - CTE pattern recommendation."""

    def test_valid_cte_pattern_passes(self, sample_valid_sql: Path) -> None:
        result = validate_dbt_model(str(sample_valid_sql))
        sql002_errors = [e for e in result.errors if e["rule_id"] == "SQL002"]
        assert len(sql002_errors) == 0

    def test_missing_cte_pattern_flagged(self, models_dir: Path) -> None:
        sql_content = """{{
    config(materialized='table')
}}

SELECT col1, col2 FROM {{ ref('source') }}
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        sql002_errors = [e for e in result.errors if e["rule_id"] == "SQL002"]
        assert len(sql002_errors) > 0

    def test_ephemeral_skips_cte_check(self, models_dir: Path) -> None:
        sql_content = """{{
    config(materialized='ephemeral')
}}

SELECT col1 FROM {{ ref('source') }}
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        sql002_errors = [e for e in result.errors if e["rule_id"] == "SQL002"]
        assert len(sql002_errors) == 0


class TestSQL004HardcodedTables:
    """Integration tests for SQL004 - hardcoded table references."""

    def test_hardcoded_table_flagged(self, models_dir: Path) -> None:
        sql_content = """
WITH source AS (
    SELECT col1 FROM my_database.raw_schema.customers
),
final AS (SELECT * FROM source)
SELECT * FROM final
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        sql004_errors = [e for e in result.errors if e["rule_id"] == "SQL004"]
        assert len(sql004_errors) > 0
        assert sql004_errors[0]["severity"] == "warning"

    def test_ref_usage_passes(self, sample_valid_sql: Path) -> None:
        result = validate_dbt_model(str(sample_valid_sql))
        sql004_errors = [e for e in result.errors if e["rule_id"] == "SQL004"]
        assert len(sql004_errors) == 0


class TestSQL006SnowflakeSyntax:
    """Integration tests for SQL006 - Snowflake-incompatible syntax."""

    def test_top_n_flagged(self, models_dir: Path) -> None:
        sql_content = """{{
    config(materialized='table')
}}

WITH source AS (SELECT TOP 10 * FROM {{ ref('raw') }})
SELECT * FROM source
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        assert result.is_valid is False
        sql006_errors = [e for e in result.errors if e["rule_id"] == "SQL006"]
        assert len(sql006_errors) > 0
        assert "TOP" in sql006_errors[0]["message"]

    def test_isnull_flagged(self, models_dir: Path) -> None:
        sql_content = """{{
    config(materialized='table')
}}

WITH source AS (SELECT ISNULL(col, 'default') AS col FROM {{ ref('raw') }})
SELECT * FROM source
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        assert result.is_valid is False
        assert any(
            "ISNULL" in e["message"] for e in result.errors if e["rule_id"] == "SQL006"
        )

    def test_getdate_flagged(self, models_dir: Path) -> None:
        sql_content = """{{
    config(materialized='table')
}}

WITH source AS (SELECT GETDATE() AS ts FROM {{ ref('raw') }})
SELECT * FROM source
"""
        sql_path = models_dir / "gold" / "test_model.sql"
        sql_path.write_text(sql_content)
        result = validate_dbt_model(str(sql_path))
        assert result.is_valid is False

    def test_valid_snowflake_passes(self, sample_valid_sql: Path) -> None:
        result = validate_dbt_model(str(sample_valid_sql))
        sql006_errors = [e for e in result.errors if e["rule_id"] == "SQL006"]
        assert len(sql006_errors) == 0


class TestFileHandling:
    """Integration tests for file handling edge cases."""

    def test_file_not_found(self, temp_dir: Path) -> None:
        result = validate_dbt_model(str(temp_dir / "nonexistent.sql"))
        assert result.is_valid is False
        assert result.errors[0]["rule_id"] == "SQL000"

    def test_empty_file_valid(self, models_dir: Path) -> None:
        sql_path = models_dir / "gold" / "empty.sql"
        sql_path.write_text("")
        result = validate_dbt_model(str(sql_path))
        assert result.is_valid is True

    def test_whitespace_only_valid(self, models_dir: Path) -> None:
        sql_path = models_dir / "gold" / "whitespace.sql"
        sql_path.write_text("   \n\n   ")
        result = validate_dbt_model(str(sql_path))
        assert result.is_valid is True
