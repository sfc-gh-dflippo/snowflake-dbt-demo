---
name: discover-extras
description: Surface assets the conversion engine doesn't generate (FiveTran, dbt, Airflow, SSAS cubes, Oracle PL/SQL packages, custom shell scripts, etc.) and register them as code units with `kind=custom` and a free-form `customKind` discriminator (any string outside the reserved Kind enum) so the orchestration layer (next_object + state machine) tracks them alongside built-in units. Triggers from the setup state machine as its last step; can also be re-entered any time the user identifies more custom assets.
parent_skill: setup
license: Proprietary. See License-Skills for complete terms
---

# Discover & Register Custom Assets

The conversion engine generates a known set of object types — tables, views, procedures, functions, SSIS packages, and so on. Real migrations almost always pull in **other things** that touch the same database: orchestration tools, BI assets, custom scripts, or object kinds the engine doesn't generate yet.

This step catches those and registers them in the registry as code units with `kind=custom` and a free-form `customKind` discriminator (any string outside the reserved Kind enum), so the orchestration layer tracks them alongside built-in units.

## On Entry

The setup machine only routes here after the user has said they *have* assets
the engine doesn't generate (last setup step, after assessment and — if they
opted in — the post-assessment migration setup), so don't re-ask that. Open with:

> **Discover custom assets.** Let's get them tracked. I'll go category by category and register what you list, so each one shows up alongside the rest of your migration.

If the user has already registered some custom units (`migration_status` shows units with `kind=custom`), surface the count first:

> "You've already registered N custom units (customKinds: <comma-separated list>). Want to add more, or call this done?"

## Step 1: Pick Categories

Use `ask_user_question` (multi-select) with these top categories. Keep the list at five and let the auto-appended "Something else" cover the long tail:

> "Which of these apply to your project? (multi-select)"
> 1. **Orchestration / data movement** — FiveTran, Airflow, Informatica, Talend, ADF, Glue
> 2. **BI / analytics layer** — SSAS cubes, Tableau extracts, Looker views, dbt models
> 3. **Engine doesn't generate yet** — Oracle PACKAGE/PACKAGE BODY, SQL Server triggers, sequences, edge cases
> 4. **Hand-maintained scripts** — bash/PowerShell jobs, cron tasks, manual deployment scripts
> 5. **Nothing after all** — I was wrong upstream, move on

If the user picks **Nothing after all**, jump to **Step 4** and mark the step done — that records the step as answered so it isn't put to them again.

## Step 2: For Each Category, Walk Through Registration

For every selected category, work through it in turn. The pattern is the same:

1. Tell the user the recommended `customKind` value for this category — this string is the discriminator that will land in the registry's `source.customKind` and `target.customKind` fields. The unit's top-level `kind` is always `custom`. Recommended values:
   - Orchestration: `fivetran`, `airflow`, `informaticaWorkflow`, `talendJob`, `adfPipeline`, `glueJob`
   - BI: `ssasCube`, `tableauExtract`, `lookerView`, `dbtModel`
   - Engine gap: `oraclePackage`, `oraclePackageBody`, `sqlServerTrigger`, `sequence`, `synonym`
   - Scripts: `shellScript`, `powerShellScript`, `cronJob`, `manualScript`
   - Anything else: free-form. Pick something descriptive and stable — the agent uses it to group, filter, and route. Cannot be one of the four reserved Kind values (`databaseObject`, `script`, `etl`, `custom`).

2. Ask the user — lead with pointing you at the code, since that's the cheapest thing for them to do:
   > "For `<customKind>`, where does it live? Point me at a directory or repo path and I'll scan it and work out the names and dependencies myself. If you'd rather list them, I need a name per item, plus optionally a Snowflake `objectType`, a repo path, and what each one reads from — inline, or as a CSV/JSON/YAML paste."

3. Decide how the items get investigated. When the user hands you a ready manifest, there is nothing to investigate — go straight to step 4. When they point you at code (a directory, a repo path, "our FiveTran stuff is in ./fivetran/"), somebody has to read those files to work out the unit names, paths, and dependency ids. **Fan that reading out — don't do it serially yourself.** See [Orchestrating the investigation](#orchestrating-the-investigation) below.

4. Register with **`register_units`** — that is the only register tool. If it is not in your loaded tools, search for `register_units` by that name. Do not look for `register_custom_unit` or `register_custom_units_from_manifest`; those names are gone.

   One call, one shape:
   - Investigation findings → `register_units(expected_slugs=[...])`
   - A pasted list → `register_units(entries=[...])`
   - A single item while talking → `register_units(custom_kind=..., name=...)`

   `customKind` is required on every unit: omit it and that row fails. Report the count the registry confirmed, plus any `failed[]` and `withWarnings[]` rows. **Count what came back, never your own tally of the entries you sent.** A hand-counted merge drifts from what landed, and the closing number is the part of this step the user acts on. For failures, ask if they want to fix and retry or skip; `withWarnings[]` is where a non-portable `sourcePath` surfaces, so a warning there means the vendoring step needs revisiting before you call this done.

   Every shape returns the same envelope: `registered[]` / `failed[]` / `withMissingDependencies[]` / `withWarnings[]` (plus `notes` / `skipped` / `workflowHints` when findings were merged). That response *is* the confirmation — don't follow it with a `query_registry` to check the write landed. The default projection is `id` / `source` / `files`, so `dependencies` and `extensions` come back absent and a correctly-registered unit looks blank. Pass `fields=["*"]` when you genuinely need to read them back.

   Treat a non-empty `dependsOnMissing` as a wrong id, not a waiting one. The ids are recorded either way, but `dependsOn` resolves by registry id and nothing re-resolves it later, so an id that matches no unit today matches none tomorrow. Look it up again before moving on.

## Orchestrating the investigation

Investigating candidate assets is read-heavy and parallelizes cleanly: each slice of files is independent, and resolving dependency names to registry ids is a read. Registering is the opposite — it happens in the orchestrator, once the whole picture is in one place.

**Fan out the reading. Register from the findings folder — do not merge in context.**

```
  ./fivetran/  ./airflow/dags/  ./scripts/
       │             │              │
    [agent]       [agent]       [agent]        ← write .scai/tmp/extras/findings/<slug>.json
       └─────────────┴──────────────┘
                     │
                     ▼
   register_units(expected_slugs=[...])
                     │  tool merges + registers
                     ▼
              one report (counts, notes, hints)
```

Why the write stays here and does not go in the agents — and what has to be true of it however you make the calls:

- **Every unit is registered exactly once.** Re-registering an asset to attach an edge you settled on later gives the registry two of it. Decide the edge first, then register.
- **One reconciled report at the end**, with its numbers taken from the registration responses rather than from your own tally of what you sent.
- **Everything that didn't resolve is named in the message the user reads**, not left in the fragments.
- Registry writes take an **exclusive file lock** and each one triggers a registry-wide dependency-graph refresh (this is what maintains `requiredBy` and `topologicalRank`). At seven units that costs nothing measurable; it is a reason to prefer one call, not a reason to fear several.

`register_units(expected_slugs=[...])` is the call: the batch *is* the reconciled report — one envelope, one set of counts, nothing to add up. Do not walk the list with one call per unit.

A dependency between two units registered in the same step is not expressible either way, so don't plan for one: `dependsOn` resolves by registry id, ids are assigned at creation, and no caller can supply one. An id that matches nothing is therefore a wrong id and stays missing — never a timing artifact that settles on its own.

### Ask first, then fan out across every category at once

Step 2's questions need the user, so ask them per category. The *investigation* doesn't — so don't run a spawn-merge-register round per category. Collect every category's pointer first, then spawn one batch covering all of them, then merge and register the whole step together.

Three categories pointing at code is one round of agents and one merge, not three of each — and one closing report, not three.

### How many agents

> **MANDATORY: If the user pointed at a directory or config file, you MUST spawn sub-agents.** Do not read the directory yourself. Do not register units inline. Skipping the spawn loses the audit trail, skips dedup, and breaks the expected-slugs safety check.

| Situation | Spawn | Registration tool |
|---|---|---|
| User pasted a manifest, or named 1–3 items inline | **None.** Register directly; spawning costs more than the work. | `register_custom_unit` (one call per item) |
| One directory / config bundle per category | **One agent per `customKind`.** Mandatory — no exceptions for small directories. | `register_custom_units_from_manifest(expected_slugs=[...])` |
| A category with many independent files (DAGs, scripts, cubes) | **Shard it** — group ~10 files per agent, up to 8 agents at once. Queue the rest. | `register_custom_units_from_manifest(expected_slugs=[...])` |

Sharding rule: **one agent owns a path, and paths never overlap.** Two agents reading the same directory produce duplicate entries that you then have to reconcile by hand.

### Spawn

Spawn every agent in one `task` batch so they run concurrently. Each agent reads its own instruction file — do **not** paste the instructions inline. `<discover_extras_dir>` is this skill's own directory; pass it as an absolute path so the agent doesn't have to guess its working directory:

```
Read the instructions at <discover_extras_dir>/agents/investigate.md
then investigate your assigned slice. Write findings only to
.scai/tmp/extras/findings/<slug>.json (not to your final message).

project_dir:  <project_dir>
customKind:   <customKind>
slice:        <the directory, glob, or explicit file list this agent owns>
slug:         <short-name-for-your-output-file>
```

Spawning hands back an **agent id, not the agent's answer** — the agents are still working when the call returns. Keep every id you were given; collecting the results is its own step ([Merge](#merge) below), and an agent you never collect is work you paid for and threw away.

### Vendor assets that live outside the project

Users almost always point at something outside the project directory — a sibling repo, a downloaded export, another migration project's scratch dir. **Copy it into the project before registering.** `files.source.path` is typed repo-root-relative by the registry schema; recording an outside path leaves the project broken for everyone else, because their checkout has no such directory.

Concretely, `sourcePath: "/tmp/tmp.abc123/fivetran/connector.py"` is wrong twice: it doesn't survive `git clone`, and if that directory happens to be another migration project, this project's state now depends on an unrelated one.

The copy destination is `<project_dir>/source/<customKind>/<name>/`, mirroring the asset's own internal layout:

```
source/fivetran/tasktracker_connector/connector.py
source/fivetran/tasktracker_connector/configuration.json
```

`sourcePath` is then the entry point inside that copy — `source/fivetran/tasktracker_connector/connector.py`.

Rules:

- **Copy, never move.** The user's original is their source of truth; leave it untouched.
- **Bring the whole asset**, not just the entry point. A connector is its code plus its config; half of it isn't migratable.
- **Never overwrite a differing copy.** On re-entry the destination may already exist. Identical content → reuse it. Different content → leave it alone and ask the user which is current.
- **Already inside the project?** Don't copy — just record the repo-relative path.

**Check for secrets before copying.** Config files for hosted connectors (`configuration.json`, `.env`, `credentials.*`, `profiles.yml`) routinely hold API keys and passwords, and `source/` is committed to git. Scan what you're about to copy for secret-shaped values — `api_key`, `password`, `token`, `secret`, long opaque strings. If you find any, do **not** copy that file. Tell the user:

> "`configuration.json` looks like it holds an API key. I've left it out of `source/` so it doesn't get committed — the connector is registered against `connector.py` alone. Add a redacted copy yourself if the config matters for the migration."

Registration reports a `sourcePath` that is absolute, escapes the project with `..`, or resolves to nothing under the project root: it lands in `warnings[]` on the registered row and `withWarnings[]` on the report. Seeing one means this step was skipped.

### Merge and register — the tool, not you

Each agent writes **only** `<project_dir>/.scai/tmp/extras/findings/<slug>.json`. Its final message is a one-line confirmation (`wrote N entries to …`), not the JSON body. Do not paste, concatenate, or rewrite those files.

1. Account for every agent you spawned before you register. A missing `<slug>.json` means that agent is still going or died — `expected_slugs` makes the tool fail rather than silently drop a category.
2. Call **one** register. Do not pass `entries`.

```
register_units(
  expected_slugs=["<slug>", ...]   // every slug you spawned
)
```

The tool reads `.scai/tmp/extras/findings/<slug>.json`, drops duplicate `customKind`+`name` pairs, registers once, and returns `registered` / `failed` / `total` plus `notes` / `skipped` / `workflowHints` / `fragments`. Those arrays **are** the merge — relay `notes` to the user from the response. Do not `query_registry` to confirm the write, and do not open the fragment files to rebuild the list.

   Two different things can be missing from an entry's `dependsOn`, and they are not handled alike. An edge the investigation **can** resolve belongs in the fragment before the agent writes it. An **ambiguous** name is not yours to settle: it lands in `notes`. Resolving an ambiguous name to every candidate is the worst answer available. Leaving the edge off and naming the choice is correct; so is asking. Re-registering a unit to attach an edge later duplicates it.

3. Relay the notes in the message the user will read, e.g.:

> "Registered 14 units across 3 customKinds. Three references I couldn't resolve: `dbo.Archive` (no registry match), `Orders` (matched 3 units), `stg.Temp` (no match). Want to point me at the right ones, or leave those edges off?"

The relay is not optional once the counts look good. The numbers come from the tool and read as complete; the unresolved names live in `notes` and must appear in the same wrap-up.

A hand-pasted list of 1–3 items still uses `register_units(entries=[...])` — no findings dir, no spawn.


### Parameter names

`register_units` takes snake_case (`custom_kind`, `source_path`, `depends_on`, `expected_slugs`) and camelCase (`customKind`, `sourcePath`, `dependsOn`, `expectedSlugs`). `dependsOn` takes a JSON array of ids or a comma/newline-separated string.

### Manifest entry shape

```json
{
  "customKind": "fivetran",
  "name": "orders_sync",
  "objectType": "other",                       // optional; one of the built-in ObjectType values
  "sourcePath": "source/fivetran/orders.yaml", // optional; MUST be repo-relative — vendor first
  "dependsOn": ["<unit-id-1>", "<unit-id-2>"], // optional; ids of registry units this asset reads/writes
  "description": "Daily ingest from Shopify",  // optional human note, stored under extensions.description
  "machine": "fivetran-flow"                   // optional; leave unset — see Step 3
}
```

`dependsOn` accepts either a JSON array of ids OR a comma/newline-separated string. Use what's natural for the user's source data.

### Resolving dependencies

When the user describes "FiveTran sync depends on `dbo.Customers`", the agent should look up the registry id of `dbo.Customers` (via `query_registry` with a `where` clause matching `source.canonicalName`), then put that id in `dependsOn`. The user shouldn't have to know unit ids.

Check `dependsOnMissing` in the response afterwards — it's the cheapest way to catch an id that was misread or truncated on the way in.

## Step 3: Write a cookbook per customKind

This is the playbook every object of that kind will run. Discovery writes it **with the customer**, one file per `customKind`, at `<project_dir>/.scai/skills/<customKind>.md`. Leave `machine` unset on the units. Do **not** write `.scai/machines/` JSON — nothing reads it.

The shape of the file, and the stamp that completes an object, are in [cookbook-template.md](cookbook-template.md). Read that before you draft. Without this file the units walk the SQL `main` pipeline, which is the wrong work.

Walk **each distinct `customKind` that just registered** (or, on re-entry, each new kind). Kinds that already have a cookbook: offer to keep it; only rewrite if they ask.

### 3a. Figure out the method — files first, then the customer

Do not start from a blank page, and do not invent a Snowflake conversion the assets do not support.

**From the assets** (already in front of you — do not re-scan every file):

- Investigation `workflowHints[]` on the **register report** (and `notes` / `skipped`). Do not open the findings files to rebuild them.
- One representative unit: open its `sourcePath` and any README / non-secret config next to it.
- What you should be able to say before asking: *what this kind is* (Connector SDK, Airflow DAG, cube, script, …), *how it is run today* if the tree says so, *what it writes*.

Tell the user that in one or two sentences, then ask. Use `ask_user_question`. Two questions per kind, not per object:

1. **Done means** — "When is one `<customKind>` finished?" Options that match what you actually saw, plus "Something else":
   - Typical: destination objects exist in Snowflake / the pipeline runs on a schedule in Snowflake / converted to a native Snowflake object (Task, Dynamic Table, …) / we will walk each one with you by hand.
2. **How** — "How should the agent migrate one of these?" Point me at a runbook, a command, or describe it in a sentence. If the files already name a tool (`fivetran deploy`, `dbt run`, …), offer that as an option.

**Wait for the user's response — do not draft until they have answered both.**

The customer wins on intent. If they say "repoint the Fivetran connectors at Snowflake" that is the cookbook, even if you could imagine a Snowpark rewrite.

If they say they only wanted the units tracked: still write a short cookbook whose Step 2 is "open the files, walk the work with the user, then stamp or escalate." That keeps them off `main`. Tell them why in one sentence.

If `<project_dir>/.scai/skills/<customKind>.md` already exists, ask keep / extend / replace before touching it.

### 3b. Draft, show, write

Draft from the hints + their answers, in the template's section order. Show the customer the plan as a short numbered list (what Step 2 will tell the dispatched agent to do). **Wait for them to accept or correct it.** Then Write the file.

The dispatched agent will reuse this file for every object of the kind, so write it in terms of `<name>`, `objectId`, and `files.source.path` — never bake in one unit's id.

If you set `machine` anyway, a name that won't resolve comes back in `warnings[]` / `withWarnings[]` (and a `Warning:` line from `update_registry(field="extensions.machine", ...)`). Read them — they mean the named machine did not take; the cookbook file still will.

`extensions.machine` holds a machine **name** as a plain string. It is not a status field.

For the contract the cookbook must satisfy, see [`../../extensibility/TASKS.md`](../../extensibility/TASKS.md) ("Per-customKind skills").

## Step 4: Mark Done

Write the completion marker the setup machine watches for, so it doesn't re-route here. Use the Write tool to create the file `<project_dir>/.scai/extras_discovered` with any short content (e.g. `ok`).

The `discoverExtras` task's `statusSource` is a filesystem glob on `.scai/extras_discovered`; the task completes as soon as that file exists. (Re-entering this skill later to add more units is safe — re-create the marker when you're done again.)

Tell the user:

> "Discover step done. <N> custom units registered across <K> customKinds. Cookbooks are at `.scai/skills/<customKind>.md` — each object of that kind will run that playbook instead of the SQL pipeline."

`<N>` and `<K>` come from the registration responses — the units the registry confirmed — not from counting the entries you assembled. Those two numbers diverge more easily than they look: the merge is where a hand tally slips, and by the time you write the wrap-up the tally feels settled. If your closing number disagrees with the list of units you just named, the list is right.

Close with what is still open, in the same message: every reference that resolved to nothing or to more than one unit, and any config file you left out for holding secrets. The counts say what landed; these are what the user has to decide, and they are the reason they are reading.

Then return to the parent setup skill.

## CHECKPOINT

Before returning, verify:
- [ ] Every category the user picked was walked through (registered, declined, or explicitly skipped).
- [ ] Where the user pointed at code, the investigation was fanned out — no serial slog through directories the orchestrator could have parallelized.
- [ ] Every investigation agent's `notes[]` was relayed to the user. Unresolved and ambiguous dependency names are decisions for them, not silent omissions.
- [ ] Every asset the user pointed at from outside the project was copied under `source/`, and no `sourcePath` is absolute or outside the project. `warnings[]` / `withWarnings[]` came back empty.
- [ ] Any config file skipped for holding secrets was named to the user, not quietly dropped.
- [ ] `migration_status(next_objects)` includes the newly registered units (or the user agreed they don't need to flow through orchestration yet).
- [ ] Each asset was registered exactly once, and the closing counts came from the registration responses rather than a hand tally.
- [ ] No `dependsOnMissing` id was left unexplained — each one is a lookup to redo, since a missing id never resolves itself.
- [ ] Every newly registered `customKind` has a cookbook at `.scai/skills/<customKind>.md`, written from the assets plus the customer's answers, in the [cookbook-template.md](cookbook-template.md) shape. Existing cookbooks were kept unless the user asked to change them. No `.scai/machines/` file was written.
- [ ] The `.scai/extras_discovered` marker is written so the setup machine moves on.

## Re-Entry

This skill is safe to re-enter at any time after setup. Users who discover more assets later can invoke it directly:

> "I found another set of custom assets — let's register them."

Don't reset existing units; only add to them. The skill should detect existing custom units (via `query_registry` with `where="kind = 'custom'"`) and offer to extend rather than restart. New `customKind`s still get a cookbook (Step 3); kinds that already have `.scai/skills/<customKind>.md` keep it unless the user asks to change it.
