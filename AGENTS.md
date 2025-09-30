# AGENTS.md

Context and guidelines for AI coding agents working on this dbt + Snowflake data engineering project.

## Project Context

This is a **modern data engineering project** built with dbt-core and Snowflake, implementing industry best practices for analytics engineering.

**Technology Stack:**
- **dbt-core** for data transformation and modeling
- **Snowflake** as the cloud data warehouse
- **Python models** with Snowpark for advanced analytics
- **Taskmaster AI** for structured development workflow
- **CI/CD automation** for deployment

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
   - Create comprehensive PRD in `.taskmaster/docs/PRD.md`
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
4. **Research** - Use `task-master research` to understand implementation approaches
   - Research current best practices and patterns
   - Validate technical approaches against requirements
   - Gather implementation context and examples
   - Identify architectural patterns and technology choices

5. **Architectural Design** - Develop the technical solution
   - Design system architecture and process logic
   - Define technology stack and integration patterns
   - Plan data flow and system interactions
   - Document technical design decisions

6. **Parse and Break Down** - Use `task-master parse-prd` to generate tasks from specifications
   - Automatically convert specifications into actionable tasks
   - Use `task-master analyze-complexity` to identify complex tasks
   - Use `task-master expand <id>` to break down high/medium complexity tasks
   - Maintain traceability between requirements and implementation tasks

7. **Organize Tasks** - Set dependencies and priorities
   - Use `task-master add-dependency` to establish logical task sequencing
   - Identify critical path and bottlenecks
   - Align priorities with business value and technical dependencies

#### **Phase 3: Implement and Test**
8. **Code Development** - Use `task-master list` and `task-master next` for development
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
    - Use `task-master update-subtask <id>` to record progress
    - Update specifications based on learnings
    - Maintain audit trail of changes and decisions

#### **Phase 4: Iterate and Refine**
11. **Validation** - Test implementation against specification
    - Verify all acceptance criteria are met
    - Confirm specification compliance
    - Validate system behavior matches requirements

12. **Refine** - Iterate on specification, design, or implementation
    - Refine specifications if new insights arise
    - Update implementation until tests pass
    - Ensure requirements are fully met
    - Use `task-master set-status <id> done` to mark completion

13. **Maintain Traceability** - Keep specification as living document
    - Maintain continuous alignment throughout project lifecycle
    - Update documentation to reflect final implementation
    - Prepare for deployment and future maintenance

---

## Essential Commands for Agents

### Project Setup
```bash
# Install dependencies and test connection
pip install -r requirements.txt && dbt deps && dbt debug

# Build entire project
dbt build --full-refresh
```

### Core Development Workflow
```bash
# Run and test models
dbt run --select modelname
dbt test --select modelname
dbt build --select modelname

# Generate documentation
dbt docs generate
```

---

## Architecture Context

**Medallion Architecture**: Bronze (staging) → Silver (intermediate) → Gold (marts)
**Complexity Levels**: Crawl (basic) → Walk (intermediate) → Run (advanced)

### Key Directories
- `models/bronze/` - Staging models (raw data ingestion)
- `models/silver/` - Intermediate models (business logic)  
- `models/gold/` - Mart models (analytics-ready)
- `macros/` - Custom Jinja macros and functions
- `tests/` - Data quality tests (generic and singular)
- `snapshots/` - SCD Type 2 historical tracking

---

## AI Assistant Integration Setup

To add Taskmaster MCP server to your AI assistant for task-driven development:

```bash
# Add task-master-ai MCP server (example for Snova)
snova mcp add task-master-ai npx --args "-y,--package=task-master-ai,task-master-ai" --env "GOOGLE_API_KEY=your_google_api_key,MODEL=gemini-2.5-pro,MAX_TOKENS=64000,TEMPERATURE=0.2,DEFAULT_SUBTASKS=5,DEFAULT_PRIORITY=medium"

# Verify MCP server was added
snova mcp list
# Start AI assistant with project directory
snova -w /path/to/your/dbt/project

---

## Agent Guidelines

### Code Standards
- **Consistency** - Follow established patterns across the project
- **Testability** - Every model should have appropriate data quality tests
- **Documentation** - Document business logic and complex transformations

### Rule References
- **[dbt Best Practices](.cursor/rules/dbt.mdc)** - Complete dbt modeling guidelines
- **[Taskmaster Commands](.cursor/rules/taskmaster/taskmaster.mdc)** - Task management reference
- **[Development Workflow](.cursor/rules/taskmaster/dev_workflow.mdc)** - Detailed process guide
- **[Snowflake CLI Guide](.cursor/rules/snowflake-cli.mdc)** - Snowflake operations

---

## Key Constraints for Agents

### Security Requirements
- **Never hardcode credentials** - Always use environment variables
- **Follow data protection policies** for PII handling

### Performance Guidelines  
- **Use incremental materialization** for large fact tables
- **Apply appropriate clustering keys** for frequently queried columns
- **Size warehouses** based on model complexity

### Testing Requirements
- **Always test models** after implementation (`dbt test --select modelname`)
- **Use dbt_constraints** for primary/unique/foreign key validation
- **Run full test suite** before deployment (`dbt build`)

### Deployment Process
- **Test connection** with `dbt debug` before deployment
- **Deploy using Python script** with `python deploy_dbt_project.py --target prod`
- **Validate in production** with `dbt test --target prod`

---

*For detailed implementation rules and examples, see the referenced .cursor/rules/ files.*
