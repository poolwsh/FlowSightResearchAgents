#!/usr/bin/env python3
"""Build an LRF answer-free packet from an explicit local JSON input.

This tool is intentionally narrow. It does not discover FlowSight endpoints,
read raw databases, call external APIs, interpret markets, write hypotheses,
judge outcomes, or create research packets.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


FORBIDDEN_FIELD_TERMS = (
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


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def normalize_term(value: str) -> str:
    return value.lower().replace("-", "_").replace(" ", "_")


def find_forbidden_positive_fields(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = normalize_term(str(key))
            if any(term in normalized for term in FORBIDDEN_FIELD_TERMS):
                hits.append(f"{path}.{key}")
            hits.extend(find_forbidden_positive_fields(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(find_forbidden_positive_fields(item, f"{path}[{index}]"))
    return hits


def require_synthetic_fixture_if_marked(data: dict[str, Any]) -> None:
    attestation = data.get("fixture_attestation")
    if attestation is None:
        return
    required = {
        "synthetic_fixture": True,
        "not_market_evidence": True,
        "not_research_packet": True,
    }
    missing = [key for key, expected in required.items() if attestation.get(key) is not expected]
    if missing:
        raise ValueError(f"fixture_attestation missing true values: {missing}")


def copy_if_present(target: dict[str, Any], source: dict[str, Any], key: str) -> None:
    if key in source:
        target[key] = copy.deepcopy(source[key])


def build_answer_free_packet(input_data: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    hits = find_forbidden_positive_fields(input_data)
    if hits:
        raise ValueError(f"forbidden positive fields in input: {hits}")
    require_synthetic_fixture_if_marked(input_data)

    packet = copy.deepcopy(template)
    packet["packet_id"] = input_data.get("packet_id", "lrf-answer-free-packet-synthetic-self-test")
    packet["created_at"] = input_data.get("created_at", "")

    for key in (
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
        "missing_evidence",
    ):
        copy_if_present(packet, input_data, key)

    packet["trade_hypothesis_field_slots"] = input_data.get(
        "trade_hypothesis_field_slots",
        packet["trade_hypothesis_field_slots"],
    )
    packet["blocker_classification"] = input_data.get(
        "blocker_classification",
        {
            "class": "none",
            "reason": "",
            "required_next_evidence": [],
        },
    )
    packet["forbidden_future_fields_scan"] = {
        "future_path_present": False,
        "reveal_present": False,
        "outcome_present": False,
        "judge_result_present": False,
        "post_reveal_comparison_present": False,
        "performance_metric_present": False,
        "edge_or_can_trade_claim_present": False,
        "scan_notes": "input and output scanned by lrf_build_answer_free_packet.py",
    }
    packet["attestations"] = {
        "answer_free_packet": True,
        "known_at_only": True,
        "no_reveal_or_outcome": True,
        "no_judge_result": True,
        "no_performance_claim": True,
        "no_edge_claim": True,
        "no_can_trade_claim": True,
        "no_product_go_claim": True,
        "no_app_source_or_raw_db": True,
    }

    output_hits = find_forbidden_positive_fields_without_attestations(packet)
    if output_hits:
        raise ValueError(f"forbidden positive fields in output: {output_hits}")
    return packet


def find_forbidden_positive_fields_without_attestations(value: Any, path: str = "$") -> list[str]:
    allowed_contexts = (
        "known_at_boundary",
        "forbidden_future_fields_scan",
        "attestations",
        "forbidden_claim_attestation",
        "boundary_attestation",
        "forbidden_work_attestation",
    )
    if any(context in path for context in allowed_contexts):
        return []
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = normalize_term(str(key))
            if any(term in normalized for term in FORBIDDEN_FIELD_TERMS):
                hits.append(f"{path}.{key}")
            hits.extend(find_forbidden_positive_fields_without_attestations(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(find_forbidden_positive_fields_without_attestations(item, f"{path}[{index}]"))
    return hits


def validate_answer_free_packet(packet: dict[str, Any]) -> None:
    required = (
        "packet_id",
        "packet_version",
        "client_mirror_first",
        "app_context",
        "owner_referent",
        "bounded_window",
        "instrument",
        "known_at_boundary",
        "source_refs",
        "data_family_status",
        "trade_hypothesis_field_slots",
        "missing_evidence",
        "blocker_classification",
        "forbidden_future_fields_scan",
        "attestations",
    )
    missing = [key for key in required if key not in packet]
    if missing:
        raise ValueError(f"answer-free packet missing required fields: {missing}")
    scan = packet["forbidden_future_fields_scan"]
    positive_flags = [key for key, value in scan.items() if key != "scan_notes" and value is not False]
    if positive_flags:
        raise ValueError(f"forbidden scan flags must be false: {positive_flags}")
    attestations = packet["attestations"]
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
        raise ValueError(f"answer-free attestations must be true: {missing_true}")


def run_build(input_path: Path, template_path: Path, output_path: Path) -> dict[str, Any]:
    input_data = load_json(input_path)
    template = load_json(template_path)
    if not isinstance(input_data, dict) or not isinstance(template, dict):
        raise ValueError("input and template must be JSON objects")
    packet = build_answer_free_packet(input_data, template)
    validate_answer_free_packet(packet)
    write_json(output_path, packet)
    return {
        "status": "pass",
        "output": str(output_path),
        "packet_id": packet["packet_id"],
    }


def run_self_test() -> dict[str, Any]:
    root = repo_root()
    fixture = root / "agent-system" / "tools" / "fixtures" / "lrf_minimal_app_export.json"
    template = root / "agent-system" / "templates" / "lrf-answer-free-packet-template.json"
    with tempfile.TemporaryDirectory(prefix="lrf-answer-free-packet-") as temp_dir:
        output = Path(temp_dir) / "packet.json"
        result = run_build(fixture, template, output)
        generated = load_json(output)
        validate_answer_free_packet(generated)
        return {
            "status": "pass",
            "self_test": "lrf_build_answer_free_packet",
            "temp_output_removed_after_context": True,
            "packet_id": result["packet_id"],
        }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an LRF answer-free packet from explicit local JSON.")
    parser.add_argument("--input", type=Path, help="Explicit local app-export-like JSON input.")
    parser.add_argument("--template", type=Path, help="Answer-free packet template JSON.")
    parser.add_argument("--output", type=Path, help="Output packet JSON path.")
    parser.add_argument("--self-test", action="store_true", help="Run fixture-based self-test using a temp output path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.self_test:
            print(json.dumps(run_self_test(), indent=2, ensure_ascii=False))
            return 0
        if not args.input or not args.template or not args.output:
            raise ValueError("--input, --template, and --output are required unless --self-test is used")
        result = run_build(args.input, args.template, args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI should report all validation failures.
        print(json.dumps({"status": "fail", "error": str(exc)}, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
