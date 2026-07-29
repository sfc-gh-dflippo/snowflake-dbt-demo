---
description: <> ALL & = ANY array expressions
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/postgresql-expressions
title: SnowConvert AI - PostgreSQL - Expressions | Snowflake Documentation
---

## ALL & ANY array expressions

<> ALL & = ANY array expressions

### Description

> An expression used to **evaluate and compare** each element of an array against a specified
> expression.
> ([PostgreSQL Language Reference ANY & ALL (array)](https://www.postgresql.org/docs/current/functions-comparisons.html#FUNCTIONS-COMPARISONS-ANY-SOME))

### Grammar Syntax

```sql
 expression operator ANY (array expression)
expression operator ALL (array expression)
```

To support this expression SnowConvert AI translates the `<> ALL` to `NOT IN` and the `= ANY` to
`IN`

### Sample Source Patterns

#### Input Code

##### PostgreSQL

```sql
 SELECT some_column <> ALL (ARRAY[1, 2, 3])
FROM some_table;

SELECT *
FROM someTable
WHERE column_name = ANY (ARRAY[1, 2, 3]);
```

##### Output Code

##### Snowflake

```sql
 SELECT some_column NOT IN (1, 2, 3)
FROM some_table;

SELECT *
 FROM someTable
 WHERE column_name IN (1, 2, 3);
```

#### Known Issues

There are no known issues

#### Related EWIs

There are no related EWIs.
