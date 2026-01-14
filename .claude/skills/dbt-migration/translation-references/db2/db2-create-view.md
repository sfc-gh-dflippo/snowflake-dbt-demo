---
description: The CREATE VIEW statement defines a view on one or more tables, views or nicknames.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-view
title: SnowConvert AI - IBM DB2 - CREATE VIEW | Snowflake Documentation
---

## Description[¶](#description)

> The CREATE VIEW statement defines a view on one or more tables, views or nicknames.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view) to navigate to the
IBM DB2 documentation page for this syntax.

## Grammar Syntax[¶](#grammar-syntax)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_view_overview.png)

Navigate to the following pages to get more details about the translation spec for the subsections
of the CREATE VIEW grammar.

## Examples of Supported Create Views[¶](#examples-of-supported-create-views)

In order to test a CREATE VIEW, we need a Table with some values. Let’s look at the following code
for a table with some inserts.

```
 CREATE TABLE PUBLIC.TestTable
(
	ID INT,
	NAME VARCHAR(10)
);

Insert into TestTable Values(1,'MARCO');
Insert into TestTable Values(2,'ESTEBAN');
Insert into TestTable Values(3,'JEFF');
Insert into TestTable Values(4,'OLIVER');
```

Now that we have a Table with some data, we can do a couple of examples about a Create View.

### IBM DB2[¶](#ibm-db2)

```
CREATE VIEW ViewTest1 AS
SELECT *
FROM TestTable
WHERE ID > 2;
```

### Snowflake[¶](#snowflake)

```
CREATE VIEW ViewTest1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS SELECT *  FROM
 TestTable
WHERE ID > 2;
```

## OF type-name[¶](#of-type-name)

### Description[¶](#id1)

> Specifies that the columns of the view are based on the attributes of the structured type
> identified by type-name.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_type-name)
to navigate to the IBM DB2 documentation page for this syntax.

CREATE VIEW OF type-name is not supported in Snowflake.

### Grammar Syntax

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_view_of_type_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_view_of_type_syntax_2.png)

### Sample Source Patterns

#### IBM DB2

```
CREATE VIEW ViewTest2
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM TestTable;
```

##### Snowflake

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0015 - CREATE VIEW OF TYPE IS NOT SUPPORTED ***/!!!
 CREATE VIEW ViewTest2
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM TestTable;
```

### Related EWIs

1. [SSC-EWI-DB0015](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   CREATE VIEW OF TYPE IS NOT SUPPORTED

## WITH CHECK OPTION

### Description

> Specifies the constraint that every row that is inserted or updated through the view must conform
> to the definition of the view. A row that does not conform to the definition of the view is a row
> that does not satisfy the search conditions of the view.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_cascaded)
to navigate to the IBM DB2 documentation page for this syntax.

WITH CHECK OPTION is not supported in Snowflake.

### Grammar Syntax[¶](#id6)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_view_check_option_syntax.png)

### Sample Source Patterns[¶](#id7)

#### IBM DB2[¶](#id8)

```
CREATE VIEW ViewTest3 AS
Select * from TestTable
WITH CASCADED CHECK OPTION;
```

##### Snowflake[¶](#id9)

```
CREATE VIEW ViewTest3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS
Select * from
 TestTable;
```

## WITH ROW MOVEMENT[¶](#with-row-movement)

### Description[¶](#id10)

> Specifies the action to take for an updatable UNION ALL view when a row is updated in a way that
> violates a check constraint on the underlying table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_with_no_row_movement)
to navigate to the IBM DB2 documentation page for this syntax.

WITH ROW MOVEMENT is not supported in Snowflake.

### Grammar Syntax

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_view_row_movement_syntax.png)

### Sample Source Patterns

#### IBM DB2

```
CREATE VIEW ViewTest4
AS Select *
from TestTableId1
WITH ROW MOVEMENT;
```

##### Snowflake

```
CREATE VIEW ViewTest4
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS Select *
from
 TestTableId1
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0005 - MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED. ***/!!!
WITH ROW MOVEMENT;
```

### Related EWIs

1. [SSC-EWI-DB0005](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0005):
   MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED
