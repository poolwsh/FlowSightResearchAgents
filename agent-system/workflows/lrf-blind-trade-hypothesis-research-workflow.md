# LRF Blind Trade-Hypothesis Research Workflow

Status: active_contract
Goal: r-goal-lrf-phase2-active-workflow-skills-v0
Updated: 2026-06-20

## Purpose

This is the single canonical workflow for LRF blind trade-hypothesis research.
It turns an owner-referenced FlowSight app area into an answer-free known-at
packet, dispatches bounded Codex native subagents, freezes their outputs, and
stops before any deterministic judge/evaluator work that has not been separately
authorized and implemented.

This workflow studies trading hypotheses. It does not issue trade commands,
create a research packet, implement tools, or make edge, can-trade, Product GO,
performance, broker, OMS, exchange, or live-order claims.

## Source Docs

- `docs/research/lrf/index.md`
- `docs/research/lrf/research-object.md`
- `docs/research/lrf/trade-hypothesis-protocol.md`
- `docs/research/lrf/blind-validation-protocol.md`
- `docs/research/lrf/ledger-requirements.md`
- `docs/research/lrf/analysis-workflow.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

## Canonical Path

```text
stage_0_client_mirror_and_scope
  -> stage_1_answer_free_packet_preflight
  -> stage_2_blind_subagent_hypothesis_and_challenge
  -> stage_3_reviewer_discipline_freeze
  -> stage_4_judge_evaluator_reveal_placeholder
  -> stage_5_post_reveal_ledger_and_comparison_placeholder
  -> stage_6_cross_case_research_summary_placeholder
```

There is no alternate active LRF workflow entry point in Phase 2. If a task
cannot enter this path, report the blocker instead of switching to an ad hoc
analysis route.

## stage_0_client_mirror_and_scope

Purpose: bind the owner-referenced UI/app object to the same running FlowSight
app state before LRF interpretation.

Inputs:

- owner words / referent hint;
- FlowSight release app CLI/app endpoint readback;
- Client Mirror First result.

Outputs / handoff artifacts:

- `client_mirror_first.mirror_status: seen | partial | not_exposed`;
- app instance / endpoint or context ref;
- projection/read-model generation;
- symbol, venue, timeframe;
- visible time range and visible price range when exposed;
- owner referent binding quality;
- blocker classification when needed.

Allowed actor: main R.

Stop/blocker condition:

- `NOT_RELEASE_APP_BOUND` if no running release app endpoint is bound.
- `APP_CLIENT_PARITY_GAP` if UI state exists but CLI/projection cannot mirror it.
- `OWNER_REFERENT_AMBIGUOUS` if owner referent cannot bind to time, price, object,
  range, or viewport.
- `R_APP_USAGE_GAP` if app exposes state but R skips or misuses it.

Forbidden shortcuts:

- screenshot-first analysis;
- detached raw data first;
- external API first;
- pretending to see an owner referent that CLI/projection did not expose.

Required boundary attestations:

- no raw DB read;
- no FlowSight app source edit/read requirement;
- no market conclusion before mirror.

## stage_1_answer_free_packet_preflight

Purpose: assemble or verify the answer-free known-at packet needed before
subagent dispatch.

Inputs:

- stage 0 mirror result;
- app endpoint/export evidence authorized for the bounded research window;
- LRF docs-required fields for premise, key zone, range, entry, invalidation,
  stop, exit, cancel, no-entry, data-family status, and missing evidence.

Outputs / handoff artifacts:

- answer-free packet ref;
- packet hash or stable source ref when available;
- known-at timestamp discipline;
- required field coverage report;
- forbidden future/reveal/outcome field scan;
- missing data-family status;
- packet freeze readiness.

Allowed actor: main R, using only authorized endpoint/export evidence.

Stop/blocker condition:

- `DATA_BLOCKED` if required data is missing for the bounded packet.
- `APP_BLOCKED` if app/CLI/projection cannot expose a required primitive.
- `R_METHOD_GAP` if entry/exit/stop/invalidation/no-entry fields are absent but
  R tries to proceed as if this were a complete trade hypothesis.

Forbidden shortcuts:

- including reveal, future path, outcome, judge result, post-reveal labels, or
  performance fields;
- filling missing trades/OI/FR/orderbook evidence with prose;
- dispatching subagents before packet freeze.

Required boundary attestations:

- answer-free packet only;
- known-at source refs recorded;
- missing evidence remains visible.

## stage_2_blind_subagent_hypothesis_and_challenge

Purpose: dispatch bounded Codex native subagent tasks using the same frozen
answer-free packet.

Inputs:

- frozen answer-free packet from stage 1;
- task contract for `write-lrf-blind-trade-hypothesis`;
- task contract for `challenge-lrf-trade-hypothesis`.

Outputs / handoff artifacts:

- frozen hypothesis output;
- frozen adversarial challenge output;
- task ids / source packet refs / output hashes when available.

Allowed actor:

- main R orchestrates;
- Codex native subagent writes blind hypothesis;
- Codex native subagent writes blind challenge.

Stop/blocker condition:

- `BLOCKER` if Codex native subagent dispatch is unavailable or cannot be
  isolated to the frozen packet.
- `R_METHOD_GAP` if main R writes the hypothesis or challenge as a substitute for
  missing subagent execution.

Forbidden shortcuts:

- giving either subagent reveal/outcome/judge result;
- letting the challenge subagent see future data;
- letting main R rewrite subagent outputs after freeze;
- treating either subagent as independent authority.

Required boundary attestations:

- same frozen packet used by both subagents;
- no external/raw/reveal reads;
- outputs are evidence inputs, not market verdicts.

## stage_3_reviewer_discipline_freeze

Purpose: audit the frozen blind packet and frozen A/B outputs for discipline
before any reveal or judge step.

Inputs:

- frozen answer-free packet;
- frozen hypothesis output;
- frozen adversarial challenge output;
- task contract for `review-lrf-blind-discipline`.

Outputs / handoff artifacts:

- reviewer discipline audit output;
- reviewer verdict: `DISCIPLINE_CLEAR | DISCIPLINE_PARTIAL | BLOCKER_REQUIRED`;
- A/B/Reviewer freeze marker or stable refs.

Allowed actor:

- Reviewer subagent audits discipline only;
- main R records freeze and blockers.

Stop/blocker condition:

- `BLOCKER_REQUIRED` if answer leakage, unsupported refs, missing required fields,
  or forbidden claims are found.
- `R_METHOD_GAP` if Reviewer is asked to judge market outcome.

Forbidden shortcuts:

- Reviewer seeing reveal/outcome/judge result;
- Reviewer deciding whether the trade hypothesis worked;
- Reviewer replacing deterministic judge/evaluator;
- continuing to reveal before A/B/Reviewer freeze.

Required boundary attestations:

- reviewer did not judge market result;
- leakage and overclaim checks completed;
- A/B/Reviewer outputs frozen before any reveal.

## stage_4_judge_evaluator_reveal_placeholder

Purpose: mark the future deterministic judge/evaluator boundary.

Inputs:

- frozen packet;
- frozen A/B/Reviewer outputs;
- separately authorized deterministic judge/evaluator/tool/schema;
- separately authorized reveal/evaluation source.

Outputs / handoff artifacts:

- future judge result with triggered/not_triggered/stopped/exited/cancelled/
  timeout/no_entry/MAE/MFE/cost/judge_reason.

Allowed actor: future deterministic judge/evaluator/tool only.

Stop/blocker condition:

- Return `BLOCKER` in Phase 2 because deterministic judge/evaluator, schemas, and
  tools are not implemented or authorized by this workflow.
- R must not manually judge trigger, stop, exit, no-entry, or cost as a
  substitute.

Forbidden shortcuts:

- manual outcome judging by R;
- using Reviewer as judge;
- reading reveal before A/B/Reviewer freeze;
- treating this placeholder as tool availability.

Required boundary attestations:

- judge/evaluator is future separate authorization;
- no reveal in Phase 2 workflow-only execution.

## stage_5_post_reveal_ledger_and_comparison_placeholder

Purpose: mark the future post-reveal comparison and ledger boundary.

Inputs:

- future judge/evaluator result;
- frozen hypothesis/challenge/reviewer outputs;
- future ledger schemas/tools.

Outputs / handoff artifacts:

- future post-reveal comparison;
- future entry/stop/exit/failure/cost/no-entry ledgers.

Allowed actor: future R orchestration plus deterministic tools after separate
authorization.

Stop/blocker condition:

- Return `BLOCKER` in Phase 2 if asked to compare reveal, compute ledgers, or
  assess outcomes without authorized judge/evaluator/tools.

Forbidden shortcuts:

- post-hoc rewriting of the hypothesis;
- hand-made ledger that bypasses deterministic judge/evaluator;
- edge, can-trade, Product GO, performance, or tradeability conclusions.

Required boundary attestations:

- comparison is future separate authorization;
- no post-reveal ledger in Phase 2 workflow-only execution.

## stage_6_cross_case_research_summary_placeholder

Purpose: mark the future cross-case research boundary.

Inputs:

- multiple completed judged cases;
- stable ledger outputs;
- separately authorized cross-case protocol.

Outputs / handoff artifacts:

- future cross-case research summary;
- future keep/rewrite/drop hypothesis recommendation.

Allowed actor: future main R orchestration after separate authorization.

Stop/blocker condition:

- Return `BLOCKER` if fewer than the required completed judged cases exist, if
  ledgers are missing, or if owner has not authorized cross-case research.

Forbidden shortcuts:

- extrapolating from one case;
- turning diagnostic counts into edge or permission;
- hiding failed/no-entry cases.

Required boundary attestations:

- cross-case summary is future separate authorization;
- no performance or product claim.

## Main R Synthesis Responsibility

In Phase 2, synthesis remains with main R. Main R may:

- preserve A/B/Reviewer conflicts;
- classify blockers;
- decide whether the workflow must stop;
- recommend the next owner-authorized GOAL.

Main R must not:

- invent missing subagent outputs;
- judge market outcome;
- replace deterministic judge/evaluator;
- rewrite frozen outputs with hindsight.

## Validation Checklist

- One canonical workflow path was used.
- Client Mirror First happened before LRF analysis.
- Answer-free packet preflight happened before subagent dispatch.
- Packet was frozen before A/B outputs.
- A/B/Reviewer outputs were frozen before any reveal boundary.
- Stage 4-6 remained placeholders unless separately authorized.
- Missing judge/evaluator/tools caused `BLOCKER`, not manual judging.
- No tools/templates/schemas/subflows were created by this workflow.
- No edge, can-trade, Product GO, performance, broker, OMS, exchange, or
  live-order claim was made.
