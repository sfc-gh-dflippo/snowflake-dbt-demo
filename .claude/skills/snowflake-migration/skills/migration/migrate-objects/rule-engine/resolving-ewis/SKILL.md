---
name: resolving-ewis
description: "**[REQUIRED]** Invoke this skill FIRST before resolving ANY SnowConvert EWI (Errors, Warnings, Issues) codes. DO NOT attempt to fix EWIs manually - always invoke this skill first. Triggers: SSC-EWI, SSC-FDM, EWI code, resolve EWI, fix EWI, SnowConvert error."
license: Proprietary. See License-Skills for complete terms
---

## Usage

When you encounter an EWI code (e.g., `SSC-EWI-0021`, `SSC-EWI-TS0087`):

1. **Check for existing reference**: Look in the `reference/` folder for a file matching the EWI code (e.g., `reference/SSC-EWI-0021.md`)

2. **If the reference exists**:
   - Read and follow the guidance in the reference file
   - Apply the documented fix patterns to resolve the EWI
   - After successfully resolving the issue, update the reference file with any new learnings, edge cases, or patterns discovered

3. **If the reference does not exist**:
   - Resolve the EWI using your knowledge of SQL Server and Snowflake
   - After successfully resolving the issue, create a new reference file (e.g., `reference/SSC-EWI-XXXX.md`)
   - Document the problem, fix patterns, examples, and any important considerations

## Reference File Structure

Each reference file should follow this structure:

```markdown
# SSC-EWI-XXXX - Brief Description

Brief explanation of what this EWI means and why it occurs.

## Quick Reference

| SQL Server | Snowflake |
|------------|-----------|
| Original syntax | Converted syntax |

## Identification

How to identify this EWI in code (markers, patterns).

## Fix Process

Step-by-step process to resolve the EWI.

## Examples

### Before
```sql
-- Invalid/unconverted code
```

### After
```sql
-- Valid Snowflake code
```

## Key Points

- Important considerations
- Edge cases
- Common mistakes to avoid

## Resources

- Links to relevant Snowflake documentation
- Links to relevant SQL Server documentation
```

## Updating References

When updating an existing reference after resolving an EWI:

- Add new patterns or edge cases discovered
- Include additional examples if the fix was non-obvious
- Document any gotchas or pitfalls encountered
- Keep the file focused and well-organized
