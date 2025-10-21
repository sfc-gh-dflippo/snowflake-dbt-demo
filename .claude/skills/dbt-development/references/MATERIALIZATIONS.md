# dbt Materializations Guide

## Overview

Materialization determines how dbt builds models in the warehouse. Choose based on model purpose, size, update frequency, and query patterns.

**Official dbt Documentation**: [Materializations](https://docs.getdbt.com/docs/build/materializations)

---

## Decision Matrix

| Materialization | Use Case | Build Time | Storage | Query Speed | Best For |
|-----------------|----------|------------|---------|-------------|----------|
| **ephemeral** | Staging, reusable logic | Fast (CTE) | None | N/A | Bronze layer |
| **view** | Simple transforms | Fast | Minimal | Slow | Always-fresh data |
| **table** | Complex logic | Slow | High | Fast | Dimensions |
| **incremental** | Large datasets | Fast | Medium | Fast | Large facts |

---

## Materialization Types

### Ephemeral

**When to Use**: Staging models, reusable intermediate logic

```sql
{{ config(materialized='ephemeral') }}

select
    customer_id,
    customer_name
from {{ source('crm', 'customers') }}
```

**How it Works**: Compiled as CTE in downstream models. No physical table created.

---

### View

**When to Use**: Simple transformations, always need fresh data

```sql
{{ config(materialized='view') }}

select
    customer_id,
    count(*) as order_count
from {{ ref('stg_orders') }}
group by customer_id
```

**How it Works**: Creates database view. Query runs every time view is queried.

---

### Table

**When to Use**: Dimensions, complex transformations, frequently queried models

```sql
{{ config(
    materialized='table',
    cluster_by=['order_date']  -- Snowflake optimization
) }}

select
    customer_id,
    count(*) as lifetime_orders,
    sum(total_price) as lifetime_value
from {{ ref('stg_orders') }}
group by customer_id
```

**How it Works**: Drops and recreates table on every run. Fast query performance.

---

### Incremental

**When to Use**: Large fact tables (millions+ rows), time-series data, event logs

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    cluster_by=['order_date', 'customer_id']
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    current_timestamp() as dbt_updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new/updated records
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**How it Works**: First run loads all data. Subsequent runs insert/update only new records.

#### Incremental Strategies

**Append** (fastest): Immutable event data
```sql
{{ config(incremental_strategy='append') }}
```

**Merge** (most common): Updateable records, handles late-arriving data
```sql
{{ config(
    incremental_strategy='merge',
    unique_key='order_id',
    merge_exclude_columns=['dbt_inserted_at']  -- Preserve metadata
) }}
```

**Delete+Insert**: Partitioned data, date-based updates
```sql
{{ config(
    incremental_strategy='delete+insert',
    unique_key='order_date'
) }}
```

**Official dbt Docs**: [Incremental Models](https://docs.getdbt.com/docs/build/incremental-models)

---

## Snapshots (SCD Type 2)

**Purpose**: Track historical changes to slowly changing dimensions.

**When to Use**: Customer attributes, product catalogs, employee records

```sql
-- snapshots/dim_customers_scd.sql
{% snapshot dim_customers_scd %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

select * from {{ ref('stg_customers') }}

{% endsnapshot %}
```

**Generated Columns**: `dbt_valid_from`, `dbt_valid_to`, `dbt_scd_id`, `dbt_updated_at`

**Snapshot Strategies**:
- **Timestamp**: Tracks changes based on `updated_at` column (faster, requires reliable timestamp)
- **Check**: Compares specified columns (works without timestamp, slower)

**Querying Current Records**:
```sql
select * from {{ ref('dim_customers_scd') }}
where dbt_valid_to is null
```

**Official dbt Docs**: [Snapshots](https://docs.getdbt.com/docs/build/snapshots)

---

## Python Models

**Purpose**: Machine learning, statistical analysis, complex transformations beyond SQL

**When to Use**: ML models, clustering, advanced analytics, Python library integration

```python
# models/silver/customer_clustering.py

def model(dbt, session):
    """Cluster customers using K-Means"""
    
    dbt.config(
        materialized="table",
        packages=["scikit-learn"]
    )
    
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    # Get data
    df = dbt.ref("int_customers__metrics").to_pandas()
    
    # Features
    X = df[['total_orders', 'lifetime_value']].fillna(0)
    
    # Standardize and cluster
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    
    return df
```

**Best Practices**:
- Use SQL for data preparation
- Python for ML/complex analytics only
- Test with standard dbt tests

**Official dbt Docs**: [Python Models](https://docs.getdbt.com/docs/build/python-models)

---

## Folder-Level Configuration

Configure materializations at the folder level to minimize repetition:

```yaml
# dbt_project.yml
models:
  your_project:
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
    
    silver:
      +materialized: ephemeral
      +tags: ["silver"]
    
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
```

**Override at model level** only for special cases:
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}
```

---

## Performance Tips

**Clustering** (Snowflake):
```sql
{{ config(
    materialized='table',
    cluster_by=['date_column', 'customer_id']
) }}
```

**Warehouse Sizing** (Snowflake):
```sql
{{ config(
    snowflake_warehouse='LARGE_WH'
) }}
```

**Limit Incremental Scans**:
```sql
{% if is_incremental() %}
    -- Only scan recent data in source
    where order_date >= dateadd(day, -30, current_date())
      and updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

---

## Related Documentation

- [Official dbt Docs: Materializations](https://docs.getdbt.com/docs/build/materializations)
- [Official dbt Docs: Incremental Models](https://docs.getdbt.com/docs/build/incremental-models)
- [Official dbt Docs: Snapshots](https://docs.getdbt.com/docs/build/snapshots)
- [Official dbt Docs: Python Models](https://docs.getdbt.com/docs/build/python-models)
- `PROJECT_STRUCTURE.md` - Layer-specific patterns and templates
- `PERFORMANCE_OPTIMIZATION.md` - Snowflake optimizations
