# Migration Assistant (VS Code Extension)

The SnowConvert AI Migration Assistant is an AI-powered VS Code extension for resolving errors,
warnings, and issues (EWIs) encountered after converting SQL code with SnowConvert.

## Overview

Integrated within the Snowflake Visual Studio Code extension, the Migration Assistant provides an
interactive workflow for navigating, understanding, and fixing EWIs that SnowConvert AI cannot
automatically resolve.

## Key Features

- **AI-driven EWI analysis**: Uses Snowflake Cortex AI via REST API
- **Root cause explanations**: Understand why conversion issues occurred
- **Actionable solutions**: Get specific recommendations for fixes
- **Chat interaction**: Ask questions about SQL-related topics
- **Seamless VS Code integration**: Works within your existing development environment

## Supported Sources

The Migration Assistant is optimized for **SQL Server** migrations. It works with all SnowConvert AI
supported databases, with optimization for additional sources planned for future releases.

## Prerequisites

- Snowflake VS Code extension installed
- Signed in to your Snowflake account
- Access to SNOWFLAKE.CORTEX.COMPLETE
- Access to at least one supported Cortex model
- Optional:
  [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)
  if preferred models aren't available in your region

## Important Notes

- Large language models can make mistakes - always review and validate suggestions before
  implementing
- The assistant uses Snowflake Cortex AI which requires appropriate account access

## Documentation

- [Migration Assistant Overview](https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/README)
- [Getting Started](https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/getting-started)
- [Troubleshooting](https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/troubleshooting)
- [Model Preferences](https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/model-preference)
