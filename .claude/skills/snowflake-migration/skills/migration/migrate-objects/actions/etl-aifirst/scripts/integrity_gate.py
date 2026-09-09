#!/usr/bin/env python3
"""STRUCTURAL INTEGRITY — did the IR reach the dbt?

WHY THIS EXISTS. The owner named three kinds of gap it is GOOD for this project to detect, and the
third is that the generated models "lack structural integrity -- we lost information either in the
IR or in the dbt". Both halves had a gate for the FIRST clause and neither had one for the second:

  stage 1 loss ledger  did the DOCUMENT's records reach the identification sweep?
  Gate A (3d, 3e)      did the DOCUMENT reach the IR?
  Gate B (3e2)         does the generated SQL DO what the document says?
  ---------------------------------------------------------------------------------
  THIS GATE            did the IR reach the DBT?

Nothing asked the last question. A node the hydrator accepted, a column the IR carries, an edge the
graph resolved and a payload value a translator was handed can each vanish between `ir.json` and the
emitted `.sql` files, and every gate above would still report exactly what it reports today. Gate A
reads the document and the IR and never opens a model; Gate B reads models and the document and never
opens the IR; stage 4 counts markers in the tree and never compares it to anything.

DETERMINISTIC, DELIBERATELY. Both existing judgement gates are model calls, which makes them
expensive, unreproducible run to run (findings/53: the same bundle, five verifier calls, four
disagreements), and impossible to put in front of every migration. This gate is code. It costs
nothing, it runs on every migration, its answers are identical on identical inputs, and it can
therefore be negative-tested by planting the loss and watching it fire.

IT NEVER READS THE SOURCE DOCUMENT, AND THAT INDEPENDENCE IS THE MECHANISM. Every gate upstream of
this one has the document as an input, so every one of them is exposed to the same question -- "what
does a rule say is in this file" -- and to the same failure, a record no rule reads. This gate's two
inputs are the IR and the tree. Whatever the sweep did or did not read, whatever the model did or did
not judge, the IR is a fact on disk and so is the tree, and this gate compares the two.

WHAT IT IS NOT. It is NOT a count of artifacts. `models == nodes` is the shape of check that passes
while accomplishing nothing: three nodes emitting three models with the wrong three names scores a
perfect 3/3. Every class below compares NAMED things -- this node's model, this column's projection,
this edge's ref(), this predicate's text -- and itemises the ones it could not find.

THE SIX CLASSES, and what a real loss looks like in each:

  NODES     an IR node with no model and no dbt project directory. Also the reverse: a model no IR
            node accounts for, which is output nothing in the representation asked for.
  COLUMNS   an `OutputColumns` entry whose name never appears in the model that should project it.
            Split three ways, because "the name is there" and "the value is there" are different
            facts: PROJECTED, NAME_ONLY (`null AS FullName` -- the name survived and the value did
            not) and ABSENT.
  EDGES     an IR edge with no `ref()` (or `source()`) naming the upstream artifact from the
            downstream one. Both models exist, the edge between them does not, and the result is a
            disconnected DAG branch that compiles clean -- no parser reports a reference that is
            merely ABSENT.
  PAYLOAD   a value the IR carries for an element that does not appear in its SQL. The worked case
            is `FilterTransformation.FilterConditions`: the engine's `FilterTranslator` substitutes
            `WHERE TRUE` for an empty predicate, which silently returns every row while looking
            exactly like a filter. `TargetTransformation.TableName` is the second.
  SYNTAX    a model file that is not even well-formed SQL, independent of what the IR asked for.
            Unbalanced parentheses, a dangling trailing keyword or comma, or a `SELECT ... FROM`
            pair with nothing between them. Unlike the other four, this class reads NO IR at all --
            it is a precondition check, not a comparison, which is why it is cheap enough to run on
            every model regardless of whether the IR reached it. MEASURED, on a real M1 run
            (loaddim-ai-authored-2026-08-17): the engine's own `UnsupportedTransformationTranslator`
            fallback -- the shared "wrap the failing element in an EWI comment and still emit
            something" template used across every platform -- prints a bare `SELECT` with no
            columns and no FROM when it substitutes a fresh `UnsupportedTransformation` object whose
            `OutputColumns` came back empty and whose FROM lookup matches DAG edges by
            `ReferenceEquals` against an object no edge points to. Two ephemeral models shaped that
            way (`int_m_71.sql`, `int_m_36.sql`) get inlined into their downstream marts at compile
            time, so `dbt compile`/Snowflake failed on two marts that were themselves fine. This
            class is a cheap, deterministic tripwire for exactly that shape, independent of the
            engine-internal root cause (which is out of THIS gate's scope -- see the class's own
            docstring for where that root cause actually lives).
  SCAFFOLD  a framework file emitted into this tree whose NAME belongs to another platform. Like
            SYNTAX this class reads no IR; unlike every other class its denominator is files that
            exist rather than obligations the IR raised, so a raised count of 0 means "this run
            emitted no scaffolding at all" and is a real clean state, not an empty denominator.
            MEASURED (runs/m1-ready-2026-08-19): an Alteryx migration shipped
            `etl_instrumentation/configuration/procedures/ssis_read_baseline_data.sql` and three
            siblings, because the producer called the engine's SSIS-specific configuration writer
            unconditionally. The producer now gates that call, and this class is the tripwire that
            fails if it ever regresses -- gate B cannot be that tripwire, because it EXCLUDES these
            directories from what the verifier sees, by design and for a good reason.

WHAT IS DELIBERATELY OUT OF SCOPE, stated rather than left to be discovered:

  * `ColumnExpression.Expression` is NOT matched literally. SSIS `FirstName + " " + MiddleName`
    correctly becomes `FirstName || ' ' || MiddleName`; a literal-match rule would fire on every
    correctly lowered expression in the tree, which is a gate that cries wolf. Whether the lowering
    PRESERVES MEANING is Gate B's question and needs a reader. What this gate can say without any
    dialect knowledge is whether the expression was ERASED -- projected as a bare `null` -- and that
    is the COLUMNS class's NAME_ONLY state.
  * Behavioural parity. Out of scope by owner decision (PHASES phase 18).

THE LEDGER BALANCES, AND THE BALANCE IS A CHECKED, PRINTED ASSERTION. For every class,
`raised == discharged + outstanding + unmeasurable`. `unmeasurable` exists to keep the accounting
honest in one specific way: a column obligation whose model does not exist is not evidence about the
dbt's columns, it is the NODES class's finding seen a second time, and counting it as a column loss
would report one defect twice. If any class fails to balance the gate prints a DEFECT banner and
does NOT print its verdict line, so the driver reports it UNMEASURED rather than clean.

EXIT CODES
  0  every obligation discharged
  3  information lost between the IR and the dbt -- outstanding obligations, itemised
  1  could not run (no IR, unparseable IR, no tree, or a ledger that does not balance)
  2  usage
"""

import json
import os
import re
import sys

PRUNE = ("dbt_internal_packages", "target")


# ==================================================================================================
# READING THE ARTIFACT
# ==================================================================================================

def find_models(out_root):
    """Every model the emitter actually wrote.

    Same prune set, and for the same measured reason, as the driver's: `dbt_internal_packages`
    carries a `models` directory of ADAPTER MACROS and `target/compiled` carries dbt's own copies of
    our models. Counting either inflates every class in this gate with files no IR node produced --
    and worse, `target/compiled` would let a model discharge its own obligations twice.
    """
    found = []
    for dirpath, dirnames, filenames in os.walk(out_root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE]
        if "models" not in dirpath.split(os.sep):
            continue
        for f in filenames:
            if f.endswith(".sql"):
                found.append(os.path.join(dirpath, f))
    return sorted(found)


def find_projects(out_root):
    """Every directory carrying a `dbt_project.yml`.

    NEEDED BY THE NODES CLASS AND NOT OPTIONAL. A container node -- an SSIS Data Flow Task, a
    DataStage DSJOB, a Pentaho transformation -- is lawfully realised as the dbt PROJECT the models
    live in, not as a model. A gate that only looked for models would report the container node as
    lost on every platform, on every run, which is a false alarm the owner would have to learn to
    ignore. So the container realisation is a NAMED discharge state with the directory printed as
    its evidence, not a silent exclusion.
    """
    found = []
    for dirpath, dirnames, filenames in os.walk(out_root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE]
        if "dbt_project.yml" in filenames:
            found.append(dirpath)
    return sorted(found)


def strip_sql_comments(sql):
    """Remove `--` line comments and `/* */` block comments, preserving string and quoted-identifier
    literals.

    THIS IS LOAD-BEARING AND IT IS THE FIRST THING A LAZY VERSION OF THIS GATE GETS WRONG. The
    DataStage tree's degraded model for `Xfm_DeriveNameYear` carries the ENTIRE DSX record commented
    out, including `Name "FullName"` and `Derivation "...FirstName : \\" \\" : ..."`. A column check
    that greps the raw file finds `FullName` in that comment and discharges the obligation on
    evidence that is, in SQL terms, whitespace. Same for the payload class: the engine's own EWI
    comment often quotes the value the model then fails to use.

    Line comments are replaced by a newline and block comments by a space so that token boundaries
    survive -- `A--x\\nB` must not become `AB`.
    """
    out = []
    i, n = 0, len(sql)
    while i < n:
        c = sql[i]
        # `--` and `/*` are tested BEFORE the quote cases in the sense that matters: the scanner is
        # positional, so on a line that STARTS a comment the comment wins, and a quote inside that
        # comment is never entered. That ordering is what keeps an unbalanced `"` inside a commented
        # DSX record from swallowing the rest of the file.
        if c == "-" and i + 1 < n and sql[i + 1] == "-":
            while i < n and sql[i] != "\n":
                i += 1
            out.append("\n")
            continue
        if c == "/" and i + 1 < n and sql[i + 1] == "*":
            i += 2
            while i + 1 < n and not (sql[i] == "*" and sql[i + 1] == "/"):
                i += 1
            i = min(i + 2, n)
            out.append(" ")
            continue
        if c == "'":
            out.append(c)
            i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":   # doubled quote: an escaped '
                        out.append("''")
                        i += 2
                        continue
                    out.append("'")
                    i += 1
                    break
                out.append(sql[i])
                i += 1
            continue
        if c == '"':
            out.append(c)
            i += 1
            while i < n:
                out.append(sql[i])
                if sql[i] == '"':
                    i += 1
                    break
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


_SQ = re.compile(r"'(?:''|[^'])*'")


def blank_string_literals(sql):
    """Replace the CONTENTS of single-quoted literals with spaces, keeping the quotes.

    TWO MATCHING SURFACES, EACH JUSTIFIED, RATHER THAN ONE THAT IS WRONG FOR HALF THE CLASSES:

      code  comments stripped AND string contents blanked. Used by the COLUMNS class. A column name
            that appears ONLY inside a string literal is not a projection of that column, and
            counting it would be a bias toward discharge -- which is the direction that makes a gate
            worthless.
      text  comments stripped, string contents KEPT. Used by the PAYLOAD class, because that is
            where the values legitimately live: `{{ source('raw', 'CUSTOMER') }}` and
            `config(alias='CUSTOMER_SUMMARY')` are how a `TableName` reaches the artifact at all.
    """
    return _SQ.sub(lambda m: "'" + " " * (len(m.group(0)) - 2) + "'", sql)


_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*")
_REF = re.compile(r"\bref\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
_SOURCE = re.compile(r"\bsource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)")


class Model:
    """One emitted model file, with every surface this gate reads precomputed once."""

    def __init__(self, path, out_root):
        self.path = path
        self.rel = os.path.relpath(path, out_root)
        self.stem = os.path.splitext(os.path.basename(path))[0]
        try:
            raw = open(path, "r", encoding="utf-8", errors="replace").read()
        except OSError:
            raw = ""
        self.raw = raw
        self.text = strip_sql_comments(raw)          # comments gone, string contents kept
        self.code = blank_string_literals(self.text)  # ... and string contents blanked
        self.tokens = {t.casefold() for t in _IDENT.findall(self.code)}
        self.text_tokens = {t.casefold() for t in _IDENT.findall(self.text)}
        # refs/sources read from `text`, not from `raw`: a commented-out ref() is not an edge.
        self.refs = {r.casefold() for r in _REF.findall(self.text)}
        self.sources = {(a.casefold(), b.casefold()) for a, b in _SOURCE.findall(self.text)}
        self.flat = re.sub(r"\s+", " ", self.code).casefold()
        self.tight = re.sub(r"\s+", "", self.code).casefold()

    def erases(self, column):
        """True when the model projects `column` as a bare NULL literal.

        `null AS FullName` is the exact shape of a translator that kept the SHAPE of the projection
        and threw away its CONTENT, and it is what the engine emits for every column of a component
        it could not convert. The name is present, so a name-presence check discharges it; nothing
        about the source element survived. Reported as its own state (NAME_ONLY) so that the two
        facts stay separate.

        THE ONE WAY THIS COULD OVER-FIRE, stated rather than discovered later: a model that
        legitimately projects a constant NULL for a column the source really does leave empty would
        be reported here. No such column exists in any measured tree, and the itemisation prints the
        matching line so a reviewer can see the evidence rather than trust the count.
        """
        pat = re.compile(r"\bnull\s+as\s+\"?" + re.escape(column) + r"\"?\b", re.I)
        return bool(pat.search(self.code))


# ==================================================================================================
# READING THE REPRESENTATION
# ==================================================================================================

def norm(s):
    return (s or "").strip().casefold()


def node_keys(node):
    """Every string by which an edge endpoint could legitimately name this node.

    Same key set as `coverage_gate.ir_keys` and `issues/detect._node_keys`, deliberately: three
    readers of the same IR that disagreed about what names a node would be three gates measuring
    three different graphs.
    """
    keys = set()
    nid = node.get("id") or ""
    keys.add(norm(nid))
    for sep in ("\\", "/"):
        if sep in nid:
            keys.add(norm(nid.rsplit(sep, 1)[-1]))
    el = node.get("element") or {}
    keys.add(norm(el.get("Name")))
    keys.discard("")
    return keys


def models_for(model_name, models):
    """A model belongs to a node when its stem is the node's `modelName`, optionally behind a
    `<prefix>_` the emitter added (`stg_raw__`, `int_`, ...).

    Matched by suffix with a `_` boundary rather than against an enumerated prefix list, because the
    prefix set is the emitter's business and this gate must not encode it -- an emitter that adds a
    layer would otherwise turn every model in that layer into a false loss. AMBIGUITY IS RETURNED,
    never resolved: two nodes claiming one model is a fact about the emitter's naming and the gate
    reports it instead of picking one.

    THE PRICE OF THAT CHOICE, STATED BECAUSE IT IS REAL AND TESTED IN BOTH DIRECTIONS: ANY prefix is
    accepted, so a model renamed `zz_int_fil_names` still discharges the node whose modelName is
    `fil_names`. The suffix is what carries the identity. A rename that changes the TAIL is caught
    (`int_fil_names_zz` matches nothing) and a rename that only adds a HEAD is not. Encoding the
    emitter's real prefix list would close that at the cost of a false loss every time the emitter
    adds a layer, which is the worse failure for a gate whose value is that nobody learns to ignore
    it.
    """
    if not model_name:
        return []
    mn = norm(model_name)
    return [m for m in models
            if m.stem.casefold() == mn
            or (m.stem.casefold().endswith(mn) and m.stem.casefold()[: -len(mn)].endswith("_"))]


def projects_for(node, projects):
    """The dbt project directory a container node is realised as, if any."""
    keys = node_keys(node)
    keys.add(norm((node.get("modelName") or "")))
    keys.discard("")
    return [p for p in projects if norm(os.path.basename(p)) in keys]


# ==================================================================================================
# THE LEDGER
# ==================================================================================================

class Ledger:
    """One class of obligation, accounted so that it balances.

    `raised == discharged + outstanding + unmeasurable`, asserted and printed. The three-way split
    is the whole point: this project has twice shipped a gate whose denominator was its own output,
    and a two-way pass/fail split invites exactly that -- everything it cannot check quietly becomes
    a pass.
    """

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.discharged = []     # (subject, how, evidence)
        self.outstanding = []    # (subject, why, evidence)
        self.unmeasurable = []   # (subject, why, evidence)

    def ok(self, subject, how, evidence=""):
        self.discharged.append((subject, how, evidence))

    def lost(self, subject, why, evidence=""):
        self.outstanding.append((subject, why, evidence))

    def skip(self, subject, why, evidence=""):
        self.unmeasurable.append((subject, why, evidence))

    @property
    def raised(self):
        return len(self.discharged) + len(self.outstanding) + len(self.unmeasurable)

    def balances(self):
        return self.raised == len(self.discharged) + len(self.outstanding) + len(self.unmeasurable)

    def as_dict(self):
        return {
            "class": self.name,
            "unit": self.unit,
            "raised": self.raised,
            "discharged": len(self.discharged),
            "outstanding": len(self.outstanding),
            "unmeasurable": len(self.unmeasurable),
            "balances": self.balances(),
            "discharged_items": [{"subject": s, "how": h, "evidence": e}
                                 for s, h, e in self.discharged],
            "outstanding_items": [{"subject": s, "why": w, "evidence": e}
                                  for s, w, e in self.outstanding],
            "unmeasurable_items": [{"subject": s, "why": w, "evidence": e}
                                   for s, w, e in self.unmeasurable],
        }


# ==================================================================================================
# CLASS 1 — NODES.  Is there an artifact for every IR node, and is every model traceable to a node?
# ==================================================================================================

def check_nodes(ir, models, projects, out_root):
    """Both directions, because they are different questions with different failure modes.

    IR -> dbt   a node with no artifact is a source element that reached the representation and then
                vanished. Discharged as MODEL, or as CONTAINER when the node is realised as the dbt
                project the models live in.
    dbt -> IR   a model no node accounts for is output the representation never asked for. It is the
                rarer direction and the one nobody checks; a hardcoded or leftover model file passes
                every gate in this driver today.
    """
    fwd = Ledger("NODES", "IR node -> dbt artifact")
    rev = Ledger("MODELS", "dbt model -> IR node")
    realisation = {}     # node id -> ("MODEL", Model) | ("CONTAINER", path) | ("NONE", None)
    claimed = {}         # model rel -> [node id, ...]

    for node in ir.get("nodes") or []:
        nid = node.get("id") or ""
        el = node.get("element") or {}
        subject = "%s  [%s]" % (nid, el.get("$kind") or el.get("_unsupported") or "no kind")
        hits = models_for(node.get("modelName"), models)
        if len(hits) > 1:
            # NEVER RESOLVED SILENTLY. Two models answering to one node's modelName means the gate
            # cannot say which one carries the columns, so the node's own obligation is discharged
            # (an artifact exists) and the ambiguity is stated in the evidence.
            fwd.ok(subject, "MODEL (AMBIGUOUS)",
                   "%d models match modelName %r: %s"
                   % (len(hits), node.get("modelName"), ", ".join(m.rel for m in hits)))
            realisation[nid] = ("MODEL", hits[0])
            for m in hits:
                claimed.setdefault(m.rel, []).append(nid)
            continue
        if hits:
            fwd.ok(subject, "MODEL", hits[0].rel)
            realisation[nid] = ("MODEL", hits[0])
            claimed.setdefault(hits[0].rel, []).append(nid)
            continue
        projs = projects_for(node, projects)
        if projs:
            fwd.ok(subject, "CONTAINER",
                   "dbt project %s" % os.path.relpath(projs[0], out_root))
            realisation[nid] = ("CONTAINER", projs[0])
            continue
        fwd.lost(subject, "NO ARTIFACT",
                 "no model whose stem is or ends in %r, and no dbt project directory named for it"
                 % (node.get("modelName") or "",))
        realisation[nid] = ("NONE", None)

    for m in models:
        if m.rel in claimed:
            rev.ok(m.rel, "IR NODE", ", ".join(claimed[m.rel]))
        else:
            rev.lost(m.rel, "NO IR NODE",
                     "stem %r is not, and does not end in `_`+, any node's modelName" % m.stem)
    return fwd, rev, realisation


# ==================================================================================================
# CLASS 2 — COLUMNS.  Does every OutputColumns entry appear in the model that should project it?
# ==================================================================================================

def check_columns(ir, realisation):
    """CASE-INSENSITIVE, AND THAT IS NOT A DETAIL.

    The driver's own column-less-model check was case-SENSITIVE, required `SELECT` uppercase and
    alone on a line, and therefore counted a correct six-column model as column-less the day the
    sidecars became model-produced -- because every engine translator emits uppercase and a model
    writes lowercase. The same trap, pointed the other way, would make this gate report a real loss
    on any model-authored SQL. Every comparison here is casefolded on both sides.

    THREE STATES, NOT TWO. `null AS FullName` has the name and not the value, so calling it
    discharged would report information loss as integrity. It is counted as outstanding under
    NAME_ONLY, distinguished from ABSENT, because the two need different fixes: ABSENT means the
    projection never mentioned the column, NAME_ONLY means a translator kept the shape and dropped
    the content.
    """
    led = Ledger("COLUMNS", "IR OutputColumns entry -> projection in its model")
    empty_nodes = []
    for node in ir.get("nodes") or []:
        nid = node.get("id") or ""
        el = node.get("element") or {}
        cols = [c for c in (el.get("OutputColumns") or []) if (c or {}).get("Name")]
        kind, art = realisation.get(nid, ("NONE", None))
        if not cols:
            # PRINTED, NOT SILENT. "0 columns lost of 0 carried" and "0 of 6" are opposite facts and
            # only the second is evidence. A node the IR carries no columns for is a hole this gate
            # structurally cannot see into, and the count of such nodes goes in the report.
            empty_nodes.append("%s  [%s]" % (nid, el.get("$kind") or el.get("_unsupported")
                                             or "no kind"))
            continue
        for c in cols:
            name = str(c["Name"])
            subject = "%s . %s" % (nid, name)
            if kind != "MODEL":
                led.skip(subject,
                         "NO MODEL FOR THIS NODE",
                         "the node is realised as %s; the NODES class already carries this"
                         % ("a dbt project directory" if kind == "CONTAINER" else "nothing"))
                continue
            if name.casefold() not in art.tokens:
                led.lost(subject, "ABSENT",
                         "%s names no identifier %r outside comments and string literals"
                         % (art.rel, name))
            elif art.erases(name):
                led.lost(subject, "NAME_ONLY",
                         "%s projects it as a bare NULL literal (`null AS %s`): the name survived "
                         "and the value did not" % (art.rel, name))
            else:
                led.ok(subject, "PROJECTED", art.rel)
    return led, empty_nodes


# ==================================================================================================
# CLASS 3 — EDGES.  Does every IR edge appear as a ref() (or source()) in the downstream model?
# ==================================================================================================

def check_edges(ir, realisation):
    """A RESOLVED EDGE THAT BECOMES NO ref() IS A DISCONNECTED DAG BRANCH, AND IT COMPILES CLEAN.

    That is why this class exists and why it is not covered by the compile check in stage 4. A
    DANGLING reference fails loudly -- `dbt1005: Ref not found` -- and the driver already counts it.
    A reference that is merely ABSENT parses, compiles, runs, and quietly drops the upstream element
    out of the graph. Nothing in dbt will ever report it, because from dbt's point of view there was
    never an edge to lose.

    `source()` IS ACCEPTED AS AN ALTERNATIVE REALISATION, NARROWLY. An emitter may read a source
    element's table directly in the downstream model instead of going through a staging model. That
    is a real realisation of the edge, so it discharges -- but only when the upstream node is
    `type: source` and carries the `TableName` the downstream model names, and it is counted
    separately so the number is visible rather than folded into `discharged`.
    """
    led = Ledger("EDGES", "IR edge -> reference in the downstream artifact")
    keymap = {}
    for node in ir.get("nodes") or []:
        for k in node_keys(node):
            keymap[k] = node.get("id")
    by_id = {n.get("id"): n for n in (ir.get("nodes") or [])}
    via_source = 0

    for e in ir.get("edges") or []:
        frm, to = str(e.get("from")), str(e.get("to"))
        label = e.get("label")
        subject = "%s -> %s%s" % (frm, to, ("  [%s]" % label) if label else "")
        src_id = to_id = None
        if frm in by_id:
            src_id = frm
        else:
            src_id = keymap.get(norm(frm))
        if to in by_id:
            to_id = to
        else:
            to_id = keymap.get(norm(to))
        if not src_id or not to_id:
            led.skip(subject, "ENDPOINT NAMES NO NODE",
                     "%s does not resolve to any IR node, so the edge has no artifact to look for"
                     % ("from" if not src_id else "to"))
            continue
        skind, sart = realisation.get(src_id, ("NONE", None))
        dkind, dart = realisation.get(to_id, ("NONE", None))
        if skind == "NONE" or dkind == "NONE":
            led.skip(subject, "ENDPOINT HAS NO ARTIFACT",
                     "the %s node is already outstanding in the NODES class; counting it here "
                     "would report one loss twice" % ("upstream" if skind == "NONE" else
                                                     "downstream"))
            continue
        if dkind == "CONTAINER":
            led.lost(subject, "DOWNSTREAM IS A CONTAINER",
                     "the downstream node is realised as a dbt project directory, which carries no "
                     "ref(); no artifact in this tree states this edge")
            continue
        if skind == "CONTAINER":
            led.lost(subject, "UPSTREAM IS A CONTAINER",
                     "%s can hold no ref() naming a dbt project directory; the edge is absent from "
                     "the artifact" % dart.rel)
            continue
        if sart.stem.casefold() in dart.refs:
            led.ok(subject, "REF", "%s references ref('%s')" % (dart.rel, sart.stem))
            continue
        selem = (by_id.get(src_id) or {}).get("element") or {}
        tbl = selem.get("TableName")
        if (by_id.get(src_id) or {}).get("type") == "source" and tbl and \
                any(rel == str(tbl).casefold() for _, rel in dart.sources):
            via_source += 1
            led.ok(subject, "SOURCE",
                   "%s reads source(..., '%s') directly, so the edge is realised without a ref()"
                   % (dart.rel, tbl))
            continue
        led.lost(subject, "NO REFERENCE",
                 "%s references %s, which does not include %r. Both artifacts exist and the edge "
                 "between them does not."
                 % (dart.rel, sorted(dart.refs) or "nothing", sart.stem))
    return led, via_source


# ==================================================================================================
# CLASS 4 — PAYLOAD.  Does a value the IR carries for an element appear in its SQL?
# ==================================================================================================

# The fields whose VALUE must survive into the SQL verbatim (modulo whitespace and case), with the
# surface each is read on. DELIBERATELY A SHORT, EXPLICIT LIST rather than "every string field":
# `Expression` is on this element too and must NOT be here (a lawful dialect rewrite would fire it),
# and a list that grows by reflection would acquire it the first time the IR changed shape.
PAYLOAD_FIELDS = (
    # (field, surface, why this field's value must appear literally)
    ("FilterConditions", "text",
     "the predicate decides WHICH ROWS reach the output. FilterTranslator substitutes `WHERE TRUE` "
     "for an empty predicate and silently returns every row, which is indistinguishable from a "
     "working filter by every other check in this driver. Read on `text`, not `code`: a real "
     "predicate routinely quotes a literal (`<> 'Cancelled'`), and `code` blanks string-literal "
     "contents for the COLUMNS class's benefit -- on this field that blanking would make every "
     "quoted predicate read as ABSENT even when it reached the SQL untouched"),
    ("TableName", "text",
     "the relation the element reads or writes. It reaches the artifact as source(..., '<name>') or "
     "config(alias='<name>'), both of which are string literals, so this one is read on the surface "
     "that keeps them"),
)


def _sanitized_identifier_candidate(val):
    """Mirrors the producer's per-illegal-character sanitization (AiFirstProducerDataFlowContext.
    SanitizeRelationIdentifier / Program.SanitizeIdentifier): alnum lowercased, everything else -> a
    single `_`, no collapsed runs, then trimmed and 'u_'-prefixed if that leaves nothing or a leading
    digit. A TableName that is a UNC path or otherwise dbt-illegal (I-21/SNOW-3956438) reaches the SQL
    as THIS string, not verbatim -- checked as an alternate match, never in place of the raw one, so a
    genuinely dropped TableName still reads as ABSENT."""
    chars = [c.lower() if c.isalnum() else "_" for c in val]
    result = "".join(chars).strip("_")
    if not result or result[0].isdigit():
        result = "u_" + result
    return result


def check_payload(ir, realisation):
    led = Ledger("PAYLOAD", "IR element payload value -> its value in the SQL")
    for node in ir.get("nodes") or []:
        nid = node.get("id") or ""
        el = node.get("element") or {}
        kind, art = realisation.get(nid, ("NONE", None))
        for field, surface, _why in PAYLOAD_FIELDS:
            val = el.get(field)
            if not isinstance(val, str) or not val.strip():
                continue
            subject = "%s . %s = %r" % (nid, field, val)
            if kind != "MODEL":
                led.skip(subject, "NO MODEL FOR THIS NODE",
                         "the node is realised as %s; the NODES class already carries this"
                         % ("a dbt project directory" if kind == "CONTAINER" else "nothing"))
                continue
            hay_flat = art.flat if surface == "code" else \
                re.sub(r"\s+", " ", art.text).casefold()
            hay_tight = art.tight if surface == "code" else \
                re.sub(r"\s+", "", art.text).casefold()
            candidates = [val]
            if field == "TableName":
                candidates.append(_sanitized_identifier_candidate(val))
            matched = False
            for candidate in candidates:
                flat = re.sub(r"\s+", " ", candidate).strip().casefold()
                tight = re.sub(r"\s+", "", candidate).casefold()
                if flat in hay_flat or tight in hay_tight:
                    matched = True
                    break
            if matched:
                led.ok(subject, "VALUE PRESENT", art.rel)
                continue
            # THE NAMED DIAGNOSIS, because "the predicate is missing" and "the predicate was
            # REPLACED BY ONE THAT KEEPS EVERY ROW" call for different responses and read identically
            # in a count.
            extra = ""
            if field == "FilterConditions" and re.search(r"\bwhere\s+true\b", art.code, re.I):
                extra = (" -- and the model carries `WHERE TRUE` in its place, which returns every "
                         "row while looking exactly like a filter")
            elif field == "FilterConditions" and not re.search(r"\bwhere\b", art.code, re.I):
                extra = " -- and the model carries no WHERE clause at all, so no row is excluded"
            led.lost(subject, "VALUE ABSENT",
                     "%s does not contain this value on the %s surface%s" % (art.rel, surface, extra))
    return led


# ==================================================================================================
# CLASS 5 — SYNTAX.  Is the emitted model even well-formed SQL, independent of what the IR asked for?
# ==================================================================================================

# Keywords (and the trailing comma) that cannot lawfully end a complete SQL statement. Chosen to be
# the shape a TRUNCATED file ends on, not a generic "bad SQL" linter -- a real Snowflake parser
# already reports everything else, and duplicating it here would be a second syntax checker that can
# disagree with the first.
_DANGLING_TAIL_WORDS = frozenset({
    "SELECT", "FROM", "WHERE", "AND", "OR", "ON", "JOIN", "GROUP", "ORDER", "BY", "HAVING",
    "UNION", "DISTINCT", "AS", "WITH", "CASE", "WHEN", "THEN", "ELSE", "IN", "NOT",
})

# THE EXACT SAME PATTERN ai_fill.is_degraded USES for an empty SELECT...FROM pair, deliberately not
# reinvented a third time. This project has already shipped two implementations of "is this
# projection empty" that disagreed (the driver's own uppercase-only, alone-on-a-line check vs.
# ai_fill's); a gate meant to catch exactly that shape must not become a fourth one.
_EMPTY_PROJECTION = re.compile(r"^\s*SELECT\s*$(.*?)^\s*FROM\s*$", re.S | re.M | re.I)


def _paren_balance(code):
    """(opens, closes, depth, first_unmatched_close_line) over CODE -- comments stripped AND string
    contents blanked.

    NOT OVER THE RAW FILE, AND THAT IS THE PART THAT MATTERS. MEASURED: `int_m_69.sql` from the same
    run that produced this class's two real positives contains
    `REPLACE("Lat Long Location2", '(', '')` -- a literal `(` character inside a string ARGUMENT, not
    a structural token. A raw character count over that file reports 10 open / 9 close and calls it
    unbalanced; the model is in fact well-formed SQL (5 open / 5 close once comments are stripped and
    string contents are blanked, same as the COLUMNS class already does for the same reason). A naive
    version of this exact check would have manufactured a false positive on a file this project had
    already correctly repaired.
    """
    depth = opens = closes = 0
    first_bad_line = None
    line = 1
    for ch in code:
        if ch == "\n":
            line += 1
            continue
        if ch == "(":
            opens += 1
            depth += 1
        elif ch == ")":
            closes += 1
            depth -= 1
            if depth < 0 and first_bad_line is None:
                first_bad_line = line
    return opens, closes, depth, first_bad_line


def check_syntax(models):
    """Two DETERMINISTIC, comment/string-aware checks, chosen because they are exactly what a real
    parser's `<EOF>` error looks like from the outside and cost nothing to run on every model:

      * balanced parentheses, over `Model.code` (comments stripped, string contents blanked) --
        see `_paren_balance` for why the naive raw-character version is actively wrong, not just
        weaker.
      * no statement ending on a dangling keyword or a trailing comma, and no `SELECT ... FROM`
        pair with nothing between them -- the exact shape the engine's own
        `UnsupportedTransformationTranslator` fallback produces when it substitutes a fresh
        `UnsupportedTransformation` whose OutputColumns and FROM lookup both came back empty (see
        the module docstring's SYNTAX entry for the traced root cause). Read on `Model.text`
        (comments stripped, strings kept): the empty-projection regex must not be fooled by a
        comment sitting between `SELECT` and `FROM`, the shape every one of this run's real
        positives has (an EWI comment block, then a bare `SELECT`).

    THIS CLASS NEVER OPENS THE IR. It is a precondition for the other four classes' comparisons to
    mean anything -- a model with a dangling `SELECT` and no `FROM` cannot be lying about which
    columns it projects, because it does not project at all -- so it runs unconditionally, on every
    model this gate finds, whether or not the IR reached it.
    """
    led = Ledger("SYNTAX", "emitted model -> well-formed SQL")
    for m in models:
        if not m.raw.strip():
            led.skip(m.rel, "EMPTY OR UNREADABLE FILE", "no content to check")
            continue
        opens, closes, depth, bad_line = _paren_balance(m.code)
        if depth != 0:
            where = " (first unmatched close at line %d)" % bad_line if bad_line else ""
            led.lost(m.rel, "UNBALANCED PARENTHESES", "%d open, %d close%s" % (opens, closes, where))
            continue
        tail = m.text.strip()
        last_word = re.split(r"\s+", tail)[-1].upper().rstrip(",;") if tail else ""
        if tail.endswith(","):
            led.lost(m.rel, "DANGLING TRAILING COMMA",
                     "the file ends mid column-list: ...%s" % _clip(tail, 40))
        elif last_word in _DANGLING_TAIL_WORDS:
            led.lost(m.rel, "DANGLING TRAILING KEYWORD", "the file ends on a bare `%s`" % last_word)
        elif any(not body.strip() for body in _EMPTY_PROJECTION.findall(m.text)):
            led.lost(m.rel, "EMPTY PROJECTION", "a SELECT ... FROM pair with nothing between them")
        else:
            led.ok(m.rel, "WELL-FORMED", "")
    return led


# ==================================================================================================
# REPORT
# ==================================================================================================

W = 96


def _clip(s, n):
    s = str(s)
    return s if len(s) <= n else "…" + s[-(n - 1):]


def _wrap(s, n, indent):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        lines.append(cur)
    return ("\n" + " " * indent).join(lines)


def report(ir_path, out_root, platform, ir, models, projects, led, empty_nodes, via_source, out):
    p = out.append
    p("=" * W)
    p(" STRUCTURAL INTEGRITY — did the IR reach the dbt?")
    p("=" * W)
    if platform:
        p(" platform      : %s" % platform)
    p(" IR            : %s   [%d node(s), %d edge(s)]"
      % (_clip(ir_path, 72), len(ir.get("nodes") or []), len(ir.get("edges") or [])))
    p(" emitted models: %d file(s) under %s" % (len(models), _clip(out_root, 60)))
    p(" dbt projects  : %d directory(ies) carrying dbt_project.yml" % len(projects))
    p(" INPUTS        : the IR and the tree. THIS GATE NEVER READS THE SOURCE DOCUMENT, so no")
    p("                 identification rule can decide its denominator — which is the failure")
    p("                 every gate upstream of it shares.")
    p(" MATCH RULE    : a model belongs to a node when its stem is the node's modelName,")
    p("                 optionally behind a `<prefix>_` the emitter added. A node with no model")
    p("                 is CONTAINER-realised when a dbt project directory is named for it.")
    p(" READING RULE  : every comparison is case-folded, and SQL COMMENTS ARE STRIPPED before any")
    p("                 match. Columns are matched on code with string literals blanked; payload")
    p("                 values on code with string literals kept. A name found only in a comment")
    p("                 discharges nothing.")
    p(" SYNTAX RULE   : SYNTAX reads no IR — it checks every emitted model is parseable SQL (balanced")
    p("                 parens, no dangling trailing keyword/comma, no empty SELECT...FROM), on the")
    p("                 same comment-stripped surfaces, so a literal paren inside a string argument")
    p("                 is never counted as a structural token.")
    p(" SCAFFOLD RULE : SCAFFOLD reads no IR either — it asks whether any framework file under")
    p("                 etl_instrumentation/ or etl_configuration/ NAMES a platform other than the")
    p("                 one declared above. A neutral name discharges; no declared platform makes")
    p("                 every name unmeasurable rather than clean.")
    p("-" * W)
    p(" class     unit                                            raised  disch  outst  unmeas  bal")
    p("-" * W)
    for L in led:
        p(" %-9s %-46s %6d %6d %6d %7d  %s"
          % (L.name, _clip(L.unit, 46), L.raised, len(L.discharged), len(L.outstanding),
             len(L.unmeasurable), "yes" if L.balances() else "NO"))
    p("-" * W)

    # ---- the difference, ITEMISED. A count with no inventory beside it is the shape of claim this
    # project has had to withdraw four times.
    total_out = sum(len(L.outstanding) for L in led)
    total_un = sum(len(L.unmeasurable) for L in led)
    if total_out:
        p(" OUTSTANDING — carried by the IR, not found in the dbt:")
        for L in led:
            for subject, why, ev in L.outstanding:
                p("   %-9s %s" % (L.name, _clip(subject, 80)))
                p("             %s: %s" % (why, _wrap(ev, W - 26, 13)))
        p("-" * W)
    if total_un:
        p(" UNMEASURABLE — raised, and this gate cannot answer it; NOT counted as carried:")
        for L in led:
            for subject, why, ev in L.unmeasurable:
                p("   %-9s %s" % (L.name, _clip(subject, 80)))
                p("             %s: %s" % (why, _wrap(ev, W - 26, 13)))
        p("-" * W)

    # ---- DISCHARGED, WITH A CAVEAT. A discharge that is weaker than the primary one has to be
    # PRINTED, not left in the `--json` ledger. MEASURED, while negative-testing the ambiguity path:
    # the gate recorded `MODEL (AMBIGUOUS)` in its structured output and its stdout — the surface the
    # driver and a human actually read — said `nodes 5/5` with no hint that one node was answered by
    # two files. A caveat only a machine can see is a caveat nobody acts on.
    caveats = [(L.name, s, h, e) for L in led for s, h, e in L.discharged
               if h not in ("MODEL", "CONTAINER", "IR NODE", "PROJECTED", "REF", "VALUE PRESENT",
                            "WELL-FORMED")]
    if caveats:
        p(" DISCHARGED, WITH A CAVEAT — counted as carried on WEAKER evidence than the primary rule:")
        for name, subject, how, ev in caveats:
            p("   %-9s %s" % (name, _clip(subject, 80)))
            p("             %s: %s" % (how, _wrap(ev, W - 26, 13)))
        p("-" * W)
    if empty_nodes:
        # THE EMPTY DENOMINATOR, PRINTED. "0 columns lost" over 0 obligations and over 18 are
        # opposite facts and only the second is evidence.
        p(" NODES THE IR CARRIES NO OutputColumns FOR — the COLUMNS class raises nothing for these")
        p(" and therefore says nothing about them. This is a hole in the IR (Gate A's question),")
        p(" not a finding about the dbt:")
        for n in empty_nodes:
            p("   %s" % _clip(n, 88))
        p("-" * W)
    if via_source:
        p(" %d edge(s) discharged by a direct source() read rather than a ref(). Counted as carried,"
          % via_source)
        p(" printed separately because it is a weaker witness than a ref() to the upstream model.")
        p("-" * W)

    # ---- THE EMPTY DENOMINATOR, PER CLASS. `columns 0/0` reads as a clean result and is not one:
    # it says the IR raised no column obligation at all, which on a document with columns is a loss
    # this gate structurally cannot see. Named in the verdict rather than left in the arithmetic,
    # because "0 of 0" and "18 of 18" are printed by the same format string and mean opposite things.
    # MEASURED, on the frozen DataStage arm: `columns 0/0` over an IR whose four nodes all carry an
    # empty OutputColumns.
    for L in led:
        if L.raised == 0:
            p(" *** %s RAISED NOTHING — the IR states no obligation of this class, so `%s 0/0`"
              % (L.name, L.name.lower()))
            p("     above is an EMPTY DENOMINATOR and not a clean result. Nothing was checked and")
            p("     nothing is claimed. This is NOT counted as information lost — the loss, if any,")
            p("     is upstream in the IR and is Gate A's question, not this gate's.")
            p("-" * W)
    return total_out, total_un


# ==================================================================================================

USAGE = ("usage: integrity_gate.py <ir.json> <output-root> [--platform NAME] [--json PATH]\n"
         "  exit 0 clean / 3 information lost / 1 could not run / 2 usage\n")


# ==================================================================================================
# CLASS 6 — SCAFFOLD.  Does every framework file in this tree belong to THIS platform?
# ==================================================================================================

# The platform tokens a scaffolding filename can carry, mapped to the `--platform` values the driver
# passes (it passes the platform table's stem, e.g. `alteryx`, `ssis`, `datastage`). A name carrying
# no token at all is platform-neutral and discharges -- `table_metrics_log.sql` and
# `collect_table_metrics.sql` are shared by every platform and are not evidence of anything.
_SCAFFOLD_TOKENS = {
    "ssis": "ssis",
    "dtsx": "ssis",
    "informatica": "informatica",
    "infpc": "informatica",
    "alteryx": "alteryx",
    "datastage": "datastage",
    "dsx": "datastage",
    "pentaho": "pentaho",
    "ktr": "pentaho",
}

# Only the directories the emitter fills with FRAMEWORK files. Models are the other five classes'
# subject and are deliberately not re-examined here.
_SCAFFOLD_DIRS = ("etl_instrumentation", "etl_configuration")


def check_scaffold(out_root, platform):
    """Every framework file's name against the platform this run declared.

    NOT A NAME LINTER. The single question is whether a file that ships inside this migration's
    output NAMES a platform that is not the one being migrated, because that file then states
    something false about the source to anyone reading the output -- the same defect class as an
    assessment row whose `Technology` column named the wrong platform.

    An unknown or absent `--platform` makes every file UNMEASURABLE rather than clean: without a
    declared platform there is nothing to be foreign to, and reporting that as a pass would be the
    empty-denominator shape this gate exists to refuse.
    """
    led = Ledger("SCAFFOLD", "framework file -> belongs to this platform")
    want = _SCAFFOLD_TOKENS.get(norm(platform or ""), norm(platform or "")) or None
    for base, _dirs, files in sorted(os.walk(out_root)):
        if not any(("%s%s" % (os.sep, d)) in base or base.endswith(d) for d in _SCAFFOLD_DIRS):
            continue
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(base, f), out_root)
            stem = norm(f)
            found = sorted({fam for tok, fam in _SCAFFOLD_TOKENS.items() if tok in stem})
            if not found:
                led.ok(rel, "PLATFORM-NEUTRAL NAME", "")
            elif want is None:
                led.skip(rel, "NO PLATFORM DECLARED FOR THIS RUN",
                         "name carries %s; nothing to compare it to" % ", ".join(found))
            elif found == [want]:
                led.ok(rel, "NAMES THIS PLATFORM", want)
            else:
                led.lost(rel, "NAMES A FOREIGN PLATFORM",
                         "name carries %s; this run is %s" % (", ".join(found), want))
    return led


def main(argv):
    platform = None
    json_out = None
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] == "--platform" and i + 1 < len(argv):
            platform = argv[i + 1]
            i += 2
        elif argv[i] == "--json" and i + 1 < len(argv):
            json_out = argv[i + 1]
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    if len(rest) != 2:
        sys.stderr.write(USAGE)
        return 2
    ir_path, out_root = rest

    # ---- COULD-NOT-RUN, and every one of these prints NO ` integrity     :` line, which is how the
    # driver tells "the gate could not run" from "the gate found something". One exit integer cannot
    # carry both claims; the stdout SHAPE can.
    if not os.path.isfile(ir_path):
        print(" INTEGRITY UNMEASURED: no representation at %s. This is NOT a claim that the dbt is"
              % ir_path)
        print("   complete, and NOT a claim that it is not — there is nothing to compare it to.")
        return 1
    try:
        ir = json.load(open(ir_path, "r", encoding="utf-8"))
    except Exception as exc:                                    # noqa: BLE001
        print(" INTEGRITY UNMEASURED: the representation at %s did not parse: %s" % (ir_path, exc))
        return 1
    if not isinstance(ir, dict) or not (ir.get("nodes") or []):
        # A ZERO-NODE IR IS NOT A CLEAN RESULT. Every class would raise 0, every class would balance,
        # and the gate would print a green 0/0 on a representation that lost the entire document.
        # That is the empty-denominator defect this project has now found in four gates, so it is an
        # explicit refusal rather than an arithmetic accident.
        print(" INTEGRITY UNMEASURED: the representation at %s carries NO NODES, so every class"
              % ir_path)
        print("   below would raise zero obligations and report a clean 0/0 over a representation")
        print("   that holds nothing. An empty denominator is refused, not reported as integrity.")
        return 1
    if not os.path.isdir(out_root):
        print(" INTEGRITY UNMEASURED: no emitted tree at %s." % out_root)
        return 1

    models = [Model(p, out_root) for p in find_models(out_root)]
    projects = find_projects(out_root)

    nodes_led, models_led, realisation = check_nodes(ir, models, projects, out_root)
    cols_led, empty_nodes = check_columns(ir, realisation)
    edges_led, via_source = check_edges(ir, realisation)
    pay_led = check_payload(ir, realisation)
    syntax_led = check_syntax(models)
    scaffold_led = check_scaffold(out_root, platform)
    led = [nodes_led, models_led, cols_led, edges_led, pay_led, syntax_led, scaffold_led]

    out = []
    total_out, total_un = report(ir_path, out_root, platform, ir, models, projects, led,
                                 empty_nodes, via_source, out)

    # ---- THE BALANCE ASSERTION, CHECKED AND PRINTED AND ABLE TO FAIL. If a class does not balance,
    # its numbers are describing different questions and the verdict line is withheld.
    unbalanced = [L.name for L in led if not L.balances()]
    if unbalanced:
        out.append(" *** INTEGRITY GATE DEFECT: LEDGER DOES NOT BALANCE for %s."
                   % ", ".join(unbalanced))
        out.append("     raised must equal discharged + outstanding + unmeasurable. It does not, so")
        out.append("     every figure above is measuring a different question and none of them is a")
        out.append("     verdict. This is a defect in THIS GATE, not a finding about the output.")
        print("\n".join(out))
        return 1

    carried = " ".join(
        "%s %d/%d" % (L.name.lower(), len(L.discharged), L.raised) for L in led)
    # THE VERDICT LINE. Its literal shape is depended on by aifirst-migrate.sh, which greps for
    # `^ integrity     :` to tell a real verdict from a gate that could not run.
    out.append(" integrity     : %s carried from the IR into the dbt" % carried)
    if total_un:
        out.append("                 %d obligation(s) UNMEASURABLE and excluded from the numerators "
                   "above" % total_un)
    out.append("-" * W)
    if total_out:
        out.append(" VERDICT: INFORMATION LOST BETWEEN THE IR AND THE DBT — %d obligation(s)"
                   % total_out)
        out.append("          outstanding, itemised above. The IR carries them and no artifact in")
        out.append("          this tree does. (exit 3)")
    else:
        out.append(" VERDICT: every obligation the IR raises is carried into the dbt (exit 0)")
    print("\n".join(out))

    if json_out:
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump({
                "ir": ir_path, "out_root": out_root, "platform": platform,
                "models": [m.rel for m in models],
                "projects": [os.path.relpath(p, out_root) for p in projects],
                "classes": [L.as_dict() for L in led],
                "nodes_without_columns": empty_nodes,
                "edges_via_source": via_source,
                "outstanding": total_out, "unmeasurable": total_un,
                "verdict": "LOST" if total_out else "CARRIED",
            }, fh, indent=1, sort_keys=True)
    return 3 if total_out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
