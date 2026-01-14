---
description: Translation spec for Transact-SQL System Tables
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-system-tables
title: SnowConvert AI - SQL Server-Azure Synapse - System Tables | Snowflake Documentation
---

## System tables[¶](#system-tables)

<!-- prettier-ignore -->
|Transact-SQL|Snowflake SQL|Notes||
|---|---|---|---|
|SYS.ALL_VIEWS|INFORMATION_SCHEMA.VIEWS|||
|SYS.ALL_COLUMNS|INFORMATION_SCHEMA.COLUMNS|||
|SYS.COLUMNS|INFORMATION_SCHEMA.COLUMNS|||
|SYS.OBJECTS|INFORMATION_SCHEMA.OBJECT_PRIVILEGES|||
|SYS.PROCEDURES|INFORMATION_SCHEMA.PROCEDURES|||
|SYS.SEQUENCES|INFORMATION_SCHEMA.SEQUENCES|||
|SYS.ALL_OBJECTS|INFORMATION_SCHEMA.OBJECT_PRIVILEGES|||
|ALL_PARAMETERS|**Not supported**|||
|SYS.ALL_SQL_MODULES|**Not supported**|||
|SYS.ALLOCATION_UNITS|**Not supported**|||
|SYS.ASSEMBLY_MODULES|**Not supported**|||
|SYS.CHECK_CONSTRAINTS|**Not supported**|||
|SYS.COLUMN_STORE_DICTIONARIES|**Not supported**|||
|SYS.COLUMN_STORE_ROW_GROUPS|**Not supported**|||
|SYS.COLUMN_STORE_SEGMENTS|**Not supported**|||
|SYS.COMPUTED_COLUMNS|**Not supported**|||
|SYS.DEFAULT_CONSTRAINTS|**Not supported**|||
|SYS.EVENTS|**Not supported**|||
|SYS.EVENT_NOTIFICATIONS|**Not supported**|||
|SYS.EVENT_NOTIFICATION_EVENT_TYPES|**Not supported**|||
|SYS.EXTENDED_PROCEDURES|**Not supported**|||
|SYS.EXTERNAL_LANGUAGE_FILES|**Not supported**|||
|SYS.EXTERNAL_LANGUAGES|**Not supported**|||
|SYS.EXTERNAL_LIBRARIES|**Not supported**|||
|SYS.EXTERNAL_LIBRARY_FILES|**Not supported**|||
|SYS.FOREIGN_KEYS|INFORMATION_SCHEMA.TABLE_CONSTRAINTS|||
|SYS.FOREIGN_KEY_COLUMNS|**Not supported**|||
|SYS.FUNCTION_ORDER_COLUMNS|**Not supported**|||
|SYS.HASH_INDEXES|**Not supported**|||
|SYS.INDEXES|**Not supported**|||
|SYS.INDEX_COLUMNS|**Not supported**|||
|SYS.INDEX_RESUMABLE_OPERATIONS|**Not supported**|||
|SYS.INTERNAL_PARTITIONS|**Not supported**|||
|SYS.INTERNAL_TABLES|**Not supported**|||
|SYS.KEY_CONSTRAINTS|**Not supported**|||
|SYS.MASKED_COLUMNS|**Not supported**|||
|SYS.MEMORY_OPTIMIZED_TABLES_INTERNAL_ATTRIBUTES|**Not supported**|||
|SYS.MODULE_ASSEMBLY_USAGES|**Not supported**|||
|SYS.NUMBERED_PROCEDURES|**Not supported**|||
|SYS.NUMBERED_PROCEDURE_PARAMETERS|**Not supported**|||
|SYS.PARAMETERS|**Not supported**|||
|SYS.PARTITIONS|**Not supported**|||
|SYS.PERIODS|**Not supported**|||
|SYS.SERVER_ASSEMBLY_MODULES|**Not supported**|||
|SYS.SERVER_EVENTS|**Not supported**|||
|SYS.SERVER_EVENTT_NOTIFICATIONS|**Not supported**|||
|SYS.SERVER_SQL_MODULE|**Not supported**|||
|SYS.SERVER_TRIGGERS|**Not supported**|||
|SYS.\_SERVER_TRIGGER_EVENTS|**Not supported**|||
|SYS.SQL_DEPENDENCIES|**Not supported**|||
|SYS.SQL_EXPRESSION_DEPENDENCIES|**Not supported**|||
|SYS.SQL_MODULES|**Not supported**|||
|SYS.STATS|**Not supported**|||
|SYS.STATS_COLUMNS|**Not supported**|||
|SYS.SYNONYMS|**Not supported**|||
|SYS.SYSTEM_COLUMNS|**Not supported**|||
|SYS.SYSTEM_OBJECTS|**Not supported**|||
|SYS.SYSTEM_PARAMETERS|**Not supported**|||
|SYS.SYSTEM_SQL_MODULES”|**Not supported**|||

## SYS.FOREIGN_KEYS[¶](#sys-foreign-keys)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#description)

Contains a row per object that is a FOREIGN KEY constraint
([SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16)).

The columns for **FOREIGN KEY** (sys.foreign_keys) are the following:

<!-- prettier-ignore -->
|Column name|Data type|Description|Has equivalent column in Snowflake|
|---|---|---|---|
||-|For a list of columns that this view inherits, see [sys.objects (Transact-SQL).](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16)|Partial|
|referenced_object_id|int|ID of the referenced object.|No|
|key_index_id|int|ID of the key index within the referenced object.|No|
|is_disabled|bit|FOREIGN KEY constraint is disabled.|No|
|is_not_for_replication|bit|FOREIGN KEY constraint was created by using the NOT FOR REPLICATION option.|No|
|is_not_trusted|bit|FOREIGN KEY constraint has not been verified by the system.|No|
|delete_referential_action|tinyint|The referential action that was declared for this FOREIGN KEY when a delete happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16).|No|
|delete_referential_action_desc|nvarchar(60)|Description of the referential action that was declared for this FOREIGN KEY when a delete occurs. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16).|No|
|update_referential_action|tinyint|The referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16).|No|
|update_referential_action_desc|nvarchar(60)|Description of the referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16).|No|
|is_system_named|bit|1 = Name was generated by the system. 0 = Name was supplied by the user.|No|

The inherited columns from **sys.objects** are the following:

For more information, review the
[sys.objects documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16).

<!-- prettier-ignore -->
|Column name|Data type|Description|Has equivalent column in Snowflake|
|---|---|---|---|
|name|sysname|Object name.|Yes|
|object_id|int|Object identification number. Is unique within a database.|No|
|principal_id|int|ID of the individual owner, if different from the schema owner.|No|
|schema_id|int|ID of the schema that the object is contained in.|No|
|parent_object_id|int|ID of the object to which this object belongs.|No|
|type|char(2)|Object type|Yes|
|type_desc|nvarchar(60)|Description of the object type|Yes|
|create_date|datetime|Date the object was created.|Yes|
|modify_date|datetime|Date the object was last modified by using an ALTER statement.|Yes|
|is_ms_shipped|bit|Object is created by an internal SQL Server component.|No|
|is_published|bit|Object is created by an internal SQL Server component.|No|
|is_schema_published|bit|Only the schema of the object is published.|No|

Warning

Notice that, in this case, for the sys.foreign_keys, there is no equivalence in Snowflake. But, the
equivalence is made under the columns inherited from sys.objects.

#### Applicable column equivalence[¶](#applicable-column-equivalence)

<!-- prettier-ignore -->
|SQLServer|Snowflake|Limitations|Applicable|
|---|---|---|---|
|name|CONSTRAINT_NAME|Names auto-generated by the database may be reviewed to the target Snowflake auto-generated name,|Yes|
|type|CONSTRAINT_TYPE|The type column has a variety of options. But, in this case, the support is only for the letter ‘F’ which represents the foreign keys.|No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable.|
|type_desc|CONSTRAINT_TYPE|No limitions found.|No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable.|
|create_date|CREATED|Data type differences.|Yes|
|modify_date|LAST_ALTERED|Data type differences.|Yes|
|parent_object_id|CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA, TABLE_NAME|Columns are generated only for the cases that use the OBJECT_ID() function and, the name has a valid pattern.|Yes|

##### Syntax in SQL Server[¶](#syntax-in-sql-server)

```
SELECT ('column_name' | * )
FROM sys.foreign_keys;
```

##### Syntax in Snowflake[¶](#syntax-in-snowflake)

```
SELECT ('column_name' | * )
FROM information_schema.table_constraints
WHERE CONSTRAINT_TYPE = 'FOREIGN KEY';
```

**Note:**

Since the equivalence for the system foreign keys is the catalog view in Snowflake for in
ormation_schema.table_constraints, it is necessary to define the type of the constraint in an
additional ‘WHERE’ clause to identify foreign key constraints from other constraints.

### Sample Source Patterns[¶](#sample-source-patterns)

To accomplish correctly the following samples, it is required to run the following statements:

#### SQL Server[¶](#sql-server)

```
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

CREATE OR REPLACE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
   )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

#### 1. Simple Select Case[¶](#simple-select-case)

##### SQL Server[¶](#id1)

```
SELECT *
FROM sys.foreign_keys;
```

##### Result[¶](#result)

<!-- prettier-ignore -->
|name|object_id|principal_id|schema_id|type|type_desc|create_date|modify_date|parent_object_id|is_ms_shipped|is_published|is_schema_published|referenced_object_id|key_index_id|is_disabled|is_not_for_replication|is_not_trusted|delete_referential_action|delete_referential_action_desc|update_referential_action|update_referential_action_desc|is_system_named|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FK_Name_Test|1719677174|NULL|1|F|FOREIGN_KEY_CONSTRAINT|2023-09-11 22:20:04.160|2023-09-11 22:20:04.160|1687677060|false|true|false|1655676946|1|false|false||0|NO_ACTION|0|NO_ACTION|true|

##### Snowflake[¶](#id2)

```
SELECT *
FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id3)

<!-- prettier-ignore -->
|CONSTRAINT_CATALOG|CONSTRAINT_SCHEMA|CONSTRAINT_NAME|TABLE_CATALOG|TABLE_SCHEMA|TABLE_NAME|CONSTRAINT_TYPE|IS_DEFERRABLE|INITIALLY_DEFERRED|ENFORCED|COMMENT|CREATED|LAST_ALTERED|RELY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DBTEST|PUBLIC|FK_Name_Test|DATETEST|PUBLIC|ORDERS|FOREIGN KEY|NO|YES|NO|null|2023-09-11 15:23:51.969 -0700|2023-09-11 15:23:52.097 -0700|NO|

Warning

Results differ due to the differences in column objects and missing equivalence. The result may be
checked.

#### 2. Name Column Case[¶](#name-column-case)

##### SQL Server[¶](#id4)

```
SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test';
```

##### Result[¶](#id5)

<!-- prettier-ignore -->
|name|object_id|principal_id|schema_id|type|type_desc|create_date|modify_date|parent_object_id|is_ms_shipped|is_published|is_schema_published|referenced_object_id|key_index_id|is_disabled|is_not_for_replication|is_not_trusted|delete_referential_action|delete_referential_action_desc|update_referential_action|update_referential_action_desc|is_system_named|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FK_Name_Test|1719677174|NULL|1|F|FOREIGN_KEY_CONSTRAINT|2023-09-11 22:20:04.160|2023-09-11 22:20:04.160|1687677060|false|true|false|1655676946|1|false|false||0|NO_ACTION|0|NO_ACTION|true|

##### Snowflake[¶](#id6)

```
SELECT * FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_NAME = 'FK_NAME_TEST'
AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id7)

<!-- prettier-ignore -->
|CONSTRAINT_CATALOG|CONSTRAINT_SCHEMA|CONSTRAINT_NAME|TABLE_CATALOG|TABLE_SCHEMA|TABLE_NAME|CONSTRAINT_TYPE|IS_DEFERRABLE|INITIALLY_DEFERRED|ENFORCED|COMMENT|CREATED|LAST_ALTERED|RELY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DBTEST|PUBLIC|FK_Name_Test|DATETEST|PUBLIC|ORDERS|FOREIGN KEY|NO|YES|NO|null|2023-09-11 15:23:51.969 -0700|2023-09-11 15:23:52.097 -0700|NO|

Warning

This translation may require verification if the constraint name is auto-generated by the database
and used in the query. For more information review the [Know Issues](#known-issues) section.

#### 3. Parent Object ID Case[¶](#parent-object-id-case)

In this example, a database and schema were created to exemplify the processing of the names to
create different and equivalent columns.

##### SQL Server[¶](#id8)

```
use database_name_test
create schema schema_name_test

CREATE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers(CustomerID)
);

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test' AND parent_object_id = OBJECT_ID(N'database_name_test.schema_name_test.Orders')
```

##### Result[¶](#id9)

<!-- prettier-ignore -->
|name|object_id|principal_id|schema_id|type|type_desc|create_date|modify_date|parent_object_id|is_ms_shipped|is_published|is_schema_published|referenced_object_id|key_index_id|is_disabled|is_not_for_replication|is_not_trusted|delete_referential_action|delete_referential_action_desc|update_referential_action|update_referential_action_desc|is_system_named|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FK_Name_Test|1719677174|NULL|1|F|FOREIGN_KEY_CONSTRAINT|2023-09-11 22:20:04.160|2023-09-11 22:20:04.160|1687677060|false|true|false|1655676946|1|false|false||0|NO_ACTION|0|NO_ACTION|true|

##### Snowflake[¶](#id10)

```
USE DATABASE database_name_test;

CREATE SCHEMA IF NOT EXISTS schema_name_test
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers (CustomerID)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_NAME = 'FK_NAME_TEST'
    AND CONSTRAINT_CATALOG = 'DATABASE_NAME_TEST'
    AND CONSTRAINT_SCHEMA = 'SCHEMA_NAME_TEST'
    AND TABLE_NAME = 'ORDERS'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id11)

<!-- prettier-ignore -->
|CONSTRAINT_CATALOG|CONSTRAINT_SCHEMA|CONSTRAINT_NAME|TABLE_CATALOG|TABLE_SCHEMA|TABLE_NAME|CONSTRAINT_TYPE|IS_DEFERRABLE|INITIALLY_DEFERRED|ENFORCED|COMMENT|CREATED|LAST_ALTERED|RELY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DATABASE_NAME_TEST|SCHEMA_NAME_TEST|FK_Name_Test|DATABASE_NAME_TEST|SCHEMA_NAME_TEST|ORDERS|FOREIGN KEY|NO|YES|NO|null|2023-09-11 15:23:51.969 -0700|2023-09-11 15:23:52.097 -0700|NO|

Warning

If the name coming inside the OBJECT_ID() function does not have a valid pattern, it will not be
converted due to name processing limitations on special characters.

Warning

Review the database that is being used in Snowflake.

#### 4. Type Column Case[¶](#type-column-case)

The ‘F’ in SQL Server means ‘Foreign Key’ and it is removed due to the validation at the ending to
specify the foreign key from all the table constraints.

##### SQL Server[¶](#id12)

```
 SELECT * FROM sys.foreign_keys WHERE type = 'F';
```

##### Result[¶](#id13)

<!-- prettier-ignore -->
|name|object_id|principal_id|schema_id|type|type_desc|create_date|modify_date|parent_object_id|is_ms_shipped|is_published|is_schema_published|referenced_object_id|key_index_id|is_disabled|is_not_for_replication|is_not_trusted|delete_referential_action|delete_referential_action_desc|update_referential_action|update_referential_action_desc|is_system_named|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FK_Name_Test|1719677174|NULL|3|F|FOREIGN_KEY_CONSTRAINT|2023-09-11 22:20:04.160|2023-09-11 22:20:04.160|1687677060|false|true|false|1655676946|1|false|false||0|NO_ACTION|0|NO_ACTION|true|

##### Snowflake[¶](#id14)

```
 SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type = 'F' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id15)

<!-- prettier-ignore -->
|CONSTRAINT_CATALOG|CONSTRAINT_SCHEMA|CONSTRAINT_NAME|TABLE_CATALOG|TABLE_SCHEMA|TABLE_NAME|CONSTRAINT_TYPE|IS_DEFERRABLE|INITIALLY_DEFERRED|ENFORCED|COMMENT|CREATED|LAST_ALTERED|RELY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DBTEST|PUBLIC|FK_Name_Test|DATETEST|PUBLIC|ORDERS|FOREIGN KEY|NO|YES|NO|null|2023-09-11 15:23:51.969 -0700|2023-09-11 15:23:52.097 -0700|NO|

#### 5. Type Desc Column Case[¶](#type-desc-column-case)

The ‘type_desc’ column is removed due to the validation at the ending to specify the foreign key
from all the table constraints.

##### SQL Server[¶](#id16)

```
SELECT
    *
FROM
    sys.foreign_keys
WHERE
    type_desc = 'FOREIGN_KEY_CONSTRAINT';
```

##### Result[¶](#id17)

<!-- prettier-ignore -->
|name|object_id|principal_id|schema_id|type|type_desc|create_date|modify_date|parent_object_id|is_ms_shipped|is_published|is_schema_published|referenced_object_id|key_index_id|is_disabled|is_not_for_replication|is_not_trusted|delete_referential_action|delete_referential_action_desc|update_referential_action|update_referential_action_desc|is_system_named|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FK_Name_Test|1719677174|NULL|3|F|FOREIGN_KEY_CONSTRAINT|2023-09-11 22:20:04.160|2023-09-11 22:20:04.160|1687677060|false|true|false|1655676946|1|false|false||0|NO_ACTION|0|NO_ACTION|true|

##### Snowflake[¶](#id18)

```
SELECT
    *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type_desc = 'FOREIGN_KEY_CONSTRAINT' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id19)

<!-- prettier-ignore -->
|CONSTRAINT_CATALOG|CONSTRAINT_SCHEMA|CONSTRAINT_NAME|TABLE_CATALOG|TABLE_SCHEMA|TABLE_NAME|CONSTRAINT_TYPE|IS_DEFERRABLE|INITIALLY_DEFERRED|ENFORCED|COMMENT|CREATED|LAST_ALTERED|RELY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DBTEST|PUBLIC|FK_Name_Test|DATETEST|PUBLIC|ORDERS|FOREIGN KEY|NO|YES|NO|null|2023-09-11 15:23:51.969 -0700|2023-09-11 15:23:52.097 -0700|NO|

#### 6. Modify Date Column Simple Case[¶](#modify-date-column-simple-case)

##### SQL Server[¶](#id20)

```
SELECT *
FROM sys.foreign_keys
WHERE modify_date = CURRENT_TIMESTAMP;
```

##### Result[¶](#id21)

```
The query produced no results.
```

##### Snowflake[¶](#id22)

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    LAST_ALTERED = CURRENT_TIMESTAMP()
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id23)

```
The query produced no results.
```

#### 7. Modify Date Column with DATEDIFF() Case[¶](#modify-date-column-with-datediff-case)

The following example shows a more complex scenario where the columns from sys.foreign_keys
(inherited from sys.objects) are inside a function DATEDIFF. In this case, the argument
corresponding to the applicable equivalence is changed to the corresponding column from the
information.schema in Snowflake.

##### SQL Server[¶](#id24)

```
SELECT *
FROM sys.foreign_keys
WHERE DATEDIFF(DAY, modify_date, GETDATE()) <= 30;
```

##### Result[¶](#id25)

```
The foreign keys altered in the last 30 days.
```

##### Snowflake[¶](#id26)

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    DATEDIFF(DAY, LAST_ALTERED, CURRENT_TIMESTAMP() :: TIMESTAMP) <= 30
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id27)

```
The foreign keys altered in the last 30 days.
```

#### 8. Create Date Column Case[¶](#create-date-column-case)

##### SQL Server[¶](#id28)

```
SELECT *
FROM sys.foreign_keys
WHERE create_date = '2023-09-12 14:36:38.060';
```

##### Result[¶](#id29)

```
The foreign keys that were created on the specified date and time.
```

##### Snowflake[¶](#id30)

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CREATED = '2023-09-12 14:36:38.060'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id31)

```
The foreign keys that were created on the specified date and time.
```

Warning

The result may change if the creation date is specific due to the time on which the queries were
executed. It is possible to execute a specified query at one time on the origin database and then
execute the objects at another time in the new Snowflake queries.

#### 9. Selected Columns Single Name Case[¶](#selected-columns-single-name-case)

##### SQL Server[¶](#id32)

```
SELECT name
FROM sys.foreign_keys;
```

##### Result[¶](#id33)

<!-- prettier-ignore -->
|name|
|---|
|FK_Name_Test|

##### Snowflake[¶](#id34)

```
SELECT
    CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id35)

<!-- prettier-ignore -->
|CONSTRAINT_NAME|
|---|
|FK_Name_Test|

#### 10. Selected Columns Qualified Name Case[¶](#selected-columns-qualified-name-case)

##### SQL Server[¶](#id36)

```
SELECT
    fk.name
FROM sys.foreign_keys AS fk;
```

##### Result[¶](#id37)

<!-- prettier-ignore -->
|name|
|---|
|FK_Name_Test|

##### Snowflake[¶](#id38)

```
SELECT
    fk.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS fk
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result[¶](#id39)

<!-- prettier-ignore -->
|CONSTRAINT_NAME|
|---|
|FK_Name_Test|

### Known Issues[¶](#known-issues)

#### 1. The ‘name’ column may not show a correct output if the constraint does not have a user-created name[¶](#the-name-column-may-not-show-a-correct-output-if-the-constraint-does-not-have-a-user-created-name)

If the referenced name is one auto-generated from the database, it would be probable to review it
and use the wanted value.

##### 2. When selecting columns, there is a limitation that depends on the applicable columns that are equivalent in Snowflake[¶](#when-selecting-columns-there-is-a-limitation-that-depends-on-the-applicable-columns-that-are-equivalent-in-snowflake)

Since the columns from sys.foreign_keys are not completely equivalent in Snowflake, some results may
change due to the limitations on the equivalence.

##### 3. The OBJECT_ID() function may have a valid pattern to be processed or the database, schema or table could not be extracted[¶](#the-object-id-function-may-have-a-valid-pattern-to-be-processed-or-the-database-schema-or-table-could-not-be-extracted)

Based on the name that receives the OBJECT_ID() function, the processing of this name will be
limited and dependent on formatting.

##### 4. Name Column With OBJECT_NAME() Function Case[¶](#name-column-with-object-name-function-case)

Since the OBJECT_NAME() function is not supported yet, the transformations related to this function
are not supported.

##### SQL Server[¶](#id40)

```
SELECT name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) AS ReferencedTable
FROM sys.foreign_keys;
```

##### Snowflake[¶](#id41)

```
SELECT
    name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencedTable
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### 5. SCHEMA_NAME() and TYPE_NAME() functions are also not supported yet.[¶](#schema-name-and-type-name-functions-are-also-not-supported-yet)

##### 6. Different Join statement types may be not supported if the system table is not supported. Review the supported system tables.[¶](#different-join-statement-types-may-be-not-supported-if-the-system-table-is-not-supported-review-the-supported-system-tables)

##### 7. Cases with JOIN statements are not supported.[¶](#cases-with-join-statements-are-not-supported)

##### 8. Names with alias AS are not supported.[¶](#names-with-alias-as-are-not-supported)

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
