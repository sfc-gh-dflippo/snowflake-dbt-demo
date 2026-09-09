# SQL Query Reference

Queries against the `VALIDATION` schema created by `scai test validate --create-schema`.

The schema lives in the SnowConvert metadata database — attach
`metadata_database:` / `.scai/config/plugin.yml` (`SNOWCONVERT_AI` unless
overridden), not the migration target. Qualify every query with that name.
The examples below leave the database off only as a shorthand.

## Validation Results

```sql
-- Summary by code unit
SELECT * FROM VALIDATION.SUMMARY ORDER BY pass_rate DESC;

-- Latest result per test case
SELECT * FROM VALIDATION.LATEST ORDER BY procedure_name;

-- Failures with details
SELECT * FROM VALIDATION.FAILURES;
```

## Investigation

```sql
-- Failures for a specific code unit
SELECT procedure_name, params_hash, status, baseline_rows, actual_rows, error_message
FROM VALIDATION.LATEST
WHERE UPPER(procedure_name) = UPPER('<object_name>')
  AND status IN ('FAIL', 'ERROR');

-- All results history for a code unit (VARIANT `data`; prefer LATEST)
SELECT data:procedure::VARCHAR, data:params_hash::VARCHAR,
       data:status::VARCHAR, data:match_type::VARCHAR,
       data:error::VARCHAR, data:executed_at::TIMESTAMP_TZ
FROM VALIDATION.RESULTS
WHERE UPPER(data:procedure::VARCHAR) = UPPER('<object_name>')
ORDER BY data:executed_at::TIMESTAMP_TZ DESC;
```

## Source of truth

`scai test validate` writes each case into `VALIDATION.RESULTS`. `VALIDATION.LATEST`
is the newest run per `(procedure_name, test_name, params_hash)`. Qualify with
`metadata_database` from attach — not the migration target. There is no
`<project_dir>/test-results/results.json`.

Each LATEST row has:
- `procedure_name`, `params_hash`, `status`, `match_type`, `error_message`
- `parameters` — the case inputs
- `differences` — human-readable diff descriptions
- `baseline_rows`, `actual_rows` — counts (not the row payloads)

## Available Views

| View | Purpose |
|------|---------|
| `VALIDATION.SUMMARY` | Pass/fail counts per code unit |
| `VALIDATION.LATEST` | Latest result per test case |
| `VALIDATION.FAILURES` | Failed/errored tests with details |
