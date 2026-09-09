# SSC-FDM-SSIS0003 — Container Converted Inline

SSIS container (Sequence Container, For Loop, ForEach Loop) was expanded inline in the parent scope rather than converted to a separate block. In SSIS, containers provide variable scoping — variables declared inside a container are local to it. After inline expansion, those variables exist in the parent scope.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Low-to-moderate (once per inlined container) |
| Common action | No code change needed; review if container had local variables |

## Identification

Look for the marker:
```
--** SSC-FDM-SSIS0003 - SSIS CONTAINER EXPANDED INLINE IN PARENT SCOPE. VARIABLE SCOPING MAY DIFFER — CONTAINER-LOCAL VARIABLES NOW EXIST IN PARENT SCOPE. **
```

It appears before a block of SQL that was originally inside a container:

```sql
--** SSC-FDM-SSIS0003 - SSIS CONTAINER EXPANDED INLINE IN PARENT SCOPE. VARIABLE SCOPING MAY DIFFER — CONTAINER-LOCAL VARIABLES NOW EXIST IN PARENT SCOPE. **
-- Begin: Sequence Container - Load Stage Tables
INSERT INTO stage_customers SELECT * FROM raw_customers;
INSERT INTO stage_orders SELECT * FROM raw_orders;
-- End: Sequence Container - Load Stage Tables
```

## Fix Patterns

### Pattern 1: No local variables — no change needed (most common)

```sql
-- Before and After are identical — no fix required.
-- Most Sequence Containers simply group tasks for organizational purposes
-- and don't declare local variables.
--** SSC-FDM-SSIS0003 - SSIS CONTAINER EXPANDED INLINE IN PARENT SCOPE. VARIABLE SCOPING MAY DIFFER — CONTAINER-LOCAL VARIABLES NOW EXIST IN PARENT SCOPE. **
TRUNCATE TABLE stage_customers;
INSERT INTO stage_customers SELECT * FROM raw_customers;
```

### Pattern 2: Container had local variables — rename to avoid conflicts

```sql
-- Before (potential variable name conflict)
--** SSC-FDM-SSIS0003 - SSIS CONTAINER EXPANDED INLINE IN PARENT SCOPE. VARIABLE SCOPING MAY DIFFER — CONTAINER-LOCAL VARIABLES NOW EXIST IN PARENT SCOPE. **
LET row_count := 0;
INSERT INTO stage_customers SELECT * FROM raw_customers;
row_count := (SELECT COUNT(*) FROM stage_customers);

-- After (rename variable if it conflicts with a parent-scope variable)
LET container1_row_count := 0;
INSERT INTO stage_customers SELECT * FROM raw_customers;
container1_row_count := (SELECT COUNT(*) FROM stage_customers);
```

## Key Points

- Do **NOT** remove the FDM comment.
- The vast majority of inlined containers require **no code change** — they were used for visual grouping in SSIS, not variable isolation.
- Only investigate further if the container declared local variables that share names with parent-scope variables, which could cause unintended overwrites.
- For Loop and ForEach Loop containers are typically converted to `FOR` / `FOR row IN cursor` blocks and retain their scoping, so this marker mainly applies to Sequence Containers.
