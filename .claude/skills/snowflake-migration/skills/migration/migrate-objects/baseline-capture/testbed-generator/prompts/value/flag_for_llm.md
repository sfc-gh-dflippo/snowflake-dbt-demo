# Enrichment prompt — flag_for_llm (value pass, skill-side router)

## Role
`flag_for_llm` is **not an enrichment type** — it is a skill-side router for residuals the miner couldn't classify. You resolve each residual into **one of the 10 supported directives** and emit *that*. The token `flag_for_llm` is **never** sent to `propose-enrichments`.

## Routing
- An undeclared value domain → `inferred_enum` (Task 8) or, if branch-scoped, a `branch_values` deferral (Task 7).
- **Generator-assignment residuals** (email / phone / zip / free-text synthesis) have **no v1 enrichment representation** — they are a generate-phase concern (Faker / `IValueGenerator`, owned elsewhere). **Drop them; never invent an enrichment for them.**

## Negative constraint (the one rule)
Never emit `flag_for_llm` on the wire. `propose-enrichments` rejects a root `flag_for_llm` key with a targeted message ("resolved Skill-side … generator-assignment residuals have no v1 enrichment representation. Resolve it into the 10 supported types"). Resolve first, then emit a supported type.

## Work it out before you emit
Reason in prose first, then emit the fragment as your final output — deciding and formatting in the same
pass is where accuracy is lost. Per candidate, name the `list-unsolved` row that backs it and why it
holds, and say what you considered and dropped. Keep that reasoning out of the fragment: it carries only
the emitted type's own fields, and unknown fields are rejected.

## Examples
`SALES.CUSTOMER.TIER` residue resolves to an `inferred_enum` (a supported type) — this is what you emit:

<!-- example:accept -->
```json
{ "column_enrichments": [ { "table": "SALES.CUSTOMER", "column": "TIER", "inferred_enum": ["G", "S", "B"] } ] }
```

Sending the raw router token is rejected — `SALES.CUSTOMER.EMAIL`/`PHONE` are generator residuals with no enrichment; they are dropped, not flagged:

<!-- example:reject TBD0014 -->
```json
{ "flag_for_llm": [ { "table": "SALES.CUSTOMER", "column": "EMAIL" } ] }
```
