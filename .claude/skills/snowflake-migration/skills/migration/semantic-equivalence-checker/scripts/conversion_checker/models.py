"""Data models for the conversion checker."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Expression:
    field_name: str
    expression: str
    data_type: str | None = None


@dataclass
class Join:
    join_type: str  # NORMAL, MASTER OUTER, DETAIL OUTER
    condition: str
    tables: list[str] = field(default_factory=list)


@dataclass
class Lookup:
    table: str
    condition: str
    return_columns: list[str] = field(default_factory=list)
    sql_override: str | None = None


@dataclass
class Aggregator:
    group_by_ports: list[str] = field(default_factory=list)
    aggregate_expressions: list[Expression] = field(default_factory=list)


@dataclass
class RouterGroup:
    name: str
    condition: str


@dataclass
class InfaWorkflow:
    name: str
    pre_sql: list[str] = field(default_factory=list)
    post_sql: list[str] = field(default_factory=list)
    source_tables: list[str] = field(default_factory=list)
    target_table: str = ""
    all_targets: list[str] = field(default_factory=list)
    target_load_type: str = ""  # INSERT / UPDATE / DELETE+INSERT
    update_strategy: str | None = None  # DD_INSERT/DD_UPDATE/DD_DELETE/DD_REJECT
    columns_written: list[str] = field(default_factory=list)
    expressions: list[Expression] = field(default_factory=list)
    filters: list[str] = field(default_factory=list)
    joins: list[Join] = field(default_factory=list)
    lookups: list[Lookup] = field(default_factory=list)
    aggregators: list[Aggregator] = field(default_factory=list)
    router_groups: list[RouterGroup] = field(default_factory=list)
    sq_override: str | None = None  # first pipeline (backward compat)
    sq_overrides: list[str] = field(default_factory=list)  # all pipelines
    sq_joins: list[str] = field(default_factory=list)  # SQ User Defined Join
    sq_filters: list[str] = field(default_factory=list)  # SQ Source Filter
    update_override: str | None = None
    insert_override: str | None = None
    # P2/P3 detectors: presence flags for elements not yet fully parsed
    has_connectors: bool = False
    has_worklets: bool = False
    has_unhandled_transforms: list[str] = field(default_factory=list)  # e.g. ["Rank", "Union"]


@dataclass
class JoinClause:
    join_type: str  # INNER, LEFT, RIGHT, FULL
    table: str
    condition: str


@dataclass
class CTE:
    name: str
    sql: str


@dataclass
class DbtModel:
    name: str
    file_path: str
    materialization: str = ""  # table / incremental / view / ephemeral
    incremental_strategy: str | None = None
    pre_hooks: list[str] = field(default_factory=list)
    post_hooks: list[str] = field(default_factory=list)
    source_tables: list[str] = field(default_factory=list)
    target_table: str = ""
    columns_selected: list[str] = field(default_factory=list)
    where_clauses: list[str] = field(default_factory=list)
    join_clauses: list[JoinClause] = field(default_factory=list)
    ctes: list[CTE] = field(default_factory=list)
    raw_sql: str = ""


@dataclass
class SourceCheck:
    status: str
    infa_sources: list[str] = field(default_factory=list)
    dbt_sources: list[str] = field(default_factory=list)
    missing_in_dbt: list[str] = field(default_factory=list)
    extra_in_dbt: list[str] = field(default_factory=list)
    evidence: list[dict] = field(default_factory=list)


@dataclass
class TargetCheck:
    status: str
    infa_target: str = ""
    dbt_target: str = ""
    match: bool = False
    evidence: list[dict] = field(default_factory=list)


@dataclass
class StrategyCheck:
    status: str
    infa_strategy: str = ""
    dbt_strategy: str = ""
    match: bool = False
    evidence: list[dict] = field(default_factory=list)


@dataclass
class HookCheck:
    status: str
    infa_sql: list[str] = field(default_factory=list)
    dbt_sql: list[str] = field(default_factory=list)
    equivalent: bool = False
    evidence: list[dict] = field(default_factory=list)


@dataclass
class ColumnCheck:
    status: str
    missing_in_dbt: list[str] = field(default_factory=list)
    extra_in_dbt: list[str] = field(default_factory=list)
    evidence: list[dict] = field(default_factory=list)


@dataclass
class ColumnTransform:
    column: str
    status: str  # MATCH / DIFFERENT / MISSING_IN_DBT / MISSING_IN_INFA
    infa_expr: str = ""
    dbt_expr: str = ""
    evidence: list[dict] = field(default_factory=list)


@dataclass
class TransformCheck:
    status: str  # PASS / FAIL / PARTIAL
    matches: int = 0
    differences: int = 0
    missing: int = 0
    columns: list[ColumnTransform] = field(default_factory=list)
    evidence: list[dict] = field(default_factory=list)


@dataclass
class SemanticCheck:
    status: str
    confidence: str = ""  # high / medium / low
    divergences: list[dict] = field(default_factory=list)


@dataclass
class UnresolvedSection:
    section: str  # "pre_sql", "post_sql", "transform_logic"
    reason: str
    infa_sql: str = ""
    dbt_sql: str = ""


@dataclass
class PipelineCoverage:
    count: int = 1
    variants: list[str] = field(default_factory=list)  # e.g. ['TSS', 'AS', 'TSS-Split', 'AS-Split']


@dataclass
class CheckResult:
    workflow: str
    verdict: str = ""  # PASS / FAIL / PARTIAL
    xml_path: str = ""
    dbt_path: str = ""
    source_tables: SourceCheck | None = None
    target_table: TargetCheck | None = None
    load_strategy: StrategyCheck | None = None
    pre_hooks: HookCheck | None = None
    post_hooks: HookCheck | None = None
    column_list: ColumnCheck | None = None
    transform_logic: TransformCheck | None = None
    semantic_equivalence: SemanticCheck | None = None
    pipeline_coverage: PipelineCoverage | None = None
    sibling_context: SiblingContext | None = None
    unresolved: list[UnresolvedSection] = field(default_factory=list)


@dataclass
class SiblingModel:
    name: str
    file_path: str
    materialization: str = ""
    pre_hooks: list[str] = field(default_factory=list)
    post_hooks: list[str] = field(default_factory=list)
    refs: list[str] = field(default_factory=list)
    columns_selected: list[str] = field(default_factory=list)


@dataclass
class SiblingContext:
    primary_model: str = ""
    siblings: list[SiblingModel] = field(default_factory=list)
    upstream_columns: dict[str, list[str]] = field(default_factory=dict)
    variables: dict[str, str] = field(default_factory=dict)


@dataclass
class Evidence:
    """Line number evidence for a claim."""
    file: str = ""
    line: int = 0
    text: str = ""
