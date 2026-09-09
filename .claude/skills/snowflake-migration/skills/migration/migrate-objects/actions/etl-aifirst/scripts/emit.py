"""Emit the producer IR JSON, plus per-field provenance for the fit score.

Schema target: AiFirstProducerIrHydrator.Hydrate -- nodes[{id,type,modelName,
element{$kind,Name,InputColumns,OutputColumns}}], edges[{from,to,label?}].

PLATFORM NEUTRALITY CONTRACT (added by the SSIS generalisation pass)
--------------------------------------------------------------------
No source-vocabulary literal appears in this file. The IR field names
($kind, Name, InputColumns, OutputColumns, Precision, Scale) DO appear -- they
are the contract, which is the same for every platform, and they are the one
thing that is legitimately hardcoded here.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

from identify import (CONTAINER_ROLES, DERIVED, MISSING, MODEL, NO_SLOT,
                      NO_SLOT_DETAIL_VOCABULARY, RESIDUE, SOURCE, TABLE,
                      Identification, Port)
from source_sql import attach_source_sql

PLACEHOLDER_KIND = "UnsupportedTransformation"


def render_detail(rule: dict, tpl: str, values: dict) -> str:
    """Render a table-authored `detail` template against a CLOSED keyword set.

    Two jobs, and the first is the reason this is a function rather than three
    `tpl.format(...)` calls. `identify.validate_table` rejects a template naming anything
    outside `NO_SLOT_DETAIL_VOCABULARY[rule['from']]`, which is only sound while that
    declaration and the keywords passed HERE say the same thing. A framework change that
    adds a keyword to a call site and forgets the declaration would make the validator
    reject legal tables; one that removes a keyword would make it accept a template that
    crashes at emission. So the parity is asserted rather than trusted -- the declaration
    is the check, and this keeps the check honest.

    The second job is the message. A template that slips past validation must still not
    surface as a bare `KeyError` naming one word and no rule."""
    declared = NO_SLOT_DETAIL_VOCABULARY[rule["from"]]
    assert set(values) == set(declared), (
        f"{rule['from']} detail vocabulary drifted: identify.py declares "
        f"{sorted(declared)}, emit.py supplies {sorted(values)}. "
        f"identify.validate_table checks author templates against the declaration, so "
        f"the two must agree.")
    if not tpl:
        return ""
    try:
        return tpl.format(**values)
    except KeyError as ex:
        raise ValueError(
            f"no_slot_facts[{rule.get('id')!r}].detail names {ex.args[0]!r}, which its "
            f"{rule['from']} formatter does not supply. It may name only "
            f"{list(declared)}.") from ex


# FRAMEWORK CHANGE 66: THE HYDRATOR'S CONTRACT, CHECKED BEFORE WE HAND IT A KIND.
#
# Mirrors the `kind switch` in
# `../callable-entrypoint/Producer/AiFirstProducerIrHydrator.cs:254-330`. That switch is
# the SOURCE OF TRUTH; this is a guard in front of it, and a kind added there must be
# added here or it will be refused (which is the safe direction).
#
# WHY THIS EXISTS. A sidecar-supplied `$kind` used to be promoted unchecked, on the
# reasonable-sounding ground that the model had asserted it. Two ways that loses a
# document rather than an element:
#
#   1. A kind the switch has no arm for -- `RouterTransformation`, `JoinTransformation` --
#      falls through to its `_ => throw`.
#   2. An accepted kind whose REQUIRED payload is absent: `FilterTransformation` with no
#      `FilterConditions` reaches `RequiredString`, which throws.
#
# Either throw happens during hydration of ONE element and takes THE WHOLE DOCUMENT with
# it -- every other element, every edge, the lineage, the reports. The blast radius is the
# reason this is checked here and not left to the hydrator's own exception.
#
# This is the SAME RULE the deterministic path already follows: a payload-dependent kind
# whose required field cannot resolve DEGRADES rather than emitting a hollow element
# (`element_fields`, FRAMEWORK CHANGE 47). It held for table-declared kinds and not for
# sidecar-declared ones -- one rule honoured in one place and not its sibling, which is
# the shape of defect this project keeps finding. Unreachable while sidecars were
# hand-authored; reachable the moment `sidecar_producer.py` began producing them.
#
# `sidecar_producer.py` carries its own `KIND_CONTRACT` so it can refuse a bad answer at
# production time and re-prompt. That is a DIFFERENT job -- refuse early, before the file
# exists -- and this guard must not be deleted in favour of it: a sidecar can be
# hand-edited, produced by an older build, or written by something that is not our
# producer at all. Both copies cite the hydrator; the hydrator is what settles a
# disagreement.
HYDRATOR_KIND_CONTRACT = {
    "SourceQualifier": (),
    "ExpressionTransformation": (),
    "FilterTransformation": ("FilterConditions",),
    "TargetTransformation": ("TableName",),
    "UnsupportedTransformation": (),
}


@dataclass
class Slot:
    """One fit obligation: a field the contract wants, or a fact with no field."""

    element: str
    path: str          # dotted path into the emitted JSON, or the source fact name
    provenance: str
    where: str         # xpath, table rule id, or algorithm name
    detail: str = ""

    @property
    def satisfied(self) -> bool:
        return self.provenance in (SOURCE, TABLE, DERIVED)


# ---------------------------------------------------------------------------
# expression handling: a hand-rolled scanner over the expression string.
# Deliberately NOT a regex. Identifiers resolve against a CLOSED set of port
# names read from the document; delimited references resolve against a CLOSED
# set of column identities read from the document.
#
# FRAMEWORK CHANGE 19: v1 hardcoded the single-quote string literal and knew no
# delimited-reference form. SSIS uses double quotes and wraps every column
# reference in #{...} around a full lineage id, which the v1 scanner would have
# shredded into a dozen bogus identifiers.
# ---------------------------------------------------------------------------

_IDENT_START = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


def scan(text: str, quotes=("'",), ref_delims=None, extra="$") -> list[tuple[str, str]]:
    """-> [(kind, lexeme)] where kind is 'ident', 'str', 'ref', 'other'."""
    body = _IDENT_START | set("0123456789") | set(extra)
    out: list[tuple[str, str]] = []
    open_d, close_d = (ref_delims or (None, None))
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if open_d and text.startswith(open_d, i):
            j = text.find(close_d, i + len(open_d))
            if j == -1:
                out.append(("other", c))
                i += 1
                continue
            out.append(("ref", text[i + len(open_d): j]))
            i = j + len(close_d)
        elif c in quotes:
            j = i + 1
            while j < n and text[j] != c:
                j += 1
            out.append(("str", text[i: j + 1]))
            i = j + 1
        elif c in _IDENT_START:
            j = i
            while j < n and text[j] in body:
                j += 1
            out.append(("ident", text[i:j]))
            i = j
        else:
            out.append(("other", c))
            i += 1
    return out


class Emitter:
    def __init__(self, idn: Identification):
        self.idn = idn
        self.table = idn.table
        self.pol = self.table["port_policy"]
        self.syn = self.table["expression_syntax"]
        self.slots: list[Slot] = []
        # (ir_field, raw, transformed) per element_fields read that a declared transform
        # rewrote. Kept because a transform is the one place a table can destroy the
        # distinction between two elements, and the loss is invisible afterwards: only
        # the OUTPUT reaches the IR. See collapsed_transforms.
        self.transformed_reads: list[tuple[str, str, str]] = []
        self.ai = self._load_sidecar()
        self._assert_fact_rules_distinct()
        self._assert_attr_residue_usable()

    def collapsed_transforms(self) -> dict[tuple[str, str], list[str]]:
        """Transformed fields where two or more distinct source readings became one value.

        A table declares a transform to normalise a reading, not to merge readings, so
        this is always information the table destroyed. MEASURED on the blind Alteryx
        table of 2026-08-24: `TableName` took `UNQUALIFIED_TAIL`, a dotted-identifier
        stripper meant for `[dbo].[CUSTOMER]`, and applied it to
        `\\\\corp-fileshare\\ETL\\Sales\\Orders_Online.csv`. The tail after the last dot
        is the file EXTENSION, so all three inputs and all three outputs resolved to one
        relation named `csv`, every model read `source('raw', 'csv')`, and two of them
        selected columns that relation could not have.
        """
        by_value: dict[tuple[str, str], set[str]] = {}
        for ir_field, raw, value in self.transformed_reads:
            by_value.setdefault((ir_field, value), set()).add(raw)
        return {key: sorted(raws) for key, raws in by_value.items() if len(raws) > 1}

    # -- FRAMEWORK CHANGE 66 (a): TWO RULES, ONE READING ---------------------

    def _fact_read_key(self, rule: dict) -> str | None:
        """A canonical description of WHERE a no_slot_facts rule reads from.

        Two rules with the same read key read the SAME value out of the SAME
        document node, so at most one of them can be a distinct obligation. The
        key is computed from the table alone and contains no source vocabulary:
        the site xpath and attribute names come from the platform's own
        `attr_site` declaration.

        WHY ELEMENT_ATTR NEEDS TRANSLATING. `record_no_slot_facts`'s ELEMENT_ATTR
        branch does not read an XML attribute -- it reads `el.table_attrs`, the
        property bag that `_read_table_attrs` fills FROM the def site's declared
        `attr_site`. So on a platform whose properties are child name/value pairs,
        `ELEMENT_ATTR attr=X` and a CHILD_* rule pointed at that same pair are the
        same reading spelled two ways, and nothing detected it.

        Returns None for rule kinds whose target is not a single named node
        (GROUP, PORT, FIELD_EDGE, HARVEST, CONTAINER, ATTR_RESIDUE): those fan out
        over many keyed facts and two of them cannot silently be one obligation.
        ATTR_RESIDUE additionally cannot COLLIDE with a named rule by construction --
        it is the complement of exactly the set this method's callers describe -- so
        `_assert_attr_residue_usable` is what guards it instead.
        """
        src = rule["from"]
        if src in ("ELEMENT_ATTR", "DEF_SITE_ATTR"):
            at = self._attr_site()
            if at is None:
                return f"SELF_ATTR/@{rule['attr']}"
            if at.get("value_from") == "SELF_ATTRS":
                return f"SELF_ATTR/@{rule['attr']}"
            site = f"{at['xpath']}[@{at['name_attr']}='{rule['attr']}']"
            if at.get("value_from") == "TEXT":
                return f"CHILD_TEXT {site}/text()"
            return f"CHILD_ATTR {site}/@{at.get('value_attr')}"
        if src == "CHILD_TEXT":
            return f"CHILD_TEXT {rule['xpath']}/text()"
        if src == "CHILD_TEXT_TEMPLATE":
            parts = ",".join(f"{k}={v}" for k, v in sorted(rule["parts"].items()))
            return f"CHILD_TEXT_TEMPLATE {parts}/text()"
        if src == "CHILD_ATTR":
            return f"CHILD_ATTR {rule['xpath']}/@{rule['attr']}"
        return None

    def _attr_site(self) -> dict | None:
        """The declared property site, from whichever def site declares one.

        Read across every def site rather than only the default, because the bag
        the ELEMENT_ATTR census branch consults is filled by whichever site the
        element's kind resolves to.
        """
        st = self.table["structure"]
        cands = [st.get("self_def_site") or {}]
        cands += list((st.get("def_sites") or {}).values())
        for c in cands:
            if isinstance(c, dict) and c.get("attr_site"):
                return c["attr_site"]
        return None

    def _assert_fact_rules_distinct(self) -> None:
        """Raise when two no_slot_facts rules are the same reading.

        MEASURED DEFECT THIS CATCHES, and the reason it raises rather than warns.
        `platform_ssis.json` declared `open_rowset` (ELEMENT_ATTR @OpenRowset) and
        `oledb_open_rowset` (CHILD_TEXT ./properties/property[@name='OpenRowset']).
        The second is the rule `element_fields` promotes into `element.TableName`,
        and promotion suppresses only the promoted id -- so `!open_rowset` was
        still reported as an UNMET obligation citing the same location, with the
        same value, on an element whose TableName was populated from it. A FALSE
        unmet obligation: the document states the fact and the IR carries it.

        It raises because a table typo of this shape is invisible in the output --
        it looks exactly like a genuine coverage gap, which is the direction this
        framework must never fail in.
        """
        seen: dict[str, str] = {}
        for rule in self.table["no_slot_facts"]:
            k = self._fact_read_key(rule)
            if k is None:
                continue
            if k in seen:
                raise ValueError(
                    f"no_slot_facts rules '{seen[k]}' and '{rule['id']}' are the SAME "
                    f"reading ({k}). Two ids for one document value make one of them a "
                    f"FALSE unmet obligation: the census reports the un-promoted id as "
                    f"slotless while the promoted id fills an IR field from the same node. "
                    f"Delete one, or give them different sites.")
            seen[k] = rule["id"]

    def _load_sidecar(self) -> dict:
        """FRAMEWORK CHANGE 61: THE MODEL-AUTHORED SIDECAR — tier 2 of the fallback ladder.

        WHY THIS EXISTS. Leaning on the engine's IR made the IR a GATE on generation
        rather than a carrier for it. An element kind outside the vocabulary, a predicate
        no rule kind can scrape, an expression in a dialect no translator lowers -- each
        terminated in a NULL placeholder. On an unsupported platform every one of those is
        the expected case, so "nothing" was the normal output of an AI-first migrator.
        That is the wrong outcome: imperfect-and-marked beats absent.

        THE SIDECAR IS WHERE THE MODEL'S ANSWER LANDS. `<document>.ai.json`, keyed by
        element name, supplying exactly the things deterministic identification cannot get:

            {"elements": {"<element name>": {
                "$kind": "ExpressionTransformation",        # a kind the table has none for
                "FilterConditions": "BirthYear >= 1990",    # a predicate no rule can scrape
                "OutputColumns": [                          # expressions in Snowflake dialect
                    {"Name": "FullName", "Expression": "..."}]}}}

        A FILE AND NOT AN INLINE CALL, for three reasons that matter more than convenience:
        it is inspectable and diffable, so a reviewer can see exactly what the model
        asserted; it is replayable, so a run is reproducible without re-invoking a model;
        and it keeps the deterministic half deterministic -- identification never depends
        on a network call.

        EVERY FACT FROM HERE IS RECORDED AS `MODEL` PROVENANCE, never SOURCE. The document
        does not say these things. That distinction is the entire reason this framework
        tracks provenance at all, and collapsing it to make the fit number look better
        would defeat the purpose of having the number.
        """
        path = Path(str(self.idn.xml_path) + ".ai.json")
        if not path.is_file():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("elements") or {}

    def ai_for(self, el) -> dict:
        """The sidecar entry for an element, matched on its display name then its key."""
        if not self.ai:
            return {}
        for key in (self.element_name(el), getattr(el, "name", None), el.where):
            if key and key in self.ai:
                return self.ai[key]
        return {}

    # -- naming ------------------------------------------------------------

    def model_name(self, el) -> str:
        """FRAMEWORK CHANGE 20: modelName came from the element key, because in
        Informatica the key IS the human name. An SSIS component key is a
        backslash-delimited path (`Package\\Data Flow Task\\Derived Column`), so
        the naming source and whitespace handling must be table-driven.

        FRAMEWORK CHANGE 57: a model name had no notion of the scope it lives in.
        On DataStage that was a MEASURED data-loss defect, not a hazard: one .dsx
        holds 12 jobs, stage display names repeat across them, and 29 data-flow
        nodes collapsed onto 9 names. `DbtModelsWriter` wraps its write in
        try/catch and only logs, so 20 models were silently overwritten -- and the
        SQLite-backed ObjectReferences calculator deduplicated the same collision
        down to 6 of 18 lineage rows. `qualify_with_container` prefixes the
        enclosing element's name, which is the only scope the DOCUMENT states."""
        np = self.table["naming_policy"]
        name = el.display_name if np.get("name_from") == "DISPLAY_NAME" else el.instance_name
        qualify = np.get("qualify_with_container")
        if qualify and el.container:
            # The container's own name, normalised the same way, so the two halves
            # of the qualified name cannot disagree about case or whitespace.
            name = qualify["separator"].join([self._normalise(el.container, np),
                                              self._normalise(name, np)])
            return name
        return self._normalise(name, np)

    @staticmethod
    def _normalise(name: str, np: dict) -> str:
        if np["lowercase"]:
            name = name.lower()
        sep = np.get("replace_whitespace_with")
        if sep is not None:
            name = sep.join(name.split())
        return Emitter._sanitise(name, np)

    @staticmethod
    def _sanitise(name: str, np: dict) -> str:
        """FRAMEWORK CHANGE 58: whitespace was the only illegal character handled.

        MEASURED on Pentaho: the step `Dummy (do nothing)` produced the model name
        `dummy_(do_nothing)` and the transformation `safe-stop-gen-rows` kept its
        hyphens. Neither is a legal UNQUOTED Snowflake or dbt identifier, so both
        emit a model reference that does not compile.

        Every character outside the table's declared allowed set becomes ONE
        replacement character -- deliberately not a collapsed run, because
        collapsing merges `a--b` into `a_b` and merging two distinct names is the
        exact defect FRAMEWORK CHANGE 57 removed. A name that cannot START a bare
        identifier is PREFIXED rather than trimmed, for the same reason: prefixing
        is injective, trimming is not.

        Residual merges are still possible in principle (`a-b` and `a_b` both map to
        `a_b`), so this rule is NOT trusted on its own -- `emit` asserts injectivity
        over the whole document and fails loudly if two names collapse into one.
        """
        rule = np.get("sanitize_identifier")
        if not rule:
            return name
        allowed = set(rule["allowed_chars"])
        repl = rule["replace_illegal_with"]
        out = "".join(c if c in allowed else repl for c in name)
        if out and out[0] not in set(rule["allowed_leading_chars"]):
            out = rule["leading_prefix"] + out
        return out

    def node_type_of(self, el, role_prov: str) -> tuple[str, str, str]:
        """FRAMEWORK CHANGE 51: the role -> node.type lookup, made total.

        Returns (node_type, provenance, detail). A role the table maps keeps the
        provenance the caller computed (TABLE, or DERIVED when the role itself was
        derived from structure). A role the table does NOT map returns the declared
        placeholder with provenance MISSING, so `fit.score` counts the obligation
        and scores it zero -- the same treatment an unmapped element KIND gets. The
        emitter no longer decides anything here; the table does."""
        rmap = self.table["role_to_node_type"]
        if el.role in rmap:
            return rmap[el.role], role_prov, f"{el.role} -> {rmap[el.role]}"
        placeholder = rmap.get("unmapped_role_node_type")
        if placeholder is None:
            raise KeyError(
                f"role_to_node_type has no entry for role {el.role!r} and no "
                "'unmapped_role_node_type' fallback. Add the role, or declare the "
                "fallback -- the emitter will not choose a node type itself.")
        return placeholder, MISSING, (
            f"{el.role} -> {placeholder}: role_to_node_type states no mapping for "
            f"'{el.role}', so node.type asserts nothing")

    def is_orchestration_container(self, el) -> bool:
        """True when the table names this kind as a container, not a data-flow gap."""
        entry = self.table.get("kind_dispatch", {}).get(el.kind_raw)
        if isinstance(entry, dict) and entry.get("ir_kind") is None and not entry.get("degrade_to"):
            return True
        return (el.role or "").upper() in CONTAINER_ROLES

    def element_name(self, el) -> str:
        return (el.display_name if self.table["naming_policy"].get("element_name_from")
                == "DISPLAY_NAME" else el.instance_name)

    def ir_element_name(self, el) -> str:
        """element.Name as it reaches the IR/engine, not as a display label: engine
        translators print this value as a bare SQL correlation name (e.g.
        FilterTranslator's incoming-entity alias), so a platform whose element_name is
        not already a legal identifier (naming_policy.sanitize_element_name) gets it run
        through the same sanitize_identifier rule as model_name. ai_for()'s sidecar
        lookup keeps using the raw element_name() -- this helper is IR-assignment only."""
        name = self.element_name(el)
        np = self.table["naming_policy"]
        return self._normalise(name, np) if np.get("sanitize_element_name") else name

    # -- port classification ----------------------------------------------

    def is_output(self, p: Port) -> bool:
        return p.porttype in self.pol["output_porttypes"]

    def is_input(self, p: Port) -> bool:
        return p.porttype in self.pol["input_porttypes"]

    def is_local(self, p: Port) -> bool:
        return p.porttype == self.pol["local_variable_porttype"]

    # -- FRAMEWORK CHANGE 66 (b): WHERE InputColumns COME FROM ---------------

    def _input_columns_policy(self) -> str:
        """The table's declared mechanism for the RECEIVING column list.

        Defaulted to FIELD_EDGES so a table that says nothing keeps the
        pre-change behaviour byte-for-byte, and an undeclared value RAISES rather
        than silently emitting nothing -- the direction this framework must never
        fail in.
        """
        mech = self.pol.get("input_columns_from", "FIELD_EDGES")
        if mech not in ("FIELD_EDGES", "INPUT_PORTS", "NONE"):
            raise ValueError(
                f"port_policy.input_columns_from {mech!r} is not implemented. "
                "Declared mechanisms are FIELD_EDGES, INPUT_PORTS and NONE.")
        return mech

    def input_columns(self, name: str, el, by_lower: dict) -> list[dict]:
        """InputColumns, by the mechanism the PLATFORM declares.

        MEASURED DEFECT THIS FIXES. This was unconditionally FIELD_EDGES -- the
        list was built by walking inbound field-level lineage and reading the local
        port each edge lands on. Informatica states field lineage (CONNECTOR names
        both fields) and SSIS states it (an inputColumn carries the upstream
        outputColumn's lineageId), so on those two platforms it is right. A .dsx
        states NO field-level lineage at all: a link record names its Partner pin
        and nothing finer. So `idn.field_edges` is 0 on DataStage and
        `InputColumns` was structurally EMPTY on every element of every .dsx --
        29 of 29 nodes on MaskDemo.dsx, 4 of 4 on CustomerSummaryDerive.dsx.

        WHY THAT MATTERED EVEN THOUGH TRANSLATORS PROJECT FROM OutputColumns. Any
        verification that reads InputColumns read an empty list on this platform
        and passed, so the DataStage column check was weaker than it looked while
        appearing to pass -- the failure mode this whole spike exists to surface.

        THE EVIDENCE FOR INPUT_PORTS, and it is what decided this rather than
        declaring the field not-applicable. CustomerSummaryDerive.dsx STATES the
        receiving column list, on the element's own INPUT LINK RECORD, with a
        citable location for each column:
            V0S2P1 (CTrxInput)  FirstName, MiddleName, LastName, BirthDate
            V0S3P1 (CustomInput) FullName, BirthYear
            V0S4P1 (CustomInput) FullName, BirthYear
        The framework ALREADY READS all eight as INPUT ports -- `structure`
        declares three input port sites -- and the emitter then discarded every one
        of them because no field edge pointed at them. So this is not new data and
        not a derivation: it is a reading the producer was already making and
        throwing away. Provenance stays SOURCE for exactly that reason, cited at
        the column subrecord.

        NONE is declared where the platform states neither: a Kettle <hop> names
        two steps and no fields (a step's own <fields> are its OUTPUT schema), and
        an ADF dependsOn is orchestration order over activities that state no
        columns anywhere. Both measure 0 field edges AND 0 input ports today, so
        NONE is byte-identical for them -- it is declared to make the
        not-applicability a reviewable table entry instead of an accident of the
        algorithm.

        The `element.InputColumns` MISSING obligation is NOT retired by any of
        this. Where it fires it states a fact about the DOCUMENT -- a link in this
        direction and no column list on it -- and that fact is unchanged.
        """
        mech = self._input_columns_policy()
        inputs: list[dict] = []
        if mech == "NONE":
            return inputs
        if mech == "INPUT_PORTS":
            for p in el.ports:
                if not self.is_input(p) or self.is_local(p):
                    continue
                if self.excluded_group(el, p):
                    continue
                inputs.append(self.column_json(p, p.name, None))
                self.record_column_slots(
                    name, f"element.InputColumns[{len(inputs) - 1}]", p, None)
            return inputs
        for fe in self.idn.inbound(name):
            local = by_lower.get(fe.to_field.lower())
            if local is None:
                continue
            upstream_named = self.pol["input_column_naming"] == "UPSTREAM_FIELD"
            col_name = fe.from_field if upstream_named else local.name
            inputs.append(self.column_json(local, col_name, None))
            # INDEX FROM `inputs`, NOT FROM enumerate(inbound). The loop used
            # `enumerate`, so every field edge whose `to_field` resolved to no local port
            # advanced the index while `inputs` did not -- and from that point on the slot
            # path `element.InputColumns[i]` addressed a DIFFERENT column of the emitted
            # IR than the one whose reading it recorded. Neither fixture exercises the
            # skip today (measured: the path set is unchanged by this fix), which is the
            # only reason it was never wrong in an artifact; it is still an address
            # computed from the wrong sequence.
            self.record_column_slots(
                name, f"element.InputColumns[{len(inputs) - 1}]", local, None,
                name_where=fe.from_field_where if upstream_named else None)
        return inputs

    def excluded_group(self, el, p: Port) -> bool:
        """FRAMEWORK CHANGE 21: v1 had no notion that some output groups are not
        part of the projection. Every SSIS component carries an error output whose
        columns (ErrorCode, ErrorColumn) must not become derived columns."""
        flag = self.pol.get("exclude_port_groups_with_flag")
        if not flag or p.group is None:
            return False
        g = next((g for g in el.groups if g["name"] == p.group), None)
        return bool(g and g["flags"].get(flag))

    # -- expression resolution --------------------------------------------

    def _scan(self, text):
        rd = self.syn.get("reference_delimiters")
        return scan(text, quotes=tuple(self.syn["string_quotes"]),
                    ref_delims=tuple(rd) if rd else None,
                    extra=self.syn.get("identifier_extra_chars", ""))

    def _normalize_expression_syntax(self, value: str) -> str:
        """Rewrite a platform expression into SQL-ish delimiters via expression_syntax.

        I-19/SNOW-3936576: Alteryx FilterConditions carry [Field] refs and double-quoted
        string literals. Reuses the SAME tokenizer `resolve()` already runs Formula
        expressions through, so we do not invent a second grammar here.
        """
        parts = []
        for kind, lex in self._scan(value):
            if kind == "ref":
                parts.append(f'"{lex}"')
            elif kind == "str":
                parts.append("'" + lex[1:-1].replace("'", "''") + "'")
            else:
                parts.append(lex)
        return "".join(parts)

    def _divergence(self, out: list[str]) -> str | None:
        """FRAMEWORK CHANGE 22: the divergent-operator check was a literal
        two-character lookback for '|'. Operator length is now table-driven, which
        is what lets SSIS flag its single-character '+' concatenation."""
        div = self.table["dialect"]["syntactically_identical_semantically_divergent"]
        for ln in self.table["dialect"].get("divergent_operator_lengths", [1, 2]):
            if len(out) >= ln:
                op = "".join(out[-ln:])
                if op in div:
                    return f"operator '{op}': {div[op]}"
        return None

    def resolve(self, el, p: Port, rename: dict[str, str],
                by_lower: dict[str, Port], connected_in: set[str],
                depth: int = 0) -> tuple[str, list[str], list[str]]:
        """Resolve column references to upstream projected names and inline local
        variables. Returns (text, residue_reasons, table_rules_applied)."""
        if p.expression is None:
            return p.name, [], []
        residue: list[str] = []
        rules: list[str] = []
        out: list[str] = []
        ci = self.syn.get("case_insensitive_resolution", True)
        for kind, lex in self._scan(p.expression):
            if kind == "ref":
                # A delimited reference addresses a column identity directly.
                up = self.idn._lineage_index.get(lex)
                if up is None:
                    out.append(lex)
                    residue.append(f"unresolved column reference '{lex}'")
                else:
                    out.append(up[1])
                    rules.append("lineage_reference_resolution")
                continue
            if kind != "ident":
                out.append(lex)
                d = self._divergence(out)
                if d:
                    residue.append(d)
                continue
            target = by_lower.get(lex.lower() if ci else lex)
            if target is None:
                out.append(lex)
                residue.append(f"unknown identifier '{lex}' (function or unresolved reference)")
                continue
            if self.is_local(target) and depth < 8:
                inner, r, tr = self.resolve(el, target, rename, by_lower, connected_in, depth + 1)
                out.append(f"({inner})")
                residue.extend(r)
                rules.extend(tr)
                rules.append("port_policy.inline_local_variables")
                continue
            if self.is_input(target):
                if target.name in rename:
                    out.append(rename[target.name])
                elif target.name not in connected_in and target.default_value:
                    dv = target.default_value
                    pfx = self.table["default_value_policy"]["error_function_prefix"]
                    if pfx and dv.startswith(pfx):
                        out.append(target.name)
                        residue.append(
                            f"unconnected input '{target.name}' with error-function default")
                    else:
                        out.append(dv)
                        rules.append(
                            "default_value_policy.literal_default_on_unconnected_input")
                else:
                    out.append(target.name)
            else:
                out.append(target.name)
        return "".join(out), residue, rules

    # -- columns -----------------------------------------------------------

    def column_json(self, p: Port, name: str, expr: str | None) -> dict:
        """FRAMEWORK CHANGE 23: Precision and Scale were emitted unconditionally
        because every Informatica port states both. SSIS states `length` for
        strings, `precision`/`scale` for numerics, and NOTHING for i4 or dbDate."""
        c: dict = {}
        if expr is not None:
            c["$kind"] = "ColumnExpression"
            c["Expression"] = expr
        c["Name"] = name
        c["DataType"] = p.datatype
        if p.precision is not None:
            c["Precision"] = p.precision
        if p.scale is not None and (self.pol["emit_scale_when_zero"] or p.scale):
            c["Scale"] = p.scale
        return c

    def record_column_slots(self, el_name: str, path: str, p: Port,
                            expr_prov: tuple[str, str, str] | None,
                            name_where: str | None = None) -> None:
        # FRAMEWORK CHANGE 51 (ARCHITECTURAL A6, all call sites in this file):
        # "/@" + attr became self.idn.attr_ref(node, attr). Three sites here, plus
        # node.id and element.Name in emit_node and the CHILD_ATTR rule in
        # record_no_slot_facts -- six in total, all under this number.
        # See Identification.attr_ref.
        #
        # FRAMEWORK CHANGE 63 (b): `name_where` OVERRIDES the citation for `.Name` ONLY.
        # An InputColumns entry takes its datatype, precision and scale from the LOCAL
        # port and its NAME from the UPSTREAM field (port_policy.input_column_naming =
        # UPSTREAM_FIELD on every table), so one `where` cannot be right for all four.
        # It was the local port's for all four, which is wrong exactly where a
        # transformation renames a port -- five citations on MappingForTest.XML, found by
        # the provenance audit the moment it could read an XML front-end at all. Passed
        # rather than inferred here, because only the caller knows which naming policy
        # produced the value.
        ref = self.idn.attr_ref
        self.slots.append(Slot(el_name, f"{path}.Name", SOURCE,
                               name_where if name_where
                               else p.where + ref(p.node, p.name_attr)))
        self.slots.append(Slot(el_name, f"{path}.DataType", SOURCE,
                               p.where + (ref(p.node, p.datatype_attr)
                                          if p.datatype_attr else "/@?")))
        for ir_field, val, attr in (("Precision", p.precision, p.precision_attr),
                                    ("Scale", p.scale, p.scale_attr)):
            if val is not None:
                self.slots.append(Slot(el_name, f"{path}.{ir_field}", SOURCE,
                                       p.where + ref(p.node, attr)))
            else:
                # The contract wants this field; the platform never states it for
                # this data type. v1 had no provenance value for that direction.
                self.slots.append(Slot(
                    el_name, f"{path}.{ir_field}", MISSING, p.where,
                    f"platform states no {ir_field.lower()} for type '{p.datatype}'"))
        if expr_prov is not None:
            prov, where, detail = expr_prov
            self.slots.append(Slot(el_name, f"{path}.Expression", prov, where, detail))

    # -- no-slot source facts ---------------------------------------------

    def record_no_slot_facts(self, el, promoted: frozenset = frozenset()) -> None:
        """FRAMEWORK CHANGE 24: this method WAS the Informatica fact list, in
        Python: it named 'Sql Query', 'Select Distinct', 'OUTPUT/DEFAULT',
        'ERROR(', REUSABLE, TARGETLOADORDER and the string 'SOURCE'/'TARGET'
        roles inline. It is now an interpreter over declarative rules.

        FRAMEWORK CHANGE 59 (ENG-014 spike): `promoted` names rule ids that the
        element's KIND can now hold as real IR fields, so they must not also be
        reported as NO_SLOT. The promotion itself happens in emit_node, which is
        where the kind is known; this method only has to stop double-counting.
        Passing an id that the table does not promote is a no-op, and passing one
        that IS promoted while emitting no slot for it would LOWER the obligation
        count instead of satisfying it -- so emit_node asserts it emitted one."""
        nd = self.table["neutral_defaults"]
        dvp = self.table["default_value_policy"]
        name = el.instance_name
        connected_in = {fe.to_field for fe in self.idn.inbound(name)}
        connected_out = {fe.from_field for fe in self.idn.outbound(name)}
        attr_tpl = (self.table["structure"].get("attr_where_template")
                    or "attribute[@name='{key}']")

        def add(rid, key, prov, where, detail=""):
            path = f"!{rid}[{key}]" if key is not None else f"!{rid}"
            # FRAMEWORK CHANGE 38: detail was always emitted whole, because in XML
            # a source fact is a short attribute value. A record-block value can be
            # an entire embedded document: the XMLProperties value on a DataStage
            # connector stage is a 4 KB XML blob holding the SELECT statement, the
            # table name and the write mode. Truncation is table-declared so the
            # limit is a reviewable policy rather than a magic number, and the
            # untruncated length is reported so nothing is silently shortened.
            lim = self.table["structure"].get("detail_max_chars")
            if lim and detail and len(detail) > lim:
                detail = f"{detail[:lim]}... [{len(detail)} chars total, truncated]"
            self.slots.append(Slot(name, path, prov, where, detail))

        for rule in self.table["no_slot_facts"]:
            if rule["id"] in promoted:
                continue
            src = rule["from"]
            prov = RESIDUE if rule.get("provenance") == "RESIDUE" else NO_SLOT
            sfx = rule.get("where_suffix", "")
            tpl = rule.get("detail", "")

            if src == "HARVEST":
                if el.harvested:
                    add(rule["id"], None, prov, el.harvested["where"],
                        tpl.format(**el.harvested))

            elif src == "ELEMENT_ATTR":
                v = el.table_attrs.get(rule["attr"])
                if v and v != nd.get(rule["attr"]):
                    # FRAMEWORK CHANGE 42 (call site): prefer the LOCATED where
                    # recorded while reading the attr site; fall back to the
                    # unlocated template only when the front-end supplies no
                    # location at all.
                    add(rule["id"], None, prov,
                        el.table_attr_where.get(rule["attr"])
                        or attr_tpl.format(key=rule["attr"]), v)

            elif src == "DEF_SITE_ATTR":
                # FRAMEWORK CHANGE 63 (a): declared here as well as in resolve_fact.
                # A rule kind implemented on only ONE of the two paths is how
                # `inf_filter_condition_UNREACHABLE` stayed invisible: a rule that
                # fires on an element the table did NOT promote it for must still
                # appear as an unmet obligation rather than vanish.
                v = el.table_attrs.get(rule["attr"])
                if v and v != nd.get(rule["attr"]):
                    add(rule["id"], None, prov, self.def_attr_where(el, rule["attr"]), v)

            elif src == "ATTR_RESIDUE":
                # FRAMEWORK CHANGE 68 (a) -- THE RESIDUAL PROPERTY SWEEP.
                #
                # THE DEFECT. Every other rule kind here is a WHITELIST: it names one
                # key, or one xpath, or one porttype. So a property the table does not
                # name is not reported as uncovered -- it is not reported at all. That
                # is the shape of the measured loss on CustomerSummaryDerive.dsx: V0S4
                # states `write_method "write"` (dsx:319-320) and `write_mode "append"`
                # (dsx:323-324), and neither reached the IR, nor a no_slot fact, nor any
                # residue line. A mart materialized as a table REPLACES its rows every
                # run while the document says APPEND, so from run 2 the migration and the
                # original disagree about the target's contents with nothing saying so.
                # The same hole on SSIS swallows `FastLoadKeepNulls false` (dtsx:439-442),
                # whose own @description states that a NULL arriving from the pipeline
                # inserts the destination column's DEFAULT instead of NULL.
                #
                # THIS RULE IS THE COMPLEMENT, not another whitelist: every key in the
                # element's declared property bag that no OTHER rule in this table reads
                # and whose value is not the table's declared neutral default. A property
                # name nobody has thought of yet is therefore reported BY CONSTRUCTION,
                # which is the only form that cannot go quiet on the next document.
                #
                # SUPPRESSION IS `neutral_defaults` AND NOTHING ELSE. There is no
                # per-rule ignore list, deliberately: a curated list of "properties that
                # do not matter" is exactly what the coarse census exclusion was, and it
                # is what swallowed write_mode. `neutral_defaults` is the one declared,
                # reviewable, per-key knob, and it may only be used where the value is a
                # VERIFIED vendor default carrying no design intent. NOTE THE TRAP, which
                # is why that wording is narrow: FastLoadKeepNulls's material value IS
                # its default (false), so "equals the vendor default" does NOT imply "no
                # design intent" and that key must never be declared neutral.
                keys_read = self._attr_keys_read_by_rule()
                for key in sorted(el.table_attrs):
                    if key in keys_read:
                        continue
                    v = el.table_attrs[key]
                    if not v or v == nd.get(key):
                        continue
                    add(rule["id"], key, prov,
                        el.table_attr_where.get(key) or attr_tpl.format(key=key), v)

            elif src == "GROUP":
                for g in el.groups:
                    if rule.get("when_type") is not None and g["type"] != rule["when_type"]:
                        continue
                    if rule.get("when_flag") and not g["flags"].get(rule["when_flag"]):
                        continue
                    if rule.get("requires") == "expression" and not g["expression"]:
                        continue
                    add(rule["id"], g["name"], prov, g["where"] + sfx,
                        tpl.format(**g) if tpl else "")

            elif src == "PORT":
                if el.role in rule.get("exclude_roles", []):
                    continue
                cls = rule.get("porttype_class")
                for p in el.ports:
                    if cls == "INPUT" and not self.is_input(p):
                        continue
                    if cls == "OUTPUT" and not self.is_output(p):
                        continue
                    if cls == "LOCAL" and not self.is_local(p):
                        continue
                    if rule.get("requires") == "default_value" and not p.default_value:
                        continue
                    # FRAMEWORK CHANGE 40: a new predicate, added because the
                    # fabrication bug the SSIS pass found inside the READER turns
                    # up on DataStage inside the SOURCE FORMAT. A .dsx column
                    # states Precision "0" and Scale "0" for a BIGINT
                    # (MaskDemo.dsx dsx:307-310), where 0 does not mean zero -- it
                    # means "not applicable to this type". Provenance cannot catch
                    # this: the value IS at that line, so SOURCE is truthful. Only
                    # a per-platform rule can say "this stated value is a
                    # placeholder", so the table states it and the cost is counted.
                    #
                    # FRAMEWORK CHANGE 52: the placeholder VALUE was hardcoded to 0
                    # by the predicate name `zero_precision`. Kettle's placeholder
                    # is -1, not 0: ValueMetaBase(name, type) delegates to
                    # this(name, type, -1, -1), so <length>-1</length> means "no
                    # length stated" and 0 would mean a real zero. Hardcoding 0
                    # would have silently reported every Kettle column as fine.
                    # The placeholder set is now table-declared.
                    if rule.get("requires") == "placeholder_precision":
                        if p.precision not in rule["placeholder_values"]:
                            continue
                    # FRAMEWORK CHANGE 53: a new predicate. Kettle's <type> inside
                    # <fields><field> is POLYSEMOUS ACROSS STEP TYPES: on a
                    # RowGenerator it is a real data type resolved through
                    # ValueMetaFactory.getIdForValueMeta, but on a SystemInfo step
                    # it is a SELECTOR naming which system value to emit
                    # ("transformation name", "kettle version") from the
                    # SystemDataTypes enum. Same element, same reader, different
                    # meaning. Provenance again cannot catch it -- the value IS at
                    # that line -- so the table declares the closed type
                    # vocabulary and anything outside it is counted as a cost.
                    if rule.get("requires") == "datatype_outside_vocabulary":
                        if p.datatype in rule["vocabulary"]:
                            continue
                    # FRAMEWORK CHANGE 55: a PORT rule could only be predicated on
                    # facts the framework already reads INTO a Port -- its default
                    # value, its precision, its connectivity. A per-column fact the
                    # framework does NOT read had no predicate at all, so a rule
                    # naming one fired on EVERY column.
                    #
                    # This was found as a live FABRICATION, not by inspection. The
                    # Kettle table declares a rule for <nullif>, a per-field null
                    # substitution with no IR slot. With no predicate it reported
                    # "field 'trans_name' declares a nullif substitution" for the
                    # two SystemInfo fields at sample_trans.ktr:92-99, which state
                    # no <nullif> element at all -- a fact present in the output and
                    # absent from the source, which is the exact bug class the SSIS
                    # precision default was. The predicate asks the port's own node.
                    if rule.get("requires") == "attr_present":
                        if p.node is None or not any(p.node.get(a) is not None
                                                     for a in rule["attrs"]):
                            continue
                    if rule.get("connectivity") == "UNCONNECTED":
                        pool = connected_in if cls == "INPUT" else connected_out
                        if p.name in pool:
                            continue
                    if rule.get("skip_excluded_groups") and self.excluded_group(el, p):
                        continue
                    disp = (dvp["discardable_label"]
                            if dvp["error_function_prefix"]
                            and p.default_value.startswith(dvp["error_function_prefix"])
                            else dvp["load_bearing_label"])
                    add(rule["id"], p.name, prov, p.where + sfx,
                        render_detail(rule, tpl, {
                            "default_value": p.default_value, "disposition": disp,
                            "name": p.name, "datatype": p.datatype,
                            "lineage": p.lineage, "group": p.group}))

            elif src == "FIELD_EDGE":
                for fe in self.idn.inbound(name):
                    if rule.get("when") == "RENAME" and fe.from_field == fe.to_field:
                        continue
                    add(rule["id"], fe.to_field, prov, fe.where + sfx,
                        render_detail(rule, tpl, {
                            "from_instance": fe.from_instance,
                            "from_field": fe.from_field, "to_field": fe.to_field}))

            elif src == "LOAD_ORDER":
                if el.load_order:
                    add(rule["id"], None, prov,
                        self.table["structure"]["load_order"]["xpath"] + sfx, el.load_order)

            elif src == "ELEMENT_FLAG":
                v = el.flags.get(rule["flag"])
                if v is not None and v != nd.get(rule["flag"]):
                    add(rule["id"], None, prov, el.where + sfx, v)

            elif src == "CONTAINER":
                if el.container:
                    add(rule["id"], None, prov, el.where,
                        render_detail(rule, tpl, {"container": el.container}))

            elif src == "CHILD_ATTR":
                # FRAMEWORK CHANGE 28: there was no rule kind for a fact carried
                # on a singleton CHILD element of the element. Informatica's
                # TABLEATTRIBUTE site covers name/value pairs only; an SSIS
                # <connection> is a child element with meaningful attributes.
                node = self.idn.node_of(el)
                for i, ch in enumerate(node.findall(rule["xpath"]), start=1):
                    v = ch.get(rule["attr"])
                    # FRAMEWORK CHANGE 56: every other rule kind checked the value
                    # against neutral_defaults before creating an obligation; this
                    # one never did, and no prior platform noticed because DataStage
                    # has exactly one CHILD_ATTR rule and no neutral default for it.
                    # Both new platforms are full of child-object defaults -- an ADF
                    # activity policy states retry 0 and retryIntervalInSeconds 30,
                    # which are Microsoft's DOCUMENTED defaults, and every Kettle
                    # step states partitioning method "none" -- so the missing check
                    # inflated NO_SLOT with facts carrying no design intent. Found by
                    # writing a neutral_defaults entry, watching the fact appear
                    # anyway, and reading the interpreter.
                    if v and v != nd.get(rule["attr"]):
                        add(rule["id"], ch.get(rule.get("key_attr") or rule["attr"]), prov,
                            f"{el.where}/{rule['xpath'].lstrip('./')}[{i}]"
                            + self.idn.attr_ref(ch, rule["attr"]), v)

            elif src == "CHILD_TEXT":
                # FRAMEWORK CHANGE 68 (c): declared in `resolve_fact` since FRAMEWORK
                # CHANGE 60 (c) and NEVER on this path -- found by the `else: raise`
                # below, not by inspection. This is the identical defect FRAMEWORK
                # CHANGE 63 (a) records for DEF_SITE_ATTR, one rule kind later: a kind
                # implemented on the PROMOTION path only fires for the kinds whose
                # `element_fields` name it, and on every other element it raised
                # nothing at all rather than an unmet obligation.
                #
                # MEASURED EXPOSURE ON THE CURRENT FIXTURES: nil. Both CHILD_TEXT rules
                # in platform_ssis.json are promoted by the only kinds whose documents
                # state the property (`oledb_open_rowset` by both OLE DB endpoints,
                # `cspl_friendly_expression` by Microsoft.ConditionalSplit), and no
                # other element in either .dtsx states either property -- so the census
                # had nothing to report and the hole was invisible. It would have opened
                # the moment a table declared a CHILD_TEXT rule it does not promote,
                # which is the ordinary case for every other rule kind here.
                node = self.idn.node_of(el)
                for i, ch in enumerate(node.findall(rule["xpath"]), start=1):
                    v = (ch.text or "").strip()
                    key = ch.get("name") or ch.tag
                    if v and v != nd.get(rule.get("neutral_key") or key, object()):
                        add(rule["id"], key, prov,
                            f"{el.where}/{rule['xpath'].lstrip('./')}[{i}]/text()", v)

            elif src == "CHILD_TEXT_TEMPLATE":
                # Declared on BOTH paths for the reason DEF_SITE_ATTR and CHILD_TEXT
                # already give: a rule fires here only for the kinds `element_fields`
                # names it for, and every other kind reading the same document shape
                # must still see an unmet obligation rather than silence.
                hit = self._resolve_child_text_template(el, rule)
                if hit is not None:
                    key, where, value = hit
                    add(rule["id"], key, prov, where, value)

            elif src == "NONE":
                # A DOCUMENTATION PSEUDO-RULE. platform_informatica.json's
                # `__comment__` entry carries the list's own rationale and reads
                # nothing. Named explicitly so the else below can raise.
                pass

            else:
                # FRAMEWORK CHANGE 68 (b): the chain used to fall off the end in
                # SILENCE. A rule whose `from` this interpreter does not implement --
                # a new kind added to a table before the interpreter, or a typo --
                # produced no fact and no error, which is indistinguishable from "the
                # document does not state it". That is the same closed-vocabulary
                # failure `_attach_definitions` raises on for an undeclared def-site
                # name and `resolve_fact` raises on for an unimplemented promotion;
                # this was the one remaining branch of the three that stayed quiet.
                raise ValueError(
                    f"no_slot_facts rule '{rule['id']}' declares from={src!r}, which "
                    f"record_no_slot_facts does not implement. A rule kind the census "
                    f"cannot read raises no obligation, which looks exactly like a fact "
                    f"the source does not state.")

    def _attr_keys_read_by_rule(self) -> frozenset:
        """Property-bag keys that some OTHER rule in this table already reads.

        Used only by ATTR_RESIDUE, which is the COMPLEMENT of this set. DERIVED from
        the rules rather than restated beside them, for the reason the
        `dsx-link-record` census exclusion gives for deriving itself from
        `edge_levels`: two hand-maintained lists of the same thing drift, and the
        drift shows up as a FALSE unmet obligation (the residual sweep re-reporting a
        key that a named rule already reports) or a FALSE silence.

        Two rule shapes name a bag key:
          ELEMENT_ATTR / DEF_SITE_ATTR -- `attr` IS the bag key.
          CHILD_ATTR / CHILD_TEXT      -- the key sits in the xpath's own predicate,
                                          `[@<name_attr>='KEY']`, where `name_attr`
                                          comes from the platform's declared
                                          `attr_site` and is never guessed here
                                          (`Name` on DataStage, `name` on SSIS,
                                          `NAME` on Informatica).
        A CHILD_* rule with no such predicate names no single key and contributes
        nothing -- correctly: it reads a site that is not the property bag."""
        at = self._attr_site()
        name_attr = (at or {}).get("name_attr") or "name"
        pat = re.compile(r"\[@" + re.escape(name_attr) + r"='([^']+)'\]")
        keys = set()
        for rule in self.table["no_slot_facts"]:
            src = rule.get("from")
            if src in ("ELEMENT_ATTR", "DEF_SITE_ATTR"):
                keys.add(rule["attr"])
            elif src in ("CHILD_ATTR", "CHILD_TEXT"):
                keys.update(pat.findall(rule.get("xpath", "")))
        return frozenset(keys)

    def _assert_attr_residue_usable(self) -> None:
        """Raise when an ATTR_RESIDUE rule cannot mean what it says.

        THREE WAYS IT CANNOT, each measured or reasoned rather than imagined:

        1. TWO SUCH RULES. The complement of one read-set is one obligation per
           unread key; two rules would raise every unread key twice and DOUBLE the
           cost of the same document fact.

        2. NO DECLARED `attr_site`. The bag is empty on every element, so the sweep
           reports nothing on a platform that may well state properties -- a gate
           incapable of firing, which this project has already found four of.
           platform_adf.json is the live case: its attr site is deliberately absent
           (an activity's own scalars are name/type/description and all three are
           already read), so it must not declare this rule.

        3. `value_from: SELF_ATTRS`. On Pentaho the bag is the STEP NODE's own
           attributes after the scalar lift, so it holds the element's IDENTITY --
           @name and @type -- beside its configuration. MEASURED: a residual sweep
           there reports `name` and `type` as unread residue on 4 of 4 elements of
           safe-stop-gen-rows.ktr, which is false twice over (both are read, and
           `name` IS the element key). Separating identity from configuration needs
           the level's key/kind/display/flag attributes excluded, which is a
           framework change this pass did not make; see the pentaho table's
           `residue.step_scalar_residue_not_swept` for the measured size of the
           family that is therefore still uncounted."""
        rules = [r for r in self.table["no_slot_facts"] if r.get("from") == "ATTR_RESIDUE"]
        if not rules:
            return
        if len(rules) > 1:
            raise ValueError(
                f"{len(rules)} ATTR_RESIDUE rules declared ({[r['id'] for r in rules]}). "
                f"ATTR_RESIDUE is the COMPLEMENT of every other rule's read set, so two "
                f"of them raise every unread property key twice.")
        at = self._attr_site()
        if at is None:
            raise ValueError(
                f"no_slot_facts rule '{rules[0]['id']}' is ATTR_RESIDUE and no def site "
                f"in this table declares an `attr_site`. The property bag is empty on "
                f"every element, so the sweep is a check that cannot fire.")
        if at.get("value_from") == "SELF_ATTRS":
            raise ValueError(
                f"no_slot_facts rule '{rules[0]['id']}' is ATTR_RESIDUE and the declared "
                f"attr_site reads value_from=SELF_ATTRS, so the bag holds the element's "
                f"own identity attributes beside its configuration. The sweep would "
                f"report the element key and kind as unread residue. Exclude the level's "
                f"key/kind/display/flag attributes first.")

    # -- FRAMEWORK CHANGE 59 (ENG-014 spike) ------------------------------

    def rule_by_id(self, rule_id: str) -> dict | None:
        for rule in self.table["no_slot_facts"]:
            if rule["id"] == rule_id:
                return rule
        return None

    def _resolve_child_text_template(self, el, rule: dict):
        """CHILD_TEXT_TEMPLATE -- a predicate assembled from SIBLING child-text
        facts, not read whole off one child.

        THE GAP THIS CLOSES. Alteryx's Filter states a Simple-mode condition as
        THREE separate children (`Simple/Field`, `Simple/Operator`,
        `Simple/Operands/Operand`) and no `<Expression>` text at all -- the shape
        `filter_expression` (CHILD_TEXT) reads for Custom mode. CHILD_TEXT cannot
        answer this: there is no single child whose whole text IS the predicate.

        Fires only when the rule's `templates` map has an entry for the read
        operator AND every placeholder that SPECIFIC template actually
        references is non-blank -- e.g. `IsNull` never looks at `operand`, so
        MEASURED junk left in that field by the Alteryx GUI (`<Operand>1</Operand>`
        on an IsNull condition) is correctly ignored rather than blocking the
        template. An operator the table does not map, or a referenced part left
        blank, returns None -- the same honest degrade every other rule kind here
        gives, never a hollow predicate."""
        node = self.idn.node_of(el)
        raw: dict[str, str] = {}
        where_of: dict[str, str] = {}
        for part, xpath in rule["parts"].items():
            ch = node.find(xpath)
            raw[part] = (ch.text or "").strip() if ch is not None else ""
            where_of[part] = f"{el.where}/{xpath.lstrip('./')}/text()"
        template = rule["templates"].get(raw.get("operator"))
        if template is None:
            return None
        needed = set(re.findall(r"\{(\w+)\}", template))
        if any(not raw.get(part) for part in needed):
            return None
        formatted = {
            part: (raw[part].replace("'", "''") if part == "operand"
                   else raw[part].replace('"', '""'))
            for part in needed
        }
        value = template.format(**formatted)
        cite_parts = ["field", "operator"] + (["operand"] if "operand" in needed else [])
        where = " + ".join(where_of[p] for p in cite_parts)
        return (raw.get("field"), where, value)

    def resolve_fact(self, el, rule_id: str):
        """Re-read a no_slot_facts rule as a POPULATED fact: (key, where, value).

        Returns None when the rule does not fire on this element, which is not an
        error -- adf_First_Pipeline.json's Copy states no storeSettings, so a
        promoted slot for one must simply not appear rather than appear empty.

        Only the rule kinds a promotion currently needs are implemented, and an
        unimplemented kind RAISES rather than returning None. Returning None would
        make a table typo look like 'the source does not state it', which is the
        fabrication direction this framework exists to prevent."""
        rule = self.rule_by_id(rule_id)
        if rule is None:
            raise ValueError(f"promoted fact '{rule_id}' is not a no_slot_facts rule")

        nd = self.table["neutral_defaults"]
        src = rule["from"]

        if src == "CHILD_ATTR":
            node = self.idn.node_of(el)
            for i, ch in enumerate(node.findall(rule["xpath"]), start=1):
                v = ch.get(rule["attr"])
                if v and v != nd.get(rule["attr"]):
                    where = (f"{el.where}/{rule['xpath'].lstrip('./')}[{i}]"
                             + self.idn.attr_ref(ch, rule["attr"]))
                    return (ch.get(rule.get("key_attr") or rule["attr"]), where, v)
            return None

        if src == "CONTAINER":
            if el.container:
                return (None, el.where, el.container)
            return None

        # FRAMEWORK CHANGE 65 (a): HARVEST -- the value is one named part of a
        # DEF-SITE HARVEST, i.e. of a definition the element only REFERENCES.
        #
        # THE GAP THIS CLOSES. Informatica states the physical source table on a
        # separate <SOURCE> definition; `collapse` absorbs it into the Source
        # Qualifier that names it as its ASSOCIATED_SOURCE_INSTANCE and carries the
        # harvest across (identify.py:986). The census could already report the
        # harvest as a NO_SLOT fact, and `resolve_fact` could not read it at all --
        # so the one platform whose document actually STATES the source table could
        # not put it in the IR, and its staging model came out with a bare `FROM`.
        #
        # `harvest_key` names WHICH part is the field, because a harvest is a tuple:
        # {database, schema, table, database_type}. Reading the whole dict would
        # force this method to decide which part is the table name, which is a
        # platform fact and belongs in the table.
        if src == "HARVEST":
            key = rule.get("harvest_key")
            if key is None:
                raise ValueError(
                    f"no_slot_facts rule '{rule_id}' is a HARVEST and states no "
                    "harvest_key, so there is no way to know which part of the "
                    "harvested tuple the IR field wants")
            v = el.harvested.get(key)
            if v and v != nd.get(key):
                return (key, el.harvested.get("where", el.where), v)
            return None

        # FRAMEWORK CHANGE 60 (c): two further rule kinds, added because the payload a
        # widened element kind needs is often NOT an attribute on a child.
        #
        # CHILD_TEXT -- the value is a child element's TEXT. This is how SSIS states
        # nearly everything interesting: a Conditional Split's predicate is the text of
        # <property name="FriendlyExpression">, and a destination's table is the text of
        # <property name="OpenRowset">. CHILD_ATTR structurally cannot read either.
        if src == "CHILD_TEXT":
            node = self.idn.node_of(el)
            for i, ch in enumerate(node.findall(rule["xpath"]), start=1):
                v = (ch.text or "").strip()
                if v and v != nd.get(rule.get("neutral_key") or "", object()):
                    where = f"{el.where}/{rule['xpath'].lstrip('./')}[{i}]/text()"
                    return (ch.get("name") or ch.tag, where, v)
            return None

        if src == "CHILD_TEXT_TEMPLATE":
            return self._resolve_child_text_template(el, rule)

        # ELEMENT_ATTR -- the value is an attribute on the element's OWN node. Already
        # a declared rule kind used by the NO_SLOT census, but never implemented here,
        # so promoting one raised. Informatica's target names its table in the
        # INSTANCE's own @NAME, and Pentaho's projection lifts leaf child elements to
        # attributes, so several platforms need exactly this and nothing more.
        if src == "ELEMENT_ATTR":
            node = self.idn.node_of(el)
            v = node.get(rule["attr"])
            if v and v != nd.get(rule["attr"]):
                return (rule["attr"], el.where + self.idn.attr_ref(node, rule["attr"]), v)
            return None

        # FRAMEWORK CHANGE 63 (a): DEF_SITE_ATTR -- the value is a named property of
        # the element's DEFINITION, not of the node the element sweep matched.
        #
        # THE GAP THIS CLOSES, exactly. Informatica states a Filter's predicate on the
        # resolved TRANSFORMATION as a property of the def-site property bag, while
        # node_of() returns the INSTANCE. None of CHILD_ATTR / CHILD_TEXT /
        # ELEMENT_ATTR / CONTAINER can cross that reference: all four query the
        # instance node. The platform table declared the field required and pointed it
        # at a rule named `..._UNREACHABLE`, so every Filter degraded to
        # UnsupportedTransformation with an EWI -- an honest encoding of a gap that was
        # never actually unreachable.
        #
        # WHY IT READS THE PROPERTY BAG RATHER THAN RE-QUERYING THE DEF NODE. The bag
        # is populated by _read_table_attrs FROM that node, under the site's own
        # table-declared attr_site -- child name/value pairs on one platform, the
        # node's own attributes on another. Re-querying here would duplicate that
        # projection and would have to name a shape, which is precisely the
        # per-platform assumption this file must not contain. The bag's contents
        # therefore follow `def_site` automatically: SELF means the element's own node,
        # a named site means the definition it references.
        #
        # NOT folded into ELEMENT_ATTR even though the NO_SLOT census's ELEMENT_ATTR
        # branch reads the same bag. The two branches of ELEMENT_ATTR already disagree
        # -- the census reads el.table_attrs, this method reads the instance node's own
        # attributes -- and an Informatica Target's TableName depends on the second
        # meaning. Overloading the name a third time would make a rule's behaviour
        # depend on which code path reached it.
        if src == "DEF_SITE_ATTR":
            v = el.table_attrs.get(rule["attr"])
            if v and v != nd.get(rule["attr"]):
                return (rule["attr"], self.def_attr_where(el, rule["attr"]), v)
            return None

        raise ValueError(f"promotion is not implemented for rule kind '{src}'")

    def def_attr_where(self, el, key: str) -> str:
        """Citation for a def-site property.

        Prefers the LOCATED where the front-end recorded while reading the attr site
        (FRAMEWORK CHANGE 42). The fallback is anchored at the def query rather than
        left as a bare relative template, because an unanchored
        `TABLEATTRIBUTE[@NAME='x']/@VALUE` is true of every definition in the file
        and so is not a citation at all."""
        located = el.table_attr_where.get(key)
        if located:
            return located
        tpl = self.table["structure"].get("attr_where_template")
        rel = tpl.format(key=key) if tpl else "@" + key
        return f"{el.def_where}/{rel}" if el.def_where else rel

    # -- FRAMEWORK CHANGE 63 (b): THE PLACEHOLDER CARRIES THE SOURCE BODY --------

    #: Jinja delimiters. dbt renders Jinja BEFORE any SQL parser sees the file, and
    #: Jinja does not respect SQL comments -- a `{{` inside a `--` line is still a
    #: template expression, and an unbalanced one fails the whole model. So these
    #: are the only sequences that have to be neutralised for a fragment to be safe
    #: inside generated SQL.
    _JINJA_ESCAPES = (("{{", "{ {"), ("}}", "} }"), ("{%", "{ %"), ("%}", "% }"),
                      ("{#", "{ #"), ("#}", "# }"))

    def unsupported_body(self, el) -> str | None:
        """The element's own source fragment, made safe to sit inside a SQL comment.

        WHY THE PLACEHOLDER NEEDED THIS. `_unsupported` carried the native kind NAME
        and nothing else, so the whole of a degraded element rendered as one line --
        `--CTransformerStage`. That names WHAT failed and states nothing about what
        was lost. Vanilla SnowConvert's not-supported path emits the original element
        commented out (see UnsupportedTransformationConfigurator.GetCommentText), and
        that is strictly more useful to both readers of the file: a human recovering
        the logic by hand, and a tier-3 model asked to replace the model it is
        reading.

        THREE PROPERTIES THIS GUARANTEES, each because the alternative was measured
        or is a known hazard:

        1. NEWLINES ARE PRESERVED, not stripped. The engine's own
           UnsupportedTransformationComments.WithSourceText splits on CRLF/CR/LF and
           emits ONE line comment per line, so a multi-line fragment renders as a
           block of `--` lines and no embedded newline ever reaches a comment node.
        2. JINJA DELIMITERS ARE NEUTRALISED. See _JINJA_ESCAPES: a SQL comment does
           not protect a `{{` from dbt's renderer, which runs first. Every escape is
           ANNOUNCED in the body, so the fragment never claims to be verbatim when
           it is not. UNVERIFIED on the current fixtures: MEASURED 0 delimiters over
           the 27 fragments the five platform tables produce across every fixture in
           runall.py plus the four blind inputs, so this path is implemented and
           unexercised. Kept anyway: an ADF pipeline expression is
           `@{concat(...)}` and an SSIS property can hold arbitrary text, so the
           first source document that carries one must not be the thing that
           discovers dbt renders comments.
        3. THE LENGTH IS CAPPED BY THE PLATFORM TABLE and the cut is ANNOUNCED. A
           DataStage connector stage carries a 4 KB XMLProperties blob and a job
           record can be the whole export; an uncapped body would turn a placeholder
           into a copy of the source file. `structure.unsupported_body_max_chars` is
           policy, declared per platform, for the same reason detail_max_chars is.

        DELIBERATELY NOT RECORDED AS A SLOT. An element's whole source text is not an
        obligation the contract has a field for, and adding it as NO_SLOT would put a
        term in every degraded element's fit DENOMINATOR -- lowering the score of
        five platforms to report an improvement in the artifact. The fit number
        measures representation, and this is a comment.

        Returns None when the front-end supplies no fragment, which the caller must
        keep distinguishable from an empty one -- the field is then simply absent and
        the consumer falls back to the kind name.
        """
        raw = self.idn.source_text(el)
        if not raw or not raw.strip():
            return None
        body = raw.replace("\r\n", "\n").replace("\r", "\n")
        escaped = 0
        for bad, safe in self._JINJA_ESCAPES:
            if bad in body:
                escaped += body.count(bad)
                body = body.replace(bad, safe)
        if escaped:
            body += (f"\n... [{escaped} Jinja delimiter(s) in the source were spaced "
                     f"apart above so dbt's renderer cannot read them as template "
                     f"syntax; this fragment is NOT verbatim] ...")
        lim = self.table["structure"].get("unsupported_body_max_chars")
        if lim and len(body) > lim:
            body = body[:lim].rstrip() + (
                f"\n... [source fragment truncated at {lim} of {len(body)} chars by "
                f"structure.unsupported_body_max_chars] ...")
        return body

    def promote_containment(self, node: dict, name: str, el) -> set:
        """FRAMEWORK CHANGE 59 (b) (ENG-001 spike).

        Runs for EVERY element, supported or not. Containment is orthogonal to
        whether the element's kind is representable: the ADF notebook and validation
        activities are unsupported and still live inside a pipeline, and the DataStage
        fixture's 31 non-job elements were unrepresentable on exactly this fact. Only
        promoting it for supported elements would close the gap where it costs least
        and leave it open where it was found."""
        promoted = set()
        for ir_field, rule_id in (self.table.get("containment_slots") or {}).items():
            hit = self.resolve_fact(el, rule_id)
            promoted.add(rule_id)
            if hit is None:
                continue
            _key, where, value = hit
            node.setdefault("container", {})[ir_field] = value
            self.slots.append(Slot(name, f"node.container.{ir_field}",
                                   SOURCE, where, value))
        return promoted

    # -- the graph ---------------------------------------------------------

    def _assert_model_names_injective(self, nodes: list[dict]) -> None:
        """FRAMEWORK CHANGE 58 (gate). Two distinct elements must never share a
        model name.

        This is a LOUD failure rather than a recorded gap, and the asymmetry is
        deliberate. A missing field costs one obligation and is visible in the fit
        score; two elements sharing a model name costs a whole MODEL and is visible
        nowhere -- `DbtModelsWriter` writes `{model.Name}.sql` with `WriteAllText`
        and logs `Successfully wrote model` for each one, so the last write wins and
        every line of the log says it worked. Measured before qualification: 29
        DataStage models became 9 files, and the same collision independently
        reduced 18 lineage rows to 6.

        Raising here also stops the two naming rules from silently undoing each
        other: qualification makes names unique and sanitisation could merge them
        again (`a-b` and `a_b` both become `a_b`)."""
        seen: dict[str, str] = {}
        for node in nodes:
            name = node["modelName"]
            if name in seen:
                raise ValueError(
                    f"naming_policy '{self.table['naming_policy']['policy_id']}' maps two distinct "
                    f"elements to one model name {name!r}: {seen[name]!r} and {node['id']!r}. "
                    "The dbt writer would overwrite one with the other and report success for both. "
                    "Widen the scope (qualify_with_container) or change the sanitisation rule -- do "
                    "not add a counter, which invents a name the document does not state.")
            seen[name] = node["id"]

    # -- column propagation ------------------------------------------------

    def _propagation_policy(self) -> dict:
        """The table's declared buffer semantics, defaulted to OFF.

        FRAMEWORK CHANGE 64 (a). A table that says nothing about propagation gets
        the pre-change behaviour byte-for-byte, so adding this section to one
        platform cannot move another.
        """
        pol = dict(self.table.get("column_propagation") or {})
        pol.setdefault("mode", "NONE")
        pol.setdefault("stop_at_kinds", [])
        pol.setdefault("stop_at_roles", [])
        pol.setdefault("algorithm_id", "predecessor_column_propagation.v1")
        if pol["mode"] not in ("NONE", "ACCUMULATE", "FILL_WHEN_UNDECLARED"):
            raise ValueError(
                f"column_propagation.mode {pol['mode']!r} is not implemented. "
                "Declared modes are NONE, ACCUMULATE and FILL_WHEN_UNDECLARED.")
        return pol

    def propagate_columns(self, nodes: list[dict]) -> None:
        """FRAMEWORK CHANGE 64: AN ELEMENT'S COLUMNS ARE NOT ONLY ITS OWN.

        WHAT WAS MISSING. Every column this producer emitted came from the
        element's OWN declarations. Nothing walked the graph, so an element that
        states no projection projected nothing, and an element that states only
        the columns it ADDS projected only those. Two measured defects were the
        same hole:

          * SSIS `CSPL Filter BirthYear` emitted InputColumns=['BirthYear'] and
            OutputColumns=[] while the synchronous buffer at that point carried
            six. Its model projected one column, so the downstream destination
            model referenced `FullName` -- absent upstream -- and the only
            correctly translated model in the tree became an orphan.
          * On DataStage, `GetSourceModelName(ctx, filter.OutputColumns, filter)`
            returns null when OutputColumns is empty, and `FilterTranslator`
            substitutes `NotFoundPlaceholder`. That is the literal cause of
            `{{ ref('int_NOT_FOUND') }}` and its dbt1005 -- an EMPTY COLUMN LIST
            breaking a MODEL REFERENCE, two floors away from where it was read.

        REFERENCE IMPLEMENTATION. `SsisProjectionContext.GetEffectiveOutputColumns`
        (Assemblies/EtlToDbt/DtsxSsis/SsisProjectionContext.cs:280) walks
        predecessor edges backwards accumulating each visited element's outputs and
        stops at elements that define their own output shape rather than passing
        input through. Its stop list is five SSIS componentClassIDs, so per this
        module's neutrality contract the list is TABLE-DECLARED here, on two axes:
        native kind (`stop_at_kinds`) and normalised role (`stop_at_roles`).

        TWO MODES, BECAUSE THE BUFFER RULE IS A PLATFORM FACT.
          ACCUMULATE -- a synchronous output carries the input buffer PLUS the
            columns the element declares. SSIS. Declaring only the new columns is
            the .dtsx's normal form, so a declared list is never exhaustive.
          FILL_WHEN_UNDECLARED -- a declared column list IS exhaustive, and only
            the absence of one means "whatever arrives here". DataStage states this
            outright (Runtime Column Propagation; `LinkHasMetaDatas "False| "`),
            and Informatica ports are explicit by construction.
        A table that declares neither gets NONE and is untouched.

        DELIBERATE DEVIATIONS FROM THE REFERENCE, both widenings:
          1. The engine follows `Edges.FirstOrDefault(x => x.To == node)` -- ONE
             predecessor. This unions ALL of them in edge order and dedupes by
             folded name, because a two-input element whose kind is not in the stop
             list would otherwise silently see half its buffer.
          2. Accumulated columns are ordered UPSTREAM-FIRST rather than self-first.
             The engine's list is consumed as a lookup set; ours becomes a SELECT
             list, and buffer order is the order the rows actually carry.

        PROVENANCE. A propagated column is NOT recorded as SOURCE. It is not read
        from the document at this element -- there is no location to cite there --
        so it earns exactly one DERIVED slot per element naming the algorithm, the
        columns added and the element each came from. Recording them as SOURCE
        would have credited five platforms' fit scores with readings no query made.

        A NODE THE HYDRATOR DROPS IS A BARRIER, not a pipe. `$kind: null` keeps a
        node out of the graph and takes every edge touching it with it, so carrying
        a buffer through one would assert lineage the emitted graph does not have.
        """
        pol = self._propagation_policy()
        mode = pol["mode"]
        if mode == "NONE":
            return
        by_id = {n["id"]: n for n in nodes}
        stop_kinds = set(pol["stop_at_kinds"])
        stop_roles = set(pol["stop_at_roles"])
        preds: dict[str, list[str]] = {}
        for e in self.idn.element_edges():
            preds.setdefault(e["to"], []).append(e["from"])

        def declared(nid: str) -> list[dict] | None:
            """The node's own OutputColumns, or None when the node is a barrier."""
            node = by_id.get(nid)
            if node is None or node["element"].get("$kind") is None:
                return None
            return list(node["element"].get("OutputColumns") or [])

        def stops(nid: str) -> bool:
            el = self.idn.elements.get(nid)
            return el is not None and (el.kind_raw in stop_kinds
                                       or el.role in stop_roles)

        memo: dict[str, list[dict]] = {}

        def carried(c: dict) -> dict:
            """A column as it ARRIVES at a downstream element.

            THE EXPRESSION IS DROPPED, and this is a correctness rule rather than
            tidiness. `FullName` is a ColumnExpression at the Derived Column that
            declares it; one hop later it is an ordinary column OF THAT MODEL, and
            copying the expression down would make the next model RE-EVALUATE
            `FirstName || ' ' || MiddleName || ' ' || LastName` against a relation
            that already has FullName in it -- silently wrong wherever the operands
            are not also projected, and duplicated work where they are. The engine's
            own accumulator does exactly this: AddColumnsFromOutput
            (SsisProjectionContext.cs:434) builds a plain `Column` from the name and
            datatype and never a ColumnExpression. Caught by the emitter reporting
            the same expression rewritten TWICE for one declaration.
            """
            return {k: v for k, v in c.items()
                    if k not in ("$kind", "Expression")}

        def effective(nid: str, seen: frozenset) -> list[dict]:
            if nid in memo:
                return memo[nid]
            if nid in seen:
                return []                      # cycle guard: a loop carries nothing
            own = declared(nid)
            if own is None:
                return []                      # barrier
            if stops(nid) or (mode == "FILL_WHEN_UNDECLARED" and own):
                memo[nid] = own
                return own
            out, taken = [], set()
            for p in preds.get(nid, []):
                for c in effective(p, seen | {nid}):
                    key = c["Name"].lower()
                    if key not in taken:
                        taken.add(key)
                        out.append(carried(c))
            # The element's OWN declaration always wins on a name collision: it may
            # carry an expression, and the upstream copy never does.
            own_names = {c["Name"].lower() for c in own}
            out = [c for c in out if c["Name"].lower() not in own_names] + own
            memo[nid] = out
            return out

        for nid, node in by_id.items():
            own = declared(nid)
            if own is None or stops(nid):
                continue
            if mode == "FILL_WHEN_UNDECLARED" and own:
                continue
            eff = effective(nid, frozenset())
            added = [c for c in eff if c["Name"].lower()
                     not in {o["Name"].lower() for o in own}]
            if not added:
                continue
            node["element"]["OutputColumns"] = [dict(c) for c in eff]
            # FRAMEWORK CHANGE 64 (c): RENUMBER THE SLOT PATHS THIS INSERTION INVALIDATED.
            #
            # `eff` is prefix + own, with the element's OWN declarations LAST (see the
            # deviation note above: buffer order is the order the rows carry). So every
            # slot path recorded while reading the declarations -- `element.OutputColumns[0]`
            # for the first declared column -- now addresses a PROPAGATED column instead.
            #
            # MEASURED on DerivedColumn.dtsx before this fix, and it is a provenance record
            # pointing at the wrong field of the shipped IR, not a cosmetic index:
            #   slot element.OutputColumns[0].Name cites outputColumn[1][@name='FullName']
            #   emitted OutputColumns[0].Name is 'FirstName'   (FullName moved to [4])
            # Four such disagreements on that one document, invisible until the provenance
            # audit gained an XML locator. `len(added)` is exactly the prefix length,
            # because `added` IS the prefix: every propagated column is by construction one
            # whose folded name is not among `own`.
            shift = len(added)
            prefix = "element.OutputColumns["
            for s in self.slots:
                if s.element != nid or not s.path.startswith(prefix):
                    continue
                head, sep, tail = s.path[len(prefix):].partition("]")
                if sep and head.isdigit():
                    s.path = f"{prefix}{int(head) + shift}]{tail}"
            origin = ", ".join(sorted({p for p in preds.get(nid, [])})) or "<none>"
            self.slots.append(Slot(
                nid, f"element.OutputColumns[+{len(added)} propagated]", DERIVED,
                pol["algorithm_id"],
                (f"{mode}: this element declares NO projection, so the {len(added)} "
                 f"column(s) it carries "
                 if not own else
                 f"{mode}: the {len(own)} column(s) this element declares are not the "
                 f"whole buffer it carries; {len(added)} more ")
                + f"({', '.join(c['Name'] for c in added)}) reached it through "
                f"predecessor {origin} and are DERIVED from the graph, not read from "
                f"the document at this element"))
            # FRAMEWORK CHANGE 64 (b): the pre-existing MISSING obligation is KEPT.
            # `element.OutputColumns` MISSING states a fact about the DOCUMENT -- a
            # supported element with a link in this direction that declares no
            # projection -- and that fact is still true. Retiring it would have
            # turned every propagation into a free +1 and hidden the DataStage
            # measurement FRAMEWORK CHANGE 37 exists to surface (28 of 29 stages
            # carry no column metadata). Its detail line is amended instead, so a
            # reader cannot conclude the emitted model projects nothing.
            for s in self.slots:
                if (s.element == nid and s.path == "element.OutputColumns"
                        and s.provenance == MISSING):
                    s.detail += ("; the IR field IS populated, by "
                                 f"{pol['algorithm_id']} -- this obligation stays "
                                 "unmet because the DOCUMENT states no projection here")

    def emit(self) -> dict:
        nodes = [self.emit_node(n, el) for n, el in self.idn.elements.items()]
        self._assert_model_names_injective(nodes)
        self.propagate_columns(nodes)
        edges = []
        mech = self.table["edge_policy"]["element_edges_from"]
        derivation = ("EXPLICIT_EDGE_ELEMENT" if mech == "EXPLICIT_EDGE_ELEMENTS"
                      else self.table["edge_policy"]["collapse_connectors_by"])
        eprov = SOURCE if mech == "EXPLICIT_EDGE_ELEMENTS" else DERIVED
        for e in self.idn.element_edges():
            ej = {"from": e["from"], "to": e["to"]}
            if e["label"] is not None:
                ej["label"] = e["label"]
            edges.append(ej)
            where = e.get("where") or derivation
            for endpoint in ("from", "to"):
                self.slots.append(Slot("<edges>", f"edge[{e['from']}->{e['to']}].{endpoint}",
                                       eprov, where))
            if e["label"] is not None:
                self.slots.append(Slot("<edges>", f"edge[{e['from']}->{e['to']}].label",
                                       SOURCE,
                                       e.get("where")
                                       or self.table["edge_policy"]["label_source"]))
        # FRAMEWORK CHANGE 63: THE IR NOW STATES WHICH PLATFORM PRODUCED IT.
        #
        # WHY THIS FIELD EXISTS, and it is not metadata for a log line. `ShimSteps
        # .TranslateExpressions` in AiFirstSsisSemanticsShim.cs rewrites expression text with three
        # SSIS-dialect rules -- `[FUNC](` -> `FUNC(`, `"lit"` -> `'lit'`, and `+` -> `||` -- and
        # applied them to EVERY platform, because the shim was never told which platform produced the
        # IR. Its sibling SynthesizePassThrough was DELETED for exactly that (it fabricated four
        # columns on Informatica). This one was measured harmless only by fixture accident:
        # 0 rewrites on Informatica/DataStage/Pentaho/ADF and 2 and 1 on the two SSIS fixtures,
        # because those four fixtures happen to contain no double-quoted literal and no bracketed
        # function name. An Informatica expression containing a double-quoted literal -- legal, and
        # meaning a STRING in PowerCenter's expression language -- would be rewritten by a rule
        # written for another language.
        #
        # The previous pass declined to gate it because "gating it needs the platform identity to
        # cross the process boundary, which is an IR-schema change". We own this schema, so the
        # change is here: every platform_*.json already declares `platform`, and the value is copied
        # verbatim rather than derived, so a new table needs no code change to be gateable.
        #
        # NOT a node and not an edge: it is a property of the DOCUMENT, so it sits beside them. The
        # C# hydrator reads `nodes` and `edges` by name and ignores unknown root keys, which is why
        # this addition does not change a single hydrated graph.
        return {"platform": self.table["platform"], "nodes": nodes, "edges": edges}

    def emit_node(self, name: str, el) -> dict:
        # FRAMEWORK CHANGE 65: WHERE THE MODEL'S FINGERPRINTS GO INTO THE IR.
        #
        # Slots created between here and the return are this element's; the MODEL-provenance
        # ones among them are exactly the facts a model authored, and they are attached to the
        # node so the C# half can mark the ARTIFACT. Snapshotting the ledger rather than
        # instrumenting each site is deliberate: MODEL slots are appended in four places today
        # (element_fields escalation, sidecar $kind, its promoted fields, sidecar
        # OutputColumns) and a fifth would otherwise ship unmarked -- which is the defect
        # itself, one level up.
        _model_mark = len(self.slots)
        # FRAMEWORK CHANGE 32 (call site): ir_kind may depend on role as well as
        # native kind. See Identification.dispatch_for.
        dispatch = self.idn.dispatch_for(el)
        ir_kind = dispatch["ir_kind"]
        key_attr = self.idn.key_attr_of(el)

        # FRAMEWORK CHANGE 60: PAYLOAD-DEPENDENT KINDS, and the rule that a missing
        # payload DEGRADES rather than upgrades.
        #
        # Widening the hydrator past source-and-expression means some element kinds
        # carry a mandatory scalar: a FilterTransformation is meaningless without its
        # predicate, a TargetTransformation without its table name. `element_fields`
        # declares those, per kind, as {ir_field: {rule, required}} where `rule` is a
        # no_slot_facts id -- so the extraction is table-declared and cited, exactly
        # like external_io_slots, rather than hardcoded per platform in this emitter.
        #
        # WHY REQUIRED MEANS DEGRADE, NOT EMIT-EMPTY. This is a safety property, not
        # tidiness. FilterTranslator's shared base substitutes `WHERE TRUE` for an
        # empty predicate and records that only as a log warning. A filter that
        # silently becomes TRUE does not fail -- it returns EVERY ROW, and the model
        # looks like a clean migration. Degrading to UnsupportedTransformation instead
        # puts a blocking EWI in the artifact where a reviewer actually sees it.
        #
        # So an unextractable predicate must never become a FilterTransformation. The
        # decision belongs HERE and not in the hydrator: the hydrator throwing would
        # lose the whole document over one element, whereas the producer can degrade a
        # single node and keep the rest. The hydrator still throws if a producer
        # ignores this contract, which is the same treatment an unknown $kind gets.
        payload: dict = {}
        payload_missing: list[str] = []
        # FRAMEWORK CHANGE 68 (d): rule ids whose value actually REACHED `payload`, so
        # `record_no_slot_facts` can suppress them.
        #
        # THE DEFECT, and it is the one platform_ssis.json's `_element_fields_comment`
        # already describes -- found again, in the mechanism rather than in a table.
        # `external_io_slots` and `containment_slots` both add their rule ids to
        # `promoted`; `element_fields` NEVER DID. So a rule promoted into an IR field
        # was ALSO reported as a slotless NO_SLOT fact, citing the same location with
        # the same value, on an element whose IR field is SOURCE-populated from it. A
        # FALSE unmet obligation -- the one case where retiring an obligation is
        # correct, because the document states the fact and the IR carries it.
        #
        # WHY IT WAS INVISIBLE, per rule, because "no output changed" is what let it
        # sit: `oledb_open_rowset` and `cspl_friendly_expression` are CHILD_TEXT, a kind
        # the census did not implement until FRAMEWORK CHANGE 68 (c) -- so the duplicate
        # could not be raised. `inf_target_instance_name` is ELEMENT_ATTR @NAME and the
        # census's ELEMENT_ATTR branch reads the TABLEATTRIBUTE bag, which has no NAME
        # key. That left THREE rules where the duplicate was live and simply not on a
        # canonical fixture: `dsx_prop_table` / `dsx_prop_where` (MEASURED on
        # CustomerSummaryDerive.dsx: `!dsx_prop_table[table]` unmet on V0S1 and V0S4 and
        # `!dsx_prop_where[where]` unmet on V0S3, all three with element.TableName /
        # element.FilterConditions populated from the very same subrecord), and
        # `ktr_table_output_table` on the blind .ktr's TableOutput step. MaskDemo.dsx
        # contains no PxOdbc and no PxFilter and neither canonical .ktr contains a
        # TableOutput, which is the whole reason the canonical numbers never showed it.
        promoted_fields: set = set()
        for ir_field, fspec in (dispatch.get("element_fields") or {}).items():
            # `rule` may be a LIST of candidate ids, tried in table order, first
            # non-None hit wins -- Alteryx's FilterConditions needs this because
            # Custom mode states the whole predicate as one child's text
            # (`filter_expression`) while Simple mode states it as three sibling
            # facts assembled by a template (`filter_simple_predicate`); a single
            # id cannot name both readings of the same IR field.
            rule_ids = fspec["rule"] if isinstance(fspec["rule"], list) else [fspec["rule"]]
            hit = None
            fired_rule_id = None
            for rid in rule_ids:
                hit = self.resolve_fact(el, rid)
                if hit is not None:
                    fired_rule_id = rid
                    break
            if hit is None:
                if fspec.get("required"):
                    payload_missing.append(f"{ir_field} (rule {fspec['rule']})")
                continue
            _key, where, value = hit
            # FRAMEWORK CHANGE 60 (e): an optional table-declared normalisation.
            #
            # SSIS states a destination as `[dbo].[CUSTOMER_SUMMARY]` -- a QUALIFIED,
            # bracket-quoted name. Passing that straight through produced
            # `{{ config(alias='[dbo].[CUSTOMER_SUMMARY]') }}`, where real SnowConvert
            # emits `alias='CUSTOMER_SUMMARY'`. Brackets are not legal in an unquoted
            # Snowflake identifier, so the raw value is not merely ugly, it is wrong --
            # the same class as the Pentaho model-name finding, reached by another route.
            #
            # The transform is declared PER RULE in the table rather than inferred here,
            # because "which part of a qualified name is the table" is a platform fact.
            # Deliberately NOT trying to also populate SchemaName: `dbo` is a SQL Server
            # schema, and asserting it as the Snowflake target schema would state a
            # destination the migration has not actually decided. Dropping it leaves
            # TargetTranslatorBase's documented fallback in charge, which is honest.
            xf = fspec.get("transform")
            if isinstance(xf, dict):
                # A transform declared PER CANDIDATE RULE, not per field --
                # `filter_expression` states raw Alteryx expression syntax and
                # needs NORMALIZE_EXPRESSION_SYNTAX; `filter_simple_predicate`
                # already assembles final SQL and must not be re-lexed (its own
                # quoting would be misread as an Alteryx `[ref]`/`"literal"` pair
                # and mangled). A rule id absent from the map gets no transform.
                xf = xf.get(fired_rule_id)
            if xf == "UNQUALIFIED_TAIL":
                raw = value
                value = value.split(".")[-1].strip("[]`\"")
                if value != raw:
                    where += f"  [transform UNQUALIFIED_TAIL from {raw!r}]"
                    self.transformed_reads.append((ir_field, raw, value))
            elif xf == "NORMALIZE_EXPRESSION_SYNTAX":
                # I-19/SNOW-3936576: whole PREDICATE rewrite via _normalize_expression_syntax.
                raw = value
                value = self._normalize_expression_syntax(value)
                if value != raw:
                    where += f"  [transform NORMALIZE_EXPRESSION_SYNTAX from {raw!r}]"
                    self.transformed_reads.append((ir_field, raw, value))
            elif xf is not None:
                raise ValueError(f"element_fields transform '{xf}' is not implemented")
            payload[ir_field] = value
            # PARTIAL PROMOTIONS ARE NOT SUPPRESSED, and this exception is not a
            # special case so much as the definition of the rule kind. A HARVEST rule
            # with a `harvest_key` promotes ONE NAMED PART of a tuple while the census
            # branch reports the WHOLE tuple -- Informatica's
            # `source_table_qualification` promotes {table} into
            # SourceQualifier.TableName and its census detail says `mydb.dbo
            # qualification has no IR field`, which is a TRUE unmet obligation about
            # the database and schema that still have none. MEASURED: suppressing it
            # took MappingForTest.XML from 186/220 to 186/219 and SQ_EMPLOYEE from
            # 93.8% to 96.8% while nothing new had been read -- a fit rise bought by
            # deleting a real cost, which is the exact move this project forbids.
            rule = self.rule_by_id(fired_rule_id) or {}
            if not (rule.get("from") == "HARVEST" and rule.get("harvest_key")):
                promoted_fields.add(fired_rule_id)
            self.slots.append(Slot(name, f"element.{ir_field}", SOURCE, where, value))

        if ir_kind is not None and payload_missing:
            # FRAMEWORK CHANGE 61 (b): ESCALATE TO THE MODEL BEFORE DEGRADING.
            #
            # The previous rule went straight from "required payload missing" to
            # "degrade", which was half right. Emitting a hollow FilterTransformation is
            # genuinely unsafe -- an empty predicate becomes WHERE TRUE and silently
            # returns every row. But degrading is not the only alternative, and treating
            # it as such is what made "nothing" the normal output. A predicate no rule
            # kind can scrape is exactly the kind of thing a model CAN read.
            #
            # So the order is: deterministic rule -> model -> degrade. Degradation is now
            # the third answer rather than the second.
            supplied = self.ai_for(el)
            still_missing = []
            for entry in payload_missing:
                field = entry.split(" ")[0]
                if field in supplied and not field.startswith("_"):
                    payload[field] = supplied[field]
                    self.slots.append(Slot(
                        name, f"element.{field}", MODEL, f"sidecar:{field}",
                        f"{supplied[field]!r} -- no deterministic rule could read this; "
                        f"authored by a model, NOT read from the document"))
                else:
                    still_missing.append(entry)
            payload_missing = still_missing

        if ir_kind is not None and payload_missing:
            # Record the refusal as its own obligation so the fit number reflects that
            # a representable kind was DECLINED, not that the element was never seen.
            self.slots.append(Slot(
                name, "element.$kind", MISSING, "element_fields",
                f"'{el.kind_raw}' maps to {ir_kind}, but required payload did not "
                f"resolve deterministically OR from the model sidecar: "
                f"{', '.join(payload_missing)}. Degrading rather than emitting "
                f"a semantically hollow {ir_kind} -- an empty filter predicate becomes "
                f"WHERE TRUE downstream, which silently returns every row."))
            ir_kind = None
            payload = {}
            # The payload is DISCARDED here, so nothing was promoted after all and the
            # census must report every one of these facts again. Clearing this is the
            # difference between "the IR carries it" and "the IR was going to".
            promoted_fields.clear()

        # FRAMEWORK CHANGE 61 (c): THE MODEL MAY SUPPLY A KIND THE TABLE HAS NONE FOR.
        #
        # This is the case that produced literal zeros: Pentaho's Janino step and
        # DataStage's Transformer hold expressions in Java and DataStage BASIC, which no
        # engine translator lowers, so the table deliberately left them unmapped rather
        # than emit Java into a .sql file. Correct as far as it went -- and it left the
        # derive step of every such pipeline as a placeholder.
        #
        # A model CAN lower those. If it has, it says so here by naming the IR kind, and
        # the element rejoins the graph as a first-class node. The table's refusal stands
        # as the DEFAULT; the sidecar is what overrides it, per element, on the record.
        if ir_kind is None:
            supplied = self.ai_for(el)
            if supplied.get("$kind"):
                # FRAMEWORK CHANGE 66: refuse a kind the hydrator would throw on, and
                # DEGRADE this element instead of losing the document. See
                # HYDRATOR_KIND_CONTRACT for why the blast radius makes this worth a
                # guard rather than an exception at hydration time.
                _claimed = supplied["$kind"]
                if _claimed not in HYDRATOR_KIND_CONTRACT:
                    self.slots.append(Slot(
                        name, "element.$kind", MISSING, "sidecar:$kind",
                        f"a model asserts '{_claimed}', which the hydrator's kind switch "
                        f"has no arm for, so promoting it would throw during hydration and "
                        f"lose the WHOLE document. Refused; this element degrades. Accepted "
                        f"kinds: {', '.join(sorted(HYDRATOR_KIND_CONTRACT))}"))
                else:
                    _absent = [f for f in HYDRATOR_KIND_CONTRACT[_claimed]
                               if not str(supplied.get(f) or "").strip()]
                    if _absent:
                        # The required-payload rule, on the sidecar path. A hollow
                        # FilterTransformation is the worse outcome even than degrading:
                        # `FilterTranslator` substitutes `WHERE TRUE` for an empty
                        # predicate and silently returns every row.
                        self.slots.append(Slot(
                            name, "element.$kind", MISSING, "sidecar:$kind",
                            f"a model asserts '{_claimed}' but supplies no "
                            f"{', '.join(_absent)}, which the hydrator reads with "
                            f"RequiredString; promoting it would throw and lose the WHOLE "
                            f"document. Refused; this element degrades."))
                    else:
                        ir_kind = _claimed
                if ir_kind is not None:
                    for _f, _v in supplied.items():
                        # `_`-prefixed keys are the sidecar's own documentation -- source
                        # expression, reasoning, flagged divergences. They are for a human
                        # reviewer, not IR fields, and promoting them put
                        # `_source_dialect` into an element the hydrator then had to ignore.
                        if _f.startswith("_") or _f in ("$kind", "OutputColumns", "ModelSql"):
                            continue
                        payload[_f] = _v
                        self.slots.append(Slot(name, f"element.{_f}", MODEL,
                                               f"sidecar:{_f}", str(_v)))
                    self.slots.append(Slot(
                        name, "element.$kind", MODEL, "sidecar:$kind",
                        f"'{el.kind_raw}' has no table ir_kind; a model asserts {ir_kind}. "
                        f"MODEL provenance, not TABLE -- the platform table still refuses "
                        f"this kind and that refusal is the default."))

        # FRAMEWORK CHANGE 44: node.id was always a single attribute reading. Under
        # key scoping it is COMPOSED from two readings -- the enclosing job's key
        # and the record's own -- by a named rule, so citing only the record's
        # attribute would understate it.
        ks = self.idn.struct.get("key_scope")
        if ks:
            self.slots.append(Slot(
                name, "node.id", DERIVED,
                el.where + self.idn.attr_ref(self.idn.node_of(el), key_attr),
                f"key_scope: @{ks['key_attr']} of the enclosing {ks['tag']} "
                f"+ '{ks['separator']}' + @{key_attr}"))
        else:
            self.slots.append(Slot(name, "node.id", SOURCE,
                                   el.where + self.idn.attr_ref(
                                       self.idn.node_of(el), key_attr)))
        # FRAMEWORK CHANGE 34 (call site) and FRAMEWORK CHANGE 41: the role is no
        # longer always an attribute. When it is DERIVED, the VALUE of node.type
        # and of element.$kind is decided by an algorithm over identified
        # structure and the table supplies only the mapping -- so recording them
        # as TABLE would credit the table with a reading it did not make. Both
        # DERIVED and TABLE count as satisfied, so the fit number is unchanged;
        # what changes is the provenance breakdown, which is the integrity
        # measure when there is no golden output to check against.
        role_derived = el.role_source.startswith("DERIVED")
        role_prov = DERIVED if role_derived else TABLE
        # FRAMEWORK CHANGE 51: `role_to_node_type[el.role]` was indexed directly, so
        # a role the table does not map did not degrade -- it CRASHED the emitter.
        # EXECUTED: InfPc/Registry/MappletPart/mapplet_part.xml raises
        # `KeyError: 'MAPPLET'` here, and MAPPLET is an ordinary Informatica
        # INSTANCE/@TYPE. The cost is not one bad node, it is the whole document:
        # the other 11 elements never get emitted either, and the run produces no
        # IR and no fit number at all, so the gap is invisible rather than small.
        #
        # An unhandled ROLE now behaves the way an unhandled KIND already does --
        # emit a table-declared placeholder, record the obligation as MISSING so it
        # earns no fit credit, and name the role that could not be mapped. The
        # placeholder is `unmapped_role_node_type` in the table because choosing it
        # is policy; it is deliberately NOT 'transformation', which would assert a
        # role the producer failed to determine.
        node_type, role_prov, role_detail = self.node_type_of(el, role_prov)
        self.slots.append(Slot(name, "node.type", role_prov, "role_to_node_type",
                               role_detail
                               + (f"  [role via {el.role_source}]" if role_derived else "")))
        self.slots.append(Slot(name, "node.modelName", TABLE,
                               self.table["naming_policy"]["policy_id"]))
        # FRAMEWORK CHANGE 43 (a pre-existing provenance defect, found on
        # DataStage and present on SSIS too): this cited el.where + "/@" +
        # key_attr, the KEY attribute, even though element.Name is emitted from
        # the DISPLAY attribute whenever naming_policy says so. On SSIS it cited
        # @refId for a value read from @name; on DataStage it cited @Identifier
        # for a value read from @Name. The count was right and the citation was
        # wrong, which is the failure mode provenance exists to prevent.
        name_attr = (el.display_name_attr
                     if self.table["naming_policy"].get("element_name_from")
                     == "DISPLAY_NAME" else key_attr)
        self.slots.append(Slot(name, "element.Name", SOURCE,
                               el.where + self.idn.attr_ref(
                                   self.idn.node_of(el), name_attr)))

        node = {
            "id": name,
            "type": node_type,
            "modelName": self.model_name(el),
            "element": {},
        }

        # FRAMEWORK CHANGE 49: a null ir_kind used to END the node here -- the node
        # was emitted as `$kind: null` with no columns, and the hydrator then kept
        # it OUT of the data-flow graph and dropped EVERY EDGE touching it. Measured
        # across five platforms that cost DataStage 19 of 19 edges: 43 nodes, 19
        # dependencies, zero surviving lineage.
        #
        # `degrade_to` names an engine Transformation class that keeps the node IN
        # the graph while still declaring the element's own kind unrepresented. Two
        # invariants make that honest rather than a number-raising trick:
        #   1. element.$kind stays MISSING, so fit.score's census gate still returns
        #      NotSupported for the element and the degradation earns no fit credit.
        #   2. `_unsupported` still carries the native kind, so the consumer can name
        #      what it could not translate.
        # No degrade_to: containers stay `$kind: null` (no model). A refused
        # data-flow kind becomes UnsupportedTransformation so a placeholder
        # model exists for tier-3 fill; the $kind obligation stays MISSING.
        degraded_from = None
        if ir_kind is None:
            degrade = dispatch.get("degrade_to")
            if not degrade and not self.is_orchestration_container(el):
                degrade = PLACEHOLDER_KIND
            self.slots.append(Slot(name, "element.$kind", MISSING, "kind_dispatch",
                                   f"'{el.kind_raw}' has no ir_kind; hydrator accepts only "
                                   "SourceQualifier and ExpressionTransformation"
                                   + (f"; degraded to {degrade} so the node and its edges "
                                      f"survive hydration -- census stays NotSupported"
                                      if degrade else "")))
            if degrade is None:
                node["element"] = {"$kind": None, "Name": self.ir_element_name(el),
                                   "_unsupported": el.kind_raw}
                # FRAMEWORK CHANGE 59 (b): containment is promoted even here. An
                # element whose KIND is unrepresentable can still state which
                # container owns it, and that is where ENG-001 was found -- on the
                # 31 non-job DataStage elements, none of which is a supported kind.
                self.record_no_slot_facts(
                    el, frozenset(self.promote_containment(node, name, el)))
                return node

            ir_kind, degraded_from = degrade, el.kind_raw

        if degraded_from is None:
            self.slots.append(Slot(name, "element.$kind",
                                   DERIVED if role_derived and dispatch.get("ir_kind_by_role")
                                   else TABLE, "kind_dispatch",
                                   f"'{el.kind_raw}' -> {ir_kind}"
                                   + (f"  [via role {el.role}, {el.role_source}]"
                                      if role_derived and dispatch.get("ir_kind_by_role")
                                      else "")))

        rename = self.idn.rename_map(name)
        by_lower = {p.name.lower(): p for p in el.ports}
        connected_in = {fe.to_field for fe in self.idn.inbound(name)}

        inputs = self.input_columns(name, el, by_lower)

        outputs = []
        oi = 0
        for p in el.ports:
            if not self.is_output(p):
                continue
            if self.is_local(p) and self.pol["drop_local_variables_from_outputs"]:
                continue
            if self.excluded_group(el, p):
                continue
            # FRAMEWORK CHANGE 25: `if p.ref_field is not None` hardcoded the
            # Informatica Router's REF_FIELD passthrough into the emitter.
            if p.ref_field is not None and \
                    self.pol.get("ref_field_passthrough_rule") == "REF_FIELD_IS_UPSTREAM_NAME":
                text, residue, rules = p.ref_field, [], ["ref_field_passthrough"]
            else:
                text, residue, rules = self.resolve(el, p, rename, by_lower, connected_in)
            passthrough = text == p.name
            expr = None if passthrough else text
            outputs.append(self.column_json(p, p.name, expr))
            if expr is None:
                self.record_column_slots(name, f"element.OutputColumns[{oi}]", p, None)
            else:
                if residue:
                    prov = (RESIDUE, p.where + p.expr_where_suffix,
                            "; ".join(sorted(set(residue))))
                elif rules:
                    prov = (TABLE, p.where + p.expr_where_suffix,
                            "; ".join(sorted(set(rules))))
                else:
                    prov = (DERIVED, p.where + p.expr_where_suffix,
                            "port-reference resolution over the connector graph")
                self.record_column_slots(name, f"element.OutputColumns[{oi}]", p, prov)
            oi += 1

        node["element"] = {
            "$kind": ir_kind,
            "Name": self.ir_element_name(el),
            "InputColumns": inputs,
            "OutputColumns": outputs,
        }

        # FRAMEWORK CHANGE 61 (d): MODEL-AUTHORED COLUMN EXPRESSIONS.
        #
        # The last piece of tier 2, and the one that decides whether a derive step becomes
        # a real model or a placeholder. Port resolution can find that a step HAS output
        # fields; it cannot lower `BirthDate.getYear() + 1900` (Java) or `a : b : c`
        # (DataStage BASIC) into Snowflake, because no engine translator handles those
        # dialects. Without this the node is present and projects nothing.
        #
        # Expressions here are expected ALREADY IN SNOWFLAKE DIALECT. That works because
        # the value migrator on this path is a pass-through -- the same behaviour that let
        # Informatica's GET_DATE_PART reach the artifact verbatim, which was a defect
        # there and is the mechanism here. It does mean the model owns correctness of the
        # SQL it writes, with no second opinion from the engine's expression translators.
        # That is the trade tier 2 makes, and it is why these carry MODEL provenance.
        supplied_cols = self.ai_for(el).get("OutputColumns")
        if ir_kind is not None and supplied_cols:
            by_name = {c["Name"].lower(): c for c in node["element"]["OutputColumns"]}
            for i, sc in enumerate(supplied_cols):
                col = {"Name": sc["Name"]}
                if sc.get("Expression"):
                    col["$kind"] = "ColumnExpression"
                    col["Expression"] = sc["Expression"]
                for k in ("DataType", "Precision", "Scale"):
                    if sc.get(k) is not None:
                        col[k] = sc[k]
                by_name[sc["Name"].lower()] = col
                self.slots.append(Slot(
                    name, f"element.OutputColumns[{i}]", MODEL, "sidecar:OutputColumns",
                    f"{sc['Name']} = {sc.get('Expression', '<passthrough>')!r} -- lowered to "
                    f"Snowflake by a model; the source dialect has no engine translator"))
            node["element"]["OutputColumns"] = list(by_name.values())

        # FRAMEWORK CHANGE 60 (d): A TARGET'S PROJECTION IS WHAT IT RECEIVES.
        #
        # Measured defect this fixes: with TargetTransformation newly reachable, every
        # mart model came out as `SELECT` followed by `FROM source_data AS sd` -- no
        # columns, unrunnable SQL, on all four platforms. Cause is not the translator.
        # TargetTranslator projects OutputColumns, and a target's OutputColumns were
        # empty because a destination has no OUTBOUND edge, so port resolution -- which
        # walks the connector graph forward -- had nothing to resolve.
        #
        # A write stage genuinely has no outputs in the source document. But it does
        # have a projection: the columns it writes are the columns it receives. Mirroring
        # inputs is therefore a derivation, not an invention, and it is recorded as
        # DERIVED rather than SOURCE so provenance does not credit the document with
        # stating something it never stated.
        #
        # Guarded three ways so it cannot quietly paper over a real gap: only for a
        # TARGET role, only when outputs are genuinely empty, and only when inputs are
        # not -- a target with no inputs either keeps its existing MISSING obligation.
        if (ir_kind is not None and el.role == "TARGET"
                and not outputs and inputs):
            node["element"]["OutputColumns"] = [dict(c) for c in inputs]
            self.slots.append(Slot(
                name, "element.OutputColumns", DERIVED, "target_projection_mirrors_input",
                f"a write stage declares no outbound port, so its projection is derived "
                f"from its {len(inputs)} inbound column(s); without this every mart model "
                f"emits a column-less SELECT"))
        # FRAMEWORK CHANGE 60 (b): the table-declared scalar payload. Merged after the
        # base fields and never over them -- a rule that tried to supply $kind or Name
        # would be a table bug, and silently letting it win would hide that.
        for _f, _v in payload.items():
            if _f in node["element"]:
                raise ValueError(
                    f"element_fields rule for '{el.kind_raw}' tries to overwrite "
                    f"reserved IR field '{_f}'")
            node["element"][_f] = _v
        # FRAMEWORK CHANGE 49 (b): a degraded node still names its native kind, so a
        # consumer can report WHAT it failed to translate rather than only that it
        # failed. UnsupportedTransformation.OriginalTransformationText is exactly the
        # field this feeds.
        #
        # FRAMEWORK CHANGE 63 (b): and `_unsupported_body` carries the element's own
        # SOURCE FRAGMENT beside it. `_unsupported` keeps its meaning unchanged -- the
        # native kind NAME -- deliberately: the hydrator reads it for
        # UnsupportedIrNode.NativeKind on the `$kind: null` path too, and the marker
        # line naming WHAT failed is the one thing the current placeholder does get
        # right. The body is an ADDITION beside it, not a redefinition of it.
        if degraded_from is not None:
            node["element"]["_unsupported"] = degraded_from
            body = self.unsupported_body(el)
            if body is not None:
                node["element"]["_unsupported_body"] = body
                attach_source_sql(node["element"], body)

        # FRAMEWORK CHANGE 59 (ENG-014 spike): EXTERNAL I/O AS TWO ORTHOGONAL FACTS.
        #
        # A table entry may declare `external_io` -- "Reads", "Writes", or
        # "Reads|Writes" -- alongside a real `ir_kind`. That is the widened
        # classification: the kind axis still decides the model name, and reads/writes
        # is a separate axis. An ADF Copy activity is the case the old binary could
        # not carry: classified as a source its write is unrepresented, classified as
        # a transformation its read has no external origin.
        #
        # `external_io_slots` names, per side, which no_slot_facts ids the widened
        # classification can now HOLD. Each promoted fact becomes a SOURCE-provenance
        # obligation citing the same document location it cited as NO_SLOT, and is
        # suppressed from the NO_SLOT pass so nothing is counted twice.
        #
        # The promotion is deliberately NARROW. Only facts that are genuinely part of
        # a read spec or a write spec are promoted. The store settings
        # (AzureBlobFSReadSettings / AzureBlobFSWriteSettings) name a CONNECTION and
        # stay NO_SLOT -- that is ENG-002, a different ticket -- and the activity
        # policy timeouts stay NO_SLOT because they are execution policy, ENG-012.
        # Promoting those would credit this ticket with closing gaps it does not close.
        promoted = set()
        promoted |= promoted_fields
        external_io = dispatch.get("external_io")
        if external_io is not None:
            node["element"]["ExternalIo"] = external_io
            self.slots.append(Slot(
                name, "element.ExternalIo", TABLE, "kind_dispatch",
                f"'{el.kind_raw}' reads/writes externally: {external_io}"))

            for side, fields in (dispatch.get("external_io_slots") or {}).items():
                spec = {}
                for ir_field, rule_id in fields.items():
                    hit = self.resolve_fact(el, rule_id)
                    if hit is None:
                        # The rule did not fire. Suppressing it anyway is correct:
                        # there is no fact here to represent, so there is no
                        # obligation either way.
                        promoted.add(rule_id)
                        continue
                    _key, where, value = hit
                    spec[ir_field] = value
                    self.slots.append(Slot(name, f"element.{side}.{ir_field}",
                                           SOURCE, where, value))
                    promoted.add(rule_id)
                if spec:
                    node["element"][side] = spec

        # FRAMEWORK CHANGE 59 (b) (ENG-001 spike): CONTAINMENT AS MODELLED DATA.
        #
        # `containment_slots` names no_slot_facts ids whose fact IS a containment
        # relationship, and which a `node.container` field can now hold. Same
        # promotion rule: SOURCE provenance, same citation, suppressed from NO_SLOT.
        promoted |= self.promote_containment(node, name, el)

        # FRAMEWORK CHANGE 37: a supported element that projects NO columns used to
        # create no column obligations at all, so it scored 100% for having nothing
        # to fail at. That is a defect in the metric, not a property of the source:
        # 28 of the 29 DataStage stages carry no column metadata, and the
        # CContainerView states this outright (LinkHasMetaDatas "False| " at
        # dsx:725). "There is a link in this direction but no columns on it" is an
        # unmet obligation and must be counted as one.
        #
        # The obligation is conditioned on an EDGE existing in that direction, not
        # on the element being supported. A source with no inbound edge is not
        # missing its InputColumns -- there is nothing upstream for them to come
        # from -- and counting that would have penalised every source on every
        # platform for a fact that is not a gap.
        edges = self.idn.element_edges()
        has_in = any(e["to"] == name for e in edges)
        has_out = any(e["from"] == name for e in edges)
        for ir_field, cols, linked in (("OutputColumns", outputs, has_out),
                                       ("InputColumns", inputs, has_in)):
            if linked and not cols:
                self.slots.append(Slot(
                    name, f"element.{ir_field}", MISSING, el.where,
                    (f"element is in the graph as {ir_kind} (degraded from "
                     f"'{degraded_from}') and has a link in this "
                     if degraded_from is not None
                     else f"element is supported ($kind={ir_kind}) and has a link in this ")
                    + f"direction, but the document projects no {ir_field}"))
        self.record_no_slot_facts(el, frozenset(promoted))
        # FRAMEWORK CHANGE 65 (b): TIER-2 CONTENT WAS SHIPPING UNMARKED.
        #
        # MEASURED on poc/blind-run/runU/pentaho:
        # `int_derive_fullname_and_birthyear.sql` holds
        #   FirstName || ' ' || MiddleName || ' ' || LastName AS FullName,
        #   YEAR(BirthDate) AS BirthYear
        # BOTH authored by a model -- the .ktr states them as Java
        # (`FirstName + " " + MiddleName + " " + LastName`, `BirthDate.getYear() + 1900`) and no
        # engine translator lowers Java. The file carried NO marker, so it read exactly like an
        # expression read from the document and lowered by a translator. Tier 3 is stamped
        # (SSC-AI-AUTHORED); tier 2 was invisible, and stage 4's MODEL-AUTHORED count therefore
        # reported 2 for a tree in which 3 of 4 models hold model-authored content.
        #
        # The distinction already existed HERE -- `MODEL` is its own provenance class precisely
        # so a model's assertion is never mistaken for a reading (CONFIDENCE.yml,
        # `model-provenance-is-a-separate-class`). It was kept in the ledger and thrown away in
        # the artifact, which is the only thing a reviewer reads. This carries it across.
        authored = [s for s in self.slots[_model_mark:] if s.provenance == MODEL]
        if authored:
            node["modelAuthored"] = [
                {"path": s.path, "sidecar": s.where, "detail": s.detail} for s in authored]
        return node
