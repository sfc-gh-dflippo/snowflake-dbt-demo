# SAS domain — integration wiring

How the SAS parallel track connects to the AIM migration plugin, what to verify, and what not to change.

## Wiring table

| Component | Location | Role |
|-----------|----------|------|
| **Router** | `plugin/skills/migration/sas/SKILL.md` | Classifies SAS intent; loads one child skill |
| **Skill-match (router)** | `plugin/skills/migration/SKILL.md` | SAS section under the migration `<skill-match>` — natural-language SAS prompts route here |
| **Structural test** | `ai/crates/mcp-server/tests/sas_skill_integration_check.rs` | Pins required files; asserts SAS is **present** in the migration `<skill-match>` and that `plugin/commands/` stays absent |
| **Root packaging test** | `ai/crates/mcp-server/tests/plugin_skill_root_check.rs` | Ensures single top-level skill root |
| **CUR bridge (opt-in)** | `register-sas-source-units/`, `register-sas-converted-units/` + `assess-sas-migration/tool/sas_analyzer/cur_emitter.py` | Writes `registry/<id>.json` **directly as JSON** so `scai test` can exercise conversions. Contract: `references/cur-schema.md`. Skill-side only \u2014 no dialect, no `.NET` registry engine |

Discovery is **natural-language routed**. The SAS track is registered in the migration `<skill-match>` in `plugin/skills/migration/SKILL.md`, so SAS prompts route here the same way the other migration skills do. There are **no dedicated SAS slash commands** (`plugin/commands/` was removed in SNOW-3973489). Per SNOW-3915306, PMs promoted the Preview track out of the earlier explicit-invoke-only scope; `sas_skill_integration_check` now guards that SAS stays in skill-match and that the commands tree stays gone.

## Do not touch (unless a separate design revisits AIM integration)

| Area | Constraint |
|------|------------|
| Migration `<skill-match>` | SAS entries live here (natural-language routed). Edit only `plugin/skills/migration/SKILL.md` (`sas_skill_integration_check` enforces the SAS paths stay listed) |
| `plugin/.cortex-plugin/plugin.json` `skills` array | Must remain `["skills/migration"]` only — no second top-level SAS root |
| `ai/crates/mcp-server/data/machines/*.json` | Do not add SAS tasks to MCP state machines |
| `plugin_skill_root_check` expected set | `plugin/skills/` must contain only `migration/` |
| SnowConvert dialect registry | SAS is not a SnowConvert source dialect in v1 (not in `TestGenerationDialects` / `CodeUnitRegistryDialects`) |
| `.NET` `CodeUnitRegistry` engine | The `scai test` CUR bridge writes `registry/<id>.json` **directly as JSON** (see `references/cur-schema.md`); it must not call the `.NET` registry engine or register a dialect |

Adding SAS to AIM claims, waves, `OBJECT_CLAIMS`, or the migration `<skill-match>` beyond the routing bullets would require a separate product design — not this parallel track. The CUR bridge is a bounded exception: it only writes standalone registry JSON into the conversion `<output_dir>` for `scai test`, and does not integrate SAS into the SnowConvert pipeline.

## Verification commands

Run from the repo root:

```bash
cd ai/crates/mcp-server && SKIP_DASHBOARD_BUILD=1 cargo test --test sas_skill_integration_check
cd ai/crates/mcp-server && SKIP_DASHBOARD_BUILD=1 cargo test --test plugin_skill_root_check
```

`sas_skill_integration_check` asserts:

- Router + child `SKILL.md`s (assess, convert, migrate-sas7bdat, validate sub-skill, register-sas-source-units, register-sas-converted-units) exist
- `README.md` and `INTEGRATION.md` exist
- The SAS skill files resolve on disk
- SAS is **present** in the migration `<skill-match>` (natural-language routed)
- `plugin/commands/` does not exist

## Manual invocation checklist

The SAS track is reached by **natural-language routing** through the migration `<skill-match>`. There are no dedicated SAS slash commands.

### Should route to SAS

| Prompt | Expected behavior |
|--------|-------------------|
| "assess this SAS portfolio" | Routes to `sas/assess-sas-migration/SKILL.md` |
| "convert MyJob.sas to Snowflake" | Routes to `sas/convert-sas-to-snowflake/SKILL.md` |
| "load these `.sas7bdat` files from a stage" | Routes to `sas/migrate-sas7bdat-to-snowflake/SKILL.md` |
| "migrate SAS" (programs vs datasets ambiguous) | Routes to the `sas/SKILL.md` router, which asks: programs (`.sas`) vs datasets (`.sas7bdat`) |

### Should NOT route to SAS

| Prompt | Expected behavior |
|--------|-------------------|
| "assess my SQL Server migration" | AIM migration workflow (SnowConvert / registry) — unaffected |
