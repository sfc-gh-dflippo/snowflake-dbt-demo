---
auto_generated: true
description: The Snowpark library provides an intuitive API for querying and processing
  data in a data pipeline. Using the Snowpark library, you can build applications
  that process data in Snowflake without moving
last_scraped: '2026-01-14T16:58:06.097356+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/scala/index
title: Snowpark Developer Guide for Scala | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../index.md)

   * [Java](../java/index.md)
   * [Python](../python/index.md)
   * [Scala](index.md)

     + [Setting Up a Development Environment](setup.md)
     + [Creating a Session](creating-session.md)
     + [Using DataFrames](working-with-dataframes.md)
     + [Creating User-Defined Functions](creating-udfs.md)
     + [Creating Stored Procedures](creating-sprocs.md)
     + [Calling Functions and Stored Procedures](calling-functions.md)
     + [Example](example.md)
     + [Troubleshooting](troubleshooting.md)
     + [Map of Scala APIs to SQL Commands](sql-to-snowpark.md)
     + [Scala API Reference - Scala 2.12](/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/index.html)
     + [Scala API Reference - Scala 2.13 (Public Preview)](/developer-guide/snowpark/reference/scala/2.13/com/snowflake/snowpark/index.html)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)
13. [Logging, Tracing, and Metrics](../../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../../streamlit/object-management/billing.md)
      - [Security considerations](../../streamlit/object-management/security.md)
      - [Privilege requirements](../../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../../streamlit/app-development/dependency-management.md)
      - [File organization](../../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../../streamlit/features/git-integration.md)
      - [External access](../../streamlit/features/external-access.md)
      - [Row access policies](../../streamlit/features/row-access.md)
      - [Sleep timer](../../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../../streamlit/troubleshooting.md)
    - [Release notes](../../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../../snowflake-cli/index.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Snowpark API](../index.md)Scala

# Snowpark Developer Guide for Scala[¶](#snowpark-developer-guide-for-scala "Link to this heading")

The Snowpark library provides an intuitive API for querying and processing data in a data pipeline. Using the Snowpark library, you can
build applications that process data in Snowflake without moving data to the system where your application code runs.

For an introduction to Snowpark, see [Snowpark API](../index).

## Get Started[¶](#get-started "Link to this heading")

[Setting Up Your Development Environment for Snowpark Scala](setup)
:   Set up to build Snowpark apps using any of several development environments.

[Snowpark Library for Scala and Java release notes](../../../release-notes/clients-drivers/snowpark-scala-java)
:   Get the latest release notes.

### Quickstarts[¶](#quickstarts "Link to this heading")

[Getting Started With Snowpark in Scala](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_scala/index.html) (Snowflake Quickstarts)
:   Use a tutorial to learn the basics of Snowpark with Scala.

## Developer Guides[¶](#developer-guides "Link to this heading")

[Creating a Session for Snowpark Scala](creating-session)
:   Establish a session with which you interact with the Snowflake database.

[Working with DataFrames in Snowpark Scala](working-with-dataframes)
:   Query and process data with a `DataFrame` object.

[Creating User-Defined Functions (UDFs) for DataFrames in Scala](creating-udfs)
:   Create user-defined functions (UDFs) using the Snowpark API.

[Creating stored procedures for DataFrames in Scala](creating-sprocs)
:   Create stored procedures using the Snowpark API.

[Calling functions and stored procedures in Snowpark Scala](calling-functions)
:   Use the Snowpark API to call system-defined functions, UDFs, and stored procedures.

[A Simple Example of Using Snowpark Scala](example)
:   See example code for an application that prints information about tables in Snowflake.

[Logging, tracing, and metrics](../../logging-tracing/logging-tracing-overview)
:   Record log messages and trace events in an event table for analysis later.

[Analyzing Queries and Troubleshooting with Snowpark Scala](troubleshooting)
:   Troubleshoot your code with logging and by viewing underlying SQL.

## Reference[¶](#reference "Link to this heading")

[Quick reference: Snowpark Scala APIs for SQL commands](sql-to-snowpark)
:   Learn how SQL statements map to Snowpark APIs for common operations.

[Snowpark Library for Scala API Reference](/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/index.html)
:   Read details about the classes and methods in the Snowpark API.

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

1. [Get Started](#get-started)
2. [Developer Guides](#developer-guides)
3. [Reference](#reference)

Related content

1. [Snowpark API](/developer-guide/snowpark/scala/../index)
2. [Snowpark Library for Scala and Java release notes](/developer-guide/snowpark/scala/../../../release-notes/clients-drivers/snowpark-scala-java)
3. [Getting Started With Snowpark in Scala](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_scala/index.html)