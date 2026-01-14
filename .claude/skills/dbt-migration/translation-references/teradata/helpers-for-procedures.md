---
description:
  In this section you will find the helper functions used inside procedures that are used to achieve
  functional equivalence of some Teradata features that are not supported natively in Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/helpers-for-procedures
title: SnowConvert AI - Teradata - SnowConvert AI Procedures Helpers | Snowflake Documentation
---

## Cursor Helper[¶](#cursor-helper)

This section describes the usage of different functions to achieve functional equivalence for
Teradata cursors in JavaScript.

The cursor helper is a function that contains the main four actions that Teradata cursors perform
such as Open, Fetch, Next, and Close.

- _CURSOR(),_ the main routine which declares the needed variables and other sub-routines.
- _OPEN(),_ opens the cursor executing the given statement, and updates the necessary variables.
- _NEXT(),_ moves the cursor to the next row (if any) of the statement and sets every column value
  to the current row.
- _FETCH(),_ obtains the values (if any) from the response of the statement executed.
- _CLOSE(),_ removes the temporary table from the \_OUTQUERIES (if it was added in the EXEC helper)
  and unsets the necessary variables.

Note

Some parts of the output code are omitted for clarity reasons.

### Cursor Sample Usage[¶](#cursor-sample-usage)

Teradata

```
 -- Additional Params: -t JavaScript
Replace procedure procedure1()
dynamic result sets 2
begin

    -------- Local variables --------
    declare sql_cmd varchar(20000) default ' ';
    declare num_cols integer;

    ------- Declare cursor with return only-------
    declare resultset cursor with return only for firststatement;

    ------- Declare cursor -------
    declare cur2 cursor for select count(columnname) from table1;

    -------- Set --------
    set sql_cmd='sel * from table1';

    -------- Prepare cursor --------
    prepare firststatement from sql_cmd;

    -------- Open cursors --------
    open resultset;
    open cur1;

    -------- Fetch -------------
    fetch cur1 into val1, val2;

    -------- Close cursor --------
    close cur1;
end;
```

Copy

Snowflake output

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    //------ Local variables --------
    var SQL_CMD = ` `;
    var NUM_COLS;
    var RESULTSET = new CURSOR(() => FIRSTSTATEMENT,[],true);
    //----- Declare cursor -------
    var CUR2 = new CURSOR(`SELECT
   COUNT(columnname)
from
   table1`,[],false);
    //------ Set --------
    SQL_CMD = `SELECT
   * from
   table1`;
    //------ Prepare cursor --------
    var FIRSTSTATEMENT = SQL_CMD;
    //------ Open cursors --------
    RESULTSET.OPEN();
    CUR1.OPEN();

        //------ Fetch -------------
    CUR1.FETCH() && ([val1,val2] = CUR1.INTO());
    //------ Close cursor --------
    CUR1.CLOSE();
    return PROCRESULTS();
$$;
```

Copy

#### Cursor Helper Function Definition[¶](#cursor-helper-function-definition)

```
 var CURSOR = function (stmt,binds,withReturn) {
	   var rs, rows, row_count, opened = false, resultsetTable = '', self = this;
	   this.CURRENT = new Object;
	   this.INTO = function () {
	         return self.res;
	      };
	   this.OPEN = function (usingParams) {
	         try {
	            if (usingParams) binds = usingParams;
	            if (binds instanceof Function) binds = binds();
	            var finalBinds = binds && binds.map(fixBind);
	            var finalStmt = stmt instanceof Function ? stmt() : stmt;
	            if (withReturn) {
	               resultsetTable = EXEC(finalStmt,finalBinds,true,null,{
	                     temp : true
	                  });
	               finalStmt = `SELECT * FROM TABLE(RESULT_SCAN('${resultsetTable}'))`;
	               finalBinds = [];
	            }
	            rs = snowflake.createStatement({
	                  sqlText : finalStmt,
	                  binds : finalBinds
	               });
	            rows = rs.execute();
	            row_count = rs.getRowCount();
	            ACTIVITY_COUNT = rs.getRowCount();
	            opened = true;
	            return this;
	         } catch(error) {
	            ERROR_HANDLERS && ERROR_HANDLERS(error);
	         }
	      };
	   this.NEXT = function () {
	         if (row_count && rows.next()) {
	            this.CURRENT = new Object;
	            for(let i = 1;i <= rs.getColumnCount();i++) {
	               (this.CURRENT)[rs.getColumnName(i)] = rows.getColumnValue(i);
	            }
	            return true;
	         } else return false;
	      };
	   this.FETCH = function () {
	         self.res = [];
	         self.res = fetch(row_count,rows,rs);
	         if (opened) if (self.res.length > 0) {
	            SQLCODE = 0;
	            SQLSTATE = '00000';
	         } else {
	            SQLCODE = 7362;
	            SQLSTATE = '02000';
	            var fetchError = new Error('There are not rows in the response');
	            fetchError.code = SQLCODE;
	            fetchError.state = SQLSTATE;
	            if (ERROR_HANDLERS) ERROR_HANDLERS(fetchError);
	         } else {
	            SQLCODE = 7631;
	            SQLSTATE = '24501';
	         }
	         return self.res && self.res.length > 0;
	      };
	   this.CLOSE = function () {
	         if (withReturn && _OUTQUERIES.includes(resultsetTable)) {
	            _OUTQUERIES.splice(_OUTQUERIES.indexOf(resultsetTable),1);
	         }
	         rs = rows = row_count = undefined;
	         opened = false;
	         resultsetTable = '';
	      };
	};
```

Copy

### Known Issues [¶](#known-issues)

No issues were found.

### Related EWIs [¶](#related-ewis)

No related EWIs.

## Exec Helper[¶](#exec-helper)

The exec helper is a function used to execute SQL statements in procedures.

### Syntax[¶](#syntax)

EXEC(stmt) EXEC(stmt, binds) EXEC(stmt, binds, noCatch) EXEC(stmt, binds, noCatch, catchFunction)
EXEC(stmt, binds, noCatch, catchFunction, opts)

### Parameters[¶](#parameters)

#### stmt[¶](#stmt)

The string of the SQL statement to execute.

#### binds (optional)[¶](#binds-optional)

An array with the values or the variables to bind into the SQL statement.

#### NoCatch (optional)[¶](#nocatch-optional)

Boolean to know if an error should not be catched.

#### catchFunction (optional)[¶](#catchfunction-optional)

A function to execute in case an error occurs during the execution of the exec function.

#### opts (optional)[¶](#opts-optional)

A JSON object ({ temp : true }) to know if the query ID should be returned.

### FixBind And FormatDate Functions[¶](#fixbind-and-formatdate-functions)

The Exec helper uses a function defined in the helpers called FixBind. This function uses the
FormatDate function when it encounters that one of the binding variables is a date type, this is
done to manage properly the date types in Snowflake. Both functions are defined as below.

```
 var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
	var fixBind = function (arg) {
	   arg = arg == undefined ? null : arg instanceof Date ? formatDate(arg) : arg;
	   return arg;
	};
```

Copy

Note

Some parts of the output code are omitted for clarity reasons.

#### Exec Usage Sample[¶](#exec-usage-sample)

Teradata

```
 -- Additional Params: -t JavaScript
REPLACE PROCEDURE ProcedureSample ()
BEGIN

case value
when 0 then
  select * from table1
else
  update table1 set name = "SpecificValue" where id = value;
end case

END;
```

Copy

Snowflake output

```
 CREATE OR REPLACE PROCEDURE ProcedureSample ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  switch(value) {
    case 0:EXEC(`SELECT * from table1`,[]);
    break;
    default:EXEC(`UPDATE table1
    set
      name = "SpecificValue"
    where
      id = value`,[]);
    break;
  }
$$;
```

Copy

#### Exec Helper Definition[¶](#exec-helper-definition)

```
 var EXEC = function (stmt,binds,noCatch,catchFunction,opts) {
	   try {
	      binds = binds ? binds.map(fixBind) : binds;
	      _RS = snowflake.createStatement({
	            sqlText : stmt,
	            binds : binds
	         });
	      _ROWS = _RS.execute();
	      ROW_COUNT = _RS.getRowCount();
	      ACTIVITY_COUNT = _RS.getNumRowsAffected();
	      HANDLE_NOTFOUND && HANDLE_NOTFOUND(_RS);
	      if (INTO) return {
	         INTO : function () {
	            return INTO();
	         }
	      };
			  if (_OUTQUERIES.length < DYNAMIC_RESULTS) _OUTQUERIES.push(_ROWS.getQueryId());
	      if (opts && opts.temp) return _ROWS.getQueryId();
	   } catch(error) {
	      MESSAGE_TEXT = error.message;
	      SQLCODE = error.code;
	      SQLSTATE = error.state;
	      var msg = `ERROR CODE: ${SQLCODE} SQLSTATE: ${SQLSTATE} MESSAGE: ${MESSAGE_TEXT}`;
	      if (catchFunction) catchFunction(error);
	      if (!noCatch && ERROR_HANDLERS) ERROR_HANDLERS(error); else throw new Error(msg);
	   }
	};
```

Copy

### Known Issues [¶](#id1)

No issues were found.

### Related EWIs [¶](#id2)

No related EWIs.

## Functional Equivalence Helpers[¶](#functional-equivalence-helpers)

A list of helpers functions in JavaScript that procedures in SnowFlake can use, in order to better
support several Teradata language features.

Depending on what is in each Stored Procedure in Teradata, SnowConvert AI will create one or more of
the following javascript functions inside them.

### **_CompareDates_**[¶](#comparedates)

A function that compares dates handling nullity. In Javascript, it is needed to call _.getTime()_
for date comparisons.

```
 var CompareDates = function(value1, value2) {
	var value1Time = value1 && value1.getTime() || null;
	var value2Time = value2 && value2.getTime() || null;
	if (value1Time == null && value2Time == null) return null; /*in SQL null == null is equal to null as well as any other comparison */
	return value1Time > value2Time? 1 : value1Time<value2Time? -1 : 0;
}
```

Copy

### **_BetweenFunc_**[¶](#betweenfunc)

A function to handle the _BETWEEN_ statement in Teradata.

```
 var BetweenFunc = function (expression,startExpr,endExpr) {
	if ([expression,startExpr,endExpr].some((arg) => arg == null)) {
		  return false;
	}
	return expression >= startExpr && expression <= endExpr;
};
```

Copy

### **_LikeFunction()_**[¶](#likefunction)

A function to handle the _LIKE_ statement in Teradata.

```
 var likeFunction = function (leftExpr,rightExpr) {
	RegExp.escape = function (text) {
		if (!arguments.callee.sRE) {
			var specials = ['/','.','*','+','?','|','(',')','[',']','{','}','\\'];
			arguments.callee.sRE = new RegExp('(\\' + specials.join('|\\') + ')','g');
		}
		return text.replace(arguments.callee.sRE,'\\$1');
	}
	var likeExpr = RegExp.escape(rightExpr);
	var likeResult = new RegExp(likeExpr.replace('%','.*').replace('_','.')).exec(leftExpr) != null;
	return likeResult;
};
```

Copy

### **_ERROR_HANDLERS()_**[¶](#error-handlers)

The main error-handling routine.

```
 var continue_handler_1 = function (error) {
   {
	  V_SQL_VALUE = SQLSTATE;
	  V_EXCEPTION_FLAG = `Y`;
   }
};

// Main error-handling routine
var ERROR_HANDLERS = function (error) {
   switch(error.state) {
	  //Conversion Warning - handlers for the switch default (SQLWARNING/SQLEXCEPTION/NOT FOUND) can be the following
	  default:continue_handler_1(error);
   }
};
```

Copy

### **_INSERT_TEMP_**[¶](#insert-temp)

Warning

**_This helper has been deprecated in stored procedures since version 2.0.15._**

A function to create a temporary table using the argument _query_ with the given _parameters_.

```
 var procname = `PUBLIC.Procedure1`;
var temptable_prefix, tablelist = [];
var INSERT_TEMP = function (query,parameters) {
		if (!temptable_prefix) {
	  		var sql_stmt = `select current_session() || '_' || to_varchar(current_timestamp, 'yyyymmddhh24missss')`;
	      var rs = snowflake.createStatement({
	         sqlText : sql_stmt,
	         binds : []
	      }).execute();
	      temptable_prefix = rs.next() && (procname + '_TEMP_' + rs.getColumnValue(1) + '_');
	  }
	  var tablename = temptable_prefix + tablelist.length;
	  tablelist.push(tablename);
	  var sql_stmt = `CREATE OR REPLACE TEMPORARY TABLE ${tablename} AS ${query}`;
	  snowflake.execute({
	  		sqlText : sql_stmt,
	      binds : parameters
	  });
	  return tablename;
};
```

Copy

### **_IS_NOT_FOUND()_**[¶](#is-not-found)

A function that validates when a SELECT returns no values or a sentence affects zero rows. This is
done in order to emulate the same behavior as Teradata, when there are exits or continue handlers
for NOT FOUND EXCEPTIONS.

```
 let IS_NOT_FOUND = (stmt) => {
	   let n = -1;
	   let cmd = stmt.getSqlText().replace(new RegExp("\\/\\*.*\\*\\/","gsi"),"").replace(new RegExp("--.*?\\n","gsi"),"");
	   let matched = cmd.match(new RegExp("\\s*(\\w+)\\s+"),"");
	   if (matched) {
	      cmd = matched[1].toUpperCase();
	      switch(cmd) {
		       case "CALL":
	         case "DROP":
	         case "CREATE":
	         case "ALTER":
	         case "SELECT":
								n = stmt.getRowCount();
	         break;
	         default:n = stmt.getNumRowsAffected();
	         break;
	      }
	   }
	   return n == 0;
	};
```

Copy

### **_HANDLE_NOTFOUND()_**[¶](#handle-notfound)

This function uses the above _IS_NOT_\_FOUND function to validate when an artificial error ‘NOT
FOUND’ is being thrown.

```
  	let HANDLE_NOTFOUND = (stmt) => {
	   if (IS_NOT_FOUND(stmt) && (error = new Error('NOT_FOUND')) && (NOT_FOUND = true) && ([error.code,error.state] = ['020000','020000'])) throw error;
	};
```

Copy

### PROCRESULTS()[¶](#procresults)

A function that takes zero or multiple output parameters and binds them with the \_OUTQUERIES in an
array in order to be returned.

```
 let PROCRESULTS = (...OUTPARAMS) => JSON.stringify([...OUTPARAMS,[..._OUTQUERIES]]);
```

Copy

### Known Issues [¶](#id3)

No issues were found.

### Related EWIs [¶](#id4)

No related EWIs.

## Into Helper[¶](#into-helper)

The into function is used to extract the resulting rows from a subquery or from a select into
statement.

### Fetch Function[¶](#fetch-function)

The INTO helper uses a fetch function to get the row from a resulting query. The definition of the
Fetch Function is described below.

```
 var fetch = (count,rows,stmt) =>
(count && rows.next() && Array.apply(null,Array(stmt.getColumnCount())).map((_,i)
=> rows.getColumnValue(i + 1))) || [];
```

Copy

Note

Some parts of the output code are omitted for clarity reasons.

### Into Sample Usage[¶](#into-sample-usage)

Teradata

```
 -- Additional Params: -t JavaScript
REPLACE PROCEDURE SubQuerypoc ()
BEGIN

DECLARE monat INTEGER;
SET monat      = (SELECT column1
             FROM table1);
END;
```

Copy

Snowflake output

```
CREATE OR REPLACE PROCEDURE SubQuerypoc ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var MONAT;
    EXEC(`(SELECT column1 FROM table1)`,[]);
    var subQueryVariable0;
    [subQueryVariable0] = INTO();
    MONAT = subQueryVariable0;
$$;
```

Copy

### Into Helper function Definition[¶](#into-helper-function-definition)

```
 var INTO = () => fetch(ROW_COUNT,_ROWS,_RS);
```

Copy

### Known Issues [¶](#id5)

No issues were found.

### Related EWIs [¶](#id6)

No related EWIs.
