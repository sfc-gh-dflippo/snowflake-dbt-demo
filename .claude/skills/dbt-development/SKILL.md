---
name: dbt Development
description: Expert guidance for dbt data modeling using medallion architecture (bronze/silver/gold), with testing strategies, performance best practices, and development workflows. Use this skill when designing models, choosing materializations, implementing tests, or optimizing dbt projects. Runtime agnostic - works with dbt Cloud, dbt Core, or any execution environment.
---

# dbt Development - AI Instructions

## Purpose

This skill transforms AI agents into an expert dbt data engineer and architect, providing comprehensive guidance on building production-grade data models following industry best practices for medallion architecture, testing, and performance optimization across all dbt execution platforms.

## When to Use This Skill

Activate this skill when users ask about:
- Designing dbt models and choosing materializations
- Implementing medallion architecture (bronze/silver/gold layers)
- Setting up testing strategies and data quality checks
- Optimizing dbt performance and query execution
- Establishing naming conventions and project structure
- Writing Jinja templates and custom macros
- Implementing incremental models and snapshots
- Using Python models for machine learning
- Troubleshooting dbt builds and performance issues
- Configuring dbt_project.yml and folder-level settings

**Note:** For platform-specific deployment (dbt Projects on Snowflake), use the `dbt-projects-snowflake` skill instead.

## Core Philosophy

**Medallion Architecture + Best Practices Integration**

Medallion architecture demonstrates how dbt best practices seamlessly integrate with a layered data approach:

- **Bronze Layer** = **Staging Models** (`stg_`) - One-to-one source relationships
- **Silver Layer** = **Intermediate Models** (`int_`) - Business logic transformations
- **Gold Layer** = **Marts** (`dim_`, `fct_`) - Business-ready data products

Every recommendation follows both architectural principles and dbt best practices simultaneously.

## Medallion Architecture Quick Reference

### Three Layers

**Bronze (Staging):**
- Naming: `stg_{source}__{table}`
- Materialization: `ephemeral`
- Purpose: One-to-one source cleaning
- Rules: No joins, no business logic

**Silver (Intermediate):**
- Naming: `int_{entity}__{description}`
- Materialization: `ephemeral` or `table`
- Purpose: Business logic, enrichment
- Rules: No direct source references

**Gold (Marts):**
- Naming: `dim_{entity}` or `fct_{process}`
- Materialization: `table` or `incremental`
- Purpose: Business-ready data products
- Rules: Fully tested, documented, optimized

**Reference**: `references/PROJECT_STRUCTURE.md` for complete patterns and examples

## Helping Users with dbt Development

### Strategy for Assisting Users

When users ask for help with dbt:

1. **Identify the layer**: Which medallion layer (bronze/silver/gold)?
2. **Choose materialization**: Based on purpose, size, and reusability
3. **Apply naming conventions**: Follow `stg_`, `int_`, `dim_`, `fct_` patterns
4. **Reference appropriate guide**: Point to specific reference documentation
5. **Provide working examples**: Show complete, tested code patterns

### Common User Tasks

#### Task 1: "Help me create a staging model"

**Response Pattern:**
1. Confirm source information (database, schema, table)
2. Apply naming convention: `stg_{source}__{table}`
3. Recommend `ephemeral` materialization
4. Provide template with source macro
5. Add basic tests (primary key, not_null)

**Reference**: Point to `references/STAGING_MODELS.md`

#### Task 2: "How do I make this model incremental?"

**Response Pattern:**
1. Assess model size and update patterns
2. Recommend incremental strategy (merge, append, delete+insert)
3. Help identify unique_key
4. Provide is_incremental() logic
5. Add performance optimizations (clustering, partitioning)

**Reference**: Point to `references/INCREMENTAL_MODELS.md`

#### Task 3: "What tests should I add?"

**Response Pattern:**
1. Start with dbt_constraints for database-level enforcement
2. Add primary key tests to all dimensions
3. Add foreign key tests to all facts
4. Include business rule tests
5. Set up data quality validations

**Reference**: Point to `references/TESTING_STRATEGY.md`

#### Task 4: "How do I optimize performance?"

**Response Pattern:**
1. Check materialization choices
2. Add clustering keys for large tables
3. Review warehouse sizing
4. Optimize incremental logic
5. Use explain plans for complex queries

**Reference**: Point to `references/PERFORMANCE_OPTIMIZATION.md`

#### Task 5: "How should I structure my project?"

**Response Pattern:**
1. Explain medallion architecture layers
2. Show folder organization by layer
3. Demonstrate model dependencies flow
4. Provide naming convention standards
5. Show configuration strategy (folder-level first)

**Reference**: Point to `references/PROJECT_STRUCTURE.md`

## Reference Documentation Structure

### Core References

- **`references/PROJECT_STRUCTURE.md`** - Medallion architecture, folder organization, dependencies
- **`references/NAMING_CONVENTIONS.md`** - Model, column, and file naming standards
- **`references/MATERIALIZATIONS.md`** - Choosing ephemeral, view, table, incremental
- **`references/STAGING_MODELS.md`** - Bronze layer staging patterns
- **`references/INTERMEDIATE_MODELS.md`** - Silver layer transformation patterns
- **`references/MARTS_MODELS.md`** - Gold layer dimension and fact patterns
- **`references/TESTING_STRATEGY.md`** - dbt_constraints, generic, singular tests
- **`references/INCREMENTAL_MODELS.md`** - Incremental strategies, is_incremental() patterns
- **`references/PERFORMANCE_OPTIMIZATION.md`** - Clustering, warehouses, query optimization
- **`references/JINJA_MACROS.md`** - Jinja templating, custom macros, loops
- **`references/PYTHON_MODELS.md`** - Python models for ML and advanced analytics
- **`references/SNAPSHOTS.md`** - SCD Type 2, historical tracking
- **`references/SETUP_GUIDE.md`** - Installation across all platforms
- **`references/QUICK_REFERENCE.md`** - Command cheatsheet, common patterns

### Using References Effectively

**When users ask general questions:**
- Provide direct answers with code examples
- Reference specific sections of documentation
- Link to complete guides for deeper learning

**When users need comprehensive guidance:**
- Direct them to the appropriate reference file
- Explain which sections are most relevant
- Offer to walk through specific examples

**When users face issues:**
- Provide immediate troubleshooting steps
- Reference debugging sections in guides
- Offer to review their specific code

## Best Practices to Always Follow

### Critical Rules

1. ✅ **No Direct Joins to Source** - All models reference staging, not sources
2. ✅ **Proper Staging Layer** - One-to-one relationship with sources
3. ✅ **No Source Fanout** - Each source has exactly one staging model
4. ✅ **Clear Dependencies** - Staging → Intermediate → Marts
5. ✅ **Standardized Naming** - Use `stg_`, `int_`, `dim_`, `fct_` prefixes
6. ✅ **Use ref() and source()** - No hard-coded table references

### Configuration Strategy

**Folder-Level First** (reduces repetition):
- Configure common settings in `dbt_project.yml`
- Apply to entire folders (bronze, silver, gold)
- Set materialization, tags, schemas at folder level

**Model-Level Only for Unique Settings**:
- Override folder defaults when needed
- Add incremental-specific configs
- Set clustering, warehouse, or other special options

**Reference**: `references/PROJECT_STRUCTURE.md` for configuration examples

### Testing Hierarchy

1. **Primary Keys** - `dbt_constraints.primary_key` (database-enforced)
2. **Foreign Keys** - `dbt_constraints.foreign_key` (referential integrity)
3. **Unique Keys** - `dbt_constraints.unique_key` (business keys)
4. **Business Rules** - Custom tests for domain validation
5. **Data Quality** - Completeness, accuracy, consistency checks

**Reference**: `references/TESTING_STRATEGY.md` for comprehensive testing guide

## Model Templates

For complete code examples and templates, see:
- **Staging models**: `references/STAGING_MODELS.md`
- **Intermediate models**: `references/INTERMEDIATE_MODELS.md`
- **Dimension models**: `references/MARTS_MODELS.md`
- **Fact models**: `references/MARTS_MODELS.md`
- **Incremental models**: `references/INCREMENTAL_MODELS.md`

## Troubleshooting Quick Tips

### Common Issues
- **Compilation Errors**: Use `dbt compile --select model_name --debug`
- **Performance**: Check materialization, clustering, warehouse sizing
- **Test Failures**: Use `dbt test --store-failures` to analyze
- **Connections**: Run `dbt debug` to verify configuration

**Reference**: `references/QUICK_REFERENCE.md` for detailed troubleshooting

## Advanced Guidance

### When to Use Python Models

Use Python models for:
- Machine learning and clustering
- Complex statistical analysis
- Data science workflows
- Advanced transformations beyond SQL
- Integration with pandas, scikit-learn, etc.

Reference: `references/PYTHON_MODELS.md`

### When to Use Snapshots

Use snapshots for:
- SCD Type 2 historical tracking
- Auditing dimension changes
- Time-series analysis
- Regulatory compliance
- Historical point-in-time analysis

Reference: `references/SNAPSHOTS.md`

### When to Use Incremental Models

Use incremental models for:
- Large fact tables (millions+ rows)
- Append-only or merge update patterns
- Time-series data
- Event logs and clickstreams
- Performance optimization

Reference: `references/INCREMENTAL_MODELS.md`

## Essential Commands Reference

```bash
# Setup & Debugging
dbt deps                              # Install packages
dbt debug                             # Test connection
dbt clean                             # Clear compiled files

# Development
dbt compile --select model_name      # Compile SQL
dbt build --select model_name        # Run + test model
dbt run --select +model_name+        # Run with dependencies

# Production
dbt build --target prod               # Build for production
dbt test --target prod                # Test production
dbt docs generate --static            # Generate docs
```

**Reference**: `references/QUICK_REFERENCE.md` for complete command reference

---

**Goal**: Transform AI agents into expert dbt practitioners who guide users through dbt development with confidence, clarity, and production-ready solutions.
