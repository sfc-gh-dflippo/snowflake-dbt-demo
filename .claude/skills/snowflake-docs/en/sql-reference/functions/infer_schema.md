---
auto_generated: true
description: Table functions
last_scraped: '2026-01-14T16:54:48.001204+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/infer_schema
title: INFER_SCHEMA | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Table](../functions-table.md)INFER\_SCHEMA

Categories:
:   [Table functions](../functions-table)

# INFER\_SCHEMA[¶](#infer-schema "Link to this heading")

Automatically detects the file metadata schema in a set of staged data files that contain semi-structured data and retrieves the column
definitions.

The [GENERATE\_COLUMN\_DESCRIPTION](generate_column_description) function builds on the INFER\_SCHEMA function output to simplify the
creation of new tables, external tables, or views (using the appropriate [CREATE <object>](../sql/create) command) based on the column
definitions of the staged files.

You can execute the [CREATE TABLE](../sql/create-table), [CREATE EXTERNAL TABLE](../sql/create-external-table), or [CREATE ICEBERG TABLE](../sql/create-iceberg-table)
command with the USING TEMPLATE clause to create a new table or external table with the column definitions derived from the
INFER\_SCHEMA function output.

Note

This function supports Apache Parquet, Apache Avro, ORC, JSON, and CSV files.

## Syntax[¶](#syntax "Link to this heading")

```
INFER_SCHEMA(
  LOCATION => '{ internalStage | externalStage }'
  , FILE_FORMAT => '<file_format_name>'
  , FILES => ( '<file_name>' [ , '<file_name>' ] [ , ... ] )
  , IGNORE_CASE => TRUE | FALSE
  , MAX_FILE_COUNT => <num>
  , MAX_RECORDS_PER_FILE => <num>
  , KIND => '<kind_name>'
)
```

Copy

Where:

> ```
> internalStage ::=
>     @[<namespace>.]<int_stage_name>[/<path>][/<filename>]
>   | @~[/<path>][/<filename>]
> ```
>
> Copy
>
> ```
> externalStage ::=
>   @[<namespace>.]<ext_stage_name>[/<path>][/<filename>]
> ```
>
> Copy

## Arguments[¶](#arguments "Link to this heading")

`LOCATION => '...'`
:   Name of the internal or external stage where the files are stored. Optionally include a path to one or more files in the cloud storage
    location; otherwise, the INFER\_SCHEMA function scans files in all subdirectories in the stage:

    |  |  |
    | --- | --- |
    | `@[namespace.]int_stage_name[/path][/filename]` | Files are in the specified named internal stage. |
    | `@[namespace.]ext_stage_name[/path][/filename]` | Files are in the specified named external stage. |
    | `@~[/path][/filename]` | Files are in the stage for the current user. |

    Note

    This SQL function supports named stages (internal or external) and user stages only. It does not support table stages.

`FILES => ( 'file_name' [ , 'file_name' ] [ , ... ] )`
:   Specifies a list of one or more files (separated by commas) in a set of staged files that contain semi-structured data. The files must already have been staged in either the Snowflake internal location or external location specified in the command. If any of the specified files cannot be found, the query will be aborted.

    The maximum number of files names that can be specified is 1000.

    > Note
    >
    > For external stages only (Amazon S3, Google Cloud Storage, or Microsoft Azure), the file path is set by concatenating the URL in the stage definition and the list of resolved file names.
    >
    > However, Snowflake doesn’t insert a separator implicitly between the path and file names. You must explicitly include a separator (`/`) either at the end of the URL in the stage
    > definition or at the beginning of each file name specified in this parameter.

`FILE_FORMAT => 'file_format_name'`
:   Name of the file format object that describes the data contained in the staged files. For more information, see
    [CREATE FILE FORMAT](../sql/create-file-format).

`IGNORE_CASE => TRUE | FALSE`
:   Specifies whether column names detected from stage files are treated as case sensitive. By default, the value is FALSE, which means that Snowflake preserves the case of alphabetic characters when retrieving column names. If you specify the value as TRUE, column names are treated as case-insensitive and all column names are retrieved as uppercase letters.

`MAX_FILE_COUNT => num`
:   Specifies the maximum number of files scanned from stage. This option is recommended for large number of files that have identical schema across files. This option cannot determine which files are scanned. If you want to scan specific files, use the `FILES` option instead.

`MAX_RECORDS_PER_FILE => num`
:   Specifies the maximum number of records scanned per file. This option only applies to CSV and JSON files. We recommend that you use this option for large files. This option might affect the accuracy of schema detection.

`KIND => 'kind_name'`
:   Specifies the kind of file metadata schema that can be scanned from the stage. By default, the value is `STANDARD`, which means that
    the file metadata schema that can be scanned from the stage is for Snowflake tables and the output is Snowflake data types. If you specify
    the value as `ICEBERG`, the schema is for Apache Iceberg tables and the output is Iceberg data types.

    Note

    If you’re inferring Parquet files to create Iceberg tables, we strongly recommend that you set `KIND => 'ICEBERG'`. Otherwise, the
    column definitions returned by the function might be incorrect.

## Output[¶](#output "Link to this heading")

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| COLUMN\_NAME | TEXT | Name of a column in the staged files. |
| TYPE | TEXT | Data type of the column. |
| NULLABLE | BOOLEAN | Specifies whether rows in the column can store NULL instead of a value. Currently, the inferred nullability of a column can apply to one data file but not others in the scanned set. |
| EXPRESSION | TEXT | Expression of the column in the format `$1:COLUMN_NAME::TYPE` (primarily for external tables). If IGNORE\_CASE is specified as TRUE, the expression of the column will be in the format `GET_IGNORE_CASE ($1, COLUMN_NAME)::TYPE`. |
| FILENAMES | TEXT | Names of the files that contain the column. |
| ORDER\_ID | NUMBER | Column order in the staged files. |

## Usage notes[¶](#usage-notes "Link to this heading")

* For CSV files, you can define column names by using the file format option `PARSE_HEADER = [ TRUE | FALSE ]`.

  > + If the option is set to TRUE, the first row headers will be used to determine column names.
  > + The default value FALSE will return column names as c\*, where \* is the position of the column. The SKIP\_HEADER option is not supported with PARSE\_HEADER = TRUE.
  > + The PARSE\_HEADER option isn’t supported for external tables.
* For both CSV and JSON files, the following file format options are currently not supported: DATE\_FORMAT, TIME\_FORMAT, and TIMESTAMP\_FORMAT.
* The JSON TRIM\_SPACE file format option is not supported.
* The scientific annotations (e.g. 1E2) in JSON files are retrieved as REAL data type.
* All the variations of timestamp data types are retrieved as TIMESTAMP\_NTZ without any time zone information.
* For both CSV and JSON files, all columns are identified as NULLABLE.
* For both `KIND => 'STANDARD'` and `KIND => 'ICEBERG'`, when the specified file in the stage contains nested data types, only the
  first level of nesting is supported; deeper levels aren’t supported.

## Examples[¶](#examples "Link to this heading")

### Snowflake column definitions[¶](#snowflake-column-definitions "Link to this heading")

Retrieve the Snowflake column definitions for Parquet files in the `mystage` stage:

```
-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
      , FILE_FORMAT=>'my_parquet_format'
      )
    );

+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| continent   | TEXT    | True     | $1:continent::TEXT  | geography/cities.parquet | 0        |
| country     | VARIANT | True     | $1:country::VARIANT | geography/cities.parquet | 1        |
| COUNTRY     | VARIANT | True     | $1:COUNTRY::VARIANT | geography/cities.parquet | 2        |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Copy

Similar to the previous example, but specify a single Parquet file in the `mystage` stage:

```
-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/geography/cities.parquet'
      , FILE_FORMAT=>'my_parquet_format'
      )
    );

+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| continent   | TEXT    | True     | $1:continent::TEXT  | geography/cities.parquet | 0        |
| country     | VARIANT | True     | $1:country::VARIANT | geography/cities.parquet | 1        |
| COUNTRY     | VARIANT | True     | $1:COUNTRY::VARIANT | geography/cities.parquet | 2        |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Copy

Retrieve the Snowflake column definitions for Parquet files in the `mystage` stage with IGNORE\_CASE specified as TRUE. In the returned output, all column names are retrieved as uppercase letters.

```
-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
      , FILE_FORMAT=>'my_parquet_format'
      , IGNORE_CASE=>TRUE
      )
    );

+-------------+---------+----------+----------------------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION                             | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+---------------------------------------------|----------+
| CONTINENT   | TEXT    | True     | GET_IGNORE_CASE ($1, CONTINENT)::TEXT  | geography/cities.parquet | 0        |
| COUNTRY     | VARIANT | True     | GET_IGNORE_CASE ($1, COUNTRY)::VARIANT | geography/cities.parquet | 1        |
+-------------+---------+----------+---------------------+---------------------------------------------+----------+
```

Copy

Retrieve the Snowflake column definitions for JSON files in the `mystage` stage:

```
-- Create a file format that sets the file type as JSON.
CREATE FILE FORMAT my_json_format
  TYPE = json;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/json/'
      , FILE_FORMAT=>'my_json_format'
      )
    );

+-------------+---------------+----------+---------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE          | NULLABLE | EXPRESSION                | FILENAMES                | ORDER_ID |
|-------------+---------------+----------+---------------------------+--------------------------|----------+
| col_bool    | BOOLEAN       | True     | $1:col_bool::BOOLEAN      | json/schema_A_1.json     | 0        |
| col_date    | DATE          | True     | $1:col_date::DATE         | json/schema_A_1.json     | 1        |
| col_ts      | TIMESTAMP_NTZ | True     | $1:col_ts::TIMESTAMP_NTZ  | json/schema_A_1.json     | 2        |
+-------------+---------------+----------+---------------------------+--------------------------+----------+
```

Copy

Creates a table using the detected schema from staged JSON files.

> ```
> CREATE TABLE mytable
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
>       FROM TABLE(
>         INFER_SCHEMA(
>           LOCATION=>'@mystage/json/',
>           FILE_FORMAT=>'my_json_format'
>         )
>       ));
> ```
>
> Copy

Note

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 128 MB. We recommend that you avoid using `*` for larger result sets, and only use the required columns, `COLUMN NAME`, `TYPE`, and `NULLABLE`, for the query. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`.

Retrieve the column definitions for CSV files in the `mystage` stage and load the CSV files using MATCH\_BY\_COLUMN\_NAME:

```
-- Create a file format that sets the file type as CSV.
CREATE FILE FORMAT my_csv_format
  TYPE = csv
  PARSE_HEADER = true;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/csv/'
      , FILE_FORMAT=>'my_csv_format'
      )
    );

+-------------+---------------+----------+---------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE          | NULLABLE | EXPRESSION                | FILENAMES                | ORDER_ID |
|-------------+---------------+----------+---------------------------+--------------------------|----------+
| col_bool    | BOOLEAN       | True     | $1:col_bool::BOOLEAN      | json/schema_A_1.csv      | 0        |
| col_date    | DATE          | True     | $1:col_date::DATE         | json/schema_A_1.csv      | 1        |
| col_ts      | TIMESTAMP_NTZ | True     | $1:col_ts::TIMESTAMP_NTZ  | json/schema_A_1.csv      | 2        |
+-------------+---------------+----------+---------------------------+--------------------------+----------+

-- Load the CSV file using MATCH_BY_COLUMN_NAME.
COPY INTO mytable FROM @mystage/csv/
  FILE_FORMAT = (
    FORMAT_NAME= 'my_csv_format'
  )
  MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
```

Copy

### Iceberg column definitions[¶](#iceberg-column-definitions "Link to this heading")

Retrieve the Iceberg column definitions for Parquet files on the `mystage` stage:

```
-- Create a file format that sets the file type as Parquet.
  CREATE OR REPLACE FILE FORMAT my_parquet_format
    TYPE = PARQUET
    USE_VECTORIZED_SCANNER = TRUE;

-- Query the INFER_SCHEMA function.
SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION=>'@mystage'
    , FILE_FORMAT=>'my_parquet_format'
    , KIND => 'ICEBERG'
    )
  );
```

Copy

Output:

```
+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| id          | INT     | False    | $1:id::INT          | sales/customers.parquet   | 0       |
| custnum     | INT     | False    | $1:custnum::INT     | sales/customers.parquet   | 1       |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Creates an Apache Iceberg™ table by using the detected schema from staged Parquet files.

```
 -- Create a file format that sets the file type as Parquet.
 CREATE OR REPLACE FILE FORMAT my_parquet_format
   TYPE = PARQUET
   USE_VECTORIZED_SCANNER = TRUE;

-- Create an Iceberg table.
CREATE ICEBERG TABLE myicebergtable
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    WITHIN GROUP (ORDER BY order_id)
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@mystage',
          FILE_FORMAT=>'my_parquet_format',
          KIND => 'ICEBERG'
        )
      ))
... {rest of the ICEBERG options}
;
```

Copy

Note

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 128 MB. We
recommend avoiding the use of `*` for larger result sets, and only using the required columns, `COLUMN NAME`, `TYPE`, and
`NULLABLE`, for the query. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`.

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
6. [Snowflake column definitions](#snowflake-column-definitions)
7. [Iceberg column definitions](#iceberg-column-definitions)

Related content

1. [Overview of data loading](/sql-reference/functions/../../user-guide/data-load-overview)
2. [Table schema evolution](/sql-reference/functions/../../user-guide/data-load-schema-evolution)