# SAS Migration Assessment Tool

Standalone CLI for assessing SAS-to-Snowflake migration complexity and volume.

## Usage

```bash
cd assess-sas-migration/tool

# Analyze a directory of .sas files
python assess_sas.py /path/to/sas/files --output ./results

# Analyze a single file
python assess_sas.py /path/to/script.sas --output ./results

# Use custom thresholds
python assess_sas.py /path/to/sas/ --config custom_config.json

# JSON only
python assess_sas.py /path/to/sas/ --format json --output ./results

# HTML report only
python assess_sas.py /path/to/sas/ --format html --output ./results
```

## Outputs

| File | Description |
|------|-------------|
| `assessment.json` | Machine-readable per-file metrics, portfolio summary, dependency graph |
| `assessment_report.md` | Human-readable report with tables and distribution analysis |
| `assessment_report.html` | Self-contained, SCAI-themed HTML report (KPIs, tier mix, complexity/volume charts, dependency DAG, per-file detail). Open in a browser. |
| `dependency_dag.mmd` | Mermaid diagram showing cross-file data flow dependencies |

`--format` accepts `json`, `md`, `html`, or `all` (default). The HTML report renders fully offline except the dependency diagram, which uses the Mermaid CDN when opened in a browser (an edges table is the offline fallback).

## Threshold Tuning

Edit `config.json` to adjust classification boundaries:

```json
{
  "complexity_thresholds": {
    "low_max": 50,
    "medium_max": 150
  },
  "volume_thresholds": {
    "low_max": 250,
    "medium_max": 1000
  }
}
```

**Target distribution** (empirically validated against 1400+ real SAS files):
- ~50% LOW, ~35% MEDIUM, ~15% HIGH

## Dependencies

Python 3.8+ with standard library only. No pip install required.

## How It Works

1. **Parser** — Extracts typed blocks (DATA steps, PROC SQL, macros, etc.) from SAS source
2. **Scorer** — 3-component complexity score: base (block weights) + feature (tier-specific patterns) + structure (macros/nesting). Produces the **complexity** axis (LOW/MEDIUM/HIGH), used for sizing — independent of the translation tier.
3. **Classifier** — SQL-first **translation tier** assignment aligned with the conversion skill (Tier 1 SQL → Tier 2 SP → Tier 3 PySpark). A file's tier follows the strict "any-block" rule: any Tier-3 block → Tier 3, else any Tier-2 block → Tier 2, else Tier 1. No proportion thresholds.
4. **Dependency Tracker** — Builds cross-file DAG from dataset CREATES/READS
5. **Reporter** — Generates JSON, Markdown, and Mermaid outputs

**Block counting & tiering are governed by the shared canonical spec**
`../references/block-tiering-spec.md`: macros are flattened (each inner DATA/PROC step counts as
a block), DI Studio / DataFlow boilerplate is excluded from counts and tiering, and all reported
counts (portfolio total, per-file, per-tier) are computed over the same block set so they
reconcile. This is the same logic the `convert-sas-to-snowflake` skill applies, so assessment and
conversion agree on block counts and tiers.
