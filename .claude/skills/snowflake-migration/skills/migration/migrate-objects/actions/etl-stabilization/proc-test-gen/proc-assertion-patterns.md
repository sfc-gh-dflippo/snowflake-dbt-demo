# Proc assertion patterns (scripting flavor)

How to turn a source mapping + a frozen input seed into a **batched, target-only, robust** set of
functional-equivalence assertions for a converted mapping procedure. Loaded on-demand by
[proc-test-gen](SKILL.md) in Phase 3.

## Batched format

One query, one row per assertion, PASS/FAIL:

```sql
  SELECT 'assert_01_<name>:' || CASE WHEN (<boolean>) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_<name>:' || CASE WHEN (<boolean>) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL ...
```

The grade step reads the rows and treats any non-`PASS` (or a query that ERRORS) as not-yet-converged.

## Grade-hardening robustness rules (non-negotiable)

A malformed grade query is a **false non-convergence** — it makes a correct fix look wrong and burns fix
attempts. So every assertion is deliberately dumb:

1. **Target-only.** Reference **only** `<test_schema>.<TARGET>`. Never a source, lookup, or staging table —
   the expected values were already computed by hand from the source; the query just checks the target holds
   them.
2. **One simple boolean per assertion.** Allowed shapes only:
   - a `COUNT(*)` comparison: `(SELECT COUNT(*) FROM <TARGET>) = <n>`
   - a scalar for one group/row: `(SELECT <col> FROM <TARGET> WHERE <key> = <lit>) = <expected>`
   - a flat absence check: `NOT EXISTS (SELECT 1 FROM <TARGET> WHERE <condition>)`
3. **No nested or correlated subqueries, no JOINs, no window functions.** If you're tempted to join back to a
   source to "prove" a value, stop — compute the literal by hand and compare to it.
4. **Literals, not derivations.** Expected values are constants you computed from the seed (e.g. `350`, `'EAST'`),
   embedded directly in the assertion.
5. **A simple assertion that runs beats a clever one that errors.** When in doubt, split one clever assertion
   into two dumb ones.

### Regenerate-on-erroring-grade

If the assert query ERRORS (bad column, over-clever expression, type mismatch) rather than returning FAIL, that
is a **test bug**, not a proc bug. Simplify the offending assertion to a flat target-only form and re-run — up
to 2 regenerations — before recording any proc failure.

## What to assert, always

- **Exact expected row count** of the target: `(SELECT COUNT(*) FROM <TARGET>) = <n>`.
- **Each expected group/row's value(s)** via a scalar-for-one-group check.
- **Dropped rows are absent** via a flat `NOT EXISTS`.

## Per-transform recipes (compute expected by hand, assert target-only)

| Transform | Source semantics → expected target | Assert (target-only) |
|-----------|-----------------------------------|----------------------|
| **Filter** | rows whose predicate is not TRUE (incl. NULL) are dropped | row count = kept-count; `NOT EXISTS (… WHERE <dropped condition>)` |
| **Aggregator** | `GROUP BY` group ports + stated aggregates (SUM/AVG/COUNT/MIN/MAX) | one scalar per group: `(SELECT total FROM t WHERE region='EAST') = 350`; row count = #groups |
| **Lookup** | matched key → looked-up value; no-match → NULL | scalar per matched key = looked-up literal; `(SELECT COUNT(*) FROM t WHERE lkp_col IS NULL) = <no-match count>` |
| **Joiner** | inner = matched pairs; outer keeps unmatched side | row count = expected join cardinality; scalar checks on joined columns |
| **Rank** | top/bottom N per rank port, partitioned by group ports | `(SELECT rank FROM t WHERE region='EAST') = 1`; row count = N×#partitions |
| **Union** | concatenation of inputs (no dedup unless stated) | row count = sum of inputs; `NOT EXISTS` for anything not from an input |
| **Router** | rows split to groups by group filter conditions | per-branch count; `NOT EXISTS` for mis-routed rows |
| **Update Strategy** | DD_INSERT/UPDATE/DELETE/REJECT drive target ops | final target count after ops; scalar checks on updated values; `NOT EXISTS` for rejected/deleted keys |
| **Expression** | port expressions applied in dependency order | scalar check of the computed output column against the hand-computed literal |

See `{PLATFORM_DIR}/element-types.md` for each transform's active/passive classification and row-count
behavior, and `{PLATFORM_DIR}/{transformation_guide}` (Informatica: `mapping-guide.md`) for reading the
transform's ports/expressions/join type out of the source XML. The cache-mode and Aggregator-mode nuances
below are drawn from those files — read them when a transform's mode isn't obvious from the mapping.

## Worked examples per transform

Each example gives a **tiny frozen seed**, the **expected target computed by hand** from the source rule,
and the **target-only** assertion lines. `SCH` stands for `<test_schema>`. Compute the literals from the
seed; never join back to a source. These are single-transform illustrations; real procs chain several (see
the chained example at the end).

### Expression (passive, 1:1 — NULL propagates)

`ORDER_TOTALS(id, total)` from `total = qty * price`. Seed `ORDERS`: `(1, qty=3, price=10.00)`,
`(2, qty=0, price=5.50)`, `(3, qty=NULL, price=5.00)`. Informatica expression NULL propagation: a NULL
operand yields NULL. Expected: `1→30.00`, `2→0.00`, `3→NULL`; 3 rows.

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.ORDER_TOTALS) = 3) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_id1_total:' || CASE WHEN ((SELECT total FROM SCH.ORDER_TOTALS WHERE id = 1) = 30.00) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_id2_total:' || CASE WHEN ((SELECT total FROM SCH.ORDER_TOTALS WHERE id = 2) = 0.00)  THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_id3_null:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.ORDER_TOTALS WHERE total IS NULL) = 1) THEN 'PASS' ELSE 'FAIL' END
```

### Filter (active — drops non-TRUE, incl. NULL)

`BIG_ORDERS(id, amount)` from `Filter: amount > 100`. Seed: `A=150`, `B=100`, `C=NULL`, `D=200`.
`100` is not `> 100` (FALSE → dropped); NULL predicate → dropped. Expected: `A`, `D`; 2 rows.

```sql
  SELECT 'assert_01_rowcount:' || CASE WHEN ((SELECT COUNT(*) FROM SCH.BIG_ORDERS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_no_boundary:' || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.BIG_ORDERS WHERE amount = 100)) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_no_null:'     || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.BIG_ORDERS WHERE amount IS NULL)) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_kept_min:'    || CASE WHEN ((SELECT MIN(amount) FROM SCH.BIG_ORDERS) = 150) THEN 'PASS' ELSE 'FAIL' END
```

### Router (active — split by group condition; unmatched → DEFAULT1, NOT dropped)

Router groups `HIGH: amt >= 100`, `LOW: amt < 100`, `DEFAULT1`. Target `HIGH_TXNS` is bound to the HIGH
group. Seed: `100`, `250`, `50`, `NULL`. HIGH → `100`,`250` (2 rows); `50` → LOW; `NULL` → DEFAULT1.
The difference from Filter: unmatched rows are routed elsewhere, not dropped — but a target bound to one
group holds only that group's rows. Expected `HIGH_TXNS`: 2 rows.

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.HIGH_TXNS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_no_low:'   || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.HIGH_TXNS WHERE amt < 100)) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_no_null:'  || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.HIGH_TXNS WHERE amt IS NULL)) THEN 'PASS' ELSE 'FAIL' END
```

> If the proc materializes several router groups into several targets, generate one assertion query per
> target table — never a cross-target JOIN.

### Lookup (connected, static cache — no-match → NULL; multiple-match → first value)

`EMP_ENRICHED(emp, dept_name)` from a Lookup on `DEPT(dept_id → dept_name)`. Seed input `EMP`:
`(1, dept_id=10)`, `(2, dept_id=20)`, `(3, dept_id=99)`. The **reference** `DEPT` (documented for the
hand-computation, NEVER queried by the assertion): `10→'SALES'`, `20→'ENG'`, `99` absent. Expected:
`1→'SALES'`, `2→'ENG'`, `3→NULL`; 3 rows.

```sql
  SELECT 'assert_01_rowcount:'   || CASE WHEN ((SELECT COUNT(*) FROM SCH.EMP_ENRICHED) = 3) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_emp1_dept:' || CASE WHEN ((SELECT dept_name FROM SCH.EMP_ENRICHED WHERE emp = 1) = 'SALES') THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_emp2_dept:' || CASE WHEN ((SELECT dept_name FROM SCH.EMP_ENRICHED WHERE emp = 2) = 'ENG')   THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_nomatch_null:' || CASE WHEN ((SELECT COUNT(*) FROM SCH.EMP_ENRICHED WHERE dept_name IS NULL) = 1) THEN 'PASS' ELSE 'FAIL' END
```

The looked-up literals (`'SALES'`, `'ENG'`) come from *your* reading of the reference data, embedded as
constants — the assertion touches only `EMP_ENRICHED`.

### Joiner (Normal = inner; Master/Detail/Full Outer keep the named side)

`CUST_ORDERS(order_id, cust_name)` from a **Normal** Joiner of `CUSTOMERS(id, name)` and `ORDERS(order_id,
cust)` on `id = cust`. Seed customers `(1,'Ann')`,`(2,'Bob')`; orders `(o1,cust=1)`,`(o2,cust=1)`,
`(o3,cust=3)`. Inner join: `o1`,`o2` match `Ann`; `o3` unmatched → dropped; `Bob` orderless → dropped.
Expected: 2 rows, both `cust_name='Ann'`.

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.CUST_ORDERS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_all_ann:' || CASE WHEN ((SELECT COUNT(*) FROM SCH.CUST_ORDERS WHERE cust_name = 'Ann') = 2) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_no_o3:'   || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.CUST_ORDERS WHERE order_id = 'o3')) THEN 'PASS' ELSE 'FAIL' END
```

> Join type changes the expected cardinality: **Master Outer** keeps all detail rows (unmatched masters →
> NULL master cols), **Detail Outer** keeps all master rows, **Full Outer** keeps both. Recompute the row
> count and the NULL-side scalar checks for the actual type read from the mapping.

### Aggregator (set-based — GROUP BY + aggregates)

`DEPT_STATS(dept, avg_sal, cnt)` from `GROUP BY dept; AVG(salary), COUNT(*)`. Seed `EMP`: dept `A` →
`100,200`; dept `B` → `300`. Expected: `A: avg=150, cnt=2`; `B: avg=300, cnt=1`; 2 rows.

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.DEPT_STATS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_a_avg:' || CASE WHEN ((SELECT avg_sal FROM SCH.DEPT_STATS WHERE dept = 'A') = 150) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_a_cnt:' || CASE WHEN ((SELECT cnt     FROM SCH.DEPT_STATS WHERE dept = 'A') = 2)   THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_b_avg:' || CASE WHEN ((SELECT avg_sal FROM SCH.DEPT_STATS WHERE dept = 'B') = 300) THEN 'PASS' ELSE 'FAIL' END
```

> Sorted-Input/incremental mode (element-types.md) can carry non-aggregate passthrough columns via
> `LAST_VALUE`; assert only the aggregates + the deterministic group keys, not an order-dependent
> passthrough value.

### Rank (set-based — top/bottom N per partition)

`TOP_SALES(region, amount)` from `Rank: top 1 by amount, partition by region`. Seed `EAST`: `50,90`;
`WEST`: `70`. Expected: `EAST→90`, `WEST→70`; row count = N × #partitions = `1 × 2 = 2`.

```sql
  SELECT 'assert_01_rowcount:'   || CASE WHEN ((SELECT COUNT(*) FROM SCH.TOP_SALES) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_east_top:' || CASE WHEN ((SELECT amount FROM SCH.TOP_SALES WHERE region = 'EAST') = 90) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_west_top:' || CASE WHEN ((SELECT amount FROM SCH.TOP_SALES WHERE region = 'WEST') = 70) THEN 'PASS' ELSE 'FAIL' END
```

> Seed the rank port with **distinct** values within each partition so no tie inflates the row count;
> ties keep multiple rows depending on the Rank setting. Keep the example tie-free to keep the assertion dumb.

### Union (set-based — UNION ALL, keeps duplicates)

`ALL_IDS(id)` from a Union of inputs `A` and `B`. Seed `A`: `1,2`; `B`: `2,3`. Union ALL concatenates
without dedup, so `2` appears twice. Expected: 4 rows; `id=2` twice.

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.ALL_IDS) = 4) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_dup_2:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.ALL_IDS WHERE id = 2) = 2) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_no_4:'   || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.ALL_IDS WHERE id = 4)) THEN 'PASS' ELSE 'FAIL' END
```

> The duplicate-count assertion is what distinguishes UNION ALL from UNION — assert it explicitly.

### Update Strategy (DD_INSERT / DD_UPDATE / DD_DELETE / DD_REJECT drive target ops)

`ACCOUNTS(key, val)` **pre-seeded** (ARRANGE:SETUP) with `k1→10`, `k2→20`. Source drives ops via a DD
expression: `(k1,'U',15)`, `(k2,'D')`, `(k3,'I',30)`, `(k4,'R')`. Expected final target: `k1` updated to
`15`, `k2` deleted, `k3` inserted `30`, `k4` rejected (never inserted). Final: `k1=15`, `k3=30`; 2 rows.

```sql
  SELECT 'assert_01_rowcount:' || CASE WHEN ((SELECT COUNT(*) FROM SCH.ACCOUNTS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_k1_updated:' || CASE WHEN ((SELECT val FROM SCH.ACCOUNTS WHERE key = 'k1') = 15) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_k2_deleted:' || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.ACCOUNTS WHERE key = 'k2')) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_k3_inserted:' || CASE WHEN ((SELECT val FROM SCH.ACCOUNTS WHERE key = 'k3') = 30) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_05_k4_rejected:' || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.ACCOUNTS WHERE key = 'k4')) THEN 'PASS' ELSE 'FAIL' END
```

> Update Strategy is the one transform whose ARRANGE:SETUP must seed the **target's** prior state (for the
> update/delete keys), not just the source — otherwise DD_UPDATE/DD_DELETE have nothing to act on.

### Sequence (non-deterministic ordering — assert only stable properties)

A Sequence Generator populates a surrogate key. Its row→value assignment is **non-deterministic** in SQL
(FDM `SSC-FDM-INF0016`), so never assert a specific `id → seq` mapping. Assert only order-independent
facts: the count of distinct sequence values equals the row count (uniqueness), and the value range.

```sql
  SELECT 'assert_01_unique:' || CASE WHEN ((SELECT COUNT(DISTINCT seq) FROM SCH.WITH_KEYS) = (SELECT COUNT(*) FROM SCH.WITH_KEYS)) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_range:' || CASE WHEN ((SELECT MIN(seq) FROM SCH.WITH_KEYS) >= 1) THEN 'PASS' ELSE 'FAIL' END
```

## Chained example (Lookup → Filter → Aggregator)

Seed produces, by source semantics, target `REGION_TOTALS(region, total, cnt)` = `EAST: 350/3`, `WEST: 325/2`
(rows failing the filter dropped, no-match lookups excluded from the aggregate):

```sql
  SELECT 'assert_01_rowcount:'  || CASE WHEN ((SELECT COUNT(*) FROM SCH.REGION_TOTALS) = 2) THEN 'PASS' ELSE 'FAIL' END AS r
  UNION ALL SELECT 'assert_02_east_total:' || CASE WHEN ((SELECT total FROM SCH.REGION_TOTALS WHERE region = 'EAST') = 350) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_03_east_cnt:'   || CASE WHEN ((SELECT cnt   FROM SCH.REGION_TOTALS WHERE region = 'EAST') = 3)   THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_04_west_total:' || CASE WHEN ((SELECT total FROM SCH.REGION_TOTALS WHERE region = 'WEST') = 325) THEN 'PASS' ELSE 'FAIL' END
  UNION ALL SELECT 'assert_05_no_south:'   || CASE WHEN (NOT EXISTS (SELECT 1 FROM SCH.REGION_TOTALS WHERE region = 'SOUTH')) THEN 'PASS' ELSE 'FAIL' END
```

Every assertion touches only `SCH.REGION_TOTALS`; the "SOUTH dropped by filter" case is a flat `NOT EXISTS`;
no join back to the source or lookup table.
