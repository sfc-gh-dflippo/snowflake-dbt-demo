# dbt-audit

Audits dbt projects for anti-patterns and emits findings as JSON, which the `dbt-audit` skill
renders into an HTML quality assessment.

## Running it

No install required — `uv` resolves the dependencies into a throwaway environment:

```bash
# What can be checked? (run this first)
uv run scripts/audit.py manifest-status /path/to/project

# Audit one project, or a directory containing many
uv run scripts/audit.py audit /path/to/project --out findings.json

# List the rule catalogue
uv run scripts/audit.py rules
```

Installed instead, if you prefer a stable entry point:

```bash
pip install -e .
dbt-audit audit /path/to/project
```

Useful options: `--category INC` to focus one pack, `--min-severity warning` to drop
recommendations, `--stdout` to pipe the JSON, `--fail-on-error` for CI.

The audit never runs dbt, never connects to a warehouse, and never writes inside the project under
audit except for the findings file you name.

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
- **architecture** — encodes a greenfield ideal (medallion folders, layer naming, layer-crossing
  lineage). Suppressed when the project is detected as mechanically converted from Informatica or
  SSIS, because that layout was never the customer's choice and reporting it buries the findings
  that matter. Suppressed findings are counted and summarised, not deleted, and they do not affect
  the score.
- **migration** — fires _because_ the project was converted: unresolved `SSC-EWI`/`SSC-FDM` markers,
  ETL control columns, shipped scaffolding. Never suppressed. Detecting that code was generated is
  not a quality endorsement of it.

Provenance is detected from weighted, corroborating signals (conversion markers, `Output/ETL/`
layout, `stg_raw__` naming, `etl_dml_operation__`, `.scai/` config) and can be overridden in
`.dbt-audit.yml`.

## Configuration

All optional. Place `.dbt-audit.yml` at the audit root:

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

naming:
  mode: auto # auto | medallion | retain-original | off

disabled_rules:
  - DOC005
```

`naming.mode` defaults to `auto` deliberately. This repo's guidance is self-contradictory —
`dbt-architecture` mandates `stg_`/`dim_`/`fct_` prefixes while `dbt-modeling`'s Name-Retention
Policy forbids them in favour of original source object names — so `auto` infers the project's own
dominant convention and flags deviation from that rather than imposing either standard.

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
off. Key guards include a textbook incremental model producing zero INC findings, `EXISTS`/`IN`
subqueries not counting as derived tables, and composite keys declared at model level counting as
tested.
