---
name: data_driven
description: Produce test_cases rows for an existing step-based YAML stub from realistic source-database values. Triggers: data_driven, data-driven tests, real data test cases, query source for test values.
license: Proprietary. See License-Skills for complete terms
---

You produce **`test_cases:` rows** for the object in your prompt, using
realistic values queried from the source database.

> You are NOT writing a YAML file. The stub YAML already exists (created by `scai test seed`). Your job is to produce **just the `test_cases:` rows** that will be merged into the existing stub.
>
> See [`../skills/migration/migrate-objects/references/step-based-yaml.md` → Placeholders and `test_cases`](../skills/migration/migrate-objects/references/step-based-yaml.md#placeholders-and-test_cases) for the row shape and dialect literal formatting.

## Inputs

The prompt carries `object_name`, `signature`, `source_code`,
`referenced_tables`, `source_connection`, and `project_dir`. A `split`
of `A` or `B` means this is one half of a pair — write the matching
tmp file below.

## Instructions

1. Write SQL queries to find valid parameter values from the referenced tables.
2. Run each query with the `query_source` MCP tool: `query_source(sql="<SQL>")`.
3. Build positional arrays matching the proc's parameter order. Use literals (`null`, numbers, strings) — no quoting; the runner formats them per dialect.
4. Include rows that should return data **and** rows that return empty results (real cases the proc must handle).

When `split` is `A`, focus on cases that return data (valid lookups, common
params). When it is `B`, focus on edge data (oldest / newest records,
boundary dates from the actual table contents).

### Testbed Fallback (No Live Source Connection)

When `query_source` is unavailable (e.g. Teradata migrations without a live connection):

1. Read testbed CSVs at `<project_dir>/testbed/<SCHEMA>/<TABLE>.csv` for each referenced table.
2. Derive realistic parameter values from the CSV data (dates, IDs, codes that match the proc's input columns).
3. Check `<project_dir>/specifications/data/<SCHEMA>/<TABLE>.yaml` for `branch_values` entries — these are curated values that exercise specific code branches. Prefer them over arbitrary CSV rows.

## Output

Write your rows to `<project_dir>/.scai/tmp/<object_name>_data_driven.yml`,
or `_data_driven_a.yml` / `_data_driven_b.yml` when `split` is set.

The file must contain only valid YAML starting with `test_cases:`. Also print the rows to stdout as a backup.

```yaml
test_cases:
  - [42, 19.99]           # valid customer, typical price
  - [999, 0.01]           # valid customer, minimum price (boundary in real data)
  - [12345, null]         # valid customer, NULL price (real edge from DB)
```

Each row is a JSON-ish array of literals: `null` for SQL NULL, unquoted numbers, strings in double-quotes if they contain colons / special chars (otherwise unquoted is fine in YAML).
