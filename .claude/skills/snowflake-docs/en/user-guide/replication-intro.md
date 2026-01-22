---
auto_generated: true
description: Standard & Business Critical Feature
last_scraped: '2026-01-14T16:54:15.601662+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/replication-intro
title: Introduction to business continuity & disaster recovery | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
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

    * Replication
    * [Introduction](account-replication-intro.md)
    * [Considerations](account-replication-considerations.md)
    * [Configuration and usage](account-replication-config.md)
    * [Security integrations and network policy replication](account-replication-security-integrations.md)
    * [Apache Iceberg table replication](tables-iceberg-replication.md)
    * [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history.md)
    * [Git repository replication](account-replication-git-repositories.md)
    * [Understanding cost](account-replication-cost.md)
    * Failover
    * [Account failover](account-replication-failover-failback.md)
    * Monitoring
    * [Monitoring replication and failover](account-replication-monitor.md)
    * [Error notifications for replication and failover groups](account-replication-error-notifications.md)
    * Client Redirect
    * [Overview and usage](client-redirect.md)
    * Data Recovery
    * [Backups](backups.md)
    * [Time Travel](data-time-travel.md)
    * [Fail-safe](data-failsafe.md)
    * [Storage costs for historical data](data-cdp-storage-costs.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)Business continuity & data recovery

# Introduction to business continuity & disaster recovery[¶](#introduction-to-business-continuity-disaster-recovery "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical Feature](intro-editions)

* Database and share replication are available to all accounts.
* Replication of other account objects, failover/failback, and Client Redirect require Business Critical (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes the main use cases for replication and failover across regions and cloud platforms. The Snowflake replication
and failover/failback functionality is composed of the following features:

* [Replication and Failover/Failback](#replication-and-failover-failback)
* [Client Redirect](#client-redirect)

Collectively, these individual features are designed to support a number of different fundamental business continuity scenarios,
including:

* **Planned failovers**: For disaster recovery drills to test preparedness, and measure recovery point and time.
* **Unplanned failovers**: In the case of an outage in a region or a cloud platform, promote secondary account objects and databases
  in another region or cloud platform to serve as read-write primary objects.
* **Migration**: Move your Snowflake account to a different region or cloud platform without disrupting your business. For example, to
  maintain business continuity during mergers and acquisitions, or facilitate a change in cloud strategy.
* **Multiple readable secondaries**: Account objects and databases can be replicated to multiple accounts in
  different regions and cloud platforms, mitigating the risk of multiple region or cloud platform outages.

In addition, [Snowflake Secure Data Sharing](secure-data-sharing-across-regions-platforms) and Database Replication enable sharing data securely across regions and cloud platforms.

## Account replication and failover/failback features[¶](#account-replication-and-failover-failback-features "Link to this heading")

### Replication and failover/failback[¶](#replication-and-failover-failback "Link to this heading")

[Replication](account-replication-intro) uses two Snowflake objects,
[replication group and failover group](account-replication-intro.html#label-replication-and-failover-groups), to replicate a group of objects with point-in-time
consistency from a source account to one or more target accounts. A replication group allows customers to specify what to replicate, where
to replicate to, and how often. This means specifying which objects to replicate, to which regions or cloud platforms, at customizable
scheduled intervals. A failover group enables the replication and failover of the objects in the group.

Account objects can include warehouses, users, and roles, along with databases and shares (see [Replicated objects](account-replication-intro.html#label-replicated-objects) for the full
list of objects that can be included in a replication or failover group). Account objects can be grouped in one or multiple groups.

In the case of failover, account replication enables the failover of your account to a different region or cloud platform.
Each replication and failover group has its own replication schedule, allowing you to set the frequency for replication at different
intervals for different groups of objects. In the case of failover groups, it also enables failover of groups individually. You can choose
to failover all failover groups, or only select failover groups.

### Client Redirect[¶](#client-redirect "Link to this heading")

[Client Redirect](client-redirect) provides a *connection URL* that can be used by Snowflake clients to connect to
Snowflake. The connection URL can redirect Snowflake clients to a different Snowflake account as needed.

## Business continuity and disaster recovery[¶](#business-continuity-and-disaster-recovery "Link to this heading")

In the event of a massive outage (due to a network issue, software bug, etc.) that disrupts the cloud services in a given region, access to
Snowflake will be unavailable until the source of the outage is resolved and services are restored. To ensure continued availability and
data durability in such a scenario, replicate your critical account objects to another Snowflake account in your organization
in a different region.

With asynchronous replication, secondary replicas typically lag behind the primary objects based on the replication schedule you
configure. Secondary replica objects are at most 2x the time interval between scheduled refreshes behind the primary objects. For
example, if you choose to replicate a primary replication or failover group every 30 minutes, the secondary objects in the group
are at most 60 minutes behind the primary objects during an outage.

Depending on your business needs you could choose to:

> * Recover [reads first](#label-reads-before-writes) to let client applications read data that is 30 minutes stale.
> * Recover [writes first](#label-writes-before-reads) to reconcile the last 30 minutes of data on the new primary before
>   opening up reads from client applications.
> * Recover both reads and writes simultaneously, that is, open up reads from client applications on data that is 30 minutes stale as
>   you reconcile the last 30 minutes of data on the new primary.

### Normal status: Region is operational[¶](#normal-status-region-is-operational "Link to this heading")

**Account Object Replication:** Replicate the failover group(s) with critical account objects to one or more Snowflake accounts in
regions different from that of the account that stores the primary (source) failover group(s). Refresh the failover group(s) frequently.

### Region outage[¶](#region-outage "Link to this heading")

To prioritize reads, writes, or both at the same time, follow the steps in one of the following example scenarios.

#### Reads before writes[¶](#reads-before-writes "Link to this heading")

When an outage in a region results in full or partial loss of Snowflake availability, this path allows you to redirect Snowflake clients to read-only replicas of account objects in critical failover group(s) first for minimal downtime. Choosing to operate in read-only mode is often desirable during short-term outages.

A longer-term outage combined with the need for the latest data necessitates read-write mode.

1. **Client Redirect:** Point the connection URL used by clients to a Snowflake account that stores your read-only replica (secondary) failover group(s).
2. **Failover (When Needed):** In the event of a longer-term outage, promote the secondary failover group(s) in the Snowflake account where your connection URL is pointing to serve as read-write primary failover group(s).

#### Writes before reads[¶](#writes-before-reads "Link to this heading")

When an outage in a region results in full or partial loss of Snowflake availability, this path allows you to recover failover group(s) with critical account objects and continue to process data first. This option is preferable for account administrators who want to fail over their databases and ETL (Extract, Transform, Load) processes first, and then choose to redirect Snowflake clients only when the data is current.

1. **Failover:** Promote the secondary failover group(s) with critical account objects in a different region to serve as the primary
   failover group(s), which allows writing to the objects included in each failover group(s). Once the databases in the group(s)
   are writable, you can use your ETL processes to prioritize writes and reconcile data.

   If you use Snowflake data pipeline objects for ETL processes, you can replicate and fail over those objects. For more information,
   see [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history).

   Otherwise, configure separate connection URLs for your data ingestion pipeline and one for your clients (for example, a BI
   dashboard). After failing over the failover group, fail over the connection URL for data ingestion, and write data to the newly
   promoted primary objects. After data has been reconciled, fail over the connection URL for your clients to enable reads.
2. **Client Redirect (When Needed):** Point the connection URL used by clients to the Snowflake account that stores the new primary failover group(s).

#### Prioritize both reads and writes[¶](#prioritize-both-reads-and-writes "Link to this heading")

To prioritize both reads and writes at the same time, fail over both the client connection and secondary failover group(s) without
waiting for the secondary objects to be up to date. This enables immediate access for clients to potentially stale data while the
newly promoted databases can start reingesting data from data pipelines.

1. **Client Redirect:** Point the connection URL used by clients to a Snowflake account that stores your read-only replica (secondary)
   failover group(s).
2. **Failover:** Promote the secondary failover group(s) with critical account objects in a different region to serve as the primary
   failover group(s), which enables writing to the objects included in each failover group(s).

### Normal status: Outage is resolved[¶](#normal-status-outage-is-resolved "Link to this heading")

1. **Replication:** Refresh the failover group(s) in the Snowflake account in the region where the outage occurred.
2. **Failback:** Promote the failover group(s) in the Snowflake account where the outage occurred to again serve as the primary failover
   group(s).
3. **Client Redirect:** Point the connection URL used by clients to the Snowflake account in the region where the outage occurred.

## Account migration[¶](#account-migration "Link to this heading")

Account migration is the one-time process of migrating (or transferring) the Snowflake objects and your stored data to an account in
another region or on a different cloud platform. Typical reasons for migrating your account include a closer proximity to your user base
or a preference for a different cloud platform based on your corporate strategy or co-location with other cloud assets (e.g. a data lake).

Account object replication supports the replication of account objects such as warehouses, users, and roles, along with databases and
shares. See [Replicated objects](account-replication-intro.html#label-replicated-objects) for the complete list of replicated objects.

Note

Account object replication and failover/failback requires Business Critical (or higher). Snowflake can temporarily waive this requirement
for a one-time account migration.

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

1. [Account replication and failover/failback features](#account-replication-and-failover-failback-features)
2. [Business continuity and disaster recovery](#business-continuity-and-disaster-recovery)
3. [Account migration](#account-migration)

Related content

1. [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms)