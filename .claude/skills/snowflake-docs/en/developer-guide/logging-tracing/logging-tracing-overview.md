---
auto_generated: true
description: You can record the activity of your Snowflake function and procedure
  handler code (including code you write using Snowpark APIs) by capturing log messages
  and trace events from the code as it executes
last_scraped: '2026-01-14T16:55:41.273368+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-tracing-overview
title: Logging, tracing, and metrics | Snowflake Documentation
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

[Developer](../../developer.md)Logging, Tracing, and Metrics

# Logging, tracing, and metrics[¶](#logging-tracing-and-metrics "Link to this heading")

You can record the activity of your Snowflake function and procedure handler code (including code you write
[using Snowpark APIs](../snowpark/index)) by capturing log messages and trace events from the code as it executes.
Once you’ve collected the data, you can query it with SQL to analyze the results.

Logging, tracing, and metrics are among the observability features Snowflake provides to make it easier for you to debug and optimize
applications. Snowflake captures observability data in a structure based on the [OpenTelemetry](https://opentelemetry.io/) standard.

In particular, you can record and analyze the following:

* [Log messages](logging) — Independent, detailed messages with information about the state of a
  specific piece of your code.
* [Metrics data](metrics) — CPU and memory metrics that Snowflake generates.
* [Trace events](tracing) — Structured data you can use to get information spanning and grouping
  multiple parts of your code.

## Get started[¶](#get-started "Link to this heading")

Use the following high-level steps to begin capturing and using log and trace data.

1. Ensure that you have an active event table. You can do one of the following:

   * [Use the default event table](event-table-setting-up.html#label-logging-event-table-default) that is active by default.
   * [Create and set as active an event table](event-table-setting-up.html#label-logging-event-table-custom-create).

   Snowflake collects telemetry data from your code in the event table.
2. [Set telemetry levels](#label-logging-event-table-level) so that data is collected.

   With levels, you can specify which data – and how much data – is collected. Make sure the levels are set correctly.
3. Begin emitting log or trace data from handler code.

   Once you’ve created an event table and associated it with your account, you can use an API in your handler’s language to emit log
   messages. After you’ve captured log and trace data, you can query the data to analyze the results.

   For more information on instrumenting your code, see the following:

   * [Logging messages from functions and procedures](logging)
   * [Trace events for functions and procedures](tracing)
4. Query the event table to analyze collected log and trace data.

   For more information, see the following:

   * [Viewing log messages](logging-accessing-messages)
   * [Viewing metrics data](metrics-viewing-data)
   * [Viewing trace data](tracing-accessing-events)

## Set telemetry levels[¶](#set-telemetry-levels "Link to this heading")

You can manage the level of telemetry data stored in the event table — such as log, trace, and metrics data — by setting the level
for each type of data. Use level settings to ensure that you’re capturing the amount and kind of data you want.

For more information, see [Setting levels for logging, metrics, and tracing](telemetry-levels).

## Compare log messages and trace events[¶](#compare-log-messages-and-trace-events "Link to this heading")

The following table compares the characteristics and benefits of log messages and trace events.

| Characteristic | Log entries | Trace events |
| --- | --- | --- |
| Intended use | Record detailed but unstructured information about the state of your code. Use this information to understand what happened during a particular invocation of your function or procedure. | Record a brief but structured summary of each invocation of your code. Aggregate this information to understand behavior of your code at a high level. |
| Structure as a payload | None. A log entry is just a string. | Structured with attributes you can attach to trace events. Attributes are key-value pairs that can be easily queried with a SQL query. |
| Supports grouping | No. Each log entry is an independent event. | Yes. Trace events are organized into spans. A span can have its own attributes. |
| Quantity limits | Unlimited. All log entries emitted by your code are ingested into the event table. | The number of trace events per span is capped at 128. There is also a limit on the number of span attributes. |
| Complexity of queries against recorded data | Relatively high. Your queries must parse each log entry to extract meaningful information from it. | Relatively low. Your queries can take advantage of the structured nature of trace events. |

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

1. [Get started](#get-started)
2. [Set telemetry levels](#set-telemetry-levels)
3. [Compare log messages and trace events](#compare-log-messages-and-trace-events)

Related content

1. [Enabling telemetry collection](/developer-guide/logging-tracing/logging-tracing-enabling)
2. [Logging messages from functions and procedures](/developer-guide/logging-tracing/logging)
3. [Trace events for functions and procedures](/developer-guide/logging-tracing/tracing)
4. [Collecting metrics data](/developer-guide/logging-tracing/metrics)