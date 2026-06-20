# App Referent LRF Reader Skill Contract

Status: active_contract
Goal: r-goal001-minimal-lrf-agent-system-batch
Updated: 2026-06-20

## Purpose

`app-referent-lrf-reader` is the first LLM judgment skill after Client Mirror
First. It classifies the mirrored owner app referent into an LRF research object
and decides whether enough context exists to enter the LRF workflow.

This skill does not read raw data. It depends on the client mirror report and
optional deterministic tool outputs.

## Trigger

Use after Client Mirror First reports `seen` or bounded `partial` for an owner
app referent related to price structure, range, liquidity, OB, FVG, lost zone,
breaker, sweep, fake breakout, or accept/reject behavior.

Do not use this skill when mirror status is `not_exposed`, unless the task is to
explain why LRF analysis is blocked or owner referent is ambiguous.

## Source Docs

- `docs/research/lrf/index.md`
- `docs/research/lrf/research-object.md`
- `docs/research/lrf/analysis-workflow.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

## Required Inputs

```yaml
owner_app_referent:
  owner_words: ""
  referent_type: ""
  time_hint: ""
  price_hint: ""
  object_hint: ""

client_mirror_report:
  mirror_status: "seen | partial | not_exposed"
  endpoint_or_context_ref: ""
  projection_generation: ""
  symbol: ""
  venue: ""
  timeframe: ""
  visible_time_range: ""
  visible_price_range: ""
  referent: {}
  classification: ""

optional_tool_readback_outputs:
  key_zone_candidates: []
  range_candidates: []
  sweep_candidates: []
  evidence_availability: {}
```

## Decision Task

The skill must:

1. Classify the app referent into LRF object type:
   - `liquidity`
   - `OB`
   - `FVG`
   - `lost_zone`
   - `breaker`
   - `range`
   - `sweep`
   - `fake_breakout`
   - `accept_reject`
   - `unknown`
   - `noise`
2. Decide whether enough context exists to enter the LRF workflow.
3. Identify antecedent questions R must answer next.
4. Identify missing evidence and blocker classification.
5. Separate observed app facts from hypotheses.

## Output Schema

```yaml
app_referent_lrf_reader:
  object_type: "liquidity | OB | FVG | lost_zone | breaker | range | sweep | fake_breakout | accept_reject | unknown | noise"
  referent_binding_quality: "seen | partial | not_exposed"
  antecedent_required:
    required: true
    questions: []
  key_zone_candidate:
    present: false
    price_low: ""
    price_high: ""
    time_window: ""
    confidence: "likely | possible | ambiguous | not_supported | blocked | needs_data"
  internal_range_candidate:
    present: false
    range_high: ""
    range_low: ""
    time_window: ""
    confidence: "likely | possible | ambiguous | not_supported | blocked | needs_data"
  state_transition_candidate:
    present: false
    candidate_time: ""
    comparison_needed: []
  missing_evidence: []
  blocker_classification: "APP_BLOCKED | DATA_BLOCKED | R_APP_USAGE_GAP | R_METHOD_GAP | OWNER_POLICY_GAP | none"
  allowed_next_stage: ""
  forbidden_next_actions: []
  judgment:
    label: "likely | possible | ambiguous | not_supported | blocked | needs_data"
    observed_fact: []
    hypothesis: []
    reason: ""
```

## Hard Boundaries

- Do not read raw data directly.
- Do not choose dispatcher-owned values.
- Do not produce edge, Product GO, can-trade, trade permission, money-grade, or
  research packet claims.
- Do not turn a screenshot or owner prose into app fact without a mirror report.
- Do not skip antecedent tracing when the referent appears to be a range,
  breakout, sweep, or state-transition point.
- Do not call something `likely` if the client mirror report is `not_exposed`.

## Examples

### Owner says "看 06/15 10:50"

If mirror report binds the same symbol/timeframe and selected time:

```yaml
object_type: accept_reject
referent_binding_quality: seen
antecedent_required:
  required: true
  questions:
    - "What key zone or range boundary existed before 06/15 10:50?"
    - "Was there a failed acceptance candidate to compare against?"
state_transition_candidate:
  present: true
  candidate_time: "06/15 10:50"
  comparison_needed:
    - "failed acceptance candidate"
    - "next_n_bars_acceptance"
    - "returned_inside_range"
allowed_next_stage: "trace_antecedent"
forbidden_next_actions:
  - "declare true acceptance from hindsight"
  - "discuss opportunity before failure/cost ledger"
judgment:
  label: possible
  observed_fact:
    - "owner referent is a mirrored app timestamp"
  hypothesis:
    - "timestamp may be a state-transition candidate"
```

### Owner says "看这个横盘"

If mirror report has visible range but no exact rectangle:

```yaml
object_type: range
referent_binding_quality: partial
antecedent_required:
  required: true
  questions:
    - "What prior displacement or lost zone produced this range?"
internal_range_candidate:
  present: true
  confidence: possible
missing_evidence:
  - "exact rectangle boundary if owner intended a drawn object"
allowed_next_stage: "define_key_zone"
```

### Owner says "看我画的矩形"

If CLI exposes the drawing:

```yaml
object_type: range
referent_binding_quality: seen
key_zone_candidate:
  present: true
  confidence: possible
allowed_next_stage: "trace_antecedent"
```

### mirror_status not_exposed

If owner references a UI object but CLI/projection cannot read it:

```yaml
object_type: unknown
referent_binding_quality: not_exposed
blocker_classification: APP_BLOCKED
allowed_next_stage: "stop_or_request_missing_referent"
forbidden_next_actions:
  - "pretend R saw the rectangle"
  - "start screenshot-first market interpretation"
judgment:
  label: blocked
  observed_fact:
    - "mirror report did not expose owner referent"
  hypothesis: []
```

## Common Mistakes

- Treating owner prose as app fact without mirror proof.
- Treating a timestamp as an entry signal before finding antecedent and key zone.
- Labeling a range without asking why price arrived there.
- Skipping fake breakout and failure/cost accounting.
- Using `likely` when the correct label is `possible`, `ambiguous`, or `needs_data`.
