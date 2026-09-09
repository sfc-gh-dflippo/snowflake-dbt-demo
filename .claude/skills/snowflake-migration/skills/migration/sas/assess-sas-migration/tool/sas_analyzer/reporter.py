import json
from datetime import datetime
from typing import List, Dict
from collections import Counter
from .parser import SASScript
from .constants import iter_countable_blocks


class AssessmentReporter:

    def __init__(self, config: Dict = None):
        self.config = config or {}

    def generate_assessment(self, scripts: List[SASScript], scores: List[Dict],
                            classifications: List[Dict], graph: Dict,
                            file_analyses: Dict[str, Dict]) -> Dict:
        portfolio = self._build_portfolio_summary(scripts, scores, classifications)
        files = self._build_file_details(scripts, scores, classifications, file_analyses)

        return {
            'metadata': {
                'tool_version': '1.0.0',
                'generated_at': datetime.now().isoformat(),
                'total_files': len(scripts),
                'config': self.config,
            },
            'portfolio_summary': portfolio,
            'files': files,
            'dependency_graph': graph,
        }

    def _build_portfolio_summary(self, scripts: List[SASScript], scores: List[Dict],
                                  classifications: List[Dict]) -> Dict:
        total_lines = sum(s.total_lines for s in scripts)

        # All block counts use the ONE canonical countable-block set so the
        # portfolio total, per-file counts, and tier distribution reconcile.
        total_blocks = sum(1 for s in scripts for _ in iter_countable_blocks(s))

        complexity_dist = Counter(s['complexity_level'] for s in scores)
        volume_dist = Counter(s['volume_level'] for s in scores)
        tier_dist = Counter(c['primary_tier'] for c in classifications)

        block_type_dist = Counter()
        for s in scripts:
            for b in iter_countable_blocks(s):
                block_type_dist[b.block_type.value] += 1

        func_usage = self._get_function_usage(scripts)

        return {
            'total_lines': total_lines,
            'total_blocks': total_blocks,
            'complexity_distribution': dict(complexity_dist),
            'volume_distribution': dict(volume_dist),
            'tier_distribution': dict(tier_dist),
            'block_type_distribution': dict(block_type_dist),
            'function_usage': dict(sorted(func_usage.items(), key=lambda x: -x[1])[:20]),
        }

    def _build_file_details(self, scripts: List[SASScript], scores: List[Dict],
                            classifications: List[Dict], file_analyses: Dict[str, Dict]) -> List[Dict]:
        files = []
        for script, score, classification in zip(scripts, scores, classifications):
            deps = file_analyses.get(script.filename, {'creates': [], 'reads': [], 'external_sources': []})
            files.append({
                'filename': script.filename,
                'lines': script.total_lines,
                'blocks': sum(1 for _ in iter_countable_blocks(script)),
                'complexity_score': score['overall_score'],
                'complexity_level': score['complexity_level'],
                'volume_level': score['volume_level'],
                'primary_tier': classification['primary_tier'],
                'confidence': classification['confidence'],
                'tier_distribution': classification['tier_distribution'],
                'is_boilerplate': score['is_boilerplate'],
                'dependencies': {
                    'creates': deps['creates'],
                    'reads': deps['reads'],
                },
                'external_sources': deps['external_sources'],
            })
        return files

    def _get_function_usage(self, scripts: List[SASScript]) -> Dict[str, int]:
        import re
        function_counts: Counter = Counter()
        common_functions = [
            'INPUT', 'PUT', 'SUBSTR', 'TRIM', 'COMPRESS', 'UPCASE', 'LOWCASE',
            'SUM', 'MEAN', 'COUNT', 'MAX', 'MIN', 'ROUND', 'ABS',
            'INTCK', 'INTNX', 'TODAY', 'DATETIME', 'YEAR', 'MONTH', 'DAY',
            'CAT', 'CATS', 'CATX', 'SCAN', 'INDEX', 'TRANWRD',
            'COALESCE', 'IFN', 'IFC', 'MISSING', 'MDY', 'DATEPART',
        ]
        for script in scripts:
            full_content = '\n'.join(b.content for b in script.blocks).upper()
            for func in common_functions:
                count = len(re.findall(rf'\b{func}\s*\(', full_content))
                if count > 0:
                    function_counts[func] += count
        return dict(function_counts)

    def write_json(self, assessment: Dict, output_path: str):
        with open(output_path, 'w') as f:
            json.dump(assessment, f, indent=2, default=str)

    def write_markdown(self, assessment: Dict, output_path: str):
        md = self._render_markdown(assessment)
        with open(output_path, 'w') as f:
            f.write(md)

    def write_mermaid_dag(self, mermaid_str: str, output_path: str):
        with open(output_path, 'w') as f:
            f.write(mermaid_str)

    def write_html(self, assessment: Dict, mermaid_str: str, output_path: str):
        from .html_report import render_html
        with open(output_path, 'w') as f:
            f.write(render_html(assessment, mermaid_str))

    def _render_markdown(self, assessment: Dict) -> str:
        meta = assessment['metadata']
        portfolio = assessment['portfolio_summary']
        files = assessment['files']

        lines = []
        lines.append('# SAS Migration Assessment Report')
        lines.append('')
        lines.append(f'**Generated:** {meta["generated_at"]}')
        lines.append(f'**Total Files:** {meta["total_files"]}')
        lines.append('')

        lines.append('## Portfolio Summary')
        lines.append('')
        lines.append(f'| Metric | Value |')
        lines.append(f'|--------|-------|')
        lines.append(f'| Total SAS Files | {meta["total_files"]} |')
        lines.append(f'| Total Lines | {portfolio["total_lines"]:,} |')
        lines.append(f'| Total Blocks | {portfolio["total_blocks"]:,} |')
        lines.append('')

        lines.append('## Complexity Distribution')
        lines.append('')
        lines.append('| Level | Count | Percentage |')
        lines.append('|-------|-------|------------|')
        total = meta['total_files']
        for level in ['LOW', 'MEDIUM', 'HIGH']:
            count = portfolio['complexity_distribution'].get(level, 0)
            pct = (count / total * 100) if total > 0 else 0
            lines.append(f'| {level} | {count} | {pct:.1f}% |')
        lines.append('')

        lines.append('## Volume Distribution')
        lines.append('')
        lines.append('| Level | Count | Percentage |')
        lines.append('|-------|-------|------------|')
        for level in ['LOW', 'MEDIUM', 'HIGH']:
            count = portfolio['volume_distribution'].get(level, 0)
            pct = (count / total * 100) if total > 0 else 0
            lines.append(f'| {level} | {count} | {pct:.1f}% |')
        lines.append('')

        lines.append('## Translation Tier Distribution')
        lines.append('')
        lines.append('_Translation tier is the migration approach per file (independent of the '
                     'complexity score above). A file is Tier 3 if it has any Tier-3 block, else '
                     'Tier 2 if any Tier-2 block, else Tier 1 — matching the conversion skill._')
        lines.append('')
        lines.append('| Tier | Count | Percentage | Approach |')
        lines.append('|------|-------|------------|----------|')
        tier_map = {
            'TIER_1_SQL': ('Tier 1', 'Pure SQL (CTAS + CTEs + Window Functions)'),
            'TIER_2_SP': ('Tier 2', 'Snowflake Stored Procedures'),
            'TIER_3_PYSPARK': ('Tier 3', 'PySpark/SCOS Notebook'),
        }
        for tier_key, (label, approach) in tier_map.items():
            count = portfolio['tier_distribution'].get(tier_key, 0)
            pct = (count / total * 100) if total > 0 else 0
            lines.append(f'| {label} | {count} | {pct:.1f}% | {approach} |')
        lines.append('')

        lines.append('## Block Type Distribution')
        lines.append('')
        lines.append('| Block Type | Count |')
        lines.append('|-----------|-------|')
        for btype, count in sorted(portfolio['block_type_distribution'].items(), key=lambda x: -x[1]):
            lines.append(f'| {btype} | {count} |')
        lines.append('')

        if portfolio.get('function_usage'):
            lines.append('## Top SAS Functions Used')
            lines.append('')
            lines.append('| Function | Occurrences |')
            lines.append('|----------|-------------|')
            for func, count in list(portfolio['function_usage'].items())[:15]:
                lines.append(f'| {func} | {count} |')
            lines.append('')

        lines.append('## Complexity x Volume Matrix')
        lines.append('')
        matrix = {}
        for f in files:
            key = (f['complexity_level'], f['volume_level'])
            matrix[key] = matrix.get(key, 0) + 1
        lines.append('|  | Low Volume | Medium Volume | High Volume |')
        lines.append('|--|-----------|---------------|-------------|')
        for cl in ['LOW', 'MEDIUM', 'HIGH']:
            row = f'| {cl} Complexity |'
            for vl in ['LOW', 'MEDIUM', 'HIGH']:
                row += f' {matrix.get((cl, vl), 0)} |'
            lines.append(row)
        lines.append('')

        lines.append('## Per-File Details')
        lines.append('')
        lines.append('| File | Lines | Blocks | Score | Complexity | Volume | Tier | Confidence |')
        lines.append('|------|-------|--------|-------|------------|--------|------|------------|')
        sorted_files = sorted(files, key=lambda x: x['complexity_score'], reverse=True)
        for f in sorted_files:
            lines.append(
                f'| {f["filename"]} | {f["lines"]} | {f["blocks"]} | '
                f'{f["complexity_score"]} | {f["complexity_level"]} | {f["volume_level"]} | '
                f'{f["primary_tier"]} | {f["confidence"]} |'
            )
        lines.append('')

        inventory = assessment['dependency_graph'].get('data_source_inventory', [])
        if inventory:
            lines.append('## Data Source Inventory')
            lines.append('')
            lines.append('External libraries the module reads from or writes to, aggregated by library '
                         '(local WORK, unqualified, and SAS dictionary datasets excluded):')
            lines.append('')
            lines.append('| Source | Engine / Type | Tables | Direction |')
            lines.append('|--------|---------------|-------:|-----------|')
            for row in inventory:
                lines.append(f'| {row["source"]} | {row["engine"]} | {row["tables"]} | {row["direction"]} |')
            lines.append('')

        ext_inputs = assessment['dependency_graph'].get('external_inputs', [])
        if ext_inputs:
            lines.append('## External Dependencies')
            lines.append('')
            lines.append('Tables referenced but not created by any file in scope:')
            lines.append('')
            for ext in ext_inputs[:30]:
                lines.append(f'- `{ext}`')
            lines.append('')

        graph = assessment['dependency_graph']
        if graph.get('edges'):
            lines.append('## Dependency DAG')
            lines.append('')
            lines.append('See `dependency_dag.mmd` for the full Mermaid diagram.')
            lines.append('')
            lines.append(f'- **Files:** {len(graph["nodes"])}')
            lines.append(f'- **Dependencies:** {len(graph["edges"])}')
            lines.append(f'- **External Inputs:** {len(graph.get("external_inputs", []))}')
            lines.append('')

        return '\n'.join(lines)
