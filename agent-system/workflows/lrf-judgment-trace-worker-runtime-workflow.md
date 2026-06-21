# LRF Judgment-Trace Worker Runtime Workflow

Status: active_contract
Goal: r-goal-lrf-agent-system-judgment-trace-runtime-rebuild-v0
Updated: 2026-06-21

## Purpose

This is the canonical active LRF workflow for bounded worker research.

It replaces the older fill-form blind hypothesis flow. R does not preselect
hidden structure answers for the worker. The worker receives a bounded runtime,
chooses allowed tools and rubrics, requests deterministic facts, emits
`judgment_trace` records, and only then may form a trade-hypothesis candidate.

This workflow does not run reveal, judge, evaluator, ledger, PnL, win-rate,
expectancy, performance, edge, can-trade, Product GO, broker, OMS, exchange, or
live-order work.

## Source Truth

- `docs/research/lrf/index.md`
- `docs/research/lrf/research-object.md`
- `docs/research/lrf/analysis-workflow.md`
- `docs/research/lrf/worker-agent-runtime.md`
- `docs/research/lrf/trade-hypothesis-protocol.md`
- `docs/research/lrf/blind-validation-protocol.md`
- `docs/research/lrf/ledger-requirements.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

## Canonical Path

```text
stage_0_client_mirror_and_scope
  -> stage_1_runtime_contract_freeze
  -> stage_2_worker_tool_request_loop
  -> stage_3_judgment_trace_generation
  -> stage_4_trade_hypothesis_candidate
  -> stage_5_challenge_and_runtime_review
  -> stage_6_stop_before_reveal_judge_ledger
```

There is no alternate active LRF workflow entry point in this rebuilt slice. If
the task cannot enter this path, report the blocker instead of switching to ad
hoc analysis.

## stage_0_client_mirror_and_scope

Purpose: bind the owner-referenced FlowSight app state before LRF work.

Inputs:

- owner referent;
- release app CLI/app endpoint readback;
- Client Mirror First report;
- known viewport parity limitations.

Outputs / handoff artifacts:

- `client_mirror_first.mirror_status: seen | partial | not_exposed`;
- app instance and endpoint/context reference;
- projection/read-model generation when exposed;
- symbol, venue, timeframe, and authorized time window;
- owner referent binding quality;
- typed blocker classification when needed.

Allowed actor: main R.

Stop/blocker condition:

- `NOT_RELEASE_APP_BOUND` when no release app endpoint is bound.
- `APP_CLIENT_PARITY_GAP` when UI state exists but CLI/projection cannot expose
  enough state.
- `OWNER_REFERENT_AMBIGUOUS` when the referent cannot bind to time, price,
  object, range, or viewport.
- `R_APP_USAGE_GAP` when FlowSight exposes state but R skips the mirror.

Forbidden shortcuts:

- screenshot-first analysis;
- detached raw data first;
- external exchange API substitution;
- claiming full viewport parity when the mirror is partial.

## stage_1_runtime_contract_freeze

Purpose: create and freeze the bounded worker runtime before worker autonomy.

Inputs:

- Stage 0 mirror report;
- frozen answer-free packet/ref/hash when available;
- authorized window;
- allowed tool registry;
- allowed skill/rubric registry;
- known-at cursor policy;
- forbidden sources and outputs.

Outputs / handoff artifacts:

- `runtime_contract.json`;
- `runtime_contract_hash`;
- `allowed_tool_registry`;
- `allowed_skill_registry`;
- `known_at_policy`;
- `required_artifacts`.

Allowed actor: main R.

Stop/blocker condition:

- `BLOCKER` if the runtime cannot exclude reveal/outcome/performance/judge data.
- `BLOCKER` if the worker cannot be restricted to the bounded packet, registry,
  and allowed sources.

Forbidden shortcuts:

- giving worker broad shell or whole-repo access without proven isolation;
- giving worker answer-bearing runs or future labels;
- embedding R-selected hidden structure answers into the runtime contract.

## stage_2_worker_tool_request_loop

Purpose: let the worker choose facts to inspect while R brokers boundary-safe
tool access.

Inputs:

- frozen runtime contract;
- worker objective;
- allowed tool registry;
- `lrf-worker-tool-request-template.json`;
- `lrf-worker-tool-response-template.json`.

Outputs / handoff artifacts:

- `tool_requests.jsonl`;
- `tool_responses.jsonl`;
- response ids, output refs, and output hashes;
- denied/blocked requests with reasons.

Allowed actor:

- worker chooses requests;
- main R validates boundaries and runs or denies deterministic tools.

Stop/blocker condition:

- `TOOL_REQUEST_DENIED` when a request violates registry or known-at policy.
- `TOOL_BLOCKED` when an allowed deterministic fact cannot be produced.
- `BLOCKER` when no brokered tool route or isolated runtime exists.

Forbidden shortcuts:

- main R choosing facts and feeding conclusions as if they came from the worker;
- tools returning final smart-money labels such as OB/FVG/sweep/acceptance;
- worker using raw DB, external API, app internals, reveal, judge, or outcome
  artifacts.

## stage_3_judgment_trace_generation

Purpose: convert deterministic observed facts into auditable LLM judgments.

Inputs:

- frozen runtime contract;
- tool responses;
- allowed rubric registry;
- `lrf-structure-judgment-rubric.md`;
- `lrf-judgment-trace-template.json`.

Outputs / handoff artifacts:

- `judgment_traces.jsonl`;
- evidence-linked reasoning steps;
- satisfied, not satisfied, and ambiguous rule clauses;
- counter-evidence and alternative explanations;
- missing evidence and confidence labels.

Allowed actor: worker using allowed rubrics.

Stop/blocker condition:

- `needs_data` if required facts are absent but obtainable.
- `blocked` if required facts are unavailable under the allowed registry.
- `not_supported` if the rubric cannot support the judgment.

Forbidden shortcuts:

- prose-only labels without source refs and tool response refs;
- using post-cutoff bars to support a known-at judgment;
- treating low-level tool facts as final smart-money conclusions.

## stage_4_trade_hypothesis_candidate

Purpose: allow a trade-hypothesis candidate only after key judgments have traces.

Inputs:

- judgment traces;
- known-at policy;
- trade-hypothesis field requirements from docs.

Outputs / handoff artifacts:

- `trade_hypothesis_candidate.json`;
- entry trigger;
- entry price rule;
- invalidation condition;
- stop rule;
- exit/target rule;
- cancel condition;
- no-entry condition;
- time stop;
- cost model reference or missing-cost blocker.

Allowed actor: worker.

Stop/blocker condition:

- `needs_data` if required entry/exit/stop/cost fields lack evidence.
- `R_METHOD_GAP` if a structure observation is presented as a complete strategy.
- `blocked` if known-at discipline cannot be proven.

Forbidden shortcuts:

- calling a structure observation a strategy;
- omitting entry, invalidation, stop, exit, cancel, no-entry, or cost handling;
- claiming the candidate made or lost money.

## stage_5_challenge_and_runtime_review

Purpose: attack judgments and audit runtime discipline before any reveal.

Inputs:

- frozen runtime contract;
- tool requests/responses;
- judgment traces;
- trade-hypothesis candidate;
- `review-lrf-runtime-discipline.md`.

Outputs / handoff artifacts:

- `challenge_notes.json`;
- `runtime_discipline_review.json`;
- leakage findings;
- unsupported refs;
- missing evidence;
- overclaim findings;
- reviewer verdict: `pass | needs_fix | blocked`.

Allowed actor:

- adversarial worker may challenge using the same bounded runtime;
- reviewer audits discipline only.

Stop/blocker condition:

- `needs_fix` when trace, refs, or field completeness are insufficient.
- `blocked` when leakage or forbidden-source use is detected.

Forbidden shortcuts:

- reviewer judging market outcome;
- reviewer replacing deterministic judge/evaluator;
- challenge worker using reveal/outcome/performance artifacts.

## stage_6_stop_before_reveal_judge_ledger

Purpose: freeze the rebuilt runtime outputs and stop.

Inputs:

- runtime contract;
- tool requests/responses;
- judgment traces;
- trade-hypothesis candidate;
- challenge/review artifacts.

Outputs / handoff artifacts:

- freeze hashes;
- final blocker classification;
- next recommended GOAL.

Allowed actor: main R orchestration.

Stop/blocker condition:

- always stop here unless a later owner-authorized GOAL explicitly implements
  reveal, deterministic judge/evaluator, ledger, or post-reveal comparison.

Forbidden shortcuts:

- reveal;
- judge/evaluator;
- failure/cost ledger;
- post-reveal comparison;
- PnL, win-rate, expectancy, performance, edge, can-trade, Product GO, or trade
  recommendation claims.

