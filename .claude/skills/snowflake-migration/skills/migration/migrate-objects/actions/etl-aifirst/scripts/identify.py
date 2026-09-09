"""Deterministic structural identification of ETL elements and edges.

No regex is applied to the source document. Every fact is produced by an
ElementTree structural query whose path is recorded alongside the value, so the
provenance of each emitted field is machine-checkable.

PLATFORM NEUTRALITY CONTRACT (added by the SSIS generalisation pass)
--------------------------------------------------------------------
This module contains NO source-vocabulary literal. It never names an attribute,
an element tag, an element-type string or a role string. Every one of those is
read from the platform table. If you find a source-format literal in this file,
it is a bug and a hidden per-platform assumption.

The lexing of expression *strings* lives in emit.py, because expression syntax is
not XML and has no structure to query.

DOCUMENT-MODEL CONTRACT (added by the DataStage generalisation pass)
--------------------------------------------------------------------
This module no longer knows what a document is made of. It asks docmodel.parse
for a tree and then queries it. See docmodel.py for why the seam is a pluggable
TREE PROJECTION rather than a pluggable query language, and dsxdoc.py for the
record-block projection that a .dsx needs.

EXHAUSTIVE-IDENTIFICATION CONTRACT (ADDITION 2)
-----------------------------------------------
EVERY node in the projection is classified, and the classification is a partition:
an element, a keyless level match, a record a DECLARED EXCLUSION RULE covers, or an
UNKNOWN OBJECT. Nothing falls out of the bottom. Before this, `accounting()` counted
only what a level query matched -- so the loss ledger's denominator was its own
output and a record no level matched could not be reported at all.

The exclusion rules are TABLE-DECLARED, under `structure.census.exclusions`, for the
same reason everything else here is: an exclusion says "this source thing is not an
element", which is per-platform vocabulary and per-platform judgement. Four rule
KINDS live in this file (QUERY, EDGE_RECORD, DEFINITION_OF_ELEMENT, VALUE_CARRIER)
and not one of them names a tag, an attribute or a type string. See `_census` for the
design and `_exclusion_nodes` for the kinds.
"""

import json
from dataclasses import dataclass, field
from string import Formatter
from typing import Any

import docmodel


# --------------------------------------------------------------------------
# provenance
# --------------------------------------------------------------------------

SOURCE = "SOURCE"      # read by a structural query; carries the query path
TABLE = "TABLE"        # supplied by the platform table; carries the rule id
DERIVED = "DERIVED"    # computed from structure by a named algorithm
MISSING = "MISSING"    # obligation not satisfied
NO_SLOT = "NO_SLOT"    # source fact identified, contract has no field for it
RESIDUE = "RESIDUE"    # identified but needs a model to resolve
MODEL = "MODEL"        # RESOLVED BY A MODEL. Carries the sidecar key it came from.

# Orchestration roles the platform tables declare for a container node -- not a
# data-flow element, so it must not grow a placeholder model or a ModelSql request.
# Single source of truth for emit.py and sidecar_producer.py, which both gate on it;
# a role added on one side and not here used to silently diverge from the other.
CONTAINER_ROLES = frozenset({"UNIT_OF_WORK", "JOB", "TASK", "CONTAINER", "PACKAGE"})
#
# MODEL exists because RESIDUE was a dead end. RESIDUE has always meant "identified
# but needs a model to resolve" -- the framework had a NAME for facts requiring AI and
# no path from one to an answer, so every such fact terminated in a degraded element
# and a NULL-projecting placeholder. On a platform we do not support that is the
# EXPECTED case, which made "nothing" the normal output of an AI-first migrator.
#
# MODEL is deliberately NOT folded into SOURCE or DERIVED. A model-authored predicate
# is not read from the document and is not computed from it by a named algorithm: it is
# asserted by something fallible, and the whole integrity apparatus here exists to keep
# that distinction visible. Anything downstream that reports fidelity must be able to
# separate "the document says this" from "a model believes this".



@dataclass
class Fact:
    """A single identified value plus where it came from."""

    value: Any
    provenance: str
    where: str

    def __repr__(self) -> str:
        return f"{self.value!r} <{self.provenance} {self.where}>"


@dataclass
class Port:
    name: str
    datatype: str
    precision: int | None      # None = the platform states no precision for this type
    scale: int | None          # None = the platform states no scale for this type
    porttype: str
    expression: str | None
    default_value: str
    group: str | None
    ref_field: str | None
    where: str
    site: str = ""                 # which port_site produced it
    lineage: str | None = None     # platform-native column identity, when any
    name_attr: str = ""            # attribute names travel with the value, so the
    datatype_attr: str = ""        # `where` of every emitted field is exact rather
    precision_attr: str = ""       # than a guess at what the attribute was called
    scale_attr: str = ""
    expr_where_suffix: str = ""
    # FRAMEWORK CHANGE 47 (ARCHITECTURAL A6): the attribute NAMES already
    # travelled with the value; under A6 the citation for reading one is the
    # front-end's to render, so the node has to travel with it too.
    node: Any = None


@dataclass
class Element:
    instance_name: str
    role: str
    kind_raw: str
    def_name: str
    description: str
    where: str
    where_path: str = ""   # `where` without the front-end location prefix
    display_name: str = ""
    level: str = ""
    flags: dict = field(default_factory=dict)      # table-named element flags
    ports: list[Port] = field(default_factory=list)
    groups: list[dict] = field(default_factory=list)
    table_attrs: dict = field(default_factory=dict)
    associated: str | None = None
    absorbed: list[str] = field(default_factory=list)
    harvested: dict = field(default_factory=dict)  # def-site attribute harvests
    load_order: str | None = None
    container: str | None = None                   # nearest enclosing element
    key_attr: str = ""
    role_source: str = ""                          # how the role was established
    valueless_attrs: list[str] = field(default_factory=list)  # stated key, no value
    display_name_attr: str = ""                    # which attribute the name came from
    table_attr_where: dict = field(default_factory=dict)      # attr key -> located where
    # FRAMEWORK CHANGE 63 (a): where this element's ports and properties were read
    # from. Not always the element's own node -- see _attach_definitions.
    def_where: str = ""


@dataclass
class FieldEdge:
    from_instance: str
    from_field: str
    to_instance: str
    to_field: str
    where: str
    # FRAMEWORK CHANGE 63 (b): THE ADDRESS AT WHICH `from_field` IS STATED, which is
    # not the same place as the edge itself.
    #
    # WHY IT HAD TO BE ADDED, and it was found by an audit that had never been able to
    # read this platform. `port_policy.input_column_naming` is UPSTREAM_FIELD on every
    # table, so an emitted `InputColumns[i].Name` is the UPSTREAM field's name -- while
    # `record_column_slots` cited the LOCAL port's name attribute, because that is the
    # port whose datatype/precision the column carries. Where a transformation RENAMES a
    # port the two differ, and the provenance record then pointed at a location stating a
    # different value. MEASURED on MappingForTest.XML, five citations, all `.Name` and no
    # other field (which is the signature: DataType and Precision really do come from the
    # local port and really did match):
    #   EXPTRANS  InputColumns[0].Name  emitted 'NAME1'    cited TRANSFORMFIELD[@NAME='NAME']
    #   EXPTRANS1 InputColumns[0].Name  emitted 'NEW_NAME' cited TRANSFORMFIELD[@NAME='op1']
    # Both citations resolve, both state something the IR does not hold, and nothing could
    # see it while the audit's only locator was `^dsx:`.
    from_field_where: str = ""


@dataclass
class UnknownObject:
    """FRAMEWORK CHANGE 67 (ADDITION 2): a record the platform table does not
    recognise, INVENTORIED rather than dropped.

    Why this type exists, stated as the measurement that forced it. The sweep in
    `_identify_elements` appended to `self.declared` only for nodes a level query
    MATCHED, so `accounting()`'s denominator was derived from its own output: a
    record no level matched was not counted as lost, it was not counted at all.
    MEASURED on CustomerSummaryDerive.dsx -- 5 elements in the document, ledger
    reported `declared=4 identified=4 lost=0 balances=True`, and the record it
    could not see was the CTransformerStage holding every derivation in the job.

    An Unknown Object is a FIRST-CLASS inventory entry, so it carries the same
    provenance obligation as an element: it was READ from the document, at a
    citable location, and `where` is that citation with the front-end's location
    prefix on it. Its KIND is unrecognised; its EXISTENCE and POSITION are facts.

    `attrs` is every key the record states, because "what is this thing" can only
    be answered from what it says about itself, and `identity` is the subset the
    table nominates as a record's class discriminators (structure.census.
    identity_attrs) so an inventory of 900 unknowns is still readable.
    """

    where: str                  # front-end location prefix + projection path
    where_path: str             # projection path alone, an xpath from the root
    tag: str
    depth: int
    container: str | None       # nearest enclosing IDENTIFIED element, if any
    identity: dict              # table-nominated discriminating attributes
    attrs: dict                 # every key the record states
    child_count: int


class Identification:
    """Everything structure can tell us about one document."""

    def __init__(self, table: dict, xml_path: str):
        self.table = table
        self.struct = table["structure"]
        self.xml_path = xml_path
        # FRAMEWORK CHANGE 29 (ARCHITECTURAL A1): was `self.tree = ET.parse(path);
        # self.root = self.tree.getroot()`. One document model -- an XML tree --
        # was hardcoded here, and it was invisible because both prior platforms
        # were XML. A .dsx is a record-block text format, so the front-end is now
        # selected by the platform table.
        self.doc = docmodel.parse(table, xml_path)
        self.root = self.doc.root

        # child -> parent, for structural ancestry walks. Platform-neutral: it is
        # how we resolve a port-level reference to its owning element and a
        # column to its containing output group, without string surgery on ids.
        self._parent: dict = {c: p for p in self.root.iter() for c in p}

        self.doc_name = self._read_container_name()

        self.elements: dict[str, Element] = {}
        self.field_edges: list[FieldEdge] = []
        self.element_edge_records: list[dict] = []
        self.dropped_instances: dict[str, Element] = {}
        # FRAMEWORK CHANGE 62: an edge record whose endpoint did not resolve used to be
        # dropped with nothing recorded, and the pin-pair audit needs both halves of
        # every pair addressable after the sweep. `link_audit` stays None for a platform
        # that declares no pin_pairs, so nothing about the other four platforms changes.
        self.unresolved_edges: list[dict] = []
        self.link_audit: dict | None = None
        self._pin_pair_seen: dict[int, dict] = {}   # id(link record) -> its edge record

        # FRAMEWORK CHANGE 52 (ADDITION 1): the declared-versus-identified ledger.
        # `declared` is every node the level queries matched; `keyless` those that
        # state no key and are therefore not elements; `key_collisions` those that
        # were identified and then overwritten by a later record with the same key.
        # declared - keyless - collisions must equal identified, and `accounting()`
        # asserts exactly that.
        #
        # FRAMEWORK CHANGE 67 (ADDITION 2): that ledger's denominator WAS ITS OWN
        # OUTPUT. `self.declared` is appended inside the level sweep, so a record no
        # level query matched never entered the denominator and could not be reported
        # missing. It is kept, unchanged, as the ELEMENT ledger -- and the census
        # below is now the DOCUMENT ledger it is checked against. See `_census`.
        self.declared: list[tuple[str, str]] = []
        self.keyless: list[tuple[str, str, int]] = []
        self.key_collisions: list[dict] = []

        # FRAMEWORK CHANGE 67 (ADDITION 2): the exhaustive census. Every node in the
        # projection lands in exactly one of these three, or is an element.
        self._matched_nodes: dict[int, str] = {}   # id(node) -> level that matched it
        self.record_count = 0
        self.excluded: list[dict] = []             # rule id + what it excluded
        self.unknown_objects: list[UnknownObject] = []
        self.census_contested: list[dict] = []     # a rule excluded an ELEMENT: table bug
        self.census_overlaps: list[dict] = []      # >1 rule matched: attribution note
        self.excluded_by_rule: dict[str, int] = {}

        self._node_of: dict[str, Any] = {}     # element key -> its XML node
        self._def_node_of: dict[str, Any] = {}  # element key -> its DEFINITION node
        self._element_of_node: dict = {}       # XML node -> element key
        self._ref_index: dict[str, Any] = {}   # addressable id -> XML node
        # FRAMEWORK CHANGE 63 (b): the third member is WHERE the declaring port states
        # its name. Needed because a downstream InputColumns[i].Name is the UPSTREAM
        # field's name, so its citation has to address the upstream declaration and not
        # the local port -- see FieldEdge.from_field_where.
        self._lineage_index: dict[str, tuple[str, str, str]] = {}
        self._group_node_of: dict = {}         # group XML node -> group name

        self._identify_elements()
        self._attach_definitions()
        self._index_refs()
        self._identify_edges()
        self._apply_collapse()
        # LAST, deliberately. The census needs the def nodes (_attach_definitions),
        # the edge-level matches (_identify_edges) and the collapse outcome
        # (_apply_collapse) to be able to say "this node is already inventoried".
        self._census()

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _tagpath(xpath: str) -> str:
        """Readable suffix of a site xpath, for `where` strings."""
        return xpath[2:] if xpath.startswith("./") else xpath

    @staticmethod
    def _first_attr(node, candidates) -> tuple[int | None, str]:
        """First candidate attribute actually present. (None, '') when the source
        states none of them -- which is NOT the same fact as a stated zero.

        A "P.S" decimal string (Alteryx FixedDecimal's `size="19.2"`) is tolerated
        here too, not just in `_precision_scale`: any caller passing an attribute
        that turns out to be dotted gets the whole-number part rather than a
        document-wide crash, while truly unparseable text ('abc') still raises."""
        for a in candidates:
            v = node.get(a)
            if v is not None and v != "":
                try:
                    return int(v), a
                except ValueError:
                    whole, dot, frac = v.partition(".")
                    if dot and whole.isdigit() and frac.isdigit():
                        return int(whole), a
                    raise
        return None, ""

    def _precision_scale(self, node, ps: dict) -> tuple[int | None, str, int | None, str]:
        """Precision and scale are usually two distinct attributes, but a
        numeric-typed field's precision attribute may instead state a single
        dotted "P.S" string with no separate scale attribute at all. Honoured
        only when no scale attribute states a value -- a real, separately
        stated scale always wins over splitting the precision string."""
        prec_raw, prec_attr = None, ""
        for a in ps.get("precision_attrs", []):
            v = node.get(a)
            if v is not None and v != "":
                prec_raw, prec_attr = v, a
                break
        scale, scale_attr = self._first_attr(node, ps.get("scale_attrs", []))
        if prec_raw is None:
            return None, "", scale, scale_attr
        if scale is None:
            whole, dot, frac = prec_raw.partition(".")
            if dot and whole.isdigit() and frac.isdigit():
                return int(whole), prec_attr, int(frac), prec_attr
        # Stated scale wins over splitting the precision string, but a dotted
        # precision must still not crash identify for the whole document.
        try:
            return int(prec_raw), prec_attr, scale, scale_attr
        except ValueError:
            whole, dot, frac = prec_raw.partition(".")
            if dot and whole.isdigit() and frac.isdigit():
                return int(whole), prec_attr, scale, scale_attr
            raise

    def key_attr_of(self, el: Element) -> str:
        return el.key_attr

    def at(self, node, path: str) -> str:
        """FRAMEWORK CHANGE 30 (ARCHITECTURAL A3): every `where` string was a bare
        structural path. For an XML source that IS a location in the document, but
        for a projected tree it is a location in the PROJECTION -- so "SOURCE"
        would have become unfalsifiable. Every front-end is now also a location
        oracle; the XML one returns "" so Informatica and SSIS `where` strings are
        byte-identical to before."""
        return self.doc.loc_prefix(node) + path

    def attr_ref(self, node, attr: str) -> str:
        """FRAMEWORK CHANGE 48 (ARCHITECTURAL A6): the last step of every SOURCE
        citation was the hardcoded string "/@" + attr, in seven places. Two of the
        five platforms carry no attributes at all -- a Kettle .ktr has zero, and a
        JSON member is not an attribute -- so the front-end lifts the value and
        "/@name" becomes an address that is not in the file. The front-end now
        renders it. XML and record-block front-ends return "/@" + attr, so the
        three prior platforms are byte-identical."""
        return self.doc.attr_ref(node, attr)

    def _scope_of(self, node) -> str | None:
        """FRAMEWORK CHANGE 31 (ARCHITECTURAL A5): element keys were assumed
        DOCUMENT-unique. An Informatica INSTANCE/@NAME and an SSIS @refId both are.
        A .dsx identifier is only unique inside its DSJOB: MaskDemo.dsx has 65
        stage and link records carrying 22 distinct identifiers, 14 of them reused
        across jobs. Without scoping, eight different stages named V0S1 collapse
        into one element and their edges cross between unrelated jobs.

        The scope is the nearest STRICT ancestor matching the declared tag, so a
        scope node does not scope itself."""
        ks = self.struct.get("key_scope")
        if not ks:
            return None
        cur = self._parent.get(node)
        while cur is not None:
            if cur.tag == ks["tag"]:
                return cur.get(ks["key_attr"])
            cur = self._parent.get(cur)
        return None

    def _scoped(self, node, raw: str) -> str:
        ks = self.struct.get("key_scope")
        if not ks:
            return raw
        scope = self._scope_of(node)
        return f"{scope}{ks['separator']}{raw}" if scope else raw

    def _scoped_ref(self, node, raw: str | None) -> str | None:
        """FRAMEWORK CHANGE 66 (c): SCOPE A REFERENCE THE SAME WAY AS A KEY.

        `_scoped` builds an element's KEY. This builds the key a REFERENCE to an
        element resolves to, and it exists because those two were done in different
        places and only one of them applied the scope.

        THE MEASURED TRAP. Element keys have been scoped since FRAMEWORK CHANGE 31,
        but three sites read a raw document key and then matched it against those
        scoped keys:
          * an ELEMENT_KEY edge's two endpoints (an Informatica CONNECTOR's
            FROMINSTANCE / TOINSTANCE);
          * the `associated` reference that `_apply_collapse` resolves;
          * the `load_order` target reference.
        DataStage never exposed it: its edges are PIN_PAIR/PORT_REF, which resolve
        through `_ref_index` -- and THAT index is already keyed by
        `(scope, id)` (identify.py:764), which is the one site that got it right.
        So declaring `key_scope` on a platform whose edges are ELEMENT_KEY silently
        broke every edge: MEASURED, adding the scope to `platform_informatica.json`
        without this dropped TOTAL FIT from 84.5% to 72.8% (edges resolve to keys
        that are not elements, so InputColumns collapse) and raised
        `KeyError: 'INCR_SALARY'` in decisions.py. A half-applied scope is worse
        than none, because the loss is in the edges rather than in the ledger.

        A reference is scoped by ITS OWN enclosing scope node, not by the target's:
        a CONNECTOR names an instance in the mapping the CONNECTOR itself lives in,
        which is exactly what makes cross-mapping name reuse safe. None passes
        through unchanged -- an absent reference must stay absent rather than become
        the string 'None' prefixed by a scope.
        """
        if raw is None:
            return None
        return self._scoped(node, raw)

    def accounting(self) -> dict:
        """FRAMEWORK CHANGE 52 (ADDITION 1): declared versus identified, as a
        closed ledger the caller can assert on.

        `fit.score` divides satisfied obligations by obligations RAISED, and an
        element that was never identified raises none -- so silently dropping
        elements does not lower the fit score, it raises it. MEASURED on
        Informatica's `WF_PARAMFILE_MULTI_SESSION.XML`: 9 INSTANCEs declared, 3
        identified, TOTAL FIT 89.9%, the highest of any document in the project.
        The fit number cannot be read at all without this ledger beside it.

        FRAMEWORK CHANGE 67 (ADDITION 2): `declared` NOW MEANS EVERY RECORD IN THE
        DOCUMENT, not every record a level query matched. THIS IS A CHANGE OF
        MEANING and it is the point of the change: the old `declared` was produced
        inside the level sweep, so the ledger's denominator was its own output and a
        record no level matched could not be reported at all. MEASURED on
        CustomerSummaryDerive.dsx: `declared=4 identified=4 lost=0 balances=True` on
        a document holding 5 elements, the fifth being the CTransformerStage that
        holds every derivation in the job.

        The old number is still here under `level_matched`, because "the level
        queries matched 43 nodes" and "the document holds 1341 records" are both
        facts and neither can be read without the other.

        THE IDENTITY, exhaustive over the document:

            declared = identified + lost + keyless + excluded + unknown

        `identified` are elements; `lost` were identified and then overwritten by a
        later record with the same key; `keyless` were matched by a level and state
        no key; `excluded` were matched by a DECLARED, NAMED, REASONED exclusion
        rule in the table (`structure.census.exclusions`); `unknown` are Unknown
        Objects -- records nothing in the table recognises, inventoried with a
        citable location rather than dropped.

        `lost` is still the number that must be zero. An Unknown Object is NOT lost:
        it is tracked, which is the whole difference this change makes.

        `balances` is now the CONJUNCTION of three facts, two of which can actually
        fail (the exhaustive sum cannot -- `unknown` is a complement, see `_census`):
        the document identity, no node matched by two levels, and no exclusion rule
        contesting a node a level query matched.
        """
        identified = len(self.elements) + len(self.dropped_instances)
        level_matched = len(self.declared)
        keyless = len(self.keyless)
        lost = len(self.key_collisions)
        excluded = len(self.excluded)
        unknown = len(self.unknown_objects)
        sums = (identified + lost + keyless + excluded + unknown) == self.record_count
        no_double_level = len(self._matched_nodes) == level_matched
        element_ledger = level_matched - keyless - lost == identified
        return {
            # THE DOCUMENT LEDGER -- exhaustive over every record in the projection.
            "declared": self.record_count,
            "records": self.record_count,
            "identified": identified,
            "lost": lost,
            "keyless": keyless,
            "excluded": excluded,
            "unknown": unknown,
            "balances": (sums and no_double_level and element_ledger
                         and not self.census_contested),
            # THE ELEMENT LEDGER -- what `declared` used to mean, kept because the
            # two numbers answer different questions.
            "level_matched": level_matched,
            "element_ledger_balances": element_ledger,
            "document_sums": sums,
            "no_double_level_match": no_double_level,
            "collisions": self.key_collisions,
            "excluded_by_rule": dict(self.excluded_by_rule),
            "contested": self.census_contested,
            "overlaps": self.census_overlaps,
            "unknown_objects": self.unknown_objects,
        }

    def dispatch_for(self, el: Element) -> dict:
        """FRAMEWORK CHANGE 32: kind_dispatch mapped a native kind to exactly ONE
        ir_kind. In DataStage a single StageType is used in both directions --
        JDBCConnectorPX is a source in MaskJdbc and a target in MaskJdbc's sibling
        job -- so the IR kind depends on kind AND role. Emitting SourceQualifier
        for a write stage would be a fabrication, not a lossy mapping.

        A kind ABSENT from kind_dispatch is not the same fact as a kind present
        with an explicit `degrade_to: null` -- the latter is a declared container
        (an SSIS Data Flow Task, a DataStage DSJOB) that the table author decided
        has no data-flow representation. The former is a kind the table never
        considered, and defaulting it to that same null silently reused the
        container's answer for an unrelated gap, dropping the node and every edge
        touching it. `unmapped_kind_degrade_to` is the table's fallback for that
        gap, distinct from any per-kind degrade_to."""
        d = self.table["kind_dispatch"].get(el.kind_raw)
        if d is None:
            return {"ir_kind": None,
                    "degrade_to": self.table["kind_dispatch"].get("unmapped_kind_degrade_to")}
        by_role = d.get("ir_kind_by_role")
        if by_role is not None:
            d = dict(d)
            d["ir_kind"] = by_role.get(el.role)
        return d

    def node_of(self, el: Element):
        return self._node_of[el.instance_name]

    def def_node_of(self, el: Element):
        """The node this element's ports and properties were read from.

        FRAMEWORK CHANGE 63 (a). `node_of` returns the node the element sweep
        matched -- on a platform that separates an INSTANCE from the DEFINITION it
        references, that node carries the element's identity and none of its
        payload. Returns None when no definition resolved, which is a real state
        (a reference to a definition the document does not contain) and must stay
        distinguishable from "the definition states nothing"."""
        return self._def_node_of.get(el.instance_name)

    def source_text(self, el: Element) -> str:
        """The SOURCE FRAGMENT that declares this element, in the source's own
        syntax, or "" when the front-end cannot supply one.

        FRAMEWORK CHANGE 63 (b). This is the framework's only reason to ask a
        front-end for bytes rather than for structure, and it exists because a
        placeholder naming only the KIND that failed is nearly useless: vanilla
        SnowConvert's not-supported path emits the original element commented out,
        and a reviewer (or a tier-3 model) needs the same. Whether a fragment is
        reconstructed or sliced from the file is the front-end's business -- see
        `source_text` in docmodel.py, dsxdoc.py, ktrdoc.py and jsondoc.py.

        BOTH SITES, when the platform has two. MEASURED: on Informatica the element
        node is `<INSTANCE NAME=".." TRANSFORMATION_TYPE="Router"/>` -- 162 bytes of
        pure reference, holding not one group, port or property -- because the
        payload is on the TRANSFORMATION it names. That is the same instance-versus-
        definition split DEF_SITE_ATTR exists for, showing up a second time, and
        SnowConvert's own configurator serialises the DEFINITION for exactly this
        reason (`GetTransformationText(transformationDef)`). The two fragments are
        emitted in document order, element first. On a platform whose elements carry
        their own payload the two nodes ARE the same node and the output is
        byte-identical to the single-fragment form."""
        fn = getattr(self.doc, "source_text", None)
        if fn is None:
            return ""
        node = self.node_of(el)
        parts = [fn(node) or ""]
        defn = self.def_node_of(el)
        if defn is not None and defn is not node:
            parts.append(fn(defn) or "")
        extra = self._reusable_definition_text(el)
        if extra:
            parts.append(extra)
        return "\n".join(p for p in parts if p.strip())

    def _reusable_definition_text(self, el: Element) -> str:
        """Mapplet INSTANCE/@TRANSFORMATION_NAME names a folder-level <MAPPLET>
        whose internal graph is not the thin TYPE=Mapplet TRANSFORMATION that
        default_def_site resolves. Without that fragment the sidecar model only
        sees the INSTANCE and abstains (measured: inf-mapplet mplt_mp1_multi).

        A MAPPLET name is only unique inside its own <FOLDER>: two folders can
        each declare one named the same. Search the enclosing folder first so a
        same-named mapplet in a different folder is never picked by mistake;
        fall back to a document-wide search only when no enclosing folder exists."""
        if getattr(el, "kind_raw", None) != "Mapplet":
            return ""
        node = self.node_of(el)
        name = None
        if node is not None:
            name = node.get("TRANSFORMATION_NAME") or node.get("NAME")
        name = name or el.instance_name.rsplit("\\", 1)[-1]

        scope = node
        while scope is not None:
            if scope.tag.rsplit("}", 1)[-1] == "FOLDER":
                break
            scope = self._parent.get(scope)
        search_roots = [scope] if scope is not None else [self.root]

        for root in search_roots:
            for cand in root.iter():
                tag = cand.tag.rsplit("}", 1)[-1]
                if tag != "MAPPLET" or cand.get("NAME") != name:
                    continue
                fn = getattr(self.doc, "source_text", None)
                return (fn(cand) if fn is not None else "") or ""
        return ""

    def _read_container_name(self) -> str | None:
        """Document-level name. FRAMEWORK CHANGE 1: was
        `root.find(elements + '/..').get('NAME')`, i.e. the container of the
        elements was assumed to be the named unit of work. In a .dtsx the
        container of the components is <components>, which is anonymous, and the
        named unit is the package root."""
        c = self.struct.get("container")
        if not c:
            return None
        node = self.root if c["xpath"] == "." else self.root.find(c["xpath"])
        return node.get(c["name_attr"]) if node is not None else None

    def _owner_element_of(self, node) -> str | None:
        """Nearest ancestor-or-self that is an identified element."""
        cur = node
        while cur is not None:
            key = self._element_of_node.get(id(cur))
            if key is not None:
                return key
            cur = self._parent.get(cur)
        return None

    def _group_of_node(self, node) -> str | None:
        """Nearest ancestor-or-self that is an identified output group."""
        cur = node
        while cur is not None:
            name = self._group_node_of.get(id(cur))
            if name is not None:
                return name
            cur = self._parent.get(cur)
        return None

    # -- element sweeps ----------------------------------------------------

    def _identify_elements(self) -> None:
        """FRAMEWORK CHANGE 2: was a single sweep over one xpath. A .dtsx carries
        two graph levels in one document -- control-flow executables and
        data-flow components -- so the sweep is now a list.

        FRAMEWORK CHANGE 52 (ADDITION 1): this sweep wrote `self.elements[name]`
        blind. When two source records key to the same name the second overwrote
        the first and NOTHING recorded it, so the document silently shrank -- and
        because `fit.score`'s denominator counts only obligations of elements that
        were found, losing elements RAISES the fit score. MEASURED: Informatica's
        `WF_PARAMFILE_MULTI_SESSION.XML` declares 9 INSTANCEs, 3 survive, and it
        scored the highest fit of any document in the project. A metric that
        rewards data loss is worse than no metric. Every overwrite is now recorded
        with the `where` of both the record kept and the record it replaced."""
        for level in self.struct["levels"]:
            q = level["elements"]
            key_attr = level["key_attr"]
            for idx, node in enumerate(self.root.findall(q), start=1):
                self.declared.append((level["name"], q))
                # FRAMEWORK CHANGE 67 (ADDITION 2): the census needs to know which
                # NODES a level reached, not just how many matches there were. The
                # two differ if two levels ever match one node, and `accounting()`
                # reports that rather than letting it silently unbalance the ledger.
                if id(node) in self._matched_nodes:
                    self.census_overlaps.append({
                        "kind": "TWO_LEVELS_MATCHED_ONE_NODE",
                        "tag": node.tag,
                        "first": self._matched_nodes[id(node)],
                        "second": level["name"],
                    })
                self._matched_nodes[id(node)] = level["name"]
                raw_name = node.get(key_attr)
                if raw_name is None:
                    # Not an element: the level's query matched a node that states
                    # no key at all. Counted separately so `declared` stays an
                    # honest denominator rather than an inflated one.
                    self.keyless.append((level["name"], q, idx))
                    continue
                name = self._scoped(node, raw_name)
                # FRAMEWORK CHANGE 33: kind_attr was mandatory. A DSJOB block
                # states no kind attribute of any sort -- it is a job because of
                # the keyword that opens it -- so a level may now assert its kind
                # literally. Provenance of that kind is TABLE, not SOURCE.
                if level.get("kind_literal") is not None:
                    kind = level["kind_literal"]
                else:
                    kind = node.get(level["kind_attr"], "")
                disp = self.table["kind_dispatch"].get(kind, {})
                # FRAMEWORK CHANGE 3: role was assumed to be an attribute
                # independent of kind (Informatica INSTANCE/@TYPE vs
                # @TRANSFORMATION_TYPE). SSIS has one axis only: a component
                # declares componentClassID and nothing else, so role must be
                # derivable from the kind table.
                # FRAMEWORK CHANGE 34: DataStage adds a THIRD mechanism. A
                # connector stage's direction is not an attribute and is not
                # implied by its StageType; it is stated by WHICH PIN LISTS the
                # stage declares. The obvious-looking alternative -- the "Context"
                # property, value source/target -- is absent on all 6 PxDataSet
                # stages and states the non-role value "request" on all 7
                # JavaStagePX stages, so reading it as the role would have been
                # both incomplete and wrong.
                role_src = ""
                if level.get("role_attr"):
                    role = node.get(level["role_attr"], "")
                    role_src = "@" + level["role_attr"]
                elif level.get("role_from", {}).get("kind") == "PIN_DIRECTION":
                    rf = level["role_from"]
                    has_in = bool(node.get(rf["input_list_attr"]))
                    has_out = bool(node.get(rf["output_list_attr"]))
                    slot = ("BOTH" if has_in and has_out else
                            "IN_ONLY" if has_in else
                            "OUT_ONLY" if has_out else "NEITHER")
                    role = rf["roles"][slot]
                    role_src = (f"DERIVED pin direction {slot} from @"
                                f"{rf['input_list_attr']}/@{rf['output_list_attr']}")
                else:
                    role = disp.get("role", "")
                    role_src = "kind_dispatch"
                assoc = None
                a = level.get("associated")
                if a:
                    an = node.find(a["xpath"])
                    if an is not None:
                        # FRAMEWORK CHANGE 66 (c): `_apply_collapse` matches this
                        # against element KEYS, so it must be scoped like one.
                        assoc = self._scoped_ref(node, an.get(a["name_attr"]))
                el = Element(
                    instance_name=name,
                    role=role,
                    kind_raw=kind,
                    def_name=node.get(level.get("def_name_attr") or key_attr, raw_name),
                    description=node.get(level.get("description_attr", ""), ""),
                    where=self.at(node, f"{q}[{idx}][@{key_attr}='{raw_name}']"),
                    where_path=f"{q}[{idx}][@{key_attr}='{raw_name}']",
                    display_name=node.get(level.get("display_name_attr") or key_attr,
                                          raw_name),
                    level=level["name"],
                    associated=assoc,
                    key_attr=key_attr,
                    role_source=role_src,
                    display_name_attr=(level.get("display_name_attr") or key_attr),
                )
                # FRAMEWORK CHANGE 4: `reusable` was a named field on Element
                # reading INSTANCE/@REUSABLE. Element flags are now a
                # table-named dict, so no source vocabulary reaches the model.
                for flag, attr in level.get("flag_attrs", {}).items():
                    v = node.get(attr)
                    if v is not None:
                        el.flags[flag] = v
                # FRAMEWORK CHANGE 52: record the collision BEFORE the write, while
                # both records are still addressable. `where` on each side is what
                # makes this auditable against the file rather than a bare count.
                # This is last-wins: `el` (the new record) overwrites and survives,
                # so it is KEPT and the existing record is LOST. The existing
                # record's node must also lose its `_element_of_node` entry --
                # otherwise that stale entry still resolves to `name` even though
                # `self.elements[name]` no longer names that node.
                if name in self.elements:
                    old_node = self._node_of.get(name)
                    self.key_collisions.append({
                        "key": name,
                        "level": level["name"],
                        "kept_where": el.where,
                        "lost_where": self.elements[name].where,
                    })
                    if old_node is not None:
                        self._element_of_node.pop(id(old_node), None)
                self.elements[name] = el
                self._node_of[name] = node
                self._element_of_node[id(node)] = name

        # containment between levels, computed from ancestry, not from id text.
        for name, node in self._node_of.items():
            parent = self._parent.get(node)
            if parent is not None:
                owner = self._owner_element_of(parent)
                if owner and owner != name:
                    self.elements[name].container = owner

        # FRAMEWORK CHANGE 5: load order read @TARGETINSTANCE and @ORDER as
        # literals. Both are now table-named, and the site is optional.
        lo = self.struct.get("load_order")
        if lo:
            for node in self.root.findall(lo["xpath"]):
                # FRAMEWORK CHANGE 66 (c): a load-order entry names an element, so
                # the name is a reference and is scoped like one.
                tgt = self._scoped_ref(node, node.get(lo["key_attr"]))
                if tgt in self.elements:
                    self.elements[tgt].load_order = node.get(lo["order_attr"])

    # -- definitions -------------------------------------------------------

    def _attach_definitions(self) -> None:
        """FRAMEWORK CHANGE 6: dispatch was `if kind_raw == 'Source Definition'
        ... elif 'Target Definition' ... else transformation`, i.e. two
        Informatica type strings hardcoded in framework code. The def site is now
        named by the kind_dispatch entry, and 'SELF' covers platforms where the
        element carries its own ports (SSIS components do)."""
        sites = self.struct.get("def_sites", {})
        default = self.struct.get("default_def_site", "SELF")
        for el in self.elements.values():
            disp = self.table["kind_dispatch"].get(el.kind_raw, {})
            site_name = disp.get("def_site", default)
            if site_name == "SELF":
                node = self._node_of[el.instance_name]
                # FRAMEWORK CHANGE 30b: was `defq = el.where`. Once `where` carries
                # a location prefix, reusing it as a query base would nest one
                # prefix inside another ("dsx:306 dsx:145 DSJOB/..."). The prefix
                # is applied once, at the leaf, from the leaf's own node.
                defq = el.where_path
                # FRAMEWORK CHANGE 54 (ARCHITECTURAL A8): there was exactly ONE
                # self def site per platform, so every element kind read its
                # columns from the same place with the same attributes. That held
                # for three platforms because Informatica, SSIS and DataStage each
                # have one column schema. Kettle does not: <step>/<fields>/<field>
                # is a DIFFERENT
                # sub-schema per step plugin. A RowGenerator's fields are OUTPUT
                # columns with name/type/length/precision
                # (RowGeneratorMeta.getFields merges them into the outgoing row); a
                # WriteToLog's fields are INCOMING columns stating only a name
                # (WriteToLogMeta has no getFields override and WriteToLog.processRow
                # resolves them with getInputRowMeta().indexOfValue). Reading the
                # second as outputs would invent an output row the step does not
                # produce. Named sites override the base site key by key.
                site_cfg = self.struct.get("self_def_site", {})
                named = disp.get("self_def_site")
                if named:
                    site_cfg = {**site_cfg, **self.struct["self_def_sites"][named]}
            else:
                site_cfg = sites.get(site_name)
                # FRAMEWORK CHANGE 63 (a): an UNDECLARED def-site name used to
                # `continue` in silence, and that silence was load-bearing.
                # MEASURED: platform_informatica.json's Filter entry named
                # def_site "RESOLVED", which structure.def_sites does not declare,
                # so the Filter element was given NO ports and NO property bag at
                # all -- and the output was indistinguishable from "the document
                # states neither". Its predicate lives in that property bag, so the
                # gap that was catalogued as "no rule kind can follow
                # instance->definition" was in fact "the def site never resolved".
                #
                # This is the same closed-vocabulary failure the rest of this file
                # documents: a name the table does not know must not read as
                # nothing. Loud for the reason resolve_fact raises on an
                # unimplemented rule kind -- returning nothing would make a table
                # typo look like a fact the source does not state.
                if site_cfg is None:
                    raise ValueError(
                        f"kind_dispatch['{el.kind_raw}'].def_site is "
                        f"{site_name!r}, which structure.def_sites does not "
                        f"declare (declared: {sorted(sites)} plus 'SELF'). Every "
                        f"port and every property of this element would be "
                        f"silently unread.")
                # FRAMEWORK CHANGE 7: the def lookup predicate was hardcoded as
                # [@NAME='...'] even though the element key attribute was already
                # table-driven. Now the def site names its own key attribute.
                defq = f"{site_cfg['xpath']}[@{site_cfg['key_attr']}='{el.def_name}']"
                node = self.root.find(defq)
                if node is None:
                    continue
                for out_key, attr in site_cfg.get("harvest_attrs", {}).items():
                    el.harvested[out_key] = node.get(attr, "")
                if site_cfg.get("harvest_attrs"):
                    el.harvested["where"] = self.at(node, defq)
            # group_site FIRST: ancestry-based port-group resolution needs the
            # group index populated before any port is read.
            # FRAMEWORK CHANGE 63: the def query and the def NODE are recorded --
            # (a) so a promoted def-site fact can cite the node it was actually read
            # from, and (b) so a degraded element's source fragment can include the
            # definition and not just the reference to it. On a SELF def site both
            # are the element's own node and nothing downstream changes.
            el.def_where = defq
            self._def_node_of[el.instance_name] = node
            self._read_groups(el, node, defq, site_cfg)
            self._read_ports(el, node, defq, site_cfg)
            self._read_table_attrs(el, node, defq, site_cfg)

    def _read_ports(self, el: Element, node, defq: str, site_cfg: dict) -> None:
        """FRAMEWORK CHANGE 8: there were three near-identical readers
        (_attach_transformation_def / _attach_source_def / _attach_target_def),
        each with nine hardcoded Informatica attribute names, and each element
        had exactly ONE port list read from ONE xpath. SSIS splits columns across
        two containment sites (inputs/.../inputColumn and
        outputs/.../outputColumn) with DIFFERENT attribute names on each side --
        inputs use cachedName/cachedDataType/cachedLength, outputs use
        name/dataType/length -- so port sites are now a list, each naming its own
        attributes and contributing a synthesised porttype."""
        for ps in site_cfg.get("port_sites", []):
            tag = self._tagpath(ps["xpath"])
            for idx, f in enumerate(node.findall(ps["xpath"]), start=1):
                nm = f.get(ps["name_attr"])
                if nm is None:
                    continue
                where = self.at(f, f"{defq}/{tag}[{idx}][@{ps['name_attr']}='{nm}']")
                # FRAMEWORK CHANGE 26: precision/scale were single hardcoded
                # attribute names, defaulted to 0 when absent. SSIS states
                # `length` for strings, `precision`+`scale` for numerics, and
                # nothing at all for i4 or dbDate -- so the attribute is a list of
                # candidates and "absent" must stay distinguishable from zero.
                prec, prec_attr, scale, scale_attr = self._precision_scale(f, ps)
                # FRAMEWORK CHANGE 9: porttype was always an attribute value.
                # SSIS states nothing: a column IS an input because of where it
                # sits. A port site may therefore assert its porttype.
                if ps.get("porttype_attr"):
                    porttype = f.get(ps["porttype_attr"], "")
                else:
                    porttype = ps.get("porttype", "")
                # FRAMEWORK CHANGE 10: the expression was always an attribute.
                # An SSIS derived column keeps it in the text of a nested
                # <property> element.
                expr = None
                expr_sfx = ""
                ex = ps.get("expression")
                if ex:
                    if ex["from"] == "ATTR":
                        expr = f.get(ex["attr"])
                        expr_sfx = self.attr_ref(f, ex["attr"])
                    elif ex["from"] == "TEXT":
                        en = f.find(ex["xpath"])
                        expr = en.text if en is not None else None
                        expr_sfx = "/" + self._tagpath(ex["xpath"]) + "/text()"
                # FRAMEWORK CHANGE 11: group membership was an attribute on the
                # port (TRANSFORMFIELD/@GROUP). In SSIS a column belongs to an
                # output because it is nested inside it, so membership is
                # resolved by ancestry.
                if ps.get("group_from") == "ANCESTOR":
                    group = self._group_of_node(f)
                elif ps.get("group_attr"):
                    group = f.get(ps["group_attr"])
                else:
                    group = None
                p = Port(
                    name=nm,
                    datatype=f.get(ps.get("datatype_attr") or "", ""),
                    precision=prec,
                    scale=scale,
                    porttype=porttype,
                    expression=expr,
                    default_value=f.get(ps.get("default_attr") or "", ""),
                    group=group,
                    ref_field=f.get(ps["ref_attr"]) if ps.get("ref_attr") else None,
                    where=where,
                    site=ps.get("id", tag),
                    lineage=f.get(ps["lineage_attr"]) if ps.get("lineage_attr") else None,
                    name_attr=ps["name_attr"],
                    datatype_attr=ps.get("datatype_attr", ""),
                    precision_attr=prec_attr,
                    scale_attr=scale_attr,
                    expr_where_suffix=expr_sfx,
                    node=f,
                )
                el.ports.append(p)
                if p.lineage and ps.get("lineage_role") == "DECLARE":
                    self._lineage_index[p.lineage] = (
                        el.instance_name, p.name,
                        p.where + self.attr_ref(p.node, p.name_attr))

    def _read_groups(self, el: Element, node, defq: str, site_cfg: dict) -> None:
        """FRAMEWORK CHANGE 12: the group reader hardcoded @NAME, @TYPE, @ORDER,
        @EXPRESSION and @DESCRIPTION. SSIS output groups carry name/isErrorOut/
        exclusionGroup and no condition at all."""
        gs = site_cfg.get("group_site")
        if not gs:
            return
        tag = self._tagpath(gs["xpath"])
        for idx, g in enumerate(node.findall(gs["xpath"]), start=1):
            nm = g.get(gs["name_attr"])
            rec = {
                "name": nm,
                "type": g.get(gs["type_attr"], "") if gs.get("type_attr") else "",
                "order": g.get(gs["order_attr"]) if gs.get("order_attr") else None,
                "expression": g.get(gs["expression_attr"]) if gs.get("expression_attr") else None,
                "where": self.at(g, f"{defq}/{tag}[{idx}][@{gs['name_attr']}='{nm}']"),
                "flags": {k: g.get(a) for k, a in gs.get("flag_attrs", {}).items()
                          if g.get(a) is not None},
            }
            el.groups.append(rec)
            self._group_node_of[id(g)] = nm

    def _read_table_attrs(self, el: Element, node, defq: str, site_cfg: dict) -> None:
        """FRAMEWORK CHANGE 13: hardcoded a.get('NAME') / a.get('VALUE'). SSIS
        component properties use lowercase @name and carry the value as element
        TEXT, not as an attribute."""
        at = site_cfg.get("attr_site")
        if not at:
            return
        # FRAMEWORK CHANGE 49: an element's properties were always a CHILD SITE of
        # name/value pairs -- Informatica TABLEATTRIBUTE, SSIS <property>, DataStage
        # Properties/DSSUBRECORD. A Kettle step has no such site: its configuration
        # IS its own set of child elements, whose names vary by step type
        # (<limit>/<never_ending> on a RowGenerator, <timeout>/<scaletime> on a
        # Delay). After the scalar lift those are the element node's own attributes,
        # so the site can be the element itself.
        if at.get("value_from") == "SELF_ATTRS":
            for key, v in node.attrib.items():
                el.table_attrs[key] = v
                el.table_attr_where[key] = el.where + self.attr_ref(node, key)
            return
        for a in node.findall(at["xpath"]):
            key = a.get(at["name_attr"])
            if key is None:
                continue
            if at.get("value_from") == "TEXT":
                el.table_attrs[key] = (a.text or "").strip()
            else:
                # FRAMEWORK CHANGE 36: this was `a.get(value_attr, "")`. It is the
                # SAME BUG CLASS the SSIS pass caught in the precision reader: an
                # ABSENT value silently became a stated empty string. MaskDemo.dsx
                # has 134 subrecords (of 1092) that state a Name and no Value at
                # all -- e.g. the APT SchemaFormat bag entry at dsx:362 -- and
                # coercing those to "" makes "the platform says nothing here"
                # indistinguishable from "the platform says the empty string".
                # Absent keys are now recorded separately and never enter
                # table_attrs.
                v = a.get(at["value_attr"]) if at.get("value_attr") else None
                if v is None:
                    el.valueless_attrs.append(key)
                else:
                    el.table_attrs[key] = v
            # FRAMEWORK CHANGE 42: an attr-site fact's `where` came from
            # structure.attr_where_template, a string with no node behind it, so
            # it carried no location at all. On DataStage those facts are the
            # MAJORITY of every connector stage's unmet obligations -- the
            # XMLProperties blob among them -- and "RESIDUE at a template" is not
            # a citation. The located `where` is now recorded per key.
            tpl = self.struct.get("attr_where_template")
            if tpl:
                # FRAMEWORK CHANGE 63 (a): the template is RELATIVE to the site
                # node, so on a platform whose properties live on a DEFINITION the
                # citation named no node at all -- "TABLEATTRIBUTE[@NAME='Sql
                # Query']/@VALUE" is true of every transformation in the file.
                # Anchoring it at the def query makes it checkable, which is the
                # whole point of FRAMEWORK CHANGE 42. The prefix comes from `at`
                # exactly once, at the leaf (see FRAMEWORK CHANGE 30b).
                rel = tpl.format(key=key)
                el.table_attr_where[key] = self.at(a, f"{defq}/{rel}" if defq else rel)

    # -- reference index ---------------------------------------------------

    def _index_refs(self) -> None:
        """FRAMEWORK CHANGE 14 (new machinery): index every addressable id in the
        document so a port-level reference can be resolved to its owning element.
        Informatica needed none of this: a CONNECTOR names the instance directly.
        An SSIS <path> names an OUTPUT and an INPUT, never the components."""
        for attr in self.struct.get("ref_attrs", []):
            for node in self.root.iter():
                v = node.get(attr)
                if v is not None:
                    # FRAMEWORK CHANGE 31 (ARCHITECTURAL A5, second half): the ref
                    # index was document-global. In a .dsx the pin id V0S0P1 exists
                    # in three different jobs, so a global index resolves an edge
                    # endpoint into whichever job happened to be exported first.
                    self._ref_index.setdefault((self._scope_of(node), v), node)

    # -- edges -------------------------------------------------------------

    def _identify_edges(self) -> None:
        """FRAMEWORK CHANGE 15: edge reading hardcoded four Informatica attribute
        names (FROMINSTANCE, FROMFIELD, TOINSTANCE, TOFIELD) and assumed one edge
        record carries BOTH endpoints AND the field pair. SSIS splits those two
        jobs across two unrelated places: <path> carries element-level endpoints
        with no field detail, and field detail lives on the DOWNSTREAM column as
        a lineageId back-reference."""
        for lv in self.struct.get("edge_levels", []):
            q = lv["xpath"]
            # FRAMEWORK CHANGE 62: A DIRECTION FILTER SEPARATE FROM THE SITE QUERY.
            #
            # An edge level had exactly one selector -- its xpath -- so "which nodes are
            # edges" and "which END of the edge is this" had to be the same question. For
            # every platform so far they were: an Informatica CONNECTOR and an SSIS <path>
            # each state both endpoints, and an ADF dependsOn entry states its direction by
            # being a dependsOn.
            #
            # A .dsx states neither. It HAS NO LINK OBJECT AT ALL: one link is TWO peer
            # records pointing at each other through Partner, and nothing in the shape of
            # either record says which is upstream. The direction is carried by a per-pin
            # CLASS attribute whose vocabulary varies by stage family. Folding that into the
            # xpath -- one edge level per class, which is what this table did -- makes every
            # class the table has not enumerated SILENTLY INVISIBLE, and that was the
            # measured defect: DataStage emitted 0 edges on a 3-link document because two
            # levels named CCustomOutput/CJSActivityOutput and the document states
            # CustomOutput/CTrxOutput.
            #
            # The site query now matches BOTH halves of every pair and the table says which
            # half to read. Both the attribute name and the value set come from the table,
            # so no source vocabulary reaches this file; and because the unread half is now
            # MATCHED rather than unmatched, `_audit_pin_pairs` can account for every link
            # record in the document and report the ones no declared class covers.
            pp = (self.table["edge_policy"].get("pin_pairs")
                  if lv.get("direction") == "PIN_PAIR" else None)
            for idx, c in enumerate(self.root.findall(q), start=1):
                if pp is not None and c.get(pp["class_attr"]) not in pp["output_classes"]:
                    # The peer half of a pair already read from the other side, or a class
                    # the table does not know. `_audit_pin_pairs` tells those two apart.
                    # `idx` deliberately keeps counting: it is the node's position among
                    # ALL matches of `q`, which is what makes the `where` string an address
                    # that resolves rather than a running total of the ones we kept.
                    continue
                where = self.at(c, f"{q}[{idx}]")
                if lv["endpoint_kind"] == "ELEMENT_KEY":
                    # FRAMEWORK CHANGE 66 (c): both endpoints go through
                    # `_scoped_ref`. They were raw, and element keys are not.
                    self.field_edges.append(FieldEdge(
                        from_instance=self._scoped_ref(c, c.get(lv["from_attr"])),
                        from_field=c.get(lv["from_field_attr"]),
                        to_instance=self._scoped_ref(c, c.get(lv["to_attr"])),
                        to_field=c.get(lv["to_field_attr"]),
                        where=where,
                        # The edge element states the upstream field itself, so the
                        # address of `from_field` is this node's own attribute.
                        from_field_where=where + self.attr_ref(c, lv["from_field_attr"]),
                    ))
                elif lv["endpoint_kind"] == "PORT_REF":
                    # FRAMEWORK CHANGE 35: both endpoints were assumed to be
                    # REFERENCES carried by a third element. An SSIS <path> is
                    # exactly that. A DataStage link record IS one of its own two
                    # endpoints: the CCustomOutput record under stage A carries
                    # Partner "B|Bpin" and nothing else, so `from` is the record's
                    # own owner. from_attr null now means "this node".
                    scope = self._scope_of(c)
                    a = (c if lv.get("from_attr") is None
                         else self._ref_index.get((scope, c.get(lv["from_attr"]))))
                    # FRAMEWORK CHANGE 50: CHANGE 35 made `from_attr` null mean
                    # "this node", because a DataStage CCustomOutput record sits
                    # under its own upstream stage. An ADF `dependsOn` entry is the
                    # MIRROR IMAGE: it sits under its own DOWNSTREAM activity and
                    # names the predecessor, because an ADF dependency points
                    # backwards (learn.microsoft.com/.../concepts-pipelines-activities:
                    # "Activity 2 depends on the Activity 1 succeeding"). So `to`
                    # also has to be able to mean "this node". Without the mirror
                    # the only way to read an ADF edge is to invert the graph in
                    # the table, which would put the direction of every edge in a
                    # place no reviewer would look for it.
                    b = (c if lv.get("to_attr") is None
                         else self._ref_index.get((scope, c.get(lv["to_attr"]))))
                    rec = {
                        "from": self._owner_element_of(a) if a is not None else None,
                        "to": self._owner_element_of(b) if b is not None else None,
                        "label": c.get(lv["label_attr"]) if lv.get("label_attr") else None,
                        "where": where,
                        "field_edges": [],
                    }
                    if rec["from"] and rec["to"]:
                        self.element_edge_records.append(rec)
                    else:
                        # FRAMEWORK CHANGE 62 (b): an endpoint that did not resolve used
                        # to vanish with no record of it, which is how a document could
                        # report "0 edges" and look like a document with no links.
                        self.unresolved_edges.append({
                            "where": where,
                            "reason": ("neither endpoint resolved" if not (rec["from"] or rec["to"])
                                       else f"only the {'from' if rec['from'] else 'to'} "
                                            f"endpoint resolved"),
                        })
                    if pp is not None:
                        # The RESOLVED endpoint nodes are kept, not re-derived later.
                        # Re-deriving them in the audit meant re-splitting the compound
                        # partner value there, which would have put the '|' separator --
                        # a DataStage format literal -- into this file. The nodes the
                        # sweep already resolved carry the same information with no
                        # vocabulary attached.
                        self._pin_pair_seen[id(c)] = {"rec": rec, "from_node": a,
                                                      "to_node": b}

        # FRAMEWORK CHANGE 16 (new machinery): field-level edges reconstructed
        # from downstream lineage back-references.
        lin = self.struct.get("lineage")
        if lin:
            for el in self.elements.values():
                for p in el.ports:
                    if p.porttype not in lin["referencing_porttypes"]:
                        continue
                    up = self._lineage_index.get(p.lineage or "")
                    if up is None:
                        continue
                    self.field_edges.append(FieldEdge(
                        from_instance=up[0], from_field=up[1],
                        to_instance=el.instance_name, to_field=p.name,
                        where=p.where + self.attr_ref(p.node, lin["reference_attr"]),
                        # NOT this node's lineageId, whose value is an opaque id and not
                        # a field name. The upstream DECLARATION is where the name is
                        # stated, and the lineage index kept its address for exactly this.
                        from_field_where=up[2],
                    ))

        self._audit_pin_pairs()

    # -- FRAMEWORK CHANGE 62 (c): the pin-pair completeness audit --------------

    def _endpoint_is_declared_owner(self, node) -> bool:
        """True when an endpoint reference lands on, or one step under, an element.

        The endpoint of a pin-pair edge is found by walking from the referenced node
        to the nearest ANCESTOR that is an identified element. That walk has no stop
        condition, so when a pin's own declaring record is NOT an element the walk
        keeps going and lands on whatever container is above it -- and the edge then
        asserts a link between the upstream stage and a CONTAINER, which the document
        does not state. This predicate is what makes that case countable: a legitimate
        reference either names an element outright (the compound Partner form names the
        partner stage) or names a child of one (the bare Partner form names the partner
        pin, whose declared owner is that stage). Anything deeper is a fall-through.

        Deliberately vocabulary-free: it asks the ancestry index, never a tag or an
        attribute, so it holds for any platform that declares pin_pairs."""
        if id(node) in self._element_of_node:
            return True
        p = self._parent.get(node)
        return p is not None and id(p) in self._element_of_node

    def _audit_pin_pairs(self) -> None:
        """FRAMEWORK CHANGE 62 (c): account for EVERY link record in the document.

        `pin_pairs` selects one half of each pair by a CLOSED class list, and a closed
        list is only honest with a total-coverage check beside it -- otherwise a class
        the table has never seen produces no edge, no error and no mention, which is
        exactly the 3-links-0-edges state this change was written to fix. The audit
        divides every marker-bearing record into output half, input half, or
        UNCLASSIFIED, and counts the two ways a selected record can still fail to
        become a truthful edge (unresolved partner, fall-through endpoint).

        Reported, never raised. A hard failure here would refuse whole documents over a
        single unknown pin class, which loses more than it protects; and the numbers are
        printed unconditionally so `edges: 0` can never again read as `links: 0`."""
        pp = self.table["edge_policy"].get("pin_pairs")
        if not pp:
            return
        marker, cattr = pp["marker_attr"], pp["class_attr"]
        out_cls, in_cls = set(pp["output_classes"]), set(pp["input_classes"])
        audit = {"marker_records": 0, "output_half": 0, "input_half": 0,
                 "unclassified": [], "unresolved": [], "fallthrough": []}
        # Deliberately does NOT restate an edge count. `element_edge_records` may hold
        # records from edge levels that are not pin-pair levels, so a number here would
        # be right on this platform and wrong the moment a second level is added -- and
        # the driver prints the real edge count on the line above this one anyway.
        for node in self.root.iter():
            if node.get(marker) is None:
                continue
            audit["marker_records"] += 1
            # `node.tag` is READ from the projection, not written here, so the citation
            # names the record class without this file knowing what a record is called.
            site = self.at(node, node.tag)
            cls = node.get(cattr)
            if cls in out_cls:
                audit["output_half"] += 1
                seen = self._pin_pair_seen.get(id(node))
                rec = seen["rec"] if seen else None
                if rec is None or not (rec["from"] and rec["to"]):
                    audit["unresolved"].append(
                        {"where": site + self.attr_ref(node, marker),
                         "class": cls, "partner": node.get(marker)})
                    continue
                for endpoint in ("from", "to"):
                    ref = seen[f"{endpoint}_node"]
                    if ref is not None and not self._endpoint_is_declared_owner(ref):
                        audit["fallthrough"].append(
                            {"where": site + self.attr_ref(node, marker),
                             "endpoint": endpoint, "resolved_to": rec[endpoint],
                             "class": cls})
            elif cls in in_cls:
                audit["input_half"] += 1
            else:
                audit["unclassified"].append(
                    {"where": site + self.attr_ref(node, cattr),
                     "class": cls, "partner": node.get(marker)})
        audit["balances"] = (audit["marker_records"]
                             == audit["output_half"] + audit["input_half"])
        self.link_audit = audit

    # -- the exhaustive census ----------------------------------------------

    def _projection_path(self, node) -> str:
        """An ElementTree xpath from the root to `node`, with sibling positions.

        FRAMEWORK CHANGE 67 (ADDITION 2). An Unknown Object has to be citable or it
        is not an inventory entry, and it has no key_attr to cite by -- that is what
        makes it unknown. So the citation is its POSITION, written in the same query
        language the level queries use, which means a reviewer can paste it back into
        `root.findall` and land on the same node. On a projected tree this is a
        location in the PROJECTION, which is exactly why `at()` puts the front-end's
        own byte/pointer location in front of it (ARCHITECTURAL CHANGE A3)."""
        steps: list[str] = []
        cur = node
        while True:
            parent = self._parent.get(cur)
            if parent is None:
                break
            same = [c for c in parent if c.tag == cur.tag]
            steps.append(f"{cur.tag}[{same.index(cur) + 1}]")
            cur = parent
        if not steps:
            return "."
        steps.reverse()
        return "./" + "/".join(steps)

    def _is_value_carrier(self, node) -> bool:
        """Is this node a SCALAR the projection lifted, rather than a record?

        Structural and platform-neutral: no tag, attribute or type name appears
        here. A node qualifies when it has no element children AND no attributes of
        its own AND either
          (a) its parent carries an attribute of the same name whose value is
              exactly this node's text -- i.e. the front-end lifted it, and the fact
              is already inventoried as the parent's attribute; or
          (b) it states no text at all -- a key stated with no value, which the
              front-end already reports in its own `unaccounted` line.

        MEASURED on Pentaho: a .ktr contains ZERO XML attributes, so every value is
        the text of a child element and `ktrdoc._lift` copies it onto the parent
        WITHOUT removing the child (removing it would break the citation `attr_ref`
        produces). 274 of safe-stop-gen-rows.ktr's 437 projected nodes are those
        copies. Counting them as unrecognised records would put 274 entries in an
        inventory of things that are not records, which is the failure mode this
        whole change has to avoid."""
        if len(node) or node.attrib:
            return False
        parent = self._parent.get(node)
        if parent is None:
            return False
        text = (node.text or "").strip()
        lifted = parent.get(node.tag)
        if lifted is not None and lifted == text:
            return True
        return not text

    def _exclusion_nodes(self, rule: dict) -> set[int]:
        """The node set one declared exclusion rule covers.

        FOUR rule kinds, and the split is between "the table names it" and "the
        framework can prove it".

        QUERY                 an xpath in the SAME query language as the levels. The
                              table names every tag, so the rule is reviewable by a
                              human reading the table -- which is the whole point of
                              declaring exclusions rather than dropping records.
        EDGE_RECORD           the node was matched by one of this platform's own
                              `edge_levels` queries, so it is inventoried as an EDGE.
                              Derived from the table's existing edge declarations;
                              nothing new is declared and nothing can drift.
        DEFINITION_OF_ELEMENT the node IS the resolved definition node of an
                              identified element, so its payload is already read
                              through `def_sites`. Self-auditing: a definition record
                              that no element references does NOT match, and stays
                              an Unknown Object.
        VALUE_CARRIER         a scalar the projection lifted, or a key stated with no
                              value. Structural -- see `_is_value_carrier`.

        `subtree: true` extends a rule to the matched node AND its descendants, for
        a wholesale exclusion (an export envelope, a logging configuration block).
        It is the one place a single rule can hide many records, so a rule that uses
        it must say so in its own `why` text and its count is reported per rule.
        """
        kind = rule["kind"]
        if kind == "QUERY":
            # `match` is one xpath or a LIST of them. A list keeps ONE reason text
            # over several paths that are excluded for the SAME reason -- an export
            # envelope is three wrapper tags and one argument, and splitting it into
            # three rules would triple the text a reviewer has to read to disagree.
            paths = rule["match"]
            if isinstance(paths, str):
                paths = [paths]
            hits = [n for p in paths for n in self.root.findall(p)]
        elif kind == "EDGE_RECORD":
            hits = []
            for lv in self.struct.get("edge_levels", []):
                hits.extend(self.root.findall(lv["xpath"]))
        elif kind == "DEFINITION_OF_ELEMENT":
            # ONLY where the definition is a DIFFERENT node than the element. A
            # `def_site` of "SELF" means the element carries its own payload, so its
            # def node IS its own node -- excluding that would be an exclusion rule
            # claiming an identified element is not one. MEASURED on Informatica:
            # kind_dispatch["Target Definition"].def_site is "SELF", so one INSTANCE
            # per mapping resolves to itself and was reported as `contested` until
            # this filter existed.
            hits = [n for key, n in self._def_node_of.items()
                    if n is not None and n is not self._node_of.get(key)]
        elif kind == "VALUE_CARRIER":
            hits = [n for n in self.root.iter() if self._is_value_carrier(n)]
        else:
            raise ValueError(
                f"structure.census.exclusions[{rule.get('id')!r}]: unknown kind "
                f"{kind!r}. Kinds are QUERY, EDGE_RECORD, DEFINITION_OF_ELEMENT, "
                "VALUE_CARRIER.")
        if rule.get("subtree"):
            out: set[int] = set()
            for n in hits:
                out.update(id(x) for x in n.iter())
            return out
        return {id(n) for n in hits}

    def _census(self) -> None:
        """FRAMEWORK CHANGE 67 (ADDITION 2): EXHAUSTIVE ELEMENT IDENTIFICATION.

        THE DEFECT THIS CLOSES, as measured. `_identify_elements` appends to
        `self.declared` INSIDE the level loop, so `declared` counted only what a
        level query matched. A record no level matched was not counted as lost and
        was not counted at all -- the ledger's denominator was its own output, so it
        could not report an element it never saw. MEASURED on
        CustomerSummaryDerive.dsx: 5 elements in the document, ledger reported
        `declared=4 identified=4 lost=0 balances=True`, and the invisible record was
        the CTransformerStage that holds every derivation in the job.

        THE DESIGN, and why it is not simply "count everything unmatched as lost".
        On the five canonical documents the projection holds 82 / 78 / 1341 / 437 /
        34 nodes against 7 / 3 / 43 / 4 / 3 elements. Most of the remainder are not
        elements by any reading -- a DSSUBRECORD is one property row, a lifted .ktr
        leaf is one scalar, a POWERMART/REPOSITORY/FOLDER wrapper is an export
        envelope. An inventory of 1298 "unknown objects" for MaskDemo.dsx tracks
        nothing. So the shape is DECLARED EXCLUSIONS, THEN UNKNOWNS:

          * a level query matches it            -> an element (or keyless), as before
          * a DECLARED EXCLUSION RULE matches it -> excluded, and the rule is named,
            reasoned and counted, so a human can inspect the exclusion list and
            argue with it
          * neither                              -> an UNKNOWN OBJECT, inventoried
            with a citable location

        The asymmetry is deliberate. A table that excludes too much is a table
        someone can read and dispute; a sweep that drops records silently is not.
        The failure mode is a NOISY BUT HONEST inventory, and a large unknown count
        is the expected first result rather than something to tune away.

        WHAT IS AND IS NOT AN ASSERTION HERE. `unknown` is the COMPLEMENT of
        matched-plus-excluded, so `records == matched + excluded + unknown` is true
        by construction and asserting it proves nothing. The checks that can
        actually fail, and are therefore the ones `accounting()` reports:
          * `len(self._matched_nodes) == len(self.declared)` -- no node was matched
            by two levels, which would double-count it in the element ledger;
          * keyed matched nodes == identified + lost -- the element DICT closes
            against the node set it came from;
          * `census_contested` empty -- no exclusion rule claims a node that a level
            query also matched, which would be a table asserting both that a record
            is an element and that it is not one.
        """
        cfg = self.struct.get("census") or {}
        identity_attrs = cfg.get("identity_attrs") or []
        rules = cfg.get("exclusions") or []
        resolved = [(r, self._exclusion_nodes(r)) for r in rules]

        self.excluded_by_rule = {r["id"]: 0 for r in rules}
        nodes = list(self.root.iter())
        self.record_count = len(nodes)

        for node in nodes:
            hits = [r for r, ids in resolved if id(node) in ids]
            if id(node) in self._matched_nodes:
                # A rule claiming an element is a contradiction in the table, not a
                # judgement call. Reported, and the LEVEL wins -- identification is
                # never overridden by an exclusion.
                for r in hits:
                    self.census_contested.append({
                        "rule": r["id"],
                        "level": self._matched_nodes[id(node)],
                        "where": self.at(node, self._projection_path(node)),
                    })
                continue
            if hits:
                if len(hits) > 1:
                    self.census_overlaps.append({
                        "kind": "TWO_RULES_MATCHED_ONE_NODE",
                        "tag": node.tag,
                        "attributed_to": hits[0]["id"],
                        "also": [r["id"] for r in hits[1:]],
                    })
                # FIRST RULE IN TABLE ORDER WINS, so attribution is deterministic
                # and a reader can reproduce it from the table alone.
                self.excluded_by_rule[hits[0]["id"]] += 1
                self.excluded.append({
                    "rule": hits[0]["id"],
                    "tag": node.tag,
                    "where": self.at(node, self._projection_path(node)),
                    "identity": {a: node.get(a) for a in identity_attrs
                                 if node.get(a) is not None},
                })
                continue
            path = self._projection_path(node)
            self.unknown_objects.append(UnknownObject(
                where=self.at(node, path),
                where_path=path,
                tag=node.tag,
                depth=path.count("/"),
                container=self._owner_element_of(node),
                identity={a: node.get(a) for a in identity_attrs
                          if node.get(a) is not None},
                attrs=dict(node.attrib),
                child_count=len(node),
            ))

    # -- table-driven collapse ---------------------------------------------

    def _apply_collapse(self) -> None:
        """FRAMEWORK CHANGE 17: the collapse rule value
        'INTO_ASSOCIATED_SOURCE_QUALIFIER' and the role string 'SOURCE' it
        assigned were both Informatica vocabulary in framework code."""
        for name, el in list(self.elements.items()):
            rule = self.table["kind_dispatch"].get(el.kind_raw, {}).get("collapse")
            if not rule:
                continue
            host = next((h for h in self.elements.values() if h.associated == name), None)
            if host is None:
                continue
            host.absorbed.append(name)
            if rule.get("carry_harvest"):
                host.harvested = el.harvested
            if rule.get("set_host_role"):
                host.role = rule["set_host_role"]
            self.dropped_instances[name] = el
            del self.elements[name]

    # -- derived views ------------------------------------------------------

    def inbound(self, instance: str) -> list[FieldEdge]:
        return [e for e in self.field_edges if e.to_instance == instance]

    def outbound(self, instance: str) -> list[FieldEdge]:
        return [e for e in self.field_edges if e.from_instance == instance]

    def resolved_instance(self, instance: str) -> str:
        for name, el in self.elements.items():
            if instance == name or instance in el.absorbed:
                return name
        return instance

    def element_edges(self) -> list[dict]:
        """FRAMEWORK CHANGE 18: element edges were ALWAYS derived by collapsing
        field-level connectors. SSIS states them explicitly as <path> elements,
        so the derivation is now one of two table-selected mechanisms."""
        mech = self.table["edge_policy"]["element_edges_from"]
        if mech == "EXPLICIT_EDGE_ELEMENTS":
            out = []
            for rec in self.element_edge_records:
                a, b = self.resolved_instance(rec["from"]), self.resolved_instance(rec["to"])
                if a == b:
                    continue
                fes = [fe for fe in self.field_edges
                       if self.resolved_instance(fe.from_instance) == a
                       and self.resolved_instance(fe.to_instance) == b]
                out.append({"from": a, "to": b, "field_edges": fes,
                            "label": rec["label"], "where": rec["where"]})
            return out

        seen: dict[tuple[str, str], dict] = {}
        for fe in self.field_edges:
            a = self.resolved_instance(fe.from_instance)
            b = self.resolved_instance(fe.to_instance)
            if a == b:
                continue
            key = (a, b)
            if key not in seen:
                seen[key] = {"from": a, "to": b, "field_edges": [], "label": None,
                             "where": None}
            seen[key]["field_edges"].append(fe)
        if self.table["edge_policy"]["label_source"] == "OUTPUT_GROUP_NAME_WHEN_PRESENT":
            for (a, _b), e in seen.items():
                up = self.elements.get(a)
                if not up or not up.groups:
                    continue
                labels = {p.group for fe in e["field_edges"] for p in up.ports
                          if p.name == fe.from_field and p.group}
                if len(labels) == 1:
                    e["label"] = labels.pop()
        return list(seen.values())

    def rename_map(self, instance: str) -> dict[str, str]:
        """local port name -> upstream field name, for inbound connectors."""
        return {fe.to_field: fe.from_field for fe in self.inbound(instance)}


def declarable_roles(table: dict) -> set:
    """Every role value this table can produce for an element.

    Two sources and no others, both table-declared:
      kind_dispatch[*].role          -- stated per element kind.
      structure.levels[*].role_from  -- DERIVED, e.g. DataStage's PIN_DIRECTION,
                                        whose `roles` map is the closed set of
                                        outcomes.
    A level with `role_attr` reads the role out of the DOCUMENT, which is an OPEN
    vocabulary and cannot be enumerated from the table -- that is exactly what
    `unmapped_role_node_type` exists for, so such a level contributes nothing here
    and its coverage stays the fallback's job."""
    roles = set()
    for entry in table.get("kind_dispatch", {}).values():
        if isinstance(entry, dict) and entry.get("role"):
            roles.add(entry["role"])
    for lvl in table.get("structure", {}).get("levels", []):
        rf = lvl.get("role_from") or {}
        roles.update((rf.get("roles") or {}).values())
    return roles


# WHAT A DECLARED BLOCK MUST CARRY, AND WHAT A DETAIL TEMPLATE MAY NAME.
#
# Both of these exist because a blind authoring run died on a bare `KeyError` naming
# neither the block that was short a key nor the key's whereabouts. MEASURED, once each,
# on the two cold runs of 2026-08-24:
#
#   `KeyError: 'key_attr'`. The Informatica author found TARGETLOADORDER in the document,
#   declared `structure.load_order` correctly, and named the attribute holding the target
#   `target_attr` -- an accurate name for what it holds. The reader subscripts `key_attr`.
#   NOT ONE of the five prior-art tables staged in the authoring view declares a
#   `load_order` block, because Informatica is the only platform here that has one and its
#   table is precisely the one withheld from a blind Informatica run. So the block's shape
#   was unavailable by construction, and 4 minutes of authoring bought one word.
#
#   `KeyError: 'field'`. The Alteryx author wrote a PORT-family rule whose `detail` said
#   `{field}` and `{rename}`. The formatter supplies six names and `field` is not among
#   them (`name` is). No prior-art table demonstrates the vocabulary, so it was guessed,
#   plausibly, and wrongly.
#
# The vocabularies below are therefore not documentation: they are the check. A `detail`
# template is a table-authored format string against a CLOSED keyword set that the author
# cannot see from the shapes, which makes it exactly the kind of thing that must fail at
# load time with the vocabulary printed, rather than mid-emission with a KeyError. Rule
# families whose vocabulary comes from the DOCUMENT (HARVEST spreads a harvested bag,
# GROUP spreads a group record) are open and deliberately absent -- there is no closed set
# to check them against.
NO_SLOT_DETAIL_VOCABULARY = {
    "PORT": ("default_value", "disposition", "name", "datatype", "lineage", "group"),
    "FIELD_EDGE": ("from_instance", "from_field", "to_field"),
    "CONTAINER": ("container",),
}

# Keys a declared `structure` block's reader subscripts outright. Declaring the block at
# all is optional; declaring it short of these is not a smaller block, it is a crash.
REQUIRED_STRUCTURE_BLOCK_KEYS = {
    "load_order": ("xpath", "key_attr", "order_attr"),
}


def validate_table(table: dict) -> dict:
    """Static table checks: a DECLARED READER MUST BE REACHABLE, and a DECLARABLE
    VALUE MUST BE MAPPED. Raises on either. Returns the table so it can wrap a load.

    WHY THIS EXISTS AS A CHECK AND NOT AS A REVIEW HABIT. `_attach_definitions`
    already raises the OTHER direction -- a kind naming a def site the table does not
    declare -- and that check was added because `def_site: "RESOLVED"` had silently
    given every Informatica Filter no ports and no property bag. THIS is the mirror
    defect and it shipped in the same table: `structure.def_sites.target` declares a
    TARGETFIELD port site, and `kind_dispatch['Target Definition'].def_site` was
    'SELF', so NO dispatch path ever reached it. MEASURED consequence on
    m_CUSTOMER_SUMMARY_fullname_birthyear.xml: the document declares
    `BirthYear DATATYPE="number(p,s)" PRECISION="4"` at line 14 and the IR mart node
    said integer / precision 10 -- the UPSTREAM Expression port width from line 40 --
    because with no ports of its own the target was filled by column propagation. A
    narrower target column silently widened, and an unfed target column undetectable.
    Both directions are now loud, because the failure mode is identical in both: a
    reader that is never called and a name that never resolves are the same silence.

    ROLE COVERAGE is the same shape one level up. platform_ssis.json's
    `role_to_node_type` declared SOURCE / TRANSFORMATION / TASK and no TARGET while
    its own kind_dispatch declares `role: "TARGET"` for Microsoft.OLEDBDestination,
    so every OLE DB Destination took the unmapped fallback and was emitted with
    node type "unknown". The table's `unmapped_role_reason` said that path was
    "untested here because every componentClassID in the fixture is mapped" -- true
    of KINDS and irrelevant to ROLES, which is why a prose note is not a check.

    NEITHER CHECK NEEDS A DOCUMENT, deliberately: both defects are properties of the
    table alone, and both survived every document this spike runs because a fixture
    that happens not to contain the element proves nothing about the table."""
    st = table.get("structure", {})

    declared = set(k for k in (st.get("def_sites") or {}) if not k.startswith("_"))
    named = {st.get("default_def_site", "SELF")}
    for entry in table.get("kind_dispatch", {}).values():
        if isinstance(entry, dict) and entry.get("def_site"):
            named.add(entry["def_site"])
    unreachable = sorted(declared - named)
    if unreachable:
        raise ValueError(
            f"structure.def_sites declares {unreachable}, and no kind_dispatch entry "
            f"names it as its `def_site` (named: {sorted(named)}). Every port site, "
            f"harvest and property site under an unreachable def site is dead: the "
            f"table reads as coverage and the reader is never called.")

    declared_self = set(k for k in (st.get("self_def_sites") or {}) if not k.startswith("_"))
    named_self = set()
    for entry in table.get("kind_dispatch", {}).values():
        if isinstance(entry, dict) and entry.get("self_def_site"):
            named_self.add(entry["self_def_site"])
    unreachable_self = sorted(declared_self - named_self)
    if unreachable_self:
        raise ValueError(
            f"structure.self_def_sites declares {unreachable_self}, and no "
            f"kind_dispatch entry names it as its `self_def_site` (named: "
            f"{sorted(named_self)}). Same defect one site kind over.")

    r2n = table.get("role_to_node_type") or {}
    mapped = set(k for k in r2n
                 if not k.startswith("_")
                 and k not in ("unmapped_role_node_type", "unmapped_role_reason",
                               "known_defect"))
    missing = sorted(declarable_roles(table) - mapped)
    if missing:
        raise ValueError(
            f"role_to_node_type does not map {missing}, and this table can produce "
            f"{'that role' if len(missing) == 1 else 'those roles'} -- from "
            f"kind_dispatch[*].role or from a level's role_from.roles. The unmapped "
            f"fallback would fire on an element whose role the table DID determine, "
            f"emitting node type "
            f"{r2n.get('unmapped_role_node_type', 'unknown')!r} for it.")

    # EVERY violation of these two, not the first.
    #
    # MEASURED, and it cost an authoring pass to learn: a blind Alteryx table wrote the
    # same wrong template twice, in `yxmd_select_field_rename` and in
    # `yxmd_summarize_action`. Told about the first, the author fixed exactly the first --
    # correctly, because the repair instruction says not to touch what the validator has
    # not objected to -- and the second cost another attempt to be told about in identical
    # words. A check that can enumerate its own domain cheaply has no excuse for reporting
    # one instance of a class at a time.
    problems: list[str] = []

    for block, required in sorted(REQUIRED_STRUCTURE_BLOCK_KEYS.items()):
        declared = st.get(block)
        if not isinstance(declared, dict):
            continue
        absent = [k for k in required if k not in declared]
        if absent:
            present = sorted(k for k in declared if not k.startswith("_"))
            problems.append(
                f"structure.{block} is declared without {absent}. Its reader "
                f"subscripts every one of {list(required)}, so the block as written "
                f"raises KeyError the first time a document matches it. Declared "
                f"here: {present}. If one of those is the value {absent[0]!r} should "
                f"hold, rename it -- the reader knows the key, not the meaning.")

    for rule in table.get("no_slot_facts") or []:
        if not isinstance(rule, dict):
            continue
        vocabulary = NO_SLOT_DETAIL_VOCABULARY.get(rule.get("from"))
        tpl = rule.get("detail")
        if not vocabulary or not tpl:
            continue
        try:
            named = {f for _, f, _, _ in Formatter().parse(tpl) if f}
        except ValueError as ex:
            problems.append(
                f"no_slot_facts[{rule.get('id')!r}].detail is not a parseable format "
                f"string: {ex}")
            continue
        unknown = sorted(n.split(".")[0].split("[")[0] for n in named
                         if n.split(".")[0].split("[")[0] not in vocabulary)
        if unknown:
            problems.append(
                f"no_slot_facts[{rule.get('id')!r}].detail names {unknown}, which its "
                f"{rule['from']} formatter does not supply. That template may only "
                f"name {list(vocabulary)}. The detail string is rendered per "
                f"{rule['from'].lower().replace('_', ' ')}, and a name outside that "
                f"set raises KeyError at emission, not here, unless this check "
                f"catches it.")

    if problems:
        if len(problems) == 1:
            raise ValueError(problems[0])
        raise ValueError(
            "%d table defects of the same kind, all of which must be fixed:\n%s"
            % (len(problems), "\n".join(f"  ({i}) {p}" for i, p in enumerate(problems, 1))))

    return table


class TableContractError(KeyError):
    """A table was read for a key it does not declare, and the read said where.

    A KeyError subclass so that anything already catching KeyError around a table read
    keeps catching it, with `__str__` overridden because KeyError renders `args[0]` through
    `repr` and would turn a located message back into a bare quoted word.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._message = message

    def __str__(self) -> str:
        return self._message


class TableSection(dict):
    """A table sub-object that knows where in the table it lives.

    WHY THE TABLE CARRIES THIS RATHER THAN EACH READER CHECKING.
    identify.py and emit.py subscript table-authored dicts in over a hundred places, and a
    missing key at any of them raises `KeyError: 'xpath'` -- a word, with no block, no
    platform and no line of the table. MEASURED across four blind authoring runs: the same
    shape of failure landed on `structure.load_order` (`key_attr`), on
    `structure.def_sites.<name>` (`xpath`), and twice inside `no_slot_facts` rules, and
    each one cost an authoring pass to identify by hand from a traceback.

    Enumerating required keys per block, which is what the first fix did, only covers
    UNCONDITIONAL requirements -- and most of these are conditional, needed on the paths a
    particular kind dispatches through and absent-by-design elsewhere. A static list cannot
    express that without either missing cases or refusing tables that work.

    Locating the read solves it from the other side: `.get()` is untouched, so every
    optional read stays optional, and a MANDATORY read that comes up empty names the block
    it was reading and the keys that block declares. No reader changes, and a key added to
    the framework tomorrow is covered the day it is added.
    """

    __slots__ = ("_table_path",)

    def __init__(self, data: dict, table_path: str) -> None:
        super().__init__(data)
        self._table_path = table_path

    def __missing__(self, key):
        declared = sorted(k for k in self if not str(k).startswith("_"))
        raise TableContractError(
            f"{self._table_path} does not declare {key!r}, and its reader requires it. "
            f"That block declares: {declared or 'nothing'}. If one of those holds the "
            f"value {key!r} should, rename it -- the reader knows the key, not the "
            f"meaning.")


def _locate(value, table_path: str):
    """Recursively re-home the table's dicts so each one knows its own path."""
    if isinstance(value, dict):
        return TableSection(
            {k: _locate(v, f"{table_path}.{k}") for k, v in value.items()}, table_path)
    if isinstance(value, list):
        return [_locate(v, f"{table_path}[{i}]") for i, v in enumerate(value)]
    return value


def load_table(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return _locate(validate_table(json.load(fh)), "table")
