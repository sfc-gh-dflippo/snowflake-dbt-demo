{{- config(
    pre_hook=[ "ALTER SESSION SET WEEK_START = 7", "ALTER SESSION SET WEEK_OF_YEAR_POLICY = 1" ],
    post_hook=[ "{%- do insert_ghost_key( 'DAY_KEY', 0,
        {'DAY_SEQ': '0', 'DAY_DT': \"'1900-01-01'::DATE\", 'DAY_TEXT': \"'1900-01-01'\", 'MONTH': \"'January'\", 'QUARTER_NAME': \"'First'\", 'YEAR_NUM': '1900'}
    ) -%}" ],
    alias='DIM_CALENDAR_DAY'
) -}}

with today as (
    select
        current_date() as current_day,
        date_trunc('WEEK', current_day) as current_week_start,
        date_trunc('MONTH', current_day) as current_month_start,
        date_trunc('WEEK', current_day) as current_year_start
),

data_generator as (
    select row_number() over (order by seq4()) as day_seq
    from table(generator(rowcount => 50 * 365))
)

select
    day_seq,
    dateadd(day, day_seq - 1, '1992-01-01'::date) as day_dt,
    to_char(day_dt, 'YYYYMMDD')::number(8, 0) as day_key,
    to_char(day_dt, 'YYYY-MM-DD') as day_text, --ISO 8601 standard
    to_char(day_dt, 'DD.MM.YYYY') as day_eu_text,
    to_char(day_dt, 'DD') as day_of_month,
    -- Use ISO standard to avoid WEEK_START parameter
    decode(
        extract('dayofweekiso', day_dt),
        1, 'Monday',
        2, 'Tuesday',
        3, 'Wednesday',
        4, 'Thursday',
        5, 'Friday',
        6, 'Saturday',
        7, 'Sunday'
    ) as day_of_week,
    decode(
        extract(month from day_dt),
        1, 'January',
        2, 'February',
        3, 'March',
        4, 'April',
        5, 'May',
        6, 'June',
        7, 'July',
        8, 'August',
        9, 'September',
        10, 'October',
        11, 'November',
        12, 'December'
    ) as month,
    to_char(day_dt, 'YYYY') as year,
    'Q' || extract(quarter from day_dt) as quarter,
    decode(
        extract(quarter from day_dt),
        1, 'First',
        2, 'Second',
        3, 'Third',
        4, 'Fourth'
    ) as quarter_name,
    to_char(day_dt, 'DD')::number(2, 0) as day_of_month_num,
    extract(dayofweek from day_dt)::number(2, 0) as day_of_week_num,
    extract(dayofweekiso from day_dt)::number(1, 0) as day_of_week_iso_num,
    extract(week from day_dt)::number(2, 0) as week_num,
    extract(weekiso from day_dt)::number(2, 0) as week_iso_num,
    extract(month from day_dt)::number(2, 0) as month_num,
    extract(quarter from day_dt)::number(1, 0) as quarter_num,
    extract(year from day_dt)::number(4, 0) as year_num,
    extract(yearofweekiso from day_dt)::number(4, 0) as year_of_week_iso_num,
    date_trunc('YEAR', day_dt) as year_start_dt,
    last_day(day_dt, 'YEAR') as year_end_dt,
    date_trunc('MONTH', day_dt) as month_start_dt,
    last_day(day_dt, 'MONTH') as month_end_dt,
    date_trunc('WEEK', day_dt) as week_start_dt,
    last_day(day_dt, 'WEEK') as week_end_dt,
    dateadd(year, -1, day_dt) as year_ago_dt,
    dateadd(month, -1, day_dt) as month_ago_dt,
    dateadd(week, -1, day_dt) as week_ago_dt,
    year_end_dt - year_start_dt + 1 as days_in_year,
    year_end_dt - year_start_dt + 1 as days_in_month,
    case when day_dt = current_day then 'Y' else 'N' end as current_day_flag,
    case when current_week_start = week_start_dt then 'Y' else 'N' end as current_week_flag,
    case when current_month_start = month_start_dt then 'Y' else 'N' end as current_month_flag,
    case when current_year_start = year_start_dt then 'Y' else 'N' end as current_year_flag,
    sysdate() as dbt_insert_ts,
    sysdate() as dbt_last_update_ts
from data_generator
cross join today
