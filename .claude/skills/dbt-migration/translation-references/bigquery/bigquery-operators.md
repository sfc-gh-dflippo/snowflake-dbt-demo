---
description:
  IS operators return TRUE or FALSE for the condition they are testing. They never return NULL, even
  for NULL inputs. (BigQuery SQL Language Reference IS operators)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-operators
title: SnowConvert AI - BigQuery - Operators | Snowflake Documentation
---

## IS operators[¶](#is-operators)

IS operators return `TRUE` or `FALSE` for the condition they are testing. They never return `NULL`,
even for `NULL` inputs.
([BigQuery SQL Language Reference IS operators](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=en#is_operators))

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|`X IS TRUE`|`NVL(X, FALSE)`|
|`X IS NOT TRUE`|`NVL(NOT X, TRUE)`|
|`X IS FALSE`|`NVL(NOT X, FALSE)`|
|`X IS NOT FALSE`|`NVL(X, TRUE)`|
|`X IS NULL`|`X IS NULL`|
|`X IS NOT NULL`|`X IS NOT NULL`|
|`X IS UNKNOWN`|`X IS NULL`|
|`X IS NOT UNKNOWN`|`X IS NOT NULL`|

## UNNEST operator[¶](#unnest-operator)

The UNNEST operator takes an array and returns a table with one row for each element in the array.
([BigQuery SQL Language Reference UNNEST operator](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#unnest_operator)).

This operator will be emulated using the [FLATTEN](../../../../sql-reference/functions/flatten)
function, the `VALUE` and `INDEX` columns returned by the function will be renamed accordingly to
match the UNNEST operator aliases

<!-- prettier-ignore -->
|BigQuery|Snowflake|
|---|---|
|`UNNEST(arrayExpr)`|`FLATTEN(INPUT => arrayExpr) AS F0_(SEQ, KEY, PATH, INDEX, F0_, THIS)`|
|`UNNEST(arrayExpr) AS alias`|`FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, INDEX, alias, THIS)`|
|`UNNEST(arrayExpr) AS alias WITH OFFSET`|`FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, OFFSET, alias, THIS)`|
|`UNNEST(arrayExpr) AS alias WITH OFFSET AS offsetAlias`|`FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, offsetAlias, alias, THIS)`|

### SELECT \* with UNNEST[¶](#select-with-unnest)

When the UNNEST operator is used inside a SELECT \* statement the `EXCLUDE` keyword will be used to
remove the unnecessary FLATTEN columns.

Input:

```
SELECT * FROM UNNEST ([10,20,30]) AS numbers WITH OFFSET position;
```

Generated code:

```
 SELECT
* EXCLUDE(SEQ, KEY, PATH, THIS)
FROM
TABLE(FLATTEN(INPUT => [10,20,30])) AS numbers (
SEQ,
KEY,
PATH,
position,
numbers,
THIS
);
```
