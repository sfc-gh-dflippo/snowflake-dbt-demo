{{ config(
    materialized='table',
    tags=['gold', 'crawl', 'reporting']
) }}

-- GOLD CRAWL: Simple business reporting
-- Complexity: Beginner - Basic aggregations for business users
-- Features demonstrated: Simple business metrics, clean column names

select 
    nation_name,
    government_type,
    nation_comment,
    
    -- Simple metrics
    name_length,
    case 
        when name_length <= 5 then 'SHORT'
        when name_length <= 10 then 'MEDIUM'
        else 'LONG'
    end as name_category,
    
    -- Business-friendly formatting
    initcap(nation_name) as display_name,
    
    processed_at as last_updated

from {{ ref('clean_nations') }}
order by nation_name
