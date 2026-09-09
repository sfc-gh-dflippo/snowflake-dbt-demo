# Enrichment prompt — predicate_fills (value pass)

## Role
You supply the value that makes a **parameter-gated** branch fire — a gate the deterministic miner could not solve because it compares a column to a procedure parameter, a function of one, or several parameters at once. Input: `list-unsolved` `branch_predicate` rows that carry a `branch_id` and a `parameters` list (run with `--fillable` to see only rows a fill can be keyed to). Key your answer to that `branch_id`, and bind every parameter the row names.

## Output schema (`predicate_fills[]`)
```json
{ "predicate_fills": [ { "fill_id": "<stable id you choose>", "branch_id": "<branch_id verbatim from list-unsolved>", "table": "<SCHEMA.TABLE>", "column": "<COL>", "value": "<the value that fires the gate>", "parameters": [ { "name": "@Param", "value": "<what the caller would pass>" } ], "source_evidence": "<PROC:... branches[n]>" } ] }
```
`fill_id`, `branch_id` and `table` are required. Pin **one** column per entry; a gate constraining two columns of the same table cannot be expressed and should be skipped.

`non_coverable_reason` replaces `column`/`value` and is a **last resort**, not a fallback. Use it only when no value of any column could ever satisfy the gate — a non-invertible hash of a column, for instance. It is written to durable state and stops the gate being offered again, so a wrong verdict is expensive to retract. Specifically, do **not** use it for:

- **A clock-dependent gate** (`GETDATE()`, `DATEADD(DAY, -7, GETDATE())`). These become satisfiable once the run clock is frozen. Skip the row; do not mark it.
- **An environment check or an always-true arm** (`OBJECT_ID('tempdb..#X') IS NOT NULL`, `TRUE`, a housekeeping guard around a `TRUNCATE`). These reference no table column, so they are not a data question at all — the backend hard-rejects a `non_coverable_reason` on them. Skip the row.
- **A gate you merely cannot work out.** Skipping leaves it for a later pass; marking hides it forever.

If a row carries no `table`/`column` from `list-unsolved`, skip it — this directive has nothing to offer a column-less branch in either direction.

## Negative constraint (the one rule)
The value must **satisfy the gate's own atom on the column you pin**, under the parameter bindings you supply — the backend re-evaluates it and hard-rejects a value that does not. Do not pin a key, foreign-key or unique column, and do not exceed the column's declared width or step outside its declared domain: those are rejected too.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`REFRESH_ORDERS` gates on `ORDER_STATUS = @Status`; bind the parameter and pin the matching column value:

<!-- example:accept -->
```json
{ "predicate_fills": [ { "fill_id": "refresh-orders-0-status", "branch_id": "cu-sales-refresh#0", "table": "SALES.ORDERS", "column": "ORDER_STATUS", "value": "S", "parameters": [ { "name": "@Status", "value": "S" } ], "source_evidence": "PROC:refresh_orders branches[0]" } ] }
```

A value that contradicts the atom it claims to satisfy is rejected:

<!-- example:reject TBD0014 -->
```json
{ "predicate_fills": [ { "fill_id": "bad", "branch_id": "cu-sales-refresh#0", "table": "SALES.ORDERS", "column": "ORDER_STATUS", "value": "C", "parameters": [ { "name": "@Status", "value": "S" } ] } ] }
```
