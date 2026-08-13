-- MAC008: model body mostly Jinja
{{ config(materialized='table') }}

{{ generate_transaction_query(ref('stg_transactions'), ref('stg_accounts')) }}
{{ add_audit_fields('transaction_id') }}
{{ apply_scd_logic('account_id', 'effective_date') }}
