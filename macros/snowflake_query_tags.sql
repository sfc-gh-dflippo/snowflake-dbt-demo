{#

This macro is derived from the dbt-snowflake-query-tags package from get-select, published under the MIT Licence.

You can find the original package at:
https://github.com/get-select/dbt-snowflake-query-tags

#}
{% macro set_query_tag() -%}

    {# Get session level query tag #}
    {% set original_query_tag = get_current_query_tag() %}
    {% set original_query_tag_parsed = {} %}

    {% if original_query_tag %}
        {% if fromjson(original_query_tag) is mapping %}
            {% set original_query_tag_parsed = fromjson(original_query_tag) %}
        {% endif %}
    {% endif %}

    {# Start with any model-configured dict #}
    {% set query_tag_dict = config.get('query_tag', default={}) %}

    {% if query_tag_dict is not mapping %}
    {% do log("set_query_tag() warning: the query_tag config value of '{}' is not a mapping type, so is being ignored. If you'd like to add additional query tag information, use a mapping type instead, or remove it to avoid this message.".format(query_tag), True) %}
    {% set query_tag_dict = {} %} {# If the user has set the query tag config as a non mapping type, start fresh #}
    {% endif %}

    {% do query_tag_dict.update(original_query_tag_parsed) %}

    {%- do query_tag_dict.update(
        app='dbt',
        dbt_version=dbt_version,
        project_name=project_name,
        target_name=target.name,
        target_database=target.database,
        target_schema=target.schema,
        invocation_id=invocation_id,
        run_started_at=run_started_at.astimezone(modules.pytz.utc).isoformat(),
        full_refresh=flags.FULL_REFRESH,
        which=flags.WHICH,
    ) -%}

    {%- if model -%}
        {%- do query_tag_dict.update(
            node_name=model.name,
            node_alias=model.alias,
            node_package_name=model.package_name,
            node_original_file_path=model.original_file_path,
            node_database=model.database,
            node_schema=model.schema,
            node_unique_id=model.unique_id,
            node_resource_type=model.resource_type,
            node_meta=model.config.meta,
            node_tags=model.tags,
        ) -%}

        {% if model.resource_type == 'model' %}
            {%- do query_tag_dict.update(
                is_incremental=is_incremental()
            ) -%}
        {% endif %}

        {%- if flags.INVOCATION_COMMAND -%}
            {%- do query_tag_dict.update(
                invocation_command=flags.INVOCATION_COMMAND
            ) -%}
        {%- endif -%}

        {%- if model.resource_type != ('seed') -%} {# Otherwise this throws an error saying 'Seeds cannot depend on other nodes.' #}
            {%- if model.refs is defined -%}
                {% set refs = [] %}
                {% for ref in model.refs %}
                    {%- if dbt_version >= '1.5.0' -%}
                        {%- do refs.append(ref.name) -%}
                    {%- else -%}
                        {%- do refs.append(ref[0]) -%}
                    {%- endif -%}
                {% endfor %}
                {%- do query_tag_dict.update(
                    node_refs=refs | unique | list
                ) -%}
            {%- endif -%}
        {%- endif -%}
        {%- if model.resource_type == 'model' -%}
            {%- do query_tag_dict.update(
                materialized=model.config.materialized,
            ) -%}
        {%- endif -%}

        {%- if model.raw_code is not none and local_md5 -%}
            {%- do query_tag_dict.update({
                "raw_code_hash": local_md5(model.raw_code)
            }) -%}
        {%- endif -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_PROJECT_ID', False) -%}
        {%- do query_tag_dict.update(
            dbt_cloud_project_id=env_var('DBT_CLOUD_PROJECT_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_JOB_ID', False) -%}
        {%- do query_tag_dict.update(
            dbt_cloud_job_id=env_var('DBT_CLOUD_JOB_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_ID', False) -%}
        {%- do query_tag_dict.update(
            dbt_cloud_run_id=env_var('DBT_CLOUD_RUN_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON_CATEGORY', False) -%}
        {%- do query_tag_dict.update(
            dbt_cloud_run_reason_category=env_var('DBT_CLOUD_RUN_REASON_CATEGORY')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON', False) -%}
        {%- do query_tag_dict.update(
            dbt_cloud_run_reason=env_var('DBT_CLOUD_RUN_REASON')
        ) -%}
    {%- endif -%}

    {% if thread_id %}
        {%- do query_tag_dict.update(
            thread_id=thread_id
        ) -%}
    {% endif %}

    {% set query_tag_json = tojson(query_tag_dict) %}
    {{ log("Setting query_tag to '" ~ query_tag_json ~ "'. Will reset to '" ~ original_query_tag ~ "' after materialization.", info=false) }}
    {% do run_query("alter session set query_tag = '{}'".format(query_tag_json)) %}
    {{ return(original_query_tag)}}
{% endmacro %}

{% macro unset_query_tag(original_query_tag) -%}
    {% if original_query_tag %}
        {{ log("Resetting query_tag to '" ~ original_query_tag ~ "'.", info=false) }}
        {% do run_query("alter session set query_tag = '{}'".format(original_query_tag)) %}
    {% else %}
        {{ log("No original query_tag, unsetting parameter.", info=false) }}
        {% do run_query("alter session unset query_tag") %}
    {% endif %}
{% endmacro %}
