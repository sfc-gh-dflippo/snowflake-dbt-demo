# Jenkins Pipeline Setup for dbt Deployment

This guide explains how to set up the Jenkins pipeline equivalent to the GitHub Actions workflow for
deploying dbt projects to Snowflake.

## Prerequisites

### 1. Jenkins Plugins Required

Install these plugins in Jenkins:

- **Pipeline**: For declarative pipeline syntax
- **Git Plugin**: For SCM checkout
- **Credentials Binding Plugin**: For secure credential handling
- **Pipeline Utility Steps**: For additional pipeline functionality
- **AnsiColor** (optional): For colored console output

### 2. Python Environment on Jenkins Agent

Ensure Python 3.11 is installed on the Jenkins agent:

```bash
python3.11 --version
```

### 3. System Dependencies

Install Snowflake CLI and other required tools on the Jenkins agent:

```bash
pip install snowflake-cli-labs
pip install dbt-core dbt-snowflake
pip install schemachange
```

## Jenkins Configuration

### 1. Create Jenkins Credentials

Navigate to **Jenkins → Manage Jenkins → Credentials** and create the following credentials for each
environment (development, test, production):

#### Private Keys (Secret Text)

- **ID**: `snowflake-private-key-production`
- **Description**: Snowflake Private Key for Production
- **Secret**: Paste the contents of your RSA private key

- **ID**: `snowflake-private-key-test`
- **Description**: Snowflake Private Key for Test
- **Secret**: Paste the contents of your RSA private key

- **ID**: `snowflake-private-key-development`
- **Description**: Snowflake Private Key for Development
- **Secret**: Paste the contents of your RSA private key

#### Passphrases (Secret Text)

- **ID**: `private-key-passphrase-production`
- **Secret**: Your private key passphrase

- **ID**: `private-key-passphrase-test`
- **Secret**: Your private key passphrase

- **ID**: `private-key-passphrase-development`
- **Secret**: Your private key passphrase

### 2. Configure Environment Variables

Navigate to **Jenkins → Manage Jenkins → System** and add these global environment variables (or
configure them per job):

#### Production Environment

```
SNOWFLAKE_ACCOUNT_PRODUCTION=your-account
SNOWFLAKE_USER_PRODUCTION=your-user
SNOWFLAKE_ROLE_PRODUCTION=your-role
SNOWFLAKE_WAREHOUSE_PRODUCTION=your-warehouse
SNOWFLAKE_DATABASE_PRODUCTION=your-database
SNOWFLAKE_SCHEMA_PRODUCTION=your-schema
SNOWFLAKE_THREADS_PRODUCTION=4
DBT_PROJECT_NAME_PRODUCTION=your-dbt-project
```

#### Test Environment

```
SNOWFLAKE_ACCOUNT_TEST=your-account
SNOWFLAKE_USER_TEST=your-user
SNOWFLAKE_ROLE_TEST=your-role
SNOWFLAKE_WAREHOUSE_TEST=your-warehouse
SNOWFLAKE_DATABASE_TEST=your-database
SNOWFLAKE_SCHEMA_TEST=your-schema
SNOWFLAKE_THREADS_TEST=4
DBT_PROJECT_NAME_TEST=your-dbt-project
```

#### Development Environment

```
SNOWFLAKE_ACCOUNT_DEVELOPMENT=your-account
SNOWFLAKE_USER_DEVELOPMENT=your-user
SNOWFLAKE_ROLE_DEVELOPMENT=your-role
SNOWFLAKE_WAREHOUSE_DEVELOPMENT=your-warehouse
SNOWFLAKE_DATABASE_DEVELOPMENT=your-database
SNOWFLAKE_SCHEMA_DEVELOPMENT=your-schema
SNOWFLAKE_THREADS_DEVELOPMENT=4
DBT_PROJECT_NAME_DEVELOPMENT=your-dbt-project
```

### 3. Create Pipeline Job

1. In Jenkins, click **New Item**
2. Enter a name (e.g., "Deploy-dbt-Project")
3. Select **Pipeline** and click OK
4. In the job configuration:

#### General Section

- Check **"This project is parameterized"** (optional, the Jenkinsfile already defines parameters)
- Add description: "Deploy dbt project to Snowflake"

#### Build Triggers

Choose one or more:

- **Build periodically**: Use cron syntax (e.g., `H 2 * * *` for nightly builds)
- **Poll SCM**: `H/5 * * * *` (check every 5 minutes)
- **GitHub hook trigger**: For webhook-based triggering

#### Pipeline Section

- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: Your repository URL
- **Credentials**: Your Git credentials
- **Branches to build**: `*/main`, `*/test`, `*/development` (or use wildcards)
- **Script Path**: `.github/workflows/Jenkinsfile.example`

5. Click **Save**

## Usage

### Manual Execution

1. Go to your pipeline job
2. Click **Build with Parameters**
3. Select the environment:
   - **auto**: Automatically determine based on branch (main=production, test=test,
     others=development)
   - **development**: Force development deployment
   - **test**: Force test deployment
   - **production**: Force production deployment
4. Click **Build**

### Automatic Execution

If you configured build triggers, the pipeline will run automatically when:

- Code is pushed to tracked branches (main, test)
- On a schedule (if configured)
- Via webhook from GitHub/GitLab

## Key Differences from GitHub Actions

| Aspect                    | GitHub Actions                                     | Jenkins                                                    |
| ------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| **Credentials**           | Stored in GitHub Secrets per environment           | Stored in Jenkins Credential Store per environment         |
| **Environment Variables** | Configured in GitHub Environment Variables         | Configured in Jenkins Global Properties or Job Properties  |
| **Python Setup**          | Uses `actions/setup-python@v6`                     | Requires Python pre-installed on agent, uses venv          |
| **Caching**               | Automatic with `cache: 'pip'`                      | Manual with `PIP_CACHE_DIR`                                |
| **Artifacts**             | `actions/upload-artifact@v4`                       | `archiveArtifacts` step                                    |
| **Environment Selection** | Automatic based on branch with GitHub Environments | Parameter-based or branch-based with environment variables |
| **Cleanup**               | Automatic by runner                                | Manual in `post` section                                   |

## Troubleshooting

### Python Not Found

If Python 3.11 is not available:

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# On RHEL/CentOS
sudo yum install python311
```

### Snowflake CLI Issues

Ensure the Snowflake CLI is properly installed:

```bash
pip install --upgrade snowflake-cli-labs
snow --version
```

### Permission Issues with Private Key

The pipeline sets `chmod 600` on the private key. Ensure the Jenkins user has write permissions in
the workspace.

### Environment Variable Not Found

Double-check that all environment variables are configured in Jenkins with the correct naming
pattern:

- `SNOWFLAKE_ACCOUNT_PRODUCTION`
- `SNOWFLAKE_ACCOUNT_TEST`
- `SNOWFLAKE_ACCOUNT_DEVELOPMENT`

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use Jenkins Credential Store** for all sensitive data
3. **Restrict job permissions** to authorized users only
4. **Rotate private keys** regularly
5. **Use separate service accounts** per environment
6. **Enable audit logging** in Jenkins
7. **Limit agent access** to only necessary resources

## Multi-Branch Pipeline (Advanced)

For automatic pipeline creation per branch, use a **Multibranch Pipeline** instead:

1. Create a new **Multibranch Pipeline** job
2. Configure the Git source
3. Rename `Jenkinsfile.example` to `Jenkinsfile` in your repository
4. Jenkins will automatically create a pipeline for each branch

This approach provides better branch isolation and automatic pipeline creation for feature branches.

## Notifications (Optional)

Add notification steps to the `post` section:

```groovy
post {
    success {
        // Slack notification
        slackSend(
            color: 'good',
            message: "dbt deployment to ${TARGET_ENV} succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )

        // Email notification
        emailext(
            subject: "SUCCESS: dbt Deployment to ${TARGET_ENV}",
            body: "The dbt project was successfully deployed.",
            to: 'team@example.com'
        )
    }

    failure {
        slackSend(
            color: 'danger',
            message: "dbt deployment to ${TARGET_ENV} failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )

        emailext(
            subject: "FAILED: dbt Deployment to ${TARGET_ENV}",
            body: "The dbt project deployment failed. Check logs for details.",
            to: 'team@example.com'
        )
    }
}
```

## References

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Credentials Binding Plugin](https://plugins.jenkins.io/credentials-binding/)
- [Snowflake CLI Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
- [dbt Documentation](https://docs.getdbt.com/)
