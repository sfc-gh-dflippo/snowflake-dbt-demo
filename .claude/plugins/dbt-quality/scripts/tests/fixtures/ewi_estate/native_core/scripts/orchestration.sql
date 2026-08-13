-- Additional orchestration script for PRJ006 (need >=2 hits)
CREATE OR REPLACE TASK analytics.tasks.run_native
  WAREHOUSE = TRANSFORM_WH
  SCHEDULE = 'USING CRON 0 7 * * * America/New_York'
AS
  EXECUTE DBT PROJECT 'native_core';
