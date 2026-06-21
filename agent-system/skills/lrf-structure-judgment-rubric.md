---
name: lrf-structure-judgment-rubric
description: Use when an LRF worker must judge structure, liquidity, sweep, fake breakout, acceptance, lost-zone reaction, displacement, or no-entry context from deterministic facts and produce an auditable judgment_trace.
---

# LRF Structure Judgment Rubric

## Purpose

This is a bounded LLM judgment rubric. It helps a worker decide whether
deterministic facts support an LRF/ICT structure judgment.

It is not a persona, not a data reader, not a tool, and not a market-result
judge. The worker must cite tool response refs and produce a `judgment_trace`.

## Accepted Inputs

- frozen runtime contract;
- research objective;
- authorized window;
- known-at policy;
- allowed tool response refs;
- observed facts from deterministic tools;
- source refs and hashes;
- missing evidence list.

## Allowed Judgment Types

- `range_context`
- `fvg_candidate`
- `ob_candidate`
- `liquidity_sweep`
- `fake_breakout`
- `acceptance`
- `rejection`
- `lost_zone_reaction`
- `displacement`
- `no_entry_reason`
- `ambiguous_structure`

These are judgment labels, not tool labels. A tool may return facts such as bar
high/low, wick extreme, close-back-inside, or range stats. The worker applies
this rubric to decide whether those facts support a label.

## Required Evidence

Every judgment must include:

- at least one `tool_response_ref`;
- source refs for the observed facts;
- `decision_time`;
- `evidence_cutoff`;
- observed facts at or before the cutoff;
- rule clauses marked `satisfied`, `not_satisfied`, or `ambiguous`;
- evidence-linked reasoning steps;
- counter-evidence;
- alternative explanations;
- missing evidence;
- confidence label;
- invalidation or recheck condition.

## Rule Clauses

Use these clauses as a checklist. Do not force a label when the facts do not
support it.

### Context Clauses

- The judgment is inside the authorized window.
- The cited facts are at or before `evidence_cutoff`.
- The relevant symbol, venue, timeframe, and data-family status are named.
- Partial mirror or missing data-family limits are carried into the judgment.

### Structure Clauses

- A candidate range, level, zone, or displacement has source refs.
- The alleged key area has a reason to matter, such as prior liquidity, lost
  zone, range boundary, displacement origin, or imbalance candidate.
- The internal evolution is described with facts, not just a final label.
- A no-entry explanation is allowed when facts are mixed or incomplete.

### Liquidity / Sweep Clauses

- The swept level or liquidity reference is named.
- The probe beyond the level is backed by bar facts.
- The close, reclaim, or failure-to-accept behavior is backed by facts.
- Opposite explanations are considered, including normal volatility or an
  unresolved range test.

### FVG / OB Clauses

- The candidate is tied to displacement or an imbalance/reaction area.
- The worker states which facts support the candidate and which facts are
  missing.
- The worker does not treat a visual gap or prior candle body as sufficient by
  itself.
- The worker distinguishes low-level proxy facts from final smart-money
  judgment.

### Fake Breakout / Acceptance Clauses

- The breakout side, level, and decision time are explicit.
- The worker cites facts for acceptance, rejection, or close-back-inside.
- The worker names what would invalidate the judgment.
- The worker does not use later outcome bars to prove the known-at call.

## Confidence Labels

Use only:

- `likely`
- `possible`
- `ambiguous`
- `not_supported`
- `needs_data`
- `blocked`

Do not use confident language when counter-evidence or missing evidence is
material.

## Output Requirement

The worker must output a `judgment_trace` compatible with
`agent-system/templates/lrf-judgment-trace-template.json`.

Minimum trace fields:

- `judgment_id`
- `judgment_type`
- `decision_time`
- `evidence_cutoff`
- `observed_facts`
- `applied_rule_clauses`
- `reasoning_chain`
- `counter_evidence`
- `alternative_explanations`
- `missing_evidence`
- `confidence_label`
- `invalidation_or_recheck_condition`
- `forbidden_future_attestation`

`reasoning_chain` must be a concise evidence-linked chain. It must not rely on
private intuition or unsupported narrative.

## Forbidden

- Do not read raw DB.
- Do not call external APIs.
- Do not inspect FlowSight app source, verifier, release, dispatcher, or endpoint
  internals.
- Do not run tools directly unless the runtime explicitly grants isolated tool
  access.
- Do not output PnL, win-rate, expectancy, performance, edge, can-trade, Product
  GO, or trade recommendations.
- Do not judge whether a stop survived, a target hit, or a hypothesis made
  money.
- Do not use reveal, outcome, judge, ledger, or post-reveal comparison artifacts.

