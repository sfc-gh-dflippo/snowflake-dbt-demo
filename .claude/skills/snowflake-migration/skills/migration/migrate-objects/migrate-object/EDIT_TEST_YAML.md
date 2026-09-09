# Edit Test YAML — Recipes for Special Cases

On-demand recipe book for editing an existing step-based test YAML when the default scaffolded shape isn't enough. Loaded by [`DIAGNOSE_FIX.md`](DIAGNOSE_FIX.md) Step 2.5 after a failing test points at a YAML-shape issue (multi-RS proc returned more sets than the stub asserts, OUT param mismatch, "no rows captured" on a DML proc, etc.).

Always load the [`step-based-yaml.md` cheat sheet](../references/step-based-yaml.md) alongside this file when editing — the cheat sheet explains the schema; this file shows how to apply it.

## Routine

1. Read the existing YAML at `<project_dir>/<files.artifacts.path>/test/*.yml` (from `query_registry`; use verbatim — do not reconstruct).
2. Identify which recipe matches the failure (table below).
3. Apply the recipe — keep `test_cases:` untouched unless the recipe says otherwise.
4. Re-run `scai test capture --where "source.canonicalName ILIKE '%<obj>%'"` to refresh the baseline.
5. Re-run `scai test validate ...` to confirm the fix.

| Failure smell | Recipe |
|---|---|
| Multi-result-set source proc; only first RS compared | [Multi-result-set validation](#multi-result-set-validation) |
| "unexpected null column" / value differs in OUT/INOUT param | [OUT / INOUT parameter comparison](#out--inout-parameter-comparison) |
| Proc writes to a persistent table; no rows captured | [Table-read assertion](#table-read-assertion) |
| Redshift proc returns a refcursor | [Cursor-read step](#cursor-read-step) |
| DML proc; "no rows captured" but delta tracking expected | [Side-effect-only DML](#side-effect-only-dml) |
| Need before/after view of a row a proc mutates | [Before/after state capture](#beforeafter-state-capture) |
| Dialect-specific quirk (see "Per-dialect gotchas" section) | [Per-dialect gotchas](#per-dialect-gotchas) |

---

## Multi-result-set validation

**When.** Source proc returns N result sets (SQL Server's `SELECT ... ; SELECT ... ; SELECT ...` pattern). The Snowflake target either writes each RS to a named table, returns them concatenated, or returns one and skips the rest.

**SQL Server source only.** Redshift rejects `validate: [list]` — use [Cursor-read step](#cursor-read-step) instead.

**Edit.** Change the CALL step's `validate` field from default (`true`) to a list, one entry per source RS in order.

```yaml
# Before
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.GetDashboard @region = {0}"
      target_query: "CALL MyDB.dbo.GetDashboard({0})"
  test_cases:
    - ["West"]

# After
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.GetDashboard @region = {0}"
      target_query: "CALL MyDB.dbo.GetDashboard({0})"
      validate:
        - target_query: "SELECT * FROM MyDB.dbo.T_Orders ORDER BY Status"
        - table: "MyDB.dbo.T_TopProducts"
        - target_query: "SELECT * FROM MyDB.dbo.T_RegionTotal ORDER BY Category"
  test_cases:
    - ["West"]
```

**Entry shapes.**

| Shape | Use when |
|---|---|
| `false` | This RS is debug output / not migrated. Skip. |
| `result` | Snowflake target also returns this RS as the CALL's direct return value. |
| `table: "name"` | Target wrote this RS to a persistent table. Compare via `SELECT *` on that table. |
| `cursor: "name"` | Target wrote this RS to a named cursor. |
| `target_query: "SQL"` | Anything more complex — `ORDER BY`, `WHERE _RESULT_SET_ID = N`, etc. |

**Concatenated-into-one-table pattern.** If the Snowflake migration writes all N source RSs to a single table with a `_RESULT_SET_ID` discriminator column, filter per entry:

```yaml
validate:
  - target_query: "SELECT ID, Name FROM MyDB.dbo.T_AllOrders WHERE _RESULT_SET_ID = 1 ORDER BY OrderDate"
  - target_query: "SELECT ID, Name FROM MyDB.dbo.T_AllOrders WHERE _RESULT_SET_ID = 2 ORDER BY OrderDate"
```

---

## OUT / INOUT parameter comparison

**When.** Proc has an `OUTPUT` (SQL Server) or `INOUT` (Redshift, Snowflake) parameter and the test should verify its post-call value, not the proc's return value.

**Three steps:** declare → call → compare params. The CALL step itself uses `validate: false` because we're not comparing the proc's direct return — the next step compares the param values.

### SQL Server source

```yaml
validation:
  steps:
    - source_query: "DECLARE @name VARCHAR(100) = {1}, @price DECIMAL(10,2) = {2}"
      target_query: "LET NAME STRING := {1}; LET PRICE NUMBER(10,2) := {2}"
      validate: false

    - source_query: "EXECUTE MyDB.dbo.GetProduct @id = {0}, @name = @name OUTPUT, @price = @price OUTPUT"
      target_query: "CALL MyDB.dbo.GetProduct({0}, :NAME, :PRICE)"
      validate: false

    - source_params: ["@name", "@price"]
      target_params: ["NAME", "PRICE"]

  test_cases:
    - [1, "", 0]
    - [3, "", 0]
```

Notes:

- `LET` declarations on the Snowflake side use uppercase variable names; references use `:NAME` (colon prefix).
- Multi-statement `LET` declarations can be combined in one step (`LET A...; LET B...;`).
- The `test_cases` initial values for OUT params are placeholders — the runner doesn't use them on the source side once `DECLARE` has set the initial value. Empty string / 0 is conventional.

### Redshift source

Redshift INOUT params are extracted from the CALL result row automatically — no `DECLARE` needed on the source side.

```yaml
validation:
  steps:
    - target_query: "LET NAME STRING := {1}"
      validate: false

    - source_query: "CALL mydb.dbo.get_product({0}, {1})"
      target_query: "CALL MyDB.dbo.GetProduct({0}, :NAME)"
      validate: false

    - source_params: ["name"]
      target_params: ["NAME"]

  test_cases:
    - [1, ""]
```

---

## Table-read assertion

**When.** Proc writes its output to a persistent table rather than returning a result set; the test should compare what's in that table after the proc runs.

**Edit.** Add a Table Read Step after the CALL.

```yaml
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.PopulateSummary @region = {0}"
      target_query: "CALL MyDB.dbo.PopulateSummary({0})"
      validate: false

    - table: "MyDB.dbo.OrderSummary"
  test_cases:
    - ["West"]
    - ["East"]
```

`table:` reads `SELECT *` (Snowflake side uses `IDENTIFIER('{name}')`). If source and target use different names:

```yaml
- source_table: "MyDB.dbo.OrderSummary_v1"
  target_table: "MyDB.dbo.OrderSummary"
```

For non-trivial reads (filter, order, project columns), use a SQL Query Step with `both:` instead:

```yaml
- both: "SELECT Region, COUNT(*) FROM MyDB.dbo.OrderSummary WHERE Region = {0} GROUP BY Region"
```

---

## Cursor-read step

**Redshift only on the source side.** SQL Server should use [Multi-result-set validation](#multi-result-set-validation).

```yaml
validation:
  steps:
    - source_query: "CALL mydb.dbo.return_orders({0}, 'result_cursor')"
      target_query: "CALL MyDB.dbo.ReturnOrders({0})"
      validate: false

    - cursor: "result_cursor"

  test_cases:
    - ["West"]
```

Redshift emits `FETCH ALL FROM result_cursor`. Snowflake emits `SELECT * FROM IDENTIFIER('result_cursor')`.

**Constraints.** Redshift allows one cursor open per session at a time, and cursors are transaction-scoped. Sequential cursor reads across steps are fine; nested ones are not.

---

## Side-effect-only DML

**When.** Proc performs DML (INSERT / UPDATE / DELETE / MERGE) and has no return value worth comparing. The test should verify the *data state* after the call.

**Two ways**, often combined:

### A. Delta capture (automatic)

Let the runner snapshot affected tables before / after the call and compare deltas.

```yaml
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.InsertProduct @name = {0}, @category = {1}, @price = {2}"
      target_query: "CALL MyDB.dbo.InsertProduct({0}, {1}, {2})"
      validate: false

  modifies_data: true
  affected_tables:
    - MyDB.dbo.Products
  test_cases:
    - ["Widget", "Hardware", 12.34]
```

**Only override `modifies_data` / `affected_tables` when CUR's inference is wrong.** In most cases, omit both — the runner reads them from the registry.

### B. Explicit post-condition assertions

Add follow-up SQL Query Steps that select the rows you want to verify.

```yaml
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.InsertProduct @name = {0}, @category = {1}, @price = {2}"
      target_query: "CALL MyDB.dbo.InsertProduct({0}, {1}, {2})"
      validate: false

    - both: "SELECT Name, Category, Price FROM MyDB.dbo.Products WHERE Name = {0}"
    - both: "SELECT COUNT(*) AS Total FROM MyDB.dbo.Products"

  test_cases:
    - ["Widget", "Hardware", 12.34]
```

Use (B) when you want surgical row-level assertions and don't trust delta tracking for this proc. Use (A) when you want broad "did anything else change?" coverage.

---

## Before/after state capture

**When.** A proc mutates a row and you want to verify both the read-before-mutation behavior and the post-mutation state, or you want to compare the pre/post values for a specific record.

```yaml
validation:
  steps:
    - both: "SELECT Quantity FROM MyDB.dbo.Orders WHERE ID = {0}"

    - source_query: "DECLARE @newQty INT = 0"
      target_query: "LET NEWQTY INT := 0"
      validate: false

    - source_query: "EXECUTE MyDB.dbo.AdjustQty @orderId = {0}, @delta = {1}, @newQty = @newQty OUTPUT"
      target_query: "CALL MyDB.dbo.AdjustQty({0}, {1}, :NEWQTY)"

    - source_params: ["@newQty"]
      target_params: ["NEWQTY"]

    - both: "SELECT Quantity FROM MyDB.dbo.Orders WHERE ID = {0}"

  modifies_data: true
  affected_tables:
    - MyDB.dbo.Orders
  test_cases:
    - [7, 5]
```

Five steps: pre-snapshot → DECLARE → CALL → param read → post-snapshot. The runner compares step 0 (pre) and step 4 (post) independently as two separate validation points, so divergent pre or post state both surface as named-step failures.

---

## Per-dialect gotchas

Patterns that come up often enough to deserve their own section.

### SQL Server: temp-table return via `#TempTable`

A proc populates a global temp table (`##Foo` or `#Foo`) and the caller reads it. The runner needs an explicit read step after the CALL.

```yaml
validation:
  steps:
    - source_query: "EXECUTE MyDB.dbo.PopulateTemp @region = {0}"
      target_query: "CALL MyDB.dbo.PopulateTemp({0})"
      validate: false

    - source_query: "SELECT * FROM {1} ORDER BY OrderID"
      target_query: "SELECT * FROM {1} ORDER BY OrderID"

  test_cases:
    - ["West", "##temp_orders"]
```

Pass the temp-table name as a placeholder so the test stays parametric. **Use `{N}` (quoted) for normal placeholders; if the runner is over-quoting an identifier, use `{UNQUOTED:N}` instead** — but this is rare since the temp-table name is typically a string literal anyway.

### Redshift: scalar INOUT — anonymous block & column aliasing

Snowflake `OUT` params can't take literal values; the migration typically wraps the CALL in an anonymous block. Redshift returns the param as a column named after the param; the Snowflake anonymous block returns it as `"ANONYMOUS BLOCK"`. Alias to match.

```yaml
validation:
  steps:
    - source_query: "CALL mydb.dbo.calc_result({0}, {1}, 0)"
      target_query: |-
        BEGIN
          LET out_var NUMERIC := 0;
          CALL MyDB.dbo.CalcResult({0}, {1}, :out_var);
          RETURN :out_var;
        END;
      validate:
        - target_query: 'SELECT "ANONYMOUS BLOCK" AS P_RESULT FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))'

  test_cases:
    - [2024, 1]
```

Key points:

- The `BEGIN ... END;` block is needed because Snowflake OUT params cannot accept literal values.
- The `target_query` of the `validate: [list]` entry aliases `"ANONYMOUS BLOCK"` (Snowflake's auto-column) to the Redshift param name (`P_RESULT`) so column names match.
- The initial value (`0`) in the test case is the Redshift literal seed; Snowflake reads from `:out_var` via `LET`.

### Redshift: INOUT carries a temp-table name

A proc takes an INOUT param that's the name of a temp table the proc populates. Caller passes a literal name; both sides read the temp table.

```yaml
validation:
  steps:
    - source_query: "CALL mydb.dbo.get_orders({0}, {1}, 'temp_orders')"
      target_query: |-
        BEGIN
          LET out_var VARCHAR := 'temp_orders';
          CALL MyDB.dbo.GetOrders({0}::TIMESTAMP_NTZ, {1}::TIMESTAMP_NTZ, :out_var);
        END;
      validate: false

    - both: "SELECT * FROM temp_orders ORDER BY order_id"

  test_cases:
    - ["2025-01-01 00:00:00", "2025-01-31 23:59:59"]
```

The temp table persists in the session, so both source and target read from it directly (no `RESULT_SCAN`). Cast Snowflake params explicitly when the proc expects typed inputs (`{0}::TIMESTAMP_NTZ`).

### Teradata: cross-database GRANTs (when using clone isolation)

See [`platforms/teradata.md`](../baseline-capture/synthetic-seeder/platforms/teradata.md) — the full guidance, including the GRANT step template and call syntax, lives there.

### Oracle

See [`synthetic-seeder/platforms/oracle.md`](../baseline-capture/synthetic-seeder/platforms/oracle.md) for all Oracle-specific patterns: anonymous PL/SQL block execution model, `source_declare` syntax, package member three-part FQN, artifact path conventions, OUT params, and SYS_REFCURSOR.

---

## Things this file is not for

- **Adding new test cases.** That's [`baseline-capture/SWARM.md`](../baseline-capture/SWARM.md) — agents fill `test_cases:` against an existing stub structure.
- **Authoring a YAML from scratch.** [`baseline-capture/synthetic-seeder/SKILL.md`](../baseline-capture/synthetic-seeder/SKILL.md) is the only place that authors whole step-based YAMLs without a `scai test seed` stub.
- **Schema reference.** See [`step-based-yaml.md`](../references/step-based-yaml.md).

If a YAML edit is needed but no recipe above matches, prefer to read the [upstream schema doc](https://github.com/snowflakedb/migrations-snowconvert-desktop/blob/main/testing-infrastructure/docs/step-based-test-yaml-configuration.md) directly before guessing.

---

## BTEQ script tests

BTEQ YAML uses `validation.steps[].script` with `bindings` + `files.reads/writes`, not `CALL` steps or `validate:` return lists. Common fixes:
- A read had no/empty input → correct the `files.reads[].fixture` file.
- A binding resolved wrong (schema/db mismatch) → fix the `bindings.<NAME>` value or its `source`/`target`.
- A declared output wasn't compared → ensure it's listed under `files.writes`.

Full shape: [../references/BTEQ_TEST_YAML.md](../references/BTEQ_TEST_YAML.md). After editing, re-run `scai test capture --where "id IN (...)"` then `scai test validate ...` (same as procs).
