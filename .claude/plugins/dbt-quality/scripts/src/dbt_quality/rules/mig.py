"""
MIG -- unresolved conversion debt.

These rules fire only where migration provenance was detected, and they are
``Tier.MIGRATION`` so they are never suppressed. That is the deliberate asymmetry
in this audit: detecting that code was machine-converted excuses it from
*architectural* expectations it never chose, but it does not excuse leftover
conversion markers, non-idiomatic ETL control flow, or shipped scaffolding. Those
are defects, and a converted project that still contains them is unfinished.

The conversion tooling documents several of these itself -- unresolved EWIs break
compilation, FDM markers record deliberate behavioural differences awaiting
human sign-off. Surfacing them is the point.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbt_quality.core.base import (
    Effort,
    Kind,
    Level,
    Scope,
    Severity,
    Suggestion,
    Tier,
    make_suggestion,
    plural,
    rule,
)
from dbt_quality.core.sqlutil import span
from dbt_quality.provenance import (
    DD_CONSTANT_PATTERN,
    ETL_CONTROL_COLUMN_PATTERN,
    ETL_INSTANCE_PATTERN,
    FDM_PATTERN,
    NEEDS_USER_PATTERN,
    RESOLVE_EWI_PATTERN,
    STABILIZATION_TAG_PATTERN,
    marker_text,
    needs_user_text,
)

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "MIG"

MIG_RESOLVE_EWI = "SSC-EWI-DBTMIG0001"
MIG_EWI_MARKER = "SSC-EWI-DBTMIG0002"
MIG_FDM_MARKER = "SSC-FDM-DBTMIG0003"
MIG_NEEDS_USER = "SSC-EWI-DBTMIG0004"
MIG_CONTROL_COLUMN = "SSC-FDM-DBTMIG0005"
MIG_SCAFFOLDING = "SSC-EWI-DBTMIG0006"
MIG_ETL_NAMES = "SSC-EWI-DBTMIG0007"
MIG_PLACEHOLDER = "SSC-EWI-DBTMIG0008"

#: EWI codes, excluding the !!!RESOLVE!!! form which MIG001 reports separately.
EWI_CODE_PATTERN = re.compile(r"SSC-EWI-[A-Z]*\d+", re.IGNORECASE)


def _is_migrated(project: ProjectContext) -> bool:
    return bool(project.provenance and project.provenance.is_migration)


@rule(
    MIG_RESOLVE_EWI,
    "Unresolved conversion error blocks compilation",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.CRITICAL,
    rationale=(
        "A `!!!RESOLVE EWI!!!` block is invalid SQL the converter could not translate."
        " The model cannot compile until it is rewritten."
    ),
)
def resolve_ewi(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    for match in RESOLVE_EWI_PATTERN.finditer(model.raw):
        context = model.raw[match.start() : match.start() + 260]
        vendor = marker_text(model.raw, match.end())
        yield make_suggestion(
            MIG_RESOLVE_EWI,
            vendor
            or (
                "This model contains an `!!!RESOLVE EWI!!!` block the converter"
                " could not translate and cannot compile."
            ),
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=re.sub(r"\s+", " ", context).strip(),
            remediation=(
                "Translate the original expression by hand; the marker quotes the"
                " source construct it could not convert. Reimplement it in Snowflake"
                " SQL, delete the marker, and verify with"
                f" `dbt compile --select {model.name}`."
            ),
            effort=Effort.HIGH,
            vendor_text=bool(vendor),
        )


@rule(
    MIG_EWI_MARKER,
    "Conversion error marker left in place",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.HIGH,
    rationale=(
        "An EWI records a construct the converter could not fully translate."
        " The model's output has not been verified against the original source."
    ),
)
def ewi_marker(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    seen: set[tuple[str, str]] = set()
    # Searched in ``without_directives``: a dbt-quality waiver names a rule id
    # spelled exactly like a conversion marker, so scanning ``raw`` would report
    # the reader's own waiver as unresolved conversion debt. The blanking keeps
    # offsets identical, so every slice off ``raw`` below still lines up.
    for match in EWI_CODE_PATTERN.finditer(model.without_directives or model.raw):
        code = match.group(0).upper()
        if RESOLVE_EWI_PATTERN.search(
            model.raw[max(0, match.start() - 40) : match.start()]
        ):
            continue
        # Keyed on (code, text), not the code alone: the converter emits one code
        # with different text per site -- SSC-EWI-SSIS0004 names the specific
        # control-flow element -- and keying on the code would hide all but the
        # first.
        vendor = marker_text(model.raw, match.start())
        if (code, vendor) in seen:
            continue
        seen.add((code, vendor))
        line_start = model.raw.rfind("\n", 0, match.start()) + 1
        line_end = model.raw.find("\n", match.end())
        yield make_suggestion(
            MIG_EWI_MARKER,
            vendor
            or (
                f"This model carries an unresolved `{code}` marker for a construct"
                " the converter could not translate."
            ),
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=model.raw[
                line_start : line_end if line_end != -1 else len(model.raw)
            ].strip()[:200],
            remediation=(
                "Look up the code in the conversion tool's EWI reference and verify"
                " the model against the source system's output. Remove the marker once"
                " the output is verified, and add a test to pin the validated"
                " behaviour."
            ),
            effort=Effort.MEDIUM,
            code=code,
            vendor_text=bool(vendor),
        )


@rule(
    MIG_FDM_MARKER,
    "Functional-difference marker awaiting sign-off",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    kind=Kind.FDM,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "An FDM records a deliberate behavioural difference from the source platform,"
        " commonly in ordering or NULL handling. It compiles and runs, which is exactly"
        " why it gets forgotten."
    ),
)
def fdm_marker(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    seen: set[tuple[str, str]] = set()
    # See ``ewi_marker``: scanned without waiver directives, which are spelled
    # like markers.
    for match in FDM_PATTERN.finditer(model.without_directives or model.raw):
        code = match.group(0).upper()
        vendor = marker_text(model.raw, match.start())
        if (code, vendor) in seen:
            continue
        seen.add((code, vendor))
        line_start = model.raw.rfind("\n", 0, match.start()) + 1
        line_end = model.raw.find("\n", match.end())
        yield make_suggestion(
            MIG_FDM_MARKER,
            vendor
            or (
                f"The `{code}` marker records a deliberate behavioural difference"
                " from the source platform that has not been signed off."
            ),
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=model.raw[
                line_start : line_end if line_end != -1 else len(model.raw)
            ].strip()[:220],
            remediation=(
                "Decide whether the difference is acceptable. For ordering or"
                " deduplication differences, supply a deterministic `order by`;"
                " SQL008 suggestions usually pair with these markers. Record the"
                " decision in the model description and note the sign-off beside"
                " the marker."
            ),
            effort=Effort.MEDIUM,
            code=code,
            vendor_text=bool(vendor),
        )


@rule(
    MIG_NEEDS_USER,
    "Explicit hand-off marker left unresolved",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.HIGH,
    rationale=(
        "A `NEEDS-USER` marker is an explicit statement that a required conversion"
        " step has not yet been completed."
    ),
)
def needs_user(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    for match in NEEDS_USER_PATTERN.finditer(model.raw):
        line_end = model.raw.find("\n", match.end())
        vendor = needs_user_text(model.raw, match.start())
        yield make_suggestion(
            MIG_NEEDS_USER,
            vendor
            or (
                "An unresolved `NEEDS-USER` marker records an incomplete required"
                " conversion step."
            ),
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=model.raw[
                match.start() : line_end if line_end != -1 else len(model.raw)
            ].strip()[:200],
            remediation="Complete the described step and delete the marker.",
            effort=Effort.MEDIUM,
            vendor_text=bool(vendor),
        )


@rule(
    MIG_CONTROL_COLUMN,
    "ETL control flag threaded through models",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    kind=Kind.FDM,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "A row-level DML decision column is how the source ETL tool expressed"
        " insert/update/delete intent. In dbt that decision belongs to the"
        " materialization, not to a string column filtered by inequality."
    ),
)
def control_column(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    match = ETL_CONTROL_COLUMN_PATTERN.search(
        model.stripped
    ) or DD_CONSTANT_PATTERN.search(model.stripped)
    if not match:
        return
    yield make_suggestion(
        MIG_CONTROL_COLUMN,
        "This model references an ETL DML-decision column or `DD_*` constant"
        " from the source pipeline.",
        file=model.relative_path,
        **span(model.stripped, match.start(), match.end()),
        evidence=match.group(0),
        remediation=(
            "Express insert, update, and delete intent through dbt materializations."
            " Use `incremental_strategy='merge'` with a `unique_key` for inserts"
            " and updates; filter rejected rows in the model; represent deletions as"
            " a soft-delete flag. Drop the column from the output once it no longer"
            " drives behaviour."
        ),
        effort=Effort.HIGH,
    )


@rule(
    MIG_ETL_NAMES,
    "Models named after ETL transformation instances",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Names like `int_UPDTRANS` or `stg_raw__SQ_EMPLOYEE` carry the source tool's"
        " internal instance identifiers into the warehouse, where consumers cannot"
        " interpret them."
    ),
)
def etl_names(project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    affected = [m for m in project.models if ETL_INSTANCE_PATTERN.match(m.name)]
    if not affected:
        return
    names = sorted(m.name for m in affected)
    yield make_suggestion(
        MIG_ETL_NAMES,
        f"{plural(len(names), 'model')} "
        f"{'retains' if len(names) == 1 else 'retain'} "
        "ETL transformation-instance prefixes:"
        f" {', '.join(names[:6])}" + (" ..." if len(names) > 6 else "") + ".",
        file=affected[0].relative_path,
        evidence=", ".join(names[:10]),
        remediation=(
            "Rename to describe the business entity each model produces. Do this"
            " alongside collapsing per-transformation chains (see MAT003 findings);"
            " after collapsing, there are far fewer names to choose. Use `alias` if"
            " a consumer depends on the current relation name during the transition."
        ),
        effort=Effort.HIGH,
        models=names,
    )


@rule(
    MIG_SCAFFOLDING,
    "Conversion scaffolding shipped in the project",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.MEDIUM,
    rationale=(
        "Stabilization artifacts verify one-time convergence with the source model."
        " Left in place, they imply test coverage that does not hold for new data"
        " or changed business logic."
    ),
)
def scaffolding(project: ProjectContext) -> Iterator[Suggestion]:
    if not _is_migrated(project):
        return
    hits: list[str] = []
    if STABILIZATION_TAG_PATTERN.search(str(project.project_yml)):
        hits.append("dbt_project.yml")
    for path, raw in project.singular_tests:
        if STABILIZATION_TAG_PATTERN.search(raw):
            try:
                hits.append(str(path.relative_to(project.root)))
            except ValueError:
                hits.append(str(path))
    for model in project.models:
        if STABILIZATION_TAG_PATTERN.search(model.raw):
            hits.append(model.relative_path)
    if not hits:
        return
    yield make_suggestion(
        MIG_SCAFFOLDING,
        f"{plural(len(hits), 'location')} "
        f"{'still carries' if len(hits) == 1 else 'still carry'} "
        "conversion-stabilization scaffolding:"
        f" {', '.join(hits[:5])}" + (" ..." if len(hits) > 5 else "") + ".",
        file=hits[0],
        evidence=", ".join(hits[:8]),
        remediation=(
            "Remove the scaffolding and replace it with primary-key, foreign-key,"
            " and business-rule tests that hold for any input. See the TST findings"
            " for a starting point."
        ),
        effort=Effort.MEDIUM,
        locations=hits,
    )


#: Substrings indicating a model is a conversion placeholder rather than real
#: logic. Deliberately stricter than the version in the retired dbt-validation
#: package: that one matched the bare word "placeholder" anywhere in a file, so
#: any comment mentioning it counted, and matched "null::" which fires on an
#: ordinary `null::integer` cast. Both are anchored here.
PLACEHOLDER_PATTERNS = (
    re.compile(r"^\s*--\s*status:\s*placeholder", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*--\s*awaiting\s+logic\s+conversion", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*--\s*todo:\s*(implement|convert)", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\bwhere\s+false\b", re.IGNORECASE),
)

#: A tag the conversion tooling applies to scaffolded placeholder models.
PLACEHOLDER_TAG = re.compile(r"placeholder", re.IGNORECASE)


def _is_placeholder(model: ModelFile) -> str:
    """Return the matched placeholder evidence, or empty string if not one."""
    tags = model.effective_config.get("tags")
    if tags:
        tag_list = tags if isinstance(tags, list) else [tags]
        for tag in tag_list:
            if PLACEHOLDER_TAG.fullmatch(str(tag).strip()):
                return f"tags={tag_list}"
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(
            model.stripped if pattern.pattern.startswith(r"\bwhere") else model.raw
        )
        if match:
            return match.group(0).strip()
    return ""


@rule(
    MIG_PLACEHOLDER,
    "Conversion placeholder model still in place",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.MIGRATION,
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.CRITICAL,
    rationale=(
        "A placeholder produces an empty table. Downstream models return nothing,"
        " tests pass vacuously, and dashboards show zero with no error, so an"
        " unconverted model can reach production silently."
    ),
)
def placeholder_models(project: ProjectContext) -> Iterator[Suggestion]:
    """
    Carried over from the retired dbt-validation ``migration/checker.py``.

    Reports placeholders individually and adds a completion figure, which is the
    number a migration is actually steered by.
    """
    if not _is_migrated(project):
        return

    placeholders = [(m, _is_placeholder(m)) for m in project.models]
    placeholders = [(m, ev) for m, ev in placeholders if ev]
    if not placeholders:
        return

    total = len(project.models)
    complete = total - len(placeholders)
    percentage = (complete / total * 100) if total else 100.0

    for model, evidence in placeholders:
        yield make_suggestion(
            MIG_PLACEHOLDER,
            "This model is a conversion placeholder that builds but returns no rows.",
            file=model.relative_path,
            evidence=evidence[:160],
            remediation=(
                "Convert the original logic, or remove the model and all `ref()`s"
                " to it until it is ready. An empty table silently returns nothing"
                " while a missing one raises an error."
            ),
            effort=Effort.HIGH,
            completion_percentage=round(percentage, 1),
            placeholder_count=len(placeholders),
            model_total=total,
        )
