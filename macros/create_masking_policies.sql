{%- macro create_masking_policies() -%}

{%- set query -%}
CREATE MASKING POLICY IF NOT EXISTS TEST_MASKING_POLICY AS (val string) RETURNS string ->
    CASE WHEN CURRENT_ROLE() IN ('DFLIPPO_ROLE') THEN val 
         WHEN CURRENT_ROLE() IN ('DEVELOPER') THEN SHA2(val)
    ELSE '**********'
    END
{%- endset -%}
{%- do run_query(query) -%}

{%- endmacro -%}