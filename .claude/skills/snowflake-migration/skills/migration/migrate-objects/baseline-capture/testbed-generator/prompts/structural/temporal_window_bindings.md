# Enrichment prompt — temporal_window_bindings (structural pass)

## Role
You bind a **child table's date column into a matched SCD parent version's `[from, to]` window** so a proc's SCD-2 lookup resolves to rows. Input: `list-unsolved` cross-table temporal predicates spanning a child and its slowly-changing parent, plus the `join_edge` (FK) that links them. Never raw SQL. Every table, column, and filter is stated explicitly — no name heuristics.

## Output schema (`temporal_window_bindings[]`)
```json
{ "temporal_window_bindings": [ { "binding_id": "<id>", "child_table": "<SCHEMA.TABLE>", "child_date_column": "<COL>", "parent_table": "<SCHEMA.TABLE>", "parent_from_column": "<COL>", "parent_to_column": "<COL>", "child_key_columns": ["<COL>"], "parent_key_columns": ["<COL>"], "parent_filters": [ { "column": "<COL>", "value": "<v>" } ] } ] }
```
All fields required except `parent_filters` (optional). `child_date_column`, `parent_from_column`, and `parent_to_column` must each be a **date/timestamp or integer** column. `child_key_columns` and `parent_key_columns` must have **equal arity (>= 1)** — they carry the business-key correspondence. `parent_filters` pins the exact parent version the child clamps into: each version's `column` must equal `value` (so the clamped-into row is the same version that carries the proc's literals).

## Negative constraints
- A **child->parent foreign key edge must exist** (declared or `fk_chains`-inferred). It guarantees the parent is generated before the child (its windows indexed first) and supplies the key link. A binding to a parent with no FK edge is rejected (`TBD0014`).
- The date and window columns **must not** participate in a `UNIQUE`/`PRIMARY KEY` constraint — the clamp runs after uniqueness repair, so mutating a key column would silently break the repair.
- `child_date_column`, `parent_from_column`, `parent_to_column` must all be date/int; a string/other-typed column is rejected.
- `child_key_columns` and `parent_key_columns` must have equal arity and every column (keys and filters) must resolve on its own table.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`ORDERS.ORDER_DT` clamps into the matching `CUSTOMER` SCD version's `[EFFECTIVE_DT, EXPIRY_DT]` window, keyed by `CUST_ID` (ORDERS has an FK to CUSTOMER), on the active (`STATUS='A'`) version:

<!-- example:accept -->
```json
{ "temporal_window_bindings": [ { "binding_id": "twb_orders_into_customer_scd", "child_table": "SALES.ORDERS", "child_date_column": "ORDER_DT", "parent_table": "SALES.CUSTOMER", "parent_from_column": "EFFECTIVE_DT", "parent_to_column": "EXPIRY_DT", "child_key_columns": ["CUST_ID"], "parent_key_columns": ["CUST_ID"], "parent_filters": [ { "column": "STATUS", "value": "A" } ] } ] }
```

`SHIPMENT` has no foreign key edge to `CUSTOMER`, so the parent-before-child ordering and key link can't be guaranteed — rejected:

<!-- example:reject TBD0014 -->
```json
{ "temporal_window_bindings": [ { "binding_id": "twb_shipment_no_fk", "child_table": "SALES.SHIPMENT", "child_date_column": "SHIP_TS", "parent_table": "SALES.CUSTOMER", "parent_from_column": "EFFECTIVE_DT", "parent_to_column": "EXPIRY_DT", "child_key_columns": ["ORDER_ID"], "parent_key_columns": ["CUST_ID"], "parent_filters": [ { "column": "STATUS", "value": "A" } ] } ] }
```
