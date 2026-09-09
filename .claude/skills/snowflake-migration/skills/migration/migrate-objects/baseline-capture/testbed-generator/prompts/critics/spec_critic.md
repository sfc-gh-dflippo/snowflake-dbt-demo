# spec_critic — value enrichment critic

Scope: `inferred_enum`, `branch_values`, `must_include`, `null_fraction_override` (per-object; per
column). The backbone already verbatim-checked literals against `source_evidence`, applied the
declared-enum ACCEPT-and-skip, and range-checked fractions. Judge only the semantic residue below, then
emit your verdict per **verdict-contract.md**.

## Per-type residue

### inferred_enum — is the domain complete and genuinely enum-like?
The backbone already rejected invented literals and skipped declared enums.
- The domain **misses** a discriminating branch literal that appears in the source → **REVISE**, mode `b`.
- A listed literal **positively contradicts** a declared domain (rare) → **REJECT**, mode `a`, citation
  `declared_enum`.
- Complete and enum-like → **ACCEPT**.

### branch_values — did it capture ALL discriminating branch literals?
- A shallow subset (source branches on more literals than listed) → **REVISE**, mode `b`.
- Complete → **ACCEPT**.

### must_include — are these values the source actually requires?
- A value that **positively contradicts** a source predicate/domain → **REJECT**, mode `a` (cite the span).
- Unsupported-but-not-contradictory (source doesn't require it) → **REVISE**, mode `b`.
- Required by the source → **ACCEPT**.

### null_fraction_override — does the source justify overriding nullability?
- No justification in the source (procs don't treat the column as optional) → **REVISE**, mode `b`.
- Justified → **ACCEPT**.
