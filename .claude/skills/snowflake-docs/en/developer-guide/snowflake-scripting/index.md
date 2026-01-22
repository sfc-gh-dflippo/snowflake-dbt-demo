---
auto_generated: true
description: Snowflake Scripting is an extension to Snowflake SQL that adds support
  for procedural logic. You can use Snowflake Scripting syntax in stored procedures
  and user-defined functions (UDFs). You can also
last_scraped: '2026-01-14T16:55:12.824697+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/index
title: Snowflake Scripting Developer Guide | Snowflake Documentation
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
13. [Logging, Tracing, and Metrics](../logging-tracing/logging-tracing-overview.md)
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
27. [Snowflake Scripting Developer Guide](index.md)

    * [Blocks](blocks.md)
    * [Variables](variables.md)
    * [Returning a value](return.md)
    * [Conditional logic](branch.md)
    * [Loops](loops.md)
    * [Cursors](cursors.md)
    * [RESULTSETs](resultsets.md)
    * [Asynchronous child jobs](asynchronous-child-jobs.md)
    * [Exceptions](exceptions.md)
    * [Affected rows](dml-status.md)
    * [Getting a query ID](query-id.md)
    * [Examples for common use cases of Snowflake Scripting](use-cases.md)
    * [Using Snowflake Scripting in Snowflake CLI, SnowSQL, or the Python Connector](running-examples.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)Snowflake Scripting Developer Guide

# Snowflake Scripting Developer Guide[¶](#snowflake-scripting-developer-guide "Link to this heading")

Snowflake Scripting is an extension to Snowflake SQL that adds support for procedural logic. You can use Snowflake
Scripting syntax in [stored procedures](../stored-procedure/stored-procedures-overview) and
[user-defined functions (UDFs)](../udf/sql/udf-sql-procedural-functions). You can also use Snowflake
Scripting syntax outside of stored procedures and UDFs and stored procedures. The next topics explain how to use
Snowflake Scripting.

[Understanding blocks in Snowflake Scripting](blocks)
:   Learn the basic structure of Snowflake Scripting code.

[Working with variables](variables)
:   Declare and use variables.

[Returning a value](return)
:   Return values from stored procedures and an anonymous block.

[Working with conditional logic](branch)
:   Control flow with IF and CASE statements.

[Working with loops](loops)
:   Control flow with FOR, WHILE, REPEAT, and LOOP.

[Working with cursors](cursors)
:   Iterate through query results with a cursor.

[Working with RESULTSETs](resultsets)
:   Iterate over the result set returned by a query.

[Handling exceptions](exceptions)
:   Handle errors by handling and raising exceptions.

[Determining the number of rows affected by DML commands](dml-status)
:   Use global variables to determine the effect of data manipulation language (DML) commands.

[Getting the query ID of the last query](query-id)
:   Use the global variable SQLID to get the query ID of the last query.

[Examples for common use cases of Snowflake Scripting](use-cases)
:   Explore examples of Snowflake Scripting code for some common use cases.

[Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)
:   Run the Snowflake Scripting examples in SnowSQL, Snowsight and Python Connector code.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Related content

1. [Snowflake Scripting reference](/developer-guide/snowflake-scripting/../../sql-reference-snowflake-scripting)
2. [Writing stored procedures in Snowflake Scripting](/developer-guide/snowflake-scripting/../stored-procedure/stored-procedures-snowflake-scripting)
3. [Snowflake Scripting UDFs](/developer-guide/snowflake-scripting/../udf/sql/udf-sql-procedural-functions)