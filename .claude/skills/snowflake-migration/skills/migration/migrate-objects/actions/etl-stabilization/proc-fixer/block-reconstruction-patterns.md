# Block reconstruction patterns (scripting flavor)

How to turn a **source transformation node** + a **broken block stub** into a reconstructed block that compiles
and is functionally faithful to the source. Loaded on-demand by [proc-fixer](SKILL.md) in Step 2.

A defective block is a materialized transformation whose body SnowConvert could not translate. It looks like a
CTE (or temp-table) that returns `null` placeholders, preceded by a `!!!RESOLVE EWI!!!` marker and the source
`<TRANSFORMATION>` / `<CONNECTOR>` XML as comments:

```sql
      !!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - ... TRANSFORMATION IS NOT SUPPORTED ... ***/!!!
      cte_lkp_customer AS
      (
         -- <TRANSFORMATION NAME="LKP_Customer" TYPE="Lookup Procedure" ...>  (source XML, as comments)
         SELECT null AS region, null AS tier, null AS SQ_EVENTS__amount
      ),
```

Reconstruct the CTE body from the source node; keep its name, its output columns, and its place in the chain.

## Minimal-change / semantic-preservation rules (non-negotiable)

1. **Author from source, never from the placeholders.** The `null AS <col>` lines only tell you the output
   column names — never the values. Recover the logic from the source node (the embedded XML + `source.xml`).
2. **Preserve the output contract.** Same CTE/temp name, same output column names and order, same feeding
   relationship to the next block. The final `SELECT`/`INSERT` column list must be unchanged.
3. **Minimal change.** Touch only the defective block. Leave the surrounding statement, other blocks, casing,
   and formatting alone. Keep sensible names.
4. **Never mock or hardcode.** No constant result rows, no literal expected values, no commenting-out. If you
   cannot reconstruct a transform from source, revert and escalate — a fabricated fix that passes is worse than
   an honest gap.
5. **Remove `!!!RESOLVE EWI!!!` lines; keep `--** SSC-*` one-line comments.** Replace the whole stub body
   (marker + commented source XML) with working SQL; do not leave dead commented code behind.
6. **Preserve transformation order.** Reconstruct each block in place; a downstream block reads the upstream
   block's output, so order is load-bearing (lookup → filter → aggregate is not the same as any other order).

## Reading the source node

From the embedded XML / `source.xml` (see `{PLATFORM_DIR}/{transformation_guide}`, Informatica
`mapping-guide.md`), recover:
- **TYPE** of the transformation (Lookup Procedure / Filter / Aggregator / Joiner / Router / Rank / Union /
  Expression / Update Strategy).
- **TRANSFORMFIELD** ports: input vs output, `EXPRESSION`, `EXPRESSIONTYPE` (`GROUPBY` marks group keys).
- **TABLEATTRIBUTE**: the `Filter Condition`, `Lookup condition` + `Lookup table name`, `Update Strategy
  Expression`, `Sorted Input`, cache mode, `Lookup policy on multiple match`.
- **CONNECTOR** wiring: which upstream port feeds which input port (tells you the join/feed columns).

## Per-transform reconstruction recipes

| Source TYPE | Reconstruct the block as | Load-bearing detail |
|-------------|--------------------------|---------------------|
| **Lookup Procedure** (connected) | `LEFT OUTER JOIN` from the incoming rows to `{SCHEMA}.<Lookup table name>` on the `Lookup condition`, selecting the LOOKUP/OUTPUT ports | no-match → NULL outputs; **do not** use INNER JOIN; no fan-out if the key is unique |
| **Filter** | `SELECT … FROM <upstream> WHERE <Filter Condition>` | NULL predicate drops the row — **never** add `OR <col> IS NULL` |
| **Aggregator** | `SELECT <group ports>, <aggregates> FROM <upstream> GROUP BY <group ports>` | group ports = `EXPRESSIONTYPE="GROUPBY"`; aggregates from the OUTPUT port expressions (`SUM`/`COUNT`/…) |
| **Joiner** | join the two upstream CTEs on the join condition, per the join type | Normal = INNER; Master/Detail/Full Outer keep the named side (unmatched → NULL) |
| **Router** | one block/branch per group condition (`WHERE`), unmatched → the `DEFAULT1` group | a Router feeds several targets; reconstruct only the branch this block represents |
| **Rank** | window function + `QUALIFY ROW_NUMBER()/RANK() OVER (PARTITION BY <group> ORDER BY <rank port>) <= N` | partition by the group ports; top vs bottom from the rank direction |
| **Union** | `UNION ALL` of the upstream inputs | no dedup unless the source states DISTINCT |
| **Expression** | `SELECT <port expressions> …` applied in dependency order | translate `IIF`→`IFF`, `DECODE`→`CASE`; preserve declared output types |
| **Update Strategy** | the DD_ operation(s) against the target (`INSERT`/`UPDATE`/`DELETE`), driven by the DD expression | seed the prior target state (proc-test-gen handles ARRANGE); reconstruct the DML, not a SELECT |

## Worked example: a Lookup → Filter → Aggregator chain

Three chained defective blocks. The source: `EVENTS --SQ--> LKP_Customer(DimCustomer) --> FIL(tier != 'STANDARD')
--> AGG(GROUP BY region)`. This chain is a good teaching case because the filter tests the **looked-up** column
`tier`, so lookup semantics and order are load-bearing.

**Block 1 — Lookup (`cte_lkp_customer`).** Source: `Lookup table name = DimCustomer`,
`Lookup condition = customer_id = customer_id1`, LOOKUP/OUTPUT ports `region`, `tier`.

```sql
cte_lkp_customer AS
(
   SELECT
      dc.region              AS region,
      dc.tier                AS tier,
      sq.amount              AS SQ_EVENTS__amount
   FROM
      {SCHEMA}.EVENTS AS sq
      LEFT OUTER JOIN {SCHEMA}.DimCustomer AS dc
         ON dc.customer_id = sq.customer_id      -- no-match ⇒ region/tier NULL
)
```

**Block 2 — Filter (`cte_fil_notstandard`).** Source: `Filter Condition = tier != 'STANDARD'`.

```sql
cte_fil_notstandard AS
(
   SELECT region, tier, SQ_EVENTS__amount AS amount
   FROM   cte_lkp_customer
   WHERE  tier != 'STANDARD'          -- a no-match row has tier NULL ⇒ NULL != 'STANDARD' is NULL ⇒ dropped
)
```

**Block 3 — Aggregator (`cte_agg_byregion`).** Source: `GROUPBY region`; `total_amount = SUM(amount)`,
`event_count = COUNT(amount)`.

```sql
cte_agg_byregion AS
(
   SELECT region, SUM(amount) AS total_amount, COUNT(amount) AS event_count
   FROM   cte_fil_notstandard
   GROUP BY region
)
```

The final `SELECT`/`INSERT` shape (`region, total_amount, event_count`) is preserved from the broken proc.

**Why the traps matter (what a careless fix gets wrong):**
- `LEFT OUTER JOIN`, not `INNER` — but the no-match row is then correctly dropped **by the filter**, not by the
  join. Using INNER would drop it for the wrong reason and mask the semantics.
- `WHERE tier != 'STANDARD'` — **not** `... OR tier IS NULL`. The "helpful" NULL-keeping variant wrongly keeps
  the unmatched row and invents a spurious NULL-region group.
- Filter **before** aggregate. Aggregating first would fold the dropped amounts into the totals and add a
  NULL-region group — wrong sums and an extra row.

## Using grader feedback to target the next fix

When Step 4 reports failing assertions, map the symptom back to the responsible block before re-reconstructing:

| Failing assertion symptom | Likely block / cause | Correction |
|---------------------------|----------------------|------------|
| Row count too high; an unexpected NULL-key group present | Filter (kept NULLs) or Lookup (INNER vs LEFT then bad filter) or aggregate-before-filter | restore `WHERE` NULL-drop; keep lookup→filter→aggregate order |
| Row count too low; an expected group missing | Filter too strict, or Lookup INNER dropping matched rows, or wrong join type | widen the predicate to the source condition; use LEFT OUTER for a connected lookup |
| A group's aggregate value wrong | Aggregator (wrong agg, wrong group key) or upstream filter leaking/eating rows | re-derive the aggregate + group ports from the source OUTPUT/GROUPBY ports |
| A looked-up column is NULL when it should have a value (or vice-versa) | Lookup join condition / port mapping | fix the `ON` to the source `Lookup condition`; map the correct LOOKUP/OUTPUT port |
| Deploy/CALL error (not a FAIL) | a structural/dialect error in a block | read `errorText`, `stabilization_tools.py task-error-locate` the block, fix the SQL (e.g. `IIF`→`IFF`) |

Feed the specific failing assertions into the reconstruction; change only what the feedback implicates, keeping
every other block intact.
