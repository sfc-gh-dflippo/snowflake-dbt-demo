# Rule Catalogue

Every rule, the practice it protects, and the signal that detects it. Load this when a user asks why
a rule fired, disputes a finding, or you are adding a rule.

Run `uv run audit.py rules` for the live catalogue with tiers and severities — that is generated
from the registry and cannot drift.

## Tiers

| Tier           | Behaviour                                                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `universal`    | Always applies. Correctness, load mechanics, testing, fragmentation.                                                                |
| `architecture` | Greenfield ideals. **Suppressed** for detected lift-and-shift migrations; counted and reported separately, excluded from the score. |
| `migration`    | Fires _because_ code was converted. Never suppressed.                                                                               |

## Severity

| Severity         | Meaning                                                                               |
| ---------------- | ------------------------------------------------------------------------------------- |
| `error`          | Broken, wrong, or blocking — will fail, silently corrupt data, or prevent compilation |
| `warning`        | Correctness or maintainability risk                                                   |
| `recommendation` | Best-practice improvement                                                             |

Only `error` affects the process exit code (`--fail-on-error`).

---

## PRJ — Project structure and fragmentation `universal`

Portfolio-scoped; requires tree mode (point the audit at a parent directory).

| ID     | Finding                                 | Signal                                                                                                                  |
| ------ | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| PRJ001 | Project has very few models             | Model count <= `micro_project_threshold` (5). Requires 2+ projects — one small project is a new repo, not fragmentation |
| PRJ002 | Multiple projects read the same sources | Same `source()` pair referenced from 2+ projects                                                                        |
| PRJ003 | Config duplicated across siblings       | 3+ projects, with package version drift called out                                                                      |
| PRJ004 | `profiles.yml` committed                | File at project root; escalated to error when it contains a literal secret                                              |
| PRJ005 | Converter placeholders unresolved       | `YOUR_PROJECT_NAME`, `YOUR_DB` etc. in config                                                                           |
| PRJ006 | Projects chained by Snowflake Tasks     | 2+ `EXECUTE DBT PROJECT` in orchestration SQL                                                                           |
| PRJ007 | Baseline packages absent                | `dbt_utils` / `dbt_constraints` missing from `packages.yml`                                                             |
| PRJ008 | Build artifacts unignored               | `target/`, `logs/`, `dbt_packages/` present without a `.gitignore` entry                                                |

PRJ001, PRJ002 and PRJ006 together describe the per-data-flow conversion shape: one project per ETL
data flow, stitched by a Task graph. It forfeits cross-project lineage, a single `dbt build`,
project-wide tests, and one set of docs. It is the highest-value structural finding this audit
produces.

---

## INC — Load patterns and incremental correctness `universal`

| ID     | Finding                          | Signal                                                                                                                                       |
| ------ | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| INC001 | Truncate-and-load                | `TRUNCATE`/`DROP` in a hook targeting `{{ this }}` or the model's own relation                                                               |
| INC002 | Delete-and-load                  | `DELETE FROM {{ this }}` in a hook; notes when the hook also `ref()`s a sibling                                                              |
| INC003 | Folder hook runs DML             | `+pre-hook`/`+post-hook` in `dbt_project.yml` containing TRUNCATE/DELETE/INSERT — fires once per model, so the second model undoes the first |
| INC004 | Manual incremental               | `materialized='table'` + relative date predicate + no `is_incremental()`                                                                     |
| INC005 | Full-reload naming or config     | `*_full_reload` / `*_full_refresh` name, or `full_refresh: true`                                                                             |
| INC006 | No `is_incremental()` guard      | Incremental materialization without the call                                                                                                 |
| INC007 | No `unique_key`                  | Incremental with `merge` or `delete+insert` and no key                                                                                       |
| INC008 | Strategy not declared            | No `incremental_strategy`, or an unrecognised value                                                                                          |
| INC009 | No watermark                     | `is_incremental()` block never references `{{ this }}`                                                                                       |
| INC010 | Hook writes elsewhere            | `INSERT`/`MERGE` in a hook targeting another relation                                                                                        |
| INC011 | `merge_exclude_columns` mismatch | Excluded column never selected by the model                                                                                                  |
| INC012 | `append` on mutable data         | `append` strategy alongside `updated_at` / `status` / `valid_to`                                                                             |
| INC013 | Unbounded watermark scan         | `max()` watermark with no absolute date floor                                                                                                |
| INC015 | Loaded outside dbt               | A task or procedure inserting into a dbt-managed relation                                                                                    |

**False-positive guard:** the sanctioned watermark `(select max(c) from {{ this }})` is exempt from
every subquery check. Without that exemption every correct incremental model would be flagged.

---

## SQL — Query construction `universal`

| ID     | Finding                                     | Signal                                                                                                                                                                                                                          |
| ------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SQL001 | Subquery should be a CTE or ephemeral model | Parenthesised SELECT in FROM/JOIN position. **Reuse decides the advice**: normalised body fingerprinted across all models — appears once, recommend a CTE; appears in 2+, recommend an ephemeral model and name the other sites |
| SQL002 | Identical CTE across models                 | Same normalised CTE body in 2+ models                                                                                                                                                                                           |
| SQL003 | Deep nesting                                | 2+ nested SELECT levels in one derived table                                                                                                                                                                                    |
| SQL004 | Window filtered by wrapper                  | Window function in a subquery, filtered by the enclosing WHERE, no `QUALIFY` present                                                                                                                                            |
| SQL005 | `SELECT *` outside staging                  | `select *` reading directly from a `ref()`/`source()`; staging exempt                                                                                                                                                           |
| SQL006 | Hardcoded table reference                   | `FROM`/`JOIN` a dotted literal not wrapped in `{{ }}`; local CTE names excluded                                                                                                                                                 |
| SQL007 | Implicit comma join                         | Comma-separated FROM list                                                                                                                                                                                                       |
| SQL008 | Non-deterministic dedup                     | `ORDER BY (SELECT null)` or `ORDER BY 1` inside a window function                                                                                                                                                               |
| SQL009 | Uninformative CTE name                      | Matches `cte1`, `tmp`, `t`, `q2`, etc.                                                                                                                                                                                          |
| SQL010 | Unused CTE                                  | Defined, never referenced outside its own body (recursive self-reference excluded)                                                                                                                                              |

SQL001 is the flagship rule and the one users ask about most. The reuse test is the whole point:
promoting single-use logic to a model adds a DAG node for no benefit, while leaving duplicated logic
inline guarantees it drifts.

**Guards:** comments, string literals and `{% %}` blocks stripped before matching; `EXISTS`/`IN`
predicates and scalar subqueries in a SELECT list are never treated as derived tables; a minimum
normalised length of 60 characters suppresses trivial inline tables.

---

## MAC — Macro discipline `universal`

Over-use and under-use are both failures with opposite remedies, so both are measured. No existing
skill in this repo carries prescriptive macro guidance, so these thresholds were authored for the
audit and are all configurable.

| ID     | Finding                         | Signal                                                                                                 |
| ------ | ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| MAC001 | High macro-to-model ratio       | Macros / models >= `macro_model_ratio` (0.5)                                                           |
| MAC002 | Single call site                | Exactly one external caller; macros with real branching and >10 lines exempt                           |
| MAC003 | Never called                    | No call sites; dbt hook and adapter-dispatch names (`snowflake__`, `generate_schema_name`, ...) exempt |
| MAC004 | Trivial wrapper                 | One short expression, no `if`/`for`/`set`/`do`                                                         |
| MAC005 | Emits a whole query             | Body contains `SELECT ... FROM`; materialization and operational macros exempt                         |
| MAC006 | Hardcodes a relation            | Literal dotted relation in the body; `information_schema` exempt                                       |
| MAC007 | Deep nesting                    | Macro call chain 3+ levels deep                                                                        |
| MAC008 | Model is mostly Jinja           | >50% Jinja lines and 2+ project macro calls; config block excluded from the count                      |
| MAC009 | Reimplements `dbt_utils`        | Hand-rolled surrogate key, date spine, row generator, pivot                                            |
| MAC010 | Missing abstraction (under-use) | Identical N-line window in `duplicate_block_threshold` (3) or more models                              |
| MAC011 | Macro defined in `models/`      | `{% macro %}` inside a model file                                                                      |
| MAC012 | Filename mismatch               | Single-macro file whose stem differs from the macro name                                               |

Call-site counting includes other macros, `dbt_project.yml` hooks and snapshots — without that, a
helper called only by another macro reads as dead.

---

## MAT — Materialization fitness `mixed`

| ID     | Finding                      | Tier         | Signal                                                                                                                       |
| ------ | ---------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| MAT001 | Ephemeral/view fan-out       | universal    | `ephemeral`/`view` with >= `ephemeral_fanout_threshold` (3) model consumers — logic runs once per consumer. _Needs manifest_ |
| MAT002 | Single-consumer intermediate | universal    | Silver model with one consumer and no tests or description. _Needs manifest_                                                 |
| MAT003 | Pass-through chain           | universal    | 3+ consecutive single-child, single-parent models. The per-transformation conversion signature. _Needs manifest_             |
| MAT004 | Clustering                   | universal    | Fact/incremental table with no `cluster_by`, or `cluster_by` with > 4 columns                                                |
| MAT005 | Complex view                 | universal    | `view` with 3+ CTEs or 60+ lines and 2+ consumers. _Needs manifest_                                                          |
| MAT006 | Redundant config             | architecture | Model `config()` restates the resolved folder default                                                                        |
| MAT007 | No folder default            | architecture | Layer folder with no `+materialized` in `dbt_project.yml`                                                                    |
| MAT008 | Python model issue           | universal    | Imports without `packages=`, or no analytical library present                                                                |

---

## TST — Testing and constraints `universal`

| ID     | Finding                                         | Signal                                                                                          |
| ------ | ----------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| TST001 | No tests at all                                 | Models present, zero tests in YAML or `tests/`                                                  |
| TST002 | No key test                                     | No PK/UK at column or model level; staging downgraded to recommendation                         |
| TST003 | Dimension without `dbt_constraints.primary_key` | `dim_*`; distinguishes "has `unique`+`not_null`" from "has nothing"                             |
| TST004 | Fact without FK tests                           | `fct_*`/`fact_*` with `_id` columns lacking FK or PK coverage                                   |
| TST005 | Built-in where constraints would enforce        | `unique`+`not_null`, or `relationships`                                                         |
| TST006 | Coverage below threshold                        | <60% of models have a key test; projects under 5 models exempt                                  |
| TST007 | Singular test that could be generic             | Single-table null/count assertion, no joins                                                     |
| TST008 | `store_failures` not enabled                    | Absent from `tests:` in `dbt_project.yml`                                                       |
| TST009 | Snapshot config incomplete                      | Missing `unique_key`/`strategy`; `timestamp` without `updated_at`; `check` without `check_cols` |
| TST010 | Orphan model or schema entry                    | Model with no YAML entry, or YAML entry with no model (error)                                   |

**Guards mirrored from `dbt_validation.yaml.validator`:** composite keys declared at model level via
`column_name` / `column_names` / `fk_column_name` / `fk_column_names` count as tested, and the dbt
1.10.5+ `arguments:` wrapper is unwrapped. Both `tests:` and `data_tests:` are read. Omitting any of
these produces large numbers of false "untested" findings on correctly tested projects.

---

## DOC — Documentation `universal`

| ID     | Finding                         | Signal                                                                           |
| ------ | ------------------------------- | -------------------------------------------------------------------------------- |
| DOC001 | No model description            | Schema entry with empty `description`; gold escalated to warning                 |
| DOC002 | Column coverage below threshold | <`column_doc_coverage` (0.8) of columns described; models with <3 columns exempt |
| DOC003 | Source undescribed              | Source or source table without `description`                                     |
| DOC004 | `persist_docs` not configured   | Descriptions exist but never reach Snowflake metadata                            |
| DOC005 | No exposures                    | 10+ models and no `exposures:` anywhere                                          |

---

## ARC — Architecture and lineage `architecture` (all suppressible)

| ID     | Finding                    | Signal                                                     |
| ------ | -------------------------- | ---------------------------------------------------------- |
| ARC001 | Outside a layer folder     | No path segment matching a known layer alias               |
| ARC002 | Naming convention          | Layer prefix mismatch, **mode-dependent** — see below      |
| ARC003 | `source()` outside staging | `source()` in a silver or gold model                       |
| ARC004 | Duplicate staging          | One source table staged by 2+ bronze models                |
| ARC005 | Layer-crossing dependency  | Parent in a later layer than the child. _Needs manifest_   |
| ARC006 | Staging contains logic     | JOIN, aggregation, or 2+ upstream references in bronze     |
| ARC007 | Duplicate tags             | Nested `dbt_project.yml` key re-declaring an inherited tag |
| ARC008 | Filename not snake_case    | Uppercase, or `__` outside the `stg_`/`int_` convention    |

**ARC002 and the naming contradiction.** `dbt-architecture` mandates `stg_`/`int_`/`dim_`/`fct_`
prefixes; `dbt-modeling`'s Name-Retention Policy explicitly forbids them in favour of original
source object names. The two cannot both be enforced. `naming.mode` therefore defaults to `auto`,
which infers the project's own dominant convention (>=60% prefixed means medallion, <=20% means
retain-original) and enforces only that. Where there is no clear majority, ARC002 stays silent
rather than guessing. Override with `medallion`, `retain-original`, or `off`.

---

## MIG — Conversion debt `migration` (never suppressed)

Fires only where provenance detected a migration.

| ID     | Finding                      | Signal                                                                                         |
| ------ | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| MIG001 | Unresolved conversion error  | `!!!RESOLVE EWI!!!` — invalid SQL, model cannot compile (error)                                |
| MIG002 | EWI marker left in place     | `SSC-EWI-*` code present; fidelity unconfirmed                                                 |
| MIG003 | FDM marker awaiting sign-off | `SSC-FDM-*` — a documented behavioural difference that compiles and runs, so it gets forgotten |
| MIG004 | `NEEDS-USER` marker          | Explicit unactioned hand-off (error)                                                           |
| MIG005 | ETL control column           | `etl_dml_operation__` or `DD_*` constants — load behaviour encoded in row data                 |
| MIG006 | Scaffolding shipped          | `stabilization_test` artifacts left in the project                                             |
| MIG007 | ETL-instance names           | `SQ_`/`EXP_`/`FIL_`/`LKP_`/`UPDTRANS` prefixes in model names                                  |

MIG003 usually pairs with SQL008 — the FDM markers most often document non-deterministic ordering,
and the placeholder `ORDER BY (SELECT null)` is the mechanism. Report them together.

---

## OPS — Operational hygiene `universal`

| ID     | Finding                             | Signal                                                                                                            |
| ------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| OPS001 | Artifact logging wired but disabled | `dbt_artifacts` with an active `on-run-end` hook and `+enabled: false`, or installed with no hook at all          |
| OPS002 | Literal credential                  | `password`/`token`/`secret` with a literal value in a tracked file (error)                                        |
| OPS003 | Evaluator misconfigured             | `dbt_project_evaluator` without `primary_key_test_macros`, so it reports false key gaps against `dbt_constraints` |
| OPS004 | `dbt run` + `dbt test`              | Both present in a script or workflow, instead of `dbt build`                                                      |

---

## Provenance signals

Weighted; threshold 4. Corroboration is required so one weak signal cannot silence the whole
architecture pack.

| Signal                                                             | Weight |
| ------------------------------------------------------------------ | ------ |
| `.scai/config/project.yml` present                                 | 4      |
| `SSC-EWI` / `SSC-FDM` / `!!!RESOLVE EWI!!!` / `NEEDS-USER` markers | 4      |
| `.dbt-audit.yml` `migration.paths` match                           | 4      |
| `Output/ETL/{Package}/{DataFlow}` layout                           | 3      |
| `etl_dml_operation__` or `DD_*` constants                          | 3      |
| `stg_raw__` prefix                                                 | 3      |
| Converter placeholders in `dbt_project.yml`                        | 3      |
| ETL instance names in model names                                  | 2      |

Score >= 7 is `high` confidence and suppresses architecture findings project-wide; 4-6 is `medium`
and suppresses only the specific files carrying markers, so a hybrid repo with migrated legacy code
beside hand-written marts is scored correctly.

**Not reused:** the existing `SQL005` `check_migration_header` in `.claude/hooks/dbt-validation`. It
triggers on the bare substrings `oracle`, `sql server` or `teradata` appearing anywhere in a file,
then accepts any block comment containing the word `Source` — matched with `.*?` under `re.DOTALL`,
so it spans the whole file. It passes vacuously on ordinary models and carries no information.

---

## Adding a rule

1. Pick the pack. Declare the ID as a module-local constant beside its siblings.
2. Decorate with `@rule(...)`, choosing `tier`, `scope`, `severity`, `requires_manifest`, and a
   `rationale` — the rationale is required and appears in the report, so write it for a customer,
   not for yourself.
3. Yield `make_finding(...)` with `evidence` (what was observed) and `remediation` (what to do, with
   a code example where it helps).
4. **Add both a positive and a negative test** in `tests/test_rules.py`. The negative — the correct
   form of the same pattern staying silent — matters more. An audit that flags well-written code
   gets switched off, and then none of the other rules matter either.

Scope determines the call signature: `MODEL` gets `(model, project)`, `PROJECT` gets `(project)`,
`PORTFOLIO` gets `(portfolio)`. Use `PROJECT` or `PORTFOLIO` whenever a rule needs to compare across
files — that is how SQL001 fingerprints subqueries across models to decide between a CTE and an
ephemeral model.
