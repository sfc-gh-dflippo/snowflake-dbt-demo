"""Shared constants and the canonical countable-block iterator.

Single source of truth for block counting so the portfolio total, per-file count,
and per-tier distribution are always computed over the SAME set of blocks and
reconcile. Mirrors `references/block-tiering-spec.md` (Section 1).
"""

from typing import Iterator

from .parser import SASScript, SASBlock, BlockType


# DI Studio / DataFlow scaffolding macro names — excluded from counts and tiering.
BOILERPLATE_MACRO_NAMES = frozenset({
    'rcset', 'rcsetds', 'etls_startperformancestats', 'etls_setdebug',
    'etls_recordcount', 'etls_endperformancestats', 'etls_recordtable',
    'etls_getrecordcount', 'etls_jobstatus', 'etls_logerror',
})

# File-level boilerplate indicators (used by the complexity scorer's discount).
BOILERPLATE_INDICATORS = (
    'etls_',
    'sas data integration studio',
    '%macro etls_',
    '%macro rcset',
    'perfinit',
    'log4sas',
    'armsubsys',
    '%macro etls_startperformancestats',
)

# Block types that are never counted as code blocks.
SKIP_TYPES = frozenset({
    BlockType.LET_STATEMENT,
    BlockType.COMMENT,
    BlockType.LIBNAME,
    BlockType.MACRO_CALL,
})


def is_boilerplate_macro(block: SASBlock) -> bool:
    """True if a MACRO_DEF block is DI Studio / DataFlow scaffolding."""
    content_lower = block.content.lower()
    return any(f'%macro {name}' in content_lower for name in BOILERPLATE_MACRO_NAMES)


def iter_countable_blocks(script: SASScript) -> Iterator[SASBlock]:
    """Canonical countable-block set for a parsed SAS file.

    Every block count reported by the assessment (portfolio total, per-file
    count, per-tier distribution) MUST iterate this generator so the numbers
    reconcile and match how the conversion skill enumerates blocks.

    The parser surfaces each DATA/PROC step at the TOP level even when it lives
    inside a macro (its extraction regexes scan the whole file). So macros are
    already "flattened": we count those top-level steps directly and never
    descend into ``sub_blocks`` (that would double-count). We then:

    - skip non-code types (LET/COMMENT/LIBNAME/MACRO_CALL);
    - skip a MACRO_DEF wrapper when it has inner blocks (they are counted at the
      top level); count the wrapper once only for a pure macro-language macro
      with no DATA/PROC step inside;
    - exclude boilerplate macros AND every block whose line falls within a
      boilerplate macro's range (its inner steps also appear at the top level).

    See ``references/block-tiering-spec.md`` Section 1.
    """
    boilerplate_ranges = [
        (b.start_line, b.end_line)
        for b in script.blocks
        if b.block_type == BlockType.MACRO_DEF and is_boilerplate_macro(b)
    ]

    def within_boilerplate(block: SASBlock) -> bool:
        return any(lo <= block.start_line <= hi for lo, hi in boilerplate_ranges)

    for block in script.blocks:
        if block.block_type in SKIP_TYPES:
            continue

        if block.block_type == BlockType.MACRO_DEF:
            if is_boilerplate_macro(block):
                continue
            if block.sub_blocks:
                # Inner DATA/PROC steps are already surfaced at the top level;
                # skip the wrapper to avoid double counting.
                continue
            # Pure macro-language logic (no DATA/PROC inside) counts once.
            yield block
            continue

        if within_boilerplate(block):
            # A DATA/PROC step belonging to a boilerplate macro, surfaced at the
            # top level by the parser's global extraction.
            continue

        yield block

