# Test Strategy: Isolated vs Grouped

This document describes the decision logic the **orchestrator** uses when authoring the ROADMAP (Step 7) to classify elements as `isolated` or `grouped`. The orchestrator authors these decisions based on element relationship analysis in PACKAGE_ORCH_CONTEXT.md.

Sub-skills (orchestration-test-gen, orchestration-fixer) read the pre-assigned strategy from ROADMAP and session_status.json — they do NOT re-determine grouping.

## Isolated Tests

For elements that are self-contained with no shared state:

- One test file per element: `<task_procedure_name>/<element_name>.sql`
- Full ARRANGE:SETUP → ARRANGE:SEED → ACT → ASSERT
- ARRANGE:SETUP creates only the infrastructure this element needs (DDL objects)
- ARRANGE:SEED populates test data (TRUNCATE + INSERT) — re-run before each ACT/ASSERT cycle
- ACT wraps this element's logic in a stored procedure (see [stored-procedure-wrapping.md](stored-procedure-wrapping.md))
- ASSERT validates this element's side effects with positive and negative checks

**When to use:** Element has no shared tables with other elements in the same container and no sequential dependencies.

## Grouped Tests

For elements that share tables or have sequential dependencies:

- One test file per group: `<task_procedure_name>/grouped_<group_name>.sql`
- Shared ARRANGE:SETUP sets up infrastructure (DDL) for all elements in the group
- Shared ARRANGE:SEED populates test data for all elements — re-run before each cycle
- Sequential ACT executes elements in order, each wrapped in its own stored procedure
- ASSERT validates the combined outcome of the group

**When to use:**
- Elements share tables (element A INSERTs, element B reads/transforms)
- Elements must execute in order to be meaningful

Variable sharing is NOT a grouping constraint — test infrastructure (CLEAR_VARIABLES) isolates variable state between test runs. Only TABLE sharing requires grouped execution.

## Test Strategy in ROADMAP

Each phase definition in ROADMAP.md specifies the test strategy:

```
**Test strategy:**
- SCR_Init_Batch + SQL_Load_Data + SQL_Update_Status → grouped (SQL_Load_Data writes to staging_table, SQL_Update_Status reads it)
- SEQC_Truncate elements → isolated (independent operations)
```

## Test Strategy in session_status.json

Each element has a `test_strategy` field:
- `"isolated"` — tested alone
- `"grouped:<group_name>"` — tested with other elements in the named group

## Folder Structure

```
<UNIT>/stabilization/tests/orchestration/
  <task_procedure_name>/
    <element_name>.sql                # Isolated test
    grouped_<group_name>.sql          # Grouped test (multiple elements)
  test_report.md
```

Each file is fully self-contained with its own ARRANGE:SETUP, ARRANGE:SEED, ACT, and ASSERT sections.
