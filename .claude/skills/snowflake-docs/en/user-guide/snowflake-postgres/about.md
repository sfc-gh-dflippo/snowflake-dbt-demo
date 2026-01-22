---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:54:24.463842+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-postgres/about
title: Snowflake Postgres | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](about.md)

    * [Creating instances](postgres-create-instance.md)
    * [Connecting](connecting-to-snowflakepg.md)
    * [Managing instances](managing-instances.md)
    * Monitoring
    * [Evaluate cost](postgres-cost.md)
    * [Insights](insights.md)
    * [Logging](postgres-logging.md)
    * Security and networking
    * [Networking](postgres-network.md)
    * [Tri-Secret Secure](postgres-tss.md)
    * Reference
    * [Instance sizes](postgres-instance-sizes.md)
    * [Extensions](postgres-extensions.md)
    * [Server settings](postgres-server-settings.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)Snowflake Postgres

# Snowflake Postgres[¶](#snowflake-postgres "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

## About Snowflake Postgres[¶](#about-snowflake-postgres "Link to this heading")

Snowflake Postgres lets you create, manage, and use Postgres instances directly from Snowflake. Each instance runs a Postgres
database server on a dedicated virtual machine managed by Snowflake. You connect directly to your instances using any Postgres
client. Snowflake Postgres brings the reliable and trusted transactional database capabilities of Postgres to the Snowflake data
platform.

## About Postgres[¶](#about-postgres "Link to this heading")

PostgreSQL (also referred to as Postgres) is a mature, open-source relational database management system that has been actively
developed for more than 30 years. As a general-purpose transactional database, Postgres is designed for operational applications that
require highly-concurrent read/write operations, and low-latency data processing. Postgres offers a wide array of data types, including
JSONB, and sophisticated indexing capabilities. Postgres is increasingly becoming the database of choice for a wide range of use cases,
and is supported by an ecosystem of community-sponsored developer tools and extensions that offer enhanced capabilities. With
its proven reliability and performance, and active developer community, Postgres is a great addition to the Snowflake AI Data Cloud
platform that supports an expanded set of customer workloads.

## Architecture[¶](#architecture "Link to this heading")

Postgres is a mature, battle-tested database known for its reliability and performance, but it follows a more traditional architectural
model than the rest of the Snowflake platform. To bring Postgres into Snowflake, we designed an approach that preserves its operational
strengths while integrating it with Snowflake’s security, management, and connectivity capabilities.

Snowflake Postgres provisions a dedicated Postgres instance with attached disks to deliver best-in-class transactional performance. Each
Postgres instance runs in a fully isolated private network and supports private connectivity via firewall rules or Private Link. Snowflake
Postgres also offers built-in connection pooling via PgBouncer to support high-concurrency application workloads.

Snowflake Postgres is fully compatible with existing Postgres tooling and workloads, enabling you to lift-and-shift applications to
Snowflake with no code changes, and use everything that works with your Postgres instances today, including ORMs and all supported SQL
clients.

## Regional availability[¶](#regional-availability "Link to this heading")

Snowflake Postgres is available in the following [regions](../intro-regions).

| Cloud region | Cloud region ID |
| --- | --- |
| **Amazon Web Services (AWS)** |  |
| US East (N. Virginia) | us-east-1 |
| US West (Oregon) | us-west-2 |
| Europe (Ireland) | eu-west-1 |
| **Microsoft Azure** |  |
| East US 2 (Virginia) | eastus2 |
| West US 2 (Washington) | westus2 |
| North Europe (Ireland) | northeurope |

## Postgres major versions[¶](#postgres-major-versions "Link to this heading")

Postgres major versions 16-18 are currently available. We will automatically use the latest minor version when creating a
new instance.

## When to use Postgres[¶](#when-to-use-postgres "Link to this heading")

Choose Postgres when you need a high-throughput, high-concurrency operational database, you have a use case that can benefit from
specific Postgres capabilities, or have an existing Postgres application.

## Customer Configurable Security Controls[¶](#customer-configurable-security-controls "Link to this heading")

Customers are responsible for managing the following controls to ensure a level of security appropriate to the particular content of their Postgres instances:

* Securing, keeping confidential, and rotating Postgres instance credentials, including passwords and connection strings.
* Maintaining appropriate password uniqueness, length, complexity, and expiration; and
* Configuring user and role-based access controls, including scope and duration of user access.

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

1. [About Snowflake Postgres](#about-snowflake-postgres)
2. [About Postgres](#about-postgres)
3. [Architecture](#architecture)
4. [Regional availability](#regional-availability)
5. [Postgres major versions](#postgres-major-versions)
6. [When to use Postgres](#when-to-use-postgres)
7. [Customer Configurable Security Controls](#customer-configurable-security-controls)