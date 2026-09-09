# Multi-Block Program Orchestration

## When to Load

Load at **Step 5** when a SAS program is **multi-block** and the blocks share state — specifically when any of these are present:
- A program that produces **3+ blocks** with temp-table / macro-variable dependencies between them
- Macro `%DO` loops that wrap multiple operations
- Indexed macro-array variables (`&&var&i`)
- `&SYSERR`-driven error branching
- `%SYSFUNC(FILEEXIST(...))` / `FEXIST()` file-existence gates
- Trigger-file gates (`%if not %sysfunc(fileexist(trigger)) %then endsas`)

These patterns are about **stitching converted blocks into one runnable Snowflake program**. All examples use placeholders (`<TARGET_DB>`, `<TARGET_SCHEMA>`, `@<STAGE>`, `<TABLE>`) — resolve them from the conversion context / library mapping. Never hard-code database, schema, stage, or table names.

---

## 1. Orchestration Wrapper — `SP_<PROGRAM>_MAIN()`

A converted SAS program that produces more than ~3 dependent blocks SHOULD ship with a top-level orchestration procedure that runs every block **in one session, in order**. Without it, the user receives disconnected blocks and must manually determine execution order, session scoping, and error handling — which is the bulk of post-conversion effort.

```sql
CREATE OR REPLACE PROCEDURE <TARGET_DB>.<TARGET_SCHEMA>.SP_<PROGRAM>_MAIN()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER            -- REQUIRED: shares temp tables + session vars across the chain
AS
BEGIN
  USE DATABASE <TARGET_DB>;
  USE SCHEMA <TARGET_SCHEMA>;

  -- Block B00001: environment / macro-parameter setup (inline small blocks)
  -- Block B00002: CREATE OR REPLACE TEMPORARY TABLE ... ;
  -- Block B00003: CALL <TARGET_DB>.<TARGET_SCHEMA>.SP_<SUBSTEP>();   -- large blocks → sub-procs
  -- ... blocks in dependency order ...

  -- CLEANUP (only after ALL blocks complete)
  DROP TABLE IF EXISTS <TEMP1>;
  DROP TABLE IF EXISTS <TEMP2>;

  RETURN 'Program <PROGRAM> completed successfully';
EXCEPTION
  WHEN OTHER THEN
    RETURN 'FAILED: ' || SQLERRM;
END;
```

Rules:
- Name it `SP_<SAS_PROGRAM_NAME>_MAIN()`; make it the **last** item in the output.
- **Inline** small blocks (<~20 lines); **extract** large/looping blocks as sub-procs and `CALL` them.
- **Every** proc in the chain (this one and all it calls) MUST be `EXECUTE AS CALLER` — owner's-rights procs run in an isolated scope and cannot see the caller's temp tables or session variables, breaking the flow. (See `common-patterns.md` → Platform Constraints.)
- **Temp-table lifetime:** never `DROP` a temp table until no later block reads it. Before emitting any `DROP`, scan all subsequent blocks for that table name; if found, defer the drop to the cleanup section at the end.
- **Macro-parameter persistence:** if the SAS program is a macro with parameters, `SET` each parameter as a session variable at the top so every sub-block can read it; never let a sub-block silently overwrite one.

This is a report/skeleton recommendation — actually creating objects still follows the skill's Snowflake Interaction Policy (explicit user confirmation).

---

## 2. Indexed Macro Variables (`&&var&i`) → `LOOP_VARS` Temp Table

SAS macro arrays use doubly-resolved names (`&&file_extn&i`, `&&tin&i`). Snowflake session variables **cannot be dynamically named** at runtime (`SELECT $VAR || i` does not work). Replace the whole indexed-variable scheme with a temp table keyed by an index column, then iterate it with a cursor.

```sql
-- Replaces all CALL SYMPUTX(cats('var', i), value) assignments:
CREATE OR REPLACE TEMPORARY TABLE LOOP_VARS AS
SELECT
    ROW_NUMBER() OVER (ORDER BY <deterministic_key>) AS IDX,
    <col_a>, <col_b>, <col_c>          -- one column per &&var&i prefix
FROM <source_table>
WHERE <filters>;

-- Replaces CALL SYMPUTX('cnt', _n_):
--   SELECT COUNT(*) FROM LOOP_VARS;

-- Replaces %DO i=1 %TO &cnt (access columns directly, no dynamic var reads):
DECLARE cur CURSOR FOR SELECT * FROM LOOP_VARS ORDER BY IDX;
BEGIN
  FOR rec IN cur DO
    -- use rec.<col_a>, rec.<col_b> directly
  END FOR;
END;
```

- **NEVER** emit `EXECUTE IMMEDIATE 'SELECT $STG' || CAST(v_i AS VARCHAR)` — dynamic session-variable names do not resolve in Snowflake.
- Simplest variant: if the loop just copies columns straight from a source table and consumes them together, skip `LOOP_VARS` and put a cursor directly over the source table.
- Exception: a single indexed value used once may stay a plain session variable.

---

## 3. `%DO` Loop Unification → One `WHILE` Block

When a SAS `%DO i=1 %TO &cnt` loop wraps several operations (data steps, queries, exports, `%IF`/`%THEN` branches), produce **one** Snowflake Scripting `WHILE` block (or one stored proc) containing the **entire** loop body — never separate disconnected blocks per operation.

```sql
DECLARE
  v_cnt INTEGER;
  v_i INTEGER DEFAULT 1;
BEGIN
  SELECT COUNT(*) INTO :v_cnt FROM LOOP_VARS;
  WHILE (v_i <= v_cnt) DO
    BEGIN
      -- ALL operations from the SAS %DO body, in sequence:
      -- 1. variable/row resolution   2. query/extract   3. export/file op
      -- 4. status update             5. %IF/%THEN branches → IF/ELSEIF/ELSE
    EXCEPTION
      WHEN OTHER THEN NULL;   -- one iteration's failure must not abort the loop
    END;
    v_i := v_i + 1;
  END WHILE;
END;
```

- Nested `%DO` → nested `WHILE`. All `%IF/%THEN/%ELSE` branches inside the loop become `IF/ELSEIF/ELSE` inside the same iteration.
- **Anti-pattern (forbidden):** emitting "Block A = txt export", "Block B = csv export" when they are branches of one `%IF/%ELSE` inside a single `%DO` loop; or a bare comment like `-- call this inside a loop` without providing the loop.

---

## 4. `&SYSERR` Error Propagation → `ERROR_STATE` Temp Table

SAS uses `&SYSERR` (`%LET error = &syserr; %IF &error %THEN ...`) to gate flow on the last step's status. For programs with 3+ error checkpoints, track state in a temp table (session variables are fragile for complex flows).

```sql
CREATE OR REPLACE TEMPORARY TABLE ERROR_STATE (
  BLOCK_ID VARCHAR, STEP_NAME VARCHAR,
  ERROR_CODE INTEGER DEFAULT 0, ERROR_MSG VARCHAR DEFAULT '',
  OCCURRED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

BEGIN
  -- ... run step ...
  INSERT INTO ERROR_STATE (BLOCK_ID, STEP_NAME, ERROR_CODE) VALUES ('B00010', '<STEP>', 0);
EXCEPTION
  WHEN OTHER THEN
    INSERT INTO ERROR_STATE (BLOCK_ID, STEP_NAME, ERROR_CODE, ERROR_MSG)
    SELECT 'B00010', '<STEP>', SQLCODE, SQLERRM;   -- INSERT ... SELECT: functions not allowed in VALUES
END;

-- Check before the next step (equivalent of %IF &error %THEN):
DECLARE v_last_error INTEGER;
BEGIN
  SELECT ERROR_CODE INTO :v_last_error FROM ERROR_STATE
  WHERE BLOCK_ID = 'B00010' ORDER BY OCCURRED_AT DESC LIMIT 1;
  IF (v_last_error != 0) THEN
    NULL; -- SAS error branch
  ELSE
    NULL; -- SAS normal branch
  END IF;
END;
```

- `%IF &error %THEN` → `IF (v_last_error != 0) THEN`; `%IF NOT &error` → `IF (v_last_error = 0) THEN`.
- For 1–2 checks a session variable `SET ERROR = 0` is acceptable. Never silently drop a `&SYSERR` check — it controls SAS program flow.

---

## 5. `FILEEXIST` / `FEXIST` → Stage `LIST` + `RESULT_SCAN`

SAS `%SYSFUNC(FILEEXIST(path))` / `FEXIST(fileref)` check the filesystem; in Snowflake, files live on stages. Convert to a `LIST ... PATTERN` count, wrapped in an exception handler so a missing stage / permission error returns "not found" rather than aborting.

```sql
DECLARE
  v_file_exists BOOLEAN DEFAULT FALSE;
  v_file_count INTEGER DEFAULT 0;
BEGIN
  BEGIN
    LET rs RESULTSET := (EXECUTE IMMEDIATE
      'LIST @' || :v_stage || ' PATTERN=''.*' || :v_filename || '.*''');
    LET cur CURSOR FOR rs;
    FOR rec IN cur DO
      v_file_count := v_file_count + 1;
    END FOR;
  EXCEPTION
    WHEN OTHER THEN v_file_count := 0;
  END;
  v_file_exists := (v_file_count > 0);
END;
```

- `%IF %SYSFUNC(FILEEXIST(path)) %THEN` → `IF (v_file_exists) THEN`; the `%ELSE`/`ENDSAS` branch → a named exception `RAISE` (never a bare comment or silent continue).
- Resolve the SAS filesystem path to a stage from the conversion context's stage/library mapping. If no mapping is provided, flag `MANUAL_REVIEW_REQUIRED` for that path — do **not** invent a stage name.
- For file **matching** driven by a lookup (does *my expected* file exist?), match lookup→stage: `LIST @<stage> PATTERN='.*<expected_name>.*'`. Never list all stage files and compare each against one expected name (produces false errors for unrelated files).

---

## 6. Trigger-File Gates → Exclude / Recommend `TASK ... WHEN`

SAS batch programs often gate execution on a scheduler trigger file:
```sas
%if not %sysfunc(fileexist(/path/TRIGGER_FILE.txt)) %then %do; endsas; %end;
```
This is a **batch-scheduling mechanism**, not business logic. In Snowflake, notebooks/procedures execute their steps sequentially in one session — there is no scheduler dropping trigger files.

Rules:
- **Exclude** the trigger-check block from executable output; replace with a comment:
  `-- Trigger check excluded — sequential execution in Snowflake`
- If job gating is genuinely required, recommend a Snowflake **`TASK` with a `WHEN` clause** or **stream-based triggering** (e.g., `WHEN SYSTEM$STREAM_HAS_DATA('<stream>')`) rather than a file gate.
- Detection: block contains `fileexist` + `TRIGGER` + `endsas` (typically a `%if ... fileexist ... endsas` macro).
- Distinguish from rule 5: a **data-dependent** `FILEEXIST` gate (does an input data file exist before processing it?) must be converted per rule 5; only **scheduler trigger** files are excluded.
