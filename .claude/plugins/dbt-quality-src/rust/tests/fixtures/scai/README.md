# scai fixtures

Real scai (SnowConvert AI) output, copied unchanged from `migrations-snowconvert-desktop`
at commit `07da0826cb1c98f2f956231804ef57341dc82f20`. Do not edit these files to suit the parser.

| Folder | Source path | Covers |
|---|---|---|
| `tasktracker/` | `snaps/primitives/scai-eval-tasktracker-converted/project/{snowflake,registry}` | scai project layout, inline PK/FK/CHECK, registry `signature.columns` |
| `sample_store/` | `snowconvert-ai/e2e/test-data/projects/sql-server/e2e_sample_20_objects/converted/Output/SnowConvert/table/store` | BOM, `USE DATABASE`, `IDENTITY ORDER`, `DEFAULT (x :: T)`, `COLLATE` with SSC comments, table `COMMENT` |
| `bindings/` | `testing-infrastructure/integration/sample_data/sqlserver/database-bindings/target_deploy.sql` | `${TOKEN}` names, `<sc-table>` tags, INSERT statements |

To refresh, copy the same paths from a newer commit and update the commit above.
