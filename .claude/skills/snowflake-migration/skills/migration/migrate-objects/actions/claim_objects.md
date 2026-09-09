# Action: Claim Objects

Add new objects to the working set.

> **Claim small batches.** Migrations are collaborative: an object claimed by one user is hidden from every other user's picker (`migration_status(next_objects)` excludes anyone's active claims). Claiming a large batch starves teammates of work and locks objects you may not get to for hours. Default to **showing the first 5 ready objects** (the picker's default page size) and let the user pick which to claim. Only fetch more when the user *explicitly* asks for a larger view (e.g. "show me 20", "list the whole wave"). Re-enter this skill after the user finishes a batch to show the next page.
>
> **Never auto-claim.** A casual "go ahead", "yes", "claim", or "next" is approval to *enter this skill and show the picker* — it is **not** approval to claim specific IDs. Always render the picker (Step 2) and wait for the user to name which objects to claim before calling `transition_status`.
>
> **Never substitute a category filter for picker IDs.** Do not claim with `where="source.objectType = 'table'"` or any other broad predicate as a shortcut. The `where` clause must be `id IN (...)` listing IDs the user picked from the picker output.

## Step 1: Discover

```
migration_status(mode="next_objects")
```

**Call the tool with no `limit` argument.** The tool returns 5 by default — that is the right number for the picker render.

> **`limit` rule.** Pass `limit` **only** when the user typed an explicit numeric request in this turn — e.g. "show me 20", "list 15 ready objects", "claim the whole wave (~30)". A casual "go ahead", "yes", "more", "show some more", or "next" is **not** an explicit request. If the user wants more without a number, ask "how many?" before calling the tool.

## Step 2: Confirm

> **Whatever the user said to enter this skill is not approval to claim specific IDs.** Even if the previous turn's answer was "claim", "pick up work", or "go ahead", that approval was for *entering* this skill — the IDs come from this turn's picker output, which the user has not yet seen. Render the list, then stop and wait.

Render the `objects` returned by Step 1 as a numbered list with id, name, and object type. For any entry with `blocked: true`, append a `BLOCKED at <blocked_at>: <missing_deps> missing deps` marker.

If `total_available` exceeds the number of returned `objects`, tell the user how many ready objects exist in total and that they can ask for a numeric `limit` (e.g. "show me 20") to view more.

Then offer concrete picker options and **wait for the user's response.** Example render:

```
Next 5 ready objects (12 total):

1. [Staging].[CWSO_CUST_TBL]      table       ready to deploy
2. [Staging].[CWSO_SOPEVEH_TBL]   table       BLOCKED at deploy: 2 missing deps
3. [Staging].[CWSO_ITEM_TBL]      table       ready to deploy
4. [Reporting].[v_daily_sales]    view        ready to deploy
5. [Reporting].[sp_load_sales]    procedure   ready to deploy

Pick one or more by number or name, or say "all", "first 3", or "show more".
```

**Do not call `transition_status` until the user names which objects to claim in this turn.** Without a specific pick, there is nothing to claim — re-prompt instead of guessing.

## Step 3: Claim

```
transition_status(status="begin", where="id IN ('<id1>', '<id2>')")
```

The `where` clause must be `id IN (...)` with the specific IDs the user picked in Step 2 — never a category predicate.

Surface any error and stop without retry.

If the response includes `reclaimed_from_other_sessions`, tell the user which objects were re-claimed from a previous session (include the session ID and timestamp) before proceeding with any deployment or migration work.

Return to [../SKILL.md](../SKILL.md).
