# Platform-table authoring contract

Create `platform_table.json` for the requested platform by reading the source document and the
non-target prior-art tables in this view. You may also write `authoring_notes.md`.

The JSON table is provisional, but it must be executable by the deterministic identification
framework:

- `platform` must exactly equal the requested platform identity in `REQUEST.md`.
- Follow the same top-level and nested data shapes demonstrated by the prior-art tables.
- Describe source vocabulary only in the table. Do not assume changes to framework code.
- Every `structure.levels` entry must identify records through structural queries and stable keys.
- Every record in the projected document must be accounted for as an identified element, a keyless
  level match, a named exclusion, or an inventoried unknown.
- Exclusions must be named, deterministic, and explain why the matched records are not elements.
- Dispatch, role, edge, naming, port, type, expression, and residue policies must be explicit.
- Prefer an honest unsupported or residue outcome over invented semantics.
- Do not copy a prior-art platform identity or claim source behavior not supported by the document.

## Six things the consumers require that the shapes above do not show

Each of these was authored wrong by a table that satisfied every rule above, and each cost a
downstream failure that named a symptom far from its cause. Prior art demonstrates all six, but
only for the platforms that already needed them, so reading shapes alone will not surface them.

**`kind_attr` reads one flat attribute on the element node.** It is `node.get(name)`, so an
attribute one level below the node — Alteryx keeps the tool kind in `GuiSettings/@Plugin` — does
not resolve and every element dispatches as unknown. Hoist a descendant attribute onto the node
with a `LIFT_XML` rule first, then name the lifted attribute in `kind_attr`.

**A connection's endpoints are rarely children of either endpoint.** Every platform here states
its dataflow in a third element that names both sides — an Alteryx `<Connection>` with
`Origin/@ToolID` and `Destination/@ToolID`, a Pentaho `<hop>`, an SSIS `<path>` — so an author
that looks for the downstream reference underneath the upstream element finds nothing and matches
no connection at all. Those endpoint attributes usually sit one level below the connection too, so
they need lifting before `from_field_attr`/`to_field_attr` can read them. A representation with
elements and no edges is refused: nothing downstream can order or wire it, and it is the one
defect whose symptom appears three stages later as a consumer that hydrated nothing.

The declaration path is exact: lifting is a document front-end, so rules belong only at
`structure.document_model.lift_rules`, and `structure.document_model.kind` must be `LIFT_XML`.
Putting `lift_rules` at the table root, at the `structure` root, or inside a level/edge level is
ignored configuration and is rejected even if the canonical list also exists. Rules at
`structure.document_model.lift_rules` are themselves inactive unless `kind` is `LIFT_XML`; a
missing kind, `XML`, or a non-LIFT kind such as `CHILD_TEXT_XML` will not apply them. COPY rules
use `on_tag`, `from_child`, `from_attr`, and `onto_attr` — not `xpath`/`attr`/`as`. This generic
example lifts child endpoint attributes onto the edge element that the framework reads (the names
are illustrative, not platform vocabulary):

```json
{
  "structure": {
    "document_model": {
      "kind": "LIFT_XML",
      "lift_rules": [
        {
          "on_tag": "FlowLink",
          "from_child": "SourceEndpoint",
          "from_attr": "ref",
          "onto_attr": "from_ref"
        },
        {
          "on_tag": "FlowLink",
          "from_child": "TargetEndpoint",
          "from_attr": "ref",
          "onto_attr": "to_ref"
        }
      ]
    },
    "edge_levels": [
      {
        "name": "flow-links",
        "xpath": ".//FlowLink",
        "endpoint_kind": "PORT_REF",
        "from_attr": "from_ref",
        "to_attr": "to_ref",
        "label_attr": null
      }
    ]
  }
}
```

For a source fragment such as
`<FlowLink><SourceEndpoint ref="n1"/><TargetEndpoint ref="n2"/></FlowLink>`, those rules copy
`SourceEndpoint/@ref` and `TargetEndpoint/@ref` onto the in-memory `FlowLink`; they do not rewrite
the source. `from_attr`/`to_attr` (or the field variants required by the chosen endpoint kind) then
name the lifted attributes because edge reads are flat. COPY rules are one child level deep and
use `on_tag`, `from_child`, `from_attr`, and `onto_attr`; the first non-empty rule for an
`onto_attr` wins.

**A transform normalises one reading; it must not merge two.** `UNQUALIFIED_TAIL` exists because
SSIS states a destination as `[dbo].[CUSTOMER_SUMMARY]` and the unqualified tail is the table, so
it splits on `.` and takes the last part. Declared on a value that is not a dotted identifier it
silently means something else: on `\\fileshare\ETL\Orders_Online.csv` the part after the last dot
is the file EXTENSION, and every file element in the document resolves to the relation `csv`. The
models stay individually correct and all read the same table, which is why this surfaces only in
the executor, as columns missing from a relation that three different files were merged into.
Acceptance refuses a transform that maps two distinct readings onto one value; if a field needs
the file name, read the part the document actually states.

**One fact rule per distinct source reading.** The emitter asserts that no two `no_slot_facts`
rules read the same source location, and rejects the whole table when two do. Two rules that
happen to share an XPath are a duplicate reading, not two facts.

**`column_propagation` decides whether a mapped element resolves its upstream at all.** Omit it
and the mode is `NONE`: an element that declares no output columns projects nothing, its
successor's column-driven source lookup returns null, and the emitted model reads
`{{ ref('int_NOT_FOUND') }}` — a dbt1005 at run time, two floors from the empty column list that
caused it. Declare `ACCUMULATE` when an element states only the columns it ADDS to an inbound
buffer, `FILL_WHEN_UNDECLARED` when a declared list is exhaustive and only its absence means
"whatever arrives here". `stop_at_kinds` is for elements that genuinely define a new output shape,
and listing a kind that declares no output shape of its own is worse than omitting it: the walk
stops at an element that states nothing, and every mapped successor is starved of the columns it
needed. An aggregate belongs there. A union that declares no output port site does not.

**The platform identity must match a source-element counting rule.** `coverage_gate.RULES` keys
Gate A's denominator by the identity string, and an identity with no rule leaves coverage
UNMEASURED for the whole run — not failed, not passed, unmeasurable, which is the one outcome this
pipeline treats as worse than a bad number. The keys are `SqlServerIntegrationServices`,
`InformaticaPowerCenter`, `PentahoDataIntegration`, `IbmInfoSphereDataStage` and `alteryx`. They
are not uniformly cased and are not derivable from the platform's name; use the requested identity
in `REQUEST.md` verbatim, and if it is a platform with no rule yet, say so in
`authoring_notes.md` rather than inventing a near miss.

Write JSON only to `platform_table.json`. The caller validates the table, runs deterministic
identification over the source, and builds the representation before accepting it. A
representation that builds is not yet one a consumer can use, so acceptance also asks that the
document's elements be wired to each other and that at least one of them arrive at a kind —
whether a translated kind or an honestly degraded one.

## If your table comes back

The validator reports the FIRST failure it finds, and you may be handed your own table back with
that message and asked to fix it. When that happens the file is unchanged and still in this
directory: repair the specific defect named and rewrite it. Expect to be told about a later
failure next — that is the validator working forward, not your fix being rejected — and do not
restructure anything it has not objected to. If a message names a key or a block this document
did not prepare you for, that is a gap in this document; note it in `authoring_notes.md` so it
stops costing the next author an attempt.
