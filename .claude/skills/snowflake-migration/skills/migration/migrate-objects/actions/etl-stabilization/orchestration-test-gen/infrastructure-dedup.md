# Infrastructure Deduplication — `_infrastructure.sql` Generation Rules

## Location

Generated once per phase at:

```
{UNIT}/stabilization/phases/phase_{N}/_infrastructure.sql
```

Where `{SCHEMA}` is a placeholder string-replaced by the orchestrator at execution time with each batch's actual schema name (e.g., `ETL_FIX_P1_B2`).

---

## Core Objects (always included)

These are included in every `_infrastructure.sql` regardless of phase content:

```sql
CREATE SCHEMA IF NOT EXISTS {SCHEMA};
USE SCHEMA {SCHEMA};

CREATE OR REPLACE TRANSIENT TABLE {SCHEMA}.control_variables (
    variable_name    VARCHAR        NOT NULL,
    variable_value   VARIANT,
    variable_type    VARCHAR        NOT NULL,
    variable_scope   VARCHAR        NOT NULL,
    is_parameter     BOOLEAN        NOT NULL DEFAULT FALSE,
    is_persistent    BOOLEAN        NOT NULL DEFAULT FALSE,
    last_updated_at  TIMESTAMP_NTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (variable_name, variable_scope)
);

CREATE OR REPLACE FUNCTION {SCHEMA}.GetControlVariableUDF(
    p_variable_name  VARCHAR,
    p_variable_scope VARCHAR
)
RETURNS VARIANT
LANGUAGE SQL
AS $$
    SELECT variable_value
    FROM {SCHEMA}.control_variables
    WHERE variable_name  = p_variable_name
      AND variable_scope = p_variable_scope
$$;

CREATE OR REPLACE PROCEDURE {SCHEMA}.UpdateControlVariable(
    p_variable_name  VARCHAR,
    p_variable_scope VARCHAR,
    p_variable_value VARIANT
)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$
BEGIN
    MERGE INTO {SCHEMA}.control_variables AS target
    USING (SELECT :p_variable_name AS variable_name, :p_variable_scope AS variable_scope) AS source
    ON target.variable_name = source.variable_name
   AND target.variable_scope = source.variable_scope
    WHEN MATCHED THEN
        UPDATE SET variable_value = :p_variable_value, last_updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (variable_name, variable_scope, variable_value, variable_type, is_parameter, is_persistent, last_updated_at)
        VALUES (:p_variable_name, :p_variable_scope, :p_variable_value, 'DYNAMIC', FALSE, FALSE, CURRENT_TIMESTAMP());
    RETURN 'OK';
END;
$$;
```

---

## Conditional Helpers (included by infrastructure tag)

The ROADMAP lists which helper tags a phase requires. Include the corresponding DDL only when the tag is present.

### Tag: `CLEAR_VARIABLES`

```sql
CREATE OR REPLACE PROCEDURE {SCHEMA}.ClearVariables(
    p_variable_scope VARCHAR
)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$
BEGIN
    DELETE FROM {SCHEMA}.control_variables
    WHERE variable_scope = :p_variable_scope
      AND is_persistent  = FALSE;
    RETURN 'OK';
END;
$$;
```

### Tag: `INIT_FROM_CONFIG`

Copy full DDL from existing test artifacts — search for `InitVariablesFromConfig` in `stabilization/tests/` and paste verbatim, replacing the schema qualifier with `{SCHEMA}`.

> **Phase 1 bootstrap:** If no prior test artifacts exist yet (first phase of a new package), use the canonical DDL from the orchestration guide's `InitVariablesFromConfig` reference section instead.

### Tag: `BUILD_DBT_VARS`

Copy full DDL from existing test artifacts — search for `BuildDbtVarsJsonUDF` in `stabilization/tests/` and paste verbatim, replacing the schema qualifier with `{SCHEMA}`.

> **Phase 1 bootstrap:** If no prior test artifacts exist yet, use the canonical DDL from the orchestration guide's `BuildDbtVarsJsonUDF` reference section instead.

---

## Execution

The orchestrator:

1. Reads `_infrastructure.sql` once per phase.
2. String-replaces `{SCHEMA}` with each batch's actual schema name (e.g., `ETL_FIX_P1_B2`).
3. Executes the resulting SQL via a single `snowflake_sql_execute` call (multi-statement) before spawning the batch agent.
4. Batch agents can assume all core objects already exist in their `{TASK_SCHEMA}`.

Tasks execute in parallel; each receives its own substituted copy — there is no shared mutable state.

---

## What belongs in `ARRANGE:SETUP` vs `_infrastructure.sql`

| Belongs in `_infrastructure.sql`           | Belongs in `ARRANGE:SETUP`                            |
|--------------------------------------------|-------------------------------------------------------|
| `control_variables` table                  | Mock source/target tables specific to the element     |
| `GetControlVariableUDF`                    | Cross-schema references (stubs, synonyms)             |
| `UpdateControlVariable`                    | Stub procedures that the ACT section calls            |
| `ClearVariables` (if tagged)               | Any DDL not shared across all tasks in the phase      |
| `InitVariablesFromConfig` (if tagged)      |                                                       |
| `BuildDbtVarsJsonUDF` (if tagged)          |                                                       |

`ARRANGE:SEED` always stays in each test file (TRUNCATE + INSERT are element-specific).

---

## Why This Matters

Eliminates ~500 tokens of identical DDL per test file and ~3.7 seconds of redundant Snowflake DDL per test execution.
