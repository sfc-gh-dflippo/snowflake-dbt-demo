"""JSON front-end: projects an Azure Data Factory pipeline into a queryable tree.

This is the THIRD format family. XmlDocument reads a markup tree; dsxdoc reads a
line-oriented record-block text; a pipeline JSON is neither.

Format facts, each from Microsoft's own documentation:
  * top-level `name` + `properties`; `properties.activities[]` required; an
    activity has name / type / typeProperties / policy / dependsOn --
    https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities
  * `dependsOn[].activity` names the PREDECESSOR that must run first, so the
    dependency points BACKWARDS; `dependencyConditions` is exactly one of
    Succeeded / Failed / Skipped / Completed -- same URL
  * `{"value": "@...", "type": "Expression"}` is the expression wrapper; `@`
    introduces an expression and `@@` escapes a literal `@` --
    https://learn.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions

FOUR projection rules. Each exists because JSON states something XML states by a
different mechanism, or states something XML cannot state at all.

PROJECTION RULE 1 -- OBJECT IS A NODE, SCALAR IS AN ATTRIBUTE.
    An object becomes an element tagged with the key that reached it; its scalar
    members become attributes of that element. This is what lets the framework's
    single query language reach a pipeline.

PROJECTION RULE 2 -- AN ARRAY OF OBJECTS IS REPEATED SIBLINGS.
    `"activities": [ {...}, {...} ]` becomes two `<activities>` children of
    `<properties>`, NOT a wrapper element containing two items. XML expresses
    repetition as repeated siblings, so this needs no invented tag name -- and
    `./properties/activities` then selects the activities exactly as
    `./DSJOB/DSRECORD` selects records.

    An EMPTY array projects to nothing, which makes `"dependsOn": []` (stated and
    empty) indistinguishable from an absent `dependsOn`. Both occur in the two
    fixtures -- myPipeline.json activity 0 states the empty array,
    adf_First_Pipeline.json activity 0 omits the key -- so the difference is real
    and the projection cannot carry it. Empty arrays are recorded and reported
    rather than silently equated with absence.

PROJECTION RULE 3 -- AN ARRAY OF SCALARS IS INDEXED PARTS.
    `"dependencyConditions": ["Succeeded"]` cannot be repeated child elements,
    because its members are not objects. It becomes `@dependencyConditions$1`,
    reusing the K$1..K$n convention the DataStage pass introduced for delimited
    compound values (ARCHITECTURAL CHANGE A4a). Same shape of fact -- one key,
    several ordered values -- reached from a different format.

PROJECTION RULE 4 -- JSON null IS A VALUELESS KEY; TYPES KEEP THEIR LEXEME.
    XML attribute values are strings; JSON scalars are typed. `"retry": 0` and
    `"secureOutput": false` must not become the strings "0" and "False", so a
    non-string scalar is stored as its JSON LEXEME (`0`, `false`, `1.5`) and the
    JSON type is recorded beside it.

    `null` is not a value. It is the key stated with no value -- the same fact as
    a bare .dsx key (FRAMEWORK CHANGE 36) and a Kettle <tag/>, now for the third
    time in a third format. It is recorded and NEVER set as an attribute, so
    nothing unsourceable can be read back out.
    UNVERIFIED: neither fixture contains a null (0 measured), so rule 4's null
    path is implemented and unexercised. The bool and int paths ARE exercised --
    myPipeline.json has 7 booleans and 4 integers.

ARCHITECTURAL CHANGE A3 (location oracle).
    A JSON Pointer (RFC 6901) is this front-end's citable position. It is NOT a
    byte offset: it is an address that resolves against the parsed document, which
    is what makes a SOURCE claim falsifiable. Every pointer emitted by this
    front-end is checkable by evaluating it against the file.

ARCHITECTURAL CHANGE A6 (attribute-reference citation).
    `attr_ref` returns "/name", so a full citation is a real pointer
    `/properties/activities/1/name`. It also expands the rule-3 parts back to
    their true addresses: `dependencyConditions$1` cites
    `/dependencyConditions/0`, which is where the value actually is.
"""

import json
import xml.etree.ElementTree as ET

_XML_NAME_START = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
_XML_NAME_BODY = _XML_NAME_START | set("0123456789.-")


def _esc(token: str) -> str:
    """RFC 6901 escaping: ~ -> ~0 and / -> ~1, in that order."""
    return token.replace("~", "~0").replace("/", "~1")


def _lexeme(v) -> str:
    """The JSON text of a non-string scalar. json.dumps gives the source lexeme:
    True -> 'true', 0 -> '0'. Never Python's repr."""
    return json.dumps(v)


class JsonDocument:
    """Front-end satisfying the contract in docmodel.py."""

    kind = "JSON"

    def __init__(self, path: str, cfg: dict):
        self.path = path
        self.cfg = cfg
        self._ptr: dict[int, str] = {}                  # id(node) -> JSON Pointer
        self._attr_kind: dict[tuple[int, str], str] = {}  # (id(node), attr) -> json type
        self.valueless_keys: list[tuple[str, str]] = []  # (pointer, key) stated null
        self.empty_arrays: list[str] = []
        self.scalar_array_parts = 0
        self.unsafe_tags: list[tuple[str, str]] = []     # key not an XML name
        self.objects = 0
        self.arrays = 0
        self.scalars = 0

        with open(path, "rb") as fh:
            self.data = json.loads(fh.read().decode(cfg.get("encoding", "utf-8")))
        if not isinstance(self.data, dict):
            raise ValueError(f"{path}: top level is {type(self.data).__name__}, "
                             "not a JSON object")
        self.root = ET.Element(cfg.get("root_tag", "pipeline"))
        self._ptr[id(self.root)] = ""
        self._build(self.root, self.data, "")

    # -- tree construction -------------------------------------------------

    def _safe_tag(self, key: str, ptr: str) -> bool:
        ok = bool(key) and key[0] in _XML_NAME_START and all(
            c in _XML_NAME_BODY for c in key[1:])
        if not ok:
            # A key that is not an XML name cannot be reached by the framework's
            # query language. Reported rather than mangled into one that can.
            self.unsafe_tags.append((ptr, key))
        return ok

    def _build(self, node, obj: dict, ptr: str) -> None:
        """PROJECTION RULES 1-4, applied to one object."""
        self.objects += 1
        for key, val in obj.items():
            kptr = f"{ptr}/{_esc(key)}"
            if isinstance(val, dict):                       # RULE 1
                if not self._safe_tag(key, kptr):
                    continue
                child = ET.SubElement(node, key)
                self._ptr[id(child)] = kptr
                self._build(child, val, kptr)
            elif isinstance(val, list):
                self.arrays += 1
                if not val:                                 # RULE 2, empty
                    self.empty_arrays.append(kptr)
                    continue
                if all(isinstance(x, dict) for x in val):   # RULE 2
                    if not self._safe_tag(key, kptr):
                        continue
                    for i, x in enumerate(val):
                        child = ET.SubElement(node, key)
                        self._ptr[id(child)] = f"{kptr}/{i}"
                        self._build(child, x, f"{kptr}/{i}")
                elif any(isinstance(x, (dict, list)) for x in val):
                    # Heterogeneous or nested arrays have no single projection.
                    # Reported rather than flattened. UNVERIFIED: 0 in either
                    # fixture, so this path is implemented and unexercised.
                    self.unsafe_tags.append((kptr, f"{key} (mixed/nested array)"))
                else:                                       # RULE 3
                    for i, x in enumerate(val):
                        self.scalars += 1
                        if x is None:
                            self.valueless_keys.append((f"{kptr}/{i}", key))
                            continue
                        a = f"{key}${i + 1}"
                        node.set(a, x if isinstance(x, str) else _lexeme(x))
                        self._attr_kind[(id(node), a)] = type(x).__name__
                        self.scalar_array_parts += 1
            else:                                           # RULE 1 / RULE 4
                self.scalars += 1
                if val is None:
                    self.valueless_keys.append((kptr, key))
                    continue
                node.set(key, val if isinstance(val, str) else _lexeme(val))
                self._attr_kind[(id(node), key)] = type(val).__name__

    # -- location oracle ---------------------------------------------------

    def loc_prefix(self, node) -> str:
        p = self._ptr.get(id(node))
        return f"json:{p or '/'} " if p is not None else ""

    def attr_ref(self, node, attr: str) -> str:
        """ARCHITECTURAL CHANGE A6. A rule-3 part cites the array member it came
        from, so `dependencyConditions$1` -> `/dependencyConditions/0`."""
        base, sep, idx = attr.rpartition("$")
        if sep and idx.isdigit() and (id(node), attr) in self._attr_kind:
            return f"/{_esc(base)}/{int(idx) - 1}"
        return "/" + _esc(attr)

    def attr_json_type(self, node, attr: str) -> str | None:
        return self._attr_kind.get((id(node), attr))

    def source_text(self, node) -> str:
        """ARCHITECTURAL CHANGE A9. RE-SERIALISED from the parsed member the node's
        JSON Pointer addresses, because json.loads keeps no offsets. Indentation is
        this function's, not the file's -- so, as with the XML front-end, this is a
        reconstruction of the fragment and not a quotation of it. Returns "" when
        the pointer does not resolve, which cannot happen for a node the projection
        built and is therefore reported as nothing rather than raising."""
        ptr = self._ptr.get(id(node))
        if ptr is None:
            return ""
        cur = self.data
        for tok in ptr.lstrip("/").split("/") if ptr else []:
            tok = tok.replace("~1", "/").replace("~0", "~")
            try:
                cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
            except (KeyError, IndexError, ValueError, TypeError):
                return ""
        return json.dumps(cur, indent=2, ensure_ascii=False)

    def report(self) -> list[str]:
        typed = {}
        for (_n, a), t in self._attr_kind.items():
            typed[t] = typed.get(t, 0) + 1
        out = [
            f"front-end      : {self.kind}  (RFC 6901 JSON Pointer locations)",
            f"projection     : {self.objects} objects -> nodes, {self.arrays} arrays, "
            f"{self.scalars} scalars -> attributes by JSON type {typed}",
            f"                 {self.scalar_array_parts} scalar-array parts as K$n",
            f"unaccounted    : {len(self.empty_arrays)} arrays stated and EMPTY "
            f"(indistinguishable from an absent key after projection), "
            f"{len(self.valueless_keys)} keys stated null, "
            f"{len(self.unsafe_tags)} keys unreachable by the query language",
        ]
        for p in self.empty_arrays[:6]:
            out.append(f"                 empty array at {p}")
        for p, k in self.valueless_keys[:5]:
            out.append(f"                 null at {p}")
        for p, k in self.unsafe_tags[:5]:
            out.append(f"                 unreachable key {k!r} at {p}")
        return out
