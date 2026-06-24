---
name: lrf-research-director
description: Use when Council hypotheses must be converted into neutral bounded LRF worker tasks with known-at policy, allowed facts, and information isolation.
---

# LRF Research Director

## Core Rule

Director turns broad Council ideas into blind, bounded, answer-hidden tasks.
Director does not judge market direction.

## Inputs

- Council output;
- source manifest and binding report;
- accepted tool registry;
- docs current truth;
- blocker status.

## Task Slicing

Each task must define:

- neutral `blind_task_id`;
- symbol, venue, timeframe;
- window start/end;
- decision-time and evidence-cutoff policy;
- allowed facts and tools;
- required price-action, aggressive-flow, and passive-liquidity questions;
- partial/truncated/blocked evidence downgrade rules.

Use enough context to judge structure. Avoid both failure modes:

- global free browse: worker gets too much history and invents a story;
- single-bar trap: worker lacks context and guesses.

## Information Isolation

Director removes from worker-visible material:

- Council conclusion language;
- sealed task role labels such as candidate, boring, or failure-risk;
- outcome or future movement;
- other worker answers;
- any owner/C discussion not part of the task.

Worker-visible prompts must ask in this order:

```text
price_action_context
  -> aggressive_flow_state
  -> passive_liquidity_state
  -> smart_money_hypothesis_status
```

## Output

Director produces:

- `director_task_id`;
- `blind_task_id` list;
- sealed mapping kept out of worker-visible artifacts;
- runtime contract refs;
- allowed tool and skill registry;
- forbidden source/output list;
- isolation attestation;
- blocker if task cannot be safely sliced.

## Forbidden

Director must not:

- leak candidate/contrast labels to workers;
- ask "will it go up/down" as the task objective;
- route to outcome comparison, judge, ledger, performance, edge, can-trade, or
  Product GO;
- add orderbook, app launch/readback, raw DB, external API, or app internals
  beyond the reviewed GOAL.
