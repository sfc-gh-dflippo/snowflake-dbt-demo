"""
Integration tests for cli.py - Command-line interface.

Tests CLI commands and file routing with actual files.
"""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from dbt_validation.cli import app, is_models_yaml, is_sql_model, validate_file_internal

runner = CliRunner()


# =============================================================================
# File Type Detection Tests (Unit-like but part of CLI)
# =============================================================================


class TestIsModelsYaml:
    """Tests for is_models_yaml function."""

    def test_valid_paths(self) -> None:
        assert is_models_yaml(Path("models/gold/_models.yml")) is True
        assert is_models_yaml(Path("models/silver/_sources.yml")) is True
        assert is_models_yaml(Path("models/bronze/schema.yml")) is True
        assert is_models_yaml(Path("/abs/path/models/gold/_models.yml")) is True

    def test_invalid_paths(self) -> None:
        assert is_models_yaml(Path("models/gold/model.sql")) is False
        assert is_models_yaml(Path("dbt_project.yml")) is False
        assert is_models_yaml(Path("macros/_macros.yml")) is False
        assert is_models_yaml(Path("_models.yml")) is False  # Not in models/


class TestIsSqlModel:
    """Tests for is_sql_model function."""

    def test_valid_paths(self) -> None:
        assert is_sql_model(Path("models/gold/dim_customers.sql")) is True
        assert is_sql_model(Path("models/silver/int_orders.sql")) is True
        assert is_sql_model(Path("/abs/path/models/bronze/stg_raw.sql")) is True

    def test_invalid_paths(self) -> None:
        assert is_sql_model(Path("models/gold/_models.yml")) is False
        assert is_sql_model(Path("macros/my_macro.sql")) is False
        assert is_sql_model(Path("dim_customers.sql")) is False  # Not in models/


# =============================================================================
# File Routing Tests
# =============================================================================


class TestValidateFileInternal:
    """Tests for internal file routing function."""

    def test_yaml_routing(self, sample_valid_yaml: Path) -> None:
        success, errors = validate_file_internal(str(sample_valid_yaml))
        assert isinstance(success, bool)
        assert isinstance(errors, list)

    def test_sql_routing(self, sample_valid_sql: Path) -> None:
        success, errors = validate_file_internal(str(sample_valid_sql))
        assert isinstance(success, bool)
        assert isinstance(errors, list)

    def test_non_dbt_file_skipped(self, temp_dir: Path) -> None:
        other_file = temp_dir / "readme.txt"
        other_file.write_text("Not a dbt file")
        success, errors = validate_file_internal(str(other_file))
        assert success is True
        assert len(errors) == 0

    def test_nonexistent_file_skipped(self, temp_dir: Path) -> None:
        success, errors = validate_file_internal(str(temp_dir / "missing.sql"))
        assert success is True
        assert len(errors) == 0


# =============================================================================
# CLI Command Tests
# =============================================================================


class TestCLIBasic:
    """Basic CLI command tests."""

    def test_help_flag(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Validate dbt file(s)" in result.output

    def test_simple_flag(self, sample_valid_yaml: Path) -> None:
        result = runner.invoke(app, [str(sample_valid_yaml), "--simple"])
        assert result.exit_code == 0

    def test_verbose_flag(self, sample_valid_yaml: Path) -> None:
        result = runner.invoke(app, [str(sample_valid_yaml), "--verbose"])
        assert result.exit_code == 0


class TestCLISingleFile:
    """CLI tests for single file validation."""

    def test_valid_yaml_exits_0(self, sample_valid_yaml: Path) -> None:
        result = runner.invoke(app, [str(sample_valid_yaml)])
        assert result.exit_code == 0

    def test_valid_sql_exits_0(self, sample_valid_sql: Path) -> None:
        result = runner.invoke(app, [str(sample_valid_sql)])
        assert result.exit_code == 0

    def test_yaml_with_warnings_exits_0(self, sample_invalid_yaml: Path) -> None:
        """Warnings don't cause exit 1."""
        result = runner.invoke(app, [str(sample_invalid_yaml)])
        assert result.exit_code == 0

    def test_invalid_sql_exits_1(self, sample_invalid_sql: Path) -> None:
        """Snowflake-incompatible syntax causes exit 1."""
        result = runner.invoke(app, [str(sample_invalid_sql)])
        assert result.exit_code == 1

    def test_non_dbt_file_exits_0(self, temp_dir: Path) -> None:
        other_file = temp_dir / "readme.txt"
        other_file.write_text("Not a dbt file")
        result = runner.invoke(app, [str(other_file)])
        assert result.exit_code == 0


class TestCLIDirectory:
    """CLI tests for directory validation."""

    def test_valid_directory_exits_0(self, temp_dir: Path) -> None:
        models_dir = temp_dir / "models" / "gold"
        models_dir.mkdir(parents=True)

        # Valid YAML
        (models_dir / "_models.yml").write_text(
            """
version: 2
models:
  - name: dim_test
    description: "A test model"
    columns:
      - name: id
        description: "Primary key"
"""
        )

        # Valid SQL
        (models_dir / "dim_test.sql").write_text(
            """
{{ config(materialized='table') }}

WITH source AS (SELECT * FROM {{ ref('stg_test') }}),
final AS (SELECT id FROM source)
SELECT * FROM final
"""
        )

        result = runner.invoke(app, [str(models_dir)])
        assert result.exit_code == 0

    def test_invalid_directory_exits_1(self, temp_dir: Path) -> None:
        models_dir = temp_dir / "models" / "gold"
        models_dir.mkdir(parents=True)

        # SQL with Snowflake-incompatible syntax
        (models_dir / "bad_model.sql").write_text(
            """
{{ config(materialized='table') }}
SELECT TOP 10 * FROM {{ ref('stg_test') }}
"""
        )

        result = runner.invoke(app, [str(models_dir)])
        assert result.exit_code == 1

    def test_empty_directory_exits_0(self, temp_dir: Path) -> None:
        empty_dir = temp_dir / "empty_models"
        empty_dir.mkdir()
        result = runner.invoke(app, [str(empty_dir)])
        assert result.exit_code == 0
        assert "No dbt files found" in result.output

    def test_verbose_shows_summary(self, temp_dir: Path) -> None:
        models_dir = temp_dir / "models" / "gold"
        models_dir.mkdir(parents=True)

        (models_dir / "dim_test.sql").write_text(
            """
{{ config(materialized='table') }}
WITH source AS (SELECT * FROM {{ ref('stg_test') }}),
final AS (SELECT id FROM source)
SELECT * FROM final
"""
        )

        result = runner.invoke(app, [str(models_dir), "--verbose"])
        assert result.exit_code == 0
        assert "Directory Summary" in result.output
