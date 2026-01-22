---
auto_generated: true
description: Generation 2 Standard Warehouse (Gen2) is an updated version (the “next
  generation”) of the current standard virtual warehouse in Snowflake, focused on
  improving performance for analytics and data eng
last_scraped: '2026-01-14T16:57:39.799299+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-gen2
title: Snowflake generation 2 standard warehouses | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)

   * [Overview](warehouses-overview.md)
   * [Multi-cluster](warehouses-multicluster.md)
   * [Considerations](warehouses-considerations.md)
   * [Working with warehouses](warehouses-tasks.md)
   * [Next-generation standard warehouses](warehouses-gen2.md)
   * [Query Acceleration Service](query-acceleration-service.md)
   * [Monitoring load](warehouses-load-monitoring.md)
   * [Snowpark-optimized warehouses](warehouses-snowpark-optimized.md)
   * [Interactive tables and warehouses](interactive.md)
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Next-generation standard warehouses

# Snowflake generation 2 standard warehouses[¶](#snowflake-generation-2-standard-warehouses "Link to this heading")

Generation 2 Standard Warehouse (Gen2) is an updated version (the “next generation”) of the
current standard virtual warehouse in Snowflake, focused on improving performance for
analytics and data engineering workloads. Gen2 is built on top of faster underlying hardware
and intelligent software optimizations, such as enhancements to delete, update, and merge operations,
and table scan operations. With Gen2, you can expect the majority of queries finish faster, and you can do more work
at the same time. The exact details depend on your configuration and workload. Conduct tests to verify how much this feature
improves your costs, performance, or both.

You can specify the RESOURCE\_CONSTRAINT clause in the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse)
or [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) commands for standard warehouses, using one of the following values:

* STANDARD\_GEN\_1 represents Snowflake’s original, industry-leading standard virtual warehouses.
* STANDARD\_GEN\_2 represents the next generation of Snowflake’s standard virtual warehouses.

Note

Currently, the
STANDARD\_GEN\_1 and STANDARD\_GEN\_2 values aren’t available in Snowsight. You must specify them
with SQL commands.

Generation 2 standard warehouses aren’t available for warehouse sizes X5LARGE and X6LARGE.

This feature applies to standard warehouses. It doesn’t apply to Snowpark-optimized warehouses.

STANDARD\_GEN\_1 provides the same memory capacity for standard warehouses as MEMORY\_1X does
for Snowpark-optimized warehouses.

## Default value for the RESOURCE\_CONSTRAINT for standard warehouses[¶](#default-value-for-the-resource-constraint-for-standard-warehouses "Link to this heading")

For the following regions, any account associated with a new organization created after June 27th, 2025 will have standard
warehouses default to Gen2:

* AWS US West (Oregon)
* AWS EU (Frankfurt)
* Azure East US 2 (Virginia)
* Azure West Europe (Netherlands)

For all other regions where Gen2 warehouses are available, all new organizations created after July 15th, 2025 will have standard
warehouses default to Gen2. For information about region availability, see
[Region availability](#label-gen-2-standard-warehouses-region-availability).

For any regions or organizations where the preceding factors don’t apply, if you don’t specify the RESOURCE\_CONSTRAINT clause when
you create a standard warehouse, Snowflake creates a Gen1 standard warehouse.

## Changing a warehouse to or from a generation 2 warehouse[¶](#changing-a-warehouse-to-or-from-a-generation-2-warehouse "Link to this heading")

You can alter a standard warehouse and specify a different RESOURCE\_CONSTRAINT clause to change
it from generation 1 to generation 2, or from generation 2 to generation 1. You can make that change
whether the warehouse is running or suspended.

You can also switch between a Gen2 standard warehouse and a Snowpark-optimized warehouse by
changing the value of the WAREHOUSE\_TYPE and RESOURCE\_CONSTRAINT clauses. You can make that change
whether the warehouse is running or suspended.

Note

When you convert a Gen1 warehouse to Gen2 without suspending it first, existing queries that were running on Gen1 continue to run
to completion using the Gen1 compute resources. At the same time, the warehouse runs any new queries on the Gen2 compute
resources. While the existing queries are running, you are charged for both sets of compute resources. The warehouse doesn’t
automatically suspend during this period, whether or not any queries are using the Gen2 compute resources. When the existing
queries complete, the workload shifts entirely to the Gen2 compute resources. Therefore, you can maximize availability by
converting the warehouse while it’s running. Or, you can reduce costs by converting the warehouse while it’s suspended and no
queries are running.

The same consideration applies to converting between standard and Snowpark-optimized warehouses, or any other change
to the RESOURCE\_CONSTRAINT property. Existing queries will complete on the warehouse they began on and with the
RESOURCE\_CONSTRAINT that was in effect at the initialization of the query, while new queries will operate on the new warehouse
type or the new RESOURCE\_CONSTRAINT that you set.

You can see the setting for a standard warehouse in the `"resource_constraint"` column of
the SHOW WAREHOUSES output.

This setting isn’t reflected in the INFORMATION\_SCHEMA views for warehouses.

## Region availability[¶](#region-availability "Link to this heading")

Gen2 standard warehouses are available for the Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP)
cloud service providers (CSPs).

Gen2 standard warehouses are available in all [CSP regions](intro-regions),
with some exceptions. Currently, Gen2 standard warehouses *aren’t* available in these CSP regions:

* AWS EU (Zurich)
* AWS Africa (Cape Town)
* GCP Middle East Central2 (Dammam)
* Azure US Gov Virginia (FedRAMP High Plus)
* Azure US Gov Virginia

Important

If you use account replication for your warehouses, and you create any Gen2 warehouses, any secondary regions must
also have Gen2 warehouse support. Otherwise, the Gen2 warehouses might not be able to resume in the
secondary regions after a failover. Make sure to test that any Gen2 warehouses can be resumed in secondary regions.

The defaults for Snowflake standard warehouses are changing, based on the availability of Gen2 standard warehouses. Currently, the
default value of the RESOURCE\_CONSTRAINT property depends on your organization and the CSP region of your account. For more
information, see [Default value for the RESOURCE\_CONSTRAINT for standard warehouses](#label-gen-2-standard-warehouses-default-generation).

## Cost and billing for Gen2 standard warehouses[¶](#cost-and-billing-for-gen2-standard-warehouses "Link to this heading")

For general information about credit usage with Snowflake virtual warehouses,
see [Virtual warehouse credit usage](cost-understanding-compute.html#label-virtual-warehouse-credit-usage).

For information about credit consumption for Gen2 standard warehouses,
see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples[¶](#examples "Link to this heading")

The following examples show how you can specify Gen2 standard warehouses when creating a new
warehouse or altering an existing one. The examples show variations such as changing the warehouse size,
type, and memory capacity at the same time.

The following example creates a Gen2 warehouse with all other properties left as defaults. The warehouse
type is STANDARD and the size is XSMALL. Those defaults are the same for both generation 1 and generation 2
standard warehouses.

```
CREATE OR REPLACE WAREHOUSE next_generation_default_size
  RESOURCE_CONSTRAINT = STANDARD_GEN_2;
```

Copy

The following example creates a Gen2 standard warehouse with size SMALL.

```
CREATE OR REPLACE WAREHOUSE next_generation_size_small
  RESOURCE_CONSTRAINT = STANDARD_GEN_2
  WAREHOUSE_SIZE = SMALL;
```

Copy

The following example shows how to convert a generation 1 standard warehouse to generation 2. The warehouse size
remains the same, XLARGE, throughout the operation.

```
CREATE OR REPLACE WAREHOUSE old_to_new_xlarge
  WAREHOUSE_SIZE = XLARGE;

ALTER WAREHOUSE old_to_new_xlarge
  SET RESOURCE_CONSTRAINT = STANDARD_GEN_2;
```

Copy

The following example shows how to convert a Gen2 standard warehouse to Snowpark-optimized.
Snowpark-optimized warehouses currently aren’t available as Gen2 warehouses.
Because the warehouse has size XSMALL when it has the type STANDARD, we specify a RESOURCE\_CONSTRAINT value of MEMORY\_1X.
That RESOURCE\_CONSTRAINT produces a memory size that’s compatible with Snowpark-optimized warehouses of XSMALL size.

```
CREATE OR REPLACE WAREHOUSE gen2_to_snowpark_optimized
  RESOURCE_CONSTRAINT = STANDARD_GEN_2;

ALTER WAREHOUSE gen2_to_snowpark_optimized
  SET WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED' RESOURCE_CONSTRAINT = MEMORY_1X;
```

Copy

The following example shows how to convert a Snowpark-optimized warehouse to a standard Gen2 warehouse.
The Snowpark-optimized warehouse starts with size MEDIUM and a relatively large memory capacity represented by a RESOURCE\_CONSTRAINT
value of MEMORY\_16X. After the change, the warehouse is of type STANDARD, still with size MEDIUM.
However, its memory capacity is lower.
That’s because the RESOURCE\_CONSTRAINT value of STANDARD\_GEN\_2 has the same memory capacity
as a Snowpark-optimized warehouse with a resource constraint of MEMORY\_1X.

```
CREATE OR REPLACE WAREHOUSE snowpark_optimized_medium_to_gen2
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  WAREHOUSE_SIZE = MEDIUM
  RESOURCE_CONSTRAINT = MEMORY_16X;

ALTER WAREHOUSE snowpark_optimized_medium_to_gen2
  SET WAREHOUSE_TYPE = STANDARD RESOURCE_CONSTRAINT = STANDARD_GEN_2;
```

Copy

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

1. [Default value for the RESOURCE\_CONSTRAINT for standard warehouses](#default-value-for-the-resource-constraint-for-standard-warehouses)
2. [Changing a warehouse to or from a generation 2 warehouse](#changing-a-warehouse-to-or-from-a-generation-2-warehouse)
3. [Region availability](#region-availability)
4. [Cost and billing for Gen2 standard warehouses](#cost-and-billing-for-gen2-standard-warehouses)
5. [Examples](#examples)

Related content

1. [Virtual warehouses](/user-guide/warehouses)