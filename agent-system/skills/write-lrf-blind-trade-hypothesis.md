---
name: write-lrf-blind-trade-hypothesis
description: Use when a bounded Codex native subagent must write an LRF trade hypothesis from an answer-free known-at packet.
---

# Write LRF Blind Trade Hypothesis

Status: active_contract
Goal: r-goal-lrf-phase2-active-workflow-skills-v0
Updated: 2026-06-20

## Purpose

This bounded task prompt makes a Codex native subagent write an LRF trade
hypothesis from a frozen answer-free known-at packet. It defines the research
object; it does not judge whether the hypothesis later worked.

## Trigger

Use only from `lrf-blind-trade-hypothesis-research-workflow.md` after:

- Client Mirror First has completed;
- an answer-free known-at packet exists;
- the packet has been checked for forbidden future/reveal/outcome fields;
- the packet is ready to freeze for blind subagent work.

## Allowed Input

- The frozen answer-free packet.
- Packet source refs and hashes.
- Known-at fields available before entry/freeze.
- Missing-evidence and blocker status.

## Forbidden Input

- reveal;
- future path;
- outcome;
- success/failure label;
- post-reveal comparison;
- judge result;
- performance;
- raw DB;
- external API;
- FlowSight app source, verifier, release, dispatcher, endpoint implementation,
  broker, OMS, exchange, live-order, or account data.

## Task

Write one blind LRF trade hypothesis that is fully fieldized. If the packet does
not support a complete hypothesis, return `blocked` or `needs_data` and explain
which required fields are missing.

## Required Output

```yaml
write_lrf_blind_trade_hypothesis:
  observed_fact: []
  hypothesis: ""
  premise: ""
  setup_context:
    liquidity: ""
    OB: ""
    FVG: ""
    lost_zone: ""
    breaker: ""
    displacement: ""
  entry_trigger: ""
  entry_price_rule: ""
  invalidation_condition: ""
  stop_rule: ""
  exit_or_target_rule: ""
  cancel_condition: ""
  no_entry_condition: ""
  time_stop: ""
  cost_model_ref: ""
  missing_evidence: []
  blocker_classification: "APP_BLOCKED | DATA_BLOCKED | R_APP_USAGE_GAP | R_METHOD_GAP | OWNER_POLICY_GAP | none"
  confidence_label: "likely | possible | ambiguous | not_supported | blocked | needs_data"
  forbidden_claim_attestation:
    no_reveal_seen: true
    no_outcome_seen: true
    no_raw_db_or_external_api: true
    no_edge_claim: true
    no_can_trade_claim: true
    no_product_go_claim: true
```

## Discipline Rules

- Separate `observed_fact` from `hypothesis`.
- Do not call an incomplete field set a complete trade hypothesis.
- Do not infer trades/OI/FR/orderbook evidence from OHLCV prose.
- Use `ambiguous`, `blocked`, or `needs_data` when evidence is insufficient.
- Include no-entry and cancel logic even when the setup looks promising.
- Entry, stop, and exit fields are research fields, not trade commands.

## Common Mistakes

- Treating a range breakout as enough for a complete hypothesis.
- Omitting stop, invalidation, cancel, or no-entry.
- Writing the hypothesis as if future movement is known.
- Turning a structural candidate into edge, can-trade, Product GO, or
  performance language.
