# AI-First platform tables

One `platform_<name>.json` per source platform. Consumed by identify/emit and Gate A.

## Entry contract

Use the checked-in table path whenever one exists:

`aifirst-migrate.sh <platform-table.json> <source-document> <output-root>`

When the caller has a platform identity rather than a table path:

`aifirst-migrate.sh --platform <platform-identity> <source-document> <output-root>`

`<platform-identity>` is the exact value of the table's top-level `platform` field. Stage 0 prefers
the matching checked-in table. If none exists, it authors a provisional table from the source
document, `AUTHORING_CONTRACT.md`, and non-target prior-art tables, and accepts it only when
`identify.validate_table` succeeds and Identification accounting over the source has no loss and
balances. A bare or misspelled path is always treated as a table path and remains a usage error.
Accepted table bytes, optional notes, and run/provenance metadata are retained in the Stage 0
gate evidence directory.
