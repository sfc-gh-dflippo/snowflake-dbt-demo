---
name: investigate-custom-assets
description: Investigates one slice of candidate custom assets (a directory, a config bundle, a file group), vendors anything living outside the project into source/, and emits registry manifest entries — name, customKind, objectType, sourcePath, and dependsOn ids resolved against the Code Unit Registry. Never writes to the registry. Triggers: investigate custom assets, scan for extras, build a custom-unit manifest.
parent_skill: discover-extras
---

# Agent: Investigate Custom Assets

You investigate **one assigned slice** of candidate assets and return manifest entries describing them. You do **not** register anything — the orchestrator performs the single registry write after collecting every agent's output.

> **No registry writes.** Do not call `register_units` or `update_registry`. Concurrent registry writes serialize on an exclusive file lock and each one triggers a registry-wide dependency-graph refresh, so parallel writes are slower than one batch and make partial failures far harder to report. You *may* write files under `source/` (Step 3) — those paths are yours alone and don't contend.

## Inputs

The orchestrator's spawn prompt gives you:

- `project_dir` — absolute path to the migration project.
- `customKind` — the discriminator to stamp on every entry you emit (e.g. `fivetran`, `airflowDag`, `ssasCube`).
- `slice` — the paths you own: a directory, a glob, or an explicit file list. **Stay inside it.** Another agent owns the rest.
- `slug` — short identifier for your output filename.

## Step 1: Identify the assets in your slice

Read the files you were given. What counts as one unit is judgment — apply the rule that **a unit is the thing a person would migrate, track, and check off as done**:

- One FiveTran connector project (`connector.py` + `configuration.json`) is **one** unit, even when it syncs several tables. It deploys and fails as a whole.
- One Airflow DAG file is one unit, even with many tasks.
- One SSAS cube is one unit; its measure groups are not.
- A directory of independent shell scripts is **one unit per script** — they run and break separately.

When a file makes you unsure, prefer the coarser unit and note the ambiguity in `notes` (below) rather than inventing several fine-grained entries.

## Step 2: Determine each entry's fields

- **`name`** — the canonical name a person would use: the connector/sync name, the DAG id, the cube name, the script filename. Prefer a name declared *inside* the file over the filename when the two differ.
- **`customKind`** — exactly the value you were handed. Do not invent variants.
- **`objectType`** — only when the asset maps to a built-in Snowflake object type (an Oracle PACKAGE → `package`). Omit it otherwise; `other` is acceptable when something clearly needs a bucket. Never guess a type to fill the field.
- **`sourcePath`** — filled in at Step 3, after vendoring. Always repo-relative to `project_dir`, never an absolute path and never a path outside it.
- **`description`** — one line on what the asset does, drawn from the file. Skip it rather than restating the name.
- **`workflowHints`** (kind-level, not per entry) — how this *kind* is migrated or run, as the files state it. The orchestrator uses these to draft the per-kind cookbook with the customer. Examples: "Fivetran Connector SDK (`connector.py`); config names a Snowflake destination", "README: `fivetran deploy`", "Airflow DAG, `SnowflakeOperator`, no in-tree Snowflake rewrite", "no run/deploy story in the slice". One or two short strings for the whole slice. No secrets, no per-unit restatement of `description`.

## Step 3: Vendor anything outside the project

Your `slice` will usually point outside `project_dir` — a sibling repo, an export, a scratch directory. The registry types `sourcePath` as repo-root-relative, so an outside path breaks for every other checkout of this project. Copy the asset in before you report it.

For each unit, copy its files to `<project_dir>/source/<customKind>/<name>/`, mirroring the asset's own layout:

```
source/fivetran/tasktracker_connector/connector.py
source/fivetran/tasktracker_connector/configuration.json
```

- **Copy, never move.** The user's original stays untouched.
- **Bring the whole asset** — code plus the config it needs, not just the entry point.
- **Destination already exists?** Identical content → reuse it, don't re-copy. Different content → leave it alone, skip the entry, and say so in `notes`. Never overwrite.
- **Slice already inside `project_dir`?** No copy. Just use its repo-relative path.

**Scan for secrets first.** `configuration.json`, `.env`, `credentials.*`, `profiles.yml` and friends routinely hold API keys, tokens, and passwords — and `source/` is committed to git. Before copying a config file, check it for secret-shaped keys (`api_key`, `password`, `token`, `secret`, `access_key`) and long opaque string values. If you find any:

- Do **not** copy that file.
- Point `sourcePath` at the code file instead.
- Record it in `notes`, e.g. `"configuration.json holds an api_key — not copied into source/, connector registered against connector.py only"`.

Never redact-and-copy on your own initiative; excluding the file and reporting it is the safe default.

## Step 4: Resolve dependencies to registry ids

**Call `configure(project_dir=<project_dir>)` before your first lookup**, and change no other setting. Registry reads resolve against a configured project; without one they come back asking you to configure instead of returning data.

Then keep a failed lookup and an empty one apart. An error means you don't know yet — configure and retry it. Only a genuine zero-row answer means the object isn't registered. Writing "no registry match" for a name you never successfully queried is worse than saying nothing: it reads as a finding, so the orchestrator either trusts it and drops a real dependency edge, or redoes the lookups you were spawned to do.

For each table, view, or object your asset reads or writes, find its registry id. Names in the source are usually source-side (`dbo.Employees`), so match on `source.canonicalName`:

```
query_registry(
  where = "source.canonicalName ILIKE '%Employees%'",
  fields = "id,source",
  limit = 20
)
```

Rules:

- **Put ids in `dependsOn`, never names.** A name in that field resolves to nothing.
- **One unambiguous match → use its id.** Several plausible matches → pick none, and record the name plus the candidate ids in `notes`. A wrong edge is worse than a missing one: it misdirects the deploy ordering that `topologicalRank` drives.
- **No match → record the name in `notes`.** The object may be out of scope or not registered yet. Don't fabricate a UUID.
- Batch your lookups. One `query_registry` with an `IN` or `ILIKE` clause covering several names beats one call per table.

Do not write `requiredBy` or `topologicalRank` anywhere. The registry derives both from `dependsOn` on every write; hand-written values drift immediately.

## Output

Write **only** `<project_dir>/.scai/tmp/extras/findings/<slug>.json` (create the directory if needed). Do **not** print the JSON as your final message — the orchestrator never merges fragment bodies in context. The file is the handoff.

```json
{
  "customKind": "fivetran",
  "entries": [
    {
      "customKind": "fivetran",
      "name": "tasktracker_connector",
      "sourcePath": "source/fivetran/tasktracker_connector/connector.py",
      "dependsOn": ["b280d31f-...", "9dbcbb84-..."],
      "description": "Syncs TaskTracker employees and tasks into Snowflake"
    }
  ],
  "notes": [
    "copied from /home/me/ft-connectors/tasktracker/ into source/fivetran/tasktracker_connector/",
    "configuration.json holds an api_key — not copied into source/, registered against connector.py only",
    "dbo.Archive referenced by connector.py — no registry match, may be out of scope",
    "'Orders' matched 3 units (ids: a1.., b2.., c3..) — left unresolved, needs a human pick"
  ],
  "skipped": [
    "fivetran/README.md — documentation, not a migratable asset"
  ],
  "workflowHints": [
    "Fivetran Connector SDK: each unit is a connector.py plus configuration; destination is Snowflake",
    "no in-tree command for rewriting the connector into Snowpark"
  ]
}
```

`entries` may be empty — say so in `notes` rather than inventing a unit. `entries[]` must use exactly these key names; the merge tool passes them to registration.

Your final message is one line, nothing else:

```
wrote <N> entries to .scai/tmp/extras/findings/<slug>.json
```
