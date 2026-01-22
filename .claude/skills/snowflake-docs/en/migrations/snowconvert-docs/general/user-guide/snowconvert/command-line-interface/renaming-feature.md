---
auto_generated: true
description: Renaming objects during a database migration process is something that
  a lot of users need to do. For this reason, SnowConvert AI enables the Renaming
  feature to allow defining new names for the follo
last_scraped: '2026-01-14T16:52:56.875021+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/command-line-interface/renaming-feature
title: SnowConvert AI - Renaming feature | Snowflake Documentation
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)GeneralUser Guide[SnowConvert AI](../README.md)[Command Line Interface](README.md)Renaming Feature

# SnowConvert AI - Renaming feature[¶](#snowconvert-ai-renaming-feature "Link to this heading")

Renaming objects during a database migration process is something that a lot of users need to do. For this reason, SnowConvert AI enables the Renaming feature to allow defining new names for the following types of user-defined objects:

Note

This feature is supported for Teradata, Sql Server and Redshift **ONLY**.

* Schemas
* Tables
* Views
* Materialized Views
* Procedures
* Functions
* Macros

Note

The renaming feature will apply to both the object definition and the object’s uses.

These objects are usually qualified within a schema or a database, so, depending on the Database platform, the object `Table1` might be referenced simply as `Table1`, as `MySchema.Table1` or as `MyDatabase.MySchema.Table1`. It is **essential** to fully qualify each object in the renaming file to avoid ambiguity.

The new object names are specified via a .json file with the following format.

Note

Note that this example contains a “Macros” section, this is a **Teradata** specific element, and may vary depending on the specified language.

```
{
  "Schemas": {
    "SchemaName": "NewSchema"
  },
  "Tables": {
    "SchemaName.TableName": "NewSchema.TableNameChanged",
    "Table1": "Table2"
  },
  "TablesRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "Prefix_$1.$2"
    }
  ],
  
  "Views": {
    "ViewName": "ViewNameChanged",
    "MaterializedViewName": "MaterializedViewNameChanged",
  },
  "ViewsRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],
  
  "Procedures": {
    "ProcedureName": "ProcedureNameChanged"
  },
  "ProceduresRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],
  
  "Macros": {
    "SchemaName.MacroName": "MacroNameChanged",
    "SimpleMacro": "SimpleMacroSf"
  },
  "MacrosRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],
  
  "Functions": {
    "SchemaName.FunctionName": "FunctionNameChanged",
    "SimpleFunction": "SimpleFunctionSf"
  },
  "FunctionsRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ]
}
```

Copy

## Usage[¶](#usage "Link to this heading")

In order to use the renaming feature you have to execute the CLI version of SnowConvert AI with the following argument `--RenamingFile` and provide the path to the .json file containing the renaming information. An example of the command can look like this:

> snowct.exe -i “somePath/input” -o “somePath/output” –RenamingFile “somePath/renamings.json”

### Renaming modes[¶](#renaming-modes "Link to this heading")

Notice there are two fields for each kind of object: `"Tables"` and `"TablesRegex"`*,* `"Views"` and `"ViewsRegex"`, and so on. This is because there are two ways in which renamings can be specified.

#### Object by object (line by line)[¶](#object-by-object-line-by-line "Link to this heading")

In this mode, each line represents an object, and it must contain the original fully qualified name and the new name. So, if we want to move an object named “Table1” inside the schema *“OriginalSchema”* to the schema *“SchemaSF”*, the line must be like this:

```
"OriginalSchema.Table1": "SchemaSF.Table1"
```

Copy

If we also want to rename it to “Table2”, the line should be like this:

```
"OriginalSchema.Table1": "SchemaSF.Table2"
```

Copy

This information has to be specified in the `"Tables"`*,* `"Views"`*,* `"Procedures"`*,* `"Macros"` *and* `"Functions"` sections of the .json file and each line must be separated with a comma. Let’s take a look at an example:

**TableExample1**

```
"Tables": {
    "Schema1.Table1": "SF_Schema1.SF_Table1",
    "Schema1.Table2": "SF_Schema1.SF_Table2",
    "Schema1.Table3": "SF_Schema1.SF_Table3"
  },
```

Copy

The above sample is saying that the only three tables in the whole workload to be renamed are the ones called “*Table1*”, “*Table2*” and “*Table3*”, all located inside the “Schema1” schema; they must be renamed to “*SF\_Table1”, “SF*\_*Table2”* and *“SF*\_*Table3”,* respectively; and finally, they will be located under the *“SF\_Schema1*” schema in Snowflake.

#### Regular expressions[¶](#regular-expressions "Link to this heading")

If there is a need to rename multiple objects in the same way, the feature also allows regular expressions to define patterns to apply to objects of the same kind. Two lines are required to specify each renaming, the first line is `"RegexExpr"` which is the matching expression and the second line is the `"RegexReplace"` which is the replacing expression. This information has to be provided in the `"TablesRegex"`*,* `"ViewsRegex"`*,* `"ProceduresRegex"`*,* `"MacrosRegex"` and `"FunctionsRegex"` sections of the .json file. So, the previous example can also be written in the following manner, using the regular expression feature.

**TableExample2**

```
"TablesRegex": [
    {
      "RegexExpr": "Schema1\\.(.*)",
      "RegexReplace": "SF_Schema1.SF_$1"
    }
  ],
```

Copy

The only difference is that this way applies to all tables located within the “Schema1” schema. The regex expression would match all tables defined within the “Schema1” schema and will create a capturing group with everything after the dot. The regex replace will move the tables to the “SF\_Schema1” schema and will add the “SF\_” prefix to all tables found referencing the first group created ($1) in the regex expression.

#### Renaming priority[¶](#renaming-priority "Link to this heading")

There might be renamings that apply to the same object and only one of them is chosen. Within the same section, SnowConvert AI will apply the first renaming that matches the current object’s name, and it will stop trying to rename that object. So in the following example, despite the fact that `"Tables"` section specifies renaming “Table1” to “Table1-a” and also to “Table1-b”, SnowConvert AI will only rename it to “Table1-a”.

```
"Tables": {
    "Schema1.Table1": "Schema1.Table1-a",
    "Schema1.Table1": "Schema1.Table1-b",
  },
```

Copy

Also, SnowConvert AI will try to rename an object first checking the object by object renaming section before trying the regular expressions section. So, in the following example despite the fact that both renamings can apply to the same object “Schema1.Table1”, only the one defined in the `"Tables"` section is applied.

```
"Tables": {
    "Schema1.Table1": "Schema1.TableA",
  }, 
  "TablesRegex": [
    {
      "RegexExpr": "Schema1\\.(.*)",
      "RegexReplace": "Schema1.SF_$1"
    }
  ],
```

Copy

#### Example[¶](#example "Link to this heading")

Let’s say we have the following input code.

**Input Code**

```
CREATE TABLE CLIENT ( 
    ID INTEGER, 
    NAME varchar(20));
    
CREATE TABLE TICKET ( 
    CLIENT_ID INTEGER,
    FOREIGN KEY (CLIENT_ID_FK) REFERENCES CLIENT(ID));
    
SELECT * FROM CLIENT;
```

Copy

And the following renaming information

**Renaming File (.JSON)**

```
{
  "Tables": {
    "CLIENT": "USER"
  }
}
```

Copy

This would be the output code with and without renaming.

#### Snowflake output code[¶](#snowflake-output-code "Link to this heading")

```
CREATE OR REPLACE TABLE CLIENT (
    ID INTEGER,
    NAME varchar(20))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE TICKET (
    CLIENT_ID INTEGER,
       FOREIGN KEY (CLIENT_ID_FK) REFERENCES CLIENT (ID))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

SELECT
    * FROM
    CLIENT;
```

Copy

```
CREATE OR REPLACE TABLE USER (
    ID INTEGER,
    NAME varchar(20))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE TICKET (
    CLIENT_ID INTEGER,
       FOREIGN KEY (CLIENT_ID_FK) REFERENCES USER (ID))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

SELECT
    * FROM
    USER;
```

Copy

Notice how all the references to “CLIENT” are renamed to “USER”

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

1. [Usage](#usage)