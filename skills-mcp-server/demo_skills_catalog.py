#!/usr/bin/env python3
"""
Quick demo to show what skills catalog the MCP server will return to agents.
This simulates what agents will see when they connect to the server.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_catalog():
    """Show a sample skills catalog based on known skills in the repos."""
    
    print("=" * 80)
    print("SKILLS CATALOG - As Returned by MCP Server to Agents")
    print("=" * 80)
    print()
    print("This is what agents will see in their context when they connect.")
    print("The catalog lists all available skills from configured repositories.")
    print()
    print("=" * 80)
    print()
    
    # Based on the actual skills in your repositories
    catalog = """# Available Skills

The following skills are available for use. To load a skill, reference its URI.

## Skills from sfc-gh-dflippo-snowflake-dbt-demo

### dbt-architecture
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-architecture`  
**Description:** dbt project structure using medallion architecture (bronze/silver/gold layers). Use this skill when planning project organization, establishing folder structure, defining naming conventions, implementing layer-based configuration, or ensuring proper model dependencies and architectural patterns.
**Resources:** 0 files available

### dbt-artifacts
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-artifacts`  
**Description:** Monitor dbt execution using the dbt Artifacts package. Use this skill when you need to track test and model execution history, analyze run patterns over time, monitor data quality metrics, or enable programmatic access to dbt execution metadata across any dbt version or platform.
**Resources:** 0 files available

### dbt-commands
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-commands`  
**Description:** dbt command-line operations, model selection syntax, Jinja patterns, troubleshooting, and debugging. Use this skill when running dbt commands, selecting specific models, debugging compilation errors, using Jinja macros, or troubleshooting dbt execution issues.
**Resources:** 0 files available

### dbt-core
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-core`  
**Description:** Managing dbt-core locally - installation, configuration, project setup, package management, troubleshooting, and development workflow. Use this skill for all aspects of local dbt-core development including non-interactive scripts for environment setup with conda or venv, and comprehensive configuration templates for profiles.yml and dbt_project.yml.
**Resources:** 0 files available

### dbt-materializations
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-materializations`  
**Description:** Choosing and implementing dbt materializations (ephemeral, view, table, incremental, snapshots, Python models). Use this skill when deciding on materialization strategy, implementing incremental models, setting up snapshots for SCD Type 2 tracking, or creating Python models for machine learning workloads.
**Resources:** 0 files available

### dbt-modeling
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-modeling`  
**Description:** Writing dbt models with proper CTE patterns, SQL structure, and layer-specific templates. Use this skill when writing or refactoring dbt models, implementing CTE patterns, creating staging/intermediate/mart models, or ensuring proper SQL structure and dependencies.
**Resources:** 0 files available

### dbt-performance
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-performance`  
**Description:** Optimizing dbt and Snowflake performance through materialization choices, clustering keys, warehouse sizing, and query optimization. Use this skill when addressing slow model builds, optimizing query performance, sizing warehouses, implementing clustering strategies, or troubleshooting performance issues.
**Resources:** 0 files available

### dbt-projects-on-snowflake
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-projects-on-snowflake`  
**Description:** Deploying, managing, executing, and monitoring dbt projects natively within Snowflake using dbt PROJECT objects and event tables. Use this skill when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration directly in Snowflake.
**Resources:** 0 files available

### dbt-testing
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/dbt-testing`  
**Description:** dbt testing strategies using dbt_constraints for database-level enforcement, generic tests, and singular tests. Use this skill when implementing data quality checks, adding primary/foreign key constraints, creating custom tests, or establishing comprehensive testing frameworks across bronze/silver/gold layers.
**Resources:** 0 files available

### snowflake-cli
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/snowflake-cli`  
**Description:** Executing SQL, managing Snowflake objects, deploying applications, and orchestrating data pipelines using the Snowflake CLI (snow) command. Use this skill when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, automate Snowflake operations from CI/CD pipelines, or work with variables and templating.
**Resources:** 0 files available

### task-master
**URI:** `skill://sfc-gh-dflippo-snowflake-dbt-demo/task-master`  
**Description:** AI-powered task management for structured, specification-driven development. Use this skill when you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies, and maintain organized development workflows across features and branches.
**Resources:** 0 files available

## Skills from anthropics-skills

### algorithmic-art
**URI:** `skill://anthropics-skills/algorithmic-art`  
**Description:** Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.
**Resources:** Multiple script and reference files available

### artifacts-builder
**URI:** `skill://anthropics-skills/artifacts-builder`  
**Description:** Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
**Resources:** Multiple reference and script files available

### mcp-builder
**URI:** `skill://anthropics-skills/mcp-builder`  
**Description:** Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
**Resources:** Multiple reference files (best practices, examples, evaluation scripts) available

### skill-creator
**URI:** `skill://anthropics-skills/skill-creator`  
**Description:** Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
**Resources:** Reference documentation available

And more skills from Anthropic's repository...
"""
    
    print(catalog)
    print()
    print("=" * 80)
    print("USAGE EXAMPLES")
    print("=" * 80)
    print()
    print("1. Agent sees catalog automatically in context")
    print("2. Agent decides which skill to use based on task")
    print("3. Agent loads skill: skill://anthropics-skills/mcp-builder")
    print("4. Agent receives raw SKILL.md content")
    print("5. Agent can access resources: skill://anthropics-skills/mcp-builder/resource/scripts/evaluation.py")
    print()
    print("=" * 80)
    print("MCP TOOLS AVAILABLE")
    print("=" * 80)
    print()
    print("list_skills(filter_repo=None)")
    print("  - Lists all skills with name, description, repo, URI, resource count")
    print()
    print("get_skill_resources(skill_name)")
    print("  - Lists all resources for a specific skill")
    print()
    print("refresh_repositories(repo_name=None)")
    print("  - Re-downloads and syncs repositories to get latest skills")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demo_catalog()


