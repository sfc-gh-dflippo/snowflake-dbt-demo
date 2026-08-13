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
FIRST_STATEMENT_PATTERN = re.compile(
    r"^[ \t]*(with|select)\b", re.IGNORECASE | re.MULTILINE
)

#: Categories whose suggestions concern configuration rather than query text, so
#: the config block is the most useful place to point.
CONFIG_CATEGORIES = frozenset({"MAT", "INC", "OPS"})

#: Categories whose suggestions concern the schema YAML entry rather than the model.
YAML_CATEGORIES = frozenset({"TST", "DOC"})


def find_column(content: str, position: int) -> int:
    """
    Return the 1-based column of a character offset.

    Columns are only ever derived from an offset a rule actually matched. There is
    no guessing fallback: callers without an offset pass nothing and get 1, which
    is honest, whereas a fabricated column sends the reader to the wrong place.
    """
    if position <= 0:
        return 1
    line_start = content.rfind("\n", 0, position)
    return position - line_start if line_start != -1 else position + 1


def _line_of_offset(content: str, position: int) -> int:
    return content.count("\n", 0, position) + 1


def config_line(model: ModelFile) -> int | None:
    """Line of the model's config block, or its first statement."""
    match = CONFIG_PATTERN.search(model.raw)
    if match:
        return _line_of_offset(model.raw, match.start())
    match = FIRST_STATEMENT_PATTERN.search(model.raw)
    if match:
        return _line_of_offset(model.raw, match.start())
    return None


def first_statement_line(model: ModelFile) -> int | None:
    """Line where the model's query actually begins, skipping header comments."""
    match = FIRST_STATEMENT_PATTERN.search(model.raw)
    if match:
        return _line_of_offset(model.raw, match.start())
    return None


def _yaml_key_line(text: str, key: str, start: int = 0) -> int | None:
    """Line of a ``- name: <key>`` list entry, searching from ``start``."""
    pattern = re.compile(
        rf"^[ \t]*-[ \t]*name[ \t]*:[ \t]*[\"']?{re.escape(key)}[\"']?[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text, start)
    if match is None:
        return None
    return _line_of_offset(text, match.start())


def yaml_model_line(project: ProjectContext, model_name: str) -> int | None:
    """Line of ``- name: <model>`` in the schema file that declares it."""
    relative = project.schema_sources.get(model_name)
    if not relative:
        return None
    text = _read(project.root / relative)
    if text is None:
        return None
    return _yaml_key_line(text, model_name)


def yaml_column_line(
    project: ProjectContext, model_name: str, column: str
) -> int | None:
    """
    Line of a column entry, scoped to its own model.

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
        rf"^[ \t]*-[ \t]*name[ \t]*:[ \t]*[\"']?{re.escape(model_name)}[\"']?[ \t]*$",
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
    line = _yaml_key_line(text[:end], column, model_match.end())
    return line if line else _line_of_offset(text, model_match.start())


def project_yml_line(project: ProjectContext, *keys: str) -> int | None:
    """Line of the last resolvable key in a nested ``dbt_project.yml`` path."""
    text = _read(project.root / "dbt_project.yml")
    if text is None:
        return None
    position = 0
    found: int | None = None
    for key in keys:
        pattern = re.compile(
            rf"^[ \t]*[\"']?\+?{re.escape(key)}[\"']?[ \t]*:", re.MULTILINE
        )
        match = pattern.search(text, position)
        if match is None:
            break
        found = _line_of_offset(text, match.start())
        position = match.end()
    return found


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def resolve_line(suggestion: Any, project: ProjectContext | None) -> int:
    """
    Best available line for a suggestion that did not supply one.

    Dispatches on the target file's type and the rule's category, because those are
    the only two things reliably known at this point. Always returns at least 1, so
    the invariant "every suggestion has a line" holds for the linter.
    """
    if suggestion.line:
        return suggestion.line
    if project is None or not suggestion.file:
        return 1

    target = suggestion.file
    category = suggestion.category

    if target.endswith((".yml", ".yaml")):
        if target.endswith("dbt_project.yml"):
            return project_yml_line(project, "models") or 1
        model_name = _model_name_for(suggestion, project)
        if model_name:
            # ``column_name`` is the SQL column, not a character offset -- the
            # position field on Suggestion is ``column``. The two were once both
            # spelled "column", which made this branch unreachable: the rule's
            # value bound to make_suggestion's position parameter instead of
            # landing in context.
            column = suggestion.context.get("column_name")
            if isinstance(column, str) and column:
                return yaml_column_line(project, model_name, column) or 1
            return yaml_model_line(project, model_name) or 1
        return 1

    model = _model_for_file(project, target)
    if model is None:
        return 1

    if category in YAML_CATEGORIES:
        # The observation is about tests or docs, which live in the schema YAML --
        # but this suggestion points at the model file, so anchor on its config or
        # first statement rather than pretending to know a YAML offset.
        return config_line(model) or 1
    if category in CONFIG_CATEGORIES:
        return config_line(model) or 1
    return first_statement_line(model) or 1


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
