#!/usr/bin/env python3
"""
Clean up verbose descriptions in SKILL.md to be more concise.

This script removes filler phrases like "Translation specification for" and
makes descriptions more scannable while preserving context that helps agents
understand document contents.

Usage:
    python clean_skill_descriptions.py

The script will:
1. Apply regex-based replacements for common verbose patterns
2. Apply literal string replacements for specific edge cases
3. Run pre-commit linter on the SKILL.md file
"""

import re
import subprocess
import sys
from pathlib import Path

# Get the skill directory (parent of scripts folder)
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
SKILL_FILE = SKILL_DIR / "SKILL.md"


def apply_regex_replacements(content: str) -> str:
    """Apply regex-based replacements for common verbose patterns."""

    replacements = [
        # Remove filler phrases
        (r"Translation specification for ", ""),
        (r"Translation reference for all the supported ", "Supported "),
        (r"Translation reference for the ", ""),
        (r"Translation reference for ", ""),
        (r"Translation references to convert ", ""),
        (r"Translation reference to convert ", ""),
        (r"Translation spec for ", ""),
        (r"Translation from ", ""),
        (r"This section shows equivalents between ", ""),
        (r"This section describes ", ""),
        (
            r"This section provides information about the translation that SnowConvert AI performs, over ",
            "",
        ),
        (r"This section details how Snow Convert translates the ", ""),
        (r"This section covers the transformation of ", ""),
        (
            r"This section describe important consideration when migration ",
            "Considerations for migrating ",
        ),
        (
            r"In this section you will find the helper functions used inside procedures that are used to achieve functional equivalence of some ",
            "Helper functions for ",
        ),
        (
            r"In this section you will find helper functions or procedures that are used to achieve functional equivalence of some ",
            "Helper functions for ",
        ),
        (
            r"In this section, you will find the documentation for the translation reference of ",
            "",
        ),
        (r"In this section you could find information about ", ""),
        (r"In this section, you could find information about ", ""),
        (r"This is a translation reference to convert ", ""),
        (r"This article provides an alphabetical list of ", "Alphabetical list of "),
        (r"This page provides a description of the translation for the ", ""),
        # Simplify database names in README descriptions
        (r"BigQuery syntax to Snowflake", "BigQuery"),
        (r"IBM DB2 syntax to Snowflake", "IBM DB2"),
        (
            r"Hive, Spark, and Databricks SQL syntax to Snowflake",
            "Hive, Spark, Databricks",
        ),
        (r"Oracle grammar syntax to Snowflake", "Oracle"),
        (
            r"PostgreSQL, Greenplum, and Netezza syntax to Snowflake",
            "PostgreSQL, Greenplum, Netezza",
        ),
        (r"Amazon Redshift syntax to Snowflake", "Amazon Redshift"),
        (r"SQL Server Integration Services \(SSIS\) to Snowflake", "SSIS"),
        (r"Sybase IQ syntax to Snowflake", "Sybase IQ"),
        (r"Teradata grammar syntax to Snowflake", "Teradata"),
        (
            r"SQL Server and Azure Synapse syntax to Snowflake",
            "SQL Server / Azure Synapse",
        ),
        (r"Vertica syntax to Snowflake", "Vertica"),
        # General translation references
        (
            r"General translation references applicable across multiple source databases",
            "Cross-database references",
        ),
        # Clean up remaining patterns
        (
            r"built-in functions shared by the different dialects\.",
            "Built-in functions (cross-platform)",
        ),
        (r"functions in Oracle and in Snowflake\.", "Functions"),
        (
            r"data types in Oracle and Snowflake, as well as some notes on arithmetic differences\.",
            "Data types and arithmetic",
        ),
        (r"data types in Teradata and in Snowflake\.", "Data types"),
        (r"built-in functions in Teradata to Snowflake", "Built-in functions"),
        (r"Analytic Language Elements\.", "Analytic functions"),
        (r"Data Definition Language Elements\.", "DDL statements"),
        (r"Data Manipulation Language Elements\.", "DML statements"),
        # Final cleanup - remove trailing/leading spaces and fix double spaces
        (r"  +", " "),
        (r"\[ ", "["),
        (r" \]", "]"),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    return content


def apply_specific_replacements(content: str) -> str:
    """Apply specific replacements for edge cases with special characters."""

    # Use regex for patterns that may have Unicode characters
    specific_patterns = [
        # BigQuery identifiers (may have curly quotes)
        (
            r"\[BigQuery quoted identifiers are enclosed by backticks.*?\]\(translation-references/bigquery/bigquery-identifiers\.md\)",
            "[Quoted identifier syntax](translation-references/bigquery/bigquery-identifiers.md)",
        ),
        # Oracle create type (may have curly apostrophe)
        (
            r"\[Oracle Create Type Statements.*?\]\(translation-references/oracle/sql-translation-reference/create_type\.md\)",
            "[CREATE TYPE (UDTs)](translation-references/oracle/sql-translation-reference/create_type.md)",
        ),
        # Wrapped objects
        (
            r"\[Input code can contain wrapped objects.*?\]\(translation-references/oracle/wrapped-objects\.md\)",
            "[Wrapped/encrypted objects](translation-references/oracle/wrapped-objects.md)",
        ),
        # Transact procedure (may have curly apostrophe)
        (
            r"\[This section documents the transformation of the syntax and the procedure.*?\]\(translation-references/transact/transact-create-procedure\.md\)",
            "[CREATE PROCEDURE to JavaScript](translation-references/transact/transact-create-procedure.md)",
        ),
    ]

    for pattern, replacement in specific_patterns:
        content = re.sub(pattern, replacement, content)

    return content


def apply_table_specific_fixes(content: str) -> str:
    """Apply fixes specific to table rows."""

    table_fixes = [
        # Fix generic "SQL Server syntax" descriptions
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/etl-bi-repointing/power-bi-transact-repointing\.md\)",
            "| transact | [Power BI connection repointing](translation-references/transact/etl-bi-repointing/power-bi-transact-repointing.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-ansi-nulls\.md\)",
            "| transact | [ANSI_NULLS setting](translation-references/transact/transact-ansi-nulls.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-built-in-functions\.md\)",
            "| transact | [Built-in functions](translation-references/transact/transact-built-in-functions.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-built-in-procedures\.md\)",
            "| transact | [Built-in procedures](translation-references/transact/transact-built-in-procedures.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-create-table\.md\)",
            "| transact | [CREATE TABLE](translation-references/transact/transact-create-table.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-create-view\.md\)",
            "| transact | [CREATE VIEW](translation-references/transact/transact-create-view.md)",
        ),
        (
            r"\| transact \| \[SQL Server syntax\]\(translation-references/transact/transact-quoted-identifier\.md\)",
            "| transact | [QUOTED_IDENTIFIER setting](translation-references/transact/transact-quoted-identifier.md)",
        ),
        # Fix Hive DDL/DML duplicates
        (
            r"\| hive \| \[DDL/DML statements\]\(translation-references/hive/built-in-functions\.md\)",
            "| hive | [Built-in functions](translation-references/hive/built-in-functions.md)",
        ),
        (
            r"\| hive \| \[DDL/DML statements\]\(translation-references/hive/ddls/create-external-table\.md\)",
            "| hive | [CREATE EXTERNAL TABLE](translation-references/hive/ddls/create-external-table.md)",
        ),
        (
            r"\| hive \| \[DDL/DML statements\]\(translation-references/hive/ddls/create-view\.md\)",
            "| hive | [CREATE VIEW](translation-references/hive/ddls/create-view.md)",
        ),
        (
            r"\| hive \| \[DDL/DML statements\]\(translation-references/hive/ddls/select\.md\)",
            "| hive | [SELECT](translation-references/hive/ddls/select.md)",
        ),
        (
            r"\| hive \| \[DDL/DML statements\]\(translation-references/hive/ddls/tables\.md\)",
            "| hive | [CREATE TABLE](translation-references/hive/ddls/tables.md)",
        ),
        # Fix postgres/greenplum/netezza
        (
            r"\| postgres \| \[Greenplum CREATE TABLE\]\(translation-references/postgres/ddls/create-materialized-view/greenplum-create-materialized-view\.md\)",
            "| postgres | [Greenplum Materialized View](translation-references/postgres/ddls/create-materialized-view/greenplum-create-materialized-view.md)",
        ),
        # Fix system catalog
        (
            r"\| redshift \| \[Built-in functions\]\(translation-references/redshift/redshift-system-catalog\.md\)",
            "| redshift | [System catalog views](translation-references/redshift/redshift-system-catalog.md)",
        ),
    ]

    for pattern, replacement in table_fixes:
        content = re.sub(pattern, replacement, content)

    return content


def run_linter():
    """Run pre-commit linter on SKILL.md."""
    print("\nRunning pre-commit linter...")
    try:
        result = subprocess.run(
            ["pre-commit", "run", "--files", str(SKILL_FILE)],
            cwd=SKILL_DIR.parent.parent.parent,  # Go to repo root
            capture_output=True,
            text=True,
            timeout=120,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Linter timed out")
        return False
    except FileNotFoundError:
        print("pre-commit not found, skipping linter")
        return True


def main():
    """Main function to clean up SKILL.md descriptions."""

    if not SKILL_FILE.exists():
        print(f"Error: {SKILL_FILE} not found")
        sys.exit(1)

    print(f"Reading {SKILL_FILE}...")
    content = SKILL_FILE.read_text()

    print("Applying regex replacements...")
    content = apply_regex_replacements(content)

    print("Applying specific replacements...")
    content = apply_specific_replacements(content)

    print("Applying table-specific fixes...")
    content = apply_table_specific_fixes(content)

    print(f"Writing {SKILL_FILE}...")
    SKILL_FILE.write_text(content)

    print("Done! Descriptions cleaned up.")

    # Run linter
    run_linter()


if __name__ == "__main__":
    main()
