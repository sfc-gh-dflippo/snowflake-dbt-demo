# Known false positives

The deterministic pass compares structure, so a correct conversion that restructures the work fails it. These are the patterns that recur. Each still needs citations — this file tells you what to look for, not what to conclude.

## Restructuring patterns

| Pattern | Informatica side | dbt side | Determination |
|---|---|---|---|
| Manual upsert becomes MERGE | Pre-SQL `UPDATE` followed by `INSERT` | `incremental_strategy='merge'` | `EQUIVALENT` |
| Full delete becomes truncate | `DELETE FROM <table> ALL` | `TRUNCATE TABLE {{ this }}` in a pre_hook | `EQUIVALENT` |
| Staging table eliminated | `DELETE` staging, `INSERT` staging, `INSERT` target | Direct write to target with `insert_overwrite` | `EQUIVALENT` |
| Statistics collection dropped | `CALL COLLECT_STATS_WRAP(...)` | absent | `PLATFORM_HOUSEKEEPING` — Snowflake maintains statistics itself |
| Job naming convention | `wf_FOO` | `DAG_FOO` | `EQUIVALENT` — naming convention, not logic |
| Column reference style | `TABLE.COLUMN` | `COLUMN`, resolved from a CTE | `EQUIVALENT` — same data, different reference form |
| UNION branch becomes a sibling model | One mapping with a `UNION` of N branches | N separate `.sql` models in the `_wf` directory | `EQUIVALENT` — architectural decomposition, not a dropped branch |

For the staging-elimination case, confirm the direct write actually reproduces the staging query's filters and joins. This pattern is the most common source of *genuine* loss: the restructure is legitimate, but a predicate that lived on the staging insert gets dropped along the way.

## Platform function equivalences

Record these under `aspect_comparison` with `"aspect": "platform_functions"`:

| Teradata / Informatica | Snowflake |
|---|---|
| `ZEROIFNULL(x)` | `COALESCE(x, 0)` |
| `RANDOM(lo, hi)` | `UNIFORM(lo, hi, RANDOM())` |
| `USER` | `CURRENT_USER()` |
| `SEL` | `SELECT` |
| `QUALIFY` | `QUALIFY`, or a windowed subquery with an outer filter |
| `$$VAR.TABLE` | `DB.SCHEMA.TABLE` — already resolved in `dbt_primary.sql` / `dbt_siblings.json` |
| `COLLECT STATS`, `COLLECT_STATS_WRAP` | removed; Snowflake maintains statistics itself |
| `REVENUE_AUDITS_WRAP` | `RUN_CREV_AUDITS_PROC` |

A `QUALIFY` rewritten as a subquery is equivalent only when the partition, order, and filter predicate all survive. Check all three rather than the presence of `ROW_NUMBER()`.

## Conversion-standard additions

Present in dbt, absent from Informatica, and not defects:

- `CAST` additions for Snowflake type strictness
- `COALESCE` additions for null safety
- `ROW_NUMBER` restructuring
- Audit column renaming, e.g. `EDW_CREATE_DTM` → `EDWSF_CREATE_DTM`
- Extra audit columns such as `EDWSF_BATCH_ID`, `EDWSF_SOURCE_DELETED_FLAG`
- `__THIS__` — a model's own temp table, a dbt architectural pattern

## What is not a false positive

Treat these as real until evidence says otherwise:

- A filter, predicate, join, or lookup in the XML with no counterpart in **the primary or any sibling**, including their hooks.
- An SQ Override `WHERE` predicate whose model keeps the pipeline's output label but drops the predicate — the rows change, the columns do not, and nothing in `check.json` reports it.
- An aggregation whose `GROUP BY` grain differs.
- A pipeline with no model implementing it when the XML has more pipelines than the `_wf` directory has models.
- Any section reported `SKIP`. Nothing was compared, so there is no basis for calling it equivalent.
