# dbt Best Practices Guide

## 📚 Documentation Navigation
| Document | Description |
|----------|-------------|
| **[README.md](README.md)** | Project overview, architecture, and feature matrix |
| **[DBT_SETUP_GUIDE.md](DBT_SETUP_GUIDE.md)** | Complete installation and setup instructions |
| **[DBT_BEST_PRACTICES.md](DBT_BEST_PRACTICES.md)** | 👈 **You are here** - Implementation guide for dbt modeling best practices |

---

This guide provides comprehensive best practices for dbt development, covering project structure, modeling conventions, testing strategies, and performance optimization.

## 🏗️ Project Structure & Organization

### Recommended Folder Structure

```
models/
├── staging/          # One-to-one with source tables
│   ├── source_name/
│   │   ├── _models.yml
│   │   ├── stg_source_name__table_name.sql
│   │   └── ...
├── intermediate/     # Business logic transformations
│   ├── _models.yml
│   ├── int_subject_area__transformation.sql
│   └── ...
├── marts/           # Business-ready data products
│   ├── core/        # Company-wide metrics
│   ├── finance/     # Department-specific
│   ├── marketing/   # Department-specific
│   └── ...
└── utilities/       # Helper models and references
    ├── _models.yml
    └── ...
```

### Layer Responsibilities

#### 🥉 **Staging / Raw / Bronze Layer** (`staging/`)
- **Purpose**: Clean and standardize raw source data
- **Sample Naming**: `stg_{source_name}__{table_name}`
- **Most Common Materialization**: `ephemeral` or `view` unless there are formulas on join columns
- **Rules**:
  - One-to-one relationship with source tables
  - Light transformations only (renaming, casting, basic cleaning)
  - No joins between sources
  - No business logic
  - All downstream models should reference staging, not sources

#### 🥈 **Intermediate / Silver / Transformed Layer** (`intermediate/`)
- **Purpose**: Reusable business logic and complex transformations
- **Sample Naming**: `int_{subject_area}__{description}`
- **Most Common Materialization**: `ephemeral` (for reusable logic) or `table` (for complex computations)
- **Rules**:
  - Reference staging models and other intermediate models
  - Contain business logic and complex transformations
  - Should be reusable across multiple marts
  - No direct source references

#### 🥇 **Mart / Gold / Presentation Layer** (`marts/`)
- **Purpose**: Business-ready data products for end users
- **Sample Naming**: `dim_{entity}`, `fct_{process}`, or business-friendly names
- **Most Common Materialization**: `table` or `incremental`
- **Rules**:
  - Reference staging, intermediate, and other mart models
  - Contain final business logic
  - Optimized for query performance
  - Well-documented for business users

## 🏷️ Naming Conventions

### Model Names

| Layer | Prefix | Example | Description |
|-------|--------|---------|-------------|
| **Staging** | `stg_` | `stg_salesforce__accounts` | Clean source data |
| **Intermediate** | `int_` | `int_sales__monthly_metrics` | Business logic |
| **Marts - Dimensions** | `dim_` | `dim_customers` | Business entities |
| **Marts - Facts** | `fct_` | `fct_orders` | Business processes |
| **Utilities** | No prefix | `date_spine`, `exchange_rates` | Helper models |

### Column Names

```sql
-- ✅ Good: Consistent, descriptive naming
SELECT
    customer_id,
    customer_name,
    order_date,
    order_total_amount_usd,
    is_first_order,
    created_at_utc

-- ❌ Bad: Inconsistent, unclear naming  
SELECT
    custID,
    name,
    dt,
    amt,
    first_order_flag,
    created
```

### Key Naming Standards

- **Primary Keys**: `{entity}_id` (e.g., `customer_id`, `order_id`)
- **Foreign Keys**: `{referenced_entity}_id` (e.g., `customer_id` in orders table)
- **Boolean Fields**: `is_{condition}` or `has_{attribute}`
- **Dates**: `{event}_date` or `{event}_at` for timestamps
- **Amounts**: Include currency when applicable (`amount_usd`)
- **Counts**: `{entity}_count` (e.g., `order_count`)

## 📊 Materialization Strategy

### Choosing the Right Materialization

| Materialization | Use Case | Performance | Storage | Freshness |
|-----------------|----------|-------------|---------|-----------|
| **ephemeral** | Staging models, reusable logic | Fast (CTE) | None | Real-time |
| **view** | Simple transformations, always fresh | Medium | Low | Real-time |
| **table** | Complex logic, stable data | Fast | High | Batch refresh |
| **incremental** | Large datasets, append-only | Fast | Medium | Near real-time |

### Materialization Guidelines

```sql
-- Staging: Use ephemeral for performance
{{ config(materialized='ephemeral') }}

-- Intermediate: Use ephemeral for reusable logic
{{ config(materialized='ephemeral') }}

-- Marts: Use table for smaller dimensions
{{ config(materialized='table') }}

-- Large facts and dimensions: Use incremental
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    on_schema_change='fail'
) }}
```

## 🧪 Testing Strategy

### Test Coverage Hierarchy

1. **Primary Keys**: Every model should have a `dbt_constraints.primary_key` test
2. **Foreign Keys**: All relationships should be tested with `dbt_constraints.foreign_key`
3. **Unique Keys**: Business unique constraints with `dbt_constraints.unique_key`
4. **Business Rules**: Critical business logic validation
5. **Data Quality**: Completeness, accuracy, consistency

### Why Use dbt_constraints?

The `dbt_constraints` package provides several advantages over built-in dbt tests:

- **Database Enforcement**: Creates actual database constraints (PK, FK, UK) in Snowflake
- **Performance**: Database-level constraints can improve query optimization
- **Data Integrity**: Prevents invalid data at the database level, not just during dbt runs
- **Documentation**: Constraints are visible in database metadata and BI tools
- **Consistency**: Ensures referential integrity across all data access patterns

### Essential Tests

```yaml
# models/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
        description: "Primary key for customers"
      
      - name: customer_email
        tests:
          - dbt_constraints.unique_key
        description: "Customer email address"
      
      - name: customer_created_at
        tests:
          - not_null
        description: "When customer was created"

  - name: fct_orders
    columns:
      - name: order_id_line_number
        tests:
          - dbt_constraints.unique_key:
              column_names:
                - order_id
                - order_line_number
        description: "Composite unique key for order lines"
      
      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```



### Packages Configuration

```yaml
# packages.yml
packages:
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  - package: brooklyn-data/dbt_artifacts
    version: [">=2.0.0", "<3.0.0"]
  - package: calogica/dbt_expectations
    version: [">=0.10.0", "<1.0.0"]
```

```yaml
# dbt_project.yml - Configure constraint behavior
models:
  your_project:
    +copy_grants: true  # Preserve grants when recreating tables with constraints
    
    # Staging models - minimal constraints
    staging:
      +materialized: ephemeral
      
    # Intermediate models - business logic constraints
    intermediate:
      +materialized: ephemeral
      
    # Marts - full constraint enforcement
    marts:
      +materialized: table
      +post-hook: "{{ dbt_constraints.create_constraints(this) }}"
```

### Constraint Best Practices

1. **Primary Keys**: Use `dbt_constraints.primary_key` on all dimension tables and fact table surrogate keys
2. **Foreign Keys**: Use `dbt_constraints.foreign_key` to enforce all dimensional relationships in fact tables
3. **Unique Keys**: Use `dbt_constraints.unique_key` for natural business keys and alternate keys
4. **Composite Keys**: Use `dbt_constraints.unique_key` with `column_names` list for multi-column unique constraints
5. **Performance**: Constraints can improve query performance through query optimization
6. **Documentation**: Constraints appear in `SHOW TABLES` and BI tool metadata
7. **Layered Approach**: Apply constraints primarily in Gold/Marts layer where data is most stable

### Custom Generic Tests

```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} <= 0
{% endtest %}
```

## 🔧 Performance Optimization

### Query Performance

#### Use Appropriate Joins
```sql
-- ✅ Good: Use appropriate join types
SELECT 
    c.customer_id,
    c.customer_name,
    COALESCE(o.order_count, 0) AS order_count
FROM {{ ref('dim_customers') }} c
LEFT JOIN {{ ref('int_customer_order_counts') }} o
    ON c.customer_id = o.customer_id

-- ❌ Bad: Unnecessary cross joins
SELECT DISTINCT
    c.customer_id,
    c.customer_name
FROM {{ ref('dim_customers') }} c,
     {{ ref('dim_products') }} p
```

#### Optimize Incremental Models
```sql
-- ✅ Good: Efficient incremental logic
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

SELECT *
FROM {{ source('ecommerce', 'orders') }}
{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

### Snowflake-Specific Optimizations

#### Clustering Keys
```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}
```

#### Warehouse Management
```sql
{{ config(
    snowflake_warehouse='TRANSFORM_WH'
) }}
```

## 📝 Documentation Standards

### Model Documentation

```yaml
models:
  - name: dim_customers
    description: |
      Customer dimension table containing all unique customers.
      
      This table is updated daily and includes both active and inactive customers.
      Use this as the primary source for customer attributes in all reporting.
      
      **Grain**: One row per customer
      **Refresh**: Daily at 6 AM UTC
    
    columns:
      - name: customer_id
        description: "Unique identifier for each customer (primary key)"
        tests:
          - not_null
          - unique
      
      - name: customer_tier
        description: |
          Customer tier based on lifetime value:
          - 'bronze': < $1,000 LTV
          - 'silver': $1,000 - $5,000 LTV  
          - 'gold': $5,000+ LTV
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold']
```

### Code Documentation

```sql
-- Purpose: Calculate customer lifetime value and tier assignment
-- Grain: One row per customer
-- Dependencies: stg_orders, stg_customers
-- Business Logic: LTV = sum of all order values for customer

WITH customer_orders AS (
    -- Aggregate order data by customer
    SELECT 
        customer_id,
        COUNT(*) AS order_count,
        SUM(order_total) AS lifetime_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
),

customer_tiers AS (
    -- Assign customer tiers based on LTV
    SELECT 
        *,
        CASE 
            WHEN lifetime_value >= 5000 THEN 'gold'
            WHEN lifetime_value >= 1000 THEN 'silver'
            ELSE 'bronze'
        END AS customer_tier
    FROM customer_orders
)

SELECT * FROM customer_tiers
```

## 🔄 Development Workflow

### Git Workflow

1. **Feature Branches**: Create branches for each feature/fix
2. **Pull Requests**: All changes go through PR review
3. **CI/CD**: Automated testing on all PRs
4. **Deployment**: Automated deployment to production

### Environment Strategy

```yaml
# profiles.yml
dbt_project:
  outputs:
    dev:
      type: snowflake
      schema: "{{ env_var('DBT_USER') }}_dev"
      
    staging:
      type: snowflake  
      schema: "analytics_staging"
      
    prod:
      type: snowflake
      schema: "analytics"
```

### Development Commands

```bash
# Development workflow
dbt deps                    # Install packages
dbt seed                    # Load seed data
dbt run --select +my_model  # Run model and dependencies
dbt test --select my_model  # Test specific model
dbt build                   # Run and test everything

# Production deployment
dbt run --target prod
dbt test --target prod
```

## 🛡️ Data Quality & Governance

### Data Contracts

```yaml
models:
  - name: fct_orders
    config:
      contract:
        enforced: true
    columns:
      - name: order_id
        data_type: varchar
        constraints:
          - type: not_null
          - type: primary_key
      
      - name: order_total
        data_type: number(10,2)
        constraints:
          - type: not_null
```

### Freshness Monitoring

```yaml
sources:
  - name: ecommerce
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    tables:
      - name: orders
        freshness:
          warn_after: {count: 1, period: hour}
```

## 🎯 Advanced Patterns

### Slowly Changing Dimensions (SCD Type 2)

```sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

scd_data AS (
    SELECT 
        customer_id,
        customer_name,
        customer_email,
        -- SCD Type 2 fields
        '{{ run_started_at }}' AS valid_from,
        NULL AS valid_to,
        TRUE AS is_current,
        {{ dbt_utils.generate_surrogate_key(['customer_id', 'customer_name', 'customer_email']) }} AS row_hash
    FROM source_data
)

SELECT * FROM scd_data
```

### Dynamic SQL Generation

```sql
-- Generate pivot columns dynamically
{% set payment_methods_query %}
    SELECT DISTINCT payment_method 
    FROM {{ ref('stg_orders') }}
    ORDER BY payment_method
{% endset %}

{% set results = run_query(payment_methods_query) %}
{% if execute %}
    {% set payment_methods = results.columns[0].values() %}
{% else %}
    {% set payment_methods = [] %}
{% endif %}

SELECT 
    order_date,
    {% for payment_method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ payment_method }}' THEN order_total ELSE 0 END) AS {{ payment_method | replace(' ', '_') | lower }}_total
    {%- if not loop.last -%},{%- endif %}
    {% endfor %}
FROM {{ ref('stg_orders') }}
GROUP BY order_date
```

## 🔍 Debugging & Troubleshooting

### Common Issues & Solutions

#### Compilation Errors
```bash
# Check model compilation
dbt compile --select my_model

# Debug specific model
dbt run --select my_model --debug
```

#### Performance Issues
```sql
-- Use EXPLAIN to analyze query plans
{{ config(pre_hook="EXPLAIN " ~ this) }}
```

#### Data Quality Issues
```bash
# Run tests with detailed output
dbt test --store-failures

# Check test results
SELECT * FROM analytics.dbt_test_failures
```

### Monitoring & Alerting

```yaml
# Set up monitoring for key models
models:
  - name: fct_daily_revenue
    tests:
      - dbt_utils.expression_is_true:
          expression: "revenue_amount > 0"
          config:
            severity: error
            
      - dbt_utils.accepted_range:
          column_name: revenue_amount
          min_value: 0
          max_value: 1000000
          config:
            severity: warn
```

## 📚 Resources & References

### Official Documentation
- [dbt Developer Hub](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [dbt Style Guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md)

### Community Resources
- [dbt Discourse](https://discourse.getdbt.com/)
- [dbt Slack Community](https://www.getdbt.com/community/)
- [dbt Package Hub](https://hub.getdbt.com/)

### Essential Packages

#### Core Packages (Recommended for All Projects)

- [**dbt_constraints**](https://github.com/Snowflake-Labs/dbt_constraints): Database-enforced PK, FK, UK constraints
  - Creates actual database constraints in Snowflake
  - Improves query performance through constraint-based optimization
  - Provides referential integrity at the database level
  - Essential for enterprise data warehouse standards

- [**dbt_utils**](https://github.com/dbt-labs/dbt_utils): Essential macros and utility functions
  - Cross-database compatibility macros
  - Date/time manipulation functions
  - SQL generation helpers (pivot, surrogate_key, etc.)
  - Foundation for most other dbt packages

- [**dbt_artifacts**](https://github.com/brooklyn-data/dbt_artifacts): Execution logging and metadata tracking
  - Tracks dbt run history and performance metrics
  - Enables operational monitoring and alerting
  - Provides insights into model execution patterns
  - Essential for production monitoring

- [**dbt_expectations**](https://github.com/calogica/dbt_expectations): Advanced data quality and profiling tests
  - Statistical data profiling and validation
  - Advanced data quality checks beyond basic tests
  - Great Expectations-style testing framework
  - Comprehensive data quality monitoring

#### Additional Useful Packages
- [dbt-audit-helper](https://github.com/dbt-labs/dbt-audit-helper): Migration and comparison tools
- [dbt-project-evaluator](https://github.com/dbt-labs/dbt-project-evaluator): Project health checks and best practice validation

---

