# Git Collaboration Model

How the migration plugin manages git for multi-user concurrent migrations.

## Key Principles

- **No pull requests needed.** `finish` pushes directly to `main` — creating a PR would duplicate the merge and cause conflicts.
- **Branch-per-user.** Each user works on their own branch (e.g. `migrate-alice`). The plugin rebases onto updated `main` after every finish and on every status check.
- **Implicit sync.** `migration_status` calls automatically fetch and rebase before returning data, so status always reflects the latest shared state.
- **Claims prevent double-work.** `transition_status(status="begin")` records claims in Snowflake; two users cannot work on the same object simultaneously.

## What Happens During `finish`

1. Files for the finished objects are committed on top of `origin/main` using pure git plumbing (the working tree stays on your branch).
2. The commit is pushed to the remote. If a teammate pushed in between, the plugin re-fetches, checks for overlapping files, rebuilds, and retries (up to 3 times).
3. Your branch is rebased onto the updated `main`, pulling in teammates' merged work.

All of these steps are reported in the response's `git_activity` array. Dependents waiting on the finished objects are offered again on the next walk — that is derived, not a finish-time stamp clear.

## What Happens During `migration_status`

1. `git fetch <remote> <main_branch>`
2. `git rebase --autostash <remote>/<main_branch>` on your current branch
3. Status is computed from the rebased state (includes teammates' finished work).

If the sync pulled in new commits, `git_activity` will say so. If your branch was already up to date, it confirms that too.

## The `git_main_branch` Setting

Configured in `.scai/config/plugin.yml` under `git.main_branch` (default: `main`). This is the branch that `finish` pushes to and that `migration_status` syncs from.

## Conflict Scenarios

| Scenario | How it surfaces |
|----------|-----------------|
| Teammate overlap on finish | Response status `"conflict"` with list of affected files and instructions to resolve and retry |
| Rebase content conflict | Response status `"conflict"` with conflicted file list; agent resolves markers then retries |
| Autostash pop conflict | Response includes `stash_warning` — rebase succeeded but re-applying your uncommitted WIP had conflicts; use `git stash pop` |

## Multi-User Worktree Support

Each user can work in a separate git worktree. The plugin never switches branches — it builds commits via a throwaway index and pushes the SHA directly. Worktrees work correctly with no special configuration.

## Same-User Concurrent Sessions

When the same user runs multiple sessions (e.g., separate worktrees or terminals), each session has its own MCP session ID (`AGENT_ID` in the claims table). The plugin surfaces this transparently:

- **`my_objects_summary`** reports how many open claims belong to other sessions. If all claims are from a previous session, a note suggests resuming by claiming objects.
- **`transition_begin`** always allows re-claiming. If objects were held by a different session, the response includes `reclaimed_from_other_sessions` listing which objects were taken over (with the previous session ID and timestamp).
- **No hard locks.** The user decides whether to proceed — the plugin informs but never blocks.

This handles both concurrent sessions (two terminals at once) and sequential sessions (resuming work from yesterday in a new session).

## Why PRs Would Conflict

The plugin pushes finished files directly to `main`. If you also create a PR with the same files, merging it would either:
- Fail with merge conflicts (the files already exist on main), or
- Create duplicate commits.

The correct workflow is: claim → work → `finish` → done. No PR step.
