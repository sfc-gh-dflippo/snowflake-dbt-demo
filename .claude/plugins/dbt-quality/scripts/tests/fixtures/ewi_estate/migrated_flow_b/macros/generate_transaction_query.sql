-- MAC005: macro that emits a full query
-- MAC006: hardcoded relation in macro
{% macro generate_transaction_query(transactions_ref, accounts_ref) %}
    select
        t.transaction_id,
        t.account_id,
        t.amount,
        a.account_name
    from analytics.raw.transactions t
    join {{ accounts_ref }} a on t.account_id = a.account_id
{% endmacro %}
