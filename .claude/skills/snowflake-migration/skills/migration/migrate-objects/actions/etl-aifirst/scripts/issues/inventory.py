"""THE INVENTORY: append-only, one file per type, classify before you mint.

WHY IT IS A DIRECTORY AND NOT A FILE
------------------------------------
A single `inventory.json` that every agent reads, edits and writes back is a lost-update
race with no lock. One file per type, named by the type's own content-addressed id, is
concurrency-safe BY CONSTRUCTION:

  * two agents that found the SAME issue derive the same id, so they write the same
    filename with the same bytes -- the race is benign;
  * two agents that found DIFFERENT issues write different filenames -- they cannot
    collide;
  * a type file is created with O_CREAT|O_EXCL, so "create if absent" is one atomic
    syscall rather than a check followed by a write. The loser of a race does not
    overwrite; it records a divergence if the content differed and otherwise does
    nothing.

NOTHING IS EVER RENUMBERED, because there is no number. That is not neatness: emitted
artifacts CITE these codes, and a code whose meaning shifts makes last week's output
unreadable. It also means a type is never edited in place -- a correction is a new type
plus a `supersedes` pointer, never a mutation of a code someone else has already shipped.

PROPOSE, THEN PROMOTE
---------------------
Agents PROPOSE into `proposals/`; a single writer PROMOTES into `types/`. Proposals are
idempotent atomic writes, so a proposing agent needs no coordination at all. The
single-writer step is where the classification is enforced and where the append-only
guarantee is kept in one place instead of in every caller. `classify_or_mint` exists for
the in-process case (the driver stage) and takes the same path.

CLASSIFY BEFORE MINT, AND WHY THE MATCHING IS THE WHOLE THING
-------------------------------------------------------------
We are escaping a closed 888-member enum whose only two "not supported" members name the
two platforms the engine already supports. The failure mode of the OPEN vocabulary that
replaces it is fifty near-duplicate types for one issue -- the mirror defect, and just as
useless for aggregation. The only thing standing between those two failures is that a
lookup runs before every mint and that the lookup is good enough.

So: an exact signature hit REUSES. A near-duplicate above NEAR_DUP reuses and records the
redirect. A candidate in the ambiguous band forces the proposer to state, in writing,
what distinguishes the new type from it -- and refuses the mint if they cannot. Every
mint stores the full candidate list with scores, so "no existing type matched" is an
inspectable claim rather than an assertion.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from difflib import SequenceMatcher
from pathlib import Path

from .signature import (CATEGORIES, SIG_VERSION, canonical, normalise,
                        signature_id)
from .textrule import lint

# A weighted score at or above this means "the same issue, worded differently" -- reuse.
NEAR_DUP = 0.82
# Between this and NEAR_DUP the proposer MUST say what differs, or the mint is refused.
AMBIGUOUS = 0.60
# Independently of the weighted score: two types whose human-readable statements are this
# similar are the same type. This rule, not the token scores, is what actually stops the
# fifty-near-duplicates failure -- token overlap is easy to dodge by accident, prose is
# not.
TEXT_SHORT_CIRCUIT = 0.85


class MintWithoutClassification(RuntimeError):
    """A type was written without an inventory lookup. Refused: the lookup IS the
    defence against an open vocabulary sprawling into near-duplicates."""


class NearDuplicateWithoutDistinguisher(RuntimeError):
    """A candidate scored in the ambiguous band and the proposer said nothing about what
    differs. Refused rather than minted, because an unexplained near-duplicate is
    indistinguishable from a duplicate."""


class PlatformAssertionRefused(RuntimeError):
    """The text asserts what the source platform does, or claims a fidelity property
    nothing here checks."""


def _atomic_write(path: Path, data: str) -> None:
    """Write via a temp file in the same directory + os.replace.

    os.replace is atomic on POSIX, so a concurrent reader sees either the old file or
    the new one and never a half-written one. Two writers with identical content produce
    identical results in either order.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _append_line(path: Path, line: str) -> None:
    """Append one line. O_APPEND makes a single small write atomic between processes,
    which is all an audit log needs and is why the log is lines and not JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line.rstrip("\n") + "\n")


def _tokset(s: str) -> set[str]:
    return {t for t in normalise(s).replace(":", "-").split("-") if t}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").casefold(), (b or "").casefold()).ratio()


class Inventory:
    """The issue-type inventory rooted at `root`.

    root/types/<id>.json        one immutable record per type
    root/proposals/<id>.json    agent proposals awaiting promotion
    root/mints.log              one line per mint, reuse and refusal
    root/divergences.log        one line per same-id-different-content collision
    """

    def __init__(self, root: str | os.PathLike):
        self.root = Path(root)
        self.types_dir = self.root / "types"
        self.proposals_dir = self.root / "proposals"
        self.mints_log = self.root / "mints.log"
        self.divergences_log = self.root / "divergences.log"
        self.reload()

    # ---------------------------------------------------------------- reading
    def reload(self) -> None:
        self.types: dict[str, dict] = {}
        if self.types_dir.is_dir():
            for p in sorted(self.types_dir.glob("AIM-*.json")):
                try:
                    rec = json.loads(p.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    # A half-written file cannot happen (atomic replace), so this means
                    # a hand-edit. Loud, not silent, and not fatal to a run.
                    _append_line(self.divergences_log,
                                 f"{time.strftime('%FT%TZ', time.gmtime())} UNREADABLE "
                                 f"{p.name}")
                    continue
                self.types[rec["id"]] = rec

    def __len__(self) -> int:
        return len(self.types)

    # ------------------------------------------------------------ classifying
    def classify(self, proposal: dict) -> dict:
        """Look the proposal up in the inventory. NEVER mints.

        Returns {"verdict": EXACT|NEAR_DUPLICATE|NOVEL, "id": <id or None>,
                 "computed_id", "considered": [...], "rule": <which rule decided>}.

        `considered` holds every existing type with its score and, for anything in or
        above the ambiguous band, the fields that differ -- so the record of "no
        existing type matched" names the candidates it was compared against.
        """
        cid, sig, material = signature_id(
            proposal["category"], proposal["construct"], proposal["reason"])
        ptext = f"{proposal.get('title', '')} {proposal.get('text', '')}"

        if cid in self.types:
            return {"verdict": "EXACT", "id": cid, "computed_id": cid,
                    "signature": sig, "hashed_material": material,
                    "rule": "SIGNATURE_IDENTICAL", "considered": []}

        considered = []
        for tid, rec in self.types.items():
            tsig = rec["signature"]
            cat_eq = 1.0 if tsig["category"] == sig["category"] else 0.0
            con = _jaccard(_tokset(tsig["construct"]), _tokset(sig["construct"]))
            rsn = (1.0 if tsig["reason"] == sig["reason"]
                   else _ratio(tsig["reason"], sig["reason"]))
            txt = _ratio(f"{rec.get('title', '')} {rec.get('text', '')}", ptext)
            score = 0.35 * cat_eq + 0.30 * con + 0.20 * rsn + 0.15 * txt
            entry = {
                "id": tid, "score": round(score, 4),
                "parts": {"category_equal": cat_eq, "construct_jaccard": round(con, 4),
                          "reason_similarity": round(rsn, 4),
                          "text_similarity": round(txt, 4)},
                "differs_in": [f for f in ("category", "construct", "reason")
                               if tsig[f] != sig[f]],
            }
            if cat_eq == 1.0 and txt >= TEXT_SHORT_CIRCUIT:
                entry["short_circuit"] = "TEXT_NEAR_IDENTICAL"
            considered.append(entry)

        considered.sort(key=lambda e: -e["score"])
        best = considered[0] if considered else None

        if best and best.get("short_circuit"):
            return {"verdict": "NEAR_DUPLICATE", "id": best["id"], "computed_id": cid,
                    "signature": sig, "hashed_material": material,
                    "rule": "TEXT_NEAR_IDENTICAL_SAME_CATEGORY",
                    "considered": considered}
        if best and best["score"] >= NEAR_DUP:
            return {"verdict": "NEAR_DUPLICATE", "id": best["id"], "computed_id": cid,
                    "signature": sig, "hashed_material": material,
                    "rule": f"WEIGHTED_SCORE>={NEAR_DUP}", "considered": considered}
        return {"verdict": "NOVEL", "id": None, "computed_id": cid, "signature": sig,
                "hashed_material": material, "rule": "NO_CANDIDATE_ABOVE_THRESHOLD",
                "considered": considered}

    # --------------------------------------------------------------- proposing
    def propose(self, proposal: dict, by: str) -> dict:
        """Write a proposal. Safe to call concurrently from any number of agents.

        Deliberately does NOT touch types/. A proposing agent has no write access to the
        inventory proper and needs no coordination: it writes one file named by the id
        it derived, and an agent that derived the same id writes the same content.
        """
        checked = self._check_text(proposal)
        cid, sig, material = signature_id(
            proposal["category"], proposal["construct"], proposal["reason"])
        record = self._record(proposal, cid, sig, material, checked)
        record["proposed_by"] = by
        # NOT a timestamp: a timestamp would make two identical proposals differ, which
        # would turn a benign race into a spurious divergence. The proposal is pure
        # content; WHEN it was seen belongs to the instance, not the type.
        _atomic_write(self.proposals_dir / f"{cid}.json",
                      json.dumps(record, indent=2, sort_keys=True) + "\n")
        return {"id": cid, "path": str(self.proposals_dir / f"{cid}.json")}

    def promote(self, by: str = "single-writer") -> dict:
        """SINGLE WRITER. Fold proposals into the inventory, classifying each first."""
        out = {"minted": [], "reused": [], "refused": [], "already": [], "raced": [],
               "redirects": {}}
        if not self.proposals_dir.is_dir():
            return out
        for p in sorted(self.proposals_dir.glob("AIM-*.json")):
            try:
                proposal = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                out["refused"].append({"path": p.name, "why": "unreadable proposal"})
                continue
            proposal.setdefault("category", proposal.get("signature", {}).get("category"))
            proposal.setdefault("construct",
                                proposal.get("signature", {}).get("construct"))
            proposal.setdefault("reason", proposal.get("signature", {}).get("reason"))
            try:
                res = self.classify_or_mint(proposal, by=proposal.get("proposed_by", by))
            except (MintWithoutClassification, NearDuplicateWithoutDistinguisher,
                    PlatformAssertionRefused) as exc:
                out["refused"].append({"id": proposal.get("id"),
                                       "why": f"{type(exc).__name__}: {exc}"})
                continue
            out[{"MINTED": "minted", "REUSED_EXACT": "already",
                 "REUSED_NEAR": "reused", "MINT_RACED": "raced"}[res["action"]]].append(
                     res["id"])
            # The proposal's own id can differ from res["id"] when classification
            # redirects it to a near-duplicate that already exists -- a caller who
            # serialized the proposal's id elsewhere (e.g. into an issues artifact)
            # before promotion needs this to fix up that stale citation.
            original_id = proposal.get("id")
            if original_id and original_id != res["id"]:
                out["redirects"][original_id] = res["id"]
            p.unlink(missing_ok=True)
        return out

    # ------------------------------------------------------------- the one door
    def classify_or_mint(self, proposal: dict, by: str) -> dict:
        """The ONLY way a type enters the inventory. Classification is not optional.

        `proposal` needs category / construct / reason / title / text, and
        `distinguisher` when a candidate lands in the ambiguous band.
        """
        checked = self._check_text(proposal)
        cls = self.classify(proposal)

        if cls["verdict"] in ("EXACT", "NEAR_DUPLICATE"):
            action = "REUSED_EXACT" if cls["verdict"] == "EXACT" else "REUSED_NEAR"
            self._log_mint(action, cls["id"], by, cls, proposal)
            return {"id": cls["id"], "action": action, "classification": cls}

        best = cls["considered"][0] if cls["considered"] else None
        if (best and best["score"] >= AMBIGUOUS
                and not (proposal.get("distinguisher") or "").strip()):
            self._log_mint("REFUSED", cls["computed_id"], by, cls, proposal)
            raise NearDuplicateWithoutDistinguisher(
                f"{cls['computed_id']} scores {best['score']} against {best['id']} "
                f"(>= {AMBIGUOUS}) and the proposal states no distinguisher. Either "
                f"reuse {best['id']} or say in `distinguisher` what a reviewer would do "
                f"differently for this type."
            )

        record = self._record(proposal, cls["computed_id"], cls["signature"],
                              cls["hashed_material"], checked)
        record["mint"] = {
            "by": by,
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "distinguisher": proposal.get("distinguisher", ""),
            "category_novel": record["signature"]["category"] not in CATEGORIES,
            # THE AUDITABLE PART. Not "nothing matched" -- the list of what it was
            # compared against, each with its score and the fields that differ.
            "classification": {k: cls[k] for k in ("verdict", "rule", "considered")},
        }
        created = self._write_type(record)
        # MINT_RACED, AND THE NEGATIVE TEST IS WHY IT EXISTS.
        #
        # Eight processes released at the same instant all classified against an
        # inventory that was still empty, all got NOVEL, and all called _write_type. The
        # O_EXCL create means exactly ONE file exists afterwards -- the outcome was
        # always correct -- but every worker REPORTED "MINTED", so the audit log claimed
        # eight mints of one type. A log that describes one record as eight is not a
        # record of a benign race; it is a race that has been hidden.
        #
        # So the losers report MINT_RACED: classified as novel, and by the time the write
        # happened an identical type already existed. The race is now VISIBLE in the log
        # and still benign in the store.
        action = "MINTED" if created else "MINT_RACED"
        self._log_mint(action, record["id"], by, cls, proposal)
        if created:
            self.types[record["id"]] = record
        else:
            self.reload()
        return {"id": record["id"], "action": action, "classification": cls}

    # ----------------------------------------------------------------- internals
    def _check_text(self, proposal: dict) -> dict:
        """Run the platform-assertion rule. A REJECT stops the mint."""
        title = proposal.get("title", "")
        text = proposal.get("text", "")
        res = lint(f"{title}. {text}", scope="type")
        if res["verdict"] == "REJECT":
            reasons = "; ".join(f"[{f['rule']}] {f['match']!r}: {f['why']}"
                                for f in res["findings"]
                                if f["severity"] == "REJECT")
            raise PlatformAssertionRefused(reasons)
        # The note is inventory-internal prose about our own tooling, so it is linted
        # for the record and never blocks: "RouterTransformation is abstract with only
        # platform-specific subclasses" is a true statement about the engine that a type
        # SHOULD be allowed to record.
        note_res = lint(proposal.get("note", "") or "-", scope="instance")
        return {"text": res, "note": note_res}

    def _record(self, proposal: dict, cid: str, sig: dict, material: str,
                checked: dict) -> dict:
        return {
            "id": cid,
            "sig_version": SIG_VERSION,
            "signature": sig,
            "hashed_material": material,
            "title": proposal["title"],
            "text": proposal["text"],
            "impact": proposal.get("impact", "output-incomplete"),
            "note": proposal.get("note", ""),
            # PERSISTED HERE AND NOT ONLY UNDER mint, AND A TEST CAUGHT WHY. It used to
            # live only in the mint receipt, so a proposal written to disk lost it: the
            # single writer read the proposal back, found no distinguisher, and refused a
            # perfectly good mint as an unexplained near-duplicate. The propose/promote
            # path was broken for exactly the proposals that needed a rationale most.
            "distinguisher": proposal.get("distinguisher", ""),
            "first_observed": proposal.get("first_observed", ""),
            "supersedes": proposal.get("supersedes", ""),
            "text_lint": checked["text"],
            "note_lint": checked["note"],
        }

    def _write_type(self, record: dict) -> bool:
        """Create types/<id>.json atomically. Returns True if THIS call created it.

        The classification receipt is checked HERE and not only in classify_or_mint, so
        a caller that reaches around the front door still cannot write an unclassified
        type. That is the difference between a constraint in a comment and a constraint
        in the code -- a distinction this project has already paid for once.
        """
        if not (record.get("mint") or {}).get("classification"):
            raise MintWithoutClassification(
                f"{record.get('id')} carries no classification receipt. Mint through "
                f"classify_or_mint(), which runs the inventory lookup first."
            )
        path = self.types_dir / f"{record['id']}.json"
        payload = json.dumps(record, indent=2, sort_keys=True) + "\n"
        self.types_dir.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            # APPEND-ONLY. Somebody else got there first. Never overwrite: the existing
            # record may already be cited by an emitted artifact.
            existing = json.loads(path.read_text(encoding="utf-8"))
            drift = [k for k in ("title", "text", "signature")
                     if existing.get(k) != record.get(k)]
            if drift:
                _append_line(
                    self.divergences_log,
                    f"{time.strftime('%FT%TZ', time.gmtime())} SAME_ID_DIFFERENT_CONTENT "
                    f"{record['id']} fields={','.join(drift)} "
                    f"kept={existing.get('mint', {}).get('by')} "
                    f"discarded={record.get('mint', {}).get('by')}")
            return False
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(payload)
        return True

    def _log_mint(self, action: str, cid: str, by: str, cls: dict,
                  proposal: dict) -> None:
        best = cls["considered"][0] if cls["considered"] else None
        _append_line(self.mints_log, json.dumps({
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action": action, "id": cid, "by": by, "verdict": cls["verdict"],
            "rule": cls["rule"],
            "best_candidate": (best or {}).get("id"),
            "best_score": (best or {}).get("score"),
            "distinguisher": proposal.get("distinguisher", ""),
        }, sort_keys=True))

    # --------------------------------------------------------------------- audit
    def audit(self) -> list[str]:
        """Human-readable account of the inventory and of every mint's rationale."""
        out = [f"inventory root : {self.root}",
               f"types          : {len(self.types)} (sig {SIG_VERSION})"]
        for tid in sorted(self.types):
            rec = self.types[tid]
            sig = rec["signature"]
            out.append(f"  {tid}")
            out.append(f"    signature   : {sig['category']} | {sig['construct']} | "
                       f"{sig['reason']}")
            out.append(f"    title       : {rec['title']}")
            out.append(f"    text lint   : {rec['text_lint']['verdict']} "
                       f"({rec['text_lint']['rule_version']})")
            mint = rec.get("mint") or {}
            out.append(f"    minted by   : {mint.get('by')} at {mint.get('at')}")
            if mint.get("distinguisher"):
                out.append(f"    distinguish : {mint['distinguisher']}")
            cand = (mint.get("classification") or {}).get("considered") or []
            if cand:
                top = ", ".join(f"{c['id']}={c['score']}" for c in cand[:3])
                out.append(f"    no match vs : {top}")
            else:
                out.append("    no match vs : (inventory was empty at mint time)")
            if rec.get("first_observed"):
                out.append(f"    first seen  : {rec['first_observed']}")
        if self.divergences_log.is_file():
            out.append(f"divergences    : {self.divergences_log}")
            for line in self.divergences_log.read_text(encoding="utf-8").splitlines():
                out.append(f"  {line}")
        return out

    def stability_check(self) -> list[str]:
        """Recompute every stored id from its stored signature.

        This is the append-only / never-renumber property, checked rather than asserted:
        if any id in the inventory is not the hash of its own signature, something
        renumbered.
        """
        bad = []
        for tid, rec in self.types.items():
            if rec.get("sig_version") != SIG_VERSION:
                continue  # an older normaliser's id is legitimately not recomputable
            sig = rec["signature"]
            recomputed, _, _ = signature_id(sig["category"], sig["construct"],
                                            sig["reason"])
            if recomputed != tid:
                bad.append(f"{tid} recomputes to {recomputed}")
        return bad


if __name__ == "__main__":
    # `python3 -m issues.inventory [root]` from the callable-entrypoint directory --
    # read the inventory and its mint rationales without needing a migration run. The
    # audit is the answer to "why does this code exist and what was it compared against",
    # which is the question a reviewer of an emitted artifact will actually have.
    # (`-m` and not a direct path: this is a package module and uses relative imports.)
    import sys as _sys
    _root = _sys.argv[1] if len(_sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent / "issue-inventory")
    _inv = Inventory(_root)
    for _line in _inv.audit():
        print(_line)
    _bad = _inv.stability_check()
    print("id stability  : " + ("OK — every id recomputes from its own signature"
                                if not _bad else f"*** {_bad}"))
