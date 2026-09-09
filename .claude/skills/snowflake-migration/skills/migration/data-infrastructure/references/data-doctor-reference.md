# Data Doctor reference

Run `scai data doctor` before starting data migration or data validation. The command checks Snowflake grants, worker (DEW) configuration, orchestrator connectivity, workflow YAML schema (when `--config` is passed), and partition-key feasibility on the source (migration configs). It does **not** create or modify objects.

Use `--json` (a global flag) so you can parse structured results. Run from the project root.

## JSON contract

The envelope is the standard CLI shape. On success it carries a `result` object; on a runtime error it carries an `error` object instead of `result`:

```json
{
  "success": true,
  "warnings": ["..."],
  "result": {
    "hasFailures": false,
    "hasWarnings": true,
    "checks": [
      {
        "label": "Role grants",
        "status": "Pass",
        "detail": "Role MIGRATION_ROLE has USAGE on SNOWCONVERT_AI.DATA_MIGRATION",
        "suggestion": null,
        "section": "Snowflake"
      },
      {
        "label": "Partition key — dbo.Orders",
        "status": "Warning",
        "detail": "High NULL ratio (12%) in OrderDate",
        "suggestion": "Choose a non-nullable column or accept skewed partitions",
        "section": "Partition key"
      }
    ],
    "recommendations": {
      "advice": "...",
      "suggestedMaxThreads": 8
    }
  }
}
```

- `result.hasFailures` / `result.hasWarnings` are precomputed booleans — gate on `hasFailures` directly instead of re-scanning.
- `result.checks[].status` is one of `Pass`, `Warning`, `Fail`, `Skipped` (PascalCase — match exactly).
- `result.checks[].section` is one of `Snowflake`, `DEW`, `Orchestrator`, `Partition key`.
- `suggestion` is populated only for `Warning` and `Fail` checks; it is `null` otherwise.
- `warnings` is omitted when empty.

## Result handling (all levels)

1. **If there is no `result` object** — the envelope has a top-level `error` (`code`, `message`, `suggestion`, `details`) or the command emitted no JSON at all — surface stderr / the error to the user and stop. This is a runtime error (bad connection name, missing TOML, command crash), not a check failure; do **not** treat it as a passing run.
2. Read `result.checks`. **Group by `section`**, then list **Fail** first, then **Warning**, then **Skipped**.
3. **Gate on `result.hasFailures`** — when you run doctor manually (Level 1, before setup), don't proceed to workflow setup while it is `true`. The run tools (`migrate_data`/`validate_data`) enforce this gate themselves at run time, so you only apply it by hand for the pre-setup Level 1 check. Present each failure's `detail` and `suggestion` to the user with concrete next steps (grants SQL, TOML edits, partition column changes, etc.); you do not need to auto-fix everything.
4. **Iterate** — after the user applies fixes, re-run the same doctor command until `hasFailures` is `false`.
5. **Warnings** — the CLI exits 0 with warnings. Summarize them and ask whether to fix now or proceed.
6. **Skipped** — explain what was skipped and which flag unlocks that check (usually `--config` or `--source-connection`).

| Section | Common fixes |
|---------|----------------|
| Snowflake | Grants from [data-infrastructure/SKILL.md](../SKILL.md); warehouse on connection; [troubleshooting-reference.md](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md#spcs-service-privilege-errors) |
| DEW | Worker TOML placeholders, ODBC driver, [worker-config-reference.md](./worker-config-reference.md) |
| Orchestrator | Service suspended → `ALTER SERVICE … RESUME`; affinity mismatch → migration troubleshooting |
| Partition key | Set or change `columnNamesToPartitionBy`; use `--analyze-partition-keys` for suggestions |

---

## Level 1: Infrastructure (no workflow YAML)

**When:** After compute pool registration and worker config are complete (end of [data-infrastructure/SKILL.md](../SKILL.md) or any worker sub-skill), **before** generating or running a migration/validation workflow.

Resolve connection names from the latest `configure()` response (`snowflake_connection`, `source_connection`).

```bash
scai data doctor \
  -c <snowflake_connection> \
  --source-connection <source_connection> \
  --json
```

Omit `-c` or `--source-connection` only when not yet configured; those sections will show `Skipped` checks with instructions to pass the flag.

**Done when:** `result.hasFailures` is `false`. User has acknowledged or resolved warnings.

---

## Level 2: Workflow gate (automatic — do not run by hand)

The run-time doctor is **built into the tools**. `migrate_data(mode="run")` and `validate_data(mode="run")` run a quick infrastructure doctor (no `--config`) before starting and **refuse to start** when any check fails, returning `doctor_failures` in the response. You do not run `scai data doctor` manually before run.

- **On `doctor_failures`:** surface each failure's `detail` / `suggestion` to the user and fix it, then call the tool again. To proceed despite failures, pass `skip_doctor=true` — only after the user explicitly accepts them. Overridden failures come back as `doctor_warnings`.
- **Workflow-schema validation** is already enforced by the run tools (they reject a malformed YAML before starting), so the run gate intentionally skips `--config`.

### Partition-key analysis (setup, not run)

`migrate_data(mode="setup")` runs the partition-key probe (`--analyze-partition-keys`: NULL-ratio and cardinality queries against the source, plus PK-based suggestions from the Code Unit Registry) and returns `partition_key_findings`. Resolve or accept those while editing the YAML — they are advisory and never block. Validation configs have no partition-key analysis.

### Manual invocation (debugging only)

To reproduce what the tools run, e.g. when diagnosing a persistent `doctor_failures`:

```bash
scai data doctor -c <snowflake_connection> --source-connection <source_connection> --json
# add --config <workflow_path> --analyze-partition-keys to mirror the setup probe
```

