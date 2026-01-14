---
description:
  Translation reference for all the DDL statements that are preceded by the ALTER keyword.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-alter-statement
title: SnowConvert AI - SQL Server-Azure Synapse - ALTER | Snowflake Documentation
---

## TABLE[¶](#table)

### Description[¶](#description)

Modifies a table definition by altering, adding, or dropping columns and constraints. ALTER TABLE
also reassigns and rebuilds partitions, or disables and enables constraints and triggers.
(<https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql>)

## CHECK CONSTRAINT[¶](#check-constraint)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id1)

**Note:**

Some parts in the output code are omitted for clarity reasons.

When the constraint that was being added in the SQL Server code is not supported at all in
Snowflake, SnowConvert AI comments out the Check constraint statement, since it’s no longer valid.

### Sample Source Patterns[¶](#sample-source-patterns)

#### SQL Server[¶](#sql-server)

```
ALTER TABLE
    [Person].[EmailAddress] CHECK CONSTRAINT [FK_EmailAddress_Person_BusinessEntityID]
GO
```

#### Snowflake[¶](#snowflake)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
ALTER TABLE IF EXISTS Person.EmailAddress CHECK CONSTRAINT FK_EmailAddress_Person_BusinessEntityID;
```

### Known Issues[¶](#known-issues)

- 1. The invalid CHECK CONSTRAINT is commented out leaving an invalid ALTER TABLE statement.

### Related EWIs[¶](#related-ewis)

- [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
  Check statement not supported.

## ADD[¶](#add)

### Description[¶](#id2)

**Note:**

In SQL Server, the ADD clause permits multiple actions per ADD, whereas Snowflake only allows a
sequence of ADD column actions. Consequently, SnowConvert AI divides the ALTER TABLE ADD clause into
individual ALTER TABLE statements.

There is a subset of functionalities provided by the ADD keyword, allowing the addition of different
elements to the target table. These include:

- Column definition
- Computed column definition
- Table constraint
- Column set definition

## TABLE CONSTRAINT[¶](#table-constraint)

Applies to

- SQL Server

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id3)

Specifies the properties of a PRIMARY KEY, FOREIGN KEY, UNIQUE, or CHECK constraint that is part of
a new column definition added to a table by using
[ALTER TABLE](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16).
(<https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-constraint-transact-sql>)

Translation for column constraints is relatively straightforward. There are several parts of the
syntax that are not required or not supported in Snowflake.

These parts include:

- `CLUSTERED | NONCLUSTERED`
- `WITH FILLFACTOR = fillfactor`
- `WITH ( index_option [, ...n ] )`
- `ON { partition_scheme_name ( partition\_column\_name ) | filegroup | "default" }`
- `NOT FOR REPLICATION`
- `CHECK [ NOT FOR REPLICATION ]`

#### Syntax in SQL Server[¶](#syntax-in-sql-server)

```
 [ CONSTRAINT constraint_name ]
{
    { PRIMARY KEY | UNIQUE }
        [ CLUSTERED | NONCLUSTERED ]
        (column [ ASC | DESC ] [ ,...n ] )
        [ WITH FILLFACTOR = fillfactor
        [ WITH ( <index_option>[ , ...n ] ) ]
        [ ON { partition_scheme_name ( partition_column_name ... )  | filegroup | "default" } ]
    | FOREIGN KEY
        ( column [ ,...n ] )
        REFERENCES referenced_table_name [ ( ref_column [ ,...n ] ) ]
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ NOT FOR REPLICATION ]
    | CONNECTION
        ( { node_table TO node_table }
          [ , {node_table TO node_table }]
          [ , ...n ]
        )
        [ ON DELETE { NO ACTION | CASCADE } ]
    | DEFAULT constant_expression FOR column [ WITH VALUES ]
    | CHECK [ NOT FOR REPLICATION ] ( logical_expression )
}
```

#### Syntax in [**Snowflake**](https://docs.snowflake.com/en/sql-reference/sql/create-table-constraint.html#inline-unique-primary-foreign-key)[¶](#syntax-in-snowflake)

```
 inlineUniquePK ::=
  [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]

 [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

### Sample Source Patterns[¶](#id4)

#### Multiple ALTER TABLE instances[¶](#multiple-alter-table-instances)

##### SQL Server[¶](#id5)

```
 -- PRIMARY KEY
ALTER TABLE
    [Person]
ADD
    CONSTRAINT [PK_EmailAddress_BusinessEntityID_EmailAddressID] PRIMARY KEY CLUSTERED (
        [BusinessEntityID] ASC,
        [EmailAddressID] ASC
    ) ON [PRIMARY]
GO

-- FOREING KEY TO ANOTHER TABLE
ALTER TABLE
    [Person].[EmailAddress] WITH CHECK
ADD
    CONSTRAINT [FK_EmailAddress_Person_BusinessEntityID] FOREIGN KEY([BusinessEntityID]) REFERENCES [Person].[Person] ([BusinessEntityID]) ON DELETE CASCADE
GO
```

##### Snowflake[¶](#id6)

```
 -- PRIMARY KEY
ALTER TABLE Person
ADD
    CONSTRAINT PK_EmailAddress_BusinessEntityID_EmailAddressID PRIMARY KEY (BusinessEntityID, EmailAddressID);

-- FOREING KEY TO ANOTHER TABLE
ALTER TABLE Person.EmailAddress
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
WITH CHECK
ADD
    CONSTRAINT FK_EmailAddress_Person_BusinessEntityID FOREIGN KEY(BusinessEntityID) REFERENCES Person.Person (BusinessEntityID) ON DELETE CASCADE ;
```

#### DEFAULT within constraints[¶](#default-within-constraints)

##### SQL Server[¶](#id7)

```
CREATE TABLE Table1
(
   COL_VARCHAR VARCHAR,
   COL_INT INT,
   COL_DATE DATE
);

ALTER TABLE
    Table1
ADD
    CONSTRAINT [DF_Table1_COL_INT] DEFAULT ((0)) FOR [COL_INT]
GO

ALTER TABLE
    Table1
ADD
    COL_NEWCOLUMN VARCHAR,
    CONSTRAINT [DF_Table1_COL_VARCHAR] DEFAULT ('NOT DEFINED') FOR [COL_VARCHAR]
GO

ALTER TABLE
    Table1
ADD
    CONSTRAINT [DF_Table1_COL_DATE] DEFAULT (getdate()) FOR [COL_DATE]
GO
```

##### Snowflake[¶](#id8)

```
CREATE OR REPLACE TABLE Table1 (
   COL_VARCHAR VARCHAR DEFAULT ('NOT DEFINED'),
   COL_INT INT DEFAULT ((0)),
   COL_DATE DATE DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--    CONSTRAINT DF_Table1_COL_INT DEFAULT ((0)) FOR COL_INT
                                                          ;

ALTER TABLE Table1
ADD COL_NEWCOLUMN VARCHAR;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--CONSTRAINT DF_Table1_COL_VARCHAR DEFAULT ('NOT DEFINED') FOR COL_VARCHAR
                                                                        ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--    CONSTRAINT DF_Table1_COL_DATE DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP) FOR COL_DATE
                                                                                         ;
```

### Known Issues[¶](#id9)

**1. DEFAULT is only supported within** `CREATE TABLE` and `ALTER TABLE ... ADD COLUMN`

SQL Server supports defining a `DEFAULT` property within a constraint, while Snowflake only allows
that when adding the column via `CREATE TABLE` or `ALTER TABLE ... ADD COLUMN`. `DEFAULT` properties
within the `ADD CONSTRAINT` syntax are not supported and will be translated to ALTER TABLE ALTER
COLUMN.

### Related EWIs[¶](#id10)

1. [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
   Check statement not supported.
2. [SSC-EWI-0040](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040):
   Statement Not Supported.
3. [SSC-FDM-TS0020](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0020):
   Default constraint was commented out and may have been added to a table definition.

## CHECK[¶](#check)

Applies to

- SQL Server

### Description[¶](#id11)

**Note:**

Some parts in the output code are omitted for clarity reasons.

When CHECK clause is in the ALTER statement, SnowConvert AI will comments out the entire statement,
since it is not supported.

### Sample Source Patterns[¶](#id12)

#### SQL Server[¶](#id13)

```
ALTER TABLE dbo.doc_exd
ADD CONSTRAINT exd_check CHECK NOT FOR REPLICATION (column_a > 1);
```

#### Snowflake[¶](#id14)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
ALTER TABLE dbo.doc_exd
ADD CONSTRAINT exd_check CHECK NOT FOR REPLICATION (column_a > 1);
```

### Known Issues[¶](#id15)

**1.** **ALTER TABLE CHECK clause is not supported in Snowflake.**

The entire ALTER TABLE CHECK clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id16)

- [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
  Check statement not supported.

## CONNECTION[¶](#connection)

Applies to

- SQL Server

### Description[¶](#id17)

**Note:**

Some parts in the output code are omitted for clarity reasons.

When CONNECTION clause is in the ALTER statement, SnowConvert AI will comment out the entire
statement, since it is not supported.

### Sample Source Patterns[¶](#id18)

#### SQL Server[¶](#id19)

```
ALTER TABLE bought
ADD COL2 VARCHAR(32), CONSTRAINT EC_BOUGHT1 CONNECTION (Customer TO Product, Supplier TO Product)
ON DELETE NO ACTION;
```

#### Snowflake[¶](#id20)

```
ALTER TABLE bought
ADD COL2 VARCHAR(32);

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!
ALTER TABLE bought
ADD
CONSTRAINT EC_BOUGHT1 CONNECTION (Customer TO Product, Supplier TO Product)
ON DELETE NO ACTION;
```

### Known Issues[¶](#id21)

**1.** **ALTER TABLE CONNECTION clause is not supported in Snowflake.**

The entire ALTER TABLE CONNECTION clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id22)

- [SSC-EWI-0109](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0109):
  Alter Table syntax is not applicable in Snowflake.

## DEFAULT[¶](#default)

Applies to

- SQL Server

### Description[¶](#id23)

When DEFAULT clause is in the ALTER statement, SnowConvert AI will comment out the entire statement,
since it is not supported.

The only functional scenario happens when the table definition is on the same file, in this way the
default is added in the column definition.

### Sample Source Patterns[¶](#id24)

#### SQL Server[¶](#id25)

```
CREATE TABLE table1
(
  col1 integer not null,
  col2 varchar collate Latin1_General_CS,
  col3 date not null
)

ALTER TABLE table1
ADD CONSTRAINT col1_constraint DEFAULT 50 FOR col1;

ALTER TABLE table1
ADD CONSTRAINT col2_constraint DEFAULT 'hello world' FOR col2;

ALTER TABLE table1
ADD CONSTRAINT col3_constraint DEFAULT getdate() FOR col3;
```

#### Snowflake[¶](#id26)

```
CREATE OR REPLACE TABLE table1 (
  col1 INTEGER not null DEFAULT 50,
  col2 VARCHAR COLLATE 'EN-CS' DEFAULT 'hello world',
  col3 DATE not null DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col1_constraint DEFAULT 50 FOR col1
                                                  ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col2_constraint DEFAULT 'hello world' FOR col2
                                                             ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col3_constraint DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP FOR col3
                                                                                ;
```

### Known Issues[¶](#id27)

**1. ALTER TABLE DEFAULT clause is not supported in Snowflake.**

The entire ALTER TABLE DEFAULT clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id28)

1. [SSC-FDM-TS0020](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0020):
   Default constraint was commented out and may have been added to a table definition.

## FOREIGN KEY[¶](#foreign-key)

Applies to

- SQL Server

### Description[¶](#id29)

**Note:**

Some parts in the output code are omitted for clarity reasons.

Snowflake supports the grammar for Referential Integrity Constraints, and their properties to
facilitate the migration from other databases.

#### SQL Server[¶](#id30)

```
FOREIGN KEY
        ( column [ ,...n ] )
        REFERENCES referenced_table_name [ ( ref_column [ ,...n ] ) ]
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ NOT FOR REPLICATION ]
```

#### Snowflake[¶](#id31)

```
  [ FOREIGN KEY ]
  REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
  [ MATCH { FULL | SIMPLE | PARTIAL } ]
  [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
       [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

### Sample Source Patterns[¶](#id32)

#### SQL Server[¶](#id33)

```
ALTER TABLE [Tests].[dbo].[Employee]
ADD CONSTRAINT FK_Department FOREIGN KEY(DepartmentID) REFERENCES Department(DepartmentID)
ON UPDATE CASCADE
ON DELETE NO ACTION
NOT FOR REPLICATION;
```

#### Snowflake[¶](#id34)

```
ALTER TABLE Tests.dbo.Employee
ADD CONSTRAINT FK_Department FOREIGN KEY(DepartmentID) REFERENCES Department (DepartmentID)
ON UPDATE CASCADE
ON DELETE NO ACTION;
```

**Note:**

Constraints are not enforced in Snowflake, excepting NOT NULL.

Primary and Foreign Key are only used for documentation purposes more than design constraints.

## ON PARTITION[¶](#on-partition)

Applies to

- SQL Server

**Note:**

Non-relevant statement.

Warning

Notice that this statement is removed from the migration because it is a non-relevant syntax. It
means that it is not required in Snowflake.

### Description[¶](#id35)

**Note:**

Some parts in the output code are omitted for clarity reasons.

In Transact SQL Server, the `on partition` statement is used inside `alter` statements and is used
to divide the data across the database. Review more information
[here](https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes?view=sql-server-ver16).

### Sample Source Patterns[¶](#id36)

#### On Partition[¶](#id37)

Notice that in this example the `ON PARTITION` has been removed. This is because Snowflake provides
an integrated partitioning methodology. Thus, the syntax is not relevant.

##### SQL SERVER[¶](#id38)

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
ON partition_scheme_name (partition_column_name);
```

##### Snowflake[¶](#id39)

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;
```

## PRIMARY KEY[¶](#primary-key)

Applies to

- SQL Server

### Description[¶](#id40)

**Note:**

Some parts in the output code are omitted for clarity reasons.

SQL Server primary key has many clauses that are not applicable for Snowflake. So, most of the
statement will be commented out.

#### Syntax in SQL Server[¶](#id41)

```
{ PRIMARY KEY | UNIQUE }
[ CLUSTERED | NONCLUSTERED ]
(column [ ASC | DESC ] [ ,...n ] )
[ WITH FILLFACTOR = fillfactor
[ WITH ( <index_option>[ , ...n ] ) ]
[ ON { partition_scheme_name ( partition_column_name ... )  | filegroup | "default" } ]
```

#### Syntax in Snowflake[¶](#id42)

```
[ CONSTRAINT <constraint_name> ]
{ UNIQUE | PRIMARY KEY } ( <col_name> [ , <col_name> , ... ] )
[ [ NOT ] ENFORCED ]
[ [ NOT ] DEFERRABLE ]
[ INITIALLY { DEFERRED | IMMEDIATE } ]
[ ENABLE | DISABLE ]
[ VALIDATE | NOVALIDATE ]
[ RELY | NORELY ]
```

### Sample Source Patterns[¶](#id43)

Warning

Notice that `WITH FILLFACTOR` statement has been removed from the translation because it is not
relevant in Snowflake syntax.

#### SQL Server[¶](#id44)

```
ALTER TABLE Production.TransactionHistoryArchive
   ADD CONSTRAINT PK_TransactionHistoryArchive_TransactionID PRIMARY KEY
   CLUSTERED (TransactionID)
   WITH (FILLFACTOR = 75, ONLINE = ON, PAD_INDEX = ON)
   ON "DEFAULTLOCATION";
```

#### Snowflake[¶](#id45)

```
ALTER TABLE Production.TransactionHistoryArchive
   ADD CONSTRAINT PK_TransactionHistoryArchive_TransactionID PRIMARY KEY (TransactionID);
```

## COLUMN DEFINITION[¶](#column-definition)

ALTER TABLE ADD column_name

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id46)

Specifies the properties of a column that are added to a table by using
[ALTER TABLE](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16).

Adding a
[column definition](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-definition-transact-sql?view=sql-server-ver16)
in Snowflake does have some differences compared to SQL Server.

For instance, several parts of the SQL Server grammar are not required or entirely not supported by
Snowflake. These include:

- [FILESTREAM](#unsupported-clauses)
- [ROWGUIDCOL](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-definition-transact-sql?view=sql-server-ver16)
- [ENCRYPTED WITH …](#encrypted-with)
- [SPARSE](#sparse)

Additionally, a couple other parts are partially supported, and require additional work to be
implemented in order to properly emulate the original functionality. Specifically, we’re talking
about the [`MASKED WITH` property](#masked-with), which will be covered in the
[patterns section](#sample-source-patterns) of this page.

#### SQL Server[¶](#id47)

```
column_name <data_type>
[ FILESTREAM ]
[ COLLATE collation_name ]
[ NULL | NOT NULL ]
[
    [ CONSTRAINT constraint_name ] DEFAULT constant_expression [ WITH VALUES ]
    | IDENTITY [ ( seed , increment ) ] [ NOT FOR REPLICATION ]
]
[ ROWGUIDCOL ]
[ SPARSE ]
[ ENCRYPTED WITH
  ( COLUMN_ENCRYPTION_KEY = key_name ,
      ENCRYPTION_TYPE = { DETERMINISTIC | RANDOMIZED } ,
      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'
  ) ]
[ MASKED WITH ( FUNCTION = ' mask_function ') ]
[ <column_constraint> [ ...n ] ]
```

#### Snowflake[¶](#id48)

```
ADD [ COLUMN ] <col_name> <col_type>
        [ { DEFAULT <expr> | { AUTOINCREMENT | IDENTITY } [ { ( <start_num> , <step_num> ) | START <num> INCREMENT <num> } ] } ]
                            /* AUTOINCREMENT (or IDENTITY) supported only for columns with numeric data types (NUMBER, INT, FLOAT, etc.). */
                            /* Also, if the table is not empty (i.e. rows exist in the table), only DEFAULT can be altered.               */
        [ inlineConstraint ]
        [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1_name> , cond_col_1 , ... ) ] ]
```

### Sample Source Patterns[¶](#id49)

#### Basic pattern[¶](#basic-pattern)

This pattern showcases the removal of elements from the original ALTER TABLE.

##### SQL Server[¶](#id50)

```
ALTER TABLE table_name
ADD column_name INTEGER;
```

##### Snowflake[¶](#id51)

```
ALTER TABLE IF EXISTS table_name
ADD column_name INTEGER;
```

#### COLLATE[¶](#collate)

Collation allows you to specify broader rules when talking about string comparison.

##### SQL Server[¶](#id52)

```
ALTER TABLE table_name
ADD COLUMN new_column_name VARCHAR
COLLATE Latin1_General_CI_AS;
```

Since the collation rule nomenclature varies from SQL Server to Snowflake, it is necessary to make
adjustments.

##### Snowflake[¶](#id53)

```
ALTER TABLE IF EXISTS table_name
ADD COLUMN new_column_name VARCHAR COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/;
```

#### MASKED WITH[¶](#masked-with)

This pattern showcases the translation for MASKED WITH property. CREATE OR REPLACE MASKING POLICY is
inserted somewhere before the first usage, and then referenced by a SET MASKING POLICY clause.

The name of the new MASKING POLICY will be the concatenation of the name and arguments of the
original MASKED WITH FUNCTION, as seen below:

##### SQL Server[¶](#id54)

```
ALTER TABLE table_name
ALTER COLUMN column_name
ADD MASKED WITH ( FUNCTION = ' random(1, 999) ' );
```

##### Snowflake[¶](#id55)

```
--** SSC-FDM-TS0022 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER **
CREATE OR REPLACE MASKING POLICY "random_1_999" AS
(val SMALLINT)
RETURNS SMALLINT ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE UNIFORM(1, 999, RANDOM()) :: SMALLINT
END;

ALTER TABLE IF EXISTS table_name MODIFY COLUMN column_name/*** SSC-FDM-TS0021 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/  SET MASKING POLICY "random_1_999";
```

#### DEFAULT[¶](#id56)

This pattern showcases some of the basic translation scenarios for DEFAULT property.

##### SQL Server[¶](#id57)

```
ALTER TABLE table_name
ADD intcol INTEGER DEFAULT 0;

ALTER TABLE table_name
ADD varcharcol VARCHAR(20) DEFAULT '';

ALTER TABLE table_name
ADD datecol DATE DEFAULT CURRENT_TIMESTAMP;
```

##### Snowflake[¶](#id58)

```
ALTER TABLE IF EXISTS table_name
ADD intcol INTEGER DEFAULT 0;

ALTER TABLE IF EXISTS table_name
ADD varcharcol VARCHAR(20) DEFAULT '';

ALTER TABLE IF EXISTS table_name
ADD datecol DATE
                 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0078 - DEFAULT OPTION NOT ALLOWED IN SNOWFLAKE ***/!!!
                 DEFAULT CURRENT_TIMESTAMP;
```

#### ENCRYPTED WITH[¶](#encrypted-with)

This pattern showcases the translation for ENCRYPTED WITH property, which is commented out in the
output code.

##### SQL Server[¶](#id59)

```
ALTER TABLE table_name
ADD encryptedcol VARCHAR(20)
ENCRYPTED WITH
  ( COLUMN_ENCRYPTION_KEY = key_name ,
      ENCRYPTION_TYPE = RANDOMIZED ,
      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'
  );
```

##### Snowflake[¶](#id60)

```
ALTER TABLE IF EXISTS table_name
ADD encryptedcol VARCHAR(20)
----** SSC-FDM-TS0009 - ENCRYPTED WITH NOT SUPPORTED IN SNOWFLAKE **
--ENCRYPTED WITH
--  ( COLUMN_ENCRYPTION_KEY = key_name ,
--      ENCRYPTION_TYPE = RANDOMIZED ,
--      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'
--  )
   ;
```

#### NOT NULL[¶](#not-null)

The SQL Server NOT NULL clause has the same pattern and functionality as the Snowflake NOT NULL
clause

##### SQL Server[¶](#id61)

```
ALTER TABLE table2 ADD
column_test INTEGER NOT NULL,
column_test2 INTEGER NULL,
column_test3 INTEGER;
```

##### Snowflake[¶](#id62)

```
ALTER TABLE IF EXISTS table2 ADD column_test INTEGER NOT NULL;

ALTER TABLE IF EXISTS table2 ADD column_test2 INTEGER NULL;

ALTER TABLE IF EXISTS table2 ADD column_test3 INTEGER;
```

#### IDENTITY[¶](#identity)

This pattern showcases the translation for IDENTITY. The `NOT FOR REPLICATION` portion is removed in
Snowflake.

##### SQL Server[¶](#id63)

```
ALTER TABLE table3 ADD
column_test INTEGER IDENTITY(1, 100) NOT FOR REPLICATION;
```

##### Snowflake[¶](#id64)

```
ALTER TABLE IF EXISTS table3 ADD column_test INTEGER IDENTITY(1, 100) ORDER;
```

### Unsupported clauses[¶](#unsupported-clauses)

#### FILESTREAM[¶](#filestream)

The original behavior of `FILESTREAM` is not replicable in Snowflake, and merits commenting out the
entire `ALTER TABLE` statement.

##### SQL Server[¶](#id65)

```
ALTER TABLE table2
ADD column1 varbinary(max)
FILESTREAM;
```

##### Snowflake[¶](#id66)

```
ALTER TABLE IF EXISTS table2
ADD column1 VARBINARY
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'FILESTREAM COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FILESTREAM;
```

#### SPARSE[¶](#sparse)

In SQL Server,
[SPARSE](https://docs.microsoft.com/en-us/sql/relational-databases/tables/use-sparse-columns) is
used to define columns that are optimized for NULL storage. However, when we’re using Snowflake, we
are not required to use this clause.

Snowflake performs
[optimizations over tables](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html#benefits-of-micro-partitioning)
automatically, which mitigates the need for manual user-made optimizations.

##### SQL Server[¶](#id67)

```
-- ADD COLUMN DEFINITION form
ALTER TABLE table3
ADD column1 int NULL SPARSE;

----------------------------------------
/* It also applies to the other forms */
----------------------------------------

-- CREATE TABLE form
CREATE TABLE table3
(
    column1 INT SPARSE NULL
);

-- ALTER COLUMN form
ALTER TABLE table3
ALTER COLUMN column1 INT NULL SPARSE;
```

##### Snowflake[¶](#id68)

```
-- ADD COLUMN DEFINITION form
ALTER TABLE IF EXISTS table3
ALTER COLUMN column1
                     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0061 - ALTER COLUMN COMMENTED OUT BECAUSE SPARSE COLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                     INT NULL SPARSE;

----------------------------------------
/* It also applies to the other forms */
----------------------------------------

-- CREATE TABLE form
CREATE OR REPLACE TABLE table3
(
    column1 INT
                !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SPARSE COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                SPARSE NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

-- ALTER COLUMN form
ALTER TABLE IF EXISTS table3
ALTER COLUMN column1
                     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0061 - ALTER COLUMN COMMENTED OUT BECAUSE SPARSE COLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                     INT NULL SPARSE;
```

#### ROWGUIDCOL[¶](#rowguidcol)

##### SQL Server[¶](#id69)

```
ALTER TABLE table_name
ADD column_name UNIQUEIDENTIFIER
ROWGUIDCOL;
```

##### Snowflake[¶](#id70)

```
ALTER TABLE IF EXISTS table_name
ADD column_name VARCHAR
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'ROWGUIDCOL COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ROWGUIDCOL;
```

### Known Issues[¶](#id71)

**1. Roles and users have to be previously set up for masking policies**

Snowflake’s Masking Policies can be applied to columns only after the policies were created. This
requires the user to create the policies and assign them to roles, and these roles to users, in
order to work properly. Masking Policies can behave differently depending on which user is querying.

Warning

SnowConvert AI does not perform this setup automatically.

**2. Masking policies require a Snowflake Enterprise account or higher.**

higher-rankThe Snowflake documentation states that masking policies are available on Entreprise or
higher rank accounts.

**Note:**

For further details visit
[CREATE MASKING POLICY — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-masking-policy.html#create-masking-policy).

**3. DEFAULT only supports constant values**

SQL Server’s DEFAULT property is partially supported by Snowflake, as long as its associated value
is a constant.

**4.** **FILESTREAM clause is not supported in Snowflake.**

The entire FILESTSTREAM clause is commented out, since it is not supported in Snowflake.

**5.** **SPARSE clause is not supported in Snowflake.**

The entire SPARSE clause is commented out, since it is not supported in Snowflake. When it is added
within an ALTER COLUMN statement, and it’s the only modification being made to the column, the
entire statement is removed since it’s no longer adding anything.

### Related EWIs[¶](#id72)

1. [SSC-EWI-0040](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040):
   Statement Not Supported.
2. [SSC-EWI-TS0061](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0061):
   ALTER COLUMN not supported.
3. [SSC-EWI-TS0078](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0078):
   Default value not allowed in Snowflake.
4. [SSC-FDM-TS0009](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0009):
   Encrypted with not supported in Snowflake.
5. [SSC-FDM-TS0021](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0021):
   A MASKING POLICY was created as a substitute for MASKED WITH.
6. [SSC-FDM-TS0022](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM#ssc-fdm-ts0022):
   The user must previously define the masking role.
7. [SSC-PRF-0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0002):
   Case-insensitive columns can decrease the performance of queries.

## COLUMN CONSTRAINT[¶](#column-constraint)

ALTER TABLE ADD COLUMN … COLUMN CONSTRAINT

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id73)

Specifies the properties of a PRIMARY KEY, FOREIGN KEY or CHECK that is part of a new
[column constraint](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-constraint-transact-sql?view=sql-server-ver16)
added to a table by using
[Alter Table.](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16)

#### SQL Server[¶](#id74)

```
[ CONSTRAINT constraint_name ]
{
    [ NULL | NOT NULL ]
    { PRIMARY KEY | UNIQUE }
        [ CLUSTERED | NONCLUSTERED ]
        [ WITH FILLFACTOR = fillfactor ]
        [ WITH ( index_option [, ...n ] ) ]
        [ ON { partition_scheme_name (partition_column_name)
            | filegroup | "default" } ]
    | [ FOREIGN KEY ]
        REFERENCES [ schema_name . ] referenced_table_name
            [ ( ref_column ) ]
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
        [ NOT FOR REPLICATION ]
    | CHECK [ NOT FOR REPLICATION ] ( logical_expression )
}
```

#### Snowflake[¶](#id75)

```
CREATE TABLE <name> ( <col1_name> <col1_type>    [ NOT NULL ] { inlineUniquePK | inlineFK }
                     [ , <col2_name> <col2_type> [ NOT NULL ] { inlineUniquePK | inlineFK } ]
                     [ , ... ] )

ALTER TABLE <name> ADD COLUMN <col_name> <col_type> [ NOT NULL ] { inlineUniquePK | inlineFK }
```

Where:

```
inlineUniquePK ::=
  [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

```
inlineFK :=
  [ CONSTRAINT <constraint_name> ]
  [ FOREIGN KEY ]
  REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
  [ MATCH { FULL | SIMPLE | PARTIAL } ]
  [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
       [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

## CHECK[¶](#id76)

Applies to

- SQL Server

### Description[¶](#id77)

**Note:**

Some parts in the output code are omitted for clarity reasons.

When CHECK clause is in the ALTER statement, SnowConvert AI will comments out the entire statement,
since it is not supported.

### Sample Source Patterns[¶](#id78)

#### SQL Server[¶](#id79)

```
ALTER TABLE table_name
ADD column_name VARCHAR(255)
CONSTRAINT constraint_name
CHECK NOT FOR REPLICATION (column_name > 1);
```

#### Snowflake[¶](#id80)

```
ALTER TABLE IF EXISTS table_name
ADD column_name VARCHAR(255)
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
CONSTRAINT constraint_name
CHECK NOT FOR REPLICATION (column_name > 1);
```

### Known Issues[¶](#id81)

**1.** **ALTER TABLE CHECK clause is not supported in Snowflake.**

The entire ALTER TABLE CHECK clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id82)

- [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
  Check statement not supported.

## FOREIGN KEY[¶](#id83)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id84)

The syntax for the Foreign Key is fully supported by SnowFlake, except for the
`[ NOT FOR REPLICATION ]` and the `WITH CHECK` clauses.

#### SQL Server[¶](#id85)

Review the following
[SQL Server documentation](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16#syntax-for-memory-optimized-tables)
for more information.

```
[ FOREIGN KEY ]
REFERENCES [ schema_name . ] referenced_table_name
[ ( ref_column ) ]
[ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
[ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]
[ NOT FOR REPLICATION ]
```

#### Snowflake[¶](#id86)

```
[ FOREIGN KEY ]
REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
[ MATCH { FULL | SIMPLE | PARTIAL } ]
[ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
     [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
[ [ NOT ] ENFORCED ]
[ [ NOT ] DEFERRABLE ]
[ INITIALLY { DEFERRED | IMMEDIATE } ]
[ ENABLE | DISABLE ]
[ VALIDATE | NOVALIDATE ]
[ RELY | NORELY ]
```

### Sample Source Patterns[¶](#id87)

#### General case[¶](#general-case)

##### SQL Server[¶](#id88)

```
ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp(id);

ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp(id)
NOT FOR REPLICATION;
```

##### Snowflake[¶](#id89)

```
ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp (id);

ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp (id);
```

#### WITH CHECK / NO CHECK case[¶](#with-check-no-check-case)

Notice that Snowflake logic does not support the CHECK clause in the creation of foreign keys. The
`WITH CHECK` statement is marked as not supported. Besides, the `WITH NO CHECK` clause is removed
because it is the default behavior in Snowflake and the equivalence is the same.

Please, review the following examples to have a better understanding of the translation.

##### SQL Server[¶](#id90)

```
ALTER TABLE testTable
WITH CHECK ADD CONSTRAINT testFK1 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);

ALTER TABLE testTable
WITH NOCHECK ADD CONSTRAINT testFK2 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);
```

##### Snowflake[¶](#id91)

```
ALTER TABLE testTable
----** SSC-FDM-0014 - CHECK STATEMENT NOT SUPPORTED **
--WITH CHECK
           ADD CONSTRAINT testFK1 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);


ALTER TABLE testTable
ADD CONSTRAINT testFK2 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);
```

### Known Issues[¶](#id92)

**1.** **NOT FOR REPLICATION clause.**

Snowflake has a different approach to the replication cases. Please, review the following
[documentation](https://docs.snowflake.com/en/user-guide/account-replication-considerations).

**2. WITH CHECK clause.**

Snowflake does not support the `WITH CHECK` statement. Review the following
[documentation](https://docs.snowflake.com/en/sql-reference/constraints-overview) for more
information.

## PRIMARY KEY / UNIQUE[¶](#primary-key-unique)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id93)

All of the optional clauses of the PRIMARY KEY / UNIQUE constraint are removed in Snowflake.

**Syntax in SQL Server**

```
{ PRIMARY KEY | UNIQUE }
    [ CLUSTERED | NONCLUSTERED ]
    [ WITH FILLFACTOR = fillfactor ]
    [ WITH ( index_option [, ...n ] ) ]
    [ ON { partition_scheme_name (partition_column_name)
        | filegroup | "default" } ]
```

### Sample Source Patterns[¶](#id94)

#### SQL Server[¶](#id95)

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY
NONCLUSTERED;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
WITH FILLFACTOR = 80;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY
WITH (PAD_INDEX = off);

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
ON partition_scheme_name (partition_column_name);
```

#### Snowflake[¶](#id96)

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;
```
