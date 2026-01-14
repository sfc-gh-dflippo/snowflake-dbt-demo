---
description:
  In this section, you could find information about Oracle Views and their Snowflake equivalent. The
  syntax of subquery used to create the view can be found in the SELECT section
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create-view
title: SnowConvert AI - Oracle - Create View | Snowflake Documentation
---

## Create View[¶](#create-view)

```
CREATE OR REPLACE VIEW View1 AS SELECT Column1 from Schema1.Table1;
```

```
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

```
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

```
CREATE OR REPLACE VIEW Schema1.View1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT Column1 from
Schema1.Table1;
```

## Alter View[¶](#alter-view)

Alter is not supported by SnowConvert AI yet.

## Drop View[¶](#drop-view)

The CASCADE CONSTRAINT clause is not supported yet.

```
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS;
```

```
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'DropBehavior' NODE ***/!!!;
```

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.
