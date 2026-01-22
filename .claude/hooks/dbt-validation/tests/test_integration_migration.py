"""
Integration tests for migration/checker.py - Migration status with file fixtures.

Tests file discovery and migration status checking with actual files.
"""

from __future__ import annotations

from pathlib import Path

from dbt_validation.migration import (
    check_migration_status,
    find_models_yml_files,
    find_sql_files,
    load_schema_definitions,
)


class TestFindSQLFiles:
    """Integration tests for SQL file discovery."""

    def test_finds_sql_files(self, models_dir: Path) -> None:
        (models_dir / "gold" / "dim_customers.sql").write_text("SELECT 1")
        (models_dir / "gold" / "dim_products.sql").write_text("SELECT 2")
        (models_dir / "silver" / "int_orders.sql").write_text("SELECT 3")

        sql_files = find_sql_files(str(models_dir))

        assert len(sql_files) == 3
        assert any("dim_customers" in f for f in sql_files)

    def test_ignores_non_sql_files(self, models_dir: Path) -> None:
        (models_dir / "gold" / "dim_customers.sql").write_text("SELECT 1")
        (models_dir / "gold" / "_models.yml").write_text("version: 2")
        (models_dir / "gold" / "README.md").write_text("# Docs")

        sql_files = find_sql_files(str(models_dir))

        assert len(sql_files) == 1


class TestLoadSchemaDefinitions:
    """Integration tests for schema YAML loading."""

    def test_loads_models_from_yaml(self, models_dir: Path) -> None:
        yaml_content = """
version: 2

models:
  - name: dim_customers
    description: Customer dimension
    columns:
      - name: customer_id
        description: Primary key
  - name: dim_products
    description: Product dimension
"""
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text(yaml_content)

        yml_files = find_models_yml_files(str(models_dir))
        models = load_schema_definitions(yml_files)

        assert "dim_customers" in models
        assert "dim_products" in models
        assert models["dim_customers"]["description"] == "Customer dimension"

    def test_handles_empty_yaml(self, models_dir: Path) -> None:
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text("")

        yml_files = find_models_yml_files(str(models_dir))
        models = load_schema_definitions(yml_files)

        assert len(models) == 0

    def test_handles_invalid_yaml(self, models_dir: Path) -> None:
        yaml_path = models_dir / "gold" / "_models.yml"
        yaml_path.write_text("invalid: yaml: content: [")

        yml_files = find_models_yml_files(str(models_dir))
        models = load_schema_definitions(yml_files)

        assert len(models) == 0


class TestCheckMigrationStatus:
    """Integration tests for main migration status checker."""

    def test_detects_complete_migration(self, models_dir: Path) -> None:
        sql_content = """
{{ config(materialized='table') }}
SELECT customer_id, name FROM {{ ref('raw') }}
"""
        (models_dir / "gold" / "dim_customers.sql").write_text(sql_content)

        yaml_content = """
version: 2

models:
  - name: dim_customers
    description: Customer dimension table
    columns:
      - name: customer_id
        description: Primary key
        tests:
          - unique
          - not_null
"""
        (models_dir / "gold" / "_models.yml").write_text(yaml_content)

        report = check_migration_status(str(models_dir))

        assert report.total_models >= 1
        assert "dim_customers" in report.models
        assert report.models["dim_customers"].schema_entry is True

    def test_detects_missing_schema_entry(self, models_dir: Path) -> None:
        sql_content = """
{{ config(materialized='table') }}
SELECT customer_id, name FROM {{ ref('raw') }}
"""
        (models_dir / "gold" / "dim_orphan.sql").write_text(sql_content)

        yaml_content = "version: 2\nmodels: []\n"
        (models_dir / "gold" / "_models.yml").write_text(yaml_content)

        report = check_migration_status(str(models_dir))

        assert "dim_orphan" in report.models
        assert report.models["dim_orphan"].schema_entry is False
        assert report.missing_schema >= 1
