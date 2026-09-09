---
name: etl-validate
description: Run scai test etl-validate to compare live ETL pipeline output (SSIS/Informatica natively, any platform via an external_command opt-in) against the converted Snowflake output. The CLI stamps codeStatus.etlValidate — do not invent advance outcomes.
parent_skill: migrate-etl
license: Proprietary. See License-Skills for complete terms
---

# ETL Validate

Runs `scai test etl-validate --platform <platform>` against a single ETL code unit, verifying that the original source package and its Snowflake equivalent produce identical output. Requires the ETL unit to be **deployed** and a **test YAML** to exist for it.

**Deploy, the test YAML, and connections are all enforced by the state machine, not this skill.** `etlValidate` has deterministic preconditions: `deploy` (the unit is deployed to Snowflake), `artifactExists` on `etl-test/*.y*ml` (a `kind: etl` test YAML — `.yml` or `.yaml`, from `etlSeed`/`scai test seed` or hand-authored — is present under the unit's artifacts dir), and `configureSourceConnectionExtract` + `configureSnowflakeTarget`. The executor only dispatches this skill once all hold, so it is safe to run standalone (targeted directly at `etlValidate`): the machine will not dispatch it against an undeployed unit, one with no test YAML, or an unconfigured session. `scai test etl-validate` reads the connection details from the project's `settings/test_config.yaml`; named-connection overrides can be passed with `-c` / `-s`.

## Step 0: Resolve Unit

Read the registry entry (the executor passes `object_id`; if entered by name, locate via `migration_status(mode="my_objects_summary")`):

| Field | Used as |
|---|---|
| `id` | `{ETL_ID}` for the `--where` filter |
| `source.platform` | `{PLATFORM_ID}` for `--platform` (`ssis`, `informatica`, …) — pass the registry's value **verbatim**, including its casing (`sqlServer`, not `sqlserver`) |

## Step 0b: Platforms Without a Built-in Executor

Only `ssis` (SQL Agent / SSISDB) and `informatica` (`pmcmd` / dbt Cloud) have a built-in
executor. Any other `kind: etl` platform — DataStage, Talend, an in-house shell or binary
orchestrator — is rejected by `--platform` and by the seeder **unless** the project declares an
`external_command:` section in `.scai/settings/test_config.yaml`:

```yaml
external_command:
  side: source                              # source | target — required
  command: ["/opt/etl/run.sh", "--full"]    # required, argv list (no shell)
  working_dir: /opt/etl                     # optional
  env: {ETL_ENV: prod}                      # optional
  wait_seconds: 300                         # seed-time default for the emitted YAML
```

The named side is then driven by **launching that command and waiting** `wait_seconds`. It is a
timer, not a status poll: nothing is polled, the exit code is never read, and this side cannot
fail. When the wait expires the side reports SUCCEEDED and the **table comparison alone decides
pass/fail** — so a script that exits 1 still yields a PASS if the tables match, and a pipeline
still running when the timer expires shows up as a row difference. Set `wait_seconds` longer than
the real pipeline runtime.

Three things to tell the user when you set this up:

- **`command` is an argv list, not a shell string.** No quoting, globbing, or `&&` chaining is
  interpreted — wrap those in a script and point `command` at it.
- **The child gets a minimal environment**: `PATH`, `HOME`, plus whatever `env:` declares, and
  nothing else. The harness environment (which carries Snowflake credentials) is deliberately not
  inherited, so a script that relied on an inherited variable must declare it under `env:`.
- **Seed ordering.** `test_config.yaml` is generated *after* ETL emission, so on a first-ever seed
  the section does not exist yet and the native path is taken. Add the section, then re-run
  `scai test seed --where "id = '{ETL_ID}'" --append` for the section to be honoured.

Without the section every gate stays loud — a mistyped `--platform` is still an error rather than
a zero-unit run that reads as "everything passed".

## Step 1: Live Environment Pre-flight

The state machine guarantees the connections are *configured*; it cannot know whether the live systems are *reachable*. Run the built-in probe once to catch a down SQL Server, an expired Snowflake token, or a missing SSISDB catalog before starting a long comparison:

```bash
scai test etl-validate --platform {PLATFORM_ID} --check-env
```

The probe must test the **same** connection the real run in Step 2 will use, so if the session uses named-connection overrides append the identical flags here (`--connection {SNOWFLAKE_CONNECTION}` / `--source-connection {SOURCE_CONNECTION}`) — otherwise the probe green-lights the default connection while Step 2 runs against a different one.

| Check | What it tests |
|---|---|
| `sql_server_connectivity` | Can reach the source SQL Server instance (SSIS) |
| `teradata_connectivity` | Can reach the source Teradata system (Informatica) |
| `snowflake_connectivity` | Can reach the Snowflake account |
| `ssisdb_catalog_access` | Can query `SSISDB.catalog.packages` (SSIS only) |
| `pmcmd_accessibility` | The `informatica:` section exists and its `pmcmd` binary is present and executable (Informatica only) |
| `informatica_service_domain` | Every seeded Informatica unit resolves a `pmcmd` integration service + domain (Informatica only) |
| `mwaa_accessibility` | The MWAA environment named by the `mwaa:` section is reachable (Informatica, when configured) |

`informatica_service_domain` is the one **configuration** check in this set. `scai test seed` no
longer writes a `service`/`domain` per seeded unit — both are project-wide, so they live once in
the `informatica:` section of `.scai/settings/test_config.yaml` — and this check resolves that
section through the same resolver the real run uses, once per seeded unit, so a leftover
`TODO_INFA_*` sentinel or an unset `${VAR}` is caught here instead of reaching `pmcmd` as a
literal. It reports the offending files. Fix it by filling the section (see `etl-seed` Step 3b),
or, for a project whose workflows span more than one Integration Service, by setting `service:` /
`domain:` under that unit's `pipeline.source`.

With `external_command:` + `side: source`, the probe switches to the platform-agnostic strategy
**regardless of platform** (including `ssis`): it reports `snowflake_connectivity`, plus source
connectivity when the run built a source connector, and runs **no** platform-tooling check. There
is no SSISDB catalog to read and no `pmcmd` to locate when the harness just launches a command, and
demanding them would fail a run that would otherwise work. The source connection is still probed
where it exists because the table comparison reads the source tables through it. With
`side: target` the source is still native and keeps its native checks, tooling included.

If any check fails: **STOPPING POINT** — surface the failing check name and the error from the output, and help the user fix the live-system issue (start the server, refresh credentials, grant catalog access). Do not proceed to Step 2 with a failing probe. These are mostly runtime reachability checks, not config gates — a failure usually means the environment is down, not that the plugin is misconfigured. The exception is `informatica_service_domain` (and `pmcmd_accessibility` when it reports a missing section): those *are* configuration gaps, so the fix is an edit to `test_config.yaml`, not a restart.

## Step 2: Run Live Comparison

```bash
scai test etl-validate --platform {PLATFORM_ID} \
  --where "id = '{ETL_ID}'"
```

If the session uses named-connection overrides, append:
- `--connection {SNOWFLAKE_CONNECTION}` (Snowflake)
- `--source-connection {SOURCE_CONNECTION}` (source DB)

The command streams per-package results. Watch for the summary line reporting the failed-unit count.

**The CLI owns the registry stamp.** On each unit it actually ran, `scai test etl-validate` writes `codeStatus.etlValidate`:

| CLI outcome | Registry stamp |
|---|---|
| Unit passed | `{ status: "completed", updatedAt }` |
| Unit failed | `{ status: "failed", updatedAt, error: "comparison" }` |
| Skipped (no ETL test YAML) | *no stamp* — field stays pending |

## Step 3: Confirm stamp — do not invent advance

**Do not** call `transition_status(status="advance", …)` to invent a green or red outcome from narration. Re-read the unit via `query_registry` / `migration_status` and confirm `codeStatus.etlValidate` matches the CLI summary.

- All packages passed → registry should already read `completed`; the ETL flow is terminal.
- One or more packages failed → registry should read `failed` with `error: "comparison"`. Surface the failed package names and row-level differences from the CLI output so the user can investigate the conversion gap.

If the CLI exited non-zero but the stamp is missing (registry write failed), say so explicitly and do **not** stamp green yourself — ask the user to re-run or investigate the registry write error.

## Step 4: Exclusion

To skip live validation, disable the task at the project level in `.scai/config/plugin.yml`:

```yaml
tasks:
  etlValidate:
    enabled: false
```

A disabled task reads as **excluded** by the state machine, so the ETL flow reaches its terminal state without running the comparison. This is **project-wide** — it disables `etlValidate` for every ETL unit. Per-unit exclusion is not supported: writing `codeStatus.etlValidate=excluded` on a single entry reads back as *completed*, not excluded.
