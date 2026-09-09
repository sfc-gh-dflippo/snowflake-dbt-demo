---
name: testbed-generator
description: >
  Drive the workload-scoped Synthetic Testbed Generator through its MINE →
  VALIDATE → ENRICH → COMPILE → GENERATE phases for a migration. Sequences `scai
  testbed init` → `list-unsolved` (mine) and surfaces the categorized
  unsolved-constraint view; `scai testbed validate` and surfaces the readiness view
  (fk gaps / type conflicts / unsatisfied constraints); `scai testbed compile` and
  surfaces the cluster summary; runs the two-pass ENRICH reasoning (structural then
  value prompts) that turns unsolved constraints into enrichment JSON; `scai testbed
  generate` (readiness-gated) and surfaces the row counts + CSV/manifest deliverable.
  Resumes each phase after a kill by recomputing from on-disk state. Reads
  machine-readable JSON views; mutates state only through scai testbed subcommands,
  never the opaque state.bin. Triggers: generate testbed, mine testbed, validate
  testbed, compile testbed, enrich testbed, run testbed phases, resume testbed,
  inspect unsolved constraints, testbed data source. Runs the two-pass ENRICH phase then the ORCHESTRATE phase between mine and compile
  (assemble the 8-array envelope, drive propose-enrichments/validate with bounded
  retries + observability). Does NOT generate CSVs or seed test YAML.
parent_skill: baseline-capture
license: Proprietary. See License-Skills for complete terms
---

# Testbed generator — mine + validate + enrich + compile + generate

Drives the deterministic `scai testbed` mine, validate, enrich, compile, and
generate phases for the whole workload. The data lives in the CLI's opaque state; this
skill only sequences subcommands and surfaces their JSON. It replaces production
*data*, not source *access* — a source connection is still required downstream to
capture the baseline.

The core phases are independent and resumable: **mine** (`init` → `list-unsolved`
→ whole-workload branch drill-down) inventories the constraint/branch coverage;
**validate** reads the mined state and reports readiness (fk gaps / type conflicts
/ unsatisfied constraints) — `ready: false` is a report, not a failure; **enrich**
is the reasoning + propose/validate loop that turns unsolved constraints into
enrichment JSON (see the Orchestrate phase below); **compile** materializes the
data-coupling clusters + coordination spec that data generation consumes;
**generate** (readiness-gated) writes the CSV pool + manifest deliverable. Each
phase is deterministic — re-running it is safe and cheap.

## On Entry

Tell the user:

> "Running the testbed mine → validate → enrich → compile → generate phases: I'll inventory
> the branch/constraint coverage your converted workload needs and show the
> categorized unsolved-constraint view, report readiness (fk gaps / type conflicts /
> unsatisfied constraints), run the enrichment loop that turns the unsolved constraints
> into enrichment JSON (assemble → propose → validate, with a bounded retry/iterate budget),
> compile the data-coupling / coordination spec and show its cluster summary, then —
> readiness permitting — generate the CSV pool + manifest and show the row counts. This
> reads the conversion artifacts and the testbed state; the enrich phase mutates that state
> (through `propose-enrichments`) and only the generate phase writes data files."

## Scope

- In scope: `init` → `list-unsolved` (mine) → surface the categorized view; `validate` → surface the readiness view; `compile` → surface the cluster summary; the two-pass ENRICH reasoning (structural then value prompts) that turns unsolved constraints into enrichment JSON (§enrich below); `generate` (readiness-gated) → surface row counts + CSV/manifest deliverable; resume each phase; classify failures.
- In scope (orchestrate): assemble the per-type fragments into the 8-array envelope, drive `propose-enrichments`/`validate` with a bounded retry/iterate budget, emit observability counts (SNOW-3782435).
- Out of scope: `generate`'s CSV internals; the per-object test-YAML bridge.
- Phase-scoped runs: each driver subcommand (`mine`, `validate`, `enrich`, `compile`, `generate`) can be run and stopped independently — e.g. run `validate` to inspect readiness without generating data.

## Steps

1. Ensure the MCP session is configured: if you were spawned as a sub-agent, call `configure(project_dir=<abs_path>)` first (you may be the first to touch the server, and there is no working-directory fallback).
2. **Mine phase.** Run the driver:

   ```
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py mine --project-dir {PROJECT_DIR}
   ```

3. **On mine exit code 0:** the driver wrote `testbed/mine/unsolved-view.json` and printed a one-line summary. Present the summary, then read `testbed/mine/unsolved-view.json` and show the per-`kind` counts (`fk`, `check`, `branch_predicate`, `join_edge`, `enum_domain`) and the `branches` drill-down (per object: `branch_count`, `unsolved_branches`). Do not paraphrase the counts — read them from the file. A table with `branch_count: 0` is normal — tables have no branches; do not report it as a gap.
4. **On mine non-zero exit:** the driver printed `"<station> failed [<code>] <message> (<class>)"`. Act on the class, then stop (do not proceed to compile):
   - `input_config` (e.g. `PRJ0003`, `TBD0007`): the project dir or artifacts path is wrong. Fix it and re-run step 2.
   - `data_isolable` / `data_quarantine`: the driver recorded the offending object as PENDING in `.scai/testbed/run.json` and continued where it could. Tell the user which objects are PENDING and why.
   - `escalate`: stop and surface the full error; do not retry.
5. **Validate phase (after mine exit 0).** Run the driver:

   ```
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py validate --project-dir {PROJECT_DIR}
   ```

6. **On validate exit code 0:** the driver wrote `testbed/validate/readiness-view.json` and printed a one-line summary. Read the view and present `ready`, `counts` (`blocking`, `advisory`, `fk_gaps`, `type_conflicts`, `unsatisfied_constraints`, `overlaps`), and the `fk_gaps` / `type_conflicts` / `unsatisfied_constraints` / `overlaps` arrays. **`ready: false` is not an error** — it is a successful report of gaps carried in the view. If not ready, tell the user the blocking issues must be fixed (or explicitly overridden at generate) before data will generate. On a package-driven (SSIS) workload, FK-gap checking is suppressed and `overlaps` (Lookup / Merge-Join key domains that provably cannot match) is usually the only populated bucket — so it is the whole answer to "what is blocking this run", and each entry's `remediation.hint` is what the user must act on. Present every bucket the `counts` object reports; if a tally is non-zero and its array is empty, say so rather than reporting no issues.
7. **On validate non-zero exit:** act on the class (`input_config` `TBD0002`: state missing — re-run mine; `escalate` `TBD0003/4/5`: surface the CLI `suggestion` and stop).
8. **Enrich phase (after validate exit 0, before compile).** Run the enrichment orchestration — assemble the prompt fragments into one envelope, propose it, and re-validate readiness in a bounded retry/iterate loop:

   ```
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py enrich --project-dir {PROJECT_DIR}
   ```

   On **exit 0** the driver wrote `testbed/enrich/enrichment-view.json` and the workload is ready — proceed to compile. On **non-zero exit** read `testbed/enrich/enrichment-report.json` and act on its `stop_kind` (`reject` / `iterate` / `documented-stop` / `budget-exhausted`); the full loop and each stop's remediation are in the **Orchestrate phase** below. **Enrich MUST precede compile** — it mutates the mined state that compile materializes into clusters, and its terminal `validate ready` is the readiness precondition the generate gate checks.
9. **Compile phase (only after enrich exit 0).** Run the driver:

   ```
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py compile --project-dir {PROJECT_DIR}
   ```

10. **On compile exit code 0:** the driver wrote `testbed/compile/clusters-view.json` and printed a one-line summary. Present the summary, then read `testbed/compile/clusters-view.json` and show `clusters`, `coupled_objects`, `singleton_objects`, `largest_cluster`. Note for the user: per-cluster membership is not surfaced yet — that arrives with the (later) generate phase.
11. **On compile non-zero exit:** the driver printed `"compile failed [<code>] <message> (<class>)"`. Act on the class:
    - `input_config` (`TBD0002`): the testbed state (`.scai/testbed/state.bin`) is missing — the mine phase's `init` didn't run or was cleared. Re-run step 2, then step 9.
    - `escalate` (`TBD0003`/`TBD0004`/`TBD0005`): the state is unreadable, version-mismatched, or corrupt. Surface the CLI's `suggestion` verbatim (typically: re-run `init`, or remove a duplicate source object then re-mine). Do not retry blindly.
12. **Generate phase (after compile exit 0 and validate ready — or an explicit override).** Run the driver:

    ```
    uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py generate --project-dir {PROJECT_DIR}
    ```

    - If the workspace was **not ready** at validate, the driver blocks with `"generate blocked: N blocking issue(s); re-run with --ignore-readiness to override"`. Only re-run with `--ignore-readiness` after telling the user which blocking issues will be bypassed.
    - If validate never ran, the driver blocks with `"generate blocked: run validate first"` — run Step 5 first.
13. **On generate exit code 0:** the driver wrote `testbed/generate/summary-view.json` and printed a one-line summary. Read the view and present `tables`, `rows_written`, `csv_files`, `warnings`, and `readiness_overridden` — surface each warning (a non-fatal generation diagnostic, e.g. a declared width too narrow to hold `row_count` distinct key values). An empty workspace is a success with `csv_files: 0` and a `note` — surface the note. `out_path` is the **project root** the manifest's per-table `csv_path` entries are relative to (not a CSV directory), and `manifest_path` is the provenance `manifest.json` beside `state.bin`; to list the generated CSVs, read the `csv_path` entries from `manifest.json` at `manifest_path` — don't present `out_path` as the output directory.
14. **On generate non-zero exit:** act on the class (`input_config` `TBD0012`: state not compiled — run Step 9 first; `escalate`: surface the error and stop).
15. Do **not** call `transition_status`. The `generateTestbed` task completes when `testbed/generate/summary-view.json` exists (a `filesystemProxy` status source) — the resolver detects it. Calling `advance` for a filesystem-backed task returns an error. If generate is blocked or escalates and never writes the summary view, the task stays incomplete by design; surface the error and stop rather than looping.

## Enrich phase (two-pass)

After mine, once `list-unsolved` has emitted the gaps, run the enrichment reasoning. The prompt files live under `prompts/{structural,value}/`. Assembling the envelope and calling `scai testbed propose-enrichments` / `validate` is the Orchestrate phase below (SNOW-3782435) — this phase produces the reasoning inputs and the per-type outputs.

**Map each unsolved `kind` to its prompt:**

| unsolved `kind` | prompt(s) |
|---|---|
| `fk`, `join_edge` | `structural/fk_chains.md`; peer-attribute joins → `structural/correlated_groups.md` |
| compound `branch_predicate` (cross-table) | `structural/correlated_groups.md` |
| anti-join `branch_predicate` (`NOT EXISTS` / `LEFT JOIN … IS NULL`) | `structural/anti_join_tables.md` |
| date-column pairs | `structural/temporal_alignment.md` |
| `branch_predicate` (value arm) | `value/branch_values.md` |
| `enum_domain` (undeclared) | `value/inferred_enum.md`; unclassifiable residue → `value/flag_for_llm.md` |
| `check` / lookup floors | `value/must_include.md` |
| column null semantics | `value/null_fraction_override.md` |

**Order:** run the **structural pass first** (`fk_chains` → `correlated_groups` → `temporal_alignment` → `anti_join_tables`) because its outputs feed the value pass; within a pass, independent types are order-free. Then the **value pass** (`branch_values`, `inferred_enum`, `must_include`, `null_fraction_override`, `predicate_fills`; `flag_for_llm` is a router resolved skill-side into one of the other types — never emitted). This phase stops at the per-type outputs; the Orchestrate phase below (SNOW-3782435) assembles them into the 8-array wire envelope (`column_enrichments`, `branch_values`, `fk_chains`, `temporal_alignment`, `correlated_groups`, `anti_join_tables`, `temporal_window_bindings`, `predicate_fills`) and drives `propose-enrichments`/`validate`.

## Orchestrate phase (assemble + propose/validate loop)

Runs after the enrich pass and **before compile** (`mine → enrich → compile → generate`). The enrich pass writes per-type fragments to `testbed/enrich/fragments/<prompt_type>.json` — **one file per prompt-type, overwrite-in-place** (a re-prompt MUST replace the same file, never add a sibling; v1 keys fragments by prompt-type only). Run the structural pass first, then the value pass (same discipline as the Enrich phase), then close the loop:

1. **Assemble + propose + validate (one attempt).** Run the driver:

   ```
   uv run --project {SKILL_DIR} python {SKILL_DIR}/scripts/run_pipeline.py enrich --project-dir {PROJECT_DIR}
   ```

   Between *assemble* and *propose*, the driver runs the **critic station** (the deterministic
   backbone ① + citation gate ③, SNOW-3717841). On the first pass over a given envelope it runs the
   backbone and stops with `stop_kind: "critique"`, having written
   `testbed/enrich/critic/critique-request.json` (the entries that passed the backbone, with the spans
   to judge). **You then run the critic prompts** — `prompts/critics/joins_critic.md` for the structural
   arrays, `prompts/critics/spec_critic.md` for the value arrays — and write your verdict to
   `testbed/enrich/critic/verdict.json` per `prompts/critics/verdict-contract.md`. Re-invoke the driver:
   with a fresh verdict present (its `envelope_sig` matching the assembled envelope) the driver applies
   the citation gate and, on all-ACCEPT, proceeds to `propose-enrichments`.

2. **On exit 0:** the driver wrote `testbed/enrich/enrichment-view.json` and the workload is ready — proceed to compile.
3. **On non-zero exit:** read `testbed/enrich/enrichment-report.json` and act on `stop_kind`:
   - `reject` — a fragment was malformed OR the critic backbone/gate rejected an entry (`reason:
     critic_backbone` with `citations`, or `reason: critic_reject`). Re-run the prompt named by
     `prompt_type` (`critic` for a critic rejection), overwrite its fragment, re-invoke step 1. Bounded
     by the per-prompt-type budget.
   - `critique` — the backbone passed; the envelope awaits your semantic judgment. Run the two critic
     prompts against `critique-request.json`, write `verdict.json` (copy `envelope_sig` verbatim), then
     re-invoke step 1. A `REJECT` needs a verifiable mode-`a` citation; when you can't cite a
     contradicting span, use `REVISE` (mode `b`). Re-authoring a fragment on REVISE changes the envelope
     and re-runs the backbone on the new version.
   - `iterate` — either `validate` is not ready, or the citation gate downgraded a critic `REJECT` to
     a bounded `REVISE`. When `validate` is not ready, for each `blocking` issue whose
     `remediation.enrichment_fixable` is true, re-run the prompt for its `remediation.enrichment_type`
     (using the `hint`), overwrite the fragment, re-invoke. When the stop instead carries `reason:
     critic_revise` / `prompt_type: critic`, the payload is not the `blocking`/`remediation` shape but
     `entries[]` — each with `kind`, the offending `table`/`column(s)`, and the critic's `feedback` —
     so re-author the named fragment(s) per that `feedback` and re-invoke; re-authoring changes the
     envelope and re-runs the backbone. The two `iterate` causes are bounded by two independent
     budgets: a not-ready `validate` iterate draws on the global iteration budget
     (`--max-iterations`, exhausting as `reason: iteration_budget`), while a `critic_revise` iterate
     draws on the `critic` bucket of the per-prompt-type reject budget
     (`--max-rejections-per-type`, exhausting as `reason: critic_budget`).
   - `documented-stop` — a structural gap (FK cycle → `TBD0015`), CAS-retry exhaustion, a **malformed
     `verdict.json`** (`reason: critic_verdict_malformed`), or a **value cycle** (`reason: value_cycle`
     — the same value was rejected and re-proposed). Surface the `detail`/`citations` and stop; a human
     resolves it. The critic never auto-applies an un-critiqued or cyclically-failing entry.
   - `budget-exhausted` — the retry/iterate budget is spent. Surface the report and stop; a human fixes the fragment and re-runs with `--reset-budget`.
4. **Only after enrich exit 0**, run compile (enrich MUST precede compile). Enrich's terminal `validate ready` is the readiness precondition the downstream `generate` gate checks; the standalone `validate` step above remains a cheap idempotent re-check.

Note: `fk_cycle` and `parent_missing_key` gaps are **advisory** (never blocking), so a `validate`-ready workspace that still lists those is legitimately ready — a not-null FK *cycle* instead surfaces at propose-time as `TBD0015` (a `documented-stop`).

## Persistent files

- `.scai/testbed/state.bin` — opaque CLI state (mining spec + materialized clusters). Never read or edit it; treat it as a black box owned by `scai testbed`.
- `testbed/mine/unsolved-view.json` — the mine deliverable (written by the driver).
- `testbed/validate/readiness-view.json` — the validate deliverable: readiness + `fk_gaps` / `type_conflicts` / `unsatisfied_constraints` / `overlaps` (written by the driver).
- `testbed/compile/clusters-view.json` — the compile deliverable: cluster summary (written by the driver).
- `testbed/generate/summary-view.json` — the generate deliverable and **task completion predicate**: row counts + CSV/manifest paths (written by the driver).
- Generated CSVs + provenance `manifest.json` — the `generate` deliverable. Each table's CSV lands under its own object's `<artifacts>/testbed/` folder; the `manifest.json` (beside `state.bin`, at the view's `manifest_path`) lists them as project-root-relative `csv_path` entries. The view's `out_path` is that project root — not a CSV directory. No output dir is passed to `scai testbed generate`.
- `testbed/enrich/critic/critique-request.json` — the backbone-pass entries + spans the critic judges (written by the driver at the `critique` stop).
- `testbed/enrich/critic/verdict.json` — the agent-authored critic verdict (`ACCEPT`/`REVISE`/`REJECT` per entry); consumed by the citation gate on re-invocation.
- `.scai/testbed/run.json` — derived progress ledger (mine/validate/compile/generate status, PENDING records).
