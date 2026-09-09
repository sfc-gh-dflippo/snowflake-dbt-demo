# 1Password Integration for Source Database Connections

Use 1Password CLI (`op`) to securely inject credentials at runtime without exposing them in the shell.

## SQL Server

Search for an existing 1Password item:

```bash
op item list | grep -i sql
```

Get item details:

```bash
op item get <ITEM_NAME> --vault=<VAULT_NAME> --format=json
```

Add connection using `op run` with inline env-file:

```bash
op run --env-file=<(cat <<'EOF'
SERVER_URL="op://vault_name/item_name/host"
DATABASE="op://vault_name/item_name/db"
USER="op://vault_name/item_name/username"
PASSWORD="op://vault_name/item_name/password"
EOF
) -- bash -c 'scai connection add-sql-server \
  --connection <CONNECTION_NAME> \
  --auth standard \
  --server-url "$SERVER_URL" \
  --port 1433 \
  --database "$DATABASE" \
  --user "$USER" \
  --password "$PASSWORD"'
```

**Example with real values:**

```bash
op run --env-file=<(cat <<'EOF'
SERVER_URL="op://migrations_demo/sqlserver_adventureworks/host"
DATABASE="op://migrations_demo/sqlserver_adventureworks/db"
USER="op://migrations_demo/sqlserver_adventureworks/username"
PASSWORD="op://migrations_demo/sqlserver_adventureworks/password"
EOF
) -- bash -c 'scai connection add-sql-server \
  --connection sqlserver_adventureworks \
  --auth standard \
  --server-url "$SERVER_URL" \
  --port 1433 \
  --database "$DATABASE" \
  --user "$USER" \
  --password "$PASSWORD"'
```

---

## Redshift

Search for an existing 1Password item:

```bash
op item list | grep -i redshift
```

Get item details:

```bash
op item get <ITEM_NAME> --vault=<VAULT_NAME> --format=json
```

Add connection using `op run` with inline env-file:

```bash
op run --env-file=<(cat <<'EOF'
REDSHIFT_USER="op://vault_name/item_name/user"
REDSHIFT_CLUSTER_ID="op://vault_name/item_name/cluster_id"
REDSHIFT_DATABASE="op://vault_name/item_name/database"
REDSHIFT_REGION="op://vault_name/item_name/region"
ACCESS_KEY_ID="op://vault_name/item_name/access_key_id"
SECRET_ACCESS_KEY="op://vault_name/item_name/secret_access_key"
EOF
) -- bash -c 'scai connection add-redshift \
  --connection <CONNECTION_NAME> \
  --auth iam-provisioned-cluster \
  --user "$REDSHIFT_USER" \
  --cluster-id "$REDSHIFT_CLUSTER_ID" \
  --database "$REDSHIFT_DATABASE" \
  --region "$REDSHIFT_REGION" \
  --access-key-id "$ACCESS_KEY_ID" \
  --secret-access-key "$SECRET_ACCESS_KEY"'
```

**Example with real values:**

```bash
op run --env-file=<(cat <<'EOF'
REDSHIFT_USER="op://migrations_demo/redshift_scd_usw2/user"
REDSHIFT_CLUSTER_ID="op://migrations_demo/redshift_scd_usw2/cluster_id"
REDSHIFT_DATABASE="op://migrations_demo/redshift_scd_usw2/database"
REDSHIFT_REGION="op://migrations_demo/redshift_scd_usw2/region"
ACCESS_KEY_ID="op://migrations_demo/redshift_scd_usw2/access_key_id"
SECRET_ACCESS_KEY="op://migrations_demo/redshift_scd_usw2/secret_access_key"
EOF
) -- bash -c 'scai connection add-redshift \
  --connection redshift_scd_usw2 \
  --auth iam-provisioned-cluster \
  --user "$REDSHIFT_USER" \
  --cluster-id "$REDSHIFT_CLUSTER_ID" \
  --database "$REDSHIFT_DATABASE" \
  --region "$REDSHIFT_REGION" \
  --access-key-id "$ACCESS_KEY_ID" \
  --secret-access-key "$SECRET_ACCESS_KEY"'
```

---

## PostgreSQL

Search for an existing 1Password item:

```bash
op item list | grep -i postgres
```

Get item details:

```bash
op item get <ITEM_NAME> --vault=<VAULT_NAME> --format=json
```

Add connection using `op run` with inline env-file:

```bash
op run --env-file=<(cat <<'EOF'
PG_HOST="op://vault_name/item_name/host"
PG_PORT="op://vault_name/item_name/port"
PG_DATABASE="op://vault_name/item_name/database"
PG_USER="op://vault_name/item_name/username"
PG_PASSWORD="op://vault_name/item_name/password"
EOF
) -- bash -c 'scai connection add-postgresql \
  -c <CONNECTION_NAME> \
  --auth standard \
  --host "$PG_HOST" \
  --port "${PG_PORT:-5432}" \
  --database "$PG_DATABASE" \
  --user "$PG_USER" \
  --password "$PG_PASSWORD" \
  --ssl-mode Require'
```

**Example with real values:**

```bash
op run --env-file=<(cat <<'EOF'
PG_HOST="op://migrations_demo/postgresql_northwind/host"
PG_PORT="op://migrations_demo/postgresql_northwind/port"
PG_DATABASE="op://migrations_demo/postgresql_northwind/database"
PG_USER="op://migrations_demo/postgresql_northwind/username"
PG_PASSWORD="op://migrations_demo/postgresql_northwind/password"
EOF
) -- bash -c 'scai connection add-postgresql \
  -c postgresql_northwind \
  --auth standard \
  --host "$PG_HOST" \
  --port "${PG_PORT:-5432}" \
  --database "$PG_DATABASE" \
  --user "$PG_USER" \
  --password "$PG_PASSWORD" \
  --ssl-mode Require'
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `op://` strings stored instead of values | Wrap command in `bash -c '...'` with single quotes |
| "Not signed in" error | Run `op signin` first |
| "Item not found" | Verify vault and item names with `op item list --vault <vault>` |
| Variable not expanding | Ensure variable is inside `bash -c '...'` quotes, not outside |

## Why `bash -c '...'`?

The outer single quotes prevent the parent shell from expanding `$VARIABLE` etc. Instead, `op run` injects the resolved values into the environment, then the inner `bash -c` expands them from that environment.
