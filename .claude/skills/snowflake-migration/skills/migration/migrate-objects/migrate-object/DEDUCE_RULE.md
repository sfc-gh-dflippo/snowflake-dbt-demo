# Deduce Rule

This skill has two modes:

- **Success path** (default) — after a fix passes all tests, check if the pattern should become a reusable rule
- **Anti-pattern path** (`mode = "anti-pattern"`) — after escalation, record what was tried and failed so future objects avoid the same dead ends

## Execution Model

When invoked from the migrate-object loop, run Steps 1-2 automatically (summarize fix, search for duplicates). Only pause for user input at Step 3 (save decision). If the user confirms, Steps 4-5 (insert rule + propagation scan) run automatically.

---

## Success Path

Invoked from [SKILL.md](SKILL.md) Step 6 when all tests pass and code changes were made.

### Step 1: Summarize the Fix (automatic)

Describe what changed and why in a short sentence (e.g., "Replaced CHARINDEX with POSITION for string lookups").

### Step 2: Search for Existing Rules (automatic)

Check if a similar rule already exists:

Use the `find_similar_rules` tool with `query` set to `"<fix_description>"`.

**If a similar rule exists** (top result is clearly the same pattern):
> "This fix matches existing rule `<name>`. No new rule needed."

Done — return to [SKILL.md](SKILL.md) Step 6.

### Step 3: Propose Rule to User

Present the extracted pattern with enough detail for a quick decision:

> **Extracted pattern from fix:** `<fix_description>`
> **Proposed mode:** `regex` / `ai`
> **Match pattern:** `<regex>`
> **No duplicate found in rule engine.**
>
> Save as a reusable rule? This will auto-apply to future objects with the same pattern.
> 1. Yes — save and check which other objects it applies to
> 2. No — one-off fix, continue

If **no**, done — return to [SKILL.md](SKILL.md) Step 6.

### Step 4: Insert the Rule (automatic after confirmation)

- If the fix is mechanical (simple find/replace), set `replacement_mode = 'regex'` and populate `replacement_find` / `replacement_replace`
- If the fix requires context or judgment, set `replacement_mode = 'ai'` and populate `ai_context` with detection hints, fix strategy, and edge cases
- Always populate `examples` with the before/after from the actual fix

Use the `create_rule` tool with the appropriate parameters. The tool generates the ID, builds search text, and inserts the rule.

For the full standalone extraction workflow (interactive fix mode or git history analysis), see [../rule-engine/extract/SKILL.md](../rule-engine/extract/SKILL.md).

### Step 5: Find Other Affected Code Units (automatic)

Use the `reverse_search_rules` tool to find which other objects have the same pattern:

Use the `reverse_search_rules` tool with `rule_id` set to `<new_rule_id>`.

If results found, report:
> "This rule also matches N other code units: `dbo.X`, `dbo.Y`, ... They will be auto-fixed during their pre-apply step."

Return to [SKILL.md](SKILL.md) Step 6.2.

---

## Anti-Pattern Path

Invoked from [SKILL.md](SKILL.md) on escalation — when fix iterations failed and the loop is being handed to the user. Records **what didn't work** so that future objects (and future attempts on this object) avoid repeating the same approaches.

### Step A1: Summarize the Failed Attempts

From the escalation context, build a summary of each failed approach:

```
Attempt 1: <what was tried> → <why it failed (error or test diff)>
Attempt 2: <what was tried> → <why it failed>
...
```

Distill a single description of the anti-pattern (e.g., "Replacing CONVERT with TO_VARCHAR without handling style codes causes date format mismatches").

### Step A2: Search for Existing Anti-Pattern Rules

Check if this anti-pattern is already recorded:

Use the `find_similar_rules` tool with `query` set to `"[AVOID] <anti_pattern_description>"`.

**If a similar negative rule exists:**
> "This anti-pattern matches existing rule `<name>`. No new rule needed."

Done — return to [SKILL.md](SKILL.md).

### Step A3: Create the Anti-Pattern Rule

Use the `create_rule` tool with:

- `name` = `[AVOID] <short_description>` (the `[AVOID]` prefix is the convention for negative rules)
- `replacement_mode` = `ai`
- `ai_context` = A structured description containing:
  - **What was tried:** the fix approach(es) that failed
  - **Why it failed:** the resulting error or test failure
  - **What to do instead:** if you have a hypothesis, include it; otherwise state "requires human investigation"
- `examples` = before/after showing the **failed** transformation (so agents can recognize the pattern)
- `match_pattern` = regex that detects the error-triggering code pattern (from the original error messages)

The `[AVOID]` prefix signals to [DIAGNOSE_FIX.md](DIAGNOSE_FIX.md) Step 3 that this is an anti-pattern — agents will read the `ai_context` to learn what to avoid.

### Step A4: Report

> "Recorded anti-pattern rule: `[AVOID] <description>`. Future objects with similar errors will see this as a known failed approach."

Return to [SKILL.md](SKILL.md).
