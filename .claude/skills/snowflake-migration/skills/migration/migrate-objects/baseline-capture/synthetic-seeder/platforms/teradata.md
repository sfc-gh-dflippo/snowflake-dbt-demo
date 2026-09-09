# Synthetic Seeder — Teradata-Specific Guidance

Load this file when `source_dialect` is `Teradata` before generating call steps (Phase 3).

---

## Cross-database GRANT steps

The test runner creates isolated database copies with random suffixes on Teradata. Stored procedures execute with **definer rights** (the owning database's privileges), so the procedure's database needs explicit access to every other database it touches. Without these grants the procedure fails with `Error 5315: does not have SELECT/INSERT access`.

**Immediately before the CALL step**, add a `source_query`-only GRANT step for each database the procedure references. No `target_query` is needed (Snowflake doesn't have this isolation constraint). The test runner suffixes the database names automatically.

```yaml
  # --- Cross-database grants for Teradata isolation ---
  - source_query: GRANT ALL ON SCHEMA_A TO PROC_SCHEMA;
    validate: false
  - source_query: GRANT ALL ON SCHEMA_B TO PROC_SCHEMA;
    validate: false
  # ... one per referenced database
  - source_query: "CALL PROC_SCHEMA.do_work({0})"
    target_query: "CALL PROC_SCHEMA.DO_WORK({0})"
```

Where `PROC_SCHEMA` is the database containing the procedure, and `SCHEMA_A`, `SCHEMA_B` are all other databases it reads from or writes to.

## Call syntax

Teradata uses `CALL proc(args)` — not `EXECUTE`. Source and target call syntax is symmetric except for quoting conventions.

**Simple call (no cross-database access needed):**

```yaml
  - source_query: "CALL PROC_SCHEMA.do_work({0})"
    target_query: "CALL PROC_SCHEMA.DO_WORK({0})"
```

Source uses lowercase names; Snowflake uses uppercase. OUT parameters use `:PARAM` syntax on the target side.
