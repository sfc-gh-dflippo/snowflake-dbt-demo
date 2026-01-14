---
description:
  BigQuery quoted identifiers are enclosed by backticks (`) while Snowflake encloses them in double
  quotes (“).
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-identifiers
title: SnowConvert AI - BigQuery - Identifier differences between BigQuery and Snowflake
---

## Quoted identifiers[¶](#quoted-identifiers)

BigQuery quoted identifiers are enclosed by backticks (`) while Snowflake encloses them in double
quotes (“).

In BigQuery, quoted identifiers stick to the
[case sensitivity rules](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#case_sensitivity),
which means that, for example, column names are still case insensitive even when quoted:

### BigQuery[¶](#bigquery)

```
CREATE TABLE test.quotedIdentTable
(
  `col#1` INTEGER
);

SELECT `col#1` FROM test.quotedIdentTable;

SELECT `COL#1` FROM test.quotedIdentTable;
```

In Snowflake, case sensitivity of quoted identifiers depends on the session parameter
[QUOTED_IDENTIFIERS_IGNORE_CASE](https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case),
by default quoted identifiers comparison is case sensitive, this means that the result code from
migrating the above example:

### Snowflake[¶](#snowflake)

```
CREATE TABLE test.quotedIdentTable
(
  "col#1" INTEGER
);

SELECT
  "col#1"
FROM
  test.quotedIdentTable;

SELECT
  "COL#1"
FROM
  test.quotedIdentTable;
```

Will fail when executing the second select unless the session parameter is set to TRUE.

## How SnowConvert AI migrates quoted identifiers[¶](#how-snowconvert-ai-migrates-quoted-identifiers)

SnowConvert AI will analyze quoted identifiers to determine if they contain non-alphanumeric
characters or are reserved words in Snowflake, if they do then it will transform them to quoted
identifiers in Snowflake, alphanumeric identifiers will be left unquoted:

### BigQuery[¶](#id1)

```
CREATE TABLE `test.identsTable1`
(
  `col#1` INTEGER,
  `col2` INTEGER
);

-- Group is a reserved word
SELECT
`col#1` AS `group`,
`col2`AS `hello`
FROM
`test.identsTable1`;
```

### Snowflake[¶](#id2)

```
CREATE TABLE test.identsTable1
(
  "col#1" INTEGER,
  col2 INTEGER
);

-- Group is a reserved word
SELECT
  "col#1" AS "group",
  col2 AS hello
FROM
  test.identsTable1;
```

## Known issues[¶](#known-issues)

By default, BigQuery considers table and dataset names as case sensitive, unless the
[is_case_insensitive](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#schema_option_list)
option is activated for the dataset, this allows the following tables to coexist without problems:

### BigQuery[¶](#id3)

```
CREATE TABLE test.myTable
(
  col1 INTEGER
);

CREATE TABLE test.MyTable
(
  col1 INTEGER
);
```

However, unquoted identifiers in Snowflake are
[always stored and compared in uppercase](https://docs.snowflake.com/en/sql-reference/identifiers-syntax),
meaning that `test.MyTable` will raise a duplicated object error when trying to create it.
SnowConvert AI also works under the assumption that identifiers are case insensitive, so when one of
these scenarios appears during transformation, SSC-FDM-0019 will be generated to warn the user:

### Snowflake[¶](#id4)

```
CREATE TABLE test.myTable
(
  col1 INTEGER
);

--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR test.MyTable. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE TABLE test.MyTable
(
  col1 INTEGER
);
```

## Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0019](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0019):
   Semantic information could not be loaded
