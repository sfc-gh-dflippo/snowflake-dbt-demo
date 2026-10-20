-- MIG001: !!!RESOLVE EWI!!!
-- MIG002: bare SSC-EWI code with no description (fallback path)
-- MIG007: ETL instance name (SQ_ prefix)
--
-- Marker syntax below is copied verbatim from the SnowConvert EWI reference:
-- docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation
--   /issues-and-troubleshooting/conversion-issues/ssisEWI
-- Do NOT reshape these to match the parser. If the parser stops reading them,
-- the parser is wrong -- this is what the converter actually emits.

-- SSC-EWI-INF0001 has no description here, so MIG002 must fall back to its own
-- wording rather than reporting an empty message.
-- SSC-EWI-INF0001 marker

-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!

select
    customer_id,
    !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT 'FORLOOP CONTAINER ITERATION LOGIC' CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
    status
from {{ source('raw', 'customers') }}
