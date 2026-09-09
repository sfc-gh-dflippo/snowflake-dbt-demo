# SSC-EWI-0073: Geospatial Methods — STArea

This sub-skill resolves `SSC-EWI-0073` for `STArea` nodes only.
Other geospatial methods (`STIntersection`, `STUnion`, `STIntersects`)
appear here solely as supporting context when chained with `STArea`.

## Quick Reference

| SQL Server | Snowflake | Notes |
|-----------|-----------|-------|
| `Shape.STArea()` | `ST_AREA_ELLIPSOIDAL(Shape)` | Always use UDF |
| `a.STIntersection(b).STArea()` | `COALESCE(ST_AREA_ELLIPSOIDAL(ST_INTERSECTION(a,b)),0)` | COALESCE mandatory |
| `a.STUnion(b).STArea()` | `ST_AREA_ELLIPSOIDAL(ST_UNION(a,b))` | Direct translation |
| `a.STIntersects(b) = 1` | `ST_INTERSECTS(a, b)` | BOOLEAN; drop `= 1` |
| `Shape.MakeValid()` | Not needed | Auto-normalized |
| `Shape.ReorientObject()` | Not needed | Auto-normalized |

## Identification

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR '...STArea' NODE ***/
```

The marker appears on `.STArea()` calls and on chained methods
(`.STIntersection(...)`, `.STUnion(...)`) when they precede `.STArea()`.

## UDF Prerequisite: ST_AREA_ELLIPSOIDAL

**EXECUTE THIS DDL FIRST** in each schema with affected procedures.
Source file: `UDF_Helpers/ST_AREA_ELLIPSOIDAL.sql`

Corrects Snowflake S2-sphere `ST_AREA()` to match SQL Server
WGS84-ellipsoid `STArea()`. Residual diff: <10 nanopercent.

```sql
CREATE OR REPLACE FUNCTION ST_AREA_ELLIPSOIDAL(g GEOGRAPHY)
RETURNS DOUBLE
LANGUAGE SQL
AS
$$
    ST_AREA(g) *
    (6378137.0 * 6378137.0 * (1.0 - 0.00669437999014)) /
    (
        POWER(
            1.0 - 0.00669437999014
                * POWER(
                    SIN(
                        ST_Y(ST_CENTROID(g))
                        * 3.141592653589793 / 180.0
                    ), 2
                ), 2
        )
        * 6371010.0 * 6371010.0
    )
$$;
```

## Fix Process

1. **Search** for `SSC-EWI-0073` markers containing `STArea`
2. **Deploy UDF** — execute the DDL above in each target schema
3. **Replace `.STArea()` calls**:
   `<expr>.STArea()` → `ST_AREA_ELLIPSOIDAL(<expr>)`
4. **Replace `.STIntersection().STArea()` chains**:
   → `COALESCE(ST_AREA_ELLIPSOIDAL(ST_INTERSECTION(a,b)),0)`
   COALESCE mandatory (SQL Server=0, Snowflake=NULL)
5. **Replace `.STUnion().STArea()` chains**:
   → `ST_AREA_ELLIPSOIDAL(ST_UNION(a,b))`
6. **Replace `.STIntersects()` in JOINs**:
   `a.STIntersects(b) = 1` → `ST_INTERSECTS(a, b)`
7. **Remove `.MakeValid().ReorientObject()`** if present
8. **Remove markers** — delete `!!!RESOLVE EWI!!!` lines
9. **Verify** — row counts and percentage values match baseline

---

## Example: Bridge Procedure (Most Common Pattern)

### Before (SQL Server)
```sql
SELECT
    REGION_A.geo_id AS RegionA_id,
    REGION_B.geo_id AS RegionB_id,
    REGION_A.Shape.STArea() AS RegionAArea,
    REGION_B.Shape.STArea() AS RegionBArea,
    REGION_A.Shape.STIntersection(REGION_B.Shape).STArea() AS AreaInt,
    REGION_A.Shape.STUnion(REGION_B.Shape).STArea() AS UnionInt
FROM RegionA REGION_A
FULL OUTER JOIN RegionB REGION_B
    ON REGION_A.Shape.STIntersects(REGION_B.Shape) = 1
```

### After (Snowflake)
```sql
SELECT
    REGION_A.geo_id AS RegionA_id,
    REGION_B.geo_id AS RegionB_id,
    ST_AREA_ELLIPSOIDAL(REGION_A.Shape) AS RegionAArea,
    ST_AREA_ELLIPSOIDAL(REGION_B.Shape) AS RegionBArea,
    COALESCE(
        ST_AREA_ELLIPSOIDAL(
            ST_INTERSECTION(REGION_A.Shape, REGION_B.Shape)
        ), 0
    ) AS AreaInt,
    ST_AREA_ELLIPSOIDAL(
        ST_UNION(REGION_A.Shape, REGION_B.Shape)
    ) AS UnionInt
FROM RegionA REGION_A
FULL OUTER JOIN RegionB REGION_B
    ON ST_INTERSECTS(REGION_A.Shape, REGION_B.Shape)
```

**Key changes:**
- `Shape.STArea()` → `ST_AREA_ELLIPSOIDAL(Shape)`
- `a.STIntersection(b).STArea()` →
  `COALESCE(ST_AREA_ELLIPSOIDAL(ST_INTERSECTION(a,b)),0)`
- `a.STUnion(b).STArea()` →
  `ST_AREA_ELLIPSOIDAL(ST_UNION(a,b))`
- `a.STIntersects(b) = 1` → `ST_INTERSECTS(a, b)`
- `MakeValid().ReorientObject()` → remove
- Dot-notation → function syntax

---

## Corner Cases

| Input | Source | Snowflake | Handling |
|-------|--------|-----------|----------|
| NULL geography | NULL | NULL | Parity |
| Disjoint intersection | 0.0 | NULL | COALESCE mandatory |
| POINT / LINESTRING | 0 | 0 | Div-by-zero risk |
| Near-pole (lat ~89.99) | WGS84 | UDF corrects | <10 nanopercent |
| Equatorial (lat ~0) | WGS84 | UDF corrects | <10 nanopercent |
| Antimeridian (180) | Correct | Correct | Parity |

## Guardrails

**DO:**
- Always use `ST_AREA_ELLIPSOIDAL()`, never native `ST_AREA()`
- Always wrap `ST_INTERSECTION` in `COALESCE(..., 0)`
- Preserve `WHERE`, `GROUP BY`, `FULL OUTER JOIN` as-is
- Deploy UDF from `UDF_Helpers/ST_AREA_ELLIPSOIDAL.sql`
- Convert all dot-notation to function syntax

**DO NOT:**
- Never use native `ST_AREA()` for STArea translation
- Never replace `ST_UNION(a,b)` with `ST_COLLECT(a,b)`
- Never use dot-notation (`Shape.STArea()` is invalid)

**Known Limitations:**
- Zero-area geometries as denominators → division-by-zero
  (SQL Server inserts NaN)
- Degenerate polygons → `empty loops are not allowed` error

## Resources

- [Snowflake ST_AREA](https://docs.snowflake.com/en/sql-reference/functions/st_area)
- [Snowflake ST_INTERSECTION](https://docs.snowflake.com/en/sql-reference/functions/st_intersection)
- [Snowflake ST_UNION](https://docs.snowflake.com/en/sql-reference/functions/st_union)
- [Snowflake ST_INTERSECTS](https://docs.snowflake.com/en/sql-reference/functions/st_intersects)
- [SQL Server STArea](https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/starea-geography-data-type)
- [SnowConvert SSC-EWI-0073](https://docs.snowconvert.com/sc/general/technical-documentation/issues-and-troubleshooting/conversion-issues/general/ssc-ewi-0073)
