---
name: semantic-equivalence-checker
description: Check semantic equivalence between an Informatica PowerCenter workflow XML and its converted dbt model. Runs a deterministic structural and transform comparison, then adjudicates what it could not resolve by reading every sibling model in the workflow's directory, and writes a per-workflow verdict with file:line citations. Read-only — it never edits the dbt project. Triggers: semantic equivalence check, check semantic equivalence, run an equivalence check between Informatica and dbt, is this dbt conversion correct, does the dbt model match the Informatica mapping, Informatica vs dbt equivalence, semantic equivalence of a converted workflow, conversion checker.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Semantic Equivalence Checker

## How this skill is reached

Nothing in the plugin references this skill. It is not in the manifest, it has no slash command, and the migration skill's `<skill-match>` block does not list it, so it will never be suggested and nothing routes into it on its own.

It is reached by being named together with where it lives, for example "using the semantic-equivalence-checker sub-skill under `migration/SKILL.md`, check ...". Naming the checker without saying where it sits is not enough: an agent asked only to "use the semantic checker" does not find this directory, and will compare the XML and the models unaided instead, which produces something shaped like a verdict with no deterministic pass behind it.

## On Entry

Tell the user:

> **Semantic equivalence check** — I'll compare an Informatica workflow XML against its converted dbt model and tell you whether the conversion preserves the business logic. I won't change any files. I need the XML, the dbt models folder, and which workflow to check.

`<SKILL_DIR>` below is the absolute path to the directory containing this file. Loaded the
normal way, from the migration skill's `<skill-match>` block, that is the
`semantic-equivalence-checker` directory sitting beside the migration skill's own `SKILL.md`,
so resolve it from wherever you read this file.

If you do not have an absolute path for it, say so and stop. Every command here runs as
`uv run --project <SKILL_DIR>`, and a relative path gives `--project` nothing to resolve. Do
not fall back to comparing the files by hand: see the check at the end of Step 3.

Run every shell command through `uv run --project <SKILL_DIR>`, which resolves the checker's dependencies from its `pyproject.toml`. Do not activate a virtualenv or invoke `python` directly — the package is only importable under that project.

Chain the commands of a single step into one bash call. Each separate call costs the user another permission prompt.

## Architecture: one workflow, many models

This is the single most important thing to hold onto, because almost every false positive comes from ignoring it.

- An Informatica workflow may run **N pipelines** (`SQ_1`…`SQ_N`) sequentially in one session.
- In dbt those decompose into **N separate `.sql` models in the same `_wf` directory**.
- The **primary** model is the one named in the pair index. It implements *one* pipeline.
- **Sibling** models implement the other pipelines, plus pre-hook operations (DELETEs, TRUNCATEs) and post-hook business logic (UPDATEs, INSERTs, DELETEs, CALLs).
- So a source table, column, expression or operation "missing" from the primary **may exist in a sibling's body SQL, its `pre_hook`, or its `post_hook`.**
- Equivalence is a property of **all the models together**, never of the primary alone.
- `__THIS__` refers to a model's own temp table — a dbt architectural pattern, not a defect.

Step 3 writes every sibling out with Jinja pre-resolved precisely so you can search them. A `FAIL` you report without having searched the siblings is the most likely way this skill produces a wrong answer.

## Step 1: Resolve Inputs

You need four values. Take any the user already gave you; ask for the rest in **one** message.

| Value | What it is | How to resolve |
|---|---|---|
| `{XML_PATH}` | The Informatica XML export containing the workflow | From the user's request |
| `{DBT_DIR}` | The dbt models root — the folder whose subdirectories hold the converted models | From the user's request |
| `{WORKFLOW}` | The Informatica workflow name, `wf_`-prefixed | Read `<WORKFLOW NAME="...">` from `{XML_PATH}`; if the XML holds several, list them and ask which |
| `{PRIMARY_MODEL}` | The path to the **primary** `.sql` inside `{DBT_DIR}` | See the warning below |

Set `{OUTPUT_DIR}` to `equivalence-reports/` under the current working directory unless the user names somewhere else.

**Wait for the user's response — do not guess a path or a workflow name.** A wrong pairing produces a confident verdict about the wrong model, which is worse than no verdict.

If the user names a workflow and the XML does not contain it, **stop and say so.** Do not substitute the workflow the XML does contain, even when there is exactly one and the substitution looks obvious. A name that does not match usually means the wrong XML was supplied or the name was mistyped, and either way the answer to a different question is not useful. Report the mismatch, list what the XML actually holds, and let the user choose.

### Resolving the primary model

Glob `{DBT_DIR}` for the workflow's `_wf` directory. Then:

- **One `.sql` in it** — that is the primary.
- **More than one** — the primary is **not** derivable, and it is frequently *not* the model named after the directory. List the candidates, say which pipeline each appears to implement, and **ask the user which is primary.** Guessing here silently compares the wrong file and every finding after it is worthless.

The deterministic pass enforces this rather than trusting it. When the `_wf` directory holds
several models and no primary is named, `check` writes `work/primary_ambiguous.json` with the
candidate list and exits 2 without producing a verdict. If you see that, report the
candidates and ask — there is no artifact to analyse and nothing to salvage by guessing.

Resolve the primary only from the user's answer, or from a pair index or mapping that names it. Do not resolve it from an example in this skill, from a prior session, or from your own inference about which model "looks like" the target — a plausible-sounding justification for skipping the question produces the same wrong pairing as a blind guess.

If the user already has a pair index or mapping CSV that names the primary, use it and skip the question.

Confirm the resolved set back to the user in one line before continuing:

> Checking `{WORKFLOW}` — XML `{XML_PATH}` against `{PRIMARY_MODEL}`, plus N sibling(s). Reports to `{OUTPUT_DIR}`.

## Step 2: Build the Pair Index

Write `{OUTPUT_DIR}/pair-index.json` directly, so the primary you resolved in Step 1 is the one used:

```json
{
  "_preamble": {"dbt_repo_commit": null},
  "{WORKFLOW_LOWERCASE}": {
    "xml_path": "{XML_PATH}",
    "dbt_path": "{PRIMARY_MODEL}",
    "dbt_model_name": "{THE _wf DIRECTORY NAME}"
  }
}
```

Prefer this over the `manifest` subcommand. That subcommand globs the `_wf` directory and takes an arbitrary first match, which is fine for a single-model directory and wrong for a sibling directory.

The file is called `pair-index.json`, not a manifest — a dbt project has its own `manifest.json` and confusing the two sends readers to the wrong file.

## Step 3: Deterministic Comparison

```bash
uv run --project <SKILL_DIR> python -m conversion_checker check \
  --manifest {OUTPUT_DIR}/pair-index.json \
  --workflow {WORKFLOW} \
  --report {OUTPUT_DIR}
```

**On success:** exit 0, a verdict line `✓|✗|~ {WORKFLOW}: PASS|FAIL|PARTIAL`, and these under `{OUTPUT_DIR}/{WORKFLOW}/work/`:

| Artifact | Contents |
|---|---|
| `check.json` | Section statuses, hook SQL, and the paths used. Single-element array — read element `0` |
| `unresolved.json` | Only when the deterministic pass could not decide. `section`, `reason`, `infa_sql`, `dbt_sql` |
| `siblings.json` | Sibling **metadata** — hooks, output columns, refs |
| `dbt_primary.sql` | The primary model with `source()`, `var()` and `ref()` resolved to concrete identifiers |
| `dbt_siblings.json` | **Every other `.sql` in the `_wf` directory**, each with Jinja resolved |

`dbt_primary.sql` and `dbt_siblings.json` appear only when the dbt project root was found. If they are missing, `{DBT_DIR}` is not inside a dbt project — say so and stop, because without them you would be reading raw `{{ }}` and guessing at identifiers.

**On failure:** the command exits non-zero with an `Error:` line naming the cause. Surface it verbatim and stop; every later step reads these artifacts.

**Before Step 4, confirm the deterministic pass actually ran.** Read
`{OUTPUT_DIR}/{WORKFLOW}/work/check.json` and check that element `0` has all of
`source_tables`, `target_table`, `load_strategy`, `column_list`, `pre_hooks`, `post_hooks`,
`transform_logic` and `verdict`. If the file is absent, or sits somewhere other than
`work/`, or is missing any of those keys, the CLI did not produce it. **Stop and report
that.** Do not write the file yourself, do not carry on by reading the XML and models
directly, and do not produce a verdict.

A verdict without the deterministic pass behind it is just an unaided reading of two files,
which is the thing this skill exists to avoid. It will also look exactly like a real result
to whoever receives it.

A `FAIL` or `PARTIAL` here is expected and is not a conclusion. This pass reads only the primary model, so it cannot see logic that lives in a sibling. Resolving that is the next four steps' whole job.

## Step 4: Read Everything

Read, in this order:

1. `check.json`, `unresolved.json`, `siblings.json` from `{OUTPUT_DIR}/{WORKFLOW}/work/`.
2. `dbt_primary.sql` — the resolved primary. Use this, not the original `.sql`, for citations.
3. `dbt_siblings.json` — the resolved siblings.
4. `{XML_PATH}` — the Informatica source.

You cannot cite a line you have not read, and every determination from here on requires a citation.

## Step 5: Section and Pipeline Analysis → `llm_check.json`

Load [references/llm-check-schema.md](references/llm-check-schema.md) for the output shape, citation rules and completeness requirements. Load [references/known-false-positives.md](references/known-false-positives.md) for the platform rewrites that routinely surface as failures without being any.

**For each `FAIL` or `PARTIAL` section in `check.json`:** decide whether it is a true failure or a false positive. **Search every sibling** — body SQL, `pre_hook`, `post_hook` — for the logic reported missing. A false positive here usually means the logic is in a sibling.

**For each entry in `unresolved.json`:** search the siblings for matching logic, compare it against the Informatica SQL, and record which sibling resolved it in `resolved_in`.

**For a multi-pipeline workflow:** confirm each Informatica pipeline maps to some model, primary or sibling. Check that variant-specific logic — join conditions, filters, expressions, allocation columns — survives. Flag any pipeline whose distinct logic has no counterpart anywhere.

**`PASS` sections:** skip, unless you spot a false *equivalence* — something the deterministic pass matched that is not actually equivalent. Record those with `is_false_equivalence: true`.

Cite file and line for every determination, using sibling names as the `file` value where the evidence is in a sibling. Then write `{OUTPUT_DIR}/{WORKFLOW}/work/llm_check.json`.

### The bar for calling anything missing

Every claim gets checked against the whole workflow, not the primary alone. The primary implements one pipeline; the conversion is all the models together.

Before asserting any difference between Informatica and dbt, search all six places: the primary's body SQL, `pre_hook` and `post_hook`, and the same three in **every** sibling. Only when the logic is absent from all of them may you call it missing or different.

When a sibling resolves the discrepancy, name that sibling in the citation. When nothing resolves it, say so in exactly this form:

> NOT FOUND IN ANY MODEL (primary + N siblings searched)

with `N` being the real count from `dbt_siblings.json`. That sentence is the claim's evidence, so it cannot be written without having done the count.

A claim resting on the primary alone is incomplete, and for a multi-pipeline workflow it is usually wrong.

## Step 6: Verdict → `llm_verdict.json`

From your `section_reviews`, `unresolved_analysis` and `pipeline_analysis`:

| Verdict | When |
|---|---|
| `PASS` | Every section passes or is a false positive, every pipeline is covered, and every unresolved item is `EQUIVALENT` or `PLATFORM_HOUSEKEEPING` |
| `FAIL` | Any section is a true `FAIL`, or any pipeline is missing, or any unresolved item is `NOT_EQUIVALENT` |
| `PARTIAL` | A mix of resolved and unresolved issues |

Write `{OUTPUT_DIR}/{WORKFLOW}/work/llm_verdict.json`.

## Step 7: Critic → `llm_critic.json`

Tell the user:

> **Critic** — I'll verify the analysis against the source files: every cited line gets re-read, and every "missing logic" claim gets checked against the sibling models before the verdict stands.

This step validates the work of Steps 5 and 6. If `llm_check.json` is absent, Step 5 has not run — say so and stop rather than validating nothing.

**7a. Run the deterministic critic.**

```bash
uv run --project <SKILL_DIR> python -m conversion_checker critic \
  --workflow {WORKFLOW} \
  --reports-dir {OUTPUT_DIR}
```

**On success:** `{OUTPUT_DIR}/{WORKFLOW}/work/critic.json` is written with 12 automated checks in four categories:

| Category | Checks |
|---|---|
| A — Internal consistency | evidence completeness, verdict vs sections, source-target symmetry, unresolved coverage |
| B — False-positive detection | source/pre-hook overlap, CAST equivalence, audit column leakage, DELETE strategy overlap |
| C — Unresolved quality | reason actionability, housekeeping noise |
| D — Completeness | all sections evaluated, transform logic coverage, pre_sql content comparison |

**On failure:** the command reports the missing input file. Surface it and stop. A failed *check*, by contrast, is a finding to classify in 7d, not a reason to stop.

**7b. Read every artifact.**

Read `critic.json`, `llm_check.json`, `llm_verdict.json`, `check.json` and `unresolved.json` from `{OUTPUT_DIR}/{WORKFLOW}/work/`, then the Informatica XML, `dbt_primary.sql`, and `dbt_siblings.json`.

Read the resolved artifacts, not the original `.sql` files — the analysis cited the resolved ones, so those are the lines to verify against.

**7c. Verify claims against source.**

For every `llm_check.json → verdict.claims[]` entry: read each `sources[].file` at `sources[].lines` and confirm the content is there and supports the claim; confirm the `reasoning` follows from that evidence; note any significant aspect omitted.

For every `unresolved_analysis[]` entry: confirm `aspect_comparison[]` covers the structural dimensions present in the SQL — target, columns, joins, filters, grouping; read each `citations[].lines` and confirm the content matches `content_summary`; cross-check the `equivalence` value against the actual SQL; confirm `resolved_in` names a model that genuinely contains the logic.

For every `section_reviews[]` entry: read each cited line and confirm it matches `content_summary`; where `is_false_positive` is `true`, confirm the evidence genuinely supports overturning the deterministic failure; where `stage3_status` differs from `stage2_status`, confirm the citations justify the change.

**Then the sibling check, which is the reason this step exists.** For every claim of a true failure — a section left `FAIL`, or an item marked `NOT_EQUIVALENT` — confirm the analysis actually searched the siblings before concluding the logic was missing. The deterministic pass reads only the primary model, so a "missing" finding that never looked at `dbt_siblings.json` is unsupported no matter how well it is cited. Set `sibling_search_evidenced` accordingly, and treat `resolved_in: "not_found"` alongside `EQUIVALENT` as a contradiction.

Two of the issue types are critical. Record the type on each `llm_analysis_validation[]` entry as `issue_type`:

- **`hallucinated_citation`** — the cited lines do not exist, or hold something other than what the claim says. Read the file at the cited lines; do not infer from the summary.
- **`false_equivalence`** — the claim asserts a difference, but the logic *is* present in the primary or a sibling's body, `pre_hook` or `post_hook`. Search all of them before accepting any "missing" or "different" claim. This is the largest source of false failures in this skill.

The other two types, `wrong_reasoning` and `missed_issue`, are not automatically critical; judge them on severity.

Reject these three inferences wherever they appear:

- "Not in the primary" does not mean "not in the workflow".
- "Different from Informatica `SQ_1`" can be correct when dbt implements `SQ_1` in a sibling.
- A column present in a sibling's `SELECT` or `post_hook` is not missing from dbt.

A UNION branch on the Informatica side is often a separate sibling model in dbt. That is an architectural difference, not a dropped branch.

`false_equivalence` here and `is_false_equivalence` in `llm_check.json` are different fields in different artifacts, and they point opposite ways. In `llm_check.json`, `is_false_equivalence` marks an equivalence the deterministic pass accepted that is not real. In the critic, `false_equivalence` marks a difference the analysis claimed that is not real. Keep them straight when reading a report.

Re-read each cited line rather than trusting the line number written earlier. A citation that points at a nearby structural boundary instead of the actual expression is the most common defect here, and it invalidates the claim resting on it.

**7d. Cross-consistency.** Check all five:

- `stage3_verdict` agrees with the individual `section_reviews[].stage3_status` values.
- `llm_verdict.json`'s outcome follows from `llm_check.json` under the Step 6 rules: any true `FAIL`, missing pipeline, or `NOT_EQUIVALENT` item forces `FAIL`.
- Every entry in `unresolved.json` has a matching entry in `unresolved_analysis[]`.
- Every `FAIL` or `PARTIAL` section in `check.json` has a matching entry in `section_reviews[]`.
- With N pipelines in the XML, `pipeline_analysis.coverage` accounts for all N, and no claim in `verdict.claims[]` contradicts a finding in `unresolved_analysis[]` or `section_reviews[]`.

**7e. Write `{OUTPUT_DIR}/{WORKFLOW}/work/llm_critic.json`:**

```json
{
  "workflow": "{WORKFLOW}",
  "confidence": "HIGH|MEDIUM|LOW",
  "quality": "HIGH|MEDIUM|LOW",
  "recommendation": "ACCEPT|RERUN",
  "critic_checks": {
    "passed": 10,
    "failed": 2,
    "total": 12,
    "failures": [
      {
        "check": "evidence_completeness",
        "classification": "true_bug|false_positive|known_limitation",
        "detail": "source_tables: evidence line=0",
        "reasoning": "Why this classification was chosen"
      }
    ]
  },
  "llm_analysis_validation": [
    {
      "item": "unresolved_analysis[0]|section_reviews[0]|verdict.claims[0]",
      "valid": "VALID|INVALID|INCOMPLETE",
      "issue_type": "hallucinated_citation|wrong_reasoning|missed_issue|false_equivalence",
      "issue": "Description of the issue, or an empty string when VALID",
      "sibling_search_evidenced": true,
      "verified_at": [
        {"file": "xml", "lines": "423-435", "found": "What was actually at those lines"}
      ]
    }
  ],
  "true_bugs": [
    {"description": "What is broken", "evidence": "Where to look to confirm", "fix": "Suggested fix"}
  ],
  "false_positives": [
    {"source": "critic|llm_analysis", "check_or_claim": "Which check or claim", "reasoning": "Why it is a false positive"}
  ],
  "missing_coverage": [
    "What was not checked but should have been"
  ]
}
```

Judge each validation entry as:

- **VALID** — every cited line exists and contains the described content, the reasoning follows, and no contradictory evidence sits at or near the citation.
- **INVALID** — a cited line is absent or says something different, the reasoning does not follow, or contradictory evidence was omitted.
- **INCOMPLETE** — the claim holds but misses nuance visible in the source, omits nearby code that would strengthen or weaken it, or lacks an `aspect_comparison` entry for a dimension the SQL actually uses.

Then set the two summary fields:

- **`quality`** — `HIGH` when every citation verified and every true-failure claim evidenced a sibling search. `MEDIUM` when some claims needed interpretation or a sibling search was implied but not shown. `LOW` when citations were wrong, sibling searches were absent, or findings contradict each other.
- **`recommendation`** — `RERUN` if any citation is `INVALID`, if any `NOT_EQUIVALENT` claim lacks sibling-search evidence, if any `hallucinated_citation` or `false_equivalence` was found, or if `quality` is `LOW`. Otherwise `ACCEPT`. Any critical `false_equivalence` also forces `quality: LOW`.

`RERUN` is not a failure of the run; it is the mechanism that keeps a confident-but-unsupported verdict from reaching the user. Prefer it over rationalising a weak citation.

Report the passed/failed counts, the `quality` rating, the `recommendation`, every `INVALID` entry and every `true_bugs` entry to the user before continuing.

If the recommendation is `RERUN`, or any citation is `INVALID`, correct `llm_check.json` and repeat from 7a — a verdict resting on a citation that does not say what you claimed is not a verdict.

## Step 8: Final Verdict → `final_verdict.json`

Write this one to `{OUTPUT_DIR}/{WORKFLOW}/final_verdict.json` — **not** into `work/`. It is the only artifact at that level, so a reader gets the answer without having to pick it out of the evidence that produced it.

Consume `work/llm_check.json`, `work/llm_verdict.json` and `work/llm_critic.json` together:

- Critic recommends `RERUN` → set `confidence: LOW` and name the claims that are unreliable.
- Critic found critical issues → downgrade the affected section statuses.
- Critic says `ACCEPT` → carry `llm_verdict`'s outcome through.

```json
{
  "workflow": "{WORKFLOW}",
  "equivalent": true,
  "confidence": "HIGH|MEDIUM|LOW",
  "summary": "One paragraph, plain English: is the conversion correct, and why.",
  "reasons": [
    {
      "factor": "Short label, e.g. 'Missing filter in sibling' or 'Platform syntax only'",
      "detail": "Explanation of this factor",
      "impact": "BLOCKING|ACCEPTABLE|INFORMATIONAL|SKIPPED",
      "source": "work/llm_check.json → unresolved_analysis[1]"
    }
  ],
  "sections_summary": {
    "source_tables": "PASS|FAIL|FALSE_POSITIVE",
    "target_table": "PASS|FAIL|FALSE_POSITIVE",
    "load_strategy": "PASS|FAIL|FALSE_POSITIVE",
    "column_list": "PASS|FAIL|FALSE_POSITIVE",
    "pre_hooks": "PASS|FAIL|EQUIVALENT|INCOMPLETE",
    "post_hooks": "PASS|FAIL|EQUIVALENT|INCOMPLETE",
    "transform_logic": "PASS|FAIL|PARTIAL"
  }
}
```

Field rules:

- `equivalent` is `true` only when all Informatica logic is represented somewhere in the dbt models, platform differences aside. Any missing, wrong or incomplete business logic makes it `false`. **A `SKIP` section also makes it `false`** — logic that was never compared cannot be called equivalent, and reporting it as such is the one failure mode a reviewer cannot detect from the artifacts.
- `impact`: `BLOCKING` means production would produce wrong data. `ACCEPTABLE` means a platform difference or housekeeping with no data effect. `INFORMATIONAL` means it does not bear on correctness. `SKIPPED` means equivalence is unknown for that area.
- `source` points at the artifact and field holding the evidence.
- `sections_summary` is the status *after* adjudication, so a deterministic `FAIL` you overturned becomes `FALSE_POSITIVE`. Every `SKIP` must also appear in `reasons` with impact `SKIPPED`.

## Step 9: Report

Tell the user the verdict, the one-paragraph summary, and every `BLOCKING` or `SKIPPED` reason with its citation. Give the path to `{OUTPUT_DIR}/{WORKFLOW}/final_verdict.json`, and mention that the evidence behind it is in `work/` alongside.

If `equivalent` is `false`, name the specific Informatica logic that has no dbt counterpart, say which models you searched, and cite where you looked. "Missing" without naming the siblings you checked is not a finding.

Do not propose or apply a fix to the dbt project — this skill reports, and the user decides what to change.

This skill records nothing on the migration registry and advances no task: it runs on paths the user handed over, not on a claimed code unit, so there is no task state for it to stamp.
