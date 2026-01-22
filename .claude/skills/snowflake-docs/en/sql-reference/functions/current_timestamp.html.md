---
auto_generated: true
description: Context functions (General)
last_scraped: '2026-01-14T16:55:51.798769+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/current_timestamp.html
title: CURRENT_TIMESTAMP | Snowflake Documentation
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

     + General
     + [CURRENT\_CLIENT](current_client.md)
     + [CURRENT\_DATE](current_date.md)
     + [CURRENT\_IP\_ADDRESS](current_ip_address.md)
     + [CURRENT\_REGION](current_region.md)
     + [CURRENT\_TIME](current_time.md)
     + [CURRENT\_TIMESTAMP](current_timestamp.md)
     + [CURRENT\_VERSION](current_version.md)
     + [GETDATE](getdate.md)
     + [LOCALTIME](localtime.md)
     + [LOCALTIMESTAMP](localtimestamp.md)
     + [SYSDATE](sysdate.md)
     + [SYSTIMESTAMP](systimestamp.md)
     + [SYS\_CONTEXT](sys_context.md)
     + Session
     + [ALL\_USER\_NAMES](all_user_names.md)
     + [CURRENT\_ACCOUNT](current_account.md)
     + [CURRENT\_ACCOUNT\_NAME](current_account_name.md)
     + [CURRENT\_ORGANIZATION\_NAME](current_organization_name.md)
     + [CURRENT\_ORGANIZATION\_USER](current_organization_user.md)
     + [CURRENT\_ROLE](current_role.md)
     + [CURRENT\_AVAILABLE\_ROLES](current_available_roles.md)
     + [CURRENT\_SECONDARY\_ROLES](current_secondary_roles.md)
     + [CURRENT\_SESSION](current_session.md)
     + [CURRENT\_STATEMENT](current_statement.md)
     + [CURRENT\_TRANSACTION](current_transaction.md)
     + [CURRENT\_USER](current_user.md)
     + [GETVARIABLE](getvariable.md)
     + [LAST\_QUERY\_ID](last_query_id.md)
     + [LAST\_TRANSACTION](last_transaction.md)
     + Session object
     + [CURRENT\_DATABASE](current_database.md)
     + [CURRENT\_ROLE\_TYPE](current_role_type.md)
     + [CURRENT\_SCHEMA](current_schema.md)
     + [CURRENT\_SCHEMAS](current_schemas.md)
     + [CURRENT\_WAREHOUSE](current_warehouse.md)
     + [INVOKER\_ROLE](invoker_role.md)
     + [INVOKER\_SHARE](invoker_share.md)
     + [IS\_APPLICATION\_ROLE\_IN\_SESSION](is_application_role_in_session.md)
     + [IS\_DATABASE\_ROLE\_IN\_SESSION](is_database_role_in_session.md)
     + [IS\_GRANTED\_TO\_INVOKER\_ROLE](is_granted_to_invoker_role.md)
     + [IS\_INSTANCE\_ROLE\_IN\_SESSION](is_instance_role_in_session.md)
     + [IS\_ORGANIZATION\_USER\_GROUP\_IN\_SESSION](is_organization_user_group_in_session.md)
     + [IS\_ROLE\_IN\_SESSION](is_role_in_session.md)
     + [POLICY\_CONTEXT](policy_context.md)
     + Alert
     + [GET\_CONDITION\_QUERY\_UUID](get_condition_query_uuid.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Context](../functions-context.md)CURRENT\_TIMESTAMP

Categories:
:   [Context functions](../functions-context) (General)

# CURRENT\_TIMESTAMP[¶](#current-timestamp "Link to this heading")

Returns the current timestamp for the system in the local time zone.

Aliases:
:   [LOCALTIMESTAMP](localtimestamp) , [GETDATE](getdate) , [SYSTIMESTAMP](systimestamp)

## Syntax[¶](#syntax "Link to this heading")

```
CURRENT_TIMESTAMP( [ <fract_sec_precision> ] )

CURRENT_TIMESTAMP
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`fract_sec_precision`
:   This optional argument indicates the precision with which to report the
    time. For example, a value of 3 says to use 3 digits after the decimal
    point (that is, to specify the time with a precision of milliseconds).

    The default precision is 9 (nanoseconds).

    Valid values range from 0 - 9. However, most platforms do not support true
    nanosecond precision; the precision that you get might be less than the
    precision you specify. In practice, precision is usually approximately
    milliseconds (3 digits) at most.

    Note

    Fractional seconds are only displayed if they have been explicitly set in the [TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format) parameter for the session (e.g. `'YYYY-MM-DD HH24:MI:SS.FF'`).

## Returns[¶](#returns "Link to this heading")

Returns the current system time. The data type of the returned value is
[TIMESTAMP\_LTZ](../data-types-datetime.html#label-datatypes-timestamp-variations).

## Usage notes[¶](#usage-notes "Link to this heading")

* The setting of the [TIMEZONE](../parameters.html#label-timezone) parameter affects the return value. The returned timestamp is in the time zone for the session.
* The setting of the [TIMESTAMP\_TYPE\_MAPPING](../parameters.html#label-timestamp-type-mapping) parameter does not affect the return value.
* Do not use the returned value for precise time ordering between concurrent queries (processed by the same virtual warehouse) because the queries might be serviced by different compute resources (in the warehouse).

* To comply with the ANSI standard, this function can be called without parentheses in SQL statements.

  However, if you are setting a [Snowflake Scripting variable](../../developer-guide/snowflake-scripting/variables)
  to an expression that calls the function (for example, `my_var := CURRENT_TIMESTAMP();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](../functions-context.html#label-context-function-usage-notes).
* The aliases SYSTIMESTAMP and GETDATE differ from CURRENT\_TIMESTAMP in the following ways:

  + They do not support the `fract_sec_precision` argument.
  + These functions must be called with parentheses.

## Examples[¶](#examples "Link to this heading")

The examples in this section use the timestamp output format `YYYY-MM-DD HH24:MI:SS.FF`. To configure
your session to use the same output format, run the following statement:

```
ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
```

Copy

### Call the CURRENT\_TIMESTAMP function with different precision values[¶](#call-the-current-timestamp-function-with-different-precision-values "Link to this heading")

Return the current timestamp with fractional seconds precision set to `2`:

```
SELECT CURRENT_TIMESTAMP(2);
```

Copy

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2024-04-17 15:41:38.29 |
+------------------------+
```

Return the current timestamp with fractional seconds precision set to `4`:

```
SELECT CURRENT_TIMESTAMP(4);
```

Copy

```
+--------------------------+
| CURRENT_TIMESTAMP(4)     |
|--------------------------|
| 2024-04-17 15:42:14.2100 |
+--------------------------+
```

Return the current timestamp with fractional seconds precision set to the default (`9`):

```
SELECT CURRENT_TIMESTAMP;
```

Copy

```
+-------------------------------+
| CURRENT_TIMESTAMP             |
|-------------------------------|
| 2024-04-17 15:42:55.130000000 |
+-------------------------------+
```

### Call the CURRENT\_TIMESTAMP function with different TIMEZONE settings[¶](#call-the-current-timestamp-function-with-different-timezone-settings "Link to this heading")

Set the [TIMEZONE](../parameters.html#label-timezone) parameter to `America/New_York` and call the CURRENT\_TIMESTAMP function:

```
ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT CURRENT_TIMESTAMP(2);
```

Copy

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2025-08-11 14:16:43.57 |
+------------------------+
```

Set the TIMEZONE parameter to `America/Los_Angeles` and call the CURRENT\_TIMESTAMP function:

```
ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

SELECT CURRENT_TIMESTAMP(2);
```

Copy

```
+------------------------+
| CURRENT_TIMESTAMP(2)   |
|------------------------|
| 2025-08-11 11:17:18.19 |
+------------------------+
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
3. [Returns](#returns)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)
6. [Call the CURRENT\_TIMESTAMP function with different precision values](#call-the-current-timestamp-function-with-different-precision-values)
7. [Call the CURRENT\_TIMESTAMP function with different TIMEZONE settings](#call-the-current-timestamp-function-with-different-timezone-settings)