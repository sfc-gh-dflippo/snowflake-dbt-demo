#!/usr/bin/env python3
"""
SAS Migration Assessment Tool

Standalone CLI that analyzes SAS files and produces:
  - assessment.json (structured metrics per file + portfolio)
  - assessment_report.md (human-readable report)
  - assessment_report.html (self-contained, SCAI-themed HTML report)
  - dependency_dag.mmd (Mermaid diagram of cross-file dependencies)

Usage:
  python assess_sas.py /path/to/sas/files --output ./assessment_output
  python assess_sas.py /path/to/single_file.sas --output ./results
  python assess_sas.py /path/to/sas/ --config custom_config.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

from sas_analyzer import SASParser, ComplexityScorer, TierClassifier, DependencyTracker, AssessmentReporter


def find_sas_files(source: str) -> list:
    source_path = Path(source)
    if source_path.is_file() and source_path.suffix.lower() == '.sas':
        return [source_path]
    elif source_path.is_dir():
        files = sorted(source_path.rglob('*.sas'))
        return files
    else:
        print(f"Error: '{source}' is not a .sas file or directory.", file=sys.stderr)
        sys.exit(1)


def load_config(config_path: str = None) -> dict:
    default_config = {
        'complexity_thresholds': {
            'low_max': 50,
            'medium_max': 150,
        },
        'volume_thresholds': {
            'low_max': 250,
            'medium_max': 1000,
        },
    }
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            user_config = json.load(f)
        for key in default_config:
            if key in user_config:
                default_config[key].update(user_config[key])
    return default_config


def main():
    ap = argparse.ArgumentParser(description='SAS Migration Assessment Tool')
    ap.add_argument('source', help='Path to .sas file or directory containing .sas files')
    ap.add_argument('--output', '-o', default='./assessment_output', help='Output directory for results')
    ap.add_argument('--config', '-c', help='Path to config.json with custom thresholds')
    ap.add_argument('--format', choices=['json', 'md', 'html', 'all'], default='all', help='Output format')
    args = ap.parse_args()

    config = load_config(args.config)

    sas_files = find_sas_files(args.source)
    if not sas_files:
        print("No .sas files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(sas_files)} SAS file(s) to analyze...")

    parser = SASParser()
    scorer = ComplexityScorer(config)
    classifier = TierClassifier()
    dep_tracker = DependencyTracker()
    reporter = AssessmentReporter(config)

    scripts = []
    scores = []
    classifications = []
    file_analyses = {}

    for sas_file in sas_files:
        try:
            content = sas_file.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  Warning: Could not read {sas_file}: {e}", file=sys.stderr)
            continue

        script = parser.parse(content, filename=sas_file.name)
        score = scorer.score_script(script)
        classification = classifier.classify_file(script)
        deps = dep_tracker.analyze_file(script)

        scripts.append(script)
        scores.append(score)
        classifications.append(classification)
        file_analyses[script.filename] = deps

        parser = SASParser()

    if not scripts:
        print("Error: No files could be parsed.", file=sys.stderr)
        sys.exit(1)

    graph = dep_tracker.build_cross_file_graph(file_analyses)
    graph['data_source_inventory'] = dep_tracker.build_source_inventory(file_analyses)
    mermaid_str = dep_tracker.generate_mermaid_with_externals(graph, file_analyses)

    assessment = reporter.generate_assessment(scripts, scores, classifications, graph, file_analyses)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ('json', 'all'):
        json_path = output_dir / 'assessment.json'
        reporter.write_json(assessment, str(json_path))
        print(f"  Written: {json_path}")

    if args.format in ('md', 'all'):
        md_path = output_dir / 'assessment_report.md'
        reporter.write_markdown(assessment, str(md_path))
        print(f"  Written: {md_path}")

    if args.format in ('html', 'all'):
        html_path = output_dir / 'assessment_report.html'
        reporter.write_html(assessment, mermaid_str, str(html_path))
        print(f"  Written: {html_path}")

    dag_path = output_dir / 'dependency_dag.mmd'
    reporter.write_mermaid_dag(mermaid_str, str(dag_path))
    print(f"  Written: {dag_path}")

    total = len(scripts)
    tier_dist = assessment['portfolio_summary']['tier_distribution']
    complexity_dist = assessment['portfolio_summary']['complexity_distribution']

    print(f"\n{'='*60}")
    print(f"  ASSESSMENT COMPLETE: {total} files analyzed")
    print(f"{'='*60}")
    print(f"  Tier 1 (SQL):          {tier_dist.get('TIER_1_SQL', 0):>4} ({tier_dist.get('TIER_1_SQL', 0)/total*100:.0f}%)")
    print(f"  Tier 2 (Stored Proc):  {tier_dist.get('TIER_2_SP', 0):>4} ({tier_dist.get('TIER_2_SP', 0)/total*100:.0f}%)")
    print(f"  Tier 3 (PySpark):      {tier_dist.get('TIER_3_PYSPARK', 0):>4} ({tier_dist.get('TIER_3_PYSPARK', 0)/total*100:.0f}%)")
    print(f"  ---")
    print(f"  Complexity LOW:        {complexity_dist.get('LOW', 0):>4} ({complexity_dist.get('LOW', 0)/total*100:.0f}%)")
    print(f"  Complexity MEDIUM:     {complexity_dist.get('MEDIUM', 0):>4} ({complexity_dist.get('MEDIUM', 0)/total*100:.0f}%)")
    print(f"  Complexity HIGH:       {complexity_dist.get('HIGH', 0):>4} ({complexity_dist.get('HIGH', 0)/total*100:.0f}%)")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
