"""ADDITION 1 — the declared-versus-identified gate.
ADDITION 2 — the same gate, now over EVERY RECORD IN THE DOCUMENT.

Exit codes, stated precisely because the two modes mean opposite things by design:

  (default)  0 when EVERY canonical run accounts for every record in its document.
             NON-ZERO on any loss. This is the gate.
  --all      additionally runs the KNOWN_BAD fixtures, which are EXPECTED to
             report FAIL. Their failure is the pass condition: exit is non-zero
             when the gate FAILS TO FIRE on a known loss. It also runs the CENSUS
             falsifiability checks below. The canonical check still applies, so
             `--all` exits 0 only when the clean set is clean AND every known-bad
             fixture was caught AND both census checks fire.

Why this gate exists, stated as the measurement that forced it:

    fixture                        declared  identified  TOTAL FIT
    WF_PARAMFILE_MULTI_SESSION.XML        9           3      89.9%
    MappingForTest.XML                    7           7      84.8%

`fit.score` divides satisfied obligations by obligations RAISED, and an element
that was never identified raises none. So the document that lost two thirds of its
elements scored HIGHER than the one that lost none -- the highest fit of any
document in this project. A quality metric that rewards data loss is worse than no
metric, because it is confidently wrong rather than merely incomplete.

So the fit number may not be reported alone. This gate is the thing that has to
pass first, and it asserts positively.

WHAT ADDITION 2 CHANGED ABOUT THIS GATE'S SEMANTICS -- read this before comparing
a number here against an older run
------------------------------------------------------------------------------
`declared` USED TO MEAN "nodes the level queries matched". It was appended inside
the level sweep, so THE GATE'S DENOMINATOR WAS THE THING IT WAS CHECKING. An
element no level query matched was not reported lost; it was not reported at all.
MEASURED on CustomerSummaryDerive.dsx: 5 elements in the document, this gate
printed `declared=4 keyless=0 identified=4 lost=0 balances=True PASS`, and the
record it could not see was the CTransformerStage holding every derivation in the
job.

`declared` now means EVERY RECORD IN THE DOCUMENT and the identity is

    declared = identified + lost + keyless + excluded + unknown

`excluded` are records a DECLARED, NAMED, REASONED rule in the platform table
(`structure.census.exclusions`) says are not elements -- property rows, port rows,
edge records, export envelopes, canvas geometry. `unknown` are UNKNOWN OBJECTS:
records nothing in the table recognises, inventoried with a citable location.

WHAT DID *NOT* CHANGE: `lost` still means "identified, then silently overwritten by
a later record with the same key", and it is still the number that must be zero.
The PASS/FAIL condition is unchanged -- `lost == 0 and balances`.

AN UNKNOWN COUNT IS NOT A FAILURE AND IS NOT GATED. A record the table does not
recognise is tracked rather than lost, which is the entire point; gating on it
would create pressure to write exclusion rules until the column reads zero, and a
table tuned to a pretty number is exactly what this change exists to prevent. The
column is printed so it cannot be ignored, and `unknowns` prints the inventory.

Usage: python3 declared_vs_identified.py            # the 7 canonical runs
       python3 declared_vs_identified.py --all      # + every falsifiability check
       python3 declared_vs_identified.py --unknowns # + the unknown-object inventory
"""

import io
import os
import sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
_SCRIPTS = _TOOLS.parent / "scripts"
for _p in (_SCRIPTS, _TOOLS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import fit
from emit import Emitter
from identify import Identification, load_table, validate_table
from runall import RUNS

from fixture_paths import engine_tests_root, fixtures_root

_FX = fixtures_root()
_ENG = engine_tests_root()

def _eng(*parts: str) -> str:
    """Path under AIFIRST_ENGINE_TESTS, or empty string if unset (entries skipped)."""
    if _ENG is None:
        return ""
    return str(_ENG.joinpath(*parts))

def _fx(*parts: str) -> str:
    return str(_FX.joinpath(*parts))

# Back-compat names used below (no machine-absolute defaults).
SC = str(_ENG) + "/" if _ENG is not None else ""
POC = str(_FX)  # fixtures replace orch poc/

# Documents that LOSE elements to a key collision. They are not part of the gate's
# pass/fail set -- they are its falsifiability half. A gate that only ever runs on
# clean documents is not evidence that it can detect a dirty one, so `--all` proves
# it fires. Each is a shipped repo fixture, not something authored for this spike.
#
# THEY NO LONGER LOSE ANYTHING AS SHIPPED, AND THAT SILENTLY RETIRED THIS WHOLE ARM.
# FRAMEWORK CHANGE 66(c) added `key_scope` to platform_informatica.json, scoping an
# element key by its enclosing MAPPING. All three of these lose elements ONLY because
# several mappings in one file reuse instance names, so scoping the key fixed them --
# genuinely and correctly. MEASURED, both ways, on the same three files:
#
#     fixture             key_scope present     key_scope removed
#     inf-multisession    9 -> 9  lost 0        9 -> 3   lost 6
#     inf-sqgaps         11 -> 11 lost 0       11 -> 8   lost 3
#     inf-mapplet        12 -> 12 lost 0       12 -> 9   lost 3
#
# So from FRAMEWORK CHANGE 66(c) until now, `--all` asserted that three fixtures MUST
# fail while none of them could, and it exited non-zero for that reason and not
# because of any loss. A gate whose falsifiability arm has quietly become unable to
# fire is the same class of defect as the ledger blind spot this file exists for.
#
# THE FIX IS NOT TO DELETE THE ARM. The loss is real and reproducible; what changed is
# the TABLE CONFIGURATION it needs. Each entry now names the mutation that reproduces
# it -- applied to a table loaded in memory, never to a file -- and the fixtures also
# run AS SHIPPED so the record shows both readings.
KNOWN_BAD = [
    ("inf-multisession", "platform_informatica.json",
     SC + "Tests_/Integration/TransformationTests/EtlToDbt/Sources/"
          "InformaticaPowerCenter/WF_PARAMFILE_MULTI_SESSION.XML"),
    ("inf-sqgaps", "platform_informatica.json",
     SC + "TestsSourceCode/SourceCode/EtlToDbt/InfPc/Registry/SourceQualifierGaps/"
          "SampleProject/SQGAPS/wf_sq_gaps.xml"),
    ("inf-mapplet", "platform_informatica.json",
     SC + "TestsSourceCode/SourceCode/EtlToDbt/InfPc/Registry/MappletPart/mapplet_part.xml"),
]


def unscope(table: dict) -> dict:
    """Remove `key_scope`, reproducing the table as it was before FRAMEWORK CHANGE
    66(c). This is the ONE mutation that makes the KNOWN_BAD fixtures lose elements
    again, and it is applied to a loaded dict -- no file is touched."""
    table["structure"].pop("key_scope", None)
    return table

# THE DOCUMENT THE CENSUS EXISTS FOR. The measured instance, kept as a named
# constant because both census checks below run against it.
CENSUS_DOC = _fx("blind-run", "datastage", "CustomerSummaryDerive.dsx")

HDR = (f"{'run':18} {'declared':>8} {'elements':>8} {'keyless':>7} {'excluded':>8} "
       f"{'unknown':>7} {'lost':>4} {'bal':>5} {'TOTAL FIT':>10} {'UNSAT':>6}  verdict")
# UNSAT is printed beside the percentage and is not decoration. A fit percentage can
# rise two ways -- by satisfying an obligation or by RETIRING one -- and only the first
# is progress. The unsatisfied count distinguishes them at a glance: it falls only when
# a cost is genuinely gone, and it rises when a cost that was invisible becomes visible,
# which is the direction this gate exists to reward.


def measure(slug, table_path, doc_path, table=None):
    buf = io.StringIO()
    with redirect_stdout(buf):
        tbl = table or load_table(table_path)
        idn = Identification(tbl, doc_path)
        em = Emitter(idn)
        em.emit()
    acc = idn.accounting()
    scored = fit.score(em.slots)
    acc["fit"] = scored["total"]["fit"]
    acc["satisfied"] = scored["total"]["satisfied"]
    acc["obligations"] = scored["total"]["total"]
    acc["unsatisfied"] = acc["obligations"] - acc["satisfied"]
    acc["slug"] = slug
    acc["columns"] = column_census(tbl, idn)
    return acc


def column_census(table: dict, idn) -> dict | None:
    """THE COLUMN LEDGER: columns the DOCUMENT states vs ports the table READ.

    None when the platform table declares no `structure.census.column_census`, which
    is the case on four of five platforms and is a declared decision rather than an
    omission -- see each table's own note.

    WHY THIS IS A SEPARATE LEDGER AND NOT A LINE IN THE RECORD ONE. The record ledger
    asks whether every RECORD was accounted for. It closes on CustomerSummaryDerive.dsx
    whether or not a single column was read, because a column subrecord is not a record
    and is excluded from that ledger by a named rule. So the record gate can pass at
    100% on a document whose every column vanished -- and that is the exact state that
    document was in: 5 of 5 stages with ports=0, 4 of 4 models column-less, the record
    ledger balancing, and the fit score reporting NO column obligations to fail because
    a PORT-keyed obligation needs a port to exist.

    THE DENOMINATOR IS INDEPENDENT BY CONSTRUCTION. `document_query` sweeps the whole
    projected tree for subrecords stating the datatype attribute, with no reference to
    any port site, any section name or any pin class. Every one of those is a thing a
    port site can get wrong, and all three HAVE been wrong on this platform: the holder
    was assumed to be `Columns` (it is whatever key preceded the run) and the pin class
    was assumed to be CCustomInput/CCustomOutput (a Transformer's are CTrxInput/
    CTrxOutput and an unprefixed spelling exists too). A denominator that shared any of
    those assumptions would have gone quiet in exactly the same way the readers did."""
    cc = ((table.get("structure") or {}).get("census") or {}).get("column_census")
    if not cc:
        return None
    stated = len(idn.root.findall(cc["document_query"]))
    read = sum(len(el.ports) for el in idn.elements.values())
    return {"stated": stated, "read": read, "shortfall": max(0, stated - read),
             "query": cc["document_query"]}


def line(a):
    ok = a["lost"] == 0 and a["balances"]
    cols = a.get("columns")
    if cols and cols["shortfall"]:
        ok = False
    verdict = "PASS"
    if not ok:
        if a["lost"]:
            verdict = f"FAIL: {a['lost']} element(s) silently overwritten"
        elif not a["balances"]:
            verdict = "FAIL: the ledger does not close -- see `bal` breakdown below"
        else:
            verdict = (f"FAIL: {cols['shortfall']} stated column(s) reached no port "
                       f"site -- see COLUMN CENSUS")
    return (f"{a['slug']:18} {a['declared']:8} {a['identified']:8} {a['keyless']:7} "
            f"{a['excluded']:8} {a['unknown']:7} {a['lost']:4} "
            f"{str(a['balances'])[:5]:>5} {a['fit'] * 100:9.1f}% "
            f"{a.get('unsatisfied', 0):6}  " + verdict), ok


def arithmetic(a) -> str:
    """The identity spelled out, per document, so the sum is checkable by eye."""
    return (f"      {a['declared']} records = {a['identified']} elements "
            f"+ {a['lost']} lost + {a['keyless']} keyless + {a['excluded']} excluded "
            f"+ {a['unknown']} unknown"
            f"   [sums={a['document_sums']}, element-ledger={a['element_ledger_balances']}, "
            f"no-double-level-match={a['no_double_level_match']}, "
            f"contested={len(a['contested'])}]")


def show_unknowns(a, limit=12) -> None:
    c = Counter()
    first: dict[str, str] = {}
    for u in a["unknown_objects"]:
        ident = " ".join(f"{k}={v}" for k, v in u.identity.items())
        key = f"<{u.tag}> {ident}".strip()
        c[key] += 1
        first.setdefault(key, u.where)
    for key, n in c.most_common(limit):
        print(f"        {n:4}x {key}")
        print(f"              first at {first[key]}")
    if len(c) > limit:
        print(f"        ... {len(c) - limit} further unknown shapes")


def main(argv) -> int:
    want_unknowns = "--unknowns" in argv or "--all" in argv
    print("=" * 110)
    print("DECLARED-VERSUS-IDENTIFIED GATE   (the fit score is unreadable without this)")
    print("declared = every record in the document = elements + lost + keyless "
          "+ excluded + unknown")
    print("=" * 110)
    print(HDR)
    print("-" * 110)
    failures = []
    measured = []
    for slug, tp, dp in RUNS:
        a = measure(slug, tp, dp)
        measured.append(a)
        txt, ok = line(a)
        print(txt)
        print(arithmetic(a))
        if not ok:
            failures.append(a)
    print("-" * 110)
    if failures:
        print(f"GATE FAILED on {len(failures)} of {len(RUNS)} canonical runs.")
        for a in failures:
            for c in a["collisions"]:
                print(f"  {a['slug']}  key {c['key']!r} ({c['level']})")
                print(f"      kept {c['kept_where']}")
                print(f"      lost {c['lost_where']}")
            for c in a["contested"]:
                print(f"  {a['slug']}  TABLE BUG: exclusion rule {c['rule']!r} claims a "
                      f"node the {c['level']!r} level matched, at {c['where']}")
    else:
        print(f"GATE PASSED: all {len(RUNS)} canonical runs account for every record in "
              "their document. No element is lost, so no fit number above is inflated "
              "by a loss.")

    print()
    print("=" * 110)
    print("COLUMN CENSUS. Columns the DOCUMENT states, against ports the table READ. "
          "The record ledger above")
    print("cannot see this: a column subrecord is not a record, so that ledger closes "
          "at 100% on a document")
    print("whose every column vanished -- which is the measured state "
          "CustomerSummaryDerive.dsx was in.")
    print("=" * 110)
    any_cc = False
    for a in measured:
        cc = a.get("columns")
        if cc is None:
            print(f"{a['slug']:18} not declared  (table states no "
                  f"structure.census.column_census; see that table's residue note)")
            continue
        any_cc = True
        flag = ("   <-- SHORTFALL: a stated column reached no port site"
                if cc["shortfall"] else "")
        print(f"{a['slug']:18} {cc['stated']:5} stated by the document, "
              f"{cc['read']:5} read as ports{flag}")
        print(f"                   independent denominator: {cc['query']}")
    if not any_cc:
        print("NOTE no canonical run declares a column census, so this section proves "
              "nothing today.")
    # AND THE DOCUMENT THE CHECK EXISTS FOR, GATED. MaskDemo.dsx states 2 columns, so
    # the canonical row above can only ever prove 2 things. CustomerSummaryDerive.dsx
    # states 16 across six pin records in three OLEType spellings and two section
    # namings, and is the document that measured 0 of 16 when the port sites still
    # assumed `Columns` and CCustom*. It is not in RUNS -- it is the blind Gate A
    # input -- so it is measured here explicitly rather than left to a run that does
    # not cover it.
    blind = measure("ds-blind*", "platform_datastage.json", CENSUS_DOC)
    bcc = blind["columns"]
    bad = bcc["shortfall"] > 0
    print(f"{blind['slug']:18} {bcc['stated']:5} stated by the document, "
          f"{bcc['read']:5} read as ports"
          + ("   <-- SHORTFALL" if bad else "")
          + f"      [{os.path.basename(CENSUS_DOC)}, GATED, not in RUNS]")
    if bad:
        failures.append(blind)
        print(f"      *** {bcc['shortfall']} stated column(s) reached no port site. "
              f"Every column-keyed no_slot fact on this platform is keyed from PORT, "
              f"so those columns' cost is not merely absent from the IR -- it is "
              f"absent from the DENOMINATOR, and the fit score rises. ***")

    print()
    print("=" * 110)
    print("EXCLUSIONS, PER RULE. Every one of these is a table-declared claim that a "
          "record is NOT an element.")
    print("A rule that excludes too much is a rule a reviewer can find here and "
          "argue with; that is the design.")
    print("=" * 110)
    for a in measured:
        print(f"{a['slug']:18} {a['excluded']:5} excluded, {a['unknown']:5} unknown")
        for rid, n in a["excluded_by_rule"].items():
            flag = "   <-- matched nothing in this document" if n == 0 else ""
            print(f"      {n:6}  {rid}{flag}")
        if a["overlaps"]:
            print(f"      NOTE {len(a['overlaps'])} node(s) matched by more than one "
                  f"rule; attributed to the first in table order")

    if want_unknowns:
        print()
        print("=" * 110)
        print("UNKNOWN OBJECTS. Records the platform table does not recognise, "
              "INVENTORIED rather than dropped.")
        print("A large count here is an expected first result, not a failure. Each "
              "entry cites where it was READ.")
        print("=" * 110)
        for a in measured:
            print(f"{a['slug']:18} {a['unknown']} unknown object(s)")
            show_unknowns(a)

    if "--all" in argv:
        # Falsifiability 1a: the shipped fixtures AS SHIPPED. NOT gated -- printed so
        # the record shows that they are clean today and why.
        print()
        print("=" * 110)
        print("FALSIFIABILITY 1a — the known-bad fixtures AS SHIPPED, with the current "
              "table. Context, not a gate.")
        print("FRAMEWORK CHANGE 66(c) added key_scope and genuinely FIXED all three. "
              "See the KNOWN_BAD comment.")
        print("=" * 110)
        print(HDR)
        print("-" * 110)
        for slug, tp, dp in KNOWN_BAD:
            a = measure(slug, tp, dp)
            print(line(a)[0])

        # Falsifiability 1b: prove the LOSS half of the gate FIRES. If these came back
        # PASS the gate would be measuring nothing.
        print()
        print("=" * 110)
        print("FALSIFIABILITY 1b — the same fixtures with key_scope REMOVED, which is "
              "the configuration the")
        print("loss was measured in. These MUST fail.")
        print("=" * 110)
        print(HDR)
        print("-" * 110)
        fired = 0
        for slug, tp, dp in KNOWN_BAD:
            a = measure(slug + "*", None, dp, table=unscope(load_table(tp)))
            txt, ok = line(a)
            print(txt)
            print(arithmetic(a))
            if not ok:
                fired += 1
                for c in a["collisions"]:
                    print(f"      key {c['key']!r}: kept {c['kept_where']}")
                    print(f"      {'':16}  lost {c['lost_where']}")
        print("-" * 110)
        print(f"gate fired on {fired} of {len(KNOWN_BAD)} known-bad fixtures"
              + ("" if fired == len(KNOWN_BAD)
                 else "  <-- THE GATE IS NOT DETECTING A KNOWN LOSS"))
        # DELIBERATE INVERSION, and the reason it reads backwards: in this block a
        # FAIL verdict is the desired outcome, so the error condition is a fixture
        # that came back PASS. `fired < len(KNOWN_BAD)` means the gate went quiet on
        # a loss we have already measured -- which is the one failure that would make
        # every PASS above meaningless.
        if fired != len(KNOWN_BAD):
            return 1

        if not census_falsifiability():
            return 1

        if not column_census_falsifiability():
            return 1

        if not table_validator_falsifiability():
            return 1

        if not attr_residue_falsifiability():
            return 1

    return 1 if failures else 0


def column_census_falsifiability() -> bool:
    """FALSIFIABILITY 4 — the COLUMN CENSUS must fire on the configuration it was
    written for, and that configuration is not invented: it is the port_sites
    platform_datastage.json actually shipped before the `*` / `[@SqlType]` widening.

    Restored here IN MEMORY: the holder is `Columns` (a literal section name, when a
    .dsx section is named after whatever scalar key preceded the run) and only the
    CCustomInput/CCustomOutput pin spellings (when CustomerSummaryDerive.dsx spells
    them CustomInput/CustomOutput and a Transformer's CTrxInput/CTrxOutput). Both
    halves miss for every pin on that document, which is how it measured 5 stages with
    ports=0 and 4 column-less models WHILE THE RECORD LEDGER BALANCED AT 100%.

    THE POINT OF THE CHECK IS THE LEDGER, not the port count -- and the direction it
    moves was MEASURED here rather than assumed, because the first version of this
    check asserted the wrong one. With no ports there are no column obligations at all,
    so the type-code cost, the placeholder-precision cost and the dangling-column cost
    leave the DENOMINATOR. What that does to the percentage depends on the satisfied/
    unsatisfied mix of what vanished: on CustomerSummaryDerive.dsx 83 obligations
    disappear, 65 of them satisfied and 18 unsatisfied, so the fit FALLS (67.1% ->
    53.0%) while UNSATISFIED also falls (49 -> 31). So a percentage cannot detect this
    and the unsatisfied count can: 18 real costs left the ledger with nothing to say so.
    THAT is why the gate is a column-count identity and not a threshold on fit, and why
    the run table prints UNSAT beside every percentage."""
    ok = True
    print()
    print("=" * 110)
    print("FALSIFIABILITY 4 — a STATED COLUMN THAT REACHES NO PORT SITE must fail the "
          "gate, not raise the score.")
    print("=" * 110)
    good = measure("ds-blind", "platform_datastage.json", CENSUS_DOC)
    t = load_table("platform_datastage.json")
    for ps in t["structure"]["self_def_site"]["port_sites"]:
        ps["xpath"] = ps["xpath"].replace("/*/", "/Columns/")
    t["structure"]["self_def_site"]["port_sites"] = [
        ps for ps in t["structure"]["self_def_site"]["port_sites"]
        if "CCustom" in ps["xpath"]]
    bad = measure("ds-blind-narrow", None, CENSUS_DOC, table=t)
    for a in (good, bad):
        txt, _ = line(a)
        print(txt)
        cc = a["columns"]
        print(f"      columns: {cc['stated']} stated / {cc['read']} read"
              f"   ({cc['shortfall']} shortfall)   fit {a['fit'] * 100:.1f}%  "
              f"obligations {a['satisfied']}/{a['obligations']}  "
              f"UNSATISFIED {a['unsatisfied']}")
    fired = bad["columns"]["shortfall"] == 16 and not line(bad)[1]
    # THE GIVEAWAY IS THE UNSATISFIED COUNT, NOT THE PERCENTAGE. Asserted in the
    # direction that was measured: 18 unmet column obligations leave the ledger.
    cost_left = bad["unsatisfied"] < good["unsatisfied"]
    if fired and cost_left:
        print(f"  FIRED: 16 of 16 stated columns reached no port site and the run is "
              f"reported FAIL.")
        print(f"         UNSATISFIED fell from {good['unsatisfied']} to "
              f"{bad['unsatisfied']} and total obligations from "
              f"{good['obligations']} to {bad['obligations']} -- "
              f"{good['unsatisfied'] - bad['unsatisfied']} real costs left the")
        print(f"         ledger because the columns they are keyed to were never read. "
              f"Fit moved {good['fit'] * 100:.1f}% -> {bad['fit'] * 100:.1f}%, which is "
              f"the wrong signal to")
        print(f"         watch: it depends on the satisfied/unsatisfied mix of what "
              f"vanished, so only the column identity catches this.")
    else:
        ok = False
        print("  *** DID NOT FIRE: shortfall="
              f"{bad['columns']['shortfall']} (want 16), verdict_ok={line(bad)[1]} "
              f"(want False), unsatisfied fell={cost_left} (want True). ***")

    print()
    print("  CONTROL: the census must NOT fire on a table that reads its columns. "
          "The unmutated row above")
    print("  reports 16 stated / 16 read and PASS, so the check distinguishes the two "
          "configurations rather")
    print("  than failing everything.")
    if good["columns"]["shortfall"] or not line(good)[1]:
        ok = False
        print("  *** THE CONTROL FAILED: the census fires on a healthy table, so a "
              "SHORTFALL means nothing. ***")
    return ok


def table_validator_falsifiability() -> bool:
    """FALSIFIABILITY 5 — `identify.validate_table` must RAISE on each of the two
    shipped table bugs it was written for, and must NOT raise on the fixed tables.

    Both mutations restore a real previous state of a real file, in memory:
      * platform_informatica.json's Target Definition with def_site 'SELF', which left
        `structure.def_sites.target` -- and its TARGETFIELD port site -- unreachable.
      * platform_ssis.json's role_to_node_type without TARGET, while its own
        kind_dispatch declares role TARGET for Microsoft.OLEDBDestination.

    A validator that cannot be made to raise is a comment with a function signature."""
    ok = True
    print()
    print("=" * 110)
    print("FALSIFIABILITY 5 — a DECLARED-BUT-UNREACHABLE reader and an UNMAPPED "
          "DECLARABLE role must RAISE.")
    print("=" * 110)
    cases = [
        ("informatica def_site 'SELF' (unreachable def_sites.target)",
         "platform_informatica.json",
         lambda t: t["kind_dispatch"]["Target Definition"].__setitem__("def_site", "SELF"),
         "def_sites declares"),
        ("ssis role_to_node_type without TARGET",
         "platform_ssis.json",
         lambda t: t["role_to_node_type"].pop("TARGET"),
         "role_to_node_type does not map"),
    ]
    for label, path, mutate, want in cases:
        t = load_table(path)
        mutate(t)
        try:
            validate_table(t)
        except ValueError as exc:
            hit = want in str(exc)
            print(f"  {'FIRED  ' if hit else 'WRONG  '} {label}")
            print(f"           {str(exc)[:160]}")
            if not hit:
                ok = False
        else:
            ok = False
            print(f"  *** DID NOT FIRE: {label} -- validate_table accepted it. ***")
    for path in ("platform_informatica.json", "platform_ssis.json",
                 "platform_datastage.json", "platform_pentaho.json",
                 "platform_adf.json"):
        try:
            validate_table(load_table(path))
        except ValueError as exc:
            ok = False
            print(f"  *** THE CONTROL FAILED: shipped {path} does not validate: "
                  f"{exc} ***")
    print("  CONTROL: all five shipped tables validate, so the checks above "
          "distinguish a broken table")
    print("           from any table at all.")
    return ok


def attr_residue_falsifiability() -> bool:
    """FALSIFIABILITY 6 — the RESIDUAL PROPERTY SWEEP must be the thing that makes
    `write_mode` visible, and its guards must refuse a table it cannot serve.

    THE MEASURED FACT UNDER TEST: CustomerSummaryDerive.dsx states
    `write_mode "append"` at dsx:323-324 on V0S4, the stage that writes
    CUSTOMER_SUMMARY. A mart materialized as a table replaces its rows every run, so
    from run 2 the migration and the document disagree about the target's contents.
    With `dsx_unread_stage_property` removed the string is in NO obligation anywhere;
    with it present there is one RESIDUE obligation citing the line. The check asserts
    both directions, because only the pair shows the rule is load-bearing.

    Then the two guards, each restoring a configuration someone would plausibly write:
      * the rule declared on platform_pentaho.json, whose attr_site is SELF_ATTRS and
        whose bag therefore holds @name and @type -- the element's own identity.
      * the rule declared twice, which double-counts every unread key."""
    ok = True
    print()
    print("=" * 110)
    print("FALSIFIABILITY 6 — the RESIDUAL PROPERTY SWEEP must make `write_mode` "
          "appear, and must refuse")
    print("a table whose property bag it cannot read.")
    print("=" * 110)

    def facts(table, doc=CENSUS_DOC):
        buf = io.StringIO()
        with redirect_stdout(buf):
            idn = Identification(table, doc)
            em = Emitter(idn)
            em.emit()
        return em.slots

    with_rule = facts(load_table("platform_datastage.json"))
    t = load_table("platform_datastage.json")
    t["no_slot_facts"] = [r for r in t["no_slot_facts"]
                          if r["id"] != "dsx_unread_stage_property"]
    without = facts(t)
    hits = [s for s in with_rule if "write_mode" in s.path]
    gone = [s for s in without if "write_mode" in s.path]
    if hits and not gone:
        print(f"  FIRED: with the rule, {len(hits)} obligation(s) name write_mode:")
        for s in hits:
            print(f"           [{s.provenance}] {s.path}  = {s.detail!r}")
            print(f"           at {s.where}")
        print(f"         with the rule removed, {len(gone)} -- the string appears in "
              f"no obligation at all,")
        print(f"         which is the state the document shipped in. Obligations "
              f"{len(without)} -> {len(with_rule)}.")
    else:
        ok = False
        print(f"  *** DID NOT FIRE: with_rule={len(hits)} (want >0), "
              f"without={len(gone)} (want 0). ***")

    for label, path, mutate, want in [
        ("ATTR_RESIDUE on a SELF_ATTRS attr_site (pentaho)", "platform_pentaho.json",
         lambda t: t["no_slot_facts"].append(
             {"id": "INJECTED", "from": "ATTR_RESIDUE"}),
         "SELF_ATTRS"),
        ("two ATTR_RESIDUE rules (datastage)", "platform_datastage.json",
         lambda t: t["no_slot_facts"].append(
             {"id": "INJECTED-SECOND", "from": "ATTR_RESIDUE"}),
         "COMPLEMENT"),
        ("an unimplemented no_slot_facts rule kind", "platform_datastage.json",
         lambda t: t["no_slot_facts"].append(
             {"id": "INJECTED-BOGUS-KIND", "from": "NOT_A_RULE_KIND"}),
         "does not implement"),
    ]:
        t = load_table(path)
        mutate(t)
        doc = CENSUS_DOC if "datastage" in path else (
            _fx("inputs", "inputs", "pentaho", "safe-stop-gen-rows.ktr"))
        try:
            facts(t, doc)
        except ValueError as exc:
            hit = want in str(exc)
            print(f"  {'FIRED  ' if hit else 'WRONG  '} {label}")
            print(f"           {str(exc)[:150]}")
            if not hit:
                ok = False
        else:
            ok = False
            print(f"  *** DID NOT FIRE: {label} was accepted. ***")
    return ok


def census_falsifiability() -> bool:
    """FALSIFIABILITY 2 and 3 — prove the CENSUS half does its job.

    The loss checks above cannot test it. A key collision is a loss the OLD ledger
    could already see; the whole point of ADDITION 2 is the loss it could NOT see --
    a record no level query matched, which never entered the denominator. So this
    runs the measured instance with the level that identifies it DELETED, and
    requires the record to come back as an Unknown Object with a citable location.

    Neither check mutates a file. Both edit a loaded table in memory, which is also
    the point: they are testing the FRAMEWORK's response to a table that does not
    cover a document, not a particular table's contents.
    """
    ok = True
    print()
    print("=" * 110)
    print("FALSIFIABILITY 2 — a record NO LEVEL MATCHES must come back as an "
          "UNKNOWN OBJECT, not vanish.")
    print("=" * 110)
    print("The measured defect, reproduced on purpose: platform_datastage.json's "
          "`transformer_stage` level is")
    print("removed in memory, so CustomerSummaryDerive.dsx's CTransformerStage -- the "
          "stage holding every")
    print("derivation in the job -- is a record the table does not cover. Before "
          "ADDITION 2 this document")
    print("reported `declared=4 identified=4 lost=0 balances=True` on 5 elements.")
    print()
    t = load_table("platform_datastage.json")
    t["structure"]["levels"] = [lv for lv in t["structure"]["levels"]
                               if lv["name"] != "transformer_stage"]
    a = measure("ds-no-xfm-level", None, CENSUS_DOC, table=t)
    txt, _ = line(a)
    print(txt)
    print(arithmetic(a))
    hits = [u for u in a["unknown_objects"]
            if u.identity.get("OLEType") == "CTransformerStage"]
    for u in hits:
        print(f"      INVENTORIED: {u.identity}")
        print(f"                   at {u.where}")
    if hits and a["balances"]:
        print("  FIRED: the unrecognised stage is in the inventory with a citable "
              "location, and the")
        print("         ledger still closes over the whole document.")
    else:
        ok = False
        print("  *** DID NOT FIRE: an unrecognised record did not reach the unknown "
              "inventory. ***")

    print()
    print("=" * 110)
    print("FALSIFIABILITY 3 — an exclusion rule that claims an ELEMENT must be "
          "reported, not obeyed.")
    print("=" * 110)
    print("A table can contradict itself: a level says a record IS an element and an "
          "exclusion rule says it")
    print("is not. Identification must win and the contradiction must be reported, "
          "because a rule quietly")
    print("deleting elements is the failure this whole change exists to prevent. A "
          "bogus rule matching the")
    print("`stage` level's own query is injected in memory.")
    print()
    t = load_table("platform_datastage.json")
    t["structure"]["census"]["exclusions"].append({
        "id": "INJECTED-BOGUS-RULE-claims-stages-are-not-elements",
        "kind": "QUERY",
        "match": "./DSJOB/DSRECORD[@OLEType='CCustomStage']",
        "excludes": "(test injection)",
        "why": "(test injection)",
    })
    a = measure("ds-contested-rule", None, CENSUS_DOC, table=t)
    txt, _ = line(a)
    print(txt)
    print(arithmetic(a))
    for c in a["contested"][:5]:
        print(f"      CONTESTED: rule {c['rule']!r} vs level {c['level']!r} at {c['where']}")
    still_identified = a["identified"] == 5
    if a["contested"] and not a["balances"] and still_identified:
        print(f"  FIRED: {len(a['contested'])} contested node(s) reported, `balances` is "
              "False so the gate fails,")
        print("         and all 5 elements are still identified -- the rule was "
              "reported, not obeyed.")
    else:
        ok = False
        print("  *** DID NOT FIRE: a rule contesting an identified element was not "
              "caught. ***")
    return ok


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
