---
auto_generated: true
description: Creates a new user defined function or replaces an existing function
  for the current database. (IBM DB2 SQL Language Reference Create Function).
last_scraped: '2026-01-14T16:53:06.124135+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-function
title: SnowConvert AI - IBM DB2 - CREATE FUNCTION | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)CREATE FUNCTION

# SnowConvert AI - IBM DB2 - CREATE FUNCTION[¶](#snowconvert-ai-ibm-db2-create-function "Link to this heading")

## Description[¶](#description "Link to this heading")

> Creates a new user defined function or replaces an existing function for the current database. ([IBM DB2 SQL Language Reference Create Function](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-function-sql-scalar-table-row)).

DB2 User Defined Functions (UDFs) allow developers to extend the built-in functionality of the database by creating custom functions that can be invoked in SQL statements. DB2 supports several types of SQL UDFs:

* **Scalar Functions**: Return a single value and can be used wherever an SQL expression is valid.
* **Table Functions**: Return a table result set and can be used in the FROM clause of SELECT statements.

**SnowConvert AI Translation Support**: SnowConvert AI supports translation of **Inline UDFs**, **SQL Scalar Functions**, and **SQL Table Functions** with the following migration approaches:

* **Inline Functions**: Will be kept as **Inline Functions** in Snowflake.
* **Non-inline UDFs**: If they are Snowflake Scripting compliant, they will be transformed into [**Snowflake Scripting UDFs**](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-procedural-functions)
* **Complex UDFs**: Any UDFs that don’t fit the above two categories will be migrated to **Stored Procedures** instead.

In cases where UDFs are converted to procedures, an **EWI** message will be added to inform the user why the UDF could not be directly migrated to a Snowflake UDF and was converted to a procedure instead.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

The following is the SQL syntax to create a user defined function in IBM DB2. Click [here](https://www.ibm.com/docs/en/db2/12.1.0?topic=statements-create-function-sql-scalar-table-row#r0003493__title__4) to go to the DB2 specification for this syntax.

```
CREATE [ OR REPLACE ] FUNCTION function_name
  [ ( [ { IN | OUT | INOUT } ] parameter_name data_type [ DEFAULT default_clause ]... ) ]
  RETURNS { data_type 
          | ROW ( column_name data_type [, column_name data_type ]... )
          | TABLE ( column_name data_type [, column_name data_type ]... )
          | row_type_name
          | anchored_row_data_type
          | ELEMENT OF array_type_name }
  [ LANGUAGE SQL ]
  [ PARAMETER CCSID { ASCII | UNICODE } ]
  [ SPECIFIC specific_name ]
  [ { DETERMINISTIC | NOT DETERMINISTIC } ]
  [ { EXTERNAL ACTION | NO EXTERNAL ACTION } ]
  [ { READS SQL DATA | CONTAINS SQL | MODIFIES SQL DATA } ]
  [ { ALLOW PARALLEL | DISALLOW PARALLEL } ]
  [ STATIC DISPATCH ]
  [ CALLED ON NULL INPUT ]
  [ INHERIT SPECIAL REGISTERS ]
  [ PREDICATES ( predicate_specification ) ]
  [ { INHERIT ISOLATION LEVEL [ { WITHOUT LOCK REQUEST | WITH LOCK REQUEST } ] } ]
  [ { SECURED | NOT SECURED } ]
  RETURN { expression 
         | SELECT statement
         | BEGIN [ ATOMIC ] 
             [ DECLARE declarations ]
             statement...
           END }
```

Copy

## UDF Option List[¶](#udf-option-list "Link to this heading")

### Description[¶](#id1 "Link to this heading")

DB2 CREATE FUNCTION statements support various options that control the behavior, performance, and security characteristics of the function. These options specify how the function should be executed, what SQL operations it can perform, whether it’s deterministic, and how it handles parallel execution, among other settings.

### Migration Support Table[¶](#migration-support-table "Link to this heading")

The following table shows the DB2 to Snowflake UDF option equivalencies:

| DB2 Option | Snowflake Equivalent | Notes |
| --- | --- | --- |
| `LANGUAGE SQL` | `LANGUAGE SQL` | Translated to Snowflake’s equivalent syntax |
| `SPECIFIC specific_name` | Not Needed | Snowflake doesn’t support specific names for UDFs |
| `DETERMINISTIC` / `NOT DETERMINISTIC` | `IMMUTABLE` / `MUTABLE` | Preserved in Snowflake UDF definition |
| `EXTERNAL ACTION` / `NO EXTERNAL ACTION` | Not Needed | Snowflake doesn’t have equivalent option |
| `READS SQL DATA` | `LANGUAGE SQL` | Snowflake UDFs can read data by default |
| `CONTAINS SQL` | `LANGUAGE SQL` | Basic SQL support is default in Snowflake |
| `MODIFIES SQL DATA` | Not Needed | UDFs that modify data are converted to stored procedures |
| `ALLOW PARALLEL` / `DISALLOW PARALLEL` | Not Needed | Snowflake handles parallelization automatically |
| `STATIC DISPATCH` | Not Needed | Not applicable in Snowflake’s architecture |
| `CALLED ON NULL INPUT` | Default Behavior | Snowflake UDFs handle NULL inputs by default |
| `INHERIT SPECIAL REGISTERS` | Not Needed | Snowflake doesn’t have equivalent special registers |
| `PREDICATES (...)` | Not Needed | Snowflake doesn’t support predicate pushdown specifications |
| `INHERIT ISOLATION LEVEL` | Not Needed | Snowflake uses different transaction isolation model |
| `SECURED` / `NOT SECURED` | Not Needed | Snowflake uses different security model |
| `PARAMETER CCSID` | Not Needed | Character set handling differs in Snowflake |

Note

Options marked as “Not Needed” will be removed during migration because Snowflake either handles the functionality automatically (e.g., parallelization, NULL input handling) or the option is not applicable in Snowflake’s architecture (e.g., special registers, isolation levels).

## INLINE UDF[¶](#inline-udf "Link to this heading")

### Description[¶](#id2 "Link to this heading")

Inline UDFs in DB2 are simple functions that contain a single SQL expression or return statement without complex procedural logic. These functions are typically defined with a direct `RETURN` clause followed by a simple expression, calculation, or query.

SnowConvert AI preserves these as **Inline Functions** in Snowflake, maintaining their simplicity and performance characteristics.

Note

Some parts in the output code are omitted for clarity reasons.

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Input Code:[¶](#input-code "Link to this heading")

#### Db2 - Inline UDF with expression[¶](#db2-inline-udf-with-expression "Link to this heading")

```
CREATE FUNCTION CALCULATE_TAX (price DECIMAL(10,2), tax_rate DECIMAL(5,4))
RETURNS DECIMAL(10,2)
LANGUAGE SQL
DETERMINISTIC
NO EXTERNAL ACTION
CONTAINS SQL
RETURN price * tax_rate;
```

Copy

### Output Code:[¶](#output-code "Link to this heading")

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE FUNCTION CALCULATE_TAX (price DECIMAL(10,2), tax_rate DECIMAL(5,4))
RETURNS DECIMAL(10,2)
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "CzuaAR6Mu3GfenyLFPxUGw==" }}'
AS
$$
    price * tax_rate
$$;
```

Copy

### Input Code:[¶](#id3 "Link to this heading")

#### Db2 - Inline UDF with Select[¶](#db2-inline-udf-with-select "Link to this heading")

```
CREATE FUNCTION GET_EMPLOYEE_COUNT (dept_id INTEGER)
RETURNS INTEGER
LANGUAGE SQL
DETERMINISTIC
READS SQL DATA
RETURN SELECT COUNT(*) FROM employees WHERE department_id = dept_id;
```

Copy

### Output Code:[¶](#id4 "Link to this heading")

#### Snowflake[¶](#id5 "Link to this heading")

```
CREATE FUNCTION GET_EMPLOYEE_COUNT (dept_id INTEGER)
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "HjuaARhyBn6VZ1Uyctr5Ag==" }}'
AS
$$
     SELECT
      COUNT(*) FROM
      employees
     WHERE department_id = :dept_id
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

There are no known issues.

### Related EWIs[¶](#related-ewis "Link to this heading")

There are no related EWIs.

## Scalar UDF[¶](#scalar-udf "Link to this heading")

### Description[¶](#id6 "Link to this heading")

Scalar UDFs in DB2 are functions that return a single value and can contain more complex logic than inline functions. These functions may include procedural constructs such as variable declarations, conditional statements, loops, and multiple SQL statements. Unlike inline UDFs, scalar UDFs with complex logic use a `BEGIN...END` block structure to encapsulate their functionality.

**SnowConvert AI Migration**: If the scalar UDF logic is compatible with Snowflake Scripting syntax, it will be translated to a **Snowflake Scripting UDF**. This preserves the function’s behavior while adapting it to Snowflake’s UDF implementation. Functions that contain unsupported constructs will be converted to stored procedures instead.

Note

Some parts in the output code are omitted for clarity reasons.

### Sample Source Patterns[¶](#id7 "Link to this heading")

#### Input Code:[¶](#id8 "Link to this heading")

#### Db2 - Scalar UDF with IF ELSE Statement[¶](#db2-scalar-udf-with-if-else-statement "Link to this heading")

```
CREATE FUNCTION CALCULATE_DISCOUNT (purchase_amount DECIMAL(10,2), customer_type VARCHAR(20))
RETURNS DECIMAL(10,2)
LANGUAGE SQL
DETERMINISTIC
NO EXTERNAL ACTION
CONTAINS SQL
BEGIN
    DECLARE discount_rate DECIMAL(5,4);
    DECLARE final_discount DECIMAL(10,2);
    
    IF customer_type = 'PREMIUM' THEN
        SET discount_rate = 0.15;
    ELSIF customer_type = 'GOLD' THEN
        SET discount_rate = 0.10;
    ELSIF customer_type = 'SILVER' THEN
        SET discount_rate = 0.05;
    ELSE
        SET discount_rate = 0.02;
    END IF;
    
    SET final_discount = purchase_amount * discount_rate;
    RETURN final_discount;
END;
```

Copy

### Output Code:[¶](#id9 "Link to this heading")

#### Snowflake[¶](#id10 "Link to this heading")

```
CREATE FUNCTION CALCULATE_DISCOUNT (purchase_amount DECIMAL(10,2), customer_type VARCHAR(20))
RETURNS DECIMAL(10,2)
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "usGaAajDzniYFKtk+Fvnzg==" }}'
AS
$$
    DECLARE
        discount_rate DECIMAL(5,4);
        final_discount DECIMAL(10,2);
    BEGIN
        IF (:customer_type = 'PREMIUM') THEN
            discount_rate := 0.15;
        ELSEIF (:customer_type = 'GOLD') THEN
            discount_rate := 0.10;
        ELSEIF (:customer_type = 'SILVER') THEN
            discount_rate := 0.05;
        ELSE
            discount_rate := 0.02;
        END IF;
        final_discount := purchase_amount * discount_rate;
    RETURN final_discount;
    END
$$;
```

Copy

### Input Code:[¶](#id11 "Link to this heading")

#### Db2 - Scalar UDF with WHILE Loop[¶](#db2-scalar-udf-with-while-loop "Link to this heading")

```
CREATE FUNCTION CALCULATE_COMPOUND_INTEREST (principal DECIMAL(15,2), rate DECIMAL(5,4), years INTEGER)
RETURNS DECIMAL(15,2)
LANGUAGE SQL
DETERMINISTIC
NO EXTERNAL ACTION
CONTAINS SQL
BEGIN
    DECLARE counter INTEGER DEFAULT 1;
    DECLARE amount DECIMAL(15,2);
    
    SET amount = principal;
    
    WHILE counter <= years DO
        SET amount = amount * (1 + rate);
        SET counter = counter + 1;
    END WHILE;
    
    RETURN amount;
END;
```

Copy

### Output Code:[¶](#id12 "Link to this heading")

#### Snowflake[¶](#id13 "Link to this heading")

```
CREATE FUNCTION CALCULATE_COMPOUND_INTEREST (principal DECIMAL(15,2), rate DECIMAL(5,4), years INTEGER)
RETURNS DECIMAL(15,2)
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "usGaAajDzniYFKtk+Fvnzg==" }}'
AS
$$
    DECLARE
        counter INTEGER DEFAULT 1;
        amount DECIMAL(15,2);
    BEGIN
        amount := principal;
        WHILE (:counter <= :years) DO
            amount := amount * (1 + rate);
            counter := counter + 1;
        END WHILE;

        RETURN amount;
    END
$$;
```

Copy

### Input Code:[¶](#id14 "Link to this heading")

#### Db2 - Scalar UDF with simple select into for variable assignment.[¶](#db2-scalar-udf-with-simple-select-into-for-variable-assignment "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice DECIMAL(10, 2),
    p_Quantity INT
)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
BEGIN
    DECLARE v_Discount DECIMAL(5, 2);
    DECLARE v_Subtotal DECIMAL(10, 2);
    DECLARE v_FinalPrice DECIMAL(10, 2);
    
    SELECT CASE 
               WHEN p_Quantity >= 10 THEN 0.15
               WHEN p_Quantity >= 5 THEN 0.10
               ELSE 0.05
           END,
           p_BasePrice * p_Quantity
    INTO v_Discount, v_Subtotal
    FROM SYSIBM.SYSDUMMY1;
    
    SET v_FinalPrice = v_Subtotal * (1 - v_Discount);
    
    RETURN v_FinalPrice;
END;
```

Copy

### Output Code:[¶](#id15 "Link to this heading")

#### Snowflake[¶](#id16 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice DECIMAL(10, 2),
    p_Quantity INT
)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "o8GaAaDmH3aONT/SIuOCFw==" }}'
AS
$$
    DECLARE
        v_Discount DECIMAL(5, 2);
        v_Subtotal DECIMAL(10, 2);
        v_FinalPrice DECIMAL(10, 2);
    BEGIN
        v_Discount := CASE
                        WHEN :p_Quantity >= 10 THEN 0.15
                        WHEN :p_Quantity >= 5 THEN 0.10
                            ELSE 0.05
                        END;
        v_Subtotal := :p_BasePrice * :p_Quantity;
        v_FinalPrice := v_Subtotal * (1 - v_Discount);

    RETURN v_FinalPrice;
    END
$$;
```

Copy

### Input Code:[¶](#id17 "Link to this heading")

#### Db2 - Scalar UDF with Values statement for variable assignment.[¶](#db2-scalar-udf-with-values-statement-for-variable-assignment "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice DECIMAL(10, 2),
    p_Quantity INT
)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
BEGIN
    DECLARE v_Discount DECIMAL(5, 2);
    DECLARE v_Subtotal DECIMAL(10, 2);
    DECLARE v_FinalPrice DECIMAL(10, 2);
    
    VALUES (CASE 
                WHEN p_Quantity >= 10 THEN 0.15
                WHEN p_Quantity >= 5 THEN 0.10
                ELSE 0.05
            END,
            p_BasePrice * p_Quantity)
    INTO v_Discount, v_Subtotal;
    
    SET v_FinalPrice = v_Subtotal * (1 - v_Discount);
    
    RETURN v_FinalPrice;
END;
```

Copy

### Output Code:[¶](#id18 "Link to this heading")

#### Snowflake[¶](#id19 "Link to this heading")

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice DECIMAL(10, 2),
    p_Quantity INT
)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "usGaAajDzniYFKtk+Fvnzg==" }}'
AS
$$
    DECLARE
        v_Discount DECIMAL(5, 2);
        v_Subtotal DECIMAL(10, 2);
        v_FinalPrice DECIMAL(10, 2);
    BEGIN
        v_Discount := CASE
                            WHEN :p_Quantity >= 10 THEN 0.15
                            WHEN :p_Quantity >= 5 THEN 0.10
                            ELSE 0.05
                        END;
        v_Subtotal :=
        p_BasePrice * p_Quantity;
        v_FinalPrice := v_Subtotal * (1 - v_Discount);

            RETURN v_FinalPrice;
    END
$$;
```

Copy

### Known Issues[¶](#id20 "Link to this heading")

Warning

**SnowConvert AI will not translate UDFs containing the following elements into SnowScripting UDFs, as these features are unsupported in SnowScripting UDFs:**

* Access database tables
* Use cursors
* Call other UDFs
* Contain aggregate or window functions
* Perform DML operations (INSERT/UPDATE/DELETE)
* Return result sets

### Related EWIs[¶](#id21 "Link to this heading")

There are no related EWIs.

## Table UDF[¶](#table-udf "Link to this heading")

### Description[¶](#id22 "Link to this heading")

Table UDFs (Table-Valued Functions) in DB2 are functions that return a table result set rather than a single value. These functions can be used in the FROM clause of SELECT statements. Table UDFs are defined with a `RETURNS TABLE` clause that specifies the structure of the returned table.

**SnowConvert AI Migration**: Table UDFs that are compatible with Snowflake’s table function syntax will be translated to **Snowflake Table Functions**. This preserves their functionality while adapting them to Snowflake’s implementation. Functions that contain unsupported [Snowflake Scripting](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-procedural-functions) elements will be converted to stored procedures that return result sets instead.

Note

Some parts in the output code are omitted for clarity reasons.

## Sample Source Patterns[¶](#id23 "Link to this heading")

### Input Code:[¶](#id24 "Link to this heading")

#### Db2 - Simple Table UDF[¶](#db2-simple-table-udf "Link to this heading")

```
CREATE FUNCTION GET_EMPLOYEES_BY_DEPT (dept_id INTEGER)
RETURNS TABLE (
    employee_id INTEGER,
    employee_name VARCHAR(100),
    salary DECIMAL(10,2),
    hire_date DATE
)
LANGUAGE SQL
DETERMINISTIC
READS SQL DATA
RETURN
    SELECT emp_id, emp_name, emp_salary, emp_hire_date
    FROM employees 
    WHERE department_id = dept_id
    ORDER BY emp_name;
```

Copy

### Output Code:[¶](#id25 "Link to this heading")

#### Snowflake[¶](#id26 "Link to this heading")

```
CREATE FUNCTION GET_EMPLOYEES_BY_DEPT (dept_id INTEGER)
RETURNS TABLE (
    employee_id INTEGER,
     employee_name VARCHAR(100),
     salary DECIMAL(10,2),
     hire_date DATE
)
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "3TuaAdyRFHCJuSE7bnMCGg==" }}'
AS
$$
    SELECT emp_id, emp_name, emp_salary, emp_hire_date
    FROM
      employees
    WHERE department_id = dept_id
    ORDER BY emp_name
$$;
```

Copy

### Input Code:[¶](#id27 "Link to this heading")

#### Db2 - Complex Table UDF with Multiple Parameters[¶](#db2-complex-table-udf-with-multiple-parameters "Link to this heading")

```
CREATE FUNCTION GET_SALES_REPORT (start_date DATE, end_date DATE, min_amount DECIMAL(10,2))
RETURNS TABLE (
    sales_id INTEGER,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    sale_amount DECIMAL(10,2),
    sale_date DATE,
    region VARCHAR(50)
)
LANGUAGE SQL
DETERMINISTIC
READS SQL DATA
RETURN
    SELECT s.sale_id, c.customer_name, p.product_name, 
           s.amount, s.sale_date, c.region
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    JOIN products p ON s.product_id = p.product_id
    WHERE s.sale_date BETWEEN start_date AND end_date
      AND s.amount >= min_amount
    ORDER BY s.sale_date DESC, s.amount DESC;
```

Copy

### Output Code:[¶](#id28 "Link to this heading")

#### Snowflake[¶](#id29 "Link to this heading")

```
CREATE FUNCTION GET_SALES_REPORT (start_date DATE, end_date DATE, min_amount DECIMAL(10,2))
RETURNS TABLE (
    sales_id INTEGER,
     customer_name VARCHAR(100),
     product_name VARCHAR(100),
     sale_amount DECIMAL(10,2),
     sale_date DATE,
     region VARCHAR(50)
)
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "3TuaAdyRFHCJuSE7bnMCGg==" }}'
AS
$$
    SELECT s.sale_id, c.customer_name, p.product_name,
           s.amount, s.sale_date, c.region
    FROM
      sales s
    JOIN
        customers c ON s.customer_id = c.customer_id
    JOIN
        products p ON s.product_id = p.product_id
    WHERE s.sale_date BETWEEN start_date AND end_date
      AND s.amount >= min_amount
    ORDER BY s.sale_date DESC, s.amount DESC
$$;
```

Copy

### Known Issues[¶](#id30 "Link to this heading")

There are no known issues.

### Related EWIs.[¶](#id31 "Link to this heading")

There are no related EWIs.

## UDF Converted to Stored Procedure[¶](#udf-converted-to-stored-procedure "Link to this heading")

### Description[¶](#id32 "Link to this heading")

Some DB2 UDFs cannot be directly migrated as Snowflake UDFs due to limitations in [Snowflake Scripting UDFs](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-procedural-functions). When a DB2 UDF contains elements that are not supported in Snowflake Scripting UDFs (such as SQL DML statements, cursors, result sets, or calls to other UDFs), SnowConvert AI will migrate these functions as **Stored Procedures** instead.

**SnowConvert AI Migration**: These UDFs are converted to stored procedures with an **EWI** message explaining why the direct UDF migration was not possible.

Note

Some parts in the output code are omitted for clarity reasons.

### Sample Source Patterns[¶](#id33 "Link to this heading")

#### Input Code:[¶](#id34 "Link to this heading")

#### Db2 - UDF with DML Statement[¶](#db2-udf-with-dml-statement "Link to this heading")

```
CREATE FUNCTION LOG_AUDIT_EVENT (event_type VARCHAR(50), event_details VARCHAR(500))
RETURNS INTEGER
LANGUAGE SQL
DETERMINISTIC
MODIFIES SQL DATA
BEGIN
    INSERT INTO audit_log (event_type, event_details, log_timestamp)
    VALUES (event_type, event_details, CURRENT_TIMESTAMP);
    
    RETURN 1;
END;
```

Copy

#### Output Code:[¶](#id35 "Link to this heading")

##### Snowflake[¶](#id36 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE BECAUSE IT CONTAINS THE FOLLOWING: VALUES CLAUSE, INSERT STATEMENT ***/!!!
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "audit_log" **
CREATE OR REPLACE PROCEDURE LOG_AUDIT_EVENT (event_type VARCHAR(50), event_details VARCHAR(500))
RETURNS INTEGER
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "10/31/2025",  "domain": "no-domain-provided",  "migrationid": "9DuaAVemZHCpeN/qzhiOkg==" }}'
AS
$$
BEGIN
    INSERT INTO audit_log (event_type, event_details, log_timestamp)
    VALUES (event_type, event_details, CURRENT_TIMESTAMP);

    RETURN 1;
END
$$;
```

Copy

### Known Issues[¶](#id37 "Link to this heading")

The main limitation is that the resulting converted procedure must be invoked using the CALL syntax, preventing its use directly within standard SQL expressions like the original UDF.

### Related EWIs[¶](#id38 "Link to this heading")

1. **SSC-EWI-0068**: User defined function was transformed to a Snowflake procedure.

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
3. [UDF Option List](#udf-option-list)
4. [INLINE UDF](#inline-udf)
5. [Sample Source Patterns](#sample-source-patterns)
6. [Scalar UDF](#scalar-udf)
7. [Table UDF](#table-udf)
8. [Sample Source Patterns](#id23)
9. [UDF Converted to Stored Procedure](#udf-converted-to-stored-procedure)