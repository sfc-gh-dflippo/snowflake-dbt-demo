# Verify

Guide for the `verify` task. The machine routes an object here in two cases:

- After conversion, when its type has no deploy/test path of its own — Oracle `PACKAGE`, `PACKAGE_BODY`, `TYPE`, `TYPE_BODY`, `SYNONYM`, and any other type the machine doesn't route onward.
- After **deploy**, when a procedure or function has **no source side** (SnowConvert UDF helpers under `snowflake/UDF Helpers/`). Those objects are Snowflake-only: there is no source to seed or baseline against, so `createTests` / `runTests` will never pass.

There is no `scai` command for this step: **verify the object by whatever means the object allows**, then record the verdict.

## Step 1: Read the conversion output

Open the object's source and converted files (`files.source.path` and `files.converted.path` on its registry entry). Establish what SnowConvert actually did with it. Common outcomes:

- **Inlined into callers** — packaged procedures/functions, and user-defined types, are frequently expanded into the referencing procedures and functions rather than emitted as standalone Snowflake objects. The converted file for the package itself may be empty, a comment, or EWI-only.
- **Resolved at the use site** — synonyms usually disappear, with references rewritten to the underlying object.
- **Emitted as a real object** — some types do convert to deployable Snowflake DDL.

## Step 2: Pick a verification that fits what you found

Use as much evidence as the object gives you. In rough order of strength:

1. **It is already deployed** (source-less helper) → confirm the object exists in Snowflake (`SHOW FUNCTIONS` / `SHOW PROCEDURES` or `DESC`) and is callable with a few smoke inputs. Do not try to seed, capture a source baseline, or author a test YAML.
2. **It produced deployable DDL** → deploy it and confirm it compiles in Snowflake.
3. **Its logic moved into referencing units** → list the referencing code units (`dependencies` on the registry entry, or `query_registry` for units that reference this name) and confirm each one converted, and that the packaged logic is present in them. Their own `runTests` results are the real proof the logic survived.
4. **Nothing was emitted and nothing references it** → confirm that: no referencing unit, no remaining references to the name in the converted SQL.
5. **Unresolved EWIs on the converted output** → treat as not verified; load [DIAGNOSE_FIX.md](DIAGNOSE_FIX.md).

Report what you checked and what you concluded. Do not claim more than the evidence supports — "the package body was inlined into 3 procedures, all 3 pass their tests" is a verification; "conversion reported success" is not.

## Step 3: Record the verdict

- **Verified** → `transition_status(task="verify", outcome="completed", where="id IN ('<object_id>')")`. This is the object's last task; it moves to done.
- **Not verifiable / genuinely out of scope** (e.g. the package was fully inlined and the standalone object will never exist in Snowflake) → say so, then mark it out of scope with `update_registry(field="inScope", status="false", objects="<object_id>")` once nothing depends on it.
- **Converted output is wrong** → load [DIAGNOSE_FIX.md](DIAGNOSE_FIX.md) to fix it, then re-verify.

Escalate to the user when you can't tell whether an object matters — a package whose logic went nowhere and whose callers are missing is a migration gap, not a completed object.
