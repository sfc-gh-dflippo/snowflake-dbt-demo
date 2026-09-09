---
name: git-setup
description: Set up git for a migration project
license: Proprietary. See License-Skills for complete terms
---

# Git Setup

The user has chosen to use git. Set up their repository.

This step runs early in setup, right after the project directory is confirmed.
If the project directory was **not** already a git repository when setup
started, `progress_setup()` has already initialized a local repo on `main` —
skip the init paths below and confirm settings with the user only when needed.

If the directory **was** already a git repository, walk the user through the
steps below before continuing.

## Step 1: Inspect current git state

Call:

```
configure(needs_git=true)
```

The response includes a `git_status` block:

```yaml
git_status:
  is_git_repo: <true|false>
  current_branch: <branch or empty>
  remote_url: <origin url or empty>
  configured_main_branch: <branch or empty>
```

Use this to drive the next step. **Do not run any `git` commands yourself**
to inspect state — `configure(needs_git=true)` is the source of truth. An
empty `remote_url` is expected and needs no action.

## Step 2: Confirm git settings

**If `git_status.is_git_repo` is `true` AND `git_status.remote_url` is present:**

Present a single confirmation covering repo, branch, and remote:

> "This folder is a git repository. I'll use these settings:
> - **Main branch:** `<current_branch>` (finished work lands here)
> - **Remote:** `<remote_url>` (`origin`) — finished work pushed here for backup/collaboration
>
> Does this look right?"
>
> 1. **Yes** — persist with `configure(git_main_branch="<current_branch>")`
>    and continue to Step 3.
> 2. **No** — ask what needs changing (branch, remote URL, or both), apply
>    the corrections:
>    ```
>    configure(git_main_branch="<branch>")
>    configure(git_remote_url="<url>")
>    ```

**If `git_status.is_git_repo` is `true` AND `git_status.remote_url` is empty:**

> "This folder is a git repository on branch `<current_branch>`, but no remote
> is configured. I'll use `<current_branch>` as the main branch.
>
> A remote (GitHub, GitLab, etc.) gives you off-machine backup and lets
> teammates collaborate in parallel. Would you like to set one up?"
>
> 1. **Set up a remote** — ask for the URL, then call:
>    ```
>    configure(git_main_branch="<current_branch>", git_remote_url="<url>")
>    ```
> 2. **Skip** — keep everything local. Call:
>    ```
>    configure(git_main_branch="<current_branch>")
>    ```
>    You can add a remote later with `configure(git_remote_url="<url>")`.

**If `git_status.is_git_repo` is `false`:**

Tell the user:

> "This folder isn't a git repository yet. Can you set one up for this folder
> and let me know when it's ready?"
>
> 1. **I'll set it up myself** — wait for the user to confirm, then re-run
>    `configure(needs_git=true)` and continue.
> 2. **Help me set it up** — initialize a fresh local repo on the user's
>    behalf:
>    ```bash
>    git init
>    git add -A
>    git commit -m "Initial migration project"
>    ```
>
> If any of these commands fails, attempt to diagnose and fix the issue (e.g.
> remove a stale `.git/index.lock`, resolve a conflicting worktree state, or
> re-run with corrected options). Surface the raw stderr to the user only if
> you cannot resolve the problem after one attempt.

After the repo is in place, re-run `configure(needs_git=true)` so you have a
fresh `git_status` snapshot, then present the confirmation above.

If `git_status.configured_main_branch` is already set and matches the
confirmed branch, you can skip the `configure(git_main_branch=...)` call.

A remote is **optional**. A purely local repository is fully supported. The
plugin will never push anywhere unless a remote is configured.

## Step 3: Housekeeping commits

After the main branch is confirmed, ask the user about automatic housekeeping
commits:

> "Would you like me to **automatically commit** workflow files and reports
> (deployment reports, data migration/validation workflows and reports) to
> `<main_branch>` as they're generated? This keeps your working tree clean
> without you having to think about it.
>
> 1. **Yes** (recommended) — automatically commit project-wide files.
> 2. **No** — leave them uncommitted; you'll manage them yourself."

**If the user says yes (or accepts the default):**

```
configure(git_housekeeping_commits=true)
```

**If the user says no:**

```
configure(git_housekeeping_commits=false)
```

## Step 4: Explain the git workflow

After the main branch is confirmed, briefly explain how git works in this migration so the user knows what to expect:

> "Here's how git works during the migration:
>
> - When you **finish** objects, I commit them directly to `<main_branch>` — no pull requests needed.
> - I regularly **fetch and rebase** your working branch onto `<main_branch>` to keep you in sync with any teammate activity.
> - If a remote is configured, finished work is pushed there automatically for backup and collaboration.
>
> You don't need to manage branches or create PRs — the plugin handles all of that behind the scenes, and I'll tell you what happened after each operation."

Keep this concise — don't elaborate further unless the user asks questions. If they want details, point them to the [collaboration model reference](../migrate-objects/references/collaboration-model.md).
