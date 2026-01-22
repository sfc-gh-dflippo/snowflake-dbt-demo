---
auto_generated: true
description: This quick reference guide provides a condensed overview of commands,
  configuration options, and common usage patterns for the Snowflake Data Validation
  CLI tool, designed for easy lookup during valid
last_scraped: '2026-01-14T16:52:12.318847+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CLI_QUICK_REFERENCE
title: Snowflake Data Validation CLI - Quick Reference | Snowflake Documentation
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../README.md)

    * Tools

      * [SnowConvert AI](../overview.md)

        + General

          + [About](../general/about.md)
          + [Getting Started](../general/getting-started/README.md)
          + [Terms And Conditions](../general/terms-and-conditions/README.md)
          + [Release Notes](../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../general/user-guide/snowconvert/README.md)
            + [Project Creation](../general/user-guide/project-creation.md)
            + [Extraction](../general/user-guide/extraction.md)
            + [Deployment](../general/user-guide/deployment.md)
            + [Data Migration](../general/user-guide/data-migration.md)
            + [Data Validation](../general/user-guide/data-validation.md)
            + [Power BI Repointing](../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../general/technical-documentation/README.md)
          + [Contact Us](../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../translation-references/general/README.md)
          + [Teradata](../translation-references/teradata/README.md)
          + [Oracle](../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../translation-references/transact/README.md)
          + [Sybase IQ](../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../translation-references/hive/README.md)
          + [Redshift](../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../translation-references/postgres/README.md)
          + [BigQuery](../translation-references/bigquery/README.md)
          + [Vertica](../translation-references/vertica/README.md)
          + [IBM DB2](../translation-references/db2/README.md)
          + [SSIS](../translation-references/ssis/README.md)
        + [Migration Assistant](../migration-assistant/README.md)
        + [Data Validation CLI](index.md)

          - [Quick reference](CLI_QUICK_REFERENCE.md)
          - [Usage Guide](CLI_USAGE_GUIDE.md)
          - [Configuration Examples](CONFIGURATION_EXAMPLES.md)
          - [Release Notes](release_notes.md)
        + [AI Verification](../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../sma-docs/README.md)
    * Guides

      * [Teradata](../../guides/teradata.md)
      * [Databricks](../../guides/databricks.md)
      * [SQL Server](../../guides/sqlserver.md)
      * [Amazon Redshift](../../guides/redshift.md)
      * [Oracle](../../guides/oracle.md)
      * [Azure Synapse](../../guides/azuresynapse.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)Quick reference

# Snowflake Data Validation CLI - Quick Reference[¶](#snowflake-data-validation-cli-quick-reference "Link to this heading")

This quick reference guide provides a condensed overview of commands, configuration options, and common usage patterns for the Snowflake Data Validation CLI tool, designed for easy lookup during validation tasks.

---

## Installation[¶](#installation "Link to this heading")

## Prerequisites[¶](#prerequisites "Link to this heading")

Before running the commands below, ensure that Python 3.10 or later and pip are installed on your system.

```
# Base installation
pip install snowflake-data-validation

# With source-specific drivers
pip install "snowflake-data-validation[sqlserver]"
pip install "snowflake-data-validation[teradata]"
pip install "snowflake-data-validation[redshift]"
```

Copy

---

## Command Structure[¶](#command-structure "Link to this heading")

```
snowflake-data-validation <dialect> <command> [options]
# or
sdv <dialect> <command> [options]
```

Copy

**Dialects:** `sqlserver` | `teradata` | `redshift`

---

## Common Commands[¶](#common-commands "Link to this heading")

### `run-validation`[¶](#run-validation "Link to this heading")

```
# SQL Server
sdv sqlserver run-validation --data-validation-config-file config.yaml

# Teradata  
sdv teradata run-validation --data-validation-config-file config.yaml

# Redshift
sdv redshift run-validation --data-validation-config-file config.yaml
```

Copy

### `generate-validation-scripts`[¶](#generate-validation-scripts "Link to this heading")

```
sdv <dialect> generate-validation-scripts --data-validation-config-file config.yaml
```

Copy

### `run-async-validation`[¶](#run-async-validation "Link to this heading")

```
sdv <dialect> run-async-validation --data-validation-config-file config.yaml
```

Copy

### `get-configuration-files`[¶](#get-configuration-files "Link to this heading")

```
sdv <dialect> get-configuration-files --templates-directory ./templates
```

Copy

### `auto-generated-configuration-file`[¶](#auto-generated-configuration-file "Link to this heading")

```
sdv <dialect> auto-generated-configuration-file
```

Copy

### `row-partitioning-helper`[¶](#row-partitioning-helper "Link to this heading")

```
sdv <dialect> row-partitioning-helper
```

Copy

Interactive command to partition large tables by rows for more efficient validation.

### `column-partitioning-helper`[¶](#column-partitioning-helper "Link to this heading")

```
sdv <dialect> column-partitioning-helper
```

Copy

Interactive command to partition wide tables by columns for more efficient validation.

---

## Configuration Template[¶](#configuration-template "Link to this heading")

This template provides the core structure for configuring data validation jobs, defining source and target connections, validation rules, and table-specific settings that control how data is compared between your source database and Snowflake.

```
# GLOBAL
source_platform: SqlServer  # SqlServer | Teradata | Redshift
target_platform: Snowflake
output_directory_path: ./output
max_threads: auto  # "auto" or 1-32
target_database: teradataTargetDatabase # For Teradata sources only - specify target database

# SOURCE CONNECTION
source_connection:
  mode: credentials
  host: "hostname"
  port: 1433
  username: "user"
  password: "pass"
  database: "db"
  # SQL Server only:
  trust_server_certificate: "no"  # yes | no
  encrypt: "yes"  # yes | no | optional

# TARGET CONNECTION
target_connection:
  mode: name  # name | default
  name: "connection_name"  # if mode=name

# VALIDATION
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
  max_failed_rows_number: 100
  exclude_metrics: false
  apply_metric_column_modifier: false

# COMPARISON
comparison_configuration:
  tolerance: 0.01  # 1% tolerance

# LOGGING (optional)
logging_configuration:
  level: INFO  # DEBUG | INFO | WARNING | ERROR | CRITICAL
  console_level: WARNING
  file_level: DEBUG

# MAPPINGS (optional)
database_mappings:
  source_db: target_db

schema_mappings:
  source_schema: target_schema

# TABLES
tables:
  - fully_qualified_name: database.schema.table1
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list: []
    where_clause: ""
    target_where_clause: ""
    chunk_number: 0
    column_mappings: {}
```

Copy

---

## Table Configuration Examples[¶](#table-configuration-examples "Link to this heading")

### Include All Columns[¶](#include-all-columns "Link to this heading")

```
- fully_qualified_name: db.schema.table
  use_column_selection_as_exclude_list: false
  column_selection_list: []
```

Copy

### Include Specific Columns[¶](#include-specific-columns "Link to this heading")

```
- fully_qualified_name: db.schema.table
  use_column_selection_as_exclude_list: false
  column_selection_list:
    - column1
    - column2
    - column3
```

Copy

### Exclude Specific Columns[¶](#exclude-specific-columns "Link to this heading")

```
- fully_qualified_name: db.schema.table
  use_column_selection_as_exclude_list: true
  column_selection_list:
    - audit_timestamp
    - internal_notes
```

Copy

### With Filtering[¶](#with-filtering "Link to this heading")

```
- fully_qualified_name: db.schema.table
  use_column_selection_as_exclude_list: false
  column_selection_list: []
  where_clause: "status = 'ACTIVE' AND created_date >= '2024-01-01'"
  target_where_clause: "status = 'ACTIVE' AND created_date >= '2024-01-01'"
```

Copy

### With Column Mappings[¶](#with-column-mappings "Link to this heading")

```
- fully_qualified_name: db.schema.table
  use_column_selection_as_exclude_list: false
  column_selection_list: []
  column_mappings:
    source_col1: target_col1
    source_col2: target_col2
```

Copy

### Large Table with Chunking[¶](#large-table-with-chunking "Link to this heading")

```
- fully_qualified_name: db.schema.large_table
  use_column_selection_as_exclude_list: false
  column_selection_list: []
  index_column_list:
    - primary_key
  chunk_number: 50
  max_failed_rows_number: 500
```

Copy

---

## Connection Examples[¶](#connection-examples "Link to this heading")

### SQL Server[¶](#sql-server "Link to this heading")

```
source_connection:
  mode: credentials
  host: "sqlserver.company.com"
  port: 1433
  username: "sql_user"
  password: "sql_pass"
  database: "prod_db"
  trust_server_certificate: "no"
  encrypt: "yes"
```

Copy

### Teradata[¶](#teradata "Link to this heading")

```
source_connection:
  mode: credentials
  host: "teradata.company.com"
  username: "td_user"
  password: "td_pass"
  database: "prod_db"
```

Copy

### Redshift[¶](#redshift "Link to this heading")

```
source_connection:
  mode: credentials
  host: "cluster.region.redshift.amazonaws.com"
  port: 5439
  username: "rs_user"
  password: "rs_pass"
  database: "prod_db"
```

Copy

### Snowflake (Named) (See more info here: https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections)[¶](#snowflake-named-see-more-info-here-https-docs-snowflake-com-en-developer-guide-snowflake-cli-connecting-configure-connections "Link to this heading")

```
target_connection:
  mode: name
  name: "my_snowflake_connection"
```

Copy

### Snowflake (Default)[¶](#snowflake-default "Link to this heading")

```
target_connection:
  mode: default
```

Copy

---

## Validation Levels[¶](#validation-levels "Link to this heading")

| Level | Type | Description | Cost |
| --- | --- | --- | --- |
| **1** | Schema | Column names, types, nullability | Low |
| **2** | Metrics | Row counts, distinct values, min/max, avg | Medium |
| **3** | Row | Hash-based row comparison | High |

---

## Common CLI Options[¶](#common-cli-options "Link to this heading")

| Option | Short | Description | Default |
| --- | --- | --- | --- |
| `--data-validation-config-file` | `-dvf` | Config file path | Required |
| `--log-level` | `-ll` | Log level | INFO |
| `--templates-directory` | `-td` | Template output dir | Current dir |
| `--query-templates` |  | Include query templates | false |
| `--output-directory` |  | Results directory | From config |

---

## Log Levels[¶](#log-levels "Link to this heading")

* **DEBUG**: Detailed diagnostic information
* **INFO**: General informational messages
* **WARNING**: Warning messages
* **ERROR**: Error messages
* **CRITICAL**: Critical errors

---

## Configuration Field Reference[¶](#configuration-field-reference "Link to this heading")

### Required Fields[¶](#required-fields "Link to this heading")

* `source_platform`
* `target_platform`
* `output_directory_path`
* `source_connection`
* `target_connection`
* `tables`

### Optional Fields[¶](#optional-fields "Link to this heading")

* `max_threads` (default: “auto”)
* `target_database` (required for Teradata)
* `validation_configuration`
* `comparison_configuration`
* `logging_configuration`
* `database_mappings`
* `schema_mappings`

---

## Table Configuration Fields[¶](#table-configuration-fields "Link to this heading")

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `fully_qualified_name` | ✓ | String | Full table identifier |
| `use_column_selection_as_exclude_list` | ✓ | Boolean | Include/exclude mode |
| `column_selection_list` | ✓ | List | Columns to include/exclude |
| `index_column_list` |  | List | Primary key columns |
| `where_clause` |  | String | Source filter |
| `target_where_clause` |  | String | Target filter |
| `chunk_number` |  | Integer | Number of chunks (0=off) |
| `max_failed_rows_number` |  | Integer | Max failures to report |
| `column_mappings` |  | Dict | Source→Target mappings |
| `is_case_sensitive` |  | Boolean | Case-sensitive matching |

---

## Performance Tips[¶](#performance-tips "Link to this heading")

### For Large Tables[¶](#for-large-tables "Link to this heading")

1. Enable chunking:

   ```
   chunk_number: 100
   ```

   Copy
2. Increase threads:

   ```
   max_threads: 32
   ```

   Copy
3. Filter data:

   ```
   where_clause: "date >= '2024-01-01'"
   ```

   Copy
4. Exclude large columns:

   ```
   use_column_selection_as_exclude_list: true
   column_selection_list:
     - large_blob
     - large_text
   ```

   Copy
5. Skip row validation initially:

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: true
     row_validation: false  # Enable after initial validation
   ```

   Copy

---

## Common Issues[¶](#common-issues "Link to this heading")

### Connection Failed[¶](#connection-failed "Link to this heading")

```
# SQL Server SSL issues
trust_server_certificate: "yes"
encrypt: "optional"
```

Copy

### Out of Memory[¶](#out-of-memory "Link to this heading")

```
# Reduce parallelism
max_threads: 4

# Enable chunking
chunk_number: 50
```

Copy

### Tolerance for Numerical Differences[¶](#tolerance-for-numerical-differences "Link to this heading")

```
# Increase tolerance
comparison_configuration:
  tolerance: 0.05  # 5%
```

Copy

### YAML Syntax Errors[¶](#yaml-syntax-errors "Link to this heading")

* Use spaces, not tabs
* Quote special characters in YAML: :code:`password: "p@ssw0rd!"`
* If a string value starts or ends with a double quote, escape the double quotes “table #1”
* Escape quotes: `name = 'O''Brien'`

---

## Asynchronous Workflow[¶](#asynchronous-workflow "Link to this heading")

The asynchronous workflow allows you to decouple script generation from execution, which is useful when you need to run validation queries manually on the source database or when you have restricted access that requires scheduled execution.

1. Generate the validation scripts:

   ```
   sdv sqlserver generate-validation-scripts --data-validation-config-file config.yaml
   ```

   Copy
2. Execute the generated scripts manually on your source database and save the results to CSV files in the output directory.
3. Run the async validation to compare the saved results:

   ```
   sdv sqlserver run-async-validation --data-validation-config-file config.yaml
   ```

   Copy

---

## Example Workflows[¶](#example-workflows "Link to this heading")

### Basic Validation[¶](#basic-validation "Link to this heading")

1. Get the configuration templates:

   ```
   sdv sqlserver get-configuration-files
   ```

   Copy
2. Edit the generated `config.yaml` file to configure your source and target connections, validation settings, and tables.
3. Run the validation:

   ```
   sdv sqlserver run-validation --data-validation-config-file config.yaml
   ```

   Copy

### Interactive Setup[¶](#interactive-setup "Link to this heading")

1. Generate a configuration file interactively by answering prompts:

   ```
   sdv sqlserver auto-generated-configuration-file
   ```

   Copy
2. Run the validation using the generated configuration:

   ```
   sdv sqlserver run-validation --data-validation-config-file generated_config.yaml
   ```

   Copy

### Debug Mode[¶](#debug-mode "Link to this heading")

To troubleshoot issues or get detailed execution information, run validation with debug logging:

```
sdv sqlserver run-validation \
  --data-validation-config-file config.yaml \
  --log-level DEBUG
```

Copy

### Large Table Partitioning[¶](#large-table-partitioning "Link to this heading")

For validating very large tables, use the partitioning helper to divide tables into smaller segments:

1. Create a configuration file with your table definitions
2. Run the partitioning helper:

   ```
   sdv sqlserver row-partitioning-helper
   ```

   Copy
3. Follow the prompts to specify partition columns and counts
4. Run validation with the partitioned configuration

---

## Output Files[¶](#output-files "Link to this heading")

Generated in `output_directory_path`:

* **Validation reports:** Schema, metrics, row comparison results
* **Log files:** `data_validation_YYYY-MM-DD_HH-MM-SS.log`
* **Difference files:** `differencesL1.csv`, `differencesL2.csv`
* **Generated scripts:** (when using `generate-validation-scripts`)

---

## Environment Variables[¶](#environment-variables "Link to this heading")

For Snowflake connections using default mode, configure:

```
export SNOWFLAKE_ACCOUNT="account_name"
export SNOWFLAKE_USER="username"
export SNOWFLAKE_PASSWORD="password"
export SNOWFLAKE_DATABASE="database"
export SNOWFLAKE_SCHEMA="schema"
export SNOWFLAKE_WAREHOUSE="warehouse"
export SNOWFLAKE_ROLE="role"
```

Copy

---

## Help Commands[¶](#help-commands "Link to this heading")

```
# Main help
sdv --help

# Dialect-specific help
sdv sqlserver --help
sdv teradata --help
sdv redshift --help

# Command-specific help
sdv sqlserver run-validation --help
sdv sqlserver generate-validation-scripts --help
sdv sqlserver row-partitioning-helper --help
sdv sqlserver column-partitioning-helper --help
```

Copy

---

## Resources[¶](#resources "Link to this heading")

* **Full Documentation:** [CLI\_USAGE\_GUIDE.md](CLI_USAGE_GUIDE)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Installation](#installation)
2. [Prerequisites](#prerequisites)
3. [Command Structure](#command-structure)
4. [Common Commands](#common-commands)
5. [Configuration Template](#configuration-template)
6. [Table Configuration Examples](#table-configuration-examples)
7. [Connection Examples](#connection-examples)
8. [Validation Levels](#validation-levels)
9. [Common CLI Options](#common-cli-options)
10. [Log Levels](#log-levels)
11. [Configuration Field Reference](#configuration-field-reference)
12. [Table Configuration Fields](#table-configuration-fields)
13. [Performance Tips](#performance-tips)
14. [Common Issues](#common-issues)
15. [Asynchronous Workflow](#asynchronous-workflow)
16. [Example Workflows](#example-workflows)
17. [Output Files](#output-files)
18. [Environment Variables](#environment-variables)
19. [Help Commands](#help-commands)
20. [Resources](#resources)