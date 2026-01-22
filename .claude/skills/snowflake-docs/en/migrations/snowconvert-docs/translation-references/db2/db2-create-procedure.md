---
auto_generated: true
description: Creates a new stored procedure or replaces an existing procedure for
  the current database. (IBM DB2 SQL Language Reference Create Procedure).
last_scraped: '2026-01-14T16:53:06.384678+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-procedure
title: SnowConvert AI - IBM DB2 - CREATE PROCEDURE | Snowflake Documentation
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
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](README.md)

            - [CONTINUE HANDLER](db2-continue-handler.md)
            - [EXIT HANDLER](db2-exit-handler.md)
            - [CREATE TABLE](db2-create-table.md)
            - [CREATE VIEW](db2-create-view.md)
            - [CREATE PROCEDURE](db2-create-procedure.md)
            - [CREATE FUNCTION](db2-create-function.md)
            - [Data Types](db2-data-types.md)
            - [SELECT](db2-select-statement.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)CREATE PROCEDURE

# SnowConvert AI - IBM DB2 - CREATE PROCEDURE[¶](#snowconvert-ai-ibm-db2-create-procedure "Link to this heading")

## Description[¶](#description "Link to this heading")

> Creates a new stored procedure or replaces an existing procedure for the current database. ([IBM DB2 SQL Language Reference Create Procedure](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-procedure-sql)).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

The following is a SQL syntax for creating a procedure in IBM Db2. See the full specification [here](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-procedure-sql).

```
CREATE [ OR REPLACE ] PROCEDURE procedure_name
  ( [ parameter { , parameter }* ] )
LANGUAGE SQL
BEGIN
  statements
END;

parameter := [ IN | OUT | INOUT ] param_name data_type [ DEFAULT expression ]
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Input Code:[¶](#input-code "Link to this heading")

#### Db2[¶](#db2 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE TEST_PROCEDURE ()
LANGUAGE SQL
BEGIN
    VALUES CURRENT_TIMESTAMP;
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE PROCEDURE TEST_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   BEGIN
      SELECT
         CURRENT_TIMESTAMP      ;
   END
$$;
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

There are no issues for this transformation.

## DECLARE[¶](#declare "Link to this heading")

### Description[¶](#id1 "Link to this heading")

Section to declare all the procedure variables except for loop variables.  
Db2 supports multiple DECLARE sections per block statement, since Snowflake does not support this behavior they must be merged into a single declaration statement per block.

### Grammar Syntax[¶](#id2 "Link to this heading")

```
 [ DECLARE declarations ]
```

Copy

### Sample Source Patterns[¶](#id3 "Link to this heading")

#### Input Code:[¶](#id4 "Link to this heading")

##### Db2[¶](#id5 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE first_procedure (first_parameter INTEGER)
LANGUAGE SQL
BEGIN
   DECLARE i INTEGER DEFAULT first_parameter;
   SELECT i;
END;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter INTEGER)
LANGUAGE SQL
BEGIN
   DECLARE i INTEGER DEFAULT first_parameter;
   DECLARE j INTEGER DEFAULT first_parameter;
   SELECT i;
END;
```

Copy

##### Output Code:[¶](#id6 "Link to this heading")

##### Snowflake[¶](#id7 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE first_procedure (first_parameter INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      i INTEGER DEFAULT first_parameter;
   BEGIN
      SELECT
         :i;
   END
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      i INTEGER DEFAULT first_parameter;
      j INTEGER DEFAULT first_parameter;
   BEGIN
      SELECT
         :i;
   END
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id8 "Link to this heading")

There are no related EWIs.

## EXCEPTION[¶](#exception "Link to this heading")

### Description[¶](#id9 "Link to this heading")

Db2 handles exceptions with handlers declared in the block. A handler can be `CONTINUE` (execution continues) or `EXIT` (leaves the block) and can catch general or specific conditions (for example, `SQLEXCEPTION`, `SQLSTATE 'state'`, `SQLCODE code`).

### Grammar Syntax[¶](#id10 "Link to this heading")

```
DECLARE { CONTINUE | EXIT } HANDLER FOR condition
  statements;

condition := SQLEXCEPTION | SQLSTATE 'state' | SQLCODE code
```

Copy

### Sample Source Patterns[¶](#id11 "Link to this heading")

#### Input Code:[¶](#id12 "Link to this heading")

##### Db2[¶](#id13 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE update_employee_sp ()
LANGUAGE SQL
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_log(ts, msg) VALUES (CURRENT_TIMESTAMP, 'An exception occurred');

    SELECT var;
END;
```

Copy

##### Output Code:[¶](#id14 "Link to this heading")

##### Snowflake[¶](#id15 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE update_employee_sp ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
BEGIN

    SELECT var;
      EXCEPTION
         WHEN OTHER CONTINUE THEN
            INSERT INTO error_log (ts, msg) VALUES (CURRENT_TIMESTAMP, 'An exception occurred')
END
$$;
```

Copy

### Known Issues[¶](#id16 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id17 "Link to this heading")

There are no related EWIs.

## LABEL[¶](#label "Link to this heading")

### Description[¶](#id18 "Link to this heading")

Labels are used in Db2 to qualify a block or to use the EXIT or END statement. Snowflake does not support labels. However, a workaround is used for accessing outer-block-declared variables which can be accessed by the fully quealified name, such as `outer_block.variable_name`

Warning

Since labels are not supported in Snowflake, an EWI will be printed.

### Grammar Syntax[¶](#id19 "Link to this heading")

```
 label : BEGIN
    statements
 END label;
```

Copy

### Sample Source Patterns[¶](#id20 "Link to this heading")

#### Input Code:[¶](#id21 "Link to this heading")

##### Db2[¶](#id22 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE P_DEMO_SCOPE()
BEGIN
outer_block:
BEGIN
    DECLARE v_scope_test VARCHAR(50) DEFAULT 'I am from the OUTER block';
    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);
    inner_block:
    BEGIN
    DECLARE v_scope_test VARCHAR(50) DEFAULT 'I am from the INNER block';      
    SET outer_block.v_scope_test = 'The INNER block changed me!';
    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);
    
    END inner_block;

    INSERT INTO TABLETEST(VALUE, TIME) VALUES(v_scope_test, CURRENT_TIMESTAMP);

    
    
END outer_block;
END;
```

Copy

##### Output Code:[¶](#id23 "Link to this heading")

##### Snowflake[¶](#id24 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE P_DEMO_SCOPE ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "vjqaAbThwXqZ0mSDaENBCw==" }}'
AS
$$
    BEGIN
        DECLARE
            outer_block_v_scope_test VARCHAR(50) DEFAULT 'I am from the OUTER block';
        BEGIN
            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:outer_block_v_scope_test, CURRENT_TIMESTAMP);
            DECLARE
                v_scope_test VARCHAR(50) DEFAULT 'I am from the INNER block';
            BEGIN
                outer_block_v_scope_test := 'The INNER block changed me!';
            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:v_scope_test, CURRENT_TIMESTAMP);
            END;

            INSERT INTO TABLETEST (VALUE, TIME) VALUES(:outer_block_v_scope_test, CURRENT_TIMESTAMP);
        END;
    END
$$;
```

Copy

### Known Issues[¶](#id25 "Link to this heading")

1. If a variable name is the same as a modified one, it will cause inconsistencies.

### Related EWIs[¶](#id26 "Link to this heading")

There are no related EWIs.

## VARIABLE DECLARATION[¶](#variable-declaration "Link to this heading")

### Description[¶](#id27 "Link to this heading")

Declare variables inside the block’s `DECLARE` area. Variables can specify an initial value using `DEFAULT`. Subsequent assignments use the `SET` statement.

Note

Variable declarations are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax[¶](#id28 "Link to this heading")

```
DECLARE
  name type [ DEFAULT expression ];
```

Copy

Notes:

* Use `SET name = expression;` to assign after declaration.

### Sample Source Patterns[¶](#id29 "Link to this heading")

#### Input Code:[¶](#id30 "Link to this heading")

##### Db2[¶](#id31 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
LANGUAGE SQL
BEGIN
    DECLARE v_simple_int INTEGER;
    DECLARE v_default_char CHAR(4) DEFAULT 'ABCD';
    DECLARE v_default_decimal DECIMAL(10,2) DEFAULT 10.00;
    DECLARE v_text VARCHAR(50) DEFAULT 'Test default';
    VALUES v_simple_int, v_default_char, v_default_decimal, v_text;
END;
```

Copy

##### Output Code:[¶](#id32 "Link to this heading")

##### Snowflake[¶](#id33 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      v_simple_int INTEGER;
      v_default_char CHAR(4) DEFAULT 'ABCD';
      v_default_decimal DECIMAL(10,2) DEFAULT 10.00;
      v_text VARCHAR(50) DEFAULT 'Test default';
   BEGIN
      SELECT
         v_simple_int, v_default_char, v_default_decimal, v_text      ;
   END
$$;
```

Copy

### Known Issues [¶](#id34 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id35 "Link to this heading")

There are no related EWIs.

## SET[¶](#set "Link to this heading")

### Description[¶](#id36 "Link to this heading")

Assign a value to a variable within a procedure block.

### Grammar Syntax[¶](#id37 "Link to this heading")

```
SET variable_name = expression;
```

Copy

### Sample Source Patterns[¶](#id38 "Link to this heading")

#### Input Code:[¶](#id39 "Link to this heading")

##### Db2[¶](#id40 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_SET ()
LANGUAGE SQL
BEGIN
    DECLARE v_total INTEGER DEFAULT 0;
    SET v_total = v_total + 10;
END;
```

Copy

##### Output Code:[¶](#id41 "Link to this heading")

##### Snowflake[¶](#id42 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_SET ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
   DECLARE
      v_total INTEGER DEFAULT 0;
   BEGIN
      v_total := v_total + 10;
   END
$$;
```

Copy

## IF[¶](#if "Link to this heading")

### Description[¶](#id43 "Link to this heading")

Evaluate conditions and execute different branches. Db2 supports `ELSEIF` and an optional `ELSE` branch.

### Grammar Syntax[¶](#id44 "Link to this heading")

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

### Sample Source Patterns[¶](#id45 "Link to this heading")

#### Input Code:[¶](#id46 "Link to this heading")

##### Db2[¶](#id47 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (paramNumber INTEGER)
LANGUAGE SQL
BEGIN
    DECLARE result VARCHAR(100);
    IF paramNumber = 0 THEN
      SET result = 'zero';
    ELSEIF paramNumber > 0 THEN
      SET result = 'positive';
    ELSEIF paramNumber < 0 THEN
      SET result = 'negative';
    ELSE
      SET result = 'NULL';
    END IF;
END;
```

Copy

##### Output Code:[¶](#id48 "Link to this heading")

##### Db2[¶](#id49 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (paramNumber INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "tDqaAcdlYXqyx5yxM208hw==" }}'
AS
$$
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
   END
$$;
```

Copy

### Known Issues[¶](#id50 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id51 "Link to this heading")

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
5. [DECLARE](#declare)
6. [EXCEPTION](#exception)
7. [LABEL](#label)
8. [VARIABLE DECLARATION](#variable-declaration)
9. [SET](#set)
10. [IF](#if)