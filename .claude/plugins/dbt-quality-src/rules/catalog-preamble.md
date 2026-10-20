## Tiers

| Tier | Behavior |
| --- | --- |
| `universal` | Applies to native and migrated projects when enabled and not waived. |
| `architecture` | Architecture guidance. Migration detection can suppress these findings; the report counts them separately for later review. |
| `migration` | Conversion-related guidance, gated by each detector's migration signals. Migration detection does not suppress these findings. |

Suppression is a review policy, not proof that the code is correct. Disabled rules and waivers
still apply to all tiers. Missing inputs and detector failures produce coverage gaps.

## Disable or waive a rule

Use the narrowest scope that fits. Prefer a waiver for an accepted trade-off or false positive
rather than disabling the rule for the entire run.

| Mechanism | Scope | Effect on the report |
| --- | --- | --- |
| `disabled_rules:` | One rule for the run | Listed as skipped, so readers know it was not checked. |
| `ignore:` config entry | One rule at matching paths | Removed from outputs and counts. |
| `-- dbt-quality: ignore-file <ids>` | One rule in one file | Removed from outputs and counts. |
| `-- dbt-quality: ignore <ids>` | One rule at a reported line | Removed from outputs and counts. |

Use full rule codes. A line directive applies to the line it is on or the line immediately below
it. Place it at the diagnostic's reported location. Config-related rules often anchor at
`{{ config() }}`, but precise read-site rules can report another line. Use `ignore-file` only
when a file-wide waiver is intended. Project- and portfolio-scoped findings need a configuration
waiver; their `file` can be a directory or `<portfolio>`.

If an expected finding is missing, search for `dbt-quality: ignore` and inspect the nearest
`.dbt-quality.yml` for `ignore` and `disabled_rules`. The configuration may be in an ancestor of
the audit root. See the plugin README for configuration lookup and usage examples.

## Codes, kind, level, and severity

Each rule has a code of the form `SSC-{KIND}-DBT{CAT}{NNNN}`. `SSC` is also used by SnowConvert.
Identify this engine's markers by the full shape, including the three-letter pack and four-digit
number. The `DBT` text alone is not enough: SnowConvert also emits codes such as `SSC-EWI-DBT0001`.
Its markers, including `SSC-EWI-SSIS0033`, remain separate from dbt-quality markers.

Three fields classify a finding. They describe the rule's concern, diagnostic level, and impact;
they are not measured probabilities or proof of a defect.

| Kind | Meaning |
| --- | --- |
| `EWI` | An issue or pattern that needs review. |
| `FDM` | A possible functional difference from source behavior. |
| `PRF` | A performance or cost concern. |

| Level | How to read it |
| --- | --- |
| `error` | The rule treats the detected condition as an error. Confirm its evidence and context before changing code. |
| `warning` | Review a likely problem or risk. |
| `information` | Check a context-dependent pattern; the current code may be appropriate. |

| Severity | Potential impact if the concern applies |
| --- | --- |
| `critical` | Secret exposure, data loss, or a model that produces no rows. |
| `high` | Wrong results. |
| `medium` | Avoidable cost or maintenance work. |
| `low` | Style or a small maintenance concern. |

`level` and `severity` are independent. An `information` finding can have `critical` impact if its
condition applies. Explain that condition instead of treating severity as certainty.

## References and local policy

Each rule's full record includes sources for its guidance. Read those sources with the stated
conditions and version limits. A source can explain a feature without requiring this linter's
threshold or policy. Review thresholds, preferred layouts, and migration conventions are local
choices unless the reference explicitly requires them. Preserve business behavior when applying
advice; a successful dbt build alone does not prove it correct.
