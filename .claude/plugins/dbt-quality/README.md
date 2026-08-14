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

|                     | Scope         | Trigger                          | Output                          |
| ------------------- | ------------- | -------------------------------- | ------------------------------- |
| **Validation hook** | One file      | Every write or edit operation    | Findings in the agent's context |
| **Audit hook**      | Whole project | After dbt rewrites the manifest  | Summary in the agent's context  |
| **Editor tasks**    | Whole project | On demand, or every five minutes | Problems panel                  |

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

### Integrating with Cortex Code Desktop and Visual Studio Code

Cortex Code Desktop is based on Visual Studio Code, so a task in `.vscode/tasks.json` with a
`problemMatcher` is the supported way to populate the Problems panel. The linter emits one line per
suggestion in the conventional compiler format, and the matcher parses each line into a diagnostic
that is attached to the correct file, line, and column range. The integration is identical in Cortex
Code Desktop and in Visual Studio Code, because both read the same task definition.

SARIF is not supported in Cortex Code Desktop, because the SARIF viewer is not present in the
application bundle. The SQLFluff extension is blocked by the default-deny extension allowlist.
Therefore the task and `problemMatcher` mechanism is the only route from an external linter to the
Problems panel.

#### Bootstrapping the tasks

A `SessionStart` hook, `hooks/setup_vscode_task.py`, writes the task definitions into the project so
that no manual setup is required. Its behavior is deliberately conservative:

- It takes no action unless the session's working directory is inside a dbt project, which it
  determines by looking for `dbt_project.yml` in the working directory and up to eight parent
  directories.
- It creates `.vscode/tasks.json` if the file does not exist.
- If the file exists, it adds only the missing dbt-quality tasks. Existing tasks are never modified,
  even if they were edited by hand or point to a different script path.
- If the file exists but is not valid JSON, for example because it contains JSONC comments, the hook
  takes no action rather than overwrite a file that it cannot round-trip safely.
- It uses only the Python standard library, because `hooks.json` invokes it with the bare `python3`
  interpreter.

The hook creates the following two tasks, which are the minimum required for Problems panel
integration:

- `dbt: quality suggestions`
- `dbt: quality suggestions (watch, every 5 min)`

The `.vscode/tasks.json` file committed in this repository defines two additional tasks. All four
are described in the following table.

| Task                                            | Command                                   | Purpose                                                                   |
| ----------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------- |
| `dbt: quality suggestions`                      | `lint.py .`                               | Reports all suggestions for the workspace in the Problems panel           |
| `dbt: quality suggestions (errors only)`        | `lint.py . --min-level error`             | Reports only the suggestions that permit no legitimate exception          |
| `dbt: quality suggestions (watch, every 5 min)` | `lint.py .` in a loop, with `sleep 300`   | Refreshes the Problems panel every five minutes while the task is running |
| `dbt: quality report (JSON)`                    | `audit.py audit . --out suggestions.json` | Writes the full report, including code examples, to `suggestions.json`    |

The JSON report task declares an empty `problemMatcher`, because it produces a file rather than
diagnostics.

#### Running the tasks

To run a task, open the Command Palette, select **Tasks: Run Task**, and select the task by name.
All tasks run with `cwd` set to `${workspaceFolder}` and use the `silent` reveal setting, so they do
not steal focus from the editor.

The watch task sets `runOn: folderOpen`, so it starts automatically when the folder is opened, and
`isBackground: true`, so the editor does not treat it as a task that terminates. Its `background`
matcher settings use the `>>> dbt-quality lint start` and `>>> dbt-quality lint done` markers that
the task echoes around each run, which is how the editor knows when to clear and repopulate
diagnostics.

> **Note**
>
> The watch task starts only when a folder is opened. If the task was added to `tasks.json` during
> the current session, reload the window or run `dbt: quality suggestions (watch, every 5 min)` once
> to start it in the current session.

#### Diagnostic format

The linter writes one line per suggestion in the following format:

```text
path:line:col:endLine:endCol: level: [RULE-ID] message -> remediation
```

For example:

```text
models/gold/fact_order_line.sql:5:1:5:38: warning: [SSC-EWI-DBTINC0002] `pre_hook` deletes rows from this model's relation outside dbt's transaction and DAG. -> Express the deletion through the materialization instead.
```

The `problemMatcher` maps these fields to the Problems panel as follows.

| Linter field        | `problemMatcher` capture group | Problems panel column |
| ------------------- | ------------------------------ | --------------------- |
| `path`              | 1 (`file`)                     | File                  |
| `line`, `col`       | 2, 3 (`line`, `column`)        | Position              |
| `endLine`, `endCol` | 4, 5 (`endLine`, `endColumn`)  | Underline range       |
| `level`             | 6 (`severity`)                 | Severity icon         |
| `RULE-ID`           | 7 (`code`)                     | Code                  |
| `message`           | 8 (`message`)                  | Message               |

The matcher declares `owner` and `source` as `dbt-quality`, so its diagnostics are attributed to the
plugin and are cleared as a group on each run, and it sets `fileLocation` to
`["relative", "${workspaceFolder}"]`, so the reported paths resolve against the workspace root.

The `level` field maps directly to the three severities that Visual Studio Code recognizes: `error`,
`warning`, and `info`. The `information` level used elsewhere in this plugin is emitted as `info` by
the linter for this reason.

> **Note**
>
> The end position fields are required. A `problemMatcher` that captures only `line` and `column`
> does not fail cleanly against this format: because the `file` group is non-greedy, the pattern
> backtracks and captures `path:line:col` as the file name, which does not resolve to a file on
> disk. If the Problems panel is empty or its entries reference paths that do not exist, compare the
> `pattern` block in `.vscode/tasks.json` against the format above.

These tasks evaluate the project at a point in time; they do not evaluate it as you type. The
validation hook covers individual files as they are written, and the editor tasks cover the whole
project. The two surfaces are complementary.

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

**The Problems panel is empty, or its entries reference paths that do not exist.** Run the
`dbt: quality suggestions` task and check the task terminal output. If the linter printed
suggestions but no diagnostics appeared, the `problemMatcher` pattern in `.vscode/tasks.json` does
not match the linter's output format; compare it against the format in
[Diagnostic format](#diagnostic-format). If the task terminal is also empty, run the linter from the
command line to confirm that it produces output at all.

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
