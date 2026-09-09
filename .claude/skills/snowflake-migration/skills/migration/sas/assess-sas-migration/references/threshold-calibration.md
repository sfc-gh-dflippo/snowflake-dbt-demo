# Threshold Calibration

> **Scope:** These thresholds tune only the **complexity** (LOW/MEDIUM/HIGH) and **volume** axes —
> a sizing/effort signal. They do NOT affect the **translation tier** (Tier 1/2/3). Tier is set by
> the strict "any-block" rule in `../../references/block-tiering-spec.md` (any Tier-3 block → Tier 3,
> else any Tier-2 → Tier 2, else Tier 1) and is not calibratable.

## Current Defaults

### Complexity Thresholds

| Level | Score Range | Meaning |
|-------|-------------|---------|
| LOW | 0 - 50 | Straightforward SQL migration, high automation potential |
| MEDIUM | 51 - 150 | Moderate complexity, may need stored procedures or manual review |
| HIGH | > 150 | Likely needs PySpark/SCOS, multiple stored procedures, or significant manual effort |

### Volume Thresholds (Line Count)

| Level | Lines | Meaning |
|-------|-------|---------|
| LOW | 0 - 250 | Small file, typically 1-3 blocks |
| MEDIUM | 251 - 1000 | Medium file, multiple logical steps |
| HIGH | > 1000 | Large file, often multi-phase pipeline or extensive macro library |

---

## How to Calibrate

### Step 1: Run Against Your Corpus

```bash
python assess_sas.py /path/to/customer/sas/files --output ./calibration_run
```

### Step 2: Check Distribution

Open `assessment.json` and examine `portfolio_summary.complexity_distribution` and `portfolio_summary.volume_distribution`.

**Target distribution** (empirically validated):
- Complexity: ~50% LOW, ~35% MEDIUM, ~15% HIGH
- Volume: ~50% LOW, ~35% MEDIUM, ~15% HIGH

### Step 3: Adjust Thresholds

If the distribution is off, create a custom `config.json`:

**Too many HIGH files (>25%):**
```json
{
  "complexity_thresholds": { "low_max": 60, "medium_max": 180 },
  "volume_thresholds": { "low_max": 300, "medium_max": 1200 }
}
```

**Too many LOW files (>70%):**
```json
{
  "complexity_thresholds": { "low_max": 35, "medium_max": 100 },
  "volume_thresholds": { "low_max": 150, "medium_max": 600 }
}
```

### Step 4: Re-run

```bash
python assess_sas.py /path/to/customer/sas/files --config config.json --output ./calibration_v2
```

---

## Known Corpus Benchmarks

| Corpus | Files | LOW% | MED% | HIGH% | Notes |
|--------|-------|------|------|-------|-------|
| Generic (1483 files) | 1483 | 62% | 37% | 0.1% | Mix of customers, default thresholds |
| DI Studio corpus (262 files) | 262 | 7% | 92% | 0% | All SAS DI Studio — boilerplate inflates MEDIUM |
| Training scripts (112 files) | 112 | ~60% | ~30% | ~10% | Representative sample |

---

## Scoring Components Explained

The total score is: `base_score + feature_score + structure_score`

### Base Score
- Sum of block-type weights (PROC SQL=2, DATA STEP=2, MACRO=4, etc.)
- Log-damped above 50 to prevent runaway scores from many simple blocks

### Feature Score
- Pattern-matched against SAS constructs that indicate translation difficulty
- Tier 3 patterns (HASH, CALL EXECUTE, statistical PROCs): +6-8 points each
- Tier 2 patterns (CALL SYMPUT, PROC TRANSPOSE): +3 points each
- Tier 1 advanced (RETAIN, ARRAY, MERGE, FIRST./LAST.): +1-3 points each
- Each pattern capped at 3 occurrences (prevents repetitive code from dominating)
- Boilerplate files get 50% discount on Tier 2/3 feature scores

### Structure Score
- Macro count: +2 per macro (max 10)
- Nested macros: +3 each (max 5)
- Macro variables: +1 each (max 10)
- Boilerplate files: subtract 5 macros and 10 vars before scoring
