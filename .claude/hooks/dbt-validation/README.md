# dbt-validation

A Python package for validating dbt models and schema YAML files. Designed for use with Claude Code hooks and as a standalone CLI tool.

## Quick Start (No Installation Required)

Run directly with `uv run` - dependencies are installed automatically:

```bash
# Validate a single file (auto-detects type)
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml

# Validate all dbt files in a directory
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/

# Validate entire models directory
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/

# With verbose output
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/dim_customers.sql --verbose

# Simple output for hooks
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml --simple
```

## Installation (Optional)

If you prefer to install the package:

```bash
# Install as a uv tool
uv tool install .claude/hooks/dbt-validation

# Or with pip
pip install .claude/hooks/dbt-validation
```

After installation, the command is available globally:

```bash
validate-dbt-file models/gold/_models.yml
validate-dbt-file models/gold/dim_customers.sql --verbose
```

## CLI Usage

The `validate-dbt-file` command validates dbt files - supports both single files and directories.

```bash
# Validate a single file
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml

# Validate all dbt files in a directory (recursive)
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/

# Options
  --verbose, -v    Show detailed output even for passing files
  --simple, -s     Disable ANSI colors (for logs/hooks)
  --help           Show help message
```

### Features

- **Directory validation**: Pass a directory to validate all SQL and YAML files recursively
- **Rich terminal output**: Beautiful tables and colored output using Rich
- **Simple mode**: Plain text output for hook integration
- **Auto-detection**: Automatically routes to YAML or SQL validator
- **Environment variables**: Supports `$FILE_PATH` substitution for hooks

## Validation Rules

### Severity Levels

| Level              | Exit Code | Description                                            |
| ------------------ | --------- | ------------------------------------------------------ |
| **Error**          | 1         | Must be fixed - will cause failures                    |
| **Warning**        | 0         | Should be addressed - data quality or portability risk |
| **Recommendation** | 0         | Best practice suggestions - nice to have               |

### YAML Validation Rules

| Rule ID | Severity       | Description                                        |
| ------- | -------------- | -------------------------------------------------- |
| YAML000 | Error          | YAML syntax error or file not found                |
| YAML001 | Warning        | Model should have description                      |
| YAML002 | Warning        | Key columns should have PK, UK, or FK test         |
| YAML004 | Recommendation | Recommend adding description for columns           |
| YAML006 | Recommendation | Consider using dbt_constraints over built-in tests |

### SQL Validation Rules

| Rule ID | Severity       | Description                                          |
| ------- | -------------- | ---------------------------------------------------- |
| SQL000  | Error          | File not found or encoding error                     |
| SQL002  | Recommendation | Consider using CTE pattern for readability           |
| SQL003  | Recommendation | Recommend specifying columns instead of SELECT \*    |
| SQL004  | Warning        | Use ref()/source() instead of hardcoded tables       |
| SQL005  | Recommendation | Migrated models should have header comment           |
| SQL006  | Error          | No Snowflake-incompatible syntax (TOP, ISNULL, etc.) |

## Claude Code Hook Integration

Add to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

## Programmatic Usage

```python
from dbt_validation import validate_schema_yaml, validate_dbt_model

# Validate a schema YAML file
result = validate_schema_yaml("models/_models.yml")
if not result.is_valid:
    for error in result.errors:
        print(f"[{error['severity']}] {error['rule_id']}: {error['message']}")

# Validate a SQL model file
result = validate_dbt_model("models/dim_customers.sql")
print(f"Valid: {result.is_valid}")
```

## dbt_constraints Package Recommendation

This validator recommends using the [dbt_constraints](https://github.com/Snowflake-Labs/dbt_constraints) package for:

- **Primary keys**: Use `dbt_constraints.primary_key` instead of `unique + not_null`
- **Unique keys**: Use `dbt_constraints.unique_key` instead of `unique`
- **Foreign keys**: Use `dbt_constraints.foreign_key` instead of `relationships`

Benefits:

- Creates actual database constraints in Snowflake
- Enables join elimination optimization with RELY property
- Allows BI tools to auto-detect relationships

## Development

### Running Tests

```bash
# Run all tests with uv
cd .claude/hooks/dbt-validation
uv run --extra dev pytest

# Run with coverage
uv run --extra dev pytest --cov=dbt_validation --cov-report=term-missing

# Run specific test file
uv run --extra dev pytest tests/test_validate_schema_yaml.py

# Run with verbose output
uv run --extra dev pytest -v
```

### Project Structure

```
.claude/hooks/dbt-validation/
├── pyproject.toml          # Package configuration
├── README.md               # This file
├── validate_dbt_file.py    # Entry point for uv run
├── src/
│   └── dbt_validation/     # Main package
│       ├── __init__.py
│       ├── cli.py          # Typer CLI entry point
│       ├── core/           # Base classes and enums
│       │   ├── __init__.py
│       │   └── base.py     # Severity, RuleIDs, BaseValidationResult
│       ├── sql/            # SQL model validation
│       │   ├── __init__.py
│       │   ├── validator.py    # Main SQL validator
│       │   ├── cte_rules.py    # CTE pattern checking
│       │   ├── syntax_rules.py # Snowflake compatibility
│       │   └── naming_rules.py # Model/column naming
│       ├── yaml/           # Schema YAML validation
│       │   ├── __init__.py
│       │   └── validator.py    # Main YAML validator
│       └── migration/      # Migration status checking
│           ├── __init__.py
│           └── checker.py      # Cross-validation of models
└── tests/                  # Pytest tests
    ├── conftest.py
    ├── test_base.py
    ├── test_cli.py
    ├── test_rules.py
    ├── test_check_migration_status.py
    ├── test_validate_dbt_model.py
    └── test_validate_schema_yaml.py
```

## Dependencies

- Python 3.11+
- pyyaml >= 6.0
- typer >= 0.9.0
- rich >= 13.0.0

All dependencies are automatically installed by `uv run`.

## License

Apache 2.0
