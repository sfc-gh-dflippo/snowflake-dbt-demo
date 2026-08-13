"""
SQL and Jinja parsing helpers shared by all rule packs.

These are deliberately tolerant, text-level utilities rather than a real SQL
parser. That is a conscious simplification: an audit needs to run on projects
that do not compile (a common state for freshly converted code), so it cannot
depend on ``dbt compile`` or on a dialect-complete grammar.

Ceiling of this approach: expressions built dynamically by macros are opaque to
us, and deeply unusual formatting can defeat the paren matcher. Upgrade path if
that becomes limiting is ``sqlglot`` on the *compiled* SQL in ``target/``, used
to enrich -- not replace -- these checks.

Every pattern-matching rule must run against stripped text (see
``strip_all``) or it will match inside comments and string literals.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

# =============================================================================
# Stripping
# =============================================================================


def strip_comments_and_strings(sql: str) -> str:
    """
    Blank out SQL comments and string literals, preserving character offsets
    where practical so line numbers stay meaningful.

    Same approach as ``dbt_validation.sql.validator.strip_comments_and_strings``,
    but newlines inside removed block comments are preserved so that
    ``find_line_number`` remains accurate afterwards.
    """

    def _blank_keep_newlines(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    sql = re.sub(r"/\*.*?\*/", _blank_keep_newlines, sql, flags=re.DOTALL)
    sql = re.sub(r"--[^\n]*", _blank_keep_newlines, sql)
    sql = re.sub(r"'[^'\n]*'", lambda m: "'" + " " * (len(m.group(0)) - 2) + "'", sql)
    sql = re.sub(r'"[^"\n]*"', lambda m: '"' + " " * (len(m.group(0)) - 2) + '"', sql)
    return sql


def strip_jinja(sql: str) -> str:
    """
    Blank out Jinja statement and comment blocks (``{% %}``, ``{# #}``),
    leaving ``{{ }}`` expressions in place because ``ref()``/``source()`` calls
    are meaningful to most checks.
    """

    def _blank_keep_newlines(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    sql = re.sub(r"\{%.*?%\}", _blank_keep_newlines, sql, flags=re.DOTALL)
    sql = re.sub(r"\{#.*?#\}", _blank_keep_newlines, sql, flags=re.DOTALL)
    return sql


def strip_all(sql: str) -> str:
    """Strip comments, string literals, and Jinja statement blocks."""
    return strip_jinja(strip_comments_and_strings(sql))


def find_line_number(content: str, position: int) -> int:
    """1-based line number for a character offset."""
    return content[:position].count("\n") + 1


def raw_span(raw: str, start: int, end: int, limit: int = 200) -> str:
    """
    Recover the original source text for a span located in stripped output.

    Safe because ``strip_comments_and_strings`` and ``strip_jinja`` blank
    characters in place rather than deleting them, so offsets are identical in
    both strings. Do not reorder or shorten text in the stripping functions
    without revisiting this.

    Rules use this for the ``evidence`` field: a finding that quotes
    ``source(' ', ' ')`` because the literals were blanked looks like a broken
    tool, even when the finding is correct.
    """
    snippet = raw[start:end]
    collapsed = re.sub(r"\s+", " ", snippet).strip()
    return collapsed[:limit]


# =============================================================================
# Paren matching
# =============================================================================


def match_paren(text: str, open_index: int) -> int:
    """
    Given the index of an opening ``(``, return the index of its matching
    ``)``, or -1 if unbalanced.

    Assumes ``text`` has already been stripped of strings and comments, so
    parentheses inside literals cannot skew the count.
    """
    if open_index >= len(text) or text[open_index] != "(":
        return -1
    depth = 0
    for i in range(open_index, len(text)):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    """Split on a delimiter, ignoring delimiters nested inside (), [] or {}."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == delimiter and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


# =============================================================================
# dbt config extraction
# =============================================================================

_TRUE = {"true", "True"}
_FALSE = {"false", "False"}


def _parse_value(raw: str) -> Any:
    """Best-effort literal conversion; unparseable values stay as raw text."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw in _TRUE:
        return True
    if raw in _FALSE:
        return False
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if raw.startswith("[") and raw.endswith("]"):
        return [_parse_value(item) for item in split_top_level(raw[1:-1])]
    return raw


def extract_config(raw_sql: str) -> dict[str, Any]:
    """
    Extract kwargs from every ``config(...)`` call in a model.

    Handles the two common shapes -- ``{{ config(...) }}`` and a ``config()``
    call inside a ``{% set %}``-style block -- and merges them, later winning.
    String, list, bool, and int values are converted; anything else (a Jinja
    expression, a dict) is kept as raw text so a rule can still pattern-match it.

    Note the values, not just the keys, matter to several rules: ``pre_hook``
    bodies are inspected for TRUNCATE/DELETE, and ``cluster_by`` length is
    counted.
    """
    config: dict[str, Any] = {}
    # Search the un-stripped text so hook strings survive, but use a stripped
    # copy for paren balancing so quotes containing parens do not break it.
    balance_text = strip_comments_and_strings(raw_sql)

    for match in re.finditer(r"\bconfig\s*\(", balance_text):
        open_index = balance_text.index("(", match.start())
        close_index = match_paren(balance_text, open_index)
        if close_index == -1:
            continue
        body = raw_sql[open_index + 1 : close_index]
        for part in split_top_level(body):
            if "=" not in part:
                continue
            key, _, value = part.partition("=")
            key = key.strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                config[key] = _parse_value(value)
    return config


def config_hooks(config: dict[str, Any]) -> list[tuple[str, str]]:
    """
    All hook bodies in a config, as ``(key, body)`` pairs.

    dbt accepts both ``pre_hook``/``pre-hook`` spellings and both a single
    string and a list of strings, so every hook rule would otherwise need to
    re-handle four shapes.
    """
    out: list[tuple[str, str]] = []
    for key in ("pre_hook", "pre-hook", "post_hook", "post-hook"):
        value = config.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            out.extend((key, str(item)) for item in value)
        else:
            out.append((key, str(value)))
    return out


# =============================================================================
# Refs, sources, CTEs, subqueries
# =============================================================================

REF_PATTERN = re.compile(
    r"\bref\s*\(\s*['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?\s*\)"
)
SOURCE_PATTERN = re.compile(
    r"\bsource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
)


def extract_refs(raw_sql: str) -> list[str]:
    """Model names referenced via ``ref()``. Handles the two-arg package form."""
    names: list[str] = []
    for match in REF_PATTERN.finditer(raw_sql):
        # Two-arg form is ref('package', 'model') -- the model is the last group.
        names.append(match.group(2) or match.group(1))
    return names


def extract_sources(raw_sql: str) -> list[tuple[str, str]]:
    """``(source_name, table_name)`` pairs referenced via ``source()``."""
    return [(m.group(1), m.group(2)) for m in SOURCE_PATTERN.finditer(raw_sql)]


#: Words that can precede ``AS (`` without being a CTE name.
_CTE_STOPWORDS = {
    "select",
    "from",
    "where",
    "and",
    "or",
    "not",
    "case",
    "when",
    "then",
    "else",
    "end",
    "as",
    "on",
    "join",
    "inner",
    "left",
    "right",
    "full",
    "outer",
    "cross",
    "union",
    "all",
    "group",
    "order",
    "by",
    "having",
    "limit",
    "with",
    "insert",
    "update",
    "delete",
    "cast",
    "over",
    "partition",
    "qualify",
    "distinct",
    "using",
    "values",
    "recursive",
}


def extract_ctes(stripped_sql: str) -> list[dict[str, Any]]:
    """
    CTEs defined in the statement, as dicts with ``name``, ``body``, ``start``.

    Input must already be stripped, otherwise ``AS (`` inside a comment counts.
    """
    ctes: list[dict[str, Any]] = []
    for match in re.finditer(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s+AS\s*\(", stripped_sql, re.IGNORECASE
    ):
        name = match.group(1)
        if name.lower() in _CTE_STOPWORDS:
            continue
        open_index = stripped_sql.index("(", match.end() - 1)
        close_index = match_paren(stripped_sql, open_index)
        if close_index == -1:
            continue
        ctes.append(
            {
                "name": name,
                "body": stripped_sql[open_index + 1 : close_index],
                "start": match.start(),
            }
        )
    return ctes


def find_derived_subqueries(stripped_sql: str) -> list[dict[str, Any]]:
    """
    Find derived-table subqueries -- a parenthesised SELECT directly after
    FROM or JOIN.

    Deliberately excludes the shapes that are legitimate and would otherwise
    dominate the results:

    - scalar subqueries in a SELECT list or WHERE clause
    - ``EXISTS (...)`` / ``IN (...)`` predicates
    - the sanctioned incremental watermark ``(select max(c) from {{ this }})``

    Only FROM/JOIN position is reported, because that is the shape a CTE or
    ephemeral model should replace.
    """
    out: list[dict[str, Any]] = []
    for match in re.finditer(r"\b(from|join)\s*\(", stripped_sql, re.IGNORECASE):
        open_index = stripped_sql.index("(", match.end() - 1)
        close_index = match_paren(stripped_sql, open_index)
        if close_index == -1:
            continue
        body = stripped_sql[open_index + 1 : close_index]
        if not re.search(r"\bselect\b", body, re.IGNORECASE):
            continue
        if is_watermark_subquery(body):
            continue
        out.append(
            {
                "body": body.strip(),
                "start": match.start(),
                "keyword": match.group(1).lower(),
                "depth": count_nested_selects(body),
            }
        )
    return out


def is_watermark_subquery(body: str) -> bool:
    """
    True for the incremental watermark pattern dbt itself documents:
    ``select max(col) from {{ this }}``.

    Without this guard, every correctly-written incremental model would be
    flagged as using a subquery -- the single largest false-positive source in
    the whole audit.
    """
    if not re.search(r"\bmax\s*\(", body, re.IGNORECASE):
        return False
    return bool(re.search(r"\{\{\s*this\s*\}\}", body)) or "this" in body.lower()


def count_nested_selects(body: str) -> int:
    """How many SELECT keywords appear -- a cheap proxy for nesting depth."""
    return len(re.findall(r"\bselect\b", body, re.IGNORECASE))


# =============================================================================
# Normalisation and fingerprinting
# =============================================================================


def normalize_sql(sql: str) -> str:
    """
    Canonical form for comparing two SQL fragments: comments and strings gone,
    whitespace collapsed, lowercased.

    Used to decide whether a repeated subquery is genuinely the same logic, and
    therefore whether the remediation is "extract to an ephemeral model"
    (reused) or "extract to a CTE" (used once).
    """
    text = strip_comments_and_strings(sql)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def fingerprint(sql: str) -> str:
    """Short stable hash of the normalised SQL, for cross-model grouping."""
    return hashlib.sha256(normalize_sql(sql).encode("utf-8")).hexdigest()[:16]


def significant_lines(sql: str) -> int:
    """Count non-blank, non-comment-only lines."""
    count = 0
    for line in sql.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("--"):
            count += 1
    return count


# =============================================================================
# Macros
# =============================================================================

MACRO_DEF_PATTERN = re.compile(
    r"\{%-?\s*macro\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", re.I
)
TEST_DEF_PATTERN = re.compile(
    r"\{%-?\s*test\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.IGNORECASE
)


def extract_macro_defs(raw: str) -> list[dict[str, Any]]:
    """
    Macro definitions in a file, with name, args, body and line.

    The body runs to the matching ``endmacro`` so a rule can measure how much
    logic the macro actually contains -- the basis for detecting trivial
    wrappers.
    """
    out: list[dict[str, Any]] = []
    for match in MACRO_DEF_PATTERN.finditer(raw):
        end = raw.find("endmacro", match.end())
        body = raw[match.end() : end] if end != -1 else raw[match.end() :]
        args = [a.strip() for a in split_top_level(match.group(2))]
        out.append(
            {
                "name": match.group(1),
                "args": args,
                "body": body,
                "line": find_line_number(raw, match.start()),
            }
        )
    return out


#: Jinja and dbt built-ins that are not user macros; calls to these must never
#: be counted as macro usage or the ratio metrics become meaningless.
JINJA_BUILTINS = {
    "config",
    "ref",
    "source",
    "var",
    "env_var",
    "this",
    "target",
    "is_incremental",
    "log",
    "return",
    "run_query",
    "adapter",
    "exceptions",
    "modules",
    "builtins",
    "dbt_version",
    "invocation_id",
    "selected_resources",
    "graph",
    "print",
    "tojson",
    "fromjson",
    "toyaml",
    "fromyaml",
    "zip",
    "set",
    "range",
    "length",
    "loop",
    "dict",
    "list",
    "str",
    "int",
    "float",
    "bool",
    "none",
    "true",
    "false",
    "if",
    "for",
    "endif",
    "endfor",
    "macro",
    "endmacro",
    "test",
    "endtest",
    "snapshot",
    "endsnapshot",
    "materialization",
    "endmaterialization",
    "call",
    "endcall",
    "statement",
    "endstatement",
    "do",
    "else",
    "elif",
    "and",
    "or",
    "not",
    "in",
    "is",
    "with",
}


def extract_macro_calls(raw: str) -> list[dict[str, Any]]:
    """
    Calls to (probable) user macros, excluding Jinja and dbt built-ins.

    Matches both ``{{ name(...) }}`` expressions and ``{% do name(...) %}``
    statements, and includes dotted package calls such as
    ``dbt_utils.star(...)`` so reimplementation checks can see them.
    """
    out: list[dict[str, Any]] = []
    pattern = re.compile(
        r"\{[{%]-?\s*(?:do\s+)?((?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*)\s*\("
    )
    for match in pattern.finditer(raw):
        name = match.group(1)
        bare = name.split(".")[-1]
        if bare.lower() in JINJA_BUILTINS or name.lower() in JINJA_BUILTINS:
            continue
        out.append(
            {"name": name, "bare": bare, "line": find_line_number(raw, match.start())}
        )
    return out
