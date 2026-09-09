# Redshift Connection Reference

Detailed reference for Redshift connection options, authentication methods, and troubleshooting.

## Connection Options

### Required Parameters (All Auth Methods)

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-c, --connection` | Unique identifier for this connection |
| Database | `--database` | Target database name |
| Authentication | `--auth` | Auth method: `iam-provisioned-cluster`, `iam-serverless`, or `standard` |

### IAM Provisioned Cluster Parameters

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Cluster ID | `--cluster-id` | Yes | Redshift cluster identifier |
| Region | `--region` | Yes | AWS region (e.g., `us-west-2`) |
| User | `--user` | Yes | Database user for IAM auth |
| Access Key ID | `--access-key-id` | Yes | AWS Access Key ID |
| Secret Access Key | `--secret-access-key` | Yes | AWS Secret Access Key |

### IAM Serverless Parameters

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Workgroup | `--workgroup` | Yes | Redshift Serverless workgroup name |
| Region | `--region` | Yes | AWS region (e.g., `us-west-2`) |
| Access Key ID | `--access-key-id` | Yes | AWS Access Key ID |
| Secret Access Key | `--secret-access-key` | Yes | AWS Secret Access Key |

### Standard Auth Parameters

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Host | `--host` | Yes | Redshift endpoint hostname |
| Port | `--port` | No | Port number (default: 5439) |
| User | `--user` | Yes | Redshift username |
| Password | `--password` | Yes | Redshift password |

### Optional Parameters (All Methods)

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

## Authentication Methods

### IAM Provisioned Cluster (Recommended)

Uses AWS IAM credentials to authenticate with a provisioned Redshift cluster.

```bash
scai connection add-redshift \
  --connection my-redshift \
  --auth iam-provisioned-cluster \
  --user myuser \
  --cluster-id my-cluster \
  --database mydb \
  --region us-west-2 \
  --access-key-id AKIAXXXXXXXXXXXXXXXX \
  --secret-access-key <SECRET>
```

**When to use:**
- Production Redshift clusters
- When using AWS IAM for access control
- CI/CD pipelines with IAM roles

**Requirements:**
- AWS Access Key with `redshift:GetClusterCredentials` permission
- User must exist in Redshift (IAM creates temporary credentials)

### IAM Serverless

Uses AWS IAM credentials with Redshift Serverless workgroups.

```bash
scai connection add-redshift \
  --connection my-serverless \
  --auth iam-serverless \
  --workgroup my-workgroup \
  --database mydb \
  --region us-west-2 \
  --access-key-id AKIAXXXXXXXXXXXXXXXX \
  --secret-access-key <SECRET>
```

**When to use:**
- Redshift Serverless workgroups
- Variable workloads with auto-scaling
- Cost-optimized environments

### Standard Authentication

Uses Redshift username and password directly.

```bash
scai connection add-redshift \
  --connection my-redshift \
  --auth standard \
  --host my-cluster.xxxxxxxxxxxx.us-west-2.redshift.amazonaws.com \
  --port 5439 \
  --database mydb \
  --user myuser \
  --password <PASSWORD>
```

**When to use:**
- Quick testing and development
- When IAM is not configured
- Legacy setups

**Note:** IAM authentication is preferred for security.

## Troubleshooting

### Connection Timeout

**Symptoms:**
- "The operation has timed out"
- Connection hangs indefinitely

**Solutions:**
1. **Check VPN connection** - Most Redshift clusters are in private subnets
2. **Verify security groups** - Port 5439 must be allowed inbound
3. **Check network ACLs** - Subnet-level firewall rules
4. **Increase timeout:**
   ```bash
   scai connection add-redshift ... --connection-timeout 60
   ```

### Database Does Not Exist

**Symptoms:**
- `3D000: database "X" does not exist`

**Solutions:**
1. Verify the database name is correct
2. List databases on the cluster:
   ```sql
   SELECT datname FROM pg_database;
   ```
3. Common default databases: `dev`, `defaultdb`

### IAM Authentication Failed

**Symptoms:**
- "IAM authentication failed"
- "GetClusterCredentials failed"

**Solutions:**
1. Verify AWS Access Key ID and Secret are correct
2. Check IAM policy includes:
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "redshift:GetClusterCredentials",
       "redshift:DescribeClusters"
     ],
     "Resource": "*"
   }
   ```
3. Verify the user exists in Redshift
4. Check cluster ID matches exactly

### Invalid Credentials

**Symptoms:**
- "FATAL: password authentication failed"
- "Invalid username or password"

**Solutions:**
1. Verify username and password
2. Check if user account is locked
3. Verify user has access to the specified database

### Cluster Not Found

**Symptoms:**
- "Cluster not found"
- "Cannot describe cluster"

**Solutions:**
1. Verify cluster ID is correct (not the endpoint hostname)
2. Confirm cluster is in the specified region
3. Check cluster status is "available"

### Network/Firewall Issues

**Symptoms:**
- Connection timeout
- "Connection refused"

**Solutions:**

1. **Check if VPN is required:**
   ```bash
   # Check if you can reach the endpoint
   nc -zv <cluster-endpoint> 5439
   ```

2. **Verify security group rules:**
   - Inbound rule for port 5439 from your IP/CIDR

3. **Check if cluster is publicly accessible:**
   - Private clusters require VPN or VPC peering
   - Public clusters need your IP in security group

4. **Common VPN troubleshooting:**
   ```bash
   # Check VPN interface
   ifconfig | grep -E "utun|tun|ppp"
   
   # Check routing
   traceroute <cluster-endpoint>
   ```

## Connection String Format

For reference, Redshift uses PostgreSQL-compatible connection strings:

**Standard Auth:**
```
host=my-cluster.xxxx.us-west-2.redshift.amazonaws.com port=5439 dbname=mydb user=myuser password=***
```

**IAM Auth:**
IAM authentication generates temporary credentials internally.

## Verifying Connectivity

### Test with scai

```bash
scai connection test -l redshift -c <CONNECTION_NAME> --json
```

### Manual Network Test

```bash
# Test TCP connectivity to Redshift
nc -zv <cluster-endpoint> 5439

# Or with telnet
telnet <cluster-endpoint> 5439
```

### Using psql (if installed)

```bash
psql -h <cluster-endpoint> -p 5439 -d <database> -U <user>
```

## Finding Cluster Details

### AWS Console

1. Go to Amazon Redshift console
2. Select your cluster
3. Find:
   - **Cluster identifier** (for `--cluster-id`)
   - **Endpoint** (for `--host` in standard auth)
   - **Database name**
   - **Port** (usually 5439)

### AWS CLI

```bash
# List clusters
aws redshift describe-clusters --query 'Clusters[*].[ClusterIdentifier,Endpoint.Address,DBName]' --output table

# Get specific cluster details
aws redshift describe-clusters --cluster-identifier <CLUSTER_ID>
```

### Redshift Serverless

```bash
# List workgroups
aws redshift-serverless list-workgroups

# Get workgroup details
aws redshift-serverless get-workgroup --workgroup-name <WORKGROUP>
```
