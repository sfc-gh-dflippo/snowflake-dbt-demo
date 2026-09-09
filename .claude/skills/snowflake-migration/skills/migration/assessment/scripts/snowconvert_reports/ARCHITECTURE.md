# `snowconvert_reports` — Architecture

> Shared data access layer for SnowConvert assessment reports.
> All sub-skills import from here instead of re-implementing CSV/JSON parsing.

---

## Package Structure

```
scripts/snowconvert_reports/
├── __init__.py                      # Public API re-exports
├── models/
│   ├── issue.py                     # IssueRecord        ← Issues.csv
│   ├── element.py                   # Element            ← Elements.csv
│   ├── code_unit.py                 # TopLevelCodeUnit   ← TopLevelCodeUnits.csv
│   ├── object_reference.py          # ObjectReference    ← ObjectReferences.*.csv
│   ├── partition_member.py          # PartitionMember    ← PartitionMembership.csv
│   └── estimation.py                # IssueEstimationEntry, SeverityBaseline, ObjectEstimation
├── loaders/
│   ├── csv_reader.py                # read_csv_rows(), load_csv_as()
│   ├── elements_loader.py           # load_elements()
│   ├── issues_loader.py             # load_issues(filter_code=)
│   ├── code_units_loader.py         # load_code_units()
│   ├── object_references_loader.py  # load_object_references(), load_missing_references()
│   ├── partition_loader.py          # load_partition_membership()
│   ├── registry_loader.py           # Code Unit Registry entries
│   ├── estimation_loader.py         # load_issues_estimation_json(), load_object_estimations()
│   └── project_config.py            # read_project_name()  ← .scai/config/project.yml
├── services/
│   ├── issue_effort_service.py      # IssueEffortService (unified effort/severity lookup)
│   ├── report_finder.py             # ReportFinder (glob-based file discovery)
│   └── assessment_metadata.py       # assessment.json read/write + resolve_assessment_name()
├── conversion_status.py             # Per-unit conversion status vocabulary
├── data_migration_readiness.py      # Registry → per-table data-migration readiness
├── data_types_scan.py               # Column types extracted from captured DDL
├── type_coverage.py                 # Per-dialect type coverage + drift guard
├── testing_readiness.py             # Registry → testing readiness; owns normalize_dialect
└── data/
    └── issues_ref.json              # Bundled issue reference (for offline/ETL use)
```

The five modules at package root differ from `loaders/` and `models/` in kind: they are **readiness
computation** for the multi-report's journey tabs, not raw-file parsing. They read the Code Unit
Registry rather than SnowConvert CSVs, and each returns a frozen dataclass the render layer in
`scripts/data_migration_report/` or `scripts/testing_report/` consumes without further computation.

---

## Layered Architecture

```
 ╔═══════════════════════════════════════════════════════════════════╗
 ║                    SnowConvert Assessment Reports                ║
 ║                    (CSV / JSON / TXT files on disk)              ║
 ╚════════════════════════════════╤══════════════════════════════════╝
                                  │
                                  ▼
 ┌────────────────────────────────────────────────────────────────────┐
 │                                                                    │
 │                    snowconvert_reports (shared lib)                 │
 │                                                                    │
 │   ┌──────────┐      ┌──────────┐      ┌──────────────────────┐   │
 │   │  models/  │◄─────│ loaders/ │      │      services/       │   │
 │   │          │      │          │      │                      │   │
 │   │ frozen   │      │ csv_     │      │ IssueEffortService   │   │
 │   │ data-    │      │  reader  │      │   .from_json_file()  │   │
 │   │ classes  │      │   ▲      │      │   .from_bundled()    │   │
 │   │          │      │   │      │      │   .get_effort_hours()│   │
 │   │ 1 model  │      │ typed    │      │                      │   │
 │   │ per CSV  │      │ loaders  │      │ ReportFinder         │   │
 │   │ file     │      │ (1 per   │      │   .find(base_name)   │   │
 │   │ type     │      │  report) │      │   .find_issues()     │   │
 │   └──────────┘      └──────────┘      └──────────────────────┘   │
 │                                                                    │
 └─────────────────────────────┬──────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┬─────────────────┐
          │                    │                    │                 │
          ▼                    ▼                    ▼                 ▼
 ┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
 │     ETL     │   │    Waves     │   │  SQL Dynamic │   │  Exclusion   │
 │  Assessment │   │  Generator   │   │   Analyzer   │   │  Detection   │
 │             │   │              │   │              │   │              │
 │ SSIS/DTSX   │   │ scai         │   │ SSC-EWI-0030 │   │ Naming       │
 │ package     │   │ assessment   │   │ pattern      │   │ patterns,    │
 │ analysis    │   │ waves →      │   │ detection &  │   │ duplicate    │
 │             │   │ HTML reports │   │ tracking     │   │ detection    │
 └─────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

---

## Import Dependency Graph

Shows exactly what each sub-skill imports from the shared library.

```
snowconvert_reports
│
├──► etl-assessment
│    ├── ElementRepository      → load_elements, Element
│    ├── IssueRepository        → read_csv_rows
│    ├── IssueLookupService     → IssueEffortService
│    └── IssueLoader            → IssueEffortService
│
├──► waves-generator
│    └── load_data_html_report  → load_issues_estimation_json
│                                  load_code_units
│                                  load_partition_membership
│                                  load_object_estimations
│                                  load_object_references
│                                  ReportFinder
│    (wave *creation* lives in the SCAI CLI — `scai assessment waves` —
│     and emits `waves_analysis_*.json` consumed via `WavesJsonAdapter`)
│
├──► analyzing-sql-dynamic-patterns
│    └── (no in-skill loaders)  → handled by `scai assessment sql-dynamic`,
│                                   which reads the project (registry/CSV) and
│                                   emits `sql_dynamic_analysis.json`
│
└──► object_exclusion_detection
     └── (no in-skill loaders)  → handled by `scai assessment object-exclusion`,
                                   which reads the SnowConvert reports / registry
                                   directly and emits `object_exclusion_analysis_*.json`
```

---

## Data Flow: From Raw Reports to Sub-Skill Domain Models

```
                         ┌───────────────────────┐
                         │  SnowConvert Reports   │
                         │  ─────────────────     │
                         │  Elements.csv          │
                         │  Issues.csv            │
                         │  TopLevelCodeUnits.csv │
                         │  ObjectReferences.csv  │
                         │  PartitionMembership   │
                         │  IssuesEstimation.json │
                         └───────────┬───────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   csv_reader.py      │
                          │   ───────────────    │
                          │   read_csv_rows()    │
                          │   • utf-8-sig → utf-8│
                          │     → latin-1        │
                          │   • strips all values│
                          │   • yields dict rows │
                          └──────────┬───────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   Typed Loaders      │
                          │   ─────────────      │
                          │   load_csv_as(       │
                          │     path, factory)   │
                          │                      │
                          │   factory = Model    │
                          │     .from_csv_row    │
                          └──────────┬───────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   Frozen Dataclasses │
                          │   ─────────────────  │
                          │   list[Element]      │
                          │   list[IssueRecord]  │
                          │   list[TopLevel...]  │
                          │   list[ObjectRef]    │
                          └──────────┬───────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
            ▼                        ▼                        ▼
  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
  │   ETL Domain    │    │  Waves Adapter  │    │ SQL-Dynamic /    │
  │   ───────────   │    │  ────────────   │    │ Exclusion        │
  │                 │    │                 │    │ ─────────        │
  │ Element         │    │ dataclass → dict│    │                  │
  │   ↓ map         │    │ (preserves old  │    │ Use IssueRecord  │
  │ Component       │    │  return types)  │    │ and TopLevel     │
  │   + issues[]    │    │                 │    │ CodeUnit directly │
  │   + sql_tasks   │    │ ▼               │    │                  │
  │                 │    │ analyze_deps.py │    │ Feed into domain │
  │ PackageAnalysis │    │ (untouched      │    │ analysis logic   │
  │ DataFlow        │    │  algorithms)    │    │ (untouched)      │
  └─────────────────┘    └─────────────────┘    └──────────────────┘
```

---

## Adapter Pattern in Waves Generator

The waves generator was the largest consumer. Its internal callers expect `dict[str, dict]`, not dataclasses. The adapter layer in `load_data_html_report.py` bridges this:

```
    Shared Library                    Adapter (load_data_html_report.py)           Consumers
    ──────────────                    ──────────────────────────────────           ─────────

    load_code_units(csv)              load_toplevel_code_units(csv)
    → list[TopLevelCodeUnit]    ──►   → dict[code_unit_id, {                ──►  analyze_deps.py
                                          'category': ...,                       generate_html.py
                                          'ewi_count': ...,
                                        }]

    load_partition_membership(csv)    load_partition_membership(csv)
    → list[PartitionMember]     ──►   → dict[object_name, {                ──►  generate_html.py
                                          'partition': int,
                                          'is_root': bool,
                                        }]

    load_issues_estimation_json(json) load_issues_estimation(json)
    → (dict[str, Entry],        ──►   → (dict[str, {                       ──►  generate_html.py
       dict[str, Baseline])              'severity': ...,                        estimate_hours()
                                          'manual_effort': ...,
                                        }],
                                        dict[str, float])
```

---

## IssueEffortService: Two Initialization Paths

```
                    ┌─────────────────────────────────┐
                    │       IssueEffortService          │
                    │                                   │
                    │  .get_effort_hours(code) → float  │
                    │  .get_severity(code)     → str    │
                    │  .get_effort_and_severity(code)   │
                    │                                   │
                    │  EWI codes: minutes / 60 → hours  │
                    │  Other codes: effort as-is        │
                    │  Negative: clamp to 0.0           │
                    └──────────┬──────────┬─────────────┘
                               │          │
              ┌────────────────┘          └────────────────┐
              ▼                                            ▼
   .from_bundled_reference()                   .from_json_file(path)
   ┌────────────────────────┐                  ┌────────────────────────┐
   │ Loads issues_ref.json  │                  │ Loads runtime          │
   │ shipped with library   │                  │ IssuesEstimation.json  │
   │                        │                  │ from reports directory  │
   │ Used by:               │                  │                        │
   │   • ETL Assessment     │                  │ Used by:               │
   │     (no reports dir    │                  │   • Waves Generator    │
   │      at analysis time) │                  │     (has reports dir)  │
   └────────────────────────┘                  └────────────────────────┘
```

---

## Composition in ETL: Element → Component

ETL doesn't subclass `Element`. It composes a richer domain model:

```
    Shared: Element (frozen)              ETL: Component (mutable)
    ────────────────────────              ────────────────────────

    full_name          ─────────────►     full_name
    file_name          ─────────────►     file_name
    technology         ─────────────►     technology
    category           ─────────────►     category
    subtype            ─────────────►     subtype
    status             ─────────────►     status
    entry_kind         ─────────────►     entry_kind
    additional_info    ─────────────►     additional_info
                                          issues: list[Issue]        ← domain
                                          sql_task_details: dict     ← domain
                                          ewi_count (property)       ← derived
                                          unique_ewis (property)     ← derived
                                          to_dict()                  ← serialization
```

---

## What Lives Where

| Concern | Location | Rationale |
|---|---|---|
| CSV parsing, encoding | `snowconvert_reports/loaders/csv_reader.py` | Single implementation for all sub-skills |
| Report file discovery | `snowconvert_reports/services/report_finder.py` | Consistent glob patterns |
| Project facts (`project_name`) | `snowconvert_reports/loaders/project_config.py` | Reads the scai-owned `.scai/config/project.yml` for assessment-name fallback and metadata tooling |
| Report display name (`assessment.json`) | `snowconvert_reports/services/assessment_metadata.py` | Composes both sources behind `resolve_assessment_name()`, so the name offered at the `SKILL.md` prompt and the name rendered in the report cannot disagree. The only module here that **writes** |
| Data models (raw rows) | `snowconvert_reports/models/` | One frozen dataclass per CSV file type |
| Effort calculation | `snowconvert_reports/services/issue_effort_service.py` | Unified EWI/non-EWI logic |
| SSIS package analysis | `etl-assessment/` | Domain-specific (DTSX parsing, DAGs) |
| Wave generation algo | External — `scai assessment waves` | Owned by SCAI; emits `waves_analysis_*.json` that the HTML generators consume via `WavesJsonAdapter` |
| Dynamic SQL detection (occurrence extraction, tracking) | External — `scai assessment sql-dynamic` | Owned by SCAI; the sub-skill is a thin wrapper that drives the CLI and applies pattern classification |
| Object exclusion (naming patterns, duplicates, version conflicts) | External — `scai assessment object-exclusion` | Owned by SCAI; the sub-skill is a thin wrapper that consumes the resulting JSON |
| Data-migration readiness, DDL type scan, type coverage | `snowconvert_reports/{data_migration_readiness,data_types_scan,type_coverage}.py` | Reads the Code Unit Registry, not CSVs; no CLI command or artifact of its own |
| Testing readiness, dialect normalization | `snowconvert_reports/testing_readiness.py` | Same; `normalize_dialect` lives here and is imported by `data_migration_readiness.py` |
| Journey-tab copy and markup | `scripts/data_migration_report/`, `scripts/testing_report/` | `content.py` holds reviewable copy with no markup; `generate_*_content()` renders it |
| HTML report rendering | `scripts/generate_multi_report.py` | Presentation layer (Vue.js, Chart.js) |

---

## Test Coverage

```
tests/assessment/snowconvert_reports/
├── conftest.py                  # fixtures_dir, sys.path setup
├── fixtures/                    # Minimal CSV/JSON/TXT fixtures
│   ├── Elements.NA.csv
│   ├── Issues.NA.csv
│   ├── TopLevelCodeUnits.NA.csv
│   ├── ObjectReferences.NA.csv
│   ├── PartitionMembership.NA.csv
│   ├── IssuesEstimation.NA.json
│   ├── TopLevelObjectsEstimation.NA.csv
│   ├── graph_summary.txt
│   └── cycles.txt
├── test_models.py               # 19 tests — all dataclass parsing
├── test_loaders.py              # 29 tests — all loaders + csv_reader + project_config
└── test_services.py             # 21 tests — effort service, finder, assessment_metadata
                                   ──────
                                   69 tests total (0.14s)
```

The five readiness modules are tested outside this mirrored package, in
`tests/assessment/data_migration_readiness/` (readiness, DDL type scan, type-coverage drift) and
`tests/assessment/testing_readiness/`. That placement diverges from the
"test structure mirrors source" convention in `ai/CLAUDE.md` and is tracked for cleanup — look in
both places when changing a readiness module.
