---
name: rule-engine-apply
description: Apply matched migration rules to a single SQL file. Runs regex replacements mechanically, presents AI-mode fixes for review. Triggers: apply rule, apply rules.
parent_skill: rule-engine
license: Proprietary. See License-Skills for complete terms
---

# Rule Apply

Apply matched rules to a single converted SQL file. For batch application (multiple files from propagation), see [BATCH.md](BATCH.md).

## Inputs

- `rules` — matched rules array from `search_rules` (sorted by priority)
- `file_path` — path to the local SQL file to modify
- `object_name` — name of the object being migrated

## Step 1: Sort by Priority

Process rules in `priority` order (ascending). Lower priority = runs first. This ensures simple regex fixes happen before structural AI rewrites.

## Step 2: Apply Regex-Mode Rules

For each rule where `replacement_mode = 'regex'`:

1. Read the current file content
2. Apply the regex substitution: find all matches of `replacement_find` and replace with `replacement_replace`
3. Write the updated content back to the file
4. Report what changed:
   > Applied **Replace ISNULL with COALESCE**: 3 replacements made

If `replacement_find` does not match anything in the file (even though `match_pattern` did), skip silently — the pattern may have already been fixed.

## Step 3: Apply AI-Mode Rules

For each rule where `replacement_mode = 'ai'`:

1. Read the current file content
2. Read the rule's `ai_context` and `examples`
3. Use your judgment to identify and fix all instances of the pattern described
4. Present the diff to the user for approval before writing:
   > **EXEC to CALL** — proposed changes:
   > ```diff
   > - EXEC schema.ProcName @p1, @p2
   > + CALL schema.ProcName(:p1, :p2)
   > ```
   > Apply this fix?
5. If approved, write the updated file
6. If rejected, skip this rule

## Step 4: Track

After each successful application, record it using the `record_rule_application` tool with `rule_id` set to the applied rule's ID and `outcome` set to `"applied"`. Optionally include `code_unit_name` and `file_path`.

## Output

Report back:
- Number of regex rules applied and total replacements made
- Number of AI rules applied (approved) and skipped (rejected)
- Whether the file was modified

## Rules

- **Always update the local file** — do not deploy SQL directly without writing changes to the file first
- **Regex rules do not need user approval** — they are mechanical and deterministic
- **AI rules always need user approval** — present the diff before writing
- **Re-read the file between rules** — earlier fixes may affect later rule matches
- **Track effectiveness** — after testing confirms the fix works, call `record_rule_application` with `outcome = "success"`
