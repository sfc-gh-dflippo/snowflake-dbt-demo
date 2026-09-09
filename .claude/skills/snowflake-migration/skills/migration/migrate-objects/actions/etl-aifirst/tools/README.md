# AI-First lab / table-build tools

Not on the convert runtime path. Runtime lives in `../scripts/`.

| Script | Role |
|--------|------|
| `build_alteryx_table.py` | Regenerate `platforms/platform_alteryx.json` |
| `alteryx_census.py` | Corpus plugin-frequency census (`AIFIRST_ALTERYX_CORPUS` or argv) |
| `runall.py` | Multi-fixture identify/emit batch (`AIFIRST_FIXTURES`, optional `AIFIRST_ENGINE_TESTS`) |
| `declared_vs_identified.py` | Element-loss gate over `runall.RUNS` |
| `decisions.py` | Informatica blind-run decision checks (CLI XML path) |
| `provenance_audit.py` | Provenance audit helper |
| `citecheck.py` | Location-oracle falsifiability (ADF/Pentaho fixtures) |
| `fixture_paths.py` | Shared fixture root resolution |

No machine-absolute paths. Point env vars at local corpora when needed.
