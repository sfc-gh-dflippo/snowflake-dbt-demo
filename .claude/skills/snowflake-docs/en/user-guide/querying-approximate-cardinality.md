---
auto_generated: true
description: Snowflake uses HyperLogLog to estimate the approximate number of distinct
  values in a data set. HyperLogLog is a state-of-the-art cardinality estimation algorithm,
  capable of estimating distinct cardi
last_scraped: '2026-01-14T16:55:35.427526+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/querying-approximate-cardinality
title: Estimating the Number of Distinct Values | Snowflake Documentation
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

    * [Joins](querying-joins.md)
    * [Subqueries](querying-subqueries.md)
    * [Querying Hierarchical Data](queries-hierarchical.md)
    * [Common Table Expressions (CTE)](queries-cte.md)")
    * [Querying Semi-structured Data](querying-semistructured.md)
    * [Using full-text search](querying-with-search-functions.md)
    * [Constructing SQL at Runtime](querying-construct-at-runtime.md)
    * [Analyzing time-series data](querying-time-series-data.md)
    * [Analyzing data with window functions](functions-window-using.md)
    * [Match Recognize](match-recognize-introduction.md)
    * [Sequences](querying-sequences.md)
    * [Persisted Query Results](querying-persisted-results.md)
    * [Distinct Counts](querying-distinct-counts.md)

      + [Estimation](querying-approximate-cardinality.md)
      + [Bitmaps for Hierarchical Aggregations](querying-bitmaps-for-distinct-counts.md)
      + [Arrays for Hierarchical Aggregations](querying-arrays-for-distinct-counts.md)
    * [Similarity Estimation](querying-approximate-similarity.md)
    * [Frequency Estimation](querying-approximate-frequent-values.md)
    * [Estimating Percentile Values](querying-approximate-percentile-values.md)
    * [Monitor query activity with Query History](ui-snowsight-activity.md)
    * [Using query insights to improve performance](query-insights.md)
    * [Query Hash](query-hash.md)
    * [Top-K pruning](querying-top-k-pruning-optimization.md)
    * [Cancel Statements](querying-cancel-statements.md)
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

[Guides](../guides/README.md)[Queries](../guides/overview-queries.md)[Distinct Counts](querying-distinct-counts.md)Estimation

# Estimating the Number of Distinct Values[¶](#estimating-the-number-of-distinct-values "Link to this heading")

Snowflake uses HyperLogLog to estimate the approximate number of distinct values in a data set. HyperLogLog is a state-of-the-art cardinality estimation algorithm, capable of estimating distinct
cardinalities of trillions of rows with an average relative error of a few percent.

HyperLogLog can be used in place of [COUNT(DISTINCT …)](../sql-reference/functions/count) in situations where estimating cardinality is acceptable.

## Overview[¶](#overview "Link to this heading")

Snowflake provides a bias-corrected implementation of the HyperLogLog algorithm presented in [HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf) by Flajolet et al.

We recommend using HyperLogLog whenever the input is potentially large and an approximate result is acceptable. The average relative error of our HyperLogLog implementation is 1.62338% (i.e. the
average relative difference to the corresponding [COUNT(DISTINCT …)](../sql-reference/functions/count) result).

## SQL Functions[¶](#sql-functions "Link to this heading")

The following [Aggregate functions](../sql-reference/functions-aggregation) are provided for estimating cardinality using HyperLogLog:

* [HLL](../sql-reference/functions/hll): Returns an approximation of the distinct cardinality of the input.
* [HLL\_ACCUMULATE](../sql-reference/functions/hll_accumulate): Skips the final estimation step and returns the HyperLogLog state at the end of an aggregation.
* [HLL\_COMBINE](../sql-reference/functions/hll_combine): Combines (i.e. merges) input states into a single output state.
* [HLL\_ESTIMATE](../sql-reference/functions/hll_estimate): Computes a cardinality estimate of a HyperLogLog state produced by HLL\_ACCUMULATE and HLL\_COMBINE.
* [HLL\_EXPORT](../sql-reference/functions/hll_export): Converts HyperLogLog states from BINARY format to an OBJECT (which can then be printed and exported as JSON).
* [HLL\_IMPORT](../sql-reference/functions/hll_import): Converts HyperLogLog states from OBJECT format to BINARY format.

## Implementation Details[¶](#implementation-details "Link to this heading")

Our implementation hashes input rows to 64-bit values, of which the upper 12 bits or “precision” (as referred to in the HyperLogLog algorithm paper; see above document link for details) are used to
partition input values into so-called sub-streams. This yields an average relative error of:

> `sqrt(3*ln(2)-1)/sqrt(2^precision) = 0.0162338 = 1.62338%`

In other words, for a query where [COUNT(DISTINCT …)](../sql-reference/functions/count) would return a result of `1,000,000`, HyperLogLog typically returns a result in the range of
`983,767` to `1,016,234`.

For each sub-stream, HyperLogLog maintains the maximum leading-zero count (between 0 and 52 for 64-bit values at precision = 12). The most straight-forward representation of this state is a simple byte
array, one byte for each of the `2^12 = 4096` sub-streams. Our implementation indeed requires at most 4096 Byte (`2^precision = 2^12 = 4096`) of memory per aggregation group. Technically, only
6 bits (rather than 8 bits) are required per sub-stream, but we trade some space efficiency for computational efficiency.

For small input cardinalities, most of the sub-streams will never be hit. So rather than allocating an entire block of 4096 Byte per aggregation group up-front, our implementation uses a space-optimized
“sparse” representation of this state whenever beneficial. Consequently, the memory cost of HyperLogLog can be substantially lower than 4096 Byte per aggregation group (down to about 32 Byte per
aggregation group). This allows cardinality estimation over many aggregation groups (millions or even billions, as determined by the GROUP BY or OVER clause of the query), using orders of magnitude less
memory and CPU time than a corresponding [COUNT(DISTINCT …)](../sql-reference/functions/count) query.

In the (rare) case where an extremely large input table and many aggregation groups cause HyperLogLog to exceed its total memory budget, Snowflake is still able to spill to temp space and perform
recursive aggregation, as with any other aggregation function.

## Exported State Format[¶](#exported-state-format "Link to this heading")

The state of the HyperLogLog algorithm can be exported and imported (or reimported) using the [HLL\_EXPORT](../sql-reference/functions/hll_export) and [HLL\_IMPORT](../sql-reference/functions/hll_import) functions,
respectively. The exported state is of type OBJECT and contains the following fields.

### Dense Format[¶](#dense-format "Link to this heading")

`version`:
:   Version number of the HyperLogLog implementation.

`precision`:
:   Number of hashed value bits to use to select sub-streams. Currently fixed to 12.

`dense`:
:   An array of integers, each containing the maximum leading-zero count + 1 for the corresponding sub-stream. 0 indicates that the corresponding sub-stream has not been hit yet. Legal values
    are in the range of 0 to 53. The corresponding sub-stream index is given by the element position in the array.

For example:

> ```
> {
>   "version" : 3,
>   "precision" : 12,
>   "dense" : [3,3,3,3,5,3,4,3,5,6,2,4,4,7,5,6,6,3,2,2,3,2,4,5,5,5,2,5,5,3,6,1,4,2,2,4,4,5,2,5,...,4,6,3]
> }
> ```
>
> Copy

### Sparse Format[¶](#sparse-format "Link to this heading")

`version`:
:   Version number of the HyperLogLog implementation.

`precision`:
:   Number of hashed value bits to use to select sub-streams. Currently fixed to 12.

`sparse`:
:   `indices`: An array of integers, each containing a sub-stream index (base 0). Legal values are in the range of 0 to 4095.

    `maxLzCounts`: An array of integers, each containing the maximum leading-zero count + 1 for the corresponding sub-stream. 0 indicates that the corresponding sub-stream has not been hit yet.
    :   Legal values are in the range of 0 to 53. The sub-stream for a given leading-zero count is given by the corresponding element in the `indices` array.

    The `indices` and `maxLzCounts` arrays must have the same length. The [HLL\_IMPORT](../sql-reference/functions/hll_import) function also checks that sub-stream indices are in the valid range, and
    that there are no duplicate sub-stream indices. The `indices` array need not be sorted. The leading-zero counts are not validated. Invalid values will not cause query failures, but will lead
    to undefined results for [HLL\_ESTIMATE](../sql-reference/functions/hll_estimate).

For example:

> ```
> {
>   "version" : 3,
>   "precision" : 12,
>   "sparse" : {
>     "indices": [1131,1241,1256,1864,2579,2699,3730],
>     "maxLzCounts":[2,4,2,1,3,2,1]
>   }
> }
> ```
>
> Copy

## Examples[¶](#examples "Link to this heading")

**Environment set up:**

> ```
> USE WAREHOUSE dontdrop;
> USE DATABASE stressdb;
> USE SCHEMA bdb_5nodes;
>
> SELECT COUNT(*) FROM uservisits;
>
> -----------+
>  COUNT(*)  |
> -----------+
>  751754869 |
> -----------+
> ```
>
> Copy

**Step 1:**

Create a table that contains the calendar date (year/month/day) and the HLL structure. We use [HLL\_EXPORT](../sql-reference/functions/hll_export) to store the binary structure as a text object:

> ```
> CREATE OR REPLACE TABLE daily_uniques
> AS
> SELECT
>  visitdate,
>  hll_export(hll_accumulate(sourceip)) AS hll_sourceip
> FROM uservisits
> GROUP BY visitdate;
> ```
>
> Copy

**Step 2:**

We can calculate the unique IPs by month by aggregating each day’s HLL structure from Step 1. We use [HLL\_IMPORT](../sql-reference/functions/hll_import) to transform the text to the binary structure, then
[HLL\_COMBINE](../sql-reference/functions/hll_combine) to combine multiple HLL structures into a single structure, then [HLL\_ESTIMATE](../sql-reference/functions/hll_estimate) to compute the number of distinct values:

> ```
> SELECT
>   EXTRACT(year FROM visitdate) AS visit_year,
>   EXTRACT(month FROM visitdate) AS visit_month,
>   hll_estimate(hll_combine(hll_import(hll_sourceip))) AS distinct_ips
> FROM daily_uniques
> WHERE visitdate BETWEEN '2000-01-01' AND '2000-12-31'
> GROUP BY 1,2
> ORDER BY 1,2;
>
> ------------+-------------+--------------+
>  VISIT_YEAR | VISIT_MONTH | DISTINCT_IPS |
> ------------+-------------+--------------+
>        2000 |           1 |      1515168 |
>        2000 |           2 |      1410289 |
>        2000 |           3 |      1491997 |
>        2000 |           4 |      1460837 |
>        2000 |           5 |      1546647 |
>        2000 |           6 |      1485599 |
>        2000 |           7 |      1522643 |
>        2000 |           8 |      1492831 |
>        2000 |           9 |      1488507 |
>        2000 |          10 |      1553201 |
>        2000 |          11 |      1461140 |
>        2000 |          12 |      1515772 |
> ------------+-------------+--------------+
>
> Elapsed 1.3s
> ```
>
> Copy

**Compare:**

We compare the use of the aggregation using the HLL functions to HLL on the detail level data. In this case, `HLL()` is equivalent to the `HLL_ESTIMATE(HLL_COMBINE(HLL_IMPORT()))` from
Step 2:

> ```
> SELECT
>   EXTRACT(year FROM visitdate) AS visit_year,
>   EXTRACT(month FROM visitdate) AS visit_month,
>   hll(sourceip) AS distinct_ips
> FROM uservisits
> WHERE visitdate BETWEEN '2000-01-01' AND '2000-12-31'
> GROUP BY 1,2
> ORDER BY 1,2;
>
> ------------+-------------+--------------+
>  VISIT_YEAR | VISIT_MONTH | DISTINCT_IPS |
> ------------+-------------+--------------+
>        2000 |           1 |      1515168 |
>        2000 |           2 |      1410289 |
>        2000 |           3 |      1491997 |
>        2000 |           4 |      1460837 |
>        2000 |           5 |      1546647 |
>        2000 |           6 |      1485599 |
>        2000 |           7 |      1522643 |
>        2000 |           8 |      1492831 |
>        2000 |           9 |      1488507 |
>        2000 |          10 |      1553201 |
>        2000 |          11 |      1461140 |
>        2000 |          12 |      1515772 |
> ------------+-------------+--------------+
>
> Elapsed 2m 29s
> ```
>
> Copy

As you can see, aggregation of the HLL structures is significantly faster than aggregation over the base data, e.g. 1.3 seconds vs 149 seconds in this small example, which represents a 100x decrease
in query time.

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

1. [Overview](#overview)
2. [SQL Functions](#sql-functions)
3. [Implementation Details](#implementation-details)
4. [Exported State Format](#exported-state-format)
5. [Examples](#examples)