---
name: lrf-falsifier-negative-sample
description: Use when an LRF hypothesis or worker judgment needs an answer-free adversarial pass that searches for counter evidence, no-entry, boring, failure, and alternative explanations without judging market outcome.
---

# LRF Falsifier / Negative Sample

## Purpose

Attack a Council or worker hypothesis before reveal.

The falsifier uses bounded known-at evidence to find reasons the hypothesis may
be weak, overfit, ambiguous, incomplete, or not worth continuing.

## Non-Goals

Do not use this skill to:

- judge whether the setup won or lost;
- compute PnL, win-rate, expectancy, performance, edge, can-trade, or Product
  GO;
- run reveal, deterministic judge, evaluator, or ledger;
- repair the hypothesis by writing better market prose;
- read raw DB, external APIs, app source, release internals, verifier internals,
  dispatcher internals, endpoint internals, broker, OMS, or live-order paths.

## Accepted Inputs

- Director task packet;
- source binding ref;
- hypothesis ref;
- worker judgment traces, if available;
- allowed tool responses or allowed tool registry;
- known-at policy;
- missing evidence notes;
- forbidden outputs.

## Required Work

Check for:

- counter evidence;
- no-entry reasons;
- boring samples;
- failure samples;
- alternative explanations;
- missing data families;
- weak or overly broad rules;
- partial or truncated evidence used too strongly;
- one-case overfitting;
- conflict from trades, OI, funding, or other allowed data families.

## Required Output

Return output compatible with
`agent-system/templates/lrf-falsifier-output-template.json`.

Minimum fields:

- `falsifier_output_id`;
- `director_task_ref`;
- `hypothesis_ref`;
- `counter_evidence`;
- `no_entry_findings`;
- `boring_sample_findings`;
- `failure_sample_findings`;
- `alternative_explanations`;
- `missing_evidence`;
- `confidence_label`;
- `forbidden_future_attestation`.

## Forbidden Output

- market result judgment;
- win/loss;
- outcome;
- reveal;
- judge result;
- ledger result;
- performance;
- edge;
- can-trade;
- Product GO;
- live signal;
- broker / OMS / live-order action.
