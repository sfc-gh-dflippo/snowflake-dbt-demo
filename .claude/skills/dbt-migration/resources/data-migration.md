# Data Migration

SnowConvert AI's Data Migration feature transfers actual table data from source systems to Snowflake
after the database structure is deployed.

## Supported Sources

| Source     | Method                                                    |
| ---------- | --------------------------------------------------------- |
| SQL Server | Direct optimized data transfer                            |
| Redshift   | Unload to S3 (PARQUET) → COPY to Snowflake stage → tables |

## Prerequisites

### General Requirements

- Database structure deployed in Snowflake
- Active connections to both source database and Snowflake account
- Sufficient permissions for data operations on both systems

### Amazon Redshift Requirements

**S3 Bucket:**

- S3 bucket in same AWS region as Redshift cluster
- Empty bucket path (process fails if files exist in specified path)

**IAM Role for Redshift (unload data to S3):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:GetBucketLocation", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::<your_bucket_name>/*", "arn:aws:s3:::<your_bucket_name>"]
    }
  ]
}
```

**IAM User for S3 Access (read/delete from S3):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": ["arn:aws:s3:::<your_bucket_name>/*", "arn:aws:s3:::<your_bucket_name>"]
    }
  ]
}
```

> **Warning**: Without `s3:DeleteObject` and `s3:DeleteObjectVersion` permissions, temporary data
> files won't be deleted from S3 even if migration succeeds.

### SQL Server Requirements

- Valid connection to SQL Server source database
- Appropriate permissions to read data from source tables
- Network connectivity between migration tool and both systems

## Migration Steps

### SQL Server

1. Open project in SnowConvert AI → Select **Migrate data**
2. Enter source database connection → **Continue**
3. Enter Snowflake connection → **Continue**
4. Select tables to migrate
5. Click **Migrate data**
6. Review results → **Go to data validation**

### Amazon Redshift

1. Open project in SnowConvert AI → Select **Migrate data**
2. Enter source database connection → **Continue**
3. Enter Snowflake connection → **Continue**
4. Configure S3 bucket:
   - Database and Schema selection
   - Stage for data files
   - S3 bucket URI (must end with `/`)
   - Data unloading IAM role ARN
5. Select tables to migrate
6. Click **Migrate data**
7. Review results → **Go to data validation**

## Next Step

After data migration completes, proceed to [Data Validation](data-validation.md) to verify data
accuracy.

## Documentation

- [Data Migration Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/data-migration)
