-- Generic test: Check that values in a column are positive
-- Usage: tests: [positive_values]

{% test positive_values(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} <= 0

{% endtest %}
