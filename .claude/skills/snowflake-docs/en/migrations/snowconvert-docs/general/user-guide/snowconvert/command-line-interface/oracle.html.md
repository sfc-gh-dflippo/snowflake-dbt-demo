---
auto_generated: true
description: Flag to indicate whether SnowConvert AI should migrate the procedures
  to Javascript and Python. By default, it is set to false.
last_scraped: '2026-01-14T16:55:47.233172+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/command-line-interface/oracle.html
title: SnowConvert AI - Oracle | Snowflake Documentation
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../README.md)

              - [How To Install The Tool](../how-to-install-the-tool/README.md)
              - [How To Request An Access Code](../how-to-request-an-access-code/README.md)
              - [Command Line Interface](README.md)

                * [Renaming Feature](renaming-feature.md)
                * [Oracle](oracle.md)
                * [Teradata](teradata.md)
                * [SQL Server](sql-server.md)
                * [Redshift](redshift.md)
              - [What Is A SnowConvert AI Project](../what-is-a-snowconvert-project.md)
              - [How To Update The Tool](../how-to-update-the-tool.md)
              - [How To Use The SnowConvert AI Cli](../how-to-use-the-snowconvert-cli.md)
            + [Project Creation](../../project-creation.md)
            + [Extraction](../../extraction.md)
            + [Deployment](../../deployment.md)
            + [Data Migration](../../data-migration.md)
            + [Data Validation](../../data-validation.md)
            + [Power BI Repointing](../../power-bi-repointing-general.md)
            + [ETL Migration](../../etl-migration-replatform.md)
          + [Technical Documentation](../../../technical-documentation/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)GeneralUser Guide[SnowConvert AI](../README.md)[Command Line Interface](README.md)Oracle

# SnowConvert AI - Oracle[¶](#snowconvert-ai-oracle "Link to this heading")

## Specific CLI arguments[¶](#specific-cli-arguments "Link to this heading")

### `--disableSnowScript`[¶](#disablesnowscript "Link to this heading")

Flag to indicate whether SnowConvert AI should migrate the procedures to Javascript and Python. By default, it is set to **false**.

#### `--disableSynonym`[¶](#disablesynonym "Link to this heading")

Flag to indicate whether or not Synonyms should be transformed. By default, it’s set to **true**.

#### `--disablePackagesAsSchemas`[¶](#disablepackagesasschemas "Link to this heading")

Flag to indicate whether or not the Packages should be transformed to new Schemas.

Please check the naming of the procedure enabling and disabling the flag:

```
CREATE OR REPLACE PACKAGE emp_mgmt AS
PROCEDURE remove_emp (employee_id NUMBER );
END emp_mgmt;

CREATE OR REPLACE PACKAGE BODY emp_mgmt AS 
PROCEDURE remove_emp (employee_id NUMBER) IS 
   BEGIN 
      DELETE FROM employees 
      WHERE employees.employee_id = remove_emp.employee_id; 
      tot_emps := tot_emps - 1; 
   END; 
END emp_mgmt;
```

Copy

```
CREATE SCHEMA IF NOT EXISTS emp_mgmt
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE emp_mgmt.remove_emp (employee_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DELETE FROM
         employees
         WHERE employees.employee_id = remove_emp.employee_id;
         tot_emps :=
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
                     tot_emps - 1;
   END;
$$;
```

Copy

```
-- Additional Params: --disablePackagesAsSchemas
CREATE OR REPLACE PROCEDURE EMP_MGMT_REMOVE_EMP (employee_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DELETE FROM
         employees
         WHERE employees.employee_id = remove_emp.employee_id;
         tot_emps :=
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
                     tot_emps - 1;
   END;
$$;
```

Copy

#### `--outerJoinsToOnlyAnsiSyntax`[¶](#outerjoinstoonlyansisyntax "Link to this heading")

Flag to indicate whether Outer Joins should be transformed to only ANSI syntax.

#### `--disableDateAsTimestamp`[¶](#disabledateastimestamp "Link to this heading")

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` *or* `CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to `TIMESTAMP`.

```
CREATE TABLE DATE_TABLE(
    DATE_COL DATE
);

SELECT SYSDATE FROM DUAL;
```

Copy

```
CREATE OR REPLACE TABLE DATE_TABLE (
        DATE_COL TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    SELECT
        CURRENT_TIMESTAMP()
    FROM DUAL;
```

Copy

```
-- Additional Params: --disableDateAsTimestamp
CREATE OR REPLACE TABLE DATE_TABLE (
        DATE_COL DATE /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

SELECT
    CURRENT_DATE()
FROM DUAL;
```

Copy

Learn more about how you can get access to the SnowConvert AI for Oracle Command Line Interface tool by filling out the form on our [**Snowflake Migrations Info**](https://www.mobilize.net/services/database-migrations/snowflake/get-info) page.

#### `--arrange`[¶](#arrange "Link to this heading")

Flag to indicate whether the input code should be processed before parsing and transformation.

Learn more about this step on our **Processing the code** page.

#### `--dataTypeCustomizationFile`[¶](#datatypecustomizationfile "Link to this heading")

The path to a .json file that specifies rules of data type transformation considering data type origin and column name. This feature allows you to customize how data types are transformed during migration, including support for transforming `NUMBER` columns to `DECFLOAT`.

When this argument is provided, SnowConvert AI generates a [TypeMappings Report](../../../getting-started/running-snowconvert/review-results/reports/type-mappings-report) that shows all data type transformations applied, making it easy to verify your customization rules were applied correctly.

Navigate to the [Data Type Customization](../../../../translation-references/oracle/basic-elements-of-oracle-sql/data-types/README.html#data-type-customization) documentation to learn more about configuring data type transformation rules.

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

1. [Specific CLI arguments](#specific-cli-arguments)