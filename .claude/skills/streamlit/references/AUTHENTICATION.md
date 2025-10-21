# Streamlit Authentication Methods

Complete guide to authenticating Streamlit apps with Snowflake.

**Reference:** [Snowflake CLI Connection Configuration](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/specify-credentials)

---

## Connection Configuration File

All authentication methods use `~/.snowflake/connections.toml`:

```toml
[default]
warehouse = "COMPUTE_WH"
database = "YOUR_DB"
schema = "YOUR_SCHEMA"
role = "your_role"
account = "your_account"
user = "your_username"

# Choose ONE authentication method below
```

---

## Authentication Methods

### Option 1: Username/Password

**Simplest method** - Use for development/testing

```toml
[default]
account = "your_account"
user = "your_username"
password = "your_password"
```

**Pros:**
- ✅ Simple setup
- ✅ Works everywhere

**Cons:**
- ❌ Less secure (password in plain text)
- ❌ Not recommended for production

---

### Option 2: SSO/External Browser (Recommended)

**Best for organizations with SSO** - Opens browser for authentication

```toml
[default]
account = "your_account"
user = "your_username"
authenticator = "externalbrowser"
```

**Pros:**
- ✅ Most secure
- ✅ Leverages existing SSO
- ✅ No password storage

**Cons:**
- ❌ Requires browser access
- ❌ Not suitable for headless environments

**Usage:**
```bash
streamlit run app.py  # Browser opens automatically for authentication
```

---

### Option 3: Key Pair Authentication

**Best for automated/production workloads** - Uses RSA key pair

```toml
[default]
account = "your_account"
user = "your_username"
authenticator = "snowflake_jwt"
private_key_path = "~/.ssh/snowflake_key.p8"
private_key_passphrase = "your_passphrase"  # Optional if key is encrypted
```

**Setup:**

1. **Generate Key Pair:**
```bash
# Generate private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out snowflake_key.p8 -nocrypt

# Generate public key
openssl rsa -in snowflake_key.p8 -pubout -out snowflake_key.pub
```

2. **Add Public Key to Snowflake:**
```sql
-- Remove header/footer and newlines from public key
ALTER USER your_username SET RSA_PUBLIC_KEY='MIIBIjANBg...';
```

3. **Verify:**
```sql
DESC USER your_username;
-- Check RSA_PUBLIC_KEY_FP field
```

**Pros:**
- ✅ Very secure
- ✅ No password storage
- ✅ Ideal for CI/CD and automation
- ✅ Works in headless environments

**Cons:**
- ❌ More complex setup
- ❌ Requires key management

---

### Option 4: OAuth Token

**For OAuth-based integrations** - Uses pre-obtained token

```toml
[default]
account = "your_account"
authenticator = "oauth"
token = "your_oauth_token"
```

**Pros:**
- ✅ Supports OAuth workflows
- ✅ Token-based security

**Cons:**
- ❌ Requires token refresh logic
- ❌ Token expiration management

---

## Multiple Connections

Define multiple connection profiles for different environments:

```toml
[default]
account = "dev_account"
user = "dev_user"
authenticator = "externalbrowser"
warehouse = "DEV_WH"
database = "DEV_DB"

[production]
account = "prod_account"
user = "prod_user"
authenticator = "snowflake_jwt"
private_key_path = "~/.ssh/prod_key.p8"
warehouse = "PROD_WH"
database = "PROD_DB"

[staging]
account = "staging_account"
user = "staging_user"
authenticator = "externalbrowser"
warehouse = "STAGING_WH"
database = "STAGING_DB"
```

**Usage:**
```python
# In your Streamlit app
import streamlit as st
from snowflake.snowpark import Session

# Use specific connection
connection_name = st.selectbox("Environment", ["default", "staging", "production"])
session = Session.builder.config("connection_name", connection_name).create()
```

---

## Streamlit Connection Pattern

**Required pattern** for all Streamlit apps:

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

def get_snowpark_session():
    """Get or create Snowpark session"""
    try:
        # Try to get active session (when running in Snowflake)
        return get_active_session()
    except:
        # Fall back to connections.toml (when running locally)
        from snowflake.snowpark import Session
        return Session.builder.configs(st.secrets.get("snowflake", {})).create()
```

---

## Environment Variable Overrides

Override connection settings without modifying `connections.toml`:

```bash
# Override specific settings
export SNOWFLAKE_DATABASE=ANALYTICS_DB
export SNOWFLAKE_SCHEMA=PUBLIC
export SNOWFLAKE_WAREHOUSE=LARGE_WH

streamlit run app.py
```

**Supported variables:**
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_ROLE`

---

## Best Practices

### ✅ DO

- Use **SSO/externalbrowser** for development
- Use **key pair** for production and CI/CD
- Store keys outside project directory
- Use environment-specific connection profiles
- Rotate keys regularly
- Use `.gitignore` to exclude connection files
- Test authentication locally before deployment

### ❌ DON'T

- Commit `connections.toml` to git
- Store passwords in code
- Share private keys
- Use same credentials for dev/prod
- Hardcode authentication details

---

## Troubleshooting

### Connection Failed

**Error:** `Could not connect to Snowflake`

**Solutions:**
1. Verify `connections.toml` path: `~/.snowflake/connections.toml`
2. Check account/user/role are correct
3. Test with `snow sql -c default -q "SELECT CURRENT_USER()"`

### SSO Not Opening Browser

**Error:** `External browser authentication failed`

**Solutions:**
1. Ensure browser is installed
2. Check firewall/proxy settings
3. Try `authenticator = "username_password_mfa"` instead

### Key Pair Authentication Failed

**Error:** `JWT token is invalid`

**Solutions:**
1. Verify public key is set: `DESC USER your_username`
2. Check private key path is correct
3. Ensure private key format is PKCS#8
4. Verify passphrase if key is encrypted

---

## Quick Reference

```toml
# SSO (Recommended for development)
[default]
authenticator = "externalbrowser"

# Key Pair (Recommended for production)
[production]
authenticator = "snowflake_jwt"
private_key_path = "~/.ssh/snowflake_key.p8"

# Username/Password (Development only)
[dev]
password = "your_password"

# OAuth
[oauth]
authenticator = "oauth"
token = "your_token"
```

---

**Related Documentation:**
- `CONNECTION_CONFIG.md` - Connection configuration and overrides
- `BEST_PRACTICES.md` - Streamlit development patterns


