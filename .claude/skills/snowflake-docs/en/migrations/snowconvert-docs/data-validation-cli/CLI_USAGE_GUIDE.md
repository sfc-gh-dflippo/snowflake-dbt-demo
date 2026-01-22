---
auto_generated: true
description: The Snowflake Data Validation CLI (snowflake-data-validation or sdv)
  is a comprehensive command-line tool for validating data migrations between source
  databases (SQL Server, Teradata, Amazon Redshift
last_scraped: '2026-01-14T16:52:13.102960+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CLI_USAGE_GUIDE
title: Snowflake Data Validation CLI - Complete Usage Guide | Snowflake Documentation
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)Usage Guide

# Snowflake Data Validation CLI - Complete Usage Guide[¶](#snowflake-data-validation-cli-complete-usage-guide "Link to this heading")

## Overview[¶](#overview "Link to this heading")

The Snowflake Data Validation CLI (`snowflake-data-validation` or `sdv`) is a comprehensive command-line tool for validating data migrations between source databases (SQL Server, Teradata, Amazon Redshift) and Snowflake. It provides multi-level validation strategies to ensure data consistency and quality.

### Key Features[¶](#key-features "Link to this heading")

* **Multi-Level Validation**: Schema, statistical metrics, and row-by-row data validation
* **Multiple Source Platforms**: SQL Server, Teradata, and Amazon Redshift
* **Flexible Execution Modes**: Synchronous, asynchronous, and script generation
* **Comprehensive Configuration**: YAML-based configuration with extensive customization options
* **Detailed Reporting**: Comprehensive validation reports with mismatch information

---

## Prerequisites[¶](#prerequisites "Link to this heading")

Before installing the Snowflake Data Validation CLI, ensure you have the following prerequisites installed:

### System Requirements[¶](#system-requirements "Link to this heading")

* **Python**: Version 3.8 or higher
* **pip**: Latest version recommended
* **Operating System**: Linux, macOS, or Windows

### ODBC Drivers[¶](#odbc-drivers "Link to this heading")

The CLI requires appropriate ODBC drivers to be installed on your system for connecting to source databases. Install the ODBC driver that matches your source database dialect:

#### SQL Server ODBC Driver[¶](#sql-server-odbc-driver "Link to this heading")

For SQL Server as a source database, you need the **Microsoft ODBC Driver for SQL Server**.

**Recommended Version**: ODBC Driver 17 or 18 for SQL Server

**Installation Instructions:**

* **Linux**:

  ```
  # Ubuntu/Debian
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
  curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
  apt-get update
  ACCEPT_EULA=Y apt-get install -y msodbcsql18
  ```

  Copy
* **macOS**:

  ```
  # Using Homebrew
  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
  brew update
  HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
  ```

  Copy
* **Windows**:
  Download and install from [Microsoft’s official download page](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

**Verification:**

```
# List available drivers (should show ODBC Driver 17 or 18 for SQL Server)
odbcinst -q -d
```

Copy

**Documentation**: [Microsoft ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server)

#### Teradata ODBC Driver[¶](#teradata-odbc-driver "Link to this heading")

For Teradata as a source database, you need the **Teradata ODBC Driver**.

**Recommended Version**: Teradata ODBC Driver 17.20 or higher

**Installation Instructions:**

1. Download the Teradata Tools and Utilities (TTU) package from [Teradata Downloads](https://downloads.teradata.com/)
2. Select your operating system and download the appropriate installer
3. Run the installer and select “ODBC Driver” during installation
4. Configure the driver according to Teradata’s documentation

**Note**: You may need to create a Teradata account to access the download page.

**Configuration:**
After installation, you may need to configure the ODBC driver:

* **Linux/macOS**: Edit `/etc/odbc.ini` and `/etc/odbcinst.ini`
* **Windows**: Use the ODBC Data Source Administrator

**Documentation**: [Teradata ODBC Driver Documentation](https://downloads.teradata.com/download/connectivity/odbc-driver/linux)

#### Amazon Redshift ODBC Driver[¶](#amazon-redshift-odbc-driver "Link to this heading")

For Amazon Redshift as a source database, you need the **Amazon Redshift ODBC Driver** or a **PostgreSQL ODBC Driver** (since Redshift is PostgreSQL-compatible).

**Option 1: Amazon Redshift ODBC Driver (Recommended)**

**Recommended Version**: Amazon Redshift ODBC Driver 2.x

**Installation Instructions:**

* Download from [Amazon Redshift ODBC Driver Download](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-odbc-connection.html)
* Choose your operating system and architecture
* Follow the installation wizard

**Option 2: PostgreSQL ODBC Driver (Alternative)**

* **Linux**:

  ```
  # Ubuntu/Debian
  sudo apt-get install odbc-postgresql

  # RHEL/CentOS/Fedora
  sudo yum install postgresql-odbc
  ```

  Copy
* **macOS**:

  ```
  # Using Homebrew
  brew install psqlodbc
  ```

  Copy
* **Windows**:
  Download from [PostgreSQL ODBC Driver](https://www.postgresql.org/ftp/odbc/versions/)

**Verification:**

```
# List available drivers (should show Amazon Redshift or PostgreSQL drivers)
odbcinst -q -d
```

Copy

**Documentation**: [Amazon Redshift ODBC Driver Documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-odbc-connection.html)

### Additional Tools (Optional)[¶](#additional-tools-optional "Link to this heading")

* **unixODBC** (Linux/macOS): Required for ODBC driver management

  ```
  # Ubuntu/Debian
  sudo apt-get install unixodbc unixodbc-dev

  # macOS
  brew install unixodbc

  # RHEL/CentOS/Fedora
  sudo yum install unixODBC unixODBC-devel
  ```

  Copy

### Network Access[¶](#network-access "Link to this heading")

Ensure your environment has network access to:

* Source database (SQL Server, Teradata, or Redshift)
* Snowflake account
* Package repositories (for pip installation)

---

## Installation[¶](#installation "Link to this heading")

### Base Installation[¶](#base-installation "Link to this heading")

```
pip install snowflake-data-validation
```

Copy

### Source-Specific Installation[¶](#source-specific-installation "Link to this heading")

Install with the appropriate database driver for your source system:

```
# For SQL Server as source
pip install "snowflake-data-validation[sqlserver]"

# For Teradata as source
pip install "snowflake-data-validation[teradata]"

# For Amazon Redshift as source
pip install "snowflake-data-validation[redshift]"

# For development with all drivers
pip install "snowflake-data-validation[all]"
```

Copy

### Post-Installation Verification[¶](#post-installation-verification "Link to this heading")

After installation, verify the CLI is correctly installed:

```
# Check version
snowflake-data-validation --version

# Or using the alias
sdv --version

# Verify ODBC drivers are accessible
odbcinst -q -d
```

Copy

---

## Quick Start[¶](#quick-start "Link to this heading")

### 1. Generate a Configuration Template[¶](#generate-a-configuration-template "Link to this heading")

```
# Get SQL Server configuration templates
snowflake-data-validation sqlserver get-configuration-files

# Get Teradata configuration templates
snowflake-data-validation teradata get-configuration-files

# Get Redshift configuration templates
snowflake-data-validation redshift get-configuration-files
```

Copy

### 2. Auto-Generate Configuration from Connection[¶](#auto-generate-configuration-from-connection "Link to this heading")

```
# Interactive configuration generation for SQL Server
snowflake-data-validation sqlserver auto-generated-configuration-file

# Interactive configuration generation for Teradata
snowflake-data-validation teradata auto-generated-configuration-file

# Interactive configuration generation for Redshift
snowflake-data-validation redshift auto-generated-configuration-file
```

Copy

### 3. Run Validation[¶](#run-validation "Link to this heading")

```
# Run synchronous validation
snowflake-data-validation sqlserver run-validation \
  --data-validation-config-file ./config/validation_config.yaml
```

Copy

---

## Best Practices & Guidance[¶](#best-practices-guidance "Link to this heading")

This section provides strategic guidance on how to approach data validation effectively, minimize resource consumption, and identify issues early.

### Incremental Validation Approach[¶](#incremental-validation-approach "Link to this heading")

Note

Always start small and scale up incrementally. Running full validation on large datasets immediately can:

* Consume significant compute resources on both source and target systems
* Take hours or days to complete
* Make troubleshooting difficult if issues are found
* Impact production systems if run during business hours

### Recommended Validation Strategy[¶](#recommended-validation-strategy "Link to this heading")

Follow this proven approach to ensure efficient and effective validation:

#### Phase 1: Start with a Sample Dataset[¶](#phase-1-start-with-a-sample-dataset "Link to this heading")

**Goal**: Verify configuration and establish baseline

**Approach**:

* Test with 1-2 small tables first (< 100,000 rows)
* Choose tables with diverse data types to validate type mapping
* Verify connectivity and authentication work correctly
* Confirm output format meets your needs

**Example Configuration**:

```
tables:
  - source_table_name: "small_reference_table"
    target_table_name: "small_reference_table"
    source_schema_name: "dbo"
    target_schema_name: "PUBLIC"
    target_database_name: "MIGRATION_DB"
    where_clause: "reference_id <= 1000"  # Limit to first 1000 rows on source
    target_where_clause: "reference_id <= 1000"  # Limit to first 1000 rows on target
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"
```

Copy

**What to Verify**:

* ✅ Connection to both source and target successful
* ✅ Schema validation passes
* ✅ Row count matches
* ✅ Data types mapped correctly
* ✅ Validation report generated successfully

**Understanding `where_clause` vs `target_where_clause`**:

The tool provides two filtering options:

* **`where_clause`**: Applied **only** to the **source** table

  ```
  where_clause: "ProductID <= 45"  # Filters only the source table
  ```

  Copy
* **`target_where_clause`**: Applied **only** to the **target** table (Snowflake)

  ```
  target_where_clause: "ProductID <= 45"  # Filters only the target table
  ```

  Copy

**Common Usage Patterns**:

```
# Pattern 1: Apply same filter to both source and target
tables:
  - source_table_name: "products"
    where_clause: "ProductID <= 100"           # Filter source
    target_where_clause: "ProductID <= 100"     # Filter target with same condition
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"

# Pattern 2: Different filters for source and target
# Useful when target has additional test data to exclude
tables:
  - source_table_name: "products"
    where_clause: "ProductID <= 100"                    # Filter source
    target_where_clause: "ProductID <= 100 AND ProductID != 5"  # Exclude test data in target
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"

# Pattern 3: Filter only source (validate all target data)
tables:
  - source_table_name: "products"
    where_clause: "ProductID <= 100"  # Only validate subset from source
    # No target_where_clause - validates all matching rows in target
    validations:
      - validation_type: "row_count"
```

Copy

#### Phase 2: Verify Small Subsets of Production Tables[¶](#phase-2-verify-small-subsets-of-production-tables "Link to this heading")

**Goal**: Test against actual production data patterns with limited scope

**Approach**:

* Select a subset of rows from production tables (10,000 - 100,000 rows)
* Use `where_clause` and `target_where_clause` to restrict data
* Focus on recent data or specific partitions
* Validate critical business columns first

**Example Configuration**:

```
tables:
  - source_table_name: "large_transactions_table"
    target_table_name: "large_transactions_table"
    source_schema_name: "sales"
    target_schema_name: "SALES"
    target_database_name: "MIGRATION_DB"
    where_clause: "transaction_date >= '2024-01-01' AND transaction_date < '2024-02-01'"
    target_where_clause: "transaction_date >= '2024-01-01' AND transaction_date < '2024-02-01'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"
        columns_to_validate:
          - "transaction_id"
          - "amount"
          - "customer_id"
          - "transaction_date"
```

Copy

**Key Points**:

* 🎯 Use date ranges or ID ranges to limit scope
* 🎯 Test different data patterns (recent vs. historical, high-volume dates)
* 🎯 Validate critical business columns before validating all columns

#### Phase 3: Partition-Based Validation for Large Tables[¶](#phase-3-partition-based-validation-for-large-tables "Link to this heading")

**Goal**: Validate large tables efficiently using partitioning strategy

**⚠️ IMPORTANT**: For tables with millions or billions of rows, validating the entire table at once is:

* Resource-intensive (high compute costs)
* Time-consuming (can take hours/days)
* Risky (harder to identify specific issue patterns)

**Recommended Approach for Large Tables**:

**Strategy 1: Date-Based Partitioning**

Validate data in chunks based on date ranges:

```
# Validation 1: January 2024
tables:
  - source_table_name: "orders"
    target_table_name: "orders"
    source_schema_name: "dbo"
    target_schema_name: "PUBLIC"
    target_database_name: "MIGRATION_DB"
    where_clause: "order_date >= '2024-01-01' AND order_date < '2024-02-01'"
    target_where_clause: "order_date >= '2024-01-01' AND order_date < '2024-02-01'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"

# Validation 2: February 2024
# Create separate config with: 
# where_clause: "order_date >= '2024-02-01' AND order_date < '2024-03-01'"
# target_where_clause: "order_date >= '2024-02-01' AND order_date < '2024-03-01'"
```

Copy

**Strategy 2: Modulo-Based Sampling**

Use modulo arithmetic to sample evenly distributed rows:

```
tables:
  - source_table_name: "customers"
    target_table_name: "customers"
    source_schema_name: "dbo"
    target_schema_name: "PUBLIC"
    target_database_name: "MIGRATION_DB"
    where_clause: "customer_id % 100 = 0"  # 1% sample - evenly distributed
    target_where_clause: "customer_id % 100 = 0"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"
```

Copy

**Strategy 3: Statistical Sampling**

For very large tables (> 100M rows), validate representative samples:

```
tables:
  - source_table_name: "clickstream_events"
    target_table_name: "clickstream_events"
    source_schema_name: "dbo"
    target_schema_name: "PUBLIC"
    target_database_name: "MIGRATION_DB"
    where_clause: "event_id % 10000 = 0"  # ~0.01% sample - statistically distributed
    target_where_clause: "event_id % 10000 = 0"
    validations:
      # First: Validate aggregates and row count (fast)
      - validation_type: "row_count"
      - validation_type: "aggregate_metrics"
      
      # Second: Validate a statistical sample of rows
      - validation_type: "column_level"
```

Copy

**Strategy 4: Progressive Partition Validation**

Validate multiple partitions progressively:

```
# config_q1.yaml - Validate Q1 2024
tables:
  - source_table_name: "orders"
    target_table_name: "orders"
    where_clause: "order_date >= '2024-01-01' AND order_date < '2024-04-01'"
    target_where_clause: "order_date >= '2024-01-01' AND order_date < '2024-04-01'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"

# config_q2.yaml - Validate Q2 2024 (run after Q1 passes)
tables:
  - source_table_name: "orders"
    target_table_name: "orders"
    where_clause: "order_date >= '2024-04-01' AND order_date < '2024-07-01'"
    target_where_clause: "order_date >= '2024-04-01' AND order_date < '2024-07-01'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"
```

Copy

```
# Validate Q1 2024
sdv sqlserver run-validation --data-validation-config-file config_q1.yaml

# If Q1 passes, validate Q2 2024
sdv sqlserver run-validation --data-validation-config-file config_q2.yaml

# Continue for remaining quarters
```

Copy

#### Phase 4: Full Validation[¶](#phase-4-full-validation "Link to this heading")

**Goal**: Complete comprehensive validation after successful subset testing

**When to Run Full Validation**:

* ✅ Sample validations pass successfully
* ✅ Subset validations show no data quality issues
* ✅ You have allocated sufficient time and compute resources
* ✅ Preferably during off-peak hours

**Considerations**:

* Use **asynchronous validation** for large datasets to avoid timeouts
* Consider using **script generation mode** to run validations in parallel
* Monitor resource consumption on both source and target systems
* Plan for validation to run during maintenance windows

**Example**:

```
# Generate scripts for parallel execution
sdv sqlserver generate-validation-scripts \
  --data-validation-config-file full_validation_config.yaml \
  --output-directory ./validation_scripts

# Review generated scripts and execute in parallel or scheduled
```

Copy

### Performance Optimization Tips[¶](#performance-optimization-tips "Link to this heading")

#### 1. Use Appropriate Validation Types[¶](#use-appropriate-validation-types "Link to this heading")

Not all tables need all validation types:

```
# For reference/lookup tables (small, static)
validations:
  - validation_type: "schema"
  - validation_type: "row_count"
  - validation_type: "column_level"  # Full validation OK

# For large transaction tables
validations:
  - validation_type: "schema"
  - validation_type: "row_count"
  - validation_type: "aggregate_metrics"  # Use aggregates instead of row-by-row
```

Copy

#### 2. Prioritize Critical Columns[¶](#prioritize-critical-columns "Link to this heading")

For large tables, validate critical business columns first:

```
validations:
  - validation_type: "column_level"
    columns_to_validate:
      # Start with business-critical columns
      - "customer_id"
      - "transaction_amount"
      - "transaction_date"
      # Add more columns after initial validation succeeds
```

Copy

#### 3. Leverage Partitioning Metadata[¶](#leverage-partitioning-metadata "Link to this heading")

If your tables are partitioned, validate partition by partition:

```
# Config 1: Validate partition 1
tables:
  - source_table_name: "orders"
    target_table_name: "orders"
    where_clause: "partition_key = '2024-01'"
    target_where_clause: "partition_key = '2024-01'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"

# Config 2: Validate partition 2
tables:
  - source_table_name: "orders"
    target_table_name: "orders"
    where_clause: "partition_key = '2024-02'"
    target_where_clause: "partition_key = '2024-02'"
    validations:
      - validation_type: "row_count"
      - validation_type: "column_level"
```

Copy

#### 4. Use Asynchronous Validation for Production[¶](#use-asynchronous-validation-for-production "Link to this heading")

For production environments, use asynchronous validation:

```
# Async validation returns immediately, processes in Snowflake
sdv sqlserver run-async-validation \
  --data-validation-config-file config.yaml \
  --poll-interval 30 \
  --max-wait-time 3600
```

Copy

### Cost and Resource Management[¶](#cost-and-resource-management "Link to this heading")

#### Estimate Query Costs[¶](#estimate-query-costs "Link to this heading")

**Before running validation on large tables**:

1. **Estimate row counts**:

   ```
   -- Source
   SELECT COUNT(*) FROM source_table WHERE <partition_filter>;

   -- Target
   SELECT COUNT(*) FROM target_table WHERE <partition_filter>;
   ```

   Copy
2. **Estimate data volume**:

   ```
   -- Check table size
   SELECT 
       table_name,
       row_count,
       bytes,
       bytes / (1024*1024*1024) as size_gb
   FROM information_schema.tables
   WHERE table_name = 'your_table';
   ```

   Copy
3. **Start with small partitions**: If estimated size > 10 GB, break into smaller chunks

#### Compute Warehouse Sizing (Snowflake)[¶](#compute-warehouse-sizing-snowflake "Link to this heading")

* **Small tables (< 1M rows)**: XS or S warehouse
* **Medium tables (1M - 10M rows)**: S or M warehouse
* **Large tables (> 10M rows)**: M or L warehouse, use partitioning
* **Very large tables (> 100M rows)**: L or XL warehouse, mandatory partitioning

### Common Pitfalls to Avoid[¶](#common-pitfalls-to-avoid "Link to this heading")

| ❌ Don’t Do This | ✅ Do This Instead |
| --- | --- |
| Validate entire 1B row table at once | Validate in partitions of 10M-100M rows |
| Run validation during business hours on production | Schedule during off-peak hours or use read replicas |
| Skip sample testing and go straight to full validation | Always validate samples first |
| Use same configuration for all table sizes | Tailor validation strategy to table size |
| Validate all columns for all tables | Prioritize critical columns, especially for large tables |
| Ignore resource consumption | Monitor and set appropriate compute resources |

### Validation Checklist[¶](#validation-checklist "Link to this heading")

Use this checklist to ensure you’re following best practices:

**Before Starting**:

* [ ] ODBC drivers installed and tested
* [ ] Connectivity to source and target verified
* [ ] Configuration template generated
* [ ] Test credentials have appropriate read permissions

**Initial Testing** (Phase 1):

* [ ] Selected 1-2 small tables for initial test
* [ ] Configuration file created and reviewed
* [ ] Sample validation executed successfully
* [ ] Validation report reviewed and understood

**Subset Validation** (Phase 2):

* [ ] Identified subset of production data to validate
* [ ] Used `where_clause` and `target_where_clause` to restrict rows
* [ ] Validated 10,000 - 100,000 rows successfully
* [ ] Reviewed results for any data quality issues

**Large Table Strategy** (Phase 3):

* [ ] Identified tables > 10M rows
* [ ] Chosen partitioning strategy (date, ID range, modulo)
* [ ] Estimated compute costs for validation
* [ ] Tested validation on 1-2 partitions first
* [ ] Documented partition validation schedule

**Production Validation** (Phase 4):

* [ ] All subset validations passed
* [ ] Resource allocation planned (compute, time)
* [ ] Validation scheduled during maintenance window
* [ ] Using asynchronous or script generation mode
* [ ] Monitoring plan in place

### Example: Complete Validation Strategy[¶](#example-complete-validation-strategy "Link to this heading")

Here’s a complete example of validating a large e-commerce database:

**Day 1: Initial Setup and Small Tables**

```
# Test with small reference tables
sdv sqlserver run-validation --data-validation-config-file config_small_tables.yaml
# Tables: product_categories (1K rows), payment_types (50 rows)
```

Copy

**Day 2: Subset of Medium Tables**

```
# Test with recent data from medium tables
sdv sqlserver run-validation --data-validation-config-file config_subset_medium.yaml
# Tables: customers WHERE created_date >= '2024-01-01' (50K rows)
#         products WHERE product_id <= 10000 (10K rows)
```

Copy

**Day 3: Partition Strategy for Large Tables**

```
# Validate one month of orders
sdv sqlserver run-validation --data-validation-config-file config_orders_jan2024.yaml
# Table: orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31' (500K rows)
```

Copy

**Day 4-5: Progressive Partition Validation**

```
# Generate scripts for all partitions
sdv sqlserver generate-validation-scripts \
  --data-validation-config-file config_all_partitions.yaml \
  --output-directory ./scripts

# Review and execute scripts for each partition
```

Copy

**Day 6: Full Validation (Off-Peak)**

```
# Run complete validation during weekend maintenance window
sdv sqlserver run-async-validation \
  --data-validation-config-file config_full_validation.yaml \
  --poll-interval 60 \
  --max-wait-time 28800  # 8 hours
```

Copy

---

## CLI Commands[¶](#cli-commands "Link to this heading")

### Command Structure[¶](#command-structure "Link to this heading")

All commands follow this consistent structure:

```
snowflake-data-validation <source_dialect> <command> [options]

# Or use the shorter alias
sdv <source_dialect> <command> [options]
```

Copy

Where:

* `<source_dialect>` is one of: `sqlserver`, `teradata`,`redshift.`
* `<command>` is one of:

  + `run-validation` - Run synchronous validation
  + `run-async-validation` - Run asynchronous validation
  + `generate-validation-scripts` - Generate validation scripts
  + `get-configuration-files` - Get configuration templates
  + `auto-generated-configuration-file` - Interactive config generation

### Global Options[¶](#global-options "Link to this heading")

These options can be used with the CLI without specifying a source dialect or command:

#### Check Version[¶](#check-version "Link to this heading")

Display the current installed version of the Snowflake Data Validation CLI:

```
# Using full command name
snowflake-data-validation --version

# Using the alias
sdv --version
```

Copy

**Output Example:**

```
snowflake-data-validation 1.2.3
```

Copy

**Use Cases:**

* Verify successful installation
* Check which version is currently installed
* Confirm version before reporting issues
* Ensure compatibility with documentation

#### Help[¶](#help "Link to this heading")

Display general help information:

```
# General help
snowflake-data-validation --help
sdv --help

# Command-specific help
sdv sqlserver --help
sdv teradata run-validation --help
sdv redshift generate-validation-scripts --help
```

Copy

### Dialect-Specific Command References[¶](#dialect-specific-command-references "Link to this heading")

For detailed command documentation specific to your source database, see the following pages:

* **[SQL Server Commands Reference](sqlserver_commands)** - Complete command reference for SQL Server migrations
* **[Teradata Commands Reference](teradata_commands)** - Complete command reference for Teradata migrations
* **[Amazon Redshift Commands Reference](redshift_commands)** - Complete command reference for Redshift migrations

Each page provides:

* Detailed syntax for all commands
* Complete option descriptions with examples
* Connection configuration specifics
* Dialect-specific examples
* Troubleshooting tips for that platform
* Best practices for that database type

---

### SQL Server Commands[¶](#sql-server-commands "Link to this heading")

For complete SQL Server command documentation, see [SQL Server Commands Reference](sqlserver_commands).

**Quick Links:**

* [Run Synchronous Validation](sqlserver_commands.html#run-synchronous-validation)
* [Run Asynchronous Validation](sqlserver_commands.html#run-asynchronous-validation)
* [Generate Validation Scripts](sqlserver_commands.html#generate-validation-scripts)
* [Get Configuration Templates](sqlserver_commands.html#get-configuration-templates)
* [Auto-Generate Configuration File](sqlserver_commands.html#auto-generate-configuration-file)
* [Connection Configuration](sqlserver_commands.html#sql-server-connection-configuration)
* [Troubleshooting](sqlserver_commands.html#troubleshooting-sql-server-connections)

#### Common Commands[¶](#common-commands "Link to this heading")

**Run Validation:**

```
sdv sqlserver run-validation \
  --data-validation-config-file ./configs/sqlserver_validation.yaml
```

Copy

**Generate Scripts:**

```
sdv sqlserver generate-validation-scripts \
  --data-validation-config-file /path/to/config.yaml
```

Copy

**Get Templates:**

```
sdv sqlserver get-configuration-files \
  --templates-directory ./templates
```

Copy

For complete documentation, see [SQL Server Commands Reference](sqlserver_commands).

---

### Teradata Commands[¶](#teradata-commands "Link to this heading")

For complete Teradata command documentation, see [Teradata Commands Reference](teradata_commands).

**Quick Links:**

* [Run Synchronous Validation](teradata_commands.html#run-synchronous-validation)
* [Run Asynchronous Validation](teradata_commands.html#run-asynchronous-validation)
* [Generate Validation Scripts](teradata_commands.html#generate-validation-scripts)
* [Get Configuration Templates](teradata_commands.html#get-configuration-templates)
* [Auto-Generate Configuration File](teradata_commands.html#auto-generate-configuration-file)
* [Connection Configuration](teradata_commands.html#teradata-connection-configuration)
* [Troubleshooting](teradata_commands.html#troubleshooting-teradata-connections)

#### Common Commands[¶](#id1 "Link to this heading")

**Run Validation:**

```
sdv teradata run-validation \
  --data-validation-config-file ./configs/teradata_validation.yaml
```

Copy

**Generate Scripts:**

```
sdv teradata generate-validation-scripts \
  ./config.yaml \
  --output-directory ./scripts
```

Copy

**Get Templates:**

```
sdv teradata get-configuration-files \
  --templates-directory ./templates
```

Copy

For complete documentation, see [Teradata Commands Reference](teradata_commands).

---

### Amazon Redshift Commands[¶](#amazon-redshift-commands "Link to this heading")

For complete Amazon Redshift command documentation, see [Redshift Commands Reference](redshift_commands).

**Quick Links:**

* [Run Synchronous Validation](redshift_commands.html#run-synchronous-validation)
* [Run Asynchronous Validation](redshift_commands.html#run-asynchronous-validation)
* [Generate Validation Scripts](redshift_commands.html#generate-validation-scripts)
* [Get Configuration Templates](redshift_commands.html#get-configuration-templates)
* [Auto-Generate Configuration File](redshift_commands.html#auto-generate-configuration-file)
* [Connection Configuration](redshift_commands.html#amazon-redshift-connection-configuration)
* [Troubleshooting](redshift_commands.html#troubleshooting-redshift-connections)

#### Common Commands[¶](#id2 "Link to this heading")

**Run Validation:**

```
sdv redshift run-validation \
  --data-validation-config-file ./configs/redshift_validation.yaml
```

Copy

**Generate Scripts:**

```
sdv redshift generate-validation-scripts \
  --data-validation-config-file /path/to/config.yaml
```

Copy

**Get Templates:**

```
sdv redshift get-configuration-files \
  --templates-directory ./templates
```

Copy

For complete documentation, see [Redshift Commands Reference](redshift_commands).

---

## Configuration File Reference[¶](#configuration-file-reference "Link to this heading")

### Global Configuration[¶](#global-configuration "Link to this heading")

The global configuration section defines the overall behavior of the validation process.

```
# Platform configuration
source_platform: SqlServer  # Options: SqlServer, Teradata, Redshift, Snowflake
target_platform: Snowflake  # Currently only Snowflake is supported

# Output configuration
output_directory_path: /path/to/output/directory

# Threading configuration
max_threads: auto  # Options: "auto" or positive integer (1-32)

# Teradata-specific configuration (required only for Teradata)
target_database: TARGET_DB_NAME

# Directory path for source validation file
source_validation_files_path: /path/to/source_validation_file/directory

# Directory path for target validation file
target_validation_files_path: /path/to/target_validation_file/directory
```

Copy

#### Platform Configuration Options[¶](#platform-configuration-options "Link to this heading")

**`source_platform`** (required)

* **Type:** String
* **Valid Values:** `SqlServer`, `Teradata`, `Redshift`, `Snowflake`
* **Description:** The source database platform for validation
* **Example:** `source_platform: SqlServer`

**`target_platform`** (required)

* **Type:** String
* **Valid Values:** `Snowflake`
* **Description:** The target database platform (currently only Snowflake is supported)
* **Example:** `target_platform: Snowflake`

**`output_directory_path`** (required)

* **Type:** String (path)
* **Description:** Directory where validation results, logs, and reports will be saved
* **Example:** `output_directory_path: /home/user/validation_output`

**`max_threads`** (optional)

* **Type:** String or Integer
* **Valid Values:** `"auto"` or positive integer (1-32)
* **Default:** `"auto"`
* **Description:** Controls parallelization for validation operations

  + `"auto"`: Automatically detects optimal thread count based on CPU cores
  + Integer value: Specifies exact number of threads to use
* **Examples:**

  ```
  max_threads: auto        # Auto-detect optimal threads
  max_threads: 4           # Use exactly 4 threads
  max_threads: 16          # Use 16 threads
  ```

  Copy

**`target_database`** (required for Teradata only)

* **Type:** String
* **Description:** Target database name in Snowflake for Teradata validations
* **Example:** `target_database: PROD_DB`

**`source_validation_files_path`** (optional)

* **Type:** String (path)
* **Description:** Path to the directory containing the source validation files.
* **Example:** `source_validation_files_path: /path/to/source_validation_file/directory`

**`target_validation_files_path`** (optional)

* **Type:** String (path)
* **Description:** Path to the directory containing the target validation files.
* **Example:** `target_validation_files_path: /path/to/targetvalidation_file/directory`

---

### Connection Configuration[¶](#connection-configuration "Link to this heading")

Define how to connect to source and target databases.

#### Source Connection Configuration[¶](#source-connection-configuration "Link to this heading")

##### SQL Server Source Connection[¶](#sql-server-source-connection "Link to this heading")

```
source_connection:
  mode: credentials
  host: "sqlserver.company.com"
  port: 1433
  username: "sqlserver_user"
  password: "secure_password"
  database: "source_database"
  trust_server_certificate: "no"   # Optional: yes/no
  encrypt: "yes"                   # Optional: yes/no/optional
```

Copy

**Connection Fields:**

* **`mode`** (required)

  + **Type:** String
  + **Valid Values:** `credentials`
  + **Description:** Connection mode for SQL Server
* **`host`** (required)

  + **Type:** String
  + **Description:** SQL Server hostname or IP address
  + **Example:** `"sqlserver.company.com"` or `"192.168.1.100"`
* **`port`** (required)

  + **Type:** Integer
  + **Default:** 1433
  + **Description:** SQL Server port number
* **`username`** (required)

  + **Type:** String
  + **Description:** SQL Server authentication username
* **`password`** (required)

  + **Type:** String
  + **Description:** SQL Server authentication password
  + **Security Note:** Consider using environment variables or secret management
* **`database`** (required)

  + **Type:** String
  + **Description:** SQL Server database name
* **`trust_server_certificate`** (optional)

  + **Type:** String
  + **Valid Values:** `"yes"`, `"no"`
  + **Default:** `"no"`
  + **Description:** Whether to trust the server certificate for SSL/TLS connections
* **`encrypt`** (optional)

  + **Type:** String
  + **Valid Values:** `"yes"`, `"no"`, `"optional"`
  + **Default:** `"yes"`
  + **Description:** Connection encryption setting

##### Teradata Source Connection[¶](#teradata-source-connection "Link to this heading")

```
source_connection:
  mode: credentials
  host: "teradata.company.com"
  username: "teradata_user"
  password: "secure_password"
  database: "source_database"
```

Copy

**Connection Fields:**

* **`mode`** (required)

  + **Type:** String
  + **Valid Values:** `credentials`
* **`host`** (required)

  + **Type:** String
  + **Description:** Teradata hostname or IP address
* **`username`** (required)

  + **Type:** String
  + **Description:** Teradata authentication username
* **`password`** (required)

  + **Type:** String
  + **Description:** Teradata authentication password
* **`database`** (required)

  + **Type:** String
  + **Description:** Teradata database name

##### Amazon Redshift Source Connection[¶](#amazon-redshift-source-connection "Link to this heading")

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

**Connection Fields:**

* **`mode`** (required)

  + **Type:** String
  + **Valid Values:** `credentials`
* **`host`** (required)

  + **Type:** String
  + **Description:** Redshift cluster endpoint
* **`port`** (required)

  + **Type:** Integer
  + **Default:** 5439
  + **Description:** Redshift port number
* **`username`** (required)

  + **Type:** String
  + **Description:** Redshift authentication username
* **`password`** (required)

  + **Type:** String
  + **Description:** Redshift authentication password
* **`database`** (required)

  + **Type:** String
  + **Description:** Redshift database name

#### Target Connection (Snowflake)[¶](#target-connection-snowflake "Link to this heading")

Snowflake connections support three modes: `name`, `default`, and `credentials` (IPC only and SnowConvert exclusive).

##### Option 1: Named Connection[¶](#option-1-named-connection "Link to this heading")

Use a pre-configured Snowflake connection saved in your Snowflake connections file.

```
target_connection:
  mode: name
  name: "my_snowflake_connection"
```

Copy

**Fields:**

* **`mode`** (required): Must be `"name"`
* **`name`** (required): Name of the saved Snowflake connection

##### Option 2: Default Connection[¶](#option-2-default-connection "Link to this heading")

Use the default Snowflake connection from your environment.

```
target_connection:
  mode: default
```

Copy

**Fields:**

* **`mode`** (required): Must be `"default"`

##### Option 3: Credentials Mode (IPC Only)[¶](#option-3-credentials-mode-ipc-only "Link to this heading")

> **Note:** The `credentials` mode is only available when using IPC (Inter-Process Communication) commands directly via CLI parameters, not in YAML configuration files. This mode is exclusive to the SnowConvert UI.

---

### Validation Configuration[¶](#validation-configuration "Link to this heading")

Controls which validation levels are executed.

```
validation_configuration:
  schema_validation: true          # Level 1: Schema validation
  metrics_validation: true         # Level 2: Statistical metrics validation
  row_validation: false            # Level 3: Row-level data validation
  max_failed_rows_number: 100      # Maximum failed rows to report (applies only for row validation)
  exclude_metrics: false           # Exclude statistical metrics from validation
  apply_metric_column_modifier: false  # Apply column modifiers for metrics
  custom_templates_path: /path/to/templates  # Optional: Custom query templates
```

Copy

**Validation Options:**

* **`schema_validation`** (optional)

  + **Type:** Boolean
  + **Default:** `true`
  + **Description:** Validates table and column schema consistency
  + **Checks:**

    - Column names match between source and target
    - Data types are compatible
    - Column nullability settings
    - Primary key definitions
* **`metrics_validation`** (optional)

  + **Type:** Boolean
  + **Default:** `true`
  + **Description:** Validates statistical metrics for each column
  + **Checks:**

    - Row counts
    - Distinct value counts
    - Null value counts
    - Min/max values
    - Average, sum, standard deviation (for numeric columns)
* **`row_validation`** (optional)

  + **Type:** Boolean
  + **Default:** `false`
  + **Description:** Validates data at the row level using hash-based comparison

    - **Note:** Requires index columns for row identification. If not specified in the configuration, the tool attempts to auto-detect them from primary keys.
  + **Warning:** This is the most resource-intensive validation level
  + **Checks:**

    - MD5 hash comparison of row chunks
    - Identifies specific rows with differences
* **`max_failed_rows_number`** (optional)

  + **Type:** Integer
  + **Default:** 100
  + **Minimum:** 1
  + **Description:** Maximum number of failed rows to report per table
  + **Example:** `max_failed_rows_number: 250`
* **`exclude_metrics`** (optional)

  + **Type:** Boolean
  + **Default:** `false`
  + **Description:** When `true`, excludes certain statistical metrics (avg, sum, stddev, variance) from validation
  + **Use Case:** Useful for large tables where statistical calculations might cause an overflow.
* **`apply_metric_column_modifier`** (optional)

  + **Type:** Boolean
  + **Default:** `true`
  + **Description:** Applies column modifiers defined in metric templates
  + **Use Case:** Advanced users with custom metric calculations
* **`custom_templates_path`** (optional)

  + **Type:** String (path)
  + **Description:** Path to directory containing custom Jinja2 query templates
  + **Example:** `custom_templates_path: /opt/validation/custom_templates`

---

### Table Configuration[¶](#table-configuration "Link to this heading")

Defines which tables to validate and how to validate them.

```
tables:
  # Table 1: Include specific columns
  - fully_qualified_name: database.schema.table1
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - customer_id
      - customer_name
      - email
    index_column_list:
      - customer_id
    where_clause: "status = 'ACTIVE'"
    target_where_clause: "status = 'ACTIVE'"
    is_case_sensitive: false
    chunk_number: 10
    max_failed_rows_number: 50
    column_mappings:
      customer_id: cust_id
      customer_name: name

  # Table 2: Exclude specific columns
  - fully_qualified_name: database.schema.table2
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - audit_timestamp
      - created_by
      - modified_by
    index_column_list: []

  # Table 3: Simple configuration
  - fully_qualified_name: database.schema.table3
    use_column_selection_as_exclude_list: false
    column_selection_list: []
```

Copy

**Table Configuration Fields:**

* **`fully_qualified_name`** (required)

  + **Type:** String
  + **Format:** `database.schema.table` or `schema.table`
  + **Description:** Full table identifier in the source database
  + **Examples:**

    ```
    fully_qualified_name: my_database.dbo.customers
    fully_qualified_name: public.orders  # For Redshift
    ```

    Copy
* **`target_database`** (optional)

  + **Type:** String
  + **Default:** Source database name from fully\_qualified\_name field
  + **Description:** Target database name if different from source database name
  + **Example:**

    ```
    target_database: target_database_name
    ```

    Copy
* **`target_schema`** (optional)

  + **Type:** String
  + **Default:** Source schema name from fully\_qualified\_name field
  + **Description:** Target schema name if different from source schema name
  + **Example:**

    ```
    target_schema: target_schema_name
    ```

    Copy
* **`target_name`** (optional)

  + **Type:** String
  + **Default:** Source table name from fully\_qualified\_name field
  + **Description:** Target table name if different from source table name
  + **Example:**

    ```
    target_name: customers_new
    ```

    Copy
* **`use_column_selection_as_exclude_list`** (required)

  + **Type:** Boolean
  + **Description:** Determines how `column_selection_list` is interpreted

    - `false`: Include only the specified columns
    - `true`: Exclude the specified columns (include all others)
  + **Examples:**

    ```
    # Include only these columns
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - id
      - name
      - email

    # Exclude these columns (include all others)
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - internal_notes
      - audit_timestamp
    ```

    Copy
* **`column_selection_list`** (required)

  + **Type:** List of strings
  + **Description:** List of column names to include or exclude
  + **Note:** Use an empty list `[]` to include all columns
* **`index_column_list`** (optional)

  + **Type:** List of strings
  + **Default:** Auto-detected from primary keys
  + **Description:** Columns to use as unique identifiers for row validation
  + **Use Case:** Specify when the table doesn’t have a primary key or you want to use different columns
  + **Example:**

    ```
    index_column_list:
      - customer_id
      - order_date
    ```

    Copy
* **`target_index_column_list`** (optional)

  + **Type:** List of strings
  + **Description:** Index columns in the target table (if different from source)
  + **Note:** Automatically derived from `column_mappings` if not specified
* **`where_clause`** (optional)

  + **Type:** String
  + **Default:** `""` (empty, no filter)
  + **Description:** SQL WHERE clause to filter source data (without “WHERE” keyword)
  + **Examples:**

    ```
    where_clause: "created_date >= '2024-01-01'"
    where_clause: "status IN ('ACTIVE', 'PENDING') AND region = 'US'"
    where_clause: "amount > 1000 AND customer_type = 'PREMIUM'"
    ```

    Copy
* **`target_where_clause`** (optional)

  + **Type:** String
  + **Default:** `""` (empty, no filter)
  + **Description:** SQL WHERE clause to filter target data
  + **Best Practice:** Should match `where_clause` to ensure consistent comparison
  + **Example:**

    ```
    target_where_clause: "created_date >= '2024-01-01'"
    ```

    Copy
* **`is_case_sensitive`** (optional)

  + **Type:** Boolean
  + **Default:** `false`
  + **Description:** Whether column name matching should be case-sensitive
* **`chunk_number`** (optional)

  + **Type:** Integer
  + **Default:** 0 (no chunking)
  + **Minimum:** 0
  + **Description:** Number of chunks to split row validation into
  + **Use Case:** Large tables benefit from chunking for better performance
  + **Example:**

    ```
    chunk_number: 20  # Split into 20 chunks for parallel processing
    ```

    Copy
* **`max_failed_rows_number`** (optional)

  + **Type:** Integer
  + **Minimum:** 1
  + **Description:** Maximum failed rows to report for this specific table
  + **Note:** Overrides the global `max_failed_rows_number` setting
* **`column_mappings`** (optional)

  + **Type:** Dictionary (key-value pairs)
  + **Description:** Maps source column names to target column names when they differ
  + **Format:** `source_column_name: target_column_name`
  + **Example:**

    ```
    column_mappings:
      cust_id: customer_id
      cust_name: customer_name
      addr: address
    ```

    Copy
* **`exclude_metrics`** (optional)

  + **Type:** Boolean
  + **Description:** Exclude metrics validation for this specific table
  + **Note:** Overrides the global `exclude_metrics` setting
* **`apply_metric_column_modifier`** (optional)

  + **Type:** Boolean
  + **Description:** Apply column modifiers for this specific table
  + **Note:** Overrides the global `apply_metric_column_modifier` setting

---

### Comparison Configuration[¶](#comparison-configuration "Link to this heading")

Controls comparison behavior and tolerance levels.

```
comparison_configuration:
  tolerance: 0.01  # 1% tolerance for statistical comparisons
```

Copy

**Comparison Options:**

* **`tolerance`** (optional)

  + **Type:** Float
  + **Default:** 0.001 (0.1%)
  + **Description:** Acceptable tolerance for statistical metric differences
  + **Use Case:** Allows for small differences due to rounding or data type conversions
  + **Examples:**

    ```
    tolerance: 0.001   # 0.1% tolerance (very strict)
    tolerance: 0.01    # 1% tolerance (recommended)
    tolerance: 0.05    # 5% tolerance (lenient)
    ```

    Copy

---

### Logging Configuration[¶](#logging-configuration "Link to this heading")

Controls logging behavior for validation operations.

```
logging_configuration:
  level: INFO              # Overall logging level
  console_level: WARNING   # Console-specific level
  file_level: DEBUG        # File-specific level
```

Copy

**Logging Options:**

* **`level`** (optional)

  + **Type:** String
  + **Valid Values:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  + **Default:** `INFO`
  + **Description:** Default logging level for all loggers
  + **Level Descriptions:**

    - `DEBUG`: Detailed diagnostic information
    - `INFO`: General informational messages
    - `WARNING`: Warning messages for potentially problematic situations
    - `ERROR`: Error messages for serious issues
    - `CRITICAL`: Critical errors that may cause application failure
* **`console_level`** (optional)

  + **Type:** String
  + **Valid Values:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  + **Default:** Same as `level`
  + **Description:** Logging level for console output
  + **Use Case:** Set to `WARNING` or `ERROR` to reduce console noise
* **`file_level`** (optional)

  + **Type:** String
  + **Valid Values:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  + **Default:** Same as `level`
  + **Description:** Logging level for file output
  + **Use Case:** Set to `DEBUG` for detailed file logs while keeping console clean

**Example Configurations:**

```
# Verbose logging for troubleshooting
logging_configuration:
  level: DEBUG
  console_level: DEBUG
  file_level: DEBUG

# Production-friendly logging
logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: INFO

# Minimal console output with detailed file logs
logging_configuration:
  level: INFO
  console_level: ERROR
  file_level: DEBUG
```

Copy

**Note:** CLI `--log-level` parameter overrides configuration file settings.

---

### Database and Schema Mappings[¶](#database-and-schema-mappings "Link to this heading")

Map source database/schema names to target names when they differ.

```
database_mappings:
  source_db1: target_db1
  source_db2: target_db2
  legacy_database: modern_database

schema_mappings:
  dbo: public
  source_schema: target_schema
  old_schema: new_schema
```

Copy

**Mapping Options:**

* **`database_mappings`** (optional)

  + **Type:** Dictionary
  + **Description:** Maps source database names to target database names
  + **Use Case:** When database names differ between source and Snowflake
  + **Example:**

    ```
    database_mappings:
      PROD_SQL: PROD_SNOWFLAKE
      DEV_SQL: DEV_SNOWFLAKE
    ```

    Copy
* **`schema_mappings`** (optional)

  + **Type:** Dictionary
  + **Description:** Maps source schema names to target schema names
  + **Use Case:** When schema names differ between source and Snowflake
  + **Example:**

    ```
    schema_mappings:
      dbo: PUBLIC
      sales: SALES_DATA
      hr: HUMAN_RESOURCES
    ```

    Copy

---

## Complete Configuration Examples[¶](#complete-configuration-examples "Link to this heading")

### Example 1: SQL Server to Snowflake - Basic Validation[¶](#example-1-sql-server-to-snowflake-basic-validation "Link to this heading")

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

# Comparison configuration
comparison_configuration:
  tolerance: 0.01

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

### Example 2: Teradata to Snowflake - Comprehensive Validation[¶](#example-2-teradata-to-snowflake-comprehensive-validation "Link to this heading")

```
# Global configuration
source_platform: Teradata
target_platform: Snowflake
output_directory_path: /opt/validation/results
max_threads: 8
target_database: PROD_SNOWFLAKE

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
  row_validation: true
  max_failed_rows_number: 100
  exclude_metrics: false
  apply_metric_column_modifier: false

# Comparison configuration
comparison_configuration:
  tolerance: 0.005

# Logging configuration
logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: DEBUG

# Schema mappings
schema_mappings:
  prod_db: PUBLIC

# Tables configuration
tables:
  - fully_qualified_name: prod_db.sales_data
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - transaction_id
      - customer_id
      - amount
      - transaction_date
    index_column_list:
      - transaction_id
    chunk_number: 10
    max_failed_rows_number: 50

  - fully_qualified_name: prod_db.customer_master
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - credit_card
    where_clause: "status = 'ACTIVE'"
    target_where_clause: "status = 'ACTIVE'"
    column_mappings:
      cust_id: customer_id
      cust_name: customer_name
```

Copy

### Example 3: Redshift to Snowflake - Advanced Configuration[¶](#example-3-redshift-to-snowflake-advanced-configuration "Link to this heading")

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
  - fully_qualified_name: analytics_db.public.fact_sales
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - sale_id
    chunk_number: 50
    max_failed_rows_number: 500

  # Dimension table with column mappings
  - fully_qualified_name: analytics_db.public.dim_customer
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
  - fully_qualified_name: analytics_db.staging.incremental_load
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - load_timestamp
      - etl_batch_id
    where_clause: "load_date >= CURRENT_DATE - 7"
    target_where_clause: "load_date >= CURRENT_DATE - 7"
    chunk_number: 10
```

Copy

### Example 4: Minimal Configuration[¶](#example-4-minimal-configuration "Link to this heading")

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./output

source_connection:
  mode: credentials
  host: localhost
  port: 1433
  username: sa
  password: password
  database: test_db

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

tables:
  - fully_qualified_name: test_db.dbo.test_table
    use_column_selection_as_exclude_list: false
    column_selection_list: []
```

Copy

---

## Advanced Usage[¶](#advanced-usage "Link to this heading")

### Working with Large Tables[¶](#working-with-large-tables "Link to this heading")

For large tables, consider these optimization strategies:

#### Enable Chunking[¶](#enable-chunking "Link to this heading")

```
tables:
  - fully_qualified_name: database.schema.large_table
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    chunk_number: 100  # Split into 100 chunks
    index_column_list:
      - primary_key_column
```

Copy

#### Increase Thread Count[¶](#increase-thread-count "Link to this heading")

```
max_threads: 32  # Use maximum threads for parallel processing
```

Copy

#### 3. Filter Data[¶](#filter-data "Link to this heading")

```
tables:
  - fully_qualified_name: database.schema.large_table
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    where_clause: "created_date >= '2024-01-01' AND region = 'US'"
    target_where_clause: "created_date >= '2024-01-01' AND region = 'US'"
```

Copy

#### Selective Column Validation[¶](#selective-column-validation "Link to this heading")

```
tables:
  - fully_qualified_name: database.schema.large_table
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - large_text_column
      - large_binary_column
      - xml_column
```

Copy

### Using Custom Query Templates[¶](#using-custom-query-templates "Link to this heading")

For advanced users, you can provide custom Jinja2 templates:

```
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  custom_templates_path: /opt/custom_templates
```

Copy

Custom template directory structure:

```
/opt/custom_templates/
├── sqlserver_columns_metrics_query.sql.j2
├── sqlserver_row_count_query.sql.j2
├── sqlserver_compute_md5_sql.j2
└── snowflake_columns_metrics_query.sql.j2
```

Copy

### Asynchronous Validation Workflow[¶](#asynchronous-validation-workflow "Link to this heading")

For environments with restricted database access or long-running validations:

#### Step 1: Generate Scripts[¶](#step-1-generate-scripts "Link to this heading")

```
sdv sqlserver generate-validation-scripts \
  --data-validation-config-file config.yaml
```

Copy

This generates SQL scripts in the output directory.

#### Step 2: Execute Scripts Manually[¶](#step-2-execute-scripts-manually "Link to this heading")

Execute the generated scripts on source and target databases, saving results to CSV files.

#### Step 3: Run Async Validation[¶](#step-3-run-async-validation "Link to this heading")

```
sdv sqlserver run-async-validation \
  --data-validation-config-file config.yaml
```

Copy

This compares the pre-generated metadata files.

### CI/CD Integration[¶](#ci-cd-integration "Link to this heading")

Integrate validation into your deployment pipeline:

```
#!/bin/bash
# validate_migration.sh

CONFIG_FILE="./configs/validation_config.yaml"
LOG_LEVEL="INFO"

# Run validation
sdv sqlserver run-validation \
  --data-validation-config-file "$CONFIG_FILE" \
  --log-level "$LOG_LEVEL"

# Check exit code
if [ $? -eq 0 ]; then
  echo "✓ Validation passed successfully"
  exit 0
else
  echo "✗ Validation failed"
  exit 1
fi
```

Copy

### Handling Multiple Environments[¶](#handling-multiple-environments "Link to this heading")

Create separate configuration files for each environment:

```
configs/
├── dev_validation.yaml
├── staging_validation.yaml
└── prod_validation.yaml
```

Copy

Run validation for specific environment:

```
# Development
sdv sqlserver run-validation --data-validation-config-file configs/dev_validation.yaml

# Staging
sdv sqlserver run-validation --data-validation-config-file configs/staging_validation.yaml

# Production
sdv sqlserver run-validation --data-validation-config-file configs/prod_validation.yaml
```

Copy

---

## Validation Reports[¶](#validation-reports "Link to this heading")

### Overview[¶](#id3 "Link to this heading")

The Snowflake Data Validation tool generates comprehensive CSV reports that document the results of data migration validations between source and target databases. These reports help identify discrepancies in schema, metrics, and row-level data.

### Report Types[¶](#report-types "Link to this heading")

The validation tool generates different types of reports based on the validation levels configured:

#### 1. Main Validation Report (`validation_report.csv`)[¶](#main-validation-report-validation-report-csv "Link to this heading")

This consolidated report contains results from schema and metrics validations for all tables.

#### 2. Row Validation Reports (per table)[¶](#row-validation-reports-per-table "Link to this heading")

Separate reports generated for each table when row validation is enabled, containing detailed row-level comparison results.

---

### Main Validation Report Structure[¶](#main-validation-report-structure "Link to this heading")

The main validation report contains the following columns:

| Column Name | Description |
| --- | --- |
| **VALIDATION\_TYPE** | Type of validation performed: `SCHEMA VALIDATION` or `METRICS VALIDATION` |
| **TABLE** | Fully qualified name of the table being validated (e.g., `database.schema.table`) |
| **COLUMN\_VALIDATED** | Name of the column being validated (or table-level attribute for schema validation) |
| **EVALUATION\_CRITERIA** | The specific property being compared (e.g., `DATA_TYPE`, `NULLABLE`, `ROW_COUNT`, `min`, `max`) |
| **SOURCE\_VALUE** | The value from the source database |
| **SNOWFLAKE\_VALUE** | The value from the target (Snowflake) database |
| **STATUS** | Validation result status (see Status Values section below) |
| **COMMENTS** | Additional context or explanation for the validation result |

---

### Validation Types Explained[¶](#validation-types-explained "Link to this heading")

#### Schema Validation[¶](#schema-validation "Link to this heading")

Compares structural metadata between source and target tables:

* **Column existence**: Ensures columns present in source exist in target
* **Data types**: Validates column data types match (with configurable mappings)
* **Nullability**: Checks if NULL constraints match between source and target
* **Primary keys**: Verifies primary key definitions
* **Column precision/scale**: Validates numeric precision and scale values
* **Character length**: Compares VARCHAR/CHAR column lengths

**Example Schema Validation Row:**

```
SCHEMA VALIDATION,mydb.myschema.customers,customer_id,DATA_TYPE,INT,NUMBER,FAILURE,"Data type mismatch detected"
```

Copy

#### Metrics Validation[¶](#metrics-validation "Link to this heading")

Compares statistical metrics calculated on column data:

* **Row count**: Total number of rows in the table
* **min**: Minimum value in numeric/date columns
* **max**: Maximum value in numeric/date columns
* **count**: Count of non-null values
* **count\_distinct**: Number of distinct values
* **avg**, **sum**, **stddev**, **variance**: Statistical measures (can be excluded via configuration)

**Example Metrics Validation Row:**

```
METRICS VALIDATION,mydb.myschema.orders,order_date,max,2024-12-31,2024-12-31,SUCCESS,""
```

Copy

#### Row Validation[¶](#row-validation "Link to this heading")

Generates separate per-table reports comparing actual row data using MD5 checksums to detect differences.

---

### Row Validation Report Structure[¶](#row-validation-report-structure "Link to this heading")

Row validation reports have a different structure focused on identifying specific rows with differences:

| Column Name | Description |
| --- | --- |
| **ROW\_NUMBER** | Sequential row number in the report |
| **TABLE\_NAME** | Fully qualified table name |
| **RESULT** | Outcome of the row comparison (see Result Values below) |
| **[INDEX\_COLUMNS]\_SOURCE** | Primary key/index column values from source |
| **[INDEX\_COLUMNS]\_TARGET** | Primary key/index column values from target |
| **SOURCE\_QUERY** | SQL query to retrieve the row from source database |
| **TARGET\_QUERY** | SQL query to retrieve the row from target database |

---

### Status Values[¶](#status-values "Link to this heading")

The **STATUS** column in the main validation report can have the following values:

| Status | Meaning |
| --- | --- |
| **SUCCESS** | Validation passed - values match between source and target |
| **FAILURE** | Validation failed - values differ between source and target |
| **WARNING** | Potential issue detected that may require attention |
| **NOT\_FOUND\_SOURCE** | Element exists in target but not in source |
| **NOT\_FOUND\_TARGET** | Element exists in source but not in target |

---

### Result Values (Row Validation)[¶](#result-values-row-validation "Link to this heading")

The **RESULT** column in row validation reports can have the following values:

| Result | Meaning |
| --- | --- |
| **SUCCESS** | Row data matches between source and target |
| **FAILURE** | Row data differs between source and target (MD5 checksum mismatch) |
| **NOT\_FOUND\_SOURCE** | Row exists in target but not in source |
| **NOT\_FOUND\_TARGET** | Row exists in source but not in target |

---

### Understanding Validation Results[¶](#understanding-validation-results "Link to this heading")

#### Interpreting Schema Validation Results[¶](#interpreting-schema-validation-results "Link to this heading")

**Success Scenario:**

* All columns exist in both source and target
* Data types match (considering configured type mappings)
* Nullability constraints are consistent
* All structural attributes align

**Common Failure Scenarios:**

1. **Data Type Mismatch**

   * Source: `VARCHAR(50)`, Target: `VARCHAR(100)`
   * Status: May be SUCCESS if within tolerance, or FAILURE if strict matching is required
2. **Missing Column**

   * Source has column `phone_number`, target does not
   * Status: NOT\_FOUND\_TARGET
3. **Nullability Difference**

   * Source: `NOT NULL`, Target: `NULL`
   * Status: FAILURE

#### Interpreting Metrics Validation Results[¶](#interpreting-metrics-validation-results "Link to this heading")

**Success Scenario:**

* Row counts match exactly
* Statistical metrics are within configured tolerance (default: 0.1%)
* All calculated metrics align between source and target

**Common Failure Scenarios:**

1. **Row Count Mismatch**

   * Source: 10,000 rows, Target: 9,998 rows
   * Status: FAILURE
   * Action: Investigate missing rows
2. **Min/Max Value Differences**

   * Source max date: `2024-12-31`, Target max date: `2024-12-30`
   * Status: FAILURE
   * Action: Check for incomplete data migration
3. **Statistical Variance**

   * Source count\_distinct: 1,000, Target count\_distinct: 995
   * Status: FAILURE (if beyond tolerance)
   * Action: Investigate potential duplicates or missing values

#### Interpreting Row Validation Results[¶](#interpreting-row-validation-results "Link to this heading")

**Success Scenario:**

* All rows in source have matching rows in target (by MD5 checksum)
* No orphaned rows in either database
* Primary key values align correctly

**Common Failure Scenarios:**

1. **Row Content Mismatch**

   * Same primary key, different column values
   * Result: FAILURE
   * Action: Use provided SQL queries to investigate specific differences
2. **Missing Rows**

   * Row exists in source but not in target
   * Result: NOT\_FOUND\_TARGET
   * Action: Check migration completeness
3. **Extra Rows**

   * Row exists in target but not in source
   * Result: NOT\_FOUND\_SOURCE
   * Action: Investigate unexpected data in target

---

### Using the Reports[¶](#using-the-reports "Link to this heading")

#### Quick Assessment[¶](#quick-assessment "Link to this heading")

1. **Filter by STATUS column**: Focus on `FAILURE`, `WARNING`, `NOT_FOUND_SOURCE`, and `NOT_FOUND_TARGET` rows
2. **Group by VALIDATION\_TYPE**: Assess schema issues separately from metrics issues
3. **Group by TABLE**: Identify which tables have the most issues

#### Investigating Failures[¶](#investigating-failures "Link to this heading")

**For Schema Validation:**

1. Review the `EVALUATION_CRITERIA` to understand what attribute failed
2. Compare `SOURCE_VALUE` vs `SNOWFLAKE_VALUE`
3. Check if differences are acceptable (e.g., VARCHAR size increase)
4. Update type mappings or schema definitions if needed

**For Metrics Validation:**

1. Review the metric that failed (e.g., `row_count`, `max`, `min`)
2. Calculate the difference magnitude
3. Determine if within acceptable business tolerance
4. Use the detailed queries to investigate source of discrepancy

**For Row Validation:**

1. Open the table-specific row validation report
2. Identify rows with `FAILURE` status
3. Use the provided `SOURCE_QUERY` and `TARGET_QUERY` to retrieve actual row data
4. Compare column-by-column to identify specific field differences
5. Investigate why values differ (data type conversion, truncation, transformation)

---

### Configuration Options Affecting Reports[¶](#configuration-options-affecting-reports "Link to this heading")

#### Tolerance Settings[¶](#tolerance-settings "Link to this heading")

The `comparison_configuration.tolerance` setting affects metrics validation:

```
comparison_configuration:
  tolerance: 0.01  # 1% tolerance for numeric comparisons
```

Copy

* Values within tolerance are marked as SUCCESS
* Values beyond tolerance are marked as FAILURE

#### Validation Levels[¶](#validation-levels "Link to this heading")

Control which validations run and therefore which reports are generated:

```
validation_configuration:
  schema_validation: true    # Validates table/column structure
  metrics_validation: true   # Validates statistical metrics
  row_validation: false      # Validates individual row data (resource intensive)
```

Copy

#### Excluded Metrics[¶](#excluded-metrics "Link to this heading")

Exclude specific metrics from validation:

```
validation_configuration:
  exclude_metrics: true  # Excludes avg, sum, stddev, variance
```

Copy

#### Maximum Failed Rows[¶](#maximum-failed-rows "Link to this heading")

Limit the number of failed rows reported in row validation:

```
validation_configuration:
  max_failed_rows_number: 100  # Report up to 100 failed rows per table
```

Copy

---

### Report File Locations[¶](#report-file-locations "Link to this heading")

Reports are generated in the configured output directory:

```
<output_directory_path>/
├── <timestamp>_validation_report.csv          # Main consolidated report
├── <timestamp>_database.schema.table1_1.csv   # Row validation for table1
├── <timestamp>_database.schema.table2_2.csv   # Row validation for table2
└── data_validation_<timestamp>.log            # Detailed execution log
```

Copy

**File naming convention:**

* Timestamp format: `YYYY-MM-DD_HH-MM-SS`
* Row validation reports include table name and unique ID to prevent collisions

---

### Best Practices[¶](#best-practices "Link to this heading")

1. **Start with Schema Validation**: Ensure structural alignment before validating data
2. **Use Appropriate Tolerance**: Set realistic tolerance thresholds for metrics validation
3. **Selective Row Validation**: Enable row validation only for critical tables (resource intensive)
4. **Iterative Approach**: Fix schema issues first, then metrics, then row-level differences
5. **Document Acceptable Differences**: Some type conversions or value transformations may be expected
6. **Automate Report Analysis**: Use scripts to parse CSV reports and flag critical issues
7. **Preserve Reports**: Archive validation reports for audit trails and compliance

---

### Troubleshooting Report Issues[¶](#troubleshooting-report-issues "Link to this heading")

#### All Validations Showing FAILURE[¶](#all-validations-showing-failure "Link to this heading")

**Possible Causes:**

* Incorrect database/schema mappings in configuration
* Type mapping file not loaded correctly
* Connection to wrong target database

**Solution:** Verify `database_mappings`, `schema_mappings`, and connection settings

#### Row Validation Shows All NOT\_FOUND\_TARGET[¶](#row-validation-shows-all-not-found-target "Link to this heading")

**Possible Causes:**

* Target table empty or not migrated yet
* Incorrect target table name
* Primary key/index columns mismatch

**Solution:** Verify target table exists and contains data, check column mappings

#### Metrics Validation Shows Large Differences[¶](#metrics-validation-shows-large-differences "Link to this heading")

**Possible Causes:**

* Incomplete data migration
* Data type conversion issues causing value changes
* Filter/WHERE clause differences between source and target queries

**Solution:** Review migration logs, verify row counts first, check data transformations

#### Report File Not Generated[¶](#report-file-not-generated "Link to this heading")

**Possible Causes:**

* Output directory doesn’t exist or lacks write permissions
* Validation configuration has all levels set to false
* Application crashed before report generation

**Solution:** Check output path permissions, review logs for errors, enable at least one validation level

---

## Troubleshooting[¶](#troubleshooting "Link to this heading")

### Common Issues and Solutions[¶](#common-issues-and-solutions "Link to this heading")

#### Issue: “Configuration file not found”[¶](#issue-configuration-file-not-found "Link to this heading")

**Symptom:**

```
Configuration file not found: ./config.yaml
```

Copy

**Solution:**

* Verify the file path is correct
* Use absolute paths: `/home/user/configs/validation.yaml`
* Check file permissions

#### Issue: “Connection error”[¶](#issue-connection-error "Link to this heading")

**Symptom:**

```
Connection error: Unable to connect to database
```

Copy

**Solutions:**

1. **Verify connection parameters:**

   ```
   source_connection:
     host: correct-hostname.com  # Verify hostname
     port: 1433                  # Verify port
     username: valid_user        # Verify username
     password: correct_password  # Verify password
   ```

   Copy
2. **Check network connectivity:**

   ```
   # Test connection to SQL Server
   telnet sqlserver.company.com 1433

   # Test connection to Teradata
   telnet teradata.company.com 1025

   # Test connection to Redshift
   telnet redshift-cluster.amazonaws.com 5439
   ```

   Copy
3. **Verify firewall rules** allow connections from your machine
4. **For SQL Server SSL issues:**

   ```
   source_connection:
     trust_server_certificate: "yes"  # Try this if SSL errors occur
     encrypt: "optional"
   ```

   Copy

#### Issue: “Invalid parameter”[¶](#issue-invalid-parameter "Link to this heading")

**Symptom:**

```
Invalid parameter: max_threads must be 'auto' or a positive integer
```

Copy

**Solution:**

```
# Correct
max_threads: auto
max_threads: 4

# Incorrect
max_threads: "4"      # Remove quotes
max_threads: 0        # Must be positive
max_threads: -1       # Must be positive
```

Copy

#### Issue: “Table not found”[¶](#issue-table-not-found "Link to this heading")

**Symptom:**

```
Table not found: database.schema.table_name
```

Copy

**Solutions:**

1. **Verify fully qualified name:**

   ```
   # For SQL Server and Teradata
   fully_qualified_name: database_name.schema_name.table_name

   # For Redshift (no database in FQN)
   fully_qualified_name: schema_name.table_name
   ```

   Copy
2. **Check case sensitivity:**

   ```
   tables:
     - fully_qualified_name: MyDatabase.MySchema.MyTable
       is_case_sensitive: true  # Match exact case
   ```

   Copy
3. **Verify table exists in source database**

#### Issue: “YAML formatting error”[¶](#issue-yaml-formatting-error "Link to this heading")

**Symptom:**

```
Error in the format of config.yaml
```

Copy

**Solutions:**

1. **Check indentation (use spaces, not tabs)**

   ```
   # Correct
   tables:
     - fully_qualified_name: db.schema.table
       column_selection_list:
         - column1
         - column2
   ```

   Copy

   Incorrect example (mixed indentation with tabs):

   ```
   tables:
   	- fully_qualified_name: db.schema.table
   	  column_selection_list:
   	    - column1
   ```

   Copy
2. **Quote special characters:**

   ```
   password: "p@ssw0rd!"    # Quote passwords with special chars
   where_clause: "name = 'O''Brien'"  # Escape quotes
   ```

   Copy
3. **Validate YAML syntax** using online validators or:

   ```
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

   Copy

#### Issue: “Validation fails with tolerance errors”[¶](#issue-validation-fails-with-tolerance-errors "Link to this heading")

**Symptom:**

```
Metrics validation failed: Difference exceeds tolerance
```

Copy

**Solution:**
Adjust tolerance in configuration:

```
comparison_configuration:
  tolerance: 0.05  # Increase to 5% tolerance
```

Copy

#### Issue: “Out of memory errors with large tables”[¶](#issue-out-of-memory-errors-with-large-tables "Link to this heading")

**Solutions:**

1. **Enable chunking:**

   ```
   tables:
     - fully_qualified_name: large_table
       chunk_number: 100  # Process in smaller chunks
   ```

   Copy
2. **Reduce thread count:**

   ```
   max_threads: 4  # Use fewer threads
   ```

   Copy
3. **Filter data:**

   ```
   tables:
     - fully_qualified_name: large_table
       where_clause: "created_date >= '2024-01-01'"
   ```

   Copy
4. **Exclude large columns:**

   ```
   tables:
     - fully_qualified_name: large_table
       use_column_selection_as_exclude_list: true
       column_selection_list:
         - large_blob_column
         - large_text_column
   ```

   Copy

### Getting Help[¶](#getting-help "Link to this heading")

1. **Check logs:** Review log files in the output directory
2. **Enable debug logging:**

   ```
   sdv sqlserver run-validation \
     --data-validation-config-file config.yaml \
     --log-level DEBUG
   ```

   Copy
3. **Review validation reports** in the output directory
4. **Consult documentation:** [Full Documentation](https://github.com/snowflakedb/migrations-data-validation)
5. **Report issues:** Email us at:[snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

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
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Best Practices & Guidance](#best-practices-guidance)
6. [CLI Commands](#cli-commands)
7. [Configuration File Reference](#configuration-file-reference)
8. [Complete Configuration Examples](#complete-configuration-examples)
9. [Advanced Usage](#advanced-usage)
10. [Validation Reports](#validation-reports)
11. [Troubleshooting](#troubleshooting)