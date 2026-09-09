---
name: seed-script
description: >
  Use when the migration state machine emits the `seedScript` task for a BTEQ
  script unit (`kind: "script"`, `source.format: "bteq"`), before baseline
  capture.
parent_skill: baseline-capture
---

# Seed BTEQ Script Inputs

Executor for the `seedScript` task. The CUR declares *which* shell variables each BTEQ script binds and their *kind*; the **values** live in the shell script that sets them before invoking `bteq` (`export UTIL_DB=PROD_UTIL`, `CFG=${1}.cfg`, `` RUN_DATE=`date +%Y%m%d` ``) — not in the `.btq`. `scai test seed --bindings-from <shell-script>` reads those scripts, pre-fills the binding values, and stages `.IMPORT` fixtures, so you hand-fill only what genuinely can't be resolved. Capture runs *after* this against the filled YAML, so leave no placeholder behind. YAML shapes: [../../references/BTEQ_TEST_YAML.md](../../references/BTEQ_TEST_YAML.md).

**Seed the whole BTEQ set in one pass**, not one unit at a time: a variable that recurs across scripts is hoisted to the global `.scai/settings/test_config.yaml` and filled once. Run this the first time any BTEQ unit reaches `seedScript` — it seeds every BTEQ unit together, so the rest are already done (idempotent; re-runs preserve filled values).

Per binding, the value resolves from the first tier that can supply it: **shell-script literal → `${N}` arg → capture-time `{ eval }` → `__REPLACE_ME__` (manual)**.

## Step 1: Ask the user for the BTEQ shell script(s)

Ask for the shell script(s) that set the BTEQ variables and run `bteq` (e.g. `runSqlScript_*.sh`), given as file paths **or a directory** (scanned recursively for `*.sh` / `*.ksh` / `*.bash`; `source` / `.` includes are followed when locatable). If a shell script derives values from invocation arguments (`CFG=${1}.cfg`, `. /etc/$1.cfg`), also ask for those positional arguments, **in order** ($1 first).

**Collect the path(s) and args only** — don't open, read, or trace the shell script to work out which bindings resolve. The seed parses it and reports what it couldn't resolve (Step 3); pre-analyzing here just duplicates that work.

If the user has no shell script, seed without `--bindings-from`; every value drops to the manual tier (Step 3).

## Step 2: Scaffold + prefill across the BTEQ corpus

```bash
scai test seed \
  -s <SOURCE_CONNECTION_NAME> \
  -c <SNOWFLAKE_CONNECTION_NAME> \
  --where "source.format ILIKE 'bteq'" \
  --bindings-from <path/to/shell-script-or-dir> \
  --bindings-args <arg1> --bindings-args <arg2>
```

- `--bindings-from` is repeatable — pass it once per shell script or directory.
- `--bindings-args` is optional — the values fill `$1`, `$2`, … in order.

`--where "source.format ILIKE 'bteq'"` scopes the pass to BTEQ script units (proc/func YAMLs are untouched). The engine resolves each binding from the shell script — filling literals, inlining `${N}` args, emitting `{ eval }` recipes for runtime values, mirroring identifier `source`/`target`, and staging `.IMPORT` fixtures — and then **reports what it could not resolve**. Read that report (next step); do **not** inspect the generated files yourself.

Re-run with `--append` to keep filled values and only refresh what's still unresolved.

## Step 3: Fill only what the seed reported

The seed prints exactly what needs a value — act on **its report**; do **not** grep or read the generated YAML / `test_config.yaml` to hunt for `__REPLACE_ME__`:

- **Unresolved bindings** — the seed lists them **by name** (the count + names of bindings the shell script couldn't match). For each, ask the user for the **source** (Teradata) and **target** (Snowflake) name/path, and fill it in the unit's `test/<name>.yml` (or the global `test_config.yaml` for a hoisted one).
- **MissingBindingArgs** — positions (`$1`, …) the shell script needs but you didn't pass. Re-run Step 2 with the missing `--bindings-args`.
- **MissingFixtures** — `.IMPORT` files not found on the host. Ask the user for the file, copy it into the unit's `fixtures/`, set `fixture: fixtures/<filename>`. Do **not** synthesize these.

Values the seed resolved to **`{ eval }` recipes need no action** — runtime-only inputs like a `` `date` ``, a `${N}`-built path, or a sourced `.cfg` that can't be reduced statically. They're recomputed in a sandbox at capture and pinned into the baseline. This is tier 3 of *literal → `${N}` arg → `{ eval }` → `__REPLACE_ME__`*: only the last tier needs a hand-filled value.

If the seed reports none of the above, `seedScript` is done — proceed to capture. (The runner refuses to load while any binding is still `__REPLACE_ME__`, which is why the seed reports them for you.)

## Notes

- The `bteq` binary is only needed at **capture**, not here — don't preflight for it. If it's missing, `scai test capture` fails with a pointer to `scai test doctor` (TTU install guidance).
- Source credentials for the `bteq` run come from the configured `source_connection` (Teradata); the shell script's `.LOGON` / connection lines are ignored — do not prompt for them.
- `{ eval }` recipes run sandboxed at capture (on by default; disable with `bteq_configuration.evaluate_eval_bindings: false`).
- Idempotent: once seeded, each BTEQ unit's `seedScript` finds its YAML filled and advances to `captureBaseline`. The seed's own report (Step 3) is the source of truth for what's still unresolved — trust it rather than re-scanning the files.
