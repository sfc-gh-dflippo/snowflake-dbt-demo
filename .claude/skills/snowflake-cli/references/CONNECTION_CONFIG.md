# Snowflake CLI Connection Configuration

## connections.toml Location

- **Unix/Mac:** `~/.snowflake/connections.toml`
- **Windows:** `%USERPROFILE%\.snowflake\connections.toml`

## Basic Configuration

```toml
[default]
account = "your_account"
user = "your_username"
password = "your_password"
warehouse = "COMPUTE_WH"
database = "MY_DB"
schema = "PUBLIC"
role = "MY_ROLE"
```

## Authentication Methods

### 1. Username/Password
```toml
[default]
account = "your_account"
user = "your_username"
password = "your_password"
```

### 2. Key Pair Authentication
```toml
[default]
account = "your_account"
user = "your_username"
authenticator = "snowflake_jwt"
private_key_path = "~/.ssh/snowflake_key.p8"
private_key_passphrase = "your_passphrase"  # Optional
```

### 3. SSO (External Browser)
```toml
[default]
account = "your_account"
authenticator = "externalbrowser"
```

### 4. OAuth
```toml
[default]
account = "your_account"
authenticator = "oauth"
token = "your_oauth_token"
```

## Multiple Connections

Define different connections for different environments:

```toml
[default]
account = "dev_account"
user = "dev_user"
warehouse = "DEV_WH"

[prod]
account = "prod_account"
user = "prod_user"
warehouse = "PROD_WH"
```

Use with `-c` flag:
```bash
snow sql -c dev -q "SELECT * FROM table"
snow sql -c prod -q "SELECT * FROM table"
```

## Environment-Specific Overrides

Use command-line flags to override configuration:

```bash
# Override warehouse
snow sql --warehouse ANALYSIS_WH -q "SELECT ..."

# Override database
snow sql --database ANALYTICS -q "SELECT ..."

# Override role
snow sql --role ANALYST -q "SELECT ..."
```
