# Enrichment prompt — temporal_alignment (structural pass)

## Role
You declare that one date column must precede another on the same table. Input: the mined date columns per table. Never raw SQL. The engine does the actual date arithmetic — you only declare the pair and (optionally) a minimum span.

## Output schema (`temporal_alignment[]`)
```json
{ "temporal_alignment": [ { "table": "<SCHEMA.TABLE>", "column_deb": "<START_COL>", "column_fin": "<END_COL>", "must_span": null } ] }
```
`table`, `column_deb`, `column_fin` are required (`deb`/`fin` = début/fin = start/end). `must_span` is an optional ISO date string. Both columns must exist, be date/timestamp, and differ.

## Negative constraint (the one rule)
Declare the ordered **pair + direction only**; both columns must be real date/timestamp columns and must differ. Do **not** pair a column with itself, and do **not** include point-in-time period columns (a first-of-month partition key or a `*_MOIS` code) — only genuine start→end lifecycles. A self-pair or a non-date column is rejected (`TBD0014`).

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`SALES.CUSTOMER.EFFECTIVE_DT` must precede `EXPIRY_DT` (`CREATED_DT` is a point-in-time foil, not part of the pair):

<!-- example:accept -->
```json
{ "temporal_alignment": [ { "table": "SALES.CUSTOMER", "column_deb": "EFFECTIVE_DT", "column_fin": "EXPIRY_DT", "must_span": null } ] }
```

Pairing a column with itself is meaningless and rejected:

<!-- example:reject TBD0014 -->
```json
{ "temporal_alignment": [ { "table": "SALES.CUSTOMER", "column_deb": "EFFECTIVE_DT", "column_fin": "EFFECTIVE_DT", "must_span": null } ] }
```
