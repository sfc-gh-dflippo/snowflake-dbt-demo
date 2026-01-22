---
auto_generated: true
description: This page provides comprehensive reference documentation for Teradata-specific
  commands in the Snowflake Data Validation CLI. For SQL Server commands, see SQL
  Server Commands Reference. For Amazon Red
last_scraped: '2026-01-14T16:55:07.608684+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/teradata_commands.html
title: Teradata Commands Reference | Snowflake Documentation
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

            * [Redshift commands](redshift_commands.md)
            * [SQLServer commands](sqlserver_commands.md)
            * [Teradata commands](teradata_commands.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)[Usage Guide](CLI_USAGE_GUIDE.md)Teradata commands

# Teradata Commands Reference[¶](#teradata-commands-reference "Link to this heading")

## Overview[¶](#overview "Link to this heading")

This page provides comprehensive reference documentation for Teradata-specific commands in the Snowflake Data Validation CLI. For SQL Server commands, see [SQL Server Commands Reference](sqlserver_commands). For Amazon Redshift commands, see [Redshift Commands Reference](redshift_commands).

---

## Command Structure[¶](#command-structure "Link to this heading")

All Teradata commands follow this consistent structure:

```
snowflake-data-validation teradata <command> [options]

# Or use the shorter alias
sdv teradata <command> [options]
```

Copy

Where `<command>` is one of:

* `run-validation` - Run synchronous validation
* `run-async-validation` - Run asynchronous validation
* `generate-validation-scripts` - Generate validation scripts
* `get-configuration-files` - Get configuration templates
* `auto-generated-configuration-file` - Interactive config generation
* `row-partitioning-helper` - Interactive row partitioning configuration
* `column-partitioning-helper` - Interactive column partitioning configuration

---

## Run Synchronous Validation[¶](#run-synchronous-validation "Link to this heading")

Validates data between Teradata and Snowflake in real-time.

### Syntax[¶](#syntax "Link to this heading")

```
snowflake-data-validation teradata run-validation \
  --data-validation-config-file /path/to/config.yaml \
  --log-level INFO
```

Copy

### Options[¶](#options "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file containing validation settings
* **Example:** `--data-validation-config-file ./configs/teradata_validation.yaml`

**`--teradata-host`** (optional)

* **Type:** String
* **Description:** Teradata server hostname (overrides config file)
* **Example:** `--teradata-host teradata.company.com`

**`--teradata-username`** (optional)

* **Type:** String
* **Description:** Teradata username (overrides config file)
* **Example:** `--teradata-username my_user`

**`--teradata-password`** (optional)

* **Type:** String
* **Description:** Teradata password (overrides config file)
* **Example:** `--teradata-password my_password`

**`--teradata-database`** (optional)

* **Type:** String
* **Description:** Teradata database name (overrides config file)
* **Example:** `--teradata-database prod_db`

**`--snowflake-connection-name`** (optional)

* **Type:** String
* **Description:** Snowflake connection name
* **Example:** `--snowflake-connection-name prod_connection`

**`--output-directory`** (optional)

* **Type:** String (path)
* **Description:** Directory for validation results
* **Example:** `--output-directory ./validation_results`

**`--log-level, -ll`** (optional)

* **Type:** String
* **Valid Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Default:** INFO
* **Description:** Logging level for validation execution
* **Example:** `--log-level DEBUG`

### Example Usage[¶](#example-usage "Link to this heading")

```
# Basic validation using config file
sdv teradata run-validation \
  --data-validation-config-file ./configs/teradata_validation.yaml

# Validation with connection override
sdv teradata run-validation \
  --data-validation-config-file ./config.yaml \
  --teradata-host teradata.company.com \
  --teradata-username my_user \
  --teradata-password my_password \
  --output-directory ./validation_results

# Validation with debug logging
sdv teradata run-validation \
  --data-validation-config-file ./config.yaml \
  --log-level DEBUG

# Using full command name with all options
snowflake-data-validation teradata run-validation \
  -dvf /opt/validations/prod_config.yaml \
  --teradata-host td-prod.company.com \
  --teradata-database production_db \
  --snowflake-connection-name snowflake_prod \
  --output-directory /data/validation_results \
  -ll INFO
```

Copy

### Use Cases[¶](#use-cases "Link to this heading")

* Real-time validation during Teradata migration
* Pre-cutover validation checks
* Post-migration verification
* Continuous validation in CI/CD pipelines
* Testing with temporary credentials

---

## Generate Validation Scripts[¶](#generate-validation-scripts "Link to this heading")

Generates SQL scripts for Teradata and Snowflake metadata extraction.

### Syntax[¶](#id1 "Link to this heading")

```
snowflake-data-validation teradata generate-validation-scripts \
  /path/to/config.yaml \
  --output-directory ./scripts
```

Copy

### Positional Arguments[¶](#positional-arguments "Link to this heading")

**`config_file`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file
* **Example:** `./configs/validation.yaml`

### Options[¶](#id2 "Link to this heading")

**`--teradata-host`** (optional)

* **Type:** String
* **Description:** Teradata server hostname (overrides config file)
* **Example:** `--teradata-host teradata.company.com`

**`--teradata-username`** (optional)

* **Type:** String
* **Description:** Teradata username (overrides config file)
* **Example:** `--teradata-username script_generator`

**`--teradata-password`** (optional)

* **Type:** String
* **Description:** Teradata password (overrides config file)
* **Example:** `--teradata-password secure_password`

**`--teradata-database`** (optional)

* **Type:** String
* **Description:** Teradata database name (overrides config file)
* **Example:** `--teradata-database analytics_db`

**`--output-directory`** (optional)

* **Type:** String (path)
* **Description:** Directory for generated scripts
* **Example:** `--output-directory ./generated_scripts`

### Example Usage[¶](#id3 "Link to this heading")

```
# Basic script generation
sdv teradata generate-validation-scripts \
  ./configs/validation.yaml

# Script generation with connection override
sdv teradata generate-validation-scripts \
  ./config.yaml \
  --teradata-host teradata.company.com \
  --teradata-username script_user \
  --teradata-password script_password \
  --output-directory ./scripts

# Script generation to specific directory
sdv teradata generate-validation-scripts \
  /opt/configs/prod_validation.yaml \
  --output-directory /data/validation_scripts

# Using full command name
snowflake-data-validation teradata generate-validation-scripts \
  ./config.yaml \
  --teradata-database production_db \
  --output-directory ./generated_scripts
```

Copy

### Output[¶](#output "Link to this heading")

The command generates SQL scripts in the specified output directory:

```
<output_directory>/
├── teradata_schema_queries.sql
├── teradata_metrics_queries.sql
├── teradata_row_queries.sql
├── snowflake_schema_queries.sql
├── snowflake_metrics_queries.sql
└── snowflake_row_queries.sql
```

Copy

### Use Cases[¶](#id4 "Link to this heading")

* Generating scripts for execution by DBAs
* Compliance requirements for query review
* Environments where direct CLI database access is restricted
* Manual execution and validation workflows
* Separating metadata extraction from validation

---

## Run Asynchronous Validation[¶](#run-asynchronous-validation "Link to this heading")

Performs validation using pre-generated metadata files without connecting to databases.

### Syntax[¶](#id5 "Link to this heading")

```
snowflake-data-validation teradata run-async-validation \
  /path/to/config.yaml \
  --output-directory ./validation_results
```

Copy

### Positional Arguments[¶](#id6 "Link to this heading")

**`config_file`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file
* **Example:** `./configs/async_validation.yaml`

### Options[¶](#id7 "Link to this heading")

**`--output-directory`** (optional)

* **Type:** String (path)
* **Description:** Directory containing metadata files generated from scripts
* **Example:** `--output-directory ./metadata_files`

### Example Usage[¶](#id8 "Link to this heading")

```
# Run async validation
sdv teradata run-async-validation \
  ./configs/async_validation.yaml

# Run async validation with specific metadata directory
sdv teradata run-async-validation \
  ./config.yaml \
  --output-directory ./validation_metadata

# Using full command name
snowflake-data-validation teradata run-async-validation \
  /opt/configs/validation.yaml \
  --output-directory /data/validation_metadata
```

Copy

### Prerequisites[¶](#prerequisites "Link to this heading")

Before running async validation:

1. Generate validation scripts using `generate-validation-scripts`
2. Execute the generated scripts on Teradata and Snowflake databases
3. Save results to CSV/metadata files
4. Ensure metadata files are available in the configured paths

### Use Cases[¶](#id9 "Link to this heading")

* Validating in environments with restricted database access
* Separating metadata extraction from validation
* Batch validation workflows
* Scheduled validation jobs
* When database connections are intermittent

---

## Get Configuration Templates[¶](#get-configuration-templates "Link to this heading")

Retrieves Teradata configuration templates.

### Syntax[¶](#id10 "Link to this heading")

```
snowflake-data-validation teradata get-configuration-files \
  --templates-directory ./teradata-templates \
  --query-templates
```

Copy

### Options[¶](#id11 "Link to this heading")

**`--templates-directory, -td`** (optional)

* **Type:** String (path)
* **Default:** Current directory
* **Description:** Directory to save template files
* **Example:** `--templates-directory ./templates`

**`--query-templates`** (optional)

* **Type:** Flag (no value required)
* **Description:** Include J2 (Jinja2) query template files for advanced customization
* **Example:** `--query-templates`

### Example Usage[¶](#id12 "Link to this heading")

```
# Get basic templates in current directory
sdv teradata get-configuration-files

# Save templates to specific directory
sdv teradata get-configuration-files \
  --templates-directory ./my-project/teradata-templates

# Include query templates for customization
sdv teradata get-configuration-files \
  --templates-directory ./templates \
  --query-templates

# Using short flags
sdv teradata get-configuration-files -td ./templates --query-templates
```

Copy

### Output Files[¶](#output-files "Link to this heading")

**Without `--query-templates` flag:**

```
<templates_directory>/
└── teradata_validation_template.yaml
```

Copy

**With `--query-templates` flag:**

```
<templates_directory>/
├── teradata_validation_template.yaml
└── query_templates/
    ├── teradata_columns_metrics_query.sql.j2
    ├── teradata_row_count_query.sql.j2
    ├── teradata_compute_md5_sql.j2
    └── snowflake_columns_metrics_query.sql.j2
```

Copy

### Use Cases[¶](#id13 "Link to this heading")

* Starting a new Teradata validation project
* Learning Teradata-specific configuration options
* Customizing validation queries for Teradata
* Creating organization-specific templates

---

## Auto-Generate Configuration File[¶](#auto-generate-configuration-file "Link to this heading")

Interactive command for Teradata configuration generation.

### Syntax[¶](#id14 "Link to this heading")

```
snowflake-data-validation teradata auto-generated-configuration-file
```

Copy

### Options[¶](#id15 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### Interactive Prompts[¶](#interactive-prompts "Link to this heading")

The command will prompt for the following information:

1. **Teradata host**

   * Hostname or IP address of Teradata server
   * Example: `teradata.company.com`
2. **Teradata username**

   * Authentication username
   * Example: `migration_user`
3. **Teradata password**

   * Authentication password (hidden input)
   * Not displayed on screen for security
4. **Teradata database**

   * Name of the database to validate
   * Example: `production_db`
5. **Output directory path**

   * Where to save validation results
   * Example: `./validation_results`

### Example Session[¶](#example-session "Link to this heading")

```
$ sdv teradata auto-generated-configuration-file

Teradata host: teradata.company.com
Teradata username: migration_user
Teradata password: ********
Teradata database: production_db
Output directory path: ./validation_results

Configuration file generated successfully: ./teradata_validation_config.yaml
```

Copy

### Generated Configuration[¶](#generated-configuration "Link to this heading")

The command generates a basic YAML configuration file:

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: ./validation_results
target_database: PRODUCTION_DB

source_connection:
  mode: credentials
  host: teradata.company.com
  username: migration_user
  password: "<hidden>"
  database: production_db

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

tables: []
```

Copy

### Next Steps After Generation[¶](#next-steps-after-generation "Link to this heading")

1. **Edit the configuration file** to add:

   * Target connection details (if not using default)
   * Tables to validate
   * Validation options
   * Column selections and mappings
2. **Add table configurations:**

   * Specify fully qualified table names
   * Configure column selections
   * Set up filtering where clauses
3. **Review Teradata-specific settings:**

   * Verify target\_database is correctly set
   * Check schema mappings if needed
4. **Test the configuration:**

   ```
   sdv teradata run-validation \
     --data-validation-config-file ./teradata_validation_config.yaml
   ```

   Copy

### Use Cases[¶](#id16 "Link to this heading")

* Quick setup for new Teradata users
* Generating baseline configurations
* Testing connectivity during setup
* Creating template configurations for teams

---

## Row Partitioning Helper[¶](#row-partitioning-helper "Link to this heading")

Interactive command to generate partitioned table configurations for large tables. This helper divides tables into smaller row partitions based on a specified column, enabling more efficient validation of large datasets.

### Syntax[¶](#id17 "Link to this heading")

```
snowflake-data-validation teradata row-partitioning-helper
```

Copy

### Options[¶](#id18 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#how-it-works "Link to this heading")

The table partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply partitioning
3. If partitioning is enabled, collects partition parameters
4. Queries the source Teradata database to determine partition boundaries
5. Generates new table configurations with `WHERE` clauses for each partition
6. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id19 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/teradata_validation.yaml`
2. **For each table in the configuration:**

   a. **Apply partitioning?** (yes/no)

   * Whether to partition this specific table
   * Default: yes

   b. **Partition column** (if partitioning)

   * Column name used to divide the table
   * Should be indexed for performance
   * Example: `transaction_id`, `created_date`

   c. **Is partition column a string type?** (yes/no)

   * Determines quoting in generated WHERE clauses
   * Default: no (numeric)

   d. **Number of partitions**

   * How many partitions to create
   * Example: `10`, `50`, `100`

### Example Session[¶](#id20 "Link to this heading")

```
$ sdv teradata row-partitioning-helper

Generate a configuration file for Teradata table partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip partitioning or specify partitioning parameters for each table.

Configuration file path: ./configs/teradata_validation.yaml

Apply partitioning for enterprise_db.fact_sales? [Y/n]: y
Write the partition column for enterprise_db.fact_sales: sale_id
Is 'sale_id' column a string type? [y/N]: n
Write the number of partitions for enterprise_db.fact_sales: 10

Apply partitioning for enterprise_db.dim_customer? [Y/n]: n

Apply partitioning for enterprise_db.transactions? [Y/n]: y
Write the partition column for enterprise_db.transactions: transaction_date
Is 'transaction_date' column a string type? [y/N]: n
Write the number of partitions for enterprise_db.transactions: 5

Table partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#generated-output "Link to this heading")

The command generates partitioned table configurations with WHERE clauses:

```
tables:
  # Original table partitioned into 10 segments
  - fully_qualified_name: enterprise_db.fact_sales
    where_clause: "sale_id >= 1 AND sale_id < 100000"
    target_where_clause: "sale_id >= 1 AND sale_id < 100000"
    # ... other table settings preserved

  - fully_qualified_name: enterprise_db.fact_sales
    where_clause: "sale_id >= 100000 AND sale_id < 200000"
    target_where_clause: "sale_id >= 100000 AND sale_id < 200000"
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: enterprise_db.dim_customer
    # ... original configuration
```

Copy

### Use Cases[¶](#id21 "Link to this heading")

* **Large table validation**: Break multi-billion row tables into manageable chunks
* **Parallel processing**: Enable concurrent validation of different partitions
* **Memory optimization**: Reduce memory footprint by processing smaller data segments
* **Incremental validation**: Validate specific data ranges independently
* **Performance tuning**: Optimize validation for tables with uneven data distribution

### Best Practices[¶](#best-practices "Link to this heading")

1. **Choose appropriate partition columns:**

   * Use indexed columns for better query performance
   * Prefer columns with sequential values (IDs, timestamps)
   * Avoid columns with highly skewed distributions
2. **Determine optimal partition count:**

   * Consider table size and available resources
   * Start with 10-20 partitions for tables with 10M+ rows
   * Increase partitions for very large tables (100M+ rows)
3. **String vs numeric columns:**

   * Numeric columns are generally more efficient
   * String columns work but may have uneven distribution
4. **After partitioning:**

   * Review generated WHERE clauses
   * Adjust partition boundaries if needed
   * Test with a subset before full validation

---

## Column Partitioning Helper[¶](#column-partitioning-helper "Link to this heading")

Interactive command to generate partitioned table configurations for wide tables with many columns. This helper divides tables into smaller column partitions, enabling more efficient validation of tables with a large number of columns.

### Syntax[¶](#id22 "Link to this heading")

```
snowflake-data-validation teradata column-partitioning-helper
```

Copy

### Options[¶](#id23 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#id24 "Link to this heading")

The column partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply column partitioning
3. If partitioning is enabled, collects the number of partitions
4. Queries the source Teradata database to retrieve all column names for the table
5. Divides the columns into the specified number of partitions
6. Generates new table configurations where each partition validates only a subset of columns
7. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id25 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/teradata_validation.yaml`
2. **For each table in the configuration:**

   a. **Apply column partitioning?** (yes/no)

   * Whether to partition this specific table by columns
   * Default: yes

   b. **Number of partitions** (if partitioning)

   * How many column partitions to create
   * Example: `3`, `5`, `10`

### Example Session[¶](#id26 "Link to this heading")

```
$ sdv teradata column-partitioning-helper

Generate a configuration file for Teradata column partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip column partitioning or specify column partitioning parameters for each table.

Configuration file path: ./configs/teradata_validation.yaml

Apply column partitioning for enterprise_db.wide_table? [Y/n]: y
Write the number of partitions for enterprise_db.wide_table: 5

Apply column partitioning for enterprise_db.small_table? [Y/n]: n

Apply column partitioning for enterprise_db.report_table? [Y/n]: y
Write the number of partitions for enterprise_db.report_table: 3

Column partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#id27 "Link to this heading")

The command generates partitioned table configurations with column subsets:

```
tables:
  # Original table with 100 columns partitioned into 5 segments (20 columns each)
  - fully_qualified_name: enterprise_db.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_a
      - column_b
      - column_c
      # ... first 20 columns alphabetically

  - fully_qualified_name: enterprise_db.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_d
      - column_e
      - column_f
      # ... next 20 columns alphabetically
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: enterprise_db.small_table
    # ... original configuration
```

Copy

### Use Cases[¶](#id28 "Link to this heading")

* **Wide table validation**: Break tables with hundreds of columns into manageable chunks
* **Memory optimization**: Reduce memory footprint by validating fewer columns at a time
* **Parallel processing**: Enable concurrent validation of different column groups
* **Targeted validation**: Validate specific column groups independently
* **Performance tuning**: Optimize validation for tables with many LOB or complex columns

### Best Practices[¶](#id29 "Link to this heading")

1. **Determine optimal partition count:**

   * Consider the total number of columns in the table
   * For tables with 50+ columns, start with 3-5 partitions
   * For tables with 100+ columns, consider 5-10 partitions
2. **Column ordering:**

   * Columns are divided alphabetically
   * Related columns may end up in different partitions
3. **After partitioning:**

   * Review generated column lists
   * Verify all required columns are included
   * Test with a subset before full validation
4. **Combine with row partitioning:**

   * For very large, wide tables, consider using both row and column partitioning
   * First partition by columns, then apply row partitioning to each column partition if needed

---

## Teradata Connection Configuration[¶](#teradata-connection-configuration "Link to this heading")

Teradata connections require specific configuration in the YAML file.

### Connection Example[¶](#connection-example "Link to this heading")

```
source_connection:
  mode: credentials
  host: "teradata.company.com"
  username: "teradata_user"
  password: "secure_password"
  database: "source_database"
```

Copy

### Connection Fields[¶](#connection-fields "Link to this heading")

**`mode`** (required)

* **Type:** String
* **Valid Values:** `credentials`
* **Description:** Connection mode for Teradata

**`host`** (required)

* **Type:** String
* **Description:** Teradata hostname or IP address
* **Examples:**

  + `"teradata.company.com"`
  + `"td-prod.internal.company.net"`
  + `"192.168.1.50"`

**`username`** (required)

* **Type:** String
* **Description:** Teradata authentication username
* **Example:** `"migration_admin"`

**`password`** (required)

* **Type:** String
* **Description:** Teradata authentication password
* **Security Note:** Consider using environment variables

**`database`** (required)

* **Type:** String
* **Description:** Teradata database name
* **Example:** `"production_database"`

### Teradata-Specific Global Configuration[¶](#teradata-specific-global-configuration "Link to this heading")

**`target_database`** (required for Teradata)

* **Type:** String
* **Description:** Target database name in Snowflake for Teradata validations
* **Example:** `target_database: PROD_DB`
* **Note:** This is required in the global configuration section, not the connection section

### Connection Examples[¶](#connection-examples "Link to this heading")

**Production Connection:**

```
source_connection:
  mode: credentials
  host: "td-prod.company.com"
  username: "prod_reader"
  password: "${TERADATA_PASSWORD}"  # From environment variable
  database: "production_db"

target_database: PROD_SNOWFLAKE_DB
```

Copy

**Development Connection:**

```
source_connection:
  mode: credentials
  host: "td-dev.company.local"
  username: "dev_user"
  password: "dev_password"
  database: "dev_database"

target_database: DEV_SNOWFLAKE_DB
```

Copy

**Multi-Database Setup:**

```
source_connection:
  mode: credentials
  host: "teradata.company.com"
  username: "migration_user"
  password: "secure_password"
  database: "primary_db"

target_database: ENTERPRISE_DATA_DB

database_mappings:
  primary_db: ENTERPRISE_DATA_DB
  secondary_db: ANALYTICS_DB
```

Copy

---

## Complete Teradata Examples[¶](#complete-teradata-examples "Link to this heading")

### Example 1: Basic Teradata Configuration[¶](#example-1-basic-teradata-configuration "Link to this heading")

```
# Global configuration
source_platform: Teradata
target_platform: Snowflake
output_directory_path: ./validation_results
max_threads: auto
target_database: PROD_DB

# Source connection
source_connection:
  mode: credentials
  host: teradata.company.com
  username: teradata_user
  password: teradata_password
  database: prod_db

# Target connection
target_connection:
  mode: default

# Validation configuration
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

# Schema mappings
schema_mappings:
  prod_db: PUBLIC

# Tables configuration
tables:
  - fully_qualified_name: prod_db.sales_data
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - transaction_id

  - fully_qualified_name: prod_db.customer_master
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - credit_card
```

Copy

### Example 2: Teradata Large-Scale Migration[¶](#example-2-teradata-large-scale-migration "Link to this heading")

```
# Global configuration
source_platform: Teradata
target_platform: Snowflake
output_directory_path: /opt/validation/results
max_threads: 16
target_database: PROD_SNOWFLAKE

# Source connection
source_connection:
  mode: credentials
  host: td-prod.company.com
  username: migration_admin
  password: secure_password
  database: enterprise_db

# Target connection
target_connection:
  mode: name
  name: snowflake_enterprise

# Validation configuration
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 200
  exclude_metrics: false

# Comparison configuration
comparison_configuration:
  tolerance: 0.01

# Logging configuration
logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: DEBUG

# Schema mappings
schema_mappings:
  enterprise_db: PUBLIC

# Tables configuration
tables:
  - fully_qualified_name: enterprise_db.fact_sales
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - sale_id
      - customer_id
      - product_id
      - sale_amount
      - sale_date
    index_column_list:
      - sale_id
    chunk_number: 50
    max_failed_rows_number: 500

  - fully_qualified_name: enterprise_db.dim_customer
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_notes
      - audit_fields
    where_clause: "status = 'ACTIVE'"
    target_where_clause: "status = 'ACTIVE'"
    column_mappings:
      cust_key: customer_key
      cust_name: customer_name
```

Copy

### Example 3: Teradata Multi-Schema Validation[¶](#example-3-teradata-multi-schema-validation "Link to this heading")

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: /data/validation/multi_schema
max_threads: 24
target_database: MULTI_SCHEMA_DB

source_connection:
  mode: credentials
  host: teradata.company.com
  username: multi_schema_user
  password: password123
  database: main_db

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

comparison_configuration:
  tolerance: 0.005

schema_mappings:
  sales_schema: SALES
  finance_schema: FINANCE
  hr_schema: HUMAN_RESOURCES

tables:
  # Sales schema tables
  - fully_qualified_name: main_db.sales_schema.orders
    target_schema: SALES
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id

  - fully_qualified_name: main_db.sales_schema.customers
    target_schema: SALES
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - customer_id

  # Finance schema tables
  - fully_qualified_name: main_db.finance_schema.transactions
    target_schema: FINANCE
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_ref_number
    index_column_list:
      - transaction_id
    where_clause: "fiscal_year >= 2024"
    target_where_clause: "fiscal_year >= 2024"

  # HR schema tables
  - fully_qualified_name: main_db.hr_schema.employees
    target_schema: HUMAN_RESOURCES
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - salary
      - bank_account
    index_column_list:
      - employee_id
```

Copy

---

## Troubleshooting Teradata Connections[¶](#troubleshooting-teradata-connections "Link to this heading")

### Issue: Connection Timeout[¶](#issue-connection-timeout "Link to this heading")

**Symptom:**

```
Connection timeout: Unable to connect to Teradata
```

Copy

**Solutions:**

1. Verify the host and network connectivity:

   ```
   telnet teradata.company.com 1025
   ```

   Copy
2. Check firewall rules allow Teradata connections
3. Verify Teradata server is running
4. Test connection with Teradata SQL Assistant or other client tools

### Issue: Authentication Failed[¶](#issue-authentication-failed "Link to this heading")

**Symptom:**

```
Authentication failed for user 'username'
```

Copy

**Solutions:**

1. Verify credentials are correct
2. Check user has necessary permissions:

   ```
   -- Grant read permissions
   GRANT SELECT ON database_name TO migration_user;
   ```

   Copy
3. Verify user account is not locked
4. Check password hasn’t expired

### Issue: Database Not Found[¶](#issue-database-not-found "Link to this heading")

**Symptom:**

```
Database 'database_name' does not exist
```

Copy

**Solutions:**

1. Verify database name is correct (case-sensitive)
2. Check user has access to the database:

   ```
   DATABASE database_name;
   SHOW TABLES;
   ```

   Copy
3. Ensure database exists and is accessible

### Issue: Target Database Configuration Missing[¶](#issue-target-database-configuration-missing "Link to this heading")

**Symptom:**

```
target_database configuration is required for Teradata validations
```

Copy

**Solution:**

Add `target_database` to global configuration:

```
source_platform: Teradata
target_platform: Snowflake
target_database: TARGET_DB_NAME  # Add this line
```

Copy

### Issue: Schema Mapping Errors[¶](#issue-schema-mapping-errors "Link to this heading")

**Symptom:**

```
Schema not found in target
```

Copy

**Solution:**

Add schema mappings in configuration:

```
schema_mappings:
  source_schema: TARGET_SCHEMA
  prod_db: PUBLIC
```

Copy

---

## Best Practices for Teradata[¶](#best-practices-for-teradata "Link to this heading")

### Configuration[¶](#configuration "Link to this heading")

1. **Always specify target\_database:**

   ```
   target_database: SNOWFLAKE_DB_NAME
   ```

   Copy
2. **Use schema mappings:**

   ```
   schema_mappings:
     teradata_schema: snowflake_schema
   ```

   Copy
3. **Handle case sensitivity:**

   ```
   tables:
     - fully_qualified_name: db.schema.TABLE_NAME
       is_case_sensitive: true
   ```

   Copy

### Security[¶](#security "Link to this heading")

1. **Use environment variables for passwords:**

   ```
   source_connection:
     password: "${TERADATA_PASSWORD}"
   ```

   Copy
2. **Use read-only accounts:**

   ```
   CREATE USER migration_reader AS PASSWORD = secure_password;
   GRANT SELECT ON database_name TO migration_reader;
   ```

   Copy
3. **Restrict column access for sensitive data:**

   ```
   tables:
     - fully_qualified_name: sensitive_table
       use_column_selection_as_exclude_list: true
       column_selection_list:
         - ssn
         - credit_card
         - salary
   ```

   Copy

### Performance[¶](#performance "Link to this heading")

1. **Enable chunking for large tables:**

   ```
   tables:
     - fully_qualified_name: large_table
       chunk_number: 100
   ```

   Copy
2. **Use WHERE clauses to filter data:**

   ```
   tables:
     - fully_qualified_name: transactions
       where_clause: "transaction_date >= DATE '2024-01-01'"
   ```

   Copy
3. **Optimize thread count:**

   ```
   max_threads: 16  # Adjust based on Teradata server capacity
   ```

   Copy
4. **Exclude unnecessary metrics for very large tables:**

   ```
   validation_configuration:
     exclude_metrics: true  # Excludes avg, sum, stddev, variance
   ```

   Copy

### Data Quality[¶](#data-quality "Link to this heading")

1. **Start with schema validation:**

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: false
     row_validation: false
   ```

   Copy
2. **Progress to metrics validation:**

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: true
     row_validation: false
   ```

   Copy
3. **Enable row validation for critical tables:**

   ```
   tables:
     - fully_qualified_name: critical_fact_table
       # Row validation will be performed

   validation_configuration:
     row_validation: true
   ```

   Copy

---

## See Also[¶](#see-also "Link to this heading")

* [Main CLI Usage Guide](CLI_USAGE_GUIDE)
* [SQL Server Commands Reference](sqlserver_commands)
* [Redshift Commands Reference](redshift_commands)
* [Configuration Examples](CONFIGURATION_EXAMPLES)
* [Quick Reference Guide](CLI_QUICK_REFERENCE)

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

1. [Overview](#overview)
2. [Command Structure](#command-structure)
3. [Run Synchronous Validation](#run-synchronous-validation)
4. [Generate Validation Scripts](#generate-validation-scripts)
5. [Run Asynchronous Validation](#run-asynchronous-validation)
6. [Get Configuration Templates](#get-configuration-templates)
7. [Auto-Generate Configuration File](#auto-generate-configuration-file)
8. [Row Partitioning Helper](#row-partitioning-helper)
9. [Column Partitioning Helper](#column-partitioning-helper)
10. [Teradata Connection Configuration](#teradata-connection-configuration)
11. [Complete Teradata Examples](#complete-teradata-examples)
12. [Troubleshooting Teradata Connections](#troubleshooting-teradata-connections)
13. [Best Practices for Teradata](#best-practices-for-teradata)
14. [See Also](#see-also)