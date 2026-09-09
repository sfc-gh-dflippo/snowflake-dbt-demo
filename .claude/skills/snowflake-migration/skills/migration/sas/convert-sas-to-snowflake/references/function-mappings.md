# SAS to Snowflake Function Mappings

## When to Load

Load for **all conversions** - comprehensive function translation reference.

---

## String Functions

| SAS Function | Snowflake Equivalent | Notes |
|--------------|---------------------|-------|
| `SUBSTR(str, pos, len)` | `SUBSTR(str, pos, len)` | Direct mapping |
| `SUBSTRN(str, pos, len)` | `SUBSTR(str, pos, len)` | Same as SUBSTR |
| `SCAN(str, n, 'delim')` | `SPLIT_PART(str, 'delim', n)` | Word extraction |
| `INDEX(str, substr)` | `CHARINDEX(substr, str)` | Find position |
| `FIND(str, substr, pos, 'i')` | `CHARINDEX(LOWER(substr), LOWER(str), pos)` | Case-insensitive with 'i' modifier |
| `UPCASE(str)` | `UPPER(str)` | |
| `LOWCASE(str)` | `LOWER(str)` | |
| `PROPCASE(str)` | `INITCAP(str)` | Title case |
| `TRIM(str)` | `TRIM(str)` | |
| `LEFT(str)` | `LTRIM(str)` | Left trim |
| `RIGHT(str)` | `RTRIM(str)` | Right trim |
| `STRIP(str)` | `TRIM(str)` | Both sides |
| `LENGTH(str)` | `LENGTH(str)` | |
| `LENGTHN(str)` | `LENGTH(str)` | |
| `LENGTHC(str)` | `LENGTH(str)` | |
| `REVERSE(str)` | `REVERSE(str)` | |
| `REPEAT(str, n)` | `REPEAT(str, n)` | |
| `TRANSLATE(str, to, from)` | `TRANSLATE(str, from, to)` | ⚠️ Argument order differs |
| `SOUNDEX(str)` | `SOUNDEX(str)` | |
| `BYTE(n)` | `CHR(n)` | Character from ASCII |
| `RANK(char)` | `ASCII(char)` | ASCII from character |

## Concatenation Functions

| SAS Function | Snowflake Equivalent | Notes |
|--------------|---------------------|-------|
| `CAT(a, b, c)` | `CONCAT(a, b, c)` | Simple concat |
| `CATS(a, b, c)` | `CONCAT(TRIM(COALESCE(a,'')), TRIM(COALESCE(b,'')), TRIM(COALESCE(c,'')))` | Strip all then concat |
| `CATT(a, b, c)` | `CONCAT(RTRIM(COALESCE(a,'')), RTRIM(COALESCE(b,'')), RTRIM(COALESCE(c,'')))` | Trailing trim then concat |
| `CATX('sep', a, b, c)` | `CONCAT_WS('sep', TRIM(COALESCE(a,'')), TRIM(COALESCE(b,'')), TRIM(COALESCE(c,'')))` | With separator |
| `a \|\| b` | `a \|\| b` | Direct mapping |

## COMPRESS Function (Special Handling)

**1-argument form (remove ALL whitespace):**

SAS `COMPRESS(str)` with NO second argument removes **all** whitespace characters — spaces, tabs, newlines, carriage returns, etc. — NOT just spaces.

```sql
-- SAS: COMPRESS(str)
-- Snowflake (CORRECT — removes all whitespace):
REGEXP_REPLACE(str, '\\s', '')
```

**⚠️ FORBIDDEN:** Do NOT map `COMPRESS(str)` to `REPLACE(str, ' ', '')` — that only strips spaces and silently leaves tabs/newlines/CR. Also do NOT expand it into a chain of nested `REPLACE(...)` calls per character — that is verbose, error-prone, and misses characters. A single `REGEXP_REPLACE(expr, '\\s', '')` matches SAS default `COMPRESS()` behavior exactly.

**2-argument form (remove specific chars):**
```sql
-- SAS: COMPRESS(str, 'abc')
-- Snowflake:
REGEXP_REPLACE(str, '[abc]', '')
```

**3-argument form with modifiers:**

| Modifier | Meaning | Snowflake Pattern |
|----------|---------|-------------------|
| `a`, `i` | Alphabetic | `[A-Za-z]` |
| `d` | Digits | `[0-9]` |
| `n` | Alphanumeric + underscore | `[A-Za-z0-9_]` |
| `l` | Lowercase | `[a-z]` |
| `u` | Uppercase | `[A-Z]` |
| `f` | Underscore + letters | `[A-Za-z_]` |
| `k` | **KEEP** these chars (invert) | Use `[^...]` |

```sql
-- SAS: COMPRESS(str, '', 'kd')  -- Keep only digits
-- Snowflake:
REGEXP_REPLACE(str, '[^0-9]', '')

-- SAS: COMPRESS(str, '', 'd')   -- Remove digits
-- Snowflake:
REGEXP_REPLACE(str, '[0-9]', '')
```

## COMPBL Function

```sql
-- SAS: COMPBL(str)  -- Compress multiple blanks to single
-- Snowflake:
REGEXP_REPLACE(str, ' +', ' ')
```

## Conditional Functions

| SAS Function | Snowflake Equivalent | Notes |
|--------------|---------------------|-------|
| `IFC(cond, true_str, false_str)` | `CASE WHEN cond THEN true_str ELSE false_str END` | Character IF |
| `IFN(cond, true_num, false_num)` | `CASE WHEN cond THEN true_num ELSE false_num END` | Numeric IF |
| `COALESCE(a, b, c)` | `COALESCE(a, b, c)` | First non-null |
| `COALESCEC(a, b, c)` | `COALESCE(a, b, c)` | Character version |

**Nested IFC/IFN handling:**
Parse with balanced parentheses to handle:
```sas
IFC(cond1, IFC(cond2, 'A', 'B'), 'C')
```
→
```sql
CASE WHEN cond1 THEN 
  CASE WHEN cond2 THEN 'A' ELSE 'B' END 
ELSE 'C' END
```

## Date/Time Functions

| SAS Function | Snowflake Equivalent | Notes |
|--------------|---------------------|-------|
| `TODAY()` | `CURRENT_DATE()` | |
| `DATE()` | `CURRENT_DATE()` | |
| `DATETIME()` | `CURRENT_TIMESTAMP()` | |
| `TIME()` | `CURRENT_TIME()` | |
| `YEAR(date)` | `YEAR(date)` | |
| `MONTH(date)` | `MONTH(date)` | |
| `DAY(date)` | `DAY(date)` | |
| `HOUR(dt)` | `HOUR(dt)` | |
| `MINUTE(dt)` | `MINUTE(dt)` | |
| `SECOND(dt)` | `SECOND(dt)` | |
| `WEEK(date)` | `WEEK(date)` | |
| `QTR(date)` | `QUARTER(date)` | |
| `WEEKDAY(date)` | `DAYOFWEEK(date)` | |
| `DATEPART(datetime)` | `TO_DATE(datetime)` | Extract date from datetime |
| `TIMEPART(datetime)` | `TO_TIME(datetime)` | Extract time from datetime |
| `MDY(m, d, y)` | `DATE_FROM_PARTS(y, m, d)` | ⚠️ Argument order differs |
| `YMD(y, m, d)` | `DATE_FROM_PARTS(y, m, d)` | |
| `HMS(h, m, s)` | `TIME_FROM_PARTS(h, m, s)` | |
| `DHMS(date, h, m, s)` | `TIMESTAMP_FROM_PARTS(...)` | Complex conversion |

## INTCK (Date Intervals)

```sql
-- SAS: INTCK('MONTH', start_date, end_date)
-- Snowflake:
DATEDIFF('month', start_date, end_date)
```

| SAS Interval | Snowflake Interval |
|--------------|-------------------|
| `'YEAR'` | `'year'` |
| `'MONTH'` | `'month'` |
| `'DAY'` | `'day'` |
| `'WEEK'` | `'week'` |
| `'HOUR'` | `'hour'` |
| `'MINUTE'` | `'minute'` |
| `'SECOND'` | `'second'` |
| `'QTR'` | `'quarter'` |
| `'QUARTER'` | `'quarter'` |

## INTNX (Date Arithmetic)

```sql
-- SAS: INTNX('MONTH', date, 3)           -- Default alignment = 'S' (same day)
-- Snowflake:
DATEADD('month', 3, date)

-- SAS: INTNX('MONTH', date, 3, 'B')      -- Beginning of interval
-- Snowflake:
DATE_TRUNC('month', DATEADD('month', 3, date))

-- SAS: INTNX('MONTH', date, 3, 'E')      -- End of interval
-- Snowflake:
LAST_DAY(DATEADD('month', 3, date))

-- SAS: INTNX('MONTH', date, 0, 'B')      -- Beginning of CURRENT month
-- Snowflake:
DATE_TRUNC('month', date)

-- SAS: INTNX('MONTH', date, 0, 'E')      -- End of CURRENT month
-- Snowflake:
LAST_DAY(date)

-- SAS: INTNX('YEAR', date, 1, 'B')       -- Beginning of next year
-- Snowflake:
DATE_TRUNC('year', DATEADD('year', 1, date))

-- SAS: INTNX('YEAR', date, 0, 'E')       -- End of current year
-- Snowflake:
DATEADD('day', -1, DATE_TRUNC('year', DATEADD('year', 1, date)))

-- SAS: INTNX('WEEK', date, 0, 'B')       -- Beginning of current week
-- Snowflake:
DATE_TRUNC('week', date)

-- SAS: INTNX('QTR', date, 1, 'B')        -- Beginning of next quarter
-- Snowflake:
DATE_TRUNC('quarter', DATEADD('quarter', 1, date))
```

**INTNX alignment parameter reference:**

| Alignment | Meaning | Snowflake Pattern |
|-----------|---------|-------------------|
| `'S'` (default) | Same day within new interval | `DATEADD(interval, n, date)` |
| `'B'` | Beginning of target interval | `DATE_TRUNC(interval, DATEADD(interval, n, date))` |
| `'E'` | End of target interval | For month: `LAST_DAY(DATEADD(...))`. For others: `DATEADD('day', -1, DATE_TRUNC(interval, DATEADD(interval, n+1, date)))` |
| `'M'` | Middle of target interval | Flag `MANUAL_REVIEW_REQUIRED` — complex midpoint logic |

**⚠️ CRITICAL:** Do NOT assume `DATEADD` alone is equivalent to `INTNX` without checking the alignment parameter. The default ('S') maps to DATEADD, but 'B' and 'E' require DATE_TRUNC/LAST_DAY wrapping.

## INPUT/PUT (Type Conversion)

**INPUT (string to typed value):**
```sql
-- SAS: INPUT(str, 8.)        -- To number
-- Snowflake:
TRY_TO_NUMBER(str)

-- SAS: INPUT(str, DATE9.)    -- To date
-- Snowflake:
TRY_TO_DATE(str)

-- SAS: INPUT(str, DATETIME20.)
-- Snowflake:
TRY_TO_TIMESTAMP(str)

-- SAS: INPUT(str, $20.)      -- Character (just trim)
-- Snowflake:
TRIM(str)
```

**PUT (typed value to string):**
```sql
-- SAS: PUT(num, 8.)
-- Snowflake:
TO_VARCHAR(num)

-- SAS: PUT(date, DATE9.)
-- Snowflake:
TO_VARCHAR(date, 'DDMONYYYY')

-- SAS: PUT(num, Z5.)         -- Zero-padded
-- Snowflake:
LPAD(TO_VARCHAR(num), 5, '0')

-- SAS: PUT(num, COMMA12.2)
-- Snowflake:
TO_VARCHAR(num, '999,999,999.99')
```

## Regular Expression Functions

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `PRXMATCH('/pattern/', str)` | `CASE WHEN REGEXP_LIKE(str, 'pattern') THEN 1 ELSE 0 END` |
| `PRXCHANGE('s/pat/repl/', -1, str)` | `REGEXP_REPLACE(str, 'pat', 'repl')` |
| `PRXCHANGE('s/pat/repl/', 1, str)` | `REGEXP_REPLACE(str, 'pat', 'repl', 1, 1)` |

## Word Functions

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `COUNTW(str)` | `ARRAY_SIZE(SPLIT(TRIM(str), ' '))` |
| `COUNTW(str, 'delim')` | `ARRAY_SIZE(SPLIT(str, 'delim'))` |
| `TRANWRD(str, find, replace)` | `REPLACE(str, find, replace)` |

## VERIFY Function

```sql
-- SAS: VERIFY(str, 'valid_chars')
-- Returns 0 if all chars valid, else position of first invalid
-- Snowflake:
CASE 
  WHEN REGEXP_LIKE(str, '^[valid_chars]*$') THEN 0 
  ELSE REGEXP_INSTR(str, '[^valid_chars]') 
END
```

## Numeric Functions

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `ABS(x)` | `ABS(x)` |
| `ROUND(x, n)` | `ROUND(x, n)` |
| `CEIL(x)` | `CEIL(x)` |
| `CEILING(x)` | `CEIL(x)` |
| `FLOOR(x)` | `FLOOR(x)` |
| `INT(x)` | `TRUNC(x)` |
| `MOD(x, y)` | `MOD(x, y)` |
| `SQRT(x)` | `SQRT(x)` |
| `LOG(x)` | `LN(x)` |
| `LOG10(x)` | `LOG(10, x)` |
| `LOG2(x)` | `LOG(2, x)` |
| `EXP(x)` | `EXP(x)` |
| `POWER(x, y)` | `POWER(x, y)` |
| `SIGN(x)` | `SIGN(x)` |
| `RANUNI(seed)` | `RANDOM()` |
| `RAND('UNIFORM')` | `RANDOM()` |

## Aggregate Functions

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `SUM(x)` | `SUM(x)` |
| `MEAN(x)` | `AVG(x)` |
| `MIN(x)` | `MIN(x)` |
| `MAX(x)` | `MAX(x)` |
| `COUNT(x)` | `COUNT(x)` |
| `N(x)` | `COUNT(x)` |
| `NMISS(x)` | `COUNT_IF(x IS NULL)` |
| `STD(x)` | `STDDEV(x)` |
| `VAR(x)` | `VARIANCE(x)` |
| `MEDIAN(x)` | `MEDIAN(x)` |
| `SKEWNESS(x)` | `SKEW(x)` |
| `KURTOSIS(x)` | `KURTOSIS(x)` |

## Window/Lag Functions

| SAS Function | Snowflake Equivalent |
|--------------|---------------------|
| `LAG(var)` | `LAG(var) OVER (ORDER BY ...)` |
| `LAG1(var)` | `LAG(var, 1) OVER (ORDER BY ...)` |
| `LAG2(var)` | `LAG(var, 2) OVER (ORDER BY ...)` |
| `DIF(var)` | `var - LAG(var) OVER (ORDER BY ...)` |

## Missing Value Handling

| SAS Construct | Snowflake Equivalent |
|---------------|---------------------|
| `.` (numeric missing) | `NULL` |
| `var = .` | `var IS NULL` |
| `var NE .` | `var IS NOT NULL` |
| `MISSING(var)` | `var IS NULL` |
| `NOTMISSING(var)` | `var IS NOT NULL` |

## Operator Conversions

| SAS Operator | Snowflake Operator |
|--------------|-------------------|
| `EQ` | `=` |
| `NE` | `<>` |
| `LT` | `<` |
| `LE` | `<=` |
| `GT` | `>` |
| `GE` | `>=` |
| `^=` | `<>` |
| `~=` | `<>` |
| `AND` | `AND` |
| `OR` | `OR` |
| `NOT` | `NOT` |

## Date Literal Conversions

```sql
-- SAS: '01JAN2024'd
-- Snowflake:
TO_DATE('01JAN2024', 'DDMONYYYY')

-- SAS: '01JAN2024:12:30:00'dt
-- Snowflake:
TO_TIMESTAMP('01JAN2024:12:30:00', 'DDMONYYYY:HH24:MI:SS')
```

## SAS Date Format to Snowflake Format

| SAS Format | Snowflake Format |
|------------|-----------------|
| `YYMMDD10.` | `YYYY-MM-DD` |
| `DDMMYY10.` | `DD/MM/YYYY` |
| `MMDDYY10.` | `MM/DD/YYYY` |
| `DATE9.` | `DDMONYYYY` |
| `DATETIME20.` | `YYYY-MM-DD HH24:MI:SS` |
| `TIME8.` | `HH24:MI:SS` |
| `MONYY7.` | `MONYYYY` |
| `YEAR4.` | `YYYY` |
| `COMMA12.2` | `999,999,999.99` |
| `DOLLAR12.2` | `$999,999,999.99` |
| `PERCENT8.2` | `999.99%` |

## Special Variables

| SAS Variable | Snowflake Equivalent |
|--------------|---------------------|
| `_N_` | `ROW_NUMBER() OVER (ORDER BY 1)` |
| `MONOTONIC()` | `ROW_NUMBER() OVER ()` |
| `_ERROR_` | No direct equivalent; use TRY_* functions |
| `END=last` (SET option) | `ROW_NUMBER() OVER (ORDER BY sort_col DESC) = 1` |

---

## SAS Automatic (Predefined) Macro Variables

SAS supplies automatic macro variables resolved at compile time. Convert each to its Snowflake equivalent — never leave a raw `&SYS...` reference in the output.

| SAS Automatic Variable | Snowflake Equivalent |
|------------------------|----------------------|
| `&SYSDATE` / `&SYSDATE9` | `TO_CHAR(CURRENT_DATE(), 'DDMONYY')` / `'DDMONYYYY'` |
| `&SYSTIME` | `TO_CHAR(CURRENT_TIME(), 'HH24:MI')` |
| `&SYSDAY` | `DAYNAME(CURRENT_DATE())` |
| `&SYSUSERID` | `CURRENT_USER()` |
| `&SYSPROCESSID` / `&SYSJOBID` | `CURRENT_SESSION()` |
| `&SQLOBS` | `SQLROWCOUNT` (rows from last DML) or `COUNT(*)` of the result |
| `&SQLRC` / `&SYSERR` | Scripting exception state (`SQLCODE` / `SQLERRM`); see multi-block-orchestration.md for `&SYSERR` flow gating |

Macro-language string/index functions (complements `%SCAN`, `%EVAL`, `%SYSFUNC` in macros.md):

| SAS Macro Function | Snowflake Equivalent |
|--------------------|----------------------|
| `%SUBSTR(str, pos, len)` | `SUBSTR(str, pos, len)` |
| `%SCAN(str, n, delim)` | `SPLIT_PART(str, delim, n)` |
| `%INDEX(source, sub)` | `POSITION(sub IN source)` |
| `%LENGTH(str)` | `LENGTH(str)` |
| `%UPCASE` / `%LOWCASE` | `UPPER` / `LOWER` |

---

## SAS Sum Statement (x + y;)

**CRITICAL:** The SAS sum statement `x + y;` (variable + expression followed by semicolon, no assignment operator) is NOT regular arithmetic:
- It **RETAINS x** across rows (initializes to 0, not missing)
- It **adds y to x**, treating missing values as 0
- Equivalent to: `RETAIN x 0; x = SUM(x, y);`

```sql
-- SAS: total + amount;
-- Snowflake (window function):
SUM(COALESCE(amount, 0)) OVER (
  PARTITION BY group_col 
  ORDER BY sort_col 
  ROWS UNBOUNDED PRECEDING
) AS total

-- SAS: total + amount; (with BY group reset)
-- If FIRST.group resets total, the PARTITION BY handles it automatically
```

---

## Oracle / DB2 Passthrough Function Mappings

See `references/vendor-function-mappings.md` for full Oracle→Snowflake and DB2→Snowflake function mapping tables and SQL passthrough conversion steps.
