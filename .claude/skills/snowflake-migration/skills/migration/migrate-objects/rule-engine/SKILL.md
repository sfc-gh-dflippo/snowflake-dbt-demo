---
name: rule-engine
description: Search, apply, extract, propagate, and manage reusable migration rules stored in Snowflake. Rules encode known source-to-Snowflake fix patterns (regex or AI-guided). Triggers: rule engine, search rules, apply rules, migration rules, known fixes, rule setup, extract rule, propagate rule.
parent_skill: migrate-objects
license: Proprietary. See License-Skills for complete terms
---

# Rule Engine

## On Entry

Tell the user:
> **Rule Engine** — I'll search for known migration fix patterns that apply to your code, and can apply them automatically (regex) or with your approval (AI-guided).

## Prerequisites

- Snowflake connection active with direct SQL ability
- Session `configure`d with a Snowflake connection and database. The `configure` MCP tool sets up the `RULE_ENGINE` schema automatically on first call.

## Setup (automatic)

You do not run a separate setup step. On the first `configure` call that supplies both `snowflake_connection` and `snowflake_database`, the MCP server creates and seeds everything needed:

- `RULE_ENGINE` schema
- `RULES`, `RULE_EVENTS`, `CODE_UNITS_SQL` tables
- Built-in seed rules (SQL Server → Snowflake patterns)
- `RULE_SEARCH` and `CODE_SEARCH` Cortex Search services

The setup handler is idempotent: calling `configure` again reruns pending migrations and re-seeds missing rules without disturbing existing data.

## Commands

### Search

Find applicable rules for a SQL file. Sends the file content to Snowflake for regex pattern matching (REGEXP_LIKE) and Cortex semantic search.

→ Load [search/SKILL.md](search/SKILL.md)

### Apply

Apply matched rules to local SQL files. Supports single-file and batch application. Runs regex replacements mechanically, presents AI-mode fixes for review.

→ Load [apply/SKILL.md](apply/SKILL.md)

### Extract Rules

Analyze code changes to extract reusable migration rules. Works on interactive fixes (before/after comparison) or git history (retroactive analysis of committed changes).

→ Load [extract/SKILL.md](extract/SKILL.md)

### Propagate

Given a rule, find all code units in the project it applies to. Uses reverse search (regex + Cortex semantic) to identify candidates, then hands off to Apply for batch application.

→ Load [propagate/SKILL.md](propagate/SKILL.md)

### Status

Check what rules exist and recent fix history:

```sql
SELECT id, name, replacement_mode, priority, rule_sentiment, rule_applications, successes, created_from
FROM RULE_ENGINE.RULES
ORDER BY priority;
```

## Tools

All tools are provided by the Rust `snowflake-migration` MCP server (`crates/mcp-server/`).

| Tool | Purpose |
|------|---------|
| MCP `configure` | Session setup; creates the `RULE_ENGINE` schema, seeds rules, and provisions the Cortex Search services on first call |
| MCP `search_rules` | Find rules matching a SQL file (regex + Cortex semantic search + EWI scan, combined) |
| MCP `search_rules_regex` | Regex-only search against `RULE_ENGINE.RULES` using in-memory SQL content |
| MCP `search_rules_cortex` | Cortex-only semantic search using in-memory SQL content |
| MCP `find_similar_rules` | Search rules by text description |
| MCP `reverse_search_rules` | Find code units affected by a rule |
| MCP `sync_sql_files` | Bulk sync SQL files from a directory for rule search |
| MCP `sync_sql_file` | Sync a single SQL file (in-memory content + metadata) into `RULE_ENGINE.CODE_UNITS_SQL` |
| MCP `create_rule` | Insert a new rule into `RULE_ENGINE.RULES` |
| MCP `list_rules` | List rules with optional filters; pass `detailed=true` for the full column set |
| MCP `record_rule_application` | Record a rule application outcome (applied / success / failure) |
