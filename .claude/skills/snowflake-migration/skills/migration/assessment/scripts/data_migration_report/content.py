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

"""Customer-facing copy for the Data Migration & Validation tab.

Everything a reviewer needs to sign off on wording lives here, with no markup
around it. Strings may contain HTML entities (``&mdash;``, ``&rsquo;``) and are
emitted verbatim; they are authored content, not user input.

Copy is owned by SNOW-3813566 and reviewed there; the four published platform pages it draws on
are cited in ``snowconvert_reports/type_coverage.py``.

The source notes for this tab carried a sentence about planned improvements to
unload for validation. It is deliberately absent: it discloses unshipped
roadmap, the Testing tab set that precedent, and a test asserts the rendered
HTML never matches /in the future|we plan to|coming soon|roadmap/i. Section 5
states what is true today and stops.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TopologyCell:
    """One quadrant of the access matrix."""

    unload: bool
    pull: bool
    title: str
    body: str
    efficiency: str


@dataclass(frozen=True)
class Suggestion:
    """One platform-specific recommendation."""

    title: str
    body: str


@dataclass(frozen=True)
class DocLink:
    label: str
    url: str


TAB_LEDE = (
    "This phase moves your data into Snowflake and then proves it arrived intact. "
    "Two access questions decide how the work is deployed, and your own schema "
    "decides which columns need a decision before it starts."
)

STRIP_LABEL = "In scope for this phase"
TILE_TABLES = "Tables"
TILE_VIEWS = "Views"
TILE_TABLES_NOTE = "rows migrate and are compared"
TILE_VIEWS_NOTE = "recreated; validate where consumers read them"
STRIP_POINTER = (
    "Wave order and per-object detail live in <strong>Dependencies</strong> and "
    "<strong>Overview</strong>; this tab stays at the phase level."
)

KNOW_YOUR_DATA_TITLE = "Know your data"
KNOW_YOUR_DATA_LEDE = (
    "Two things decide how long this phase takes and how much of it can be "
    "automated: how much data there is, and which of its types survive the trip "
    "unchanged. The report can read your schema for the second. It cannot read "
    "volume &mdash; no row count or byte size exists anywhere in the assessment "
    "input, which is what the scripts below are for."
)

FINDINGS_TITLE = "Data types requiring attention"
FINDINGS_LEDE = (
    "Types found in your own DDL that change shape on the way over, or that "
    "migrate cleanly and then cannot be fully compared. Everything not listed "
    "here maps cleanly on both sides."
)
FINDINGS_HEADERS = ("Type", "Becomes", "Migration", "Validation", "What to expect")
FINDINGS_USED_IN_HEADER = "Used in"

# {clean} types map cleanly and are not listed.
CLEAN_TYPES_SENTENCE = (
    "{clean} other {noun} in your schema map cleanly on both sides."
)

# {scanned} of {total}; named rather than rounded, because a short count that
# reads as complete is the failure mode this line exists to prevent.
SCAN_COVERAGE_SENTENCE = (
    "Read from the DDL captured for {scanned} of {total} in-scope {noun}. Confirm "
    "against the data type inventory script below, which reads the live catalog "
    "and is the authoritative count."
)

REFERENCE_TABLE_NOTE = (
    "No captured DDL was available to read, so this table is per-platform "
    "reference rather than a finding about your project. Run the data type "
    "inventory script below to see which of these your schema actually uses."
)

SCRIPTS_TITLE = "Volume inventory"
SCRIPTS_LEDE = (
    "Two read-only queries against your source catalog. Neither scans table data "
    "or takes locks. Run them, and the results give you the volume this phase has "
    "to move and the full list of types it has to handle."
)
COPY_LABEL = "Copy"
COPIED_LABEL = "Copied"
DOWNLOAD_LABEL = "Download .sql"

NO_SCRIPTS_TITLE = "What to gather"
NO_SCRIPTS_LEDE = (
    "No reviewed inventory script ships for this source platform yet, so rather "
    "than offer SQL that has not been validated against it, here is what to ask "
    "your DBA for. All of it comes from catalog metadata &mdash; no table scans."
)
NO_SCRIPTS_ITEMS: tuple[str, ...] = (
    "Row count and on-disk size per table, largest first.",
    "Every column data type in scope, with how many columns and tables use each.",
    "Declared length, precision, and scale per type, so widening on the target can be checked.",
    "Partition or distribution layout for the largest tables, which is what extraction parallelizes on.",
)

TOPOLOGY_TITLE = "Deployment topology"
TOPOLOGY_LEDE = (
    "Two questions about access set the shape of this phase, for migration and "
    "validation alike. Answer both to highlight your quadrant; the full matrix "
    "stays readable either way."
)
UNLOAD_QUESTION = (
    "Can the source export a bulk copy of the data to cloud storage &mdash; "
    "UNLOAD, BCP, or the platform equivalent?"
)
PULL_QUESTION = "Can Snowflake reach the source database over the network?"
ANSWER_YES = "Yes"
ANSWER_NO = "No, or not yet"
MATRIX_ROW_LABELS = ("Bulk export available", "No bulk export")
MATRIX_COL_LABELS = ("Snowflake can reach the source", "Snowflake cannot reach the source")
PICKER_RESET = "Clear"

TOPOLOGY_CELLS: tuple[TopologyCell, ...] = (
    TopologyCell(
        unload=True,
        pull=True,
        title="Both routes open",
        body=(
            "Stage a bulk export for the large tables and read the source directly "
            "for the ones where export setup is not worth it. The most room to tune "
            "table by table."
        ),
        efficiency="Fastest overall.",
    ),
    TopologyCell(
        unload=True,
        pull=False,
        title="Bulk export only",
        body=(
            "A worker inside your network writes the export to a stage, and "
            "Snowflake loads from the stage. Snowflake never connects to the source."
        ),
        efficiency="Very efficient &mdash; the export path carries the volume.",
    ),
    TopologyCell(
        unload=False,
        pull=True,
        title="Direct read only",
        body=(
            "A worker Snowflake can reach reads the source over its driver and "
            "writes into Snowflake, table by table."
        ),
        efficiency=(
            "Relatively efficient &mdash; throughput is bounded by the driver "
            "rather than by storage."
        ),
    ),
    TopologyCell(
        unload=False,
        pull=False,
        title="Neither yet",
        body=(
            "A worker inside your network reads the source and pushes to Snowflake "
            "over an authorized egress path. Workable, and the slowest of the four."
        ),
        efficiency=(
            "Slowest &mdash; of the two, securing bulk export buys more than "
            "opening the network."
        ),
    ),
)

WORKER_TITLE = "Where the workers run"
WORKER_OPTIONS: tuple[Suggestion, ...] = (
    Suggestion(
        "Snowpark Container Services",
        "No infrastructure of your own to run, and Snowflake authentication is "
        "provided to the service. Needs the source reachable from Snowflake.",
    ),
    Suggestion(
        "Your own hosts",
        "A laptop, a cloud VM, or an on-premises server, one worker per host. "
        "Puts the worker next to the source, which is what the no-network-access "
        "quadrants need.",
    ),
    Suggestion(
        "Your Kubernetes cluster",
        "Same placement as your own hosts, scaled by replica count instead of by "
        "host count. Both source and Snowflake credentials are supplied explicitly.",
    ),
)

BOTTLENECK_TITLE = "What actually limits throughput"
BOTTLENECKS: tuple[str, ...] = (
    "How fast the source will let you read, which is usually the binding constraint.",
    "How many workers are running, the one lever that scales without new access.",
    "Network egress between the source and wherever the data lands.",
    "Partition size on the widest tables &mdash; too small and the overhead dominates.",
)

VALIDATION_TITLE = "How validation differs"
VALIDATION_BODY: tuple[str, ...] = (
    (
        "The same two questions set the topology for validation, and the answers are "
        "normally the same ones. One thing does not carry over: bulk export does not "
        "shorten validation. Validation compares by running SQL against the live "
        "source, so a table migrated from a staged export is still validated by "
        "querying the source directly."
    ),
    (
        "Two consequences worth planning for. Keep the source reachable for the whole "
        "validation window, not just the migration window &mdash; if a "
        "decommissioning date is already set, validation has to finish before it. And "
        "treat worker count as the lever for how long validation takes, because the "
        "export path is not one."
    ),
    (
        "Views are optional. Their rows are derived from tables you are already "
        "comparing, so validate a view when a downstream consumer reads it directly "
        "and skip it otherwise."
    ),
)

SUGGESTIONS_TITLE = "Suggestions for {dialect}"
SUGGESTIONS: dict[str, tuple[Suggestion, ...]] = {
    "sqlserver": (
        Suggestion(
            "Use BCP where it is installed",
            "On a worker host that has <code>bcp</code> available, enabling it is "
            "materially faster than a driver read. Two caveats to plan for: BCP "
            "writes a NULL <code>DATETIME</code> as the Unix epoch, and it "
            "preserves trailing spaces on <code>CHAR(n)</code> columns.",
        ),
        Suggestion(
            "Avoid blocking busy tables",
            "For tables under constant write load, set the object modifier to "
            "<code>WITH (NOLOCK)</code>. That removes the blocking risk and admits "
            "dirty reads, which can surface later as false validation mismatches.",
        ),
        Suggestion(
            "Partition the largest tables",
            "Name a partitioning column and a partition size for the biggest "
            "tables so extraction runs in parallel instead of streaming one "
            "result set.",
        ),
        Suggestion(
            "State the encryption settings",
            "Set encryption and certificate trust explicitly rather than relying "
            "on driver defaults, which differ by driver version.",
        ),
    ),
    "redshift": (
        Suggestion(
            "Prefer UNLOAD once its prerequisites exist",
            "With S3, the Redshift IAM role, and a Snowflake external stage in "
            "place, UNLOAD is the better path for every table. Keep the direct "
            "read for small tables, or while those prerequisites are pending.",
        ),
        Suggestion(
            "Leave partition sizing on auto",
            "Automatic partition sizing suits most workloads. Raise the target "
            "only for very wide tables, which UNLOAD writes as few large files.",
        ),
        Suggestion(
            "Check the IAM role on both sides",
            "The role needs S3 write access and a trust relationship Redshift can "
            "assume. A role that is right on one side only fails at run time, not "
            "at setup.",
        ),
        Suggestion(
            "Keep the cluster available for validation",
            "Validation queries the live cluster even for tables that were "
            "migrated from an UNLOAD export.",
        ),
    ),
}

READING_TITLE = "Further reading"
_DOCS = "https://docs.snowflake.com/en/migrations/aim-for-datawarehouses/data-migration-validation"
SHARED_LINKS: tuple[DocLink, ...] = (
    DocLink("Data migration &amp; validation overview", f"{_DOCS}/overview"),
    DocLink("Migrating data", f"{_DOCS}/data-migration"),
    DocLink("Validating data", f"{_DOCS}/data-validation"),
    DocLink("Deploying workers", f"{_DOCS}/deploy-workers"),
    DocLink("Glossary", f"{_DOCS}/glossary"),
)
DIALECT_LINKS: dict[str, tuple[DocLink, ...]] = {
    "sqlserver": (
        DocLink("Migrating data from SQL Server", f"{_DOCS}/migrate-sql-server"),
        DocLink("Validating data from SQL Server", f"{_DOCS}/validate-sql-server"),
    ),
    "redshift": (
        DocLink("Migrating data from Amazon Redshift", f"{_DOCS}/migrate-redshift"),
        DocLink("Validating data from Amazon Redshift", f"{_DOCS}/validate-redshift"),
    ),
    "teradata": (
        DocLink("Migrating data from Teradata", f"{_DOCS}/migrate-teradata"),
        DocLink("Validating data from Teradata", f"{_DOCS}/validate-teradata"),
    ),
    "oracle": (
        DocLink("Migrating data from Oracle", f"{_DOCS}/migrate-oracle"),
        DocLink("Validating data from Oracle", f"{_DOCS}/validate-oracle"),
    ),
    "postgres": (
        DocLink("Migrating data from PostgreSQL", f"{_DOCS}/migrate-postgresql"),
        DocLink("Validating data from PostgreSQL", f"{_DOCS}/validate-postgresql"),
    ),
}

# Rendered where a status value needs a human label.
MIGRATION_LABELS = {"supported": "Supported", "unsupported": "Not supported"}
VALIDATION_LABELS = {
    "supported": "Full comparison",
    "schema-only": "Schema only",
    "no-row-comparison": "No row comparison",
    "drift": "Expect small diffs",
    "unsupported": "Not supported",
    "not documented": "Not documented",
}

DIALECT_DISPLAY_NAMES = {
    "sqlserver": "SQL Server",
    "redshift": "Amazon Redshift",
    "teradata": "Teradata",
    "oracle": "Oracle",
    "postgres": "PostgreSQL",
}

SCRIPT_TITLES = {
    "table_inventory": "Table volume",
    "data_type_inventory": "Data types",
}
SCRIPT_NOTES = {
    "table_inventory": "Row count and size per table, largest first.",
    "data_type_inventory": "Every column type in scope, with how widely each is used.",
}
