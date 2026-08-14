"""
Project discovery and context construction.

Walks a root directory for ``dbt_project.yml`` files and builds the context
objects the rule packs consume. Two things here are easy to get wrong and are
therefore handled explicitly:

1. **Folder-config resolution.** dbt config is hierarchical: a model's effective
   materialization may come from ``dbt_project.yml`` rather than a ``config()``
   block. A rule that only reads ``config()`` would report "no materialization
   set" on a correctly configured project. ``resolve_folder_config`` walks the
   ``models:`` tree so ``ModelFile.effective_config`` is the merged view.

2. **Directory exclusion.** ``dbt_packages/`` contains other people's dbt
   projects, each with its own ``dbt_project.yml``. Failing to exclude it would
   report the entire package ecosystem as fragmented micro-projects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from dbt_quality.core.graph import Graph, load_graph
from dbt_quality.core.sqlutil import (
    extract_config,
    extract_macro_calls,
    extract_macro_defs,
    extract_refs,
    extract_sources,
    strip_all,
)
from dbt_quality.waivers import blank_directives

#: Never descend into these. ``dbt_packages``/``target`` in particular contain
#: vendored projects and compiled copies of the user's own models, which would
#: otherwise be audited as if they were first-party code.
EXCLUDED_DIRS = {
    "dbt_packages",
    "target",
    "logs",
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "dbt_modules",
    "site-packages",
    ".tox",
    "build",
    "dist",
}

#: Folder names that indicate each medallion layer. Both the medallion vocabulary
#: and dbt's conventional names are accepted, because projects use either.
LAYER_ALIASES: dict[str, str] = {
    "bronze": "bronze",
    "staging": "bronze",
    "stg": "bronze",
    "raw": "bronze",
    "silver": "silver",
    "intermediate": "silver",
    "int": "silver",
    "gold": "gold",
    "marts": "gold",
    "mart": "gold",
    "presentation": "gold",
}


# =============================================================================
# Configuration
# =============================================================================

#: How far up from the audit root to look for ``.dbt-quality.yml``. Matches the
#: bound ``hooks/setup_vscode_task.py`` uses for project detection.
CONFIG_SEARCH_LIMIT = 8

CONFIG_NAMES = (".dbt-quality.yml", ".dbt-quality.yaml")


@dataclass
class IgnoreRule:
    """
    One ``ignore:`` entry: rules waived at the paths it names.

    Unlike ``disabled_rules``, which turns a rule off everywhere and reports it as
    skipped, this waives specific findings and drops them -- see ``waivers.py``.
    """

    paths: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)

    @property
    def rule_set(self) -> set[str]:
        """Upper-cased rule ids, so a lower-case config entry still matches."""
        return {r.strip().upper() for r in self.rules if str(r).strip()}


@dataclass
class AuditConfig:
    """
    Tunable thresholds and modes, optionally loaded from ``.dbt-quality.yml``.

    There is deliberately no naming option. Model and column names are not
    audited at all, because a name can legitimately be the one the object had in
    the source database and a dbt project does not record what that was -- see
    the ``rules/arc.py`` module docstring for the evidence.
    """

    #: Model count at or below which a project is considered a micro-project.
    micro_project_threshold: int = 5
    #: Downstream references at or above which ephemeral/view should become table.
    ephemeral_fanout_threshold: int = 3
    #: Length of a single-child pass-through chain that counts as model explosion.
    passthrough_chain_threshold: int = 3
    #: Column documentation coverage below which DOC002 fires.
    column_doc_coverage: float = 0.8
    #: Macros per model above which over-abstraction is flagged.
    macro_model_ratio: float = 0.5
    #: Times an identical SQL block must repeat to warrant a macro.
    duplicate_block_threshold: int = 3
    #: Minimum lines for a repeated block to be worth extracting.
    duplicate_block_min_lines: int = 4
    #: Maximum sensible clustering key count (Snowflake guidance is 1-4).
    max_cluster_columns: int = 4
    #: "auto" | "native" | "lift_and_shift"
    migration_mode: str = "auto"
    #: Glob patterns treated as migrated regardless of detected provenance.
    migration_paths: list[str] = field(default_factory=list)
    #: Rule IDs to disable entirely.
    disabled_rules: list[str] = field(default_factory=list)
    #: Path-scoped waivers. A matching suggestion is dropped, not reported.
    ignores: list[IgnoreRule] = field(default_factory=list)

    @classmethod
    def load(cls, root: Path) -> AuditConfig:
        """
        Load the nearest ``.dbt-quality.yml`` at or above ``root``, else defaults.

        The search walks upward because the audit root is not always the repo
        root. ``dbt-validate`` builds its portfolio from the dbt project that
        encloses the file being written, so a config placed once at the repo root
        would otherwise be honoured by ``dbt-audit`` and invisible to the
        save-time hook -- a waiver that works in one surface and not the other
        reads as the feature being broken.

        The walk stops at the first config found, at a directory containing
        ``.git``, or after ``CONFIG_SEARCH_LIMIT`` levels, so it cannot wander
        out of the repository and pick up an unrelated file from ``$HOME``.
        """
        config = cls()
        path = _find_config(root)
        if path is None:
            return config

        try:
            with path.open(encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}
        except (OSError, yaml.YAMLError):
            return config
        if not isinstance(data, dict):
            return config

        thresholds = data.get("thresholds", {}) or {}
        if isinstance(thresholds, dict):
            for key, value in thresholds.items():
                if hasattr(config, key):
                    setattr(config, key, value)

        migration = data.get("migration", {}) or {}
        if isinstance(migration, dict):
            config.migration_mode = migration.get("mode", config.migration_mode)
            config.migration_paths = list(migration.get("paths", []) or [])

        config.disabled_rules = list(data.get("disabled_rules", []) or [])
        config.ignores = _parse_ignores(data.get("ignore"))
        return config


def _find_config(root: Path) -> Path | None:
    """Nearest config file at or above ``root``, within the documented bounds."""
    current = root
    for _ in range(CONFIG_SEARCH_LIMIT + 1):
        for name in CONFIG_NAMES:
            candidate = current / name
            if candidate.is_file():
                return candidate
        if (current / ".git").exists():
            return None
        if current.parent == current:
            return None
        current = current.parent
    return None


def _parse_ignores(raw: Any) -> list[IgnoreRule]:
    """
    Read the ``ignore:`` list, skipping anything malformed.

    A bad entry is dropped rather than raised on, matching how the rest of this
    loader treats unreadable configuration: a typo in one waiver must not cost
    the user the entire audit. An entry naming no paths or no rules waives
    nothing, so a half-written entry silences nothing by accident.
    """
    if not isinstance(raw, list):
        return []
    entries: list[IgnoreRule] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        paths = item.get("paths") or item.get("path") or []
        rules = item.get("rules") or item.get("rule") or []
        if isinstance(paths, str):
            paths = [paths]
        if isinstance(rules, str):
            rules = [rules]
        if not isinstance(paths, list) or not isinstance(rules, list):
            continue
        entry = IgnoreRule(
            paths=[str(p) for p in paths if str(p).strip()],
            rules=[str(r) for r in rules if str(r).strip()],
        )
        if entry.paths and entry.rules:
            entries.append(entry)
    return entries


# =============================================================================
# Model files
# =============================================================================


@dataclass
class ModelFile:
    """One ``.sql`` or ``.py`` model, with everything the rules need pre-parsed."""

    path: Path
    relative_path: str
    name: str
    raw: str
    #: Comments, string literals and Jinja statement blocks blanked out.
    stripped: str = ""
    #: ``raw`` with dbt-quality waiver directives blanked to equal-length spaces.
    #: Scan this, not ``raw``, when looking for SnowConvert conversion markers: a
    #: waiver names a rule id spelled exactly like one. See
    #: ``waivers.blank_directives``.
    without_directives: str = ""
    #: kwargs from the model's own ``config()`` call(s).
    own_config: dict[str, Any] = field(default_factory=dict)
    #: ``own_config`` merged over the resolved ``dbt_project.yml`` defaults.
    effective_config: dict[str, Any] = field(default_factory=dict)
    #: Defaults inherited from ``dbt_project.yml`` alone.
    folder_config: dict[str, Any] = field(default_factory=dict)
    layer: str = ""
    #: Path segments below ``models/``.
    segments: tuple[str, ...] = ()
    refs: list[str] = field(default_factory=list)
    sources: list[tuple[str, str]] = field(default_factory=list)
    macro_calls: list[dict[str, Any]] = field(default_factory=list)
    is_python: bool = False

    @property
    def materialization(self) -> str:
        return str(self.effective_config.get("materialized", ""))

    @property
    def is_incremental(self) -> bool:
        return self.materialization == "incremental"

    def line_of(self, position: int) -> int:
        return self.raw[:position].count("\n") + 1


@dataclass
class MacroFile:
    """One file under ``macros/`` and the macros it defines."""

    path: Path
    relative_path: str
    raw: str
    macros: list[dict[str, Any]] = field(default_factory=list)


# =============================================================================
# Project context
# =============================================================================


@dataclass
class ProjectContext:
    """Everything a project-scoped or model-scoped rule needs."""

    root: Path
    name: str
    relative_root: str
    project_yml: dict[str, Any] = field(default_factory=dict)
    packages: dict[str, Any] = field(default_factory=dict)
    models: list[ModelFile] = field(default_factory=list)
    macros: list[MacroFile] = field(default_factory=list)
    #: model name -> schema.yml model definition
    schema_models: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: model name -> path of the yml that declares it
    schema_sources: dict[str, str] = field(default_factory=dict)
    #: Raw ``sources:`` entries from all schema files.
    source_defs: list[dict[str, Any]] = field(default_factory=list)
    snapshot_files: list[tuple[Path, str]] = field(default_factory=list)
    singular_tests: list[tuple[Path, str]] = field(default_factory=list)
    #: Non-model SQL found in the project tree (orchestration scripts, DDL).
    loose_sql: list[tuple[Path, str]] = field(default_factory=list)
    graph: Graph = field(default_factory=Graph)
    config: AuditConfig = field(default_factory=AuditConfig)
    provenance: Any = None  # ProvenanceVerdict; avoids a circular import
    #: Files that could not be read or parsed, surfaced in the report.
    read_errors: list[str] = field(default_factory=list)
    #: relative path -> parsed waiver directives, populated on demand by
    #: ``waivers.file_waivers``. Scoped to one run, so nothing goes stale.
    waiver_cache: dict[str, Any] = field(default_factory=dict)

    @property
    def model_count(self) -> int:
        return len(self.models)

    def model_by_name(self, name: str) -> ModelFile | None:
        for model in self.models:
            if model.name == name:
                return model
        return None

    def schema_def(self, model_name: str) -> dict[str, Any]:
        return self.schema_models.get(model_name, {})


@dataclass
class PortfolioContext:
    """All projects discovered under one root, for portfolio-scoped rules."""

    root: Path
    projects: list[ProjectContext] = field(default_factory=list)
    config: AuditConfig = field(default_factory=AuditConfig)
    #: dbt_project.yml files found but unreadable.
    read_errors: list[str] = field(default_factory=list)


# =============================================================================
# Discovery
# =============================================================================


def _iter_files(root: Path, suffixes: tuple[str, ...]) -> list[Path]:
    """Recursive file walk honouring EXCLUDED_DIRS, avoiding vendored trees."""
    out: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except (OSError, PermissionError):
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name not in EXCLUDED_DIRS and not entry.name.startswith("."):
                    stack.append(entry)
            elif entry.suffix.lower() in suffixes:
                out.append(entry)
    return sorted(out)


def find_projects(root: Path) -> list[Path]:
    """
    Every directory under ``root`` containing a ``dbt_project.yml``.

    Nested projects are all returned -- the generated
    ``Output/ETL/{Package}/{DataFlow}/`` layout puts real projects several levels
    deep, and treating only the outermost as real would hide exactly the
    fragmentation this audit is meant to surface.
    """
    found: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except (OSError, PermissionError):
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name not in EXCLUDED_DIRS and not entry.name.startswith("."):
                    stack.append(entry)
            elif entry.name == "dbt_project.yml":
                found.append(current)
    return sorted(set(found))


def _load_yaml(path: Path) -> tuple[dict[str, Any], str | None]:
    try:
        with path.open(encoding="utf-8") as handle:
            return (yaml.safe_load(handle) or {}), None
    except (OSError, yaml.YAMLError) as exc:
        return {}, f"{path}: {exc}"


def _read_text(path: Path) -> tuple[str, str | None]:
    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return "", f"{path}: {exc}"


def resolve_folder_config(
    project_yml: dict[str, Any], project_name: str, segments: tuple[str, ...]
) -> dict[str, Any]:
    """
    Resolve the ``dbt_project.yml`` ``models:`` tree for a model's path.

    Walks from the project key down through each path segment, accumulating
    ``+``-prefixed keys so deeper settings override shallower ones -- dbt's own
    precedence. Without this, a project that sets materialization once at the
    folder level looks entirely unconfigured.

    The project key may not match ``name:`` (people rename projects and forget),
    so if the declared name is absent we fall back to the sole top-level key.
    """
    models_tree = project_yml.get("models") or {}
    if not isinstance(models_tree, dict):
        return {}

    node = models_tree.get(project_name)
    if not isinstance(node, dict):
        candidates = [
            v
            for k, v in models_tree.items()
            if not k.startswith("+") and isinstance(v, dict)
        ]
        if len(candidates) != 1:
            return {}
        node = candidates[0]

    resolved: dict[str, Any] = {
        k.lstrip("+"): v for k, v in node.items() if k.startswith("+")
    }

    for segment in segments:
        child = node.get(segment)
        if not isinstance(child, dict):
            break
        node = child
        for key, value in node.items():
            if key.startswith("+"):
                resolved[key.lstrip("+")] = value
    return resolved


def infer_layer(segments: tuple[str, ...]) -> str:
    """Medallion layer for a model, from the first recognised path segment."""
    for segment in segments:
        alias = LAYER_ALIASES.get(segment.lower())
        if alias:
            return alias
    return ""


def _model_paths(project_root: Path, project_yml: dict[str, Any]) -> list[Path]:
    """Model directories declared by ``model-paths``, defaulting to ``models``."""
    declared = (
        project_yml.get("model-paths") or project_yml.get("source-paths") or ["models"]
    )
    if isinstance(declared, str):
        declared = [declared]
    return [project_root / p for p in declared]


def build_project_context(
    project_root: Path, audit_root: Path, config: AuditConfig
) -> ProjectContext:
    """Load one dbt project into a fully-populated ``ProjectContext``."""
    project_yml, error = _load_yaml(project_root / "dbt_project.yml")
    project_name = str(project_yml.get("name") or project_root.name)

    try:
        relative_root = str(project_root.relative_to(audit_root)) or "."
    except ValueError:
        relative_root = str(project_root)

    context = ProjectContext(
        root=project_root,
        name=project_name,
        relative_root=relative_root,
        project_yml=project_yml,
        config=config,
    )
    if error:
        context.read_errors.append(error)

    packages, pkg_error = _load_yaml(project_root / "packages.yml")
    context.packages = packages
    if pkg_error and (project_root / "packages.yml").is_file():
        context.read_errors.append(pkg_error)

    newest_mtime = 0.0

    # --- models -----------------------------------------------------------
    for models_dir in _model_paths(project_root, project_yml):
        if not models_dir.is_dir():
            continue
        for path in _iter_files(models_dir, (".sql", ".py")):
            raw, read_error = _read_text(path)
            if read_error:
                context.read_errors.append(read_error)
                continue
            newest_mtime = max(newest_mtime, path.stat().st_mtime)
            segments = path.relative_to(models_dir).parts[:-1]
            own_config = extract_config(raw) if path.suffix == ".sql" else {}
            folder_config = resolve_folder_config(project_yml, project_name, segments)
            model = ModelFile(
                path=path,
                relative_path=str(path.relative_to(project_root)),
                name=path.stem,
                raw=raw,
                stripped=strip_all(raw),
                without_directives=blank_directives(raw),
                own_config=own_config,
                folder_config=folder_config,
                effective_config={**folder_config, **own_config},
                layer=infer_layer(segments),
                segments=segments,
                refs=extract_refs(raw),
                sources=extract_sources(raw),
                macro_calls=extract_macro_calls(raw),
                is_python=path.suffix == ".py",
            )
            context.models.append(model)

        # Schema YAML lives alongside models.
        for path in _iter_files(models_dir, (".yml", ".yaml")):
            data, yml_error = _load_yaml(path)
            if yml_error:
                context.read_errors.append(yml_error)
                continue
            relative = str(path.relative_to(project_root))
            for entry in data.get("models") or []:
                if isinstance(entry, dict) and entry.get("name"):
                    context.schema_models[str(entry["name"])] = entry
                    context.schema_sources[str(entry["name"])] = relative
            for entry in data.get("sources") or []:
                if isinstance(entry, dict):
                    context.source_defs.append(entry)

    # --- macros -----------------------------------------------------------
    for macro_dir_name in project_yml.get("macro-paths") or ["macros"]:
        macro_dir = project_root / macro_dir_name
        if not macro_dir.is_dir():
            continue
        for path in _iter_files(macro_dir, (".sql",)):
            raw, read_error = _read_text(path)
            if read_error:
                context.read_errors.append(read_error)
                continue
            context.macros.append(
                MacroFile(
                    path=path,
                    relative_path=str(path.relative_to(project_root)),
                    raw=raw,
                    macros=extract_macro_defs(raw),
                )
            )

    # --- snapshots and singular tests ------------------------------------
    for snapshot_dir_name in project_yml.get("snapshot-paths") or ["snapshots"]:
        snapshot_dir = project_root / snapshot_dir_name
        if snapshot_dir.is_dir():
            for path in _iter_files(snapshot_dir, (".sql",)):
                raw, _ = _read_text(path)
                context.snapshot_files.append((path, raw))

    for test_dir_name in project_yml.get("test-paths") or ["tests"]:
        test_dir = project_root / test_dir_name
        if test_dir.is_dir():
            for path in _iter_files(test_dir, (".sql",)):
                raw, _ = _read_text(path)
                context.singular_tests.append((path, raw))

    # --- loose SQL (orchestration scripts, DDL outside dbt) ---------------
    for extra_dir in (
        "macros_sql",
        "scripts",
        "sql",
        "orchestration",
        "etl_configuration",
    ):
        candidate = project_root / extra_dir
        if candidate.is_dir():
            for path in _iter_files(candidate, (".sql",)):
                raw, _ = _read_text(path)
                context.loose_sql.append((path, raw))

    context.graph = load_graph(project_root, newest_mtime or None)
    return context


def build_portfolio(root: Path) -> PortfolioContext:
    """Discover every dbt project under ``root`` and build its context."""
    root = root.resolve()
    config = AuditConfig.load(root)
    portfolio = PortfolioContext(root=root, config=config)

    for project_root in find_projects(root):
        portfolio.projects.append(build_project_context(project_root, root, config))

    # Orchestration SQL frequently sits outside any single project (the
    # generated layout puts per-package .sql beside the project folders), so
    # scan the root for EXECUTE DBT PROJECT calls and attribute them to the
    # portfolio via the first project. PRJ006 reads this.
    return portfolio
