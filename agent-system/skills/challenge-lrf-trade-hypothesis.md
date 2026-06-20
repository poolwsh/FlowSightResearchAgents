---
name: challenge-lrf-trade-hypothesis
description: Use when a bounded Codex native subagent must attack an LRF trade hypothesis without reveal or outcome access.
---

# Challenge LRF Trade Hypothesis

Status: active_contract
Goal: r-goal-lrf-phase2-active-workflow-skills-v0
Updated: 2026-06-20

## Purpose

This bounded task prompt makes a Codex native subagent attack a frozen LRF trade
hypothesis using the same answer-free packet. It is adversarial, but still blind:
it must not see reveal, outcome, judge result, or post-reveal comparison.

## Trigger

Use only from `lrf-blind-trade-hypothesis-research-workflow.md` after:

- the answer-free packet is frozen;
- the blind hypothesis output is available or frozen;
- both inputs are still answer-free.

## Allowed Input

- The same frozen answer-free packet used by the hypothesis writer.
- The frozen blind hypothesis output.
- Packet and hypothesis refs/hashes.

## Forbidden Input

- reveal;
- future path;
- outcome;
- judge result;
- post-reveal comparison;
- performance;
- raw DB;
- external API;
- FlowSight app source, verifier, release, dispatcher, endpoint implementation,
  broker, OMS, exchange, live-order, or account data.

## Challenge Focus

Attack the hypothesis on:

- fake breakout risk;
- weak premise;
- invalid entry trigger;
- missing stop or invalidation;
- unrealistic exit or target;
- cost too high;
- no-entry overlooked;
- missing trades/OI/FR/orderbook;
- overclaim and hindsight risk.

## Required Output

```yaml
challenge_lrf_trade_hypothesis:
  challenged_claims: []
  supported_challenges: []
  unsupported_or_ambiguous_challenges: []
  missing_evidence: []
  blocker_classification: "APP_BLOCKED | DATA_BLOCKED | R_APP_USAGE_GAP | R_METHOD_GAP | OWNER_POLICY_GAP | none"
  overclaim_risk:
    level: "low | medium | high | blocker"
    reasons: []
  confidence_label: "likely | possible | ambiguous | not_supported | blocked | needs_data"
  forbidden_claim_attestation:
    no_reveal_seen: true
    no_outcome_seen: true
    no_market_result_judgment: true
    no_raw_db_or_external_api: true
    no_edge_claim: true
    no_can_trade_claim: true
    no_product_go_claim: true
```

## Discipline Rules

- Challenge evidence and logic; do not judge whether the trade worked.
- Preserve ambiguity when the packet lacks trades/OI/FR/orderbook.
- Do not replace missing deterministic judge/evaluator with subagent opinion.
- If the hypothesis lacks entry, stop, exit, cancel, or no-entry, classify the
  issue as `R_METHOD_GAP`.
- If the packet cannot support the challenge either, put it under
  `unsupported_or_ambiguous_challenges`.

## Common Mistakes

- Using hindsight language to attack a blind hypothesis.
- Saying a hypothesis failed or succeeded without reveal authorization.
- Treating the adversarial role as the market judge.
- Turning missing evidence into a confident rejection instead of `needs_data`.
