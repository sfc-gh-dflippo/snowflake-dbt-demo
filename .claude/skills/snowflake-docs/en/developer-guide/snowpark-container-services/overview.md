---
auto_generated: true
description: Feature — Generally Available
last_scraped: '2026-01-14T16:55:06.227771+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview
title: Snowpark Container Services | Snowflake Documentation
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
11. [Snowpark Container Services](overview.md)

    * [Tutorials](overview-tutorials.md)
    * [Service Specification Reference](specification-reference.md)
    * [Working with an Image Registry and Repository](working-with-registry-repository.md)
    * [Working with Compute Pools](working-with-compute-pool.md)
    * [Working with Services](working-with-services.md)
    * [Monitoring Services](monitoring-services.md)
    * [Configuring private connectivity](private-connectivity.md)
    * [Snowpark Container Services Troubleshooting](troubleshooting.md)
    * [Snowpark Container Services Costs](accounts-orgs-usage-views.md)
    * [Advanced Tutorials](overview-advanced-tutorials.md)
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

[Developer](../../developer.md)Snowpark Container Services

# Snowpark Container Services[¶](#snowpark-container-services "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](../../user-guide/intro-regions.html#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](#label-snowpark-containers-overview-available-regions).

## About Snowpark Container Services[¶](#about-snowpark-container-services "Link to this heading")

Snowflake started by providing a SQL database for querying structured and semi-structured data, but SQL alone isn’t ideal for complex computations or machine learning. To address this, Snowflake introduced [Snowpark](../snowpark/index), which lets developers use languages like Python, Java, and Scala to build data applications and pipelines. Snowpark translates this code into optimized SQL, combining the flexibility of modern languages with the performance and scalability of Snowflake’s SQL engine.

For more flexibility, Snowflake offers Snowpark Container Services, a managed container orchestration platform within Snowflake. You can package your application and its dependencies into an Open Container Initiative (OCI) image, which can include any programming language, framework, or library.
This enables use cases that require custom runtimes, specialized libraries, or specific software configurations. In addition, with support for advanced CPUs and GPUs, you can run compute-intensive workloads, such as ML model serving, ML model training, and advanced AI analytics. Snowflake manages the underlying infrastructure, but you have full control over the contents of your containerized environment.

As a fully managed service, Snowpark Container Services streamlines operational tasks related to running your containers. Using best practices, Snowpark Container Services handles the intricacies of container management, including security and configuration. This ensures that you can focus on developing and deploying your applications without the overhead of managing the underlying infrastructure.

Snowpark Container Services is fully integrated with Snowflake. For example, your application can easily perform these tasks:

* Connect to Snowflake and run SQL in a Snowflake virtual warehouse.
* Access data files in a Snowflake stage.
* Process data retrieved through SQL queries.

Your application can leverage your existing Snowflake configuration, including the following items:

* Network policies for network ingress
* External access integration for network egress
* Role-based access control for enabling service-to-service communications
* Event tables for logs, metrics, and events

Snowpark Container Services is also integrated with third-party tools. It lets you use third-party clients, such as Docker, to easily upload your application images to Snowflake. Seamless integration makes it easier for teams to focus on building data applications.

All these capabilities come with Snowflake platform benefits, most notably ease-of-use, security, and governance features. You also get a scalable, flexible compute layer next to the powerful Snowflake data layer without needing to move data off the platform.

## Common scenarios for using Snowpark Container Services[¶](#common-scenarios-for-using-snowpark-container-services "Link to this heading")

Your application can be deployed to Snowflake regions without concern for the underlying cloud platform (AWS, Azure, or Google Cloud). Snowpark Container Services also makes it easy for your application to access your Snowflake data. In addition, Snowflake manages the underlying compute nodes.

The following list shows the common workloads for Snowpark Container Services:

* **Batch Data Processing Jobs:** Run flexible jobs similar to stored procedures, pulling data from Snowflake or external sources, processing it, and producing results. Workloads can be distributed across multiple job instances, and graphics processing unit (GPU) support is available for computationally intensive tasks like AI and machine learning.
* **Service Functions:** Your service can provide a service function so that your queries can send batches of data to your service for processing. The query processing happens in Snowflake’s advanced query engine and your service provides custom data processing that Snowflake can scale to multiple compute nodes. For an example, see [Tutorial 1](tutorials/tutorial-1). In step 4 of this tutorial, you call the service function in a query.
* **APIs or Web UI Over Snowflake Data:** Deploy services that expose APIs or web interfaces with embedded business logic. Users interact with the service rather than raw data. Caller’s rights ensure that queries run with the correct user permissions. For an example, see [Tutorial 1](tutorials/tutorial-1). In this tutorial, the service also exposes a web UI to the internet. In step 4, you send requests to the service from a web browser.

## How does it work?[¶](#how-does-it-work "Link to this heading")

To run containerized applications in Snowpark Container Services, in addition to working with the basic Snowflake objects, such
as databases and warehouses, you work with these objects: [image repository](working-with-registry-repository),
[compute pool](working-with-compute-pool), and [service](working-with-services).

Snowflake offers an [OCIv2](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)
compliant *image registry* service for storing your images. This service enables Open Container Initiative (OCI) clients, such as Docker CLI, to upload your application images to a *repository* (a storage unit) in your
Snowflake account. You create a repository using the [CREATE IMAGE REPOSITORY](../../sql-reference/sql/create-image-repository) command. For more information, see
[Working with an image registry and repository](working-with-registry-repository).

After you upload your application image to a repository, you can run your application by creating a
[long-running service or executing a job service](working-with-services).

* **Service:** A service is long-running and, as with a web service, you explicitly stop it when it is no longer needed. If a service container
  exits for whatever reason, Snowflake restarts that container. To create a service, such as a full stack web application,
  use the [CREATE SERVICE](../../sql-reference/sql/create-service) command.
* **Job service:** A job service has a finite lifespan, similar to a stored procedure.
  When all containers exit, the job service is done. Snowflake doesn’t restart any job service containers. To start a job service, such as training a machine learning model with GPUs, use the
  [EXECUTE JOB SERVICE](../../sql-reference/sql/execute-job-service) command.

Your services, including job services, run in a *compute pool*, which is a collection of one or more virtual machine (VM) nodes. You first
create a compute pool by using the [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool) command, and then specify the compute pool when
you create a service or a job service. The required information to create a compute pool includes the machine type, the minimum number of nodes to
launch the compute pool with, and the maximum number of nodes the compute pool can scale to. Some of the supported machine types
provide GPU. For more information, see [Working with compute pools](working-with-compute-pool).

After you create a service, users in the same Snowflake account that created the service can use the service, if they have the appropriate permissions. For more information, see [Using a service](working-with-services.html#label-snowpark-containers-service-communicating).

Note

The Snowpark Container Services documentation primarily uses SQL commands and functions in explanations of concepts and in examples. Snowflake also provides other interfaces, including [Python APIs](../snowflake-python-api/snowflake-python-overview), [REST APIs](../snowflake-rest-api/snowflake-rest-api), and the [Snowflake CLI](../snowflake-cli/index) command-line tool for most operations.

## Available regions and considerations[¶](#available-regions-and-considerations "Link to this heading")

Snowpark Container Services is in all [regions](../../user-guide/intro-regions) except the following:

* Snowpark Container Services supports [public sector (government) workloads](../../user-guide/intro-regions.html#label-us-gov-regions) in the AWS US East (Commercial Gov - N. Virginia) region and is not available in other AWS or Azure government regions.
* Currently, Snowpark Container Services in the GCP Dammam region uses the global endpoints for Google Cloud APIs.

## What’s next?[¶](#what-s-next "Link to this heading")

If you’re new to Snowpark Container Services, we suggest that you first explore the tutorials and then continue with other
topics to learn more and create your own containerized applications. The following topics provide more information:

* **Tutorials:** These [introductory tutorials](overview-tutorials) provide step-by-step instructions for you to explore
  Snowpark Container Services. After initial exploration, you can continue with
  [advanced tutorials](overview-advanced-tutorials).
* **Service specification reference:** This reference explains the [YAML syntax](specification-reference) to
  create a service specification.
* **Working with services and job services:** These topics provide details about the Snowpark Container Services components that you use
  in developing services and job services:

  + [Working with an image registry and repository](working-with-registry-repository)
  + [Working with compute pools](working-with-compute-pool)
  + [Working with services](working-with-services)
  + [Troubleshooting](troubleshooting)
* **Reference:** Snowpark Container Services provides the following SQL commands and functions:

  + SQL commands: [Snowpark Container Services commands](../../sql-reference/commands-snowpark-container-services) and [CREATE FUNCTION (Snowpark Container Services)](../../sql-reference/sql/create-function-spcs)
  + SQL functions:

    - System function: [SYSTEM$GET\_SERVICE\_LOGS](../../sql-reference/functions/system_get_service_logs)
    - Scalar functions: [Snowpark Container Services functions](../../sql-reference/functions-spcs)
    - Table-valued functions:

      * [GET\_JOB\_HISTORY](../../sql-reference/functions/get_job_history)
      * [SPCS\_GET\_LOGS](../../sql-reference/functions/spcs_get_logs)
      * [SPCS\_GET\_EVENTS](../../sql-reference/functions/spcs_get_events)
      * [SPCS\_GET\_METRICS](../../sql-reference/functions/spcs_get_metrics)
* **Billing:** This topic explains the costs associated with using Snowpark Container Services:

  + [Snowpark Container Services costs](accounts-orgs-usage-views)

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

1. [About Snowpark Container Services](#about-snowpark-container-services)
2. [Common scenarios for using Snowpark Container Services](#common-scenarios-for-using-snowpark-container-services)
3. [How does it work?](#how-does-it-work)
4. [Available regions and considerations](#available-regions-and-considerations)
5. [What’s next?](#what-s-next)

Related content

1. [Working with Repository](/developer-guide/snowpark-container-services/working-with-registry-repository)
2. [Working with Compute Pool](/developer-guide/snowpark-container-services/working-with-compute-pool)
3. [Working with Services](/developer-guide/snowpark-container-services/working-with-services)