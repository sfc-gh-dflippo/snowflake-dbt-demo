-- Set Sunday as start of week"
{{ config(
    pre_hook=[ "ALTER SESSION SET WEEK_START = 7" ]
) }}

select
  to_char(DAY_DT, 'YYYYMMDD')::NUMBER(8,0) AS DAY_KEY,
  DAY_SEQ,
  DAY_DT,
  TO_CHAR(DAY_DT, 'YYYY-MM-DD') DAY_TEXT, --ISO 8601 standard
  TO_CHAR(DAY_DT, 'DD.MM.YYYY') DAY_EU_TEXT,
  TO_CHAR(DAY_DT, 'DD') DAY_OF_MONTH,
  decode (extract('dayofweek',DAY_DT),
    1 , 'Sunday',
    2 , 'Monday',
    3 , 'Tuesday',
    4 , 'Wednesday',
    5 , 'Thursday',
    6 , 'Friday',
    7 , 'Saturday'
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
  TO_CHAR(DAY_DT, 'DD')::NUMBER(2) DAY_OF_MONTH_NUM,
  extract('dayofweek',DAY_DT) DAY_OF_WEEK_NUM,
  extract(month from DAY_DT) MONTH_NUM,
  extract(year from DAY_DT) YEAR_NUM,
  date_trunc('YEAR', DAY_DT) as YEAR_START_DT,
  last_day(DAY_DT, 'YEAR') as YEAR_END_DT,
  date_trunc('MONTH', DAY_DT) as MONTH_START_DT,
  last_day(DAY_DT, 'MONTH') as MONTH_END_DT,
  date_trunc('WEEK', DAY_DT) as WEEK_START_DT,
  last_day(DAY_DT, 'WEEK') as WEEK_END_DT,
  DATEADD(YEAR, -1, DAY_DT ) AS YEAR_AGO_DT,
  DATEADD(MONTH, -1, DAY_DT ) AS MONTH_AGO_DT,
  DATEADD(WEEK, -1, DAY_DT ) AS WEEK_AGO_DT,
  CASE WHEN DAY_DT = CURRENT_DATE() THEN 'Y' ELSE 'N' END AS CURRENT_DAY_FLAG,
  CASE WHEN WEEK_START_DT = date_trunc('WEEK', CURRENT_DATE()) THEN 'Y' ELSE 'N' END AS CURRENT_WEEK_FLAG,
  CASE WHEN MONTH_START_DT = date_trunc('MONTH', CURRENT_DATE()) THEN 'Y' ELSE 'N' END AS CURRENT_MONTH_FLAG,
  CASE WHEN YEAR_START_DT = date_trunc('WEEK', CURRENT_DATE()) THEN 'Y' ELSE 'N' END AS CURRENT_YEAR_FLAG,
  SYSDATE() as dbt_last_update_ts
  from
  (select
    row_number() over (order by seq4() )-1 as DAY_SEQ,
    DATEADD(day, DAY_SEQ, '1992-01-01'::DATE) as DAY_DT
    from table(generator(rowcount => 30 * 365 )))
order by DAY_SEQ asc
