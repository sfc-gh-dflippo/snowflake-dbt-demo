---
auto_generated: true
description: Feature — Generally Available
last_scraped: '2026-01-14T16:54:13.609634+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-integration/openflow/about
title: About Openflow | Snowflake Documentation
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](about.md)

      * [Set up and access Openflow](setup-openflow-roles-login.md)
      * [About Openflow - BYOC Deployments](about-byoc.md)
      * [About Openflow - Snowflake Deployments](about-spcs.md)
      * Connect your data sources using Openflow connectors

        * [About Openflow connectors](connectors/about-openflow-connectors.md)
        * [About SAP® and Snowflake](connectors/about-sap-snowflake.md)
        * Openflow Connector for Amazon Ads

          * [About the connector](connectors/amazon-ads/about.md)
          * [Set up the connector](connectors/amazon-ads/setup.md)
        * Openflow Connector for Box

          * [About the connector](connectors/box/about.md)
          * [Set up the connector](connectors/box/setup.md)
        * Openflow Connector for Google Ads

          * [About the connector](connectors/google-ads/about.md)
          * [Set up the connector](connectors/google-ads/setup.md)
        * Openflow Connector for Google Drive

          * [About the connector](connectors/google-drive/about.md)
          * [Set up the connector](connectors/google-drive/setup.md)
        * Openflow Connector for Google Sheets

          * [About the connector](connectors/google-sheets/about.md)
          * [Set up the connector](connectors/google-sheets/setup.md)
        * Openflow Connector for Jira Cloud

          * [About the connector](connectors/jira-cloud/about.md)
          * [Set up the connector](connectors/jira-cloud/setup.md)
        * Openflow Connector for Kafka

          * [About the connector](connectors/kafka/about.md)
          * [Set up the connector (core)](connectors/kafka/setup.md)")
          * [Performance tuning](connectors/kafka/performance-tuning.md)
        * Openflow Connector for Kinesis Data Streams

          * [About the connector](connectors/kinesis/about.md)
          * [Set up the connector](connectors/kinesis/setup.md)
        * Openflow Connector for LinkedIn Ads

          * [About the connector](connectors/linkedin-ads/about.md)
          * [Set up the connector](connectors/linkedin-ads/setup.md)
        * Openflow Connector for Meta Ads

          * [About the connector](connectors/meta-ads/about.md)
          * [Set up the connector](connectors/meta-ads/setup.md)
        * Openflow Connector for Microsoft Dataverse

          * [About the connector](connectors/dataverse/about.md)
          * [Set up the connector](connectors/dataverse/setup.md)
        * Openflow Connector for MySQL

          * [About the connector](connectors/mysql/about.md)
          * [Set up the connector](connectors/mysql/setup.md)
          * [Set up incremental replication without snapshots](connectors/mysql/incremental-replication.md)
          * [Maintenance](connectors/mysql/maintenance.md)
        * Openflow Connector for PostgreSQL

          * [About the connector](connectors/postgres/about.md)
          * [Set up the connector](connectors/postgres/setup.md)
          * [Set up incremental replication without snapshots](connectors/postgres/incremental-replication.md)
          * [Maintenance](connectors/postgres/maintenance.md)
        * Openflow Connector for SharePoint

          * [About the connector](connectors/sharepoint/about.md)
          * [Set up the connector](connectors/sharepoint/setup.md)
        * Openflow Connector for Slack

          * [About the connector](connectors/slack/about.md)
          * [Set up the connector](connectors/slack/setup.md)
        * Openflow Connector for Snowflake to Kafka

          * [About the connector](connectors/snowflake-to-kafka/about.md)
          * [Set up the connector](connectors/snowflake-to-kafka/setup.md)
        * Openflow Connector for SQL Server

          * [About the connector](connectors/sql-server/about.md)
          * [Set up the connector](connectors/sql-server/setup.md)
          * [Set up incremental replication without snapshots](connectors/sql-server/incremental-replication.md)
          * [Maintenance](connectors/sql-server/maintenance.md)
        * Openflow Connector for Workday

          * [About the connector](connectors/workday/about.md)
          * [Set up the connector](connectors/workday/setup.md)
      * [Manage Openflow](manage.md)
      * [Monitor Openflow](monitor.md)
      * [Troubleshoot Openflow](troubleshoot.md)
      * [Processors](processors/index.md)
      * [Controller services](controllers/index.md)
      * [Version history](version-history.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../tables-iceberg.md)
      - [Snowflake Open Catalog](../../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../dynamic-tables-about.md)
    - [Streams and Tasks](../../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../migrations/README.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)Data IntegrationSnowflake Openflow

# About Openflow[¶](#about-openflow "Link to this heading")

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS and Azure [Commercial regions](../../intro-regions.html#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](../../intro-regions.html#label-na-general-regions).

Snowflake Openflow is an integration service that connects any data
source and any destination with hundreds of processors supporting
structured and unstructured text, images, audio, video and sensor data.
Built on [Apache NiFi](https://nifi.apache.org/), Openflow lets you run a fully managed service in
your own cloud for complete control.

Note

The Openflow platform is currently available for deployment in customers’ own VPCs in both AWS and Snowpark Container Services.

This topic describes the key features of Openflow, its benefits,
architecture, and workflow, and use cases.

## Key features and benefits[¶](#key-features-and-benefits "Link to this heading")

Open and extensible
:   An extensible managed service that’s powered
    by Apache NiFi, enabling you to build and extend processors from any
    data source to any destination.

Unified data integration platform
:   Openflow enables data engineers to handle complex,
    bi-directional data extraction and loading through a fully managed service that can be deployed inside your
    own VPC or within your Snowflake deployment.

Enterprise-ready
:   Openflow offers out-of-the box security,
    compliance, and observability and maintainability hooks for data
    integration.

High speed ingestion of all types of data
:   One unified platform lets you handle structured and unstructured data, in both batch
    and streaming modes, from your data source to Snowflake at virtually
    any scale.

Continuous ingestion of multimodal data for AI processing
:   Nea real-time unstructured data ingestion, so you can immediately chat
    with your data coming from sources such as Sharepoint, Google Drive,
    and so on.

## Openflow deployment types[¶](#openflow-deployment-types "Link to this heading")

Openflow is supported in both the Bring Your Own Cloud (BYOC) and Snowpark Container Services (SPCS) versions.

Openflow - Snowflake Deployment
:   [![Snowflake logo in black (no text)](../../../_images/logo-snowflake-black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally Available

    Snowflake Openflow - Snowflake Deployments are available to all accounts in AWS and Azure [Commercial regions](../../intro-regions.html#label-na-general-regions).

    Openflow - Snowflake Deployment, using [Snowpark Container Services](../../../developer-guide/snowpark-container-services/overview) (SPCS),
    provides a streamlined and integrated solution for connectivity.
    Because SPCS is a self-contained service within Snowflake, it’s easy to deploy and manage.
    SPCS offers a convenient and cost-effective environment for running your data flows.
    A key advantage of Openflow - Snowflake Deployment is its native integration with Snowflake’s security model,
    which allows for seamless authentication, authorization, network security and simplified operations.

    When configuring Openflow - Snowflake Deployments, follow the process as outlined in [Setup Openflow - Snowflake Deployment](setup-openflow-spcs).

Openflow - Bring Your Own Cloud
:   [![Snowflake logo in black (no text)](../../../_images/logo-snowflake-black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally Available

    Snowflake Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](../../intro-regions.html#label-na-general-regions).

    Openflow - Bring Your Own Cloud (BYOC) provides a connectivity solution that you can use
    to connect public and private systems securely and handle sensitive data preprocessing
    locally, within the secure bounds of your organization’s cloud environment.
    BYOC refers to a deployment option where the Openflow data
    processing engine, or data plane, runs within your own cloud environment
    while Snowflake manages the overall Openflow service and control plane.

    When configuring BYOC deployments, follow the process as outlined in [Set up Openflow - BYOC](setup-openflow-byoc).

## Use cases[¶](#use-cases "Link to this heading")

Use Openflow if you want to fetch data from any source and put it
in any destination with minimal management, coupled with Snowflake’s built-in data security and governance.

Openflow use cases include:

* Ingest data from unstructured data sources, such as Google Drive and Box, and make
  it ready for chat in your AI assistants with Snowflake Cortex or use the data for your own custom processing.
* Replicate the change data capture (CDC) of database tables into Snowflake for comprehensive, centralized
  reporting.
* Ingest real-time events from streaming services, such as Apache Kafka, into Snowflake for near real-time analytics.
* Ingest data from SaaS platforms, such as LinkedIn Ads, to Snowflake for reporting, analytics, and insights.
* Create an Openflow dataflow using Snowflake and NiFi
  [processors](processors/index) and [controller services](controllers/index).

## Security[¶](#security "Link to this heading")

Openflow uses industry-leading security features that help ensure you have
the highest levels of security for your account, and users,
and all the data you store in Snowflake. Some key aspects include:

Authentication
:   * Runtimes use OAuth2 for authentication to Snowflake.

Authorization
:   * Openflow supports fine-grained roles for RBAC
    * ACCOUNTADMIN to grant privileges to be able to create deployments and runtimes

Encryption in-transit
:   * Openflow connectors support TLS protocol, using standard Snowflake clients for data ingestion.
    * All the communications between the Openflow deployments and Openflow control plane are encrypted using TLS protocol.

Secrets management (BYOC)
:   * Integration with AWS Secrets Manager or Hashicorp Vault. For more information,
      see [Encrypted Passwords in Configuration Files](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html#encrypt-config_tool).

Private link support
:   * Openflow connectors are compatible with reading and writing data to Snowflake using inbound AWS PrivateLink.

Tri-Secret Secure support
:   * Openflow connectors are compatible with [Tri-Secret Secure](../../security-encryption-tss) for writing data to Snowflake.

## Architecture[¶](#architecture "Link to this heading")

The following diagram illustrates the architecture of Openflow:

[![Openflow architecture](../../../_images/openflow-architecture.png)](../../../_images/openflow-architecture.png)

The deployment agent installs and bootstraps the Openflow deployment infrastructure in your
VPC and regularly sync container images from the Snowflake system image registry.

Openflow components include:

Deployments
:   A deployment is where your data flows execute, within individual runtimes.
    You will often have multiple runtimes to isolate different projects, teams, or for SDLC reasons, all associated with a single deployment.
    Deployments come in two types [Bring Your Own Cloud (BYOC)](about-byoc)
    and [Openflow - Snowflake](about-spcs).

Control plane
:   The control plane is a layer containing all components used to manage and observe Openflow runtimes.
    This includes the Openflow service and API, which users interact with via the Openflow canvas or through interaction with Openflow APIs.
    On Openflow - Snowflake Deployments, the Control Plane consists of Snowflake-owned
    public cloud infrastructure and services as well as the control plane application itself.

BYOC deployments
:   BYOC deployments are deployments acting as containers for runtimes that are deployed in *your* cloud environment.
    They incur charges based on their compute, infrastructure, and storage use.
    See [Openflow BYOC cost and scaling considerations](cost-byoc) for more information.

Openflow - Snowflake Deployments
:   Openflow - Snowflake Deployments are containers for runtimes and are deployed
    using a [compute pool](../../../developer-guide/snowpark-container-services/working-with-compute-pool).
    They incur utilization charges based on their uptime and usage of compute.
    See [Openflow Snowflake Deployment cost and scaling considerations](cost-spcs) for more information.

Runtime
:   Runtimes host data pipelines, with the framework providing security, simplicity, and scalability.
    You can deploy Openflow runtimes in your VPC using Openflow.
    You can deploy Openflow connectors to your runtimes, and also build completely new pipelines
    using Openflow processors and controller services.

Openflow - Snowflake Deployment Runtime
:   Openflow - Snowflake Deployment Runtimes are deployed as [Snowpark Container Services](../../../developer-guide/snowpark-container-services/overview) service
    to an Openflow - Snowflake Deployment deployment, which is represented by an underlying compute pool.
    Customers request a Runtime through the deployment, which executes a request on behalf of the user to service.
    Once created, customers access it via a web browser at the URL generated for that underlying service.

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

1. [Key features and benefits](#key-features-and-benefits)
2. [Openflow deployment types](#openflow-deployment-types)
3. [Use cases](#use-cases)
4. [Security](#security)
5. [Architecture](#architecture)

Related content

1. [About Openflow: BYOC deployments](/user-guide/data-integration/openflow/about-byoc)
2. [About Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/about-spcs)
3. [Manage Openflow](/user-guide/data-integration/openflow/manage)
4. [Monitor Openflow](/user-guide/data-integration/openflow/monitor)
5. [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors)
6. [All processors (alphabetical)](/user-guide/data-integration/openflow/processors/index)
7. [All controller services (alphabetical)](/user-guide/data-integration/openflow/controllers/index)
8. [Snowflake Openflow version history](/user-guide/data-integration/openflow/version-history)