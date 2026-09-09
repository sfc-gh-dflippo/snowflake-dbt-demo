"""Pluggable document front-end.

ARCHITECTURAL CHANGE A1 (introduced by the DataStage pass)
----------------------------------------------------------
Before this module, `Identification.__init__` called `ET.parse(path)` directly.
That hardcoded ONE document model -- an XML tree -- into the framework, and it was
invisible because both prior platforms happened to be XML.

The seam is deliberately NOT "a pluggable query language". Making `find` /
`findall` polymorphic would mean reimplementing an XPath subset per platform and
would push a query dialect into every platform table. Instead the seam is a
pluggable TREE PROJECTION: each front-end is responsible for presenting its
source as a tree of nodes carrying named attributes, and the framework keeps ONE
query language (ElementTree's XPath subset) for every platform.

What the framework actually requires of a document is small: findall, find, get,
text, iter, and child iteration. A projection that satisfies those needs no
further framework support.

ARCHITECTURAL CHANGE A3 (see dsxdoc.py)
---------------------------------------
A projected tree has no line numbers, so an XPath into it is NOT a location in
the source document. Every front-end therefore also acts as a LOCATION ORACLE:
`loc_prefix(node)` returns a citable position in the byte stream, or "" when the
front-end cannot supply one. This is the only part of the abstraction the
framework could not have done without -- provenance integrity depends on it.

ARCHITECTURAL CHANGE A6 (introduced by the Pentaho and ADF pass)
----------------------------------------------------------------
A1 said a front-end presents "a tree of nodes carrying named attributes" and
silently assumed the attributes were REAL -- that `@name` named something the
source document actually contains. Both platforms in this pass break that.

  * A Kettle `.ktr` contains ZERO XML attributes. MEASURED: 0 attributes across
    both fixtures. Every value is the text of a child element,
    `<name>Delay row</name>`, because every Kettle serializer goes through
    XMLHandler.addTagValue and none of the 2336 call sites passes the optional
    attribute varargs.
  * An ADF pipeline is JSON. `"name": "mycopy"` is an object member, not an
    attribute.

Both front-ends therefore LIFT a value into an attribute so that one query
language keeps working. That is the projection doing its job -- but it means
`.../step[2]/@name` is an address that does not exist in the source, which is
exactly the unfalsifiable-SOURCE failure A3 was created to prevent. A3 fixed the
location of the NODE and left the last step of every citation, the attribute
reference itself, hardcoded as the string "/@" + attr in seven places.

So the contract gains one method: `attr_ref(node, attr)` returns the citation for
reading `attr` from `node`, in the SOURCE's own addressing syntax. XML and
record-block front-ends return "/@" + attr, which is what the framework used to
build inline -- so Informatica, SSIS and DataStage output is byte-identical.

ARCHITECTURAL CHANGE A7
-----------------------
`report()` moved the front-end banner out of main.py. FRAMEWORK CHANGE 39 put a
projection report in the driver, but wrote it in DataStage's vocabulary --
sections, reparented records, compound value parts, unsectioned subrecords. None
of those nouns exists in a Kettle or JSON projection, and a JSON projection has
facts of its own to report that a .dsx does not (empty arrays, non-XML-safe
keys). A front-end now reports itself and the driver prints whatever it says.

ARCHITECTURAL CHANGE A9 (introduced by the placeholder-body pass)
----------------------------------------------------------------
The contract gains `source_text(node)`: the SOURCE FRAGMENT that declares this
node, in the source's own syntax, or "" when the front-end cannot supply one.

WHY A FRONT-END METHOD AND NOT A FRAMEWORK ONE. This is the only place the
framework wants BYTES rather than structure, and every previous attempt to get
them generically is wrong in a way that matters:

  * `ET.tostring(node)` on a LIFTED projection serialises attributes the source
    file does not contain. A Kettle .ktr has zero XML attributes, so the
    "original source" would be a fabrication in the shape of the original.
  * A raw line slice of the node alone is INCOMPLETE where the projection
    reparents. MEASURED on DataStage: a Transformer stage's record block is 14
    lines and holds no derivation at all -- every derivation is in the OUTPUT PIN
    record the projection moved under it. Slicing only the stage loses exactly
    the thing a reviewer needs.

So each front-end answers in whatever way is faithful for its own format: the two
line-numbered front-ends return the RAW BYTES of every source block the node's
subtree covers, in file order; the XML front-end re-serialises (which is what
SnowConvert's own not-supported path does, and ElementTree preserves attribute
order); the JSON front-end re-serialises the pointed-to member.

Returning "" is a legitimate answer and must stay distinguishable from returning
a fragment -- the caller falls back to naming the kind, exactly as it did before
this method existed.
"""

import xml.etree.ElementTree as ET


def raw_block_text(lines: list[str], ranges: list[tuple[int, int]]) -> str:
    """ARCHITECTURAL CHANGE A9, shared by the two line-numbered front-ends.

    `ranges` are 1-based inclusive (start, end) line pairs for every block a
    node's subtree covers. They are MERGED and emitted in FILE order, and a gap
    between two non-adjacent blocks is marked rather than closed silently -- a
    fragment that reads as contiguous source when it is not would be a
    fabrication, and the projection reparents records across the file (see
    dsxdoc._reparent), so gaps are the normal case rather than the exception.
    """
    if not lines or not ranges:
        return ""
    merged: list[list[int]] = []
    for start, end in sorted(r for r in ranges if r[0] and r[1] and r[1] >= r[0]):
        if merged and start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    out: list[str] = []
    for i, (start, end) in enumerate(merged):
        if i:
            out.append(f"... [source lines {merged[i - 1][1] + 1}-{start - 1} omitted: "
                       f"not part of this element] ...")
        out.extend(lines[start - 1:end])
    return "\n".join(out)


class XmlDocument:
    """Front-end for XML sources (Informatica .XML, SSIS .dtsx).

    `loc_prefix` returns "" because ElementTree discards line numbers. That is a
    real limitation of the XML front-end, not of the framework: an Informatica or
    SSIS `where` string cites an XPath and nothing else, exactly as it did before
    this seam existed. Keeping it "" is also what makes the DataStage pass a
    no-op for the two prior platforms.
    """

    kind = "XML"

    def __init__(self, path: str, cfg: dict):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()

    def loc_prefix(self, node) -> str:
        return ""

    def attr_ref(self, node, attr: str) -> str:
        """ARCHITECTURAL CHANGE A6: an XML attribute reference IS "/@name". This
        is the string the framework used to concatenate inline."""
        return "/@" + attr

    def source_text(self, node) -> str:
        """ARCHITECTURAL CHANGE A9. RE-SERIALISED, not sliced: ElementTree has no
        byte offsets. Faithful in content and in attribute order (ET preserves
        parse order), and it is the same mechanism SnowConvert's own
        UnsupportedTransformationConfigurator uses -- `instance.WriteTo(xwriter)`.
        What it does NOT preserve is the file's own whitespace, entity spelling and
        comments, so this is a reconstruction of the fragment and not a quotation
        of it."""
        return ET.tostring(node, encoding="unicode")

    def report(self) -> list[str]:
        return []


def misplaced_lift_rule_paths(table: dict) -> list[str]:
    """Return lift-rule declarations the active front-end will not apply.

    The only list ``LiftXmlDocument`` reads is ``structure.document_model.lift_rules``, and
    only when ``structure.document_model.kind`` is ``LIFT_XML``. Missing ``document_model``
    remains the backward-compatible spelling of ordinary XML when no lift rules are declared
    anywhere. Unrelated keys, including comments, are ignored.
    """
    structure = table.get("structure") or {}
    cfg = structure.get("document_model") if isinstance(structure.get("document_model"), dict) else {}
    kind = cfg.get("kind") or "XML"

    paths: list[str] = []
    if "lift_rules" in table:
        paths.append("lift_rules")
    if "lift_rules" in structure:
        paths.append("structure.lift_rules")
    for block in ("levels", "edge_levels"):
        for index, level in enumerate(structure.get(block) or []):
            if isinstance(level, dict) and "lift_rules" in level:
                paths.append(f"structure.{block}[{index}].lift_rules")
    # Correct location, inactive front-end: XML default, missing kind, or a non-LIFT kind.
    if "lift_rules" in cfg and kind != "LIFT_XML":
        paths.append("structure.document_model.lift_rules")
    return paths


def parse(table: dict, path: str):
    """Dispatch on the platform table's declared document model."""
    misplaced = misplaced_lift_rule_paths(table)
    if misplaced:
        found = ", ".join(misplaced)
        raise ValueError(
            f"ignored lift_rules at {found}; the LIFT_XML front-end reads only "
            "structure.document_model.lift_rules and only when "
            "structure.document_model.kind='LIFT_XML'"
        )
    cfg = table["structure"].get("document_model") or {"kind": "XML"}
    kind = cfg["kind"]
    if kind == "XML":
        return XmlDocument(path, cfg)
    if kind == "RECORD_BLOCK":
        import dsxdoc
        return dsxdoc.RecordBlockDocument(path, cfg)
    # FRAMEWORK CHANGE 45: two more front-end kinds. CHILD_TEXT_XML is still XML
    # and still parsed by an XML parser -- what differs is WHERE the values are,
    # which is why it is a separate front-end rather than a flag on XmlDocument.
    if kind == "CHILD_TEXT_XML":
        import ktrdoc
        return ktrdoc.ChildTextXmlDocument(path, cfg)
    if kind == "JSON":
        import jsondoc
        return jsondoc.JsonDocument(path, cfg)
    if kind == "LIFT_XML":
        import alteryxdoc
        return alteryxdoc.LiftXmlDocument(path, cfg)
    raise ValueError(f"no front-end for document_model.kind={kind!r}")
