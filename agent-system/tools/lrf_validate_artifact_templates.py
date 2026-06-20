#!/usr/bin/env python3
"""Validate LRF artifact templates and answer-free packet-like artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TEMPLATE_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "lrf-answer-free-packet-template.json": (
        "packet_id",
        "packet_version",
        "created_at",
        "source_docs",
        "client_mirror_first",
        "app_context",
        "owner_referent",
        "bounded_window",
        "instrument",
        "known_at_boundary",
        "source_refs",
        "data_family_status",
        "lrf_object_candidates",
        "key_zone_candidates",
        "range_candidates",
        "sweep_or_fake_breakout_candidates",
        "trade_hypothesis_field_slots",
        "missing_evidence",
        "blocker_classification",
        "forbidden_future_fields_scan",
        "attestations",
    ),
    "lrf-blind-hypothesis-output-template.json": (
        "task_id",
        "role_id",
        "input_packet_ref",
        "input_packet_hash",
        "observed_fact",
        "hypothesis",
        "premise",
        "setup_context",
        "entry_trigger",
        "entry_price_rule",
        "invalidation_condition",
        "stop_rule",
        "exit_or_target_rule",
        "cancel_condition",
        "no_entry_condition",
        "time_stop",
        "cost_model_ref",
        "evidence_refs",
        "missing_evidence",
        "blocker_classification",
        "confidence_label",
        "forbidden_claim_attestation",
    ),
    "lrf-challenge-output-template.json": (
        "task_id",
        "role_id",
        "input_packet_ref",
        "input_packet_hash",
        "hypothesis_output_ref",
        "hypothesis_output_hash",
        "challenged_claims",
        "supported_challenges",
        "unsupported_or_ambiguous_challenges",
        "missing_evidence",
        "blocker_classification",
        "overclaim_risk",
        "confidence_label",
        "forbidden_claim_attestation",
    ),
    "lrf-reviewer-discipline-output-template.json": (
        "task_id",
        "role_id",
        "input_packet_ref",
        "input_packet_hash",
        "hypothesis_output_ref",
        "hypothesis_output_hash",
        "challenge_output_ref",
        "challenge_output_hash",
        "packet_ref_check",
        "hypothesis_field_completeness",
        "challenge_field_completeness",
        "answer_leakage_check",
        "unsupported_ref_check",
        "overclaim_check",
        "forbidden_claim_check",
        "reviewer_verdict",
        "missing_evidence",
        "blocker_classification",
        "boundary_attestation",
    ),
    "lrf-run-artifact-manifest-template.json": (
        "run_id",
        "goal_id",
        "created_at",
        "status",
        "source_docs",
        "workflow_ref",
        "skill_refs",
        "template_refs",
        "input_artifacts",
        "output_artifacts",
        "hashes",
        "freeze_points",
        "blockers",
        "forbidden_work_attestation",
        "next_review_recommendation",
    ),
}

FORBIDDEN_TERMS = (
    "future_path",
    "reveal",
    "outcome",
    "judge_result",
    "post_reveal",
    "performance",
    "edge",
    "can_trade",
    "product_go",
    "winner",
    "loser",
    "pnl",
    "win_rate",
    "trade_label",
)

ALLOWED_BOUNDARY_CONTEXTS = (
    "known_at_boundary",
    "forbidden_future_fields_scan",
    "attestations",
    "forbidden_claim_attestation",
    "boundary_attestation",
    "forbidden_work_attestation",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_term(value: str) -> str:
    return value.lower().replace("-", "_").replace(" ", "_")


def missing_required_fields(value: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    return [field for field in required if field not in value]


def scan_forbidden_positive_fields(value: Any, path: str = "$") -> list[str]:
    if any(context in path for context in ALLOWED_BOUNDARY_CONTEXTS):
        return []
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = normalize_term(str(key))
            if any(term in normalized for term in FORBIDDEN_TERMS):
                hits.append(f"{path}.{key}")
            hits.extend(scan_forbidden_positive_fields(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(scan_forbidden_positive_fields(item, f"{path}[{index}]"))
    return hits


def validate_answer_free_boundary(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scan = value.get("forbidden_future_fields_scan")
    if not isinstance(scan, dict):
        errors.append("missing forbidden_future_fields_scan object")
    else:
        positives = [key for key, flag in scan.items() if key != "scan_notes" and flag is not False]
        if positives:
            errors.append(f"forbidden scan flags must be false: {positives}")
    attestations = value.get("attestations")
    if not isinstance(attestations, dict):
        errors.append("missing attestations object")
    else:
        required_true = (
            "answer_free_packet",
            "known_at_only",
            "no_reveal_or_outcome",
            "no_judge_result",
            "no_performance_claim",
            "no_edge_claim",
            "no_can_trade_claim",
            "no_product_go_claim",
            "no_app_source_or_raw_db",
        )
        missing_true = [key for key in required_true if attestations.get(key) is not True]
        if missing_true:
            errors.append(f"answer-free attestations must be true: {missing_true}")
    forbidden_hits = scan_forbidden_positive_fields(value)
    if forbidden_hits:
        errors.append(f"forbidden positive fields outside boundary contexts: {forbidden_hits}")
    return errors


def validate_template_file(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        return {"path": str(path), "status": "fail", "errors": ["template is not a JSON object"]}
    required = TEMPLATE_REQUIRED_FIELDS.get(path.name)
    if required is None:
        return {"path": str(path), "status": "skip", "errors": ["unknown template name"]}
    errors = []
    missing = missing_required_fields(value, required)
    if missing:
        errors.append(f"missing required fields: {missing}")
    if path.name == "lrf-answer-free-packet-template.json":
        errors.extend(validate_answer_free_boundary(value))
    if path.name == "lrf-blind-hypothesis-output-template.json":
        if "observed_fact" not in value or "hypothesis" not in value:
            errors.append("observed_fact and hypothesis separation missing")
    if path.name == "lrf-reviewer-discipline-output-template.json":
        attestation = value.get("boundary_attestation", {})
        if attestation.get("reviewer_did_not_judge_market_result") is not True:
            errors.append("reviewer_did_not_judge_market_result must be true")
        if attestation.get("reviewer_did_not_replace_deterministic_judge_or_evaluator") is not True:
            errors.append("reviewer_did_not_replace_deterministic_judge_or_evaluator must be true")
    if path.name == "lrf-run-artifact-manifest-template.json":
        attestation = value.get("forbidden_work_attestation", {})
        required_true = (
            "template_only",
            "does_not_authorize_market_run",
            "does_not_authorize_reveal",
            "does_not_authorize_judge_or_evaluator",
            "does_not_authorize_tool_execution",
            "does_not_authorize_research_packet",
            "does_not_authorize_app_work",
        )
        missing_true = [key for key in required_true if attestation.get(key) is not True]
        if missing_true:
            errors.append(f"manifest forbidden-work attestations must be true: {missing_true}")
    return {"path": str(path), "status": "fail" if errors else "pass", "errors": errors}


def validate_templates_dir(templates_dir: Path) -> dict[str, Any]:
    results = []
    for name in TEMPLATE_REQUIRED_FIELDS:
        results.append(validate_template_file(templates_dir / name))
    failed = [item for item in results if item["status"] != "pass"]
    return {"status": "fail" if failed else "pass", "kind": "templates_dir", "results": results}


def validate_artifact(path: Path, kind: str) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        return {"status": "fail", "kind": kind, "errors": ["artifact is not a JSON object"]}
    if kind != "answer_free_packet":
        return {"status": "fail", "kind": kind, "errors": [f"unsupported artifact kind: {kind}"]}
    required = TEMPLATE_REQUIRED_FIELDS["lrf-answer-free-packet-template.json"]
    errors = []
    missing = missing_required_fields(value, required)
    if missing:
        errors.append(f"missing required fields: {missing}")
    errors.extend(validate_answer_free_boundary(value))
    return {"status": "fail" if errors else "pass", "kind": kind, "path": str(path), "errors": errors}


def validate_fixture(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        return {"path": str(path), "status": "fail", "errors": ["fixture is not a JSON object"]}
    attestation = value.get("fixture_attestation", {})
    required_true = ("synthetic_fixture", "not_market_evidence", "not_research_packet")
    errors = [f"fixture_attestation.{key} must be true" for key in required_true if attestation.get(key) is not True]
    forbidden_hits = scan_raw_forbidden_fixture_fields(value)
    if forbidden_hits:
        errors.append(f"forbidden fixture fields: {forbidden_hits}")
    return {"path": str(path), "status": "fail" if errors else "pass", "errors": errors}


def scan_raw_forbidden_fixture_fields(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = normalize_term(str(key))
            if any(term in normalized for term in FORBIDDEN_TERMS):
                hits.append(f"{path}.{key}")
            hits.extend(scan_raw_forbidden_fixture_fields(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(scan_raw_forbidden_fixture_fields(item, f"{path}[{index}]"))
    return hits


def run_self_test() -> dict[str, Any]:
    root = repo_root()
    templates_result = validate_templates_dir(root / "agent-system" / "templates")
    fixture_result = validate_fixture(root / "agent-system" / "tools" / "fixtures" / "lrf_minimal_app_export.json")
    failed = templates_result["status"] != "pass" or fixture_result["status"] != "pass"
    return {
        "status": "fail" if failed else "pass",
        "self_test": "lrf_validate_artifact_templates",
        "templates": templates_result,
        "fixture": fixture_result,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate LRF JSON templates and answer-free packet artifacts.")
    parser.add_argument("--templates-dir", type=Path, help="Directory containing LRF JSON templates.")
    parser.add_argument("--artifact", type=Path, help="Artifact JSON file to validate.")
    parser.add_argument("--kind", choices=("answer_free_packet",), help="Artifact kind for --artifact.")
    parser.add_argument("--self-test", action="store_true", help="Validate committed templates and synthetic fixture.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.self_test:
            result = run_self_test()
        elif args.templates_dir:
            result = validate_templates_dir(args.templates_dir)
        elif args.artifact and args.kind:
            result = validate_artifact(args.artifact, args.kind)
        else:
            raise ValueError("use --templates-dir, --artifact with --kind, or --self-test")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "pass" else 1
    except Exception as exc:  # noqa: BLE001 - CLI should report validation failures as JSON.
        print(json.dumps({"status": "fail", "error": str(exc)}, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
