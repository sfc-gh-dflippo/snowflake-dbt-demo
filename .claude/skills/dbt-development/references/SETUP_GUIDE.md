# dbt Installation & Setup Guide for Snowflake

## Overview

This guide covers installing and setting up dbt Core for Snowflake. For platform-specific deployment like dbt Projects on Snowflake, see the `dbt-projects-snowflake` skill.

## Installation Methods

### 1. Using pip (Recommended for Most Users)

```bash
# Install dbt with Snowflake adapter
pip install dbt-core dbt-snowflake
```

### 2. Using conda/mamba (Recommended for Data Scientists)

```bash
# Create isolated environment
conda create -n dbt python=3.11
conda activate dbt

# Install dbt
conda install -c conda-forge dbt-core dbt-snowflake
```

### 3. Using pipx (Isolated Installation)

```bash
# Install pipx if needed
pip install pipx

# Install dbt in isolated environment
pipx install dbt-core dbt-snowflake
```

### 4. Using Docker

```bash
# Pull dbt Snowflake image
docker pull ghcr.io/dbt-labs/dbt-snowflake:latest

# Run dbt commands
docker run -v $(pwd):/usr/app ghcr.io/dbt-labs/dbt-snowflake:latest dbt run
```

## Snowflake Configuration

### Configure profiles.yml
snowflake_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: dbt_dev
      threads: 4
```

### Authentication Methods

**Password Authentication (shown above)**
```yaml
password: "{{ env_var('DBT_PASSWORD') }}"
```

**Key Pair Authentication (Recommended for Production)**
```yaml
authenticator: snowflake_jwt
private_key_path: /path/to/private_key.p8
private_key_passphrase: "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PASSPHRASE') }}"
```

**SSO Authentication**
```yaml
authenticator: externalbrowser
```

## Initial Project Setup

### 1. Initialize New Project

```bash
# Interactive setup
dbt init

# Manual setup
mkdir my_dbt_project
cd my_dbt_project
```

### 2. Create Project Structure

```
my_dbt_project/
├── dbt_project.yml
├── profiles.yml (in ~/.dbt/ directory)
├── models/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── tests/
├── macros/
├── snapshots/
└── analyses/
```

### 3. Configure dbt_project.yml

```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

profile: 'my_project'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_dbt_project:
    +materialized: view
    +persist_docs:
      relation: true
      columns: true
    
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
    
    silver:
      +materialized: ephemeral
      +tags: ["silver", "intermediate"]
    
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
```

### 4. Configure profiles.yml

Location: `~/.dbt/profiles.yml` (or `$DBT_PROFILES_DIR/profiles.yml`)

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('DBT_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: TRANSFORMER
      database: ANALYTICS_DEV
      warehouse: TRANSFORMING
      schema: "{{ env_var('DBT_USER') }}_dev"
      threads: 4
    
    prod:
      type: snowflake
      account: "{{ env_var('DBT_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: analytics
      threads: 8
```

## Environment Variables

### Create .env File

```bash
# .env file in project root (for Snowflake)
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=dbt_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_WAREHOUSE=TRANSFORMING
SNOWFLAKE_ROLE=TRANSFORMER
```

### Load Environment Variables

```bash
# Option 1: Export manually
export SNOWFLAKE_PASSWORD=your_password

# Option 2: Use python-dotenv
pip install python-dotenv

# Option 3: Use direnv
direnv allow

# Option 4: Use SnowSQL config
# Snowflake CLI automatically loads from ~/.snowsql/config
```

## Package Installation

### Create packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  
  - package: calogica/dbt_expectations
    version: [">=0.10.0", "<1.0.0"]
  
  - package: brooklyn-data/dbt_artifacts
    version: [">=2.0.0", "<3.0.0"]
```

### Install Packages

```bash
dbt deps
```

## Verify Installation

### Test Connection

```bash
dbt debug
```

Expected output:
```
Connection:
  account: xy12345.us-east-1
  user: dbt_user
  database: ANALYTICS
  warehouse: TRANSFORMING
  role: TRANSFORMER
  schema: dbt_dev
  Connection test: OK connection ok
```

### Run First Model

```bash
# Create simple model
echo "select 1 as id" > models/test_model.sql

# Run it
dbt run --select test_model
```

## IDE Setup

### VS Code

1. **Install Extensions:**
   - Python
   - dbt Power User (recommended)
   - SQL formatter

2. **Configure Settings:**
```json
{
    "python.defaultInterpreterPath": "/path/to/dbt/venv/bin/python",
    "dbt.queryLimit": 500
}
```

3. **Add .vscode/settings.json:**
```json
{
    "files.associations": {
        "*.sql": "jinja-sql"
    }
}
```

### DataGrip / IntelliJ

1. Configure Python interpreter
2. Install dbt plugin
3. Configure database connection

## Common Setup Issues

### Issue: `dbt: command not found`
**Solution:**
```bash
# Ensure pip install location is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Snowflake connection failures
**Solution:**
```bash
# Debug connection
dbt debug

# Check environment variables
echo $SNOWFLAKE_PASSWORD

# Verify profiles.yml location
ls ~/.dbt/profiles.yml

# Test Snowflake connection directly
snowsql -a xy12345.us-east-1 -u dbt_user
```

### Issue: Network/Firewall errors
**Solution:**
```bash
# Check Snowflake connectivity
ping xy12345.us-east-1.snowflakecomputing.com

# Configure Snowflake proxy if needed
# Add to profiles.yml:
# client_session_keep_alive: true
# private_link: true  # If using PrivateLink
```

### Issue: Package installation fails
**Solution:**
```bash
# Clear package cache
rm -rf dbt_packages/
dbt deps

# Or force reinstall
dbt deps --upgrade
```

### Issue: SSL/Certificate errors with Snowflake
**Solution:**
```bash
# Install system certificate support
pip install pip-system-certs

# For corporate firewalls, install with trusted hosts
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org dbt-core dbt-snowflake

# Configure Snowflake to use OCSP fail-open mode
# Add to profiles.yml:
# insecure_mode: true  # Only for testing, not recommended for production
```

## Development Workflow

### 1. Start New Feature

```bash
# Create feature branch
git checkout -b feature/new-model

# Switch to dev target
dbt run --target dev
```

### 2. Build Models

```bash
# Develop iteratively
dbt run --select model_name
dbt test --select model_name
```

### 3. Generate Documentation

```bash
dbt docs generate
dbt docs serve
```

### 4. Deploy to Production

```bash
# Deploy
dbt run --target prod
dbt test --target prod
```

## Best Practices

### 1. Use Virtual Environments

```bash
# Create virtual environment
python -m venv dbt_venv
source dbt_venv/bin/activate

# Install dbt
pip install dbt-core dbt-snowflake
```

### 2. Version Control

```gitignore
# .gitignore
target/
dbt_packages/
logs/
*.pyc
.env
.DS_Store
```

### 3. Separate Dev/Prod

```yaml
# Use schema prefixes in dev
dev:
  schema: "{{ env_var('DBT_USER') }}_dev"

prod:
  schema: "analytics"
```

### 4. Automate with Makefile

```makefile
# Makefile
.PHONY: setup run test docs

setup:
	dbt deps
	dbt debug

run:
	dbt run

test:
	dbt test

docs:
	dbt docs generate
	dbt docs serve

all: setup run test docs
```

## Platform-Specific Deployments

### dbt Cloud

For managed dbt deployment, see [dbt Cloud documentation](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features).

### dbt Projects on Snowflake

For native Snowflake integration, use the `dbt-projects-snowflake` skill for detailed setup.

### GitHub Actions

```yaml
# .github/workflows/dbt.yml
name: dbt CI
on: [pull_request]

jobs:
  dbt-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dbt
        run: pip install dbt-core dbt-snowflake
      - name: Run dbt
        run: |
          dbt deps
          dbt run
          dbt test
        env:
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
```

## Upgrade Path

### Upgrade dbt Version

```bash
# Check current version
dbt --version

# Upgrade to latest
pip install --upgrade dbt-core dbt-snowflake

# Or specific version
pip install dbt-core==1.7.0 dbt-snowflake==1.7.0
```

### Migration Checklist

- [ ] Review changelog for breaking changes
- [ ] Test in development environment
- [ ] Update dbt_project.yml version
- [ ] Update packages.yml dependencies
- [ ] Run full test suite
- [ ] Update documentation

## Resources

### Official Documentation
- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Discourse Community](https://discourse.getdbt.com/)
- [dbt Slack Community](https://www.getdbt.com/community/join-the-community)

### Learning Resources
- [dbt Learn](https://learn.getdbt.com/)
- [dbt Fundamentals](https://courses.getdbt.com/courses/fundamentals)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

---

**Related Documentation:**
- `QUICK_REFERENCE.md` - Essential commands
- `PROJECT_STRUCTURE.md` - Project organization
- `PERFORMANCE_OPTIMIZATION.md` - Configuration tuning

