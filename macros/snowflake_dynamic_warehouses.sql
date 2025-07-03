{#
This macro is designed to automatically change the warehouse after you populate the dynamic_warehouse_assignment model
#}
{% macro set_warehouse() -%}
    {%- if execute and flags.WHICH in ('run', 'build') and this -%}
        {# The source function does not check if a table exists but adapter.get_relation will be None if it does not exist #}
        {%- set dwa_source = source('dynamic_warehouses', 'dynamic_warehouse_assignment') -%}
        {%- set dynamic_warehouse_assignment = adapter.get_relation(
                database = dwa_source.database,
                schema = dwa_source.schema,
                identifier = dwa_source.identifier) -%}

        {%- if dynamic_warehouse_assignment != None -%}
            {%- set use_warehouse_block -%}
            EXECUTE IMMEDIATE $$
            DECLARE
                V_WAREHOUSE_NAME VARCHAR;
            BEGIN
                select case when '{{ is_incremental() }}' = 'True' then incremental_warehouse
                    else full_refresh_warehouse end as warehouse_name
                into :V_WAREHOUSE_NAME
                from {{ dynamic_warehouse_assignment }}
                where target_name = '{{ this }}' and
                    warehouse_name != CURRENT_WAREHOUSE();
                EXECUTE IMMEDIATE 'USE WAREHOUSE ' || V_WAREHOUSE_NAME;
            EXCEPTION WHEN OTHER THEN
                NULL;
            END;
            $$;
            {%- endset -%}
            {%- do run_query(use_warehouse_block) -%}
        {%- endif -%}
    {%- endif -%}
{% endmacro %}
