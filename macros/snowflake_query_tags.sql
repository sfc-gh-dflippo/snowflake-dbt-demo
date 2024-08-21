{% macro set_query_tag() -%}

    {# Get session level query tag #}
    {% set original_query_tag = get_current_query_tag() %}
    {% set original_query_tag_parsed = {} %}

    {% if original_query_tag %}
        {% if fromjson(original_query_tag) is mapping %}
            {% set original_query_tag_parsed = fromjson(original_query_tag) %}
        {% endif %}
    {% endif %}
    {%- set comment_dict = {} -%}

    {% do comment_dict.update(original_query_tag_parsed) %}

    {%- do comment_dict.update(
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
        {%- do comment_dict.update(
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

        {%- if flags.INVOCATION_COMMAND -%}
            {%- do comment_dict.update(
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
                {%- do comment_dict.update(
                    node_refs=refs | unique | list
                ) -%}
            {%- endif -%}
        {%- endif -%}
        {%- if model.resource_type == 'model' -%}
            {%- do comment_dict.update(
                materialized=model.config.materialized,
            ) -%}
        {%- endif -%}

        {%- if model.raw_code is not none and local_md5 -%}
            {%- do comment_dict.update({
                "raw_code_hash": local_md5(model.raw_code)
            }) -%}
        {%- endif -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_PROJECT_ID', False) -%}
        {%- do comment_dict.update(
            dbt_cloud_project_id=env_var('DBT_CLOUD_PROJECT_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_JOB_ID', False) -%}
        {%- do comment_dict.update(
            dbt_cloud_job_id=env_var('DBT_CLOUD_JOB_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_ID', False) -%}
        {%- do comment_dict.update(
            dbt_cloud_run_id=env_var('DBT_CLOUD_RUN_ID')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON_CATEGORY', False) -%}
        {%- do comment_dict.update(
            dbt_cloud_run_reason_category=env_var('DBT_CLOUD_RUN_REASON_CATEGORY')
        ) -%}
    {%- endif -%}

    {%- if env_var('DBT_CLOUD_RUN_REASON', False) -%}
        {%- do comment_dict.update(
            dbt_cloud_run_reason=env_var('DBT_CLOUD_RUN_REASON')
        ) -%}
    {%- endif -%}

    {% do return(dbt_snowflake_query_tags.set_query_tag(extra=comment_dict)) %}
{% endmacro %}

{% macro unset_query_tag(original_query_tag) -%}
    {% do return(dbt_snowflake_query_tags.unset_query_tag(original_query_tag)) %}
{% endmacro %}
