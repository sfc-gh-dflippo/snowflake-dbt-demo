{%- macro copy_log_to_snowflake() -%}

  {%- set query -%}
    CREATE TEMPORARY STAGE IF NOT EXISTS TMP_STG_DBT_LOG_FILE FILE_FORMAT=(SKIP_BLANK_LINES=TRUE)
  {%- endset -%}
  {%- do run_query(query) -%}

  {%- set query -%}
    CREATE OR REPLACE TABLE DBT_LOG (ROW_NUM INTEGER, LOG_TEXT VARCHAR, LAST_UPDATED TIMESTAMP_TZ)
  {%- endset -%}
  {%- do run_query(query) -%}

  {%- set query -%}
    PUT file://./logs/dbt.log @TMP_STG_DBT_LOG_FILE
  {%- endset -%}
  {%- do run_query(query) -%}

  {%- set query -%}
    INSERT INTO DBT_LOG (ROW_NUM, LOG_TEXT, LAST_UPDATED)
    SELECT 
        --We use the analytic function to avoid gaps due to blank lines
        row_number() over (order by metadata$file_row_number) as ROW_NUM,
        $1 as LOG_TEXT,
        SYSDATE() AS LAST_UPDATED
    from @TMP_STG_DBT_LOG_FILE
  {%- endset -%}
  {%- do run_query(query) -%}

{%- endmacro -%}