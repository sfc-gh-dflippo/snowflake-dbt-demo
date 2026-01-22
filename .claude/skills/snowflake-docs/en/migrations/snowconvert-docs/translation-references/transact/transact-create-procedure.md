---
auto_generated: true
description: This section documents the transformation of the syntax and the procedure’s
  TSQL statements to snowflake javascript
last_scraped: '2026-01-14T16:54:04.923974+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-create-procedure
title: SnowConvert AI - SQL Server-Azure Synapse - Procedures | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageCREATE PROCEDURE (JavaScript)

# SnowConvert AI - SQL Server-Azure Synapse - Procedures[¶](#snowconvert-ai-sql-server-azure-synapse-procedures "Link to this heading")

This section documents the transformation of the syntax and the procedure’s TSQL statements to snowflake javascript

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

## 1. CREATE PROCEDURE Translation[¶](#create-procedure-translation "Link to this heading")

Snowflake `CREATE PROCEDURE` is defined in SQL Syntax whereas its inner statements are defined in JavaScript.

### Transact[¶](#transact "Link to this heading")

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE HumanResources.uspGetAllEmployees
     @FirstName NVARCHAR(50),
     @Age INT
AS
    -- TSQL Statements and queries...
GO
```

Copy

### Snowflake[¶](#snowflake "Link to this heading")

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

Copy

### Parameter’s DATA TYPE[¶](#parameter-s-data-type "Link to this heading")

Parameters data types are being translated to Snowflake equivalent. See also [Data Types](transact-data-types).

### EXEC helper[¶](#exec-helper "Link to this heading")

In order to be able to run statements from a procedure in the SnowFlake environment, these statements have to be preprocessed and adapted to reflect their execution in several variables that are specific to the source language.

SnowConvert AI automatically translates the supported statements and makes use of an EXEC helper. This helper provides access and update capabilities to many variables that simulate how the execution of these statements would be in their native environment.

For instance, you may see that in the migrated procedures, there is a block of code that is always added. We are going to explain the basic structure of this code in the next section. Please keep in mind that we are always evaluating and searching for new and improved ways to streamline the transformations and any helper that we require.

#### Structure[¶](#structure "Link to this heading")

The basic structure of the EXEC helper is as follows:

1. **Variable declaration section**: Here, we declare the different variables or objects that will contain values associated with the execution of the statements inside the procedure. This includes values such as the number of rows affected by a statement, or even the result set itself.
2. **fixBind function declaration**: This is an auxiliary function used to fix binds when they are of Date type.
3. **EXEC function declaration**: This is the main EXEC helper function. It receives the statement to execute, the array of binds (basically the variables or parameters that may be modified by the execution and require data permanence throughout the execution of the procedure), the noCatch flag that determines if the ERROR\_HANDLERS must be used, and the catchFunction function for executing custom code when there’s an exception in the execution of the statement. The body of the EXEC function is very straightforward; execute the statement and store every valuable data produced by its execution, all inside an error handling block.
4. **ERROR VARS:** The EXEC catch block sets up a list of error variables such as `MESSAGE_TEXT`, `SQLCODE`, `SQLSTATE`, `PROC_NAME` and `ERROR_LINE` that could be used to retrieve values from user defined functions, in order to emulate the SQL Server [ERROR\_LINE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-line-transact-sql?view=sql-server-ver15), [ERROR\_MESSAGE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-message-transact-sql?view=sql-server-ver15), [ERROR\_NUMBER](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-number-transact-sql?view=sql-server-ver15), [ERROR\_PROCEDURE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-procedure-transact-sql?view=sql-server-ver15) and [ERROR\_STATE](https://docs.microsoft.com/en-us/sql/t-sql/functions/error-state-transact-sql?view=sql-server-ver15) built in functions behavour. After all of these variables are set with one value, the `UPDATE_ERROR_VARS` user defined function, will be in charge of update some environment variables with the error values, in order to have access to them in the SQL scope.

#### Code[¶](#code "Link to this heading")

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

Copy

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

Copy

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_1
GO
```

Copy

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

Copy

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

Copy

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_2 N'''Hello World!'''
GO
```

Copy

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

Copy

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

Copy

```
 -- =============================================
-- Example to execute the stored procedure
-- =============================================
EXECUTE dbo.EXEC_EXAMPLE_3 N'''Hello World!'''
GO
```

Copy

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

Copy

### Parameters with Default Value.[¶](#parameters-with-default-value "Link to this heading")

In SqlServer, there can be parameters with a default value in case these are not specified when a procedure is being called.

#### SQL Server[¶](#sql-server "Link to this heading")

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

Copy

#### Snowflake[¶](#id1 "Link to this heading")

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

Copy

```
CALL PROC_WITH_DEFAULT_PARAMS1(param2 => 10, param4 => 15);
```

Copy

### CURSOR helper[¶](#cursor-helper "Link to this heading")

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

Copy

### Insert Into EXEC Helper[¶](#insert-into-exec-helper "Link to this heading")

The Insert into Exec helper generates a function called Insert `insertIntoTemporaryTable(sql).` This function will allow the transformation for `INSERT INTO TABLE_NAME EXEC(...)` from TSQL to Snowflake to imitate the behavior from the original statement by inserting it’s data into a temporary table and then re-adding it into the original Insert.

For more information on how the code for this statement is modified look at the section for Insert Into Exec

Note

This Generated code for the INSERT INTO EXEC, may present performance issues when handling EXECUTE statements containing multiple queries inside.

```
   function insertIntoTemporaryTable(sql) {
    var table = "SnowConvertPivotTemporaryTable";
    return EXEC('CREATE OR REPLACE TEMPORARY TABLE ${table} AS ${sql}');
  }
  
  insertIntoTemporaryTable(`${DBTABLES}`)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)
```

Copy

### LIKE Helper[¶](#like-helper "Link to this heading")

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

Copy

Since the inside of the procedure is transformed to javascript, the like expression will throw an error. In order to avoid and keep the functionality, a function is added at the start of the procedure if a like expression is found.

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

Copy

With this function, we can replicate the functionality of the like expression of sql. Let’s see the diferent cases that it can be used

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

Copy

In the last code, there is a normal like a not like, and a like with escape. The transformation will be

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

Copy

Note that the likes are transformed to function calls

```
LIKE(VARIABLEVALUE,`%c%`)
!LIKE(VARIABLEVALUE,`%c%`)
LIKE(VARIABLEVALUE,`%c!%%`,`!`)
```

Copy

The parameters that the function LIKE receive are the followings:

* The expression that is being evaluated.
* The pattern of comparison
* If it is present, the escape character, this is an optional parameter.

### Select Helper[¶](#select-helper "Link to this heading")

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

Copy

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

Copy

The SELECT helper could be used as well to insert into a local value a retrieved value from a query. The helper was designed specifically to support the same behavour of the SQL Server [SELECT @local\_variable](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver15). The `args` parameter, represents each operation applied to all of the local variables inside the select. See also [SELECT @Variable](#select-variable). For example:

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE [PROCEDURE1] AS

DECLARE @VAR1 int;
DECLARE @VAR2 int;
select @VAR1 = col1 + col2, @VAR2 += col1 from table1;

GO
```

Copy

In this case the variable assignments will be translated to `JavaScript` lambdas in order to emulate the SQL Server behavior.

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

Copy

### RAISERROR Helper[¶](#raiserror-helper "Link to this heading")

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

Copy

The RAISERROR executes the *UPDATE\_ERROR\_VARS\_UDF* in order to store the value of the error message, severity and state as environment variables, in case they need to be used by calling any of the ERROR built in functions. Finally, the error message is thrown with the same format as SQL Server does.

### Identity Function Helper[¶](#identity-function-helper "Link to this heading")

This helper is generated whenever the [Identity Fuction](https://docs.microsoft.com/en-us/sql/t-sql/functions/identity-function-transact-sql?view=sql-server-ver15) is used on a Select Into inside a procedure.

```
  var IdentityHelper = (seed,increment) => {
      var sequenceString = "`CREATE OR REPLACE SEQUENCE SnowConvert_Temp_Seq START = ${seed} INCREMENT = ${increment}`";
      return EXEC(sequenceString);
```

Copy

The parameters for this helper are the same as the original function, it is created in order to generate a sequence to mimic the identity function behavior in TSQL, the changes to the original code are:

* An additional method call to the IdentityHelper function using the same parameters found in the source code.
* And call to the IDENTITY\_UDF a function design to get the next value in the sequence.

```
   IdentityHelper(1,1)
   EXEC(`CREATE TABLE PUBLIC.department_table3 AS SELECT IDENTITY_UDF() /*** MSC-WARNING - MSCEWI1046 - 'identity' FUNCTION MAPPED TO 'IDENTITY_UDF', FUNCTIONAL EQUIVALENCE VERIFICATION PENDING ***/ as Primary_Rank
from PUBLIC.department_table`);
```

Copy

Just like in the TSQL if no parameters are given (1,1) will be the default values.

### CALL Procedure Helper[¶](#call-procedure-helper "Link to this heading")

This helper is generated whenever there is a call to what previously was a user defined function, but is now a procedure as a result of the translation process.

```
    var CALL = (sql,binds = [],...args) => {
      EXEC("CALL " + sql,binds);
      _ROWS.next();
      return (_ROWS.getColumnValue(1))[0];
   };
```

Copy

The purpose of this helper is to encapsulate the logic required for calling procedures as if they were functions.

Please keep in mind that this functionality is limited, since procedures cannot be invoked within queries such as SELECT.

Example of use, assuming that `FooSelfAssign(@PAR INT)` was translated to a procedure:

```
 // Input code
DECLARE @VAR1 INT = FooSelfAssign(1);
DECLARE @VAR4 INT = FooSelfAssign(FooSelfAssign(FooSelfAssign(FooSelfAssign(4))));
```

Copy

```
 // Output code
let VAR1 = CALL(`FooSelfAssign(1)`)
let VAR4 = CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(?)`,[CALL(`FooSelfAssign(4)`)])])]);
```

Copy

Note that the translation for VAR1 is very straightforward, but for VAR4, the outmost CALL contains a list with the rest of the CALLs, as bindings.

Each successive CALL is translated to a binding, if it’s contained within another CALL.

## 2. Variables[¶](#variables "Link to this heading")

### DECLARE @Variable[¶](#declare-variable "Link to this heading")

#### SQL Server[¶](#id2 "Link to this heading")

```
DECLARE @product_list VARCHAR(MAX) = ' ';
DECLARE @Variable1 AS VARCHAR(100), @Variable2 AS VARCHAR(100);
```

Copy

#### Snowflake[¶](#id3 "Link to this heading")

```
let PRODUCT_LIST = ` `;
let VARIABLE1;
let VARIABLE2;
```

Copy

### DECLARE @Variable Table[¶](#declare-variable-table "Link to this heading")

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

Copy

If we execute that code in Sql Server, we will get the following result

| col1 | col2 |
| --- | --- |
| 111 | 222 |

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

Copy

Note that from the lines **61** to **67** are the results of those statements inside the procedure.

The Declare Variable Table is turned into a Temporary Table. Note that the name, which that in the name the character @ was replaced for T\_.

If we execute that code in Snowflake, we will not get any result. it will display just null. That’s because that last Select is now in the EXEC helper. So, how do we know that the table is there?

Since it was created as a temporary table inside the Procedure in an EXEC, we can do a Select to that table outside of the Procedure.

```
 Select * from PUBLIC.T_VariableNameTable;
```

Copy

If we execute that statement, we will get the following result

| col1 | col2 |
| --- | --- |
| 111 | 222 |

### SET @Variable[¶](#set-variable "Link to this heading")

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

Copy

#### Snowflake[¶](#id4 "Link to this heading")

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

Copy

As you can see in the example, the value of the variable NOTSUPPORTED is commented since it is not being transformed for the time being. Note that means that the transformation is not completed yet.

Other kinds of sets are commented, for example the following

#### SQL Server[¶](#id5 "Link to this heading")

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

Copy

#### Snowflake[¶](#id6 "Link to this heading")

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

Copy

### SELECT @Variable[¶](#select-variable "Link to this heading")

For now, the `SELECT @variable` is being transformed into a simple select, removing the variable assignations, and keeping the expressions at the right side of the operator. The assignment operations of the local variables in the select, will be replaced with `arrow` functions that represent the same behavour of the operation being did during the local variable assignment in `SQL Server`.

#### SQL Server[¶](#id7 "Link to this heading")

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE PROC1 AS
DECLARE @VAR1 int;
DECLARE @VAR2 int;
SELECT @VAR1 = COL1 + COL2, @VAR2 = COL3 FROM TABLE1;
GO
```

Copy

#### Snowflake[¶](#id8 "Link to this heading")

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

Copy

## 3. Statements translation[¶](#statements-translation "Link to this heading")

### SELECT[¶](#select "Link to this heading")

#### Basic form[¶](#basic-form "Link to this heading")

The basic SELECT form does not have bindings, so the translation implies the creation of a call to the EXEC helper function, with one parameter.
For example:

```
 -- Source code:
SELECT * FROM DEMO_TABLE_1;
```

Copy

```
 // Translated code:
EXEC(`SELECT * FROM DEMO_TABLE_1`);
```

Copy

### IF[¶](#if "Link to this heading")

#### SQL Server[¶](#id9 "Link to this heading")

```
IF Conditional_Expression
   -- SQL Statement
ELSE IF Conditiona_Expression2
   -- SQL Statement
ELSE
   -- SQL Statement
```

Copy

#### Snowflake[¶](#id10 "Link to this heading")

```
 if (Conditional_Expression) {
    // SQL Statement
} else if (Conditional_Expression2) {
    // SQL Statement
} else{
    // SQL Statement
}
```

Copy

### WHILE[¶](#while "Link to this heading")

#### SQL Server[¶](#id11 "Link to this heading")

```
WHILE ( Conditional_Expression )
BEGIN
   -- SQL STATEMENTS
END;
```

Copy

#### Snowflake[¶](#id12 "Link to this heading")

```
while ( Conditional_Expression )
{
  // SQL STATEMENTS
}
```

Copy

### EXEC / EXECUTE[¶](#exec-execute "Link to this heading")

#### SQL Server[¶](#id13 "Link to this heading")

```
 -- Execute simple statement
Exec('Select 1');

-- Execute statement using Dynamic Sql
Exec('Select ' + @par1 + ' from [db].[t1]');

-- Execute Procedure with parameter
EXEC db.sp2 'Create proc [db].[p3] AS', @par1, 1
```

Copy

#### Snowflake[¶](#id14 "Link to this heading")

```
 -- Execute simple statement
EXEC(`Select 1`);

-- Execute statement using Dynamic Sql
EXEC(`Select ${PAR1} from MYDB.db.t1`);

-- Execute Procedure with parameter
EXEC(`CALL db.sp2(/*** SSC-EWI-0038 - THIS STATEMENT MAY BE A DYNAMIC SQL THAT COULD NOT BE RECOGNIZED AND CONVERTED ***/
'Select * from MYDB.db.t1', ?, 1, Default)`,[PAR1]);
```

Copy

### THROW[¶](#throw "Link to this heading")

The transformation for THROW ensures that the catch block that receives the error has access to the information specified in the original statement.

#### SQL Server[¶](#id15 "Link to this heading")

```
 -- Case 1
THROW

-- Case 2
THROW 123, 'The error message', 1

-- Case 3
THROW @var1, @var2, @var3
```

Copy

#### Snowflake[¶](#id16 "Link to this heading")

```
 // Case 1
throw {};

// Case 2
throw { code: 123, message: "The error message", status: 1 };

// Case 3
throw { code: VAR1, message: VAR2, status: VAR3 };
```

Copy

### RAISERROR[¶](#raiserror "Link to this heading")

SQL Server [RAISERROR](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql?view=sql-server-ver15)  function is not supported in Snowflake.
SnowConvert AI identifies all the usages in order to generate a helper that emulates the original behavour. Example:

#### SQL Server[¶](#id17 "Link to this heading")

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

Copy

#### Snowflake[¶](#id18 "Link to this heading")

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

Copy

### BREAK/CONTINUE[¶](#break-continue "Link to this heading")

The break/continue transformation, ensures flow of the code to be stopped or continue with another block.

#### SQL Server[¶](#id19 "Link to this heading")

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

Copy

#### Snowflake[¶](#id20 "Link to this heading")

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

Copy

### INSERT INTO EXEC[¶](#insert-into-exec "Link to this heading")

The code is modify slightly due to the `INSERT INTO [Table] EXEC(...)` Statement not being supported in Snowflake this allows us to replicate the behavior by adding a few lines of code:

* The first line added is a call to the `insertIntoTemporaryTable` to where the extracted code from the argument inside the `EXEC`, this will Insert the result set into a Temporary table. For more information on the function check the Insert Into EXEC Helper section.
* The Insert’s Exec is removed from the code and a query retrieving the results of the EXEC from the temporary table.

```
SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable
```

Copy

* The last line added is a DROP TABLE statement for the Temporary Table added.

```
   DROP TABLE SnowConvertPivotTemporaryTable
```

Copy

#### SQL Server[¶](#id21 "Link to this heading")

```
INSERT INTO #Table1
EXEC ('SELECT
Table1.ID
FROM Population');

INSERT INTO #Table1
EXEC (@DBTables);
```

Copy

#### Snowflake[¶](#id22 "Link to this heading")

```
  insertIntoTemporaryTable(`SELECT Table1.ID FROM MYDB.PUBLIC.Population)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table1 SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)
  
  insertIntoTemporaryTable(`${DBTABLES}`)
  EXEC(`INSERT INTO MYDB.PUBLIC.T_Table1 SELECT * FROM MYDB.PUBLIC.SnowConvertPivotTemporaryTable`);
  EXEC(`DROP TABLE SnowConvertPivotTemporaryTable`)
```

Copy

### BEGIN TRANSACTION[¶](#begin-transaction "Link to this heading")

BEGIN TRANSACTION is transformed to Snowflake’s BEGIN command, and inserted into an EXEC helper call.

The helper is in charge of actually executing the resulting BEGIN.

#### SQL Server[¶](#id23 "Link to this heading")

```
 -- Input code
BEGIN TRAN @transaction_name;
```

Copy

#### Snowflake[¶](#id24 "Link to this heading")

```
 // Output code
EXEC(`BEGIN`, []);
```

Copy

### COMMIT TRANSACTION[¶](#commit-transaction "Link to this heading")

COMMIT TRANSACTION is transformed to Snowflake’s COMMIT command, and inserted into an EXEC helper call.

The helper is in charge of actually executing the resulting COMMIT.

#### SQL Server[¶](#id25 "Link to this heading")

```
 -- Input code
COMMIT TRAN @transaction_name;
```

Copy

#### Snowflake[¶](#id26 "Link to this heading")

```
 // Output code
EXEC(`COMMIT`, []);
```

Copy

### ROLLBACK TRANSACTION[¶](#rollback-transaction "Link to this heading")

ROLLBACK TRANSACTION is transformed to Snowflake’s ROLLBACK command, and inserted into an EXEC helper call.

The helper is in charge of actually executing the resulting ROLLBACK .

#### SQL Server[¶](#id27 "Link to this heading")

```
 -- Input code
ROLLBACK TRAN @transaction_name;
```

Copy

#### Snowflake[¶](#id28 "Link to this heading")

```
 // Output code
EXEC(`ROLLBACK`, []);
```

Copy

### WAITFOR DELAY[¶](#waitfor-delay "Link to this heading")

WAITFOR DELAY clause is transformed to Snowflake’s `SYSTEM$WAIT` function. The *time\_to\_pass* parameter of the DELAY is transformed to seconds, for usage as a parameter in the `SYSTEM$WAIT` function.

The other variants of the WAITFOR clause are not supported in Snowflake, and are therefore marked with the corresponding message.

#### SQL Server[¶](#id29 "Link to this heading")

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

Copy

#### Snowflake[¶](#id30 "Link to this heading")

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

Copy

## 3. Cursors[¶](#cursors "Link to this heading")

Since `CURSORS` are not supported in Snowflake, SnowConvert AI maps their functionality to a `JavaScript` helper that emulates the original behavior in the target platform. Example:

### SQL Server[¶](#id31 "Link to this heading")

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

Copy

#### Snowflake[¶](#id32 "Link to this heading")

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

Copy

### DECLARE CURSOR[¶](#declare-cursor "Link to this heading")

#### SQL Server[¶](#id33 "Link to this heading")

```
DECLARE myCursor1 CURSOR FOR SELECT COL1 FROM TABLE1
```

Copy

#### Snowflake[¶](#id34 "Link to this heading")

```
let myCursor1 = new CURSOR(`SELECT COL1 FROM TABLE1`,() => []);
```

Copy

### OPEN[¶](#open "Link to this heading")

#### SQL Server[¶](#id35 "Link to this heading")

```
OPEN myCursor1
OPEN GLOBAL myCursor2
```

Copy

#### Snowflake[¶](#id36 "Link to this heading")

```
myCursor1.OPEN();
myCursor2.OPEN()
```

Copy

### FETCH[¶](#fetch "Link to this heading")

#### SQL Server[¶](#id37 "Link to this heading")

```
DECLARE @VALUE1 INT
FETCH NEXT FROM myCursor1 into @VALUE1
```

Copy

#### Snowflake[¶](#id38 "Link to this heading")

```
var VALUE1;
myCursor1.FETCH_NEXT();
VALUE1 = myCursor1.INTO();
```

Copy

### CLOSE[¶](#close "Link to this heading")

#### SQL Server[¶](#id39 "Link to this heading")

```
CLOSE myCursor1
CLOSE GLOBAL myCursor2
```

Copy

#### Snowflake[¶](#id40 "Link to this heading")

```
myCursor1.CLOSE()
myCursor2.CLOSE()
```

Copy

### DEALLOCATE[¶](#deallocate "Link to this heading")

#### SQL Server[¶](#id41 "Link to this heading")

```
DEALLOCATE myCursor1
DEALLOCATE GLOBAL myCursor2
```

Copy

#### Snowflake[¶](#id42 "Link to this heading")

```
myCursor1.DEALLOCATE()
myCursor2.DEALLOCATE()
```

Copy

### @@FETCH\_STATUS[¶](#fetch-status "Link to this heading")

#### SQL Server[¶](#id43 "Link to this heading")

```
 @@FETCH_STATUS
```

Copy

#### Snowflake[¶](#id44 "Link to this heading")

```
myCursor1.FETCH_STATUS()
```

Copy

### @@CURSOR\_ROWS[¶](#cursor-rows "Link to this heading")

#### SQL Server[¶](#id45 "Link to this heading")

```
 @@CURSOR_ROWS
```

Copy

#### Snowflake[¶](#id46 "Link to this heading")

```
myCursor1.FETCH_STATUS()
```

Copy

## 4. Expressions[¶](#expressions "Link to this heading")

### Binary Operations[¶](#binary-operations "Link to this heading")

#### SQL Server[¶](#id47 "Link to this heading")

```
SET @var1 = 1 + 1;
SET @var1 = 1 - 1;
SET @var1 = 1 / 1;
SET @var1 = 1 * 1;
SET @var1 = 1 OR 1;
SET @var1 = 1 AND 1;
```

Copy

#### Snowflake[¶](#id48 "Link to this heading")

```
VAR1 = 1 + 1;
VAR1 = 1 - 1;
VAR1 = 1 / 1;
VAR1 = 1 * 1;
VAR1 = 1 || 1;
VAR1 = 1 && 1;
```

Copy

### Conditionals[¶](#conditionals "Link to this heading")

#### SQL Server[¶](#id49 "Link to this heading")

```
@var1 > 0
@var1 = 0
@var1 < 0
@var1 <> 0
```

Copy

#### Snowflake[¶](#id50 "Link to this heading")

```
VAR1 > 0
VAR1 = 0
VAR1 < 0
VAR1 != 0
```

Copy

#### NULL Predicate[¶](#null-predicate "Link to this heading")

##### SQL Server[¶](#id51 "Link to this heading")

```
@var1 is null
@var2 is not null
```

Copy

##### Snowflake[¶](#id52 "Link to this heading")

```
VAR1 == null
VAR2 != null
```

Copy

## 5. Labels and Goto[¶](#labels-and-goto "Link to this heading")

`Labels` have not the same behavior in JavaScript as SQL Server has. To simulate the behavior, they are being transformed to `functions` . Its usage is being replaced with a call of the generated function that contains all the logic of the label. Example:

### Source Code[¶](#source-code "Link to this heading")

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

Copy

#### Snowflake[¶](#id53 "Link to this heading")

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

Copy

As you see in the example above, the function declarations that were the labels in the source code, will be put at the end of the code in order to make it cleaner.

`GOTO` is another command that does not exist in JavaScript. To simulate its behavour, their usages are being transformed to calls to the function (label) that is referenced, preceded by a return statement. Example:

#### SQL Server[¶](#id54 "Link to this heading")

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

Copy

#### Snowflake[¶](#id55 "Link to this heading")

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

Copy

As you see in the example above, the `return` is added to the function call, in order to stop the code flow as SQL Server does with the `GOTO` .

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.
2. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [1. CREATE PROCEDURE Translation](#create-procedure-translation)
2. [2. Variables](#variables)
3. [3. Statements translation](#statements-translation)
4. [3. Cursors](#cursors)
5. [4. Expressions](#expressions)
6. [5. Labels and Goto](#labels-and-goto)
7. [Related EWIs](#related-ewis)