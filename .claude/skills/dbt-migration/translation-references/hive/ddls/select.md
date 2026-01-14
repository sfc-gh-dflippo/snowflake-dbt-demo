---
description: Hive SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/hive/ddls/select
title: SnowConvert AI - Hive - SELECT | Snowflake Documentation
---

## Description[¶](#description)

Spark supports a `SELECT` statement and conforms to the ANSI SQL standard. Queries are used to
retrieve result sets from one or more tables.
([Spark SQL Language Reference SELECT](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select.html))

Warning

This grammar is partially supported in Snowflake. Translation pending for these CREATE VIEW
elements:

```
[ SORT BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
[ CLUSTER BY { expression [ , ... ] } ]
[ DISTRIBUTE BY { expression [, ... ] } ]
[ WINDOW { named_window [ , WINDOW named_window, ... ] } ]
[ PIVOT clause ]
[ UNPIVOT clause ]
[ LATERAL VIEW clause ] [ ... ]
[ regex_column_names ]
[ TRANSFORM (...) ]
[ LIMIT non_literal_expression ]

from_item :=
join_relation
table_value_function
LATERAL(subquery)
file_format.`file_path`

select_statement { INTERSECT | EXCEPT } { ALL | DISTINCT } select_statement
```

Copy

## Grammar Syntax[¶](#grammar-syntax)

```
[ WITH with_query [ , ... ] ]
select_statement [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select_statement, ... ]
    [ ORDER BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
    [ SORT BY { expression [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [ , ... ] } ]
    [ CLUSTER BY { expression [ , ... ] } ]
    [ DISTRIBUTE BY { expression [, ... ] } ]
    [ WINDOW { named_window [ , WINDOW named_window, ... ] } ]
    [ LIMIT { ALL | expression } ]

select_statement :=
SELECT [ hints , ... ] [ ALL | DISTINCT ] { [ [ named_expression | regex_column_names ] [ , ... ] | TRANSFORM (...) ] }
    FROM { from_item [ , ... ] }
    [ PIVOT clause ]
    [ UNPIVOT clause ]
    [ LATERAL VIEW clause ] [ ... ]
    [ WHERE boolean_expression ]
    [ GROUP BY expression [ , ... ] ]
    [ HAVING boolean_expression ]

with_query :=
expression_name [ ( column_name [ , ... ] ) ] [ AS ] ( query )

from_item :=
table_relation |
join_relation |
table_value_function |
inline_table |
LATERAL(subquery) |
file_format.`file_path`
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns)

### GROUP BY[¶](#group-by)

The `WITH { CUBE | ROLLUP }` syntax is transformed to its `CUBE(expr1, ...)` or `ROLLUP(expr1, ...)`
equivalent

#### Input Code:[¶](#input-code)

```
-- Basic case of GROUP BY
SELECT id, sum(quantity) FROM dealer GROUP BY 1;

-- Grouping by GROUPING SETS
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ());

-- Grouping by ROLLUP
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY ROLLUP(city, car_model);

SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY city, car_model WITH ROLLUP;

-- Grouping by CUBE
SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY CUBE(city, car_model);

SELECT city, car_model, sum(quantity) AS sum FROM dealer
    GROUP BY city, car_model WITH CUBE;
```

Copy

#### Output Code:[¶](#output-code)

```
-- Basic case of GROUP BY
SELECT id,
    SUM(quantity) FROM
    dealer
GROUP BY 1;

-- Grouping by GROUPING SETS
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), () !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'EmptyGroupingSet' NODE ***/!!!);

-- Grouping by ROLLUP
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY
    ROLLUP(city, car_model);

SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
GROUP BY
    ROLLUP(city, car_model);

-- Grouping by CUBE
SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
    GROUP BY CUBE(city, car_model) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'CUBE' NODE ***/!!!;

SELECT city, car_model,
    SUM(quantity) AS sum FROM
    dealer
GROUP BY
    CUBE(city, car_model);
```

Copy

### Hints[¶](#hints)

Snowflake performs automatic optimization of JOINs and partitioning, meaning that hints are
unnecessary, they are preserved as comments in the output code.

#### Input Code:[¶](#id1)

```
SELECT
/*+ REBALANCE */ /*+ COALESCE(2) */
*
FROM my_table;
```

Copy

#### Output Code:[¶](#id2)

```
SELECT
/*+ REBALANCE */ /*+ COALESCE(2) */
*
FROM
my_table;
```

Copy

### CTE[¶](#cte)

The `AS` keyword is optional in Spark/Databricks, however in Snowflake is required so it is added.

#### Input Code:[¶](#id3)

```
WITH my_cte (
   SELECT id, name FROM my_table
)
SELECT *
FROM my_cte
WHERE id = 1;
```

Copy

#### Output Code:[¶](#id4)

```
WITH my_cte AS (
     SELECT id, name FROM
        my_table
  )
SELECT *
FROM
     my_cte
WHERE id = 1;
```

Copy

### LIMIT[¶](#limit)

`LIMIT ALL` is removed as it is not needed in Snowflake, LIMIT with a literal value is preserved
as-is.

#### Input Code:[¶](#id5)

```
SELECT * FROM my_table LIMIT ALL;

SELECT * FROM my_table LIMIT 5;
```

Copy

#### Output Code:[¶](#id6)

```
SELECT * FROM
my_table;

SELECT * FROM
my_table
LIMIT 5;
```

Copy

### ORDER BY[¶](#order-by)

Note

This clause is fully supported in Snowflake

### WHERE[¶](#where)

Note

This clause is fully supported in Snowflake

### HAVING[¶](#having)

Note

This clause is fully supported in Snowflake

### FROM table_relation[¶](#from-table-relation)

Note

This clause is fully supported in Snowflake

### FROM inline_table[¶](#from-inline-table)

Note

This clause is fully supported in Snowflake

### UNION [ALL | DISTINCT][¶](#union-all-distinct)

Note

This clause is fully supported in Snowflake

### INTERSECT (no keywords)[¶](#intersect-no-keywords)

Note

This clause is fully supported in Snowflake

### EXCEPT (no keywords)[¶](#except-no-keywords)

Note

This clause is fully supported in Snowflake
