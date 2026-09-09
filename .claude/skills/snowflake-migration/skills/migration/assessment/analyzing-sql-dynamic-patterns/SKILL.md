---
name: sql-dynamic-pattern-analyzer
description: Analyzes Dynamic SQL occurrences from SnowConvert issues, classifies patterns, scores complexity, and records migration considerations. Use for SQL Server, Redshift, Oracle, or Teradata to Snowflake migrations. Driven entirely by `scai assessment sql-dynamic`; no custom scripts.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Analyzing SQL Dynamic Patterns

Analyzes Dynamic SQL occurrences flagged by SnowConvert (issue code `SSC-EWI-0030`), classifies them against a dialect-specific pattern catalog, scores complexity, and records migration considerations. All operations go through the `scai assessment sql-dynamic` command — there are no Python helpers, no CSV/JSON scripts, no bash loops.

## Sub-Agent Mode

When invoked from a parent skill (e.g., `assessment/SKILL.md`) as a sub-agent, the parent provides a context block with the fields below. The `review_mode` field controls whether the per-occurrence review loop runs.

| Field | Required | Notes |
|---|---|---|
| `project_dir` | yes | absolute path to the SCAI project root |
| `output_dir` | yes | typically `<project_dir>/assessment/json` |
| `review_mode` | yes | `generate-only`, `auto-review-all`, or `skip` |

**On entry:** call the `configure` MCP tool with `project_dir` from the context block. Snowflake credentials are not required — `scai assessment sql-dynamic` reads only local CSVs and source files.

**Branching by `review_mode`:**

- `generate-only` — run only `scai assessment sql-dynamic generate` (Workflow Step 1) and return. The output JSON will contain `PENDING` occurrences; that is expected.
- `auto-review-all` — generate, then loop `show-code-unit` → analyze → `update --status REVIEWED` for **every** PENDING occurrence (Workflow Steps 2–6). Run `stats` at the end and confirm zero PENDING. The single-record / unique-analysis rule from [Critical Rules](#critical-rules) (NO BATCH UPDATES) still applies — each occurrence gets its own analysis.
- `skip` — return immediately with `"status": "skipped"`. The parent should not have dispatched in this case; this branch is defensive.

**On completion**, return **JSON only**:

```json
{
  "sub_skill": "analyzing-sql-dynamic-patterns",
  "status": "ok",
  "output_json": "<abs path to sql_dynamic_analysis.json>",
  "summary": "<one-line: total occurrences, REVIEWED count, PENDING count>",
  "error": null
}
```

On `skip`: `"status": "skipped"`, `"output_json": null`. On failure: `"status": "error"`, `"error": "<message>"`.

## Critical Rules

**ONLY USE `scai assessment sql-dynamic`:** All generate / show / update / stats operations are subcommands of `scai assessment sql-dynamic`. Do not write custom scripts, parsers, or batch wrappers.

**NO BATCH UPDATES:** Each `update` invocation processes **ONE** record with **ONE** unique analysis.
- Do **not** "walk IDs" sequentially as a batch just because they are adjacent.
- Do **not** use shell loops (e.g. `for id in ...; do scai assessment sql-dynamic update ...; done`) to apply the same update across many records.
- Do **not** copy/paste identical notes across multiple IDs; each occurrence must have its own specific rationale, even within the same code unit.

**CODE-UNIT-BASED WORKFLOW:** Use `show-file` (or `show-code-unit`) to view all occurrences within a procedure/function. Analyze each code unit separately by reading its source code.
- The generated analysis JSON stores the **full procedure source text inside each code unit** under the `procedure` field, alongside `fileName`, `procedureName`, `codeUnitStartLine`, and `linesOfCode`. Treat the JSON as the "source bundle" for analysis.

**QUALITY OVER SPEED:** This work is often fast, but do not "rush" by batching, reusing notes, or skipping code review. Aim for consistent, defensible analyses per occurrence.

## Source Platform Detection

**CRITICAL FIRST STEP:** Before classifying patterns, determine the source platform.

**Detection methods:**
1. Check `TopLevelCodeUnits.*.csv` — `SourceLanguage` column (e.g. `Transact` for SQL Server, `RedShift` for Redshift, `Oracle` for Oracle, `Teradata` for Teradata).
2. Examine code syntax in the procedure source (visible in the analysis JSON):
   - **SQL Server indicators:** `sp_executesql`, `EXEC(@sql)`, `QUOTENAME()`, `sys.*` catalog views.
   - **Redshift indicators:** `EXECUTE ... USING`, `QUOTE_IDENT()`, `QUOTE_LITERAL()`, `pg_catalog.*`, `plpgsql` functions.
   - **Oracle indicators:** `EXECUTE IMMEDIATE`, `DBMS_SQL.*`, `DBMS_ASSERT.*`, `ALL_*`/`USER_*`/`DBA_*` catalog views, `PRAGMA AUTONOMOUS_TRANSACTION`, `:varname` named bind variables, `@dblink` references.
   - **Teradata indicators:** `REPLACE PROCEDURE ... BEGIN ... END`, `EXECUTE IMMEDIATE <sql> USING ...` with positional `?` placeholders, `DBC.TablesV` / `DBC.ColumnsV` / `DBC.DatabasesV` / `DBC.IndicesV` catalog views, `REPLACE MACRO` / `EXEC macro_name(...)`, `VOLATILE TABLE`, `MULTISET` / `SET` table semantics, `SET QUERY_BAND`, BTEQ `&variable` substitution and `BT` / `ET` transaction control.
3. Review source file extensions and DDL: `.sql`, `.prc`, `.fnc`.

**Pattern catalog selection:**
- **SQL Server → Snowflake:** `reference/PATTERNS_TRANSACT.md`
- **Redshift → Snowflake:** `reference/PATTERNS_REDSHIFT.md`
- **Oracle → Snowflake:** `reference/PATTERNS_ORACLE.md`
- **Teradata → Snowflake:** `reference/PATTERNS_TERADATA.md`

⚠️ Always confirm the source platform with the user if it is unclear. Pattern definitions differ significantly between platforms.

## Inputs (auto-detected by parent)

The parent `assessment` skill resolves all inputs from `project_dir`. Do **not** prompt the user for paths.

| Input | Where it lives under `project_dir` |
|-------|------------------------------------|
| Project directory (preferred) | The project root itself — pass via `--project-dir` |
| `Issues.*.csv` (CSV mode) | `reports/SnowConvert/` |
| `TopLevelCodeUnits.*.csv` (CSV mode) | `reports/SnowConvert/` |
| Source code directory | `source/` |

**Mode selection:**
1. **Project mode (preferred)** — `scai assessment sql-dynamic generate --project-dir <project_dir> --output <path>`. SCAI auto-detects the registry / CSV reports and the source directory.
2. **CSV mode (fallback)** — `scai assessment sql-dynamic generate --csv-dir <reports_dir> --source-dir <source_dir> --output <path>` when the project layout is not standard.

## Workflow

1. **Generate** the analysis JSON from the project (or CSVs).
2. **Show file / show-code-unit** to surface all occurrences in a procedure plus its source.
3. **Analyze** each occurrence against the dialect's pattern catalog.
4. **Update** each occurrence individually with `--status REVIEWED` and the per-occurrence fields.
5. **Stats** to track progress.
6. Repeat steps 2–4 until every occurrence is `REVIEWED`.

### 1. Generate

```bash
# Project mode (preferred)
scai assessment sql-dynamic generate \
  --project-dir <project_dir> \
  --output <project_dir>/assessment/json/sql_dynamic_analysis.json

# CSV mode (fallback)
scai assessment sql-dynamic generate \
  --csv-dir <project_dir>/reports/SnowConvert \
  --source-dir <project_dir>/source \
  --output <project_dir>/assessment/json/sql_dynamic_analysis.json
```

**What this creates:**
- A JSON file with `metadata` (totals, generation timestamp, input files) and a `codeUnits` map.
- Each code unit holds `codeUnitId`, `procedureName`, `fileName`, `codeUnitStartLine`, `linesOfCode`, the full `procedure` text, and an `occurrences` list.
- Each occurrence starts with `status: PENDING` and empty analysis fields, ready for review.

### 2. View occurrences for a code unit

Group occurrences by file or by code unit:

```bash
# All occurrences in the file containing a given record (or with no --id, list all files)
scai assessment sql-dynamic show-file <analysis.json>
scai assessment sql-dynamic show-file <analysis.json> --file <fileName>

# Full code unit view including the procedure source and every occurrence inside it
scai assessment sql-dynamic show-code-unit <analysis.json> --code-unit-id "[DB].[schema].[ProcName]"

# Single occurrence detail
scai assessment sql-dynamic show <analysis.json> --id <N>
```

**Analysis approach:**
1. Use `show-file` to enumerate code units per file.
2. Pick one code unit and read its full procedure source (`show-code-unit`).
3. Open the dialect-appropriate `reference/PATTERNS_<DIALECT>.md` and classify each dynamic SQL site against the catalog.
4. Update each occurrence individually (next step).
5. Move on to the next code unit.

### 3. Classify patterns

**Reference per dialect (must read before classifying):**
- **SQL Server migrations** → `reference/PATTERNS_TRANSACT.md`
- **Redshift migrations** → `reference/PATTERNS_REDSHIFT.md`
- **Oracle migrations** → `reference/PATTERNS_ORACLE.md`
- **Teradata migrations** → `reference/PATTERNS_TERADATA.md`

⚠️ Pick the correct catalog based on the source platform (see [Source Platform Detection](#source-platform-detection)).

**Process:**
1. Read every pattern in the appropriate catalog before reviewing the first occurrence.
2. Compare the procedure source against each pattern.
3. Identify all patterns that apply (multiple may apply to the same occurrence).
4. Collect the analysis fields described below.
5. Pass the patterns to `--category` as a pipe-separated string (`"Pattern-A | Pattern-B"`); SCAI stores them as a list.

**Per-occurrence fields to collect:**

**generated_sql (`--generated-sql`):**
- The actual SQL that would be executed at runtime.
- Include the dynamic-SQL construction logic so it is clear what is built.
- Use representative values for variables; provide a complete best-effort statement (no ellipses or vague placeholders).

**sql_classification (`--sql-classification`):**
- DQL (SELECT) | DML (INSERT/UPDATE/DELETE) | DDL (CREATE/ALTER/DROP) | DCL (GRANT/REVOKE) | TCL (COMMIT/ROLLBACK) | UNKNOWN.
- Drives operation-level prioritization. **Pattern tagging is separate** — do not infer patterns from the SQL classification; choose them from the dialect catalog and pass via `--category`.

**notes (`--notes`):** A JSON object with three required keys (see [Notes Structure](#notes-structure)).

### 4. Score complexity

**Scale:** `low` (0–30), `medium` (31–60), `high` (61–85), `critical` (86–100).

**Process:**
1. Start from the base complexity of the matched pattern in `PATTERNS_<DIALECT>.md`.
2. Read the actual code carefully.
3. Override the base score **only if** the code materially differs from the pattern baseline.
4. Document the override reasoning under `complexity` in the notes JSON.

### 5. Update an occurrence

```bash
scai assessment sql-dynamic update <analysis.json> \
  --id <N> \
  --line <line_number> \
  --status REVIEWED \
  --category "Pattern-Name | Additional-Pattern" \
  --complexity medium \
  --sql-classification DDL \
  --generated-sql "CREATE TABLE dbo.TempTable (ID INT, Name VARCHAR(100))" \
  --notes '{
    "justification": "Line X uses dynamic SQL to construct a table name from user-supplied variables...",
    "complexity": "- Deep concatenation chains (5+ levels)\n- No input validation detected\n- Cross-schema dynamic references",
    "migration_considerations": "- Recommend Snowflake IDENTIFIER() function\n- Add input validation before migration\n- Estimated effort: 4–6 hours per occurrence"
  }'
```

**Command notes:**
- The first positional argument is the analysis JSON path.
- `--id` is required; it identifies the occurrence to update.
- `--line` should be set after reading the procedure source — generated records start with `line = 0`. Keep `0` only when the source line cannot be reliably determined.
- At least one of `--line`, `--status`, `--category`, `--complexity`, `--notes`, `--generated-sql`, `--sql-classification` must be supplied.
- `--category` accepts pipe-separated names; SCAI splits them into a list internally.

### 6. Track progress

```bash
scai assessment sql-dynamic stats <analysis.json>
```

Reports totals, per-status counts, and per-category counts. Repeat steps 2–5 until no `PENDING` records remain.

## Notes Structure

Each `--notes` value must be a JSON object with the three required keys below:

```json
{
  "justification": "Why this is dynamic SQL, what it does, context.",
  "complexity": "Technical factors affecting migration difficulty.",
  "migration_considerations": "Snowflake-specific recommendations, alternatives, effort estimate."
}
```

**Field length and tone:**
- `justification`: 40+ words, full sentences, reference specific code elements.
- `complexity`: 30+ words, full sentences, list the technical drivers.
- `migration_considerations`: 40+ words, full sentences, end with a concrete effort estimate.
- Do **not** write "similar to occurrence ##"; restate the context explicitly for every record.

**Formatting tips:**
- Use `\n` for line breaks within a multi-line field.
- Single-quote the entire JSON in shell to avoid quote escaping headaches.

## Reference Files

- `reference/PATTERNS_TRANSACT.md` — pattern catalog for SQL Server → Snowflake migrations.
- `reference/PATTERNS_REDSHIFT.md` — pattern catalog for Redshift → Snowflake migrations.
- `reference/PATTERNS_ORACLE.md` — pattern catalog for Oracle → Snowflake migrations.
- `reference/PATTERNS_TERADATA.md` — pattern catalog for Teradata → Snowflake migrations.

**Platform selection:**
- Use `PATTERNS_TRANSACT.md` for SQL Server sources.
- Use `PATTERNS_REDSHIFT.md` for Redshift sources.
- Use `PATTERNS_ORACLE.md` for Oracle sources.
- Use `PATTERNS_TERADATA.md` for Teradata sources.
