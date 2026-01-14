---
description:
  Returns rows from tables, views, and user-defined functions and inserts them into a new table.
  (Redshift SQL Language Reference SELECT statement)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-select-into
title: SnowConvert AI - Redshift - SELECT INTO | Snowflake Documentation
---

## Description[¶](#description)

> Returns rows from tables, views, and user-defined functions and inserts them into a new table.
> ([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

## Grammar Syntax[¶](#grammar-syntax)

```
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number ] [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...]
INTO [ TEMPORARY | TEMP ] [ TABLE ] new_table
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ GROUP BY expression [, ...] ]
[ HAVING condition [, ...] ]
[ { UNION | INTERSECT | { EXCEPT | MINUS } } [ ALL ] query ]
[ ORDER BY expression
[ ASC | DESC ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

Copy

For more information please refer to each of the following links:

1. [WITH clause](rs-sql-statements-select.html#with-clause)
2. [SELECT list](rs-sql-statements-select.html#select-list)
3. [FROM clause](rs-sql-statements-select.html#from-clause)
4. [WHERE clause](rs-sql-statements-select.html#where-clause)
5. [CONNECT BY clause](rs-sql-statements-select.html#connect-by-clause)
6. [GROUP BY clause](rs-sql-statements-select.html#group-by-clause)
7. [HAVING clause](rs-sql-statements-select.html#having-clause)
8. [QUALIFY clause](rs-sql-statements-select.html#qualify-clause)
9. [UNION, INTERSECT, and EXCEPT](rs-sql-statements-select.html#union-intersect-and-except)
10. [ORDER BY clause](rs-sql-statements-select.html#order-by-clause)
