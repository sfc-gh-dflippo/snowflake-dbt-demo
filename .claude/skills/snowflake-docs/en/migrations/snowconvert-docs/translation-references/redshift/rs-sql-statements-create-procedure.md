---
auto_generated: true
description: Creates a new stored procedure or replaces an existing procedure for
  the current database. (Redshift SQL Language Reference Create Procedure).
last_scraped: '2026-01-14T16:53:42.408514+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-create-procedure
title: SnowConvert AI - Redshift - CREATE PROCEDURE | Snowflake Documentation
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
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)

              * [CONTINUE HANDLER](redshift-continue-handler.md)
              * [EXIT HANDLER](redshift-exit-handler.md)
              * [CREATE TABLE](redshift-sql-statements-create-table.md)
              * [CREATE TABLE AS](redshift-sql-statements-create-table-as.md)
              * [CREATE PROCEDURE](rs-sql-statements-create-procedure.md)
              * [SELECT](rs-sql-statements-select.md)
              * [SELECT INTO](rs-sql-statements-select-into.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)CREATE PROCEDURE

# SnowConvert AI - Redshift - CREATE PROCEDURE[¶](#snowconvert-ai-redshift-create-procedure "Link to this heading")

## Description[¶](#description "Link to this heading")

> Creates a new stored procedure or replaces an existing procedure for the current database. ([Redshift SQL Language Reference Create Procedure](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html)).

See the following definitions for more information about procedure clauses:

* [ARGUMENTS MODE](#arguments-mode)
* [POSITIONAL ARGUMENTS](#positional-arguments)
* [NONATOMIC](#nonatomic)
* [PROCEDURE BODY](#procedure-body)
* [SECURITY (DEFINER | INVOKER)](#security-definer-invoker)

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

The following is the SQL syntax to create a Procedure in Amazon Redshift. Click [here](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html) to here to go to Redshifts specification for this syntax.

```
 CREATE [ OR REPLACE ] PROCEDURE sp_procedure_name  
  ( [ [ argname ] [ argmode ] argtype [, ...] ] )
[ NONATOMIC ]
AS $$
  procedure_body
$$ LANGUAGE plpgsql
[ { SECURITY INVOKER | SECURITY DEFINER } ]
[ SET configuration_parameter { TO value | = value } ]
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Input Code:[¶](#input-code "Link to this heading")

#### Redshift[¶](#redshift "Link to this heading")

```
 CREATE PROCEDURE TEST_PROCEDURE()
LANGUAGE PLPGSQL
AS
$$
BEGIN
    NULL;
END;
$$;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE PROCEDURE TEST_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

There are no issues for this transformation.

## ALIAS DECLARATION[¶](#alias-declaration "Link to this heading")

### Description[¶](#id1 "Link to this heading")

If the stored procedure’s signature omits the argument name, you can declare an alias for the argument.

There is no support for this in Snowflake.

To achieve functional equivalence, aliases will be removed, and all usages will be renamed.

When an alias is declared for a parameter nameless, a generated name will be created for the parameter and the usages. When the alias is for a parameter with name the alias will be replaced by the real parameter name.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 name ALIAS FOR $n;
```

Copy

### Sample Source Patterns[¶](#id3 "Link to this heading")

#### Input Code:[¶](#id4 "Link to this heading")

##### Redshift[¶](#id5 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_procedure (integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;
```

Copy

##### Output Code:[¶](#id6 "Link to this heading")

##### Snowflake[¶](#id7 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_procedure (SC_ARG1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:SC_ARG1 + 1);
   INSERT INTO t1
   VALUES (:SC_ARG1 + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "t1" **
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:PARAMETER1 + 1);
   INSERT INTO t1
   VALUES (:PARAMETER1 + 2);
END;
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id8 "Link to this heading")

There are no related EWIs.

## ARGUMENTS MODE[¶](#arguments-mode "Link to this heading")

### Description[¶](#id9 "Link to this heading")

Amazon Redshift stored procedures support parameters that can be passed during procedure invocation. These parameters allow you to provide input values, retrieve output values, or use them for input and output operations. Below is a detailed explanation of the types of parameters, their modes, and examples of their usage. Snowflake only supports input values.

#### IN (Input Parameters)[¶](#in-input-parameters "Link to this heading")

Purpose: Used to pass values into the procedure.

Default Mode: If no mode is specified, parameters are considered IN.

Behavior: Values passed to the procedure cannot be modified inside the procedure.

##### OUT (Output Parameters)[¶](#out-output-parameters "Link to this heading")

Purpose: Used to return values from the procedure.

Behavior: Parameters can be modified inside the procedure and are returned to the caller. You cannot send an initial value.

##### INOUT (Input/Output Parameters)[¶](#inout-input-output-parameters "Link to this heading")

Purpose: Used to pass values into the procedure and modify them to return updated values.

Behavior: Combines the behavior of IN and OUT. You must send an initial value regardless of the output.

### Grammar Syntax[¶](#id10 "Link to this heading")

```
 [ argname ] [ argmode ] argtype
```

Copy

### Sample Source Patterns[¶](#id11 "Link to this heading")

#### Input Code:[¶](#id12 "Link to this heading")

##### Redshift[¶](#id13 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE SP_PARAMS(
IN PARAM1 INTEGER,
OUT PARAM2 INTEGER,
INOUT PARAM3 INTEGER)
AS 
$$
    BEGIN
        NULL;
    END;
$$ 
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id14 "Link to this heading")

##### Snowflake[¶](#id15 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_PARAMS (PARAM1 INTEGER, PARAM2 OUT INTEGER, PARAM3 OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

Copy

### Known Issues[¶](#id16 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id17 "Link to this heading")

1. [SCC-EWI-0028](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0028) : Type not supported by Snowflake.
2. [SSC-EWI-RS0010](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/redshiftEWI.html#ssc-ewi-rs0010): Top-level procedure call with out parameters is not supported.

## PROCEDURE BODY[¶](#procedure-body "Link to this heading")

### Description[¶](#id18 "Link to this heading")

Like Redshift, Snowflake supports CREATE PROCEDURE using $$ procedure\_logic $$ as the body. There is a difference in the Redshift syntax where a word can be inside the $$ like $word$ and used as a delimiter body like $word$ procedure\_logic $word$. SnowConvert AI will transform it by removing the word, leaving the $$.

### Grammar Syntax[¶](#id19 "Link to this heading")

```
 AS
$Alias$
  procedure_body
$Alias$
```

Copy

### Sample Source Patterns[¶](#id20 "Link to this heading")

#### Input Code:[¶](#id21 "Link to this heading")

##### Redshift[¶](#id22 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP()
AS 
$somename$
BEGIN
   NULL;
END;
$somename$ 
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id23 "Link to this heading")

##### Snowflake[¶](#id24 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
   BEGIN
      NULL;
   END;
$$;
```

Copy

### Known Issues[¶](#id25 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id26 "Link to this heading")

There are no related EWIs.

## BLOCK STATEMENT[¶](#block-statement "Link to this heading")

### Description[¶](#id27 "Link to this heading")

PL/pgSQL is a block-structured language. The complete body of a procedure is defined in a block, which contains variable declarations and PL/pgSQL statements. A statement can also be a nested block, or subblock.

### Grammar Syntax[¶](#id28 "Link to this heading")

```
 [ <<label>> ]
[ DECLARE
  declarations ]
BEGIN
  statements
EXCEPTION
  WHEN OTHERS THEN
    statements
END [ label ];
```

Copy

### Sample Source Patterns[¶](#id29 "Link to this heading")

#### Input Code:[¶](#id30 "Link to this heading")

##### Redshift[¶](#id31 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE() 
AS 
$$
    BEGIN
        NULL;
    END;
$$ 
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id32 "Link to this heading")

##### Snowflake[¶](#id33 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

Copy

### Known Issues[¶](#id34 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id35 "Link to this heading")

There are no related EWIs.

## DECLARE[¶](#declare "Link to this heading")

### Description[¶](#id36 "Link to this heading")

Section to declare all the procedure variables except for loop variables.  
Redshift supports multiple DECLARE sections per block statement, since Snowflake does not support this behavior they must be merged into a single declaration statement per block.

### Grammar Syntax[¶](#id37 "Link to this heading")

```
 [ DECLARE declarations ]
```

Copy

### Sample Source Patterns[¶](#id38 "Link to this heading")

#### Input Code:[¶](#id39 "Link to this heading")

##### Redshift[¶](#id40 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
DECLARE
    j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

Copy

##### Output Code:[¶](#id41 "Link to this heading")

##### Snowflake[¶](#id42 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
      j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

Copy

### Known Issues[¶](#id43 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id44 "Link to this heading")

There are no related EWIs.

## EXCEPTION[¶](#exception "Link to this heading")

### Description[¶](#id45 "Link to this heading")

When an exception occurs, and you add an exception-handling block, you can write RAISE statements and most other PL/pgSQL statements. For example, you can raise an exception with a custom message or insert a record into a logging table.

### Grammar Syntax[¶](#id46 "Link to this heading")

```
 EXCEPTION
  WHEN OTHERS THEN
    statements
```

Copy

### Sample Source Patterns[¶](#id47 "Link to this heading")

#### Input Code:[¶](#id48 "Link to this heading")

##### Redshift[¶](#id49 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE update_employee_sp() AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHERS THEN
    RAISE INFO 'An exception occurred.';
END;
$$
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id50 "Link to this heading")

##### Snowflake[¶](#id51 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE update_employee_sp ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHER THEN
        CALL RAISE_MESSAGE_UDF('INFO', 'An exception occurred.');
        RAISE;
END;
$$;
```

Copy

### Known Issues[¶](#id52 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id53 "Link to this heading")

There are no related EWIs.

## LABEL[¶](#label "Link to this heading")

### Description[¶](#id54 "Link to this heading")

Labels are used in Redshift to qualify a block or to use the EXIT or END statement. Snowflake does not support labels.

Warning

Since labels are not supported in Snowflake, an EWI will be printed.

### Grammar Syntax[¶](#id55 "Link to this heading")

```
 [<<label>>]
BEGIN
    ...
END [label]
```

Copy

### Sample Source Patterns[¶](#id56 "Link to this heading")

#### Input Code:[¶](#id57 "Link to this heading")

##### Redshift[¶](#id58 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
LANGUAGE plpgsql
AS
$$
    <<Begin_block_label>>
BEGIN
   INSERT INTO my_test_table
   VALUES (first_parameter);
END;
$$;
```

Copy

##### Output Code:[¶](#id59 "Link to this heading")

##### Snowflake[¶](#id60 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
   !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <<Begin_block_label>> ***/!!!
BEGIN
   INSERT INTO my_test_table
   VALUES (:first_parameter);
END;
$$;
```

Copy

### Known Issues[¶](#id61 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id62 "Link to this heading")

1. [SSC-EWI-0094](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0094): Label declaration not supported

## NONATOMIC[¶](#nonatomic "Link to this heading")

### Description[¶](#id63 "Link to this heading")

The NONATOMIC commits after each statement in the stored procedure. Snowflake supports an AUTOCOMMIT parameter. The default setting for AUTOCOMMIT is TRUE (enabled).

While AUTOCOMMIT is enabled, Each statement outside an explicit transaction is treated as inside its implicit single-statement transaction. In other words, that statement is automatically committed if it succeeds and automatically rolled back if it fails. In other words, Snowflake works as NONATOMIC “by default”.

### Grammar Syntax[¶](#id64 "Link to this heading")

```
 NONATOMIC
```

Copy

### Sample Source Patterns[¶](#id65 "Link to this heading")

#### Input Code:[¶](#id66 "Link to this heading")

##### Redshift[¶](#id67 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC()
NONATOMIC 
AS 
$$
    BEGIN
        NULL;
    END;
$$ 
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id68 "Link to this heading")

##### Snowflake[¶](#id69 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC ()
RETURNS VARCHAR
----** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--NONATOMIC
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

Copy

### Known Issues[¶](#id70 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id71 "Link to this heading")

There are no related EWIs.

## POSITIONAL ARGUMENTS[¶](#positional-arguments "Link to this heading")

### Description[¶](#id72 "Link to this heading")

Redshift supports nameless parameters by referencing the parameters by their position using $. Snowflake does not support this behavior. To ensure functional equivalence, SnowConvert AI can convert those references by the parameter’s name if the name is present in the definition. If not, SnowConvert AI will generate a name for the parameter, and the uses will be replaced with the new name.

### Grammar Syntax[¶](#id73 "Link to this heading")

```
 $n
```

Copy

### Sample Source Patterns[¶](#id74 "Link to this heading")

#### Input Code:[¶](#id75 "Link to this heading")

##### Redshift[¶](#id76 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES(
INTEGER,
param2 INTEGER,
INTEGER)
AS 
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := $2 + $3 + $1;
    END;
$$ 
LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id77 "Link to this heading")

##### Snowflake[¶](#id78 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES (SC_ARG1
INTEGER,
param2 INTEGER, SC_ARG3 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := param2 + SC_ARG3 + SC_ARG1;
    END;
$$;
```

Copy

### Known Issues[¶](#id79 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id80 "Link to this heading")

There are no related EWIs.

## RAISE[¶](#raise "Link to this heading")

### Description[¶](#id81 "Link to this heading")

> Use the `RAISE level` statement to report messages and raise errors.
>
> ([Redshift SQL Language Reference RAISE](https://docs.aws.amazon.com/es_es/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors))

Note

RAISE are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id82 "Link to this heading")

```
 RAISE level 'format' [, variable [, ...]];
```

Copy

In Amazon Redshift, the `RAISE` statement is used to generate messages in the console or throw custom exceptions. Redshift allows you to specify different *levels* to indicate the severity of the message. In Snowflake, this functionality can be emulated using a user-defined function (UDF) that makes a call to the console depending on the specified level.

1. **Exception**:  
   When the level is “EXCEPTION”, a custom exception is raised with a general message: *“To view the EXCEPTION MESSAGE, you need to check the log.”* The exception code is `-20002`, which informs the user that the custom message can be found in the logs. This is due to limitations when sending custom exceptions in Snowflake.
2. **Warning**:  
   If the level is “WARNING”, `SYSTEM$LOG_WARN` is used to print the warning message to Snowflake’s log, which helps highlight potential issues without interrupting the flow of execution.
3. **Info**:  
   For any other level (such as “INFO”), `SYSTEM$LOG_INFO` is used to print the message to the console log, providing more detailed feedback about the system’s state without causing critical disruptions.

This approach allows emulating Redshift’s severity levels functionality, adapting them to Snowflake’s syntax and features, while maintaining flexibility and control over the messages and exceptions generated during execution.

**Limitations**

* To view logs in Snowflake, it is necessary to have specific privileges, such as the `ACCOUNTADMIN` or `SECURITYADMIN` roles.
* Logs in Snowflake are not available immediately and may have a slight delay before the information is visible.
* Personalized error messages in exceptions are not displayed like in Redshift. To view custom messages, you must access the logs directly.

For further information, please refer to the following [page](https://docs.snowflake.com/developer-guide/logging-tracing/logging-snowflake-scripting).

### Sample Source Patterns[¶](#id83 "Link to this heading")

#### Input Code:[¶](#id84 "Link to this heading")

##### Redshift[¶](#id85 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE raise_example(IN user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
	RAISE EXCEPTION 'User % not exists.', user_id;
END;
$$;
```

Copy

##### Output Code:[¶](#id86 "Link to this heading")

##### Snowflake[¶](#id87 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE raise_example (user_id INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS $$
BEGIN
	CALL RAISE_MESSAGE_UDF('EXCEPTION', 'User % not exists.', array_construct(:user_id));
END;
$$;
```

Copy

#### UDFs [¶](#udfs "Link to this heading")

##### RAISE\_MESSAGE\_UDF[¶](#raise-message-udf "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE RAISE_MESSAGE_UDF(LEVEL VARCHAR, MESSAGE VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        MY_EXCEPTION EXCEPTION (-20002, 'To view the EXCEPTION MESSAGE, you need to check the log.');
        SC_RAISE_MESSAGE VARCHAR;
    BEGIN
        SC_RAISE_MESSAGE := STRING_FORMAT_UDF(MESSAGE, ARGS);
        IF (LEVEL = 'EXCEPTION') THEN
            SYSTEM$LOG_ERROR(SC_RAISE_MESSAGE);
            RAISE MY_EXCEPTION;
        ELSEIF (LEVEL = 'WARNING') THEN
            SYSTEM$LOG_WARN(SC_RAISE_MESSAGE);
            RETURN 'Warning printed successfully';
        ELSE
            SYSTEM$LOG_INFO(SC_RAISE_MESSAGE);
            RETURN 'Message printed successfully';
        END IF;
    END;
$$;
```

Copy

##### STRING\_FORMAT\_UDF[¶](#string-format-udf "Link to this heading")

```
 CREATE OR REPLACE FUNCTION PUBLIC.STRING_FORMAT_UDF(PATTERN VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "udf",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS
$$
	var placeholder_str = "{%}";
	var result = PATTERN.replace(/(?<!%)%(?!%)/g, placeholder_str).replace("%%","%");
	for (var i = 0; i < ARGS.length; i++)
	{
		result = result.replace(placeholder_str, ARGS[i]);
	}
	return result;
$$;
```

Copy

### Known Issues[¶](#id88 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id89 "Link to this heading")

There are no related EWIs.

## RETURN[¶](#return "Link to this heading")

### Description[¶](#id90 "Link to this heading")

> The RETURN statement returns back to the caller from a stored procedure. ([Redshift SQL Language Reference Return](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-return)).

The conversion of the return statement from Amazon Redshift to Snowflake is straightforward, only considering adding a `NULL` to the return statement on Snowflake.

### Grammar Syntax[¶](#id91 "Link to this heading")

```
 RETURN;
```

Copy

### Sample Source Patterns[¶](#id92 "Link to this heading")

#### Simple Case[¶](#simple-case "Link to this heading")

##### Input Code:[¶](#id93 "Link to this heading")

##### Redshift[¶](#id94 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id95 "Link to this heading")

##### Redshift[¶](#id96 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/12/2025",  "domain": "test" }}'
AS
$$
BEGIN
  RETURN NULL;
END
$$;
```

Copy

#### When the procedure has out parameters[¶](#when-the-procedure-has-out-parameters "Link to this heading")

SnowConvert AI returns a variant with parameters set up as output parameters. So, for each return, SnowConvert AI will add a variant as a return value.

##### Input Code:[¶](#id97 "Link to this heading")

##### Redshift[¶](#id98 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (OUT output_value VARCHAR)
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id99 "Link to this heading")

##### Redshift[¶](#id100 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (output_value OUT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS
$$
BEGIN
   RETURN NULL;
END
$$;
```

Copy

### Known Issues[¶](#id101 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id102 "Link to this heading")

There are no related EWIs.

## SECURITY (DEFINER | INVOKER)[¶](#security-definer-invoker "Link to this heading")

### Description[¶](#id103 "Link to this heading")

The SECURITY clause in Amazon Redshift stored procedures defines the access control and permissions context under which the procedure executes. This determines whether the procedure uses the privileges of the owner (creator) or the caller (user invoking the procedure).

### Grammar Syntax[¶](#id104 "Link to this heading")

```
 [ { SECURITY INVOKER | SECURITY DEFINER } ]
```

Copy

### Sample Source Patterns[¶](#id105 "Link to this heading")

#### Input Code:[¶](#id106 "Link to this heading")

##### Redshift[¶](#id107 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER( )
AS 
$$
    BEGIN
        NULL;
    END;
$$ 
LANGUAGE plpgsql
SECURITY INVOKER
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER( )
AS 
$$
     BEGIN
        NULL;
    END;
$$ 
LANGUAGE plpgsql
SECURITY DEFINER;
```

Copy

##### Output Code:[¶](#id108 "Link to this heading")

##### Snowflake[¶](#id109 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NULL;
    END;
$$
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS OWNER
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

Copy

### Known Issues[¶](#id110 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id111 "Link to this heading")

There are no related EWIs.

## VARIABLE DECLARATION[¶](#variable-declaration "Link to this heading")

### Description[¶](#id112 "Link to this heading")

> Declare all variables in a block, except for loop variables, in the block’s DECLARE section.
>
> ([Redshift SQL Language Reference Variable Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-structure.html#r_PLpgSQL-variable-declaration))

Note

Variable declarations are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id113 "Link to this heading")

```
 DECLARE
name [ CONSTANT ] type [ NOT NULL ] [ { DEFAULT | := } expression ];
```

Copy

In Redshift, the `CONSTANT` keyword prevents variable reassignment during execution. Since Snowflake does not support this keyword, it is removed during transformation. This does not impact functionality, as the logic should not attempt to reassign a constant variable.

The `NOT NULL` constraint in Redshift ensures a variable cannot be assigned a null value and requires a non-null default value. As Snowflake does not support this constraint, it is removed during transformation. However, the default value is retained to maintain functionality.

A variable declare with a Refcursor is transformed to Resultset type, for more [information](#declare-refcursor).

### Sample Source Patterns[¶](#id114 "Link to this heading")

#### Input Code:[¶](#id115 "Link to this heading")

##### Redshift[¶](#id116 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION()
LANGUAGE plpgsql
AS $$
DECLARE
    v_simple_int INT;	
    v_default_char CHAR(4) DEFAULT 'ABCD';
    v_default_float FLOAT := 10.00;
    v_constant_char CONSTANT CHAR(4) := 'ABCD';
    v_notnull VARCHAR NOT NULL DEFAULT 'Test default';
    v_refcursor REFCURSOR;
BEGIN
-- Procedure logic
END;
$$;
```

Copy

##### Output Code:[¶](#id117 "Link to this heading")

##### Snowflake[¶](#id118 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            v_simple_int INT;
            v_default_char CHAR(4) DEFAULT 'ABCD';
            v_default_float FLOAT := 10.00;
            v_constant_char CHAR(4) := 'ABCD';
            --** SSC-FDM-PG0012 - NOT NULL CONSTRAINT HAS BEEN REMOVED. ASSIGNING NULL TO THIS VARIABLE WILL NO LONGER CAUSE A FAILURE. **
            v_notnull VARCHAR DEFAULT 'Test default';
            v_refcursor RESULTSET;
BEGIN
            NULL;
-- Procedure logic
END;
$$;
```

Copy

### Known Issues [¶](#id119 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id120 "Link to this heading")

1. [SSC-FDM-PG0012](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0012): NOT NULL constraint has been removed. Assigning NULL to this variable will no longer cause a failure.

## TRANSACTIONS[¶](#transactions "Link to this heading")

## COMMIT[¶](#commit "Link to this heading")

### Description[¶](#id121 "Link to this heading")

> Commits the current transaction to the database. This command makes the database updates from the transaction permanent. ([Redshift SQL Language Reference COMMIT](https://docs.aws.amazon.com/redshift/latest/dg/r_COMMIT.html))

Grammar Syntax

```
COMMIT [WORK | TRANSACTION]
```

Copy

### Sample Source Patterns[¶](#id122 "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### Redshift[¶](#id123 "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

##### Snowflake[¶](#id124 "Link to this heading")

##### Query[¶](#id125 "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

#### COMMIT with TRANSACTION keyword[¶](#commit-with-transaction-keyword "Link to this heading")

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on functionality it will just be removed.

##### Redshift[¶](#id126 "Link to this heading")

##### Query[¶](#id127 "Link to this heading")

```
 COMMIT TRANSACTION;
```

Copy

##### Snowflake[¶](#id128 "Link to this heading")

##### Query[¶](#id129 "Link to this heading")

```
 COMMIT;
```

Copy

#### COMMIT in a default transaction behavior procedure (without NONATOMIC clause)[¶](#commit-in-a-default-transaction-behavior-procedure-without-nonatomic-clause "Link to this heading")

In order to avoid out of scope transaction exceptions in Snowflake, the usages of COMMIT will be matched with BEGIN TRANSACTION.

When multiple COMMIT statements are present in the procedure, multiple BEGIN TRANSACTION statements will be generated after every COMMIT to emulate the Redshift transaction behavior.

##### Redshift[¶](#id130 "Link to this heading")

##### Query[¶](#id131 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
    INSERT INTO transaction_values_test VALUES (a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#result "Link to this heading")

```
+------+
| col1 |
+------+
| 120  |
| 121  |
+------+
```

Copy

##### Snowflake[¶](#id132 "Link to this heading")

##### Query[¶](#id133 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

Copy

##### Result[¶](#id134 "Link to this heading")

```
+------+
| col1 |
+------+
| 120  |
| 121  |
+------+
```

Copy

#### COMMIT in a procedure with NONATOMIC behavior[¶](#commit-in-a-procedure-with-nonatomic-behavior "Link to this heading")

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the COMMIT statement inside NONATOMIC procedures is left as is.

##### Redshift[¶](#id135 "Link to this heading")

##### Query[¶](#id136 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#id137 "Link to this heading")

```
+------+
| col1 |
+------+
| 12   |
| 13   |
+------+
```

Copy

##### Snowflake[¶](#id138 "Link to this heading")

##### Query[¶](#id139 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

Copy

##### Result[¶](#id140 "Link to this heading")

```
+------+
| col1 |
+------+
| 12   |
| 13   |
+------+
```

Copy

### Known Issues[¶](#id141 "Link to this heading")

**1. COMMIT inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift[¶](#id142 "Link to this heading")

##### Query[¶](#id143 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

Copy

##### Snowflake[¶](#id144 "Link to this heading")

##### Query[¶](#id145 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

Copy

### Known Issues[¶](#id146 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id147 "Link to this heading")

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.

## ROLLBACK[¶](#rollback "Link to this heading")

### Description[¶](#id148 "Link to this heading")

> Stops the current transaction and discards all updates made by that transaction. ([Redshift SQL Language Reference ROLLBACK](https://docs.aws.amazon.com/redshift/latest/dg/r_ROLLBACK.html))

Grammar Syntax

```
ROLLBACK [WORK | TRANSACTION]
```

Copy

### Sample Source Patterns[¶](#id149 "Link to this heading")

#### Setup data[¶](#id150 "Link to this heading")

##### Redshift[¶](#id151 "Link to this heading")

##### Query[¶](#id152 "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

##### Snowflake[¶](#id153 "Link to this heading")

##### Query[¶](#id154 "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

#### ROLLBACK with TRANSACTION keyword[¶](#rollback-with-transaction-keyword "Link to this heading")

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on functionality it will just be removed.

##### Redshift[¶](#id155 "Link to this heading")

##### Query[¶](#id156 "Link to this heading")

```
 ROLLBACK TRANSACTION;
```

Copy

##### Snowflake[¶](#id157 "Link to this heading")

##### Query[¶](#id158 "Link to this heading")

```
 ROLLBACK;
```

Copy

#### ROLLBACK in a default transaction behavior procedure (without NONATOMIC clause)[¶](#rollback-in-a-default-transaction-behavior-procedure-without-nonatomic-clause "Link to this heading")

In order to avoid out of scope transaction exceptions in Snowflake, the usages of ROLLBACK will be matched with BEGIN TRANSACTION.

When multiple transaction control statements are present in the procedure, multiple BEGIN TRANSACTION statements will be generated after every each one of them to emulate the Redshift transaction behavior.

##### Redshift[¶](#id159 "Link to this heading")

##### Query[¶](#id160 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    COMMIT;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#id161 "Link to this heading")

```
+------+
| col1 |
+------+
| 120  |
+------+
```

Copy

##### Snowflake[¶](#id162 "Link to this heading")

##### Query[¶](#id163 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test values (:a);
    COMMIT;
    BEGIN TRANSACTION;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

Copy

##### Result[¶](#id164 "Link to this heading")

```
+------+
| col1 |
+------+
| 120  |
+------+
```

Copy

#### ROLLBACK in a procedure with NONATOMIC behavior[¶](#rollback-in-a-procedure-with-nonatomic-behavior "Link to this heading")

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the ROLLBACK statement inside NONATOMIC procedures is left as is.

##### Redshift[¶](#id165 "Link to this heading")

##### Query[¶](#id166 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#id167 "Link to this heading")

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

Copy

##### Snowflake[¶](#id168 "Link to this heading")

##### Query[¶](#id169 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

Copy

##### Result[¶](#id170 "Link to this heading")

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

Copy

### Known Issues[¶](#id171 "Link to this heading")

**1. ROLLBACK inside a nested procedure call**

In Redshift, when a ROLLBACK statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift[¶](#id172 "Link to this heading")

##### Query[¶](#id173 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 1);
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CALL transaction_test(a + 3);
    COMMIT;
END
$$;
```

Copy

##### Snowflake[¶](#id174 "Link to this heading")

##### Query[¶](#id175 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    ROLLBACK;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a + 1);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
    COMMIT;
END
$$;
```

Copy

**2. ROLLBACK of DDL statements**

In Snowflake, DDL statements perform an implicit commit whenever they are executed inside a procedure, making effective all the work prior to executing the DDL as well as the DDL itself. This causes the ROLLBACK statement to not be able to discard any changes before that point, this issue will be informed using an FDM.

##### Redshift[¶](#id176 "Link to this heading")

##### Query[¶](#id177 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE rollback_ddl(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );

    INSERT INTO someRollbackTable values (a);
    ROLLBACK;
END
$$;
```

Copy

##### Snowflake[¶](#id178 "Link to this heading")

##### Query[¶](#id179 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE rollback_ddl (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );
    BEGIN TRANSACTION;
    INSERT INTO someRollbackTable
    values (:a);
    --** SSC-FDM-RS0007 - DDL STATEMENTS PERFORM AN AUTOMATIC COMMIT, ROLLBACK WILL NOT WORK AS EXPECTED **
    ROLLBACK;
END
$$;
```

Copy

### Known Issues[¶](#id180 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id181 "Link to this heading")

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.
2. [SSC-FDM-RS0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0007): DDL statements perform an automatic COMMIT, ROLLBACK will not work as expected.

## TRUNCATE[¶](#truncate "Link to this heading")

### Description[¶](#id182 "Link to this heading")

> Deletes all of the rows from a table without doing a table scan ([Redshift SQL Language Reference TRUNCATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNCATE.html))

Grammar Syntax

```
TRUNCATE [TABLE] table_name
```

Copy

### Sample Source Patterns[¶](#id183 "Link to this heading")

#### Setup data[¶](#id184 "Link to this heading")

##### Redshift[¶](#id185 "Link to this heading")

##### Query[¶](#id186 "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

##### Snowflake[¶](#id187 "Link to this heading")

##### Query[¶](#id188 "Link to this heading")

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

Copy

#### TRUNCATE in a default transaction behavior procedure (without NONATOMIC clause)[¶](#truncate-in-a-default-transaction-behavior-procedure-without-nonatomic-clause "Link to this heading")

Since the TRUNCATE statement automatically commits the transaction it is executed in, any of its usages will generate a COMMIT statement in Snowflake to emulate this behavior.

Since a COMMIT statement is generated the same BEGIN TRANSACTION statement generation will be applied to TRUNCATE. For more information check the [COMMIT translation specification](#commit-in-a-default-transaction-behavior-procedure-without-nonatomic-clause).

##### Redshift[¶](#id189 "Link to this heading")

##### Query[¶](#id190 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test VALUES (a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#id191 "Link to this heading")

```
+------+
| col1 |
+------+
| 22   |
+------+
```

Copy

##### Snowflake[¶](#id192 "Link to this heading")

##### Query[¶](#id193 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM
    transaction_values_test;
```

Copy

##### Result[¶](#id194 "Link to this heading")

```
+------+
| col1 |
+------+
| 22   |
+------+
```

Copy

#### TRUNCATE in a procedure with NONATOMIC behavior[¶](#truncate-in-a-procedure-with-nonatomic-behavior "Link to this heading")

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true by SnowConvert AI, the TRUNCATE statement inside NONATOMIC procedures is left as is, there is no need to generate a COMMIT statement because every statement is automatically commited when executed.

##### Redshift[¶](#id195 "Link to this heading")

##### Query[¶](#id196 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

Copy

##### Result[¶](#id197 "Link to this heading")

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

Copy

##### Snowflake[¶](#id198 "Link to this heading")

##### Query[¶](#id199 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

Copy

##### Result[¶](#id200 "Link to this heading")

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

Copy

### Known Issues[¶](#id201 "Link to this heading")

**1. TRUNCATE inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift[¶](#id202 "Link to this heading")

##### Query[¶](#id203 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

Copy

##### Snowflake[¶](#id204 "Link to this heading")

##### Query[¶](#id205 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

Copy

### Known Issues[¶](#id206 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id207 "Link to this heading")

1. [SSC-FDM-RS0006](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/redshiftFDM.html#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.

## CONDITIONS[¶](#conditions "Link to this heading")

## CASE[¶](#case "Link to this heading")

### Description[¶](#id208 "Link to this heading")

> The `CASE` statement in Redshift lets you return values based on conditions, enabling conditional logic in queries. It has two forms: simple and searched. ([Redshift SQL Language Reference Conditionals: Case](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-case)).

### Simple Case[¶](#id209 "Link to this heading")

A simple CASE statement provides conditional execution based on equality of operands.

Note

Simple Case are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id210 "Link to this heading")

```
 CASE search-expression
WHEN expression [, expression [ ... ]] THEN
  statements
[ WHEN expression [, expression [ ... ]] THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

Copy

### Sample Source Patterns[¶](#id211 "Link to this heading")

#### Input Code:[¶](#id212 "Link to this heading")

##### Redshift[¶](#id213 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE proc1(x INT)
LANGUAGE plpgsql
AS $$
BEGIN
  CASE x
WHEN 1, 2 THEN
  NULL;
ELSE
  NULL;
END CASE;                  
END;
$$;
```

Copy

##### Output Code:[¶](#id214 "Link to this heading")

##### Redshift[¶](#id215 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE proc1 (x INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/14/2025",  "domain": "test" }}'
AS $$
BEGIN
  CASE x
    WHEN 1 THEN
      NULL;
    WHEN 2 THEN
      NULL;
   ELSE
     NULL;
  END CASE;
END;
$$;
```

Copy

### Searched Case[¶](#searched-case "Link to this heading")

Note

Searched Case are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id216 "Link to this heading")

```
 CASE
WHEN boolean-expression THEN
  statements
[ WHEN boolean-expression THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

Copy

### Sample Source Patterns[¶](#id217 "Link to this heading")

#### Input Code:[¶](#id218 "Link to this heading")

##### Redshift[¶](#id219 "Link to this heading")

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);	
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  END CASE;  
END;
$$;
```

Copy

##### Output Code:[¶](#id220 "Link to this heading")

##### Redshift[¶](#id221 "Link to this heading")

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      result VARCHAR(100);
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  ELSE
    RAISE case_not_found;
  END CASE;
END;
$$;
```

Copy

#### CASE Without ELSE[¶](#case-without-else "Link to this heading")

In Redshift, when a `CASE` expression is executed and none of the validated conditions are met, and there is no `ELSE` defined, the exception ‘CASE NOT FOUND’ is triggered. In Snowflake, the code executes but returns no result. To maintain the same functionality in Snowflake in this scenario, an exception with the same name will be declared and executed if none of the `CASE` conditions are met.

Note

Case Without Else are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

##### Input Code:[¶](#id222 "Link to this heading")

##### Redshift[¶](#id223 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
AS $$
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  END CASE;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id224 "Link to this heading")

##### Redshift[¶](#id225 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
    DECLARE
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  ELSE
   RAISE case_not_found;
  END CASE;
END;
$$;
```

Copy

### Known Issues[¶](#id226 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id227 "Link to this heading")

There are no related EWIs.

## IF[¶](#if "Link to this heading")

### Description[¶](#id228 "Link to this heading")

> This statement allows you to make decisions based on certain conditions. ([Redshift SQL Language Reference Conditionals: IF](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-if)).

SnowConvert AI will add the parenthesis in the conditions and change the keyword ELSIF by ELSEIF since Redshift does not require the parenthesis in the conditions and ELSIF is the keyword.

### Grammar Syntax[¶](#id229 "Link to this heading")

```
 IF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
    ...] ]
[ ELSE
  statements ]
END IF;
```

Copy

### Sample Source Patterns[¶](#id230 "Link to this heading")

#### Input Code:[¶](#id231 "Link to this heading")

##### Redshift[¶](#id232 "Link to this heading")

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);	
BEGIN
    IF paramNumber = 0 THEN
      result := 'zero';
    ELSIF paramNumber > 0 THEN
      result := 'positive';
    ELSIF paramNumber < 0 THEN
      result := 'negative';
    ELSE
      result := 'NULL';
    END IF;
END;
$$;
```

Copy

##### Output Code:[¶](#id233 "Link to this heading")

##### Redshift[¶](#id234 "Link to this heading")

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            result VARCHAR(100);
BEGIN
            IF (:paramNumber = 0) THEN
                result := 'zero';
            ELSEIF (:paramNumber > 0) THEN
                result := 'positive';
            ELSEIF (:paramNumber < 0) THEN
                result := 'negative';
              ELSE
                result := 'NULL';
            END IF;
END;
$$;
```

Copy

### Known Issues[¶](#id235 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id236 "Link to this heading")

There are no related EWIs.

## LOOPS[¶](#loops "Link to this heading")

### Description[¶](#id237 "Link to this heading")

These statements are used to repeat a block of code until the specified condition. ([Redshift SQL Language Reference Loops](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

[CONTINUE](#continue)
[FOR](#for)
[LOOP](#loop)
[WHILE](#while)
[EXIT](#exit)

## CONTINUE[¶](#continue "Link to this heading")

### Description[¶](#id238 "Link to this heading")

> When the CONTINUE conditions are true, the loop can continue the execution, when is false stop the loop. ([Redshift SQL Language Reference Conditionals: CONTINUE](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

CONTINUE are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id239 "Link to this heading")

```
 CONTINUE [ label ] [ WHEN expression ];
```

Copy

### Sample Source Patterns[¶](#id240 "Link to this heading")

#### Input Code:[¶](#id241 "Link to this heading")

##### Redshift[¶](#id242 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    <<simple_loop_when>>
    LOOP
        i := i + 1;
        CONTINUE WHEN i = 5;
        RAISE INFO 'i %', i;
        EXIT simple_loop_when WHEN (i >= x);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    LOOP
        i := i + 1;
		IF (I = 5) THEN 
        	CONTINUE;
		END IF;
        RAISE INFO 'i %', i;
        EXIT WHEN (i >= x);
    END LOOP;
END;
$$;
```

Copy

##### Results[¶](#results "Link to this heading")

| Console Output |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 6 |
| 7 |

##### Output Code:[¶](#id243 "Link to this heading")

##### Snowflake[¶](#id244 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
        IF (:i = 5) THEN
        	CONTINUE;
        END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT simple_loop_when;
        END IF;
    END LOOP simple_loop_when;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
		IF (:I = 5) THEN
        	CONTINUE;
		END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT;
        END IF;
    END LOOP;
END;
$$;
```

Copy

##### Results[¶](#id245 "Link to this heading")

| Console Output |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 6 |
| 7 |

### Known Issues[¶](#id246 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id247 "Link to this heading")

There are no related EWIs.

## EXIT[¶](#exit "Link to this heading")

### Description[¶](#id248 "Link to this heading")

> Stop the loop execution when the conditions defined in the WHEN statement are true ([Redshift SQL Language Reference Conditionals: EXIT](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

EXIT are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id249 "Link to this heading")

```
 EXIT [ label ] [ WHEN expression ];
```

Copy

### Sample Source Patterns[¶](#id250 "Link to this heading")

#### Input Code:[¶](#id251 "Link to this heading")

##### Redshift[¶](#id252 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop_when(x int)
LANGUAGE plpgsql
AS $$
DECLARE i INTEGER := 0;
BEGIN
  <<simple_loop_when>>
  LOOP
    RAISE INFO 'i %', i;
    i := i + 1;
    EXIT simple_loop_when WHEN (i >= x);
  END LOOP;
END;
$$;
```

Copy

##### Output Code:[¶](#id253 "Link to this heading")

##### Redshift[¶](#id254 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop_when (x int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      i INTEGER := 0;
BEGIN
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
    i := i + 1;
        IF ((:i >= : x)) THEN
          EXIT simple_loop_when;
        END IF;
  END LOOP simple_loop_when;
END;
$$;
```

Copy

### Known Issues[¶](#id255 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id256 "Link to this heading")

There are no related EWIs.

## FOR[¶](#for "Link to this heading")

### Grammar Syntax[¶](#id257 "Link to this heading")

Integer variant

```
 [<<label>>]
FOR name IN [ REVERSE ] expression .. expression LOOP
  statements
END LOOP [ label ];
```

Copy

### Sample Source Patterns[¶](#id258 "Link to this heading")

#### Input Code:[¶](#id259 "Link to this heading")

##### Redshift[¶](#id260 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS $$
BEGIN
  FOR i IN 1..10 LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10..1 LOOP
    NULL;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

Copy

##### Output Code:[¶](#id261 "Link to this heading")

##### Redshift[¶](#id262 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  FOR i IN 1 TO 10
                   --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10 TO 1
                           --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                           LOOP
    NULL;
  END LOOP;
END;
$$;
```

Copy

### Known Issues[¶](#id263 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id264 "Link to this heading")

1. [SSC-EWI-PG0006](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI.html#ssc-ewi-pg0006): Reference a variable using the Label is not supported by Snowflake.

## LOOP[¶](#loop "Link to this heading")

### Description[¶](#id265 "Link to this heading")

> A simple loop defines an unconditional loop that is repeated indefinitely until terminated by an EXIT or RETURN statement. ([Redshift SQL Language Reference Conditionals: Simple Loop](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

Simple Loop are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id266 "Link to this heading")

```
 [<<label>>]
LOOP
  statements
END LOOP [ label ];
```

Copy

### Sample Source Patterns[¶](#id267 "Link to this heading")

#### Input Code:[¶](#id268 "Link to this heading")

##### Redshift[¶](#id269 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop()
LANGUAGE plpgsql
AS $$
BEGIN
  <<simple_while>>
  LOOP
    RAISE INFO 'I am raised once';  
    EXIT simple_while;
    RAISE INFO 'I am not raised';
  END LOOP;
  RAISE INFO 'I am raised once as well';
END;
$$;
```

Copy

##### Output Code:[¶](#id270 "Link to this heading")

##### Redshift[¶](#id271 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
    CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once');
    EXIT simple_while;
    CALL RAISE_MESSAGE_UDF('INFO', 'I am not raised');
  END LOOP simple_while;
  CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once as well');
END;
$$;
```

Copy

### Known Issues[¶](#id272 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id273 "Link to this heading")

There are no related EWIs.

## WHILE[¶](#while "Link to this heading")

### Grammar Syntax[¶](#id274 "Link to this heading")

```
 [<<label>>]
WHILE expression LOOP
  statements
END LOOP [ label ];
```

Copy

### Sample Source Patterns[¶](#id275 "Link to this heading")

#### Input Code:[¶](#id276 "Link to this heading")

##### Redshift[¶](#id277 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop_when()
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE I > 5 AND I > 10 LOOP
        NULL;
    END LOOP;   
END;
$$;
```

Copy

##### Output Code:[¶](#id278 "Link to this heading")

##### Redshift[¶](#id279 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_loop_when ()
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
            DECLARE
                i INTEGER := 0;
BEGIN
                WHILE (:I > 5 AND : I > 10)
                                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                            LOOP
        NULL;
    END LOOP;
END;
$$;
```

Copy

### Known Issues[¶](#id280 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id281 "Link to this heading")

There are no related EWIs.

## CURSORS[¶](#cursors "Link to this heading")

## CLOSE CURSOR[¶](#close-cursor "Link to this heading")

### Description[¶](#id282 "Link to this heading")

> Closes all of the free resources that are associated with an open cursor.. ([Redshift SQL Language Reference Close Cursor](https://docs.aws.amazon.com/redshift/latest/dg/close.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id283 "Link to this heading")

```
 CLOSE cursor
```

Copy

### Sample Source Patterns[¶](#id284 "Link to this heading")

#### Input Code:[¶](#id285 "Link to this heading")

##### Redshift[¶](#id286 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

Copy

##### Output Code:[¶](#id287 "Link to this heading")

##### Redshift[¶](#id288 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

Copy

### Known Issues[¶](#id289 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id290 "Link to this heading")

There are no related EWIs.

## FETCH CURSOR[¶](#fetch-cursor "Link to this heading")

### Description[¶](#id291 "Link to this heading")

> Retrieves rows using a cursor. ([Redshift SQL Language reference Fetch](https://docs.aws.amazon.com/redshift/latest/dg/fetch.html))

Transformation information

```
 FETCH [ NEXT | ALL | {FORWARD [ count | ALL ] } ] FROM cursor

FETCH cursor INTO target [, target ...];
```

Copy

### Sample Source Patterns[¶](#id292 "Link to this heading")

#### Setup data[¶](#id293 "Link to this heading")

##### Redshift[¶](#id294 "Link to this heading")

##### Query[¶](#id295 "Link to this heading")

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

Copy

##### Snowflake[¶](#id296 "Link to this heading")

##### Query[¶](#id297 "Link to this heading")

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

Copy

#### Fetch into[¶](#fetch-into "Link to this heading")

The FETCH into statement from Redshift is fully equivalent in Snowflake

##### Redshift[¶](#id298 "Link to this heading")

##### Query[¶](#id299 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_into_example()
LANGUAGE plpgsql
AS $$
DECLARE my_cursor CURSOR FOR
        SELECT col1, col2
        FROM cursor_example;
        some_id INT;
        message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example VALUES (some_id * 10, message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM cursor_example;
```

Copy

##### Result[¶](#id300 "Link to this heading")

```
+------+-------------+
| col1 | col2        |
+------+-------------+
| 10   | hello       |
| 100  | hello world!|
+------+-------------+
```

Copy

##### Snowflake[¶](#id301 "Link to this heading")

##### Query[¶](#id302 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_into_example ()
RETURNS VARCHAR
LANGUAGE SQL
AS $$
DECLARE
    my_cursor CURSOR FOR
    SELECT col1, col2
    FROM
    cursor_example;
    some_id INT;
    message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example
			VALUES (:some_id * 10, :message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM
	cursor_example;
```

Copy

##### Result[¶](#id303 "Link to this heading")

```
+------+-------------+
| col1 | col2        |
+------+-------------+
| 10   | hello       |
| 100  | hello world!|
+------+-------------+
```

Copy

### Known Issues[¶](#id304 "Link to this heading")

**1. Fetch without target variables is not supported**

Snowflake requires the FETCH statement to specify the INTO clause with the variables where the fetched row values are going to be stored. When a FETCH statement is found in the code with no INTO clause an EWI will be generated.

Input Code:

```
 FETCH FORWARD FROM cursor1;
```

Copy

Output Code:

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0015 - FETCH CURSOR WITHOUT TARGET VARIABLES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FETCH FORWARD FROM cursor1;
```

Copy

### Known Issues[¶](#id305 "Link to this heading")

There are no known issues.

### Related EWIs[¶](#id306 "Link to this heading")

1. [SSC-EWI-PG0015](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/postgresqlEWI.html#ssc-ewi-pg0015): Fetch cursor without target variables is not supported in Snowflake

## OPEN CURSOR[¶](#open-cursor "Link to this heading")

### Description[¶](#id307 "Link to this heading")

> Before you can use a cursor to retrieve rows, it must be opened. ([Redshift SQL Language Reference Open Cursor](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id308 "Link to this heading")

```
 OPEN bound_cursor_name [ ( argument_values ) ];
```

Copy

### Sample Source Patterns[¶](#id309 "Link to this heading")

#### Setup data[¶](#id310 "Link to this heading")

##### Redshift[¶](#id311 "Link to this heading")

##### Query[¶](#id312 "Link to this heading")

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

Copy

##### Snowflake[¶](#id313 "Link to this heading")

##### Query[¶](#id314 "Link to this heading")

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

Copy

#### Open cursor without arguments[¶](#open-cursor-without-arguments "Link to this heading")

##### Input Code:[¶](#id315 "Link to this heading")

##### Redshift[¶](#id316 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

Copy

##### Output Code:[¶](#id317 "Link to this heading")

##### Redshift[¶](#id318 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

Copy

#### Open cursor with arguments[¶](#open-cursor-with-arguments "Link to this heading")

Cursor arguments have to be binded per each one of its uses, SnowConvert AI will generate the bindings, was well as reorder and repeat the passed values to the OPEN statement as needed to satisfy the bindings.

##### Redshift[¶](#id319 "Link to this heading")

##### Query[¶](#id320 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_open_test()
LANGUAGE plpgsql
AS $$
DECLARE
    cursor2 CURSOR (val1 VARCHAR(20), val2 INTEGER) FOR SELECT col1 + val2, col2 FROM cursor_example where val1 = col2 and val2 > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2('hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test();

SELECT * FROM cursor_example_results;
```

Copy

##### Result[¶](#id321 "Link to this heading")

```
+------+-------+
| col1 | col2  |
+------+-------+
| 60   | hello |
+------+-------+
```

Copy

##### Snowflake[¶](#id322 "Link to this heading")

##### Query[¶](#id323 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_open_test ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (50, 'hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test();
SELECT * FROM
cursor_example_results;
```

Copy

##### Result[¶](#id324 "Link to this heading")

```
+------+-------+
| col1 | col2  |
+------+-------+
| 60   | hello |
+------+-------+
```

Copy

#### Open cursor with procedure parameters or local variables[¶](#open-cursor-with-procedure-parameters-or-local-variables "Link to this heading")

The procedure parameters or local variables have to be binded per each one of its uses in the cursor query, SnowConvert AI will generate the bindings and add the parameter or variable names to the OPEN statement, even if the cursor originally had no parameters.

##### Redshift[¶](#id325 "Link to this heading")

##### Query[¶](#id326 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_open_test(someValue iNTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    charVariable VARCHAR(20) DEFAULT 'hello';
    cursor2 CURSOR FOR SELECT col1 + someValue, col2 FROM cursor_example where charVariable = col2 and someValue > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2;
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test(30);
```

Copy

##### Result[¶](#id327 "Link to this heading")

```
+------+-------+
| col1 | col2  |
+------+-------+
| 40   | hello |
+------+-------+
```

Copy

##### Snowflake[¶](#id328 "Link to this heading")

##### Query[¶](#id329 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_open_test (someValue iNTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            charVariable VARCHAR(20) DEFAULT 'hello';
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (someValue, charVariable, someValue);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test(30);
```

Copy

##### Result[¶](#id330 "Link to this heading")

```
+------+-------+
| col1 | col2  |
+------+-------+
| 40   | hello |
+------+-------+
```

Copy

### Known Issues[¶](#id331 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id332 "Link to this heading")

There are no related EWIs.

## DECLARE CURSOR[¶](#declare-cursor "Link to this heading")

### Description[¶](#id333 "Link to this heading")

> Defines a new cursor. Use a cursor to retrieve a few rows at a time from the result set of a larger query. ([Redshift SQL Language Reference Declare Cursor](https://docs.aws.amazon.com/redshift/latest/dg/declare.html)).

Note

This syntax is fully supported in Snowflake.

### Grammar Syntax[¶](#id334 "Link to this heading")

```
 name CURSOR [ ( arguments ) ] FOR query
```

Copy

### Sample Source Patterns[¶](#id335 "Link to this heading")

#### Input Code:[¶](#id336 "Link to this heading")

### Input Code:[¶](#id337 "Link to this heading")

#### Redshift[¶](#id338 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
DECLARE
   -- Declare the cursor
   cursor1 CURSOR FOR SELECT 1;
   cursor2 CURSOR (key integer) FOR SELECT 2 where 1 = key;
   
BEGIN
END;
$$;
```

Copy

##### Output Code:[¶](#id339 "Link to this heading")

##### Redshift[¶](#id340 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
      DECLARE
         -- Declare the cursor
         cursor1 CURSOR FOR SELECT 1;
         cursor2 CURSOR FOR SELECT 2 where 1 = ?;
BEGIN
         NULL;
END;
$$;
```

Copy

### Known Issues[¶](#id341 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id342 "Link to this heading")

There are no related EWIs.

## DECLARE REFCURSOR[¶](#declare-refcursor "Link to this heading")

### Description[¶](#id343 "Link to this heading")

> A `refcursor` data type simply holds a reference to a cursor. You can create a cursor variable by declaring it as a variable of type `refcursor`
>
> ([Redshift SQL Language Reference Refcursor Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors))

Note

Refcursor declarations are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id344 "Link to this heading")

```
 DECLARE
name refcursor;
```

Copy

Since Snowflake does not support the `REFCURSOR` data type, its functionality is replicated by converting the `REFCURSOR` variable into a `RESULTSET` type. The query used to open the `REFCURSOR` is assigned to the `RESULTSET` variable, after which a new cursor is created and linked to the `RESULTSET` variable. Additionally, all references to the original `REFCURSOR` within the cursor logic are updated to use the new cursor, thereby replicating the original functionality.

### Sample Source Patterns[¶](#id345 "Link to this heading")

#### Case: Single use[¶](#case-single-use "Link to this heading")

##### Input Code:[¶](#id346 "Link to this heading")

##### Redshift[¶](#id347 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

Copy

##### Output Code:[¶](#id348 "Link to this heading")

##### Snowflake[¶](#id349 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
 END;
$$;
```

Copy

##### Case: Cursor with Dynamic Sql [¶](#case-cursor-with-dynamic-sql "Link to this heading")

##### Input Code:[¶](#id350 "Link to this heading")

##### Redshift[¶](#id351 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;

    OPEN cur FOR EXECUTE qry;
-- Cursor logic
    CLOSE cur;
END;
$$;


CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
BEGIN
    OPEN cur FOR EXECUTE 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
-- Cursor logic
    CLOSE cur;
END;
$$;
```

Copy

##### Output Code:[¶](#id352 "Link to this heading")

##### Redshift[¶](#id353 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
            cur := (
                EXECUTE IMMEDIATE qry
            );
            LET cur_Resultset_1 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_1;
-- Cursor logic
    CLOSE cur_Resultset_1;
END;
$$;


CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2 (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
BEGIN
            cur := (
                EXECUTE IMMEDIATE 'SELECT id, name FROM employees WHERE salary > ' || min_salary
            );
            LET cur_Resultset_2 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_2;
-- Cursor logic
    CLOSE cur_Resultset_2;
END;
$$;
```

Copy

##### Case: Multiple uses: [¶](#case-multiple-uses "Link to this heading")

##### Input Code:[¶](#id354 "Link to this heading")

##### Redshift[¶](#id355 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
  OPEN v_curs1 FOR SELECT column3_name, column4_name FROM your_table2;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

Copy

##### Output Code:[¶](#id356 "Link to this heading")

##### Snowflake[¶](#id357 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
   v_curs1 := (
    SELECT column3_name, column4_name FROM your_table2
   );
   LET v_curs1_Resultset_2 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_2;
-- Cursor logic
  CLOSE v_curs1_Resultset_2;
 END;
$$;
```

Copy

### Known Issues[¶](#id358 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id359 "Link to this heading")

There are no related EWIs.

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
2. [Grammar Syntax](#grammar-syntax)
3. [Sample Source Patterns](#sample-source-patterns)
4. [Related EWIs](#related-ewis)
5. [ALIAS DECLARATION](#alias-declaration)
6. [ARGUMENTS MODE](#arguments-mode)
7. [PROCEDURE BODY](#procedure-body)
8. [BLOCK STATEMENT](#block-statement)
9. [DECLARE](#declare)
10. [EXCEPTION](#exception)
11. [LABEL](#label)
12. [NONATOMIC](#nonatomic)
13. [POSITIONAL ARGUMENTS](#positional-arguments)
14. [RAISE](#raise)
15. [RETURN](#return)
16. [SECURITY (DEFINER | INVOKER)](#security-definer-invoker)
17. [VARIABLE DECLARATION](#variable-declaration)
18. [TRANSACTIONS](#transactions)
19. [COMMIT](#commit)
20. [ROLLBACK](#rollback)
21. [TRUNCATE](#truncate)
22. [CONDITIONS](#conditions)
23. [CASE](#case)
24. [IF](#if)
25. [LOOPS](#loops)
26. [CONTINUE](#continue)
27. [EXIT](#exit)
28. [FOR](#for)
29. [LOOP](#loop)
30. [WHILE](#while)
31. [CURSORS](#cursors)
32. [CLOSE CURSOR](#close-cursor)
33. [FETCH CURSOR](#fetch-cursor)
34. [OPEN CURSOR](#open-cursor)
35. [DECLARE CURSOR](#declare-cursor)
36. [DECLARE REFCURSOR](#declare-refcursor)