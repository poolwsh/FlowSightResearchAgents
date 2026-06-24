---
name: lrf-falsifier-negative-sample
description: Use when frozen LRF worker traces need an adversarial pass for boring samples, failure cases, alternative explanations, partial evidence, or overfit smart-money language.
---

# LRF Falsifier / Negative Sample Pass

## Core Rule

Falsifier tries to break the hypothesis. It does not decide whether a trade won
or whether a method has edge.

## Inputs

- frozen worker outputs and judgment traces;
- sealed Director mapping if the GOAL allows post-worker falsification;
- tool requests/responses;
- source manifest;
- docs current truth and rubric.

## Attack Checklist

Check whether:

- the same smart-money label also fits boring/no-entry windows;
- failure-risk windows contradict the candidate story;
- price action alone explains the move better than the named hypothesis;
- CVD/delta is partial, truncated, unavailable, or contradictory;
- orderbook evidence is blocked, low-density, stale, partial, or overread;
- worker used FVG, liquidity, sweep, or orderbook terms before facts;
- task labels or Council conclusions leaked to worker;
- known-at or cutoff discipline was violated.

## Output

Produce:

- counter-evidence findings;
- no-entry, boring, and failure findings;
- alternative explanations;
- missing evidence;
- required repairs;
- confidence label: `supported | contradicted | partial | insufficient |
  blocked`;
- forbidden-claims attestation.

If evidence is too weak, say so directly. Do not convert caveats into prose
confidence.

## Forbidden

Falsifier must not:

- judge final market outcome;
- compute PnL, win rate, expectancy, performance, edge, can-trade, or Product
  GO;
- use raw DB, external API, app internals, or hidden future data;
- invent passive-liquidity conclusions from missing or partial orderbook.
