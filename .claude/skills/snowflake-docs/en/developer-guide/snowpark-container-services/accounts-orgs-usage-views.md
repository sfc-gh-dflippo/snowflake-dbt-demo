---
auto_generated: true
description: Feature — Generally Available
last_scraped: '2026-01-14T16:56:00.865200+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en//developer-guide/snowpark-container-services/accounts-orgs-usage-views
title: Snowpark Container Services costs | Snowflake Documentation
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

[Developer](../../developer.md)[Snowpark Container Services](overview.md)Snowpark Container Services Costs

# Snowpark Container Services costs[¶](#snowpark-container-services-costs "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](../../user-guide/intro-regions.html#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](overview.html#label-snowpark-containers-overview-available-regions).

The costs associated with using Snowpark Container Services can be categorized into storage cost, compute pool cost, and data
transfer cost.

## Storage cost[¶](#storage-cost "Link to this heading")

When you use Snowpark Container Services, storage costs associated with Snowflake, including the cost of Snowflake stage usage
or database table storage, apply. For more information, see [Exploring storage cost](../../user-guide/cost-exploring-data-storage). In addition, the
following cost considerations apply:

* **Image repository storage cost:** The implementation of the [image repository](working-with-registry-repository) uses
  a Snowflake stage. Therefore, the associated cost for using the Snowflake stage applies.
* **Log storage cost:** When you store
  [local container logs in event tables](monitoring-services.html#label-snowpark-containers-working-with-services-local-logs), event table storage
  costs apply.
* **Mounting volumes cost:**

  + When you mount a Snowflake stage as a volume, the cost of using the Snowflake stage applies.
  + When you mount storage from the compute pool node as a volume, it appears as local storage in the container. But there is no
    additional cost because the local storage cost is covered by the cost of the compute pool node.
* **Block storage cost:** When you create a service that uses [block storage](block-storage-volume), you are billed for block storage and snapshot storage. For more information about storage pricing, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). The SPCS Block Storage Pricing table in this document provides the information.

## Compute pool cost[¶](#compute-pool-cost "Link to this heading")

A [compute pool](working-with-compute-pool) is a collection of one or more virtual machine (VM) nodes on which Snowflake
runs your Snowpark Container Services jobs and services. The number and type (instance family) of the nodes in the compute pool
(see [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool)) determine the credits it consumes and thus the cost you pay. For more information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You incur charges for a compute pool in the IDLE, ACTIVE, STOPPING, or RESIZING state, but not when it is in a STARTING or
SUSPENDED state. To optimize compute pool expenses, you should leverage the AUTO\_SUSPEND feature (see CREATE COMPUTE POOL).

The following views provide usage information:

* **ACCOUNT\_USAGE views**

  The following ACCOUNT\_USAGE views contain Snowpark Container Services credit usage information:

  + The [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view](../../sql-reference/account-usage/snowpark_container_services_history) offers
    credit usage information (hourly consumption) exclusively for Snowpark Container Services.
  + In the [METERING\_DAILY\_HISTORY view](../../sql-reference/account-usage/metering_daily_history), query for rows in which the
    `service_type` column contains the value `SNOWPARK_CONTAINER_SERVICES`.
  + In the [METERING\_HISTORY view](../../sql-reference/account-usage/metering_history), query for rows in which the
    `service_type` column contains the value `SNOWPARK_CONTAINER_SERVICES`.
* **ORGANIZATION\_USAGE views**

  + In the [METERING\_DAILY\_HISTORY view](../../sql-reference/organization-usage/metering_daily_history), use the
    `SERVICE_TYPE = SNOWPARK_CONTAINER_SERVICES` query filter.

## Data transfer cost[¶](#data-transfer-cost "Link to this heading")

Data transfer is the process of moving data into (ingress) and out of (egress) Snowflake. For more information, see
[Understanding data transfer cost](../../user-guide/cost-understanding-data-transfer). When you use Snowpark Container Services, the following additional cost
considerations apply:

* **Outbound data transfer:** Snowflake applies the same data transfer rate for outbound data transfers from services and jobs
  to other cloud regions and to the internet, consistent with the rate for all Snowflake outbound data transfers. For more
  information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) (table 4a).

  You can query the [DATA\_TRANSFER\_HISTORY ACCOUNT\_USAGE view](../../sql-reference/account-usage/data_transfer_history) for
  usage information. The `transfer_type` column identifies this cost as the `SNOWPARK_CONTAINER_SERVICES` type.
* **Internal data transfer:** This class of data transfer refers to data movements across compute entities within Snowflake, such as
  between two compute pools or a compute pool and a warehouse, that resulted from executing a
  [service function](working-with-services.html#label-snowpark-containers-service-communicating).
  For more information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
  (tables 4(a) for AWS, 4(b) for Azure, and the column titled “SPCS Data Transfer to Same Cloud Provider, Same Region”).

  To view the costs associated with internal data transfer, you can do the following:

  + Query the [INTERNAL\_DATA\_TRANSFER\_HISTORY view](../../sql-reference/account-usage/internal_data_transfer_history) in the ACCOUNT\_USAGE schema.
  + Query the [DATA\_TRANSFER\_HISTORY view](../../sql-reference/account-usage/data_transfer_history) in the ACCOUNT\_USAGE schema. The
    `transfer_type` column identifies this cost as the `INTERNAL` type.
  + Query the [DATA\_TRANSFER\_HISTORY view](../../sql-reference/organization-usage/data_transfer_history) in the ORGANIZATION\_USAGE schema.
    The `transfer_type` column identifies this cost as the `INTERNAL` type.
  + Query the [DATA\_TRANSFER\_DAILY\_HISTORY view](../../sql-reference/organization-usage/data_transfer_daily_history) in the ORGANIZATION\_USAGE schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.
  + Query the [RATE\_SHEET\_DAILY view](../../sql-reference/organization-usage/rate_sheet_daily) in the ORGANIZATION USAGE
    schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.
  + Query the [USAGE\_IN\_CURRENCY\_DAILY view](../../sql-reference/organization-usage/usage_in_currency_daily) in the ORGANIZATION USAGE
    schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.

Note

Data transfer costs are currently not billed for Snowflake accounts on Google Cloud.

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

1. [Storage cost](#storage-cost)
2. [Compute pool cost](#compute-pool-cost)
3. [Data transfer cost](#data-transfer-cost)

Related content

1. [Snowpark Container Services](/developer-guide/snowpark-container-services/overview)
2. [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool)