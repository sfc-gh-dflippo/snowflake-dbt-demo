# Teradata Power Query M Formula Language Samples

Parameterized SQL query samples for Teradata using Power BI global parameters.

**Server:** `teradata.example.com`  
**Schema:** `sales_db`  
**Table:** `customers`

---

## Available Columns Reference

| Column | Type | Example |
|--------|------|---------|
| cust_id | Integer | 1363448 |
| income | Integer | 27239 |
| age | Integer | 57 |
| years_with_bank | Integer | 7 |
| nbr_children | Integer | 0 |
| gender | Char | M |
| marital_status | Integer | 1 |
| name_prefix | Char | Mr. |
| first_name | Char | DeWayne |
| last_name | Char | Ferguson |
| street_nbr | Integer | 7285 |
| street_name | Char | Peach |
| postal_code | Integer | 90195 |
| city_name | Char | Los Angeles |
| state_code | Char | CA |

---

## 1. Single Text Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | Basic Text Filter |
| **Power BI Parameter** | `pStateCode` (Text) = "CA" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "'"])
in
    Source
```

---

## 2. Single Numeric Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | Basic Numeric Filter |
| **Power BI Parameter** | `pMinIncome` (Decimal) = 50000 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE income > " & Text.From(pMinIncome)])
in
    Source
```

---

## 3. Optional Text Parameter (All or Filter)

| Property | Value |
|----------|-------|
| **Pattern Name** | Optional Filter |
| **Power BI Parameter** | `pStateCode` (Text) = "CA" or "ALL" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "' OR 'ALL'='" & pStateCode & "'"])
in
    Source
```

---

## 4. Two Text Parameters

| Property | Value |
|----------|-------|
| **Pattern Name** | Dual Text Filter |
| **Power BI Parameters** | `pStateCode` = "CA", `pCityName` = "Los Angeles" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND city_name='" & pCityName & "'"])
in
    Source
```

---

## 5. Text and Numeric Parameters

| Property | Value |
|----------|-------|
| **Pattern Name** | Mixed Type Filter |
| **Power BI Parameters** | `pStateCode` = "NY", `pMinIncome` = 40000 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND income > " & Text.From(pMinIncome)])
in
    Source
```

---

## 6. LIKE Pattern Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | Wildcard Search |
| **Power BI Parameter** | `pFirstNamePattern` = "J%" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE first_name LIKE '" & pFirstNamePattern & "'"])
in
    Source
```

---

## 7. TOP N with Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | Row Limit |
| **Power BI Parameters** | `pStateCode` = "CA", `pTopN` = 100 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT TOP " & Text.From(pTopN) & " * FROM sales_db.customers WHERE state_code='" & pStateCode & "'"])
in
    Source
```

---

## 8. Age Range Parameters

| Property | Value |
|----------|-------|
| **Pattern Name** | Numeric Range Filter |
| **Power BI Parameters** | `pMinAge` = 25, `pMaxAge` = 65 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE age BETWEEN " & Text.From(pMinAge) & " AND " & Text.From(pMaxAge)])
in
    Source
```

---

## 9. IN Clause with Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | List Filter |
| **Power BI Parameter** | `pStateList` = "CA,NY,TX" (no quotes, comma-separated) |

```m
let
    StateList = Text.Combine(List.Transform(Text.Split(pStateList, ","), each "'" & Text.Trim(_) & "'"), ","),
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code IN (" & StateList & ")"])
in
    Source
```

---

## 10. Multiple Optional Parameters

| Property | Value |
|----------|-------|
| **Pattern Name** | Multi Optional Filter |
| **Power BI Parameters** | `pStateCode` = "CA" or "ALL", `pGender` = "M" or "ALL", `pMinIncome` = 0 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE (state_code='" & pStateCode & "' OR 'ALL'='" & pStateCode & "') AND (gender='" & pGender & "' OR 'ALL'='" & pGender & "') AND income >= " & Text.From(pMinIncome)])
in
    Source
```

---

## 11. With ORDER BY Parameter

| Property | Value |
|----------|-------|
| **Pattern Name** | Dynamic Sort |
| **Power BI Parameters** | `pStateCode` = "TX", `pSortColumn` = "income", `pSortDir` = "DESC" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "' ORDER BY " & pSortColumn & " " & pSortDir])
in
    Source
```

---

## 12. Dynamic Table Name

| Property | Value |
|----------|-------|
| **Pattern Name** | Table Parameter |
| **Power BI Parameters** | `pTableName` = "customer", `pStateCode` = "CA" |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db." & pTableName & " WHERE state_code='" & pStateCode & "'"])
in
    Source
```

---

## 13. With CommandTimeout

| Property | Value |
|----------|-------|
| **Pattern Name** | Timeout + Filter |
| **Power BI Parameters** | `pStateCode` = "NY", `pMinIncome` = 30000 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT * FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND income > " & Text.From(pMinIncome), CommandTimeout=#duration(0, 0, 30, 0)])
in
    Source
```

---

## 14. Aggregation with GROUP BY

| Property | Value |
|----------|-------|
| **Pattern Name** | Aggregate Filter |
| **Power BI Parameters** | `pMinIncome` = 25000, `pMinCount` = 10 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT state_code, COUNT(*) as cnt, AVG(income) as avg_income FROM sales_db.customers WHERE income > " & Text.From(pMinIncome) & " GROUP BY state_code HAVING COUNT(*) > " & Text.From(pMinCount)])
in
    Source
```

---

## 15. Full Complex Query

| Property | Value |
|----------|-------|
| **Pattern Name** | Complete Dynamic |
| **Power BI Parameters** | `pSchema` = "val", `pTableName` = "customer", `pStateCode` = "ALL", `pCityName` = "ALL", `pGender` = "ALL", `pMinIncome` = 0, `pMinAge` = 18, `pFirstNamePattern` = "%", `pSortColumn` = "cust_id", `pSortDir` = "ASC", `pTopN` = 500 |

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT TOP " & Text.From(pTopN) & " * FROM " & pSchema & "." & pTableName & " WHERE (state_code='" & pStateCode & "' OR 'ALL'='" & pStateCode & "') AND (city_name='" & pCityName & "' OR 'ALL'='" & pCityName & "') AND (gender='" & pGender & "' OR 'ALL'='" & pGender & "') AND income >= " & Text.From(pMinIncome) & " AND age >= " & Text.From(pMinAge) & " AND first_name LIKE '" & pFirstNamePattern & "' ORDER BY " & pSortColumn & " " & pSortDir, CommandTimeout=#duration(0, 1, 0, 0)])
in
    Source
```

---

## 16. Multiple Source Connections (Conditional Data Source)

| Property | Value |
|----------|-------|
| **Pattern Name** | Multi-Source Conditional |
| **Power BI Parameters** | `pSourceSelector` (Text) = "1" or "2", `pStateCode` = "CA", `pDateType` = "PO" |

**Use Case**: Select between different data sources or query variations based on a parameter. Common scenarios include:
- Processed vs. Inventory data
- Different date ranges or filters
- A/B testing queries
- Regional data sources

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT TOP 100 cust_id, first_name, last_name, income, state_code, TO_DATE('1900/01/01','YYYY/MM/DD') AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='M'"]),
    Source_2 = Teradata.Database("teradata.example.com", [Query="SELECT cust_id, first_name, last_name, income, state_code, CURRENT_DATE AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='F'"]),
    SelectedSource = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = Table.TransformColumnTypes(SelectedSource, {{"report_date", type date}, {"income", type number}})
in
    #"Changed Type"
```

**Key Characteristics**:
- Multiple `Teradata.Database()` calls in the same expression
- Conditional logic (`if...then...else`) selects which source to use
- Downstream transformations may reference specific sources or the selected source
- ALL database connectors must be translated to Snowflake

---

## 17. Multiple Source Connections (Complex UNION-style Queries)

| Property | Value |
|----------|-------|
| **Pattern Name** | Multi-Source Complex |
| **Power BI Parameters** | `pSourceSelector` (Text) = "1" or "2", `pDateFilter` (Text) = "2024-01-01" |

**Use Case**: Complex analytical queries with UNION ALL, multiple JOINs, and conditional source selection.

```m
let
    Source = Teradata.Database("teradata.example.com", [HierarchicalNavigation=true, Query="SELECT TOP 10 * FROM (SELECT c.cust_id, c.first_name, c.last_name, c.income, c.state_code, TO_DATE('1900/01/01','YYYY/MM/DD') AS Calendar_Date, CASE WHEN c.gender='M' THEN 'Male' ELSE 'Female' END AS Gender_Desc FROM sales_db.customers c WHERE c.marital_status = 1 GROUP BY 1,2,3,4,5,6,7 UNION ALL SELECT c.cust_id, c.first_name, c.last_name, c.income, c.state_code, CURRENT_DATE AS Calendar_Date, CASE WHEN c.gender='M' THEN 'Male' ELSE 'Female' END AS Gender_Desc FROM sales_db.customers c WHERE c.marital_status = 2 GROUP BY 1,2,3,4,5,6,7) a"]),
    Source_2 = Teradata.Database("teradata.example.com", [HierarchicalNavigation=true, Query="SELECT c.cust_id, c.first_name, c.last_name, c.income, c.state_code, CURRENT_DATE AS Calendar_Date, CASE WHEN c.gender='M' THEN 'Male' ELSE 'Female' END AS Gender_Desc FROM sales_db.customers c WHERE c.age >= 21 GROUP BY 1,2,3,4,5,6,7"]),
    RowsToReturn = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = if pSourceSelector = "1" then Table.TransformColumnTypes(Source, {{"Calendar_Date", type date}}) else Table.TransformColumnTypes(Source_2, {{"Calendar_Date", type date}})
in
    #"Changed Type"
```

**Key Characteristics**:
- Complex SQL with UNION ALL inside subquery
- `HierarchicalNavigation=true` option
- Multiple CASE expressions
- GROUP BY with positional references
- Conditional type transformations based on selected source

---

## Summary Table

| # | Pattern Name | Parameters | SQL Pattern |
|---|--------------|------------|-------------|
| 1 | Basic Text Filter | `pStateCode` | `WHERE state_code='X'` |
| 2 | Basic Numeric Filter | `pMinIncome` | `WHERE income > N` |
| 3 | Optional Filter | `pStateCode` | `WHERE col='X' OR 'ALL'='X'` |
| 4 | Dual Text Filter | `pStateCode`, `pCityName` | `WHERE a='X' AND b='Y'` |
| 5 | Mixed Type Filter | `pStateCode`, `pMinIncome` | `WHERE text='X' AND num > N` |
| 6 | Wildcard Search | `pFirstNamePattern` | `WHERE LIKE 'X%'` |
| 7 | Row Limit | `pStateCode`, `pTopN` | `SELECT TOP N` |
| 8 | Numeric Range | `pMinAge`, `pMaxAge` | `BETWEEN N1 AND N2` |
| 9 | List Filter | `pStateList` | `WHERE IN ('X','Y')` |
| 10 | Multi Optional | `pStateCode`, `pGender`, `pMinIncome` | Multiple OR conditions |
| 11 | Dynamic Sort | `pStateCode`, `pSortColumn`, `pSortDir` | `ORDER BY col DIR` |
| 12 | Table Parameter | `pTableName`, `pStateCode` | `FROM schema.TABLE` |
| 13 | Timeout + Filter | `pStateCode`, `pMinIncome` | With CommandTimeout |
| 14 | Aggregate Filter | `pMinIncome`, `pMinCount` | `GROUP BY HAVING` |
| 15 | Complete Dynamic | All params | Full parameterized query |
| 16 | Multi-Source Conditional | `pSourceSelector`, `pStateCode` | Multiple `Teradata.Database()` + `if...then...else` |
| 17 | Multi-Source Complex | `pSourceSelector`, `pDateFilter` | Multiple sources + UNION ALL + conditional transforms |

---

## How to Create Power BI Parameters

1. Open Power BI Desktop
2. Go to **Home** → **Manage Parameters** → **New Parameter**
3. Set:
   - **Name:** e.g., `pStateCode`
   - **Type:** Text, Decimal Number, Date, etc.
   - **Current Value:** Default value

## Notes

- Use `Text.From()` to convert numeric parameters to text for SQL concatenation
- Use `Text.Trim()` to remove whitespace from list items
- Use `#duration(days, hours, minutes, seconds)` for CommandTimeout
- The `'ALL'='paramValue'` pattern allows optional filtering (returns all rows when parameter = "ALL")
