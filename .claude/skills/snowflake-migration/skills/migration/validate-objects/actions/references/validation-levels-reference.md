# Validation levels — what each category means

Use this when the user asks what schema, metrics, row, or execution validation means, or when you offer an explanation at setup (Step 2) or after a failure report (Step 5).

## Setup toggles (`validation_configuration`)

These control **which checks run** for every table in the workflow YAML.

| Level | YAML field | scai default | What it checks |
|-------|------------|--------------|----------------|
| **Schema** | `schema_validation` | on (`true`) | Column **definitions** on source vs Snowflake: names, types, nullability, order. Does **not** compare cell values. |
| **Metrics** | `metrics_validation` | off (`false`) | **Aggregate statistics** per column (e.g. min, max, count, avg) on source vs Snowflake. Opt-in — enable only when the user wants this extra check. |
| **Row** | `row_validation` | on (`true`) | **Row-by-row** value comparison on matched keys. Expensive at scale; requires `indexColumnList` (and `targetIndexColumnList` when names differ) per table. Snake_case `index_column_list` / `target_index_column_list` still accepted in YAML. |

Do **not** prompt the user to enable metrics unless they ask for aggregate-statistics comparison.

**Full vs metrics:** Choosing **Full** validation (entire table, not incremental) does **not** enable metrics. Metrics stays **off** unless the user explicitly asks for L2 / aggregate statistics. Do not rewrite `metricsValidation: false` → `true` just to "run all levels."

## Report categories (`### Errors` in Step 5)

These describe **what failed** after a run. Order is always: **Schema → Metrics → Row → Execution**.

| Category | When it appears | What it means |
|----------|-----------------|---------------|
| **Schema** | `schema_validation` was on and schema check failed | Structure mismatch — fix DDL, type mappings, or renamed columns in the workflow YAML before re-running. |
| **Metrics** | `metrics_validation` was on and metrics check failed | Aggregate stats differ — investigate distribution shifts, filters, or partial loads. **Omit this section entirely when metrics was off.** |
| **Row** | `row_validation` was on and row check failed | Specific cell values differ — use `row_validation_results` / `cell_validation_results` for details; may need re-migration or mapping fixes. |
| **Execution** | Job or table could not complete the workflow | **Infrastructure or runtime** — worker, connectivity, permissions, orchestrator. Not a data mismatch category. |

## Status fields (`tableStates`)

| Field | `true` | `null` | `false` |
|-------|--------|--------|---------|
| `schemaValidated` | Passed | Not run / N/A | Failed (when schema was enabled) |
| `metricsValidated` | Passed | **Not run** (typical when metrics off) | Failed (only when metrics was enabled) |
| `rowsValidated` | Passed | Not run / N/A | Failed (when row validation was enabled) |

Do **not** treat `metricsValidated: null` as a metrics failure when `metrics_validation` is false in the workflow.

## Short gloss (one line under a category header)

Use when the category appears in a failure report and the user has not seen definitions yet in this conversation:

- **Schema** — column definition mismatches (types, names), not individual cell values.
- **Metrics** — aggregate statistics differ between source and Snowflake.
- **Row** — specific row/cell values differ on matched keys.
- **Execution** — connectivity, worker, or orchestrator issue — not a data comparison result.
