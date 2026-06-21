#!/usr/bin/env python
"""List FlowSight app instances through an explicit CLI command.

This wrapper is a ResearchAgents tool. It never launches apps and never
searches the workspace for CLI binaries. Real mode requires --cli-command.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOL_ID = "fs_app_list"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def forbidden_attestation() -> dict[str, bool]:
    return {
        "no_reveal": True,
        "no_outcome": True,
        "no_judge_result": True,
        "no_performance": True,
        "no_edge_or_can_trade": True,
        "no_product_go": True,
        "no_raw_db": True,
        "no_external_api": True,
        "no_app_source": True,
        "no_release_or_dispatcher_internals": True,
    }


def with_hash(payload: dict[str, Any], output_ref: str = "") -> dict[str, Any]:
    payload = dict(payload)
    payload["output_ref"] = output_ref
    payload["output_hash"] = ""
    payload["output_hash"] = digest(payload)
    return payload


def emit(payload: dict[str, Any], output: str | None = None) -> None:
    output_ref = str(Path(output)) if output else ""
    payload = with_hash(payload, output_ref)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)


def blocked_payload(reason: str, request_id: str = "") -> dict[str, Any]:
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "status": "blocked",
        "source_ref": "",
        "command_evidence": {"mode": "blocked", "reason": reason},
        "observation_summary": {},
        "evidence_cutoff": "",
        "cutoff_respected": True,
        "blocked_reason": reason,
        "forbidden_attestation": forbidden_attestation(),
    }


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_apps(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        apps = raw
    elif isinstance(raw, dict):
        apps = raw.get("apps") or raw.get("instances") or raw.get("items") or []
        if not apps and any(key in raw for key in ("app_instance_id", "pid", "version", "lane")):
            apps = [raw]
    else:
        apps = []
    normalized: list[dict[str, Any]] = []
    for item in apps:
        if isinstance(item, dict):
            normalized.append(
                {
                    "app_instance_id": item.get("app_instance_id") or item.get("id") or item.get("selector") or "",
                    "pid": item.get("pid", ""),
                    "version": item.get("version") or item.get("commit") or "",
                    "lane": item.get("lane", ""),
                    "promotable": item.get("promotable", ""),
                    "status": item.get("status", ""),
                    "endpoint_ref": item.get("endpoint_ref") or item.get("endpoint_dir") or "",
                }
            )
    return normalized


def build_payload(
    raw: Any,
    source_ref: str,
    request_id: str = "",
    command_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    apps = normalize_apps(raw)
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "status": "ok",
        "source_ref": source_ref,
        "command_evidence": command_evidence or {},
        "observation_summary": {
            "app_count": len(apps),
            "instances": apps,
            "raw_response_hash": digest(raw),
        },
        "evidence_cutoff": "",
        "cutoff_respected": True,
        "blocked_reason": "",
        "forbidden_attestation": forbidden_attestation(),
    }


def run_cli(cli_command: str) -> tuple[int, dict[str, Any], Any | None, str]:
    cmd = [cli_command, "app", "list", "--json"]
    resolved = shutil.which(cli_command) if not Path(cli_command).is_absolute() else str(Path(cli_command))
    started_at = now_iso()
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    evidence = {
        "mode": "real_cli",
        "command": cmd,
        "command_resolved_path": resolved or "",
        "started_at": started_at,
        "completed_at": now_iso(),
        "returncode": result.returncode,
        "stdout_sha256": hashlib.sha256(result.stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr.encode("utf-8")).hexdigest(),
    }
    if result.returncode != 0:
        return result.returncode, evidence, None, result.stderr.strip()
    try:
        return 0, evidence, json.loads(result.stdout), ""
    except json.JSONDecodeError as exc:
        return 1, evidence, None, f"CLI stdout was not JSON: {exc}"


def self_test() -> dict[str, Any]:
    mock = {
        "apps": [
            {
                "app_instance_id": "pid:1234",
                "pid": 1234,
                "version": "synthetic",
                "lane": "release",
                "promotable": True,
                "status": "running",
            }
        ]
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_path = Path(temp_dir) / "mock_app_list.json"
        mock_path.write_text(json.dumps(mock), encoding="utf-8")
        raw = read_json(str(mock_path))
        payload = build_payload(raw, f"mock:{mock_path}", command_evidence={"mode": "self_test_mock"})
        assert payload["status"] == "ok"
        assert payload["observation_summary"]["app_count"] == 1
        assert payload["forbidden_attestation"]["no_external_api"] is True
    return {"status": "pass", "tool_id": TOOL_ID, "real_cli_invoked": False}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List FlowSight app instances via explicit CLI or mock JSON.")
    parser.add_argument("--cli-command", help="Explicit FlowSight CLI command/path. Required for real mode.")
    parser.add_argument("--mock-input-json", help="Mock app list JSON. Does not require --cli-command.")
    parser.add_argument("--request-id", default="", help="Optional broker request id.")
    parser.add_argument("--output", help="Optional output JSON path.")
    parser.add_argument("--self-test", action="store_true", help="Run synthetic self-test without real CLI.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.mock_input_json:
        raw = read_json(args.mock_input_json)
        payload = build_payload(
            raw,
            source_ref=f"mock:{args.mock_input_json}",
            request_id=args.request_id,
            command_evidence={"mode": "mock_input", "mock_input_json": args.mock_input_json},
        )
        emit(payload, args.output)
        return 0
    if not args.cli_command:
        emit(blocked_payload("--cli-command is required for real app readback", args.request_id), args.output)
        return 2
    code, evidence, raw, error = run_cli(args.cli_command)
    if code != 0 or raw is None:
        payload = blocked_payload(error or "app list CLI failed", args.request_id)
        payload["command_evidence"] = evidence
        payload["blocked_reason"] = error or "app list CLI failed"
        emit(payload, args.output)
        return code or 1
    payload = build_payload(raw, "cli:app list --json", args.request_id, evidence)
    emit(payload, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
