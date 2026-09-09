---
name: etl-seed
description: Seed the per-unit ETL test YAML for a deployed ETL code unit by running `scai test seed` (which fills pipeline + validation.tables from the CUR), then fill index_columns and have the user confirm before the live comparison runs.
parent_skill: migrate-etl
license: Proprietary. See License-Skills for complete terms
---

# ETL Seed

Generates the `kind: etl` test YAML for a single, already-deployed ETL code unit at `artifacts/<id>/etl-test/<name>.yml`. The YAML declares the `pipeline` (how to launch the source package and which converted target to run) and a `validation.tables` list of source→target table pairs to compare.

**`scai test seed` seeds ETL units — you do not hand-author the file.** For an ETL unit (`kind = 'etl'`; SSIS or Informatica natively, any platform once an `external_command:` section opts in — see Step 2) `scai test seed` walks the Code Unit Registry, takes the unit's **write** dependencies (`INSERT` / `UPDATE` / `MERGE` / `DELETE`), and emits a `validation.tables` entry per written table — pairing the source table (`source.canonicalName`) with its Snowflake target (`target.canonicalName`). It leaves `index_columns` blank for you to fill. Your job is to run the seeder, fill in the join keys, handle any skipped units, and confirm with the user — not to invent table pairs.

## Step 0: Resolve Unit

Read the registry entry (the executor passes `object_id`; if entered by name, locate via `migration_status(mode="my_objects_summary")`):

| Field | Used as |
|---|---|
| `id` | `{ETL_ID}` for the `--where` filter and the `artifacts/<id>/etl-test/` path |
| `source.platform` | source kind (`ssis`, `informatica`, …) |
| `files.source.path` | source definition file (`.dtsx`, `.xml`, …); its stem is the YAML file name |

The `etlSeed` task has a `taskCompleted` precondition on `deploy`, so the executor only dispatches this skill once the unit is deployed — you do not need to re-check deployment here.

## Step 1: Run `scai test seed`

```bash
scai test seed --where "id = '{ETL_ID}'"
```

Add `--append` when a YAML already exists for the unit — it re-emits the table pairs from the current CUR while **preserving** your edited `index_columns` / `test_cases` (matched per source→target pair):

```bash
scai test seed --where "id = '{ETL_ID}'" --append
```

Platform is auto-detected per unit from the registry — no `--platform` flag. On success the file is written to `artifacts/{ETL_ID}/etl-test/<name>.yml` with the execution block and table pairs filled from the CUR. When an `external_command:` section is present, the side it names is emitted as `{type: external_command, wait_seconds: <n>}` — two keys and nothing else, since the command itself lives only in `test_config.yaml` — and the other side keeps its native block. Tune `wait_seconds` per unit if one package runs longer than the shared default.

## Step 2: Handle a Skipped Unit

If `scai test seed` reports the unit was **skipped**, it names a reason. Do not paper over it by hand-writing tables — fix the cause:

| Skip reason | Meaning / action |
|---|---|
| `NoWriteDependencies` | The CUR records no write (`INSERT`/`UPDATE`/`MERGE`/`DELETE`) deps — nothing to validate. Re-check the unit was fully converted/assessed; confirm with the user whether it actually writes tables. |
| `MissingDependency` | A write-dep is flagged `isMissing` in the CUR — register/resolve that dependency first. |
| `MissingCanonicalName` | A resolved write-dep has no source/target canonical name — fix the registry entry. |
| `UnknownFormat` / `PendingFormat` / `MixedFormat` | The converted part(s) aren't in a seedable target format yet — finish stabilization/deploy for the routable parts. |
| `NoArtifactsPath` | The CUR has no artifacts path — the unit isn't converted/deployed as expected. |
| `UnsupportedPlatform` | Source platform is neither SSIS nor Informatica, and the project has not opted into an external command. Only SSIS and Informatica have a built-in source executor; any other `kind: etl` platform is seedable **only** once `.scai/settings/test_config.yaml` declares an `external_command:` section with `side: source`, which replaces the source executor with a launch-and-wait command. With `side: target` the source is still native, so this skip still applies. Add the section (see `etl-validate`) and re-run with `--append`, or treat the unit as out of scope. |

Only after the underlying issue is understood should you add a missing pair by hand (with the user), and only if genuinely necessary.

## Step 3: Fill `index_columns` and Confirm

`scai test seed` leaves `index_columns` blank. Open `artifacts/{ETL_ID}/etl-test/<name>.yml` and, for each `validation.tables[]` entry, set the join key used to align rows between source and target:

- `comparison.index_columns` — the column(s) that uniquely key a row (usually the natural / primary key).
- `comparison.target_index_columns` — only when the target's key column names differ from the source's.

Then show the user the seeded table pairs and the keys you chose, and ask them to confirm or correct — the CUR can miss dynamically-named or conditionally-written tables. Adjust per their feedback. This is a stopping point that needs the user's input — as is Step 3b on an Informatica project.

## Step 3b: Ask for the Informatica `pmcmd` Endpoint (Informatica projects only)

A seeded Informatica unit carries no `service` / `domain` of its own. Neither can be derived from
the CUR, and both are the same for every unit of a project, so they live **once** in the
`informatica:` section of `.scai/settings/test_config.yaml` — beside `pmcmd_path` / `username` /
`password` — which `scai test seed` creates with `TODO_INFA_*` placeholders and warns about:

```yaml
informatica:
  pmcmd_path: /opt/informatica/10.5/server/bin/pmcmd
  username: ${INFORMATICA_USERNAME}
  password: ${INFORMATICA_PASSWORD}
  service: IS_EDW_NIGHTLY      # pmcmd -sv: the Integration Service running the workflows
  domain: Domain_EDW           # pmcmd -d:  the domain that service belongs to
```

**Ask the user for `service` and `domain`** — and for `pmcmd_path` too if that placeholder is
still there. As at Step 3, this is a stopping point that needs the user's input, not agent-side
work: nothing on disk can supply these values (see above), so there is nothing to infer them from.
Do not invent a plausible-looking Integration Service name, and do not leave a sentinel in place
expecting `--check-env` to settle it later — the check reports the gap, it cannot fill it. With the
user's answers in hand, write them in once for the project, then verify **every** seeded unit
resolves before handing off to `etlValidate`:

```bash
scai test etl-validate --platform {PLATFORM_ID} --check-env
```

The `informatica_service_domain` check names any file that still cannot resolve an endpoint. A
leftover `TODO_INFA_*` there is a failure, not a default — an unresolved sentinel would otherwise
reach `pmcmd` as a literal `-sv TODO_INFA_SERVICE`.

Two things this does **not** mean:

- **Per-unit `TODO_INFA_FOLDER` / `TODO_INFA_WORKFLOW` are separate.** Those are the only
  placeholders still emitted into a unit's own YAML, and only when the CUR could not supply them —
  fill them in that file, not in `test_config.yaml`.
- **A per-unit override is still available.** A project whose workflows span more than one
  Integration Service or domain can set `service:` / `domain:` under that unit's `pipeline.source`;
  a unit-level value wins over the project-wide one. Hand-added overrides survive a re-seed with
  `--append`.

## Step 4: Record Completion

Once the YAML has a non-empty `validation.tables` with `index_columns` filled and the user has confirmed:

```
transition_status(status="advance", task="etlSeed", outcome="completed", where="id = '{ETL_ID}'")
```

The state machine routes to `etlValidate`.

## Step 5: Exclusion

To skip seeding (no live source system, or the packages are deprecated), disable the task at the project level in `.scai/config/plugin.yml`:

```yaml
tasks:
  etlSeed:
    enabled: false
```

A disabled task reads as **excluded** by the state machine: `etlValidate`'s `artifactExists` gate then treats `etlSeed` as a producer that will never run and is itself excluded rather than blocked (a hand-authored test YAML still readies `etlValidate`). This is **project-wide** — it disables `etlSeed` for every ETL unit. Per-unit exclusion is not supported: writing `codeStatus.etlSeed=excluded` on a single entry reads back as *completed*, not excluded.
