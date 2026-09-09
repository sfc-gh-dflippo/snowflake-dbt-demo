# Enrichment prompt — branch_values (value pass)

## Role
You supply the concrete values that fire a branch arm, keyed to the **resolved source column** the miner bound the predicate to (via var-flow `(table, type)`). Input: `list-unsolved` `branch_predicate` rows with their resolved `(table, column)`. Never reason about the opaque local (`v_amt`); reason about the column it resolved to (`SALES.ORDERS.AMOUNT`).

## Output schema (`branch_values[]`)
```json
{ "branch_values": [ { "table": "<SCHEMA.TABLE>", "column": "<COL>", "inferred_enum": ["<v>"], "must_include": ["<v>"], "source_evidence": "<PROC:...>" } ] }
```
`table` and `column` are required. Provide `inferred_enum` (a value domain) and/or `must_include` (values that must appear). The column must exist.

## Negative constraint (the one rule)
Reason about the **resolved source column**, never the opaque local, and stay consistent with any `correlated_groups` tuples that touch the same column — do not emit a raw-SQL guess or a value the correlated tuple contradicts.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`PROCESS_ORDER` filters `AMOUNT BETWEEN 100 AND 500` — force the boundary values to exist on the resolved column `SALES.ORDERS.AMOUNT`:

<!-- example:accept -->
```json
{ "branch_values": [ { "table": "SALES.ORDERS", "column": "AMOUNT", "must_include": ["100", "500"], "source_evidence": "PROC:process_order predicates[1]" } ] }
```

Guessing at a local that resolves to no real column is rejected:

<!-- example:reject TBD0014 -->
```json
{ "branch_values": [ { "table": "SALES.ORDERS", "column": "V_AMT", "must_include": ["100"] } ] }
```
