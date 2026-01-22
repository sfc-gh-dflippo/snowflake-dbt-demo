---
auto_generated: true
description: SQL Server
last_scraped: '2026-01-14T16:54:01.850340+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-built-in-procedures
title: SnowConvert AI - SQL Server-Azure Synapse - Built-in procedures | Snowflake
  Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Built-in Procedures

# SnowConvert AI - SQL Server-Azure Synapse - Built-in procedures[¶](#snowconvert-ai-sql-server-azure-synapse-built-in-procedures "Link to this heading")

## SP\_ADDEXTENDEDPROPERTY\_UDP[¶](#sp-addextendedproperty-udp "Link to this heading")

Applies to

* SQL Server

### Description[¶](#description "Link to this heading")

Adds a new extended property to a database object.

#### SQLServer syntax[¶](#sqlserver-syntax "Link to this heading")

```
 sp_addextendedproperty
    [ @name = ] N'name'
    [ , [ @value = ] value ]
    [ , [ @level0type = ] 'level0type' ]
    [ , [ @level0name = ] N'level0name' ]
    [ , [ @level1type = ] 'level1type' ]
    [ , [ @level1name = ] N'level1name' ]
    [ , [ @level2type = ] 'level2type' ]
    [ , [ @level2name = ] N'level2name' ]
[ ; ]
```

Copy

### Custom UDP[¶](#custom-udp "Link to this heading")

Keeps the same parameters as the original procedure

#### UDP[¶](#udp "Link to this heading")

```
 -- <copyright file="SP_ADDEXTENDEDPROPERTY_UDP.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2023 Snowflake Inc. All rights reserved.
-- </copyright>

-- =======================================================================================================
-- Description: The sp_addextendedproperty provides an equivalent functionality for adding extended 
--              properties in Snowflake. This version is only supporting 'MS_Description' property to 
--              add comments at schema/table/view/procedure/function level. 
--              Comments on columns are only supported for tables.
--              If the name of the object includes double quotes, they need to be added as part of the 
--              parameter values, for example level1name='"My_Col"'.

-- Parameters:
--   name:       Name of the extended property. 'MS_Description' is the only supported in this version.
--   value:      Value of the extended property. Cannot be null for 'MS_Description' property.
--   level0type: Type of level 0 object. SCHEMA is the only supported value in this version. 
--   level0name: Value associated to the level 0 object.
--   level1type: Type of level 1 object. TABLE/VIEW/PROCEDURE/FUNCTION are the only supported values in this 
--               version. 
--   level1name: Value associated to the level 1 object.
--   level2type: Type of level 2 object. COLUMN is the only supported value in this version. 
--   level2name: Value associated to the level 2 object.

-- Return:      This procedure returns a message with the result of the execution. If an exception occurs, 
--              the exception is raised.
-- =======================================================================================================

CREATE OR REPLACE PROCEDURE SP_ADDEXTENDEDPROPERTY_UDP(
    name varchar, 
    value varchar, 
    level0type varchar DEFAULT '', 
    level0name varchar DEFAULT '',
    level1type varchar DEFAULT '', 
    level1name varchar DEFAULT '',
    level2type varchar DEFAULT '', 
    level2name varchar DEFAULT '')

RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS 
   DECLARE  stmt VARCHAR;
            str_result VARCHAR;
BEGIN
    IF(lower(name) = 'ms_description') THEN --Comments on
        IF (value IS NOT NULL) THEN
        
            --Comment on table column
            IF(lower(level0type) = 'schema' and lower(level1type) = 'table' and lower(level2type) = 'column') THEN 
                stmt := 'COMMENT ON COLUMN ' || level0name || '.' || level1name || '.' || level2name || ' IS ''' || value || ''';';
    
            --Comment on table/view/procedure/function 
            ELSEIF(lower(level0type) = 'schema' and lower(level1type) in ('table', 'view', 'procedure', 'function') and level2type IS NULL) THEN 
                stmt := 'COMMENT ON ' || upper(level1type) || ' ' || level0name || '.' || level1name || ' IS ''' || value || ''';';
    
            --Comment on schema
            ELSEIF(lower(level0type) = 'schema' and level1type IS NULL) THEN 
                stmt := 'COMMENT ON ' || upper(level0type) || ' ' || level0name || ' IS ''' || value || ''';';

ELSE
                str_result := 'ERROR: COMMENT ON level0type: ' || level0type || ' | level1type: ' || nvl(level1type,'') || ' | level2type: ' || nvl(level2type,'') || ' is not supported yet.';
END IF;
    
            IF(stmt IS NOT NULL) THEN
                EXECUTE IMMEDIATE :stmt;
                str_result := name || ' extended property was successfully created.';
END IF;
ELSE
            str_result := 'ERROR: NULL value for COMMENT ON is not supported.';
END IF;
ELSE
        str_result := 'ERROR: ' || name || ' extended property is not supported yet.';
END IF;
RETURN str_result;
END;
```

Copy

##### SQL Server[¶](#sql-server "Link to this heading")

```
 EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Technical identifier.' , @level0type=N'SCHEMA',@level0name=N'Monitoring', @level1type=N'TABLE',@level1name=N'tProcessingIssue', @level2type=N'COLUMN',@level2name=N'ID'
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CALL SP_ADDEXTENDEDPROPERTY_UDP('MS_Description', 'Technical identifier.', 'SCHEMA', 'Monitoring', 'TABLE', 'tProcessingIssue', 'COLUMN', 'ID');
```

Copy

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

1. [SP\_ADDEXTENDEDPROPERTY\_UDP](#sp-addextendedproperty-udp)