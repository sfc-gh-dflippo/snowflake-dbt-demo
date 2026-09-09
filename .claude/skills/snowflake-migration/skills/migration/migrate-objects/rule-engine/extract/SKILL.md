---
name: rule-engine-extract
description: Extract reusable migration rules from code changes. Works on interactive fixes (before/after comparison), git history, or any pair of SQL files. Triggers: extract rule, deduce rule, learn from fix, create rule from fix, rule extraction.
parent_skill: rule-engine
license: Proprietary. See License-Skills for complete terms
---

# Extract Rules

Analyze changes to converted SQL files and extract reusable migration rules. Works in two modes:

- **Interactive fix mode** — the user fixed a file; compare before/after to extract a rule
- **Git history mode** — analyze committed changes retroactively

## Prerequisites

- Rule engine set up ([../SKILL.md](../SKILL.md))
- Snowflake connection active

## Mode Selection

If the user says something like "I fixed X, extract a rule" or "deduce a rule from my fix" → use **Interactive Fix Mode**.

If the user says "analyze recent changes" or "extract rules from git history" → use **Git History Mode**.

---

## Interactive Fix Mode

### Step 1: Get the "After" SQL

Read the current converted file (the fixed version):

```bash
cat <project_dir>/snowflake/<type>/<schema>/<name>.sql
```

Or ask the user which file they fixed.

### Step 2: Get the "Before" SQL

Find the changes in the file — use git diff, git log, or any other method to obtain the previous version. If no history is available, ask the user.

### Step 3: Analyze the Diff

Compare before and after to identify **distinct fix patterns**. For each pattern:

1. **What changed** — describe the transformation (before → after)
2. **Why** — what Snowflake compatibility issue does this fix?
3. **Is it mechanical?** — can a regex handle it, or does it need AI context?

If mechanical (direct find/replace):
- Propose `replacement_mode = 'regex'`
- Write `match_pattern` (detection regex)
- Write `replacement_find` and `replacement_replace` (substitution regex)

If context-dependent:
- Propose `replacement_mode = 'ai'`
- Write `match_pattern` (detection regex)
- Write `ai_context` describing: what to look for, how to fix it, edge cases to watch for

Always generate `examples` from the actual before/after.

### Step 4: Check for Duplicates

Use the `find_similar_rules` tool with `query` set to a description of the pattern.

If a similar rule exists:
> This pattern matches existing rule **"<name>"**. No new rule needed.

Done.

### Step 5: Confirm with User

Present the proposed rule:

> **New rule from your fix:**
>
> - **Name:** Variable binding colon prefix
> - **Mode:** ai
> - **Match pattern:** `LANGUAGE\s+SQL`
> - **Context:** In Snowflake LANGUAGE SQL procedures, variables in SQL statements need `:` prefix...
> - **Example:** `WHERE col >= p_start_date` → `WHERE col >= :p_start_date`
>
> Save this rule? [Yes / Edit / Skip]

### Step 6: Create the Rule

Use the `create_rule` tool with the confirmed parameters.

### Step 7: Propagate (Optional)

After creating the rule, offer to find other affected code units:

> Rule created. Check which other code units it applies to?

If yes → Load [../propagate/SKILL.md](../propagate/SKILL.md) with the new rule ID.

---

## Git History Mode

### Step 1: Identify Target Objects

Accept object names from the user, or discover from recent commits to find modified SQL files under the project's `snowflake/` directory.

Present the list:

> Found N modified SQL files. Analyze all, or select specific files?

### Step 2: Extract Diffs

For each target file, retrieve the diff showing what changed.

### Step 3: Analyze Changes

For each diff, identify distinct fix patterns. Classify each:

| Category | Example | Likely Mode |
|----------|---------|-------------|
| Direct substitution | `ISNULL(` → `COALESCE(` | `regex` |
| Syntax rewrite | `TOP N` → `LIMIT N` | `regex` |
| Structural change | `EXEC proc @p` → `CALL proc(:p)` | `ai` |
| Logic adjustment | Date arithmetic rewrite | `ai` |

### Step 4: Deduplicate Across Objects

Merge identical patterns across files. Two patterns are the same if they describe the same source→target transformation.

### Step 5: Check for Existing Rules

For each unique pattern, use `find_similar_rules` to check for duplicates. Remove already-covered patterns.

### Step 6: Confirm with User

For each new pattern, ask:

> **New pattern:** `EXEC schema.Proc @p1` → `CALL schema.Proc(:p1)`
> Found in: `dbo.CalcDiscount` (2 occurrences)
>
> Save as a reusable migration rule? [Yes / No]

### Step 7: Insert New Rules

Use the `create_rule` tool for each confirmed pattern with `created_from` = "deduced_from_history".

### Step 8: Find Other Affected Code Units

For each new rule, use `reverse_search_rules` to find other matching objects and report the count.

### Summary

> **Extraction complete:**
> - Analyzed N files
> - Found P distinct patterns
> - K already covered by existing rules
> - Created R new rules
> - New rules match Q additional code units
