"""Record-block front-end: projects an IBM DataStage .dsx export into a tree.

A .dsx is not XML. It is a line-oriented nest of named blocks:

    BEGIN DSJOB
       Identifier "DictRand"
       BEGIN DSRECORD
          Identifier "V0S0"
          OLEType "CCustomStage"
          Properties "CCustomProperty"
          BEGIN DSSUBRECORD
             Name "Context"
             Value "source"
          END DSSUBRECORD
       END DSRECORD
    END DSJOB

Format facts honoured here, each read from the engine's own DataStage scanner
rather than guessed:
  * block keywords and the double-quoted STRINGCON with a \\" escape
    -- Parsers/Assemblies/DataStage/DsxParser/Coco/Dsx.atg:29-53
  * IGNORECASE lexing -- Dsx.atg:6
  * the =+=+=+= multi-line literal, whose closing marker may be preceded by
    spaces or tabs -- Parsers/Assemblies/DataStage/DsxParser/Coco/Scanner.cs:44-75

Three projection rules do the real work. Each exists because the record-block
model states something that XML states by nesting, and none of the three has an
XML analogue.

ARCHITECTURAL CHANGE A2 -- POSITIONAL SECTIONS.
    Subrecord grouping in a .dsx is POSITIONAL. A scalar line whose value names a
    subrecord class (Properties "CCustomProperty", Columns "COutputColumn",
    MetaBag "CMetaProperty") opens a section, and every DSSUBRECORD until the next
    such line belongs to it. Flatten that and a stage's connection properties, its
    column metadata and its APT runtime bag become one undifferentiated list --
    which is exactly what the engine's own AST does: DsxRecord.Properties and
    DsxRecord.SubRecords are filters over one flat Sequence
    (Parsers/Assemblies/DataStage/DsxAST/AST/Elements/DsxRecord.Properties.cs:24-50).
    The projection turns each section into a real container node, after which
    ordinary containment queries work.

ARCHITECTURAL CHANGE A3 -- LOCATION ORACLE.
    An XPath into a projected tree is not a location in the source file, so
    "SOURCE" would become unfalsifiable. Every attribute records the 1-based line
    it was read from, and loc_prefix() puts a citable "dsx:LINE " in front of
    every `where` string.

ARCHITECTURAL CHANGE A4 -- DECLARED-OWNERSHIP REPARENTING and COMPOUND VALUES.
    Link records (OLEType CCustomOutput / CCustomInput) are SIBLINGS of the stage
    records they belong to; ownership is stated on the stage as
    OutputPins "V0S0P1" / InputPins "V0S1P1". A single value also carries a
    delimited tuple: Partner "V0S1|V0S1P1" names a partner stage AND a partner
    pin. XML attribute values are opaque and XML containment is nesting, so the
    framework had no concept for either. The projection splits declared compound
    values into K$1..K$n parts and reparents each link record under the stage that
    names it, after which the DataStage tree has the same shape as an SSIS
    component tree and the existing ancestry machinery works untouched.
"""

import re
import xml.etree.ElementTree as ET

import docmodel

_BEGIN = re.compile(r"^(BEGIN)\s+([A-Za-z][A-Za-z0-9_]*)\s*$", re.I)
_END = re.compile(r"^(END)\s+([A-Za-z][A-Za-z0-9_]*)\s*$", re.I)
_MULTI = re.compile(r"^([A-Za-z][A-Za-z0-9_$]*)\s*=\+=\+=\+=\s*$")
_BARE = re.compile(r"^([A-Za-z][A-Za-z0-9_$]*)\s*$")
_MULTI_CLOSE = re.compile(r"^[ \t]*=\+=\+=\+=[ \t]*$")

_ENC = {"CP1251": "cp1251", "UTF-8": "utf-8", "UTF8": "utf-8", "CP1252": "cp1252"}


def _unquote(raw: str) -> str | None:
    """A STRINGCON per Dsx.atg:29-36: double-quoted, \\" for an embedded quote.
    Returns None when the line is not a quoted value at all, so the caller can
    report it rather than coerce it."""
    if len(raw) < 2 or raw[0] != '"' or raw[-1] != '"':
        return None
    out, i, n = [], 1, len(raw) - 1
    while i < n:
        if raw[i] == "\\" and i + 1 <= n and raw[i + 1] == '"':
            out.append('"')
            i += 2
        else:
            out.append(raw[i])
            i += 1
    return "".join(out)


class RecordBlockDocument:
    """Front-end satisfying the contract in docmodel.py."""

    kind = "RECORD_BLOCK"

    def __init__(self, path: str, cfg: dict):
        self.path = path
        self.cfg = cfg
        self._line_of: dict[tuple[int, str], int] = {}   # (id(node), attr) -> line
        self._block_line: dict[int, int] = {}            # id(node) -> BEGIN line
        self._block_end: dict[int, int] = {}             # id(node) -> END line
        self.unparsed: list[tuple[int, str]] = []        # never silently dropped
        self.valueless_keys: list[tuple[int, str]] = []  # stated key, no value
        self.sections: set[str] = set()
        self.unsectioned = 0
        self.reparented = 0
        self.compound_expanded = 0

        text = self._decode()
        self.lines = text.split("\n")     # kept for source_text (A9)
        self.root = ET.Element(cfg.get("root_tag", "dsx"))
        self._block_line[id(self.root)] = 1
        self._build(self.lines)
        self._expand_compound()
        self._reparent()

    # -- decoding ----------------------------------------------------------

    def _decode(self) -> str:
        """The character set is declared IN BAND, inside the HEADER block, so it
        cannot be known before reading. Sniff the declaration from the ASCII-safe
        prefix, then decode. UNVERIFIED: the only fixture available is pure ASCII
        (0 bytes >= 0x80), so the cp1251 path is exercised but not proven."""
        raw = open(self.path, "rb").read()
        enc = self.cfg.get("default_encoding", "utf-8")
        head = raw[:512].decode("ascii", errors="replace")
        m = re.search(r'CharacterSet\s+"([^"]*)"', head)
        if m:
            self.declared_charset = m.group(1)
            enc = _ENC.get(m.group(1).upper(), enc)
        else:
            self.declared_charset = None
        self.encoding = enc
        return raw.decode(enc)

    # -- tree construction -------------------------------------------------

    def _build(self, lines: list[str]) -> None:
        section_blocks = set(self.cfg.get("section_blocks", []))
        stack = [self.root]
        last_key: dict[int, str] = {}      # id(parent) -> most recent scalar key
        sect_of: dict[int, dict] = {}      # id(parent) -> {key: section node}
        i, n = 0, len(lines)
        while i < n:
            raw = lines[i]
            line_no = i + 1
            s = raw.strip()
            i += 1
            if not s:
                continue

            m = _BEGIN.match(s)
            if m:
                tag = m.group(2).upper()
                parent = stack[-1]
                if tag in section_blocks:
                    key = last_key.get(id(parent))
                    if key is None:
                        key = self.cfg.get("unsectioned_tag", "_unsectioned")
                        self.unsectioned += 1
                    else:
                        self.sections.add(key)
                    holder = sect_of.setdefault(id(parent), {}).get(key)
                    if holder is None:
                        holder = ET.SubElement(parent, key)
                        self._block_line[id(holder)] = line_no
                        sect_of[id(parent)][key] = holder
                    parent = holder
                node = ET.SubElement(parent, tag)
                self._block_line[id(node)] = line_no
                stack.append(node)
                continue

            m = _END.match(s)
            if m:
                if len(stack) > 1:
                    # ARCHITECTURAL CHANGE A9: the END line closes the block, so
                    # this is the last line the record occupies. Recorded here
                    # rather than derived from the next BEGIN, because sibling
                    # blocks are not contiguous in a .dsx.
                    self._block_end[id(stack[-1])] = line_no
                    stack.pop()
                else:
                    self.unparsed.append((line_no, s))
                continue

            node = stack[-1]

            m = _MULTI.match(s)
            if m:
                key, body = m.group(1), []
                while i < n and not _MULTI_CLOSE.match(lines[i]):
                    body.append(lines[i])
                    i += 1
                i += 1                                  # consume closing marker
                self._set(node, key, "\n".join(body), line_no)
                last_key[id(node)] = key
                continue

            if " " in s:
                key, rest = s.split(" ", 1)
                val = _unquote(rest.strip())
                if val is None:
                    self.unparsed.append((line_no, s))
                    continue
                self._set(node, key, val, line_no)
                last_key[id(node)] = key
                continue

            if _BARE.match(s):
                # A key stated with no value. NOT the same fact as an empty
                # string, and NOT the same fact as an absent key. Recorded so it
                # can be reported instead of being coerced into "".
                self.valueless_keys.append((line_no, s))
                last_key[id(node)] = s
                continue

            self.unparsed.append((line_no, s))

    def _set(self, node, key: str, val: str, line_no: int) -> None:
        node.set(key, val)
        self._line_of[(id(node), key)] = line_no

    # -- projection rules --------------------------------------------------

    def _expand_compound(self) -> None:
        """ARCHITECTURAL CHANGE A4a: a declared compound value becomes K$1..K$n.
        The part names keep the real key visible, so `where` cites @Partner$1 --
        readable as "part 1 of the @Partner value at this line" -- rather than
        inventing an attribute the file does not contain."""
        for key, spec in (self.cfg.get("compound_attrs") or {}).items():
            sep = spec["separator"]
            for node in self.root.iter():
                v = node.get(key)
                if v is None:
                    continue
                for j, part in enumerate(v.split(sep), start=1):
                    part = part.strip()
                    if part:
                        self._set(node, f"{key}${j}", part,
                                  self._line_of.get((id(node), key), 0))
                        self.compound_expanded += 1

    def _reparent(self) -> None:
        """ARCHITECTURAL CHANGE A4b: move each child named by an owner's declared
        ownership list under that owner. Driven entirely by a value stated in the
        document; nothing is inferred from the shape of an identifier."""
        for rule in self.cfg.get("reparent", []):
            sep = rule["separator"]
            ckey = rule["child_key_attr"]
            for scope in self.root.iter(rule["scope_tag"]):
                by_key = {c.get(ckey): c for c in scope
                          if c.tag == rule["child_tag"] and c.get(ckey)}
                moves, claimed = [], set()
                for owner in scope:
                    if owner.tag != rule["owner_tag"]:
                        continue
                    for attr in rule["owner_list_attrs"]:
                        v = owner.get(attr)
                        if not v:
                            continue
                        for part in v.split(sep):
                            part = part.strip()
                            child = by_key.get(part)
                            if (child is not None and child is not owner
                                    and id(child) not in claimed):
                                claimed.add(id(child))
                                moves.append((owner, child))
                for owner, child in moves:
                    scope.remove(child)
                    owner.append(child)
                    self.reparented += 1

    # -- location oracle ---------------------------------------------------

    def loc_prefix(self, node) -> str:
        ln = self._block_line.get(id(node))
        return f"dsx:{ln} " if ln else ""

    def attr_line(self, node, attr: str) -> int | None:
        return self._line_of.get((id(node), attr))

    def attr_ref(self, node, attr: str) -> str:
        """ARCHITECTURAL CHANGE A6 (see docmodel.py). A .dsx key really is read as
        an attribute of the projected record, so this returns what the framework
        used to concatenate inline and DataStage output is unchanged."""
        return "/@" + attr

    def source_text(self, node) -> str:
        """ARCHITECTURAL CHANGE A9. RAW BYTES of the record blocks this node's
        subtree covers, in file order -- not a re-serialisation. A .dsx is not XML
        and the projected tree is not the file, so anything reconstructed here
        would be in a syntax the source does not use.

        THE SUBTREE AND NOT THE NODE. MEASURED on CustomerSummaryDerive.dsx: the
        `Xfm_DeriveNameYear` CTransformerStage block is lines 124-137 and states
        no derivation whatsoever -- both derivations live in the CTrxOutput pin
        record at 187-218, which `_reparent` moved under the stage on the strength
        of the stage's own OutputPins value. Slicing the stage alone would have
        produced a 14-line fragment missing the only thing worth reading."""
        ranges = [(self._block_line.get(id(n), 0), self._block_end.get(id(n), 0))
                  for n in node.iter()]
        return docmodel.raw_block_text(self.lines, ranges)

    def report(self) -> list[str]:
        """ARCHITECTURAL CHANGE A7: these lines were printed by main.py in
        DataStage's own vocabulary. A front-end now reports itself."""
        out = [
            f"front-end      : {self.kind}  encoding={self.encoding} "
            f"(declared CharacterSet {self.declared_charset!r})",
            f"projection     : {len(self.sections)} distinct section names "
            f"{sorted(self.sections)}",
            f"                 {self.reparented} records reparented by declared "
            f"ownership, {self.compound_expanded} compound value parts",
            f"unaccounted    : {len(self.unparsed)} unparsed lines, "
            f"{len(self.valueless_keys)} keys stated with no value, "
            f"{self.unsectioned} subrecords with no enclosing section",
        ]
        for ln, s in self.unparsed[:5]:
            out.append(f"                 line {ln}: {s[:90]}")
        return out
