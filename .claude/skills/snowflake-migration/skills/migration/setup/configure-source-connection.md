---
name: configure-source-connection
description: Set up a connection to the source database (extract DDL, migrate data, run baselines). Routes to per-dialect connection skills; offers deferral or a permanent opt-out only if the user pushes back.
license: Proprietary. See License-Skills for complete terms
---

# Configure source connection

Two ways in, and they differ in whether a connection has already been agreed to:

- **From setup**, because the user chose **Extract from database** at
  `chooseCodeSource`. That answer already *is* "yes, I need a source
  connection" — don't ask again, go straight to **Set up the connection**.
- **From `generateTestCases` / `migrateData`**, whose prereq isn't met. Here the user
  has no connection and may never have wanted one, so name the capability that
  needs it and ask before setting one up.

A user importing local SQL files never reaches this skill from setup.

## Before connecting — tell the user

Before proceeding to connection setup, show the following warning **verbatim** regardless of which entry path brought the user here.

> **What this connection is used for:** This source connection will be used
> throughout the migration lifecycle for metadata extraction, DDL/code
> extraction, schema introspection, data migration reads, and validation
> queries.
>
> **Use a non-production instance.** Connect to a dev, test, or sandbox
> database — not production. Migration operations can introduce significant
> query load, long-running reads, and potential locking on the source database
> during data migration and validation phases.

## Set up the connection

Call `configure(needs_source_connection=true)` to list existing connections for
the configured dialect. Safe to repeat — it only reads.

- If `existing_connections` is non-empty, ask the user to pick one.
- Otherwise, load the per-dialect connection sub-skill:
  - `sqlserver` → `../connection/sql-server-connection/SKILL.md`
  - `redshift` → `../connection/redshift-connection/SKILL.md`
  - `oracle` → `../connection/oracle-connection/SKILL.md`
  - `teradata` → `../connection/teradata-connection/SKILL.md`
  - `postgresql` → `../connection/postgresql-connection/SKILL.md`
  - `db2` → `../connection/db2-connection/SKILL.md`
  - `bigquery` → `../connection/bigquery-connection/SKILL.md`

## If the user pushes back

Don't offer these up front on the setup path — only once the user says they
don't want to connect now, or the re-entry question above gets a "no".

**Defer for this run:**

```
progress_setup(mode="setup", skip="configureSourceConnectionExtract")
```

Nothing is persisted, so a later `progress_setup()` — or a re-entry from
`generateTestCases` / `migrateData` — can offer it again.

**Permanent opt-out:**

```
configure(tasks={"configureSourceConnectionExtract": {"enabled": false}})
```

Say what it costs first: code already in the project still converts and
deploys; extracting code from the source, tests-from-source and data migration
stay unavailable until they reconsider.

## On completion

Return to the parent setup skill once the connection is set, or the user has
deferred or opted out.
