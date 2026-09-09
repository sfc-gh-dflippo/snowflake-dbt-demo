## Reference Index

Quick-lookup index for all reference files. Load on-demand — only read a file when its content is needed for the current step.

### Protocols

Rules and conventions that govern skill behavior.

| File | Purpose |
|------|---------|
| [protocols/element-statuses.md](protocols/element-statuses.md) | Canonical element status list, valid transitions, and rules |
| [protocols/phase-execution.md](protocols/phase-execution.md) | Full phase execution protocol (orchestration, dbt, final validation, validation gate) |
| [orchestration-tags.md](orchestration-tags.md) | Canonical tag reference: container vs non-container patterns, replacement boundaries |

### Platforms

Platform-specific guides are organized under `platforms/{platform_id}/`. See [platforms/README.md](../platforms/README.md) for how to add a new platform.

| Platform | Profile | Orchestration Guide | Transformation Guide | Element Types | EWIs |
|----------|---------|--------------------|-----------------------|---------------|------|
| SSIS | [platform-profile.md](../platforms/ssis/platform-profile.md) | [control-flow-guide.md](../platforms/ssis/control-flow-guide.md) | [dataflow-guide.md](../platforms/ssis/dataflow-guide.md) | [element-types.md](../platforms/ssis/element-types.md) | [ewi/](../platforms/ssis/ewi/) |
| Informatica | [platform-profile.md](../platforms/informatica/platform-profile.md) | [workflow-guide.md](../platforms/informatica/workflow-guide.md) | [mapping-guide.md](../platforms/informatica/mapping-guide.md) | [element-types.md](../platforms/informatica/element-types.md) | [ewi/](../platforms/informatica/ewi/) |

### Shared EWI / FDM Fix Guides

Decision trees and fix patterns for SnowConvert conversion issues that are not platform-specific. Read the relevant guide before fixing an element with that code.

| File | Code | Description |
|------|------|-------------|
| [ewi/SSC-EWI-TS0077.md](ewi/SSC-EWI-TS0077.md) | SSC-EWI-TS0077 | T-SQL conversion issue |
| [ewi/SSC-FDM-0007.md](ewi/SSC-FDM-0007.md) | SSC-FDM-0007 | Functional difference marker |

### SSIS-Specific EWI / FDM Fix Guides

Located under `platforms/ssis/ewi/`. These guides are loaded when `platform_id` is `ssis`.

| File | Code | Description |
|------|------|-------------|
| [SSC-EWI-SSIS0001.md](../platforms/ssis/ewi/SSC-EWI-SSIS0001.md) | SSC-EWI-SSIS0001 | Data flow component not supported (includes third-party connectors) |
| [SSC-EWI-SSIS0002.md](../platforms/ssis/ewi/SSC-EWI-SSIS0002.md) | SSC-EWI-SSIS0002 | SSIS expression conversion issues |
| [SSC-EWI-SSIS0003.md](../platforms/ssis/ewi/SSC-EWI-SSIS0003.md) | SSC-EWI-SSIS0003 | Execute SQL Task conversion |
| [SSC-EWI-SSIS0004.md](../platforms/ssis/ewi/SSC-EWI-SSIS0004.md) | SSC-EWI-SSIS0004 | Script Task conversion |
| [SSC-EWI-SSIS0014.md](../platforms/ssis/ewi/SSC-EWI-SSIS0014.md) | SSC-EWI-SSIS0014 | For Loop container conversion |
| [SSC-FDM-SSIS0001.md](../platforms/ssis/ewi/SSC-FDM-SSIS0001.md) | SSC-FDM-SSIS0001 | SSIS variable conversion |
| [SSC-FDM-SSIS0002.md](../platforms/ssis/ewi/SSC-FDM-SSIS0002.md) | SSC-FDM-SSIS0002 | SSIS connection manager |
| [SSC-FDM-SSIS0003.md](../platforms/ssis/ewi/SSC-FDM-SSIS0003.md) | SSC-FDM-SSIS0003 | SSIS precedence constraint |
| [SSC-FDM-SSIS0004.md](../platforms/ssis/ewi/SSC-FDM-SSIS0004.md) | SSC-FDM-SSIS0004 | SSIS event handler |
| [SSC-FDM-SSIS0005.md](../platforms/ssis/ewi/SSC-FDM-SSIS0005.md) | SSC-FDM-SSIS0005 | SSIS package configuration |
| [SSC-FDM-SSIS0006.md](../platforms/ssis/ewi/SSC-FDM-SSIS0006.md) | SSC-FDM-SSIS0006 | SSIS logging provider |

### Informatica-Specific EWI / FDM Fix Guides

Located under `platforms/informatica/ewi/`. These guides are loaded when `platform_id` is `informatica`.

| File | Code | Description |
|------|------|-------------|
| [SSC-EWI-INF0001.md](../platforms/informatica/ewi/SSC-EWI-INF0001.md) | SSC-EWI-INF0001 | PowerCenter transformation not supported |
| [SSC-EWI-INF0003.md](../platforms/informatica/ewi/SSC-EWI-INF0003.md) | SSC-EWI-INF0003 | Workflow element cannot be converted |
| [SSC-EWI-INF0038.md](../platforms/informatica/ewi/SSC-EWI-INF0038.md) | SSC-EWI-INF0038 | Informatica conversion issue |
| [SSC-EWI-INF0039.md](../platforms/informatica/ewi/SSC-EWI-INF0039.md) | SSC-EWI-INF0039 | Informatica conversion issue |
| [SSC-EWI-INF0040.md](../platforms/informatica/ewi/SSC-EWI-INF0040.md) | SSC-EWI-INF0040 | Informatica conversion issue |
| [SSC-EWI-INF0050.md](../platforms/informatica/ewi/SSC-EWI-INF0050.md) | SSC-EWI-INF0050 | User-defined function call not converted |
| [SSC-FDM-INF0002.md](../platforms/informatica/ewi/SSC-FDM-INF0002.md) | SSC-FDM-INF0002 | Informatica functional difference |
| [SSC-FDM-INF0015.md](../platforms/informatica/ewi/SSC-FDM-INF0015.md) | SSC-FDM-INF0015 | Informatica functional difference |
| [SSC-FDM-INF0016.md](../platforms/informatica/ewi/SSC-FDM-INF0016.md) | SSC-FDM-INF0016 | Informatica functional difference |

### Agent Prompts

Templates loaded when spawning autonomous batch agents. Each prompt wires the agent to the appropriate sub-skill.

| File | Agent | Loaded by |
|------|-------|-----------|
| [agent-prompts/context-mapper.md](agent-prompts/context-mapper.md) | Context mapper (Planning Step 6) | Orchestrator |
| [agent-prompts/apply-fixes.md](agent-prompts/apply-fixes.md) | Mechanical tag replacement agent | Orchestrator (Execution) |

Note: Test generation and fixing agents (`orchestration-test-gen`, `orchestration-fixer`, `dbt-test-gen`, `dbt-fixer`) read their task mode specifications directly from their SKILL.md files (§ Task Mode section), not from reference prompts.

### Templates

Templates for generated artifacts.

| File | Purpose |
|------|---------|
| [templates/ROADMAP_TEMPLATE.md](templates/ROADMAP_TEMPLATE.md) | Template for agent-authored ROADMAP.md |
| [templates/batch-artifacts.md](templates/batch-artifacts.md) | Batch artifact and learning artifact format specs |
| [templates/baseline-artifacts.md](templates/baseline-artifacts.md) | Baseline report schema (baseline_batch_{B}.md format) |
| [templates/fix-log-format.md](templates/fix-log-format.md) | Cross-phase fix log format (fix_log.md structure) |
| [templates/report-template.html](templates/report-template.html) | HTML report template (CSS + shell for `generate_report.py`) |

### Other

| File | Purpose |
|------|---------|
| [tools.md](tools.md) | Consolidated script and MCP tool reference |
| [examples.md](examples.md) | Worked examples of common fix patterns |
| [troubleshooting.md](troubleshooting.md) | Common failure scenarios and resolutions |
