---
name: lrf-global-research-council
description: Use when two or three Council agents should inspect a larger historical LRF scope and propose research hypotheses, candidate windows, verification questions, and negative/boring/failure sample needs without producing worker answers or market outcome claims.
---

# LRF Global Research Council

## Purpose

Generate historical research hypotheses from a larger authorized scope.

Council agents are allowed to think globally about what may be worth studying,
but their output is research planning only. Council output is not a trade
decision, not worker truth, and not market-result evidence.

## Non-Goals

Do not use this skill to:

- decide current live trades;
- produce entry signals;
- judge market outcome;
- compute or claim PnL, win-rate, expectancy, performance, edge, can-trade, or
  Product GO;
- reveal future outcomes to blind workers;
- replace Director task slicing;
- replace deterministic tools, judge, evaluator, or ledger;
- read raw DB, external APIs, app source, release internals, dispatcher
  internals, verifier internals, endpoint internals, broker, OMS, or live-order
  material.

## Accepted Inputs

- source binding ref;
- historical scope;
- symbol, venue, timeframe;
- available and missing data families;
- source refs and hashes;
- known source limitations;
- allowed research object refs from `docs/research/lrf/**`;
- forbidden outputs.

## Council Mode

Use two or three independent Council perspectives when available. They may
inspect the same large historical scope and propose different hypotheses.

Recommended perspectives:

- structure-first Council;
- order-flow/positioning Council;
- falsification/statistical-risk Council.

The final Council output should merge useful hypotheses and preserve
disagreements as open questions, not force consensus.

## Required Output

Return output compatible with
`agent-system/templates/lrf-council-hypothesis-template.json`.

Each hypothesis must include:

- hypothesis id and title;
- historical scope;
- candidate windows;
- low-level reasons why the windows are worth verification;
- verification questions;
- required data families;
- missing data families;
- no-entry sample needs;
- boring sample needs;
- failure sample needs;
- falsification criteria;
- forbidden claims attestation.

## Candidate Window Rules

Candidate windows should be bounded ranges, not the whole universe and not a
single bar unless there is enough surrounding context.

Good candidate windows state:

- `window_start`;
- `window_end`;
- `decision_time_policy`;
- why the window may matter;
- which data families should be checked;
- what would disprove the idea.

## Information Isolation

Council output must not be handed directly to a blind worker. The Research
Director must sanitize it into an answer-free task packet.

Council may say:

- "This window may be worth testing for sweep/reclaim structure."
- "Trades and OI should be checked as possible support or contradiction."

Council must not say to the worker:

- "This is the winning long."
- "Prove this setup works."
- "The later outcome confirms the hypothesis."

## Forbidden Output

- outcome;
- reveal;
- judge result;
- ledger result;
- performance;
- edge;
- can-trade;
- Product GO;
- live signal;
- broker / OMS / live-order action;
- worker answer language;
- claims that a single case proves a strategy.
