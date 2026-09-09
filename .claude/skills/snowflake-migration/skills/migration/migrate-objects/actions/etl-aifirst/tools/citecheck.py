"""Falsifiability check for the two new front-ends' location oracles.

The fit score credits a field as SOURCE when a structural query produced it. That
credit is only worth something if the `where` string is CHECKABLE against the
source file. For the XML front-end it never was -- ElementTree discards line
numbers, so an Informatica `where` is an XPath and nothing more. The DataStage
pass fixed that for .dsx with line numbers, and this pass has to make the same
claim good for a lifted-attribute front-end, where the attribute in the citation
does not exist in the file at all.

So this script does not trust the front-ends. It re-reads the raw source and
verifies every location they emitted:

  JSON     every `json:<pointer>` must resolve against json.load of the file,
           and every attr_ref tail must resolve to a scalar or array member.
  KTR      every `ktr:<line>` must be the start line of an element, and every
           `#ktr:<line>` on a lifted value must be a line whose text contains
           the cited tag AND the value that was read from it.

Usage (from tools/):
  python3 citecheck.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from fixture_paths import fixtures_root

_TOOLS = Path(__file__).resolve().parent
_ACTION = _TOOLS.parent
_SCRIPTS = _ACTION / "scripts"
_PLATFORMS = _ACTION / "platforms"
_INPUTS = fixtures_root() / "inputs" / "inputs"
KTR = _INPUTS / "pentaho"
ADF = _INPUTS / "adf"

_JSON_PTR = re.compile(r"json:(/[^\s]*|/)")
_KTR_NODE = re.compile(r"ktr:(\d+) ")
_KTR_ATTR = re.compile(r"/([A-Za-z_][A-Za-z0-9_.-]*)/text\(\)#ktr:(\d+)")


def run(table: str, doc: Path) -> str:
    table_path = _PLATFORMS / table
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        out_path = tmp.name
    try:
        completed = subprocess.run(
            [sys.executable, str(_SCRIPTS / "main.py"), str(table_path), str(doc), out_path],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(_SCRIPTS),
        )
        return completed.stdout
    finally:
        Path(out_path).unlink(missing_ok=True)


def unesc(tok: str) -> str:
    return tok.replace("~1", "/").replace("~0", "~")


def resolve(data, ptr: str):
    """RFC 6901. Raises on a pointer that does not resolve."""
    if ptr in ("", "/"):
        return data
    cur = data
    for tok in ptr.lstrip("/").split("/"):
        tok = unesc(tok)
        if isinstance(cur, list):
            cur = cur[int(tok)]
        elif isinstance(cur, dict):
            cur = cur[tok]
        else:
            raise KeyError(f"{ptr}: cannot descend into {type(cur).__name__} at {tok!r}")
    return cur


def check_json(name: str) -> int:
    path = ADF / name
    data = json.loads(path.read_text(encoding="utf-8"))
    text = run("platform_adf.json", path)
    ptrs = _JSON_PTR.findall(text)
    ok = bad = 0
    for p in sorted(set(ptrs)):
        try:
            resolve(data, p)
            ok += 1
        except Exception as e:
            bad += 1
            print(f"  FAIL {p}: {e}")
    print(
        f"{name:26} {len(ptrs):4} json: locations, {len(set(ptrs)):3} distinct, "
        f"{ok} RESOLVE, {bad} FAIL"
    )

    # Stronger claim for the SOURCE-credited element citations: reconstruct the
    # FULL pointer -- the front-end's node pointer plus the attr_ref tail -- and
    # check that it resolves to the value the report says was read. The report
    # states that value in the [@name='X'] predicate, so the check is closed.
    #
    # DELIBERATELY NOT CHECKED, and this is the honest limit: a CHILD_ATTR
    # citation reads json:<ACTIVITY pointer> then a projection path DOWN to a
    # nested object, so its pointer prefix and its final attribute belong to
    # different nodes. Concatenating them resolves -- to the wrong member. That
    # citation is mechanically recoverable by a reader (drop the [n] indices and
    # append the path to the pointer) and is NOT verified here.
    vok = vbad = 0
    for line in text.split("\n"):
        m = re.search(r"json:(\S+) \S*\[@(\w+)='([^']*)'\]((?:/[^/\s\[\]]+)+)$", line)
        if not m:
            continue
        ptr, pred_attr, expected, tail = m.groups()
        if tail.count("/") != 1 or tail != "/" + pred_attr:
            continue
        try:
            got = resolve(data, ptr + tail)
        except Exception as e:
            vbad += 1
            print(f"  FAIL value {ptr}{tail}: {e}")
            continue
        if got == expected:
            vok += 1
        else:
            vbad += 1
            print(f"  FAIL value {ptr}{tail}: resolved {got!r}, report says {expected!r}")
    print(
        f"{'':26} {vok + vbad:4} element citations reconstructed to a full "
        f"pointer, {vok} RESOLVE TO THE STATED VALUE, {vbad} FAIL"
    )
    return bad + vbad


def check_ktr(name: str) -> int:
    path = KTR / name
    lines = path.read_text(encoding="utf-8").split("\n")
    text = run("platform_pentaho.json", path)
    nodes = _KTR_NODE.findall(text)
    ok = bad = 0
    for ln in sorted(set(int(x) for x in nodes)):
        if "<" in lines[ln - 1] and not lines[ln - 1].lstrip().startswith("</"):
            ok += 1
        else:
            bad += 1
            print(f"  FAIL node line {ln}: {lines[ln - 1]!r} is not an element start")
    attrs = _KTR_ATTR.findall(text)
    aok = abad = 0
    for tag, ln in sorted(set(attrs)):
        src = lines[int(ln) - 1]
        if f"<{tag}>" in src and f"</{tag}>" in src:
            aok += 1
        else:
            abad += 1
            print(f"  FAIL attr {tag} at line {ln}: {src!r} does not contain <{tag}>...</{tag}>")
    # Stronger claim, on the closed subset where the report also states the VALUE:
    # a citation whose tail tag is the same tag the LAST xpath predicate filters on
    # must land on a line reading <tag>THAT EXACT VALUE</tag>. This is what makes
    # "/name/text()#ktr:451" a real address even though the file has no attributes
    # -- tag, line and value all have to agree at once.
    #
    # A citation whose tail tag DIFFERS from the predicate reads a different member
    # of the same element (the predicate says which <step>, the tail says which of
    # its children), so the report states no value to compare and only the weaker
    # tag+line check above applies to it.
    vok = vbad = skipped = 0
    for line in text.split("\n"):
        m = re.search(r"/([A-Za-z_][A-Za-z0-9_.-]*)/text\(\)#ktr:(\d+)\s*$", line)
        if not m:
            continue
        tag, ln = m.group(1), int(m.group(2))
        preds = re.findall(r"\[@(\w+)='([^']*)'\]", line)
        if not preds or preds[-1][0] != tag:
            skipped += 1
            continue
        if f"<{tag}>{preds[-1][1]}</{tag}>" in lines[ln - 1]:
            vok += 1
        else:
            vbad += 1
            print(
                f"  FAIL value <{tag}> at line {ln}: {lines[ln - 1]!r} "
                f"does not state {preds[-1][1]!r}"
            )
    print(
        f"{name:26} {len(nodes):4} ktr: node locations, {len(set(nodes)):3} distinct, "
        f"{ok} RESOLVE, {bad} FAIL"
    )
    print(
        f"{'':26} {len(attrs):4} lifted-value citations, {len(set(attrs)):3} distinct, "
        f"{aok} RESOLVE, {abad} FAIL"
    )
    print(
        f"{'':26} {vok + vbad:4} of those checked TAG+LINE+VALUE together, "
        f"{vok} AGREE, {vbad} FAIL  ({skipped} state no value to compare)"
    )
    return bad + abad + vbad


if __name__ == "__main__":
    if not KTR.is_dir() or not ADF.is_dir():
        print(
            f"Missing fixture inputs under {fixtures_root()}/inputs/inputs/ "
            "(need pentaho/ and adf/).",
            file=sys.stderr,
        )
        sys.exit(2)
    fails = 0
    print("=" * 78)
    print("LOCATION-ORACLE FALSIFIABILITY CHECK")
    print("=" * 78)
    for n in ("safe-stop-gen-rows.ktr", "sample_trans.ktr"):
        fails += check_ktr(n)
    for n in ("myPipeline.json", "adf_First_Pipeline.json"):
        fails += check_json(n)
    print("=" * 78)
    print("ALL LOCATIONS RESOLVE" if fails == 0 else f"{fails} UNRESOLVABLE LOCATIONS")
    sys.exit(1 if fails else 0)
