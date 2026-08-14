"""
INC -- load patterns and incremental correctness.

The pack that catches teams doing ETL-era loading inside dbt: truncating a table
in a hook and reloading it, deleting a date range and re-inserting, or
materializing as ``table`` while hand-rolling a date window that dbt's
incremental materialization exists to manage.

All UNIVERSAL. A truncate-and-load is wrong whether a person wrote it or a
converter emitted it, so nothing here is suppressed for migrated projects.
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
    make_suggestion,
    rule,
)
from dbt_quality.core.sqlutil import (
    config_hooks,
    span,
    strip_comments_and_strings,
)

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "INC"

INC_TRUNCATE_LOAD = "SSC-EWI-DBTINC0001"
INC_DELETE_LOAD = "SSC-EWI-DBTINC0002"
INC_FOLDER_HOOK_DML = "SSC-EWI-DBTINC0003"
INC_MANUAL_INCREMENTAL = "SSC-PRF-DBTINC0004"
INC_FULL_RELOAD = "SSC-PRF-DBTINC0005"
INC_NO_GUARD = "SSC-PRF-DBTINC0006"
INC_NO_UNIQUE_KEY = "SSC-FDM-DBTINC0007"
INC_NO_STRATEGY = "SSC-EWI-DBTINC0008"
INC_NO_WATERMARK = "SSC-PRF-DBTINC0009"
INC_HOOK_WRITES_ELSEWHERE = "SSC-EWI-DBTINC0010"
INC_MERGE_EXCLUDE_MISMATCH = "SSC-FDM-DBTINC0011"
INC_APPEND_ON_MUTABLE = "SSC-FDM-DBTINC0012"
INC_UNBOUNDED_SCAN = "SSC-PRF-DBTINC0013"
INC_EXTERNAL_LOADER = "SSC-EWI-DBTINC0015"

# --- patterns ---------------------------------------------------------------

# The captured group is the remainder of the statement, not a single token,
# because the target is very often `{{ this }}` -- a `\S+` capture stops at the
# space inside the Jinja braces and yields a useless `{{`. `_dml_target` then
# extracts the real relation from the captured text.
TRUNCATE_PATTERN = re.compile(
    r"\btruncate\s+(?:table\s+)?(?:if\s+exists\s+)?(.{0,120})", re.IGNORECASE
)
DELETE_PATTERN = re.compile(r"\bdelete\s+from\s+(.{0,120})", re.IGNORECASE)
DROP_PATTERN = re.compile(
    r"\bdrop\s+table\s+(?:if\s+exists\s+)?(.{0,120})", re.IGNORECASE
)
INSERT_PATTERN = re.compile(
    r"\b(insert\s+into|merge\s+into)\s+(.{0,120})", re.IGNORECASE
)
THIS_PATTERN = re.compile(r"\{\{\s*this\s*\}\}", re.IGNORECASE)
IS_INCREMENTAL_PATTERN = re.compile(r"\bis_incremental\s*\(\s*\)", re.IGNORECASE)

#: Relative date-window expressions that indicate a hand-rolled incremental.
DATE_WINDOW_PATTERN = re.compile(
    r"\b(?:dateadd|date_sub|date_add|datediff|current_date|current_timestamp|sysdate|getdate)\b",
    re.IGNORECASE,
)
#: A WHERE/AND predicate comparing a date-ish column with >= or >.
DATE_PREDICATE_PATTERN = re.compile(
    r"\b(?:where|and)\s+[\w.\"]*(?:date|dt|day|ts|timestamp|updated|modified|created|load)"
    r"[\w.\"]*\s*(?:>=|>)",
    re.IGNORECASE,
)

FULL_RELOAD_NAME_PATTERN = re.compile(
    r"(_full_reload|_full_refresh|_truncate_load|_trunc_load|_reload|_rebuild)$",
    re.IGNORECASE,
)

#: Columns whose presence implies rows change after insert, so append is unsafe.
MUTABLE_COLUMN_PATTERN = re.compile(
    r"\b(?:as\s+)?(updated_at|updated_date|modified_at|modified_date|last_modified|"
    r"status|order_status|is_active|is_current|is_deleted|valid_to|dbt_valid_to|"
    r"effective_to|end_date)\b",
    re.IGNORECASE,
)

#: Snowflake streams track their own consumption offset, so a model reading one
#: needs no {{ this }} watermark -- the stream only ever yields unconsumed rows.
#: Flagging these as missing a watermark is wrong, and the CDC models it hits are
#: exactly the ones whose authors know incremental loading best.
STREAM_PATTERN = re.compile(
    r"metadata\$action|metadata\$isupdate|metadata\$row_id|\bstream\b", re.IGNORECASE
)

#: A model whose columns come out of a macro cannot be checked by a text scan --
#: the column list does not exist until compile time.
MACRO_CALL_PATTERN = re.compile(
    r"\{\{-?\s*(?!config|ref|source|var|env_var|this|target|is_incremental)[a-z_][\w.]*\s*\(",
    re.IGNORECASE,
)


def _reads_stream(model: ModelFile) -> bool:
    """Whether the model appears to consume a Snowflake stream."""
    if STREAM_PATTERN.search(model.stripped):
        return True
    return any("stream" in name.lower() for name in (*model.refs, model.name))


def _is_microbatch(model: ModelFile) -> bool:
    """Whether the model uses the microbatch incremental strategy."""
    return (
        str(model.effective_config.get("incremental_strategy", "")).lower()
        == "microbatch"
    )


STRATEGIES_NEEDING_KEY = {"merge", "delete+insert"}
VALID_STRATEGIES = {
    "merge",
    "append",
    "delete+insert",
    "insert_overwrite",
    "microbatch",
}


def _dml_target(text: str) -> str:
    """
    Extract the relation a DML statement targets from the text following its verb.

    Handles the two shapes that actually occur: a Jinja expression such as
    ``{{ this }}`` or ``{{ ref('x') }}``, and a plain (optionally qualified)
    identifier. Returning the whole Jinja expression rather than its first token
    is what makes ``{{ this }}`` detectable at all.
    """
    text = text.strip()
    if text.startswith("{{"):
        close = text.find("}}")
        return text[: close + 2] if close != -1 else text
    match = re.match(r'[\w.$"`\[\]]+', text)
    return match.group(0) if match else text


def _targets_self(text: str, model: ModelFile) -> bool:
    """Whether a DML statement's target is the model's own relation."""
    target = _dml_target(text)
    if THIS_PATTERN.search(target):
        return True
    normalized = target.strip().strip("();\"'`[]").lower()
    if normalized == "this":
        return True
    return normalized.split(".")[-1] == model.name.lower()


# =============================================================================
# Hook-based load patterns
# =============================================================================


@rule(
    INC_TRUNCATE_LOAD,
    "Truncate-and-load instead of an incremental model",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.CRITICAL,
    rationale=(
        "dbt rebuilds a table declaratively. Truncating the relation in a hook "
        "reimplements ETL-era batch loading and leaves the table empty if the model "
        "then fails."
    ),
)
def truncate_and_load(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    for key, body in config_hooks(model.effective_config):
        for match in TRUNCATE_PATTERN.finditer(body):
            if not _targets_self(match.group(1), model):
                continue
            yield make_suggestion(
                INC_TRUNCATE_LOAD,
                f"`{key}` truncates this model's own relation before dbt rebuilds it, "
                "so a failed run leaves the table empty.",
                file=model.relative_path,
                evidence=f'{key}="{body.strip()[:180]}"',
                remediation=(
                    "Delete the hook. If the goal is a periodic clean rebuild, use "
                    "`materialized='table'` and let dbt replace the relation "
                    "atomically; "
                    "if the goal is loading only new rows, convert the model to "
                    "`materialized='incremental'` with a `unique_key` and an "
                    "`is_incremental()` guard."
                ),
                effort=Effort.MEDIUM,
            )
        for match in DROP_PATTERN.finditer(body):
            if not _targets_self(match.group(1), model):
                continue
            yield make_suggestion(
                INC_TRUNCATE_LOAD,
                f"`{key}` drops this model's own relation, racing dbt's "
                "create-or-replace on the next run.",
                file=model.relative_path,
                evidence=f'{key}="{body.strip()[:180]}"',
                remediation=(
                    "Remove the hook. Use `dbt build --full-refresh --select "
                    f"{model.name}` when the relation needs rebuilding."
                ),
                effort=Effort.LOW,
            )


@rule(
    INC_DELETE_LOAD,
    "Delete-and-load instead of an incremental strategy",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "dbt's `delete+insert` and `merge` strategies express row replacement "
        "declaratively and atomically. A `delete` in a hook runs outside that contract "
        "and can leave the table short of rows if the insert then fails."
    ),
)
def delete_and_load(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    for key, body in config_hooks(model.effective_config):
        for match in DELETE_PATTERN.finditer(body):
            if not _targets_self(match.group(1), model):
                continue
            reads_sibling = bool(re.search(r"\bref\s*\(", body))
            message = (
                f"`{key}` deletes rows from this model's relation outside dbt's "
                "transaction and DAG."
            )
            if reads_sibling:
                message += (
                    " The hook also reads another model via `ref()`, an invisible "
                    "DAG dependency."
                )
            yield make_suggestion(
                INC_DELETE_LOAD,
                message,
                file=model.relative_path,
                evidence=f'{key}="{body.strip()[:220]}"',
                remediation=(
                    "Express the deletion through the materialization instead: use "
                    "`incremental_strategy='delete+insert'` with a `unique_key`, or "
                    "`'merge'` and carry a soft-delete flag in the model body so the "
                    "`merge` can act on it. That keeps the operation inside dbt's "
                    "transaction and inside the DAG."
                ),
                effort=Effort.MEDIUM,
                reads_sibling_model=reads_sibling,
            )


@rule(
    INC_HOOK_WRITES_ELSEWHERE,
    "Hook writes to a table other than the model",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "A model should produce exactly one relation. A hook inserting into a "
        "different table creates a write dbt does not track and will not rebuild in "
        "the right order."
    ),
)
def hook_writes_elsewhere(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    for key, body in config_hooks(model.effective_config):
        for match in INSERT_PATTERN.finditer(body):
            target = _dml_target(match.group(2))
            if _targets_self(match.group(2), model):
                continue
            yield make_suggestion(
                INC_HOOK_WRITES_ELSEWHERE,
                f"`{key}` runs `{match.group(1).lower()}` against "
                f"`{target.strip('();')}`, a relation this model does not otherwise "
                "produce.",
                file=model.relative_path,
                evidence=f'{key}="{body.strip()[:180]}"',
                remediation=(
                    "Make the target its own dbt model so the write is declarative "
                    "and appears in the DAG. If it is operational bookkeeping (an "
                    "audit or control table), move it to an on-run-end hook so it "
                    "runs once per invocation rather than once per model."
                ),
                effort=Effort.MEDIUM,
            )


@rule(
    INC_FOLDER_HOOK_DML,
    "Folder-level hook runs DML once per model, not once per run",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "A +pre-hook or +post-hook in dbt_project.yml fires for every model in that "
        "folder. A `truncate` there wipes data written by models that ran before it, "
        "so results depend on execution order."
    ),
)
def folder_hook_dml(project: ProjectContext) -> Iterator[Suggestion]:
    def walk(node: object, path: list[str]) -> Iterator[tuple[str, str, str]]:
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            if key in ("+pre-hook", "+post-hook", "+pre_hook", "+post_hook"):
                bodies = value if isinstance(value, list) else [value]
                for body in bodies:
                    yield "/".join(path) or "<project root>", key, str(body)
            elif not key.startswith("+"):
                yield from walk(value, [*path, str(key)])

    for scope_path, key, body in walk(project.project_yml.get("models") or {}, []):
        stripped = strip_comments_and_strings(body)
        verb = None
        if TRUNCATE_PATTERN.search(stripped):
            verb = "`truncate`"
        elif DELETE_PATTERN.search(stripped):
            verb = "`delete`"
        elif INSERT_PATTERN.search(stripped):
            verb = "`insert`/`merge`"
        if verb is None:
            continue
        yield make_suggestion(
            INC_FOLDER_HOOK_DML,
            f"A folder-level `{key}` on `{scope_path}` runs {verb} once per model, "
            "so results depend on execution order.",
            file="dbt_project.yml",
            yaml_keys=("models", *scope_path.split("/"), key),
            evidence=f"{key}: {body.strip()[:200]}",
            remediation=(
                "Move one-time setup out of a folder hook. Use `on-run-start`/"
                "`on-run-end` for once-per-invocation work, or make the operation "
                "idempotent and scope it to a single model's own hook. If this came "
                "from a converted disconnected stored procedure, the run-once "
                "semantics of the source do not survive as a folder hook."
            ),
            effort=Effort.MEDIUM,
        )


# =============================================================================
# Materialization mismatch
# =============================================================================


@rule(
    INC_MANUAL_INCREMENTAL,
    "Full-table materialization with a hand-rolled date window",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Filtering to a rolling window inside a `table` model rebuilds everything each "
        "run and silently drops history older than the window. That is the problem "
        "`materialized='incremental'` solves."
    ),
)
def manual_incremental(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    if model.is_python or model.materialization not in ("table", ""):
        return
    if model.materialization == "" and not model.raw.strip():
        return
    if IS_INCREMENTAL_PATTERN.search(model.raw):
        return
    if not DATE_PREDICATE_PATTERN.search(model.stripped):
        return
    if not DATE_WINDOW_PATTERN.search(model.stripped):
        return

    match = DATE_PREDICATE_PATTERN.search(model.stripped)
    yield make_suggestion(
        INC_MANUAL_INCREMENTAL,
        "This `table` model filters to a rolling date window, so each run rebuilds "
        "the window and drops older rows.",
        file=model.relative_path,
        **span(model.stripped, match.start(), match.end()),
        evidence=(match.group(0).strip() if match else ""),
        remediation=(
            "Convert to an incremental model: set `materialized='incremental'` with a "
            "`unique_key`, move the window filter inside `{% if is_incremental() %}`, "
            "and bound it against the target relation "
            "(`where updated_at > (select max(updated_at) from {{ this }})`). Keep an "
            "absolute floor alongside the watermark to bound the source scan."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    INC_FULL_RELOAD,
    "Named or configured as a full reload",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "A name or config declaring a full reload usually marks a table that outgrew "
        "full refresh but was never converted, and it forecloses incremental "
        "processing."
    ),
)
def full_reload(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    name_match = FULL_RELOAD_NAME_PATTERN.search(model.name)
    if name_match:
        yield make_suggestion(
            INC_FULL_RELOAD,
            f"`{model.name}` declares a full reload, which forecloses incremental "
            "processing.",
            file=model.relative_path,
            evidence=model.name,
            remediation=(
                "Assess whether the source supports incremental processing. If rows "
                "carry a reliable updated-at timestamp or an immutable event time, "
                "convert to `materialized='incremental'`. If a full rebuild is "
                "required, drop the suffix and say why in the model description so "
                "the choice reads as deliberate."
            ),
            effort=Effort.MEDIUM,
        )

    if model.effective_config.get("full_refresh") is True:
        yield make_suggestion(
            INC_FULL_RELOAD,
            "`full_refresh: true` forces a full rebuild on every run.",
            file=model.relative_path,
            evidence="full_refresh=True",
            remediation=(
                "Remove `full_refresh: true`. Trigger a rebuild on demand with "
                f"`dbt build --full-refresh --select {model.name}` instead of making "
                "every run a full refresh."
            ),
            effort=Effort.LOW,
        )


# =============================================================================
# Incremental model mechanics
# =============================================================================


@rule(
    INC_NO_GUARD,
    "Incremental model has no is_incremental() guard",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Without an `is_incremental()` branch the model reads its full source on "
        "every run, so the incremental materialization adds merge cost without "
        "saving any scan. With merge it can also rewrite every row each run."
    ),
)
def no_incremental_guard(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    if not model.is_incremental or model.is_python:
        return
    if _is_microbatch(model) or _reads_stream(model):
        return  # microbatch and streams manage their own filtering
    if IS_INCREMENTAL_PATTERN.search(model.raw):
        return
    yield make_suggestion(
        INC_NO_GUARD,
        "This incremental model has no `is_incremental()` guard and rescans its "
        "full source each run.",
        file=model.relative_path,
        evidence="materialized='incremental'; no is_incremental() call found",
        remediation=(
            "Add a guarded filter that bounds the read to new rows:\n\n"
            "```sql\n"
            "{% if is_incremental() %}\n"
            "where updated_at > (select max(updated_at) from {{ this }})\n"
            "{% endif %}\n"
            "```"
        ),
        effort=Effort.LOW,
    )


@rule(
    INC_NO_UNIQUE_KEY,
    "Incremental model has no unique_key",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.FDM,
    level=Level.INFORMATION,
    severity=Severity.HIGH,
    rationale=(
        "`merge` and `delete+insert` need a `unique_key` to know which rows to "
        "replace. Without one the model appends, so any reprocessed row silently "
        "duplicates."
    ),
)
def no_unique_key(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not model.is_incremental:
        return
    strategy = str(model.effective_config.get("incremental_strategy", "merge")).lower()
    if strategy not in STRATEGIES_NEEDING_KEY:
        return
    if model.effective_config.get("unique_key"):
        return
    yield make_suggestion(
        INC_NO_UNIQUE_KEY,
        f"`{strategy}` with no `unique_key` appends, so a restated row duplicates "
        "on reprocessing.",
        file=model.relative_path,
        evidence=f"incremental_strategy='{strategy}'; unique_key absent",
        remediation=(
            "Add the business key to the config, e.g. `unique_key='order_id'` (or a "
            "list for a composite key). Pair it with a "
            "`dbt_constraints.primary_key` test on the same column so the assumption "
            "is enforced rather than assumed."
        ),
        effort=Effort.LOW,
    )


@rule(
    INC_NO_STRATEGY,
    "Incremental model does not state its strategy",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "The default strategy is adapter-dependent. Stating it makes the load "
        "semantics reviewable and stops an adapter upgrade from changing behaviour."
    ),
)
def no_strategy(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not model.is_incremental:
        return
    strategy = model.effective_config.get("incremental_strategy")
    if strategy is None:
        yield make_suggestion(
            INC_NO_STRATEGY,
            "`incremental_strategy` is unset, so the load uses the adapter default.",
            file=model.relative_path,
            evidence="incremental_strategy absent",
            remediation=(
                "State the intended strategy: `merge` for updateable records, "
                "`append` for immutable events, `delete+insert` for reprocessing whole "
                "partitions."
            ),
            effort=Effort.LOW,
        )
        return
    if str(strategy).lower() not in VALID_STRATEGIES:
        yield make_suggestion(
            INC_NO_STRATEGY,
            f"`incremental_strategy='{strategy}'` is not one of dbt-snowflake's "
            "built-in strategies.",
            level=Level.WARNING,
            file=model.relative_path,
            evidence=f"incremental_strategy='{strategy}'",
            remediation="Use one of: " + ", ".join(sorted(VALID_STRATEGIES)) + ".",
            effort=Effort.LOW,
        )


@rule(
    INC_NO_WATERMARK,
    "Incremental branch does not reference the target relation",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "An `is_incremental()` branch that does not consult `{{ this }}` has no "
        "watermark: it cannot know what has already been loaded, so it either "
        "reprocesses a fixed window or misses late rows."
    ),
)
def no_watermark(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not model.is_incremental or not IS_INCREMENTAL_PATTERN.search(model.raw):
        return
    if _reads_stream(model) or _is_microbatch(model):
        return  # streams and microbatch manage their own offset; {{ this }} watermark is redundant
    for match in re.finditer(
        r"\{%-?\s*if\s+is_incremental\s*\(\s*\)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}",
        model.raw,
        re.DOTALL | re.IGNORECASE,
    ):
        body = match.group(1)
        if THIS_PATTERN.search(body):
            continue
        yield make_suggestion(
            INC_NO_WATERMARK,
            "This incremental branch does not reference `{{ this }}`, so it has no "
            "watermark against loaded rows.",
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=body.strip()[:200],
            remediation=(
                "Bound the read against the existing relation:\n\n"
                "```sql\n"
                "where updated_at > (select max(updated_at) from {{ this }})\n"
                "```\n\n"
                "Subtract a lookback interval if the source can deliver late rows."
            ),
            effort=Effort.LOW,
        )


@rule(
    INC_UNBOUNDED_SCAN,
    "Incremental watermark has no absolute lower bound",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "A watermark alone still asks the warehouse to scan the whole source to "
        "evaluate the predicate on first run and after a full refresh. An absolute "
        "date floor lets Snowflake prune partitions."
    ),
)
def unbounded_scan(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if not model.is_incremental:
        return
    if _reads_stream(model) or _is_microbatch(model):
        return
    for match in re.finditer(
        r"\{%-?\s*if\s+is_incremental\s*\(\s*\)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}",
        model.raw,
        re.DOTALL | re.IGNORECASE,
    ):
        body = match.group(1)
        if not THIS_PATTERN.search(body):
            continue  # INC009 already covers this
        has_floor = bool(
            DATE_WINDOW_PATTERN.search(body)
            or re.search(r"'\d{4}-\d{2}-\d{2}'", body)
            or re.search(r"\bvar\s*\(", body)
        )
        if has_floor:
            continue
        yield make_suggestion(
            INC_UNBOUNDED_SCAN,
            "With only a `max()` watermark, the first run scans the whole source.",
            file=model.relative_path,
            **span(model.raw, match.start(), match.end()),
            evidence=body.strip()[:180],
            remediation=(
                "Add a second predicate that gives the optimiser something to prune "
                "on, e.g.\n\n"
                "```sql\n"
                "where updated_at > (select max(updated_at) from {{ this }})\n"
                "  and updated_at >= dateadd(day, -7, current_date())\n"
                "```\n\n"
                "Use a `var()` for the window so a backfill can widen it."
            ),
            effort=Effort.LOW,
        )


@rule(
    INC_MERGE_EXCLUDE_MISMATCH,
    "merge_exclude_columns for an unselected column",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.FDM,
    level=Level.INFORMATION,
    severity=Severity.HIGH,
    rationale=(
        "`merge_exclude_columns` preserves an insert-time value on update, but only "
        "if the model still selects that column. Excluding a column the model never "
        "produces leaves it NULL on insert."
    ),
)
def merge_exclude_mismatch(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    excluded = model.effective_config.get("merge_exclude_columns")
    if not excluded:
        return
    # A macro can generate the column list, in which case the columns do not exist
    # in the file text and every one of them would look absent.
    body = re.sub(r"\{\{-?\s*config\s*\([\s\S]*?\)\s*-?\}\}", "", model.raw)
    if MACRO_CALL_PATTERN.search(body):
        return
    columns = excluded if isinstance(excluded, list) else [excluded]
    for column in columns:
        name = str(column).strip()
        if not name or re.search(
            rf"\b{re.escape(name)}\b", model.stripped, re.IGNORECASE
        ):
            continue
        yield make_suggestion(
            INC_MERGE_EXCLUDE_MISMATCH,
            f"`merge_exclude_columns` lists `{name}`, which this model does not "
            "appear to select.",
            file=model.relative_path,
            evidence=f"merge_exclude_columns={columns}",
            remediation=(
                f"Either select `{name}` in the model body (typically "
                f"`current_timestamp() as {name}`), or remove it from "
                "`merge_exclude_columns`."
            ),
            effort=Effort.LOW,
        )


@rule(
    INC_APPEND_ON_MUTABLE,
    "append strategy on data that appears mutable",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.FDM,
    level=Level.INFORMATION,
    severity=Severity.HIGH,
    rationale=(
        "`append` never updates an existing row. If the source can restate a "
        "record, `append` accumulates duplicate versions with no way to tell which "
        "is current."
    ),
)
def append_on_mutable(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    if not model.is_incremental:
        return
    if str(model.effective_config.get("incremental_strategy", "")).lower() != "append":
        return
    match = MUTABLE_COLUMN_PATTERN.search(model.stripped)
    if not match:
        return
    yield make_suggestion(
        INC_APPEND_ON_MUTABLE,
        f"This model selects `{match.group(1)}` while using `append`, which never "
        "updates existing rows.",
        file=model.relative_path,
        **span(model.stripped, match.start(), match.end()),
        evidence=match.group(0).strip(),
        remediation=(
            "If rows can change, switch to `incremental_strategy='merge'` with the "
            "business `unique_key`. If the model is an immutable event stream and "
            "the column is only carried through, say so in the model description so "
            "the append is reviewable."
        ),
        effort=Effort.MEDIUM,
    )


# =============================================================================
# Loading outside dbt
# =============================================================================


@rule(
    INC_EXTERNAL_LOADER,
    "Loaded by a task or procedure outside dbt",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "A procedure or task writing to a dbt-managed relation competes with dbt "
        "for ownership. dbt will overwrite it, so lineage and tests describe a "
        "state nothing guarantees."
    ),
)
def external_loader(project: ProjectContext) -> Iterator[Suggestion]:
    model_names = {model.name.lower() for model in project.models}
    if not model_names:
        return
    for path, raw in project.loose_sql:
        stripped = strip_comments_and_strings(raw)
        if not re.search(
            r"\bcreate\s+(or\s+replace\s+)?(task|procedure)\b", stripped, re.IGNORECASE
        ):
            continue
        for match in INSERT_PATTERN.finditer(stripped):
            target = _dml_target(match.group(2)).strip("();\"'`").split(".")[-1].lower()
            if target not in model_names:
                continue
            try:
                relative = str(path.relative_to(project.root))
            except ValueError:
                relative = str(path)
            yield make_suggestion(
                INC_EXTERNAL_LOADER,
                f"`{path.name}`'s task or procedure writes `{target}`, which is also "
                "a dbt model.",
                file=relative,
                **span(stripped, match.start(), match.end()),
                evidence=match.group(0).strip()[:160],
                remediation=(
                    "Choose one owner. Either move the load logic into the dbt model "
                    "(preferred, so it gains lineage, tests and docs), or remove the "
                    "dbt model and treat the relation as a source."
                ),
                effort=Effort.HIGH,
            )
