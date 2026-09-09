# Testing Framework Permissions — Reference

What Snowflake and source-DB privileges the testing framework needs, and what to do when `configure()` reports a `schema_status_validation: error(...)` or `prereq_status_clone_perms: failed(...)`.

> **Not auto-loaded.** The agent surfaces the configure response message verbatim and stops. The user can read this reference to find the GRANTs needed, apply them out-of-band, then say "recheck" / "done" — the agent runs `configure(ensure_metadata_schema=true)` to re-verify.

## What the testing framework does on Snowflake

When the user opts into testing (answers Q1 in `migrate-objects/SKILL.md` Step 2), `configure(ensure_metadata_schema=true)` triggers two probes that may write to Snowflake:

1. **`scai test validate --create-schema`** — installs the `VALIDATION` schema in the database named by `testing_results_database` in `.scai/settings/test_config.yaml` (the SnowConvert metadata database, not the migration target; projects predating that setting still have it in the target). Creates a stage (`@VALIDATION.BASELINES`), a results table (`VALIDATION.RESULTS`), supporting views (`SUMMARY`, `LATEST`, `FAILURES`), and the validation stored procedures (`VALIDATE_SINGLE`, `VALIDATE_BATCH`). Idempotent on the scai side — re-runs against an already-deployed schema are no-ops.
2. **`SHOW GRANTS TO ROLE CURRENT_ROLE()`** — read-only check that the active Snowflake role has `CREATE DATABASE on ACCOUNT`, needed for clone-based test isolation during `scai test validate`.

Later, during the deploy-test-fix loop, the framework also:

- Writes baseline JSON files to `@VALIDATION.BASELINES` (one per test case).
- Inserts results rows into `VALIDATION.RESULTS`.
- Creates short-lived database clones for DML procedure testing (`CREATE OR REPLACE DATABASE <clone> CLONE <user_db>`; dropped on teardown).
- Reads from source procedures, captures result sets via `scai test capture`.

The Snowflake-side privileges below cover all of the above.

## Snowflake-side privileges

Have a `SECURITYADMIN`-equivalent user (or whoever owns role grants in your account) run this block. Substitute `<DATABASE>`, `<WAREHOUSE>`, and `<ROLE>` with your project values. `<ROLE>` is the role used by the connection in `~/.snowflake/config.toml`.

```sql
USE DATABASE <DATABASE>;

-- Database-level provisioning for the testing schema.
GRANT USAGE ON DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT CREATE SCHEMA ON DATABASE <DATABASE> TO ROLE <ROLE>;

-- After `scai test validate --create-schema` creates the VALIDATION schema,
-- the role owning that schema needs to keep creating objects inside it.
-- Granting ownership is cleanest:
GRANT OWNERSHIP ON SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>
    COPY CURRENT GRANTS;

-- If you prefer not to transfer ownership, grant the bundle instead:
GRANT USAGE ON SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;
GRANT CREATE TABLE, CREATE VIEW, CREATE STAGE, CREATE FILE FORMAT, CREATE PROCEDURE
    ON SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;
GRANT SELECT, INSERT, UPDATE, DELETE
    ON FUTURE TABLES IN SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;
GRANT READ, WRITE
    ON ALL STAGES IN SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;
GRANT READ, WRITE
    ON FUTURE STAGES IN SCHEMA <DATABASE>.VALIDATION TO ROLE <ROLE>;

-- Read access to the schemas being tested. The validation procs run as the
-- caller and need to read the source rows the procedures under test touch.
GRANT USAGE ON ALL SCHEMAS IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT SELECT ON ALL TABLES IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT SELECT ON FUTURE TABLES IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT USAGE ON ALL PROCEDURES IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT USAGE ON FUTURE PROCEDURES IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT USAGE ON ALL FUNCTIONS IN DATABASE <DATABASE> TO ROLE <ROLE>;
GRANT USAGE ON FUTURE FUNCTIONS IN DATABASE <DATABASE> TO ROLE <ROLE>;

-- Clone-based test isolation. Each `scai test validate` run creates a
-- short-lived database clone of <DATABASE> and drops it on teardown. This
-- grant is what makes DML procedures safe to test against real data — and
-- what `prereq_status_clone_perms` checks for.
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <ROLE>;

-- Warehouse to run validation procs.
GRANT USAGE, OPERATE ON WAREHOUSE <WAREHOUSE> TO ROLE <ROLE>;
```

After applying, tell the agent "done" or "recheck" — it will run `configure(ensure_metadata_schema=true)` which clears the cached failure and re-probes.

### Why each grant

| Grant | Used for |
|---|---|
| `USAGE ON DATABASE` | Connecting to the database at all |
| `CREATE SCHEMA ON DATABASE` | `scai test validate --create-schema` installing `VALIDATION` |
| `OWNERSHIP` or the explicit bundle on `VALIDATION` | Creating the testing objects inside the schema |
| `READ, WRITE ON STAGE` | Uploading baseline JSON files to `@VALIDATION.BASELINES`, reading them during validation |
| `SELECT ON ALL/FUTURE TABLES` | Validation procs reading source rows the procedures under test touch |
| `USAGE ON ALL/FUTURE PROCEDURES, FUNCTIONS` | Invoking the migrated procs/functions during validation |
| `CREATE DATABASE ON ACCOUNT` | Clone-based isolation for DML proc tests |
| `USAGE, OPERATE ON WAREHOUSE` | Running validation queries |

## Source-side privileges by dialect

When `scai test capture` later fails with `permission denied on EXECUTE` or `SELECT permission denied` errors, the source role is missing privileges. The testing framework needs to (a) execute every procedure under test and (b) read every table those procedures touch.

### SQL Server

```sql
GRANT EXECUTE ON SCHEMA::<SCHEMA> TO <LOGIN>;
GRANT SELECT  ON SCHEMA::<SCHEMA> TO <LOGIN>;
-- Snapshot isolation is used to capture DML deltas atomically:
ALTER DATABASE <DB> SET ALLOW_SNAPSHOT_ISOLATION ON;
ALTER DATABASE <DB> SET READ_COMMITTED_SNAPSHOT ON WITH NO_WAIT;
```

### Redshift

```sql
GRANT USAGE ON SCHEMA <schema> TO <user>;
GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO <user>;
GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA <schema> TO <user>;
-- Transaction-based isolation needs nothing extra: each test runs in its
-- own implicit transaction that gets rolled back after capture.
```

### Oracle

```sql
GRANT CONNECT, RESOURCE TO <USER>;
GRANT SELECT ON <SCHEMA>.<TABLE> TO <USER>;       -- per table
GRANT EXECUTE ON <SCHEMA>.<PROCEDURE> TO <USER>;  -- per proc / package
-- Or, less granular but more common in dev environments:
GRANT SELECT ANY TABLE, EXECUTE ANY PROCEDURE TO <USER>;
```

### Teradata

```sql
GRANT SELECT  ON <DATABASE> TO <USER>;
GRANT EXECUTE PROCEDURE ON <DATABASE> TO <USER>;
-- Backup/restore isolation creates short-lived database copies on Teradata;
-- the user needs CREATE DATABASE on the parent database:
GRANT CREATE DATABASE ON <PARENT_DATABASE> TO <USER>;
```

## Common errors → fix

| Error message (verbatim from configure response or scai) | Fix |
|---|---|
| `Insufficient privileges to operate on database '<DB>'` | `GRANT USAGE ON DATABASE`, then `configure(ensure_metadata_schema=true)` |
| `Insufficient privileges to operate on schema 'VALIDATION'` or `not authorized to perform: CREATE SCHEMA` | `GRANT CREATE SCHEMA ON DATABASE`, then `configure(ensure_metadata_schema=true)`. After the deploy succeeds, the schema-bundle grants above are still needed for ongoing test runs. |
| `prereq_status_clone_perms: failed("CREATE DATABASE on ACCOUNT is not granted ...")` | `GRANT CREATE DATABASE ON ACCOUNT`. If your role inherits this via a parent role, the probe may report a false positive — confirm with `SHOW GRANTS ON ROLE <ROLE>` and proceed (the actual clone operation will succeed). |
| `Object 'VALIDATION.BASELINES' is not owned by ... GRANT WRITE` | `GRANT READ, WRITE ON STAGE` (or grant ownership of the schema) |
| Source-side: `permission denied on EXECUTE` | Apply the dialect-specific EXECUTE grants above |
| Source-side: `SELECT permission denied on relation X` | Apply the dialect-specific SELECT grants above |
