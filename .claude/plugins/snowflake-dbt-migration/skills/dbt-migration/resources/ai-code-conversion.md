# AI Code Conversion

AI-powered code conversion strengthens the migration process by using AI agents to validate and
repair converted database code through automated functional testing.

## Overview

After SnowConvert AI performs deterministic code conversion (which may surface EWIs and FDMs for
issues it cannot automatically resolve), AI Code Conversion reduces manual remediation effort by:

- Generating synthetic test data
- Creating AI-driven unit tests
- Suggesting patches to produce consistent results between legacy and Snowflake systems

## Key Features

- **Accelerated AI validation**: Reduce time spent on manual testing
- **Automated test generation**: Creates test cases based on existing queries and business logic
- **Agentic repair suggestions**: Suggests code patches to fix identified issues

## Conversion Status Types

| Status                   | Description                      |
| ------------------------ | -------------------------------- |
| Verified                 | Code validated successfully      |
| Fixed with AI            | AI suggested and applied repairs |
| Could not verify         | Requires manual review           |
| Error in original object | Issue exists in source code      |

## Prerequisites

- SnowConvert AI installed
- Snowflake account designated for testing (not production)
- Role with CREATE DATABASE and CREATE MIGRATION privileges
- Cortex AI enabled with `claude-4-sonnet` model
- PUBLIC role should not have access to production data

## Cost Considerations

AI Code Conversion consumes Snowflake credits through:

- Cortex AI SQL functions
- Warehouse compute for test queries
- Stage storage for inputs/outputs
- Snowpark Container Services (compute pools named `AI_MIGRATOR_*`)

## Limitations

- Optimized for SQL Server migrations
- All AI-generated changes require customer review before deployment

## Documentation

- [AI Code Conversion Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/snowconvert-ai-verification)
- [Two-Sided Verification](https://docs.snowflake.com/en/migrations/snowconvert-docs/ai-verification/snowconvert-ai-twosided-verification)
