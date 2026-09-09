# Enrichment prompt — must_include (value pass)

## Role
You declare a **floor** of values that must appear in a column (e.g. lookup values a `check` or a downstream join depends on). Input: `list-unsolved` `check` rows and lookup columns. Emit into `column_enrichments[].must_include`.

## Output schema (`column_enrichments[].must_include`)
```json
{ "column_enrichments": [ { "table": "<SCHEMA.TABLE>", "column": "<COL>", "must_include": ["<v>"], "source_evidence": "<...>" } ] }
```
`table` and `column` required; the column must exist.

## Negative constraint (the one rule)
A **floor** (at least these values exist), not a full-domain model. The values must satisfy any `check` on the column — but note the `check` contradiction is **not** caught by `propose-enrichments`; it surfaces later at `validate` (the readiness gate), which fails the whole state. So a `must_include` that violates a `check` is accepted here yet blocks `validate` — get it right at authoring time.

## What `generate` does with a pinned value
Each pinned value takes one row of the column, so `n` values need at least `n` rows. Values are emitted in the column's canonical form: a **date/timestamp column carries no time-of-day**, so `"2026-06-14 00:00:00"` is emitted as `2026-06-14` — pin the date you want to see in the CSV. A `BINARY` column loads hexadecimal, so pin an even-length run of hex digits; a `DECIMAL(p,s)` value is rounded to `s` decimals, and is rejected outright if rounding carries it past `p` digits.

`generate` warns, naming the column and the value, whenever a pin does not reach the data — wider than the column, outside its domain, not loadable in the column's kind, rounding out of the declared precision, or no row left to carry it. A pin on a **foreign-key column** is reported separately as *not pinned*: those values come from the parent key, so the pin is ignored and the value appears only if the parent supplies it. Either way a pin never disappears in silence.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`SALES.ORDER_LINE.SKU` is a `VARCHAR(40)` lookup column — force the SKUs a branch depends on to exist:

<!-- example:accept -->
```json
{ "column_enrichments": [ { "table": "SALES.ORDER_LINE", "column": "SKU", "must_include": ["ABC-1", "XYZ-9"], "source_evidence": "PROC:process_order predicates[4]" } ] }
```

A non-existent column is rejected:

<!-- example:reject TBD0014 -->
```json
{ "column_enrichments": [ { "table": "SALES.ORDER_LINE", "column": "NOPE", "must_include": ["ABC-1"] } ] }
```
