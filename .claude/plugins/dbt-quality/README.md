# dbt-quality

Finds the dbt anti-patterns that don't announce themselves.

A model with `TOP 10` in it fails loudly the first time you build it against Snowflake. A model that
truncates its own table in a `pre_hook` works perfectly — until a run fails partway and leaves the
table empty. This plugin exists for the second kind of problem: things that pass CI, produce
plausible numbers, and cost you money or correctness quietly.

It ships 87 rules across 10 packs, three ways to run them, and an HTML report for when you need to
show someone else.

## What it catches

A sample, to give you the flavour:

| Situation                                     | Why it matters                                                                                             |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `pre_hook` truncates the model's own relation | dbt already owns that relation's lifecycle. A failed run leaves the table empty rather than stale.         |
| `incremental` + `merge` with no `unique_key`  | Correct only if the load is append-only. Otherwise reprocessing duplicates rows instead of replacing them. |
| The same derived subquery in two models       | Two copies of one business rule. Usually wants to be an ephemeral model.                                   |
| An ephemeral model with several consumers     | Its SQL is inlined into every consumer, so the work is repeated per consumer.                              |
| `select *` straight off a `ref()`             | The output schema silently changes whenever the upstream one does.                                         |
| A literal `db.schema.table` reference         | dbt can't see the dependency, so lineage is wrong and the relation doesn't resolve per target.             |
| A leftover `!!!RESOLVE EWI!!!` marker         | A migration left a construct untranslated and it shipped anyway.                                           |
| `profiles.yml` committed inside the project   | Credentials in version control.                                                                            |

Every finding gets a stable ID (`SSC-EWI-DBTINC0001`), a severity, an effort estimate, and
remediation text. Findings are phrased as questions to check rather than verdicts, because a rule
can see the code but not your intent — a truncate-and-load really is right sometimes.

## Install

Requires [`uv`](https://docs.astral.sh/uv/) on your `PATH`. Nothing else — `uv` resolves the
engine's dependencies into a throwaway environment on each run.

```bash
cortex plugin install /absolute/path/to/.claude/plugins/dbt-quality
cortex plugin list
```

The in-repo directory is the **source**. Hooks only run from the installed copy under
`~/.snowflake/cortex/plugins/`, so re-run `cortex plugin update dbt-quality` after editing the
source.

Works in both Cortex Code and Claude Code — the two hook manifests (`hooks/hooks.json`,
`hooks/hooks.claude.json`) differ only in tool naming and the plugin-root variable.

## Three ways to run it

|                   | Scope         | When it runs                    | Output                          |
| ----------------- | ------------- | ------------------------------- | ------------------------------- |
| **Validate hook** | one file      | on every write or edit          | findings in the agent's context |
| **Audit hook**    | whole project | after dbt rewrites the manifest | short summary as context        |
| **Editor tasks**  | whole project | on demand                       | Problems panel                  |

Plus the skills and the CLI, below.

### Validate on save

Fires on `write`, `edit` and `multi_edit`. Silent unless there's something to report, and silent for
anything that isn't a dbt model — non-`models/` paths, non-SQL files, missing files.

**It never blocks a save**, at any severity. A validation hook that fails mid-refactor gets switched
off, after which it protects nothing. Gate on errors in CI instead, with `lint --strict`.

### Audit after dbt

Two gates, both of which must pass:

1. **dbt was invoked in a way that rewrites the manifest** — a Bash command directly runs the `dbt`
   executable followed by `run`, `build`, `compile`, `parse`, `seed`, `snapshot`, `test` or `docs`.
   `dbt debug`, `dbt deps`, `dbt --version`, and textual mentions of dbt don't qualify. Server-side
   dbt Projects do not update a local manifest and therefore do not trigger this audit.
2. **the manifest actually advanced** — `target/manifest.json` is newer than a stamp under
   `~/.cache/dbt-quality/`. A failed run leaves no new manifest, so it stays quiet.

Always advisory; never returns non-zero. A report shouldn't fail somebody's command.

To force the next run: `rm -f ~/.cache/dbt-quality/*.stamp`.

### Editor tasks

Cortex Code Desktop is a VS Code fork, so `.vscode/tasks.json` plus a `problemMatcher` populates the
Problems panel. This repo defines four:

- `dbt: quality suggestions`
- `dbt: quality suggestions (errors only)`
- `dbt: quality suggestions (watch, every 5 min)`
- `dbt: quality report (JSON)`

These are point-in-time, not live-as-you-type. The five-minute watch task starts when the folder
opens; if it was added during an existing session, reload the window or run
`dbt: quality suggestions (watch, every 5 min)` once to start it. The validate hook covers per-file
on save; the tasks cover the whole project. Complementary, not redundant.

### Skills

```text
dbt-quality:dbt-audit      whole project or an estate, produces the HTML assessment
dbt-quality:dbt-validate   one file
```

Use the `dbt-quality:` prefix — the bare names collide with other installed skills.

### CLI

```bash
cd .claude/plugins/dbt-quality/scripts

uv run audit.py manifest-status .          # what can be checked right now?
uv run audit.py audit . --out out.json     # full audit
uv run audit.py lint .                     # one line per finding, compiler-style
uv run audit.py rules                      # the catalogue
uv run validate.py path/to/model.sql       # single file
```

The audit never runs dbt, never connects to a warehouse, and never writes inside the project except
the output file you name.

## The manifest matters

Rules that need the dependency graph — ephemeral fan-out, pass-through chains, layer crossing,
single-consumer models — require `target/manifest.json`. Without it they're reported as **skipped**,
never as passing. "We couldn't check" and "we checked and it's clean" are different statements.

Two consequences worth knowing:

- Run `dbt parse` before auditing if the manifest is stale. `manifest-status` tells you what's
  currently unavailable.
- **Newly added models are invisible to graph rules until you re-parse.** A model you just wrote
  isn't in the old manifest, so it has no known consumers.

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

The tiers exist because migrated code needs different treatment from greenfield code:

- **universal** — always applies. A truncate-and-load is wrong however the code came to exist.
- **architecture** — encodes a greenfield ideal (medallion folders, clean layer lineage). Suppressed
  when the project is detected as mechanically converted from Informatica or SSIS, because that
  layout was never the customer's choice and reporting it buries what matters. Suppressed findings
  are counted and summarised separately, not deleted.
- **migration** — fires _because_ the code was converted: unresolved `SSC-EWI`/`SSC-FDM` markers,
  ETL control columns, shipped scaffolding. Never suppressed.

Provenance is inferred from corroborating signals and can be forced in config.

## Configuration

Entirely optional. Drop `.dbt-quality.yml` at the audit root:

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

Full option list in [`scripts/README.md`](scripts/README.md).

## What it deliberately doesn't check

**Naming.** No rule checks model or column names. A migrated model often keeps the name its source
object had, and a dbt project records nowhere machine-readable what that name was — the
`/* Original Object: */` header is a comment that never reaches `manifest.json`. A naming rule would
be guessing. Reasoning in
[`skills/dbt-audit/references/rule-catalog.md`](skills/dbt-audit/references/rule-catalog.md).

**SQL dialect syntax.** No rule looks for `TOP n`, `ISNULL`, `ROWNUM`. dbt surfaces those itself the
first time the model builds. This engine earns its keep on silent problems.

## Troubleshooting

**Hook never fires.** Confirm the plugin is _installed_, not just present in the repo —
`cortex plugin list`. Then check `uv` is on the PATH the hook inherits; the hooks skip quietly when
`shutil.which("uv")` finds nothing.

**Hook fires but reports nothing on a file you know is bad.** Almost always scope: the file must be
under a `models/` directory, be `.sql` or `.py`, and have a findable `dbt_project.yml` above it. Run
the CLI on the same path to see the real output.

**Audit never fires after a dbt command.** Check that dbt actually rewrote `target/manifest.json` —
a failed run doesn't. Then clear the stamp. Note that dbt Projects on Snowflake runs server-side and
updates no local manifest, so it correctly stays quiet.

**Audit fires too often.** The hook is registered only for Bash. Its first gate in
`hooks/audit_after_dbt.py` requires a shell command that directly invokes dbt with a
manifest-producing subcommand; mentions in output, commit messages, or `echo` commands do not
qualify. The second gate requires a newer local manifest.

## Development

```bash
cd scripts
pytest tests/ -q
```

The suite is mostly a false-positive gate. Correct code staying silent matters more than
anti-patterns being caught: an audit that flags every well-written incremental model gets switched
off.

`scripts/tests/fixtures/ewi_estate/` is a static four-project integration fixture. Its audit must
emit every active EWI rule; update the estate and its README whenever an EWI rule is added, removed,
or materially changes. Unit fixtures still cover nearest-neighbor forms that must remain silent.

One trap: `pytest` creates `scripts/.venv`, whose Python symlink points outside the plugin directory
and makes `cortex plugin install` refuse the tree ("symlink escapes the allowed root"). Run
`rm -rf scripts/.venv` before reinstalling.

## Docs map

| File                                                                                         | Read it for                                     |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| [`scripts/README.md`](scripts/README.md)                                                     | Engine internals, all config options, CLI flags |
| [`skills/dbt-audit/references/rule-catalog.md`](skills/dbt-audit/references/rule-catalog.md) | Why a rule exists, or adding one                |
| [`skills/dbt-audit/references/report-spec.md`](skills/dbt-audit/references/report-spec.md)   | HTML report structure                           |
| [`skills/dbt-audit/SKILL.md`](skills/dbt-audit/SKILL.md)                                     | The project-wide audit workflow                 |
| [`skills/dbt-validate/SKILL.md`](skills/dbt-validate/SKILL.md)                               | Per-file validation, hook details               |
