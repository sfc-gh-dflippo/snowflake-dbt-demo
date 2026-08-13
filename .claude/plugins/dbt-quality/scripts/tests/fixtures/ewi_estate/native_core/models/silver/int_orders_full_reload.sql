-- INC005: model named as full reload
{{ config(materialized='table') }}

select * from {{ ref('stg_orders') }}
