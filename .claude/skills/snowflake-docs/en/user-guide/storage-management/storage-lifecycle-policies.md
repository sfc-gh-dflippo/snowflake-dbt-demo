---
auto_generated: true
description: Note
last_scraped: '2026-01-14T16:54:22.292458+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/storage-management/storage-lifecycle-policies
title: Storage lifecycle policies | Snowflake Documentation
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
12. [Storage Lifecycle Policies](storage-lifecycle-policies.md)

    * [Billing](storage-lifecycle-policies-billing.md)
    * [Creating and Managing Policies](storage-lifecycle-policies-create-manage.md)
    * [Retrieving Archived Data](storage-lifecycle-policies-retrieving-archived-data.md)
    * [Monitoring](storage-lifecycle-policies-monitoring.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)Storage Lifecycle Policies

# Storage lifecycle policies[¶](#storage-lifecycle-policies "Link to this heading")

Note

[Storage lifecycle policies](#) aren’t currently available in government regions.

A *storage lifecycle policy* is a schema-level object that automatically manages the data lifecycle for standard Snowflake tables.
Use these policies to archive or expire specific table rows that are based on conditions that you define, such as data age or other criteria.
Snowflake automatically executes these policies daily by using shared compute resources.

## How storage lifecycle policies work[¶](#how-storage-lifecycle-policies-work "Link to this heading")

[![Overview of the storage lifecycle policy workflow](../../_images/storage-lifecycle-policy-workflow.svg)](../../_images/storage-lifecycle-policy-workflow.svg)

To get started with storage lifecycle policies, complete the following steps:

1. [Create a policy](storage-lifecycle-policies-create-manage.html#label-slp-create) with an expression that identifies rows to archive or expire.
2. [Attach the policy to one or more tables](storage-lifecycle-policies-create-manage.html#label-slp-attach-to-table).

After you attach a storage lifecycle policy to a table, Snowflake waits approximately 24 hours before running the policy for the first time.
Following this initial delay, Snowflake automatically runs the policy daily by using shared compute resources to identify
and process rows that meet your defined conditions.

When the policy runs, it checks each row against your expression, and then either archives the data to
[COOL or COLD storage](#label-slp-archive-tiers) or expires the data, which deletes it permanently. You can retrieve archived data by using the
[CREATE TABLE … FROM ARCHIVE OF](../../sql-reference/sql/create-table.html#label-create-table-from-archive-of-syntax) command before expiration occurs. Snowflake waits until the
specified archive period elapses before expiring the data from archive storage.

[![Overview of the storage lifecycle policy archive-to-expiration flow.](../../_images/storage-lifecycle-policy-archive-flow.svg)](../../_images/storage-lifecycle-policy-archive-flow.svg)

### Key capabilities[¶](#key-capabilities "Link to this heading")

Storage lifecycle policies provide the following benefits for managing your Snowflake data.

Reduced storage costs
:   Storage lifecycle policies help optimize costs by automatically moving older data to
    more cost-effective [archival tiers](#label-slp-archive-tiers).
    For data that must be retained long-term but
    accessed infrequently, archival storage can significantly reduce storage costs compared
    to standard storage tiers.

Regulatory compliance
:   Automatically meet compliance requirements by configuring policies to archive or expire data according to regulatory standards.
    You can archive data for a specific time before expiration, or expire it directly without archiving.
    This ensures that your data management follows your organization’s governance standards.

Simple data management
:   Storage lifecycle policies eliminate manual data management tasks by automatically executing
    archival and expiration rules. For more information, see [Monitor storage lifecycle policies](storage-lifecycle-policies-monitoring).

Flexible data retrieval
:   [Retrieve archived data](storage-lifecycle-policies-retrieving-archived-data)
    with precision by creating a new table that contains only the
    rows you need. Use a simple command with a WHERE clause to specify exactly which
    archived data to restore.

## Archive storage tiers[¶](#archive-storage-tiers "Link to this heading")

Snowflake supports archiving data in the following storage tiers:

| Archive tier | Description |
| --- | --- |
| COOL | Offers fast retrieval time, so data is readily available. The minimum archival period is 90 days. |
| COLD | Offers greater cost savings than the COOL tier; it is four times less expensive. The minimum archival period is 180 days. Compared to the COOL tier, COLD has a longer data retrieval time, which is up to 48 hours. Data retrieval operations from the COLD storage tier support a maximum of 1 million files per restore operation. |

### Choosing an archive tier[¶](#choosing-an-archive-tier "Link to this heading")

When you select an archive tier, consider the following factors:

* **Archiving costs**: The one-time cost to archive data is the same for both tiers.
* **Storage costs**: COLD tier storage is less expensive than COOL tier storage.
* **Retrieval costs**: COLD tier data retrieval is less expensive than COOL tier retrieval.
* **Retrieval time**: The COOL storage tier offers instant data retrieval, whereas COLD tier retrieval can take up to 48 hours.

Important

If you attach an archival storage policy to a table, the table is permanently assigned to the specified archive tier for its lifetime. You can’t change the archive tier by applying a new policy. For example, you can’t specify a policy created with a COOL archive tier in ALTER TABLE…DROP STORAGE LIFECYCLE POLICY and then subsequently alter the table to add a policy created with a COLD archive tier. To alter the archive tier for a table, contact Snowflake Support to request deletion of the currently archived data. For additional considerations, see [Archival storage policies](#label-slp-archive-limitations).

For detailed pricing information, see
tables 3(e) and 4(f) in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

For more information about archiving data, see [Create a storage lifecycle policy](storage-lifecycle-policies-create-manage.html#label-slp-create)
and [Archive storage considerations](#label-slp-archive-limitations).

## Considerations[¶](#considerations "Link to this heading")

Consider the following information when you work with storage lifecycle policies.

### Cloud provider support[¶](#cloud-provider-support "Link to this heading")

* **Expiration policies**: Supported for accounts hosted on all cloud providers (Amazon Web Services (AWS), Microsoft Azure, and Google Cloud).
* **Archival policies**: Currently available only for accounts hosted on AWS.

### Supported tables and features[¶](#supported-tables-and-features "Link to this heading")

* **Supported tables**: Storage lifecycle policies are supported for standard Snowflake tables.
  To evaluate and apply storage lifecycle policy expressions, Snowflake internally and temporarily bypasses any governance policies on a table.
* **Replication**:

  + Snowflake replicates storage lifecycle policies and their associations with tables to target accounts, but doesn’t run the policies.
  + Snowflake doesn’t replicate archived data in the COOL or COLD tiers. After failover,
    archived data in your source account isn’t available in the target account.
  + After failover to a target account, Snowflake pauses storage lifecycle policy execution in the original primary account. After failback to the original primary account, Snowflake resumes policy execution.
  + Snowflake never automatically runs secondary storage lifecycle policies on secondary tables, even after failover. However, you can use secondary policies in a target account by attaching them to *new* tables. For those new tables, Snowflake runs the policies.
* **Cloning**: Snowflake doesn’t automatically apply storage lifecycle policies to cloned tables. If you apply a storage lifecycle policy to
  a table in a clone group, Snowflake archives rows only from that specific table. The policy doesn’t affect clones. This creates copies of the data in both the standard and archive
  storage tiers, and you pay for storage in each tier. For cost information, see [Billing for storage lifecycle policies](storage-lifecycle-policies-billing).
* **Unsupported features**

  Storage lifecycle policies aren’t supported for the following features:

  + All object types other than regular Snowflake tables and dynamic tables.
  + Write once read many (WORM) snapshots, which are immutable snapshots that can’t be modified after creation.
  + Both provider and consumer tables shared through Snowflake data sharing.
  + Native Apps.
  + User-defined functions (UDFs) with external access and external functions.
  + Python, Java, or Scala UDFs.

### Policy behavior and execution[¶](#policy-behavior-and-execution "Link to this heading")

Storage lifecycle policies use performance guidelines that are similar to
[guidelines for row-level access policies](../security-row-intro.html#label-security-row-performance),
and operate automatically with the following characteristics:

* When you attach a storage lifecycle policy to a table, Snowflake waits approximately 24 hours before running it for the first time.
* Snowflake runs storage lifecycle policies every day by using shared compute resources. For information about cost
  for storage lifecycle policies, see
  [Billing for storage lifecycle policies](storage-lifecycle-policies-billing).
* To prevent excessively long archive or expiration runs, Snowflake processes large data operations incrementally in smaller chunks.
  A large operation might not complete in one daily run and might instead complete across multiple daily runs.
* When a storage lifecycle policy is running on a table, Snowflake locks UPDATE, DELETE, and MERGE operations.
  You can still perform INSERT and COPY operations during this time. For more information,
  see [Resource locking](../../sql-reference/transactions.html#label-txn-locking).

### Archival storage policies[¶](#archival-storage-policies "Link to this heading")

Consider the following information when you work with tables that have an archival storage lifecycle policy attached:

* **Accessing archived data**: After Snowflake archives rows, you can’t query them directly. To access them, use
  the [CREATE TABLE … FROM ARCHIVE OF](../../sql-reference/sql/create-table.html#label-create-table-from-archive-of-syntax) command
  to create a new table with a copy of the archived data. For more information, see
  [Retrieving archived data](storage-lifecycle-policies-retrieving-archived-data).
* **Security**: You can use Tri-Secret Secure ([TSS](../security-encryption-tss)) to protect archived data with regular key rotation.
* **Rekeying**: Snowflake doesn’t rekey archived data. If you suspect a key compromise, perform the following steps:

  1. Retrieve the archived data to a new table with the [CREATE TABLE … FROM ARCHIVE OF](../../sql-reference/sql/create-table.html#label-create-table-from-archive-of-syntax)
     command.
  2. Archive data in the new table when needed.

     Each table has its own encryption key, so the new table effectively uses a new key.
  3. Drop the archive of the original table in which the keys were compromised.
* **Archive tier limitations**:

  + You can’t change the [archive tier](#label-slp-archive-tiers) for a policy from COOL to COLD or from COLD to COOL. Create a new policy instead. For instructions, see [Recreate a storage lifecycle policy](storage-lifecycle-policies-create-manage.html#label-slp-recreate).
  + A table can only use one archive tier *for its lifetime*. For example, you can’t attach a policy that uses a COLD archive tier to a table that already uses a COOL archive tier or vice versa. In addition, you can’t alter a table to drop a policy and then subsequently attach a policy that specifies a different archive tier.
* **Removing policies**: When you remove a policy from a table, the archived data remains in archive storage and can still be retrieved.
* **Dropping or truncating a table**:

  + Truncating a table doesn’t affect archived data for that table. You can still retrieve data from archive storage after truncating the table.
  + When you use [UNDROP TABLE](../../sql-reference/sql/undrop-table) to restore a table in an applicable
    [Time Travel data retention period](../data-time-travel.html#label-time-travel-data-retention-period), Snowflake also restores any data in archive storage.
  + When a table is within the [Fail-safe](../data-failsafe) period, the data in archive storage might be recoverable
    by using Fail-safe data recovery steps through Snowflake Support.
  + Table data in archive storage that you delete before the ARCHIVE\_FOR\_DAYS period has elapsed is subject to storage cost.
    For more information, see [Minimum storage duration charges](storage-lifecycle-policies-billing.html#label-slp-billing-penalty-bytes).

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

1. [How storage lifecycle policies work](#how-storage-lifecycle-policies-work)
2. [Key capabilities](#key-capabilities)
3. [Archive storage tiers](#archive-storage-tiers)
4. [Choosing an archive tier](#choosing-an-archive-tier)
5. [Considerations](#considerations)
6. [Cloud provider support](#cloud-provider-support)
7. [Supported tables and features](#supported-tables-and-features)
8. [Policy behavior and execution](#policy-behavior-and-execution)
9. [Archival storage policies](#archival-storage-policies)

Related content

1. [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing)
2. [Create and manage storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-create-manage)
3. [Retrieve archived data](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data)
4. [Monitor storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-monitoring)