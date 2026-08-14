"""
User-authored waivers: selectively silencing a rule for a file or a line.

Distinct from the two suppression mechanisms that already exist:

- ``disabled_rules`` in ``.dbt-quality.yml`` turns a rule off for the whole run,
  and the rule is reported as *skipped* so the report says what was not checked.
- Migration-tier suppression (``provenance.py``) mutes the ARCHITECTURE tier for
  converted code, and those suggestions are counted and summarised separately.

A waiver is narrower and stronger than either: the reader has looked at this
finding, in this place, and settled it. The suggestion is dropped rather than
reported, so nothing downstream counts it -- see ``engine._collect``.

Three surfaces, deliberately overlapping in capability:

1. ``-- dbt-quality: ignore SSC-EWI-DBTINC0008`` -- the line the diagnostic
   reports, or the line above it.
2. ``-- dbt-quality: ignore-file SSC-EWI-DBTDOC0002`` -- anywhere in the file,
   applying to the whole file.
3. an ``ignore:`` entry in ``.dbt-quality.yml`` -- path glob plus rule list. The
   only surface that can address project- and portfolio-scoped findings, whose
   ``file`` is often a directory or a pseudo-path (``models/``, ``<portfolio>``)
   with nowhere to put a comment.

``*`` in place of a rule list means every rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dbt_quality.discovery import AuditConfig, ProjectContext

#: A waiver directive, in either form.
#:
#: The rule list accepts commas or (horizontal) whitespace as separators, and
#: ``*`` for "every rule". ``ignore-file`` is matched before ``ignore`` in the
#: alternation because a regex alternation is ordered -- with ``ignore`` first,
#: ``ignore-file`` would match as ``ignore`` and leave ``-file`` to be read as a
#: rule id.
#:
#: Every whitespace class here is ``[ \t]`` rather than ``\s`` on purpose: ``\s``
#: matches newlines, and this pattern is applied to a whole file at once by
#: ``blank_directives``. With ``\s`` in the rule-list class, a match starting on
#: one directive line ran past the newline and consumed the ``-- dbt-quality`` of
#: the next directive (all characters are in the class) up to its ``:``, so two
#: consecutive directives collapsed into one match -- the second rule id survived
#: unblanked and was then read as a SnowConvert marker, and the swallowed newline
#: shifted every later line number. Restricting to horizontal whitespace makes a
#: match physically unable to cross a line, so per-line and whole-file scanning
#: agree and offsets are preserved.
#:
#: Intentional simplification: this does not verify the directive sits inside a
#: comment. Comment syntax differs across the file types a suggestion can target
#: (``--`` and ``/* */`` in SQL, ``{# #}`` in Jinja, ``#`` in YAML), and a bare
#: occurrence outside a comment would not parse in any of them, so the file would
#: already be broken for reasons this engine is not responsible for detecting.
DIRECTIVE = re.compile(
    r"dbt-quality[ \t]*:[ \t]*(ignore-file|ignore)[ \t]*[=:]?[ \t]*([A-Za-z0-9\-,* \t]*)",
    re.IGNORECASE,
)

#: Splits the rule list on commas and/or whitespace.
_SEPARATORS = re.compile(r"[,\s]+")

#: Stands in for "every rule" in both a directive and a config entry.
ALL_RULES = "*"


@dataclass
class FileWaivers:
    """The waivers one file declares."""

    #: Rules waived for the whole file, or ``{ALL_RULES}``.
    file_rules: set[str] = field(default_factory=set)
    #: 1-based line -> rules waived at that line, or ``{ALL_RULES}``.
    line_rules: dict[int, set[str]] = field(default_factory=dict)

    def waives(self, rule_id: str, line: int | None) -> bool:
        if _matches(self.file_rules, rule_id):
            return True
        if line is None:
            return False
        return _matches(self.line_rules.get(line, set()), rule_id)


def _matches(rules: set[str], rule_id: str) -> bool:
    """Whether a waived-rule set covers one rule id, case-insensitively."""
    if not rules:
        return False
    return ALL_RULES in rules or rule_id.upper() in rules


def _parse_rule_list(raw: str) -> set[str]:
    """
    Rule ids from a directive's argument.

    Upper-cased so a directive written in lower case still matches; ``*`` is
    passed through untouched. An empty result means the directive named no rules
    -- a truncated ``-- dbt-quality: ignore`` -- and waives nothing, rather than
    being read as a wildcard. Silently widening a malformed directive to "every
    rule" would hide findings the author never intended to waive.
    """
    tokens = {t.strip().upper() for t in _SEPARATORS.split(raw) if t.strip()}
    return {t for t in tokens if t}


def parse_waivers(text: str) -> FileWaivers:
    """
    Read every waiver directive in a file.

    An ``ignore`` directive registers against its own line *and* against the
    first following non-blank line, so both shapes a reader would reach for work:

        select ...  -- dbt-quality: ignore SSC-EWI-DBTSQL0002

        -- dbt-quality: ignore SSC-EWI-DBTSQL0002
        select ...

    The blank-line tolerance matters because a directive is usually written above
    the statement with a blank line between, and requiring adjacency would make
    the feature look unreliable.

    A *trailing* directive -- one with code before it on the same line -- applies
    to its own line only. Extending it forward would silence a finding on the
    following statement that the author never looked at, and an unintended false
    negative is the most expensive thing this mechanism can produce.
    """
    waivers = FileWaivers()
    lines = text.splitlines()

    for index, line in enumerate(lines):
        match = DIRECTIVE.search(line)
        if match is None:
            continue
        form, rules_raw = match.group(1).lower(), match.group(2)
        rules = _parse_rule_list(rules_raw)
        if not rules:
            continue

        if form == "ignore-file":
            waivers.file_rules |= rules
            continue

        for target in _line_targets(lines, index, match.start()):
            waivers.line_rules.setdefault(target, set()).update(rules)

    return waivers


#: Comment openers a directive may sit behind. Text before one of these on the
#: directive's line is code, which makes the directive a trailing one.
_COMMENT_OPENERS = ("--", "/*", "{#", "#")


def _is_trailing(line: str, position: int) -> bool:
    """Whether the directive at ``position`` has code before it on its own line."""
    before = line[:position]
    for opener in _COMMENT_OPENERS:
        head = before.split(opener, 1)[0]
        if opener in before and not head.strip():
            return False
    return bool(before.strip())


def _line_targets(lines: list[str], index: int, position: int) -> list[int]:
    """
    1-based lines an ``ignore`` at 0-based ``index`` applies to.

    Its own line, plus -- for a directive on a line of its own -- the next line
    that carries anything, skipping blanks so a directive separated from its
    statement by an empty line still attaches.
    """
    targets = [index + 1]
    if _is_trailing(lines[index], position):
        return targets
    for offset in range(index + 1, len(lines)):
        if lines[offset].strip():
            targets.append(offset + 1)
            break
    return targets


def blank_directives(text: str) -> str:
    """
    Replace waiver directives with spaces of equal length.

    A waiver names a rule id, and a dbt-quality rule id is spelled exactly like a
    SnowConvert conversion marker (``SSC-EWI-DBTSQL0006`` against
    ``SSC-EWI-SSIS0033``). Two things read the file looking for those markers:

    - ``rules/mig.py`` reports an unresolved marker as an error, so writing a
      waiver would produce a brand-new error-level finding naming the waiver
    - ``provenance.py`` counts markers as evidence of mechanical conversion, so
      waivers accumulating in a hand-written project could flip its verdict to
      lift-and-shift and suppress the entire ARCHITECTURE tier

    Both would be caused by the reader's attempt to silence something, which
    makes them worse than the noise the waiver was written to remove. Blanking
    the directive before those scans is what keeps the mechanism inert.

    The replacement preserves length so every offset the callers compute from the
    result -- line starts, ``span()`` positions, evidence slices -- still lines up
    with the original text.
    """
    return DIRECTIVE.sub(lambda m: " " * len(m.group(0)), text)


def candidate_paths(suggestion: Any, project: ProjectContext | None) -> list[str]:
    """
    The path forms a waiver may name for one suggestion.

    ``suggestion.file`` is not written consistently across the rule packs: most
    rules pass a project-relative path, ``prj.py`` passes one already prefixed
    with ``project.relative_root``, and several pass a pseudo-path such as
    ``models/`` or ``<portfolio>``. A config glob is authored against what the
    user sees in the report, so both forms are offered for matching rather than
    forcing every rule pack to be rewritten.

    Order matters to callers that read a file: the project-relative form is
    first, because that is the one that resolves under ``project.root``.
    """
    raw = suggestion.file
    if not raw:
        return []

    forms = [raw]
    prefix = project.relative_root if project else ""
    if prefix and prefix != ".":
        stripped = f"{prefix}/"
        if raw.startswith(stripped):
            forms.insert(0, raw[len(stripped) :])
        else:
            forms.append(f"{prefix}/{raw}")

    seen: set[str] = set()
    return [f for f in forms if f and not (f in seen or seen.add(f))]


def _config_waives(config: AuditConfig | None, rule_id: str, paths: list[str]) -> bool:
    """Whether any ``ignore:`` entry covers this rule at one of these paths."""
    if config is None or not config.ignores:
        return False
    for entry in config.ignores:
        if not _matches(entry.rule_set, rule_id):
            continue
        for pattern in entry.paths:
            if any(fnmatch(path, pattern) for path in paths):
                return True
    return False


def file_waivers(project: ProjectContext, relative: str) -> FileWaivers:
    """
    Waivers declared by one file, parsed at most once per run.

    Cached on the project rather than in a module-level cache so the lifetime is
    exactly one audit -- there is no question of a stale entry surviving into a
    later run, which matters for the watch task that lints on a timer.
    """
    cached = project.waiver_cache.get(relative)
    if cached is not None:
        return cached

    waivers = FileWaivers()
    path = project.root / relative
    try:
        if path.is_file():
            waivers = parse_waivers(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        # An unreadable file declares no waivers. Discovery already records read
        # errors; failing the audit over one here would be a worse trade.
        pass

    project.waiver_cache[relative] = waivers
    return waivers


def is_waived(
    suggestion: Any, project: ProjectContext | None, config: AuditConfig | None
) -> bool:
    """
    Whether the reader has waived this suggestion.

    Config entries are tested first: they need no file read, and they are the
    only surface that applies when ``project`` is ``None`` (a portfolio-scoped
    rule) or when ``suggestion.file`` names a directory rather than a file.
    """
    paths = candidate_paths(suggestion, project)
    if _config_waives(config, suggestion.rule_id, paths):
        return True
    if project is None or not paths:
        return False

    # candidate_paths puts the project-relative form first; only that one
    # resolves against the project root.
    relative = paths[0]
    if Path(relative).is_absolute():
        return False
    return file_waivers(project, relative).waives(suggestion.rule_id, suggestion.line)
