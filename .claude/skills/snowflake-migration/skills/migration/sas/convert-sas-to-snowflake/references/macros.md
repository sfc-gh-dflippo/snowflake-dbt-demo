# SAS Macros to Snowflake Conversion

## When to Load

Load when SAS code contains: `%MACRO`, `%MEND`, `%LET`, `&variable` references, `%DO` loops, `%IF`/`%THEN`, `%SYSFUNC`, or autocall macro calls.

---

## Overview

SAS macros generate code at compile time. Snowflake alternatives:
1. **Stored Procedures** - For procedural logic
2. **UDFs** - For reusable calculations
3. **Jinja templates** - For SQL generation (in dbt or external tools)
4. **JavaScript UDFs** - For complex string manipulation

## Macro Variables

### Simple Variable Substitution

**SAS:**
```sas
%LET start_date = 2024-01-01;
%LET table_name = sales;

PROC SQL;
  SELECT * FROM &table_name
  WHERE date >= "&start_date"d;
QUIT;
```

**Snowflake (Session Variables):**
```sql
SET start_date = '2024-01-01';
SET table_name = 'sales';

SELECT * FROM IDENTIFIER($table_name)
WHERE date >= $start_date::DATE;
```

**Snowflake (Stored Procedure Parameters):**
```sql
CREATE OR REPLACE PROCEDURE query_table(table_name STRING, start_date DATE)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
DECLARE
  result RESULTSET;
BEGIN
  result := (SELECT * FROM IDENTIFIER(:table_name) WHERE date >= :start_date);
  RETURN TABLE(result);
END;
$$;

CALL query_table('sales', '2024-01-01'::DATE);
```

### Macro Variable from Query

**SAS:**
```sas
PROC SQL NOPRINT;
  SELECT MAX(date) INTO :max_date FROM transactions;
QUIT;
%PUT Max date is &max_date;
```

**Snowflake:**
```sql
CREATE OR REPLACE PROCEDURE get_max_date()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  max_date DATE;
BEGIN
  SELECT MAX(date) INTO :max_date FROM transactions;
  RETURN 'Max date is ' || max_date::STRING;
END;
$$;

CALL get_max_date();
```

## Simple Macro Programs

### Macro Without Parameters

**SAS:**
```sas
%MACRO clean_data;
  DATA cleaned;
    SET raw;
    name = PROPCASE(STRIP(name));
    IF age < 0 THEN age = .;
  RUN;
%MEND;

%clean_data;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE clean_data()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  err_no_source EXCEPTION (-20001, 'Source table raw does not exist');
  v_row_count INTEGER;
BEGIN
  -- Validate source exists
  SELECT COUNT(*) INTO :v_row_count FROM INFORMATION_SCHEMA.TABLES 
  WHERE TABLE_NAME = 'RAW' AND TABLE_SCHEMA = CURRENT_SCHEMA();
  IF (v_row_count = 0) THEN
    RAISE err_no_source;
  END IF;
  
  CREATE OR REPLACE TABLE cleaned AS
  SELECT *,
    INITCAP(TRIM(name)) AS name_clean,
    CASE WHEN age < 0 THEN NULL ELSE age END AS age_clean
  FROM raw;
  
  SELECT COUNT(*) INTO :v_row_count FROM cleaned;
  RETURN 'Data cleaned: ' || v_row_count || ' rows';
EXCEPTION
  WHEN err_no_source THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
END;
$$;

CALL clean_data();
```

### Macro With Parameters

**SAS:**
```sas
%MACRO summarize(input=, output=, by_var=);
  PROC MEANS DATA=&input NOPRINT;
    CLASS &by_var;
    VAR amount;
    OUTPUT OUT=&output SUM=total MEAN=average;
  RUN;
%MEND;

%summarize(input=sales, output=sales_summary, by_var=region);
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE summarize(
  p_input_table STRING, 
  p_output_table STRING, 
  p_by_var STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  err_invalid_input EXCEPTION (-20001, 'Input parameters cannot be NULL');
  v_sql_stmt STRING;
  v_row_count INTEGER;
BEGIN
  -- Validate inputs
  IF (p_input_table IS NULL OR p_output_table IS NULL OR p_by_var IS NULL) THEN
    RAISE err_invalid_input;
  END IF;
  
  v_sql_stmt := 'CREATE OR REPLACE TABLE ' || p_output_table || ' AS 
    SELECT ' || p_by_var || ', 
      SUM(amount) AS total, 
      AVG(amount) AS average,
      COUNT(*) AS n
    FROM ' || p_input_table || '
    GROUP BY ' || p_by_var;
  EXECUTE IMMEDIATE v_sql_stmt;
  
  v_sql_stmt := 'SELECT COUNT(*) FROM ' || p_output_table;
  EXECUTE IMMEDIATE v_sql_stmt INTO :v_row_count;
  
  RETURN OBJECT_CONSTRUCT('status', 'SUCCESS', 'table', p_output_table, 'rows', v_row_count)::STRING;
EXCEPTION
  WHEN err_invalid_input THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN STATEMENT_ERROR THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('status', 'ERROR', 'code', sqlcode, 'message', sqlerrm)::STRING;
END;
$$;

CALL summarize('sales', 'sales_summary', 'region');
```

## Conditional Logic (%IF)

**SAS:**
```sas
%MACRO process(include_nulls=N);
  PROC SQL;
    SELECT * FROM data
    %IF &include_nulls = Y %THEN %DO;
      /* include all */
    %END;
    %ELSE %DO;
      WHERE value IS NOT NULL
    %END;
    ;
  QUIT;
%MEND;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE process(include_nulls BOOLEAN)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
DECLARE
  result RESULTSET;
BEGIN
  IF (:include_nulls) THEN
    result := (SELECT * FROM data);
  ELSE
    result := (SELECT * FROM data WHERE value IS NOT NULL);
  END IF;
  RETURN TABLE(result);
END;
$$;

CALL process(FALSE);
```

## Looping (%DO)

**SAS:**
```sas
%MACRO create_monthly_tables;
  %DO month = 1 %TO 12;
    DATA sales_&month;
      SET sales;
      WHERE MONTH(date) = &month;
    RUN;
  %END;
%MEND;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE create_monthly_tables()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  month INTEGER;
  sql_stmt STRING;
BEGIN
  FOR month IN 1 TO 12 DO
    sql_stmt := 'CREATE OR REPLACE TABLE sales_' || month::STRING || 
                ' AS SELECT * FROM sales WHERE MONTH(date) = ' || month::STRING;
    EXECUTE IMMEDIATE sql_stmt;
  END FOR;
  RETURN 'Created 12 monthly tables';
END;
$$;

CALL create_monthly_tables();
```

## Macro Functions

### %SYSFUNC

**SAS:**
```sas
%LET today = %SYSFUNC(TODAY(), DATE9.);
%LET file_count = %SYSFUNC(COUNTW(&file_list));
```

**Snowflake:**
```sql
-- Session variables (outside procedures):
SET today = CURRENT_DATE()::STRING;
SET file_count = ARRAY_SIZE(SPLIT('file1 file2 file3', ' '));

-- Or in stored procedures:
CREATE OR REPLACE PROCEDURE sysfunc_example(file_list STRING)
RETURNS OBJECT
LANGUAGE SQL
AS
$$
DECLARE
  today STRING := CURRENT_DATE()::STRING;
  file_count INTEGER := ARRAY_SIZE(SPLIT(:file_list, ' '));
BEGIN
  RETURN OBJECT_CONSTRUCT('today', today, 'file_count', file_count);
END;
$$;
```

### %EVAL and %SYSEVALF

**SAS:**
```sas
%LET result = %EVAL(10 + 5);
%LET pct = %SYSEVALF(100 * &num / &denom);
```

**Snowflake:**
```sql
-- Session variables:
SET result = 10 + 5;
SET pct = 100.0 * $num / $denom;

-- Or in stored procedures:
CREATE OR REPLACE PROCEDURE eval_example(num FLOAT, denom FLOAT)
RETURNS OBJECT
LANGUAGE SQL
AS
$$
DECLARE
  result INTEGER := 10 + 5;
  pct FLOAT := 100.0 * :num / :denom;
BEGIN
  RETURN OBJECT_CONSTRUCT('result', result, 'pct', pct);
END;
$$;
```

## Complex Macro: JavaScript UDF Alternative

For complex text manipulation that macros do:

**SAS:**
```sas
%MACRO parse_name(full_name);
  %LET first = %SCAN(&full_name, 1, %STR( ));
  %LET last = %SCAN(&full_name, -1, %STR( ));
%MEND;
```

**Snowflake JavaScript UDF:**
```sql
CREATE OR REPLACE FUNCTION parse_name(full_name STRING)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
AS
$$
  var parts = FULL_NAME ? FULL_NAME.trim().split(/\s+/) : [];
  return {
    first: parts[0] || null,
    last: parts.length > 1 ? parts[parts.length - 1] : null
  };
$$;

SELECT parse_name('John Michael Smith')['first'] AS first_name,
       parse_name('John Michael Smith')['last'] AS last_name;
```

## Autocall Macros / Reusable Libraries

**SAS autocall library:**
```sas
/* In autocall library */
%MACRO stdize(var);
  (&var - MEAN(&var)) / STD(&var)
%MEND;
```

**Snowflake UDF:**
```sql
CREATE OR REPLACE FUNCTION stdize(val FLOAT, mean_val FLOAT, std_val FLOAT)
RETURNS FLOAT
AS
$$
  (val - mean_val) / NULLIF(std_val, 0)
$$;

-- Usage with window function:
SELECT *,
  stdize(value, AVG(value) OVER(), STDDEV(value) OVER()) AS standardized
FROM data;
```

## Dynamic SQL Generation

**SAS (macro building SQL):**
```sas
%MACRO build_select(varlist);
  %LET n = %SYSFUNC(COUNTW(&varlist));
  SELECT 
  %DO i = 1 %TO &n;
    %SCAN(&varlist, &i)
    %IF &i < &n %THEN ,;
  %END
%MEND;

PROC SQL;
  %build_select(name age salary)
  FROM employees;
QUIT;
```

**Snowflake Stored Procedure:**
```sql
CREATE OR REPLACE PROCEDURE build_select(varlist STRING, table_name STRING)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
DECLARE
  sql_stmt STRING;
  result RESULTSET;
BEGIN
  sql_stmt := 'SELECT ' || varlist || ' FROM ' || table_name;
  result := (EXECUTE IMMEDIATE sql_stmt);
  RETURN TABLE(result);
END;
$$;

CALL build_select('name, age, salary', 'employees');
```

## Conversion Decision Guide

| SAS Macro Pattern | Snowflake Approach |
|-------------------|-------------------|
| Simple variable substitution | Session variables (`SET var = value`) |
| Parameterized code blocks | Stored Procedure with parameters |
| Reusable calculations | SQL UDF or JavaScript UDF |
| Dynamic table/column names | Stored Procedure with EXECUTE IMMEDIATE |
| Complex text processing | JavaScript UDF |
| Code generation | External tool (dbt Jinja, Python) |
| Complex string manipulation (mixed case, word parsing) | JavaScript UDF |
| PROC FORMAT lookup macros | Lookup tables with LEFT JOIN |
| Filter/validation macros | Views or SQL UDFs |

---

## Macro Internal Completeness Rules (CRITICAL)

Every SAS statement inside a macro MUST have a corresponding Snowflake equivalent. Do NOT skip any.

### Branch Completeness
- For `%IF/%THEN/%ELSE`: convert BOTH the IF branch AND the ELSE branch completely
- Never skip a branch even if it appears to be an edge case

### Statement Coverage
| SAS Statement in Macro | Snowflake Conversion |
|-----------------------|---------------------|
| `%SYSEXEC` (shell commands) | `MANUAL_REVIEW_REQUIRED` with Snowflake stage commands |
| `%INCLUDE` (external SAS file) | `CALL stored_procedure_name()` + `MANUAL_REVIEW_REQUIRED` if not yet converted |
| `%sysfunc(fileexist(path))` | LIST @stage with RESULT_SCAN pattern in BEGIN...EXCEPTION block |
| `ENDSAS` / `%ABORT` | Named EXCEPTION with RAISE |
| LIBNAME inside macros | Resolve to fully qualified DATABASE.SCHEMA per mapping |
| Nested macro calls `%macroname(args)` | `CALL procedure_name(args)` |

### Repeated Macro Invocations
- When a macro is called multiple times with different parameters, track each invocation separately
- Different parameter combinations may trigger different `%IF` branches
- Generate separate output for each invocation if results differ
- If macro is called >5 times with varying parameters, prefer a stored procedure called in a loop

### CALL SYMPUT / SYMGET Cross-Block Persistence

```sql
-- SAS: CALL SYMPUT('my_var', value);
-- ... later in another step: WHERE col = "&my_var"

-- Snowflake (within same stored procedure):
v_my_var := value;

-- Snowflake (across anonymous blocks):
-- At end of block N:
EXECUTE IMMEDIATE 'SET MY_VAR = ''' || REPLACE(v_my_var, '''', '''''') || '''';

-- At start of block N+1:
-- Reference as $MY_VAR in SQL
SELECT * FROM table WHERE col = $MY_VAR;
```

### Macro-Variable IN-Lists → `SPLIT_TO_TABLE`

SAS frequently builds a comma-separated list in a macro variable (via `CATS`/`CATX` in a loop, or `SELECT ... INTO :var SEPARATED BY ','`) and injects it into an `IN (&var)` clause. SAS macro resolution expands `&var` into quoted literals; Snowflake has no macro resolution, so the idiomatic equivalent is to store the value as **unquoted, plain comma-separated** text and expand it at query time with `SPLIT_TO_TABLE`.

```sql
-- Build the list UNQUOTED (comma only, no embedded quotes):
--   v_list := v_list || ',' || v_item;   -- e.g. '202301,01/2023,12/2022'

-- Consume with SPLIT_TO_TABLE + TRIM (works in static SQL and dynamic SQL):
WHERE col IN (
  SELECT TRIM(VALUE) FROM TABLE(SPLIT_TO_TABLE($MY_LIST, ','))
)
```

- **Store unquoted.** Adding `'` around each value (`'202301',''01/2023''`) breaks `SPLIT_TO_TABLE` — the quotes become part of each value and every comparison fails.
- **Always `TRIM(VALUE)`.** Leading/trailing whitespace from the CSV causes silent zero-match failures.
- Only embed quotes when the value is used as a raw injected IN-list (`IN (' || v_list || ')`), where `v_list` must itself already contain `'a','b'`. Prefer the `SPLIT_TO_TABLE` form — it is the safe default.

### %INCLUDE Without Source Available

When `%INCLUDE` references a file whose source is not available:

```sql
-- MANUAL_REVIEW_REQUIRED: %INCLUDE '/path/to/macros.sas'
-- This file was not available for conversion.
-- Expected to define: [inferred macro names from usage context]
-- Action required: Convert the included file separately and create the
-- corresponding stored procedures/UDFs, then update CALL statements below.
CALL sp_included_macro_name();  -- Stub: replace with actual procedure
```

---

## PROC FORMAT as Macro → Lookup Table or UDF

### Simple Value Mapping → CASE or Lookup Table
```sql
-- SAS: PROC FORMAT; VALUE status_fmt 1='Active' 2='Inactive'; RUN;
-- Then: PUT(status, status_fmt.)

-- Option 1: Inline CASE
CASE status WHEN 1 THEN 'Active' WHEN 2 THEN 'Inactive' END

-- Option 2: Lookup table (for complex or reusable formats)
CREATE OR REPLACE TABLE LKP_STATUS (code INT, description STRING);
INSERT INTO LKP_STATUS VALUES (1, 'Active'), (2, 'Inactive');
-- Usage: LEFT JOIN LKP_STATUS l ON t.status = l.code
```

### Range-Based Mapping → CASE with ranges
```sql
-- SAS: VALUE age_grp LOW-17='Youth' 18-64='Adult' 65-HIGH='Senior';
CASE 
  WHEN age <= 17 THEN 'Youth'
  WHEN age BETWEEN 18 AND 64 THEN 'Adult'
  WHEN age >= 65 THEN 'Senior'
END
```

### PROC FORMAT with CNTLIN= (data-driven format)
```sql
-- SAS: PROC FORMAT CNTLIN=format_data; RUN;
-- Snowflake: Create a lookup table from the format dataset
CREATE OR REPLACE TABLE LKP_FORMAT AS
SELECT start AS code, label AS description FROM format_data;
```

### Complex String Manipulation Macro → JavaScript UDF
For macros that perform complex string operations (mixed case conversion, word parsing, pattern matching), use JavaScript UDFs:

```sql
CREATE OR REPLACE FUNCTION fn_complex_string_op(input_str STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
  if (!INPUT_STR) return null;
  // Complex string logic here
  return result;
$$;
```
