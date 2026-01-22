---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:53:55.128085+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/ssis/README
title: SnowConvert AI - SSIS | Snowflake Documentation
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

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation ReferencesSSIS

# SnowConvert AI - SSIS[¶](#snowconvert-ai-ssis "Link to this heading")

[Preview Feature](../../../../release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This section provides a comprehensive reference of SSIS elements and components that SnowConvert can convert to dbt and Snowflake. Control Flow elements (tasks and containers) become orchestration logic, while Data Flow components (sources, transformations, destinations) become dbt models.

## Control Flow Elements[¶](#control-flow-elements "Link to this heading")

These SSIS Control Flow tasks and containers are supported:

| Element | Category | Conversion Target | Notes |
| --- | --- | --- | --- |
| [Microsoft.Pipeline (Data Flow Task)](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/data-flow?view=sql-server-ver17) | Task | Complete dbt Project | - |
| [Microsoft.ExecuteSQLTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-sql-task?view=sql-server-ver17) | Task | Inline SQL or Stored Procedure | - |
| [Microsoft.ExecutePackageTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-package-task?view=sql-server-ver17) | Task | Inline EXECUTE TASK or PROCEDURE call | - |
| [Microsoft.SendMailTask](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/send-mail-task?view=sql-server-ver17) | Task | SYSTEM$SEND\_EMAIL with Notification Integration | Some features not supported; See [Send Mail Task](#send-mail-task) section |
| [STOCK:SEQUENCE (Sequence Container)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/sequence-container?view=sql-server-ver17) | Container | Inline sequential execution | - |
| [STOCK:FORLOOP (For Loop Container)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/for-loop-container?view=sql-server-ver17) | Container | Sequential execution | Manual iteration logic required; Check [EWI SSC-EWI-SSIS0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0004) for more information |
| [STOCK:FOREACHLOOP (ForEach Loop Container)](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) | Container | LIST/CURSOR pattern | Requires stage mapping; Check [EWI SSC-EWI-SSIS0014](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0014) for more information |
| [Event Handlers](https://learn.microsoft.com/en-us/sql/integration-services/integration-services-ssis-event-handlers?view=sql-server-ver17) | Container | Not converted | Implement manually using Snowflake exception handling |

**Note**: Unlisted Control Flow elements generate EWI [SSC-EWI-SSIS0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0004).

### Container Conversion Details[¶](#container-conversion-details "Link to this heading")

SSIS containers (Sequence, For Loop, ForEach, Event Handlers) are converted using an inline approach where container logic is expanded within the parent TASK or procedure rather than creating separate procedures.

#### Sequence Containers[¶](#sequence-containers "Link to this heading")

[Sequence containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/sequence-container?view=sql-server-ver17) are converted inline within the parent TASK. The container’s boundaries are marked with comments in the generated code, and all tasks within the container execute sequentially in the same TASK scope.

**Conversion characteristics:**

* No separate procedure or TASK is created for the container
* Container boundaries are clearly marked BEGIN … END blocks
* All tasks execute sequentially within the parent TASK
* Task execution order based on precedence constraints is maintained
* **Limitation**: Only “Success” precedence constraints are fully supported. Conditional execution based on task outcomes (Failure or Completion constraints) is not currently implemented and will require manual post-migration adjustments

**Behavioral differences:**

* FDM generated: [SSC-FDM-SSIS0003](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0003)
* Variable scoping differs from SSIS: Container variables are accessible throughout the entire parent TASK, not just within the container scope

**Example:**

```
-- BEGIN Sequence Container: MySequence
-- Task 1 within sequence
EXECUTE DBT PROJECT public.DataFlow1 ARGS='build --target dev';
-- Task 2 within sequence  
EXECUTE DBT PROJECT public.DataFlow2 ARGS='build --target dev';
-- END Sequence Container: MySequence
```

Copy

#### For Loop Containers[¶](#for-loop-containers "Link to this heading")

[For Loop containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/for-loop-container?view=sql-server-ver17) are converted to sequential execution of their contained tasks. However, the loop iteration logic itself requires manual implementation.

**Conversion limitations:**

* The container executes once by default (iteration logic not automatically converted)
* InitExpression, EvalExpression, and AssignExpression require manual conversion
* An [EWI (SSC-EWI-SSIS0004)](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0004) is generated to indicate manual work is needed

**Required manual steps:**

1. Review EvalExpression to understand the loop termination condition
2. Implement the iteration using Snowflake’s WHILE loop construct
3. Update AssignExpression logic for proper loop counter management

#### ForEach Loop Containers[¶](#foreach-loop-containers "Link to this heading")

**File Enumerator (Supported)**

[ForEach File Enumerator containers](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/foreach-loop-container?view=sql-server-ver17) are converted to Snowflake stage operations using the LIST command and cursor pattern:

```
-- List files from Snowflake stage
LIST @<STAGE_PLACEHOLDER>/FolderPath PATTERN = '.*/file_pattern\.csv';

-- Create cursor for iteration
LET file_cursor CURSOR FOR
   SELECT REGEXP_SUBSTR($1, '[^/]+$') AS FILE_VALUE
   FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   WHERE $1 NOT LIKE '%FolderPath/%/%';

-- Iterate through files
FOR file_row IN file_cursor DO
   User_CurrentFileName := :file_row.FILE_VALUE;
   EXECUTE DBT PROJECT public.My_DataFlow_Project ARGS='build --target dev';
END FOR;
```

Copy

**Configuration requirements:**

After migration, you’ll need to:

* Replace `<STAGE_PLACEHOLDER>` with your actual Snowflake stage name
* Ensure the folder path is correctly mapped to a Snowflake stage
* Verify that files are properly staged in Snowflake

An [EWI (SSC-EWI-SSIS0014)](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0014) is generated to remind you of this manual configuration step.

**Other Enumerator Types**

Other ForEach enumerator types (ForEach Item, ForEach ADO, ForEach NodeList, etc.) aren’t currently supported. SnowConvert generates an [EWI (SSC-EWI-SSIS0004)](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0004) for these cases. Consider implementing the equivalent logic using Snowflake queries or scripting constructs.

#### Event Handlers[¶](#event-handlers "Link to this heading")

[Event handlers](https://learn.microsoft.com/en-us/sql/integration-services/integration-services-ssis-event-handlers?view=sql-server-ver17) (OnError, OnWarning, OnPreExecute, OnPostExecute, etc.) aren’t supported. EWIs are generated. Implement manually using Snowflake exception handling.

### Execute SQL Task[¶](#execute-sql-task "Link to this heading")

[Execute SQL Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-sql-task?view=sql-server-ver17) are converted as inline SQL statements or separate stored procedures, depending on complexity and result set bindings.

**Conversion approach:**

* **Simple SQL statements**: Converted inline within the parent TASK
* **Complex statements with result sets**: May be converted to separate stored procedures
* **Result bindings**: Handled where possible; unsupported patterns generate [EWI SSC-EWI-SSIS0011](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0011)

### Execute Package Task[¶](#execute-package-task "Link to this heading")

[Execute Package Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/execute-package-task?view=sql-server-ver17) are handled differently based on package type:

| Package Type | Conversion | Notes |
| --- | --- | --- |
| **Local** (single reference) | Inline execution within parent TASK | Package logic expanded inline |
| **Reusable** (2+ references or parameters) | CALL to stored procedure | Enables synchronous execution with parameters; generates [FDM SSC-FDM-SSIS0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0005) |
| **External** | CALL with path resolution | Generates [EWI SSC-EWI-SSIS0008](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0008) for manual verification |

**Asynchronous execution note:**

TASK-based Execute Package conversions run asynchronously. For synchronous behavior, packages are converted to stored procedures. See [EWI SSC-EWI-SSIS0005](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0005).

### Send Mail Task[¶](#send-mail-task "Link to this heading")

[Send Mail Tasks](https://learn.microsoft.com/en-us/sql/integration-services/control-flow/send-mail-task?view=sql-server-ver17) are converted to Snowflake Tasks that use `SYSTEM$SEND_EMAIL` with a dynamically created Notification Integration.

#### Key Differences from SSIS[¶](#key-differences-from-ssis "Link to this heading")

| Aspect | SSIS | Snowflake |
| --- | --- | --- |
| Email Service | Custom SMTP server | Snowflake’s built-in email service |
| Configuration | SMTP Connection Manager | Notification Integration |
| Sender Address | Custom FROM address | Fixed by Snowflake account |
| CC/BCC Support | Full support | Not supported (merged into recipients) |
| Attachments | File attachments supported | Not supported |
| HTML Body | Supported | Plain text only |
| Priority | High/Normal/Low | Not supported |

#### Property Mapping[¶](#property-mapping "Link to this heading")

| SSIS Property | Snowflake Equivalent | Notes |
| --- | --- | --- |
| ToLine | `ALLOWED_RECIPIENTS` + recipients parameter | Direct mapping |
| FromLine | Prepended to message body | [FDM SSC-FDM-SSIS0008](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0008) |
| CCLine | Added to recipients list | [FDM SSC-FDM-SSIS0009](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0009) |
| BCCLine | Added to recipients list | [FDM SSC-FDM-SSIS0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0010) (privacy concern) |
| Subject | `subject` parameter | Direct mapping |
| MessageSource | `message` parameter | Direct mapping |
| MessageSourceType (DirectInput) | Supported | - |
| MessageSourceType (Variable) | Supported | Variable reference converted |
| MessageSourceType (FileConnection) | Not supported | [EWI SSC-EWI-SSIS0017](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0017) |
| Priority | Not supported | [EWI SSC-EWI-SSIS0016](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0016) |
| FileAttachments | Not supported | [EWI SSC-EWI-SSIS0015](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0015) |
| SMTPConnection | Managed by Snowflake | [FDM SSC-FDM-SSIS0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0007) |
| BodyFormat (HTML) | Not supported | [EWI SSC-EWI-SSIS0018](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0018) |

#### Conversion Output Structure[¶](#conversion-output-structure "Link to this heading")

Each Send Mail Task is converted to a Snowflake Task containing:

1. **Notification Integration Creation**: Created dynamically via `EXECUTE IMMEDIATE`
2. **SYSTEM$SEND\_EMAIL Call**: Sends the email through the integration

```
CREATE OR REPLACE TASK public.my_package_send_mail_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.my_package
AS
BEGIN
   -- Step 1: Create Notification Integration dynamically
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com", "team@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   
   -- Step 2: Send the email
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com,team@example.com', 'Subject', 'Message body');
END;
```

Copy

#### Conversion Examples[¶](#conversion-examples "Link to this heading")

**Basic Email (To, Subject, Body):**

```
BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("admin@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'admin@example.com', 'Daily Report', 'The daily report is ready.');
END;
```

Copy

**Email with FROM Address:**

```
BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("noreply@company.com", "admin@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   --** SSC-FDM-SSIS0008 - SNOWFLAKE'S EMAIL INTEGRATION USES A FIXED SENDER ADDRESS. THE ORIGINAL FROM ADDRESS HAS BEEN PREPENDED TO THE MESSAGE BODY FOR REFERENCE. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'noreply@company.com,admin@example.com', 'Notification', 'Email sent by: noreply@company.com

Package completed successfully.');
END;
```

Copy

**Email with Multiple Features (attachments, priority, CC):**

```
BEGIN
   BEGIN
      LET my_package_Send_Mail_Task_integration_sql STRING := 'CREATE OR REPLACE NOTIFICATION INTEGRATION my_package_Send_Mail_Task
  TYPE=EMAIL
  ENABLED=TRUE
  ALLOWED_RECIPIENTS=("noreply@company.com", "admin@example.com", "team@example.com")';
      EXECUTE IMMEDIATE :my_package_Send_Mail_Task_integration_sql;
   END;
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0015 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT FILE ATTACHMENTS. CONSIDER USING STAGED FILES WITH SHARED LINKS OR ALTERNATIVE DELIVERY METHODS. ***/!!!
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0016 - EMAIL PRIORITY SETTINGS (HIGH/NORMAL/LOW) ARE NOT SUPPORTED BY SYSTEM$SEND_EMAIL AND WILL BE IGNORED. ***/!!!
   --** SSC-FDM-SSIS0008 - SNOWFLAKE'S EMAIL INTEGRATION USES A FIXED SENDER ADDRESS. THE ORIGINAL FROM ADDRESS HAS BEEN PREPENDED TO THE MESSAGE BODY FOR REFERENCE. **
   --** SSC-FDM-SSIS0009 - SNOWFLAKE'S SYSTEM$SEND_EMAIL DOES NOT SUPPORT CC ADDRESSING. ALL CC RECIPIENTS HAVE BEEN ADDED TO THE MAIN RECIPIENTS LIST. **
   CALL SYSTEM$SEND_EMAIL('my_package_Send_Mail_Task', 'noreply@company.com,admin@example.com,team@example.com', 'Monthly Report', 'Email sent by: noreply@company.com

Please review the attached monthly report.');
END;
```

Copy

#### Prerequisites for Snowflake Email[¶](#prerequisites-for-snowflake-email "Link to this heading")

Before using converted Send Mail Tasks:

1. **Email Notification Integration permissions**: Account admin must grant `CREATE INTEGRATION ON ACCOUNT` to the executing role
2. **Recipient verification**: All email addresses in `ALLOWED_RECIPIENTS` must be verified in Snowflake
3. **Update warehouse name**: Replace `DUMMY_WAREHOUSE` with your actual warehouse name

#### Workarounds for Unsupported Features[¶](#workarounds-for-unsupported-features "Link to this heading")

**File Attachments:**

Upload files to a Snowflake stage and share links instead:

```
-- Upload file to stage
PUT file://report.pdf @my_stage;

-- Get shareable link (valid for 1 hour)
LET file_url STRING := GET_PRESIGNED_URL(@my_stage, 'report.pdf', 3600);

-- Include link in email body
CALL SYSTEM$SEND_EMAIL('my_integration', 'admin@example.com', 'Report Available', 
  'Download the report from: ' || :file_url);
```

Copy

**BCC Privacy:**

Send separate emails to maintain recipient privacy:

```
-- Send to main recipients
CALL SYSTEM$SEND_EMAIL('my_integration', 'admin@example.com', 'Subject', 'Message');

-- Send separately to BCC recipients
CALL SYSTEM$SEND_EMAIL('my_integration', 'audit@example.com', 'Subject', 'Message');
```

Copy

### dbt Project Execution[¶](#dbt-project-execution "Link to this heading")

Within the orchestration code, Data Flow Tasks are executed using Snowflake’s [`EXECUTE DBT PROJECT`](../../../../sql-reference/sql/execute-dbt-project) command:

```
EXECUTE DBT PROJECT schema.project_name ARGS='build --target dev'
```

Copy

**Important requirements:**

* The `project_name` must match the name you used when deploying the dbt project (via `CREATE DBT PROJECT` or Snowflake Workspace deployment)
* Arguments passed are standard dbt CLI arguments (like `build`, `run`, `test`)
* Each execution runs the entire dbt project with all models in dependency order

**Deployment:**

Before executing dbt projects in orchestration, deploy them using:

* Snowflake CLI: `snow dbt deploy --schema schema_name --database database_name --force package_name`
* Snowflake Workspace: Upload and deploy via UI

For complete deployment instructions, see the [user guide](../../general/user-guide/etl-migration-replatform).

## Data Flow Components[¶](#data-flow-components "Link to this heading")

These SSIS Data Flow sources, transformations, and destinations are supported:

| Component | Category | dbt Mapping | Model Naming | Notes |
| --- | --- | --- | --- | --- |
| **Source Components** |  |  |  |  |
| [Microsoft.OLEDBSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/ole-db-source?view=sql-server-ver17) | Source | Staging Model | `stg_raw__{component_name}` | - |
| [Microsoft.FlatFileSource](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/flat-file-source?view=sql-server-ver17) | Source | Staging Model | `stg_raw__{component_name}` | - |
| **Transformation Components** |  |  |  |  |
| [Microsoft.DerivedColumn](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/derived-column-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (SELECT with expressions) | `int_{component_name}` | - |
| [Microsoft.DataConvert](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/data-conversion-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (CAST expressions) | `int_{component_name}` | - |
| [Microsoft.Lookup](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/lookup-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (LEFT JOIN) | `int_{component_name}` | Might present functional differences for ORDER BY requirements. Check [FDM SSC-FDM-SSIS0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0001) for more information |
| [Microsoft.UnionAll](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/union-all-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (UNION ALL) | `int_{component_name}` | - |
| [Microsoft.Merge](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/merge-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (UNION ALL) | `int_{component_name}` | Might present functional differences for sorted output. Check [FDM SSC-FDM-SSIS0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0002) for more information |
| [Microsoft.MergeJoin](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/merge-join-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (JOIN) | `int_{component_name}` | Might present functional differences for ORDER BY requirements. Check [FDM SSC-FDM-SSIS0004](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/ssisFDM.html#ssc-fdm-ssis0004) for more information |
| [Microsoft.ConditionalSplit](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/conditional-split-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (Router pattern with CTEs) | `int_{component_name}` | - |
| [Microsoft.Multicast](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/multicast-transformation?view=sql-server-ver17) | Transformation | Intermediate Model (SELECT pass-through) | `int_{component_name}` | - |
| [Microsoft.RowCount](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/row-count-transformation?view=sql-server-ver17) | Transformation | Intermediate Model with macro | `int_{component_name}` | Uses m\_update\_row\_count\_variable macro |
| **Destination Components** |  |  |  |  |
| [Microsoft.OLEDBDestination](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/ole-db-destination?view=sql-server-ver17) | Destination | Mart Model (table) | `{target_table_name}` | - |
| [Microsoft.FlatFileDestination](https://learn.microsoft.com/en-us/sql/integration-services/data-flow/flat-file-destination?view=sql-server-ver17) | Destination | Mart Model (table) | `{target_table_name}` | - |

**Note**: Unlisted Data Flow components generate EWI [SSC-EWI-SSIS0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/ssisEWI.html#ssc-ewi-ssis0001).

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

1. [Control Flow Elements](#control-flow-elements)
2. [Data Flow Components](#data-flow-components)