# Data Validation (GUI)

SnowConvert AI's Data Validation feature validates migrated data to ensure both structure and values
match the original source. This is the GUI-based validation within SnowConvert AI.

## Supported Sources

- SQL Server

> For SQL Server, Teradata, or Redshift CLI-based validation, see
> [Data Validation CLI](data-validation-cli.md).

## Validation Modes

### Schema Validation

Confirms the structure of migrated tables is preserved:

| Check                | Description                         |
| -------------------- | ----------------------------------- |
| Table name           | Names match between systems         |
| Column names         | All columns present with same names |
| Ordinal position     | Column order preserved              |
| Data types           | Types compatible or equivalent      |
| Character max length | Text column lengths match           |
| Numeric precision    | Precision and scale preserved       |
| Row count            | Total rows match                    |

### Metrics Validation

Confirms data values match the source by comparing aggregate metrics:

| Metric             | Description                            |
| ------------------ | -------------------------------------- |
| Minimum value      | MIN() matches for numeric/date columns |
| Maximum value      | MAX() matches for numeric/date columns |
| Average            | AVG() matches for numeric columns      |
| NULL count         | Count of NULLs matches per column      |
| DISTINCT count     | Unique value counts match              |
| Standard deviation | STDDEV() matches for numeric columns   |
| Variance           | VARIANCE() matches for numeric columns |

## Validation Results

Results are classified into three categories:

| Status | Meaning                                                                   |
| ------ | ------------------------------------------------------------------------- |
| ✓      | Values match exactly between source and Snowflake                         |
| ~      | Minor differences that don't affect data (e.g., higher numeric precision) |
| ✗      | Values don't match - requires investigation                               |

A CSV report is generated for detailed review and sharing.

## Prerequisites

- Python 3.10 to 3.13 installed and available in PATH
- Completed data migration to Snowflake

To verify Python version:

```bash
python --version
```

## Validation Steps

1. In SnowConvert AI, open **Validate data**:
   - After data migration: Click **Go to data validation**
   - From project: Select **Data validation**
2. Enter source database connection → **Test connection** → **Continue**
3. Select objects to validate
4. Click **Validate data**
5. Review results:
   - Success: "No differences found" message
   - Differences: Summary report with discrepancies
6. Open reports folder for CSV files

> **Warning**: Don't alter migrated data during validation to avoid false negatives.

## Documentation

- [Data Validation Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/data-validation)
