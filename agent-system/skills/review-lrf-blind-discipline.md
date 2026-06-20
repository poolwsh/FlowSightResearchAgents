---
name: review-lrf-blind-discipline
description: Use when a bounded Reviewer subagent must audit LRF blind packet and A/B outputs for leakage, refs, completeness, and overclaim.
---

# Review LRF Blind Discipline

Status: active_contract
Goal: r-goal-lrf-phase2-active-workflow-skills-v0
Updated: 2026-06-20

## Purpose

This bounded Reviewer task audits whether the answer-free packet, blind
hypothesis output, and blind challenge output followed LRF evidence discipline.
It does not judge market outcome and must not replace deterministic
judge/evaluator.

## Trigger

Use only from `lrf-blind-trade-hypothesis-research-workflow.md` after:

- the answer-free packet is frozen;
- the blind hypothesis output is frozen;
- the blind challenge output is frozen;
- no reveal/evaluator/judge output has been introduced.

## Reviewer May See

- frozen answer-free packet;
- frozen hypothesis output;
- frozen challenge output;
- packet/output refs and hashes;
- workflow boundary requirements.

## Reviewer Must Not See

- reveal;
- outcome;
- judge result;
- post-reveal comparison;
- future path;
- performance;
- raw DB;
- external API;
- FlowSight app source, verifier, release, dispatcher, endpoint implementation,
  broker, OMS, exchange, live-order, or account data.

## Reviewer Must Not Do

- judge market result;
- decide whether the hypothesis worked;
- replace deterministic judge/evaluator;
- rewrite A/B outputs;
- create missing entry/stop/exit/no-entry fields on behalf of A/B.

## Required Output

```yaml
review_lrf_blind_discipline:
  packet_ref_check:
    status: "pass | partial | fail | blocked"
    notes: []
  hypothesis_field_completeness:
    status: "pass | partial | fail | blocked"
    missing_fields: []
  challenge_field_completeness:
    status: "pass | partial | fail | blocked"
    missing_fields: []
  answer_leakage_check:
    status: "pass | fail | blocked"
    evidence: []
  unsupported_ref_check:
    status: "pass | partial | fail | blocked"
    refs: []
  overclaim_check:
    status: "pass | partial | fail | blocked"
    overclaims: []
  forbidden_claim_check:
    status: "pass | fail | blocked"
    hits: []
  reviewer_verdict: "DISCIPLINE_CLEAR | DISCIPLINE_PARTIAL | BLOCKER_REQUIRED"
  missing_evidence: []
  blocker_classification: "APP_BLOCKED | DATA_BLOCKED | R_APP_USAGE_GAP | R_METHOD_GAP | OWNER_POLICY_GAP | none"
```

## Discipline Rules

- If reveal, outcome, or judge result appears in blind inputs, return
  `BLOCKER_REQUIRED`.
- If A/B references fields not present in the packet, flag unsupported refs.
- If hypothesis lacks entry, stop, exit, cancel, or no-entry, flag incomplete
  trade-hypothesis fields.
- If challenge judges market outcome, flag role-boundary failure.
- If Reviewer is asked to decide trigger/stop/exit/no-entry/cost, return
  `BLOCKER_REQUIRED`; that is deterministic judge/evaluator work.

## Common Mistakes

- Treating Reviewer as the third market-opinion agent.
- Letting Reviewer choose a winner between hypothesis and challenge.
- Allowing post-reveal language into a blind discipline review.
- Passing outputs that omit mandatory trade-hypothesis fields.
