---
auto_generated: true
description: Snowpark-optimized warehouses let you configure the available memory
  resources and CPU architecture on a single-node instance for your workloads.
last_scraped: '2026-01-14T16:57:40.893011+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized
title: Snowpark-optimized warehouses | Snowflake Documentation
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Snowpark-optimized warehouses

# Snowpark-optimized warehouses[¶](#snowpark-optimized-warehouses "Link to this heading")

Snowpark-optimized warehouses let you configure the available memory resources and CPU architecture on a single-node instance for
your workloads.

## When to use a Snowpark-optimized warehouse[¶](#when-to-use-a-snowpark-optimized-warehouse "Link to this heading")

While [Snowpark](https://www.snowflake.com/en/data-cloud/snowpark/) workloads can be run on both standard and Snowpark-optimized warehouses,
Snowpark-optimized warehouses are recommended for running Snowpark workloads such as code that has large
memory requirements or dependencies on a specific CPU architecture. Example workloads include Machine Learning (ML) training
use cases using a [stored procedure](../developer-guide/stored-procedure/stored-procedures-overview) on a single virtual warehouse
node. Snowpark workloads, utilizing [UDF](../developer-guide/udf/udf-overview) or
[UDTF](../developer-guide/udf/python/udf-python-tabular-functions), might also benefit from Snowpark-optimized warehouses.
Workloads that don’t use Snowpark might not benefit from running on Snowpark-optimized warehouses.

Note

Initial creation and resumption of a Snowpark-optimized virtual warehouse might take longer than standard warehouses.

## Configuration options for Snowpark-optimized warehouses[¶](#configuration-options-for-snowpark-optimized-warehouses "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

The 1 TB resource constraints (MEMORY\_64X and MEMORY\_64X\_x86) are available as a preview feature.
The 1 TB constraints are available only on the Amazon Web Services (AWS) cloud platform.

All other MEMORY\_\* resource constraint sizes are generally available and are available for all cloud platforms.

The default configuration for a Snowpark-optimized warehouse provides 16x memory per node compared to a standard warehouse. You can
optionally configure additional memory per node and specify CPU architecture using the `resource_constraint` property
of the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.
The following options are available:

| Memory (up to) | CPU architecture | RESOURCE\_CONSTRAINT values | Minimum warehouse size |
| --- | --- | --- | --- |
| 16GB | Default or x86 | MEMORY\_1X, MEMORY\_1X\_x86 | XSMALL |
| 256GB | Default or x86 | MEMORY\_16X, MEMORY\_16X\_x86 | M |
| 1TB | Default or x86 | MEMORY\_64X, MEMORY\_64X\_x86 | L |

## Creating a Snowpark-optimized warehouse[¶](#creating-a-snowpark-optimized-warehouse "Link to this heading")

To create a new Snowpark-optimized warehouse, you can set the warehouse type property in the following interfaces.

SQLPython

Set the WAREHOUSE\_TYPE property to `'SNOWPARK-OPTIMIZED'` when running the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command. For example:

```
CREATE OR REPLACE WAREHOUSE snowpark_opt_wh WITH
  WAREHOUSE_SIZE = 'MEDIUM'
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
```

Copy

Create a large Snowpark-optimized warehouse `so_warehouse` with 256 GB of memory by specifying the resource constraint
`MEMORY_16X_X86`:

```
CREATE WAREHOUSE so_warehouse WITH
  WAREHOUSE_SIZE = 'LARGE'
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  RESOURCE_CONSTRAINT = 'MEMORY_16X_X86';
```

Copy

Note

The default resource constraint is `MEMORY_16X`.

Set the `warehouse_type` property to `'SNOWPARK-OPTIMIZED'` when constructing a [Warehouse](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.Warehouse) object.

Then, pass this `Warehouse` object to the [WarehouseCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseCollection#snowflake.core.warehouse.WarehouseCollection.create)
method to create the warehouse in Snowflake. For example:

```
from snowflake.core import CreateMode
from snowflake.core.warehouse import Warehouse

my_wh = Warehouse(
  name="snowpark_opt_wh",
  warehouse_size="MEDIUM",
  warehouse_type="SNOWPARK-OPTIMIZED"
)
root.warehouses.create(my_wh, mode=CreateMode.or_replace)
```

Copy

Note

Resource constraints are currently not supported in the Snowflake Python APIs.

## Modifying Snowpark-optimized warehouse properties[¶](#modifying-snowpark-optimized-warehouse-properties "Link to this heading")

To modify warehouse properties including the warehouse type, you can use the following interfaces.

Note

You can change the warehouse type whether the warehouse is in the `STARTED` or `SUSPENDED` state.
If you suspend a warehouse before changing the `warehouse_type` property, execute the following operation:

SQLPython

```
ALTER WAREHOUSE snowpark_opt_wh SUSPEND;
```

Copy

```
root.warehouses["snowpark_opt_wh"].suspend()
```

Copy

SQLPython

Use the [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command to modify the memory resources and CPU architecture for Snowpark-optimized
warehouse `so_warehouse`:

```
ALTER WAREHOUSE so_warehouse SET
  RESOURCE_CONSTRAINT = 'MEMORY_1X_x86';
```

Copy

Resource constraints are currently not supported in the Snowflake Python APIs.

## Using Snowpark Python Stored Procedures to run ML training workloads[¶](#using-snowpark-python-stored-procedures-to-run-ml-training-workloads "Link to this heading")

For information on Machine Learning Models and Snowpark Python, see [Training Machine Learning Models with Snowpark Python](../developer-guide/snowpark/python/python-snowpark-training-ml).

## Billing for Snowpark-optimized warehouses[¶](#billing-for-snowpark-optimized-warehouses "Link to this heading")

For information on Snowpark-optimized warehouse credit consumption, see
`Table 1` in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](warehouses-gen2.html#label-gen-2-standard-warehouses-altering).

## Region availability[¶](#region-availability "Link to this heading")

Snowpark-optimized warehouses are available in all regions across AWS, Azure, and Google Cloud.

1 TB memory options are not currently available for the Microsoft Azure and Google Cloud Platform (GCP)
[cloud platforms](intro-cloud-platforms). On the Amazon Web Services (AWS) cloud platform,
the 1 TB memory option is also still a preview feature.

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

1. [When to use a Snowpark-optimized warehouse](#when-to-use-a-snowpark-optimized-warehouse)
2. [Configuration options for Snowpark-optimized warehouses](#configuration-options-for-snowpark-optimized-warehouses)
3. [Creating a Snowpark-optimized warehouse](#creating-a-snowpark-optimized-warehouse)
4. [Modifying Snowpark-optimized warehouse properties](#modifying-snowpark-optimized-warehouse-properties)
5. [Using Snowpark Python Stored Procedures to run ML training workloads](#using-snowpark-python-stored-procedures-to-run-ml-training-workloads)
6. [Billing for Snowpark-optimized warehouses](#billing-for-snowpark-optimized-warehouses)
7. [Region availability](#region-availability)

Related content

1. [ALTER WAREHOUSE](/user-guide/../sql-reference/sql/alter-warehouse)
2. [CREATE WAREHOUSE](/user-guide/../sql-reference/sql/create-warehouse)
3. [SHOW WAREHOUSES](/user-guide/../sql-reference/sql/show-warehouses)
4. [Snowpark API](/user-guide/../developer-guide/snowpark/index)
5. [Snowpark Developer Guide for Python](/user-guide/../developer-guide/snowpark/python/index)
6. [Training Machine Learning Models with Snowpark Python](/user-guide/../developer-guide/snowpark/python/python-snowpark-training-ml)
7. [Managing Snowflake virtual warehouses with Python](/user-guide/../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses)