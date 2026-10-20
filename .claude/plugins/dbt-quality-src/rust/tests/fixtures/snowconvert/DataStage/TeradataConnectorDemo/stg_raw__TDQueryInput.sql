SELECT
   COL1,
   COL2
FROM
   {{ source('raw_InputSchema', 'QUERY_TABLE') }}
WHERE
   COLLATE(REGION, 'en-ci-rtrim') = '{{ var('pRegion', 'pRegion') }}'
