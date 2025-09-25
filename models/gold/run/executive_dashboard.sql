{{ config(
    materialized='table',
    tags=['gold', 'run', 'executive']
) }}

-- GOLD RUN: Executive dashboard with advanced KPIs
-- Complexity: Advanced - Complex business logic, executive metrics, advanced features
-- Features demonstrated: Advanced post-hooks, logging, executive KPIs

{% set current_year = run_started_at.strftime("%Y") | int %}
{% set previous_year = current_year - 1 %}

with daily_metrics as (
    select 
        order_date,
        order_year,
        order_month,
        order_quarter,
        
        -- Core metrics
        sum(total_order_value) as daily_revenue,
        sum(order_count) as daily_orders,
        sum(unique_customers) as daily_active_customers,
        avg(avg_order_value) as daily_avg_order_value,
        
        -- Status breakdown
        sum(revenue_o_status) as open_revenue,
        sum(revenue_f_status) as fulfilled_revenue,
        sum(revenue_p_status) as partial_revenue,
        
        -- Growth calculations
        lag(sum(total_order_value)) over (order by order_date) as prev_day_revenue,
        avg(sum(total_order_value)) over (
            order by order_date 
            rows between 6 preceding and current row
        ) as seven_day_avg_revenue

    from {{ ref('order_facts_dynamic') }}
    group by order_date, order_year, order_month, order_quarter
),

executive_kpis as (
    select 
        order_date as metric_date,
        
        -- Revenue metrics
        daily_revenue as total_revenue,
        daily_orders as total_orders,
        round(daily_avg_order_value, 2) as avg_order_value,
        daily_active_customers as active_customers,
        
        -- Additional metrics for context
        seven_day_avg_revenue as "7-Day Average Revenue",
        case 
            when prev_day_revenue > 0 
            then round(((daily_revenue - prev_day_revenue) / prev_day_revenue) * 100, 2)
            else null 
        end as "Daily Revenue Growth %",
        
        -- Efficiency metrics
        round(daily_revenue / nullif(daily_orders, 0), 2) as "Revenue per Order",
        round(daily_revenue / nullif(daily_active_customers, 0), 2) as "Revenue per Customer",
        
        -- Status analysis
        round((fulfilled_revenue / nullif(daily_revenue, 0)) * 100, 1) as "Fulfillment Rate %",
        round((open_revenue / nullif(daily_revenue, 0)) * 100, 1) as "Open Orders %",
        round((partial_revenue / nullif(daily_revenue, 0)) * 100, 1) as "Partial Orders %",
        
        -- Performance indicators
        case 
            when daily_revenue > seven_day_avg_revenue * 1.2 then 'Excellent'
            when daily_revenue > seven_day_avg_revenue * 1.1 then 'Good'
            when daily_revenue > seven_day_avg_revenue * 0.9 then 'Average'
            else 'Below Average'
        end as "Performance Rating",
        
        -- Trend indicators
        case 
            when daily_revenue > prev_day_revenue then '↗️ Increasing'
            when daily_revenue < prev_day_revenue then '↘️ Decreasing'  
            else '➡️ Stable'
        end as "Trend",
        
        order_year as "Year",
        order_quarter as "Quarter",
        order_month as "Month"

    from daily_metrics
)

select *
from executive_kpis
where metric_date >= dateadd(year, -2, current_date())
order by metric_date desc
