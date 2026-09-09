"""Parse Informatica workflow XML into InfaWorkflow dataclass.

Extracts all logic-bearing elements: Source Qualifier SQL, Pre/Post SQL,
Lookup overrides, Expression transforms, Filter conditions, Joiner conditions,
target load type, and session-level overrides (Update Override, Insert SQL).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .models import Aggregator, Expression, InfaWorkflow, Join, Lookup, RouterGroup


# ──────────────────────────────────────────────────────────────
# Helpers (adapted from xml_truth.py)
# ──────────────────────────────────────────────────────────────

def _attr(elem: ET.Element, name: str, default: str = "") -> str:
    return (elem.get(name) or default).strip()


def _tableattrs(elem: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for ta in elem.findall("TABLEATTRIBUTE"):
        k = _attr(ta, "NAME")
        v = _attr(ta, "VALUE")
        if k:
            result[k] = v
    return result


def _session_instance_attrs(elem: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for a in elem.findall("ATTRIBUTE"):
        k = _attr(a, "NAME")
        v = _attr(a, "VALUE")
        if k:
            result[k] = v
    return result


def decode_informatica_sql(raw: str) -> str:
    """Decode Informatica's XML-encoded SQL (&#xD;&#xA; → newlines, etc.)."""
    if not raw:
        return ""
    text = raw.replace("&#xD;&#xA;", "\n").replace("&#xA;", "\n").replace("&#xD;", "\n")
    text = text.replace("&apos;", "'").replace("&quot;", '"')
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()


def _normalize_table(name: str) -> str:
    """Strip DB prefix, return uppercase table name."""
    parts = name.split(".")
    return parts[-1].upper().strip()


# ──────────────────────────────────────────────────────────────
# Extraction from MAPPING element
# ──────────────────────────────────────────────────────────────

def _extract_sources(mapping: ET.Element) -> list[str]:
    """Extract source table names from SOURCE instances."""
    sources = []
    for inst in mapping.findall("INSTANCE"):
        if _attr(inst, "TYPE") == "SOURCE":
            name = _attr(inst, "TRANSFORMATION_NAME")
            if name:
                sources.append(_normalize_table(name))
    return sorted(set(sources))


def _extract_target(mapping: ET.Element) -> tuple[str, list[str], list[str]]:
    """Extract primary target table, all targets, and column names from TARGET instances."""
    all_targets: list[str] = []
    for inst in mapping.findall("INSTANCE"):
        if _attr(inst, "TYPE") == "TARGET":
            name = _attr(inst, "TRANSFORMATION_NAME")
            if name:
                all_targets.append(_normalize_table(name))

    target = all_targets[0] if all_targets else ""
    columns: list[str] = []
    return target, all_targets, columns


def _extract_target_columns(folder: ET.Element, target_name: str) -> list[str]:
    """Get column names from TARGET definition element."""
    for tgt in folder.findall("TARGET"):
        name = _attr(tgt, "NAME")
        if _normalize_table(name) == _normalize_table(target_name):
            return [_attr(f, "NAME").upper() for f in tgt.findall("TARGETFIELD") if _attr(f, "NAME")]
    return []


def _extract_expressions(mapping: ET.Element) -> list[Expression]:
    """Extract Expression transformation fields."""
    expressions = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Expression":
            continue
        for tf in t.findall("TRANSFORMFIELD"):
            expr = _attr(tf, "EXPRESSION")
            if expr and expr != _attr(tf, "NAME"):
                expressions.append(Expression(
                    field_name=_attr(tf, "NAME"),
                    expression=expr,
                    data_type=_attr(tf, "DATATYPE") or None,
                ))
    return expressions


def _extract_filters(mapping: ET.Element) -> list[str]:
    """Extract Filter transformation conditions."""
    filters = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Filter":
            continue
        for tf in t.findall("TRANSFORMFIELD"):
            expr = _attr(tf, "EXPRESSION")
            if expr and _attr(tf, "NAME").upper() == "FILTERCONDITION":
                filters.append(expr)
        # Also check TABLEATTRIBUTE for filter condition
        attrs = _tableattrs(t)
        if "Filter Condition" in attrs and attrs["Filter Condition"]:
            filters.append(attrs["Filter Condition"])
    return filters


def _extract_joins(mapping: ET.Element) -> list[Join]:
    """Extract Joiner transformation conditions."""
    joins = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Joiner":
            continue
        attrs = _tableattrs(t)
        join_type = attrs.get("Join Type", "NORMAL")
        condition = attrs.get("Join Condition", "")
        if condition:
            joins.append(Join(join_type=join_type, condition=condition))
    return joins


def _extract_lookups(mapping: ET.Element) -> list[Lookup]:
    """Extract Lookup transformation details."""
    lookups = []
    for t in mapping.findall("TRANSFORMATION"):
        t_type = _attr(t, "TYPE")
        if t_type not in ("Lookup Procedure", "Lookup"):
            continue
        attrs = _tableattrs(t)
        table_name = _attr(t, "NAME")
        # The actual lookup table is often in the associated INSTANCE
        # or can be derived from the transformation name
        condition = attrs.get("Lookup condition", "") or attrs.get("Lookup Condition", "")
        sql_override = decode_informatica_sql(attrs.get("Lookup Sql Override", ""))
        return_cols = [
            _attr(tf, "NAME")
            for tf in t.findall("TRANSFORMFIELD")
            if _attr(tf, "PORTTYPE", "").upper() in ("OUTPUT", "INPUT/OUTPUT")
        ]
        lookups.append(Lookup(
            table=table_name,
            condition=condition,
            return_columns=return_cols,
            sql_override=sql_override or None,
        ))
    return lookups


def _extract_sq_override(mapping: ET.Element) -> str | None:
    """Extract first Source Qualifier SQL override (backward compat)."""
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Source Qualifier":
            continue
        attrs = _tableattrs(t)
        sql = decode_informatica_sql(attrs.get("Sql Query", ""))
        if sql:
            return sql
    return None


def _extract_all_sq_overrides(mapping: ET.Element) -> list[str]:
    """Extract ALL Source Qualifier SQL overrides from a mapping."""
    overrides = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Source Qualifier":
            continue
        attrs = _tableattrs(t)
        sql = decode_informatica_sql(attrs.get("Sql Query", ""))
        if sql:
            overrides.append(sql)
    return overrides


def _extract_sq_joins_and_filters(mapping: ET.Element) -> tuple[list[str], list[str]]:
    """Extract Source Qualifier User Defined Join and Source Filter."""
    sq_joins: list[str] = []
    sq_filters: list[str] = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Source Qualifier":
            continue
        attrs = _tableattrs(t)
        join = decode_informatica_sql(attrs.get("User Defined Join", ""))
        if join:
            sq_joins.append(join)
        filt = decode_informatica_sql(attrs.get("Source Filter", ""))
        if filt:
            sq_filters.append(filt)
    return sq_joins, sq_filters


def _extract_update_strategy(mapping: ET.Element) -> str | None:
    """Extract Update Strategy transformation expression (DD_INSERT/DD_UPDATE/etc)."""
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Update Strategy":
            continue
        for tf in t.findall("TRANSFORMFIELD"):
            expr = _attr(tf, "EXPRESSION")
            if expr and "DD_" in expr.upper():
                return expr
    return None


def _extract_aggregators(mapping: ET.Element) -> list[Aggregator]:
    """Extract Aggregator transformation GROUP BY ports and aggregate expressions."""
    aggregators = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Aggregator":
            continue
        group_by: list[str] = []
        agg_exprs: list[Expression] = []
        for tf in t.findall("TRANSFORMFIELD"):
            port_type = _attr(tf, "PORTTYPE", "").upper()
            expr = _attr(tf, "EXPRESSION")
            name = _attr(tf, "NAME")
            group_flag = _attr(tf, "GROUP", "").upper()
            if group_flag == "YES" or "GROUP BY" in port_type:
                group_by.append(name)
            elif expr and expr != name:
                agg_exprs.append(Expression(field_name=name, expression=expr))
        if group_by or agg_exprs:
            aggregators.append(Aggregator(group_by_ports=group_by, aggregate_expressions=agg_exprs))
    return aggregators


def _extract_routers(mapping: ET.Element) -> list[RouterGroup]:
    """Extract Router transformation group conditions."""
    groups = []
    for t in mapping.findall("TRANSFORMATION"):
        if _attr(t, "TYPE") != "Router":
            continue
        attrs = _tableattrs(t)
        # Router groups are stored in TABLEATTRIBUTE with names like "Router Group_N"
        for key, val in attrs.items():
            if "group" in key.lower() and val:
                groups.append(RouterGroup(name=key, condition=val))
        # Also check TRANSFORMFIELD for group filter expressions
        for tf in t.findall("TRANSFORMFIELD"):
            expr = _attr(tf, "EXPRESSION")
            name = _attr(tf, "NAME")
            if expr and "GROUP_FILTER" in name.upper():
                groups.append(RouterGroup(name=name, condition=expr))
    return groups


def _detect_unhandled_transforms(mapping: ET.Element) -> list[str]:
    """Detect presence of transform types not fully parsed (P2/P3 elements)."""
    unhandled_types = {"Rank", "Sorter", "Union", "Sequence Generator",
                       "Stored Procedure", "External Procedure", "Custom"}
    found = []
    for t in mapping.findall("TRANSFORMATION"):
        t_type = _attr(t, "TYPE")
        if t_type in unhandled_types and t_type not in found:
            found.append(t_type)
    return found


def _detect_connectors(mapping: ET.Element) -> bool:
    """Detect if mapping has CONNECTOR elements (data-flow graph)."""
    return len(mapping.findall("CONNECTOR")) > 0


# ──────────────────────────────────────────────────────────────
# Extraction from SESSION element
# ──────────────────────────────────────────────────────────────

def _extract_session_overrides(session: ET.Element) -> dict[str, str | list[str]]:
    """Extract pre/post SQL, update override, insert SQL from session."""
    pre_sql: list[str] = []
    post_sql: list[str] = []
    sq_overrides: list[str] = []
    update_override: str = ""
    insert_override: str = ""
    load_type: str = ""

    for si in session.findall("SESSTRANSFORMATIONINST"):
        si_type = _attr(si, "TRANSFORMATIONTYPE")

        attrs = _session_instance_attrs(si)

        # Collect Pre/Post SQL from both Target Definition and Source Qualifier
        if si_type in ("Target Definition", "Source Qualifier"):
            raw_pre = decode_informatica_sql(attrs.get("Pre SQL", ""))
            if raw_pre:
                pre_sql.extend(s.strip() for s in raw_pre.split(";") if s.strip())

            raw_post = decode_informatica_sql(attrs.get("Post SQL", ""))
            if raw_post:
                post_sql.extend(s.strip() for s in raw_post.split(";") if s.strip())

        # Session-level SQ override (takes precedence over mapping-level)
        if si_type == "Source Qualifier":
            raw_sq = decode_informatica_sql(attrs.get("Sql Query", ""))
            if raw_sq:
                sq_overrides.append(raw_sq)

        if si_type != "Target Definition":
            continue

        raw_update = decode_informatica_sql(attrs.get("Update Override", ""))
        if raw_update:
            update_override = raw_update

        raw_insert = decode_informatica_sql(attrs.get("Insert SQL", ""))
        if raw_insert:
            insert_override = raw_insert

        # Target load type from CONFIGREFERENCE or session attributes
        target_load = attrs.get("Target Load Type", "") or attrs.get("target load type", "")
        if target_load:
            load_type = target_load

    # Also check session-level CONFIGREFERENCE for load type
    for cfg in session.findall(".//CONFIGREFERENCE"):
        for cfg_attr in cfg.findall("ATTRIBUTE"):
            if _attr(cfg_attr, "NAME") == "Target Load Type":
                lt = _attr(cfg_attr, "VALUE")
                if lt:
                    load_type = lt

    return {
        "pre_sql": pre_sql,
        "post_sql": post_sql,
        "sq_overrides": sq_overrides,
        "update_override": update_override,
        "insert_override": insert_override,
        "load_type": load_type,
    }


def _infer_load_type(session_load: str, update_override: str, insert_override: str,
                     update_strategy: str | None = None) -> str:
    """Map Informatica load type to normalized form."""
    # Update Strategy transform takes precedence if present
    if update_strategy:
        us_upper = update_strategy.upper()
        if "DD_UPDATE" in us_upper and "DD_INSERT" in us_upper:
            return "UPSERT"
        if "DD_UPDATE" in us_upper:
            return "UPDATE"
        if "DD_DELETE" in us_upper:
            return "DELETE+INSERT"

    lt = session_load.upper().strip()
    if "INSERT" in lt and "UPDATE" in lt:
        return "UPSERT"
    if "DELETE" in lt or "TRUNCATE" in lt:
        return "DELETE+INSERT"
    if update_override:
        return "UPDATE"
    if "UPDATE" in lt:
        return "UPDATE"
    return "INSERT"


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────

def parse_infa_xml(xml_path: Path, workflow_name: str | None = None) -> InfaWorkflow | None:
    """Parse an INFA workflow XML file and return an InfaWorkflow dataclass.

    If workflow_name is provided, returns that specific workflow.
    Otherwise returns the first workflow found.
    Returns None if the XML cannot be parsed or contains no workflow.
    """
    workflows = parse_infa_xml_all(xml_path)
    if not workflows:
        return None
    if workflow_name:
        for wf in workflows:
            if wf.name.upper() == workflow_name.upper():
                return wf
    return workflows[0]


def parse_infa_xml_all(xml_path: Path) -> list[InfaWorkflow]:
    """Parse an INFA workflow XML file and return ALL workflows found."""
    try:
        tree = ET.parse(str(xml_path))
    except ET.ParseError:
        try:
            content = xml_path.read_bytes()
            root = ET.fromstring(content)
            tree = ET.ElementTree(root)
        except ET.ParseError:
            return []

    root = tree.getroot()
    results: list[InfaWorkflow] = []

    for repo in root.findall("REPOSITORY"):
        for folder in repo.findall("FOLDER"):
            # Index mappings
            mappings: dict[str, ET.Element] = {}
            for m in folder.findall("MAPPING"):
                m_name = _attr(m, "NAME")
                if m_name:
                    mappings[m_name] = m

            # Detect worklets
            has_worklets = len(folder.findall(".//WORKLET")) > 0 or len(
                [t for t in folder.findall("WORKFLOW//TASKINSTANCE")
                 if _attr(t, "TASKTYPE") == "Worklet"]) > 0

            for workflow in folder.findall("WORKFLOW"):
                wf_name = _attr(workflow, "NAME")
                if not wf_name:
                    continue

                # Also detect worklets within workflow
                wf_has_worklets = has_worklets or any(
                    _attr(ti, "TASKTYPE") == "Worklet"
                    for ti in workflow.findall("TASKINSTANCE")
                )

                # Collect from all sessions in this workflow
                all_sources: list[str] = []
                all_targets: list[str] = []
                target = ""
                columns: list[str] = []
                expressions: list[Expression] = []
                filters: list[str] = []
                joins: list[Join] = []
                lookups: list[Lookup] = []
                aggregators: list[Aggregator] = []
                router_groups: list[RouterGroup] = []
                sq_override: str | None = None
                sq_overrides: list[str] = []
                sq_joins: list[str] = []
                sq_filters: list[str] = []
                pre_sql: list[str] = []
                post_sql: list[str] = []
                update_override: str = ""
                insert_override: str = ""
                load_type: str = ""
                update_strategy: str | None = None
                has_connectors: bool = False
                unhandled_transforms: list[str] = []

                for session in workflow.findall("SESSION"):
                    mapping_name = _attr(session, "MAPPINGNAME")
                    mapping = mappings.get(mapping_name)

                    if mapping is not None:
                        all_sources.extend(_extract_sources(mapping))
                        t, targets, cols = _extract_target(mapping)
                        all_targets.extend(targets)
                        if t and not target:
                            target = t
                        if not columns:
                            columns = _extract_target_columns(folder, t) if t else []
                        expressions.extend(_extract_expressions(mapping))
                        filters.extend(_extract_filters(mapping))
                        joins.extend(_extract_joins(mapping))
                        lookups.extend(_extract_lookups(mapping))
                        aggregators.extend(_extract_aggregators(mapping))
                        router_groups.extend(_extract_routers(mapping))
                        # SQ overrides, joins, filters
                        sq_overrides.extend(_extract_all_sq_overrides(mapping))
                        if not sq_override:
                            sq_override = sq_overrides[0] if sq_overrides else None
                        m_sq_joins, m_sq_filters = _extract_sq_joins_and_filters(mapping)
                        sq_joins.extend(m_sq_joins)
                        sq_filters.extend(m_sq_filters)
                        # Update Strategy
                        us = _extract_update_strategy(mapping)
                        if us and not update_strategy:
                            update_strategy = us
                        # P2/P3 detectors
                        if not has_connectors:
                            has_connectors = _detect_connectors(mapping)
                        unhandled_transforms.extend(_detect_unhandled_transforms(mapping))

                    # Session-level overrides (take precedence over mapping-level)
                    overrides = _extract_session_overrides(session)
                    pre_sql.extend(overrides["pre_sql"])
                    post_sql.extend(overrides["post_sql"])
                    # Session-level SQ overrides override mapping-level
                    if overrides.get("sq_overrides"):
                        sq_overrides.extend(overrides["sq_overrides"])
                    if overrides["update_override"] and not update_override:
                        update_override = overrides["update_override"]
                    if overrides["insert_override"] and not insert_override:
                        insert_override = overrides["insert_override"]
                    if overrides["load_type"] and not load_type:
                        load_type = overrides["load_type"]

                results.append(InfaWorkflow(
                    name=wf_name,
                    pre_sql=pre_sql,
                    post_sql=post_sql,
                    source_tables=sorted(set(all_sources)),
                    target_table=target,
                    all_targets=sorted(set(all_targets)),
                    target_load_type=_infer_load_type(load_type, update_override, insert_override, update_strategy),
                    update_strategy=update_strategy,
                    columns_written=columns,
                    expressions=expressions,
                    filters=filters,
                    joins=joins,
                    lookups=lookups,
                    aggregators=aggregators,
                    router_groups=router_groups,
                    sq_override=sq_override,
                    sq_overrides=sq_overrides,
                    sq_joins=sq_joins,
                    sq_filters=sq_filters,
                    update_override=update_override or None,
                    insert_override=insert_override or None,
                    has_connectors=has_connectors,
                    has_worklets=wf_has_worklets,
                    has_unhandled_transforms=sorted(set(unhandled_transforms)),
                ))

    return results
