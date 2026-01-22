---
auto_generated: true
description: This document provides ready-to-use configuration examples for various
  validation scenarios. Copy and adapt these examples for your specific use case.
last_scraped: '2026-01-14T16:52:13.328476+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/CONFIGURATION_EXAMPLES
title: Configuration File Examples | Snowflake Documentation
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)Configuration Examples

# Configuration File Examples[¶](#configuration-file-examples "Link to this heading")

This document provides ready-to-use configuration examples for various validation scenarios. Copy and adapt these examples for your specific use case.

## Table of Contents[¶](#table-of-contents "Link to this heading")

* [SQL Server Examples](#sql-server-examples)
* [Teradata Examples](#teradata-examples)
* [Redshift Examples](#redshift-examples)
* [Scenario-Based Examples](#scenario-based-examples)

---

## SQL Server Examples[¶](#sql-server-examples "Link to this heading")

### Example 1: Minimal SQL Server Configuration[¶](#example-1-minimal-sql-server-configuration "Link to this heading")

Perfect for quick testing or simple validations.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./validation_output

source_connection:
  mode: credentials
  host: localhost
  port: 1433
  username: sa
  password: YourPassword123
  database: TestDB

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

tables:
  - fully_qualified_name: TestDB.dbo.Customers
    use_column_selection_as_exclude_list: false
    column_selection_list: []
```

Copy

### Example 2: Production SQL Server with SSL/TLS[¶](#example-2-production-sql-server-with-ssl-tls "Link to this heading")

Secure production setup with proper encryption settings.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: /data/validation/production
max_threads: 16

source_connection:
  mode: credentials
  host: sqlserver-prod.company.com
  port: 1433
  username: validation_user
  password: SecurePassword123!
  database: PRODUCTION_DB
  trust_server_certificate: "no"
  encrypt: "yes"

target_connection:
  mode: name
  name: snowflake_production

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 250

comparison_configuration:
  tolerance: 0.01

logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: DEBUG

database_mappings:
  PRODUCTION_DB: PROD_SNOWFLAKE

schema_mappings:
  dbo: PUBLIC

tables:
  - fully_qualified_name: PRODUCTION_DB.dbo.Orders
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
    chunk_number: 20

  - fully_qualified_name: PRODUCTION_DB.dbo.Customers
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - credit_card_number
    index_column_list:
      - customer_id

  - fully_qualified_name: PRODUCTION_DB.dbo.Products
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - product_id
      - product_name
      - price
      - category
    where_clause: "is_active = 1"
    target_where_clause: "is_active = 1"
```

Copy

### Example 3: SQL Server Incremental Validation[¶](#example-3-sql-server-incremental-validation "Link to this heading")

Validate only recent changes using date filters.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./incremental_validation
max_threads: auto

source_connection:
  mode: credentials
  host: sqlserver.company.com
  port: 1433
  username: etl_user
  password: EtlPassword123
  database: DataWarehouse

target_connection:
  mode: name
  name: snowflake_dw

validation_configuration:
  schema_validation: false
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 100

comparison_configuration:
  tolerance: 0.001

tables:
  - fully_qualified_name: DataWarehouse.dbo.FactSales
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - transaction_id
    where_clause: "transaction_date >= DATEADD(day, -7, GETDATE())"
    target_where_clause: "transaction_date >= DATEADD(day, -7, CURRENT_TIMESTAMP)"
    chunk_number: 10

  - fully_qualified_name: DataWarehouse.dbo.DimCustomer
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    where_clause: "modified_date >= DATEADD(day, -7, GETDATE())"
    target_where_clause: "modified_date >= DATEADD(day, -7, CURRENT_TIMESTAMP)"
```

Copy

### Example 4: SQL Server with Column Mappings[¶](#example-4-sql-server-with-column-mappings "Link to this heading")

Handle renamed columns during migration.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./validation_with_mappings
max_threads: 8

source_connection:
  mode: credentials
  host: legacy-sql.company.com
  port: 1433
  username: migration_user
  password: MigrationPass123
  database: LegacyDB

target_connection:
  mode: name
  name: snowflake_modernized

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true

tables:
  - fully_qualified_name: LegacyDB.dbo.CustomerMaster
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - cust_id
      - cust_name
      - cust_email
      - cust_phone
      - addr_line1
      - addr_line2
      - addr_city
      - addr_state
      - addr_zip
    index_column_list:
      - cust_id
    column_mappings:
      cust_id: customer_id
      cust_name: customer_name
      cust_email: email_address
      cust_phone: phone_number
      addr_line1: address_line_1
      addr_line2: address_line_2
      addr_city: city
      addr_state: state
      addr_zip: postal_code
```

Copy

---

## Teradata Examples[¶](#teradata-examples "Link to this heading")

### Example 5: Basic Teradata Configuration[¶](#example-5-basic-teradata-configuration "Link to this heading")

Simple Teradata to Snowflake validation.

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: ./teradata_validation
target_database: SNOWFLAKE_DB
max_threads: auto

source_connection:
  mode: credentials
  host: teradata.company.com
  username: td_user
  password: TeradataPass123
  database: PROD_DB

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

tables:
  - fully_qualified_name: PROD_DB.sales_data
    use_column_selection_as_exclude_list: false
    column_selection_list: []
```

Copy

### Example 6: Teradata Large-Scale Migration[¶](#example-6-teradata-large-scale-migration "Link to this heading")

Enterprise-scale Teradata migration validation.

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: /opt/validation/teradata_migration
target_database: ENTERPRISE_DW
max_threads: 32

source_connection:
  mode: credentials
  host: teradata-prod.company.com
  username: validation_service
  password: SecureTdPassword!123
  database: ENTERPRISE_TD

target_connection:
  mode: name
  name: snowflake_enterprise

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 500
  exclude_metrics: false

comparison_configuration:
  tolerance: 0.005

logging_configuration:
  level: INFO
  console_level: ERROR
  file_level: DEBUG

schema_mappings:
  ENTERPRISE_TD: PUBLIC

tables:
  # Large fact table - high chunking
  - fully_qualified_name: ENTERPRISE_TD.fact_transactions
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - transaction_key
    chunk_number: 100
    max_failed_rows_number: 1000

  # Dimension table with exclusions
  - fully_qualified_name: ENTERPRISE_TD.dim_customer
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - tax_id
      - bank_account
    index_column_list:
      - customer_key
    chunk_number: 20

  # Filtered validation for current year only
  - fully_qualified_name: ENTERPRISE_TD.fact_sales
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - sale_key
    where_clause: "sale_date >= DATE '2024-01-01'"
    target_where_clause: "sale_date >= DATE '2024-01-01'"
    chunk_number: 50
```

Copy

### Example 7: Teradata Multi-Schema Validation[¶](#example-7-teradata-multi-schema-validation "Link to this heading")

Validate multiple schemas with different settings.

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: ./multi_schema_validation
target_database: MULTI_SCHEMA_DW
max_threads: 16

source_connection:
  mode: credentials
  host: teradata.company.com
  username: schema_validator
  password: ValidatorPass123
  database: DBC

target_connection:
  mode: name
  name: snowflake_multi_schema

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 200

comparison_configuration:
  tolerance: 0.01

schema_mappings:
  SALES_SCHEMA: SALES
  FINANCE_SCHEMA: FINANCE
  HR_SCHEMA: HUMAN_RESOURCES

tables:
  # Sales schema tables
  - fully_qualified_name: SALES_SCHEMA.orders
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id

  - fully_qualified_name: SALES_SCHEMA.order_details
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
      - line_number

  # Finance schema tables
  - fully_qualified_name: FINANCE_SCHEMA.invoices
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - invoice_id
    chunk_number: 30

  # HR schema tables - exclude sensitive data
  - fully_qualified_name: HR_SCHEMA.employees
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - ssn
      - salary
      - bank_account
      - emergency_contact
    index_column_list:
      - employee_id
```

Copy

---

## Redshift Examples[¶](#redshift-examples "Link to this heading")

### Example 8: Basic Redshift Configuration[¶](#example-8-basic-redshift-configuration "Link to this heading")

Simple Redshift to Snowflake validation.

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: ./redshift_validation
max_threads: auto

source_connection:
  mode: credentials
  host: redshift-cluster.us-east-1.redshift.amazonaws.com
  port: 5439
  username: redshift_user
  password: RedshiftPass123
  database: analytics

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false

tables:
  - fully_qualified_name: public.events
    use_column_selection_as_exclude_list: false
    column_selection_list: []
```

Copy

### Example 9: Redshift Data Lake Migration[¶](#example-9-redshift-data-lake-migration "Link to this heading")

Validate Redshift data lake migration to Snowflake.

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: /data/validation/redshift_datalake
max_threads: 24

source_connection:
  mode: credentials
  host: datalake-cluster.us-west-2.redshift.amazonaws.com
  port: 5439
  username: datalake_validator
  password: SecureRedshiftPass!123
  database: datalake

target_connection:
  mode: name
  name: snowflake_datalake

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 500

comparison_configuration:
  tolerance: 0.02

logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: DEBUG

database_mappings:
  datalake: DATALAKE_PROD

schema_mappings:
  public: PUBLIC
  staging: STAGING
  analytics: ANALYTICS

tables:
  # Raw data staging
  - fully_qualified_name: staging.raw_events
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - event_id
    chunk_number: 80
    max_failed_rows_number: 1000

  # Analytics tables
  - fully_qualified_name: analytics.user_sessions
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - session_id
    where_clause: "session_date >= CURRENT_DATE - 30"
    target_where_clause: "session_date >= CURRENT_DATE - 30"
    chunk_number: 40

  - fully_qualified_name: analytics.aggregated_metrics
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - metric_id
      - date_key
    chunk_number: 20

  # Public schema - exclude system columns
  - fully_qualified_name: public.customer_360
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - _sys_created_at
      - _sys_modified_at
      - _sys_user_id
    index_column_list:
      - customer_id
    chunk_number: 50
```

Copy

### Example 10: Redshift with Complex Filtering[¶](#example-10-redshift-with-complex-filtering "Link to this heading")

Advanced filtering and column selection for Redshift.

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: ./complex_validation
max_threads: 16

source_connection:
  mode: credentials
  host: analytics-cluster.region.redshift.amazonaws.com
  port: 5439
  username: validator
  password: ComplexPass123!
  database: analytics_db

target_connection:
  mode: name
  name: snowflake_analytics

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 100

comparison_configuration:
  tolerance: 0.01

tables:
  # Complex WHERE clause with multiple conditions
  - fully_qualified_name: public.transactions
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - transaction_id
      - customer_id
      - amount
      - transaction_date
      - status
      - payment_method
    index_column_list:
      - transaction_id
    where_clause: "status IN ('completed', 'settled') AND amount > 100 AND transaction_date >= '2024-01-01' AND payment_method != 'test'"
    target_where_clause: "status IN ('completed', 'settled') AND amount > 100 AND transaction_date >= '2024-01-01' AND payment_method != 'test'"
    chunk_number: 30

  # Date-based partitioned validation
  - fully_qualified_name: public.daily_metrics
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - metric_date
      - metric_id
    where_clause: "metric_date >= DATE_TRUNC('month', CURRENT_DATE)"
    target_where_clause: "metric_date >= DATE_TRUNC('month', CURRENT_DATE)"
    chunk_number: 10

  # Selective column validation with mappings
  - fully_qualified_name: public.legacy_customers
    use_column_selection_as_exclude_list: false
    column_selection_list:
      - cust_no
      - full_name
      - email_addr
      - phone_num
      - signup_dt
    index_column_list:
      - cust_no
    column_mappings:
      cust_no: customer_number
      full_name: customer_name
      email_addr: email
      phone_num: phone
      signup_dt: signup_date
```

Copy

---

## Scenario-Based Examples[¶](#scenario-based-examples "Link to this heading")

### Example 11: Development Environment - Fast Validation[¶](#example-11-development-environment-fast-validation "Link to this heading")

Quick validation for development with minimal overhead.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./dev_validation
max_threads: 4

source_connection:
  mode: credentials
  host: localhost
  port: 1433
  username: dev_user
  password: DevPass123
  database: DevDB
  trust_server_certificate: "yes"
  encrypt: "no"

target_connection:
  mode: default

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false  # Skip for speed

comparison_configuration:
  tolerance: 0.05  # More lenient

logging_configuration:
  level: WARNING  # Less verbose

tables:
  - fully_qualified_name: DevDB.dbo.TestTable1
    use_column_selection_as_exclude_list: false
    column_selection_list: []

  - fully_qualified_name: DevDB.dbo.TestTable2
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    where_clause: "id <= 1000"  # Limit rows for speed
    target_where_clause: "id <= 1000"
```

Copy

### Example 12: Staging Environment - Comprehensive Testing[¶](#example-12-staging-environment-comprehensive-testing "Link to this heading")

Thorough validation for staging environment.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: /staging/validation
max_threads: 12

source_connection:
  mode: credentials
  host: sqlserver-staging.company.com
  port: 1433
  username: staging_validator
  password: StagingPass123!
  database: STAGING_DB
  trust_server_certificate: "no"
  encrypt: "yes"

target_connection:
  mode: name
  name: snowflake_staging

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 200

comparison_configuration:
  tolerance: 0.01

logging_configuration:
  level: INFO
  console_level: INFO
  file_level: DEBUG

tables:
  - fully_qualified_name: STAGING_DB.dbo.Orders
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
    chunk_number: 15

  - fully_qualified_name: STAGING_DB.dbo.Customers
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - customer_id
    chunk_number: 10
```

Copy

### Example 13: Production - Maximum Performance[¶](#example-13-production-maximum-performance "Link to this heading")

Optimized for large-scale production validation.

```
source_platform: Teradata
target_platform: Snowflake
output_directory_path: /prod/validation
target_database: PROD_SNOWFLAKE
max_threads: 32  # Maximum parallelization

source_connection:
  mode: credentials
  host: teradata-prod.company.com
  username: prod_validator
  password: SecureProdPass!123
  database: PROD_TD

target_connection:
  mode: name
  name: snowflake_prod

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 1000
  exclude_metrics: false

comparison_configuration:
  tolerance: 0.001  # Strict tolerance

logging_configuration:
  level: INFO
  console_level: ERROR  # Minimal console output
  file_level: DEBUG  # Detailed file logging

tables:
  # Massive fact table - heavy chunking
  - fully_qualified_name: PROD_TD.fact_transactions
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - transaction_key
    chunk_number: 200  # Maximum chunking
    max_failed_rows_number: 5000

  # Other tables...
  - fully_qualified_name: PROD_TD.fact_sales
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - sale_key
    chunk_number: 150
```

Copy

### Example 14: PII-Compliant Validation[¶](#example-14-pii-compliant-validation "Link to this heading")

Exclude sensitive personally identifiable information.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: ./pii_compliant_validation
max_threads: auto

source_connection:
  mode: credentials
  host: sqlserver.company.com
  port: 1433
  username: compliance_validator
  password: CompliancePass123!
  database: CustomerDB

target_connection:
  mode: name
  name: snowflake_customer

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 100

comparison_configuration:
  tolerance: 0.01

tables:
  - fully_qualified_name: CustomerDB.dbo.Customers
    use_column_selection_as_exclude_list: true
    column_selection_list:
      # Exclude all PII columns
      - ssn
      - tax_id
      - date_of_birth
      - drivers_license
      - passport_number
      - credit_card_number
      - bank_account_number
      - email_address
      - phone_number
      - home_address
      - mailing_address
    index_column_list:
      - customer_id

  - fully_qualified_name: CustomerDB.dbo.Transactions
    use_column_selection_as_exclude_list: true
    column_selection_list:
      - credit_card_last4
      - account_number
      - routing_number
    index_column_list:
      - transaction_id
```

Copy

### Example 15: Migration Cutover Validation[¶](#example-15-migration-cutover-validation "Link to this heading")

Final validation before production cutover.

```
source_platform: Redshift
target_platform: Snowflake
output_directory_path: /cutover/validation
max_threads: 32

source_connection:
  mode: credentials
  host: redshift-prod.amazonaws.com
  port: 5439
  username: cutover_validator
  password: CutoverPass123!
  database: production

target_connection:
  mode: name
  name: snowflake_production_new

validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 0  # Zero tolerance for cutover

comparison_configuration:
  tolerance: 0.0001  # Extremely strict

logging_configuration:
  level: DEBUG  # Maximum detail
  console_level: INFO
  file_level: DEBUG

# Validate ALL tables
tables:
  - fully_qualified_name: public.customers
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - customer_id
    chunk_number: 50

  - fully_qualified_name: public.orders
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
    chunk_number: 100

  - fully_qualified_name: public.order_items
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
      - item_id
    chunk_number: 150

  - fully_qualified_name: public.products
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - product_id
    chunk_number: 20

  - fully_qualified_name: public.inventory
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - inventory_id
    chunk_number: 30
```

Copy

### Example 16: Continuous Validation - Daily Incremental[¶](#example-16-continuous-validation-daily-incremental "Link to this heading")

Daily validation of incremental loads.

```
source_platform: SqlServer
target_platform: Snowflake
output_directory_path: /daily/validation
max_threads: 16

source_connection:
  mode: credentials
  host: sqlserver.company.com
  port: 1433
  username: daily_validator
  password: DailyPass123!
  database: ETL_DB

target_connection:
  mode: name
  name: snowflake_daily

validation_configuration:
  schema_validation: false  # Skip schema check for daily runs
  metrics_validation: true
  row_validation: true
  max_failed_rows_number: 100

comparison_configuration:
  tolerance: 0.01

logging_configuration:
  level: INFO
  console_level: WARNING
  file_level: INFO

tables:
  # Validate only yesterday's data
  - fully_qualified_name: ETL_DB.dbo.DailyTransactions
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - transaction_id
    where_clause: "CAST(created_date AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)"
    target_where_clause: "CAST(created_date AS DATE) = CAST(DATEADD(day, -1, CURRENT_TIMESTAMP) AS DATE)"
    chunk_number: 10

  - fully_qualified_name: ETL_DB.dbo.DailyOrders
    use_column_selection_as_exclude_list: false
    column_selection_list: []
    index_column_list:
      - order_id
    where_clause: "CAST(order_date AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)"
    target_where_clause: "CAST(order_date AS DATE) = CAST(DATEADD(day, -1, CURRENT_TIMESTAMP) AS DATE)"
    chunk_number: 5
```

Copy

---

## Tips for Adapting These Examples[¶](#tips-for-adapting-these-examples "Link to this heading")

1. **Replace connection details** with your actual database credentials
2. **Update table names** to match your schema
3. **Adjust `max_threads`** based on your system resources
4. **Modify `chunk_number`** based on table sizes
5. **Set appropriate `tolerance`** based on your data characteristics
6. **Customize `where_clause`** for your filtering needs
7. **Add/remove columns** in `column_selection_list` as needed
8. **Update `column_mappings`** if column names differ

## Security Best Practices[¶](#security-best-practices "Link to this heading")

* **Never commit** configuration files with real passwords to version control
* Use **environment variables** for sensitive data
* Consider **secret management** tools (AWS Secrets Manager, Azure Key Vault, etc.)
* Use **least privilege** database accounts for validation
* **Encrypt** configuration files containing sensitive information

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

1. [Table of Contents](#table-of-contents)
2. [SQL Server Examples](#sql-server-examples)
3. [Teradata Examples](#teradata-examples)
4. [Redshift Examples](#redshift-examples)
5. [Scenario-Based Examples](#scenario-based-examples)
6. [Tips for Adapting These Examples](#tips-for-adapting-these-examples)
7. [Security Best Practices](#security-best-practices)