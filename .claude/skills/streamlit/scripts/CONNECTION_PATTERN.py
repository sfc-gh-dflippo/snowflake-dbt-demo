"""
Streamlit Snowpark Connection Pattern

This pattern supports both local development and Snowflake deployment
by automatically detecting the environment and returning the appropriate session.
"""

import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session


@st.cache_resource
def get_snowpark_session():
    """
    Get Snowpark session.
    
    In Snowflake: Uses get_active_session() for managed session
    Locally: Connects via connections.toml using default connection
    
    Returns:
        snowflake.snowpark.Session - Active Snowpark session
    """
    try:
        # Running in Snowflake - get managed session
        return get_active_session()
    except:
        # Running locally - use connections.toml
        return Session.builder.config('connection_name', 'default').create()


# Usage in your Streamlit app
def main():
    st.title("My Snowflake Streamlit App")
    
    # Get session
    session = get_snowpark_session()
    
    # Use session for queries
    df = session.sql("SELECT * FROM my_table LIMIT 10").to_pandas()
    st.dataframe(df)


if __name__ == "__main__":
    main()
