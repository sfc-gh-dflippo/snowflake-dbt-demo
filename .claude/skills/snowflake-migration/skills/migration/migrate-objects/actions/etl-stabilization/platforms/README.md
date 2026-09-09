# Platform Providers

Each subdirectory represents a source ETL platform that the stabilization can process. The orchestrator detects the platform during planning and loads the corresponding profile to configure all platform-specific behavior.

## Supported Platforms

| Directory | Platform | Source File |
|-----------|----------|-------------|
| `ssis/` | SQL Server Integration Services | `.dtsx` |
| `informatica/` | Informatica PowerCenter | `.xml` |

## Adding a New Platform

1. **Create the directory**: `platforms/<platform_id>/`

2. **Write `platform-profile.md`** following the structure in any existing profile. Required sections:
   - **Identity**: platform_id, name, source file extension/label/format
   - **Source of Truth**: description, assertion derivation instruction, traceability comment format
   - **Guides**: relative paths to the guide files below
   - **Dead Code Stripping**: script path (or null if not needed)
   - **Element Classification**: disabled marker, pipeline type, external dependency types
   - **Source-Specific Vocabulary**: terms for control flow, dataflow, packages, tasks, etc.

3. **Write guide files** (filenames are platform-specific — use terminology native to the platform):
   - **Orchestration guide** (referenced by `orchestration_guide` in the profile) — How to navigate the source file to extract orchestration structure (execution order, dependencies, variables, event handling). Examples: `control-flow-guide.md` for SSIS, `workflow-guide.md` for Informatica.
   - **Transformation guide** (referenced by `transformation_guide` in the profile) — How to navigate the source file to extract transformation logic (sources, transforms, destinations, column definitions, expressions). Examples: `dataflow-guide.md` for SSIS, `mapping-guide.md` for Informatica.
   - `element-types.md` — Mapping of source platform element types to Snowflake equivalents

4. **Optionally add `strip_dead_code.py`** if the platform's SnowConvert output contains platform-specific dead code patterns that should be stripped during planning. Set `strip_script` in the profile to the script filename, or `null` to skip.

5. **Add EWI guides to `ewi/`** as platform-specific conversion issues are discovered. Name files by their EWI/FDM code (e.g., `SSC-EWI-INFA0001.md`). Shared EWI guides (not platform-specific) live in `reference/ewi/`.

6. **No changes to core skill files are needed** — the orchestrator reads the platform profile during planning and threads its values through all sub-skills and agent prompts via template variables.

## File Structure per Platform

```
platforms/<platform_id>/
├── platform-profile.md         # Required — platform identity and configuration
├── <orchestration_guide>.md    # Required — source file navigation for orchestration
│                               #   (e.g., control-flow-guide.md, workflow-guide.md)
├── <transformation_guide>.md   # Required — source file navigation for transformations
│                               #   (e.g., dataflow-guide.md, mapping-guide.md)
├── element-types.md            # Required — element type to Snowflake mapping
├── strip_dead_code.py          # Optional — dead code stripping script
└── ewi/                        # Optional — platform-specific EWI/FDM fix guides
    ├── SSC-EWI-XXXX.md
    └── ...
```

## License

Copyright (c) Snowflake Inc. All rights reserved.

Licensed under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0).
