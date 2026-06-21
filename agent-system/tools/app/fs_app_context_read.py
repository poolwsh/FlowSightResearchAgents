#!/usr/bin/env python
"""Read FlowSight app context through an explicit CLI command.

Real mode requires --cli-command and an explicit --app or --endpoint selector.
Self-test and mock mode do not invoke the real CLI.
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


TOOL_ID = "fs_app_context_read"


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


def pick(raw: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in raw:
            return raw[key]
    return ""


def build_payload(
    raw: Any,
    source_ref: str,
    request_id: str = "",
    command_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    context = raw if isinstance(raw, dict) else {}
    visible_range = {
        "visible_time_start_ms": pick(context, "visible_time_start_ms", "visible_start_ms"),
        "visible_time_end_ms": pick(context, "visible_time_end_ms", "visible_end_ms"),
        "viewport_first_idx": pick(context, "viewport_first_idx"),
        "viewport_bars_per_view": pick(context, "viewport_bars_per_view"),
    }
    observation = {
        "app_instance_id": pick(context, "app_instance_id", "app"),
        "symbol": pick(context, "symbol"),
        "venue": pick(context, "venue"),
        "timeframe": pick(context, "timeframe"),
        "generation": pick(context, "generation", "projection_generation", "selection_generation"),
        "status": pick(context, "status"),
        "visible_range": visible_range,
        "data_family_status": context.get("data_family_status", {}),
        "raw_response_hash": digest(raw),
    }
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "status": "ok",
        "source_ref": source_ref,
        "command_evidence": command_evidence or {},
        "observation_summary": observation,
        "evidence_cutoff": "",
        "cutoff_respected": True,
        "blocked_reason": "",
        "forbidden_attestation": forbidden_attestation(),
    }


def cli_args(cli_command: str, app: str | None, endpoint: str | None) -> list[str]:
    args = [cli_command]
    if app:
        args.extend(["--app", app])
    if endpoint:
        args.extend(["--endpoint", endpoint])
    args.extend(["app-context", "get", "--json"])
    return args


def run_cli(cli_command: str, app: str | None, endpoint: str | None) -> tuple[int, dict[str, Any], Any | None, str]:
    cmd = cli_args(cli_command, app, endpoint)
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
        "app_instance_id": "pid:1234",
        "symbol": "PerpUsdc:ETH-USDC",
        "venue": "PerpUsdc",
        "timeframe": "5m",
        "generation": 7,
        "visible_time_start_ms": 1781136000000,
        "visible_time_end_ms": 1781913600000,
        "data_family_status": {"ohlcv": "available", "trades": "not_exposed"},
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_path = Path(temp_dir) / "mock_context.json"
        mock_path.write_text(json.dumps(mock), encoding="utf-8")
        raw = read_json(str(mock_path))
        payload = build_payload(raw, f"mock:{mock_path}", command_evidence={"mode": "self_test_mock"})
        assert payload["status"] == "ok"
        assert payload["observation_summary"]["symbol"] == "PerpUsdc:ETH-USDC"
        assert payload["observation_summary"]["data_family_status"]["trades"] == "not_exposed"
    return {"status": "pass", "tool_id": TOOL_ID, "real_cli_invoked": False}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read FlowSight app context via explicit CLI or mock JSON.")
    parser.add_argument("--cli-command", help="Explicit FlowSight CLI command/path. Required for real mode.")
    parser.add_argument("--app", help="Explicit app selector supplied by owner/dispatcher/runtime contract.")
    parser.add_argument("--endpoint", help="Explicit endpoint selector/ref supplied by owner/dispatcher/runtime contract.")
    parser.add_argument("--mock-input-json", help="Mock app-context JSON. Does not require --cli-command.")
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
        emit(blocked_payload("--cli-command is required for real app context readback", args.request_id), args.output)
        return 2
    if not args.app and not args.endpoint:
        emit(blocked_payload("real app context readback requires --app or --endpoint", args.request_id), args.output)
        return 2
    code, evidence, raw, error = run_cli(args.cli_command, args.app, args.endpoint)
    if code != 0 or raw is None:
        payload = blocked_payload(error or "app-context CLI failed", args.request_id)
        payload["command_evidence"] = evidence
        payload["blocked_reason"] = error or "app-context CLI failed"
        emit(payload, args.output)
        return code or 1
    payload = build_payload(raw, "cli:app-context get --json", args.request_id, evidence)
    emit(payload, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
