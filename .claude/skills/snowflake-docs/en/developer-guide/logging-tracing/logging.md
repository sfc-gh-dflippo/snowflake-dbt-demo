---
auto_generated: true
description: You can log messages (such as warning or error messages) from a stored
  procedure, UDF, or UDTF, including those you write using Snowpark APIs. You can
  access the logged messages from an event table (a
last_scraped: '2026-01-14T16:58:06.806836+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/logging-tracing/logging
title: Logging messages from functions and procedures | Snowflake Documentation
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

[Developer](../../developer.md)[Logging, Tracing, and Metrics](logging-tracing-overview.md)Introduction

# Logging messages from functions and procedures[¶](#logging-messages-from-functions-and-procedures "Link to this heading")

You can log messages (such as warning or error messages) from a stored procedure, UDF, or UDTF, including those you write
[using Snowpark APIs](../snowpark/index). You can access the logged messages from an event table (a type of
predefined table that captures events, including logged messages). For a list of supported handler languages, see
[Supported languages](#label-logging-supported-languages).

For example, in a Java UDF, you can use the [SLF4J API](http://www.slf4j.org/) to log messages. Later, you can access those logged messages in an event
table.

Note

Before you can collect log messages, you must [enable telemetry data collection](logging-tracing-enabling).
When you [instrument your code](#label-logging-handler-code), Snowflake generates the data and collects it in an event table.

## Logging example[¶](#logging-example "Link to this heading")

The Python code in the following example imports the `logging` module, gets a logger, and logs a message at the `INFO` level.

Note

A message logged from a method that processes an input row will be logged *for every row* processed by the UDF. If the UDF is executed in a
large table, this can result in a large number of messages in the event table.

```
import logging

logger = logging.getLogger("mylog")

def test_logging(self):
    logger.info("This is an INFO test.")
```

Copy

## Getting started[¶](#getting-started "Link to this heading")

To get started logging from handler code, follow these high-level steps:

1. [Set up an event table.](event-table-setting-up)

   Snowflake will use your event table to store messages logged from your handler code. An event table has
   columns [predefined by Snowflake](event-table-columns).
2. Get acquainted with the logging API for the handler language you’ll be using.

   see [Supported languages](#label-logging-supported-languages) for a list of handler languages, then view
   [content about how to log from your language](#label-logging-handler-code).
3. Add logging code to your handler.
4. Learn how to [retrieve logging data](logging-accessing-messages) from the event table.

## Level for log messages[¶](#level-for-log-messages "Link to this heading")

You can manage the level of log event data stored in the event table by setting the log level. Before logging, use this setting to make
sure you’re capturing the log message severity.

For more information, see [Setting levels for logging, metrics, and tracing](telemetry-levels).

## Supported languages[¶](#supported-languages "Link to this heading")

You can log messages from code written in the following languages, including when handler code is written with
[Snowpark APIs](../snowpark/index).

| Language / Type | Java | JavaScript | Python | Scala | SQL |
| --- | --- | --- | --- | --- | --- |
| Stored procedure handler | ✔ | ✔ | ✔ | ✔ | ✔ \*\* |
| Streamlit app |  |  | ✔ |  |  |
| UDF handler (scalar function) | ✔ | ✔ | ✔ | ✔ |  |
| UDTF handler (table function) | ✔ | ✔ | ✔ | ✔ \* |  |

**Legend**

\*:
:   Scala UDTF handler written in Snowpark.

\*\*:
:   Snowflake Scripting used to write stored procedures.

Note

Logging is not supported for [Request and response translators in external functions](../../sql-reference/external-functions-translators).

### Logging from handler code[¶](#logging-from-handler-code "Link to this heading")

To log messages, you can use functions common to your handler code language. Snowflake intercepts messages and stores them in the
event table you create.

For example, in a Java UDF, you can use the [SLF4J API](http://www.slf4j.org/) to log messages. Later, you can access those logged messages in an event table.

If you plan to log messages when errors occur, you should log them from within the construct for handling errors in the language
that you are using. For example, in a Java UDF, call the method for logging a message in the `catch` block where you handle
the exception.

The following table lists handler languages supported for logging, along with links to content on logging from code.

| Language | Logging Library | Documentation |
| --- | --- | --- |
| Java | SLF4J API | [Logging messages in Java](logging-java) |
| JavaScript | Snowflake JavaScript API `snowflake` object | [Logging messages in JavaScript](logging-javascript) |
| Python | Standard Library `logging` module | [Logging messages in Python](logging-python) |
| Scala | SLF4J API | [Logging messages in Scala](logging-scala) |
| Snowflake Scripting | Snowflake SYSTEM$LOG function. | [Logging messages in Snowflake Scripting](logging-snowflake-scripting) |

## Viewing log messages[¶](#viewing-log-messages "Link to this heading")

You can view the log messages either through Snowsight or by querying the event table in which log entries are stored. For more
information, see [Viewing log messages](logging-accessing-messages).

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

1. [Logging example](#logging-example)
2. [Getting started](#getting-started)
3. [Level for log messages](#level-for-log-messages)
4. [Supported languages](#supported-languages)
5. [Viewing log messages](#viewing-log-messages)

Related content

1. [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview)
2. [Event table overview](/developer-guide/logging-tracing/event-table-setting-up)
3. [CREATE EVENT TABLE](/developer-guide/logging-tracing/../../sql-reference/sql/create-event-table)
4. [DESCRIBE EVENT TABLE](/developer-guide/logging-tracing/../../sql-reference/sql/desc-event-table)
5. [SHOW EVENT TABLES](/developer-guide/logging-tracing/../../sql-reference/sql/show-event-tables)