---
auto_generated: true
description: Window functions (General)
last_scraped: '2026-01-14T16:57:59.096552+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/conditional_change_event
title: CONDITIONAL_CHANGE_EVENT | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)
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

     + [Syntax and usage](../functions-window-syntax.md)
     + General
     + [ANY\_VALUE](any_value.md)
     + [AVG](avg.md)
     + [CONDITIONAL\_CHANGE\_EVENT](conditional_change_event.md)
     + [CONDITIONAL\_TRUE\_EVENT](conditional_true_event.md)
     + [CORR](corr.md)
     + [COUNT](count.md)
     + [COUNT\_IF](count_if.md)
     + [COVAR\_POP](covar_pop.md)
     + [COVAR\_SAMP](covar_samp.md)
     + [INTERPOLATE\_BFILL](interpolate_bfill.md)
     + [INTERPOLATE\_FFILL](interpolate_bfill.md)
     + [INTERPOLATE\_LINEAR](interpolate_bfill.md)
     + [LISTAGG](listagg.md)
     + [MAX](max.md)
     + [MEDIAN](median.md)
     + [MIN](min.md)
     + [MODE](mode.md)
     + [PERCENTILE\_CONT](percentile_cont.md)
     + [PERCENTILE\_DISC](percentile_disc.md)
     + [RATIO\_TO\_REPORT](ratio_to_report.md)
     + [STDDEV, STDDEV\_SAMP](stddev.md)
     + [STDDEV\_POP](stddev_pop.md)
     + [SUM](sum.md)
     + [VAR\_POP](var_pop.md)
     + [VAR\_SAMP](var_samp.md)
     + [VARIANCE](variance.md)
     + [VARIANCE\_POP](variance_pop.md)
     + [VARIANCE\_SAMP](variance.md)
     + Ranking
     + [CUME\_DIST](cume_dist.md)
     + [DENSE\_RANK](dense_rank.md)
     + [FIRST\_VALUE](first_value.md)
     + [LAG](lag.md)
     + [LAST\_VALUE](last_value.md)
     + [LEAD](lead.md)
     + [NTH\_VALUE](nth_value.md)
     + [NTILE](ntile.md)
     + [PERCENT\_RANK](percent_rank.md)
     + [RANK](rank.md)
     + [ROW\_NUMBER](row_number.md)
     + Bitwise aggregation
     + [BITAND\_AGG](bitand_agg.md)
     + [BITOR\_AGG](bitor_agg.md)
     + [BITXOR\_AGG](bitxor_agg.md)
     + Boolean aggregation
     + [BOOLAND\_AGG](booland_agg.md)
     + [BOOLOR\_AGG](boolor_agg.md)
     + [BOOLXOR\_AGG](boolxor_agg.md)
     + Hash aggregation
     + [HASH\_AGG](hash_agg.md)
     + Semi-structured aggregation
     + [ARRAY\_AGG](array_agg.md)
     + [OBJECT\_AGG](object_agg.md)
     + Counting distinct values
     + [ARRAY\_UNION\_AGG](array_union_agg.md)
     + [ARRAY\_UNIQUE\_AGG](array_unique_agg.md)
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
     + Cardinality estimation
     + [APPROX\_COUNT\_DISTINCT](approx_count_distinct.md)
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
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Window](../functions-window.md)CONDITIONAL\_CHANGE\_EVENT

Categories:
:   [Window functions](../functions-window) (General)

# CONDITIONAL\_CHANGE\_EVENT[¶](#conditional-change-event "Link to this heading")

Returns a window event number for each row within a window partition when the value of the argument `expr1` in
the current row is different from the value of `expr1` in the previous row. The window event number starts
from 0 and is incremented by 1 to indicate the number of changes so far within that window.

## Syntax[¶](#syntax "Link to this heading")

```
CONDITIONAL_CHANGE_EVENT( <expr1> ) OVER ( [ PARTITION BY <expr2> ] ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`expr1`
:   This is an expression that gets compared with the expression of the previous row.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the expression to order by within each partition.

## Usage notes[¶](#usage-notes "Link to this heading")

* The expression `CONDITIONAL_CHANGE_EVENT (expr1) OVER (window_frame)` is calculated as:

  > `CONDITIONAL_TRUE_EVENT( <expr1> != LAG(<expr1>) OVER(window_frame)) OVER(window_frame)`

  For more information about CONDITIONAL\_TRUE\_EVENT, see [CONDITIONAL\_TRUE\_EVENT](conditional_true_event).

## Examples[¶](#examples "Link to this heading")

This shows how to detect the number of times that the power failed and was
turned back on (i.e. the number of times that the voltage dropped to 0 or
was restored). (This example assumes that sampling the voltage every 15
minutes is sufficient. Because power failures can last less than 15 minutes,
you’d typically want more frequent samples, or you’d want to treat the
query results as an approximation.)

> Create and load the table:
>
> ```
> CREATE TABLE voltage_readings (
>     site_ID INTEGER, -- which refrigerator the measurement was taken in.
>     ts TIMESTAMP,  -- the time at which the temperature was measured.
>     VOLTAGE FLOAT
>     );
> INSERT INTO voltage_readings (site_ID, ts, voltage) VALUES
>     (1, '2019-10-30 13:00:00', 120),
>     (1, '2019-10-30 13:15:00', 120),
>     (1, '2019-10-30 13:30:00',   0),
>     (1, '2019-10-30 13:45:00',   0),
>     (1, '2019-10-30 14:00:00',   0),
>     (1, '2019-10-30 14:15:00',   0),
>     (1, '2019-10-30 14:30:00', 120)
>     ;
> ```
>
> Copy
>
> This shows the samples for which the voltage was zero, whether or not those
> zero-volt events were part of the same power failure or different power failures.
>
> ```
> SELECT site_ID, ts, voltage
>     FROM voltage_readings
>     WHERE voltage = 0
>     ORDER BY ts;
> +---------+-------------------------+---------+
> | SITE_ID | TS                      | VOLTAGE |
> |---------+-------------------------+---------|
> |       1 | 2019-10-30 13:30:00.000 |       0 |
> |       1 | 2019-10-30 13:45:00.000 |       0 |
> |       1 | 2019-10-30 14:00:00.000 |       0 |
> |       1 | 2019-10-30 14:15:00.000 |       0 |
> +---------+-------------------------+---------+
> ```
>
> Copy
>
> This shows the samples, along with a column indicating whether the voltage
> changed:
>
> ```
> SELECT
>       site_ID,
>       ts,
>       voltage,
>       CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
>     FROM voltage_readings;
> +---------+-------------------------+---------+---------------+
> | SITE_ID | TS                      | VOLTAGE | POWER_CHANGES |
> |---------+-------------------------+---------+---------------|
> |       1 | 2019-10-30 13:00:00.000 |     120 |             0 |
> |       1 | 2019-10-30 13:15:00.000 |     120 |             0 |
> |       1 | 2019-10-30 13:30:00.000 |       0 |             1 |
> |       1 | 2019-10-30 13:45:00.000 |       0 |             1 |
> |       1 | 2019-10-30 14:00:00.000 |       0 |             1 |
> |       1 | 2019-10-30 14:15:00.000 |       0 |             1 |
> |       1 | 2019-10-30 14:30:00.000 |     120 |             2 |
> +---------+-------------------------+---------+---------------+
> ```
>
> Copy
>
> This shows the times that the power stopped and restarted:
>
> ```
> WITH power_change_events AS
>     (
>     SELECT
>       site_ID,
>       ts,
>       voltage,
>       CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
>     FROM voltage_readings
>     )
> SELECT
>       site_ID,
>       MIN(ts),
>       voltage,
>       power_changes
>     FROM power_change_events
>     GROUP BY site_ID, power_changes, voltage
>     ORDER BY 2
>     ;
> +---------+-------------------------+---------+---------------+
> | SITE_ID | MIN(TS)                 | VOLTAGE | POWER_CHANGES |
> |---------+-------------------------+---------+---------------|
> |       1 | 2019-10-30 13:00:00.000 |     120 |             0 |
> |       1 | 2019-10-30 13:30:00.000 |       0 |             1 |
> |       1 | 2019-10-30 14:30:00.000 |     120 |             2 |
> +---------+-------------------------+---------+---------------+
> ```
>
> Copy
>
> This shows how many times the power stopped and restarted:
>
> ```
> WITH power_change_events AS
>     (
>     SELECT
>           site_ID,
>           CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
>         FROM voltage_readings
>     )
> SELECT MAX(power_changes) 
>     FROM power_change_events
>     GROUP BY site_ID
>     ;
> +--------------------+
> | MAX(POWER_CHANGES) |
> |--------------------|
> |                  2 |
> +--------------------+
> ```
>
> Copy

This example illustrates that:

* The change number within a partition changes each time the specified value changes.
* NULL values are not considered a new or changed value.
* The change count starts over at 0 for each partition.

  Create and load the table:

  ```
  CREATE TABLE table1 (province VARCHAR, o_col INTEGER, o2_col INTEGER);
  INSERT INTO table1 (province, o_col, o2_col) VALUES
      ('Alberta',    0, 10),
      ('Alberta',    0, 10),
      ('Alberta',   13, 10),
      ('Alberta',   13, 11),
      ('Alberta',   14, 11),
      ('Alberta',   15, 12),
      ('Alberta', NULL, NULL),
      ('Manitoba',    30, 30);
  ```

  Copy

  Query the table:

  ```
  SELECT province, o_col,
        CONDITIONAL_CHANGE_EVENT(o_col) 
          OVER (PARTITION BY province ORDER BY o_col) 
            AS change_event
      FROM table1
      ORDER BY province, o_col
      ;
  +----------+-------+--------------+
  | PROVINCE | O_COL | CHANGE_EVENT |
  |----------+-------+--------------|
  | Alberta  |     0 |            0 |
  | Alberta  |     0 |            0 |
  | Alberta  |    13 |            1 |
  | Alberta  |    13 |            1 |
  | Alberta  |    14 |            2 |
  | Alberta  |    15 |            3 |
  | Alberta  |  NULL |            3 |
  | Manitoba |    30 |            0 |
  +----------+-------+--------------+
  ```

  Copy

The next example shows that:

* `expr1` can be an expression other than a column. This query uses the expression `o_col < 15`,
  and the output of the query shows when the value in o\_col changes from a value less than 15 to
  a value greater than or equal to 15.
* `expr3` does not need to match `expr1`. In other words, the expression in the ORDER BY
  sub-clause of the OVER clause does not need to match the expression in the CONDITIONAL\_CHANGE\_EVENT function.

  Query the table:

  ```
  SELECT province, o_col,
        'o_col < 15' AS condition,
        CONDITIONAL_CHANGE_EVENT(o_col) 
          OVER (PARTITION BY province ORDER BY o_col) 
            AS change_event,
        CONDITIONAL_CHANGE_EVENT(o_col < 15) 
          OVER (PARTITION BY province ORDER BY o_col) 
            AS change_event_2
      FROM table1
      ORDER BY province, o_col
      ;
  +----------+-------+------------+--------------+----------------+
  | PROVINCE | O_COL | CONDITION  | CHANGE_EVENT | CHANGE_EVENT_2 |
  |----------+-------+------------+--------------+----------------|
  | Alberta  |     0 | o_col < 15 |            0 |              0 |
  | Alberta  |     0 | o_col < 15 |            0 |              0 |
  | Alberta  |    13 | o_col < 15 |            1 |              0 |
  | Alberta  |    13 | o_col < 15 |            1 |              0 |
  | Alberta  |    14 | o_col < 15 |            2 |              0 |
  | Alberta  |    15 | o_col < 15 |            3 |              1 |
  | Alberta  |  NULL | o_col < 15 |            3 |              1 |
  | Manitoba |    30 | o_col < 15 |            0 |              0 |
  +----------+-------+------------+--------------+----------------+
  ```

  Copy

The next example compares CONDITIONAL\_CHANGE\_EVENT and CONDITIONAL\_TRUE\_EVENT:

> ```
> SELECT province, o_col,
>       CONDITIONAL_CHANGE_EVENT(o_col) 
>         OVER (PARTITION BY province ORDER BY o_col) 
>           AS change_event,
>       CONDITIONAL_TRUE_EVENT(o_col) 
>         OVER (PARTITION BY province ORDER BY o_col) 
>           AS true_event
>     FROM table1
>     ORDER BY province, o_col
>     ;
> +----------+-------+--------------+------------+
> | PROVINCE | O_COL | CHANGE_EVENT | TRUE_EVENT |
> |----------+-------+--------------+------------|
> | Alberta  |     0 |            0 |          0 |
> | Alberta  |     0 |            0 |          0 |
> | Alberta  |    13 |            1 |          1 |
> | Alberta  |    13 |            1 |          2 |
> | Alberta  |    14 |            2 |          3 |
> | Alberta  |    15 |            3 |          4 |
> | Alberta  |  NULL |            3 |          4 |
> | Manitoba |    30 |            0 |          1 |
> +----------+-------+--------------+------------+
> ```
>
> Copy

This example also compares CONDITIONAL\_CHANGE\_EVENT and CONDITIONAL\_TRUE\_EVENT:

> ```
> CREATE TABLE borrowers (
>     name VARCHAR,
>     status_date DATE,
>     late_balance NUMERIC(11, 2),
>     thirty_day_late_balance NUMERIC(11, 2)
>     );
> INSERT INTO borrowers (name, status_date, late_balance, thirty_day_late_balance) VALUES
>
>     -- Pays late frequently, but catches back up rather than falling further
>     -- behind.
>     ('Geoffrey Flake', '2018-01-01'::DATE,    0.0,    0.0),
>     ('Geoffrey Flake', '2018-02-01'::DATE, 1000.0,    0.0),
>     ('Geoffrey Flake', '2018-03-01'::DATE, 2000.0, 1000.0),
>     ('Geoffrey Flake', '2018-04-01'::DATE,    0.0,    0.0),
>     ('Geoffrey Flake', '2018-05-01'::DATE, 1000.0,    0.0),
>     ('Geoffrey Flake', '2018-06-01'::DATE, 2000.0, 1000.0),
>     ('Geoffrey Flake', '2018-07-01'::DATE,    0.0,    0.0),
>     ('Geoffrey Flake', '2018-08-01'::DATE,    0.0,    0.0),
>
>     -- Keeps falling further behind.
>     ('Cy Dismal', '2018-01-01'::DATE,    0.0,    0.0),
>     ('Cy Dismal', '2018-02-01'::DATE,    0.0,    0.0),
>     ('Cy Dismal', '2018-03-01'::DATE, 1000.0,    0.0),
>     ('Cy Dismal', '2018-04-01'::DATE, 2000.0, 1000.0),
>     ('Cy Dismal', '2018-05-01'::DATE, 3000.0, 2000.0),
>     ('Cy Dismal', '2018-06-01'::DATE, 4000.0, 3000.0),
>     ('Cy Dismal', '2018-07-01'::DATE, 5000.0, 4000.0),
>     ('Cy Dismal', '2018-08-01'::DATE, 6000.0, 5000.0),
>
>     -- Fell behind and isn't catching up, but isn't falling further and 
>     -- further behind. Essentially, this person just 'failed' once.
>     ('Leslie Safer', '2018-01-01'::DATE,    0.0,    0.0),
>     ('Leslie Safer', '2018-02-01'::DATE,    0.0,    0.0),
>     ('Leslie Safer', '2018-03-01'::DATE, 1000.0, 1000.0),
>     ('Leslie Safer', '2018-04-01'::DATE, 2000.0, 1000.0),
>     ('Leslie Safer', '2018-05-01'::DATE, 2000.0, 1000.0),
>     ('Leslie Safer', '2018-06-01'::DATE, 2000.0, 1000.0),
>     ('Leslie Safer', '2018-07-01'::DATE, 2000.0, 1000.0),
>     ('Leslie Safer', '2018-08-01'::DATE, 2000.0, 1000.0),
>
>     -- Always pays on time and in full.
>     ('Ida Idyll', '2018-01-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-02-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-03-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-04-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-05-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-06-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-07-01'::DATE,    0.0,    0.0),
>     ('Ida Idyll', '2018-08-01'::DATE,    0.0,    0.0)
>
>     ;
> ```
>
> Copy
>
> ```
> SELECT name, status_date, late_balance AS "OVERDUE", 
>         thirty_day_late_balance AS "30 DAYS OVERDUE",
>         CONDITIONAL_CHANGE_EVENT(thirty_day_late_balance) 
>           OVER (PARTITION BY name ORDER BY status_date) AS change_event_cnt,
>         CONDITIONAL_TRUE_EVENT(thirty_day_late_balance) 
>           OVER (PARTITION BY name ORDER BY status_date) AS true_cnt
>     FROM borrowers
>     ORDER BY name, status_date
>     ;
> +----------------+-------------+---------+-----------------+------------------+----------+
> | NAME           | STATUS_DATE | OVERDUE | 30 DAYS OVERDUE | CHANGE_EVENT_CNT | TRUE_CNT |
> |----------------+-------------+---------+-----------------+------------------+----------|
> | Cy Dismal      | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
> | Cy Dismal      | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
> | Cy Dismal      | 2018-03-01  | 1000.00 |            0.00 |                0 |        0 |
> | Cy Dismal      | 2018-04-01  | 2000.00 |         1000.00 |                1 |        1 |
> | Cy Dismal      | 2018-05-01  | 3000.00 |         2000.00 |                2 |        2 |
> | Cy Dismal      | 2018-06-01  | 4000.00 |         3000.00 |                3 |        3 |
> | Cy Dismal      | 2018-07-01  | 5000.00 |         4000.00 |                4 |        4 |
> | Cy Dismal      | 2018-08-01  | 6000.00 |         5000.00 |                5 |        5 |
> | Geoffrey Flake | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
> | Geoffrey Flake | 2018-02-01  | 1000.00 |            0.00 |                0 |        0 |
> | Geoffrey Flake | 2018-03-01  | 2000.00 |         1000.00 |                1 |        1 |
> | Geoffrey Flake | 2018-04-01  |    0.00 |            0.00 |                2 |        1 |
> | Geoffrey Flake | 2018-05-01  | 1000.00 |            0.00 |                2 |        1 |
> | Geoffrey Flake | 2018-06-01  | 2000.00 |         1000.00 |                3 |        2 |
> | Geoffrey Flake | 2018-07-01  |    0.00 |            0.00 |                4 |        2 |
> | Geoffrey Flake | 2018-08-01  |    0.00 |            0.00 |                4 |        2 |
> | Ida Idyll      | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-03-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-04-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-05-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-06-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-07-01  |    0.00 |            0.00 |                0 |        0 |
> | Ida Idyll      | 2018-08-01  |    0.00 |            0.00 |                0 |        0 |
> | Leslie Safer   | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
> | Leslie Safer   | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
> | Leslie Safer   | 2018-03-01  | 1000.00 |         1000.00 |                1 |        1 |
> | Leslie Safer   | 2018-04-01  | 2000.00 |         1000.00 |                1 |        2 |
> | Leslie Safer   | 2018-05-01  | 2000.00 |         1000.00 |                1 |        3 |
> | Leslie Safer   | 2018-06-01  | 2000.00 |         1000.00 |                1 |        4 |
> | Leslie Safer   | 2018-07-01  | 2000.00 |         1000.00 |                1 |        5 |
> | Leslie Safer   | 2018-08-01  | 2000.00 |         1000.00 |                1 |        6 |
> +----------------+-------------+---------+-----------------+------------------+----------+
> ```
>
> Copy

Here is a more extensive example:

```
CREATE OR REPLACE TABLE tbl
(p int, o int, i int, r int, s varchar(100));

INSERT INTO tbl VALUES
(100,1,1,70,'seventy'),(100,2,2,30, 'thirty'),(100,3,3,40,'fourty'),(100,4,NULL,90,'ninety'),(100,5,5,50,'fifty'),(100,6,6,30,'thirty'),
(200,7,7,40,'fourty'),(200,8,NULL,NULL,'n_u_l_l'),(200,9,NULL,NULL,'n_u_l_l'),(200,10,10,20,'twenty'),(200,11,NULL,90,'ninety'),
(300,12,12,30,'thirty'),
(400,13,NULL,20,'twenty');

SELECT * FROM tbl ORDER BY p, o, i;

+-----+----+--------+--------+---------+
|  P  | O  |   I    |   R    |    S    |
+-----+----+--------+--------+---------+
| 100 | 1  | 1      | 70     | seventy |
| 100 | 2  | 2      | 30     | thirty  |
| 100 | 3  | 3      | 40     | fourty  |
| 100 | 4  | [NULL] | 90     | ninety  |
| 100 | 5  | 5      | 50     | fifty   |
| 100 | 6  | 6      | 30     | thirty  |
| 200 | 7  | 7      | 40     | fourty  |
| 200 | 8  | [NULL] | [NULL] | n_u_l_l |
| 200 | 9  | [NULL] | [NULL] | n_u_l_l |
| 200 | 10 | 10     | 20     | twenty  |
| 200 | 11 | [NULL] | 90     | ninety  |
| 300 | 12 | 12     | 30     | thirty  |
| 400 | 13 | [NULL] | 20     | twenty  |
+-----+----+--------+--------+---------+

SELECT p, o, CONDITIONAL_CHANGE_EVENT(o) OVER (PARTITION BY p ORDER BY o) FROM tbl ORDER BY p, o;

+-----+----+--------------------------------------------------------------+
|   P |  O | CONDITIONAL_CHANGE_EVENT(O) OVER (PARTITION BY P ORDER BY O) |
|-----+----+--------------------------------------------------------------|
| 100 |  1 |                                                            0 |
| 100 |  2 |                                                            1 |
| 100 |  3 |                                                            2 |
| 100 |  4 |                                                            3 |
| 100 |  5 |                                                            4 |
| 100 |  6 |                                                            5 |
| 200 |  7 |                                                            0 |
| 200 |  8 |                                                            1 |
| 200 |  9 |                                                            2 |
| 200 | 10 |                                                            3 |
| 200 | 11 |                                                            4 |
| 300 | 12 |                                                            0 |
| 400 | 13 |                                                            0 |
+-----+----+--------------------------------------------------------------+
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)