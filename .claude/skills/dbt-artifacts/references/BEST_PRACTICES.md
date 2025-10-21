# dbt Artifacts - Best Practices

Strategic guidance for when and how to use dbt Artifacts for monitoring dbt execution.

## When to Use dbt Artifacts

### ✅ Use dbt Artifacts When:

**Cross-platform compatibility is critical**
- Running dbt from multiple platforms (dbt Cloud, local CLI, Airflow, etc.)
- Need consistent monitoring across all execution environments
- Team uses mixed deployment strategies

**Historical analysis is primary goal**
- Analyzing trends over 30+ days
- Long-term performance baseline tracking
- Quarterly or annual reporting on dbt execution
- Compliance or audit trail requirements

**Running dbt outside Snowflake**
- Using dbt Cloud exclusively
- Executing dbt from Airflow, Azure DevOps, GitHub Actions
- Local development with dbt CLI
- Any non-Snowflake execution environment

**Programmatic access to metadata required**
- Building custom dashboards in BI tools
- Integrating with existing observability platforms
- Creating custom alerting logic
- Feeding data to data catalogs or lineage tools

**Delayed reporting is acceptable**
- Runs on `on-run-end` hook (after full execution completes)
- Historical batch analysis vs real-time monitoring
- End-of-run summaries are sufficient

### ❌ Avoid dbt Artifacts When:

**Real-time monitoring is critical**
- Need immediate notification of failures
- Want to see execution progress during runs
- Require detailed trace spans and profiling
→ **Use**: dbt Projects on Snowflake Event Tables

**Running exclusively in Snowflake**
- Using dbt PROJECT objects in Snowflake
- Native Snowflake integration preferred
- Want Snowflake-native telemetry
→ **Use**: dbt Projects Event Tables

**Storage constraints exist**
- Limited database space for historical data
- Can't maintain growing execution history
- No archival strategy in place
→ **Use**: Event Tables with shorter retention or external logging

## Comparison: dbt Artifacts vs dbt Projects Event Tables

| Feature | dbt Artifacts | dbt Projects Event Tables |
|---------|--------------|---------------------------|
| **Execution Environment** | Any (Cloud, CLI, Airflow) | Snowflake native only |
| **Telemetry Timing** | On run completion (hook) | Real-time during execution |
| **Historical Data** | User-managed retention | Configurable retention policy |
| **Platform Integration** | Cross-platform | Snowflake-native |
| **Query Interface** | Standard SQL tables | Event table syntax |
| **Setup Complexity** | Package + hook config | dbt PROJECT configuration |
| **Trace Spans** | No | Yes (detailed profiling) |
| **Best For** | Historical analysis | Real-time monitoring |

## Combining Both Approaches

**Recommended: Use BOTH for comprehensive monitoring**

```
dbt Artifacts (Historical)          Event Tables (Real-time)
        ↓                                    ↓
Long-term trends                   Immediate alerts
Quarterly reports                  Live dashboards
Cross-platform metrics             Trace-level profiling
BI tool integration               Native Snowflake tools
```

**Example Architecture:**
1. **Event Tables**: Monitor active runs in real-time, alert on failures immediately
2. **dbt Artifacts**: Analyze historical patterns, track monthly trends, feed BI dashboards

## Performance Optimization

### Query Performance Best Practices

**ALWAYS:**
- ✅ Filter by `run_started_at` with specific date ranges
  ```sql
  WHERE run_started_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  ```
- ✅ Use `command_invocation_id` to link related executions efficiently
- ✅ Apply `HAVING COUNT(*) >= 5` to filter out one-off anomalies
- ✅ Join through both `command_invocation_id` AND `node_id` when linking metadata to executions

**NEVER:**
- ❌ Query entire table without date filtering
  ```sql
  -- BAD: Scans entire history
  SELECT * FROM test_executions WHERE status = 'fail';

  -- GOOD: Filtered by date
  SELECT * FROM test_executions
  WHERE status = 'fail'
    AND run_started_at >= DATEADD(day, -7, CURRENT_TIMESTAMP());
  ```
- ❌ Create alerts for every single test failure (too noisy)
- ❌ Store more than 6 months without archival strategy

### Storage Management

**Archival Strategy (Quarterly)**

```sql
-- Archive data older than 90 days
CREATE TABLE dbt_artifacts_archive.model_executions_2024_q4 AS
SELECT *
FROM dbt_artifacts.model_executions
WHERE run_started_at < DATEADD(day, -90, CURRENT_DATE());

-- Delete archived data from active tables
DELETE FROM dbt_artifacts.model_executions
WHERE run_started_at < DATEADD(day, -90, CURRENT_DATE());
```

**Storage Planning:**
- Small project (50 models, 100 tests): ~1-5 MB/week
- Medium project (200 models, 500 tests): ~10-20 MB/week
- Large project (1000+ models, 2000+ tests): ~50-100 MB/week

Plan for **1-2 GB per quarter** for medium projects.

## Monitoring Best Practices

### Test Quality Monitoring

**Establish baselines:**
- **Healthy**: Test failure rate < 5%
- **Warning**: Test failure rate 5-10%
- **Critical**: Test failure rate > 10%

**Identify flaky tests:**
- Failure rate between 10-90% (inconsistent results)
- Recommend investigation or test refactoring

**Alert on patterns:**
- New test with 100% failure rate (incorrect test logic)
- Previously stable test suddenly failing
- Test execution time 2x+ baseline

### Model Performance Monitoring

**Performance thresholds:**
- **Investigate**: Models consistently > 5 minutes
- **Critical**: Runtime increase > 2x historical average
- **Optimize**: Models in top 20 slowest (refer to `DBT_ARTIFACTS_QUERIES.sql`)

**Alert strategies:**
- High priority: Models with `status = 'error'`
- Medium priority: Runtime increase > 50% from baseline
- Low priority: Slow model trending (track over time)

### Execution Pattern Analysis

**Track invocation patterns:**
- Command frequency (run vs build vs test)
- Environment usage (dev vs prod)
- Timing patterns (peak hours, scheduled runs)
- Full refresh frequency and impact

**Identify anomalies:**
- Unusual command patterns (unexpected full refreshes)
- Environment misuse (production runs in dev)
- Off-schedule executions
- Excessive reruns of same models

## Integration Strategies

### BI Dashboard Integration

**Recommended approach:**

1. Create a consolidated view:
```sql
CREATE OR REPLACE VIEW dbt_monitoring_dashboard AS
SELECT
    i.command_invocation_id,
    i.dbt_command,
    i.run_started_at,
    i.target_name,
    m.name AS model_name,
    m.materialization,
    me.status,
    me.total_node_runtime AS runtime_seconds,
    me.rows_affected,
    t.name AS test_name,
    te.status AS test_status,
    te.failures AS test_failures
FROM dbt_artifacts.invocations i
LEFT JOIN dbt_artifacts.model_executions me ON i.command_invocation_id = me.command_invocation_id
LEFT JOIN dbt_artifacts.models m ON me.node_id = m.node_id AND me.command_invocation_id = m.command_invocation_id
LEFT JOIN dbt_artifacts.test_executions te ON i.command_invocation_id = te.command_invocation_id
LEFT JOIN dbt_artifacts.tests t ON te.node_id = t.node_id AND te.command_invocation_id = t.command_invocation_id
WHERE i.run_started_at >= DATEADD(day, -90, CURRENT_DATE());
```

2. Connect BI tool (Tableau, Power BI, Looker) to view
3. Build dashboards focusing on:
   - Test failure trends
   - Model performance over time
   - Run frequency and success rates
   - Environment-specific metrics

### Orchestration Tool Integration

**Airflow example:**
```python
from airflow.decorators import task

@task
def check_dbt_test_failures():
    """Check for recent dbt test failures and alert if found."""
    conn = get_snowflake_connection('snowflake_default')
    query = """
        SELECT COUNT(*) AS failure_count
        FROM dbt_artifacts.test_executions
        WHERE run_started_at >= CURRENT_DATE()
          AND status = 'fail'
    """
    result = conn.execute(query).fetchone()

    if result['failure_count'] > 0:
        raise Exception(f"dbt tests failed: {result['failure_count']} failures detected")

    return f"All tests passed ({result['failure_count']} failures)"
```

**Use cases:**
- Downstream pipeline gating (don't proceed if tests fail)
- Conditional execution based on model status
- Dynamic alerting based on failure patterns

### Alerting Best Practices

**High Priority (Immediate Action):**
- Test status = 'fail' or 'error'
- Model status = 'error'
- Critical model runtime > 2x baseline
- Production environment failures

**Medium Priority (Investigation Within 24h):**
- Test status = 'warn'
- Model skipped > 10% of runs
- Runtime increase > 50% from baseline
- Unusual invocation patterns

**Low Priority (Track Trends):**
- Slow model performance (not critical path)
- Test success rate slowly declining
- Incremental drift in execution duration

## Common Pitfalls and Solutions

### Pitfall 1: Query Performance Degradation

**Problem**: Queries become slow as historical data accumulates

**Solution**:
- Always filter by `run_started_at` with date ranges
- Archive data quarterly to separate tables
- Create summary tables for common aggregations
- Consider materialized views for frequent queries

### Pitfall 2: Alert Fatigue

**Problem**: Too many alerts for every minor issue

**Solution**:
- Set intelligent thresholds (5% test failure rate, not 0%)
- Use rate-based alerting (failures increasing over time)
- Whitelist expected failures (known issues, data freshness)
- Alert on patterns, not individual occurrences

### Pitfall 3: Incomplete Context

**Problem**: Alerts lack context for action

**Solution**:
- Include model/test name, run timestamp, environment
- Link to compiled SQL or dbt docs
- Show historical context (was this test always failing?)
- Provide runbook links for common failures

### Pitfall 4: Storage Growth

**Problem**: Artifacts tables grow unbounded

**Solution**:
- Implement quarterly archival process
- Set retention policies (6-12 months active data)
- Monitor table sizes regularly
- Compress archived tables with clustering

## Complementary Tools and Approaches

**Use dbt Artifacts with:**

1. **dbt Projects Event Tables** (Snowflake)
   - Real-time monitoring + historical analysis
   - Event Tables for immediate alerts, Artifacts for trends

2. **dbt Cloud Discovery API**
   - Job scheduling and orchestration
   - Cloud-specific metadata and lineage

3. **Elementary Data** (dbt package)
   - Data quality anomaly detection
   - Column-level profiling and monitoring

4. **Monte Carlo, Great Expectations**
   - Advanced data quality monitoring
   - ML-based anomaly detection

**Artifacts provides**: Execution metadata foundation
**Complementary tools provide**: Advanced analytics, anomaly detection, data profiling

## References

- **Query Scripts**: See `../scripts/` for individual executable query files
- **Setup Guide**: See `../SKILL.md` for installation and configuration
- **Package Documentation**: [brooklyn-data.github.io/dbt_artifacts](https://brooklyn-data.github.io/dbt_artifacts)
- **dbt Best Practices**: [docs.getdbt.com/guides/best-practices](https://docs.getdbt.com/guides/best-practices)
