---
auto_generated: true
description: Welcome to the Snowflake Data Validation CLI documentation. The Snowflake
  Data Validation CLI (snowflake-data-validation or sdv) is a comprehensive command-line
  tool for validating data migrations bet
last_scraped: '2026-01-14T16:52:13.544664+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/index
title: Snowflake Data Validation - Documentation Index | Snowflake Documentation
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)Data Validation CLI

# Snowflake Data Validation - Documentation Index[¶](#snowflake-data-validation-documentation-index "Link to this heading")

Welcome to the Snowflake Data Validation CLI documentation. The Snowflake Data Validation CLI (`snowflake-data-validation` or `sdv`) is a comprehensive command-line tool for validating data migrations between source databases (SQL Server, Teradata, Amazon Redshift) and Snowflake. It provides multi-level validation strategies to ensure data consistency and quality.

## Documentation roadmap[¶](#documentation-roadmap "Link to this heading")

### 1. Command References by Database Dialect[¶](#command-references-by-database-dialect "Link to this heading")

**Choose your source database for dialect-specific commands:**

* **[SQL Server Commands Reference](sqlserver_commands)** - Complete SQL Server command documentation
* **[Teradata Commands Reference](teradata_commands)** - Complete Teradata command documentation
* **[Amazon Redshift Commands Reference](redshift_commands)** - Complete Redshift command documentation

Each command reference includes:

* Detailed syntax and options for all commands
* Connection configuration specifics
* Complete examples
* Troubleshooting tips
* Best practices for that platform

---

### 2. CLI Usage Guide - Comprehensive Reference[¶](#cli-usage-guide-comprehensive-reference "Link to this heading")

**[Start here for complete documentation.](CLI_USAGE_GUIDE)**

A comprehensive, customer-facing guide covering all aspects of the CLI tool.

**Contents:**

* Complete installation instructions
* Detailed command reference for all source databases
* In-depth configuration file reference with all options explained
* Complete configuration examples
* Advanced usage patterns
* Troubleshooting guide

**Best for:**

* First-time users getting started
* Users needing detailed explanations of configuration options
* Troubleshooting issues
* Understanding all available features

---

### 3. Quick Reference Guide - Fast Lookup[¶](#quick-reference-guide-fast-lookup "Link to this heading")

**[Use this for quick lookups and reminders.](CLI_QUICK_REFERENCE)**

A concise reference guide with essential information in an easy-to-scan format.

**Contents:**

* Command syntax at a glance
* Quick configuration templates
* Table configuration patterns
* Common CLI options reference
* Performance tips
* Common issues and quick fixes

**Best for:**

* Experienced users who need quick reminders
* Looking up specific syntax
* Quick configuration templates
* Performance optimization tips

---

### 4. Configuration Examples - Ready-to-Use configurations[¶](#configuration-examples-ready-to-use-configurations "Link to this heading")

**[Copy and adapt these real-world examples.](CONFIGURATION_EXAMPLES)**

A collection of ready-to-use configuration file examples for various scenarios.

**Contents:**

* 16+ complete configuration examples
* SQL Server configurations
* Teradata configurations
* Redshift configurations
* Scenario-based examples (dev, staging, production, PII-compliant, etc.)
* Tips for adapting examples
* Security best practices

**Best for:**

* Jump-starting your configuration
* Finding a configuration similar to your use case
* Learning by example
* Best practices for different scenarios

---

## Quick Navigation by Task[¶](#quick-navigation-by-task "Link to this heading")

### The following sections provide quick references to the documentation for specific tasks.[¶](#the-following-sections-provide-quick-references-to-the-documentation-for-specific-tasks "Link to this heading")

#### Get Started[¶](#get-started "Link to this heading")

1. Follow installation instructions in [CLI Usage Guide](CLI_USAGE_GUIDE.html#installation)
2. Copy an example from [Configuration Examples](CONFIGURATION_EXAMPLES)
3. Run your first validation using the [Quick Reference](CLI_QUICK_REFERENCE)

#### Understand All Options[¶](#understand-all-options "Link to this heading")

→ [CLI Usage Guide - Configuration File Reference](CLI_USAGE_GUIDE.html#configuration-file-reference)

#### Find a Command[¶](#find-a-command "Link to this heading")

→ [Quick Reference - Common Commands](CLI_QUICK_REFERENCE.html#common-commands)

#### Create a Configuration File[¶](#create-a-configuration-file "Link to this heading")

→ [Configuration Examples](CONFIGURATION_EXAMPLES) (pick the closest match to your scenario)

#### Troubleshoot an Issue[¶](#troubleshoot-an-issue "Link to this heading")

→ [CLI Usage Guide - Troubleshooting](CLI_USAGE_GUIDE.html#troubleshooting)

#### Optimize Performance[¶](#optimize-performance "Link to this heading")

→ [Quick Reference - Performance Tips](CLI_QUICK_REFERENCE.html#performance-tips)

#### Validate Large Tables[¶](#validate-large-tables "Link to this heading")

→ [CLI Usage Guide - Working with Large Tables](CLI_USAGE_GUIDE.html#working-with-large-tables)

#### Understand Connection Options[¶](#understand-connection-options "Link to this heading")

→ [CLI Usage Guide - Connection Configuration](CLI_USAGE_GUIDE.html#connection-configuration)

#### Set Up Validation Levels[¶](#set-up-validation-levels "Link to this heading")

→ [CLI Usage Guide - Validation Configuration](CLI_USAGE_GUIDE.html#validation-configuration)

#### Configure Table-Specific Settings[¶](#configure-table-specific-settings "Link to this heading")

→ [CLI Usage Guide - Table Configuration](CLI_USAGE_GUIDE.html#table-configuration)

---

## Documentation by Source Database[¶](#documentation-by-source-database "Link to this heading")

The following sections provide quick references to the documentation for specific source databases.

### SQL Server Users[¶](#sql-server-users "Link to this heading")

**Essential Reading:**

1. **[SQL Server Commands Reference](sqlserver_commands)** - Complete command reference
2. [Quick Reference - SQL Server Connection](CLI_QUICK_REFERENCE.html#sql-server)
3. [CLI Usage Guide - SQL Server Commands](CLI_USAGE_GUIDE.html#sql-server-commands)
4. [Configuration Examples - SQL Server Examples](CONFIGURATION_EXAMPLES.html#sql-server-examples)

**Key Examples:**

* [Example 1: Minimal SQL Server Configuration](CONFIGURATION_EXAMPLES.html#example-1-minimal-sql-server-configuration)
* [Example 2: Production SQL Server with SSL/TLS](CONFIGURATION_EXAMPLES.html#example-2-production-sql-server-with-ssl-tls)
* [Example 3: SQL Server Incremental Validation](CONFIGURATION_EXAMPLES.html#example-3-sql-server-incremental-validation)
* [Example 4: SQL Server with Column Mappings](CONFIGURATION_EXAMPLES.html#example-4-sql-server-with-column-mappings)

### Teradata Users[¶](#teradata-users "Link to this heading")

**Essential Reading:**

1. **[Teradata Commands Reference](teradata_commands)** - Complete command reference
2. [Quick Reference - Teradata Connection](CLI_QUICK_REFERENCE.html#teradata)
3. [CLI Usage Guide - Teradata Commands](CLI_USAGE_GUIDE.html#teradata-commands)
4. [Configuration Examples - Teradata Examples](CONFIGURATION_EXAMPLES.html#teradata-examples)

**Key Examples:**

* [Example 5: Basic Teradata Configuration](CONFIGURATION_EXAMPLES.html#example-5-basic-teradata-configuration)
* [Example 6: Teradata Large-Scale Migration](CONFIGURATION_EXAMPLES.html#example-6-teradata-large-scale-migration)
* [Example 7: Teradata Multi-Schema Validation](CONFIGURATION_EXAMPLES.html#example-7-teradata-multi-schema-validation)

### Amazon Redshift Users[¶](#amazon-redshift-users "Link to this heading")

**Essential Reading:**

1. **[Amazon Redshift Commands Reference](redshift_commands)** - Complete command reference
2. [Quick Reference - Redshift Connection](CLI_QUICK_REFERENCE.html#redshift)
3. [CLI Usage Guide - Redshift Commands](CLI_USAGE_GUIDE.html#amazon-redshift-commands)
4. [Configuration Examples - Redshift Examples](CONFIGURATION_EXAMPLES.html#redshift-examples)

**Key Examples:**

* [Example 8: Basic Redshift Configuration](CONFIGURATION_EXAMPLES.html#example-8-basic-redshift-configuration)
* [Example 9: Redshift Data Lake Migration](CONFIGURATION_EXAMPLES.html#example-9-redshift-data-lake-migration)
* [Example 10: Redshift with Complex Filtering](CONFIGURATION_EXAMPLES.html#example-10-redshift-with-complex-filtering)

---

## Documentation by Use Case[¶](#documentation-by-use-case "Link to this heading")

### Development Environment[¶](#development-environment "Link to this heading")

* [Configuration Example 11: Development Environment - Fast Validation](CONFIGURATION_EXAMPLES.html#example-11-development-environment-fast-validation)
* [Quick Reference - Common Commands](CLI_QUICK_REFERENCE.html#common-commands)

### Staging Environment[¶](#staging-environment "Link to this heading")

* [Configuration Example 12: Staging Environment - Comprehensive Testing](CONFIGURATION_EXAMPLES.html#example-12-staging-environment-comprehensive-testing)
* [CLI Usage Guide - Advanced Usage](CLI_USAGE_GUIDE.html#advanced-usage)

### Production Environment[¶](#production-environment "Link to this heading")

* [Configuration Example 13: Production - Maximum Performance](CONFIGURATION_EXAMPLES.html#example-13-production-maximum-performance)
* [CLI Usage Guide - Working with Large Tables](CLI_USAGE_GUIDE.html#working-with-large-tables)
* [Quick Reference - Performance Tips](CLI_QUICK_REFERENCE.html#performance-tips)

### PII/Compliance Requirements[¶](#pii-compliance-requirements "Link to this heading")

* [Configuration Example 14: PII-Compliant Validation](CONFIGURATION_EXAMPLES.html#example-14-pii-compliant-validation)
* [CLI Usage Guide - Table Configuration](CLI_USAGE_GUIDE.html#table-configuration)

### Migration Cutover[¶](#migration-cutover "Link to this heading")

* [Configuration Example 15: Migration Cutover Validation](CONFIGURATION_EXAMPLES.html#example-15-migration-cutover-validation)
* [CLI Usage Guide - Advanced Usage](CLI_USAGE_GUIDE.html#advanced-usage)

### Continuous/Incremental Validation[¶](#continuous-incremental-validation "Link to this heading")

* [Configuration Example 16: Continuous Validation - Daily Incremental](CONFIGURATION_EXAMPLES.html#example-16-continuous-validation-daily-incremental)
* [CLI Usage Guide - Advanced Usage](CLI_USAGE_GUIDE.html#advanced-usage)

---

## Configuration Reference[¶](#configuration-reference "Link to this heading")

The following sections provide quick references to the documentation for specific configuration scenarios.

### Quick Config Template[¶](#quick-config-template "Link to this heading")

→ [Quick Reference - Configuration Template](CLI_QUICK_REFERENCE.html#configuration-template)

### Complete Field Reference[¶](#complete-field-reference "Link to this heading")

→ [CLI Usage Guide - Configuration File Reference](CLI_USAGE_GUIDE.html#configuration-file-reference)

### Real-World Examples[¶](#real-world-examples "Link to this heading")

→ [Configuration Examples](CONFIGURATION_EXAMPLES)

---

## Common Workflows[¶](#common-workflows "Link to this heading")

The following sections provide quick references to the documentation for common workflows.

### First-Time Setup Workflow[¶](#first-time-setup-workflow "Link to this heading")

1. Install the CLI

   * → [CLI Usage Guide - Installation](CLI_USAGE_GUIDE.html#installation)
2. Generate configuration template

   * → [Quick Reference - Get Templates](CLI_QUICK_REFERENCE.html#get-configuration-files)
3. Copy and modify an example

   * → [Configuration Examples](CONFIGURATION_EXAMPLES)
4. Run validation

   * → [Quick Reference - Run Validation](CLI_QUICK_REFERENCE.html#run-validation)
5. Review results

   * → [CLI Usage Guide - Validation Reports](CLI_USAGE_GUIDE.html#validation-reports)

### Troubleshooting Workflow[¶](#troubleshooting-workflow "Link to this heading")

1. Check error message

   * → [CLI Usage Guide - Troubleshooting](CLI_USAGE_GUIDE.html#troubleshooting)
2. Review configuration

   * → [Quick Reference - Configuration Template](CLI_QUICK_REFERENCE.html#configuration-template)
3. Enable debug logging

   * → [CLI Usage Guide - Logging Configuration](CLI_USAGE_GUIDE.html#logging-configuration)
4. Review logs

   * → [CLI Usage Guide - Troubleshooting](CLI_USAGE_GUIDE.html#troubleshooting)
5. Adjust configuration

   * → [Configuration Examples](CONFIGURATION_EXAMPLES)

### Performance Optimization Workflow[¶](#performance-optimization-workflow "Link to this heading")

1. Review performance tips

   * → [Quick Reference - Performance Tips](CLI_QUICK_REFERENCE.html#performance-tips)
2. Enable chunking

   * → [CLI Usage Guide - Working with Large Tables](CLI_USAGE_GUIDE.html#working-with-large-tables)
3. Adjust thread count

   * → [CLI Usage Guide - Global Configuration](CLI_USAGE_GUIDE.html#global-configuration)
4. Add filters

   * → [CLI Usage Guide - Table Configuration](CLI_USAGE_GUIDE.html#table-configuration)
5. Test with examples

   * → [Configuration Examples - Production](CONFIGURATION_EXAMPLES.html#example-13-production-maximum-performance)

---

## Feature Matrix[¶](#feature-matrix "Link to this heading")

| Feature | Command Refs | Quick Reference | Usage Guide | Examples |
| --- | --- | --- | --- | --- |
| Installation |  | ✓ | ✓✓✓ |  |
| Command Syntax | ✓✓✓ | ✓✓✓ | ✓✓ |  |
| Configuration | ✓ | ✓✓ | ✓✓✓ | ✓✓✓ |
| Connection Setup | ✓✓✓ | ✓ | ✓✓✓ | ✓✓✓ |
| Table Config |  | ✓✓ | ✓✓✓ | ✓✓✓ |
| Validation Levels |  | ✓ | ✓✓✓ | ✓✓ |
| Performance |  | ✓✓✓ | ✓✓ | ✓✓ |
| Troubleshooting | ✓✓✓ | ✓✓ | ✓✓✓ |  |
| Examples | ✓✓ | ✓ | ✓✓ | ✓✓✓ |

Legend: ✓ = Covered, ✓✓ = Good Coverage, ✓✓✓ = Comprehensive Coverage

---

## Learning Path[¶](#learning-path "Link to this heading")

### Beginner Path[¶](#beginner-path "Link to this heading")

1. **Day 1: Understanding the Tool**

   * Read the [Main Project Repository](https://github.com/snowflakedb/migrations-data-validation)
   * Skim [CLI Usage Guide - Overview](CLI_USAGE_GUIDE.html#overview)
   * Review [Quick Reference](CLI_QUICK_REFERENCE)
2. **Day 2: First Validation**

   * Follow [CLI Usage Guide - Quick Start](CLI_USAGE_GUIDE.html#quick-start)
   * Copy [Configuration Example 1 or 5 or 8](CONFIGURATION_EXAMPLES)
   * Run your first validation
3. **Day 3: Configuration Mastery**

   * Read [CLI Usage Guide - Configuration Reference](CLI_USAGE_GUIDE.html#configuration-file-reference)
   * Review multiple [Configuration Examples](CONFIGURATION_EXAMPLES)
   * Customize configuration for your needs

### Intermediate Path[¶](#intermediate-path "Link to this heading")

1. **Optimize Performance**

   * [CLI Usage Guide - Working with Large Tables](CLI_USAGE_GUIDE.html#working-with-large-tables)
   * [Quick Reference - Performance Tips](CLI_QUICK_REFERENCE.html#performance-tips)
2. **Advanced Features**

   * [CLI Usage Guide - Advanced Usage](CLI_USAGE_GUIDE.html#advanced-usage)
   * [Configuration Examples - Scenario-Based](CONFIGURATION_EXAMPLES.html#scenario-based-examples)
3. **CI/CD Integration**

   * [CLI Usage Guide - CI/CD Integration](CLI_USAGE_GUIDE.html#ci-cd-integration)
   * [Configuration Examples - Continuous Validation](CONFIGURATION_EXAMPLES.html#example-16-continuous-validation-daily-incremental)

### Expert Path[¶](#expert-path "Link to this heading")

1. **Custom Templates**

   * [CLI Usage Guide - Using Custom Query Templates](CLI_USAGE_GUIDE.html#using-custom-query-templates)
2. **Async Workflows**

   * [CLI Usage Guide - Asynchronous Validation Workflow](CLI_USAGE_GUIDE.html#asynchronous-validation-workflow)
3. **Production Deployment**

   * [Configuration Example 13 & 15](CONFIGURATION_EXAMPLES)

---

## Search Tips[¶](#search-tips "Link to this heading")

### Finding Information Quickly[¶](#finding-information-quickly "Link to this heading")

**For Commands:**

* Look in [Quick Reference](CLI_QUICK_REFERENCE) first
* For details, see [CLI Usage Guide - CLI Commands](CLI_USAGE_GUIDE.html#cli-commands)

**For Configuration:**

* Start with [Quick Reference - Configuration Template](CLI_QUICK_REFERENCE.html#configuration-template)
* For full details, see [CLI Usage Guide - Configuration Reference](CLI_USAGE_GUIDE.html#configuration-file-reference)
* For examples, see [Configuration Examples](CONFIGURATION_EXAMPLES)

**For Errors:**

* Check [CLI Usage Guide - Troubleshooting](CLI_USAGE_GUIDE.html#troubleshooting)
* Review [Quick Reference - Common Issues](CLI_QUICK_REFERENCE.html#common-issues)

---

## Additional Support[¶](#additional-support "Link to this heading")

If you cannot find what you need in these documents:

Email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

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

1. [Documentation roadmap](#documentation-roadmap)
2. [Quick Navigation by Task](#quick-navigation-by-task)
3. [Documentation by Source Database](#documentation-by-source-database)
4. [Documentation by Use Case](#documentation-by-use-case)
5. [Configuration Reference](#configuration-reference)
6. [Common Workflows](#common-workflows)
7. [Feature Matrix](#feature-matrix)
8. [Learning Path](#learning-path)
9. [Search Tips](#search-tips)
10. [Additional Support](#additional-support)