# EWI Estate Test Fixtures

Static dbt project fixtures for testing every active EWI rule in the dbt-quality engine.

## Projects

| Project           | Purpose                                                | Key rules triggered                   |
| ----------------- | ------------------------------------------------------ | ------------------------------------- |
| `native_core`     | Well-structured native project (some intentional gaps) | DOC, TST, SQL, MAT, OPS rules         |
| `migrated_flow_a` | SnowConvert-migrated project with unresolved markers   | MIG001-008, PRJ005, PRJ007, ARC rules |
| `migrated_flow_b` | ETL-era load patterns, hook DML, bad orchestration     | INC001-013, MAC rules, PRJ006         |
| `migrated_flow_c` | Micro-project (2 models) for portfolio fragmentation   | PRJ001, PRJ002, PRJ003                |

## Rule coverage

### PRJ (project structure)

- PRJ001: `migrated_flow_c` has 2 models (micro-project)
- PRJ002: `migrated_flow_a` and `migrated_flow_c` share source `raw.customers`
- PRJ003: 3+ projects with diverging package versions
- PRJ004: `migrated_flow_b` has `profiles.yml` with credential
- PRJ005: `migrated_flow_a` has placeholder config values
- PRJ006: `migrated_flow_b/scripts/` has EXECUTE DBT PROJECT
- PRJ007: `migrated_flow_a` missing baseline packages
- PRJ008: `migrated_flow_b` has unignored `target/` dir

### INC (load patterns)

- INC001: `migrated_flow_b` model with pre-hook truncate
- INC002: `migrated_flow_b` model with pre-hook delete
- INC003: `migrated_flow_b` folder-level hook DML in dbt_project.yml
- INC004: `native_core` table model with hand-rolled date window
- INC005: `native_core` model named `*_full_reload`
- INC006: `native_core` incremental with no is_incremental() guard
- INC007: `native_core` incremental merge with no unique_key
- INC008: `native_core` incremental with no strategy stated
- INC009: `native_core` incremental guard without {{ this }}
- INC010: `migrated_flow_b` hook writes to another table
- INC011: `native_core` merge_exclude_columns referencing absent column
- INC012: `native_core` append strategy on mutable data
- INC013: `native_core` incremental watermark without absolute floor
- INC015: `migrated_flow_b` external loader task targeting a model

### SQL (query construction)

- SQL001: `native_core` derived-table subquery in FROM
- SQL003: `native_core` deeply nested subqueries
- SQL004: `native_core` window wrapper instead of QUALIFY
- SQL005: `native_core` SELECT \* outside staging
- SQL006: `native_core` hardcoded table reference
- SQL007: `native_core` implicit comma join
- SQL008: `native_core` non-deterministic ORDER BY (SELECT null)
- SQL009: `native_core` generic CTE name
- SQL010: `native_core` unused CTE
- SQL011: `native_core` no CTE structure
- SQL012: `native_core` UNION without ALL
- SQL013: `native_core` SELECT DISTINCT

### MAC (macros)

- MAC001: `migrated_flow_b` high macro:model ratio
- MAC002: `migrated_flow_b` macro with single caller
- MAC003: `migrated_flow_b` unused macro
- MAC004: `migrated_flow_b` trivial wrapper macro
- MAC005: `migrated_flow_b` macro emitting full query
- MAC006: `migrated_flow_b` macro with hardcoded relation
- MAC008: `migrated_flow_b` model body mostly Jinja
- MAC009: `native_core` hashed FK field
- MAC011: `native_core` macro defined in models dir

### MAT (materialization)

- MAT004: `native_core` clustering key over-specified
- MAT007: `native_core` layer folder without materialization default

### TST (testing)

- TST001: `migrated_flow_a` project with no tests
- TST002: `native_core` model with no key test
- TST003: `native_core` dim\_ model without dbt_constraints PK
- TST004: `native_core` fact\_ model without FK tests
- TST005: `native_core` unique+not_null instead of dbt_constraints
- TST006: test coverage below threshold
- TST007: `native_core` singular test that should be generic
- TST008: store_failures not enabled
- TST009: `native_core` snapshot with incomplete config
- TST010: `native_core` model without schema entry
- TST012: `native_core` key column untested

### DOC (documentation)

- DOC001: `native_core` model missing description
- DOC002: `native_core` column doc below threshold
- DOC003: `native_core` source missing description
- DOC004: `native_core` no persist_docs

### ARC (architecture)

- ARC001: `native_core` model outside recognised layer
- ARC003: `native_core` source() used in silver model
- ARC004: `native_core` duplicate staging models for same source
- ARC005: `native_core` backward layer dependency (requires manifest)
- ARC006: `native_core` staging model with join/aggregation
- ARC007: `native_core` nested folder repeats parent tags

### MIG (migration debt)

- MIG001: `migrated_flow_a` !!!RESOLVE EWI!!! marker
- MIG002: `migrated_flow_a` SSC-EWI-\* marker in model
- MIG003: `migrated_flow_a` SSC-FDM-\* marker in model
- MIG004: `migrated_flow_a` NEEDS-USER marker
- MIG005: `migrated_flow_a` etl_dml_operation\_\_ control column
- MIG006: `migrated_flow_a` stabilization_test scaffolding
- MIG007: `migrated_flow_a` ETL instance names (SQ*, EXP*)
- MIG008: `migrated_flow_a` placeholder model (WHERE FALSE)

### OPS (operational)

- OPS001: `native_core` dbt_artifacts hook wired but disabled
- OPS002: `migrated_flow_b` literal credential in profiles.yml
- OPS004: `native_core` automation script with dbt run + dbt test
