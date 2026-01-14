---
description:
  This section documents the transformation of the syntax and the procedure’s TSQL statements to
  snowflake javascript
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-procedure
title: SnowConvert AI - SQL Server-Azure Synapse - Procedures | Snowflake Documentation
---

## 1. CREATE PROCEDURE Translation[¶](#create-procedure-translation)

Snowflake `CREATE PROCEDURE` is defined in SQL Syntax whereas its inner statements are defined in
JavaScript.

### Transact[¶](#transact)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE HumanResources.uspGetAllEmployees
     @FirstName NVARCHAR(50),
     @Age INT
AS
    -- TSQL Statements and queries...
GO
```

### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE PROCEDURE HumanResources.uspGetAllEmployees (FIRSTNAME STRING, AGE INT)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
$$;
```

### Parameter’s DATA TYPE[¶](#parameter-s-data-type)

Parameters data types are being translated to Snowflake equivalent. See also
[Data Types](transact-data-types).

### EXEC helper[¶](#exec-helper)

In order to be able to run statements from a procedure in the SnowFlake environment, these
statements have to be preprocessed and adapted to reflect their execution in several variables that
are specific to the source language.

SnowConvert AI automatically translates the supported statements and makes use of an EXEC helper.
This helper provides access and update capabilities to many variables that simulate how the
execution of these statements would be in their native environment.

For instance, you may see that in the migrated procedures, there is a block of code that is always
added. We are going to explain the basic structure of this code in the next section. Please keep in
mind that we are always evaluating and searching for new and improved ways to streamline the
transformations and any helper that we require.

#### Structure[¶](#structure)

The basic structure of the EXEC helper is as follows:

1. **Variable declaration section**: Here, we declare the different variables or objects that will
   contain values associated with the execution of the statements inside the procedure. This
   includes values such as the number of rows affected by a statement, or even the result set
   itself.
2. **fixBind function declaration**: This is an auxiliary function used to fix binds when they are
   of Date type.
3. **EXEC function declaration**: This is the main EXEC helper function. It receives the statement
   to execute, the array of binds (basically the variables or parameters that may be modified by the
   execution and require data permanence throughout the execution of the procedure), the noCatch
   flag that determines if the ERROR_HANDLERS must be used, and the catchFunction function for
   executing custom code when there’s an exception in the execution of the statement. The body of
   the EXEC function is very straightforward; execute the statement and store every valuable data
   produced by its execution, all inside an error handling block.
4. **ERROR VARS:** The EXEC catch block sets up a list of error variables such as `MESSAGE_TEXT`,
   `SQLCODE`, `SQLSTATE`, `PROC_NAME` and `ERROR_LINE` that could be used to retrieve values from
   user defined functions, in order to emulate the SQL Server
   [ERROR_LINE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-line-transact-sql?view=sql-server-ver15),
   [ERROR_MESSAGE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-message-transact-sql?view=sql-server-ver15),
   [ERROR_NUMBER](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-number-transact-sql?view=sql-server-ver15),
   [ERROR_PROCEDURE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-procedure-transact-sql?view=sql-server-ver15)
   and
   [ERROR_STATE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-state-transact-sql?view=sql-server-ver15)
   built in functions behavour. After all of these variables are set with one value, the
   `UPDATE_ERROR_VARS` user defined function, will be in charge of update some environment variables
   with the error values, in order to have access to them in the SQL scope.

#### Code[¶](#code)

The following code block represents the EXEC helper inside a procedure:

```
   var _RS, ROW_COUNT, _ROWS, MESSAGE_TEXT, SQLCODE = 0, SQLSTATE = '00000', ERROR_HANDLERS, NUM_ROWS_AFFECTED, INTO;
   var fixBind = function (arg) {
      arg = arg == undefined ? null : arg instanceof Date ? arg.toISOString() : arg;
      return arg;
   };
   var fetch = (count,rows,stmt) => (count && rows.next() && Array.apply(null,Array(stmt.getColumnCount())).map((_,i) => rows.getColumnValue(i + 1))) || [];
   var EXEC = (stmt,binds = [],noCatch = false) => {
      binds = binds ? binds.map(fixBind) : binds;
      for(var stmt of stmt.split(";").filter((_) => _)) {
         try {
            _RS = snowflake.createStatement({
                  sqlText : stmt,
                  binds : binds
               });
            _ROWS = _RS.execute();
            ROW_COUNT = _RS.getRowCount();
            NUM_ROWS_AFFECTED = _RS.getNumRowsAffected();
            return {
               THEN : (action) => !SQLCODE && action(fetch(_ROWS))
            };
         } catch(error) {
            let rStack = new RegExp('At .*, line (\\d+) position (\\d+)');
            let stackLine = error.stackTraceTxt.match(rStack) || [0,-1];
            MESSAGE_TEXT = error.message.toString();
            SQLCODE = error.code.toString();
            SQLSTATE = error.state.toString();
            snowflake.execute({sqlText: `SELECT UPDATE_ERROR_VARS_UDF(?,?,?,?,?)`,binds: [stackLine[1], SQLCODE, SQLSTATE, MESSAGE_TEXT, PROC_NAME]});
            throw error;
         }
      }
   };
```

**Simple EXEC example**

This is a simple example of an EXEC call inside a Stored Procedure

**Source Code**

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE dbo.EXEC_EXAMPLE_1
AS
   EXECUTE('SELECT 1 AS Message');
GO
```

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_1
GO
```

**Expected code**

```
CREATE OR REPLACE PROCEDURE dbo.EXEC_EXAMPLE_1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// REGION SnowConvert AI Helpers Code
	var _RS, ROW_COUNT, _ROWS, MESSAGE_TEXT, SQLCODE = 0, SQLSTATE = '00000', OBJECT_SCHEMA_NAME  = 'dbo', ERROR_HANDLERS, NUM_ROWS_AFFECTED, PROC_NAME = arguments.callee.name, DOLLAR_DOLLAR = '$' + '$';
	function* sqlsplit(sql) {
		var part = '';
		var ismark = () => sql[i] == '$' && sql[i + 1] == '$';
		for(var i = 0;i < sql.length;i++) {
			if (sql[i] == ';') {
				yield part + sql[i];
				part = '';
			} else if (ismark()) {
				part += sql[i++] + sql[i++];
				while ( i < sql.length && !ismark() ) {
					part += sql[i++];
				}
				part += sql[i] + sql[i++];
			} else part += sql[i];
		}
		if (part.trim().length) yield part;
	};
	var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
	var fixBind = function (arg) {
		arg = arg == undefined ? null : arg instanceof Date ? formatDate(arg) : arg;
		return arg;
	};
	var EXEC = (stmt,binds = [],severity = "16",noCatch = false) => {
		binds = binds ? binds.map(fixBind) : binds;
		for(var stmt of sqlsplit(stmt)) {
			try {
				_RS = snowflake.createStatement({
						sqlText : stmt,
						binds : binds
					});
				_ROWS = _RS.execute();
				ROW_COUNT = _RS.getRowCount();
				NUM_ROWS_AFFECTED = _RS.getNumRowsAffected();
				return {
					THEN : (action) => !SQLCODE && action(fetch(_ROWS))
				};
			} catch(error) {
				let rStack = new RegExp('At .*, line (\\d+) position (\\d+)');
				let stackLine = error.stackTraceTxt.match(rStack) || [0,-1];
				MESSAGE_TEXT = error.message.toString();
				SQLCODE = error.code.toString();
				SQLSTATE = error.state.toString();
				snowflake.execute({
					sqlText : `SELECT UPDATE_ERROR_VARS_UDF(?,?,?,?,?,?)`,
					binds : [stackLine[1],SQLCODE,SQLSTATE,MESSAGE_TEXT,PROC_NAME,severity]
				});
				throw error;
			}
		}
	};
	// END REGION

	EXEC(`SELECT 1 AS Message;`);
$$;
```

**EXEC within a Store Procedure with a parameter**

In this example, the EXEC command is inside a Stored Procedure and receives a parameter value

**Source Code**

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE dbo.EXEC_EXAMPLE_2
	@p1 varchar(50) = N''
AS
	EXEC ('SELECT ' + @p1);
GO
```

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_2 N'''Hello World!'''
GO
```

**Expected Code**

```
CREATE OR REPLACE PROCEDURE dbo.EXEC_EXAMPLE_2 (P1 STRING DEFAULT '')
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	EXEC(`SELECT
   ${P1};`);
$$;
```

**EXEC invoking a Store Procedure with a parameter**

In this example, the EXEC invokes another Stored Procedure and pass adds a parameter

**Source Code**

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE dbo.EXEC_EXAMPLE_3
	@p1 varchar(50) = N''
AS
	EXEC EXEC_EXAMPLE_2 @p1
GO
```

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_3 N'''Hello World!'''
GO
```

**Expected Code**

```
CREATE OR REPLACE PROCEDURE dbo.EXEC_EXAMPLE_3 (P1 STRING DEFAULT '')
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	EXEC(`CALL EXEC_EXAMPLE_2(?)`,[P1]);
$$;
```

### Parameters with Default Value.[¶](#parameters-with-default-value)

In SqlServer, there can be parameters with a default value in case these are not specified when a
procedure is being called.

#### SQL Server[¶](#sql-server)

```
CREATE PROCEDURE PROC_WITH_DEFAULT_PARAMS1
@PARAM1 INT = 0, @PARAM2 INT = 0, @PARAM3 INT = 0, @PARAM4 INT = 0
AS
BEGIN
    .
    .
    .
END
```

#### Snowflake[¶](#id1)

```
CREATE OR REPLACE PROCEDURE PROC_WITH_DEFAULT_PARAMS1(param1 int default 0, param2 int default 0, param3 int default 0, param4 int default 0)
RETURNS TABLE()
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
    .
    .
    .
$$;
```

```
CALL PROC_WITH_DEFAULT_PARAMS1(param2 => 10, param4 => 15);
```

### CURSOR helper[¶](#cursor-helper)

```
CREATE OR REPLACE PROCEDURE PROC1()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
	  var CURSOR = function (stmt, binds) {
	  var statementObj, result_set, total_rows, isOpen = false, self = this, row_count;

	  this.CURRENT = new Object;

	  var fetch = (count,rows,stmt) => (count && rows.next() && Array.apply(null,Array(stmt.getColumnCount())).map((_,i) => rows.getColumnValue(i + 1))) || [];

	  var fixBind = function (arg) {
	      arg = arg == undefined ? null : arg instanceof Date ? formatDate(arg) : arg;
	      return arg;
	   };

	  this.OPEN = function(openParameters) {
		  if (result_set == undefined) {
			try {
				if (openParameters) binds = openParameters;
				if (binds instanceof Function) binds = binds();
				var finalBinds = binds && binds.map(fixBind);
				var finalStmt = stmt instanceof Function ? stmt() : stmt;
				statementObj = snowflake.createStatement({
					sqlText : finalStmt,
					binds : finalBinds
				});
				result_set = statementObj.execute();
				total_rows = statementObj.getRowCount();
				isOpen = true;
				row_count = 0;
			} catch(error) {
				RAISE(error.code,"error",error.message);
			}
			else {
				isOpen = true;
			}
		  }

	      return this;
	  };

	  this.CURSOR_ROWS = function () {
	      return total_rows;
	  };

	  this.FETCH_STATUS = function() {
	      if(total_rows > row_count)
	          return 0;
	      else
	          return -1;
	  };

	  this.FETCH_NEXT = function() {
		  self.res = [];
	      if (isOpen) {
			  self.res = fetch(total_rows,result_set,statementObj);
			  if (self.res)
				  row_count++;
		  }
		  return self.res && self.res.length > 0;
	  };

	  this.INTO = function () {
	      return self.res;
	  };

	  this.CLOSE = function () {
	      isOpen = false;
	  };

	  this.DEALLOCATE = function() {
	      this.CURRENT = row_count = result_set_table = total_rows = result_set = statementObj = self = undefined;
	  };
  };

  var COL1, COL2;
  var sql_stmt = ``;

  let c = new CURSOR(`SELECT COL1, COL2 FROM TABLE1;`,() => []);

  c.OPEN();
  c.FETCH_NEXT();
  [COL1, COL2] = c.INTO();
  while ( c.FETCH_STATUS()) {


        sql_stmt = `INSERT INTO TABLE2 (COL1, COL2) VALUES (` + COL1+ `, ` + COL2 + `)`;

        snowflake.createStatement({
            sqlText : sql_stmt
         }).execute();
  }

  c.CLOSE();
  c.DEALLOCATE();

  return 'sucess';
$$;
```

### Insert Into EXEC Helper[¶](#insert-into-exec-helper)

The Insert into Exec helper generates a function called Insert `insertIntoTemporaryTable(sql).` This
function will allow the transformation for `INSERT INTO TABLE_NAME EXEC(...)` from TSQL to Snowflake
to imitate the behavior from the original statement by inserting it’s data into a temporary table
and then re-adding it into the original Insert.

For more information on how the code for this statement is modified look at the section for Insert
Into Exec

**Note:**

This Generated code for the INSERT INTO EXEC, may present performance issues when handling EXECUTE
statements containing multiple queries inside.

```
   function insertIntoTemporaryTable(sql) {
    var table = "SnowConvertPivotTemporaryTable";
    return EXEC('CREATE OR REPLACE TEMPORARY TABLE ${table} AS ${sql}');
  }

  insertIntoTemporaryTable(`${DBTABLES}`)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)
```

### LIKE Helper[¶](#like-helper)

In case that a like expression is found in a procedure, for example

```
CREATE PROCEDURE ProcedureLike @VariableValue VARCHAR(50) AS
BEGIN
	IF @VariableValue like '%c%'
	BEGIN
		Select AValue from ATable;
	END;
END;
```

Since the inside of the procedure is transformed to javascript, the like expression will throw an
error. In order to avoid and keep the functionality, a function is added at the start of the
procedure if a like expression is found.

```
   function LIKE(expr,pattern,esc,cs) {
    function fixPattern(pattern,esc) {
      const specials = '/.*+?|(){}[]\\'.split('');
      var newPattern = "";
      var fix = (c) => specials.includes(c) ? '\\' + c : c;
      for(var i = 0;i < pattern.length;i++) {
        var c = pattern[i];
        if (c === esc) {
          newPattern += pattern[i + 1]
          i++
        } else if (c === '%') {
          newPattern += ".*?"
        } else if (c === '_') {
          newPattern += "."
        } else if (c === '[' || ']') {
          newPattern += c
        } else newPattern += fix(c)
      }
      return newPattern;
    }
    return new RegExp(`^${fixPattern(pattern,esc)}$`,cs ? '' : 'i').exec(expr) != null;
  }
```

With this function, we can replicate the functionality of the like expression of sql. Let’s see the
diferent cases that it can be used

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE ProcedureLike @VariableValue VARCHAR(50) AS
BEGIN
	IF @VariableValue like '%c%'
	BEGIN
		Select AValue from ATable;
	END;
	IF @VariableValue not like '%c%'
	BEGIN
		Select BValue from BTable;
	END;
  IF @VariableValue like '%c!%%' escape '!'
	BEGIN
		Select CValue from CTable;
	END;
END;
```

In the last code, there is a normal like a not like, and a like with escape. The transformation will
be

```
CREATE OR REPLACE PROCEDURE ProcedureLike (VARIABLEVALUE STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	if (LIKE(VARIABLEVALUE,`%c%`)) {
		{
			EXEC(`		Select
		   AValue
		from
		   ATable`);
		}
	}
	if (!LIKE(VARIABLEVALUE,`%c%`)) {
		{
			EXEC(`		Select
		   BValue
		from
		   BTable`);
		}
	}
	if (LIKE(VARIABLEVALUE,`%c!%%`,`!`)) {
		{
			EXEC(`		Select
		   CValue
		from
		   CTable`);
		}
	}
$$;
```

Note that the likes are transformed to function calls

```
LIKE(VARIABLEVALUE,`%c%`)
!LIKE(VARIABLEVALUE,`%c%`)
LIKE(VARIABLEVALUE,`%c!%%`,`!`)
```

The parameters that the function LIKE receive are the followings:

- The expression that is being evaluated.
- The pattern of comparison
- If it is present, the escape character, this is an optional parameter.

### Select Helper[¶](#select-helper)

Generates a function called SELECT when a scalar value has to be set to a variable

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE MAX_EMPLOYEE_ID
AS
BEGIN
   DECLARE @VARIABLE INT
   SET @VARIABLE = (SELECT MAX(EMPLOYEE_ID) FROM EMPLOYEES);
   RETURN @VARIABLE
END;
```

In this case, it will generate the following code with the SELECT helper

```
CREATE OR REPLACE PROCEDURE MAX_EMPLOYEE_ID ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.

   let VARIABLE;
   VARIABLE = EXEC(`SELECT
   MAX(EMPLOYEE_ID) FROM
   EMPLOYEES`);
   return VARIABLE;
$$;
```

The SELECT helper could be used as well to insert into a local value a retrieved value from a query.
The helper was designed specifically to support the same behavour of the SQL Server
[SELECT @local_variable](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver15).
The `args` parameter, represents each operation applied to all of the local variables inside the
select. See also [SELECT @Variable](#select-variable). For example:

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE [PROCEDURE1] AS

DECLARE @VAR1 int;
DECLARE @VAR2 int;
select @VAR1 = col1 + col2, @VAR2 += col1 from table1;

GO
```

In this case the variable assignments will be translated to `JavaScript` lambdas in order to emulate
the SQL Server behavior.

```
CREATE OR REPLACE PROCEDURE PROCEDURE1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
// SnowConvert AI Helpers Code section is omitted.

let VAR1;
let VAR2;
SELECT(`   col1 + col2,
   col1
   from
   table1`,[],(value) => VAR1 = value,(value) => VAR2 += value);
$$;
```

### RAISERROR Helper[¶](#raiserror-helper)

This helper is generated when there exists usages of a RAISERROR call in the source code. Example:

```
 var RAISERROR = (message,severity,state) => {
    snowflake.execute({
      sqlText : `SELECT UPDATE_ERROR_VARS_UDF(?,?,?)`,
      binds : [message,severity,state]
    });
    var msg = `Message: ${message}, Level: ${severity}, State: ${state}`;
    throw msg;
  };
```

The RAISERROR executes the _UPDATE_ERROR_VARS_UDF_ in order to store the value of the error message,
severity and state as environment variables, in case they need to be used by calling any of the
ERROR built in functions. Finally, the error message is thrown with the same format as SQL Server
does.

### Identity Function Helper[¶](#identity-function-helper)

This helper is generated whenever the
[Identity Fuction](https://docs.microsoft.com/en-us/sql/t-sql/functions/identity-function-transact-sql?view=sql-server-ver15)
is used on a Select Into inside a procedure.

```
  var IdentityHelper = (seed,increment) => {
      var sequenceString = "`CREATE OR REPLACE SEQUENCE SnowConvert_Temp_Seq START = ${seed} INCREMENT = ${increment}`";
      return EXEC(sequenceString);
```

The parameters for this helper are the same as the original function, it is created in order to
generate a sequence to mimic the identity function behavior in TSQL, the changes to the original
code are:

- An additional method call to the IdentityHelper function using the same parameters found in the
  source code.
- And call to the IDENTITY_UDF a function design to get the next value in the sequence.

```
   IdentityHelper(1,1)
   EXEC(`CREATE TABLE PUBLIC.department_table3 AS SELECT IDENTITY_UDF() /*** MSC-WARNING - MSCEWI1046 - 'identity' FUNCTION MAPPED TO 'IDENTITY_UDF', FUNCTIONAL EQUIVALENCE VERIFICATION PENDING ***/ as Primary_Rank
from PUBLIC.department_table`);
```

Just like in the TSQL if no parameters are given (1,1) will be the default values.

### CALL Procedure Helper[¶](#call-procedure-helper)

This helper is generated whenever there is a call to what previously was a user defined function,
but is now a procedure as a result of the translation process.

```
    var CALL = (sql,binds = [],...args) => {
      EXEC("CALL " + sql,binds);
      _ROWS.next();
      return (_ROWS.getColumnValue(1))[0];
   };
```

The purpose of this helper is to encapsulate the logic required for calling procedures as if they
were functions.

Please keep in mind that this functionality is limited, since procedures cannot be invoked within
queries such as SELECT.

Example of use, assuming that `FooSelfAssign(@PAR INT)` was translated to a procedure:

```
 // Input code
DECLARE @VAR1 INT = FooSelfAssign(1);
DECLARE @VAR4 INT = FooSelfAssign(FooSelfAssign(FooSelfAssign(FooSelfAssign(4))));
```

```
 // Output code
let VAR1 = CALL(`FooSelfAssign(1)`)
let VAR4 = CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(4)`)])])]);
```

Note that the translation for VAR1 is very straightforward, but for VAR4, the outmost CALL contains
a list with the rest of the CALLs, as bindings.

Each successive CALL is translated to a binding, if it’s contained within another CALL.

## 2. Variables[¶](#variables)

### DECLARE @Variable[¶](#declare-variable)

#### SQL Server[¶](#id2)

```
DECLARE @product_list VARCHAR(MAX) = ' ';
DECLARE @Variable1 AS VARCHAR(100), @Variable2 AS VARCHAR(100);
```

#### Snowflake[¶](#id3)

```
let PRODUCT_LIST = ` `;
let VARIABLE1;
let VARIABLE2;
```

### DECLARE @Variable Table[¶](#declare-variable-table)

In this case, the DECLARE is used to declare a variable table, let’s see an example.

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE PROC1
AS
BEGIN
DECLARE @VariableNameTable TABLE
 (
 [Col1] INT NOT NULL,
 [Col2] INT NOT NULL
 );
INSERT INTO @VariableNameTable Values(111,222);
Select * from @VariableNameTable;
END

Exec PROC1;
```

If we execute that code in Sql Server, we will get the following result

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|111|222|

Now, let’s see the transformation in Snowflake

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
 // SnowConvert AI Helpers Code section is omitted.

 {
  EXEC(`CREATE OR REPLACE TEMPORARY TABLE T_VariableNameTable
(
   Col1 INT NOT NULL,
   Col2 INT NOT NULL
)`);
  EXEC(`INSERT INTO T_VariableNameTable Values(111,222)`);
  EXEC(`Select
   *
from
   T_VariableNameTable`);
 }
 EXEC(`CALL PROC1()`);
$$;
```

Note that from the lines **61** to **67** are the results of those statements inside the procedure.

The Declare Variable Table is turned into a Temporary Table. Note that the name, which that in the
name the character @ was replaced for T\_.

If we execute that code in Snowflake, we will not get any result. it will display just null. That’s
because that last Select is now in the EXEC helper. So, how do we know that the table is there?

Since it was created as a temporary table inside the Procedure in an EXEC, we can do a Select to
that table outside of the Procedure.

```
 Select * from PUBLIC.T_VariableNameTable;
```

If we execute that statement, we will get the following result

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|111|222|

### SET @Variable[¶](#set-variable)

For now, the Set Variable is transformed depending on the expression that is has on the right side.

If the expression has a transformation, it will be transformed to it’s JavaScript equivalent.

Example

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE PROC1
AS
BEGIN
	SET @product_list2 = '';
    SET @product_list = '';
    SET @var1 += '';
    SET @var2 &= '';
    SET @var3 ^= '';
    SET @var4 |= '';
    SET @var5 /= '';
    SET @var6 %= '';
    SET @var7 *= '';
    SET @var8 -= '';
    SET @ProviderStatement = 'SELECT * FROM TABLE1
WHERE COL1 = '+@PARAM1+ ' AND COL2 = ' + @LOCALVAR1;
    SET @NotSupported = functionValue(a,b,c);
END
```

#### Snowflake[¶](#id4)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	PRODUCT_LIST2 = ``;
	PRODUCT_LIST = ``;
	VAR1 += ``;
	VAR2 &= ``;
	VAR3 ^= ``;
	VAR4 |= ``;
	VAR5 /= ``;
	VAR6 %= ``;
	VAR7 *= ``;
	VAR8 -= ``;
	PROVIDERSTATEMENT = `SELECT
   *
FROM
   TABLE1
WHERE
   COL1 = ${PARAM1}
   AND COL2 = ${LOCALVAR1};`;
	NOTSUPPORTED = SELECT(`   functionValue(a,b,c) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'functionValue' NODE ***/!!!`);
$$;
```

As you can see in the example, the value of the variable NOTSUPPORTED is commented since it is not
being transformed for the time being. Note that means that the transformation is not completed yet.

Other kinds of sets are commented, for example the following

#### SQL Server[¶](#id5)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE PROC1
AS
BEGIN
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
;

SET NOCOUNT ON
;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
;

SET NOCOUNT OFF
;
END
```

#### Snowflake[¶](#id6)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
// SnowConvert AI Helpers Code section is omitted.

/*** SSC-EWI-0040 - THE 'SET' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
/*SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED*/
;
/*** SSC-EWI-0040 - THE 'SET' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
/*SET NOCOUNT ON*/
;
/*** SSC-EWI-0040 - THE 'SET' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
/*SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED*/
;
/*** SSC-EWI-0040 - THE 'SET' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
/*SET NOCOUNT OFF*/
;
$$;
```

### SELECT @Variable[¶](#select-variable)

For now, the `SELECT @variable` is being transformed into a simple select, removing the variable
assignations, and keeping the expressions at the right side of the operator. The assignment
operations of the local variables in the select, will be replaced with `arrow` functions that
represent the same behavour of the operation being did during the local variable assignment in
`SQL Server`.

#### SQL Server[¶](#id7)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE PROC1 AS
DECLARE @VAR1 int;
DECLARE @VAR2 int;
SELECT @VAR1 = COL1 + COL2, @VAR2 = COL3 FROM TABLE1;
GO
```

#### Snowflake[¶](#id8)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
// SnowConvert AI Helpers Code section is omitted.

let VAR1;
let VAR2;
SELECT(`   COL1 + COL2,
   COL3
   FROM
   TABLE1`,[],(value) => VAR1 = value,(value) => VAR2 = value);
$$;
```

## 3. Statements translation[¶](#statements-translation)

### SELECT[¶](#select)

#### Basic form[¶](#basic-form)

The basic SELECT form does not have bindings, so the translation implies the creation of a call to
the EXEC helper function, with one parameter. For example:

```
 -- Source code:
SELECT * FROM DEMO_TABLE_1;
```

```
 // Translated code:
EXEC(`SELECT * FROM DEMO_TABLE_1`);
```

### IF[¶](#if)

#### SQL Server[¶](#id9)

```
IF Conditional_Expression
   -- SQL Statement
ELSE IF Conditiona_Expression2
   -- SQL Statement
ELSE
   -- SQL Statement
```

#### Snowflake[¶](#id10)

```
 if (Conditional_Expression) {
    // SQL Statement
} else if (Conditional_Expression2) {
    // SQL Statement
} else{
    // SQL Statement
}
```

### WHILE[¶](#while)

#### SQL Server[¶](#id11)

```
WHILE ( Conditional_Expression )
BEGIN
   -- SQL STATEMENTS
END;
```

#### Snowflake[¶](#id12)

```
while ( Conditional_Expression )
{
  // SQL STATEMENTS
}
```

### EXEC / EXECUTE[¶](#exec-execute)

#### SQL Server[¶](#id13)

```
 -- Execute simple statement
Exec('Select 1');

-- Execute statement using Dynamic Sql
Exec('Select ' + @par1 + ' from [db].[t1]');

-- Execute Procedure with parameter
EXEC db.sp2 'Create proc [db].[p3] AS', @par1, 1
```

#### Snowflake[¶](#id14)

```
 -- Execute simple statement
EXEC(`Select 1`);

-- Execute statement using Dynamic Sql
EXEC(`Select ${PAR1} from MYDB.db.t1`);

-- Execute Procedure with parameter
EXEC(`CALL db.sp2(/*** SSC-EWI-0038 - THIS STATEMENT MAY BE A DYNAMIC SQL THAT COULD NOT BE RECOGNIZED AND CONVERTED ***/
'Select * from MYDB.db.t1', ?, 1, Default)`,[PAR1]);
```

### THROW[¶](#throw)

The transformation for THROW ensures that the catch block that receives the error has access to the
information specified in the original statement.

#### SQL Server[¶](#id15)

```
 -- Case 1
THROW

-- Case 2
THROW 123, 'The error message', 1

-- Case 3
THROW @var1, @var2, @var3
```

#### Snowflake[¶](#id16)

```
 // Case 1
throw {};

// Case 2
throw { code: 123, message: "The error message", status: 1 };

// Case 3
throw { code: VAR1, message: VAR2, status: VAR3 };
```

### RAISERROR[¶](#raiserror)

SQL Server
[RAISERROR](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql?view=sql-server-ver15)
function is not supported in Snowflake. SnowConvert AI identifies all the usages in order to
generate a helper that emulates the original behavour. Example:

#### SQL Server[¶](#id17)

```
 -- Additional Params: -t JavaScript
CREATE OR ALTER PROCEDURE  RAISERRORTEST AS
BEGIN
    DECLARE @MessageTXT VARCHAR = 'ERROR MESSAGE';
    RAISERROR (N'E_INVALIDARG', 16, 1);
    RAISERROR ('Diagram does not exist or you do not have permission.', 16, 1);
    RAISERROR(@MessageTXT, 16, 1);
END
GO
```

#### Snowflake[¶](#id18)

```
CREATE OR REPLACE PROCEDURE RAISERRORTEST ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let MESSAGETXT = `ERROR MESSAGE`;
    RAISERROR("E_INVALIDARG","16","1");
    RAISERROR("Diagram does not exist or you do not have permission.","16","1");
    RAISERROR(MESSAGETXT,"16","1");
$$;
```

### BREAK/CONTINUE[¶](#break-continue)

The break/continue transformation, ensures flow of the code to be stopped or continue with another
block.

#### SQL Server[¶](#id19)

```
-- Additional Params: -t JavaScript
CREATE PROCEDURE ProcSample
AS
BEGIN
IF @@ROWCOUNT > 0
  Continue;
ELSE
  BREAK;
END
```

#### Snowflake[¶](#id20)

```
CREATE OR REPLACE PROCEDURE ProcSample ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  if (ROW_COUNT > 0) {
    continue;
  } else {
    break;
  }
$$;
```

### INSERT INTO EXEC[¶](#insert-into-exec)

The code is modify slightly due to the `INSERT INTO [Table] EXEC(...)` Statement not being supported
in Snowflake this allows us to replicate the behavior by adding a few lines of code:

- The first line added is a call to the `insertIntoTemporaryTable` to where the extracted code from
  the argument inside the `EXEC`, this will Insert the result set into a Temporary table. For more
  information on the function check the Insert Into EXEC Helper section.
- The Insert’s Exec is removed from the code and a query retrieving the results of the EXEC from the
  temporary table.

```
SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable
```

- The last line added is a DROP TABLE statement for the Temporary Table added.

```
   DROP TABLE SnowConvertPivotTemporaryTable
```

#### SQL Server[¶](#id21)

```
INSERT INTO #Table1
EXEC ('SELECT
Table1.ID
FROM Population');

INSERT INTO #Table1
EXEC (@DBTables);
```

#### Snowflake[¶](#id22)

```
  insertIntoTemporaryTable(`SELECT Table1.ID FROM MYDB.PUBLIC.Population)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table1 SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)

  insertIntoTemporaryTable(`${DBTABLES}`)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table1 SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)
```

### BEGIN TRANSACTION[¶](#begin-transaction)

BEGIN TRANSACTION is transformed to Snowflake’s BEGIN command, and inserted into an EXEC helper
call.

The helper is in charge of actually executing the resulting BEGIN.

#### SQL Server[¶](#id23)

```
 -- Input code
BEGIN TRAN @transaction_name;
```

#### Snowflake[¶](#id24)

```
 // Output code
EXEC(`BEGIN`, []);
```

### COMMIT TRANSACTION[¶](#commit-transaction)

COMMIT TRANSACTION is transformed to Snowflake’s COMMIT command, and inserted into an EXEC helper
call.

The helper is in charge of actually executing the resulting COMMIT.

#### SQL Server[¶](#id25)

```
 -- Input code
COMMIT TRAN @transaction_name;
```

#### Snowflake[¶](#id26)

```
 // Output code
EXEC(`COMMIT`, []);
```

### ROLLBACK TRANSACTION[¶](#rollback-transaction)

ROLLBACK TRANSACTION is transformed to Snowflake’s ROLLBACK command, and inserted into an EXEC
helper call.

The helper is in charge of actually executing the resulting ROLLBACK .

#### SQL Server[¶](#id27)

```
 -- Input code
ROLLBACK TRAN @transaction_name;
```

#### Snowflake[¶](#id28)

```
 // Output code
EXEC(`ROLLBACK`, []);
```

### WAITFOR DELAY[¶](#waitfor-delay)

WAITFOR DELAY clause is transformed to Snowflake’s `SYSTEM$WAIT` function. The _time_to_pass_
parameter of the DELAY is transformed to seconds, for usage as a parameter in the `SYSTEM$WAIT`
function.

The other variants of the WAITFOR clause are not supported in Snowflake, and are therefore marked
with the corresponding message.

#### SQL Server[¶](#id29)

```
 -- Input code
1) WAITFOR DELAY '02:00';
2) WAITFOR TIME '13:30';
3) WAITFOR (RECEIVE TOP (1)
   @dh = conversation_handle,
   @mt = message_type_name,
   @body = message_body
   FROM [eqe]), TIMEOUT 5000;
```

#### Snowflake[¶](#id30)

```
 // Output code
1) EXEC(`SYSTEM$WAIT(120)`,[]);
2) /*** SSC-EWI-0040 - THE 'WAIT FOR' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
   /*WAITFOR TIME '13:30'*/
   ;
3) /*** SSC-EWI-0040 - THE 'WAIT FOR' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/
   /*WAITFOR (RECEIVE TOP (1)
      @dh = conversation_handle,
      @mt = message_type_name,
      @body = message_body
      FROM [eqe]), TIMEOUT 5000*/
   ;
```

## 3. Cursors[¶](#cursors)

Since `CURSORS` are not supported in Snowflake, SnowConvert AI maps their functionality to a
`JavaScript` helper that emulates the original behavior in the target platform. Example:

### SQL Server[¶](#id31)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE [procCursorHelper] AS

DECLARE vendor_cursor CURSOR FOR
    SELECT VendorID, Name
    FROM Purchasing.Vendor
    WHERE PreferredVendorStatus = 1
    ORDER BY VendorID;
GO
```

#### Snowflake[¶](#id32)

```
CREATE OR REPLACE PROCEDURE procCursorHelper ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var VENDOR_CURSOR = new CURSOR(`SELECT
       VendorID,
       Name
    FROM
       Purchasing.Vendor
    WHERE
       PreferredVendorStatus = 1
    ORDER BY VendorID`,[],false);
$$;
```

### DECLARE CURSOR[¶](#declare-cursor)

#### SQL Server[¶](#id33)

```
DECLARE myCursor1 CURSOR FOR SELECT COL1 FROM TABLE1
```

#### Snowflake[¶](#id34)

```
let myCursor1 = new CURSOR(`SELECT COL1 FROM TABLE1`,() => []);
```

### OPEN[¶](#open)

#### SQL Server[¶](#id35)

```
OPEN myCursor1
OPEN GLOBAL myCursor2
```

#### Snowflake[¶](#id36)

```
myCursor1.OPEN();
myCursor2.OPEN()
```

### FETCH[¶](#fetch)

#### SQL Server[¶](#id37)

```
DECLARE @VALUE1 INT
FETCH NEXT FROM myCursor1 into @VALUE1
```

#### Snowflake[¶](#id38)

```
var VALUE1;
myCursor1.FETCH_NEXT();
VALUE1 = myCursor1.INTO();
```

### CLOSE[¶](#close)

#### SQL Server[¶](#id39)

```
CLOSE myCursor1
CLOSE GLOBAL myCursor2
```

#### Snowflake[¶](#id40)

```
myCursor1.CLOSE()
myCursor2.CLOSE()
```

### DEALLOCATE[¶](#deallocate)

#### SQL Server[¶](#id41)

```
DEALLOCATE myCursor1
DEALLOCATE GLOBAL myCursor2
```

#### Snowflake[¶](#id42)

```
myCursor1.DEALLOCATE()
myCursor2.DEALLOCATE()
```

### @@FETCH_STATUS[¶](#fetch-status)

#### SQL Server[¶](#id43)

```
 @@FETCH_STATUS
```

#### Snowflake[¶](#id44)

```
myCursor1.FETCH_STATUS()
```

### @@CURSOR_ROWS[¶](#cursor-rows)

#### SQL Server[¶](#id45)

```
 @@CURSOR_ROWS
```

#### Snowflake[¶](#id46)

```
myCursor1.FETCH_STATUS()
```

## 4. Expressions[¶](#expressions)

### Binary Operations[¶](#binary-operations)

#### SQL Server[¶](#id47)

```
SET @var1 = 1 + 1;
SET @var1 = 1 - 1;
SET @var1 = 1 / 1;
SET @var1 = 1 * 1;
SET @var1 = 1 OR 1;
SET @var1 = 1 AND 1;
```

#### Snowflake[¶](#id48)

```
VAR1 = 1 + 1;
VAR1 = 1 - 1;
VAR1 = 1 / 1;
VAR1 = 1 * 1;
VAR1 = 1 || 1;
VAR1 = 1 && 1;
```

### Conditionals[¶](#conditionals)

#### SQL Server[¶](#id49)

```
@var1 > 0
@var1 = 0
@var1 < 0
@var1 <> 0
```

#### Snowflake[¶](#id50)

```
VAR1 > 0
VAR1 = 0
VAR1 < 0
VAR1 != 0
```

#### NULL Predicate[¶](#null-predicate)

##### SQL Server[¶](#id51)

```
@var1 is null
@var2 is not null
```

##### Snowflake[¶](#id52)

```
VAR1 == null
VAR2 != null
```

## 5. Labels and Goto[¶](#labels-and-goto)

`Labels` have not the same behavior in JavaScript as SQL Server has. To simulate the behavior, they
are being transformed to `functions` . Its usage is being replaced with a call of the generated
function that contains all the logic of the label. Example:

### Source Code[¶](#source-code)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE [procWithLabels]
AS
SUCCESS_EXIT:
	SET @ErrorStatus = 0
	RETURN @ErrorStatus

ERROR_EXIT:
	RETURN @ErrorStatus
```

#### Snowflake[¶](#id53)

```
CREATE OR REPLACE PROCEDURE procWithLabels ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	SUCCESS_EXIT();
	ERROR_EXIT();
	function SUCCESS_EXIT() {
		ERRORSTATUS = 0;
		return ERRORSTATUS;
	}
	function ERROR_EXIT() {
		return ERRORSTATUS;
	}
$$;
```

As you see in the example above, the function declarations that were the labels in the source code,
will be put at the end of the code in order to make it cleaner.

`GOTO` is another command that does not exist in JavaScript. To simulate its behavour, their usages
are being transformed to calls to the function (label) that is referenced, preceded by a return
statement. Example:

#### SQL Server[¶](#id54)

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE [procWithLabels]
AS
DECLARE @ErrorStatus int = 0;
IF @ErrorStatus <> 0 GOTO ERROR_EXIT

SUCCESS_EXIT:
	SET @ErrorStatus = 0
	RETURN @ErrorStatus

ERROR_EXIT:
	RETURN @ErrorStatus
```

#### Snowflake[¶](#id55)

```
CREATE OR REPLACE PROCEDURE procWithLabels ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	let ERRORSTATUS = 0;
	if (ERRORSTATUS != 0) {
		return ERROR_EXIT();
	}
	SUCCESS_EXIT();
	ERROR_EXIT();
	function SUCCESS_EXIT() {
		ERRORSTATUS = 0;
		return ERRORSTATUS;
	}
	function ERROR_EXIT() {
		return ERRORSTATUS;
	}
$$;
```

As you see in the example above, the `return` is added to the function call, in order to stop the
code flow as SQL Server does with the `GOTO` .

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040):
   Statement Not Supported.
2. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.
