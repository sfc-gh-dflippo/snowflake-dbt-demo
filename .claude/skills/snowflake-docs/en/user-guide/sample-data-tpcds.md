---
auto_generated: true
description: TPC-DS is a benchmark that models a retail product supplier’s decision
  support system. It has customer, order, and product data. Snowflake provides 10TB
  and 100TB versions of TPC-DS data for you to ex
last_scraped: '2026-01-14T16:57:49.106451+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/sample-data-tpcds
title: 'Sample data: TPC-DS | Snowflake Documentation'
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

[Get started](getting-started.md)[Sample data](sample-data.md)TPC-DS

# Sample data: TPC-DS[¶](#sample-data-tpc-ds "Link to this heading")

TPC-DS is a benchmark that models a retail product supplier’s decision support system. It has customer, order, and product data. Snowflake provides 10TB and 100TB versions of TPC-DS data for you to explore, in schemas named TPCDS\_SF10TCL and TPCDS\_SF100TCL, respectively, within the SNOWFLAKE\_SAMPLE\_DATA shared database.

As described in the [TPC Benchmark™ DS (TPC-DS)](http://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v2.5.0.pdf) specification:

> “In order to address the enormous range of query types and user behaviors encountered by a decision support
> system, TPC-DS utilizes a generalized query model. This model allows the benchmark to capture important
> aspects of the interactive, iterative nature of on-line analytical processing (OLAP) queries, the longer-running
> complex queries of data mining and knowledge discovery, and the more planned behavior of well known report queries.”

## Add the TPC-DS data set to your account[¶](#add-the-tpc-ds-data-set-to-your-account "Link to this heading")

You can access TPC-DS data sets in two ways:

* To access TPC-DS data sets that are provided by Snowflake directly, go to [Snowflake Marketplace](https://other-docs.snowflake.com/collaboration/collaboration-marketplace-about) in Snowsight.

  For more information, see [Getting TPC-DS data from Snowflake Marketplace](#label-get-tpcds-data-marketplace).
* To access the list of TPC-DS queries, download [`this script`](../_downloads/0eec2c68e78863a07eb994c85e76b188/tpc-ds-all-queries.sql).

## Database entities, relationships, and characteristics[¶](#database-entities-relationships-and-characteristics "Link to this heading")

The TPC-DS data set consists of 7 fact tables and 17 dimensions in the following schemas:

* TPCDS\_SF100TCL: The 100 TB (*scale factor* 100,000) version represents 100 million customers and over 500,000 items stored, with sales data spanning 3 channels — stores, catalogs,
  and the web — covering a period of 5 years. The largest table, STORE\_SALES, contains nearly 300 billion rows, and the fact tables contain over 560 billion rows in total.
* TPCDS\_SF10TCL: The 10 TB (scale factor 10,000) version represents 65 million customers and over 400,000 items stored, with sales data spanning 3 channels — stores, catalogs, and
  the web — covering a period of 5 years. The largest table, STORE\_SALES, contains nearly 29 billion rows, and the fact tables contain over 56 billion rows in total.

The relationships between facts and dimensions are represented through joins on surrogate keys. The detailed relationships are too numerous to display here, but can be found in the TPC-DS specification.

## Query definitions[¶](#query-definitions "Link to this heading")

TPC-DS contains a set of 99 queries with wide variation in complexity and range of data scanned. Each TPC-DS query asks a business question and includes the corresponding query to
answer the question. We have generated samples of all 99 TPC-DS queries for you to explore. Alternatively, you can use the tools in the TPC-DS Benchmark Kit to generate many different
versions of these queries that vary by parameter values.

Below, we describe just one of the queries. More information about TPC-DS and all the queries involved can be found in the official TPC-DS specification.

The [`TPC-DS script`](../_downloads/0eec2c68e78863a07eb994c85e76b188/tpc-ds-all-queries.sql), provided by Snowflake, contains the full list of TPC-DS queries. You can save the file to your local file system for reference.

### An example: Catalog sales call center outliers (Q57)[¶](#an-example-catalog-sales-call-center-outliers-q57 "Link to this heading")

This query looks at a year’s worth of CATALOG\_SALES table data and reveals the categories and brands where sales in a month vary more than 10% from average for a given call center.

#### Business question[¶](#business-question "Link to this heading")

Find the item brands and categories for each call center and their monthly sales figures for a specified year, where the monthly sales figure deviated
more than 10% of the average monthly sales for the year, sorted by deviation and call center. Report the sales deviation from the previous and following months.

#### Functional query definition[¶](#functional-query-definition "Link to this heading")

The query lists the following totals:

* Extended price
* Discounted extended price
* Discounted extended price plus tax
* Average quantity
* Average extended price
* Average discount

These aggregates are grouped by RETURNFLAG and LINESTATUS and are listed in ascending order of RETURNFLAG and LINESTATUS. A count of the number of line items in each group is included:

> ```
> use schema snowflake_sample_data.tpcds_sf10Tcl;
>
> -- QID=TPC-DS_query57
>
> with
> v1 as(
>   select i_category, i_brand,
>          cc_name,
>          d_year, d_moy,
>          sum(cs_sales_price) sum_sales,
>          avg(sum(cs_sales_price)) over
>            (partition by i_category, i_brand, cc_name, d_year) avg_monthly_sales,
>          rank() over (partition by i_category, i_brand, cc_name order by d_year, d_moy) rn
>   from item, catalog_sales, date_dim, call_center
>   where cs_item_sk = i_item_sk and
>         cs_sold_date_sk = d_date_sk and
>         cc_call_center_sk= cs_call_center_sk and
>           (
>             d_year = 2001 or
>           ( d_year = 2001-1 and d_moy =12) or
>           ( d_year = 2001+1 and d_moy =1)
>           )
>   group by i_category, i_brand,
>            cc_name , d_year, d_moy),
> v2 as(
>   select v1.i_brand
>     ,v1.d_year, v1.d_moy
>     ,v1.avg_monthly_sales
>     ,v1.sum_sales, v1_lag.sum_sales psum, v1_lead.sum_sales nsum
>   from v1, v1 v1_lag, v1 v1_lead
>   where v1.i_category = v1_lag.i_category and
>     v1.i_category = v1_lead.i_category and
>     v1.i_brand = v1_lag.i_brand and
>     v1.i_brand = v1_lead.i_brand and
>     v1.cc_name = v1_lag. cc_name and
>     v1.cc_name = v1_lead. cc_name and
>     v1.rn = v1_lag.rn + 1 and
>     v1.rn = v1_lead.rn - 1)
> select  *
> from v2
> where d_year = 2001 and
>   avg_monthly_sales > 0 and
>   case when avg_monthly_sales > 0
>        then abs(sum_sales - avg_monthly_sales) / avg_monthly_sales
>        else null
>        end > 0.1
> order by sum_sales - avg_monthly_sales, nsum
> limit 100;
> ```
>
> Copy

## Getting TPC-DS data from Snowflake Marketplace[¶](#getting-tpc-ds-data-from-sf-marketplace "Link to this heading")

You can access TPC-DS data directly by going to Snowflake Marketplace in Snowsight. You can create and query your own instance of the following data sets:

* TPC-DS 10 TB (standard table format)
* TPC-DS 10 TB Managed Iceberg ([Iceberg table format](tables-iceberg))

The data in the Managed Iceberg data set is physically stored in Iceberg format, rather than the Snowflake proprietary table format. You can get both data sets and compare the behavior of the two formats.

To get these data sets:

1. [Search for TPC-DS](https://app.snowflake.com/marketplace/data-products/search?search=tpc-ds) in Snowflake Marketplace. (Log in to Snowsight if prompted.)
2. Select one of the TPC-DS data sets.
3. Select Get.

   Request access from your administrator if necessary. Your login role might not have access to these data sets.
4. Under Options, give your TPC-DS database a user-defined name and select the role that you will use to access it. Alternatively, proceed with the default selections.
5. Select Get it for Free.

   In a few seconds, you should see the following pop-up window, which indicates that your instance of the TPC-DS database has been created and is available to inspect and query.

   [![Pop-up window that shows that the TPC-DS data set has been written to a database that you can query.](../_images/tpcds_ready_to_use.png)](../_images/tpcds_ready_to_use.png)
6. Select Query Data.
7. Query the data in the database, using either the worksheet provided or the [`TPC-DS script`](../_downloads/0eec2c68e78863a07eb994c85e76b188/tpc-ds-all-queries.sql), which contains all of the queries.

If you have already used Get to create one of these databases, you can go to it by selecting Open on the Marketplace [search results](https://app.snowflake.com/marketplace/data-products/search?search=tpc-ds).

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

1. [Add the TPC-DS data set to your account](#add-the-tpc-ds-data-set-to-your-account)
2. [Database entities, relationships, and characteristics](#database-entities-relationships-and-characteristics)
3. [Query definitions](#query-definitions)
4. [Getting TPC-DS data from Snowflake Marketplace](#getting-tpc-ds-data-from-sf-marketplace)