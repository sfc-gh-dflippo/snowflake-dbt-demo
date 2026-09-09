# Batch Apply

Apply one or more rules to multiple files (from propagation results).

## Step 1: Accept Targets

Receive the target list from [../propagate/SKILL.md](../propagate/SKILL.md) or from the user:
- "Apply rule X to all matching code units" → apply to entire list
- "Apply rule X to 3 of them" → let user pick 3 from the list
- "Apply rule X to dbo.ProcA, dbo.ProcB" → specific named targets

## Step 2: Batch Regex-Mode Rules

For rules where `replacement_mode = 'regex'`:

1. Apply to the **first** target file
2. Show the diff as a sample:
   > **Sample diff** (`dbo.GetOrderTotal`):
   > ```diff
   > - ISNULL(@val, 0)
   > + COALESCE(@val, 0)
   > ```
   > Apply to all N files? [All / One-by-one / Cancel]
3. If **All**: apply the same regex to every target file, report summary
4. If **One-by-one**: show diff for each file, ask approval per file
5. If **Cancel**: skip this rule entirely

## Step 3: Batch AI-Mode Rules

For rules where `replacement_mode = 'ai'`:

1. Process each target file individually:
   a. Read the file content
   b. Apply the rule using `ai_context` and `examples`
   c. Show the proposed diff
   d. Ask for approval
2. After reviewing a few, offer "approve remaining":
   > Approved 3/8. Apply the same pattern to the remaining 5 without review? [Yes / Continue reviewing]

## Step 4: Sync and Track

After each successful application:
1. Update the rule's application counter:
   ```sql
   UPDATE RULE_ENGINE.RULES SET rule_applications = rule_applications + 1 WHERE id = '<rule_id>';
   ```
2. After all files are processed, sync updated files:
   Use the `sync_sql_files` tool with `directory` set to `<project_dir>/snowflake`.

## Step 5: Batch Summary

> **Batch application complete for rule "EXEC to CALL":**
> - Applied to **N** of **M** code units
> - Regex mode: K auto-applied
> - AI mode: J applied (user approved), L skipped
> - Updated `rule_applications` count in RULE_ENGINE.RULES
>
> Test the modified objects?
>
> - **Re-validate all modified objects at once** (fast sanity check):
>   ```bash
>   scai test validate -c <SNOWFLAKE_CONNECTION_NAME> \
>     --where "source.canonicalName IN (<comma-separated-canonical-names>)"
>   ```
>   Confirm in `<metadata_database>.VALIDATION.LATEST`; the state machine picks up testing status from that table when the agent calls `transition_status(status='advance', task='runTests', outcome=...)` per object.
> - **For any failures, run the full diagnose/fix loop per object** → [../../migrate-object/SKILL.md](../../migrate-object/SKILL.md)
