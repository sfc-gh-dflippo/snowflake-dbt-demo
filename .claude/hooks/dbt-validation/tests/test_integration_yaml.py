"""
Integration tests for yaml/validator.py - YAML schema validation with file fixtures.

Tests the validate_schema_yaml function with actual files.
"""

from __future__ import annotations

from pathlib import Path

from dbt_validation.yaml import validate_schema_yaml


class TestYAML000FileErrors:
    """Integration tests for YAML000 - file errors."""

    def test_file_not_found(self, temp_dir: Path) -> None:
        result = validate_schema_yaml(str(temp_dir / "nonexistent.yml"))
        assert result.is_valid is False
        assert result.errors[0]["rule_id"] == "YAML000"

    def test_invalid_yaml_syntax(self, models_dir: Path) -> None:
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text("invalid: yaml: content: [")
        result = validate_schema_yaml(str(yaml_path))
        assert result.is_valid is False
        assert result.errors[0]["rule_id"] == "YAML000"

    def test_empty_file_valid(self, models_dir: Path) -> None:
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text("")
        result = validate_schema_yaml(str(yaml_path))
        assert result.is_valid is True


class TestYAML001Description:
    """Integration tests for YAML001 - missing description."""

    def test_valid_model_with_description(self, sample_valid_yaml: Path) -> None:
        result = validate_schema_yaml(str(sample_valid_yaml))
        assert result.is_valid is True

    def test_missing_description_warning(self, sample_invalid_yaml: Path) -> None:
        result = validate_schema_yaml(str(sample_invalid_yaml))
        # YAML001 is a warning, not an error
        assert result.is_valid is True
        yaml001_warnings = [e for e in result.errors if e["rule_id"] == "YAML001"]
        assert len(yaml001_warnings) > 0
        assert yaml001_warnings[0]["severity"] == "warning"


class TestYAML004ColumnDescription:
    """Integration tests for YAML004 - missing column description."""

    def test_missing_column_description_recommendation(self, models_dir: Path) -> None:
        yaml_content = """
version: 2

models:
  - name: test_model
    description: Test model description
    columns:
      - name: col1
        data_type: VARCHAR
"""
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text(yaml_content)
        result = validate_schema_yaml(str(yaml_path))
        yaml004 = [e for e in result.errors if e["rule_id"] == "YAML004"]
        assert len(yaml004) > 0
        assert yaml004[0]["severity"] == "recommendation"


class TestCompleteValidation:
    """Integration tests for complete validation scenarios."""

    def test_well_formed_schema_passes(self, models_dir: Path) -> None:
        yaml_content = """
version: 2

models:
  - name: dim_customers
    description: Customer dimension table
    columns:
      - name: customer_key
        description: Primary key
        tests:
          - dbt_constraints.primary_key
      - name: customer_name
        description: Customer full name
"""
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text(yaml_content)
        result = validate_schema_yaml(str(yaml_path))
        assert result.is_valid is True
        # May have recommendations but no errors/warnings
        errors_and_warnings = [
            e for e in result.errors if e["severity"] in ("error", "warning")
        ]
        assert len(errors_and_warnings) == 0
