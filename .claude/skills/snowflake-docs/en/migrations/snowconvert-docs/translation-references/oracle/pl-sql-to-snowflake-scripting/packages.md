---
auto_generated: true
description: Use the CREATE PACKAGE statement to create the specification for a stored
  package, which is an encapsulated collection of related procedures, functions, and
  other program objects stored together in th
last_scraped: '2026-01-14T16:53:25.999813+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/packages
title: SnowConvert AI - Oracle - PACKAGES | Snowflake Documentation
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)[PL/SQL to Snowflake Scripting](README.md)PACKAGES

# SnowConvert AI - Oracle - PACKAGES[¶](#snowconvert-ai-oracle-packages "Link to this heading")

## Description[¶](#description "Link to this heading")

> Use the `CREATE` `PACKAGE` statement to create the specification for a stored package, which is an encapsulated collection of related procedures, functions, and other program objects stored together in the database. The package specification declares these objects. The package body, specified subsequently, defines these objects.([Oracle PL/SQL Language Reference CREATE PACKAGE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PACKAGE.html#GUID-40636655-899F-47D0-95CA-D58A71C94A56))

Snowflake does not have an equivalent for Oracle packages, so in order to maintain the structure, the packages are transformed into a schema, and all its elements are defined inside it. Also, the package and its elements are renamed to preserve the original schema name.

## BODY[¶](#body "Link to this heading")

### Description[¶](#id1 "Link to this heading")

The header of the PACKAGE BODY is removed and each procedure or function definition is transformed into a standalone function or procedure.

#### CREATE PACKAGE SYNTAX[¶](#create-package-syntax "Link to this heading")

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE BODY plsql_package_body_source
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

Note

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE OR REPLACE PACKAGE BODY SCHEMA1.PKG1 AS
    PROCEDURE procedure1 AS
        BEGIN
            dbms_output.put_line('hello world');
        END;
END package1;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

##### Snowflake[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE SCHEMA1_PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('hello world');
    END;
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-OR0035](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0035): DBMS\_OUTPUT.PUTLINE check UDF implementation.

## Constants[¶](#constants "Link to this heading")

Translation spec for Package Constants

### Description[¶](#id3 "Link to this heading")

PACKAGE CONSTANTS can be declared either in the package declaration or in the PACKAGE BODY. When a package constant is used in a procedure, a new variable is declared with the same name and value as the constant, so the resulting code is pretty similar to the input.

#### Oracle Constant declaration Syntax[¶](#oracle-constant-declaration-syntax "Link to this heading")

```
constant CONSTANT datatype [NOT NULL] { := | DEFAULT } expression ;
```

Copy

### Sample Source Patterns[¶](#id4 "Link to this heading")

#### Sample auxiliary code[¶](#sample-auxiliary-code "Link to this heading")

##### Oracle[¶](#id5 "Link to this heading")

```
create table table1(id number);
```

Copy

##### Snowflake[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

##### Oracle[¶](#id7 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_constant CONSTANT NUMBER:= 9999;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_constant);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

Copy

##### Result[¶](#result "Link to this heading")

| ID |
| --- |
| 9999 |

##### Snowflake[¶](#id8 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PACKAGE_CONSTANT NUMBER := 9999;
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(:PACKAGE_CONSTANT);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

Copy

##### Result[¶](#id9 "Link to this heading")

| ID |
| --- |
| 9999 |

Note

Note that the`PROCEDURE` definition is being removed since it is not required in Snowflake.

### Known Issues[¶](#id10 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id11 "Link to this heading")

1. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.

## DECLARATION[¶](#declaration "Link to this heading")

### Description[¶](#id12 "Link to this heading")

The declaration is converted to a schema, so each inner element is declared inside this schema. All the elements present in the package are commented except for the VARIABLES which have a proper transformation.

#### CREATE PACKAGE SYNTAX[¶](#id13 "Link to this heading")

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE plsql_package_source
```

Copy

### Sample Source Patterns[¶](#id14 "Link to this heading")

Note

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle[¶](#id15 "Link to this heading")

```
CREATE OR REPLACE PACKAGE SCHEMA1.PKG1 AS
   -- Function Declaration
   FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER;

   -- Procedure Declaration
   PROCEDURE procedure_declaration(param1 VARCHAR2, param2 VARCHAR2);

END PKG1;
```

Copy

##### Snowflake[¶](#id16 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS SCHEMA1_PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

Note

Note that both `FUNCTION` and `PROCEDURE` definitions are being removed since they are not required in Snowflake.

### Known Issues[¶](#id17 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id18 "Link to this heading")

No related EWIs.

## VARIABLES[¶](#variables "Link to this heading")

Translation spec for Package Variables

### Description[¶](#id19 "Link to this heading")

PACKAGE VARIABLES can be declared either in the package declaration or in the PACKAGE BODY. Due to its behavior, these variables are converted into [Snowflake session variables](https://docs.snowflake.com/en/sql-reference/session-variables.html) so each usage or assignment is translated to its equivalent in Snowflake.

#### Oracle Variable declaration syntax[¶](#oracle-variable-declaration-syntax "Link to this heading")

```
variable datatype [ [ NOT NULL] {:= | DEFAULT} expression ] ;
```

Copy

### Sample Source Patterns[¶](#id20 "Link to this heading")

#### Sample auxiliary code[¶](#id21 "Link to this heading")

##### Oracle[¶](#id22 "Link to this heading")

```
create table table1(id number);
```

Copy

##### Snowflake[¶](#id23 "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

#### Variable declaration[¶](#variable-declaration "Link to this heading")

##### Oracle[¶](#id24 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PKG1 AS
    package_variable NUMBER:= 100;
END PKG1;
```

Copy

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);
```

Copy

#### Variable Usage[¶](#variable-usage "Link to this heading")

Package variable usages are transformed into the Snowflake [GETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions) function which accesses the current value of a session variable. An explicit cast is added to the original variable data type in order to maintain the functional equivalence in the operations where these variables are used.

##### Oracle[¶](#id25 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM TABLE1;
```

Copy

##### Result[¶](#id26 "Link to this heading")

| ID |
| --- |
| 100 |

##### Snowflake[¶](#id27 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

Copy

##### Result[¶](#id28 "Link to this heading")

| ID |
| --- |
| 100 |

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

### Variable regular assignment[¶](#variable-regular-assignment "Link to this heading")

When a package variable is assigned using the `:=` operator, the assignation is replaced by a SnowConvert AI UDF called UPDATE\_PACKAGE\_VARIABLE\_STATE which is an abstraction of the Snowflake [SETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions) function.

Oracle

#### Oracle[¶](#id29 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        package_variable := package_variable + 100;
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

Copy

##### Result[¶](#id30 "Link to this heading")

| ID |
| --- |
| 200 |

#### Snowflake[¶](#id31 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER + 100));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

Copy

##### Result[¶](#id32 "Link to this heading")

| ID |
| --- |
| 200 |

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

#### Variable assignment as an output argument[¶](#variable-assignment-as-an-output-argument "Link to this heading")

When a package variable is used as an output argument a new variable is declared inside the procedure, this variable will catch the output argument value of the procedure, and then the variable will be used to update the session variable which refers to the package variable using the UPDATE\_PACKAGE\_VARIABLE\_STATE mentioned above.

##### Oracle[¶](#id33 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    PROCEDURE procedure2(out_param OUT NUMBER);
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        procedure2(package_variable);
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
    PROCEDURE procedure2 (out_param OUT NUMBER) AS
    BEGIN
        out_param := 1000;
    END;
END PKG1;

CALL PKG1.procedure1();
```

Copy

##### Result[¶](#id34 "Link to this heading")

| ID |
| --- |
| 1000 |

##### Snowflake[¶](#id35 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PKG1_PACKAGE_VARIABLE VARIANT;
    BEGIN
        CALL PKG1.
        procedure2(:PKG1_PACKAGE_VARIABLE);
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(:PKG1_PACKAGE_VARIABLE));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CREATE OR REPLACE PROCEDURE PKG1.procedure2 (out_param OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        out_param := 1000;
    END;
$$;

CALL PKG1.procedure1();
```

Copy

##### Result[¶](#id36 "Link to this heading")

| ID |
| --- |
| 1000 |

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

### Known Issues[¶](#id37 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id38 "Link to this heading")

1. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.

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
2. [BODY](#body)
3. [Constants](#constants)
4. [DECLARATION](#declaration)
5. [VARIABLES](#variables)