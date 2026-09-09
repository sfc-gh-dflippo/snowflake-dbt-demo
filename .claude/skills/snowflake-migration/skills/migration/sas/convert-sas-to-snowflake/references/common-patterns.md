# Common SAS to Snowflake Patterns

## When to Load

Load this reference for **all conversions** - contains critical patterns for stored procedures, function mappings, and troubleshooting.

---

## Key Conversion Principles

### SAS → Snowflake Mental Model

| SAS Concept | Snowflake Equivalent |
|-------------|---------------------|
| DATA step | SQL INSERT/SELECT or Stored Procedure |
| SAS dataset | Table or View |
| Observation | Row |
| Variable | Column |
| RETAIN | Variable declaration in procedure OR window functions |
| BY group processing | PARTITION BY / window functions |
| Missing (.) | NULL |
| SAS date (days since 1960) | `DATEADD('day', sas_date, '1960-01-01')` |
| SAS datetime (seconds since 1960) | `DATEADD('second', sas_datetime, '1960-01-01')` |
| PROC SQL | SQL (mostly 1:1) |
| SAS Macro | Stored Procedure, UDF, or Jinja templating |

---

## Translation Priority

1. **SQL First** - Rule-based conversion to Snowflake SQL
2. **Window Functions** - For RETAIN, FIRST./LAST. patterns
3. **Stored Procedures** - For complex iteration, state management
4. **Flag for Review** - Unknown patterns with clear comments

### When to Use Pure SQL

- Simple column transformations
- Filtering (WHERE)
- Aggregations (PROC MEANS/SUMMARY → GROUP BY)
- Joins (MERGE with BY → JOIN)
- Sorting (PROC SORT → ORDER BY)
- Running totals with RETAIN → `SUM() OVER (ROWS UNBOUNDED PRECEDING)`

### When to Use Stored Procedures

- Row-by-row conditional logic with state
- RETAIN variables that accumulate with complex conditions
- Complex FIRST./LAST. BY-group processing beyond simple window functions
- Multiple output datasets from one pass
- Iterative/looping constructs (`DO WHILE`, `DO UNTIL`)
- Dynamic SQL generation

---

## Variable Binding Rules (CRITICAL)

**⚠️ ALWAYS review before generating stored procedures.**

In Snowflake Scripting stored procedures:

| Context | Use `:` prefix? | Example |
|---------|-----------------|---------|
| SQL statement (SELECT, INSERT, etc.) | YES | `SELECT * FROM t WHERE id = :my_var` |
| INTO clause | YES | `SELECT col INTO :my_var FROM t` |
| IDENTIFIER() for dynamic names | YES | `FROM IDENTIFIER(:table_name)` |
| Assignment (`:=`) | NO | `my_var := 'value'` |
| RETURN statement | NO | `RETURN my_var` |
| String concatenation | NO | `sql_stmt := 'SELECT ' \|\| col_name` |
| FOR loop variable | NO | `FOR i IN 1 TO 10` |
| IF condition | NO | `IF (my_var > 0) THEN` |

**Common Mistakes:**
```sql
-- WRONG: Missing colon in SQL
SELECT * FROM table WHERE id = my_var;

-- CORRECT:
SELECT * FROM table WHERE id = :my_var;

-- WRONG: Colon in assignment
:my_var := 'value';

-- CORRECT:
my_var := 'value';
```

---

## Error Handling Pattern (CRITICAL)

Always wrap stored procedures with EXCEPTION handling:

```sql
CREATE OR REPLACE PROCEDURE process_data(input_table STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  invalid_input EXCEPTION (-20001, 'Invalid input parameter');
  rows_processed INTEGER DEFAULT 0;
BEGIN
  -- Validate inputs
  IF (input_table IS NULL OR input_table = '') THEN
    RAISE invalid_input;
  END IF;
  
  -- Main logic here
  CREATE OR REPLACE TABLE output AS SELECT * FROM IDENTIFIER(:input_table);
  SELECT COUNT(*) INTO :rows_processed FROM output;
  
  RETURN 'Success: Processed ' || rows_processed || ' rows';
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN invalid_input THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
END;
$$;
```

**Exception types:**
- `STATEMENT_ERROR` — SQL execution failed
- `EXPRESSION_ERROR` — Expression evaluation failed
- Custom exceptions — Declare with `EXCEPTION (code, 'message')`
- `OTHER` — Catch-all

**Built-in error variables:**
- `SQLCODE` — Error code (integer)
- `SQLERRM` — Error message (string)
- `SQLSTATE` — ANSI SQL state code

---

## Stored Procedure Best Practices

```sql
CREATE OR REPLACE PROCEDURE schema_name.proc_name(
  p_input_table STRING,
  p_output_table STRING,
  p_run_date DATE DEFAULT CURRENT_DATE()
)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  -- 1. Exceptions
  err_invalid_input EXCEPTION (-20001, 'Invalid input');
  err_no_data EXCEPTION (-20002, 'No data found');
  
  -- 2. Variables
  v_row_count INTEGER DEFAULT 0;
  v_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP();
BEGIN
  -- 3. Validation
  IF (p_input_table IS NULL) THEN
    RAISE err_invalid_input;
  END IF;
  
  -- 4. Processing
  CREATE OR REPLACE TABLE IDENTIFIER(:p_output_table) AS
  SELECT * FROM IDENTIFIER(:p_input_table)
  WHERE process_date = :p_run_date;
  
  -- 5. Metrics
  SELECT COUNT(*) INTO :v_row_count FROM IDENTIFIER(:p_output_table);
  
  IF (v_row_count = 0) THEN
    RAISE err_no_data;
  END IF;
  
  -- 6. Return success
  RETURN OBJECT_CONSTRUCT(
    'status', 'SUCCESS',
    'rows_processed', v_row_count,
    'duration_sec', DATEDIFF('second', v_start_time, CURRENT_TIMESTAMP())
  )::STRING;

EXCEPTION
  WHEN err_invalid_input THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN err_no_data THEN
    RETURN OBJECT_CONSTRUCT('status', 'WARNING', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
END;
$$;
```

**Naming conventions:**
- Procedures: `verb_noun` (e.g., `process_sales`)
- Parameters: `p_` prefix
- Variables: `v_` prefix
- Exceptions: `err_` prefix
- Custom error codes: -20001 to -20999

---

## Common Pattern Translations

### Running Total (RETAIN)

**SAS:**
```sas
DATA running;
  SET transactions;
  BY customer_id;
  RETAIN running_sum 0;
  IF FIRST.customer_id THEN running_sum = 0;
  running_sum = running_sum + amount;
RUN;
```

**Snowflake:**
```sql
SELECT *,
  SUM(amount) OVER (
    PARTITION BY customer_id 
    ORDER BY transaction_date 
    ROWS UNBOUNDED PRECEDING
  ) AS running_sum
FROM transactions;
```

### FIRST./LAST. Detection

**SAS:**
```sas
DATA flagged;
  SET sorted;
  BY group_var;
  first_flag = FIRST.group_var;
  last_flag = LAST.group_var;
RUN;
```

**Snowflake:**
```sql
SELECT *,
  CASE WHEN ROW_NUMBER() OVER (PARTITION BY group_var ORDER BY sort_col) = 1 
       THEN 1 ELSE 0 END AS first_flag,
  CASE WHEN ROW_NUMBER() OVER (PARTITION BY group_var ORDER BY sort_col DESC) = 1 
       THEN 1 ELSE 0 END AS last_flag
FROM sorted;
```

### Keep Last Row per Group

**SAS:**
```sas
DATA last_only;
  SET sorted;
  BY customer_id;
  IF LAST.customer_id;
RUN;
```

**Snowflake:**
```sql
SELECT * FROM sorted
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY sort_col DESC) = 1;
```

### Conditional Output to Multiple Tables

**SAS:**
```sas
DATA high_value low_value;
  SET customers;
  IF total_spend > 1000 THEN OUTPUT high_value;
  ELSE OUTPUT low_value;
RUN;
```

**Snowflake (two statements):**
```sql
CREATE TABLE high_value AS
SELECT * FROM customers WHERE total_spend > 1000;

CREATE TABLE low_value AS
SELECT * FROM customers WHERE total_spend <= 1000;
```

---

## Untranslated Section Comment Template

```sql
-- ============================================================
-- WARNING: UNTRANSLATED/LOW CONFIDENCE SECTION
-- Reason: [specific reason - e.g., "Complex ARRAY with DO loop"]
-- Original SAS Code:
-- [original SAS code here]
-- ============================================================
-- TODO: Manual review required
```

---

## Cross-Block Variable Persistence (CRITICAL)

Snowflake Scripting variables declared in DECLARE...BEGIN...END **DO NOT persist** after the block ends.

### When to Persist

If block N computes a value (via SELECT INTO :var or := assignment) that block N+1 or later needs, you MUST persist it as a session variable.

### How to Persist

```sql
-- At end of block N:
EXECUTE IMMEDIATE 'SET MY_VAR = ''' || REPLACE(v_local_var, '''', '''''') || '''';

-- For numeric values:
EXECUTE IMMEDIATE 'SET MY_COUNT = ' || CAST(v_count AS VARCHAR);

-- In block N+1, reference as:
SELECT * FROM my_table WHERE col = $MY_VAR;
```

### Rules
- Use `REPLACE(val, '''', '''''')` for proper single-quote escaping — **NEVER** backslash escaping
- Scripting variables (:var) only work within the same DECLARE...BEGIN...END block
- Session variables ($var) persist for the entire Snowflake session
- When converting SAS `PROC SQL INTO :macrovar`, always persist as session variable if any downstream block references `&macrovar`

---

## LISTAGG and String Aggregation Rules

When converting SAS RETAIN+concatenation loops to Snowflake:
- Use `LISTAGG(column, delimiter) WITHIN GROUP (ORDER BY ...)`
- The ORDER BY clause MUST reference only columns that exist in the source table
- If no natural ordering column exists, ORDER BY the value column itself or omit ORDER BY
- LISTAGG has a 1MB output limit — flag MANUAL_REVIEW_REQUIRED for large concatenations
- Pattern: strip leading delimiter then wrap → `'(' || LISTAGG(TRIM(col), ' or ') WITHIN GROUP (ORDER BY col) || ')'`

### LISTAGG(DISTINCT ...) with a computed ORDER BY

Snowflake rejects a **computed expression** in `ORDER BY` when the aggregate is `LISTAGG(DISTINCT ...)` — it fails at runtime with *"not a valid order by expression"*. A plain column reference is fine inline; any function/CONCAT/TRIM/SPLIT_PART/operator in the ordered expression must be pushed into a `SELECT DISTINCT` subquery first.

```sql
-- WRONG (fails): computed expr in both DISTINCT and ORDER BY
SELECT LISTAGG(DISTINCT TRIM(col), '~') WITHIN GROUP (ORDER BY TRIM(col)) FROM t;

-- CORRECT: distinct the computed value in a subquery, then aggregate
SELECT LISTAGG(val, '~') WITHIN GROUP (ORDER BY val)
FROM (SELECT DISTINCT TRIM(col) AS val FROM t);
```
This is common when converting SAS `PROC SQL SELECT ... INTO :var SEPARATED BY` over a derived expression.

---

## Snowflake Platform Constraints (common runtime traps)

These are generic Snowflake behaviors that silently break otherwise-plausible converted code.

### Session variables inside stored procedures (EXECUTE AS CALLER)

A stored procedure created with the **default owner's rights cannot access session variables at all** — it can neither read a `$VAR` set before the call nor `SET` one for later use. To use session variables inside a procedure, it MUST be created with `EXECUTE AS CALLER`.

```sql
CREATE OR REPLACE PROCEDURE my_proc()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER          -- REQUIRED to read/set session variables
AS
$$
BEGIN
  -- $RDT resolves correctly here only under EXECUTE AS CALLER:
  CREATE OR REPLACE TEMPORARY TABLE out AS SELECT * FROM src WHERE run_dt = $RDT;
  RETURN 'ok';
END;
$$;
```

- `$VAR` syntax **does** work inside an `EXECUTE AS CALLER` procedure body — you do NOT need `GETVARIABLE()` to read it. (`GETVARIABLE('VAR')` is an equivalent alternative, not a requirement.)
- The orchestration pattern (one driver proc calling sub-procs, sharing temp tables + session vars) only works if **every** proc in the chain is `EXECUTE AS CALLER` — owner's-rights procs run in an isolated scope and cannot see the caller's temp tables or session variables.

### Referencing a session variable SET in the SAME scripting block

If a SQL statement references a session variable that was `SET` earlier in the **same** `DECLARE...BEGIN...END` (or `EXECUTE IMMEDIATE`) block, that statement must itself run via `EXECUTE IMMEDIATE` — a static statement in the same block fails with *"Session variable '$VAR' does not exist"*.

```sql
-- WRONG (fails in the same block):
BEGIN
  SET val = (SELECT 100);
  INSERT INTO my_table VALUES ($val);
END;

-- CORRECT:
BEGIN
  SET val = (SELECT 100);
  EXECUTE IMMEDIATE 'INSERT INTO my_table VALUES ($val)';
END;
```

### Session variables are NOT allowed in a VALUES() clause

`$VAR` works in `SELECT`, `WHERE`, and `SET` contexts but NOT inside `INSERT ... VALUES(...)`. Use `INSERT ... SELECT` instead.

```sql
-- WRONG:
INSERT INTO t (c1, c2) VALUES ('lit', $RSTRDT);
-- CORRECT:
INSERT INTO t (c1, c2) SELECT 'lit', TO_DATE($RSTRDT, 'YYYY-MM-DD');
```

### Reserved-word column names must be double-quoted

Many ordinary SAS column names are Snowflake reserved keywords and must be double-quoted wherever used as identifiers (CREATE, INSERT column list, SELECT, alias). When unsure, quote — over-quoting is safe.

Common offenders from SAS sources: `DESC`, `TYPE`, `VALUE`, `LOCATION`, `NAME`, `FILE`, `STATUS`, `ORDER`, `GROUP`, `DATE`, `TIME`, `KEY`, `COMMENT`, `START`, `END`, `ROW`, `ROWS`, `SHARE`, `ROLE`, `USER`, `SCHEMA`, `COLUMN`, `INDEX`, `REPLACE`.

```sql
CREATE OR REPLACE TABLE t ("DESC" VARCHAR, "TYPE" NUMBER, "VALUE" NUMBER);
SELECT "DESC", "TYPE" FROM t;
```

### Temp/session-table metadata: use `DESCRIBE TABLE`, not `INFORMATION_SCHEMA`

`INFORMATION_SCHEMA.COLUMNS` does **not** reliably show temporary/session-scoped tables — it may return no rows, or stale metadata from a since-dropped permanent table of the same name. To discover columns/types of a table that may be temporary (created earlier in the same session), use `DESCRIBE TABLE`.

```sql
-- CORRECT for temp/session tables:
DESCRIBE TABLE MY_TABLE;   -- row["name"], row["type"], row["null?"], ...
-- WRONG (unreliable for temp tables):
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'MY_TABLE';
```
`INFORMATION_SCHEMA` remains fine for permanent tables in other schemas/databases and for counting/pattern queries.

### `COPY FILES` does not support user stages (`@~`)

`COPY FILES INTO ... FROM @~/...` fails — user stages are not valid sources/targets. Use a **named internal stage** as the intermediate, single-quote any path containing spaces, and `REMOVE` temp files afterward so they don't accumulate.

```sql
-- WRONG:  COPY FILES INTO @target FROM @~/temp ...
-- CORRECT:
CREATE STAGE IF NOT EXISTS <TARGET_DB>.<TARGET_SCHEMA>.NAMED_STG;
COPY FILES INTO @<TARGET_DB>.<TARGET_SCHEMA>.NAMED_STG FROM @source ...;
-- paths with spaces must be single-quoted:  COPY FILES INTO '@STG/My Folder/Sub Dir' FROM ...;
REMOVE @<TARGET_DB>.<TARGET_SCHEMA>.NAMED_STG/<file>;   -- cleanup
```

---

## WORK / Temporary Table Rules

| Rule | Details |
|------|---------|
| SAS WORK dataset | → `CREATE OR REPLACE TEMPORARY TABLE name AS ...` |
| Schema prefix | **NEVER** — use bare table name only |
| Wrong | `CREATE OR REPLACE TEMPORARY TABLE DB.SCHEMA.MY_TABLE` |
| Correct | `CREATE OR REPLACE TEMPORARY TABLE MY_TABLE` |
| TEMPORARY keyword | **ALWAYS** preserve on rewrites/deduplication |
| Permanence | Temp tables persist for the session — available to all subsequent blocks |
| FROM reference | `FROM MY_TABLE` — no schema prefix |

---

## Oracle / DB2 Passthrough SQL Conversion

See `references/vendor-passthrough.md` for full vendor function mapping tables and passthrough conversion steps.

---

## Troubleshooting

### Unsupported SAS Constructs

| Construct | Issue | Workaround |
|-----------|-------|------------|
| HASH objects | No direct equivalent | Use JOINs or temp tables |
| INFILE/FILE | File I/O | Use Snowflake stages |
| CALL SYMPUT | Dynamic macro vars | Use stored procedure variables |
| CALL EXECUTE | Dynamic code | Use EXECUTE IMMEDIATE |
| DO loops with state | Complex iteration | Stored procedure with cursors |

### Common Compile Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Invalid identifier" | Missing colon in SQL | Add `:` before variable |
| "Object does not exist" | Dynamic table name | Use `IDENTIFIER(:var)` |
| "Type mismatch" | SAS is type-flexible | Add explicit `CAST()` |
| "Reserved word" | Column name is keyword | Quote with `"column"` |

### Performance Concerns

- SAS row-by-row → Use window functions, not cursors
- Large RETAIN patterns → Consider incremental/staging approach
- Many small queries → Batch into fewer larger queries
