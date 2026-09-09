"""THE TEXT RULE: an issue text states what was OBSERVED, never what the source does.

WHAT THIS IS FOR, MEASURED
--------------------------
A sweep of the engine's own issue catalogue found 33 texts that ASSERT source-platform
runtime behaviour -- 25 functional-difference notices and 8 warnings -- every one of
them in the two ETL dialects and none in the 12 SQL dialects. The worst of them tells a
reviewer that the source loads targets sequentially in a declared order, explains that
the generated model combines pipelines into one query instead, and asks the reviewer to
verify a consequence of that premise. On a platform nobody has implemented support for,
the premise is a GUESS PRESENTED AS FACT, and the reviewer is being asked to act on it.

The severity is not "a wrong label". A functional-difference notice is a thing a human
is expected to do something about. A reviewer who trusts a false one reasons about
semantics their platform does not have; a reviewer who learns to distrust them discounts
the whole channel, which is worse, because that channel is how real risk is reported.

So this module is the rule, executable, run at mint time. A text that asserts what the
source platform DOES is refused. A text that states what was READ from the document, or
what THIS pipeline could not do, passes.

WHY THE RULE DIFFERS FOR A TYPE AND AN INSTANCE
-----------------------------------------------
A TYPE is shared across platforms, so naming any platform in it is wrong by
construction -- refused outright. An INSTANCE describes one element in one document, so
naming the platform and the native element kind there is a FACT read off the file. What
is still refused on an instance is the adjacency that turns a name into a claim:
`<platform> <behaviour-verb>`.

WHAT THIS RULE CANNOT DO
------------------------
It is a lexical rule. It cannot tell a true claim from a false one, and it will not
catch a platform assertion phrased without a platform name or a listed verb
("targets are loaded in the declared order" has neither). It is a floor, not a proof.
Its value is that it is ON THE MINT PATH: a text that fails it does not reach an
artifact, so the failure mode has to be a new phrasing rather than a forgotten check.
"""

from __future__ import annotations

import re
import unicodedata

from .signature import PLATFORM_TOKENS, find_platform_tokens

TEXT_RULE_VERSION = "aim.text.v1"

# Verbs that describe what a system DOES at run time. Deliberately excludes the
# observation verbs -- declares, states, carries, contains, names, holds, records --
# because those describe the DOCUMENT's content, which is exactly what we want texts to
# talk about. `<platform> declares X` is a fact about a file; `<platform> evaluates X`
# is a claim about a runtime nobody here has run.
BEHAVIOUR_VERBS = {
    "load", "loads", "loaded", "loading",
    "evaluate", "evaluates", "evaluated",
    "execute", "executes", "executed",
    "run", "runs", "ran",
    "treat", "treats", "treated",
    "return", "returns", "returned",
    "propagate", "propagates", "propagated",
    "convert", "converts", "converted",
    "coerce", "coerces", "coerced",
    "truncate", "truncates", "truncated",
    "round", "rounds", "rounded",
    "sort", "sorts", "sorted",
    "process", "processes", "processed",
    "apply", "applies", "applied",
    "ignore", "ignores", "ignored",
    "allow", "allows", "allowed",
    "require", "requires", "required",
    "perform", "performs", "performed",
    "handle", "handles", "handled",
    "resolve", "resolves", "resolved",
    "default", "defaults", "defaulted",
    "use", "uses", "used",
    "read", "reads",
    "write", "writes", "wrote",
    "send", "sends", "sent",
    "route", "routes", "routed",
    "order", "orders", "ordered",
    "compare", "compares", "compared",
    "cast", "casts",
    "interpret", "interprets", "interpreted",
    "store", "stores", "stored",
    "generate", "generates", "generated",
    "support", "supports", "supported",
    "assign", "assigns", "assigned",
    "increment", "increments",
    "trim", "trims", "trimmed",
    "pad", "pads", "padded",
    "compute", "computes", "computed",
    "behave", "behaves", "behaved",
}

# PASSIVE VOICE IS NOT A PLATFORM ASSERTION, AND THIS WAS A MEASURED FALSE POSITIVE.
# "An Informatica transformation WAS NOT CONVERTED" describes OUR output; "Informatica
# LOADS targets sequentially" describes a runtime nobody here ran. The first is exactly
# what an honest issue text says, and the first version of this rule refused it, because
# `converted` is in the verb list and sat three tokens after the platform name. So a
# behaviour verb whose nearest preceding significant token is a form of "be" is read as
# passive and does not fire. Nothing this rule caught before is lost: in a passive claim
# ABOUT the platform ("targets are loaded sequentially by Informatica") the platform name
# comes AFTER the verb, and the forward scan never reached it anyway.
_BE_FORMS = {"is", "are", "was", "were", "be", "been", "being", "am", "'s", "get",
             "gets", "got", "becomes", "became"}

# Words that may sit between the subject and the verb without breaking the claim.
_SKIPPABLE = {
    "the", "a", "an", "its", "their", "this", "that", "these", "those",
    "always", "also", "then", "will", "would", "may", "might", "can", "could",
    "does", "do", "did", "not", "only", "by", "default", "usually", "typically",
    "generally", "silently", "implicitly", "internally", "automatically",
    "first", "instead", "either", "both", "all", "each", "every", "and", "or",
}

# Generic ways of naming the source system without naming the product. These are as
# much of a claim as a product name is, and easier to write by accident.
_SOURCE_SUBJECTS = (
    "the source platform", "the source system", "the source engine",
    "the source tool", "the source product", "the source application",
    "the source job", "the source mapping", "the source package",
    "the source transformation", "the source pipeline", "the source workflow",
    "the original job", "the original mapping", "the original package",
    "the original pipeline", "the original workflow", "the original transformation",
    "the source", "the origin platform", "the legacy platform", "the legacy system",
)

# Claims nothing in this pipeline verifies. Distinct from a platform assertion: these
# are assertions about the OUTPUT's fidelity, and this project has already shipped one
# ("RUNNABLE, NOT VERIFIED") that was measured false in the same line whose purpose was
# honesty.
_UNVERIFIABLE = (
    "is equivalent", "are equivalent", "semantically equivalent",
    "same behaviour", "same behavior", "identical behaviour", "identical behavior",
    "will produce the same", "produces the same result", "guarantees", "guaranteed",
    "preserves the semantics", "preserves semantics", "behaves identically",
    "no functional difference", "fully equivalent", "exactly the same",
)

_TOKEN = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(unicodedata.normalize("NFKC", text or "").casefold())


def _verb_after(tokens: list[str], start: int, window: int = 3) -> str | None:
    """The first ACTIVE behaviour verb within `window` significant tokens after `start`.

    A verb in the passive voice is skipped rather than matched -- see _BE_FORMS.
    """
    seen = 0
    prev = tokens[start] if 0 <= start < len(tokens) else ""
    for tok in tokens[start + 1:]:
        if tok in _SKIPPABLE:
            continue
        if tok in BEHAVIOUR_VERBS and prev not in _BE_FORMS:
            return tok
        prev = tok
        seen += 1
        if seen >= window:
            return None
    return None


def _platform_positions(tokens: list[str]) -> list[tuple[int, str]]:
    """Indices of single-word platform tokens. Multi-word names are handled by the
    substring pass in find_platform_tokens; the adjacency rule only needs a position,
    and every multi-word name here begins with a word that is also matched alone."""
    singles = {t for t in PLATFORM_TOKENS if " " not in t}
    return [(i, t) for i, t in enumerate(tokens) if t in singles]


def lint(text: str, *, scope: str) -> dict:
    """Lint one issue text.

    scope="type"     a text shared across platforms. Naming any platform is refused.
    scope="instance" a text about one element in one document. A platform name is a
                     fact; a platform name next to a behaviour verb is not.

    Returns {"rule_version", "scope", "verdict": PASS|REJECT|WARN, "findings": [...]}.
    Each finding carries the rule id, the matched span and why it is refused, so a
    reviewer can see the reason and not just the outcome.
    """
    toks = _tokens(text)
    findings: list[dict] = []

    for idx, tok in _platform_positions(toks):
        verb = _verb_after(toks, idx)
        if verb:
            findings.append({
                "rule": "A1_PLATFORM_ASSERTS_BEHAVIOUR",
                "severity": "REJECT",
                "match": " ".join(toks[idx:idx + 5]),
                "why": f"{tok!r} followed by the behaviour verb {verb!r}: this states "
                       f"what the source platform DOES at run time. Nothing here ran "
                       f"it. State what the document DECLARES instead.",
            })

    low = " ".join(toks)
    for subject in _SOURCE_SUBJECTS:
        for m in re.finditer(re.escape(subject) + r"\b", low):
            # Position in token space, to reuse the adjacency window.
            before = low[:m.end()].split()
            verb = _verb_after(low.split(), len(before) - 1)
            if verb:
                findings.append({
                    "rule": "A2_SOURCE_SUBJECT_ASSERTS_BEHAVIOUR",
                    "severity": "REJECT",
                    "match": low[m.start():m.end() + 30],
                    "why": f"{subject!r} followed by the behaviour verb {verb!r}: a "
                           f"claim about the source's runtime, made without naming it. "
                           f"Same defect as naming it.",
                })

    for phrase in _UNVERIFIABLE:
        if phrase in low:
            findings.append({
                "rule": "A3_UNVERIFIABLE_CLAIM",
                "severity": "REJECT",
                "match": phrase,
                "why": f"{phrase!r} asserts a fidelity property nothing in this "
                       f"pipeline checks. This project has already shipped one such "
                       f"claim and measured it false.",
            })

    if scope == "type":
        named = find_platform_tokens(text)
        if named:
            findings.append({
                "rule": "B1_TYPE_NAMES_A_PLATFORM",
                "severity": "REJECT",
                "match": ", ".join(named),
                "why": "an issue TYPE is shared across platforms by construction. "
                       "Naming one here makes the type unusable for the next platform "
                       "-- the exact defect that forced a producer to report a "
                       "third platform's element under another platform's name.",
            })
    elif scope == "instance":
        named = find_platform_tokens(text)
        if named:
            findings.append({
                "rule": "B2_INSTANCE_NAMES_A_PLATFORM",
                "severity": "WARN",
                "match": ", ".join(named),
                "why": "allowed on an instance -- the platform of THIS document is a "
                       "fact -- but recorded so a sweep can find it if the rule is "
                       "ever tightened.",
            })
    else:
        raise ValueError(f"scope must be 'type' or 'instance', not {scope!r}")

    verdict = ("REJECT" if any(f["severity"] == "REJECT" for f in findings)
               else "WARN" if findings else "PASS")
    return {"rule_version": TEXT_RULE_VERSION, "scope": scope,
            "verdict": verdict, "findings": findings}
