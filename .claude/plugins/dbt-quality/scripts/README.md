# dbt-audit

Audits dbt projects for anti-patterns and emits suggestions as JSON, which the `dbt-audit` skill
renders into an HTML quality assessment.

## Running it

No install required — `uv` resolves the dependencies into a throwaway environment:

```bash
# What can be checked? (run this first)
uv run scripts/audit.py manifest-status /path/to/project

# Audit one project, or a directory containing many
uv run scripts/audit.py audit /path/to/project --out suggestions.json

# Lint: one line per suggestion, compiler-style
uv run scripts/audit.py lint /path/to/project

# List the rule catalogue
uv run scripts/audit.py rules
```

Installed instead, if you prefer a stable entry point:

```bash
pip install -e .
dbt-audit audit /path/to/project
dbt-audit lint /path/to/project
```

Useful options for `audit`: `--category INC` to focus one pack, `--min-level`
`error|warning|information` to raise the floor, `--stdout` to pipe the JSON, `--fail-on-error` for
CI.

Useful options for `lint`: `--format text|json`, `--min-level` `error|warning|information`,
`--strict` (exits non-zero when any _error_-level suggestion is emitted; default is always 0 so a
lint task doesn't train people to ignore it).

The audit never runs dbt, never connects to a warehouse, and never writes inside the project under
audit except for the suggestions file you name.

## Rule packs

| Pack | Concern                                          | Tier         |
| ---- | ------------------------------------------------ | ------------ |
| PRJ  | Project structure and fragmentation              | universal    |
| INC  | Load patterns and incremental correctness        | universal    |
| SQL  | Query construction: subquery vs CTE vs ephemeral | universal    |
| MAC  | Macro over-use and under-use                     | universal    |
| MAT  | Materialization fitness                          | mixed        |
| TST  | Testing and constraint coverage                  | universal    |
| DOC  | Documentation coverage                           | universal    |
| ARC  | Architecture and lineage conventions             | architecture |
| MIG  | Unresolved conversion debt                       | migration    |
| OPS  | Operational hygiene                              | universal    |

## Tiers, and why lift-and-shift is treated differently

- **universal** — always applies. A truncate-and-load is wrong however the code came to exist.
- **architecture** — encodes a greenfield ideal (medallion folders, layer-crossing lineage).
  Suppressed when the project is detected as mechanically converted from Informatica or SSIS,
  because that layout was never the customer's choice and reporting it buries the suggestions that
  matter. Suppressed suggestions are counted and summarised in a separate section, not deleted, and
  are not included in the suggestions total.
- **migration** — fires _because_ the project was converted: unresolved `SSC-EWI`/`SSC-FDM` markers,
  ETL control columns, shipped scaffolding. Never suppressed. Detecting that code was generated is
  not a quality endorsement of it.

Provenance is detected from weighted, corroborating signals (conversion markers, `Output/ETL/`
layout, `stg_raw__` naming, `etl_dml_operation__`, `.scai/` config) and can be overridden in
`.dbt-quality.yml`.

## Configuration

All optional. Place `.dbt-quality.yml` at the audit root:

```yaml
thresholds:
  micro_project_threshold: 5 # models at or below which a project is "micro"
  ephemeral_fanout_threshold: 3 # consumers at which ephemeral should become table
  passthrough_chain_threshold: 3 # chain length counting as model explosion
  column_doc_coverage: 0.8
  macro_model_ratio: 0.5
  duplicate_block_threshold: 3
  max_cluster_columns: 4

migration:
  mode: auto # auto | native | lift_and_shift
  paths:
    - models/legacy/** # force these paths to be treated as converted

disabled_rules:
  - SSC-EWI-DBTDOC0002
```

There is no naming option, because names are not audited. A model may keep the name its object had
in the source database, and a dbt project records nowhere that a tool can read what that name was —
so a naming rule would be guessing. The reasoning and evidence are in
`../skills/dbt-audit/references/rule-catalog.md`.

## Manifest

Graph-dependent rules (ephemeral fan-out, pass-through chains, layer crossing, single-consumer
models) need `target/manifest.json`. When it is missing they are reported as **skipped**, never as
passing: "we could not check" and "we checked and it was clean" are different statements to put in
front of a customer.

`manifest-status` reports what is unavailable and exits cleanly, so the skill can offer to run
`dbt parse` before auditing.

## Tests

```bash
uv run --with pyyaml --with typer --with rich python tests/test_rules.py   # standalone
pytest tests/ -q                                                          # or via pytest
```

The suite is mostly a false-positive gate. Correct code staying silent matters more than
anti-patterns being caught: an audit that flags every well-written incremental model gets switched
off. Key guards include a textbook incremental model producing zero INC suggestions, `EXISTS`/`IN`
subqueries not counting as derived tables, and composite keys declared at model level counting as
tested.
