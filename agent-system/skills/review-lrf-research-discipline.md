---
name: review-lrf-research-discipline
description: Use when R or a reviewer worker must audit the LRF Council/Director/Blind Worker/Falsifier chain for information isolation, known-at discipline, source refs, tool response linkage, truncation handling, overclaim, and reviewer-as-judge violations.
---

# Review LRF Research Discipline

## Purpose

Audit whether an LRF historical research attempt followed the accepted
Council / Director / Blind Worker / Falsifier workflow.

This review checks process discipline. It does not decide whether a market
hypothesis was profitable, whether an entry would have worked, or whether a
strategy has edge.

## Accepted Inputs

- source binding ref;
- Council output;
- Director task packet;
- research runtime contract;
- allowed tool registry;
- allowed skill registry;
- tool requests;
- tool responses;
- judgment traces;
- falsifier output;
- validation report.

## Review Checks

### Council Boundary

- Council output is research planning, not worker truth.
- Council did not include outcome, reveal, performance, edge, can-trade,
  Product GO, live signal, broker, OMS, or live-order claims.
- Council candidate windows include verification questions and falsification
  needs.

### Director Sanitization

- Director converted Council output into bounded worker tasks.
- Director removed conclusion language and future outcome hints.
- Director did not give worker a global free-browse universe.
- Director did not give worker only a single bar without enough context.
- Director preserved known-at policy and forbidden sources/outputs.

### Worker Trace Discipline

- Worker used only allowed tools and rubrics.
- Every non-trivial judgment has a `judgment_trace`.
- Trace fields include decision time, evidence cutoff, observed facts, tool
  response refs, rule clauses, reasoning chain, counter evidence, missing
  evidence, confidence, and forbidden future attestation.

### Tool Response Linkage

- Every observed fact resolves to a tool response.
- Tool responses contain source refs, output refs or hashes, requested
  start/end, evidence cutoff, cutoff status, and complete/partial status.
- Denied, blocked, or partial responses include reasons.

### Known-At And Partial Data

- Cited facts are at or before the trace cutoff.
- Completed bars use close-time known-at semantics when close time exists.
- Truncated or partial trades are not used as complete aggression confirmation.
- Missing data families remain explicit.

### Hint Pollution

- Worker did not see Council discussion that told it what to prove.
- Worker did not receive outcome, judge, ledger, performance, or answer-bearing
  artifacts.
- Main R did not substitute worker judgment.

### Falsifier Coverage

- Falsifier searched for counter evidence.
- Falsifier considered no-entry, boring, failure, and alternative explanations.
- Missing falsifier coverage is recorded as a discipline gap.

### Overclaim And Reviewer-As-Judge

- No process output claims performance, edge, can-trade, Product GO, live signal,
  broker action, OMS action, or live-order action.
- Reviewer did not judge market result or replace deterministic judge/ledger.

## Required Output

Return output compatible with
`agent-system/templates/lrf-reviewer-discipline-template.json`.

Minimum fields:

- `review_id`;
- `reviewed_refs`;
- `verdict`;
- `council_boundary_findings`;
- `director_sanitization_findings`;
- `worker_trace_findings`;
- `tool_response_linkage_findings`;
- `known_at_findings`;
- `partial_truncation_findings`;
- `hint_pollution_findings`;
- `falsifier_coverage_findings`;
- `overclaim_findings`;
- `reviewer_as_judge_violations`;
- `required_fixes`;
- `forbidden_next_actions`.

## Forbidden

- Do not judge market result.
- Do not decide stop survival, target hit, win/loss, PnL, win-rate,
  expectancy, performance, edge, can-trade, or Product GO.
- Do not run reveal, deterministic judge, evaluator, or ledger.
- Do not read raw DB, external APIs, app source, release internals, verifier
  internals, dispatcher internals, endpoint internals, broker, OMS, or
  live-order paths.
