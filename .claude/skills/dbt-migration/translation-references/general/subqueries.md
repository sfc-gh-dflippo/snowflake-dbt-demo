---
description:
  A subquery is a query within another query. Subqueries in a FROM or WHERE clause are used to
  provide data that will be used to limit or compare/evaluate the data returned by the containing
  query. (Sno
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/general/subqueries
title: SnowConvert AI - ANSI SQL - Subqueries | Snowflake Documentation
---

## Description[¶](#description)

> A subquery is a query within another query. Subqueries in a
> [FROM](https://docs.snowflake.com/en/sql-reference/constructs/from) or
> [WHERE](https://docs.snowflake.com/en/sql-reference/constructs/where) clause are used to provide
> data that will be used to limit or compare/evaluate the data returned by the containing query.
> ([Snowflake subqueries documentation](https://docs.snowflake.com/en/user-guide/querying-subqueries)).

Subqueries can be correlated/uncorrelated as well as scalar/non-scalar.

**Correlated subqueries** reference columns from the outer query. In Snowflake, correlated
subqueries execute for each row in the query. On the other hand, **Uncorrelated subqueries** do not
reference the outer query and are executed once for the entire query.

**Scalar subqueries** return a single value as result, otherwise the subquery is **non-scalar.**

The following patterns are based on these categories.

## Sample Source Patterns[¶](#sample-source-patterns)

### Setup data[¶](#setup-data)

#### Teradata[¶](#teradata)

```
CREATE TABLE tableA
(
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE TABLE tableB
(
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey');
INSERT INTO tableA VALUES (20, 'Example');

INSERT INTO tableB VALUES (50, 'Hey');
INSERT INTO tableB VALUES (20, 'Bye');
```

#### _Snowflake_[¶](#snowflake)

```
CREATE OR REPLACE TABLE tableA
(
    col1 INTEGER,
    col2 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/02/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE tableB
(
    col3 INTEGER,
    col4 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/02/2024",  "domain": "test" }}'
;

INSERT INTO tableA
VALUES (50, 'Hey');

INSERT INTO tableA
VALUES (20, 'Example');

INSERT INTO tableB
VALUES (50, 'Hey');

INSERT INTO tableB
VALUES (20, 'Bye');
```

### Correlated Scalar subqueries[¶](#correlated-scalar-subqueries)

Snowflake evaluates correlated subqueries **at compile time** to determine if they are scalar and
therefore valid in the context were a single return value is expected. To solve this, the ANY_VALUE
aggregate function is added to the returned column when the result is not an aggregate function.
This allows the compiler to determine a single value return is expected. Since scalar subqueries are
expected to return a single value the function ANY_VALUE will not change the result, it will just
return the original value as is.

#### _Teradata_[¶](#id1)

```
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB WHERE col2 = col4);
```

#### Results[¶](#results)

```
+------+
<!-- prettier-ignore -->
|col2|
+------+
<!-- prettier-ignore -->
|Hey|
+------+
```

#### _Snowflake_[¶](#id2)

```
SELECT
    col2
FROM
    tableA
WHERE col1 =
             --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
             (
                 SELECT
                     ANY_VALUE(col3) FROM
                     tableB
                 WHERE
                     RTRIM( col2) = RTRIM(col4));
```

#### Results[¶](#id3)

```
+------+
<!-- prettier-ignore -->
|col2|
+------+
<!-- prettier-ignore -->
|Hey|
+------+
```

### Uncorrelated Scalar subqueries[¶](#uncorrelated-scalar-subqueries)

Snowflake fully supports uncorrelated scalar subqueries.

#### _Teradata_[¶](#id4)

```
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avgTableB
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

#### Results[¶](#id5)

```
+------+-----------+
<!-- prettier-ignore -->
|col2|avgTableB|
+------+-----------+
<!-- prettier-ignore -->
|Hey|35|
+------+-----------+
```

#### _Snowflake_[¶](#id6)

```
SELECT
    col2,
    (
                 SELECT
                     AVG(col3) FROM
                     tableB
    ) AS avgTableB
            FROM
    tableA
            WHERE col1 = (
                 SELECT
                     MAX(col3) FROM
                     tableB
    );
```

#### Results[¶](#id7)

```
+------+-----------+
<!-- prettier-ignore -->
|col2|avgTableB|
+------+-----------+
<!-- prettier-ignore -->
|Hey|35.000000|
+------+-----------+
```

### Non-scalar subqueries[¶](#non-scalar-subqueries)

Non-scalar subqueries specified inside subquery operators (ANY/ALL/IN/EXISTS) are supported.

Non-scalar subqueries used as derived tables are also supported.

#### _Teradata_[¶](#id8)

```
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

SELECT col2
FROM tableA
WHERE col1 >= ALL(SELECT col3 FROM tableB);

SELECT col2, myDerivedTable.col4
FROM tableA, (SELECT * FROM tableB) AS myDerivedTable
WHERE col1 = myDerivedTable.col3;
```

#### Result[¶](#result)

```
+---------+
<!-- prettier-ignore -->
|col2|
+---------+
<!-- prettier-ignore -->
|Example|
+---------+
<!-- prettier-ignore -->
|Hey|
+---------+

+---------+
<!-- prettier-ignore -->
|col2|
+---------+
<!-- prettier-ignore -->
|Hey|
+---------+

+---------+------+
<!-- prettier-ignore -->
|col2|col4|
+---------+------+
<!-- prettier-ignore -->
|Example|Bye|
+---------+------+
<!-- prettier-ignore -->
|Hey|Hey|
+---------+------+
```

#### _Snowflake_[¶](#id9)

```
SELECT
    col2
            FROM
    tableA
            WHERE col1 IN (
                 SELECT
                     col3 FROM
                     tableB
    );

                     SELECT
    col2
            FROM
    tableA
            WHERE col1 >= ALL(
                 SELECT
                     col3 FROM
                     tableB
    );
                    SELECT
    col2,
    myDerivedTable.col4
            FROM
    tableA, (
                 SELECT
                     * FROM
                     tableB
    ) AS myDerivedTable
            WHERE col1 = myDerivedTable.col3;
```

#### Results[¶](#id10)

```
+---------+
<!-- prettier-ignore -->
|col2|
+---------+
<!-- prettier-ignore -->
|Example|
+---------+
<!-- prettier-ignore -->
|Hey|
+---------+

+---------+
<!-- prettier-ignore -->
|col2|
+---------+
<!-- prettier-ignore -->
|Hey|
+---------+

+---------+------+
<!-- prettier-ignore -->
|col2|col4|
+---------+------+
<!-- prettier-ignore -->
|Example|Bye|
+---------+------+
<!-- prettier-ignore -->
|Hey|Hey|
+---------+------+
```

## Known Issues[¶](#known-issues)

**1. Subqueries with FETCH first that are not uncorrelated scalar**

Oracle allows using the FETCH clause in subqueries, Snowflake only allows using this clause if the
subquery is uncorrelated scalar, otherwise an exception will be generated.

SnowConvert AI will mark any inalid usage of FETCH in subqueries with
[SSC-EWI-0108](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0108)

Oracle:

```
-- Correlated scalar
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB WHERE col3 = col1 FETCH FIRST ROW ONLY);

-- Uncorrelated scalar
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB FETCH FIRST ROW ONLY);
```

Snowflake:

```
-- Correlated scalar
SELECT col2
FROM
    tableA
    WHERE col2 =
                 --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (SELECT
                         ANY_VALUE( col4) FROM
                         tableB
                     WHERE col3 = col1
                     FETCH FIRST 1 ROW ONLY);

 -- Uncorrelated scalar
SELECT col2
FROM
    tableA
    WHERE col2 = (SELECT col4 FROM
                         tableB
                     FETCH FIRST 1 ROW ONLY);
```

## Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0002):
   Correlated subquery may have functional differences
2. [SSC-EWI-0108](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0108):
   The following subquery matches at least one of the patterns considered invalid and may produce
   compilation errors
