# Platform Profile: Informatica

## Identity
- platform_id: informatica
- platform_name: "Informatica PowerCenter"
- source_file_extension: .xml
- source_file_label: "Informatica XML export"
- source_file_format: XML

## Source of Truth
- source_description: >
    The Informatica XML export contains workflow, session, and mapping
    definitions including source/target definitions, transformations,
    and expression logic.
- assertion_derivation: >
    Derive test assertions from the Informatica mapping and transformation
    logic, NOT from the converted Snowflake SQL.
- traceability_format: "-- (Trace: Informatica {source} → {logic} → {expected})"

## Guides
- orchestration_guide: workflow-guide.md
- transformation_guide: mapping-guide.md
- element_types: element-types.md
- ewi_directory: ewi/

## Dead Code Stripping
- strip_script: null
- strip_description: null

## Element Classification
- disabled_marker: 'ENABLED="NO"'
- disabled_reason: "disabled-in-source"
- pipeline_type: null
- external_dep_types:
  - Email
  - Command
  - Timer
  - Control

## Source-Specific Vocabulary
- orchestration_term: "workflow"
- transformation_term: "mapping"
- unit_term: "Informatica workflow"
- task_term: "session"
- container_term: "worklet"
- variable_binding: "$$variable"
- sql_source_attribute: "Sql Query"
