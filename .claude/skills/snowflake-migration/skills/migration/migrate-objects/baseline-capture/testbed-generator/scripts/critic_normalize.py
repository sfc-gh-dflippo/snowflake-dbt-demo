"""Verbatim-groundedness primitives for the enrichment critics.

The backbone asks "does this literal appear in the source?" against a corpus built from
constraint `detail` strings and deref'd `source_evidence` spans. Normalization must be
lenient enough that a correctly-cased golden literal never false-REJECTs, strict enough
that an invented literal ('Z' in a STATUS enum) is not spuriously matched.
"""
from __future__ import annotations

import re

_PTR = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\[(\d+)\]$")

# Where one literal ends and the next begins, applied as negative lookarounds rather than \b: \b is
# defined against the *pattern's* own edge characters, so a literal like '-1' would lose its left
# boundary, while a lookaround on an explicit class is keyed on the corpus text and holds for any
# literal shape.
#
# Deliberately `\w` and NOT critic_gate's _IDENT class ([A-Za-z_][A-Za-z0-9_$]*), on two counts:
#   * No `$`. _IDENT's `$` is a SQL-identifier *continuation* character, correct where that class
#     tokenizes a mined FK edge into identifiers. Here the corpus is prose-and-SQL constraint detail,
#     where `$` is overwhelmingly a currency *prefix*: with `$` as a boundary char the correctly-mined
#     'min balance $100' stops grounding the literal '100' -- a false-REJECT of a golden literal, the
#     one failure this module's docstring forbids outright, and worse than a stray false positive
#     because a backbone FAIL is a contractually-guaranteed-true hard reject. The trade is one observed
#     positive against a hypothetical `$`-in-identifier false positive: no `$`-containing identifier
#     appears anywhere in the corpora this actually sees (constraint `detail` strings plus deref'd
#     `source_evidence` string leaves, across the critics benchmark set and every mine-phase fixture).
#   * Unicode, not an ASCII class. Snowflake permits non-ASCII quoted identifiers, so an ASCII-only
#     boundary leaves 'GOLD' grounding in "GOLDN-with-enye" -- the exact aliasing this check exists to
#     stop, just spelled outside [A-Za-z]. `\w` on a str pattern is Unicode-aware by default.
_BOUND = r"\w"

# Numeric literals ground on VALUE, not on spelling -- see literal_grounded_normalized. Corpus numbers
# carry the same `\w` boundary as strings, so on word adjacency the value path is no more permissive than
# the string path and the widening adds only scale-equivalence: '50' grounds in neither 'ITEM_50' nor
# 'ITEM50'. The '-' and '.' in the lookbehind are a SIGN/SCALE guard on the corpus side, not an adjacency
# guard: they stop a digit run being read as a whole number when it is really the magnitude of a negative
# ('-5' yields no number, so the literal '5.0' does not ground in 'min temp -5') or the tail of a longer
# dotted run ('1.2.3' yields nothing rather than the fragment '2.3'). They do NOT withhold a hyphen
# adjacency from the overall answer, because '-' is not in \w and the STRING path above already grounds
# there first -- measured, literal_grounded('1', ['ABC-1']) is True, under the same boundary rule that
# lets the whole SKU 'ABC-1' ground.
_CORPUS_NUM = re.compile(r"(?<![\w.\-])\d+(?:\.\d+)?(?![\w.])")
_NUMERIC_LITERAL = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")


def normalize(s: object) -> str:
    t = "" if s is None else str(s)
    t = t.strip().casefold()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "'\"":
        t = t[1:-1].strip()
    return " ".join(t.split())


def string_leaves(node: object) -> list[str]:
    out: list[str] = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for v in node.values():
            out.extend(string_leaves(v))
    elif isinstance(node, list):
        for v in node:
            out.extend(string_leaves(v))
    return out


def deref_pointer(pointer: object, obj: object) -> list[str]:
    if not isinstance(pointer, str) or not isinstance(obj, dict):
        return []
    m = _PTR.match(pointer.strip())
    if not m:
        return []
    array, idx = m.group(1), int(m.group(2))
    seq = obj.get(array)
    if not isinstance(seq, list) or idx >= len(seq):
        return []
    return string_leaves(seq[idx])


def literal_grounded(literal: object, corpus: list) -> bool:
    return literal_grounded_normalized(literal, [normalize(c) for c in corpus])


def _numeric_value(t: str) -> float | None:
    # None for anything not a plain number, so a non-numeric literal never enters the value comparison.
    return float(t) if _NUMERIC_LITERAL.match(t) else None


def literal_grounded_normalized(literal: object, normalized_corpus: list[str]) -> bool:
    # Takes an already-normalized corpus so a caller checking M literals against one corpus
    # normalizes it once instead of M times.
    n = normalize(literal)
    if not n:
        return True  # empty literal: nothing to ground, must not false-REJECT
    # Boundary match, not substring. A bare `n in c` grounds any literal that merely happens to sit
    # inside a longer word, and the corpus always contains the column's own name and type: 'A' would
    # be "grounded" by "STATUS IN ('I','P')" via STATUS, and the docstring's own counter-example 'Z'
    # by BRONZE. Single-char CHAR(1) enum codes -- the canonical inferred_enum case, whose accept
    # example is ["G","S","B"] -- are exactly the values that alias most, so the backbone would PASS
    # an invented literal to the residue carrying a grounded_in anchor asserting evidence that was
    # never matched. Boundaries are _BOUND only, so a literal stays matchable when it is delimited by
    # quotes, commas, pipes, operators or a currency '$', and a hyphenated SKU like 'ABC-1' still
    # matches whole (tokenizing the corpus into SQL literals instead would split it at the hyphen).
    pat = re.compile(f"(?<!{_BOUND})" + re.escape(n) + f"(?!{_BOUND})")
    if any(pat.search(c) for c in normalized_corpus):
        return True
    # Numbers ground on value, not on spelling, because no boundary class can reconcile two spellings
    # of one number: '0.5' and '0.50' are the same value written at the scale each source happened to
    # use. Numeric literals do reach here -- inferred_enum elements are passed through unguarded
    # (check_value_entry grades each element of the raw wire array), and the gate cites `literal` for
    # an invented_literal REJECT with a numeric still counting as cited. (null_fraction_override does
    # NOT: it is range-checked only and never grounded, so its scale never matters here.) Strictness is
    # preserved because equality is on the parsed value: '10' still does not ground in '100'.
    num = _numeric_value(n)
    if num is None:
        return False
    return any(num == float(t) for c in normalized_corpus for t in _CORPUS_NUM.findall(c))
