---
auto_generated: true
description: ''
last_scraped: '2026-01-14T16:52:02.995339+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/oracle-conversion-settings
title: SnowConvert AI -  Oracle Conversion Settings | Snowflake Documentation
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
          + [Getting Started](../../README.md)

            - [System Requirements](../../system-requirements.md)
            - [Best Practices](../../best-practices.md)
            - [Download And Access](../../download-and-access.md)
            - [Code Extraction](../../code-extraction/README.md)
            - [Running Snowconvert AI](../README.md)

              * [Supported Languages](../supported-languages/README.md)
              * [Validation](../validation/README.md)
              * [Conversion](README.md)

                + [SQL Server Conversion Settings](sql-server-conversion-settings.md)
                + [General Conversion Settings](general-conversion-settings.md)
                + [Converting Subfolders](converting-subfolders.md)
                + [Oracle Conversion Settings](oracle-conversion-settings.md)
                + [Teradata Conversion Settings](teradata-conversion-settings.md)
                + [Preview Features Settings](preview-conversion-settings.md)
              * [Review Results](../review-results/README.md)
            - [Training And Support](../../training-and-support.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)Oracle Conversion Settings

# SnowConvert AI - Oracle Conversion Settings[¶](#snowconvert-ai-oracle-conversion-settings "Link to this heading")

## General Conversion Settings[¶](#general-conversion-settings "Link to this heading")

### Object Conversion[¶](#object-conversion "Link to this heading")

![Object Conversion Settings page](../../../../../../_images/oracle-object-conversion-settings.png)

1. **Transform Synonyms:** Flag to indicate whether or not Synonyms should be transformed. By default, it’s set to true.
2. **Transform Packages to new Schemas:** Flag to indicate whether or not the Packages should be transformed to new Schemas.

   Please check the naming of the procedure enabling and disabling the flag:

**Input**

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

**Output Default**

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

**Output with param disablePackagesAsSchemas**

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

3. **Transform Date as Timestamp:**

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` *or* `CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to `TIMESTAMP`.

**Input**

```
CREATE TABLE DATE_TABLE(
    DATE_COL DATE
);

SELECT SYSDATE FROM DUAL;
```

Copy

**Output Default**

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

**Output with param disableDateAsTimestamp**

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

4. **Transform OUTER JOINS to ANSI Syntax:** Flag to indicate whether Outer Joins should be transformed to only ANSI syntax.

### Data type mappings[¶](#data-type-mappings "Link to this heading")

![Data type mappings settings page](../../../../../../_images/data-type-mappings-settings.png)

SnowConvert defines default mappings for data type conversions. However, you can point to a JSON file to customize specific data type mappings.

**Customize data types:** You can upload a JSON file to define specific data type transformation rules. This feature allows you to customize how data types are converted during migration.

**Supported transformations include:**

* `NUMBER` to custom `NUMBER` with specific precision and scale
* `NUMBER` to `DECFLOAT` for preserving exact decimal precision

When you upload a data type customization file:

* SnowConvert AI applies your transformation rules during conversion
* Numeric literals in `INSERT` statements targeting customized columns are automatically cast to the appropriate type
* A [TypeMappings Report](../review-results/reports/type-mappings-report) is generated showing all data type transformations applied

**JSON Structure:**

The JSON file supports three ways to specify data type changes:

| Method | Scope | Use Case |
| --- | --- | --- |
| `projectTypeChanges.types` | Global | Transform all occurrences of a specific data type |
| `projectTypeChanges.columns` | Global | Transform columns matching a name pattern (case-insensitive substring match) |
| `specificTableTypeChanges.tables` | Table-specific | Transform specific columns in specific tables |

Warning

**Use column name patterns carefully.** The `projectTypeChanges.columns` rules only apply to columns with `NUMBER` data types, but they match by name pattern without considering the precision or scale of the original `NUMBER` type. This means a pattern like `"MONTH"` will transform **all** matching `NUMBER` columns to the target type, regardless of their original precision (e.g., `NUMBER(10,0)`, `NUMBER(38,18)`, or `NUMBER` without precision). Always review the [TypeMappings Report](../review-results/reports/type-mappings-report) after conversion to verify that the transformations were applied correctly.

**Priority order:** When multiple rules apply to the same column, SnowConvert AI uses this priority (highest to lowest):

1. `specificTableTypeChanges` (most specific)
2. `projectTypeChanges.columns` (name pattern)
3. `projectTypeChanges.types` (global type mapping)

**Example JSON configuration:**

```
{
  "projectTypeChanges": {
    "types": {
      "NUMBER": "DECFLOAT",
      "NUMBER(10, 0)": "NUMBER(18, 0)"
    },
    "columns": [
      {
        "nameExpression": "PRICE",
        "targetType": "DECFLOAT"
      },
      {
        "nameExpression": ".*_AMOUNT$",
        "targetType": "NUMBER(18, 2)"
      }
    ]
  },
  "specificTableTypeChanges": {
    "tables": [
      {
        "tableName": "EMPLOYEES",
        "columns": [
          {
            "columnName": "SALARY",
            "targetType": "NUMBER(15, 2)"
          }
        ]
      }
    ]
  }
}
```

Copy

**Download template:** Copy and save the JSON structure above as your starting point.

**Example transformation:**

Given the following Oracle input code:

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE TABLE employees (
    employee_ID NUMBER,
    manager_YEAR NUMBER(10, 0),
    manager_MONTH NUMBER(10, 0),
    salary NUMBER(12, 2)
);
```

Copy

And a JSON customization file with:

* `"NUMBER": "NUMBER(11, 2)"` in `projectTypeChanges.types`
* `"NUMBER(10, 0)": "NUMBER(18, 0)"` in `projectTypeChanges.types`
* `"MONTH"` pattern targeting `NUMBER(2,0)` in `projectTypeChanges.columns`
* `SALARY` column targeting `NUMBER(15, 2)` in `specificTableTypeChanges` for EMPLOYEES table

The output will be:

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TABLE employees (
    employee_ID NUMBER(11, 2),
    manager_YEAR NUMBER(18, 0),
    manager_MONTH NUMBER(2, 0),
    salary NUMBER(15, 2)
);
```

Copy

| Column | Original Type | Transformed To | Rule Applied |
| --- | --- | --- | --- |
| employee\_ID | NUMBER | NUMBER(11, 2) | `projectTypeChanges.types` |
| manager\_YEAR | NUMBER(10, 0) | NUMBER(18, 0) | `projectTypeChanges.types` |
| manager\_MONTH | NUMBER(10, 0) | NUMBER(2, 0) | `projectTypeChanges.columns` (MONTH pattern) |
| salary | NUMBER(12, 2) | NUMBER(15, 2) | `specificTableTypeChanges` (highest priority) |

### General Result Tab[¶](#general-result-tab "Link to this heading")

![General Results Tab](../../../../../../_images/image%28540%29.png)

1. **Comment objects with missing dependencies:** This flag indicates whether the user wants to comment on nodes with missing dependencies.
2. **Set encoding of the input files:** Check [General Conversion Settings](general-conversion-settings) for more details.

Note

To review the Settings that apply to all supported languages, go to the following [article](general-conversion-settings).

## DB Objects Names Settings[¶](#db-objects-names-settings "Link to this heading")

![DB Objects Names Settings page](../../../../../../_images/image%28414%29.png)

1. **Schema:** The string value specifies the custom schema name to apply. If not specified, the original database name will be used. Example: DB1.**myCustomSchema**.Table1.
2. **Database:** The string value specifies the custom database name to apply. Example: **MyCustomDB**.PUBLIC.Table1.
3. **Default:** None of the above settings will be used in the object names.

## Prepare Code Settings[¶](#prepare-code-settings "Link to this heading")

![Prepare Code Settings page](../../../../../../_images/image%28416%29.png)

### **Description**[¶](#description "Link to this heading")

**Prepare my code:** Flag to indicate whether the input code should be processed before parsing and transformation. This can be useful to improve the parsing process. By default, it’s set to FALSE.

Splits the input code top-level objects into multiple files. The containing folders would be organized as follows:

Copy

```
└───A new folder named ''[input_folder_name]_Processed''
    └───Top-level object type
        └───Schema name
```

Copy

### **Example**[¶](#example "Link to this heading")

#### **Input**[¶](#input "Link to this heading")

```
├───in
│       DDL_Packages.sql
│       DDL_Procedures.sql
│       DDL_Tables.sql
```

Copy

#### **Output**[¶](#output "Link to this heading")

Assume that the name of the files is the name of the top-level objects in the input files.

```
├───in_Processed
    ├───package
    │   └───MY_SCHEMA
    │           MY_FIRST_PACKAGE.sql
    │           ANOTHER_PACKAGE.sql
    │
    ├───procedure
    │   └───MY_SCHEMA
    │           A_PROCEDURE.sql
    │           ANOTHER_PROCEDURE.sql
    │           YET_ANOTHER_PROCEDURE.sql
    │
    └───table
        └───MY_SCHEMA
                MY_TABLE.sql
                ADDITIONAL_TABLE.sql
                THIRD_TABLE.sql
```

Copy

Inside the “schema name” folder, there should be as many files as top-level objects in the input code. Also, it is possible to have copies of some files when multiple same-type top-level objects have the same name. In this case, the file names will be enumerated in ascending order.

![](../../../../../../_images/image%28541%29.png)

### Requirements [¶](#requirements "Link to this heading")

To identify top-level objects, a tag must be included in a comment before their declaration. Our [Extraction](../../code-extraction/oracle) scripts generate these tags.

The tag should follow the next format:

```
<sc-top_level_object_type>top_level_object_name</sc-top_level_object_type>
```

Copy

You can follow the next example:

```
/* <sc-table> MY_SCHEMA.MY_TABLE</sc-table> */
CREATE TABLE "MY_SCHEMA"."MY_TABLE" (
    "MY_COLUMN" VARCHAR2(128)
) ;
```

Copy

## Conversion Rate Settings[¶](#conversion-rate-settings "Link to this heading")

![Conversion Rate Settings page](../../../../../../_images/image%28417%29.png)

On this page, you can choose whether the successfully converted code percentage is calculated using lines of code or using the total number of characters. The **character conversion rate** is the default option. You can read the entire rate documentation on the[documentation page](../../../user-guide/snowconvert/README).

## Stored Procedures Target Languages Settings[¶](#stored-procedures-target-languages-settings "Link to this heading")

![Stored Procedures Target Languages Settings page](../../../../../../_images/image%28418%29.png)

On this page, you can choose whether stored procedures are migrated to JavaScript embedded in Snow SQL, or to Snowflake Scripting. The default option is Snowflake Scripting.

**Reset Settings:** The reset settings option appears on every page. If you’ve made changes, you can reset SnowConvert AI to its original default settings.

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

1. [General Conversion Settings](#general-conversion-settings)
2. [DB Objects Names Settings](#db-objects-names-settings)
3. [Prepare Code Settings](#prepare-code-settings)
4. [Conversion Rate Settings](#conversion-rate-settings)
5. [Stored Procedures Target Languages Settings](#stored-procedures-target-languages-settings)