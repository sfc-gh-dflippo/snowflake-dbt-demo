---
auto_generated: true
description: With Snowpark Connect for Apache Spark™, you can connect your existing
  Spark workloads directly to Snowflake and run them on the Snowflake compute engine.
  Snowpark Connect for Spark supports using the
last_scraped: '2026-01-14T16:54:26.416102+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-overview
title: Run Apache Spark™ workloads on Snowflake with Snowpark Connect for Spark |
  Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](snowpark-connect-overview.md)

   * [Development clients](snowpark-connect-clients.md)
   * [Cloud service data access](snowpark-connect-file-data.md)
   * [Snowflake SQL execution](snowpark-connect-snowflake-sql.md)
   * [Batch workloads with Snowpark Submit](snowpark-submit.md)
   * [Compatibility](snowpark-connect-compatibility.md)
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

[Developer](../../developer.md)Spark workloads on Snowflake

# Run Apache Spark™ workloads on Snowflake with Snowpark Connect for Spark[¶](#run-spark-tm-workloads-on-snowflake-with-spconnect "Link to this heading")

With Snowpark Connect for Apache Spark™, you can connect your existing Spark workloads directly to Snowflake and run them on the Snowflake compute engine.
Snowpark Connect for Spark supports using the [Spark DataFrame API](https://spark.apache.org/docs/latest/sql-programming-guide.html) on Snowflake.
All workloads run on Snowflake warehouse. As a result, you can run your PySpark dataframe code with all the benefits of the
Snowflake engine.

In Apache Spark™ version 3.4, the Apache Spark community introduced Spark Connect. Its decoupled client-server architecture separates
the user’s code from the Spark cluster where the work is done. This new architecture makes it possible for Snowflake to power Spark jobs.

You can [develop using familiar client tools](#label-snowpark-connect-overview-develop).

Snowpark Connect for Spark offers the following benefits:

* Decouples client and server, so that Spark code can run remotely against the Snowflake compute engine without your needing to manage a
  Spark cluster.
* Lets team use their existing ecosystem to author and orchestrate their Spark workloads—for example, Jupyter notebooks, VS code,
  and Airflow.
* Allows you to reuse open source Spark dataframes and Spark SQL code with minimal migrations or changes.
* Offers a streamlined way to integrate Snowflake governance, security, and scalability into Spark-based workflows, supporting a familiar
  PySpark experience with pushdown optimizations into Snowflake.
* Allows you to use any of several languages, including PySpark and Spark SQL.

## Get started with Snowpark Connect for Spark[¶](#get-started-with-spconnect "Link to this heading")

To get started with Snowpark Connect for Spark, follow these steps:

1. [Set up the client tool](snowpark-connect-clients) that you’ll use to develop Spark
   workloads to run on Snowflake.

   For example, you can use [Snowflake Notebooks](snowpark-connect-workloads-snowflake-notebook)
   or [another tool](snowpark-connect-workloads-jupyter).
2. Run Spark workloads asynchronously using Snowpark Submit.

   For more information, see [Run Spark batch workloads from Snowpark Submit](snowpark-submit).
3. Get to know Snowpark Connect for Spark support for Spark particulars.

   For more information, see [Snowpark Connect for Spark compatibility guide](snowpark-connect-compatibility).

## Develop and run Spark workloads on Snowflake[¶](#develop-and-run-spark-workloads-on-snowflake "Link to this heading")

You can use familiar development tools to develop Spark workloads that run on Snowflake, and then run those workloads in batches by
using the Snowpark Submit command-line tool.

* You can use local tools for interactive development.

  Using tools such as [Snowflake Notebooks](snowpark-connect-workloads-snowflake-notebook)
  [and others](snowpark-connect-workloads-jupyter), you can develop Spark
  workloads. You can authenticate with Snowflake, start a Spark session, and run PySpark code to load, transform, and analyze data.
* You can run non-interactive, asynchronous Spark workloads directly on Snowflake’s infrastructure while using familiar Spark semantics.

  With Snowpark Submit, you can submit production-ready Spark applications using a simple CLI interface and using your tools, including Airflow.

  For more information, see [Run Spark batch workloads from Snowpark Submit](snowpark-submit).

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

1. [Get started with Snowpark Connect for Spark](#get-started-with-spconnect)
2. [Develop and run Spark workloads on Snowflake](#develop-and-run-spark-workloads-on-snowflake)

Related content

1. [Snowpark Connect for Spark compatibility guide](/developer-guide/snowpark-connect/snowpark-connect-compatibility)
2. [Snowpark Connect for Spark release notes](/developer-guide/snowpark-connect/../../release-notes/clients-drivers/snowpark-connect)