/*
    dbt Feature Demonstration: INTERMEDIATE MODEL - BUSINESS LOGIC

    This model demonstrates:
    - ✅ Intermediate layer best practices (business logic isolation)
    - ✅ Ephemeral materialization for reusable components
    - ✅ Aggregation functions (COUNT, SUM, MIN, MAX)
    - ✅ Window functions for analytics
    - ✅ Model aliasing for backward compatibility
    - ✅ References to staging models only (no direct sources)
    - ✅ CTE pattern for complex transformations

    Complexity: 🥈 WALK (Intermediate)
    Layer: Silver - Business Logic
*/

{{ config(
    tags=['intermediate', 'customers'],
    alias='LKP_CUSTOMERS_WITH_ORDERS'
) }}

-- Intermediate model: Customer order statistics
-- Following best practices: intermediate models contain business logic
-- This replaces the lookup_customers_with_orders model

with customer_orders as (
    select
        customer_key,
        count(*) as order_count,
        sum(
            case
                when order_status = 'O' then 1
                else 0
            end
        ) as open_order_count
    from {{ ref('stg_tpc_h__orders') }}
    group by customer_key
)

select * from customer_orders
