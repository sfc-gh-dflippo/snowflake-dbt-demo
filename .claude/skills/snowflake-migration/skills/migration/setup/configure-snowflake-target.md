---
name: configure-snowflake-target
description: Set the Snowflake target for object migration — connection name and database — then confirm the whole project configuration before the deploy loop starts. Persists via `configure(snowflake_connection=…, snowflake_database=…)`.
license: Proprietary. See License-Skills for complete terms
---

# Configure Snowflake target

Invoked by the setup state machine once the user has opted into object
migration at the `continueToMigration` gate. Conversion and assessment
have already run — they don't need a Snowflake target, which is why this
question waits until now.

## Step 1: Snowflake connection

Call `configure()` (no arguments) and read `snowflake_connection` from the
response.

- **Non-empty** — a connection is already resolved (from
  `project.local.yml` or `$SNOWFLAKE_CONNECTION`). Confirm rather than
  re-ask:
  > I'll deploy through the Snowflake connection `<name>`. Use it?
- **Empty** — you have an active Snowflake connection in this session.
  Propose it by name:
  > I'll deploy through your active Snowflake connection `<name>`. Use it,
  > or would you rather name a different one?

If the user wants a different connection, ask for the name and use it.

If they still need a Snowflake connection created, or the current one fails
SSO against Microsoft Entra ID / Azure AD / OIDC, load
`../connection/snowflake-connection/SKILL.md` before persisting a name.
Use `oauth_authorization_code` for Entra OIDC — never `externalbrowser`.

## Step 2: Target database

This is where the migration tracking database and the converted objects
will live. Read `snowflake_database` from the same `configure()` response:

- **Already set** — confirm it in the recap below; don't re-ask.
- **Empty but the connection has a default database** — the `configure()`
  response reports it as the effective database. Offer it:
  > Deploy into `<db>` (your connection's current database)?
- **Empty with no default** — ask:
  > Which Snowflake database should I deploy into?

## Step 3: Confirm everything, then persist

Show one recap covering every value the migration phase depends on, pulled
from the `configure()` response:

> Before we start deploying, here's the setup:
> - **Snowflake connection:** `<snowflake_connection>`
> - **Target database:** `<snowflake_database>`
> - **Source connection:** `<source_connection>` — or "none (synthetic test
>   data only)" when unset
> - **Source dialect:** `<source_language>`
> - **Git branch:** `<git_main_branch>`
>
> Correct?

Ask via `ask_user_question` (`multiSelect = false`) with **Yes, continue**
and **Change something**. On "Change something", ask which value and loop
back to the relevant step. Only once the user confirms, persist both
values in a single call:

```
configure(snowflake_connection="<name>", snowflake_database="<db>")
```

## Step 4: Handle a missing database

The `configure()` response now carries `schema_status_*` and
`prereq_status_*` lines. Only one matters here — the rest are checked by
`configure-testing.md`:

- `schema_status_validation: database_missing` → the configured database
  does not exist. **Ask before creating it** — the name may be a typo:
  > `<db>` doesn't exist yet. Create it, or did you mean a different name?

  On confirmation run `CREATE DATABASE <snowflake_database>;`, then
  `configure(ensure_metadata_schema=true)` to refresh.

## If the user won't name a database

Don't block and don't error. Conversion and assessment are already
complete and committed; the target can be named later. Tell the user the
deploy loop needs a current database and stop here:

> No problem — assessment is done and committed. I'll need a target
> database before deploying anything, so say the word when you've picked
> one.

## On completion

Return to the parent setup skill. The resolver will pick the next task.
