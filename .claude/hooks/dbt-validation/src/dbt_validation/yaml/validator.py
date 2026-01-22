"""
Schema YAML Validator for dbt models.

This module validates dbt schema YAML files (_models.yml, _sources.yml) to ensure
they follow best practices for documentation, testing, and constraint definition.

Validates:
- Required fields (model name, description, columns)
- Key constraint tests (PK, UK, or FK) on key columns
- Column descriptions
- dbt_constraints package usage recommendations

Rule IDs:
- YAML000: YAML syntax error or file not found (Error)
- YAML001: Model/source must have description (Warning for models, Recommendation for sources)
- YAML002: Key columns should have PK, UK, or FK test (Warning)
- YAML004: All columns should have description (Recommendation)
- YAML006: Recommend dbt_constraints over built-in tests (Recommendation)

References:
    - dbt_constraints package: https://github.com/Snowflake-Labs/dbt_constraints
    - dbt schema.yml docs: https://docs.getdbt.com/reference/configs-and-properties
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Union

import yaml

from dbt_validation.core import (
    BaseValidationResult,
    Severity,
)

# =============================================================================
# Rule IDs - Define locally, no need to modify core/base.py for new rules
# =============================================================================

YAML_SYNTAX_ERROR = "YAML000"
YAML_MISSING_DESCRIPTION = "YAML001"
YAML_MISSING_KEY_TEST = "YAML002"
# YAML003 removed - consolidated into YAML002
YAML_MISSING_COLUMN_DESC = "YAML004"
# YAML005 removed - data_type is rarely used in practice
YAML_RECOMMEND_CONSTRAINTS = "YAML006"


# =============================================================================
# Type Aliases
# =============================================================================

# A dbt test can be either a simple string name or a dict with test config
DbtTest = Union[str, dict[str, Any]]

# Column definition from schema YAML
ColumnDef = dict[str, Any]

# Model definition from schema YAML
ModelDef = dict[str, Any]

# Recommendation for test improvement
TestRecommendation = dict[str, str]


# =============================================================================
# Constants
# =============================================================================

# Regex patterns for detecting key columns by naming convention
# These columns likely need some form of constraint (PK, UK, or FK)
KEY_COLUMN_PATTERNS: list[str] = [
    r".*_id$",  # customer_id, order_id, etc.
    r".*_key$",  # customer_key, date_key, etc.
    r"^id$",  # Simple 'id' column
    r".*_sk$",  # Surrogate key columns (customer_sk, etc.)
    r"^fk_.*",  # fk_customer, fk_order, etc.
    r".*_fk$",  # customer_fk, order_fk, etc.
]

# Valid primary key test names (standalone tests that define a PK)
PRIMARY_KEY_TESTS: tuple[str, ...] = (
    "dbt_constraints.primary_key",
    "primary_key",
)

# Valid unique key test names (require not_null to form a PK)
UNIQUE_KEY_TESTS: tuple[str, ...] = (
    "dbt_constraints.unique_key",
    "unique_key",
    "unique",
)

# Valid foreign key / relationship test names
FOREIGN_KEY_TESTS: tuple[str, ...] = (
    "dbt_constraints.foreign_key",
    "foreign_key",
    "relationships",
)


# =============================================================================
# Result Class
# =============================================================================


@dataclass
class YAMLValidationResult(BaseValidationResult):
    """
    Result of YAML schema file validation.

    Extends BaseValidationResult with YAML-specific functionality for
    adding model_name and column_name context to errors.
    """

    def add_error(
        self,
        rule_id: str,
        message: str,
        severity: str = Severity.ERROR,
        line: int | None = None,
        model_name: str | None = None,
        column_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Add a validation error or warning to the results.

        Args:
            rule_id: Unique identifier for the validation rule (e.g., "YAML001")
            message: Human-readable description of the issue
            severity: Severity.ERROR or Severity.WARNING
            line: Optional line number where the issue was found
            model_name: Optional name of the model with the issue
            column_name: Optional name of the column with the issue
            **kwargs: Additional context fields
        """
        extra_kwargs: dict[str, Any] = {}
        if model_name is not None:
            extra_kwargs["model_name"] = model_name
        if column_name is not None:
            extra_kwargs["column_name"] = column_name
        extra_kwargs.update(kwargs)

        super().add_error(
            rule_id=rule_id,
            message=message,
            severity=severity,
            line=line,
            **extra_kwargs,
        )


# =============================================================================
# Column Name Pattern Matching Functions
# =============================================================================


def is_key_column(column_name: str) -> bool:
    """
    Check if a column name suggests it's a key column based on naming conventions.

    Key columns typically need some form of constraint test (PK, UK, or FK).

    Args:
        column_name: The name of the column to check

    Returns:
        True if the column name matches a key column pattern
    """
    return any(re.match(pattern, column_name, re.IGNORECASE) for pattern in KEY_COLUMN_PATTERNS)


# =============================================================================
# Test Detection Functions
# =============================================================================


def _extract_test_name(test: DbtTest) -> str | None:
    """Extract the test name from a dbt test definition."""
    if isinstance(test, str):
        return test
    elif isinstance(test, dict) and test:
        return list(test.keys())[0]
    return None


def _get_column_tests(column: ColumnDef) -> list[DbtTest]:
    """Get the list of tests defined on a column."""
    tests = column.get("tests") or column.get("data_tests")
    return tests if tests else []


def has_key_constraint_test(column: ColumnDef) -> bool:
    """
    Check if a column has a valid key constraint test configured.

    A valid key constraint test is one of:
    1. primary_key or dbt_constraints.primary_key
    2. unique_key or dbt_constraints.unique_key
    3. unique + not_null (combination that acts as PK)
    4. foreign_key, dbt_constraints.foreign_key, or relationships

    Args:
        column: A column definition from the schema YAML

    Returns:
        True if the column has any valid key constraint test
    """
    tests = _get_column_tests(column)
    if not tests:
        return False

    has_unique: bool = False
    has_not_null: bool = False

    for test in tests:
        test_name = _extract_test_name(test)
        if not test_name:
            continue

        # Direct PK test
        if test_name in PRIMARY_KEY_TESTS:
            return True

        # Direct UK test (standalone, not requiring not_null)
        if test_name in ("dbt_constraints.unique_key", "unique_key"):
            return True

        # FK/relationship test
        if test_name in FOREIGN_KEY_TESTS:
            return True

        # Track for unique + not_null combination
        if test_name == "unique":
            has_unique = True
        elif test_name == "not_null":
            has_not_null = True

    # unique + not_null combination acts as PK
    return has_unique and has_not_null


def has_model_level_key_test(model: ModelDef, column_name: str) -> bool:
    """
    Check if a model has a key constraint test at the model level that references the column.

    Model-level tests can reference columns via:
    - column_name: Single column (PK, UK)
    - column_names: Multiple columns (PK, UK)
    - fk_column_name: Single FK column
    - fk_column_names: Multiple FK columns

    Args:
        model: The model definition from schema YAML
        column_name: The column name to check for

    Returns:
        True if the model has a key constraint test referencing this column
    """
    model_tests = model.get("tests") or model.get("data_tests") or []

    for test in model_tests:
        if isinstance(test, str):
            continue  # Simple test names at model level don't reference specific columns

        if isinstance(test, dict) and test:
            test_name = list(test.keys())[0]
            test_config = test.get(test_name, {})

            # Check if this is a key constraint test
            if test_name not in (
                "dbt_constraints.primary_key",
                "primary_key",
                "dbt_constraints.unique_key",
                "unique_key",
                "dbt_constraints.foreign_key",
                "foreign_key",
                "relationships",
            ):
                continue

            if not isinstance(test_config, dict):
                continue

            # Check for arguments wrapper (dbt 1.10.5+ format)
            if "arguments" in test_config:
                test_config = test_config["arguments"]

            # Check single column references
            if test_config.get("column_name", "").lower() == column_name.lower():
                return True
            if test_config.get("fk_column_name", "").lower() == column_name.lower():
                return True

            # Check multi-column references
            column_names = test_config.get("column_names", [])
            if column_name.lower() in [c.lower() for c in column_names]:
                return True

            fk_column_names = test_config.get("fk_column_names", [])
            if column_name.lower() in [c.lower() for c in fk_column_names]:
                return True

    return False


def get_constraint_test_recommendations(column: ColumnDef) -> list[TestRecommendation]:
    """
    Check if a column uses built-in dbt tests that could be upgraded to dbt_constraints.

    Args:
        column: A column definition from the schema YAML

    Returns:
        List of recommendations with 'builtin', 'recommended', and 'reason' keys
    """
    tests = _get_column_tests(column)
    if not tests:
        return []

    has_unique: bool = False
    has_not_null: bool = False
    has_relationships: bool = False
    uses_dbt_constraints_pk: bool = False
    uses_dbt_constraints_uk: bool = False
    uses_dbt_constraints_fk: bool = False

    for test in tests:
        test_name = _extract_test_name(test)
        if not test_name:
            continue

        if test_name == "unique":
            has_unique = True
        elif test_name == "not_null":
            has_not_null = True
        elif test_name == "relationships":
            has_relationships = True
        elif test_name in ("dbt_constraints.primary_key", "primary_key"):
            uses_dbt_constraints_pk = True
        elif test_name in ("dbt_constraints.unique_key", "unique_key"):
            uses_dbt_constraints_uk = True
        elif test_name in ("dbt_constraints.foreign_key", "foreign_key"):
            uses_dbt_constraints_fk = True

    recommendations: list[TestRecommendation] = []

    if has_unique and has_not_null and not uses_dbt_constraints_pk:
        recommendations.append(
            {
                "builtin": "unique + not_null",
                "recommended": "dbt_constraints.primary_key",
                "reason": "Creates database primary key constraint with RELY for join elimination",
            }
        )
    elif (
        has_unique
        and not has_not_null
        and not uses_dbt_constraints_uk
        and not uses_dbt_constraints_pk
    ):
        recommendations.append(
            {
                "builtin": "unique",
                "recommended": "dbt_constraints.unique_key",
                "reason": "Creates database unique constraint with RELY for join elimination",
            }
        )

    if has_relationships and not uses_dbt_constraints_fk:
        recommendations.append(
            {
                "builtin": "relationships",
                "recommended": "dbt_constraints.foreign_key",
                "reason": "Creates database foreign key constraint enabling BI tool auto-joins",
            }
        )

    return recommendations


# =============================================================================
# Model Validation Functions
# =============================================================================


def validate_model(model: ModelDef, result: YAMLValidationResult) -> None:
    """
    Validate a single model definition from the schema YAML.

    Args:
        model: A model definition dict from the schema YAML
        result: The validation result object to add errors/warnings to
    """
    model_name: str = model.get("name", "unknown")

    # YAML001: Check model description
    if not model.get("description"):
        result.add_error(
            rule_id="YAML001",
            message=f"Model '{model_name}' is missing a description",
            severity=Severity.WARNING,
            model_name=model_name,
        )

    # Validate columns exist
    columns: list[ColumnDef] = model.get("columns", [])
    if not columns:
        result.add_error(
            rule_id="YAML001",
            message=f"Model '{model_name}' has no columns defined",
            severity=Severity.RECOMMENDATION,
            model_name=model_name,
        )
        return

    # Validate each column
    for column in columns:
        column_name: str = column.get("name", "unknown")

        # YAML004: Check column description
        if not column.get("description"):
            result.add_error(
                rule_id="YAML004",
                message=f"Recommend adding description for column '{column_name}' in model '{model_name}'",
                severity=Severity.RECOMMENDATION,
                model_name=model_name,
                column_name=column_name,
            )

        # YAML002: Check key constraint test (column-level or model-level)
        has_column_test = has_key_constraint_test(column)
        has_model_test = has_model_level_key_test(model, column_name)
        if is_key_column(column_name) and not has_column_test and not has_model_test:
            result.add_error(
                rule_id="YAML002",
                message=f"Column '{column_name}' in model '{model_name}' appears to be a key column "
                "but has no primary_key, unique_key, or foreign_key test",
                severity=Severity.WARNING,
                model_name=model_name,
                column_name=column_name,
            )

        # YAML006: Recommend dbt_constraints
        recommendations = get_constraint_test_recommendations(column)
        for rec in recommendations:
            result.add_error(
                rule_id="YAML006",
                message=f"Column '{column_name}' in model '{model_name}' uses '{rec['builtin']}' test. "
                f"Consider using '{rec['recommended']}' instead. {rec['reason']}",
                severity=Severity.RECOMMENDATION,
                model_name=model_name,
                column_name=column_name,
            )


# =============================================================================
# Main Validation Function
# =============================================================================


def validate_schema_yaml(file_path: str) -> YAMLValidationResult:
    """
    Validate a dbt schema YAML file (_models.yml or _sources.yml).

    Args:
        file_path: Path to the YAML file to validate

    Returns:
        YAMLValidationResult containing validation status and any errors/warnings
    """
    result = YAMLValidationResult(file_path=file_path, is_valid=True)

    # Parse YAML file
    try:
        with open(file_path, encoding="utf-8") as f:
            content: Any = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.add_error(
            rule_id="YAML000",
            message=f"Invalid YAML syntax: {e}",
            severity=Severity.ERROR,
        )
        return result
    except FileNotFoundError:
        result.add_error(
            rule_id="YAML000",
            message=f"File not found: {file_path}",
            severity=Severity.ERROR,
        )
        return result

    # Empty file is valid
    if not content:
        return result

    # Validate models section
    models: list[ModelDef] = content.get("models", [])
    for model in models:
        validate_model(model, result)

    # Validate sources section (less strict)
    sources: list[dict[str, Any]] = content.get("sources", [])
    for source in sources:
        source_name: str = source.get("name", "unknown")
        if not source.get("description"):
            result.add_error(
                rule_id="YAML001",
                message=f"Source '{source_name}' is missing a description",
                severity=Severity.RECOMMENDATION,
                model_name=source_name,
            )

    return result
