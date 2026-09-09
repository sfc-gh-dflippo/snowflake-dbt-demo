# DTSX Dataflow Analysis Guide

Reference for navigating DTSX XML files to extract SSIS dataflow information used during dbt test generation.

## Table of Contents

- [XML Namespaces](#xml-namespaces)
- [Finding Dataflow Tasks](#finding-dataflow-tasks)
- [Inside a Data Flow Task](#inside-a-data-flow-task)
- [Common Component Class IDs](#common-component-class-ids)
- [Extracting Column Information](#extracting-column-information)
- [Extracting Expressions](#extracting-expressions)
- [Tracing Data Flow Paths](#tracing-data-flow-paths)
- [SSIS Component Extraction Details](#ssis-component-extraction-details)
- [SSIS-to-dbt Layer Mapping](#ssis-to-dbt-layer-mapping)

---

## XML Namespaces

DTSX files use several XML namespaces. The most important:

- `DTS` -- `www.microsoft.com/SqlServer/Dts` (package metadata, executables, variables)
- `pipeline` -- `www.microsoft.com/SqlServer/Dts/Pipeline` (dataflow components)

## Finding Dataflow Tasks

```
DTS:Executable (root package)
  └─ DTS:Executables
       └─ DTS:Executable (task container or sequence container)
            └─ DTS:Executables
                 └─ DTS:Executable[@DTS:ExecutableType="Microsoft.Pipeline"]  ← Data Flow Task
```

Each Data Flow Task has a `DTS:ObjectName` attribute that typically matches the dbt project subfolder name.

## Inside a Data Flow Task

```
DTS:Executable[@DTS:ExecutableType="Microsoft.Pipeline"]
  └─ DTS:ObjectData
       └─ pipeline:Pipeline
            ├─ pipeline:components
            │    └─ pipeline:component (one per source/transform/destination)
            │         ├─ @componentClassID  ← identifies the component type
            │         ├─ @name              ← display name
            │         ├─ pipeline:properties
            │         │    └─ pipeline:property[@name="..."]  ← config properties
            │         ├─ pipeline:inputs
            │         │    └─ pipeline:input
            │         │         └─ pipeline:inputColumns
            │         │              └─ pipeline:inputColumn  ← input column refs
            │         └─ pipeline:outputs
            │              └─ pipeline:output
            │                   └─ pipeline:outputColumns
            │                        └─ pipeline:outputColumn  ← output column defs
            └─ pipeline:paths
                 └─ pipeline:path  ← data flow connections between components
                      ├─ @startId   ← output ID of source component
                      └─ @endId     ← input ID of target component
```

## Common Component Class IDs

| componentClassID | SSIS Component | What to Extract |
|---|---|---|
| `DTSAdapter.OLEDBSource` | OLE DB Source | Table/query name, output columns with data types |
| `DTSAdapter.OLEDBDestination` | OLE DB Destination | Target table name, column mappings |
| `DTSTransform.DerivedColumn` | Derived Column | Expression for each derived/replaced column |
| `DTSTransform.ConditionalSplit` | Conditional Split | Condition expression per output, default output |
| `DTSTransform.Lookup` | Lookup | Join columns, reference table, match columns |
| `DTSTransform.FuzzyLookup` | Fuzzy Lookup | Match columns, similarity threshold, reference table |
| `DTSTransform.ScriptComponent` | Script Component | Input/output columns (script logic is compiled, not in XML) |
| `DTSTransform.Aggregate` | Aggregate | Group-by columns, aggregate type per output column |
| `DTSTransform.Sort` | Sort | Sort columns, direction (ASC/DESC) |
| `DTSTransform.UnionAll` | Union All | Input-to-output column mapping |
| `DTSTransform.DataConvert` | Data Conversion | Source column, target type |
| `DTSAdapter.FlatFileSource` | Flat File Source | File connection, output columns |
| `DTSAdapter.FlatFileDestination` | Flat File Destination | File connection, column mappings |

## Extracting Column Information

Output columns have attributes for data type mapping:

```xml
<pipeline:outputColumn
    name="<ColumnName>"
    dataType="i4"           <!-- DT_I4 = 32-bit integer -->
    length="0"
    precision="0"
    scale="0"
    lineageId="..." />
```

Common `dataType` values: `i4` (int), `i8` (bigint), `wstr` (nvarchar), `str` (varchar), `r4` (float), `r8` (double), `dbTimeStamp` (datetime), `bool` (boolean), `date` (date).

## Extracting Expressions

Derived Column and Conditional Split expressions are in `pipeline:property` elements:

```xml
<!-- Derived Column expression -->
<pipeline:property name="Expression">[<ColumnA>] + " " + [<ColumnB>]</pipeline:property>
<pipeline:property name="FriendlyExpression">[<ColumnA>] + " " + [<ColumnB>]</pipeline:property>

<!-- Conditional Split condition -->
<pipeline:property name="Expression">[<Column>] == "<Value>"</pipeline:property>
<pipeline:property name="FriendlyExpression"><Column> == "<Value>"</pipeline:property>
```

SSIS expression syntax uses `==` for equality, `||` for OR, `&&` for AND, and square brackets `[]` for column references. Translate these to Snowflake SQL equivalents when designing test assertions.

## Tracing Data Flow Paths

The `pipeline:paths` section defines how data flows between components:

```xml
<pipeline:path startId="OLE DB Source.Outputs[OLE DB Source Output]"
               endId="Derived Column.Inputs[Derived Column Input]" />
```

Follow these paths to understand the order of transformations and which component feeds into which.

## SSIS Component Extraction Details

For each `pipeline:component` within a dataflow, identify the component type from `componentClassID` and extract relevant information:

- **Derived Column**: expressions in `pipeline:property[@name="Expression"]` or `pipeline:property[@name="FriendlyExpression"]`
- **Conditional Split**: condition expressions and output names
- **Lookup/Fuzzy Lookup**: join columns, reference table, match type
- **Script Component**: input/output column mappings (logic is in the script, infer from column relationships)
- **Aggregate**: grouping columns and aggregate functions
- **Sort**: sort columns and direction
- **Union All**: input-to-output column mappings
- **Data Conversion**: source/target types

Extract connection manager references for sources and destinations (table names, queries).

### Building a Component Flow Graph

Use `pipeline:path` elements to trace how data flows from source components through transforms to destination components. Each path's `startId` and `endId` attributes identify the output and input endpoints. Reconstruct the full pipeline graph to understand transformation order.

## SSIS-to-dbt Layer Mapping

Map SSIS pipeline components to dbt model layers:

| SSIS Component Type | dbt Layer | Naming Convention |
|---|---|---|
| OLE DB Source / Flat File Source | Staging | `stg_raw__<source_name>` |
| Derived Column, Conditional Split, Lookup, Aggregate, Sort, Script Component | Intermediate | `int_<transform_name>` |
| OLE DB Destination / Flat File Destination | Mart | Named after destination table |

Use this mapping to determine what each dbt model SHOULD do based on the SSIS logic:
- What columns should appear in the output
- What transformations should be applied (derived columns, conditional splits, lookups)
- What filtering/routing logic should apply
- What join conditions and match criteria should hold

### SSIS Data Types to Seed Values

When generating seed data, use DTSX data types to produce appropriate synthetic values:

| DTSX Type | Seed Value Format |
|---|---|
| `DT_WSTR` / `DT_STR` | String values |
| `DT_I4` / `DT_I8` | Integer values |
| `DT_R4` / `DT_R8` | Decimal values |
| `DT_DBTIMESTAMP` / `DT_DATE` | `YYYY-MM-DD` or `YYYY-MM-DD HH:MI:SS` |
| `DT_BOOL` | `true` / `false` |
