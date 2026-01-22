---
auto_generated: true
description: This topic provides general guidelines and best practices for using virtual
  warehouses in Snowflake to process queries. It does not provide specific or absolute
  numbers, values, or recommendations bec
last_scraped: '2026-01-14T16:57:42.305552+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-considerations
title: Warehouse considerations | Snowflake Documentation
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Considerations

# Warehouse considerations[¶](#warehouse-considerations "Link to this heading")

This topic provides general guidelines and best practices for using virtual warehouses in Snowflake to process queries. It does
not provide specific or absolute numbers, values, or recommendations because every query scenario is different and is affected by
numerous factors, including number of concurrent users/queries, number of tables being queried, and data size and composition, as well as
your specific requirements for warehouse availability, latency, and cost.

It also does not cover warehouse considerations for data loading, which are covered in another topic (see the sidebar).

The keys to using warehouses effectively and efficiently are:

1. Experiment with different types of queries and different warehouse sizes to determine the combinations that best meet your
   specific query needs and workload.
2. Don’t focus on warehouse size. Snowflake utilizes per-second billing, so you can run larger warehouses (Large, X-Large,
   2X-Large, etc.) and simply suspend them when not in use.

Note

These guidelines and best practices apply to both single-cluster warehouses, which are standard for all accounts, and
[multi-cluster warehouses](warehouses-multicluster), which are available in [Snowflake Enterprise Edition](intro-editions) (and higher).

## How are credits charged for warehouses?[¶](#how-are-credits-charged-for-warehouses "Link to this heading")

Credit charges are calculated based on:

* The warehouse size.
* The number of clusters (if using [multi-cluster warehouses](warehouses-multicluster)).
* The length of time the compute resources in each cluster runs.

For example:

X-Small:
:   Bills 1 credit per full, continuous hour that each cluster runs; each successive size generally doubles the number of compute
    resources per warehouse.

4X-Large:
:   Bills 128 credits per full, continuous hour that each cluster runs.

Note the following:

* When compute resources are provisioned for a warehouse:

  + The minimum billing charge for provisioning compute resources is 1 minute (i.e. 60 seconds).
  + There is no benefit to stopping a warehouse before the first 60-second period is over because the credits have already
    been billed for that period.
  + After the first 60 seconds, all subsequent billing for a running warehouse is per-second (until all its compute resources are shut down).
    Three examples are provided below:

    - If a warehouse runs for 30 to 60 seconds, it is billed for 60 seconds.
    - If a warehouse runs for 61 seconds, it is billed for only 61 seconds.
    - If a warehouse runs for 61 seconds, shuts down, and then restarts and runs for less than 60 seconds, it is billed for 121 seconds (60 + 1 + 60).
* Resizing a warehouse provisions additional compute resources for each cluster in the warehouse:

  + This results in a corresponding increase in the number of credits billed for the warehouse (while the additional compute resources are
    running).
  + The additional compute resources are billed when they are provisioned (i.e. credits for the additional resources are billed relative
    to the time when the warehouse was resized).
  + Resizing between a 5XL or 6XL warehouse to a 4XL or smaller warehouse results in a brief period during which the customer is
    charged for both the new warehouse and the old warehouse while the old warehouse is quiesced.
  + Credit usage is displayed in hour increments. With per-second billing, you will see fractional amounts for credit usage/billing.

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](warehouses-gen2.html#label-gen-2-standard-warehouses-altering).

## How does query composition impact warehouse processing?[¶](#how-does-query-composition-impact-warehouse-processing "Link to this heading")

The compute resources required to process a query depend on the size and complexity of the query. For the most part, queries scale
linearly with respect to warehouse size, particularly for larger, more complex queries. When considering factors that impact query
processing, consider the following:

* The overall size of the tables being queried has more impact than the number of rows.
* Query filtering using predicates has an impact on processing, as does the number of joins/tables in the query.

Tip

To achieve the best results, try to execute relatively homogeneous queries (complexity, data sets, etc.) on the same warehouse;
executing queries of widely varying complexity on the same warehouse makes it more difficult to analyze warehouse load,
which can make it more difficult to select the best warehouse size to match the complexity, composition, and number of queries in your
workload.

## How does warehouse caching impact queries?[¶](#how-does-warehouse-caching-impact-queries "Link to this heading")

Each warehouse, when running, maintains a cache of table data accessed as queries are processed by the warehouse. This enables improved
performance for subsequent queries if they are able to read from the cache instead of from the table(s) in the query. The size of the cache
is determined by the compute resources in the warehouse (that is, the larger the warehouse and, therefore, more compute resources in the
warehouse, the larger the cache).

This cache is dropped when the warehouse is suspended, which might result in slower initial performance for some queries after the warehouse
is resumed. As the resumed warehouse runs and processes more queries, the cache is rebuilt, and queries that are able to take advantage of
the cache will experience improved performance.

Keep this in mind when deciding whether to suspend a warehouse or leave it running. In other words, consider the trade-off between saving
credits by suspending a warehouse versus maintaining the cache of data from previous queries to help with performance.

## Creating a warehouse[¶](#creating-a-warehouse "Link to this heading")

When creating a warehouse, the two most critical factors to consider, from a cost and performance perspective, are:

* Warehouse size (that is, available compute resources)
* Manual vs automated management (for starting/resuming and suspending warehouses).

The number of clusters in a warehouse is also important if you are using [Snowflake Enterprise Edition](intro-editions) (or higher) and
[multi-cluster warehouses](warehouses-multicluster). For more details, see [Scaling Up vs Scaling Out](#scaling-up-vs-scaling-out) (in this topic).

### Selecting an initial warehouse size[¶](#selecting-an-initial-warehouse-size "Link to this heading")

The initial size you select for a warehouse depends on the task the warehouse is performing and the workload it processes. For example:

* For data loading, the warehouse size should match the number of files being loaded and the amount of data in each file. For more information,
  see [Planning a data load](data-load-considerations-plan).
* For queries in small-scale testing environments, smaller warehouses sizes (X-Small, Small, Medium) may be sufficient.
* For queries in large-scale production environments, larger warehouse sizes (Large, X-Large, 2X-Large, etc.) may be more cost effective.

However, note that per-second credit billing and auto-suspend give you the flexibility to start with larger sizes and then adjust the size
to match your workloads. You can decrease the size of a warehouse at any time.

Also, larger is not necessarily faster for smaller, more basic queries. Small/simple queries typically do not need an X-Large (or larger)
warehouse because they do not necessarily benefit from the additional resources, regardless of the number of queries being processed
concurrently. In general, you should try to match the size of the warehouse to the expected size and complexity of the queries to be
processed by the warehouse.

Tip

Experiment by running the same queries against warehouses of multiple sizes (for example, X-Large, Large, Medium). The queries you experiment
with should be of a size and complexity that you know will typically complete within 5 to 10 minutes (or less).

### Selecting a warehouse for Snowsight[¶](#selecting-a-warehouse-for-sf-web-interface "Link to this heading")

Certain Snowsight pages, such as Task Run History or Data Preview, require a warehouse to run SQL queries in order to
display more than just metadata. On these pages, a warehouse selector indicates the warehouse where these UI queries are running. A green
dot indicates when the warehouse is active.

An X-Small warehouse is recommended and generally sufficient for most of these queries, however large accounts may see performance
improvements by using a larger warehouse.

In some cases, your account is not billed for client-generated statements. For example, [SHOW TABLES](../sql-reference/sql/show-tables) does not
require a warehouse to retrieve data, so no charges apply. For more information about warehouses in general, see [Overview of warehouses](warehouses-overview).

Note

Snowsight performance can be affected if the warehouse is temporarily overloaded and UI queries are queued behind other active
workloads. If you notice inconsistent Snowsight performance, Snowflake recommends that you review the selected warehouse for
overload and consider using one with lower utilization. Large accounts with many active users might benefit from a dedicated X-Small
warehouse for UI-related tasks.

You can view which Snowsight queries have been running on the currently selected warehouse and when they ran. To monitor these
queries, follow these steps:

1. In the navigation menu, select Monitoring » Query History.
2. Select the Filters drop-down list.
3. Select the Client-generated statements checkbox to view internal queries run by a client, driver, or library, including the web interface.
4. Select Apply Filters.

For information about cost governance, see [Exploring compute cost](cost-exploring-compute).

### Using the default warehouse for Notebook apps[¶](#using-the-default-warehouse-for-notebook-apps "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

Available to all accounts.

Each account is provisioned with the SYSTEM$STREAMLIT\_NOTEBOOK\_WH warehouse that is specifically designed to run Notebook Python code. This multi-cluster X-Small warehouse helps reduce cluster fragmentation, optimize costs, and improve bin-packing efficiency. For more
details, see [Default warehouse for notebooks](warehouses-overview.html#label-default-warehouse).

### Automating warehouse suspension[¶](#automating-warehouse-suspension "Link to this heading")

Warehouses can be set to automatically suspend when there’s no activity after a specified period of time. Auto-suspend is enabled by
specifying the time period (minutes, hours, etc.) of inactivity for the warehouse.

We recommend setting auto-suspend according to your workload and your requirements for warehouse availability:

* If you enable auto-suspend, we recommend setting it to a low value (for example, 5 or 10 minutes or less) because Snowflake utilizes per-second
  billing. This will help keep your warehouses from running (and consuming credits) when not in use.

  However, the value you set should match the gaps, if any, in your query workload. For example, if you have regular gaps of 2 or 3 minutes
  between incoming queries, it doesn’t make sense to set auto-suspend to 1 or 2 minutes because your warehouse will be in a continual state
  of suspending and resuming (if auto-resume is also enabled) and each time it resumes, you are billed for the minimum credit usage (that is, 60 seconds).
* You might want to consider disabling auto-suspend for a warehouse if:

  + You have a heavy, steady workload for the warehouse.
  + You require the warehouse to be available with no delay or lag time. Warehouse provisioning is generally very fast (e.g. 1 or 2
    seconds); however, depending on the size of the warehouse and the availability of compute resources to provision, it can take longer.

Important

If you choose to disable auto-suspend, carefully consider the costs associated with running a warehouse continually, even when the
warehouse is not processing queries. The costs can be significant, especially for larger warehouses (X-Large, 2X-Large, etc.).

To disable auto-suspend, you must explicitly select Never in the web interface, or specify `0` or `NULL` in SQL.

### Automating warehouse resumption[¶](#automating-warehouse-resumption "Link to this heading")

Warehouses can be set to automatically resume when new queries are submitted.

We recommend enabling/disabling auto-resume depending on how much control you wish to exert over usage of a particular warehouse:

* If cost and access are not an issue, enable auto-resume to ensure that the warehouse starts whenever needed. Keep in mind that there
  might be a short delay in the resumption of the warehouse due to provisioning.
* If you wish to control costs and/or user access, leave auto-resume disabled and instead manually resume the warehouse only when needed.

## Scaling up vs scaling out[¶](#scaling-up-vs-scaling-out "Link to this heading")

Snowflake supports two ways to scale warehouses:

* Scale up by resizing a warehouse.
* Scale out by adding clusters to a multi-cluster warehouse (requires [Snowflake Enterprise Edition](intro-editions) or
  higher).

### Warehouse resizing improves performance[¶](#warehouse-resizing-improves-performance "Link to this heading")

Resizing a warehouse generally improves query performance, particularly for larger, more complex queries. It can also help reduce the
queuing that occurs if a warehouse does not have enough compute resources to process all the queries that are submitted concurrently. Note
that warehouse resizing is not intended for handling concurrency issues; instead, use additional warehouses to handle the workload or use a
multi-cluster warehouse (if this feature is available for your account).

Snowflake supports resizing a warehouse at any time, even while running. If a query is running slowly and you have additional queries of
similar size and complexity that you want to run on the same warehouse, you might choose to resize the warehouse while it is running; however,
note the following:

* As stated earlier about warehouse size, larger is not necessarily faster; for smaller, basic queries that are already executing quickly,
  you may not see any significant improvement after resizing.
* Resizing a running warehouse does not impact queries that are already being processed by the warehouse; the additional compute resources,
  once fully provisioned, are only used for queued and new queries.
* Resizing between a 5XL or 6XL warehouse to a 4XL or smaller warehouse results in a brief period during which the customer is charged
  for both the new warehouse and the old warehouse while the old warehouse is quiesced.

Tip

Decreasing the size of a running warehouse removes compute resources from the warehouse. When the computer resources are removed, the
cache associated with those resources is dropped, which can impact performance in the same way that suspending the warehouse can impact
performance after it is resumed.

Keep this in mind when choosing whether to decrease the size of a running warehouse or keep it at the current size. In other words, there
is a trade-off with regards to saving credits versus maintaining the cache.

### Multi-cluster warehouses improve concurrency[¶](#multi-cluster-warehouses-improve-concurrency "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition Feature](intro-editions)

To inquire about upgrading to Enterprise Edition, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Multi-cluster warehouses](warehouses-multicluster) are designed specifically for handling queuing and performance issues
related to large numbers of concurrent users and/or
queries. In addition, multi-cluster warehouses can help automate this process if your number of users/queries tend to fluctuate.

When deciding whether to use multi-cluster warehouses and the number of clusters to use per multi-cluster warehouse, consider the
following:

* If you are using Snowflake Enterprise Edition (or a higher edition), all your warehouses should be configured as multi-cluster
  warehouses.
* Unless you have a specific requirement for running in Maximized mode, multi-cluster warehouses should be configured to run in Auto-scale
  mode, which enables Snowflake to automatically start and stop clusters as needed.
* When choosing the minimum and maximum number of clusters for a multi-cluster warehouse:

  Minimum:
  :   Keep the default value of `1`; this ensures that additional clusters are only started as needed. However, if
      high-availability of the warehouse is a concern, set the value higher than `1`. This helps ensure multi-cluster warehouse availability
      and continuity in the unlikely event that a cluster fails.

  Maximum:
  :   Set this value as large as possible, while being mindful of the warehouse size and corresponding credit costs. For example, an
      X-Large multi-cluster warehouse with maximum clusters = `10` will consume 160 credits in an hour if all 10 clusters run
      continuously for the hour.

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

1. [How are credits charged for warehouses?](#how-are-credits-charged-for-warehouses)
2. [How does query composition impact warehouse processing?](#how-does-query-composition-impact-warehouse-processing)
3. [How does warehouse caching impact queries?](#how-does-warehouse-caching-impact-queries)
4. [Creating a warehouse](#creating-a-warehouse)
5. [Scaling up vs scaling out](#scaling-up-vs-scaling-out)

Related content

1. [Working with resource monitors](/user-guide/resource-monitors)
2. [Data loading considerations](/user-guide/data-load-considerations)