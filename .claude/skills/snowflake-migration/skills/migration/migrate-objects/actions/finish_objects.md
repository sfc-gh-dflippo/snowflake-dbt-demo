# Action: Finish Objects

Mark completed objects as done and (when git is enabled) merge them into `main`.

## Step 1: Confirm selection

Call `migration_status(mode="my_objects_details", group="done")` to fetch the list of object IDs ready to finish. Confirm with the user (all or a subset).

## Step 2: Run

```
transition_status(status="finish", where="id IN ('<id1>', '<id2>')")
```

### When git is enabled

The handler stamps each object done (`isDone`), then lands its registered files (`files.source.path`, `files.converted.path`, `files.artifacts.path`, `registry/<id>.json`) on top of `origin/main` using pure git plumbing — it builds the commit in a throwaway index and pushes the commit SHA directly, so your working tree never leaves your current branch (the response reports the new commit as `merge_commit`). It then rebases your branch onto the updated `origin/main`, pulling in any teammates' merged work. Files outside the selection stay on your branch.

### Relaying git activity

The response includes a `git_activity` array of human-readable strings describing the git operations that ran. **Always relay these to the user** (as a brief summary or bullet list) so they understand what happened to their repo. Example:

> - Pushed commit abc1234f to origin/main with 3 files (registry/obj-1.json, snowflake/proc_1.sql, snowflake/proc_1_test.sql)
> - Rebased branch 'migrate-alice' onto origin/main
On error (e.g. merge conflict), attempt to resolve it:

1. Read each conflicted file and decide the correct resolution (accept incoming, keep current, or merge both sides).
2. Edit the files to remove conflict markers and produce correct content.
3. Stage the resolved files with `git add`.
4. Continue the operation (`git rebase --continue` or `git merge --continue`).
5. Retry the tool call.

If resolution is ambiguous (both sides made substantive, incompatible logic changes), surface the conflict to the user with the relevant file contents and ask which version to keep.

### When git is disabled

The handler stamps each object done (`isDone`) and closes Snowflake claims. No git operations are performed — the response includes `"git_disabled": true` instead of `merge_commit`. Files remain on disk exactly as they are.

### After success (both modes)

The finish payload is `{status, action, actual_size}` plus git extras (`merge_commit`, `git_activity`, …) or `git_disabled`. It does **not** include `my_objects_summary` — pull claim status with `migration_status(mode="my_objects_summary")` if you need it.

Dependents waiting on these objects are offered again on the next walk — finish does not stamp or clear a dependency wait. Return to [../SKILL.md](../SKILL.md).
