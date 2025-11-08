# AGENTS.md

Context and guidelines for AI coding agents working on this dbt + Snowflake data engineering project.

## Project Context

This is a **modern data engineering project** built with dbt-core and Snowflake, implementing industry best practices for analytics engineering.

---

## Technology Stack

### Core Technologies
- **dbt-core**: data transformation framework
- **dbt-snowflake**: Snowflake adapter for dbt
- **Snowflake**: Relational database
- **Streamlit in Snowflake**:  Preferred graphical user interface (if needed)
- **Schemachange**: CI/CD for database objects outside dbt
- **Python**: 3.11+ with Snowpark for advanced analytics and ML models

**Version Compatibility**: dbt versions should align with [dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake#dbt-projects) requirements (dbt-core 1.9.4, dbt-snowflake 1.9.2)

### Key dbt Packages
- **dbt_constraints**: Database-level constraint enforcement (primary keys, foreign keys)
- **dbt_utils**: Utility macros and helper functions for common transformations
- **dbt_artifacts**: dbt logging to Snowflake database tables

### Development Tools
- **Snowflake CLI (`snow` command)**:  Execution of database commands and scripts
- **dbt Projects on Snowflake**: Preferred execution environment when not developing locally
- **conda and uv**: Preferred Python package managers
- **schemachange**: Preferred CI/CD deployment tool for non-dbt objects (procedures, UDF, tasks, etc.)
- **Taskmaster AI**: Task-driven development workflow management
- **Git**: Version control with feature branch strategy
- **Playwright**: Testing GUI applications

---

## Agent Guidelines and Constraints

### Code Standards
- **Consistency** - Follow established patterns across the project
- **Testability** - Models should have appropriate data quality tests
- **Documentation** - Document business logic, complex transformations, models, and columns

### Legacy Rules (Cursor-specific)

For Cursor IDE integration, see `.cursor/rules/`:
- **[dbt.mdc](.cursor/rules/dbt.mdc)** - Complete dbt modeling guidelines
- **[dbt-observability.mdc](.cursor/rules/dbt-observability.mdc)** - Original observability guide
- **[snowflake-cli.mdc](.cursor/rules/snowflake-cli.mdc)** - Snowflake operations
- **[streamlit.mdc](.cursor/rules/streamlit.mdc)** - Streamlit development
- **[playwright.mdc](.cursor/rules/playwright.mdc)** - Browser testing
- **[schemachange.mdc](.cursor/rules/schemachange.mdc)** - Database migrations

---

### Safety and permissions

#### Allowed without prompt:
- read files, list files
- reformat SQL
- executing dbt models
- query Snowflake database

#### Ask first: 
- Adding dbt macros, dbt packages, or python libraries
- git push
- deleting files, chmod

### Security Requirements
- **Never hardcode credentials** - Always use configuration files or environment variables

### Performance Guidelines  
- **Use incremental materialization** for data pipelines with many rows
- **Apply appropriate clustering keys** for frequently queried columns
- **Size warehouses** based on execution time and model complexity

### Testing Requirements
- **Use `dbt build` instead of `dbt run`** to run dbt tests after model execution (`dbt build --select modelname`)
- **Use dbt_constraints** for primary/unique/foreign key validation

### Deployment Process
- **Test connection** with `dbt debug` before deployment
- **Deploy to dev, test, prod using Python script** with `python deploy_dbt_project.py --target environment_name`
- **Validate in production** with `dbt build --target prod`

---

## Specification-Driven Development Process

This project follows **Specification-Driven Development (SDD)** methodology, where a detailed, often executable, specification serves as the blueprint for development, testing, and documentation. This approach ensures stakeholder alignment, improves code quality, and enables efficient development cycles.

### Core SDD Principles
- **Early Specification Definition** - Clear requirements, objectives, and constraints upfront
- **Stakeholder Collaboration** - Engage all parties to align with business goals
- **Iterative Refinement** - Continuously update specifications based on feedback
- **Traceability** - Maintain clear links between specifications and implementation
- **Test-First Approach** - Define validation criteria before implementation

### Development Workflow

#### **Phase 1: Define the Functional and Technical Specifications**
1. **Gather Requirements** - Start with user stories or high-level requirements
   - Create comprehensive requirements, plans, and tasks in a PRD markdown document
   - Define functional requirements and design goals
   - Document business logic and transformation requirements
   - Specify acceptance criteria and validation requirements

2. **Write Clear Specs** - Document specifications in structured format
   - Use natural language that is easy for technology architects and engineers to review
   - Define data models, APIs, interfaces, and system behavior
   - Outline performance and scalability requirements
   - Establish quality and testing standards

3. **Validate Specifications** - Collaborate with stakeholders for approval
   - Validate business alignment and technical feasibility
   - Ensure completeness and clarity of specifications
   - Approve scope and acceptance criteria
   - Confirm specifications align with business needs

#### **Phase 2: Design and Plan**
4. **Research** - Research on the web to understand implementation approaches
   - Research current best practices and patterns
   - Validate technical approaches against requirements
   - Gather implementation context and examples
   - Identify architectural patterns and technology choices

5. **Architectural Design** - Develop the technical solutions
   - Expand our PRD to include the design for system architecture and process logic
   - Define technology stack and integration patterns
   - Plan data flow and system interactions
   - Document technical design decisions in the PRD

6. **Parse and Break Down** - Generate tasks from specifications
   - Automatically convert specifications into actionable tasks
   - Analyze the complexity of each task to identify complex tasks
   - Break down high/medium complexity tasks into subtasks
   - Maintain traceability between PRD requirements and implementation tasks

7. **Organize Tasks** - Set dependencies and priorities
   - Add dependencies to your tasks to establish logical task sequencing
   - Identify critical path and bottlenecks
   - Align priorities with business value and technical dependencies

#### **Phase 3: Implement and Test**
8. **Code Development** - Use list of tasks for development
   - Follow test-first development approach
   - Implement functionality defined in the specification
   - Write code to meet predefined specifications
   - Ensure code aligns with architectural design

9. **Test Generation and Execution** - Derive tests from acceptance criteria
   - Generate automated tests directly from specification criteria
   - Execute specification-based tests
   - Validate functionality against requirements
   - Ensure performance meets specified requirements

10. **Document Progress** - Log implementation decisions and findings
    - Update the PRD continueously
    - Update specifications based on learnings
    - Maintain audit trail of changes and decisions
    - Update task completion

#### **Phase 4: Iterate and Refine**
11. **Validation** - Test implementation against specification
    - Verify all acceptance criteria are met
    - Confirm specification compliance
    - Validate system behavior matches requirements

12. **Refine** - Iterate on specification, design, or implementation
    - Refine specifications if new insights arise
    - Update implementation until tests pass
    - Ensure requirements are fully met
    - Update task completion

13. **Maintain Traceability** - Keep specification as living document
    - Maintain continuous alignment throughout project lifecycle
    - Update documentation to reflect final implementation
    - Prepare for deployment and future maintenance

---

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
<!-- Generated: 2025-11-08T22:49:11.086Z -->

## MCP-Managed Skills

This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.

# Skills

**What are Skills?**

Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:
- **SKILL.md** - Core instructions and guidelines
- **references/** - Detailed documentation and examples
- **scripts/** - Helper scripts and templates
- **config/** - Configuration files

Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized "expert personas" for areas like dbt development, Snowflake operations, or testing frameworks.

**Key Features:**
- Skills can be enabled `[x]` or disabled `[ ]` individually

**Available Skills:**

### Local Skills

- [x] **[dbt-architecture](.claude/skills/dbt-architecture/SKILL.md)** - dbt project structure using medallion architecture (bronze/silver/gold layers). Use this skill when planning project organization, establishing folder structure, defining naming conventions, implementing layer-based configuration, or ensuring proper model dependencies and architectural patterns.
- [x] **[dbt-artifacts](.claude/skills/dbt-artifacts/SKILL.md)** - Monitor dbt execution using the dbt Artifacts package. Use this skill when you need to track test and model execution history, analyze run patterns over time, monitor data quality metrics, or enable programmatic access to dbt execution metadata across any dbt version or platform.
- [x] **[dbt-commands](.claude/skills/dbt-commands/SKILL.md)** - dbt command-line operations, model selection syntax, Jinja patterns, troubleshooting, and debugging. Use this skill when running dbt commands, selecting specific models, debugging compilation errors, using Jinja macros, or troubleshooting dbt execution issues.
- [x] **[dbt-core](.claude/skills/dbt-core/SKILL.md)** - Managing dbt-core locally - installation, configuration, project setup, package management, troubleshooting, and development workflow. Use this skill for all aspects of local dbt-core development including non-interactive scripts for environment setup with conda or venv, and comprehensive configuration templates for profiles.yml and dbt_project.yml.
- [x] **[dbt-materializations](.claude/skills/dbt-materializations/SKILL.md)** - Choosing and implementing dbt materializations (ephemeral, view, table, incremental, snapshots, Python models). Use this skill when deciding on materialization strategy, implementing incremental models, setting up snapshots for SCD Type 2 tracking, or creating Python models for machine learning workloads.
- [x] **[dbt-modeling](.claude/skills/dbt-modeling/SKILL.md)** - Writing dbt models with proper CTE patterns, SQL structure, and layer-specific templates. Use this skill when writing or refactoring dbt models, implementing CTE patterns, creating staging/intermediate/mart models, or ensuring proper SQL structure and dependencies.
- [x] **[dbt-performance](.claude/skills/dbt-performance/SKILL.md)** - Optimizing dbt and Snowflake performance through materialization choices, clustering keys, warehouse sizing, and query optimization. Use this skill when addressing slow model builds, optimizing query performance, sizing warehouses, implementing clustering strategies, or troubleshooting performance issues.
- [x] **[dbt-projects-on-snowflake](.claude/skills/dbt-projects-on-snowflake/SKILL.md)** - Deploying, managing, executing, and monitoring dbt projects natively within Snowflake using dbt PROJECT objects and event tables. Use this skill when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration directly in Snowflake.
- [x] **[dbt-projects-snowflake-setup](.claude/skills/dbt-projects-snowflake-setup/SKILL.md)** - Step-by-step setup guide for dbt Projects on Snowflake including prerequisites, external access integration, Git API integration, event table configuration, and automated scheduling. Use this skill when setting up dbt Projects on Snowflake for the first time or troubleshooting setup issues.
- [x] **[dbt-testing](.claude/skills/dbt-testing/SKILL.md)** - dbt testing strategies using dbt_constraints for database-level enforcement, generic tests, and singular tests. Use this skill when implementing data quality checks, adding primary/foreign key constraints, creating custom tests, or establishing comprehensive testing frameworks across bronze/silver/gold layers.
- [x] **[playwright-mcp](.claude/skills/playwright-mcp/SKILL.md)** - Browser testing, web scraping, and UI validation using Playwright MCP. Use this skill when you need to test Streamlit apps, validate web interfaces, test responsive design, check accessibility, or automate browser interactions through MCP tools.
- [x] **[schemachange](.claude/skills/schemachange/SKILL.md)** - Deploying and managing Snowflake database objects using version control with schemachange. Use this skill when you need to manage database migrations for objects not handled by dbt, implement CI/CD pipelines for schema changes, or coordinate deployments across multiple environments.
- [x] **[snowflake-cli](.claude/skills/snowflake-cli/SKILL.md)** - Executing SQL, managing Snowflake objects, deploying applications, and orchestrating data pipelines using the Snowflake CLI (snow) command. Use this skill when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, automate Snowflake operations from CI/CD pipelines, or work with variables and templating.
- [x] **[snowflake-connections](.claude/skills/snowflake-connections/SKILL.md)** - Configuring Snowflake connections using connections.toml (for Snowflake CLI, Streamlit, Snowpark) or profiles.yml (for dbt) with multiple authentication methods (SSO, key pair, username/password, OAuth), managing multiple environments, and overriding settings with environment variables. Use this skill when setting up Snowflake CLI, Streamlit apps, dbt, or any tool requiring Snowflake authentication and connection management.
- [x] **[streamlit-development](.claude/skills/streamlit-development/SKILL.md)** - Developing, testing, and deploying Streamlit data applications on Snowflake. Use this skill when you're building interactive data apps, setting up local development environments, testing with pytest or Playwright, or deploying apps to Snowflake using Streamlit in Snowflake.
- [x] **[task-master](.claude/skills/task-master/SKILL.md)** - AI-powered task management for structured, specification-driven development. Use this skill when you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies, and maintain organized development workflows across features and branches.

### github-com/anthropics-skills

- [x] **[algorithmic-art](.skills/repositories/github-com/anthropics-skills/algorithmic-art/SKILL.md)** - Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.
- [x] **[artifacts-builder](.skills/repositories/github-com/anthropics-skills/artifacts-builder/SKILL.md)** - Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
- [x] **[brand-guidelines](.skills/repositories/github-com/anthropics-skills/brand-guidelines/SKILL.md)** - Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
- [x] **[canvas-design](.skills/repositories/github-com/anthropics-skills/canvas-design/SKILL.md)** - Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.
- [x] **[docx](.skills/repositories/github-com/anthropics-skills/document-skills/docx/SKILL.md)** - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
- [x] **[internal-comms](.skills/repositories/github-com/anthropics-skills/internal-comms/SKILL.md)** - A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).
- [x] **[mcp-builder](.skills/repositories/github-com/anthropics-skills/mcp-builder/SKILL.md)** - Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
- [x] **[pdf](.skills/repositories/github-com/anthropics-skills/document-skills/pdf/SKILL.md)** - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
- [x] **[pptx](.skills/repositories/github-com/anthropics-skills/document-skills/pptx/SKILL.md)** - Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks
- [x] **[skill-creator](.skills/repositories/github-com/anthropics-skills/skill-creator/SKILL.md)** - Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
- [x] **[slack-gif-creator](.skills/repositories/github-com/anthropics-skills/slack-gif-creator/SKILL.md)** - Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints and composable animation primitives. This skill applies when users request animated GIFs or emoji animations for Slack from descriptions like "make me a GIF for Slack of X doing Y".
- [x] **[template-skill](.skills/repositories/github-com/anthropics-skills/template-skill/SKILL.md)** - Replace with description of the skill and when Claude should use it.
- [x] **[theme-factory](.skills/repositories/github-com/anthropics-skills/theme-factory/SKILL.md)** - Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.
- [x] **[webapp-testing](.skills/repositories/github-com/anthropics-skills/webapp-testing/SKILL.md)** - Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
- [x] **[xlsx](.skills/repositories/github-com/anthropics-skills/document-skills/xlsx/SKILL.md)** - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas

<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
