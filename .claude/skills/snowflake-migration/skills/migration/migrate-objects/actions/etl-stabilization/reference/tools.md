## Tools Reference

All scripts live in `<SKILL_DIR>/scripts/` and are invoked via `uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/<script>`.

---

### `scan_unit.py` — Unit Scanner

Scans a converted ETL unit folder and produces a structural JSON index.

```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/scan_unit.py <unit_folder> [<source_file>] [--platform <platform_id>]
```

- **Input**: Unit folder path, optional source definition file path, optional `--platform` flag (auto-detected from extension if omitted)
- **Output**: `<unit_folder>/stabilization/planning/scan.json`
- **Used in**: Planning Step 2

---

### `backup_unit.py` — Unit Backup

Creates a backup of the entire unit folder before any stabilization work begins. Useful for recovery if scripting errors or unexpected changes occur during the scanning or fixing phases.

```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/backup_unit.py <unit_folder> [--backup-dir <path>]
```

- **Input**: Unit folder path; optional backup destination directory (defaults to `<unit_folder>/../backup/`)
- **Output**: `<backup_dir>/<unit_folder_name>_<timestamp>.tar.gz`
- **Used in**: Optional manual backup before starting phases

---

### `strip_dead_code.py` — Dead Code Stripper (Platform-Specific)

Removes platform-specific boilerplate and binary data from converted code blocks. Example: for SSIS, strips commented-out C#/XML boilerplate and base64 binary data from SSIS0004 ScriptTask blocks, keeping only ScriptMain.cs business logic. Located at `platforms/<platform>/strip_dead_code.py`.

```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/platforms/<platform>/strip_dead_code.py <orchestration_sql_file>
```

- **Input**: Orchestration SQL file (modified in-place)
- **Used in**: Planning Step 5 (after scan and backup) — only when the platform profile defines a `strip_script`
- **Note**: Each platform may have its own strip script, or none (if `strip_script: null` in the platform profile, this step is skipped)

---

### `track_status.py` — Session Status Tracker

Manages `artifacts/tracking/session_status.json` — the single source of truth for element and phase tracking. **All writes to session_status.json MUST go through this script** (never edit the JSON directly).

> **Orchestrator-only writes:** Only the orchestrator calls `track_status.py`. Sub-skill agents (test-gen, fixer, dbt-fixer, dbt-test-gen) report results in their artifacts; the orchestrator reads those artifacts and updates session_status.json sequentially after agents complete.

#### Essential Commands (always used)

| Command | Usage |
|---------|-------|
| `init` | `track_status.py init <scan.json>` — Initialize session from scan results |
| `update` | `track_status.py update <session.json> <element> --status <status> [--reason <reason>]` — Update element status |
| `set-test-env` | `track_status.py set-test-env <session.json> <database> <schema>` — Set test environment |
| `init-roadmap` | `track_status.py init-roadmap <session.json> --phases-json '<json>'` or `--phases-file <path>` — Initialize ROADMAP phases |
| `assign-phases` | `track_status.py assign-phases <session.json> --phase <N> --elements <csv> --strategy <strategy>` or `--elements-file <path>` — Assign elements to a single phase |
| `batch-assign-phases` | `track_status.py batch-assign-phases <session.json> --assignments-file <path>` or `--assignments-json '<json>'` — Assign all phases atomically in one call (preferred over multiple `assign-phases`) |
| `update-state` | `track_status.py update-state <session.json> --current-phase <N> --phase-status <text> --next-action <text>` — Update STATE.md |
| `complete-phase` | `track_status.py complete-phase <session.json> <phase_num>` — Mark phase complete |
| `validate-phase` | `track_status.py validate-phase <session.json> <phase_num> [--list-test-files]` — Validate phase readiness |

#### Situational Commands (error recovery, dbt)

| Command | Usage |
|---------|-------|
| `add-phase` | `track_status.py add-phase <session.json> --phase <N> --name <name> --goal <goal> --scope <scope>` — Add a new phase |
| `add-decision` | `track_status.py add-decision <session.json> --phase <N> --decision <text>` — Record a decision |
| `init-dbt` | `track_status.py init-dbt <session.json> <project_name> <dbt_project_path>` — Initialize dbt project tracking |
| `update-dbt` | `track_status.py update-dbt <session.json> <project_name> --status <status> [--reason <reason>]` — Update dbt project status |
| `update-dbt-node` | `track_status.py update-dbt-node <session.json> <project_name> <node_name> --status <status> [--reason <reason>]` — Update individual dbt node status |

#### Valid Statuses

- **Orchestration elements**: See [protocols/element-statuses.md](protocols/element-statuses.md)
- **dbt projects**: `pending`, `dbt-tested`, `dbt-fixed`, `dbt-failed`
- **dbt nodes**: `pending`, `test-passed`, `test-failed`, `fixed`, `failed`, `skipped`

---

### `generate_report.py` — HTML Report Generator

Generates a self-contained HTML report from all ETL fixer artifacts. Aggregates `scan.json`, `session_status.json`, `ROADMAP.md`, `orchestration-context.md`, `dbt-context.md`, `fix_log.md`, and `STATE.md` into a single browsable HTML file.

```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/generate_report.py <unit_folder> [--template <path>]
```

- **Input**: Unit folder path; optional `--template` for custom HTML template (defaults to `reference/templates/report-template.html`)
- **Output**: `<unit_folder>/stabilization/report.html`
- **Used in**: Final Validation phase (phase-execution.md step c)

---

### Cortex Code Interfaces

This skill uses two distinct interfaces. **Do not mix them** — bash commands are not tools, and tools are not bash commands.

#### Bash CLI commands (run via the `bash` tool)

These provide **user-facing progress tracking**. They are the ONLY way to show task/step progress to the user.

| Command | Purpose |
|---------|---------|
| `cortex ctx task add "<name>"` | Create a progress task (visible to user) |
| `cortex ctx task start <id>` | Mark task as started |
| `cortex ctx step add -t <id> "<text>" ["<text>" ...]` | Add one or more steps to a task (pass every step in ONE call) |
| `cortex ctx step done <id> [<id> ...]` | Mark one or more steps complete (group them; flush before agent waves, turn ends and phase transitions) |
| `cortex ctx show tasks` | List active tasks and steps |

**Do NOT use** `cortex ctx remember` or `cortex ctx forget` — these persist across sessions and pollute future sessions in the same project.

#### Native CoCo tools (invoked directly, NOT via bash)

These are built-in tools invoked through the tool-use interface, the same way you invoke `read`, `write`, `bash`, or `glob`.

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `task` | Spawn a subagent | `subagent_type`, `name`, `run_in_background`, `prompt`, `description`, `team_name` |
| `task_create` | Create a work item in a team's shared queue | `subject`, `description`, `prompt`, `team_name`, `blocked_by` |
| `task_update` | Update a work item's status/owner | `task_id`, `status`, `team_name` |
| `task_list` | List work items | `status`, `team_name` |
| `task_get` | Get full work item details | `task_id` |
| `task_claim` | Claim a work item | `task_id`, `owner` |
| `team_create` | Create a team | `team_name`, `description` |
| `team_delete` | Delete the current active team | (no parameters) |
| `send_message` | Message a teammate | `type` (message/broadcast/shutdown_request/shutdown_response), `recipient`, `content` |
| `snowflake_sql_execute` | Run SQL against Snowflake | SQL string, connection |
| `ask_user_question` | Ask the user a question | question text, options |

**`agent_output`** — documented in CoCo guides but not reliably available. Do not attempt to call it — failed attempts waste a turn. Use the **Agent Wait Protocol** in SKILL.md. Never tell the user a subagent is running unless this turn's spawn tool results include live agent ids.

#### How to reference tools in this skill

- **Bash commands** appear in fenced code blocks and are run via the `bash` tool
- **Native tools** are described in prose: "Use the `task` tool to spawn..." or "Use `team_create` to create..."
- **Never write pseudocode** like `agent_output(wait=true)` or `Task(name=..., run_in_background=true)` — it looks like code but maps to nothing the model can execute
