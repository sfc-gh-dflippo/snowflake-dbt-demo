# How to Write SSIS Package Analysis

This guide defines how to write comprehensive, actionable AI analysis for SSIS packages being assessed for migration to Snowflake.

---

## Context: SnowConvert AI Migration

SnowConvert AI processes SSIS packages and converts them to Snowflake-native components:

| SSIS Component | Snowflake Target | Technology |
|----------------|------------------|------------|
| **Control Flow** | [Snowflake Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) | Snowflake Scripting |
| **Data Flow** | dbt Projects | dbt models running on Snowflake |

### Critical Understanding

**SnowConvert will process all packages**, but the analysis must identify external connectivity requirements. dbt projects on Snowflake cannot directly connect to external sources - data must already exist in Snowflake. This means:

- **Ingestion packages** require attention to identify external connector solutions
- **Packages with transformations on internal sources** have straightforward conversion paths
- **Mixed packages** require analysis to separate what converts directly vs. what needs connector solutions

### External Connector Solutions

When a package performs ingestion from external sources, identify the source type and recommend appropriate solutions:

| Source Type | Recommended Solution |
|-------------|---------------------|
| **Cloud Services** (Google Services, ServiceNow, Salesforce, etc.) | Snowpark Python connectors, Fivetran managed connectors |
| **APIs / REST endpoints** | Snowpark Python with External Access Integration |
| **File-based** (CSV, Excel, JSON from cloud storage) | Snowpipe, External Stages |
| **File-based** (local/network shares) | Snowflake Openflow, custom orchestration |
| **External databases** (Oracle, MySQL, PostgreSQL) | Fivetran, Snowflake Openflow, Airflow with custom operators |
| **FTP/SFTP servers** | Airflow orchestration, custom Python scripts |

The analysis should clearly identify the external source type so the migration team can plan the appropriate connector solution.

---

## Your Task

Using the package information, package metrics, DAG structure, and SQL logic gathered from the previous analysis steps, write an AI analysis that:

1. **Classifies** the package based on its actual logic, purpose and data flow patterns
2. **Describes** the package structure, sources, targets, and logic
3. **Identifies** external connectivity requirements and recommends connector solutions
4. **Estimates** migration effort realistically

---

## Classification Categories

### Data Transformation

**Definition:** Processes data that already exists within the data platform, applying business logic to move data between internal layers.

**Classification Requirement:** You MUST analyze all available package information to classify as Data Transformation. Base your classification on concrete evidence found in:
- SQL statements in Execute SQL Tasks and stored procedure calls
- Script Task code (C#/VB.NET)
- Data Flow component configurations, DAG and transformations
- Control Flow DAG structure and task dependencies
- Connection manager configurations (source types, server names)
- Package metrics (component counts, Data Flow counts, complexity indicators)

**Why classify as Data Transformation:**

A package is Data Transformation when the primary purpose is to **transform, enrich, aggregate, or restructure data** that is already inside the data warehouse ecosystem. The key distinction is that **both source and target are internal database objects** - no external system connectivity is required.

This classification applies when you observe in the package analysis (SQL logic, Script logic, Data Flow components, DAG structure, metrics, and connection managers):

1. **Internal-to-internal data movement:** Sources are staging tables, mirror tables, operational data stores or other internal schemas. Targets are data warehouse tables, dimensions, facts, or presentation layer objects.

2. **Business logic application:** The SQL contains JOINs between multiple tables, CASE statements for business rules, aggregations (SUM, COUNT, AVG), window functions for rankings or running totals, or MERGE/upsert operations for incremental loading.

3. **Dimensional modeling patterns:** The package builds or maintains dimensions (Type 1 overwrites, Type 2 history tracking), fact tables, or aggregate/summary tables for reporting.

4. **No external connection managers:** All OLE DB or ADO.NET connections point to internal SQL Server databases within the same environment. No file paths, FTP servers, API endpoints, CSV or Excel files, or external database servers.

**SnowConvert Outcome:**
- Control Flow → Snowflake Tasks
- Data Flow → dbt models
- **Excellent conversion candidate**

---

### Ingestion

**Definition:** Extracts data from external sources to the data platform.

**Classification Requirement:** You MUST analyze all available package information to classify as Ingestion. Look for evidence in connection manager configurations (external servers, file paths), Data Flow source components (Flat File, Excel, OData sources), Control Flow DAG structure, and package metrics indicating file/API access patterns.

**Why classify as Ingestion:**

A package is Ingestion when the primary purpose is to **bring data INTO the data platform from an external source**. The defining characteristic is that **the source exists outside the data warehouse** - it could be files, APIs, FTP servers, external databases, or cloud services.

This classification applies when you observe in the package analysis (SQL logic, Script logic, Data Flow components, DAG structure, metrics, and connection managers):

1. **External source connections:** Connection managers reference file paths (local or network shares), FTP/SFTP servers, HTTP/API endpoints, external database servers (Oracle, MySQL, PostgreSQL outside your environment), SharePoint, or cloud storage.

2. **File-based sources in Data Flows:** Data Flow components include Flat File Source, Excel Source, XML Source, Raw File Source, or OData Source. These indicate the package reads from files rather than database tables.

3. **File System or FTP Tasks in Control Flow:** Presence of tasks that download files, move files between directories, or interact with external file systems indicates ingestion patterns.

**SnowConvert Outcome:**
- Control Flow → Snowflake Tasks
- Data Flow → dbt projects
- **Requires external connector solution** - identify source type and recommend appropriate approach
- Pure ingestion packages (minimal transformation) may be better served by dedicated connector solutions rather than converted dbt models

---

### Configuration & Control

**Definition:** Orchestrates processes, manages metadata, call packages or performs system operations without directly moving business data.

**Classification Requirement:** You MUST analyze all available package information to classify as Configuration & Control. Look for evidence in Execute Package Tasks, control framework table operations (SQL logic), File/Scripts operations, Control Flow DAG showing orchestration patterns, package metrics (high control flow count, zero/minimal Data Flows), and Script Tasks for coordination logic.

**Why classify as Configuration & Control:**

A package is Configuration & Control when the primary purpose is to **coordinate, orchestrate, or manage other processes** rather than move or transform business data directly. These packages are the "conductors" of the ETL orchestra.

This classification applies when you observe in the package analysis (Control Flow DAG structure, SQL logic for metadata operations, Script logic, package metrics, and component types):

1. **Package orchestration:** Execute Package Tasks that call child packages in sequence or parallel. The parent package's role is coordination, not data movement.

2. **Dynamic iteration:** For Each Loop or For Loop containers that iterate over files, tables, or configuration values to drive processing dynamically.

3. **System operations:** File System Tasks (copy, move, delete, archive), Send Mail Tasks for notifications, or Script Tasks that perform maintenance operations.

4. **Metadata management:** SQL Tasks that update control tables, log execution status, manage configuration parameters, or perform housekeeping operations.

5. **No Data Flows or minimal Data Flows:** The package may have zero Data Flows, or only small Data Flows that move metadata/configuration rather than business data.

6. **Script-heavy logic:** Script Tasks with C#/VB.NET code for complex orchestration logic, error handling, or integration with external systems.

**SnowConvert Outcome:**
- Control Flow → Snowflake Tasks with procedural Snowflake Scripting
- May require Snowflake stored procedures for complex conditional logic
- Script Tasks need manual rewrite (Python UDFs or external orchestration)
- File/FTP operations need external orchestration (Airflow) or pre/post processing

---

### Mixed: Ingestion + Transformation

**Definition:** Package performs both ingestion from external sources AND applies significant transformations.

**Classification Requirement:** You MUST analyze all available package information to classify as Mixed. Look for evidence of both external source connections (in connection managers, Data Flow sources) AND significant business logic transformations (in SQL logic, Data Flow transformations, DAG structure) within the same package.

**Why classify as Mixed:**

A package is Mixed when it **combines ingestion and transformation in a single package**. This is common in legacy SSIS designs where a single package does "everything" - extracts from external source, cleanses, transforms, and loads to final destination.

This classification applies when you observe in the package analysis (SQL logic, Script logic, Data Flow components, DAG structure, metrics, and connection managers):

1. **External sources feeding into transformation logic:** A Data Flow reads from an external source (file, API, external DB) but then applies significant transformations - not just type conversion, but joins, lookups, business calculations.

2. **Multiple Data Flows with different source types:** Some Data Flows read from external sources (ingestion), while others read from internal staging tables (transformation).

3. **SQL Tasks that transform after external load:** The package loads data from external source to staging, then SQL Tasks perform significant transformation logic on that staged data.

**SnowConvert Outcome:**
- **Partial candidate** - transformation portions can convert, ingestion cannot
- Recommend architectural separation: ingestion via Fivetran/Airflow, transformation via dbt
- Analysis should clearly identify which components are convertible vs. which need alternatives

---

## Analysis Structure (MANDATORY)

**All analyses MUST follow this exact format.** Each section must be a separate paragraph with the section header followed by a colon. This format is required for validation and consistency.

```
Classification: [Category]. [Two-three sentences explaining WHY based on specific evidence from the package]

Sources & Destinations: Analysis and explanation of connection managers, sources and destinations

Purpose: Business purpose and value - why does this package exist, what business need does it serve, who depends on it (avoid technical pipeline descriptions, the DAG shows that)

Conversion: Why is a good candidate or not to Snowflake
```

**Format Requirements:**
1. Each section header must start at the beginning of a paragraph: `Classification:`, `Sources & Destinations:`, `Purpose:`, `Conversion:`
2. Sections must be separated by blank lines (paragraph breaks)

> **See:** [analysis_example.md](./analysis_example.md) for complete examples of well-structured analyses for each classification type.

---

## Writing Guidelines

### Call Out External Connections

If you find external sources, explicitly state them:
- "Source includes Flat File connection to network share path - **EXTERNAL**"
- "OLE DB connection references external Oracle server - **requires alternative ingestion solution**"

### Identify Transformation Potential in Non-Data-Flow Packages

Packages with 0 Data Flows but SQL-heavy logic may still be excellent candidates:
- "0 Data Flows, 45 Execute SQL Tasks - all internal table operations, **suitable for Snowflake Tasks**"

### Recognize Hidden Ingestion

A package may look like transformation but actually does ingestion:
- Data Flow reads from OLE DB Source connected to external system
- SQL Task uses OPENROWSET or linked server to external database
- File System Task processes files before loading

---

## Component Inventory Guide

Report these counts to assess conversion complexity:

| Component | Count | Conversion Notes |
|-----------|-------|------------------|
| Execute SQL Tasks | X | Low complexity - direct SQL to Snowflake Scripting |
| Data Flow Tasks | X | Converts to dbt models (if not ingestion) |
| Script Tasks | X | **Effort depends on script logic** - analyze the code to determine complexity (easy, medium, or complex) |
| For Each Loop Containers | X | Snowflake procedural logic |
| Sequence Containers | X | Organizational - minimal impact |
| Execute Package Tasks | X | Task dependencies |
| File System Tasks | X | May need external orchestration |
| FTP/SFTP Tasks | X | **Not convertible** - need alternative |

---


---

## Effort Estimation

Effort = hours to bring package to **production** (migration + validation + deployment).

### Effort Scale

| Effort | Package Profile |
|--------|-----------------|
| 6-8 hrs | Simple: <10 components, no Data Flows, standard patterns |
| 8-24 hrs | Medium: 10-30 components, simple Data Flows, standard SQL |
| 24-40 hrs | Complex: 30-50 components, multiple Data Flows, some custom logic |
| 40-80 hrs | Large: 50+ components, complex Data Flows, UDF dependencies |
| 80-120 hrs | Very large: Many Data Flows, Script Tasks, complex orchestration |
| 120+ hrs | Massive: 100+ components, heavy scripting, external dependencies |

### Effort Multipliers

| Factor | Impact |
|--------|--------|
| Script Tasks present | +20%-30% |
| External connections (need alternative solution) | +15-30% |
| Complex orchestration (nested loops, conditions) | +20-40% |
| Third-party components | +25-50% |

---

## Quality Checklist

Before submitting analysis, verify:

**Content:**
- [ ] Classification includes clear reasoning explaining WHY (not just the label)
- [ ] Sources explicitly state if INTERNAL or EXTERNAL
- [ ] External connections identify source type and recommend connector solutions
- [ ] Logic describes actual SQL patterns and operations found
- [ ] Conversion assessment identifies external connector needs for ingestion packages
- [ ] Effort is realistic based on complexity factors
- [ ] Analysis is 150-300 words

---

## Update JSON Command

After writing your analysis, update the package record using command options (NOT a file path):

```bash
scai assessment etl update '<PACKAGE_PATH>' \
  --ai-status DONE \
  --ai-analysis '<YOUR_FULL_ANALYSIS_TEXT>' \
  --classification '<CATEGORY>' \
  --effort '<HOURS>'
```

**Parameters:**
- `<PACKAGE_PATH>` — relative path matching the package (e.g., `Extract_CWSO_DEALER_TBL.dtsx`)
- `--ai-status` — must be `DONE` when submitting completed analysis
- `--ai-analysis` — your full analysis text (all four sections: Classification, Sources & Destinations, Purpose, Conversion)
- `--classification` — one of: `Ingestion`, `Data Transformation`, `Configuration & Control`, `Mixed`
- `--effort` — estimated hours (e.g., `20-28 hours`, `16-24 hours`)

**Important:** Pass the analysis text directly as a command option, NOT as a file path. The command validates the analysis format before updating the JSON.
