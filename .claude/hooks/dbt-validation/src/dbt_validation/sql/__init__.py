"""
SQL model validation module.

Validates dbt SQL model files for:
- CTE pattern structure (source → transformed → final)
- Required config block presence
- Explicit column aliases (no SELECT * in final)
- Jinja ref/source usage (not hardcoded table names)
- Snowflake SQL syntax compatibility
- Migration comment headers for converted models
"""

from dbt_validation.sql.cte_rules import (
    CTEPatternResult,
    categorize_cte,
    check_cte_patterns,
    extract_cte_names,
)
from dbt_validation.sql.naming_rules import (
    NamingConventionResult,
    check_model_naming,
    check_naming_conventions,
    infer_layer_from_path,
)
from dbt_validation.sql.syntax_rules import (
    SnowflakeSyntaxResult,
    check_for_platform,
    check_snowflake_syntax,
)
from dbt_validation.sql.validator import (
    SQLValidationResult,
    validate_dbt_model,
)

__all__ = [
    # Main validator
    "SQLValidationResult",
    "validate_dbt_model",
    # CTE rules
    "CTEPatternResult",
    "check_cte_patterns",
    "extract_cte_names",
    "categorize_cte",
    # Syntax rules
    "SnowflakeSyntaxResult",
    "check_snowflake_syntax",
    "check_for_platform",
    # Naming rules
    "NamingConventionResult",
    "check_naming_conventions",
    "check_model_naming",
    "infer_layer_from_path",
]
