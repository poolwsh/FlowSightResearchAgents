---
name: review-lrf-runtime-discipline
description: Use when R or a reviewer worker must audit LRF runtime outputs for known-at discipline, source refs, tool response refs, judgment_trace completeness, leakage, and overclaim without judging market results.
---

# Review LRF Runtime Discipline

## Purpose

Audit whether an LRF worker runtime followed the accepted method stack.

This review checks process discipline. It does not decide whether a market call
was profitable, whether a stop survived, whether a target hit, or whether a
strategy has edge.

## Accepted Inputs

- runtime contract;
- frozen packet/ref/hash;
- allowed tool registry;
- allowed skill/rubric registry;
- tool requests;
- tool responses;
- judgment traces;
- trade-hypothesis candidate, if present;
- challenge output, if present.

## Review Checks

### Runtime Boundary

- The worker stayed inside the authorized window.
- The worker used only allowed tools and rubrics.
- Any partial Client Mirror limitation is still present.
- Missing data families remain labelled and are not inferred away.

### Known-At Discipline

- Each judgment has `decision_time` and `evidence_cutoff`.
- Supporting facts are at or before cutoff.
- Post-cutoff data is not used to support entry, stop, exit, no-entry, or
  confidence.
- Reveal, outcome, judge, ledger, performance, or answer-bearing artifacts are
  absent.

### Tool Request / Response Discipline

- Each observed fact has a `tool_response_ref`.
- Each `tool_response_ref` resolves to a stable response id, output ref, or hash.
- Denied or blocked requests include a reason.
- Tools return deterministic facts, not final smart-money labels.

### Judgment Trace Completeness

- `judgment_id`, `judgment_type`, `decision_time`, and `evidence_cutoff` exist.
- `observed_facts` cite source refs and tool response refs.
- `applied_rule_clauses` include satisfied, not satisfied, and ambiguous clauses.
- `reasoning_chain` is supported by observed facts.
- `counter_evidence` and `alternative_explanations` are present.
- `missing_evidence` is explicit.
- `confidence_label` is one of the allowed labels.
- `forbidden_future_attestation` is present.

### Trade-Hypothesis Completeness

If a trade-hypothesis candidate exists, it must include:

- premise;
- setup context;
- entry trigger;
- entry price rule;
- invalidation condition;
- stop rule;
- exit or target rule;
- cancel condition;
- no-entry condition;
- time stop;
- cost model reference or missing-cost blocker.

If these fields are absent, classify the result as `R_METHOD_GAP`, `needs_data`,
or `blocked`; do not patch the hypothesis by prose.

### Overclaim

Flag:

- structure observation presented as complete strategy;
- low-level proxy fact presented as OB/FVG/liquidity final truth;
- unsupported confidence;
- missing failure/no-entry/cost treatment;
- Product GO, edge, can-trade, performance, or trade recommendation language.

## Output

Return a structured review:

```yaml
runtime_discipline_review:
  review_id:
  reviewed_runtime_ref:
  verdict: pass | needs_fix | blocked
  leakage_findings: []
  unsupported_refs: []
  missing_tool_response_refs: []
  incomplete_judgment_traces: []
  overclaim_findings: []
  reviewer_as_judge_violations: []
  blocker_classification:
  required_fixes: []
  forbidden_next_actions: []
```

## Forbidden

- Do not judge market result.
- Do not replace deterministic judge/evaluator.
- Do not decide stop survival, target hit, win/loss, PnL, win-rate, expectancy,
  performance, edge, can-trade, or Product GO.
- Do not read raw DB, external API, screenshots, FlowSight app source, verifier,
  release, dispatcher, endpoint internals, or answer-bearing runs.

