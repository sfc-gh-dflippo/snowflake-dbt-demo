---
name: dbt Setup
description: Expert guidance for installing dbt, configuring Snowflake connections, setting up authentication (PAT, SSO, key pair), managing packages, and troubleshooting installation issues. Use this skill when setting up new dbt projects, configuring profiles.yml, managing authentication, or resolving connection and installation problems.
---

# dbt Installation & Setup

## Purpose

Transform AI agents into experts on dbt installation and Snowflake configuration, providing guidance on setting up dbt projects, configuring authentication, managing packages, and troubleshooting common setup issues.

## When to Use This Skill

Activate this skill when users ask about:
- Installing dbt-core and dbt-snowflake
- Configuring profiles.yml for Snowflake
- Setting up authentication (PAT, SSO, key pair, password)
- Installing and managing dbt packages
- Troubleshooting connection issues
- Initializing new dbt projects
- Verifying installation and configuration
- Upgrading dbt versions

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

**Expected output:**
```
installed version: 1.9.4
   latest version: 1.9.4

Up to date!

Plugins:
  - snowflake: 1.9.2
```

---

### Alternative: conda

```bash
# Create isolated environment
conda create -n dbt python=3.11
conda activate dbt

# Install dbt
pip install -U dbt-core dbt-snowflake

# Verify
dbt --version
```

**Benefits of conda:**
- Isolated Python environment
- Avoids conflicts with other tools
- Easy to recreate/reset

**Official dbt Docs**: [Core Installation](https://docs.getdbt.com/docs/core/installation-overview)

---

## Snowflake Configuration

### Configure profiles.yml

**Location**: `~/.dbt/profiles.yml`

**Basic configuration:**
```yaml
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: snowflake
      password: "{{ env_var('DBT_ENV_SECRET_SNOWFLAKE_PAT') }}"
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
      password: "{{ env_var('DBT_ENV_SECRET_SNOWFLAKE_PAT') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: analytics
      threads: 8
```

**Key fields:**
- `account`: Snowflake account identifier (e.g., xy12345.us-east-1)
- `user`: Snowflake username
- `role`: Snowflake role with appropriate permissions
- `database`: Target database
- `warehouse`: Compute warehouse for dbt operations
- `schema`: Target schema (use dev-specific naming)
- `threads`: Parallel execution threads

**Official dbt Docs**: [profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)

---

## Authentication Methods

### 1. Programmatic Access Token (PAT) - RECOMMENDED

**Best for**: Production environments, CI/CD pipelines, service accounts

Programmatic Access Tokens (PATs) are the recommended authentication method. They can be scoped to specific roles, have configurable expiration times, and can be easily rotated without changing passwords or key pairs.

**Generate a PAT in Snowflake:**
```sql
-- Generate a token with 30-day expiration, restricted to TRANSFORMER role
ALTER USER dbt_user ADD PAT dbt_prod_token
ROLE_RESTRICTION = TRANSFORMER
DAYS_TO_EXPIRY = 30
COMMENT = 'dbt production deployment';
```

**Rotate a PAT in Snowflake:**
```sql
-- Rotate and expire old token after 24 hours
ALTER USER dbt_user ROTATE PAT dbt_prod_token
EXPIRE_ROTATED_TOKEN_AFTER_HOURS = 24;
```

**List active PATs:**
```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER dbt_user;
```

**Configure in profiles.yml:**
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

**Set environment variable:**
```bash
# In .env file or shell
export DBT_ENV_SECRET_SNOWFLAKE_PAT="your-pat-token-here"
```

**Best Practices**:
- Use `DBT_ENV_SECRET_` prefix for PAT environment variables (scrubs from logs and obfuscates in UI)
- Store PAT secrets securely (use secrets manager in production)
- Set appropriate expiration times (30-90 days)
- Restrict tokens to specific roles
- Rotate tokens regularly
- Revoke tokens when no longer needed

**Official Snowflake Documentation**: [Programmatic Access Tokens](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens)

**Official dbt Documentation**: [Environment Variables](https://docs.getdbt.com/docs/build/environment-variables#handling-secrets)

---

### 2. SSO Authentication (Externalbrowser)

**Best for**: Local interactive developer sessions

```yaml
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: externalbrowser  # Opens browser for SSO
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: dbt_dev
      threads: 4
```

**How it works**: 
- Opens browser window for authentication
- Uses organization's SSO (Okta, Azure AD, etc.)
- No password stored in files
- Great for development

---

### 3. Key Pair Authentication

**Best for**: Environments where PAT is not available, automated processes

**Generate key pair:**
```bash
# Generate private key
openssl genrsa -out snowflake_key.pem 2048

# Generate public key
openssl rsa -in snowflake_key.pem -pubout -out snowflake_key.pub

# (Optional) Encrypt private key with passphrase
openssl genrsa -aes256 -out snowflake_key_encrypted.pem 2048
```

**Assign public key to Snowflake user:**
```sql
-- Copy public key content (remove header/footer)
ALTER USER dbt_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqhki...';
```

**Configure in profiles.yml:**
```yaml
your_project:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      authenticator: snowflake_jwt
      private_key_path: /path/to/snowflake_key.pem
      private_key_passphrase: "{{ env_var('DBT_ENV_SECRET_PRIVATE_KEY_PASSPHRASE') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: analytics
      threads: 8
```

**Official Snowflake Docs**: [Key Pair Authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth)

---

### 4. Password Authentication

**Not Recommended**: Use PAT, SSO, or Key Pair authentication instead.

```yaml
# Only use for testing/temporary access
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      # ... other settings
```

**Security concerns:**
- Password stored in environment/file
- No automatic rotation
- No scope restrictions
- Less secure than alternatives

---

## Package Installation

### Create packages.yml

**Location**: Project root

```yaml
# packages.yml
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
# Install all packages
dbt deps

# Packages installed to dbt_packages/ directory
```

**Package updates:**
```bash
# Remove old packages
rm -rf dbt_packages/

# Reinstall
dbt deps

# Force upgrade to latest compatible versions
dbt deps --upgrade
```

**Official dbt Docs**: [Package Management](https://docs.getdbt.com/docs/build/packages)

---

## Verify Installation

### Test Connection

```bash
dbt debug
```

**Expected successful output:**
```
Configuration:
  profiles.yml file [OK found and valid]
  dbt_project.yml file [OK found and valid]

Connection:
  account: xy12345.us-east-1
  user: dbt_user
  database: ANALYTICS
  warehouse: TRANSFORMING
  role: TRANSFORMER
  schema: dbt_dev
  authenticator: snowflake
  Connection test: [OK connection ok]

All checks passed!
```

---

## Common Connection Issues

### Issue: `dbt: command not found`

**Solution:**
```bash
# Ensure pip install location is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or for zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify dbt is in PATH
which dbt
dbt --version
```

---

### Issue: Snowflake connection failures

**Solutions:**

**1. Check environment variables:**
```bash
echo $DBT_ENV_SECRET_SNOWFLAKE_PAT
echo $SNOWFLAKE_ACCOUNT

# Verify PAT is set
if [ -z "$DBT_ENV_SECRET_SNOWFLAKE_PAT" ]; then
    echo "PAT not set!"
else
    echo "PAT is configured"
fi
```

**2. Verify profiles.yml location:**
```bash
ls ~/.dbt/profiles.yml

# Check contents
cat ~/.dbt/profiles.yml
```

**3. Test Snowflake connection directly:**
```bash
# Using snowsql with PAT
snowsql -a xy12345.us-east-1 -u dbt_user --authenticator snowflake --token $DBT_ENV_SECRET_SNOWFLAKE_PAT
```

**4. Verify PAT is active in Snowflake:**
```sql
-- Run in Snowflake
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER dbt_user;
```

---

### Issue: SSL/Certificate errors

**Solution:**
```bash
# Install system certificate support
pip install pip-system-certs

# For corporate firewalls
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org dbt-core dbt-snowflake
```

**Official Snowflake Docs**: [Network Issues](https://docs.snowflake.com/en/user-guide/troubleshooting-network)

---

### Issue: Package installation fails

**Solutions:**

```bash
# Clear package cache
rm -rf dbt_packages/
dbt clean
dbt deps

# Force reinstall
dbt deps --upgrade

# Check packages.yml syntax
cat packages.yml
```

---

### Issue: Python version incompatibility

**Solution:**
```bash
# Check Python version
python --version

# dbt requires Python 3.8+
# Upgrade Python if needed, or use conda

conda create -n dbt python=3.11
conda activate dbt
pip install dbt-core dbt-snowflake
```

---

## Project Initialization

### Initialize New Project

**Interactive setup:**
```bash
dbt init

# Follow prompts:
# - Enter project name
# - Select database (snowflake)
# - Configure connection details
```

**Manual setup:**
```bash
# Create project directory
mkdir my_dbt_project
cd my_dbt_project

# Create basic structure
mkdir models tests macros
touch dbt_project.yml
```

---

### Project Structure

```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # (in ~/.dbt/ not project root)
├── packages.yml             # Package dependencies
├── models/
│   ├── bronze/             # Staging layer
│   ├── silver/             # Intermediate layer
│   └── gold/               # Marts layer
├── tests/
│   ├── generic/            # Reusable test definitions
│   └── singular/           # One-off tests
├── macros/                 # Custom Jinja macros
├── seeds/                  # CSV data files
└── snapshots/              # SCD Type 2 tracking
```

---

## dbt_project.yml Configuration

**Minimal configuration:**
```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

profile: 'my_project'  # Must match profiles.yml

model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]
seed-paths: ["seeds"]
snapshot-paths: ["snapshots"]

models:
  my_dbt_project:
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
      +schema: bronze
    
    silver:
      +materialized: ephemeral
      +tags: ["silver"]
      +schema: silver
    
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
      +schema: gold
```

---

## Development Workflow

### 1. Initial Setup

```bash
# Install packages
dbt deps

# Verify connection
dbt debug

# Load seed data (if any)
dbt seed
```

---

### 2. Development Cycle

```bash
# Build specific model
dbt build --select model_name

# Build with dependencies
dbt build --select +model_name+

# Build entire project
dbt build
```

---

### 3. Deploy to Production

```bash
# Build against production target
dbt build --target prod

# Test production
dbt test --target prod

# Generate documentation
dbt docs generate --target prod
```

---

## Best Practices

### 1. Use Virtual Environments

**Avoid package conflicts:**
```bash
# Create virtual environment
python -m venv dbt_venv
source dbt_venv/bin/activate  # Linux/Mac
dbt_venv\Scripts\activate     # Windows

# Install dbt
pip install dbt-core dbt-snowflake
```

---

### 2. Separate Dev/Prod Configurations

**Use schema prefixes in dev:**
```yaml
dev:
  schema: "{{ env_var('DBT_USER', 'default') }}_dev"  # user_dev

prod:
  schema: "analytics"  # Shared production schema
```

---

### 3. Version Control

**Add to .gitignore:**
```gitignore
# .gitignore
target/
dbt_packages/
logs/
.env
*.log
```

**Commit to git:**
```gitignore
# DO commit:
dbt_project.yml
packages.yml
models/
tests/
macros/
README.md

# DON'T commit:
profiles.yml (contains credentials)
.env (contains secrets)
target/ (compiled SQL)
dbt_packages/ (installed packages)
logs/ (run logs)
```

---

## Upgrade dbt Version

```bash
# Check current version
dbt --version

# Upgrade to latest
pip install --upgrade dbt-core dbt-snowflake

# Or specific version (for dbt Projects on Snowflake compatibility)
pip install dbt-core==1.9.4 dbt-snowflake==1.9.2

# Verify upgrade
dbt --version
```

**Version considerations:**
- Check [dbt Migration Guides](https://docs.getdbt.com/docs/dbt-versions/core-upgrade) for breaking changes
- Test in dev environment first
- For dbt Projects on Snowflake: Use compatible versions (1.9.4 / 1.9.2)

**Official dbt Docs**: [Version Migration Guides](https://docs.getdbt.com/docs/dbt-versions/core-upgrade)

---

## Helping Users with Setup

### Strategy for Assisting Users

When users have setup issues:

1. **Identify the stage**: Installation? Configuration? Connection?
2. **Check basics first**: Python version, pip, PATH
3. **Verify credentials**: Environment variables, profiles.yml
4. **Test connection**: `dbt debug` output
5. **Provide specific solutions**: Commands and configuration examples
6. **Reference official docs**: Link to relevant Snowflake/dbt documentation

### Common User Questions

**"How do I install dbt?"**
```bash
pip install -U dbt-core dbt-snowflake
dbt --version
```

**"How do I set up authentication?"**
- Recommend PAT for production
- SSO for local development
- Provide configuration examples
- Show how to set environment variables

**"Where do I put my credentials?"**
- `~/.dbt/profiles.yml` for connection config
- `.env` file or environment variables for secrets
- Never commit credentials to git

**"My connection isn't working"**
```bash
# Debug checklist
dbt debug
echo $DBT_ENV_SECRET_SNOWFLAKE_PAT
cat ~/.dbt/profiles.yml
# Test Snowflake connection directly
```

---

## Related Official Documentation

- [dbt Docs: Installation](https://docs.getdbt.com/docs/core/installation-overview)
- [dbt Docs: profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)
- [dbt Docs: Environment Variables](https://docs.getdbt.com/docs/build/environment-variables)
- [Snowflake Docs: dbt](https://docs.snowflake.com/en/user-guide/data-engineering/dbt)
- [Snowflake Docs: PAT](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens)

---

**Goal**: Transform AI agents into expert dbt setup specialists who guide users through installation, configuration, authentication, and troubleshooting with clear, actionable instructions and best practices.

