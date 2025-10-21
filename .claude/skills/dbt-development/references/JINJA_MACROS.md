# Jinja Templates & Custom Macros Guide

## Overview

Jinja is a powerful templating language that enables dynamic SQL generation in dbt. Use it to reduce repetition, generate complex queries, and make models more maintainable.

## Core Jinja Concepts

### Variables

```sql
-- Using dbt variables
{% set payment_methods = ['credit_card', 'debit_card', 'paypal', 'cash'] %}

select
    order_id,
    {% for method in payment_methods %}
    sum(case when payment_method = '{{ method }}' then 1 else 0 end) as {{ method }}_count
    {%- if not loop.last -%},{%- endif %}
    {% endfor %}
from {{ ref('stg_orders') }}
group by order_id
```

### Conditionals

```sql
-- Environment-based logic
select
    customer_id,
    customer_name,
    customer_email
from {{ ref('stg_customers') }}

{% if target.name == 'dev' %}
    where customer_id <= 1000  -- Limit data in dev
{% endif %}
```

### Loops

```sql
-- Generate columns dynamically
{% set statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'] %}

select
    date_trunc('day', order_date) as order_date,
    {% for status in statuses %}
    count(case when status = '{{ status }}' then 1 end) as {{ status }}_orders
    {{ "," if not loop.last }}
    {% endfor %}
from {{ ref('stg_orders') }}
group by 1
```

## Common Jinja Patterns

### Pattern 1: Dynamic Column Selection

```sql
-- Select columns based on environment
{% set required_columns = ['order_id', 'customer_id', 'order_date', 'order_total'] %}
{% set optional_columns = ['internal_notes', 'commission_rate', 'cost_basis'] %}

select
    {% for col in required_columns %}
    {{ col }}{{ "," if not loop.last else "" }}
    {% endfor %}
    
    {% if target.name == 'prod' %}
    ,{% for col in optional_columns %}
    {{ col }}{{ "," if not loop.last else "" }}
    {% endfor %}
    {% endif %}
    
from {{ ref('stg_orders') }}
```

### Pattern 2: Pivot Tables

```sql
{% set categories_query %}
    select distinct product_category
    from {{ ref('stg_products') }}
    order by product_category
{% endset %}

{% if execute %}
    {% set categories = run_query(categories_query).columns[0].values() %}
{% else %}
    {% set categories = [] %}
{% endif %}

select
    date_trunc('month', order_date) as order_month,
    {% for category in categories %}
    sum(case when product_category = '{{ category }}' then sales_amount else 0 end) as {{ category | replace(' ', '_') | lower }}_sales
    {{ "," if not loop.last }}
    {% endfor %}
from {{ ref('fct_order_lines') }}
group by 1
```

### Pattern 3: Date Range Generation

```sql
with date_series as (
    {% for i in range(0, 365) %}
    select dateadd(day, {{ i }}, '2024-01-01'::date) as date_day
    {{ "union all" if not loop.last }}
    {% endfor %}
)

select * from date_series
```

### Pattern 4: Conditional Column Definitions

```sql
select
    order_id,
    customer_id,
    order_date,
    
    {% if var('include_pii', false) %}
    customer_email,
    customer_phone,
    shipping_address,
    {% endif %}
    
    order_total
from {{ ref('stg_orders') }}
```

## Custom Macros

### Creating Macros

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}
```

**Usage:**
```sql
select
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_payments') }}
```

### Macro with Multiple Parameters

```sql
-- macros/generate_alias_name.sql
{% macro generate_alias_name(custom_alias_name=none, node=none) %}
    {%- if custom_alias_name is none -%}
        {{ node.name }}
    {%- else -%}
        {{ custom_alias_name | trim }}
    {%- endif -%}
{% endmacro %}
```

### Macro with Default Behavior

```sql
-- macros/get_column_values_with_default.sql
{% macro get_column_values_with_default(table, column, default_value='Unknown') %}
    {% set query %}
        select distinct {{ column }}
        from {{ table }}
        where {{ column }} is not null
        union all
        select '{{ default_value }}'
    {% endset %}
    
    {% set results = run_query(query) %}
    
    {% if execute %}
        {{ return(results.columns[0].values()) }}
    {% else %}
        {{ return([]) }}
    {% endif %}
{% endmacro %}
```

## Advanced Jinja Techniques

### Snowflake-Specific Optimizations

```sql
-- macros/use_warehouse.sql
{% macro use_warehouse(model_type) %}
    {% if target.name == 'prod' %}
        {% if model_type == 'large_fact' %}
            {{ config(snowflake_warehouse='LARGE_WH') }}
        {% elif model_type == 'ml' %}
            {{ config(snowflake_warehouse='ML_WH') }}
        {% else %}
            {{ config(snowflake_warehouse='TRANSFORMING_WH') }}
        {% endif %}
    {% endif %}
{% endmacro %}
```

### Macro for SQL Generation

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) %}
    {%- set default_schema = target.schema -%}
    
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- elif target.name == 'dev' -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{% endmacro %}
```

### Dynamic Table Creation

```sql
-- macros/create_dynamic_aggregation.sql
{% macro create_dynamic_aggregation(model_name, group_by_cols, agg_cols) %}
    select
        {% for col in group_by_cols %}
        {{ col }}{{ "," if not loop.last else "," }}
        {% endfor %}
        
        {% for agg in agg_cols %}
        {{ agg['function'] }}({{ agg['column'] }}) as {{ agg['alias'] }}
        {{ "," if not loop.last }}
        {% endfor %}
    from {{ ref(model_name) }}
    group by {% for col in group_by_cols %}{{ loop.index }}{{ "," if not loop.last }}{% endfor %}
{% endmacro %}
```

## dbt_utils Macros

### Surrogate Key Generation

```sql
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_id,
    order_id,
    line_number
from {{ ref('stg_order_lines') }}
```

### Pivot

```sql
{{ dbt_utils.pivot(
    column='payment_method',
    values=dbt_utils.get_column_values(ref('stg_orders'), 'payment_method'),
    then_value='count(*)',
    else_value='0',
    agg='sum',
    prefix='',
    suffix='_count'
) }}
```

### Union Relations

```sql
{{ dbt_utils.union_relations(
    relations=[
        ref('orders_2022'),
        ref('orders_2023'),
        ref('orders_2024')
    ],
    include=['order_id', 'customer_id', 'order_date', 'order_total']
) }}
```

### Date Spine

```sql
{{ dbt_utils.date_spine(
    datepart="day",
    start_date="cast('2020-01-01' as date)",
    end_date="current_date()"
) }}
```

## Testing Macros

### Create Testable Macro

```sql
-- macros/positive_value_check.sql
{% macro positive_value_check(column_name) %}
    case
        when {{ column_name }} <= 0 then 'Invalid: Value must be positive'
        else 'Valid'
    end as {{ column_name }}_validation
{% endmacro %}
```

**Usage:**
```sql
select
    order_id,
    order_total,
    {{ positive_value_check('order_total') }}
from {{ ref('stg_orders') }}
```

## When NOT to Use Macros

### ❌ Don't Recreate Database Functions

**Critical Rule:** Never create a custom Jinja macro when you can use a native SQL function or data warehouse feature.

```sql
-- ❌ BAD: Custom macro for date truncation
{% macro my_date_trunc(datepart, column) %}
    cast(date_trunc('{{ datepart }}', {{ column }}) as date)
{% endmacro %}

-- ✅ GOOD: Use native SQL function
date_trunc('month', order_date)
```

```sql
-- ❌ BAD: Custom macro for rounding
{% macro round_to_cents(amount) %}
    round({{ amount }}, 2)
{% endmacro %}

-- ✅ GOOD: Use native ROUND function
round(order_total, 2)
```

```sql
-- ❌ BAD: Custom macro for string concatenation
{% macro concat_name(first, last) %}
    {{ first }} || ' ' || {{ last }}
{% endmacro %}

-- ✅ GOOD: Use native CONCAT or || operator
concat(first_name, ' ', last_name)
-- or
first_name || ' ' || last_name
```

### When Macros ARE Appropriate

✅ **Dynamic SQL generation** - Creating columns/tables based on data  
✅ **Complex templating** - Repeating patterns with variations  
✅ **Project-specific business logic** - Reusable domain calculations  
✅ **Environment-specific logic** - Dev vs prod differences  

**Examples of Appropriate Macro Use:**

```sql
-- ✅ GOOD: Dynamic column generation from data
{% set payment_methods_query %}
    select distinct payment_method from {{ ref('stg_orders') }}
{% endset %}

{% set payment_methods = run_query(payment_methods_query).columns[0].values() %}

{% macro generate_payment_columns() %}
    {% for method in payment_methods %}
    sum(case when payment_method = '{{ method }}' then 1 else 0 end) as {{ method }}_count
    {{ "," if not loop.last }}
    {% endfor %}
{% endmacro %}
```

```sql
-- ✅ GOOD: Environment-specific data limiting
{% macro limit_data_in_dev(column_name, dev_days=3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= dateadd(day, -{{ dev_days }}, current_date())
    {% endif %}
{% endmacro %}
```

```sql
-- ✅ GOOD: Complex business logic reused across models
{% macro calculate_customer_tier(ltv_column, order_count_column) %}
    case 
        when {{ ltv_column }} >= 10000 and {{ order_count_column }} >= 20 then 'VIP'
        when {{ ltv_column }} >= 5000 and {{ order_count_column }} >= 10 then 'Premium'
        when {{ ltv_column }} >= 1000 and {{ order_count_column }} >= 5 then 'Standard'
        else 'Basic'
    end
{% endmacro %}
```

## Macro Best Practices

### 1. Document Your Macros

```sql
-- macros/calculate_tax.sql
{%- macro calculate_tax(amount, tax_rate=0.08) -%}
    {#
    Calculates tax amount from base amount and tax rate.
    
    Args:
        amount: Column name or value to calculate tax on
        tax_rate: Tax rate as decimal (default: 0.08 for 8%)
    
    Returns:
        Calculated tax amount rounded to 2 decimal places
    
    Example:
        {{ calculate_tax('subtotal', 0.10) }}
    #}
    round({{ amount }} * {{ tax_rate }}, 2)
{%- endmacro -%}
```

### 2. Use Whitespace Control

```sql
-- Remove whitespace before/after
{%- for item in items -%}
    {{ item }}
{%- endfor -%}

-- Keep whitespace
{% for item in items %}
    {{ item }}
{% endfor %}
```

### 3. Handle Edge Cases

```sql
{% macro safe_divide(numerator, denominator, decimal_places=2) %}
    round(
        {{ numerator }} / nullif({{ denominator }}, 0),
        {{ decimal_places }}
    )
{% endmacro %}
```

### 4. Make Macros Reusable

```sql
-- ✅ Good: Flexible, reusable
{% macro create_metric(column, metric_type='sum', alias=none) %}
    {{ metric_type }}({{ column }}) as {% if alias %}{{ alias }}{% else %}{{ metric_type }}_{{ column }}{% endif %}
{% endmacro %}

-- ❌ Bad: Too specific
{% macro sum_revenue() %}
    sum(revenue) as total_revenue
{% endmacro %}
```

## Debugging Jinja

### Compile to See Generated SQL

```bash
# Compile model to see final SQL
dbt compile --select model_name

# View compiled SQL
cat target/compiled/your_project/models/model_name.sql
```

### Print Debugging

```sql
{{ log("Debug: payment_methods = " ~ payment_methods, info=true) }}

{% set query_result = run_query("select count(*) from " ~ ref('stg_orders')) %}
{{ log("Row count: " ~ query_result.columns[0][0], info=true) }}
```

### Check Variable Values

```sql
-- At model start
{{ log("Target: " ~ target.name, info=true) }}
{{ log("Execute: " ~ execute, info=true) }}
{{ log("Invocation ID: " ~ invocation_id, info=true) }}
```

## Common Jinja Variables

### Built-in Variables

```sql
-- Environment info
{{ target.name }}            -- 'dev', 'prod', etc.
{{ target.schema }}          -- Target schema
{{ target.database }}        -- Target database
{{ target.warehouse }}       -- Snowflake warehouse
{{ target.role }}            -- Snowflake role

-- Run info
{{ run_started_at }}         -- Run start timestamp
{{ invocation_id }}          -- Unique run identifier
{{ modules.datetime.datetime.now() }}  -- Current timestamp

-- Model info
{{ this }}                   -- Current model reference
{{ this.schema }}            -- Current model's schema
{{ this.name }}              -- Current model's name
{{ this.database }}          -- Current model's database

-- Flags
{{ flags.FULL_REFRESH }}     -- True if --full-refresh
```

### Custom Variables

```yaml
# dbt_project.yml
vars:
  start_date: '2024-01-01'
  default_currency: 'USD'
```

```sql
-- Using custom variables
where order_date >= '{{ var("start_date") }}'
  and currency = '{{ var("default_currency") }}'
```

## Performance Considerations

### Avoid Heavy Queries in Jinja

```sql
-- ❌ Bad: Heavy query at compile time
{% set all_customers = run_query("select * from customers") %}

-- ✅ Good: Lightweight query
{% set customer_count = run_query("select count(*) from customers") %}
```

### Cache Results

```sql
-- Cache query results when used multiple times
{% set categories_query %}
    select distinct category from products
{% endset %}

{% set categories = run_query(categories_query).columns[0].values() %}

-- Use categories multiple times without re-querying
{% for cat in categories %}
    ...
{% endfor %}
```

---

**Related Documentation:**
- `QUICK_REFERENCE.md` - Jinja patterns cheatsheet
- `PERFORMANCE_OPTIMIZATION.md` - Jinja performance tips
- Official: [dbt Jinja Function Reference](https://docs.getdbt.com/reference/dbt-jinja-functions)

