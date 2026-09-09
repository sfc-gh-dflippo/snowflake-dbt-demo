# SSC-EWI-INF0001 — PowerCenter Transformation Not Supported

An Informatica PowerCenter **transformation** has no SnowConvert translation, so the converter emitted a
stub: a `!!!RESOLVE EWI!!!` marker plus the transformation's original XML as comments. The marker
**breaks compilation**, and the transformation's logic is absent from the output — so unlike an annotation,
resolving this means *reconstructing behaviour*, not just deleting a line.

The commented XML is the contract. It is usually complete enough to rebuild the transformation, and it is
the only place the intent survives.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Logic present in output? | **No** — the transformation body is only present as commented XML |
| Frequency | Low per mapping, but each occurrence is real work |
| Common action | Read the commented `<TRANSFORMATION>` XML, rebuild the logic in SQL, remove the marker |

## Identification

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - INFORMATICA POWERCENTER TRANSFORMATION IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--
--<TRANSFORMATION NAME="sql_PAYMENT_DETAIL_GRP1" TYPE="Custom Transformation" DESCRIPTION="This SQL transformation is used for parsing XML." ... TEMPLATENAME="SQL Transform" ...>
--  <GROUP NAME="SQLInputs" ORDER="1" TYPE="INPUT" />
--  <GROUP NAME="SQLOutputs" ORDER="2" TYPE="OUTPUT" />
--  <TRANSFORMFIELD NAME="DESC_TAG_PATH" DATATYPE="string" PORTTYPE="INPUT" ... />
--  ...
```

The marker text itself is generic — it does not say which transformation type failed. **Read the
`TYPE` and `TEMPLATENAME` attributes of the commented `<TRANSFORMATION>` element** to find out what you
are rebuilding.

## Decision Tree

1. **Read `TYPE` (and `TEMPLATENAME` when `TYPE="Custom Transformation"`).** That identifies the
   transformation. Everything else follows from it.
2. **Read the ports.** `<TRANSFORMFIELD>` entries give you the input and output column contract:
   `PORTTYPE` (INPUT / OUTPUT / INPUT-OUTPUT), `DATATYPE`, `PRECISION`, and any `EXPRESSION` attribute.
   The output ports are what downstream models expect to consume — preserve their names and types.
3. **Read the ports' expressions and the transformation's `<TABLEATTRIBUTE>` values.** These carry the
   actual logic (filter conditions, group-by keys, join conditions, SQL text, sort order, rank settings).
4. **Rebuild in SQL from that contract** using the type table below. Reconstruct from the source
   semantics — never infer the logic from surrounding converted SQL, and never fabricate values.
5. **Is the transformation genuinely not reproducible in SQL?** (An external procedure, a Java
   transformation, a call into a third-party library.) Mark the node needs-user with what the
   transformation did and what input is required. Do not stub it with constants.

## Transformation Type Reference

| PowerCenter transformation | Snowflake / dbt approach | Reconstructable from XML? |
|---|---|---|
| Rank | `RANK()`/`ROW_NUMBER() OVER (PARTITION BY <group> ORDER BY <port> DESC)` filtered to the rank limit | Yes |
| Sorter (with distinct) | `ORDER BY`, or `SELECT DISTINCT` when the distinct flag is set | Yes |
| Aggregator | `GROUP BY` + aggregate functions per output port | Yes |
| Joiner | `JOIN` with the join type from the transformation's attributes | Yes |
| Filter / Router | `WHERE`, or one CTE per router group with the group's condition | Yes |
| Union | `UNION ALL` (PowerCenter Union does not de-duplicate) | Yes |
| Normalizer | `LATERAL FLATTEN`, or an explicit `UNION ALL` per occurrence | Usually |
| Sequence generator | `SEQ`/`IDENTITY`, or `ROW_NUMBER()` where ordering is deterministic | Usually |
| Custom Transformation — SQL Transform | Port the embedded SQL to Snowflake dialect | Usually |
| Custom Transformation — XML parsing | `PARSE_XML` + `XMLGET`/`LATERAL FLATTEN` over the tag paths | Often, with care |
| Java / external procedure | Snowpark UDF, or escalate | No — needs-user |

## Fix Patterns

### Pattern 1: Rank — rebuild as a window function

```sql
-- Before (breaks compilation; the ranking logic exists only in the comments)
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - INFORMATICA POWERCENTER TRANSFORMATION IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--<TRANSFORMATION NAME="rnk_latest_per_party" TYPE="Rank" ...>
--  <TABLEATTRIBUTE NAME="Top/Bottom" VALUE="Top"/>
--  <TABLEATTRIBUTE NAME="Number of Ranks" VALUE="1"/>
--  <TRANSFORMFIELD NAME="LOAD_TS" PORTTYPE="INPUT/OUTPUT" ... SORTKEYDIRECTION="DESC"/>
--  <TRANSFORMFIELD NAME="PARTY_ID" PORTTYPE="INPUT/OUTPUT" GROUPBY="YES"/>
--</TRANSFORMATION>

-- After: Top 1 per PARTY_ID by LOAD_TS descending
SELECT PARTY_ID, PARTY_TYPE, PARTY_NAME, LOAD_TS
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY PARTY_ID ORDER BY LOAD_TS DESC) AS rn
    FROM {{ ref('int_parties_enriched') }}
)
WHERE rn = 1
```

Use `RANK()` rather than `ROW_NUMBER()` when the source's rank semantics keep ties (PowerCenter's
`RANKINDEX` behaviour). With a single rank and a tie, `ROW_NUMBER()` keeps one row while `RANK()` keeps all
tied rows — that difference changes row counts, so choose deliberately.

### Pattern 2: Custom Transformation (SQL Transform) — port the embedded SQL

```sql
-- Before
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - INFORMATICA POWERCENTER TRANSFORMATION IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--<TRANSFORMATION NAME="sql_PAYMENT_DETAIL_GRP1" TYPE="Custom Transformation"
--   DESCRIPTION="This SQL transformation is used for parsing XML." TEMPLATENAME="SQL Transform" ...>
--  <TRANSFORMFIELD NAME="DESC_TAG_PATH" DATATYPE="string" PORTTYPE="INPUT" .../>
--  ...

-- After: the embedded statement translated to Snowflake, exposing the declared output ports
SELECT
    x.value:"TagPath"::VARCHAR   AS DESC_TAG_PATH,
    x.value:"TagValue"::VARCHAR  AS DESC_TAG_VALUE
FROM {{ ref('stg_raw__pymt_msg') }} m,
     LATERAL FLATTEN(input => PARSE_XML(m.MSG_BODY):"Document") x
```

For XML-parsing transformations, take the tag paths from the transformation's port definitions and
attributes, and reproduce them with `PARSE_XML` plus `XMLGET`/`LATERAL FLATTEN`. Keep the output port
names exactly as declared so downstream models still resolve.

### Pattern 3: Not reproducible — escalate with evidence

```sql
-- After (marker removed so the file parses; behaviour explicitly unresolved)
-- NEEDS-USER: PowerCenter transformation "jtx_score_customer" (TYPE="Java") cannot be reproduced in SQL.
-- It called an external scoring library on each row and returned RISK_SCORE (decimal(5,2)).
-- Required to proceed: the scoring rules, or an approved Snowpark equivalent.
-- Downstream models consuming RISK_SCORE: mart_customer_risk.
-- Not stubbed with a constant on purpose — a placeholder value would silently corrupt the mart.
```

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` line — it breaks compilation.
- Removing the marker alone is **not** a fix: the transformation's logic is missing from the output and
  must be rebuilt, or the model will compile and produce wrong data.
- **Keep** the commented `<TRANSFORMATION>` XML unless the rebuild fully replaces it; it is the only
  record of intent for the next reader.
- Preserve the output port names, data types and null behaviour exactly — downstream models reference them.
- Never substitute constants or `NULL` for missing logic; escalate as needs-user instead.
- Reconstruct from the source XML, not from the shape of the surrounding generated SQL.
- Validate against source-derived expected results: a rebuilt transformation that compiles can still have
  the wrong grain, the wrong join type, or the wrong tie-breaking.
