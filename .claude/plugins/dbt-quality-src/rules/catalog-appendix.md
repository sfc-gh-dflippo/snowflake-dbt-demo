
---

## Naming-policy history

The general naming-convention rules ARC002 (layer prefix) and ARC008 (filename case) were removed.
Their IDs are retired and must not be reused. No column-naming rule was added. MIG0007 still
flags ETL-instance names for review; it does not establish that those names are invalid.

The original decision followed `dbt-modeling`'s Name-Retention Policy: a migrated model can keep
its source object's name. A useful naming check would need a reliable source-to-target mapping.
The migration output reviewed at the time did not provide one inside the project:

- `/* Original Object: ... */` was a comment, not a required structured manifest field.
- Header identifiers varied by platform: 2-part `[owner].[object]` or 3-part
  `[database].[schema].[object]` forms.
- Two header templates existed, and enforcement was warning-only.
- `meta.original_object`, `source_object`, and a crosswalk file were absent from that output.
- The source-to-target mapping was in SnowConvert's external `MIGRATION_REGISTRY`.

These are the recorded reasons for the removal, not universal claims about every dbt project.
The recorded self-audit produced 18 naming findings, most allowed by the retention policy. The
current Rust provenance code still infers platform signals; it does not prove original object
names. Do not restore the naming rule behind a config flag. Reconsider it only with an explicit,
reliable provenance contract.

## Conversion and operational guidance

The generated MIG and OPS tables above are the source of rule IDs, levels, severities, and
signals. Use a rule's full record for its remediation and references; do not maintain a second
copy of those tables here.

MIG0003 and SQL0008 can describe the same finding when an FDM marker concerns ordering and the SQL
uses `ORDER BY (SELECT null)`. Read the marker before grouping them. Do not assume every FDM
marker concerns ordering or that an EWI marker alone proves the SQL cannot compile.

OPS0002 concerns literal credentials in tracked files. PRJ0004 concerns `profiles.yml` placement.
Keep those concerns separate: a profile's presence alone does not prove credential exposure.
Likewise, an installed package or configured hook does not prove that its operational task ran.

## Provenance signals

Automatic migration detection uses the following local weights and a threshold of 4. These are
linter heuristics, not dbt requirements. One weak signal does not suppress all architecture rules.

| Signal | Weight |
| --- | ---: |
| `.scai/config/project.yml` present | 4 |
| `SSC-EWI` / `SSC-FDM` / `!!!RESOLVE EWI!!!` / `NEEDS-USER` markers | 4 |
| `.dbt-quality.yml` `migration.paths` match | 4 |
| `Output/ETL/{Package}/{DataFlow}` layout | 3 |
| `etl_dml_operation__` or `DD_*` constants | 3 |
| `stg_raw__` prefix | 3 |
| Converter placeholders in `dbt_project.yml` | 3 |
| ETL instance names in model names | 2 |

Marker detection uses text with waiver directives blanked by `waivers::blank_directives`. A waiver
contains a rule ID that can resemble a conversion marker. Without blanking, waivers could falsely
classify a native project as a migration. Owned dbt-quality markers are also blanked during discovery.

A score of at least 7 gives `high` confidence and permits project-wide architecture suppression.
A score of 4-6 gives `medium` confidence and covers files with detected migration signals; findings
with no file location can also be suppressed. Explicit `migration.mode: lift_and_shift` covers the
project; `native` skips automatic provenance classification. Inspect the recorded reasons before
accepting the scope, especially in a project with both migrated and native code.

The retired dbt-validation package's `check_migration_header` rule was not carried over. It used
broad source-platform substrings and a block-comment match for `Source`, rather than a structured
provenance check. Its acceptance did not prove a reliable original-object mapping. This history
explains why a replacement needs a declared contract rather than another naming heuristic.

## Adding a rule

### Diagnostic wording

State what the detector observed, the possible consequence, and the condition under which a change
is needed. Use direct wording for a verified condition. Do not turn a local policy into an upstream
requirement or treat a diagnostic level as proof that every matching model is wrong.

An information-level finding must explain when the code is acceptable. For example:
"Verify `unique_key` is set; correct as-is if the load is append-only and duplicates are acceptable."

An error-level rule still needs evidence-specific wording. A literal relation reference can bypass
dbt dependency tracking without being invalid SQL. A conversion marker can require review without
proving that the model cannot run. PRJ0004 reports profile placement at `warning` when untracked or
Git status is unknown, and at `information` when Git-ignored. Credential content belongs to OPS0002.

Use humanizer and ASD-STE100 principles: short sentences, clear subjects, active voice, and consistent
terms. Do not claim certified compliance. Keep exact code identifiers and executable examples.

### Implementation steps

1. Add a record to `rules/<PACK>.json`, sorted by `number`, with every required field from
   `rules/schema.json`: name, descriptions, remediation, level, severity, tier, scope, effort,
   `since`, and at least one example. The record is the source of rule metadata. `cargo build`
   rejects invalid metadata, duplicate codes, and pack/code mismatches.
2. Add official references that support the actual guidance. Keep the long description's References
   list consistent with the structured `references` array. State version limits and local policy
   choices. Keep names single-line and at most 60 characters, without annotation/Jinja delimiters;
   keep short descriptions at most 160 characters.
3. Add the detector in `rust/crates/dbt-quality-core/src/rules/<pack>.rs` and register it in
   `DETECTORS` with `Detect::Model`, `Detect::Project`, or `Detect::Portfolio`. Its scope must match
   the record. A test checks that records and detectors correspond.
4. Build findings with `Suggestion::new(code, message)`, evidence, and finding-specific remediation
   where needed. Use `.span(...)` for a real match offset. Otherwise the anchor layer uses the
   `{{ config() }}` block for config rules, a schema YAML model entry for test/doc rules, or the
   first query token, with line 1 as a fallback. Report a column only when a real offset is known.
5. Add a positive test and a clean counterpart with `crate::testing::TempProject`. Include valid
   exceptions and missing-input cases. Confirm both that the intended pattern fires and that the
   accepted form stays silent.
6. Regenerate the catalog: `dbt-quality rules --format markdown > plugin/skills/dbt-audit/references/rule-catalog.md`.
   `scripts/check-catalog.sh` fails when the committed copy differs. Run the Rust tests and report
   checks before treating the change as complete.
