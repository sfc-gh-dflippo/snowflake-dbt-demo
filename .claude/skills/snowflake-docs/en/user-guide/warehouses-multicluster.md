---
auto_generated: true
description: Enterprise Edition Feature
last_scraped: '2026-01-14T16:57:41.971228+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-multicluster
title: Multi-cluster warehouses | Snowflake Documentation
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Multi-cluster

# Multi-cluster warehouses[¶](#multi-cluster-warehouses "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition Feature](intro-editions)

To inquire about upgrading to Enterprise Edition (or higher), please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Multi-cluster warehouses enable you to scale compute resources to manage your user and query concurrency needs as they change, such as during
peak and off hours.

## What is a multi-cluster warehouse?[¶](#what-is-a-multi-cluster-warehouse "Link to this heading")

By default, a virtual warehouse consists of a single cluster of compute resources available to the
warehouse for executing queries. As queries are submitted to a warehouse, the warehouse allocates resources to each query and begins
executing the queries. If sufficient resources are not available to execute all the queries submitted to the warehouse, Snowflake queues the
additional queries until the necessary resources become available.

With multi-cluster warehouses, Snowflake supports allocating, either statically or dynamically, additional clusters to make a larger pool
of compute resources available. A multi-cluster warehouse is defined by specifying the following properties:

* Maximum number of clusters, greater than 1. The highest value you can specify depends on the warehouse size.
  For the upper limit on the number of clusters for each warehouse size,
  see [Upper limit on number of clusters for a multi-cluster warehouse](#label-max-cluster-size-limit-per-warehouse-size) (in this topic).
* Minimum number of clusters, equal to or less than the maximum.

Additionally, multi-cluster warehouses support all the same properties and actions as single-cluster warehouses, including:

* Specifying a warehouse size.
* Resizing a warehouse at any time.
* Auto-suspending a running warehouse due to inactivity; note that this does not apply to individual clusters, but rather the entire
  multi-cluster warehouse.
* Auto-resuming a suspended warehouse when new queries are submitted.

### Upper limit on number of clusters for a multi-cluster warehouse[¶](#upper-limit-on-number-of-clusters-for-a-multi-cluster-warehouse "Link to this heading")

The maximum number of clusters for a multi-cluster warehouse depends on the warehouse size. Larger warehouse sizes have lower limits on the number of clusters. The following table shows the maximum number of clusters for each warehouse size:

| Warehouse size | Allowed maximum cluster count | Default maximum cluster count |
| --- | --- | --- |
| XSMALL | 300 | 10 |
| SMALL | 300 | 10 |
| MEDIUM | 300 | 10 |
| LARGE | 160 | 10 |
| XLARGE | 80 | 10 |
| 2XLARGE | 40 | 10 |
| 3XLARGE | 20 | 10 |
| 4XLARGE | 10 | 10 |
| 5XLARGE | 10 | 10 |
| 6XLARGE | 10 | 10 |

Note

Currently, Snowsight supports updating MAX\_CLUSTER\_COUNT to a maximum of 10 clusters.
To specify a MAX\_CLUSTER\_COUNT larger than 10, use the CREATE WAREHOUSE or ALTER WAREHOUSE command in SQL.

### Maximized vs. auto-scale[¶](#maximized-vs-auto-scale "Link to this heading")

You can choose to run a multi-cluster warehouse in either of the following modes:

Maximized:
:   This mode is enabled by specifying the same value for both maximum and minimum number of clusters (note that the
    specified value must be larger than 1). In this mode, when the warehouse is started, Snowflake starts all the clusters so
    that maximum resources are available while the warehouse is running.

    This mode is effective for statically controlling the available compute resources, particularly if you have large numbers of concurrent
    user sessions and/or queries and the numbers do not fluctuate significantly.

Auto-scale:
:   This mode is enabled by specifying different values for maximum and minimum number of clusters. In this mode,
    Snowflake starts and stops clusters as needed to dynamically manage the load on the warehouse:

    * As the number of concurrent user sessions and/or queries for the warehouse increases, and queries start to queue due to
      insufficient resources, Snowflake automatically starts additional clusters, up to the maximum number defined for the warehouse.
    * Similarly, as the load on the warehouse decreases, Snowflake automatically shuts down clusters to reduce the number of
      running clusters and, correspondingly, the number of credits used by the warehouse.

    To help control the usage of credits in Auto-scale mode, Snowflake provides a property, SCALING\_POLICY, that determines the scaling policy
    to use when automatically starting or shutting down additional clusters. For more information, see [Setting the scaling policy for a multi-cluster warehouse](#label-mcw-scaling-policies) (in
    this topic).

To create a multi-cluster warehouse, see [Creating a multi-cluster warehouse](#label-multi-cluster-create) (in this topic).

* For auto-scale mode, the maximum number of clusters must be *greater* than the minimum number of clusters.
* For maximized mode, the maximum number of clusters must be *equal* to the minimum number of clusters.

Tip

When determining the maximum and minimum number of clusters to use for a multi-cluster warehouse, start with Auto-scale mode and start
small (for example, maximum = 2 or 3, minimum = 1). As you track how your warehouse load fluctuates over time, you can increase the maximum and
minimum number of clusters until you determine the numbers that best support the upper and lower boundaries of your user/query concurrency.

### Multi-cluster size and credit usage[¶](#multi-cluster-size-and-credit-usage "Link to this heading")

The amount of compute resources in each cluster is determined by the warehouse size:

* The total number of clusters for the multi-cluster warehouse is calculated by multiplying the warehouse size by the maximum number of
  clusters. This also indicates the maximum number of credits consumed by the warehouse per full hour of usage (i.e. if
  all clusters run during the hour).

  For example, the maximum number of credits consumed per hour for a Medium-size multi-cluster warehouse with 3 clusters is 12 credits.
* If a multi-cluster warehouse is resized, the new size applies to all the clusters for the warehouse, including
  clusters that are currently running and any clusters that are started after the multi-cluster warehouse is resized.

The actual number of credits consumed per hour depends on the number of clusters running during each hour that the warehouse
is running. For more details, see [Examples of multi-cluster credit usage](#label-multi-cluster-credit-usage-examples) (in this topic).

Tip

If you use Query Acceleration Service (QAS) for a multi-cluster warehouse, consider adjusting the QAS scale
factor higher than for a single-cluster warehouse. That helps to apply the QAS optimizations across all the
clusters of the warehouse.
For more information, see [Adjusting the scale factor](query-acceleration-service.html#label-query-acceleration-scale-factor).

### Benefits of multi-cluster warehouses[¶](#benefits-of-multi-cluster-warehouses "Link to this heading")

With a standard, single-cluster warehouse, if your user/query load increases to the point where you need more compute resources:

1. You must either increase the size of the warehouse or start additional warehouses and explicitly redirect the additional users/queries to
   these warehouses.
2. Then, when the resources are no longer needed, to conserve credits, you must manually downsize the larger warehouse or suspend the additional
   warehouses.

In contrast, a multi-cluster warehouse enables larger numbers of users to connect to the same size warehouse. In addition:

* In Auto-scale mode, a multi-cluster warehouse eliminates the need for resizing the warehouse or starting and stopping additional
  warehouses to handle fluctuating workloads. Snowflake automatically starts and stops additional clusters as needed.
* In Maximized mode, you can control the capacity of the multi-cluster warehouse by increasing or decreasing the number of clusters as
  needed.

Tip

Multi-cluster warehouses are best utilized for scaling resources to improve concurrency for users/queries. They are not as beneficial for
improving the performance of slow-running queries or data loading. For these types of operations, resizing the warehouse provides
more benefits.

## Examples of multi-cluster credit usage[¶](#examples-of-multi-cluster-credit-usage "Link to this heading")

The following four examples illustrate credit usage for a multi-cluster warehouse. Refer to [Virtual warehouse credit usage](cost-understanding-compute.html#label-virtual-warehouse-credit-usage) for
the number of credits billed per full hour by warehouse size.

Note

For the sake of simplicity, all these examples depict credit usage in increments of 1 hour, 30 minutes, and 15 minutes. In a real-world
scenario, with per-second billing, the actual credit usage would contain fractional amounts, based on the number of seconds that each
cluster runs.

### Example 1: Maximized (2 Hours)[¶](#example-1-maximized-2-hours "Link to this heading")

In this example, a Medium-size Standard warehouse with 3 clusters runs in Maximized mode for 2 hours:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits** |
| 1st Hour | 4 | 4 | 4 | **12** |
| 2nd Hour | 4 | 4 | 4 | **12** |
| **Total Credits** | **8** | **8** | **8** | **24** |

### Example 2: Auto-scale (2 Hours)[¶](#example-2-auto-scale-2-hours "Link to this heading")

In this example, a Medium-size Standard warehouse with 3 clusters runs in Auto-scale mode for 2 hours:

* Cluster 1 runs continuously.
* Cluster 2 runs continuously for the 2nd hour only.
* Cluster 3 runs for 30 minutes during the 2nd hour.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits** |
| 1st Hour | 4 | 0 | 0 | **4** |
| 2nd Hour | 4 | 4 | 2 | **10** |
| **Total Credits** | **8** | **4** | **2** | **14** |

### Example 3: Auto-scale (3 Hours)[¶](#example-3-auto-scale-3-hours "Link to this heading")

In this example, a Medium-size Standard warehouse with 3 clusters runs in Auto-scale mode for 3 hours:

* Cluster 1 runs continuously.
* Cluster 2 runs continuously for the entire 2nd hour and 30 minutes in the 3rd hour.
* Cluster 3 runs for 30 minutes in the 3rd hour.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits** |
| 1st Hour | 4 | 0 | 0 | **4** |
| 2nd Hour | 4 | 4 | 0 | **8** |
| 3rd Hour | 4 | 2 | 2 | **8** |
| **Total Credits** | **12** | **6** | **2** | **20** |

### Example 4: Auto-scale (3 Hours) with resize[¶](#example-4-auto-scale-3-hours-with-resize "Link to this heading")

In this example, the same warehouse from example 3 runs in Auto-scale mode for 3 hours with a resize from Medium to Large:

* Cluster 1 runs continuously.
* Cluster 2 runs continuously for the 2nd and 3rd hours.
* Warehouse is resized from Medium to Large at 1:30 hours.
* Cluster 3 runs for 15 minutes in the 3rd hour.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits** |
| 1st Hour | 4 | 0 | 0 | **4** |
| 2nd Hour | 4+2 | 4+2 | 0 | **12** |
| 3rd Hour | 8 | 8 | 2 | **18** |
| **Total Credits** | **18** | **14** | **2** | **34** |

## Creating a multi-cluster warehouse[¶](#creating-a-multi-cluster-warehouse "Link to this heading")

You can create a multi-cluster warehouse in [Snowsight](ui-snowsight-gs.html#label-snowsight-getting-started-sign-in) or by using SQL:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses » + Warehouse
>
>     1. Expand Advanced Options.
>     2. Select the Multi-cluster Warehouse checkbox.
>     3. In the Max Clusters field, select a value greater than 1.
>
>        Note
>
>        Currently, the highest value you can choose in Snowsight is 10.
>        The maximum sizes shown in [Upper limit on number of clusters for a multi-cluster warehouse](#label-max-cluster-size-limit-per-warehouse-size)
>        apply to the CREATE WAREHOUSE and ALTER WAREHOUSE commands in SQL only.
>     4. In the Min Clusters field, optionally select a value greater than 1.
>     5. Enter other information for the warehouse, as needed, and click Create Warehouse.
>
> SQL:
> :   Execute a [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command with:
>
>     * `MAX_CLUSTER_COUNT` set to a value greater than `1`. For the highest value
>       you can specify depending on the warehouse size, see
>       [Upper limit on number of clusters for a multi-cluster warehouse](#label-max-cluster-size-limit-per-warehouse-size) (in this topic).
>     * `MIN_CLUSTER_COUNT` (optionally) set to a value greater than `1`.

To view information about the multi-cluster warehouses you create:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses.
>
>     The Clusters column displays the minimum and maximum clusters for each warehouse, as well as the number of
>     clusters that are currently running if the warehouse is started. You can sort by the Clusters column in
>     descending order to list the multi-cluster warehouses at the top.
>
> SQL:
> :   Execute a [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses) command.
>
>     The output includes three columns (`min_cluster_count`, `max_cluster_count`, `started_clusters`)
>     that display the same information provided in the Clusters column in the web interface.
>
>     Tip
>
>     If the SHOW WAREHOUSES output is difficult to read because it includes so many columns, you can
>     use the [pipe operator](../sql-reference/operators-flow) (`->>`) to show just the columns you want,
>     along with any other clauses for filtering and sorting. Use a query that is similar to the following example,
>     and adjust it to suit your needs. The column names are quoted because they’re case-sensitive in
>     the SHOW WAREHOUSES output:
>
>     ```
>     SHOW WAREHOUSES
>       ->> SELECT "name", "state", "size", "max_cluster_count", "started_clusters", "type"
>             FROM $1
>             WHERE "state" IN ('STARTED','SUSPENDED')
>             ORDER BY "type" DESC, "name";
>     ```
>
>     Copy

All other tasks for multi-cluster warehouses (except for the remaining tasks described in this topic) are identical to single-cluster
[warehouse tasks](warehouses-tasks).

## Setting the scaling policy for a multi-cluster warehouse[¶](#setting-the-scaling-policy-for-a-multi-cluster-warehouse "Link to this heading")

To help control the credits consumed by a multi-cluster warehouse running in Auto-scale mode, Snowflake provides scaling policies.
Snowflake uses the scaling policies to determine how to adjust the capacity of your multi-cluster warehouse
by starting or shutting down individual clusters while the warehouse is running. You can specify a scaling policy
to make Snowflake prioritize responsiveness and throughput for the queries in that warehouse, or to minimize costs
for that warehouse.

The scaling policy for a multi-cluster warehouse only applies if it is running in Auto-scale mode.
In Maximized mode, all clusters run concurrently, so there is no need to start or shut down individual clusters.

Snowflake supports the following scaling policies:

| Policy | Description | A new cluster starts… | An idle or lightly loaded cluster shuts down… |
| --- | --- | --- | --- |
| Standard (default) | Prevents/minimizes queuing by favoring starting additional clusters over conserving credits. | When a query is queued, or if Snowflake estimates the currently running clusters don’t have enough resources to handle any additional queries, Snowflake increases the number of clusters in the warehouse.  For warehouses with a MAX\_CLUSTER\_COUNT of 10 or less, Snowflake starts one additional cluster.  For warehouses with a MAX\_CLUSTER\_COUNT greater than 10, Snowflake starts multiple clusters at once to accommodate rapid increases in workload. | After a sustained period of low load, Snowflake shuts down one or more of the least-loaded clusters when the queries running on them finish. When the cluster count is higher than 10, Snowflake might shut down multiple clusters at a time. When the cluster count is 10 or less, Snowflake shuts down the idle clusters one at a time. |
| Economy | Conserves credits by favoring keeping running clusters fully-loaded rather than starting additional clusters, which may result in queries being queued and taking longer to complete. | Only if the system estimates there’s enough query load to keep the cluster busy for at least 6 minutes. | Snowflake marks the least-loaded cluster for shutdown if it estimates the cluster has less than 6 minutes of work left to do. Snowflake shuts down the cluster after finishing any queries that are running on that cluster. When the cluster count is higher than 10, Snowflake might shut down multiple clusters at a time. When the cluster count is 10 or less, Snowflake shuts down the idle clusters one at a time. |

Note

A third scaling policy, Legacy, was formerly provided for backward compatibility. Legacy has been removed.
All warehouses that were using the Legacy policy now use the default Standard policy.

You can set the scaling policy for a multi-cluster warehouse when it is created or at any time afterwards,
either in Snowsight or using SQL:

> Snowsight:
> :   When you select Multi-cluster Warehouse under Advanced Options in the New Warehouse dialog,
>     you can select the scaling policy from the Scaling Policy drop-down list.
>
>     For an existing multi-cluster warehouse, in the navigation menu, select Compute » Warehouses. Then select Edit
>     under the More menu (…).
>
>     In the Scaling Policy field, select the desired value from the drop-down list.
>
>     Tip
>
>     You only see the Scaling Policy drop-down list when the warehouse you selected is a multi-cluster warehouse,
>     and the maximum clusters value is higher than the minimum clusters value.
>
> SQL:
> :   Execute a [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command with `SCALING_POLICY`
>     set to the desired value.

For example, in SQL:

> ```
> CREATE WAREHOUSE mywh WITH MAX_CLUSTER_COUNT = 2, SCALING_POLICY = 'STANDARD';
> ALTER WAREHOUSE mywh SET SCALING_POLICY = 'ECONOMY';
> ```
>
> Copy

## Increasing or decreasing clusters for a multi-cluster warehouse[¶](#increasing-or-decreasing-clusters-for-a-multi-cluster-warehouse "Link to this heading")

You can increase or decrease the maximum and minimum number of clusters for a warehouse at any time,
even while it is running and executing statements. You can adjust the maximum and minimum clusters
for a warehouse in Snowsight or using SQL:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses.
>
>     Click on the warehouse name to view its properties and historical activity.
>     Select Edit from More menu (…).
>     You can also deselect the Multi-cluster Warehouse checkbox to reset the maximum and minimum
>     cluster settings to 1, changing the warehouse to a single-cluster one.
>
> SQL:
> :   Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.

Note

Currently, Snowsight supports updating MAX\_CLUSTER\_COUNT to a maximum of 10 clusters.
To increase MAX\_CLUSTER\_COUNT beyond 10, use the ALTER WAREHOUSE command in SQL.

The effect of changing the maximum and minimum clusters for a running warehouse depends on whether it is running in
Maximized or Auto-scale mode:

* Maximized:

  ↑ max & min:
  :   Specified number of clusters start immediately.

  ↓ max & min:
  :   Specified number of clusters shut down when they finish executing statements and the auto-suspend period elapses.
* Auto-scale:

  ↑ max:
  :   If `new_max_clusters > running_clusters`, no changes until additional clusters are needed.

  ↓ max:
  :   If `new_max_clusters < running_clusters`, excess clusters shut down when they finish executing statements and the
      [scaling policy](#label-mcw-scaling-policies) conditions are met.

  ↑ min:
  :   If `new_min_clusters > running_clusters`, additional clusters immediately started to meet the minimum.

  ↓ min:
  :   If `new_min_clusters < running_clusters`, excess clusters shut down when they finish executing statements and the
      [scaling policy](#label-mcw-scaling-policies) conditions are met.

## Monitoring multi-cluster warehouses[¶](#monitoring-multi-cluster-warehouses "Link to this heading")

You can monitor usage of multi-cluster warehouses through the web interface:

1. In the navigation menu, select Compute » Warehouses.
2. Select a warehouse name.

   > That way, you can monitor one warehouse in precise detail, such as viewing queries that are currently
   > running or queued.
   >
   > Alternatively, in the navigation menu, select Monitoring » Query History.
   > This page lets you view activity across multiple warehouses in your account.
   > To see the activity only for one warehouse, select Warehouse under the
   > Filters drop-down menu. Then choose a warehouse name from the list.

When you monitor a multi-cluster warehouse, you can see all the queries the warehouse processed.
For each query, you can see details such as how long it took, how many bytes
it scanned, and how many rows it returned. You can also see the cluster used to execute
each statement that the warehouse processed. To choose which details to view, select
the items such as Cluster Number, Duration, Rows, and so on
under the Columns drop-down menu.

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

1. [What is a multi-cluster warehouse?](#what-is-a-multi-cluster-warehouse)
2. [Examples of multi-cluster credit usage](#examples-of-multi-cluster-credit-usage)
3. [Creating a multi-cluster warehouse](#creating-a-multi-cluster-warehouse)
4. [Setting the scaling policy for a multi-cluster warehouse](#setting-the-scaling-policy-for-a-multi-cluster-warehouse)
5. [Increasing or decreasing clusters for a multi-cluster warehouse](#increasing-or-decreasing-clusters-for-a-multi-cluster-warehouse)
6. [Monitoring multi-cluster warehouses](#monitoring-multi-cluster-warehouses)

Related content

1. [Understanding compute cost](/user-guide/cost-understanding-compute)
2. [Working with resource monitors](/user-guide/resource-monitors)