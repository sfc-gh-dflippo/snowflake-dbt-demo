import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def model(dbt, session):
    """
    SILVER RUN: Customer clustering using Python and scikit-learn
    Complexity: Advanced - Python models, ML integration, data science
    Features demonstrated: Python models, ML libraries, advanced analytics
    """
    
    # Configuration
    dbt.config(
        materialized="table",
        tags=["silver", "run", "python", "ml"],
        packages=["scikit-learn", "pandas", "numpy"]
    )
    
    # Get customer data
    customer_df = dbt.ref("customer_segments").to_pandas()
    
    # Prepare features for clustering (using available columns from customer_segments - uppercase)
    features = ['ACCOUNT_BALANCE', 'BALANCE_PERCENTILE', 'BALANCE_RANK_IN_NATION']
    X = customer_df[features].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add cluster information to dataframe
    customer_df['ML_CLUSTER'] = clusters
    customer_df['CLUSTER_NAME'] = customer_df['ML_CLUSTER'].map({
        0: 'High Value Stable',
        1: 'Premium Elite', 
        2: 'Growth Potential',
        3: 'Standard Base',
        4: 'At Risk'
    })
    
    # Calculate cluster statistics
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    # Add cluster center distances
    distances = []
    for i, row in enumerate(X_scaled):
        cluster_id = clusters[i]
        center = kmeans.cluster_centers_[cluster_id]
        distance = np.linalg.norm(row - center)
        distances.append(distance)
    
    customer_df['DISTANCE_TO_CLUSTER_CENTER'] = distances
    
    # Add derived ML features
    customer_df['IS_CLUSTER_OUTLIER'] = customer_df['DISTANCE_TO_CLUSTER_CENTER'] > customer_df['DISTANCE_TO_CLUSTER_CENTER'].quantile(0.95)
    customer_df['ML_CONFIDENCE_SCORE'] = 1 - (customer_df['DISTANCE_TO_CLUSTER_CENTER'] / customer_df['DISTANCE_TO_CLUSTER_CENTER'].max())
    
    # Add metadata
    customer_df['ML_MODEL_VERSION'] = '1.0'
    customer_df['CLUSTERING_ALGORITHM'] = 'KMeans'
    customer_df['N_CLUSTERS_USED'] = n_clusters
    customer_df['FEATURES_USED'] = str(features)
    
    return customer_df
