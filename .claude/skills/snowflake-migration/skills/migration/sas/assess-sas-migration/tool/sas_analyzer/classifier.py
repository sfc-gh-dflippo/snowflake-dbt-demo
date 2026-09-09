from typing import Dict
from .parser import SASScript, SASBlock, BlockType
from .constants import iter_countable_blocks


class TierClassifier:

    TIER3_TRIGGERS = [
        ('declare hash', 'HASH objects - no SQL equivalent'),
        ('call execute', 'CALL EXECUTE - dynamic code generation'),
    ]

    # Statistical-modeling PROCs -> Tier 3 (PySpark/SCOS). Canonical list, kept in
    # sync with references/block-tiering-spec.md and the conversion skill.
    TIER3_STAT_PROCS = [
        'proc reg', 'proc glm', 'proc logistic', 'proc cluster',
        'proc factor', 'proc phreg', 'proc lifetest', 'proc surveyselect',
        'proc mixed', 'proc genmod', 'proc nlmixed',
    ]

    # External DB engines -> LOW confidence. Canonical union list.
    EXTERNAL_ENGINES = [
        'sqlsvr', 'mssql', 'sql server', 'oracle', 'teradata',
        'odbc', 'oledb', 'db2', 'postgres', 'mysql', 'dsn=',
    ]

    def classify_block(self, block: SASBlock) -> Dict:
        content_lower = block.content.lower()

        for trigger, reason in self.TIER3_TRIGGERS:
            if trigger in content_lower:
                return {'tier': 3, 'label': 'TIER_3_PYSPARK', 'reason': reason, 'confidence': 'HIGH'}

        if ('do until' in content_lower or 'do while' in content_lower):
            if 'symput' in content_lower or content_lower.count('call ') > 2:
                return {'tier': 3, 'label': 'TIER_3_PYSPARK', 'reason': 'DO loop with external state', 'confidence': 'HIGH'}

        for proc in self.TIER3_STAT_PROCS:
            if proc in content_lower:
                return {'tier': 3, 'label': 'TIER_3_PYSPARK', 'reason': f'Statistical modeling: {proc}', 'confidence': 'HIGH'}

        if 'retain ' in content_lower and 'first.' in content_lower:
            if '= 0' in content_lower or '= .' in content_lower:
                return {'tier': 2, 'label': 'TIER_2_SP', 'reason': 'RETAIN with conditional reset', 'confidence': 'HIGH'}

        if ('first.' in content_lower or 'last.' in content_lower):
            if content_lower.count('output ') > 1:
                return {'tier': 2, 'label': 'TIER_2_SP', 'reason': 'FIRST./LAST. with multiple OUTPUT', 'confidence': 'HIGH'}

        if content_lower.count('output ') > 1 and 'output;' not in content_lower:
            return {'tier': 2, 'label': 'TIER_2_SP', 'reason': 'Multiple OUTPUT datasets', 'confidence': 'MEDIUM'}

        # Procedural IF/THEN/ELSE and SELECT/WHEN branching only exists in DATA
        # steps. A PROC SQL CASE WHEN is pure SQL (Tier 1) no matter how many
        # WHEN clauses, so gate this rule to DATA steps. See block-tiering-spec.md.
        if block.block_type == BlockType.DATA_STEP and (
                content_lower.count('if ') > 5 or content_lower.count('when ') > 5):
            return {'tier': 2, 'label': 'TIER_2_SP', 'reason': 'Complex branching (>5 IF/WHEN) in DATA step', 'confidence': 'MEDIUM'}

        dml_count = sum(1 for kw in ['delete ', 'insert ', 'update '] if kw in content_lower)
        if dml_count >= 3:
            return {'tier': 2, 'label': 'TIER_2_SP', 'reason': '3+ sequential DML operations', 'confidence': 'MEDIUM'}

        confidence = self._assess_confidence(content_lower)
        return {'tier': 1, 'label': 'TIER_1_SQL', 'reason': 'SQL-translatable', 'confidence': confidence}

    def _assess_confidence(self, content_lower: str) -> str:
        if content_lower.count('%macro') > 2:
            return 'LOW'
        if '%include' in content_lower and '&' in content_lower:
            return 'LOW'
        if any(eng in content_lower for eng in self.EXTERNAL_ENGINES):
            return 'LOW'
        if 'intck' in content_lower or 'intnx' in content_lower or 'datepart' in content_lower:
            return 'MEDIUM'
        if 'notsorted' in content_lower:
            return 'MEDIUM'
        return 'HIGH'

    def classify_file(self, script: SASScript) -> Dict:
        block_classifications = []
        tier_counts = {1: 0, 2: 0, 3: 0}
        confidence_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

        for block in iter_countable_blocks(script):
            classification = self.classify_block(block)
            block_classifications.append({
                'block_type': block.block_type.value,
                'start_line': block.start_line,
                'end_line': block.end_line,
                **classification
            })
            tier_counts[classification['tier']] += 1
            confidence_counts[classification['confidence']] += 1

        # Strict "any-block" rule: the file's tier is driven by its most demanding
        # block, matching the conversion skill (one Tier-3 block -> notebook).
        # See references/block-tiering-spec.md Section 3.
        if tier_counts[3] > 0:
            primary_tier = 'TIER_3_PYSPARK'
        elif tier_counts[2] > 0:
            primary_tier = 'TIER_2_SP'
        else:
            primary_tier = 'TIER_1_SQL'

        if confidence_counts['LOW'] > 0:
            overall_confidence = 'LOW'
        elif confidence_counts['MEDIUM'] > 0:
            overall_confidence = 'MEDIUM'
        else:
            overall_confidence = 'HIGH'

        return {
            'primary_tier': primary_tier,
            'confidence': overall_confidence,
            'tier_distribution': {
                'TIER_1_SQL': tier_counts[1],
                'TIER_2_SP': tier_counts[2],
                'TIER_3_PYSPARK': tier_counts[3],
            },
            'block_classifications': block_classifications,
        }
