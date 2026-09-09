# Enrichment prompt — inferred_enum (value pass)

## Role
You infer the value domain of a column that has **no declared domain**. Input: `list-unsolved` `enum_domain` rows. Emit into `column_enrichments[].inferred_enum`.

## Output schema (`column_enrichments[].inferred_enum`)
```json
{ "column_enrichments": [ { "table": "<SCHEMA.TABLE>", "column": "<COL>", "inferred_enum": ["<v>"], "source_evidence": "<...>" } ] }
```
`table` and `column` required; the column must exist.

## Negative constraint (the one rule)
**Undeclared-domain columns only.** Never re-classify a column that already has a declared enum (the applier skips it — "declared enum wins" — so it is wasted output). Never coerce a value to fit (`'ACTIVE'` → `'A'`): emit values in the column's own representation, or the applier drops the incompatible value.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`SALES.CUSTOMER.TIER` is `CHAR(1)` with no declared domain — a real inferred-enum target:

<!-- example:accept -->
```json
{ "column_enrichments": [ { "table": "SALES.CUSTOMER", "column": "TIER", "inferred_enum": ["G", "S", "B"], "source_evidence": "columns[3]" } ] }
```

A non-existent column is rejected (a declared-enum column like `STATUS` would instead be silently skipped — don't emit it either):

<!-- example:reject TBD0014 -->
```json
{ "column_enrichments": [ { "table": "SALES.CUSTOMER", "column": "NOPE", "inferred_enum": ["X"] } ] }
```
