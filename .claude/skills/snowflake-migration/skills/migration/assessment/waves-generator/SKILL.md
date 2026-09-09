---
name: sql-migration-waves-generator
description: Analyze SQL object dependencies and create deployment waves/partitions for database migrations. Use when working with SQL migration planning, SnowConvert outputs, or deployment wave creation.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Migration Waves/Partition Generator

## Overview

This skill produces a deployment wave plan for database/ETL migrations by running the SCAI CLI command `scai assessment waves` from inside a SCAI project. The command builds the dependency graph directly from the project's registry, assigns priority tiers, partitions objects into dependency-ordered waves, and emits a single consolidated JSON file.

**Use this skill when:**
- Planning SQL database and/or ETL migration deployment sequences
- Creating deployment waves that respect object dependencies
- Optimizing migration batch sizes for deployment

## Sub-Agent Mode

When invoked from a parent skill (e.g., `assessment/SKILL.md`) as a sub-agent, the parent provides a context block with the fields below. **Skip the prompts in [Required User Interactions](#required-user-interactions) whenever the corresponding fields are present in the context block** — sub-agents must not block on stdin.

| Field | Required | Notes |
|---|---|---|
| `project_dir` | yes | absolute path to the SCAI project root |
| `partition_min_size` | yes | integer; maps to `--min-size` |
| `partition_max_size` | yes | integer; maps to `--max-size` |
| `prioritization_globs` | yes | list of glob strings; emit one `--prioritize <glob>` per entry; pass nothing if empty |
| `wave_ordering` | yes | `category` (default) or `dependency` (adds `--no-category-waves`) |
| `output_dir` | yes | typically `<project_dir>/assessment` |

**On entry:** call the `configure` MCP tool with `project_dir` from the context block. Snowflake credentials are not required — `scai assessment waves` reads only the local registry.

**Pass every required input as a CLI flag.** If `scai assessment waves` still requests TTY input for any reason, fail fast and report the missing flag — do not block waiting for stdin.

**On completion**, return **JSON only** (no surrounding prose):

```json
{
  "sub_skill": "waves-generator",
  "status": "ok",
  "output_json": "<abs path to waves_analysis_*.json>",
  "summary": "<one-line counts: partitions, sccs, objects>",
  "error": null
}
```

On failure: `"status": "error"`, `"output_json": null`, `"error": "<message>"`. The parent verifies the JSON path exists before continuing.

## Prerequisites

- The working directory must be a SCAI project (i.e. `.scai/` exists and the registry is initialized).
- `scai assessment waves` reads the registry produced by `scai code convert`. The parent `assessment/SKILL.md` ensures the project is bootstrapped before routing here — do **not** prompt the user for paths.

## Inputs (auto-detected by parent)

The parent `assessment` skill has already set `project_dir` and verified the registry exists. This skill does **not** take any input paths — `scai assessment waves` reads the registry from the current project folder.

## Required User Interactions

**These steps are mandatory in inline (standalone) mode.** When invoked as a sub-agent (see [Sub-Agent Mode](#sub-agent-mode)) and the corresponding context-block fields are present, skip the prompts and use the supplied values directly.

### Before Generating Waves

You MUST confirm the following with the user before running `scai assessment waves`:

1. **Partition size** — The default is 40-80 objects per wave. Ask:
   > "The default wave size is 40-80 objects per wave. Would you like to keep these defaults, or set custom min/max limits?"

2. **Object prioritization** — Some objects may need to be deployed first. Ask:
   > "Would you like to prioritize specific objects to appear in the earliest waves? You can use name patterns, for example `"*Payroll*"` to prioritize all Payroll-related objects, or `"dbo.Customer"` for an exact match."

3. **Wave ordering strategy** — Explain the default and offer the alternative. Ask:
   > "By default, waves are grouped by category: TABLEs are deployed first, then VIEWs, then FUNCTIONs/PROCEDUREs, and ETL packages last. This ensures schema foundations exist before the code that depends on them. Alternatively, you can use a pure dependency-based approach that mixes all object types by dependency level. Would you like to keep the default category-based ordering, or switch to dependency-based?"
   >
   > If user chooses dependency-based, add `--no-category-waves` to the command.

### After Generating Waves

4. **Return to parent workflow** — After the waves JSON is written:
   > "Wave generation is complete. Would you like to generate the HTML report now?"
   >
   > If yes, return to the parent skill (`../SKILL.md`) and follow its **Report Generation** section using `generate_multi_report.py` ONLY.
   >
   > If the assessment includes other sub-skills (Object Exclusion, Dynamic SQL, SSIS), continue with the parent workflow sequence.

---

## Command Reference

Run `scai assessment waves` from inside the SCAI project root. The command must **not** be run from elsewhere, and it does not accept a `--project-dir` flag — change to the project directory first if needed.

### Basic Usage

```bash
scai assessment waves
```

**Output**: `<projectRoot>/assessment/waves_analysis_YYYYMMDD_HHMMSS.json` — a single consolidated JSON containing the graph summary, partitions, SCCs, top dependencies, and statistics.

### With Custom Partition Sizes

```bash
scai assessment waves --min-size 15 --max-size 50
```

### With Object Prioritization

Prioritize specific objects or patterns for earlier deployment in Wave 1. The flag is repeatable.

```bash
scai assessment waves \
  --prioritize "*ComputerAsset*" \
  --prioritize "*Worker*" \
  --prioritize "PKG_PAYROLL*"
```

**Supports wildcards:**
- `--prioritize "PKG_*"` — All objects starting with `PKG_`
- `--prioritize "*OrthoContract*"` — All objects containing `OrthoContract`
- `--prioritize "[SCHEMA].[TABLE]"` — Exact object name

### Disable Category-Based Wave Ordering

By default, waves are grouped by category (TABLE → VIEW → FUNCTION → PROCEDURE → ETL). To mix all object types purely by dependency level, use `--no-category-waves`:

```bash
scai assessment waves --no-category-waves
```

## Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--min-size <N>` | 40 | Minimum target wave size for bin-packing |
| `--max-size <N>` | 80 | Maximum wave size for bin-packing |
| `--prioritize <PATTERN>` | — | Glob pattern for user-prioritized objects (repeatable) |
| `--no-category-waves` | off | Disable category-based waves (TABLE→VIEW→FUNCTION first). Mixes all types by dependency level. |

Run `scai assessment waves -h` for the latest list of flags.

## Output File

`scai assessment waves` writes **one** file:

- `<projectRoot>/assessment/waves_analysis_YYYYMMDD_HHMMSS.json`

The consolidated JSON contains:

| Section | Purpose |
|---------|---------|
| `graph_summary` | Total nodes, edges, weakly connected components, cycle counts |
| `partitions` | Wave composition: partition number, size, type, members, root/leaf flags |
| `sccs` | Strongly connected components (circular dependencies) |
| `excluded_edges` | Edges excluded from partitioning (self-refs, undefined objects, temp tables) |
| `top_dependencies` | Objects with the most dependencies and dependents |
| `scc_priority_order` | Priority tier distribution (User-Prioritized / Regular / ETL) |
| `objects` | Per-object metadata (category, conversion status, assigned partition, root/leaf flags) |
| `statistics` | Per-category counts, size distributions, cycle/missing-dep totals |

The HTML generators (`generate_multi_report.py`, `generate_html_report.py`) read this JSON directly via the `WavesJsonAdapter`.

## Algorithm Details

The algorithm lives in the SCAI implementation of `scai assessment waves`. At a high level:

1. **Build Dependency Graph** — load deployable in-scope objects from the registry and build a directed graph from `dependencies.dependsOn`. Self-references are excluded; undefined references are tracked separately.
2. **Category-Based Wave Ordering (Default)** — TABLEs first, then VIEWs, then FUNCTIONs, with a convergence loop to handle cross-category dependencies (e.g. TABLE → FUNCTION). Disable with `--no-category-waves`.
3. **Priority Classification** —
   - Tier 0 (User-Prioritized): objects matching `--prioritize` patterns (earliest)
   - Tier 1 (Regular): DDL/DML foundations (TABLE, VIEW, PROCEDURE, FUNCTION)
   - Tier 2 (ETL): SSIS packages and ETL objects (latest — they consume the foundations)
4. **Initial Partitioning** — process prioritized objects first with their transitive dependencies; start from roots; iteratively add nodes whose dependencies are all satisfied; create partitions between `--min-size` and `--max-size`; handle cycles via iterative Tarjan SCC.
5. **Partition Merging** — merge partitions smaller than `--min-size` (excluding category waves) with adjacent ones while preserving ordering.
6. **Dependency Validation** — each partition only depends on earlier partitions (enforced by §15 invariants before emitting output).

## Filtering Rules

- **Self-references excluded**: edges where caller equals referenced object
- **CREATE statements only**: only objects with a `CREATE X` definition in the registry
- **Undefined nodes tracked**: edges to/from objects not in the registry are surfaced as missing dependencies
- **Temp tables excluded**: dynamic temp tables (e.g. `#TTableName`) are not tracked as formal objects

## Examples

### Example 1: Standard Migration Analysis

```bash
# From inside the SCAI project root
scai assessment waves
```

**Output**: deployment waves of 40-80 objects each in `<projectRoot>/assessment/waves_analysis_<timestamp>.json`.

### Example 2: Prioritize Critical ETL Processes

```bash
scai assessment waves \
  --prioritize "*ComputerAsset*" \
  --prioritize "*Worker*" \
  --prioritize "PKG_PAYROLL*"
```

**Output**: places all ComputerAsset, Worker, and Payroll-related objects (with their dependencies) in Wave 1.

### Example 3: Smaller Batch Sizes

```bash
scai assessment waves --min-size 10 --max-size 30
```

**Output**: more partitions with 10-30 objects each for incremental deployment.

### Example 4: Dependency-Based Mixing

```bash
scai assessment waves --no-category-waves
```

**Output**: waves mix all object types purely by dependency level (no TABLE→VIEW→FUNCTION ordering).

## Typical Workflow

1. **Bootstrap the project** — `scai init`, connect, register, `scai code convert` (handled by `../setup/SKILL.md`). The registry must exist.

2. **Generate deployment waves**:
   ```bash
   scai assessment waves
   ```
   Re-run with `--min-size`, `--max-size`, `--prioritize`, or `--no-category-waves` as the user requested.

3. **Review the output** — open `<projectRoot>/assessment/waves_analysis_<timestamp>.json`. Inspect the `graph_summary`, `sccs`, `excluded_edges`, and `partitions` sections.

4. **Generate the HTML report** — return to the parent skill and use `generate_multi_report.py --project-dir <projectRoot>`. The script auto-discovers the registry, reports, exclusion JSON, dynamic-SQL JSON, and the latest `waves_analysis_*.json`. Do not write HTML manually.

## Key Concepts

### Root Nodes
Objects with no dependencies (no incoming edges). Safe to deploy first.

### Leaf Nodes
Objects with no dependents (no outgoing edges). Nothing else depends on them.

### Weakly Connected Components
Separate forests/trees in the dependency graph. Each can be deployed independently.

### Strongly Connected Components (SCCs)
Circular dependencies where objects depend on each other. Requires special handling.

### Progressive Disclosure
Partitions are numbered sequentially. Each partition depends only on partitions with lower numbers.

## Troubleshooting

### `scai assessment waves` reports "must run inside a SCAI project"

**Cause**: The current directory is not a SCAI project root (no `.scai/` or registry).

**Solution**: `cd` into the project directory before running, or bootstrap via `../setup/SKILL.md`.

### Many Single-Object Partitions

**Cause**: Graph has many disconnected components or complex dependency patterns.

**Solution**: Adjust `--min-size` / `--max-size` or accept that some objects are isolated.

### Circular Dependencies Detected

**Cause**: Objects have mutual dependencies (A depends on B, B depends on A).

**Solution**: Review the `sccs` section of the JSON to identify problem objects. May require manual intervention or schema refactoring.

### High Excluded Edge Count

**Cause**: Many temp tables or dynamic objects not tracked as formal objects.

**Solution**: Normal for SQL Server migrations. Review the `excluded_edges` section of the JSON for patterns.

## Best Practices

1. **Start with default settings** (40-80 objects) and adjust based on deployment capacity.
2. **Review graph structure** first (`graph_summary`, `sccs`) to understand component count and cycles.
3. **Check excluded edges** to understand temp table usage patterns.
4. **Use prioritization for critical ETL processes** — prioritize business-critical objects (e.g., `--prioritize "*Payroll*" --prioritize "*Customer*"`) to ensure they deploy first.
5. **Review the `scc_priority_order` section** after prioritization to verify expected objects are in Tier 0.
6. **Combine prioritization with custom sizes** for fine-grained control over wave composition.
7. **Deploy partitions sequentially** respecting the partition number order.
