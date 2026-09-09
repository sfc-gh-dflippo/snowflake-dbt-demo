"""Mechanical fit score. No model, no judgement, no self-grading.

fit(element) = satisfied_obligations / total_obligations

An obligation is satisfied only when the field was populated AND the value came
from an identified provenance: a structural query (SOURCE), the per-platform
table (TABLE), or a named algorithm over identified structure (DERIVED).

NO_SLOT / RESIDUE / MISSING obligations score zero. That is the point: a source
fact the contract cannot hold, or an expression a model must still translate, is
a real gap in coverage and must show up in the number.

Census gate:
  NotSupported  element $kind has no door in the hydrator, OR the table refused
                the kind and a MODEL assertion of $kind is the only thing filling it
  Success       fit == 1.0 and $kind was not MODEL-authored over a table refusal
  Partial       0 < fit < 1.0, including MODEL $kind when other obligations are met
"""

import math
import re
from collections import Counter, defaultdict

from identify import DERIVED, MISSING, MODEL, NO_SLOT, RESIDUE, SOURCE, TABLE

# Credential-shaped key patterns for the `report()` choke point only -- the
# emitted IR and any sidecar are untouched, because neither carries a
# credential value: no_slot_facts rules like DataStage's `credential_ref`
# exist precisely because the IR has no field for a Username or a
# ConnectionString, so the raw value only ever reaches a human via this
# report's `detail` column. `_looks_credential_shaped` itself is matched
# against `path`/`where` (the rule id and attribute key) only, never against
# `detail`, so an unrelated diagnostic whose VALUE happens to contain one of
# these words is not swept up by this check alone. `_value_looks_credential_shaped`
# below is the separate, content-based signal that catches the opposite case:
# a key/path that does not look credential-shaped but a detail value that does.
_CREDENTIAL_KEY_TOKENS = (
    "password", "passwd", "pwd", "secret", "token", "credential",
    "apikey", "accesskey", "privatekey", "clientsecret",
    "connectionstring", "username",
)

# Content-shaped credential detector, independent of the key-name check above:
# a long single token drawn from a base64/hex-like alphabet with high
# per-character entropy looks like a real secret regardless of what the
# rule id or attribute key was called. Either signal is sufficient to redact.
_CREDENTIAL_VALUE_TOKEN_RE = re.compile(r"^[A-Za-z0-9+/_=-]{20,}$")
_CREDENTIAL_VALUE_ENTROPY_THRESHOLD = 3.0


def _shannon_entropy(s: str) -> float:
    length = len(s)
    if not length:
        return 0.0
    counts = Counter(s)
    return -sum((n / length) * math.log2(n / length) for n in counts.values())


def _looks_credential_shaped(*sources: str) -> bool:
    for s in sources:
        if not s:
            continue
        norm = re.sub(r"[^a-z0-9]", "", s.lower())
        if any(tok in norm for tok in _CREDENTIAL_KEY_TOKENS):
            return True
    return False


def _value_looks_credential_shaped(value: str) -> bool:
    """True when the value's *content* -- not its key name -- looks like a
    credential: a long, high-entropy, base64/hex-like token embedded
    anywhere in the text (whitespace-delimited)."""
    if not value:
        return False
    for token in value.split():
        if (_CREDENTIAL_VALUE_TOKEN_RE.match(token)
                and _shannon_entropy(token) >= _CREDENTIAL_VALUE_ENTROPY_THRESHOLD):
            return True
    return False


def _report_detail(s) -> str:
    """The `detail` text as it should appear in the report -- redacted when
    the slot's path or where names a credential-shaped key, or when the
    detail value itself looks credential-shaped by content."""
    if s.detail and (_looks_credential_shaped(s.path, s.where)
                      or _value_looks_credential_shaped(s.detail)):
        return "[REDACTED]"
    return s.detail


def score(slots) -> dict:
    by_el = defaultdict(list)
    for s in slots:
        by_el[s.element].append(s)

    result = {"elements": {}, "total": {}}
    for el, group in by_el.items():
        sat = sum(1 for s in group if s.satisfied)
        tot = len(group)
        kind_slots = [s for s in group if s.path == "element.$kind"]
        unsupported = any(s.provenance == MISSING for s in kind_slots)
        model_kind = any(s.provenance == MODEL for s in kind_slots)
        fit = sat / tot if tot else 0.0
        if unsupported:
            status = "NotSupported"
        elif model_kind:
            # MODEL $kind is an assertion, not a table door. Success would report a
            # conversion the platform table refused. Partial only when other
            # obligations actually scored; otherwise the refusal stays NotSupported.
            status = "Partial" if sat > 0 else "NotSupported"
        elif sat == tot:
            status = "Success"
        else:
            status = "Partial"
        result["elements"][el] = {
            "fit": fit,
            "satisfied": sat,
            "total": tot,
            "status": status,
            "provenance": dict(Counter(s.provenance for s in group)),
            "slots": group,
        }

    sat = sum(1 for s in slots if s.satisfied)
    tot = len(slots)
    result["total"] = {
        "fit": sat / tot if tot else 0.0,
        "satisfied": sat,
        "total": tot,
        "provenance": dict(Counter(s.provenance for s in slots)),
    }
    return result


def report(scored: dict) -> str:
    lines = []
    order = [SOURCE, TABLE, DERIVED, MODEL, RESIDUE, NO_SLOT, MISSING]
    lines.append("=" * 78)
    lines.append("FIT SCORE  (mechanical: field-level completeness x identified provenance)")
    lines.append("=" * 78)
    for el, d in scored["elements"].items():
        lines.append("")
        lines.append(f"{el}")
        lines.append(f"  fit {d['fit'] * 100:5.1f}%   {d['satisfied']}/{d['total']} obligations"
                     f"   census: {d['status']}")
        prov = "  ".join(f"{k}={d['provenance'][k]}" for k in order if k in d["provenance"])
        lines.append(f"  provenance: {prov}")
        unmet = [s for s in d["slots"] if not s.satisfied]
        if unmet:
            lines.append(f"  UNMET ({len(unmet)}):")
            for s in unmet:
                lines.append(f"    [{s.provenance:7}] {s.path}")
                lines.append(f"              at {s.where}")
                detail = _report_detail(s)
                if detail:
                    lines.append(f"              {detail}")
        met = [s for s in d["slots"] if s.satisfied]
        if met:
            lines.append(f"  MET ({len(met)}):")
            for s in met:
                detail = _report_detail(s)
                extra = f"  {detail}" if detail else ""
                lines.append(f"    [{s.provenance:7}] {s.path:44} <- {s.where}{extra}")
    t = scored["total"]
    lines.append("")
    lines.append("=" * 78)
    prov = "  ".join(f"{k}={t['provenance'][k]}" for k in order if k in t["provenance"])
    lines.append(f"TOTAL FIT {t['fit'] * 100:.1f}%   {t['satisfied']}/{t['total']} obligations")
    lines.append(f"provenance: {prov}")
    lines.append("=" * 78)
    lines.append("")
    lines.append("CENSUS")
    for el, d in scored["elements"].items():
        if el.startswith("<"):
            continue
        lines.append(f"  {el:18} {d['status']:13} fit {d['fit'] * 100:5.1f}%")
    return "\n".join(lines)
