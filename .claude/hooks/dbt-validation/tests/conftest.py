"""
Pytest fixtures and configuration for dbt-validation tests.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def models_dir(temp_dir: Path) -> Path:
    """Create a models directory structure for testing."""
    models = temp_dir / "models"
    models.mkdir()
    (models / "gold").mkdir()
    (models / "silver").mkdir()
    (models / "bronze").mkdir()
    return models


@pytest.fixture
def sample_valid_yaml(models_dir: Path) -> Path:
    """Create a sample valid schema YAML file."""
    yaml_content = """
version: 2

models:
  - name: dim_customers
    description: Customer dimension table with key attributes
    columns:
      - name: customer_key
        description: Unique identifier for the customer
        data_type: INTEGER
        tests:
          - dbt_constraints.primary_key
      - name: customer_name
        description: Full name of the customer
        data_type: VARCHAR
      - name: nation_key
        description: Foreign key to nation dimension
        data_type: INTEGER
        tests:
          - dbt_constraints.foreign_key:
              to: ref('dim_nations')
              field: nation_key
"""
    yaml_path = models_dir / "gold" / "_models.yml"
    yaml_path.write_text(yaml_content)
    return yaml_path


@pytest.fixture
def sample_invalid_yaml(models_dir: Path) -> Path:
    """Create a sample invalid schema YAML file (missing descriptions)."""
    yaml_content = """
version: 2

models:
  - name: dim_products
    columns:
      - name: product_id
      - name: product_name
"""
    # Must use standard filename to be recognized by validator
    yaml_path = models_dir / "silver" / "_models.yml"
    yaml_path.write_text(yaml_content)
    return yaml_path


@pytest.fixture
def sample_valid_sql(models_dir: Path) -> Path:
    """Create a sample valid SQL model file."""
    sql_content = """{{
    config(
        materialized='table',
        schema='gold'
    )
}}

WITH source AS (
    SELECT *
    FROM {{ ref('stg_customers') }}
),

transformed AS (
    SELECT
        customer_id AS customer_key,
        customer_name,
        nation_id AS nation_key,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM source
),

final AS (
    SELECT
        customer_key,
        customer_name,
        nation_key,
        loaded_at
    FROM transformed
)

SELECT * FROM final
"""
    sql_path = models_dir / "gold" / "dim_customers.sql"
    sql_path.write_text(sql_content)
    return sql_path


@pytest.fixture
def sample_invalid_sql(models_dir: Path) -> Path:
    """Create a sample SQL with Snowflake-incompatible syntax."""
    sql_content = """
-- Simple query without config
SELECT TOP 10 *
FROM SCHEMA.TABLE_NAME
WHERE ISNULL(column1, 'default') = 'value'
"""
    sql_path = models_dir / "gold" / "bad_model.sql"
    sql_path.write_text(sql_content)
    return sql_path
