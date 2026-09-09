# How to Write Informatica Workflow Analysis

This guide defines how to write comprehensive, actionable AI analysis for Informatica PowerCenter workflows being assessed for migration to Snowflake.

---

## Context: SnowConvert AI Migration

SnowConvert AI processes Informatica PowerCenter workflows and converts them to Snowflake-native components. The conversion target depends on `informatica_target` (set by the parent skill):

### dbt mode (`informatica_target: dbt`)

| Informatica Component | Snowflake Target | Technology |
|----------------------|------------------|------------|
| **Workflow (Control Flow)** | [Snowflake Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) | Snowflake Scripting |
| **Mappings (Data Flow)** | dbt Projects | dbt models running on Snowflake |
| **Sessions** | Snowflake Tasks calling dbt | Orchestration layer |

### scripting mode (`informatica_target: scripting`)

| Informatica Component | Snowflake Target | Technology |
|----------------------|------------------|------------|
| **Workflow (Control Flow)** | [Snowflake Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) | Snowflake Scripting |
| **Mappings (Data Flow)** | Snowflake Stored Procedures | Snowflake Scripting (inline SQL) |
| **Sessions** | Snowflake Tasks with CALL statements | Orchestration layer |

### Critical Understanding

**SnowConvert will process all workflows**, but the analysis must identify external connectivity requirements.

**dbt mode:** dbt projects on Snowflake cannot directly connect to external sources — data must already exist in Snowflake.

**scripting mode:** Stored procedures operate on data already in Snowflake — external sources still require ingestion solutions.

In both modes:
- **Ingestion workflows** require attention to identify external connector solutions
- **Workflows with transformations on internal sources** have straightforward conversion paths
- **Mixed workflows** require analysis to separate what converts directly vs. what needs connector solutions

### External Connector Solutions

When a workflow performs ingestion from external sources, identify the source type and recommend appropriate solutions:

| Source Type | Recommended Solution |
|-------------|---------------------|
| **Cloud Services** (Google Services, ServiceNow, Salesforce, etc.) | Snowpark Python connectors, Fivetran managed connectors |
| **APIs / REST endpoints** | Snowpark Python with External Access Integration |
| **File-based** (CSV, Excel, JSON from cloud storage) | Snowpipe, External Stages |
| **File-based** (local/network shares) | Snowflake Openflow, custom orchestration |
| **External databases** (Oracle, MySQL, PostgreSQL, DB2, Teradata) | Fivetran, Snowflake Openflow, Airflow with custom operators |
| **FTP/SFTP servers** | Airflow orchestration, custom Python scripts |

---

## Your Task

Using the workflow information from the ETL.Elements.csv report and the source XML file, write an AI analysis that:

1. **Classifies** the workflow based on its actual logic, purpose and data flow patterns
2. **Describes** the workflow structure, sources, targets, and logic
3. **Identifies** external connectivity requirements and recommends connector solutions

---

## What to Read from XML Files

When analyzing an Informatica PowerCenter XML file, look for these elements:

### Workflow Level (Control Flow)
- `<WORKFLOW>` — the top-level orchestration unit
- `<SESSION>` — references to mappings within the workflow
- `<TASKINSTANCE>` — tasks (Timer, Command, Decision, Assignment, Email, etc.)
- `<WORKFLOWLINK>` — execution order (predecessors/successors)

### Mapping Level (Data Flow)
- `<MAPPING>` — a data pipeline from sources to targets
- `<SOURCE>` elements with `DATABASETYPE` attribute — identifies source database type (Oracle, DB2, Teradata, Flat File, ODBC)
- `<TARGET>` elements with `DATABASETYPE` attribute — identifies target database type
- `<TRANSFORMATION>` elements with `TYPE` attribute:
  - `Source Qualifier` — entry point, may have `Sql Query` override
  - `Expression` — calculated fields (look at `EXPRESSION` attributes on TRANSFORMFIELD)
  - `Lookup Procedure` — may have `Lookup Sql Override` (external joins)
  - `Filter` — row filtering (look at `Filter Condition`)
  - `Joiner` — joins between data streams
  - `Aggregator` — GROUP BY operations
  - `Update Strategy` — INSERT/UPDATE/DELETE logic
  - `Router` — conditional routing (like CASE)
  - `Sorter` — sorting
  - `Sequence` — sequence generation
  - `Stored Procedure` — calls to external stored procs
  - `Custom Transformation`, `Java Transformation` — custom code (HIGH complexity)
  - `HTTP Transformation` — external API calls (INGESTION indicator)

### Session Configuration
- `<SESSIONEXTENSION>` — connection info
- `<ATTRIBUTE NAME="Connection Name">` — identifies database connections
- `<CONFIGREFERENCE>` — session config references

---

## Classification Categories

### Data Transformation

**Definition:** Processes data that already exists within the data platform, applying business logic to move data between internal layers.

**Classification Requirement:** You MUST analyze all available workflow information to classify as Data Transformation. Base your classification on concrete evidence found in:
- `<SOURCE>` and `<TARGET>` elements with their `DATABASETYPE` attributes
- `<TRANSFORMATION>` elements and their `TYPE` attributes
- Expression transformation formulas (`EXPRESSION` attributes on TRANSFORMFIELD)
- Lookup transformations and any `Lookup Sql Override` values
- Session connection configurations (`<SESSIONEXTENSION>`, connection names)
- Workflow structure (`<WORKFLOWLINK>` dependencies, task types)

**Why classify as Data Transformation:**

A workflow is Data Transformation when the primary purpose is to **transform, enrich, aggregate, or restructure data** that is already inside the data warehouse ecosystem. The key distinction is that **both source and target are internal database objects** — no external system connectivity is required.

This classification applies when you observe in the workflow analysis (mapping logic, transformation types, source/target definitions, session configurations):

1. **Internal-to-internal data movement:** SOURCE elements reference internal database tables. TARGET elements are warehouse tables. DATABASETYPE is consistent (same platform or known internal).

2. **Business logic in mappings:** Expression transformations with complex formulas, Lookup transformations joining dimension tables, Aggregator transformations for rollups, Router transformations for conditional processing, Update Strategy for SCD patterns.

3. **Dimensional modeling patterns:** Mappings build dimensions (SCD Type 1/2), fact tables, or aggregation layers.

4. **No external connection indicators:** All sources/targets reference the same database platform or known internal schemas.

**SnowConvert Outcome:**
- Workflow → Snowflake Tasks
- Mappings → dbt models (dbt mode) / Stored procedures (scripting mode)
- **Excellent conversion candidate** in both modes

---

### Ingestion

**Definition:** Extracts data from external sources into the data platform.

**Classification Requirement:** You MUST analyze all available workflow information to classify as Ingestion. Look for evidence in `<SOURCE>` elements with external DATABASETYPE values (Flat File, ODBC to non-warehouse databases), HTTP Transformations, Stored Procedure calls to external systems, session connection configurations referencing external servers, and file-based source patterns.

**Why classify as Ingestion:**

A workflow is Ingestion when the primary purpose is to **bring data INTO the data platform from an external source**. The defining characteristic is that **the source exists outside the data warehouse** — it could be files, APIs, FTP servers, external databases, or cloud services.

This classification applies when you observe in the workflow analysis (mapping logic, transformation types, source/target definitions, session configurations):

1. **External source connections:** SOURCE elements with DATABASETYPE pointing to external systems (Flat File, FTP, ODBC to non-warehouse databases, HTTP).

2. **File-based sources:** Source Qualifier transformations reading from flat files, XML files, or other file formats.

3. **Minimal transformation logic:** Mappings primarily move data with type conversions but no complex business rules.

4. **HTTP Transformations or Stored Procedure calls to external systems.**

**SnowConvert Outcome:**
- Workflow → Snowflake Tasks
- Mappings → dbt projects (dbt mode) / Stored procedures (scripting mode) — but external sources need connector alternatives
- **Requires external connector solution** — identify source type and recommend approach
- Pure ingestion workflows (minimal transformation) may be better served by dedicated connector solutions rather than converted output

---

### Configuration & Control

**Definition:** Orchestrates processes, manages metadata, or performs system operations without directly moving business data.

**Classification Requirement:** You MUST analyze all available workflow information to classify as Configuration & Control. Look for evidence in `<TASKINSTANCE>` types (Command, Timer, Decision, Assignment, Email), workflow link structure showing orchestration patterns, minimal or no `<MAPPING>` elements, and session configurations indicating coordination rather than data movement.

**Why classify as Configuration & Control:**

A workflow is Configuration & Control when the primary purpose is to **coordinate, orchestrate, or manage other processes** rather than move or transform business data directly. These workflows are the "conductors" of the ETL orchestra.

This classification applies when you observe in the workflow analysis (workflow structure, task types, session configurations):

1. **Workflow-level orchestration:** Multiple sessions chained with decisions, timers, or conditional links.

2. **Command tasks:** Shell commands for file management, cleanup, or triggers.

3. **No mappings or minimal utility mappings:** The workflow's value is in orchestration logic (start/stop timing, conditional execution, failure handling).

4. **Assignment/Decision tasks:** Variable manipulation and conditional branching for control flow.

5. **Email tasks:** Notification workflows.

**SnowConvert Outcome:**
- Workflow → Snowflake Tasks with procedural Snowflake Scripting
- Command tasks → Stored procedures or external orchestration
- **May require Airflow** for complex orchestration patterns

---

### Mixed: Ingestion + Transformation

**Definition:** Workflow performs both ingestion from external sources AND applies significant transformations.

**Classification Requirement:** You MUST analyze all available workflow information to classify as Mixed. Look for evidence of both external source connections (in SOURCE elements, session configurations) AND significant business logic transformations (in Expression, Lookup, Aggregator, Router transformations) within the same workflow.

**Why classify as Mixed:**

A workflow is Mixed when it **combines ingestion and transformation in a single workflow**. This is common in legacy Informatica designs where a single workflow does "everything" — extracts from external source, cleanses, transforms, and loads to final destination.

This classification applies when you observe in the workflow analysis (mapping logic, transformation types, source/target definitions, session configurations):

1. **External sources feeding into transformation logic:** Mappings read from external sources but then apply significant business logic (joins, lookups, aggregations) before writing to targets.

2. **Multiple mappings with different source types:** Some mappings read from external sources (ingestion), while others read from internal staging tables (transformation).

3. **Sessions that load then transform:** The workflow loads data from external source to staging, then subsequent sessions perform significant transformation logic on that staged data.

**SnowConvert Outcome:**
- **Partial candidate** — transformation portions can convert, ingestion cannot
- **dbt mode:** Recommend architectural separation: ingestion via Fivetran/Airflow, transformation via dbt models
- **scripting mode:** Recommend architectural separation: ingestion via Fivetran/Airflow, transformation via stored procedures
- Analysis should clearly identify which components are convertible vs. which need alternatives

---

## Analysis Structure (MANDATORY)

**All analyses MUST follow this exact format.** Each section must be a separate paragraph with the section header followed by a colon. This format is required for validation and consistency.

```
Classification: [Category]. [Detailed explanation WHY based on specific evidence from the workflow XML — transformation types found, source/target database types, session configurations, etc. Must be specific to THIS workflow.]

Sources & Destinations: [List the actual SOURCE and TARGET definitions found in the XML. State database types. Identify if INTERNAL or EXTERNAL.]

Purpose: [Business purpose — what does this workflow accomplish, what business domain does it serve, who depends on it.]

Conversion: [Assessment of conversion readiness — what converts directly, what needs alternatives, specific risks from custom transformations or SQL overrides. Frame in terms of the active conversion target: use "dbt models" if dbt mode, "stored procedures" if scripting mode.]
```

**Format Requirements:**
1. Each section header must start at the beginning of a paragraph: `Classification:`, `Sources & Destinations:`, `Purpose:`, `Conversion:`
2. Sections must be separated by blank lines (paragraph breaks)
3. Total analysis should be 150-300 words

---

## Writing Guidelines

### Identify Source Types from XML

Look at `<SOURCE>` elements:
- `DATABASETYPE="Oracle"` + internal schema → **INTERNAL**
- `DATABASETYPE="Flat File"` → **EXTERNAL** (file-based ingestion)
- `DATABASETYPE="ODBC"` → Check DBDNAME for external vs internal
- `DATABASETYPE="DB2"` / `DATABASETYPE="Teradata"` → Could be internal source being migrated

### Look for Custom Code Indicators

These increase complexity:
- `<TRANSFORMATION TYPE="Custom Transformation">` — manual rewrite needed
- `<TRANSFORMATION TYPE="Java Transformation">` — manual rewrite needed
- `Sql Query` attribute on Source Qualifier with complex SQL
- `Lookup Sql Override` with complex joins
- `<TRANSFORMATION TYPE="Stored Procedure">` — external dependency

### Recognize Transformation Patterns

- Expression transformations with business formulas → Data Transformation
- Multiple Lookup transformations → dimensional enrichment
- Aggregator + Sorter → reporting/analytics pipeline
- Update Strategy → SCD or incremental load patterns
- Router → conditional data distribution

### Call Out External Connections

If you find external sources, explicitly state them:
- "SOURCE with DATABASETYPE='Flat File' — **EXTERNAL** file-based ingestion"
- "ODBC connection references external Oracle server — **requires alternative ingestion solution**"

### Recognize Hidden Ingestion

A workflow may look like transformation but actually does ingestion:
- SOURCE elements with DATABASETYPE pointing to external systems
- HTTP Transformation making API calls
- Stored Procedure calls to external databases
- Command tasks downloading files before mapping execution

---

## Quality Checklist

Before submitting analysis, verify:

- [ ] Classification includes clear reasoning explaining WHY (not just the label)
- [ ] Sources explicitly state DATABASETYPE and whether INTERNAL or EXTERNAL
- [ ] Custom transformations are called out specifically
- [ ] SQL Overrides are mentioned if present
- [ ] Conversion section identifies what converts vs what needs alternatives
- [ ] Analysis is 150-300 words

---

## Update JSON Command

After completing analysis:

```bash
uv run python -m informatica_assessment_analyzer informatica <JSON_PATH> update '<WORKFLOW_PATH>' \
  --ai-status DONE \
  --ai-analysis "..." \
  --classification "Ingestion|Data Transformation|Configuration & Control|Mixed: Ingestion + Transformation"
```
