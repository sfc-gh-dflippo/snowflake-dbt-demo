---
name: rule-engine-search
description: Find applicable migration rules for a SQL file using Snowflake. Combines regex pattern matching (REGEXP_LIKE) with Cortex semantic search.
parent_skill: rule-engine
license: Proprietary. See License-Skills for complete terms
---

# Rule Search

Find applicable rules for a converted SQL file. All search happens in Snowflake — no local rule files. The `search_rules` MCP tool handles syncing file content and running queries so the SQL file content stays out of the agent's context window.

## Prerequisites

- Rule engine set up ([../SKILL.md](../SKILL.md))
- A converted SQL file to scan (e.g., `snowflake/<type>/<schema>/<name>.sql`)

## Search for Applicable Rules

Use the `search_rules` tool with:
- `file_path` = `<sql_file_path>`
- `description` = `"<brief description of the code and its migration-relevant patterns>"`

**Always pass `description`** — your description of the code's structure and patterns (e.g., `"procedure with dynamic SQL via sp_executesql, CONVERT with date style codes, and cursor-based iteration"`). This is prepended to the structural fingerprint the tool extracts, significantly improving Cortex semantic search relevance. You've already read the code, so summarize what you see.

The tool:
1. Reads the SQL file locally
2. Syncs it to `RULE_ENGINE.CODE_UNITS_SQL` via MERGE (so it's available for reverse searches)
3. Runs **regex pattern matching** (`REGEXP_LIKE`) — deterministic, pattern-based hits
4. Builds a search query from your `description` + a structural fingerprint (migration-relevant lines extracted from the procedure body)
5. Runs **Cortex semantic search** (`RULE_SEARCH!SEARCH`) using that query — catches structural patterns regex might miss
6. Scans for **EWI markers** (`SSC-EWI-*`, `SSC-FDM-*`) and resolves to local reference files
7. Deduplicates rules by `id` (regex hits take precedence)
8. Returns a JSON object with `rules` (sorted by priority) and `ewi_references`

### Output Format

```json
{
  "rules": [
    {
      "id": "isnull-to-coalesce",
      "name": "Replace ISNULL with COALESCE",
      "description": "...",
      "replacement_mode": "regex",
      "priority": 10,
      "replacement_find": "ISNULL\\s*\\(",
      "replacement_replace": "COALESCE(",
      "ai_context": null,
      "examples": [...],
      "match_source": "regex"
    },
    {
      "id": "variable-binding",
      "name": "Variable binding colon prefix",
      "description": "...",
      "replacement_mode": "ai",
      "ai_context": "...",
      "match_source": "semantic"
    }
  ],
  "ewi_references": [
    {
      "ewi_code": "SSC-EWI-0056",
      "title": "SSC-EWI-0056 - User-Defined Types Not Supported",
      "reference_file": "/path/to/resolving-ewis/reference/SSC-EWI-0056.md"
    }
  ]
}
```

### Present Results

**Rules** — label each based on `match_source` and `replacement_mode`:
- `regex` source + `regex` mode: `[regex match, auto-fixable]`
- `regex` source + `ai` mode: `[regex match, needs review]`
- `semantic` source: `[semantic match — needs review]`

**EWI references** — for each entry, read the `reference_file` and follow the fix guidance inside. If `reference_file` is null, the EWI code was found in the file but no reference doc exists yet — resolve it using your knowledge and then create the reference file per [../resolving-ewis/SKILL.md](../resolving-ewis/SKILL.md).

> Found N applicable rules and M EWI references for `<object_name>`:
>
> **Rules:**
> 1. **Replace ISNULL with COALESCE** [regex match, auto-fixable]
> 2. **EXEC to CALL** [regex match, needs review]
>
> **EWI references:**
> 1. **SSC-EWI-0056** — User-Defined Types Not Supported
> 2. **SSC-EWI-0021** — OUTPUT Clause Not Supported
>
> Apply fixes before deploying?

If both arrays are empty:

> No known rules or EWI markers found for `<object_name>`. Proceeding to deploy.

## Reverse Search: Find Code Units Affected by a Rule

Given a rule ID, find which other code units it applies to:

Use the `reverse_search_rules` tool with `rule_id` set to `<rule_id>`.

The tool runs both regex (`REGEXP_LIKE` on `RULE_ENGINE.CODE_UNITS_SQL`) and semantic search (`CODE_SEARCH!SEARCH`), deduplicates, and returns:

```json
{
  "rule_id": "isnull-to-coalesce",
  "rule_name": "Replace ISNULL with COALESCE",
  "affected_code_units": [
    {"code_unit_name": "dbo.GetOrderTotal", "object_type": "procedure", "file_path": "...", "match_source": "regex"},
    {"code_unit_name": "dbo.CalcDiscount", "object_type": "function", "file_path": "...", "match_source": "semantic"}
  ]
}
```

## Bulk Sync

To sync all SQL files in a directory to `RULE_ENGINE.CODE_UNITS_SQL` without searching:

Use the `sync_sql_files` tool with `directory` set to `<project_dir>/snowflake`.

This is useful before the `migrate-objects` deploy step to make all table/view SQL content searchable.

## Quick Actions

After reviewing results, offer these shortcuts:

- **"Apply all matched rules"** → Load [../apply/SKILL.md](../apply/SKILL.md) with the full rules list and file path.
- **"Find other objects matching rule X"** → Load [../propagate/SKILL.md](../propagate/SKILL.md) with the selected rule ID.
- **"Apply rule X to all matching objects"** → Load [../propagate/SKILL.md](../propagate/SKILL.md) followed by [../apply/BATCH.md](../apply/BATCH.md).

## Output

Carry the matched `rules` JSON forward into the apply step → [../apply/SKILL.md](../apply/SKILL.md).

For `ewi_references`, read each reference file and apply the documented fix patterns before deploying. After resolving an EWI, update or create the reference file per [../resolving-ewis/SKILL.md](../resolving-ewis/SKILL.md).
