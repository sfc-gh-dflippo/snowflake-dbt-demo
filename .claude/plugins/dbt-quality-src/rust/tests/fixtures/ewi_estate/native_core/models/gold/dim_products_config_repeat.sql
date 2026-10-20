-- MAT006 trigger: config(materialized='table') repeats the gold folder default
{{ config(materialized='table') }}
select 1 as product_id, 'widget' as product_name
