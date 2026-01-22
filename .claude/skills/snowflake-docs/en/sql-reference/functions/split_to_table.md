---
auto_generated: true
description: String & binary functions (General) , Table functions
last_scraped: '2026-01-14T16:57:17.323008+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/split_to_table
title: SPLIT_TO_TABLE | Snowflake Documentation
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

     + Data loading
     + [INFER\_SCHEMA](infer_schema.md)
     + [VALIDATE](validate.md)
     + Data generation
     + [GENERATOR](generator.md)
     + Data conversion
     + [SPLIT\_TO\_TABLE](split_to_table.md)
     + [STRTOK\_SPLIT\_TO\_TABLE](strtok_split_to_table.md)
     + Differential privacy
     + [CUMULATIVE\_PRIVACY\_LOSSES](cumulative_privacy_losses.md)
     + ML-powered analysis
     + Object modeling
     + [GET\_OBJECT\_REFERENCES](get_object_references.md)
     + Parameterized queries
     + [TO\_QUERY](to_query.md)
     + Semi-structured queries
     + [FLATTEN](flatten.md)
     + Query results
     + [RESULT\_SCAN](result_scan.md)
     + Query profile
     + [GET\_QUERY\_OPERATOR\_STATS](get_query_operator_stats.md)
     + User login
     + [LOGIN\_HISTORY](login_history.md)
     + [LOGIN\_HISTORY\_BY\_USER](login_history.md)
     + Queries
     + [QUERY\_HISTORY](query_history.md)
     + [QUERY\_HISTORY\_BY\_\*](query_history.md)
     + [QUERY\_ACCELERATION\_HISTORY](query_acceleration_history.md)
     + Warehouse & storage usage
     + [DATABASE\_STORAGE\_USAGE\_HISTORY](database_storage_usage_history.md)
     + [WAREHOUSE\_LOAD\_HISTORY](warehouse_load_history.md)
     + [WAREHOUSE\_METERING\_HISTORY](warehouse_metering_history.md)
     + [STAGE\_STORAGE\_USAGE\_HISTORY](stage_storage_usage_history.md)
     + Storage lifecycle policies
     + [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](storage_lifecycle_policy_history.md)
     + Data Quality
     + [DATA\_METRIC\_FUNCTION\_EXPECTATIONS](data_metric_function_expectations.md)
     + [DATA\_METRIC\_FUNCTION\_REFERENCES](data_metric_function_references.md)
     + [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS](data_quality_monitoring_expectation_status.md)
     + [DATA\_QUALITY\_MONITORING\_RESULTS](data_quality_monitoring_results.md)
     + [SYSTEM$DATA\_METRIC\_SCAN](system_data_metric_scan.md)
     + Data Lineage
     + [GET\_LINEAGE](get_lineage-snowflake-core.md)
     + Network security
     + [NETWORK\_RULE\_REFERENCES](network_rule_references.md)
     + Column & Row-level Security
     + [POLICY\_REFERENCES](policy_references.md)
     + Object tagging
     + [TAG\_REFERENCES](tag_references.md)
     + [TAG\_REFERENCES\_ALL\_COLUMNS](tag_references_all_columns.md)
     + [TAG\_REFERENCES\_WITH\_LINEAGE](tag_references_with_lineage.md)
     + Account replication
     + [REPLICATION\_GROUP\_DANGLING\_REFERENCES](replication_group_dangling_references.md)
     + [REPLICATION\_GROUP\_REFRESH\_HISTORY](replication_group_refresh_history.md)
     + [REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](replication_group_refresh_history.md)
     + [REPLICATION\_GROUP\_REFRESH\_PROGRESS](replication_group_refresh_progress.md)
     + [REPLICATION\_GROUP\_REFRESH\_PROCESS\_ALL](replication_group_refresh_progress.md)
     + [REPLICATION\_GROUP\_REFRESH\_PROCESS\_BY\_JOB](replication_group_refresh_progress.md)
     + [REPLICATION\_GROUP\_USAGE\_HISTORY](replication_group_usage_history.md)
     + Alerts
     + [ALERT\_HISTORY](alert_history.md)
     + [SERVERLESS\_ALERT\_HISTORY](serverless_alert_history.md)
     + Bind variables
     + [BIND\_VALUES](bind_values.md)
     + Database replication
     + [DATABASE\_REFRESH\_HISTORY](database_refresh_history.md)
     + [DATABASE\_REFRESH\_PROCESS](database_refresh_progress.md)
     + [DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](database_refresh_progress.md)
     + [DATABASE\_REPLICATION\_USAGE\_HISTORY](database_replication_usage_history.md)
     + [REPLICATION\_USAGE\_HISTORY](replication_usage_history.md)
     + Data loading & transfer
     + [COPY\_HISTORY](copy_history.md)
     + [DATA\_TRANSFER\_HISTORY](data_transfer_history.md)
     + [PIPE\_USAGE\_HISTORY](pipe_usage_history.md)
     + [STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY](stage_directory_file_registration_history.md)
     + [VALIDATE\_PIPE\_LOAD](validate_pipe_load.md)
     + Data clustering (within tables)
     + [AUTOMATIC\_CLUSTERING\_HISTORY](automatic_clustering_history.md)
     + dbt Projects on Snowflake
     + [DBT\_PROJECT\_EXECUTION\_HISTORY](dbt_project_execution_history.md)
     + Dynamic tables
     + [DYNAMIC\_TABLES](dynamic_tables.md)
     + [DYNAMIC\_TABLE\_GRAPH\_HISTORY](dynamic_table_graph_history.md)
     + [DYNAMIC\_TABLE\_REFRESH\_HISTORY](dynamic_table_refresh_history.md)
     + External functions
     + [EXTERNAL\_FUNCTIONS\_HISTORY](external_functions_history.md)
     + External tables
     + [AUTO\_REFRESH\_REGISTRATION\_HISTORY](auto_refresh_registration_history.md)
     + [EXTERNAL\_TABLE\_FILES](external_table_files.md)
     + [EXTERNAL\_TABLE\_FILE\_REGISTRATION\_HISTORY](external_table_registration_history.md)
     + Iceberg tables
     + [ICEBERG\_TABLE\_FILES](iceberg_table_files.md)
     + [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](iceberg_table_snapshot_refresh_history.md)
     + Listing functions
     + [AVAILABLE\_LISTING\_REFRESH\_HISTORY](available_listing_refresh_history.md)
     + [LISTING\_REFRESH\_HISTORY](listing_refresh_history.md)
     + Materialized views maintenance
     + [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](materialized_view_refresh_history.md)
     + Machine learning
     + [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](online-feature-table-refresh-history.md)
     + Notifications
     + [NOTIFICATION\_HISTORY](notification_history.md)
     + SCIM maintenance
     + [REST\_EVENT\_HISTORY](rest_event_history.md)
     + Search optimization maintenance
     + [SEARCH\_OPTIMIZATION\_HISTORY](search_optimization_history.md)
     + Streams
     + [SYSTEM$STREAM\_BACKLOG](system_stream_backlog.md)
     + Tasks
     + [COMPLETE\_TASK\_GRAPHS](complete_task_graphs.md)
     + [CURRENT\_TASK\_GRAPHS](current_task_graphs.md)
     + [SERVERLESS\_TASK\_HISTORY](serverless_task_history.md)
     + [TASK\_DEPENDENTS](task_dependents.md)
     + [TASK\_HISTORY](task_history.md)
     + Cortex Search
     + [CORTEX\_SEARCH\_DATA\_SCAN](cortex_search_data_scan.md)
     + Contacts
     + [GET\_CONTACTS](get_contacts.md)
     + Snowpark Container Services
     + [GET\_JOB\_HISTORY](get_job_history.md)
     + [SPCS\_GET\_EVENTS](spcs_get_events.md)
     + [SPCS\_GET\_LOGS](spcs_get_logs.md)
     + [SPCS\_GET\_METRICS](spcs_get_metrics.md)
     + Native Apps
     + [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY](application_specification_status_history.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Table](../functions-table.md)SPLIT\_TO\_TABLE

Categories:
:   [String & binary functions](../functions-string) (General) , [Table functions](../functions-table)

# SPLIT\_TO\_TABLE[¶](#split-to-table "Link to this heading")

This table function splits a string (based on a specified delimiter) and flattens the results into rows.

See also:
:   [SPLIT](split)

## Syntax[¶](#syntax "Link to this heading")

```
SPLIT_TO_TABLE(<string>, <delimiter>)
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`string`
:   Text to be split.

`delimiter`
:   Text to split the string by.

## Output[¶](#output "Link to this heading")

This function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| SEQ | NUMBER | A unique sequence number associated with the input record. The sequence is not guaranteed to be gap-free or ordered. in any particular way. |
| INDEX | NUMBER | The one-based index of the element. |
| VALUE | VARCHAR | The value of the element of the flattened array. |

Note

The query can also access the columns of the original (correlated) table that served as the source of data for this function. If a single row
from the original table resulted in multiple rows in the flattened view, the values in this input row are replicated to match the number of
rows produced by this function.

## Examples[¶](#examples "Link to this heading")

Here is a simple example on constant input.

```
SELECT table1.value
  FROM TABLE(SPLIT_TO_TABLE('a.b', '.')) AS table1
  ORDER BY table1.value;
```

Copy

```
+-------+
| VALUE |
|-------|
| a     |
| b     |
+-------+
```

Create a table and insert data:

```
CREATE OR REPLACE TABLE splittable (v VARCHAR);
INSERT INTO splittable (v) VALUES ('a.b.c'), ('d'), ('');
SELECT * FROM splittable;
```

Copy

```
+-------+
| V     |
|-------|
| a.b.c |
| d     |
|       |
+-------+
```

You can use the [LATERAL](../constructs/join-lateral) keyword with the SPLIT\_TO\_TABLE function
so that the function executes on each row of the `splittable` table as a correlated table:

```
SELECT *
  FROM splittable, LATERAL SPLIT_TO_TABLE(splittable.v, '.')
  ORDER BY SEQ, INDEX;
```

Copy

```
+-------+-----+-------+-------+
| V     | SEQ | INDEX | VALUE |
|-------+-----+-------+-------|
| a.b.c |   1 |     1 | a     |
| a.b.c |   1 |     2 | b     |
| a.b.c |   1 |     3 | c     |
| d     |   2 |     1 | d     |
|       |   3 |     1 |       |
+-------+-----+-------+-------+
```

Create another table that contains authors in one column and some of their book titles in another column, separated
by commas:

```
CREATE OR REPLACE TABLE authors_books_test (author VARCHAR, titles VARCHAR);
INSERT INTO authors_books_test (author, titles) VALUES
  ('Nathaniel Hawthorne', 'The Scarlet Letter , The House of the Seven Gables,The Blithedale Romance'),
  ('Herman Melville', 'Moby Dick,The Confidence-Man');
SELECT * FROM authors_books_test;
```

Copy

```
+---------------------+---------------------------------------------------------------------------+
| AUTHOR              | TITLES                                                                    |
|---------------------+---------------------------------------------------------------------------|
| Nathaniel Hawthorne | The Scarlet Letter , The House of the Seven Gables,The Blithedale Romance |
| Herman Melville     | Moby Dick,The Confidence-Man                                              |
+---------------------+---------------------------------------------------------------------------+
```

Use the LATERAL keyword and the SPLIT\_TO\_TABLE function to run a query that returns a separate row for each title.
In addition, use the [TRIM](trim) function to remove leading and trailing spaces from the titles. Note that the
SELECT list includes the fixed `value` column that is returned by the function:

```
SELECT author, TRIM(value) AS title
  FROM authors_books_test, LATERAL SPLIT_TO_TABLE(titles, ',')
  ORDER BY author;
```

Copy

```
+---------------------+-------------------------------+
| AUTHOR              | TITLE                         |
|---------------------+-------------------------------|
| Herman Melville     | Moby Dick                     |
| Herman Melville     | The Confidence-Man            |
| Nathaniel Hawthorne | The Scarlet Letter            |
| Nathaniel Hawthorne | The House of the Seven Gables |
| Nathaniel Hawthorne | The Blithedale Romance        |
+---------------------+-------------------------------+
```

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
3. [Output](#output)
4. [Examples](#examples)