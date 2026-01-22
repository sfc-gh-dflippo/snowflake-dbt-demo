---
name: Task Master AI - Development Workflows
description:
  Comprehensive workflow guide for different Task Master AI development scenarios including basic
  development loop, PRD-driven features, git branch workflows, team collaboration, experiments, and
  iterative subtask implementation patterns.
---

# Task Master AI - Development Workflows

Comprehensive guide for using Task Master in different development scenarios.

## Basic Development Loop

The fundamental cycle for task-driven development:

1. **List** - See what needs to be done
2. **Next** - Decide what to work on
3. **Show** - Get task details
4. **Expand** - Break down complex tasks
5. **Implement** - Write code
6. **Update** - Log progress
7. **Complete** - Mark as done
8. **Repeat**

## Simple Workflow (Getting Started)

### 1. Initialize Project

```sql
Initialize taskmaster-ai in my project
```

Creates `.taskmaster/` directory with configuration.

### 2. Create PRD

Create `.taskmaster/docs/prd.txt` with your requirements:

```markdown
# Project: E-Commerce Platform

## Overview

Build a modern e-commerce platform with user authentication, product catalog, shopping cart, and
checkout.

## Requirements

- User registration and login
- Product browsing and search
- Shopping cart management
- Secure checkout with Stripe
- Order history

## Technical Stack

- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Auth: JWT tokens
```

### 3. Parse PRD

```sql
Parse my PRD at .taskmaster/docs/prd.txt
```

Generates initial task list automatically.

### 4. View Tasks

```sql
Show me the task list
```

### 5. Analyze Complexity

```sql
Analyze task complexity for all pending tasks
```

### 6. Expand Complex Tasks

```sql
Expand task 3 into subtasks
```

Or expand all at once:

```sql
Expand all pending tasks based on complexity
```

### 7. Work on Next Task

```sql
What's the next task I should work on?
```

### 8. Implement & Track

```sql
Can you help me implement task 3?
Update subtask 3.2 with implementation findings
Mark task 3 as done
```

## Advanced Workflows

### PRD-Driven Feature Development

**Scenario:** Adding a major new feature to existing project

**Steps:**

1. **Create Feature Tag**

```sql
Create a new tag called feature-dashboard
```

1. **Write Feature PRD** Create `.taskmaster/docs/feature-dashboard-prd.txt`

2. **Parse into Tag**

```sql
Parse .taskmaster/docs/feature-dashboard-prd.txt into tag feature-dashboard
```

1. **Switch to Tag**

```sql
Switch to the feature-dashboard tag
```

1. **Analyze & Expand**

```sql
Analyze complexity for all tasks in feature-dashboard
Expand all pending tasks
```

1. **Implement** Work through tasks in the feature context

2. **Merge Back** When complete, merge code and optionally move key tasks to master

### Git Branch-Based Workflow

**Scenario:** Working on a feature branch

**Steps:**

1. **Create Git Branch**

```bash
git checkout -b feature/user-auth
```

1. **Create Matching Tag**

```sql
Create a tag from the current git branch
```

Creates `feature-user-auth` tag automatically.

1. **Develop in Isolation** All tasks stay isolated in the tag context.

2. **Merge**

```bash
git checkout main
git merge feature/user-auth
```

Tasks remain in tag for reference or can be moved to master.

### Team Collaboration Workflow

**Scenario:** Multiple developers working on same codebase

**Steps:**

1. **Create Personal Tag**

```sql
Create a new tag called alice-work --copy-from-current
```

1. **Work Independently** Alice works in `alice-work` tag, Bob works in `bob-work` tag.

2. **Master Stays Clean** Master tag contains only high-level deliverables.

3. **Coordinate Merges** Move completed tasks to master when features are merged.

### Experiment Workflow

**Scenario:** Trying a risky refactor or new approach

**Steps:**

1. **Create Experiment Tag**

```sql
Create a new tag called experiment-zustand --description="Testing Zustand for state management"
```

1. **Copy Relevant Tasks**

```sql
Copy tasks 5,6,7 to experiment-zustand tag
```

1. **Experiment** Modify and test in isolation.

2. **Decision**

- **Keep:** Merge code and tasks back
- **Discard:** Delete tag without affecting master

```sql
Delete tag experiment-zustand
```

### Existing Codebase Workflow

**Scenario:** Adding Task Master to an existing project

**Steps:**

1. **Initialize**

```sql
Initialize taskmaster-ai in my project
```

1. **Research Codebase**

```sql
Research current architecture and improvement opportunities --tree --files=src/
```

1. **Create Strategic PRD** Based on research findings, create improvement PRD.

2. **Organize by Area**

```sql
Create tag refactor-api
Create tag tech-debt
Create tag feature-dashboard
```

1. **Parse PRDs into Tags**

```sql
Parse api-refactor-prd.txt into tag refactor-api
Parse tech-debt-prd.txt into tag tech-debt
```

1. **Master for High-Level** Keep only major initiatives in master tag.

## Iterative Subtask Implementation

### Detailed Process

**1. Understand the Goal**

```sql
Show me subtask 3.2
```

**2. Plan Implementation**

- Explore codebase
- Identify files to modify
- Determine approach
- Note potential challenges

**3. Log the Plan**

```sql
Update subtask 3.2 with detailed implementation plan:
- Modify src/auth/login.ts lines 45-60
- Add new validation function
- Update tests in tests/auth.test.ts
- Potential issue: Need to handle edge case for OAuth users
```

**4. Verify Plan Logged**

```sql
Show me subtask 3.2
```

**5. Begin Implementation**

```sql
Mark subtask 3.2 as in-progress
```

**6. Log Progress Iteratively**

```sql
Update subtask 3.2 with progress:
- ✅ Validation function working correctly
- ✅ Tests passing
- ⚠️ OAuth edge case more complex than expected
- 📝 Added fallback for OAuth users
- 📝 Updated documentation
```

**7. Complete**

```sql
Mark subtask 3.2 as done
```

**8. Commit**

```bash
git add .
git commit -m "feat(auth): Implement login validation for subtask 3.2

- Added validation function with OAuth support
- Updated tests with edge cases
- Added fallback handling
- Updated documentation"
```

## Multi-Context Patterns

### Pattern 1: Version-Based Development

**MVP Tag:**

```sql
Create tag mvp --description="Minimum viable product"
```

- Focus on speed
- Basic functionality
- Fewer subtasks
- Direct implementation

**Production Tag:**

```sql
Create tag v1.0 --description="Production release"
```

- Focus on robustness
- Comprehensive testing
- Error handling
- Documentation

### Pattern 2: Priority-Based Tags

```sql
Create tag critical --description="Critical path items"
Create tag nice-to-have --description="Enhancement features"
Create tag tech-debt --description="Technical debt"
```

### Pattern 3: Module-Based Tags

```sql
Create tag frontend --description="Frontend development"
Create tag backend --description="Backend development"
Create tag infrastructure --description="Infrastructure work"
```

## Task Management Strategies

### Master List Strategy

**Keep in Master:**

- ✅ High-level deliverables
- ✅ Major milestones
- ✅ Critical infrastructure
- ✅ Release-blocking items

**Move to Feature Tags:**

- ❌ Detailed implementation subtasks
- ❌ Refactoring work
- ❌ Experimental features
- ❌ Team member-specific tasks

### Dependency Management

**Add Dependencies:**

```sql
Add dependency: task 8 depends on task 5
Add dependency: task 10 depends on tasks 7,8,9
```

**Validate:**

```sql
Validate all task dependencies
```

**Fix Issues:**

```sql
Fix all dependency issues automatically
```

### Task Reorganization

**Move Tasks:**

```sql
Move task 5 to become subtask 7.3
Move tasks 10,11,12 to positions 16,17,18
```

**Reorder:**

```sql
Move subtask 5.2 to 5.4
```

**Convert:**

```sql
Convert subtask 5.2 to standalone task 10
```

## Implementation Drift Handling

**Scenario:** Implementation differs from original plan

**Steps:**

1. **Identify Drift** Realize current approach differs from planned tasks.

2. **Update Future Tasks**

```sql
Update tasks from 18 onwards with new context:
We switched to React Query instead of Redux Toolkit.
All data fetching needs to use useQuery hooks.
Update task descriptions accordingly.
```

1. **Update Specific Task**

```sql
Update task 20 with:
Change from Redux actions to React Query mutations.
Use useMutation hook instead of dispatch.
Update tests to mock React Query.
```

## Research Integration

### When to Research

- **Before implementing** - Get current best practices
- **New technologies** - Up-to-date guidance
- **Security tasks** - Latest recommendations
- **Dependency updates** - Breaking changes
- **Performance optimization** - Current patterns
- **Complex bugs** - Known solutions

### Research Patterns

**Basic Research:**

```sql
Research latest best practices for JWT authentication
```

**With Context:**

```sql
Research React Query v5 migration for our API in src/api.js
```

**With Tasks:**

```sql
Research implementation approaches for tasks 5,6,7
```

**Save to Task:**

```sql
Research authentication patterns and save to task 3
```

## Best Practices

### PRD Creation

- Be specific about requirements
- Include technical stack
- Define acceptance criteria
- Note constraints and dependencies

### Task Breakdown

- Run complexity analysis first
- Use research for unfamiliar areas
- Keep subtasks focused (1-4 hours)
- Log implementation findings

### Tag Usage

- One tag per feature branch
- Use descriptive names
- Add descriptions
- Clean up merged tags

### Progress Tracking

- Update subtasks regularly
- Log what worked/didn't work
- Mark complete promptly
- Commit with task references

### Team Coordination

- Use personal tags for WIP
- Keep master for coordination
- Document tag purposes
- Communicate tag usage

## Troubleshooting Workflows

### Circular Dependencies

```sql
Validate all task dependencies
Fix all dependency issues
```

### Lost in Tasks

```sql
Show me the next task
Show me all pending tasks
Show complexity report
```

### Need to Reorganize

```sql
Move tasks to better positions
Update task priorities
Consolidate related tasks
```

### Tag Confusion

```sql
List all tags
Show current tag
Switch to master tag
```

## References

- See `COMMANDS.md` for complete command reference
- See `SETUP.md` for configuration details
- See `BEST_PRACTICES.md` for tips and patterns
