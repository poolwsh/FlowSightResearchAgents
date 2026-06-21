#!/usr/bin/env python
"""Compute deterministic OHLCV facts from an app-owned bars export artifact."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


TOOL_ID = "ohlcv_facts"
VALID_MODES = {"bars_slice", "bar_lookup", "range_stats", "wick_close_back_fact"}


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
        "no_smart_money_final_label": True,
    }


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ms_to_utc_iso(value: Any) -> str:
    try:
        millis = int(value)
    except (TypeError, ValueError):
        return ""
    return datetime.fromtimestamp(millis / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_phase5_bar(row: dict[str, Any]) -> dict[str, Any] | None:
    time_value = row.get("time") or ms_to_utc_iso(row.get("open_time_ms"))
    required = ("open", "high", "low", "close", "volume")
    if not time_value or any(key not in row for key in required):
        return None
    return {
        "time": time_value,
        "open": row["open"],
        "high": row["high"],
        "low": row["low"],
        "close": row["close"],
        "volume": row["volume"],
        "source_open_time_ms": row.get("open_time_ms", ""),
        "source_close_time_ms": row.get("close_time_ms", ""),
    }


def normalize_bars(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        return []
    return [
        normalized
        for row in rows
        if isinstance(row, dict)
        for normalized in [normalize_phase5_bar(row)]
        if normalized is not None
    ]


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
        "observation_summary": {},
        "evidence_cutoff": evidence_cutoff,
        "cutoff_respected": True,
        "blocked_reason": reason,
        "forbidden_attestation": forbidden_attestation(),
    }


def extract_export(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict) and "bars_export" in raw and isinstance(raw["bars_export"], dict):
        return raw["bars_export"]
    if isinstance(raw, dict) and isinstance(raw.get("data"), dict) and isinstance(raw["data"].get("bars"), list):
        data = raw["data"]
        return {
            "symbol": data.get("symbol", raw.get("symbol", "")),
            "venue": data.get("venue", raw.get("venue", "")),
            "timeframe": data.get("timeframe", raw.get("timeframe", "")),
            "source_shape": "data.bars",
            "bars": normalize_bars(data["bars"]),
        }
    if isinstance(raw, dict) and isinstance(raw.get("ohlcv"), list):
        return {
            "symbol": raw.get("symbol", ""),
            "venue": raw.get("venue", ""),
            "timeframe": raw.get("timeframe", ""),
            "source_shape": "ohlcv",
            "bars": normalize_bars(raw["ohlcv"]),
        }
    if isinstance(raw, dict) and isinstance(raw.get("known_at_ohlcv_bars"), list):
        bounded_window = raw.get("bounded_window") if isinstance(raw.get("bounded_window"), dict) else {}
        metadata = {
            "symbol": bounded_window.get("symbol", raw.get("symbol", "")),
            "venue": bounded_window.get("venue", raw.get("venue", "")),
            "timeframe": bounded_window.get("timeframe", raw.get("timeframe", "")),
            "source_shape": "known_at_ohlcv_bars",
        }
        metadata["bars"] = normalize_bars(raw["known_at_ohlcv_bars"])
        return metadata
    if isinstance(raw, dict):
        return raw
    return {"bars": []}


def bars_from_export(raw: Any) -> list[dict[str, Any]]:
    export = extract_export(raw)
    bars = export.get("bars") or []
    return sorted([bar for bar in bars if isinstance(bar, dict) and "time" in bar], key=lambda item: str(item.get("time", "")))


def in_window(bar: dict[str, Any], start: str, end: str, cutoff: str) -> bool:
    time_value = str(bar.get("time", ""))
    if start and time_value < start:
        return False
    if end and time_value > end:
        return False
    if cutoff and time_value > cutoff:
        return False
    return True


def select_bars(raw: Any, start: str, end: str, cutoff: str) -> list[dict[str, Any]]:
    return [bar for bar in bars_from_export(raw) if in_window(bar, start, end, cutoff)]


def range_stats(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if not bars:
        return {"bar_count": 0}
    highs = [float(bar["high"]) for bar in bars if "high" in bar]
    lows = [float(bar["low"]) for bar in bars if "low" in bar]
    volumes = [float(bar.get("volume", 0)) for bar in bars]
    return {
        "bar_count": len(bars),
        "first_bar_time": bars[0].get("time", ""),
        "last_bar_time": bars[-1].get("time", ""),
        "open_first": bars[0].get("open", ""),
        "close_last": bars[-1].get("close", ""),
        "high_max": max(highs) if highs else "",
        "low_min": min(lows) if lows else "",
        "volume_sum": sum(volumes),
    }


def bar_lookup(all_bars: list[dict[str, Any]], timestamp: str, cutoff: str) -> dict[str, Any]:
    eligible = [bar for bar in all_bars if (not cutoff or str(bar.get("time", "")) <= cutoff)]
    exact = [bar for bar in eligible if str(bar.get("time", "")) == timestamp]
    before = [bar for bar in eligible if str(bar.get("time", "")) <= timestamp]
    after = [bar for bar in eligible if str(bar.get("time", "")) >= timestamp]
    return {
        "target_timestamp": timestamp,
        "exact_matches": exact,
        "nearest_before": before[-1] if before else {},
        "nearest_after": after[0] if after else {},
    }


def wick_close_back_facts(bars: list[dict[str, Any]], price_high: float | None, price_low: float | None) -> dict[str, Any]:
    facts: list[dict[str, Any]] = []
    for bar in bars:
        high = float(bar.get("high", 0))
        low = float(bar.get("low", 0))
        close = float(bar.get("close", 0))
        fact = {
            "bar_time": bar.get("time", ""),
            "high": high,
            "low": low,
            "close": close,
            "price_high": price_high,
            "price_low": price_low,
            "wick_above_price_high": bool(price_high is not None and high > price_high),
            "close_back_below_price_high": bool(price_high is not None and high > price_high and close <= price_high),
            "wick_below_price_low": bool(price_low is not None and low < price_low),
            "close_back_above_price_low": bool(price_low is not None and low < price_low and close >= price_low),
        }
        if (
            fact["wick_above_price_high"]
            or fact["close_back_below_price_high"]
            or fact["wick_below_price_low"]
            or fact["close_back_above_price_low"]
        ):
            facts.append(fact)
    return {
        "fact_count": len(facts),
        "facts": facts,
        "label_boundary": "deterministic wick/close facts only; no smart-money final label",
    }


def build_payload(args: argparse.Namespace, raw: Any) -> dict[str, Any]:
    selected = select_bars(raw, args.start, args.end, args.evidence_cutoff)
    export = extract_export(raw)
    source_hash = digest(raw)
    if args.mode == "bars_slice":
        summary: dict[str, Any] = {
            "mode": args.mode,
            "bars": selected,
            "stats": range_stats(selected),
        }
    elif args.mode == "bar_lookup":
        summary = {"mode": args.mode, "lookup": bar_lookup(bars_from_export(raw), args.timestamp, args.evidence_cutoff)}
    elif args.mode == "range_stats":
        summary = {"mode": args.mode, "stats": range_stats(selected)}
    elif args.mode == "wick_close_back_fact":
        summary = {
            "mode": args.mode,
            "wick_close_back_fact": wick_close_back_facts(selected, args.price_high, args.price_low),
        }
    else:
        return blocked_payload(f"unsupported mode: {args.mode}", args.request_id, args.evidence_cutoff)
    return {
        "tool_id": TOOL_ID,
        "request_id": args.request_id,
        "status": "ok",
        "source_ref": args.input,
        "observation_summary": {
            "artifact_kind": "ohlcv_fact_response.v1",
            "source_hash": source_hash,
            "symbol": export.get("symbol", ""),
            "venue": export.get("venue", ""),
            "timeframe": export.get("timeframe", ""),
            "requested_start": args.start,
            "requested_end": args.end,
            "mode_result": summary,
        },
        "evidence_cutoff": args.evidence_cutoff,
        "cutoff_respected": all(not args.evidence_cutoff or str(bar.get("time", "")) <= args.evidence_cutoff for bar in selected),
        "blocked_reason": "",
        "forbidden_attestation": forbidden_attestation(),
    }


def self_test() -> dict[str, Any]:
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "lrf_ohlcv_fact_minimal_fixture.json"
    raw = read_json(str(fixture))
    class Args:
        input = str(fixture)
        request_id = "self-test"
        start = "2026-06-11T00:00:00Z"
        end = "2026-06-11T00:20:00Z"
        evidence_cutoff = "2026-06-11T00:20:00Z"
        timestamp = "2026-06-11T00:05:00Z"
        price_high = 102.5
        price_low = 98.0
        mode = "range_stats"

    args = Args()
    payload = build_payload(args, raw)
    assert payload["status"] == "ok"
    assert payload["observation_summary"]["mode_result"]["stats"]["bar_count"] == 5
    args.mode = "bar_lookup"
    payload = build_payload(args, raw)
    assert payload["observation_summary"]["mode_result"]["lookup"]["exact_matches"]
    args.mode = "wick_close_back_fact"
    payload = build_payload(args, raw)
    facts = payload["observation_summary"]["mode_result"]["wick_close_back_fact"]["facts"]
    assert any(item["close_back_below_price_high"] for item in facts)
    assert any(item["close_back_above_price_low"] for item in facts)
    return {"status": "pass", "tool_id": TOOL_ID, "fixture": str(fixture)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute deterministic OHLCV facts from an app-owned bars export.")
    parser.add_argument("--input", help="App-owned bars export JSON.")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), help="Fact mode.")
    parser.add_argument("--start", default="", help="Inclusive start timestamp.")
    parser.add_argument("--end", default="", help="Inclusive end timestamp.")
    parser.add_argument("--timestamp", default="", help="Timestamp for bar_lookup.")
    parser.add_argument("--price-high", type=float, default=None, help="High-side price for wick/close fact.")
    parser.add_argument("--price-low", type=float, default=None, help="Low-side price for wick/close fact.")
    parser.add_argument("--evidence-cutoff", default="", help="Known-at cutoff; bars after this are ignored.")
    parser.add_argument("--request-id", default="", help="Optional broker request id.")
    parser.add_argument("--output", help="Optional output JSON path.")
    parser.add_argument("--self-test", action="store_true", help="Run synthetic fixture self-test.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if not args.input or not args.mode:
        emit(blocked_payload("--input and --mode are required", args.request_id, args.evidence_cutoff), args.output)
        return 2
    raw = read_json(args.input)
    payload = build_payload(args, raw)
    emit(payload, args.output)
    return 0 if payload["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
