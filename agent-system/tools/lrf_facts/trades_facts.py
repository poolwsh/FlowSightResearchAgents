#!/usr/bin/env python
"""Compute deterministic trades facts from app-owned trades readback."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Any


TOOL_ID = "trades_facts"
VALID_MODES = {"slice_summary", "adaptive_time_buckets", "price_zone_filter", "large_prints"}
MAX_ROWS_HARD_CAP = 100000


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def file_digest(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def empty_source_hashes() -> dict[str, str]:
    return {"raw_source_hash": "", "normalized_source_hash": ""}


def hash_semantics() -> dict[str, str]:
    return {
        "response_id": "canonical tool response identity; when request_id is present use <tool_id>:<request_id>:response",
        "response_id_source": "identity source enum: explicit, derived_from_request_id, or derived_from_payload_core",
        "request_id": "broker request identity; not the primary trace reference",
        "raw_source_hash": "sha256 over exact saved source artifact bytes or canonical app response payload hash bundle",
        "normalized_source_hash": "sha256 over canonical normalized rows/facts consumed by this tool",
        "output_hash": "sha256 over the emitted response payload with output_hash fields blank before hashing",
    }


def response_id_for(payload: dict[str, Any]) -> str:
    request_id = str(payload.get("request_id") or "")
    tool_id = str(payload.get("tool_id") or TOOL_ID)
    if request_id:
        return f"{tool_id}:{request_id}:response"
    core = dict(payload)
    for key in ("response_id", "identity", "output_ref", "output_hash"):
        core.pop(key, None)
    return f"{tool_id}:response:{digest(core)[:16]}"


def response_id_source_for(payload: dict[str, Any]) -> str:
    if payload.get("response_id"):
        return "explicit"
    if payload.get("request_id"):
        return "derived_from_request_id"
    return "derived_from_payload_core"


def forbidden_attestation() -> dict[str, bool]:
    return {
        "no_orderbook": True,
        "no_raw_db": True,
        "no_external_api": True,
        "no_app_source": True,
        "no_smart_money_final_label": True,
        "no_reveal": True,
        "no_judge_result": True,
        "no_performance": True,
        "no_edge_or_can_trade": True,
        "no_product_go": True,
    }


def parse_time_ms(value: Any) -> int | None:
    if value in ("", None):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
        return int(text)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.astimezone(timezone.utc).timestamp() * 1000)


def ms_to_utc_iso(value: Any) -> str:
    try:
        millis = int(value)
    except (TypeError, ValueError):
        return ""
    return datetime.fromtimestamp(millis / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def with_hash(payload: dict[str, Any], output_ref: str = "") -> dict[str, Any]:
    payload = dict(payload)
    response_id_source = response_id_source_for(payload)
    if not payload.get("response_id"):
        payload["response_id"] = response_id_for(payload)
    payload["output_ref"] = output_ref
    payload.setdefault("source_hashes", empty_source_hashes())
    payload.setdefault("hash_semantics", hash_semantics())
    payload["identity"] = {
        "response_id": payload["response_id"],
        "response_id_source": response_id_source,
        "request_id": payload.get("request_id", ""),
        "output_ref": output_ref,
        "output_hash": "",
    }
    payload["output_hash"] = ""
    output_hash = digest(payload)
    payload["output_hash"] = output_hash
    payload["identity"]["output_hash"] = output_hash
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


def blocked_payload(reason: str, request_id: str = "", evidence_cutoff: str = "", status: str = "blocked") -> dict[str, Any]:
    return {
        "tool_id": TOOL_ID,
        "request_id": request_id,
        "response_id": "",
        "status": status,
        "source_ref": "",
        "observation_summary": {},
        "evidence_cutoff": evidence_cutoff,
        "cutoff_respected": True,
        "blocked_reason": reason,
        "adaptive_slices": [],
        "source_hashes": empty_source_hashes(),
        "legacy_source_hashes": [],
        "hash_semantics": hash_semantics(),
        "forbidden_attestation": forbidden_attestation(),
    }


def extract_rows(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    rows = payload.get("rows")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    data = payload.get("data")
    if isinstance(data, dict) and isinstance(data.get("rows"), list):
        return [row for row in data["rows"] if isinstance(row, dict)]
    return []


def payload_channel(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("channel") or payload.get("data", {}).get("channel") or "")


def payload_truncated(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    return bool(payload.get("truncated", False))


def payload_source(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return {}
    return payload.get("source", {})


def payload_known_at_policy(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("known_at_policy", ""))


def row_time_ms(row: dict[str, Any]) -> int | None:
    return parse_time_ms(row.get("ts_ms") or row.get("time_ms") or row.get("timestamp_ms") or row.get("time"))


def row_known_at_ms(row: dict[str, Any]) -> int | None:
    return parse_time_ms(row.get("known_at_ms") or row.get("ts_ms") or row.get("time_ms") or row.get("time"))


def normalize_side(value: Any) -> str:
    text = str(value or "unknown").strip().lower()
    if text in {"buy", "b", "aggressor_buy"}:
        return "buy"
    if text in {"sell", "s", "aggressor_sell"}:
        return "sell"
    return "unknown"


def filter_rows(rows: list[dict[str, Any]], start_ms: int, end_ms: int, cutoff_ms: int | None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        ts = row_time_ms(row)
        known_at = row_known_at_ms(row)
        if ts is None:
            continue
        if ts < start_ms or ts >= end_ms:
            continue
        if cutoff_ms is not None and (known_at is None or known_at > cutoff_ms):
            continue
        out.append(row)
    return sorted(out, key=lambda item: int(row_time_ms(item) or 0))


def summarize_rows(rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    pre_filter_count = len(rows)
    filtered_rows: list[dict[str, Any]] = []
    price_low = args.price_low
    price_high = args.price_high
    for row in rows:
        price = float(row.get("price", 0) or 0)
        if price_low is not None and price < price_low:
            continue
        if price_high is not None and price > price_high:
            continue
        filtered_rows.append(row)

    prices: list[float] = []
    qty_sum = 0.0
    notional_sum = 0.0
    side_counts = {"buy": 0, "sell": 0, "unknown": 0}
    side_qty = {"buy": 0.0, "sell": 0.0, "unknown": 0.0}
    large_prints: list[dict[str, Any]] = []
    threshold = args.large_print_qty_threshold

    for row in filtered_rows:
        price = float(row.get("price", 0) or 0)
        qty = float(row.get("qty", 0) or 0)
        side = normalize_side(row.get("aggressor_side"))
        side_counts[side] += 1
        side_qty[side] += qty
        prices.append(price)
        qty_sum += qty
        notional_sum += price * qty
        if threshold is not None and qty >= threshold:
            large_prints.append(
                {
                    "ts_ms": row_time_ms(row),
                    "time_utc": ms_to_utc_iso(row_time_ms(row)),
                    "price": price,
                    "qty": qty,
                    "aggressor_side": side,
                    "trade_id": row.get("trade_id", ""),
                }
            )

    ts_values = [int(row_time_ms(row) or 0) for row in filtered_rows if row_time_ms(row) is not None]
    summary: dict[str, Any] = {
        "count": len(filtered_rows),
        "pre_filter_count": pre_filter_count,
        "filtered_out_count": pre_filter_count - len(filtered_rows),
        "min_ts_ms": min(ts_values) if ts_values else None,
        "max_ts_ms": max(ts_values) if ts_values else None,
        "first_ts_ms": ts_values[0] if ts_values else None,
        "last_ts_ms": ts_values[-1] if ts_values else None,
        "first_time_utc": ms_to_utc_iso(ts_values[0]) if ts_values else "",
        "last_time_utc": ms_to_utc_iso(ts_values[-1]) if ts_values else "",
        "price_min": min(prices) if prices else None,
        "price_max": max(prices) if prices else None,
        "qty_sum": qty_sum,
        "notional_sum": notional_sum,
        "vwap": (notional_sum / qty_sum) if qty_sum else None,
        "side_counts": side_counts,
        "side_qty": side_qty,
        "net_aggressor_qty": side_qty["buy"] - side_qty["sell"],
    }
    if args.mode == "large_prints" or threshold is not None:
        summary["large_prints"] = sorted(large_prints, key=lambda item: item["qty"], reverse=True)
        summary["large_print_qty_threshold"] = threshold
    if args.mode == "price_zone_filter":
        summary["price_zone_filter"] = {"price_low": price_low, "price_high": price_high}
    return summary


def bucket_rows(rows: list[dict[str, Any]], bucket_ms: int, args: argparse.Namespace) -> list[dict[str, Any]]:
    buckets: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        ts = row_time_ms(row)
        if ts is None:
            continue
        bucket_start = (ts // bucket_ms) * bucket_ms
        buckets.setdefault(bucket_start, []).append(row)
    out = []
    for start in sorted(buckets):
        fake_args = argparse.Namespace(**vars(args))
        fake_args.mode = "slice_summary"
        summary = summarize_rows(buckets[start], fake_args)
        summary["bucket_start_ms"] = start
        summary["bucket_end_ms"] = start + bucket_ms
        summary["bucket_start_utc"] = ms_to_utc_iso(start)
        summary["bucket_end_utc"] = ms_to_utc_iso(start + bucket_ms)
        out.append(summary)
    return out


def coverage_ok(payload: Any, start_ms: int, end_ms: int, cutoff_ms: int | None) -> bool:
    if not isinstance(payload, dict):
        return False
    requested = payload.get("requested_range") if isinstance(payload.get("requested_range"), dict) else {}
    from_ms = parse_time_ms(requested.get("from_ms"))
    to_ms = parse_time_ms(requested.get("to_ms"))
    as_of_ms = parse_time_ms(requested.get("as_of_ms"))
    if from_ms is None or to_ms is None or as_of_ms is None:
        return False
    if from_ms is not None and from_ms > start_ms:
        return False
    if to_ms is not None and to_ms < end_ms:
        return False
    if cutoff_ms is not None and as_of_ms is not None and as_of_ms < cutoff_ms:
        return False
    return True


def query_trades(args: argparse.Namespace, start_ms: int, end_ms: int, cutoff_ms: int, attempt: int) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    argv = [
        args.cli_command,
        "--app",
        args.app,
        "trades",
        "get",
        "--symbol",
        args.symbol,
        "--from-ms",
        str(start_ms),
        "--to-ms",
        str(end_ms),
        "--as-of-ms",
        str(cutoff_ms),
        "--max-rows",
        str(args.max_rows),
    ]
    env = os.environ.copy()
    env["FS_APP_ENDPOINT_DIR"] = args.endpoint_dir
    started = time.monotonic()
    try:
        result = subprocess.run(
            argv,
            text=True,
            capture_output=True,
            env=env,
            timeout=max(1, int(args.subprocess_timeout_seconds)),
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        payload = json.loads(stdout) if stdout.strip().startswith("{") else None
        exit_code = result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else "subprocess timeout"
        payload = None
        exit_code = 124
    record = {
        "argv": argv,
        "endpoint_binding_method": "FS_APP_ENDPOINT_DIR",
        "endpoint_dir": args.endpoint_dir,
        "exit_code": exit_code,
        "stdout_hash": text_hash(stdout),
        "stderr_hash": text_hash(stderr),
        "requested_start_ms": start_ms,
        "requested_end_ms": end_ms,
        "evidence_cutoff_ms": cutoff_ms,
        "requested_start_utc": ms_to_utc_iso(start_ms),
        "requested_end_utc": ms_to_utc_iso(end_ms),
        "evidence_cutoff_utc": ms_to_utc_iso(cutoff_ms),
        "max_rows": args.max_rows,
        "row_count": len(extract_rows(payload)) if payload else 0,
        "truncated": payload_truncated(payload) if payload else None,
        "source": payload_source(payload) if payload else {},
        "channel": payload_channel(payload) if payload else "",
        "known_at_policy": payload_known_at_policy(payload) if payload else "",
        "response_hash": digest(payload) if payload else "",
        "duration_ms": int((time.monotonic() - started) * 1000),
        "attempt": attempt,
    }
    return payload, record


def adaptive_query(args: argparse.Namespace, start_ms: int, end_ms: int, cutoff_ms: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    pending = [(start_ms, end_ms)]
    complete_payloads: list[dict[str, Any]] = []
    slice_records: list[dict[str, Any]] = []
    rows_seen = 0
    started = time.monotonic()
    blocked_reason = ""

    while pending:
        if len(slice_records) >= args.max_slice_count:
            blocked_reason = "TOOL_BLOCKED: TRADES_MAX_SLICE_COUNT_EXCEEDED"
            break
        if time.monotonic() - started > args.max_wall_clock_seconds:
            blocked_reason = "TOOL_BLOCKED: TRADES_MAX_WALL_CLOCK_EXCEEDED"
            break
        current_start, current_end = pending.pop(0)
        payload: dict[str, Any] | None = None
        record: dict[str, Any] = {}
        for attempt in range(args.retries_per_slice + 1):
            payload, record = query_trades(args, current_start, current_end, cutoff_ms, attempt)
            slice_records.append(record)
            if payload and record["exit_code"] == 0 and payload.get("ok") is True:
                break
        if not payload or record["exit_code"] != 0 or payload.get("ok") is not True:
            blocked_reason = "APP_BINDING_UNAVAILABLE" if "endpoint" in json.dumps(record).lower() else "TOOL_BLOCKED: TRADES_APP_READBACK_FAILED"
            break
        rows = extract_rows(payload)
        rows_seen += len(rows)
        if rows_seen > args.max_total_rows_processed:
            blocked_reason = "TOOL_BLOCKED: TRADES_MAX_TOTAL_ROWS_EXCEEDED"
            break
        if not payload_truncated(payload):
            complete_payloads.append(payload)
            continue
        duration = current_end - current_start
        if duration <= args.min_slice_ms:
            blocked_reason = "TOOL_BLOCKED: TRADES_SLICE_TRUNCATED_AT_MIN_WINDOW"
            break
        midpoint = current_start + duration // 2
        pending.insert(0, (midpoint, current_end))
        pending.insert(0, (current_start, midpoint))
    return complete_payloads, slice_records, blocked_reason


def build_observation(rows: list[dict[str, Any]], slices: list[dict[str, Any]], args: argparse.Namespace, complete: bool) -> dict[str, Any]:
    summary = summarize_rows(rows, args)
    result: dict[str, Any] = {
        "artifact_kind": "trades_fact_response.v1",
        "mode": args.mode,
        "symbol": args.symbol,
        "requested_start": args.start,
        "requested_end": args.end,
        "complete": complete,
        "facts": summary,
    }
    if args.mode == "adaptive_time_buckets":
        bucket_ms = int(args.bucket_ms or 0)
        result["bucket_ms"] = bucket_ms
        result["time_buckets"] = bucket_rows(rows, bucket_ms, args) if bucket_ms > 0 else []
    result["slice_count"] = len(slices)
    return result


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.max_rows > MAX_ROWS_HARD_CAP:
        return blocked_payload("max_rows exceeds hard cap 100000", args.request_id, args.evidence_cutoff)
    if args.mode not in VALID_MODES:
        return blocked_payload(f"unsupported mode: {args.mode}", args.request_id, args.evidence_cutoff)
    start_ms = parse_time_ms(args.start)
    end_ms = parse_time_ms(args.end)
    cutoff_ms = parse_time_ms(args.evidence_cutoff)
    if start_ms is None or end_ms is None or cutoff_ms is None or end_ms <= start_ms:
        return blocked_payload("valid --start, --end, and --evidence-cutoff are required", args.request_id, args.evidence_cutoff)
    if args.mode == "adaptive_time_buckets" and (args.bucket_ms is None or args.bucket_ms <= 0):
        return blocked_payload("--bucket-ms is required for adaptive_time_buckets", args.request_id, args.evidence_cutoff)

    raw_source_hashes: list[str] = []
    adaptive_slices: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    complete = False
    blocked_reason = ""
    source_ref = args.input or ""

    if args.input:
        raw = read_json(args.input)
        raw_source_hashes.append(file_digest(args.input))
        if payload_channel(raw) not in ("", "trades"):
            return blocked_payload("input payload is not trades channel", args.request_id, args.evidence_cutoff)
        if payload_truncated(raw):
            blocked_reason = "TOOL_BLOCKED: TRUNCATED_SAVED_PAYLOAD_NOT_COMPLETE"
            complete = False
        elif not coverage_ok(raw, start_ms, end_ms, cutoff_ms):
            blocked_reason = "TOOL_BLOCKED: SAVED_PAYLOAD_COVERAGE_NOT_PROVEN"
            complete = False
        else:
            rows = filter_rows(extract_rows(raw), start_ms, end_ms, cutoff_ms)
            adaptive_slices.append(
                {
                    "source_ref": args.input,
                    "response_hash": digest(raw),
                    "requested_start_ms": start_ms,
                    "requested_end_ms": end_ms,
                    "evidence_cutoff_ms": cutoff_ms,
                    "row_count": len(rows),
                    "truncated": False,
                    "source": payload_source(raw),
                    "channel": payload_channel(raw),
                    "known_at_policy": payload_known_at_policy(raw),
                }
            )
            complete = True
    else:
        if not args.cli_command or not args.app or not args.endpoint_dir or not args.symbol:
            return blocked_payload("--cli-command, --app, --endpoint-dir, and --symbol are required in app CLI mode", args.request_id, args.evidence_cutoff)
        payloads, adaptive_slices, blocked_reason = adaptive_query(args, start_ms, end_ms, cutoff_ms)
        for payload in payloads:
            raw_source_hashes.append(digest(payload))
            rows.extend(filter_rows(extract_rows(payload), start_ms, end_ms, cutoff_ms))
        complete = not blocked_reason

    rows = sorted(rows, key=lambda item: int(row_time_ms(item) or 0))
    status = "ok" if complete else ("partial" if rows else "blocked")
    observation = build_observation(rows, adaptive_slices, args, complete) if rows else {}
    raw_source_hash = ""
    if len(raw_source_hashes) == 1:
        raw_source_hash = raw_source_hashes[0]
    elif raw_source_hashes:
        raw_source_hash = digest(raw_source_hashes)
    normalized_source_hash = digest(
        {
            "mode": args.mode,
            "requested_start": args.start,
            "requested_end": args.end,
            "evidence_cutoff": args.evidence_cutoff,
            "price_low": args.price_low,
            "price_high": args.price_high,
            "bucket_ms": args.bucket_ms,
            "large_print_qty_threshold": args.large_print_qty_threshold,
            "rows": rows,
            "facts": observation.get("facts", {}) if observation else {},
        }
    ) if rows else ""
    return {
        "tool_id": TOOL_ID,
        "request_id": args.request_id,
        "response_id": "",
        "status": status,
        "source_ref": source_ref,
        "observation_summary": observation,
        "evidence_cutoff": args.evidence_cutoff,
        "cutoff_respected": all((row_known_at_ms(row) is not None and int(row_known_at_ms(row) or 0) <= cutoff_ms) for row in rows),
        "blocked_reason": blocked_reason,
        "adaptive_slices": adaptive_slices,
        "source_hashes": {
            "raw_source_hash": raw_source_hash,
            "normalized_source_hash": normalized_source_hash,
        },
        "legacy_source_hashes": raw_source_hashes,
        "hash_semantics": hash_semantics(),
        "forbidden_attestation": forbidden_attestation(),
    }


def make_mock_cli_script(path: Path) -> None:
    path.write_text(
        r'''
import json
import sys

def arg(name, default=""):
    if name not in sys.argv:
        return default
    return sys.argv[sys.argv.index(name) + 1]

start = int(arg("--from-ms", "0"))
end = int(arg("--to-ms", "0"))
mid = start + (end - start) // 2
truncated = (end - start) > 120000
rows = []
if not truncated:
    rows = [
        {"ts_ms": start, "known_at_ms": start, "trade_id": start, "price": 100.0, "qty": 1.0, "aggressor_side": "buy"},
        {"ts_ms": min(start + 30000, end - 1), "known_at_ms": min(start + 30000, end - 1), "trade_id": start + 1, "price": 101.0, "qty": 2.0, "aggressor_side": "sell"},
    ]
print(json.dumps({
    "ok": True,
    "read_model": "market_data_readback",
    "channel": "trades",
    "requested_range": {"from_ms": start, "to_ms": end, "as_of_ms": int(arg("--as-of-ms", str(end)))},
    "count": len(rows),
    "limit": {"requested_max_rows": int(arg("--max-rows", "100000")), "effective_max_rows": int(arg("--max-rows", "100000"))},
    "truncated": truncated,
    "source": {"channel_source": "mock_cli"},
    "known_at_policy": "row_known_at_lte_as_of_ms",
    "rows": rows,
}))
'''.lstrip(),
        encoding="utf-8",
    )


def self_test() -> dict[str, Any]:
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "lrf_trades_fact_minimal_fixture.json"
    args = argparse.Namespace(
        input=str(fixture),
        mode="slice_summary",
        start="1781280000000",
        end="1781280300000",
        evidence_cutoff="1781280300000",
        request_id="self-test",
        output=None,
        cli_command="",
        app="",
        endpoint_dir="",
        symbol="PerpUsdc:ETH-USDC",
        max_rows=100000,
        min_slice_ms=60000,
        max_slice_count=64,
        max_total_rows_processed=1000000,
        max_wall_clock_seconds=180,
        retries_per_slice=1,
        subprocess_timeout_seconds=30,
        bucket_ms=None,
        price_low=None,
        price_high=None,
        large_print_qty_threshold=None,
    )
    payload = build_payload(args)
    assert payload["status"] == "ok"
    assert payload["observation_summary"]["facts"]["count"] == 4
    assert payload["observation_summary"]["facts"]["side_qty"]["buy"] == 5.0
    assert payload["observation_summary"]["facts"]["side_qty"]["sell"] == 1.5

    args.mode = "price_zone_filter"
    args.price_low = 101.0
    args.price_high = 102.0
    payload = build_payload(args)
    facts = payload["observation_summary"]["facts"]
    assert payload["status"] == "ok"
    assert facts["count"] == 2
    assert facts["pre_filter_count"] == 4
    assert facts["filtered_out_count"] == 2
    assert facts["first_ts_ms"] == 1781280060000
    assert facts["last_ts_ms"] == 1781280120000
    assert facts["price_min"] == 101.0
    assert facts["price_max"] == 102.0
    args.mode = "slice_summary"
    args.price_low = None
    args.price_high = None

    truncated = read_json(str(fixture))
    truncated["truncated"] = True
    temp_dir = Path(tempfile.mkdtemp(prefix="trades-facts-self-test-"))
    truncated_path = temp_dir / "truncated.json"
    truncated_path.write_text(json.dumps(truncated), encoding="utf-8")
    args.input = str(truncated_path)
    payload = build_payload(args)
    assert payload["status"] in {"blocked", "partial"}
    assert payload["blocked_reason"] == "TOOL_BLOCKED: TRUNCATED_SAVED_PAYLOAD_NOT_COMPLETE"

    no_coverage = read_json(str(fixture))
    no_coverage.pop("requested_range", None)
    no_coverage_path = temp_dir / "no_coverage.json"
    no_coverage_path.write_text(json.dumps(no_coverage), encoding="utf-8")
    args.input = str(no_coverage_path)
    payload = build_payload(args)
    assert payload["status"] == "blocked"
    assert payload["blocked_reason"] == "TOOL_BLOCKED: SAVED_PAYLOAD_COVERAGE_NOT_PROVEN"

    mock_cli = temp_dir / "mock_cli.py"
    make_mock_cli_script(mock_cli)
    args.input = ""
    args.cli_command = sys.executable
    args.app = "pid:mock"
    args.endpoint_dir = str(temp_dir)
    args.symbol = "PerpUsdc:ETH-USDC"
    args.start = "1781280000000"
    args.end = "1781280240000"
    args.evidence_cutoff = "1781280240000"
    args.max_slice_count = 8

    original_query = query_trades

    def mock_query(mock_args: argparse.Namespace, start_ms: int, end_ms: int, cutoff_ms: int, attempt: int):
        mock_args = argparse.Namespace(**vars(mock_args))
        mock_args.cli_command = sys.executable
        argv = [
            sys.executable,
            str(mock_cli),
            "--app",
            mock_args.app,
            "trades",
            "get",
            "--symbol",
            mock_args.symbol,
            "--from-ms",
            str(start_ms),
            "--to-ms",
            str(end_ms),
            "--as-of-ms",
            str(cutoff_ms),
            "--max-rows",
            str(mock_args.max_rows),
        ]
        result = subprocess.run(argv, text=True, capture_output=True, timeout=10)
        payload = json.loads(result.stdout)
        record = {
            "argv": argv,
            "endpoint_binding_method": "FS_APP_ENDPOINT_DIR",
            "endpoint_dir": mock_args.endpoint_dir,
            "exit_code": result.returncode,
            "stdout_hash": text_hash(result.stdout),
            "stderr_hash": text_hash(result.stderr),
            "requested_start_ms": start_ms,
            "requested_end_ms": end_ms,
            "evidence_cutoff_ms": cutoff_ms,
            "requested_start_utc": ms_to_utc_iso(start_ms),
            "requested_end_utc": ms_to_utc_iso(end_ms),
            "evidence_cutoff_utc": ms_to_utc_iso(cutoff_ms),
            "max_rows": mock_args.max_rows,
            "row_count": len(extract_rows(payload)),
            "truncated": payload_truncated(payload),
            "source": payload_source(payload),
            "channel": payload_channel(payload),
            "known_at_policy": payload_known_at_policy(payload),
            "response_hash": digest(payload),
            "duration_ms": 0,
            "attempt": attempt,
        }
        return payload, record

    globals()["query_trades"] = mock_query
    try:
        payload = build_payload(args)
    finally:
        globals()["query_trades"] = original_query
    assert payload["status"] == "ok"
    assert len(payload["adaptive_slices"]) > 1
    assert any(item["truncated"] is True for item in payload["adaptive_slices"])
    assert payload["observation_summary"]["facts"]["count"] > 0
    return {"status": "pass", "tool_id": TOOL_ID, "fixture": str(fixture)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute deterministic trades facts from app-owned trades readback.")
    parser.add_argument("--input", help="Saved app-owned trades payload JSON.")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), default="slice_summary")
    parser.add_argument("--cli-command", default="", help="Explicit flowsight-cli executable path for real app mode.")
    parser.add_argument("--app", default="", help="Explicit app selector.")
    parser.add_argument("--endpoint-dir", default="", help="Explicit endpoint directory for FS_APP_ENDPOINT_DIR.")
    parser.add_argument("--symbol", default="", help="Symbol for app CLI mode.")
    parser.add_argument("--start", default="", help="Inclusive start timestamp/ms.")
    parser.add_argument("--end", default="", help="Exclusive end timestamp/ms.")
    parser.add_argument("--evidence-cutoff", default="", help="Known-at/as-of cutoff timestamp/ms.")
    parser.add_argument("--max-rows", type=int, default=100000)
    parser.add_argument("--min-slice-ms", type=int, default=60000)
    parser.add_argument("--max-slice-count", type=int, default=64)
    parser.add_argument("--max-total-rows-processed", type=int, default=1000000)
    parser.add_argument("--max-wall-clock-seconds", type=int, default=180)
    parser.add_argument("--retries-per-slice", type=int, default=1)
    parser.add_argument("--subprocess-timeout-seconds", type=int, default=30)
    parser.add_argument("--bucket-ms", type=int, default=None)
    parser.add_argument("--price-low", type=float, default=None)
    parser.add_argument("--price-high", type=float, default=None)
    parser.add_argument("--large-print-qty-threshold", type=float, default=None)
    parser.add_argument("--request-id", default="")
    parser.add_argument("--output")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    payload = build_payload(args)
    emit(payload, args.output)
    return 0 if payload["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
