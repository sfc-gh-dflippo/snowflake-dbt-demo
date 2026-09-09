# SSC-EWI-TS0083: ROLLBACK TRANSACTION REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED

> Legacy code: SSC-EWI-0073 (SCAI versions prior to v2.17).

## Context

SQL Server stored procedures commonly use the defensive error-handling pattern:

```sql
BEGIN CATCH
    IF (@@TRANCOUNT > 0)
        ROLLBACK TRANSACTION;
    THROW;
END CATCH
```

This pattern checks whether an active transaction exists, rolls it back on error, and re-raises the original exception. It works across procedure boundaries: a proc can roll back a transaction started by its caller.

SnowConvert (SCAI) cannot auto-resolve this because:

1. **`@@TRANCOUNT`** has no Snowflake equivalent. SCAI converts it to `:TRANCOUNT`, an uninitialized variable that is always NULL.
2. **`ROLLBACK TRANSACTION`** fails with error 90239 when the transaction was started by the caller (cross-scope). Snowflake enforces scoped transactions — a proc cannot commit or rollback a transaction it did not start.
3. **`THROW`** is converted to `LET DECLARED_EXCEPTION EXCEPTION; RAISE DECLARED_EXCEPTION;`, which creates a new generic exception (-20000) instead of re-raising the original error.

### Source Construct

**Pattern 1: `@@TRANCOUNT` guard + `THROW`** (16 of 19 procedures)

```sql
BEGIN CATCH
    -- diagnostic logging omitted for brevity
    IF (@@TRANCOUNT > 0)
    BEGIN
        ROLLBACK TRANSACTION;
    END;
    THROW;
END CATCH
```

**Pattern 2: `XACT_STATE()` guard + retry loop** (3 of 19 procedures)

```sql
BEGIN CATCH
    SET @errnum = ERROR_NUMBER()
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION
    IF @errnum IN (1205, -2)
    BEGIN
        -- retry logic
    END
    ELSE
    BEGIN
        RAISERROR(@errmsg, 16, 1)
        RETURN 9
    END
END CATCH
```

### SnowConvert Output

**Pattern 1 SCAI output (broken):**

```sql
EXCEPTION
    WHEN OTHER THEN
        -- diagnostic logging
        IF ((:TRANCOUNT > 0)) THEN          -- BUG 1: uninitialized variable
            BEGIN
                !!!RESOLVE EWI!!! /*** SSC-EWI-TS0083 - ROLLBACK TRANSACTION REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED. ***/!!!
                ROLLBACK TRANSACTION;        -- BUG 2: fails 90239 cross-scope
            END;
        END IF;
        LET DECLARED_EXCEPTION EXCEPTION;    -- BUG 3: new exception, loses original
        RAISE DECLARED_EXCEPTION;
```

**Pattern 2 SCAI output:** SCAI correctly converts `XACT_STATE() <> 0` to `CURRENT_TRANSACTION() IS NOT NULL`, but ROLLBACK is still unwrapped (BUG 2) and the `!!!RESOLVE EWI!!!` marker is present.

## Workaround

Apply three targeted fixes to the SCAI-generated EXCEPTION block.

### Prerequisites

None. No UDFs, helper objects, or one-time setup required.

### Snowflake Code

**FIX 1 — Replace transaction guard:**

```sql
-- BEFORE (SCAI output):
IF ((:TRANCOUNT > 0)) THEN

-- AFTER (fix):
IF ((CURRENT_TRANSACTION() IS NOT NULL)) THEN
```

**FIX 2 — Wrap ROLLBACK in exception handler:**

```sql
-- BEFORE (SCAI output):
BEGIN
    !!!RESOLVE EWI!!! /*** SSC-EWI-TS0083 ... ***/!!!
    ROLLBACK TRANSACTION;
END;

-- AFTER (fix):
BEGIN
    ROLLBACK;
EXCEPTION
    WHEN OTHER THEN
        NULL; /*** Cross-scope ROLLBACK: caller owns the transaction, swallow 90239 ***/
END;
```

**FIX 3 — Replace RAISE with bare RAISE:**

```sql
-- BEFORE (SCAI output):
LET DECLARED_EXCEPTION EXCEPTION;
RAISE DECLARED_EXCEPTION;

-- AFTER (fix):
RAISE; /*** Re-raise the original exception (equivalent to SQL Server THROW) ***/
```

**Complete fixed EXCEPTION block (Pattern 1):**

```sql
EXCEPTION
    WHEN OTHER THEN
        MSG := :THIS_PROC || ' : !!ERROR : at line N/A' || ' : err_no=' || CAST(SQLCODE AS VARCHAR) || ' : err_msg=' || SQLERRM;
        SYSTEM$LOG_INFO(:MSG);
        IF ((CURRENT_TRANSACTION() IS NOT NULL)) THEN
            BEGIN
                ROLLBACK;
            EXCEPTION
                WHEN OTHER THEN
                    NULL; /*** Cross-scope ROLLBACK: caller owns the transaction, swallow 90239 ***/
            END;
        END IF;
        RAISE; /*** Re-raise the original exception (equivalent to SQL Server THROW) ***/
```

### Parity Status

**FUNCTIONAL PARITY** — Full data-integrity parity across all scenarios. Two mechanism differences documented:

1. **Cross-scope ROLLBACK mechanism**: In SQL Server, the proc's ROLLBACK directly undoes the caller's transaction. In Snowflake, the proc's ROLLBACK fails (90239, swallowed), and Snowflake's auto-rollback handles it at scope exit. **Data outcome is identical.**
2. **Pattern 2 RAISERROR**: `RAISERROR_UDF` does not propagate exceptions (tracked under SSC-FDM-TS0019, separate EWI). ROLLBACK behavior is correct.

## Instructions

1. **Identify the EWI pattern** in SCAI output. Search for:
   ```
   !!!RESOLVE EWI!!! /*** SSC-EWI-TS0083
   ```
   Also search for `:TRANCOUNT` (Pattern 1 indicator) and `LET DECLARED_EXCEPTION EXCEPTION` (BUG 3 indicator).

2. **Apply FIX 1** — Replace the transaction guard:
   - Search: `IF ((:TRANCOUNT > 0)) THEN`
   - Replace: `IF ((CURRENT_TRANSACTION() IS NOT NULL)) THEN`
   - Note: Pattern 2 procs may already have `CURRENT_TRANSACTION() IS NOT NULL` (SCAI handles `XACT_STATE()` correctly). Skip FIX 1 if already correct.

3. **Apply FIX 2** — Wrap the ROLLBACK block. Replace the entire `BEGIN ... END` block containing the `!!!RESOLVE EWI!!!` marker and `ROLLBACK TRANSACTION`:
   - Remove the `!!!RESOLVE EWI!!!` line
   - Replace `ROLLBACK TRANSACTION;` with `ROLLBACK;`
   - Add `EXCEPTION WHEN OTHER THEN NULL;` before the closing `END;`

4. **Apply FIX 3** — Replace the RAISE statement:
   - Search: `LET DECLARED_EXCEPTION EXCEPTION;\n                RAISE DECLARED_EXCEPTION;`
   - Replace: `RAISE;`
   - Note: Only applies to Pattern 1. Pattern 2 procs use `RAISERROR_UDF` + `RETURN 9` (separate issue).

5. **Verify** by running the mock workaround test:
   - Create `stress_source` with one good row and one NULL row (column mapped to NOT NULL target).
   - Create `stress_target` with NOT NULL constraint on first column.
   - Test: happy path, error without transaction, error with caller transaction, nested calls.
   - Expected: error is caught, ROLLBACK succeeds or is absorbed, only pre-existing data survives.

## Guardrails

### Positive Constraints (DO)

- **DO** replace `:TRANCOUNT > 0` with `CURRENT_TRANSACTION() IS NOT NULL` in every converted EXCEPTION block — Evidence: Stress tests S3, S4
- **DO** wrap `ROLLBACK` in `BEGIN ... EXCEPTION WHEN OTHER THEN NULL; END;` whenever the proc uses `EXECUTE AS CALLER` — Evidence: Stress tests S4, S6
- **DO** replace `LET DECLARED_EXCEPTION EXCEPTION; RAISE DECLARED_EXCEPTION;` with bare `RAISE;` — Evidence: Step 4 Tests 2, 3
- **DO** keep the `IF (CURRENT_TRANSACTION() IS NOT NULL)` guard to skip ROLLBACK when no transaction is active — Evidence: Stress tests S3, S8
- **DO** preserve `EXECUTE AS CALLER` — required for scoped transaction visibility
- **DO** apply FIX 2 even when the proc has its own `BEGIN TRANSACTION` — the wrapper is harmless for same-scope ROLLBACK and protective when a caller also has a transaction — Evidence: Stress test S5

### Negative Constraints (DO NOT)

- **No Hallucinations**: never suggest non-existent Snowflake syntax or functions (e.g., `@@TRANCOUNT`, `XACT_STATE()`, `THROW`)
- **No Logic Deletion**: never remove the ROLLBACK block, the transaction guard, or the error re-raise
- **No Lazy Bypassing**: never comment out the ROLLBACK or replace it with a no-op
- **DO NOT** replace `CURRENT_TRANSACTION() IS NOT NULL` with a boolean variable or manual transaction tracking
- **DO NOT** add `BEGIN TRANSACTION` inside the proc to "fix" the cross-scope issue — this changes transactional semantics
- **DO NOT** use `RAISE DECLARED_EXCEPTION` or any named exception — only bare `RAISE;` preserves original error context
- **DO NOT** change `WHEN OTHER THEN NULL` in the ROLLBACK wrapper to a more specific exception — error 90239 has no named exception constant
- **DO NOT** attempt to fix `RAISERROR_UDF` (SSC-FDM-TS0019) as part of this EWI

### Known Limitations

- **L1: Cross-scope ROLLBACK mechanism differs** — SQL Server ROLLBACK works across scopes; Snowflake's fails (90239, absorbed) and auto-rollback handles it. Data outcome is identical; mechanism differs. — Evidence: Step 4 Test 4
- **L2: No doomed-transaction concept** — SQL Server `XACT_STATE() = -1` (doomed) has no Snowflake equivalent. `CURRENT_TRANSACTION() IS NOT NULL` covers active transactions but cannot distinguish doomed state. Acceptable for this codebase: only `XACT_STATE() <> 0` is used. — Evidence: Step 3 Baseline
- **L3: Error codes differ** — SQL Server error numbers (208, 515, 1205, -2) do not map 1:1 to Snowflake SQLCODEs. The deadlock/timeout retry logic (`@errnum IN (1205, -2)`) will never match. Separate concern from ROLLBACK. — Evidence: Step 3 Baseline
- **L4: `RAISERROR_UDF` does not raise** — SCAI's `RAISERROR_UDF` is a scalar function, not an exception-raising mechanism. Tracked under SSC-FDM-TS0019. — Evidence: Step 4 Tests 6, 7

### Corner Cases

| # | Input / Scenario | Source Behavior | Snowflake Behavior | Handling |
|---|-----------------|----------------|-------------------|----------|
| S1 | Happy path, no tran | 2 rows inserted, return 0 | OK: 2 rows inserted | No ROLLBACK path exercised |
| S2 | Empty result set (no matching rows) | 0 rows, return 0 | OK: 0 rows inserted | No error, no ROLLBACK |
| S3 | Error + no active tran | CATCH → @@TRANCOUNT=0 → skip ROLLBACK → THROW | EXCEPTION → CURRENT_TRANSACTION()=NULL → skip → RAISE | ROLLBACK correctly skipped |
| S4 | Error + caller tran + no handler | CATCH → ROLLBACK succeeds → THROW aborts | EXCEPTION → 90239 swallowed → RAISE → auto-rollback | Only pre-existing data survives |
| S5 | Same-scope tran (proc owns BEGIN TRAN) | CATCH → ROLLBACK succeeds (same scope) | EXCEPTION → ROLLBACK succeeds (no 90239) | Only pre-existing data survives |
| S6 | Nested call (outer→inner, inner fails) | Inner ROLLBACK undoes outer tran | Inner 90239 swallowed, outer ROLLBACK succeeds | Only pre-existing data survives |
| S7 | Sequential errors, no tran | Both errors caught, @@TRANCOUNT=0 | Both errors caught, no orphaned tran | No state leakage |
| S8 | No active tran path (autocommit) | @@TRANCOUNT=0 → ROLLBACK skipped | CURRENT_TRANSACTION()=NULL → ROLLBACK skipped | Guard prevents error |
