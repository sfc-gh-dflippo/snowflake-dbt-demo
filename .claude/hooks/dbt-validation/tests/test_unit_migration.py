"""
Unit tests for migration/checker.py dataclasses and helper functions.

Tests migration analysis functions without file I/O.
"""

from __future__ import annotations

from dbt_validation.migration import (
    MigrationStatusReport,
    ModelStatus,
    is_placeholder_model,
)

# =============================================================================
# ModelStatus Tests
# =============================================================================


class TestModelStatus:
    """Tests for ModelStatus dataclass."""

    def test_incomplete_by_default(self) -> None:
        status = ModelStatus(model_name="test_model")
        assert status.is_complete is False

    def test_complete_model(self) -> None:
        status = ModelStatus(
            model_name="test_model",
            sql_path="/path/to/model.sql",
            schema_entry=True,
            has_description=True,
            has_primary_key_test=True,
            is_placeholder=False,
        )
        assert status.is_complete is True

    def test_placeholder_never_complete(self) -> None:
        status = ModelStatus(
            model_name="test_model",
            sql_path="/path/to/model.sql",
            schema_entry=True,
            has_description=True,
            has_primary_key_test=True,
            is_placeholder=True,  # Makes it incomplete
        )
        assert status.is_complete is False

    def test_completion_percentage_full(self) -> None:
        status = ModelStatus(
            model_name="test_model",
            sql_path="/path/to/model.sql",
            schema_entry=True,
            has_description=True,
            has_primary_key_test=True,
            is_placeholder=False,
            columns_documented=10,
            columns_total=10,
        )
        assert status.completion_percentage == 100.0

    def test_completion_percentage_partial(self) -> None:
        status = ModelStatus(
            model_name="test_model",
            sql_path="/path/to/model.sql",
            schema_entry=True,
            has_description=False,
            has_primary_key_test=False,
            is_placeholder=False,
        )
        assert 0 < status.completion_percentage < 100


# =============================================================================
# MigrationStatusReport Tests
# =============================================================================


class TestMigrationStatusReport:
    """Tests for MigrationStatusReport dataclass."""

    def test_empty_report_defaults(self) -> None:
        report = MigrationStatusReport()
        assert report.total_models == 0
        assert report.completion_percentage == 100.0  # No models = 100%

    def test_add_complete_model(self) -> None:
        report = MigrationStatusReport()
        complete_model = ModelStatus(
            model_name="complete",
            sql_path="/path/to/model.sql",
            schema_entry=True,
            has_description=True,
            has_primary_key_test=True,
            is_placeholder=False,
        )
        report.add_model(complete_model)
        assert report.total_models == 1
        assert report.complete_models == 1

    def test_tracks_placeholders(self) -> None:
        report = MigrationStatusReport()
        placeholder = ModelStatus(
            model_name="placeholder",
            sql_path="/path/to/model.sql",
            is_placeholder=True,
        )
        report.add_model(placeholder)
        assert report.placeholder_models == 1


# =============================================================================
# Placeholder Detection Tests
# =============================================================================


class TestIsPlaceholderModel:
    """Tests for is_placeholder_model function."""

    def test_where_false(self) -> None:
        sql = "SELECT * FROM {{ ref('source') }} WHERE FALSE"
        assert is_placeholder_model(sql) is True

    def test_placeholder_comment(self) -> None:
        sql = "-- status: placeholder\nSELECT * FROM {{ ref('source') }}"
        assert is_placeholder_model(sql) is True

    def test_null_cast(self) -> None:
        sql = "SELECT NULL::INTEGER AS customer_id, NULL::VARCHAR AS name FROM t"
        assert is_placeholder_model(sql) is True

    def test_normal_model(self) -> None:
        sql = "SELECT customer_id, name FROM {{ ref('stg_customers') }} WHERE id > 0"
        assert is_placeholder_model(sql) is False
