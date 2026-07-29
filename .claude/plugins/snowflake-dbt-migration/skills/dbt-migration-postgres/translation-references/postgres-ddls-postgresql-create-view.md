---
description: Translation from PostgreSQL to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/postgresql-create-view
title: SnowConvert AI - PostgreSQL - CREATE VIEW | Snowflake Documentation
---

## Applies to

- PostgreSQL
- Greenplum
- Netezza

## Description

This command creates a view in a database, which is run every time the view is referenced in a
query.

For more information, please refer to
[`CREATE VIEW`](https://www.postgresql.org/docs/current/sql-createview.html) documentation.

## Grammar Syntax

```sql
CREATE [OR REPLACE] [TEMP | TEMPORARY] [RECURSIVE] VIEW `<name>` [ ( `<column_name>` [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS `<query>`
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

## Code Examples

### [OR REPLACE] [TEMP | TEMPORARY] [RECURSIVE]

Hint

This syntax is fully supported in Snowflake.

#### Input Code

##### PostgreSQL

```sql
CREATE OR REPLACE VIEW view1 AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
        table1
    GROUP BY
        product_id;

CREATE TEMPORARY RECURSIVE VIEW view2 AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
        table1
    GROUP BY
        product_id;
```

#### Output Code

##### Snowflake

```sql
CREATE OR REPLACE VIEW view1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
table1
    GROUP BY
        product_id;

CREATE TEMPORARY RECURSIVE VIEW view2
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT
        product_id,
        SUM(quantity) AS sum_quantity
    FROM
table1
    GROUP BY
        product_id;
```

### WITH CHECK CLAUSE

This WITH CHECK CLAUSE clause on a view enforces that any data inserted or updated through the view
must satisfy the view’s defining conditions. LOCAL checks only the current view’s conditions, while
CASCADED checks conditions of the view and all underlying views. It prevents creating rows that are
invisible through the view and cannot be used with recursive views.

Danger

This syntax is not supported in Snowflake.

#### Input Code: 2

##### PostgreSQL 2

```sql
CREATE VIEW updatable_products AS
    SELECT id, name, price
    FROM products
    WHERE price > 0
WITH LOCAL CHECK OPTION;
```

#### Output Code: 2

##### Snowflake 2

```sql
CREATE VIEW updatable_products
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT id, name, price
    FROM
products
    WHERE price > 0;
```

### WITH PARAMETERS OPTIONS

This WITH PARAMETERS OPTIONS allows setting optional properties for the view, such as how
modifications through the view are checked (check_option) and whether to enforce row-level security
(security_barrier).

Danger

This syntax is not supported in Snowflake.

#### Input Code: 3

##### PostgreSQL 3

```sql
CREATE VIEW large_orders WITH (security_barrier=true, check_option=local) AS
    SELECT order_id, customer_id, total_amount
    FROM orders
    WHERE total_amount > 1000;
```

#### Output Code: 3

##### Snowflake 3

```sql
CREATE VIEW large_orders
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/14/2025",  "domain": "no-domain-provided" }}'
AS
    SELECT order_id, customer_id, total_amount
    FROM
orders
    WHERE total_amount > 1000;
```

### VALUES OPTION

Hint

This syntax is fully supported in Snowflake.

#### Input Code: 4

##### PostgreSQL 4

```sql
CREATE VIEW numbers_view (number_1) AS
    VALUES (1,2), (2,2), (3,2), (4,2), (5,2);
```

#### Output Code: 4

##### Snowflake 4

```sql
CREATE VIEW numbers_view
AS
SELECT
*
FROM
(
        VALUES (1,2), (2,2), (3,2), (4,2), (5,2)
) AS numbers_view (
        number_1
);
```
