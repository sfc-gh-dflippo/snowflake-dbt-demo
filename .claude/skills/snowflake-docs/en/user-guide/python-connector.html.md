---
auto_generated: true
description: Note
last_scraped: '2026-01-14T16:55:13.577066+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/python-connector.html
title: Snowflake Connector for Python | Snowflake Documentation
---

1. [Overview](../developer.md)
2. Builders
3. [Snowflake DevOps](../developer-guide/builders/devops.md)
4. [Observability](../developer-guide/builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../developer-guide/snowpark/index.md)
7. [Spark workloads on Snowflake](../developer-guide/snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../developer-guide/snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../developer-guide/snowpark-container-services/overview.md)
12. [Functions and procedures](../developer-guide/extensibility.md)
13. [Logging, Tracing, and Metrics](../developer-guide/logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../developer-guide/snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../developer-guide/snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../developer-guide/sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../developer-guide/streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../developer-guide/streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../developer-guide/streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../developer-guide/streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../developer-guide/streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../developer-guide/streamlit/object-management/billing.md)
      - [Security considerations](../developer-guide/streamlit/object-management/security.md)
      - [Privilege requirements](../developer-guide/streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../developer-guide/streamlit/object-management/owners-rights.md)
      - [PrivateLink](../developer-guide/streamlit/object-management/privatelink.md)
      - [Logging and tracing](../developer-guide/streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../developer-guide/streamlit/app-development/runtime-environments.md)
      - [Dependency management](../developer-guide/streamlit/app-development/dependency-management.md)
      - [File organization](../developer-guide/streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../developer-guide/streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../developer-guide/streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../developer-guide/streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../developer-guide/streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../developer-guide/streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../developer-guide/streamlit/features/git-integration.md)
      - [External access](../developer-guide/streamlit/features/external-access.md)
      - [Row access policies](../developer-guide/streamlit/features/row-access.md)
      - [Sleep timer](../developer-guide/streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../developer-guide/streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../developer-guide/streamlit/troubleshooting.md)
    - [Release notes](../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../developer-guide/declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../developer-guide/native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../developer-guide/snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
30. [Git](../developer-guide/git/git-overview.md)
31. Drivers
32. [Overview](../developer-guide/drivers.md)

    * [Go](../developer-guide/golang/go-driver.md)
    * [JDBC](../developer-guide/jdbc/jdbc.md)
    * [.NET](../developer-guide/dotnet/dotnet-driver.md)
    * [Node.js](../developer-guide/node-js/nodejs-driver.md)
    * [ODBC](../developer-guide/odbc/odbc.md)
    * [PHP](../developer-guide/php-pdo/php-pdo-driver.md)
    * [Python](../developer-guide/python-connector/python-connector.md)

      + [Installing](../developer-guide/python-connector/python-connector-install.md)
      + [Connecting](../developer-guide/python-connector/python-connector-connect.md)
      + [Using](../developer-guide/python-connector/python-connector-example.md)
      + [pandas DataFrames](../developer-guide/python-connector/python-connector-pandas.md)
      + [Distributing workloads](../developer-guide/python-connector/python-connector-distributed-fetch.md)
      + [Usage with SQLAlchemy](../developer-guide/python-connector/sqlalchemy.md)
      + [API](../developer-guide/python-connector/python-connector-api.md)
      + [Dependency management policy](../developer-guide/python-connector/python-connector-dependencies.md)
33. [Considerations when drivers reuse sessions](../developer-guide/driver-connections.md)
34. [Scala versions](../developer-guide/scala-version-differences.md)
35. Reference
36. [API Reference](../api-reference.md)

[Developer](../developer.md)[Overview](../developer-guide/drivers.md)Python

# Snowflake Connector for Python[¶](#snowflake-connector-for-python "Link to this heading")

Note

This driver currently does not support GCP regional endpoints. Please ensure that any workloads using through this driver do not require support for regional endpoints on GCP. If you have questions about this, please contact Snowflake Support.

The Snowflake Connector for Python provides an interface for developing Python applications that can connect to Snowflake and perform all standard operations. It provides a programming alternative to
developing applications in Java or C/C++ using the Snowflake JDBC or ODBC drivers.

The connector is a native, pure Python package that has no dependencies on JDBC or ODBC. It can be installed using `pip` on
Linux, MacOS, and Windows platforms where Python is installed.

The connector supports developing applications using the Python Database API v2 specification (PEP-249), including using the following standard API objects:

* `Connection` objects for connecting to Snowflake.
* `Cursor` objects for executing DDL/DML statements and queries.

For more information, see [PEP-249](https://www.python.org/dev/peps/pep-0249/).

[SnowSQL](../../user-guide/snowsql), the command-line client provided by Snowflake, is an example of an application developed using the connector.

Note

Snowflake now provides first-class Python APIs for managing core Snowflake resources including databases, schemas, tables, tasks, and
warehouses, without using SQL. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](../snowflake-python-api/snowflake-python-overview).

**Next Topics:**

* [Installing the Python Connector](python-connector-install)
* [Using the Python Connector](python-connector-example)
* [Using pandas DataFrames with the Python Connector](python-connector-pandas)
* [Distributing workloads that fetch results with the Snowflake Connector for Python](python-connector-distributed-fetch)
* [Using the Snowflake SQLAlchemy toolkit with the Python Connector](sqlalchemy)
* [Python Connector API](python-connector-api)
* [Dependency management policy for the Python Connector](python-connector-dependencies)

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

1. [Client versions & support policy](/developer-guide/python-connector/../../release-notes/requirements)
2. [Snowflake Connector for Python release notes](/developer-guide/python-connector/../../release-notes/clients-drivers/python-connector)
3. [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/python-connector/../snowflake-python-api/snowflake-python-overview)

Related info

For a tutorial on using the Snowflake Connector for Python, see the following page:

* [Getting Started with Python](https://quickstarts.snowflake.com/guide/getting_started_with_python/index.html) (Snowflake Quickstarts)

For information about changes in the latest version of the Snowflake Connector for Python, see the following page:

* [Python Connector Release Notes](https://github.com/snowflakedb/snowflake-connector-python/blob/master/DESCRIPTION.md) (GitHub)