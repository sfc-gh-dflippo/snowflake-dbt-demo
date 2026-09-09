---
name: worker-distributed-setup
description: Run multiple Data Exchange Workers on separate VMs or servers, using affinity so each worker only processes the workflow it belongs to.
parent_skill: data-infrastructure-setup
license: Proprietary. See License-Skills for complete terms
---

# Worker Distributed Setup

Use this path when you will run **more than one** Data Exchange Worker on **separate hosts** — for
example to parallelize a large migration, or to migrate **multiple source databases/servers**
concurrently, one worker per source.

The per-host install/start mechanics are identical to a single worker — this skill covers only what is
**different** across multiple hosts: **affinity** (so workers don't steal each other's tasks) and
**per-host config**.

> **Read first:** [Affinity Reference](../references/affinity-reference.md) — what affinity is, the
> orchestrator claim rule, and why the orchestrator must stay null-affinity.

## When you need affinity here

- **Multiple workers, one source, sharing load** — leave the explicit override unset. scai stamps the
  same stable project-default affinity on the workflow and every generated worker config, and the
  orchestrator hands each matching free worker the next task. Follow
  [worker-local-setup/SKILL.md](../worker-local-setup/SKILL.md) on each host and stop.
- **Multiple sources (or you want strict isolation)** — you **must** tag each source's workflow and its
  worker with a **matching, non-null** label, or a worker will claim another source's tasks and write to
  the wrong place. This is the rest of this skill.

## Step 1 — Choose one affinity label per source

Pick a short, stable label per source database/server — a per-database label reads well, e.g.
`mdx-salesnorth`, `mdx-finance`. Confirm the set of labels with the user (one per worker/source).

## Step 2 — Tag the workflow and the worker together

For **each** source, set the label with the plugin's single source of truth:

```
configure(affinity="<label>")
```

`configure(affinity=…)` persists the override. `migrate_data`/`validate_data` setup forwards it to
workflow generation, and `data_infrastructure(mode="up")` forwards it to local-worker generation, so
the two agree by construction (see the Affinity Reference for the two-carrier rule). Then generate that
source's workflow and worker config as usual.

- **Local workers on each host** → the generated `dew_configuration.toml` already carries the label;
  copy it to the matching host (Step 3).
- **SPCS / Kubernetes workers** → `configure` tagged the *workflow*; set the **same** label as
  `AGENT_AFFINITY` in that worker's spec/manifest (the [worker-spcs](../worker-spcs/SKILL.md) /
  [worker-k8s-external](../worker-k8s-external/SKILL.md) skills do this). The workflow label and
  `AGENT_AFFINITY` must match exactly.

> **Never set an orchestrator affinity.** One orchestrator (null-affinity) serves all sources: it drains
> every workflow and routes each task to the worker whose label matches. Giving the orchestrator an
> affinity would starve every other source. See the Affinity Reference.

## Step 3 — Per-host worker config + start

For each worker host:

1. Ensure the host meets that source's prerequisites and can reach both that source and Snowflake — see
   [worker-local-setup/SKILL.md](../worker-local-setup/SKILL.md) Prerequisites.
2. Place that source's `.scai/config/dew_configuration.toml` on the host (the one carrying its label from
   Step 2). Each host runs exactly one worker against one source config.
3. Start the worker on that host: `scai data worker start --local` (see worker-local-setup Step 2). Repeat
   per host.

> **Cost note (relay to the user):** each running worker polls Snowflake and can accrue warehouse
> credits even when idle. Stop workers per host when the wave's data work is done (teardown skill).

## Step 4 — Verify

Confirm each host's worker connected to the orchestrator and is polling. If a worker reports it is
running but its workflow shows "0 pending" / tasks never start, suspect an affinity mismatch (workflow
label ≠ worker label, or an orchestrator was given an affinity) — see the data-migration
[Troubleshooting Reference](../../migrate-objects/actions/data-migration/references/troubleshooting-reference.md)
and the [Affinity Reference](../references/affinity-reference.md).

## Done

All workers are running on their hosts. Return control to the parent skill, which runs Level 1 Data
Doctor before proceeding.
