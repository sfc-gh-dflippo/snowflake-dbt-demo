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
- **Streamlit in Snowflake**: Preferred graphical user interface (if needed)
- **Schemachange**: CI/CD for database objects outside dbt
- **Python**: 3.11+ with Snowpark for advanced analytics and ML models

**Version Compatibility**: dbt versions should align with [dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake#dbt-projects) requirements (dbt-core 1.9.4, dbt-snowflake 1.9.2)

### Key dbt Packages

- **dbt_constraints**: Database-level constraint enforcement (primary keys, foreign keys)
- **dbt_utils**: Utility macros and helper functions for common transformations
- **dbt_artifacts**: dbt logging to Snowflake database tables

### Development Tools

- **Snowflake CLI (`snow` command)**: Execution of database commands and scripts
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

#### Allowed without prompt

- read files, list files
- reformat SQL
- executing dbt models
- query Snowflake database

#### Ask first

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

1. **Research** - Research on the web to understand implementation approaches
   - Research current best practices and patterns
   - Validate technical approaches against requirements
   - Gather implementation context and examples
   - Identify architectural patterns and technology choices

2. **Architectural Design** - Develop the technical solutions
   - Expand our PRD to include the design for system architecture and process logic
   - Define technology stack and integration patterns
   - Plan data flow and system interactions
   - Document technical design decisions in the PRD

3. **Parse and Break Down** - Generate tasks from specifications
   - Automatically convert specifications into actionable tasks
   - Analyze the complexity of each task to identify complex tasks
   - Break down high/medium complexity tasks into subtasks
   - Maintain traceability between PRD requirements and implementation tasks

4. **Organize Tasks** - Set dependencies and priorities
   - Add dependencies to your tasks to establish logical task sequencing
   - Identify critical path and bottlenecks
   - Align priorities with business value and technical dependencies

#### **Phase 3: Implement and Test**

1. **Code Development** - Use list of tasks for development
   - Follow test-first development approach
   - Implement functionality defined in the specification
   - Write code to meet predefined specifications
   - Ensure code aligns with architectural design

2. **Test Generation and Execution** - Derive tests from acceptance criteria
   - Generate automated tests directly from specification criteria
   - Execute specification-based tests
   - Validate functionality against requirements
   - Ensure performance meets specified requirements

3. **Document Progress** - Log implementation decisions and findings
   - Update the PRD continueously
   - Update specifications based on learnings
   - Maintain audit trail of changes and decisions
   - Update task completion

#### **Phase 4: Iterate and Refine**

1. **Validation** - Test implementation against specification
   - Verify all acceptance criteria are met
   - Confirm specification compliance
   - Validate system behavior matches requirements

2. **Refine** - Iterate on specification, design, or implementation
   - Refine specifications if new insights arise
   - Update implementation until tests pass
   - Ensure requirements are fully met
   - Update task completion

3. **Maintain Traceability** - Keep specification as living document
   - Maintain continuous alignment throughout project lifecycle
   - Update documentation to reflect final implementation
   - Prepare for deployment and future maintenance

---

<!-- BEGIN AVAILABLE SKILLS - AUTO-GENERATED, DO NOT EDIT MANUALLY -->

<available_skills>
<skill>
<name>
snowflake-cli
</name>
<description>
Executing SQL, managing Snowflake objects, deploying applications, and orchestrating data pipelines using the Snowflake CLI (snow) command. Use this skill when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, automate Snowflake operations from CI/CD pipelines, or work with variables and templating.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/snowflake-cli/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-commands
</name>
<description>
dbt command-line operations, model selection syntax, Jinja patterns, troubleshooting, and debugging. Use this skill when running dbt commands, selecting specific models, debugging compilation errors, using Jinja macros, or troubleshooting dbt execution issues.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-commands/SKILL.md
</location>
</skill>
<skill>
<name>
task-master-viewer
</name>
<description>
Launch a Streamlit GUI for Task Master tasks.json editing. Use when users want a visual interface instead of CLI/MCP commands.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/task-master-viewer/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-materializations
</name>
<description>
Choosing and implementing dbt materializations (ephemeral, view, table, incremental, snapshots, Python models). Use this skill when deciding on materialization strategy, implementing incremental models, setting up snapshots for SCD Type 2 tracking, or creating Python models for machine learning workloads.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-materializations/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-testing
</name>
<description>
dbt testing strategies using dbt_constraints for database-level enforcement, generic tests, and singular tests. Use this skill when implementing data quality checks, adding primary/foreign key constraints, creating custom tests, or establishing comprehensive testing frameworks across bronze/silver/gold layers.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-testing/SKILL.md
</location>
</skill>
<skill>
<name>
schemachange
</name>
<description>
Deploying and managing Snowflake database objects using version control with schemachange. Use this skill when you need to manage database migrations for objects not handled by dbt, implement CI/CD pipelines for schema changes, or coordinate deployments across multiple environments.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/schemachange/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-artifacts
</name>
<description>
Monitor dbt execution using the dbt Artifacts package. Use this skill when you need to track test and model execution history, analyze run patterns over time, monitor data quality metrics, or enable programmatic access to dbt execution metadata across any dbt version or platform.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-artifacts/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-architecture
</name>
<description>
dbt project structure using medallion architecture (bronze/silver/gold layers). Use this skill when planning project organization, establishing folder structure, defining naming conventions, implementing layer-based configuration, or ensuring proper model dependencies and architectural patterns.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-architecture/SKILL.md
</location>
</skill>
<skill>
<name>
skills-sync
</name>
<description>
Manage and synchronize AI agent skills from local SKILL.md files and remote Git repositories, generating Cursor rules with Agent Skills specification XML. This skill should be used when users need to sync skills, add/remove skill repositories, or set up the skills infrastructure.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/skills-sync/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-performance
</name>
<description>
Optimizing dbt and Snowflake performance through materialization choices, clustering keys, warehouse sizing, and query optimization. Use this skill when addressing slow model builds, optimizing query performance, sizing warehouses, implementing clustering strategies, or troubleshooting performance issues.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-performance/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-projects-on-snowflake
</name>
<description>
Deploying, managing, executing, and monitoring dbt projects natively within Snowflake using dbt PROJECT objects and event tables. Use this skill when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration directly in Snowflake.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-projects-on-snowflake/SKILL.md
</location>
</skill>
<skill>
<name>
task-master
</name>
<description>
AI-powered task management for structured, specification-driven development. Use this skill when you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies, and maintain organized development workflows across features and branches.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/task-master/SKILL.md
</location>
</skill>
<skill>
<name>
snowflake-connections
</name>
<description>
Configuring Snowflake connections using connections.toml (for Snowflake CLI, Streamlit, Snowpark) or profiles.yml (for dbt) with multiple authentication methods (SSO, key pair, username/password, OAuth), managing multiple environments, and overriding settings with environment variables. Use this skill when setting up Snowflake CLI, Streamlit apps, dbt, or any tool requiring Snowflake authentication and connection management.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/snowflake-connections/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-projects-snowflake-setup
</name>
<description>
Step-by-step setup guide for dbt Projects on Snowflake including prerequisites, external access integration, Git API integration, event table configuration, and automated scheduling. Use this skill when setting up dbt Projects on Snowflake for the first time or troubleshooting setup issues.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-projects-snowflake-setup/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-core
</name>
<description>
Managing dbt-core locally - installation, configuration, project setup, package management, troubleshooting, and development workflow. Use this skill for all aspects of local dbt-core development including non-interactive scripts for environment setup with conda or venv, and comprehensive configuration templates for profiles.yml and dbt_project.yml.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-core/SKILL.md
</location>
</skill>
<skill>
<name>
doc-scraper
</name>
<description>
Generic web scraper for extracting and organizing Snowflake documentation with intelligent caching and configurable spider depth. Install globally with uv for easy access, or use uvx for development. Scrapes any section of docs.snowflake.com controlled by --base-path.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/doc-scraper/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-modeling
</name>
<description>
Writing dbt models with proper CTE patterns, SQL structure, and layer-specific templates. Use this skill when writing or refactoring dbt models, implementing CTE patterns, creating staging/intermediate/mart models, or ensuring proper SQL structure and dependencies.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/dbt-modeling/SKILL.md
</location>
</skill>
<skill>
<name>
task-master-install
</name>
<description>
Install and initialize task-master for AI-powered task management and specification-driven development. Use this skill when users ask you to parse a new PRD, when starting a new project that needs structured task management, when users mention wanting task breakdown or project planning, or when implementing specification-driven development workflows.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/task-master-install/SKILL.md
</location>
</skill>
<skill>
<name>
streamlit-development
</name>
<description>
Developing, testing, and deploying Streamlit data applications on Snowflake. Use this skill when you&#x27;re building interactive data apps, setting up local development environments, testing with pytest or Playwright, or deploying apps to Snowflake using Streamlit in Snowflake.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/streamlit-development/SKILL.md
</location>
</skill>
<skill>
<name>
playwright-mcp
</name>
<description>
Browser testing, web scraping, and UI validation using Playwright MCP. Use this skill when you need to test Streamlit apps, validate web interfaces, test responsive design, check accessibility, or automate browser interactions through MCP tools.
</description>
<location>
/Users/dflippo/Documents/GitHub/snowflake-dbt-demo/.claude/skills/playwright-mcp/SKILL.md
</location>
</skill>
<skill>
<name>
web-artifacts-builder
</name>
<description>
Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-web-artifacts-builder/SKILL.md
</location>
</skill>
<skill>
<name>
doc-coauthoring
</name>
<description>
Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-doc-coauthoring/SKILL.md
</location>
</skill>
<skill>
<name>
workflow-design
</name>
<description>
Workflow design, state machines, process flows, and automation sequences following SDD best practices. Use when defining multi-step processes, task decomposition, state transitions, error handling flows, or automation patterns.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/workflow-design/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-testing
</name>
<description>
dbt testing strategies using dbt_constraints for database-level enforcement, generic tests, and singular tests. Use this skill when implementing data quality checks, adding primary/foreign key constraints, creating custom tests, or establishing comprehensive testing frameworks across bronze/silver/gold layers.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-testing/SKILL.md
</location>
</skill>
<skill>
<name>
pptx
</name>
<description>
Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-pptx/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-setup
</name>
<description>
Set up and configure migration environment infrastructure including tool installation, connection configuration, and environment validation. Use when initializing new migration projects or troubleshooting environment issues.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-setup/SKILL.md
</location>
</skill>
<skill>
<name>
theme-factory
</name>
<description>
Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-theme-factory/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-documentation-editor
</name>
<description>
Review, edit, and ensure consistency across technical documentation following SDD best practices. Use for quality reviews, cross-reference validation, terminology standardization, style consistency, and completeness checks.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-documentation-editor/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-commands
</name>
<description>
dbt command-line operations, model selection syntax, Jinja patterns, troubleshooting, and debugging. Use this skill when running dbt commands, selecting specific models, debugging compilation errors, using Jinja macros, or troubleshooting dbt execution issues.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-commands/SKILL.md
</location>
</skill>
<skill>
<name>
algorithmic-art
</name>
<description>
Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists&#x27; work to avoid copyright violations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-algorithmic-art/SKILL.md
</location>
</skill>
<skill>
<name>
requirements-analysis
</name>
<description>
Write user stories, acceptance criteria, success metrics, and verification strategies following SDD best practices. Use when translating product goals into testable requirements, creating machine-verifiable acceptance criteria, or writing agent stories for AI-assisted development.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/requirements-analysis/SKILL.md
</location>
</skill>
<skill>
<name>
internal-comms
</name>
<description>
A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-internal-comms/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-tools
</name>
<description>
Install and manage SQL Server to Snowflake migration tools (AI Migrator, SnowConvert AI, Snowflake CLI, Cortex Code CLI, UV, Graphviz, ODBC Driver). Use when setting up migration environments or troubleshooting installations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-tools/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-technical-writer
</name>
<description>
Write technical specifications, architecture documentation, API references, and implementation guides following SDD best practices. Use when documenting systems, creating developer guides, writing CLI references, or explaining complex technical concepts.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-technical-writer/SKILL.md
</location>
</skill>
<skill>
<name>
webapp-testing
</name>
<description>
Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-webapp-testing/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-quickstart
</name>
<description>
Deploy and configure Cortex Tasks framework in Snowflake. Use when setting up Cortex Tasks for a new project, deploying schema and MCP server, creating first features/tasks, or installing sub-agents. Covers prerequisites, deployment steps, verification, and common operations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-quickstart/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-core
</name>
<description>
Managing dbt-core locally - installation, configuration, project setup, package management, troubleshooting, and development workflow. Use this skill for all aspects of local dbt-core development including non-interactive scripts for environment setup with conda or venv, and comprehensive configuration templates for profiles.yml and dbt_project.yml.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-core/SKILL.md
</location>
</skill>
<skill>
<name>
skills-sync
</name>
<description>
Manage and synchronize AI agent skills from local SKILL.md files and remote Git repositories to AGENTS.md. This skill should be used when users need to sync skills, add/remove skill repositories, update skill catalogs, or set up the skills infrastructure in their projects.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-skills-sync/SKILL.md
</location>
</skill>
<skill>
<name>
docx
</name>
<description>
Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-docx/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-sql-review
</name>
<description>
Review and validate converted SQL code for Snowflake compatibility. Use when reviewing AI-generated conversions, fixing syntax issues, or validating SQL Server to Snowflake translations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-sql-review/SKILL.md
</location>
</skill>
<skill>
<name>
mcp-builder
</name>
<description>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-mcp-builder/SKILL.md
</location>
</skill>
<skill>
<name>
product-specification
</name>
<description>
Create strategic product specifications including executive summaries, problem statements, goals, competitive analysis, and vision documents following SDD best practices. Use when defining product strategy, articulating business value, writing executive summaries, or establishing goals and non-goals.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/product-specification/SKILL.md
</location>
</skill>
<skill>
<name>
documentation-editing
</name>
<description>
Review, edit, and ensure consistency across technical documentation following SDD best practices. Use for quality reviews, cross-reference validation, terminology standardization, style consistency, and completeness checks.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/documentation-editing/SKILL.md
</location>
</skill>
<skill>
<name>
brand-guidelines
</name>
<description>
Applies Anthropic&#x27;s official brand colors and typography to any sort of artifact that may benefit from having Anthropic&#x27;s look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-brand-guidelines/SKILL.md
</location>
</skill>
<skill>
<name>
schemachange
</name>
<description>
Deploying and managing Snowflake database objects using version control with schemachange. Use this skill when you need to manage database migrations for objects not handled by dbt, implement CI/CD pipelines for schema changes, or coordinate deployments across multiple environments.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-schemachange/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-schema-designer
</name>
<description>
Design data schemas, type systems, API contracts, and configuration formats following SDD best practices. Use when creating database schemas, JSON/YAML schemas, API request/response types, or configuration formats.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-schema-designer/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-architecture
</name>
<description>
dbt project structure using medallion architecture (bronze/silver/gold layers). Use this skill when planning project organization, establishing folder structure, defining naming conventions, implementing layer-based configuration, or ensuring proper model dependencies and architectural patterns.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-architecture/SKILL.md
</location>
</skill>
<skill>
<name>
doc-scraper
</name>
<description>
Generic web scraper for extracting and organizing Snowflake documentation with intelligent caching and configurable spider depth. Install globally with uv for easy access, or use uvx for development. Scrapes any section of docs.snowflake.com controlled by --base-path.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-doc-scraper/SKILL.md
</location>
</skill>
<skill>
<name>
playwright-mcp
</name>
<description>
Browser testing, web scraping, and UI validation using Playwright MCP. Use this skill when you need to test Streamlit apps, validate web interfaces, test responsive design, check accessibility, or automate browser interactions through MCP tools.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-playwright-mcp/SKILL.md
</location>
</skill>
<skill>
<name>
snowflake-cli
</name>
<description>
Executing SQL, managing Snowflake objects, deploying applications, and orchestrating data pipelines using the Snowflake CLI (snow) command. Use this skill when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, automate Snowflake operations from CI/CD pipelines, or work with variables and templating.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-snowflake-cli/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-github-automation
</name>
<description>
Automate GitHub operations including pull request creation, reviews, and merges for migration projects. Use when creating PRs, managing reviews, or merging completed work.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-github-automation/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-workflow-designer
</name>
<description>
Design workflows, state machines, process flows, and automation sequences following SDD best practices. Use when defining multi-step processes, task decomposition, state transitions, error handling flows, or automation patterns.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-workflow-designer/SKILL.md
</location>
</skill>
<skill>
<name>
canvas-design
</name>
<description>
Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists&#x27; work to avoid copyright violations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-canvas-design/SKILL.md
</location>
</skill>
<skill>
<name>
pdf
</name>
<description>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-pdf/SKILL.md
</location>
</skill>
<skill>
<name>
skill-creator
</name>
<description>
Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude&#x27;s capabilities with specialized knowledge, workflows, or tool integrations.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-skill-creator/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-prd-architect
</name>
<description>
Create strategic product specifications including executive summaries, problem statements, goals, competitive analysis, and vision documents following SDD best practices. Use when defining product strategy, articulating business value, or establishing goals and non-goals.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-prd-architect/SKILL.md
</location>
</skill>
<skill>
<name>
task-master
</name>
<description>
AI-powered task management for structured, specification-driven development. Use this skill when you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies, and maintain organized development workflows across features and branches.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-task-master/SKILL.md
</location>
</skill>
<skill>
<name>
snowflake-connections
</name>
<description>
Configuring Snowflake connections using connections.toml (for Snowflake CLI, Streamlit, Snowpark) or profiles.yml (for dbt) with multiple authentication methods (SSO, key pair, username/password, OAuth), managing multiple environments, and overriding settings with environment variables. Use this skill when setting up Snowflake CLI, Streamlit apps, dbt, or any tool requiring Snowflake authentication and connection management.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-snowflake-connections/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-git-workflow
</name>
<description>
Manage Git version control workflows including branching, commits, and merges for migration projects. Use when creating branches, committing changes, or managing code history.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-git-workflow/SKILL.md
</location>
</skill>
<skill>
<name>
schema-design
</name>
<description>
Database schema design, data modeling, type systems, API contracts, and configuration formats using SDD best practices. Use when designing schemas, type definitions, JSON/YAML configs, or API request/response types.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/schema-design/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-artifacts
</name>
<description>
Monitor dbt execution using the dbt Artifacts package. Use this skill when you need to track test and model execution history, analyze run patterns over time, monitor data quality metrics, or enable programmatic access to dbt execution metadata across any dbt version or platform.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-artifacts/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-playwright-automation
</name>
<description>
Automate web interactions using Playwright for migration tracking spreadsheets and object selection. Use when selecting migration objects from trackers or updating web-based tracking systems.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-playwright-automation/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-task-reviewer
</name>
<description>
Review and validate task/subtask creation following SDD best practices. Use when reviewing task structures for quality, SDD compliance, machine-verifiability, and proper skill assignment before approval. Mandatory checkpoint before marking feature/task creation complete.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-task-reviewer/SKILL.md
</location>
</skill>
<skill>
<name>
task-master-install
</name>
<description>
Install and initialize task-master for AI-powered task management and specification-driven development. Use this skill when users ask you to parse a new PRD, when starting a new project that needs structured task management, when users mention wanting task breakdown or project planning, or when implementing specification-driven development workflows.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-task-master-install/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-sdd-requirements-analyst
</name>
<description>
Write user stories, acceptance criteria, success metrics, and verification strategies following SDD best practices. Use when translating product goals into testable requirements, creating clear acceptance criteria, or writing agent stories for AI-assisted development.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-sdd-requirements-analyst/SKILL.md
</location>
</skill>
<skill>
<name>
template-skill
</name>
<description>
Replace with description of the skill and when Claude should use it.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-template-skill/SKILL.md
</location>
</skill>
<skill>
<name>
task-master-viewer
</name>
<description>
Launch a Streamlit GUI for Task Master tasks.json editing. Use when users want a visual interface instead of CLI/MCP commands.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-task-master-viewer/SKILL.md
</location>
</skill>
<skill>
<name>
slack-gif-creator
</name>
<description>
Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints and composable animation primitives. This skill applies when users request animated GIFs or emoji animations for Slack from descriptions like &quot;make me a GIF for Slack of X doing Y&quot;.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-slack-gif-creator/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-materializations
</name>
<description>
Choosing and implementing dbt materializations (ephemeral, view, table, incremental, snapshots, Python models). Use this skill when deciding on materialization strategy, implementing incremental models, setting up snapshots for SCD Type 2 tracking, or creating Python models for machine learning workloads.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-materializations/SKILL.md
</location>
</skill>
<skill>
<name>
artifacts-builder
</name>
<description>
Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-artifacts-builder/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-projects-snowflake-setup
</name>
<description>
Step-by-step setup guide for dbt Projects on Snowflake including prerequisites, external access integration, Git API integration, event table configuration, and automated scheduling. Use this skill when setting up dbt Projects on Snowflake for the first time or troubleshooting setup issues.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-projects-snowflake-setup/SKILL.md
</location>
</skill>
<skill>
<name>
technical-writing
</name>
<description>
Write technical specifications, architecture documentation, API references, and implementation guides following SDD best practices. Use when documenting systems, creating developer guides, writing CLI references, or explaining complex technical concepts.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/technical-writing/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-snowflake-testing
</name>
<description>
Execute and validate tests for converted database objects in Snowflake. Use when running compilation tests, unit tests, or validating migration results.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-snowflake-testing/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-projects-on-snowflake
</name>
<description>
Deploying, managing, executing, and monitoring dbt projects natively within Snowflake using dbt PROJECT objects and event tables. Use this skill when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration directly in Snowflake.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-projects-on-snowflake/SKILL.md
</location>
</skill>
<skill>
<name>
xlsx
</name>
<description>
Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-xlsx/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-workflow
</name>
<description>
Execute the complete SQL Server to Snowflake migration workflow using the 13-step migration process. Coordinates object selection, AI-assisted conversion, testing, validation, and deployment. Use when converting stored procedures, functions, or other database objects as part of migration projects.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-workflow/SKILL.md
</location>
</skill>
<skill>
<name>
streamlit-development
</name>
<description>
Developing, testing, and deploying Streamlit data applications on Snowflake. Use this skill when you&#x27;re building interactive data apps, setting up local development environments, testing with pytest or Playwright, or deploying apps to Snowflake using Streamlit in Snowflake.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-streamlit-development/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-performance
</name>
<description>
Optimizing dbt and Snowflake performance through materialization choices, clustering keys, warehouse sizing, and query optimization. Use this skill when addressing slow model builds, optimizing query performance, sizing warehouses, implementing clustering strategies, or troubleshooting performance issues.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-performance/SKILL.md
</location>
</skill>
<skill>
<name>
cortex-tasks-migration-jira-automation
</name>
<description>
Automate Jira ticket creation, status updates, and workflow transitions for migration tracking. Use when managing migration tickets, updating status, or querying project progress.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/cortex-tasks-migration-jira-automation/SKILL.md
</location>
</skill>
<skill>
<name>
frontend-design
</name>
<description>
Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/anthropics-skills-frontend-design/SKILL.md
</location>
</skill>
<skill>
<name>
dbt-modeling
</name>
<description>
Writing dbt models with proper CTE patterns, SQL structure, and layer-specific templates. Use this skill when writing or refactoring dbt models, implementing CTE patterns, creating staging/intermediate/mart models, or ensuring proper SQL structure and dependencies.
</description>
<location>
/Users/dflippo/.snowflake/cortex/skills/snowflake-dbt-demo-dbt-modeling/SKILL.md
</location>
</skill>
</available_skills>

<!-- END AVAILABLE SKILLS -->
