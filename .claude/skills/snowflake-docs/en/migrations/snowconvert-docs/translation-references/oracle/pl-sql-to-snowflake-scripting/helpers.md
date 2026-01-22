---
auto_generated: true
description: In this section you will find helper functions or procedures that are
  used to achieve functional equivalence of some Oracle features that are not supported
  natively in Snowflake Scripting.
last_scraped: '2026-01-14T16:53:25.569226+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/helpers
title: SnowConvert AI - Oracle - HELPERS | Snowflake Documentation
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

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../../teradata/README.md)
          + [Oracle](../README.md)

            - [Sample Data](../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../basic-elements-of-oracle-sql/literals.md)
              - [Data Types](../basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](../functions/README.md)
            - [Built-in Packages](../built-in-packages.md)
            - [SQL Queries and Subqueries](../sql-queries-and-subqueries/selects.md)
            - [SQL Statements](../sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](README.md)

              * [CREATE PROCEDURE](create-procedure.md)
              * [CREATE FUNCTION](create-function.md)
              * [COLLECTIONS AND RECORDS](collections-and-records.md)
              * [CURSOR](cursor.md)
              * [DML STATEMENTS](dml-statements.md)
              * [HELPERS](helpers.md)
              * [PACKAGES](packages.md)
            - [PL/SQL to Javascript](../pl-sql-to-javascript/README.md)
            - [SQL Plus](../sql-plus.md)
            - [Wrapped Objects](../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../etl-bi-repointing/power-bi-oracle-repointing.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)[PL/SQL to Snowflake Scripting](README.md)HELPERS

# SnowConvert AI - Oracle - HELPERS[¶](#snowconvert-ai-oracle-helpers "Link to this heading")

In this section you will find helper functions or procedures that are used to achieve functional equivalence of some Oracle features that are not supported natively in Snowflake Scripting.

## Bulk Cursor Helpers[¶](#bulk-cursor-helpers "Link to this heading")

Note

You might also be interested in [Default FORALL transformation](README.html#forall).

The Cursor is simulated with an `OBJECT` with different information regarding the state of the cursor. A temporary table is created to store the result set of the cursor’s query.

Most of these Procedures return a new Object with the updated state of the cursor.

### INIT\_CURSOR[¶](#init-cursor "Link to this heading")

This function initializes a new object with the basic cursor information

```
CREATE OR REPLACE FUNCTION INIT_CURSOR(NAME VARCHAR, QUERY VARCHAR)
RETURNS OBJECT
AS
$$
  SELECT OBJECT_CONSTRUCT('NAME', NAME, 'ROWCOUNT', -1, 'QUERY', QUERY, 'ISOPEN', FALSE, 'FOUND', NULL, 'NOTFOUND', NULL)
$$;
```

Copy

### OPEN\_BULK\_CURSOR[¶](#open-bulk-cursor "Link to this heading")

These procedures creates a temporary table with the query of the cursor. An optional overload exists to support bindings.

```
CREATE OR REPLACE PROCEDURE OPEN_BULK_CURSOR(CURSOR OBJECT, BINDINGS ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var query = `CREATE OR REPLACE TEMPORARY TABLE ${CURSOR.NAME}_TEMP_TABLE AS ${CURSOR.QUERY}`;
  snowflake.execute({ sqlText: query, binds: BINDINGS });
  CURSOR.ROWCOUNT = 0;
  CURSOR.ISOPEN = true;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE OPEN_BULK_CURSOR(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL OPEN_BULK_CURSOR(:CURSOR, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

### CLOSE\_BULK\_CURSOR[¶](#close-bulk-cursor "Link to this heading")

This procedure deletes the temporary table that stored the result set of the cursor and resets the cursor’s properties to their initial state.

```
CREATE OR REPLACE PROCEDURE CLOSE_BULK_CURSOR(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var query = `DROP TABLE ${CURSOR.NAME}_TEMP_TABLE`;
  snowflake.execute({ sqlText: query });
  CURSOR.ROWCOUNT = -1;
  CURSOR.ISOPEN = false;
  CURSOR.FOUND = null;
  CURSOR.NOTFOUND = null;
  return CURSOR;
$$;
```

Copy

### FETCH Helpers[¶](#fetch-helpers "Link to this heading")

Due to Oracle being capable of doing the `FETCH` statement on different kind of scenarios, a multiple procedures with overloads were created to handle each case. These helpers save the fetched values into the `RESULT` property in the `CURSOR` object.

Some of the overloads include variations when the `LIMIT` clause was used or not. Other overloads have a `COLUMN_NAMES` argument that is necessary when the `FETCH` statement is being done into a variable that has or contains a records with column names that are different to the column names of the query.

#### FETCH\_BULK\_COLLECTION\_RECORDS[¶](#fetch-bulk-collection-records "Link to this heading")

These procedures are used when a `FETCH BULK` is done into a collection of records.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var objectConstructArgs = [];
  if (COLUMN_NAMES) {
    for (let i = 0 ; i < COLUMN_NAMES.length ; i++) {
      objectConstructArgs.push("'" + COLUMN_NAMES[i] + "'");
      objectConstructArgs.push('$' + (i + 1));
    }
  } else {
    objectConstructArgs.push('*');
  }
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT ARRAY_AGG(OBJECT_CONSTRUCT(${objectConstructArgs.join(', ')})) FROM (SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT})`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  resultSet.next();
  CURSOR.RESULT = resultSet.getColumnValue(1);
  CURSOR.ROWCOUNT += CURSOR.RESULT.length;
  CURSOR.FOUND = CURSOR.RESULT.length > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, NULL, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, LIMIT INTEGER)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, :LIMIT, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, NULL, :COLUMN_NAMES));
    RETURN :RESULT;
  END;
$$;
```

Copy

#### FETCH\_BULK\_COLLECTIONS[¶](#fetch-bulk-collections "Link to this heading")

These procedures are used when the `FETCH` statement is done into one or multiple collections. Since the columns are specified in this `FETCH` operation, an override for specific `COLUMN_NAMES` is not necessary.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTIONS(CURSOR OBJECT, LIMIT FLOAT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var limitClause = '';
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT}`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  var column_count = stmt.getColumnCount();
  CURSOR.RESULT = [];
  for (let i = 0 ; i < column_count ; i++) {
    CURSOR.RESULT[i] = [];
  }

  while (resultSet.next()) {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      CURSOR.RESULT[i - 1].push(resultSet.getColumnValue(columnName));
    }
  }
  CURSOR.ROWCOUNT += stmt.getRowCount();
  CURSOR.FOUND = stmt.getRowCount() > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTIONS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTIONS(:CURSOR, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

#### FETCH\_BULK\_RECORD\_COLLECTIONS[¶](#fetch-bulk-record-collections "Link to this heading")

These procedures are used when a `FETCH BULK` is done into a record of collections.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT}`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  var column_count = stmt.getColumnCount();
  CURSOR.RESULT = {};
  if (COLUMN_NAMES)
  {
    for (let i = 0 ; i < COLUMN_NAMES.length ; i++) {
      CURSOR.RESULT[COLUMN_NAMES[i]] = [];
    }
  } else {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      CURSOR.RESULT[columnName] = [];
    }
  }
  
  while (resultSet.next()) {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      let fieldName = COLUMN_NAMES ? COLUMN_NAMES[i - 1] : columnName;
      CURSOR.RESULT[fieldName].push(resultSet.getColumnValue(columnName));
    }
  }
  CURSOR.ROWCOUNT += stmt.getRowCount();
  CURSOR.FOUND = stmt.getRowCount() > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, NULL, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, LIMIT INTEGER)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, :LIMIT, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, NULL, :COLUMN_NAMES));
    RETURN :RESULT;
  END;
$$;
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

1. [Bulk Cursor Helpers](#bulk-cursor-helpers)