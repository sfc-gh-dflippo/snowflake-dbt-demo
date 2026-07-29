---
description:
  In PostgreSQL and PostgreSQL-based languages (Greenplum, RedShift, Netezza), when comparing
  fixed-length data types (CHAR, CHARACTER, etc) or comparing fixed-length data types against
  varchar data typ
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/postgresql-string-comparison
title: SnowConvert AI - PostgreSQL - String Comparison | Snowflake Documentation
---

## Sample Source Patterns

Let’s use the following script data to explain string comparison.

```sql
create table table1(c1 char(2), c2 char(2), c3 VARCHAR(2), c4 VARCHAR(2));

insert into table1 values ('a','a ','a','a ');

insert into table1 values ('b','b','b','b');
```

### NULLIF

#### Varchar Data Type

Input Code:

##### PostgreSQL

```sql
SELECT NULLIF(c3,c4) FROM table1;
```

Output Code:

##### Snowflake

```sql
SELECT
NULLIF(c3,c4) FROM
table1;
```

#### Char Data Types

Input Code:

##### PostgreSQL 2

```sql
select nullif(c1,c2) AS case2 from table1;
```

Output Code:

##### Snowflake 2

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
select
nullif(c1,c2) AS case2 from
table1;
```

### GREATEST or LEAST

Input Code:

#### PostgreSQL 3

```sql
select '"' || greatest(c1, c2) || '"' AS greatest, '"' || least(c1, c2) || '"' AS least from table1;
```

Output Code:

##### Snowflake 3

```sql
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table1" **
select '"' || GREATEST_IGNORE_NULLS(c1, c2) || '"' AS greatest, '"' || LEAST_IGNORE_NULLS(c1, c2) || '"' AS least from
table1;
```
