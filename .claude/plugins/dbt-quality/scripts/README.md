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

All optional. Place `.dbt-quality.yml` at the audit root, or anywhere above it — the loader walks up
from the audit root and takes the first file it finds, stopping at a directory containing `.git` or
after eight levels. The upward search is what keeps a single repo-root config authoritative for
`dbt-audit`, `dbt-lint`, and the save-time `dbt-validate` hook alike; the hook builds its portfolio
from the enclosing dbt project, so a config read only at the audit root would apply to some surfaces
and not others.

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
  - SSC-EWI-DBTDOC0002 # off everywhere, reported as skipped

ignore: # waived at these paths, dropped from the output
  - paths: ["models/legacy/**"]
    rules: [SSC-EWI-DBTARC0001, SSC-EWI-DBTDOC0002]
  - paths: ["vendor/**"]
    rules: ["*"]
```

There is no naming option, because names are not audited. A model may keep the name its object had
in the source database, and a dbt project records nowhere that a tool can read what that name was —
so a naming rule would be guessing. The reasoning and evidence are in
`../skills/dbt-audit/references/rule-catalog.md`.

## Waivers

Three ways to silence a specific finding, all equivalent in effect: the suggestion is dropped, so it
does not reach the report, the Problems panel, or any count.

| Surface          | Scope       | Written as                                       |
| ---------------- | ----------- | ------------------------------------------------ |
| Inline directive | One line    | `-- dbt-quality: ignore SSC-EWI-DBTINC0008`      |
| File directive   | One file    | `-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002` |
| `ignore:` config | A path glob | see above                                        |

Details that decide whether a waiver takes effect:

- **An inline directive attaches to the line the diagnostic reports.** For `MAT`, `INC` and `OPS`
  rules that line is the `{{ config() }}` block rather than the SQL a reader might consider at fault
  — `resolve_position` in `core/anchors.py` anchors by category. Take the line from the reported
  position, or use `ignore-file`, which does not depend on a line.
- **A directive on its own line also covers the next line that carries anything**, so a blank line
  between the directive and its statement is fine. A _trailing_ directive — one with code before it
  on the same line — covers its own line only, deliberately: extending it forward would silence a
  finding on the following statement that nobody reviewed.
- **`*` in place of a rule list means every rule**, in a directive or a config entry.
- **A rule list may be comma- or space-separated**, and is matched case-insensitively. Trailing
  prose is ignored, so `-- dbt-quality: ignore SSC-EWI-DBTINC0008 (append-only feed)` works.
- **A directive naming no rules waives nothing.** A truncated `-- dbt-quality: ignore` is not read
  as a wildcard, because widening a half-written directive would hide findings nobody named.
- **Config globs use `fnmatch` semantics**, in which `*` crosses `/`. This matches
  `migration.paths`. Paths may be written project-relative or audit-root-relative; both forms are
  matched.
- **Only the config surface can waive project- and portfolio-scoped findings.** Those often name a
  directory or a pseudo-path (`models/`, `<portfolio>`) with nowhere to put a comment.

Waivers are distinct from `disabled_rules`, which turns a rule off for the whole run and reports it
as _skipped_ so the report still states what was not checked. A waiver is narrower and stronger: the
reader has settled this finding, in this place, and it is removed rather than reported.

Two consequences worth knowing:

- **A waiver leaves no audit trail.** A directive written for code that has since been fixed is not
  reported as stale, and nothing counts what has been silenced. Grep for `dbt-quality: ignore` to
  review them.
- **Waiver text is excluded from marker scanning.** A rule id here is spelled exactly like a
  SnowConvert marker, so `waivers.blank_directives` removes directives before the MIG pack and
  `provenance.py` scan for conversion markers. Without it, writing a waiver would both raise a new
  `SSC-EWI-DBTMIG0002` error and count as evidence of mechanical conversion — which suppresses the
  whole ARCHITECTURE tier.

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
