# dbt Testing Strategy

## Overview

Implement tests in this order for maximum data quality: Primary Keys → Foreign Keys → Unique Keys → Business Rules → Data Quality.

**Official dbt Documentation**: [Testing](https://docs.getdbt.com/docs/build/tests)

---

## Why Use dbt_constraints?

The `dbt_constraints` package provides database-level enforcement (not just dbt tests):

✅ **Database Enforcement** - Creates actual constraints in the data warehouse  
✅ **Performance** - Database-level constraints improve query optimization  
✅ **Data Integrity** - Prevents invalid data at all access points  
✅ **Documentation** - Constraints visible in database metadata and BI tools  

**Official dbt_constraints Documentation**: [GitHub - Snowflake-Labs/dbt_constraints](https://github.com/Snowflake-Labs/dbt_constraints)

---

## Package Installation

```yaml
# packages.yml
packages:
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
```

Run `dbt deps` to install.

---

## Primary Key Testing

### Simple Primary Key (dbt_constraints)
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

### Composite Primary Key
```yaml
models:
  - name: fct_order_lines
    tests:
      - dbt_constraints.primary_key:
          column_names:
            - order_id
            - line_number
```

### Alternative (Built-in dbt)
```yaml
columns:
  - name: product_id
    tests:
      - not_null
      - unique
```

---

## Foreign Key Testing

### Simple Foreign Key (dbt_constraints)
```yaml
models:
  - name: fct_orders
    columns:
      - name: customer_id
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

### Alternative (Built-in dbt)
```yaml
columns:
  - name: customer_id
    tests:
      - relationships:
          to: ref('dim_customers')
          field: customer_id
```

---

## Generic Tests

### dbt_utils Tests
```yaml
columns:
  - name: customer_email
    tests:
      - dbt_utils.not_null_proportion:
          at_least: 0.95
  
  - name: customer_status
    tests:
      - dbt_utils.accepted_range:
          min_value: 0
```

**Official dbt_utils Documentation**: [dbt_utils - Generic Tests](https://github.com/dbt-labs/dbt-utils#generic-tests)

### Custom Generic Test
```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}
    select count(*)
    from {{ model }}
    where {{ column_name }} <= 0
{% endtest %}
```

**Usage**:
```yaml
columns:
  - name: order_total
    tests:
      - positive_values
```

---

## Singular Tests

```sql
-- tests/singular/test_order_dates_sequential.sql
with date_validation as (
    select
        o.order_id,
        o.order_date,
        c.signup_date
    from {{ ref('fct_orders') }} o
    join {{ ref('dim_customers') }} c on o.customer_id = c.customer_id
    where o.order_date < c.signup_date
)

select * from date_validation
```

**Official dbt Documentation**: [Singular Tests](https://docs.getdbt.com/docs/build/tests#singular-tests)

---

## Testing by Layer

### Bronze Layer (Staging)
```yaml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

**Focus**: Basic data quality at source

---

### Silver Layer (Intermediate)
```yaml
models:
  - name: int_customers__with_orders
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      - name: lifetime_orders
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**Focus**: Business rule validation, calculated fields

---

### Gold Layer (Marts)
```yaml
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

**Focus**: Comprehensive constraint enforcement with dbt_constraints

---

## Test Configuration

### Store Test Failures
```bash
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
columns:
  - name: customer_email
    tests:
      - dbt_constraints.unique_key:
          config:
            severity: warn  # or 'error'
```

---

## Running Tests

```bash
# Run all tests
dbt test

# Test specific model
dbt test --select dim_customers

# Test by type
dbt test --select test_type:generic
dbt test --select test_type:singular

# Test with dependencies
dbt test --select +dim_customers+
```

**Official dbt Documentation**: [Test Selection](https://docs.getdbt.com/reference/node-selection/test-selection-examples)

---

## Best Practices

1. **Test Early and Often** - Add tests as you build models
2. **Layer-Appropriate Testing**:
   - Bronze: Basic not_null and unique tests
   - Silver: Business rule validation
   - Gold: Comprehensive constraint enforcement
3. **Use dbt_constraints** - Database-level constraints for marts

---

## Testing Checklist

Before moving to production:

- [ ] All dimensions have primary key tests
- [ ] All facts have foreign key tests
- [ ] Business rules are validated
- [ ] Data quality tests are in place
- [ ] Tests run successfully in CI/CD
- [ ] dbt_constraints enabled for marts

---

## Related Documentation

- [Official dbt Docs: Tests](https://docs.getdbt.com/docs/build/tests)
- [dbt_constraints Package](https://github.com/Snowflake-Labs/dbt_constraints)
- [dbt_utils Generic Tests](https://github.com/dbt-labs/dbt-utils#generic-tests)
- `PROJECT_STRUCTURE.md` - Layer-specific patterns and testing by layer
