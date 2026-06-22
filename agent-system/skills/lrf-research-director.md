---
name: lrf-research-director
description: Use when Council research hypotheses must be converted into bounded answer-free blind worker tasks with explicit candidate windows, known-at policy, tool/skill registry, and information isolation.
---

# LRF Research Director

## Purpose

Convert Council hypotheses into bounded blind worker tasks.

The Director is the research dispatcher. It chooses candidate windows, task
granularity, allowed tools, allowed rubrics, and information isolation. It does
not make the market judgment.

## Non-Goals

Do not use this skill to:

- produce smart-money conclusions;
- prove the Council hypothesis;
- decide market outcome;
- run reveal, judge, evaluator, or ledger;
- compute performance, edge, can-trade, Product GO, PnL, win-rate, or
  expectancy;
- read raw DB, external APIs, app source, release internals, verifier internals,
  dispatcher internals, endpoint internals, broker, OMS, or live-order paths.

## Accepted Inputs

- Council output ref;
- source binding ref;
- hypothesis ref;
- candidate windows;
- data family availability;
- allowed tool registry;
- allowed skill registry;
- known-at policy;
- source limitations;
- forbidden sources and outputs.

## Task Granularity Rules

### No Global Free Browse

Do not give blind workers a broad historical universe and ask them to "find
something." Council and Director own the global view.

### No Single-Bar Trap

Do not give workers only one bar unless the task includes enough surrounding
context to judge structure. A single bar can be a lookup target, not the default
research universe.

### Default Window

Default to a bounded candidate window, such as a short multi-bar range, a
session fragment, or a Council-selected event window. The worker may drill down
inside this window through brokered tool requests.

## Sanitization Rules

Before worker dispatch, remove:

- Council conclusion language;
- future outcome;
- win/loss;
- judge result;
- performance;
- "this is the good one" language;
- other worker answers;
- any hint that the worker should confirm rather than test.

Keep:

- objective;
- bounded window;
- verification question;
- data family availability;
- allowed tools and rubrics;
- known-at policy;
- missing evidence to check.

## Required Output

Return output compatible with
`agent-system/templates/lrf-director-task-packet-template.json`.

Minimum fields:

- `director_task_id`;
- `council_ref`;
- `hypothesis_ref`;
- `candidate_window`;
- `worker_objective`;
- `decision_time_policy`;
- `evidence_cutoff_policy`;
- `allowed_tool_registry`;
- `allowed_skill_registry`;
- `forbidden_sources`;
- `forbidden_outputs`;
- `information_isolation_attestation`.

## Next-Action Routing

After worker/reviewer output, route to one of:

- `continue_research`;
- `seek_counterexamples`;
- `tool_goal`;
- `app_goal`;
- `rubric_goal`;
- `director_goal`;
- `stop_or_archive`.

Do not route to reveal, judge, ledger, performance, edge, can-trade, or Product
GO without a separate owner-authorized GOAL.
