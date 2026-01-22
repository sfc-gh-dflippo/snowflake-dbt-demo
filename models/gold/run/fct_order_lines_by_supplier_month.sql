/*
    dbt Feature Demonstration: MARTS MODEL - AGGREGATED FACT TABLE

    This model demonstrates:
    - ✅ Aggregated fact table (monthly rollup by supplier)
    - ✅ Table materialization for pre-aggregated analytics
    - ✅ References to other fact tables (proper layering)
    - ✅ Time-based aggregation with year and month
    - ✅ Business metrics aggregation
    - ✅ Proper gold layer structure for BI tools

    Complexity: 🥇 RUN (Advanced)
    Layer: Gold - Aggregated Facts
*/

{{ config(
    materialized='table',
    tags=['marts', 'aggregates', 'monthly_rollup']
) }}

-- Aggregated Fact: Order lines summarized by supplier, year, and month
-- Following best practices: aggregate on fact tables for reporting efficiency

with order_lines as (
    select * from {{ ref('fct_order_lines') }}
),

aggregated as (
    select
        -- Dimensions (grouping keys)
        supplier_key,
        year(order_date) as order_year,
        month(order_date) as order_month,

        -- Aggregated measures
        count(*) as total_order_lines,
        count(distinct order_key) as total_orders,
        sum(quantity) as total_quantity,
        sum(extended_price) as total_extended_price,
        sum(discounted_price) as total_discounted_price,
        sum(final_price) as total_final_price,
        sum(final_price_eur) as total_final_price_eur,

        -- Average metrics
        avg(quantity) as avg_quantity_per_line,
        avg(final_price) as avg_final_price_per_line,
        avg(discount) as avg_discount_rate,

        -- Min/Max tracking
        min(ship_date) as earliest_ship_date,
        max(ship_date) as latest_ship_date,

        -- Audit columns
        current_timestamp() as _updated_at

    from order_lines
    group by
        supplier_key,
        year(order_date),
        month(order_date)
),

final as (
    select
        -- Composite key for uniqueness
        supplier_key,
        order_year,
        order_month,

        -- Create a readable month identifier
        to_date(order_year || '-' || lpad(order_month::varchar, 2, '0') || '-01') as month_start_date,

        -- Metrics
        total_order_lines,
        total_orders,
        total_quantity,
        total_extended_price,
        total_discounted_price,
        total_final_price,
        total_final_price_eur,

        -- Averages
        avg_quantity_per_line,
        avg_final_price_per_line,
        avg_discount_rate,

        -- Date ranges
        earliest_ship_date,
        latest_ship_date,

        -- Calculated metrics
        case
            when total_order_lines > 0
            then total_orders::float / total_order_lines
            else 0
        end as avg_lines_per_order,

        -- Audit
        _updated_at

    from aggregated
)

select * from final
