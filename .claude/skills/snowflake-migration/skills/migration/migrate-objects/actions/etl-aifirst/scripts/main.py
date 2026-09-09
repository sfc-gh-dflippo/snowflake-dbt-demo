"""Driver. Usage: python3 main.py <platform_table.json> <source_document> [out.json]

FRAMEWORK CHANGE 27: the table path was a module constant
(TABLE_PATH = "platform_informatica.json"), the output filename was the literal
"mapping-ir.json", and the identification banner printed "mapping" and
"INSTANCE"/"CONNECTOR" counts using Informatica's words.
"""

import json
import sys

import fit
from emit import Emitter
from identify import Identification, load_table


def main(table_path: str, doc_path: str, out_path: str) -> None:
    table = load_table(table_path)
    idn = Identification(table, doc_path)

    print("=" * 78)
    print("STRUCTURAL IDENTIFICATION")
    print("=" * 78)
    print(f"platform table : {table['table_version']}")
    print(f"document       : {idn.doc_name}")
    # FRAMEWORK CHANGE 39: the banner reported only what was identified. A
    # non-XML front-end can also FAIL to read lines, and that failure was
    # invisible. Anything the projection could not account for is now printed.
    # FRAMEWORK CHANGE 46 (ARCHITECTURAL A7): the report was BUILT here, in
    # DataStage's vocabulary -- sections, reparented records, compound parts,
    # unsectioned subrecords. A Kettle projection has none of those nouns and a
    # JSON projection has facts of its own (empty arrays, unreachable keys), so
    # the driver now prints whatever the front-end reports about itself. The DSX
    # lines are unchanged; they moved to dsxdoc.RecordBlockDocument.report.
    for line in getattr(idn.doc, "report", lambda: [])():
        print(line)
    # FRAMEWORK CHANGE 52 (ADDITION 1): the banner reported what was identified
    # without ever stating what the document DECLARED, so an element lost to a key
    # collision was invisible here and INVISIBLE IN THE FIT SCORE TOO -- the score
    # divides by obligations raised, and a missing element raises none. Printed
    # unconditionally and before the fit number, because a fit percentage without
    # this line beside it cannot be read.
    acc = idn.accounting()
    # FRAMEWORK CHANGE 67 (ADDITION 2): this line used to read `declared: N nodes
    # matched by the level queries`, which is the blind spot itself written out --
    # the denominator WAS the level sweep's own output, so a record no level matched
    # was not reported here at all. `declared` is now every record in the document
    # and the breakdown states where each one went.
    print(f"declared       : {acc['declared']} records in the document "
          f"= {acc['identified']} elements + {acc['lost']} lost + {acc['keyless']} keyless "
          f"+ {acc['excluded']} excluded by table rule + {acc['unknown']} UNKNOWN OBJECTS "
          f"(ledger closes: {acc['balances']})")
    print(f"                 {acc['level_matched']} of those records were matched by a "
          f"level query")
    for rid, n in acc["excluded_by_rule"].items():
        print(f"      excluded : {n:6}  {rid}")
    if acc["unknown"]:
        # An unknown object is INVENTORIED, so it is printed. A count with no
        # inventory beside it is the same shape of claim as a fit score with no
        # ledger beside it.
        print(f"*** {acc['unknown']} UNKNOWN OBJECT(S): records this platform table does "
              f"not recognise. NOT lost -- tracked. ***")
        for u in acc["unknown_objects"][:20]:
            ident = " ".join(f"{k}={v}" for k, v in u.identity.items()) or "(states no "\
                "identifying attribute)"
            print(f"      <{u.tag}> {ident}")
            print(f"        read at {u.where}"
                  + (f"  inside element {u.container}" if u.container else ""))
        if acc["unknown"] > 20:
            print(f"      ... {acc['unknown'] - 20} more")
    for c in acc["contested"]:
        print(f"*** TABLE BUG: exclusion rule {c['rule']!r} claims a node the "
              f"{c['level']!r} level matched, at {c['where']}. Identification wins; the "
              f"rule is reported, not obeyed. ***")
    if acc["lost"]:
        print(f"*** ELEMENTS LOST : {acc['lost']} identified element(s) were SILENTLY "
              f"OVERWRITTEN by a later record with the same key. The fit score below "
              f"does NOT count them and is therefore OVERSTATED. ***")
        for c in acc["collisions"]:
            print(f"      key {c['key']!r} ({c['level']})")
            print(f"        kept {c['kept_where']}")
            print(f"        lost {c['lost_where']}")
    else:
        print(f"elements lost  : 0 (declared == elements + keyless + excluded + unknown, "
              f"ledger balances: {acc['balances']})")
    print(f"elements       : {len(idn.elements) + len(idn.dropped_instances)} identified, "
          f"{len(idn.elements)} emitted "
          f"({len(idn.dropped_instances)} collapsed by table rule)")
    print(f"field lineage  : {len(idn.field_edges)} field-level -> "
          f"{len(idn.element_edges())} element-level edges "
          f"[{table['edge_policy']['element_edges_from']}]")
    # FRAMEWORK CHANGE 62 (d): THE LINK CENSUS, printed for the same reason the
    # declared-versus-identified ledger above it is printed. `0 element-level edges`
    # and `this document has no links` are opposite facts and that line renders them
    # identically -- which is exactly how DataStage shipped a 3-link document as a
    # 0-edge graph. Nothing here is printed unless the table declares pin_pairs, so
    # the four platforms that do not are byte-identical.
    la = idn.link_audit
    if idn.unresolved_edges:
        # ALL-PLATFORM, and printed only when non-zero, so every current run is
        # byte-identical (measured: 0 on all 7). This is the general form of the
        # DataStage lesson -- an edge record whose endpoint did not resolve is a
        # STATED link the graph does not contain, and it used to be discarded in
        # silence on every platform, not just this one.
        print(f"*** {len(idn.unresolved_edges)} EDGE RECORD(S) READ AND NOT EMITTED -- an "
              f"endpoint reference did not resolve to an identified element. ***")
        for r in idn.unresolved_edges:
            print(f"      {r['reason']} at {r['where']}")
    if la and (table["edge_policy"]["pin_pairs"].get("audit") or {}).get("report"):
        print(f"link records   : {la['marker_records']} carry a partner reference "
              f"-> {la['output_half']} read as edges, {la['input_half']} are the peer "
              f"half of one (pair ledger balances: {la['balances']})")
        if la["unclassified"]:
            print(f"*** {len(la['unclassified'])} LINK RECORD(S) OF AN UNDECLARED CLASS. "
                  f"The document pairs these records and edge_policy.pin_pairs lists the "
                  f"class in neither direction, so each one is a link that produced NO edge "
                  f"and the graph below is missing it. ***")
            for r in la["unclassified"]:
                print(f"      class {r['class']!r} partner {r['partner']!r} at {r['where']}")
        if la["unresolved"]:
            print(f"*** {len(la['unresolved'])} LINK RECORD(S) WHOSE ENDPOINTS DID NOT "
                  f"RESOLVE -- read as an edge, emitted as none. ***")
            for r in la["unresolved"]:
                print(f"      class {r['class']!r} partner {r['partner']!r} at {r['where']}")
        if la["fallthrough"]:
            print(f"*** {len(la['fallthrough'])} EDGE ENDPOINT(S) FELL THROUGH TO A "
                  f"CONTAINER. The pin's own declaring record is not an identified element, "
                  f"so the endpoint walk did not stop there -- the edge below asserts a link "
                  f"the document does NOT state. ***")
            for r in la["fallthrough"]:
                print(f"      {r['endpoint']} endpoint of the {r['class']} link at "
                      f"{r['where']} resolved to {r['resolved_to']!r}")
        else:
            print(f"endpoint walks : 0 fell through to a container "
                  f"(every endpoint is the record that DECLARES the pin)")
    print()
    for name, el in idn.elements.items():
        d = idn.dispatch_for(el)
        # FRAMEWORK CHANGE 49 (banner): the banner printed only ir_kind, so a node
        # DEGRADED to an engine class in order to keep its edges alive was
        # indistinguishable from one left out of the graph entirely. Both print
        # None for ir_kind; only one of them still has lineage.
        kind_shown = (f"None->{d['degrade_to']}" if d["ir_kind"] is None
                      and d.get("degrade_to") else str(d["ir_kind"]))
        print(f"  {name:34} {el.kind_raw:26} role={el.role:14} "
              f"$kind={kind_shown:26} ports={len(el.ports):2} "
              f"groups={len(el.groups)} level={el.level}"
              + (f" absorbs={el.absorbed}" if el.absorbed else "")
              + (f" in={el.container}" if el.container else "")
              + (f" valueless_keys={len(el.valueless_attrs)}"
                 if el.valueless_attrs else ""))
        print(f"    at {el.where}")
    print()
    for e in idn.element_edges():
        pairs = ", ".join(f"{f.from_field}->{f.to_field}" for f in e["field_edges"])
        print(f"  {e['from']:34} -> {e['to']:34} label={str(e['label']):22} [{pairs}]")

    em = Emitter(idn)
    ir = em.emit()

    print()
    print("=" * 78)
    print("EMITTED PRODUCER IR")
    print("=" * 78)
    out = json.dumps(ir, indent=2)
    print(out)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(out + "\n")

    print()
    print(fit.report(fit.score(em.slots)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],
         sys.argv[3] if len(sys.argv) > 3 else "element-ir.json")
