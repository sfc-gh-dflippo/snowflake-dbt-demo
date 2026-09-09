# Affinity Reference — routing workers to workflows

Affinity is a **routing label** that binds a workflow's tasks to the worker(s) allowed to run them.
It is the mechanism that makes **multiple workers** (or multiple source databases/servers) run
**concurrently** without stealing each other's work.

## How the orchestrator matches (the claim rule)

When a worker (or the orchestrator itself) pulls tasks, the queue matches on affinity with this rule
(consumer = the puller's affinity; task = the affinity stamped on the task row):

```
consumer IS NULL            → claims tasks of EVERY affinity
task affinity IS NULL       → claimable by ANY consumer
consumer == task            → exact match
consumer contains '*'       → glob match (e.g. "team-*" matches "team-sales")
```

Two consequences drive everything below:

1. **A null-affinity consumer claims all tasks.** This is why the **orchestrator must never be given an
   affinity** — a null orchestrator drains workflows of *every* affinity, and stamps each task with its
   own workflow's affinity so the right worker picks it up. If you gave the orchestrator an affinity it
   would partition itself, and workflows of other affinities would sit at "0 pending" forever. **The
   plugin never sets the orchestrator's affinity.** Isolation happens at the *worker* layer.
2. **Isolation requires BOTH the workflow and the worker to carry the same non-null label.** A
   null worker cross-claims other sources' tasks (wrong-server writes); a null workflow is claimed by
   any worker. So the working multi-source recipe is:

   > **null orchestrator + affinity-tagged workflow + affinity-tagged worker**, one label per source/DB.

## The two carriers that must agree

Affinity lives in **two** files that must carry the same value:

| Carrier | Where | Set by |
|---|---|---|
| **Workflow config** (`affinity:`) | `artifacts/data_{migration,validation}/workflows/*.yaml` | `migrate_data`/`validate_data` (`mode="setup"`) |
| **Worker config** (`[application].affinity`) | project-relative `.scai/config/dew_configuration.toml` (local worker) | `data_infrastructure(mode="up")` |
| **Worker env** (`AGENT_AFFINITY`) | SPCS spec / k8s Deployment manifest | the worker-spcs / worker-k8s-external skill (set it to the **same** label) |

## Project default vs explicit override

scai gives each project a stable default affinity such as `northwind-3f9a1c2b`. When the plugin does
not pass `--affinity`, scai applies that default to both newly generated workflow and local-worker
configuration. This is the normal path for one project/source and requires no user-selected label.

Use `configure(affinity="<label>")` only when you need an explicit routing group, typically one label
per source database/server in a multi-source project. The override persists to project-relative
`.scai/config/plugin.yml` and is forwarded to both generators:

- **Local worker:** `data_infrastructure(mode="up")` generates the DEW config with the same override.
  If an existing generated config carries a different affinity, the plugin regenerates it.
- **SPCS / Kubernetes worker:** set the same override as `AGENT_AFFINITY` in the worker spec/manifest.
  The worker-spcs and worker-k8s-external skills do this.

The plugin never passes affinity to the orchestrator.

## Dispatch diagnostics

Bare `create-workflow` performs an advisory affinity-aware readiness check. It warns when no running
orchestrator or worker can claim the workflow affinity; the workflow is still created. A separate
warning can say an explicit workflow override differs from the project's default affinity. That second
warning is expected for a deliberate multi-source override; verify that the worker carries the same
override.

## When affinity is the cause of a stall

"Found 0 pending workflows" / tasks stuck non-terminal is often an affinity mismatch: the workflow
carries one label and no worker carries a matching (or null) one, or the orchestrator was mistakenly
given an affinity. See the data-migration [Troubleshooting Reference](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md).
