# Informatica XML Navigation Guide — Workflows and Sessions

Reference for navigating Informatica PowerCenter XML exports to extract workflow and session structure for orchestration test generation.

## XML Hierarchy

Informatica PowerCenter exports use a `POWERMART` root element:

```
POWERMART
└── REPOSITORY
    └── FOLDER
        ├── SOURCE (source table definitions)
        ├── TARGET (target table definitions)
        ├── MAPPING (data transformation pipelines)
        │   ├── TRANSFORMATION (Source Qualifier, Expression, Filter, etc.)
        │   ├── INSTANCE (runtime references to transformations)
        │   ├── CONNECTOR (port-to-port wiring between instances)
        │   └── TARGETLOADORDER
        ├── CONFIG (session configuration)
        ├── WORKFLOW (orchestration — execution order)
        │   ├── TASK (individual executable units: Session, Timer, Command, etc.)
        │   └── WORKFLOWLINK (execution dependencies between tasks)
        └── SESSION (runtime config binding a workflow task to a mapping)
            └── SESSTRANSFORMATIONINST (per-transformation runtime overrides)
```

## Finding Workflows

Workflows are `WORKFLOW` elements inside a `FOLDER`. Each workflow contains `TASK` elements and `WORKFLOWLINK` elements defining execution order.

```xml
<WORKFLOW NAME="w_DailyLoad" ... ISENABLED="YES" ...>
  <TASK NAME="Start" TYPE="Start" REUSABLE="NO" .../>
  <TASK NAME="s_mapping_customers" TYPE="Session" REUSABLE="NO" ...>
    <ATTRIBUTE NAME="Mapping Name" VALUE="m_CustomerLoad"/>
    <!-- Connection attributes, error handling, etc. -->
  </TASK>
  <TASK NAME="s_mapping_orders" TYPE="Session" REUSABLE="NO" .../>
  <TASK NAME="cmd_notify" TYPE="Command" REUSABLE="NO" ...>
    <ATTRIBUTE NAME="Command" VALUE="echo 'Load complete'"/>
  </TASK>
  <WORKFLOWLINK FROMTASK="Start" TOTASK="s_mapping_customers" CONDITION=""/>
  <WORKFLOWLINK FROMTASK="s_mapping_customers" TOTASK="s_mapping_orders" CONDITION="$s_mapping_customers.Status = SUCCEEDED"/>
  <WORKFLOWLINK FROMTASK="s_mapping_orders" TOTASK="cmd_notify" CONDITION=""/>
</WORKFLOW>
```

### Key Attributes

| Element | Key Attributes | Purpose |
|---------|---------------|---------|
| `WORKFLOW` | `NAME`, `ISENABLED` | Workflow identity; `ISENABLED="NO"` means disabled |
| `TASK` | `NAME`, `TYPE`, `REUSABLE` | Individual task; `TYPE` determines behavior |
| `WORKFLOWLINK` | `FROMTASK`, `TOTASK`, `CONDITION` | Execution dependency + optional condition |

### Task Types

| TYPE Value | Description | Snowflake Equivalent |
|------------|-------------|---------------------|
| `Start` | Entry point — every workflow has exactly one | Root TASK (no AFTER clause) |
| `Session` | Executes a mapping | `EXECUTE DBT PROJECT` or `CREATE TASK` |
| `Command` | Shell command / OS script | `EXECUTE IMMEDIATE` or external dependency |
| `Timer` | Wait/delay between tasks | Not directly supported — EWI emitted (`SSC-EWI-INF0003`) |
| `Email` | Send notification email | `SYSTEM$SEND_EMAIL` or external dependency |
| `Control` | Stop/abort workflow | Error handling |
| `Assignment` | Set variable value | Variable assignment |
| `Decision` | Conditional routing | Conditional task chaining |

### Worklets (Reusable Sub-Workflows)

Worklets are reusable workflow containers that encapsulate a group of tasks and workflow links. They can be embedded in multiple parent workflows.

**How worklets expand:** When a workflow references a worklet, the worklet's internal tasks are **flattened into the parent workflow's task DAG**:

- Each worklet task becomes a Snowflake TASK with a name prefixed by the parent workflow and worklet instance name
- Worklet-internal `WORKFLOWLINK` edges are preserved as `AFTER` clauses
- The worklet's Start task connects to the parent's preceding task
- The worklet's final task(s) connect to the parent's next task

```
Parent Workflow:
  Start → s_load_dims → [wklt_validation] → s_load_facts

Expanded (Snowflake TASKs):
  w_Daily_s_load_dims
    → w_Daily_wklt_validation_s_check_nulls
    → w_Daily_wklt_validation_s_check_refs
    → w_Daily_s_load_facts
```

**Worklet parameters:** Worklets can accept parameters that override mapping variables or session attributes. These appear as `ATTRIBUTE` elements on the worklet `TASK` instance within the parent workflow.

**Task naming convention:** Converted task names follow the pattern `{workflow}_{worklet_instance}_{task_name}` to ensure uniqueness across the parent DAG.

## Conversion Output Structure

Informatica workflows convert to **Snowflake TASK chains**:

```sql
-- Root task (from Start)
CREATE OR REPLACE TASK public.w_DailyLoad AS SELECT 1;

-- Session tasks (from TASK TYPE="Session")
CREATE OR REPLACE TASK public.w_DailyLoad_s_mapping_customers
  WAREHOUSE=DUMMY_WAREHOUSE
  AFTER public.w_DailyLoad
AS BEGIN
  EXECUTE DBT PROJECT public.m_CustomerLoad ARGS='build --target dev';
END;

-- Chained task (from WORKFLOWLINK)
CREATE OR REPLACE TASK public.w_DailyLoad_s_mapping_orders
  WAREHOUSE=DUMMY_WAREHOUSE
  AFTER public.w_DailyLoad_s_mapping_customers
AS BEGIN
  EXECUTE DBT PROJECT public.m_OrderLoad ARGS='build --target dev';
END;
```

## Execution Dependencies (WORKFLOWLINK)

`WORKFLOWLINK` defines the DAG edges:

- `FROMTASK` → `TOTASK` with optional `CONDITION`
- Conditions reference task status: `$TaskName.Status = SUCCEEDED`
- No condition means unconditional execution
- Multiple links from one task create parallel branches
- Multiple links to one task create a join point (all predecessors must complete)

## Session Configuration

`SESSION` elements bind workflow tasks to mappings and contain runtime config:

```xml
<SESSION NAME="s_mapping_customers" ...>
  <SESSTRANSFORMATIONINST TRANSFORMATIONNAME="SQ_Customer" TRANSFORMATIONTYPE="Source Qualifier" ...>
    <ATTRIBUTE NAME="Sql Query" VALUE="SELECT * FROM customers WHERE active = 1"/>
  </SESSTRANSFORMATIONINST>
  <!-- Connection overrides, error handling, pre/post-session SQL -->
</SESSION>
```

### Critical Session Attributes

| ATTRIBUTE NAME | Informatica Behavior | Snowflake / dbt Equivalent |
|----------------|---------------------|---------------------------|
| `Commit Interval` | Commits after N rows during target load | dbt transaction boundaries (Snowflake auto-commits DDL; DML within stored procedures uses explicit `BEGIN`/`COMMIT`) |
| `Stop On Errors` | Threshold of errors before session aborts (e.g., `0` = stop on first error) | Task error handling — `SUSPEND_TASK_AFTER_NUM_FAILURES` on Snowflake TASK |
| `Pre SQL` | SQL executed once before session starts | dbt `+pre-hook` at model or folder level |
| `Post SQL` | SQL executed once after session completes | dbt `+post-hook` at model or folder level |
| `Sql Query` | Override on Source Qualifier — replaces table-based query | Appears in the dbt staging model's `FROM` clause (see Source Qualifier SQL Overrides below) |
| `$PMSessionLogDir` | Directory for session log files | Snowflake provides `TASK_HISTORY`, `QUERY_HISTORY`, and `EVENT TABLE` for observability |
| `$PMBadFileDir` | Directory for rejected/error row files | Snowflake `COPY INTO ... VALIDATION_MODE` + error tables |
| `Recovery Strategy` | Restart or Resume from checkpoint after failure | Snowflake TASK retry with `SUSPEND_TASK_AFTER_NUM_FAILURES` — no checkpoint-based resume |

### Source Qualifier SQL Overrides

When `ATTRIBUTE NAME="Sql Query"` exists inside a `SESSTRANSFORMATIONINST` for a Source Qualifier:

- **Takes precedence** over the table-based source definition in the `TRANSFORMATION` element
- The override SQL appears directly in the dbt staging model's `FROM` clause
- May contain complex `WHERE`, `JOIN`, or subquery logic **not visible** in the `TRANSFORMATION` element
- Always check the `SESSION` element, not just `TRANSFORMATION`, when tracing source SQL

```xml
<SESSION NAME="s_mapping_customers" ...>
  <SESSTRANSFORMATIONINST TRANSFORMATIONNAME="SQ_Customer"
    TRANSFORMATIONTYPE="Source Qualifier" ...>
    <!-- This override replaces the default "SELECT * FROM Customers" -->
    <ATTRIBUTE NAME="Sql Query"
      VALUE="SELECT c.*, o.last_order_date FROM customers c LEFT JOIN order_summary o ON c.id = o.customer_id WHERE c.active = 1"/>
  </SESSTRANSFORMATIONINST>
</SESSION>
```

## Disabled Detection

| Level | Check | Meaning |
|-------|-------|---------|
| Workflow | `ISENABLED="NO"` on `WORKFLOW` | Entire workflow disabled |
| Task | `ISENABLED="NO"` on `TASK` | Individual task disabled |
| Mapping-level | `ENABLED="NO"` on transformation instance | Transformation disabled within mapping |

## Variables and Parameters

Informatica uses `$$variable` syntax for mapping variables and parameters:

```xml
<MAPPINGVARIABLE NAME="$$m_LastLoadDate" DATATYPE="date/time"
  DEFAULTVALUE="01/01/1900 00:00:00" DESCRIPTION=""
  ISEXPRESSIONVARIABLE="NO" ISPARAM="NO"
  USERDEFINED="YES" AGGFUNCTION="MAX"/>
```

| Property | Description |
|----------|-------------|
| `AGGFUNCTION` | How the variable persists across sessions: `MAX`, `MIN`, `COUNT` |
| `ISPARAM` | If `YES`, value is set externally (parameter file) |
| `DEFAULTVALUE` | Initial value on first run |

## Connection Objects

Database connections appear as `DBCONNECTION` elements or are referenced by name in session attributes:

| Reference | Meaning |
|-----------|---------|
| `$Source` | Default source connection (maps to dbt source) |
| `$Target` | Default target connection (maps to Snowflake) |
| Named (e.g., `EDWLOAD`) | Custom connection — EWI `SSC-EWI-INF0038` emitted |
