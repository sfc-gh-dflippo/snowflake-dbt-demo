---
auto_generated: true
description: Aggregate functions (General) , Window function syntax and usage (General)
last_scraped: '2026-01-14T16:57:20.993775+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/stddev.html
title: STDDEV, STDDEV_SAMP | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)

     + General
     + [ANY\_VALUE](any_value.md)
     + [AVG](avg.md)
     + [CORR](corr.md)
     + [COUNT](count.md)
     + [COUNT\_IF](count_if.md)
     + [COVAR\_POP](covar_pop.md)
     + [COVAR\_SAMP](covar_samp.md)
     + [LISTAGG](listagg.md)
     + [MAX](max.md)
     + [MAX\_BY](max_by.md)
     + [MEDIAN](median.md)
     + [MIN](min.md)
     + [MIN\_BY](min_by.md)
     + [MODE](mode.md)
     + [PERCENTILE\_CONT](percentile_cont.md)
     + [PERCENTILE\_DISC](percentile_disc.md)
     + [STDDEV, STDDEV\_SAMP](stddev.md)
     + [STDDEV\_POP](stddev_pop.md)
     + [SUM](sum.md)
     + [VAR\_POP](var_pop.md)
     + [VAR\_SAMP](var_samp.md)
     + [VARIANCE](variance.md)
     + [VARIANCE\_POP](variance_pop.md)
     + [VARIANCE\_SAMP](variance.md)
     + Bitwise
     + [BITAND\_AGG](bitand_agg.md)
     + [BITOR\_AGG](bitor_agg.md)
     + [BITXOR\_AGG](bitxor_agg.md)
     + Boolean
     + [BOOLAND\_AGG](booland_agg.md)
     + [BOOLOR\_AGG](boolor_agg.md)
     + [BOOLXOR\_AGG](boolxor_agg.md)
     + Hash
     + [HASH\_AGG](hash_agg.md)
     + Semi-structured
     + [ARRAY\_AGG](array_agg.md)
     + [OBJECT\_AGG](object_agg.md)
     + Linear regression
     + [REGR\_AVGX](regr_avgx.md)
     + [REGR\_AVGY](regr_avgy.md)
     + [REGR\_COUNT](regr_count.md)
     + [REGR\_INTERCEPT](regr_intercept.md)
     + [REGR\_R2](regr_r2.md)
     + [REGR\_SLOPE](regr_slope.md)
     + [REGR\_SXX](regr_sxx.md)
     + [REGR\_SXY](regr_sxy.md)
     + [REGR\_SYY](regr_syy.md)
     + Statistics and probability
     + [KURTOSIS](kurtosis.md)
     + [SKEW](skew.md)
     + Count distinct values
     + [ARRAY\_UNION\_AGG](array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](array_unique_agg.md)
     + [BITMAP\_BIT\_POSITION](bitmap_bit_position.md)
     + [BITMAP\_BUCKET\_NUMBER](bitmap_bucket_number.md)
     + [BITMAP\_COUNT](bitmap_count.md)
     + [BITMAP\_CONSTRUCT\_AGG](bitmap_construct_agg.md)
     + [BITMAP\_OR\_AGG](bitmap_or_agg.md)
     + Cardinality estimation
     + [APPROX\_COUNT\_DISTINCT](approx_count_distinct.md)
     + [DATASKETCHES\_HLL](datasketches_hll.md)
     + [DATASKETCHES\_HLL\_ACCUMULATE](datasketches_hll_accumulate.md)
     + [DATASKETCHES\_HLL\_COMBINE](datasketches_hll_combine.md)
     + [DATASKETCHES\_HLL\_ESTIMATE](datasketches_hll_estimate.md)
     + [HLL](hll.md)
     + [HLL\_ACCUMULATE](hll_accumulate.md)
     + [HLL\_COMBINE](hll_combine.md)
     + [HLL\_ESTIMATE](hll_estimate.md)
     + [HLL\_EXPORT](hll_export.md)
     + [HLL\_IMPORT](hll_import.md)
     + Similarity estimation
     + [APPROXIMATE\_JACCARD\_INDEX](approximate_jaccard_index.md)
     + [APPROXIMATE\_SIMILARITY](approximate_similarity.md)
     + [MINHASH](minhash.md)
     + [MINHASH\_COMBINE](minhash_combine.md)
     + Frequency estimation
     + [APPROX\_TOP\_K](approx_top_k.md)
     + [APPROX\_TOP\_K\_ACCUMULATE](approx_top_k_accumulate.md)
     + [APPROX\_TOP\_K\_COMBINE](approx_top_k_combine.md)
     + [APPROX\_TOP\_K\_ESTIMATE](approx_top_k_estimate.md)
     + Percentile estimation
     + [APPROX\_PERCENTILE](approx_percentile.md)
     + [APPROX\_PERCENTILE\_ACCUMULATE](approx_percentile_accumulate.md)
     + [APPROX\_PERCENTILE\_COMBINE](approx_percentile_combine.md)
     + [APPROX\_PERCENTILE\_ESTIMATE](approx_percentile_estimate.md)
     + Utilities
     + [GROUPING](grouping.md)
     + [GROUPING\_ID](grouping_id.md)
     + AI Functions
     + [AI\_AGG](ai_agg.md)
     + [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     + Semantic views
     + [AGG](agg.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](ai_classify.md)
       * [AI\_COMPLETE](ai_complete.md)
       * [AI\_COUNT\_TOKENS](ai_count_tokens.md)
       * [AI\_EMBED](ai_embed.md)
       * [AI\_EXTRACT](ai_extract.md)
       * [AI\_FILTER](ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](ai_parse_document.md)
       * [AI\_REDACT](ai_redact.md)
       * [AI\_SENTIMENT](ai_sentiment.md)
       * [AI\_SIMILARITY](ai_similarity.md)
       * [AI\_TRANSCRIBE](ai_transcribe.md)
       * [AI\_TRANSLATE](ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](try_complete-snowflake-cortex.md)")
   * [Bitwise expression](../expressions-byte-bit.md)
   * [Conditional expression](../expressions-conditional.md)
   * [Context](../functions-context.md)
   * [Conversion](../functions-conversion.md)
   * [Data generation](../functions-data-generation.md)
   * [Data metric](../functions-data-metric.md)
   * [Date & time](../functions-date-time.md)
   * [Differential privacy](../functions-differential-privacy.md)
   * [Encryption](../functions-encryption.md)
   * [File](../functions-file.md)
   * [Geospatial](../functions-geospatial.md)
   * [Hash](../functions-hash-scalar.md)
   * [Metadata](../functions-metadata.md)
   * [ML Model Monitors](../functions-model-monitors.md)
   * [Notification](../functions-notification.md)
   * [Numeric](../functions-numeric.md)
   * [Organization users and organization user groups](../functions-organization-users.md)
   * [Regular expressions](../functions-regexp.md)
   * [Semi-structured and structured data](../functions-semistructured.md)
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Aggregate](../functions-aggregation.md)STDDEV, STDDEV\_SAMP

Categories:
:   [Aggregate functions](../functions-aggregation) (General) , [Window function syntax and usage](../functions-window-syntax) (General)

# STDDEV, STDDEV\_SAMP[¶](#stddev-stddev-samp "Link to this heading")

Returns the sample standard deviation (square root of sample variance) of non-NULL values. STDDEV and STDDEV\_SAMP are aliases
for the same function.

See also [STDDEV\_POP](stddev_pop), which returns the population standard deviation (square root of variance).

## Syntax[¶](#syntax "Link to this heading")

**Aggregate function**

```
{ STDDEV | STDDEV_SAMP } ( [ DISTINCT ] <expr1> )
```

Copy

**Window function**

```
{ STDDEV | STDDEV_SAMP } ( [ DISTINCT ] <expr1> ) OVER (
                                                       [ PARTITION BY <expr2> ]
                                                       [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                                       )
```

Copy

For details about `window_frame` syntax, see [Usage notes for window frames](../functions-window-syntax.html#label-window-frames).

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   An expression that evaluates to a numeric value. This is the expression on which the standard deviation is calculated.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is DOUBLE.

If all records inside a group are NULL, this function returns NULL.

## Usage notes[¶](#usage-notes "Link to this heading")

* For single-record inputs, STDDEV and STDDEV\_SAMP both return NULL. This is different from the Oracle behavior, where STDDEV\_SAMP returns NULL for a single record and STDDEV returns 0.
* When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast cannot be performed, an error is returned.
* When this function is called as a window function and the OVER clause contains an ORDER BY clause:

  + The DISTINCT keyword is prohibited and results in a SQL compilation error.
  + A window frame must be specified. If you do not specify a window frame, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

  For more details about window frames, including syntax and examples, see [Usage notes for window frames](../functions-window-syntax.html#label-window-frames).

## Aggregate function examples[¶](#aggregate-function-examples "Link to this heading")

The following example calculates the standard deviation for a small sample of integers:

> ```
> CREATE TABLE t1 (c1 INTEGER);
> INSERT INTO t1 (c1) VALUES
>     (6),
>    (10),
>    (14)
>    ;
> SELECT STDDEV(c1) FROM t1;
> ```
>
> Copy
>
> ```
> +----------+
> | STDDEV() |
> |----------|
> |        4 |
> +----------+
> ```

Note that the function STDDEV\_SAMP returns the same result:

> ```
> SELECT STDDEV_SAMP(c1) FROM t1;
> ```
>
> Copy
>
> ```
> +-----------------+
> | STDDEV_SAMP(C1) |
> |-----------------|
> |               4 |
> +-----------------+
> ```

The following example uses a small table named `menu_items`, which lists items for sale from a food
truck. If you would like to create and load this table, see [Create and load the menu\_items table](#label-create-and-load-menu-items-table).

To find the sample standard deviation for both the cost of goods sold (COGS) and the sale price for the
`Dessert` rows, run this query:

> ```
> SELECT menu_category, STDDEV(menu_cogs_usd) stddev_cogs, STDDEV(menu_price_usd) stddev_price
>   FROM menu_items
>   WHERE menu_category='Dessert'
>   GROUP BY 1;
> ```
>
> Copy
>
> ```
> +---------------+-------------+--------------+
> | MENU_CATEGORY | STDDEV_COGS | STDDEV_PRICE |
> |---------------+-------------+--------------|
> | Dessert       |  1.00519484 |  1.471960144 |
> +---------------+-------------+--------------+
> ```

## Window function example[¶](#window-function-example "Link to this heading")

The following example also uses the `menu_items` table (see [Create and load the menu\_items table](#label-create-and-load-menu-items-table))
but calls the STDDEV function as a window function.

The window function partitions rows by the `menu_category` column. Therefore, the standard deviation is
calculated once for each category, and that value is repeated in the result for each row in the group.
In this example, the rows must be grouped by both the menu category and the cost of goods sold.

> ```
> SELECT menu_category, menu_cogs_usd,
>     STDDEV(menu_cogs_usd) OVER(PARTITION BY menu_category) stddev_cogs
>   FROM menu_items
>   GROUP BY 1,2
>   ORDER BY menu_category;
> ```
>
> Copy

The following output is a partial result set for this query (the first 15 rows):

> ```
> +---------------+---------------+--------------+
> | MENU_CATEGORY | MENU_COGS_USD |  STDDEV_COGS |
> |---------------+---------------+--------------|
> | Beverage      |          0.50 | 0.1258305738 |
> | Beverage      |          0.65 | 0.1258305738 |
> | Beverage      |          0.75 | 0.1258305738 |
> | Dessert       |          1.25 | 1.054751155  |
> | Dessert       |          3.00 | 1.054751155  |
> | Dessert       |          1.00 | 1.054751155  |
> | Dessert       |          2.50 | 1.054751155  |
> | Dessert       |          0.50 | 1.054751155  |
> | Main          |          4.50 | 3.444051572  |
> | Main          |          2.40 | 3.444051572  |
> | Main          |          1.50 | 3.444051572  |
> | Main          |         11.00 | 3.444051572  |
> | Main          |          8.00 | 3.444051572  |
> | Main          |          NULL | 3.444051572  |
> | Main          |         12.00 | 3.444051572  |
> ...
> ```

## Create and load the menu\_items table[¶](#create-and-load-the-menu-items-table "Link to this heading")

To create and insert rows into the `menu_items` table that is used in some function examples,
run the following SQL commands. (This table contains 60 rows. It is based on, but not identical to,
the `menu` table in the
[Tasty Bytes sample database](https://quickstarts.snowflake.com/guide/tasty_bytes_introduction/index.html#0).)

```
CREATE OR REPLACE TABLE menu_items(
  menu_id INT NOT NULL,
  menu_category VARCHAR(20),
  menu_item_name VARCHAR(50),
  menu_cogs_usd NUMBER(7,2),
  menu_price_usd NUMBER(7,2));
```

Copy

```
INSERT INTO menu_items VALUES(1,'Beverage','Bottled Soda',0.500,3.00);
INSERT INTO menu_items VALUES(2,'Beverage','Bottled Water',0.500,2.00);
INSERT INTO menu_items VALUES(3,'Main','Breakfast Crepe',5.00,12.00);
INSERT INTO menu_items VALUES(4,'Main','Buffalo Mac & Cheese',6.00,10.00);
INSERT INTO menu_items VALUES(5,'Main','Chicago Dog',4.00,9.00);
INSERT INTO menu_items VALUES(6,'Main','Chicken Burrito',3.2500,12.500);
INSERT INTO menu_items VALUES(7,'Main','Chicken Pot Pie Crepe',6.00,15.00);
INSERT INTO menu_items VALUES(8,'Main','Combination Curry',9.00,15.00);
INSERT INTO menu_items VALUES(9,'Main','Combo Fried Rice',5.00,11.00);
INSERT INTO menu_items VALUES(10,'Main','Combo Lo Mein',6.00,13.00);
INSERT INTO menu_items VALUES(11,'Main','Coney Dog',5.00,10.00);
INSERT INTO menu_items VALUES(12,'Main','Creamy Chicken Ramen',8.00,17.2500);
INSERT INTO menu_items VALUES(13,'Snack','Crepe Suzette',4.00,9.00);
INSERT INTO menu_items VALUES(14,'Main','Fish Burrito',3.7500,12.500);
INSERT INTO menu_items VALUES(15,'Snack','Fried Pickles',1.2500,6.00);
INSERT INTO menu_items VALUES(16,'Snack','Greek Salad',4.00,11.00);
INSERT INTO menu_items VALUES(17,'Main','Gyro Plate',8.00,12.00);
INSERT INTO menu_items VALUES(18,'Main','Hot Ham & Cheese',7.00,11.00);
INSERT INTO menu_items VALUES(19,'Dessert','Ice Cream Sandwich',1.00,4.00);
INSERT INTO menu_items VALUES(20,'Beverage','Iced Tea',0.7500,3.00);
INSERT INTO menu_items VALUES(21,'Main','Italian',6.00,11.00);
INSERT INTO menu_items VALUES(22,'Main','Lean Beef Tibs',6.00,13.00);
INSERT INTO menu_items VALUES(23,'Main','Lean Burrito Bowl',3.500,12.500);
INSERT INTO menu_items VALUES(24,'Main','Lean Chicken Tibs',5.00,11.00);
INSERT INTO menu_items VALUES(25,'Main','Lean Chicken Tikka Masala',10.00,17.00);
INSERT INTO menu_items VALUES(26,'Beverage','Lemonade',0.6500,3.500);
INSERT INTO menu_items VALUES(27,'Main','Lobster Mac & Cheese',10.00,15.00);
INSERT INTO menu_items VALUES(28,'Dessert','Mango Sticky Rice',1.2500,5.00);
INSERT INTO menu_items VALUES(29,'Main','Miss Piggie',2.600,6.00);
INSERT INTO menu_items VALUES(30,'Main','Mothers Favorite',4.500,12.00);
INSERT INTO menu_items VALUES(31,'Main','New York Dog',4.00,8.00);
INSERT INTO menu_items VALUES(32,'Main','Pastrami',8.00,11.00);
INSERT INTO menu_items VALUES(33,'Dessert','Popsicle',0.500,3.00);
INSERT INTO menu_items VALUES(34,'Main','Pulled Pork Sandwich',7.00,12.00);
INSERT INTO menu_items VALUES(35,'Main','Rack of Pork Ribs',11.2500,21.00);
INSERT INTO menu_items VALUES(36,'Snack','Seitan Buffalo Wings',4.00,7.00);
INSERT INTO menu_items VALUES(37,'Main','Spicy Miso Vegetable Ramen',7.00,17.2500);
INSERT INTO menu_items VALUES(38,'Snack','Spring Mix Salad',2.2500,6.00);
INSERT INTO menu_items VALUES(39,'Main','Standard Mac & Cheese',3.00,8.00);
INSERT INTO menu_items VALUES(40,'Dessert','Sugar Cone',2.500,6.00);
INSERT INTO menu_items VALUES(41,'Main','Tandoori Mixed Grill',11.00,18.00);
INSERT INTO menu_items VALUES(42,'Main','The Classic',4.00,12.00);
INSERT INTO menu_items VALUES(43,'Main','The King Combo',12.00,20.00);
INSERT INTO menu_items VALUES(44,'Main','The Kitchen Sink',6.00,14.00);
INSERT INTO menu_items VALUES(45,'Main','The Original',1.500,5.00);
INSERT INTO menu_items VALUES(46,'Main','The Ranch',2.400,6.00);
INSERT INTO menu_items VALUES(47,'Main','The Salad of All Salads',6.00,12.00);
INSERT INTO menu_items VALUES(48,'Main','Three Meat Plate',10.00,17.00);
INSERT INTO menu_items VALUES(49,'Main','Three Taco Combo Plate',7.00,11.00);
INSERT INTO menu_items VALUES(50,'Main','Tonkotsu Ramen',7.00,17.2500);
INSERT INTO menu_items VALUES(51,'Main','Two Meat Plate',9.00,14.00);
INSERT INTO menu_items VALUES(52,'Dessert','Two Scoop Bowl',3.00,7.00);
INSERT INTO menu_items VALUES(53,'Main','Two Taco Combo Plate',6.00,9.00);
INSERT INTO menu_items VALUES(54,'Main','Veggie Burger',5.00,9.00);
INSERT INTO menu_items VALUES(55,'Main','Veggie Combo',4.00,9.00);
INSERT INTO menu_items VALUES(56,'Main','Veggie Taco Bowl',6.00,10.00);
INSERT INTO menu_items VALUES(57,'Dessert','Waffle Cone',2.500,6.00);
INSERT INTO menu_items VALUES(58,'Main','Wonton Soup',2.00,6.00);
INSERT INTO menu_items VALUES(59,'Main','Mini Pizza',null,null);
INSERT INTO menu_items VALUES(60,'Main','Large Pizza',null,null);
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Arguments](#arguments)
3. [Returns](#returns)
4. [Usage notes](#usage-notes)
5. [Aggregate function examples](#aggregate-function-examples)
6. [Window function example](#window-function-example)
7. [Create and load the menu\_items table](#create-and-load-the-menu-items-table)