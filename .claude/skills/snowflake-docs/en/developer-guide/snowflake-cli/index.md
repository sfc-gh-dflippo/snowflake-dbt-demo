---
auto_generated: true
description: Snowflake CLI is an open-source command-line tool explicitly designed
  for developer-centric workloads in addition to SQL operations. It is a flexible
  and extensible tool that can accommodate modern de
last_scraped: '2026-01-14T16:55:45.497516+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-cli/index
title: Snowflake CLI | Snowflake Documentation
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
27. [Snowflake Scripting Developer Guide](../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](index.md)

    * [Introduction](introduction/introduction.md)
    * [Installing Snowflake CLI](installation/installation.md)
    * [Configuring Snowflake CLI and connecting to Snowflake](connecting/connect.md)
    * [Bootstrapping a project from a template](bootstrap-project/bootstrap.md)
    * [Project definition files](project-definitions/about.md)
    * [Managing Snowflake objects](objects/manage-objects.md)
    * [Managing Snowflake stages](stages/manage-stages.md)
    * [Managing Container Services](services/overview.md)
    * [Using Snowpark APIs](snowpark/overview.md)
    * [Working with notebooks](notebooks/use-notebooks.md)
    * [Working with Streamlit in Snowflake](streamlit-apps/overview.md)
    * [Using Snowflake Native Apps](native-apps/overview.md)
    * [Executing SQL](sql/execute-sql.md)
    * [Managing Snowflake Git repositories](git/overview.md)
    * [Managing data pipelines](data-pipelines/data-pipelines.md)
    * [Integrating CI/CD with Snowflake CLI](cicd/integrate-ci-cd.md)
    * [Migrating from SnowSQL](../../user-guide/snowsql-migrate.md)
    * [Command reference](command-reference/overview.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)Snowflake CLI

# Snowflake CLI[¶](#sf-cli "Link to this heading")

## What is Snowflake CLI?[¶](#what-is-sf-cli "Link to this heading")

Snowflake CLI is an open-source command-line tool explicitly designed for developer-centric workloads in
addition to SQL operations. It is a flexible and extensible tool that can accommodate modern development practices and
technologies.

With Snowflake CLI, developers can create, manage, update, and view apps running on Snowflake across workloads such as
Streamlit in Snowflake, the Snowflake Native App Framework, Snowpark Container Services, and Snowpark. It supports a range of Snowflake features,
including user-defined functions, stored procedures, Streamlit in Snowflake, and SQL execution.

## What’s in this guide?[¶](#what-s-in-this-guide "Link to this heading")

This guide introduces and explains how to install and use Snowflake CLI. It includes the following sections:

* [Introducing Snowflake CLI](introduction/introduction)
* [Installing Snowflake CLI](installation/installation)
* [Configuring Snowflake CLI and connecting to Snowflake](connecting/connect)
* [Bootstrapping a project from a template](bootstrap-project/bootstrap)
* [About project definition files](project-definitions/about)
* [Managing Snowflake objects](objects/manage-objects)
* [Managing Snowflake stages](stages/manage-stages)
* [Managing Snowpark Container Services in Snowflake CLI](services/overview)
* [Using Snowpark in Snowflake CLI](snowpark/overview)
* [Using Snowflake Notebooks](notebooks/use-notebooks)
* [Managing Streamlit apps with Snowflake CLI](streamlit-apps/overview)
* [Using Snowflake Native App in Snowflake CLI](native-apps/overview)
* [Executing SQL statements](sql/execute-sql)
* [Managing Git repositories](git/overview)
* [Snowflake CLI command reference](command-reference/overview)

For more information about supported Snowflake products, see the following:

* [Snowflake Cortex](../../user-guide/snowflake-cortex/aisql) documentation
* [Native App Framework](../native-apps/native-apps-about) documentation
* [Snowflake notebooks](../../user-guide/ui-snowsight/notebooks) documentation
* [Snowpark Container Services](../snowpark-container-services/overview) documentation
* [Snowpark](../snowpark/index) documentation
* [SQL](../../reference) documentation
* [Git](../git/git-overview) documentation
* [Streamlit](../streamlit/about-streamlit) documentation

To see what changed in this release, see the [Snowflake CLI release notes](../../release-notes/clients-drivers/snowflake-cli).

Snowflake CLI is an open-source project available in the [Snowflake CLI Git repository](https://github.com/snowflakedb/snowflake-cli).

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

1. [What is Snowflake CLI?](#what-is-sf-cli)
2. [What’s in this guide?](#what-s-in-this-guide)

Related content

1. [Introducing Snowflake CLI](/developer-guide/snowflake-cli/introduction/introduction)
2. [Git in Snowflake](/developer-guide/snowflake-cli/../git/git-overview)
3. [Native App Framework](/developer-guide/snowflake-cli/../native-apps/native-apps-about)
4. [Snowflake Notebooks](/developer-guide/snowflake-cli/../../user-guide/ui-snowsight/notebooks)
5. [Snowpark Container Services](/developer-guide/snowflake-cli/../snowpark-container-services/overview)
6. [Snowpark](/developer-guide/snowflake-cli/../snowpark/index)
7. [SQL](/developer-guide/snowflake-cli/../../reference)
8. [Streamlit](/developer-guide/snowflake-cli/../streamlit/about-streamlit)
9. [Snowflake CLI release notes](/developer-guide/snowflake-cli/../../release-notes/clients-drivers/snowflake-cli)
10. [Snowflake CLI Git repository](https://github.com/snowflakedb/snowflake-cli)