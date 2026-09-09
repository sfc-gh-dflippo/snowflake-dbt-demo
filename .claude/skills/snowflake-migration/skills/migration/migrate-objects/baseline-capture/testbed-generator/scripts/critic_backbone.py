"""Deterministic backbone (layer ①) for the enrichment critics.

Runs cheap, 100%-reproducible checks per enrichment entry and classifies each into:
  fail        -> hard REJECT (guaranteed-true citation); skips the LLM residue.
  accept_skip -> boundary rule (declared-enum wins / declared-FK duplicate); no residue needed.
  flag        -> semantically-unsupported-but-in-range; routed to the residue as a mode-(b) question.
  pass        -> existence/grounding OK; residue judges the semantic bit.
This module makes ZERO model calls. It holds the value + structural entry checks, the run_backbone
dispatch over an envelope, and build_critique_request (the pass/flag entries handed to the residue).
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field

from critic_index import ObjectIndex, canon_owner, canon_table
from critic_normalize import literal_grounded_normalized, normalize


class CheckStatus(enum.StrEnum):
    # One source of truth for the backbone verdict a check carries; compared across module
    # boundaries (run_pipeline reads FAIL, build_critique_request reads PASS/FLAG), so a bare
    # literal here would let a typo silently route a check to the wrong gate branch.
    FAIL = "fail"
    ACCEPT_SKIP = "accept_skip"
    FLAG = "flag"
    PASS = "pass"


@dataclass
class EntryCheck:
    kind: str
    container: str
    identity: dict
    status: CheckStatus
    citation: str = ""
    anchors: dict = field(default_factory=dict)


def _cell(entry: dict) -> tuple:
    return entry.get("table"), entry.get("column")


def _in_unit_range(v: object) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 0.0 <= v <= 1.0


def _wire_array(value: object) -> list | None:
    # None for a value the wire contract declares as an array but that arrived as something else. A bare
    # string is the case that matters: truthy and iterable, so an unguarded loop grades its characters as
    # literals and "GOLD" is accepted as four of them. Falsy stays [] so an absent field reads as absent.
    if not value:
        return []
    return value if isinstance(value, list) else None


def _fail(name: str, ident: dict, msg: str) -> list[EntryCheck]:
    # Each structural array is its own kind and container, so the FAIL shape lives in exactly one place.
    return [EntryCheck(name, name, ident, CheckStatus.FAIL, msg)]


def _resolved_key(index: ObjectIndex, table: str | None) -> str:
    # Identity key for a table name: its owner when the name resolves to exactly one, else the name as
    # written. Two names are then equal only when they provably denote the same table -- which is what a
    # guaranteed-true FAIL needs. canon_table would instead collapse SALES.ORDERS and STAGING.ORDERS.
    owners = index.table_owners(table)
    return owners[0] if len(owners) == 1 else canon_owner(table)


def _table_matches(index: ObjectIndex, a: str | None, b: str | None) -> bool:
    # Deliberately looser than _resolved_key equality: a declared FK's referenced table is written at
    # inconsistent qualification depth across artifacts, so require owner equality only when both names
    # resolve uniquely. Used solely where a match SKIPS review, never where it hard-blocks.
    ka, kb = index.table_owners(a), index.table_owners(b)
    if len(ka) == 1 and len(kb) == 1:
        return ka[0] == kb[0]
    return canon_table(a) == canon_table(b)


def _ambiguity_check(kind: str, container: str, ident: dict, index: ObjectIndex,
                     *tables) -> list[EntryCheck]:
    # An unresolvable bare name yields no column facts, so every existence/type check below it would
    # read as a guaranteed-true FAIL on a column that does exist in each candidate. The ambiguity
    # itself is deterministic, so hand it to the residue with the candidate owners attached instead.
    unresolved = [t for t in dict.fromkeys(tables) if index.ambiguous_table(t)]
    if not unresolved:
        return []
    return [EntryCheck(kind, container, ident, CheckStatus.FLAG,
                       anchors={"owners": sorted({o for t in unresolved for o in index.table_owners(t)}),
                                "question": "the same bare table name is declared in more than one "
                                            "schema; does this entry mean one of them?"})]


@dataclass(frozen=True)
class _ValueCell:
    """The (table, column) context each value-field check needs, once the entry cleared the guards.

    Bundled rather than threaded through every helper as six parameters, and built exactly once per
    entry: `cell_corpus` re-walks constraints and re-derefs `source_evidence` on each call, and
    `normalize` would otherwise re-fold the whole corpus once per literal.
    """
    container: str
    table: str | None
    column: str | None
    index: ObjectIndex
    corpus_normalized: list[str]
    grounded_sample: list[str]

    @classmethod
    def build(cls, container: str, table: str | None, column: str | None,
              index: ObjectIndex) -> _ValueCell:
        corpus = index.cell_corpus(table, column)
        return cls(container, table, column, index, [normalize(c) for c in corpus], corpus[:5])

    @property
    def ident(self) -> dict:
        # A fresh dict per check: EntryCheck.identity is handed to the residue and the gate, so a
        # shared one would let a later mutation rewrite an already-emitted check's identity.
        return {"table": self.table, "column": self.column}

    def literal_ident(self, literal: object) -> dict:
        # The FAIL shape the value-cycle memo reads: `literal` present <=> a value was cited.
        return {"table": self.table, "column": self.column, "literal": literal}


def _nfo_range_fail(nfo, container: str, ident: dict) -> list[EntryCheck]:
    # The range is provable whichever table the name resolves to, so it must survive the ambiguity
    # guard in check_value_entry rather than be softened to a question the residue has to re-derive.
    if nfo is None or _in_unit_range(nfo):
        return []
    return [EntryCheck("null_fraction_override", container, ident, CheckStatus.FAIL,
                       f"null_fraction_override {nfo!r} for {ident['table']}.{ident['column']} "
                       f"is outside [0,1]")]


def _declared_enum_check(cell: _ValueCell, lit) -> EntryCheck:
    # The declared domain wins over an inferred one only for literals it actually contains.
    # An out-of-domain literal is the same guaranteed-true contradiction the gate adjudicates
    # as CitationType.DECLARED_ENUM, and ACCEPT_SKIP is forwarded to neither the residue nor
    # the gate -- so if this doesn't FAIL, nothing downstream ever checks it.
    if cell.index.literal_in_declared_domain(cell.table, cell.column, lit):
        return EntryCheck("inferred_enum", cell.container, cell.ident, CheckStatus.ACCEPT_SKIP)
    return EntryCheck("inferred_enum", cell.container, cell.literal_ident(lit), CheckStatus.FAIL,
                      f"inferred_enum literal {lit!r} for {cell.table}.{cell.column} is outside the "
                      f"declared enum domain {cell.index.declared_enum_domain(cell.table, cell.column)}")


def _grounded_enum_check(cell: _ValueCell, lit) -> EntryCheck:
    if literal_grounded_normalized(lit, cell.corpus_normalized):
        return EntryCheck("inferred_enum", cell.container, cell.ident, CheckStatus.PASS,
                          anchors={"grounded_in": cell.grounded_sample})
    return EntryCheck("inferred_enum", cell.container, cell.literal_ident(lit), CheckStatus.FAIL,
                      f"inferred_enum literal {lit!r} for {cell.table}.{cell.column} "
                      f"is not present in any source_evidence span")


def _check_inferred_enum(cell: _ValueCell, raw) -> list[EntryCheck]:
    literals = _wire_array(raw)
    if literals is None:
        return [EntryCheck("inferred_enum", cell.container, cell.ident, CheckStatus.FLAG,
                           anchors={"value": raw,
                                    "question": "inferred_enum is not an array; is it intended?"})]
    if cell.index.is_declared_enum(cell.table, cell.column):
        return [_declared_enum_check(cell, lit) for lit in literals]
    return [_grounded_enum_check(cell, lit) for lit in literals]


def _check_must_include(cell: _ValueCell, raw) -> list[EntryCheck]:
    values = _wire_array(raw)
    out: list[EntryCheck] = []
    if values is None:
        out.append(EntryCheck("must_include", cell.container, cell.ident, CheckStatus.FLAG,
                              anchors={"value": raw,
                                       "question": "must_include is not an array; is it intended?"}))
        values = []
    for val in values:
        if not isinstance(val, str) or not val.strip():
            # Nothing to ground against, so neither verdict is provable: a PASS here would carry a
            # grounded_in anchor asserting evidence that was never matched, steering the residue to ACCEPT.
            out.append(EntryCheck("must_include", cell.container, cell.ident, CheckStatus.FLAG,
                                  anchors={"value": val,
                                           "question": "must_include value is not a non-empty string; "
                                                       "is it intended?"}))
        elif not literal_grounded_normalized(val, cell.corpus_normalized):
            out.append(EntryCheck("must_include", cell.container, cell.literal_ident(val),
                                  CheckStatus.FAIL,
                                  f"must_include value {val!r} for {cell.table}.{cell.column} "
                                  f"is not present in any source_evidence span"))
        else:
            out.append(EntryCheck("must_include", cell.container, cell.ident, CheckStatus.PASS,
                                  anchors={"grounded_in": cell.grounded_sample}))
    return out


def _check_null_fraction_override(cell: _ValueCell, nfo) -> list[EntryCheck]:
    # Only the in-range case is graded here; an out-of-range value already FAILed in _nfo_range_fail,
    # which runs ahead of the ambiguity guard because its verdict needs no table resolution.
    if nfo is None or not _in_unit_range(nfo):
        return []
    if nfo > 0 and cell.index.is_pk_or_notnull(cell.table, cell.column):
        return [EntryCheck("null_fraction_override", cell.container, cell.ident, CheckStatus.FAIL,
                           f"null_fraction_override {nfo!r} cannot introduce nulls into "
                           f"{cell.table}.{cell.column}, which is a primary key or declared NOT NULL")]
    return [EntryCheck("null_fraction_override", cell.container, cell.ident, CheckStatus.FLAG,
                       anchors={"fraction": nfo,
                                "question": "does the source justify overriding nullability?"})]


def check_value_entry(entry: dict, container: str, index: ObjectIndex) -> list[EntryCheck]:
    # Existence/ambiguity guards first, then one independent per-field check composed in wire order.
    # Each field's rules live in its own helper: they share only the cell they are graded against, so
    # inlining them here bought nothing but one function past the length and complexity budget.
    table, col = _cell(entry)
    nfo = entry.get("null_fraction_override")
    # Each guard builds its own identity dict for the same reason _ValueCell.ident does: two emitted
    # checks sharing one object would let a later mutation rewrite an already-emitted identity.
    range_fail = _nfo_range_fail(nfo, container, {"table": table, "column": col})
    ambiguous = _ambiguity_check("column", container, {"table": table, "column": col}, index, table)
    if ambiguous:
        return range_fail + ambiguous
    if not index.has_column(table, col):
        return range_fail + [EntryCheck("column", container, {"table": table, "column": col},
                                        CheckStatus.FAIL, f"column {table}.{col} does not exist")]
    cell = _ValueCell.build(container, table, col, index)
    return (range_fail
            + _check_inferred_enum(cell, entry.get("inferred_enum"))
            + _check_must_include(cell, entry.get("must_include"))
            + _check_null_fraction_override(cell, nfo))


def _both_cells_distinct(index: ObjectIndex, t1, c1, t2, c2) -> bool:
    return not (_resolved_key(index, t1) == _resolved_key(index, t2) and str(c1).upper() == str(c2).upper())


def check_fk_chain(entry: dict, index: ObjectIndex) -> list[EntryCheck]:
    ct, cc = entry.get("child_table"), entry.get("child_col")
    pt, pc = entry.get("parent_table"), entry.get("parent_col")
    ident = {"child_table": ct, "child_col": cc, "parent_table": pt, "parent_col": pc}

    def fail(msg: str) -> list[EntryCheck]:
        return _fail("fk_chains", ident, msg)

    ambiguous = _ambiguity_check("fk_chains", "fk_chains", ident, index, ct, pt)
    if ambiguous:
        return ambiguous
    if not index.has_column(ct, cc):
        return fail(f"fk_chains child column {ct}.{cc} does not exist")
    if not index.has_column(pt, pc):
        return fail(f"fk_chains parent column {pt}.{pc} does not exist")
    if not _both_cells_distinct(index, ct, cc, pt, pc):
        return fail("fk_chains is a self-join on identical columns")
    dfk = index.declared_fk(ct, cc)
    if dfk and _table_matches(index, dfk[0], pt) and str(dfk[1] or "").upper() == str(pc).upper():
        return [EntryCheck("fk_chains", "fk_chains", ident, CheckStatus.ACCEPT_SKIP)]
    if not index.has_kind_for_cell(ct, cc, ("fk", "join_edge")):
        return fail(f"fk_chains for {ct}.{cc} maps to no unsolved fk/join_edge constraint (spurious)")
    mined = [c.get("detail") for c in index.cell_constraints(ct, cc) if c.get("kind") in ("fk", "join_edge")]
    return [EntryCheck("fk_chains", "fk_chains", ident, CheckStatus.PASS,
                       anchors={"child": f"{ct}.{cc}", "proposed_parent": f"{pt}.{pc}", "mined_edges": mined})]


def _group_table_names(tables: list) -> list:
    # Wire shape is [{table, columns}] (CorrelatedGroupTableEntry). A bare string is tolerated so a
    # hand-built entry degrades to a name instead of pushing an unhashable dict through the guards.
    return [t.get("table") if isinstance(t, dict) else t for t in tables]


def _split_tuple_col(tc, tables: list) -> list[tuple]:
    # "TABLE.COLUMN" -> (table, col); bare "COLUMN" -> pair with every table in the group.
    if isinstance(tc, str) and "." in tc:
        t, c = tc.rsplit(".", 1)
        return [(t, c)]
    return [(t, tc) for t in tables]


def check_correlated_group(entry: dict, index: ObjectIndex) -> list[EntryCheck]:
    names = _group_table_names(entry.get("tables", []) or [])
    tuple_cols = entry.get("tuple_columns", []) or []
    ident = {"tables": entry.get("tables", []) or [], "tuple_columns": tuple_cols,
             "group_id": entry.get("group_id")}

    def fail(msg: str) -> list[EntryCheck]:
        return _fail("correlated_groups", ident, msg)

    # Two names are one table only when they resolve to the same owner, so this survives resolution and
    # stays a hard FAIL even for an ambiguous name. Comparing bare names instead would reject
    # SALES.ORDERS + STAGING.ORDERS -- a legitimate cross-schema group.
    if len({_resolved_key(index, n) for n in names}) < 2:
        return fail("correlated_groups needs at least 2 distinct tables")
    ambiguous = _ambiguity_check("correlated_groups", "correlated_groups", ident, index, *names)
    if ambiguous:
        return ambiguous
    cells = [pair for tc in tuple_cols for pair in _split_tuple_col(tc, names)]
    for t, c in cells:
        if not index.has_column(t, c):
            return fail(f"correlated_groups column {t}.{c} does not exist")
    if not any(index.has_kind_for_cell(t, c, ("branch_predicate",)) for t, c in cells):
        return fail("correlated_groups maps to no unsolved branch_predicate gap (spurious)")
    return [EntryCheck("correlated_groups", "correlated_groups", ident, CheckStatus.PASS,
                       anchors={"cells": [f"{t}.{c}" for t, c in cells],
                                "question": "is the correlation real, or a coincidence?"})]


def check_temporal(entry: dict, index: ObjectIndex) -> list[EntryCheck]:
    # One table, two of its date columns: column_deb / column_fin = the span's start ("début") and end
    # ("fin"). The names are wire-contract-locked (TemporalAlignmentEntry), not descriptive labels.
    t = entry.get("table")
    deb, fin = entry.get("column_deb"), entry.get("column_fin")
    ident = {"table": t, "column_deb": deb, "column_fin": fin}

    def fail(msg: str) -> list[EntryCheck]:
        return _fail("temporal_alignment", ident, msg)

    # Provable whichever table the name resolves to, so it survives the ambiguity guard.
    same_column = [] if str(deb).upper() != str(fin).upper() else fail(
        "temporal_alignment references the same column twice")
    ambiguous = _ambiguity_check("temporal_alignment", "temporal_alignment", ident, index, t)
    if ambiguous:
        return same_column + ambiguous
    if same_column:
        return same_column
    for col in (deb, fin):
        if not index.has_column(t, col):
            return fail(f"temporal_alignment column {t}.{col} does not exist")
        if not index.is_date(t, col):
            return fail(f"temporal_alignment column {t}.{col} is not a date/timestamp")
    return [EntryCheck("temporal_alignment", "temporal_alignment", ident, CheckStatus.FLAG,
                       anchors={"question": "does the source imply column_deb <= column_fin?"})]


def check_anti_join(entry: dict, index: ObjectIndex) -> list[EntryCheck]:
    t, fkc = entry.get("table"), entry.get("fk_column")
    frac = entry.get("anti_join_fraction")
    ident = {"table": t, "fk_column": fkc, "anti_join_fraction": frac}

    def fail(msg: str) -> list[EntryCheck]:
        return _fail("anti_join_tables", ident, msg)

    # The range check needs no table resolution, so it stays a hard FAIL even for an ambiguous name.
    if not _in_unit_range(frac):
        return fail(f"anti_join_tables anti_join_fraction {frac!r} is outside [0,1]")
    ambiguous = _ambiguity_check("anti_join_tables", "anti_join_tables", ident, index, t)
    if ambiguous:
        return ambiguous
    if not index.has_column(t, fkc):
        return fail(f"anti_join_tables column {t}.{fkc} does not exist")
    return [EntryCheck("anti_join_tables", "anti_join_tables", ident, CheckStatus.FLAG,
                       anchors={"anti_join_fraction": frac,
                                "question": "does the source contain a real NOT EXISTS / LEFT JOIN ... IS NULL?"})]


_STRUCTURAL_CHECKERS = {
    "fk_chains": check_fk_chain,
    "correlated_groups": check_correlated_group,
    "temporal_alignment": check_temporal,
    "anti_join_tables": check_anti_join,
}

_VALUE_CONTAINERS = ("column_enrichments", "branch_values")


def reads_column_facts(envelope: dict) -> bool:
    """True when grading this envelope would actually read the per-object column facts.

    Derived from the two registries above rather than restated as its own literal list, so registering a
    new checker cannot leave a caller's answer stale. The partition is exactly those registries: every
    array with a checker reads facts (each one consults `has_column` before it asserts anything, and the
    value containers additionally read the grounding corpus), while every array without one falls to
    `_uncovered`, which inspects only the entry's own keys and can only ever FLAG.

    Emptiness is what makes this answerable at all: `run_backbone` iterates `envelope.get(array, []) or
    []`, so an absent or empty array contributes no entries and therefore reads nothing -- the same
    truthiness test used here. Callers use this to tell "the facts are missing and something needs them"
    from "the facts are missing and nothing was going to read them", which are different situations: only
    the first can manufacture a verdict out of an empty fact base.
    """
    return any(envelope.get(array) for array in (*_VALUE_CONTAINERS, *_STRUCTURAL_CHECKERS))


def _uncovered(array: str, entry: dict) -> list[EntryCheck]:
    # An enrichment type this backbone predates has no deterministic verdict available, but skipping it
    # is the one outcome that must not happen: run_backbone would iterate neither it nor the residue, so
    # the entry would be applied having been checked by nobody. Hand it to the residue as a question.
    return [EntryCheck(array, array, {"container": array}, CheckStatus.FLAG,
                       anchors={"fields": sorted(k for k, v in entry.items() if v is not None),
                                "question": "this enrichment type has no deterministic checker in the "
                                            "backbone; does the entry hold up on inspection?"})]


def run_backbone(envelope: dict, index: ObjectIndex) -> list[EntryCheck]:
    checks: list[EntryCheck] = []
    for container in _VALUE_CONTAINERS:
        for entry in envelope.get(container, []) or []:
            checks.extend(check_value_entry(entry, container, index))
    for array, checker in _STRUCTURAL_CHECKERS.items():
        for entry in envelope.get(array, []) or []:
            checks.extend(checker(entry, index))
    covered = set(_VALUE_CONTAINERS) | set(_STRUCTURAL_CHECKERS)
    for array, entries in envelope.items():
        if array in covered or not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict):
                checks.extend(_uncovered(array, entry))
    return checks


def build_critique_request(checks: list[EntryCheck]) -> dict:
    entries = [
        {"kind": c.kind, "container": c.container, "identity": c.identity,
         "status": c.status, "citation": c.citation, "anchors": c.anchors}
        for c in checks if c.status in (CheckStatus.PASS, CheckStatus.FLAG)
    ]
    return {"schema_version": 1, "entries": entries}
