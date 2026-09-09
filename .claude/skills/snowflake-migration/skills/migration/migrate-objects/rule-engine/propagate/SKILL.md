---
name: rule-engine-propagate
description: Find code units that match a given rule for batch application. Uses reverse search (regex + Cortex semantic) to identify propagation candidates. Triggers: propagate rule, find candidates, which objects match, apply rule everywhere.
parent_skill: rule-engine
license: Proprietary. See License-Skills for complete terms
---

# Rule Propagation — Find Matching Code Units

Given a rule, find all code units in the project that the rule applies to using a lightweight, interactive reverse search (regex + Cortex semantic matching).

## Prerequisites

- Rule engine set up ([../SKILL.md](../SKILL.md))
- SQL files synced to `RULE_ENGINE.CODE_UNITS_SQL` (run `sync_sql_files` if not done yet)
- A rule to propagate (by ID or name)

## Step 1: Identify the Rule

Accept a rule ID, rule name, or description from the user. If the user says "my latest rule" or "the rule I just created", check recent rules:

```sql
SELECT id, name, replacement_mode, created_at
FROM RULE_ENGINE.RULES
ORDER BY created_at DESC
LIMIT 5;
```

If the user provides a description rather than an exact ID, use `find_similar_rules` to locate it.

## Step 2: Ensure SQL Files Are Synced

Before searching, make sure the project's converted SQL files are indexed:

Use the `sync_sql_files` tool with `directory` set to `<project_dir>/snowflake`.

If the user recently synced or you know files are up to date, skip this step.

## Step 3: Find Matching Code Units

Use the `reverse_search_rules` tool with `rule_id` set to the identified rule ID.

This runs:
1. **Regex matching** — `REGEXP_LIKE(sql_content, match_pattern)` against all synced SQL
2. **Cortex semantic search** — finds structurally similar code that the regex might miss

## Step 4: Review and Filter Results

Present the matches to the user:

> **Rule "EXEC to CALL"** matches **N code units**:
>
> | # | Code Unit | Type | Match Source |
> |---|-----------|------|-------------|
> | 1 | `dbo.GetOrderTotal` | procedure | regex |
> | 2 | `dbo.CalcDiscount` | procedure | regex |
> | 3 | `dbo.UpdateInventory` | procedure | semantic |
>
> Options:
> 1. **Apply to all N** — batch apply
> 2. **Select specific ones** — pick by number
> 3. **Review each first** — I'll show the relevant code sections

For semantic matches (lower confidence), briefly read the file and verify the pattern actually applies.

## Step 5: Hand Off to Apply

Once the user selects targets:

→ Load [../apply/SKILL.md](../apply/SKILL.md) with the selected rule(s) and target file list.

Pass along:
- The rule details (id, replacement_mode, replacement_find, replacement_replace, ai_context, examples)
- The list of target file paths
- Whether this is a batch-all or selective application

## Quick Shortcut

For rapid propagation without interactive review:

> "Apply rule `<rule_id>` to all matching code units"

This chains Steps 1–5 automatically: identify rule → sync → reverse search → apply all.
