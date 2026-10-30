# Registry and dbt consolidation

Load this when you merge dbt projects, or when a report shows that the registry
and the dbt folders disagree. Applies only inside a migration project (a
`.scai/config/project.yml` at or above the audit path). Outside one, there is no
registry.

## Rules

- The registry (`registry/*.json`) is the system of record. Each ETL unit has
  `parts[]`. A dbt part has `target.format: dbt`, `target.path` (for example
  `snowflake/_etl/<Pkg>/<DataFlow>/`) and `target.modelName`.
- Every dbt target must be a folder that contains `dbt_project.yml`.
- Every deployable dbt project under `snowflake/_etl/` must be targeted by at
  least one in-scope unit. dbt-quality audits only the projects the registry
  targets, so an untargeted project is not audited.
- Every `modelName` must exist in its target project.
- Never edit `registry/*.json` by hand or with a script. Registry writes go
  through `update_registry`.

## Read a disagreement

`report` and `findings` return `inputs.registry_check`:

| Key | Meaning |
|-----|---------|
| `stale_targets` | A unit part targets a folder with no `dbt_project.yml` (unit, part, path) |
| `unregistered_projects` | A dbt project on disk that no unit targets (path) |
| `missing_models` | A part's `modelName` is not in its target project (unit, part, model) |
| `skipped_targets` | A target skipped on purpose, such as a backup or `obj/` copy (unit, path, reason) |

Findings PRJ0001-0003 and PRJ0006 carry `registry_units`: the units that target
the project. Use them as the mapping source.

## Before you consolidate

1. Run `query_registry(where="kind = 'etl'", fields="id,parts", limit=<enough>)`.
2. Build a mapping: old project path -> unit ids, part indexes, `modelName`.
   Use `registry_units` from the findings to cross-check it.
3. Show the user which units each merge affects, and how many.

**⚠️ Stop:** a merge across packages changes deployment boundaries. Get explicit
approval before you move any file.

## After a merge

Do these in order:

1. Move the models and macros into the merged project. Resolve name conflicts
   (PRJ0020) and var conflicts (PRJ0012) there.
2. Dispatch the `cur_reconciler` agent with the mapping. It retargets every
   affected part. See "dbt consolidation retarget" in
   `agents/cur_reconciler.md`.
3. Delete the old project folders only after the patch has landed. A failed
   patch then leaves the old targets valid.
4. Verify:
   - `query_registry` shows no dbt target under a deleted path.
   - `report` shows `registry_check` with zero entries for the merged paths.
   - The audited project count dropped by the number of projects merged.

## Consolidation at convert time

`scai code convert` with `--consolidate-dbt-projects` or
`--consolidate-as-single-dbt-project` should leave the registry pointing at
`{PackageName}Dbt/` or at the single project. After convert, run the checks in
"After a merge", step 4.

If the registry does not match, show the mismatch and fix it with the same
`cur_reconciler` retarget. Never run convert again with
`--overwrite-working-directory`: it discards stabilization fixes.

## Never register these paths

- `stabilization/original/` backups
- `bin/` and `obj/` build copies
- `target/` and `dbt_packages/`

dbt-quality skips them and lists them in `inputs.skipped`. If a unit already
targets one, `cur_reconciler` sets `inScope: false` on that unit with
`update_registry`, after the user approves. Do not leave it as a gap.

## Undo a merge

Reverse the mapping with the same retarget (new path -> old path), then restore
the old folders from git.
