"""
Naming Convention Rules for dbt models.

Validates that model and column names follow established conventions:
- Bronze/Staging: stg_{source}__{table}
- Silver/Intermediate: int_{entity}__{description}
- Gold/Mart: dim_{entity} or fct_{process}
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# =============================================================================
# Result Class
# =============================================================================


@dataclass
class NamingConventionResult:
    """Result of naming convention check."""

    is_valid: bool
    model_name: str
    expected_prefix: str
    actual_prefix: str
    suggestion: str | None = None


# =============================================================================
# Constants
# =============================================================================

# Layer prefix configurations
LAYER_PREFIXES = {
    "bronze": {
        "prefixes": ["stg_"],
        "pattern": r"^stg_[a-z0-9_]+__[a-z0-9_]+$",
        "description": "stg_{source}__{table}",
        "example": "stg_sqlserver__customers",
    },
    "staging": {
        "prefixes": ["stg_"],
        "pattern": r"^stg_[a-z0-9_]+__[a-z0-9_]+$",
        "description": "stg_{source}__{table}",
        "example": "stg_sqlserver__customers",
    },
    "silver": {
        "prefixes": ["int_", "lookup_"],
        "pattern": r"^(int_|lookup_)[a-z0-9_]+(__[a-z0-9_]+)?$",
        "description": "int_{entity}__{description} or lookup_{name}",
        "example": "int_customers__with_orders",
    },
    "intermediate": {
        "prefixes": ["int_", "lookup_"],
        "pattern": r"^(int_|lookup_)[a-z0-9_]+(__[a-z0-9_]+)?$",
        "description": "int_{entity}__{description} or lookup_{name}",
        "example": "int_customers__with_orders",
    },
    "gold": {
        "prefixes": ["dim_", "fct_", "mart_", "agg_"],
        "pattern": r"^(dim_|fct_|mart_|agg_)[a-z0-9_]+$",
        "description": "dim_{entity}, fct_{process}, mart_{name}, or agg_{name}",
        "example": "dim_customers, fct_order_lines",
    },
    "marts": {
        "prefixes": ["dim_", "fct_", "mart_", "agg_"],
        "pattern": r"^(dim_|fct_|mart_|agg_)[a-z0-9_]+$",
        "description": "dim_{entity}, fct_{process}, mart_{name}, or agg_{name}",
        "example": "dim_customers, fct_order_lines",
    },
}

# Column naming patterns
COLUMN_PATTERNS = {
    "primary_key": r"^[a-z_]+_id$|^[a-z_]+_key$|^[a-z_]+_sk$",
    "boolean": r"^(is_|has_|was_|can_|should_|did_)[a-z_]+$",
    "date": r"^[a-z_]+_(date|at|on)$",
    "amount": r"^[a-z_]+_(amount|total|sum|count|qty|quantity)$",
    "timestamp": r"^[a-z_]+_(at|timestamp|ts)$",
}


# =============================================================================
# Functions
# =============================================================================


def infer_layer_from_path(file_path: str) -> str | None:
    """
    Infer the dbt layer from file path.

    Args:
        file_path: Path to the model file

    Returns:
        Layer name or None if not detected
    """
    path_lower = file_path.lower()

    for layer in ["bronze", "silver", "gold", "staging", "intermediate", "marts"]:
        if f"/{layer}/" in path_lower or f"\\{layer}\\" in path_lower:
            return layer

    return None


def get_expected_prefixes(layer: str) -> list[str]:
    """Get expected prefixes for a layer."""
    config = LAYER_PREFIXES.get(layer, {})
    return config.get("prefixes", [])


def check_model_naming(model_name: str, layer: str) -> NamingConventionResult:
    """
    Check if a model name follows naming conventions for its layer.

    Args:
        model_name: The name of the dbt model
        layer: The layer the model belongs to (bronze, silver, gold, etc.)

    Returns:
        NamingConventionResult with validation details
    """
    config = LAYER_PREFIXES.get(layer)

    if not config:
        # Unknown layer, allow any name
        return NamingConventionResult(
            is_valid=True,
            model_name=model_name,
            expected_prefix="any",
            actual_prefix=model_name.split("_")[0] + "_" if "_" in model_name else "",
        )

    expected_prefixes = config["prefixes"]
    pattern = config["pattern"]
    example = config["example"]

    # Check if model name starts with valid prefix
    actual_prefix = ""
    for prefix in expected_prefixes:
        if model_name.lower().startswith(prefix):
            actual_prefix = prefix
            break

    if not actual_prefix:
        # Get the actual prefix from the model name
        parts = model_name.split("_")
        actual_prefix = parts[0] + "_" if parts else ""

    # Check against pattern
    is_valid = bool(re.match(pattern, model_name.lower()))

    suggestion = None
    if not is_valid:
        suggestion = f"Expected format: {config['description']} (e.g., {example})"

    return NamingConventionResult(
        is_valid=is_valid,
        model_name=model_name,
        expected_prefix=", ".join(expected_prefixes),
        actual_prefix=actual_prefix,
        suggestion=suggestion,
    )


def check_column_naming(column_name: str) -> tuple[bool, str | None]:
    """
    Check if a column name follows naming conventions.

    Returns:
        Tuple of (is_valid, suggestion_if_invalid)
    """
    column_lower = column_name.lower()

    # Check for common anti-patterns
    anti_patterns = [
        (r"^col\d+$", "Avoid generic column names like 'col1'"),
        (r"^field\d+$", "Avoid generic column names like 'field1'"),
        (r"^column\d+$", "Avoid generic column names like 'column1'"),
        (r"^var\d+$", "Avoid generic column names like 'var1'"),
        (r"^tmp_", "Avoid temporary column prefixes"),
        (r"^temp_", "Avoid temporary column prefixes"),
        (r"[A-Z]", "Use snake_case (lowercase with underscores)"),
    ]

    for pattern, message in anti_patterns:
        if re.search(pattern, column_name):
            return False, message

    # Check for recommended patterns (informational)
    suggestions = []

    # Boolean columns should start with is_, has_, etc.
    if column_lower.startswith(("active", "enabled", "visible", "deleted")):
        suggestions.append(
            f"Consider renaming to 'is_{column_lower}' for boolean clarity"
        )

    # Date columns should end with _date or _at
    if column_lower.endswith(
        ("day", "month", "year", "time")
    ) and not column_lower.endswith(("_date", "_at")):
        suggestions.append("Consider ending date columns with '_date' or '_at'")

    return True, suggestions[0] if suggestions else None


def check_naming_conventions(
    model_name: str,
    file_path: str | None = None,
    columns: list[str] | None = None,
) -> NamingConventionResult:
    """
    Comprehensive naming convention check.

    Args:
        model_name: The name of the dbt model
        file_path: Optional path to infer layer
        columns: Optional list of column names to check

    Returns:
        NamingConventionResult with validation details
    """
    layer = "other"
    if file_path:
        layer = infer_layer_from_path(file_path) or "other"

    result = check_model_naming(model_name, layer)

    # Check columns if provided
    if columns:
        invalid_columns = []
        for col in columns:
            is_valid, suggestion = check_column_naming(col)
            if not is_valid:
                invalid_columns.append((col, suggestion))

        if invalid_columns:
            col_issues = "; ".join([f"{col}: {msg}" for col, msg in invalid_columns])
            if result.suggestion:
                result.suggestion += f". Column issues: {col_issues}"
            else:
                result.suggestion = f"Column issues: {col_issues}"

    return result
