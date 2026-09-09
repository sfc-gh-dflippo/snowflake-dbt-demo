# Phase 5: Integration & End-to-End Orchestration Test

## When to Load

Load ONLY when Phase 5 runs (Tier-2 consent approved). This is the heaviest validation phase — it proves the full pipeline works end-to-end, not just that individual files compile/execute.

## Why Phase 5 exists (distinct from Phase 4)

| | Phase 4 (Execution) | Phase 5 (E2E Orchestration) |
|---|---|---|
| Scope | Each Tier 2/3 file in isolation | **Entire pipeline as one integrated flow** |
| Dependency handling | Per-file mini chain | **Full topological DAG order** |
| Output check | Compare each file's output to baseline | **Assert terminal tables non-empty + compare** |
| Artifact | `snowflake_execution_results.json` | **Reusable harness on disk + `e2e_test_results.json`** |

A pipeline can pass Phase 4 (every SP runs) yet still be broken end-to-end (terminal tables empty because an intermediate join produced zero rows). Phase 5 catches that.

---

## Step 1: Build the Topological Layer Order

Read the cross-file dependency DAG (built at Step 3, stored per file under `files.<name>.dependencies.{creates,reads}` in `conversion_state.json`).

```python
# Kahn topological sort over files using creates/reads
def topo_layers(files):
    # node = file; edge A->B if B.reads intersects A.creates
    produced = {}  # table -> file that creates it
    for f, info in files.items():
        for t in info["dependencies"]["creates"]:
            produced[t.upper()] = f
    deps = {f: set() for f in files}
    for f, info in files.items():
        for t in info["dependencies"]["reads"]:
            src = produced.get(t.upper())
            if src and src != f:
                deps[f].add(src)
    layers, placed = [], set()
    while len(placed) < len(files):
        layer = [f for f in files if f not in placed and deps[f] <= placed]
        if not layer:  # cycle or external-only inputs left
            layer = [f for f in files if f not in placed]
        layers.append(sorted(layer))
        placed.update(layer)
    return layers
```

Files whose `reads` are ALL external source tables (no upstream converted file) land in Layer 0. Terminal files = those whose `creates` tables appear in NO other file's `reads`.

---

## Step 2: Generate the Reusable Harness (on disk)

Generate five files. These are deliverables — they let the user re-run the integration test and deploy orchestration without regenerating.

### 2.1 `orchestration/sp_e2e_pipeline.sql`

A master stored procedure that runs every converted file in DAG layer order. For Tier-2 files, `CALL` the procedure; for Tier-1 files, inline the file's primary `CREATE TABLE AS` statement (or `CALL` a thin wrapper). Track step count and catch errors.

```sql
CREATE OR REPLACE PROCEDURE <SCHEMA>.SP_E2E_PIPELINE()
RETURNS STRING LANGUAGE SQL EXECUTE AS CALLER AS
$$
DECLARE
  v_step STRING DEFAULT '';
  v_passed INTEGER DEFAULT 0;
  v_count INTEGER;
BEGIN
  -- Layer 1
  v_step := 'L1: <proc_or_file>'; CALL <SCHEMA>.SP_...(); v_passed := v_passed + 1;
  -- ... one statement per file, in layer order ...
  -- Layer N (terminal)
  v_step := 'VALIDATION';
  SELECT COUNT(*) INTO :v_count FROM <SCHEMA>.<TERMINAL_TABLE>;
  RETURN OBJECT_CONSTRUCT('status','SUCCESS','steps_passed',v_passed,
                          'steps_failed',0,'last_step',v_step,
                          'terminal_rows',v_count)::STRING;
EXCEPTION WHEN OTHER THEN
  RETURN OBJECT_CONSTRUCT('status','FAILED','failed_at',v_step,
                          'steps_passed',v_passed,'code',sqlcode,'message',sqlerrm)::STRING;
END;
$$;
```

### 2.2 `orchestration/task_dag.sql`

Snowflake Task DAG mirroring the layers: a root task + `AFTER` children, one task (or one bundled task per layer). Tasks created `SUSPENDED`; include `ALTER TASK ... RESUME` lines bottom-up. Include a comment noting `EXECUTE TASK` requires the `EXECUTE TASK` account privilege (ACCOUNTADMIN grant).

### 2.3 `orchestration/adf_pipeline.sql`

ADF master-orchestrator definition (JSON in a comment block): a Script activity that CALLs the staging SP, then a Script activity that CALLs `SP_E2E_PIPELINE()`, then a Lookup activity that validates a terminal table row count. ADF is the master scheduler; Snowflake Tasks handle intra-DAG parallelism.

### 2.4 `testing/setup_test_data.sql`

The depth/unit-aligned synthetic loader (from Phase 1 output). MUST follow the range-join + unit-consistency rules in `references/synthetic-data-rules.md` so multi-hop joins survive to terminal tables. Include a `TRUNCATE` block so it is idempotent.

### 2.5 `testing/expected_results.sql`

Expected terminal-table row counts and key values (from Phase 2 baselines), as comments + sample assertion `SELECT`s.

---

## Step 3: Execute End-to-End

1. Ensure source tables + aligned synthetic data are loaded (run `testing/setup_test_data.sql`).
2. Deploy all Tier-2 procedures (if not already created in Phase 4).
3. `CREATE` then `CALL <SCHEMA>.SP_E2E_PIPELINE()`.
4. Parse the returned JSON. Require `steps_failed = 0`. If a step failed, the `failed_at` field localizes the broken file — fix the converted SQL (not the SAS interpretation) and re-run.

---

## Step 4: Terminal-Output Assertion (the key check)

For every **terminal** table (no downstream consumer), assert row count > 0:

```sql
SELECT '<TERMINAL_TABLE>' AS TBL, COUNT(*) AS ROW_CNT FROM <SCHEMA>.<TERMINAL_TABLE>
UNION ALL ...;
```

Classify each terminal table:
- **POPULATED** (> 0 rows): pass.
- **EMPTY — JUSTIFIED**: the table is empty only because a genuine source/reference table is empty by design (e.g. an unused regional reference). Record the empty upstream in `notes`.
- **EMPTY — DEFECT**: empty despite populated sources. This is a real failure (almost always a join that did not overlap — see the range-join/unit-consistency rules). Flag for fix.

A run where any terminal table is `EMPTY — DEFECT` does NOT pass Phase 5.

---

## Step 5: Compare Terminal Outputs to Baselines

For terminal tables that have a Phase 2 expected baseline, compare row counts and key values per `references/comparison-rules.md`. Apply the trivial-pass rule from `references/snowflake-execution.md`: `expected = 0 AND actual = 0` is a WARNING (`TRIVIAL_PASS`), not a silent pass.

---

## Step 6: Write Results

```python
e2e = {
  "executed_at": "<ISO>",
  "warehouse": "<wh>",
  "layers": <n>,
  "steps_total": <n>, "steps_passed": <n>, "steps_failed": <n>,
  "terminal_tables": [
    {"table": "<T>", "rows": <n>, "status": "POPULATED|EMPTY_JUSTIFIED|EMPTY_DEFECT",
     "empty_source": "<table or null>", "baseline_match": "PASS|FAIL|NO_BASELINE|TRIVIAL_PASS"}
  ],
  "harness_files": ["orchestration/sp_e2e_pipeline.sql","orchestration/task_dag.sql",
                    "orchestration/adf_pipeline.sql","testing/setup_test_data.sql",
                    "testing/expected_results.sql"],
  "status": "PASS|FAIL"
}
# write <output_dir>/e2e_test_results.json
```

`status = PASS` requires: `steps_failed == 0` AND no terminal table is `EMPTY_DEFECT`.

---

## Step 7: Cleanup

If a temporary validation database was created for Phase 5, prompt to drop it (or auto-drop under consent propagation), same pattern as Phase 4.

---

## Modular Execution (Context-Aware)

Generating the master SP for a large pipeline (40+ files) can be large. Build it incrementally:
1. Generate the SP layer-by-layer, appending each layer's CALLs.
2. After writing the harness files, update `execution_progress` in `conversion_state.json` and append a checkpoint line.
3. If context nears the limit mid-generation: save the partial harness + state, inform the user, exit. Resume reads `execution_progress` and continues from the next layer.

---

## HARD GATE (Phase 5)

```python
import os, sys, json
out = "<output_dir>"
need = [os.path.join(out, "e2e_test_results.json"),
        os.path.join(out, "orchestration", "sp_e2e_pipeline.sql")]
missing = [p for p in need if not os.path.exists(p)]
if missing:
    print(f"BLOCKED: Phase 5 artifacts missing: {missing}"); sys.exit(1)
print("Phase 5 GATE PASSED")
```

Update `conversion_state.json`: `gates.phase_5_e2e_orchestration: "PASSED"`. Append checkpoint `step:"phase_5" gate:"phase_5_e2e_orchestration" status:"PASSED"`.
