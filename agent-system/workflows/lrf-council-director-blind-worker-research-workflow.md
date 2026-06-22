# LRF Council / Director / Blind Worker Research Workflow

Status: active_contract
Goal: r-goal-lrf-agent-system-replacement-cleanup-v0
Updated: 2026-06-22

## Purpose

This is the canonical active LRF workflow for historical research.

The workflow replaces the obsolete worker-centered runtime trunk. Research now
starts with large-scope historical hypothesis generation, then Director task
slicing, then bounded blind worker validation. The workflow stops before future
reveal, deterministic judge, ledger, performance, edge, can-trade, Product GO,
broker, OMS, exchange, or live-order work.

## Source Truth

- `docs/research/lrf/research-agent-organization.md`
- `docs/research/lrf/analysis-workflow.md`
- `docs/research/lrf/worker-agent-runtime.md`
- `docs/research/lrf/blind-validation-protocol.md`
- `docs/research/lrf/trade-hypothesis-protocol.md`
- `docs/research/lrf/ledger-requirements.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

## Canonical Path

```text
stage_0_source_binding
  -> stage_1_council_hypothesis
  -> stage_2_director_task_slicing
  -> stage_3_blind_worker_fact_loop
  -> stage_4_judgment_trace
  -> stage_5_falsifier_negative_pass
  -> stage_6_reviewer_research_discipline
  -> stage_7_freeze_stop_before_judge_ledger
```

If a task cannot enter this path, report a typed blocker. Do not fall back to
ad hoc chart commentary or obsolete source-packaging flows.

## stage_0_source_binding

Purpose: bind app-owned historical source evidence before any research agent
uses it.

Inputs:

- owner or dispatcher supplied source scope;
- release app CLI/app endpoint readback when current app data is used;
- source data manifest;
- symbol, venue, timeframe, and bounded historical range;
- known limitations for missing data families.

Outputs:

- `source_binding_ref`;
- app selector and endpoint binding ref when applicable;
- source hashes;
- available and missing data families;
- known-at policy;
- typed blocker when binding is unavailable.

Rules:

- R does not choose dispatcher-owned formal `release-root`, `endpoint-dir`, or
  `verifier-integrity-sha256`.
- R must not use raw DB, external API, app source, release internals,
  dispatcher internals, or endpoint internals as substitutes.
- Missing binding stops the workflow.

## stage_1_council_hypothesis

Purpose: let two or three Council agents inspect a larger historical scope and
propose research hypotheses.

Inputs:

- source binding ref;
- historical scope;
- data family availability;
- allowed Council skill;
- forbidden outputs.

Outputs:

- `lrf-council-hypothesis-template.json` compatible output;
- research hypotheses;
- candidate windows;
- verification questions;
- required data families;
- no-entry, boring, and failure sample needs.

Rules:

- Council output is research planning, not worker truth.
- Council must not output outcome, reveal, performance, edge, can-trade,
  Product GO, live signal, broker action, OMS action, or live-order action.
- Council discussion is not passed directly to blind workers.

## stage_2_director_task_slicing

Purpose: convert Council output into bounded answer-free worker tasks.

Inputs:

- Council output;
- source binding ref;
- allowed tool registry;
- allowed skill registry;
- known-at policy.

Outputs:

- `lrf-director-task-packet-template.json` compatible task packet;
- candidate window;
- worker objective;
- decision time and evidence cutoff policy;
- forbidden sources and outputs;
- information isolation attestation.

Rules:

- Director prevents global free-browse worker behavior.
- Director prevents single-bar-only tasks without enough context.
- Default worker scope is a bounded candidate window with permission to drill
  down through brokered tool requests.
- Director removes Council conclusion language and future outcome hints before
  worker dispatch.
- Director does not write the market judgment.

## stage_3_blind_worker_fact_loop

Purpose: let the blind worker request deterministic facts inside the assigned
window.

Inputs:

- research runtime contract;
- Director task packet;
- allowed tool registry;
- allowed skill registry;
- tool request and response templates.

Outputs:

- `tool_requests.jsonl`;
- `tool_responses.jsonl`;
- output refs and hashes;
- denied, partial, or blocked responses with reasons.

Rules:

- Worker requests facts; R brokers and records them.
- Tools return deterministic facts, source refs, hashes, cutoff, requested
  start/end, and complete/partial status.
- Worker may drill down inside the assigned window.
- Tools must not output final smart-money labels.
- Worker must not use raw DB, external API, app internals, reveal, judge, ledger,
  performance, edge, can-trade, Product GO, broker, OMS, or live-order material.

## stage_4_judgment_trace

Purpose: convert deterministic facts into auditable LLM judgments.

Inputs:

- Director task packet;
- tool responses;
- allowed rubric registry;
- judgment trace template.

Outputs:

- `judgment_traces.jsonl`;
- evidence-linked reasoning;
- satisfied, not satisfied, and ambiguous rule clauses;
- counter evidence;
- alternative explanations;
- missing evidence;
- confidence labels.

Rules:

- No prose-only labels.
- Every non-trivial judgment cites tool response refs and source refs.
- Every judgment states `decision_time` and `evidence_cutoff`.
- Post-cutoff facts cannot support known-at judgments.

## stage_5_falsifier_negative_pass

Purpose: attack the hypothesis before any reveal.

Inputs:

- Director task packet;
- worker judgment traces;
- allowed facts and rubrics under the same known-at policy.

Outputs:

- `lrf-falsifier-output-template.json` compatible output;
- counter evidence;
- no-entry findings;
- boring sample findings;
- failure sample findings;
- alternative explanations;
- missing evidence.

Rules:

- Falsifier uses bounded known-at evidence.
- Falsifier does not judge market result.
- Falsifier does not use reveal, judge, ledger, performance, edge, can-trade, or
  Product GO material.

## stage_6_reviewer_research_discipline

Purpose: audit the full Council / Director / Worker / Falsifier chain.

Inputs:

- source binding ref;
- Council output;
- Director task packet;
- tool requests and responses;
- judgment traces;
- falsifier output.

Outputs:

- `lrf-reviewer-discipline-template.json` compatible output;
- discipline verdict;
- required fixes;
- forbidden next actions.

Rules:

- Reviewer checks Council boundary, Director sanitization, worker refs,
  known-at, partial/truncated data use, hint pollution, falsifier coverage,
  overclaim, and reviewer-as-judge violations.
- Reviewer does not judge market result and does not replace deterministic judge
  or ledger.

## stage_7_freeze_stop_before_judge_ledger

Purpose: freeze research process evidence and stop before outcome evaluation.

Inputs:

- all prior stage outputs.

Outputs:

- freeze refs and hashes;
- final blocker classification or next GOAL recommendation.

Rules:

- Always stop here unless a later owner-authorized GOAL explicitly starts
  reveal, deterministic judge, evaluator, ledger, or post-reveal comparison.
- No performance, edge, can-trade, Product GO, broker, OMS, exchange, live-order,
  or trade recommendation claim is allowed.
