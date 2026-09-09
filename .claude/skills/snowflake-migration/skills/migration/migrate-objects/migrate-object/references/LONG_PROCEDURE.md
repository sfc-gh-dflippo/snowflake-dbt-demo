# Long Procedure: Decompose-Convert-Assemble

Structured workflow for converting large stored procedures (200+ non-empty source lines) that are too big for the standard fix loop to handle holistically. Instead of fixing the entire procedure at once, decompose it into logical segments, convert each independently, assemble the result, and verify.

## When to Use

- The source procedure has **200+ non-empty lines**
- The standard deploy-test-fix loop has failed 2+ iterations without converging
- The SnowConvert output is substantially broken (many EWI markers, large unconverted blocks)
- The user explicitly asks to decompose or split a procedure

## Phase 1: Decompose

### Read Source and Converted SQL

Read both files:
- **Source SQL** — the original procedure (under `source/`)
- **Converted SQL** — what SnowConvert produced (under `snowflake/`). Use this as a starting reference for segments that were partially converted correctly.

### Create a Segment Map

Identify the logical segments of the procedure. For each segment, document:

| Field | Description |
|-------|-------------|
| Segment # and name | e.g., "Seg 3: Cursor loop — build matrix" |
| Line range in source | e.g., lines 45-120 |
| Purpose | What the segment does |
| Dependencies | Shared variables, temp tables, cursors used by other segments |

Present the segment map to the user before proceeding.

### Common Segment Types

| Segment Type | What to Look For | Conversion Considerations |
|---|---|---|
| **Declarations** | Variable declarations, parameter lists | Snowflake Scripting variable syntax, type mappings |
| **Cursor operations** | DECLARE CURSOR, OPEN, FETCH, CLOSE, DEALLOCATE | Replace with RESULTSET + loop, or refactor to set-based |
| **Loop blocks** | WHILE, FOR, cursor fetch loops | Snowflake Scripting FOR/WHILE syntax |
| **Error handling** | TRY/CATCH, BEGIN...EXCEPTION, @@ERROR | Snowflake EXCEPTION blocks |
| **Temp table operations** | CREATE #temp, INSERT INTO #temp, SELECT INTO | Snowflake temporary tables (CREATE TEMPORARY TABLE) |
| **Dynamic SQL** | EXEC(@sql), EXECUTE IMMEDIATE, sp_executesql | Snowflake EXECUTE IMMEDIATE with bind variables. See [SSC-EWI-0030.md](../../../rule-engine/resolving-ewis/reference/SSC-EWI-0030.md) for conversion reference. |
| **Transaction management** | BEGIN TRAN, COMMIT, ROLLBACK, SAVE TRANSACTION | Snowflake transaction semantics (auto-commit differences) |
| **Output/result sets** | SELECT for output, OUTPUT clause, PRINT | RETURN TABLE(), RESULTSET, or SYSTEM$LOG |
| **Conditional branching** | Large IF/ELSE IF chains, CASE blocks | Direct mapping to Snowflake IF/CASE |
| **Nested procedure calls** | EXEC proc, CALL proc | Snowflake CALL syntax, parameter passing |

## Phase 2: Convert Each Segment

Convert each segment independently from the source dialect to Snowflake SQL:

1. **Focus on the segment** but keep the full procedure context in mind (shared variables, control flow)
2. **Apply platform-specific transformations** — for dynamic SQL segments, follow the guidance in [SSC-EWI-0030.md](../../../rule-engine/resolving-ewis/reference/SSC-EWI-0030.md)
3. **Preserve the segment's interface** — inputs it consumes and outputs it produces must remain compatible with adjacent segments
4. **Document any transformation decisions** that affect other segments

### Schema Qualification and PIVOT Column Quoting

Two recurring issues affect almost every decomposed T-SQL procedure. Both are documented in the shared troubleshooting reference; audit every segment against the source before assembly:

- **Schema prefixes (DBO and others) dropped by SnowConvert/CoCo.** Every `FROM`, `JOIN`, `INSERT INTO`, `UPDATE`, `MERGE INTO`, and function-call reference must keep the source schema qualifier. See [Missing Schema Prefix (DBO and others)](../../references/troubleshooting.md#missing-schema-prefix-dbo-and-others) for the full audit checklist and broken-vs-correct examples.
- **Static PIVOT output columns include the embedded single quotes in their names.** Reference them as `g."'Medical'"`, never `g.Medical` or `g."Medical"`. See [Hardcoded PIVOT Columns](../../references/troubleshooting.md#hardcoded-pivot-columns).

### Platform-Specific Quick Reference

**MS SQL Server (T-SQL) to Snowflake:**
- `@@ROWCOUNT` -> `SQLROWCOUNT`
- `@@ERROR` / `TRY...CATCH` -> `BEGIN ... EXCEPTION ... END`
- `EXEC sp_executesql` -> `EXECUTE IMMEDIATE`
- `#temp_table` -> `TEMPORARY TABLE temp_table`
- `CURSOR ... FETCH NEXT` -> `RESULTSET` + `FOR record IN cursor_result DO`
- `RAISERROR` / `THROW` -> `RAISE` or custom exception
- `VARCHAR(MAX)` -> `VARCHAR(16777216)`
- `BIT` -> `BOOLEAN`
- `GETDATE()` -> `CURRENT_TIMESTAMP()`

**Teradata to Snowflake:**
- `COLLECT STATISTICS` -> Not needed (Snowflake auto-manages)
- `VOLATILE TABLE` -> `TEMPORARY TABLE`
- `SEL` -> `SELECT`
- `QUALIFY` -> Snowflake supports QUALIFY natively
- `CASESPECIFIC` / `NOT CASESPECIFIC` -> Snowflake is case-insensitive by default

**Oracle (PL/SQL) to Snowflake:**
- `%TYPE` / `%ROWTYPE` -> Explicit type declarations
- `SYS_REFCURSOR` -> `RESULTSET`
- `DBMS_OUTPUT.PUT_LINE` -> `SYSTEM$LOG` or `RETURN`
- `NVL` -> `NVL` (supported) or `COALESCE`
- `SYSDATE` -> `CURRENT_TIMESTAMP()`
- `DUAL` table -> Not needed (Snowflake allows `SELECT` without `FROM`)

## Phase 3: Assemble

Combine all converted segments into a single Snowflake stored procedure:

1. **Consolidate variable declarations** at the top of the procedure body (DECLARE section)
2. **Order segments** to match the original control flow
3. **Resolve cross-segment references** — ensure variables, cursors, and temp tables referenced across segments are properly scoped
4. **Remove any duplicate declarations** introduced during per-segment conversion

Write the assembled procedure to the file in `snowflake/`, overwriting the failed SnowConvert output.

**Present the final assembled SQL to the user for confirmation before writing.**

## Phase 4: Verify

Use the standard migrate-object workflow to verify the assembled procedure:

1. **Deploy** using the `deploy` MCP tool (see [SKILL.md](../SKILL.md) Step 3)
2. **Run tests** using `test-runner validate` (see [SKILL.md](../SKILL.md) Step 4)
3. **Check results** — if all tests pass, proceed to rule deduction and registry update

### If Verification Fails

Map the error back to a specific segment:

| Error Location | Action |
|----------------|--------|
| **Specific segment** (e.g., cursor block, dynamic SQL section) | Re-convert only that segment, re-assemble, re-verify |
| **Segment boundary** (e.g., variable type mismatch between segments) | Adjust the interface between the two segments |
| **Systemic** (e.g., wrong procedure signature, wrong return type) | Review the overall structure, not individual segments |

After **3 failed verification attempts**, escalate to the user with the remaining issues.

## Troubleshooting

For runtime errors (`Object 'XYZ' does not exist`, `invalid identifier 'G.MEDICAL'`, PIVOT column quoting, 0-row test results, connection errors, etc.), see the shared [troubleshooting reference](../../references/troubleshooting.md). The two issues most often hit in decomposed procedures are [Missing Schema Prefix (DBO and others)](../../references/troubleshooting.md#missing-schema-prefix-dbo-and-others) and [Hardcoded PIVOT Columns](../../references/troubleshooting.md#hardcoded-pivot-columns).

### Procedure Too Large for Context Window

If the source procedure exceeds the context window even after segmentation:
- Convert one segment at a time, keeping only the segment map and the current segment in context
- Use the failed SnowConvert output as a starting reference for segments that were partially converted correctly

### Cross-Segment Dependencies Are Complex

If segments are tightly coupled (many shared cursors, deeply nested control flow):
- Group related segments together rather than converting them independently
- Convert the most independent segments first, then handle coupled segments as a group
