# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Load and render versioned migration effort-estimate artifacts."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

_HOURS_PER_WORK_DAY = 8.0

# Shares the ``.nav-preview-badge`` CSS class defined in generate_multi_report.py's
# stylesheet (embedded in the same HTML page) so the badge markup is defined once.
EFFORT_PREVIEW_BADGE_HTML = '<span class="nav-preview-badge">Preview</span>'

_OVERRIDES_INFO_ICON = (
    '<span class="info-icon" style="margin-left:4px;">i<span class="tooltip">'
    "An override is one rate you have changed. Snowflake's own figure is kept alongside it, "
    "so every total can be compared against the unedited estimate — and a single override "
    "can be cleared by emptying its cell."
    "</span></span>"
)

EFFORT_DISCLAIMER_HTML = (
    '<p style="color: #0369A1; background: #F0F9FF; border: 1px solid #BAE6FD; '
    'border-radius: 8px; padding: 12px 14px; font-size: 0.88rem; line-height: 1.5; '
    'margin-bottom: 20px;">'
    "<strong>Disclaimer:</strong> These estimates are a best-effort recommendation only. "
    "Actual effort may vary based on project scope, team experience, data quality, "
    "and migration complexity."
    "</p>"
)
_DDL_EXCLUDED_DISPLAY_TYPES = frozenset({"Index", "Flow Control"})

# Rendered wherever an hour figure is absent because the work has no estimation
# approach yet, matching the fixed-budget tooltip's own N/A cells.
_NOT_APPLICABLE = "N/A"

# Complexity bands, worst first — the order the .NET calculator, the FDE workbook
# and this report all list them in. ``Redesign`` carries a rate but no objects
# are classified into it, so only the first four are shown and edited.
_BANDS = ("critical", "high", "medium", "low")
_BAND_LABELS = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}


@dataclass
class CalculatorRow:
    """One calculator line item, mirroring the .NET record it is rehydrated from.

    A row is priced one of two ways, readable from its fields. A *banded* row
    prices counted objects and carries ``band_counts`` plus ``band_rates``; a
    *flat* row is one budget for the whole line and carries ``flat_hours``.
    """

    # Stable config key, unique per row: how an override addresses a row without
    # matching a display label. ``bucket`` is the roll-up class and ``ddl_type``
    # the DDL summary entry the row prices, or None when it prices no single type.
    key: str
    bucket: str
    ddl_type: Optional[str]
    component: str
    object_type: str
    quantity: Any
    # ``None`` on a flat row; a mapping of band name to objects / hours otherwise.
    band_counts: Optional[Dict[str, Any]]
    band_rates: Optional[Dict[str, float]]
    # ``None`` on a banded row, and on a flat row Snowflake publishes no figure
    # for. The latter renders as N/A and contributes nothing to the totals until
    # the user enters their own budget, which they may: declining to price a line
    # is a statement about our estimate, not a restriction on theirs.
    flat_hours: Optional[float]
    estimated_hours: Optional[float]
    manual_rewrite_hours: Optional[float]
    automation_pct: Optional[float]
    comments: str = ""


def load_effort_assessment(path: Path) -> Optional[Dict[str, Any]]:
    """Load an effort artifact and rehydrate its calculator rows for HTML renderers."""
    try:
        with Path(path).open(encoding="utf-8") as stream:
            assessment = json.load(stream)
        assessment["calculator_rows"] = [
            CalculatorRow(**row) for row in assessment.get("calculator_rows") or []
        ]
        return assessment
    except (OSError, json.JSONDecodeError, TypeError, ValueError, AttributeError) as exc:
        print(f"Warning: Could not load effort estimates data: {exc}", file=sys.stderr)
        return None


# The Effort tab's whole Vue surface, as a mixin the root app pulls in. It lives
# in a plain string rather than inside generate_multi_report.py's f-string
# template so no `{{ }}` needs brace-doubling — the one place a mistake here
# would be invisible until the report renders.
EFFORT_MIXIN_JS = r"""
(function () {
  "use strict";

  const baseline = window.__EFFORT_BASELINE__ || null;
  const shared = globalThis.EffortOverrides || null;
  if (!baseline || !shared) {
    window.__EFFORT_MIXIN__ = null;
    return;
  }

  // Edits stay in memory; download is the only way to persist. The file on disk
  // is the single source of truth shared with the dashboard.
  const stored = shared.parseOverrides(window.__EFFORT_OVERRIDES__ || {});

  /**
   * One 16x16 stroked glyph. Inline because the report is a single file opened over
   * file://, where an icon font or a sprite sheet cannot be fetched. Rendered with
   * v-html from a computed, so the markup is built here rather than in a template
   * attribute where its quotes would have to be escaped.
   */
  function _svg(path) {
    return (
      '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" ' +
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" ' +
      'stroke-linejoin="round"><path d="' + path + '"/></svg>'
    );
  }

  window.__EFFORT_MIXIN__ = {
    data() {
      const loaded = shared.countEntries(stored);
      return {
        // Rate overrides are keyed (row key -> band -> hours); a flat row's whole
        // budget is one number, so the two live in separate maps exactly as the
        // overrides file stores them.
        effortRateOverrides: Object.assign({}, stored.band_rates),
        effortFlatOverrides: Object.assign({}, stored.flat_hours),
        effortDrafts: {},
        effortErrors: {},
        effortNotice: stored.discarded
          ? "The saved overrides were written by an older effort model" +
            (stored.discarded_version === null ? "" : " (schema " + stored.discarded_version + ")") +
            ", so their rates cannot be applied and need re-entering."
          : loaded > 0 ? loaded + " override(s) loaded from file." : "",
        // Collapse state is view state, not arithmetic, so unlike the override maths
        // it is not shared with the dashboard. A key present and true means closed,
        // so sections start open without having to enumerate them. Not persisted.
        effortCollapsed: {},
        effortMenuOpen: false,
      };
    },
    computed: {
      effortChevronDown() {
        return _svg('M4 6.5 8 10.5l4-4');
      },
      effortChevronRight() {
        return _svg('M6.5 4 10.5 8l-4 4');
      },
      effortIconDownload() {
        return _svg('M8 2.5v6.5M5.2 6.7 8 9.5l2.8-2.8M3 12.5h10');
      },
      effortIconUpload() {
        return _svg('M8 9.5V3M5.2 5.8 8 3l2.8 2.8M3 12.5h10');
      },
      effortIconReset() {
        return _svg('M3.5 7.5h5.5a2.75 2.75 0 1 1 0 5.5H6M3.5 7.5 6 5M3.5 7.5 6 10');
      },
      effortBands() {
        return shared.EDITABLE_BANDS;
      },
      effortApplied() {
        return shared.applyOverrides(
          baseline.calculator_rows,
          this.effortRateOverrides,
          this.effortFlatOverrides,
        );
      },
      effortRollup() {
        return shared.rollUp(
          this.effortApplied,
          baseline.summary,
          this.effortRateOverrides,
          this.effortFlatOverrides,
        );
      },
      // Grouping and its subtotals come from the shared module, not from this
      // template, so the report and the dashboard cannot disagree about one.
      effortSections() {
        return shared.groupSections(this.effortApplied, baseline.summary, this.effortRollup);
      },
      // Component, object type, quantity, one per band, hours, comments. Derived so
      // a new band cannot leave a spanning cell one column short.
      effortColumnCount() {
        return 5 + this.effortBands.length;
      },
      effortHasOverrides() {
        return this.effortRollup.overridden_count > 0;
      },
      effortTotalChanged() {
        return this.effortRollup.custom.total !== this.effortRollup.sf.total;
      },
      effortCodeChanged() {
        return this.effortRollup.custom.code !== this.effortRollup.sf.code;
      },
      effortTestingChanged() {
        return this.effortRollup.custom.testing !== this.effortRollup.sf.testing;
      },
      effortFixedBudgetChanged() {
        return this.effortRollup.custom.fixed_budget !== this.effortRollup.sf.fixed_budget;
      },
      effortStaleKeys() {
        return this.effortRollup.stale_keys;
      },
      effortSummary() {
        return baseline.summary || {};
      },
    },
    methods: {
      effortHours(value) {
        if (typeof value !== "number" || !isFinite(value)) return "N/A";
        return value.toLocaleString(undefined, {
          minimumFractionDigits: 1,
          maximumFractionDigits: 1,
        });
      },
      effortHoursOrNa(value) {
        return value === null || value === undefined ? "N/A" : this.effortHours(value);
      },
      effortCompact(value) {
        return value === null || value === undefined ? "N/A" : String(value);
      },
      effortDaysLabel(hours) {
        const days = shared.hoursToDays(hours);
        return days.toLocaleString() + (days === 1 ? " day" : " days");
      },
      effortPercent(fraction) {
        const value = typeof fraction === "number" && isFinite(fraction) ? fraction : 0;
        return (value * 100).toFixed(1) + "%";
      },
      effortCount(value) {
        return typeof value === "number" ? value.toLocaleString() : "0";
      },
      effortQuantity(quantity) {
        return typeof quantity === "number" ? quantity.toLocaleString() : quantity;
      },
      effortBandLabel(band) {
        return band.charAt(0).toUpperCase() + band.slice(1);
      },
      effortBandCount(row, band) {
        return row.band_counts ? row.band_counts[band] || 0 : 0;
      },
      effortBandRate(row, band) {
        return row.custom_band_rates ? row.custom_band_rates[band] : null;
      },
      effortSfBandRate(row, band) {
        return row.band_rates ? row.band_rates[band] : null;
      },
      /** Whether one band's rate differs from Snowflake's. Per cell, not per row:
       *  editing Critical must not annotate High, Medium and Low, which still hold
       *  Snowflake's own rates. */
      effortMenuPick(action) {
        this.effortMenuOpen = false;
        if (action === 'download') {
          this.effortDownload();
        } else if (action === 'reset') {
          this.effortResetAll();
        }
      },
      effortResetSubLabel() {
        return this.effortHasOverrides
          ? 'Clears every override and returns to the published estimate'
          : 'Nothing to reset — every rate is already Snowflake\u2019s';
      },
      effortSectionOpen(section) {
        // Read, do not probe -- see applyOverrides in effort_overrides.js.
        return this.effortCollapsed[section.key] !== true;
      },
      effortToggleSection(section) {
        // Replace the map rather than mutating it: a new object is what a computed
        // reading it re-runs on.
        const next = Object.assign({}, this.effortCollapsed);
        next[section.key] = this.effortCollapsed[section.key] !== true;
        this.effortCollapsed = next;
      },
      effortBandChanged(row, band) {
        const bands = row.overridden_bands || [];
        return bands.indexOf(band) >= 0;
      },
      /** Identifies one editable cell: a band of a banded row, or a flat row's budget. */
      effortCellKey(row, band) {
        return band ? row.key + "|" + band : row.key;
      },
      effortInputValue(row, band) {
        // Read, do not probe: a hasOwnProperty check is not tracked by Vue's
        // reactive proxy. See applyOverrides in effort_overrides.js. A blank
        // draft is "", which stays distinct from an absent one.
        const draft = this.effortDrafts[this.effortCellKey(row, band)];
        if (draft !== undefined) {
          return draft;
        }
        const value = band ? this.effortBandRate(row, band) : row.custom_flat_hours;
        return value === null || value === undefined ? "" : String(value);
      },
      effortOnInput(row, band, raw) {
        // The draft is exactly what the user typed, so re-rendering never moves
        // the caret; only a valid value reaches the override map.
        const cell = this.effortCellKey(row, band);
        this.effortDrafts[cell] = raw;
        const checked = shared.validateRateInput(raw);
        if (!checked.ok) {
          this.effortErrors[cell] = checked.error;
          return;
        }
        delete this.effortErrors[cell];
        // Typing Snowflake's own number back clears the cell instead of storing an
        // override that prices identically, which would still count toward the
        // badge and still ride along in a downloaded file.
        const stored = shared.overrideToStore(row, band, checked.value);
        if (band) {
          this.effortSetRate(row.key, band, stored);
        } else if (stored === null) {
          delete this.effortFlatOverrides[row.key];
        } else {
          this.effortFlatOverrides[row.key] = stored;
        }
      },
      effortSetRate(key, band, value) {
        // Replace the card rather than mutating it in place: a new object is what
        // makes the computed re-run, and dropping an emptied card keeps the
        // downloaded file free of rows the user has cleared.
        const card = Object.assign({}, this.effortRateOverrides[key]);
        if (value === null) {
          delete card[band];
        } else {
          card[band] = value;
        }
        if (Object.keys(card).length === 0) {
          delete this.effortRateOverrides[key];
        } else {
          this.effortRateOverrides[key] = card;
        }
      },
      effortOnBlur(row, band) {
        const cell = this.effortCellKey(row, band);
        if (this.effortErrors[cell]) return;
        delete this.effortDrafts[cell];
      },
      effortCellError(row, band) {
        return this.effortErrors[this.effortCellKey(row, band)];
      },
      effortSubtotalChanged(section) {
        return section.subtotal.custom !== section.subtotal.sf;
      },
      /** "Views", "Views or Tables", "Views, Tables or Indexes". */
      effortZeroNote(types) {
        const list = Array.isArray(types) ? types : [];
        if (list.length <= 1) return list[0] || "";
        return list.slice(0, -1).join(", ") + " or " + list[list.length - 1];
      },
      effortDdlTableTotalChanged(types) {
        return this.effortDdlTableTotal(types) !== this.effortDdlTableTotalSf(types);
      },
      effortDdlTableTotal(types) {
        const rollup = this.effortRollup;
        const listed = (Array.isArray(types) ? types : []).reduce((sum, type) => {
          const entry = rollup.ddl_by_type[type];
          return sum + (entry ? entry.custom : 0);
        }, 0);
        return listed + rollup.custom.testing;
      },
      effortDdlTableTotalSf(types) {
        const rollup = this.effortRollup;
        const listed = (Array.isArray(types) ? types : []).reduce((sum, type) => {
          const entry = rollup.ddl_by_type[type];
          return sum + (entry ? entry.sf : 0);
        }, 0);
        return listed + rollup.sf.testing;
      },
      effortDdlCell(type) {
        const entry = this.effortRollup.ddl_by_type[type];
        if (!entry) return { custom: 0, sf: 0, changed: false };
        return {
          custom: entry.custom,
          sf: entry.sf,
          changed: entry.custom !== entry.sf,
        };
      },
      effortResetAll() {
        this.effortRateOverrides = {};
        this.effortFlatOverrides = {};
        this.effortDrafts = {};
        this.effortErrors = {};
        this.effortNotice = "";
      },

      effortDownload() {
        const payload = shared.serializeOverrides(
          this.effortRateOverrides,
          this.effortFlatOverrides,
          { artifact: baseline.artifact, source_dialect: baseline.source_dialect },
          new Date().toISOString(),
        );
        const blob = new Blob([JSON.stringify(payload, null, 2) + "\n"], {
          type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "effort-overrides.json";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      },
      effortLoadFile(event) {
        this.effortMenuOpen = false;
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          const parsed = shared.parseOverrides(String(reader.result));
          if (parsed.discarded) {
            const version = parsed.discarded_version;
            this.effortNotice =
              file.name +
              " was written by an older effort model" +
              (version === null ? "" : " (schema " + version + ")") +
              ", so its rates cannot be applied and need re-entering.";
            return;
          }
          const count = shared.countEntries(parsed);
          this.effortRateOverrides = Object.assign({}, parsed.band_rates);
          this.effortFlatOverrides = Object.assign({}, parsed.flat_hours);
          this.effortDrafts = {};
          this.effortErrors = {};
          this.effortNotice =
            count === 0
              ? file.name + " carried no overrides, so every figure is Snowflake's again."
              : "Loaded " +
                count +
                " override(s) from " +
                file.name +
                ", replacing what was here.";
        };
        reader.readAsText(file);
        event.target.value = "";
      },
    },
  };
})();
"""

# Every block below is a plain (non-f) string, interpolated whole into the
# renderers' f-strings. f-string interpolation runs once, so Vue's `{{ }}` inside
# these constants is never parsed as a replacement field and needs no doubling —
# which is where a silent brace mistake would otherwise land.

_EFFORT_KPI_CARDS_HTML = """
        <div class="effort-cards">
            <div class="effort-card">
                <div class="effort-card-num">{{ effortCount(effortSummary.ddl_objects) }}</div>
                <div class="effort-card-lbl">Total DDL Objects</div>
            </div>
            <div class="effort-card">
                <div class="effort-card-num">{{ effortPercent(effortSummary.ddl_auto_pct) }}</div>
                <div class="effort-card-lbl">DDL Auto-Converted</div>
            </div>
            <div class="effort-card">
                <div class="effort-card-num">{{ effortHours(effortRollup.custom.total) }} h</div>
                <div class="effort-card-lbl">Total Effort</div>
                <div v-if="effortTotalChanged" class="effort-sf-note">Snowflake: {{ effortHours(effortRollup.sf.total) }} h</div>
            </div>
            <div class="effort-card">
                <div class="effort-card-num">{{ effortHours(effortRollup.custom.code) }} h</div>
                <div class="effort-card-lbl">Code Conversion Effort</div>
                <div v-if="effortCodeChanged" class="effort-sf-note">Snowflake: {{ effortHours(effortRollup.sf.code) }} h</div>
            </div>
        </div>
"""

_EFFORT_BAND_LEGEND_HTML = """
        <div class="effort-band-legend">
            <span class="effort-band-legend-lead">Every object is counted in exactly one complexity band:</span>
            <span><strong>Critical</strong> — a critical finding, or SnowConvert could not convert it</span>
            <span><strong>High</strong> — a high-severity finding, or a partial conversion</span>
            <span><strong>Medium</strong> — converted, with medium-severity findings</span>
            <span><strong>Low</strong> — converted clean, or minor findings only</span>
        </div>
"""

_EFFORT_TOOLBAR_HTML = """
        <div class="effort-toolbar">
            <div class="effort-menu-wrap">
                <button type="button" class="effort-btn effort-menu-btn"
                        :aria-expanded="effortMenuOpen ? 'true' : 'false'"
                        @click="effortMenuOpen = !effortMenuOpen">
                    Overrides
                    <span class="effort-chevron" aria-hidden="true" v-html="effortChevronDown"></span>
                </button>
                <!-- A backdrop closes the menu on any outside click, so the mixin needs
                     no document-level listener and no lifecycle hook of its own. -->
                <div v-if="effortMenuOpen" class="effort-menu-backdrop" @click="effortMenuOpen = false"></div>
                <div v-if="effortMenuOpen" class="effort-menu" role="menu">
                    <button type="button" class="effort-menu-item" role="menuitem"
                            @click="effortMenuPick('download')">
                        <span class="effort-menu-icon" aria-hidden="true" v-html="effortIconDownload"></span>
                        <span class="effort-menu-text">
                            <span class="effort-menu-label">Download a copy</span>
                            <span class="effort-menu-sub">Keeps your rates in a file you can hand to someone else</span>
                        </span>
                    </button>
                    <label class="effort-menu-item" role="menuitem">
                        <span class="effort-menu-icon" aria-hidden="true" v-html="effortIconUpload"></span>
                        <span class="effort-menu-text">
                            <span class="effort-menu-label">Load from a file</span>
                            <span class="effort-menu-sub">Replaces the rates on this page with the ones in the file</span>
                        </span>
                        <input type="file" accept="application/json,.json" @change="effortLoadFile" hidden>
                    </label>
                    <button type="button" class="effort-menu-item effort-menu-danger" role="menuitem"
                            :disabled="!effortHasOverrides" @click="effortMenuPick('reset')">
                        <span class="effort-menu-icon" aria-hidden="true" v-html="effortIconReset"></span>
                        <span class="effort-menu-text">
                            <span class="effort-menu-label">Reset all to Snowflake's</span>
                            <span class="effort-menu-sub">{{ effortResetSubLabel() }}</span>
                        </span>
                    </button>
                </div>
            </div>
            <span v-if="effortHasOverrides" class="effort-badge">
                {{ effortRollup.overridden_count }} applied
            </span>
        </div>
        <p v-if="effortNotice" class="effort-notice">{{ effortNotice }}</p>
        <p v-if="effortStaleKeys.length" class="effort-warning">
            {{ effortStaleKeys.length }} override(s) no longer match this assessment and are
            being ignored: {{ effortStaleKeys.join(', ') }}
        </p>
"""

# Rows are grouped into three sections, each with its own subtotal: code
# conversion, unit testing, and the flat budgets. In the first two, each object
# type occupies two table rows — the band object counts, then the editable
# hours-per-object beneath each count. Reading down a column gives `count x rate`,
# and the row total is the sum across the four columns: the same shape, and the
# same arithmetic, as the FDE workbook's Scope Input sheet.
#
# The third section has no complexity dimension, so it restates the column headers
# rather than stretching one budget under Critical / High / Medium / Low. Its
# subtotal is the grand total less the other two, so the three always add up even
# when the summary counts a flat budget that no calculator row carries.
_EFFORT_CALCULATOR_TABLE_HTML = """
        <div class="effort-table-wrap">
            <table class="effort-table">
                <thead>
                    <tr>
                        <th rowspan="2">Migration Component</th>
                        <th rowspan="2">Object Type</th>
                        <th class="num" rowspan="2">Objects</th>
                        <th class="ctr" :colspan="effortBands.length">Objects by complexity · hours per object</th>
                        <th class="num" rowspan="2">Est. Hours</th>
                        <th rowspan="2">Comments</th>
                    </tr>
                    <tr>
                        <th class="num" v-for="band in effortBands" :key="band">{{ effortBandLabel(band) }}</th>
                    </tr>
                </thead>
                <tbody>
                  <template v-for="section in effortSections" :key="section.key">
                    <!-- The subtotal sits in the header rather than under the rows, so
                         collapsing a section never hides the figure it reports. -->
                    <tr>
                        <th class="effort-section" :colspan="effortColumnCount" scope="colgroup">
                            <button type="button" class="effort-section-toggle"
                                    :aria-expanded="effortSectionOpen(section) ? 'true' : 'false'"
                                    @click="effortToggleSection(section)">
                                <span class="effort-chevron" aria-hidden="true"
                                      v-html="effortSectionOpen(section) ? effortChevronDown : effortChevronRight"></span>
                                <span>{{ section.title }}</span>
                                <span class="effort-section-blurb">{{ section.blurb }}</span>
                                <span class="effort-section-total">
                                    {{ effortHours(section.subtotal.custom) }} h
                                    <span v-if="effortSubtotalChanged(section)" class="effort-sf-note">Snowflake: {{ effortHours(section.subtotal.sf) }}</span>
                                </span>
                            </button>
                        </th>
                    </tr>
                    <tr v-if="effortSectionOpen(section) &amp;&amp; section.shape === 'flat'">
                        <th class="effort-subhead">Migration Component</th>
                        <th class="effort-subhead">Line Item</th>
                        <th class="effort-subhead num">Basis</th>
                        <th class="effort-subhead num" :colspan="effortBands.length">Budget (hours)</th>
                        <th class="effort-subhead num">Est. Hours</th>
                        <th class="effort-subhead">Comments</th>
                    </tr>
                    <template v-for="row in section.rows" :key="row.key">
                        <tr v-if="effortSectionOpen(section)" :class="{'effort-row-overridden': row.is_overridden}">
                            <td :rowspan="row.band_counts ? 2 : 1">{{ row.component }}</td>
                            <td :rowspan="row.band_counts ? 2 : 1">{{ row.object_type }}</td>
                            <td class="num">{{ effortQuantity(row.quantity) }}</td>
                            <template v-if="row.band_counts">
                                <td class="num" v-for="band in effortBands" :key="band">
                                    {{ effortCount(effortBandCount(row, band)) }}
                                </td>
                            </template>
                            <td v-else class="num" :colspan="effortBands.length">
                                <input type="text" inputmode="decimal" class="effort-input"
                                       :class="{'effort-input-error': effortCellError(row, null)}"
                                       :value="effortInputValue(row, null)"
                                       :disabled="!row.is_editable"
                                       :aria-label="'Budget hours for ' + row.component + ' ' + row.object_type"
                                       :title="row.is_unestimated ? 'Snowflake publishes no figure for this line — enter your own budget' : 'Enter your own budget for this line'"
                                       @input="effortOnInput(row, null, $event.target.value)"
                                       @blur="effortOnBlur(row, null)">
                                <span v-if="effortCellError(row, null)" class="effort-error">{{ effortCellError(row, null) }}</span>
                                <span v-else-if="row.is_unestimated" class="effort-sf-note">Snowflake: not estimated</span>
                                <span v-else-if="row.is_overridden" class="effort-sf-note">Snowflake: {{ effortCompact(row.flat_hours) }}</span>
                            </td>
                            <td class="num" style="font-weight:600;" :rowspan="row.band_counts ? 2 : 1">
                                {{ effortHoursOrNa(row.custom_estimated_hours) }}
                                <!-- Suppressed on an unpriced line: this note could only ever read
                                     "Snowflake: N/A", which the input's own note already said better. -->
                                <span v-if="row.is_overridden &amp;&amp; !row.is_unestimated" class="effort-sf-note">Snowflake: {{ effortHoursOrNa(row.estimated_hours) }}</span>
                            </td>
                            <td style="color:#64748B;font-size:0.85rem;" :rowspan="row.band_counts ? 2 : 1">
                                {{ row.comments }}
                                <span v-if="row.automation_pct !== null" class="effort-sf-note">{{ effortPercent(row.automation_pct) }} auto-converted</span>
                            </td>
                        </tr>
                        <tr v-if="effortSectionOpen(section) &amp;&amp; row.band_counts" class="effort-rate-row"
                            :class="{'effort-row-overridden': row.is_overridden}">
                            <td class="num effort-rate-lbl">h / object</td>
                            <td class="num" v-for="band in effortBands" :key="band">
                                <input type="text" inputmode="decimal" class="effort-input"
                                       :class="{'effort-input-error': effortCellError(row, band)}"
                                       :value="effortInputValue(row, band)"
                                       :disabled="!row.is_editable"
                                       :aria-label="'Hours per ' + effortBandLabel(band) + ' ' + row.object_type"
                                       :title="row.is_editable ? 'Hours to migrate one ' + effortBandLabel(band) + ' object' : 'No objects of this type in this workload'"
                                       @input="effortOnInput(row, band, $event.target.value)"
                                       @blur="effortOnBlur(row, band)">
                                <span v-if="effortCellError(row, band)" class="effort-error">{{ effortCellError(row, band) }}</span>
                                <span v-else-if="effortBandChanged(row, band)" class="effort-sf-note">Snowflake: {{ effortCompact(effortSfBandRate(row, band)) }}</span>
                            </td>
                        </tr>
                    </template>
                    <template v-if="effortSectionOpen(section)">
                        <tr v-for="extra in section.extraRows" :key="extra.label">
                            <td colspan="2">{{ extra.label }}</td>
                            <td class="num effort-muted">Flat budget</td>
                            <td class="num effort-muted" :colspan="effortBands.length">N/A</td>
                            <td class="num" style="font-weight:600;">{{ effortHours(extra.hours) }}</td>
                            <td class="effort-muted">Priced as a flat budget; not editable</td>
                        </tr>
                    </template>
                    <tr v-if="effortSectionOpen(section) &amp;&amp; section.zeroTypes.length">
                        <td class="effort-muted" :colspan="effortColumnCount">
                            No {{ effortZeroNote(section.zeroTypes) }} in this workload.
                        </td>
                    </tr>
                  </template>
                    <tr class="effort-total">
                        <td :colspan="effortColumnCount - 2">TOTAL MIGRATION EFFORT</td>
                        <td class="num">
                            {{ effortHours(effortRollup.custom.total) }}
                            <span v-if="effortTotalChanged" class="effort-sf-note">Snowflake: {{ effortHours(effortRollup.sf.total) }}</span>
                        </td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
"""

_OVERVIEW_EFFORT_CARD_TOTAL_HTML = """
                <div class="effort-card">
                    <div class="effort-card-num">{{ effortDaysLabel(effortRollup.custom.total) }}</div>
                    <div class="effort-card-lbl">Total Effort</div>
                    <div v-if="effortTotalChanged" class="effort-sf-note">Snowflake: {{ effortDaysLabel(effortRollup.sf.total) }}</div>
                </div>
                <div class="effort-card">
                    <div class="effort-card-num">{{ effortHours(effortRollup.custom.code) }} h</div>
                    <div class="effort-card-lbl">Code Conversion Effort · {{ effortCount(effortSummary.ddl_objects) }} objects · {{ effortPercent(effortSummary.ddl_auto_pct) }} auto-converted · includes unit testing</div>
                    <div v-if="effortCodeChanged" class="effort-sf-note">Snowflake: {{ effortHours(effortRollup.sf.code) }} h</div>
                </div>
"""

_OVERVIEW_FIXED_BUDGET_VALUE_HTML = """
                    <div style="font-size: 1.6rem; font-weight: 800; color: #102E46; margin-top: 4px;">{{ effortHours(effortRollup.custom.fixed_budget) }} h</div>
                    <div v-if="effortFixedBudgetChanged" class="effort-sf-note">Snowflake: {{ effortHours(effortRollup.sf.fixed_budget) }} h</div>
"""


def load_effort_overrides(path: Path) -> Dict[str, Any]:
    """Load the user's baseline-hour overrides, or an empty set if unusable.

    The overrides are a convenience layered on an estimate that stands without
    them, so an absent or corrupt file must not stop the report generating.
    """
    try:
        with Path(path).open(encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Warning: Could not load effort overrides: {exc}", file=sys.stderr)
        return {}
    if not isinstance(payload, dict):
        print("Warning: Could not load effort overrides: not a JSON object", file=sys.stderr)
        return {}
    return payload


def effort_overrides_module_js() -> str:
    """The shared override module's source, for inlining into the report.

    Inlined rather than linked because the report is opened over file://, where a
    linked script would be blocked.
    """
    module = Path(__file__).parent / "effort_overrides.js"
    try:
        return module.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Warning: Could not read {module.name}: {exc}", file=sys.stderr)
        return ""


def _json_for_script(value: Any) -> str:
    """`json.dumps`, safe to embed inside an HTML `<script>` block.

    A `</script>` sequence inside a string value (a project name or dialect
    label, ultimately from the source database) would otherwise close the
    tag early and let whatever follows run as markup. `<` and `>` cannot
    appear in valid JSON syntax outside a string, so escaping them is lossless.
    """
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")


def effort_payloads_js(
    assessment: Dict[str, Any],
    overrides: Optional[Dict[str, Any]] = None,
    artifact_name: str = "",
) -> str:
    """Baseline artifact and stored overrides, as globals the mixin reads."""
    baseline = {
        "project_name": assessment.get("project_name", ""),
        "source_dialect": assessment.get("source_dialect", ""),
        "artifact": artifact_name,
        "summary": assessment.get("summary", {}),
        "calculator_rows": [asdict(row) for row in assessment.get("calculator_rows", [])],
    }
    return (
        "window.__EFFORT_BASELINE__ = "
        + _json_for_script(baseline)
        + ";\nwindow.__EFFORT_OVERRIDES__ = "
        + _json_for_script(overrides or {})
        + ";"
    )


def effort_overrides_js(
    assessment: Dict[str, Any],
    overrides: Optional[Dict[str, Any]] = None,
    artifact_name: str = "",
) -> str:
    """Everything the Effort tab's interactivity needs, as one classic script."""
    return "\n".join(
        [
            effort_overrides_module_js(),
            effort_payloads_js(assessment, overrides, artifact_name),
            EFFORT_MIXIN_JS,
        ]
    )


def workload_size_label(tier: str, small_max: int, medium_max: int) -> str:
    """Human-readable workload tier label using thresholds from the artifact."""
    labels = {
        "small": f"Small (up to {small_max:,} objects)",
        "medium": f"Medium ({small_max + 1:,}–{medium_max:,} objects)",
        "large": f"Large (more than {medium_max:,} objects)",
    }
    return labels.get(tier, tier.title())


def _esc(text: Any) -> str:
    import html

    return html.escape(str(text)) if text is not None else ""


def _js_str(value: str) -> str:
    """A JS string literal safe to embed in a double-quoted HTML attribute.

    Vue expressions live in attributes (``v-if="..."``), so a double-quoted JS
    string would close the attribute at its first quote and leave the browser
    parsing the rest of the expression as further attribute names -- Vue then
    never sees the expression at all. Single quotes survive the HTML parser.
    """
    js = value.replace("\\", "\\\\").replace("'", "\\'")
    # `"` becomes an entity rather than a JS escape: the HTML parser decodes it
    # back to a plain quote inside the single-quoted literal, so the attribute
    # stays intact and the expression Vue compiles is unchanged.
    html_safe = (
        js.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    )
    return "'" + html_safe + "'"


def _js_str_array(values: List[str]) -> str:
    """A JS array-of-strings literal, attribute-safe -- see :func:`_js_str`."""
    return "[" + ", ".join(_js_str(v) for v in values) + "]"


def _hours_to_rounded_days(hours: float) -> int:
    """Convert effort hours to whole days, rounded up (8h work day)."""
    if hours <= 0:
        return 0
    return int(math.ceil(hours / _HOURS_PER_WORK_DAY))


def _days_label(days: int) -> str:
    return f"{days:,} day" if days == 1 else f"{days:,} days"


def _render_fixed_budget_info_icon(
    fixed_items: Dict[str, Optional[float]],
    workload_tier: str,
    total_objects: int,
    small_max: int,
    medium_max: int,
) -> str:
    """Info icon with hover tooltip listing fixed budget line items."""
    if not fixed_items:
        return ""
    header = (
        f"<div style='margin-bottom:8px;font-weight:600;'>"
        f"{_esc(workload_size_label(workload_tier, small_max, medium_max))} · "
        f"{total_objects:,} objects"
        f"</div>"
    )
    tooltip_lines = header + "".join(
        f"<div style='margin-bottom:4px;'>{_esc(label)}: "
        f"{f'{hours:g} h' if hours is not None else _NOT_APPLICABLE}</div>"
        for label, hours in fixed_items.items()
    )
    return (
        f'<span class="info-icon" style="margin-left:4px;">i'
        f'<span class="tooltip">{tooltip_lines}</span></span>'
    )


def render_overview_section_b_html(assessment: Dict[str, Any]) -> str:
    """Section B on Overview: effort summary for SQL Server DDL + fixed budgets."""
    s = assessment["summary"]
    ddl = s.get("ddl_summary", {})
    ddl_rows = ""
    for obj_type in sorted(ddl.keys()):
        if obj_type in _DDL_EXCLUDED_DISPLAY_TYPES:
            continue
        st = ddl[obj_type]
        pct = f"{st['pct_auto'] * 100:.1f}%"
        bands = st.get("bands") or {}
        ddl_rows += f"""
        <tr>
            <td>{_esc(obj_type)}</td>
            <td class="ctr">{st['total']:,}</td>
            <td class="ctr">{bands.get('critical', 0):,}</td>
            <td class="ctr">{bands.get('high', 0):,}</td>
            <td class="ctr">{bands.get('medium', 0):,}</td>
            <td class="ctr">{bands.get('low', 0):,}</td>
            <td class="ctr">{pct}</td>
        </tr>"""

    fixed_items = s.get("fixed_budget_items", {})
    workload_tier = s.get("workload_size_tier", "small")
    workload_objects = s.get("workload_object_count", s.get("ddl_objects", 0))
    small_max = s.get("workload_small_max", 500)
    medium_max = s.get("workload_medium_max", 1500)
    fixed_info_icon = _render_fixed_budget_info_icon(
        fixed_items,
        workload_tier,
        workload_objects,
        small_max,
        medium_max,
    )
    workload_subtitle = (
        f"<div style='font-size:0.72rem;color:#64748B;margin-top:4px;'>"
        f"{_esc(workload_size_label(workload_tier, small_max, medium_max))}</div>"
    )

    # One metric among several, so it carries the shared card styling rather than a
    # colour and type size that would read as the section's headline.
    automation_card = ""
    hours_saved = s.get("hours_saved_by_automation", 0)
    if hours_saved > 0:
        auto_pct = s.get("automation_savings_pct", 0) * 100
        rewrite_hours = s.get("manual_rewrite_hours", 0)
        automation_card = f"""
                <div class="effort-card">
                    <div class="effort-card-num">{hours_saved:,.0f} h</div>
                    <div class="effort-card-lbl">Saved by automation · {auto_pct:.0f}% of the {rewrite_hours:,.0f} h a manual rebuild would cost</div>
                </div>"""

    return f"""
            <h2 id="effort-estimates" style="font-size: 1.5rem; font-weight: 700; color: #102E46; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="background: #E0F2FE; color: #0284C7; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem;">Section B</span>
                Estimated effort to migrate
                {EFFORT_PREVIEW_BADGE_HTML}
            </h2>
            {EFFORT_DISCLAIMER_HTML}
            <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 20px; line-height: 1.6;">
                Every object is placed in one complexity band and priced at that band's hours per object,
                plus flat budgets for the project phases. Counts reflect unique converted objects
                (session and batch rows excluded).
            </p>

            <div class="effort-cards">
{_OVERVIEW_EFFORT_CARD_TOTAL_HTML}
                {automation_card}
                <div style="background: white; padding: 18px; border-radius: 12px; border-top: 4px solid #FF9F36; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.78rem; color: #64748B; font-weight: 600; text-transform: uppercase; display: flex; align-items: center;">
                        Fixed Budget{fixed_info_icon}
                    </div>
{_OVERVIEW_FIXED_BUDGET_VALUE_HTML}
                    {workload_subtitle}
                </div>
            </div>

            <h3 style="font-size: 1.1rem; font-weight: 700; color: #102E46; margin-bottom: 12px;">Objects by complexity band</h3>
            <div class="effort-table-wrap">
                <table class="effort-table">
                    <thead>
                        <tr>
                            <th>Object Type</th>
                            <th class="ctr">Total</th>
                            <th class="ctr">Critical</th>
                            <th class="ctr">High</th>
                            <th class="ctr">Medium</th>
                            <th class="ctr">Low</th>
                            <th class="ctr">% Auto-Converted</th>
                        </tr>
                    </thead>
                    <tbody>{ddl_rows}</tbody>
                </table>
            </div>

            <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 10px; padding: 16px 20px; margin-bottom: 40px;">
                <p style="margin: 0 0 8px 0; color: #102E46; font-weight: 600;">Need line-item detail?</p>
                <p style="margin: 0 0 12px 0; color: #475569; font-size: 0.9rem; line-height: 1.5;">
                    The Effort Estimates tab shows the full migration calculator — every component, its objects per complexity band, the editable hours per object, and the resulting total.
                </p>
                <a @click="activeTab = 'effort-estimates'"
                   style="display: inline-block; background: #005C8F; color: white; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; cursor: pointer; text-decoration: none;">
                    Open detailed effort calculator →
                </a>
            </div>
    """


def _new_ddl_row() -> Dict[str, int]:
    """Column accumulator for the DDL table's TOTALS row."""
    return {
        "total": 0,
        "success": 0,
        "lines_of_code": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "issues_high": 0,
        "issues_critical": 0,
    }


def _ddl_effort_cell(obj_type: str) -> str:
    """Per-type Effort (h) cell, bound to the override roll-up for that type."""
    key = _js_str(obj_type)
    return (
        "{{ effortDdlCell(" + key + ").custom ? "
        "effortHours(effortDdlCell(" + key + ").custom) : '\u2014' }}"
        '<span v-if="effortDdlCell(' + key + ').changed" class="effort-sf-note">'
        "Snowflake: {{ effortHours(effortDdlCell(" + key + ").sf) }}</span>"
    )


def _render_ddl_assessment_table(
    ddl_summary: Dict[str, Dict[str, Any]],
    testing_hours: float = 0.0,
) -> str:
    """Per-object-type conversion detail: inventory, bands, findings, and hours.

    The band columns count *objects* and the issue columns count *occurrences*,
    which is why the two do not agree: one object carrying three critical findings
    is a single critical object. Only the band columns feed the estimate.
    """
    rows_html = ""
    displayed_types: List[str] = []
    totals = _new_ddl_row()
    for obj_type in sorted(ddl_summary.keys()):
        if obj_type in _DDL_EXCLUDED_DISPLAY_TYPES:
            continue
        st = ddl_summary[obj_type]
        bands = st.get("bands") or {}
        for column in totals:
            totals[column] += bands.get(column, 0) if column in _BANDS else st.get(column, 0)
        pct = f"{st['pct_auto'] * 100:.1f}%"
        effort = _ddl_effort_cell(obj_type)
        displayed_types.append(obj_type)
        rows_html += f"""
        <tr>
            <td>{_esc(obj_type)}</td>
            <td class="ctr">{st['total']:,}</td>
            <td class="ctr">{bands.get('critical', 0):,}</td>
            <td class="ctr">{bands.get('high', 0):,}</td>
            <td class="ctr">{bands.get('medium', 0):,}</td>
            <td class="ctr">{bands.get('low', 0):,}</td>
            <td class="ctr">{pct}</td>
            <td class="num">{st['lines_of_code']:,}</td>
            <td class="ctr">{st['issues_high']:,}</td>
            <td class="ctr">{st['issues_critical']:,}</td>
            <td class="num" style="font-weight:600;">{effort}</td>
            <td style="color:#64748B;font-size:0.8rem;">{_esc(st.get('notes', ''))}</td>
        </tr>"""
    total_pct = f"{(totals['success'] / totals['total'] * 100):.1f}%" if totals["total"] else "—"
    # Always the true sum of the rows displayed above (+ testing) so TOTALS never
    # understates what's visibly listed in this table.
    types_literal = _js_str_array(displayed_types)
    testing_cell = (
        "{{ effortHours(effortRollup.custom.testing) }}"
        '<span v-if="effortTestingChanged" class="effort-sf-note">'
        "Snowflake: {{ effortHours(effortRollup.sf.testing) }}</span>"
    )
    total_effort_cell = (
        "{{ effortHours(effortDdlTableTotal(" + types_literal + ")) }}"
        '<span v-if="effortDdlTableTotalChanged(' + types_literal + ')" class="effort-sf-note">'
        "Snowflake: {{ effortHours(effortDdlTableTotalSf(" + types_literal + ")) }}</span>"
    )
    if testing_hours:
        rows_html += f"""
        <tr style="background:#F8FAFC;">
            <td style="padding:8px 12px;">Code Conversion Testing</td>
            <td colspan="9" style="padding:8px 12px;color:#64748B;font-size:0.8rem;">Unit testing for functions and stored procedures</td>
            <td style="padding:8px 12px;text-align:right;font-weight:600;">{testing_cell}</td>
            <td style="padding:8px 12px;color:#64748B;font-size:0.8rem;">Priced per object by band (see calculator)</td>
        </tr>"""
    rows_html += f"""
        <tr class="effort-total">
            <td>TOTALS</td>
            <td class="ctr">{totals['total']:,}</td>
            <td class="ctr">{totals['critical']:,}</td>
            <td class="ctr">{totals['high']:,}</td>
            <td class="ctr">{totals['medium']:,}</td>
            <td class="ctr">{totals['low']:,}</td>
            <td class="ctr">{total_pct}</td>
            <td class="num">{totals['lines_of_code']:,}</td>
            <td class="ctr">{totals['issues_high']:,}</td>
            <td class="ctr">{totals['issues_critical']:,}</td>
            <td class="num">{total_effort_cell}</td>
            <td></td>
        </tr>"""
    return rows_html


def _render_top_issues_section(top_issues: List[Dict[str, Any]]) -> str:
    """Top DDL issues section, worst severity first; empty if there are no issues.

    The order is the artifact's own -- C# selects the most frequent codes and emits them
    severity-first, so neither renderer needs a severity comparator of its own.
    """
    if not top_issues:
        return ""

    issues_html = ""
    for issue in top_issues:
        issues_html += f"""
        <tr>
            <td>{_esc(issue['code'])}</td>
            <td>{_esc(issue.get('name', ''))}</td>
            <td class="ctr">{_esc(issue.get('severity', '—'))}</td>
            <td class="ctr">{issue['occurrences']:,}</td>
        </tr>"""

    return f"""
        <h2 id="effort-top-issues" style="font-size:1.35rem;font-weight:700;color:#102E46;margin:32px 0 12px;">Top issues (DDL)</h2>
        <p class="effort-lead">The conversion issue codes that occur most across DDL objects, listed
        most severe first — a critical code hit a dozen times needs attention before a low one hit
        hundreds.</p>
        <div class="effort-table-wrap">
            <table class="effort-table">
                <thead><tr>
                    <th>Issue Code</th>
                    <th>Name</th>
                    <th class="ctr">Severity</th>
                    <th class="ctr">Occurrences</th>
                </tr></thead>
                <tbody>{issues_html}</tbody>
            </table>
        </div>"""


def _render_effort_formulas_legend(summary: Dict[str, Any]) -> str:
    """Collapsible legend explaining how each effort figure is derived."""
    automation_note = ""
    if summary.get("hours_saved_by_automation", 0) > 0:
        automation_note = (
            "<p><strong>Saved by automation:</strong> what the same objects would cost rebuilt "
            "by hand, minus what is charged above. Automation is never applied as a discount to "
            "the hours themselves — it is already expressed by where the objects landed, since a "
            "cleanly converted object is a Low one. "
            f"Here a manual rebuild would cost ≈ {summary.get('manual_rewrite_hours', 0):,.0f} h "
            f"against the {summary.get('code_estimated_hours', 0):,.0f} h charged, so automation "
            f"saved ≈ {summary.get('hours_saved_by_automation', 0):,.0f} h.</p>"
        )
    return f"""
        <details style="margin-bottom:32px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px;">
            <summary style="font-weight:700;color:#102E46;cursor:pointer;">How these hours are calculated</summary>
            <div style="margin-top:12px;font-size:0.88rem;color:#475569;line-height:1.6;">
                <p><strong>One formula, per object type:</strong></p>
                <p style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;padding:10px 12px;">
                    hours = (critical objects × h/critical) + (high × h/high) + (medium × h/medium) + (low × h/low)
                </p>
                <p>Every object is counted in exactly one band, so the band counts always add up to the
                object total — which means you can reproduce any figure in the calculator with a
                calculator. Unit testing is priced the same way, from its own hours-per-object card.</p>
                <p><strong>Bands:</strong> Critical = a critical finding, or SnowConvert could not convert it.
                High = a high-severity finding, or a partial conversion. Medium = converted, with
                medium-severity findings. Low = converted clean, or minor findings only.</p>
                {automation_note}
                <p><strong>Fixed Budget:</strong> data migration setup plus phase budgets scaled by workload size — Small (≤{summary.get('workload_small_max', 500):,} objects), Medium ({summary.get('workload_small_max', 500) + 1:,}–{summary.get('workload_medium_max', 1500):,}), Large (&gt;{summary.get('workload_medium_max', 1500):,}).</p>
                <p><strong>Sources:</strong> SnowConvert conversion statistics — per-object conversion status and issue severities.</p>
            </div>
        </details>"""


def render_effort_tab_html(assessment: Dict[str, Any]) -> str:
    """Full effort page aligned with the migration assessment workbook sections."""
    summary = assessment["summary"]
    ddl = summary.get("ddl_summary", {})
    top_issues = assessment.get("top_issues", [])

    issues_section = _render_top_issues_section(top_issues)
    formulas_legend = _render_effort_formulas_legend(summary)

    return f"""
    <div class="tab-content" :class="{{active: activeTab === 'effort-estimates'}}">
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 1.875rem; font-weight: 800; color: #102E46; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                Migration effort estimates
                {EFFORT_PREVIEW_BADGE_HTML}
            </h1>
            <p class="effort-lead">
                A person-hours estimate for this migration, derived from SnowConvert's own conversion
                results. Every object lands in exactly one complexity band — Critical, High, Medium or
                Low — and each band carries an hours-per-object rate. So every figure below is
                objects × rate, and you can check any of them by hand.
            </p>
            <p class="effort-lead">
                Snowflake's rates are a starting point, not a verdict: real effort varies with project
                scope, team experience, data quality and migration complexity. Adjust any rate to match
                what your team knows.
            </p>
        </div>

{_EFFORT_KPI_CARDS_HTML}

        <h2 id="effort-calculator" style="font-size:1.35rem;font-weight:700;color:#102E46;margin-bottom:12px;">Migration effort calculator</h2>
        <p class="effort-lead">
            Every hours-per-object cell is editable. Change one and its row, its section subtotal,
            the total and the cards above all follow — Snowflake's own figure stays beside yours, so
            nothing is overwritten.
        </p>
        <p class="effort-lead">
            Your changes are called <strong>overrides</strong>{_OVERRIDES_INFO_ICON}. They live in
            this page while it is open — download them to keep them, or to hand them to someone else.
        </p>
{_EFFORT_BAND_LEGEND_HTML}
{_EFFORT_TOOLBAR_HTML}
{_EFFORT_CALCULATOR_TABLE_HTML}

        <h2 id="effort-ddl-assessment" style="font-size:1.35rem;font-weight:700;color:#102E46;margin:32px 0 12px;">Conversion detail by object type</h2>
        <p style="color:#64748B;font-size:0.9rem;margin-bottom:12px;">Band columns count objects; the two findings columns count issue occurrences, so one object with several critical findings appears once as Critical but several times under Critical findings.</p>
        <div class="effort-table-wrap">
            <table class="effort-table compact">
                <thead><tr>
                    <th>Object Type</th>
                    <th class="ctr">Objects</th>
                    <th class="ctr">Critical</th>
                    <th class="ctr">High</th>
                    <th class="ctr">Medium</th>
                    <th class="ctr">Low</th>
                    <th class="ctr">% Auto-Conv.</th>
                    <th class="num">Lines of Code</th>
                    <th class="ctr">High findings</th>
                    <th class="ctr">Critical findings</th>
                    <th class="num">Effort (h)</th>
                    <th>Priced as</th>
                </tr></thead>
                <tbody>{_render_ddl_assessment_table(ddl, summary.get("testing_estimated_hours", 0))}</tbody>
            </table>
        </div>

        {issues_section}

        {formulas_legend}
    </div>
    """
