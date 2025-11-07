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

### Skills

**What are Skills?**

Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:
- **SKILL.md** - Core instructions and guidelines
- **references/** - Detailed documentation and examples
- **scripts/** - Helper scripts and templates
- **config/** - Configuration files

Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized "expert personas" for areas like dbt development, Snowflake operations, or testing frameworks.

**Key Features:**
- Skills can be enabled `[x]` or disabled `[ ]` individually
- Organized by project-specific and reference examples

---

#### Project-Specific Skills

- [x] **[dbt-artifacts](.claude/skills/dbt-artifacts/SKILL.md)** - Monitor dbt execution using the dbt Artifacts package
  - Use when you need to track test and model execution history, analyze run patterns over time, monitor data quality metrics, or enable programmatic access to dbt execution metadata
  
- [x] **[dbt-projects-on-snowflake](.claude/skills/dbt-projects-on-snowflake/SKILL.md)** - Deploy and manage dbt projects natively in Snowflake
  - Use when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration
  
- [x] **[dbt-architecture](.claude/skills/dbt-architecture/SKILL.md)** - Project structure & medallion architecture patterns
  - Use when planning project organization, establishing folder structure, defining naming conventions, or implementing layer-based configuration
  
- [x] **[dbt-modeling](.claude/skills/dbt-modeling/SKILL.md)** - Writing dbt models with proper CTE patterns and SQL structure
  - Use when writing or refactoring models, implementing CTE patterns, or creating staging/intermediate/mart models
  
- [x] **[dbt-materializations](.claude/skills/dbt-materializations/SKILL.md)** - Choosing and implementing dbt materializations
  - Use when deciding on materialization strategy, implementing incremental models, setting up snapshots, or creating Python models
  
- [x] **[dbt-testing](.claude/skills/dbt-testing/SKILL.md)** - Testing strategies with dbt_constraints and data quality checks
  - Use when implementing tests, adding primary/foreign key constraints, creating custom tests, or establishing testing frameworks
  
- [x] **[dbt-performance](.claude/skills/dbt-performance/SKILL.md)** - Performance optimization for dbt and Snowflake
  - Use when addressing slow builds, optimizing query performance, sizing warehouses, or implementing clustering strategies
  
- [x] **[dbt-commands](.claude/skills/dbt-commands/SKILL.md)** - Command-line operations, selection syntax, and Jinja patterns
  - Use when running dbt commands, selecting models, debugging compilation errors, or using Jinja macros
  
- [x] **[dbt-core](.claude/skills/dbt-core/SKILL.md)** - Complete local dbt-core development guide
  - Use for installation, configuration, project setup, package management, troubleshooting, development workflow, and upgrades with non-interactive scripts and configuration templates
  
- [x] **[schemachange](.claude/skills/schemachange/SKILL.md)** - Deploy and manage Snowflake database objects using version control
  - Use when you need to manage database migrations for objects not handled by dbt, implement CI/CD pipelines for schema changes, or coordinate deployments across environments
  
- [x] **[snowflake-cli](.claude/skills/snowflake-cli/SKILL.md)** - Execute SQL and manage Snowflake objects using the CLI
  - Use when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, or automate Snowflake operations from CI/CD pipelines
  
- [x] **[streamlit-development](.claude/skills/streamlit-development/SKILL.md)** - Develop, test, and deploy Streamlit data applications
  - Use when you're building interactive data apps, setting up local development environments, testing with pytest or Playwright, or deploying apps to Snowflake
  
- [x] **[playwright-mcp](.claude/skills/playwright-mcp/SKILL.md)** - Automate browser testing using Playwright MCP
  - Use when you need to test Streamlit apps, validate web interfaces, test responsive design, check accessibility, or automate browser interactions through MCP tools

- [x] **[task-master](.claude/skills/task-master/SKILL.md)** - AI-powered task management for structured development
  - Use when you need to manage complex projects with PRDs, break down tasks into subtasks, track dependencies, and maintain organized workflows across features and branches

---

#### Anthropic Reference Skills

**Sync Command:** Run `.claude/skills/sync-anthropic-skills.sh` to update Anthropic skills to the latest version.

**Creative & Design:**
- [x] **[algorithmic-art](.claude/skills/anthropic-reference/algorithmic-art/SKILL.md)** - Create algorithmic art using p5.js with seeded randomness
  - Use when creating generative art, flow fields, or particle systems
- [x] **[canvas-design](.claude/skills/anthropic-reference/canvas-design/SKILL.md)** - Design visual art in PNG/PDF formats
  - Use for creating professional visual designs with design philosophies
- [x] **[slack-gif-creator](.claude/skills/anthropic-reference/slack-gif-creator/SKILL.md)** - Create animated GIFs optimized for Slack
  - Use for creating animations within Slack's size constraints

**Development & Technical:**
- [x] **[artifacts-builder](.claude/skills/anthropic-reference/artifacts-builder/SKILL.md)** - Build complex HTML artifacts with React and Tailwind
  - Use for complex artifacts requiring state management, routing, or shadcn/ui components
- [x] **[mcp-builder](.claude/skills/anthropic-reference/mcp-builder/SKILL.md)** - Create high-quality MCP servers
  - Use when building MCP servers to integrate external APIs or services in Python or Node/TypeScript
- [x] **[webapp-testing](.claude/skills/anthropic-reference/webapp-testing/SKILL.md)** - Test web applications using Playwright
  - Use for automated browser testing and UI validation

**Enterprise & Communication:**
- [x] **[brand-guidelines](.claude/skills/anthropic-reference/brand-guidelines/SKILL.md)** - Apply Anthropic brand standards
  - Use for applying official brand colors and typography to artifacts
- [x] **[internal-comms](.claude/skills/anthropic-reference/internal-comms/SKILL.md)** - Write internal communications
  - Use for creating status reports, newsletters, and FAQ documents
- [x] **[theme-factory](.claude/skills/anthropic-reference/theme-factory/SKILL.md)** - Style artifacts with professional themes
  - Use for applying pre-set or custom themes to artifacts

**Document Skills:**
- [x] **[docx](.claude/skills/anthropic-reference/document-skills/docx/SKILL.md)** - Create and edit Word documents
  - Use for working with .docx files, tracked changes, comments, and document formatting
- [x] **[pdf](.claude/skills/anthropic-reference/document-skills/pdf/SKILL.md)** - Manipulate PDF documents
  - Use for extracting text, creating PDFs, merging, splitting, or handling forms
- [x] **[pptx](.claude/skills/anthropic-reference/document-skills/pptx/SKILL.md)** - Create and edit PowerPoint presentations
  - Use for working with presentations, layouts, templates, and charts
- [x] **[xlsx](.claude/skills/anthropic-reference/document-skills/xlsx/SKILL.md)** - Create and edit Excel spreadsheets
  - Use for working with spreadsheets, formulas, data analysis, and visualization

**Meta Skills:**
- [x] **[skill-creator](.claude/skills/anthropic-reference/skill-creator/SKILL.md)** - Guide for creating effective skills
  - Use when you need to create new custom skills
- [x] **[template-skill](.claude/skills/anthropic-reference/template-skill/SKILL.md)** - Basic template for new skills
  - Use as a starting point when creating new skills

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

*For the most up-to-date and comprehensive guidance, prioritize Skills (`.claude/skills/`) over legacy Cursor rules (`.cursor/rules/`).*
