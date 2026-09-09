# Classification Logic (Deferred Reference)

## When to Load

Load this file at Step 3 (Classify Each Block) if you need the detailed classification pseudocode, confidence assessment, or output-type determination logic.

> **Canonical source:** The block-counting and tiering rules below mirror
> `../../references/block-tiering-spec.md`. That spec is the single source of truth shared with
> the `assess-sas-migration` CLI — keep this file in sync with it. In particular:
> **enumerate each DATA/PROC step inside a macro as its own block**, and **exclude DI Studio /
> DataFlow boilerplate** (macros named `etls_*`, `rcset`, `rcsetds`; content markers `etls_`,
> `perfinit`, `log4sas`, `armsubsys`, `sas data integration studio`) from both the block count
> and tiering.

---

## SQL-First Block Classification

```python
def classify_block_sql_first(block_content, block_type='DATA_STEP'):
    """
    SQL-FIRST classification. Returns: ('sql' | 'stored_proc' | 'pyspark', reason)
    PySpark via SCOS is LAST RESORT only.
    `block_type` is the parsed block kind (e.g. 'DATA_STEP', 'PROC_SQL') — used to
    scope the branch-count rule so PROC SQL CASE WHEN is not mistaken for procedural logic.
    """
    content_lower = block_content.lower()
    
    # === TIER 3: PySpark/SCOS (ONLY when SQL/SP truly cannot work) ===
    if 'declare hash' in content_lower:
        return ('pyspark', 'HASH objects - no SQL equivalent, use SCOS')
    
    if 'call execute' in content_lower:
        return ('pyspark', 'CALL EXECUTE - dynamic code generation, use SCOS')
    
    if ('do until' in content_lower or 'do while' in content_lower):
        if 'symput' in content_lower or content_lower.count('call ') > 2:
            return ('pyspark', 'DO loop with external state - use SCOS')
    
    # Statistical modeling (canonical list — keep in sync with block-tiering-spec.md)
    stats_procs = ['proc reg', 'proc glm', 'proc logistic', 'proc cluster',
                   'proc factor', 'proc phreg', 'proc lifetest', 'proc surveyselect',
                   'proc mixed', 'proc genmod', 'proc nlmixed']
    for proc in stats_procs:
        if proc in content_lower:
            return ('pyspark', f'Statistical modeling: {proc} - use SCOS')
    
    # === TIER 2: Stored Procedure ===
    if 'retain ' in content_lower and 'first.' in content_lower:
        if '= 0' in content_lower or '= .' in content_lower:
            return ('stored_proc', 'RETAIN with conditional reset - use SP')
    
    if ('first.' in content_lower or 'last.' in content_lower):
        if content_lower.count('output ') > 1:
            return ('stored_proc', 'FIRST./LAST. with multiple OUTPUT - use SP')
    
    if content_lower.count('output ') > 1 and 'output;' not in content_lower:
        return ('stored_proc', 'Multiple OUTPUT datasets - use SP')
    
    # Branch-count rule applies to DATA steps ONLY. A PROC SQL CASE WHEN is pure
    # SQL (Tier 1) however many WHEN clauses it has. See block-tiering-spec.md.
    if block_type == 'DATA_STEP' and (
            content_lower.count('if ') > 5 or content_lower.count('when ') > 5):
        return ('stored_proc', 'Complex branching (>5 IF/WHEN in DATA step) - use SP')
    
    # 3+ sequential DML operations -> orchestration + error handling
    if sum(1 for kw in ['delete ', 'insert ', 'update '] if kw in content_lower) >= 3:
        return ('stored_proc', '3+ sequential DML operations - use SP')
    
    # === TIER 1: SQL (Default - EVERYTHING ELSE) ===
    return ('sql', 'SQL-translatable with window functions/CTEs')


def determine_output_type(blocks, user_requested_notebook=False):
    """
    Determine output type. DEFAULT is ALWAYS .sql
    Returns: 'sql' | 'notebook'
    """
    if user_requested_notebook:
        return 'notebook'
    
    for block in blocks:
        # `block` carries its parsed type; pass it so the branch-count rule is
        # scoped to DATA steps.
        tier, _ = classify_block_sql_first(block.content, block.block_type)
        if tier == 'pyspark':
            return 'notebook'
    
    return 'sql'


def assess_confidence(block_content):
    """Assess translation confidence."""
    content_lower = block_content.lower()
    
    # LOW CONFIDENCE
    if content_lower.count('%macro') > 2:
        return ('low', 'Nested macros - complex resolution')
    if '%include' in content_lower and '&' in content_lower:
        return ('low', '%INCLUDE with dynamic path')
    # External DB engines (canonical union list — keep in sync with block-tiering-spec.md)
    if any(eng in content_lower for eng in
            ['sqlsvr', 'mssql', 'sql server', 'oracle', 'teradata',
             'odbc', 'oledb', 'db2', 'postgres', 'mysql', 'dsn=']):
        return ('low', 'External database engine reference')
    
    # MEDIUM CONFIDENCE
    if any(func in content_lower for func in ['intck', 'intnx', 'datepart']):
        return ('medium', 'Complex date manipulation - verify')
    if 'notsorted' in content_lower:
        return ('medium', 'BY-group with NOTSORTED')
    
    # HIGH CONFIDENCE
    return ('high', 'Standard pattern with direct mapping')
```

## File-Level Tier (strict "any-block" rule)

A file's overall tier is driven by its most demanding block — identical to
`determine_output_type` above and to the assessment CLI:

- **any** block is `pyspark` → file is **Tier 3** (emit a notebook)
- else **any** block is `stored_proc` → file is **Tier 2**
- else → file is **Tier 1** (pure SQL)

There are no proportion thresholds. Boilerplate blocks are excluded *before* this rule is
applied (see the canonical-source note above), so a stray scaffolding HASH does not promote a
whole generated file to Tier 3.

> **PROC SQL CASE WHEN is Tier 1.** A large `CASE WHEN ... END` in PROC SQL is pure Snowflake
> SQL, regardless of how many `WHEN` clauses it has. The ">5 IF/WHEN" Tier-2 rule fires only for
> **DATA-step** procedural branching (`IF/THEN/ELSE`, `SELECT/WHEN`) — never for PROC SQL.

