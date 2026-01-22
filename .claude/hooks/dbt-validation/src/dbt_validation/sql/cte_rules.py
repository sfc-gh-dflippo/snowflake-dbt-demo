"""
CTE Pattern Rules for dbt models.

Validates that SQL models follow the recommended CTE structure:
1. Import CTEs - Reference source data via ref()/source()
2. Logical CTEs - Transform and join data
3. Final CTE - Prepare final output

Pattern: source → renamed/transformed → final
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# =============================================================================
# Result Class
# =============================================================================


@dataclass
class CTEPatternResult:
    """Result of CTE pattern validation."""

    has_ctes: bool
    cte_names: list[str] = field(default_factory=list)
    has_import_cte: bool = False
    has_final_cte: bool = False
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if CTE pattern is valid (no critical issues)."""
        return self.has_ctes or len(self.issues) == 0


# =============================================================================
# Constants
# =============================================================================

# Common CTE name patterns
IMPORT_CTE_PATTERNS = [
    r"^source",
    r"^src_",
    r"^raw_",
    r"^staged",
    r"^stg_",
    r"^import",
]

FINAL_CTE_PATTERNS = [
    r"^final$",
    r"^result$",
    r"^output$",
    r"^combined$",
    r"^enriched$",
]

LOGICAL_CTE_PATTERNS = [
    r"^filtered",
    r"^joined",
    r"^aggregated",
    r"^transformed",
    r"^renamed",
    r"^deduplicated",
    r"^unioned",
    r"^pivoted",
    r"^unpivoted",
]

# SQL keywords that shouldn't be matched as CTE names
SQL_KEYWORDS = {
    "select",
    "from",
    "where",
    "join",
    "left",
    "right",
    "inner",
    "outer",
    "full",
    "cross",
    "on",
    "and",
    "or",
    "not",
    "in",
    "between",
    "like",
    "is",
    "null",
    "true",
    "false",
    "case",
    "when",
    "then",
    "else",
    "end",
    "cast",
    "coalesce",
    "nullif",
    "group",
    "order",
    "having",
    "limit",
    "offset",
    "union",
    "intersect",
    "except",
    "distinct",
    "all",
    "any",
    "exists",
}


# =============================================================================
# Functions
# =============================================================================


def extract_cte_names(sql: str) -> list[str]:
    """
    Extract CTE names from SQL.

    Args:
        sql: The SQL content to analyze

    Returns:
        List of CTE names found
    """
    # Pattern to match CTE definitions: name AS (
    cte_pattern = r"\b(\w+)\s+AS\s*\("

    # Find all CTEs
    matches = re.findall(cte_pattern, sql, re.IGNORECASE)

    # Filter out SQL keywords
    return [m for m in matches if m.lower() not in SQL_KEYWORDS]


def categorize_cte(cte_name: str) -> str:
    """
    Categorize a CTE by its name pattern.

    Args:
        cte_name: The name of the CTE

    Returns:
        Category: "import", "final", "logical", or "unknown"
    """
    name_lower = cte_name.lower()

    for pattern in IMPORT_CTE_PATTERNS:
        if re.match(pattern, name_lower):
            return "import"

    for pattern in FINAL_CTE_PATTERNS:
        if re.match(pattern, name_lower):
            return "final"

    for pattern in LOGICAL_CTE_PATTERNS:
        if re.match(pattern, name_lower):
            return "logical"

    return "unknown"


def check_cte_order(cte_names: list[str]) -> list[str]:
    """
    Check if CTEs follow a logical order.

    Args:
        cte_names: List of CTE names in order of appearance

    Returns:
        List of order-related issues found
    """
    issues = []

    if not cte_names:
        return issues

    categories = [categorize_cte(name) for name in cte_names]

    # Check that import CTEs come first
    first_non_import = None
    for i, cat in enumerate(categories):
        if cat != "import" and first_non_import is None:
            first_non_import = i
        elif cat == "import" and first_non_import is not None:
            issues.append(
                f"Import CTE '{cte_names[i]}' appears after transformation CTEs. "
                "Consider moving import CTEs to the beginning."
            )

    # Check that final CTE is last
    final_indices = [i for i, cat in enumerate(categories) if cat == "final"]
    if final_indices and final_indices[-1] != len(categories) - 1:
        issues.append(
            f"Final CTE '{cte_names[final_indices[-1]]}' is not the last CTE. "
            "The 'final' CTE should be the last one before the main SELECT."
        )

    return issues


def strip_comments(sql: str) -> str:
    """Remove SQL comments from content."""
    # Remove block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    # Remove single-line comments
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
    return sql


def check_cte_patterns(sql: str) -> CTEPatternResult:
    """
    Check if SQL follows recommended CTE patterns.

    Args:
        sql: The SQL content to analyze

    Returns:
        CTEPatternResult with analysis details
    """
    result = CTEPatternResult(has_ctes=False)

    # Strip comments for analysis
    sql_clean = strip_comments(sql)

    # Check for WITH clause
    if not re.search(r"\bWITH\b", sql_clean, re.IGNORECASE):
        result.suggestions.append(
            "Consider using CTEs for better readability: WITH source AS (...), final AS (...)"
        )
        return result

    result.has_ctes = True

    # Extract CTE names
    result.cte_names = extract_cte_names(sql_clean)

    if not result.cte_names:
        result.issues.append("WITH clause found but no CTEs detected")
        return result

    # Categorize CTEs
    categories = {name: categorize_cte(name) for name in result.cte_names}

    # Check for import CTE
    import_ctes = [name for name, cat in categories.items() if cat == "import"]
    result.has_import_cte = len(import_ctes) > 0

    if not result.has_import_cte:
        result.suggestions.append(
            "Consider naming your first CTE 'source' or using prefix 'src_' for import CTEs"
        )

    # Check for final CTE
    final_ctes = [name for name, cat in categories.items() if cat == "final"]
    result.has_final_cte = len(final_ctes) > 0

    if not result.has_final_cte:
        result.suggestions.append(
            "Consider adding a 'final' CTE as the last CTE for clarity"
        )

    # Check CTE order
    order_issues = check_cte_order(result.cte_names)
    result.issues.extend(order_issues)

    # Check for very long CTE names
    for name in result.cte_names:
        if len(name) > 50:
            result.suggestions.append(
                f"CTE name '{name[:30]}...' is quite long. Consider a shorter, more concise name."
            )

    # Check for meaningful names (not just cte1, cte2, etc.)
    generic_pattern = r"^(cte|temp|t|q|query)\d*$"
    for name in result.cte_names:
        if re.match(generic_pattern, name, re.IGNORECASE):
            result.issues.append(
                f"CTE '{name}' has a generic name. "
                "Use descriptive names like 'filtered_orders' or 'customer_totals'."
            )

    return result


def suggest_cte_structure(sql: str) -> str:
    """
    Suggest a CTE structure for non-CTE SQL.

    Args:
        sql: SQL content without CTEs

    Returns:
        Suggested CTE structure template
    """
    return """
-- Suggested CTE structure:
WITH source AS (
    -- Import data from ref() or source()
    SELECT * FROM {{ ref('upstream_model') }}
),

transformed AS (
    -- Apply transformations
    SELECT
        column1,
        column2,
        -- Add calculated columns
    FROM source
    WHERE condition
),

final AS (
    -- Prepare final output
    SELECT
        *
    FROM transformed
)

SELECT * FROM final
"""
