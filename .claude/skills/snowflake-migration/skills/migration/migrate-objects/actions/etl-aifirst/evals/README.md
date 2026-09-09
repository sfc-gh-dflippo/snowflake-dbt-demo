# etl-aifirst trigger-tuning set (I-54)

Should-trigger / should-not-trigger prompt set for wording `SKILL.md`'s
`description`, using the skill-authoring plugin's own trigger-rate tool
(`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_eval.py`).
This is deliberately **not** the `ai/tests/skills` desktop eval harness — it
needs no plugin wiring, no Snowflake, no live routing (I-51 doesn't exist
yet) — see `docs-unlock/evals-m1/DECISIONS-NEEDED.md` / `INVENTORY.md` Q6 for
why the two are kept separate.

## Files

- `trigger-eval-set.json` — 20 prompts: 10 should-trigger (one per AI-First
  platform table, see below) and 10 should-not-trigger (natively-supported
  dialects plus deliberately tricky near-misses). Each item carries a
  `split: "train"|"test"` field (12 train / 8 test, stratified by
  `should_trigger`, matching `run_loop.py`'s own 60/40 convention) and a
  `platform` / `note` field for traceability — `run_eval.py` itself only
  reads `query` and `should_trigger`, the rest is documentation.
- `trigger-baseline-result.json` — raw, unedited output of `run_eval.py`
  against the current `SKILL.md` description (see command below). Not
  hand-edited in any way.

## Platform coverage (ticket text vs. ground truth)

The ticket body says "the five platform element tables that already exist
today." `platforms/` in this skill directory actually ships **six** today:
`platform_adf.json`, `platform_alteryx.json`, `platform_datastage.json`,
`platform_informatica.json`, `platform_pentaho.json`, `platform_ssis.json`
(confirmed by directory listing, not the ticket text). This set covers all
six on the should-trigger side rather than only five, since the ticket's
own done-when says "covering all five already-defined AI-First platform
tables" — the intent is full coverage of whatever the table set actually is,
and the count grew after the ticket was written (the `platform_informatica.json`
header calls itself `informatica.v2`, i.e. a later addition).

`docs-unlock/evals-m1/INVENTORY.md`'s I-54 row also suggests "Informatica"
as a *should-not-trigger* (natively supported) example. That's inconsistent
with the actual repo state: Informatica PowerCenter has its own AI-First
platform table here (`platform_informatica.json`) and is not one of
SnowConvert's native SQL dialects (confirmed: `setup/midway-entry.md:35`
still lists only `sqlserver` and `redshift` as the native `-l` dialects, same
grounding I-50 already did). This set treats Informatica as should-trigger
and uses SQL Server / Redshift (the two actually-documented native dialects)
for the should-not-trigger side instead.

## Running the tool

```bash
cd ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
python3 -m scripts.run_eval \
  --eval-set <repo>/ai/plugin/skills/migration/migrate-objects/actions/etl-aifirst/evals/trigger-eval-set.json \
  --skill-path <repo>/ai/plugin/skills/migration/migrate-objects/actions/etl-aifirst \
  --model claude-sonnet-5 \
  --runs-per-query 1 \
  --num-workers 5 \
  --timeout 45 \
  --verbose
```

`--model claude-sonnet-5` because that's the model powering this session, per
the skill-creator's own `SKILL.md` guidance ("Use the model ID from your
system prompt... so the triggering test matches what the user actually
experiences"). `--runs-per-query 1` (the tool's own default is 3) as a
deliberate cost/time tradeoff for a first baseline — a single real
`claude -p` subprocess per query still gives one honest, non-fabricated data
point per prompt; it is not the statistically-smoothed number a `3`-run
majority vote would give, and a future re-run should say so if it changes
`--runs-per-query`.

## Baseline result and an important caveat

`trigger-baseline-result.json`: **10/20 passed** — all 10 should-not-trigger
prompts correctly did not trigger (`trigger_rate: 0.0`, `pass: true`), but
all 10 should-trigger prompts also did not trigger (`trigger_rate: 0.0`,
`pass: false`).

That 0/10 positive rate is **not** reliable evidence that the current
description under-triggers. Verified directly (not assumed): `run_eval.py`
detects a trigger by writing the query + description into a temporary file
under `.claude/commands/<clean-name>.md` and watching for a `Skill` or
`Read` tool-use naming that file, in a fresh `claude -p --output-format
stream-json` subprocess. A manual, unfiltered repro of exactly that
mechanism (same command-file shape, same query, same `claude -p` flags,
full raw stream captured and inspected line-by-line rather than truncated)
showed the injected file is exposed to that subprocess only as a
**slash command** (`slash_commands` in the `system/init` event), never as an
entry in the `skills` array the model actually consults for the `Skill`
tool. Given full repo access, the model instead solved the task on its own
(`Agent`→`Explore` subagent, then direct `grep`/`Read` of
`platform_informatica.json` etc.) and answered correctly and specifically —
a good outcome for a real user, but not the signal `run_eval.py` is trying
to measure, and not something rewording the description can fix. This
appears to be a gap between the skill-creator plugin's assumptions (built
against a Claude Code build where a dropped-in command file could be
autonomously consulted as a Skill) and this installed CLI build
(`claude-code-version` `2.1.220`), not a defect in this eval set or in the
`etl-aifirst` description.

This ticket's done-when only requires that running the tool "produces a
baseline trigger-rate number, recorded for comparison against the future
wired-routing state" — done, honestly, above. Actually tuning the
description (out of scope for this ticket) should wait until this
measurement-mechanism gap is understood or worked around; optimizing wording
against a broken 0% positive signal would be tuning noise, not the
description.
