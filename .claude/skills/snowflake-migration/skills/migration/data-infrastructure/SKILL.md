---
name: data-infrastructure-setup
description: Shared infrastructure setup for data migration and data validation — prerequisites, compute pool, worker config, and source database/schema capture.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Data Infrastructure Setup

## Overview — Tell the User

Before starting any configuration, tell the user verbatim:

> Snowflake's Data Migration and Validation Framework is a fault-tolerant, scalable system for Snowflake Migrations. It uses a two-component architecture: an **Orchestrator** that runs inside your Snowflake account (on Snowpark Container Services) and breaks migration work into parallel tasks, and one or more **Workers** that run in an environment of your choice, connect and read data from your source system, and upload it to your Snowflake account.

> You make **two independent placement choices** in Step 0: where the **orchestrator** runs — **local** (on your machine, no compute pool — simplest) or **SPCS** (on a Snowpark Container Services compute pool — scalable) — and where each **worker** runs (usually **your machine**, since it reads your source; optionally other VMs, SPCS, or Kubernetes). The two don't have to match; nothing about compute pools matters until you put the orchestrator on SPCS.

> **You are in full control of what gets migrated and how.** You decide which tables to include, how they are partitioned for extraction, whether to use incremental synchronization or full loads, and how many workers run in parallel. You can filter rows, remap column names and types, and stop or resume the process at any point without losing progress. Nothing runs until you review and approve the configuration.
>
> **The same infrastructure is used for validation.** You choose what level of validation to run: **schema validation**, **metrics validation**, and **row-level validation**.

> **Metadata storage mode (trial accounts):** On Snowflake accounts **without Hybrid Table** support, the orchestrator falls back to standard/`TRANSIENT` metadata tables automatically. That path preserves correctness but **reduces task-queue throughput under contention** and effectively **limits how many workers you should run in parallel** — start with fewer workers and scale up carefully. This is **not** the same as L3 “hybrid” row validation. See [Metadata storage mode reference](./references/metadata-storage-mode-reference.md).

> **Always use the official tooling for data movement and validation.** Route table migration through `migrate_data` and validation through `validate_data`. Do not suggest ad-hoc extract/copy/compare scripts — the DMVF orchestrator and workers handle partitioning, loading, and multi-level validation.

> **Supported sources**: SQL Server, Redshift, Oracle, Teradata, PostgreSQL, Snowflake (validation only)
> **Supported target**: Snowflake

## Architecture

```
┌──────────────────┐     ┌──────────────────────────────────────┐
│  Customer Env     │     │         Snowflake Account             │
│  ┌─────────────┐ │     │  ┌────────────────────────────────┐  │
│  │  Worker(s)   │─┼─────┤  │  Orchestrator (SPCS)            │  │
│  └──────┬──────┘ │     │  │  → migration + validation tasks │  │
│         │ reads   │     │  └────────────────────────────────┘  │
│  ┌─────────────┐ │     │  ┌────────────────────────────────┐  │
│  │Source System │ │     │  │  Target Tables                  │  │
│  └─────────────┘ │     │  └────────────────────────────────┘  │
└──────────────────┘     └──────────────────────────────────────┘
```

- **Orchestrator** runs on SPCS (requires a compute pool) or locally. Handles migration workflows (break into tasks, `COPY INTO`) and validation workflows (schema/metrics/row comparison).
- **Worker** runs locally. Reads from the source and uploads to a Snowflake stage (migration) or streams rows for comparison (validation). Not needed for most Iceberg migration strategies.
- **Snowflake-to-Snowflake validation runs in warehouse.** It uses the
  orchestrator but no Data Exchange Worker. Do not generate worker config,
  ask for worker placement, or start a worker for a Snowflake source project.
- **The orchestrator + worker are shared, brought up ONCE, and reused across every `migrate_data` / `validate_data` dispatch** (migrate → validate → revalidate all run against the same infrastructure). Bring it up with `data_infrastructure(mode="up")` and tear it down with `data_infrastructure(mode="down")` (local) or [./teardown/SKILL.md](./teardown/SKILL.md) (SPCS). Dispatch does **not** start or resume infrastructure — if it is not up, `migrate_data` / `validate_data` return a `remediation` pointing back to `data_infrastructure(mode="up")`.
- **Whenever infrastructure starts**, tell the user that idle infrastructure can accrue Snowflake credits until teardown — the `data_infrastructure(mode="up")` response includes a `cost_reminder` field to relay.

## The `data_infrastructure` tool

Use the `data_infrastructure` tool (modes `up` / `down` / `status`) to manage the shared orchestrator + worker lifecycle — **pass `compute_pool` to run the orchestrator on SPCS, omit it for local**; `start_worker=false` skips the local worker (Iceberg / externally-managed workers). Call `up` once before dispatching migrations/validations. See the tool's own description for the full parameter list — don't restate it here.

## Idempotency

**One project setting, not one choice per action.** The orchestrator/worker
placement selected in Step 0 is shared by migration and validation and remains
in effect until the user explicitly asks to change it. Do not re-ask local vs
SPCS when validation begins, and do not ask a per-object subagent to start,
stop, repair, or reconfigure infrastructure. Subagents only dispatch against
the setup already in place; if infrastructure is unavailable, they return the
remediation to the main agent.

If the user explicitly asks to change placement or a persisted data strategy,
the **main agent** owns that setup change. Re-enter this skill for placement or
worker changes, and load [`../setup/data-strategy/SKILL.md`](../setup/data-strategy/SKILL.md)
for migration/validation strategy changes. Complete the change once, persist
it, bring infrastructure up as needed, and only then resume per-object
dispatch.

If this sub-skill has already been completed in the current project — i.e.,
the project has a recorded orchestrator placement, or (for worker-based
sources) `.scai/config/dew_configuration.toml` exists with no remaining
`<placeholder>` values — the infrastructure is **configured**, but that does
not mean it is **running**. Completion is durable; "up" is ephemeral.

Tell the user verbatim: "Data infrastructure already configured — bringing the shared orchestrator + worker back up (this also runs `scai data doctor` to confirm nothing has drifted)." Say it out loud rather than acting silently, because this runs live checks against Snowflake and the source. Then call `data_infrastructure(mode="up")` — it runs the [Level 1 Data Doctor](./references/data-doctor-reference.md#level-1-infrastructure-no-workflow-yaml) gate first (iterate until it stops reporting `doctor_failures`), then starts/resumes the orchestrator and (unless this project runs no local worker) the worker; relay its `cost_reminder`. **Also state the placement it resolved** — the response carries the project's recorded decision: `orchestrator_placement` (`local` = on this machine, no compute pool; `spcs` = SPCS compute pool) and `worker_placement` (`local` | `spcs` | `none` for Iceberg / externally-managed). `up` persists this the first time it resolves it, so on later resumes it is the project's saved choice — relayed consistently rather than re-inferred silently. If `orchestrator_placement` is `local` and they meant SPCS, they can switch by re-running with `compute_pool="<POOL>"`. Return to the caller without re-prompting. Only run a bare Level 1 Data Doctor instead when you specifically need a config-drift check *without* bringing infrastructure up.

Otherwise, proceed through the steps below.


---

## Step 0 — Choose where to run (ask FIRST)

The user has already confirmed they want data infrastructure (answered by
the `enableDataMigration` prompt node in the setup state machine). Now gather
placement choices **before** any compute pool, role, or warehouse details.

### 0.b — Where should the orchestrator run?

The orchestrator runs inside your Snowflake account, breaking work into tasks and issuing `COPY INTO` / validation queries. This is the **only** choice that decides whether you need a compute pool — it is **independent** of where the worker runs (0.c).

| Orchestrator | What it means | Choose when |
|--------------|---------------|-------------|
| **Local** | Runs on your machine — **no compute pool** | Simplest; small tables, dev/PoC, or an account that can't use SPCS. Runs only while your session is up. |
| **SPCS** | Runs on a Snowpark Container Services **compute pool** | Scalable + fault-tolerant, lives in your Snowflake account, survives your local session. Large/production migrations. Needs a compute pool. |

Ask:

> Where should the data-migration **orchestrator** run — **local** (simplest, no compute pool) or **SPCS** (scalable, needs a compute pool)?

| Answer | Next step |
|--------|-----------|
| **Local** | **Skip Question 0** (no compute pool). Bring it up later with `data_infrastructure(mode="up")` (omit `compute_pool`). |
| **SPCS** | Now that SPCS is chosen, call `configure(needs_compute_pools=true)` so the response lists the accessible pools, then resolve the pool in **Question 0**. Bring it up with `data_infrastructure(mode="up", compute_pool="<POOL>")`. |

### 0.c — Where should each worker run?

For a Snowflake source project, skip this question and record
`start_worker=false`. Continue to Question 1 after resolving the orchestrator
placement. `data_infrastructure(mode="up")` also enforces this server-side.

The worker reads from your **source** system and moves the data, so it **usually runs on your machine** (or wherever can reach the source) — independent of the orchestrator's placement in 0.b. Ask this **once**; the Worker setup step (Question 3) only acts on the answer and does **not** re-ask:

> How will you run the Data Exchange **Worker(s)** — a **single worker on this machine** (default), **multiple workers on separate VMs/servers**, on **Snowpark Container Services (SPCS)**, or on **Kubernetes**? (Some Iceberg strategies need **no** worker at all — say so and I'll set `start_worker=false`.)

Record the answer; it selects the worker sub-skill in **Question 3**.

## Worker Deployment Decisions

Having chosen placement in Step 0, gather the remaining Snowflake-side details **in order**. Question 0 is **SPCS-only** — skip it entirely on the local path.

### Question 0: Compute pool SPCS

If the user chose **local** in Step 0.b, **do not ask Question 0** — continue from **Question 1**.

The orchestrator on SPCS needs a compute pool. **Always ask** whether the user already has one or needs to create one — but first surface the pools their role can already reach, so they pick from a short list instead of recalling a name. Call `configure(needs_compute_pools=true)`; its response carries an `existing_compute_pools:` line listing them as `NAME (state)` (the compute-pool analogue of the `existing_connections:` line from `needs_source_connection`).

Then ask, presenting those pools as a short list (name + `state`):

> The Orchestrator needs a compute pool to run on SPCS. Here are the pools your role can access:
> `<NAME — state>` (one per line)
> Do you already have one to use, or do you need to create one?

Handle the `existing_compute_pools:` value:

- **Pools listed** → present them and let the user pick, or create a new one.
- **`none`** → the role sees no pool; say so and go straight to the create path.
- **`(unavailable: …)`** → couldn't reach Snowflake; tell the user, then fall back to asking them to name an existing pool or create one.

| Answer | Action |
|--------|--------|
| **Use an existing pool** | Confirm its `state` (from the list) is **ACTIVE** or **IDLE**. If `SUSPENDED`, run `ALTER COMPUTE POOL <POOL> RESUME;` and re-check; if `STARTING`, wait a moment and re-check. Then save it and continue to Question 1. |
| **Create a new one** | Route to → `./compute-pool-setup/SKILL.md` — guide the user through creating and configuring a compute pool. After that skill completes, return here and run the steps below. |

**Bring the shared infrastructure up on this pool:**

```
data_infrastructure(mode="up", compute_pool="<COMPUTE_POOL>")
```

> The pool is persisted, so later `up` calls (and `migrate_data`/`validate_data` after them) reuse it without re-passing it. Omit `compute_pool` to run a local orchestrator instead.

### Question 1: Snowflake role and privileges

Ask the user:

> What Snowflake role will you use for the migration? The Orchestrator needs a role with USAGE on the `SNOWCONVERT_AI` database and its `DATA_MIGRATION` and `DATA_VALIDATION` schemas.

| Situation | Action |
|-----------|--------|
| **Role has the required privileges** | Continue to Question 2. |
| **Role needs grants** | Run the grants below on behalf of the user (or show them to run with an admin role), then continue. |
| **DATA_MIGRATION_SERVICE already exists (created by another role)** | The executing role also needs OPERATE and MONITOR on the service. Run the extended grants below, then continue. |

**Standard grants:**

```sql
GRANT USAGE ON DATABASE SNOWCONVERT_AI TO ROLE <your_role>;
GRANT USAGE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <your_role>;
GRANT USAGE ON SCHEMA SNOWCONVERT_AI.DATA_VALIDATION TO ROLE <your_role>;
```

**Extended grants (when the service was created by another role):**

```sql
GRANT OPERATE, MONITOR ON SERVICE SNOWCONVERT_AI.DATA_MIGRATION.DATA_MIGRATION_SERVICE TO ROLE <your_role>;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <your_role>;
GRANT ALL PRIVILEGES ON ALL PROCEDURES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <your_role>;
GRANT ALL PRIVILEGES ON ALL STAGES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <your_role>;
```

### Question 2: Snowflake warehouse

Ask the user:

> Which Snowflake warehouse should be used for data migration and validation? The Orchestrator uses this warehouse to execute `COPY INTO` statements and run validation queries. Your Snowflake connection must have a warehouse configured — without one, data migration will fail silently.

| Situation | Action |
|-----------|--------|
| **User provides a warehouse name** | Verify the warehouse exists and the role from Question 1 has USAGE on it. Confirm that `~/.snowflake/config.toml` has `warehouse = "<WAREHOUSE>"` under the active connection. If not, help the user add it. Continue to Question 3. |
| **User is unsure** | Run `SHOW WAREHOUSES;` to list available warehouses and help them pick one. For large migrations, recommend a dedicated warehouse to avoid contention with other workloads. |

### Question 3: Worker setup

Skip Question 3 for a Snowflake source project. Call
`data_infrastructure(mode="up", start_worker=false, ...)` and continue to Data
Doctor; no DEW configuration file is expected.

**Do not ask where the worker runs again** — that was decided in **Step 0.c**. Route to the matching sub-skill; it handles install/start and returns control here:

| Step 0.c answer | Sub-skill |
|-----------------|-----------|
| **Single worker on this machine** | → `./worker-local-setup/SKILL.md` — install and start on one host |
| **Multiple workers on separate VMs/servers** | → `./worker-distributed-setup/SKILL.md` — affinity config + per-host copy instructions |
| **Snowpark Container Services (SPCS)** | → `./worker-spcs/SKILL.md` — image selection, Snowflake Secrets, CREATE SERVICE |
| **Kubernetes (external cluster)** | → `./worker-k8s-external/SKILL.md` — image selection, Kubernetes Secrets, Deployment manifest |
| **No worker (Iceberg or Snowflake-to-Snowflake validation)** | none — set `start_worker=false` on `data_infrastructure(mode="up")` |

**Stop here for worker deployment** — the routed sub-skill handles install/start, then **returns control here**. After it returns (or on the no-worker path), run the Data Doctor section below before returning to the caller.

---

## Data Doctor (Level 1)

This is the **single place** Level 1 Data Doctor runs — after **any** worker deployment path (local, distributed, SPCS, Kubernetes) returns control here. The worker sub-skills do not run it themselves.

Run [Level 1 Data Doctor](./references/data-doctor-reference.md#level-1-infrastructure-no-workflow-yaml). **Do not** start migration or validation setup until `result.hasFailures` is `false`. Iterate with the user on failures and warnings using each check's `suggestion`; you do not need to fix everything automatically.

---

## Checklist

```
- [ ] Compute pool passed to `data_infrastructure(mode="up", compute_pool=...)` — when using SPCS orchestrator
- [ ] Snowflake role has DATA_MIGRATION / DATA_VALIDATION usage (and service grants if needed)
- [ ] Warehouse configured on the Snowflake connection
- [ ] Worker config complete (no <placeholder> values) — unless pure Iceberg or Snowflake-to-Snowflake validation
- [ ] Level 1 scai data doctor — no Fail checks
```

---

Return control to the calling skill.

---

## Advanced operations (when the customer asks)

These are **optional** — not part of default setup. Load [Advanced operations reference](./references/advanced-operations-reference.md) when the user mentions:

| Topic | Trigger phrases | Summary |
|-------|-----------------|---------|
| **Rate limiting** | Source overloaded, throttle extractions/loads, pause one workflow | SQL rules in `DATA_MIGRATION.RATE_LIMIT`; soft cap on worker task pulls |
| **Preflight migration** | Dry-run, smoke test pipeline, test before full load | `preflight: true` in DM YAML → transient `PREFLIGHT_<id>` schema (not doctor, not Preliminary) |
| **Incremental validation** | Re-validate only changed partitions, ongoing DV | `synchronization` + watermark/checksum in DV YAML; baseline run required first |
| **Re-validation** | Retry failed validation partitions | `validate_data(mode="revalidate", workflow_name=…)` after parent workflow finishes |
| **Custom L3 normalization** | Formatting drift, case/spatial/period compare | `validationCustomNormalizationRules` in DV YAML — not DM `columnTypeMappings` |
| **Checksum blind spots** | Incremental sync missed a column change | Some types excluded/rounded from checksum — see advanced ref |
| **Non-hybrid metadata (trial)** | Trial account, HYBRID TABLE unsupported, slow pulls with many workers | Standard/`TRANSIENT` fallback — limit workers; see metadata storage mode ref |

Do not suggest ad-hoc throttling via polling env vars. Rate limits are metadata SQL, not workflow YAML fields.

---

## Reference

- [Metadata storage mode reference](./references/metadata-storage-mode-reference.md) — Hybrid vs standard metadata (trial fallback, worker scaling)
- [Advanced operations reference](./references/advanced-operations-reference.md) — rate limiting, preflight, incremental DV, revalidate
- [Data Doctor reference](./references/data-doctor-reference.md)
- [Worker Config Reference](./references/worker-config-reference.md)
- [Affinity Reference](./references/affinity-reference.md) — routing workers to workflows (multi-worker / multi-source)
- [Teardown (cost-saving suspend)](./teardown/SKILL.md)
