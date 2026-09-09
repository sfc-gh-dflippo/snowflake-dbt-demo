# SSC-EWI-0073 - Pending Functional Equivalence Review

SnowConvert marks nodes with this EWI when SQL Server constructs
have no direct 1:1 equivalent in Snowflake. Route to the correct
sub-skill based on the node type in the EWI marker.

## Routing

```
What node appears in the !!!RESOLVE EWI!!! marker?
│
├── ERROR_NUMBER / ERROR_MESSAGE / ERROR_SEVERITY
│   ERROR_STATE / ERROR_LINE / ERROR_PROCEDURE
│   → SSC-EWI-0073/0073-Error-Handling.md
│
└── STArea / STIntersection (chained with STArea)
    STUnion (chained with STArea) / STIntersects
    → SSC-EWI-0073/0073-Geospatial-Methods.md
```

## Sub-Skills

| Node Pattern | Sub-Skill | Scope |
|-------------|-----------|-------|
| `ERROR_*()` functions | [0073-Error-Handling.md](SSC-EWI-0073/0073-Error-Handling.md) | TRY..CATCH → EXCEPTION, SQLCODE/SQLERRM/SQLSTATE |
| `STArea` + chained methods | [0073-Geospatial-Methods.md](SSC-EWI-0073/0073-Geospatial-Methods.md) | STArea → ST_AREA_ELLIPSOIDAL UDF. UDF DDL: `UDF_Helpers/ST_AREA_ELLIPSOIDAL.sql` |

## Resources

- [SnowConvert SSC-EWI-0073](https://docs.snowconvert.com/sc/general/technical-documentation/issues-and-troubleshooting/conversion-issues/general/ssc-ewi-0073)
