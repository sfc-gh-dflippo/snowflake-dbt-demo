# Capture and Upload Baselines

After creating the test YAML files, capture baselines from the source database and upload to Snowflake.

> **⚠️ SCOPE: Capture baselines for ONE object at a time.**

## Step 1: Capture Baselines from Source Database

Baselines upload to the Snowflake stage `@<TESTING_RESULTS_DATABASE>.VALIDATION.BASELINES` — the database named by `testing_results_database` in `.scai/settings/test_config.yaml`; no copy is kept on the user's laptop (customer data residency).

```bash
scai test capture \
  -s <SOURCE_CONNECTION_NAME> \
  -c <SNOWFLAKE_CONNECTION_NAME> \
  --where "source.canonicalName ILIKE '%<schema>.<object_name>%'"
```

**Flags:**
- `-s, --source-connection` — Name of the source connection (from `scai connection list`). Uses default if not specified.
- `-c, --connection` — Snowflake connection (destination for baseline upload). Required unless `target_connection.name` is set in `settings/test_config.yaml`.
- `--where` — Registry filter, SQL-like (same syntax as `scai code deploy --where`). The canonical form used across the plugin is `source.canonicalName ILIKE '%<name>%'`.

## Step 2: Verify

List the stage, filtering server-side to just this object's baselines:

```bash
snow stage list-files @<TESTING_RESULTS_DATABASE>.VALIDATION.BASELINES \
  --pattern ".*<schema>\.<object_name>.*" \
  -c <SNOWFLAKE_CONNECTION_NAME>
```

## Step 3 (BTEQ scripts only): mark capture complete

For BTEQ scripts the baseline is uploaded to the stage and `VALIDATION.BASELINE_METADATA` is not written, so the state machine cannot infer capture from Snowflake — stamp the task explicitly:

```
transition_status status=advance task=captureBaseline --where "id = '<unit_id>'"
```

Procedures/functions skip this — their `captureBaseline` completes once `VALIDATION.BASELINE_METADATA` has a row for the object whose `ROW_COUNTS` sum to more than zero.

If capture fails because **the source object cannot run as written** (column-count mismatch on `INSERT…EXEC`, missing columns, the object's own SQL errors on `EXEC`), escalate on `captureBaseline`. Do not `ALTER` the source to make the capture green and do not skip ahead to deploy. A person decides whether to fix source, mark the object out of scope, or treat it as always-erroring.

## CHECKPOINT

Confirm:
- [ ] Baselines captured for `<object_name>` from source database
- [ ] Baselines visible on Snowflake stage `@<TESTING_RESULTS_DATABASE>.VALIDATION.BASELINES`
- [ ] At least 15-25 test cases for this object

## Next Steps

Load [migrate-object/SKILL.md](../migrate-object/SKILL.md) to start the deploy-test-fix loop for `<object_name>`.
