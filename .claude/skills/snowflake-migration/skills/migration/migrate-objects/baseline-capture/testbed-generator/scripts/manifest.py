"""Derived progress ledger for the mine phase.

Authority is the on-disk CLI state + artifacts (§1.1); this run.json is a derived
cache of progress/PENDING records, never the sole authority. Written atomically.
"""
from __future__ import annotations

import json
import os
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from pathlib import Path

from critic_index import canon_owner, canon_table
from critic_normalize import normalize

SCHEMA_VERSION = 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def classify_rejections(cells: Iterable[tuple],
                        previously_rejected: Callable[[str | None, str | None, object], bool],
                        ) -> tuple[bool, list[tuple]]:
    """The single home of the "a re-proposed rejected value is a cycle" rule.

    `cells` is (table, column, literal) triples read out of whatever shape the caller holds -- the
    backbone's EntryCheck.identity or the gate's adjudicated REJECT detail. Returns
    (is_cycle, recorded): whether any cited literal was already rejected in an earlier round, and the
    triples the caller must persist with record_rejected_value.

    Two things live here rather than at each call site, which is why they cannot drift apart:

      * A triple whose literal is None cites no VALUE (a structural or out-of-range FAIL), so it
        neither votes on the cycle nor enters the memo. Recording one would key the memo on None and
        make every later non-literal FAIL on that cell read as a repeat; letting one vote would
        escalate a first-ever structural reject to a human. Its crash-loop bound is the per-type
        reject budget instead.
      * The cycle question is answered against the memo as it stands BEFORE anything here is
        persisted, so a round can never trip on its own recording. The (is_cycle, recorded) return
        shape is what holds that ordering: a caller asks once and persists afterwards, because
        `recorded` is handed back rather than written here.

    Stateless on purpose: the gate holds no ledger, so the memo predicate arrives as a callable and
    persisting `recorded` stays the caller's step.
    """
    recorded = [(t, c, lit) for t, c, lit in cells if lit is not None]
    return any(previously_rejected(t, c, lit) for t, c, lit in recorded), recorded


@dataclass
class Manifest:
    schema_version: int = SCHEMA_VERSION
    phase: str = "mine"
    mine_status: str = "pending"  # pending | completed
    validate_status: str = "pending"  # pending | completed
    compile_status: str = "pending"  # pending | completed
    generate_status: str = "pending"  # pending | completed
    enrich_status: str = "pending"  # pending | completed
    enrichment: dict = field(default_factory=lambda: {
        "fragments": 0, "rejections": 0, "retries": 0,
        "iterations": 0, "ready": False, "rejections_by_type": {},
    })
    pending: list = field(default_factory=list)  # [{"object", "reason"}]
    updated_at: str = field(default_factory=_now)

    @classmethod
    def path(cls, project_dir: str) -> Path:
        return Path(project_dir) / ".scai" / "testbed" / "run.json"

    @classmethod
    def load(cls, project_dir: str) -> "Manifest":
        p = cls.path(project_dir)
        if not p.exists():
            return cls()
        # A corrupt derived cache (truncated write, non-object payload, hand-edit)
        # must not abort resume: authority is the on-disk CLI state, so degrade to a
        # fresh ledger rather than propagating the read/parse error. A mid-write
        # truncation can land mid-codepoint (UnicodeDecodeError) or race a reader
        # (OSError), so guard the whole triple — the same set run_pipeline's predicate
        # readers guard.
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return cls()
        if not isinstance(raw, dict):
            return cls()
        known = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in raw.items() if k in known}
        # A known field carrying the wrong runtime type (a hand-edited `"pending": "oops"`)
        # constructs fine but blows up later (record_pending does list.append), so degrade
        # to fresh now — same "never propagate a bad cache" contract as the guards above.
        blank = cls()
        if any(not isinstance(v, type(getattr(blank, k))) for k, v in filtered.items()):
            return cls()
        return cls(**filtered)

    def record_pending(self, obj: str, reason: str) -> None:
        self.pending.append({"object": obj, "reason": reason})

    def mark_mine_complete(self) -> None:
        self.mine_status = "completed"

    def mark_compile_complete(self) -> None:
        self.compile_status = "completed"
        self.phase = "compile"

    def mark_validate_complete(self) -> None:
        self.validate_status = "completed"
        self.phase = "validate"

    def mark_generate_complete(self) -> None:
        self.generate_status = "completed"
        self.phase = "generate"

    def mark_enrich_complete(self) -> None:
        self.enrich_status = "completed"
        self.enrichment["ready"] = True

    def record_fragments(self, n: int) -> None:
        # Overwrite, not sum: re-application of the same fragments must not inflate the tally (design §7, Inv 3).
        self.enrichment["fragments"] = n

    def record_rejection(self, prompt_type: str) -> None:
        self.enrichment["rejections"] += 1
        by_type = self.enrichment["rejections_by_type"]
        by_type[prompt_type] = by_type.get(prompt_type, 0) + 1

    def record_retry(self) -> None:
        self.enrichment["retries"] += 1

    def record_iteration(self) -> None:
        self.enrichment["iterations"] += 1

    def rejection_budget_exhausted(self, prompt_type: str, cap: int) -> bool:
        return self.enrichment["rejections_by_type"].get(prompt_type, 0) >= cap

    def iteration_budget_exhausted(self, cap: int) -> bool:
        return self.enrichment["iterations"] >= cap

    def reset_enrich_budget(self) -> None:
        # Explicit fresh-human-run override only; never implicit, or a crash-loop would reset and bound nothing.
        # Clearing rejected_values_by_cell is the point, not a leak: a value_cycle stop would otherwise be
        # unrecoverable, since the human's corrected re-proposal keeps tripping the same memo.
        self.enrichment = {"fragments": 0, "rejections": 0, "retries": 0,
                           "iterations": 0, "ready": False, "rejections_by_type": {}}

    _CELL_SEP = "\x1f"

    @classmethod
    def _cell_key(cls, table: str | None, column: str | None) -> str:
        # A qualified name keys on its own owner. Keying every name on the bare table put SALES.ORDERS.TIER
        # and STAGING.ORDERS.TIER in one bucket, so a first-ever literal on one read as a re-proposal of the
        # one rejected on the other, and escalated a healthy run to a human.
        name = str(table or "")
        owner = canon_owner(name) if "." in name else canon_table(name)
        return f"{owner}{cls._CELL_SEP}{str(column).upper()}"

    def _buckets_for(self, table: str | None, column: str | None):
        # Lookup is deliberately more permissive than the key: a bare name could denote any owner, so it
        # also matches what an earlier round recorded qualified. A qualified name matches only itself.
        memo = self.enrichment.get("rejected_values_by_cell", {})
        exact = self._cell_key(table, column)
        if exact in memo:
            yield memo[exact]
        if "." in str(table or ""):
            return
        want = f"{canon_table(table)}{self._CELL_SEP}{str(column).upper()}"
        for key, values in memo.items():
            owner, _, col = key.partition(self._CELL_SEP)
            if key != exact and f"{canon_table(owner)}{self._CELL_SEP}{col}" == want:
                yield values

    def record_rejected_value(self, table: str | None, column: str | None, value: object) -> None:
        memo = self.enrichment.setdefault("rejected_values_by_cell", {})
        bucket = memo.setdefault(self._cell_key(table, column), [])
        # normalize() folds case and strips matching quotes, matching how the gate grounds literals,
        # so a re-proposed 'GOLD'/gold/GOLD is recognized as the same already-rejected value.
        s = normalize(value)
        if s not in bucket:
            bucket.append(s)

    def value_previously_rejected(self, table: str | None, column: str | None,
                                  value: object) -> bool:
        s = normalize(value)
        return any(s in bucket for bucket in self._buckets_for(table, column))

    def save(self, project_dir: str) -> None:
        self.updated_at = _now()
        p = self.path(project_dir)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        # Explicit utf-8 both ways (load reads it back the same). This write cannot corrupt today
        # and the pin is not what stops it: json.dumps escapes non-ASCII (ensure_ascii defaults to
        # True), so these bytes are pure ASCII and identical under every ASCII-superset locale
        # codec. What the pin buys is that the ledger's encoding is declared here rather than
        # inherited, so the round trip stays well-defined the day a writer emits the artifacts'
        # object/column names raw -- a mis-decoded rejected-value memo silently stops recognizing a
        # re-proposed literal.
        tmp.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        os.replace(tmp, p)  # atomic on POSIX
