"""Independent provenance audit.

With no golden output for DataStage, provenance IS the quality signal -- so the
claim "this field was SOURCEd at dsx:307" has to be falsifiable. This script
re-reads the raw source file with NO help from the framework's reader, and for
every located slot checks that the cited location really does state the cited
attribute, and (where the slot maps to an emitted scalar) that the value at that
location really is the value that was emitted.

Usage: python3 provenance_audit.py <platform_table.json> <source_doc>

It is deliberately dumb and deliberately separate. If it agreed with the reader by
construction it would prove nothing.

WHAT THIS USED TO CHECK, AND WHY THAT WAS WORSE THAN NO AUDIT
-------------------------------------------------------------
One locator, `^dsx:(\\d+) `, and nothing else. Three of the four other front-ends
emit no `dsx:` prefix at all, so on Informatica this script reported

    satisfied slots with a claimed reading : 158
      no location available (XML front-end): 158
      emitted value matches the file       : 0
    InputColumns 44 emitted, 0 value-checked / OutputColumns 96 emitted, 0 value-checked
    VERDICT: PASS

PASS while comparing ZERO of 140 column scalars against the file. Same on Pentaho
(0 of 12) and ADF (0 of 0). The per-family coverage line made that visible, which
is honest, and left the audit reading nothing on four platforms out of five.

An audit that reads nothing and says PASS is worse than no audit: it occupies the
slot where a check is supposed to be.

WHAT IT CHECKS NOW: ONE LOCATOR PER FRONT-END, DISPATCHED ON THE PLATFORM TABLE'S
OWN `document_model.kind` -- never guessed from the shape of the `where` string,
because a `where` with no scheme prefix means "an XPath into an XML file" on one
platform and "no location available" on another, and confusing the two is how an
audit starts resolving addresses against the wrong document.

  XML            (Informatica .XML, SSIS .dtsx) the citation IS an ElementTree
                 XPath. Resolved against an INDEPENDENT `ET.parse` of the raw
                 file -- a second parse, in this process, using no framework
                 module -- then `@attr` is read off the node it finds. MEASURED
                 that ElementTree resolves every shape the framework emits,
                 including chained predicates (`TRANSFORMFIELD[1][@NAME='NAME']`)
                 and namespaced attribute predicates
                 (`[@{www.microsoft.com/SqlServer/Dts}refId='Package\\Data Flow Task']`).
  RECORD_BLOCK   (.dsx) unchanged: `dsx:<line>` plus a raw-text block scan for the
                 cited key. This is the path that already worked and its numbers
                 do not move.
  CHILD_TEXT_XML (.ktr) the citation's `#ktr:<line>` suffix addresses the child
                 element the value was lifted from. That RAW LINE is read and
                 `<tag>value</tag>` extracted from it -- no XML parser, so the
                 projection's lifted attributes cannot participate.
  JSON           (ADF) the citation's XPath tail is walked against `json.load` of
                 the raw file, step by step, mapping `name[i]` onto an array index
                 and `name` onto an object member. Where a step carries a
                 `[@k='v']` predicate the member is checked to hold `v`, so the
                 address and the value have to agree at once.

WHAT IT STILL DOES NOT CHECK, STATED RATHER THAN PAPERED OVER
------------------------------------------------------------
A `where` that names a TABLE RULE or an ALGORITHM instead of a position in the
document ("EXPLICIT_EDGE_ELEMENT", a rule id) is not a reading and cannot be
audited. Those are counted as `no locator in this citation` per front-end and are
NOT folded into the located total -- on DataStage that is 41 of 192 and the number
is unchanged by this pass.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET

from emit import Emitter
from identify import DERIVED, SOURCE, Identification, load_table

_LOC = re.compile(r"^dsx:(\d+) (.*)$")
# WIDENED for the XML front-ends: an SSIS attribute name is `{namespace-uri}local`,
# which the old `[A-Za-z][A-Za-z0-9_]*` could not start on, so every SSIS citation
# would have been dropped as "no attribute in the path" even once located.
_ATTR = re.compile(r"/@((?:\{[^}]*\})?[A-Za-z][A-Za-z0-9_.-]*)(\$\d+)?$")
_KEYLINE = re.compile(r'^(\s*)([A-Za-z][A-Za-z0-9_]*) (.*)$')
_KTR_TAIL = re.compile(r"/([A-Za-z_][A-Za-z0-9_.-]*)/text\(\)#ktr:(\d+)$")
_JSON_LOC = re.compile(r"^json:(\S+) (.*)$")
_STEP = re.compile(r"^([^\[]+)((?:\[[^\]]*\])*)$")
# emit.py appends `  [transform <RULE> from '<raw>']` to a citation whose emitted value
# is a TRANSFORM of what the document states (SSIS `[dbo].[DimCustomer]` ->
# `DimCustomer` under UNQUALIFIED_TAIL). The annotation is not part of the address, and
# passing it to ElementTree raised `KeyError: '()'` -- the audit CRASHED on SSIS the
# moment it gained an XML locator, which is how this was found.
#
# It also changes WHAT IS CHECKABLE, and in the stronger direction: the emitted value is
# not expected to equal the file's, so the check becomes "the raw value this annotation
# claims to have transformed is the value the document states at that location". A
# transform annotation that misquotes its own input now fails.
_TRANSFORM = re.compile(r"\s{2,}\[transform [A-Z_]+ from (.*)\]$")


def split_transform(where: str) -> tuple[str, str | None]:
    m = _TRANSFORM.search(where)
    if not m:
        return where, None
    raw = m.group(1).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        raw = raw[1:-1]
    return where[:m.start()], raw


def block_lines(lines: list[str], start: int) -> list[str]:
    """The raw lines of the block whose BEGIN is at 1-based `start`, to its END.
    Sections projected by the reader are not blocks in the file, so a section's
    start line is a BEGIN DSSUBRECORD and this still terminates correctly."""
    i = start - 1
    indent = len(lines[i]) - len(lines[i].lstrip())
    out = [lines[i]]
    depth = 0
    for ln in lines[i + 1:]:
        s = ln.strip()
        if s.startswith("BEGIN "):
            depth += 1
        elif s.startswith("END "):
            if depth == 0:
                break
            depth -= 1
        elif depth == 0 and s and (len(ln) - len(ln.lstrip())) <= indent:
            break
        out.append(ln)
    return out


class Unlocated(Exception):
    """The citation carries no address at all. NOT a failure -- a rule id or an
    algorithm name is a legitimate `where` and is counted, never reported as a bad
    address."""


class NodeOnly(Exception):
    """The citation addresses a NODE and claims no attribute reading, so there is no
    value to compare -- but the node itself must exist. Kept distinct from Unlocated
    because "no address" and "an address that resolves to a node" are different
    facts, and the node's existence IS checkable."""


class NotThere(Exception):
    """The citation carries an address and the address does not state what was cited.
    This IS a failure: the framework claimed a reading at a place that has none."""


def locate_dsx(where, lines, _doc_path):
    """RECORD_BLOCK. Unchanged behaviour for attribute citations, plus a node check."""
    m = _LOC.match(where)
    if not m:
        raise Unlocated()
    line_no, path = int(m.group(1)), m.group(2)
    if line_no < 1 or line_no > len(lines):
        raise NotThere(f"cited dsx:{line_no} is outside the file ({len(lines)} lines)")
    am = _ATTR.search(path)
    if not am:
        # A block citation with no attribute. The BEGIN line has to be there.
        if not lines[line_no - 1].strip().startswith("BEGIN "):
            raise NotThere(f"cited dsx:{line_no} is not a record BEGIN: "
                           f"{lines[line_no - 1].strip()!r}")
        raise NodeOnly(f"dsx:{line_no}")
    attr = am.group(1)
    body = block_lines(lines, line_no)
    for ln in body:
        km = _KEYLINE.match(ln)
        if km and km.group(2) == attr:
            return _unquote(km.group(3).strip()), am.group(2), f"dsx:{line_no} /@{attr}"
    raise NotThere(f"cited dsx:{line_no} /@{attr}; block at that line: "
                   f"{body[0].strip()!r}")


def locate_xml(where, _lines, doc_path):
    """XML. The citation is an XPath; resolve it against a SECOND, INDEPENDENT parse.

    `ET.parse` here is stdlib called directly on the raw path -- the framework's
    XmlDocument is never constructed, so nothing about this resolution can be
    inherited from the reader whose claim is under test.
    """
    am = _ATTR.search(where)
    text_cite = am is None and where.endswith("/text()")
    xpath = where[:am.start()] if am else (where[:-len("/text()")] if text_cite else where)
    if not xpath.startswith("."):
        raise Unlocated()
    root = _xml_root(doc_path)
    try:
        node = root.find(xpath)
    # KeyError, not only SyntaxError: ElementTree's path compiler raises KeyError for a
    # token it has no operator for. Catching only SyntaxError let the audit crash.
    except (SyntaxError, KeyError) as exc:
        raise NotThere(f"cited {xpath} -- ElementTree rejects it: {exc!r}") from exc
    if node is None:
        # A TRAILING POSITIONAL PREDICATE AFTER AN ATTRIBUTE PREDICATE, which is valid
        # XPath 1.0 (`property[@name='OpenRowset'][1]` = the first such property) and
        # OUTSIDE ElementTree's subset: MEASURED, ET resolves `component[1][@refId='x']`
        # and returns None for `property[@name='x'][1]`. The framework builds the second
        # order by appending `[i]` to a table-supplied xpath, so its own query engine
        # cannot re-resolve the address it emitted -- worth reporting, and NOT a reason
        # for this audit to give up on the citation. Resolved here by XPath 1.0's own
        # definition, using ET's findall.
        pm = re.match(r"^(.*)\[(\d+)\]$", xpath)
        if pm:
            try:
                candidates = root.findall(pm.group(1))
            except (SyntaxError, KeyError):
                candidates = []
            i = int(pm.group(2))
            if 1 <= i <= len(candidates):
                node = candidates[i - 1]
    if node is None:
        raise NotThere(f"cited {xpath} resolves to NO element in the raw file")
    if text_cite:
        # An element's TEXT is a value the document states, exactly as an attribute is.
        if node.text is None:
            raise NotThere(f"cited {xpath}/text(): that element has no text")
        return node.text, None, f"{xpath}/text()"
    if am is None:
        raise NodeOnly(xpath)
    attr = am.group(1)
    if attr not in node.attrib:
        raise NotThere(f"cited {xpath}/@{attr}: the element at that path states "
                       f"{sorted(node.attrib)!r} and not {attr!r}")
    return node.attrib[attr], am.group(2), f"{xpath}/@{attr}"


def locate_ktr(where, lines, _doc_path):
    """CHILD_TEXT_XML. `#ktr:<line>` is the exact line of the child element the value
    was lifted from, so the RAW LINE is read and the tag extracted from it. No XML
    parser is involved, which is the point: a .ktr contains zero real attributes, so
    an audit that re-parsed it would be reading the projection's own inventions."""
    m = _KTR_TAIL.search(where)
    if not m:
        node = re.match(r"^ktr:(\d+) ", where)
        if not node:
            raise Unlocated()
        ln = int(node.group(1))
        if ln < 1 or ln > len(lines):
            raise NotThere(f"cited ktr:{ln} is outside the file ({len(lines)} lines)")
        # citecheck.py's rule for a node line: it opens an element.
        if "<" not in lines[ln - 1] or lines[ln - 1].lstrip().startswith("</"):
            raise NotThere(f"cited ktr:{ln} is not an element start: "
                           f"{lines[ln - 1].strip()!r}")
        raise NodeOnly(f"ktr:{ln}")
    tag, line_no = m.group(1), int(m.group(2))
    if line_no < 1 or line_no > len(lines):
        raise NotThere(f"cited #ktr:{line_no} is outside the file ({len(lines)} lines)")
    src = lines[line_no - 1]
    hit = re.search(rf"<{re.escape(tag)}>(.*?)</{re.escape(tag)}>", src)
    if not hit:
        # `<tag/>` is Kettle's null AND its empty string; the projection skips those,
        # so a citation landing on one is a real disagreement and not an empty value.
        raise NotThere(f"cited #ktr:{line_no} for <{tag}>: the line reads {src.strip()!r}")
    return hit.group(1), None, f"ktr:{line_no} <{tag}>"


def locate_json(where, _lines, doc_path):
    """JSON. Walk the XPath tail against json.load of the raw file.

    The front-end's `json:<pointer>` prefix addresses the ELEMENT node, while the
    XPath tail continues DOWN from the document root into a nested member, so the
    two cannot simply be concatenated -- citecheck.py records that trap in its own
    words ("its pointer prefix and its final attribute belong to different nodes.
    Concatenating them resolves -- to the wrong member"). This walks the tail from
    the root instead, which is the same address expressed without the trap.

    TWO CITATION SHAPES, AND THE DIFFERENCE IS NOT COSMETIC. An element citation's
    tail is an absolute path from the root and ends in the member that was read. An
    EDGE citation's tail is a DESCENDANT query (`.//dependsOn[1]`) and names no
    member at all -- the emitted from/to/label are derived from that node, not read
    off one attribute of it. So the second shape is a NODE citation, and what is
    checkable about it is that its pointer resolves. Both are checked; neither is
    reported as the other.
    """
    m = _JSON_LOC.match(where)
    if not m:
        raise Unlocated()
    pointer, path = m.group(1), m.group(2)
    data = _json_data(doc_path)
    if path.startswith(".//") or not path.startswith("."):
        # A descendant query addresses a node. The pointer is the resolved address of
        # that node, so THAT is what has to hold.
        _resolve_pointer(data, pointer)
        raise NodeOnly(f"json:{pointer}")
    steps = [s for s in path.lstrip(".").split("/") if s]
    if not steps:
        raise Unlocated()
    cur = data
    walked = []
    for step in steps:
        sm = _STEP.match(step)
        if not sm:
            raise Unlocated()
        name, preds = sm.group(1), sm.group(2)
        idx = None
        want_pred = []
        for p in re.findall(r"\[([^\]]*)\]", preds):
            if p.isdigit():
                idx = int(p)
            else:
                pm = re.match(r"@([A-Za-z_][A-Za-z0-9_.$-]*)='(.*)'$", p)
                if pm:
                    want_pred.append((pm.group(1), pm.group(2)))
        if name != ".":
            if not isinstance(cur, dict) or name not in cur:
                raise NotThere(f"cited /{'/'.join(walked + [name])}: not a member of "
                               f"the {type(cur).__name__} at /{'/'.join(walked)}")
            cur = cur[name]
            walked.append(name)
        if isinstance(cur, list):
            # A positional predicate on a JSON array IS the array index (1-based in
            # the projection, because ElementTree's XPath subset is 1-based).
            i = (idx or 1) - 1
            if i >= len(cur):
                raise NotThere(f"cited /{'/'.join(walked)}[{idx}]: the array holds "
                               f"{len(cur)} member(s)")
            cur = cur[i]
            walked.append(str(i))
        elif idx is not None and idx != 1:
            raise NotThere(f"cited /{'/'.join(walked)}[{idx}]: that member is a "
                           f"{type(cur).__name__}, not an array")
        for k, v in want_pred:
            # The predicate is part of the ADDRESS, so a predicate that does not hold
            # makes the citation point somewhere the framework said it did not.
            if isinstance(cur, dict) and k in cur and _lex(cur[k]) != v:
                raise NotThere(f"cited /{'/'.join(walked)}[@{k}='{v}']: that member "
                               f"states {_lex(cur[k])!r}")
    if isinstance(cur, (dict, list)):
        # The tail resolved and ended on a node. Same treatment as the descendant
        # form: a node citation, verified to resolve, with no value to compare.
        raise NodeOnly("json:/" + "/".join(walked))
    return _lex(cur), None, "json:/" + "/".join(walked)


def _resolve_pointer(data, ptr):
    """RFC 6901, raising NotThere. The independent half of citecheck.py's json check,
    kept here so a node citation is not simply believed."""
    if ptr in ("", "/"):
        return data
    cur = data
    for tok in ptr.lstrip("/").split("/"):
        tok = tok.replace("~1", "/").replace("~0", "~")
        try:
            cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise NotThere(f"cited json:{ptr} does not resolve ({tok!r})") from exc
    return cur


LOCATORS = {
    "XML": locate_xml,
    "RECORD_BLOCK": locate_dsx,
    "CHILD_TEXT_XML": locate_ktr,
    "JSON": locate_json,
}

_XML_CACHE: dict[str, ET.Element] = {}
_JSON_CACHE: dict[str, object] = {}


def _xml_root(path):
    if path not in _XML_CACHE:
        _XML_CACHE[path] = ET.parse(path).getroot()
    return _XML_CACHE[path]


def _json_data(path):
    if path not in _JSON_CACHE:
        with open(path, encoding="utf-8") as fh:
            _JSON_CACHE[path] = json.load(fh)
    return _JSON_CACHE[path]


def _lex(v):
    """The source lexeme of a JSON scalar, matching jsondoc._lexeme so that a
    comparison of two strings is a comparison of two source values and not of two
    languages' idea of how to spell a boolean."""
    return v if isinstance(v, str) else json.dumps(v)


def _unquote(found: str) -> str:
    return found[1:-1] if len(found) >= 2 and found[0] == '"' else found


def main(table_path: str, doc_path: str) -> int:
    table = load_table(table_path)
    idn = Identification(table, doc_path)
    em = Emitter(idn)
    ir = em.emit()

    raw = open(doc_path, "rb").read().decode(getattr(idn.doc, "encoding", "utf-8"))
    lines = raw.split("\n")
    kind = (table["structure"].get("document_model") or {"kind": "XML"})["kind"]
    locate = LOCATORS[kind]

    emitted: dict[tuple[str, str], object] = {}
    families: dict[str, int] = {"InputColumns": 0, "OutputColumns": 0}
    for node in ir["nodes"]:
        emitted[(node["id"], "node.id")] = node["id"]
        el = node["element"]
        emitted[(node["id"], "element.Name")] = el.get("Name")
        for kind_of_col in ("InputColumns", "OutputColumns"):
            for i, c in enumerate(el.get(kind_of_col) or []):
                for f in ("Name", "DataType", "Precision", "Scale"):
                    if f in c:
                        emitted[(node["id"], f"element.{kind_of_col}[{i}].{f}")] = c[f]
                        families[kind_of_col] += 1

    checked = unlocated = node_ok = attr_ok = attr_bad = val_ok = val_bad = 0
    transform_checked = 0
    family_checked: dict[str, int] = {"InputColumns": 0, "OutputColumns": 0}
    failures = []
    for s in em.slots:
        if s.provenance not in (SOURCE, DERIVED):
            continue
        checked += 1
        where, transformed_from = split_transform(s.where)
        try:
            got, compound_part, cite = locate(where, lines, doc_path)
        except Unlocated:
            unlocated += 1
            continue
        except NodeOnly:
            node_ok += 1
            continue
        except NotThere as exc:
            attr_bad += 1
            failures.append(f"ATTR NOT AT CITED LOCATION  {s.element} {s.path}\n"
                            f"    {exc}")
            continue
        attr_ok += 1
        want = (transformed_from if transformed_from is not None
                else emitted.get((s.element, s.path)))
        if want is None:
            continue
        if transformed_from is not None:
            transform_checked += 1
        for _fam in family_checked:
            if s.path.startswith(f"element.{_fam}["):
                family_checked[_fam] += 1
        if compound_part:                     # a compound part: value is a member
            if str(want) in got:
                val_ok += 1
            else:
                val_bad += 1
                failures.append(f"VALUE MISMATCH {s.element} {s.path}: emitted "
                                f"{want!r} not a part of {got!r} at {cite}")
            continue
        if s.provenance == DERIVED:
            # A DERIVED value is COMPOSED from one or more readings, so equality is
            # the wrong test: the cited reading must be a COMPONENT of the emitted
            # value. Checking equality here would report every scoped node.id as a
            # mismatch, which is how this distinction was found.
            if got in str(want):
                val_ok += 1
            else:
                val_bad += 1
                failures.append(f"DERIVED VALUE NOT COMPOSED {s.element} {s.path}: "
                                f"emitted {want!r} does not contain {got!r} "
                                f"at {cite}")
            continue
        if str(want) == got:
            val_ok += 1
        else:
            val_bad += 1
            failures.append(f"VALUE MISMATCH {s.element} {s.path}: emitted {want!r}, "
                            f"file states {got!r} at {cite}")

    print("=" * 78)
    print(f"PROVENANCE AUDIT  {table['table_version']}  {doc_path.split('/')[-1]}")
    print("=" * 78)
    print(f"front-end / locator                    : {kind} -> {locate.__name__}")
    print(f"satisfied slots with a claimed reading : {checked}")
    print(f"  no locator in the citation           : {unlocated}   "
          f"(a table rule id or algorithm name, not a position in the document)")
    print(f"  cited NODE exists (no value claimed)  : {node_ok}")
    print(f"  cited attribute present at cited loc : {attr_ok}")
    print(f"  cited attribute ABSENT               : {attr_bad}")
    print(f"  emitted value matches the file       : {val_ok}")
    print(f"  emitted value DIFFERS from the file  : {val_bad}")
    print(f"  of those, citations whose emitted value is a TRANSFORM of the document's: "
          f"{transform_checked}")
    print(f"    (for those the RAW value the annotation quotes is what is compared, "
          f"since the emitted value is by construction not the file's)")
    # THE AUDIT'S OWN COVERAGE, per column family. Added because a family with
    # NOTHING in it is indistinguishable from a family that checked out clean:
    # this script reported VERDICT PASS on every .dsx while comparing ZERO
    # InputColumns values, because InputColumns was structurally empty on that
    # platform (port_policy.input_columns_from was unconditionally FIELD_EDGES and
    # a .dsx states no field-level lineage). "0 of 0 checked" and "40 of 40
    # checked" are opposite facts and a bare PASS renders them identically --
    # the same shape as `dbt compile`'s `models compiled: 0` in stage 4 of
    # aifirst-migrate.sh. NOT a failure: on a platform that states no such list
    # zero is the correct number. It is printed so nobody can read this PASS as
    # coverage it does not have.
    mech = table["port_policy"].get("input_columns_from", "FIELD_EDGES")
    print(f"  column scalars in the IR / value-checked by this audit:")
    for fam in ("InputColumns", "OutputColumns"):
        extra = f"   [port_policy.input_columns_from={mech}]" if fam == "InputColumns" else ""
        flag = "   <-- THIS AUDIT READ NOTHING HERE" if families[fam] == 0 else ""
        print(f"    {fam:14} {families[fam]:4} emitted, {family_checked[fam]:4} "
              f"value-checked{extra}{flag}")
    for f in failures:
        print("  " + f)
    print("VERDICT:", "PASS" if not failures else f"FAIL ({len(failures)})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
