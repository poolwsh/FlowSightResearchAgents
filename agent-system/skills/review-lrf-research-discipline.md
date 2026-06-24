---
name: review-lrf-research-discipline
description: Use when auditing an LRF Council/Director/Blind Worker/Falsifier run for docs authority, isolation, known-at evidence, response identity, partial evidence handling, and forbidden claims.
---

# Review LRF Research Discipline

## Core Rule

Reviewer audits process discipline. Reviewer does not judge market outcome and
does not decide profitability.

## Review Scope

Check the run against:

- accepted docs current truth;
- reviewed GOAL scope;
- source binding and known-at policy;
- actor isolation;
- canonical tool response identity;
- partial/truncated/orderbook downgrade rules;
- forbidden claims boundary.

## Required Checks

### Authority

- Workflow starts from research thesis and current framework.
- No lower-layer artifact rewrites thesis/framework during execution.
- Any framework issue is recorded as blocker, counterexample, or docs-change
  proposal.

### Actor Isolation

- Council and Director are distinct roles.
- Director task packets use neutral `blind_task_id`.
- Worker-visible artifacts do not expose sealed candidate/boring/failure labels.
- Main R did not substitute role judgment.

### Evidence Linkage

Every cited fact must resolve to a tool response with:

- canonical `response_id`;
- `identity.response_id_source`;
- `request_id`;
- `output_hash`;
- `source_hashes.raw_source_hash`;
- `source_hashes.normalized_source_hash`;
- evidence cutoff and `cutoff_respected`;
- completeness / partial / blocked status.

No trace may rely on line number, argv, or prose summary as primary evidence.

### Judgment Order

Worker traces must follow:

```text
price_action_context
  -> aggressive_flow_state
  -> passive_liquidity_state
  -> smart_money_hypothesis_status
```

Smart-money labels cannot appear as proof before price and order-flow facts.

### Partial Evidence

- Truncated trades cannot be complete CVD/delta proof.
- Missing side field means unknown side, not inferred aggression.
- Partial or blocked orderbook cannot confirm absorption, distribution, support,
  or resistance.
- Blocked evidence must remain blocked or insufficient.

### Forbidden Claims

Flag any claim of performance, edge, can-trade, Product GO, live signal, broker,
OMS, exchange, or live-order action.

## Verdicts

Use:

- `pass`
- `needs_fix`
- `typed_blocker`
- `out_of_scope`

Reviewer pass means process discipline passed. It does not mean the market idea
works.
