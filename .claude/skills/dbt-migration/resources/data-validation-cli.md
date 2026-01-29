# Data Validation CLI

The Snowflake Data Validation CLI (`snowflake-data-validation` or `sdv`) is a command-line tool for
validating data migrations between source databases and Snowflake.

## Supported Source Databases

- SQL Server
- Teradata
- Amazon Redshift

## Validation Levels

### Schema Validation

Confirms the structure of migrated tables is preserved:

- Table name
- Column names and ordinal position
- Data types
- Character maximum length (text columns)
- Numeric precision and scale
- Row count

### Metrics Validation

Confirms data values match the source:

- Minimum value
- Maximum value
- Average
- NULL count
- DISTINCT count
- Standard deviation
- Variance

## Key Features

- **Multi-level validation**: Schema and metrics validation strategies
- **Large table support**: Chunking for performance with big tables
- **Multi-threaded execution**: Parallel processing for efficiency
- **CI/CD integration**: Ready for automated pipelines
- **Configuration files**: YAML-based configuration for repeatability
- **Incremental validation**: Support for ongoing/daily validation

## Quick Start

```bash
# Install
pip install snowflake-data-validation

# Generate config template
sdv sqlserver init-config

# Run validation
sdv sqlserver validate --config validation_config.yaml
```

## Configuration Examples

The CLI supports detailed configuration for:

- Connection settings (source and Snowflake)
- Table-specific settings (column mappings, filters, exclusions)
- Validation levels per table
- Performance tuning (threads, chunk sizes)

## Documentation

- [Documentation Index](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/index)
- [CLI Usage Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CLI_USAGE_GUIDE)
- [Quick Reference](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CLI_QUICK_REFERENCE)
- [Configuration Examples](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CONFIGURATION_EXAMPLES)

### Platform-Specific Commands

- [SQL Server Commands](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/sqlserver_commands)
- [Teradata Commands](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/teradata_commands)
- [Redshift Commands](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/redshift_commands)
