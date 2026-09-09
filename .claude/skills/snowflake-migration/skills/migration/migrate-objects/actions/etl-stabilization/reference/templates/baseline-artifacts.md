# Baseline Report Schema

Defines the format for `artifacts/phases/phase_{N}/baseline_batch_{B}.md` written by test-gen agents.

## Required Structure

### Summary Table (top of file, machine-parseable)

| Element | Test File | Baseline Result | Failure Details |
|---------|-----------|-----------------|-----------------|
| `{name}` | `{test_file_path}` | passed/failed/skipped | failure summary or — |

### Element Details (one section per element with failures or notable context)

#### {element_name}

- **Status:** passed | failed | skipped:{reason}
- **EWI:** {codes}
- **Failing Assertions:** {list with failure messages}
- **Fix Hint:** {one-line suggested approach based on EWI pattern}

Only include Element Details sections for failed or notable elements. Passed elements need only their Summary Table row.

## Statuses

- `passed` — all assertions passed on unfixed code
- `failed` — one or more assertions failed (fix agent needed)
- `skipped:disabled-in-source` — element is disabled in source definition
- `skipped:container-only` — element is a structural container with no executable logic
- `skipped:file-io-noop` — element performs file I/O not applicable in Snowflake
- `skipped:dbt-dependency` — element is an EXECUTE DBT PROJECT invocation
- `skipped:external-dependency` — element has unfixable external dependencies
