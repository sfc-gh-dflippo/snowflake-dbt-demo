# BTEQ test-YAML shape

For BTEQ scripts (`kind: "script"`, `source.format: "bteq"`). Different from the proc/func step-based YAML in [step-based-yaml.md](step-based-yaml.md): a BTEQ test runs the whole script once per case and compares its **file I/O and table effects**, not a `CALL` return value. Per-object YAML lives under the unit's registry artifacts path in a `test/` dir — `artifacts/<unit-artifacts-path>/test/<name>.btq.yml` (e.g. `artifacts/BTEQ/script/test/script.btq.yml`). Discovery is keyed off the unit's `files.artifacts.path`, not a free-form glob, so the YAML must sit under that exact path. Binding values that recur across BTEQ units are hoisted to a single global `.scai/settings/test_config.yaml`.

## Binding values are resolved, not hand-typed
[seed-script/SKILL.md](../baseline-capture/seed-script/SKILL.md) runs `scai test seed --bindings-from <shell-script>` to fill these from the shell script that sets the variables before invoking `bteq`. Each value takes one of four forms:

| Form | YAML | When |
|---|---|---|
| scalar | `KEY: value` | source and target share the value |
| block | `KEY: { source: s, target: t }` | identifier kinds (database/schema/table); sides may differ under clone isolation |
| eval | `KEY: { source: { eval: '<bash>' }, target: { reuse: true } }` | runtime-only value (a `` `date` ``, a `${N}`-arg-built path, a sourced `.cfg`) — capture runs the recipe, validate reuses the captured value so both sides match |
| placeholder | `KEY: __REPLACE_ME__` (identifier) / `KEY: ''` (string) | nothing could resolve it — fill by hand |

## Shape

Global `.scai/settings/test_config.yaml` — bindings shared by 2+ BTEQ units, filled once:
```yaml
script_bindings:
  # kind:database/schema/table -> real name on each side
  UTIL_DB:
    source: PROD_UTIL
    target: PROD_UTIL
```

Per-object `artifacts/<unit-artifacts-path>/test/<name>.btq.yml`:
```yaml
validation:
  steps:
    - script:
        bindings:
          # kind:string/file -> scalar, or an { eval } recipe for a runtime value
          RUN_DATE:
            source:
              eval: |-
                RUN_DATE="`date +%Y%m%d`"
                printf '%s' "$RUN_DATE"
            target:
              reuse: true
          CFG: myconn.cfg              # ${1}-derived, arg supplied at seed
          err_file: bteq_err.log       # plain literal from the shell script
          # kind:schema/database/table -> {source, target} (unless hoisted to test_config.yaml)
          EXT_STAGE_DB_NAME: { source: ecommerce, target: ecommerce }
        files:
          reads:   # one per scriptMetadata.IO direction:read - staged from disk or user-provided
            - fixture: fixtures/widget_daily.csv
          writes:  # one per scriptMetadata.IO direction:write - the declared output name
            - bteq_err.log
```
A binding used by a single script stays in its per-object YAML; one used by 2+ is hoisted to `test_config.yaml` and omitted here.

## Where each piece comes from
| YAML field | Source |
|---|---|
| `bindings.<NAME>` | `scriptBindings[].name` + `kind`; the **value** is resolved by seed-script from the `--bindings-from` shell script (literal / `${N}` arg / `{ eval }`), else `__REPLACE_ME__` |
| `script_bindings.<NAME>` (global) | a binding used by 2+ BTEQ units, hoisted to `.scai/settings/test_config.yaml` |
| `files.reads[].fixture` | `scriptMetadata.IO` `direction:read` — staged from beside the shell script when present, else user-supplied |
| `files.writes[]` | `scriptMetadata.IO` `direction:write` — declared target name |

## Baseline / results
`scai test capture` writes `baseline_type:"script"` baselines (`exit_code`, `stderr`, `success`, `table_deltas`, `script_io`); `{ eval }` recipes are evaluated at capture and their resolved values pinned into the baseline. `scai test validate` re-runs `snowflake/BTEQ/<name>.sql` and compares (reuse targets take the capture-pinned value); results land in `<metadata_database>.VALIDATION.RESULTS` with `metadata.kind:"bteq"`.

## Prerequisites
- The `bteq` binary (Teradata Tools & Utilities) must be on PATH on the capture host - capture runs the source `.btq` through it.
- Binding values and `.IMPORT` fixtures are collected by [../baseline-capture/seed-script/SKILL.md](../baseline-capture/seed-script/SKILL.md) — resolved from the shell script (`--bindings-from`) where possible, hand-filled otherwise; they are not synthesized.
- BTEQ units are **not deployed** - the converted script is exercised by the test. Table dependencies migrate through the normal table flow first.
