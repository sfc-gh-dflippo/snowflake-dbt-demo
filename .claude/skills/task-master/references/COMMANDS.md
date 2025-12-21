---
name: Command Reference
description: Comprehensive command-line reference and usage examples for task-master
---

# Task Master AI - Command Reference

Quick reference for common Task Master commands in natural language (for AI agents) and CLI format.

## Task Viewing

### List Tasks

**AI agents:** `Show me the task list` or `List all tasks` **CLI:** `task-master list`

**With filters:**

- `Show me pending tasks` → `task-master list --status pending`
- `Show me done tasks` → `task-master list --status done`
- `Show tasks with subtasks` → `task-master list --with-subtasks`

### View Specific Tasks

**AI agents:** `Show me task 5` or `Show me tasks 1, 3, and 5` **CLI:** `task-master show 5` or
`task-master show 1,3,5`

**For subtasks:**

- `Show me subtask 3.2` → `task-master show 3.2`

### Next Task

**AI agents:** `What's the next task I should work on?` **CLI:** `task-master next`

Shows the next available task based on dependencies and priorities.

## Task Creation

### Add Task

**AI agents:** `Add a task to implement user authentication` **CLI:**
`task-master add-task --prompt="Implement user authentication"`

**With options:**

```bash
task-master add-task \
  --prompt="Implement user authentication" \
  --priority=high \
  --dependencies=1,2 \
  --research
```

### Add Subtask

**AI agents:** `Add a subtask to task 5 for validation logic` **CLI:**
`task-master add-subtask --parent=5 --title="Add validation logic"`

## Task Modification

### Update Task

**AI agents:** `Update task 5 with new requirements about OAuth support` **CLI:**
`task-master update-task --id=5 --prompt="Add OAuth support requirements"`

### Update Subtask

**AI agents:** `Update subtask 3.2 with implementation findings` **CLI:**
`task-master update-subtask --id=3.2 --prompt="Implementation findings..."`

### Update Multiple Tasks

**AI agents:** `Update tasks from 18 onwards with context about React Query` **CLI:**
`task-master update --from=18 --prompt="Switching to React Query..."`

### Set Status

**AI agents:** `Mark task 3 as done` or `Mark subtask 3.2 as in-progress` **CLI:**
`task-master set-status --id=3 --status=done`

**Status options:** `pending`, `in-progress`, `done`, `review`, `deferred`, `cancelled`

## Task Breakdown

### Expand Task

**AI agents:** `Expand task 4 into subtasks` **CLI:** `task-master expand --id=4`

**With options:**

```bash
task-master expand --id=4 \
  --num=7 \
  --research \
  --force \
  --prompt="Focus on security aspects"
```

### Expand All

**AI agents:** `Expand all pending tasks based on complexity` **CLI:**
`task-master expand --all --research`

### Clear Subtasks

**AI agents:** `Clear all subtasks from task 5` **CLI:** `task-master clear-subtasks --id=5`

## Complexity Analysis

### Analyze Complexity

**AI agents:** `Analyze task complexity for all pending tasks` **CLI:**
`task-master analyze-complexity --research`

### View Report

**AI agents:** `Show me the complexity report` **CLI:** `task-master complexity-report`

## Dependencies

### Add Dependency

**AI agents:** `Add dependency: task 8 depends on task 5` **CLI:**
`task-master add-dependency --id=8 --depends-on=5`

**Multiple dependencies:**

```bash
task-master add-dependency --id=10 --depends-on=7,8,9
```

### Remove Dependency

**AI agents:** `Remove dependency: task 8 no longer depends on task 5` **CLI:**
`task-master remove-dependency --id=8 --depends-on=5`

### Validate Dependencies

**AI agents:** `Validate all task dependencies` **CLI:** `task-master validate-dependencies`

### Fix Dependencies

**AI agents:** `Fix all dependency issues automatically` **CLI:** `task-master fix-dependencies`

## Task Organization

### Move Task

**AI agents:** `Move task 5 to become subtask 7.3` **CLI:** `task-master move --from=5 --to=7.3`

**Move multiple:**

```bash
task-master move --from=10,11,12 --to=16,17,18
```

### Remove Task

**AI agents:** `Remove task 5 permanently` **CLI:** `task-master remove-task --id=5 --yes`

### Remove Subtask

**AI agents:** `Remove subtask 5.2` **CLI:** `task-master remove-subtask --id=5.2`

**Convert to task:**

```bash
task-master remove-subtask --id=5.2 --convert
```

## Tag Management

### List Tags

**AI agents:** `Show me all tags` or `List all tags` **CLI:** `task-master tags`

**With metadata:**

```bash
task-master tags --show-metadata
```

### Create Tag

**AI agents:** `Create a new tag called feature-auth` **CLI:** `task-master add-tag feature-auth`

**From git branch:**

```bash
task-master add-tag --from-branch
```

**Copy from current:**

```bash
task-master add-tag my-work --copy-from-current --description="My tasks"
```

### Switch Tag

**AI agents:** `Switch to the feature-auth tag` **CLI:** `task-master use-tag feature-auth`

### Delete Tag

**AI agents:** `Delete the experiment-zustand tag` **CLI:**
`task-master delete-tag experiment-zustand --yes`

### Rename Tag

**AI agents:** `Rename tag old-name to new-name` **CLI:** `task-master rename-tag old-name new-name`

### Copy Tag

**AI agents:** `Copy tag master to backup` **CLI:** `task-master copy-tag master backup`

## Research

### Basic Research

**AI agents:** `Research latest best practices for JWT authentication` **CLI:**
`task-master research "latest JWT authentication best practices"`

### Research with Context

**AI agents:** `Research React Query v5 migration for our API in src/api.js` **CLI:**
`task-master research "React Query v5 migration" --files=src/api.js`

**With project tree:**

```bash
task-master research "architecture improvements" --tree
```

**With tasks:**

```bash
task-master research "implementation approaches" --id=5,6,7
```

**Save to task:**

```bash
task-master research "auth patterns" --save-to=3
```

**Save to file:**

```bash
task-master research "performance optimization" --save-file
```

## Project Management

### Initialize

**AI agents:** `Initialize taskmaster-ai in my project` **CLI:** `task-master init`

**Quick init:**

```bash
task-master init --yes
```

**With rules:**

```bash
task-master init --rules cursor,windsurf
```

### Parse PRD

**AI agents:** `Parse my PRD at .taskmaster/docs/prd.txt` **CLI:**
`task-master parse-prd .taskmaster/docs/prd.txt`

**Into specific tag:**

```bash
task-master parse-prd feature-prd.txt --tag=feature-auth
```

**With options:**

```bash
task-master parse-prd prd.txt \
  --num-tasks=10 \
  --force \
  --research
```

### Generate Task Files

**AI agents:** `Generate task files` **CLI:** `task-master generate`

## Configuration

### View Models

**AI agents:** `Show me the current model configuration` **CLI:** `task-master models`

### Configure Models

**AI agents:** `Change the main model to claude-3-5-sonnet` **CLI:**
`task-master models --set-main claude-3-5-sonnet-20241022`

**Interactive setup:**

```bash
task-master models --setup
```

**Set all models:**

```bash
task-master models \
  --set-main claude-3-5-sonnet-20241022 \
  --set-research perplexity/sonar-pro \
  --set-fallback gpt-4o
```

### Manage Rules

**AI agents:** `Add windsurf and roo rules to the project` **CLI:**
`task-master rules add windsurf,roo`

**Remove rules:**

```bash
task-master rules remove vscode
```

**Interactive:**

```bash
task-master rules setup
```

## Common Patterns

### Start New Feature

```bash
# 1. Create branch and tag
git checkout -b feature/user-auth
task-master add-tag --from-branch

# 2. Create PRD
# Edit .taskmaster/docs/feature-auth-prd.txt

# 3. Parse and prepare
task-master parse-prd feature-auth-prd.txt --tag=feature-user-auth
task-master analyze-complexity --research
task-master expand --all --research

# 4. Start working
task-master next
```

### Daily Development

```bash
# Morning: Check status
task-master list --status pending
task-master next

# During: Track progress
task-master show 3.2
task-master update-subtask --id=3.2 --prompt="Progress notes..."
task-master set-status --id=3.2 --status=done

# End of day: Review
task-master list --status done
```

### Handle Implementation Drift

```bash
# Update future tasks
task-master update --from=18 --prompt="New approach: using React Query"

# Update specific task
task-master update-task --id=20 --prompt="Change to React Query mutations"
```

### Merge Feature

```bash
# 1. Complete all tasks
task-master list --status pending --tag=feature-auth

# 2. Merge code
git checkout main
git merge feature/user-auth

# 3. Optional: Move key tasks to master
task-master use-tag master
# Manually recreate important tasks or keep feature tag for reference
```

## Flags & Options

### Common Flags

- `--research` - Use research model for AI operations
- `--force` - Skip confirmations or replace existing
- `--yes` - Skip all prompts
- `--tag=<name>` - Specify tag context
- `--file=<path>` - Specify tasks.json path

### Status Values

- `pending` - Ready to work on
- `in-progress` - Currently being worked on
- `done` - Completed
- `review` - Ready for review
- `deferred` - Postponed
- `cancelled` - Cancelled
- `blocked` - Blocked by external factors

### Priority Values

- `high` - Critical/urgent
- `medium` - Normal priority (default)
- `low` - Nice to have

## Tips

1. **Use comma-separated IDs** for batch operations:

   ```bash
   task-master show 1,3,5,7
   task-master set-status --id=1,2,3 --status=done
   ```

2. **Leverage research** for unfamiliar areas:

   ```bash
   task-master expand --id=5 --research
   task-master add-task --prompt="..." --research
   ```

3. **Tag naming conventions**:

   - Features: `feature-<name>`
   - Experiments: `experiment-<name>`
   - Versions: `v1.0`, `v2.0`, `mvp`
   - Personal: `<name>-work`

4. **Log implementation findings** to subtasks:

   ```bash
   task-master update-subtask --id=3.2 --prompt="
   ✅ Validation working
   ⚠️ OAuth edge case complex
   📝 Added fallback
   "
   ```

5. **Use dependencies** to enforce order:
   ```bash
   task-master add-dependency --id=8 --depends-on=5,6,7
   ```

## References

- See `WORKFLOW.md` for detailed workflows
- See `SETUP.md` for configuration
- See `BEST_PRACTICES.md` for tips
- [Full CLI Reference](https://github.com/eyaltoledano/claude-task-master)
