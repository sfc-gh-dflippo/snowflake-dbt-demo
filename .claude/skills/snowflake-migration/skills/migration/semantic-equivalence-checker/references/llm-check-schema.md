# `llm_check.json` — schema and rules

Written by the Section and Pipeline Analysis step. Every claim must be traceable to a line a reviewer can open.

## Schema

```json
{
  "workflow": "wf_foo",
  "xml_path": "path/to/FOLDER_wf_FOO.xml",
  "dbt_path": "path/to/models/GROUP/FOO_wf/PRIMARY.sql",
  "stage3_verdict": "PASS|FAIL|PARTIAL",
  "section_reviews": [
    {
      "section": "source_tables|target_table|load_strategy|column_list|pre_hooks|post_hooks|transform_logic",
      "stage2_status": "PASS|FAIL|PARTIAL",
      "stage3_status": "PASS|FAIL|PARTIAL",
      "is_false_positive": true,
      "is_false_equivalence": false,
      "explanation": "Why this determination was made",
      "citations": [
        {"file": "xml", "lines": "50", "content_summary": "SQ Override referencing WI_ staging"},
        {"file": "TEMP_WI_SHIP_COST_INTL", "lines": "16-30", "content_summary": "sibling reads the same source"}
      ]
    }
  ],
  "unresolved_analysis": [
    {
      "item_index": 0,
      "section": "pre_sql|post_sql|transform_logic",
      "original_reason": "verbatim from unresolved.json",
      "equivalence": "EQUIVALENT|NOT_EQUIVALENT|INTENTIONAL_CHANGE|PLATFORM_HOUSEKEEPING",
      "resolved_in": "<sibling_name>|primary|not_found",
      "explanation": "Why this determination was made",
      "citations": [
        {"file": "xml", "lines": "423-435", "content_summary": "Pre SQL INSERT stmt"},
        {"file": "SOME_SIBLING_MODEL", "lines": "12-45", "content_summary": "sibling post_hook INSERT"}
      ],
      "aspect_comparison": [
        {"aspect": "target_table", "infa": "$$STGDB.WI_X", "dbt": "MY_DB.WI.WI_X", "match": true},
        {"aspect": "filter_conditions", "infa": "SHIP_TYPE = 'INTERNATIONAL'", "dbt": "absent", "match": false}
      ]
    }
  ],
  "verdict": {
    "overall": "PASS|FAIL|PARTIAL",
    "confidence": "HIGH|MEDIUM|LOW",
    "claims": [
      {
        "statement": "The claim being made",
        "sources": [{"file": "xml", "lines": "423-435"}, {"file": "dbt_primary", "lines": "12-45"}],
        "reasoning": "Why this claim holds — specific structural evidence"
      }
    ]
  },
  "pipeline_analysis": {
    "count": 3,
    "variants": ["DOMESTIC", "INTERNATIONAL", "SUMMARY"],
    "coverage": [
      {
        "variant": "INTERNATIONAL",
        "covered_in_dbt": true,
        "model": "TEMP_WI_SHIP_COST_INTL",
        "citations": [{"file": "TEMP_WI_SHIP_COST_INTL", "lines": "17", "content_summary": "'INTERNATIONAL' AS SHIP_TYPE"}],
        "notes": "label present but the source predicate is absent"
      }
    ],
    "missing_logic": ["Pipeline logic absent from every model; empty when all covered"]
  }
}
```

`pipeline_analysis` is required whenever `check.json` carries `pipeline_coverage` or the `_wf` directory holds more than one model.

## Field definitions

`equivalence`:

| Value | Meaning |
|---|---|
| `EQUIVALENT` | Same logic, different syntax — a platform rewrite |
| `NOT_EQUIVALENT` | Genuine logic difference: a bug or an undocumented divergence |
| `INTENTIONAL_CHANGE` | Deliberate conversion decision, e.g. adding an explicit DELETE |
| `PLATFORM_HOUSEKEEPING` | Platform-specific operations with no data effect, e.g. COLLECT_STATS |

`resolved_in` — **where you found the logic.** `primary` if in `dbt_primary.sql`, the sibling's name if in a sibling, `not_found` if nowhere. `not_found` combined with `EQUIVALENT` is a contradiction and the critic will flag it.

`is_false_equivalence` — set on a section the deterministic pass marked `PASS` that is not actually equivalent. Rare, and the only reason to review a passing section at all.

This is a different field from the critic's `false_equivalence` issue type, and the two point opposite ways. `is_false_equivalence` here is an equivalence accepted that is not real. `false_equivalence` in `llm_critic.json` is a difference claimed that is not real, because the logic was sitting in a sibling all along.

When logic genuinely appears nowhere, say so in exactly this form so the count is on the record:

> NOT FOUND IN ANY MODEL (primary + N siblings searched)

`N` comes from `dbt_siblings.json`. Writing the sentence requires having done the search, which is the point of fixing the wording.

`citations[].file` — one of:

| Value | Resolves to |
|---|---|
| `xml` | the top-level `xml_path` |
| `dbt_primary` | `dbt_primary.sql` in the reports directory, Jinja already resolved |
| `<sibling_name>` | that entry's `name` in `dbt_siblings.json` |

Do not cite `dbt` — it is ambiguous once siblings exist. Do not cite the original `.sql` files; cite the resolved artifacts, so a reviewer sees the identifiers you saw.

`citations[].lines` — a single line or a range, e.g. `"423"` or `"12-45"`.

`confidence`: `HIGH` when every item was verified with no ambiguity; `MEDIUM` when some required interpretation; `LOW` when significant uncertainty remains.

## Citation rules

1. Every `unresolved_analysis` item carries at least one citation per side where both sides have content.
2. Every `section_reviews` item cites the lines supporting its call.
3. Every `verdict.claims[]` entry carries `sources` a reviewer can open.
4. Where one side is genuinely empty — "no matching DELETE on the Informatica side" — cite only the side with content.
5. Treat the `evidence` fields in `check.json` as starting points, then confirm against the file.
6. Re-read the exact line after writing its number. A wrong line number invalidates the claim built on it.
7. Cite the precise line: the line with the `FROM` keyword, not the CTE or query start; the `SET` line, not the statement head.
8. Before writing that the deterministic pass matched or classified something, read `matched_pairs` in the relevant `check.json` hook section. When it is empty, say the pass could not match the pair — do not attribute a result it never produced.

## Completeness requirements

1. **Every unresolved item gets an entry.** `N` items in `unresolved.json` means exactly `N` entries in `unresolved_analysis`.
2. **Search every sibling before calling anything missing.** For any section or item you are about to mark a true failure, state which models you searched. The deterministic pass reads only the primary, so "missing" without a sibling search is not a finding — it is the single most common way this analysis goes wrong.
3. **Trace post-hook chains.** Where dbt writes through a temp table and a post_hook merge, follow temp → final and record which hook corresponds to which piece of Informatica logic. `__THIS__` is the model's own temp table.
4. **Name architectural restructuring.** Where one Informatica pipeline becomes a temp-plus-merge pair, say so and establish equivalence of the combined chain, not of either half.
5. **Every FAIL or PARTIAL section gets a `section_reviews` entry**, even when its items already appear in `unresolved_analysis`.
6. **Account for every pipeline.** With N pipelines in the XML, `pipeline_analysis.coverage` has N entries, each naming the model that implements it.
7. **Enumerate platform function equivalences** under `aspect_comparison` with `"aspect": "platform_functions"`. See [known-false-positives.md](known-false-positives.md).
8. **Audit the XML for uncompared logic.** `check.json` reports only the seven comparison sections — it carries no inventory of Informatica transformations, so the deterministic pass can be entirely green about logic it never looked at. Read the XML yourself and confirm each of these has a counterpart in the primary, a sibling, or a hook:

   | XML element | Look for |
   |---|---|
   | `TRANSFORMATION TYPE="Filter"` → `Filter Condition` | a `WHERE` or `QUALIFY` predicate |
   | `TRANSFORMATION TYPE="Lookup Procedure"` → `Lookup condition`, `Lookup Sql Override` | a join or subquery against the same table |
   | `TRANSFORMATION TYPE="Expression"` → `TRANSFORMFIELD EXPRESSION` | the same expression on the corresponding output column |
   | `TRANSFORMATION TYPE="Joiner"` → `Join Condition` | an equivalent join |
   | `TRANSFORMATION TYPE="Aggregator"` → group-by ports | the same `GROUP BY` grain |
   | `TRANSFORMATION TYPE="Router"` → group conditions | equivalent branching |
   | SQ Override `WHERE` predicates | the same predicate, in the model implementing that pipeline |

   A Filter transformation and an SQ `WHERE` predicate are the highest-risk cases: nothing in `check.json` reports them, `transform_logic` compares only column expressions, and a dropped predicate changes row counts without changing any column. Cite the XML line of every predicate you checked and say where it landed — or that it did not land anywhere.

   Anything with no counterpart belongs in the verdict's reasons with impact `BLOCKING` when it changes data, or `SKIPPED` when you could not determine where it went. Silence about uncompared logic reads as a pass, which is the one error a reviewer of this file cannot catch.
