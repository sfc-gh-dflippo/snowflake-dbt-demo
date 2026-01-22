---
auto_generated: true
description: This page provides comprehensive reference documentation for SQL Server-specific
  commands in the Snowflake Data Validation CLI. For Teradata commands, see Teradata
  Commands Reference. For Amazon Redsh
last_scraped: '2026-01-14T16:55:07.898749+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/sqlserver_commands.html
title: SQL Server Commands Reference | Snowflake Documentation
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)[Usage Guide](CLI_USAGE_GUIDE.md)SQLServer commands

# SQL Server Commands Reference[¶](#sql-server-commands-reference "Link to this heading")

## Overview[¶](#overview "Link to this heading")

This page provides comprehensive reference documentation for SQL Server-specific commands in the Snowflake Data Validation CLI. For Teradata commands, see [Teradata Commands Reference](teradata_commands). For Amazon Redshift commands, see [Redshift Commands Reference](redshift_commands).

---

## Command Structure[¶](#command-structure "Link to this heading")

All SQL Server commands follow this consistent structure:

```
snowflake-data-validation sqlserver <command> [options]

# Or use the shorter alias
sdv sqlserver <command> [options]
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

Validates data between SQL Server and Snowflake in real-time.

### Syntax[¶](#syntax "Link to this heading")

```
snowflake-data-validation sqlserver run-validation \
  --data-validation-config-file /path/to/config.yaml \
  --log-level INFO
```

Copy

### Options[¶](#options "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file containing validation settings
* **Example:** `--data-validation-config-file ./configs/sqlserver_validation.yaml`

**`--log-level, -ll`** (optional)

* **Type:** String
* **Valid Values:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Default:** INFO
* **Description:** Logging level for validation execution
* **Example:** `--log-level DEBUG`

### Example Usage[¶](#example-usage "Link to this heading")

```
# Basic validation
sdv sqlserver run-validation \
  --data-validation-config-file ./configs/sqlserver_validation.yaml

# Validation with debug logging
sdv sqlserver run-validation \
  --data-validation-config-file ./configs/sqlserver_validation.yaml \
  --log-level DEBUG

# Using full command name
snowflake-data-validation sqlserver run-validation \
  -dvf /opt/validations/prod_config.yaml \
  -ll INFO
```

Copy

### Use Cases[¶](#use-cases "Link to this heading")

* Real-time validation during migration
* Pre-cutover validation checks
* Post-migration verification
* Continuous validation in CI/CD pipelines

---

## Run Asynchronous Validation[¶](#run-asynchronous-validation "Link to this heading")

Performs validation using pre-generated metadata files without connecting to databases.

### Syntax[¶](#id1 "Link to this heading")

```
snowflake-data-validation sqlserver run-async-validation \
  --data-validation-config-file /path/to/config.yaml
```

Copy

### Options[¶](#id2 "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file
* **Note:** Configuration must specify paths to pre-generated metadata files

### Example Usage[¶](#id3 "Link to this heading")

```
# Run async validation
sdv sqlserver run-async-validation \
  --data-validation-config-file ./configs/async_validation.yaml

# Using full command name
snowflake-data-validation sqlserver run-async-validation \
  -dvf /data/validations/async_config.yaml
```

Copy

### Prerequisites[¶](#prerequisites "Link to this heading")

Before running async validation:

1. Generate validation scripts using `generate-validation-scripts`
2. Execute the generated scripts on source and target databases
3. Ensure metadata files are available in the configured paths

### Use Cases[¶](#id4 "Link to this heading")

* Validating in environments with restricted database access
* Separating metadata extraction from validation
* Batch validation workflows
* Scheduled validation jobs

---

## Generate Validation Scripts[¶](#generate-validation-scripts "Link to this heading")

Generates SQL scripts for extracting metadata that can be executed separately.

### Syntax[¶](#id5 "Link to this heading")

```
snowflake-data-validation sqlserver generate-validation-scripts \
  --data-validation-config-file /path/to/config.yaml
```

Copy

### Options[¶](#id6 "Link to this heading")

**`--data-validation-config-file, -dvf`** (required)

* **Type:** String (path)
* **Description:** Path to YAML configuration file

### Example Usage[¶](#id7 "Link to this heading")

```
# Generate scripts
sdv sqlserver generate-validation-scripts \
  --data-validation-config-file ./configs/validation.yaml

# Using full command name
snowflake-data-validation sqlserver generate-validation-scripts \
  -dvf /opt/configs/script_generation.yaml
```

Copy

### Output[¶](#output "Link to this heading")

The command generates SQL scripts in the output directory configured in your YAML file:

```
<output_directory>/
├── source_schema_queries.sql
├── source_metrics_queries.sql
├── source_row_queries.sql
├── target_schema_queries.sql
├── target_metrics_queries.sql
└── target_row_queries.sql
```

Copy

### Use Cases[¶](#id8 "Link to this heading")

* Generating scripts for execution by DBAs
* Compliance requirements for query review
* Environments where direct CLI database access is restricted
* Manual execution and validation workflows

---

## Get Configuration Templates[¶](#get-configuration-templates "Link to this heading")

Retrieves example configuration files and optional query templates.

### Syntax[¶](#id9 "Link to this heading")

```
snowflake-data-validation sqlserver get-configuration-files \
  --templates-directory ./my-templates \
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
sdv sqlserver get-configuration-files

# Save templates to specific directory
sdv sqlserver get-configuration-files \
  --templates-directory ./my-project/templates

# Include query templates for customization
sdv sqlserver get-configuration-files \
  --templates-directory ./templates \
  --query-templates

# Using short flags
sdv sqlserver get-configuration-files -td ./templates --query-templates
```

Copy

### Output Files[¶](#output-files "Link to this heading")

**Without `--query-templates` flag:**

```
<templates_directory>/
└── sqlserver_validation_template.yaml
```

Copy

**With `--query-templates` flag:**

```
<templates_directory>/
├── sqlserver_validation_template.yaml
└── query_templates/
    ├── sqlserver_columns_metrics_query.sql.j2
    ├── sqlserver_row_count_query.sql.j2
    ├── sqlserver_compute_md5_sql.j2
    └── snowflake_columns_metrics_query.sql.j2
```

Copy

### Use Cases[¶](#id12 "Link to this heading")

* Starting a new validation project
* Learning configuration options
* Customizing validation queries for specific needs
* Creating organization-specific templates

---

## Auto-Generate Configuration File[¶](#auto-generate-configuration-file "Link to this heading")

Interactive command to generate a configuration file by prompting for connection parameters.

### Syntax[¶](#id13 "Link to this heading")

```
snowflake-data-validation sqlserver auto-generated-configuration-file
```

Copy

### Options[¶](#id14 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### Interactive Prompts[¶](#interactive-prompts "Link to this heading")

The command will prompt for the following information:

1. **SQL Server host**

   * Hostname or IP address of SQL Server
   * Example: `sqlserver.company.com`
2. **SQL Server port** (default: 1433)

   * Port number for SQL Server connection
   * Press Enter to accept default
3. **SQL Server username**

   * Authentication username
   * Example: `migration_user`
4. **SQL Server password**

   * Authentication password (hidden input)
   * Not displayed on screen for security
5. **SQL Server database**

   * Name of the database to validate
   * Example: `production_db`
6. **SQL Server schema**

   * Schema name within the database
   * Example: `dbo`
7. **Trust server certificate** (default: no)

   * Options: yes/no
   * Set to “yes” for self-signed certificates
8. **Encrypt connection** (default: yes)

   * Options: yes/no/optional
   * Controls SSL/TLS encryption
9. **Output path for configuration file**

   * Where to save the generated YAML file
   * Example: `./configs/my_validation.yaml`

### Example Session[¶](#example-session "Link to this heading")

```
$ sdv sqlserver auto-generated-configuration-file

SQL Server host: sqlserver.company.com
SQL Server port [1433]: 
SQL Server username: migration_user
SQL Server password: ********
SQL Server database: production_db
SQL Server schema: dbo
Trust server certificate (yes/no) [no]: no
Encrypt connection (yes/no/optional) [yes]: yes
Output path for configuration file: ./configs/sqlserver_config.yaml

Configuration file generated successfully: ./configs/sqlserver_config.yaml
```

Copy

### Generated Configuration[¶](#generated-configuration "Link to this heading")

The command generates a basic YAML configuration file:

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./validation_results

source_connection:
  mode: credentials
  host: sqlserver.company.com
  port: 1433
  username: migration_user
  password: "<hidden>"
  database: production_db
  trust_server_certificate: "no"
  encrypt: "yes"

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

   * Target connection details
   * Tables to validate
   * Validation options
   * Column selections and mappings
2. **Review security settings:**

   * Consider using environment variables for passwords
   * Update trust certificate and encryption settings as needed
3. **Add table configurations:**

   * Specify fully qualified table names
   * Configure column selections
   * Set up filtering where clauses
4. **Test the configuration:**

   ```
   sdv sqlserver run-validation \
     --data-validation-config-file ./configs/sqlserver_config.yaml
   ```

   Copy

### Use Cases[¶](#id15 "Link to this heading")

* Quick setup for new users
* Generating baseline configurations
* Testing connectivity during setup
* Creating template configurations for teams

---

## Row Partitioning Helper[¶](#row-partitioning-helper "Link to this heading")

Interactive command to generate partitioned table configurations for large tables. This helper divides tables into smaller row partitions based on a specified column, enabling more efficient validation of large datasets.

### Syntax[¶](#id16 "Link to this heading")

```
snowflake-data-validation sqlserver row-partitioning-helper
```

Copy

### Options[¶](#id17 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#how-it-works "Link to this heading")

The table partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply partitioning
3. If partitioning is enabled, collects partition parameters
4. Queries the source database to determine partition boundaries
5. Generates new table configurations with `WHERE` clauses for each partition
6. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id18 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/sqlserver_validation.yaml`
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
$ sdv sqlserver row-partitioning-helper

Generate a configuration file for SQL Server table partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip partitioning or specify partitioning parameters for each table.

Configuration file path: ./configs/sqlserver_validation.yaml

Apply partitioning for production_db.dbo.fact_sales? [Y/n]: y
Write the partition column for production_db.dbo.fact_sales: sale_id
Is 'sale_id' column a string type? [y/N]: n
Write the number of partitions for production_db.dbo.fact_sales: 10

Apply partitioning for production_db.dbo.dim_customer? [Y/n]: n

Apply partitioning for production_db.dbo.transactions? [Y/n]: y
Write the partition column for production_db.dbo.transactions: transaction_date
Is 'transaction_date' column a string type? [y/N]: n
Write the number of partitions for production_db.dbo.transactions: 5

Table partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#generated-output "Link to this heading")

The command generates partitioned table configurations with WHERE clauses:

```
tables:
  # Original table partitioned into 10 segments
  - fully_qualified_name: production_db.dbo.fact_sales
    where_clause: "sale_id >= 1 AND sale_id < 100000"
    target_where_clause: "sale_id >= 1 AND sale_id < 100000"
    # ... other table settings preserved

  - fully_qualified_name: production_db.dbo.fact_sales
    where_clause: "sale_id >= 100000 AND sale_id < 200000"
    target_where_clause: "sale_id >= 100000 AND sale_id < 200000"
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: production_db.dbo.dim_customer
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
snowflake-data-validation sqlserver column-partitioning-helper
```

Copy

### Options[¶](#id22 "Link to this heading")

This command has no command-line options. All input is provided through interactive prompts.

### How It Works[¶](#id23 "Link to this heading")

The column partitioning helper:

1. Reads an existing configuration file with table definitions
2. For each table, prompts whether to apply column partitioning
3. If partitioning is enabled, collects the number of partitions
4. Queries the source database to retrieve all column names for the table
5. Divides the columns into the specified number of partitions
6. Generates new table configurations where each partition validates only a subset of columns
7. Saves the partitioned configuration to a new file

### Interactive Prompts[¶](#id24 "Link to this heading")

The command will prompt for the following information:

1. **Configuration file path**

   * Path to existing YAML configuration file
   * Example: `./configs/sqlserver_validation.yaml`
2. **For each table in the configuration:**

   a. **Apply column partitioning?** (yes/no)

   * Whether to partition this specific table by columns
   * Default: yes

   b. **Number of partitions** (if partitioning)

   * How many column partitions to create
   * Example: `3`, `5`, `10`

### Example Session[¶](#id25 "Link to this heading")

```
$ sdv sqlserver column-partitioning-helper

Generate a configuration file for SQL Server column partitioning. This interactive 
helper function processes each table in the configuration file, allowing users to 
either skip column partitioning or specify column partitioning parameters for each table.

Configuration file path: ./configs/sqlserver_validation.yaml

Apply column partitioning for production_db.dbo.wide_table? [Y/n]: y
Write the number of partitions for production_db.dbo.wide_table: 5

Apply column partitioning for production_db.dbo.small_table? [Y/n]: n

Apply column partitioning for production_db.dbo.report_table? [Y/n]: y
Write the number of partitions for production_db.dbo.report_table: 3

Column partitioning configuration file generated successfully!
```

Copy

### Generated Output[¶](#id26 "Link to this heading")

The command generates partitioned table configurations with column subsets:

```
tables:
  # Original table with 100 columns partitioned into 5 segments (20 columns each)
  - fully_qualified_name: production_db.dbo.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_a
      - column_b
      - column_c
      # ... first 20 columns alphabetically

  - fully_qualified_name: production_db.dbo.wide_table
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - column_d
      - column_e
      - column_f
      # ... next 20 columns alphabetically
    # ... continues for each partition

  # Non-partitioned table preserved as-is
  - fully_qualified_name: production_db.dbo.small_table
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

## SQL Server Connection Configuration[¶](#sql-server-connection-configuration "Link to this heading")

SQL Server connections require specific configuration in the YAML file.

### Connection Example[¶](#connection-example "Link to this heading")

```
source_connection:
  mode: credentials
  host: "sqlserver.company.com"
  port: 1433
  username: "sqlserver_user"
  password: "secure_password"
  database: "source_database"
  trust_server_certificate: "no"
  encrypt: "yes"
```

Copy

### Connection Fields[¶](#connection-fields "Link to this heading")

**`mode`** (required)

* **Type:** String
* **Valid Values:** `credentials`
* **Description:** Connection mode for SQL Server

**`host`** (required)

* **Type:** String
* **Description:** SQL Server hostname or IP address
* **Examples:**

  + `"sqlserver.company.com"`
  + `"192.168.1.100"`
  + `"sql-prod-01.internal.company.net"`

**`port`** (required)

* **Type:** Integer
* **Default:** 1433
* **Description:** SQL Server port number
* **Common Values:**

  + 1433 (default)
  + 1434 (SQL Server Browser)

**`username`** (required)

* **Type:** String
* **Description:** SQL Server authentication username
* **Example:** `"migration_admin"`

**`password`** (required)

* **Type:** String
* **Description:** SQL Server authentication password
* **Security Note:** Consider using environment variables

**`database`** (required)

* **Type:** String
* **Description:** SQL Server database name
* **Example:** `"production_database"`

**`trust_server_certificate`** (optional)

* **Type:** String
* **Valid Values:** `"yes"`, `"no"`
* **Default:** `"no"`
* **Description:** Whether to trust the server certificate for SSL/TLS connections
* **Use Case:** Set to “yes” for self-signed certificates

**`encrypt`** (optional)

* **Type:** String
* **Valid Values:** `"yes"`, `"no"`, `"optional"`
* **Default:** `"yes"`
* **Description:** Connection encryption setting
* **Recommendations:**

  + Use “yes” for production
  + Use “optional” for development/testing
  + Use “no” only in secure internal networks

### Connection Examples[¶](#connection-examples "Link to this heading")

**Production Connection with SSL/TLS:**

```
source_connection:
  mode: credentials
  host: "sql-prod.company.com"
  port: 1433
  username: "prod_reader"
  password: "${SQL_SERVER_PASSWORD}"  # From environment variable
  database: "production_db"
  trust_server_certificate: "no"
  encrypt: "yes"
```

Copy

**Development Connection:**

```
source_connection:
  mode: credentials
  host: "localhost"
  port: 1433
  username: "dev_user"
  password: "dev_password"
  database: "dev_database"
  trust_server_certificate: "yes"
  encrypt: "optional"
```

Copy

**Self-Signed Certificate Connection:**

```
source_connection:
  mode: credentials
  host: "internal-sql.company.local"
  port: 1433
  username: "internal_user"
  password: "secure_password"
  database: "internal_db"
  trust_server_certificate: "yes"  # Required for self-signed certs
  encrypt: "yes"
```

Copy

---

## Complete SQL Server Examples[¶](#complete-sql-server-examples "Link to this heading")

### Example 1: Basic SQL Server Validation[¶](#example-1-basic-sql-server-validation "Link to this heading")

```
# Global configuration
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./validation_results
max_threads: auto

# Source connection
source_connection:
  mode: credentials
  host: sqlserver.company.com
  port: 1433
  username: sql_user
  password: sql_password
  database: production_db
  trust_server_certificate: "no"
  encrypt: "yes"

# Target connection
target_connection:
  mode: name
  name: snowflake_prod

# Validation configuration
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

# Tables to validate
tables:
  - fully_qualified_name: production_db.dbo.customers
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - customer_id

  - fully_qualified_name: production_db.dbo.orders
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_notes
      - audit_log
    where_clause: "order_date >= '2024-01-01'"
    target_where_clause: "order_date >= '2024-01-01'"
```

Copy

### Example 2: SQL Server with Column Mappings[¶](#example-2-sql-server-with-column-mappings "Link to this heading")

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: /opt/validation/sqlserver
max_threads: 16

source_connection:
  mode: credentials
  host: sql-prod.company.com
  port: 1433
  username: migration_user
  password: secure_password
  database: legacy_db
  trust_server_certificate: "no"
  encrypt: "yes"

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 100

comparison_configuration:
  tolerance: 0.01

tables:
  - fully_qualified_name: legacy_db.dbo.customer_master
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - cust_id
      - cust_name
      - email_addr
      - phone_num
    column_mappings:
      cust_id: customer_id
      cust_name: customer_name
      email_addr: email
      phone_num: phone
    index_column_list:
      - cust_id
    chunk_number: 20
```

Copy

### Example 3: SQL Server Large Table Optimization[¶](#example-3-sql-server-large-table-optimization "Link to this heading")

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./large_table_validation
max_threads: 32

source_connection:
  mode: credentials
  host: bigdata-sql.company.com
  port: 1433
  username: bigdata_reader
  password: readonly_password
  database: analytics_db
  trust_server_certificate: "no"
  encrypt: "yes"

target_connection:
  mode: name
  name: snowflake_analytics

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 500
  exclude_metrics: false

comparison_configuration:
  tolerance: 0.005

tables:
  - fully_qualified_name: analytics_db.dbo.fact_transactions
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - large_blob_column
      - xml_metadata
    index_column_list:
      - transaction_id
    chunk_number: 100
    where_clause: "transaction_date >= '2024-01-01' AND amount > 0"
    target_where_clause: "transaction_date >= '2024-01-01' AND amount > 0"
    max_failed_rows_number: 1000
```

Copy

---

## Troubleshooting SQL Server Connections[¶](#troubleshooting-sql-server-connections "Link to this heading")

### Issue: SSL/TLS Certificate Errors[¶](#issue-ssl-tls-certificate-errors "Link to this heading")

**Symptom:**

```
SSL certificate verification failed
```

Copy

**Solution:**

Set `trust_server_certificate` to “yes”:

```
source_connection:
  trust_server_certificate: "yes"
  encrypt: "yes"
```

Copy

### Issue: Connection Timeout[¶](#issue-connection-timeout "Link to this heading")

**Symptom:**

```
Connection timeout: Unable to connect to SQL Server
```

Copy

**Solutions:**

1. Verify the host and port:

   ```
   telnet sqlserver.company.com 1433
   ```

   Copy
2. Check firewall rules
3. Verify SQL Server is running and accepting connections
4. Test with SQL Server Management Studio (SSMS)

### Issue: Authentication Failed[¶](#issue-authentication-failed "Link to this heading")

**Symptom:**

```
Login failed for user 'username'
```

Copy

**Solutions:**

1. Verify credentials are correct
2. Check SQL Server authentication mode (mixed mode required)
3. Ensure user has necessary permissions:

   ```
   -- Grant read permissions
   GRANT SELECT ON SCHEMA::dbo TO migration_user;
   GRANT VIEW DEFINITION ON SCHEMA::dbo TO migration_user;
   ```

   Copy

### Issue: Database Not Found[¶](#issue-database-not-found "Link to this heading")

**Symptom:**

```
Cannot open database "database_name"
```

Copy

**Solutions:**

1. Verify database name is correct
2. Check user has access to the database:

   ```
   USE database_name;
   SELECT * FROM sys.tables;
   ```

   Copy
3. Ensure database is online and accessible

---

## Best Practices for SQL Server[¶](#best-practices-for-sql-server "Link to this heading")

### Security[¶](#security "Link to this heading")

1. **Use encrypted connections** in production:

   ```
   source_connection:
     encrypt: "yes"
     trust_server_certificate: "no"
   ```

   Copy
2. **Store passwords securely:**

   * Use environment variables
   * Use secret management systems
   * Avoid hardcoding passwords
3. **Use read-only accounts:**

   ```
   CREATE USER migration_reader WITH PASSWORD = 'secure_password';
   GRANT SELECT ON SCHEMA::dbo TO migration_reader;
   ```

   Copy

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
       where_clause: "date >= '2024-01-01'"
   ```

   Copy
3. **Optimize thread count:**

   ```
   max_threads: 16  # Adjust based on server capacity
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
2. **Add metrics validation:**

   ```
   validation_configuration:
     schema_validation: true
     metrics_validation: true
     row_validation: false
   ```

   Copy
3. **Enable row validation selectively:**

   ```
   validation_configuration:
     row_validation: true

   tables:
     - fully_qualified_name: critical_table
       # Row validation enabled for this table
   ```

   Copy

---

## See Also[¶](#see-also "Link to this heading")

* [Main CLI Usage Guide](CLI_USAGE_GUIDE)
* [Teradata Commands Reference](teradata_commands)
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
4. [Run Asynchronous Validation](#run-asynchronous-validation)
5. [Generate Validation Scripts](#generate-validation-scripts)
6. [Get Configuration Templates](#get-configuration-templates)
7. [Auto-Generate Configuration File](#auto-generate-configuration-file)
8. [Row Partitioning Helper](#row-partitioning-helper)
9. [Column Partitioning Helper](#column-partitioning-helper)
10. [SQL Server Connection Configuration](#sql-server-connection-configuration)
11. [Complete SQL Server Examples](#complete-sql-server-examples)
12. [Troubleshooting SQL Server Connections](#troubleshooting-sql-server-connections)
13. [Best Practices for SQL Server](#best-practices-for-sql-server)
14. [See Also](#see-also)