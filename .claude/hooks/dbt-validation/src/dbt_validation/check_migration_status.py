"""
Migration Status Checker for dbt models.

Cross-validates model + schema pairs to ensure:
- Every SQL model has corresponding schema.yml entry
- All columns in SQL are documented in schema.yml
- Primary keys have required tests
- Placeholder models are flagged for completion

This module is designed for batch validation and reporting,
not for hook-based blocking (which uses validate-dbt-file).

Usage:
    check-dbt-migration [models_directory]
"""

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ModelStatus:
    """Status of a single dbt model."""

    model_name: str
    sql_path: str | None = None
    schema_entry: bool = False
    has_description: bool = False
    columns_documented: int = 0
    columns_total: int = 0
    has_primary_key_test: bool = False
    is_placeholder: bool = False
    issues: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        """Check if model migration is complete."""
        return (
            self.sql_path is not None
            and self.schema_entry
            and self.has_description
            and not self.is_placeholder
            and self.has_primary_key_test
        )

    @property
    def completion_percentage(self) -> float:
        """Calculate migration completion percentage."""
        checks = [
            self.sql_path is not None,
            self.schema_entry,
            self.has_description,
            not self.is_placeholder,
            self.has_primary_key_test,
            (
                self.columns_documented >= self.columns_total * 0.8
                if self.columns_total > 0
                else True
            ),
        ]
        return sum(checks) / len(checks) * 100


@dataclass
class MigrationStatusReport:
    """Overall migration status report."""

    models: dict[str, ModelStatus] = field(default_factory=dict)
    total_models: int = 0
    complete_models: int = 0
    placeholder_models: int = 0
    missing_schema: int = 0
    missing_pk_test: int = 0

    def add_model(self, status: ModelStatus):
        """Add a model to the report."""
        self.models[status.model_name] = status
        self.total_models += 1

        if status.is_complete:
            self.complete_models += 1
        if status.is_placeholder:
            self.placeholder_models += 1
        if not status.schema_entry:
            self.missing_schema += 1
        if not status.has_primary_key_test and not status.is_placeholder:
            self.missing_pk_test += 1

    @property
    def completion_percentage(self) -> float:
        """Overall migration completion percentage."""
        if self.total_models == 0:
            return 100.0
        return self.complete_models / self.total_models * 100

    def to_dict(self) -> dict[str, Any]:
        """Convert report to dictionary for JSON serialization."""
        return {
            "summary": {
                "total_models": self.total_models,
                "complete_models": self.complete_models,
                "placeholder_models": self.placeholder_models,
                "missing_schema": self.missing_schema,
                "missing_pk_test": self.missing_pk_test,
                "completion_percentage": round(self.completion_percentage, 1),
            },
            "models": {
                name: {
                    "sql_path": status.sql_path,
                    "schema_entry": status.schema_entry,
                    "has_description": status.has_description,
                    "columns_documented": f"{status.columns_documented}/{status.columns_total}",
                    "has_primary_key_test": status.has_primary_key_test,
                    "is_placeholder": status.is_placeholder,
                    "is_complete": status.is_complete,
                    "completion_percentage": round(status.completion_percentage, 1),
                    "issues": status.issues,
                }
                for name, status in self.models.items()
            },
        }


def extract_model_name_from_path(sql_path: str) -> str:
    """Extract model name from SQL file path."""
    return Path(sql_path).stem


def is_placeholder_model(sql_content: str) -> bool:
    """Check if SQL file is a placeholder model."""
    indicators = [
        "where false",
        "placeholder",
        "null::",
        "-- status: placeholder",
        "-- awaiting logic conversion",
    ]
    content_lower = sql_content.lower()
    return any(ind in content_lower for ind in indicators)


def extract_columns_from_sql(sql_content: str) -> set[str]:
    """Extract column names from SQL model (best effort)."""
    columns = set()

    # Look for column aliases in SELECT statements
    # Pattern: column_name AS alias or just alias at end of line

    # This is a simplified extraction - focus on final CTE columns
    final_match = re.search(
        r"(?:final|result|output)\s+AS\s*\(\s*SELECT(.*?)\)",
        sql_content,
        re.IGNORECASE | re.DOTALL,
    )

    if final_match:
        select_clause = final_match.group(1)
        # Extract column names
        for match in re.finditer(r"\s+AS\s+(\w+)", select_clause, re.IGNORECASE):
            columns.add(match.group(1).lower())

    return columns


def find_models_yml_files(models_dir: str) -> list[str]:
    """Find all schema YAML files in models directory."""
    yml_files = []
    for root, _dirs, files in os.walk(models_dir):
        for file in files:
            if file in ("_models.yml", "_sources.yml", "schema.yml"):
                yml_files.append(os.path.join(root, file))
    return yml_files


def find_sql_files(models_dir: str) -> list[str]:
    """Find all SQL model files in models directory."""
    sql_files = []
    for root, _dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith(".sql"):
                sql_files.append(os.path.join(root, file))
    return sql_files


def load_schema_definitions(yml_files: list[str]) -> dict[str, dict[str, Any]]:
    """Load all model definitions from schema YAML files."""
    models_schema = {}

    for yml_file in yml_files:
        try:
            with open(yml_file, encoding="utf-8") as f:
                content = yaml.safe_load(f)
        except Exception:
            continue

        if not content:
            continue

        models = content.get("models", [])
        for model in models:
            model_name = model.get("name")
            if model_name:
                models_schema[model_name] = {
                    "yml_file": yml_file,
                    "description": model.get("description", ""),
                    "columns": model.get("columns", []),
                }

    return models_schema


def has_pk_test_in_schema(columns: list[dict[str, Any]]) -> bool:
    """Check if any column has a primary key test."""
    for column in columns:
        tests = column.get("tests", []) or column.get("data_tests", [])
        for test in tests:
            if (
                isinstance(test, str)
                and test
                in (
                    "dbt_constraints.primary_key",
                    "primary_key",
                    "unique",
                )
                or isinstance(test, dict)
                and ("dbt_constraints.primary_key" in test or "primary_key" in test)
            ):
                return True
    return False


def check_migration_status(models_dir: str) -> MigrationStatusReport:
    """
    Check migration status for all models in a directory.

    Args:
        models_dir: Path to the models directory

    Returns:
        MigrationStatusReport with status of all models
    """
    report = MigrationStatusReport()

    # Find all files
    yml_files = find_models_yml_files(models_dir)
    sql_files = find_sql_files(models_dir)

    # Load schema definitions
    schema_defs = load_schema_definitions(yml_files)

    # Track which models we've seen
    seen_models = set()

    # Process SQL files
    for sql_path in sql_files:
        model_name = extract_model_name_from_path(sql_path)
        seen_models.add(model_name)

        # Read SQL content
        try:
            with open(sql_path, encoding="utf-8") as f:
                sql_content = f.read()
        except Exception:
            sql_content = ""

        # Create model status
        status = ModelStatus(
            model_name=model_name,
            sql_path=sql_path,
            is_placeholder=is_placeholder_model(sql_content),
        )

        # Check schema entry
        if model_name in schema_defs:
            schema_info = schema_defs[model_name]
            status.schema_entry = True
            status.has_description = bool(schema_info.get("description"))

            columns = schema_info.get("columns", [])
            status.columns_documented = sum(1 for c in columns if c.get("description"))
            status.columns_total = len(columns)
            status.has_primary_key_test = has_pk_test_in_schema(columns)
        else:
            status.issues.append("Missing schema entry in _models.yml")

        # Add issues based on status
        if status.is_placeholder:
            status.issues.append("Model is still a placeholder")
        if not status.has_description:
            status.issues.append("Missing model description")
        if not status.has_primary_key_test and not status.is_placeholder:
            status.issues.append("Missing primary key test")

        report.add_model(status)

    # Check for schema entries without SQL files
    for model_name in schema_defs:
        if model_name not in seen_models:
            status = ModelStatus(
                model_name=model_name,
                schema_entry=True,
                has_description=bool(schema_defs[model_name].get("description")),
            )
            status.issues.append("Schema entry exists but no SQL file found")
            report.add_model(status)

    return report


def print_report(report: MigrationStatusReport):
    """Print a formatted migration status report."""
    print("\n" + "=" * 70)
    print("dbt Migration Status Report")
    print("=" * 70)

    print("\nSummary:")
    print(f"  Total Models:      {report.total_models}")
    print(f"  Complete:          {report.complete_models}")
    print(f"  Placeholders:      {report.placeholder_models}")
    print(f"  Missing Schema:    {report.missing_schema}")
    print(f"  Missing PK Test:   {report.missing_pk_test}")
    print(f"  Completion:        {report.completion_percentage:.1f}%")

    # Group models by status
    incomplete = [
        (name, status)
        for name, status in report.models.items()
        if not status.is_complete
    ]

    if incomplete:
        print(f"\n{'='*70}")
        print("Incomplete Models:")
        print("-" * 70)
        for name, status in sorted(
            incomplete, key=lambda x: x[1].completion_percentage
        ):
            print(f"\n  {name} ({status.completion_percentage:.0f}% complete)")
            for issue in status.issues:
                print(f"    - {issue}")

    print("\n" + "=" * 70 + "\n")


def main():
    """CLI entry point for migration status check."""
    models_dir = "./models" if len(sys.argv) < 2 else sys.argv[1]

    if not os.path.isdir(models_dir):
        print(f"Error: Directory not found: {models_dir}", file=sys.stderr)
        sys.exit(1)

    report = check_migration_status(models_dir)
    print_report(report)

    # Exit with error if incomplete migrations
    if report.completion_percentage < 100:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
