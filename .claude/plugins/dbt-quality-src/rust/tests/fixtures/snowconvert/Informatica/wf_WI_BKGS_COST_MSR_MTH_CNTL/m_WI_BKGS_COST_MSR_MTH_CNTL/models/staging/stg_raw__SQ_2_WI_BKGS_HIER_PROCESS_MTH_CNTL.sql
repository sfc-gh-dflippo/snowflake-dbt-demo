{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER_PROCESS_MTH_CNTL' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
SELECT
FISCAL_YEAR_WEEK_NUM_INT  FISCAL_YEAR_WEEK_NUM_INT,
(RANK() OVER (  ORDER BY FISCAL.FISCAL_YEAR_WEEK_NUM_INT DESC NULLS LAST)-1)/3+1 RUN_BATCH_ID,
'N' AS INC_FLAG
FROM
{{ source('raw', 'R_FISCAL_WEEK_TO_YEAR') }} FISCAL
WHERE FISCAL.FISCAL_YEAR_AGE BETWEEN 0 AND 3