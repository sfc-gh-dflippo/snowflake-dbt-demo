# dbt Deployment Script for Snowflake

This directory contains a Python script for deploying dbt projects using Snowflake's native dbt
commands via the Snowflake CLI.

## 📋 Script Overview

### `deploy_dbt_project.py` - Python Deployment Script

Deploys your dbt project to Snowflake using the native `snow dbt deploy` command. This script:

- Checks dependencies (`snow` CLI and `dbt-core`)
- Tests Snowflake connection
- Verifies `deploy_config/profiles.yml` exists
- Cleans and installs dbt dependencies (`dbt clean`, `dbt deps`)
- Parses the dbt project using system profile (`dbt parse`)
- Temporarily copies `deploy_config/profiles.yml` to root for deployment
- Deploys to Snowflake using `snow dbt deploy`
- Cleans up temporary profiles after deployment
- Creates a dbt project object in Snowflake
- Supports force overwrite of existing projects

## 🚀 Quick Start

### Prerequisites

Before using the script, ensure you have:

1. **Snowflake CLI installed and configured**

   ```bash
   # Install Snowflake CLI
   pip install snowflake-cli

   # Configure connection (interactive)
   snow connection add
   ```

2. **dbt-core installed**

   ```bash
   # Install dbt-core (required for parsing)
   pip install dbt-core dbt-snowflake
   ```

3. **System dbt profile configured** The script uses your system dbt profile (from
   `~/.dbt/profiles.yml` or environment variables) for parsing.

4. **deploy_config/profiles.yml file** The script requires a `deploy_config/profiles.yml` file for
   the actual deployment to Snowflake. This file is temporarily copied to the root during deployment
   only.

5. **Snowflake dbt Projects feature enabled** This feature is currently in preview. Ensure your
   Snowflake account has access to dbt Projects on Snowflake.

### Basic Usage

#### Deploy Project

```bash
# Basic deployment
python deploy_dbt_project.py -n my_dbt_project -d MY_DATABASE -s MY_SCHEMA

# Deploy with specific connection and warehouse
python deploy_dbt_project.py -n analytics_pipeline -d PROD_DB -s ANALYTICS -c prod_connection -w COMPUTE_WH

# Force overwrite existing project
python deploy_dbt_project.py -n my_project -d DEV_DB -s TESTING -f

# Deploy with role specification
python deploy_dbt_project.py -n my_project -d PROD_DB -s ANALYTICS -r ANALYTICS_ROLE
```

## 📖 Detailed Usage

### Command Line Arguments

| Argument       | Short | Required | Description                      | Example          |
| -------------- | ----- | -------- | -------------------------------- | ---------------- |
| `--name`       | `-n`  | ✅       | dbt project name                 | `my_dbt_project` |
| `--database`   | `-d`  | ✅       | Target database name             | `ANALYTICS_DB`   |
| `--schema`     | `-s`  | ✅       | Target schema name               | `PROD_SCHEMA`    |
| `--connection` | `-c`  | ❌       | Snowflake connection name        | `default`        |
| `--warehouse`  | `-w`  | ❌       | Warehouse to use                 | `COMPUTE_WH`     |
| `--role`       | `-r`  | ❌       | Role to use                      | `ANALYTICS_ROLE` |
| `--force`      | `-f`  | ❌       | Force overwrite existing project | (flag)           |

### Examples

#### Development Environment

```bash
# Deploy to development environment
python deploy_dbt_project.py \
  -n dev_analytics \
  -d DEV_DATABASE \
  -s ANALYTICS \
  -c dev_connection \
  -w DEV_WH
```

#### Production Environment

```bash
# Deploy to production with specific role
python deploy_dbt_project.py \
  -n prod_analytics \
  -d PROD_DATABASE \
  -s ANALYTICS \
  -c prod_connection \
  -w PROD_WH \
  -r PROD_ANALYTICS_ROLE \
  -f
```

#### Testing Environment

```bash
# Deploy for testing (force overwrite)
python deploy_dbt_project.py \
  -n test_project \
  -d TEST_DB \
  -s SANDBOX \
  -f
```

## 🔧 Advanced Configuration

### Profile Configuration

The script uses two different profile configurations:

1. **System Profile** (for parsing and docs): Uses your standard dbt profile from
   `~/.dbt/profiles.yml` or environment variables
2. **Deployment Profile** (for `snow dbt deploy`): Uses `deploy_config/profiles.yml` temporarily
   copied to root

#### deploy_config/profiles.yml Structure

```yaml
SNOWFLAKE:
  target: dev
  outputs:
    dev:
      type: "snowflake"
      account: ""
      user: ""
      role: "YOUR_ROLE"
      database: "YOUR_DATABASE"
      warehouse: "YOUR_WAREHOUSE"
      schema: "YOUR_SCHEMA"
      threads: 8
```

### Environment Variables

The script respects standard Snowflake environment variables:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

## 📁 Generated Files

After successful deployment, you'll find:

```text
your-dbt-project/
├── deploy_dbt_project.py    # Python deployment script
├── deploy_config/
│   └── profiles.yml         # Deployment-specific profile
├── target/                  # dbt artifacts
│   ├── static_index.html    # Static documentation (generated)
│   ├── manifest.json        # dbt manifest
│   └── ...                  # Other dbt artifacts
├── dbt_packages/            # Installed packages
└── logs/                    # dbt logs
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Connection Test Fails

```bash
# Test your connection manually
snow connection test -c your_connection_name

# List available connections
snow connection list
```

#### 2. Parsing Fails

- Ensure your system dbt profile is properly configured
- Check that all required environment variables are set
- Verify database/schema permissions

#### 3. Deployment Fails

- Verify `deploy_config/profiles.yml` exists and is properly formatted
- Check that the target database and schema exist
- Ensure you have appropriate permissions for the deployment

#### 4. Profile Issues

```bash
# Check if dbt can find your profile
dbt debug

# Verify profile configuration
cat ~/.dbt/profiles.yml
```

### Debug Mode

For detailed logging, you can modify the script to enable debug mode or check the generated logs in
the `logs/` directory.

## 🔄 Workflow Integration

### CI/CD Pipeline Example

```yaml
# GitHub Actions example
- name: Deploy dbt Project
  run: |
    python deploy_dbt_project.py \
      -n ${{ github.event.repository.name }} \
      -d ${{ vars.SNOWFLAKE_DATABASE }} \
      -s ${{ vars.SNOWFLAKE_SCHEMA }} \
      -c ${{ vars.SNOWFLAKE_CONNECTION }} \
      -f
```

### Local Development Workflow

```bash
# 1. Deploy your project
python deploy_dbt_project.py -n my_project -d DEV_DB -s MY_SCHEMA -f

# 2. Run dbt commands via Snowflake CLI
snow dbt execute my_project -c default run
snow dbt execute my_project -c default test
snow dbt execute my_project -c default build

# 3. Check deployed objects
snow sql -q "SHOW TABLES IN SCHEMA DEV_DB.MY_SCHEMA" -c default
```

## 📊 Monitoring & Management

### Check Deployment Status

```bash
# List deployed dbt projects
snow dbt list -c default

# Check project objects
snow sql -q "SHOW OBJECTS IN SCHEMA YOUR_DATABASE.YOUR_SCHEMA" -c default
```

### Execute dbt Commands

```bash
# Run models
snow dbt execute your_project_name -c default run

# Run tests
snow dbt execute your_project_name -c default test

# Build everything
snow dbt execute your_project_name -c default build

# Run specific models
snow dbt execute your_project_name -c default run --select model_name

# Run with full refresh
snow dbt execute your_project_name -c default run --full-refresh
```

---

## 🔗 Related Documentation

- [Snowflake CLI dbt Commands](https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/dbt-commands)
- [dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial)
- [DBT_SETUP_GUIDE.md](./DBT_SETUP_GUIDE.md) - Detailed dbt setup instructions

---

**Note**: This script is designed for Snowflake's dbt Projects feature, which is currently in
preview. Features and syntax may change as the service evolves.
