---
name: dbt-materializations
description:
  Choosing and implementing dbt materializations (ephemeral, view, table, incremental, snapshots,
  Python models). Use this skill when deciding on materialization strategy, implementing incremental
  models, setting up snapshots for SCD Type 2 tracking, or creating Python models for machine
  learning workloads.
---

# dbt Materializations

## Purpose

Transform AI agents into experts on dbt materializations, providing guidance on choosing the right
materialization strategy based on model purpose, size, update frequency, and query patterns, plus
implementation details for each type including advanced features like snapshots and Python models.

## When to Use This Skill

Activate this skill when users ask about:

- Choosing the right materialization for a model
- Implementing incremental models with merge/append/delete+insert strategies
- Setting up snapshots for SCD Type 2 historical tracking
- Converting table materializations to incremental
- Creating Python models for ML or advanced analytics
- Understanding trade-offs between ephemeral, view, and table
- Optimizing materialization performance
- Implementing slowly changing dimensions

**Official dbt Documentation**:
[Materializations](https://docs.getdbt.com/docs/build/materializations)

---

## Decision Matrix

| Materialization | Use Case                | Build Time | Storage | Query Speed | Best For          |
| --------------- | ----------------------- | ---------- | ------- | ----------- | ----------------- |
| **ephemeral**   | Staging, reusable logic | Fast (CTE) | None    | N/A         | Bronze layer      |
| **view**        | Simple transforms       | Fast       | Minimal | Slow        | Always-fresh data |
| **table**       | Complex logic           | Slow       | High    | Fast        | Dimensions        |
| **incremental** | Large datasets          | Fast       | Medium  | Fast        | Large facts       |

---

## Ephemeral Materialization

**When to Use**: Staging models, reusable intermediate logic that doesn't need to be queried
directly

```sql
{{ config(materialized='ephemeral') }}

select
    customer_id,
    customer_name,
    upper(trim(email)) as email_clean
from {{ source('crm', 'customers') }}
```

**How it Works**:

- Compiled as CTE in downstream models
- No physical table created
- Zero storage cost
- Cannot be queried directly

**Best For**:

- Bronze/staging layer models
- Reusable intermediate transformations
- Models referenced by only 1-2 downstream models

**Performance Note**: If an ephemeral model is referenced by many downstream models or contains
complex logic, consider changing to `table` materialization to avoid recomputing.

---

## View Materialization

**When to Use**: Simple transformations where you always need fresh data and query performance isn't
critical

```sql
{{ config(materialized='view') }}

select
    customer_id,
    count(*) as order_count,
    sum(order_amount) as total_spent
from {{ ref('stg_orders') }}
group by customer_id
```

**How it Works**:

- Creates database view
- Query runs every time view is accessed
- Minimal storage (just view definition)
- Always shows latest data

**Best For**:

- Simple aggregations
- Always-fresh reporting needs
- Development/prototyping

**When to Avoid**:

- Complex transformations
- Frequently queried models
- Performance-critical queries

---

## Table Materialization

**When to Use**: Dimensions, complex transformations, frequently queried models

```sql
{{ config(
    materialized='table',
    cluster_by=['order_date']  -- Snowflake optimization
) }}

select
    customer_id,
    customer_name,
    count(distinct order_id) as lifetime_orders,
    sum(order_amount) as lifetime_value,
    min(order_date) as first_order_date
from {{ ref('stg_customers') }} c
join {{ ref('stg_orders') }} o using (customer_id)
group by customer_id, customer_name
```

**How it Works**:

- Drops and recreates table on every run (DROP + CREATE TABLE AS)
- Full refresh every time
- Fast query performance
- Higher storage cost

**Best For**:

- Dimension tables
- Gold layer marts
- Complex silver layer transformations
- Models with frequent queries

**Performance Optimization**:

```sql
{{ config(
    materialized='table',
    cluster_by=['date_column', 'category'],  -- Snowflake clustering
    snowflake_warehouse='LARGE_WH'  -- Custom warehouse for complex logic
) }}
```

---

## Incremental Materialization

**When to Use**: Large fact tables (millions+ rows), time-series data, event logs, append-only data

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at'],
    cluster_by=['order_date', 'customer_id']
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    order_status,
    {% if is_incremental() %}
        dbt_inserted_at,  -- Preserve from first insert
    {% else %}
        current_timestamp() as dbt_inserted_at,
    {% endif %}
    current_timestamp() as dbt_updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new/updated records
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**How it Works**:

- First run: Loads all data (acts like table)
- Subsequent runs: Insert/update only new records
- Uses `unique_key` to identify records
- Dramatically faster builds for large tables

**Performance Benefits**:

- Reduces build time from hours to minutes
- Lower compute costs
- Enables more frequent refreshes

---

### Incremental Strategies

#### 1. Merge Strategy (Most Common)

**Use For**: Updateable records, handling late-arriving data, SCD Type 1

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at']  -- Preserve original timestamp
) }}

select
    order_id,
    customer_id,
    order_status,  -- Can change over time
    order_amount,
    {% if is_incremental() %}
        dbt_inserted_at,
    {% else %}
        current_timestamp() as dbt_inserted_at,
    {% endif %}
    current_timestamp() as dbt_updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**How It Works**:

- Matches on `unique_key`
- Updates existing records
- Inserts new records
- Preserves columns in `merge_exclude_columns`

---

#### 2. Append Strategy (Fastest)

**Use For**: Immutable event data, logs, clickstreams

```sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='append'
) }}

select
    event_id,
    user_id,
    event_type,
    event_timestamp,
    event_properties
from {{ ref('stg_events') }}

{% if is_incremental() %}
    where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

**How It Works**:

- Only inserts new records
- No updates or deletes
- Fastest incremental strategy
- Assumes data is immutable

---

#### 3. Delete+Insert Strategy

**Use For**: Partitioned data, date-based reprocessing

```sql
{{ config(
    materialized='incremental',
    unique_key='order_date',
    incremental_strategy='delete+insert'
) }}

select
    order_date,
    customer_id,
    count(*) as daily_orders,
    sum(order_amount) as daily_revenue
from {{ ref('stg_orders') }}
group by order_date, customer_id

{% if is_incremental() %}
    where order_date >= dateadd(day, -7, current_date())  -- Reprocess last 7 days
{% endif %}
```

**How It Works**:

- Deletes records matching `unique_key` values
- Inserts all new records
- Good for reprocessing entire partitions

**Official dbt Docs**: [Incremental Models](https://docs.getdbt.com/docs/build/incremental-models)

---

### Incremental Best Practices

**1. Always Include is_incremental() Check**

```sql
{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**2. Add Lookback for Late Data**

```sql
{% if is_incremental() %}
    where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))
{% endif %}
```

**3. Limit Source Scans**

```sql
{% if is_incremental() %}
    -- Only scan recent source data
    where source_updated_at >= dateadd(day, -30, current_date())
      and source_updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**4. Use Clustering for Performance**

```sql
{{ config(
    cluster_by=['event_date', 'user_id']  -- Commonly filtered/joined columns
) }}
```

**5. Handle Full Refresh**

```bash
# Force rebuild from scratch
dbt build --full-refresh --select model_name
```

---

## Snapshots (SCD Type 2)

**Purpose**: Track historical changes to slowly changing dimensions

**When to Use**: Customer attributes, product catalogs, employee records, pricing history

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

**Generated Columns**:

- `dbt_valid_from` - When record became active
- `dbt_valid_to` - When record was superseded (NULL for current)
- `dbt_scd_id` - Unique identifier for each version
- `dbt_updated_at` - Last snapshot processing time

---

### Snapshot Strategies

#### Timestamp Strategy (Recommended)

**Use When**: Source has reliable `updated_at` timestamp

```sql
{% snapshot customers_snapshot_timestamp %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}

select * from {{ source('crm', 'customers') }}

{% endsnapshot %}
```

**Advantages**:

- Faster performance
- Only checks timestamp
- More efficient

---

#### Check Strategy

**Use When**: No reliable timestamp, need to check specific columns

```sql
{% snapshot customers_snapshot_check %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'customer_email', 'customer_tier']
    )
}}

select * from {{ source('crm', 'customers') }}

{% endsnapshot %}
```

**Advantages**:

- Works without timestamp
- Tracks specific column changes
- More control over what triggers new version

---

### Querying Snapshots

**Get Current Records Only**:

```sql
select *
from {{ ref('dim_customers_scd') }}
where dbt_valid_to is null
```

**Point-in-Time Query**:

```sql
select *
from {{ ref('dim_customers_scd') }}
where '2024-01-15' between dbt_valid_from and coalesce(dbt_valid_to, '9999-12-31')
```

**Change History**:

```sql
select
    customer_id,
    customer_name,
    dbt_valid_from,
    dbt_valid_to
from {{ ref('dim_customers_scd') }}
order by customer_id, dbt_valid_from
```

**Running Snapshots**:

```bash
dbt snapshot  # Runs all snapshots
dbt snapshot --select dim_customers_scd  # Specific snapshot
```

**Official dbt Docs**: [Snapshots](https://docs.getdbt.com/docs/build/snapshots)

---

## Python Models

**Purpose**: Machine learning, statistical analysis, complex transformations beyond SQL

**When to Use**: ML models, clustering, advanced analytics, Python library integration (pandas,
scikit-learn, etc.)

```python
# models/silver/customer_clustering.py

def model(dbt, session):
    """Cluster customers using K-Means"""

    dbt.config(
        materialized="table",
        packages=["scikit-learn", "pandas"]
    )

    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    # Get data from dbt model
    df = dbt.ref("int_customers__metrics").to_pandas()

    # Select features
    features = ['total_orders', 'lifetime_value', 'avg_order_value']
    X = df[features].fillna(0)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    df['cluster_label'] = df['cluster_id'].map({
        0: 'Low Value',
        1: 'Medium Value',
        2: 'High Value',
        3: 'VIP',
        4: 'At Risk'
    })

    # Return final dataframe
    return df[['customer_id', 'cluster_id', 'cluster_label'] + features]
```

### Python Model Best Practices

**1. Use SQL for Data Preparation**

```python
# Let SQL handle filtering, joins, aggregations
df = dbt.ref("int_customers__prepared").to_pandas()
```

**2. Python for ML/Complex Analytics Only**

```python
# Don't use Python for simple transformations
# Use SQL instead
```

**3. Specify Required Packages**

```python
dbt.config(
    packages=["scikit-learn==1.3.0", "pandas", "numpy"]
)
```

**4. Test Python Models**

```yaml
# Can use standard dbt tests
models:
  - name: customer_clustering
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      - name: cluster_id
        tests:
          - not_null
          - accepted_values:
              values: [0, 1, 2, 3, 4]
```

**Official dbt Docs**: [Python Models](https://docs.getdbt.com/docs/build/python-models)

---

## When to Change Materializations

### Change Ephemeral/View to Table When:

1. **Model is Referenced Multiple Times**

   - If 3+ downstream models reference it
   - Avoids recomputing same logic

2. **Complex Transformations**

   - Heavy aggregations or window functions
   - Self-joins or complex CTEs

3. **Memory Issues**
   - Queries failing due to memory constraints
   - CTE becoming too large

### Change Table to Incremental When:

1. **Large Data Volumes**

   - Table has millions+ rows
   - Full refresh takes > 5 minutes

2. **Time-Series Data**

   - Append-only event logs
   - Daily/hourly data loads

3. **Performance Requirements**
   - Need faster, more frequent refreshes
   - Cost optimization needed

---

## Folder-Level Configuration

Configure materializations at folder level in `dbt_project.yml`:

```yaml
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

**Override at model level** only for special cases (incremental, Python, etc.).

---

## Helping Users Choose Materializations

### Strategy for Assisting Users

When users ask about materializations:

1. **Understand purpose**: What is the model for?
2. **Assess size**: How many rows? How often updated?
3. **Check usage**: How many downstream models? Query frequency?
4. **Recommend materialization**: Based on layer and requirements
5. **Provide configuration**: Complete working example
6. **Explain trade-offs**: Build time, storage, query performance

### Common User Questions

**"Should this be ephemeral or table?"**

- Ephemeral: Staging, lightweight intermediate models
- Table: Dimensions, marts, complex intermediate models
- Consider: Reusability, complexity, downstream usage

**"When should I use incremental?"**

- Large tables (millions+ rows)
- Time-series or append-only data
- Performance/cost optimization needed
- Full rebuild takes too long

**"How do I set up SCD Type 2?"**

- Use snapshots with timestamp or check strategy
- Configure unique_key and updated_at
- Query with dbt_valid_to IS NULL for current records

---

## Related Official Documentation

- [dbt Docs: Materializations](https://docs.getdbt.com/docs/build/materializations)
- [dbt Docs: Incremental Models](https://docs.getdbt.com/docs/build/incremental-models)
- [dbt Docs: Snapshots](https://docs.getdbt.com/docs/build/snapshots)
- [dbt Docs: Python Models](https://docs.getdbt.com/docs/build/python-models)

---

**Goal**: Transform AI agents into experts on dbt materializations who guide users to optimal
materialization choices based on data characteristics, usage patterns, and performance requirements.
