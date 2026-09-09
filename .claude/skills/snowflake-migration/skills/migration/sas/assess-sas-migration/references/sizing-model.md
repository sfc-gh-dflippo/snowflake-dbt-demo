# Sizing Model

## Per-File Effort Estimation

### Base Effort by Tier

| Tier | Min Hours | Typical Hours | Max Hours | Description |
|------|-----------|---------------|-----------|-------------|
| Tier 1 (SQL) | 0.5 | 1.5 | 4 | Direct SQL translation — CTAS, CTEs, window functions |
| Tier 2 (Stored Proc) | 2 | 5 | 12 | Procedural logic — cursors, state management, multi-step |
| Tier 3 (PySpark/SCOS) | 4 | 10 | 20 | Complex patterns — HASH, CALL EXECUTE, statistical modeling |

### Effort Multipliers

| Factor | Multiplier | When Applied |
|--------|-----------|--------------|
| LOW confidence | 1.5x | File has nested macros, dynamic %INCLUDE, or external LIBNAME |
| HIGH volume (>1000 lines) | 1.3x | Large files take proportionally longer to review |
| External DB dependency | 1.2x | Oracle/DB2/SQL Server passthrough requires function mapping |
| Boilerplate (DI Studio) | 0.7x | Scaffolding code is mostly deletable |
| Cross-file dependency | 0.9x per dependent | Files in same cluster share context (batch discount) |

### Formula

```
file_effort = base_hours[tier] × confidence_multiplier × volume_multiplier × external_multiplier × boilerplate_multiplier
```

Where `base_hours[tier]` uses the "Typical Hours" column by default.

### Portfolio-Level Effort

```
total_effort = SUM(file_effort for each file)
overhead_factor = 1.15  # integration testing, orchestration setup, documentation
total_with_overhead = total_effort × overhead_factor
```

---

## Staffing Model

### Team Composition by Portfolio Size

| Portfolio Size | SE (Snowflake) | Developer | QA | Duration |
|---------------|----------------|-----------|-----|----------|
| Small (≤20 files) | 0.25 FTE | 1 FTE | 0.25 FTE | 2-4 weeks |
| Medium (21-100 files) | 0.5 FTE | 2-3 FTE | 0.5 FTE | 6-12 weeks |
| Large (100+ files) | 0.5 FTE | 3-5 FTE | 1 FTE | 12-24 weeks |

### Timeline Formula

```
calendar_weeks = total_effort_hours / (developer_count × 30 hours/week × 0.8 utilization)
```

The 0.8 utilization accounts for meetings, context switching, and review cycles.

> **Phasing/sequencing lives in `references/wave-planning.md`.** This file covers effort and
> staffing only. To map effort onto the migration timeline, apply the wave plan from
> `wave-planning.md` — both deliverables share the same waves.

---

## Calibration Notes

These estimates are starting points derived from 50+ SAS migration engagements. Adjust based on:

1. **Pilot results**: After the pilot wave (see `wave-planning.md`), compare actual hours vs estimated — derive a site-specific correction factor
2. **Team expertise**: If the team has prior SAS experience, apply 0.8x multiplier
3. **Code quality**: If SAS code is well-documented with clear data flow, apply 0.9x
4. **Testing requirements**: If full regression testing required (not just compilation), add 30% to effort
