# Oracle Test YAML Guidance

Reference for Oracle-specific patterns when authoring or editing step-based test YAMLs.
Load when `source_dialect` is `Oracle` — applies to both synthetic-seeder (Phase 3 call generation) and EDIT_TEST_YAML (per-dialect gotchas).

---

## Execution model

Oracle source steps are assembled into a single **anonymous PL/SQL block** by the test runner. All steps are wrapped in `DECLARE … BEGIN … END;`. This means:

- You do NOT write `DECLARE` or `BEGIN`/`END` yourself — the runner does it.
- Every `source_declare` row is hoisted into the DECLARE section; a `source_declare` that appears _after_ a `source_query` opens a nested `DECLARE … BEGIN … END;` sub-block so earlier variables stay in scope.
- Invoke procedures by bare qualified name — **no `CALL` or `EXECUTE`** on the Oracle source side. `CALL` is a SQL statement and is illegal inside the anonymous PL/SQL block the runner assembles. Reserve `CALL` for Snowflake `target_query` only.
- **COMMIT is not supported inside test steps.** The runner uses savepoint-based isolation; a commit inside a case breaks isolation for subsequent test cases. If the source procedure commits internally, document it and skip coverage of that code path.

---

## Variable declarations: `source_declare`

Use `source_declare` instead of `source_query` when declaring PL/SQL variables. The value is the bare declaration — no `DECLARE` keyword.

```yaml
# Oracle: naked declaration — runner emits DECLARE once per block
- source_declare: v_id NUMBER := 9901
  target_declare: LET V_ID INT := 9901
  validate: false
- source_query: "TEST.MY_PROC(v_id)"
  target_query: "CALL MY_SCHEMA.MY_PROC(:V_ID)"
```

Multiple `source_declare` rows are grouped into one DECLARE section by the runner:

```yaml
- source_declare: v_count NUMBER := 0
  target_declare: LET V_COUNT INT := 0
  validate: false
- source_declare: v_name VARCHAR2(100) := 'test'
  target_declare: LET V_NAME STRING := 'test'
  validate: false
```

---

## Package member calls

Oracle packages bundle related procedures/functions under one schema-level name. SnowConvert explodes each package into a dedicated Snowflake schema named `{source_schema}_{PACKAGE_NAME}` (e.g. source schema `TEST`, package `ITEM_MGMT` → Snowflake schema `TEST_ITEM_MGMT`).

**Registry signal:** a package member's registry entry has `source.package` non-empty (e.g. `"ITEM_MGMT"`). Always check this in Phase 0.4. Record:
- `source_package` = value of `source.package`
- `source_schema` = value of `source.schema`
- `target_schema` = value of `target.schema` (the `{source_schema}_{PACKAGE_NAME}` schema SnowConvert created)

**Call syntax:**

| Side | Pattern |
|---|---|
| Source (Oracle) | `{source_schema}.{PACKAGE}.{MEMBER}({args})` — three-part FQN, no `CALL` |
| Target (Snowflake) | `CALL {target_schema}.{MEMBER}({args})` — member lives in the package schema |

> **Critical:** Never use a two-part FQN (`SCHEMA.MEMBER`) for Oracle package members. The test runner resolves call schemas from the third segment of the FQN (SNOW-3677527). A two-part name produces zero matched test cases.

**Full example** — `ITEM_MGMT.ADD_ITEM`, `source.package = "ITEM_MGMT"`, `source.schema = "TEST"`, `target.schema = "TEST_ITEM_MGMT"`:

```yaml
validation:
  test_cases:
    - [9901, "Widget A", 10]
  steps:
    - source_query: "INSERT INTO TEST.INVENTORY VALUES (9901, 'Widget A', 10)"
      target_query: "INSERT INTO TEST.INVENTORY VALUES (9901, 'Widget A', 10)"
      validate: false
    - source_query: "TEST.ITEM_MGMT.ADD_ITEM({0}, {1}, {2})"
      target_query: "CALL TEST_ITEM_MGMT.ADD_ITEM({0}, {1}, {2})"
    - source_query: "SELECT ITEM_ID, ITEM_NAME, QTY FROM TEST.INVENTORY ORDER BY ITEM_ID"
      target_query: "SELECT ITEM_ID, ITEM_NAME, QTY FROM TEST.INVENTORY ORDER BY ITEM_ID"
```

---

## Artifact path for package members

The CUR places package member test YAMLs under a subdirectory named after the package:

```
artifacts/<db>/<schema>/procedure/<package_name_lower>/<member_name>/test/<member_name>.<idx>.yml
```

e.g. `artifacts/MY_DB/TEST/procedure/item_mgmt/add_item/test/add_item.0.yml`

**Always read `files.artifacts.path` from `query_registry` rather than constructing this path.** The CUR value already includes the package subdirectory — do not flatten the package level.

---

## OUT params and SYS_REFCURSOR

For plain OUT params, the runner wraps them in a `SYS_REFCURSOR` over `SELECT … FROM DUAL` so capture and validate treat them as normal result sets — no special step needed.

For procedures that explicitly return a `SYS_REFCURSOR`, use a three-step pattern: declare the cursor variable, call the procedure by bare name, then publish the cursor with `DBMS_SQL.RETURN_RESULT`:

```yaml
steps:
  - source_declare: "p_cursor SYS_REFCURSOR"
    validate: false
  - source_query: "SCHEMA.PACKAGE.GET_RESULTS(p_cursor)"
    target_query: "CALL SCHEMA_PACKAGE.GET_RESULTS(:P_CURSOR)"
  - source_query: "DBMS_SQL.RETURN_RESULT(p_cursor)"
```

Reserve `source_params` for plain scalar OUT params only.
