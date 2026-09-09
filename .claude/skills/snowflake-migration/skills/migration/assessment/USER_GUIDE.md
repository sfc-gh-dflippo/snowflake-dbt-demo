# SnowConvert Assessment Skill - User Guide

> **Internal Review Document** - Draft for public documentation

This guide helps users understand how to effectively use the SnowConvert Assessment Skill to analyze their migration workload and create deployment plans.

## Overview

The SnowConvert Assessment Skill analyzes your database migration workload using SnowConvert output files. It helps you:

- **Plan deployment waves** - Organize objects into deployment sequences that respect dependencies
- **Identify exclusions** - Find temporary, staging, and deprecated objects that may not need migration
- **Surface migration anti-patterns** - Group SnowConvert findings into performance, architecture/security, and behavior/semantic risk buckets (SQL Server)
- **Analyze complexity** - Assess Dynamic SQL patterns and SSIS packages for migration effort
- **Generate reports** - Create interactive HTML reports for stakeholders

## What You Can Do

This skill is designed for interactive use:

| Capability | Description |
|------------|-------------|
| 📊 **View Reports** | After analysis, an interactive HTML report is generated that you can explore |
| 🔄 **Iterate & Refine** | Ask to adjust results - change wave sizes or prioritize objects |
| 🎯 **Set Goals Upfront** | Specify your preferences before analysis (e.g., number of waves, priority objects) |

## Getting Started

### Prerequisites

Before using this skill, ensure you have:

1. **SnowConvert output files** from a completed assessment:
   - `ObjectReferences.csv` - Object dependencies
   - `TopLevelCodeUnits.csv` - Object metadata
   - `Issues.csv` - For Dynamic SQL analysis (optional)
   - `ETL.Elements.csv` and `ETL.Issues.csv` - For SSIS analysis (optional)

2. **Python 3.11+** installed

3. **uv package manager** installed

### What to Expect

When you invoke the skill, it will:

1. **Show a welcome message** explaining what you can do
2. **Confirm your request** before running any analysis
3. **Ask for details** if needed (paths, goals, preferences)

### Quick Start

Start by invoking the skill:

```
use skill assessment
```

The skill will greet you and ask for:
- Path to your SnowConvert reports directory
- Output directory for results
- Any specific goals or preferences

## Example Prompts

### Starting an Assessment

```
Run a comprehensive assessment with all analyses
```

```
Analyze my SnowConvert reports at /path/to/Reports
```

```
Start fresh analysis (don't reuse previous results)
```

### Setting Goals Upfront

**Limit Number of Waves:**
```
I want a maximum of 5 deployment waves
```

```
Create 3-4 deployment waves for easier rollout
```

**Control Wave Size:**
```
Waves should have 20-30 objects each
```

```
I need smaller batches - maximum 15 objects per wave
```

**Prioritize Objects:**
```
Prioritize all Payroll-related objects in Wave 1
```

```
Put all Customer* objects in the earliest waves
```

```
I need PKG_PAYROLL, PKG_HR, and PKG_FINANCE deployed first
```

### Refining Results After Analysis

Once you have initial results, you can refine them:

**Relocate Objects:**
```
Move dbo.CriticalTable to Wave 1
```

```
Relocate all reporting procedures to Wave 5
```

**Investigate Dependencies:**
```
Show me which objects have circular dependencies
```

```
What objects are blocking the migration?
```

```
Which objects depend on dbo.LegacyTable?
```

**Regenerate with Changes:**
```
Regenerate waves with smaller batch sizes
```

```
Redo the analysis excluding the Staging schema
```

### Working with Reports

**Generate Report:**
```
Generate the HTML report
```

**Query Results:**
```
How many objects are flagged for exclusion?
```

```
What's the breakdown by schema?
```

```
Show me a summary of the assessment
```

### Specific Analyses

**Object Exclusion:**
```
Identify temporary and staging objects
```

```
Find deprecated objects that can be excluded
```

**Anti-Patterns (SQL Server):**
```
Show me the migration anti-patterns in my workload
```

**Dynamic SQL:**
```
Analyze Dynamic SQL patterns in my codebase
```

**SSIS/ETL:**
```
Assess my SSIS packages for migration complexity
```

## Tips for Best Results

### 1. Specify Goals Upfront

Instead of using defaults and refining later, tell the skill what you want:

❌ Less efficient:
```
Generate waves
```
Then: `Make the waves smaller`
Then: `Prioritize Payroll objects`

✅ More efficient:
```
Generate waves with 20-30 objects each, prioritizing all Payroll-related objects
```

### 2. Use Patterns for Prioritization

The skill supports wildcards for object selection:

| Pattern | Matches |
|---------|---------|
| `*Payroll*` | Any object containing "Payroll" |
| `PKG_*` | Objects starting with "PKG_" |
| `dbo.Customer*` | Objects in dbo schema starting with "Customer" |
| `*_Archive` | Objects ending with "_Archive" |

### 3. Understand Wave Ordering

By default, waves are organized by object category:
1. **TABLEs** - Deployed first (schema foundation)
2. **VIEWs** - Second (depend on tables)
3. **FUNCTIONs** - Third
4. **PROCEDUREs** - Fourth
5. **ETL/SSIS Packages** - Last (consume everything else)

If you prefer pure dependency-based ordering (mixing all types), ask:
```
Use dependency-based ordering instead of category-based
```

### 4. Iterate on Results

After the initial analysis, you can:

- **View the report** to understand the results
- **Ask questions** about specific findings
- **Request changes** like relocating objects or adjusting wave sizes
- **Regenerate** with different parameters

The skill maintains context, so you don't need to start over.

## Understanding the Output

### HTML Report

The generated HTML report opens on the **Migration Journey** page. For SQL Server,
**Discovery** appears next, followed by the conversion tabs grouped under
**Code/ETL Conversion** and the later migration phases. Most tabs appear only when
the report has data to fill them. Discovery is SQL Server only: with an Extended
Events capture it shows observed volume and executions; without one the tab stays
and walks through starting a capture, copying `.xel` files, and re-running the
assessment. Other dialects omit the tab entirely.

| Tab | Contents |
|-----|----------|
| **Migration Journey** | Landing page — what each phase of your migration involves, one card per phase |
| **Discovery** | SQL Server Extended Events volume, duration mix, statement types, applications, users, long-running executions, and errors. No capture yet: how-to for the starter session + re-run. Hidden on other dialects. |
| **Waves** | Deployment sequence with objects per wave, dependencies |
| **Object Exclusion** | Temporary, staging, deprecated objects identified |
| **Anti-Patterns** | Performance, architecture/security, and behavior/semantic findings grouped by priority (SQL Server) |
| **Dynamic SQL** | Patterns found with complexity scores |
| **SSIS** | Package classifications and migration effort |
| **Effort Estimates** | Hours for code conversion and testing, priced per object by complexity, plus workload tier and phase budgets. Editable — change an hours-per-object rate and every total updates (SQL Server and Redshift) |
| **Data Migration & Validation** | Data type coverage for your source platform, per-table readiness, topology and validation guidance, plus reviewed inventory SQL (SQL Server and Redshift) |
| **Testing** | Procedure/function and ETL readiness ladders — what is testable now, and what each object still needs first |

### Key Metrics

- **Total Objects** - Number of objects in the migration
- **Waves/Partitions** - Number of deployment batches
- **Exclusion Candidates** - Objects that may not need migration
- **Circular Dependencies** - Objects with mutual dependencies (require attention)

## Troubleshooting

### "I want different wave sizes"

Specify min and max sizes:
```
Regenerate waves with minimum 15 and maximum 30 objects per wave
```

### "Important objects are in late waves"

Use prioritization:
```
Prioritize *CriticalProcess* objects to appear in Wave 1
```

### "I have too many waves"

Increase wave size:
```
Regenerate with larger waves - 60-100 objects each
```

### "Objects with circular dependencies"

Review the `sccs` section of `waves_analysis_<timestamp>.json` and consider:
- Schema refactoring
- Deploying circular dependency groups together
- Manual intervention for complex cases

## FAQ

**Q: Can I run just one analysis (e.g., only waves)?**
A: Yes! Ask for the specific analysis: "Just generate deployment waves"

**Q: How do I update the analysis after code changes?**
A: Re-run the analysis with updated SnowConvert reports, or say "Start fresh analysis"

**Q: Can I export the data?**
A: Yes, the HTML report includes CSV/Excel export options

**Q: What if I disagree with object exclusion recommendations?**
A: The exclusions are recommendations - you decide what to actually exclude

**Q: How do I handle objects the skill can't categorize?**
A: Review them manually - the skill flags uncertain items for your review
