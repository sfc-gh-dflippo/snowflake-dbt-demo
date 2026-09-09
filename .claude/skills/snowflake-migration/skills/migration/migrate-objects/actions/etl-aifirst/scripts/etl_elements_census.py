"""Append census-declared non-graph rows to ETL.Elements as Status=N/A.

The producer census is graph nodes (plus not-in-graph Unsupported). Native
ETL.Elements also carries metadata/control rows (Package, Path, ConnectionManager,
Workflow, Mapping, Session, folder SOURCE/TARGET). Those records are already
classified by Identification; this module writes them without inventing names
or reclassifying Success/Partial/NotSupported graph rows.

Conversion-rate exclusions (Path, Package, PrecedenceConstraint, ConnectionManager)
are preserved: new rows use those subtypes or Status=N/A, never a convertible status.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

from identify import Identification, load_table

ETL_ELEMENTS_FIELDS = [
    "SessionID",
    "Technology",
    "Category",
    "Subtype",
    "FullName",
    "FileName",
    "Status",
    "EWI Count",
    "EWIs",
    "FDM Count",
    "FDMs",
    "PRF Count",
    "PRFs",
    "Entry Kind",
    "Additional Info",
    "MigrationID",
]

# Subtypes assessment conversion-rate already drops. New rows that use these
# names stay out of the rate even if a consumer ignores Status=N/A.
CONVERSION_RATE_EXCLUDED_SUBTYPES = frozenset(
    {"Path", "Package", "PrecedenceConstraint", "ConnectionManager"}
)

_NAME_ATTRS = ("refId", "NAME", "ObjectName", "name")

# Excluded census rules whose matched node IS the metadata element native reports.
_EXCLUDED_RULE_CATEGORY = {
    "ssis-package-root": ("Control Flow", "Package"),
    "inf-mapping-container": ("Folder", "Mapping"),
}

# Excluded records classified by local tag. CONNECTOR and TRANSFORMATION definition
# records are deliberately absent: native either does not emit them as Path, or
# would duplicate a graph INSTANCE.
_EXCLUDED_TAG_CATEGORY = {
    "path": ("Data Flow", "Path"),
    "PrecedenceConstraint": ("Control Flow", "PrecedenceConstraint"),
    "SOURCE": ("Folder", "Source Definition"),
    "TARGET": ("Folder", "Target Definition"),
}

_UNKNOWN_TAG_CATEGORY = {
    "ConnectionManager": ("Control Flow", "ConnectionManager"),
    "WORKFLOW": ("Folder", "Workflow"),
    "SESSION": ("Workflow", "Session"),
    "SCHEDULER": ("Workflow", "Scheduler"),
}

# Native identity for these is folder-qualified (Folder.object / Folder.mapping.object)
# or a second Declaration row of an INSTANCE already in the graph.
REMAINING_NATIVE_CATEGORIES = (
    "Informatica Mapping-level Declaration duplicates of INSTANCE graph elements",
    "Informatica folder-qualified dotted FullNames (Folder.object / Folder.wf.task)",
    "Informatica Workflow START / TASKINSTANCE / SESSION Instance Success rows",
    "Informatica CONNECTOR rows as Path",
    "SSIS Variable, nested ObjectData ConnectionManager without refId, "
    "pipeline input/connection/externalMetadataColumn unknown objects",
)


def local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def declared_full_name(identity: dict[str, Any] | None) -> str | None:
    """First declared identity value that is an actual name, never TYPE/class."""
    if not identity:
        return None
    by_local = {local_tag(k): v for k, v in identity.items() if v}
    for key in _NAME_ATTRS:
        value = by_local.get(key)
        if value:
            return value
    return None


def find_etl_elements_csv(reports_dir: Path) -> Path | None:
    candidates = sorted(reports_dir.glob("ETL.Elements*.csv"))
    if len(candidates) <= 1:
        return candidates[0] if candidates else None
    timestamped = [p for p in candidates if not p.stem.endswith(".NA")]
    if not timestamped:
        return candidates[0]
    return max(timestamped, key=lambda p: p.name.lower())


def _blank_row(template: dict[str, str]) -> dict[str, str]:
    row = {k: "" for k in ETL_ELEMENTS_FIELDS}
    row["SessionID"] = template.get("SessionID") or "Development Session"
    row["Technology"] = template.get("Technology") or ""
    row["FileName"] = template.get("FileName") or ""
    row["Status"] = "N/A"
    row["EWI Count"] = "0"
    row["EWIs"] = ""
    row["FDM Count"] = "0"
    row["FDMs"] = ""
    row["PRF Count"] = "0"
    row["PRFs"] = ""
    row["Entry Kind"] = "N/A"
    row["MigrationID"] = template.get("MigrationID") or ""
    return row


def _technology_from_table(table: dict) -> str:
    plat = table.get("platform") or ""
    if plat == "SqlServerIntegrationServices":
        return "Ssis"
    if plat == "InformaticaPowerCenter":
        return "InformaticaPowerCenter"
    return plat or "N/A"


def _additional_info(existing: list[dict[str, str]], doc_path: str) -> str:
    for row in existing:
        info = row.get("Additional Info") or ""
        if "sourceDocumentExtension" in info:
            try:
                parsed = json.loads(info)
                ext = parsed.get("sourceDocumentExtension")
                if ext:
                    return json.dumps(
                        {"sourceDocumentExtension": ext, "inGraph": False, "columns": 0},
                        separators=(",", ":"),
                    )
            except json.JSONDecodeError:
                pass
    ext = Path(doc_path).suffix.lstrip(".")
    return json.dumps(
        {"sourceDocumentExtension": ext, "inGraph": False, "columns": 0},
        separators=(",", ":"),
    )


# Leading characters a spreadsheet reads as a formula trigger rather than text.
_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _sanitize_csv_field(value: str) -> str:
    """Prefix a leading formula-trigger character with `'` so Excel/LibreOffice keep the cell as text."""
    if value and value[0] in _CSV_FORMULA_PREFIXES:
        return "'" + value
    return value


def _candidate(category: str, subtype: str, full_name: str, template: dict[str, str],
               additional: str) -> dict[str, str]:
    row = _blank_row(template)
    row["Category"] = _sanitize_csv_field(category)
    row["Subtype"] = _sanitize_csv_field(subtype)
    row["FullName"] = _sanitize_csv_field(full_name)
    row["Additional Info"] = additional
    return row


def metadata_rows(idn: Identification, *, file_name: str, technology: str,
                  template: dict[str, str], additional: str) -> list[dict[str, str]]:
    """N/A rows for declared non-graph census records that already have a name.

    Keyed on (category, subtype, full_name), not full_name alone: a SOURCE and a
    TARGET definition (or any two declared records) can legitimately share a name,
    and a name that happens to match a graph instance from a wholly different
    category/subtype is still a distinct record, not a duplicate of that instance.
    """
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def add(category: str, subtype: str, full_name: str | None) -> None:
        if not full_name:
            return
        key = (category, subtype, full_name)
        if key in seen:
            return
        seen.add(key)
        rows.append(_candidate(category, subtype, full_name, template, additional))

    for rec in idn.excluded:
        tag = local_tag(rec["tag"])
        identity = rec.get("identity") or {}
        rule = rec.get("rule")
        mapped = _EXCLUDED_RULE_CATEGORY.get(rule)
        if mapped is None:
            mapped = _EXCLUDED_TAG_CATEGORY.get(tag)
        if mapped is None:
            continue
        add(mapped[0], mapped[1], declared_full_name(identity))

    for obj in idn.unknown_objects:
        mapped = _UNKNOWN_TAG_CATEGORY.get(local_tag(obj.tag))
        if mapped is None:
            continue
        add(mapped[0], mapped[1], declared_full_name(obj.identity))

    for row in rows:
        if not row.get("FileName"):
            row["FileName"] = file_name
        if not row.get("Technology"):
            row["Technology"] = technology
    return rows


def augment_elements_csv(table: dict, doc_path: str, out_root: str | Path) -> dict[str, Any]:
    """Append missing metadata rows onto the existing ETL.Elements CSV. Graph rows stay put."""
    out = Path(out_root)
    reports = out / "Reports"
    path = find_etl_elements_csv(reports)
    existing: list[dict[str, str]] = []
    fieldnames = list(ETL_ELEMENTS_FIELDS)
    if path is not None and path.is_file():
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames:
                fieldnames = list(reader.fieldnames)
            existing = list(reader)

    idn = Identification(table, doc_path)
    file_name = Path(doc_path).name
    template = existing[0] if existing else {
        "SessionID": "Development Session",
        "Technology": _technology_from_table(table),
        "FileName": file_name,
        "MigrationID": "",
    }
    additional = _additional_info(existing, doc_path)
    # Same key as metadata_rows' own dedup: category/subtype/full_name, not full_name
    # alone, so a declared record is only treated as a duplicate of an existing row
    # that is actually the same kind of thing, not just a same-named different one.
    existing_keys = {
        (r.get("Category") or "", r.get("Subtype") or "", r.get("FullName") or "")
        for r in existing
    }
    added = []
    skipped_dup = 0
    for row in metadata_rows(
        idn,
        file_name=file_name,
        technology=template.get("Technology") or _technology_from_table(table),
        template=template,
        additional=additional,
    ):
        key = (row["Category"], row["Subtype"], row["FullName"])
        if key in existing_keys:
            skipped_dup += 1
            continue
        existing_keys.add(key)
        added.append(row)

    target = path or (reports / "ETL.Elements.NA.csv")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in existing:
            writer.writerow(row)
        for row in added:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    return {
        "path": str(target),
        "graph_rows": len(existing),
        "added": len(added),
        "skipped_dup": skipped_dup,
        "total": len(existing) + len(added),
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 3:
        print("usage: etl_elements_census.py <platform_table.json> <source_document> <out_root>",
              file=sys.stderr)
        return 2
    table_path, doc_path, out_root = args
    stats = augment_elements_csv(load_table(table_path), doc_path, out_root)
    print(
        f"metadata rows: added={stats['added']} skipped_dup={stats['skipped_dup']} "
        f"graph={stats['graph_rows']} total={stats['total']}"
    )
    print(f"artifact     : {stats['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
