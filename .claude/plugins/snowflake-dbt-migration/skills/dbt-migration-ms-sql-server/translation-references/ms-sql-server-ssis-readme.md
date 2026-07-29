---
description: Translation specification for SQL Server Integration Services (SSIS) to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/ssis/README
title: SSIS to Snowflake Translation Reference
---

## SSIS to Snowflake Translation Reference

This directory contains translation references for migrating SQL Server Integration Services (SSIS)
packages to Snowflake-compatible workflows.

## Overview

SSIS packages can be migrated to Snowflake using several approaches:

1. **dbt models** - Transform SSIS data flow logic into dbt models
2. **Snowflake Tasks** - Schedule and orchestrate transformations
3. **Snowpark Python** - Complex transformation logic
4. **External orchestration** - Airflow, dbt Cloud, or other tools

Refer to the Snowflake Migration Accelerator for detailed SSIS migration guidance.
