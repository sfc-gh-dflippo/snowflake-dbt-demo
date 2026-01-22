---
auto_generated: true
description: 'As described in the TPC Benchmark™ H (TPC-H) specification:'
last_scraped: '2026-01-14T16:57:49.502462+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/sample-data-tpch
title: 'Sample data: TPC-H | Snowflake Documentation'
---

1. [Overview](getting-started.md)
2. [Get started for users](../getting-started-for-users.md)
3. [Tutorials](../learn-tutorials.md)
4. [Concepts for administrators](../concepts-for-administrators.md)
5. [Sample data](sample-data.md)

   * [Usage](sample-data-using.md)
   * [TPC-DS](sample-data-tpcds.md)
   * [TPC-H](sample-data-tpch.md)
6. [Contacting support](contacting-support.md)

[Get started](getting-started.md)[Sample data](sample-data.md)TPC-H

# Sample data: TPC-H[¶](#sample-data-tpc-h "Link to this heading")

As described in the [TPC Benchmark™ H (TPC-H)](http://www.tpc.org/tpch/) specification:

> “TPC-H is a decision support benchmark. It consists of a suite of business-oriented ad hoc queries and concurrent data modifications. The queries and the data populating the database have been chosen
> to have broad industry-wide relevance. This benchmark illustrates decision support systems that examine large volumes of data, execute queries with a high degree of complexity, and give answers to
> critical business questions.”

## Database and schemas[¶](#database-and-schemas "Link to this heading")

TPC-H comes with various data set sizes to test different scaling factors. For demonstration purposes, we’ve shared four versions of the TPC-H data. The data is provided in the following schemas in the
SNOWFLAKE\_SAMPLE\_DATA shared database:

* TPCH\_SF1: Consists of the base row size (several million elements).
* TPCH\_SF10: Consists of the base row size x 10.
* TPCH\_SF100: Consists of the base row size x 100 (several hundred million elements).
* TPCH\_SF1000: Consists of the base row size x 1000 (several billion elements).

## Database entities, relationships, and characteristics[¶](#database-entities-relationships-and-characteristics "Link to this heading")

The components of TPC-H consist of eight separate and individual tables (the Base Tables). The relationships between columns in these tables are illustrated in the following ER diagram:

> ![Schema for TPC-H benchmark data](../_images/sample-data-tpch-schema.png)

(source: [TPC Benchmark H Standard Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf))

## Query definitions[¶](#query-definitions "Link to this heading")

Each TPC-H query asks a business question and includes the corresponding query to answer the question. Some of the TPC-H queries are included in Snowflake’s Get Started tutorials.

This section describes one of the queries. For more information about TPC-H and all the queries that are involved, see the official
[TPC Benchmark H Standard Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf).

### Q1: Pricing summary report query[¶](#q1-pricing-summary-report-query "Link to this heading")

This query reports the amount of business that was billed, shipped, and returned.

#### Business question[¶](#business-question "Link to this heading")

The Pricing Summary Report Query provides a summary pricing report for all line items that were shipped as of a given date. The date is within 60-120 days of the greatest ship date contained in the database.

#### Functional query definition[¶](#functional-query-definition "Link to this heading")

The query lists totals for extended price, discounted extended price, discounted extended price plus tax, average quantity, average extended price, and average discount. These aggregates are grouped by
RETURNFLAG and LINESTATUS, and listed in ascending order of RETURNFLAG and LINESTATUS. A count of the number of line items in each group is included:

> ```
> use schema snowflake_sample_data.tpch_sf1;   -- or snowflake_sample_data.{tpch_sf10 | tpch_sf100 | tpch_sf1000}
>
> select
>        l_returnflag,
>        l_linestatus,
>        sum(l_quantity) as sum_qty,
>        sum(l_extendedprice) as sum_base_price,
>        sum(l_extendedprice * (1-l_discount)) as sum_disc_price,
>        sum(l_extendedprice * (1-l_discount) * (1+l_tax)) as sum_charge,
>        avg(l_quantity) as avg_qty,
>        avg(l_extendedprice) as avg_price,
>        avg(l_discount) as avg_disc,
>        count(*) as count_order
>  from
>        lineitem
>  where
>        l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
>  group by
>        l_returnflag,
>        l_linestatus
>  order by
>        l_returnflag,
>        l_linestatus;
> ```
>
> Copy

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

1. [Database and schemas](#database-and-schemas)
2. [Database entities, relationships, and characteristics](#database-entities-relationships-and-characteristics)
3. [Query definitions](#query-definitions)