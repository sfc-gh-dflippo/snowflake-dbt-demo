-- PRJ006: EXECUTE DBT PROJECT in orchestration
-- INC015: external loader targeting a dbt model
CREATE OR REPLACE TASK analytics.tasks.load_flow_b
  WAREHOUSE = TRANSFORM_WH
  SCHEDULE = 'USING CRON 0 6 * * * America/New_York'
AS
  EXECUTE DBT PROJECT 'migrated_flow_b';

CREATE OR REPLACE TASK analytics.tasks.load_flow_a
  WAREHOUSE = TRANSFORM_WH
  AFTER analytics.tasks.load_flow_b
AS
  EXECUTE DBT PROJECT 'migrated_flow_a';

CREATE OR REPLACE PROCEDURE analytics.procedures.backfill_transactions()
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  INSERT INTO analytics.silver.int_transactions_load
  SELECT * FROM analytics.raw.transactions
  WHERE transaction_date < '2020-01-01';
  RETURN 'done';
END;
