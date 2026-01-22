---
auto_generated: true
description: This page provides comprehensive reference documentation for Amazon Redshift-specific
  commands in the Snowflake Data Validation CLI. For SQL Server commands, see SQL
  Server Commands Reference. For Ter
last_scraped: '2026-01-14T16:52:14.083184+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/redshift_commands
title: Amazon Redshift Commands Reference | Snowflake Documentation
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)[Usage Guide](CLI_USAGE_GUIDE.md)Redshift commands

# Amazon Redshift Commands Reference[¶](#amazon-redshift-commands-reference "Link to this heading")

## Overview[¶](#overview "Link to this heading")

This page provides comprehensive reference documentation for Amazon Redshift-specific commands in the Snowflake Data Validation CLI. For SQL Server commands, see [SQL Server Commands Reference](sqlserver_commands). For Teradata commands, see [Teradata Commands Reference](teradata_commands).

---

## Command Structure[¶](#command-structure "Link to this heading")

All Amazon Redshift commands follow this consistent structure:

```
snowflake-data-validation redshift <command> [options]

# Or use the shorter alias
sdv redshift <command> [options]
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

Validates data between Amazon Redshift and Snowflake in real-time.

### Syntax[¶](#syntax "Link to this heading")

```
snowflake-data-validation redshift run-validation \
  --data-validation-config-file /path/to/config.yaml \
  --log-level INFO
```

Copy

### Options[¶](#options "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file containing validation settings
* **Example:** `--data-validation-config-file ./configs/redshift_validation.yaml`

**`--log-level, -ll`** (optional)

* **Type:** String
* **Valid Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Default:** INFO
* **Description:** Logging level for validation execution
* **Example:** `--log-level DEBUG`

### Example Usage[¶](#example-usage "Link to this heading")

```
# Basic validation
sdv redshift run-validation \
  --data-validation-config-file ./configs/redshift_validation.yaml

# Validation with debug logging
sdv redshift run-validation \
  --data-validation-config-file ./configs/redshift_validation.yaml \
  --log-level DEBUG

# Using full command name
snowflake-data-validation redshift run-validation \
  -dvf /opt/validations/prod_config.yaml \
  -ll INFO
```

Copy

### Use Cases[¶](#use-cases "Link to this heading")

* Real-time validation during Redshift migration
* Pre-cutover validation checks
* Post-migration verification
* Continuous validation in CI/CD pipelines
* Data lake migration validation

---

## Run Asynchronous Validation[¶](#run-asynchronous-validation "Link to this heading")

Performs validation using pre-generated metadata files without connecting to databases.

### Syntax[¶](#id1 "Link to this heading")

```
snowflake-data-validation redshift run-async-validation \
  --data-validation-config-file /path/to/config.yaml \
  --log-level INFO
```

Copy

### Options[¶](#id2 "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file
* **Note:** Configuration must specify paths to pre-generated metadata files

**`--log-level, -ll`** (optional)

* **Type:** String
* **Valid Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Default:** INFO
* **Description:** Logging level for validation execution
* **Example:** `--log-level DEBUG`

### Example Usage[¶](#id3 "Link to this heading")

```
# Run async validation
sdv redshift run-async-validation \
  --data-validation-config-file ./configs/async_validation.yaml

# Async validation with debug logging
sdv redshift run-async-validation \
  --data-validation-config-file ./configs/async_validation.yaml \
  --log-level DEBUG

# Using full command name
snowflake-data-validation redshift run-async-validation \
  -dvf /data/validations/async_config.yaml \
  -ll INFO
```

Copy

### Prerequisites[¶](#prerequisites "Link to this heading")

Before running async validation:

1. Generate validation scripts using `generate-validation-scripts`
2. Execute the generated scripts on Redshift and Snowflake databases
3. Save results to CSV/metadata files
4. Ensure metadata files are available in the configured paths

### Use Cases[¶](#id4 "Link to this heading")

* Validating in environments with restricted database access
* Separating metadata extraction from validation
* Batch validation workflows
* Scheduled validation jobs
* When database connections are intermittent

---

## Generate Validation Scripts[¶](#generate-validation-scripts "Link to this heading")

Generates SQL scripts for Redshift and Snowflake metadata extraction.

### Syntax[¶](#id5 "Link to this heading")

```
snowflake-data-validation redshift generate-validation-scripts \
  --data-validation-config-file /path/to/config.yaml \
  --log-level DEBUG
```

Copy

### Options[¶](#id6 "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file

**`--log-level, -ll`** (optional)

* **Type:** String
* **Valid Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Default:** INFO
* **Description:** Logging level for script generation
* **Example:** `--log-level DEBUG`

### Example Usage[¶](#id7 "Link to this heading")

```
# Generate scripts
sdv redshift generate-validation-scripts \
  --data-validation-config-file ./configs/validation.yaml

# Generate scripts with debug logging
sdv redshift generate-validation-scripts \
  --data-validation-config-file ./configs/validation.yaml \
  --log-level DEBUG

# Using full command name
snowflake-data-validation redshift generate-validation-scripts \
  -dvf /opt/configs/script_generation.yaml \
  -ll INFO
```

Copy

### Output[¶](#output "Link to this heading")

The command generates SQL scripts in the output directory configured in your YAML file:

```
<output_directory>/
├── redshift_schema_queries.sql
├── redshift_metrics_queries.sql
├── redshift_row_queries.sql
├── snowflake_schema_queries.sql
├── snowflake_metrics_queries.sql
└── snowflake_row_queries.sql
```

Copy

### Use Cases[¶](#id8 "Link to this heading")

* Generating scripts for execution by DBAs
* Compliance requirements for query review
* Environments where direct CLI database access is restricted
* Manual execution and validation workflows
* Separating metadata extraction from validation

---

## Get Configuration Templates[¶](#get-configuration-templates "Link to this heading")

Retrieves Redshift configuration templates.

### Syntax[¶](#id9 "Link to this heading")

```
snowflake-data-validation redshift get-configuration-files \
  --templates-directory ./redshift-templates \
  --query-templates
```

Copy

### Options[¶](#id10 "Link to this heading")

**`--templates-directory, -td`** (optional)

* **Type:** String (path)
* **Default:** Current directory
* **Description:** Directory to save template files
* **Example:** `--templates-directory ./templates`

**`--query-templates`** (optional)

* **Type:** Flag (no value required)
* **Description:** Include J2 (Jinja2) query template files for advanced customization
* **Example:** `--query-templates`

### Example Usage[¶](#id11 "Link to this heading")

```
# Get basic templates in current directory
sdv redshift get-configuration-files

# Save templates to specific directory
sdv redshift get-configuration-files \
  --templates-directory ./my-project/redshift-templates

# Include query templates for customization
sdv redshift get-configuration-files \
  --templates-directory ./templates \
  --query-templates

# Using short flags
sdv redshift get-configuration-files -td ./templates --query-templates
```

Copy

### Output Files[¶](#output-files "Link to this heading")

**Without `--query-templates` flag:**

```
<templates_directory>/
└── redshift_validation_template.yaml
```

Copy

**With `--query-templates` flag:**

```
<templates_directory>/
├── redshift_validation_template.yaml
└── query_templates/
    ├── redshift_columns_metrics_query.sql.j2
    ├── redshift_row_count_query.sql.j2
    ├── redshift_compute_md5_sql.j2
    └── snowflake_columns_metrics_query.sql.j2
```

Copy

### Use Cases[¶](#id12 "Link to this heading")

* Starting a new Redshift validation project
* Learning Redshift-specific configuration options
* Customizing validation queries for Redshift
* Creating organization-specific templates

---

## Auto-Generate Configuration File[¶](#auto-generate-configuration-file "Link to this heading")

Interactive command for Redshift configuration generation.

### Syntax[¶](#id13 "Link to this heading")

```
snowflake-data-validation redshift auto-generated-configuration-file
```

Copy

### Options[¶](#id14 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### Interactive Prompts[¶](#interactive-prompts "Link to this heading")

The command will prompt for the following information:

1. **Redshift host**

   * Hostname/endpoint of Redshift cluster
   * Example: `redshift-cluster.region.redshift.amazonaws.com`
2. **Redshift port** (default: 5439)

   * Port number for Redshift connection
   * Press Enter to accept default
3. **Redshift username**

   * Authentication username
   * Example: `migration_user`
4. **Redshift password**

   * Authentication password (hidden input)
   * Not displayed on screen for security
5. **Redshift database**

   * Name of the database to validate
   * Example: `analytics_db`
6. **Redshift schema**

   * Schema name within the database
   * Example: `public`
7. **Output directory path**

   * Where to save validation results
   * Example: `./validation_results`

### Example Session[¶](#example-session "Link to this heading")

```
$ sdv redshift auto-generated-configuration-file

Redshift host: redshift-cluster.us-east-1.redshift.amazonaws.com
Redshift port [5439]: 
Redshift username: migration_user
Redshift password: ********
Redshift database: analytics_db
Redshift schema: public
Output directory path: ./validation_results

Configuration file generated successfully: ./redshift_validation_config.yaml
```

Copy

### Generated Configuration[¶](#generated-configuration "Link to this heading")

The command generates a basic YAML configuration file:

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: ./validation_results

source_connection:
  mode: credentials
  host: redshift-cluster.us-east-1.redshift.amazonaws.com
  port: 5439
  username: migration_user
  password: "<hidden>"
  database: analytics_db

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
2. **Review security settings:**

   * Consider using environment variables for passwords
   * Verify IAM authentication if applicable
3. **Add table configurations:**

   * Specify fully qualified table names
   * Configure column selections
   * Set up filtering where clauses
4. **Test the configuration:**

   ```
   sdv redshift run-validation \
     --data-validation-config-file ./redshift_validation_config.yaml
   ```

   Copy

### Use Cases[¶](#id15 "Link to this heading")

* Quick setup for new Redshift users
* Generating baseline configurations
* Testing connectivity during setup
* Creating template configurations for teams

---

## Row Partitioning Helper[¶](#row-partitioning-helper "Link to this heading")

Interactive command to generate partitioned table configurations for large tables. This helper divides tables into smaller row partitions based on a specified column, enabling more efficient validation of large datasets.

### Syntax[¶](#id16 "Link to this heading")

```
snowflake-data-validation redshift row-partitioning-helper
```

Copy

### Options[¶](#id17 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#how-it-works "Link to this heading")

The table partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply partitioning
3. If partitioning is enabled, collects partition parameters
4. Queries the source Redshift database to determine partition boundaries
5. Generates new table configurations with `WHERE` clauses for each partition
6. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id18 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/redshift_validation.yaml`
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

### Example Session[¶](#id19 "Link to this heading")

```
$ sdv redshift row-partitioning-helper

Generate a configuration file for Redshift table partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip partitioning or specify partitioning parameters for each table.

Configuration file path: ./configs/redshift_validation.yaml

Apply partitioning for public.fact_sales? [Y/n]: y
Write the partition column for public.fact_sales: sale_id
Is 'sale_id' column a string type? [y/N]: n
Write the number of partitions for public.fact_sales: 10

Apply partitioning for public.dim_customer? [Y/n]: n

Apply partitioning for public.transactions? [Y/n]: y
Write the partition column for public.transactions: transaction_date
Is 'transaction_date' column a string type? [y/N]: n
Write the number of partitions for public.transactions: 5

Table partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#generated-output "Link to this heading")

The command generates partitioned table configurations with WHERE clauses:

```
tables:
  # Original table partitioned into 10 segments
  - fully_qualified_name: public.fact_sales
    where_clause: "sale_id >= 1 AND sale_id < 100000"
    target_where_clause: "sale_id >= 1 AND sale_id < 100000"
    # ... other table settings preserved

  - fully_qualified_name: public.fact_sales
    where_clause: "sale_id >= 100000 AND sale_id < 200000"
    target_where_clause: "sale_id >= 100000 AND sale_id < 200000"
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: public.dim_customer
    # ... original configuration
```

Copy

### Use Cases[¶](#id20 "Link to this heading")

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

### Syntax[¶](#id21 "Link to this heading")

```
snowflake-data-validation redshift column-partitioning-helper
```

Copy

### Options[¶](#id22 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#id23 "Link to this heading")

The column partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply column partitioning
3. If partitioning is enabled, collects the number of partitions
4. Queries the source Redshift database to retrieve all column names for the table
5. Divides the columns into the specified number of partitions
6. Generates new table configurations where each partition validates only a subset of columns
7. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id24 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/redshift_validation.yaml`
2. **For each table in the configuration:**

   a. **Apply column partitioning?** (yes/no)

   * Whether to partition this specific table by columns
   * Default: yes

   b. **Number of partitions** (if partitioning)

   * How many column partitions to create
   * Example: `3`, `5`, `10`

### Example Session[¶](#id25 "Link to this heading")

```
$ sdv redshift column-partitioning-helper

Generate a configuration file for Redshift column partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip column partitioning or specify column partitioning parameters for each table.

Configuration file path: ./configs/redshift_validation.yaml

Apply column partitioning for public.wide_table? [Y/n]: y
Write the number of partitions for public.wide_table: 5

Apply column partitioning for public.small_table? [Y/n]: n

Apply column partitioning for public.report_table? [Y/n]: y
Write the number of partitions for public.report_table: 3

Column partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#id26 "Link to this heading")

The command generates partitioned table configurations with column subsets:

```
tables:
  # Original table with 100 columns partitioned into 5 segments (20 columns each)
  - fully_qualified_name: public.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_a
      - column_b
      - column_c
      # ... first 20 columns alphabetically

  - fully_qualified_name: public.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_d
      - column_e
      - column_f
      # ... next 20 columns alphabetically
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: public.small_table
    # ... original configuration
```

Copy

### Use Cases[¶](#id27 "Link to this heading")

* **Wide table validation**: Break tables with hundreds of columns into manageable chunks
* **Memory optimization**: Reduce memory footprint by validating fewer columns at a time
* **Parallel processing**: Enable concurrent validation of different column groups
* **Targeted validation**: Validate specific column groups independently
* **Performance tuning**: Optimize validation for tables with many LOB or complex columns

### Best Practices[¶](#id28 "Link to this heading")

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

## Amazon Redshift Connection Configuration[¶](#amazon-redshift-connection-configuration "Link to this heading")

Redshift connections require specific configuration in the YAML file.

### Connection Example[¶](#connection-example "Link to this heading")

```
source_connection:
  mode: credentials
  host: "redshift-cluster.region.redshift.amazonaws.com"
  port: 5439
  username: "redshift_user"
  password: "secure_password"
  database: "source_database"
```

Copy

### Connection Fields[¶](#connection-fields "Link to this heading")

**`mode`** (required)

* **Type:** String
* **Valid Values:** `credentials`
* **Description:** Connection mode for Redshift

**`host`** (required)

* **Type:** String
* **Description:** Redshift cluster endpoint
* **Format:** `<cluster-name>.<cluster-id>.<region>.redshift.amazonaws.com`
* **Examples:**

  + `"redshift-cluster-1.abc123.us-east-1.redshift.amazonaws.com"`
  + `"analytics-cluster.xyz789.eu-west-1.redshift.amazonaws.com"`
  + `"data-warehouse.def456.ap-southeast-1.redshift.amazonaws.com"`

**`port`** (required)

* **Type:** Integer
* **Default:** 5439
* **Description:** Redshift port number
* **Note:** Use the port configured for your Redshift cluster

**`username`** (required)

* **Type:** String
* **Description:** Redshift authentication username
* **Example:** `"migration_admin"`

**`password`** (required)

* **Type:** String
* **Description:** Redshift authentication password
* **Security Note:** Consider using environment variables or IAM authentication

**`database`** (required)

* **Type:** String
* **Description:** Redshift database name
* **Example:** `"analytics_database"`

### Connection Examples[¶](#connection-examples "Link to this heading")

**Production Connection:**

```
source_connection:
  mode: credentials
  host: "prod-cluster.abc123.us-east-1.redshift.amazonaws.com"
  port: 5439
  username: "prod_reader"
  password: "${REDSHIFT_PASSWORD}"  # From environment variable
  database: "production_db"
```

Copy

**Development Connection:**

```
source_connection:
  mode: credentials
  host: "dev-cluster.xyz789.us-west-2.redshift.amazonaws.com"
  port: 5439
  username: "dev_user"
  password: "dev_password"
  database: "dev_database"
```

Copy

**Data Lake Migration Connection:**

```
source_connection:
  mode: credentials
  host: "datalake-cluster.def456.us-east-1.redshift.amazonaws.com"
  port: 5439
  username: "migration_user"
  password: "${AWS_REDSHIFT_PASSWORD}"
  database: "datalake_db"
```

Copy

---

## Complete Amazon Redshift Examples[¶](#complete-amazon-redshift-examples "Link to this heading")

### Example 1: Basic Redshift Configuration[¶](#example-1-basic-redshift-configuration "Link to this heading")

```
# Global configuration
source_platform: Redshift
target_platform: Snowflake
output_directory_path: ./validation_results
max_threads: auto

# Source connection
source_connection:
  mode: credentials
  host: redshift-cluster.us-east-1.redshift.amazonaws.com
  port: 5439
  username: redshift_user
  password: redshift_password
  database: analytics_db

# Target connection
target_connection:
  mode: name
  name: snowflake_analytics

# Validation configuration
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

# Tables to validate
tables:
  - fully_qualified_name: public.customers
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - customer_id

  - fully_qualified_name: public.orders
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_notes
      - audit_log
```

Copy

### Example 2: Redshift Data Lake Migration[¶](#example-2-redshift-data-lake-migration "Link to this heading")

```
# Global configuration
source_platform: Redshift
target_platform: Snowflake
output_directory_path: /data/validation/redshift_migration
max_threads: 16

# Source connection
source_connection:
  mode: credentials
  host: redshift-cluster.us-east-1.redshift.amazonaws.com
  port: 5439
  username: redshift_admin
  password: redshift_secure_password
  database: analytics_db

# Target connection
target_connection:
  mode: name
  name: snowflake_analytics

# Validation configuration
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 200
  exclude_metrics: false

# Comparison configuration
comparison_configuration:
  tolerance: 0.02

# Logging configuration
logging_configuration:
  level: INFO
  console_level: ERROR
  file_level: DEBUG

# Database mappings
database_mappings:
  analytics_db: ANALYTICS_PROD

# Schema mappings
schema_mappings:
  public: PUBLIC
  staging: STAGING

# Tables configuration
tables:
  # Large fact table with chunking
  - fully_qualified_name: public.fact_sales
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - sale_id
    chunk_number: 50
    max_failed_rows_number: 500

  # Dimension table with column mappings
  - fully_qualified_name: public.dim_customer
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - customer_key
      - customer_name
      - email
      - phone
      - address
    column_mappings:
      customer_key: cust_key
      customer_name: name
    is_case_sensitive: false

  # Filtered validation
  - fully_qualified_name: staging.incremental_load
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - load_timestamp
      - etl_batch_id
    where_clause: "load_date >= CURRENT_DATE - 7"
    target_where_clause: "load_date >= CURRENT_DATE - 7"
    chunk_number: 10
```

Copy

### Example 3: Redshift with Complex Filtering[¶](#example-3-redshift-with-complex-filtering "Link to this heading")

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: /opt/validation/redshift
max_threads: 24

source_connection:
  mode: credentials
  host: complex-cluster.us-west-2.redshift.amazonaws.com
  port: 5439
  username: validation_user
  password: secure_password
  database: enterprise_db

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 150

comparison_configuration:
  tolerance: 0.01

logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: DEBUG

schema_mappings:
  public: PUBLIC

tables:
  # Time-based filtering
  - fully_qualified_name: public.transactions
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - transaction_id
      - customer_id
      - amount
      - transaction_date
      - status
    index_column_list:
      - transaction_id
    where_clause: "transaction_date >= '2024-01-01' AND status IN ('COMPLETED', 'PENDING')"
    target_where_clause: "transaction_date >= '2024-01-01' AND status IN ('COMPLETED', 'PENDING')"
    chunk_number: 30

  # Complex filtering with multiple conditions
  - fully_qualified_name: public.customer_activity
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_score
      - risk_assessment
    where_clause: "last_activity_date >= DATEADD(month, -6, CURRENT_DATE) AND account_status = 'ACTIVE' AND total_purchases > 100"
    target_where_clause: "last_activity_date >= DATEADD(month, -6, CURRENT_DATE) AND account_status = 'ACTIVE' AND total_purchases > 100"
    index_column_list:
      - customer_id
    chunk_number: 20
    max_failed_rows_number: 100

  # Regional filtering
  - fully_qualified_name: public.sales_by_region
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    where_clause: "region IN ('US-EAST', 'US-WEST', 'EU') AND sale_date >= '2024-01-01'"
    target_where_clause: "region IN ('US-EAST', 'US-WEST', 'EU') AND sale_date >= '2024-01-01'"
    index_column_list:
      - sale_id
      - region
```

Copy

---

## Troubleshooting Redshift Connections[¶](#troubleshooting-redshift-connections "Link to this heading")

### Issue: Connection Timeout[¶](#issue-connection-timeout "Link to this heading")

**Symptom:**

```
Connection timeout: Unable to connect to Redshift cluster
```

Copy

**Solutions:**

1. Verify the cluster endpoint and port:

   ```
   telnet redshift-cluster.region.redshift.amazonaws.com 5439
   ```

   Copy
2. Check VPC security groups allow inbound connections on port 5439
3. Verify the cluster is publicly accessible (if connecting from outside VPC)
4. Check route tables and network ACLs
5. Verify the cluster is in “available” state in AWS console

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
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO migration_user;
   ```

   Copy
3. Verify user account exists:

   ```
   SELECT usename FROM pg_user WHERE usename = 'migration_user';
   ```

   Copy
4. Check if password has expired or needs to be reset

### Issue: Database Not Found[¶](#issue-database-not-found "Link to this heading")

**Symptom:**

```
Database 'database_name' does not exist
```

Copy

**Solutions:**

1. Verify database name is correct (case-sensitive)
2. List available databases:

   ```
   SELECT datname FROM pg_database;
   ```

   Copy
3. Ensure user has access to the database

### Issue: SSL/TLS Certificate Errors[¶](#issue-ssl-tls-certificate-errors "Link to this heading")

**Symptom:**

```
SSL certificate verification failed
```

Copy

**Solutions:**

1. Verify SSL is required for the cluster
2. Check AWS Redshift SSL/TLS settings
3. Ensure you’re using the correct endpoint (not VPC endpoint)

### Issue: Network/VPC Configuration[¶](#issue-network-vpc-configuration "Link to this heading")

**Symptom:**

```
Connection refused or network unreachable
```

Copy

**Solutions:**

1. **Check cluster publicly accessible setting:**

   * In AWS Console, verify “Publicly accessible” is enabled if connecting externally
2. **Verify VPC security group rules:**

   * Inbound rule: Type = Custom TCP, Port = 5439, Source = Your IP
3. **Check VPC route table:**

   * Ensure proper routing to internet gateway (for public access)
4. **Verify VPC Network ACLs:**

   * Allow inbound/outbound traffic on port 5439

---

## Best Practices for Amazon Redshift[¶](#best-practices-for-amazon-redshift "Link to this heading")

### Security[¶](#security "Link to this heading")

1. **Use IAM authentication when possible:**

   ```
   # Note: IAM authentication setup requires additional AWS configuration
   source_connection:
     mode: credentials
     host: "cluster.region.redshift.amazonaws.com"
     # Use temporary credentials from IAM
   ```

   Copy
2. **Store passwords securely:**

   ```
   source_connection:
     password: "${REDSHIFT_PASSWORD}"  # From environment variable
   ```

   Copy
3. **Use read-only accounts:**

   ```
   CREATE USER migration_reader WITH PASSWORD 'secure_password';
   GRANT USAGE ON SCHEMA public TO migration_reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO migration_reader;
   ```

   Copy
4. **Restrict VPC access:**

   * Configure security groups to allow access only from specific IPs
   * Use VPC endpoints for internal AWS connectivity

### Performance[¶](#performance "Link to this heading")

1. **Enable chunking for large tables:**

   ```
   tables:
     - fully_qualified_name: large_table
       chunk_number: 50
   ```

   Copy
2. **Use WHERE clauses to filter data:**

   ```
   tables:
     - fully_qualified_name: transactions
       where_clause: "transaction_date >= CURRENT_DATE - 30"
   ```

   Copy
3. **Optimize thread count:**

   ```
   max_threads: 16  # Adjust based on cluster size
   ```

   Copy
4. **Consider cluster size and workload:**

   * Run validations during off-peak hours
   * Monitor cluster performance during validation

### Data Quality[¶](#data-quality "Link to this heading")

1. **Handle distribution and sort keys:**

   * Be aware that Redshift distribution/sort keys may affect data ordering
   * Use appropriate index columns that match distribution keys
2. **Start with schema validation:**

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: false
     row_validation: false
   ```

   Copy
3. **Progress to metrics validation:**

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: true
     row_validation: false
   ```

   Copy
4. **Enable row validation selectively:**

   ```
   validation_configuration:
     row_validation: true

   tables:
     - fully_qualified_name: critical_fact_table
       # Row validation enabled for this table
   ```

   Copy

### AWS-Specific Considerations[¶](#aws-specific-considerations "Link to this heading")

1. **Monitor cluster performance:**

   * Use AWS CloudWatch metrics during validation
   * Monitor query performance and WLM queues
2. **Consider cluster maintenance windows:**

   * Avoid running validations during maintenance windows
   * Check cluster status before starting validation
3. **Use appropriate cluster endpoints:**

   * Use cluster endpoint for direct connections
   * Use VPC endpoint for internal AWS connectivity
4. **Handle AWS region-specific configurations:**

   ```
   source_connection:
     host: "cluster.us-east-1.redshift.amazonaws.com"  # Specify correct region
   ```

   Copy

---

## See Also[¶](#see-also "Link to this heading")

* [Main CLI Usage Guide](CLI_USAGE_GUIDE)
* [SQL Server Commands Reference](sqlserver_commands)
* [Teradata Commands Reference](teradata_commands)
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
4. [Run Asynchronous Validation](#run-asynchronous-validation)
5. [Generate Validation Scripts](#generate-validation-scripts)
6. [Get Configuration Templates](#get-configuration-templates)
7. [Auto-Generate Configuration File](#auto-generate-configuration-file)
8. [Row Partitioning Helper](#row-partitioning-helper)
9. [Column Partitioning Helper](#column-partitioning-helper)
10. [Amazon Redshift Connection Configuration](#amazon-redshift-connection-configuration)
11. [Complete Amazon Redshift Examples](#complete-amazon-redshift-examples)
12. [Troubleshooting Redshift Connections](#troubleshooting-redshift-connections)
13. [Best Practices for Amazon Redshift](#best-practices-for-amazon-redshift)
14. [See Also](#see-also)