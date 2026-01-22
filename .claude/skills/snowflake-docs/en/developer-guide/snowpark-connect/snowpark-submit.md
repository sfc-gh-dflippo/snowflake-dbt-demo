---
auto_generated: true
description: 'You can run Spark workloads in a non-interactive, asynchronous way directly
  on Snowflake’s infrastructure while you use familiar Spark semantics. With Snowpark
  Submit, you can submit production-ready '
last_scraped: '2026-01-14T16:57:53.302356+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-submit
title: Run Spark batch workloads from Snowpark Submit | Snowflake Documentation
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

     + [Installation](snowpark-submit-install.md)
     + [Reference](snowpark-submit-reference.md)
     + [Examples](snowpark-submit-examples.md)
     + [Troubleshooting](snowpark-submit-troubleshooting.md)
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

[Developer](../../developer.md)[Spark workloads on Snowflake](snowpark-connect-overview.md)Batch workloads with Snowpark Submit

# Run Spark batch workloads from Snowpark Submit[¶](#run-spark-batch-workloads-from-spsubmit "Link to this heading")

You can run Spark workloads in a non-interactive, asynchronous way directly on Snowflake’s infrastructure while you use familiar
Spark semantics. With Snowpark Submit, you can submit production-ready Spark applications—such as ETL pipelines and scheduled data
transformations—by using a simple CLI interface. In this way, you can maintain your existing Spark development workflows without a
dedicated Spark cluster.

For example, you can package your PySpark ETL script, then use the Snowpark Submit CLI to run the script as a batch job on a Snowpark Container Services container.
This method lets you automate nightly data pipelines with Apache Airflow or CI/CD tools. Your Spark code runs in cluster mode on Snowpark Container Services,
scaling seamlessly with built-in dependency and resource management.

For examples of Snowpark Submit in use, see [Snowpark Submit examples](snowpark-submit-examples).

Snowpark Submit runs Spark workloads on Snowflake by using Snowpark Connect for Spark. For more information about Snowpark Connect for Spark, see
[Run Apache Spark™ workloads on Snowflake with Snowpark Connect for Spark](snowpark-connect-overview).

Snowpark Submit offers the following benefits:

* Ability to run in cluster mode on Snowflake-managed infrastructure with no external Spark setup
* Workflow integration, supporting automation through CI/CD pipelines, Apache Airflow, or cron-based scheduling
* Support for Python, enabling reuse of existing Spark applications across languages
* Dependency management, with support for packaging external Python modules or JARs

Note

**snowpark-submit** supports much of the same functionality as **spark-submit**. However, some functionality has been
omitted because it is not needed when running Spark workloads on Snowflake.

## Get started with Snowpark Submit[¶](#get-started-with-spsubmit "Link to this heading")

To get started using Snowpark Submit, follow these steps:

1. Install Snowpark Submit by following the steps in [Install Snowpark Submit](snowpark-submit-install).
2. Study the [Snowpark Submit examples](snowpark-submit-examples).
3. Get to know how to use Snowpark Submit with [Snowpark Submit reference](snowpark-submit-reference).

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

1. [Get started with Snowpark Submit](#get-started-with-spsubmit)

Related content

1. [Run Apache Spark™ workloads on Snowflake with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-overview)
2. [Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-submit-reference)