# SSC-EWI-INF0050 — User-Defined Function Call Not Converted

An Informatica PowerCenter **user-defined function** (a `:UDF.<name>` call in a mapping expression) has no
built-in Snowflake counterpart, so SnowConvert left the call in place and flagged it. The
`!!!RESOLVE EWI!!!` marker **breaks compilation**, and the call it wraps (for example `ISBLANK(...)`) is not
a Snowflake function either, so both the marker and the call have to be resolved.

This is one of the highest-frequency compilation-breaking markers in real Informatica output: a single
mapping can carry dozens of occurrences of the *same* UDF, because the function is reused across
expressions. Fix them consistently.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** — and the wrapped call is also invalid Snowflake SQL |
| Frequency | **High** — repeats once per call site, often tens per mapping |
| Common action | Replace the UDF call with its inline Snowflake equivalent, identically at every call site |

## Identification

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0050 - INFORMATICA POWERCENTER USER-DEFINED FUNCTION CALL ':UDF.<NAME>' WAS NOT CONVERTED. REVIEW AND MANUALLY MAP TO AN EQUIVALENT SNOWFLAKE FUNCTION. ***/!!!
<the unconverted call, e.g. ISBLANK(SOME_COLUMN)>
```

The marker names the original function as `:UDF.<NAME>`. The line immediately after it is the call that
must be rewritten. Because these sit **inside expressions** (a `CASE`/`WHEN` condition, a `WHERE` clause,
a derived column), the replacement has to keep the expression's shape and operator precedence intact.

## Decision Tree

1. **Find the UDF's definition in the source.** In the mapping/repository XML, locate the
   `<EXPRESSION>`/UDF definition for `<NAME>`. That definition — not a guess from the name — is the
   contract you are reproducing.
2. **Is it a known blank/empty test (`ISBLANK`, `IS_EMPTY`, `ISNULLOREMPTY`)?** Use the canonical rewrite
   in Pattern 1. Confirm whether the source treats whitespace-only values as blank before choosing the
   form.
3. **Does it wrap a function Snowflake has natively?** Map it directly
   (`ISNULL` → `NVL`/`COALESCE`, `IIF` → `IFF`, `DECODE` → `CASE`, `LTRIM(RTRIM(x))` → `TRIM(x)`).
4. **Is it genuinely custom business logic?** Inline the expression if it is small, or create one
   Snowflake UDF and call it from every site. Prefer inlining for one-liners; prefer a real UDF when the
   logic is long or reused across models, so the definition lives in exactly one place.
5. **Cannot determine the definition from the source?** Mark the node needs-user with the UDF name and
   every call site. Do **not** guess semantics for a function you cannot read — a wrong blank/NULL test
   silently changes row counts.

## Fix Patterns

### Pattern 1: `ISBLANK` — the common case

Informatica's blank test is true for NULL **and** for empty/whitespace-only text. Snowflake has no
`ISBLANK`, so express it directly:

```sql
-- Before (breaks compilation; ISBLANK is not a Snowflake function)
WHEN (
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0050 - INFORMATICA POWERCENTER USER-DEFINED FUNCTION CALL ':UDF.ISBLANK' WAS NOT CONVERTED. REVIEW AND MANUALLY MAP TO AN EQUIVALENT SNOWFLAKE FUNCTION. ***/!!!
ISBLANK(PARTY_TYPE)
OR LTRIM(RTRIM(PARTY_TYPE)) = '')

-- After (marker removed, call rewritten, expression shape preserved)
WHEN (PARTY_TYPE IS NULL OR TRIM(PARTY_TYPE) = '')
```

Note the converter often emits a hand-written whitespace check next to the UDF call
(`LTRIM(RTRIM(x)) = ''`). Once `ISBLANK(x)` becomes `x IS NULL OR TRIM(x) = ''`, that neighbouring check
is usually redundant — collapse the two into the single condition above rather than leaving both.

Keep the negation correct. `NOT ISBLANK(x)` becomes:

```sql
(x IS NOT NULL AND TRIM(x) <> '')
```

Wrap the replacement in parentheses whenever it sits next to `AND`/`OR`/`NOT`. `x IS NULL OR TRIM(x) = ''`
without parentheses changes the meaning of the surrounding boolean expression.

### Pattern 2: UDF that maps to a native Snowflake function

```sql
-- Before
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0050 - ... ':UDF.NVL2' WAS NOT CONVERTED. ... ***/!!!
NVL2(DISCOUNT_PCT, DISCOUNT_PCT, 0)

-- After
IFF(DISCOUNT_PCT IS NOT NULL, DISCOUNT_PCT, 0)
```

### Pattern 3: Custom logic reused across many call sites

```sql
-- Define once (in the project's macro/UDF layer), then call it everywhere:
CREATE OR REPLACE FUNCTION normalize_party_code(P_CODE VARCHAR)
RETURNS VARCHAR
AS $$ UPPER(TRIM(REGEXP_REPLACE(P_CODE, '[^A-Za-z0-9]', ''))) $$;

-- Call site, marker removed
normalize_party_code(PARTY_CODE)
```

### Pattern 4: Definition unavailable — escalate, do not guess

```sql
-- After (compiles is NOT the goal here; correctness is unknown)
-- NEEDS-USER: Informatica user-defined function :UDF.CALC_RISK_TIER could not be located in the
-- supplied source. Its definition is required to reproduce the semantics. Call sites in this model:
-- lines 118, 204, 291. Do not deploy until resolved.
```

## Vertical-tab caveat (whitespace edge case)

If the source's blank test relies on Informatica's `IS_SPACES`, be aware Informatica counts a vertical tab
(`CHR(11)`) as whitespace while Snowflake's `\s` in `REGEXP_LIKE` does not. `TRIM()` is sufficient for
ordinary spaces and tabs. Only reach for an explicit character class when the data genuinely contains
vertical tabs — SnowConvert emits `SSC-FDM-INF0048` as an annotation where this applies, and that
annotation needs no code change on its own.

## Key Points

- **Must** remove every `!!!RESOLVE EWI!!!` line — each one breaks compilation.
- **Must** also rewrite the call underneath it; deleting only the marker leaves invalid SQL.
- Derive the semantics from the UDF's definition in the source, never from its name alone.
- Apply the **same** rewrite at every call site in the unit. Inconsistent variants of the same fix are a
  review burden and hide real differences.
- Preserve parentheses and operator precedence — these calls live inside larger boolean expressions.
- Compilation success does not prove correctness here: a wrong blank/NULL test compiles cleanly and
  silently changes which rows survive. Validate against source-derived expected results.
