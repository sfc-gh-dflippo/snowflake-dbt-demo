# Enrichment prompt — null_fraction_override (value pass)

## Role
You override the fraction of NULLs generated for a column when the name/semantics justify it. Emit into `column_enrichments[].null_fraction_override`.

## Output schema (`column_enrichments[].null_fraction_override`)
```json
{ "column_enrichments": [ { "table": "<SCHEMA.TABLE>", "column": "<COL>", "null_fraction_override": 0.0, "source_evidence": "<...>" } ] }
```
`table` and `column` required; value in `[0,1]`. The column must exist and must be nullable (not a PK / NOT NULL).

## Negative constraint (the one rule)
Override only when name-confident, and **never raise the null fraction on an FK-join column or a correlated-group column** — nulls there re-create the zero-row failure. A PK / NOT NULL column, or a fraction outside `[0,1]`, is rejected (`TBD0014`).

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`SALES.ORDERS.AMOUNT` is nullable; pin its null fraction low so `BETWEEN` branches have rows:

<!-- example:accept -->
```json
{ "column_enrichments": [ { "table": "SALES.ORDERS", "column": "AMOUNT", "null_fraction_override": 0.05, "source_evidence": "PROC:process_order" } ] }
```

`SALES.CUSTOMER.CUST_ID` is a NOT NULL primary key — overriding its null fraction is rejected:

<!-- example:reject TBD0014 -->
```json
{ "column_enrichments": [ { "table": "SALES.CUSTOMER", "column": "CUST_ID", "null_fraction_override": 0.5 } ] }
```
