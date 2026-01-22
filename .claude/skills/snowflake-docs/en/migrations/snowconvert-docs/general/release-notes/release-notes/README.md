---
auto_generated: true
description: SQL Server extraction process now adds ‘GO’ statements after USE database
  commands in object definition files to allow files to be executable.
last_scraped: '2026-01-14T16:51:18.860505+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README
title: SnowConvert AI - Recent Release Notes | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../about.md)
          + [Getting Started](../../getting-started/README.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](README.md)
          + User Guide

            + [SnowConvert AI](../../user-guide/snowconvert/README.md)
            + [Project Creation](../../user-guide/project-creation.md)
            + [Extraction](../../user-guide/extraction.md)
            + [Deployment](../../user-guide/deployment.md)
            + [Data Migration](../../user-guide/data-migration.md)
            + [Data Validation](../../user-guide/data-validation.md)
            + [Power BI Repointing](../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../technical-documentation/README.md)
          + [Contact Us](../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../translation-references/general/README.md)
          + [Teradata](../../../translation-references/teradata/README.md)
          + [Oracle](../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../translation-references/hive/README.md)
          + [Redshift](../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../translation-references/postgres/README.md)
          + [BigQuery](../../../translation-references/bigquery/README.md)
          + [Vertica](../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../translation-references/db2/README.md)
          + [SSIS](../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)GeneralRelease Notes

# SnowConvert AI - Recent Release Notes[¶](#snowconvert-ai-recent-release-notes "Link to this heading")

## Version 2.2.2 (Jan 13, 2026)[¶](#version-2-2-2-jan-13-2026 "Link to this heading")

### Improvements[¶](#improvements "Link to this heading")

#### General[¶](#general "Link to this heading")

* SQL Server extraction process now adds ‘GO’ statements after `USE database` commands in object definition files to allow files to be executable.
* Metadata extraction now intelligently focuses on extracting only supported object types for each specific platform.
* Improved conversion settings and disabled action buttons when a conversion status is pending (e.g., during AI verification).
* Added a ConnectionInfoBanner component to clearly display saved connection information.
* Refactored credential management by removing secret handling methods and simplifying connection processes.
* Introduced a database dropdown in data migration and validation screens and removed unnecessary required fields in connection configurations.
* Updated an internal dependency from ‘balto’ to ‘stellar’.
* Enhanced internal utilities for managing test results and progress.

## Version 2.2.1 (Jan 08, 2026)[¶](#version-2-2-1-jan-08-2026 "Link to this heading")

### New Feature[¶](#new-feature "Link to this heading")

#### General[¶](#id1 "Link to this heading")

* The Missing Object Report has been merged into Object References, streamlining reporting. This unifies both valid and missing object references in a single report.

### Improvements[¶](#id2 "Link to this heading")

#### General[¶](#id3 "Link to this heading")

* Implemented a mechanism to parse and modify `.toml` files for credentials for Snowflake and various source languages.

## Version 2.2.0 (Jan 07, 2026)[¶](#version-2-2-0-jan-07-2026 "Link to this heading")

### New Features[¶](#new-features "Link to this heading")

#### General[¶](#id4 "Link to this heading")

* Implemented initial code unit state management using JSON files.
* Added a new JobStorageService.
* Implemented AI verification server and interfaces.
* Added support for identity columns in table definition queries.
* Added required credentials configuration for the Data Migration Connection Page and updated the Data Validation Connection Page to include KeyPair as a supported authentication method.
* Migrated AI Verification to the new jobs infrastructure and services.
* Added models for the AI Verification job.
* Defined reader and writer components for TOML files.

### Improvements[¶](#id5 "Link to this heading")

#### General[¶](#id6 "Link to this heading")

* Updated the VersionInfoProvider to strip branch and commit hash from the version string.
* Added a missing singletons registry for dependency injection.
* Made the `reportFilePath` optional in `CodeUnitConversionProgress`.
* Moved the `SpcsManager` and its dependencies to the Databases project for better organization.
* Implemented an AI verification orchestrator.
* Refactored credential management methods to utilize `CreateOrEditCredentials`.
* Updated conversion status in other features when verified by a user.
* Removed AI Verification v1.
* Enhanced password input fields to prevent overflowing.
* Refactored AI Verification to use `CredentialsId` instead of `ConnectionString`.
* Improvements in the deploy command.
* Updated application version retrieval to use semantic versioning.

### Fixes[¶](#fixes "Link to this heading")

#### Teradata[¶](#teradata "Link to this heading")

* Fixed parenthesis issues that caused incorrect `PARTITION BY` generation for Iceberg table transformations in Teradata.

#### General[¶](#id7 "Link to this heading")

* Fixed SSO URL handling in Snowflake credentials configuration.
* Addressed minor issues related to AI verification.
* Fixed relative paths in AI verification job execution and application state management.

## Version 2.1.0 (Dec 18, 2025)[¶](#version-2-1-0-dec-18-2025 "Link to this heading")

### New Features[¶](#id8 "Link to this heading")

#### IBM DB2[¶](#ibm-db2 "Link to this heading")

* Implemented DECFLOAT transformation.

#### Oracle[¶](#oracle "Link to this heading")

* Added support for transforming `NUMBER` to `DECFLOAT` using the [Data Type Mappings](../../getting-started/running-snowconvert/conversion/oracle-conversion-settings.html#data-type-mappings) feature.
* Added a new report [TypeMappings.csv](../../getting-started/running-snowconvert/review-results/reports/type-mappings-report) that displays the data types that were changed using the Data Type Mappings feature.

#### PowerBI[¶](#powerbi "Link to this heading")

* Added support for the Transact connector pattern for queries and multiple properties in the property list for PowerBI.

#### Teradata[¶](#id9 "Link to this heading")

* Added a new conversion setting [Tables Translation](../../getting-started/running-snowconvert/conversion/teradata-conversion-settings.html#table-translation) which allows transforming all tables in the source code to a specific table type supported by Snowflake.
* Enabled conversion of tables to Snowflake-managed Iceberg tables.

#### SSIS[¶](#ssis "Link to this heading")

* Added support for full cache in SSIS lookup transformations.

#### General[¶](#id10 "Link to this heading")

* Added temporary credentials retrieval for AI Verification jobs.
* Added summary cards for selection and result pages.
* Implemented full support for the Git Service.
* Added ‘verified by user’ checkboxes and bulk actions to the selection and results pages.
* Added a dependency tag for AI Verification.
* Implemented the generation of a SqlObjects Report.

### Improvements[¶](#id11 "Link to this heading")

#### RedShift[¶](#redshift "Link to this heading")

* Optimized RedShift transformations to only add escape characters when necessary in `LIKE` conditions.

#### SSIS[¶](#id12 "Link to this heading")

* Improved Microsoft.DerivedColumn migrations for SSIS.

#### General[¶](#id13 "Link to this heading")

* Added the number of copied files to relevant outputs.
* Changed some buttons to the footer for improved UI consistency.

### Fixes[¶](#id14 "Link to this heading")

#### Teradata[¶](#id15 "Link to this heading")

* Fixed transformation of bash variables substitution in scripts.

## Version 2.0.86 (Dec 10, 2025)[¶](#version-2-0-86-dec-10-2025 "Link to this heading")

### Improvements[¶](#id16 "Link to this heading")

#### RedShift[¶](#id17 "Link to this heading")

* Added support for the `MURMUR3_32_HASH` function.
* Replaced Redshift epoch and interval patterns with Snowflake `TO_TIMESTAMP`.

#### SSIS[¶](#id18 "Link to this heading")

* Added support for converting Microsoft SendMailTask to Snowflake SYSTEM.
* Implemented SSIS event handler translation for `OnPreExecute` and `OnPostExecute`.

#### SQL Server[¶](#sql-server "Link to this heading")

* Enhanced transformation for the `Round` function with three arguments.

#### Informatica[¶](#informatica "Link to this heading")

* Updated `InfPcIntegrationTestBase` to import the real implementation of translators and other necessary components.

#### General[¶](#id19 "Link to this heading")

* Enhanced procedure name handling and improved identifier splitting logic.
* Improved object name normalization in DDL extracted code.
* Implemented a temporal variable to keep credentials in memory and retrieve the configuration file.
* Updated the TOML Credential Manager.
* Improved error suggestions.
* Added missing path validations related to ETL.
* Improved the application update mechanism.
* Implemented an exception to be thrown when calling the `ToToml` method for Snowflake credentials.
* Changed the log path and updated the cache path.
* Implemented a mechanism to check for updates.
* Merged the Missing Object References Report with ObjectReferences.
* Changed values in the name and description columns of the ETL.Issues report.
* Added support for Open Source and Converted models in AI Verification.
* Added a new custom JSON localizer
* Added a dialog to appear when accepting changes if multiple code units are present in the same file.
* Added a `FileSystemService`.
* Added an expression in the ETL issues report for `SSISExpressionCannotBeConverted`.

### Fixes[¶](#id20 "Link to this heading")

#### SQL Server[¶](#id21 "Link to this heading")

* Fixed a bug that caused the report database to be generated incorrectly.
* Fixed a bug that caused unknown Code Units to be duplicated during arrangement.

#### General[¶](#id22 "Link to this heading")

* Fixed an issue that prevented the cancellation of AI Verification jobs.
* Fixed an issue to support EAI in the AI specification file.
* Fixed an issue where the progress number was not being updated.
* Fixed the handling of application shutdowns during updates.

## Version 2.0.57 (Dec 03, 2025)[¶](#version-2-0-57-dec-03-2025 "Link to this heading")

### Improvements[¶](#id23 "Link to this heading")

#### SQL Server[¶](#id24 "Link to this heading")

* Enhanced SQL Server code extraction to return schema-qualified objects.

#### General[¶](#id25 "Link to this heading")

* Enhanced Project Service and Snowflake Authentication for improved execution.
* Removed GS validation from client-side, as it is now performed on the server side.
* Implemented connection validation to block deployment, data migration, and data validation when a connection is unavailable.
* Enhanced conversion to use the source dialect from project initialization.
* Improved `CodeUnitStatusMapper` to accurately handle progress status in UI status determination.
* Implemented batch insert functionality for enhanced object result processing.

### Fixes[¶](#id26 "Link to this heading")

#### General[¶](#id27 "Link to this heading")

* Resolved an issue where conversion settings were not being saved correctly.
* Corrected data validation select tree to properly skip folders.
* Fixed content centering issues in the UI.
* Normalized object names in AI Verification responses to prevent missing status entries in the catalog.

## Version 2.0.34 (Nov 27, 2025)[¶](#version-2-0-34-nov-27-2025 "Link to this heading")

### Improvements[¶](#id28 "Link to this heading")

#### General[¶](#id29 "Link to this heading")

* Resolved an issue where PowerBI was not correctly displayed in the list of supported languages.

## Version 2.0.30 (Nov 26, 2025)[¶](#version-2-0-30-nov-26-2025 "Link to this heading")

### New Features 🚀[¶](#id30 "Link to this heading")

#### IBM DB2[¶](#id31 "Link to this heading")

* Added transformation support for SELECT INTO and VALUES statement for variable assignments within User-Defined Functions (UDFs).

#### Oracle[¶](#id32 "Link to this heading")

* Added transformation support for SELECT INTO for variables assignments within User-Defined Functions (UDFs).

#### SQL Server[¶](#id33 "Link to this heading")

* Added transformation support for SELECT INTO for variables assignments within User-Defined Functions (UDFs).

#### SSIS[¶](#id34 "Link to this heading")

* Added support for SSIS Event Handlers.

#### General[¶](#id35 "Link to this heading")

* Introduced AI Verification Contract Model Codes.
* Created a base component for the Code Processing View.
* Implemented YAML reading and writing services with an enhanced `info` command.
* Created an execution type selector page.

### Improvements[¶](#id36 "Link to this heading")

#### General[¶](#id37 "Link to this heading")

* Updated GS Version to 9.50.99 to ensure compatibility with newer versions of GS.
* Expanded job storage test coverage across data validation, migration, deployment, extraction, metadata, and AI verification.
* Refactored the FilteredObjectExplorer layout and removed unnecessary container styles from the AI Verification Selection Page and Mappings Page to improve UI consistency.
* Enhanced deployment database selection.

### Fixes[¶](#id38 "Link to this heading")

#### SQL Server[¶](#id39 "Link to this heading")

* Resolved an error that occurred when parsing SQL Server connections with a specific port.

#### General[¶](#id40 "Link to this heading")

* Resolved an issue where mappings were not functioning correctly in code conversion.
* Corrected the process for cleaning the conversion directory before conversion.
* Fixed deployment dropdown functionality.

## Version 2.0.8 (Nov 21, 2025)[¶](#version-2-0-8-nov-21-2025 "Link to this heading")

### Improvements[¶](#id41 "Link to this heading")

#### Teradata[¶](#id42 "Link to this heading")

* Added support for `GOTO-LABELS` in SnowScript.

#### Spark SQL[¶](#spark-sql "Link to this heading")

* Added support for transformation rules to handle `INSERT OVERWRITE` statements.

#### SQL Server[¶](#id43 "Link to this heading")

* Added support for the `CREATE SEQUENCE` statement.

#### General[¶](#id44 "Link to this heading")

* Added support for IBM Db2 from the UI.
* Fixed Db2 support in SourceDialect and Update Conversion settings window.
* Added support for tables with large numbers of rows (> 2.5B) in data migrator.

## Version 2.0.0 (Nov 20, 2025)[¶](#version-2-0-0-nov-20-2025 "Link to this heading")

The SnowConvert AI interface is revised to improve efficiency, control, and usability.
In the improved interface, you can run specific flows independently, including extraction, deployment, and
data validation. There is now a dedicated project page to show you which flows you can run. The improved
interface gives you more granular control over your project and makes managing complex workflows easier.

For more information, [SnowConvert AI: Project Creation](../../user-guide/project-creation)

## Version 1.21.0 (Nov 08, 2025)[¶](#version-1-21-0-nov-08-2025 "Link to this heading")

### Improvements[¶](#id45 "Link to this heading")

#### SQL Server[¶](#id46 "Link to this heading")

* Added support for the CREATE SEQUENCE statement.

#### General[¶](#id47 "Link to this heading")

* Added a notification to inform users about the SnowConvertAI 2.0 New UI experience.

## Version 1.20.11 (Nov 07, 2025)[¶](#version-1-20-11-nov-07-2025 "Link to this heading")

### Improvements[¶](#id48 "Link to this heading")

#### RedShift[¶](#id49 "Link to this heading")

* Added support for the `CURRENT_SETTING` timezone.

#### Spark SQL[¶](#id50 "Link to this heading")

* Added support for `INSERT BY NAME` and removed the `TABLE` keyword and partition clause.

#### PowerBI[¶](#id51 "Link to this heading")

* Supported dynamic parameterization in connectors with embedded queries in WHERE clauses.

## Version 1.20.10 (Nov 06, 2025)[¶](#version-1-20-10-nov-06-2025 "Link to this heading")

### Improvements and Fixes[¶](#improvements-and-fixes "Link to this heading")

#### RedShift[¶](#id52 "Link to this heading")

* Added support for HLL functions.
* Added support for JSON functions.
* Added support for OBJECT\_TRANSFORM.

#### SSIS[¶](#id53 "Link to this heading")

* Added conversion support for SSIS Microsoft.ExpressionTask.
* Modified the condition used to determine if an SSIS package is reusable.

#### Teradata[¶](#id54 "Link to this heading")

* Added support for named arguments in the EXECUTE (Macro Form) statement.
* Fixed an issue where scripts were not being migrated to Snowscript.
* The Continue Handler is now available for Scripts.

#### PostgreSQL[¶](#postgresql "Link to this heading")

* Fixed an issue where procedures did not have the EXECUTE AS CALLER clause generated by default when the SECURITY clause was absent in the input.

#### RedShift[¶](#id55 "Link to this heading")

* Fixed an issue where non-ASCII characters in columns were not quoted during data migration.

#### SQL Server[¶](#id56 "Link to this heading")

* Fixed an issue where default GETDATE column constraints applied an unnecessary double cast in the column definition.

## Version 1.20.8 (Nov 05, 2025)[¶](#version-1-20-8-nov-05-2025 "Link to this heading")

### Improvements[¶](#id57 "Link to this heading")

#### General[¶](#id58 "Link to this heading")

* Added support for alert preview notifications.
* Improved Claude model validation to inform users about required access.

## Version 1.20.7 (Oct 31, 2025)[¶](#version-1-20-7-oct-31-2025 "Link to this heading")

### IBM DB2 Stored Procedures & User-Defined Functions Support[¶](#ibm-db2-stored-procedures-user-defined-functions-support "Link to this heading")

SnowConvert AI now supports the conversion of DB2 stored procedures to Snowflake equivalents, enabling seamless migration of procedural code. This feature includes support for variable operations, and control flow statements. Also, DB2 user-defined functions will be converted to Snowflake Scripting UDFs when possible.

### New Features 🚀[¶](#id59 "Link to this heading")

#### SSIS[¶](#id60 "Link to this heading")

* Implemented SSIS to Snowflake string literal escape sequence conversion.

### Improvements[¶](#id61 "Link to this heading")

#### Teradata[¶](#id62 "Link to this heading")

* Updated scripts transformation to utilize a `continue` handler.

#### General[¶](#id63 "Link to this heading")

* Cleaned up `package.json` for customer distribution.

### Fixes[¶](#id64 "Link to this heading")

#### BigQuery[¶](#bigquery "Link to this heading")

* Fixed an aggregation issue that occurred when column aliases had the same name as table columns.

#### Oracle[¶](#id65 "Link to this heading")

* Fixed `NOT NULL` constraint behavior with `INLINE`, `CHECK`, and `PK` constraints.

#### SSIS[¶](#id66 "Link to this heading")

* Fixed an issue where comment tags were not displayed in converted reusable packages.

#### General[¶](#id67 "Link to this heading")

* Updated database dependencies and resolved dependencies vulnerabilities.

## Version 1.20.6 (Oct 29, 2025)[¶](#version-1-20-6-oct-29-2025 "Link to this heading")

### New Features 🚀[¶](#id68 "Link to this heading")

#### SSIS[¶](#id69 "Link to this heading")

* **SSIS Replatform migration (Public Preview)** - SnowConvert AI now supports SSIS package migration to Snowflake in Public Preview, enabling automated conversion of SSIS workflows to modern cloud-native data pipelines.

#### BigQuery[¶](#id70 "Link to this heading")

* Added support for the `JSON_TYPE` built-in function.
* Added support for the `SAFE.POW` function.
* Added transformation for array slice patterns.
* Added more array pattern support.

#### IBM DB2[¶](#id71 "Link to this heading")

* Added support for `CONTINUE HANDLER`.

#### Oracle[¶](#id72 "Link to this heading")

* Added support for the `PARTITION` clause in `MERGE` statements.

#### RedShift[¶](#id73 "Link to this heading")

* Added support for `CONTINUE HANDLER`.

#### Teradata[¶](#id74 "Link to this heading")

* Added support for `CONTINUE HANDLER`.

#### PowerBI[¶](#id75 "Link to this heading")

* Added the `HierarchicalNavigation` flag as an optional parameter in native connectors.

### Improvements[¶](#id76 "Link to this heading")

#### Oracle[¶](#id77 "Link to this heading")

* Enhanced arithmetic operations with `TIMESTAMP` values.

#### SSIS[¶](#id78 "Link to this heading")

* Enhanced the UI for the SSIS Replatform Public Preview release with improved user experience and workflow optimization.

#### General[¶](#id79 "Link to this heading")

* Removed the SSC-EWI-0009 warning from non-literal expressions and added FDM instead.
* AiVerification - Added support for `n_tests` parameter in configuration file.

### Fixes[¶](#id80 "Link to this heading")

#### BigQuery[¶](#id81 "Link to this heading")

* Fixed an issue where UDF files were not generated.

#### General[¶](#id82 "Link to this heading")

* Fixed an issue where symbols were not loaded in views and set operations.

## Version 1.20.3 (Oct 20, 2025)[¶](#version-1-20-3-oct-20-2025 "Link to this heading")

### Fixes[¶](#id83 "Link to this heading")

#### General[¶](#id84 "Link to this heading")

* Fixed incorrect verified objects count calculation during validation process.
* Updated warehouse validation error messages to maintain consistency with connector messaging.

## Version 1.20.2 (Oct 20, 2025)[¶](#version-1-20-2-oct-20-2025 "Link to this heading")

### New Features 🚀[¶](#id85 "Link to this heading")

#### BigQuery[¶](#id86 "Link to this heading")

* Added support for `REGEXP_EXTRACT_ALL` and `ROW_NUMBER` built-in functions.
* Added support for the `ARRAY` built-in function.

### Improvements[¶](#id87 "Link to this heading")

#### SQL Server[¶](#id88 "Link to this heading")

* Migrated `XACT_STATE` to `CURRENT_TRANSACTION`.
* Enabled `ROLLBACK` transformation within explicit transactions.

#### PowerBI[¶](#id89 "Link to this heading")

* Improved the ‘Pending Work Description’ on repointing reports.

### Fixes[¶](#id90 "Link to this heading")

#### BigQuery[¶](#id91 "Link to this heading")

* Fixed an issue where literals inside `IN UNNEST` were not being transformed.
* Fixed `SAFE_CAST` behavior when the input type is not `VARCHAR`.

#### General[¶](#id92 "Link to this heading")

* Fixed queries containing aggregate functions and multiple columns.

## Version 1.20.1 (Oct 16, 2025)[¶](#version-1-20-1-oct-16-2025 "Link to this heading")

### New Features 🚀[¶](#id93 "Link to this heading")

#### BigQuery[¶](#id94 "Link to this heading")

* Added support for the `REGEXP_REPLACE` function.
* Added support for the `FORMAT` function with the `%t` argument.
* Added support for the `BYTE_LENGTH` function.
* Added support for the `TIMESTAMP_TRUNC` function.

### Improvements[¶](#id95 "Link to this heading")

#### Teradata[¶](#id96 "Link to this heading")

* Improved the preservation of default values in `SELECT INTO` statements for empty results.

#### PowerBI[¶](#id97 "Link to this heading")

* Improved M-Query source retrieving from metadata files.

### Fixes[¶](#id98 "Link to this heading")

#### PowerBI[¶](#id99 "Link to this heading")

* Fixed an issue where the parameter list was not read correctly when the connection pattern was rejected.
* Added description in ETLAndBiRepointing assessment report when non-database or non-applicable connectors are unmodified.

## Version 1.20.0 (Oct 15, 2025)[¶](#version-1-20-0-oct-15-2025 "Link to this heading")

### New Features 🚀[¶](#id100 "Link to this heading")

#### BigQuery[¶](#id101 "Link to this heading")

* Added support for `TimestampDiff`, `Safe_Divide`, and `Except` functions.
* Added support for the `ARRAY_AGG` function.
* Added the `UNNEST` built-in symbol.
* Added support for the `UNIX_SECONDS` built-in function.
* Added support for `UNIX_MILLIS` and `UNIX_MICROS` built-in functions.
* Added support for `ARRAY_CONCAT`, `TIMESTAMP_MILLIS`, and `ENDS_WITH` functions.
* Added support for `JSON_QUERY`, `JSON_EXTRACT`, `JSON_QUERY_ARRAY`, and `JSON_EXTRACT_ARRAY` functions.

#### Teradata[¶](#id102 "Link to this heading")

* Added support for `.REMARK` in SnowScript.

#### SSIS[¶](#id103 "Link to this heading")

* Implemented SSIS ForEach File Enumerator translation logic.

#### Tableau[¶](#tableau "Link to this heading")

* Added repointing assessment for Tableau repointing.

#### General[¶](#id104 "Link to this heading")

* Added support for the MD5 function.

### Improvements[¶](#id105 "Link to this heading")

#### Teradata[¶](#id106 "Link to this heading")

* Commented out ERROR LEVEL in BTEQ.

#### SSIS[¶](#id107 "Link to this heading")

* Enhanced identifier sanitization for SSIS.
* Improved retrieval of the “CopyFromReferenceColumn” property for output columns in SSIS Lookup.

#### General[¶](#id108 "Link to this heading")

* Added account information to AiVerification logs.
* Added warehouse validation to the Snowflake login.
* Wrapped control variable values with `TO_VARIANT` in `UpdateControlVariable` calls.
* Refactored SQL task creation to use `CREATE OR REPLACE` syntax.
* Added `INSERT...SELECT` with `TO_VARIANT` for control variables.
* Added transformation for string case-insensitive comparisons.

### Fixes[¶](#id109 "Link to this heading")

#### General[¶](#id110 "Link to this heading")

* Fixed name collisions of tasks in the main control flow with container tasks.
* Fixed “No expression translation for negative numbers (or unary ‘minus’)” issues.

## Version 1.19.7 (Oct 10, 2025)[¶](#version-1-19-7-oct-10-2025 "Link to this heading")

### New Features 🚀[¶](#id111 "Link to this heading")

#### BigQuery[¶](#id112 "Link to this heading")

* Support was added for the `TO_HEX` and `ARRAY_TO_STRING_FUNCTION`.

#### Oracle[¶](#id113 "Link to this heading")

* SnowScript UDF is now generally available.

#### SQL Server[¶](#id114 "Link to this heading")

* SnowScript UDF is now generally available.

#### General[¶](#id115 "Link to this heading")

* A feature flag was added to hide additional options for the AiVerification API.
* An interface was added to Abstract Syntax Trees (ASTs) for representing string comparisons.
* Partial support was added for the `ARRAY_CONCAT_AGG` function.
* Support was added for the `REGEXP_EXTRACT` function.
* Transformation support was added for the `UNNEST` function within an `IN` predicate.
* Support was added for the `NET.IPV4_TO_INT64` function.

### Improvements[¶](#id116 "Link to this heading")

* The maximum GS version was bumped to 9.37 to extend the period of SC usage until the end of October.
* The `TSqlNotSupportedStatementReplacer` rule is now bypassed when processing ETL SQL fragments.
* Predecessor name generation now uses the SSIS package file name.

### Fixes[¶](#id117 "Link to this heading")

* The verified objects count issue was resolved.

## Version 1.19.6 (Oct 08, 2025)[¶](#version-1-19-6-oct-08-2025 "Link to this heading")

### New Features 🚀[¶](#id118 "Link to this heading")

#### SSIS[¶](#id119 "Link to this heading")

* Added core foundation for ForEach File Enumerator.
* Added base infrastructure for Dynamic SQL.
* Added cursor-based iteration structure for SSIS ForEach Loop containers.
* Added dynamic SQL support for SSIS Execute SQL Task.

#### Oracle[¶](#id120 "Link to this heading")

* Added support for the BigQuery UNNEST operator.
* Added support for JSON\_VALUE\_ARRAY built-in function.
* Added support for multiple built-in functions.
* Added support for TIMESTAMP\_SECONDS.
* Added support for SnowScript UDF.

#### SQL Server[¶](#id121 "Link to this heading")

* Added TSqlSetIdentityInsertReplacer to handle SET IDENTITY\_INSERT in Transact.

#### General[¶](#id122 "Link to this heading")

* Added AI Verification PuPr Followup items.
* Added ‘connection’ element in Tableau repointing.
* Added semicolons to execute SQL task statements inside containers.
* Added transformation for NET.SAFE\_IP\_FROM\_STRING function.
* Added support for HLL\_COUNT.MERGE function.
* Added support for NET.IP\_NET\_MASK function.
* Added ETL Preprocess Task.
* Added transformation for HLL\_COUNT.INIT function.
* Added support for offset array accessor function.

### Improvements[¶](#id123 "Link to this heading")

* Added serialization and deserialization of query symbols in the migration context.

### Fixes[¶](#id124 "Link to this heading")

#### Teradata[¶](#id125 "Link to this heading")

* Fixed issues related to CAST formats.

#### Oracle[¶](#id126 "Link to this heading")

* Fixed an issue where supported formats were incorrectly marked as unsupported.
* Fixed a bug related to symbol key creation.

#### General[¶](#id127 "Link to this heading")

* Fixed an issue with symbol key creation when loading symbols with context.
* Fixed an issue with quotes and value length in Tableau repointing.

## Version 1.19.5 (Oct 03, 2025)[¶](#version-1-19-5-oct-03-2025 "Link to this heading")

### New Features 🚀[¶](#id128 "Link to this heading")

#### General[¶](#id129 "Link to this heading")

* Added support for Snowflake select asterisk column expressions.

#### SSIS[¶](#id130 "Link to this heading")

* Added support for converting CAST expressions.

### Improvements[¶](#id131 "Link to this heading")

#### General[¶](#id132 "Link to this heading")

* Enhanced the SnowflakeLogin method to handle email users correctly.
* Moved the Declare Statement Replacer to SQL.

### Fixes[¶](#id133 "Link to this heading")

#### SSIS[¶](#id134 "Link to this heading")

* Fixed an issue where SSIS containers BEGIN END without a semicolon.

#### Oracle[¶](#id135 "Link to this heading")

* Fixed an issue with incorrect function transformation.
* Fixed an issue where SYS\_REFCURSOR was not being migrated correctly.

#### dbt[¶](#dbt "Link to this heading")

* Fixed an issue with conditional split downstream ref() calls.

## Version 1.19.4 (Oct 1, 2025)[¶](#version-1-19-4-oct-1-2025 "Link to this heading")

### New Features 🚀[¶](#id136 "Link to this heading")

#### PowerBI[¶](#id137 "Link to this heading")

* Expanded test scenarios for Teradata Power BI repointing.

#### SSIS[¶](#id138 "Link to this heading")

* Introduced support for the SSIS Merge Join transformation.
* Implemented orchestrator task variable wrappers for SSIS tasks.

#### Teradata[¶](#id139 "Link to this heading")

* Ensured script files are now correctly reported as code units when Snowscript is the target.

#### Oracle[¶](#id140 "Link to this heading")

* Implemented a warning system for users when a referenced datatype might be unsupported.
* Renamed `RAISE_MESSAGE_UDF.sql` to `RAISE_MESSAGE.sql` for clarity and consistency.

#### SQL Server[¶](#id141 "Link to this heading")

* Added parameters as an identifier for improved recognition.

#### dbt[¶](#id142 "Link to this heading")

* Relocated configuration files to the ETL output directory and removed analyses and snapshots folders from dbt projects.

#### General[¶](#id143 "Link to this heading")

* Added transformations for BTEQ labels to support nested procedures.
* Enabled result binding for the Execute SQL Task.
* Included Migration ID in object tagging and relevant reports for enhanced telemetry.
* Reduced the frequency of the AI Verification prompt.

### Improvements[¶](#id144 "Link to this heading")

#### Oracle[¶](#id145 "Link to this heading")

* Enhanced the conversion process for `%TYPE` declarations.
* Refactored DB2 variable declarations for improved consistency.

#### General[¶](#id146 "Link to this heading")

* Improved collision detection and resolution mechanisms for ETL transformations.

### Fixes[¶](#id147 "Link to this heading")

#### Oracle[¶](#id148 "Link to this heading")

* Resolved an issue where `RAISE_MESSAGE_UDF.sql` was incorrectly referenced in PostgreSQL tests.
* Addressed a problem where EWI (Error Warning Information) was not being added to unresolved types in Oracle.

#### General[¶](#id149 "Link to this heading")

* Improved error handling and logging within the `AiVerificationHttpClient`.

## Version 1.19.3 (Sep 29, 2025)[¶](#version-1-19-3-sep-29-2025 "Link to this heading")

### Improvements[¶](#id150 "Link to this heading")

#### General[¶](#id151 "Link to this heading")

* Enhanced VerifiedTemplate to better manage child verification states.

### Fixes[¶](#id152 "Link to this heading")

#### General[¶](#id153 "Link to this heading")

* Fixed an issue where the role was not being propagated correctly to the login endpoint.
* Fixed an issue where ZIP files created in Windows did not preserve proper Unix permissions.

## Version 1.19.2 (Sep 26, 2025)[¶](#version-1-19-2-sep-26-2025 "Link to this heading")

### New Features 🚀[¶](#id154 "Link to this heading")

#### PowerBI[¶](#id155 "Link to this heading")

* Added support for dynamic or custom concatenation for greater flexibility in data transformations.

#### SSIS[¶](#id156 "Link to this heading")

* Implemented the core infrastructure for recursive conversion of SSIS containers (e.g., `For Loop`, `Foreach Loop`), enabling the processing of more complex structures.

### Improvements[¶](#id157 "Link to this heading")

#### SSIS[¶](#id158 "Link to this heading")

* Completed the implementation of inlined conversion for containers to better handle control flows.

#### Teradata[¶](#id159 "Link to this heading")

* Reordered UDFs and updated the default time format (`HH:MI:SS.FF6`) to improve conversion compatibility.

#### dbt[¶](#id160 "Link to this heading")

* Removed angled brackets (`<>`) from generated YML configuration files to prevent potential syntax errors.
* Removed unnecessary tags from models generated during ETL conversions to produce cleaner code.
* Simplified the names of generated models in ETL conversions to enhance project readability.

### Fixes[¶](#id161 "Link to this heading")

#### PostgreSQL[¶](#id162 "Link to this heading")

* Resolved an error in the `RAISE_MESSAGE_UDF` when it was called with only two parameters.

#### General[¶](#id163 "Link to this heading")

* Updated SQLite storage filename to include file extension for better file management.
* Corrected an issue in the `TRANSFORM_SP_EXECUTE_SQL_STRING_UDF` helper where `datetime` values were formatted incorrectly in dynamic SQL.
* Applied internal fixes related to Nuget package management.
* Corrected an incorrect enumeration in an internal resource file (`IssueResources.json`).

## Version 1.19.0 (Sep 24, 2025)[¶](#version-1-19-0-sep-24-2025 "Link to this heading")

### New Features 🚀[¶](#id164 "Link to this heading")

#### General[¶](#id165 "Link to this heading")

* Added support for IDENTITY in CTAS statements.
* Enhanced telemetry settings in data migration configuration for improved metrics collection control.

#### Tableau[¶](#id166 "Link to this heading")

* Added initial infrastructure for converting Tableau projects.

#### ETL & SSIS[¶](#etl-ssis "Link to this heading")

* Implemented new output structure for ETL conversions, grouped by filename.
* Added support for ISNULL function conversion and variables in “Derived Column” expressions.
* Enhanced SSIS assessment report and task generation using original package names.

#### DB2[¶](#db2 "Link to this heading")

* Added support for DECLARE TABLE statement transformation.

#### BigQuery[¶](#id167 "Link to this heading")

* Added support for REGEXP\_CONTAINS function.

#### dbt[¶](#id168 "Link to this heading")

* Refactored dbt project generator to unify variable conversion logic.

### Fixes[¶](#id169 "Link to this heading")

#### PowerBI[¶](#id170 "Link to this heading")

* Fixed CommandTimeout parameter and schema uppercase conversion issues.

#### SSIS[¶](#id171 "Link to this heading")

* Fixed critical bug with plus operator (+) on numeric operands.

#### General[¶](#id172 "Link to this heading")

* Corrected conversion rate calculation.
* Enhanced DROP TABLE handling and COALESCE type resolution.
* Removed conversion of On Commit Preserve Rows node for Teradata.

## Version 1.18.3 (Sep 22, 2025)[¶](#version-1-18-3-sep-22-2025 "Link to this heading")

### Fixes[¶](#id173 "Link to this heading")

* Improved the refresh deployment catalog functionality in the end-to-end experience.
* Fixed navigation issues with the Retry Conversion flow.

## Version 1.18.0 (Sep 18, 2025)[¶](#version-1-18-0-sep-18-2025 "Link to this heading")

### New Features 🚀[¶](#id174 "Link to this heading")

#### PuPr AI Verification[¶](#pupr-ai-verification "Link to this heading")

* Added new [AI Verification](../../../snowconvert-ai-verification) step for SQL Server migrations.

#### SQL Server[¶](#id175 "Link to this heading")

* [Preview Feature] Support for UDF translation to [Snowflake Scripting UDFs](../../../../../developer-guide/udf/sql/udf-sql-procedural-functions)
* Support for `ERROR_NUMBER` to `SQLCODE`.
* Support for `COL_LENGTH` built-in function.

#### Teradata[¶](#id176 "Link to this heading")

* Support for the `TD_MONTH_BEGIN`, `TD_WEEK_BEGIN`, and `TD_WEEK_END` built-in functions.
* Support for hex literals in the `OREPLACE` built-in function.

#### Oracle[¶](#id177 "Link to this heading")

* Support `ASCIISTR` built-in function.
* Support for `MAX DENSE_RANK FIRST` and `MIN DENSE_RANK LAST` clauses.

#### SSIS[¶](#id178 "Link to this heading")

* Added SSIS Microsoft.Merge transformation
* Enhanced SSIS variable handling transformation

### Fixes[¶](#id179 "Link to this heading")

#### Oracle[¶](#id180 "Link to this heading")

* Improved recognition of correlated queries.

## Version 1.17.6 (Sep 5, 2025)[¶](#version-1-17-6-sep-5-2025 "Link to this heading")

### Fixes[¶](#id181 "Link to this heading")

* Fixed crashes in code conversion on SnowConvert classic mode.

## Version 1.17.2 (Sep 4, 2025)[¶](#version-1-17-2-sep-4-2025 "Link to this heading")

### Fixes[¶](#id182 "Link to this heading")

* Fixed visual issues in the object selection screen.

## Version 1.17.1 (Sep 1, 2025)[¶](#version-1-17-1-sep-1-2025 "Link to this heading")

### New Features 🚀[¶](#id183 "Link to this heading")

#### General[¶](#id184 "Link to this heading")

* [IBM DB2 SQL Support](../../getting-started/running-snowconvert/supported-languages/ibm-db2)  
  SnowConvert AI now supports the conversion of Tables and Views to Snowflake. This feature includes support for the following:

  + Translation of [Tables](../../../translation-references/db2/db2-create-table).
  + Translation of Views.
  + Translation of [Data Types](../../../translation-references/db2/db2-data-types).
  + Translation of Built-in Functions.
* Added new columns to [Top Level Code Unit report](../../getting-started/running-snowconvert/review-results/reports/top-level-code-units-report): Code Unit Database, Code Unit Schema and Code Unit Name

#### PostgreSQL & Based Languages[¶](#postgresql-based-languages "Link to this heading")

* Support for Bitwise Functions

### Fixes[¶](#id185 "Link to this heading")

#### General[¶](#id186 "Link to this heading")

* Modified [SSC-EWI-0040](../../technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040) to specify the error node.

#### Teradata[¶](#id187 "Link to this heading")

* Removed .SET FORMAT from BTEQ transformation
* Fixed several BTEQ parsing errors
* Added support for BTEQ `.MESSAGEOUT` command
* Added pending transformation for shell variables inside conditions
* Added support for BTEQ `.SET FOLDLINE` command
* Added transformation for `.SET TITLEDASHES` command
* Downgraded EWI to FDM for `STATISTICS` BTEQ clause
* Downgraded EWI to FDM for `PERIOD` BTEQ clause

#### Oracle[¶](#id188 "Link to this heading")

* Fix transformation for DATE type attribute

#### SQL Server[¶](#id189 "Link to this heading")

* Improved the handling of procedures containing `SELECT INTO` statements that return a query.
* Transform `@@DateFirst` to `GET_WEEK_START`
* `Numeric format` function support
* `Convert` function support
* `Datename` function support
* Removed the symbol `@` in the conversion that uses XML queries.
* `Print` statement support
* Formats for datetime support.
* Improved the update statement by removing the table name from the clause when it appears in the target table.
* Error functions translation support.

## Version 1.16.2 (Aug 19, 2025)[¶](#version-1-16-2-aug-19-2025 "Link to this heading")

### New Features 🚀[¶](#id190 "Link to this heading")

#### General[¶](#id191 "Link to this heading")

* Added a [new report](../../getting-started/running-snowconvert/review-results/reports/functions-usage-report), SQLFunctionsUsage.csv, that summarizes the invocations of built-in and user-defined functions grouped by their migration status. This report allows users to get details about function usages, whether they were transformed to Snowflake with no problem, or whether they require an additional post-conversion action.

#### Teradata[¶](#id192 "Link to this heading")

* Added transformation for the period `CONTAINS` clause

### Fixes[¶](#id193 "Link to this heading")

#### Oracle[¶](#id194 "Link to this heading")

* Fixed the `GENERATED ALWAYS` AS expr column option not being transformed
* Fixed dynamic SQL code strings not having their literal values properly escaped in the output

#### SQL Server[¶](#id195 "Link to this heading")

* Fixed the `DATETIME2` datatype not transformed correctly when precision is specified
* Fixed object names without brackets not being renamed when using the renamed feature
* Promoted SSC-FDM-TS0015 to EWI [SSC-EWI-TS0015](../../technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0015) to fix objects with unsupported datatypes incorrectly marked as successfuly transformed
* Fixed some virtual columns transformed to datatype `VARIANT` instead of the right datatype for their expression
* Implemented transformation for the `STRING_SPLIT` function, previously being left as is in the output code
* Fixed `CREATE FUNCTION` bodies not generated when a `SELECT` statement was found in the `ELSE` clause of an `IF` statement
* Fixed identifiers containing the `@` character producing parsing errors
* Fixed the `DATE_PART` function incorrect transformation when the weekday part is specified
* Fixed the empty statements generated by parsing error recovery causing a pending functional equivalence error to be reported
* Fixed the `DATENAME` function transformation not generating the necessary UDF definitions in the `UDF Helpers` folder
* Fixed the `TRY_CAST/TRY_CONVERT` functions not being transformed in some cases

## Version 1.16.1 (Aug 11, 2025)[¶](#version-1-16-1-aug-11-2025 "Link to this heading")

### New Features 🚀[¶](#id196 "Link to this heading")

* Added Key Pair authentication to login to Snowflake.
* Upgraded data validation Python support to 3.13.

## Version 1.16.0 (Aug 8, 2025)[¶](#version-1-16-0-aug-8-2025 "Link to this heading")

### Fixes[¶](#id197 "Link to this heading")

* Fixed issue with retrieving access codes from SnowConvert due to certificate handling problems.
* Added Data Validation manual execution instruction and scripts.

## Version 1.15.1 (Aug 6, 2025)[¶](#version-1-15-1-aug-6-2025 "Link to this heading")

### New Features 🚀[¶](#id198 "Link to this heading")

* Added support for PostgreSQL Array Expression and Array Access.

### Fixes[¶](#id199 "Link to this heading")

* Fixed transformation for Oracle’s JSON\_OBJECT function.
* Updated links to the new [official documentation site](../../../overview).
* Fixed bug when clicking on retry conversion on a non E2E platform.
* Fixed optional fields in Snowflake connection form.
* Fixed some Oracle functions not being transformed to the correct target.

## Version 1.14.0 (Jul 30, 2025)[¶](#version-1-14-0-jul-30-2025 "Link to this heading")

### New Features 🚀[¶](#id200 "Link to this heading")

* Added Migration Project Context feature.

## Version 1.13.0 (Jul 28, 2025)[¶](#version-1-13-0-jul-28-2025 "Link to this heading")

### New Features 🚀[¶](#id201 "Link to this heading")

* Enhanced data migration performance by increasing default timeout values for large-scale operations including data extraction, analysis, and loading processes.
* Support for [nested procedures](../../../translation-references/oracle/pl-sql-to-snowflake-scripting/README.html#nested-procedures) in Oracle.

### Fixes[¶](#id202 "Link to this heading")

* Routed SnowConvert AI API traffic from Azure-hosted domains (*.azurewebsites.net) to Snowflake-hosted domains (*.snowflake.com) to streamline integration and deliver a unified user experience.
* Fixed SSO authentication token caching during data migration processes, eliminating repeated authentication prompts that previously opened new browser tabs for each request.

## Version 1.12.1 (Jul 21, 2025)[¶](#version-1-12-1-jul-21-2025 "Link to this heading")

### New Features 🚀[¶](#id203 "Link to this heading")

Conversion Option for External Tables for Hive-Spark-Databricks SQL.

### Fixes[¶](#id204 "Link to this heading")

* Backtick Identifiers Support in Sybase.
* Translation for Amazon Redshift COMMENT ON statement.
* Non-returning functions translated to stored procedures for PostgreSQL.

## Version 1.11.1 (Jul 11, 2025)[¶](#version-1-11-1-jul-11-2025 "Link to this heading")

### New Features 🚀[¶](#id205 "Link to this heading")

Support for new Snowflake Out Arguments syntax within Snowflake Scripting on Teradata, Oracle, SQL Server, and Redshift migrations.

### Fixes[¶](#id206 "Link to this heading")

Enhanced Teradata Data Type Handling: JSON to VARIANT migration.
Improved recovery on Redshift procedures written with Python.

## Version 1.11.0 (Jul 1, 2025)[¶](#version-1-11-0-jul-1-2025 "Link to this heading")

### New Features 🚀[¶](#id207 "Link to this heading")

New [Data Validation framework integration](../../user-guide/data-validation) for SQL Server End-to-End experience: Now, users can validate their data after migrating it. The Data Validation framework offers the following validations:
Schema validation: Validate the table structure to attest the correct mappings among datatypes.
Metrics validation: Generate metrics of the data stored in a table, ensuring the consistency of your data post-migration.

## Version 1.3.0 (Mar 25, 2025)[¶](#version-1-3-0-mar-25-2025 "Link to this heading")

### Sybase IQ Support[¶](#sybase-iq-support "Link to this heading")

SnowConvert AI now supports the conversion of Sybase IQ Create Table to Snowflake. This feature includes support for the following:

### New Features 🚀[¶](#id208 "Link to this heading")

* Sybase:

  + Translation of Regular and Temporary Tables
  + Translation of Constraints
  + Translation of Data Types

### Azure Synapse[¶](#azure-synapse "Link to this heading")

* Fix Object References not shown in Object References and Missing Object References reports.
* Added parsing support for Materialized Views with distribution clause

## Version 1.2.17 (Mar 18, 2025)[¶](#version-1-2-17-mar-18-2025 "Link to this heading")

### Azure Synapse Support[¶](#azure-synapse-support "Link to this heading")

SnowConvert AI is adding support for Azure Synapse to Snowflake, now enabling direct translation for Azure Synapse SQL scripts and stored procedures to Snowflake’s SQL dialect. This complements our existing support for Transact-SQL (T-SQL) and provides a more comprehensive solution for users migrating from Microsoft’s data warehousing ecosystem.

### New Features 🚀[¶](#id209 "Link to this heading")

* **Common**:

  + Add a Relation Type column to the [Object References](../../getting-started/running-snowconvert/review-results/reports/object-references-report) and [Missing Object References](../../getting-started/running-snowconvert/review-results/reports/missing-objects-report) reports.

## Version 1.2.16 (Mar 10, 2025)[¶](#version-1-2-16-mar-10-2025 "Link to this heading")

### Redshift Stored Procedures Support[¶](#redshift-stored-procedures-support "Link to this heading")

SnowConvert AI now supports the conversion of Redshift stored procedures to Snowflake, enabling seamless migration of procedural code. This feature includes support for variable operations, control flow statements, cursor handling, and transaction management capabilities.

### New Features 🚀[¶](#id210 "Link to this heading")

Stored procedures new supported functionality.

* **General support**:

  + Transformation for `SELECT INTO` variables inside stored procedures.
  + Transformation for `CASE` statements without ELSE clauses.
  + Transformation of `RETURN` statement in Redshift.
  + Support of `RAISE` for logging, warnings, and exceptions.
* **Variable Binding**:

  + Support for binding variables in stored procedures.
  + Handling positional arguments for binding variables.
  + Variable bindings in the `OPEN cursor` statement.
* **Transaction Support**:

  + Initial support for `COMMIT`, `ROLLBACK`, and `TRUNCATE` statements.
* **Cursor Operations**:

  + Support for the `FETCH` statement.
  + Transformation for `refcursor variable declaration`.
* **DML Operations**:

  + Transformations for `INSERT`, `UPDATE`, `MERGE`, `SELECT INTO` statements.
* `**Control Flow Statements**`:

  + Support for basic control flows statements.
  + Transformations of Labels Stats against loops.
* **DDL Operations**:

  + Support for `CREATE TABLE AS` statement.

### Breaking Changes ⛓️‍💥[¶](#breaking-changes "Link to this heading")

* Renamed Code Unit Name to Code Unit ID in Top-Level Code Units report.

## Version 1.2.6 (Feb 26, 2025)[¶](#version-1-2-6-feb-26-2025 "Link to this heading")

### Oracle[¶](#id211 "Link to this heading")

* Fixed CONSTRAINT clauses incorrectly reported as parsing errors.

### Redshift[¶](#id212 "Link to this heading")

Added

* Support for **Declare** statement.
* Support for **Merge** statement.
* Support for **Update** statement.
* Support for variable declaration with **Refcursor** type.
* Support for **Declare**, **Open** and **Close** Cursor.

### Teradata[¶](#id213 "Link to this heading")

* Fixed ‘chars’, and ‘characters’ built-in functions being reported as missing references.

## Version 1.2.5 (Feb 7, 2025)[¶](#version-1-2-5-feb-7-2025 "Link to this heading")

### Common[¶](#common "Link to this heading")

* Improved SnowConvert AI CLI help messages.

## Version 1.2.4 (Feb 7, 2025)[¶](#version-1-2-4-feb-7-2025 "Link to this heading")

### Common[¶](#id214 "Link to this heading")

* Improved SnowConvert AI CLI help messages.

### Teradata[¶](#id215 "Link to this heading")

* Improved EWI consistency on DATE casting.

## Version 1.2.1 (Jan 31, 2025)[¶](#version-1-2-1-jan-31-2025 "Link to this heading")

### Common[¶](#id216 "Link to this heading")

**Fixed**

* Improved mechanism to validate the SnowConvert AI license by preventing the use of the powershell current user profile settings, ensuring a smoother execution.

## Version 1.2.0 (Jan 28, 2025)[¶](#version-1-2-0-jan-28-2025 "Link to this heading")

* **Free** access for anyone with a corporate email.
* **Redshift** conversion is now supported under preview.
* Remove assessment step. Assessment and conversion are now completed in only one step.
* Introduction of the new Code Completeness Score and Code Unit Methodology.
* Improved messages like Functional Difference Messages (FDMs), Performance Reviews (PRFs) and EWIs (error, warnings, and issues).

### Common[¶](#id217 "Link to this heading")

**Fixed**

* Usage of correlated scalar subqueries erroneously causing [SSC-EWI-0108](../../technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0108) under certain scenarios.

### Teradata[¶](#id218 "Link to this heading")

**Fixed**

* Set **Character Set** as optional in description of columns in derived tables.

## Version 1.1.91 (Dec 19, 2024)[¶](#version-1-1-91-dec-19-2024 "Link to this heading")

### Common[¶](#id219 "Link to this heading")

**Fixed**

* Correlated scalar subqueries missing an aggregate function.
* Uncorrelated scalar subqueries are being marked as unsupported.

### Teradata[¶](#id220 "Link to this heading")

#### Added[¶](#added "Link to this heading")

* Added “ANSI/TERA Session Mode” and “Use COLLATE for Case Specification” settings:

  + ANSI mode with COLLATE.
  + ANSI mode without COLLATE.
  + TERA mode with COLLATE.
  + TERA mode without COLLATE.
* Support parsing of GENERATED TIMECOLUMN column option.
* Support parsing of TD\_NORMALIZE\_MEET function.\

#### Fixed[¶](#fixed "Link to this heading")

* Fixed inconsistencies in column names when it comes to Snowflake reserved keywords.
* Parsing errors in PARTITION BY RANGE\_N clause.
* Improved support for COALESCE expression.

### SQL Server[¶](#id221 "Link to this heading")

#### Fixed[¶](#id222 "Link to this heading")

* Some functions were incorrectly marked as a pending functional.

## Version 1.1.80 (Dec 5, 2024)[¶](#version-1-1-80-dec-5-2024 "Link to this heading")

### Common[¶](#id223 "Link to this heading")

**Fixed**

* SnowConvert AI was incorrectly marking scalar subqueries as invalid when some function aliases were used.
* Crash when SnowConvert AI didn’t have read/write permissions to configuration folder.

### Teradata[¶](#id224 "Link to this heading")

#### Fixed[¶](#id225 "Link to this heading")

* Renaming feature now contemplates function with parameters.
* The UPDATE statement with ELSE INSERT syntax was not converted correctly.

### SQL Server[¶](#id226 "Link to this heading")

#### Fixed[¶](#id227 "Link to this heading")

* SnowConvert AI now successfully converts @@ROWCOUNT using the global variable SQLROWCOUNT.
* View and column names from sys objects are now be paired with INFORMATION\_SCHEMA.

## Version 1.1.69 (Nov 14, 2024)[¶](#version-1-1-69-nov-14-2024 "Link to this heading")

### SQL Server[¶](#id228 "Link to this heading")

#### Fixed[¶](#id229 "Link to this heading")

* BIT Datatype with DEFAULT value is not converted to true or false but 1 or 0.

### Oracle[¶](#id230 "Link to this heading")

#### Fixed[¶](#id231 "Link to this heading")

* Code missing when converting a function with CONNECT BY.

## Version 1.1.67 (Oct 30, 2024)[¶](#version-1-1-67-oct-30-2024 "Link to this heading")

### Teradata[¶](#id232 "Link to this heading")

#### Fixed[¶](#id233 "Link to this heading")

* Flag TeraModeForStirngComparison is set to true as default.

### SQL Server[¶](#id234 "Link to this heading")

#### Fixed[¶](#id235 "Link to this heading")

* Columns with default value are now converted correctly with their respective data type casting.

### Oracle[¶](#id236 "Link to this heading")

#### Fixed[¶](#id237 "Link to this heading")

* Code missing when converting a function with CONNECT BY.

## Version 1.1.63 (Oct 24, 2024)[¶](#version-1-1-63-oct-24-2024 "Link to this heading")

### Common[¶](#id238 "Link to this heading")

* Recovery codes removed from the parsing error messages.
* Windows close button now works as intended.
* Added a new field **domain** to the comment clause for each DDL SnowConvert AI generates.

### Teradata[¶](#id239 "Link to this heading")

**Added**

* Support for UNION ALL clause with different data types and column sizes.
* Support for sp\_executeql.

#### Fixed[¶](#id240 "Link to this heading")

* Inconsistencies in string comparison in Tera mode and ANSI mode.
* Complex column alias with syntax ‘’n is not being recognized by SnowConvert.

### SQL Server[¶](#id241 "Link to this heading")

**Added**

* FDM in every corelated subquery.

#### Fixed[¶](#id242 "Link to this heading")

* Issue with WITH DISTRIBUTION and CLUSTERED in table creation.

### Oracle[¶](#id243 "Link to this heading")

#### Fixed[¶](#id244 "Link to this heading")

* Issue that caused SP conversion to fail when using .rownum within a FOR statement.

## Version 1.1.61 (Oct 18, 2024)[¶](#version-1-1-61-oct-18-2024 "Link to this heading")

### Teradata[¶](#id245 "Link to this heading")

#### Fixed[¶](#id246 "Link to this heading")

* Conversion of stored procedures inside macros is now supported.
* StringSimilarity Teradata Function is now converted successfully

### Oracle[¶](#id247 "Link to this heading")

#### Fixed[¶](#id248 "Link to this heading")

* DATEDIFF\_UDF now returns date difference with timestamp as parameter with decimals (time part difference).

## Version 1.1.56 (Oct 9, 2024)[¶](#version-1-1-56-oct-9-2024 "Link to this heading")

### Teradata[¶](#id249 "Link to this heading")

#### Fixed[¶](#id250 "Link to this heading")

* Create a Stored Procedure to compliance the same flow as in Teradata (StoredProcedure inside a Macro)
* Use a UDF Helper to emulate the functionality given for a VALIDTIME column in Teradata

### Oracle[¶](#id251 "Link to this heading")

#### Fixed[¶](#id252 "Link to this heading")

* Empty Create Statement
* Return date difference with timestamp as parameter with decimals (time part difference).

## Version 1.1.54 (Oct 3, 2024)[¶](#version-1-1-54-oct-3-2024 "Link to this heading")

### Common[¶](#id253 "Link to this heading")

* Improved the auto-update mechanism.

### Teradata[¶](#id254 "Link to this heading")

#### Fixed[¶](#id255 "Link to this heading")

* UDF called “PERIOD\_TO\_TIME\_UDF” is now included as part of the code output if it is used in the converted code.
* UDF called “DATE\_TO\_PERIOD\_UDF” is now included as part of the code output if it is used in the converted code.

### SQL Server[¶](#id256 "Link to this heading")

#### Fixed[¶](#id257 "Link to this heading")

* The CLUSTERED clause is no longer in the output code.

### Oracle[¶](#id258 "Link to this heading")

#### Fixed[¶](#id259 "Link to this heading")

* PARTITION clause in queries is now identified as an EWI instead of FDM.

## Version 1.1.52 (Sep 24, 2024)[¶](#version-1-1-52-sep-24-2024 "Link to this heading")

### Common[¶](#id260 "Link to this heading")

* Adding an informative message when there is no communication to the licensing API and a link with more information of what is happening.
* A new column named “Lines of Code” was added on the report, specifically the “2.1 Conversion Rates Summary” table

### Teradata[¶](#id261 "Link to this heading")

#### Fixed[¶](#id262 "Link to this heading")

* Cast to CHAR/CHARACTER causing parsing error

### SQL Server[¶](#id263 "Link to this heading")

#### Fixed[¶](#id264 "Link to this heading")

* Empty STAT EWI when there is an extra ‘;’.
* Continue statement is not marked as an EWI any more.

### Oracle[¶](#id265 "Link to this heading")

#### Fixed[¶](#id266 "Link to this heading")

* `DATE_TO_RR_FORMAT_UDF` is now included on the output if there is a reference to it on the input source code.

## Version 1.1.45 (Sep 12, 2024)[¶](#version-1-1-45-sep-12-2024 "Link to this heading")

### Common[¶](#id267 "Link to this heading")

Fix Encoding issue SSC-EWI-0041

#### Teradata[¶](#id268 "Link to this heading")

Added

* New conversion setting for TERA MODE strings comparison transformation

Fixed

* Anonymous block of code converted to a stored procedure.
* PRIMARY TIME INDEX not being parsed.

#### SQL Server[¶](#id269 "Link to this heading")

Fixed

* Empty stat should not be classified as pending functional
* SQL report has a text referring to Teradata

#### Oracle[¶](#id270 "Link to this heading")

Added

* Oracle function conversion to Functions (single statement)

Fixed

* DATE\_TO\_RR\_FORMAT\_UDF is added in the view conversion but is not part of the SC output

## Version 1.1.38 (Aug 29, 2024)[¶](#version-1-1-38-aug-29-2024 "Link to this heading")

### Common[¶](#id271 "Link to this heading")

* Improved the performance for running SnowConvert.

#### Teradata[¶](#id272 "Link to this heading")

* Added translation for EXTRACT function.
* Fix translation in procedure when there is a presence of IMMUTABLE/VOLATILE.
* Improved translation of EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF to support timestamp as parameter.

#### SQL Server[¶](#id273 "Link to this heading")

* Improved error handling when translating long-named columns.

#### Oracle[¶](#id274 "Link to this heading")

* Added translation for STANDARD\_HASH function.
* Improved the parser to be able to read DBMS\_DATAPUMP.detach.

## Version 1.1.33 (Aug 9, 2024)[¶](#version-1-1-33-aug-9-2024 "Link to this heading")

### Common[¶](#id275 "Link to this heading")

* Fixed numerous SSC-EWI-0013 occurrences.
* Improved UI experience when user does not have read/write permissions on a particular local directory.

#### Teradata[¶](#id276 "Link to this heading")

* Added translation for `PREPARE STATEMENT`, `ACTIVITY_COUNT`, `DAY_OF_MONTH`, `DAY_OF_WEEK`, `WEEK_OF_CALENDAR`, `MONTH_OF_CALENDAR`.
* Added translation for `CREATE SCHEMA`.
* Fixed `INTERVAL` literal not converted in minus operations.
* Improved parser capability to read `LATEST` as a column name.

#### Oracle[¶](#id277 "Link to this heading")

* Improved translation on PL/SQL parameter data types: VARCHAR and INTEGER.
* Fixed duplicated comments in PL/SQL procedure declarations.

## Version 1.1.26 (Jul 28, 2024)[¶](#version-1-1-26-jul-28-2024 "Link to this heading")

### Oracle[¶](#id278 "Link to this heading")

* Add parsing of `ACCESS PARAMETERS` table options.
* Add parsing of `XMLType` table.
* Added translation for `FUNCTION` definition within anonymous blocks.
* Fixed duplicated code SSC-FDM-OR0045.
* Improve parsing of `XMLSchema` specification.

#### SQLServer[¶](#sqlserver "Link to this heading")

* Fixed `EXECUTE AS` statement wrongly transformed to `EXECUTE IMMEDIATE`.
* Fixed temporary table generated erroneously.
* Improve parsing of `WITH xmlnamespaces` statement.

## Version 1.1.16 (Jun 26, 2024)[¶](#version-1-1-16-jun-26-2024 "Link to this heading")

### Teradata[¶](#id279 "Link to this heading")

* Fixed translation of `LIKE NOT CASESPECIFIC`.
* Improved translation of variable declarations inside `BEGIN…END`.
* Improved parsing of `AS OF` clause and `WITH TIE`S option from `CREATE VIEW`.

#### Oracle[¶](#id280 "Link to this heading")

* Fixed translation for columns with whitespaces in `CREATE VIEW`.
* Improved description of `SSC-EWI-OR0042`.
* Improved parsing of `ACCESSIBLE BY` clause and `SQL_MACRO` option from `CREATE FUNCTION`.
* Improved parsing of the `DECLARE` statement.

#### SQLServer[¶](#id281 "Link to this heading")

* Fixed translation of `BEGIN…END` showing pending functional equivalence.
* Added translation for `FOR XML PATH` clause.

## Version 1.1.9 (Jun 12, 2024)[¶](#version-1-1-9-jun-12-2024 "Link to this heading")

### Common[¶](#id282 "Link to this heading")

* Added more info in the COMMENT clause of each object.

#### Teradata[¶](#id283 "Link to this heading")

* Added an EWI 0073 to `PREPARE` statement.
* Added `OR REPLACE` to `CREATE TABLE`

#### Oracle[¶](#id284 "Link to this heading")

* Added translation for Materialized View’s `REFRESH_MODE` property.
* Improved parsing capability to read MODEL clause and to read CREATE VIEW alternate routes.

## Version 1.1.8 (May 31, 2024)[¶](#version-1-1-8-may-31-2024 "Link to this heading")

### Common[¶](#id285 "Link to this heading")

* Added translation of Materialized View to Dynamic Tables.
* Improved CodeUnit Report to show more code units.

#### SQLServer[¶](#id286 "Link to this heading")

* Added translation of SET ANSI\_NULLS.
* Added translation of INSERT that contains a FROM Subquery + MERGE INTO pattern.

## Version 1.1.6 (May 21, 2024)[¶](#version-1-1-6-may-21-2024 "Link to this heading")

### Teradata[¶](#id287 "Link to this heading")

* Fixed translation for `Cast('POINT(x t)' As ST_GEOMETRY`
* Fixed translation of casting from one format to another.
* Fixed translation related to `DATEADD_UDF` and `TO_INTERVAL_UDF`

#### Oracle[¶](#id288 "Link to this heading")

* Improved parsing capability to read `JSON_OBJECT` and `JSON_ARRAYAGG` built-in functions.

#### SQLServer[¶](#id289 "Link to this heading")

* Improved Missing Object References report’s content.
* Improved robustness during the semantic analysis phase and translation phase.

## Version 1.1.5 (May 10, 2024)[¶](#version-1-1-5-may-10-2024 "Link to this heading")

### Common[¶](#id290 "Link to this heading")

* Provide more information and details for SSC-EWI-0001
* Improved robustness of assessment mode when providing free tables.

#### Teradata[¶](#id291 "Link to this heading")

* Improved translation related to date handling.
* Improved parsing capability to read code that contains block comments.
* Improved parsing capability to read NOT NULL column option before the data type declaration in a table.
* Improved the functionality of TIMESTAMP\_DIFFERENCE\_UDF and EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF.

#### SQL Server[¶](#id292 "Link to this heading")

* Improved translation for ALTER TABLE CHECK constraint.

## Version 1.1.4 (May 2, 2024)[¶](#version-1-1-4-may-2-2024 "Link to this heading")

### Common[¶](#id293 "Link to this heading")

* Added new breaking change at the UI. Now, the user will have to inquire about an access code for doing their assessment. For more details, please check [here](../../user-guide/snowconvert/how-to-request-an-access-code/README).
* Added a new assessment report EmbeddedCodeUnitReport, for more information, please visit [here](../../getting-started/running-snowconvert/review-results/reports/embedded-code-units-report).
* Improved the TopLevelCodeUnitReport. Added four more columns: FDM Count, PRF Count, FDM and PRF. For more information, please visit [here](../../getting-started/running-snowconvert/review-results/reports/embedded-code-units-report.html#information-in-the-embedded-code-units-report).
* Fixed an unexpected error in creating an assessment report.

#### Teradata[¶](#id294 "Link to this heading")

* Added translation for CONTINUE HANDLER.
* Added new parsing capability for BYTE data type.
* Improved binding variable translations.

#### Oracle[¶](#id295 "Link to this heading")

* Added and improved parsing capability to read EXPLAIN PLAN statement, U-Literals and CTAS.
* Improve CURSOR translation when it has to define a cursor with object\_construct.
* Improved translation of procedure parameters avoiding deployment errors.

#### SQLServer[¶](#id296 "Link to this heading")

* Added translation for DB\_ID function.
* Added basic translation for CREATE SCHEMA.
* Added an FDM for CREATE INDEX.
* Improved ALTER TABLE translation.

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

1. [Version 2.2.2 (Jan 13, 2026)](#version-2-2-2-jan-13-2026)
2. [Version 2.2.1 (Jan 08, 2026)](#version-2-2-1-jan-08-2026)
3. [Version 2.2.0 (Jan 07, 2026)](#version-2-2-0-jan-07-2026)
4. [Version 2.1.0 (Dec 18, 2025)](#version-2-1-0-dec-18-2025)
5. [Version 2.0.86 (Dec 10, 2025)](#version-2-0-86-dec-10-2025)
6. [Version 2.0.57 (Dec 03, 2025)](#version-2-0-57-dec-03-2025)
7. [Version 2.0.34 (Nov 27, 2025)](#version-2-0-34-nov-27-2025)
8. [Version 2.0.30 (Nov 26, 2025)](#version-2-0-30-nov-26-2025)
9. [Version 2.0.8 (Nov 21, 2025)](#version-2-0-8-nov-21-2025)
10. [Version 2.0.0 (Nov 20, 2025)](#version-2-0-0-nov-20-2025)
11. [Version 1.21.0 (Nov 08, 2025)](#version-1-21-0-nov-08-2025)
12. [Version 1.20.11 (Nov 07, 2025)](#version-1-20-11-nov-07-2025)
13. [Version 1.20.10 (Nov 06, 2025)](#version-1-20-10-nov-06-2025)
14. [Version 1.20.8 (Nov 05, 2025)](#version-1-20-8-nov-05-2025)
15. [Version 1.20.7 (Oct 31, 2025)](#version-1-20-7-oct-31-2025)
16. [Version 1.20.6 (Oct 29, 2025)](#version-1-20-6-oct-29-2025)
17. [Version 1.20.3 (Oct 20, 2025)](#version-1-20-3-oct-20-2025)
18. [Version 1.20.2 (Oct 20, 2025)](#version-1-20-2-oct-20-2025)
19. [Version 1.20.1 (Oct 16, 2025)](#version-1-20-1-oct-16-2025)
20. [Version 1.20.0 (Oct 15, 2025)](#version-1-20-0-oct-15-2025)
21. [Version 1.19.7 (Oct 10, 2025)](#version-1-19-7-oct-10-2025)
22. [Version 1.19.6 (Oct 08, 2025)](#version-1-19-6-oct-08-2025)
23. [Version 1.19.5 (Oct 03, 2025)](#version-1-19-5-oct-03-2025)
24. [Version 1.19.4 (Oct 1, 2025)](#version-1-19-4-oct-1-2025)
25. [Version 1.19.3 (Sep 29, 2025)](#version-1-19-3-sep-29-2025)
26. [Version 1.19.2 (Sep 26, 2025)](#version-1-19-2-sep-26-2025)
27. [Version 1.19.0 (Sep 24, 2025)](#version-1-19-0-sep-24-2025)
28. [Version 1.18.3 (Sep 22, 2025)](#version-1-18-3-sep-22-2025)
29. [Version 1.18.0 (Sep 18, 2025)](#version-1-18-0-sep-18-2025)
30. [Version 1.17.6 (Sep 5, 2025)](#version-1-17-6-sep-5-2025)
31. [Version 1.17.2 (Sep 4, 2025)](#version-1-17-2-sep-4-2025)
32. [Version 1.17.1 (Sep 1, 2025)](#version-1-17-1-sep-1-2025)
33. [Version 1.16.2 (Aug 19, 2025)](#version-1-16-2-aug-19-2025)
34. [Version 1.16.1 (Aug 11, 2025)](#version-1-16-1-aug-11-2025)
35. [Version 1.16.0 (Aug 8, 2025)](#version-1-16-0-aug-8-2025)
36. [Version 1.15.1 (Aug 6, 2025)](#version-1-15-1-aug-6-2025)
37. [Version 1.14.0 (Jul 30, 2025)](#version-1-14-0-jul-30-2025)
38. [Version 1.13.0 (Jul 28, 2025)](#version-1-13-0-jul-28-2025)
39. [Version 1.12.1 (Jul 21, 2025)](#version-1-12-1-jul-21-2025)
40. [Version 1.11.1 (Jul 11, 2025)](#version-1-11-1-jul-11-2025)
41. [Version 1.11.0 (Jul 1, 2025)](#version-1-11-0-jul-1-2025)
42. [Version 1.3.0 (Mar 25, 2025)](#version-1-3-0-mar-25-2025)
43. [Version 1.2.17 (Mar 18, 2025)](#version-1-2-17-mar-18-2025)
44. [Version 1.2.16 (Mar 10, 2025)](#version-1-2-16-mar-10-2025)
45. [Version 1.2.6 (Feb 26, 2025)](#version-1-2-6-feb-26-2025)
46. [Version 1.2.5 (Feb 7, 2025)](#version-1-2-5-feb-7-2025)
47. [Version 1.2.4 (Feb 7, 2025)](#version-1-2-4-feb-7-2025)
48. [Version 1.2.1 (Jan 31, 2025)](#version-1-2-1-jan-31-2025)
49. [Version 1.2.0 (Jan 28, 2025)](#version-1-2-0-jan-28-2025)
50. [Version 1.1.91 (Dec 19, 2024)](#version-1-1-91-dec-19-2024)
51. [Version 1.1.80 (Dec 5, 2024)](#version-1-1-80-dec-5-2024)
52. [Version 1.1.69 (Nov 14, 2024)](#version-1-1-69-nov-14-2024)
53. [Version 1.1.67 (Oct 30, 2024)](#version-1-1-67-oct-30-2024)
54. [Version 1.1.63 (Oct 24, 2024)](#version-1-1-63-oct-24-2024)
55. [Version 1.1.61 (Oct 18, 2024)](#version-1-1-61-oct-18-2024)
56. [Version 1.1.56 (Oct 9, 2024)](#version-1-1-56-oct-9-2024)
57. [Version 1.1.54 (Oct 3, 2024)](#version-1-1-54-oct-3-2024)
58. [Version 1.1.52 (Sep 24, 2024)](#version-1-1-52-sep-24-2024)
59. [Version 1.1.45 (Sep 12, 2024)](#version-1-1-45-sep-12-2024)
60. [Version 1.1.38 (Aug 29, 2024)](#version-1-1-38-aug-29-2024)
61. [Version 1.1.33 (Aug 9, 2024)](#version-1-1-33-aug-9-2024)
62. [Version 1.1.26 (Jul 28, 2024)](#version-1-1-26-jul-28-2024)
63. [Version 1.1.16 (Jun 26, 2024)](#version-1-1-16-jun-26-2024)
64. [Version 1.1.9 (Jun 12, 2024)](#version-1-1-9-jun-12-2024)
65. [Version 1.1.8 (May 31, 2024)](#version-1-1-8-may-31-2024)
66. [Version 1.1.6 (May 21, 2024)](#version-1-1-6-may-21-2024)
67. [Version 1.1.5 (May 10, 2024)](#version-1-1-5-may-10-2024)
68. [Version 1.1.4 (May 2, 2024)](#version-1-1-4-may-2-2024)