/* Shared migration-effort override math for the HTML assessment report and the
 * dashboard. One implementation so the two renderers can never disagree on a
 * total; they still format and lay out independently.
 *
 * Pure functions only: no DOM, no storage, no clock. `serializeOverrides` takes
 * the timestamp as a parameter so it is testable.
 *
 * Loaded as a CLASSIC script, not a module. Chrome blocks external module
 * scripts over file://, and an inline type="module" block is deferred so it
 * would run after the classic script that calls createApp. So this file
 * publishes one frozen object on globalThis instead of using `export`.
 */
(function () {
  "use strict";

  /* Bumped to 2 when pricing moved from one baseline figure per row to a rate
   * per complexity band. A v1 file is discarded rather than reinterpreted: its
   * single number meant something this model has no place for. */
  const SCHEMA_VERSION = 2;
  const HOURS_PER_WORK_DAY = 8;

  /* Bounds shared with the dashboard's PUT validator so a value the report
   * accepts is never rejected on write. */
  const MAX_OVERRIDE_ENTRIES = 256;
  const MAX_RATE_HOURS = 100000;
  const MAX_DECIMAL_PLACES = 2;

  /* Worst first — the order the workbook lists them and the report renders them.
   * Redesign carries a rate but never a count, so it is not offered for editing. */
  const BANDS = ["critical", "high", "medium", "low", "redesign"];
  const EDITABLE_BANDS = ["critical", "high", "medium", "low"];

  const CONVERSION = "conversion";
  const TESTING = "testing";
  const FIXED_BUDGET = "fixed_budget";
  const DATA_MIGRATION = "data_migration";

  /* Wider than any displayed precision (hours render to one decimal), so this
   * only clears accumulated float noise and never moves a shown figure. */
  function round4(value) {
    return Math.round(value * 10000) / 10000;
  }

  function isNumber(value) {
    return typeof value === "number" && isFinite(value);
  }

  function numberOr(value, fallback) {
    return isNumber(value) ? value : fallback;
  }

  function has(object, key) {
    return Object.prototype.hasOwnProperty.call(object, key);
  }

  function isPlainObject(value) {
    return !!value && typeof value === "object" && !Array.isArray(value);
  }

  /** A banded row prices counted objects per band; a flat row is one budget. */
  function isBandedRow(row) {
    return isPlainObject(row && row.band_counts) && isPlainObject(row.band_rates);
  }

  /**
   * Whether a user's number could change anything on this row.
   *
   * A banded row with no objects is not editable: every band count is zero, so
   * any rate the user enters still prices zero.
   *
   * A flat row is always editable, including one Snowflake declines to price.
   * "We publish no figure for this yet" is a statement about our estimate, not a
   * restriction on the user's -- and a line nobody has costed is exactly where a
   * customer's own number is worth the most. Such a row keeps rendering N/A until
   * something is typed into it.
   */
  function isEditableRow(row) {
    if (isBandedRow(row)) {
      return numberOr(row.band_counts.total, 0) > 0;
    }
    return !!row;
  }

  /**
   * A flat row Snowflake publishes no figure for. Renderers say so beside the
   * input rather than leaving an empty box unexplained; the concept lives here so
   * neither renderer has to re-derive it from a null.
   */
  function isUnestimatedRow(row) {
    return !isBandedRow(row) && !isNumber(row && row.flat_hours);
  }

  /**
   * The rates a banded row prices with, after the user's edits.
   *
   * A row's own card is the starting point, so an override of one band leaves
   * the others exactly as Snowflake priced them.
   */
  function ratesFor(row, override) {
    const rates = {};
    BANDS.forEach(function (band) {
      const edited = override ? override[band] : undefined;
      rates[band] = isNumber(edited)
        ? edited
        : numberOr(row.band_rates[band], 0);
    });
    return rates;
  }

  /**
   * Snowflake's own figure for one editable cell: a band's rate on a banded row,
   * or a flat row's whole budget, which is null when Snowflake does not price the
   * line at all.
   *
   * Normalized exactly as `ratesFor` normalizes, so "the user typed what
   * Snowflake already charges" is decided against the number actually priced
   * rather than against a missing key.
   */
  function snowflakeRateFor(row, band) {
    if (!band) {
      return row && isNumber(row.flat_hours) ? row.flat_hours : null;
    }
    return row && row.band_rates ? numberOr(row.band_rates[band], 0) : 0;
  }

  /**
   * The value to store for one cell, or null to clear it.
   *
   * A number typed back to Snowflake's own figure clears the override instead of
   * recording one that prices identically: such an entry would still count toward
   * the override badge, still ride along in an exported file, and still leave
   * "Reset all" enabled with nothing to reset.
   */
  function overrideToStore(row, band, value) {
    if (!isNumber(value)) {
      return null;
    }
    return value === snowflakeRateFor(row, band) ? null : value;
  }

  /**
   * Hours for a banded row: the sum over bands of objects times rate.
   *
   * The same arithmetic the .NET calculator ran, which is why the two agree
   * without this module having to know anything about how the rates were chosen.
   */
  function priceBands(counts, rates) {
    return round4(
      BANDS.reduce(function (total, band) {
        return total + numberOr(counts[band], 0) * numberOr(rates[band], 0);
      }, 0),
    );
  }

  /** Which bands of a row a user may edit: the ones its objects can land in. */
  function editableBands(row) {
    return isBandedRow(row) ? EDITABLE_BANDS.slice() : [];
  }

  /**
   * Validates one rate or flat-hours input. Blank clears the override; `0` is a
   * real override meaning "we will not spend time here" and must stay distinct
   * from blank. Decimal places are counted on the text, not by comparing floats.
   */
  function validateRateInput(raw) {
    if (raw === null || raw === undefined) {
      return { ok: true, value: null, error: "" };
    }
    const text = String(raw).trim();
    if (text === "") {
      return { ok: true, value: null, error: "" };
    }
    if (!/^-?(?:\d+\.?\d*|\.\d+)$/.test(text)) {
      return { ok: false, value: null, error: "Enter a number of hours." };
    }
    const value = Number(text);
    if (!isFinite(value)) {
      return { ok: false, value: null, error: "Enter a number of hours." };
    }
    if (value < 0) {
      return { ok: false, value: null, error: "Hours cannot be negative." };
    }
    if (value > MAX_RATE_HOURS) {
      return {
        ok: false,
        value: null,
        error: "Hours must be " + MAX_RATE_HOURS.toLocaleString() + " or less.",
      };
    }
    const dot = text.indexOf(".");
    if (dot >= 0 && text.length - dot - 1 > MAX_DECIMAL_PLACES) {
      return { ok: false, value: null, error: "At most two decimal places." };
    }
    return { ok: true, value: value, error: "" };
  }

  /**
   * Pairs every row with its custom figures. An un-overridden row's custom
   * values are its Snowflake values verbatim, so a renderer can read the custom
   * column unconditionally.
   */
  function applyOverrides(rows, bandRates, flatHours) {
    const rateOverrides = bandRates || {};
    const flatOverrides = flatHours || {};
    return (rows || []).map(function (row) {
      const editable = isEditableRow(row);
      // Read the value; never probe with hasOwnProperty. A missing key reads as
      // undefined, which the checks below reject, so the two are equivalent --
      // except that a plain property read is what reactive frameworks track.
      // Vue 3's reactive proxy traps get/set/has/ownKeys but NOT
      // getOwnPropertyDescriptor, so a hasOwnProperty probe is invisible to it;
      // combined with `&&` short-circuiting it meant an absent key was never
      // read at all, leaving the computed with no dependency on it. The first
      // override typed into a row then changed nothing on screen until some
      // other row forced a recompute.
      if (isBandedRow(row)) {
        const candidate = rateOverrides[row.key];
        const edits = isPlainObject(candidate) ? candidate : null;
        const customRates = ratesFor(row, editable ? edits : null);
        // Overridden means "prices differently from Snowflake", not "has an entry
        // stored". Two cases turn on the difference: a rate typed back to
        // Snowflake's own number, and the three bands left untouched on a row
        // edited in a fourth. Neither is a change, and reporting either as one
        // puts a "Snowflake: x" note beside a figure that is Snowflake's.
        const overriddenBands = EDITABLE_BANDS.filter(function (band) {
          return customRates[band] !== snowflakeRateFor(row, band);
        });
        const overridden = overriddenBands.length > 0;
        return Object.assign({}, row, {
          custom_band_rates: customRates,
          custom_estimated_hours: overridden
            ? priceBands(row.band_counts, customRates)
            : row.estimated_hours,
          custom_flat_hours: null,
          is_overridden: overridden,
          overridden_bands: overriddenBands,
          is_editable: editable,
          is_unestimated: false,
          editable_bands: EDITABLE_BANDS.slice(),
        });
      }

      const candidate = flatOverrides[row.key];
      const stored = editable && isNumber(candidate) ? round4(candidate) : null;
      // Null flat_hours is Snowflake declining to price the line, so any budget
      // the user enters differs from it and is a real override.
      const overridden = stored !== null && stored !== snowflakeRateFor(row, null);
      return Object.assign({}, row, {
        custom_band_rates: null,
        custom_estimated_hours: overridden ? stored : row.estimated_hours,
        custom_flat_hours: overridden ? stored : row.flat_hours,
        is_overridden: overridden,
        overridden_bands: [],
        is_editable: editable,
        // Stays true once overridden: Snowflake still has no figure, which is why
        // the comparison beside the input reads "not estimated" rather than a number.
        is_unestimated: isUnestimatedRow(row),
        editable_bands: [],
      });
    });
  }

  function bucketOf(row) {
    return row && row.bucket;
  }

  function isConversion(row) {
    return bucketOf(row) === CONVERSION;
  }

  function isTesting(row) {
    return bucketOf(row) === TESTING;
  }

  function isFixedBudget(row) {
    const bucket = bucketOf(row);
    return bucket === FIXED_BUDGET || bucket === DATA_MIGRATION;
  }

  function always() {
    return true;
  }

  function sumBy(rows, predicate, field) {
    return rows.reduce(function (total, row) {
      return predicate(row) ? total + numberOr(row[field], 0) : total;
    }, 0);
  }

  /**
   * Rolls applied rows up into the figures the report and dashboard display.
   *
   * Each custom figure is its rows' custom hours plus a residual: whatever the
   * C# summary counts that no calculator row carries, which today is the synonym
   * conversion budget. Deriving the residual from the summary rather than
   * enumerating its sources means an empty override set reproduces every
   * Snowflake figure exactly, with no compatibility branch.
   *
   * The override maps are only read to report keys that no longer match a row;
   * the arithmetic uses the applied rows alone.
   */
  function rollUp(appliedRows, summary, bandRates, flatHours) {
    const rows = appliedRows || [];
    const s = summary || {};

    function figure(summaryValue, predicate) {
      const custom = sumBy(rows, predicate, "custom_estimated_hours");
      if (!isNumber(summaryValue)) {
        return round4(custom);
      }
      const residual = summaryValue - sumBy(rows, predicate, "estimated_hours");
      return round4(custom + residual);
    }

    const customConversion = figure(s.conversion_estimated_hours, isConversion);
    const customTesting = figure(s.testing_estimated_hours, isTesting);

    const sf = {
      total: numberOr(s.total_estimated_hours, 0),
      code: numberOr(s.code_estimated_hours, 0),
      conversion: numberOr(s.conversion_estimated_hours, 0),
      testing: numberOr(s.testing_estimated_hours, 0),
      fixed_budget: numberOr(s.fixed_budget_hours, 0),
    };
    const custom = {
      total: figure(s.total_estimated_hours, always),
      code: round4(customConversion + customTesting),
      conversion: customConversion,
      testing: customTesting,
      fixed_budget: figure(s.fixed_budget_hours, isFixedBudget),
    };

    const ddlSummary = s.ddl_summary || {};
    const ddlByType = {};
    Object.keys(ddlSummary).forEach(function (type) {
      const entry = ddlSummary[type] || {};
      const sfHours = numberOr(entry.estimated_hours, 0);
      // Only an overridden row moves a DDL cell; otherwise keep the summary's own
      // figure so this surface is byte-identical to the baseline report.
      const row = rows.filter(function (candidate) {
        return isConversion(candidate) && candidate.ddl_type === type;
      })[0];
      ddlByType[type] = {
        sf: sfHours,
        custom:
          row && row.is_overridden
            ? round4(numberOr(row.custom_estimated_hours, 0))
            : sfHours,
      };
    });

    const rowKeys = {};
    rows.forEach(function (row) {
      rowKeys[row.key] = true;
    });
    const staleKeys = Object.keys(bandRates || {})
      .concat(Object.keys(flatHours || {}))
      .filter(function (key) {
        return !has(rowKeys, key);
      });

    return {
      sf: sf,
      custom: custom,
      ddl_by_type: ddlByType,
      overridden_count: rows.filter(function (row) {
        return row.is_overridden;
      }).length,
      stale_keys: staleKeys,
    };
  }

  /* The calculator's sections, in display order. Fixed rather than derived from
   * artifact row order: a rate table reordering its rows must not reshuffle the
   * page. The third section is a catch-all, so no row can go unrendered. */
  const SECTION_DEFS = [
    {
      key: CONVERSION,
      title: "Code conversion",
      blurb: "objects × hours per object",
      shape: "banded",
      match: isConversion,
    },
    {
      key: TESTING,
      title: "Unit testing",
      blurb: "testing what was converted",
      shape: "banded",
      match: isTesting,
    },
    {
      key: FIXED_BUDGET,
      title: "Fixed budgets & data migration",
      blurb: "one budget per line, no complexity",
      shape: "flat",
      match: always,
    },
  ];

  /**
   * A banded row with no objects prices nothing and cannot be overridden, so it
   * is collapsed into a footnote rather than shown as a line of zeros. A row that
   * charges nothing for another reason -- the "included elsewhere" marker -- still
   * has objects, so it stays visible.
   */
  function isEmptyBandedRow(row) {
    return isBandedRow(row) && numberOr(row.band_counts.total, 0) === 0;
  }

  /**
   * Flat budgets the summary counts that no calculator row carries, today the
   * synonym conversion budget. Rendered read-only so a section's visible lines
   * add up to its subtotal.
   *
   * Matched by label against each row's "Component - ObjectType". The numeric
   * test is what keeps the null data-migration entries out: their labels do not
   * match their rows' labels either, so label mismatch alone would render them a
   * second time beside the real rows.
   */
  function orphanBudgetItems(rows, summary) {
    const items = (summary || {}).fixed_budget_items;
    if (!isPlainObject(items)) {
      return [];
    }
    const rowLabels = {};
    rows.forEach(function (row) {
      rowLabels[row.component + " — " + row.object_type] = true;
    });
    return Object.keys(items)
      .filter(function (label) {
        return isNumber(items[label]) && items[label] !== 0 && !has(rowLabels, label);
      })
      .map(function (label) {
        return { label: label, hours: round4(items[label]) };
      });
  }

  /**
   * Groups applied rows into the sections both renderers lay out, with a subtotal
   * each.
   *
   * Shared rather than reimplemented per renderer for the same reason `rollUp` is:
   * these subtotals are arithmetic over numbers the user typed, and two
   * implementations could disagree about one.
   *
   * The final section's subtotal is a residual -- the total less the two banded
   * sections -- not a sum of its own rows. That makes the three subtotals add up
   * to the grand total by construction, absorbing both the flat budgets no row
   * carries and any row whose bucket this module does not recognize.
   */
  function groupSections(appliedRows, summary, rollup) {
    const rows = appliedRows || [];
    const totals = rollup || { sf: {}, custom: {} };
    const claimed = {};

    const sections = SECTION_DEFS.map(function (def) {
      const mine = rows.filter(function (row) {
        return !has(claimed, row.key) && def.match(row);
      });
      mine.forEach(function (row) {
        claimed[row.key] = true;
      });

      const visible = mine.filter(function (row) {
        return !isEmptyBandedRow(row);
      });
      const zeroTypes = mine
        .filter(isEmptyBandedRow)
        .map(function (row) {
          return row.object_type;
        });

      return {
        key: def.key,
        title: def.title,
        blurb: def.blurb,
        shape: def.shape,
        rows: visible,
        extraRows: def.shape === "flat" ? orphanBudgetItems(rows, summary) : [],
        zeroTypes: zeroTypes,
        subtotal: {
          custom: numberOr(totals.custom[def.key], 0),
          sf: numberOr(totals.sf[def.key], 0),
        },
      };
    });

    // The catch-all section is priced by difference so that whatever the other
    // two do not claim -- including buckets added to the artifact after this code
    // was written -- still reaches the reader inside a subtotal that matches.
    const last = sections[sections.length - 1];
    ["custom", "sf"].forEach(function (side) {
      last.subtotal[side] = round4(
        numberOr(totals[side].total, 0) -
          numberOr(totals[side][CONVERSION], 0) -
          numberOr(totals[side][TESTING], 0),
      );
    });

    return sections;
  }

  /** Whole work days, rounded up — matches the report's own hours-to-days rule. */
  function hoursToDays(hours) {
    if (!isNumber(hours) || hours <= 0) {
      return 0;
    }
    return Math.ceil(hours / HOURS_PER_WORK_DAY);
  }

  function emptyOverrides() {
    return {
      schema_version: SCHEMA_VERSION,
      updated_at: null,
      baseline: null,
      band_rates: {},
      flat_hours: {},
      // Set only when a file was rejected for its schema, so a reader can be told
      // "written by an older model" instead of the indistinguishable "0 overrides".
      discarded: false,
      discarded_version: null,
    };
  }

  function countEntries(overrides) {
    return (
      Object.keys(overrides.band_rates).length + Object.keys(overrides.flat_hours).length
    );
  }

  /**
   * Normalizes an overrides payload, tolerating anything malformed by falling
   * back to "no overrides" rather than throwing. An unknown schema_version is
   * discarded whole: a writer's semantics for a different version are unknown,
   * so guessing at them would silently corrupt the user's numbers.
   */
  function parseOverrides(json) {
    let raw = json;
    if (typeof raw === "string") {
      try {
        raw = JSON.parse(raw);
      } catch (error) {
        return emptyOverrides();
      }
    }
    if (!isPlainObject(raw)) {
      return emptyOverrides();
    }
    if (
      raw.schema_version !== undefined &&
      raw.schema_version !== null &&
      raw.schema_version !== SCHEMA_VERSION
    ) {
      // A v1 file's single baseline figure has no meaning under band pricing, so it
      // is still discarded whole -- but reported. Loading it as "0 overrides" told
      // the user nothing, and their rates need re-entering rather than hunting.
      return Object.assign(emptyOverrides(), {
        discarded: true,
        discarded_version: isNumber(raw.schema_version) ? raw.schema_version : null,
      });
    }

    const bandRates = {};
    if (isPlainObject(raw.band_rates)) {
      Object.keys(raw.band_rates)
        .slice(0, MAX_OVERRIDE_ENTRIES)
        .forEach(function (key) {
          const card = raw.band_rates[key];
          if (!isPlainObject(card)) {
            return;
          }
          const kept = {};
          EDITABLE_BANDS.forEach(function (band) {
            const checked = validateRateInput(card[band]);
            if (checked.ok && checked.value !== null) {
              kept[band] = checked.value;
            }
          });
          if (Object.keys(kept).length > 0) {
            bandRates[key] = kept;
          }
        });
    }

    const flatHours = {};
    if (isPlainObject(raw.flat_hours)) {
      Object.keys(raw.flat_hours)
        .slice(0, MAX_OVERRIDE_ENTRIES)
        .forEach(function (key) {
          const checked = validateRateInput(raw.flat_hours[key]);
          if (checked.ok && checked.value !== null) {
            flatHours[key] = checked.value;
          }
        });
    }

    return {
      schema_version: SCHEMA_VERSION,
      updated_at: typeof raw.updated_at === "string" ? raw.updated_at : null,
      baseline: isPlainObject(raw.baseline) ? raw.baseline : null,
      band_rates: bandRates,
      flat_hours: flatHours,
      discarded: false,
      discarded_version: null,
    };
  }

  function serializeOverrides(bandRates, flatHours, baselineMeta, nowIso) {
    const rates = {};
    const rateSource = bandRates || {};
    Object.keys(rateSource).forEach(function (key) {
      const card = rateSource[key];
      if (!isPlainObject(card)) {
        return;
      }
      const kept = {};
      EDITABLE_BANDS.forEach(function (band) {
        if (isNumber(card[band])) {
          kept[band] = card[band];
        }
      });
      if (Object.keys(kept).length > 0) {
        rates[key] = kept;
      }
    });

    const flat = {};
    const flatSource = flatHours || {};
    Object.keys(flatSource).forEach(function (key) {
      if (isNumber(flatSource[key])) {
        flat[key] = flatSource[key];
      }
    });

    return {
      schema_version: SCHEMA_VERSION,
      updated_at: typeof nowIso === "string" ? nowIso : null,
      baseline: isPlainObject(baselineMeta) ? baselineMeta : null,
      band_rates: rates,
      flat_hours: flat,
    };
  }

  /**
   * Decides between overrides handed to the page at generation time and
   * overrides the browser has stored, by comparing `updated_at`. The file wins
   * only when it is strictly newer, so edits saved from the dashboard carry over
   * into a regenerated report without discarding unsaved local edits.
   */
  function adoptOverrides(fileOverrides, storedOverrides) {
    const file = parseOverrides(fileOverrides);
    const stored = parseOverrides(storedOverrides);
    const hasStored = countEntries(stored) > 0;
    const hasFile = countEntries(file) > 0;

    if (!hasStored) {
      return { overrides: file, source: hasFile ? "file" : "empty" };
    }
    if (!hasFile) {
      return { overrides: stored, source: "stored" };
    }
    const fileNewer =
      typeof file.updated_at === "string" &&
      (typeof stored.updated_at !== "string" || file.updated_at > stored.updated_at);
    return fileNewer
      ? { overrides: file, source: "file" }
      : { overrides: stored, source: "stored" };
  }

  globalThis.EffortOverrides = Object.freeze({
    SCHEMA_VERSION: SCHEMA_VERSION,
    HOURS_PER_WORK_DAY: HOURS_PER_WORK_DAY,
    MAX_OVERRIDE_ENTRIES: MAX_OVERRIDE_ENTRIES,
    MAX_RATE_HOURS: MAX_RATE_HOURS,
    BANDS: Object.freeze(BANDS.slice()),
    EDITABLE_BANDS: Object.freeze(EDITABLE_BANDS.slice()),
    validateRateInput: validateRateInput,
    isBandedRow: isBandedRow,
    editableBands: editableBands,
    priceBands: priceBands,
    snowflakeRateFor: snowflakeRateFor,
    overrideToStore: overrideToStore,
    applyOverrides: applyOverrides,
    rollUp: rollUp,
    groupSections: groupSections,
    hoursToDays: hoursToDays,
    countEntries: countEntries,
    parseOverrides: parseOverrides,
    serializeOverrides: serializeOverrides,
    adoptOverrides: adoptOverrides,
  });
})();
