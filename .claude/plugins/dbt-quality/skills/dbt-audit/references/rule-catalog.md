# Rule Catalog

Every rule, the practice it protects, and the signal that detects it. Load this when a user asks why
a rule fired, disputes a suggestion, or you are adding a rule.

Run `uv run audit.py rules` for the live catalogue with tiers and levels — that is generated from
the registry and cannot drift.

## Tiers

| Tier           | Behaviour                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `universal`    | Always applies. Correctness, load mechanics, testing, fragmentation.                                                                      |
| `architecture` | Greenfield ideals. **Suppressed** for detected lift-and-shift migrations; counted and reported separately as a modernisation opportunity. |
| `migration`    | Fires _because_ code was converted. Never suppressed.                                                                                     |

## Silencing a rule

Three mechanisms, in increasing narrowness. Reach for the narrowest that fits, and prefer a waiver
over disabling a rule when the finding is a defensible trade-off rather than a bad rule.

| Mechanism                           | Scope                    | Effect on the report                                                   |
| ----------------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| `disabled_rules:`                   | The rule, the whole run  | Reported as **skipped**, so the report still says what was not checked |
| `ignore:` config entry              | The rule, at a path glob | Dropped — absent from every output and every count                     |
| `-- dbt-quality: ignore-file <ids>` | The rule, one file       | Dropped                                                                |
| `-- dbt-quality: ignore <ids>`      | The rule, one line       | Dropped                                                                |

When explaining why a rule fired and the reader disagrees, offer a waiver at the narrowest scope
that covers their case rather than `disabled_rules`. An inline directive attaches to **the line the
diagnostic reports**, which for `MAT`/`INC`/`OPS` rules is the `{{ config() }}` block; `ignore-file`
avoids the question. Only the config surface can waive project- and portfolio-scoped findings, whose
`file` is often a directory or `<portfolio>`. Full semantics:
[`../../../scripts/README.md`](../../../scripts/README.md).

When a rule is _not_ firing where you expect one, check for a waiver before suspecting the rule —
`grep -rn "dbt-quality: ignore"` plus the `ignore:` block of the nearest `.dbt-quality.yml`, which
may sit in a parent directory of the audit root.

## Codes, kind, level and severity

Every rule carries a code of the form `SSC-{KIND}-DBT{CAT}{NNNN}`. `SSC` is SnowConvert's own
prefix; `DBT` reserves a namespace inside it for this engine, distinct from the codes SnowConvert
itself emits during a conversion (e.g. `SSC-EWI-SSIS0033`). A reader cannot tell from the shared
`SSC` prefix alone which tool produced a given code — only the `DBT` segment identifies this engine.

Three orthogonal axes classify each rule:

| Kind  | Meaning                                                                          |
| ----- | -------------------------------------------------------------------------------- |
| `EWI` | Issue — something is wrong or worth attention                                    |
| `FDM` | Functional difference — the model's results differ from what the source produced |
| `PRF` | Performance / cost                                                               |

| Level         | Meaning                                                                                                                |
| ------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `error`       | Confidence it is actually wrong; the message is direct and factual                                                     |
| `warning`     | Confidence it is wrong in nearly all cases                                                                             |
| `information` | Context-dependent (the default); the message states a check plus the condition under which the code is already correct |

| Severity   | Meaning                                                               |
| ---------- | --------------------------------------------------------------------- |
| `critical` | Secret exposure, data loss, or a model that silently produces nothing |
| `high`     | Wrong results                                                         |
| `medium`   | Avoidable cost or maintainability                                     |
| `low`      | Style                                                                 |

`level` and `severity` are deliberately independent. A rule can be `information` (only the reader
can tell if it applies) and yet `critical` (if it does apply, data is lost).

---

## PRJ — Project structure and fragmentation `universal`

Portfolio-scoped; requires tree mode (point the audit at a parent directory).

| Rule               | Kind | Level       | Severity | Suggestion                              | Signal                                                                                                                   |
| ------------------ | ---- | ----------- | -------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| SSC-EWI-DBTPRJ0001 | EWI  | information | low      | Project has very few models             | Model count <= `micro_project_threshold` (5). Requires 2+ projects — one small project is a new repo, not fragmentation  |
| SSC-EWI-DBTPRJ0002 | EWI  | information | medium   | Multiple projects read the same sources | Same `source()` pair referenced from 2+ projects                                                                         |
| SSC-EWI-DBTPRJ0003 | EWI  | information | low      | Config duplicated across siblings       | 3+ projects, with package version drift called out                                                                       |
| SSC-EWI-DBTPRJ0004 | EWI  | warning     | medium   | `profiles.yml` present in project tree  | File at project root. `information` when git-ignored; `warning` when tracked/untracked/unknown. Content is OPS0002's job |
| SSC-EWI-DBTPRJ0005 | EWI  | warning     | high     | Converter placeholders unresolved       | `YOUR_PROJECT_NAME`, `YOUR_DB` etc. in config                                                                            |
| SSC-EWI-DBTPRJ0006 | EWI  | information | medium   | Projects chained by Snowflake Tasks     | 2+ `EXECUTE DBT PROJECT` in orchestration SQL                                                                            |
| SSC-EWI-DBTPRJ0007 | EWI  | information | low      | Baseline packages absent                | `dbt_utils` / `dbt_constraints` missing from `packages.yml`                                                              |
| SSC-EWI-DBTPRJ0008 | EWI  | information | low      | Build artifacts unignored               | `target/`, `logs/`, `dbt_packages/` present without a `.gitignore` entry                                                 |

PRJ001, PRJ002 and PRJ006 together describe the per-data-flow conversion shape: one project per ETL
data flow, stitched by a Task graph. It forfeits cross-project lineage, a single `dbt build`,
project-wide tests, and one set of docs. It is the highest-value structural suggestion this audit
produces.

---

## INC — Load patterns and incremental correctness `universal`

| Rule               | Kind | Level       | Severity | Suggestion                       | Signal                                                                                                                                       |
| ------------------ | ---- | ----------- | -------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTINC0001 | EWI  | warning     | critical | Truncate-and-load                | `TRUNCATE`/`DROP` in a hook targeting `{{ this }}` or the model's own relation                                                               |
| SSC-EWI-DBTINC0002 | EWI  | warning     | high     | Delete-and-load                  | `DELETE FROM {{ this }}` in a hook; notes when the hook also `ref()`s a sibling                                                              |
| SSC-EWI-DBTINC0003 | EWI  | warning     | high     | Folder hook runs DML             | `+pre-hook`/`+post-hook` in `dbt_project.yml` containing TRUNCATE/DELETE/INSERT — fires once per model, so the second model undoes the first |
| SSC-PRF-DBTINC0004 | PRF  | information | medium   | Manual incremental               | `materialized='table'` + relative date predicate + no `is_incremental()`                                                                     |
| SSC-PRF-DBTINC0005 | PRF  | information | medium   | Full-reload naming or config     | `*_full_reload` / `*_full_refresh` name, or `full_refresh: true`                                                                             |
| SSC-PRF-DBTINC0006 | PRF  | information | medium   | No `is_incremental()` guard      | Incremental materialization without the call; Snowflake streams and microbatch models exempt                                                 |
| SSC-FDM-DBTINC0007 | FDM  | information | high     | No `unique_key`                  | Incremental with `merge` or `delete+insert` and no key                                                                                       |
| SSC-EWI-DBTINC0008 | EWI  | information | low      | Strategy not declared            | No `incremental_strategy`, or an unrecognised value                                                                                          |
| SSC-PRF-DBTINC0009 | PRF  | information | medium   | No watermark                     | `is_incremental()` block never references `{{ this }}`; Snowflake streams and microbatch models exempt                                       |
| SSC-EWI-DBTINC0010 | EWI  | information | medium   | Hook writes elsewhere            | `INSERT`/`MERGE` in a hook targeting another relation                                                                                        |
| SSC-FDM-DBTINC0011 | FDM  | information | high     | `merge_exclude_columns` mismatch | Excluded column never selected by the model                                                                                                  |
| SSC-FDM-DBTINC0012 | FDM  | information | high     | `append` on mutable data         | `append` strategy alongside `updated_at` / `status` / `valid_to`                                                                             |
| SSC-PRF-DBTINC0013 | PRF  | information | medium   | Unbounded watermark scan         | `max()` watermark with no absolute date floor; Snowflake streams and microbatch models exempt                                                |
| SSC-EWI-DBTINC0015 | EWI  | information | medium   | Loaded outside dbt               | A task or procedure inserting into a dbt-managed relation                                                                                    |

**False-positive guard:** the sanctioned watermark `(select max(c) from {{ this }})` is exempt from
every subquery check. Without that exemption every correct incremental model would be flagged.

---

## SQL — Query construction `universal`

| Rule               | Kind | Level       | Severity | Suggestion                                  | Signal                                                                                                                                                                                                                          |
| ------------------ | ---- | ----------- | -------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTSQL0001 | EWI  | information | low      | Subquery should be a CTE or ephemeral model | Parenthesised SELECT in FROM/JOIN position. **Reuse decides the advice**: normalised body fingerprinted across all models — appears once, recommend a CTE; appears in 2+, recommend an ephemeral model and name the other sites |
| SSC-EWI-DBTSQL0002 | EWI  | information | low      | Identical CTE across models                 | Same normalised CTE body in 2+ models                                                                                                                                                                                           |
| SSC-EWI-DBTSQL0003 | EWI  | information | low      | Deep nesting                                | 2+ nested SELECT levels in one derived table                                                                                                                                                                                    |
| SSC-EWI-DBTSQL0004 | EWI  | information | low      | Window filtered by wrapper                  | Window function in a subquery, filtered by the enclosing WHERE, no `QUALIFY` present                                                                                                                                            |
| SSC-EWI-DBTSQL0005 | EWI  | information | medium   | `SELECT *` outside staging                  | `select *` reading directly from a `ref()`/`source()`; staging exempt                                                                                                                                                           |
| SSC-EWI-DBTSQL0006 | EWI  | information | high     | Hardcoded table reference                   | `FROM`/`JOIN` a dotted literal not wrapped in `{{ }}`; local CTEs and Snowflake system schemas excluded                                                                                                                         |
| SSC-EWI-DBTSQL0007 | EWI  | information | medium   | Implicit comma join                         | Comma-separated FROM list                                                                                                                                                                                                       |
| SSC-FDM-DBTSQL0008 | FDM  | warning     | high     | Non-deterministic dedup                     | `ORDER BY (SELECT null)` or `ORDER BY 1` inside a window function                                                                                                                                                               |
| SSC-EWI-DBTSQL0009 | EWI  | information | low      | Uninformative CTE name                      | Matches `cte1`, `tmp`, `t`, `q2`, etc.                                                                                                                                                                                          |
| SSC-EWI-DBTSQL0010 | EWI  | information | low      | Unused CTE                                  | Defined, never referenced outside its own body (recursive self-reference excluded)                                                                                                                                              |
| SSC-EWI-DBTSQL0011 | EWI  | information | low      | No CTE structure                            | Join, aggregate, window or set op with no named CTE. Skips staging, ephemeral and placeholder models                                                                                                                            |
| SSC-EWI-DBTSQL0012 | EWI  | information | low      | UNION removes duplicates                    | `UNION` not followed by `ALL`; verify distinct combined rows are required because duplicate elimination adds database work                                                                                                      |
| SSC-EWI-DBTSQL0013 | EWI  | information | low      | SELECT DISTINCT may hide a grain issue      | Every `SELECT DISTINCT`; investigate duplicate origin and use deterministic `QUALIFY` only when selecting one row per business key                                                                                              |

SQL001 is the flagship rule and the one users ask about most. The reuse test is the whole point:
promoting single-use logic to a model adds a DAG node for no benefit, while leaving duplicated logic
inline guarantees it drifts.

**Guards:** comments, string literals and `{% %}` blocks stripped before matching; `EXISTS`/`IN`
predicates and scalar subqueries in a SELECT list are never treated as derived tables; a minimum
normalised length of 60 characters suppresses trivial inline tables. UNION and DISTINCT checks run
on the same stripped SQL, so comments and string literals do not trigger them.

---

## MAC — Macro discipline `universal`

Over-use and under-use are both failures with opposite remedies, so both are measured. No existing
skill in this repo carries prescriptive macro guidance, so these thresholds were authored for the
audit and are all configurable.

| Rule               | Kind | Level       | Severity | Suggestion                                              | Signal                                                                                                                                      |
| ------------------ | ---- | ----------- | -------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTMAC0001 | EWI  | information | low      | High macro-to-model ratio                               | Macros / models >= `macro_model_ratio` (0.5)                                                                                                |
| SSC-EWI-DBTMAC0002 | EWI  | information | low      | Single call site                                        | Exactly one external caller; macros with real branching and >10 lines exempt                                                                |
| SSC-EWI-DBTMAC0003 | EWI  | information | low      | Never called                                            | No call sites; dbt hook and adapter-dispatch names (`snowflake__`, `generate_schema_name`, ...) exempt                                      |
| SSC-EWI-DBTMAC0004 | EWI  | information | low      | Trivial wrapper                                         | One short expression, no `if`/`for`/`set`/`do`                                                                                              |
| SSC-EWI-DBTMAC0005 | EWI  | information | medium   | Emits a whole query                                     | Body contains `SELECT ... FROM`; materialization and operational macros exempt                                                              |
| SSC-EWI-DBTMAC0006 | EWI  | warning     | high     | Hardcodes a relation                                    | Literal dotted relation in the body; `information_schema` exempt                                                                            |
| SSC-EWI-DBTMAC0007 | EWI  | information | medium   | Deep nesting                                            | Macro call chain 3+ levels deep                                                                                                             |
| SSC-EWI-DBTMAC0008 | EWI  | information | medium   | Model is mostly Jinja                                   | >50% Jinja lines and 2+ project macro calls; config block excluded from the count                                                           |
| SSC-EWI-DBTMAC0009 | EWI  | information | low      | Hashed foreign-key fields impair Snowflake join pruning | Snowflake `HASH`, `MD5`, `MD5_BINARY`, `SHA1`, `SHA1_BINARY`, `SHA2`, or `SHA2_BINARY` over FK-shaped fields; non-key hash-diffs are exempt |
| SSC-EWI-DBTMAC0010 | EWI  | information | low      | Missing abstraction (under-use)                         | Identical N-line window in `duplicate_block_threshold` (3) or more models                                                                   |
| SSC-EWI-DBTMAC0011 | EWI  | information | medium   | Macro defined in `models/`                              | `{% macro %}` inside a model file                                                                                                           |
| SSC-EWI-DBTMAC0012 | EWI  | information | low      | Filename mismatch                                       | Single-macro file whose stem differs from the macro name                                                                                    |

Call-site counting includes other macros, `dbt_project.yml` hooks and snapshots — without that, a
helper called only by another macro reads as dead.

---

## MAT — Materialization fitness `mixed`

| Rule               | Kind | Level       | Severity | Suggestion                    | Tier         | Signal                                                                                                                       |
| ------------------ | ---- | ----------- | -------- | ----------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| SSC-PRF-DBTMAT0001 | PRF  | information | medium   | Ephemeral/view fan-out        | universal    | `ephemeral`/`view` with >= `ephemeral_fanout_threshold` (3) model consumers — logic runs once per consumer. _Needs manifest_ |
| SSC-PRF-DBTMAT0002 | PRF  | information | low      | Single-consumer intermediate  | universal    | Silver model with one consumer and no tests or description. _Needs manifest_                                                 |
| SSC-PRF-DBTMAT0004 | PRF  | information | medium   | Over-specified clustering key | universal    | `cluster_by` with > 4 columns; inspect Snowflake catalog size and query filters before changing it                           |
| SSC-EWI-DBTMAT0006 | EWI  | information | low      | Redundant config              | architecture | Model `config()` restates the resolved folder default                                                                        |
| SSC-EWI-DBTMAT0007 | EWI  | information | low      | No folder default             | architecture | Layer folder with no `+materialized` in `dbt_project.yml`                                                                    |

---

## TST — Testing and constraints `universal`

| Rule               | Kind | Level       | Severity | Suggestion                                      | Signal                                                                                          |
| ------------------ | ---- | ----------- | -------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTTST0001 | EWI  | warning     | high     | No tests at all                                 | Models present, zero tests in YAML or `tests/`                                                  |
| SSC-EWI-DBTTST0002 | EWI  | information | medium   | No key test                                     | No PK/UK at column or model level; staging downgraded to `optional`                             |
| SSC-EWI-DBTTST0003 | EWI  | information | medium   | Dimension without `dbt_constraints.primary_key` | `dim_*`; distinguishes "has `unique`+`not_null`" from "has nothing"                             |
| SSC-EWI-DBTTST0004 | EWI  | information | medium   | Fact without FK tests                           | `fct_*`/`fact_*` with `_id` columns lacking FK or PK coverage                                   |
| SSC-EWI-DBTTST0005 | EWI  | information | low      | Built-in where constraints would enforce        | `unique`+`not_null`, or `relationships`                                                         |
| SSC-EWI-DBTTST0006 | EWI  | information | low      | Coverage below threshold                        | <60% of models have a key test; projects under 5 models exempt                                  |
| SSC-EWI-DBTTST0007 | EWI  | information | low      | Singular test that could be generic             | Single-table null/count assertion, no joins                                                     |
| SSC-EWI-DBTTST0008 | EWI  | information | low      | `store_failures` not enabled                    | Absent from `tests:` in `dbt_project.yml`                                                       |
| SSC-EWI-DBTTST0009 | EWI  | warning     | high     | Snapshot config incomplete                      | Missing `unique_key`/`strategy`; `timestamp` without `updated_at`; `check` without `check_cols` |
| SSC-EWI-DBTTST0010 | EWI  | warning     | medium   | Orphan model or schema entry                    | Model with no YAML entry, or YAML entry with no model (verify)                                  |
| SSC-EWI-DBTTST0012 | EWI  | information | medium   | Key column untested                             | Key-shaped column with no PK/UK/FK test; composite keys at model level count as tested          |

**Composite-key guards:** keys declared at model level via `column_name` / `column_names` /
`fk_column_name` / `fk_column_names` count as tested, and the dbt 1.10.5+ `arguments:` wrapper is
unwrapped. Both `tests:` and `data_tests:` are read. Omitting any of these produces large numbers of
false "untested" suggestions on correctly tested projects.

---

## DOC — Documentation `universal`

| Rule               | Kind | Level       | Severity | Suggestion                      | Signal                                                                           |
| ------------------ | ---- | ----------- | -------- | ------------------------------- | -------------------------------------------------------------------------------- |
| SSC-EWI-DBTDOC0001 | EWI  | information | low      | No model description            | Schema entry with empty `description`; gold escalated to `consider`              |
| SSC-EWI-DBTDOC0002 | EWI  | information | low      | Column coverage below threshold | <`column_doc_coverage` (0.8) of columns described; models with <3 columns exempt |
| SSC-EWI-DBTDOC0003 | EWI  | information | low      | Source undescribed              | Source or source table without `description`                                     |
| SSC-EWI-DBTDOC0004 | EWI  | information | low      | `persist_docs` not configured   | Descriptions exist but never reach Snowflake metadata                            |

### Exposures are not audited

DOC0005 (no `exposures:` declared) was **removed**, and the ID is retired rather than reused.

It was a project-scoped rule, so it fired once against every project with 10 or more models — and it
fired on projects that had made a deliberate choice not to use exposures at all. A suggestion that
cannot be satisfied except by adopting a feature the team has decided against is noise, not a
finding, and noise in a once-per-project slot is the most expensive kind.

Nothing replaces it. If impact analysis across BI assets matters on a given project, exposures are
worth adopting on their own merits, and the dbt docs cover them better than a linter message can.

---

## ARC — Architecture and lineage `architecture` (all suppressible)

| Rule               | Kind | Level       | Severity | Suggestion                 | Signal                                                     |
| ------------------ | ---- | ----------- | -------- | -------------------------- | ---------------------------------------------------------- |
| SSC-EWI-DBTARC0001 | EWI  | information | low      | Outside a layer folder     | No path segment matching a known layer alias               |
| SSC-EWI-DBTARC0003 | EWI  | information | medium   | `source()` outside staging | `source()` in a silver or gold model                       |
| SSC-EWI-DBTARC0004 | EWI  | information | medium   | Duplicate staging          | One source table staged by 2+ bronze models                |
| SSC-EWI-DBTARC0005 | EWI  | information | medium   | Layer-crossing dependency  | Parent in a later layer than the child. _Needs manifest_   |
| SSC-EWI-DBTARC0006 | EWI  | information | low      | Staging contains logic     | JOIN or aggregation in bronze                              |
| SSC-EWI-DBTARC0007 | EWI  | information | low      | Duplicate tags             | Nested `dbt_project.yml` key re-declaring an inherited tag |

### Names are not audited

There is no naming rule, in this pack or any other. ARC002 (layer prefix) and ARC008 (filename case)
were **removed**, and the IDs are retired rather than reused. No column-naming rule was ever added.

A model may keep the name its object had in the source database it was migrated from —
`dbt-modeling`'s Name-Retention Policy states this outright, and columns are looser again, since
case may legitimately change. Judging a name therefore requires knowing the original object name,
and a dbt project **does not record it anywhere a tool can read**:

- the prescribed `/* Original Object: ... */` header is a comment, so it never reaches
  `manifest.json`
- its identifier shape is platform-dependent and unlabelled (2-part `[owner].[object]` vs 3-part
  `[database].[schema].[object]`), so it cannot be parsed without already knowing the platform —
  which is only on the next line
- two competing header templates exist, and enforcement was warning-only
- `meta.original_object`, `source_object` and any crosswalk file do not exist
- the one real source-to-target mapping lives in SnowConvert's external `MIGRATION_REGISTRY`, which
  points into a project and writes nothing back

The corroboration is inside this tool: `provenance.py` must _infer_ `source_platform` heuristically
because nothing declares it.

A rule that cannot obtain the fact it needs is guessing. This one guessed badly — 18 findings on a
self-audit of this repo, most legal under the retention policy. Do not reintroduce it behind a
config flag: the problem is the missing fact, not the default. Revisit only if provenance becomes
declared.

---

## MIG — Conversion debt `migration` (never suppressed)

Fires only where provenance detected a migration.

| Rule               | Kind | Level       | Severity | Suggestion                   | Signal                                                                                         |
| ------------------ | ---- | ----------- | -------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTMIG0001 | EWI  | error       | critical | Unresolved conversion error  | `!!!RESOLVE EWI!!!` — invalid SQL, model cannot compile (verify)                               |
| SSC-EWI-DBTMIG0002 | EWI  | error       | high     | EWI marker left in place     | `SSC-EWI-*` code present; fidelity unconfirmed                                                 |
| SSC-FDM-DBTMIG0003 | FDM  | warning     | high     | FDM marker awaiting sign-off | `SSC-FDM-*` — a documented behavioural difference that compiles and runs, so it gets forgotten |
| SSC-EWI-DBTMIG0004 | EWI  | error       | high     | `NEEDS-USER` marker          | Explicit unactioned hand-off (verify)                                                          |
| SSC-FDM-DBTMIG0005 | FDM  | information | medium   | ETL control column           | `etl_dml_operation__` or `DD_*` constants — load behaviour encoded in row data                 |
| SSC-EWI-DBTMIG0006 | EWI  | warning     | medium   | Scaffolding shipped          | `stabilization_test` artifacts left in the project                                             |
| SSC-EWI-DBTMIG0007 | EWI  | information | low      | ETL-instance names           | `SQ_`/`EXP_`/`FIL_`/`LKP_`/`UPDTRANS` prefixes in model names                                  |
| SSC-EWI-DBTMIG0008 | EWI  | error       | critical | Conversion placeholder       | `-- Status: placeholder`, `where false`, or a `placeholder` tag; reports completion %          |

MIG003 usually pairs with SQL008 — the FDM markers most often document non-deterministic ordering,
and the placeholder `ORDER BY (SELECT null)` is the mechanism. Report them together.

---

## OPS — Operational hygiene `universal`

| Rule               | Kind | Level       | Severity | Suggestion                          | Signal                                                                                                            |
| ------------------ | ---- | ----------- | -------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| SSC-EWI-DBTOPS0001 | EWI  | warning     | medium   | Artifact logging wired but disabled | `dbt_artifacts` with an active `on-run-end` hook and `+enabled: false`, or installed with no hook at all          |
| SSC-EWI-DBTOPS0002 | EWI  | error       | critical | Literal credential                  | `password`/`token`/`secret` with a literal value in a tracked file (verify)                                       |
| SSC-EWI-DBTOPS0003 | EWI  | information | low      | Evaluator misconfigured             | `dbt_project_evaluator` without `primary_key_test_macros`, so it reports false key gaps against `dbt_constraints` |
| SSC-EWI-DBTOPS0004 | EWI  | information | medium   | `dbt run` + `dbt test`              | Both present in a script or workflow, instead of `dbt build`                                                      |

---

## Provenance signals

Weighted; threshold 4. Corroboration is required so one weak signal cannot silence the whole
architecture pack.

| Signal                                                             | Weight |
| ------------------------------------------------------------------ | ------ |
| `.scai/config/project.yml` present                                 | 4      |
| `SSC-EWI` / `SSC-FDM` / `!!!RESOLVE EWI!!!` / `NEEDS-USER` markers | 4      |
| `.dbt-quality.yml` `migration.paths` match                         | 4      |
| `Output/ETL/{Package}/{DataFlow}` layout                           | 3      |
| `etl_dml_operation__` or `DD_*` constants                          | 3      |
| `stg_raw__` prefix                                                 | 3      |
| Converter placeholders in `dbt_project.yml`                        | 3      |
| ETL instance names in model names                                  | 2      |

The marker signal is evaluated against text with dbt-quality waiver directives blanked out
(`waivers.blank_directives`). A waiver names a rule id spelled exactly like a conversion marker, so
without that step waivers accumulating in a hand-written project would push it over the threshold
and suppress its entire architecture pack -- caused by the reader trying to silence one finding.

Score >= 7 is `high` confidence and suppresses architecture suggestions project-wide; 4-6 is
`medium` and suppresses only the specific files carrying markers, so a hybrid repo with migrated
legacy code beside hand-written marts is scored correctly.

**Not carried over:** the `check_migration_header` rule from the retired dbt-validation package,
which tried to require an `Original Object` provenance header. It triggered on the bare substrings
`oracle`, `sql server` or `teradata` appearing anywhere in a file, then accepted any block comment
containing the word `Source` — matched with `.*?` under `re.DOTALL`, so it spanned the whole file.
It passed vacuously on ordinary models and carried no information. Its absence is also why names
cannot be audited: that header was the only place provenance was ever written down, and it was never
enforced.

---

## Adding a rule

### Level and message framing

`level` and message framing are coupled by an invariant: **`error` implies the message is direct and
factual; `information` implies it is conditional** — it states a check plus the condition under
which the current code is already correct. A future rule author must get this invariant right: an
`error` rule that hedges ("possibly an issue") contradicts the reader's expectation that it is
unconditionally wrong, and an `information` rule that asserts breakage overstates it.

An `information` message names the condition under which the code is already correct. Example:
"Verify `unique_key` is set — correct as-is if the load is append-only and duplicates are
acceptable."

The `error`-level rules detect something unconditionally wrong in dbt and use a direct message:
`SSC-EWI-DBTSQL0006` (literal table reference), `SSC-EWI-DBTMIG0001`/`SSC-EWI-DBTMIG0002`/
`SSC-EWI-DBTMIG0004`/`SSC-EWI-DBTMIG0008` (unresolved EWI / EWI marker / NEEDS-USER / placeholder),
and `SSC-EWI-DBTOPS0002` (literal credential). Direct messages are warranted only when there is no
context under which the pattern is correct. `SSC-EWI-DBTPRJ0004` is not among them: it reports the
_presence_ of `profiles.yml` in the project tree (a placement concern), at `warning` when the file
is untracked or its git status is unknown and `information` when it is git-ignored, and leaves
credential _content_ to `SSC-EWI-DBTOPS0002`.

### Steps

1. Pick the pack. Declare the ID as a module-local constant beside its siblings.
2. Decorate with `@rule(...)`, choosing `tier`, `scope`, `level`, `requires_manifest`, and a
   `rationale` — the rationale is required and appears in the report, so write it for a customer,
   not for yourself.
3. Yield `make_suggestion(...)` with `evidence` (what was observed), `remediation` (what to do, with
   a code example where it helps), and `line=` when the rule has a character offset. The anchor
   layer fills in the rest: the `{{ config() }}` block for config rules, the `- name: <model>` entry
   in schema YAML for test/doc rules, the first `select`/`with` otherwise, falling back to line 1.
   Pass `column=` only when you matched a real character offset — do not estimate it.
4. **Add both a positive and a negative test** in `tests/test_rules.py`. The negative — the correct
   form of the same pattern staying silent — matters more. An audit that flags well-written code
   gets switched off, and then none of the other rules matter either.

Scope determines the call signature: `MODEL` gets `(model, project)`, `PROJECT` gets `(project)`,
`PORTFOLIO` gets `(portfolio)`. Use `PROJECT` or `PORTFOLIO` whenever a rule needs to compare across
files — that is how SQL001 fingerprints subqueries across models to decide between a CTE and an
ephemeral model.
