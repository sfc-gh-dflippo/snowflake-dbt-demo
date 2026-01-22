---
auto_generated: true
description: This family of functions allows for the gathering of information about
  the context in which the statement is executed. These functions are evaluated at
  most once per statement.
last_scraped: '2026-01-14T16:55:28.029542+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-context
title: Context functions | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)

   * [Summary of functions](intro-summary-operators-functions.md)
   * [All functions (alphabetical)](functions-all.md)")
   * [Aggregate](functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](functions/ai_classify.md)
       * [AI\_COMPLETE](functions/ai_complete.md)
       * [AI\_COUNT\_TOKENS](functions/ai_count_tokens.md)
       * [AI\_EMBED](functions/ai_embed.md)
       * [AI\_EXTRACT](functions/ai_extract.md)
       * [AI\_FILTER](functions/ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](functions/ai_parse_document.md)
       * [AI\_REDACT](functions/ai_redact.md)
       * [AI\_SENTIMENT](functions/ai_sentiment.md)
       * [AI\_SIMILARITY](functions/ai_similarity.md)
       * [AI\_TRANSCRIBE](functions/ai_transcribe.md)
       * [AI\_TRANSLATE](functions/ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](functions/classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](functions/embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](functions/embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](functions/entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](functions/extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](functions/finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](functions/parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](functions/sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](functions/summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](functions/translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](functions/ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](functions/ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](functions/count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](functions/search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](functions/split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](functions/split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](functions/try_complete-snowflake-cortex.md)")
   * [Bitwise expression](expressions-byte-bit.md)
   * [Conditional expression](expressions-conditional.md)
   * [Context](functions-context.md)

     + General
     + [CURRENT\_CLIENT](functions/current_client.md)
     + [CURRENT\_DATE](functions/current_date.md)
     + [CURRENT\_IP\_ADDRESS](functions/current_ip_address.md)
     + [CURRENT\_REGION](functions/current_region.md)
     + [CURRENT\_TIME](functions/current_time.md)
     + [CURRENT\_TIMESTAMP](functions/current_timestamp.md)
     + [CURRENT\_VERSION](functions/current_version.md)
     + [GETDATE](functions/getdate.md)
     + [LOCALTIME](functions/localtime.md)
     + [LOCALTIMESTAMP](functions/localtimestamp.md)
     + [SYSDATE](functions/sysdate.md)
     + [SYSTIMESTAMP](functions/systimestamp.md)
     + [SYS\_CONTEXT](functions/sys_context.md)
     + Session
     + [ALL\_USER\_NAMES](functions/all_user_names.md)
     + [CURRENT\_ACCOUNT](functions/current_account.md)
     + [CURRENT\_ACCOUNT\_NAME](functions/current_account_name.md)
     + [CURRENT\_ORGANIZATION\_NAME](functions/current_organization_name.md)
     + [CURRENT\_ORGANIZATION\_USER](functions/current_organization_user.md)
     + [CURRENT\_ROLE](functions/current_role.md)
     + [CURRENT\_AVAILABLE\_ROLES](functions/current_available_roles.md)
     + [CURRENT\_SECONDARY\_ROLES](functions/current_secondary_roles.md)
     + [CURRENT\_SESSION](functions/current_session.md)
     + [CURRENT\_STATEMENT](functions/current_statement.md)
     + [CURRENT\_TRANSACTION](functions/current_transaction.md)
     + [CURRENT\_USER](functions/current_user.md)
     + [GETVARIABLE](functions/getvariable.md)
     + [LAST\_QUERY\_ID](functions/last_query_id.md)
     + [LAST\_TRANSACTION](functions/last_transaction.md)
     + Session object
     + [CURRENT\_DATABASE](functions/current_database.md)
     + [CURRENT\_ROLE\_TYPE](functions/current_role_type.md)
     + [CURRENT\_SCHEMA](functions/current_schema.md)
     + [CURRENT\_SCHEMAS](functions/current_schemas.md)
     + [CURRENT\_WAREHOUSE](functions/current_warehouse.md)
     + [INVOKER\_ROLE](functions/invoker_role.md)
     + [INVOKER\_SHARE](functions/invoker_share.md)
     + [IS\_APPLICATION\_ROLE\_IN\_SESSION](functions/is_application_role_in_session.md)
     + [IS\_DATABASE\_ROLE\_IN\_SESSION](functions/is_database_role_in_session.md)
     + [IS\_GRANTED\_TO\_INVOKER\_ROLE](functions/is_granted_to_invoker_role.md)
     + [IS\_INSTANCE\_ROLE\_IN\_SESSION](functions/is_instance_role_in_session.md)
     + [IS\_ORGANIZATION\_USER\_GROUP\_IN\_SESSION](functions/is_organization_user_group_in_session.md)
     + [IS\_ROLE\_IN\_SESSION](functions/is_role_in_session.md)
     + [POLICY\_CONTEXT](functions/policy_context.md)
     + Alert
     + [GET\_CONDITION\_QUERY\_UUID](functions/get_condition_query_uuid.md)
   * [Conversion](functions-conversion.md)
   * [Data generation](functions-data-generation.md)
   * [Data metric](functions-data-metric.md)
   * [Date & time](functions-date-time.md)
   * [Differential privacy](functions-differential-privacy.md)
   * [Encryption](functions-encryption.md)
   * [File](functions-file.md)
   * [Geospatial](functions-geospatial.md)
   * [Hash](functions-hash-scalar.md)
   * [Metadata](functions-metadata.md)
   * [ML Model Monitors](functions-model-monitors.md)
   * [Notification](functions-notification.md)
   * [Numeric](functions-numeric.md)
   * [Organization users and organization user groups](functions-organization-users.md)
   * [Regular expressions](functions-regexp.md)
   * [Semi-structured and structured data](functions-semistructured.md)
   * [Snowpark Container Services](functions-spcs.md)
   * [String & binary](functions-string.md)
   * [System](functions-system.md)
   * [Table](functions-table.md)
   * [Vector](functions-vector.md)
   * [Window](functions-window.md)
   * [Stored procedures](../sql-reference-stored-procedures.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)Context

# Context functions[¶](#context-functions "Link to this heading")

This family of functions allows for the gathering of information about the context in which the statement is executed. These functions are evaluated
at most once per statement.

## List of functions[¶](#list-of-functions "Link to this heading")

| Sub-category | Function | Notes |
| --- | --- | --- |
| General context | [CURRENT\_CLIENT](functions/current_client) |  |
|  | [CURRENT\_DATE](functions/current_date) |  |
|  | [CURRENT\_IP\_ADDRESS](functions/current_ip_address) |  |
|  | [CURRENT\_REGION](functions/current_region) |  |
|  | [CURRENT\_TIME](functions/current_time) |  |
|  | [CURRENT\_TIMESTAMP](functions/current_timestamp) |  |
|  | [CURRENT\_VERSION](functions/current_version) |  |
|  | [GETDATE](functions/getdate) | Alias for CURRENT\_TIMESTAMP. |
|  | [LOCALTIME](functions/localtime) | Alias for CURRENT\_TIME. |
|  | [LOCALTIMESTAMP](functions/localtimestamp) | Alias for CURRENT\_TIMESTAMP. |
|  | [SYSDATE](functions/sysdate) |  |
|  | [SYSTIMESTAMP](functions/systimestamp) |  |
|  | [SYS\_CONTEXT](functions/sys_context) |  |
| Session context | [ALL\_USER\_NAMES](functions/all_user_names) |  |
|  | [CURRENT\_ACCOUNT](functions/current_account) | Returns account locator. |
|  | [CURRENT\_ACCOUNT\_NAME](functions/current_account_name) | Returns account name. |
|  | [CURRENT\_ORGANIZATION\_NAME](functions/current_organization_name) |  |
|  | [CURRENT\_ORGANIZATION\_USER](functions/current_organization_user) |  |
|  | [CURRENT\_ROLE](functions/current_role) |  |
|  | [CURRENT\_AVAILABLE\_ROLES](functions/current_available_roles) |  |
|  | [CURRENT\_SECONDARY\_ROLES](functions/current_secondary_roles) |  |
|  | [CURRENT\_SESSION](functions/current_session) |  |
|  | [CURRENT\_STATEMENT](functions/current_statement) |  |
|  | [CURRENT\_TRANSACTION](functions/current_transaction) |  |
|  | [CURRENT\_USER](functions/current_user) |  |
|  | [GETVARIABLE](functions/getvariable) |  |
|  | [LAST\_QUERY\_ID](functions/last_query_id) |  |
|  | [LAST\_TRANSACTION](functions/last_transaction) |  |
| Session object context | [CURRENT\_DATABASE](functions/current_database) |  |
|  | [CURRENT\_ROLE\_TYPE](functions/current_role_type) |  |
|  | [CURRENT\_SCHEMA](functions/current_schema) |  |
|  | [CURRENT\_SCHEMAS](functions/current_schemas) |  |
|  | [CURRENT\_WAREHOUSE](functions/current_warehouse) |  |
|  | [INVOKER\_ROLE](functions/invoker_role) |  |
|  | [INVOKER\_SHARE](functions/invoker_share) |  |
|  | [IS\_APPLICATION\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](functions/is_application_role_activated) |  |
|  | [IS\_APPLICATION\_ROLE\_IN\_SESSION](functions/is_application_role_in_session) |  |
|  | [IS\_DATABASE\_ROLE\_IN\_SESSION](functions/is_database_role_in_session) |  |
|  | [IS\_GRANTED\_TO\_INVOKER\_ROLE](functions/is_granted_to_invoker_role) |  |
|  | [IS\_INSTANCE\_ROLE\_IN\_SESSION](functions/is_instance_role_in_session) |  |
|  | [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](functions/is_role_activated) |  |
|  | [IS\_ROLE\_IN\_SESSION](functions/is_role_in_session) |  |
|  | [POLICY\_CONTEXT](functions/policy_context) |  |
| Alert context | [GET\_CONDITION\_QUERY\_UUID](functions/get_condition_query_uuid) |  |
| Organization context | [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](functions/is_group_activated) |  |
|  | [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](functions/is_group_imported) |  |
|  | [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](functions/is_user_imported) |  |

## Usage notes[¶](#usage-notes "Link to this heading")

* Context functions generally do not require arguments (except for [SYS\_CONTEXT](functions/sys_context)).
* To comply with the ANSI standard, the following context functions can be called without parentheses
  in SQL statements:

  + CURRENT\_DATE
  + CURRENT\_TIME
  + CURRENT\_TIMESTAMP
  + CURRENT\_USER
  + LOCALTIME
  + LOCALTIMESTAMP

  Note

  If you are setting a [Snowflake Scripting variable](../developer-guide/snowflake-scripting/variables)
  to an expression that calls one of these functions (for example, `my_var := <function_name>();`),
  you must include the parentheses.

## Examples[¶](#examples "Link to this heading")

Display the current warehouse, database, and schema for the session:

```
SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
```

Copy

```
+---------------------+--------------------+------------------+
| CURRENT_WAREHOUSE() | CURRENT_DATABASE() | CURRENT_SCHEMA() |
|---------------------+--------------------+------------------+
| MY_WAREHOUSE        | MY_DB              | PUBLIC           |
|---------------------+--------------------+------------------+
```

Display the current date, time, and timestamp (note that parentheses are not required to call these functions):

```
SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP;
```

Copy

```
+--------------+--------------+-------------------------------+
| CURRENT_DATE | CURRENT_TIME | CURRENT_TIMESTAMP             |
|--------------+--------------+-------------------------------|
| 2024-06-07   | 10:45:15     | 2024-06-07 10:45:15.064 -0700 |
+--------------+--------------+-------------------------------+
```

In a Snowflake Scripting block, call the CURRENT\_DATE function without parentheses to set a variable in a
SQL statement:

```
EXECUTE IMMEDIATE
$$
DECLARE
  currdate DATE;
BEGIN
  SELECT CURRENT_DATE INTO currdate;
  RETURN currdate;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
| 2024-06-07      |
+-----------------+
```

In a Snowflake Scripting block, attempting to set a variable to an expression that calls the CURRENT\_DATE
function without parentheses results in an error:

```
EXECUTE IMMEDIATE
$$
DECLARE
  today DATE;
BEGIN
  today := CURRENT_DATE;
  RETURN today;
END;
$$
;
```

Copy

```
000904 (42000): SQL compilation error: error line 5 at position 11
invalid identifier 'CURRENT_DATE'
```

The same block returns the current date when the function is called with the parentheses:

```
EXECUTE IMMEDIATE
$$
DECLARE
  today DATE;
BEGIN
  today := CURRENT_DATE();
  RETURN today;
END;
$$
;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
| 2024-06-07      |
+-----------------+
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

1. [List of functions](#list-of-functions)
2. [Usage notes](#usage-notes)
3. [Examples](#examples)