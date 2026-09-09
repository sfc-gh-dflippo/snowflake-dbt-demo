"""Classify scai testbed failures into a remediation class.

Deterministic-first: known error codes map to a canned class; unknowns escalate.
DATA_QUARANTINE encodes the C5 init contract — init aborts atomically on a bad
artifact, so the remediation is quarantine-the-artifact + PENDING + re-run.
"""
from __future__ import annotations

from enum import Enum


class RecoveryClass(str, Enum):
    INPUT_CONFIG = "input_config"       # fix input/config, re-run the station
    DATA_ISOLABLE = "data_isolable"     # bad object token -> PENDING that object, continue
    DATA_QUARANTINE = "data_quarantine" # malformed artifact -> quarantine + PENDING + re-run
    ESCALATE = "escalate"               # unknown / defect -> stop with a structured diagnosis
    REPROMPT = "reprompt"   # malformed enrichment field -> re-prompt the offending fragment
    RETRY = "retry"         # concurrent state change (CAS loss) -> retry the same envelope


_MAP: dict[str, RecoveryClass] = {
    "PRJ0003": RecoveryClass.INPUT_CONFIG,
    "TBD0002": RecoveryClass.INPUT_CONFIG,  # state file not found (init not yet run)
    "TBD0006": RecoveryClass.INPUT_CONFIG,
    "TBD0007": RecoveryClass.INPUT_CONFIG,
    "TBD0008": RecoveryClass.DATA_ISOLABLE,
    "TBD0010": RecoveryClass.DATA_ISOLABLE,
    "TBD0009": RecoveryClass.DATA_QUARANTINE,
    "TBD0011": RecoveryClass.DATA_QUARANTINE,
    "TBD0012": RecoveryClass.INPUT_CONFIG,  # NotCompiled — run compile before generate
    "TBD0003": RecoveryClass.ESCALATE,  # state magic mismatch — state.bin unreadable
    "TBD0004": RecoveryClass.ESCALATE,  # state version mismatch — regenerate via init
    "TBD0005": RecoveryClass.ESCALATE,  # state corrupt / duplicate object identity
    "TBD0014": RecoveryClass.REPROMPT,  # EnrichmentRejected — malformed/unknown field
    "TBD0015": RecoveryClass.ESCALATE,  # EnrichmentCycle — structural; re-prompting the same edge loops
    "TBD0016": RecoveryClass.RETRY,     # EnrichmentStateChanged — retryable with the same input
}


def classify(error_code: str) -> RecoveryClass:
    return _MAP.get(error_code, RecoveryClass.ESCALATE)
