---
name: lrf-price-cvd-orderbook-judgment-rubric
description: Use when an LRF Blind Worker must judge a bounded historical window using price action, CVD/delta or trades aggression, and orderbook passive-liquidity evidence.
---

# LRF Price + CVD/Delta + Orderbook Judgment Rubric

## Core Rule

Always judge in this order:

```text
price_action_context
  -> aggressive_flow_state
  -> passive_liquidity_state
  -> smart_money_hypothesis_status
```

Do not begin with FVG, order block, liquidity, sweep, absorption, or
distribution words and then backfill facts.

## Layer 0: Price Action Context

Answer what structure the price is in:

- range high / range low;
- breakout or breakdown;
- sweep / reclaim;
- displacement;
- acceptance / rejection;
- pullback / retest;
- failed breakout;
- consolidation or compression.

Price action is context, not a trade permission.

## Layer 1A: Aggressive Flow

Use trades/CVD/delta facts only when source coverage and truncation permit.

Allowed facts:

- fixed time bucket buy/sell/unknown quantities;
- net aggressive quantity where side is explicit;
- cumulative delta from complete slices;
- volume concentration near the structure;
- price-CVD divergence;
- VWAP, price min/max, trade count.

If side is unavailable, write `delta_unavailable`. If slices are truncated,
write `partial_aggressive_flow_evidence` or blocked.

## Layer 1B: Passive Liquidity

Use orderbook/book-depth facts only as low-level passive-liquidity evidence.

Allowed facts:

- snapshot count and density;
- spread;
- best bid/ask drift;
- top-N bid/ask depth;
- depth imbalance;
- wall presence by explicit numeric rule;
- replenish / withdraw / consume proxy if the fact response defines it;
- coverage, truncation, timeout, and stability status.

Orderbook evidence may be `complete`, `partial`, `blocked`, or `insufficient`.
Partial orderbook cannot confirm absorption or distribution.

## Layer 2: Smart-Money Hypothesis Status

Only after Layers 0 and 1, assign one status:

- `hypothesis_supported`;
- `hypothesis_contradicted`;
- `hypothesis_partial`;
- `evidence_insufficient`;
- `blocked`.

Allowed minimal hypothesis names:

- sweep / reclaim candidate;
- displacement continuation candidate;
- FVG candidate;
- failed breakout / distribution candidate;
- absorption candidate;
- range liquidity context.

These names classify the observation. They do not prove outcome.

## Required Trace Fields

Each judgment trace includes:

- `blind_task_id`;
- `price_action_context`;
- `aggressive_flow_state`;
- `passive_liquidity_state`;
- `smart_money_hypothesis_status`;
- supporting facts by canonical `response_id`;
- contradicting facts;
- partial or blocked evidence;
- alternative explanations;
- confidence label;
- forbidden claims attestation.

## Downgrade Rules

- No deterministic fact refs: `evidence_insufficient`.
- Truncated trades: no complete delta/CVD confirmation.
- Unknown side: do not infer buy/sell aggression.
- Missing orderbook: `passive_liquidity_state=blocked | insufficient`.
- Low-density orderbook: partial only.
- Smart-money label with weak facts: `hypothesis_partial` or
  `evidence_insufficient`.

## Forbidden

Do not output:

- absorption confirmed;
- distribution confirmed;
- smart-money action confirmed;
- will rise / will fall certainty;
- stop, target, win, loss, PnL;
- performance, edge, can-trade, Product GO;
- broker, OMS, exchange, or live-order action.
