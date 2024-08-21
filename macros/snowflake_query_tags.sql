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
        {% else %}
            {%- do original_query_tag_parsed.update(original_query_tag=original_query_tag) -%}
        {% endif %}
    {% endif %}

    {# Get model config level query tag #}
    {% set config_query_tag = config.get('query_tag') %}
    {% set config_query_tag_parsed = {} %}
    {% if config_query_tag %}
        {% if fromjson(config_query_tag) is mapping %}
            {% set config_query_tag_parsed = fromjson(config_query_tag) %}
        {% else %}
            {%- do config_query_tag_parsed.update(config_query_tag=config_query_tag) -%}
        {% endif %}
    {% endif %}

    {% set query_tag_dict = {} %}
    {% do query_tag_dict.update(original_query_tag_parsed) %}
    {% do query_tag_dict.update(config_query_tag_parsed) %}

    {% set env_det = {} %}
    {%- do env_det.update(
        database=target.database,
        schema=target.schema
    ) -%}

    {% set run_det = {} %}
    {%- do run_det.update(
        full_refresh=flags.FULL_REFRESH,
        which=flags.WHICH
    ) -%}

    {%- if env_var('DBT_CLOUD_PROJECT_ID', False) -%}
        {%- do run_det.update(
            dbt_cloud_project_id=env_var('DBT_CLOUD_PROJECT_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_JOB_ID', False) -%}
        {%- do run_det.update(
            dbt_cloud_job_id=env_var('DBT_CLOUD_JOB_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_ID', False) -%}
        {%- do run_det.update(
            dbt_cloud_run_id=env_var('DBT_CLOUD_RUN_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON_CATEGORY', False) -%}
        {%- do run_det.update(
            dbt_cloud_run_reason_category=env_var('DBT_CLOUD_RUN_REASON_CATEGORY')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON', False) -%}
        {%- do run_det.update(
            dbt_cloud_run_reason=env_var('DBT_CLOUD_RUN_REASON')
        ) -%}
    {%- endif -%}

    {%- if flags.INVOCATION_COMMAND -%}
        {%- do run_det.update(
            invocation_command=flags.INVOCATION_COMMAND
        ) -%}
    {%- endif -%}

    {% if thread_id %}
        {%- do run_det.update(
            thread_id=thread_id
        ) -%}
    {% endif %}

    {%- do query_tag_dict.update(
        app='dbt',
        app_version=dbt_version,
        project_name=project_name,
        environment_name=target.name,
        environment_details=env_det,
        run_id=invocation_id,
        run_started_at=run_started_at.astimezone(modules.pytz.utc).isoformat(),
        run_details=run_det
    ) -%}

    {%- if model -%}
        {% set module_det = {} %}

        {%- do module_det.update(
            module_database=model.database,
            module_schema=model.schema,
            module_alias=model.alias,
            module_package_name=model.package_name,
            module_original_file_path=model.original_file_path,
            module_meta=model.config.meta
        ) -%}

        {% if model.resource_type == 'model' %}
            {%- do module_det.update(
                is_incremental=is_incremental()
            ) -%}
        {% endif %}

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
                {%- do module_det.update(
                    node_refs=refs | unique | list
                ) -%}
            {%- endif -%}
        {%- endif -%}
        {%- if model.resource_type == 'model' -%}
            {%- do module_det.update(
                materialized=model.config.materialized,
            ) -%}
        {%- endif -%}

        {%- if model.raw_code is not none and local_md5 -%}
            {%- do module_det.update({
                "raw_code_hash": local_md5(model.raw_code)
            }) -%}
        {%- endif -%}

        {%- do query_tag_dict.update(
            module_id=model.unique_id,
            module_name=model.name,
            module_type=model.resource_type,
            module_tags=model.tags,
            module_details=module_det
        ) -%}

    {%- endif -%}

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
