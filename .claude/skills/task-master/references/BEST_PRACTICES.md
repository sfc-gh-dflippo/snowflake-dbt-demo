# Task Master AI - Best Practices

Proven patterns and tips for effective task management with Task Master AI.

## PRD Creation

### Write Comprehensive PRDs

✅ **DO:**
```markdown
# Project: User Authentication System

## Overview
Implement secure user authentication with JWT tokens,
OAuth providers, and role-based access control.

## Requirements
1. User registration with email validation
2. Login with email/password
3. OAuth integration (Google, GitHub)
4. JWT token generation and validation
5. Role-based permissions (user, admin)
6. Password reset flow
7. Session management

## Technical Stack
- Backend: Node.js + Express
- Database: PostgreSQL with Prisma ORM
- Auth: Passport.js + JWT
- Email: SendGrid
- Testing: Jest + Supertest

## Acceptance Criteria
- Users can register with valid email
- OAuth login works for Google and GitHub
- JWT tokens expire after 24 hours
- Admin users can access admin routes
- Password reset emails sent within 1 minute
- All endpoints have >90% test coverage
```

❌ **DON'T:**
```markdown
# Project: Auth

Build authentication.

Requirements:
- Login
- Register
```

### Be Specific About Stack

✅ **DO:** "Use React Query v5 for data fetching"
❌ **DON'T:** "Use a state management library"

✅ **DO:** "PostgreSQL with Prisma ORM"
❌ **DON'T:** "Use a database"

### Include Constraints

- Performance requirements
- Security considerations
- Browser/device support
- Scalability needs
- Budget/time constraints

## Task Breakdown

### Use Complexity Analysis

```bash
# Always analyze before expanding
task-master analyze-complexity --research
task-master complexity-report
task-master expand --all --research
```

### Keep Subtasks Focused

✅ **Good subtask size:** 1-4 hours
❌ **Too large:** Full day or multi-day
❌ **Too small:** 15 minutes

✅ **DO:**
- Subtask 1: Create user model and migration
- Subtask 2: Implement registration endpoint
- Subtask 3: Add email validation
- Subtask 4: Write registration tests

❌ **DON'T:**
- Subtask 1: Build entire authentication system

### Use Research for Unfamiliar Areas

```bash
# Before expanding complex tasks
task-master research "latest JWT best practices" --save-to=3
task-master expand --id=3 --research
```

## Tag Management

### Naming Conventions

✅ **Good names:**
- `feature-user-auth`
- `feature-dashboard`
- `refactor-api`
- `experiment-zustand`
- `tech-debt`
- `v1.0`, `v2.0`
- `mvp`, `prototype`

❌ **Bad names:**
- `stuff`
- `temp`
- `test`
- `misc`

### Tag Organization Patterns

**Feature-Based:**
```
master          # High-level coordination
feature-auth    # Authentication feature
feature-cart    # Shopping cart feature
feature-payment # Payment processing
```

**Team-Based:**
```
master          # Shared coordination
alice-work      # Alice's tasks
bob-work        # Bob's tasks
```

**Version-Based:**
```
mvp             # MVP features
v1.0            # Version 1.0 features
v2.0            # Version 2.0 features
```

**Module-Based:**
```
frontend        # Frontend tasks
backend         # Backend tasks
infrastructure  # Infrastructure tasks
```

### When to Create Tags

✅ **Create tags for:**
- Feature branches
- Major initiatives
- Experiments
- Team member isolation
- Version milestones

❌ **Don't create tags for:**
- Single tasks
- Quick fixes
- Every small change

### Tag Cleanup

```bash
# After feature merge
git branch -d feature/user-auth
task-master delete-tag feature-user-auth --yes

# Or keep for reference
# (tags don't affect performance)
```

## Progress Tracking

### Log Implementation Findings

✅ **DO:**
```bash
task-master update-subtask --id=3.2 --prompt="
Implementation findings:

✅ What worked:
- JWT validation with jsonwebtoken library
- Middleware pattern for protected routes
- Token refresh using refresh tokens

⚠️ Challenges encountered:
- OAuth callback URL configuration tricky
- Had to handle edge case for expired tokens during refresh
- CORS issues with credentials

📝 Solutions implemented:
- Added CORS configuration for credentials
- Implemented token refresh endpoint
- Added comprehensive error handling

🔗 References:
- https://jwt.io/introduction
- OAuth 2.0 RFC 6749
"
```

❌ **DON'T:**
```bash
task-master update-subtask --id=3.2 --prompt="Done"
```

### Update Regularly

- Log plan before starting
- Update during implementation
- Note what worked/didn't work
- Document decisions made

### Use Status Effectively

**Status Progression:**
```
pending → in-progress → review → done
```

**Alternative flows:**
```
pending → deferred (postponed)
pending → cancelled (no longer needed)
pending → blocked (waiting on external)
```

## Dependency Management

### Define Dependencies Early

```bash
# After parsing PRD
task-master add-dependency --id=5 --depends-on=1,2
task-master add-dependency --id=8 --depends-on=5,6,7
task-master validate-dependencies
```

### Validate Regularly

```bash
# Before expanding tasks
task-master validate-dependencies

# After reorganizing
task-master fix-dependencies
```

### Logical Dependency Chains

✅ **DO:**
```
1. Database schema
2. API endpoints (depends on 1)
3. Frontend components (depends on 2)
4. Integration tests (depends on 3)
```

❌ **DON'T:**
```
1. Integration tests
2. Frontend components (depends on 1) ← Wrong order!
```

## Research Integration

### When to Research

**Always research for:**
- Security implementations
- New libraries/frameworks
- Performance optimizations
- Complex algorithms
- Breaking changes

**Example:**
```bash
# Before implementing auth
task-master research "JWT authentication best practices 2025" --save-to=3

# Before choosing library
task-master research "React Query vs Redux Toolkit comparison" --save-file

# Before refactoring
task-master research "Node.js async patterns" --files=src/api.js
```

### Research + Implementation Pattern

1. **Research first:**
```bash
task-master research "OAuth 2.0 implementation guide" --save-to=5
```

2. **Review findings:**
```bash
task-master show 5
```

3. **Expand with context:**
```bash
task-master expand --id=5 --research --prompt="Use findings from research"
```

4. **Implement:**
Follow the research-backed plan

## Team Collaboration

### Personal Tags for WIP

```bash
# Alice creates her tag
task-master add-tag alice-work --copy-from-current

# Bob creates his tag
task-master add-tag bob-work --copy-from-current

# Work independently
task-master use-tag alice-work
# ... work on tasks ...

# Coordinate via master
task-master use-tag master
# Review high-level progress
```

### Communicate Tag Usage

Document in team wiki or README:
```markdown
## Task Master Tags

- `master` - High-level coordination only
- `alice-work` - Alice's current work
- `bob-work` - Bob's current work
- `feature-*` - Feature branches (match git branches)
```

### Avoid Merge Conflicts

✅ **DO:**
- Use personal tags for WIP
- Keep master minimal
- Coordinate major changes

❌ **DON'T:**
- Have multiple people edit master simultaneously
- Create overlapping feature tags

## Implementation Patterns

### Iterative Development

```bash
# 1. View task
task-master show 3.2

# 2. Plan
task-master update-subtask --id=3.2 --prompt="Plan: ..."

# 3. Start
task-master set-status --id=3.2 --status=in-progress

# 4. Implement & log
# ... code ...
task-master update-subtask --id=3.2 --prompt="Progress: ..."

# 5. Complete
task-master set-status --id=3.2 --status=done

# 6. Commit
git commit -m "feat: implement subtask 3.2"
```

### Handle Implementation Drift

When implementation differs from plan:

```bash
# Update future tasks
task-master update --from=18 --prompt="
Changed approach: Using React Query instead of Redux.

Impact:
- All data fetching uses useQuery hooks
- No more Redux actions/reducers
- Simpler state management
- Update all related tasks
"

# Update specific task
task-master update-task --id=20 --prompt="
Change from Redux to React Query:
- Replace useDispatch with useMutation
- Remove Redux store setup
- Update tests to mock React Query
"
```

### Commit Messages

Link commits to tasks:

```bash
git commit -m "feat(auth): implement JWT validation (task 3.2)

- Added JWT middleware
- Implemented token refresh
- Added error handling
- Updated tests

Closes #3.2"
```

## Performance Tips

### Batch Operations

✅ **DO:**
```bash
# View multiple tasks at once
task-master show 1,3,5,7,9

# Update multiple statuses
task-master set-status --id=1,2,3 --status=done
```

❌ **DON'T:**
```bash
# One at a time
task-master show 1
task-master show 3
task-master show 5
```

### Use Complexity Analysis

```bash
# Analyze once, expand many
task-master analyze-complexity --research
task-master expand --all  # Uses analysis results
```

### Efficient Tag Switching

```bash
# Check current context
task-master tags

# Switch efficiently
task-master use-tag feature-auth
task-master next
```

## Common Pitfalls

### ❌ Avoid: Vague Tasks

**Bad:**
- "Fix bugs"
- "Improve performance"
- "Update code"

**Good:**
- "Fix login validation to handle special characters"
- "Optimize database queries in user endpoint (reduce from 500ms to <100ms)"
- "Update React components to use hooks instead of class components"

### ❌ Avoid: Skipping Dependencies

```bash
# Always define dependencies
task-master add-dependency --id=5 --depends-on=1,2

# Not just in your head!
```

### ❌ Avoid: Ignoring Complexity

```bash
# Don't skip analysis
task-master analyze-complexity --research

# Don't expand without research for complex tasks
task-master expand --id=8 --research
```

### ❌ Avoid: Poor Logging

**Bad:**
```bash
task-master update-subtask --id=3.2 --prompt="Done"
```

**Good:**
```bash
task-master update-subtask --id=3.2 --prompt="
Completed JWT implementation:
- Used jsonwebtoken library
- Added refresh token support
- Handled edge cases for expired tokens
- All tests passing
"
```

## Advanced Patterns

### Experiment Workflow

```bash
# 1. Create experiment tag
task-master add-tag experiment-graphql --description="Testing GraphQL migration"

# 2. Copy relevant tasks
task-master use-tag experiment-graphql
# Copy tasks 5,6,7 manually or via PRD

# 3. Experiment
# ... try new approach ...

# 4. Decision
if [ success ]; then
  # Merge code, move tasks to master
  git merge experiment-graphql
  task-master use-tag master
  # Recreate key tasks
else
  # Discard
  git branch -d experiment-graphql
  task-master delete-tag experiment-graphql --yes
fi
```

### Version Planning

```bash
# MVP
task-master add-tag mvp --description="Minimum viable product"
task-master use-tag mvp
# Focus on core features only

# V1.0
task-master add-tag v1.0 --description="First production release"
task-master use-tag v1.0
# Add polish, testing, documentation

# V2.0
task-master add-tag v2.0 --description="Major feature additions"
task-master use-tag v2.0
# Plan future enhancements
```

### Refactoring Strategy

```bash
# 1. Create refactor tag
task-master add-tag refactor-api --description="API refactoring"

# 2. Research current state
task-master research "current API architecture" --tree --files=src/api/

# 3. Create refactor PRD
# Document current issues and proposed solutions

# 4. Parse and implement
task-master parse-prd refactor-prd.txt --tag=refactor-api
task-master analyze-complexity --research
task-master expand --all --research
```

## Troubleshooting

### Lost Track of Tasks

```bash
# Find your place
task-master next
task-master list --status in-progress
task-master show <last-worked-on-id>
```

### Circular Dependencies

```bash
# Detect
task-master validate-dependencies

# Fix automatically
task-master fix-dependencies

# Or fix manually
task-master remove-dependency --id=8 --depends-on=5
```

### Tag Confusion

```bash
# See all tags
task-master tags --show-metadata

# Check current
task-master tags | grep "current"

# Switch back to master
task-master use-tag master
```

## References

- See `WORKFLOW.md` for complete workflows
- See `COMMANDS.md` for command reference
- See `SETUP.md` for configuration
- [Task Master GitHub](https://github.com/eyaltoledano/claude-task-master)


