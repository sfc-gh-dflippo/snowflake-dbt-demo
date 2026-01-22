---
auto_generated: true
description: You can log messages from a stored procedure handler written in Snowflake
  Scripting by using the Snowflake SYSTEM$LOG, SYSTEM$LOG_<level> (for Snowflake Scripting)
  function. When you’ve set up an even
last_scraped: '2026-01-14T16:55:15.317020+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-snowflake-scripting
title: Logging messages in Snowflake Scripting | Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../snowpark-container-services/overview.md)
12. [Functions and procedures](../extensibility.md)
13. [Logging, Tracing, and Metrics](logging-tracing-overview.md)

    * [Get started tutorial](tutorials/logging-tracing-getting-started.md)
    * [Enabling monitoring](logging-tracing-enabling.md)
    * [Telemetry levels](telemetry-levels.md)
    * [Limitations](logging-tracing-limitations.md)
    * [Troubleshooting](logging-tracing-troubleshooting.md)
    * [Costs](logging-tracing-billing.md)
    * Event tables
    * [Event table overview](event-table-setting-up.md)
    * [Event table operations](event-table-operations.md)
    * [Event table columns](event-table-columns.md)
    * [Unhandled exception messages](unhandled-exception-messages.md)
    * [Telemetry package dependencies](telemetry-package-dependencies.md)
    * [Java and Scala packaging](telemetry-build-maven.md)
    * Logging
    * [Introduction](logging.md)
    * [Java](logging-java.md)
    * [JavaScript](logging-javascript.md)
    * [Python](logging-python.md)
    * [Scala](logging-scala.md)
    * [Snowflake Scripting](logging-snowflake-scripting.md)
    * [Viewing log messages](logging-accessing-messages.md)
    * Metrics
    * [Introduction](metrics.md)
    * [Limitations](metrics-limitations.md)
    * [Handlers](metrics-handler.md)
    * [Viewing metrics data](metrics-viewing-data.md)
    * Tracing
    * [Introduction](tracing.md)
    * [Trace events](tracing-how-events-work.md)
    * [Custom spans](tracing-custom-spans.md)
    * [Java](tracing-java.md)
    * [JavaScript](tracing-javascript.md)
    * [Python](tracing-python.md)
    * [Scala](tracing-scala.md)
    * [Snowflake Scripting](tracing-snowflake-scripting.md)
    * [Viewing trace data](tracing-accessing-events.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../streamlit/object-management/billing.md)
      - [Security considerations](../streamlit/object-management/security.md)
      - [Privilege requirements](../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../streamlit/app-development/dependency-management.md)
      - [File organization](../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../streamlit/features/git-integration.md)
      - [External access](../streamlit/features/external-access.md)
      - [Row access policies](../streamlit/features/row-access.md)
      - [Sleep timer](../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../streamlit/troubleshooting.md)
    - [Release notes](../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)[Logging, Tracing, and Metrics](logging-tracing-overview.md)Snowflake Scripting

# Logging messages in Snowflake Scripting[¶](#logging-messages-in-snowflake-scripting "Link to this heading")

You can log messages from a stored procedure handler written in Snowflake Scripting by using the Snowflake
[SYSTEM$LOG, SYSTEM$LOG\_<level> (for Snowflake Scripting)](../../sql-reference/functions/system_log) function. When you’ve set up an event table to store log entries, Snowflake stores log entries
generated by your handler code in the table.

Before logging from code, be sure you have the logging level set so that the messages you want are stored in the event table. For more
information, see [Setting levels for logging, metrics, and tracing](telemetry-levels).

Note

Before you can begin logging messages, you must set up an event table. For more information, see
[Event table overview](event-table-setting-up).

You can access log messages by executing a SELECT command on the event table. For more information, see
[Viewing log messages](logging-accessing-messages).

For general information about setting up logging and retrieving messages in Snowflake, see
[Logging messages from functions and procedures](logging).

## Snowflake Scripting example[¶](#snowflake-scripting-example "Link to this heading")

Code in the following example uses the SYSTEM$LOG function to log messages at each of the supported levels. Note that a message logged
from code that processes an input row will be logged *for every row* processed by the handler. If the handler is executed in a large table,
this can result in a large number of messages in the event table.

```
-- The following calls are equivalent.
-- Both log information-level messages.
SYSTEM$LOG('info', 'Information-level message');
SYSTEM$LOG_INFO('Information-level message');

-- The following calls are equivalent.
-- Both log error messages.
SYSTEM$LOG('error', 'Error message');
SYSTEM$LOG_ERROR('Error message');


-- The following calls are equivalent.
-- Both log warning messages.
SYSTEM$LOG('warning', 'Warning message');
SYSTEM$LOG_WARN('Warning message');

-- The following calls are equivalent.
-- Both log debug messages.
SYSTEM$LOG('debug', 'Debug message');
SYSTEM$LOG_DEBUG('Debug message');

-- The following calls are equivalent.
-- Both log trace messages.
SYSTEM$LOG('trace', 'Trace message');
SYSTEM$LOG_TRACE('Trace message');

-- The following calls are equivalent.
-- Both log fatal messages.
SYSTEM$LOG('fatal', 'Fatal message');
SYSTEM$LOG_FATAL('Fatal message');
```

Copy

## Automatically add log messages about blocks and child jobs[¶](#automatically-add-log-messages-about-blocks-and-child-jobs "Link to this heading")

You can automatically log the following additional information about the execution of a Snowflake Scripting
stored procedure:

* BEGIN/END of a Snowflake Scripting block.
* BEGIN/END of a child job request.

Automatic logging is intended for the following use cases:

* You want to generate the additional log messages without modifying the body of the stored procedure.
* You want comprehensive information about the execution of the stored procedure.
* You want more visibility into stored procedure execution to make it easier to develop and debug it without
  manually adding logging code in the procedure.

To automatically log these Snowflake Scripting messages for a stored procedure, set the [AUTO\_EVENT\_LOGGING](../../sql-reference/parameters.html#label-auto-event-logging) parameter
for the stored procedure to `LOGGING` or `ALL` using the [ALTER PROCEDURE](../../sql-reference/sql/alter-procedure) command. When
you set this parameter to `ALL`, additional [trace events](tracing-snowflake-scripting) are also emitted automatically
for the stored procedure.

Important

The additional information is added to the event table only if the effective [LOG\_LEVEL](../../sql-reference/parameters.html#label-log-level) is set
to `TRACE`. For more information, see [Setting levels for logging, metrics, and tracing](telemetry-levels).

For example, create a simple table and insert data:

```
CREATE OR REPLACE TABLE test_auto_event_logging (id INTEGER, num NUMBER(12, 2));

INSERT INTO test_auto_event_logging (id, num) VALUES
  (1, 11.11),
  (2, 22.22);
```

Copy

Next, create a stored procedure named `auto_event_logging_sp`. This sample stored procedure updates a table row and
then queries the table:

```
CREATE OR REPLACE PROCEDURE auto_event_logging_sp(
  table_name VARCHAR,
  id_val INTEGER,
  num_val NUMBER(12, 2))
RETURNS TABLE()
LANGUAGE SQL
AS
$$
BEGIN
  UPDATE IDENTIFIER(:table_name)
    SET num = :num_val
    WHERE id = :id_val;
  LET res RESULTSET := (SELECT * FROM IDENTIFIER(:table_name) ORDER BY id);
  RETURN TABLE(res);
EXCEPTION
  WHEN statement_error THEN
    res := (SELECT :sqlcode sql_code, :sqlerrm error_message, :sqlstate sql_state);
    RETURN TABLE(res);
END;
$$
;
```

Copy

The following examples set the AUTO\_EVENT\_LOGGING parameter for the stored procedure:

```
ALTER PROCEDURE auto_event_logging_sp(VARCHAR, INTEGER, NUMBER)
  SET AUTO_EVENT_LOGGING = 'LOGGING';
```

Copy

```
ALTER PROCEDURE auto_event_logging_sp(VARCHAR, INTEGER, NUMBER)
  SET AUTO_EVENT_LOGGING = 'ALL';
```

Copy

Call the stored procedure:

```
CALL auto_event_logging_sp('test_auto_event_logging', 2, 33.33);
```

Copy

```
+----+-------+
| ID |   NUM |
|----+-------|
|  1 | 11.11 |
|  2 | 33.33 |
+----+-------+
```

Query the event table for messages logged by the stored procedure named `auto_event_logging_sp`. For each message,
print out the timestamp, log level, and text of the message.

```
SELECT
    TIMESTAMP as time,
    RECORD['severity_text'] as severity,
    VALUE as message
  FROM
    my_db.public.my_events
  WHERE
    RESOURCE_ATTRIBUTES['snow.executable.name'] LIKE '%AUTO_EVENT_LOGGING_SP%'
    AND RECORD_TYPE = 'LOG';
```

Copy

```
+-------------------------+----------+----------------------------------+
| TIME                    | SEVERITY | MESSAGE                          |
|-------------------------+----------+----------------------------------|
| 2024-10-25 20:42:24.134 | "TRACE"  | "Entering outer block at line 2" |
| 2024-10-25 20:42:24.135 | "TRACE"  | "Entering block at line 2"       |
| 2024-10-25 20:42:24.135 | "TRACE"  | "Starting child job"             |
| 2024-10-25 20:42:24.633 | "TRACE"  | "Ending child job"               |
| 2024-10-25 20:42:24.633 | "TRACE"  | "Starting child job"             |
| 2024-10-25 20:42:24.721 | "TRACE"  | "Ending child job"               |
| 2024-10-25 20:42:24.721 | "TRACE"  | "Exiting with return at line 7"  |
+-------------------------+----------+----------------------------------+
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

1. [Snowflake Scripting example](#snowflake-scripting-example)
2. [Automatically add log messages about blocks and child jobs](#automatically-add-log-messages-about-blocks-and-child-jobs)

Related content

1. [Viewing log messages](/developer-guide/logging-tracing/logging-accessing-messages)
2. [Logging messages from functions and procedures](/developer-guide/logging-tracing/logging)
3. [Event table overview](/developer-guide/logging-tracing/event-table-setting-up)