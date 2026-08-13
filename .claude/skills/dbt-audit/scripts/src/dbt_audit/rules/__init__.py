"""
Rule packs. Importing this package registers every rule in ``core.base.REGISTRY``.

Ten packs:

| Pack | Concern | Tier |
|------|---------|------|
| PRJ  | project structure and fragmentation | universal |
| INC  | load patterns and incremental correctness | universal |
| SQL  | query construction: subquery vs CTE vs ephemeral | universal |
| MAC  | macro over-use and under-use | universal |
| MAT  | materialization fitness | mixed |
| TST  | testing and constraint coverage | universal |
| DOC  | documentation coverage | universal |
| ARC  | architecture and lineage conventions | architecture |
| MIG  | unresolved conversion debt | migration |
| OPS  | operational hygiene | universal |
"""

from __future__ import annotations

from dbt_audit.rules import arc, doc, inc, mac, mat, mig, ops, prj, sql, tst

__all__ = ["arc", "doc", "inc", "mac", "mat", "mig", "ops", "prj", "sql", "tst"]
