import math
from typing import List, Dict
from .parser import SASScript, SASBlock, BlockType
from .constants import (
    BOILERPLATE_INDICATORS,
    iter_countable_blocks,
)


class ComplexityScorer:

    COMPLEXITY_WEIGHTS = {
        BlockType.PROC_SQL: 2,
        BlockType.DATA_STEP: 2,
        BlockType.MACRO_DEF: 4,
        BlockType.PROC_SORT: 1,
        BlockType.PROC_APPEND: 1,
        BlockType.PROC_DATASETS: 1,
        BlockType.PROC_MEANS: 2,
        BlockType.PROC_SUMMARY: 2,
        BlockType.PROC_FREQ: 2,
        BlockType.PROC_TRANSPOSE: 3,
        BlockType.PROC_FORMAT: 1,
        BlockType.PROC_IMPORT: 1,
        BlockType.PROC_EXPORT: 1,
        BlockType.PROC_PRINT: 0,
        BlockType.PROC_CONTENTS: 0,
        BlockType.PROC_OTHER: 2,
        BlockType.LET_STATEMENT: 0,
        BlockType.LIBNAME: 0,
        BlockType.COMMENT: 0,
        BlockType.MACRO_CALL: 0,
        BlockType.UNKNOWN: 0,
    }

    TIER3_PATTERNS = {
        'declare hash': 8,
        'call execute': 6,
        'proc reg ': 6,
        'proc glm ': 6,
        'proc logistic ': 6,
        'proc cluster ': 6,
        'proc factor ': 6,
        'proc phreg ': 6,
        'proc lifetest ': 6,
    }

    TIER2_PATTERNS = {
        'call symput': 3,
        'symget': 3,
        'proc transpose': 3,
    }

    TIER1_ADVANCED_PATTERNS = {
        'retain ': 2,
        'array ': 2,
        'merge ': 2,
        'first.': 1,
        'last.': 1,
        '%do ': 1,
        '%if ': 1,
        'infile ': 3,
        'ods ': 1,
    }

    FEATURE_CAP = 3

    def __init__(self, config: Dict = None):
        config = config or {}
        thresholds = config.get('complexity_thresholds', {})
        self.low_max = thresholds.get('low_max', 50)
        self.medium_max = thresholds.get('medium_max', 150)

        volume = config.get('volume_thresholds', {})
        self.volume_low_max = volume.get('low_max', 250)
        self.volume_medium_max = volume.get('medium_max', 1000)

    def score_script(self, script: SASScript) -> Dict:
        is_boilerplate = self._detect_boilerplate(script)
        # Score over the canonical countable-block set (flattened macros,
        # boilerplate + non-code types excluded) so complexity and tier are
        # computed on the same block universe. See constants.iter_countable_blocks.
        business_blocks = list(iter_countable_blocks(script))

        raw_base = sum(self.COMPLEXITY_WEIGHTS.get(b.block_type, 0) for b in business_blocks)
        base_score = (min(raw_base, 50) + max(0, int(math.log2(max(raw_base - 50, 1))))) if raw_base > 50 else raw_base

        feature_score = self._calculate_feature_score(business_blocks, is_boilerplate)
        structure_score = self._calculate_structure_score(script, is_boilerplate)

        overall_score = base_score + feature_score + structure_score
        complexity_level = self._get_complexity_level(overall_score)
        volume_level = self._get_volume_level(script.total_lines)

        return {
            'overall_score': overall_score,
            'complexity_level': complexity_level,
            'volume_level': volume_level,
            'base_score': base_score,
            'feature_score': feature_score,
            'structure_score': structure_score,
            'is_boilerplate': is_boilerplate,
            'business_block_count': len(business_blocks),
        }

    def _detect_boilerplate(self, script: SASScript) -> bool:
        full_content = '\n'.join(b.content for b in script.blocks).lower()
        matches = sum(1 for ind in BOILERPLATE_INDICATORS if ind in full_content)
        return matches >= 3

    def _calculate_feature_score(self, business_blocks: List[SASBlock], is_boilerplate: bool) -> int:
        score = 0
        full_content = '\n'.join(b.content for b in business_blocks).lower()
        boilerplate_discount = 0.5 if is_boilerplate else 1.0

        for pattern, weight in self.TIER3_PATTERNS.items():
            count = min(full_content.count(pattern), self.FEATURE_CAP)
            score += int(count * weight * boilerplate_discount)

        for pattern, weight in self.TIER2_PATTERNS.items():
            count = min(full_content.count(pattern), self.FEATURE_CAP)
            score += int(count * weight * boilerplate_discount)

        for pattern, weight in self.TIER1_ADVANCED_PATTERNS.items():
            count = min(full_content.count(pattern), self.FEATURE_CAP)
            score += count * weight

        return score

    def _calculate_structure_score(self, script: SASScript, is_boilerplate: bool) -> int:
        score = 0

        if is_boilerplate:
            effective_macros = max(len(script.macros) - 5, 0)
            effective_vars = max(len(script.macro_variables) - 10, 0)
        else:
            effective_macros = len(script.macros)
            effective_vars = len(script.macro_variables)

        score += min(effective_macros, 10) * 2
        nested_macros = sum(
            1 for b in script.blocks
            if b.block_type == BlockType.MACRO_DEF and b.sub_blocks
        )
        score += min(nested_macros, 5) * 3
        score += min(effective_vars, 10)
        return score

    def _get_complexity_level(self, score: int) -> str:
        if score <= self.low_max:
            return "LOW"
        elif score <= self.medium_max:
            return "MEDIUM"
        else:
            return "HIGH"

    def _get_volume_level(self, lines: int) -> str:
        if lines <= self.volume_low_max:
            return "LOW"
        elif lines <= self.volume_medium_max:
            return "MEDIUM"
        else:
            return "HIGH"

    def identify_hotspots(self, script: SASScript) -> List[Dict]:
        hotspots = []
        for block in script.blocks:
            if block.complexity_score >= 5:
                hotspots.append({
                    'block_type': block.block_type.value,
                    'start_line': block.start_line,
                    'end_line': block.end_line,
                    'complexity_score': block.complexity_score,
                    'content_preview': block.content[:200] + '...' if len(block.content) > 200 else block.content,
                })
        hotspots.sort(key=lambda x: x['complexity_score'], reverse=True)
        return hotspots[:10]
