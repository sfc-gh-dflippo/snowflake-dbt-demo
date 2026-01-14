---
description: This section shows equivalents between data types in Oracle and Snowflake,
  as well as some notes on arithmetic differences.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/README
title: SnowConvert AI - Oracle - Data Types | Snowflake Documentation
---

## Notes on arithmetic operations[¶](#notes-on-arithmetic-operations)

Please be aware that every operation performed on numerical datatypes is internally stored as a Number. Furthermore, depending on the operation performed it is possible to incur an error related to how intermediate values are stored within Snowflake, for more information please check this post on [Snowflake’s post on intermediate numbers in Snowflake](https://community.snowflake.com/s/question/0D50Z00008HhSHCSA3/sql-compilation-error-invalid-intermediate-datatype-number7148).

## ANSI Data Types[¶](#ansi-data-types)

### Description[¶](#description)

> SQL statements that create tables and clusters can also use ANSI data types and data types from the IBM products SQL/DS and DB2. Oracle recognizes the ANSI or IBM data type name that differs from the Oracle Database data type name. It converts the data type to the equivalent Oracle data type, records the Oracle data type as the name of the column data type, and stores the column data in the Oracle data type based on the conversions shown in the tables that follow. ([Oracle Language Reference ANSI, DB2, and SQL/DS Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-0BC16006-32F1-42B1-B45E-F27A494963FF)).

When creating a new table, Oracle and Snowflake handle some data types as synonyms and aliases and transform them into the default data type. As shown in the next table:

<!-- prettier-ignore -->
|ANSI|ORACLE|SNOWFLAKE|
|---|---|---|
|CHARACTER (n)|CHAR (n)|VARCHAR|
|CHAR (n)|CHAR (n)|VARCHAR|
|CHARACTER VARYING (n)|VARCHAR2 (n)|VARCHAR|
|CHAR VARYING (n)|VARCHAR2 (n)|VARCHAR|
|NATIONAL CHARACTER (n)|NCHAR (n)|VARCHAR\*|
|NATIONAL CHAR (n)|NCHAR (n)|VARCHAR\*|
|NCHAR (n)|NCHAR (n)|VARCHAR|
|NATIONAL CHARACTER VARYING (n)|NVARCHAR2 (n)|VARCHAR\*|
|NATIONAL CHAR VARYING (n)|NVARCHAR2 (n)|VARCHAR\*|
|NCHAR VARYING (n)|NVARCHAR2 (n)|NUMBER (p, s)|
|NUMERIC [(p, s)]|NUMBER (p, s)|NUMBER (p, s)|
|DECIMAL [(p, s)]|NUMBER (p, s)|NUMBER (38)|
|INTEGER|NUMBER (38)|NUMBER (38)|
|INT|NUMBER (38)|NUMBER (38)|
|SMALLINT|NUMBER (38)|NUMBER (38)|
|FLOAT|FLOAT (126)|DOUBLE|
|DOUBLE PRECISION|FLOAT (126)|DOUBLE|
|REAL|FLOAT (63)|DOUBLE|

To get more information about the translation specification of the Oracle data types, go to [Oracle Built-in Data Types](oracle-built-in-data-types).

**Note:**

VARCHAR\*: Almost all the ANSI datatypes compile in Snowflake, but those marked with an asterisk, are manually converted to VARCHAR.

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIs[¶](#related-ewis)

EWIs related to these data types are specified in the transformation of the [Oracle Built-in data types.](oracle-built-in-data-types)

## Data Type Customization[¶](#data-type-customization)

SnowConvert AI enables Data Type Customization to specify rules for data type transformation based on data type origin and column name. This feature allows you to personalize data type conversions and set precision values more accurately during migration.

For complete documentation on configuring data type customization, including JSON structure, configuration options, and priority rules, see [Data type mappings](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/oracle-conversion-settings#data-type-mappings) in the Oracle Conversion Settings documentation.

### NUMBER to DECFLOAT Transformation[¶](#number-to-decfloat-transformation)

SnowConvert AI supports transforming Oracle `NUMBER` columns to Snowflake `DECFLOAT` data type. This is useful when you need to preserve the exact decimal precision of numeric values during migration.

When a `NUMBER` column is configured to be transformed to `DECFLOAT`:

1. The column data type in `CREATE TABLE` statements is transformed to `DECFLOAT`
2. Numeric literals in `INSERT` statements that target `DECFLOAT` columns are automatically wrapped with `CAST(... AS DECFLOAT)` to ensure proper data type handling
3. Column references in `INSERT ... SELECT` statements are also cast appropriately

#### Example[¶](#example)

##### Oracle[¶](#oracle)

```
CREATE TABLE products (
    product_id NUMBER(10),
    price NUMBER(15, 2)
);

INSERT INTO products VALUES (1, 99.99);
```

##### Snowflake (with DECFLOAT customization for price column)[¶](#snowflake-with-decfloat-customization-for-price-column)

```
CREATE OR REPLACE TABLE products (
    product_id NUMBER(10),
    price DECFLOAT
);

INSERT INTO products VALUES (1, CAST(99.99 AS DECFLOAT));
```

**Note:**

The TypeMappings report (TypeMappings.csv) provides a detailed view of all data type transformations applied during conversion. See [TypeMappings Report](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/review-results/reports/type-mappings-report) for more information.
