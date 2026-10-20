# cisco_estate — multi-project dbt estate from real SnowConvert output

Four dbt projects that SnowConvert generated from the Cisco Informatica
PowerCenter workflows. The fixture covers both kinds of work the estate needs:
fixing each project (linter findings), then consolidating the projects.

## Source

- Repo: `snowflake-eng/ai-orchestrator-experiments`, commit
  `4cc9c93cbad1ead31dded1924d6c81be76776ec7`
- Input: `projects/cisco-etl/source/_etl/wf_*.xml`, 20 workflows from
  folder `EDW_Prod_104/EDWTD_BKG_AGGRS`

## Converter

- SnowConvert AI CLI `scai` 2.50.1-Pr.451 (preview channel), SQL Conversion
  Core 202.0.0, from `~/.local/bin/scai`
- One scai project per group. Commands:

```
scai init p_<group> -l Teradata -n <group> -i in_<group> -c prod_snowhouse
cd p_<group> && scai code convert -c prod_snowhouse --consolidate-dbt-projects
```

The default ETL target is dbt. `--consolidate-dbt-projects` makes one dbt
project per Informatica folder instead of one per mapping. All 20 workflows sit
in one folder, so every group's run produces one project at
`snowflake/_etl/EDW_Prod_104/EDWTD_BKG_AGGRS/pipelines/EDWTD_BKG_AGGRS/`. A
plain run without the flag produces 20 single-mapping projects.

The converter output is copied unchanged, with two exceptions:

- `name:` and `models:` key in each `dbt_project.yml`: `YOUR_PROJECT_NAME` is
  replaced by `cisco_<group>`
- the grouping into projects

`profiles.yml` contains only the converter's placeholders: `YOUR_PROFILE_NAME`,
`ACCOUNT`, `USERNAME`. No `target/`, `logs/` or `dbt_packages/` was produced.

## Grouping

Workflows are grouped by subject area, like a real estate
split by domain across teams.

| Project | Workflows |
|---|---|
| `cisco_bookings_quarterly` | MT_RSTD_BKGS_BY_QUARTER_CORP, MT_RSTD_BKGS_BY_QUARTER_NON_CORP, WI1_RSTD_BKGS_BY_QUARTER, MT_FDI_RSTD_BOOKINGS_FMTH, MT_FDI_RSTD_BOOKINGS_FQTR |
| `cisco_bookings_order_month` | MT_RSTD_BKGS_MEASURE_ORDER_MTH, WI_RSTD_BKGS_MEASURE_ORDER_MTH, WI1/WI2_RSTD_BKGS_ORDER_MTH, MT_RSTD_SA_BKGS_MONTH, MT_RSTD_BKGS_BY_WEEK, MT_RSTD_BKGS_PF_STL3_FWEEK, MT_RSTD_BKGS_PID_SL6_FWEEK, WI_BKGS_HIER |
| `cisco_audit_cost` | AUDIT_SERVICE_ANNUALISED, WI_AUD_RSTD_BKGS_MEASURE_ORDER_MTH, WI_BKGS_COST_MSR_MTH_CNTL, MT_BKGS_COST_MEASURE |
| `cisco_services_annuity` | MT_PRODUCT_HWSW_ANNUITY, MT_RSTD_BKGS_MSR_ANNUITY |

## Fix and consolidation opportunities

- **Duplicated macros.** `macros/generate_database_name.sql` and
  `macros/generate_schema_name.sql` are byte-identical in all four projects
  (MAC0015 ×8). They belong in one shared package.
- **Duplicated project scaffolding.** All four `dbt_project.yml`,
  `profiles.yml` and `sources.yml` files have the same shape. They share
  `profile: YOUR_PROFILE_NAME`, the `staging/intermediate/marts` defaults and
  the session vars (`STGDB`, `SLSORDVWDB`, `WORKDB`, `SLSORDDB`,
  `SESSSTARTTIME`, `PMSESSIONNAME`…) (PRJ0003, PRJ0004, PRJ0005, PRJ0014).
- **Colliding source name.** Each project declares `sources: - name: raw`
  against `YOUR_DB.YOUR_SCHEMA`. If the projects are merged, these `raw`
  sources collide.
- **Shared physical tables read across projects.** These tables are read
  through `{{ var(...) }}.TABLE` in several projects, so each one is a
  candidate for a single shared source:
  - `R_FISCAL_MONTH_TO_YEAR` (4 projects)
  - `R_FISCAL_DAY_TO_YEAR` (4 projects)
  - `MT_RSTD_BKGS_MEASURE` (4 projects)
  - `R_FISCAL_WEEK_TO_YEAR` (3 projects)
  - `N_BOOKINGS_CHANNEL_MEASURE` (3 projects)
  - `MT_RSTD_BKGS_MSR_ANNUITY` (3 projects)
  - `N_PRDT_TO_PRDT_CLSFTN_ALCTN` (2 projects)
  - `N_BKGS_CHNL_MEASURE` (2 projects)
  - `BKG_PROCESS_DT_CNTRL` (2 projects)
- **Cross-project producer/consumer.** `MT_RSTD_BKGS_MSR_ANNUITY` is written by
  `cisco_services_annuity` (`m_MT_RSTD_BKGS_MSR_ANNUITY`). It is read by
  `cisco_audit_cost` and `cisco_bookings_order_month`. After consolidation,
  those reads should become `ref()`s.
- **Colliding model names.** In each pair below, the same file name is
  generated twice, so the pair cannot coexist in one project without renaming:
  - `cisco_bookings_quarterly/models/m_MT_RSTD_BKGS_BY_QUARTER_CORP/marts/MT_RSTD_BKGS_BY_QUARTER1.sql`
    and `.../m_MT_RSTD_BKGS_BY_QUARTER_NON_CORP/marts/MT_RSTD_BKGS_BY_QUARTER1.sql`
  - `cisco_bookings_quarterly/models/m_WI1_RSTD_BKGS_BY_QUARTER/staging/stg_raw__SQ_MT_RSTD_BKGS_MEASURE.sql`
    and `cisco_bookings_order_month/models/m_MT_RSTD_BKGS_PID_SL6_FWEEK/staging/stg_raw__SQ_MT_RSTD_BKGS_MEASURE.sql`.
    This pair crosses projects.
  - `cisco_bookings_order_month/models/m_WI2_RSTD_BKGS_ORDER_MTH/staging/stg_raw__SQ_WI2_RSTD_BKGS_ORDER_MTH.sql`
    and `.../m_WI_RSTD_BKGS_MEASURE_ORDER_MTH/staging/stg_raw__SQ_WI2_RSTD_BKGS_ORDER_MTH.sql`
- **Repeated SQL across projects** (MAC0010 ×809). The fiscal-calendar join
  and the `PRODUCT_KEY` / `SALES_TERRITORY_KEY` sentinel `CASE` blocks repeat
  in up to 50 models across all 4 projects. They are macro candidates.
- **Identical CTEs** (SQL0002). Pairs of models share a byte-identical CTE:
  - `MT_RSTD_BKGS_PF_STL3_FWEEK` / `MT_RSTD_BKGS_PID_SL6_FWEEK`
  - `WI1_` / `WI2_RSTD_BKGS_ORDER_MTH1`
  - `WI_BKGS_MSR_ANNUITY_SW_PRDT_13` / `WI_BKGS_MSR_ATY_SW_PRDT_22`
- **Per-project fixes.**
  - Converter errors: MIG0001 in `cisco_audit_cost` and
    `cisco_services_annuity`; MIG0008 in `cisco_audit_cost`
  - Unsigned FDMs (MIG0003)
  - Relation locations taken from vars (PRJ0009)
  - Hook SQL taken from vars (INC0019)
  - Incremental models with no strategy, `unique_key` or `is_incremental()`
    guard
  - No tests (TST0001)
