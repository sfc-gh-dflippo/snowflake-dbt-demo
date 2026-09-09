---
name: basic-support
description: Post-conversion guidance for code-conversion-only dialects (Sybase, Spark, BigQuery, etc.). Offers deployment and next-step options. For full-migration sources (SQL Server, Redshift, Oracle, Teradata), use [migrate-objects](./SKILL.md) instead.
parent_skill: migrate-objects
license: Proprietary. See License-Skills for complete terms
---

# Basic Support — Post-Conversion

Your conversion is complete! The converted code is ready in the `snowflake/` directory. Would you like to:

1. **Deploy** — deploy converted objects to Snowflake
2. **Something else** — tell me what you need

If the user chooses **Deploy**, run `scai code deploy -c <snowflake_connection> --json` from the project directory. Present the results and ask what to do next.

If the user chooses **Something else**, follow their instructions.

Return to the parent [SKILL.md](./SKILL.md) after handling the user's choice.
