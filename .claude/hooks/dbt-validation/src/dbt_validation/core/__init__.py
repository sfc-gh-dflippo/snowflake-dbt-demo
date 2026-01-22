"""
Core module for dbt validation.

Contains shared base classes, protocols, and utilities used across
all validators (SQL, YAML, migration).
"""

from dbt_validation.core.base import (
    # Base classes
    BaseValidationResult,
    # Constants
    Severity,
    # Type aliases
    ValidationErrorDict,
    # Protocols
    ValidationResult,
    # Utilities
    create_error,
)

__all__ = [
    # Constants
    "Severity",
    # Type aliases
    "ValidationErrorDict",
    # Protocols
    "ValidationResult",
    # Base classes
    "BaseValidationResult",
    # Utilities
    "create_error",
]
