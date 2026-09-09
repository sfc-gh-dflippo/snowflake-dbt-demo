## Troubleshooting

### scan_unit.py fails
- Verify unit folder contains exactly one `.sql` orchestration file
- Verify source definition file path is correct and readable
- Verify `uv` is installed: `which uv`
- If using `--platform`, verify the platform ID matches a directory under `platforms/`
- Check whether the input is a flat, multi-unit conversion output rather than an isolated per-unit folder; see SKILL.md "When the converted-output folder is not isolated"

### track_status.py errors
- Verify `scan.json` exists in `{UNIT}/stabilization/planning/`
- Verify JSON is well-formed: `python -m json.tool {UNIT}/stabilization/planning/scan.json`

### Snowflake connection issues
- Verify active connection: run a simple `SELECT 1` query
- Verify write privileges: `CREATE TABLE`, `CREATE FUNCTION`, `CREATE PROCEDURE` on the configured database/schema
- If credentials changed, re-run: `track_status.py set-test-env {SESSION_JSON} {DATABASE} {SCHEMA}`

### Sub-skill fails mid-execution
- Check STATE.md for last completed element
- Retry the phase — sub-skills skip already-completed elements (idempotent re-entry)
- If the same element fails repeatedly, log in STATE.md Blockers and skip it

### Task agent runs out of context

**Symptoms:**
- Task notification arrives with `failed` status and no output files, OR
- `batch_{B}.md` exists but is missing element sections (fewer `###` entries than elements assigned in ROADMAP), OR
- Agent completion message states `"partial-completion: context pressure"`

**Recovery (automatic):**
The orchestrator applies the partial artifact recovery sub-protocol (see [protocols/phase-execution.md step e](protocols/phase-execution.md)):
1. Parse `batch_{B}.md` to find completed elements (those with a `### element_name` section and a terminal status)
2. Identify remaining unprocessed elements (assigned in ROADMAP but absent from artifact)
3. Spawn a continuation agent `orch-batch-{B}-r1` with only the remaining elements — same schema, same team
4. If a single element remains unprocessed, spawn a dedicated single-element agent `orch-batch-{B}-r2` — the full context budget goes to that one hard element
5. After 2 retry spawns, any still-unprocessed elements are marked `failed` with reason `"context-exhaustion-after-retries"`

**Prevention:**
Batch agents self-assess context pressure after each element and write artifacts to disk before stopping. This produces partial artifacts that the recovery flow handles cleanly, without re-doing completed work. Agents implement context monitoring per their SKILL.md Task Mode specifications.
