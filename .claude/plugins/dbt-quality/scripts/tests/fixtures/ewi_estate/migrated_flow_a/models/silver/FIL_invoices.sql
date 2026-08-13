-- MIG003: SSC-FDM marker
-- MIG004: NEEDS-USER marker
-- MIG005: etl_dml_operation__ control column
--
-- Marker syntax below is copied verbatim from the SnowConvert FDM reference:
-- docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation
--   /issues-and-troubleshooting/functional-difference/sqlServerFDM
-- Do NOT reshape these to match the parser.

--** SSC-FDM-TS0001 - COLLATION Albanian_BIN NOT SUPPORTED **
----** SSC-FDM-TS0029 - SET NOCOUNT STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "#temptable" **
-- NEEDS-USER: Verify sort order matches original mapping

select
    invoice_id,
    customer_id,
    amount,
    /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/
    etl_dml_operation__,
    case
        when etl_dml_operation__ = 'DD_INSERT' then 'I'
        when etl_dml_operation__ = 'DD_UPDATE' then 'U'
    end as dml_flag
from {{ source('raw', 'invoices') }}
where etl_dml_operation__ <> 'DD_REJECT'
