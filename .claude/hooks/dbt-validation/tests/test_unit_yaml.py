"""
Unit tests for yaml/validator.py helper functions.

Tests YAML analysis functions without file I/O.
"""

from __future__ import annotations

from dbt_validation.yaml import (
    get_constraint_test_recommendations,
    has_key_constraint_test,
    is_key_column,
)

# =============================================================================
# Key Column Detection Tests
# =============================================================================


class TestIsKeyColumn:
    """Tests for is_key_column function."""

    def test_id_suffix(self) -> None:
        assert is_key_column("customer_id") is True
        assert is_key_column("order_id") is True
        assert is_key_column("CUSTOMER_ID") is True

    def test_key_suffix(self) -> None:
        assert is_key_column("customer_key") is True
        assert is_key_column("date_key") is True
        assert is_key_column("CUSTOMER_KEY") is True

    def test_sk_suffix(self) -> None:
        assert is_key_column("customer_sk") is True
        assert is_key_column("ORDER_SK") is True

    def test_simple_id(self) -> None:
        assert is_key_column("id") is True
        assert is_key_column("ID") is True

    def test_fk_prefix(self) -> None:
        assert is_key_column("fk_customer") is True
        assert is_key_column("FK_ORDER") is True

    def test_fk_suffix(self) -> None:
        assert is_key_column("customer_fk") is True
        assert is_key_column("ORDER_FK") is True

    def test_non_key_columns(self) -> None:
        assert is_key_column("order_date") is False
        assert is_key_column("customer_name") is False
        assert is_key_column("amount") is False
        assert is_key_column("foreign_value") is False


# =============================================================================
# Key Constraint Test Detection Tests
# =============================================================================


class TestHasKeyConstraintTest:
    """Tests for has_key_constraint_test function."""

    # Primary Key Tests
    def test_dbt_constraints_primary_key(self) -> None:
        column = {"name": "id", "tests": ["dbt_constraints.primary_key"]}
        assert has_key_constraint_test(column) is True

    def test_simple_primary_key(self) -> None:
        column = {"name": "id", "tests": ["primary_key"]}
        assert has_key_constraint_test(column) is True

    def test_unique_plus_not_null(self) -> None:
        column = {"name": "id", "tests": ["unique", "not_null"]}
        assert has_key_constraint_test(column) is True

    # Unique Key Tests
    def test_unique_key(self) -> None:
        column = {"name": "id", "tests": ["unique_key"]}
        assert has_key_constraint_test(column) is True

    def test_dbt_constraints_unique_key(self) -> None:
        column = {"name": "id", "tests": ["dbt_constraints.unique_key"]}
        assert has_key_constraint_test(column) is True

    # Foreign Key Tests
    def test_relationships(self) -> None:
        column = {
            "name": "customer_id",
            "tests": [{"relationships": {"to": "ref('dim_customers')", "field": "id"}}],
        }
        assert has_key_constraint_test(column) is True

    def test_foreign_key(self) -> None:
        column = {"name": "customer_id", "tests": ["foreign_key"]}
        assert has_key_constraint_test(column) is True

    def test_dbt_constraints_foreign_key(self) -> None:
        column = {
            "name": "customer_id",
            "tests": [
                {"dbt_constraints.foreign_key": {"to": "ref('dim')", "field": "id"}}
            ],
        }
        assert has_key_constraint_test(column) is True

    # Invalid Cases
    def test_unique_alone_invalid(self) -> None:
        column = {"name": "id", "tests": ["unique"]}
        assert has_key_constraint_test(column) is False

    def test_not_null_alone_invalid(self) -> None:
        column = {"name": "id", "tests": ["not_null"]}
        assert has_key_constraint_test(column) is False

    def test_no_tests(self) -> None:
        column = {"name": "id"}
        assert has_key_constraint_test(column) is False

    # Alternative Test Keys
    def test_data_tests_key(self) -> None:
        """dbt 1.8+ uses data_tests instead of tests."""
        column = {"name": "id", "data_tests": ["dbt_constraints.primary_key"]}
        assert has_key_constraint_test(column) is True

    def test_dict_style_test(self) -> None:
        column = {
            "name": "id",
            "tests": [{"dbt_constraints.primary_key": {"constraint_name": "pk_table"}}],
        }
        assert has_key_constraint_test(column) is True


# =============================================================================
# Constraint Recommendation Tests
# =============================================================================


class TestGetConstraintTestRecommendations:
    """Tests for get_constraint_test_recommendations function."""

    def test_recommend_pk_for_unique_not_null(self) -> None:
        column = {"name": "id", "tests": ["unique", "not_null"]}
        recs = get_constraint_test_recommendations(column)
        assert len(recs) == 1
        assert recs[0]["recommended"] == "dbt_constraints.primary_key"

    def test_recommend_uk_for_unique_alone(self) -> None:
        column = {"name": "email", "tests": ["unique"]}
        recs = get_constraint_test_recommendations(column)
        assert len(recs) == 1
        assert recs[0]["recommended"] == "dbt_constraints.unique_key"

    def test_recommend_fk_for_relationships(self) -> None:
        column = {
            "name": "customer_id",
            "tests": [{"relationships": {"to": "ref('customers')", "field": "id"}}],
        }
        recs = get_constraint_test_recommendations(column)
        assert len(recs) == 1
        assert recs[0]["recommended"] == "dbt_constraints.foreign_key"

    def test_no_recommendation_for_dbt_constraints(self) -> None:
        column = {"name": "id", "tests": ["dbt_constraints.primary_key"]}
        recs = get_constraint_test_recommendations(column)
        assert len(recs) == 0
