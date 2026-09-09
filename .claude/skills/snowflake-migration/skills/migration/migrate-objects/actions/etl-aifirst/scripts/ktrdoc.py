"""Child-text XML front-end: projects a Pentaho Kettle .ktr into a queryable tree.

A .ktr IS XML, and the existing XmlDocument parses it without complaint. It also
identifies absolutely nothing, because the framework reads every value with
`node.get(attr)` and a .ktr contains no attributes at all:

    <step>
      <name>Delay row</name>
      <type>Delay</type>
      <copies>1</copies>
      <partitioning>
        <method>none</method>
      </partitioning>
    </step>

MEASURED, both fixtures: 0 XML attributes in the whole document
(sample_trans.ktr 319 leaf child elements, safe-stop-gen-rows.ktr 341).

Format facts, each read from Kettle's own serialiser rather than guessed:
  * every value is written by XMLHandler.addTagValue, which emits
    <tag>value</tag>. The method accepts optional attributes but of the 2336
    addTagValue call sites in engine/ + core/ the only one passing them is the
    declaration itself, so no transformation, step or hop serializer writes an
    attribute -- core/src/main/java/org/pentaho/di/core/xml/XMLHandler.java
  * <transformation> / <info> / <order> / <hop>(<from>,<to>,<enabled>) / <step>
    (<name>,<type>,...) -- engine/src/main/java/org/pentaho/di/trans/TransMeta.java,
    TransHopMeta.java, trans/step/StepMeta.java
  * addTagValue emits a SELF-CLOSING <tag/> when the value is null OR empty. The
    format therefore CANNOT distinguish the two, which is why an empty element is
    reported here rather than resolved.

TWO projection rules.

PROJECTION RULE 1 -- SCALAR LIFT.
    Every child element that has no element children of its own is a scalar. Its
    text is lifted to an attribute of the same name on its PARENT, after which the
    framework's ordinary attribute reads work untouched.

    The lift is ONE LEVEL ONLY, never recursive. <step> and <step>/<GUI> both
    have a <draw>-shaped leaf namespace, and flattening the tree would collide
    them and destroy the containment the queries rely on.

    Lifted children are NOT removed. Removing them would make the citation
    produced by attr_ref point at a node the projected tree no longer contains.

PROJECTION RULE 2 -- EMPTY LEAF IS A VALUELESS KEY, NOT AN EMPTY STRING.
    <description /> is a stated key with no value. Coercing it to "" is the exact
    bug the SSIS pass found in the precision reader and the DataStage pass found
    again in the attr-site reader (FRAMEWORK CHANGE 36) -- an absent value
    becoming a value that is present in the representation and absent from the
    source. Here the ambiguity is WORSE than on DataStage, because Kettle's own
    writer collapses null and "" into the same <tag/>, so it is not recoverable by
    any reader. Recorded and reported; never lifted.

ARCHITECTURAL CHANGE A3 (location oracle, as DataStage).
    ElementTree discards line numbers, so this front-end parses with expat and
    keeps the 1-based start line of every element. That gives BOTH a node
    location and -- because a lifted value has its own element -- an exact line
    for each individual value, which the XML front-end cannot supply.

ARCHITECTURAL CHANGE A6 (attribute-reference citation).
    `attr_ref(node, "name")` returns "/name/text()#ktr:451", not "/@name".
    `.../step[2]/@name` would be an address a reviewer cannot check against the
    file, because the file has no attributes.
"""

import re
import xml.etree.ElementTree as ET
import xml.parsers.expat

import docmodel


class ChildTextXmlDocument:
    """Front-end satisfying the contract in docmodel.py."""

    kind = "CHILD_TEXT_XML"

    def __init__(self, path: str, cfg: dict):
        self.path = path
        self.cfg = cfg
        self._block_line: dict[int, int] = {}            # id(node) -> start line
        self._block_end: dict[int, int] = {}             # id(node) -> end-tag line
        self._line_of: dict[tuple[int, str], int] = {}    # (id(node), attr) -> line
        self.valueless_keys: list[tuple[int, str]] = []   # stated key, no value
        self.collisions: list[tuple[int, str, str]] = []  # repeated leaf sibling
        self.lifted = 0
        self.leaves = 0
        self.source_attributes = 0

        self.root = self._parse()
        self._read_lines()
        self._lift()

    def _read_lines(self) -> None:
        """ARCHITECTURAL CHANGE A9: the raw text, for source_text to slice.

        The encoding is sniffed from the XML declaration rather than taken from
        expat, which exposes none after ParseFile. MEASURED on both fixtures:
        safe-stop-gen-rows.ktr declares UTF-8 and sample_trans.ktr declares
        nothing, and the XML spec's default for a declaration-less document is
        UTF-8 -- so both decode identically either way. A .ktr declaring a
        non-UTF-8 encoding is UNVERIFIED here.
        """
        raw = open(self.path, "rb").read()
        m = re.search(rb'encoding\s*=\s*["\']([^"\']+)["\']', raw[:256])
        enc = m.group(1).decode("ascii", "replace") if m else "utf-8"
        try:
            self.lines = raw.decode(enc).split("\n")
        except LookupError:
            self.lines = raw.decode("utf-8", errors="replace").split("\n")
        self.encoding = enc

    # -- parsing -----------------------------------------------------------

    def _parse(self):
        """expat rather than ET.parse, purely for CurrentLineNumber. The
        declaration is honoured by expat: safe-stop-gen-rows.ktr declares
        UTF-8 and sample_trans.ktr declares nothing."""
        p = xml.parsers.expat.ParserCreate()
        root = None
        stack: list = []
        text: dict[int, list[str]] = {}

        def start(tag, attrs):
            nonlocal root
            node = ET.Element(tag)
            # A .ktr states no attributes. If one ever appears it is carried
            # through and counted rather than dropped, so the claim "this format
            # has no attributes" stays measured instead of assumed.
            for k, v in attrs.items():
                node.set(k, v)
                self._line_of[(id(node), k)] = p.CurrentLineNumber
                self.source_attributes += 1
            self._block_line[id(node)] = p.CurrentLineNumber
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
            text[id(node)] = []

        def chars(data):
            if stack:
                text[id(stack[-1])].append(data)

        def end(tag):
            node = stack.pop()
            node.text = "".join(text.pop(id(node), []))
            # ARCHITECTURAL CHANGE A9: expat's line number at the end handler is
            # the line the closing tag sits on, which is the last line the element
            # occupies. Needed because source_text slices raw bytes rather than
            # re-serialising -- see ChildTextXmlDocument.source_text.
            self._block_end[id(node)] = p.CurrentLineNumber

        p.StartElementHandler = start
        p.EndElementHandler = end
        p.CharacterDataHandler = chars
        with open(self.path, "rb") as fh:
            p.ParseFile(fh)
        return root

    # -- projection --------------------------------------------------------

    def _lift(self) -> None:
        """PROJECTION RULE 1 and 2."""
        for parent in self.root.iter():
            seen: set[str] = set()
            for child in parent:
                if len(child):
                    continue                     # has element children: a node
                self.leaves += 1
                val = (child.text or "").strip()
                line = self._block_line[id(child)]
                if not val:
                    # PROJECTION RULE 2.
                    self.valueless_keys.append((line, child.tag))
                    continue
                if child.tag in seen:
                    # Repeated leaf siblings would overwrite one another. The
                    # first wins and the collision is reported, because silently
                    # keeping one of two stated values is a fabrication.
                    # UNVERIFIED: neither fixture contains one (0 collisions
                    # measured), so this path is implemented and unexercised.
                    self.collisions.append((line, parent.tag, child.tag))
                    continue
                seen.add(child.tag)
                parent.set(child.tag, val)
                self._line_of[(id(parent), child.tag)] = line
                self.lifted += 1

    # -- location oracle ---------------------------------------------------

    def loc_prefix(self, node) -> str:
        ln = self._block_line.get(id(node))
        return f"ktr:{ln} " if ln else ""

    def attr_ref(self, node, attr: str) -> str:
        """ARCHITECTURAL CHANGE A6. A lifted value's real address is a child
        element's text, and its exact line is known, so the citation carries it."""
        ln = self._line_of.get((id(node), attr))
        return f"/{attr}/text()" + (f"#ktr:{ln}" if ln else "")

    def source_text(self, node) -> str:
        """ARCHITECTURAL CHANGE A9. RAW BYTES of the element's own lines, not a
        re-serialisation.

        THE DISTINCTION IS NOT COSMETIC HERE. `_lift` sets attributes on this node
        for every scalar child, and a .ktr contains ZERO real XML attributes
        (measured: 0 across both fixtures). `ET.tostring` would therefore return a
        fragment whose every attribute is an artefact of the projection -- source
        text that is not in the source, which is the exact failure ARCHITECTURAL
        CHANGE A6 exists to prevent one step earlier in the same citation."""
        ranges = [(self._block_line.get(id(n), 0), self._block_end.get(id(n), 0))
                  for n in node.iter()]
        return docmodel.raw_block_text(self.lines, ranges)

    def report(self) -> list[str]:
        out = [
            f"front-end      : {self.kind}  (XML parsed by expat for line numbers)",
            f"projection     : {self.lifted} scalar child elements lifted to "
            f"attributes of {self.leaves} leaf children examined; "
            f"{self.source_attributes} real XML attributes in the source",
            f"unaccounted    : {len(self.valueless_keys)} elements stated with no "
            f"value (Kettle's writer emits <tag/> for null AND for \"\", so the "
            f"two are not distinguishable), "
            f"{len(self.collisions)} repeated-leaf-sibling collisions",
        ]
        for ln, tag in self.valueless_keys[:5]:
            out.append(f"                 line {ln}: <{tag}/>")
        for ln, parent, tag in self.collisions[:5]:
            out.append(f"                 line {ln}: second <{tag}> under <{parent}>")
        return out
