# Streamlit Connection Configuration

Guide to configuring and overriding Snowflake connections for Streamlit apps.

---

## Configuration File Location

`~/.snowflake/connections.toml` - Standard Snowflake CLI configuration

```toml
[default]
warehouse = "COMPUTE_WH"
database = "YOUR_DB"
schema = "YOUR_SCHEMA"
role = "your_role"
account = "your_account"
user = "your_username"
authenticator = "externalbrowser"
```

---

## Environment Variable Overrides

Override connection settings without modifying `connections.toml`:

### Command-Line Overrides

```bash
# Override database/schema
export SNOWFLAKE_DATABASE=ANALYTICS_DB
export SNOWFLAKE_SCHEMA=REPORTING
streamlit run app.py

# Override warehouse
export SNOWFLAKE_WAREHOUSE=LARGE_WH
streamlit run app.py

# Multiple overrides
export SNOWFLAKE_DATABASE=PROD_DB
export SNOWFLAKE_SCHEMA=PUBLIC
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
streamlit run app.py
```

### Supported Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `SNOWFLAKE_ACCOUNT` | Override account | `xy12345.us-east-1` |
| `SNOWFLAKE_USER` | Override user | `john_doe` |
| `SNOWFLAKE_PASSWORD` | Override password | `secret123` |
| `SNOWFLAKE_DATABASE` | Override database | `ANALYTICS_DB` |
| `SNOWFLAKE_SCHEMA` | Override schema | `REPORTING` |
| `SNOWFLAKE_WAREHOUSE` | Override warehouse | `LARGE_WH` |
| `SNOWFLAKE_ROLE` | Override role | `ANALYST` |

---

## Startup Script Pattern

**Recommended:** Use startup script for consistent environment:

```bash
#!/bin/bash
# run_local.sh

# Set environment-specific variables
export SNOWFLAKE_DATABASE=DEV_DB
export SNOWFLAKE_SCHEMA=PUBLIC
export SNOWFLAKE_WAREHOUSE=DEV_WH

# Start Streamlit
streamlit run app.py
```

**Usage:**
```bash
chmod +x run_local.sh
./run_local.sh
```

---

## Multi-Environment Setup

### Approach 1: Multiple Connection Profiles

```toml
# ~/.snowflake/connections.toml

[dev]
account = "dev_account"
database = "DEV_DB"
schema = "DEV_SCHEMA"
warehouse = "DEV_WH"
authenticator = "externalbrowser"

[staging]
account = "staging_account"
database = "STAGING_DB"
schema = "STAGING_SCHEMA"
warehouse = "STAGING_WH"
authenticator = "externalbrowser"

[prod]
account = "prod_account"
database = "PROD_DB"
schema = "PROD_SCHEMA"
warehouse = "PROD_WH"
authenticator = "snowflake_jwt"
private_key_path = "~/.ssh/prod_key.p8"
```

**Select at runtime:**
```python
import streamlit as st
from snowflake.snowpark import Session

env = st.selectbox("Environment", ["dev", "staging", "prod"])
session = Session.builder.config("connection_name", env).create()
```

### Approach 2: Environment Scripts

```bash
# dev.sh
export SNOWFLAKE_DATABASE=DEV_DB
export SNOWFLAKE_SCHEMA=DEV_SCHEMA
streamlit run app.py

# staging.sh
export SNOWFLAKE_DATABASE=STAGING_DB
export SNOWFLAKE_SCHEMA=STAGING_SCHEMA
streamlit run app.py

# prod.sh (typically deployed to Snowflake, not local)
export SNOWFLAKE_DATABASE=PROD_DB
export SNOWFLAKE_SCHEMA=PROD_SCHEMA
streamlit run app.py
```

---

## Programmatic Configuration

### Using Streamlit Secrets

For deployed apps in Snowflake:

```python
# .streamlit/secrets.toml (gitignored)
[snowflake]
account = "your_account"
user = "your_user"
password = "your_password"
warehouse = "COMPUTE_WH"
database = "YOUR_DB"
schema = "YOUR_SCHEMA"
```

```python
# app.py
import streamlit as st
from snowflake.snowpark import Session

def get_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()  # When deployed to Snowflake
    except:
        # Local development
        return Session.builder.configs(st.secrets["snowflake"]).create()

session = get_session()
```

### Dynamic Configuration

```python
import streamlit as st
from snowflake.snowpark import Session
import os

def get_session_with_overrides():
    """Create session with environment variable overrides"""
    config = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT", "default_account"),
        "user": os.getenv("SNOWFLAKE_USER", "default_user"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "DEFAULT_DB"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
        "role": os.getenv("SNOWFLAKE_ROLE", "PUBLIC"),
    }
    
    # Use externalbrowser if no password provided
    if not config["password"]:
        config["authenticator"] = "externalbrowser"
    
    return Session.builder.configs(config).create()
```

---

## Best Practices

### ✅ DO

- Use environment variables for local development overrides
- Use connection profiles for multi-environment setups
- Use startup scripts for consistent configuration
- Keep `connections.toml` in `.gitignore`
- Use `st.secrets` for deployed apps
- Test connections with `snow sql -c profile_name`

### ❌ DON'T

- Hardcode credentials in code
- Commit `connections.toml` or `.streamlit/secrets.toml`
- Use production credentials for local development
- Share connection files between developers

---

## Testing Connection

```bash
# Test connection profile
snow sql -c default -q "SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()"

# Test with overrides
export SNOWFLAKE_DATABASE=TEST_DB
snow sql -c default -q "SELECT CURRENT_DATABASE()"

# Verify environment variables
env | grep SNOWFLAKE_
```

---

## Troubleshooting

### Wrong Database/Schema

**Problem:** App uses unexpected database/schema

**Solution:**
```python
# Add debug info to your app
st.write("Database:", session.get_current_database())
st.write("Schema:", session.get_current_schema())
st.write("Warehouse:", session.get_current_warehouse())
```

### Environment Variables Not Applied

**Problem:** Overrides don't take effect

**Solutions:**
1. Verify variables are exported: `env | grep SNOWFLAKE_`
2. Restart Streamlit after setting variables
3. Check if app caches session (clear with `st.cache_data.clear()`)

### Connection Profile Not Found

**Error:** `Connection 'profile_name' not found`

**Solutions:**
1. Check `~/.snowflake/connections.toml` exists
2. Verify profile name is correct (case-sensitive)
3. Test with: `snow connection test -c profile_name`

---

## Quick Reference

```bash
# Basic override
export SNOWFLAKE_DATABASE=MY_DB
export SNOWFLAKE_SCHEMA=MY_SCHEMA
streamlit run app.py

# Multiple profiles in connections.toml
[dev]
database = "DEV_DB"

[prod]
database = "PROD_DB"

# Select profile
snow sql -c dev -q "SELECT CURRENT_DATABASE()"

# Test connection
snow connection test -c default
```

---

**Related Documentation:**
- `AUTHENTICATION.md` - Authentication methods
- `BEST_PRACTICES.md` - Streamlit development patterns


