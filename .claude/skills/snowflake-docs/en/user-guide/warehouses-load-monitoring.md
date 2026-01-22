---
auto_generated: true
description: The web interface provides a query load chart that depicts concurrent
  queries processed by a warehouse over a two-week period. Warehouse query load measures
  the average number of queries that were run
last_scraped: '2026-01-14T16:57:38.825850+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-load-monitoring
title: Monitoring warehouse load | Snowflake Documentation
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Monitoring load

# Monitoring warehouse load[¶](#monitoring-warehouse-load "Link to this heading")

The web interface provides a *query load* chart that depicts concurrent queries processed by a warehouse over a two-week period. Warehouse
query load measures the average number of queries that were running or queued within a specific interval.

You can customize the time period and time interval during which to evaluate warehouse performance by querying the Account Usage
[QUERY\_HISTORY view](../sql-reference/account-usage/query_history).

## Viewing the load monitoring chart[¶](#viewing-the-load-monitoring-chart "Link to this heading")

Note

To view the load monitoring chart, you must be using a role that has the MONITOR privilege on the warehouse.

To view the chart:

> In the navigation menu, select Compute » Warehouses » *<warehouse\_name>*
>
> > The Warehouse Activity tile appears with a bar chart and lets you select a window of time to view in
> > the chart. By default, the chart displays the past two weeks in 1-day intervals.
> >
> > You can select a range from 1 hour (minimum) to 2 weeks (maximum). The chart displays the total query load in intervals of 1 minute
> > to 1 day, depending on the range you selected.

### Understanding the bar chart[¶](#understanding-the-bar-chart "Link to this heading")

Hover over a bar to view the average number of queries processed by the warehouse during the time period represented. The bar displays the
individual load for each query status that occurred within the interval:

| Query Status | Description |
| --- | --- |
| Running | Queries that were actively running during the interval. Note that they may have started running before and continued running after the interval. |
| Queued (Provisioning) | Queries that were waiting while the warehouse provisioned compute resources. Typically only occurs in the first few minutes after a warehouse resumes. |
| Blocked | Queries that were blocked during the interval due to a transaction lock. |
| Queued | Queries that were waiting to run due to warehouse overload (i.e. waiting for other queries to finish running and free compute resources). |

## How query load is calculated[¶](#how-query-load-is-calculated "Link to this heading")

Query load is calculated by dividing the execution time (in seconds) of all queries in an interval by the total time (in seconds) for the interval.

For example, the following table illustrates how query load is calculated based on 5 queries that contributed to the warehouse load during a 5-minute interval. The load from running queries was .92 and queued queries (due to warehouse overload) was .08.

| Query | Status | Execution Time / Interval (in Seconds) | Query Load |
| --- | --- | --- | --- |
| Query 1 | Running | 30 / 300 | 0.10 |
| Query 2 | Running | 201 / 300 | 0.67 |
| Query 3 | Running | 15 / 300 | 0.05 |
| Query 4 | Running | 30 / 300 | 0.10 |
|  |  | **Running Load** | **0.92** |
| Query 5 | Queued | 24 / 300 | 0.08 |
|  |  | **Queued Load** | **0.08** |
|  |  | **TOTAL WAREHOUSE LOAD** | **1.00** |

To determine the actual number of running queries (and the duration of each query) during a specific interval, consult the
History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page. On the page, filter the query history by warehouse, then scroll down to the interval you specified in
the load monitoring chart.

## Using the load monitoring chart to make decisions[¶](#using-the-load-monitoring-chart-to-make-decisions "Link to this heading")

The load monitoring chart can help you make decisions for managing your warehouses by showing current and historic usage patterns.

### Slow query performance[¶](#slow-query-performance "Link to this heading")

When you notice that a query is running slowly, check whether an overloaded warehouse is causing the query to compete for resources or get queued:

* If the running query load is high or there’s queuing, consider starting a separate warehouse and moving queued queries to that warehouse.
  Alternatively, if you are using [multi-cluster warehouses](warehouses-multicluster), you could change your multi-cluster
  settings to add additional clusters to handle higher concurrency going forward.

* If the running query load is low and query performance is slow, you could resize the warehouse to provide more compute resources. You would
  need to restart the query once all the new resources were fully provisioned to take advantage of the added resources.

### Peak query performance[¶](#peak-query-performance "Link to this heading")

Analyze the daily workload on the warehouse over the previous two weeks. If you see recurring usage spikes, consider moving some of the peak
workload to its own warehouse and potentially running the remaining workload on a smaller warehouse. Alternatively, you could change your
multi-cluster settings to add additional clusters to handle higher concurrency going forward.

If you notice that your current workload is considerably higher than normal, open the History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page to investigate which
queries are contributing to the higher load.

### Excessive credit usage[¶](#excessive-credit-usage "Link to this heading")

Analyze the daily workload on the warehouse over the previous two weeks. If the chart shows recurring time periods when the warehouse was
running and consuming credits, but the total query load was less than **1** for substantial periods of time, the warehouse use is inefficient.
You might consider any of the following actions:

* Decrease the warehouse size. Note that decreasing the warehouse size generally increases the query execution time.
* For a multi-cluster warehouse, decrease the **MIN\_CLUSTER\_COUNT** parameter value.

## Using Account Usage QUERY\_HISTORY view to evaluate warehouse performance[¶](#using-account-usage-query-history-view-to-evaluate-warehouse-performance "Link to this heading")

You can query the QUERY\_HISTORY view to calculate virtual warehouse performance metrics such as throughput and latency for specific
statement types. For more information, see [Examples: Warehouse performance](../sql-reference/account-usage.html#label-account-usage-warehouse-performance-query).

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

1. [Viewing the load monitoring chart](#viewing-the-load-monitoring-chart)
2. [How query load is calculated](#how-query-load-is-calculated)
3. [Using the load monitoring chart to make decisions](#using-the-load-monitoring-chart-to-make-decisions)
4. [Using Account Usage QUERY\_HISTORY view to evaluate warehouse performance](#using-account-usage-query-history-view-to-evaluate-warehouse-performance)

Related content

1. [Understanding compute cost](/user-guide/cost-understanding-compute)
2. [Working with resource monitors](/user-guide/resource-monitors)