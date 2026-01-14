---
description:
  DML statement extensions differ from normal DML statements because they can use PL/SQL elements
  like collections and records. So far some of these elements are not supported by snowflake
  scripting. If
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/dml-statements
title: SnowConvert AI - Oracle - DML STATEMENTS | Snowflake Documentation
---

## Description [¶](#description)

DML statement extensions differ from normal DML statements because they can use PL/SQL elements like
collections and records. So far some of these elements are not supported by snowflake scripting. If
one statement is not supported, an EWI will be added during the translation. Other DML statements
will be translated as if they were not inside a procedure.

## INSERT Statement Extension[¶](#insert-statement-extension)

Translation reference to convert Oracle INSERT Statement Extension to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id1)

> The PL/SQL extension to the SQL `INSERT` statement lets you specify a record name in the
> `values_clause` of the `single_table_insert` instead of specifying a column list in the
> `insert_into_clause.`
> ([Oracle PL/SQL Language Reference INSERT Statement Extension](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/INSERT-statement-extension.html#GUID-D81224C4-06DE-4635-A850-41D29D4A8E1B))

Snowflake INSERT INTO differs from Snowflake Scripting in variable constraints; needing to have the
names preceded by a colon ‘:’ in order to bind the variables’ value.

### Recommendations[¶](#recommendations)

Note

This code was executed to a better understanding of the examples:

#### Oracle[¶](#oracle)

```
CREATE TABLE numbers_table(num integer, word varchar2(20));
```

Copy

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE PUBLIC.numbers_table (num integer,
word VARCHAR(20));
```

Copy

#### INSERT Statement Extension simple case[¶](#insert-statement-extension-simple-case)

##### Oracle[¶](#id2)

```
CREATE OR REPLACE PROCEDURE proc_insert_statement
AS
number_variable integer := 10;
word_variable varchar2(20) := 'ten';
BEGIN
	INSERT INTO numbers_table VALUES(number_variable, word_variable);
	INSERT INTO numbers_table VALUES(11, 'eleven');
END;

CALL proc_insert_statement();
SELECT * FROM numbers_table ;
```

Copy

##### Result[¶](#result)

<!-- prettier-ignore -->
|NUM|WORD|
|---|---|
|10|ten|
|11|eleven|

##### Snowflake Scripting[¶](#snowflake-scripting)

```
CREATE OR REPLACE PROCEDURE proc_insert_statement ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		number_variable integer := 10;
		word_variable VARCHAR(20) := 'ten';
	BEGIN
		INSERT INTO numbers_table
		VALUES(:number_variable, :word_variable);
		INSERT INTO numbers_table
		VALUES(11, 'eleven');
	END;
$$;

CALL proc_insert_statement();

SELECT * FROM
	numbers_table;
```

Copy

##### Result[¶](#id3)

<!-- prettier-ignore -->
|NUM|WORD|
|---|---|
|10|ten|
|11|eleven|

### Known Issues[¶](#known-issues)

#### 1. Records are not supported by Snowflake Scripting[¶](#records-are-not-supported-by-snowflake-scripting)

Since records are not supported by snowflake scripting, instead of using the `VALUES record` clause,
it is necessary to change it into a SELECT clause and split the columns of the record. For more
information please see the
[Record Type Definition Section](collections-and-records.html#record-type-definition).

### Related EWIs[¶](#related-ewis)

No related EWIs.

## MERGE Statement[¶](#merge-statement)

Translation reference to convert Oracle MERGE statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id4)

> The `MERGE` statement is used to select rows from one or more sources for update or insertion into
> a table or view. It is possible to specify conditions to determine whether to update or insert
> into the target table or view. This statement is a convenient way to combine multiple operations.
> It lets to avoid multiple `INSERT`, `UPDATE`, and `DELETE` DML statements. `MERGE` is a
> deterministic statement. It is not possible to update the same row of the target table multiple
> times in the same `MERGE` statement.
> ([Oracle PL/SQL Language Reference MERGE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/MERGE.html#GUID-5692CCB7-24D9-4C0E-81A7-A22436DC968F))

#### Oracle MERGE Syntax[¶](#oracle-merge-syntax)

```
MERGE [ hint ]
   INTO [ schema. ] { table | view } [ t_alias ]
   USING { [ schema. ] { table | view }
         | ( subquery )
         } [ t_alias ]
   ON ( condition )
   [ merge_update_clause ]
   [ merge_insert_clause ]
   [ error_logging_clause ] ;

merge_update_clause := WHEN MATCHED THEN
UPDATE SET column = { expr | DEFAULT }
           [, column = { expr | DEFAULT } ]...
[ where_clause ]
[ DELETE where_clause ]

merge_insert_clause := WHEN NOT MATCHED THEN
INSERT [ (column [, column ]...) ]
VALUES ({ expr | DEFAULT }
          [, { expr | DEFAULT } ]...
       )
[ where_clause ]

error_logging_clause := LOG ERRORS
  [ INTO [schema.] table ]
  [ (simple_expression) ]
  [ REJECT LIMIT { integer | UNLIMITED } ]

where_clause := WHERE condition
```

Copy

##### Snowflake Scripting MERGE Syntax[¶](#snowflake-scripting-merge-syntax)

```
MERGE INTO <target_table> USING <source> ON <join_expr>
{ matchedClause | notMatchedClause } [ ... ]

matchedClause ::= WHEN MATCHED [ AND <case_predicate> ]
THEN { UPDATE SET <col_name> = <expr> [ , <col_name2> = <expr2> ... ] | DELETE } [ ... ]

notMatchedClause ::= WHEN NOT MATCHED [ AND <case_predicate> ]
THEN INSERT [ ( <col_name> [ , ... ] ) ] VALUES ( <expr> [ , ... ] )
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Sample auxiliary data[¶](#sample-auxiliary-data)

Note

This code was executed for a better understanding of the examples:

##### Oracle[¶](#id5)

```
CREATE TABLE people_source (
    person_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR2(20) NOT NULL,
    last_name VARCHAR2(20) NOT NULL,
    title VARCHAR2(10) NOT NULL
);

CREATE TABLE people_target (
    person_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR2(20) NOT NULL,
    last_name VARCHAR2(20) NOT NULL,
    title VARCHAR2(10) NOT NULL
);

CREATE TABLE bonuses (
    employee_id NUMBER,
    bonus NUMBER DEFAULT 100
);

INSERT INTO people_target
VALUES (1, 'John', 'Smith', 'Mr');

INSERT INTO people_target
VALUES (2, 'alice', 'jones', 'Mrs');

INSERT INTO people_source
VALUES (2, 'Alice', 'Jones', 'Mrs.');

INSERT INTO people_source
VALUES (3, 'Jane', 'Doe', 'Miss');

INSERT INTO people_source
VALUES (4, 'Dave', 'Brown', 'Mr');

INSERT INTO
    bonuses(employee_id) (
        SELECT
            e.employee_id
        FROM
            hr.employees e,
            oe.orders o
        WHERE
            e.employee_id = o.sales_rep_id
        GROUP BY
            e.employee_id
    );
```

Copy

##### Snowflake[¶](#id6)

```
CREATE OR REPLACE TABLE people_source (
    person_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE people_target (
    person_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE bonuses (
    employee_id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
    bonus NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ DEFAULT 100
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO people_target
VALUES (1, 'John', 'Smith', 'Mr');

INSERT INTO people_target
VALUES (2, 'alice', 'jones', 'Mrs');

INSERT INTO people_source
VALUES (2, 'Alice', 'Jones', 'Mrs.');

INSERT INTO people_source
VALUES (3, 'Jane', 'Doe', 'Miss');

INSERT INTO people_source
VALUES (4, 'Dave', 'Brown', 'Mr');

INSERT INTO bonuses(employee_id) (
    SELECT
        e.employee_id
    FROM
        hr.employees e,
        oe.orders o
    WHERE
        e.employee_id = o.sales_rep_id
    GROUP BY
        e.employee_id
);
```

Copy

#### MERGE Statement simple case[¶](#merge-statement-simple-case)

##### Oracle[¶](#id7)

```
MERGE INTO people_target pt USING people_source ps ON (pt.person_id = ps.person_id)
WHEN MATCHED THEN
UPDATE
SET
    pt.first_name = ps.first_name,
    pt.last_name = ps.last_name,
    pt.title = ps.title
    WHEN NOT MATCHED THEN
INSERT
    (
        pt.person_id,
        pt.first_name,
        pt.last_name,
        pt.title
    )
VALUES
    (
        ps.person_id,
        ps.first_name,
        ps.last_name,
        ps.title
    );

SELECT * FROM people_target;
```

Copy

##### Result[¶](#id8)

<!-- prettier-ignore -->
|PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
|---|---|---|---|
|1|John|Smith|Mr|
|2|Alice|Jones|Mrs.|
|3|Jane|Doe|Miss|
|4|Dave|Brown|Mr|

##### Snowflake[¶](#id9)

```
MERGE INTO people_target pt USING people_source ps ON (pt.person_id = ps.person_id)
WHEN MATCHED THEN
    UPDATE
SET
    pt.first_name = ps.first_name,
    pt.last_name = ps.last_name,
    pt.title = ps.title
WHEN NOT MATCHED THEN
INSERT
    (
        pt.person_id,
        pt.first_name,
        pt.last_name,
        pt.title
    )
VALUES
    (
        ps.person_id,
        ps.first_name,
        ps.last_name,
        ps.title
    );

SELECT * FROM
    people_target;
```

Copy

##### Result[¶](#id10)

<!-- prettier-ignore -->
|PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
|---|---|---|---|
|1|John|Smith|Mr|
|2|Alice|Jones|Mrs.|
|3|Jane|Doe|Miss|
|4|Dave|Brown|Mr|

#### MERGE Statement with DELETE and where clause[¶](#merge-statement-with-delete-and-where-clause)

In order to find an equivalence for the **DELETE** statement and the **where clause**, it is
necessary to reorder and implement some changes in the Snowflake merge statement.

##### Changed required:[¶](#changed-required)

- Replace the Oracle’s **DELETE where_clause** with a new Snowflake’s **matchedClause** with the
  **AND predicate** statement
- Replace the **where_clause** from the Oracle’s **merge_insert_clause** with an **AND predicate**
  statement in the Snowflake’s **notMatchedClause**

##### Oracle[¶](#id11)

```
MERGE INTO bonuses D USING (
    SELECT
        employee_id,
        salary,
        department_id
    FROM
        hr.employees
    WHERE
        department_id = 80
) S ON (D.employee_id = S.employee_id)
WHEN MATCHED THEN
UPDATE
SET
    D.bonus = D.bonus + S.salary *.01 DELETE
WHERE
    (S.salary > 8000)
    WHEN NOT MATCHED THEN
INSERT
    (D.employee_id, D.bonus)
VALUES
    (S.employee_id, S.salary *.01)
WHERE
    (S.salary <= 8000);

SELECT * FROM bonuses ORDER BY employee_id;
```

Copy

##### Result[¶](#id12)

<!-- prettier-ignore -->
|EMPLOYEE_ID|BONUS|
|---|---|
|153|180|
|154|175|
|155|170|
|159|180|
|160|175|
|161|170|
|164|72|
|165|68|
|166|64|
|167|62|
|171|74|
|172|73|
|173|61|
|179|62|

##### Snowflake[¶](#id13)

```
--** SSC-FDM-OR0018 - SNOWFLAKE MERGE STATEMENT MAY HAVE SOME FUNCTIONAL DIFFERENCES COMPARED TO ORACLE **
MERGE INTO bonuses D USING (
 SELECT
     employee_id,
     salary,
     department_id
 FROM
     hr.employees
 WHERE
     department_id = 80) S ON (D.employee_id = S.employee_id)
    WHEN MATCHED AND
    (S.salary > 8000) THEN
 DELETE
    WHEN MATCHED THEN
 UPDATE SET
    D.bonus = D.bonus + S.salary *.01
    WHEN NOT MATCHED AND
    (S.salary <= 8000) THEN
 INSERT
 (D.employee_id, D.bonus)
VALUES
 (S.employee_id, S.salary *.01);

SELECT * FROM
bonuses
ORDER BY employee_id;
```

Copy

##### Result[¶](#id14)

<!-- prettier-ignore -->
|EMPLOYEE_ID|BONUS|
|---|---|
|153|180|
|154|175|
|155|170|
|159|180|
|160|175|
|161|170|
|164|72|
|165|68|
|166|64|
|167|62|
|171|74|
|172|73|
|173|61|
|179|62|

Warning

In some cases the changes applied may do not work as expected, like the next example:

##### Oracle[¶](#id15)

```
MERGE INTO people_target pt USING people_source ps ON (pt.person_id = ps.person_id)
WHEN MATCHED THEN
UPDATE
SET
    pt.first_name = ps.first_name,
    pt.last_name = ps.last_name,
    pt.title = ps.title DELETE
where
    pt.title = 'Mrs.'
    WHEN NOT MATCHED THEN
INSERT
    (
        pt.person_id,
        pt.first_name,
        pt.last_name,
        pt.title
    )
VALUES
    (
        ps.person_id,
        ps.first_name,
        ps.last_name,
        ps.title
    )
WHERE
    ps.title = 'Mr';

SELECT * FROM people_target;
```

Copy

##### Result[¶](#id16)

<!-- prettier-ignore -->
|PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
|---|---|---|---|
|1|John|Smith|Mr|
|4|Dave|Brown|Mr|

##### Snowflake[¶](#id17)

```
--** SSC-FDM-OR0018 - SNOWFLAKE MERGE STATEMENT MAY HAVE SOME FUNCTIONAL DIFFERENCES COMPARED TO ORACLE **
MERGE INTO people_target pt USING people_source ps ON (pt.person_id = ps.person_id)
    WHEN MATCHED AND
    pt.title = 'Mrs.' THEN
        DELETE
    WHEN MATCHED THEN
        UPDATE SET
    pt.first_name = ps.first_name,
    pt.last_name = ps.last_name,
    pt.title = ps.title
    WHEN NOT MATCHED AND
    ps.title = 'Mr' THEN
        INSERT
        (
            pt.person_id,
            pt.first_name,
            pt.last_name,
            pt.title
        )
VALUES
        (
            ps.person_id,
            ps.first_name,
            ps.last_name,
            ps.title
        );


SELECT * FROM
        people_target;
```

Copy

##### Result[¶](#id18)

<!-- prettier-ignore -->
|PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
|---|---|---|---|
|1|John|Smith|Mr|
|2|Alice|Jones|Mrs.|
|4|Dave|Brown|Mr|

### Known Issues[¶](#id19)

#### 1. Oracle’s error_logging_clause is not supported[¶](#oracle-s-error-logging-clause-is-not-supported)

There is no equivalent for the error logging clause in Snowflake Scripting.

##### 2. Changed applied do not work as expected[¶](#changed-applied-do-not-work-as-expected)

Sometimes, the changes applied in order to achieve the functional equivalence between Oracle’s merge
statement and Snowflake’s do not work as expected.

### Related EWIs[¶](#id20)

1. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
2. [SSC-FDM-OR0018](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0018):
   Merge statement may not work as expected

## SELECT INTO Statement[¶](#select-into-statement)

Translation reference to convert Oracle SELECT INTO statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id21)

> The `SELECT` `INTO` statement retrieves values from one or more database tables (as the SQL
> `SELECT` statement does) and stores them in variables (which the SQL `SELECT` statement does not
> do).
> ([Oracle PL/SQL Language Reference SELECT INTO Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/SELECT-INTO-statement.html#GUID-6E14E04D-4344-45F3-BE80-979DD26C7A90))

#### Oracle SELECT INTO Syntax[¶](#oracle-select-into-syntax)

```
SELECT [ { DISTINCT | UNIQUE } | ALL ] select_list
    { into_clause | bulk_collect_into_clause } FROM rest-of-statement ;
```

Copy

##### Oracle Into Clause Syntax[¶](#oracle-into-clause-syntax)

```
INTO { variable [, variable ]... | record )
```

Copy

##### Oracle Bulk Collect Syntax[¶](#oracle-bulk-collect-syntax)

```
BULK COLLECT INTO { collection | :host_array }
  [, { collection | :host_array } ]...
```

Copy

##### Snowflake Scripting SELECT INTO Syntax[¶](#snowflake-scripting-select-into-syntax)

```
SELECT [ { ALL | DISTINCT } ]
    {
          [{<object_name>|<alias>}.]*
        | [{<object_name>|<alias>}.]<col_name>
        | [{<object_name>|<alias>}.]$<col_position>
        | <expr>
        [ [ AS ] <col_alias> ]
    }
    [ , ... ]
    INTO :<variable> [, :<variable> ... ]
    [...]
```

Copy

### Sample Source Patterns[¶](#id22)

#### Sample auxiliary data[¶](#id23)

Note

This code was executed to a better understanding of the examples:

##### Oracle[¶](#id24)

```
CREATE TABLE numbers_table(num integer, word varchar2(20));
INSERT INTO numbers_table VALUES (1, 'one');
CREATE TABLE aux_numbers_table(aux_num integer, aux_word varchar2(20));
```

Copy

##### Snowflake[¶](#id25)

```
CREATE OR REPLACE TABLE numbers_table (num integer,
word VARCHAR(20))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO numbers_table
VALUES (1, 'one');

CREATE OR REPLACE TABLE aux_numbers_table (aux_num integer,
aux_word VARCHAR(20))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

#### SELECT INTO Statement simple case[¶](#select-into-statement-simple-case)

##### Oracle[¶](#id26)

```
CREATE OR REPLACE PROCEDURE proc_select_into_variables
AS
number_variable integer;
word_variable varchar2(20);
BEGIN
	SELECT * INTO number_variable, word_variable FROM numbers_table;
	INSERT INTO aux_numbers_table VALUES(number_variable, word_variable);
END;

CALL proc_select_into_variables();
SELECT * FROM aux_numbers_table;
```

Copy

##### Result[¶](#id27)

<!-- prettier-ignore -->
|AUX_NUM|AUX_WORD|
|---|---|
|1|one|

##### Snowflake Scripting[¶](#id28)

```
CREATE OR REPLACE PROCEDURE proc_select_into_variables ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		number_variable integer;
		word_variable VARCHAR(20);
	BEGIN
		SELECT * INTO
			:number_variable,
			:word_variable
		FROM
			numbers_table;
		INSERT INTO aux_numbers_table
		VALUES(:number_variable, :word_variable);
	END;
$$;

CALL proc_select_into_variables();

SELECT * FROM
	aux_numbers_table;
```

Copy

##### Result[¶](#id29)

```
<!-- prettier-ignore -->
|AUX_NUM|AUX_WORD|
|---|---|
|1|one|
```

Copy

### Known Issues[¶](#id30)

#### 1. BULK COLLECT INTO is not supported[¶](#bulk-collect-into-is-not-supported)

Snowflake Scripting does not support the BULK COLLECT INTO clause. However, it is possible to use
ARRAY_AGG to construct a new variable. For more information please see the
[Collection Bulk Operations Section](collections-and-records.html#collection-bulk-operations).

##### 2. Collections and records are not supported[¶](#collections-and-records-are-not-supported)

Snowflake Scripting does not support the use of collections nor records. It is possible to migrate
them using Semi-structured data types as explained in [this section](collections-and-records).

### Related EWIs[¶](#id31)

No related EWIs.

## Work around to simulate the use of Records[¶](#work-around-to-simulate-the-use-of-records)

Warning

This page is deprecated but was left for compatibility purposes. If you want to see the updated
section, please refer to [Collections And Records](collections-and-records)

### Description[¶](#id32)

This section describes how to simulate the behavior of Oracle records in SELECT and INSERT
Statements, using RESULTSET and CURSORS of Snowflake Scripting.

#### Snowflake Scripting RESULTSET and CURSOR[¶](#snowflake-scripting-resultset-and-cursor)

##### Snowflake RESULTSET Syntax[¶](#snowflake-resultset-syntax)

```
<resultset_name> RESULTSET [ DEFAULT ( <query> ) ] ;

LET <resultset_name> RESULTSET [ { DEFAULT | := } ( <query> ) ] ;

LET <resultset_name> RESULTSET [ { DEFAULT | := } ( <query> ) ] ;
```

Copy

### Recommendations[¶](#id33)

Note

For the following examples, this code was executed to better understanding of the examples:

#### Oracle[¶](#id34)

```
CREATE TABLE numbers_table(num integer, word varchar2(20));
INSERT INTO numbers_table VALUES (1, 'one');
CREATE TABLE aux_numbers_table(aux_num integer, aux_word varchar2(20));
```

Copy

##### Snowflake[¶](#id35)

```
CREATE OR REPLACE TABLE numbers_table (num integer,
word VARCHAR(20))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO numbers_table
VALUES (1, 'one');

CREATE OR REPLACE TABLE aux_numbers_table (aux_num integer,
aux_word VARCHAR(20))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

#### Using RESULTSET and Cursors instead of Records[¶](#using-resultset-and-cursors-instead-of-records)

##### Oracle[¶](#id36)

```
CREATE OR REPLACE PROCEDURE proc_insert_select_resultset
AS
TYPE number_record_definition IS RECORD(
	rec_num numbers_table.num%type,
	rec_word numbers_table.word%type
);
number_record number_record_definition;
BEGIN
	SELECT * INTO number_record FROM numbers_table;
	INSERT INTO aux_numbers_table VALUES number_record;
END;

CALL proc_insert_select_resultset();
SELECT * FROM aux_numbers_table;
```

Copy

##### Result[¶](#id37)

<!-- prettier-ignore -->
|AUX_NUM|AUX_WORD|
|---|---|
|1|one|

##### Snowflake[¶](#id38)

```
CREATE OR REPLACE PROCEDURE proc_insert_select_resultset ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
		TYPE number_record_definition IS RECORD(
			rec_num numbers_table.num%type,
			rec_word numbers_table.word%type
		);
		number_record OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - number_record_definition DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
	BEGIN
		SELECT
			OBJECT_CONSTRUCT( *) INTO
			:number_record
		FROM
			numbers_table;
		INSERT INTO aux_numbers_table
		SELECT
			:number_record:REC_NUM,
			:number_record:REC_WORD;
	END;
$$;

CALL proc_insert_select_resultset();

SELECT * FROM
	aux_numbers_table;
```

Copy

using cursor

```
CREATE OR REPLACE PROCEDURE PUBLIC.proc_select_into()
RETURNS INTEGER
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
$$
DECLARE
    NUMBER_VARIABLE INTEGER;
    WORD_VARIABLE VARCHAR;
    NUMBER_RECORD RESULTSET;
BEGIN
    LET c2 CURSOR FOR NUMBER_RECORD;
    FOR row_variable IN c2 DO
        let var1 integer := row_variable.num;
        let var2 varchar := row_variable.word;
        INSERT INTO PUBLIC.aux_numbers_table VALUES(:var1, :var2);
    END FOR;
end;
$$;
```

Copy

##### Result[¶](#id39)

<!-- prettier-ignore -->
|AUX_NUM|AUX_WORD|
|---|---|
|1|one|

### Known Issues[¶](#id40)

#### 1. Limitation in the use of RESULTSET[¶](#limitation-in-the-use-of-resultset)

RESULTSET is very limited in its use. If `table(result_scan(last_query_id()))` statement, should be
used just after the RESULTSET’s query is executed. For further information check this
[link](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/resultsets.html#limitations-of-the-resultset-data-type).

### Related EWIs[¶](#id41)

1. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.
