# SSC-EWI-INF0040 — Connected Stored Procedure Translated as UDF

A connected stored procedure transformation (Normal mode) is translated assuming the original database procedure has been converted to a Snowflake UDF. The translation calls it inline with VARIANT/OBJECT field extraction for output ports.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Low (once per connected stored procedure transformation) |
| Common action | Convert the SP to a UDF, or replace with inline SQL |

## Identification

Look for the marker:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0040 - THE STORED PROCEDURE TRANSFORMATION 'SP_CalcTax' IS TRANSLATED ASSUMING THE PROCEDURE HAS BEEN CONVERTED TO A UDF. THE ORIGINAL INFORMATICA TRANSFORMATION CALLED THE PROCEDURE ONCE PER ROW. THE TRANSLATION CALLS IT AS AN INLINE UDF. CONVERT THE STORED PROCEDURE TO A SNOWFLAKE UDF THAT RETURNS OBJECT_CONSTRUCT WITH NAMED FIELDS MATCHING THE OUTPUT PORT NAMES. ***/!!!
```

Followed by a model with inline UDF calls:
```sql
WITH source_data AS (
   SELECT Salary AS inSalary, EmpID, Salary
   FROM {{ ref('stg_raw__SQ_SRC_EMPLOYEES') }}
),
sp_result AS (
   SELECT
      source_data.*,
      dbo.sp_calc_tax(source_data.inSalary, source_data.EmpID, source_data.Salary):outTaxAmount :: NUMBER AS outTaxAmount,
      dbo.sp_calc_tax(source_data.inSalary, source_data.EmpID, source_data.Salary):RETURN_VALUE :: NUMBER AS RETURN_VALUE
   FROM source_data
)
SELECT * FROM sp_result
```

## Context

In Informatica, connected stored procedures call a database procedure **once per row** with input port values as arguments and capture output port values from the result. The Snowflake translation assumes:

1. The SP has been converted to a **UDF** (User-Defined Function)
2. The UDF returns an **OBJECT** with named fields matching output port names
3. Output values are extracted via `:fieldName::TYPE` syntax

## Fix Patterns

### Pattern 1: Convert SP to UDF (recommended)

Create a Snowflake UDF that matches the expected signature:

```sql
CREATE OR REPLACE FUNCTION dbo.sp_calc_tax(in_salary NUMBER, emp_id NUMBER, salary NUMBER)
RETURNS OBJECT
LANGUAGE SQL
AS
$$
  OBJECT_CONSTRUCT(
    'outTaxAmount', in_salary * 0.3,
    'RETURN_VALUE', in_salary * 0.3
  )
$$;
```

Then remove the `!!!RESOLVE EWI!!!` marker from the model.

### Pattern 2: Replace with inline SQL

If the SP logic is simple, replace the UDF call with inline expressions:

```sql
-- Before
dbo.sp_calc_tax(source_data.inSalary, source_data.EmpID, source_data.Salary):outTaxAmount :: NUMBER AS outTaxAmount

-- After
source_data.inSalary * 0.3 AS outTaxAmount
```

### Pattern 3: Mark as needs-user

If the SP logic is complex:
```sql
-- NEEDS-USER: Original Informatica SP 'SP_CalcTax' must be converted to a Snowflake UDF.
-- UDF must return OBJECT_CONSTRUCT with fields: outTaxAmount, RETURN_VALUE
-- Original SP signature: sp_calc_tax(inSalary NUMBER, EmpID NUMBER, Salary NUMBER)
```

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker — it breaks compilation.
- The model's CTE structure (`source_data` → `sp_result`) is correct — only the UDF needs to exist.
- INPUT/OUTPUT ports (bidirectional) appear as call arguments but are **not** extracted from the return value — they flow through via `source_data.*`.
- If the SP name is schema-qualified (e.g., `dbo.sp_calc_tax`), the UDF must match that qualification.
