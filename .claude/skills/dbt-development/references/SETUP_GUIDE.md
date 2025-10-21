# dbt Installation & Setup Guide for Snowflake

## Overview

This guide covers common setup challenges and Snowflake-specific configuration for dbt Core.

**Official dbt Documentation**: [Install dbt](https://docs.getdbt.com/docs/core/installation-overview)

---

## Installation

### Recommended: pip

```bash
# Install dbt with Snowflake adapter
pip install -U dbt-core dbt-snowflake

# Verify installation
dbt --version
```

### Alternative: conda

```bash
# Create isolated environment
conda create -n dbt python=3.11
conda activate dbt
pip install -U dbt-core dbt-snowflake
```

**Official dbt Docs**: [Core Installation](https://docs.getdbt.com/docs/core/installation-overview)

---

## Snowflake Configuration

### Configure profiles.yml

Location: `~/.dbt/profiles.yml`

```yaml
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: snowflake
      token: "{{ env_var('DBT_ENV_SECRET_SNOWFLAKE_PAT') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: dbt_dev
      threads: 4
    
    prod:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: snowflake
      token: "{{ env_var('DBT_ENV_SECRET_SNOWFLAKE_PAT') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: analytics
      threads: 8
```

---

## Authentication Methods

### Programmatic Access Token (PAT) - Recommended

**Best for**: Production environments, CI/CD pipelines, service accounts

Programmatic Access Tokens (PATs) are the recommended authentication method. They can be scoped to specific roles, have configurable expiration times, and can be easily rotated without changing passwords or key pairs.

**Generate a PAT in Snowflake**:
```sql
-- Generate a token for yourself with 30-day expiration, restricted to TRANSFORMER role
ALTER USER ADD PAT dbt_prod_token
ROLE_RESTRICTION = TRANSFORMER
DAYS_TO_EXPIRY = 30
COMMENT = 'dbt production deployment';
```

**Rotate a PAT in Snowflake**:
```sql
-- Rotate a token for yourself and set the previous PAT to expire after 24 hours
ALTER USER ROTATE PAT dbt_prod_token
EXPIRE_ROTATED_TOKEN_AFTER_HOURS = 24;
```

**Configure in profiles.yml**:
```yaml
your_project:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: snowflake
      password: "{{ env_var('DBT_ENV_SECRET_SNOWFLAKE_PAT') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: analytics
      threads: 8
```

**Best Practices**:
- Use `DBT_ENV_SECRET_` prefix for PAT environment variables (scrubs from logs and obfuscates in UI)
- Store PAT secrets securely (use secrets manager)
- Set appropriate expiration times (30-90 days)
- Restrict tokens to specific roles
- Rotate tokens regularly
- Revoke tokens when no longer needed

**Official Documentation**: 
- [Snowflake Programmatic Access Tokens](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens)
- [dbt Environment Variables](https://docs.getdbt.com/docs/build/environment-variables#handling-secrets)

---

### SSO Authentication

**Best for**: Local interactive developer sessions

```yaml
      authenticator: externalbrowser
```

---

### Key Pair Authentication

**Best for**: Environments where PAT is not available

```yaml
      authenticator: snowflake_jwt
      private_key_path: /path/to/private_key.p8
      private_key_passphrase: "{{ env_var('DBT_ENV_SECRET_PRIVATE_KEY_PASSPHRASE') }}"
```

**Official Snowflake Docs**: [Key Pair Authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth)

---

### Password Authentication

**Not Recommended**: Use PAT, SSO, or Key Pair authentication instead.

---

## Package Installation

### Create packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  
  - package: brooklyn-data/dbt_artifacts
    version: [">=2.0.0", "<3.0.0"]
```

### Install Packages

```bash
dbt deps
```

**Official dbt Docs**: [Package Management](https://docs.getdbt.com/docs/build/packages)

---

## Verify Installation

### Test Connection

```bash
dbt debug
```

**Expected output**:
```
Connection:
  account: xy12345.us-east-1
  user: dbt_user
  database: ANALYTICS
  warehouse: TRANSFORMING
  Connection test: OK connection ok
```

### Common Connection Issues

**Issue**: `dbt: command not found`

**Solution**:
```bash
# Ensure pip install location is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

**Issue**: Snowflake connection failures

**Solution**:
```bash
# Check environment variables
echo $DBT_ENV_SECRET_SNOWFLAKE_PAT

# Verify profiles.yml location
ls ~/.dbt/profiles.yml

# Test Snowflake connection directly with PAT
snowsql -a xy12345.us-east-1 -u dbt_user --authenticator snowflake --token $DBT_ENV_SECRET_SNOWFLAKE_PAT

# Verify PAT is active in Snowflake
# Run in Snowflake:
# SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER dbt_user;
```

---

**Issue**: SSL/Certificate errors with Snowflake

**Solution**:
```bash
# Install system certificate support
pip install pip-system-certs

# For corporate firewalls
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org dbt-core dbt-snowflake
```

**Official Snowflake Docs**: [Network Issues](https://docs.snowflake.com/en/user-guide/troubleshooting-network)

---

**Issue**: Package installation fails

**Solution**:
```bash
# Clear package cache
rm -rf dbt_packages/
dbt deps

# Force reinstall
dbt deps --upgrade
```

---

## Project Initialization

### Initialize New Project

```bash
# Interactive setup
dbt init

# Manual setup
mkdir my_dbt_project
cd my_dbt_project
```

### Project Structure

```
my_dbt_project/
├── dbt_project.yml
├── profiles.yml (in ~/.dbt/)
├── models/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── tests/
├── macros/
└── packages.yml
```

---

## dbt_project.yml Configuration

```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

profile: 'my_project'

model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]

models:
  my_dbt_project:
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

---

## Development Workflow

### 1. Start Development

```bash
# Switch to dev target
dbt run --target dev
```

### 2. Build Models

```bash
# Develop iteratively
dbt run --select model_name
dbt test --select model_name
```

### 3. Deploy to Production

```bash
dbt run --target prod
dbt test --target prod
```

---

## Best Practices

### 1. Use Virtual Environments

```bash
# Create virtual environment
python -m venv dbt_venv
source dbt_venv/bin/activate

# Install dbt
pip install dbt-core dbt-snowflake
```

### 2. Separate Dev/Prod

```yaml
# Use schema prefixes in dev
dev:
  schema: "{{ env_var('DBT_USER') }}_dev"

prod:
  schema: "analytics"
```

### 3. Version Control

```gitignore
# .gitignore
target/
dbt_packages/
logs/
.env
```

---

## Upgrade dbt Version

```bash
# Check current version
dbt --version

# Upgrade to latest
pip install --upgrade dbt-core dbt-snowflake

# Or specific version (compatible with dbt Projects on Snowflake)
pip install dbt-core==1.9.4 dbt-snowflake==1.9.2
```

**Official dbt Docs**: [Version Migration Guides](https://docs.getdbt.com/docs/dbt-versions/core-upgrade)

---

## Related Documentation

- [Official dbt Docs: Installation](https://docs.getdbt.com/docs/core/installation-overview)
- [Official dbt Docs: profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)
- [Official Snowflake Docs: dbt](https://docs.snowflake.com/en/user-guide/data-engineering/dbt)
- `QUICK_REFERENCE.md` - Essential commands
- `PROJECT_STRUCTURE.md` - Project organization
