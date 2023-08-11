{{- config(
    pre_hook=[ "ALTER SESSION SET WEEK_START = 7", "ALTER SESSION SET WEEK_OF_YEAR_POLICY = 1" ],
    post_hook=[ "{%- do insert_ghost_key( 'DAY_KEY', 0,
        {'DAY_SEQ': '0', 'DAY_DT': \"'1900-01-01'::DATE\"}
    ) -%}" ]
) -}}

WITH TODAY AS (
    SELECT
    CURRENT_DATE() AS CURRENT_DAY,
    date_trunc('WEEK', CURRENT_DAY) AS CURRENT_WEEK_START,
    date_trunc('MONTH', CURRENT_DAY) AS CURRENT_MONTH_START,
    date_trunc('WEEK', CURRENT_DAY) AS CURRENT_YEAR_START
),

DATA_GENERATOR AS (
    SELECT
    row_number() over (order by seq4() ) as DAY_SEQ
    from table(generator(rowcount => 50 * 365 ))
)

select
  DAY_SEQ,
  DATEADD(day, DAY_SEQ-1, '1992-01-01'::DATE) AS DAY_DT,
  to_char(DAY_DT, 'YYYYMMDD')::NUMBER(8,0) AS DAY_KEY,
  TO_CHAR(DAY_DT, 'YYYY-MM-DD') DAY_TEXT, --ISO 8601 standard
  TO_CHAR(DAY_DT, 'DD.MM.YYYY') DAY_EU_TEXT,
  TO_CHAR(DAY_DT, 'DD') DAY_OF_MONTH,
  -- Use ISO standard to avoid WEEK_START parameter
  decode (extract('dayofweekiso',DAY_DT),
    1 , 'Monday',
    2 , 'Tuesday',
    3 , 'Wednesday',
    4 , 'Thursday',
    5 , 'Friday',
    6 , 'Saturday',
    7 , 'Sunday'
    ) DAY_OF_WEEK,
decode (extract(month from DAY_DT),
    1 , 'January',
    2 , 'February',
    3 , 'March',
    4 , 'April',
    5 , 'May',
    6 , 'June',
    7 , 'July',
    8 , 'August',
    9 , 'September',
    10, 'October',
    11, 'November',
    12, 'December'
    ) MONTH,
  TO_CHAR(DAY_DT, 'YYYY') year,
  TO_CHAR(DAY_DT, 'QQ') QUARTER,
  DECODE(QUARTER,
    'Q1', 'First',
    'Q2', 'Second',
    'Q3', 'Third',
    'Q4', 'Fourth'
    ) QUARTER_NAME,
  TO_CHAR(DAY_DT, 'DD')::NUMBER(2,0) DAY_OF_MONTH_NUM,
  extract(dayofweek from DAY_DT)::NUMBER(2,0) DAY_OF_WEEK_NUM,
  extract(dayofweekiso from DAY_DT)::NUMBER(1,0) DAY_OF_WEEK_ISO_NUM,
  extract(week from DAY_DT)::NUMBER(2,0) WEEK_NUM,
  extract(weekiso from DAY_DT)::NUMBER(2,0) WEEK_ISO_NUM,
  extract(month from DAY_DT)::NUMBER(2,0) MONTH_NUM,
  extract(quarter from DAY_DT)::NUMBER(1,0) QUARTER_NUM,
  extract(year from DAY_DT)::NUMBER(4,0) YEAR_NUM,
  extract(yearofweekiso from DAY_DT)::NUMBER(4,0) YEAR_OF_WEEK_ISO_NUM,
  date_trunc('YEAR', DAY_DT) as YEAR_START_DT,
  last_day(DAY_DT, 'YEAR') as YEAR_END_DT,
  date_trunc('MONTH', DAY_DT) as MONTH_START_DT,
  last_day(DAY_DT, 'MONTH') as MONTH_END_DT,
  date_trunc('WEEK', DAY_DT) as WEEK_START_DT,
  last_day(DAY_DT, 'WEEK') as WEEK_END_DT,
  DATEADD(YEAR, -1, DAY_DT ) AS YEAR_AGO_DT,
  DATEADD(MONTH, -1, DAY_DT ) AS MONTH_AGO_DT,
  DATEADD(WEEK, -1, DAY_DT ) AS WEEK_AGO_DT,
  YEAR_END_DT - YEAR_START_DT + 1 AS DAYS_IN_YEAR,
  YEAR_END_DT - YEAR_START_DT + 1 AS DAYS_IN_MONTH,
  CASE WHEN DAY_DT = CURRENT_DAY THEN 'Y' ELSE 'N' END AS CURRENT_DAY_FLAG,
  CASE WHEN CURRENT_WEEK_START = WEEK_START_DT THEN 'Y' ELSE 'N' END AS CURRENT_WEEK_FLAG,
  CASE WHEN CURRENT_MONTH_START = MONTH_START_DT THEN 'Y' ELSE 'N' END AS CURRENT_MONTH_FLAG,
  CASE WHEN CURRENT_YEAR_START = YEAR_START_DT THEN 'Y' ELSE 'N' END AS CURRENT_YEAR_FLAG,
  SYSDATE() as DBT_INSERT_TS,
  SYSDATE() as DBT_LAST_UPDATE_TS
from DATA_GENERATOR
CROSS JOIN TODAY
