---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:57:52.384248+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-postgres/postgres-instance-sizes
title: Snowflake Postgres Instance Sizes | Snowflake Documentation
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

[Guides](../../guides/README.md)[Snowflake Postgres](about.md)Instance sizes

# Snowflake Postgres Instance Sizes[¶](#snowflake-postgres-instance-sizes "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Snowflake Postgres offers three tiers of instances — Burstable, Standard, and Memory — to cover a variety of use cases.

In general:

* **Burstable** instances have a baseline CPU level but can temporarily burst above this baseline.
* **Standard** instances have a good balance of CPU and memory.
* **Memory-optimized** instances have a higher ratio of memory to CPU, which may improve performance for workloads with greater
  memory needs.

## Burstable[¶](#burstable "Link to this heading")

*Important notes*

* Burstable instances can be provisioned with a maximum of 100GB storage.
* Burstable instances have burstable vCPUs. Utilization in excess of the CPU baseline shown below will deplete available vCPU
  credits, leading to CPU rate limiting. This may appear as a sudden downgrade in performance with no other cause.
* Burstable instances do not support High Availability standbys.

| Name | Cores | Memory | IOPS | HA supported |
| --- | --- | --- | --- | --- |
| BURST\_XS | 2 | 1GB | 11,800 | No |
| BURST\_S | 2 | 2GB | 11,800 | No |
| BURST\_M | 2 | 4GB | 11,800 | No |

## General purpose[¶](#general-purpose "Link to this heading")

| Name | Cores | Memory | IOPS | HA supported |
| --- | --- | --- | --- | --- |
| STANDARD\_M | 1 | 4GB | 20,000 | Yes |
| STANDARD\_L | 2 | 8GB | 40,000 | Yes |
| STANDARD\_XL | 4 | 16GB | 40,000 | Yes |
| STANDARD\_2XL | 8 | 32GB | 40,000 | Yes |
| STANDARD\_4XL | 16 | 64GB | 40,000 | Yes |
| STANDARD\_8XL | 32 | 128GB | 40,000 | Yes |
| STANDARD\_12XL | 48 | 192GB | 60,000 | Yes |
| STANDARD\_24XL | 96 | 384GB | 78,000 | Yes |

Note

The STANDARD\_M instance size is not available on Microsoft Azure.

## Memory optimized[¶](#memory-optimized "Link to this heading")

| Name | Cores | Memory | IOPS | HA supported |
| --- | --- | --- | --- | --- |
| HIGHMEM\_L | 2 | 16GB | 40,000 | Yes |
| HIGHMEM\_XL | 4 | 32GB | 40,000 | Yes |
| HIGHMEM\_2XL | 8 | 64GB | 40,000 | Yes |
| HIGHMEM\_4XL | 16 | 128GB | 40,000 | Yes |
| HIGHMEM\_8XL | 32 | 256GB | 40,000 | Yes |
| HIGHMEM\_12XL | 48 | 384GB | 78,000 | Yes |
| HIGHMEM\_16XL | 64 | 512GB | 78,000 | Yes |
| HIGHMEM\_24XL | 96 | 768GB | 78,000 | Yes |
| HIGHMEM\_32XL | 128 | 1TB | 78,000 | Yes |
| HIGHMEM\_48XL | 192 | 1.5TB | 78,000 | Yes |

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

1. [Burstable](#burstable)
2. [General purpose](#general-purpose)
3. [Memory optimized](#memory-optimized)