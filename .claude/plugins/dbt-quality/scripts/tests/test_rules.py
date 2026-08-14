"""
Verification harness for the dbt-audit rule packs.

Two kinds of check:

1. **Fixture tests** -- synthetic projects written to a temp dir, asserting that a
   specific anti-pattern fires and that the sanctioned form of the same pattern
   does not. These are the false-positive gate; without them a regex tightened for
   one repo silently breaks on another.

2. **Ground-truth tests** -- run against this repository, asserting known-true
   suggestions (a model literally named ``*_full_reload`` must produce INC005) and
   known-false ones (a single 40-model project must not be reported as
   fragmented).

Run with:  pytest tests/ -q
Or standalone: python tests/test_rules.py
"""

from __future__ import annotations

import shutil
import sys
import textwrap
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS / "src"))

from dbt_quality.core.base import REGISTRY  # noqa: E402
from dbt_quality.core.sqlutil import (  # noqa: E402
    extract_config,
    extract_ctes,
    find_derived_subqueries,
    is_watermark_subquery,
)
from dbt_quality.discovery import build_portfolio  # noqa: E402
from dbt_quality.engine import run_audit, run_single_file  # noqa: E402
from dbt_quality.scoring import build_report  # noqa: E402
from dbt_quality.waivers import blank_directives, parse_waivers  # noqa: E402


def _find_repo_root(start: Path) -> Path:
    """
    Walk up to the nearest directory holding a dbt_project.yml.

    Resolved by search rather than a fixed number of `.parent` hops, because a
    hop count silently breaks when the package moves -- which it did when this
    engine became a plugin. A wrong root makes the ground-truth test skip itself
    and report success, which is the worst possible failure mode for a test.
    """
    for candidate in [start, *start.parents]:
        if (candidate / "dbt_project.yml").is_file():
            return candidate
    return start


REPO_ROOT = _find_repo_root(SCRIPTS)
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# Deliberately static: this integration fixture must change alongside the EWI
# catalogue, rather than silently accepting a newly registered rule.
EXPECTED_EWI_RULE_IDS = frozenset(
    {
        "SSC-EWI-DBTARC0001",
        "SSC-EWI-DBTARC0003",
        "SSC-EWI-DBTARC0004",
        "SSC-EWI-DBTARC0005",
        "SSC-EWI-DBTARC0006",
        "SSC-EWI-DBTARC0007",
        "SSC-EWI-DBTDOC0001",
        "SSC-EWI-DBTDOC0002",
        "SSC-EWI-DBTDOC0003",
        "SSC-EWI-DBTDOC0004",
        "SSC-EWI-DBTINC0001",
        "SSC-EWI-DBTINC0002",
        "SSC-EWI-DBTINC0003",
        "SSC-EWI-DBTINC0008",
        "SSC-EWI-DBTINC0010",
        "SSC-EWI-DBTINC0015",
        "SSC-EWI-DBTMAC0001",
        "SSC-EWI-DBTMAC0002",
        "SSC-EWI-DBTMAC0003",
        "SSC-EWI-DBTMAC0004",
        "SSC-EWI-DBTMAC0005",
        "SSC-EWI-DBTMAC0006",
        "SSC-EWI-DBTMAC0007",
        "SSC-EWI-DBTMAC0008",
        "SSC-EWI-DBTMAC0009",
        "SSC-EWI-DBTMAC0010",
        "SSC-EWI-DBTMAC0011",
        "SSC-EWI-DBTMAC0012",
        "SSC-EWI-DBTMAT0006",
        "SSC-EWI-DBTMAT0007",
        "SSC-EWI-DBTMIG0001",
        "SSC-EWI-DBTMIG0002",
        "SSC-EWI-DBTMIG0004",
        "SSC-EWI-DBTMIG0006",
        "SSC-EWI-DBTMIG0007",
        "SSC-EWI-DBTMIG0008",
        "SSC-EWI-DBTOPS0001",
        "SSC-EWI-DBTOPS0002",
        "SSC-EWI-DBTOPS0003",
        "SSC-EWI-DBTOPS0004",
        "SSC-EWI-DBTPRJ0001",
        "SSC-EWI-DBTPRJ0002",
        "SSC-EWI-DBTPRJ0003",
        "SSC-EWI-DBTPRJ0004",
        "SSC-EWI-DBTPRJ0005",
        "SSC-EWI-DBTPRJ0006",
        "SSC-EWI-DBTPRJ0007",
        "SSC-EWI-DBTPRJ0008",
        "SSC-EWI-DBTSQL0001",
        "SSC-EWI-DBTSQL0002",
        "SSC-EWI-DBTSQL0003",
        "SSC-EWI-DBTSQL0004",
        "SSC-EWI-DBTSQL0005",
        "SSC-EWI-DBTSQL0006",
        "SSC-EWI-DBTSQL0007",
        "SSC-EWI-DBTSQL0009",
        "SSC-EWI-DBTSQL0010",
        "SSC-EWI-DBTSQL0011",
        "SSC-EWI-DBTSQL0012",
        "SSC-EWI-DBTSQL0013",
        "SSC-EWI-DBTTST0001",
        "SSC-EWI-DBTTST0002",
        "SSC-EWI-DBTTST0003",
        "SSC-EWI-DBTTST0004",
        "SSC-EWI-DBTTST0005",
        "SSC-EWI-DBTTST0006",
        "SSC-EWI-DBTTST0007",
        "SSC-EWI-DBTTST0008",
        "SSC-EWI-DBTTST0009",
        "SSC-EWI-DBTTST0010",
        "SSC-EWI-DBTTST0012",
    }
)


# =============================================================================
# Fixture helpers
# =============================================================================


def write_project(
    root: Path, name: str = "fixture", project_yml: str | None = None
) -> Path:
    """Create a minimal dbt project skeleton and return its root."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "models").mkdir(exist_ok=True)
    (root / "dbt_project.yml").write_text(
        project_yml or textwrap.dedent(f"""
            name: '{name}'
            version: '1.0.0'
            profile: '{name}'
            models:
              {name}:
                +materialized: view
            """).strip(),
        encoding="utf-8",
    )
    return root


def add_model(root: Path, relative: str, sql: str) -> None:
    path = root / "models" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(sql).strip(), encoding="utf-8")


def copy_fixture(tmp_path: Path, name: str) -> Path:
    destination = tmp_path / name
    shutil.copytree(FIXTURES / name, destination)
    return destination


def audit(root: Path) -> dict:
    return build_report(run_audit(build_portfolio(root)), str(root))


def rule_ids(report: dict) -> set[str]:
    return {f["rule_id"] for f in report["suggestions"]}


def suggestions_for(report: dict, rule_id: str) -> list[dict]:
    return [f for f in report["suggestions"] if f["rule_id"] == rule_id]


def skipped_rule_ids(report: dict) -> set[str]:
    return {f["rule_id"] for f in report["skipped_checks"]}


# =============================================================================
# Unit checks: the parsing primitives everything else depends on
# =============================================================================


def test_config_extraction() -> None:
    config = extract_config("""
        {{ config(
            materialized='incremental',
            unique_key='order_id',
            cluster_by=['order_date', 'customer_id'],
            full_refresh=false,
            pre_hook="TRUNCATE TABLE {{ this }}"
        ) }}
        select 1
        """)
    assert config["materialized"] == "incremental"
    assert config["unique_key"] == "order_id"
    assert config["cluster_by"] == ["order_date", "customer_id"]
    assert config["full_refresh"] is False
    assert "TRUNCATE" in config["pre_hook"]


def test_watermark_subquery_is_exempt() -> None:
    """The single most important false-positive guard in the whole audit."""
    assert is_watermark_subquery("select max(updated_at) from {{ this }}")
    assert not is_watermark_subquery(
        "select customer_id, sum(amount) from orders group by 1"
    )


def test_derived_subquery_detection_scope() -> None:
    sql = """
    select *
    from (select a, b from {{ ref('x') }} where a > 0) inner_q
    where b in (select b from {{ ref('y') }})
      and exists (select 1 from {{ ref('z') }})
    """
    found = find_derived_subqueries(sql)
    # Only the FROM-position subquery counts; IN and EXISTS are legitimate.
    assert len(found) == 1
    assert found[0]["keyword"] == "from"


def test_cte_extraction_ignores_keywords() -> None:
    ctes = extract_ctes("""
        with source as (select 1),
             filtered as (select 1 from source where x > 0)
        select cast(a as varchar) from filtered
        """)
    assert {c["name"] for c in ctes} == {"source", "filtered"}


# =============================================================================
# Fixture checks: does the anti-pattern fire, and does the good form stay silent
# =============================================================================


def test_truncate_load_fires(tmp_path: Path) -> None:
    root = write_project(tmp_path / "trunc")
    add_model(
        root,
        "gold/fct_orders.sql",
        """
        {{ config(materialized='table', pre_hook="truncate table {{ this }}") }}
        select 1 as order_id
        """,
    )
    ids = rule_ids(audit(root))
    assert (
        "SSC-EWI-DBTINC0001" in ids
    ), "truncate-and-load in a pre_hook must fire INC001"


def test_correct_incremental_stays_silent(tmp_path: Path) -> None:
    """
    A textbook incremental model must produce no INC suggestions.

    This is the regression guard for the watermark exemption: if the subquery or
    incremental rules over-fire, every well-written project looks broken.
    """
    root = write_project(tmp_path / "clean")
    add_model(
        root,
        "gold/fct_orders.sql",
        """
        {{ config(
            materialized='incremental',
            unique_key='order_id',
            incremental_strategy='merge',
            cluster_by=['order_date']
        ) }}
        select order_id, order_date, updated_at
        from {{ ref('stg_orders') }}
        {% if is_incremental() %}
        where updated_at > (select max(updated_at) from {{ this }})
          and updated_at >= dateadd(day, -7, current_date())
        {% endif %}
        """,
    )
    add_model(root, "bronze/stg_orders.sql", "select 1 as order_id")
    inc = [f for f in audit(root)["suggestions"] if f["category"] == "INC"]
    assert not inc, f"correct incremental model produced INC suggestions: {inc}"


def test_incremental_without_guard_or_key(tmp_path: Path) -> None:
    root = write_project(tmp_path / "badinc")
    add_model(
        root,
        "gold/fct_events.sql",
        """
        {{ config(materialized='incremental') }}
        select event_id from {{ ref('stg_events') }}
        """,
    )
    add_model(root, "bronze/stg_events.sql", "select 1 as event_id")
    ids = rule_ids(audit(root))
    assert "SSC-PRF-DBTINC0006" in ids, "missing is_incremental() must fire INC006"
    assert "SSC-FDM-DBTINC0007" in ids, "missing unique_key on merge must fire INC007"


def test_subquery_recommends_cte_when_used_once(tmp_path: Path) -> None:
    root = write_project(tmp_path / "sub1")
    add_model(
        root,
        "gold/fct_a.sql",
        """
        select o.id, c.total
        from {{ ref('stg_o') }} o
        join (
            select customer_id, sum(amount) as total, count(*) as n
            from {{ ref('stg_p') }}
            where status = 'complete' and amount > 0
            group by customer_id
        ) c on c.customer_id = o.id
        """,
    )
    add_model(root, "bronze/stg_o.sql", "select 1 as id")
    add_model(root, "bronze/stg_p.sql", "select 1 as customer_id")
    hits = suggestions_for(audit(root), "SSC-EWI-DBTSQL0001")
    assert hits, "FROM/JOIN subquery must fire SQL001"
    assert hits[0]["context"]["reuse_count"] == 1
    assert "CTE" in hits[0]["remediation"], "single-use subquery must recommend a CTE"


def test_subquery_recommends_ephemeral_when_reused(tmp_path: Path) -> None:
    """Identical logic in two models must recommend a model, not a CTE."""
    root = write_project(tmp_path / "sub2")
    shared = """
        select customer_id, sum(amount) as total, count(*) as n
        from {{ ref('stg_p') }}
        where status = 'complete' and amount > 0
        group by customer_id
    """
    for name in ("fct_a", "fct_b"):
        add_model(
            root,
            f"gold/{name}.sql",
            f"""
            select o.id, c.total
            from {{{{ ref('stg_o') }}}} o
            join ({shared}) c on c.customer_id = o.id
            """,
        )
    add_model(root, "bronze/stg_o.sql", "select 1 as id")
    add_model(root, "bronze/stg_p.sql", "select 1 as customer_id")
    hits = suggestions_for(audit(root), "SSC-EWI-DBTSQL0001")
    assert len(hits) == 2, "both models carrying the shared subquery must be reported"
    assert hits[0]["context"]["reuse_count"] == 2
    assert (
        "ephemeral" in hits[0]["remediation"]
    ), "reused subquery must recommend an ephemeral model"


def test_macro_overuse_and_underuse(tmp_path: Path) -> None:
    root = write_project(tmp_path / "macros")
    (root / "macros").mkdir()
    (root / "macros" / "trivial.sql").write_text(
        "{% macro trivial(col) %}coalesce({{ col }}, 0){% endmacro %}", encoding="utf-8"
    )
    (root / "macros" / "orphan.sql").write_text(
        "{% macro orphan(col) %}upper({{ col }}){% endmacro %}", encoding="utf-8"
    )
    add_model(
        root,
        "gold/dim_a.sql",
        "select {{ trivial('amount') }} as amount from {{ ref('s') }}",
    )
    add_model(root, "bronze/s.sql", "select 1 as amount")
    ids = rule_ids(audit(root))
    assert "SSC-EWI-DBTMAC0003" in ids, "macro with no call sites must fire MAC003"
    assert (
        "SSC-EWI-DBTMAC0002" in ids or "SSC-EWI-DBTMAC0004" in ids
    ), "single-caller trivial macro must be flagged"


def test_fragmentation_fires_only_across_projects(tmp_path: Path) -> None:
    estate = tmp_path / "estate"
    for i in range(3):
        root = write_project(estate / f"flow_{i}", name=f"flow_{i}")
        add_model(
            root,
            f"gold/out_{i}.sql",
            f"select {i} as id from {{{{ source('raw','t') }}}}",
        )
    report = audit(estate)
    micro = suggestions_for(report, "SSC-EWI-DBTPRJ0001")
    assert len(micro) == 3, "each 1-model project must be reported as a micro-project"
    assert suggestions_for(
        report, "SSC-EWI-DBTPRJ0002"
    ), "projects sharing a source must be a consolidation candidate"


def test_single_small_project_is_not_fragmentation(tmp_path: Path) -> None:
    """A new or deliberately scoped repo is not fragmentation."""
    root = write_project(tmp_path / "solo")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    assert not suggestions_for(audit(root), "SSC-EWI-DBTPRJ0001")


def test_migration_suppresses_architecture_not_correctness(tmp_path: Path) -> None:
    """
    The core tier behaviour.

    A converted project must keep its correctness suggestions and its unresolved
    conversion debt, while losing the architecture-purity noise.
    """
    root = write_project(tmp_path / "migrated")
    add_model(
        root,
        "staging/stg_raw__SQ_EMPLOYEE.sql",
        """
        {{ config(materialized='table',
                  pre_hook="DELETE FROM {{ this }} WHERE id IN
                            (SELECT id FROM {{ ref('int_UPDTRANS') }})") }}
        --** SSC-FDM-INF0015 - UPDATE STRATEGY LOGIC HAS BEEN MOVED TO THE TARGET MODEL. **
        select *, 'DD_INSERT' as etl_dml_operation__
        from {{ source('raw', 'employee') }}
        """,
    )
    add_model(root, "staging/int_UPDTRANS.sql", "select 1 as id")
    # A model outside any layer folder gives an architecture suggestion (ARC001)
    # that will be suppressed because provenance confidence is "high".
    add_model(root, "output/legacy_dump.sql", "select 1 as id")
    report = audit(root)
    ids = rule_ids(report)

    assert report["projects"][0]["provenance"][
        "is_migration"
    ], "conversion markers must be detected"
    assert (
        "SSC-EWI-DBTINC0002" in ids
    ), "delete-and-load must still fire on converted code"
    assert "SSC-FDM-DBTMIG0003" in ids, "SSC-FDM marker must be reported"
    assert "SSC-FDM-DBTMIG0005" in ids, "ETL control column must be reported"

    architecture = [f for f in report["suggestions"] if f["tier"] == "architecture"]
    assert architecture, "architecture rules should still evaluate"
    assert all(
        f.get("suppressed") for f in architecture
    ), "every architecture finding on converted code must be suppressed, not reported"
    assert report["suppressed"]["count"] > 0
    # Suppressed suggestions must not affect the active counts.
    assert all(
        not f.get("suppressed") for f in report["suggestions"] if f["category"] == "INC"
    )


def test_native_project_keeps_architecture_suggestions(tmp_path: Path) -> None:
    """The mirror of the above: with no conversion markers, nothing is suppressed."""
    root = write_project(tmp_path / "native")
    # Outside any recognised layer folder, which ARC001 reports. Deliberately not
    # asserting on the filename's mixed case -- that is no longer audited, since a
    # model may keep the name its object had in the source database.
    add_model(root, "other/WeirdName.sql", "select 1 as id")
    report = audit(root)
    assert not report["projects"][0]["provenance"]["is_migration"]
    assert "SSC-EWI-DBTARC0001" in rule_ids(
        report
    ), "model outside a layer folder must be reported on native code"
    assert report["suppressed"]["count"] == 0


def test_folder_hook_dml_fires(tmp_path: Path) -> None:
    root = write_project(
        tmp_path / "hooks",
        project_yml=textwrap.dedent("""
            name: 'hooks'
            version: '1.0.0'
            profile: 'hooks'
            models:
              hooks:
                gold:
                  +pre-hook: "TRUNCATE TABLE staging_scratch"
            """).strip(),
    )
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    assert "SSC-EWI-DBTINC0003" in rule_ids(
        audit(root)
    ), "folder-level TRUNCATE hook must fire INC003"


# =============================================================================
# Ground truth against this repository
# =============================================================================


def test_hardcoded_ref_exempts_snowflake_system_schemas(tmp_path: Path) -> None:
    """
    SNOWFLAKE.ACCOUNT_USAGE, SNOWFLAKE.ORGANIZATION_USAGE, and INFORMATION_SCHEMA
    cannot be expressed as ref() or source() -- they must not fire SQL006.
    """
    root = write_project(tmp_path / "sysref")
    add_model(
        root,
        "gold/account_summary.sql",
        """
        select query_id, total_elapsed_time
        from snowflake.account_usage.query_history
        where start_time > dateadd(day, -7, current_date())
        """,
    )
    add_model(
        root,
        "gold/org_credits.sql",
        """
        select account_name, sum(credits_used) as total_credits
        from snowflake.organization_usage.metering_daily_history
        group by 1
        """,
    )
    add_model(
        root,
        "gold/schema_cols.sql",
        """
        select table_name, column_name
        from information_schema.columns
        where table_schema = 'PUBLIC'
        """,
    )
    add_model(
        root,
        "gold/db_info.sql",
        """
        select table_name
        from mydb.information_schema.tables
        """,
    )
    ids = rule_ids(audit(root))
    assert (
        "SSC-EWI-DBTSQL0006" not in ids
    ), "SNOWFLAKE system schemas and INFORMATION_SCHEMA must not fire SQL006"


def test_hardcoded_ref_fires_as_information_not_error(tmp_path: Path) -> None:
    """A regular hardcoded table reference fires as information, not error."""
    from dbt_quality.core.base import Level

    root = write_project(tmp_path / "hardref")
    add_model(root, "gold/fct_x.sql", "select id from analytics.public.orders")
    result = run_audit(build_portfolio(root))
    hits = [s for s in result.suggestions if s.rule_id == "SSC-EWI-DBTSQL0006"]
    assert hits, "regular hardcoded ref must still fire SQL006"
    assert all(
        s.level == Level.INFORMATION for s in hits
    ), "SQL006 must be information level, not error"


def test_passthrough_chain_rule_removed() -> None:
    """MAT003 was removed; it must not be registered."""
    assert (
        "SSC-PRF-DBTMAT0003" not in REGISTRY
    ), "passthrough-chain rule was removed and must not be registered"


def test_python_model_rule_removed() -> None:
    """MAT008 was removed; it must not be registered."""
    assert (
        "SSC-EWI-DBTMAT0008" not in REGISTRY
    ), "python-model rule was removed and must not be registered"


def test_clustering_does_not_fire_for_missing_key(tmp_path: Path) -> None:
    """MAT004 must not suggest adding a cluster_by when none is present."""
    root = write_project(tmp_path / "nocluster")
    add_model(
        root,
        "gold/fct_sales.sql",
        "{{ config(materialized='incremental', unique_key='id') }}\nselect 1 as id",
    )
    assert "SSC-PRF-DBTMAT0004" not in rule_ids(
        audit(root)
    ), "clustering rule must not fire when no cluster_by is present"


def test_clustering_fires_for_over_specified_key(tmp_path: Path) -> None:
    """MAT004 still fires when cluster_by has more than the maximum columns."""
    root = write_project(tmp_path / "overcluster")
    add_model(
        root,
        "gold/fct_events.sql",
        """
        {{ config(materialized='table',
                  cluster_by=['event_date', 'user_id', 'event_type', 'session_id', 'region']) }}
        select 1 as event_id
        """,
    )
    hits = suggestions_for(audit(root), "SSC-PRF-DBTMAT0004")
    assert hits, "over-specified cluster_by must still fire MAT004"
    assert (
        "system$clustering_information" in hits[0]["remediation"].lower()
    ), "remediation must point to system$clustering_information"


def test_repo_ground_truth() -> None:
    """
    Assert known-true and known-false suggestions against snowflake-dbt-demo.

    Skipped when run outside the repo so the fixture tests stay portable.
    """
    if not (REPO_ROOT / "dbt_project.yml").is_file():
        print(f"  (skipped: {REPO_ROOT} is not a dbt project)")
        return

    report = audit(REPO_ROOT)
    ids = rule_ids(report)

    def files_for(rule_id: str) -> set[str]:
        return {f["file"] for f in suggestions_for(report, rule_id)}

    # Known-true: a model literally named *_full_reload.
    assert "SSC-PRF-DBTINC0005" in ids
    assert any("full_reload" in f for f in files_for("SSC-PRF-DBTINC0005"))

    # Known-true: models outside a recognised layer folder. ARC001 is a folder
    # rule, not a naming rule, so it survives the naming removal.
    assert any("other/" in f for f in files_for("SSC-EWI-DBTARC0001"))

    # Known-FALSE by design: model and column names are never audited. These IDs
    # are retired, and `DIM__CUSTOMERS` -- uppercase with a double underscore --
    # is the case that proves it, because that may be the name the object had in
    # the source database. See the rules/arc.py docstring.
    assert not suggestions_for(
        report, "SSC-EWI-DBTARC0002"
    ), "ARC002 was removed; it must not fire"
    assert not suggestions_for(
        report, "SSC-EWI-DBTARC0008"
    ), "ARC008 was removed; it must not fire"
    assert not suggestions_for(
        report, "SSC-EWI-DBTARC0010"
    ), "column naming is not audited"
    naming_free = {
        f["file"]
        for f in report["suggestions"]
        if "DIM__CUSTOMERS" in f["file"] and f["category"] == "ARC"
    }
    assert not any(
        f["rule_id"] in ("SSC-EWI-DBTARC0002", "SSC-EWI-DBTARC0008")
        for f in report["suggestions"]
        if f["file"] in naming_free
    )

    # Known-true: dbt_artifacts hook wired while its models are disabled.
    assert "SSC-EWI-DBTOPS0001" in ids

    # Known-false: one project with many models is not fragmentation.
    assert not suggestions_for(report, "SSC-EWI-DBTPRJ0001")

    # Known-false: no conversion markers here, so nothing is suppressed.
    assert report["suppressed"]["count"] == 0
    assert not any(f["category"] == "MIG" for f in report["suggestions"])

    # The manifest is committed in this repo, so graph rules must have run.
    assert report["summary"]["rules_skipped"] == 0, report["skipped_checks"]

    # There is deliberately no score and no grade -- a graded verdict asserts
    # something the engine cannot know. Counts and a per-model rate replaced them.
    assert "score" not in report["summary"], "score was removed; do not reintroduce it"
    assert "grade" not in report["summary"], "grade was removed; do not reintroduce it"
    assert report["summary"]["counts"]["total"] > 0
    assert report["summary"]["per_model"] > 0


def test_stream_model_needs_no_watermark(tmp_path: Path) -> None:
    """
    A Snowflake stream tracks its own consumption offset.

    Regression guard: INC009/INC013 originally fired on CDC models reading a
    stream, which is wrong -- a stream only ever yields unconsumed rows, so a
    {{ this }} watermark would be redundant.
    """
    root = write_project(tmp_path / "streams")
    add_model(
        root,
        "bronze/stg_customer_cdc_stream.sql",
        """
        {{ config(materialized='incremental', unique_key='customer_id',
                  incremental_strategy='merge') }}
        select customer_id, metadata$action as cdc_action
        from {{ source('raw', 'customer_stream') }}
        {% if is_incremental() %}
        where metadata$action = 'INSERT'
        {% endif %}
        """,
    )
    ids = rule_ids(audit(root))
    assert (
        "SSC-PRF-DBTINC0009" not in ids
    ), "stream-based CDC model must not be flagged for no watermark"
    assert "SSC-PRF-DBTINC0013" not in ids


def test_macro_generated_columns_not_flagged(tmp_path: Path) -> None:
    """
    Regression guard for INC011.

    When the column list is produced by a macro it does not exist in the file
    text, so every merge_exclude_columns entry looks absent. Suppress rather than
    emit suggestions that cannot be verified from the source.
    """
    root = write_project(tmp_path / "macrogen")
    (root / "macros").mkdir()
    (root / "macros" / "get_scd_sql.sql").write_text(
        "{% macro get_scd_sql(rel) %}select 1 as dbt_inserted_at{% endmacro %}",
        encoding="utf-8",
    )
    add_model(
        root,
        "gold/dim_customers.sql",
        """
        {{ config(materialized='incremental', unique_key='customer_id',
                  incremental_strategy='merge',
                  merge_exclude_columns=['dbt_inserted_at']) }}
        {{ get_scd_sql(ref('stg_c')) }}
        """,
    )
    add_model(root, "bronze/stg_c.sql", "select 1 as customer_id")
    assert "SSC-FDM-DBTINC0011" not in rule_ids(
        audit(root)
    ), "columns generated by a macro cannot be verified from file text and must not be flagged"


def test_no_cte_structure_fires_on_complex_flat_model(tmp_path: Path) -> None:
    """SQL011, carried over from dbt-validation SQL002."""
    root = write_project(tmp_path / "flatsql")
    add_model(
        root,
        "gold/fct_totals.sql",
        """
        select o.order_date, sum(o.amount) as total_amount, c.region
        from {{ ref('stg_o') }} o
        join {{ ref('stg_c') }} c on c.id = o.customer_id
        group by o.order_date, c.region
        """,
    )
    add_model(root, "bronze/stg_o.sql", "select 1 as customer_id")
    add_model(root, "bronze/stg_c.sql", "select 1 as id")
    assert "SSC-EWI-DBTSQL0011" in rule_ids(audit(root))


def test_no_cte_structure_stays_quiet_on_simple_and_staging(tmp_path: Path) -> None:
    """
    The narrowing guards. A flat model doing nothing complex needs no CTE, and a
    staging model is meant to be a flat one-to-one projection -- flagging either
    would make the rule noise.
    """
    root = write_project(tmp_path / "simplesql")
    add_model(
        root,
        "gold/dim_passthrough.sql",
        "select id, name from {{ ref('stg_x') }} where is_active",
    )
    add_model(
        root,
        "bronze/stg_x.sql",
        """
        select id, name, is_active
        from {{ source('raw', 't') }}
        join {{ source('raw', 'u') }} on u.id = t.id
        """,
    )
    assert "SSC-EWI-DBTSQL0011" not in rule_ids(
        audit(root)
    ), "simple model and staging must not fire"


def test_key_column_untested_respects_composite_model_level_key(tmp_path: Path) -> None:
    """
    TST012, carried over from dbt-validation YAML002.

    The composite-key case is the whole reason this reuses _model_level_key_covers:
    a key declared once at model level with column_names must count as testing every
    column it names, or the rule fires hardest on the models most likely to be right.
    """
    root = write_project(tmp_path / "keycols")
    add_model(
        root,
        "gold/fct_bridge.sql",
        "select 1 as order_id, 2 as product_id, 3 as amount",
    )
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: fct_bridge
                description: Bridge table.
                tests:
                  - dbt_constraints.primary_key:
                      column_names: [order_id, product_id]
                columns:
                  - name: order_id
                    description: Order.
                  - name: product_id
                    description: Product.
                  - name: amount
                    description: Amount.
            """).strip(),
        encoding="utf-8",
    )
    assert "SSC-EWI-DBTTST0012" not in rule_ids(
        audit(root)
    ), "composite key declared at model level must count as tested"


def test_key_column_untested_fires_on_bare_key(tmp_path: Path) -> None:
    root = write_project(tmp_path / "barekey")
    add_model(root, "gold/fct_sales.sql", "select 1 as sale_id, 2 as customer_id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: fct_sales
                description: Sales.
                columns:
                  - name: sale_id
                    description: Sale key.
                    tests:
                      - dbt_constraints.primary_key
                  - name: customer_id
                    description: Customer reference.
            """).strip(),
        encoding="utf-8",
    )
    hits = suggestions_for(audit(root), "SSC-EWI-DBTTST0012")
    assert hits, "an untested foreign key must fire even when the PK is tested"
    assert hits[0]["context"]["untested_columns"] == ["customer_id"]


def test_placeholder_model_detection_and_guards(tmp_path: Path) -> None:
    """
    MIG008, carried over from dbt-validation migration/checker.py, with its two
    false-positive classes fixed: a bare `null::` cast and the word "placeholder"
    appearing in prose must not count.
    """
    root = write_project(tmp_path / "placeholders")
    # Conversion markers make this a migrated project, which MIG rules require.
    add_model(
        root,
        "staging/stg_raw__SQ_X.sql",
        """
        --** SSC-FDM-INF0015 - UPDATE STRATEGY LOGIC HAS BEEN MOVED. **
        select 1 as id
        """,
    )
    add_model(
        root,
        "staging/pending_model.sql",
        """
        -- Status: placeholder
        select null as id where false
        """,
    )
    add_model(
        root,
        "staging/real_model.sql",
        """
        -- This is not a placeholder, despite mentioning the word.
        select null::integer as maybe_id, 1 as id from {{ ref('stg_raw__SQ_X') }}
        """,
    )
    report = audit(root)
    files = {f["file"] for f in suggestions_for(report, "SSC-EWI-DBTMIG0008")}
    assert any("pending_model" in f for f in files), "real placeholder must fire"
    assert not any(
        "real_model" in f for f in files
    ), "null:: cast and the word 'placeholder' in prose must not count"


def test_single_file_mode_scopes_correctly(tmp_path: Path) -> None:
    """
    Single-file mode runs model-scoped rules for the target and reports the rest as
    skipped rather than passed.

    The skipped-not-passed distinction is the point: SQL001 chooses between a CTE and
    an ephemeral model by fingerprinting across every model, so one file cannot
    answer it. Reporting it clean would assert something never checked.
    """
    root = write_project(tmp_path / "single")
    add_model(
        root,
        "gold/fct_events.sql",
        """
        {{ config(materialized='incremental') }}
        select event_id from {{ ref('stg_events') }}
        """,
    )
    add_model(root, "bronze/stg_events.sql", "select 1 as event_id")

    target = root / "models" / "gold" / "fct_events.sql"
    result = run_single_file(build_portfolio(root), target)

    ids = {f.rule_id for f in result.suggestions}
    assert (
        "SSC-PRF-DBTINC0006" in ids
    ), "model-scoped rules must run for the target file"
    assert all(
        f.file.endswith("fct_events.sql") for f in result.suggestions
    ), "only the target file may produce suggestions"

    skipped = {s.rule_id for s in result.skipped}
    assert (
        "SSC-EWI-DBTSQL0001" in skipped
    ), "project-scoped rules must be skipped, not passed"
    assert (
        "SSC-EWI-DBTPRJ0001" in skipped
    ), "portfolio-scoped rules must be skipped, not passed"


def test_single_file_mode_ignores_non_model(tmp_path: Path) -> None:
    """A path that is not a model yields nothing, so the hook stays quiet."""
    root = write_project(tmp_path / "nonmodel")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    result = run_single_file(build_portfolio(root), root / "dbt_project.yml")
    assert not result.suggestions
    assert not result.projects


def test_superseded_yaml_rules_have_successors(tmp_path: Path) -> None:
    """
    Parity gate for the dbt-validation YAML rules that were superseded rather than
    migrated. Deleting that package is only safe if each successor demonstrably
    fires on the same input.

        YAML001 (missing description)      -> DOC001 / DOC003
        YAML004 (missing column desc)      -> DOC002
        YAML006 (prefer dbt_constraints)   -> TST005
    """
    root = write_project(tmp_path / "yamlparity")
    add_model(
        root,
        "gold/dim_thing.sql",
        "select 1 as thing_id, 'a' as name, 2 as size, 3 as weight",
    )
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            sources:
              - name: raw_src
                tables:
                  - name: things
            models:
              - name: dim_thing
                columns:
                  - name: thing_id
                    tests:
                      - unique
                      - not_null
                  - name: name
                  - name: size
                  - name: weight
            """).strip(),
        encoding="utf-8",
    )
    ids = rule_ids(audit(root))
    assert "SSC-EWI-DBTDOC0001" in ids, "YAML001 successor: missing model description"
    assert "SSC-EWI-DBTDOC0003" in ids, "YAML001 successor: missing source description"
    assert (
        "SSC-EWI-DBTDOC0002" in ids
    ), "YAML004 successor: column documentation coverage"
    assert (
        "SSC-EWI-DBTTST0005" in ids
    ), "YAML006 successor: prefer dbt_constraints over unique+not_null"


def test_cli_entry_points_are_wired(tmp_path: Path) -> None:
    """
    Both console entry points must actually invoke their Typer app.

    This exists because ``main()`` was once left with a docstring and no body. Every
    rule test still passed, because they call the engine directly, so the CLI shipped
    as a silent no-op: exit 0, no output, indistinguishable from success. Asserting
    the entry points produce output is the cheapest guard against that recurring.

    ``--help`` is the probe for ``validate_main`` rather than a real file, because a
    clean model correctly produces no output -- so silence there would be ambiguous,
    which is exactly the ambiguity this test exists to remove. The suggestions path is
    covered by ``test_single_file_mode_scopes_correctly``.
    """
    import contextlib
    import io

    from dbt_quality.cli import main, validate_main

    root = write_project(tmp_path / "clismoke")
    add_model(root, "gold/dim_a.sql", "select 1 as id")

    for entry, argv in (
        (main, ["dbt-audit", "rules"]),
        (validate_main, ["dbt-validate", "--help"]),
    ):
        out, err = io.StringIO(), io.StringIO()
        saved = sys.argv
        sys.argv = argv
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                with contextlib.suppress(SystemExit):
                    entry()
        finally:
            sys.argv = saved
        assert (out.getvalue() + err.getvalue()).strip(), (
            f"{entry.__name__} produced no output for {argv!r}; "
            "the entry point is not wired to its Typer app"
        )


def test_every_suggestion_has_a_line(tmp_path: Path) -> None:
    """
    No suggestion may ship without a line number.

    This is the invariant the linter depends on: a diagnostic with no line cannot be
    placed in an editor. Before the anchor layer existed only 29% of suggestions had
    one, and the regression is silent -- the report still renders, the linter just
    quietly loses rows. Hence an explicit guard.
    """
    root = write_project(tmp_path / "lines")
    add_model(
        root,
        "gold/fct_a.sql",
        """
        {{ config(materialized='incremental') }}
        select o.id, sum(o.amt) as amt
        from {{ ref('stg_b') }} o
        join {{ ref('stg_c') }} c on c.id = o.id
        group by o.id
        """,
    )
    add_model(root, "bronze/stg_b.sql", "select 1 as id, 2 as amt")
    add_model(root, "bronze/stg_c.sql", "select 1 as id")
    report = audit(root)
    missing = [s for s in report["suggestions"] if not s.get("line")]
    assert not missing, f"{len(missing)} suggestion(s) have no line: {missing[:3]}"
    assert all(s["line"] >= 1 for s in report["suggestions"])


def test_lint_lines_parse_with_the_problem_matcher_regex(tmp_path: Path) -> None:
    """
    Every lint line must match the regex in `.vscode/tasks.json`.

    The linter's output format and the editor's matcher are a contract split across
    two files, so a change to either silently breaks the Problems panel with no
    error anywhere. This asserts them against each other, reading the regex from
    tasks.json rather than restating it -- a copy here would drift.
    """
    import json as _json
    import re as _re

    from dbt_quality.cli import _lint_line

    tasks_file = REPO_ROOT / ".vscode" / "tasks.json"
    if not tasks_file.is_file():
        print(f"  (skipped: {tasks_file} not present)")
        return
    tasks = _json.loads(tasks_file.read_text(encoding="utf-8"))
    spec = next(
        t["problemMatcher"]["pattern"]
        for t in tasks["tasks"]
        if isinstance(t.get("problemMatcher"), dict)
    )
    matcher = _re.compile(spec["regexp"])
    # Read the group indices from the same pattern block rather than hard-coding
    # them. Fixed indices here were themselves a drift: they still named the
    # 3-field layout after the end-position fields shipped, so this test failed
    # against a correct tasks.json.
    severity_group = spec["severity"]
    code_group = spec["code"]

    root = write_project(tmp_path / "lintfmt")
    add_model(
        root,
        "gold/fct_x.sql",
        """
        {{ config(materialized='incremental', incremental_strategy='merge') }}
        select a.id, count(*) as n from {{ ref('stg_y') }} a group by a.id
        """,
    )
    add_model(root, "bronze/stg_y.sql", "select 1 as id")

    result = run_audit(build_portfolio(root))
    active = [s for s in result.suggestions if not s.suppressed]
    assert active, "fixture produced no suggestions, so this test would prove nothing"

    for suggestion in active:
        line = _lint_line(suggestion, root)
        assert "\n" not in line, "a lint line must not contain a newline"
        match = matcher.match(line)
        assert match, f"tasks.json regex did not match: {line[:160]}"
        assert match.group(severity_group) in ("error", "warning", "info")
        assert match.group(code_group) == suggestion.rule_id


def test_lint_tokens_cover_every_level() -> None:
    """
    Each level maps to a token a problem matcher recognises.

    A level with no mapping would silently fall back to `info`, quietly demoting
    something meant to stand out. `error` IS reachable now: under the EWI vocabulary
    `Level.ERROR` means genuinely wrong, not merely worth checking, so it deserves
    the matcher's error token rather than being softened to a warning.
    """
    from dbt_quality.core.base import LEVEL_RANK, LINT_TOKENS, Level

    assert set(LINT_TOKENS) == set(LEVEL_RANK), "every level needs a lint token"
    assert set(LINT_TOKENS.values()) <= {"error", "warning", "info"}
    assert LINT_TOKENS[Level.ERROR] == "error"
    assert LINT_TOKENS[Level.WARNING] == "warning"
    assert LINT_TOKENS[Level.INFORMATION] == "info"


def test_lint_targets_are_always_real_files(tmp_path: Path) -> None:
    """
    Every lint diagnostic must name a file that exists.

    Project-scoped rules legitimately describe a directory (`models/`) or nothing at
    all, but an editor cannot open a directory as a diagnostic target -- the row would
    simply do nothing when clicked. Those are redirected to `dbt_project.yml`.
    """
    from dbt_quality.cli import _lint_relative

    root = write_project(tmp_path / "targets")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    result = run_audit(build_portfolio(root))
    active = [s for s in result.suggestions if not s.suppressed]
    assert active, "fixture produced no suggestions, so this test would prove nothing"

    for suggestion in active:
        target = root / _lint_relative(suggestion, root)
        assert (
            target.is_file()
        ), f"{suggestion.rule_id} points at {target}, which is not a file"


def test_every_code_follows_the_ssc_format() -> None:
    """
    Every registered rule code matches SSC-{EWI|FDM|PRF}-DBT{CAT}{NNNN}, is unique,
    and its category segment agrees with the rule's declared category.

    The category check guards a specific landmine: the registry used to derive a
    category with `rule_id[:3]`, which under this scheme is `"SSC"` for every rule.
    That would collapse all ten categories into one and raise nothing -- the report
    would simply become quietly wrong.
    """
    from dbt_quality.core.base import CODE_PATTERN, REGISTRY, parse_code

    assert REGISTRY, "no rules registered"
    for rule_id, meta in REGISTRY.items():
        assert CODE_PATTERN.match(rule_id), f"{rule_id} is not a valid SSC code"
        kind, category, number = parse_code(rule_id)
        assert kind == meta.kind, f"{rule_id}: code kind {kind} != {meta.kind}"
        assert (
            category == meta.category
        ), f"{rule_id}: code category {category} != declared {meta.category}"
        assert number > 0
    assert len(set(REGISTRY)) == len(REGISTRY), "duplicate rule codes"

    retired = {"SSC-EWI-DBTARC0002", "SSC-EWI-DBTARC0008"}
    assert not (retired & set(REGISTRY)), (
        "ARC0002/ARC0008 were retired with the model-name rules; the numbers are a "
        "deliberate gap and must not be reissued"
    )


def test_every_rule_declares_kind_level_and_severity() -> None:
    """All three axes are populated, and each uses a value from its own vocabulary."""
    from dbt_quality.core.base import LEVEL_RANK, REGISTRY, SEVERITY_RANK, Kind

    kinds = {Kind.EWI, Kind.FDM, Kind.PRF}
    for rule_id, meta in REGISTRY.items():
        assert meta.kind in kinds, f"{rule_id}: bad kind {meta.kind!r}"
        assert meta.default_level in LEVEL_RANK, f"{rule_id}: bad level"
        assert meta.default_severity in SEVERITY_RANK, f"{rule_id}: bad severity"


def test_error_level_implies_a_direct_message(tmp_path: Path) -> None:
    """
    The invariant tying the levels to the prose: an `error` states a fact, an
    `information` states a check.

    A rule cannot claim certainty in its level while hedging in its message, or the
    reverse -- that combination is what made the old output impossible to triage.
    Checked on emitted messages rather than on source, so conditional branches are
    covered too.

    Suggestions carrying `vendor_text` are exempt. Their message is the conversion
    tool's own description quoted verbatim, so it is evidence rather than a claim
    this engine authors, and its wording is outside our control -- SnowConvert
    already ships strings like "REVIEW AND ADJUST MANUALLY IF NEEDED". Policing it
    here would break the suite on an upstream wording change that is not a defect.
    """
    from dbt_quality.core.base import Level

    hedges = ("check whether", "confirm ", "consider whether", "worth ")
    root = write_project(tmp_path / "levels")
    add_model(root, "gold/dim_a.sql", "select 1 as id from analytics.public.t")
    result = run_audit(build_portfolio(root))

    for suggestion in result.suggestions:
        if suggestion.context.get("vendor_text"):
            continue
        lowered = suggestion.message.lower()
        if suggestion.level == Level.ERROR:
            assert not any(h in lowered for h in hedges), (
                f"{suggestion.rule_id} is an error but its message hedges: "
                f"{suggestion.message[:90]}"
            )


def test_validate_never_blocks_a_save(tmp_path: Path) -> None:
    """
    Single-file validation always exits 0, even on an error-level suggestion.

    A save-time hook that fails mid-refactor gets switched off, after which it
    protects nothing. Errors are gated in CI with `dbt-lint --strict` instead.
    """
    import contextlib
    import io

    from dbt_quality.cli import validate_main

    root = write_project(tmp_path / "noblock")
    # A literal relation reference is SSC-EWI-DBTSQL0006, an information-level rule.
    add_model(root, "gold/dim_x.sql", "select a.id from analytics.public.customers a")
    target = root / "models" / "gold" / "dim_x.sql"

    saved_argv = sys.argv
    sys.argv = ["dbt-validate", "--simple", str(target)]
    code = 0
    try:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            try:
                validate_main()
            except SystemExit as exc:
                code = int(exc.code or 0)
    finally:
        sys.argv = saved_argv

    assert code == 0, f"validate exited {code}; nothing should block a save"


def test_every_rule_has_metadata() -> None:
    """Guard against a rule registered without the text the report needs."""
    for meta in REGISTRY.values():
        assert meta.title, f"{meta.rule_id} has no title"
        assert meta.category, f"{meta.rule_id} has no category"
        assert meta.rationale, f"{meta.rule_id} has no rationale for the report"


def test_audit_hook_only_fires_for_manifest_producing_dbt_commands() -> None:
    """
    The audit hook fires on every bash call -- hooks.json matches on tool name,
    not command text -- so its own regex is the only filter. It must require a
    subcommand that rewrites the manifest, or every unrelated command starts an
    audit.
    """
    import importlib.util

    hook = SCRIPTS.parent / "hooks" / "audit_after_dbt.py"
    spec = importlib.util.spec_from_file_location("_audit_hook", hook)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pattern = module.DBT_INVOCATION

    for command in (
        "dbt run",
        "dbt build",
        "dbt parse",
        "uv run dbt build",
        "dbt --profiles-dir ~/.dbt run",
        "cd /repo && dbt build --select foo",
        "DBT_PROFILES_DIR=~/.dbt dbt test",
    ):
        assert pattern.search(command), f"should match: {command}"

    for command in (
        "dbt debug",
        "dbt deps",
        "dbt --version",
        "cortex plugin update dbt-quality",
        "cd /Users/me/snowflake-dbt-demo && ls",
        "grep -r dbt_quality .",
        "echo 'remember to run the build later'",
        "echo dbt build",
        "git commit -m 'dbt build'",
        "python -c 'print(\"dbt parse\")'",
        "dbt-quality build",
        "dbt-build run",
    ):
        assert not pattern.search(command), f"should not match: {command}"


def test_task_bootstrap_explains_how_to_start_existing_watcher(tmp_path: Path) -> None:
    """A configured watcher tells the current session how to activate it."""
    import contextlib
    import importlib.util
    import io
    import json

    project_root = write_project(tmp_path / "watcher")
    hook = SCRIPTS.parent / "hooks" / "setup_vscode_task.py"
    spec = importlib.util.spec_from_file_location("_task_bootstrap", hook)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_stdin = sys.stdin
    try:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            sys.stdin = io.StringIO(json.dumps({"cwd": str(project_root)}))
            assert module.main() == 0
        assert "added the lint task" in output.getvalue()

        with contextlib.redirect_stdout(io.StringIO()) as output:
            sys.stdin = io.StringIO(json.dumps({"cwd": str(project_root)}))
            assert module.main() == 0
        assert "five-minute watcher is already configured" in output.getvalue()
        assert "Reload the window or run" in output.getvalue()
    finally:
        sys.stdin = original_stdin


def test_task_bootstrap_adds_missing_watcher_to_partial_configuration(
    tmp_path: Path,
) -> None:
    """Existing one-shot tasks do not prevent the periodic watcher from being added."""
    import contextlib
    import importlib.util
    import io
    import json

    project_root = write_project(tmp_path / "partial-watcher")
    tasks_path = project_root / ".vscode" / "tasks.json"
    tasks_path.parent.mkdir()
    tasks_path.write_text(
        json.dumps(
            {"version": "2.0.0", "tasks": [{"label": "dbt: quality suggestions"}]}
        ),
        encoding="utf-8",
    )
    hook = SCRIPTS.parent / "hooks" / "setup_vscode_task.py"
    spec = importlib.util.spec_from_file_location("_task_bootstrap_partial", hook)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_stdin = sys.stdin
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            sys.stdin = io.StringIO(json.dumps({"cwd": str(project_root)}))
            assert module.main() == 0
    finally:
        sys.stdin = original_stdin

    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))["tasks"]
    labels = {task["label"] for task in tasks}
    assert labels == {
        "dbt: quality suggestions",
        "dbt: quality suggestions (watch, every 5 min)",
    }
    watcher = next(task for task in tasks if "watch" in task["label"])
    assert watcher["runOptions"] == {"runOn": "folderOpen"}
    assert watcher["problemMatcher"]["background"]["activeOnStart"] is True


def test_microbatch_no_guard_stays_silent(tmp_path: Path) -> None:
    """
    microbatch manages its own incremental filter; INC006/INC009/INC013 must not fire.

    Regression guard: before the microbatch early-returns, these rules fired on
    every microbatch model, which is always missing an is_incremental() guard by design.
    """
    root = write_project(tmp_path / "microbatch")
    add_model(
        root,
        "gold/fct_events.sql",
        """
        {{ config(materialized='incremental', incremental_strategy='microbatch',
                  unique_key='event_id', event_time='created_at',
                  begin='2020-01-01') }}
        select event_id, created_at from {{ ref('stg_events') }}
        """,
    )
    add_model(
        root,
        "bronze/stg_events.sql",
        "select 1 as event_id, current_timestamp() as created_at",
    )
    ids = rule_ids(audit(root))
    assert (
        "SSC-PRF-DBTINC0006" not in ids
    ), "microbatch model must not fire INC006 (no is_incremental guard)"
    assert (
        "SSC-PRF-DBTINC0009" not in ids
    ), "microbatch model must not fire INC009 (no watermark)"
    assert (
        "SSC-PRF-DBTINC0013" not in ids
    ), "microbatch model must not fire INC013 (unbounded scan)"


def test_stream_no_guard_stays_silent(tmp_path: Path) -> None:
    """
    A stream-reading model consumes only unconsumed rows, so INC006 must not fire.

    test_stream_model_needs_no_watermark covers INC009/INC013; this test closes
    the gap for INC006 specifically.
    """
    root = write_project(tmp_path / "streamguard")
    add_model(
        root,
        "bronze/stg_orders_cdc.sql",
        """
        {{ config(materialized='incremental', unique_key='order_id',
                  incremental_strategy='merge') }}
        select order_id, metadata$action as cdc_action
        from {{ source('raw', 'orders_stream') }}
        """,
    )
    ids = rule_ids(audit(root))
    assert (
        "SSC-PRF-DBTINC0006" not in ids
    ), "stream model without is_incremental() must not fire INC006"


def test_conditional_aggregation_no_mac009(tmp_path: Path) -> None:
    """
    sum(case when) is no longer in the MAC009 scope after pivot removal.

    Regression guard: before removal the pivot pattern fired on every CASE-based
    conditional aggregation, which is a standard SQL pattern that needs no macro.
    """
    root = write_project(tmp_path / "condagg")
    add_model(
        root,
        "gold/fct_pivot.sql",
        """
        select
            customer_id,
            sum(case when status = 'shipped' then 1 else 0 end) as shipped_count,
            sum(case when status = 'pending' then 1 else 0 end) as pending_count
        from {{ ref('stg_orders') }}
        group by customer_id
        """,
    )
    add_model(
        root, "bronze/stg_orders.sql", "select 1 as customer_id, 'shipped' as status"
    )
    assert "SSC-EWI-DBTMAC0009" not in rule_ids(
        audit(root)
    ), "conditional aggregation must not fire MAC009 after pivot pattern removal"


def test_union_without_all_fires_sql0012(tmp_path: Path) -> None:
    root = write_project(tmp_path / "union")
    add_model(
        root,
        "gold/combined.sql",
        "select customer_id from {{ ref('customers_a') }} union select customer_id from {{ ref('customers_b') }}",
    )
    add_model(root, "bronze/customers_a.sql", "select 1 as customer_id")
    add_model(root, "bronze/customers_b.sql", "select 2 as customer_id")
    hits = suggestions_for(audit(root), "SSC-EWI-DBTSQL0012")
    assert len(hits) == 1
    assert hits[0]["level"] == "information"
    assert "duplicate-elimination work" in hits[0]["message"]


def test_union_all_and_stripped_literals_stay_silent(tmp_path: Path) -> None:
    root = write_project(tmp_path / "union_all")
    add_model(
        root,
        "gold/combined.sql",
        """
        -- union is documented here only
        select 'union' as label from {{ ref('customers_a') }}
        union all
        select 'union all' as label from {{ ref('customers_b') }}
        """,
    )
    add_model(root, "bronze/customers_a.sql", "select 1 as customer_id")
    add_model(root, "bronze/customers_b.sql", "select 2 as customer_id")
    assert "SSC-EWI-DBTSQL0012" not in rule_ids(audit(root))


def test_select_distinct_fires_sql0013(tmp_path: Path) -> None:
    root = write_project(tmp_path / "distinct")
    add_model(
        root,
        "gold/customers.sql",
        "select distinct customer_id from {{ ref('stg_customers') }}",
    )
    add_model(root, "bronze/stg_customers.sql", "select 1 as customer_id")
    hits = suggestions_for(audit(root), "SSC-EWI-DBTSQL0013")
    assert len(hits) == 1
    assert hits[0]["level"] == "information"
    assert "qualify" in hits[0]["message"].lower()


def test_select_distinct_in_comment_or_literal_stays_silent(tmp_path: Path) -> None:
    root = write_project(tmp_path / "distinct_literal")
    add_model(
        root,
        "gold/customers.sql",
        """
        -- select distinct would deduplicate rows
        select 'select distinct' as note from {{ ref('stg_customers') }}
        """,
    )
    add_model(root, "bronze/stg_customers.sql", "select 1 as customer_id")
    assert "SSC-EWI-DBTSQL0013" not in rule_ids(audit(root))


def test_snowflake_hash_functions_on_fk_fields_fire_mac009(tmp_path: Path) -> None:
    """
    Hashing key fields fires MAC009 with a Snowflake-pruning focused message.

    The message must explain the Snowflake pruning consequence so reviewers know
    the concern is hash keys used for joins, not hash-diff change detection.
    """
    functions = (
        "HASH(order_id, customer_id)",
        "MD5(order_id)",
        "MD5_BINARY(order_id)",
        "SHA1(order_id)",
        "SHA1_BINARY(order_id)",
        "SHA2(order_id, 256)",
        "SHA2_BINARY(order_id, 256)",
    )
    for index, expression in enumerate(functions):
        root = write_project(tmp_path / f"hashfk_{index}")
        add_model(
            root,
            "gold/dim_orders.sql",
            f"""
            select
                {expression} as order_key,
                order_id,
                customer_id
            from {{{{ ref('stg_orders') }}}}
            """,
        )
        add_model(
            root, "bronze/stg_orders.sql", "select 1 as order_id, 2 as customer_id"
        )
        hits = suggestions_for(audit(root), "SSC-EWI-DBTMAC0009")
        assert hits, f"{expression} over a foreign-key field must fire MAC009"
        message = hits[0]["message"].lower()
        assert (
            "prun" in message and "join" in message
        ), f"MAC009 message should explain Snowflake join pruning; got: {message[:120]}"


def test_hash_diff_without_key_fields_stays_silent(tmp_path: Path) -> None:
    """A hash-diff over non-key attributes is valid change-detection logic."""
    root = write_project(tmp_path / "hashdiff")
    add_model(
        root,
        "gold/dim_customer_changes.sql",
        """
        select
            hash(customer_name, customer_address, market_segment) as cdc_hash,
            customer_name
        from {{ ref('stg_customers') }}
        """,
    )
    add_model(root, "bronze/stg_customers.sql", "select 'Ada' as customer_name")
    assert "SSC-EWI-DBTMAC0009" not in rule_ids(audit(root))


def test_disabled_rule_is_skipped_in_full_audit(tmp_path: Path) -> None:
    root = write_project(
        tmp_path / "disabled",
        project_yml="""
        name: 'fixture'
        version: '1.0.0'
        profile: 'fixture'
        models:
          fixture:
            +materialized: view
        """,
    )
    (root / ".dbt-quality.yml").write_text(
        "disabled_rules:\n  - SSC-EWI-DBTSQL0006\n", encoding="utf-8"
    )
    add_model(root, "gold/literal_relation.sql", "select * from PROD.PUBLIC.ORDERS")
    report = audit(root)
    assert "SSC-EWI-DBTSQL0006" not in rule_ids(report)
    assert "SSC-EWI-DBTSQL0006" in skipped_rule_ids(report)


def test_disabled_rule_is_skipped_in_single_file_validation(tmp_path: Path) -> None:
    root = write_project(tmp_path / "disabled_single")
    (root / ".dbt-quality.yml").write_text(
        "disabled_rules:\n  - SSC-EWI-DBTSQL0006\n", encoding="utf-8"
    )
    relative = "gold/literal_relation.sql"
    add_model(root, relative, "select * from PROD.PUBLIC.ORDERS")
    result = run_single_file(build_portfolio(root), root / "models" / relative)
    assert not any(f.rule_id == "SSC-EWI-DBTSQL0006" for f in result.suggestions)
    assert any(f.rule_id == "SSC-EWI-DBTSQL0006" for f in result.skipped)


def test_embedded_ewi_estate_exercises_every_active_ewi(tmp_path: Path) -> None:
    """The committed estate is the integration fixture for every active EWI rule."""
    from dbt_quality.core.base import Kind

    report = audit(copy_fixture(tmp_path, "ewi_estate"))
    registered = {
        rule_id for rule_id, meta in REGISTRY.items() if meta.kind == Kind.EWI
    }
    active = {
        finding["rule_id"]
        for finding in report["suggestions"]
        if not finding.get("suppressed")
        and REGISTRY[finding["rule_id"]].kind == Kind.EWI
    }
    assert not report["errors"], report["errors"]
    assert registered == EXPECTED_EWI_RULE_IDS, (
        "update the fixture EWI inventory: "
        f"missing={sorted(registered - EXPECTED_EWI_RULE_IDS)}, "
        f"stale={sorted(EXPECTED_EWI_RULE_IDS - registered)}"
    )
    assert active == EXPECTED_EWI_RULE_IDS, (
        "fixture estate EWI output changed: "
        f"missing={sorted(EXPECTED_EWI_RULE_IDS - active)}, "
        f"unexpected={sorted(active - EXPECTED_EWI_RULE_IDS)}"
    )


# =============================================================================
# Standalone runner (no pytest required)
# =============================================================================


# =============================================================================
# Focused regression tests for targeted fixes
# =============================================================================


def test_persist_docs_all_false_not_enabled(tmp_path: Path) -> None:
    """persist_docs with relation:false and columns:false must not suppress DOC004."""
    root = write_project(
        tmp_path / "pd_false",
        project_yml=textwrap.dedent("""
            name: 'pd_false'
            version: '1.0.0'
            profile: 'pd_false'
            models:
              pd_false:
                +persist_docs:
                  relation: false
                  columns: false
                +materialized: view
            """).strip(),
    )
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: dim_a
                description: A model.
            """).strip(),
        encoding="utf-8",
    )
    # Should fire because all-false persist_docs is not enabled
    assert "SSC-EWI-DBTDOC0004" in rule_ids(audit(root))


def test_persist_docs_relation_true_is_enabled(tmp_path: Path) -> None:
    """persist_docs with relation:true must suppress DOC004."""
    root = write_project(
        tmp_path / "pd_true",
        project_yml=textwrap.dedent("""
            name: 'pd_true'
            version: '1.0.0'
            profile: 'pd_true'
            models:
              pd_true:
                +persist_docs:
                  relation: true
                  columns: false
                +materialized: view
            """).strip(),
    )
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: dim_a
                description: A model.
            """).strip(),
        encoding="utf-8",
    )
    assert "SSC-EWI-DBTDOC0004" not in rule_ids(audit(root))


def test_missing_packages_requires_constraints_and_semantic_view(
    tmp_path: Path,
) -> None:
    """PRJ007 must fire for dbt_constraints and dbt_semantic_view; not dbt_utils."""
    root = write_project(tmp_path / "nopkgs")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    # Add dbt_utils only -- the old baseline, now no longer required
    (root / "packages.yml").write_text(
        textwrap.dedent("""
            packages:
              - package: dbt-labs/dbt_utils
                version: [">=1.0.0", "<2.0.0"]
            """).strip(),
        encoding="utf-8",
    )
    hits = suggestions_for(audit(root), "SSC-EWI-DBTPRJ0007")
    assert (
        hits
    ), "PRJ007 must fire when dbt_constraints and dbt_semantic_view are absent"
    missing = hits[0]["context"]["missing"]
    assert "Snowflake-Labs/dbt_constraints" in missing
    assert "Snowflake-Labs/dbt_semantic_view" in missing
    # dbt_utils is no longer required and must not appear in missing
    assert not any("dbt_utils" in m for m in missing)


def test_missing_packages_silent_when_both_present(tmp_path: Path) -> None:
    """PRJ007 must stay silent when both required packages are declared."""
    root = write_project(tmp_path / "allpkgs")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    (root / "packages.yml").write_text(
        textwrap.dedent("""
            packages:
              - package: Snowflake-Labs/dbt_constraints
                version: [">=1.0.0", "<2.0.0"]
              - package: Snowflake-Labs/dbt_semantic_view
                version: [">=1.0.0", "<2.0.0"]
            """).strip(),
        encoding="utf-8",
    )
    assert not suggestions_for(audit(root), "SSC-EWI-DBTPRJ0007")


def test_staging_logic_no_fire_on_multiple_refs_alone(tmp_path: Path) -> None:
    """ARC006 must not fire on a staging model that has multiple refs but no JOIN/aggregation."""
    root = write_project(tmp_path / "multirefs")
    # Two source references but no JOIN keyword and no aggregation
    add_model(
        root,
        "bronze/stg_combo.sql",
        """
        select a, b
        from {{ source('raw', 'left_table') }}
        union all
        select a, b
        from {{ source('raw', 'right_table') }}
        """,
    )
    assert "SSC-EWI-DBTARC0006" not in rule_ids(
        audit(root)
    ), "multiple refs alone without JOIN/aggregation must not fire ARC006"


def test_staging_logic_still_fires_on_join(tmp_path: Path) -> None:
    """ARC006 must still fire when a staging model contains a JOIN."""
    root = write_project(tmp_path / "stgjoin")
    add_model(
        root,
        "bronze/stg_joined.sql",
        """
        select a.id, b.name
        from {{ source('raw', 'a') }} a
        join {{ source('raw', 'b') }} b on a.id = b.id
        """,
    )
    assert "SSC-EWI-DBTARC0006" in rule_ids(audit(root))


def test_etl_instance_pattern_rejects_generic_prefixes() -> None:
    """Generic prefixes (AGG, SEQ, UPD, UNI, SP, TRANS) must not match ETL_INSTANCE_PATTERN."""
    from dbt_quality.provenance import ETL_INSTANCE_PATTERN

    generic = [
        "AGG_totals",
        "SEQ_step1",
        "UPD_customers",
        "UNI_all",
        "SP_load",
        "TRANS_data",
    ]
    for name in generic:
        assert not ETL_INSTANCE_PATTERN.match(
            name
        ), f"generic prefix should not match: {name}"

    # Tool-specific ones must still match
    specific = [
        "SQ_employee",
        "EXP_calc",
        "FIL_active",
        "LKP_region",
        "JNR_merged",
        "RTR_split",
        "SRT_ordered",
        "NRM_flat",
        "MPLT_common",
        "int_UPDTRANS1",
    ]
    for name in specific:
        assert ETL_INSTANCE_PATTERN.match(
            name
        ), f"tool-specific prefix must match: {name}"


# =============================================================================
# Vendor marker text
# =============================================================================
#
# Every marker string below is copied verbatim from the SnowConvert EWI and FDM
# references. They are NOT shaped to suit the parser: the parser exists to read
# what the converter actually emits. If one of these stops parsing, the parser is
# wrong.
#
# This matters because the fixtures previously used `SSC-EWI-INF0001: text` with a
# colon, a form SnowConvert does not emit -- an extractor written against that
# would have parsed nothing on a real converted project with every test green.

#: (label, marker line, expected extracted text)
VENDOR_MARKERS = [
    (
        "resolve-ewi triple-star-bang terminator",
        "-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT"
        " SUPPORTED BY SNOWCONVERT ***/!!!",
        "SSC-EWI-SSIS0001",
        "SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT",
    ),
    (
        "quoted element name preserved",
        "!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT"
        " 'FORLOOP CONTAINER ITERATION LOGIC' CANNOT BE CONVERTED TO SNOWFLAKE"
        " SCRIPTING. ***/!!!",
        "SSC-EWI-SSIS0004",
        "SSIS CONTROL FLOW ELEMENT 'FORLOOP CONTAINER ITERATION LOGIC' CANNOT BE"
        " CONVERTED TO SNOWFLAKE SCRIPTING.",
    ),
    (
        "double-dash double-star comment form",
        "--** SSC-FDM-TS0001 - COLLATION Albanian_BIN NOT SUPPORTED **",
        "SSC-FDM-TS0001",
        "COLLATION Albanian_BIN NOT SUPPORTED",
    ),
    (
        "quadruple-dash commented-out-statement form",
        "----** SSC-FDM-TS0029 - SET NOCOUNT STATEMENT IS COMMENTED OUT, WHICH IS"
        " NOT APPLICABLE IN SNOWFLAKE. **",
        "SSC-FDM-TS0029",
        "SET NOCOUNT STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN"
        " SNOWFLAKE.",
    ),
    (
        "inline block comment, already mixed case",
        "/*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in"
        " certain cases ***/",
        "SSC-FDM-TS0010",
        "CURRENT_DATABASE function has different behavior in certain cases",
    ),
    (
        "generic code with no letter prefix",
        '--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "#temptable" **',
        "SSC-FDM-0007",
        'MISSING DEPENDENT OBJECT "#temptable"',
    ),
]


def test_marker_text_reads_every_real_snowconvert_shape() -> None:
    """All four terminators, both comment styles, and prefixless codes."""
    from dbt_quality.provenance import marker_text

    for label, line, code, expected in VENDOR_MARKERS:
        got = marker_text(line, line.upper().index(code))
        assert got == expected, f"{label}: expected {expected!r}, got {got!r}"


def test_marker_text_strips_every_terminator() -> None:
    """No `***/!!!`, `***/`, `**/` or ` **` residue may reach the message."""
    from dbt_quality.provenance import marker_text

    for label, line, code, _ in VENDOR_MARKERS:
        got = marker_text(line, line.upper().index(code))
        for residue in ("*", "/", "!"):
            assert not got.endswith(residue), f"{label}: terminator residue in {got!r}"


def test_marker_text_does_not_leak_surrounding_json() -> None:
    """
    SSC-EWI-SSIS0026 is emitted inside a JSON string in a task CONFIG block, and
    closes with a single-star `**/`. Capturing to end of line would swallow the
    rest of the JSON into the message.
    """
    from dbt_quality.provenance import marker_text

    line = (
        '    "Data_Flow_Task_stage_path": {"value": "!!!RESOLVE EWI!!! /***'
        " SSC-EWI-SSIS0026 - PROPERTY EXPRESSION 'ConnectionString' IS NOT"
        ' SUPPORTED. **/ @[$Project::FlatFileDir]", "type": "VARCHAR"}'
    )
    got = marker_text(line, line.index("SSC-EWI-SSIS0026"))
    assert got == "PROPERTY EXPRESSION 'ConnectionString' IS NOT SUPPORTED."
    assert "VARCHAR" not in got and "FlatFileDir" not in got


def test_marker_text_is_scoped_to_its_own_line() -> None:
    """
    The same code can appear on several lines with different text. Each occurrence
    must report its own description, not the file's first.
    """
    from dbt_quality.provenance import marker_text

    raw = (
        "--** SSC-EWI-SSIS0004 - FIRST ELEMENT CANNOT BE CONVERTED. **\n"
        "--** SSC-EWI-SSIS0004 - SECOND ELEMENT CANNOT BE CONVERTED. **\n"
    )
    second = raw.index("SSC-EWI-SSIS0004", raw.index("\n"))
    assert marker_text(raw, second) == "SECOND ELEMENT CANNOT BE CONVERTED."


def test_marker_text_returns_empty_for_a_bare_code() -> None:
    """A code with no description must fall back, not report an empty message."""
    from dbt_quality.provenance import marker_text

    line = "-- SSC-EWI-INF0001 marker"
    assert marker_text(line, line.index("SSC-EWI-INF0001")) == ""


def test_vendor_text_is_quoted_verbatim_including_case(tmp_path: Path) -> None:
    """
    The converter's wording reaches the message untouched -- not sentence-cased,
    reflowed, or truncated. Guards against a later "helpful" normalisation.
    """
    root = write_project(tmp_path / "verbatim")
    add_model(
        root,
        "staging/stg_raw__SQ_ORDERS.sql",
        "-- !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT"
        " SUPPORTED BY SNOWCONVERT ***/!!!\n"
        "select 1 as id from {{ source('raw', 'orders') }}",
    )
    hits = suggestions_for(audit(root), "SSC-EWI-DBTMIG0001")
    assert hits, "MIG0001 must fire on a RESOLVE EWI block"
    assert hits[0]["message"] == "SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT"


def test_same_code_with_different_text_is_reported_twice(tmp_path: Path) -> None:
    """
    Deduping on the code alone would report one and silently hide the other.
    SSC-EWI-SSIS0004 names the specific control-flow element, so two occurrences
    are two distinct defects.
    """
    root = write_project(tmp_path / "dedup")
    add_model(
        root,
        "staging/stg_raw__SQ_ITEMS.sql",
        "--** SSC-FDM-INF0015 - FORLOOP CONTAINER LOGIC MOVED. **\n"
        "--** SSC-FDM-INF0015 - FOREACH CONTAINER LOGIC MOVED. **\n"
        "--** SSC-FDM-INF0015 - FORLOOP CONTAINER LOGIC MOVED. **\n"
        "select 1 as id from {{ source('raw', 'items') }}",
    )
    messages = {
        f["message"] for f in suggestions_for(audit(root), "SSC-FDM-DBTMIG0003")
    }
    assert messages == {
        "FORLOOP CONTAINER LOGIC MOVED.",
        "FOREACH CONTAINER LOGIC MOVED.",
    }, f"expected one suggestion per distinct text, got {messages}"


def test_bare_marker_falls_back_to_our_own_wording(tmp_path: Path) -> None:
    """With no vendor description there is nothing to quote, so we say it ourselves."""
    root = write_project(tmp_path / "fallback")
    add_model(
        root,
        "staging/stg_raw__SQ_BARE.sql",
        "-- SSC-EWI-INF0001 marker\n"
        "-- !!!RESOLVE EWI!!!\n"
        "select 1 as id from {{ source('raw', 'bare') }}",
    )
    report = audit(root)
    hits = suggestions_for(report, "SSC-EWI-DBTMIG0002")
    assert hits, "MIG0002 must still fire on a bare code"
    assert "SSC-EWI-INF0001" in hits[0]["message"]
    assert not hits[0].get("context", {}).get("vendor_text")


def test_needs_user_quotes_the_hand_off_note(tmp_path: Path) -> None:
    """The whole value of NEEDS-USER is the instruction the converter left."""
    root = write_project(tmp_path / "needsuser")
    add_model(
        root,
        "staging/stg_raw__SQ_FIL.sql",
        "-- NEEDS-USER: Verify sort order matches original mapping\n"
        "--** SSC-FDM-INF0042 - NULL HANDLING DIFFERS. **\n"
        "select 1 as id from {{ source('raw', 'fil') }}",
    )
    hits = suggestions_for(audit(root), "SSC-EWI-DBTMIG0004")
    assert hits, "MIG0004 must fire on a NEEDS-USER marker"
    assert hits[0]["message"] == "Verify sort order matches original mapping"


# =============================================================================
# Positions
# =============================================================================


def test_line_col_maps_offsets_to_one_based_positions() -> None:
    from dbt_quality.core.sqlutil import line_col

    text = "select a\nfrom foo\nwhere x = 1\n"
    assert line_col(text, 0) == (1, 1)
    assert line_col(text, text.index("a")) == (1, 8)
    assert line_col(text, text.index("from")) == (2, 1)
    assert line_col(text, text.index("x = 1")) == (3, 7)


def test_span_bounds_the_match_and_end_is_exclusive() -> None:
    from dbt_quality.core.sqlutil import span

    text = "select a\nfrom foo\nwhere x = 1\n"
    start = text.index("from")
    assert span(text, start, start + 4) == {
        "line": 2,
        "column": 1,
        "end_line": 2,
        "end_column": 5,
    }


def test_span_clamps_a_multi_line_match_to_the_start_line() -> None:
    """
    The documented simplification: a range never spans lines, because a squiggle
    over a 60-line CTE body is worse than one over its first line.
    """
    from dbt_quality.core.sqlutil import span

    text = "select a\nfrom foo\nwhere x = 1\n"
    got = span(text, text.index("a"), text.index("where"))
    assert got["end_line"] == got["line"] == 1
    assert got["end_column"] == 9, "clamped to end of line 1, not into line 2"


def test_span_widens_a_zero_width_match() -> None:
    """A zero-width range would render as an invisible squiggle."""
    from dbt_quality.core.sqlutil import span

    text = "select a\nfrom foo\n"
    at = text.index("foo")
    got = span(text, at, at)
    assert got["end_column"] > got["column"]


def test_make_suggestion_forwards_every_position_field() -> None:
    """
    Regression guard for the original defect: ``column`` was a declared parameter
    that was never passed to ``Suggestion``, so every diagnostic reported column 1
    and ``to_dict``'s column branch was unreachable.
    """
    from dbt_quality.core.base import REGISTRY, make_suggestion

    rule_id = next(iter(REGISTRY))
    got = make_suggestion(
        rule_id, "msg", line=4, column=7, end_line=4, end_column=12
    ).to_dict()
    assert (got["line"], got["column"]) == (4, 7)
    assert (got["end_line"], got["end_column"]) == (4, 12)


def test_sql_column_name_reaches_context_not_the_position_field(
    tmp_path: Path,
) -> None:
    """
    ``column`` is a character offset; the SQL column name is ``column_name``. The
    two were once both spelled "column", so the rule's string bound to the
    position parameter and was dropped -- leaving ``context["column"]`` unset for
    the anchor resolver that reads it.
    """
    root = write_project(tmp_path / "colname")
    add_model(root, "gold/dim_c.sql", "select 1 as id, 2 as customer_id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: dim_c
                description: C.
                columns:
                  - name: customer_id
                    description: Natural key.
                    data_tests:
                      - unique
                      - not_null
            """).strip(),
        encoding="utf-8",
    )
    hits = suggestions_for(audit(root), "SSC-EWI-DBTTST0005")
    assert hits, "TST0005 must fire on unique + not_null"
    context = hits[0].get("context", {})
    assert context.get("column_name") == "customer_id"
    assert "column" not in context, "position field must not leak into context"


def test_positions_are_internally_consistent_across_the_estate(
    tmp_path: Path,
) -> None:
    """
    Estate-wide invariant. Catches a rule that spans the wrong string: an offset
    taken from one file and reported against another yields a column past the end
    of the target line.

    An anchor-resolved position carries a column but no end: the anchor knows where
    a construct starts, not where the finding stops, so those render as a caret
    rather than a range. Only a real span is required to be non-empty.
    """
    report = audit(copy_fixture(tmp_path, "ewi_estate"))
    root = Path(tmp_path) / "ewi_estate"
    for finding in report["suggestions"]:
        rule_id = finding["rule_id"]
        column = finding.get("column")
        if column is None:
            continue
        assert column >= 1, f"{rule_id}: column {column} is not 1-based"
        end_column = finding.get("end_column")
        if end_column is not None:
            assert end_column > column, f"{rule_id}: empty range {column}..{end_column}"
            assert (
                finding.get("end_line", finding["line"]) == finding["line"]
            ), f"{rule_id}: end_line must equal line under the clamp"

        # The column must exist on that line of the file the finding points at.
        path = root / finding["file"]
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        index = finding["line"] - 1
        if index >= len(lines):
            continue
        width = len(lines[index]) + 1
        assert column <= width, (
            f"{rule_id}: column {column} is past the end of "
            f"{finding['file']}:{finding['line']} (width {width}) -- "
            "the offset probably came from a different string"
        )


# =============================================================================
# Anchor-resolved positions
# =============================================================================


class _FakeSuggestion:
    """Minimal stand-in: resolve_position reads only these five attributes."""

    def __init__(
        self, *, line=None, column=None, file="", category="SQL", context=None
    ):
        self.line = line
        self.column = column
        self.file = file
        self.category = category
        self.context = context or {}


def test_resolve_position_never_fabricates_a_column_for_a_supplied_line() -> None:
    """
    The trap this phase exists to avoid.

    A rule that supplies a line but no offset (MAC0007, MAC0010) must keep column
    None. Filling it from the anchor would pair the rule's line with the anchor's
    column -- a character on a different line, which looks precise and is wrong.
    """
    from dbt_quality.core.anchors import resolve_position

    line, column = resolve_position(_FakeSuggestion(line=42), None)
    assert (line, column) == (42, None)


def test_resolve_position_returns_a_supplied_position_untouched() -> None:
    from dbt_quality.core.anchors import resolve_position

    got = resolve_position(_FakeSuggestion(line=7, column=13), None)
    assert got == (7, 13)


def test_resolve_position_falls_back_to_line_one_with_no_column() -> None:
    """Unresolvable means no column, not column 1 dressed up as a real position."""
    from dbt_quality.core.anchors import resolve_position

    assert resolve_position(_FakeSuggestion(), None) == (1, None)
    assert resolve_position(_FakeSuggestion(file=""), None) == (1, None)


def test_config_position_reports_the_indented_column(tmp_path: Path) -> None:
    """
    An indented config block must not report column 1 -- that would mean the column
    half is being discarded again, which is the original defect.
    """
    from dbt_quality.core.anchors import config_position

    root = write_project(tmp_path / "cfgpos")
    add_model(
        root,
        "gold/dim_x.sql",
        "-- header\n    {{ config(materialized='table') }}\nselect 1 as id",
    )
    project = build_portfolio(root).projects[0]
    model = next(m for m in project.models if m.name == "dim_x")
    assert config_position(model) == (2, 5)


def test_yaml_column_position_is_scoped_to_its_own_model(tmp_path: Path) -> None:
    """
    The same column name under two models must resolve to the right one. An
    unscoped search lands on whichever model comes first in the file.
    """
    from dbt_quality.core.anchors import yaml_column_position

    root = write_project(tmp_path / "yamlscope")
    add_model(root, "gold/dim_a.sql", "select 1 as shared_id")
    add_model(root, "gold/dim_b.sql", "select 1 as shared_id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: dim_a
                columns:
                  - name: shared_id
              - name: dim_b
                columns:
                  - name: shared_id
            """).strip(),
        encoding="utf-8",
    )
    project = build_portfolio(root).projects[0]
    first = yaml_column_position(project, "dim_a", "shared_id")
    second = yaml_column_position(project, "dim_b", "shared_id")
    assert first is not None and second is not None
    assert (
        second[0] > first[0]
    ), f"dim_b's shared_id must resolve below dim_a's, got {first} and {second}"
    assert first[1] > 1, "the column entry is indented, so its column is not 1"


def test_anchor_resolved_suggestions_gain_a_column(tmp_path: Path) -> None:
    """
    End-to-end: a TST rule supplies no offset, so its position comes from the
    anchor. Before this phase it reported column 1.

    TST0010 (no schema YAML entry) is used because it targets the model file and
    reliably fires on any undocumented model, so the position must come from that
    model's config block.

    The config block is deliberately not on the first line: ``add_model`` strips
    the leading whitespace of the whole string, so a first-line indent would be
    lost and the test would assert column 1 either way.
    """
    root = write_project(tmp_path / "anchorcol")
    add_model(
        root,
        "gold/dim_y.sql",
        "-- header\n    {{ config(materialized='table') }}\nselect 1 as id",
    )
    hits = [
        h
        for h in suggestions_for(audit(root), "SSC-EWI-DBTTST0010")
        if h["file"].endswith("dim_y.sql")
    ]
    assert hits, "TST0010 must fire on a model with no schema entry"
    assert (hits[0].get("line"), hits[0].get("column")) == (2, 5), (
        "expected the indented config block at 2:5, got "
        f"{hits[0].get('line')}:{hits[0].get('column')}"
    )
    assert (
        hits[0].get("end_column") is None
    ), "an anchor knows where a construct starts, not where the finding ends"


def _two_model_schema(root: Path) -> None:
    """A schema file declaring two models, so the name cannot be inferred."""
    add_model(root, "gold/dim_p.sql", "select 1 as id")
    add_model(root, "gold/dim_q.sql", "select 1 as id")
    (root / "models" / "gold" / "_models.yml").write_text(
        textwrap.dedent("""
            version: 2
            models:
              - name: dim_p
                columns:
                  - name: id
              - name: dim_q
                columns:
                  - name: id
            """).strip(),
        encoding="utf-8",
    )


def test_schema_yaml_rules_resolve_in_a_multi_model_file(tmp_path: Path) -> None:
    """
    A schema file declaring several models cannot be disambiguated by filename, so
    the rule must pass ``model=`` in context. Without it ``_model_name_for``
    returns "" and the position falls back to 1 with no column -- which is how ~27
    DOC and TST diagnostics silently stayed at column 1.
    """
    root = write_project(tmp_path / "multimodel")
    _two_model_schema(root)
    hits = suggestions_for(audit(root), "SSC-EWI-DBTDOC0001")
    assert hits, "DOC0001 must fire on models with no description"
    for hit in hits:
        assert hit["file"].endswith(".yml"), "must target the schema YAML"
        assert hit.get("column"), (
            f"{hit['file']}:{hit.get('line')} resolved no column -- "
            "model= is missing from context"
        )
    lines = {h.get("line") for h in hits}
    assert len(lines) == len(
        hits
    ), f"each model must resolve to its own line, got {lines}"


def test_retargeted_tst_rules_point_at_the_schema_yaml(tmp_path: Path) -> None:
    """A model with a schema entry: the finding belongs where the fix is made."""
    root = write_project(tmp_path / "retarget")
    _two_model_schema(root)
    hits = suggestions_for(audit(root), "SSC-EWI-DBTTST0002")
    assert hits, "TST0002 must fire on models with no key test"
    assert all(
        h["file"].endswith(".yml") for h in hits
    ), f"expected schema YAML targets, got {[h['file'] for h in hits]}"


def test_retargeted_rules_fall_back_to_the_model_file(tmp_path: Path) -> None:
    """
    The other half of the retarget, which is what rots if left untested.

    Asserted on the fallback expression and on the no-empty-file invariant rather
    than on one rule's output: TST0002 happens not to fire without a schema entry,
    so a test keyed to it would pass vacuously while the fallback broke. Every
    retargeted call site uses
    ``project.schema_sources.get(model.name, model.relative_path)``, so the
    premise to protect is that the default arm yields a real path.
    """
    root = write_project(tmp_path / "fallback")
    add_model(root, "gold/dim_orphan.sql", "select 1 as id")
    project = build_portfolio(root).projects[0]
    model = next(m for m in project.models if m.name == "dim_orphan")

    assert (
        project.schema_sources.get("dim_orphan") is None
    ), "fixture must have no schema entry, or the fallback is not exercised"
    resolved = project.schema_sources.get(model.name, model.relative_path)
    assert resolved == model.relative_path
    assert resolved.endswith("dim_orphan.sql")

    for finding in audit(root)["suggestions"]:
        assert finding["file"], f"{finding['rule_id']} reported an empty file path"


def test_yaml_keys_anchors_a_nested_dbt_project_key(tmp_path: Path) -> None:
    """
    Rules that know their key pass ``yaml_keys``; the resolver walks the path. The
    default is ``("models",)``, which anchored an `on-run-end` finding at
    `models:` -- honest about the file, wrong about the place.
    """
    from dbt_quality.core.anchors import resolve_position

    root = write_project(tmp_path / "yamlkeys")
    project_yml = root / "dbt_project.yml"
    project_yml.write_text(
        project_yml.read_text(encoding="utf-8") + textwrap.dedent("""
            on-run-end:
              - "{{ dbt_artifacts.upload_results(results) }}"
            """),
        encoding="utf-8",
    )
    project = build_portfolio(root).projects[0]

    default = resolve_position(
        _FakeSuggestion(file="dbt_project.yml", category="OPS"), project
    )
    routed = resolve_position(
        _FakeSuggestion(
            file="dbt_project.yml",
            category="OPS",
            context={"yaml_keys": ("on-run-end",)},
        ),
        project,
    )
    assert (
        routed[0] != default[0]
    ), f"yaml_keys must move the anchor off the default, both gave {routed}"
    text = project_yml.read_text(encoding="utf-8").splitlines()
    assert (
        text[routed[0] - 1].lstrip().startswith("on-run-end")
    ), f"line {routed[0]} is {text[routed[0] - 1]!r}, not the on-run-end key"


# =============================================================================
# Waivers: selectively silencing a rule by line, by file, or by config path
# =============================================================================
#
# All of these build their own project under tmp_path. They deliberately do not
# annotate tests/fixtures/ewi_estate/: EXPECTED_EWI_RULE_IDS asserts every active
# EWI rule fires there, so a waiver in that tree would fail the inventory test
# while looking like a rule regression.
#
# The reported line is read from a baseline run rather than hard-coded, because
# the anchor for a rule is resolved by category (see core/anchors.py) and a
# literal line number here would encode that resolution rather than test it.

#: Fires on the line carrying the literal reference, with a precise column.
HARDCODED_REF = "SSC-EWI-DBTSQL0006"
#: Two rules that both fire on one under-configured incremental model.
INC_NO_GUARD = "SSC-PRF-DBTINC0006"
INC_NO_KEY = "SSC-FDM-DBTINC0007"


def _fired(root: Path, rule_id: str) -> list:
    return [
        s for s in run_audit(build_portfolio(root)).suggestions if s.rule_id == rule_id
    ]


def _reported_line(root: Path, rule_id: str) -> int:
    hits = _fired(root, rule_id)
    assert hits, f"{rule_id} did not fire on the baseline fixture"
    return hits[0].line


def _edit_lines(path: Path, mutate) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(mutate(lines)) + "\n", encoding="utf-8")


def _hardcoded_ref_project(tmp_path: Path, name: str) -> tuple[Path, Path]:
    """A project whose single model carries a literal db.schema.table reference."""
    root = write_project(tmp_path / name)
    add_model(root, "gold/fct_x.sql", "select id from analytics.public.orders")
    return root, root / "models" / "gold" / "fct_x.sql"


def _incremental_project(tmp_path: Path, name: str) -> tuple[Path, Path]:
    """A project whose model fires both INC_NO_GUARD and INC_NO_KEY."""
    root = write_project(tmp_path / name)
    add_model(
        root,
        "gold/fct_events.sql",
        """
        {{ config(materialized='incremental') }}
        select event_id from {{ ref('stg_events') }}
        """,
    )
    add_model(root, "bronze/stg_events.sql", "select 1 as event_id")
    return root, root / "models" / "gold" / "fct_events.sql"


def test_inline_waiver_on_the_reported_line(tmp_path: Path) -> None:
    """A directive appended to the line the diagnostic reports silences it."""
    root, model = _hardcoded_ref_project(tmp_path, "inline_same")
    line = _reported_line(root, HARDCODED_REF)

    _edit_lines(
        model,
        lambda ls: [
            f"{text}  -- dbt-quality: ignore {HARDCODED_REF}" if i == line - 1 else text
            for i, text in enumerate(ls)
        ],
    )
    assert not _fired(root, HARDCODED_REF), "trailing directive must waive its own line"


def test_inline_waiver_above_the_reported_line(tmp_path: Path) -> None:
    """
    A directive on its own line waives the next line that carries anything.

    The blank-line variant is the shape people actually write, and requiring
    adjacency would make the mechanism look unreliable.
    """
    for name, spacer in (("inline_above", []), ("inline_gap", [""])):
        root, model = _hardcoded_ref_project(tmp_path, name)
        line = _reported_line(root, HARDCODED_REF)

        _edit_lines(
            model,
            lambda ls, line=line, spacer=spacer: [
                *ls[: line - 1],
                f"-- dbt-quality: ignore {HARDCODED_REF}",
                *spacer,
                *ls[line - 1 :],
            ],
        )
        assert not _fired(
            root, HARDCODED_REF
        ), f"directive above the reported line must waive it ({name})"


def test_trailing_waiver_does_not_reach_the_next_line() -> None:
    """
    A trailing directive applies to its own line only.

    Extending it forward would silence a finding on the following statement that
    the author never looked at -- an unintended false negative, which is the most
    expensive thing this mechanism can produce.
    """
    waivers = parse_waivers(
        "select 1 as a  -- dbt-quality: ignore SSC-EWI-DBTSQL0006\nselect 2 as b\n"
    )
    assert waivers.waives("SSC-EWI-DBTSQL0006", 1)
    assert not waivers.waives(
        "SSC-EWI-DBTSQL0006", 2
    ), "a trailing directive must not carry to the following line"


def test_ignore_file_waives_the_whole_file(tmp_path: Path) -> None:
    """`ignore-file` is the answer when the reported line is inconvenient."""
    root, model = _incremental_project(tmp_path, "ignorefile")
    assert _fired(root, INC_NO_GUARD), "baseline must fire before waiving"

    model.write_text(
        f"-- dbt-quality: ignore-file {INC_NO_GUARD}\n"
        + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert not _fired(root, INC_NO_GUARD), "ignore-file must waive regardless of line"


def test_waiver_is_rule_specific(tmp_path: Path) -> None:
    """
    Waiving one rule must leave every other rule firing on the same file.

    The false-negative gate for this feature. A waiver that over-reaches silences
    findings the author never reviewed, which is worse than having no waivers.
    """
    root, model = _incremental_project(tmp_path, "specific")
    assert _fired(root, INC_NO_GUARD) and _fired(root, INC_NO_KEY)

    model.write_text(
        f"-- dbt-quality: ignore-file {INC_NO_GUARD}\n"
        + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert not _fired(root, INC_NO_GUARD), "the named rule must be waived"
    assert _fired(root, INC_NO_KEY), "an unnamed rule on the same file must still fire"


def test_wildcard_waives_every_rule(tmp_path: Path) -> None:
    """`*` in place of a rule list waives everything for that file."""
    root, model = _incremental_project(tmp_path, "wildcard")
    model.write_text(
        "-- dbt-quality: ignore-file *\n" + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    remaining = [
        s
        for s in run_audit(build_portfolio(root)).suggestions
        if s.file.endswith("fct_events.sql")
    ]
    assert not remaining, f"wildcard must waive every rule, got {remaining}"


def test_lowercase_directive_still_matches(tmp_path: Path) -> None:
    """A rule id written in lower case waives, so the directive is forgiving."""
    root, model = _incremental_project(tmp_path, "lowercase")
    model.write_text(
        f"-- dbt-quality: ignore-file {INC_NO_GUARD.lower()}\n"
        + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert not _fired(root, INC_NO_GUARD)


def test_config_ignore_scopes_by_path_glob(tmp_path: Path) -> None:
    """An `ignore:` entry waives only at the paths it names."""
    root = write_project(tmp_path / "cfgpath")
    add_model(root, "gold/fct_x.sql", "select id from analytics.public.orders")
    add_model(root, "bronze/stg_y.sql", "select id from analytics.public.customers")
    assert len(_fired(root, HARDCODED_REF)) == 2, "both models must fire at baseline"

    (root / ".dbt-quality.yml").write_text(
        textwrap.dedent(f"""
            ignore:
              - paths: ["models/gold/**"]
                rules: [{HARDCODED_REF}]
            """).strip(),
        encoding="utf-8",
    )
    hits = _fired(root, HARDCODED_REF)
    assert len(hits) == 1, f"only the unmatched path may still fire, got {hits}"
    assert hits[0].file.endswith("stg_y.sql")


def test_config_ignore_accepts_a_rule_wildcard(tmp_path: Path) -> None:
    """`rules: ["*"]` waives every rule at the named paths."""
    root, _model = _incremental_project(tmp_path, "cfgwild")
    (root / ".dbt-quality.yml").write_text(
        textwrap.dedent("""
            ignore:
              - paths: ["models/gold/**"]
                rules: ["*"]
            """).strip(),
        encoding="utf-8",
    )
    remaining = [
        s
        for s in run_audit(build_portfolio(root)).suggestions
        if s.file.endswith("fct_events.sql")
    ]
    assert not remaining, f"rule wildcard must waive everything, got {remaining}"


def test_config_is_found_in_a_parent_directory(tmp_path: Path) -> None:
    """
    A repo-root config governs an audit rooted at a nested project.

    This is what keeps the save-time hook and the audit in agreement:
    `dbt-validate` builds its portfolio from the enclosing dbt project, so a
    config read only at the audit root would be honoured by one surface and
    ignored by the other.
    """
    repo = tmp_path / "repo"
    root = write_project(repo / "project")
    add_model(root, "gold/fct_x.sql", "select id from analytics.public.orders")
    assert _fired(root, HARDCODED_REF), "baseline must fire before waiving"

    (repo / ".dbt-quality.yml").write_text(
        textwrap.dedent(f"""
            ignore:
              - paths: ["**/fct_x.sql"]
                rules: [{HARDCODED_REF}]
            """).strip(),
        encoding="utf-8",
    )
    assert not _fired(
        root, HARDCODED_REF
    ), "a config above the audit root must still be honoured"


def test_waivers_apply_in_single_file_mode(tmp_path: Path) -> None:
    """
    The hook path honours a waiver identically to the audit.

    A waiver the report respects and the editor ignores would read as the feature
    being broken, so the two surfaces are asserted against the same fixture.
    """
    root, model = _incremental_project(tmp_path, "hookparity")
    baseline = {
        s.rule_id for s in run_single_file(build_portfolio(root), model).suggestions
    }
    assert {INC_NO_GUARD, INC_NO_KEY} <= baseline

    model.write_text(
        f"-- dbt-quality: ignore-file {INC_NO_GUARD}\n"
        + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    after = {
        s.rule_id for s in run_single_file(build_portfolio(root), model).suggestions
    }
    assert INC_NO_GUARD not in after, "single-file mode must honour the waiver"
    assert INC_NO_KEY in after, "single-file mode must not over-waive"


def test_malformed_waivers_are_inert(tmp_path: Path) -> None:
    """
    A truncated directive or a malformed config entry waives nothing and raises
    nothing.

    A half-written directive must not widen to "every rule": silently hiding
    findings the author never named is the failure mode worth guarding against.
    """
    root, model = _incremental_project(tmp_path, "malformed")
    model.write_text(
        "-- dbt-quality: ignore\n" + model.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / ".dbt-quality.yml").write_text(
        textwrap.dedent("""
            ignore:
              - paths: ["models/gold/**"]
              - rules: [SSC-EWI-DBTSQL0006]
              - "not a mapping"
            """).strip(),
        encoding="utf-8",
    )
    assert _fired(root, INC_NO_GUARD), "a rule-less directive must waive nothing"
    assert _fired(root, INC_NO_KEY), "an incomplete config entry must waive nothing"


def test_a_waiver_is_not_read_as_a_conversion_marker(tmp_path: Path) -> None:
    """
    Writing a waiver must not create a new finding.

    A dbt-quality rule id is spelled exactly like a SnowConvert marker
    (`SSC-EWI-DBTSQL0006` against `SSC-EWI-SSIS0033`), so MIG002 read the waiver
    itself as unresolved conversion debt and reported an error naming it. The
    reader silencing one finding would have gained another.
    """
    root = write_project(tmp_path / "markerclash")
    add_model(
        root,
        "gold/fct_x.sql",
        f"select id from analytics.public.orders  -- dbt-quality: ignore {HARDCODED_REF}",
    )
    # Force migration provenance so the MIG pack is active at all.
    (root / ".dbt-quality.yml").write_text(
        "migration:\n  mode: lift_and_shift\n", encoding="utf-8"
    )

    ids = {s.rule_id for s in run_audit(build_portfolio(root)).suggestions}
    assert HARDCODED_REF not in ids, "the waiver must still take effect"
    assert (
        "SSC-EWI-DBTMIG0002" not in ids
    ), "a waiver directive must not be reported as an unresolved conversion marker"


def test_waivers_do_not_shift_migration_provenance(tmp_path: Path) -> None:
    """
    Waivers must not accumulate into a lift-and-shift verdict.

    Marker count is a provenance signal heavy enough to classify a project as
    converted on its own, which suppresses the entire ARCHITECTURE tier. A
    hand-written project acquiring waivers would have silently lost those checks.
    """
    from dbt_quality.provenance import classify

    root = write_project(tmp_path / "provenance_clash")
    for index in range(3):
        add_model(
            root,
            f"gold/fct_{index}.sql",
            f"-- dbt-quality: ignore-file {HARDCODED_REF}\n"
            "select id from analytics.public.orders",
        )
    portfolio = build_portfolio(root)
    verdict = classify(portfolio.projects[0])
    assert (
        not verdict.is_migration
    ), f"waivers must not read as conversion evidence: {verdict.signals}"


# =============================================================================
# PRJ0004 -- profiles.yml is a git-aware placement rule (defects 1, 2, obs 4)
# =============================================================================

PROFILES_PRESENT = "SSC-EWI-DBTPRJ0004"


def _add_profiles(root: Path, body: str = "  target: dev\n  outputs:\n") -> None:
    (root / "profiles.yml").write_text(body, encoding="utf-8")


def _init_repo(root: Path):
    """Init a git repo at ``root`` with a usable identity, or None if git absent."""
    if shutil.which("git") is None:
        return None
    try:
        import git
    except Exception:  # noqa: BLE001
        return None
    repo = git.Repo.init(root)
    with repo.config_writer() as cw:
        cw.set_value("user", "email", "test@example.com")
        cw.set_value("user", "name", "Test")
        cw.set_value("commit", "gpgsign", "false")
    return repo


def test_prj0004_presence_only_when_not_a_repo(tmp_path: Path) -> None:
    """
    Outside a git repo, PRJ0004 states presence and never claims 'committed'.

    Defect 1: the old rule titled the finding 'committed' and told the reader to
    rotate a credential 'git history retains', from a bare ``path.is_file()`` --
    false in a working tree that was never a repo.
    """
    root = write_project(tmp_path / "norepo")
    _add_profiles(root)

    hits = _fired(root, PROFILES_PRESENT)
    assert len(hits) == 1, "profiles.yml present must fire PRJ0004"
    s = hits[0]
    assert s.level == "warning", "unknown git status is a warning, not an error"
    assert "present in the project directory" in s.message
    assert "committed" not in s.message.lower()
    assert "git rm" not in s.remediation, "must not assert removal when not tracked"
    assert "git history retains" not in s.remediation


def test_prj0004_does_not_escalate_on_credential_content(tmp_path: Path) -> None:
    """
    Content is OPS0002's concern; PRJ0004 must not raise itself to error on it.

    Defect 2 / observation 4: the old rule ran its own secret regex and escalated
    WARNING -> ERROR, double-counting content that OPS0002 already owns.
    """
    root = write_project(tmp_path / "withsecret")
    _add_profiles(root, "  password: SuperSecret123!\n")

    hits = _fired(root, PROFILES_PRESENT)
    assert hits, "profiles.yml present must still fire PRJ0004"
    assert all(
        s.level != "error" for s in hits
    ), "PRJ0004 must not escalate to error on credential content"


def test_prj0004_reports_committed_only_when_tracked(tmp_path: Path) -> None:
    """When the file is genuinely tracked, the 'committed' framing is correct."""
    root = write_project(tmp_path / "tracked")
    _add_profiles(root)
    repo = _init_repo(root)
    if repo is None:
        return  # git unavailable: the fallback branch is covered elsewhere
    repo.index.add(["profiles.yml"])
    repo.index.commit("add profiles")

    hits = _fired(root, PROFILES_PRESENT)
    assert len(hits) == 1
    s = hits[0]
    assert s.level == "warning"
    assert "tracked in git" in s.message
    assert "git rm --cached" in s.remediation, "tracked file should advise removal"
    assert "rotate" in s.remediation.lower()


def test_prj0004_ignored_is_informational(tmp_path: Path) -> None:
    """An untracked, git-ignored profiles.yml is the low-risk, informational case."""
    root = write_project(tmp_path / "ignored")
    _add_profiles(root)
    (root / ".gitignore").write_text("profiles.yml\n", encoding="utf-8")
    repo = _init_repo(root)
    if repo is None:
        return

    hits = _fired(root, PROFILES_PRESENT)
    assert len(hits) == 1
    s = hits[0]
    assert s.level == "information", "git-ignored presence is informational"
    assert "git-ignored" in s.message
    assert "git rm" not in s.remediation


# =============================================================================
# OPS0002 -- SECRET_PATTERN distinguishes a literal from a templated value
# =============================================================================


def test_ops0002_secret_pattern_ignores_templated_values() -> None:
    """
    Defect 2 root: a quoted ``env_var`` is not a literal secret.

    The lookahead must tolerate an opening quote before the template, or the
    idiomatic ``password: "{{ env_var('X') }}"`` is flagged -- and, worse,
    survives its own recommended remediation.
    """
    from dbt_quality.rules.ops import SECRET_PATTERN

    dq = '"'
    sq = "'"
    fires = [
        "Snowflake",
        f"{dq}Snowflake{dq}",
    ]
    quiet = [
        f"{dq}{{{{ env_var('X') }}}}{dq}",
        "{{ env_var('X') }}",
        f"{sq}{{{{ env_var('X') }}}}{sq}",
        "$SNOWFLAKE_PW",
        f"{dq}$SNOWFLAKE_PW{dq}",
        "",
    ]
    for value in fires:
        assert SECRET_PATTERN.search(
            f"      password: {value}"
        ), f"literal must fire: {value!r}"
    for value in quiet:
        assert not SECRET_PATTERN.search(
            f"      password: {value}"
        ), f"templated/empty must stay quiet: {value!r}"


def test_ops0002_clears_once_credentials_are_templated(tmp_path: Path) -> None:
    """End to end: a profiles.yml using env_var raises no OPS0002 finding."""
    root = write_project(tmp_path / "templated")
    _add_profiles(root, "  password: \"{{ env_var('SNOWFLAKE_PW') }}\"\n")
    assert not _fired(
        root, "SSC-EWI-DBTOPS0002"
    ), "a templated credential must not be reported as a literal secret"


# =============================================================================
# blank_directives -- consecutive waivers must not merge (defect 3)
# =============================================================================


def test_blank_directives_handles_consecutive_directives() -> None:
    """
    Two directives on consecutive lines are blanked independently.

    Defect 3: the rule-list class contained ``\\s``, so a whole-file substitution
    let one match span the newline and swallow the next directive up to its colon
    -- the second rule id survived (read later as a marker) and the eaten newline
    shifted every later line number.
    """
    text = (
        "-- dbt-quality: ignore-file SSC-EWI-DBTINC0002\n"
        "-- dbt-quality: ignore-file SSC-FDM-DBTINC0007\n"
        "select 1\n"
    )
    blanked = blank_directives(text)
    assert "SSC-EWI-DBTINC0002" not in blanked, "first id must be blanked"
    assert "SSC-FDM-DBTINC0007" not in blanked, "second id must be blanked too"
    assert blanked.count("\n") == text.count("\n"), "newlines must be preserved"
    assert len(blanked) == len(text), "length must be preserved for offset parity"


def test_consecutive_waivers_produce_no_marker_finding(tmp_path: Path) -> None:
    """
    Two consecutive waivers must not manufacture a conversion-marker finding.

    The end-to-end form of defect 3: the surviving second id was read by the MIG
    pack as an unresolved marker, so silencing two rules raised a brand-new one.
    """
    root = write_project(tmp_path / "twowaivers")
    add_model(
        root,
        "gold/fct_x.sql",
        "-- dbt-quality: ignore-file SSC-PRF-DBTINC0006\n"
        "-- dbt-quality: ignore-file SSC-FDM-DBTINC0007\n"
        "{{ config(materialized='incremental') }}\n"
        "select id from {{ ref('stg_x') }}",
    )
    add_model(root, "bronze/stg_x.sql", "select 1 as id")
    (root / ".dbt-quality.yml").write_text(
        "migration:\n  mode: lift_and_shift\n", encoding="utf-8"
    )

    ids = {s.rule_id for s in run_audit(build_portfolio(root)).suggestions}
    assert "SSC-PRF-DBTINC0006" not in ids, "first waiver must take effect"
    assert "SSC-FDM-DBTINC0007" not in ids, "second waiver must take effect"
    assert not any(
        i.startswith("SSC-EWI-DBTMIG") or i.startswith("SSC-FDM-DBTMIG") for i in ids
    ), "a waiver id must not be read as a conversion marker"


def _main() -> int:
    import tempfile
    import traceback

    tests = [
        (name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")
    ]
    failures = 0
    for name, fn in tests:
        try:
            if "tmp_path" in fn.__code__.co_varnames[: fn.__code__.co_argcount]:
                with tempfile.TemporaryDirectory() as tmp:
                    fn(Path(tmp))
            else:
                fn()
            print(f"PASS {name}")
        except Exception:  # noqa: BLE001 -- test runner boundary
            failures += 1
            print(f"FAIL {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_main())
