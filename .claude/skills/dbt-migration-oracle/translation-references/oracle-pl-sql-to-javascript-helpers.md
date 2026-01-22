---
description:
  In this section you will find the helper functions used inside procedures that are used to achieve
  functional equivalence of some Oracle features that are not supported natively in Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-javascript/helpers
title: SnowConvert AI - Oracle - Javascript Helpers | Snowflake Documentation
---

## Between operator helper

### Between Operator Helper Function Definition

```sql
var BetweenFunc = function (expression,startExpr,endExpr) {
   if ([expression,startExpr,endExpr].some((arg) => arg == null)) {
      return null;
   }
   return expression >= startExpr && expression <= endExpr;
};
```

## Concat Value Helper

### Note

This helper also uses [IS NULL helper.](#is-null-helper)

### Concat Helper Function Definition

Helper method used to concatenate values in a JavaScript Template Literal. This is necessary to
check if values are null or not. Oracle handles null values as empty strings in concatenations.

```sql
 :force:
 var concatValue = (arg) => IS_NULL(arg) ? "" : arg;
```

## Cursor Helper

### Note 2

You might also be interested in:

- [Cursor FOR LOOP.](README.html#cursor-for-loop)
- [OPEN, FETCH and CLOSE statements](README.html#open-fetch-and-close-statement).
- [Cursor declaration.](README.html#cursor-declarations-and-definition)

### Note 3

This helper also uses [Raise helper](#raise-helper) and [EXEC helper](#exec-helper).

### Cursor Helper Function Definition

```sql
var FETCH_INTO_COLLECTIONS = function (collections,fetchValues) {
   for(let i = 0;i < collections.length;i++) {
      collections[i].push(fetchValues[i]);
   }
};
var CURSOR = function (stmt,binds,isRefCursor,isOut) {
   var statementObj, result_set, total_rows, ISOPEN = false, result_set_table = '', self = this, row_count, found;
   this.CURRENT = new Object;
   this.INTO = function () {
         return self.res;
      };
   this.OPEN = function (openParameters) {
         if (ISOPEN && !isRefCursor) RAISE(-6511,"CURSOR_ALREADY_OPEN","cursor already open");
         var finalStmt = openParameters && openParameters.query || stmt;
         var parameters = openParameters && openParameters.binds || [];
         var finalBinds = binds instanceof Function ? binds(...parameters) : binds;
         finalBinds = finalBinds || parameters;
         try {
            if (isOut) {
               if (!temptable_prefix) {
                  temptable_prefix = `${procname}_TEMP_${(EXEC(`select current_session() || '_' || to_varchar(current_timestamp, 'yyyymmddhh24missss')`,{
                        sql : 0
                     }))[0]}_`;
               }
               if (!result_set_table) {
                  result_set_table = temptable_prefix + outCursorResultNumber++;
                  EXEC(`CREATE OR REPLACE TEMPORARY TABLE ${result_set_table} AS ${finalStmt}`,{
                     sql : 0
                  });
               }
               finalStmt = "SELECT * FROM " + result_set_table
            }
            [result_set,statementObj,total_rows] = [EXEC(finalStmt,finalBinds,{
                  sql : 0,
                  row : 2
               }),_RS,_RS.getColumnCount()]
            ISOPEN = true;
            row_count = 0;
         } catch(error) {
            RAISE(error.code,"error",error.message);
         }
         return this;
      };
   this.NEXT = function () {
         if (total_rows && result_set.next()) {
            this.CURRENT = new Object;
            for(let i = 1;i <= statementObj.getColumnCount();i++) {
               (this.CURRENT)[statementObj.getColumnName(i)] = result_set.getColumnValue(i);
            }
            return true;
         } else return false;
      };
   this.FETCH = function (record) {
         var recordKeys = record ? Object.keys(record) : undefined;
         self.res = [];
         if (!ISOPEN) RAISE(-1001,"INVALID_CURSOR","invalid cursor");
         if (recordKeys && recordKeys.length != statementObj.getColumnCount()) RAISE(-6504,"ROWTYPE_MISMATCH","Return types of Result Set variables or query do not match");
         self.res = fetch(statementObj,result_set);
         if (self.res && self.res.length > 0) {
            found = true;
            row_count++;
            if (recordKeys) {
               for(let i = 0;i < self.res.length;i++) {
                  record[recordKeys[i]] = (self.res)[i];
               }
               return false;
            }
            return true;
         } else found = false;
         return false;
      };
   this.CLOSE = function () {
         if (!ISOPEN) RAISE(-1001,"INVALID_CURSOR","invalid cursor");
         found = row_count = result_set_table = total_rows = result_set = statementObj = undefined;
         ISOPEN = false;
      };
   this.FETCH_BULK_COLLECT_INTO = function (variables,limit) {
         if (variables.length != statementObj.getColumnCount()) RAISE(-6504,"ROWTYPE_MISMATCH","Return types of Result Set variables or query do not match");
         if (limit) {
            for(let i = 0;i < limit && this.FETCH();i++)FETCH_INTO_COLLECTIONS(variables,self.res);
         } else {
            while ( this.FETCH() )
               FETCH_INTO_COLLECTIONS(variables,self.res);
         }
      };
   this.FOUND = () => ISOPEN ? typeof(found) == "boolean" ? found : null : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
   this.NOTFOUND = () => ISOPEN ? typeof(found) == "boolean" ? !found : null : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
   this.ROWCOUNT = () => ISOPEN ? row_count : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
   this.ISOPEN = () => ISOPEN;
   this.SAVE_STATE = function () {
         return {
            tempTable : result_set_table,
            position : row_count
         };
      };
   this.RESTORE_STATE = function (tempTable,position) {
         result_set_table = tempTable
         if (result_set_table) {
            isOut = true
            this.OPEN();
            for(let i = 0;i < position;i++)this.FETCH();
         }
      };
   this.ROWTYPE = () => ROWTYPE(stmt,binds());
};
var outCursorResultNumber = 0;
```

## EXEC Helper

### Note 4

You might also be interested in:

- [DDL - DML Statements.](README.html#ddl-dml-statements)
- [Commit.](README.html#commit)
- [Execute Immediate.](README.html#execute-immediate)

### Note 5

EXEC helper depends on [IS NULL helper](#is-null-helper).

### Syntax

EXEC(stmt) EXEC(stmt, binds[]) EXEC(stmt, opts{}) EXEC(stmt, binds[], opts{})

### Parameters

#### stmt

The string of the SQL statement to execute.

#### binds (optional)

An array with the values or the variables to bind into the SQL statement.

#### opts (optional)

This is a Javascript object to describe how the values returned by the exec should be formated, this
is used for SELECT statements.

##### Valid arguments for opts parameter

The following tables describe, how arguments should be sent to opts parameter in EXEC call:

##### Options when a query returns a single row

<!-- prettier-ignore -->
|opts|description|
|---|---|
|{ }|When opts is empty or not sent to exec call, the data will be returned inside an array.|
|{vars: 0}|This has the same effect as the default option. It will return the data inside an array.|
|{vars: 1}|This is used when a query returns just one column and one row. EXEC will return the value directly. This is equivalent to EXEC[stmt](0)|
|{rec:recordVariable}|Used when you want to store the values returned by the query inside a record. Translation of records is described in [Records translation reference](README.html#collections-records). Record variable should be passed as an argument.|
|{row: 1}|This option returns a copy of ResultSet, this means that the object returned contains the methods described in [ResultSet Snowflake documentation](https://docs.snowflake.com/en/sql-reference/stored-procedures-api.html#object-resultset).|

##### Options when a query returns multiple rows

<!-- prettier-ignore -->
|opts|Description|
|---|---|
|{row:2}|With this option, it always returns a copy of the ResultSet regardless of the number of rows returned by the EXEC.|

##### General options

<!-- prettier-ignore -->
|opts|Description|
|---|---|
|{sql:0}|It makes sure that the [SQL implicit Cursor attribute](#implicit-cursor-attribute-helper) is not modified after executing the statement.|

### EXEC Helper Function Definition

```sql
var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
var fixBind = function (arg) {
   arg = arg instanceof Date ? formatDate(arg) : IS_NULL(arg) ? null : arg;
   return arg;
};
var _RS, _ROWS, SQLERRM = "normal, successful completion", SQLCODE = 0;
var getObj = (_rs) => Object.assign(new Object(),_rs);
var getRow = (_rs) => (values = Object.values(_rs)) && (values = values.splice(-1 * _rs.getColumnCount())) && values;
var fetch = (_RS,_ROWS,fmode) => _RS.getRowCount() && _ROWS.next() && (fmode ? getObj : getRow)(_ROWS) || (fmode ? new Object() : []);

var EXEC = function (stmt,binds,opts) {
   try {
      binds = !(arguments[1] instanceof Array) && ((opts = arguments[1]) && []) || (binds || []);
      opts = opts || new Object();
      binds = binds ? binds.map(fixBind) : binds;
      _RS = snowflake.createStatement({
            sqlText : stmt,
            binds : binds
         });
      _ROWS = _RS.execute();
      if (opts.sql !== 0) {
         var isSelect = stmt.toUpperCase().trimStart().startsWith("SELECT");
         var affectedRows = isSelect ? _RS.getRowCount() : _RS.getNumRowsAffected();
         SQL.FOUND = affectedRows != 0;
         SQL.NOTFOUND = affectedRows == 0;
         SQL.ROWCOUNT = affectedRows;
      }
      if (opts.row === 2) {
         return _ROWS;
      }
      var INTO = function (opts) {
         if (opts.vars == 1 && _RS.getColumnCount() == 1 && _ROWS.next()) {
            return _ROWS.getColumnValue(1);
         }
         if (opts.rec instanceof Object && _ROWS.next()) {
            var recordKeys = Object.keys(opts.rec);
            Object.assign(opts.rec,Object.fromEntries(new Map(getRow(_ROWS).map((element,Index) => [recordKeys[Index],element]))))
            return opts.rec;
         }
         return fetch(_RS,_ROWS,opts.row);
      };
      var BULK_INTO_COLLECTION = function (into) {
         for(let i = 0;i < _RS.getRowCount();i++) {
            FETCH_INTO_COLLECTIONS(into,fetch(_RS,_ROWS,opts.row));
         }
         return into;
      };
      if (_ROWS.getRowCount() > 0) {
         return _ROWS.getRowCount() == 1 ? INTO(opts) : BULK_INTO_COLLECTION(opts);
      }
   } catch(error) {
      RAISE(error.code,error.name,error.message)
   }
};
```

### Usage Samples

The following code examples illustrates how EXEC works.

#### EXEC simple case

##### Oracle

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC AS
BEGIN
  --CREATES HARDWARE TABLE WITH COLUMNS ID, DEVICE AND COLOR
  --THIS IS AN EXECUTE IMMEDIATE JUST WITH AN STATEMENT
  EXECUTE IMMEDIATE 'CREATE TABLE HARDWARE (ID NUMBER, DEVICE VARCHAR2(15), COLOR VARCHAR(15))';
END;
```

##### Snowflake

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  //CREATES HARDWARE TABLE WITH COLUMNS ID, DEVICE AND COLOR
  //THIS IS AN EXECUTE IMMEDIATE JUST WITH AN STATEMENT
  EXEC(`CREATE OR REPLACE TABLE HARDWARE (ID NUMBER(38, 18),
   DEVICE VARCHAR(15),
   COLOR VARCHAR(15))`);
$$;
```

#### EXEC with bindings

##### Oracle 2

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC AS
  ID_VAR NUMBER;
  DEVICE_VAR VARCHAR2(15);
  DEV_COLOR  VARCHAR2(15);
  COLOR_VAR  VARCHAR2(15);
BEGIN
  --EXEC WITH BINDINGS
  --INSERTS A ROW WITH  | 12 | MOUSE | BLACK |  VALUES USING DIRECT BINDING FOR MOUSE
  EXECUTE IMMEDIATE 'INSERT INTO HARDWARE VALUES (12, :MOUSE, ''BLACK'')' USING 'MOUSE';

  --INSERTS A ROW WITH  | 13 | KEYBOARD | WHITE |  VALUES USING DIRECT BINDING FOR 13 AND KEYBOARD
  EXECUTE IMMEDIATE 'INSERT INTO HARDWARE VALUES (:ID, :KEYBOARD, ''WHITE'')' USING 13, 'KEYBOARD';

  --INSERTS A ROW WITH  | 14 | HEADSET | GRAY |  VALUES USING BINDING VARIABLES
  ID_VAR := 14;
  DEVICE_VAR := 'HEADSET';
  COLOR_VAR := 'GRAY';
  EXECUTE IMMEDIATE 'INSERT INTO HARDWARE VALUES (:DEV_ID, :DEV_VAR, :DEV_COLOR)' USING  ID_VAR, DEVICE_VAR, COLOR_VAR;
END;
```

##### Snowflake 2

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let ID_VAR;
  let DEVICE_VAR;
  let DEV_COLOR;
  let COLOR_VAR;
  //EXEC WITH BINDINGS
  //INSERTS A ROW WITH  | 12 | MOUSE | BLACK |  VALUES USING DIRECT BINDING FOR MOUSE
  EXEC(`INSERT INTO HARDWARE
VALUES (12, ?, 'BLACK')`,[`MOUSE`]);
  //INSERTS A ROW WITH  | 13 | KEYBOARD | WHITE |  VALUES USING DIRECT BINDING FOR 13 AND KEYBOARD
  EXEC(`INSERT INTO HARDWARE
VALUES (?, ?, 'WHITE')`,[13,`KEYBOARD`]);

  //INSERTS A ROW WITH  | 14 | HEADSET | GRAY |  VALUES USING BINDING VARIABLES
  ID_VAR = 14;
  DEVICE_VAR = `HEADSET`;
  COLOR_VAR = `GRAY`;
  EXEC(`INSERT INTO HARDWARE
VALUES (?, ?, ?)`,[ID_VAR,DEVICE_VAR,COLOR_VAR]);
$$;
```

#### EXEC with options

##### Oracle 3

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC AS
BEGIN
  --STORES THE ID INTO ID_VAR
  EXECUTE IMMEDIATE 'SELECT ID FROM HARDWARE WHERE COLOR = ''BLACK''' INTO ID_VAR;
  DBMS_OUTPUT.PUT_LINE(ID_VAR);

  --STORES THE ID AND DEVICE INTO ID_VAR AND DEV_VAR, USING BINDING FOR COLOR
  COLOR_VAR := 'BLACK';
  EXECUTE IMMEDIATE 'SELECT ID, DEVICE FROM HARDWARE WHERE COLOR = :DEV_COLOR' INTO ID_VAR, DEVICE_VAR USING COLOR_VAR;
  DBMS_OUTPUT.PUT_LINE(ID_VAR || ' ' || DEVICE_VAR);
END;
```

##### Snowflake 3

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  //STORES THE ID INTO ID_VAR
  [ID_VAR] = EXEC(`SELECT ID FROM
   HARDWARE
WHERE COLOR = 'BLACK'`);
  EXEC(`--** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
CALL DBMS_OUTPUT.PUT_LINE_UDF(ID_VAR)`);

  //STORES THE ID AND DEVICE INTO ID_VAR AND DEV_VAR, USING BINDING FOR COLOR
  COLOR_VAR = `BLACK`;
  [ID_VAR,DEVICE_VAR] = EXEC(`SELECT ID, DEVICE FROM
   HARDWARE
WHERE COLOR = ?`,[
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT COLOR_VAR MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    COLOR_VAR]);
  EXEC(`--** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
CALL DBMS_OUTPUT.PUT_LINE_UDF(NVL(ID_VAR :: STRING, '') || ' ' || NVL(DEVICE_VAR :: STRING, ''))`);
$$;
```

For the following sample, EXEC call returns [12], with object destructuring `ID_VAR` stores 12:

```sql
[ID_VAR] = EXEC(`SELECT ID FROM PUBLIC.HARDWARE WHERE COLOR = 'BLACK'`);
```

The following two EXEC calls are alternative ways for the previous sample without object
destructuring:

```sql
ID_VAR = EXEC(`SELECT ID FROM PUBLIC.HARDWARE WHERE COLOR = 'BLACK'`)[0];
ID_VAR = EXEC(`SELECT ID FROM PUBLIC.HARDWARE WHERE COLOR = 'BLACK'`, {vars:1});
```

Object destructuring also works with bindings as you may note on these statements (EXEC call returns
[12, “MOUSE”] values):

```sql
COLOR_VAR = `BLACK`;
[ID_VAR,DEVICE_VAR] = EXEC(`SELECT ID, DEVICE FROM PUBLIC.HARDWARE WHERE COLOR = ?`,[COLOR_VAR]);
```

To obtain the actual result set returned by Snowflake, you can use this synaxis:

```sql
let RESULT_SET_COPY;
RESULT_SET_COPY = EXEC(`SELECT * FROM PUBLIC.HARDWARE WHERE COLOR = 'BLACK'`, {row:1});
/* RETURNS
{
  "COLOR": "BLACK",
  "DEVICE": "MOUSE",
  "ID": 12,
  "getColumnCount": {},
  ...
  "next": {}
}*/
```

#### EXEC with record types

##### Note 6

You might be interested in [Records transformation](README.html#collections-records).

##### Oracle 4

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC AS
  TYPE DEVTRECTYP IS RECORD (
    ID NUMBER(4) NOT NULL := 0,
    DEV_TYPE VARCHAR2(30) NOT NULL := 'UNKNOWN',
    COLOR VARCHAR2(30) := 'GREEN'
  );

  DEV_VARIABLE DEVTRECTYP;
BEGIN

  --STORES THE ROW VALUES IN THE RECORD
  EXECUTE IMMEDIATE 'SELECT * FROM HARDWARE WHERE COLOR = ''BLACK''' INTO DEV_VARIABLE;
  DBMS_OUTPUT.PUT_LINE(DEV_VARIABLE.ID || ' ' || DEV_VARIABLE.DEV_TYPE || ' ' || DEV_VARIABLE.COLOR);
END;
```

##### Snowflake 4

```sql
CREATE OR REPLACE PROCEDURE EXECUTE_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  class DEVTRECTYP {
    ID = 0
    DEV_TYPE = `UNKNOWN`
    COLOR = `GREEN`
    constructor() {
      [...arguments].map((element,Index) => this[(Object.keys(this))[Index]] = element)
    }
  }
  let DEV_VARIABLE = new DEVTRECTYP();
  //STORES THE ROW VALUES IN THE RECORD
  EXEC(`SELECT * FROM
   HARDWARE
WHERE COLOR = 'BLACK'`,{
    rec : DEV_VARIABLE
  });
  EXEC(`--** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
CALL DBMS_OUTPUT.PUT_LINE_UDF(NVL(? :: STRING, '') || ' ' || NVL(? :: STRING, '') || ' ' || NVL(? :: STRING, ''))`,[DEV_VARIABLE.ID,DEV_VARIABLE.DEV_TYPE,DEV_VARIABLE.COLOR]);
$$;
```

Warning

This is still a work in progress. The transformation to properly store the record values will be:

```sql
EXEC(`SELECT * FROM PUBLIC.HARDWARE WHERE COLOR = 'BLACK'`, {rec:DEV_VARIABLE});
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0053):
   Object may not work.
2. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation

## Implicit Cursor attribute helper

### Overview

These are the attributes that you can use inside Snowflake stored procedures using this helper:

- FOUND
- NOTFOUND
- ROWCOUNT
- ISOPEN

In Snowflake code, inside the procedures, you will find the initialization of these attributes:

```sql
 var SQL = {
  FOUND : false,
  NOTFOUND : false,
  ROWCOUNT : 0,
  ISOPEN : false
 };
```

The attribute ISOPEN is always false, just like in Oracle.

### Usage Samples 2

#### Oracle 5

```sql
CREATE OR REPLACE PROCEDURE PROC1
IS
VAR1 VARCHAR(100) := '';
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 WHERE COL1 = 1;
    VAR1 := 'Rows affected: ' || TO_CHAR(SQL%ROWCOUNT);
    VAR1 := 'Error: ' || SQLERRM;

    PKG.TEST_PROC1(SQL%ROWCOUNT, SQL%FOUND, SQL%NOTFOUND);
    PKG.TEST_PROC2(SQLCODE);

    SELECT SQL%ROWCOUNT FROM DUAL;
END;
```

#### Snowflake 5

```sql
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let VAR1 = undefined;
    [VAR1] = EXEC(`SELECT
   COL1
FROM
   TABLE1
WHERE COL1 = 1`);
    VAR1 = `Rows affected: ${concatValue((EXEC(`SELECT
   TO_CHAR(?)`,[SQL.ROWCOUNT]))[0])}`;
    VAR1 = `Error: ${concatValue(SQLERRM)}`;
    EXEC(`CALL

PKG.TEST_PROC1(?, ?, ?)`,[SQL.ROWCOUNT,SQL.FOUND,SQL.NOTFOUND]);
    EXEC(`CALL
PKG.TEST_PROC2(?)`,[SQLCODE]);
    EXEC(`SELECT
       ?
    FROM DUAL`,[SQL.ROWCOUNT]);
$$;
```

##### Note 7

SQLCODE and SQLERRM are converted into helper variables with the same name and are bound in the same
way as the cursor variables.

### Known Issues 2

No issues were found.

### Related EWIs 2

No related EWIs.

## IS NULL Helper

### IS NULL Helper Function Definition

This helper method is used to transform the NULL predicate. It is also used by other helpers to
check if a value is null. This is necessary to handle values like NaN or empty strings as nulls.

Oracle handles empty strings as null values. This helper takes that into account.

```sql
var IS_NULL = (arg) => !(arg || arg === 0);
```

## Like operator Helper

### Like Operator Helper Function Definition

```sql
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

## Package variables helper

### Note 8

You might also be interested in [variables declaration](README.html#variables-declaration) and
[package variables inside procedures.](README.html#package-variables-inside-procedures)

### Package variables Helper Function Definition

#### Note 9

Helper depends on [IS NULL helper](#is-null-helper)

When a package variable is used inside a procedure, the following helper will be generated:

When a package variable is used inside a procedure, the following helper will be generated:

```sql
function StateManager(packageName,keepInCache) {
   function getTypeChar(arg) {
      if (arg instanceof Date) {
         return "&";
      } else if (typeof arg == "number") {
         return "#";
      } else if (IS_NULL(arg)) {
         return "~";
      } else {
         return "$";
      }
   }
   function deserialize(arg) {
      if (arg === null) return undefined;
      let prefix = arg[0];
      let rest = arg.substr(1);
      switch(prefix) {
         case "&":return new Date(rest);
         case "#":return parseFloat(rest);
         case "$":return rest;
         case "~":return undefined;
         default:return arg;
      }
   }
   function saveVar(varName,value) {
      let varPackageName = `${packageName}.${varName}`;
      let fixedValue = `${getTypeChar(value)}${fixBind(value)}`;
      EXEC("SELECT SETVARIABLE(?,?)",[varPackageName,fixedValue]);
   }
   function readVar(varName) {
      let varPackageName = `${packageName}.${varName}`;
      return deserialize((EXEC("SELECT GETVARIABLE(?)",[varPackageName]))[0]);
   }
   this.saveState = function () {
         let keys = Object.keys(this.cache);
         for(let key of keys) {
            saveVar(key,(this.cache)[key]);
         }
      }
   this.cache = new Object();
   let c = this.cache;
   let rsProxy = new Proxy(this,{
      get : function (target,prop,receiver) {
         if (!target[prop]) {
            c[prop] === undefined && (c[prop] = readVar(prop));
            return c[prop];
         }
         return Reflect.get(...arguments);
      },
      set : function (target,prop,value) {
         if (target[prop]) return;
         c[prop] = value;
         if (!keepInCache) {
            saveVar(prop,value);
         }
      }
   });
   return rsProxy;
};
var PACKAGE_VARIABLES = new StateManager("PACKAGE_VARIABLES",true);
```

A helper instance is created for each package used to access its variables. Variables will be
qualified with the name of the package if they are not qualified with it.

At the end of the procedure, the state of the variables used will be saved using the helper.

Note that in the following statement, name of the variable will change to match the package name:

```sql
var PACKAGE_VARIABLES = new StateManager("PACKAGE_VARIABLES",true);
```

## Raise Helper

### Note 10

You might be interested in
[Errors and Exception Handling.](README.html#errors-and-exception-handling)

### Raise Helper Function Definition

```sql
var RAISE = function (code,name,message) {
    message === undefined && ([name,message] = [message,name])
    var error = new Error(message);
    error.name = name
    SQLERRM = `${(SQLCODE = (error.code = code))}: ${message}`
    throw error;
};
```

## ROWTYPE Helper

### Note 11

You might be interested in [ROWTYPE Record Declaration.](#raise-helper-function-definition)

### ROWTYPE Helper Function Definition

```sql
var ROWTYPE = (stmt, binds = [], obj = new Object()) => {
      EXEC(`SELECT * FROM (${stmt}) LIMIT 0`,binds);
      for(let i = 1;i <= _RS.getColumnCount();i++)obj[_ROWS.getColumnName(i)] = null;
      return obj;
   };
```
