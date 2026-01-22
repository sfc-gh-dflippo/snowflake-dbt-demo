---
auto_generated: true
description: Oracle Create Function to Snowflake Snow Scripting
last_scraped: '2026-01-14T16:53:24.042142+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/create-function
title: SnowConvert AI - Oracle - CREATE FUNCTION | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)[PL/SQL to Snowflake Scripting](README.md)CREATE FUNCTION

# SnowConvert AI - Oracle - CREATE FUNCTION[¶](#snowconvert-ai-oracle-create-function "Link to this heading")

Oracle Create Function to Snowflake Snow Scripting

## Description[¶](#description "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

> A **stored function** (also called a **user function** or **user-defined function**) is a set of PL/SQL statements you can call by name. Stored functions are very similar to procedures, except that a function returns a value to the environment in which it is called. User functions can be used as part of a SQL expression.
>
> A **call specification** declares a Java method or a third-generation language (3GL) routine so that it can be called from PL/SQL. You can also use the `CALL` SQL statement to call such a method or routine. The call specification tells Oracle Database which Java method, or which named function in which shared library, to invoke when a call is made. It also tells the database what type conversions to make for the arguments and return value. [Oracle SQL Language Reference Create Function](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-FUNCTION.html).

### Oracle Syntax[¶](#oracle-syntax "Link to this heading")

For more information regarding Oracle Create Function, check [here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-FUNCTION-statement.html).

#### Oracle Create Function Syntax[¶](#oracle-create-function-syntax "Link to this heading")

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONABLE ]
FUNCTION
[ schema. ] function_name
  [ ( parameter_declaration [, parameter_declaration]... ) ] RETURN datatype 
[ sharing_clause ]
  [ { invoker_rights_clause
    | accessible_by_clause
    | default_collation_clause    
    | deterministic_clause
    | parallel_enable_clause
    | result_cache_clause 
    | aggregate_clause
    | pipelined_clause
    | sql_macro_clause
       }...
  ]
{ IS | AS } { [ declare_section ] 
    BEGIN statement ...
    [ EXCEPTION exception_handler [ exception_handler ]... ]
    END [ name ] ;
      |
    { java_declaration | c_declaration } } ;
```

Copy

### Snowflake Syntax[¶](#snowflake-syntax "Link to this heading")

Snowflake allows 3 different languages in their user-defined functions:

* SQL
* JavaScript
* Java

For now, SnowConvert AI will support only `SQL` and `JavaScript` as target languages.

For more information regarding Snowflake Create Function, check [here](https://docs.snowflake.com/en/developer-guide/udf/udf-overview).

#### SQL[¶](#sql "Link to this heading")

Note

SQL user-defined functions only support one query as their body. They can read from the database but are not allowed to write to or modify it ([Scalar SQL UDFs](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-scalar-functions.html)).

```
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

Copy

##### JavaScript[¶](#javascript "Link to this heading")

Note

JavaScript user-defined functions allow multiple statements in their bodies but cannot perform queries to the database. ([Scalar JavaScript UDFs](https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-scalar-functions)).

```
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Sample auxiliary data[¶](#sample-auxiliary-data "Link to this heading")

Note

This code was executed for a better understanding of the examples:

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE TABLE table1 (col1 int, col2 int, col3 varchar2(250), col4 varchar2(250), col5 date);

INSERT INTO table1 VALUES (1, 11, 'val1_1', 'val1_2', TO_DATE('2004/05/03', 'yyyy-MM-dd'));
INSERT INTO table1 VALUES (2, 22, 'val2_1', 'val2_2', TO_DATE('2014/05/03', 'yyyy-MM-dd'));
INSERT INTO table1 VALUES (3, 33, 'val3_1', 'val3_2', TO_DATE('2024/05/03', 'yyyy-MM-dd'));
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (col1 int,
col2 int,
col3 VARCHAR(250),
col4 VARCHAR(250),
col5 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/25/2024" }}'
;

INSERT INTO table1
VALUES (1, 11, 'val1_1', 'val1_2', TO_DATE('2004/05/03', 'yyyy-MM-dd'));

INSERT INTO table1
VALUES (2, 22, 'val2_1', 'val2_2', TO_DATE('2014/05/03', 'yyyy-MM-dd'));

INSERT INTO table1
VALUES (3, 33, 'val3_1', 'val3_2', TO_DATE('2024/05/03', 'yyyy-MM-dd'));
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

## Related EWIS[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior

## Cursor for a return variable[¶](#cursor-for-a-return-variable "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

This pattern defines a function in Oracle PL/SQL that uses a cursor to fetch a single value and return it.

**Components:**

1. **Function Declaration:**

   * `CREATE FUNCTION functionName(parameters) RETURN returnType`
   * Declares the function with input parameters and the return type.
2. **Variable Declarations:**

   * Declares variables, including the return variable.
3. **Cursor Declaration:**

   * `CURSOR cursorName IS SELECT singleColumn FROM ... WHERE ... [AND col1 = localVar1];`
   * Defines a cursor to select a single column from a table with optional filtering conditions.
4. **BEGIN-END Block:**

   * Variables assignment.
   * Opens the cursor.
   * Fetch the result into the return variable.
   * Closes the cursor.
   * Returns the fetched value.

In this case, the variables are transformed into a common table expression (CTE). As well as the query within the cursor to which, in addition, the `FETCH FIRST 1 ROW ONLY` clause is added to simulate the `FETCH CURSOR` behavior.

`RETURN` statement is transformed to the final select.

### Queries[¶](#queries "Link to this heading")

#### Oracle[¶](#id1 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func1 (
   company_ IN VARCHAR2,
   book_id_ IN DATE,
   object_id_ IN VARCHAR2 ) RETURN INTEGER
IS
   temp_ table1.col2%TYPE;
   CURSOR get_attr IS
      SELECT col2
      FROM table1
      WHERE col3 = company_
      AND   col4 = object_id_
      AND   col5 = book_id_;
BEGIN
   OPEN get_attr;
   FETCH get_attr INTO temp_;
   CLOSE get_attr;
   RETURN temp_;
END func1;
```

Copy

##### Snowflake[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func1 (company_ VARCHAR, book_id_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/, object_id_ VARCHAR)
RETURNS INTEGER
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         (
         SELECT col2
         FROM table1
         WHERE col3 = company_
         AND   col4 = object_id_
         AND   col5 = book_id_
         FETCH FIRST 1 ROW ONLY) AS temp_
   )
   SELECT
      temp_
   FROM
      declaration_variables_cte1
$$;
```

Copy

##### Result[¶](#result "Link to this heading")

| FUNC1() |
| --- |
| 2004-05-03. |

##### Oracle[¶](#id3 "Link to this heading")

```
CREATE FUNCTION func2 (
   fa_period_   IN NUMBER,
   to_date_     IN DATE DEFAULT NULL,
   from_date_   IN DATE DEFAULT NULL ) RETURN NUMBER
IS
   value_                    NUMBER;
   cond_date_to_             DATE;
   cond_date_from_           DATE;
   CURSOR get_acq_value IS
      SELECT NVL(SUM(col1),0)
      FROM   table1
      WHERE  col3                   IN (DECODE(fa_period_, 1, 'val1_1', 'val2_1'))
      AND    col5           <= cond_date_to_
      AND    col5           >= cond_date_from_;
BEGIN
   value_ := 0;
   cond_date_to_       := Get_Cond_Date( to_date_, 'MAX' );
   cond_date_from_     := Get_Cond_Date( from_date_, 'MIN' );
   OPEN get_acq_value;
   FETCH get_acq_value INTO value_;
   CLOSE get_acq_value;
   RETURN (NVL(value_,0));
END func2;
```

Copy

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func2 (fa_period_ NUMBER(38, 18),
  to_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT NULL,
  from_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT NULL )
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         0 AS
         value_,
         Get_Cond_Date( to_date_, 'MAX' ) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Get_Cond_Date' NODE ***/!!! AS
         cond_date_to_,
         Get_Cond_Date( from_date_, 'MIN' ) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Get_Cond_Date' NODE ***/!!! AS
         cond_date_from_
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         (
         SELECT NVL(SUM(col1),0)
         FROM   table1
         WHERE  col3                   IN (DECODE(fa_period_, 1, 'val1_1', 'val2_1'))
         AND    col5           <= cond_date_to_
         AND    col5           >= cond_date_from_
         FETCH FIRST 1 ROW ONLY) AS value_,
         cond_date_to_,
         cond_date_from_
      FROM
         declaration_variables_cte1
   )
   SELECT
      (NVL(value_,0))
   FROM
      declaration_variables_cte2
$$;
```

Copy

##### Result[¶](#id5 "Link to this heading")

| FUNC1() |
| --- |
| 2004-05-03. |

### Known Issues[¶](#id6 "Link to this heading")

No issues were found.

### Related EWIS[¶](#id7 "Link to this heading")

1. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.
2. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Cursor with IF statement[¶](#cursor-with-if-statement "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

This pattern defines a function that conditionally uses a cursor to fetch and return a value based on an `IF` statement.

**Components:**

1. **Function Declaration:**

   * `CREATE FUNCTION functionName(parameters) RETURN returnType`
   * Declares the function with input parameters and the return type.
2. **Cursor Declaration:**

   * `CURSOR cursorName IS SELECT singleColumn FROM ... WHERE ... [AND col1 = localVar1];`
   * Defines a cursor to select a single column from a table with optional filtering conditions.
3. **Variable Declaration:**

   * Declares variables, including the return variable.
4. **BEGIN-END Block with IF Statement:**

   * Variables assignment.
   * Check if a condition is true.
   * If true, opens the cursor, fetches the result into the return variable, closes the cursor, and returns the fetched value. (The cursor can also be opened in the `ELSE` block and must meet the same conditions)
   * The `ELSE` Block is optional, if it exists, it should only contain a single statement that can be an assignment or a `RETURN` statement.

The variables are transformed into a common table expression (CTE). As well as the query within the cursor to which, in addition, the `FETCH FIRST 1 ROW ONLY` clause is added to simulate the `FETCH CURSOR` behavior.

`IF/ELSE` statement can be handled using the [`CASE EXPRESSION`](https://docs.snowflake.com/en/sql-reference/functions/case) inside the select allowing conditionals inside the queries. `RETURN` statement is transformed to the final select..

### Queries[¶](#id8 "Link to this heading")

#### Oracle[¶](#id9 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func1 (
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 12;
BEGIN
   IF 1 = 1 THEN
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
      RETURN max_period_;
   ELSE
      RETURN NULL;
   END IF;
END func1;
```

Copy

##### Snowflake[¶](#id10 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func1 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         12 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN 1 = 1
               THEN (
               SELECT max(col2)
               FROM   table1
               FETCH FIRST 1 ROW ONLY)
            ELSE NULL
         END AS max_period_
      FROM
         declaration_variables_cte0
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte1
$$;
```

Copy

##### Result[¶](#id11 "Link to this heading")

| FUNC2(0) |
| --- |
| NULL |

| FUNC2(1) |
| --- |
| 33 |

##### Oracle[¶](#id12 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func2(
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 1;
BEGIN
   max_period_:= 2;
   IF company_ = 1 THEN
      RETURN max_period_ * 2;
   ELSE
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
      RETURN max_period_;
   END IF;
END func2;
```

Copy

##### Snowflake[¶](#id13 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func2 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         1 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         2 AS
         max_period_
      FROM
         declaration_variables_cte0
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         CASE
            WHEN company_ = 1
               THEN max_period_ * 2
            ELSE (
            SELECT max(col2)
            FROM   table1
            FETCH FIRST 1 ROW ONLY)
         END AS max_period_
      FROM
         declaration_variables_cte1
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte2
$$;
```

Copy

##### Result[¶](#id14 "Link to this heading")

| FUNC2(0) |
| --- |
| 33 |

| FUNC2(1) |
| --- |
| 2 |

##### Oracle[¶](#id15 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func3 (
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 0;
BEGIN
   IF company_ = 1 THEN
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
   END IF;
   RETURN max_period_;
END func10;
```

Copy

##### Snowflake[¶](#id16 "Link to this heading")

```
CREATE OR REPLACE FUNCTION func3 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         0 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN company_ = 1
               THEN (
               SELECT max(col2)
               FROM   table1
               FETCH FIRST 1 ROW ONLY)
            ELSE max_period_
         END AS max_period_
      FROM
         declaration_variables_cte0
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte1
$$;
```

Copy

##### Result[¶](#id17 "Link to this heading")

| FUNC2(0) |
| --- |
| 0 |

| FUNC2(1) |
| --- |
| 33 |

### Known Issues[¶](#id18 "Link to this heading")

No issues were found.

### Related EWIS[¶](#id19 "Link to this heading")

No EWIs related.

## Multiples IFs statement[¶](#multiples-ifs-statement "Link to this heading")

This pattern defines a function that uses conditional statements over local variables.

**Components:**

1. **Function Declaration:**

   * `CREATE FUNCTION functionName(parameters) RETURN returnType`
   * Declares the function with input parameters and the return type.
2. **Variable Declaration:**

   * Declares variables, including the return variable.
3. **BEGIN-END Block with IF Statement:**

   * Check if a condition is true.
   * Each case is used to assign a value over the same variable.

### Conversion:[¶](#conversion "Link to this heading")

**`DECLARE SECTION`** : variables with default an expression are moved to a common table expression.

**`IF/ELSE`** statement can be handled using the [`CASE EXPRESSION`](https://docs.snowflake.com/en/sql-reference/functions/case) inside the select allowing conditionals inside the queries.

**`RETURN`** statement is transformed to the final select.

#### Oracle[¶](#id20 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case1 (
   in_date_ IN DATE,
   min_max_ IN VARCHAR2 )
RETURN DATE
IS
   cond_date_  DATE := CURRENT_DATE;
BEGIN
   IF ( in_date_ IS NULL ) THEN
      IF ( min_max_ = 'MIN' ) THEN
         cond_date_ := FOO1();
      ELSE
         cond_date_ := FOO2();
      END IF;
   ELSE
      cond_date_ := TRUNC(in_date_);
   END IF;
   RETURN cond_date_;
END Case1;
```

Copy

#### Snowflake[¶](#id21 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case1 (in_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/, min_max_ VARCHAR)
RETURNS TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         CURRENT_DATE AS
         cond_date_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN ( in_date_ IS NULL )
               THEN CASE
                  WHEN ( min_max_ = 'MIN' )
                     THEN FOO1() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!!
                  ELSE FOO2() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!!
               END
            ELSE TRUNC(in_date_, 'DD')
         END AS cond_date_
      FROM
         declaration_variables_cte0
   )
   SELECT
      cond_date_
   FROM
      declaration_variables_cte1
$$;
```

Copy

#### Oracle[¶](#id22 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case2 (
   year_        IN NUMBER,
   id           IN NUMBER) 
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   RETURN fully_depritiated_;
END Case2;
```

Copy

#### Snowflake[¶](#id23 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case2 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte1
$$;
```

Copy

#### Oracle[¶](#id24 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case2_1 (
   year_        IN NUMBER,
   id           IN NUMBER) 
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING';
   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING2';
   RETURN fully_depritiated_;
END Case2;
```

Copy

#### Snowflake[¶](#id25 "Link to this heading")

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "FOO1", "FOO2", "FOO3" **
CREATE OR REPLACE FUNCTION Case2_1 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_,
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING' AS

         fully_depritiated
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING2' AS
         fully_depritiated,
         base_value_,
         acc_depr_,
         acc_depr_prev_,
         residual_value_
      FROM
         declaration_variables_cte1
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte2
$$;
```

Copy

#### Oracle[¶](#id26 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case2_1 (
   year_        IN NUMBER,
   id           IN NUMBER) 
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING';
   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING2';
   RETURN fully_depritiated_;
END Case2;
```

Copy

#### Snowflake[¶](#id27 "Link to this heading")

```
CREATE OR REPLACE FUNCTION Case2_1 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_,
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING' AS

         fully_depritiated
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING2' AS
         fully_depritiated,
         base_value_,
         acc_depr_,
         acc_depr_prev_,
         residual_value_
      FROM
         declaration_variables_cte1
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte2
$$;
```

Copy

### Known Issues[¶](#id28 "Link to this heading")

No issues were found.

### Related EWIS[¶](#id29 "Link to this heading")

1. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.
2. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
3. [SSC-EWI-OR0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0036): Types resolution issues, the arithmetic operation may not behave correctly between string and date.

## Snowflake Script UDF (SCALAR)[¶](#snowflake-script-udf-scalar "Link to this heading")

Translation reference for Oracle User Defined Functions to [Snowflake Scripting UDFs](../../../../../developer-guide/udf/sql/udf-sql-procedural-functions)

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id30 "Link to this heading")

SnowConvert now supports translating Oracle PL/SQL User Defined Functions directly to **Snowflake Scripting UDFs** (SnowScript UDFs) when they meet specific criteria.

**Snowflake Scripting UDFs** are user-defined functions written using Snowflake’s procedural language syntax (Snowscript) within a SQL UDF body. They support variables, loops, conditional logic, and exception handling without requiring database access.

#### When Functions Become SnowScript UDFs[¶](#when-functions-become-snowscript-udfs "Link to this heading")

SnowConvert analyzes each Oracle function and automatically determines the appropriate Snowflake target. A function becomes a SnowScript UDF when it contains **only** procedural logic without data access operations.

### Sample Source Patterns[¶](#id31 "Link to this heading")

#### Simple Calculation Function[¶](#simple-calculation-function "Link to this heading")

A basic function that performs calculations without querying data.

##### Oracle[¶](#id32 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculateTax (
    amount_ IN NUMBER,
    tax_rate_ IN NUMBER
) RETURN NUMBER
IS
    tax_amount_ NUMBER;
BEGIN
    tax_amount_ := amount_ * (tax_rate_ / 100);
    RETURN tax_amount_;
END CalculateTax;
```

Copy

##### Result[¶](#id33 "Link to this heading")

| CALCULATETAX(1000, 15) |
| --- |
| 150 |

##### Snowflake (SnowScript UDF)[¶](#snowflake-snowscript-udf "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculateTax (amount_ NUMBER(38, 18), tax_rate_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      tax_amount_ NUMBER(38, 18);
   BEGIN
      tax_amount_ := :amount_ * (:tax_rate_ / 100);
      RETURN :tax_amount_;
   END;
$$;
```

Copy

##### Result[¶](#id34 "Link to this heading")

| CALCULATETAX(1000, 15) |
| --- |
| 150 |

#### Function with IF/ELSIF/ELSE Logic[¶](#function-with-if-elsif-else-logic "Link to this heading")

Functions using conditional statements for business logic.

##### Oracle[¶](#id35 "Link to this heading")

```
CREATE OR REPLACE FUNCTION GetShippingCost (
    distance_ IN NUMBER,
    weight_ IN NUMBER
) RETURN NUMBER
IS
    shipping_cost_ NUMBER := 0;
BEGIN
    IF distance_ < 50 THEN
        shipping_cost_ := 10;
    ELSIF distance_ < 100 THEN
        shipping_cost_ := 20;
    ELSIF distance_ < 200 THEN
        shipping_cost_ := 35;
    ELSE
        shipping_cost_ := 50;
    END IF;
    
    IF weight_ > 20 THEN
        shipping_cost_ := shipping_cost_ * 1.5;
    END IF;
    
    RETURN shipping_cost_;
END GetShippingCost;
```

Copy

##### Result[¶](#id36 "Link to this heading")

| GETSHIPPINGCOST(75, 25) |
| --- |
| 30 |

##### Snowflake (SnowScript UDF)[¶](#id37 "Link to this heading")

```
CREATE OR REPLACE FUNCTION GetShippingCost (distance_ NUMBER(38, 18), weight_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      shipping_cost_ NUMBER(38, 18) := 0;
   BEGIN
      IF (:distance_ < 50) THEN
         shipping_cost_ := 10;
      ELSEIF (:distance_ < 100) THEN
         shipping_cost_ := 20;
      ELSEIF (:distance_ < 200) THEN
         shipping_cost_ := 35;
    ELSE
         shipping_cost_ := 50;
      END IF;
      IF (:weight_ > 20) THEN
         shipping_cost_ := :shipping_cost_ * 1.5;
      END IF;
      RETURN :shipping_cost_;
   END;
$$;
```

Copy

##### Result[¶](#id38 "Link to this heading")

| GETSHIPPINGCOST(75, 25) |
| --- |
| 30 |

#### Function with FOR Loop[¶](#function-with-for-loop "Link to this heading")

Functions using loops for iterative calculations.

##### Oracle[¶](#id39 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculateCompoundInterest (
    principal_ IN NUMBER,
    rate_ IN NUMBER,
    years_ IN NUMBER
) RETURN NUMBER
IS
    amount_ NUMBER;
    i NUMBER;
BEGIN
    amount_ := principal_;
    
    FOR i IN 1..years_ LOOP
        amount_ := amount_ * (1 + rate_ / 100);
    END LOOP;
    
    RETURN ROUND(amount_, 2);
END CalculateCompoundInterest;
```

Copy

##### Result[¶](#id40 "Link to this heading")

| CALCULATECOMPOUNDINTEREST(1000, 5, 3) |
| --- |
| 1157.63 |

##### Snowflake (SnowScript UDF)[¶](#id41 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculateCompoundInterest (principal_ NUMBER(38, 18), rate_ NUMBER(38, 18), years_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      amount_ NUMBER(38, 18);
      i NUMBER(38, 18);
   BEGIN
      amount_ := :principal_;
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
      FOR i IN 1 TO :years_
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
         amount_ := :amount_ * (
                                !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Number AND unknown ***/!!!1 + :rate_ / 100);
                               END LOOP;
      RETURN ROUND(:amount_, 2);
   END;
$$;
```

Copy

##### Result[¶](#id42 "Link to this heading")

| CALCULATECOMPOUNDINTEREST(1000, 5, 3) |
| --- |
| 1157.63 |

#### CASE and DECODE Logic[¶](#case-and-decode-logic "Link to this heading")

Functions using CASE expressions and DECODE for categorization.

##### Oracle[¶](#id43 "Link to this heading")

```
CREATE OR REPLACE FUNCTION GetCustomerTier (
    annual_spend_ IN NUMBER,
    years_active_ IN NUMBER
) RETURN VARCHAR2
IS
    tier_ VARCHAR2(20);
    base_tier_ VARCHAR2(20);
BEGIN
    -- Determine base tier by spending
    base_tier_ := CASE
        WHEN annual_spend_ >= 10000 THEN 'PLATINUM'
        WHEN annual_spend_ >= 5000 THEN 'GOLD'
        WHEN annual_spend_ >= 2000 THEN 'SILVER'
        ELSE 'BRONZE'
    END;
    
    -- Upgrade tier if customer is loyal (5+ years)
    IF years_active_ >= 5 THEN
        tier_ := DECODE(base_tier_,
            'GOLD', 'PLATINUM',
            'SILVER', 'GOLD',
            'BRONZE', 'SILVER',
            base_tier_);
    ELSE
        tier_ := base_tier_;
    END IF;
    
    RETURN tier_;
END GetCustomerTier;
```

Copy

##### Result[¶](#id44 "Link to this heading")

| GETCUSTOMERTIER(3000, 6) |
| --- |
| GOLD |

##### Snowflake (SnowScript UDF)[¶](#id45 "Link to this heading")

```
CREATE OR REPLACE FUNCTION GetCustomerTier (annual_spend_ NUMBER(38, 18), years_active_ NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      tier_ VARCHAR(20);
      base_tier_ VARCHAR(20);
   BEGIN
      -- Determine base tier by spending
      base_tier_ := CASE
                WHEN :annual_spend_ >= 10000 THEN 'PLATINUM'
                WHEN :annual_spend_ >= 5000 THEN 'GOLD'
                WHEN :annual_spend_ >= 2000 THEN 'SILVER'
                ELSE 'BRONZE'
            END;
      -- Upgrade tier if customer is loyal (5+ years)
      IF (:years_active_ >= 5) THEN
                tier_ := DECODE(:base_tier_,
                           'GOLD', 'PLATINUM',
                           'SILVER', 'GOLD',
                           'BRONZE', 'SILVER', :base_tier_);
      ELSE
                tier_ := :base_tier_;
      END IF;
      RETURN :tier_;
   END;
$$;
```

Copy

##### Result[¶](#id46 "Link to this heading")

| GETCUSTOMERTIER(3000, 6) |
| --- |
| GOLD |

#### Select Into variable assingment[¶](#select-into-variable-assingment "Link to this heading")

Functions using simple select into for variable assignment.

##### Oracle[¶](#id47 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice NUMBER,
    p_Quantity NUMBER
)
RETURN NUMBER
IS
    v_Discount NUMBER;
    v_Subtotal NUMBER;
    v_FinalPrice NUMBER;
BEGIN

    SELECT CASE 
               WHEN p_Quantity >= 10 THEN 0.15
               WHEN p_Quantity >= 5 THEN 0.10
               ELSE 0.05
           END,
           p_BasePrice * p_Quantity
    INTO v_Discount, v_Subtotal
    FROM DUAL;
    
    v_FinalPrice := v_Subtotal * (1 - v_Discount);
    
    RETURN v_FinalPrice;
END;
```

Copy

##### Result[¶](#id48 "Link to this heading")

| CALCULATEPRICE(100, 3) |
| --- |
| 285 |

##### Snowflake (SnowScript UDF)[¶](#id49 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(p_BasePrice NUMBER(38, 18), p_Quantity NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "DsGaAXVMinypPa0FTZmrKQ==" }}'
AS
$$
    DECLARE
        v_Discount NUMBER(38, 18);
        v_Subtotal NUMBER(38, 18);
        v_FinalPrice NUMBER(38, 18);
    BEGIN
        v_Discount := CASE
                          WHEN :p_Quantity >= 10 THEN 0.15
                          WHEN :p_Quantity >= 5 THEN 0.10
                          ELSE 0.05
                      END;
        v_Subtotal := :p_BasePrice * :p_Quantity;
        v_FinalPrice := :v_Subtotal * (1 - :v_Discount);
        RETURN :v_FinalPrice;
    END;
$$;
```

Copy

##### Result[¶](#id50 "Link to this heading")

| CALCULATEPRICE(100, 3) |
| --- |
| 285 |

### Known Issues[¶](#id51 "Link to this heading")

Warning

**SnowConvert AI will not translate UDFs containing the following elements into SnowScripting UDFs, as these features are unsupported in SnowScripting UDFs:**

* Access database tables
* Use cursors
* Call other UDFs
* Contain aggregate or window functions
* Perform DML operations (INSERT/UPDATE/DELETE)
* Return result sets

### Related EWIs[¶](#id52 "Link to this heading")

1. [SSC-EWI-0067](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0067): UDF was transformed to Snowflake procedure, calling procedures inside a query is not supported.
2. [SSC-EWI-0068](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0068): User defined function was transformed to a Snowflake procedure.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
4. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.

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

1. [Description](#description)
2. [Sample Source Patterns](#sample-source-patterns)
3. [Known Issues](#known-issues)
4. [Related EWIS](#related-ewis)
5. [Cursor for a return variable](#cursor-for-a-return-variable)
6. [Cursor with IF statement](#cursor-with-if-statement)
7. [Multiples IFs statement](#multiples-ifs-statement)
8. [Snowflake Script UDF (SCALAR)](#snowflake-script-udf-scalar)