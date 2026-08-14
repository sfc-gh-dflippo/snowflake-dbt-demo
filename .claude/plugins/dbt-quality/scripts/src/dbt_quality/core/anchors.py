"""
Line and column attribution for suggestions.

A suggestion without a line number is not actionable in an editor, and this engine
feeds a linter. Most rules know exactly where they looked -- they matched a regex
and have a character offset -- but a large minority reason about *config* or about
a model's *schema entry*, where there is no single offset to point at.

Rather than force every rule to invent one, this module resolves an anchor from
what the suggestion already carries: the target file, and the rule's category. Two
layers cooperate:

1. rules that know an offset pass ``line=`` explicitly and are left alone
2. everything else is resolved here, so no suggestion ever ships a null line

The distinction that matters is between *precision* and *honesty*. Pointing at the
``{{ config() }}`` block for a materialization suggestion is precise. Pointing at
line 1 for a whole-model observation is merely honest -- but it is still better than
null, because an editor can open the file at all. What this module never does is
invent a plausible-looking line it cannot justify; unresolvable falls back to 1.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from dbt_quality.core.sqlutil import line_col

if TYPE_CHECKING:
    from pathlib import Path

    from dbt_quality.discovery import ModelFile, ProjectContext

#: The opening of a dbt config block, in either the Jinja or Python model form.
CONFIG_PATTERN = re.compile(r"\{\{\s*config\s*\(|dbt\.config\s*\(", re.IGNORECASE)

#: The first statement of a model, used when nothing more specific applies. Matches
#: ``with`` as well as ``select`` because a CTE chain starts with the former.
#:
#: Indentation is ``[ \t]*`` rather than ``\s*`` throughout this module: ``\s``
#: matches newlines, so ``^\s*`` happily consumes preceding blank lines and reports
#: the position of the blank line instead of the match.
#:
#: Because the pattern is anchored at the line start, the *column* must come from
#: group 1 rather than ``match.start()`` -- the latter is the start of the
#: indentation, which is column 1 on every line and tells the reader nothing.
FIRST_STATEMENT_PATTERN = re.compile(
    r"^[ \t]*(with|select)\b", re.IGNORECASE | re.MULTILINE
)

#: Categories whose suggestions concern configuration rather than query text, so
#: the config block is the most useful place to point.
CONFIG_CATEGORIES = frozenset({"MAT", "INC", "OPS"})

#: Categories whose suggestions concern the schema YAML entry rather than the model.
YAML_CATEGORIES = frozenset({"TST", "DOC"})


def config_position(model: ModelFile) -> tuple[int, int] | None:
    """Position of the model's config block, or of its first statement."""
    match = CONFIG_PATTERN.search(model.raw)
    if match:
        return line_col(model.raw, match.start())
    match = FIRST_STATEMENT_PATTERN.search(model.raw)
    if match:
        return line_col(model.raw, match.start(1))
    return None


def first_statement_position(model: ModelFile) -> tuple[int, int] | None:
    """Position where the model's query begins, skipping header comments."""
    match = FIRST_STATEMENT_PATTERN.search(model.raw)
    if match:
        return line_col(model.raw, match.start(1))
    return None


def _yaml_key_position(text: str, key: str, start: int = 0) -> tuple[int, int] | None:
    """
    Position of a ``- name: <key>`` list entry, searching from ``start``.

    The column is that of the key itself, taken from group 1. Using
    ``match.start()`` would report the start of the indentation -- column 1 on
    every line, which is no more useful than having no column at all.
    """
    pattern = re.compile(
        rf"^[ \t]*-[ \t]*name[ \t]*:[ \t]*[\"']?({re.escape(key)})[\"']?[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text, start)
    if match is None:
        return None
    return line_col(text, match.start(1))


def yaml_model_position(
    project: ProjectContext, model_name: str
) -> tuple[int, int] | None:
    """Position of ``- name: <model>`` in the schema file that declares it."""
    relative = project.schema_sources.get(model_name)
    if not relative:
        return None
    text = _read(project.root / relative)
    if text is None:
        return None
    return _yaml_key_position(text, model_name)


def yaml_column_position(
    project: ProjectContext, model_name: str, column: str
) -> tuple[int, int] | None:
    """
    Position of a column entry, scoped to its own model.

    Scoping matters: column names repeat across models in a shared schema file, so
    an unscoped search lands on whichever model happens to come first.
    """
    relative = project.schema_sources.get(model_name)
    if not relative:
        return None
    text = _read(project.root / relative)
    if text is None:
        return None
    model_pattern = re.compile(
        rf"^[ \t]*-[ \t]*name[ \t]*:[ \t]*[\"']?({re.escape(model_name)})[\"']?[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    )
    model_match = model_pattern.search(text)
    if model_match is None:
        return None
    # Bound the search at the next model entry so a miss cannot silently walk into
    # the following model's columns.
    next_model = re.compile(r"^[ \t]{0,4}-[ \t]*name[ \t]*:", re.MULTILINE).search(
        text, model_match.end()
    )
    end = next_model.start() if next_model else len(text)
    found = _yaml_key_position(text[:end], column, model_match.end())
    return found if found else line_col(text, model_match.start(1))


def project_yml_position(project: ProjectContext, *keys: str) -> tuple[int, int] | None:
    """Position of the last resolvable key in a nested ``dbt_project.yml`` path."""
    text = _read(project.root / "dbt_project.yml")
    if text is None:
        return None
    position = 0
    found: tuple[int, int] | None = None
    for key in keys:
        pattern = re.compile(
            rf"^[ \t]*[\"']?\+?({re.escape(key)})[\"']?[ \t]*:", re.MULTILINE
        )
        match = pattern.search(text, position)
        if match is None:
            break
        found = line_col(text, match.start(1))
        position = match.end()
    return found


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def resolve_position(
    suggestion: Any, project: ProjectContext | None
) -> tuple[int, int | None]:
    """
    Best available ``(line, column)`` for a suggestion that did not supply one.

    Dispatches on the target file's type and the rule's category, because those are
    the only two things reliably known at this point. The line is always at least 1,
    so the invariant "every suggestion has a line" holds for the linter.

    Three cases, and the middle one is the one that matters:

    - a rule supplied a column: it owns the whole position, returned untouched
    - a rule supplied a line but no column: return ``(line, None)``. **Never
      fabricate a column here.** The anchor's column belongs to the anchor's line,
      and pairing it with the rule's line points at a character on a different
      line -- worse than column 1, because it looks precise and is wrong.
    - a rule supplied neither: resolve both from the anchor, as an atomic pair

    A column is only ever derived from an offset something actually matched. There
    is no guessing fallback: unresolvable yields column ``None``, which renders as
    1, whereas a fabricated column sends the reader to the wrong place.
    """
    if suggestion.column is not None:
        return suggestion.line or 1, suggestion.column
    if suggestion.line:
        return suggestion.line, None
    if project is None or not suggestion.file:
        return 1, None

    target = suggestion.file
    category = suggestion.category

    if target.endswith((".yml", ".yaml")):
        if target.endswith("dbt_project.yml"):
            # Rules that know which key they are complaining about pass a
            # ``yaml_keys`` path; the rest fall back to ``models``. Without this a
            # `+store_failures` or `on-run-end` finding anchored at `models:`,
            # which is honest about the file and wrong about the place.
            keys = suggestion.context.get("yaml_keys") or ("models",)
            if isinstance(keys, str):
                keys = (keys,)
            return _or_line_one(project_yml_position(project, *keys))
        model_name = _model_name_for(suggestion, project)
        if model_name:
            # ``column_name`` is the SQL column, not a character offset -- the
            # position field on Suggestion is ``column``. The two were once both
            # spelled "column", which made this branch unreachable: the rule's
            # value bound to make_suggestion's position parameter instead of
            # landing in context.
            column = suggestion.context.get("column_name")
            if isinstance(column, str) and column:
                return _or_line_one(yaml_column_position(project, model_name, column))
            return _or_line_one(yaml_model_position(project, model_name))
        return 1, None

    model = _model_for_file(project, target)
    if model is None:
        # A directory or pseudo-path: ``models/``, ``macros/``, ``<portfolio>``.
        # There is no file to hold a position, so line 1 with no column is the
        # whole truth. Do not "fix" this by pointing at an arbitrary member file.
        return 1, None

    if category in YAML_CATEGORIES:
        # A TST or DOC suggestion reaching here has no schema entry to point at --
        # the rules target the schema YAML when one exists (see
        # ``project.schema_sources`` in the DOC and TST packs) and fall back to the
        # model file when it does not. Anchor on the model's config or first
        # statement rather than pretending to know a YAML offset.
        return _or_line_one(config_position(model))
    if category in CONFIG_CATEGORIES:
        return _or_line_one(config_position(model))
    return _or_line_one(first_statement_position(model))


def _or_line_one(found: tuple[int, int] | None) -> tuple[int, int | None]:
    """Unresolvable anchors fall back to line 1 with no column, never a guess."""
    return found if found is not None else (1, None)


def _model_for_file(project: ProjectContext, relative: str) -> ModelFile | None:
    for model in project.models:
        if model.relative_path == relative:
            return model
    return None


def _model_name_for(suggestion: Any, project: ProjectContext) -> str:
    """Recover the model a YAML-targeted suggestion is about."""
    name = suggestion.context.get("model")
    if isinstance(name, str) and name:
        return name
    # Fall back to whichever model this schema file declares, when unambiguous.
    declared = [
        n for n, src in project.schema_sources.items() if src == suggestion.file
    ]
    return declared[0] if len(declared) == 1 else ""
