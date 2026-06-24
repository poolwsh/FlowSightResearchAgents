#!/usr/bin/env python
"""Export bounded OHLCV bars through an explicit FlowSight CLI command.

This wrapper only creates app-owned bounded export artifacts. It does not read
raw databases, call exchange APIs, or infer market labels.
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


TOOL_ID = "fs_bars_export"


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


def blocked_payload(reason: str, request_id: str = "", evidence_cutoff: str = "") -> dict[str, Any]:
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "status": "blocked",
        "source_ref": "",
        "command_evidence": {"mode": "blocked", "reason": reason},
        "observation_summary": {},
        "bars_export": {},
        "evidence_cutoff": evidence_cutoff,
        "cutoff_respected": True,
        "blocked_reason": reason,
        "forbidden_attestation": forbidden_attestation(),
    }


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def extract_bars(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        bars = raw.get("bars") or raw.get("data", {}).get("bars") or raw.get("ohlcv") or []
    elif isinstance(raw, list):
        bars = raw
    else:
        bars = []
    return [bar for bar in bars if isinstance(bar, dict) and "time" in bar]


def within(value: str, start: str, end: str, cutoff: str) -> bool:
    if start and value < start:
        return False
    if end and value > end:
        return False
    if cutoff and value > cutoff:
        return False
    return True


def build_payload(
    raw: Any,
    source_ref: str,
    symbol: str,
    venue: str,
    timeframe: str,
    start: str,
    end: str,
    evidence_cutoff: str,
    request_id: str = "",
    command_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bars = [bar for bar in extract_bars(raw) if within(str(bar.get("time", "")), start, end, evidence_cutoff)]
    bars_export = {
        "artifact_kind": "app_owned_ohlcv_bars_export.v1",
        "synthetic_fixture": bool(isinstance(raw, dict) and raw.get("synthetic_fixture")),
        "not_market_evidence": bool(isinstance(raw, dict) and raw.get("not_market_evidence", False)),
        "not_research_packet": bool(isinstance(raw, dict) and raw.get("not_research_packet", False)),
        "symbol": symbol or (raw.get("symbol") if isinstance(raw, dict) else ""),
        "venue": venue or (raw.get("venue") if isinstance(raw, dict) else ""),
        "timeframe": timeframe or (raw.get("timeframe") if isinstance(raw, dict) else ""),
        "requested_start": start,
        "requested_end": end,
        "evidence_cutoff": evidence_cutoff,
        "bars": bars,
    }
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "status": "ok",
        "source_ref": source_ref,
        "command_evidence": command_evidence or {},
        "observation_summary": {
            "bar_count": len(bars),
            "first_bar_time": bars[0].get("time", "") if bars else "",
            "last_bar_time": bars[-1].get("time", "") if bars else "",
            "bars_export_hash": digest(bars_export),
            "raw_response_hash": digest(raw),
        },
        "bars_export": bars_export,
        "evidence_cutoff": evidence_cutoff,
        "cutoff_respected": all(not evidence_cutoff or str(bar.get("time", "")) <= evidence_cutoff for bar in bars),
        "blocked_reason": "",
        "forbidden_attestation": forbidden_attestation(),
    }


def cli_args(args: argparse.Namespace) -> list[str]:
    cmd = [args.cli_command]
    if args.app:
        cmd.extend(["--app", args.app])
    if args.endpoint:
        cmd.extend(["--endpoint", args.endpoint])
    cmd.extend(
        [
            "bars",
            "get",
            "--symbol",
            args.symbol,
            "--venue",
            args.venue,
            "--timeframe",
            args.timeframe,
            "--start",
            args.start,
            "--end",
            args.end,
            "--json",
        ]
    )
    return cmd


def run_cli(args: argparse.Namespace) -> tuple[int, dict[str, Any], Any | None, str]:
    cmd = cli_args(args)
    resolved = shutil.which(args.cli_command) if not Path(args.cli_command).is_absolute() else str(Path(args.cli_command))
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
        "synthetic_fixture": True,
        "not_market_evidence": True,
        "not_research_packet": True,
        "symbol": "ETH-USDC",
        "venue": "PerpUsdc",
        "timeframe": "5m",
        "bars": [
            {"time": "2026-06-11T00:00:00Z", "open": 100, "high": 101, "low": 99, "close": 100.5, "volume": 10},
            {"time": "2026-06-11T00:05:00Z", "open": 100.5, "high": 103.2, "low": 100.1, "close": 101.8, "volume": 12},
        ],
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_path = Path(temp_dir) / "mock_bars.json"
        mock_path.write_text(json.dumps(mock), encoding="utf-8")
        raw = read_json(str(mock_path))
        payload = build_payload(
            raw,
            f"mock:{mock_path}",
            "ETH-USDC",
            "PerpUsdc",
            "5m",
            "2026-06-11T00:00:00Z",
            "2026-06-11T00:05:00Z",
            "2026-06-11T00:05:00Z",
            command_evidence={"mode": "self_test_mock"},
        )
        assert payload["status"] == "ok"
        assert payload["observation_summary"]["bar_count"] == 2
        assert payload["cutoff_respected"] is True
    return {"status": "pass", "tool_id": TOOL_ID, "real_cli_invoked": False}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export bounded FlowSight OHLCV bars via explicit CLI or mock JSON.")
    parser.add_argument("--cli-command", help="Explicit FlowSight CLI command/path. Required for real mode.")
    parser.add_argument("--app", help="Explicit app selector supplied by owner/dispatcher/runtime contract.")
    parser.add_argument("--endpoint", help="Explicit endpoint selector/ref supplied by owner/dispatcher/runtime contract.")
    parser.add_argument("--symbol", default="", help="Symbol/instrument to export.")
    parser.add_argument("--venue", default="", help="Venue to export.")
    parser.add_argument("--timeframe", default="", help="Timeframe to export.")
    parser.add_argument("--start", default="", help="Inclusive start timestamp.")
    parser.add_argument("--end", default="", help="Inclusive end timestamp.")
    parser.add_argument("--evidence-cutoff", default="", help="Known-at cutoff; bars after this are omitted.")
    parser.add_argument("--mock-input-json", help="Mock bars JSON. Does not require --cli-command.")
    parser.add_argument("--request-id", default="", help="Optional broker request id.")
    parser.add_argument("--output", help="Optional output JSON path.")
    parser.add_argument("--self-test", action="store_true", help="Run synthetic self-test without real CLI.")
    return parser.parse_args()


def validate_real_args(args: argparse.Namespace) -> str:
    if not args.cli_command:
        return "--cli-command is required for real bars export"
    if not args.app and not args.endpoint:
        return "real bars export requires --app or --endpoint"
    missing = [name for name in ("symbol", "venue", "timeframe", "start", "end") if not getattr(args, name)]
    if missing:
        return "real bars export missing required args: " + ", ".join(missing)
    return ""


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
            symbol=args.symbol,
            venue=args.venue,
            timeframe=args.timeframe,
            start=args.start,
            end=args.end,
            evidence_cutoff=args.evidence_cutoff,
            request_id=args.request_id,
            command_evidence={"mode": "mock_input", "mock_input_json": args.mock_input_json},
        )
        emit(payload, args.output)
        return 0
    real_error = validate_real_args(args)
    if real_error:
        emit(blocked_payload(real_error, args.request_id, args.evidence_cutoff), args.output)
        return 2
    code, evidence, raw, error = run_cli(args)
    if code != 0 or raw is None:
        payload = blocked_payload(error or "bars export CLI failed", args.request_id, args.evidence_cutoff)
        payload["command_evidence"] = evidence
        payload["blocked_reason"] = error or "bars export CLI failed"
        emit(payload, args.output)
        return code or 1
    payload = build_payload(
        raw,
        "cli:bars get --json",
        args.symbol,
        args.venue,
        args.timeframe,
        args.start,
        args.end,
        args.evidence_cutoff,
        args.request_id,
        evidence,
    )
    emit(payload, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
