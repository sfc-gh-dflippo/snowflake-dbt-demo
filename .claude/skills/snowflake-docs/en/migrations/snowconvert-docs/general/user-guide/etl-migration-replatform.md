---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:51:42.358793+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/etl-migration-replatform
title: SnowConvert AI - ETL Migration | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../about.md)
          + [Getting Started](../getting-started/README.md)
          + [Terms And Conditions](../terms-and-conditions/README.md)
          + [Release Notes](../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](snowconvert/README.md)
            + [Project Creation](project-creation.md)
            + [Extraction](extraction.md)
            + [Deployment](deployment.md)
            + [Data Migration](data-migration.md)
            + [Data Validation](data-validation.md)
            + [Power BI Repointing](power-bi-repointing-general.md)
            + [ETL Migration](etl-migration-replatform.md)
          + [Technical Documentation](../technical-documentation/README.md)
          + [Contact Us](../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../translation-references/general/README.md)
          + [Teradata](../../translation-references/teradata/README.md)
          + [Oracle](../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../translation-references/transact/README.md)
          + [Sybase IQ](../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../translation-references/hive/README.md)
          + [Redshift](../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../translation-references/postgres/README.md)
          + [BigQuery](../../translation-references/bigquery/README.md)
          + [Vertica](../../translation-references/vertica/README.md)
          + [IBM DB2](../../translation-references/db2/README.md)
          + [SSIS](../../translation-references/ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)GeneralUser GuideETL Migration

# SnowConvert AI - ETL Migration[¶](#snowconvert-ai-etl-migration "Link to this heading")

[Preview Feature](../../../../release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

SnowConvert AI provides powerful ETL migration capabilities to help you modernize legacy ETL workflows and migrate them to cloud-native architectures on Snowflake. The Replatform feature converts traditional ETL packages into modern data transformation frameworks like [dbt (data build tool)](../../../../user-guide/data-engineering/dbt-projects-on-snowflake), while preserving orchestration logic using Snowflake’s native [TASKs](../../../../sql-reference/sql/create-task) and [stored procedures](../../../../sql-reference/sql/create-procedure).

This guide focuses on migrating [SSIS (SQL Server Integration Services)](https://learn.microsoft.com/en-us/sql/integration-services/sql-server-integration-services?view=sql-server-ver17) packages to dbt projects on Snowflake. You’ll learn about the migration process, understand the generated output structure, and discover how to work with the migrated code.

## SSIS Replatform[¶](#ssis-replatform "Link to this heading")

The SSIS Replatform feature migrates your SQL Server Integration Services packages to a modern, cloud-native architecture on Snowflake. SSIS packages are decomposed into two primary components:

* **Data Flow Tasks** → Converted to [dbt projects](../../../../user-guide/data-engineering/dbt-projects-on-snowflake) for data transformation
* **Control Flow logic** → Converted to Snowflake [TASKs](../../../../sql-reference/sql/create-task) or [stored procedures](../../../../sql-reference/sql/create-procedure) for orchestration

This section describes the step-by-step process to migrate your SSIS projects to dbt projects on Snowflake using SnowConvert AI.

### Prerequisites[¶](#prerequisites "Link to this heading")

Before you begin, ensure you have the following:

* **SnowConvert AI** is installed with a [valid license (access code)](snowconvert/how-to-request-an-access-code/README)
* **Source dependencies** accessible in Snowflake (required for running the migrated dbt project, not for the migration itself)
* **DTSX package files** extracted from ISPAC files (ISPAC files aren’t supported directly)
* **SSIS package version 8 or later** (for earlier versions, [upgrade your packages](https://learn.microsoft.com/en-us/sql/integration-services/install-windows/upgrade-integration-services-packages-using-the-ssis-package-upgrade-wizard?view=sql-server-ver17) first)

### Migration Steps[¶](#migration-steps "Link to this heading")

Follow these steps to migrate your SSIS project:

#### Step 1: Select the path to your scripts[¶](#step-1-select-the-path-to-your-scripts "Link to this heading")

Include DDL scripts for all dependencies to ensure high-quality migrated code. The migration process uses these scripts to identify data types and constraints.

![Select the path to your scripts in SnowConvert AI](../../../../_images/step1.png)


Select the path to your scripts in SnowConvert AI[¶](#id2 "Link to this image")

#### Step 2: Click the Replatform card[¶](#step-2-click-the-replatform-card "Link to this heading")

Click the Replatform card to begin the migration. If you don’t see this option, update SnowConvert AI to the latest version, or contact support.

![Click the Replatform card](../../../../_images/step2.png)


Click the Replatform card[¶](#id3 "Link to this image")

#### Step 3: Browse to your SSIS project location[¶](#step-3-browse-to-your-ssis-project-location "Link to this heading")

1. Click **Browse** and navigate to your SSIS project folder
2. Ensure the folder contains DTSX files (required for migration)
3. Click **Continue To Conversion**

![Browse to your SSIS project location](../../../../_images/step3.png)


Browse to your SSIS project location and click Continue To Conversion[¶](#id4 "Link to this image")

SnowConvert AI migrates your SSIS project and any scripts in the specified paths.

#### Step 4: Review the results[¶](#step-4-review-the-results "Link to this heading")

After migration completes:

1. Review the migration reports
2. Fix any issues identified in the reports
3. Fill placeholders in `sources.yml`, `profiles.yml`, and `dbt_project.yml`

![Review the migration reports](../../../../_images/step4-1.png)


Review the migration reports to identify any issues[¶](#id5 "Link to this image")


![Fill placeholders in configuration files](../../../../_images/step4-2.png)


Fill placeholders in `sources.yml`, `profiles.yml`, and `dbt_project.yml`[¶](#id6 "Link to this image")

The output includes:

* **ETL/**: Main folder containing all converted SSIS packages

  + **etl\_configuration/**: Infrastructure components (control\_variables table, UDFs, procedures)
  + **{PackageName}/**: Folder for each SSIS package containing:

    - **{PackageName}.sql**: Orchestration file (TASK or PROCEDURE)
    - **{DataFlowTaskName}/**: dbt project for each Data Flow Task
* **script.sql**: Migrated SQL scripts (if applicable)

For a detailed description of the output structure, see [Output Structure](#output-structure).

#### Step 5: Upload your dbt project[¶](#step-5-upload-your-dbt-project "Link to this heading")

After you’ve reviewed the dbt project, filled placeholders in `.yml` files, and fixed EWIs, upload the project using one of these methods.

For more information about working with dbt projects on Snowflake, see [Getting Started with dbt Projects](../../../../user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial).

##### Option A: Upload using Snowflake CLI[¶](#option-a-upload-using-snowflake-cli "Link to this heading")

Run this command in your dbt project directory (replace values in italics with your schema, database, and package names):

```
snow dbt deploy --schema schema_name --database database_name --force package_name
```

Copy

If successful, skip to Step 6.

##### Option B: Upload via Snowflake Workspace[¶](#option-b-upload-via-snowflake-workspace "Link to this heading")

Navigate to **Workspaces > Add new > Upload Folder** and select your dbt project folder.

![Navigate to Workspaces and upload folder](../../../../_images/step5-1.png)


Navigate to **Workspaces > Add new > Upload Folder**[¶](#id7 "Link to this image")

Deploy the dbt project to make it accessible for orchestration:

1. Click **Connect > Deploy dbt project** (top right corner)
2. Use the project name that matches your dbt project folder name

   * Example: For `Process_Sales_Files_Load_Sales_Data/`, use “Process\_Sales\_Files\_Load\_Sales\_Data”
   * This name is referenced in the orchestration file via `EXECUTE DBT PROJECT` commands

![Click Connect and Deploy dbt project](../../../../_images/step5-2.png)


Click **Connect > Deploy dbt project** (top right corner)[¶](#id8 "Link to this image")

For example, if your orchestration uses `public.Package`:

```
EXECUTE DBT PROJECT public.Package ARGS='build --select tag:package_dataflowtask --target dev';
```

Copy

Use `Package` as your project name when deploying.

![Deploy dbt project modal](../../../../_images/step5-3.png)


Deploy dbt project modal - enter the project name[¶](#id9 "Link to this image")

**Note**: Deploy all dbt projects in your migration.

#### Step 6: Run your dbt project[¶](#step-6-run-your-dbt-project "Link to this heading")

Select the correct database and schema before running your project.

![Select database and schema](../../../../_images/step6-1.png)


Select the correct database and schema before running[¶](#id10 "Link to this image")

**For single dataflow projects:**

Run the dbt project directly if you have only one data flow.

![Run the dbt project for single dataflow](../../../../_images/step6-2.png)


Run the dbt project directly for single dataflow scenarios[¶](#id11 "Link to this image")

**For multi-dataflow projects:**

1. **Run the orchestration SQL file** to create all TASK objects

   * This creates the initialization TASK and all dependent TASKs
   * For reusable packages, this creates stored procedures instead

![Run all to create TASK objects](../../../../_images/step6-3.png)


Click Run All to create all TASK objects for multi-dataflow projects[¶](#id12 "Link to this image")

2. **Execute the orchestration**:

   **For TASK-based orchestration** (standard packages):

```
-- Execute the root task
EXECUTE TASK public.Package;
```

Copy

**For PROCEDURE-based orchestration** (reusable packages):

```
-- Call the stored procedure
CALL public.PackageName();
```

Copy

**Note**: Check your generated SQL file to determine whether your package uses the TASK or PROCEDURE pattern.

## Output Structure[¶](#output-structure "Link to this heading")

SnowConvert generates an output structure that separates data transformation logic ([dbt projects](../../../../user-guide/data-engineering/dbt-projects-on-snowflake)) from orchestration logic (Snowflake [TASKs](../../../../sql-reference/sql/create-task) and [PROCEDUREs](../../../../sql-reference/sql/create-procedure)).

Understanding this structure is essential for working with the migrated code.

### Overview[¶](#overview "Link to this heading")

SnowConvert organizes all migration output under the `Output/ETL/` folder. Here’s the complete folder structure:

```
Output/
└── ETL/
    ├── etl_configuration/
    │   ├── tables/
    │   │   └── control_variables_table.sql
    │   ├── functions/
    │   │   └── GetControlVariableUDF.sql
    │   └── procedures/
    │       └── UpdateControlVariable.sql
    ├── {PackageName}/
    │   ├── {PackageName}.sql                          # Main orchestration TASK
    │   └── {DataFlowTaskName}/                        # One dbt project per Data Flow Task
    │       ├── dbt_project.yml
    │       ├── profiles.yml
    │       ├── models/
    │       │   ├── sources.yml
    │       │   ├── staging/
    │       │   │   └── stg_raw__{component_name}.sql
    │       │   ├── intermediate/
    │       │   │   └── int_{component_name}.sql
    │       │   └── marts/
    │       │       └── {destination_component_name}.sql
    │       ├── macros/
    │       │   ├── m_update_control_variable.sql
    │       │   └── m_update_row_count_variable.sql
    │       ├── seeds/
    │       └── tests/
    └── (additional packages...)/
```

Copy

**SSIS to SnowConvert Conversion Mapping:**

* **SSIS Data Flow Tasks** → dbt projects (one per Data Flow Task)
* **SSIS Control Flow** → Snowflake TASK objects or stored procedures
* **SSIS Variables** → control\_variables table + UDFs + DBT variables
* **SSIS Containers** → Inline conversion within parent TASK/procedure

### ETL Configuration Components[¶](#etl-configuration-components "Link to this heading")

The `etl_configuration/` folder contains shared infrastructure components required by all ETL orchestrations. These components work together to manage variables across package executions:

* **control\_variables\_table.sql**: Creates a transient table to store package variables, parameters, and their values across orchestration executions
* **GetControlVariableUDF.sql**: User-defined function to retrieve variable values from the control variables table
* **UpdateControlVariable.sql**: Stored procedure to update variable values during orchestration execution

**Schema Dependencies**: The UDFs and stored procedures in the `etl_configuration/` folder are generated with hardcoded schema references (default: `public`). If you deploy these objects to a different schema, you must update the schema references within:

* The `GetControlVariableUDF.sql` function (references `public.control_variables` in the SELECT statement)
* The `UpdateControlVariable.sql` procedure (references `public.control_variables` in the MERGE statement)
* Any orchestration scripts that call these objects

### Common Naming and Sanitization Rules[¶](#common-naming-and-sanitization-rules "Link to this heading")

SnowConvert applies consistent sanitization rules to all SSIS object names to ensure dbt and Snowflake compatibility. This includes packages, tasks, components, and variables.

| Rule | Description | Example |
| --- | --- | --- |
| **Convert to lowercase** | All names converted to lowercase | `MyPackage` → `mypackage` |
| **Replace invalid characters** | Spaces, hyphens, and special characters become underscores | `My-Package Name` → `my_package_name` |
| **Remove consecutive underscores** | Avoids `__` sequences (except `stg_raw__` prefix) | `my___package` → `my_package` |
| **Prefix with `t_`** | Adds prefix if name starts with a number | `123package` → `t_123package` |
| **Remove quotes and brackets** | Strips surrounding quotes and brackets | `[Package]` → `package` |

These rules apply uniformly across all generated artifacts: dbt model names, Snowflake TASK names, procedure names, and variable identifiers.

### Data Flow Task Output (dbt Projects)[¶](#data-flow-task-output-dbt-projects "Link to this heading")

Each [SSIS Data Flow Task](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/data-flow?view=sql-server-ver17) is converted into a standalone dbt project with a three-tier architecture. These dbt projects contain all the data transformation logic from your original SSIS packages.

**Supported Data Flow Components**: For a complete list of supported sources, transformations, and destinations, see the [SSIS Translation Reference](../../translation-references/ssis/README).

#### Layer Organization[¶](#layer-organization "Link to this heading")

Each dbt project follows a three-tier architecture that separates data extraction, transformation, and loading:

| Layer | Materialization | Purpose |
| --- | --- | --- |
| **models/staging/** | View | Provides clean, type-safe access to source data referenced in `sources.yml` |
| **models/intermediate/** | Ephemeral | Contains transformation logic from source ETL (not persisted to database for performance) |
| **models/marts/** | Incremental or Table | Final, business-ready data models corresponding to target tables. If the target overrides data in the table or re-creates the table, it will be materialized as a table, otherwise it will be materialized as an incremental model. |

**Materialization configuration:**

Default materializations are defined in `dbt_project.yml`. However, individual models can override these defaults when needed:

* Use `{{ config(materialized='view') }}` to change a specific model’s materialization
* Use `{{ config(alias='...') }}` in mart models to customize the final table name in Snowflake

#### dbt Model Naming Conventions[¶](#dbt-model-naming-conventions "Link to this heading")

SnowConvert uses prefixes to indicate each model’s layer in the dbt project:

| Model Type | Naming Pattern | Examples |
| --- | --- | --- |
| **Staging** | `stg_raw__{component_name}` | `stg_raw__flat_file_source`, `stg_raw__ole_db_source` |
| **Intermediate** | `int_{component_name}` | `int_derived_column`, `int_union_all` |
| **Mart** | `{destination_component_name}` | `ole_db_destination`, `stgdimgroup` |

The `stg_raw__` prefix indicates a staging model that selects from a raw source, while the `int_` prefix marks intermediate transformation models. Mart models use the destination table name directly or can specify a custom alias.

**Important notes:**

* All component names are sanitized according to the naming rules above
* Mart models become the final table names in Snowflake
* You can customize mart table names using `{{ config(alias='TableName') }}`

#### dbt Project Organization[¶](#dbt-project-organization "Link to this heading")

**Organization structure:**

* **One dbt project per Data Flow Task** (e.g., `Process_Sales_Files_Load_Sales_Data/`)
* **Package-level folder** contains the orchestration SQL file and all dbt project folders
* **Models organized by layer** (staging, intermediate, marts) within each dbt project
* **Orchestration execution** uses `EXECUTE DBT PROJECT` commands

#### sources.yml Configuration[¶](#sources-yml-configuration "Link to this heading")

The `sources.yml` file, located in the `models/` directory, declares all source tables used by the dbt project. This file serves three key purposes:

* **Connection**: Links dbt models to raw data tables in Snowflake
* **Documentation**: Provides metadata and descriptions for source systems
* **Lineage**: Enables tracking data flow from sources through transformations

**Important**: Before deploying your dbt project, replace the `YOUR_SCHEMA` and `YOUR_DB` placeholders with your actual Snowflake schema and database names.

#### dbt Macros[¶](#dbt-macros "Link to this heading")

Each dbt project includes these macros:

| Macro | Purpose |
| --- | --- |
| **m\_update\_control\_variable.sql** | Updates control variables from dbt models and syncs changes to orchestration |
| **m\_update\_row\_count\_variable.sql** | Captures row counts from transformations (similar to SSIS row count updates) |

### Control Flow Task Output (Orchestration)[¶](#control-flow-task-output-orchestration "Link to this heading")

[SSIS control flow logic](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/control-flow?view=sql-server-ver17) is converted into Snowflake orchestration using [TASK](../../../../sql-reference/sql/create-task) objects or [stored procedures](../../../../sql-reference/sql/create-procedure). This orchestration layer manages the execution sequence of your dbt projects and handles variables, containers, and package execution.

**Supported Control Flow Elements**: For a complete list of supported tasks and containers, see the [SSIS Translation Reference](../../translation-references/ssis/README).

#### Orchestration Naming Conventions[¶](#orchestration-naming-conventions "Link to this heading")

Orchestration objects follow consistent naming patterns based on the SSIS package and task names:

| Object Type | Naming Pattern | Example |
| --- | --- | --- |
| **Orchestration files** | `{PackageName}.sql` | `Package.sql`, `StgDimGroup.sql` |
| **Package initialization TASK** | `{schema}.{PackageName}` | `public.Package` |
| **Data Flow TASK** | `{schema}.{package_name}_{dataflow_name}` | `public.package_process_sales_files` |
| **Stored Procedure** (reusable) | `{schema}.{PackageName}` | `public.ReusableETLPackage` |

**Notes:**

* All names are sanitized according to the naming rules described earlier
* Stored procedures are used when packages are called by at least one ExecutePackage task from another control flow

#### Orchestration Approach[¶](#orchestration-approach "Link to this heading")

Each SSIS package generates an orchestration SQL file. The conversion pattern depends on whether the package is reused:

##### Standard Packages (not called by ExecutePackage tasks)[¶](#standard-packages-not-called-by-executepackage-tasks "Link to this heading")

Standard packages that are not called by ExecutePackage tasks from other control flows are converted to Snowflake TASK objects. Each package typically generates two types of TASKs:

* **Initialization TASK**: Creates and refreshes control variables for the package

  + Deletes existing package variables from the `control_variables` table
  + Inserts all variables and parameters with their default values using `TO_VARIANT()`
* **Main Orchestration TASKs**: Contains the core control flow logic

  + Declared with `WAREHOUSE=DUMMY_WAREHOUSE` (update this to your actual warehouse name)
  + Uses the `AFTER` clause to establish task dependencies
  + Executes converted control flow and data flow tasks

##### Reusable Packages (called by ExecutePackage tasks)[¶](#reusable-packages-called-by-executepackage-tasks "Link to this heading")

Packages that are called by at least one ExecutePackage task from another control flow are converted to stored procedures instead of TASK objects. This is necessary because Snowflake TASK objects can’t be called synchronously from other tasks.

**Key characteristics:**

* FDM generated: [SSC-FDM-SSIS0005](../technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0005)
* Invocation: `CALL schema.ProcedureName(params)` from parent orchestration
* Benefits: Enables synchronous execution and can be called from multiple parent packages with different parameter values

**Example orchestration structure:**

```
CREATE OR REPLACE TASK public.Package AS
BEGIN
   -- Initialize control variables
   DELETE FROM public.control_variables WHERE variable_scope = 'Package';
   INSERT INTO public.control_variables ...
END;

CREATE OR REPLACE TASK public.package_data_flow_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.package
AS
BEGIN
   -- Declare LET variables from control table
   LET User_Variable VARCHAR := public.GetControlVariableUDF('User_Variable', 'Package') :: VARCHAR;
   
   -- Execute dbt project
   EXECUTE DBT PROJECT public.My_DataFlow_Project ARGS='build --target dev';
   
   -- Update control variables
   CALL public.UpdateControlVariable('User_Variable', 'Package', TO_VARIANT(:User_Variable));
END;
```

Copy

#### Variable Management[¶](#variable-management "Link to this heading")

SSIS variables are converted into a comprehensive management system using four interconnected mechanisms:

##### 1. Control Variables Table[¶](#control-variables-table "Link to this heading")

The `control_variables` table serves as the central storage for all package variables and parameters. Each variable is stored with the following metadata:

| Field | Type | Description |
| --- | --- | --- |
| `variable_name` | VARCHAR | Variable name |
| `variable_value` | VARIANT | Value (accommodates any data type) |
| `variable_type` | VARCHAR | Original SSIS data type |
| `variable_scope` | VARCHAR | Package or container name |
| `is_parameter` | BOOLEAN | Distinguishes parameters from variables |
| `is_persistent` | BOOLEAN | Reserved for future use |
| `last_updated_at` | TIMESTAMP | Last update time |

##### 2. GetControlVariableUDF Function[¶](#getcontrolvariableudf-function "Link to this heading")

This user-defined function retrieves variable values within TASK logic. Use it to read variable values from the control variables table:

```
LET MyVar VARCHAR := public.GetControlVariableUDF('MyVar', 'Package') :: VARCHAR;
```

Copy

##### 3. UpdateControlVariable Procedure[¶](#updatecontrolvariable-procedure "Link to this heading")

This stored procedure updates variable values during orchestration execution. Use it to write variable changes back to the control variables table:

```
CALL public.UpdateControlVariable('MyVar', 'Package', TO_VARIANT(:MyVar));
```

Copy

##### 4. dbt Macros[¶](#id1 "Link to this heading")

Each dbt project includes macros that enable variable operations from within dbt models:

* `m_update_control_variable.sql`: Updates control variables and syncs changes back to the orchestration layer
* `m_update_row_count_variable.sql`: Captures row counts from transformations, similar to SSIS row count variable updates

#### Inline Container Conversion Approach[¶](#inline-container-conversion-approach "Link to this heading")

SnowConvert uses an **inline conversion approach** for [SSIS containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/control-flow?view=sql-server-ver17) rather than creating separate procedures. This architectural decision preserves execution context and simplifies the migration.

**Why inline conversion?**

Migrating SSIS isn’t just “translate this component to that component.” It’s untangling control flow, variables, and data movement that have lived together for years. Our inline approach preserves that context:

* **One place to debug**: Containers and branches are converted inline inside parent Snowflake procedures or tasks. No bouncing across tools to understand why something ran (or didn’t).
* **Deterministic orchestration**: Standalone packages become Snowflake Tasks with explicit dependencies. Packages called by ExecutePackage tasks become procedures for clean, synchronous reuse.
* **Fewer naming collisions**: We consistently sanitize object names across dbt models, tasks, procedures, and variables, so deployments remain predictable in shared environments.
* **Familiar, but modern**: Data movement and business logic land in dbt with layered models and macros, while orchestration runs natively on Snowflake. Same mental model as SSIS—without the engine lock-in.

**What gets converted inline:**

* [Sequence Containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/sequence-container?view=sql-server-ver17) - Sequential task execution with marked boundaries
* [For Loop Containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/for-loop-container?view=sql-server-ver17) - Container structure preserved, iteration logic requires manual implementation
* [ForEach Loop Containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) - File enumerators converted to Snowflake stage operations, other types require manual work
* [Event Handlers](https://learn.microsoft.com/en-us/sql/integration-services/integration-services-ssis-event-handlers?view=sql-server-ver17) - Not supported; implement using Snowflake exception handling

For detailed conversion specifications, examples, and EWI/FDM references for all control flow elements and task conversions, see the [SSIS Translation Reference](../../translation-references/ssis/README).

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [SSIS Replatform](#ssis-replatform)
2. [Output Structure](#output-structure)