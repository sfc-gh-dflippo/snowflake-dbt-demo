---
name: dbt-validate
description:
  "Validate a single dbt model file against the dbt-quality rule engine, and set up or troubleshoot
  the editor tasks. Use when: validating, checking, or linting a specific dbt model or schema file;
  setting up dbt-quality editor tasks; the Problems panel shows no dbt-quality entries. For a
  whole-project or multi-project assessment with an HTML report, use the dbt-audit skill instead.
  Triggers: validate this model, check this dbt file, lint dbt model, setup-tasks, why did my check
  fail, pre-commit dbt check, dbt validate, check my model before committing."
---

# dbt model validation

Run model-scoped dbt-quality rules against one file. The rules, codes, and remediation text are
shared with `dbt-audit`; only the scope differs. This is local static analysis. It does not build
models, connect to a warehouse, or prove that the SQL returns correct results.

## Stopping points

- Confirm the target file or project if the request is ambiguous.
- Ask before `setup-tasks` writes `.vscode/tasks.json`, unless the user already requested setup.
- Get approval before changing model code or adding a waiver. A finding is evidence to review,
  not permission to rewrite the model.

## Workflow

### 1. Check one file or the project

```bash
DQ=${CLAUDE_PLUGIN_ROOT}/bin/dbt-quality

$DQ validate path/to/models/gold/dim_customers.sql     # one file
$DQ validate --strict path/to/model.sql                # exit 1 on any error-level finding
$DQ lint <project> [--format json] [--min-level warning] [--strict]   # whole project, one line per finding
```

Replace example paths and optional arguments before running these commands. If the launcher path
contains spaces, quote `"$DQ"` when invoking it. On Windows, set `$DQ` to the absolute
`bin\dbt-quality.cmd` path (installed plugin) or `bin/dbt-quality.exe` path (release archive) and invoke it with `& $DQ validate <path>` or
`& $DQ setup-tasks <project>`. Generated tasks use process execution and the platform shell for
the periodic watcher.

`validate` exits 0 for a path that is not a discovered dbt model, including a missing path. Check
that the intended `.sql` or `.py` file is under the project's configured model paths. A literal
`$FILE_PATH` argument is read from the environment.

Project- and portfolio-scoped rules are skipped for a single-file check; they did not pass.
For example, `SSC-EWI-DBTSQL0001` compares subquery fingerprints across models, and fragmentation
checks need the estate. Report "No active findings from the model-scoped checks that ran" when
that is what the output shows. Do not call a model fully validated on that basis. Use project-wide
`lint` or the `dbt-audit` skill when the question needs broader coverage.

### 2. Set up editor tasks when requested

Run once per dbt project:

```bash
$DQ setup-tasks [PATH]
```

The command adds two tasks to `.vscode/tasks.json` at the dbt project root:
`dbt: quality suggestions` and `dbt: quality suggestions (watch, every 5 min)`. It keeps existing
tasks and adds only missing dbt-quality task labels. It exits 1 if `dbt_project.yml` is missing
or `tasks.json` is not valid JSON. JSON-with-comments is not supported. Tasks call the launcher
by its absolute path.

The linter emits `path:line:col:endLine:endCol: level: [RULE-ID] message -> fix`. The matcher must
capture all five position fields. If the Problems panel is empty or points at missing paths,
compare the `pattern` block in `.vscode/tasks.json` with this mapping:

| Linter field | `pattern` key |
| --- | --- |
| `path` | `file` (group 1) |
| `line`, `col` | `line`, `column` (2, 3) |
| `endLine`, `endCol` | `endLine`, `endColumn` (4, 5) |
| `level` | `severity` (6) |
| `RULE-ID` | `code` (7) |
| `message` | `message` (8) |

Diagnostics appear after the task runs, not as you type. The watch task requests folder-open
startup, subject to editor trust and task-approval settings. Reload the window after setup.
Findings do not cause failure by default. Use `lint --strict` to fail CI on active error-level
findings; warnings do not fail that gate. Command errors can still return nonzero.

### 3. Review findings and waivers

If the validator reports nothing on a file with known problems, first check its path and scope.
The engine must find an enclosing `dbt_project.yml` and discover the file as a model.

For a false positive or an accepted trade-off, prefer a narrow waiver to disabling the rule:

```sql
select id from analytics.public.orders  -- dbt-quality: ignore SSC-EWI-DBTSQL0006
-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002
```

```yaml
# .dbt-quality.yml — the only surface that can waive project- and portfolio-scoped findings
ignore:
  - paths: ["models/legacy/**"]
    rules: [SSC-EWI-DBTARC0001]
```

An inline directive applies to the diagnostic's reported line or the line immediately below the
directive. Config-related findings often anchor at `{{ config() }}`; other rules can have a precise
read-site anchor. Use the reported location, not a pack-wide assumption. Waived findings are
removed from outputs and counts. Record why the waiver is acceptable.

If an expected finding is missing, search for `dbt-quality: ignore` directives and the `ignore:`
block in the nearest `.dbt-quality.yml`. That configuration can be in an ancestor directory.
Also check `disabled_rules`, which produces skipped checks rather than findings.

## Limits and output

This tool has no general naming-convention validator. A migrated model may retain its original
object name; do not infer a naming defect without a reliable source-to-target mapping. MIG0007
can still flag ETL-instance names for review.

Static rules do not provide complete SQL dialect validation or business-result validation. Run
the project's dbt build/tests as appropriate after a change. Those checks also have limits; a
successful build does not prove all business logic correct.

Return the checked path, active findings, and any scope or coverage limits. Link each suggested
change to its evidence. For an HTML report or source-copy editing workflow, use `dbt-audit`.
Editing in a report does not run this validator or resolve findings; apply the change and check again.

## References

| File | Load when |
| --- | --- |
| [`../dbt-audit/references/rule-catalog.md`](../dbt-audit/references/rule-catalog.md) | Explaining why a rule fired, or adding one |
| [`../dbt-audit/SKILL.md`](../dbt-audit/SKILL.md) | The project-wide audit and marker loop |
