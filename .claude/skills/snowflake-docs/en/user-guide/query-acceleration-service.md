---
auto_generated: true
description: Enterprise Edition Feature
last_scraped: '2026-01-14T16:57:40.695307+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/query-acceleration-service
title: Using the Query Acceleration Service (QAS) | Snowflake Documentation
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

     + [Tutorial](tutorials/query-acceleration-service.md)
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

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Query Acceleration Service

# Using the Query Acceleration Service (QAS)[¶](#using-the-query-acceleration-service-qas "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The query acceleration service (QAS) can accelerate parts of the query workload in a warehouse. When it is enabled for a warehouse,
it can improve overall warehouse performance by reducing the impact of outlier queries, which are queries that use more resources than the
typical query. The query acceleration service does this by offloading portions of the query processing work to shared compute resources that
are provided by the service.

Examples of the types of workloads that might benefit from the query acceleration service include:

* Ad hoc analytics.
* Workloads with unpredictable data volume per query.
* Queries with large scans and selective filters.

The query acceleration service can handle these types of workloads more efficiently by performing more work in parallel and reducing the
wall-clock time spent in scanning and filtering.

Note

The query acceleration service depends on server availability. Therefore, performance improvements might fluctuate over time.

## SQL commands that QAS can accelerate[¶](#sql-commands-that-qas-can-accelerate "Link to this heading")

The query acceleration service supports the following SQL commands:

> * SELECT
> * INSERT
> * CREATE TABLE AS SELECT (CTAS)
> * COPY INTO <table>

Within a supported SQL command, QAS might accelerate an entire query, or a subquery or clause within the query,
if the command is eligible for acceleration.

## Enabling query acceleration[¶](#enabling-query-acceleration "Link to this heading")

To enable the query acceleration service, specify the clause ENABLE\_QUERY\_ACCELERATION = TRUE with the
[CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.

### Examples[¶](#examples "Link to this heading")

The following example enables the query acceleration service for a new warehouse named `my_wh`,
and for a warehouse named `my_other_wh` that’s initially created with QAS turned off:

```
CREATE WAREHOUSE my_wh WITH ENABLE_QUERY_ACCELERATION = true;

CREATE WAREHOUSE my_other_wh;
ALTER WAREHOUSE my_other_wh SET ENABLE_QUERY_ACCELERATION = true;
```

Copy

Run the [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses) command to display details about the `my_wh` warehouse.
The following query uses the [pipe operator](../sql-reference/operators-flow) (`->>`) to return information about
just the columns from the SHOW output that are relevant for QAS processing:

```
SHOW WAREHOUSES LIKE 'my_wh'
  ->> SELECT "name",
             "enable_query_acceleration",
             "query_acceleration_max_scale_factor"
        FROM $1;
```

Copy

```
+-------+---------------------------+-------------------------------------+
| name  | enable_query_acceleration | query_acceleration_max_scale_factor |
|-------+---------------------------+-------------------------------------|
| MY_WH | true                      |                                   8 |
+-------+---------------------------+-------------------------------------+
```

The query acceleration service might increase the credit consumption rate of a warehouse.
The maximum scale factor can help limit the consumption rate.
See [Adjusting the scale factor](#label-query-acceleration-scale-factor) to learn how to specify the
[QUERY\_ACCELERATION\_MAX\_SCALE\_FACTOR](../sql-reference/sql/create-warehouse.html#label-query-acceleration-max-scale-factor) property.
You do so using the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) and [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse)
commands.

The QUERY\_ACCELERATION\_ELIGIBLE view and the SYSTEM$ESTIMATE\_QUERY\_ACCELERATION function might be useful
in determining an appropriate scale factor for a warehouse.
See [Identifying queries and warehouses that might benefit from query acceleration](#label-identifying-queries-warehouses-for-qas) (in this topic) for details.

## Identifying queries and warehouses that might benefit from query acceleration[¶](#label-identifying-queries-warehouses-for-qas "Link to this heading")

To identify the queries or warehouses that might benefit from the query acceleration service, you can
query the [QUERY\_ACCELERATION\_ELIGIBLE](../sql-reference/account-usage/query_acceleration_eligible) view.
You can also use the [SYSTEM$ESTIMATE\_QUERY\_ACCELERATION](../sql-reference/functions/system_estimate_query_acceleration) function to assess
whether a specific query is eligible for acceleration.

### Eligible queries[¶](#eligible-queries "Link to this heading")

In general, queries are eligible because they have a portion of the query plan that can be run in parallel using QAS
compute resources. These queries fall into one of two patterns:

* Large scans with an aggregation or selective filter.
* Large scans that insert or copy many new rows (for example, INSERT and COPY commands).

Snowflake doesn’t have a specific cutoff for what constitutes a “large enough” scan to be eligible.
The threshold for eligibility depends on a variety of factors, including the query plan and
warehouse size. Snowflake only marks a query as eligible if there is high confidence that the query
would be accelerated if QAS was enabled. Over time, Snowflake is expanding the query patterns that
are eligible for acceleration. For example, formerly QAS didn’t accelerate queries with a LIMIT
clause and no ORDER BY clause, but now Snowflake automatically determines whether such queries can
benefit from QAS.

### Common reasons that queries are ineligible[¶](#common-reasons-that-queries-are-ineligible "Link to this heading")

Some queries are ineligible for query acceleration. The following are common reasons why a query cannot be accelerated:

* There aren’t enough partitions in the scan. If there aren’t enough partitions to scan, the benefits of query acceleration are offset by
  the latency in acquiring resources for the query acceleration service.
* Even if a query has a filter, the filters might not be selective enough. Alternatively, if the query has an aggregation with GROUP BY,
  the cardinality of the GROUP BY expression might be too high for eligibility.
* The query includes a LIMIT clause that prevents acceleration. QAS automatically determines which
  queries with LIMIT clauses (including those without ORDER BY) can be accelerated.
* The query includes functions that return nondeterministic results (for example, [SEQ](../sql-reference/functions/seq1) or [RANDOM](../sql-reference/functions/random)).

### Identifying queries with the SYSTEM$ESTIMATE\_QUERY\_ACCELERATION function[¶](#label-identify-queries-using-system-estimate-query-acceleration "Link to this heading")

The [SYSTEM$ESTIMATE\_QUERY\_ACCELERATION](../sql-reference/functions/system_estimate_query_acceleration) function can help determine if a previously executed query might
benefit from the query acceleration service. If the query is eligible for query acceleration, the function returns the estimated query
execution time for different query acceleration [scale factors](../sql-reference/sql/create-warehouse.html#label-query-acceleration-max-scale-factor).

#### Example[¶](#example "Link to this heading")

Execute the following statement to help determine if query acceleration might benefit a specific query:

```
SELECT PARSE_JSON(SYSTEM$ESTIMATE_QUERY_ACCELERATION('8cd54bf0-1651-5b1c-ac9c-6a9582ebd20f'));
```

Copy

In this example, the query is eligible for the query acceleration service. The result value includes estimated
query times using the service. The `ineligibleReason` property is empty.

```
{
  "estimatedQueryTimes": {
    "1": 171,
    "10": 115,
    "2": 152,
    "4": 133,
    "8": 120
  },
  "ineligibleReason": null,
  "originalQueryTime": 300.291,
  "queryUUID": "8cd54bf0-1651-5b1c-ac9c-6a9582ebd20f",
  "status": "eligible",
  "upperLimitScaleFactor": 10
}
```

Copy

The following example shows the results for a query that is not eligible for query acceleration service:

```
SELECT PARSE_JSON(SYSTEM$ESTIMATE_QUERY_ACCELERATION('cf23522b-3b91-cf14-9fe0-988a292a4bfa'));
```

Copy

The statement above produces the following output. The estimated query times are blank.
The `ineligibleReason` property reports why the query didn’t use QAS.

```
{
  "estimatedQueryTimes": {},
  "ineligibleReason": "NO_LARGE_ENOUGH_SCAN",
  "originalQueryTime": 20.291,
  "queryUUID": "cf23522b-3b91-cf14-9fe0-988a292a4bfa",
  "status": "ineligible",
  "upperLimitScaleFactor": 0
}
```

Copy

### Identifying queries and warehouses with the QUERY\_ACCELERATION\_ELIGIBLE view[¶](#label-query-acceleration-eligible-queries "Link to this heading")

Query the [QUERY\_ACCELERATION\_ELIGIBLE](../sql-reference/account-usage/query_acceleration_eligible) view
to identify the queries and warehouses that might benefit the most from the query acceleration
service. For each query, the view includes the amount of query execution time that is eligible for
the query acceleration service.

#### Examples[¶](#id1 "Link to this heading")

Note

These examples assume the ACCOUNTADMIN role (or a [role granted IMPORTED PRIVILEGES](../sql-reference/account-usage.html#label-enabling-usage-for-other-roles) on the
shared SNOWFLAKE database) is in use. If it is not in use, execute the following command before running the queries in the examples:

```
USE ROLE ACCOUNTADMIN;
```

Copy

Identify the queries in the past week that might benefit the most from the service by the longest amount of query execution time that is
eligible for acceleration:

```
SELECT query_id, eligible_query_acceleration_time
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY eligible_query_acceleration_time DESC;
```

Copy

Identify the queries in the past week that might benefit the most from the service in a specific warehouse `mywh`:

```
SELECT query_id, eligible_query_acceleration_time
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE warehouse_name = 'MYWH'
  AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY eligible_query_acceleration_time DESC;
```

Copy

Identify the warehouses with the most queries, in the past week, eligible for the query acceleration service:

```
SELECT warehouse_name, COUNT(query_id) AS num_eligible_queries
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  GROUP BY warehouse_name
  ORDER BY num_eligible_queries DESC;
```

Copy

Identify the warehouses with the most eligible time for the query acceleration service in the past week:

```
SELECT warehouse_name, SUM(eligible_query_acceleration_time) AS total_eligible_time
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  GROUP BY warehouse_name
  ORDER BY total_eligible_time DESC;
```

Copy

Identify the upper limit [scale factor](../sql-reference/sql/create-warehouse.html#label-query-acceleration-max-scale-factor) in the past week for the query acceleration
service for warehouse `mywh`:

```
SELECT MAX(upper_limit_scale_factor)
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE warehouse_name = 'MYWH'
  AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP());
```

Copy

Identify the distribution of scale factors in the past week for the query acceleration service for warehouse `mywh`:

```
SELECT upper_limit_scale_factor, COUNT(upper_limit_scale_factor)
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE warehouse_name = 'MYWH'
  AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  GROUP BY 1 ORDER BY 1;
```

Copy

## Adjusting the scale factor[¶](#adjusting-the-scale-factor "Link to this heading")

The scale factor is a cost control mechanism that allows you to set an upper bound on the amount of compute resources a warehouse can
lease for query acceleration. This value is used as a multiplier based on warehouse size and cost.

For example, suppose that you set the scale factor to 5 for a medium warehouse. This means that:

* The warehouse can lease compute resources up to 5 times the size of a medium warehouse.
* Because a medium warehouse costs [4 credits per hour](cost-understanding-compute.html#label-virtual-warehouse-credit-usage), leasing these resources can cost up
  to an additional 20 credits per hour (4 credits per warehouse x 5 times its size).

Tip

The scale factor applies to the entire warehouse, whether it’s a single-cluster or multi-cluster warehouse.
If you use QAS for a multi-cluster warehouse, consider increasing the scale factor.
That way, all the warehouse clusters can take advantage of the QAS optimizations.

The cost is the same no matter how many queries are using the query acceleration service at the same time.
The query acceleration service is billed by the second, only when the service is in use. These credits are billed separately from warehouse
usage.

Not all queries require the full set of resources that are made available by the scale factor. The amount of resources requested for the service
depends on how much of the query is eligible for acceleration and how much data will be processed to answer it. Regardless of the scale
factor value or the amount of resources requested, the amount of available compute resources for query acceleration is bound by the
availability of resources in the service and the number of other concurrent requests. The query acceleration service only uses as many
resources as it needs and that are available at the time the query is executed.

If the scale factor is not explicitly set, the default value is `8`. Setting the scale factor to `0` eliminates the upper bound limit
and allows queries to lease as many resources as necessary and as available to service the query.

### Example[¶](#id2 "Link to this heading")

The following example modifies the warehouse named `my_wh` to enable the query acceleration service with a maximum
scale factor of 0.

> ```
> ALTER WAREHOUSE my_wh SET
>   ENABLE_QUERY_ACCELERATION = true
>   QUERY_ACCELERATION_MAX_SCALE_FACTOR = 0;
> ```
>
> Copy

## Monitoring query acceleration service usage[¶](#monitoring-query-acceleration-service-usage "Link to this heading")

This section describes how to monitor the usage of the query acceleration service. By monitoring, you can understand the performance
impact, identify which queries benefit most from acceleration, and assess the overall effectiveness of the feature. Doing so can
help you manage your costs and optimize your workloads.

### Using the web interface to monitor query acceleration usage[¶](#using-the-web-interface-to-monitor-query-acceleration-usage "Link to this heading")

Once you enable the query acceleration service, you can view the Profile Overview panel in the
[Query Profile tab](ui-snowsight-activity) to see the effects of the query acceleration results.

The following screenshot displays an example of the statistics displayed for the query overall. If multiple operations in a query were
accelerated, the results are aggregated in this view so you can see the total amount of work done by the query acceleration service.

![../_images/query-acceleration-profile-overview.png](../_images/query-acceleration-profile-overview.png)

The Query Acceleration section of the Profile Overview panel includes the following statistics:

* *Partitions scanned by service* — number of files offloaded for scanning to the query acceleration service.
* *Scans selected for acceleration* — number of table scans being accelerated.

In the operator details (see [Statistics](ui-snowsight-activity.html#label-snowsight-query-profile-statistics)), click on the operator to see detailed information.
The following screenshot displays an example of the statistics displayed for a TableScan operation:

> ![../_images/query-acceleration-table-scan.png](../_images/query-acceleration-table-scan.png)

The Query Acceleration section of the TableScan details panel includes the following statistics:

* *Partitions scanned by service* — number of files offloaded for scanning to the query acceleration service.

### Using the Account Usage QUERY\_HISTORY view to monitor query acceleration usage[¶](#using-the-account-usage-query-history-view-to-monitor-query-acceleration-usage "Link to this heading")

To see the effects of query acceleration on a query, you can use the following columns in the
[QUERY\_HISTORY view](../sql-reference/account-usage/query_history).

* QUERY\_ACCELERATION\_BYTES\_SCANNED
* QUERY\_ACCELERATION\_PARTITIONS\_SCANNED
* QUERY\_ACCELERATION\_UPPER\_LIMIT\_SCALE\_FACTOR

You can use these columns to identify the queries that benefited from the query acceleration service. For each query, you can also
determine the total number of partitions and bytes scanned by the query acceleration service.

For descriptions of each of these columns, see [QUERY\_HISTORY view](../sql-reference/account-usage/query_history).

Note

For a given query, the sum of the QUERY\_ACCELERATION\_BYTES\_SCANNED and BYTES\_SCANNED columns might be greater when the query
acceleration service is used than when the service is not used. The same is true for the sum of the columns
QUERY\_ACCELERATION\_PARTITIONS\_SCANNED and PARTITIONS\_SCANNED.

The increase in the number of bytes and partitions is due to the intermediary results that are generated by the service to
facilitate query acceleration.

For example, to find the queries with the most bytes scanned by the query acceleration service in the past 24 hours:

```
SELECT query_id,
       query_text,
       warehouse_name,
       start_time,
       end_time,
       query_acceleration_bytes_scanned,
       query_acceleration_partitions_scanned,
       query_acceleration_upper_limit_scale_factor
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE query_acceleration_partitions_scanned > 0 
  AND start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  ORDER BY query_acceleration_bytes_scanned DESC;
```

Copy

To find the queries with the largest number of partitions scanned by the query acceleration service in the past 24 hours:

```
SELECT query_id,
       query_text,
       warehouse_name,
       start_time,
       end_time,
       query_acceleration_bytes_scanned,
       query_acceleration_partitions_scanned,
       query_acceleration_upper_limit_scale_factor
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE query_acceleration_partitions_scanned > 0 
  AND start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  ORDER BY query_acceleration_partitions_scanned DESC;
```

Copy

## Query acceleration service cost[¶](#query-acceleration-service-cost "Link to this heading")

Query Acceleration consumes credits as it uses [serverless compute resources](cost-understanding-compute.html#label-serverless-credit-usage) to execute portions of
eligible queries.

Query Acceleration is billed like other serverless features in Snowflake in that you pay by the second for the compute resources used. To
learn how many credits per compute-hour are consumed by the Query Acceleration Service, refer to the “Serverless
Feature Credit Table” in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Viewing billing information in the Classic Console[¶](#viewing-billing-information-in-the-classic-console "Link to this heading")

If you have Query Acceleration enabled for your account, the billing page in the Classic Console includes a warehouse called
QUERY\_ACCELERATION that shows all credits used by the service across all warehouses in your account.

The screenshot below shows an example of the billing information displayed for the QUERY\_ACCELERATION warehouse:

> ![../_images/query-acceleration-billing-ui.png](../_images/query-acceleration-billing-ui.png)

### Viewing billing using the Account Usage QUERY\_ACCELERATION\_HISTORY view[¶](#viewing-billing-using-the-account-usage-query-acceleration-history-view "Link to this heading")

You can view billing data in the Account Usage [QUERY\_ACCELERATION\_HISTORY view](../sql-reference/account-usage/query_acceleration_history).

#### Example[¶](#id3 "Link to this heading")

This query returns the total number of credits used by each warehouse in your account for the query acceleration service
(month-to-date):

```
SELECT warehouse_name,
       SUM(credits_used) AS total_credits_used
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
  WHERE start_time >= DATE_TRUNC(month, CURRENT_DATE)
  GROUP BY 1
  ORDER BY 2 DESC;
```

Copy

### Viewing billing using the Organization Usage QUERY\_ACCELERATION\_HISTORY view[¶](#viewing-billing-using-the-organization-usage-query-acceleration-history-view "Link to this heading")

You can view billing data for the query acceleration service for all accounts in your organization in the Organization Usage
[QUERY\_ACCELERATION\_HISTORY view](../sql-reference/organization-usage/query_acceleration_history).

#### Example[¶](#id4 "Link to this heading")

This query returns the total number of credits used by each warehouse in each account for the query acceleration service (month-to-date):

```
SELECT account_name,
       warehouse_name,
       SUM(credits_used) AS total_credits_used
  FROM SNOWFLAKE.ORGANIZATION_USAGE.QUERY_ACCELERATION_HISTORY
  WHERE usage_date >= DATE_TRUNC(month, CURRENT_DATE)
  GROUP BY 1, 2
  ORDER BY 3 DESC;
```

Copy

### Viewing billing using the QUERY\_ACCELERATION\_HISTORY function[¶](#viewing-billing-using-the-query-acceleration-history-function "Link to this heading")

You can also view billing data using the Information Schema [QUERY\_ACCELERATION\_HISTORY](../sql-reference/functions/query_acceleration_history) function.

#### Example[¶](#id5 "Link to this heading")

The following example uses the QUERY\_ACCELERATION\_HISTORY function to return information about the queries accelerated by this service
within the past 12 hours:

> ```
> SELECT start_time,
>        end_time,
>        credits_used,
>        warehouse_name,
>        num_files_scanned,
>        num_bytes_scanned
>   FROM TABLE(INFORMATION_SCHEMA.QUERY_ACCELERATION_HISTORY(
>     date_range_start=>DATEADD(H, -12, CURRENT_TIMESTAMP)));
> ```
>
> Copy

## Evaluating cost and performance[¶](#evaluating-cost-and-performance "Link to this heading")

This section includes example queries that might help you evaluate query performance and cost before and after enabling the query
acceleration service.

### Viewing warehouse and query acceleration service costs[¶](#viewing-warehouse-and-query-acceleration-service-costs "Link to this heading")

The following query computes the costs of the warehouse and the query acceleration service for a specific warehouse. You can execute
this query after enabling the query acceleration service for a warehouse to compare costs before and after enabling query acceleration.
The date range for the query begins 8 weeks prior to the first credit usage for the query acceleration service to 8 weeks after the last
incurred cost for query acceleration service (or up to the current date).

Note

* This query is most useful for evaluating the cost of the service if the warehouse properties and workload remain the same
  before and after enabling the query acceleration service.
* This query returns results only if there has been credit usage for accelerated queries in the warehouse.

This example query returns the warehouse and query acceleration service costs for `my_warehouse`:

```
WITH credits AS (
  SELECT 'QC' AS credit_type,
         TO_DATE(end_time) AS credit_date,
         SUM(credits_used) AS num_credits
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
    WHERE warehouse_name = 'my_warehouse'
    AND credit_date BETWEEN
           DATEADD(WEEK, -8, (
             SELECT TO_DATE(MIN(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
               WHERE warehouse_name = 'my_warehouse'
           ))
           AND
           DATEADD(WEEK, +8, (
             SELECT TO_DATE(MAX(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
               WHERE warehouse_name = 'my_warehouse'
           ))
  GROUP BY credit_date
  UNION ALL
  SELECT 'WC' AS credit_type,
         TO_DATE(end_time) AS credit_date,
         SUM(credits_used) AS num_credits
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE warehouse_name = 'my_warehouse'
    AND credit_date BETWEEN
           DATEADD(WEEK, -8, (
             SELECT TO_DATE(MIN(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
               WHERE warehouse_name = 'my_warehouse'
           ))
           AND
           DATEADD(WEEK, +8, (
             SELECT TO_DATE(MAX(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
               WHERE warehouse_name = 'my_warehouse'
           ))
  GROUP BY credit_date
)
SELECT credit_date,
       SUM(IFF(credit_type = 'QC', num_credits, 0)) AS qas_credits,
       SUM(IFF(credit_type = 'WC', num_credits, 0)) AS compute_credits,
       compute_credits + qas_credits AS total_credits,
       AVG(total_credits) OVER (
         PARTITION BY NULL ORDER BY credit_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
         AS avg_total_credits_7days
  FROM credits
  GROUP BY credit_date
  ORDER BY credit_date;
```

Copy

### Viewing query performance[¶](#viewing-query-performance "Link to this heading")

This query returns the average execution time for query acceleration eligible queries for a given warehouse. The date range for the query
begins 8 weeks prior to the first credit usage for the query acceleration service to 8 weeks after the last incurred cost for query
acceleration service (or up to the current date). The results might help you evaluate how the average query performance changed after
enabling the query acceleration service.

Note

* This query is most useful for evaluating query performance if the warehouse workload remains the same before and after enabling
  the query acceleration service.
* If the warehouse workload remains stable, the value in the `num_execs` column should remain consistent.
* If the value in the `num_execs` column of the query results dramatically increases or decreases, the results of this query
  will likely not be useful for query performance evaluation.

This example query returns the query execution time by day and computes the 7 day average for the week prior for queries that are
eligible for acceleration in the warehouse `my_warehouse`:

```
WITH qas_eligible_or_accelerated AS (
  SELECT TO_DATE(qh.end_time) AS exec_date,
        COUNT(*) AS num_execs,
        SUM(qh.execution_time) AS exec_time,
        MAX(IFF(qh.query_acceleration_bytes_scanned > 0, 1, NULL)) AS qas_accel_flag
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY AS qh
    WHERE qh.warehouse_name = 'my_warehouse'
    AND TO_DATE(qh.end_time) BETWEEN
           DATEADD(WEEK, -8, (
             SELECT TO_DATE(MIN(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
              WHERE warehouse_name = 'my_warehouse'
           ))
           AND
           DATEADD(WEEK, +8, (
             SELECT TO_DATE(MAX(end_time))
               FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
              WHERE warehouse_name = 'my_warehouse'
           ))
    AND (qh.query_acceleration_bytes_scanned > 0
          OR
          EXISTS (
            SELECT 1
              FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE AS qae
               WHERE qae.query_id = qh.query_id
               AND qae.warehouse_name = qh.warehouse_name
          )
         )
    GROUP BY exec_date
)
SELECT exec_date,
       SUM(exec_time) OVER (
         PARTITION BY NULL ORDER BY exec_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) /
       NULLIFZERO(SUM(num_execs) OVER (
         PARTITION BY NULL ORDER BY exec_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
       ) AS avg_exec_time_7days,
      exec_time / NULLIFZERO(num_execs) AS avg_exec_time,
      qas_accel_flag,
      num_execs,
      exec_time
  FROM qas_eligible_or_accelerated;
```

Copy

The output from the statement includes the following columns:

| Column | Description |
| --- | --- |
| EXEC\_DATE | Query execution date. |
| AVG\_EXEC\_TIME\_7DAYS | The average execution time for the prior 7 days inclusive of EXEC\_DATE. |
| AVG\_EXEC\_TIME | The average query execution time. |
| QAS\_ACCEL\_FLAG | 1 if any queries were accelerated; NULL if no queries were accelerated. |
| NUM\_EXECS | Number of queries accelerated. |
| EXEC\_TIME | Total execution time of all query acceleration eligible queries. |

Tip

When the query acceleration service (QAS) is enabled, Snowflake writes a small amount of data to remote storage
for each eligible query, even if QAS isn’t used for that query. Therefore, don’t be concerned by a nonzero
value for `bytes_spilled_to_remote_storage` in the QUERY\_HISTORY view when QAS is enabled.

## Compatibility with search optimization[¶](#compatibility-with-search-optimization "Link to this heading")

Query acceleration and [search optimization](search-optimization-service) can work together to
optimize query performance. First, search optimization can prune the [micro-partitions](tables-clustering-micropartitions.html#label-what-are-micropartitions) not needed for a query. Then, for [eligible queries](#label-identifying-queries-warehouses-for-qas), query acceleration can offload portions of the rest of the work to
shared compute resources provided by the service.

Performance of queries accelerated by both services varies depending on workload and available resources.

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

1. [SQL commands that QAS can accelerate](#sql-commands-that-qas-can-accelerate)
2. [Enabling query acceleration](#enabling-query-acceleration)
3. [Identifying queries and warehouses that might benefit from query acceleration](#label-identifying-queries-warehouses-for-qas)
4. [Adjusting the scale factor](#adjusting-the-scale-factor)
5. [Monitoring query acceleration service usage](#monitoring-query-acceleration-service-usage)
6. [Query acceleration service cost](#query-acceleration-service-cost)
7. [Evaluating cost and performance](#evaluating-cost-and-performance)
8. [Compatibility with search optimization](#compatibility-with-search-optimization)

Related content

1. [Tutorial: Improve Workload Performance with the Query Acceleration Service](/user-guide/tutorials/query-acceleration-service)
2. [CREATE WAREHOUSE](/user-guide/../sql-reference/sql/create-warehouse)
3. [ALTER WAREHOUSE](/user-guide/../sql-reference/sql/alter-warehouse)
4. [QUERY\_ACCELERATION\_ELIGIBLE view](/user-guide/../sql-reference/account-usage/query_acceleration_eligible)