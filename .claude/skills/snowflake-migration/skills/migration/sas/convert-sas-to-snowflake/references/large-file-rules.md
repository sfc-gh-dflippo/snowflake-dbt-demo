# Large File Conversion Rules

## When to Load

Load when SAS file exceeds **500 lines**, **50K characters**, or **20 blocks**.

---

## Chunked Conversion Strategy

Large SAS files must be converted completely. Never truncate output.

### Approach: Dependency-Aware Block Groups

1. **Build full dependency graph** before converting any block
2. **Group blocks** into independent clusters that can be converted together
3. **Convert each group** in dependency order
4. **Validate inter-group references** — ensure table/variable names match

### Conversion Order

```
1. Parse all blocks → build dependency map (creates/reads/variables)
2. Identify independent clusters (blocks with no cross-dependencies)
3. Convert Tier 1 (pure SQL) blocks first — they are fastest
4. Convert Tier 2 (stored procedure) blocks next
5. Convert Tier 3 (PySpark) blocks last
6. Validate cross-references between all converted blocks
```

---

## Output Completeness Rules

### NEVER Truncate

- If a block has 100+ lines: convert ALL lines
- If a block creates 10 tables: generate ALL 10 CREATE TABLE statements
- If a macro has 20 internal steps: convert ALL 20 steps
- If an ARRAY iterates over 50 columns: generate ALL 50 column expressions

### NEVER Summarize

These shortcuts are FORBIDDEN in output:
- "similar pattern for remaining columns"
- "same as above"
- "repeat for other tables"
- "adjusted joins/filters"
- "... and so on for columns X through Z"
- Any ellipsis (`...`) replacing actual logic

### Verify Completeness

After generating conversion for each block:
1. Count output tables in SAS → verify same count in Snowflake
2. Count CALL SYMPUT/SYMPUTX assignments → verify all persisted
3. Count %IF branches → verify all branches converted
4. Count column derivations → verify all present

---

## Repeated Macro Invocations

When a macro is called multiple times with different parameters:

1. **Track each invocation separately** — different parameters may trigger different branches
2. **Do NOT assume** all invocations produce the same output structure
3. For %IF/%THEN branches controlled by parameters, verify which branch each invocation takes
4. Generate separate SQL for each invocation if outputs differ
5. If macro is called >5 times, consider converting to a stored procedure called multiple times

### Example: Macro called with different date parameters

```sas
%process_month(month=JAN, year=2024);
%process_month(month=FEB, year=2024);
%process_month(month=MAR, year=2024);
```

Convert to:
```sql
CALL sp_process_month('JAN', 2024);
CALL sp_process_month('FEB', 2024);
CALL sp_process_month('MAR', 2024);
```

NOT to a single call or summary comment.

---

## Inter-Block Dependency Rules

### Table Dependencies

- A temp table created in block N may be consumed by block N+2, N+3, or later
- Do NOT assume consumption is always N+1
- Session variables persist across ALL blocks in the session
- Temporary tables persist across ALL blocks in the session
- Do NOT recreate a temp table that was already created upstream

### Variable Dependencies

- Macro variables set via CALL SYMPUT in one step may be referenced in distant downstream steps
- In Snowflake: persist via `EXECUTE IMMEDIATE 'SET ...'` and reference as `$VAR_NAME`
- Track ALL variable assignments and their downstream consumers

### Column Dependencies

- Verify column names match between producer and consumer blocks
- If block N renames a column (e.g., RENAME in SAS), downstream blocks must use the new name
- If block N adds a computed column, downstream blocks may reference it

---

## Error Recovery for Large Files

If conversion fails partway through:
1. Save completed blocks to the output file
2. Mark the failing block with MANUAL_REVIEW_REQUIRED
3. Continue converting remaining blocks
4. Report: "X of Y blocks converted successfully. Block Z requires manual review: [reason]"
