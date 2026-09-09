# Platform Profile: SSIS

## Identity
- platform_id: ssis
- platform_name: "SSIS (SQL Server Integration Services)"
- source_file_extension: .dtsx
- source_file_label: "DTSX file"
- source_file_format: XML

## Source of Truth
- source_description: >
    The DTSX file contains the complete SSIS package definition in XML format,
    including control flow tasks, data flow pipelines, variables, precedence
    constraints, event handlers, and connection managers.
- assertion_derivation: >
    Derive test assertions from the DTSX control flow and dataflow logic,
    NOT from the converted Snowflake SQL. The DTSX is the source of truth.
- traceability_format: "-- (Trace: DTSX {source} → {logic} → {expected})"

## Guides
- orchestration_guide: control-flow-guide.md
- transformation_guide: dataflow-guide.md
- element_types: element-types.md
- ewi_directory: ewi/

## Dead Code Stripping
- strip_script: strip_dead_code.py
- strip_description: "Strip ScriptTask C#/XML boilerplate from SSIS0004 blocks"

## Element Classification
- disabled_marker: 'Disabled="True"'
- disabled_reason: "disabled-in-source"
- pipeline_type: "Microsoft.Pipeline"
- external_dep_types:
  - Microsoft.SendMailTask
  - Microsoft.FileSystemTask
  - Microsoft.FtpTask
  - Microsoft.ExecuteProcess

## Source-Specific Vocabulary
- orchestration_term: "control flow"
- transformation_term: "data flow"
- unit_term: "SSIS package"
- task_term: "task"
- container_term: "container"
- variable_binding: "DTS:Variable"
- sql_source_attribute: "SqlStatementSource"
