---
name: data-infrastructure-teardown
description: Cost-saving teardown for shared data infrastructure — verify no in-flight workflows, then call data_infrastructure(mode="down") to stop/suspend orchestrator and worker (SPCS or local, as configured). The compute pool auto-suspends. Invoked after every migrate_data() / validate_data() cycle and at end-of-migration.
parent_skill: data-infrastructure-setup
license: Proprietary. See License-Skills for complete terms
---

# Data Infrastructure Teardown

`data_infrastructure(mode="down")` does the teardown for **both** placements in one call:

- **Local** — reaps the orchestrator + worker processes this MCP session started.
- **SPCS** — when a `compute_pool` is configured for the project, it also suspends the SPCS orchestrator
  service and the Data Exchange Worker. The compute pool then **auto-suspends** on its own
  (`AUTO_SUSPEND_SECS`), so there is no separate pool step. Pass `drop=true` to remove the DEW service
  permanently instead of suspending it.

So teardown is normally just: **call `data_infrastructure(mode="down")`**. Everything below is the
in-flight check to do first, plus the few cases the tool cannot cover on its own. Nothing auto-resumes —
bring it back with `data_infrastructure(mode="up")` before the next wave (per `../SKILL.md`).

> **Why this exists:** an SPCS `DATA_MIGRATION_SERVICE` consumes compute pool seconds; a local
> orchestrator or local worker polling `TASK_QUEUE` wakes the warehouse on every interval — all accrue
> cost when idle.

## When to Invoke

| Trigger | Invocation |
|---------|------------|
| After `migrate_data()` reaches `completed` or `failed` for a wave | Caller prompts the user (default Yes) before loading this skill |
| After `validate_data()` reaches `completed` or `failed` for a wave | Caller prompts the user (default Yes) before loading this skill |
| End of full migration (no more waves) | Caller invokes this skill unconditionally |

**Skip entirely** when the project never configured data infrastructure (no `compute_pool` and no local
orchestrator/worker was started).

---

## Step 1: Verify no in-flight workflows

`data_infrastructure(mode="down")` already **refuses** while a migrate/validate job it can see is running
(it reads the project's relay ledger) — so a plain `down` is safe by default. But that ledger only covers
jobs dispatched from **this project on this machine**. Before tearing down shared SPCS infrastructure that
**another machine** might be using, confirm the queue is quiet directly:

- `job_status()` — every job you know about must report `terminal: true`.
- Then probe the orchestrator's queue (SPCS, cross-machine):

```sql
SELECT WORKFLOW_ID, STATUS, COUNT(*) AS N
FROM SNOWCONVERT_AI.DATA_MIGRATION.TASK_QUEUE
WHERE STATUS NOT IN ('completed', 'failed', 'cancelled')
GROUP BY WORKFLOW_ID, STATUS
ORDER BY WORKFLOW_ID;
```

If any rows return, **abort teardown** and report:

> Teardown skipped — workflow `<id>` still has `<N>` `<status>` task(s). Wait for completion (or cancel via the troubleshooting reference) before suspending.

If a job is running only on this machine and you intend to stop it anyway, pass
`data_infrastructure(mode="down", force=true)`.

---

## Step 2: Tear down

Call the tool:

```
data_infrastructure(mode="down")                # suspend (resumable) — the default
data_infrastructure(mode="down", drop=true)     # SPCS: also permanently drop the DEW service
```

The response reports `execution` (`local` | `cloud`) and the `orchestrator` / `worker` actions
(`stopped_local` | `suspended_spcs` | `dropped` | `stop_failed`). Relay it to the user. On SPCS the
compute pool auto-suspends shortly after the service stops — no pool call needed.

If the payload reports a `partial` status with `spcs_errors`, read the error to decide what it means:
- An **insufficient-privileges** failure on the `ALTER SERVICE … SUSPEND` the tool runs through scai —
  grant the privileges below and re-run `data_infrastructure(mode="down")`.
- A **"service … does not exist"** failure on `worker stop` — this project has no SPCS DEW worker (Iceberg,
  a local worker, or `start_worker=false` at `up`); nothing to suspend, so it is safe to ignore.

### Privilege prerequisites (SPCS)

The tool suspends the SPCS service via `scai`, using the project's connection/role. The role that ran
`scai data orchestrator setup` holds these already; a **different** teardown role (e.g. `ACCOUNTADMIN`
cleaning up after the owner) needs them granted explicitly:

```sql
GRANT MONITOR, OPERATE ON SERVICE SNOWCONVERT_AI.DATA_MIGRATION.DATA_MIGRATION_SERVICE TO ROLE <your_role>;
-- If the DEW worker service is in use:
GRANT MONITOR, OPERATE ON SERVICE SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_WORKER_SERVICE TO ROLE <your_role>;
```

### Local orchestrator started outside MCP (the tool can't reap it)

`data_infrastructure(mode="down")` reaps the local orchestrator/worker **this MCP session** spawned. A
local orchestrator the user launched **in their own terminal** (`scai data orchestrator start --local`) is
a foreground process the tool did not spawn and cannot kill (`scai data orchestrator stop --local` is
advisory only). Tell the user:

> Stop the local orchestrator so it stops polling Snowflake:
> - Find the terminal running `scai data orchestrator start --local` and press `Ctrl+C`.
> - If it was launched in the background, end that process (`pkill -f "scai data orchestrator.*start"`, or
>   Task Manager on Windows).

The same applies to a local **worker** started outside MCP (`scai data worker start --local`): the
MCP-managed worker stops on session exit, but a manually-launched one needs a `Ctrl+C` /
`pkill -f "scai data.*worker.*start"`.

---

## Step 3: Cost-hygiene recommendations (idempotent, optional)

Run these once per project — they make future suspend cycles tighter. **Skip compute-pool items** when no
`compute_pool` is configured.

```sql
-- Compute pool auto-suspend — the pool unblocks quickly after the service stops:
ALTER COMPUTE POOL <COMPUTE_POOL> SET AUTO_SUSPEND_SECS = 60;

-- Warehouse auto-suspend — verify the connection's warehouse suspends quickly:
SHOW PARAMETERS LIKE 'AUTO_SUSPEND' IN WAREHOUSE <WAREHOUSE>;
-- If value > 60:
ALTER WAREHOUSE <WAREHOUSE> SET AUTO_SUSPEND = 60;
```

`<COMPUTE_POOL>` is the value persisted by `data_infrastructure(mode="up", compute_pool=...)` — read from
`.scai/settings/cloud-migration.yaml`. Both changes are persistent and safe to apply outside teardown.

---

## Resuming for the next wave

Nothing auto-resumes on the next dispatch. Bring the shared infrastructure back up **once** with
`data_infrastructure(mode="up")` before the next `migrate_data` / `validate_data` — it resumes the SPCS
orchestrator (expect a 30–60s warm-up after suspend) or starts a persistent local orchestrator, plus the
worker, depending on whether a `compute_pool` is configured.

---

## Checklist

```
- [ ] No in-flight workflows — job_status() terminal + TASK_QUEUE quiet (Step 1)
- [ ] data_infrastructure(mode="down") called; response relayed (Step 2)
- [ ] Local orchestrator/worker started outside MCP stopped by the user, or N/A
- [ ] Warehouse AUTO_SUSPEND <= 60s (one-time, Step 3), or N/A
```

Return control to the caller.
</content>
