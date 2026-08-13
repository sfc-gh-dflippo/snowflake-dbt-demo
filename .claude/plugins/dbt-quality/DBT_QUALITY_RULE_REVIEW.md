# Independent Review of dbt Quality Rules

## Executive summary

The plugin has a sound rule framework: each suggestion separates confidence (`level`), potential
impact (`severity`), issue family (`kind`), and applicability (`tier`). The implementation also
contains several unusually careful false-positive guards. This repository and plugin are
Snowflake-only, so Snowflake-specific packages, system schemas, materializations, and catalog
statistics are valid defaults rather than optional adapter branches. The principal weakness is not
the framework but the classification and evidence behind individual rules. Some team conventions are
labeled universal, some static heuristics make performance recommendations that require runtime
evidence, and several detectors do not account for supported dbt behavior.

The highest-priority changes are:

1. Exempt microbatch and Snowflake stream models from conventional incremental watermark rules.
2. Stop treating a three-node linear DAG as proof of pass-through model explosion.
3. Make missing clustering guidance conditional on physical table size from `catalog.json`, and
   require workload evidence before recommending clustering columns.
4. Correct the package policy to require only Snowflake Labs' `dbt_constraints` and
   `dbt_semantic_view` packages.
5. Reclassify style and team-policy rules so they are not presented as correctness rules, while
   keeping Snowflake-specific requirements as normal plugin defaults.
6. Close the large gap between the catalogue's positive-and-negative test requirement and actual
   per-rule test coverage.

## Scope and review method

This review examined:

- all ten rule packs under `scripts/src/dbt_quality/rules/`;
- the rule metadata and execution contracts in `core/base.py`, `engine.py`, and `scoring.py`;
- migration provenance detection in `provenance.py`;
- the live rule catalogue and plugin guidance; and
- detector tests in `scripts/tests/test_rules.py`.

The review distinguishes four kinds of guidance:

| Class        | Required evidence                                       | Appropriate default              |
| ------------ | ------------------------------------------------------- | -------------------------------- |
| Correctness  | The observed construct is invalid or changes results    | Universal; warning or error      |
| Performance  | Physical size, execution cost, or workload behavior     | Evidence-gated; informational    |
| Architecture | A coherent project-design convention                    | Architecture tier; informational |
| Team policy  | A local requirement beyond Snowflake or dbt correctness | Explicitly labeled policy        |

This distinction matters because the engine describes `error` as having no legitimate correct
condition and `information` as context-dependent (`scripts/src/dbt_quality/core/base.py:53-71`). It
also describes `universal` as always applicable and `architecture` as a greenfield ideal
(`scripts/src/dbt_quality/core/base.py:163-179`). The recommendations below apply those contracts to
the rules themselves.

## Implementation principle

The implementation should prefer deletion, early-return guards, and clearer messages over new
classifiers, artifact frameworks, or more speculative detection. If the existing source text or
manifest cannot establish the claim reliably, the linter should either remove the rule or ask the
audit agent to investigate the project, `target/catalog.json`, and query behavior before offering
guidance.

This means catalog data remains audit-agent evidence for clustering and `source()` versus `ref()`
questions; it is not a new analyzer prerequisite or rule engine. The existing `disabled_rules`
configuration is the mechanism for suppressing any exact rule ID. The implementation should add
focused tests and documentation for that existing path, not a second suppression system.

## Findings and recommended changes

### 1. Incremental rules do not recognize microbatch semantics

**Rules:** `SSC-PRF-DBTINC0006`, `SSC-PRF-DBTINC0009`, `SSC-PRF-DBTINC0013`

The plugin recognizes `microbatch` as a valid strategy
(`scripts/src/dbt_quality/rules/inc.py:122-129`) but still expects an `is_incremental()` guard and a
`{{ this }}` watermark (`scripts/src/dbt_quality/rules/inc.py:491-515`,
`scripts/src/dbt_quality/rules/inc.py:620-650`, and `scripts/src/dbt_quality/rules/inc.py:667-706`).
This advice is incorrect for a microbatch model. dbt Core 1.9 and later automatically filters
parents with `event_time`; authors are specifically not expected to write conventional
`is_incremental()` filtering. See dbt's
[microbatch documentation](https://docs.getdbt.com/docs/build/incremental-microbatch).

**Recommended change:**

- Short-circuit conventional guard, target-watermark, and absolute-floor rules when
  `incremental_strategy == "microbatch"`.
- Add microbatch-specific validation for required `event_time`, `begin`, and `batch_size` configs.
- Check whether direct parents that should be filtered declare `event_time`; this is the actual
  full-scan risk for microbatch models.
- Add positive and negative tests using the documented Fusion/Core microbatch form.

### 2. Stream handling is inconsistent inside the incremental pack

**Rule:** `SSC-PRF-DBTINC0006`

The pack correctly explains that Snowflake streams track their own consumption offset and defines
`_reads_stream()` for that reason (`scripts/src/dbt_quality/rules/inc.py:99-119`). The watermark and
unbounded-scan rules use this exemption (`scripts/src/dbt_quality/rules/inc.py:620-624` and
`scripts/src/dbt_quality/rules/inc.py:667-671`), but the missing-guard rule does not
(`scripts/src/dbt_quality/rules/inc.py:491-515`). A valid stream-backed incremental model is
therefore told it rescans its full source.

**Recommended change:** apply the existing stream exemption to `INC0006` and add one fixture that
proves all conventional watermark rules remain silent for a stream consumer.

### 3. Linear DAG topology is not proof of pass-through model explosion

**Rule:** `SSC-PRF-DBTMAT0003`

The detector walks any single-parent/single-child chain and flags a chain of three models
(`scripts/src/dbt_quality/rules/mat.py:150-217`). It does not inspect whether those models are
pass-throughs. A normal `staging -> intermediate -> mart` pipeline therefore exactly matches the
default signal, even where the intermediate model re-grains or isolates complex logic. dbt's
[intermediate-model guidance](https://docs.getdbt.com/best-practices/how-we-structure/3-intermediate)
explicitly recommends intermediate models for those purposes.

**Recommended change:**

- Do not use graph topology alone.
- Require evidence that intermediate nodes are structurally pass-through: one upstream relation, no
  aggregate, window, join, filter, grain change, or substantive expression.
- Alternatively, limit the rule to repeated same-layer chains and exempt deliberate
  staging-to-intermediate-to-mart boundaries.
- Retain `information/medium`; this remains an optimization prompt, not a defect.

### 4. Static model shape cannot justify a Snowflake clustering recommendation

**Rule:** `SSC-PRF-DBTMAT0004`

The current rule treats an incremental table or fact-like model with no `cluster_by` as a candidate
(`scripts/src/dbt_quality/rules/mat.py:263-282`). That is not enough evidence. Snowflake generally
starts with naturally organized micro-partitions; clustering adds maintenance cost and should be
driven by table scale, clustering depth, pruning behavior, and repeated selective predicates.

The repository's actual `target/catalog.json`, generated on 2026-08-13 by dbt Fusion
`2.0.0-preview.205`, confirms that Snowflake provides the metadata needed to make the first part of
this rule evidence-based. The artifact contains 48 dbt nodes and 10 sources. For physical relations,
Snowflake emits these stats:

| Stat ID         | Meaning                                         | Coverage in this catalog   |
| --------------- | ----------------------------------------------- | -------------------------- |
| `has_stats`     | Whether physical statistics are available       | 48/48 nodes, 10/10 sources |
| `bytes`         | Approximate relation size reported by Snowflake | 47/48 nodes, 9/10 sources  |
| `row_count`     | Approximate row count                           | 47/48 nodes, 9/10 sources  |
| `last_modified` | Last update/change timestamp                    | 47/48 nodes, 9/10 sources  |

The one node and one source without physical stats are views. Of the 48 nodes, 34 have nonzero
`bytes` and `row_count`. The largest model in this catalog is
`model.snowflake_demo.fct_order_lines`, with 6,001,215 rows and approximately 262 MB. The artifact
also distinguishes `BASE TABLE`, `DYNAMIC TABLE`, and `VIEW`, and supplies database, schema,
relation name, owner, comments, and column types/comments. These observations come from
`target/catalog.json`; they are not inferred from the generic catalog schema.

Catalog schema v1 defines each node's relation metadata, columns, and `stats` map. See dbt's
[catalog artifact reference](https://docs.getdbt.com/reference/artifacts/catalog-json) and the
[catalog v1 schema](https://schemas.getdbt.com/dbt/catalog/v1.json). Fusion writes this artifact
with:

```bash
dbt compile --write-catalog
```

The generic schema permits arbitrary stat IDs, but this plugin is Snowflake-only and the actual
Fusion catalog establishes the Snowflake contract to consume: `has_stats`, `bytes`, `row_count`, and
`last_modified`. The parser should read those exact IDs and remain tolerant of a missing stat for
views or metadata-query failures.

**What catalog evidence can support:**

- The physical relation exists.
- Adapter-provided row-count or byte-size statistics indicate whether the table is materially large.
- Catalog generation time can be used to identify stale evidence.

**What catalog evidence cannot support:**

- Which columns appear in selective query predicates.
- Bytes scanned, partitions pruned, or cache behavior for actual queries.
- Clustering depth or overlap for candidate keys.
- Whether clustering maintenance cost is justified.

**Recommended change:**

1. Load `target/catalog.json` when available and join nodes by manifest/catalog `unique_id`.
2. Read Snowflake's `has_stats`, `bytes`, `row_count`, and `last_modified` values. Include the
   catalog generation timestamp so users can judge freshness.
3. Suppress the "missing cluster_by" suggestion for views and for tables below a configurable
   Snowflake size threshold. If the catalog or physical stats are unavailable, retain an
   informational finding but say that size could not be checked; do not imply the table is large.
4. Enrich every clustering-related message with available catalog facts: relation type, approximate
   rows, approximate bytes in human-readable form, last modified time, and whether a cluster key is
   already configured. For example: "6,001,215 rows, approximately 262 MB; no `cluster_by`. This
   table is measurable but not large enough by size alone to justify clustering."
5. Use catalog size only to say "investigate clustering," never to recommend a key.
6. Require separate Snowflake workload evidence before naming columns: recurring filter/join
   predicates, scan and pruning metrics, and `SYSTEM$CLUSTERING_INFORMATION` or equivalent
   clustering-depth evidence.
7. Retain the static check for an excessively long `cluster_by` list, but enrich its message with
   catalog size and keep it informational because expression complexity and workload shape matter
   more than a fixed column count.

### 5. The Snowflake package baseline names the wrong packages

**Rule:** `SSC-EWI-DBTPRJ0007`

The current implementation requires `dbt_utils` and `dbt_constraints`, explicitly calling them
"baseline in this estate" (`scripts/src/dbt_quality/rules/prj.py:379-425`). Because this plugin is
Snowflake-only, it can require a fixed Snowflake package baseline. That baseline should be only:

- [`Snowflake-Labs/dbt_constraints`](https://hub.getdbt.com/Snowflake-Labs/dbt_constraints/latest/)
- [`Snowflake-Labs/dbt_semantic_view`](https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/)

**Recommended change:**

- Replace `dbt_utils` with `dbt_semantic_view` in the expected-package map, message, rationale, and
  remediation example.
- State in the rule rationale that these are the plugin's required Snowflake packages. No adapter
  profile or configurability is needed.
- Remove `dbt_utils` absence as a finding. Individual rules may still suggest a package helper when
  they can accurately identify equivalent hand-written logic, but package installation itself is not
  mandatory.

### 6. Hardcoded relation detection has a legitimate system-schema exception

**Rule:** `SSC-EWI-DBTSQL0006`

The rule classifies every dotted literal relation as `error/high`, exempting only table functions,
lateral references, and values (`scripts/src/dbt_quality/rules/sql.py:422-463`). Direct references
to `SNOWFLAKE.ACCOUNT_USAGE`, `SNOWFLAKE.ORGANIZATION_USAGE`, and `INFORMATION_SCHEMA` are
legitimate and common. The analogous macro detector already has system-relation exemptions, so the
two rules are inconsistent.

**Recommended change:** exempt Snowflake system schemas consistently. For other literal relations,
use `information/high` unless project policy explicitly forbids them; a declared dbt `source()` is
preferable for lineage, but the SQL is not unconditionally invalid.

### 7. Literal credential detection contradicts the level contract

**Rule:** `SSC-EWI-DBTOPS0002`

The rule is `error/critical`, but its emitted message asks the reader to confirm whether the value
is actually a credential (`scripts/src/dbt_quality/rules/ops.py:133-175`). The detector matches key
names such as `token` or `secret`, so a noncredential scalar can be legitimate. The test intended to
enforce direct error messages only exercises a hardcoded-table fixture and therefore does not emit
this project-scoped finding (`scripts/tests/test_rules.py:978-1001`).

**Recommended change:** parse supported configuration shapes and distinguish verified literal
credential fields from ambiguous key names. Emit `error/critical` only for the verified subset; emit
`information/critical` for ambiguous cases. Add a fixture that actually emits every error-level rule
and verifies its message and detector preconditions.

### 8. Macro reimplementation patterns overclaim semantic equivalence

**Rule:** `SSC-EWI-DBTMAC0009`

The plugin maps `md5(concat(...))` to surrogate-key generation and any
`sum(case when ... then 1 else 0 end)` to a pivot (`scripts/src/dbt_quality/rules/mac.py:57-79`).
The first is also a normal hash-diff pattern for change detection; the second is ordinary
conditional aggregation and does not prove a dynamic pivot.

**Recommended change:**

- Keep the hash lint. Flag `MD5`, `SHA*`, `HASH`, or equivalent functions applied to fields that
  participate in a foreign key, because using a hashed relationship key harms Snowflake
  micro-partition pruning and makes joins less efficient than the natural key columns.
- Rewrite the message to distinguish that case from a hash-diff: an FK-derived hash should be
  replaced with the project's concatenated natural-key strategy or the original relationship
  columns; a hash-diff used solely for change detection is valid when it is not used as a join key.
- Remove the `sum(case when ... then 1 else 0 end)` pivot detector. Ordinary conditional aggregation
  is too common to justify a lint finding.
- Keep the remediation optional: `dbt_utils` is not required, so the message should recommend
  checking the existing project key convention rather than prescribing a package helper.

### 9. Key-shaped column detection is too broad

**Rules:** `SSC-EWI-DBTTST0004`, `SSC-EWI-DBTTST0012`

The shared pattern treats every `*_id` and `*_key` as relational-key evidence
(`scripts/src/dbt_quality/rules/tst.py:60`). That includes batch IDs, external IDs, transaction IDs,
session IDs, and operational identifiers. Two rules then report the same uncertain inference.

**Recommended change:** prefer manifest/schema evidence: match a column to a declared model key or
relationship target. If text heuristics remain as a fallback, exclude common operational and
degenerate identifiers and emit one informational suggestion rather than duplicate findings.

### 10. `persist_docs` and exposure detection contain concrete logic defects

**Rules:** `SSC-EWI-DBTDOC0004`, `SSC-EWI-DBTDOC0005`

`_has_persist_docs()` treats any non-empty mapping as enabled, including
`{relation: false, columns: false}` (`scripts/src/dbt_quality/rules/doc.py:240-247`). Exposure
detection searches for the substring `exposures` anywhere in YAML
(`scripts/src/dbt_quality/rules/doc.py:264-273`), so comments and descriptions can suppress the
finding.

**Recommended change:** inspect nested `relation` and `columns` booleans, and parse YAML for a real
top-level `exposures` collection.

### 11. Several team preferences are labeled universal correctness

The following are reasonable policies but not universal correctness rules:

| Rule or group                    | Why contextual                                                                                                          | Recommended classification                        |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Stylistic MAC rules              | Macro ratio, one caller, wrapper size, nesting, Jinja percentage, and filename matching are maintainability conventions | Architecture or convention tier                   |
| `TST0008`                        | dbt documents `store_failures` as optional and also supports the CLI flag                                               | Explicit operational policy                       |
| `DOC0005`                        | Exposures help only when downstream assets are represented in dbt                                                       | Architecture/information                          |
| `PRJ0002`                        | Separate domain-owned projects may intentionally read shared reference sources                                          | Information with stronger corroboration           |
| `ARC0006` reference-count branch | A staging model can legitimately union regional/source variants                                                         | Detect joins/aggregations, not source count alone |
| `MAT0008` library allowlist      | Python models have valid non-ML uses and Snowpark-only implementations                                                  | Remove allowlist or keep informational            |

`TST0010` also defaults to warning while its missing-schema-entry branch explicitly says a trivial
helper may be correct (`scripts/src/dbt_quality/rules/tst.py:483-515`). Split the rule: stale YAML
without a model is warning-worthy; a model without YAML is informational unless a project policy
requires complete documentation.

### 12. Migration provenance uses ambiguous model prefixes

The provenance score includes generic prefixes such as `AGG`, `SEQ`, `SP`, `UNI`, and `TRANS`
(`scripts/src/dbt_quality/provenance.py:55-59`). These can be ordinary business names. Although the
signal alone is below the migration threshold, it can combine with another weak signal and suppress
architecture findings.

**Recommended change:** only use converter-specific transformation abbreviations for provenance.
Generic prefixes may remain as informational migration-debt evidence after migration status has
already been established, but they should not help establish that status.

### 13. `source()` may refer to a dbt-managed relation

This is an audit-agent investigation, not a deterministic lint rule. When `target/catalog.json` is
available, compare a source relation and dbt node using exact Snowflake `database`, `schema`, and
relation `name`. If a source points to the same physical relation as a dbt model, seed, or snapshot,
the audit should ask whether it should use `ref()` to restore lineage and build ordering.

The finding must state the intentional exception: `source()` is correct when the relation is an
independently deployed contract boundary. Do not add catalog loading, staleness machinery, or a new
registry rule solely for this check.

### 14. Any exact lint rule ID can be disabled

The existing `.dbt-quality.yml` setting already accepts `disabled_rules`. It should remain the one
mechanism for disabling an exact registered rule ID across audit, lint, validate, strict linting,
and the editor hook. Disabled rules should produce no suggestion and appear as skipped with the
reason `disabled in .dbt-quality.yml`.

Add focused tests and documentation showing that any rule ID can be disabled. Do not add inline SQL
suppression comments, category wildcards, a second configuration format, or a large rule-validation
subsystem.

## Rules to retain

The following rules have strong signals and useful guards and should remain substantially intact:

- destructive DML hooks that target the dbt-managed relation;
- incomplete snapshot configuration;
- unresolved conversion errors, hand-off markers, and placeholder models;
- nondeterministic window ordering used for row selection;
- unused CTEs;
- build artifacts not ignored;
- artifact logging configured in a contradictory disabled state; and
- duplicate SQL logic where the detector fingerprints substantive normalized bodies across models.

The decision not to audit names should also remain. The catalogue correctly documents that dbt does
not provide the source-object identity required to distinguish a retained migration name from a new
name, and a rule without that fact would guess
(`skills/dbt-audit/references/rule-catalog.md:209-235`).

## Remediation plan

### Phase 1: Correct false positives and false negatives

1. Add microbatch and stream exemptions, then add microbatch-specific config checks.
2. Fix `persist_docs` boolean handling and YAML exposure detection.
3. Exempt Snowflake system schemas from hardcoded-relation errors.
4. Narrow credential and migration-provenance detectors.
5. Replace the package pair with `dbt_constraints` and `dbt_semantic_view`.
6. Keep FK-derived hash linting while removing the conditional-aggregation pivot heuristic.

### Phase 2: Reclassify evidence and policy

1. Label team conventions as policy rules without introducing adapter profiles; Snowflake remains
   the only supported platform.
2. Re-tier subjective MAC, exposure, failure-storage, package, and folder-default rules.
3. Ensure messages match confidence: direct statements for errors, narrow exceptions for warnings,
   and explicit correct-as-is conditions for information.
4. Remove category weights from remediation priority where they encode undocumented preferences;
   rank first by verified correctness and available evidence.

### Phase 3: Add artifact-backed performance guidance

1. Teach the audit agent to inspect `target/catalog.json` for rows, bytes, relation type, and last
   modified time when discussing clustering or `source()` versus `ref()`.
2. Keep these contextual questions out of the deterministic analyzer unless a small existing helper
   can answer them without new artifact infrastructure.
3. Use catalog facts to guide investigation, never to select a clustering key.

### Phase 4: Focused regressions and configuration guidance

Add positive and negative tests for every changed rule, including the existing `disabled_rules`
behavior. Update the rule catalogue and agent guidance so the audit agent knows when to investigate
catalog and workload evidence instead of trusting a static heuristic.

## Acceptance criteria for the rule changes

- A documented microbatch model emits no conventional incremental watermark suggestions.
- A valid Snowflake stream consumer emits no conventional incremental guard suggestions.
- A staging-to-intermediate-to-mart chain with real transformations does not trigger `MAT0003`.
- `MAT0004` messages include Snowflake catalog rows, bytes, relation type, and last-modified time
  when available.
- `MAT0004` does not imply a table is large when physical-size evidence is unavailable.
- No rule proposes clustering columns from `catalog.json` alone.
- `PRJ0007` requires only `Snowflake-Labs/dbt_constraints` and `Snowflake-Labs/dbt_semantic_view` as
  the plugin's Snowflake baseline.
- Snowflake system views do not trigger an unconditional hardcoded-relation error.
- Disabled `persist_docs` and real exposure YAML are classified correctly.
- Each changed rule has a focused positive and nearest-neighbor negative test.
- A disabled exact rule ID is skipped consistently across audit, lint, validate, strict linting, and
  the editor hook.
- The audit agent investigates catalog matches before recommending `ref()` for a source and uses
  catalog facts before discussing clustering.

## Conclusion

The plugin should continue to be a deterministic suggestion engine rather than a scoring oracle. Its
strongest differentiator is the effort already invested in evidence, suppression, and false-positive
guards. Applying the same discipline to package policy, modern dbt incremental behavior, and
runtime-dependent performance advice will make the report more credible: objective defects stay
prominent, conventions are honestly labeled, and clustering guidance appears only when the available
artifacts justify it.
