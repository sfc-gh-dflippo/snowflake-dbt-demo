SELECT
   ROUTE_ID
FROM
   {{ source('raw_InputSchema', 'TD_PARAM_TABLE') }} AS TD_PARAM_TABLE