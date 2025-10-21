# dbt Testing Strategy

## Testing Hierarchy

Implement tests in this order for maximum data quality and integrity:

1. **Primary Keys** - Database-enforced uniqueness and not-null
2. **Foreign Keys** - Referential integrity between tables
3. **Unique Keys** - Business key uniqueness
4. **Business Rules** - Domain-specific validation
5. **Data Quality** - Completeness, accuracy, consistency

## Why Use dbt_constraints?

The `dbt_constraints` package provides database-level enforcement (not just dbt tests):

✅ **Database Enforcement** - Creates actual constraints in the data warehouse  
✅ **Performance** - Database-level constraints improve query optimization  
✅ **Data Integrity** - Prevents invalid data at all access points  
✅ **Documentation** - Constraints visible in database metadata and BI tools  
✅ **Consistency** - Ensures referential integrity across all query patterns  

## Package Installation

```yaml
# packages.yml
packages:
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  - package: calogica/dbt_expectations
    version: [">=0.10.0", "<1.0.0"]
```

Run `dbt deps` to install.

## Primary Key Testing

### Simple Primary Key
```yaml
# models/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        description: "Unique identifier for customers"
        tests:
          - dbt_constraints.primary_key
```

### Composite Primary Key
```yaml
models:
  - name: fct_order_lines
    columns:
      - name: order_line_id
        description: "Composite key: order_id + line_number"
        tests:
          - dbt_constraints.unique_key:
              column_names:
                - order_id
                - line_number
```

### Built-in dbt Tests (Alternative)
```yaml
models:
  - name: dim_products
    columns:
      - name: product_id
        tests:
          - not_null
          - unique
```

## Foreign Key Testing

### Simple Foreign Key
```yaml
models:
  - name: fct_orders
    columns:
      - name: customer_id
        description: "Links to dim_customers"
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

### Multiple Foreign Keys
```yaml
models:
  - name: fct_order_lines
    columns:
      - name: order_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_orders')
              pk_column_name: order_id
      
      - name: product_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_products')
              pk_column_name: product_id
```

### Built-in Relationships (Alternative)
```yaml
models:
  - name: fct_orders
    columns:
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

## Unique Key Testing

### Business Key Uniqueness
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_email
        description: "Business unique key"
        tests:
          - dbt_constraints.unique_key
```

### Composite Unique Key
```yaml
models:
  - name: dim_products
    tests:
      - dbt_constraints.unique_key:
          column_names:
            - product_sku
            - supplier_id
```

## Generic Tests

### Create Custom Generic Test
```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}
    select count(*)
    from {{ model }}
    where {{ column_name }} <= 0
{% endtest %}
```

### Use Custom Generic Test
```yaml
models:
  - name: fct_orders
    columns:
      - name: order_total
        tests:
          - positive_values
```

### dbt_utils Generic Tests
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_email
        tests:
          - dbt_utils.not_null_proportion:
              at_least: 0.95
      
      - name: customer_status
        tests:
          - dbt_utils.accepted_values:
              values: ['active', 'inactive', 'suspended']
      
      - name: customer_id
        tests:
          - dbt_utils.unique_combination_of_columns:
              combination_of_columns:
                - customer_id
                - effective_date
```

### dbt_expectations Tests
```yaml
models:
  - name: fct_orders
    columns:
      - name: order_total
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000000
      
      - name: order_date
        tests:
          - dbt_expectations.expect_column_values_to_be_of_type:
              column_type: date
```

## Singular Tests

### Create Singular Test
```sql
-- tests/singular/test_customer_balance_distribution.sql
-- Ensure customer account balances follow expected distribution

with validation as (
    select count(*) as invalid_count
    from {{ ref('dim_customers') }}
    where account_balance < -10000
       or account_balance > 1000000
)

select invalid_count
from validation
where invalid_count > 0
```

### Business Rule Validation
```sql
-- tests/singular/test_order_dates_sequential.sql
-- Ensure order dates are not before customer signup dates

with date_validation as (
    select
        o.order_id,
        o.order_date,
        c.signup_date
    from {{ ref('fct_orders') }} o
    join {{ ref('dim_customers') }} c
      on o.customer_id = c.customer_id
    where o.order_date < c.signup_date
)

select *
from date_validation
```

## Testing by Layer

### Bronze Layer (Staging)
```yaml
# models/bronze/_models.yml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique
      
      - name: customer_name
        tests:
          - not_null
```

**Recommendations:**
- Test primary keys (not_null + unique)
- Validate critical fields are not null
- Keep tests simple and fast
- Focus on data quality at source

### Silver Layer (Intermediate)
```yaml
# models/silver/_models.yml
models:
  - name: int_customers__with_orders
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique
      
      - name: lifetime_orders
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**Recommendations:**
- Test aggregation logic
- Validate calculated fields
- Test business rules
- Ensure referential integrity

### Gold Layer (Marts)
```yaml
# models/gold/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      
      - name: customer_tier
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
  
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - dbt_constraints.primary_key
      
      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

**Recommendations:**
- Use dbt_constraints for database enforcement
- Test all foreign keys
- Validate business metrics
- Add comprehensive data quality tests

## Test Configuration

### Model-Level Test Configuration
```yaml
models:
  - name: fct_orders
    tests:
      - dbt_utils.expression_is_true:
          expression: "order_total >= 0"
          config:
            severity: error
            
      - dbt_utils.recency:
          datepart: day
          field: order_date
          interval: 1
          config:
            severity: warn
```

### Store Test Failures
```bash
# Run tests and store failures for analysis
dbt test --store-failures
```

```yaml
# dbt_project.yml
tests:
  +store_failures: true
  +schema: dbt_test_failures
```

### Test Severity Levels
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_email
        tests:
          - unique:
              config:
                severity: warn  # or 'error'
```

## Running Tests

### Run All Tests
```bash
dbt test
```

### Run Tests for Specific Model
```bash
dbt test --select dim_customers
```

### Run Tests by Type
```bash
# Run only generic tests
dbt test --select test_type:generic

# Run only singular tests
dbt test --select test_type:singular
```

### Run Tests by Tag
```bash
# Tag tests in schema.yml
tests:
  - name: test_customer_balance
    config:
      tags: ["critical"]

# Run tagged tests
dbt test --select tag:critical
```

### Run Tests with Selection Syntax
```bash
# Test model and all upstream dependencies
dbt test --select +dim_customers

# Test model and all downstream dependencies
dbt test --select dim_customers+

# Test model and all dependencies
dbt test --select +dim_customers+
```

## Best Practices

### 1. Test Early and Often
- Add tests as you build models
- Run tests frequently during development
- Fix test failures immediately

### 2. Layer-Appropriate Testing
- **Bronze**: Basic not_null and unique tests
- **Silver**: Business rule validation
- **Gold**: Comprehensive constraint enforcement

### 3. Use dbt_constraints for Production
- Database-level constraints for marts
- Improves query performance
- Ensures data integrity

### 4. Document Test Failures
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique:
              config:
                error_if: ">1000"  # Threshold for failure
                warn_if: ">100"    # Threshold for warning
```

### 5. Create Reusable Tests
```sql
-- tests/generic/test_valid_email.sql
{% test valid_email(model, column_name) %}
    select count(*)
    from {{ model }}
    where {{ column_name }} not like '%_@__%.__%'
{% endtest %}
```

## Troubleshooting

### Test Failures Analysis
```bash
# Store failures for investigation
dbt test --store-failures

# Query failed test results
select * from dbt_test_failures.unique_dim_customers_customer_id
```

### Performance Optimization
```yaml
# Limit rows for faster testing in dev
models:
  - name: fct_orders
    config:
      limit: 1000  # Only in dev target
```

### Debugging Tests
```bash
# Compile test to see generated SQL
dbt compile --select test_name

# View compiled test SQL
cat target/compiled/your_project/tests/test_name.sql
```

## Testing Checklist

### Before Moving to Production

- [ ] All dimensions have primary key tests
- [ ] All facts have foreign key tests
- [ ] Business rules are validated
- [ ] Data quality tests are in place
- [ ] Tests run successfully in CI/CD
- [ ] Test failures are documented
- [ ] dbt_constraints enabled for marts

---

**Related Documentation:**
- `STAGING_MODELS.md` - Bronze layer testing
- `INTERMEDIATE_MODELS.md` - Silver layer testing
- `MARTS_MODELS.md` - Gold layer testing
- `QUICK_REFERENCE.md` - Test command cheatsheet

