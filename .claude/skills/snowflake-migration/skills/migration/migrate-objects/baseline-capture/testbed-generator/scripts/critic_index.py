"""Read-only index over per-object testbed JSONs + the list-unsolved view.

The backbone dispatches on facts, not on the opaque state.bin: column existence/type from the
per-object `columns[]`, the list-unsolved constraints (per kind and per cell), and a grounding
corpus per (table,column) built from constraint `detail` + deref'd `source_evidence`. Both column
facts and constraint cells are keyed on the resolved qualified owner and reached through a bare-name
alias: bare keying alone would let two schemas' same-named tables overwrite each other's columns and
share one constraint bucket, and the critic would then validate enrichments against another table's
facts or ground a literal in another table's evidence. list-unsolved rows are sometimes
schema-qualified, sometimes bare, and fk/enum/check rows carry table=None with the owner in `object`,
so resolution is guarded by `names_compatible`: a row may only be attributed to a table whose name it
under- or over-qualifies, never to one whose schema it contradicts. A row that cannot be attributed
keeps the name it was written with (qualified) or the bare name, and is recorded in `unattributed`
when a differently-schema'd table would otherwise have absorbed it.

Cell lookups are then deliberately path-dependent, because the two readers fail in opposite
directions. `cell_corpus` (grounding) is permissive and merges the unattributable bare bucket into
every candidate owner: a row it cannot see makes a golden literal false-REJECT, and a backbone FAIL
is a contractually guaranteed-true hard reject. `cell_constraints` / `has_kind_for_cell` (structural)
is strict: there an EXTRA row from a table the entry never named manufactures a hard reject, while a
missing one only routes the entry to the residue. A bare name that maps to more than one owner is
`ambiguous_table` and yields no column facts at all -- the backbone's FAILs are contractually
guaranteed-true, so an unresolvable name must route to the residue rather than assert anything.

An artifact's own name is read as `object ?? table`, mirroring TestbedArtifact.ResolvedName: procedural
artifacts name themselves in `object`, table artifacts in `table`. A TABLE artifact with neither is
recorded in `skipped` rather than indexed, and two artifacts claiming one owner are recorded in
`ambiguities` -- either would otherwise make a table's columns vanish with nothing in the report.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from critic_normalize import deref_pointer, literal_grounded, normalize


def canon_table(name: str | None) -> str:
    return str(name or "").split(".")[-1].upper()


def canon_owner(name: str | None) -> str:
    return str(name or "").strip().upper()


def names_compatible(a: str | None, b: str | None) -> bool:
    """True when two object names can denote the same table: every part they both spell agrees.

    Compared right-to-left over the shared depth, so `ORDERS` and `DB.SALES.ORDERS` are both
    compatible with the artifact `SALES.ORDERS` (one under-qualifies, one over-qualifies the same
    table) while `STAGING.ORDERS` is not (it names a schema the artifact contradicts). This is the
    test `_resolve`'s bare-alias fallback lacks: that fallback answers "which captured table shares
    this leaf name", which for a row that already named its own schema is a different question.
    """
    pa = [p for p in canon_owner(a).split(".") if p]
    pb = [p for p in canon_owner(b).split(".") if p]
    n = min(len(pa), len(pb))
    return n > 0 and pa[-n:] == pb[-n:]


@dataclass
class ObjectIndex:
    objects: dict = field(default_factory=dict)          # object name (as written) -> testbed json
    tables: dict = field(default_factory=dict)           # canon owner (qualified) -> {col upper: colfacts}
    _bare: dict = field(default_factory=dict)            # canon bare table -> [canon owner, ...]
    _by_kind: dict = field(default_factory=dict)         # kind -> [constraint]
    _by_cell: dict = field(default_factory=dict)         # (canon table, col upper) -> [constraint]
    skipped: list = field(default_factory=list)          # testbed JSONs dropped as unreadable/corrupt
    ambiguities: list = field(default_factory=list)      # bare table names owned by >1 qualified object
    unattributed: list = field(default_factory=list)     # qualified rows naming a table no artifact covers

    def _resolve(self, table: str | None) -> list[str]:
        # Exact qualified match first, then the bare alias -- so a 3-part name still finds a 2-part
        # artifact, and a bare list-unsolved row still finds its uniquely-named table.
        owner = canon_owner(table)
        if owner in self.tables:
            return [owner]
        return list(self._bare.get(canon_table(table), []))

    def table_owners(self, table: str | None) -> list[str]:
        return self._resolve(table)

    def ambiguous_table(self, table: str | None) -> bool:
        return len(self._resolve(table)) > 1

    def has_column(self, table: str | None, col: str | None) -> bool:
        return self.col_facts(table, col) is not None

    def col_facts(self, table: str | None, col: str | None) -> dict | None:
        owners = self._resolve(table)
        if len(owners) != 1:  # unknown table, or a bare name several schemas answer to
            return None
        return self.tables[owners[0]].get(str(col).upper())

    def is_date(self, table: str | None, col: str | None) -> bool:
        c = self.col_facts(table, col)
        return bool(c and c.get("is_date"))

    def is_declared_enum(self, table: str | None, col: str | None) -> bool:
        c = self.col_facts(table, col)
        return bool(c and c.get("enum_domain") and c.get("semantic_class") == "enum")

    def declared_enum_domain(self, table: str | None, col: str | None) -> list[object]:
        # list[object], not list[str]: the domain is copied out of the artifact verbatim, so a
        # numeric or boolean member arrives as it was mined. Every reader goes through normalize.
        return list((self.col_facts(table, col) or {}).get("enum_domain") or [])

    def literal_in_declared_domain(self, table: str | None, col: str | None,
                                   literal: object) -> bool:
        # The backbone's declared-enum fast path and the gate's CitationType.DECLARED_ENUM arm
        # adjudicate the same fact from opposite directions; sharing one predicate is what keeps them
        # from disagreeing, which would let the gate DROP a literal the backbone hard-REJECTed.
        return normalize(literal) in {normalize(x) for x in self.declared_enum_domain(table, col)}

    def declared_fk(self, table: str | None, col: str | None) -> tuple | None:
        c = self.col_facts(table, col)
        if c and c.get("foreign_key") and c.get("foreign_key_referenced_table"):
            return (c["foreign_key_referenced_table"], c.get("foreign_key_referenced_column"))
        return None

    def is_pk_or_notnull(self, table: str | None, col: str | None) -> bool:
        c = self.col_facts(table, col)
        return bool(c and (c.get("primary_key") or c.get("nullable") is False))

    def _cell_keys(self, table: str | None, col: str | None, *, permissive: bool) -> list[tuple]:
        # Two buckets are always in scope: the row's resolved owner (when the name resolves to exactly
        # one table AND that table does not contradict the schema the name spells), and the name exactly
        # as written -- which is where load_index parks a row it could not attribute, so a lookup naming
        # the same table still reaches its own evidence.
        col_u = str(col).upper()
        owners = self._resolve(table)
        keys: list = []
        if len(owners) == 1 and names_compatible(table, owners[0]):
            keys.append((owners[0], col_u))
        if canon_owner(table) and (canon_owner(table), col_u) not in keys:
            keys.append((canon_owner(table), col_u))
        if not permissive:
            return keys
        # The permissive tail: the bare-name bucket (rows whose owner resolved to zero or several
        # tables), plus every candidate owner of an ambiguous bare name. Reserved for the GROUNDING
        # corpus, where a missing row makes a golden literal false-REJECT -- a guaranteed-true hard
        # reject asserted on evidence the reader simply could not see. The structural path deliberately
        # does NOT take this tail: there the asymmetry inverts (see cell_constraints).
        for candidate in [(canon_table(table), col_u)] + [(o, col_u) for o in owners]:
            if candidate not in keys:
                keys.append(candidate)
        return keys

    def _cell_rows(self, table: str | None, col: str | None, *, permissive: bool) -> list[dict]:
        rows: list = []
        for key in self._cell_keys(table, col, permissive=permissive):
            rows.extend(self._by_cell.get(key, []))
        return rows

    def cell_corpus(self, table: str | None, col: str | None) -> list[str]:
        corpus: list = []
        for c in self._cell_rows(table, col, permissive=True):
            if c.get("detail"):
                corpus.append(c["detail"])
            # deref target = THIS row's own object json (the TABLE for fk/enum/check, the proc for edges/predicates)
            owner = self.objects.get(c.get("object"))
            corpus.extend(deref_pointer(c.get("source_evidence"), owner or {}))
        return corpus

    def literal_grounded_in_cell(self, table: str | None, col: str | None, literal: object) -> bool:
        return literal_grounded(literal, self.cell_corpus(table, col))

    def cell_constraints(self, table: str | None, col: str | None) -> list[dict]:
        # Strict, unlike cell_corpus, because the failure asymmetry runs the other way on this path.
        # These rows answer "does a mined constraint back this structural claim", and an EXTRA row from
        # a table the entry never named manufactures a hard reject: critic_gate's fk_parent_mismatch arm
        # REVISEs (bounded, re-promptable) when `mined` is empty but hard-REJECTs when it is non-empty
        # and the proposed parent is absent from it -- so borrowing another schema's edge converts a
        # bounded revise into a guaranteed-true-shaped REJECT the entry cannot answer. A MISSING row
        # only routes the entry to the residue, which is the recoverable direction. (Nothing is lost by
        # dropping the bare bucket here: a name that resolves to zero or several tables is stopped
        # upstream by the backbone's own has_column / _ambiguity_check guards before it reaches a kind
        # test, so the bare bucket has no reachable reader on this path.)
        return self._cell_rows(table, col, permissive=False)

    def has_kind_for_cell(self, table: str | None, col: str | None, kinds: tuple) -> bool:
        return any(c.get("kind") in kinds for c in self.cell_constraints(table, col))


def _iter_testbed_jsons(artifacts_path: str, skipped: list[str]):
    root = Path(artifacts_path)
    if not root.is_dir():
        return
    for p in sorted(root.rglob("*.testbed.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        # read_text raises UnicodeDecodeError on a file that died mid-codepoint, which is a ValueError
        # and so escapes OSError/JSONDecodeError entirely -- one truncated artifact would abort the
        # whole index build. The explicit utf-8 is what makes that guarantee hold: on the locale
        # default a non-UTF-8 host (cp1252 leaves only 5 byte values undefined) decodes an accented
        # artifact to mojibake without raising at all, so nothing lands in `skipped` and a genuine
        # golden literal instead false-REJECTs as absent from every source_evidence span.
        except (OSError, ValueError) as exc:
            # A corrupt/unreadable artifact silently vanishing from the index makes the backbone
            # hard-REJECT that table's columns as "does not exist"; record it so the drop is visible.
            skipped.append(f"{p}: {exc}")
            continue
        if isinstance(doc, dict):
            yield p, doc


def load_index(artifacts_path: str | Path, unsolved_view: dict | None) -> ObjectIndex:
    idx = ObjectIndex()
    for path, doc in _iter_testbed_jsons(str(artifacts_path), idx.skipped):
        # Mirrors TestbedArtifact.ResolvedName (object ?? table): procedural artifacts name themselves in
        # `object`, table artifacts in `table`. Reading only `object` collapsed every artifact of the
        # latter shape onto one nameless key, and the last one read silently won.
        name = doc.get("object") or doc.get("table")
        if name:
            idx.objects[name] = doc
        if doc.get("object_type") == "TABLE":
            owner = canon_owner(name)
            if not owner:
                skipped_reason = "TABLE artifact names itself in neither 'object' nor 'table'"
                idx.skipped.append(f"{path}: {skipped_reason}")
                continue
            cols = {str(c.get("name")).upper(): c for c in doc.get("columns", []) if isinstance(c, dict)}
            if owner in idx.tables and idx.tables[owner] != cols:
                # Two artifacts claiming one owner: the second overwrites the first, so the critic would
                # validate against half a table with nothing in the report to explain it.
                idx.ambiguities.append(f"table {owner} is described by more than one artifact with "
                                       f"differing columns; the last one read wins")
            idx.tables[owner] = cols
            aliases = idx._bare.setdefault(canon_table(name), [])
            if owner not in aliases:  # a re-read of the same owner is not a collision
                aliases.append(owner)
    for bare, owners in idx._bare.items():
        if len(owners) > 1:
            idx.ambiguities.append(f"bare table name {bare} is owned by {', '.join(sorted(owners))}")
    by_kind = (unsolved_view or {}).get("by_kind", {})
    for kind, block in by_kind.items():
        for c in block.get("constraints", []):
            if not isinstance(c, dict):
                continue
            idx._by_kind.setdefault(kind, []).append(c)
            owner = c.get("table") or c.get("object")
            # Key on the resolved owner, not the bare name: bare keying put SALES.ORDERS.STATUS and
            # STAGING.ORDERS.STATUS in one bucket, so one schema's grounding corpus contained the
            # other's evidence and the backbone PASSed literals invented for the table it was checking.
            # `_resolve` is fully populated by now (the artifact loop and the collision scan above have
            # both run).
            #
            # Resolution alone is not enough, because `_resolve` falls back to the bare alias: with only
            # SALES.ORDERS captured, a row that explicitly says STAGING.ORDERS resolves to
            # ['SALES.ORDERS'] -- length 1, so the "cannot be attributed" escape below never fires --
            # and STAGING's evidence lands in SALES' bucket, re-creating the exact leak this keying
            # exists to close (one schema grounding the other's literals, and one schema's mined fk
            # backing the other's fk_chain as a hard reject). `names_compatible` is the missing guard: it
            # accepts a row that under- or over-qualifies the same table and rejects one that names a
            # contradicting schema. A name that resolves to zero or several tables genuinely cannot be
            # attributed, so it stays on the bare key and `_cell_keys`' permissive tail merges it into
            # every candidate owner for grounding.
            owners = idx._resolve(owner)
            if len(owners) == 1 and names_compatible(owner, owners[0]):
                key_owner = owners[0]
            elif owners and "." in str(owner or ""):
                # Qualified, and the bare alias points at a table whose schema this name contradicts --
                # the mis-attribution above. Keep the row on its own name so it is reachable from a
                # lookup naming the same table, and from nowhere else. Narrow on `owners` deliberately:
                # when NOTHING is captured under that leaf name there is no other schema to absorb the
                # row, so it keeps the bare key and a bare lookup still reaches it.
                key_owner = canon_owner(owner)
                # Silence here is what made this invisible: `ambiguities` stays empty (a qualified name
                # is not ambiguous) and `ambiguous_table` is False, so nothing in the report explained
                # why the row's evidence stopped counting anywhere.
                note = (f"constraint rows name {key_owner}, which has no TABLE artifact; the only "
                        f"captured table sharing that name is {', '.join(sorted(owners))}, so those "
                        f"rows are attributed to neither")
                if note not in idx.unattributed:
                    idx.unattributed.append(note)
            else:
                key_owner = canon_table(owner)
            cell = (key_owner, str(c.get("column")).upper())
            idx._by_cell.setdefault(cell, []).append(c)
    return idx
