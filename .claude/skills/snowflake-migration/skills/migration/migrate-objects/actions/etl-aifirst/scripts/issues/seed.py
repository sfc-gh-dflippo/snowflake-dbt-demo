"""THE SEED: six issue types this project has already MEASURED.

Why seed at all? An empty inventory cannot demonstrate classification -- every finding
would mint, and "classify before you mint" would be an untested branch on the first run.
Every type here is taken from a measurement already recorded in this project, with the
citation on the record, so the first run exercises the reuse path against real cases
rather than against invented ones.

Each text was written to pass the framework's OWN platform-assertion rule, which is the
point of having the rule on the mint path: the six seeds are the first six things it
checked. Note what the texts do NOT say. None of them explains what the source platform
would have done with the construct, because on a platform nobody has implemented support
for, that is a guess. They say what the document DECLARES, what the representation
CARRIES, and what the generated output therefore does not contain.
"""

from __future__ import annotations

from .inventory import Inventory

SEEDS = [
    # ------------------------------------------------------------------ 1. REPR
    {
        "category": "REPR",
        "construct": "element:containment-scope",
        "reason": "no-vocabulary-member",
        "title": "Element kind with no member in the representation for a containment "
                 "scope",
        "text": "The document declares an element of kind '{kind}' named '{element}' "
                "that contains other elements. The representation this migration uses "
                "is a flat graph of data-flow elements with no member for an element "
                "that contains others, so it is carried as an unrepresented node: no "
                "model is generated from it, and whatever it declares about the "
                "elements inside it is not carried. {detail}",
        "impact": "output-incomplete",
        "note": "The engine's intermediate representation has no containment tier at "
                "all; a task holding a whole data flow becomes a directory plus a row "
                "in the orchestration SQL and never a model. Filed as ENG-001. Left "
                "unrepresented deliberately rather than degraded, because the "
                "orchestration half reads these nodes to find its boundary marker.",
        "first_observed": "poc/spikes/element-id-fit/platform_ssis.json "
                          "kind_dispatch['Microsoft.Pipeline'].degrade_reason; ticket "
                          "ENG-001-ir-containment-tier.md",
        "distinguisher": "seed",
    },
    # ------------------------------------------------------------------ 2. EXPR
    {
        "category": "EXPR",
        "construct": "element:derivation-text",
        "reason": "no-lowering-for-source-language",
        "title": "Derivation text in a language this migration does not lower",
        "text": "Element '{element}' of kind '{kind}' carries derivation text in the "
                "document. This migration has no lowering from that text's language "
                "into the target dialect, so the text was read and not translated. "
                "Nothing generated for this element computes the values the text "
                "names, and no check here establishes what they should be. {detail}",
        "impact": "output-incomplete",
        "note": "Two measured instances, both refused deliberately rather than mapped: "
                "a transformer stage whose derivations are in a procedural BASIC "
                "dialect, and a user-defined-expression step whose body is Java. "
                "Mapping either onto the expression-carrying element would have put "
                "untranslated text into a .sql file -- syntactically plausible, "
                "semantically wrong, and with no marker saying so. One of the two has "
                "an unconsumed parser already in the engine tree (findings/45), so a "
                "deterministic lowering is tractable there and a model is a stopgap; "
                "for the other no such groundwork exists.",
        "first_observed": "findings/41-the-fallback-ladder.md (Java derivation, tier 2); "
                          "poc/spikes/element-id-fit/platform_datastage.json "
                          "kind_dispatch['CTransformerStage'].degrade_reason",
        "distinguisher": "seed",
    },
    # ------------------------------------------------------------------ 3. PRED
    {
        "category": "PRED",
        "construct": "predicate:row-filter",
        "reason": "not-extractable-by-any-rule",
        "title": "Row-selection condition not obtained by any extraction rule",
        "text": "Element '{element}' of kind '{kind}' is represented as a row-selection "
                "step and the representation carries no condition for it. No extraction "
                "rule in this migration obtained one from the document. A row-selection "
                "step with no condition must not be generated as one that keeps every "
                "row, because that changes which rows reach the output while looking "
                "correct, so no selection is generated here at all. {detail}",
        "impact": "output-incomplete",
        "note": "The engine's filter translator substitutes WHERE TRUE for an empty "
                "predicate and records it only as a log warning -- a filter that keeps "
                "every row with nothing in the artifact saying so. That is why an "
                "unobtainable predicate has to degrade loudly instead of hydrating a "
                "hollow filter. Measured shape: a predicate held as a nested condition "
                "tree that no flat scrape rule reaches.",
        "first_observed": "poc/spikes/element-id-fit/platform_ssis.json "
                          "kind_dispatch['Microsoft.ConditionalSplit'].note; "
                          "findings/41-the-fallback-ladder.md (nested condition tree)",
        "distinguisher": "seed",
    },
    # ----------------------------------------------------------------- 4. SHAPE
    {
        "category": "SHAPE",
        "construct": "element:column-set",
        "reason": "not-declared-by-document",
        "title": "No column metadata for an element",
        "text": "Element '{element}' of kind '{kind}' is represented with no input "
                "columns and no output columns. The document states none at the place "
                "this migration's rule looks for them, so nothing generated from this "
                "element can name a column and a generated artifact for it can only "
                "project a placeholder. {detail}",
        "impact": "output-incomplete",
        "note": "Measured on a reader step that declares no field metadata at all: the "
                "column list existed only inside the step's embedded query text. Also "
                "measured on a writer element where both column lists came back empty "
                "because the table rule did not resolve the step's field mapping -- so "
                "this type covers a real document gap AND a gap in our own port policy, "
                "and the instance record is where they are told apart.",
        "first_observed": "findings/41-the-fallback-ladder.md (tier-3 table: reader "
                          "declares no field metadata; writer column lists empty)",
        "distinguisher": "seed",
    },
    # ------------------------------------------------------------------- 5. REF
    {
        "category": "REF",
        "construct": "reference:upstream-element",
        "reason": "reference-does-not-resolve",
        "title": "A generated reference names a unit that is not in the output",
        "text": "A generated artifact for element '{element}' references the unit "
                "'{detail}', and no generated unit of that name is present in the "
                "output. The reference cannot resolve, so the artifact cannot run as "
                "generated. This states a defect in the generated output and claims "
                "nothing about the document.",
        "impact": "output-absent",
        "note": "Two measured causes with one symptom. The engine resolves an upstream "
                "reference by walking COLUMNS, so an element whose column lists are "
                "empty gets a reference to nothing (ENG-021); and when the walk fails "
                "the renderer emits a not-found placeholder that reaches the artifact as "
                "a dangling reference (ENG-022). A column-poor platform hits both.",
        "first_observed": "tickets/ENG-021-ref-resolved-through-columns.md; "
                          "tickets/ENG-022-notfound-placeholder-emits-a-dangling-ref.md",
        "distinguisher": "seed",
    },
    # ----------------------------------------------------------------- 6. SHAPE
    {
        "category": "SHAPE",
        "construct": "element:multi-output-branching",
        "reason": "branches-collapsed-in-representation",
        "title": "Fewer output branches in the representation than the document declares",
        "text": "The document declares {detail} for element '{element}' of kind "
                "'{kind}'. The representation carries fewer of them. The branches that "
                "are not carried, and the conditions the document states for them, are "
                "absent from the output, and nothing generated here refers to them.",
        "impact": "output-incomplete",
        "note": "THE CASE THAT CANNOT BE REPRESENTED WITHOUT ASSERTING A PLATFORM. The "
                "engine has the right class for a multi-output router, but it is "
                "abstract and its only concrete subclasses are named after the two "
                "platforms the engine supports -- so a producer for a third platform "
                "would have to pick one of those two names to represent a router at "
                "all. The representation also exposes no per-branch group, so carrying "
                "the branch conditions is a schema widening and not a table edit. A "
                "split with one live branch is representable as a row-selection step; "
                "two live branches is this type.",
        "first_observed": "poc/spikes/element-id-fit/platform_informatica.json "
                          "kind_dispatch['Router'].degrade_reason; "
                          "platform_ssis.json kind_dispatch['Microsoft.ConditionalSplit']"
                          ".note; ticket ENG-017",
        "distinguisher": "seed",
    },
]


def seed(inv: Inventory, by: str = "seed") -> dict:
    """Idempotent. Every seed goes through classify_or_mint like anything else."""
    out = {"minted": [], "already": [], "reused": [], "raced": []}
    for s in SEEDS:
        res = inv.classify_or_mint(dict(s), by=by)
        out[{"MINTED": "minted", "REUSED_EXACT": "already", "REUSED_NEAR": "reused",
             "MINT_RACED": "raced"}[res["action"]]].append(res["id"])
    return out
