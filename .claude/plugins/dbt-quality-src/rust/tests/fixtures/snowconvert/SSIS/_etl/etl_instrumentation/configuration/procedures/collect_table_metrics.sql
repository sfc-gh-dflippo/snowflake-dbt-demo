-- <copyright file="collect_table_metrics.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
-- </copyright>

-- ==========================================================================
-- DESCRIPTION: The COLLECT_TABLE_METRICS(task_ref_id VARCHAR, package_name VARCHAR) collects metrics (row count) 
--    for the tables that are related to the  current task. The procedure queries the 
--    CONTROL_FLOW_TABLE_USAGE table to retrieve the names of all tables impacted by the specified task, 
--    counts the rows in each table, and logs the metrics to the TABLE_METRICS_LOG table.
-- ==========================================================================  

CREATE OR REPLACE PROCEDURE PUBLIC.COLLECT_TABLE_METRICS(task_ref_id VARCHAR, package_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE c1 CURSOR FOR SELECT SCHEMA_NAME, TABLE_NAME, (SCHEMA_NAME ||  '.' || TABLE_NAME) AS TBL
                      FROM PUBLIC.CONTROL_FLOW_TABLE_USAGE
                      WHERE TASK_REFID=?;
        row_count NUMBER;
        tbl_name VARCHAR;
        simple_table_name VARCHAR;
        schema_name VARCHAR;
BEGIN
    OPEN C1 USING (:task_ref_id);
    FOR record IN c1 DO
        tbl_name :=  record.tbl;
        simple_table_name := record.table_name;
        schema_name := record.schema_name;

        BEGIN
            SELECT COUNT(*) 
            INTO :row_count
            FROM IDENTIFIER(:tbl_name);
    
            INSERT INTO PUBLIC.TABLE_METRICS_LOG (
                package_name,
                task_name,
                schema_name,
                table_name,
                rowcount,
                timestamp)
            VALUES (:package_name, 
                    :task_ref_id, 
                    :schema_name, 
                    :simple_table_name, 
                    :row_count, 
                    CURRENT_TIMESTAMP());
        EXCEPTION 
           WHEN STATEMENT_ERROR CONTINUE THEN
               SYSTEM$LOG_WARN('Error collecting table metrics:' || COALESCE(:sqlerrm, '<NULL>') || ' table name: ' || COALESCE(:simple_table_name, '<NULL>'));
        END;
    END FOR;
    CLOSE C1;

    RETURN 'DONE';
END;
$$;
