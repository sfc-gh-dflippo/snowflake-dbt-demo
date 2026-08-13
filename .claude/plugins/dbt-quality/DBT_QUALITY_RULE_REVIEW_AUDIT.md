# Independent Audit of DBT_QUALITY_RULE_REVIEW.md

## Summary

I checked every substantive local `file:line` citation in the report against the actual repository
contents, verified rule-ID-to-implementation mappings, and confirmed the report satisfies the three
structural requirements (package-policy scope, catalog.json size-vs-clustering distinction, and
presence of concrete recommended changes/acceptance criteria). Of roughly 30 checkable citations,
the large majority are accurate — several to the exact line — but I found one clear citation-to-code
mismatch (Major) and one off-by-one line citation (Minor). No fabricated rule IDs or fabricated code
behavior were found.

## Findings

### Major — Finding #4 citation points to the wrong lines for the claimed behavior

**Report line:** 113 (`(scripts/src/dbt_quality/rules/mat.py:220-240)`) **Evidence:** Lines 220–240
of `mat.py` are the `@rule(...)` decorator for `MAT_CLUSTERING` plus the start of `clustering()`
through the `if cluster_by:` branch guard (the case where a `cluster_by` **is** already configured,
handling the "over-specified" / too-many-columns path). The behavior the report describes — "treats
an incremental table or fact-like model with no `cluster_by` as a candidate" — is implemented in the
_other_ branch, `if FACT_NAME_PATTERN.match(model.name) or model.is_incremental:` at lines 263–282
(verified:
`yield make_suggestion(MAT_CLUSTERING, "Check table size and query filter patterns before adding a \`cluster_by\`...")`). **Implication:** A reader following the citation to verify the claim lands on the wrong code (the over-specified-key branch, not the missing-key branch). The underlying claim itself is correct — the missing-cluster_by branch really does fire off `FACT_NAME_PATTERN`or`is_incremental`alone, with no size evidence — but the citation would need to be`mat.py:263-282`(or`220-282`
to cover the whole rule) to actually support it. **Confidence:** High.

### Minor — off-by-one line citation in Finding #9

**Report line:** 236 (`(scripts/src/dbt_quality/rules/tst.py:59)`) **Evidence:**
`KEY_COLUMN_PATTERN = re.compile(r"(.*_id|.*_key|id|.*_sk|fk_.*|.*_fk)$", re.IGNORECASE)` is at line
**60**, not 59, confirmed via `grep -n KEY_COLUMN_PATTERN scripts/src/dbt_quality/rules/tst.py` →
`60:KEY_COLUMN_PATTERN = ...`. **Implication:** Trivial for a human reader (adjacent line, same
statement block) but technically inaccurate. **Confidence:** High.

### Minor — loosely-scoped citation in Finding #12

**Report line:** 277 (`(scripts/src/dbt_quality/provenance.py:51-59)`) **Evidence:** Line 51 is the
`STG_RAW_PATTERN` comment, unrelated to the claim. The `ETL_INSTANCE_PATTERN` regex that actually
contains the generic prefixes `AGG`, `SEQ`, `SP`, `UNI`, `TRANS` spans lines 55–59 (comment at 55,
`re.compile(` at 56, the prefix alternation at 57, `re.IGNORECASE,` at 58, closing `)` at 59). The
citation's end (59) is exactly right; its start (51) is four lines too early and includes an
unrelated pattern. **Implication:** Does not change the validity of the underlying claim (all five
named prefixes — AGG, SEQ, SP, UNI, TRANS — are present in `ETL_INSTANCE_PATTERN`, confirmed) but
the range is imprecise. **Confidence:** High.

## Verified-accurate citations (spot-checked, no issues)

All of the following were checked by reading the exact cited line range and comparing it against the
report's description of the code's behavior. All matched:

- `inc.py:122-129` (`VALID_STRATEGIES` includes `"microbatch"`) — exact.
- `inc.py:491-515` (`no_incremental_guard`, `INC_NO_GUARD` / `SSC-PRF-DBTINC0006`) — exact function
  bounds; confirmed it does **not** call `_reads_stream()`, unlike the two rules below — this
  substantiates Finding #2's core claim of an inconsistency.
- `inc.py:620-650` (`no_watermark`, `INC_NO_WATERMARK` / `SSC-PRF-DBTINC0009`) — exact function
  bounds; confirmed `if _reads_stream(model): return` at line 623, inside the cited range.
- `inc.py:667-706` (`unbounded_scan`, `INC_UNBOUNDED_SCAN` / `SSC-PRF-DBTINC0013`) — exact function
  bounds; confirmed the stream-exemption call at line 670, inside the cited range.
- `inc.py:99-119` (stream-tracking comment + `STREAM_PATTERN` + `_reads_stream()`) — accurate.
- `mat.py:150-217` (`passthrough_chain`, `MAT_PASSTHROUGH_CHAIN`) — exact rule+function bounds.
  Default `passthrough_chain_threshold = 3` confirmed in `discovery.py:96`, substantiating "flags a
  chain of three models."
- `prj.py:379-425` (`missing_packages`, `PRJ_MISSING_PACKAGES` / `SSC-EWI-DBTPRJ0007`) — confirmed
  `EXPECTED_PACKAGES = {"dbt_utils": "dbt-labs/dbt_utils", "dbt_constraints": "Snowflake-Labs/dbt_constraints"}`
  at lines 53–56, and the docstring literally calls both "baseline in this estate."
- `sql.py:422-463` (`hardcoded_ref`, `SQL_HARDCODED_REF` / `SSC-EWI-DBTSQL0006`) — exact bounds;
  confirmed `level=Level.ERROR, severity=Severity.HIGH` and that the only exemptions are local CTE
  names and `table./lateral./values.` prefixes — no `ACCOUNT_USAGE`/`ORGANIZATION_USAGE`/
  `INFORMATION_SCHEMA` exemption anywhere in this rule.
- The claimed inconsistency vs. the macro detector is real: `mac.py`'s `macro_hardcoded_relation`
  (lines 358–398) exempts `("information_schema.", "snowflake.", "table.")` at lines 377–380 — this
  is the "analogous macro detector" the report refers to, confirmed case-insensitively via
  `.lower().startswith(...)`.
- `ops.py:133-175` (`credentials`, `OPS_CREDENTIALS` / `SSC-EWI-DBTOPS0002`) — exact bounds;
  confirmed `level=Level.ERROR, severity=Severity.CRITICAL` while the emitted message opens with
  "Confirm the ... value ... is a real credential rather than a placeholder."
- `test_rules.py:978-1001` (`test_error_level_implies_a_direct_message`) — exact function start;
  confirmed the fixture is
  `add_model(root, "gold/dim_a.sql", "select 1 as id from analytics.public.t")` — a
  hardcoded-relation fixture — and no `profiles.yml`/`dbt_project.yml` credential fixture is
  created, so `OPS_CREDENTIALS` indeed cannot fire in this test.
- `mac.py:57-79` (`UTIL_REIMPLEMENTATIONS` list) — exact bounds; confirmed `md5\s*\(\s*concat` →
  `dbt_utils.generate_surrogate_key` and `sum\s*\(\s*case\s+when.*then\s+1\s+else\s+0\s+end\s*\)` →
  `dbt_utils.pivot`.
- `doc.py:240-247` (`_has_persist_docs`) — exact bounds; confirmed it returns `True` for any truthy
  value at any nesting level, i.e. `{relation: false, columns: false}` would need each leaf checked
  but a mapping with any truthy leaf trips it (matches claim).
- `doc.py:264-273` (exposures substring scan) — function/block bounds correct; the actual
  `"exposures" in path.read_text(...)` check is at line 268, within range.
- `provenance.py` `ETL_INSTANCE_PATTERN` — prefixes `AGG|SP|UNI|TRANS|SEQ` all present (line 57),
  confirming the substance of Finding #12 even though the cited range starts 4 lines early (see
  Minor finding above).
- `core/base.py:53-71` (`Level` docstring) — exact: class starts at 53, docstring's closing sentence
  ("or the reverse.") is at line 71.
- `core/base.py:163-179` (`Tier` docstring + class body) — exact: class starts at 163,
  `MIGRATION: str = "migration"` is at line 179.
- `skills/dbt-audit/references/rule-catalog.md:209-235` ("Names are not audited") — exact: header at
  209, closing word "declared." at 235.
- `skills/dbt-audit/references/rule-catalog.md:320-334` (positive/negative test requirement) — range
  correct; "Add both a positive and a negative test" is at line 332, inside range.
- Rule-ID-to-implementation mapping spot checks — all correct: `SSC-EWI-DBTTST0004` =
  `TST_FACT_NO_FK`, `SSC-EWI-DBTTST0012` = `TST_KEY_COLUMN_UNTESTED`, `SSC-EWI-DBTDOC0004` =
  `DOC_NO_PERSIST_DOCS`, `SSC-EWI-DBTDOC0005` = `DOC_NO_EXPOSURES`, `SSC-EWI-DBTTST0008` =
  `TST_NO_STORE_FAILURES`, `SSC-EWI-DBTTST0010` = `TST_ORPHAN_MODEL`.
- `tst.py:483-515` (`TST_ORPHAN_MODEL` decorator + missing-schema-entry branch) — confirmed
  `level=Level.WARNING` (default) and the message "A trivial or ephemeral helper with no downstream
  consumers may not need one" sits inside the cited range.
- Table entries without citations, spot-checked against code anyway: `ARC0006`'s reference-count
  branch (`if len(model.sources) + len(model.refs) > 1: issues.append(...)`, fires independent of
  JOIN/aggregate — confirms the claim) and `MAT0008`'s analytical-library allowlist
  (`sklearn|scikit|scipy|statsmodels|xgboost|lightgbm|prophet|torch|tensorflow|numpy\.linalg` at
  mat.py:365-369) — both match their table descriptions.
- Phase 4 claim "the MAT pack lacks direct rule-code assertions": confirmed by exhaustive grep —
  zero occurrences of any `MAT_*` constant or `SSC-PRF-DBTMAT*`/`SSC-EWI-DBTMAT*` ID anywhere in
  `scripts/tests/test_rules.py`, and it is the only test file in the repo.

## Requirement checks (as specified in the audit brief)

1. **"Only Snowflake-Labs/dbt_constraints and Snowflake-Labs/dbt_semantic_view are required"** —
   Satisfied. Finding #5 (report lines 162–183) states this explicitly as the target end state and
   gives the concrete edit (replace `dbt_utils` with `dbt_semantic_view` in the expected-package map
   at `prj.py:53-56`, and stop treating `dbt_utils` absence as a finding). The Acceptance Criteria
   section (line 352–353) restates the same pair as the acceptance test.

2. **"catalog.json described as useful for size eligibility but insufficient to select clustering
   keys"** — Satisfied. Finding #4 (lines 109–161) has an explicit "What catalog evidence can
   support" / "cannot support" split: size/row-count/byte-size and staleness are listed as
   supportable; column-level predicate selectivity, scan/pruning metrics, clustering depth/overlap,
   and maintenance-cost justification are listed as _not_ supportable from catalog.json alone. This
   matches the catalog v1 schema's actual content (adapter-defined `stats` map with no guaranteed
   keys) as far as I can verify from the report's own description — I did not have network access to
   independently re-verify the dbt schema docs, so I treat the schema-shape claims (`stats` entries
   having `id`/`label`/`value`/ `include`/`description`, no guaranteed `num_rows`/`num_bytes`) as
   unverified against the external source; they are at least internally consistent with the rest of
   the report's defensive-parsing recommendations (item 2 under "Recommended change").

3. **"Concrete recommended changes and acceptance criteria are included"** — Satisfied. Every
   numbered finding (1–12) ends with a "Recommended change" subsection giving specific, actionable
   edits (e.g., "Short-circuit conventional guard... when `incremental_strategy == 'microbatch'`",
   "apply the existing stream exemption to `INC0006`"). A dedicated "Acceptance criteria for the
   rule changes" section (lines 345–358) gives ten testable pass/fail statements tied back to the
   findings (e.g., "A documented microbatch model emits no conventional incremental watermark
   suggestions").

## Gaps

- I did not execute the test suite or the rule engine; all checks were static (reading source
  against the report's prose). If `REGISTRY`/`@rule` metadata is mutated at runtime in a way not
  visible from the decorator arguments, that would not be caught here — I saw no evidence of this in
  the modules read.
- I did not independently re-verify the dbt Core / Fusion catalog-v1 schema claims (stats shape,
  `dbt compile --write-catalog` flag) against getdbt.com; those are external-documentation claims,
  not local-repository claims, and were out of scope for "local file:line citation" verification per
  the audit brief. Flagged above under requirement #2 as an unverified-but- plausible external
  claim.
- I did not check every one of the ~150 rules in the plugin against the report — I verified all
  citations that the report actually makes (a complete set) plus a sample of uncited table entries
  (`ARC0006`, `MAT0008`) as a spot check. I did not independently audit rules the report did not
  mention.

## Recommendation

The report is substantively accurate and well-evidenced. Fix the two citation issues before treating
the document as a citation-verified reference:

1. Correct `mat.py:220-240` → `mat.py:263-282` (or widen to `220-282`) in Finding #4, so the
   citation actually points at the missing-`cluster_by` branch it describes.
2. Correct `tst.py:59` → `tst.py:60` in Finding #9.
3. Optionally tighten `provenance.py:51-59` → `provenance.py:55-59` in Finding #12 to drop the
   unrelated `STG_RAW_PATTERN` line.

No blocker-level issues found. No fabricated rule IDs, fabricated file paths, or claims contradicted
by the code were identified.
