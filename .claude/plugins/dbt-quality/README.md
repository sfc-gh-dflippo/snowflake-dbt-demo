# dbt-quality

Finds problems in dbt projects that do not make a build fail.

A model containing `TOP 10` fails the first time it runs against Snowflake, and you find out
immediately. A model that truncates its own table in a `pre_hook` builds successfully — and leaves
the table empty if the run fails partway through. This plugin is for the second kind: conditions
that pass CI, return plausible results, and quietly reduce correctness or increase cost.

85 rules across 10 packs, three ways to run them, and an HTML assessment report.

Every finding carries a stable id (`SSC-EWI-DBTINC0001`), a level, a severity, an effort estimate,
and remediation guidance. Findings are phrased as observations rather than verdicts, because a rule
can read the code but not the intent behind it — a truncate-and-load is the right answer in some
designs.

## What it finds

| Condition                                       | Why it matters                                                                                                                                       |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pre_hook` truncates the model's own relation   | dbt manages that relation's lifecycle. A failed run leaves the table empty rather than stale.                                                        |
| `incremental` with `merge` and no `unique_key`  | Correct only for append-only loads. Otherwise reprocessing duplicates rows instead of replacing them.                                                |
| The same derived subquery in two models         | The business rule is defined twice. Usually it belongs in an ephemeral model.                                                                        |
| An ephemeral model with several consumers       | The SQL is inlined into each one, so the work is repeated per consumer.                                                                              |
| `select *` straight off a `ref()`               | The output schema changes whenever the upstream schema does.                                                                                         |
| A literal `db.schema.table` reference           | dbt cannot see the dependency, so lineage is wrong and the relation does not resolve per target.                                                     |
| A remaining `!!!RESOLVE EWI!!!` marker          | A migration left a construct untranslated and the model shipped in that state.                                                                       |
| `profiles.yml` present in the project directory | Risks committing credentials to version control and pins developers to one account; whether it holds a literal secret is a separate check (OPS0002). |

## Install

Install [`uv`](https://docs.astral.sh/uv/) and make sure it is on your `PATH`. Nothing else is
needed — `uv` resolves the engine's dependencies on each run.

```bash
cortex plugin install /absolute/path/to/.claude/plugins/dbt-quality
cortex plugin list
```

The in-repository directory is the source copy; hooks run only from the installed copy under
`~/.snowflake/cortex/plugins/`. After editing the source, run `cortex plugin update dbt-quality`.

The plugin works in both Cortex Code and Claude Code.

One rule (`profiles.yml` placement, `SSC-EWI-DBTPRJ0004`) consults git to tell a tracked file from
an ignored one. If the `git` binary is absent or the tree is not a repository, that rule falls back
to reporting presence only; nothing else depends on git.

## How to run it

| Surface             | Scope         | When it runs                     | Where results appear       |
| ------------------- | ------------- | -------------------------------- | -------------------------- |
| **Validation hook** | One file      | Every write or edit              | In the agent's context     |
| **Audit hook**      | Whole project | After dbt rewrites the manifest  | In the agent's context     |
| **Editor tasks**    | Whole project | On demand, or every five minutes | Problems panel             |
| **Skills**          | Either        | When you ask                     | Chat, plus the HTML report |
| **CLI**             | Either        | When you run it                  | Terminal, or a JSON file   |

Nothing here ever blocks a save or fails your command — at any severity. A validation hook that
interrupts a refactor gets switched off, after which it protects nothing. To enforce a gate, use
`lint --strict` in CI, which exits non-zero on any error-level finding.

### Hooks

Both hooks activate once the plugin is installed and need no configuration.

The **validation hook** checks the file you just wrote and stays silent unless it has something to
say, including for anything that is not a dbt model.

The **audit hook** runs the whole-project audit after a dbt command that rewrote
`target/manifest.json`. `dbt debug`, `dbt deps`, and a failed run do not trigger it, and neither
does dbt Projects on Snowflake, which runs server-side and leaves no local manifest. To force an
audit on the next run:

```bash
rm -f ~/.cache/dbt-quality/*.stamp
```

### Editor tasks (Cortex Code Desktop and VS Code)

Tasks are written into `.vscode/tasks.json` for you the first time you open a session inside a dbt
project. Run them from the Command Palette with **Tasks: Run Task**:

- `dbt: quality suggestions` — everything, in the Problems panel
- `dbt: quality suggestions (errors only)` — just the findings that permit no exception

A watch task refreshes the panel every five minutes and starts when the folder opens. If it was
added during the current session, reload the window or run it once by hand to start it now.

These tasks evaluate the project at a point in time; they are not live as you type. The validation
hook covers files as you write them, and the tasks cover the whole project.

The linter prints one line per finding:

```text
models/gold/fact_order_line.sql:5:1:5:38: warning: [SSC-EWI-DBTINC0002] `pre_hook` deletes rows from this model's relation outside dbt's transaction and DAG. -> Express the deletion through the materialization instead.
```

### Skills

| Skill                      | Scope                                                            |
| -------------------------- | ---------------------------------------------------------------- |
| `dbt-quality:dbt-audit`    | A project or an estate of projects; produces the HTML assessment |
| `dbt-quality:dbt-validate` | A single file                                                    |

Always use the `dbt-quality:` prefix — the bare names collide with other installed skills.

### Command line

```bash
cd .claude/plugins/dbt-quality/scripts

uv run audit.py manifest-status .          # which rules can be evaluated right now
uv run audit.py audit . --out out.json     # full audit
uv run audit.py lint .                     # one line per finding, compiler format
uv run audit.py rules                      # the rule catalogue
uv run validate.py path/to/model.sql       # a single file
```

The audit never runs dbt, never connects to a warehouse, and writes no file inside your project
except the output file you name.

## Silencing a finding

When you have reviewed a finding and it does not apply, waive it. A waived finding is dropped from
every surface: the report, the Problems panel, and all counts.

**One line** — attach the directive to the line the diagnostic reports:

```sql
select id from analytics.public.orders  -- dbt-quality: ignore SSC-EWI-DBTSQL0006
```

**One file** — anywhere in the file, and independent of any line:

```sql
-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002, SSC-EWI-DBTDOC0003
```

**A set of paths** — in `.dbt-quality.yml`. This is the only form that can waive findings about a
project or an estate, which have no single line to annotate:

```yaml
ignore:
  - paths: ["models/legacy/**"]
    rules: [SSC-EWI-DBTARC0001]
  - paths: ["vendor/**"]
    rules: ["*"]
```

Worth knowing:

- Use `*` for the rule list to waive every rule.
- A directive on its own line also covers the next line that has content, so a blank line between it
  and the statement is fine.
- The reported line is not always the line you would blame: for materialization, incremental, and
  operational rules it is the `{{ config() }}` block. Take the line from the reported position, or
  use `ignore-file`.
- A directive naming no rules waives nothing, so a half-typed one cannot silence more than you
  meant.
- Waivers leave no audit trail. Nothing reports a waiver whose finding has since been fixed — review
  them with `grep -rn "dbt-quality: ignore"`.

To turn a rule off entirely instead, use `disabled_rules` (below). That is reported as _skipped_, so
the report still records that the check did not run.

## Configuration

Optional. Add `.dbt-quality.yml` at your repository root:

```yaml
thresholds:
  micro_project_threshold: 5
  ephemeral_fanout_threshold: 3
  column_doc_coverage: 0.8

migration:
  mode: auto # auto | native | lift_and_shift

disabled_rules:
  - SSC-EWI-DBTDOC0002
```

The file is found by searching upward from wherever the audit starts, so one at the repository root
governs the audit, the linter, and the save-time hook alike. Full option list:
[`scripts/README.md`](scripts/README.md).

## Rule packs

| Pack | Concern                                          | Tier         |
| ---- | ------------------------------------------------ | ------------ |
| PRJ  | Project structure and fragmentation              | universal    |
| INC  | Load patterns and incremental correctness        | universal    |
| SQL  | Query construction: subquery, CTE, and ephemeral | universal    |
| MAC  | Macro over-use and under-use                     | universal    |
| MAT  | Materialization fitness                          | mixed        |
| TST  | Testing and constraint coverage                  | universal    |
| DOC  | Documentation coverage                           | universal    |
| ARC  | Architecture and lineage conventions             | architecture |
| MIG  | Unresolved conversion debt                       | migration    |
| OPS  | Operational hygiene                              | universal    |

Migrated code needs different treatment from code written for dbt, which is what the tiers encode:

- **universal** — always applies. A truncate-and-load is wrong however the code came to exist.
- **architecture** — conventions for a project designed for dbt, such as medallion folders and clean
  layer lineage. Suppressed when the project is detected as a mechanical conversion from Informatica
  or SSIS, because nobody chose that layout and reporting it buries the findings that matter.
  Suppressed findings are counted and summarised separately, not discarded.
- **migration** — applies precisely because the code was converted: unresolved `SSC-EWI`/`SSC-FDM`
  markers, ETL control columns, shipped scaffolding. Never suppressed.

Provenance is inferred from corroborating signals, and can be set explicitly with `migration.mode`.

## Rules that need a manifest

Rules that reason about the dependency graph — ephemeral fan-out, layer crossing, single-consumer
models — need `target/manifest.json`. Without it they are reported as **skipped**, never as passing,
because "not checked" and "checked and clean" are different claims.

Run `dbt parse` first if the manifest is missing or stale; `manifest-status` tells you which rules
are currently unavailable. A model you just added is invisible to these rules until the project is
parsed again.

## What it deliberately does not check

- **Names.** No rule evaluates model or column names. A migrated model often keeps the name of its
  source object, and a dbt project records that name nowhere a tool can read — the
  `/* Original Object: */` header is a comment and never reaches `manifest.json`, so a naming rule
  could only guess.
- **SQL dialect syntax.** Nothing looks for `TOP n`, `ISNULL`, or `ROWNUM`. dbt reports those the
  first time the model builds. This engine earns its keep on silent problems.

## Troubleshooting

**A hook never runs.** Check the plugin is installed, not just present in the repository
(`cortex plugin list`), then check `uv` is on the `PATH` the hook inherits — hooks exit silently
when `uv` cannot be found.

**A hook runs but says nothing about a file you know has a problem.** Almost always scope: the file
must be under a `models/` directory, be `.sql` or `.py`, and have a `dbt_project.yml` somewhere
above it. Run the CLI on the same path to see the full output.

**A finding you expected is missing.** Check for a waiver — `grep -rn "dbt-quality: ignore"` and the
`ignore:` block of the nearest `.dbt-quality.yml`, which may be in a parent directory.

**The audit never runs after a dbt command.** Confirm dbt actually rewrote `target/manifest.json`; a
failed run does not. Then delete the stamp files. dbt Projects on Snowflake never triggers it.

**The Problems panel is empty, or its entries point at paths that do not exist.** Run
`dbt: quality suggestions` and read the task terminal. If the linter printed findings but no
diagnostics appeared, the `problemMatcher` in `.vscode/tasks.json` no longer matches the linter's
output format — see [`skills/dbt-validate/SKILL.md`](skills/dbt-validate/SKILL.md).

## Development

```bash
cd scripts
pytest tests/ -q
```

The suite is primarily a false-positive gate: correct code producing no findings matters more than
every anti-pattern being caught, because an audit that flags well-formed models gets switched off.
`scripts/tests/fixtures/ewi_estate/` is a static four-project fixture whose audit must emit every
active EWI rule — update it whenever a rule is added, removed, or materially changed.

Running `pytest` creates `scripts/.venv`, whose Python symlink points outside the plugin directory
and makes `cortex plugin install` reject the tree. Run `rm -rf scripts/.venv` before reinstalling.

Engine internals, every configuration option, and the full waiver semantics are in
[`scripts/README.md`](scripts/README.md).

## More documentation

| File                                                                                         | Contents                                               |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [`scripts/README.md`](scripts/README.md)                                                     | Engine internals, all configuration options, CLI flags |
| [`skills/dbt-audit/references/rule-catalog.md`](skills/dbt-audit/references/rule-catalog.md) | The rationale for each rule, and how to add one        |
| [`skills/dbt-audit/references/report-spec.md`](skills/dbt-audit/references/report-spec.md)   | HTML report structure                                  |
| [`skills/dbt-audit/SKILL.md`](skills/dbt-audit/SKILL.md)                                     | The project-wide audit workflow                        |
| [`skills/dbt-validate/SKILL.md`](skills/dbt-validate/SKILL.md)                               | Per-file validation, hooks, and editor integration     |
