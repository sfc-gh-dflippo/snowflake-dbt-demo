# Per-customKind cookbook

Discovery writes one file per `customKind` at `<project_dir>/.scai/skills/<customKind>.md`. The dispatcher loads that same file for every object of the kind. Fill it with the customer during discover-extras Step 3; do not leave a placeholder for them to write later.

## How to figure out the contents

Three inputs, in this order. The customer is the authority on *intent*; the files are the authority on *what the assets actually are*.

1. **The assets.** Investigation `workflowHints[]` plus one representative unit (open its `sourcePath`, README, and non-secret config). Record: what the kind is (SDK, DAG, cube, script), how it is run today, what it writes, any command or tool named in the tree.
2. **The customer, once per kind — not per object.** What "this object is migrated" means, and how they want the agent to get there. A runbook path, a command, or a sentence is enough.
3. **Do not invent a conversion path the files do not support.** If the assets are Fivetran Connector SDK projects, do not draft "convert to Snowpark." If you cannot tell, say so in the draft and let the customer correct it.

If the files and the customer disagree, write the customer's intent and note the tension in a short "Watch-outs" step so the dispatched agent does not paper over it.

## Shape of the file you write

A procedure the dispatched agent will follow for **one** object. Open like a procedure (On Entry → numbered steps → stamp). No overview essay. Required sections, in this order:

```markdown
---
name: <customKind>
description: Migrate one <customKind> asset. Used for every object of this kind. Triggers: migrate <customKind>, <human name for the kind>.
---

# Migrate <customKind>

This cookbook runs for **one** `<customKind>` object. The current object is in the dispatch payload (`objectId`, name, `files.source.path`). Do not walk the SQL register → convert → deploy pipeline on it.

## On Entry

Tell the user:

> **Migrating `<name>` (`<customKind>`).** <one sentence: what this kind is, from discovery.>

## Step 1: Load this object

Call `query_registry(where="id = '<objectId>'", fields=["*"])` and open `files.source.path`. Work only on this id.

## Step 2: <short name for the work, from the customer>

<The actual method. Numbered actions: commands, Snowflake objects to create or check, files to edit. Use `<name>` and the source path as placeholders — this file is reused.>

## Step 3: Record the verdict

- Succeeded → `transition_status(status='advance', task='verify', outcome='completed', where="id IN ('<objectId>')")`
- Needs a person → `transition_status(status='escalate', task='verify', where="id IN ('<objectId>')", asks=[...])`
- Out of scope, and the user agreed → `update_registry(field="inScope", status="false", objects="<objectId>")`
```

The stamp is always `verify`. That is the task the overlay machine parks on; a different task id will not complete the object.
