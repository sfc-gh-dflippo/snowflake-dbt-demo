"""
Migration status checking module.

Cross-validates model + schema pairs to ensure:
- Every SQL model has corresponding schema.yml entry
- All columns in SQL are documented in schema.yml
- Primary keys have required tests
- Placeholder models are flagged for completion
"""

from dbt_validation.migration.checker import (
    MigrationStatusReport,
    ModelStatus,
    check_migration_status,
    find_models_yml_files,
    find_sql_files,
    # Helper functions
    is_placeholder_model,
    load_schema_definitions,
)

__all__ = [
    # Main classes
    "ModelStatus",
    "MigrationStatusReport",
    "check_migration_status",
    # Helper functions
    "is_placeholder_model",
    "find_sql_files",
    "find_models_yml_files",
    "load_schema_definitions",
]
