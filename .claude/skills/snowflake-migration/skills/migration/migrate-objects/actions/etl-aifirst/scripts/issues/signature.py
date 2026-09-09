"""THE ID SCHEME. A content-addressed identifier for an issue TYPE.

WHY NOT A COUNTER
-----------------
The owner flagged run conditions before any code existed, and a counter is where they
bite: two agents that each read `next_id = 7` both mint `AIM-007` for different issues,
or the same issue twice under two numbers. Locking around a counter would work and
would also mean every proposing agent needs write access to the same file at the same
time -- the exact coupling we are trying not to have.

So the id is a HASH OF A NORMALISED SEMANTIC SIGNATURE. Two agents that independently
find the same issue derive the SAME id without talking to each other, and the race
becomes benign: both write the same bytes to the same filename. Two agents that find
DIFFERENT issues derive different ids and cannot collide. Nothing is ever renumbered,
because there is no number to shift -- which matters because emitted artifacts cite
these codes, and a code that means something else next week makes last week's output
unreadable.

WHAT GOES INTO THE SIGNATURE, AND WHAT MUST NOT
-----------------------------------------------
Three fields, deliberately few:

  category   what kind of thing went wrong, in OUR pipeline's terms
  construct  the SHAPE of the thing it went wrong on, platform-neutral
  reason     why this pipeline could not handle it

The platform, the native element kind, the element's name, the file it came from and
the run it was found in are ALL EXCLUDED. They belong to the INSTANCE, not the type.
That is not tidiness: including them would mean a DataStage Transformer and a Pentaho
Janino step get two ids for one issue, which is the fifty-near-duplicates failure mode
this framework exists to avoid, and it would also make the id un-shareable across
platforms -- the whole point of not using the engine's platform-named enum.

A signature field naming a platform is REJECTED rather than silently stripped. Silent
stripping would make `ssis-router` and `router` converge, which is convenient and hides
a modelling error; the rejection tells the proposer to move the platform to the
instance where it belongs.

THE ONE HAZARD THIS SCHEME HAS
------------------------------
An id is a function of the NORMALISER. Change the alias table and old inputs hash
differently. So SIG_VERSION is part of the hashed material and is recorded on every
type. A future v2 normaliser does not invalidate v1 ids: they stay in the inventory,
append-only, and are still resolvable. It does mean v1 and v2 can hold two ids for one
issue, which is a real cost, recorded here rather than discovered later.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata

# Bumped ONLY when normalisation changes. Part of the hashed material, so a bump
# deliberately produces new ids rather than silently changing old ones.
SIG_VERSION = "aim.sig.v1"

# ------------------------------------------------------------------------------------
# CATEGORIES. Declared, with definitions, and OPEN: an unknown category is allowed and
# flagged rather than refused. A closed category enum would be the same shape as the
# 888-member enum we are escaping, one level up. What keeps the set from sprawling is
# the classify-before-mint step, not a hard list.
# ------------------------------------------------------------------------------------
CATEGORIES = {
    "REPR": "the intermediate representation has no member for the construct",
    "EXPR": "text in a language this pipeline does not lower to the target dialect",
    "PRED": "a condition or predicate no extraction rule obtained from the document",
    "SHAPE": "a structural property (columns, branches, ports) the representation "
             "does not carry",
    "REF": "a reference between generated units that does not resolve, or an edge the "
           "artifact does not carry",
    "EMIT": "the construct was represented and the renderer produced no usable output",
}

# ------------------------------------------------------------------------------------
# PLATFORM TOKENS. Rejected in a TYPE signature and in a TYPE's text. Allowed on an
# INSTANCE, where naming the platform is a fact read off the document rather than a
# claim about a vocabulary. Target-side names (snowflake, dbt) are NOT here: the target
# is not a guess.
# ------------------------------------------------------------------------------------
PLATFORM_TOKENS = (
    "informatica", "powercenter", "power center", "infapc", "infa",
    "ssis", "dtsx", "integration services", "sql server integration",
    "datastage", "infosphere", "dsx", "dsjob",
    "pentaho", "kettle", "spoon", "ktr", "pdi",
    "talend", "azure data factory", "data factory", "adf",
    "matillion", "airflow", "abinitio", "ab initio",
)

# ------------------------------------------------------------------------------------
# ALIASES. THE PART THAT MAKES TWO INDEPENDENT FINDERS CONVERGE.
#
# Content addressing only helps if two agents describing the same thing produce the
# same STRING. They will not: one writes `router`, the other `multi-output-router`,
# the third `fan-out`. So a small alias table folds known phrasings onto a canonical
# token BEFORE hashing. This is the cheap half of matching; the expensive half is the
# similarity search in inventory.py, which catches phrasings this table has never seen.
# ------------------------------------------------------------------------------------
CONSTRUCT_ALIASES = {
    "container": "element:containment-scope",
    "containment": "element:containment-scope",
    "unit-of-work": "element:containment-scope",
    "scope": "element:containment-scope",
    "element:container": "element:containment-scope",
    "router": "element:multi-output-branching",
    "fan-out": "element:multi-output-branching",
    "fanout": "element:multi-output-branching",
    "multi-output-router": "element:multi-output-branching",
    "element:router": "element:multi-output-branching",
    "element:multi-output-router": "element:multi-output-branching",
    "columns": "element:column-set",
    "column-metadata": "element:column-set",
    "field-metadata": "element:column-set",
    "element:columns": "element:column-set",
    "expression": "column:value-derivation",
    "derivation": "column:value-derivation",
    "formula": "column:value-derivation",
    "column:expression": "column:value-derivation",
    "derivation-text": "element:derivation-text",
    "expression-text": "element:derivation-text",
    "predicate": "predicate:row-filter",
    "condition": "predicate:row-filter",
    "filter-predicate": "predicate:row-filter",
    "where-clause": "predicate:row-filter",
    "upstream-ref": "reference:upstream-element",
    "dangling-ref": "reference:upstream-element",
    "ref": "reference:upstream-element",
    "role": "element:role",
}

REASON_ALIASES = {
    "unsupported-kind": "no-vocabulary-member",
    "no-ir-kind": "no-vocabulary-member",
    "no-representation": "no-vocabulary-member",
    "not-in-vocabulary": "no-vocabulary-member",
    "degraded": "degraded-to-catch-all-class",
    "degrade-to-unsupported": "degraded-to-catch-all-class",
    "dialect-not-lowered": "no-lowering-for-source-language",
    "no-translator-for-dialect": "no-lowering-for-source-language",
    "no-lowering": "no-lowering-for-source-language",
    "no-rule-scraped-it": "not-extractable-by-any-rule",
    "unscrapable": "not-extractable-by-any-rule",
    "not-obtainable": "not-extractable-by-any-rule",
    "no-field-metadata-declared": "not-declared-by-document",
    "document-declares-none": "not-declared-by-document",
    "absent-from-document": "not-declared-by-document",
    "branches-collapsed": "branches-collapsed-in-representation",
    "dangling": "reference-does-not-resolve",
    "unresolvable-reference": "reference-does-not-resolve",
    "edge-lost": "edge-absent-from-artifact",
    "translator-threw": "renderer-raised-an-error",
    "renderer-threw": "renderer-raised-an-error",
    "needs-a-platform-assertion": "would-require-asserting-a-platform",
}

_WS = re.compile(r"[\s_]+")
_PUNCT = re.compile(r"[^a-z0-9:\-]+")
_DASHES = re.compile(r"-{2,}")


class PlatformInSignature(ValueError):
    """A type signature named a platform. The platform belongs on the instance."""


def normalise(text: str, aliases: dict[str, str] | None = None) -> str:
    """Fold one signature field to its canonical token.

    NFKC first so a full-width or accented character cannot produce a second id for
    the same word; then casefold, whitespace and underscores to hyphens, punctuation
    dropped, runs of hyphens collapsed. Alias lookup happens LAST, on the folded form,
    so `Multi_Output Router` and `multi-output-router` both find the alias.
    """
    t = unicodedata.normalize("NFKC", text or "").strip().casefold()
    t = _WS.sub("-", t)
    t = _PUNCT.sub("-", t)
    t = _DASHES.sub("-", t).strip("-")
    if aliases:
        t = aliases.get(t, t)
    return t


def find_platform_tokens(text: str) -> list[str]:
    """Platform names present in `text`, matched on word boundaries.

    Word-boundary matching is not decoration: `infa` inside `information` and `adf`
    inside `adfs` would otherwise make neutral prose unminteable.
    """
    low = unicodedata.normalize("NFKC", text or "").casefold()
    hits = []
    for tok in PLATFORM_TOKENS:
        if re.search(r"(?<![a-z0-9])" + re.escape(tok) + r"(?![a-z0-9])", low):
            hits.append(tok)
    return hits


def canonical(category: str, construct: str, reason: str) -> dict[str, str]:
    """The normalised signature. Raises if any field names a platform."""
    sig = {
        "category": normalise(category).upper(),
        "construct": normalise(construct, CONSTRUCT_ALIASES),
        "reason": normalise(reason, REASON_ALIASES),
    }
    for field, value in sig.items():
        bad = find_platform_tokens(value)
        if bad:
            raise PlatformInSignature(
                f"signature field {field}={value!r} names {bad}. A type is shared "
                f"across platforms by construction; put the platform on the instance "
                f"(instance.platform / instance.native_kind) instead."
            )
    return sig


def signature_id(category: str, construct: str, reason: str) -> tuple[str, dict, str]:
    """Return (id, canonical signature, the exact string that was hashed).

    The hashed string is returned so a reader can recompute the id by hand from the
    stored record -- the property that makes "content-addressed" checkable rather
    than asserted.
    """
    sig = canonical(category, construct, reason)
    material = "\x1f".join(
        (SIG_VERSION, sig["category"], sig["construct"], sig["reason"]))
    digest = hashlib.blake2s(material.encode("utf-8"), digest_size=6).hexdigest()
    return f"AIM-{sig['category']}-{digest}", sig, material
