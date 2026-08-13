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

from dbt_audit.core.base import (
    Effort,
    Finding,
    Scope,
    Severity,
    Tier,
    make_finding,
    rule,
)
from dbt_audit.core.sqlutil import find_line_number
from dbt_audit.provenance import (
    DD_CONSTANT_PATTERN,
    ETL_CONTROL_COLUMN_PATTERN,
    ETL_INSTANCE_PATTERN,
    FDM_PATTERN,
    NEEDS_USER_PATTERN,
    RESOLVE_EWI_PATTERN,
    STABILIZATION_TAG_PATTERN,
)

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "MIG"

MIG_RESOLVE_EWI = "MIG001"
MIG_EWI_MARKER = "MIG002"
MIG_FDM_MARKER = "MIG003"
MIG_NEEDS_USER = "MIG004"
MIG_CONTROL_COLUMN = "MIG005"
MIG_SCAFFOLDING = "MIG006"
MIG_ETL_NAMES = "MIG007"

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
    severity=Severity.ERROR,
    rationale=(
        "A !!!RESOLVE EWI!!! block is invalid SQL the converter could not translate. The "
        "model cannot compile, so every downstream model, test and doc is unreachable."
    ),
)
def resolve_ewi(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    for match in RESOLVE_EWI_PATTERN.finditer(model.raw):
        context = model.raw[match.start() : match.start() + 260]
        yield make_finding(
            MIG_RESOLVE_EWI,
            "Model contains an unresolved conversion block, so it cannot compile.",
            file=model.relative_path,
            line=find_line_number(model.raw, match.start()),
            evidence=re.sub(r"\s+", " ", context).strip(),
            remediation=(
                "Translate the original expression by hand. The marker quotes the "
                "source-platform expression it could not convert -- reimplement it in "
                "Snowflake SQL, then delete the marker. Verify with "
                f"`dbt compile --select {model.name}` before moving on."
            ),
            effort=Effort.HIGH,
        )


@rule(
    MIG_EWI_MARKER,
    "Conversion error marker left in place",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    severity=Severity.WARNING,
    rationale=(
        "An EWI marks something the converter could not fully translate. Left in place, "
        "it means nobody has confirmed the model produces what the source produced."
    ),
)
def ewi_marker(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    seen: set[str] = set()
    for match in EWI_CODE_PATTERN.finditer(model.raw):
        code = match.group(0).upper()
        if code in seen or RESOLVE_EWI_PATTERN.search(
            model.raw[max(0, match.start() - 40) : match.start()]
        ):
            continue
        seen.add(code)
        line_start = model.raw.rfind("\n", 0, match.start()) + 1
        line_end = model.raw.find("\n", match.end())
        yield make_finding(
            MIG_EWI_MARKER,
            f"Conversion warning `{code}` is still present, so this model's fidelity to "
            "the original has not been confirmed.",
            file=model.relative_path,
            line=find_line_number(model.raw, match.start()),
            evidence=model.raw[
                line_start : line_end if line_end != -1 else len(model.raw)
            ].strip()[:200],
            remediation=(
                "Look up the code in the conversion tool's EWI reference, verify the "
                "model against the source system's output for the same input, then "
                "remove the marker. Add a test that pins the behaviour you verified so "
                "the check is not one-off."
            ),
            effort=Effort.MEDIUM,
            code=code,
        )


@rule(
    MIG_FDM_MARKER,
    "Functional-difference marker awaiting sign-off",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    severity=Severity.WARNING,
    rationale=(
        "An FDM records a deliberate behavioural difference from the source platform -- "
        "commonly non-deterministic ordering or NULL handling. It compiles and runs, "
        "which is exactly why it gets forgotten."
    ),
)
def fdm_marker(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    seen: set[str] = set()
    for match in FDM_PATTERN.finditer(model.raw):
        code = match.group(0).upper()
        if code in seen:
            continue
        seen.add(code)
        line_start = model.raw.rfind("\n", 0, match.start()) + 1
        line_end = model.raw.find("\n", match.end())
        yield make_finding(
            MIG_FDM_MARKER,
            f"`{code}` documents a behavioural difference from the source platform that "
            "has not been signed off.",
            file=model.relative_path,
            line=find_line_number(model.raw, match.start()),
            evidence=model.raw[
                line_start : line_end if line_end != -1 else len(model.raw)
            ].strip()[:220],
            remediation=(
                "Decide explicitly whether the difference is acceptable. Where it "
                "concerns row ordering or deduplication, supply a deterministic ORDER BY "
                "-- see the SQL008 findings, which usually pair with these markers. "
                "Record the decision in the model description; keep the marker comment "
                "if the tooling relies on it, but note the sign-off beside it."
            ),
            effort=Effort.MEDIUM,
            code=code,
        )


@rule(
    MIG_NEEDS_USER,
    "Explicit hand-off marker left unresolved",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    severity=Severity.ERROR,
    rationale=(
        "A NEEDS-USER marker is an explicit statement that a human has not yet done a "
        "required step."
    ),
)
def needs_user(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    for match in NEEDS_USER_PATTERN.finditer(model.raw):
        line_end = model.raw.find("\n", match.end())
        yield make_finding(
            MIG_NEEDS_USER,
            "Model carries a NEEDS-USER hand-off marker that has not been actioned.",
            file=model.relative_path,
            line=find_line_number(model.raw, match.start()),
            evidence=model.raw[
                match.start() : line_end if line_end != -1 else len(model.raw)
            ].strip()[:200],
            remediation="Complete the described step and delete the marker.",
            effort=Effort.MEDIUM,
        )


@rule(
    MIG_CONTROL_COLUMN,
    "ETL control flag threaded through models",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.MIGRATION,
    severity=Severity.WARNING,
    rationale=(
        "A row-level DML decision column is how the source ETL tool expressed "
        "insert/update/delete intent. In dbt that decision belongs to the "
        "materialization, not to a string column filtered by inequality."
    ),
)
def control_column(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    match = ETL_CONTROL_COLUMN_PATTERN.search(
        model.stripped
    ) or DD_CONSTANT_PATTERN.search(model.stripped)
    if not match:
        return
    yield make_finding(
        MIG_CONTROL_COLUMN,
        "Model carries an ETL DML-decision column (or its DD_* constants), so load "
        "behaviour is encoded in row data rather than in the materialization.",
        file=model.relative_path,
        line=find_line_number(model.stripped, match.start()),
        evidence=match.group(0),
        remediation=(
            "Express the intent through dbt instead. Rows to insert or update become "
            "the model's output with `incremental_strategy='merge'` and a `unique_key`; "
            "rejected rows are filtered out in the model; deletions become a "
            "soft-delete flag the merge acts on. Once the flag no longer drives "
            "behaviour, drop it from the output rather than passing it downstream."
        ),
        effort=Effort.HIGH,
    )


@rule(
    MIG_ETL_NAMES,
    "Models named after ETL transformation instances",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.MIGRATION,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Names like int_UPDTRANS or stg_raw__SQ_EMPLOYEE carry the source tool's "
        "internal instance identifiers into the warehouse, where consumers have no way "
        "to interpret them."
    ),
)
def etl_names(project: ProjectContext) -> Iterator[Finding]:
    if not _is_migrated(project):
        return
    affected = [m for m in project.models if ETL_INSTANCE_PATTERN.match(m.name)]
    if not affected:
        return
    names = sorted(m.name for m in affected)
    yield make_finding(
        MIG_ETL_NAMES,
        f"{len(names)} model(s) are named after source-tool transformation instances: "
        f"{', '.join(names[:6])}" + (" ..." if len(names) > 6 else "") + ".",
        file=affected[0].relative_path,
        evidence=", ".join(names[:10]),
        remediation=(
            "Rename to describe the business entity each model produces. Do this "
            "alongside collapsing per-transformation model chains (see the MAT003 "
            "findings) -- the two refactors touch the same files, and after collapsing "
            "there are far fewer names to choose. Use `alias` if a consumer depends on "
            "the current relation name during the transition."
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
    severity=Severity.WARNING,
    rationale=(
        "Stabilization test artifacts are a convergence gate for the conversion, not a "
        "test suite. Left in the project they suggest coverage that does not exist, "
        "because their assertions are deliberately limited to single-model checks."
    ),
)
def scaffolding(project: ProjectContext) -> Iterator[Finding]:
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
    yield make_finding(
        MIG_SCAFFOLDING,
        f"Conversion scaffolding is still present in {len(hits)} location(s): "
        f"{', '.join(hits[:5])}" + (" ..." if len(hits) > 5 else "") + ".",
        file=hits[0],
        evidence=", ".join(hits[:8]),
        remediation=(
            "Remove the scaffolding and replace it with a real test suite. Conversion "
            "tests verify that the migrated model matches the old one for one input; "
            "ongoing quality needs primary-key, foreign-key and business-rule tests that "
            "hold for any input. See the TST findings for where to start."
        ),
        effort=Effort.MEDIUM,
        locations=hits,
    )
