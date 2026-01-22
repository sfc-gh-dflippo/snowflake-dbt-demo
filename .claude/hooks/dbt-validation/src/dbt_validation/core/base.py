"""
Base classes and protocols for dbt validation.

This module provides shared types and interfaces used across all validators:
- Severity constants for error/warning classification
- ValidationResult protocol for type checking
- BaseValidationResult abstract base class
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# =============================================================================
# Constants
# =============================================================================


class Severity:
    """
    Severity levels for validation issues.

    - ERROR: Will cause failures - must be fixed
    - WARNING: Should be addressed - data quality or portability risk
    - RECOMMENDATION: Best practice suggestions - nice to have
    """

    ERROR: str = "error"
    WARNING: str = "warning"
    RECOMMENDATION: str = "recommendation"


# =============================================================================
# Type Definitions
# =============================================================================

# Standard error dictionary structure
ValidationErrorDict = dict[str, Any]


# =============================================================================
# Protocols
# =============================================================================


@runtime_checkable
class ValidationResult(Protocol):
    """Protocol defining the interface for validation results."""

    file_path: str
    is_valid: bool
    errors: list[ValidationErrorDict]

    def add_error(
        self,
        rule_id: str,
        message: str,
        severity: str = "error",
        line: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Add a validation error or warning."""
        ...


# =============================================================================
# Base Classes
# =============================================================================


@dataclass
class BaseValidationResult(ABC):
    """
    Abstract base class for validation results.

    Provides common functionality for tracking validation errors and warnings.
    Subclasses should implement any domain-specific fields.

    Attributes:
        file_path: Path to the validated file
        is_valid: True if no errors (warnings don't affect validity)
        errors: List of validation errors and warnings
    """

    file_path: str
    is_valid: bool = True
    errors: list[ValidationErrorDict] = field(default_factory=list)

    def add_error(
        self,
        rule_id: str,
        message: str,
        severity: str = "error",
        line: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Add a validation error or warning.

        Args:
            rule_id: Unique identifier for the validation rule (e.g., "YAML001")
            message: Human-readable description of the issue
            severity: Either "error" (fails validation) or "warning" (informational)
            line: Optional line number where the issue was found
            **kwargs: Additional context fields (model_name, column_name, etc.)
        """
        error: ValidationErrorDict = {
            "rule_id": str(rule_id),
            "message": message,
            "severity": severity,
        }

        if line is not None:
            error["line"] = line

        # Add any additional context fields
        error.update(kwargs)

        self.errors.append(error)

        # Only errors (not warnings) affect validity
        if severity == Severity.ERROR or severity == "error":
            self.is_valid = False

    @property
    def error_count(self) -> int:
        """Count of errors (excluding warnings)."""
        return sum(1 for e in self.errors if e.get("severity") == "error")

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return sum(1 for e in self.errors if e.get("severity") == "warning")

    def get_errors_by_rule(self, rule_id: str) -> list[ValidationErrorDict]:
        """Get all errors/warnings for a specific rule ID."""
        return [e for e in self.errors if e.get("rule_id") == rule_id]

    def has_rule_violation(self, rule_id: str) -> bool:
        """Check if a specific rule has any violations."""
        return any(e.get("rule_id") == rule_id for e in self.errors)


# =============================================================================
# Utility Functions
# =============================================================================


def create_error(
    rule_id: str,
    message: str,
    severity: str = Severity.ERROR,
    line: int | None = None,
    **kwargs: Any,
) -> ValidationErrorDict:
    """
    Create a validation error dictionary.

    Args:
        rule_id: The rule identifier (e.g., "YAML001", "SQL003")
        message: Human-readable error message
        severity: Severity.ERROR or Severity.WARNING
        line: Optional line number
        **kwargs: Additional context

    Returns:
        Formatted error dictionary
    """
    error: ValidationErrorDict = {
        "rule_id": rule_id,
        "message": message,
        "severity": severity,
    }

    if line is not None:
        error["line"] = line

    error.update(kwargs)
    return error
