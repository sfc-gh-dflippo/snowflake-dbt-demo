# Step-Based Test YAML — Cheat Sheet

Quick reference for the YAML shape `scai test capture` and `scai test validate` consume. Loaded on demand by:

- [`baseline-capture/SWARM.md`](../baseline-capture/SWARM.md) when filling `test_cases:` for an existing stub.
- [`migrate-object/DIAGNOSE_FIX.md`](../migrate-object/DIAGNOSE_FIX.md) when interpreting a failing test.
- [`migrate-object/EDIT_TEST_YAML.md`](../migrate-object/EDIT_TEST_YAML.md) when editing a YAML for a special case (multi-RS, OUT params, table-read, cursor, side-effect DML, before/after capture).

> **Source of truth:** [`testing-infrastructure/docs/step-based-test-yaml-configuration.md`](https://github.com/snowflakedb/migrations-snowconvert-desktop/blob/main/testing-infrastructure/docs/step-based-test-yaml-configuration.md). This file is a distilled cheat sheet — when the two disagree, the upstream doc wins.

---

## Top-level structure

```yaml
validation:
  steps: [...]              # required, non-empty
  test_cases: [...]         # optional, defaults to []
  modifies_data: true       # optional, inferred from CUR by default
  affected_tables:          # optional, inferred from CUR by default
    - Database.Schema.Table
```

A file is recognized as step-based when `validation` contains a `steps` list. The runner discovers files by scanning `artifacts/**/test/*.yml`.

All target-side step SQL runs in a single Snowflake `BEGIN...END;` scripting block; session state (variables declared with `LET`) carries forward between steps. Source-side behavior is dialect-specific (SQL Server: one T-SQL batch; Redshift: individual statements in one transaction).

---

## The four step types

Each step must use keys from exactly one type. Mixing keys across types is an error.

### 1. SQL Query Step — `source_query` / `target_query` / `both`

The default and most common step type.

```yaml
- source_query: "EXECUTE MyDB.dbo.GetOrders @region = {0}"
  target_query: "CALL MyDB.dbo.GetOrders({0})"
```

- `both: "SQL"` is shorthand for setting both sides to the same string.
- Omit one side to skip it (`target_query:` only, no `source_query:` → source-side no-op for that step).
- Multiline SQL uses YAML block scalars (`|-` strips the trailing newline).

### 2. Output Parameter Comparison Step — `source_params` / `target_params`

Compares OUTPUT / INOUT param values after a procedure call.

```yaml
- source_params: ["@totalOrders", "@totalSpent"]
  target_params: ["TOTALORDERS", "TOTALSPENT"]
```

Always validates — `validate: false` is rejected. Snowflake side reads `:TOTALORDERS`, etc. inside the scripting block.

### 3. Table Read Step — `table` / `source_table` / `target_table`

Reads a table and compares. Use when a proc writes its output to a persistent table.

```yaml
- table: "MyDB.dbo.OrderSummary"
# or different names per side:
- source_table: "MyDB.dbo.OrderSummary_v1"
  target_table: "MyDB.dbo.OrderSummary"
```

Always validates. Snowflake side emits `SELECT * FROM IDENTIFIER('{name}')`.

### 4. Cursor Read Step — `cursor` / `source_cursor` / `target_cursor`

Reads a cursor's rows. **Redshift only on the source side** — SQL Server uses multi-RS instead.

```yaml
- cursor: "result_cursor"
```

Always validates. Redshift emits `FETCH ALL FROM {cursor}`; Snowflake emits `SELECT * FROM IDENTIFIER('{cursor}')`.

---

## The `validate` field

Applies to SQL Query Steps only (the other three step types always validate).

| Value | Behavior |
|---|---|
| `true` (default) | Result is captured and compared between source and target. |
| `false` | Step executes but no result is captured. Used for setup, declarations, and side-effecting calls whose result you don't compare directly. |
| `[list]` | **SQL Server source → Snowflake target only.** Maps source result sets (in order) to comparison targets. See [Multi-Result-Set Validation](#multi-result-set-validation). |

```yaml
- source_query: "DECLARE @count INT = 0"
  target_query: "LET COUNT INT := 0"
  validate: false       # executes, not compared
```

---

## Multi-result-set validation

For SQL Server procedures returning multiple result sets. Each list entry maps one source RS (in order) to a comparison target.

| Entry shape | Meaning |
|---|---|
| `false` | Skip this result set. |
| `result` | Compare against the CALL's direct return value on target. |
| `table: "name"` | Compare against `SELECT * FROM <name>` on target. |
| `cursor: "name"` | Compare against the named cursor on target. |
| `target_query: "SQL"` | Compare against the result of arbitrary SQL on target. |

```yaml
- source_query: "EXECUTE MyDB.dbo.GetDashboard @region = {0}"
  target_query: "CALL MyDB.dbo.GetDashboard({0})"
  validate:
    - target_query: "SELECT * FROM MyDB.dbo.T_Orders ORDER BY Status"
    - false                              # skip RS[1] (debug output)
    - table: "MyDB.dbo.T_Summary"
```

Redshift does not support `validate: [list]`. Use cursor read steps instead.

---

## Placeholders and `test_cases`

`{0}`, `{1}`, ... in step SQL are substituted from the current test case array, formatted as dialect-correct SQL literals.

```yaml
test_cases:
  - ["West", "active"]    # {0} = 'West', {1} = 'active'
  - ["East", null]         # {0} = 'East', {1} = NULL
  - []                     # no placeholders (zero-arg)
```

Substitution table (high-signal rows):

| YAML value | SQL Server | Snowflake | Redshift |
|---|---|---|---|
| `null` | `NULL` | `NULL` | `NULL` |
| `true` / `false` | `1` / `0` | `TRUE` / `FALSE` | `TRUE` / `FALSE` |
| `42` | `42` | `42` | `42` |
| `"hello"` | `'hello'` | `'hello'` | `'hello'` |
| `"it's"` | `'it''s'` | `'it''s'` | `'it''s'` |

All steps run once per test case, in a fresh session per case. Placeholder indices that exceed the array length are left as the literal `{N}` text — no error.

---

## `modifies_data` and `affected_tables` are inferred from CUR

Both fields are **optional overrides**. When omitted, the runner reads the Code Unit Registry's metadata for the object being tested. **Don't set them by default** — the inference is the right answer for the vast majority of procedures.

Override only when:

- CUR doesn't detect DML (`modifies_data: true` to force delta capture).
- Forcing skip of delta capture (`modifies_data: false`).
- CUR misses a table the procedure touches (`affected_tables: [...]` to add).

When delta capture is active, the runner snapshots `SELECT *` from each affected table on both sides before steps run, snapshots again after, and compares deltas (inserts / deletes / changes).

---

## Things that bite

A handful of behaviors that surprise agents reading or writing these YAMLs:

### CALL detection on Snowflake

The runner checks whether `target_query` **starts with `CALL ` (case-insensitive, after trim)**. This determines result capture:

- `CALL ...` + `validate: true` → CALL runs; result captured via `RESULT_SCAN(LAST_QUERY_ID())`.
- `CALL ...` + `validate: false` → CALL runs; no capture.
- Not a CALL + `validate: true` → SQL wrapped in `CREATE OR REPLACE TEMPORARY TABLE _step_N AS <query>`.

**Implication:** if you want a procedure's return value compared, the step's `target_query` must *start* with `CALL ` — no preceding statements. Need to do work after a CALL? Put it in a follow-up step.

### Scripting block scope

All target steps run in one `BEGIN ... END;` block. Variables declared with `LET` in step 0 are visible in step 5. References use `:VARNAME` (uppercase, colon prefix). No need to redeclare across steps.

### Reserved temp table names

The runner uses these internally; avoid them in your own SQL:

- `_step_N` — captured result for step N
- `_step_N_vK` — result for the Kth entry of `validate: [list]` on step N
- `_rs_N` — raw CALL result captured for a `validate: [list]` `"result"` entry

### `validate: false` is for SQL Query Steps only

Output-Parameter, Table-Read, and Cursor-Read steps always validate. Setting `validate: false` on any of them is a parse error.

### Source-side execution differs by dialect

- **SQL Server source:** all steps run in one T-SQL batch. `DECLARE`'d variables and OUTPUT parameters persist across steps.
- **Redshift source:** steps run individually inside one transaction. INOUT params are extracted from CALL result rows (no `DECLARE` needed). One cursor open at a time.
- **`validate: [list]`** is SQL Server only.

---

## When you're stuck on a special case

Don't try to author multi-RS, OUT-param, table-read, cursor-read, side-effect DML, or before/after-capture YAMLs from this cheat sheet. The recipes for each live in [`migrate-object/EDIT_TEST_YAML.md`](../migrate-object/EDIT_TEST_YAML.md) — each carries a before/after example, when to use, and dialect-specific gotchas.
