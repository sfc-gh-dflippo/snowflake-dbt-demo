# dbt-quality

dbt-quality checks dbt projects for Snowflake readiness, including dbt projects that SnowConvert
produced. It reads the project files, reports findings against 126 rules, and writes a JSON report
and an HTML report. The rules cover project structure, vars and parameters, hooks, incremental
loads, macros, SQL, materialization, tests, documentation, column contracts against scai DDL, and
conversion debt. The [rule catalog](references/rule-catalog.md) lists every rule.

dbt-quality ships in the `snowflake-migration` plugin as a second MCP server, `dbt-quality`, and as a
command-line tool. Both use the same analyzer, so they report the same findings.

## Limits

Read these before you rely on a result.

- **Static analysis only.** dbt-quality reads files. It does not run dbt, compile models, execute
  SQL, or connect to Snowflake or any other database. It does not read `target/manifest.json`.
- **Findings are evidence to review, not verdicts.** A finding can be a false positive, and a clean
  audit does not prove that a project is correct. Skipped checks are coverage gaps, not passes.
- **No correctness guarantee for suggested SQL.** Remediation text, examples, and `fix-columns`
  casts are suggestions. Snowflake does not guarantee that they compile, keep the original
  results, or perform well. Review each change, run your dbt build and tests, and compare results
  before you adopt it.
- **Local process, your file permissions.** The CLI and the MCP server run on your machine as your
  user. They can read every file that your user can read, and the caller chooses which directory
  to audit and where to write reports. dbt-quality does not sandbox those choices. Connect the MCP
  server only to clients you trust.
- **Unsigned binaries.** The macOS and Windows executables are not code-signed or notarized. If your
  organization allows only signed executables, dbt-quality cannot run there.
- **Writes happen only when you ask.** `annotate` and `fix-columns` preview a diff by default. To write,
  they need an explicit `--write` (MCP: `dry_run: false`) and a clean Git tree.

## Install

### 1. Install the plugin

Install the `snowflake-migration` plugin as the
[Snowflake documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/migration-skill/skill)
describes. To install it from its public repository with Cortex Code:

```bash
cortex plugin install "https://github.com/Snowflake-Labs/cortex-code-migrations/tree/main/plugin"
cortex plugin list   # shows the plugin and its directory
```

In this guide, `<plugin>` is that directory, and `DQ` is the dbt-quality launcher in it:

```bash
DQ="<plugin>/bin/dbt-quality"        # macOS and Linux
```

```powershell
$DQ = "<plugin>\bin\dbt-quality.cmd" # Windows; run it as & $DQ <command>
```

### 2. Let the launcher get the binary

The launcher downloads the native `dbt-quality` executable the first time it runs, so the first
start needs access to `github.com` and GitHub's release download hosts. It downloads the archive for your platform from the
[Snowflake-Labs/cortex-code-migrations releases](https://github.com/Snowflake-Labs/cortex-code-migrations/releases)
(release tag `dbt-quality-v<version>`), checks its SHA-256 against the release's `.sha256` file,
and caches the executable:

| Platform | Archive | Cache |
| --- | --- | --- |
| Linux x86_64, ARM64 | `dbt-quality-x86_64-unknown-linux-musl.tar.gz`, `dbt-quality-aarch64-unknown-linux-musl.tar.gz` | `${XDG_CACHE_HOME:-~/.cache}/dbt-quality/<version>/<target>/` |
| macOS Intel, Apple Silicon | `dbt-quality-x86_64-apple-darwin.tar.gz`, `dbt-quality-aarch64-apple-darwin.tar.gz` | the same |
| Windows x64, ARM64 | `dbt-quality-x86_64-pc-windows-msvc.zip`, `dbt-quality-aarch64-pc-windows-msvc.zip` | `%LOCALAPPDATA%\dbt-quality\<version>\<target>\` |

You need no Rust, Python, uv, or Node runtime. You need Git for `annotate`, `fix-columns --write`,
and the Git-aware checks. Check the installation:

```bash
"$DQ" --version
```

The checksum comes from the same release as the archive. It detects a corrupt or partial download;
it does not prove how the release was built.

**No internet access, or a proxy that blocks GitHub?** Download the archive and its `.sha256` file
yourself, check the checksum (`sha256sum -c`, `shasum -a 256 -c`, or `certutil -hashfile` on
Windows), extract it, and set `DBT_QUALITY_EXE` to the extracted `bin/dbt-quality` (Windows:
`bin\dbt-quality.exe`) before you start your client. To use an internal mirror of the releases
instead, set `DBT_QUALITY_DOWNLOAD_BASE` to the URL that replaces
`https://github.com/Snowflake-Labs/cortex-code-migrations/releases/download`.

## Run a first audit

### From Cortex Code

The plugin starts the `dbt-quality` MCP server for you. Open a Cortex Code session in your dbt
project (or in the folder that contains several projects), run `/mcp` to check that `dbt-quality`
is connected, and ask:

> Use dbt-quality to audit this project and show the highest-priority findings. Do not edit files.

The plugin's `dbt-quality` skill tells the agent how to run the audit, read the report, and stop for
your approval before it writes anything. See the [dbt-quality skill](SKILL.md).

### From Claude Code

Register the launcher as an MCP server once, then start Claude Code in your dbt project:

```bash
claude mcp add --scope user dbt-quality -- "<plugin>/bin/dbt-quality" mcp
```

On Windows, register `<plugin>\bin\dbt-quality.cmd` the same way. Run `/mcp` in Claude Code to
check the connection, then ask the same question as above. The server needs no API key and no
Snowflake credentials. It is a local stdio process: it has no port or URL, and if you start it by
hand in a terminal it waits for protocol messages and looks idle.

### From the command line

```bash
# JSON on stdout; no report files and no project edits.
"$DQ" audit /path/to/dbt-project --stdout --quiet

# Save JSON and HTML outside the project. Create the folder first.
mkdir -p ./reports
"$DQ" audit /path/to/dbt-project --out ./reports/findings.json --html ./reports/report.html
```

To find collisions between projects (duplicate models and sources, copied macros, conflicting
vars), audit the **folder that contains all the projects**. An audit of one project cannot see the
others. Without `--out` or `--stdout`, `audit` writes `dbt-audit-suggestions.json` into the audited
folder; it writes HTML only with `--html`.

## MCP tools and arguments

These are tool arguments, not shell commands. Paths must be readable by the server. An unknown
argument is an error.

| Tool | What it does | Arguments (default) |
| --- | --- | --- |
| `report` | Audits `path`, writes `dbt-audit-suggestions.json` and `dbt-audit-report.html`, returns their paths, the counts, and the top five remediation items | `path` (required), `out_dir` (a folder under the system temp folder, outside the project), `category` (packs, such as `["PRJ"]`), `min_level` (`information`), `html` (`true`), `include_models` (`false`), `ddl` |
| `findings` | Returns active findings as JSON | `path` (required), `rule_ids`, `files` (relative to `path`), `min_level`, `ddl` |
| `rules` | Lists rules, or returns one rule's full record with its remediation and examples | `code`, `pack`, `kind` (`EWI`, `FDM`, or `PRF`) |
| `annotate` | Previews or writes finding markers into the dbt files | `path` (required), `rule_ids`, `min_level`, `dry_run` (`true`), `remove` (`false`), `allow_dirty` (`false`) |
| `fix_columns` | Previews or writes casts to the column types and collations in scai DDL | `path` (required), `ddl`, `select`, `dry_run` (`true`), `allow_dirty` (`false`) |
| `version` | Returns the dbt-quality version, the pinned dbt version and commit, and the rule count | none |

Example arguments:

```json
{"path": "/work/estate", "out_dir": "/work/reports/dbt-quality"}
{"path": "/work/estate", "rule_ids": ["SSC-EWI-DBTPRJ0020"]}
{"code": "SSC-EWI-DBTPRJ0020"}
```

Reports in the default `out_dir` are temporary. Copy the ones you want to keep.

## CLI quick start

| Command | Use |
| --- | --- |
| `"$DQ" audit <root>` | Full audit: JSON report, and HTML with `--html <file>`. `--category`, `--min-level`, `--ddl`, `--fail-on-error`, `--quiet`, `--stdout`, `--out` |
| `"$DQ" lint <root>` | One line per finding, for editors and CI. `--format text\|json`, `--min-level`, `--strict`, `--ddl` |
| `"$DQ" validate <file>` | Model-scoped rules on one `.sql` or `.py` model. `--strict` |
| `"$DQ" rules` | The rule list. `--code <code>` prints one rule; `--format json\|markdown` |
| `"$DQ" annotate <root>` | Marker diff; `--write`, `--remove`, `--rule <code>`, `--allow-dirty` |
| `"$DQ" fix-columns <root>` | Cast diff against scai DDL; `--ddl`, `--select <glob>`, `--write`, `--allow-dirty` |
| `"$DQ" setup-tasks [project]` | VS Code tasks for the Problems panel |

`validate` runs only the rules that need one model. Project- and estate-wide rules are listed as
skipped, so a clean `validate` result does not mean the project passes. `validate` also returns
success for a file that is not a discovered model, such as a missing path or a file outside the
project's model paths, so check the path when it reports nothing.

## Read the HTML report

Open the HTML file in a browser. The overview shows the audit scope, coverage gaps, and the fixes
to do first. The findings view has search, filters, and sorting; open a finding to read its
evidence, the rule's guidance, and references. Suppressed findings, skipped checks, and read errors
have their own views, and none of them count as passed. Each release archive contains
`sample-report.html`, a report on synthetic test projects, if you want to try the report first.

For each finding or rule, you can record a decision: *Will address*, *Ignore once*, or *Ignore
permanently* with a reason. The browser keeps decisions in local storage for that audit folder, so
they survive a re-audit in the same browser. *Export decisions* downloads
`dbt-quality-decisions.json`; an *Ignore permanently* entry includes the waiver comment to add.
The report never writes project files. You or your agent apply the decisions, review the diff, run
your dbt checks, and audit again.

The report loads Chart.js 4.4.4 from a pinned jsDelivr URL with an integrity check, so its charts
need CDN access. Filters and code panels work without it, and the findings stay readable when
scripts are blocked. A preview pane or a sandbox that blocks scripts may not show the interactive
parts.

**Before you share a report, review it.** It contains file paths and finding evidence. By default it
does not contain whole model files. `--include-models` (MCP: `include_models: true`) adds the text of
discovered SQL and Python models, up to 256 KiB a file, 4 MiB in total, and 100 files. It never
adds profiles or configuration files. Sharing such a report shares that source code.

## Mark findings in the files, safely

`annotate` writes one marker comment above each finding, so you and your agent can fix the code
where the problem is:

```sql
--** SSC-EWI-DBTSQL0007 - <rule name>: <subject> **
```

YAML and Python files get `# ** ... **`. Markers carry only dbt-quality codes, and the analyzer ignores
them, so they do not change the findings. SnowConvert's own markers stay as they are, and a finding
that only reports a SnowConvert marker gets no second marker.

1. Audit, and read the evidence for the findings you plan to fix.
2. Preview: `"$DQ" annotate <root>` (MCP: `dry_run: true`). Review the diff.
3. Commit or stash your changes, then write: `"$DQ" annotate <root> --write`. It refuses when the Git
   tree, or a nested repository, has uncommitted changes; the two report files do not count.
   `--allow-dirty` skips that check; use it only on purpose.
4. Fix the code under each marker. `"$DQ" rules --code <code>` explains the rule and its remediation.
5. Run your dbt build and tests, audit again, and run `annotate` again: it removes the markers of
   fixed findings. `annotate --remove --write` removes all dbt-quality markers. With no edits in
   between, removal restores the original bytes; it does not undo your code changes.

`--rule <code>` (MCP: `rule_ids`) limits annotation to some rules.

## Check columns against scai DDL

The COL rules compare each model's outer `SELECT` with the Snowflake table that scai converted:
missing and extra columns, alias, type, and collation differences. Point them at a scai project
(they read `snowflake/<db>/<schema>/table/*.sql`), at a folder with `table/` subfolders, or at
`.sql` files:

```bash
"$DQ" lint /path/to/dbt-project --ddl /path/to/scai-project
"$DQ" fix-columns /path/to/dbt-project --ddl /path/to/scai-project            # diff only
"$DQ" fix-columns /path/to/dbt-project --ddl /path/to/scai-project --write    # clean Git tree
```

`fix-columns` rewrites a mismatched column as
`CAST(<expr> AS <DDL type>) COLLATE '<DDL collation>' AS <alias>`. It changes only types and
collations; missing and extra columns stay findings. A cast can fail or change values at run time,
so run your dbt build and tests afterwards.

## Configure and waive

Put `.dbt-quality.yml` (or `.dbt-quality.yaml`) in the folder you audit. dbt-quality reads one file
per audit: the first one it finds in the audited folder or up to eight folders above it, stopping
at the folder that contains `.git`. When you audit an estate, a `.dbt-quality.yml` inside one of its
projects is not read. A file that is not valid YAML is ignored without an error, so check your
settings with an audit after you edit the file.

```yaml
migration:
  mode: auto                 # auto, native, or lift_and_shift
  paths: ["models/legacy/*"] # optional: model paths that are converted code
disabled_rules: [SSC-EWI-DBTDOC0002]
exclude_dirs: [target, dbt_packages, logs, node_modules, archive]  # replaces the default list
thresholds:
  micro_project_threshold: 5
  column_doc_coverage: 0.8
ddl_paths: [../scai-project]   # for the COL rules, relative to this file
type_compare: normalized       # or strict: TIMESTAMP_NTZ does not match TIMESTAMP_NTZ(3)
ddl_bindings: {E2E_DB: PROD}   # values for <%TOKEN%> and ${TOKEN} in DDL names
ignore:
  - paths: ["models/legacy/*"]
    rules: [SSC-EWI-DBTSQL0006]
```

Use full rule codes in `disabled_rules` and `ignore`; they are case-sensitive. A disabled rule does
not run and is listed as a skipped check. A **waiver** is narrower: it accepts one finding or one
rule in some files, and it is not a fix. A waived finding stays in the report as suppressed, with
the waiver as its reason, and does not count as active.

Waive in the file, at the reported line:

```sql
select id from analytics.public.orders  -- dbt-quality: ignore SSC-EWI-DBTSQL0006
-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002
```

A directive after code covers that line. A directive on a line of its own covers its own line and
the next non-blank line. `ignore-file` covers the whole file. SQLFluff-style comments also work for
dbt-quality codes: `-- noqa`, `-- noqa: SQL0002`, `-- noqa-file`, and `-- noqa: disable=CODE` until
`-- noqa: enable=CODE`. A waiver that matches no finding, or names a code that is not a dbt-quality
rule (such as SQLFluff's `LT01`), is reported as `SSC-EWI-DBTMIG0010`. Findings for a whole project
or estate have no single line; waive them with `ignore` in `.dbt-quality.yml`.

For converted projects, dbt-quality detects SnowConvert output and can suppress architecture
findings that a lift-and-shift migration is expected to have. The report counts those separately.
If the detection is wrong for your project, set `migration.mode`. The
[rule catalog](references/rule-catalog.md) explains the tiers, codes, levels, and severities.

## Editor tasks

```bash
"$DQ" setup-tasks /path/to/dbt-project
```

This adds two tasks to `.vscode/tasks.json` and keeps your other tasks: **dbt: quality
suggestions**, and a watch task that runs every five minutes when the folder opens (if your editor's
task trust settings allow it). Findings appear in the Problems panel after a task runs, not as you
type. The file must be plain JSON; JSON with comments is not supported.

## Gate CI

Install the plugin, or download an archive as in [Install](#install), then run:

```bash
"$DQ" lint /path/to/dbt-project --strict
# Or keep a report and gate on errors:
"$DQ" audit /path/to/dbt-project --stdout --quiet --fail-on-error > findings.json
```

| Command | Exits 1 when |
| --- | --- |
| `lint --strict` | an active error-level finding passes `--min-level` |
| `audit --fail-on-error` | the audit has an active error-level finding (before `--category` and `--min-level` filters) |
| `validate --strict` | the file has an error-level finding |
| `audit`, `lint` | no `dbt_project.yml` is under the folder |
| any command | the command fails, for example a missing folder or a write error |

Warnings never fail these gates. Without `--strict` or `--fail-on-error`, a run with findings still
succeeds.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `dbt-quality: cannot download ...` | Access to `github.com` from your machine. The message shows the URL. See [Install](#install) for `DBT_QUALITY_EXE` and `DBT_QUALITY_DOWNLOAD_BASE`. |
| `SHA-256 mismatch` (Windows: `cannot download and verify`) | A proxy changed the download, or it is incomplete. Download again; if it still fails, do not run the file and tell your Snowflake contact. |
| The MCP server does not start, or shows no tools | Run `"$DQ" --version`. On macOS and Linux, check that the launcher is executable. In Cortex Code, run `cortex plugin list` to check that the plugin is enabled, then reconnect with `/mcp`. The first start downloads the binary; if your client stops waiting, start it again. |
| `No dbt_project.yml found under ...` | Point at a folder that contains `dbt_project.yml`, or at the folder above several projects. |
| A check is skipped | Read `skipped_checks` in the JSON. Each entry has a reason: the rule is disabled, or it needs more than one file. |
| `annotate` or `fix-columns` refuses to write | Commit or stash your changes, including in nested repositories, and preview the diff again. The folder must be in a Git repository. |
| A waived or disabled rule still appears | Use the full code. Check which `.dbt-quality.yml` the audit read: only one, from the audited folder or above it. |
| An expected finding is missing | Search for `dbt-quality: ignore` and `noqa`, and check `ignore` and `disabled_rules` in `.dbt-quality.yml`. Look in the Suppressed view of the report. |
| The report's charts are empty | The browser cannot reach `cdn.jsdelivr.net`. The findings still work. |

## More

- [Rule catalog](references/rule-catalog.md): every rule, its tier, and its signal.
- [dbt-quality skill](SKILL.md): how the agent runs dbt-quality and when it stops for your approval.
- `"$DQ" rules --code <code>`: one rule's full description, remediation, and examples.
