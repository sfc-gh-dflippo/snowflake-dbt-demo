---
auto_generated: true
description: Creates a new task in the current/specified schema or replaces an existing
  task.
last_scraped: '2026-01-14T16:54:57.504672+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-task
title: CREATE TASK | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)

     + Stream
     + [CREATE STREAM](create-stream.md)
     + [ALTER STREAM](alter-stream.md)
     + [DESCRIBE STREAM](desc-stream.md)
     + [DROP STREAM](drop-stream.md)
     + [SHOW STREAMS](show-streams.md)
     + Task
     + [CREATE TASK](create-task.md)
     + [DESCRIBE TASK](desc-task.md)
     + [ALTER TASK](alter-task.md)
     + [DROP TASK](drop-task.md)
     + [EXECUTE TASK](execute-task.md)
     + [SHOW TASKS](show-tasks.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Streams & tasks](../commands-stream.md)CREATE TASK

# CREATE TASK[¶](#create-task "Link to this heading")

Creates a new [task](../../user-guide/tasks-intro) in the current/specified schema or replaces an existing task.

This command supports the following variants:

* [CREATE OR ALTER TASK](#label-create-or-alter-task-syntax): Creates a task if it doesn’t exist or alters an existing task.
* [CREATE TASK … CLONE](#label-create-task-clone-syntax): Creates a clone of an existing task.

See also:
:   [ALTER TASK](alter-task) , [DROP TASK](drop-task) , [SHOW TASKS](show-tasks) , [DESCRIBE TASK](desc-task)

    [CREATE OR ALTER <object>](create-or-alter)

Important

Newly created or cloned tasks are created suspended. For information about running suspended tasks, see [ALTER TASK … RESUME](alter-task) or [EXECUTE TASK](execute-task).

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
    [ WITH TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
    [ { WAREHOUSE = <string> }
      | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
    [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
      | 'USING CRON <expr> <time_zone>' } ]
    [ CONFIG = <configuration_string> ]
    [ ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE ]
    [ <session_parameter> = <value>
      [ , <session_parameter> = <value> ... ] ]
    [ USER_TASK_TIMEOUT_MS = <num> ]
    [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
    [ ERROR_INTEGRATION = <integration_name> ]
    [ SUCCESS_INTEGRATION = <integration_name> ]
    [ LOG_LEVEL = '<log_level>' ]
    [ COMMENT = '<string_literal>' ]
    [ FINALIZE = <string> ]
    [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
    [ USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = <num> ]
    [ TARGET_COMPLETION_INTERVAL = '<num> { HOURS | MINUTES | SECONDS }' ]
    [ SERVERLESS_TASK_MIN_STATEMENT_SIZE = '{ XSMALL | SMALL
      | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
    [ SERVERLESS_TASK_MAX_STATEMENT_SIZE = '{ XSMALL | SMALL
      | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
  [ AFTER <string> [ , <string> , ... ] ]
  [ EXECUTE AS USER <user_name> ]
  [ WHEN <boolean_expr> ]
  AS
    <sql>
```

Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

### CREATE OR ALTER TASK[¶](#create-or-alter-task "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Creates a new task if it doesn’t already exist, or transforms an existing task into the task defined in the statement.
A CREATE OR ALTER TASK statement follows the syntax rules of a CREATE TASK statement and has the same limitations as an
[ALTER TASK](alter-task) statement.

Supported task alterations include:

* Change task properties and parameters. For example, SCHEDULE, USER\_TASK\_TIMEOUT\_MS, or COMMENT.
* Set, unset, or change task predecessors.
* Set, unset, or change task condition (WHEN clause).
* Change the task definition (AS clause).

For more information, see [CREATE OR ALTER TASK usage notes](#label-create-or-alter-task-usage-notes).

```
CREATE OR ALTER TASK <name>
    [ { WAREHOUSE = <string> }
      | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
    [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
      | 'USING CRON <expr> <time_zone>' } ]
    [ CONFIG = <configuration_string> ]
    [ ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE ]
    [ USER_TASK_TIMEOUT_MS = <num> ]
    [ <session_parameter> = <value>
      [ , <session_parameter> = <value> ... ] ]
    [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
    [ ERROR_INTEGRATION = <integration_name> ]
    [ SUCCESS_INTEGRATION = <integration_name> ]
    [ COMMENT = '<string_literal>' ]
    [ FINALIZE = <string> ]
    [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ AFTER <string> [ , <string> , ... ] ]
  [ WHEN <boolean_expr> ]
  AS
    <sql>
```

Copy

### CREATE TASK … CLONE[¶](#create-task-clone "Link to this heading")

Creates a new task with the same parameter values:

> ```
> CREATE [ OR REPLACE ] TASK <name> CLONE <source_task>
>   [ ... ]
> ```
>
> Copy

For more details, see [CREATE <object> … CLONE](create-clone).

Note

Cloning tasks using CREATE TASK <name> CLONE, or cloning a schema containing tasks,
copies all underlying task properties unless explicitly overridden.

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   String that specifies the identifier for the task; must be unique for the schema in which the task is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes, such as `"My object"`. Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

`sql`
:   Any one of the following:

    * Single SQL statement
    * Call to a stored procedure
    * Procedural logic using [Snowflake Scripting](../../developer-guide/snowflake-scripting/index)

    The SQL code is executed when the task runs. Verify that the `{sql}` executes as expected before using it in a task.

### Clone tasks in a task graph[¶](#clone-tasks-in-a-task-graph "Link to this heading")

> For task graphs, you might also need to make clones of each dependent task (that is, each child task or finalizer task); for example:
>
> 1. Clone the task (for example, `CREATE TASK new_task_name CLONE old_task_name`).
> 2. Find dependent tasks by using the [TASK\_DEPENDENTS](../functions/task_dependents) function; for example:
>
>    ```
>    SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_DEPENDENTS('old_task_name'));
>    ```
>
>    Copy
> 3. Clone the dependent tasks (for example, `CREATE TASK new_child_task CLONE old_child_task`).
> 4. Update the new dependent tasks to use the new cloned task name (`ALTER TASK new_child_task ADD AFTER new_task_name`).

## Optional parameters[¶](#optional-parameters "Link to this heading")

`CREATE OR REPLACE TASK` or . `CREATE TASK IF NOT EXISTS`

> * `..OR REPLACE`
>   Replaces an existing task with the same name. If the task doesn’t exist, this clause is ignored.
>
>   Consider the following behaviors when you replace a task:
>
>   + The recreated task is suspended by default.
>   + If a standalone or root task is recreated, the next scheduled run of the task is cancelled.
>   + CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
>   + Tasks with large definitions can cause errors. If you experience an error due to task size, try using stored procedure or making your task definition less complex.
>
>   When you replace a task, any ongoing task run is completed.
>
>   + To stop an ongoing task run before replacing it with CREATE OR REPLACE TASK, use the [SYSTEM$USER\_TASK\_CANCEL\_ONGOING\_EXECUTIONS](../functions/system_user_task_cancel_ongoing_executions) function.
>   + To stop an ongoing task run after you replace it with CREATE OR REPLACE TASK:
>
>     1. Find the query ID of the ongoing run; for example:
>
>        ```
>        select name, query_id, state, scheduled_time, error_message
>        from table(information_schema.task_history(task_name => 'my_task'));
>        ```
>
>        Copy
>     2. Cancel the query using the [SYSTEM$CANCEL\_QUERY](../functions/system_cancel_query) function with the query ID, for example:
>
>        ```
>        select system$cancel_query('query_id');
>        ```
>
>        Copy
>     3. Monitor the task run for a few seconds until the cancel completes, for example:
>
>        ```
>        select name, query_id, state, scheduled_time, error_message
>        from table(information_schema.task_history(task_name => 'my_task'));
>        ```
>
>        Copy
> * `...IF NOT EXISTS`
>   Creates a new task only if a task with the same name doesn’t already exist. If the task already exists, this clause is ignored.
>
> Note
>
> * The `CREATE OR REPLACE` and `CREATE IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.

`WAREHOUSE = string` or . `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string`

> `WAREHOUSE = string`
> :   Specifies the virtual warehouse that provides compute resources for task runs.
>
>     Omit this parameter to use serverless compute resources for runs of this task. Snowflake automatically resizes and scales serverless
>     compute resources as required for each workload. When a schedule is specified for a task, Snowflake adjusts the resource size to
>     complete future runs of the task within the specified time frame. To specify the initial warehouse size for the task, set the
>     `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string` parameter.
>
> `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string`
> :   Applied only to serverless tasks.
>
>     Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for
>     Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting.
>
>     Note that if the task history is unavailable for a given task, the compute resources revert to this initial size.
>
>     Note
>
>     If a `WAREHOUSE = string` parameter value is specified, then setting this parameter produces a user error.
>
>     The size is equivalent to the compute resources available when creating a warehouse (using
>     [CREATE WAREHOUSE](create-warehouse)), such as `SMALL`, `MEDIUM`, or `LARGE`. The largest size supported by the parameter
>     is `XXLARGE`. If the parameter is omitted, the first runs of the task are executed using a medium-sized (`MEDIUM`) warehouse.
>
>     You can change the initial size (using [ALTER TASK](alter-task)) after the task is created but
>     before it has run successfully once. Changing the parameter after the first run of this task starts has no effect on the
>     compute resources for current or future task runs.
>
>     Note that suspending and resuming a task doesn’t remove the task history used to size the compute resources. The task history is
>     only removed if the task is recreated (using the CREATE OR REPLACE TASK syntax).
>
>     For more information about this parameter, see [USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE](../parameters.html#label-user-task-managed-initial-warehouse-size).

`SCHEDULE = ...`
:   Specifies the schedule for periodically running the task:

    Note

    * For [Triggered tasks](../../user-guide/tasks-triggered), a schedule is not required. For other tasks, a schedule must be defined for a standalone task or the root task in a [task graph](../../user-guide/tasks-graphs.html#label-task-dag);
      otherwise, the task only runs if manually executed using [EXECUTE TASK](execute-task).
    * A schedule cannot be specified for child tasks in a task graph.

    * `'USING CRON expr time_zone'`
      :   Specifies a cron expression and time zone for periodically running the task. Supports a subset of standard cron utility syntax.

      + `'expr'`: The cron expression consists of the following fields:

        ```
        # __________ minute (0-59)
        # | ________ hour (0-23)
        # | | ______ day of month (1-31, or L)
        # | | | ____ month (1-12, JAN-DEC)
        # | | | | __ day of week (0-6, SUN-SAT, or L)
        # | | | | |
        # | | | | |
          * * * * *
        ```

        Copy

        The following special characters are supported:

        `*`
        :   Wildcard. Specifies any occurrence of the field.

        `L`
        :   Stands for “last”. When used in the day-of-week field, it allows you to specify constructs such as “the last Friday” (“5L”) of
            a given month. In the day-of-month field, it specifies the last day of the month.

        `/n`
        :   Indicates the *nth* instance of a given unit of time. Each quanta of time is computed independently. For example, if `4/3` is
            specified in the month field, then the task is scheduled for April, July, and October, which is every 3 months, starting with the
            4th month of the year. The same schedule is maintained in subsequent years. That is, the task is not scheduled to run in
            January (3 months after the October run).

        Timing examples:

        | SCHEDULE Value | Description |
        | --- | --- |
        | `* * * * * UTC` | Every minute. UTC time zone. |
        | `0/5 * * * * UTC` | Every five minutes, starting at the top of the hour. UTC time zone. |
        | `5 * * * * UTC` | The 5th minute of every hour. UTC time zone. |
        | `30 3 * * * UTC` | Every night at 3:30 a.m. UTC time zone. |
        | `0 6,18 * * * UTC` | Twice daily, at 6:00 a.m. and 6:00 p.m.UTC time zone. |
        | `0 3 * * MON-FRI UTC` | Weekdays at 3:00 a.m. UTC time zone. |
        | `0 0 1 * * UTC` | At midnight on the first day of every month. UTC time zone. |
        | `0 0 L * * UTC` | At midnight on the last day of every month. UTC time zone. |
      > Note
      >
      > + The cron expression defines all valid run times for the task. Snowflake attempts to run a task based on this schedule;
      >   however, any valid run time is skipped if a previous run hasn’t completed before the next valid run time starts.
      > + When both a specific day of month and day of week are included in the cron expression, then the task is scheduled on days
      >   satisfying either the day of month or day of week. For example, `SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'`
      >   schedules a task at midnight on any 10th to 20th day of the month and also on any Tuesday or Thursday outside of those dates.
      > + The shortest granularity of time in cron is minutes. To set a task to run in a shorter interval, use the `SCHEDULE = ' <num> SECONDS'` parameter instead. For example, `SCHEDULE = '10 SECONDS'` runs the task every 10 seconds.
      > + If a task is resumed during the minute defined in its cron expression,
      >   the first scheduled run of the task is the next occurrence of the instance of the cron expression. For example, if task
      >   scheduled to run daily at midnight (`USING CRON 0 0 * * *`) is resumed at midnight plus 5 seconds (`00:00:05`), the
      >   first task run is scheduled for the following midnight.

      + `'time_zone'`: The cron time zone for the task. The time zone is specified as a string literal. For a list of time zones, see the [list of tz database time zones](https://wikipedia.org/wiki/List_of_tz_database_time_zones)
        (in Wikipedia). Example:

        | SCHEDULE Value | Description |
        | --- | --- |
        | `0 3 * * * America/Los_Angeles` | Every night at 3:00 a.m., Pacific Standard Time / Pacific Daylight Time (PST/PDT) time zone |

        Note

        - The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](../parameters.html#label-timezone) parameter value for the account (or setting the value at the user or session level) does *not* change the time zone for the task.
        - For time zones that observe daylight saving time, tasks scheduled during daylight saving time transitions can have unexpected behaviors. Examples:
        - During the change from daylight saving time to standard time, a task scheduled to start at 1:00 a.m. in the America/Los\_Angeles time zone (`0 1 * * * America/Los_Angeles`) would run twice: at 1:00 a.m., and then again when 1:59:59 a.m. shifts to 1:00:00 a.m. local time.
        - During the change from standard time to daylight saving time, a task scheduled to start at 2:00 a.m. in the America/Los\_Angeles time zone (`0 2 * * * America/Los_Angeles`) would not run because the local time shifts from 1:59:59 a.m. to 3:00:00 a.m.

        To avoid unexpected task executions due to daylight saving time, consider the following:

        - Don’t schedule tasks to start between 1:00 a.m. and 2:59 a.m.
        - Manually adjust the cron expression for tasks scheduled between 1 a.m. and 3 a.m. twice each year to compensate for the time change.
        - Use a time format that does not apply daylight saving time, such as UTC. Do not change the time zone for the task.

    > * `'num { HOURS | MINUTES | SECONDS }'`
    >   :   Specifies an interval of wait time between runs of the task.
    >
    >       Snowflake sets the base interval time when the task is resumed ([ALTER TASK … RESUME](alter-task)) or when a different interval is set ([ALTER TASK … SET SCHEDULE](alter-task)).
    >
    >       For example, if an INTERVAL value of `10 MINUTES` is set and the task is enabled at 9:03 a.m., then the task runs at 9:13 a.m., 9:23 a.m., and
    >       so on.
    >
    >       Snowflake ensures that a task won’t run before the set interval; however, Snowflake can’t guarantee task runs at precisely the specified interval.
    >
    >       Values: `{ 10 - 691200 } SECONDS`, `{ 1 - 11520 } MINUTES`, or `{ 1-192 } HOURS` (That is, from 10 seconds to the equivalent of 8 days). Accepts positive integers only.
    >
    >       Also supports the notations: HOUR, MINUTE, SECOND, and H, M, S.

    * `CONFIG = configuration_string`
      :   Specifies a string representation in valid JSON format that all tasks in a
          [task graph](../../user-guide/tasks-graphs) can access.
          For more information about retrieving configuration values,
          see [SYSTEM$GET\_TASK\_GRAPH\_CONFIG](../functions/system_get_task_graph_config).

          Syntax:

          ```
          CONFIG=$${"string1": value1 [, "string2": value2, ...] }$$
          ```

          Copy

          Examples:

          ```
          CONFIG=$${"learning_rate": 0.1}$$
          ```

          Copy

          ```
          CONFIG=$${"environment": "production", "path": "/prod_directory/"}$$
          ```

          Copy

          Note

          + To share information with tasks in a task graph, you must define this parameter in the root task.
          + You can set this parameter on standalone tasks, but doing so doesn’t affect the task behavior.

`ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE`
:   Specifies whether to allow multiple instances of the task graph to run concurrently.

    Note

    This parameter can only be set on a root task. The setting applies to all tasks in the task graph.

    The parameter can be set on standalone tasks but doesn’t affect the task behavior. Snowflake ensures only one instance of a
    standalone task is running at a given time.

    * `TRUE` If the next scheduled run of the root task occurs while the current run of any child task is still in operation, another
      instance of the task graph begins. If a root task is still running when the next scheduled run time occurs, then that scheduled time is
      skipped.
    * `FALSE` The next run of a root task is scheduled only after all child tasks in the task graph have finished running. This means
      that if the cumulative time required to run all tasks in the task graph exceeds the explicit scheduled time set in the definition of
      the root task, at least one run of the Task Graph is skipped.

    Default: `FALSE`

`session_parameter = value [ , session_parameter = value ... ]`
:   Specifies a comma-separated list of session parameters to set for the session when the task runs. A task supports all session
    parameters. For the complete list, see [Session parameters](../parameters.html#label-session-parameters).

    Note

    The following session parameter configurations aren’t supported for tasks:

    * [SEARCH\_PATH](../parameters.html#label-search-path) set to any value.
    * [AUTOCOMMIT = FALSE](../parameters.html#label-autocommit).

`USER_TASK_TIMEOUT_MS = num`
:   Specifies the time limit on a single run of the task before it times out (in milliseconds).

    Note

    * Before you increase the time limit on a task significantly, consider whether the SQL statement initiated by the task could be
      optimized (either by rewriting the statement or using a stored procedure) or the warehouse size should be increased.
    * When both [STATEMENT\_TIMEOUT\_IN\_SECONDS](../parameters.html#label-statement-timeout-in-seconds) and USER\_TASK\_TIMEOUT\_MS are set, the timeout is the lowest non-zero value of the two parameters.
    * When both [STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS](../parameters.html#label-statement-queued-timeout-in-seconds) and USER\_TASK\_TIMEOUT\_MS are set, the value of USER\_TASK\_TIMEOUT\_MS takes precedence.

    For more information about this parameter, see [USER\_TASK\_TIMEOUT\_MS](../parameters.html#label-user-task-timeout-ms).

    Values: `0` - `604800000` (7 days). A value of `0` specifies that the maximum timeout value is enforced.

    Default: `3600000` (1 hour)

`SUSPEND_TASK_AFTER_NUM_FAILURES = num`
:   Specifies the number of consecutive failed task runs after which the current task is suspended automatically. Failed task runs
    include runs in which the SQL code in the task body either produces a user error or times out. Task runs that are skipped,
    canceled, or that fail due to a system error are considered indeterminate and aren’t included in the count of failed task runs.

    Set the parameter on a standalone task or the root task in a task graph. When the parameter is set to a value greater than `0`, the
    following behavior applies to runs of the standalone task or task graph:

    * Standalone tasks are automatically suspended after the specified number of consecutive task runs either fail or time out.
    * The root task is automatically suspended after the run of any single task in a task graph fails or times out the specified
      number of times in consecutive runs.

    When the parameter is set to `0`, failed tasks aren’t automatically suspended.

    The setting applies to tasks that rely on either serverless compute resources or virtual warehouse compute resources.

    For more information about this parameter, see [SUSPEND\_TASK\_AFTER\_NUM\_FAILURES](../parameters.html#label-suspend-task-after-num-failures).

    Values: `0` - No upper limit.

    Default: `10`

`ERROR_INTEGRATION = 'integration_name'`
:   Required only when configuring a task to send error notifications using Amazon Simple Notification Service (SNS), Microsoft Azure Event Grid, or Google Pub/Sub.

    Specifies the name of the notification integration used to communicate with Amazon SNS, MS Azure Event Grid, or Google Pub/Sub. For more information, see
    [Enabling notifications for tasks](../../user-guide/tasks-errors).

`SUCCESS_INTEGRATION = 'integration_name'`
:   Required only when configuring a task to send success notifications using Amazon Simple Notification Service (SNS), Microsoft Azure Event Grid, or Google Pub/Sub.

    Specifies the name of the notification integration used to communicate with Amazon SNS, MS Azure Event Grid, or Google Pub/Sub. For more information, see
    [Enabling notifications for tasks](../../user-guide/tasks-errors).

`LOG_LEVEL = 'log_level'`
:   Specifies the severity level of [events for this task](../../user-guide/tasks-events) that are ingested and made available in
    the active event table. Events at the specified level (and at more severe levels) are ingested.

    For more information about levels, see [LOG\_LEVEL](../parameters.html#label-log-level). For information about setting the log level, see
    [Setting levels for logging, metrics, and tracing](../../developer-guide/logging-tracing/telemetry-levels).

`COMMENT = 'string_literal'`
:   Specifies a comment for the task.

    Default: No value

`AFTER string [ , string , ... ]`
:   Specifies one or more predecessor tasks for the current task. Use this option to create a [task graph](../../user-guide/tasks-graphs.html#label-task-dag) or
    add this task to an existing task graph. A task graph is a series of tasks that starts with a scheduled root task and is linked together
    by dependencies.

    Note that the structure of a task graph can be defined after all of its component tasks are created. Execute
    [ALTER TASK](alter-task) … ADD AFTER statements to specify the predecessors for each task in the planned task graph.

    A task runs after all of its predecessor tasks have finished their own runs successfully (after a brief lag).

    Note

    * The root task should have a defined schedule. Each child task must have one or more defined predecessor tasks, specified
      using the `AFTER` parameter, to link the tasks together.
    * A single task is limited to 100 predecessor tasks and 100 child tasks. In addition, a task graph is limited to a maximum of 1000 tasks
      total (including the root task) in either a resumed or suspended state.
    * Accounts are currently limited to a maximum of 30000 resumed tasks.
    * All tasks in a task graph must have the same task owner. A single role must have the OWNERSHIP privilege on all of the tasks in
      the task graph.
    * All tasks in a task graph must exist in the same schema.
    * The root task must be suspended before any task is recreated (using the CREATE OR REPLACE TASK syntax) or a child task
      is added (using CREATE TASK … AFTER or ALTER TASK … ADD AFTER) or removed (using ALTER TASK … REMOVE AFTER).
    * If any task in a task graph is cloned, the role that clones the task becomes the owner of the clone by default.

      + If the owner of the original task creates the clone, then the task clone retains the link between the task and the predecessor
        task. This means the same predecessor task triggers both the original task and the task clone.
      + If another role creates the clone, then the task clone can have a schedule but not a predecessor.
    * Current limitations:

      + Snowflake guarantees that at most one instance of a task with a defined schedule is running at a given time; however, we cannot
        provide the same guarantee for tasks with a defined predecessor task.

`WHEN boolean_expr`
:   Specifies a Boolean SQL expression; multiple conditions joined with AND/OR are supported. When a task is triggered (based on its
    `SCHEDULE` or `AFTER` setting), it validates the conditions of the expression to determine whether to execute. If the
    conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a
    predecessor also don’t run.

    The following are supported in a task WHEN clause:

    * [SYSTEM$STREAM\_HAS\_DATA](../functions/system_stream_has_data) is supported for evaluation in the SQL expression.

      This function indicates whether a specified stream contains change tracking data. You can use this function to evaluate whether the specified stream contains
      change data before starting the current run. If the result is FALSE, then the task doesn’t run.

      Note

      [SYSTEM$STREAM\_HAS\_DATA](../functions/system_stream_has_data) is designed to avoid returning a FALSE value even when the stream contains
      change data. However, this function isn’t guaranteed to avoid returning a TRUE value when the stream contains no change data.
    * [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](../functions/system_get_predecessor_return_value) is supported for evaluation in the SQL expression.

      This function retrieves the return value for the predecessor task in a task graph. The return value can be used as part of
      a boolean expression. When using SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE, you can cast the returned value to
      the appropriate numeric, string, or boolean type if required.

      Simple examples include:

      ```
      WHEN NOT SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name')::BOOLEAN
      ```

      Copy

      ```
      WHEN SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name') != 'VALIDATION'
      ```

      Copy

      ```
      WHEN SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name')::FLOAT < 0.2
      ```

      Copy

      Note

      Use of [PARSE\_JSON](../functions/parse_json) in TASK … WHEN expressions isn’t supported as it requires warehouse based compute resources.
    * [Boolean operators](../operators-logical) such as AND, OR, NOT, and others.

      Simple example that runs whenever data changes in either of two streams:

      ```
      CREATE TASK my_task
          WAREHOUSE = my_warehouse
          WHEN SYSTEM$STREAM_HAS_DATA('my_customer_stream')
          OR   SYSTEM$STREAM_HAS_DATA('my_order_stream')
          AS
            SELECT CURRENT_TIMESTAMP;
      ```

      Copy
    * Casts between numeric, string, and boolean types.
    * [Comparison operators](../operators-comparison) such as equal, not equal, greater than, less than, and others.

    Validating the conditions of the WHEN expression does not require compute resources. The validation is instead processed in the cloud
    services layer. A nominal charge accrues each time a task evaluates its WHEN condition and doesn’t run. The charges accumulate each time
    the task is triggered until it runs. At that time, the charge is converted to Snowflake credits and added to the compute resource usage
    for the task run.

    Generally the compute time to validate the condition is insignificant compared to task execution time. As a best practice, align
    scheduled and actual task runs as closely as possible. Avoid task schedules that don’t align with task runs. For
    example, if data is inserted into a table with a stream roughly every 24 hours, don’t schedule a task that checks for stream data
    every minute. The charge to validate the WHEN expression with each run is generally insignificant, but the charges are cumulative.

    Note that daily consumption of cloud services that falls below the
    [10% quota of the daily usage of the compute resources](../../user-guide/cost-understanding-compute.html#label-cloud-services-credit-usage) accumulates no cloud services charges.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](../../user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](../../user-guide/object-tagging/introduction.html#label-object-tagging-quota).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](../../user-guide/contacts-using).

`FINALIZE = string`
:   Specifies the name of a root task that the finalizer task is associated with. Finalizer tasks run after all other tasks in the task graph run to completion. You can define the SQL of a finalizer task to handle notifications and the release and cleanup of resources that a task graph uses. For more information, see [Finalizer task](../../user-guide/tasks-graphs.html#label-finalizer-task).

    * A root task can only have one finalizer task. If you create multiple finalizer tasks for a root task, the task creation will fail.
    * A finalizer task cannot have any child tasks. Any command attempting to make the finalizer task a predecessor will fail.
    * A finalizer task cannot have a schedule. Creating a finalizer task with a schedule will fail.

    Default: No value

`TASK_AUTO_RETRY_ATTEMPTS = num`
:   Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically
    retry the task graphs from the last task in the graph that failed.

    The automatic task graph retry is disabled by default. To enable this feature, set TASK\_AUTO\_RETRY\_ATTEMPTS to a value greater than `0`
    on the root task of a task graph.

    Note that this parameter must be set to the root task of a task graph. If it’s set to a child task, an error will be returned.

    Values: `0` - `30`.

    Default: `0`

`USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = num`
:   Defines how frequently a task can execute in seconds. If data changes occur more often than the specified minimum, changes will be
    grouped and processed together.

    The task will run every 12 hours even if this value is set to more than 12 hours.

    Values: Minimum `10`, maximum `604800`.

    Default: `30`

`TARGET_COMPLETION_INTERVAL = 'num { HOURS | MINUTES | SECONDS }'`
:   Specifies the desired task completion time. This parameter only applies to serverless tasks. This property is only set on a Task.

    This parameter is required when you create serverless [Triggered tasks](../../user-guide/tasks-triggered).

    Values: `{ 10 - 86400 } SECONDS`, `{ 1 - 1440 } MINUTES`, or `{ 1-24 } HOURS` (That is, from 10 seconds to the equivalent of 1 day). Accepts positive integers only.

    Also supports the notations: HOUR, MINUTE, SECOND, and H, M, S.

    Default: Snowflake resizes serverless compute resources to complete before the next scheduled execution time.

`SERVERLESS_TASK_MIN_STATEMENT_SIZE = string`
:   Specifies the minimum allowed warehouse size for the serverless task. This parameter only applies to serverless tasks. This parameter can be specified on the Task, Schema, Database, or Account. Precedence follows the standard parameter hierarchy.

    Values: Minimum `XSMALL`, Maximum `XXLARGE`. Values are consistent with [WAREHOUSE\_SIZE values](create-warehouse).

    Also supports the notation: X2LARGE.

    Default: `XSMALL`

    Note that if both SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE and USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE are specified, SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE must be equal to or smaller than USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE.

`SERVERLESS_TASK_MAX_STATEMENT_SIZE = string`
:   Specifies the maximum allowed warehouse size for the serverless task. This parameter only applies to serverless tasks. This parameter can be specified on the Task, Schema, Database, or Account. Precedence follows the standard parameter hierarchy.

    Values: Minimum `XSMALL`, Maximum `XXLARGE`.

    Also supports the notation: X2LARGE.

    Default: `XXLARGE`

    If both SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE and SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE are specified, SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE must be less than or equal to SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE. SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE must be equal to or greater than USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE

`EXECUTE AS USER <user_name>`
:   Runs the task on behalf of a specified user account. The user who runs the command must have permissions granted by using the [GRANT IMPERSONATE ON USER TO ROLE](grant-privilege-user) command.

    For more information, see [Run tasks with user privileges](../../user-guide/tasks-intro.html#label-user-based-security-for-tasks).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| EXECUTE TASK | Account | Required to run any tasks the role owns. Revoking the EXECUTE TASK privilege on a role prevents all subsequent task runs from starting under that role. |
| EXECUTE MANAGED TASK | Account | Required only for tasks that rely on serverless compute resources for runs. |
| CREATE TASK | Schema |  |
| USAGE | Warehouse | Required only for tasks that rely on user-managed warehouses for runs. |
| OWNERSHIP | Task | Required only when executing a [CREATE OR ALTER TASK](#label-create-or-alter-task-syntax) statement for an *existing* task.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## Usage notes[¶](#usage-notes "Link to this heading")

* Tasks run using the task owner’s privileges. For the list of minimum required privileges to run tasks, see
  [Task security](../../user-guide/tasks-intro.html#label-task-security-reqs).

  Run the SQL statement or call the stored procedure, as the task owner role, before you include it in a task definition to ensure
  the role has the required privileges on objects referenced by the SQL or stored procedure.
* For serverless tasks:

  + Serverless compute resources for a task can range from the equivalent of `XSMALL` to `XXLARGE` in warehouse sizes. To request a
    size increase, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
  + Individual tasks in a task graph can use serverless or user-managed compute resources. Using the serverless compute for
    all tasks in the task graph isn’t required.
* If a task fails with an unexpected error, you can receive a notification about the error.
  For more information on configuring task error notifications, see [Enabling notifications for tasks](../../user-guide/tasks-errors).
* By default, a DML statement executed without explicitly starting a transaction is automatically committed on success or rolled back on
  failure at the end of the statement. This behavior is called *autocommit* and is controlled with the [AUTOCOMMIT](../parameters.html#label-autocommit) parameter.
  This parameter must be set to TRUE. If the AUTOCOMMIT parameter is set to FALSE at the account level, then set the parameter to
  TRUE for the individual task (using ALTER TASK … SET AUTOCOMMIT = TRUE); otherwise, any DML statement executed by the task fails.
* Only one task should consume data from a stream. Create multiple streams for the same table to be consumed by more than one task. When a
  task consumes the data in a stream using a DML statement, the stream advances the offset and change data is no longer available for the
  next task to consume.
* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).

## CREATE OR ALTER TASK usage notes[¶](#create-or-alter-task-usage-notes "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

* All limitations of the [ALTER TASK](alter-task) command apply.
* A task cannot be resumed or suspended using the CREATE OR ALTER TASK command. To resume or suspend a task, use the ALTER TASK command.
* Setting or unsetting a tag is not supported; however existing tags are *not* altered by a CREATE OR ALTER statement and remain unchanged.

## Examples[¶](#examples "Link to this heading")

### Single SQL statement[¶](#single-sql-statement "Link to this heading")

Create a serverless task that queries the current timestamp every hour starting at 9:00 a.m. and ending at 5:00 p.m. on Sundays
(America/Los\_Angeles time zone).

The initial warehouse size is XSMALL:

```
CREATE TASK t1
  SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles'
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  AS
    SELECT CURRENT_TIMESTAMP;
```

Copy

Same as the previous example, but the task relies on a user-managed warehouse to provide the compute resources for runs:

```
CREATE TASK mytask_hour
  WAREHOUSE = mywh
  SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles'
  AS
    SELECT CURRENT_TIMESTAMP;
```

Copy

Create a serverless task that inserts the current timestamp into a table every hour. The task sets the [TIMESTAMP\_INPUT\_FORMAT](../parameters.html#label-timestamp-input-format)
parameter for the session in which the task runs. This session parameter specifies the format of the inserted timestamp:

```
CREATE TASK t1
  SCHEDULE = '60 MINUTES'
  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  AS
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
```

Copy

Create a task that inserts the current timestamp into a table every 5 minutes:

```
CREATE TASK mytask_minute
  WAREHOUSE = mywh
  SCHEDULE = '5 MINUTES'
  AS
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
```

Copy

Create a task that inserts change tracking data for INSERT operations from a stream into a table every 5 minutes. The task polls the
stream using the SYSTEM$STREAM\_HAS\_DATA function to determine whether change data exists and, if the result is `FALSE`, skips the
current run:

```
CREATE TASK mytask1
  WAREHOUSE = mywh
  SCHEDULE = '5 MINUTES'
  WHEN
    SYSTEM$STREAM_HAS_DATA('MYSTREAM')
  AS
    INSERT INTO mytable1(id,name) SELECT id, name FROM mystream WHERE METADATA$ACTION = 'INSERT';
```

Copy

Create a serverless child task in a task graph and add multiple predecessor tasks. The child task runs only after all specified predecessor
tasks have successfully completed their own runs.

Suppose that the root task for a task graph is `task1` and that `task2`, `task3`, and `task4`
are child tasks of `task1`. This example adds child task `task5` to the task graph and specifies
`task2`, `task3`, and `task4` as predecessor tasks:

```
-- Create task5 and specify task2, task3, task4 as predecessors tasks.
-- The new task is a serverless task that inserts the current timestamp into a table column.
CREATE TASK task5
  AFTER task2, task3, task4
AS
  INSERT INTO t1(ts) VALUES(CURRENT_TIMESTAMP);
```

Copy

### Stored procedure[¶](#stored-procedure "Link to this heading")

Create a task named `my_copy_task` that calls a stored procedure to unload data from the `mytable` table to the named `mystage`
stage (using [COPY INTO <location>](copy-into-location)) every hour:

```
-- Create a stored procedure that unloads data from a table
-- The COPY statement in the stored procedure unloads data to files in a path identified by epoch time (using the Date.now() method)
CREATE OR REPLACE PROCEDURE my_unload_sp()
  returns string not null
  language javascript
  AS
    $$
      var my_sql_command = ""
      var my_sql_command = my_sql_command.concat("copy into @mystage","/",Date.now(),"/"," from mytable overwrite=true;");
      var statement1 = snowflake.createStatement( {sqlText: my_sql_command} );
      var result_set1 = statement1.execute();
    return my_sql_command; // Statement returned for info/debug purposes
    $$;

-- Create a task that calls the stored procedure every hour
CREATE TASK my_copy_task
  WAREHOUSE = mywh
  SCHEDULE = '60 MINUTES'
  AS
    CALL my_unload_sp();
```

Copy

### Multiple SQL statements using SnowSQL[¶](#multiple-sql-statements-using-snowsql "Link to this heading")

Create a task that executes multiple SQL statements. In this example, the task modifies the TIMESTAMP\_OUTPUT\_FORMAT for the session and
then queries the CURRENT\_TIMESTAMP function.

Note

The SQL code in the task definition includes multiple statements. To execute the CREATE TASK statement, you must temporarily set a
character other than a semicolon as the delimiter for SQL statements; otherwise, the CREATE TASK statement would return a user
error. The command to change the SQL delimiter in SnowSQL is `!set sql_delimiter = '<character>'`.

```
!set sql_delimiter=/
CREATE OR REPLACE TASK test_logging
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  SCHEDULE = 'USING CRON  0 * * * * America/Los_Angeles'
  AS
    BEGIN
      ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
      SELECT CURRENT_TIMESTAMP;
    END;/
!set sql_delimiter=';'
```

Copy

### Procedural logic using Snowflake Scripting[¶](#procedural-logic-using-snowflake-scripting "Link to this heading")

Create a task that declares a variable, uses the variable, and returns the value of the variable every 15 seconds:

```
CREATE TASK t1
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  SCHEDULE = '15 SECONDS'
  AS
    EXECUTE IMMEDIATE
    $$
    DECLARE
      radius_of_circle float;
      area_of_circle float;
    BEGIN
      radius_of_circle := 3;
      area_of_circle := pi() * radius_of_circle * radius_of_circle;
      return area_of_circle;
    END;
    $$;
```

Copy

### Root task with configuration[¶](#root-task-with-configuration "Link to this heading")

Create a task that specifies configuration, and then reads that configuration.

```
CREATE OR REPLACE TASK root_task_with_config
  WAREHOUSE=mywarehouse
  SCHEDULE='10 m'
  CONFIG=$${"output_dir": "/temp/test_directory/", "learning_rate": 0.1}$$
  AS
    BEGIN
      LET OUTPUT_DIR STRING := SYSTEM$GET_TASK_GRAPH_CONFIG('output_dir')::string;
      LET LEARNING_RATE DECIMAL := SYSTEM$GET_TASK_GRAPH_CONFIG('learning_rate')::DECIMAL;
    ...
    END;
```

Copy

### Finalizer task[¶](#finalizer-task "Link to this heading")

Create a finalizer task, associated with the root task of a task graph, that sends an email alert after task completion. For more
information about finalizer tasks, see [Finalizer task](../../user-guide/tasks-graphs.html#label-finalizer-task).

```
CREATE TASK finalize_task
  WAREHOUSE = my_warehouse
  FINALIZE = my_root_task
  AS
    CALL SYSTEM$SEND_EMAIL(
      'my_email_int',
      'first.last@example.com, first2.last2@example.com',
      'Email Alert: Task A has finished.',
      'Task A has successfully finished.\nStart Time: 10:10:32\nEnd Time: 12:15:45\nTotal Records Processed: 115678'
    );
```

Copy

### Triggered task[¶](#triggered-task "Link to this heading")

Create a triggered task, associated with a stream, that inserts data from the specified stream into the table every time there is new data in the stream. For more information, see [Triggered tasks](../../user-guide/tasks-triggered).

```
CREATE TASK triggeredTask
  WAREHOUSE = my_warehouse
  WHEN system$stream_has_data('my_stream')
  AS
    INSERT INTO my_downstream_table
    SELECT * FROM my_stream;

ALTER TASK triggeredTask RESUME;
```

Copy

### Create and alter a simple task using the CREATE OR ALTER TASK command[¶](#create-and-alter-a-simple-task-using-the-create-or-alter-task-command "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Create a task `my_task` to execute every hour in warehouse `my_warehouse`:

```
CREATE OR ALTER TASK my_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '60 MINUTES'
  AS
    SELECT PI();
```

Copy

Alter task `my_task` to execute after task `my_other_task` and update the task definition:

```
CREATE OR ALTER TASK my_task
  WAREHOUSE = regress
  AFTER my_other_task
  AS
    SELECT 2 * PI();
```

Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Variant syntax](#variant-syntax)
3. [CREATE OR ALTER TASK](#create-or-alter-task)
4. [CREATE TASK … CLONE](#create-task-clone)
5. [Required parameters](#required-parameters)
6. [Clone tasks in a task graph](#clone-tasks-in-a-task-graph)
7. [Optional parameters](#optional-parameters)
8. [Access control requirements](#access-control-requirements)
9. [Usage notes](#usage-notes)
10. [CREATE OR ALTER TASK usage notes](#create-or-alter-task-usage-notes)
11. [Examples](#examples)
12. [Single SQL statement](#single-sql-statement)
13. [Stored procedure](#stored-procedure)
14. [Multiple SQL statements using SnowSQL](#multiple-sql-statements-using-snowsql)
15. [Procedural logic using Snowflake Scripting](#procedural-logic-using-snowflake-scripting)
16. [Root task with configuration](#root-task-with-configuration)
17. [Finalizer task](#finalizer-task)
18. [Triggered task](#triggered-task)
19. [Create and alter a simple task using the CREATE OR ALTER TASK command](#create-and-alter-a-simple-task-using-the-create-or-alter-task-command)