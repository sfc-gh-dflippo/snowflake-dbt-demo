# dbt-quality

## Overview

The dbt-quality plugin detects anti-patterns in dbt projects that do not cause a build to fail. A
model that contains `TOP 10` fails the first time it is built against Snowflake. A model that
truncates its own table in a `pre_hook` builds successfully, but leaves the table empty if a run
fails partway through. This plugin addresses the second category of problem: conditions that pass
CI, return plausible results, and reduce correctness or increase cost without producing an error.

The plugin provides 87 rules in 10 rule packs, three execution modes, and an HTML assessment report.

Each finding includes a stable identifier (for example, `SSC-EWI-DBTINC0001`), a severity, an effort
estimate, and remediation guidance. Findings are phrased as questions to review rather than as
verdicts, because a rule can evaluate the code but not the intent behind it. A truncate-and-load
pattern is correct in some designs.

## Detected conditions

The following table lists representative conditions that the rules detect.

| Condition                                      | Impact                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `pre_hook` truncates the model's own relation  | dbt manages the lifecycle of that relation. A failed run leaves the table empty rather than stale.      |
| `incremental` with `merge` and no `unique_key` | Correct only for append-only loads. Otherwise, reprocessing duplicates rows instead of replacing them.  |
| The same derived subquery in two models        | The business rule is defined twice. In most cases, the logic belongs in an ephemeral model.             |
| An ephemeral model with multiple consumers     | The SQL is inlined into every consumer, so the work is repeated for each one.                           |
| `select *` applied directly to a `ref()`       | The output schema changes whenever the upstream schema changes.                                         |
| A literal `db.schema.table` reference          | dbt cannot detect the dependency, so lineage is incorrect and the relation does not resolve per target. |
| A remaining `!!!RESOLVE EWI!!!` marker         | A migration left a construct untranslated and the model was released in that state.                     |
| `profiles.yml` committed inside the project    | Credentials are stored in version control.                                                              |

## Prerequisites

Install [`uv`](https://docs.astral.sh/uv/) and confirm that it is available on your `PATH`. No other
dependencies are required. On each run, `uv` resolves the rule engine's dependencies into a
temporary environment.

## Installing the plugin

To install the plugin and verify the installation, run the following commands:

```bash
cortex plugin install /absolute/path/to/.claude/plugins/dbt-quality
cortex plugin list
```

The in-repository directory is the source copy. Hooks run only from the installed copy under
`~/.snowflake/cortex/plugins/`. After you edit the source, run `cortex plugin update dbt-quality` to
apply the changes.

The plugin supports both Cortex Code and Claude Code. The two hook manifests (`hooks/hooks.json` and
`hooks/hooks.claude.json`) differ only in tool naming and in the plugin-root variable.

## Execution modes

The following table summarizes the three hook-based and editor-based execution modes. Skills and the
command line interface are described in later sections.

|                     | Scope         | Trigger                         | Output                          |
| ------------------- | ------------- | ------------------------------- | ------------------------------- |
| **Validation hook** | One file      | Every write or edit operation   | Findings in the agent's context |
| **Audit hook**      | Whole project | After dbt rewrites the manifest | Summary in the agent's context  |
| **Editor tasks**    | Whole project | On demand                       | Problems panel                  |

### Validating a file on write

The validation hook runs on the `write`, `edit`, and `multi_edit` operations. It produces no output
unless there are findings to report, and it produces no output for files that are not dbt models,
including paths outside `models/`, files that are not SQL, and files that cannot be found.

> **Note**
>
> The validation hook never blocks a write operation, at any severity. A validation hook that
> interrupts a refactor is typically disabled, after which it provides no protection. Enforce errors
> in CI instead, by using `lint --strict`.

### Auditing a project after a dbt command

The audit hook runs only when both of the following conditions are met:

1. **dbt was invoked in a way that rewrites the manifest.** A Bash command directly runs the `dbt`
   executable with the `run`, `build`, `compile`, `parse`, `seed`, `snapshot`, `test`, or `docs`
   subcommand. The `dbt debug`, `dbt deps`, and `dbt --version` commands do not qualify, and neither
   do textual references to dbt. dbt Projects on Snowflake runs server-side and does not update a
   local manifest, so it does not trigger this audit.
2. **The manifest advanced.** The `target/manifest.json` file is newer than the stamp file under
   `~/.cache/dbt-quality/`. A failed run produces no new manifest, so no audit is performed.

The audit hook is always advisory and never returns a non-zero exit code, so it does not cause a
user's command to fail.

To force an audit on the next run, delete the stamp files:

```bash
rm -f ~/.cache/dbt-quality/*.stamp
```

### Running the editor tasks

Cortex Code Desktop is based on Visual Studio Code, so a `.vscode/tasks.json` entry with a
`problemMatcher` populates the Problems panel. This repository defines the following four tasks:

- `dbt: quality suggestions`
- `dbt: quality suggestions (errors only)`
- `dbt: quality suggestions (watch, every 5 min)`
- `dbt: quality report (JSON)`

These tasks evaluate the project at a point in time; they do not evaluate it as you type. The
five-minute watch task starts when the folder is opened. If the task was added during an existing
session, reload the window or run `dbt: quality suggestions (watch, every 5 min)` once to start it.
The validation hook covers individual files on write, and the editor tasks cover the whole project.

### Using the skills

The plugin provides the following skills:

| Skill                      | Scope                                                            |
| -------------------------- | ---------------------------------------------------------------- |
| `dbt-quality:dbt-audit`    | A project or an estate of projects; produces the HTML assessment |
| `dbt-quality:dbt-validate` | A single file                                                    |

Always specify the `dbt-quality:` prefix. The unqualified names conflict with other installed
skills.

### Using the command line interface

To run the rule engine directly, use the following commands:

```bash
cd .claude/plugins/dbt-quality/scripts

uv run audit.py manifest-status .          # Report which rules can currently be evaluated
uv run audit.py audit . --out out.json     # Run a full audit
uv run audit.py lint .                     # Print one line per finding, in compiler format
uv run audit.py rules                      # List the rule catalog
uv run validate.py path/to/model.sql       # Validate a single file
```

The audit does not run dbt, does not connect to a warehouse, and does not write any file inside the
project except the output file that you specify.

## Manifest requirements

Rules that depend on the dependency graph require `target/manifest.json`. These rules include
ephemeral fan-out, pass-through chains, layer crossing, and single-consumer models. If the manifest
is not available, these rules are reported as **skipped** rather than as passing, because "not
evaluated" and "evaluated and clean" are different results.

Observe the following requirements:

- If the manifest is stale, run `dbt parse` before you run an audit. The `manifest-status` command
  reports which rules cannot currently be evaluated.
- Newly added models are not visible to graph rules until the project is parsed again. A model that
  was just created is absent from the previous manifest, so it has no known consumers.

## Rule packs

The plugin organizes its rules into the following packs.

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

Tiers exist because migrated code requires different treatment from code that was written for dbt:

- **universal** — Always applies. A truncate-and-load pattern is incorrect regardless of how the
  code was produced.
- **architecture** — Encodes conventions for a project designed for dbt, such as medallion folders
  and clean layer lineage. These rules are suppressed when the project is detected as a mechanical
  conversion from Informatica or SSIS, because that layout was not chosen by the customer and
  reporting it obscures the significant findings. Suppressed findings are counted and summarized
  separately; they are not discarded.
- **migration** — Applies specifically because the code was converted, and covers unresolved
  `SSC-EWI` and `SSC-FDM` markers, ETL control columns, and released scaffolding. These rules are
  never suppressed.

Project provenance is inferred from corroborating signals and can be set explicitly in
configuration.

## Configuration

Configuration is optional. To override the defaults, add a `.dbt-quality.yml` file at the audit
root:

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

For the complete list of options, see [`scripts/README.md`](scripts/README.md).

## Excluded checks

The plugin intentionally omits the following categories of check:

- **Naming.** No rule evaluates model or column names. A migrated model often retains the name of
  its source object, and a dbt project does not record that name in any machine-readable form. The
  `/* Original Object: */` header is a comment and does not appear in `manifest.json`, so a naming
  rule could only guess. For the full rationale, see
  [`skills/dbt-audit/references/rule-catalog.md`](skills/dbt-audit/references/rule-catalog.md).
- **SQL dialect syntax.** No rule looks for constructs such as `TOP n`, `ISNULL`, or `ROWNUM`. dbt
  reports these constructs the first time the model is built. This engine targets conditions that
  produce no error.

## Troubleshooting

**A hook never runs.** Confirm that the plugin is installed, not only present in the repository, by
running `cortex plugin list`. Then confirm that `uv` is on the `PATH` that the hook inherits. The
hooks exit without output when `shutil.which("uv")` returns nothing.

**A hook runs but reports nothing for a file that contains a known issue.** In most cases, the file
is out of scope. The file must be located under a `models/` directory, must have a `.sql` or `.py`
extension, and must have a `dbt_project.yml` file in one of its parent directories. Run the command
line interface against the same path to view the complete output.

**The audit never runs after a dbt command.** Confirm that dbt rewrote `target/manifest.json`; a
failed run does not. Then delete the stamp files. Note that dbt Projects on Snowflake runs
server-side and does not update a local manifest, so no audit is expected in that case.

**The audit runs too often.** The audit hook is registered for Bash only. Its first condition
requires a shell command that directly invokes dbt with a manifest-producing subcommand, as
implemented in `hooks/audit_after_dbt.py`. References to dbt in command output, commit messages, or
`echo` commands do not qualify. The second condition requires a newer local manifest.

## Development

To run the test suite, use the following commands:

```bash
cd scripts
pytest tests/ -q
```

The suite functions primarily as a false-positive gate. Correct code that produces no findings is
more important than every anti-pattern being detected, because an audit that reports findings for
well-formed incremental models is typically disabled.

The `scripts/tests/fixtures/ewi_estate/` directory is a static four-project integration fixture. An
audit of this fixture must emit every active EWI rule. Update the estate and its README whenever an
EWI rule is added, removed, or materially changed. Unit fixtures continue to cover the
nearest-neighbor forms that must produce no findings.

> **Note**
>
> Running `pytest` creates `scripts/.venv`, whose Python symlink points outside the plugin
> directory. This causes `cortex plugin install` to reject the tree with the error
> `symlink escapes the allowed root`. Run `rm -rf scripts/.venv` before you reinstall the plugin.

## Additional documentation

| File                                                                                         | Contents                                               |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [`scripts/README.md`](scripts/README.md)                                                     | Engine internals, all configuration options, CLI flags |
| [`skills/dbt-audit/references/rule-catalog.md`](skills/dbt-audit/references/rule-catalog.md) | The rationale for each rule, and how to add one        |
| [`skills/dbt-audit/references/report-spec.md`](skills/dbt-audit/references/report-spec.md)   | HTML report structure                                  |
| [`skills/dbt-audit/SKILL.md`](skills/dbt-audit/SKILL.md)                                     | The project-wide audit workflow                        |
| [`skills/dbt-validate/SKILL.md`](skills/dbt-validate/SKILL.md)                               | Per-file validation and hook details                   |
