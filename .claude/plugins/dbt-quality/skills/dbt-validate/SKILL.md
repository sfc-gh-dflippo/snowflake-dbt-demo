---
name: dbt-validate
description:
  "Validate a single dbt model file against the dbt-quality rule engine, and install or troubleshoot
  the editor hooks that do it automatically. Use when: validating, checking, or linting a specific
  dbt model or schema file; a save-time validation hook is firing unexpectedly, blocking a save, or
  not running at all; setting up automatic dbt validation on write. For a whole-project or
  multi-project assessment with an HTML report, use the dbt-audit skill instead. Triggers: validate
  this model, check this dbt file, lint dbt model, dbt validation hook, validate on save, why did my
  save fail, pre-commit dbt check, dbt validate, check my model before committing."
category: develop
tags:
  - dbt
  - data-quality
  - data-engineering
---

# dbt Model Validation

Run the model-scoped rules of the shared dbt-quality engine against **one file**. Same rules, same
IDs, and same remediation text as `dbt-audit` — a different scope, not a different rulebook.

## Routing

| User intent                                 | Surface                                               |
| ------------------------------------------- | ----------------------------------------------------- |
| "Check this model" / a save-time hook fired | **`dbt-validate`** — this skill                       |
| "Populate the Problems panel" / CI gate     | **`dbt-lint`** — whole project, compiler-style output |
| "Audit my project" / "assess this estate"   | **`dbt-audit` skill** — all rules plus HTML report    |

|                 | `dbt-validate`                   | `dbt-lint`                        | `dbt-audit`                                |
| --------------- | -------------------------------- | --------------------------------- | ------------------------------------------ |
| Scope           | One model file                   | A project or path                 | A project, or an estate                    |
| Rules           | Model-scoped only                | Model-scoped                      | All rules                                  |
| Output          | Suggestions to stderr            | One line per suggestion to stdout | `suggestions.json` plus HTML               |
| Typical trigger | A save, or one file under review | Editor task, CI                   | A review, an assessment, after `dbt build` |

Rules that need more than one file are reported as **skipped**, never as passing.
`SSC-EWI-DBTSQL0001` decides between a CTE and an ephemeral model by fingerprinting the same
subquery across every model, and fragmentation is a property of the estate — one file cannot answer
either. If a user asks "is this model clean?", the accurate answer is "clean on everything checkable
from one file," and the skipped list states what was not covered.

---

## Running It

```bash
cd .claude/plugins/dbt-quality/scripts

# One file
uv run validate.py path/to/models/gold/dim_customers.sql

# Plain output, no ANSI — what the hook uses
uv run validate.py --simple "$FILE_PATH"

# Exit 1 on any error-level suggestion — the CI gate
uv run validate.py --strict path/to/model.sql
```

Exits 0 for anything that is not a dbt model, including a path that does not exist, so it is safe on
a hook that fires for every write.

The PEP 723 header on `validate.py` declares its own dependencies, so `uv run` needs nothing
installed. `typer` and `rich` are used for CLI presentation only; the rules themselves need only
`pyyaml`, so the engine can also be driven directly:

```bash
cd .claude/plugins/dbt-quality/scripts
PYTHONPATH=src python3 -c "
from pathlib import Path
from dbt_quality.discovery import build_portfolio
from dbt_quality.engine import run_single_file
r = run_single_file(build_portfolio(Path('.')), Path('models/gold/dim_customers.sql'))
for s in r.suggestions: print(s.level, s.rule_id, s.message)"
```

---

## Hooks and Editor Tasks

Both hooks are declared in `hooks/hooks.json` and activate when the plugin is installed. A third
surface — editor tasks — uses the linter and requires no plugin install.

| Surface              | Scope         | Trigger                                 | Output                         |
| -------------------- | ------------- | --------------------------------------- | ------------------------------ |
| `validate_file.py`   | One file      | Write, Edit, MultiEdit                  | Suggestions as agent context   |
| `audit_after_dbt.py` | Whole project | Bash command that rewrites the manifest | Short summary as agent context |
| `tasks.json`         | Whole project | On demand, or every 5 minutes           | Problems panel                 |

### validate_file.py — on Write and Edit

Validates the file just written. Silent unless there is something to report.

⛔ **Validation never blocks a save, at any level.** It always exits 0 for a dbt model, so the hook
is safe to fire while a model is half-written. An Error prints loudly, but a validation hook that
fails mid-refactor gets switched off, after which it protects nothing. Gate on errors in CI with
`dbt-lint --strict` instead; do not reach for `--strict` on the save-time hook.

### audit_after_dbt.py — after dbt runs

Runs the whole-project audit and injects a short summary as context. **Always advisory** — it never
returns non-zero, because a report should not fail somebody's command.

Two gates, both of which must pass:

1. **dbt was invoked in a way that rewrites the manifest.** A Bash command directly runs the dbt
   executable followed by a manifest-producing subcommand (`run`, `build`, `compile`, `parse`,
   `seed`, `snapshot`, `test`, `docs`). Flags between the two are tolerated, so
   `uv run dbt --profiles-dir ~/.dbt run` is caught, while `dbt-quality`, `snowflake-dbt-demo`, and
   textual mentions of dbt are not. dbt Projects on Snowflake runs server-side, does not update a
   local manifest, and therefore does not trigger this audit.
2. **The manifest advanced.** `target/manifest.json` exists and is newer than a stamp under
   `~/.cache/dbt-quality/`. Missing or unchanged is a silent skip.

The subcommand requirement is what keeps `dbt debug`, `dbt deps`, and `dbt --version` quiet. It
exists because `matcher` in `hooks.json` is tested against the _tool name_, not the command text:
the hook process starts on every Bash call, so the script's own regex is the only filter. Without
it, unrelated commands would show a spinner before gate 2 could rule them out. Gate 2 then still
catches a failed run, which matches the subcommand but leaves no newer manifest.

### tasks.json — project-wide editor diagnostics

`.vscode/tasks.json` at the repo root defines four tasks:

| Task                                            | What it does                                                                                  |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `dbt: quality suggestions`                      | Runs `dbt-lint` against the project through a `problemMatcher`, populating the Problems panel |
| `dbt: quality suggestions (errors only)`        | Same, with `--min-level error`                                                                |
| `dbt: quality suggestions (watch, every 5 min)` | Refreshes project-wide diagnostics every five minutes while the background task runs          |
| `dbt: quality report (JSON)`                    | Runs the full audit and writes `suggestions.json`                                             |

Cortex Code Desktop is a VS Code fork, so `tasks.json` plus a `problemMatcher` is the supported
editor-integration mechanism. SARIF is not supported (not present in the app bundle), and the
SQLFluff extension is blocked by the default-deny extension allowlist.

> **Note:** `problemMatcher` diagnostics appear only after the task runs — this is not
> live-as-you-type. The watch task starts on folder open; if it was added during the current
> session, reload the window or run `dbt: quality suggestions (watch, every 5 min)` once. The
> `validate_file.py` hook covers the per-file case on every save; these tasks cover the whole
> project. They are complementary, not redundant.

---

## Troubleshooting

Work through these in order; the first two cover most reports.

**Hook does not fire at all.** Confirm the plugin is installed — the in-repo directory is a
_source_, and hooks run only from `~/.snowflake/cortex/plugins/`. Use the `local-plugin-installer`
skill. Then check that nothing else registers a competing validation hook in
`.claude/settings.local.json`; a stale entry there will double-fire or shadow this one.

**Hook fires but reports nothing, on a file with known problems.** Almost always scope. The file
must be under a `models/` directory and be `.sql` or `.py`, and an enclosing `dbt_project.yml` must
be findable by walking up. Run the CLI directly on the same path to see the real output.

**Hook silently does nothing, and the CLI works.** The hook shells out to `uv run --script`, so
first confirm `uv` is on the PATH the hook inherits — it skips quietly when `shutil.which("uv")`
finds nothing. Then run the same command by hand:

```bash
uv run --script .claude/plugins/dbt-quality/scripts/validate.py --simple <file>
```

If that prints nothing **and** exits 0, suspect the entry point rather than uv. A Typer entry
function with a missing body exits 0 with no output, which is indistinguishable from success — that
shipped once here. `test_cli_entry_points_are_wired` guards it now, so run the test suite before
spending time on uv.

**A save is never blocked, and you expect it to be.** Nothing blocks a save at any level, by design.
To fail on errors, gate in CI with `dbt-lint --strict`, which exits 1 on any error-level suggestion.

**Audit hook runs too often, or not after a dbt command.** It is stamp-gated on manifest mtime.
Delete `~/.cache/dbt-quality/*.stamp` to force the next run. If it never fires, confirm dbt actually
rewrote `target/manifest.json` — a failed run does not.

---

## What Is Not Validated

**Names.** No rule checks model or column naming, here or in `dbt-audit`. A model may keep the name
its object had in the source database it was migrated from, and a dbt project records that name
nowhere machine-readable — the prescribed `/* Original Object: */` header is a comment that never
reaches `manifest.json`. A naming rule would be guessing. Full reasoning in
[`../dbt-audit/references/rule-catalog.md`](../dbt-audit/references/rule-catalog.md).

**SQL dialect syntax.** No rule checks for `TOP n`, `ISNULL`, `ROWNUM`, and similar. dbt surfaces
these itself when the model is built against Snowflake, so they are loud, self-announcing failures.
This engine earns its keep on _silent_ problems.

---

## References

| File                                                                                 | Load when                                           |
| ------------------------------------------------------------------------------------ | --------------------------------------------------- |
| [`../dbt-audit/references/rule-catalog.md`](../dbt-audit/references/rule-catalog.md) | Explaining why a rule fired, or adding one          |
| [`../dbt-audit/SKILL.md`](../dbt-audit/SKILL.md)                                     | The project-wide audit workflow                     |
| [`../../scripts/README.md`](../../scripts/README.md)                                 | Configuring thresholds, running the engine directly |
