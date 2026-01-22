---
auto_generated: true
description: Table functions , Semi-structured and structured data functions (Extraction)
last_scraped: '2026-01-14T16:55:18.101350+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/flatten
title: FLATTEN | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Table](../functions-table.md)FLATTEN

Categories:
:   [Table functions](../functions-table) , [Semi-structured and structured data functions](../functions-semistructured) (Extraction)

# FLATTEN[¶](#flatten "Link to this heading")

Flattens (explodes) compound values into multiple rows.

FLATTEN is a table function that takes a VARIANT, OBJECT, or ARRAY column and produces a lateral view (that is, an inline view that contains
correlations to other tables that precede it in the [FROM](../constructs/from) clause).

FLATTEN can be used to convert semi-structured data to a relational representation.

## Syntax[¶](#syntax "Link to this heading")

```
FLATTEN( INPUT => <expr> [ , PATH => <constant_expr> ]
                         [ , OUTER => TRUE | FALSE ]
                         [ , RECURSIVE => TRUE | FALSE ]
                         [ , MODE => 'OBJECT' | 'ARRAY' | 'BOTH' ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`INPUT => expr`
:   The expression that will be flattened into rows. The expression must be of data type VARIANT, OBJECT, or ARRAY.

**Optional:**

`PATH => constant_expr`
:   The path to the element within a VARIANT data structure that needs to be flattened. Can be a zero-length string (that is, an empty path) if the
    outermost element is to be flattened.

    Default: Zero-length string (empty path)

`OUTER => TRUE | FALSE`
:   * If `FALSE`, any input rows that cannot be expanded, either because they cannot be accessed in the path or because they have zero fields or entries, are completely omitted from the output.
    * If `TRUE`, exactly one row is generated for zero-row expansions (with NULL in the KEY, INDEX, and VALUE columns).

    Default: `FALSE`

    Note

    A zero-row expansion of an empty compound displays NULL in the THIS output column, distinguishing it from an attempt to expand a non-existing or wrong kind of compound.

`RECURSIVE => TRUE | FALSE`
:   * If `FALSE`, only the element referenced by `PATH` is expanded.
    * If `TRUE`, the expansion is performed for all sub-elements recursively.

    Default: `FALSE`

`MODE => 'OBJECT' | 'ARRAY' | 'BOTH'`
:   Specifies whether only objects, arrays, or both should be flattened.

    Default: `BOTH`

## Output[¶](#output "Link to this heading")

The returned rows consist of a fixed set of columns:

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
```

SEQ:
:   A unique sequence number associated with the input record; the sequence is not guaranteed to be gap-free or ordered in any particular way.

KEY:
:   For maps or objects, this column contains the key to the exploded value.

PATH:
:   The path to the element within a data structure that needs to be flattened.

INDEX:
:   The index of the element, if it is an array; otherwise NULL.

VALUE:
:   The value of the element of the flattened array/object.

THIS:
:   The element being flattened (useful in recursive flattening).

Note

The columns of the original (correlated) table that was used as the source of data for FLATTEN are also accessible. If a single row from the original table resulted in multiple rows in the flattened view, the values in this input row are replicated to match the number of rows produced by FLATTEN.

## Usage notes[¶](#usage-notes "Link to this heading")

For information about using this function with [structured types](../data-types-structured), see
[Using the FLATTEN function with values of structured types](../data-types-structured.html#label-structured-types-working-flatten).

## Examples[¶](#examples "Link to this heading")

See also [Example: Using a lateral join with the FLATTEN table function](../../user-guide/lateral-join-using.html#label-lateral-flatten-example) and [Using FLATTEN to Filter the Results in a WHERE Clause](../../user-guide/querying-semistructured.html#label-using-flatten-where-clause).

The following simple example flattens one record (note that the middle element of the array is missing):

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[1, ,77]'))) f;
```

Copy

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
|   1 | NULL | [0]  |     0 |     1 | [    |
|     |      |      |       |       |   1, |
|     |      |      |       |       |   ,  |
|     |      |      |       |       |   77 |
|     |      |      |       |       | ]    |
|   1 | NULL | [2]  |     2 |    77 | [    |
|     |      |      |       |       |   1, |
|     |      |      |       |       |   ,  |
|     |      |      |       |       |   77 |
|     |      |      |       |       | ]    |
+-----+------+------+-------+-------+------+
```

The next two queries show the effect of the PATH parameter:

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88]}'), OUTER => TRUE)) f;
```

Copy

```
+-----+-----+------+-------+-------+-----------+
| SEQ | KEY | PATH | INDEX | VALUE | THIS      |
|-----+-----+------+-------+-------+-----------|
|     |     |      |       |       |   "a": 1, |
|     |     |      |       |       |   "b": [  |
|     |     |      |       |       |     77,   |
|     |     |      |       |       |     88    |
|     |     |      |       |       |   ]       |
|     |     |      |       |       | }         |
|   1 | b   | b    |  NULL | [     | {         |
|     |     |      |       |   77, |   "a": 1, |
|     |     |      |       |   88  |   "b": [  |
|     |     |      |       | ]     |     77,   |
|     |     |      |       |       |     88    |
|     |     |      |       |       |   ]       |
|     |     |      |       |       | }         |
+-----+-----+------+-------+-------+-----------+
```

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88]}'), PATH => 'b')) f;
```

Copy

```
+-----+------+------+-------+-------+-------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS  |
|-----+------+------+-------+-------+-------|
|   1 | NULL | b[0] |     0 |    77 | [     |
|     |      |      |       |       |   77, |
|     |      |      |       |       |   88  |
|     |      |      |       |       | ]     |
|   1 | NULL | b[1] |     1 |    88 | [     |
|     |      |      |       |       |   77, |
|     |      |      |       |       |   88  |
|     |      |      |       |       | ]     |
+-----+------+------+-------+-------+-------+
```

The next two queries show the effect of the OUTER parameter:

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[]'))) f;
```

Copy

```
+-----+-----+------+-------+-------+------+
| SEQ | KEY | PATH | INDEX | VALUE | THIS |
|-----+-----+------+-------+-------+------|
+-----+-----+------+-------+-------+------+
```

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[]'), OUTER => TRUE)) f;
```

Copy

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
|   1 | NULL |      |  NULL |  NULL | []   |
+-----+------+------+-------+-------+------+
```

The next two queries show the effect of the RECURSIVE parameter:

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'))) f;
```

Copy

```
+-----+-----+------+-------+------------+--------------+
| SEQ | KEY | PATH | INDEX | VALUE      | THIS         |
|-----+-----+------+-------+------------+--------------|
|   1 | a   | a    |  NULL | 1          | {            |
|     |     |      |       |            |   "a": 1,    |
|     |     |      |       |            |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | b   | b    |  NULL | [          | {            |
|     |     |      |       |   77,      |   "a": 1,    |
|     |     |      |       |   88       |   "b": [     |
|     |     |      |       | ]          |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | c   | c    |  NULL | {          | {            |
|     |     |      |       |   "d": "X" |   "a": 1,    |
|     |     |      |       | }          |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
+-----+-----+------+-------+------------+--------------+
```

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'),
                            RECURSIVE => TRUE )) f;
```

Copy

```
+-----+------+------+-------+------------+--------------+
| SEQ | KEY  | PATH | INDEX | VALUE      | THIS         |
|-----+------+------+-------+------------+--------------|
|   1 | a    | a    |  NULL | 1          | {            |
|     |      |      |       |            |   "a": 1,    |
|     |      |      |       |            |   "b": [     |
|     |      |      |       |            |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | b    | b    |  NULL | [          | {            |
|     |      |      |       |   77,      |   "a": 1,    |
|     |      |      |       |   88       |   "b": [     |
|     |      |      |       | ]          |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | NULL | b[0] |     0 | 77         | [            |
|     |      |      |       |            |   77,        |
|     |      |      |       |            |   88         |
|     |      |      |       |            | ]            |
|   1 | NULL | b[1] |     1 | 88         | [            |
|     |      |      |       |            |   77,        |
|     |      |      |       |            |   88         |
|     |      |      |       |            | ]            |
|   1 | c    | c    |  NULL | {          | {            |
|     |      |      |       |   "d": "X" |   "a": 1,    |
|     |      |      |       | }          |   "b": [     |
|     |      |      |       |            |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | d    | c.d  |  NULL | "X"        | {            |
|     |      |      |       |            |   "d": "X"   |
|     |      |      |       |            | }            |
+-----+------+------+-------+------------+--------------+
```

The following example shows the effect of the MODE parameter:

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'),
                            RECURSIVE => TRUE, MODE => 'OBJECT' )) f;
```

Copy

```
+-----+-----+------+-------+------------+--------------+
| SEQ | KEY | PATH | INDEX | VALUE      | THIS         |
|-----+-----+------+-------+------------+--------------|
|   1 | a   | a    |  NULL | 1          | {            |
|     |     |      |       |            |   "a": 1,    |
|     |     |      |       |            |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | b   | b    |  NULL | [          | {            |
|     |     |      |       |   77,      |   "a": 1,    |
|     |     |      |       |   88       |   "b": [     |
|     |     |      |       | ]          |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | c   | c    |  NULL | {          | {            |
|     |     |      |       |   "d": "X" |   "a": 1,    |
|     |     |      |       | }          |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | d   | c.d  |  NULL | "X"        | {            |
|     |     |      |       |            |   "d": "X"   |
|     |     |      |       |            | }            |
+-----+-----+------+-------+------------+--------------+
```

The following example explodes an array that is nested within another array. Create the following table:

```
CREATE OR REPLACE TABLE persons AS
  SELECT column1 AS id, PARSE_JSON(column2) as c
    FROM values
      (12712555,
       '{ name:  { first: "John", last: "Smith"},
         contact: [
         { business:[
           { type: "phone", content:"555-1234" },
           { type: "email", content:"j.smith@example.com" } ] } ] }'),
      (98127771,
       '{ name:  { first: "Jane", last: "Doe"},
         contact: [
         { business:[
           { type: "phone", content:"555-1236" },
           { type: "email", content:"j.doe@example.com" } ] } ] }') v;
```

Copy

Note the multiple instances of LATERAL FLATTEN in the FROM clause of the following query. Each LATERAL view is
based on the previous one to refer to elements in multiple levels of arrays.

```
SELECT id as "ID",
    f.value AS "Contact",
    f1.value:type AS "Type",
    f1.value:content AS "Details"
  FROM persons p,
    LATERAL FLATTEN(INPUT => p.c, PATH => 'contact') f,
    LATERAL FLATTEN(INPUT => f.value:business) f1;
```

Copy

```
+----------+-----------------------------------------+---------+-----------------------+
|       ID | Contact                                 | Type    | Details               |
|----------+-----------------------------------------+---------+-----------------------|
| 12712555 | {                                       | "phone" | "555-1234"            |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1234",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.smith@example.com", |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 12712555 | {                                       | "email" | "j.smith@example.com" |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1234",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.smith@example.com", |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 98127771 | {                                       | "phone" | "555-1236"            |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1236",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.doe@example.com",   |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 98127771 | {                                       | "email" | "j.doe@example.com"   |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1236",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.doe@example.com",   |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
+----------+-----------------------------------------+---------+-----------------------+
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
4. [Usage notes](#usage-notes)
5. [Examples](#examples)