---
description:
  Creates a new view in the current database. You define a list of columns, which each hold data of
  a distinct type. The owner of the view is the issuer of the CREATE VIEW command.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/sybase/sybase-create-view
title: SnowConvert AI - Sybase IQ - CREATE VIEW | Snowflake Documentation
---

## Description[¶](#description)

Creates a new view in the current database. You define a list of columns, which each hold data of a
distinct type. The owner of the view is the issuer of the CREATE VIEW command.

For more information, please refer to
[`CREATE VIEW`](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a61a051684f210158cced2d83231bd8a.html?version=16.1.5.0&locale=en-US)
documentation.

## Grammar Syntax [¶](#grammar-syntax)

```
 CREATE [ OR REPLACE ] VIEW
   … [ owner.]view-name [ ( column-name [ , … ] ) ]
   … AS select-without-order-by
   … [ WITH CHECK OPTION ]
```

## Sample Source Patterns[¶](#sample-source-patterns)

### Input Code:[¶](#input-code)

#### Sybase[¶](#sybase)

```
 CREATE OR REPLACE VIEW VIEW1
AS
SELECT
COL1, COL2
FROM T1
WITH CHECK OPTION;
```

#### Output Code:[¶](#output-code)

##### Snowflake[¶](#snowflake)

```
 CREATE OR REPLACE VIEW VIEW1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "04/15/2025",  "domain": "test" }}'
AS
SELECT
COL1,
COL2
FROM
T1;
```
