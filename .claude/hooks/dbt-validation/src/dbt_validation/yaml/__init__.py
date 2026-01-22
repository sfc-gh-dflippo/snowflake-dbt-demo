"""
YAML schema validation module.

Validates dbt schema YAML files (_models.yml, _sources.yml) for:
- Required fields (model name, description, columns)
- Key constraint tests (PK, UK, or FK) on key columns
- Column descriptions and data types
- dbt_constraints package usage recommendations
"""

from dbt_validation.yaml.validator import (
    YAMLValidationResult,
    get_constraint_test_recommendations,
    has_key_constraint_test,
    # Helper functions
    is_key_column,
    validate_model,
    validate_schema_yaml,
)

__all__ = [
    # Main validator
    "YAMLValidationResult",
    "validate_schema_yaml",
    "validate_model",
    # Helper functions
    "is_key_column",
    "has_key_constraint_test",
    "get_constraint_test_recommendations",
]
