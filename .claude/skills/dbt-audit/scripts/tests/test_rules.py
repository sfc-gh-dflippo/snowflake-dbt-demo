"""
Verification harness for the dbt-audit rule packs.

Two kinds of check:

1. **Fixture tests** -- synthetic projects written to a temp dir, asserting that a
   specific anti-pattern fires and that the sanctioned form of the same pattern
   does not. These are the false-positive gate; without them a regex tightened for
   one repo silently breaks on another.

2. **Ground-truth tests** -- run against this repository, asserting known-true
   findings (a model literally named ``*_full_reload`` must produce INC005) and
   known-false ones (a single 40-model project must not be reported as
   fragmented).

Run with:  pytest tests/ -q
Or standalone: python tests/test_rules.py
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS / "src"))

from dbt_audit.core.base import REGISTRY  # noqa: E402
from dbt_audit.core.sqlutil import (  # noqa: E402
    extract_config,
    extract_ctes,
    find_derived_subqueries,
    is_watermark_subquery,
)
from dbt_audit.discovery import build_portfolio  # noqa: E402
from dbt_audit.engine import run_audit  # noqa: E402
from dbt_audit.scoring import build_report  # noqa: E402

REPO_ROOT = SCRIPTS.parent.parent.parent.parent  # .../snowflake-dbt-demo


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


def audit(root: Path) -> dict:
    return build_report(run_audit(build_portfolio(root)), str(root))


def rule_ids(report: dict) -> set[str]:
    return {f["rule_id"] for f in report["findings"]}


def findings_for(report: dict, rule_id: str) -> list[dict]:
    return [f for f in report["findings"] if f["rule_id"] == rule_id]


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
    assert "INC001" in ids, "truncate-and-load in a pre_hook must fire INC001"


def test_correct_incremental_stays_silent(tmp_path: Path) -> None:
    """
    A textbook incremental model must produce no INC findings.

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
    inc = [f for f in audit(root)["findings"] if f["category"] == "INC"]
    assert not inc, f"correct incremental model produced INC findings: {inc}"


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
    assert "INC006" in ids, "missing is_incremental() must fire INC006"
    assert "INC007" in ids, "missing unique_key on merge must fire INC007"


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
    hits = findings_for(audit(root), "SQL001")
    assert hits, "FROM/JOIN subquery must fire SQL001"
    assert hits[0]["context"]["reuse_count"] == 1
    assert "CTE" in hits[0]["remediation"], "single-use subquery must recommend a CTE"


def test_subquery_recommends_ephemeral_when_reused(tmp_path: Path) -> None:
    """The reuse test: identical logic in two models must recommend a model, not a CTE."""
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
    hits = findings_for(audit(root), "SQL001")
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
    assert "MAC003" in ids, "macro with no call sites must fire MAC003"
    assert (
        "MAC002" in ids or "MAC004" in ids
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
    micro = findings_for(report, "PRJ001")
    assert len(micro) == 3, "each 1-model project must be reported as a micro-project"
    assert findings_for(
        report, "PRJ002"
    ), "projects sharing a source must be a consolidation candidate"


def test_single_small_project_is_not_fragmentation(tmp_path: Path) -> None:
    """A new or deliberately scoped repo is not fragmentation, and must not be flagged."""
    root = write_project(tmp_path / "solo")
    add_model(root, "gold/dim_a.sql", "select 1 as id")
    assert not findings_for(audit(root), "PRJ001")


def test_migration_suppresses_architecture_not_correctness(tmp_path: Path) -> None:
    """
    The core tier behaviour.

    A converted project must keep its correctness findings and its unresolved
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
    report = audit(root)
    ids = rule_ids(report)

    assert report["projects"][0]["provenance"][
        "is_migration"
    ], "conversion markers must be detected"
    assert "INC002" in ids, "delete-and-load must still fire on converted code"
    assert "MIG003" in ids, "SSC-FDM marker must be reported"
    assert "MIG005" in ids, "ETL control column must be reported"

    architecture = [f for f in report["findings"] if f["tier"] == "architecture"]
    assert architecture, "architecture rules should still evaluate"
    assert all(
        f.get("suppressed") for f in architecture
    ), "every architecture finding on converted code must be suppressed, not reported"
    assert report["suppressed"]["count"] > 0
    # Suppressed findings must not affect the grade.
    assert all(
        not f.get("suppressed") for f in report["findings"] if f["category"] == "INC"
    )


def test_native_project_keeps_architecture_findings(tmp_path: Path) -> None:
    """The mirror of the above: with no conversion markers, nothing is suppressed."""
    root = write_project(tmp_path / "native")
    add_model(root, "other/WeirdName.sql", "select 1 as id")
    report = audit(root)
    assert not report["projects"][0]["provenance"]["is_migration"]
    assert "ARC008" in rule_ids(
        report
    ), "mixed-case filename must be reported on native code"
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
    assert "INC003" in rule_ids(
        audit(root)
    ), "folder-level TRUNCATE hook must fire INC003"


# =============================================================================
# Ground truth against this repository
# =============================================================================


def test_repo_ground_truth() -> None:
    """
    Assert known-true and known-false findings against snowflake-dbt-demo.

    Skipped when run outside the repo so the fixture tests stay portable.
    """
    if not (REPO_ROOT / "dbt_project.yml").is_file():
        print(f"  (skipped: {REPO_ROOT} is not a dbt project)")
        return

    report = audit(REPO_ROOT)
    ids = rule_ids(report)

    def files_for(rule_id: str) -> set[str]:
        return {f["file"] for f in findings_for(report, rule_id)}

    # Known-true: a model literally named *_full_reload.
    assert "INC005" in ids
    assert any("full_reload" in f for f in files_for("INC005"))

    # Known-true: uppercase / double-underscore model names.
    assert any("DIM__CUSTOMERS" in f for f in files_for("ARC008"))

    # Known-true: models outside a recognised layer folder.
    assert any("other/" in f for f in files_for("ARC001"))

    # Known-true: dbt_artifacts hook wired while its models are disabled.
    assert "OPS001" in ids

    # Known-false: one project with many models is not fragmentation.
    assert not findings_for(report, "PRJ001")

    # Known-false: no conversion markers here, so nothing is suppressed.
    assert report["suppressed"]["count"] == 0
    assert not any(f["category"] == "MIG" for f in report["findings"])

    # The manifest is committed in this repo, so graph rules must have run.
    assert report["summary"]["rules_skipped"] == 0, report["skipped_checks"]

    # Sanity: the score must be a real number in range, not saturated at zero.
    score = report["summary"]["score"]
    assert 0 < score < 100, f"score {score} looks degenerate"


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
        "INC009" not in ids
    ), "stream-based CDC model must not be flagged for no watermark"
    assert "INC013" not in ids


def test_macro_generated_columns_not_flagged(tmp_path: Path) -> None:
    """
    Regression guard for INC011.

    When the column list is produced by a macro it does not exist in the file
    text, so every merge_exclude_columns entry looks absent. Suppress rather than
    emit findings that cannot be verified from the source.
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
    assert "INC011" not in rule_ids(
        audit(root)
    ), "columns generated by a macro cannot be verified from file text and must not be flagged"


def test_every_rule_has_metadata() -> None:
    """Guard against a rule registered without the text the report needs."""
    for meta in REGISTRY.values():
        assert meta.title, f"{meta.rule_id} has no title"
        assert meta.category, f"{meta.rule_id} has no category"
        assert meta.rationale, f"{meta.rule_id} has no rationale for the report"


# =============================================================================
# Standalone runner (no pytest required)
# =============================================================================


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
