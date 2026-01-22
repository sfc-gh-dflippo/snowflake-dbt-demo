---
description:
  In this section, you could find information about Oracle Views and their Snowflake equivalent. The
  syntax of subquery used to create the view can be found in the SELECT section
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create-view
title: SnowConvert AI - Oracle - Create View | Snowflake Documentation
---

## Create View

```sql
CREATE OR REPLACE VIEW View1 AS SELECT Column1 from Schema1.Table1;
```

```sql
CREATE OR REPLACE VIEW View1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT Column1 from
Schema1.Table1;
```

The following clauses for Create View are removed:

- No Force/ Force
- Edition Clause
- Sharing Clause
- Default collation
- Bequeath clause
- Container clause

```sql
CREATE OR REPLACE
NO FORCE
NONEDITIONABLE
VIEW Schema1.View1
SHARING = DATA
DEFAULT COLLATION Collation1
BEQUEATH CURRENT_USER
AS SELECT Column1 from Schema1.Table1
CONTAINER_MAP;
```

```sql
CREATE OR REPLACE VIEW Schema1.View1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT Column1 from
Schema1.Table1;
```

## Alter View

Alter is not supported by SnowConvert AI yet.

## Drop View

The CASCADE CONSTRAINT clause is not supported yet.

```sql
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS;
```

```sql
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'DropBehavior' NODE ***/!!!;
```

### Related EWIs

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
