---
auto_generated: true
description: The Snowflake Connector for Spark (“Spark connector”) brings Snowflake
  into the Apache Spark ecosystem, enabling Spark to read data from, and write data
  to, Snowflake. From Spark’s perspective, Snowfl
last_scraped: '2026-01-14T16:58:06.434328+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/spark-connector
title: Snowflake Connector for Spark | Snowflake Documentation
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

    * [Kafka Connector](kafka-connector.md)
    * [Spark Connector](spark-connector.md)

      + [Overview](spark-connector-overview.md)
      + [Install](spark-connector-install.md)
      + [Configure](spark-connector-databricks.md)
      + [Qubole](spark-connector-qubole.md)
      + [Usage](spark-connector-use.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../developer-guide/snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
30. [Git](../developer-guide/git/git-overview.md)
31. Drivers
32. [Overview](../developer-guide/drivers.md)
33. [Considerations when drivers reuse sessions](../developer-guide/driver-connections.md)
34. [Scala versions](../developer-guide/scala-version-differences.md)
35. Reference
36. [API Reference](../api-reference.md)

[Developer](../developer.md)[Kafka and Spark Connectors](connectors.md)Spark Connector

# Snowflake Connector for Spark[¶](#snowflake-connector-for-spark "Link to this heading")

The Snowflake Connector for Spark (“Spark connector”) brings Snowflake into the Apache Spark ecosystem, enabling Spark to read
data from, and write data to, Snowflake.
From Spark’s perspective, Snowflake looks similar to other Spark data sources (PostgreSQL, HDFS, S3, etc.).

Note

As an alternative to using Spark, consider writing your code to use [Snowpark API](../developer-guide/snowpark/index) instead. Snowpark
allows you to perform all of your work within Snowflake (rather than in a separate Spark compute cluster). Snowpark also
supports pushdown of all operations, including Snowflake UDFs.

Snowflake supports multiple versions of the Spark connector:

> * Spark Connector 2.x: Spark versions 3.2, 3.3, and 3.4.
>
>   + There’s a separate version of the Snowflake connector for each version of Spark. Use the correct version of the connector for your version of Spark.
> * Spark Connector 3.x: Spark versions 3.2, 3.3, 3.4, and 3.5.
>
>   + Each Spark Connector 3 package supports most versions of Spark.

The connector runs as a Spark plugin and is provided as a Spark package (`spark-snowflake`).

**Next Topics:**

* [Overview of the Spark Connector](spark-connector-overview)
* [Installing and Configuring the Spark Connector](spark-connector-install)
* [Configuring Snowflake for Spark in Databricks](spark-connector-databricks)
* [Configuring Snowflake for Spark in Qubole](spark-connector-qubole)
* [Using the Spark Connector](spark-connector-use)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.