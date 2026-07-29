---
description:
  Returns rows from tables, views, and user-defined functions. (Redshift SQL Language Reference
  SELECT statement)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/rs-sql-statements-select
title: SnowConvert AI - Redshift - SELECT | Snowflake Documentation
---

## SELECT

### Description

Returns rows from tables, views, and user-defined functions.
([Redshift SQL Language Reference SELECT statement](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html))

### Grammar Syntax

```sql
 [ WITH with_subquery [, ...] ]
SELECT
[ TOP number | [ ALL | DISTINCT ]
* | expression [ AS output_name ] [, ...] ]
[ FROM table_reference [, ...] ]
[ WHERE condition ]
[ [ START WITH expression ] CONNECT BY expression ]
[ GROUP BY expression [, ...] ]
[ HAVING condition ]
[ QUALIFY condition ]
[ { UNION | ALL | INTERSECT | EXCEPT | MINUS } query ]
[ ORDER BY expression [ ASC | DESC ] ]
[ LIMIT { number | ALL } ]
[ OFFSET start ]
```

For more information please refer to each of the following links:
