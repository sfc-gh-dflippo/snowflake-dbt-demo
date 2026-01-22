"""
dbt Validation CLI - Modern Command Line Interface

This module provides the CLI entry point for dbt file validation using Typer.
It routes validation to the appropriate validator based on file path patterns.
Supports both single files and directories.

Usage:
    # Validate a single file
    uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml

    # Validate all dbt files in a directory
    uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/

    # After installation
    validate-dbt-file models/gold/_models.yml
    validate-dbt-file models/

Exit codes:
    0: Validation passed (or no files in scope)
    1: Validation failed with errors
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dbt_validation.sql import validate_dbt_model
from dbt_validation.yaml import validate_schema_yaml

# =============================================================================
# Console Setup
# =============================================================================

# Rich console for colored output
console = Console(stderr=True)

# Plain console for simple output (no ANSI colors)
plain_console = Console(stderr=True, no_color=True, force_terminal=False)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ValidationError:
    """
    Represents a single validation error or warning.

    Attributes:
        rule_id: Unique identifier for the validation rule (e.g., "YAML001")
        message: Human-readable description of the issue
        severity: Either "error" (fails validation) or "warning" (informational)
        line: Optional line number where the issue was found
    """

    rule_id: str
    message: str
    severity: str = "error"
    line: int | None = None


# =============================================================================
# File Type Detection Functions
# =============================================================================


def is_models_yaml(file_path: Path) -> bool:
    """
    Check if file is a dbt schema YAML file.

    Args:
        file_path: Path to the file to check

    Returns:
        True if this is a schema YAML file in the models directory
    """
    path_str = str(file_path)
    if "models/" not in path_str and "models\\" not in path_str:
        return False
    filename = file_path.name
    return filename in ("_models.yml", "_sources.yml", "schema.yml")


def is_sql_model(file_path: Path) -> bool:
    """
    Check if file is a dbt SQL model file.

    Args:
        file_path: Path to the file to check

    Returns:
        True if this is a SQL file in the models directory
    """
    path_str = str(file_path)
    if "models/" not in path_str and "models\\" not in path_str:
        return False
    return file_path.suffix.lower() == ".sql"


# =============================================================================
# Directory Scanning Functions
# =============================================================================


def find_dbt_files(directory: Path) -> list[Path]:
    """
    Find all dbt SQL and YAML files in a directory recursively.

    Args:
        directory: Path to the directory to scan

    Returns:
        List of paths to dbt files (SQL models and schema YAMLs)
    """
    dbt_files: list[Path] = []

    for root, _dirs, files in os.walk(directory):
        root_path = Path(root)
        for filename in files:
            file_path = root_path / filename
            # Check if it's a dbt file we should validate
            if is_models_yaml(file_path) or is_sql_model(file_path):
                dbt_files.append(file_path)

    return sorted(dbt_files)


# =============================================================================
# Output Formatting Functions
# =============================================================================


def display_file_results(
    errors: list[ValidationError],
    file_path: str,
    verbose: bool = False,
    use_color: bool = True,
) -> None:
    """
    Display validation results for a single file using table formatting.

    Args:
        errors: List of validation errors/warnings
        file_path: Path to the validated file
        verbose: If True, show detailed output even for passing files
        use_color: If True, use ANSI colors; if False, plain text
    """
    output = console if use_color else plain_console

    if not errors and not verbose:
        return

    # Count by severity
    error_count = sum(1 for e in errors if e.severity == "error")
    warning_count = sum(1 for e in errors if e.severity == "warning")
    recommendation_count = sum(1 for e in errors if e.severity == "recommendation")

    # Create results table
    if errors:
        table = Table(title=f"Validation Results: {file_path}", show_header=True)
        table.add_column("Severity", style="bold" if use_color else None, width=14)
        table.add_column("Rule", style="cyan" if use_color else None, width=10)
        table.add_column("Line", justify="right", width=6)
        table.add_column("Message", style="white" if use_color else None)

        for error in errors:
            if use_color:
                if error.severity == "error":
                    severity_style = "red bold"
                elif error.severity == "warning":
                    severity_style = "yellow"
                else:  # recommendation
                    severity_style = "blue"
                severity_text = Text(error.severity.upper(), style=severity_style)
            else:
                severity_text = error.severity.upper()
            line_str = str(error.line) if error.line else "-"
            table.add_row(severity_text, error.rule_id, line_str, error.message)

        output.print(table)

    # Summary panel - build counts string
    counts = []
    if error_count > 0:
        counts.append(f"{error_count} error(s)")
    if warning_count > 0:
        counts.append(f"{warning_count} warning(s)")
    if recommendation_count > 0:
        counts.append(f"{recommendation_count} recommendation(s)")
    counts_str = ", ".join(counts) if counts else "No issues"

    if error_count > 0:
        if use_color:
            summary = Panel(
                f"[red bold]FAILED[/red bold]: {counts_str}",
                title="Summary",
                border_style="red",
            )
        else:
            summary = Panel(f"FAILED: {counts_str}", title="Summary")
    elif warning_count > 0:
        if use_color:
            summary = Panel(
                f"[yellow]PASSED with warnings[/yellow]: {counts_str}",
                title="Summary",
                border_style="yellow",
            )
        else:
            summary = Panel(f"PASSED with warnings: {counts_str}", title="Summary")
    elif recommendation_count > 0:
        if use_color:
            summary = Panel(
                f"[blue]PASSED[/blue]: {counts_str}",
                title="Summary",
                border_style="blue",
            )
        else:
            summary = Panel(f"PASSED: {counts_str}", title="Summary")
    else:
        if use_color:
            summary = Panel(
                "[green bold]PASSED[/green bold]: No issues found",
                title="Summary",
                border_style="green",
            )
        else:
            summary = Panel("PASSED: No issues found", title="Summary")

    output.print(summary)


def display_directory_results(
    all_results: dict[str, list[ValidationError]],
    verbose: bool = False,
    use_color: bool = True,
) -> None:
    """
    Display aggregated validation results for multiple files.

    Args:
        all_results: Dict mapping file paths to their validation errors
        verbose: If True, show detailed output even for passing files
        use_color: If True, use ANSI colors; if False, plain text
    """
    output = console if use_color else plain_console

    # Calculate totals
    total_files = len(all_results)
    files_with_errors = sum(
        1
        for errors in all_results.values()
        if any(e.severity == "error" for e in errors)
    )
    files_with_warnings = sum(
        1
        for errors in all_results.values()
        if any(e.severity == "warning" for e in errors)
        and not any(e.severity == "error" for e in errors)
    )
    total_errors = sum(
        sum(1 for e in errors if e.severity == "error")
        for errors in all_results.values()
    )
    total_warnings = sum(
        sum(1 for e in errors if e.severity == "warning")
        for errors in all_results.values()
    )
    total_recommendations = sum(
        sum(1 for e in errors if e.severity == "recommendation")
        for errors in all_results.values()
    )

    # Show per-file results for files with issues (or all if verbose)
    for file_path, errors in sorted(all_results.items()):
        has_issues = bool(errors)
        if has_issues or verbose:
            display_file_results(errors, file_path, verbose, use_color)
            output.print()  # Blank line between files

    # Build counts string
    counts = []
    if total_errors > 0:
        counts.append(f"{total_errors} error(s)")
    if total_warnings > 0:
        counts.append(f"{total_warnings} warning(s)")
    if total_recommendations > 0:
        counts.append(f"{total_recommendations} recommendation(s)")
    counts_str = ", ".join(counts) if counts else "No issues"

    # Overall summary
    if total_files == 0:
        if use_color:
            summary = Panel(
                "[yellow]No dbt files found to validate[/yellow]",
                title="Directory Summary",
                border_style="yellow",
            )
        else:
            summary = Panel("No dbt files found to validate", title="Directory Summary")
    elif files_with_errors > 0:
        if use_color:
            summary = Panel(
                f"[red bold]FAILED[/red bold]: "
                f"{files_with_errors}/{total_files} files with errors\n"
                f"Total: {counts_str}",
                title="Directory Summary",
                border_style="red",
            )
        else:
            summary = Panel(
                f"FAILED: {files_with_errors}/{total_files} files with errors\n"
                f"Total: {counts_str}",
                title="Directory Summary",
            )
    elif total_warnings > 0:
        if use_color:
            summary = Panel(
                f"[yellow]PASSED with warnings[/yellow]: "
                f"{files_with_warnings}/{total_files} files with warnings\n"
                f"Total: {counts_str}",
                title="Directory Summary",
                border_style="yellow",
            )
        else:
            summary = Panel(
                f"PASSED with warnings: {files_with_warnings}/{total_files} files with warnings\n"
                f"Total: {counts_str}",
                title="Directory Summary",
            )
    elif total_recommendations > 0:
        if use_color:
            summary = Panel(
                f"[blue]PASSED[/blue]: {total_files} files validated\n"
                f"Total: {counts_str}",
                title="Directory Summary",
                border_style="blue",
            )
        else:
            summary = Panel(
                f"PASSED: {total_files} files validated\n" f"Total: {counts_str}",
                title="Directory Summary",
            )
    else:
        if use_color:
            summary = Panel(
                f"[green bold]PASSED[/green bold]: All {total_files} files validated successfully",
                title="Directory Summary",
                border_style="green",
            )
        else:
            summary = Panel(
                f"PASSED: All {total_files} files validated successfully",
                title="Directory Summary",
            )

    output.print(summary)


# =============================================================================
# Core Validation Function
# =============================================================================


def validate_file_internal(file_path: str) -> tuple[bool, list[ValidationError]]:
    """
    Validate a dbt file and return validation status.

    Args:
        file_path: Path to the file to validate

    Returns:
        Tuple of (success: bool, errors: List[ValidationError])
    """
    path = Path(file_path)
    errors: list[ValidationError] = []

    # Skip validation if file doesn't exist
    if not path.exists():
        return True, []

    # Route to appropriate validator based on file type
    if is_models_yaml(path):
        result = validate_schema_yaml(file_path)
        errors = [
            ValidationError(
                rule_id=e["rule_id"],
                message=e["message"],
                severity=e.get("severity", "error"),
                line=e.get("line"),
            )
            for e in result.errors
        ]
    elif is_sql_model(path):
        result = validate_dbt_model(file_path)
        errors = [
            ValidationError(
                rule_id=e["rule_id"],
                message=e["message"],
                severity=e.get("severity", "error"),
                line=e.get("line"),
            )
            for e in result.errors
        ]
    else:
        # File not in scope for validation
        return True, []

    has_errors = any(e.severity == "error" for e in errors)
    return not has_errors, errors


# =============================================================================
# Typer CLI Application
# =============================================================================

app = typer.Typer(
    name="validate-dbt-file",
    help="Validate dbt model and schema files for best practices and Snowflake compatibility.",
    add_completion=False,
    rich_markup_mode="rich",
)


@app.command()
def validate(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to a dbt file or directory to validate",
            envvar="FILE_PATH",
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v", help="Show detailed output even for passing files"
        ),
    ] = False,
    simple: Annotated[
        bool,
        typer.Option("--simple", "-s", help="Disable ANSI colors (for logs/hooks)"),
    ] = False,
) -> None:
    """
    Validate dbt file(s) - supports both single files and directories.

    For single files:
    - Schema YAML files (_models.yml, _sources.yml) → YAML validation
    - SQL model files (*.sql in models/) → SQL validation
    - Other files → Skip (exit 0)

    For directories:
    - Recursively finds and validates all SQL and YAML files
    - Reports aggregated results

    [bold]Examples:[/bold]

        validate-dbt-file models/gold/_models.yml
        validate-dbt-file models/gold/dim_customers.sql --verbose
        validate-dbt-file models/                        # Validate all files
        validate-dbt-file models/gold/                   # Validate gold layer
    """
    # Handle environment variable substitution
    if path.startswith("$"):
        var_name = path[1:]
        path = os.environ.get(var_name, path)

    target = Path(path)
    use_color = not simple

    # Check if path is a directory
    if target.is_dir():
        # Find all dbt files in directory
        dbt_files = find_dbt_files(target)

        if not dbt_files:
            output = console if use_color else plain_console
            if use_color:
                output.print(f"[yellow]No dbt files found in {path}[/yellow]")
            else:
                output.print(f"No dbt files found in {path}")
            raise typer.Exit(code=0)

        # Validate all files
        all_results: dict[str, list[ValidationError]] = {}
        any_errors = False

        for file_path in dbt_files:
            success, errors = validate_file_internal(str(file_path))
            all_results[str(file_path)] = errors
            if not success:
                any_errors = True

        # Display aggregated results
        display_directory_results(all_results, verbose, use_color)

        raise typer.Exit(code=1 if any_errors else 0)

    else:
        # Single file validation
        success, errors = validate_file_internal(path)

        # Display results
        display_file_results(errors, path, verbose, use_color)

        raise typer.Exit(code=0 if success else 1)


# =============================================================================
# Entry Point
# =============================================================================


def main() -> None:
    """Main entry point for validate-dbt-file command."""
    app()


if __name__ == "__main__":
    main()
