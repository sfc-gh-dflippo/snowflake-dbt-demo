# Python Models Guide

## Overview

Python models in dbt enable advanced analytics, machine learning, and complex transformations beyond SQL capabilities. They integrate with data science libraries like pandas, scikit-learn, and more.

## When to Use Python Models

✅ **Machine Learning** - Clustering, classification, predictions  
✅ **Statistical Analysis** - Complex calculations, distributions  
✅ **Data Science Workflows** - Feature engineering, model scoring  
✅ **Advanced Transformations** - Operations difficult in SQL  
✅ **Library Integration** - Using Python packages unavailable in SQL  

## Basic Python Model Structure

```python
def model(dbt, session):
    """
    dbt Python model entry point
    
    Args:
        dbt: dbt runtime object with ref(), source(), config
        session: Data warehouse session (Snowpark, Spark, etc.)
    
    Returns:
        DataFrame to materialize as model
    """
    
    # Get configuration
    dbt.config(materialized="table")
    
    # Reference upstream models
    df = dbt.ref("stg_customers").to_pandas()
    
    # Python transformations
    df['new_column'] = df['existing_column'] * 2
    
    return df
```

## Simple Python Model Example

```python
# models/silver/customer_value_segments.py

def model(dbt, session):
    """Segment customers by lifetime value using pandas"""
    
    # Configure as table
    dbt.config(materialized="table")
    
    # Import libraries
    import pandas as pd
    
    # Get customer data
    customers_df = dbt.ref("int_customers__with_orders").to_pandas()
    
    # Create value segments
    def assign_segment(ltv):
        if ltv >= 10000:
            return 'VIP'
        elif ltv >= 5000:
            return 'High Value'
        elif ltv >= 1000:
            return 'Medium Value'
        else:
            return 'Low Value'
    
    customers_df['value_segment'] = customers_df['lifetime_value'].apply(assign_segment)
    
    # Add metadata
    customers_df['dbt_updated_at'] = pd.Timestamp.now()
    
    return customers_df
```

## Machine Learning Example

### Customer Clustering with scikit-learn

```python
# models/silver/customer_clustering.py

def model(dbt, session):
    """Cluster customers using K-Means algorithm"""
    
    dbt.config(
        materialized="table",
        packages=["scikit-learn"]  # Specify required packages
    )
    
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    # Get customer metrics
    df = dbt.ref("int_customers__metrics").to_pandas()
    
    # Select features for clustering
    features = ['total_orders', 'lifetime_value', 'avg_order_value', 'days_since_last_order']
    X = df[features].fillna(0)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    
    # Add cluster centers for interpretation
    centers = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=[f'{feat}_center' for feat in features]
    )
    
    # Label clusters based on characteristics
    def label_cluster(row):
        if row['lifetime_value_center'] > 5000:
            return 'High Value'
        elif row['total_orders_center'] > 10:
            return 'Frequent Buyers'
        elif row['days_since_last_order_center'] > 180:
            return 'At Risk'
        elif row['avg_order_value_center'] > 200:
            return 'High AOV'
        else:
            return 'Regular'
    
    centers['cluster_label'] = centers.apply(label_cluster, axis=1)
    
    # Map labels back to customers
    cluster_labels = dict(enumerate(centers['cluster_label']))
    df['cluster_label'] = df['cluster_id'].map(cluster_labels)
    
    # Add metadata
    df['dbt_updated_at'] = pd.Timestamp.now()
    df['model_version'] = 'kmeans_v1'
    
    return df
```

### Predictive Modeling

```python
# models/gold/customer_churn_prediction.py

def model(dbt, session):
    """Predict customer churn probability"""
    
    dbt.config(
        materialized="table",
        packages=["scikit-learn", "numpy"]
    )
    
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    
    # Get historical customer data with churn labels
    df = dbt.ref("customer_churn_training_data").to_pandas()
    
    # Features for prediction
    feature_cols = [
        'total_orders',
        'lifetime_value',
        'avg_order_value',
        'days_since_last_order',
        'total_returns',
        'support_tickets'
    ]
    
    X = df[feature_cols].fillna(0)
    y = df['is_churned']
    
    # Train model (in production, load pre-trained model)
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    rf_model.fit(X, y)
    
    # Get current customers for scoring
    current_customers = dbt.ref("int_customers__metrics").to_pandas()
    X_score = current_customers[feature_cols].fillna(0)
    
    # Predict churn probability
    current_customers['churn_probability'] = rf_model.predict_proba(X_score)[:, 1]
    
    # Add risk segments
    def assign_risk(prob):
        if prob >= 0.7:
            return 'High Risk'
        elif prob >= 0.4:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    current_customers['churn_risk_segment'] = current_customers['churn_probability'].apply(assign_risk)
    
    # Add metadata
    current_customers['prediction_date'] = pd.Timestamp.now()
    current_customers['model_version'] = 'rf_v1'
    
    return current_customers[['customer_id', 'churn_probability', 'churn_risk_segment', 'prediction_date']]
```

## Time Series Analysis

```python
# models/silver/sales_forecast.py

def model(dbt, session):
    """Generate sales forecasts using time series analysis"""
    
    dbt.config(
        materialized="table",
        packages=["pandas", "numpy"]
    )
    
    import pandas as pd
    import numpy as np
    from datetime import timedelta
    
    # Get historical daily sales
    df = dbt.ref("fct_daily_sales").to_pandas()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df = df.sort_values('sale_date')
    
    # Calculate rolling averages
    df['rolling_7day_avg'] = df['daily_revenue'].rolling(window=7).mean()
    df['rolling_30day_avg'] = df['daily_revenue'].rolling(window=30).mean()
    
    # Calculate year-over-year growth
    df['yoy_growth'] = df['daily_revenue'].pct_change(periods=365)
    
    # Simple forecast (30 days ahead)
    last_date = df['sale_date'].max()
    forecast_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=30,
        freq='D'
    )
    
    # Use 30-day rolling average as baseline forecast
    baseline_forecast = df['rolling_30day_avg'].iloc[-1]
    
    forecast_df = pd.DataFrame({
        'sale_date': forecast_dates,
        'forecast_revenue': baseline_forecast,
        'forecast_type': 'simple_rolling_avg',
        'confidence': 'medium',
        'created_at': pd.Timestamp.now()
    })
    
    # Combine historical and forecast
    result = pd.concat([
        df[['sale_date', 'daily_revenue']].rename(columns={'daily_revenue': 'actual_revenue'}),
        forecast_df[['sale_date', 'forecast_revenue']]
    ], ignore_index=True)
    
    return result
```

## Advanced Transformations

### JSON Processing

```python
# models/silver/parsed_event_data.py

def model(dbt, session):
    """Parse JSON event data into structured columns"""
    
    dbt.config(materialized="table")
    
    import pandas as pd
    import json
    
    # Get raw event data
    events_df = dbt.ref("stg_raw_events").to_pandas()
    
    # Parse JSON column
    events_df['event_properties'] = events_df['event_json'].apply(json.loads)
    
    # Extract nested fields
    events_df['event_type'] = events_df['event_properties'].apply(lambda x: x.get('type'))
    events_df['event_category'] = events_df['event_properties'].apply(lambda x: x.get('category'))
    events_df['event_value'] = events_df['event_properties'].apply(lambda x: x.get('value', 0))
    
    # Extract user properties
    events_df['user_segment'] = events_df['event_properties'].apply(
        lambda x: x.get('user', {}).get('segment', 'unknown')
    )
    
    return events_df[['event_id', 'event_type', 'event_category', 'event_value', 'user_segment']]
```

### Text Analysis

```python
# models/silver/product_review_sentiment.py

def model(dbt, session):
    """Analyze sentiment of product reviews"""
    
    dbt.config(
        materialized="table",
        packages=["textblob"]  # Natural language processing
    )
    
    import pandas as pd
    from textblob import TextBlob
    
    # Get review data
    reviews_df = dbt.ref("stg_product_reviews").to_pandas()
    
    def analyze_sentiment(text):
        if pd.isna(text):
            return 0, 'neutral'
        
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        return polarity, sentiment
    
    # Apply sentiment analysis
    reviews_df[['sentiment_score', 'sentiment_label']] = reviews_df['review_text'].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    
    # Add word count
    reviews_df['review_word_count'] = reviews_df['review_text'].apply(
        lambda x: len(str(x).split()) if pd.notna(x) else 0
    )
    
    return reviews_df
```

## Configuration Options

### Materialization

```python
# Table (default for Python models)
dbt.config(materialized="table")

# Incremental (with Python)
dbt.config(
    materialized="incremental",
    unique_key="customer_id"
)

# View (not recommended for Python - use SQL instead)
dbt.config(materialized="view")
```

### Package Requirements

```python
# Snowflake (Snowpark)
dbt.config(
    packages=["scikit-learn==1.0.2", "pandas==1.5.0"]
)

# Databricks (Spark)
dbt.config(
    packages=["scikit-learn", "pandas", "numpy"]
)
```

## Platform-Specific Considerations

### Snowflake (Snowpark)

```python
def model(dbt, session):
    # Snowpark DataFrames (lazy evaluation)
    df = dbt.ref("stg_customers")  # Returns Snowpark DataFrame
    
    # Convert to Pandas for Python operations
    pandas_df = df.to_pandas()
    
    # Operations on Pandas DataFrame
    pandas_df['new_column'] = pandas_df['old_column'] * 2
    
    # Return Pandas (converted back automatically)
    return pandas_df
```

### Databricks (PySpark)

```python
def model(dbt, session):
    # Spark DataFrames
    df = dbt.ref("stg_customers")  # Returns Spark DataFrame
    
    # Use PySpark operations
    from pyspark.sql import functions as F
    
    df = df.withColumn("new_column", F.col("old_column") * 2)
    
    return df
```

## Testing Python Models

```yaml
# models/_models.yml
models:
  - name: customer_clustering
    description: "Customer segments using K-Means clustering"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      
      - name: cluster_id
        tests:
          - not_null
          - accepted_values:
              values: [0, 1, 2, 3, 4]
      
      - name: cluster_label
        tests:
          - not_null
```

## Best Practices

### 1. Keep Python Models Focused

```python
# ✅ Good: Focused on specific analytical task
def model(dbt, session):
    df = dbt.ref("customer_data").to_pandas()
    # Apply ML model
    return df

# ❌ Bad: Mixing data cleaning with ML
def model(dbt, session):
    df = dbt.source("raw", "customers").to_pandas()
    # Data cleaning (should be in SQL staging)
    # ML operations
    return df
```

### 2. Use SQL for Data Preparation

```python
# ✅ Good: SQL handles joins/filters, Python for analytics
def model(dbt, session):
    # SQL already did the heavy lifting
    df = dbt.ref("int_customers__prepared").to_pandas()
    # Python only for ML
    return df
```

### 3. Handle Missing Data

```python
# Always handle nulls/NaN
df['feature'] = df['feature'].fillna(0)

# Or drop rows with missing values
df = df.dropna(subset=['critical_column'])
```

### 4. Add Model Metadata

```python
import pandas as pd

df['model_version'] = 'v1.0'
df['prediction_date'] = pd.Timestamp.now()
df['dbt_updated_at'] = pd.Timestamp.now()
```

## Performance Considerations

### Optimize Data Loading

```python
# ✅ Good: Select only needed columns in SQL
dbt.ref("large_table").select("customer_id", "order_total").to_pandas()

# ❌ Bad: Loading entire large table to Pandas
dbt.ref("large_table").to_pandas()
```

### Use Appropriate Materializations

```python
# Large datasets: Use incremental
dbt.config(
    materialized="incremental",
    unique_key="customer_id"
)
```

## Troubleshooting

### Common Issues

**Issue:** `ImportError: No module named 'sklearn'`  
**Solution:** Add to config: `dbt.config(packages=["scikit-learn"])`

**Issue:** Out of memory errors  
**Solution:** Process data in chunks or use SQL for heavy lifting

**Issue:** Slow model execution  
**Solution:** Optimize data preparation in SQL, use sampling in dev

---

**Related Documentation:**
- `STAGING_MODELS.md` - Prepare data in SQL first
- `INTERMEDIATE_MODELS.md` - SQL vs Python decision
- `PERFORMANCE_OPTIMIZATION.md` - Python model optimization
- Official: [dbt Python Models](https://docs.getdbt.com/docs/build/python-models)

