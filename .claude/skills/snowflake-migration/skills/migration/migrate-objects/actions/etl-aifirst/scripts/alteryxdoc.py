"""Child-attribute-lift XML front-end: projects an Alteryx `.yxmd` into a
queryable tree.

A `.yxmd` IS plain XML with REAL attributes everywhere -- unlike a Kettle
`.ktr` (zero attributes, see ktrdoc.py), Alteryx states almost every fact as
an attribute. So why does this platform need a front-end at all, rather than
the plain `XmlDocument` SSIS and Informatica already use?

THE GAP. `identify.py`'s two dispatch reads are both FLAT, single-node
`node.get(attr)` calls:
  * `_identify_elements`: `kind = node.get(level["kind_attr"], "")`, called on
    whatever node the level's OWN `elements` xpath matched.
  * `_identify_edges` (PORT_REF branch): `c.get(lv["from_attr"])` /
    `c.get(lv["to_attr"])`, called on whatever node the edge level's `xpath`
    matched.
Neither supports a nested path. That is fine for SSIS, where a component
states its OWN `componentClassID` and a `<path>` states its OWN `startId`/
`endId`. It is NOT fine for Alteryx, where the two facts this framework's
dispatch needs are always one level below the node that carries the key:

    <Node ToolID="5">
      <GuiSettings Plugin="AlteryxBasePluginsGui.Filter.Filter">...
      <EngineSettings EngineDll="..." EngineDllEntryPoint="AlteryxFilter" />

  MEASURED (3 real/realistic .yxmd files): `<Node>` carries ONLY `ToolID`.
  Every tool's identity lives on a CHILD -- `GuiSettings/@Plugin` for a
  built-in tool, `EngineSettings/@Macro` for a macro/custom-tool invocation
  (world_data_prep.yxmd ToolID 16: `<GuiSettings>` has NO `Plugin` attribute
  at all, only `<EngineSettings Macro="Cleanse.yxmc" />`).

  Likewise `<Connection>` carries no attribute of its own naming either
  endpoint -- `<Origin ToolID="5" Connection="True"/>` and
  `<Destination ToolID="14" Connection="Input"/>` are children, and the
  anchor name that makes an edge meaningful (True/False, Left/Right/Join,
  Unique, ...) is stated once on each side, never on `<Connection>` itself.

ONE projection rule, table-driven rather than hardcoded, because both gaps
are the same shape: "the node the framework's flat read lands on is not the
node the value is stated on."

PROJECTION RULE -- CHILD ATTRIBUTE LIFT.
    `structure.document_model.lift_rules` names, per platform TABLE (this
    module contains no Alteryx vocabulary -- no "GuiSettings", no "ToolID"
    string literal), which child's attribute to copy onto the parent as a new
    attribute. Two shapes:
      COPY   -- one child/attribute pair, optionally prefixed (used to keep
                a macro's `EngineSettings/@Macro` distinguishable from a
                built-in tool's `GuiSettings/@Plugin` while still landing in
                the ONE attribute name `kind_attr` can name).
      CONCAT -- several child/attribute pairs joined with a separator (used
                for `Connection`'s two independent anchor names, because
                which side is the informative one varies by tool: a Filter's
                signal is on `Origin` (True/False), a Join's is on
                `Destination` (Left/Right), and a single "pick one side"
                rule would silently drop the other).
    A rule with `on_tag` requires the parent to have that tag, and the FIRST
    rule (in table order) to produce a non-empty value for a given
    `onto_attr` wins -- the same "first rule wins" convention `_census` and
    `edge_policy.pin_pairs` already use elsewhere in this project.

    The lift is ONE LEVEL ONLY, matching ktrdoc.py's rule: `<Node>` and a
    macro's own `<Properties><Configuration>` both nest children, and a
    recursive lift would risk lifting an unrelated descendant attribute of
    the same name.

    Lifted children are NOT removed, for the same reason as ktrdoc.py:
    removing them would make `attr_ref`'s citation point at a node the tree
    no longer contains.

ARCHITECTURAL CHANGE A6 (citation). `attr_ref(node, "Plugin")` cannot answer
"/@Plugin" -- that is not where the source states it. Every lifted attribute
is recorded in `_synth` with its real address (`/GuiSettings/@Plugin`,
`/EngineSettings/@Macro`, or, for a CONCAT, both addresses joined) at lift
time, and `attr_ref` consults it before falling back to the XmlDocument
default. Every attribute this front-end did NOT lift (ToolID, Connection's
own `name="#1"`, everything under `<Properties>`) is real, so the fallback
covers the overwhelming majority of reads unchanged.

ARCHITECTURAL CHANGE A9 (source fidelity). `ET.tostring(node)` on a node this
module lifted onto would serialise an attribute the source file does not
contain -- exactly the fabrication ktrdoc.py's A9 override exists to avoid,
for the same reason. Rather than switch to expat + raw-byte slicing (which
would also buy line numbers this platform does not otherwise need),
`source_text` pops every fabricated attribute from the subtree, serialises,
and restores them -- cheaper than a parallel parse, and the restore is
unconditional (`finally`) so a failure mid-serialisation cannot leave the
live tree missing an attribute the rest of the run still depends on.

`loc_prefix` returns "", same as `XmlDocument` and for the same stated
reason: ElementTree discards line numbers, and citing none is honest where
citing a wrong one would not be.
"""

import xml.etree.ElementTree as ET


class LiftXmlDocument:
    """Front-end satisfying the contract in docmodel.py."""

    kind = "LIFT_XML"

    def __init__(self, path: str, cfg: dict):
        self.path = path
        self.cfg = cfg
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self._fabricated: dict[int, set] = {}       # id(node) -> {onto_attr, ...}
        self._synth: dict[tuple, str] = {}           # (id(node), onto_attr) -> citation
        self.applied: dict[str, int] = {}             # onto_attr -> count
        self.rules_with_no_match: list[str] = []
        self._lift(cfg.get("lift_rules", []))

    # -- projection ----------------------------------------------------------

    def _lift(self, rules: list[dict]) -> None:
        fired = [False] * len(rules)
        for node in self.root.iter():
            for i, rule in enumerate(rules):
                if node.tag != rule.get("on_tag"):
                    continue
                onto = rule["onto_attr"]
                if node.get(onto):
                    continue                          # an earlier rule already won
                if "concat" in rule:
                    values, cites, any_real = [], [], False
                    for part in rule["concat"]:
                        ch = node.find(part["from_child"])
                        v = ch.get(part["from_attr"]) if ch is not None else None
                        values.append(v or "")
                        cites.append(f"/{part['from_child']}/@{part['from_attr']}")
                        any_real = any_real or bool(v)
                    if not any_real:
                        continue
                    value = rule.get("separator", "->").join(values)
                    citation = " + ".join(cites)
                else:
                    ch = node.find(rule["from_child"])
                    if ch is None:
                        continue
                    v = ch.get(rule["from_attr"])
                    if not v:
                        continue
                    value = rule.get("value_prefix", "") + v
                    citation = f"/{rule['from_child']}/@{rule['from_attr']}"
                node.set(onto, value)
                self._fabricated.setdefault(id(node), set()).add(onto)
                self._synth[(id(node), onto)] = citation
                self.applied[onto] = self.applied.get(onto, 0) + 1
                fired[i] = True
        for i, r in enumerate(rules):
            if not fired[i]:
                self.rules_with_no_match.append(
                    f"{r.get('onto_attr')}<-{r.get('on_tag')}"
                    f"/{r.get('from_child', '(concat)')}")

    # -- location oracle -------------------------------------------------------

    def loc_prefix(self, node) -> str:
        return ""

    def attr_ref(self, node, attr: str) -> str:
        """ARCHITECTURAL CHANGE A6: a lifted attribute cites the child it was
        copied from; every other attribute is real, so the citation is the
        plain XML one, byte-identical to XmlDocument."""
        c = self._synth.get((id(node), attr))
        return c if c is not None else "/@" + attr

    def source_text(self, node) -> str:
        """ARCHITECTURAL CHANGE A9: strip fabricated attributes, serialise,
        restore -- see module docstring."""
        saved = []
        for n in node.iter():
            fab = self._fabricated.get(id(n))
            if not fab:
                continue
            for attr in fab:
                if attr in n.attrib:
                    saved.append((n, attr, n.attrib.pop(attr)))
        try:
            return ET.tostring(node, encoding="unicode")
        finally:
            for n, attr, val in saved:
                n.set(attr, val)

    def report(self) -> list[str]:
        out = [
            f"front-end      : {self.kind}  (XML parsed by ElementTree; "
            f"child-attribute lift for tool/edge identity)",
            f"projection     : " + ", ".join(
                f"{v} x {k}" for k, v in sorted(self.applied.items())) +
            " lifted from a child element onto its parent",
        ]
        if self.rules_with_no_match:
            out.append("unaccounted    : lift rules that never fired: "
                        + ", ".join(self.rules_with_no_match))
        return out
