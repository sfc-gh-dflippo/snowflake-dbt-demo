"""
Unit tests for core/base.py - Severity, create_error, BaseValidationResult.

Tests the core building blocks without file I/O.
"""

from __future__ import annotations

from dbt_validation import SQLValidationResult, YAMLValidationResult
from dbt_validation.core import (
    Severity,
    ValidationResult,
    create_error,
)


class TestSeverity:
    """Tests for Severity constants."""

    def test_error_value(self) -> None:
        assert Severity.ERROR == "error"

    def test_warning_value(self) -> None:
        assert Severity.WARNING == "warning"

    def test_recommendation_value(self) -> None:
        assert Severity.RECOMMENDATION == "recommendation"


class TestCreateError:
    """Tests for create_error utility function."""

    def test_minimal_error(self) -> None:
        """Create error with only required parameters."""
        error = create_error("TEST001", "Test message")
        assert error["rule_id"] == "TEST001"
        assert error["message"] == "Test message"
        assert error["severity"] == "error"

    def test_with_warning_severity(self) -> None:
        error = create_error("TEST001", "Test", severity=Severity.WARNING)
        assert error["severity"] == "warning"

    def test_with_recommendation_severity(self) -> None:
        error = create_error("TEST001", "Test", severity=Severity.RECOMMENDATION)
        assert error["severity"] == "recommendation"

    def test_with_line_number(self) -> None:
        error = create_error("TEST001", "Test", line=42)
        assert error["line"] == 42

    def test_with_extra_context(self) -> None:
        error = create_error(
            "TEST001", "Test", model_name="dim_customers", column_name="customer_id"
        )
        assert error["model_name"] == "dim_customers"
        assert error["column_name"] == "customer_id"


class TestBaseValidationResult:
    """Tests for BaseValidationResult class using YAMLValidationResult."""

    def test_initial_state_valid(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_add_error_invalidates(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("TEST001", "Error", severity="error")
        assert result.is_valid is False

    def test_add_warning_keeps_valid(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("TEST001", "Warning", severity="warning")
        assert result.is_valid is True

    def test_add_recommendation_keeps_valid(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("TEST001", "Recommendation", severity="recommendation")
        assert result.is_valid is True

    def test_error_count(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("E1", "Error 1", severity="error")
        result.add_error("W1", "Warning 1", severity="warning")
        result.add_error("E2", "Error 2", severity="error")
        assert result.error_count == 2

    def test_warning_count(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("E1", "Error", severity="error")
        result.add_error("W1", "Warning 1", severity="warning")
        result.add_error("W2", "Warning 2", severity="warning")
        assert result.warning_count == 2

    def test_get_errors_by_rule(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("YAML001", "Error 1")
        result.add_error("YAML002", "Error 2")
        result.add_error("YAML001", "Error 3")
        assert len(result.get_errors_by_rule("YAML001")) == 2

    def test_has_rule_violation(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        result.add_error("YAML001", "Error")
        assert result.has_rule_violation("YAML001") is True
        assert result.has_rule_violation("YAML002") is False


class TestValidationResultProtocol:
    """Tests for ValidationResult protocol compliance."""

    def test_yaml_result_implements_protocol(self) -> None:
        result = YAMLValidationResult(file_path="test.yml")
        assert isinstance(result, ValidationResult)

    def test_sql_result_implements_protocol(self) -> None:
        result = SQLValidationResult(file_path="test.sql")
        assert isinstance(result, ValidationResult)
