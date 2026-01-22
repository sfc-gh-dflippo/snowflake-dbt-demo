"""
dbt Validation Tools

A Python package for validating dbt models and schema YAML files.
Designed for use with Claude Code hooks and as a standalone CLI tool.

Installation:
    # No installation required with uv
    uv run .claude/hooks/dbt-validation/validate_dbt_file.py <file>

    # Or install as a tool
    uv tool install .claude/hooks/dbt-validation

CLI Usage:
    validate-dbt-file <file_path>    # Auto-detects file type
    validate-dbt-file --help         # Show options

Programmatic Usage:
    from dbt_validation import validate_schema_yaml, validate_dbt_model

    result = validate_schema_yaml("models/_models.yml")
    if not result.is_valid:
        for error in result.errors:
            print(f"[{error['severity']}] {error['rule_id']}: {error['message']}")

Package Structure:
    dbt_validation/
    ├── core/           # Base classes, enums, protocols
    ├── sql/            # SQL model validation
    │   ├── validator   # Main SQL validator
    │   ├── cte_rules   # CTE pattern checking
    │   ├── syntax_rules # Snowflake compatibility
    │   └── naming_rules # Model/column naming
    ├── yaml/           # Schema YAML validation
    │   └── validator   # Main YAML validator
    └── migration/      # Migration status checking
        └── checker     # Cross-validation of models
"""

__version__ = "0.1.0"

# Core exports
from dbt_validation.core import (
    BaseValidationResult,
    Severity,
    ValidationErrorDict,
    ValidationResult,
    create_error,
)

# Migration exports
from dbt_validation.migration import (
    MigrationStatusReport,
    ModelStatus,
    check_migration_status,
)

# SQL validation exports
from dbt_validation.sql import (
    # Rules
    CTEPatternResult,
    NamingConventionResult,
    SnowflakeSyntaxResult,
    SQLValidationResult,
    check_cte_patterns,
    check_naming_conventions,
    check_snowflake_syntax,
    validate_dbt_model,
)

# YAML validation exports
from dbt_validation.yaml import (
    YAMLValidationResult,
    has_key_constraint_test,
    is_key_column,
    validate_schema_yaml,
)

__all__ = [
    # Version
    "__version__",
    # Core
    "BaseValidationResult",
    "Severity",
    "ValidationResult",
    "ValidationErrorDict",
    "create_error",
    # SQL validation
    "SQLValidationResult",
    "validate_dbt_model",
    "CTEPatternResult",
    "check_cte_patterns",
    "SnowflakeSyntaxResult",
    "check_snowflake_syntax",
    "NamingConventionResult",
    "check_naming_conventions",
    # YAML validation
    "YAMLValidationResult",
    "validate_schema_yaml",
    "is_key_column",
    "has_key_constraint_test",
    # Migration
    "ModelStatus",
    "MigrationStatusReport",
    "check_migration_status",
]
