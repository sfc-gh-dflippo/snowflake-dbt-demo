# dbt Naming Conventions

## Model Naming

| Layer | Prefix | Example | Purpose |
|-------|--------|---------|---------|
| Staging | stg_ | stg_salesforce__accounts | Clean source data |
| Intermediate | int_ | int_customers__with_orders | Business logic |
| Dimensions | dim_ | dim_customers | Business entities |
| Facts | fct_ | fct_orders | Business processes |

## Column Naming Standards

### Primary & Foreign Keys
- `{entity}_id` - customer_id, order_id, product_id
- Foreign keys use same naming as primary key in related table

### Boolean Flags
- `is_{condition}` - is_active, is_deleted, is_first_order
- `has_{attribute}` - has_orders, has_discount

### Dates & Timestamps
- `{event}_date` - order_date, created_date
- `{event}_at` - created_at, updated_at, deleted_at
- Always use UTC timezone suffix if needed - created_at_utc

### Metrics & Aggregates
- `{metric}_count` - order_count, customer_count
- `{metric}_amount` - total_amount, discount_amount
- Include currency suffix if applicable - amount_usd, price_eur

### Row Numbers & Sequences
- `{entity}_row_number` - order_row_number
- `{entity}_seq_number` - sequence_number

## Consistency Rules

✅ **DO:**
- Use snake_case for all column names
- Use consistent entity names across models
- Include currency/units in column names when relevant
- Keep names concise but descriptive

❌ **DON'T:**
- Mix naming styles (camelCase vs snake_case)
- Use abbreviations inconsistently
- Create ambiguous names without context
- Use reserved SQL keywords

## Examples

```sql
-- ✅ Good: Consistent, clear naming
SELECT
    customer_id,
    customer_name,
    email_address,
    is_active,
    lifetime_value_usd,
    first_order_date,
    last_order_date,
    total_orders_count,
    created_at_utc

-- ❌ Bad: Inconsistent and unclear
SELECT
    cust_id,
    name,
    email,
    active_flag,
    ltv,
    first_ord,
    last_ord,
    cnt,
    created_ts
```
