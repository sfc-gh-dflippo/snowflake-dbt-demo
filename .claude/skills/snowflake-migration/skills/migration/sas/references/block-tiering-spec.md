# Canonical Block Counting & Tiering Spec (Shared)

> © Snowflake Inc. Proprietary. See License-Skills for complete terms.

This is the **single source of truth** for how a SAS file is broken into code blocks,
how each block is assigned a translation tier, and how a file's overall tier is derived.

Both SAS skills MUST follow this spec so their outputs agree:

- `assess-sas-migration` — the Python CLI (`tool/sas_analyzer/`) is the executable implementation.
- `convert-sas-to-snowflake` — the LLM-driven conversion workflow classifies blocks by hand.

If the CLI and the conversion skill ever disagree on block count or tier for the same file,
that is a bug in whichever one deviates from this spec.

---

## 1. What counts as a code block

Start from the parsed SAS constructs, then apply the rules below **in order**:

1. **Flatten macros.** A `%MACRO ... %MEND` definition is NOT a single opaque block.
   Enumerate each `DATA` step and `PROC` step **inside** the macro body as its own block,
   exactly as the conversion skill reads and converts them.
   - The macro shell itself counts as **one** block ONLY when it contains **zero** countable
     inner blocks (i.e. it is pure macro-language logic such as `%IF`/`%DO`/`%LET` with no
     DATA/PROC step). This prevents double-counting a wrapper macro alongside its children.

2. **Skip non-code block types.** Never count:
   `%LET` statements, comments, `LIBNAME` statements, and bare macro **calls** (`%name;`).
   (These map to `LET_STATEMENT`, `COMMENT`, `LIBNAME`, `MACRO_CALL` in the parser.)

3. **Exclude boilerplate.** DI Studio / DataFlow scaffolding is generated noise, not migration
   work. Exclude boilerplate blocks (and any blocks nested inside a boilerplate macro) from
   BOTH the block count AND tiering. Boilerplate is identified by:
   - **Macro names:** `rcset`, `rcsetds`, `etls_startperformancestats`, `etls_setdebug`,
     `etls_recordcount`, `etls_endperformancestats`, `etls_recordtable`,
     `etls_getrecordcount`, `etls_jobstatus`, `etls_logerror`.
   - **Content indicators:** `etls_`, `%macro rcset`, `perfinit`, `log4sas`, `armsubsys`,
     `sas data integration studio`.

The set of blocks surviving rules 1-3 is the **countable block set**. Every count the skills
report — portfolio total, per-file count, and per-tier distribution — is computed over this
exact same set, so they always reconcile.

> Note on complexity scoring: the LOW/MEDIUM/HIGH **complexity score** may additionally
> *discount* boilerplate rather than fully exclude it, but the **block count** and **tier**
> always use the countable block set defined above.

---

## 2. Per-block tier rules

Classify each countable block by scanning its (lowercased) content. Evaluate tiers
top-down; the first match wins. Tier 1 (pure SQL) is the default.

### Tier 3 — PySpark / SCOS notebook (last resort)

Any ONE of:

- `declare hash` — HASH objects, no SQL equivalent.
- `call execute` — dynamic code generation at runtime.
- `do until` / `do while` **with** external state (`symput`, or more than 2 `call ` statements).
- Statistical modeling PROC — any of:
  `proc reg`, `proc glm`, `proc logistic`, `proc cluster`, `proc factor`, `proc phreg`,
  `proc lifetest`, `proc surveyselect`, `proc mixed`, `proc genmod`, `proc nlmixed`.

### Tier 2 — Snowflake stored procedure

Any ONE of (when no Tier-3 trigger matched):

- `retain` + `first.` + conditional reset (`= 0` or `= .`).
- `first.` or `last.` **with** more than one `output ` statement.
- More than one `output ` destination and no plain `output;`.
- **In a DATA step**, more than 5 `if ` or more than 5 `when ` (SELECT/WHEN) branches.
- 3+ sequential DML operations (`delete `/`insert `/`update ` — 3 or more distinct kinds present).

> A PROC SQL `CASE WHEN` expression is pure SQL (Tier 1), no matter how many `WHEN` clauses —
> the branch-count rule above applies to **DATA steps only**, never to PROC SQL or other block
> types.

### Tier 1 — Pure SQL (default)

Everything else: PROC SQL, PROC SORT, simple DATA steps, MERGE, ARRAY, RETAIN running totals,
`%DO` loops, etc. — translatable with CTAS, CTEs, and window functions.

---

## 3. File-level tier (strict "any-block" rule)

A file's `primary_tier` is driven by its **most demanding** countable block — matching the
conversion skill, where a single Tier-3 block forces a notebook:

```
if any countable block is Tier 3:  primary_tier = TIER_3_PYSPARK
elif any countable block is Tier 2: primary_tier = TIER_2_SP
else:                               primary_tier = TIER_1_SQL
```

There are **no proportion thresholds.** One genuine (non-boilerplate) HASH block in a
50-block file makes the whole file Tier 3, because conversion will emit a notebook for it.
The boilerplate exclusion in Section 1 is what prevents a stray scaffolding HASH from
promoting an entire generated file.

---

## 4. Confidence

Assess translation confidence per block (or per file, taking the lowest):

- **LOW:** more than 2 `%macro` (nested macros); `%include` with a dynamic path (`&`);
  external DB engine present — any of
  `sqlsvr`, `mssql`, `sql server`, `oracle`, `teradata`, `odbc`, `oledb`, `db2`,
  `postgres`, `mysql`, `dsn=`.
- **MEDIUM:** complex date manipulation (`intck`, `intnx`, `datepart`); `notsorted` BY-groups.
- **HIGH:** everything else (standard patterns with direct mappings).

---

## 5. Translation tier vs complexity — two independent axes

Do not conflate these:

- **Translation tier (Tier 1/2/3):** *how* a block is migrated (SQL / stored proc / notebook).
  Governed entirely by Sections 2-3 above.
- **Complexity level (LOW/MEDIUM/HIGH):** a volume/effort score used only by the assessment
  skill for sizing and wave planning. It has no analog in the conversion skill and does NOT
  affect tier.

A file can be Tier 1 (pure SQL) yet HIGH complexity (large, many joins), or Tier 3 yet LOW
complexity (small file with one HASH lookup).
