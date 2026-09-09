# Complexity Analysis (CoCo-Native)

Heuristics for the LLM to read `.sas` source directly and produce a **portfolio-level**
complexity narrative. This layer is qualitative — it explains *why* files are complex and
*what* will need attention, complementing the quantitative metrics from the Python CLI.

Keep these heuristics aligned with the CLI (`scorer.py`, `classifier.py`) so the narrative
does not contradict the numbers. When the CLI has already run, use `assessment.json` for the
counts and use this reference only to add the qualitative "areas of complexity" interpretation.

---

## Construct Catalog

Scan each file for the constructs below. Group findings into **themes** at the portfolio
level (e.g. "Statistical modeling appears in 4 files") rather than listing every occurrence.

### Tier 3 signals (no SQL equivalent — PySpark/SCOS)

| Construct | What to grep for | Why it's complex |
|-----------|------------------|------------------|
| HASH objects | `declare hash`, `hash(` | No SQL equivalent; in-memory key lookup |
| Dynamic code gen | `call execute` | Runtime-generated SAS; needs procedural rewrite |
| Statistical PROCs | `proc reg`, `proc glm`, `proc logistic`, `proc cluster`, `proc factor`, `proc phreg`, `proc lifetest`, `proc mixed`, `proc genmod`, `proc nlmixed` | Requires ML/stats libraries, not SQL |
| Stateful DO loops | `do until` / `do while` + `symput` or many `call ` | External state mutation across iterations |

### Tier 2 signals (procedural — Stored Procedure)

| Construct | What to grep for | Why it's complex |
|-----------|------------------|------------------|
| RETAIN w/ reset | `retain ` + `first.` + (`= 0` or `= .`) | Running totals with conditional reset |
| FIRST./LAST. + multi-OUTPUT | `first.`/`last.` + 2+ `output ` | BY-group splitting into multiple datasets |
| Multiple OUTPUT datasets | 2+ `output ` (not `output;`) | One DATA step writing several tables |
| Complex branching | >5 `if `/`when ` **in a DATA step** (not PROC SQL CASE WHEN) | Dense procedural conditional logic |
| Sequential DML | 3+ of `delete `/`insert `/`update ` | Multi-statement procedural mutation |

### Tier 1 advanced (SQL-translatable, but non-trivial)

`retain `, `array `, `merge `, `first.`/`last.`, `%do `, `%if `, `infile `, `ods ` —
translatable to window functions / CTEs but worth calling out as complexity drivers.

### Confidence reducers (raise risk even within Tier 1)

| Signal | What to grep for | Effect |
|--------|------------------|--------|
| Nested/heavy macros | >2 `%macro` | LOW confidence |
| Dynamic %INCLUDE | `%include` + `&` | LOW confidence (resolved at runtime) |
| External DB engines | `oracle`, `teradata`, `db2`, `sqlsvr`, `odbc`, `oledb` | LOW confidence; passthrough/function mapping |
| Date interval funcs | `intck`, `intnx` | MEDIUM confidence; SAS vs Snowflake alignment differs |
| NOTSORTED BY | `notsorted` | MEDIUM confidence; ordering assumptions |

---

## Boilerplate Discount

DI Studio / DataFlow-generated files contain large volumes of scaffolding. Do NOT treat these
as genuine complexity. Indicators (3+ present ⇒ file is boilerplate-heavy):
`etls_`, `sas data integration studio`, `%macro rcset`, `perfinit`, `log4sas`, `armsubsys`.

Boilerplate macro names to ignore when counting business logic: `rcset`, `rcsetds`,
`etls_startperformancestats`, `etls_setdebug`, `etls_recordcount`, `etls_endperformancestats`,
`etls_recordtable`, `etls_getrecordcount`, `etls_jobstatus`, `etls_logerror`.

When a file is boilerplate-heavy, describe it as "high line count, low business complexity"
so the narrative matches the CLI's discounted score.

---

## Producing the Portfolio Narrative

1. **Identify themes**: aggregate construct findings across all files. Report the *theme*,
   the *count of files* affected, and the *migration implication* — not a per-file dump.
2. **Top complex files**: name the 5-10 highest-complexity files (use CLI `overall_score` when
   available; otherwise rank by Tier 3/2 construct density × volume). One line each on the
   dominant complexity driver.
3. **Construct hotspots**: a short table of the most impactful construct categories present,
   with file counts and the recommended target (SQL / SP / PySpark).
4. **Cross-cutting risks**: external DB dependencies, dynamic %INCLUDE, statistical modeling,
   and any circular cross-file dependencies — these gate the migration approach.

Keep it concise. This is a summary, not a per-block audit. If the user needs block-level
detail, that is the job of the `convert-sas-to-snowflake` skill.
