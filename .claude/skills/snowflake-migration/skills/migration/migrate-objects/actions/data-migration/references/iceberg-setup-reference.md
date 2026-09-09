# Iceberg Prerequisites — Automated Setup Reference

> **Scope:** Iceberg target migration is **Redshift-only** (partial support). Use this reference when `target_table_type=iceberg` and the source is Redshift. For workflow field definitions, see [workflow-config-reference.md](./workflow-config-reference.md). For orchestrator behavior, see `dmvf/docs/data-migration-orchestrator/iceberg-migration-support.md`.

This reference provides step-by-step procedures for the AI agent to execute when setting up Iceberg migration prerequisites. Each section is a self-contained procedure with input collection, execution commands, and verification.

> **Important**: These procedures use **AWS CLI** and **Snowflake SQL**. The agent should execute commands directly and parse outputs to chain steps together (e.g., extracting Snowflake-generated IAM ARNs from DESCRIBE results).

---

## Prerequisite Decision Matrix

Not all prerequisites are needed for every strategy. Use this matrix to determine which sections to execute:

| Prerequisite | `catalog_link` | `convert_to_managed` | `copy_files` |
|---|---|---|---|
| IAM Role (S3 access) | Required | Required | Required |
| IAM Role (Glue access) | Required | Required | Not needed |
| External Volume | Required | Required | Required |
| Catalog Integration | Required | Required | Not needed |
| Storage Integration + Stage | Not needed | Not needed | Needed (if `sourceDataStage`) |
| Grants | Required | Required | Required |

---

## Section A: IAM Role Setup (AWS CLI)

### Inputs to collect

| Input | Description | Example |
|-------|-------------|---------|
| `AWS_ACCOUNT_ID` | AWS account number | `123456789012` |
| `AWS_REGION` | AWS region where resources reside | `us-west-2` |
| `S3_BUCKET_NAME` | S3 bucket containing Iceberg data | `my-iceberg-bucket` |
| `IAM_ROLE_NAME` | Name for the new IAM role | `SnowflakeIcebergRole` |
| `NEEDS_GLUE` | Whether Glue permissions are needed (catalog_link/convert_to_managed) | `true` / `false` |
| `GLUE_DATABASE` | Glue database name (only if `NEEDS_GLUE=true`) | `iceberg_tpch` |

### Step A.1: Verify AWS CLI is available

```bash
aws --version
aws sts get-caller-identity
```

If `aws` is not installed, instruct the user to install it: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

If `get-caller-identity` fails, instruct the user to run `aws configure` or set `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.

### Step A.2: Create IAM role with placeholder trust policy

Create the role with a temporary trust policy. The real Snowflake IAM ARN will be filled in after the external volume is created (Section B).

```bash
aws iam create-role \
  --role-name <IAM_ROLE_NAME> \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:root"},
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "sts:ExternalId": "placeholder-will-be-updated"
          }
        }
      }
    ]
  }' \
  --description "IAM role for Snowflake Iceberg external volume access"
```

Record the output `Role.Arn` — this is `<IAM_ROLE_ARN>` used in subsequent steps.

### Step A.3: Attach S3 permissions policy

```bash
aws iam put-role-policy \
  --role-name <IAM_ROLE_NAME> \
  --policy-name SnowflakeIcebergS3Access \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:PutObject",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:DeleteObject",
          "s3:DeleteObjectVersion"
        ],
        "Resource": "arn:aws:s3:::<S3_BUCKET_NAME>/*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ],
        "Resource": "arn:aws:s3:::<S3_BUCKET_NAME>"
      }
    ]
  }'
```

### Step A.4: Attach Glue permissions policy (only if `NEEDS_GLUE=true`)

```bash
aws iam put-role-policy \
  --role-name <IAM_ROLE_NAME> \
  --policy-name SnowflakeIcebergGlueAccess \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "glue:GetTable",
          "glue:GetTables",
          "glue:GetDatabase",
          "glue:GetDatabases"
        ],
        "Resource": [
          "arn:aws:glue:<AWS_REGION>:<AWS_ACCOUNT_ID>:catalog",
          "arn:aws:glue:<AWS_REGION>:<AWS_ACCOUNT_ID>:database/<GLUE_DATABASE>",
          "arn:aws:glue:<AWS_REGION>:<AWS_ACCOUNT_ID>:table/<GLUE_DATABASE>/*"
        ]
      }
    ]
  }'
```

### Step A.5: Verify the role was created

```bash
aws iam get-role --role-name <IAM_ROLE_NAME>
```

Confirm `Role.Arn` is present. This value is `<IAM_ROLE_ARN>`.

---

## Section B: External Volume Setup (Snowflake SQL + AWS CLI)

### Inputs to collect

| Input | Description | Example |
|-------|-------------|---------|
| `VOLUME_NAME` | Name for the external volume | `my_iceberg_ext_vol` |
| `S3_BASE_URL` | S3 base URL for Iceberg data | `s3://my-iceberg-bucket/data/` |
| `IAM_ROLE_ARN` | Role ARN from Section A | `arn:aws:iam::123456789012:role/SnowflakeIcebergRole` |

### Step B.1: Create the external volume in Snowflake

```sql
CREATE EXTERNAL VOLUME IF NOT EXISTS <VOLUME_NAME>
  STORAGE_LOCATIONS = (
    (
      NAME = 'iceberg-s3-location'
      STORAGE_BASE_URL = '<S3_BASE_URL>'
      STORAGE_PROVIDER = 'S3'
      STORAGE_AWS_ROLE_ARN = '<IAM_ROLE_ARN>'
    )
  );
```

### Step B.2: Extract Snowflake-generated IAM ARN and External ID

```sql
DESCRIBE EXTERNAL VOLUME <VOLUME_NAME>;
```

Parse the output to extract:
- `STORAGE_AWS_IAM_USER_ARN` — Snowflake's IAM user ARN (e.g. `arn:aws:iam::...:user/...`)
- `STORAGE_AWS_EXTERNAL_ID` — Snowflake's external ID string

> **Agent implementation note**: The DESCRIBE output contains a JSON property list. Look for the rows where `property` is `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` under the `STORAGE_LOCATION_1` parent.

### Step B.3: Update IAM trust policy with Snowflake-generated values

```bash
aws iam update-assume-role-policy \
  --role-name <IAM_ROLE_NAME> \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "<STORAGE_AWS_IAM_USER_ARN>"
        },
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "sts:ExternalId": "<STORAGE_AWS_EXTERNAL_ID>"
          }
        }
      }
    ]
  }'
```

### Step B.4: Wait and verify access

IAM trust policy changes can take up to 60 seconds to propagate. Wait, then verify:

```sql
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('<VOLUME_NAME>');
```

If `SYSTEM$VERIFY_EXTERNAL_VOLUME` is not available, verify by creating a test Iceberg table or checking that `DESCRIBE EXTERNAL VOLUME` shows no errors.

---

## Section C: Catalog Integration Setup (Snowflake SQL + AWS CLI)

> **Only needed for `catalog_link` and `convert_to_managed` strategies.**

### Inputs to collect

| Input | Description | Example |
|-------|-------------|---------|
| `INTEGRATION_NAME` | Name for the catalog integration | `my_glue_catalog_integration` |
| `GLUE_DATABASE` | AWS Glue database namespace | `iceberg_tpch` |
| `GLUE_CATALOG_ID` | AWS account ID (same as `AWS_ACCOUNT_ID`) | `123456789012` |
| `AWS_REGION` | AWS region for Glue | `us-west-2` |
| `IAM_ROLE_ARN` | Role ARN from Section A (must have Glue permissions) | `arn:aws:iam::123456789012:role/SnowflakeIcebergRole` |

### Step C.1: Create the catalog integration in Snowflake

```sql
CREATE CATALOG INTEGRATION IF NOT EXISTS <INTEGRATION_NAME>
  CATALOG_SOURCE = GLUE
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = '<GLUE_DATABASE>'
  GLUE_AWS_ROLE_ARN = '<IAM_ROLE_ARN>'
  GLUE_CATALOG_ID = '<GLUE_CATALOG_ID>'
  GLUE_REGION = '<AWS_REGION>'
  ENABLED = TRUE;
```

### Step C.2: Extract Snowflake-generated IAM ARN and External ID

```sql
DESCRIBE CATALOG INTEGRATION <INTEGRATION_NAME>;
```

Parse the output for `GLUE_AWS_IAM_USER_ARN` and `GLUE_AWS_EXTERNAL_ID`.

### Step C.3: Update IAM trust policy to include catalog integration principal

If the external volume and catalog integration use the **same IAM role**, the trust policy must include **both** Snowflake principals. Update the trust policy to have two statements:

```bash
aws iam update-assume-role-policy \
  --role-name <IAM_ROLE_NAME> \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "<STORAGE_AWS_IAM_USER_ARN>"
        },
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "sts:ExternalId": "<STORAGE_AWS_EXTERNAL_ID>"
          }
        }
      },
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "<GLUE_AWS_IAM_USER_ARN>"
        },
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "sts:ExternalId": "<GLUE_AWS_EXTERNAL_ID>"
          }
        }
      }
    ]
  }'
```

> If using **separate IAM roles** for external volume and catalog integration, only the catalog integration's role needs updating in this step.

### Step C.4: Verify the catalog integration

```sql
DESCRIBE CATALOG INTEGRATION <INTEGRATION_NAME>;
```

Confirm `ENABLED = true` and no error messages.

---

## Section D: Storage Integration + External Stage Setup (Snowflake SQL)

> **Only needed for `copy_files` strategy with `sourceDataStage`.**

### Inputs to collect

| Input | Description | Example |
|-------|-------------|---------|
| `STORAGE_INTEGRATION_NAME` | Name for the storage integration | `my_s3_integration` |
| `S3_BUCKET_URL` | S3 URL for Parquet files | `s3://my-iceberg-bucket/data/` |
| `IAM_ROLE_ARN` | Role ARN from Section A | `arn:aws:iam::123456789012:role/SnowflakeIcebergRole` |
| `TARGET_DB` | Target database in Snowflake | `MANUEL_BUGBASH` |
| `TARGET_SCHEMA` | Target schema in Snowflake | `PUBLIC` |
| `STAGE_NAME` | Name for the external stage | `ICEBERG_SOURCE_STAGE` |

### Step D.1: Create the storage integration

```sql
CREATE STORAGE INTEGRATION IF NOT EXISTS <STORAGE_INTEGRATION_NAME>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = '<IAM_ROLE_ARN>'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('<S3_BUCKET_URL>');
```

### Step D.2: Extract Snowflake-generated IAM ARN and External ID

```sql
DESCRIBE STORAGE INTEGRATION <STORAGE_INTEGRATION_NAME>;
```

Parse the output for `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID`.

### Step D.3: Update IAM trust policy

Same pattern as Section B.3 — update the IAM role's trust policy with the Snowflake-generated ARN and external ID. If this role is shared with the external volume, merge both principals into a single trust policy (same pattern as Section C.3).

### Step D.4: Create the external stage

```sql
CREATE STAGE IF NOT EXISTS <TARGET_DB>.<TARGET_SCHEMA>.<STAGE_NAME>
  URL = '<S3_BUCKET_URL>'
  STORAGE_INTEGRATION = <STORAGE_INTEGRATION_NAME>;
```

### Step D.5: Verify files are accessible

```sql
LIST @<TARGET_DB>.<TARGET_SCHEMA>.<STAGE_NAME>;
```

Confirm Parquet files are listed. If empty, check that the S3 URL is correct and the IAM trust policy has propagated.

---

## Section E: Grant Privileges

### Step E.1: Grant Iceberg table creation

```sql
GRANT CREATE ICEBERG TABLE ON SCHEMA <TARGET_DB>.<TARGET_SCHEMA> TO ROLE <MIGRATION_ROLE>;
```

### Step E.2: Grant external volume usage

```sql
GRANT USAGE ON EXTERNAL VOLUME <VOLUME_NAME> TO ROLE <MIGRATION_ROLE>;
```

### Step E.3: Grant catalog integration usage (if applicable)

```sql
GRANT USAGE ON INTEGRATION <INTEGRATION_NAME> TO ROLE <MIGRATION_ROLE>;
```

### Step E.4: Grant stage usage (if applicable)

```sql
GRANT USAGE ON STAGE <TARGET_DB>.<TARGET_SCHEMA>.<STAGE_NAME> TO ROLE <MIGRATION_ROLE>;
```

---

## Automated Setup Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                   ICEBERG SETUP FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Collect inputs (AWS account, S3 bucket, region, etc.)   │
│                                                             │
│  2. [AWS CLI] Create IAM role with placeholder trust        │
│     └── Attach S3 permissions policy                        │
│     └── Attach Glue permissions policy (if needed)          │
│                                                             │
│  3. [Snowflake SQL] CREATE EXTERNAL VOLUME                  │
│     └── DESCRIBE to get Snowflake IAM ARN + External ID     │
│     └── [AWS CLI] Update trust policy with real values       │
│                                                             │
│  4. [Snowflake SQL] CREATE CATALOG INTEGRATION (if needed)  │
│     └── DESCRIBE to get Snowflake IAM ARN + External ID     │
│     └── [AWS CLI] Update trust policy (merge principals)     │
│                                                             │
│  5. [Snowflake SQL] CREATE STORAGE INTEGRATION (if needed)  │
│     └── CREATE STAGE                                         │
│     └── LIST @stage to verify                                │
│                                                             │
│  6. [Snowflake SQL] GRANT privileges                        │
│                                                             │
│  7. Verify all prerequisites (checklist)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
