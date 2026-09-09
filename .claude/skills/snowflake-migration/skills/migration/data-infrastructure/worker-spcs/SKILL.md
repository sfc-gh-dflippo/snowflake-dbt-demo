---
name: worker-spcs
description: Deploy the Data Exchange Worker on Snowpark Container Services (SPCS) — image selection, Snowflake Secrets, CREATE SERVICE SQL generation, and verification. Triggers: SPCS worker, container worker, snowpark container, deploy worker SPCS, spcs deployment.
parent_skill: data-infrastructure-setup
license: Proprietary. See License-Skills for complete terms
---

# Worker Setup — SPCS

Deploy the Data Exchange Worker as a Snowpark Container Services (SPCS) service. SPCS automatically provides Snowflake authentication via `@SPCS_CONNECTION` — no Snowflake credentials are needed in the service spec.

> Run worker instances on a compute pool that will stay **active** for the full migration. SPCS automatically restarts instances if they stop.

## Step 1 — Image Version

The worker image version is **pinned to your `scai` CLI release** — do not use `SHOW IMAGES` to pick the latest tag, as it may be incompatible with this version of the CLI.

Get the pinned version by running the setup command (it logs the image it would use):

```bash
scai data worker setup --compute-pool <compute_pool>
```

The CLI logs: `Using pinned Data Exchange Worker image: /snowflake/images/snowflake_images/data-exchange-worker:<version>`

Record that exact version tag (e.g., `1.11.1`). Use it as `<version>` in all subsequent steps. If the setup command succeeds and creates the SPCS service automatically, **you are done** — skip to Step 5 (Verify and Remind). Only continue through the remaining steps if you need to customize the service spec (e.g., to set a custom compute pool instance size or add external access integrations).

**Note:** The image tag is a version number (e.g., `1.12.0`), not a platform identifier. The source database type is controlled by the `DATA_SOURCE_TYPE` environment variable. Read it from the project's scai source connection:

| Source system | `DATA_SOURCE_TYPE` |
|---------------|--------------------| 
| SQL Server    | `sqlserver`        |
| Redshift      | `redshift`         |
| Oracle        | `oracle`           |
| Teradata      | `teradata`         |
| PostgreSQL    | `postgresql`       |

## Step 2 — Affinity Label

**In all steps below, substitute every `<placeholder>` token with its actual value — never output a literal `<placeholder>` string. Key substitutions:**
- `<label>` — the affinity label confirmed in this step
- `<project>` — slug derived the same way as `<label>`, used for naming secrets
- `<version>` — the image version from Step 1
- `<compute_pool>` — from the compute pool configured in the parent skill's Question 0
- `<source_type>`, `<host>`, `<port>`, `<database>` — from the project's scai source connection
- `<warehouse>` — from the parent skill's Question 2
- `<replica_count>` — the instance count the user provides in Step 4
- `<driver-download-host>` — **(Oracle/Teradata only)** the hostname of the NuGet driver download endpoint; ask the user for this value if they are on Oracle or Teradata

Affinity binds this worker to the workflow it should process — see the [Affinity Reference](../references/affinity-reference.md) for the model (and why the orchestrator stays null-affinity). The automatic `scai data worker setup` path uses the project's stable default. The custom service-spec path below needs an explicit label because `AGENT_AFFINITY` must exactly match the workflow.

Propose a short, stable label for this source database/server, for example `mdx-salesnorth`.

Tell the user:

> This custom worker needs an explicit affinity label. Proposed label: **`<label>`**. I will set it once with `configure(affinity="<label>")` and use the same value as the worker's `AGENT_AFFINITY`. Confirm or provide a different label.

Wait for the user to confirm or override, then set it: `configure(affinity="<label>")`. **Note the final label — it is used in Steps 4 and 5 as `AGENT_AFFINITY`; it must equal the workflow affinity.**

## Step 3 — Snowflake Secrets for Source Credentials

SPCS uses `@SPCS_CONNECTION` for Snowflake authentication automatically. You only need to create Snowflake Secrets for the **source database credentials**.

Ask the user if they already have Snowflake Secrets for the source database username and password.

| Answer | Action |
|--------|--------|
| **Already have secrets** | Note the secret names — they are referenced in Step 4. Continue to the Oracle/Teradata check below. |
| **Need to create them** | Run the SQL below in a Snowflake session, then wait for the user to confirm the secrets were created. |

```sql
CREATE SECRET <project>_SOURCE_USERNAME
  TYPE = GENERIC_STRING
  SECRET_STRING = '<username>';

CREATE SECRET <project>_SOURCE_PASSWORD
  TYPE = GENERIC_STRING
  SECRET_STRING = '<password>';
```

Substitute `<username>` with the source database username. For `<password>`: **do not ask the user to type the password in the chat** — instruct them to fill it directly into the SQL statement in their Snowflake session before running it.

Note the exact secret names — they are referenced in Step 4.

**Wait for the user to confirm the secrets are created before continuing.**

> **Non-SPCS / local workers:** Snowflake Secrets above apply to SPCS container services only. For external vaults, AWS Secrets Manager REST providers, or `$(...)` command substitution in worker TOML, see [Advanced: Secrets management](../references/worker-config-reference.md#advanced-secrets-management).

**Oracle and Teradata only:** The container requires outbound network access for two destinations: the source database host and the NuGet driver download endpoint. Ask the user to provide an `EXTERNAL_ACCESS_INTEGRATION` covering both. If they do not have one, show:

```sql
CREATE NETWORK RULE <project>_DRIVER_EGRESS
  TYPE = HOST_PORT
  MODE = EGRESS
  VALUE_LIST = ('<driver-download-host>:443', '<host>:<port>');

CREATE EXTERNAL ACCESS INTEGRATION <project>_DRIVER_ACCESS
  ALLOWED_NETWORK_RULES = (<project>_DRIVER_EGRESS)
  ENABLED = TRUE;
```

Where `<host>` and `<port>` are the source database host and port from the project's scai source connection.

Note the integration name — it is appended to the `CREATE SERVICE` statement in Step 4.

**Wait for the user to confirm the integration is ready before continuing.**

## Step 4 — Generate and Run CREATE SERVICE SQL

Ask the user how many worker instances they want. Recommend 2–3 for most migrations. `MAX_PARALLEL_TASKS` defaults to `4` — the user may adjust this based on their source system's capacity.

Show the complete `CREATE SERVICE` statement assembled from the project values and **wait for user confirmation before executing**:

```sql
CREATE SERVICE SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_SERVICE
  IN COMPUTE POOL <compute_pool>
  FROM SPECIFICATION $$
    spec:
      containers:
        - name: agent
          image: snowflake/images/snowflake_images/data-exchange-worker:<version>
          env:
            DATA_SOURCE_TYPE: <source_type>
            DATA_SOURCE_HOST: <host>
            DATA_SOURCE_PORT: <port>
            DATA_SOURCE_DATABASE: <database>
            SNOWFLAKE_WAREHOUSE: <warehouse>
            MAX_PARALLEL_TASKS: 4
            AGENT_AFFINITY: <label>
          resources:
            requests:
              memory: 10G
              cpu: 6
            limits:
              memory: 10G
              cpu: 6
          secrets:
            - snowflakeSecret: <project>_SOURCE_USERNAME
              envVarName: DATA_SOURCE_USERNAME
            - snowflakeSecret: <project>_SOURCE_PASSWORD
              envVarName: DATA_SOURCE_PASSWORD
  $$
  MIN_INSTANCES = <replica_count>
  MAX_INSTANCES = <replica_count>;
```

**Resource sizing:** The `memory: 10G / cpu: 6` values above match the `CPU_X64_M` instance family. Adjust to match your actual compute pool instance family — larger instance families support higher values.

**Oracle/Teradata:** Add `EXTERNAL_ACCESS_INTEGRATIONS = (<project>_DRIVER_ACCESS)` on the line before `MIN_INSTANCES`.

After the user confirms, instruct them to run the statement in a Snowflake session.

## Step 5 — Verify and Remind

Check service status:

```sql
SELECT SYSTEM$GET_SERVICE_STATUS('SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_SERVICE');
```

Confirm all instances show `READY`. If any instance is not ready after a few minutes, check logs:

```sql
SELECT SYSTEM$GET_SERVICE_LOGS('SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_SERVICE', 0, 'agent', 100);
```

**Wait for all instances to reach `READY` status before continuing.**

Then tell the user:

> **Important:** When you configure your migration workflow, set the affinity to **`<label>`**. Without this, the orchestrator will not route tasks to your workers.
>
> To check worker status at any time:
> ```sql
> SELECT SYSTEM$GET_SERVICE_STATUS('SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_SERVICE');
> ```

## Done

The SPCS worker service is deployed and all instances are READY. Return control to the parent skill, which runs Level 1 Data Doctor before proceeding.
