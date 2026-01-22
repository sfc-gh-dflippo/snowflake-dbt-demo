---
auto_generated: true
description: This topic explains the ways you can use monitoring features for dbt
  Projects on Snowflake to inspect dbt project executions—–manual or task-scheduled–—and
  how to view logs and artifacts.
last_scraped: '2026-01-14T16:57:48.076765+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability
title: Monitor dbt Projects on Snowflake | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](dbt-projects-on-snowflake.md)

      * Tutorials

        * [Tutorial: Getting started with dbt Projects](../tutorials/dbt-projects-on-snowflake-getting-started-tutorial.md)
        * [Tutorial: Set up CI/CD integrations on dbt Projects](../tutorials/dbt-projects-on-snowflake-ci-cd-tutorial.md)
      * Key concepts

        * [Understanding dbt dependencies](dbt-projects-on-snowflake-dependencies.md)
        * [Understanding schema generation and customization](dbt-projects-on-snowflake-schema-customization.md)
        * [Using workspaces for dbt Projects on Snowflake](dbt-projects-on-snowflake-using-workspaces.md)
        * [Understanding dbt project objects](dbt-projects-on-snowflake-understanding-dbt-project-objects.md)
      * [Access control](dbt-projects-on-snowflake-access-control.md)
      * dbt Project operations

        * [Deploying dbt projects](dbt-projects-on-snowflake-deploy.md)
        * [Scheduling project runs](dbt-projects-on-snowflake-schedule-project-execution.md)
      * [CI/CD integrations on dbt Projects](dbt-projects-on-snowflake-ci-cd.md)
      * [Managing dbt Projects](dbt-projects-on-snowflake-manage.md)
      * [Monitoring & observability](dbt-projects-on-snowflake-monitoring-observability.md)
      * Supported commands and limitations

        * [Supported dbt commands and flags](dbt-projects-on-snowflake-supported-commands.md)
        * [Supported source file locations](dbt-projects-on-snowflake-sources.md)
        * [Limitations](dbt-projects-on-snowflake-limitations.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)Data engineering[dbt Projects on Snowflake](dbt-projects-on-snowflake.md)Monitoring & observability

# Monitor dbt Projects on Snowflake[¶](#monitor-dbt-projects-on-snowflake "Link to this heading")

This topic explains the ways you can use monitoring features for dbt Projects on Snowflake to inspect dbt project executions—–manual or task-scheduled–—and how to view logs and artifacts.

| Section | Description |
| --- | --- |
| [Enable monitoring features for dbt projects](#label-dbt-monitoring-observability-enable) | Capture logging and tracing events for a dbt project object and for any scheduled task that runs it. To enable this feature, you must set logging, tracing, and metrics on the schema where the dbt project object and task are deployed. |
| [Monitor scheduled executions of dbt project objects](#label-dbt-projects-monitoring-tasks) | In Snowsight, in the navigation menu, select Transformation » dbt Projects to view run history, task graphs, and query details for dbt project objects. When a workspace is connected to a dbt project object that runs according to a task schedule, you can open task-run history and task graphs from within the workspace. |
| [Access dbt artifacts and logs programmatically](#label-dbt-projects-artifacts-and-logs) | Use the DBT\_PROJECT\_EXECUTION\_HISTORY table function and dbt system functions to access dbt artifacts and logs programmatically. |

## Enable monitoring features for dbt projects[¶](#enable-monitoring-features-for-dbt-projects "Link to this heading")

To enable monitoring features for your dbt project object, set LOG\_LEVEL, TRACE\_LEVEL, and METRIC\_LEVEL on the database and schema where your dbt project object is created, as shown in the following SQL example:

```
ALTER SCHEMA my_db.my_dbt_project_schema SET LOG_LEVEL = 'INFO';
ALTER SCHEMA my_db.my_dbt_project_schema SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA my_db.my_dbt_project_schema SET METRIC_LEVEL = 'ALL';
```

Copy

## Monitor scheduled executions of dbt project objects[¶](#monitor-scheduled-executions-of-dbt-project-objects "Link to this heading")

When you use a task to run a dbt project on a schedule and have a workspace connected to a dbt project object, you can use the workspace for dbt Projects on Snowflake to quickly access monitoring information for task-run history and a task graph, if applicable.

Note

This feature is only available for workspaces that are connected to a dbt project object.

**To monitor scheduled execution of a dbt project object from a workspace:**

1. From the dbt project menu in the upper right of the workspace editor, under Scheduled runs, choose View schedules.
2. From the list, select the schedule (task) that you want to inspect, and then choose View details.

   The information pane for the task opens, where you can view Task details, the task Graph (if applicable), and Run history of this task. For more information, see [Viewing tasks and task graphs in Snowsight](../ui-snowsight-tasks).
3. From the Run history for any scheduled dbt project run in the list, select the Open query history button on the far right to view query details, the query profile, and the query telemetry for the run. For more information, see [Review details and profile of a specific query](../ui-snowsight-activity.html#label-snowsight-specific-query-details).

## Monitor dbt projects in Snowsight[¶](#monitor-dbt-projects-in-sf-web-interface "Link to this heading")

You can use Monitoring in Snowsight to view detailed monitoring information about dbt project executions (runs). You must have privileges to view monitoring information for the dbt project object.

1. In the navigation menu, select Transformation » dbt Projects. A histogram shows the frequency of dbt project runs and a list of projects that have run.

   The list of dbt projects includes columns with the following information. You can filter the list by date range, command, and run status.

   * PROJECT - The name of the dbt project object and the number of executions (runs) in the selected time period.
   * LAST COMMAND - The dbt command that executed during the last run.
   * LAST RUN STATUS - The result of the run: Succeeded, Executing, or Failed.
   * LAST RUN - The elapsed time since the last run. To reverse the sort order, select the column header. The most recent run is shown first by default.
   * PREVIOUS RUNS - The number of runs in the selected time period by status.
   * DATABASE and SCHEMA - The database and schema where the dbt project object is saved.
   * LAST RUN PARAMETERS - The dbt command-line arguments (ARGS) specified in the EXECUTE DBT PROJECT command for the last dbt project run.
2. To inspect individual project runs, select a dbt project object from the list.

   The dbt project details page in the database object explorer opens for that dbt project object.

   The Run history tab is selected by default, with the following information for each job run in the selected time period:

   * COMMAND - The dbt command that executed during the last run.
   * STATUS - The result of the run: Succeeded, Executing, or Failed.
   * RUN TIME - The elapsed time since the last run. To reverse the sort order, select the column header. The most recent run is shown first by default.
   * PARAMETERS The dbt command-line arguments (ARGS) specified in the EXECUTE DBT PROJECT command for the last dbt project run.
3. To see job details for a run, select it from the list.

   The dbt run details pane opens, which includes the following tabs:

   * The Job details tab is selected by default and displays the following information:

     + Status - The result of the run: Succeeded, Executing, or Failed..
     + Start time, End time, and Duration - The time that the run started, the time it ended, and how long it took to run.
     + Warehouse size - The size of the warehouse that was used to execute the run.
     + Query ID - The unique identifier for the query that executed the dbt project command. To view the query details in query history, select the query ID.
     + SQL text - The EXECUTE DBT PROJECT command that executed.
     + dbt <command> - For the dbt command that ran (for example, `run` or `build`), shows the dbt model, the time taken for the run to execute, and the status of that model run.
   * The Output tab shows the stdout generated by the dbt project during the run.
   * The Trace tab shows the trace information generated by the dbt project during the run. For more information about traces, see [Viewing trace data](../../developer-guide/logging-tracing/tracing-accessing-events).
4. To see more detailed query information, from the Job details tab, select the Query ID.

   The query history page for the job run query opens with tabs to view Query Details, the Query Profile, and Query Telemetry for the dbt run that you selected.

   For more information, see [Review details and profile of a specific query](../ui-snowsight-activity.html#label-snowsight-specific-query-details).

## Access dbt artifacts and logs programmatically[¶](#access-dbt-artifacts-and-logs-programmatically "Link to this heading")

Use the [DBT\_PROJECT\_EXECUTION\_HISTORY](../../sql-reference/functions/dbt_project_execution_history) table function and the following system functions to access dbt artifacts and logs programmatically.

| Function | What it returns | Typical use | Notes |
| --- | --- | --- | --- |
| [SYSTEM$GET\_DBT\_LOG](../../sql-reference/functions/system_get_dbt_log) | Text log output (the run’s log tail) | Quick debugging in SQL. For example, see errors and warnings without downloading files. | Returns log content; nothing is created or moved. |
| [SYSTEM$LOCATE\_DBT\_ARTIFACTS](../../sql-reference/functions/system_locate_dbt_artifacts) | Folder path (for example, `snow://…/results/query_id_…/`) containing artifact files such as `manifest.json`, compiled SQL, logs. | Browse or copy specific files with LIST, GET, or COPY FILES. | Just a locator (a URL); you still run GET/COPY FILES to fetch. |
| [SYSTEM$LOCATE\_DBT\_ARCHIVE](../../sql-reference/functions/system_locate_dbt_archive) | Single ZIP file URL (for example, `…/dbt_artifacts.zip`). | Handy when you want to download one file (for example, with GET). | Use `GET '<url>' file:///local/dir` to download. |

### Get logs and download a ZIP file of the latest dbt project query[¶](#get-logs-and-download-a-zip-file-of-the-latest-dbt-project-query "Link to this heading")

The following example queries Snowflake’s dbt execution history to show the most recent query ID for the dbt Project. It pulls the log output
for that execution and returns the location of the zipped dbt artifacts for that execution.

The Snowflake CLI example downloads the artifacts ZIP file or specific files (like `manifest.json`) to your local folder using GET.

To download the ZIP file from Snowsight, navigate to Monitoring » Query History. Select the query, navigate to Query Details,
and select Download Build Artifacts under dbt Output.

You must use a role with the OWNERSHIP, USAGE, or MONITOR privilege on your dbt Projects.

SQLSnowflake CLI

```
--Look up the most recent dbt Project execution
SET latest_query_id = (SELECT query_id
   FROM TABLE(INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY())
   WHERE OBJECT_NAME = 'MY_DBT_PROJECT'
   ORDER BY query_end_time DESC LIMIT 1);

--Get the dbt run logs for the most recent dbt Project execution
SELECT SYSTEM$GET_DBT_LOG($latest_query_id);
```

Copy

```
============================== 15:14:53.100781 | 46d19186-61b8-4442-8339-53c771083f16 ==============================
[0m15:14:53.100781 [info ] [Dummy-1   ]: Running with dbt=1.9.4
...
[0m15:14:58.198545 [debug] [Dummy-1   ]: Command `cli run` succeeded at 15:14:58.198121 after 5.19 seconds
```

To view the stage path where Snowflake stored the dbt Project run’s artifacts (that is, the results folder for that execution), use the
SYSTEM$LOCATE\_DBT\_ARTIFACTS function. You can then use that path with `GET` or `COPY FILES` with the Snowflake CLI to download
things like `manifest.json`, compiled SQL, or logs.

```
--Get the location of the dbt Project archive ZIP file (see all files)
SELECT SYSTEM$LOCATE_DBT_ARTIFACTS($latest_query_id);
```

Copy

```
+-------------------------------------------------------------------------------------------------+
| SYSTEM$LOCATE_DBT_ARTIFACTS($LATEST_QUERY_ID)                                                   |
+-------------------------------------------------------------------------------------------------+
| snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01c01096-010c-0ccb-0000-a99506bd199e/ |
+-------------------------------------------------------------------------------------------------+
```

```
--List all the files of a dbt run
ls 'snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f5a-010b-4d87-0000-53493abb7cce/';
```

Copy

You can also create a fresh internal stage, locate the Snowflake-managed path for the specified dbt Project run’s artifacts, and copy those
artifacts into your stage for retrieval, as shown in the following example:

```
CREATE OR REPLACE STAGE my_dbt_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

SELECT SYSTEM$LOCATE_DBT_ARTIFACTS($latest_query_id);
```

Copy

```
snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf51c1-010b-5676-0000-53493ae6db02/
```

```
COPY FILES INTO @my_dbt_stage/results/ FROM 'snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf51c1-010b-5676-0000-53493ae6db02/';
```

Copy

```
results/dbt_artifacts.zip
results/logs/dbt.log
results/target/manifest.json
results/target/semantic_manifest.json
```

```
snowsql -q "SELECT query_id
   FROM TABLE(INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY())
   WHERE OBJECT_NAME = 'MY_DBT_PROJECT'
   ORDER BY query_end_time DESC LIMIT 1;"

snowsql -q "SELECT SYSTEM\$GET_DBT_LOG('01bf3f89-0300-0001-0000-0000000c1229')"
```

Copy

```
| ============================== 11:17:39.152234 | 4df65841-7aa3-40e2-81cb-2007c09c2b81
| 11:17:39.152234 [info ] [Dummy-1   ]: Running with dbt=1.9.4
....
```

```
snowsql -q "SELECT SYSTEM\$LOCATE_DBT_ARCHIVE('01bf3f89-0300-0001-0000-0000000c1229')"
```

Copy

```
snow://dbt_project/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip
```

```
snowsql -q "GET 'snow://dbt_project/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip' file:///Users/user_name/Code/temp"
```

Copy

```
Type SQL statements or !help
+-----------------------------------------------------------------+--------+------------+-----
| file                                                            |   size | status    | ....
|-----------------------------------------------------------------+--------+------------+-----
| query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip | 137351 | DOWNLOADED |...
+-----------------------------------------------------------------+--------+------------+-----
```

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Enable monitoring features for dbt projects](#enable-monitoring-features-for-dbt-projects)
2. [Monitor scheduled executions of dbt project objects](#monitor-scheduled-executions-of-dbt-project-objects)
3. [Monitor dbt projects in Snowsight](#monitor-dbt-projects-in-sf-web-interface)
4. [Access dbt artifacts and logs programmatically](#access-dbt-artifacts-and-logs-programmatically)

Related content

1. [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake)
2. [EXECUTE DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/execute-dbt-project)