# Stored Procedure Wrapping for ACT Sections

Every element's ACT logic must be wrapped in a stored procedure so it can be re-executed via `CALL`. This ensures tests are re-runnable by users and by the orchestration-fixer during its fix-test loop.

## Template

```sql
CREATE OR REPLACE PROCEDURE <DATABASE>.<SCHEMA>.test_act_<element_name>()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    -- LET variable declarations from the orchestration SQL element
BEGIN
    -- Business logic extracted from the element body
    -- All database references rewritten to <DATABASE>.<SCHEMA>
    -- EXECUTE DBT PROJECT statements commented out
    RETURN 'OK';
END;
$$;
```

After creating the procedure, execute it:

```sql
CALL <DATABASE>.<SCHEMA>.test_act_<element_name>();
```

## Snowflake Scripting Quirks

These pitfalls cause silent failures or cryptic errors. Apply them when extracting element bodies into procedures:

1. **`DECLARE...BEGIN...END` blocks cannot execute directly via SQL API** — they must be wrapped in a stored procedure. The SQL API (used by Cortex CLI and most connectors) does not support anonymous blocks.

2. **`FOR row IN cursor` fails** — `row` is a reserved word in Snowflake scripting. Replace with `record` or any non-reserved identifier:
   ```sql
   -- WRONG: FOR row IN cursor DO ...
   FOR record IN cursor DO ...
   ```

3. **`CALL proc(:variable)` may fail in scripting contexts** — bind variables in `CALL` statements are not always supported inside `BEGIN...END`. Use `EXECUTE IMMEDIATE` instead:
   ```sql
   -- WRONG: CALL my_proc(:my_var);
   EXECUTE IMMEDIATE 'CALL my_proc(''' || my_var || ''')';
   ```

4. **`EXECUTE IMMEDIATE` with multi-statement strings** — Snowflake does not support multiple statements in a single `EXECUTE IMMEDIATE` call. Split into separate calls or use a procedure.

## Naming Convention

- Procedure name: `test_act_<element_name>` (sanitized: lowercase, dots/spaces → underscores)
- Created in the user-provided `<DATABASE>.<SCHEMA>`
- Always use `CREATE OR REPLACE` for idempotent re-runs
