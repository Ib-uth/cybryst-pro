#!/usr/bin/env python3
"""
Evaluation script for the Forensic Analyzer outputs.

Computes:
- Artifact extraction Precision/Recall/F1 (exact match on type+value)
- Kill Chain mapping accuracy (percent of artifacts mapped to correct phase)

Usage:
  python evaluate.py --pred outputs/forensic_analysis_sample_report_20250913_014243.json --truth ground_truth/sample_report.json
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple, Set


def load_json(path: str) -> Dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON '{path}': {e}")
        sys.exit(1)


def to_artifact_set(artifacts_obj: Dict) -> Set[Tuple[str, str]]:
    artifacts = artifacts_obj.get('artifacts', []) if isinstance(artifacts_obj, dict) else []
    result: Set[Tuple[str, str]] = set()
    for a in artifacts:
        a_type = (a.get('type') or '').strip().lower()
        a_val = (a.get('value') or '').strip()
        if a_type and a_val:
            result.add((a_type, a_val))
    return result


def to_phase_map(kill_chain_obj: Dict) -> Dict[Tuple[str, str], str]:
    mapping = {}
    phases = kill_chain_obj.get('kill_chain_mapping', []) if isinstance(kill_chain_obj, dict) else []
    for p in phases:
        phase_name = p.get('phase', '')
        for a in p.get('artifacts', []) or []:
            a_type = (a.get('type') or '').strip().lower()
            a_val = (a.get('value') or '').strip()
            if a_type and a_val and phase_name:
                mapping[(a_type, a_val)] = phase_name
    return mapping


def precision_recall_f1(pred: Set[Tuple[str, str]], truth: Set[Tuple[str, str]]) -> Tuple[float, float, float]:
    tp = len(pred & truth)
    fp = len(pred - truth)
    fn = len(truth - pred)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def mapping_accuracy(pred_map: Dict[Tuple[str, str], str], truth_map: Dict[Tuple[str, str], str]) -> float:
    keys = set(truth_map.keys()) & set(pred_map.keys())
    if not keys:
        return 0.0
    correct = sum(1 for k in keys if pred_map.get(k) == truth_map.get(k))
    return correct / len(keys)


def main():
    parser = argparse.ArgumentParser(description="Evaluate Forensic Analyzer outputs")
    parser.add_argument('--pred', required=True, help='Path to predicted analysis JSON')
    parser.add_argument('--truth', required=True, help='Path to ground truth JSON')
    args = parser.parse_args()

    pred = load_json(args.pred)
    truth = load_json(args.truth)

    # Artifact sets
    pred_artifacts = to_artifact_set(pred.get('artifacts', {}))
    truth_artifacts = to_artifact_set(truth.get('artifacts', {}))

    p, r, f1 = precision_recall_f1(pred_artifacts, truth_artifacts)

    # Phase maps
    pred_phase_map = to_phase_map(pred.get('kill_chain_analysis', {}))
    truth_phase_map = to_phase_map(truth.get('kill_chain_analysis', {}))
    acc = mapping_accuracy(pred_phase_map, truth_phase_map)

    print("\n=== Evaluation Results ===")
    print(f"Artifacts - Precision: {p:.3f}  Recall: {r:.3f}  F1: {f1:.3f}")
    print(f"Mapping Accuracy: {acc:.3f}")


if __name__ == '__main__':
    main()


