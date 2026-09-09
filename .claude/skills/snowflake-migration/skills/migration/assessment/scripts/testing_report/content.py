# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Customer-facing copy for the Testing tab.

Everything a reviewer needs to sign off on wording lives here, with no markup
around it. Strings may contain HTML entities (``&mdash;``, ``&plus;``) and are
emitted verbatim; they are authored content, not user input.

Copy is owned by SNOW-3813566 and reviewed there. The source proposal's internal-only roadmap
note is deliberately absent: it discloses unshipped roadmap and must never reach a
customer-facing report.
"""

from __future__ import annotations

from dataclasses import dataclass

PROVEN = "proven"
RUNTIME = "runtime"

# What the report can say about a precondition it has already established, and
# about one that can only be checked while the step runs.
PRECONDITION_AFFIRMATIONS = {
    PROVEN: "present in this project",
    RUNTIME: "checked when you run capture",
}


@dataclass(frozen=True)
class Precondition:
    """A gate the report can speak to without asking the reader."""

    text: str
    status: str


@dataclass(frozen=True)
class LadderGate:
    """A precondition only the reader knows, which pins the ladder until ticked."""

    key: str
    label: str
    detail: str
    cap_tier_key: str
    cap_reason: str


@dataclass(frozen=True)
class LadderTier:
    """One rung of a testing ladder, as the matrix renders it."""

    key: str
    name: str
    qualifier: str
    provides: str
    buys: str
    untested: str
    # Checkbox label. Empty means the rung is free and never blocks the ladder.
    requirement: str = ""


# Both ladders run lowest-fidelity-first, so the stepper reads left to right
# from least access to most. This inverts the source proposal's numbering for
# procedures (its Tier 1 is the highest fidelity, and is the last rung here).
PROC_LADDER: tuple[LadderTier, ...] = (
    LadderTier(
        key="synthetic",
        name="Synthetic data",
        qualifier="synthesized inputs",
        provides="Nothing beyond the converted code",
        buys="Structural correctness against a schema-inferred data set",
        untested="Real-world data shapes, volumes, and edge cases",
    ),
    LadderTier(
        key="source-synthesized",
        name="Source data",
        qualifier="synthesized inputs",
        provides="Representative source data",
        buys="Branch and boundary coverage validated against real source behavior",
        untested="Parameter combinations that only occur in production traffic",
        requirement="Representative source data",
    ),
    LadderTier(
        key="source-query-log",
        name="Source data",
        qualifier="query-log inputs",
        provides="&plus; a query-log export",
        buys="Test cases seeded from production parameter values, edge cases, and volumes",
        untested="Nothing access-related &mdash; only test-coverage completeness",
        requirement="A query-log export",
    ),
)

ETL_LADDER: tuple[LadderTier, ...] = (
    LadderTier(
        key="data-equivalence",
        name="Data equivalence",
        qualifier="read-only",
        provides="Read-only access on both sides",
        buys="Point-in-time output comparison; orchestrator config equivalence",
        untested="No lineage or root-cause tracing; no re-run drift detection",
        requirement="Read-only access on the source and on Snowflake",
    ),
    LadderTier(
        key="conversion-iteration",
        name="Conversion iteration",
        qualifier="frozen baseline",
        provides="Source-table snapshots &plus; full control on Snowflake",
        buys="Debug-fix cycles against a frozen, known-correct baseline",
        untested="Source-side drift between snapshots; DAG topology",
        requirement="Source-table snapshots, and full control on Snowflake",
    ),
    LadderTier(
        key="coordinated-rerun",
        name="Coordinated re-run",
        qualifier="live baselines",
        provides="Source read-write &plus; pipeline trigger on both sides",
        buys="Reproducible baselines; parameter sensitivity on the source side too",
        untested="Runtime DAG equivalence; contamination risk in shared environments",
        requirement="Source read-write, and pipeline trigger on both sides",
    ),
    LadderTier(
        key="rca-acceleration",
        name="RCA acceleration",
        qualifier="lineage",
        provides="&plus; source execution history",
        buys="Runtime-verified writer lineage; fast root-cause analysis",
        untested="Coordination overhead in shared environments",
        requirement="Source execution history",
    ),
    LadderTier(
        key="gold-standard",
        name="Gold standard",
        qualifier="isolated",
        provides="&plus; dedicated test environments",
        buys="Zero coordination overhead; a synthetic warm-up phase before customer-data cycles",
        untested="Nothing access-related &mdash; only test coverage and synthetic-data quality",
        requirement="Dedicated test environments",
    ),
)

PROC_PRECONDITIONS: tuple[Precondition, ...] = (
    Precondition(
        "Access to the object's source SQL, procedure or function body plus referenced DDL "
        "&mdash; no source code, no conversion, no testing.",
        PROVEN,
    ),
    Precondition("A live source connection at capture time.", RUNTIME),
)

PROC_PRECONDITION_NOTE = (
    "Baselines can only be captured while the source system is reachable &mdash; no source "
    "connectivity means no baseline. Capture them before any decommissioning step in the "
    "migration plan."
)

ETL_PRECONDITIONS: tuple[Precondition, ...] = (
    Precondition(
        "Access to the source ETL code &mdash; no code, no conversion, no testing.",
        PROVEN,
    ),
)

ETL_PRECONDITION_NOTE = (
    "Without orchestrator configuration, output comparisons cannot be interpreted against a "
    "known job structure, and the engagement stays at Data equivalence regardless of what "
    "other access is granted."
)

# The one precondition no registry field can prove, so the reader declares it.
# Unticked, it pins the ladder to the rung ETL_PRECONDITION_NOTE already names.
ETL_GATE = LadderGate(
    key="orchestrator-config",
    label="Orchestrator configuration on both sides (Control-M, Autosys, or Snowflake Tasks)",
    detail=(
        "Job-control tables are not a substitute: they show when jobs ran, not the "
        "dependency graph."
    ),
    cap_tier_key="data-equivalence",
    cap_reason=ETL_PRECONDITION_NOTE,
)

# Shown only for the customer's detected dialect: a PostgreSQL reader does not
# need to read about Oracle SAVEPOINT behavior.
DIALECT_CAVEATS = {
    "sqlserver": "Procedures that write data need snapshot isolation enabled on the source.",
    "teradata": (
        "Procedures that write data need backup-and-restore isolation, plus a parent database "
        "with CREATE DATABASE rights."
    ),
    "oracle": (
        "Procedures that write data use SAVEPOINT-based isolation; procedures containing "
        "COMMIT are not supported yet."
    ),
}

SUPPORTED_PROC_DIALECTS_SENTENCE = (
    "Output testing for procedures and functions is supported today for SQL Server, "
    "Amazon Redshift, Teradata, and Oracle sources."
)

# ``{dialect}`` is filled with the detected source dialect at render time.
UNSUPPORTED_PROC_STATEMENT = (
    "Automated output testing for procedures and functions is not available for {dialect} "
    "sources yet. " + SUPPORTED_PROC_DIALECTS_SENTENCE
)

TAB_LEDE = (
    "This phase confirms that converted code behaves like the source. How much it can confirm "
    "depends on what the engagement has access to, so each ladder below asks what you can "
    "provide and names what that buys you."
)

PROC_LADDER_TITLE = "Procedure &amp; function testing"
ETL_LADDER_TITLE = "ETL orchestration testing"

NOTHING_TO_TEST = (
    "This project's in-scope objects are tables and views, which carry no logic to output-test. "
    "Correctness for them is established by comparing migrated data against the source."
)

DATA_VALIDATION_POINTER = (
    "Row-level and aggregate data comparison is a separate phase &mdash; see "
    "<strong>Data Migration &amp; Validation</strong>."
)

MATRIX_HEADERS = ("Tier", "What you provide", "What it buys", "What stays untested")

CURRENT_KICKER = "YOU ARE HERE"
UNLOCK_KICKER = "UNLOCK"
REACHED_KICKER = "REACHED"
NEXT_KICKER = "NEXT UNLOCK"
BLOCKED_KICKER = "BLOCKED"

PICKER_HEADING = "What can you provide?"
PICKER_HINT = "Optional &mdash; tick to see where you land."

SUMMARY_BUYS_LABEL = "What it buys"
SUMMARY_UNTESTED_LABEL = "Still untested"
SUMMARY_NEXT = "<strong>Next unlock</strong> requires &ldquo;{requirement}&rdquo;."

# Ticked access above a rung the ladder cannot reach: name the lowest thing in
# the way, which is the one the reader can act on.
GAP_MESSAGE = (
    "You already have what <strong>{ticked}</strong> needs. The next thing in the way is "
    "&ldquo;{missing}&rdquo;."
)

CAP_MESSAGE = "You have the access for <strong>{reached}</strong>. {reason}"

# Quoting the requirement sidesteps having to re-case it mid-sentence.
ABSENCE_MESSAGE = (
    "Nothing is reached yet &mdash; <strong>{tier}</strong> itself requires "
    "&ldquo;{requirement}&rdquo;."
)
