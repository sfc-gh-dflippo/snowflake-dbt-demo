---
auto_generated: true
description: Horizon Catalog is the universal catalog for your entire data estate.
  It provides context and governance for AI, enables any architecture across clouds
  and regions, works with any engine and data form
last_scraped: '2026-01-14T16:54:18.638902+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-horizon
title: Snowflake Horizon Catalog | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)

   * [Use Snowsight to generate object descriptions](ui-snowsight-cortex-descriptions.md)
   * [Use SQL to generate object descriptions](sql-cortex-descriptions.md)
   * [Contacts](contacts-using.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)Snowflake Horizon Catalog

# Snowflake Horizon Catalog[¶](#snowflake-horizon-catalog "Link to this heading")

Horizon Catalog is the universal catalog for your entire data estate. It provides context and governance for AI, enables any architecture
across clouds and regions, works with any engine and data format — and has zero risk of vendor lock-in.

## Context for AI[¶](#context-for-ai "Link to this heading")

[Snowflake Intelligence](snowflake-cortex/snowflake-intelligence) empowers users across the organization to engage with
data intuitively by allowing them to ask questions and immediately obtain answers, insights, and visualizations. Snowflake Intelligence brings all your
structured and unstructured data together and uses helpful [AI agents](snowflake-cortex/cortex-agents) that understand
your business through your [semantic views](views-semantic/overview) and search services. Powered by [Cortex AI Functions](snowflake-cortex/aisql), [Cortex Analyst](snowflake-cortex/cortex-analyst), and [Cortex Search](snowflake-cortex/cortex-search/cortex-search-overview), Snowflake Intelligence delivers clear, trustworthy insights while keeping everything secure and
fully governed inside Snowflake. With easy access to [leading models](snowflake-cortex/snowflake-intelligence.html#label-snowflake-intelligence-models) and cross-region inference,
every user can explore, discover, and act with confidence.

## Easy and safe data discovery across clouds[¶](#easy-and-safe-data-discovery-across-clouds "Link to this heading")

Horizon Catalog gives users one place to find all data resources with consistent metadata about Snowflake data, Apache Iceberg™ data, and
external relational sources and BI tools. Horizon Catalog expands visibility through
[Internal Marketplace](collaboration/listings/organizational/org-listing-about) listings so teams can discover governed
data products without copying data. Horizon Catalog enforces [access control](security-access-control-overview), protects
sensitive fields with [dynamic data masking](security-column-intro), applies
[row access policies](security-row-intro), and [identifies sensitive data](classify-intro) through data
classification.

## Enterprise-grade security and governance[¶](#enterprise-grade-security-and-governance "Link to this heading")

Horizon Catalog makes it easy to keep data safe, consistent, and well understood across your entire organization. It applies
[sensitive data classification](classify-intro), [retention](tables-iceberg-metadata), and
[data access policies](security-access-control-overview) the same way everywhere, giving every engine a shared view of your
metadata, [lineage](ui-snowsight-lineage), and rules. With [access history](ui-snowsight-lineage) and
[Time Travel](data-time-travel), teams can confidently review past activity and data states. Governance flows naturally to
external storage, Iceberg tables, and the [Snowflake Marketplace](../collaboration/collaboration-marketplace-about), so shared data
products always carry their tags and permissions wherever they go.

## Interoperability without vendor lock-in[¶](#interoperability-without-vendor-lock-in "Link to this heading")

Horizon Catalog connects all compute engines and formats through one governed environment. It presents consistent metadata and permissions
to Snowflake, Spark, and engines that read [Apache Iceberg](tables-iceberg). Horizon Catalog governs data inside Snowflake and in
external storage through [external tables](tables-external-intro) and Iceberg tables. It carries governance into the
Marketplace by [sharing](../guides-overview-sharing) data products through
[internal exchanges](collaboration/listings/organizational/org-listing-about) while preserving tags and access rules.
Horizon Catalog ensures every engine sees the same definitions, lineage, and policy behavior.

## A central spot for managing business continuity[¶](#a-central-spot-for-managing-business-continuity "Link to this heading")

Within Horizon, you [manage](account-replication-failover-failback) primary and secondary environments with ease, keeping
them consistent through database and account replication so your data, policies, and configurations stay aligned across every region and
account.

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

1. [Context for AI](#context-for-ai)
2. [Easy and safe data discovery across clouds](#easy-and-safe-data-discovery-across-clouds)
3. [Enterprise-grade security and governance](#enterprise-grade-security-and-governance)
4. [Interoperability without vendor lock-in](#interoperability-without-vendor-lock-in)
5. [A central spot for managing business continuity](#a-central-spot-for-managing-business-continuity)