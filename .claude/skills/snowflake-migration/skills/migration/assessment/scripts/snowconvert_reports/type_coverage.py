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

"""Per-dialect data-type coverage for migration and validation.

Two sources, and they disagree:

* The published platform pages, which are what a customer reads --
  https://docs.snowflake.com/en/migrations/aim-for-datawarehouses/data-migration-validation/migrate-sql-server
  https://docs.snowflake.com/en/migrations/aim-for-datawarehouses/data-migration-validation/validate-sql-server
  https://docs.snowflake.com/en/migrations/aim-for-datawarehouses/data-migration-validation/migrate-redshift
  https://docs.snowflake.com/en/migrations/aim-for-datawarehouses/data-migration-validation/validate-redshift
  All four read 2026-07-30.
* ``dmvf/data-migration-orchestrator/.../type_mappings/``, which is what the
  orchestrator executes.

The rows below follow the docs, so the report never contradicts the page a
customer is reading beside it. Where the two disagree the divergence is named
in ``KNOWN_DMVF_DIVERGENCES``, and the drift guard in
``ai/tests/assessment/data_migration_readiness/test_type_coverage_drift.py``
fails on any divergence not listed there -- and on any source type dmvf gains
that has no row here. The ``validation`` column has no executable counterpart
to guard against (there is no per-dialect DV support matrix), so re-reading the
two ``validate-*`` pages belongs on the DMVF release checklist.
"""

from __future__ import annotations

from dataclasses import dataclass

MIGRATION_SUPPORTED = "supported"
MIGRATION_UNSUPPORTED = "unsupported"

VALIDATION_SUPPORTED = "supported"
VALIDATION_SCHEMA_ONLY = "schema-only"
VALIDATION_NO_ROW_COMPARISON = "no-row-comparison"
VALIDATION_DRIFT = "drift"
VALIDATION_UNSUPPORTED = "unsupported"
# A type the orchestrator maps but no published page covers. Stated rather than
# guessed: claiming "supported" here would be an invention, and claiming
# "unsupported" would be a false alarm.
VALIDATION_UNDOCUMENTED = "not documented"


@dataclass(frozen=True)
class TypeCoverage:
    """What happens to one source type, on both sides of the phase."""

    type_name: str
    snowflake_type: str
    migration: str
    validation: str
    note: str = ""

    @property
    def is_clean(self) -> bool:
        """True when this type needs no decision from the reader.

        A note is disqualifying on its own: ``DECIMAL`` and ``UNIQUEIDENTIFIER``
        are supported on both sides and still change shape in ways no other tab
        surfaces, so a note is the signal that a row has to be read.
        """
        return (
            self.migration == MIGRATION_SUPPORTED
            and self.validation == VALIDATION_SUPPORTED
            and not self.note
        )


_CONTENTS_NEVER_COMPARED = (
    "Migrates intact, but only the column&rsquo;s presence and type are compared "
    "&mdash; never its contents."
)
_NO_ROW_COMPARISON = (
    "Migrates cleanly, then cannot be compared row by row. Plan a separate check "
    "if these columns carry business-critical text."
)
_NO_SNOWFLAKE_EQUIVALENT = "No Snowflake equivalent, so these columns cannot be compared."
_HLLSKETCH_CARDINALITY = (
    "No Snowflake sketch type; stored as <code>HLL_CARDINALITY</code> text "
    "(VARCHAR). Distinct sketches with the same cardinality compare equal."
)
_UNDOCUMENTED = (
    "Migrated by the orchestrator, but not yet covered by the published "
    "type-mapping page. Confirm handling with your migration engineer."
)
_ROWVERSION = (
    "SQL Server <code>TIMESTAMP</code> is a synonym for <code>ROWVERSION</code>, "
    "not a datetime; it migrates as BINARY."
)
_SUB_MICROSECOND = (
    "The 7th fractional-second digit truncates on readback. On high-precision "
    "columns that surfaces as level 2 and 3 differences, which are not data loss."
)
_INTERVAL = "Compared as a native INTERVAL by default; the handling is configurable."
_ORACLE_CHAR_ANTI_CASE = (
    "Snowflake stores CHAR internally as VARCHAR/TEXT; DM aligns the dict "
    "target with runtime rather than SCAI's DDL literal."
)
_ORACLE_RAW_ANTI_CASE = (
    "SCAI drops the size when converting RAW; DM keeps catalog "
    "<code>char_length</code> and emits BINARY(n) because it is strictly more "
    "informative than SCAI's bare BINARY."
)
_ORACLE_BARE_NUMBER = (
    "SCAI emits NUMBER(38,18) for bare NUMBER; DM cannot distinguish bare "
    "NUMBER from NUMBER(*) via catalog and keeps the default helper. Per-column "
    "<code>validationCustomTypeRules</code> is the escape hatch."
)
_ORACLE_DATE_AS_TIMESTAMP = (
    "Oracle DATE carries century/year/month/day/hour/minute/second; Snowflake "
    "DATE drops the time component, so migrations preserve it as TIMESTAMP_NTZ."
)
_ORACLE_FIXED_ROWID_SIZE = (
    "Emits as VARCHAR(18) per SCAI OraSimpleDataTypeReplacer fixed size."
)
_ORACLE_FIXED_UROWID_SIZE = (
    "Emits as VARCHAR(4000) per SCAI (Oracle SQL Reference default width)."
)


def _row(name: str, target: str, validation: str, note: str = "") -> TypeCoverage:
    return TypeCoverage(name, target, MIGRATION_SUPPORTED, validation, note)


_S = VALIDATION_SUPPORTED
_SCHEMA = VALIDATION_SCHEMA_ONLY

_SQLSERVER: tuple[TypeCoverage, ...] = (
    _row("BIT", "NUMBER", _S),
    _row("TINYINT", "NUMBER", _S),
    _row("SMALLINT", "NUMBER", _S),
    _row("INT", "NUMBER", _S),
    _row("BIGINT", "NUMBER", _S),
    _row("DECIMAL", "NUMBER", _S),
    _row("NUMERIC", "NUMBER", _S),
    _row("MONEY", "NUMBER", _S),
    _row("SMALLMONEY", "NUMBER", _S),
    _row("FLOAT", "FLOAT", _S),
    _row("REAL", "FLOAT", _S),
    _row("CHAR", "VARCHAR", _S),
    _row("VARCHAR", "VARCHAR", _S),
    _row("NCHAR", "VARCHAR", _S, "Row comparison applies TRIM when the target is VARCHAR."),
    _row("NVARCHAR", "VARCHAR", _S),
    _row("SYSNAME", "VARCHAR", _S),
    _row("TEXT", "VARCHAR", VALIDATION_NO_ROW_COMPARISON, _NO_ROW_COMPARISON),
    _row("NTEXT", "VARCHAR", VALIDATION_NO_ROW_COMPARISON, _NO_ROW_COMPARISON),
    _row("DATE", "DATE", _S),
    _row("TIME", "TIME", _S),
    _row("DATETIME", "TIMESTAMP_NTZ", _S),
    _row("SMALLDATETIME", "TIMESTAMP_NTZ", _S),
    _row("DATETIME2", "TIMESTAMP_NTZ", VALIDATION_DRIFT, _SUB_MICROSECOND),
    _row("DATETIMEOFFSET", "TIMESTAMP_TZ", VALIDATION_DRIFT, _SUB_MICROSECOND),
    _row("BINARY", "BINARY", _S),
    _row("VARBINARY", "BINARY", _S),
    _row("IMAGE", "BINARY", _S),
    _row("TIMESTAMP", "BINARY", _S, _ROWVERSION),
    _row("ROWVERSION", "BINARY", _S, _ROWVERSION),
    _row("UNIQUEIDENTIFIER", "VARCHAR", _S,
         "Stored as an uppercase UUID string, so case-sensitive joins on it need review."),
    _row("HIERARCHYID", "VARCHAR", _S, "Stored as its hierarchy path string."),
    _row("XML", "VARIANT", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("SQL_VARIANT", "VARIANT", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("GEOGRAPHY", "GEOGRAPHY", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("GEOMETRY", "GEOGRAPHY", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("JSON", "VARIANT", VALIDATION_UNDOCUMENTED, _UNDOCUMENTED),
    _row("VECTOR", "VECTOR", VALIDATION_UNDOCUMENTED, _UNDOCUMENTED),
)

_REDSHIFT: tuple[TypeCoverage, ...] = (
    _row("SMALLINT", "NUMBER", _S),
    _row("INT2", "NUMBER", _S),
    _row("INTEGER", "NUMBER", _S),
    _row("INT", "NUMBER", _S),
    _row("INT4", "NUMBER", _S),
    _row("BIGINT", "NUMBER", _S),
    _row("INT8", "NUMBER", _S),
    _row("DECIMAL", "NUMBER", _S),
    _row("NUMERIC", "NUMBER", _S),
    _row("REAL", "FLOAT", _S),
    _row("FLOAT4", "FLOAT", _S),
    _row("FLOAT", "FLOAT", _S),
    _row("FLOAT8", "FLOAT", _S),
    _row("DOUBLE PRECISION", "FLOAT", _S),
    _row("BOOLEAN", "BOOLEAN", _S),
    _row("BOOL", "BOOLEAN", _S),
    _row("CHAR", "VARCHAR", _S),
    _row("CHARACTER", "VARCHAR", _S),
    _row("NCHAR", "VARCHAR", _S),
    _row("BPCHAR", "VARCHAR", _S),
    _row("VARCHAR", "VARCHAR", _S),
    _row("CHARACTER VARYING", "VARCHAR", _S),
    _row("NVARCHAR", "VARCHAR", _S),
    _row("TEXT", "VARCHAR", _S),
    _row("DATE", "DATE", _S),
    _row("TIMESTAMP", "TIMESTAMP_NTZ", _S),
    _row("TIMESTAMP WITHOUT TIME ZONE", "TIMESTAMP_NTZ", _S),
    _row("TIMESTAMPTZ", "TIMESTAMP_TZ", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("TIMESTAMP WITH TIME ZONE", "TIMESTAMP_TZ", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("TIME", "TIME", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("TIME WITHOUT TIME ZONE", "TIME", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("TIMETZ", "TIME", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("TIME WITH TIME ZONE", "TIME", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("INTERVALY2M", "INTERVAL", _S, _INTERVAL),
    _row("INTERVAL YEAR TO MONTH", "INTERVAL", _S, _INTERVAL),
    _row("INTERVALD2S", "INTERVAL", _S, _INTERVAL),
    _row("INTERVAL DAY TO SECOND", "INTERVAL", _S, _INTERVAL),
    _row("VARBYTE", "BINARY", _S),
    _row("VARBINARY", "BINARY", _S),
    _row("BINARY VARYING", "BINARY", _S),
    _row("SUPER", "VARIANT", VALIDATION_UNSUPPORTED, _NO_SNOWFLAKE_EQUIVALENT),
    _row("GEOMETRY", "GEOGRAPHY", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("GEOGRAPHY", "GEOGRAPHY", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("OID", "NUMBER", VALIDATION_UNDOCUMENTED, _UNDOCUMENTED),
    _row("HLLSKETCH", "VARCHAR", _S, _HLLSKETCH_CARDINALITY),
)

_ORACLE: tuple[TypeCoverage, ...] = (
    _row("NUMBER", "NUMBER", _S, _ORACLE_BARE_NUMBER),
    _row("INTEGER", "NUMBER", _S),
    _row("INT", "NUMBER", _S),
    _row("SMALLINT", "NUMBER", _S),
    _row("DECIMAL", "NUMBER", _S),
    _row("NUMERIC", "NUMBER", _S),
    _row("FLOAT", "FLOAT", _S),
    _row("REAL", "FLOAT", _S),
    _row("BINARY_FLOAT", "FLOAT", _S),
    _row("BINARY_DOUBLE", "FLOAT", _S),
    _row("CHAR", "VARCHAR", _S, _ORACLE_CHAR_ANTI_CASE),
    _row("VARCHAR", "VARCHAR", _S),
    _row("VARCHAR2", "VARCHAR", _S),
    _row("NCHAR", "VARCHAR", _S),
    _row("NVARCHAR2", "VARCHAR", _S),
    _row("CLOB", "VARCHAR", _S),
    _row("NCLOB", "VARCHAR", _S),
    _row("LONG", "VARCHAR", _S),
    _row("RAW", "BINARY", _S, _ORACLE_RAW_ANTI_CASE),
    _row("LONG RAW", "BINARY", _S),
    _row("BLOB", "BINARY", _S),
    _row("BFILE", "VARCHAR", _S),
    _row("ROWID", "VARCHAR", _S, _ORACLE_FIXED_ROWID_SIZE),
    _row("UROWID", "VARCHAR", _S, _ORACLE_FIXED_UROWID_SIZE),
    _row("DATE", "TIMESTAMP_NTZ", _S, _ORACLE_DATE_AS_TIMESTAMP),
    _row("TIMESTAMP", "TIMESTAMP_NTZ", _S),
    _row("TIMESTAMP WITH TIME ZONE", "TIMESTAMP_TZ", _S),
    _row("TIMESTAMP WITH LOCAL TIME ZONE", "TIMESTAMP_LTZ", _S),
    _row("INTERVAL YEAR TO MONTH", "INTERVAL", _S, _INTERVAL),
    _row("INTERVAL DAY TO SECOND", "INTERVAL", _S, _INTERVAL),
    _row("BOOLEAN", "BOOLEAN", _S),
    _row("BOOL", "BOOLEAN", _S),
    _row("JSON", "VARIANT", _S),
    _row("XMLTYPE", "VARIANT", _S),
    _row("SDO_GEOMETRY", "GEOGRAPHY", _SCHEMA, _CONTENTS_NEVER_COMPARED),
    _row("VECTOR", "VECTOR", VALIDATION_UNDOCUMENTED, _UNDOCUMENTED),
)

_AZURE_SYNAPSE: tuple[TypeCoverage, ...] = (
    _row("BIT", "BOOLEAN", _S),
    _row("TINYINT", "NUMBER", _S),
    _row("SMALLINT", "NUMBER", _S),
    _row("INT", "NUMBER", _S),
    _row("BIGINT", "NUMBER", _S),
    _row("DECIMAL", "NUMBER", _S),
    _row("NUMERIC", "NUMBER", _S),
    _row("MONEY", "NUMBER", _S),
    _row("SMALLMONEY", "NUMBER", _S),
    _row("FLOAT", "FLOAT", _S),
    _row("REAL", "FLOAT", _S),
    _row("CHAR", "VARCHAR", _S),
    _row("VARCHAR", "VARCHAR", _S),
    _row("NCHAR", "VARCHAR", _S, "Row comparison applies TRIM when the target is VARCHAR."),
    _row("NVARCHAR", "VARCHAR", _S),
    _row("SYSNAME", "VARCHAR", _S),
    _row("DATE", "DATE", _S),
    _row("TIME", "TIME", _S),
    _row("DATETIME", "TIMESTAMP_NTZ", _S),
    _row("SMALLDATETIME", "TIMESTAMP_NTZ", _S),
    _row("DATETIME2", "TIMESTAMP_NTZ", VALIDATION_DRIFT, _SUB_MICROSECOND),
    _row("DATETIMEOFFSET", "TIMESTAMP_TZ", VALIDATION_DRIFT, _SUB_MICROSECOND),
    _row("BINARY", "BINARY", _S),
    _row("VARBINARY", "BINARY", _S),
    _row("UNIQUEIDENTIFIER", "VARCHAR", _S,
         "Stored as an uppercase UUID string, so case-sensitive joins on it need review."),
)


COVERAGE: dict[str, tuple[TypeCoverage, ...]] = {
    "sqlserver": _SQLSERVER,
    "redshift": _REDSHIFT,
    "oracle": _ORACLE,
    "azure_synapse": _AZURE_SYNAPSE,
}

# The rows where the published page and the shipped orchestrator disagree.
# Recorded rather than reconciled: the report follows the docs, and the drift
# guard fails on a new unrecorded mismatch.
KNOWN_DMVF_DIVERGENCES: dict[tuple[str, str], str] = {
    ("sqlserver", "BIT"): "docs NUMBER; orchestrator BOOLEAN",
    ("sqlserver", "GEOMETRY"): "docs GEOGRAPHY; orchestrator GEOMETRY",
    ("redshift", "GEOMETRY"): "docs GEOGRAPHY; orchestrator GEOMETRY",
    ("redshift", "TIMETZ"): "docs TIME; orchestrator TIMESTAMP_TZ",
    ("redshift", "TIME WITH TIME ZONE"): "docs TIME; orchestrator TIMESTAMP_TZ",
}


def coverage_for(dialect_key: str) -> tuple[TypeCoverage, ...]:
    """Coverage rows for *dialect_key*, empty for a dialect with no snapshot."""
    return COVERAGE.get(dialect_key, ())
