{#-
    Compile-time check of the argument forms that insert_ghost_key and
    integration_key support. The test fails at compile time on a mismatch.
-#}
{%- macro _norm(sql) -%}{{ sql.split() | join(' ') }}{%- endmacro -%}

{%- set body = "from ( select 0 as ghost_val ) as ghost_row left outer join T t on k = ghost_row.ghost_val where k is null limit 1" -%}

{%- set expected = {
    'dict_empty':  "insert into T ( k ) select 0 " ~ body,
    'dict_none':   "insert into T ( k ) select 0 " ~ body,
    'dict_one':    "insert into T ( k, a ) select 0, 1 " ~ body,
    'dict_many':   "insert into T ( k, a, b ) select 0, 1, 'x' " ~ body,
} -%}
{%- set actual = {
    'dict_empty':  _norm(insert_ghost_key_sql('T', 'k', 0, {})),
    'dict_none':   _norm(insert_ghost_key_sql('T', 'k', 0, none)),
    'dict_one':    _norm(insert_ghost_key_sql('T', 'k', 0, {'a': '1'})),
    'dict_many':   _norm(insert_ghost_key_sql('T', 'k', 0, {'a': '1', 'b': "'x'"})),
} -%}
{%- for name, want in expected.items() -%}
    {%- if actual[name] != want -%}
        {{ exceptions.raise_compiler_error("insert_ghost_key_sql " ~ name ~ ": got [" ~ actual[name] ~ "] want [" ~ want ~ "]") }}
    {%- endif -%}
{%- endfor -%}

{%- set ik_want = {
    'one':   "COALESCE(a::VARCHAR, '')",
    'two':   "COALESCE(a::VARCHAR, '') || '~' || COALESCE(b::VARCHAR, '')",
    'empty': "",
} -%}
{%- set ik_got = {
    'one':   integration_key(['a']),
    'two':   integration_key(['a', 'b']),
    'empty': integration_key([]),
} -%}
{%- for name, want in ik_want.items() -%}
    {%- if ik_got[name] | trim != want -%}
        {{ exceptions.raise_compiler_error("integration_key " ~ name ~ ": got [" ~ ik_got[name] ~ "] want [" ~ want ~ "]") }}
    {%- endif -%}
{%- endfor -%}

select 1 as failed where false
