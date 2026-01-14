---
description:
  An expression used to evaluate and compare each element of an array against a specified
  expression. (Vertica Language Reference ANY & ALL (array))
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-predicates
title: SnowConvert AI - Vertica - Predicates | Snowflake Documentation
---

## ALL & ANY array expressions[¶](#all-any-array-expressions)

### Description[¶](#description)

An expression used to **evaluate and compare** each element of an array against a specified
expression.
([Vertica Language Reference ANY & ALL (array)](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/any-and-all/))

### Grammar Syntax[¶](#grammar-syntax)

```
expression operator ANY (array expression)
expression operator ALL (array expression)
```

Copy

To support this expression SnowConvert AI translates the `<> ALL` to `NOT IN` and the `= ANY` to
`IN`

### Sample Source Patterns[¶](#sample-source-patterns)

#### Input Code:[¶](#input-code)

```
SELECT some_column <> ALL (ARRAY[1, 2, 3])
FROM some_table;

SELECT *
FROM someTable
WHERE column_name = ANY (ARRAY[1, 2, 3]);
```

Copy

#### Output Code:[¶](#output-code)

```
SELECT some_column NOT IN (1, 2, 3)
FROM some_table;

SELECT *
 FROM someTable
 WHERE column_name IN (1, 2, 3);
```

Copy

#### Known Issues[¶](#known-issues)

There are no known issues

#### Related EWIs[¶](#related-ewis)

There are no related EWIs.

## LIKE[¶](#like)

LIKE Predicate

### Description[¶](#id1)

> Retrieves rows where a string expression—typically a column—matches the specified pattern or, if
> qualified by ANY or ALL, set of patterns
> ([Vertica SQL Language Reference Like Predicate](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/like/))

### Grammar Syntax[¶](#id2)

```
 string-expression [ NOT ] { LIKE | ILIKE | LIKEB | ILIKEB }
   { pattern | { ANY | SOME | ALL } ( pattern,... ) } [ ESCAPE 'char' ]
```

Copy

#### Vertica Substitute symbols[¶](#vertica-substitute-symbols)

<!-- prettier-ignore -->
|Symbol|Vertica Equivalent|Snowflake Equivalent|
|---|---|---|
|~~|LIKE|LIKE|
|~#|LIKEB|LIKE|
|~~\*|ILIKE|ILIKE|
|~#\*|ILIKEB|ILIKE|
|!~~|NOT LIKE|NOT LIKE|
|!~#|NOT LIKEB|NOT LIKE|
|!~~\*|NOT ILIKE|NOT ILIKE|
|!~#\*|NOT ILIKEB|NOT ILIKE|

In Vertica, the default escape character is the backslash (`\`). Snowflake doesn’t have a default
escape character. SnowConvert AI will automatically add the `ESCAPE` clause when needed.

It’s important to know that Snowflake requires the backslash to be escaped (`\\`) when you use it as
an escape character within both the expression and the `ESCAPE` clause. This means you’ll need two
backslashes to represent a single literal backslash escape character in Snowflake queries.
SnowConvert AI handles this by automatically escaping the backslash for you.

### Sample Source Patterns[¶](#id3)

Success

This syntax is fully supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

#### Vertica[¶](#vertica)

```
 SELECT path_name
FROM file_paths
WHERE path_name ~~ '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\%%';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKEB 'C:\\%' ESCAPE'\';
```

Copy

#### Snowflake[¶](#snowflake)

```
SELECT path_name
FROM file_paths
WHERE path_name LIKE '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\\%%' ESCAPE'\\';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKE 'C:\\\\%' ESCAPE'\\';
```

Copy

#### Known Issues[¶](#id4)

While SnowConvert AI handles most backslash patterns, some **complex expressions** may still cause
**query failures**. We recommend reviewing complex patterns to prevent these issues.

#### Related EWIs[¶](#id5)

There are no related EWIs.
