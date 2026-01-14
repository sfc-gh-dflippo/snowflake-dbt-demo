---
description:
  In this section you will find helper functions or procedures that are used to achieve functional
  equivalence of some Oracle features that are not supported natively in Snowflake Scripting.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/helpers
title: SnowConvert AI - Oracle - HELPERS | Snowflake Documentation
---

## Bulk Cursor Helpers[¶](#bulk-cursor-helpers)

Note

You might also be interested in [Default FORALL transformation](README.html#forall).

The Cursor is simulated with an `OBJECT` with different information regarding the state of the
cursor. A temporary table is created to store the result set of the cursor’s query.

Most of these Procedures return a new Object with the updated state of the cursor.

### INIT_CURSOR[¶](#init-cursor)

This function initializes a new object with the basic cursor information

```
CREATE OR REPLACE FUNCTION INIT_CURSOR(NAME VARCHAR, QUERY VARCHAR)
RETURNS OBJECT
AS
$$
  SELECT OBJECT_CONSTRUCT('NAME', NAME, 'ROWCOUNT', -1, 'QUERY', QUERY, 'ISOPEN', FALSE, 'FOUND', NULL, 'NOTFOUND', NULL)
$$;
```

Copy

### OPEN_BULK_CURSOR[¶](#open-bulk-cursor)

These procedures creates a temporary table with the query of the cursor. An optional overload exists
to support bindings.

```
CREATE OR REPLACE PROCEDURE OPEN_BULK_CURSOR(CURSOR OBJECT, BINDINGS ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var query = `CREATE OR REPLACE TEMPORARY TABLE ${CURSOR.NAME}_TEMP_TABLE AS ${CURSOR.QUERY}`;
  snowflake.execute({ sqlText: query, binds: BINDINGS });
  CURSOR.ROWCOUNT = 0;
  CURSOR.ISOPEN = true;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE OPEN_BULK_CURSOR(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL OPEN_BULK_CURSOR(:CURSOR, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

### CLOSE_BULK_CURSOR[¶](#close-bulk-cursor)

This procedure deletes the temporary table that stored the result set of the cursor and resets the
cursor’s properties to their initial state.

```
CREATE OR REPLACE PROCEDURE CLOSE_BULK_CURSOR(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var query = `DROP TABLE ${CURSOR.NAME}_TEMP_TABLE`;
  snowflake.execute({ sqlText: query });
  CURSOR.ROWCOUNT = -1;
  CURSOR.ISOPEN = false;
  CURSOR.FOUND = null;
  CURSOR.NOTFOUND = null;
  return CURSOR;
$$;
```

Copy

### FETCH Helpers[¶](#fetch-helpers)

Due to Oracle being capable of doing the `FETCH` statement on different kind of scenarios, a
multiple procedures with overloads were created to handle each case. These helpers save the fetched
values into the `RESULT` property in the `CURSOR` object.

Some of the overloads include variations when the `LIMIT` clause was used or not. Other overloads
have a `COLUMN_NAMES` argument that is necessary when the `FETCH` statement is being done into a
variable that has or contains a records with column names that are different to the column names of
the query.

#### FETCH_BULK_COLLECTION_RECORDS[¶](#fetch-bulk-collection-records)

These procedures are used when a `FETCH BULK` is done into a collection of records.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var objectConstructArgs = [];
  if (COLUMN_NAMES) {
    for (let i = 0 ; i < COLUMN_NAMES.length ; i++) {
      objectConstructArgs.push("'" + COLUMN_NAMES[i] + "'");
      objectConstructArgs.push('$' + (i + 1));
    }
  } else {
    objectConstructArgs.push('*');
  }
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT ARRAY_AGG(OBJECT_CONSTRUCT(${objectConstructArgs.join(', ')})) FROM (SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT})`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  resultSet.next();
  CURSOR.RESULT = resultSet.getColumnValue(1);
  CURSOR.ROWCOUNT += CURSOR.RESULT.length;
  CURSOR.FOUND = CURSOR.RESULT.length > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, NULL, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, LIMIT INTEGER)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, :LIMIT, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTION_RECORDS(CURSOR OBJECT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTION_RECORDS(:CURSOR, NULL, :COLUMN_NAMES));
    RETURN :RESULT;
  END;
$$;
```

Copy

#### FETCH_BULK_COLLECTIONS[¶](#fetch-bulk-collections)

These procedures are used when the `FETCH` statement is done into one or multiple collections. Since
the columns are specified in this `FETCH` operation, an override for specific `COLUMN_NAMES` is not
necessary.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTIONS(CURSOR OBJECT, LIMIT FLOAT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var limitClause = '';
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT}`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  var column_count = stmt.getColumnCount();
  CURSOR.RESULT = [];
  for (let i = 0 ; i < column_count ; i++) {
    CURSOR.RESULT[i] = [];
  }

  while (resultSet.next()) {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      CURSOR.RESULT[i - 1].push(resultSet.getColumnValue(columnName));
    }
  }
  CURSOR.ROWCOUNT += stmt.getRowCount();
  CURSOR.FOUND = stmt.getRowCount() > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_COLLECTIONS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_COLLECTIONS(:CURSOR, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

#### FETCH_BULK_RECORD_COLLECTIONS[¶](#fetch-bulk-record-collections)

These procedures are used when a `FETCH BULK` is done into a record of collections.

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, LIMIT FLOAT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$
  var limitValue = LIMIT ?? 'NULL';
  var query = `SELECT * FROM ${CURSOR.NAME}_TEMP_TABLE LIMIT ${limitValue} OFFSET ${CURSOR.ROWCOUNT}`;
  var stmt = snowflake.createStatement({ sqlText: query});
  var resultSet = stmt.execute();
  var column_count = stmt.getColumnCount();
  CURSOR.RESULT = {};
  if (COLUMN_NAMES)
  {
    for (let i = 0 ; i < COLUMN_NAMES.length ; i++) {
      CURSOR.RESULT[COLUMN_NAMES[i]] = [];
    }
  } else {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      CURSOR.RESULT[columnName] = [];
    }
  }

  while (resultSet.next()) {
    for (let i = 1 ; i <= column_count ; i++) {
      let columnName = stmt.getColumnName(i);
      let fieldName = COLUMN_NAMES ? COLUMN_NAMES[i - 1] : columnName;
      CURSOR.RESULT[fieldName].push(resultSet.getColumnValue(columnName));
    }
  }
  CURSOR.ROWCOUNT += stmt.getRowCount();
  CURSOR.FOUND = stmt.getRowCount() > 0;
  CURSOR.NOTFOUND = !CURSOR.FOUND;
  return CURSOR;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, NULL, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, LIMIT INTEGER)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, :LIMIT, NULL));
    RETURN :RESULT;
  END;
$$;
```

Copy

```
CREATE OR REPLACE PROCEDURE FETCH_BULK_RECORD_COLLECTIONS(CURSOR OBJECT, COLUMN_NAMES ARRAY)
RETURNS OBJECT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    RESULT OBJECT;
  BEGIN
    RESULT := (CALL FETCH_BULK_RECORD_COLLECTIONS(:CURSOR, NULL, :COLUMN_NAMES));
    RETURN :RESULT;
  END;
$$;
```

Copy
