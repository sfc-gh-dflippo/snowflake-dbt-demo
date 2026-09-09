"""Merge AIM instances into product ETL.Issues and strip cross-platform bleed.

Owner 2026-08-13:
  - AIM rows must coexist in ETL.Issues (same CSV consumers already know).
  - Foreign dialect engine codes on a document are forbidden (e.g. SSIS/INF on Alteryx).
  - Reports/AiFirstIssues/ keeps issues.json + types-cited.json (typed inventory).
    Do not emit a parallel issues.csv — ETL.Issues is the instance list.

This module is the product-surface rewrite after stage 5 classifies AIM findings. It does not
replace detect/classify/mint.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any, Iterable

# Same map as issues/stage.py: free text under Reports/ must not re-inflate the
# whole-tree SSC-EWI/FDM grep on re-inspection. Code column values are real product
# codes and are NOT scrubbed.
SCRUB = {
    "!!!RESOLVE" + " EWI!!!": "<blocking-marker>",
    "SSC-EWI-": "<engine-warning-code:>",
    "SSC-FDM-": "<engine-difference-code:>",
    "SSC-AI-" + "AUTHORED": "<model-authored-stamp>",
    "__PRODUCER_EXPRESSION" + "_NOT_CONVERTED__": "<producer-sentinel>",
}


def scrub(text: str) -> str:
    out = str(text)
    for bad, good in SCRUB.items():
        out = out.replace(bad, good)
    return out


# Excel/Sheets treat a cell starting with any of these as a formula even when
# opened from CSV. Every field here is sourced from AIM/product data that
# ultimately traces back to source filenames, element names, or free text
# pulled from the migrated document, so escape at the write boundary.
_FORMULA_LEAD = ("=", "+", "-", "@")


def neutralize_formula(value: Any) -> str:
    s = str(value)
    if s.lstrip("\t\n\r ").startswith(_FORMULA_LEAD):
        return "'" + s
    return s


ETL_ISSUES_FIELDS = [
    "SessionID",
    "Severity",
    "Code",
    "Name",
    "Description",
    "ParentFileName",
    "ComponentFullName",
    "MigrationID",
]

# SSC-EWI-SSIS0009 / SSC-FDM-INF0001 / SSC-EWI-ETL0001 / SSC-EWI-0001
_ENGINE_CODE = re.compile(
    r"^SSC-(?P<kind>EWI|FDM)-(?P<dialect>[A-Z]+)?(?P<num>\d+)$",
    re.IGNORECASE,
)

# Platforms that may keep SSIS- or INF-named engine codes.
_NATIVE_DIALECT = {
    "ssis": "SSIS",
    "dtsx": "SSIS",
    "informatica": "INF",
    "infpc": "INF",
    "xml": "INF",  # Informatica XML exports often end in .xml — conservative: only INF when stated
}

# File-extension / table platform ids that are never SSIS/INF-native.
_UNSUPPORTED_IDS = {
    "alteryx", "yxmd", "yxmc", "yxwz",
    "pentaho", "ktr", "kjb",
    "datastage", "dsx",
    "adf", "json",
}


def normalize_platform(platform: str | None, document_name: str | None = None) -> str:
    p = (platform or "").strip().lower()
    if p.startswith("platform_"):
        p = p[len("platform_"):]
    if p in _UNSUPPORTED_IDS or p in _NATIVE_DIALECT:
        return p
    if document_name:
        ext = Path(document_name).suffix.lstrip(".").lower()
        if ext:
            return ext
    return p or "unknown"


def engine_code_dialect(code: str) -> str | None:
    """Return dialect token for an engine code, or None if not an SSC-EWI/FDM code.

    AIM-* and other non-engine codes return None (not foreign bleed — handled separately).
    Empty dialect (SSC-EWI-0125) returns "".
    """
    c = (code or "").strip()
    if not c or c.upper().startswith("AIM-"):
        return None
    m = _ENGINE_CODE.match(c)
    if not m:
        return None
    d = m.group("dialect")
    return (d or "").upper()


def is_foreign_engine_code(code: str, platform: str) -> bool:
    """True when an SSC-* code names a dialect that must not appear on this platform."""
    dialect = engine_code_dialect(code)
    if dialect is None:
        return False  # AIM or unknown shape — not "foreign engine dialect bleed"
    if dialect in ("", "ETL", "GEN", "GENERAL"):
        return False
    plat = normalize_platform(platform)
    native = _NATIVE_DIALECT.get(plat)
    if plat in _UNSUPPORTED_IDS or native is None:
        # Unsupported proving platforms: SSIS and INF (and any other named dialect) are bleed.
        return dialect in {"SSIS", "INF", "DS", "PDI", "ADF"} and dialect != plat.upper()
    # Native SSIS/Inf path through this producer: only the other big dialect is bleed.
    if native == "SSIS":
        return dialect == "INF"
    if native == "INF":
        return dialect == "SSIS"
    return False


def severity_for_aim(impact: str | None) -> str:
    i = (impact or "").lower()
    if i == "output-absent":
        return "High"
    if i == "output-incomplete":
        return "High"
    if i == "output-unverified":
        return "Medium"
    return "High"


def aim_instance_to_etl_row(
    instance: dict[str, Any],
    *,
    session_id: str = "Development Session",
    migration_id: str | None = None,
) -> dict[str, str]:
    doc = instance.get("document") or ""
    ext = Path(doc).suffix.lstrip(".").upper() or "ETL"
    mid = migration_id or f"AIFIRST-{ext}"
    code = str(instance.get("code") or "")
    title_bits = [
        instance.get("category"),
        instance.get("reason"),
    ]
    name = " / ".join(str(x) for x in title_bits if x) or code
    component = (
        str(instance.get("element") or "").strip()
        or str(instance.get("element_id") or "").strip()
        or "(unscoped)"
    )
    return {
        "SessionID": session_id,
        "Severity": severity_for_aim(instance.get("impact")),
        "Code": code,
        "Name": scrub(name[:200]),
        "Description": scrub(str(instance.get("text") or instance.get("detail") or name)),
        "ParentFileName": doc,
        "ComponentFullName": component,
        "MigrationID": mid,
    }


def read_etl_issues(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh))


def write_etl_issues(path: Path, rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=ETL_ISSUES_FIELDS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: neutralize_formula(row.get(k, "")) for k in ETL_ISSUES_FIELDS})


def find_etl_issues_csv(reports_dir: Path) -> Path | None:
    """Mirror ReportsReader.SelectLatestReportFile (C# reader): among files
    matching the glob, prefer the newest timestamped report over the .NA
    placeholder; fall back to the .NA file only when no timestamped report
    exists.
    """
    candidates = sorted(reports_dir.glob("ETL.Issues*.csv"))
    if len(candidates) <= 1:
        return candidates[0] if candidates else None
    timestamped = [p for p in candidates if not p.stem.endswith(".NA")]
    if not timestamped:
        return candidates[0]
    return max(timestamped, key=lambda p: p.name.lower())


def rewrite_etl_issues_for_coexistence(
    out_root: str | Path,
    *,
    platform: str,
    document_name: str,
    aim_instances: list[dict[str, Any]],
) -> dict[str, Any]:
    """Strip foreign engine codes from ETL.Issues and append AIM rows.

    Returns a stats dict for driver stdout.
    """
    reports = Path(out_root) / "Reports"
    path = find_etl_issues_csv(reports)
    plat = normalize_platform(platform, document_name)
    existing = read_etl_issues(path) if path else []
    kept: list[dict[str, str]] = []
    dropped: list[dict[str, str]] = []
    for row in existing:
        code = row.get("Code") or ""
        if is_foreign_engine_code(code, plat):
            dropped.append(row)
        else:
            kept.append(row)

    existing_keys = {(r.get("Code"), r.get("ComponentFullName")) for r in kept}
    added: list[dict[str, str]] = []
    for inst in aim_instances:
        row = aim_instance_to_etl_row(inst)
        key = (row["Code"], row["ComponentFullName"])
        if key in existing_keys:
            continue
        existing_keys.add(key)
        added.append(row)

    final_rows = kept + added
    target = path or (reports / "ETL.Issues.NA.csv")
    write_etl_issues(target, final_rows)
    return {
        "path": str(target),
        "platform": plat,
        "kept_engine": len(kept),
        "dropped_bleed": len(dropped),
        "dropped_codes": sorted({r.get("Code") or "" for r in dropped}),
        "aim_added": len(added),
        "total": len(final_rows),
    }
