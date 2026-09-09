# SAS Dependency Mermaid Diagrams

## When to Load

Load when user requests:
- Dependency diagram / visualization
- Data flow analysis
- Script interaction mapping
- Codebase structure overview

---

## Diagram Types

### 1. Script-Level Dependency Diagram

Shows how SAS scripts interact through shared datasets:

```mermaid
flowchart TD
    subgraph "01_extract.sas"
        E1["DATA raw_data<br/>SET source_table"]
        E2["DATA cleaned_data<br/>SET raw_data"]
    end
    
    subgraph "02_transform.sas"
        T1["DATA enriched_data<br/>MERGE cleaned_data ref_table"]
        T2["PROC SQL: summary_data<br/>FROM enriched_data"]
    end
    
    subgraph "03_load.sas"
        L1["DATA final_output<br/>SET summary_data"]
    end
    
    source_table[(source_table)] --> E1
    ref_table[(ref_table)] --> T1
    E1 --> E2
    E2 --> T1
    T1 --> T2
    T2 --> L1
    L1 --> final_output[(final_output)]
```

### 2. Block-Level Flow (Single Script)

Shows DATA steps and PROCs within one script:

```mermaid
flowchart TB
    subgraph "process_data.sas"
        direction TB
        B1["1. DATA step: temp1<br/>• Input: raw<br/>• Transforms: filter, calc"]
        B2["2. PROC SORT<br/>• BY: customer_id"]
        B3["3. DATA step: temp2<br/>• MERGE: temp1 + lookup<br/>• BY: customer_id"]
        B4["4. PROC SQL: output<br/>• Aggregation<br/>• GROUP BY region"]
    end
    
    raw[(raw)] --> B1
    lookup[(lookup)] --> B3
    B1 --> B2 --> B3 --> B4
    B4 --> output[(output)]
```

### 3. Macro Dependency Diagram

Shows macro calls and dependencies:

```mermaid
flowchart TD
    subgraph "Macros"
        M1["%MACRO process_month"]
        M2["%MACRO calc_metrics"]
        M3["%MACRO export_results"]
    end
    
    subgraph "Main Script"
        S1["Set parameters<br/>%LET year=2024"]
        S2["%process_month(jan)"]
        S3["%process_month(feb)"]
        S4["%export_results"]
    end
    
    M1 --> M2
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> M3
```

---

## Generation Rules

### Node Naming Convention

| Block Type | Node Format |
|------------|-------------|
| DATA step | `"DATA: output_table<br/>SET: input_table"` |
| PROC SQL | `"PROC SQL: table_name<br/>FROM: source"` |
| PROC SORT | `"PROC SORT<br/>DATA=input OUT=output<br/>BY: vars"` |
| PROC MEANS | `"PROC MEANS<br/>DATA=input<br/>OUTPUT: stats"` |
| Macro | `"%MACRO name(params)"` |
| Macro call | `"%macro_name(args)"` |

### Edge Rules

1. **Data dependency**: Input table → Processing block
2. **Output flow**: Processing block → Output table
3. **Sequential**: Block N → Block N+1 (if no explicit dependency)
4. **Macro calls**: Calling block → Macro definition

### Subgraph Organization

```mermaid
flowchart TD
    subgraph "script_name.sas"
        direction TB
        %% Blocks go here
    end
    
    %% External tables as cylinders
    external_input[(external_input)]
    external_output[(external_output)]
```

---

## Extracting Dependencies from SAS Code

### DATA Step Dependencies

```sas
DATA output_table;
  SET input_table1 input_table2;    /* Inputs */
  MERGE table_a table_b;            /* Also inputs */
  BY key_var;
RUN;
```

**Extract:**
- Outputs: `output_table`
- Inputs: `input_table1`, `input_table2`, `table_a`, `table_b`
- BY vars: `key_var`

### PROC SQL Dependencies

```sas
PROC SQL;
  CREATE TABLE output_sql AS
  SELECT a.*, b.field
  FROM table_a a
  LEFT JOIN table_b b ON a.key = b.key;
QUIT;
```

**Extract:**
- Output: `output_sql`
- Inputs: `table_a`, `table_b`

### Macro Dependencies

```sas
%MACRO process(input=, output=);
  DATA &output;
    SET &input;
  RUN;
%MEND;

%process(input=raw_data, output=processed_data);
```

**Extract:**
- Macro: `process` with params `input`, `output`
- Call resolves to: input=`raw_data`, output=`processed_data`

---

## Complex Example

**Input SAS files:**

```
project/
├── 01_extract.sas       # Extracts from source
├── 02_transform.sas     # Cleans and enriches
├── 03_aggregate.sas     # Creates summaries
├── macros/
│   ├── common_macros.sas
│   └── report_macros.sas
└── 04_report.sas        # Generates final output
```

**Generated Mermaid:**

```mermaid
flowchart TD
    subgraph "macros/common_macros.sas"
        M1["%MACRO clean_data"]
        M2["%MACRO validate"]
    end
    
    subgraph "macros/report_macros.sas"
        M3["%MACRO format_report"]
    end
    
    subgraph "01_extract.sas"
        E1["DATA raw_extract<br/>SET source_db.transactions"]
    end
    
    subgraph "02_transform.sas"
        T1["%clean_data(raw_extract)"]
        T2["DATA enriched<br/>MERGE cleaned lookup"]
    end
    
    subgraph "03_aggregate.sas"
        A1["PROC SQL: daily_summary<br/>FROM enriched<br/>GROUP BY date"]
        A2["PROC SQL: monthly_summary<br/>FROM daily_summary"]
    end
    
    subgraph "04_report.sas"
        R1["%format_report(monthly_summary)"]
        R2["DATA final_report<br/>SET formatted_data"]
    end
    
    source_db.transactions[(source_db.transactions)] --> E1
    lookup[(lookup)] --> T2
    
    E1 --> T1
    M1 -.-> T1
    T1 --> T2
    T2 --> A1
    A1 --> A2
    A2 --> R1
    M3 -.-> R1
    R1 --> R2
    R2 --> final_report[(final_report)]
    
    style M1 fill:#f9f,stroke:#333
    style M2 fill:#f9f,stroke:#333
    style M3 fill:#f9f,stroke:#333
```

---

## Presentation Tips

1. **Start simple**: Show high-level script dependencies first
2. **Drill down**: Offer to expand individual scripts
3. **Highlight complexity**: Use colors for complex blocks (RETAIN, ARRAY)
4. **Mark external**: Use cylinder shapes `[( )]` for external tables
5. **Show macros**: Use dotted lines `-..->` for macro dependencies

---

## Color Coding (Optional)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff'}}}%%
flowchart TD
    classDef dataStep fill:#b3d9ff,stroke:#0066cc
    classDef procSql fill:#c2f0c2,stroke:#009900
    classDef procSort fill:#ffffb3,stroke:#999900
    classDef macro fill:#ffb3ff,stroke:#990099
    classDef external fill:#f0f0f0,stroke:#666666
    
    D1[DATA step]:::dataStep
    P1[PROC SQL]:::procSql
    S1[PROC SORT]:::procSort
    M1[%MACRO]:::macro
    E1[(External)]:::external
```

| Color | Meaning |
|-------|---------|
| Blue | DATA step |
| Green | PROC SQL |
| Yellow | PROC SORT/MEANS/FREQ |
| Pink | Macro |
| Gray | External table |
