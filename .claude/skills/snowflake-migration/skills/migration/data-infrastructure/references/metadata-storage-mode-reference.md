# Metadata storage mode (Hybrid vs standard tables)

Use this when a customer runs on a **trial / lower-tier Snowflake account**, sees bootstrap errors mentioning **`HYBRID TABLE`**, or asks why migration/validation feels **slower** or **workers seem capped** despite a healthy source.

> **Not the same as L3 “hybrid” validation.** This topic is Snowflake **Hybrid Tables** used for orchestrator **metadata** (`TASK_QUEUE`, `TABLE_METADATA`, `PARTITION_METADATA`). It is **unrelated** to `rowValidationMode: hybrid` (L3 row-hash + cell drill-down).

## What happens on accounts without Hybrid Tables

The orchestrator probes Snowflake at bootstrap (or reads `SCHEMA_DEPLOYMENT_PROFILE` / env overrides). When Hybrid Tables are **unsupported**, it falls back to **standard / `TRANSIENT`** metadata tables with the same logical schema.

| Path | Metadata DDL | Task claiming |
|------|--------------|---------------|
| **Hybrid (default on capable accounts)** | `HYBRID TABLE` + hybrid indexes | High-throughput batch pull with row locking |
| **Standard (fallback)** | `TRANSIENT` tables, no hybrid indexes | `PULL_SINGLE` loop + `MERGE` idempotency |

Manual overrides (orchestrator / SPCS service env):

- `SNOWFLAKE_METADATA_STORAGE_MODE=HYBRID|STANDARD|ICEBERG` — preferred three-way selector
- `SNOWFLAKE_USE_HYBRID_TABLES=1` — force hybrid when three-way mode is unset
- `SNOWFLAKE_USE_HYBRID_TABLES=0` — force standard/`TRANSIENT` (typical on trial)

**Restart the orchestrator** after changing storage-mode env vars — resolution is cached for the process lifetime.

In-place conversion between hybrid and standard metadata schemas is **unsupported** — match env to the existing schema or deploy a **fresh** metadata schema.

See also: [Worker config reference](./worker-config-reference.md) (limit worker count on the standard path), [Advanced operations — rate limiting](./advanced-operations-reference.md#rate-limiting-protect-source-or-shared-resources).

---

## Disclaimer for customers (consistency, performance, workers)

When Hybrid Tables are **not** used and the framework falls back to regular/`TRANSIENT` metadata:

### Consistency

- **Correctness is preserved** via conditional `UPDATE`, transactional `MERGE`, and idempotent metadata writes — not via hybrid-table `SELECT … FOR UPDATE`.
- Under **high concurrent task claiming**, the standard path may show **more retries** (for example Snowflake `90232` transaction aborts) before a worker successfully leases a task. Retries are expected; do not treat them alone as data corruption.
- Metadata **`TRANSIENT`** tables have **no Time Travel** — orchestration state is rebuildable but not point-in-time recoverable like hybrid metadata.

### Performance

- **Task-queue throughput is lower** under contention: more round-trips per pull, more warehouse scan work without hybrid secondary indexes.
- Large backlogs of pending tasks can show a **degrading pull curve** until completed rows are purged/archived.
- This is **metadata-layer** latency — it can make the pipeline feel slow even when the **source database** and **Snowflake warehouse** have spare capacity.

### Worker count — practical limits

- **Do not assume unlimited horizontal scale** on the standard metadata path. Many workers × many `max_parallel_tasks` threads all compete for the same `TASK_QUEUE` rows.
- **Agent guidance:** on trial / confirmed non-hybrid metadata, **start conservatively** — for example **1–2 workers** with **`max_parallel_tasks` 2–4** — then increase gradually while watching orchestrator logs for repeated pull retries and end-to-end workflow time.
- **Source-side rate limiting** (`RATE_LIMIT`) protects the source DB but **does not** remove metadata-queue contention — both may be needed.
- If the account **supports Hybrid Tables**, prefer the hybrid metadata path (default probe) for production-scale parallelism unless the customer explicitly standardizes on trial-style deployment.

---

## When to mention this to the user

| Situation | What to say |
|-----------|-------------|
| Trial / Enterprise trial account | Fallback is automatic; set expectations on throughput and worker scaling |
| `Unsupported feature 'HYBRID TABLE'` during bootstrap | Standard path is expected; use `SNOWFLAKE_USE_HYBRID_TABLES=0` if probe is ambiguous |
| Many workers but tasks stay `pending` | Check metadata mode before adding more workers — standard path may need fewer concurrent claimers |
| Customer compares to “production Mobilize” timing | Hybrid metadata + indexes explain much of the gap on trial |

Do **not** confuse with [rate limiting](./advanced-operations-reference.md#rate-limiting-protect-source-or-shared-resources) (source protection) or [L3 hybrid validation](../../setup/data-validation/references/workflow-config-reference.md#l3-result-codes-hybrid-mode).
