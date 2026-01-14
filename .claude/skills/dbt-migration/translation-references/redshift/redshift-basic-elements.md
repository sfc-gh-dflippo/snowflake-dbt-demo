---
description: Names and identifiers translation for Redshift
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-basic-elements
title: SnowConvert AI - Redshift - Basic elements | Snowflake Documentation
---

## Names and identifiers[¶](#names-and-identifiers)

Names and identifiers translation for Redshift

### Description [¶](#description)

> Names identify database objects, including tables and columns, as well as users and passwords. The
> terms _name_ and _identifier_ can be used interchangeably. There are two types of identifiers,
> standard identifiers and quoted or delimited identifiers. Identifiers must consist of only UTF-8
> printable characters. ASCII letters in standard and delimited identifiers are case-insensitive and
> are folded to lowercase in the database.
> ([Redshift SQL Language reference Names and identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html)).

### Standard identifiers [¶](#standard-identifiers)

Standard SQL identifiers adhere to a set of rules and must:

- Begin with an ASCII single-byte alphabetic character or underscore character, or a UTF-8 multibyte
  character two to four bytes long.
- Subsequent characters can be ASCII single-byte alphanumeric characters, underscores, or dollar
  signs, or UTF-8 multibyte characters two to four bytes long.
- Be between 1 and 127 bytes in length, not including quotation marks for delimited identifiers.
- Contain no quotation marks and no spaces.
- Not be a reserved SQL keyword.
  ([Redshift SQL Language reference Standard identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html#r_names-standard-identifiers))

**Note:**

This syntax is fully supported by Snowflake.

### Special characters identifiers [¶](#special-characters-identifiers)

In Redshift, there is support for using some special characters as part of the name of the
identifier. These could be used in any part of an identifier. For this reason, to emulate this
behavior, replace these unsupported special characters with a new value valid in Snowflake.

- The **#** character is replaced by a **\_H\_**.

**Note:**

In Redshift, if you specify a table name that begins with **‘# ‘**, the table is created as a
temporary table.

#### Sample Source Patterns[¶](#sample-source-patterns)

##### Input Code:[¶](#input-code)

##### Redshift[¶](#redshift)

```
 CREATE TABLE #TABLE_NAME
(
    COL#1 int,
    "col2#" int
);

INSERT INTO #TABLE_NAME(COL#1, "col2#") VALUES (1,20),(2,21),(3,22);

SELECT col#1, "col2#" as col# FROM #TABLE_NAME;
```

##### Output Code:[¶](#output-code)

##### Snowflake[¶](#snowflake)

```
 CREATE TEMP TABLE _H_TABLE_NAME
(
	COL_H_1 int,
	"col2#" int
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/04/2025",  "domain": "test" }}';

INSERT INTO _H_TABLE_NAME (COL_H_1, "col2#") VALUES (1,20),(2,21),(3,22);

SELECT
	col_H_1,
	"col2#" as col_H_
FROM
	_H_TABLE_NAME;
```

### Delimited identifiers [¶](#delimited-identifiers)

> Delimited identifiers (**also known as quoted identifiers**) begin and end with double quotation
> marks (“). If you use a delimited identifier, you must use the double quotation marks for every
> reference to that object. The identifier can contain any standard UTF-8 printable characters other
> than the double quotation mark itself. Therefore, you can create column or table names that
> include otherwise illegal characters, such as spaces or the percent symbol.
> ([Redshift SQL Language reference Delimited identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html#r_names-delimited-identifiers)).

In Redshift, identifiers can be enclosed in quotes and are
[not case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html).
However, in Snowflake, they are
[case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html).
For this reason, to emulate this behavior, we are removing the quotes from all identifiers that are
**enclosed in quotes, are not reserved keywords in Snowflake, and contain alphanumeric characters**.
[**Reserved** **keywords**](#reserved-keywords) in Snowflake will always be enclosed in double
quotes and defined in lowercase.

Warning

This change could impact the desired behavior if the
[`enable_case_sensitive_identifier`](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html)
flag is set to true in your configuration. Future updates will allow users to define the desired
transformation for these identifiers.

#### Sample Source Patterns[¶](#id1)

For this scenario, please keep in mind that “LATERAL” and “INCREMENT” are reserved words in
Snowflake, while “LOCAL” is not a reserved word.

##### Input Code:[¶](#id2)

##### Redshift[¶](#id3)

```
 CREATE TABLE lateral
(
    INCREMENT int,
    "local" int
);

INSERT INTO lateral(INCREMENT, "local") VALUES (1,20),(2,21),(3,22);

SELECT lateral.INCREMENT, "local" FROM LATERAL;
```

##### Result[¶](#result)

<!-- prettier-ignore -->
|increment|local|
|---|---|
|1|20|
|2|21|
|3|22|

##### Output Code:[¶](#id4)

##### Snowflake[¶](#id5)

```
 CREATE TABLE "lateral"
(
    "increment" int,
    local int
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/10/2024",  "domain": "test" }}';

INSERT INTO "lateral" ("increment", local) VALUES (1,20),(2,21),(3,22);

SELECT
    "lateral"."increment",
    local
FROM
    "lateral";
```

##### Result[¶](#id6)

<!-- prettier-ignore -->
|increment|LOCAL|
|---|---|
|1|20|
|2|21|
|3|22|

### Quoted identifiers in Functions[¶](#quoted-identifiers-in-functions)

In Redshift, function names can be enclosed in quotes and are
[not case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html).
However, in Snowflake, functions may cause issues if they are in quotes and written in lowercase.
For this reason, in Snowflake, any function name enclosed in quotes will always be transformed to
uppercase and the quotation marks will be removed.

#### Sample Source Patterns[¶](#id7)

##### Input Code:[¶](#id8)

##### Redshift[¶](#id9)

```
 SELECT "getdate"();
```

##### Result[¶](#id10)

<!-- prettier-ignore -->
|“GETDATE”()|
|---|
|2024-11-21 22:08:53.000000|

##### Output Code:[¶](#id11)

##### Snowflake[¶](#id12)

```
 SELECT GETDATE();
```

##### Result[¶](#id13)

<!-- prettier-ignore -->
|“GETDATE”()|
|---|
|2024-11-21 22:08:53.000 +0000|

#### Recommendations[¶](#recommendations)

> To work around this limitation, Snowflake provides the
> [QUOTED_IDENTIFIERS_IGNORE_CASE](https://docs.snowflake.com/en/sql-reference/parameters.html#label-quoted-identifiers-ignore-case)
> session parameter, which causes Snowflake to treat lowercase letters in double-quoted identifiers
> as uppercase when creating and finding objects.
>
> ([Snowflake SQL Language Reference Identifier requirements](https://docs.snowflake.com/en/sql-reference/identifiers-syntax#migrating-from-databases-that-treat-double-quoted-identifiers-as-case-insensitive)).

## Reserved Keywords[¶](#reserved-keywords)

Reserved keywords translation for Redshift

### Description[¶](#id14)

In Redshift you can use some of the
[Snowflake reserved keywords](https://docs.snowflake.com/en/sql-reference/reserved-keywords) as
column names, table names, etc. For this reason, it is necessary that these words are enclosed in
double quotes in order to be able to use them.

**Note:**

Please be aware that in Snowflake when these names are enclosed in double quotes, they are
**case-sensitive**. For this reason It is important to emphasize that when a reserved keyword is
used in Snowflake it is always transformed with double quotes and in lowercase. For more information
please refer to
[Snowflake identifiers documentation.](https://docs.snowflake.com/en/sql-reference/identifiers-syntax#label-delimited-identifier)

### Sample Source Patterns[¶](#id15)

#### Input Code:[¶](#id16)

##### Redshift[¶](#id17)

```
 CREATE TABLE alter
(
    alter INT
);

CREATE TABLE CONNECT
(
    CONNECT INT
);

DROP TABLE alter;
DROP TABLE CONNECT;
```

##### Output Code:[¶](#id18)

##### Snowflake[¶](#id19)

```
 CREATE TABLE "alter"
(
    "alter" INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

CREATE TABLE "connect"
(
    "connect" INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

DROP TABLE "alter";
DROP TABLE "connect";
```

### Related EWIs[¶](#related-ewis)

No related EWIs.

### Known Issues [¶](#known-issues)

No issues were found.
