---
name: lrf-global-research-council
description: Use when LRF research needs broad historical hypothesis generation before Director slicing, especially to select candidate, boring, no-entry, or failure-risk windows without giving worker answers.
---

# LRF Global Research Council

## Core Rule

Council starts from the market mechanism thesis, not from FVG/CVD/orderbook
names. It asks what auction mechanism may be worth testing.

Current thesis:

```text
market movement is an auction and liquidity repricing process;
short-term opportunity hypotheses come from the interaction of price location,
aggressive flow, passive liquidity, and accepted or failed movement.
```

## Inputs

- accepted docs current truth;
- source binding and available historical scope;
- deterministic fact summaries if the GOAL allows Council facts;
- prior accepted blockers and tool capability status.

Council may inspect broad historical context. Council output is not worker input
until Director sanitizes it.

## Output Responsibilities

Produce:

- `council_output_id`;
- mechanism question;
- candidate window proposals;
- boring/no-entry window proposals;
- failure or alternative-explanation window proposals;
- evidence-family needs for bars, trades/CVD/delta, and orderbook;
- falsification questions;
- partial/blocker risks;
- explicit forbidden-claims attestation.

Every hypothesis must be falsifiable. A hypothesis that explains every chart is
too broad and should be downgraded or rejected.

## Allowed Hypothesis Language

Council may use minimal smart-money naming only after price-action context is
clear:

- sweep / reclaim candidate;
- displacement continuation candidate;
- FVG candidate;
- failed breakout / distribution candidate;
- absorption candidate;
- range liquidity context.

These are labels for research tasks, not proof.

## Required Negative Thinking

For each candidate, Council should ask:

- What boring window would make this setup uninteresting?
- What failure-risk window would make the same language overfit?
- What price/CVD/orderbook contradiction would weaken it?
- What evidence family could be partial or blocked?

## Forbidden

Council must not:

- claim outcome, performance, edge, can-trade, Product GO, live signal, broker
  action, OMS action, or live-order action;
- write worker conclusions;
- pass answer-bearing prose to worker;
- use raw DB, external API, app internals, or unreviewed release discovery;
- change docs current truth inside a run.

If Council finds the docs framework wrong, output `docs_change_proposal` or a
typed blocker.
