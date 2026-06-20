# LRF App Referent Analysis Workflow

Status: active_contract
Goal: r-goal001-minimal-lrf-agent-system-batch
Updated: 2026-06-20

## Purpose

This workflow makes R analyze an owner-referenced FlowSight app object, time range,
rectangle, selected bar, cursor point, level, or price/time area through the same
running app state before doing LRF research.

The entry is an owner app referent, not a screenshot. R must first bind the same
FlowSight app state, then follow the LRF causal research sequence.

## Trigger

Use this workflow when owner says things like:

- "看 app 上这段"
- "看 06/15 10:50"
- "看这个横盘"
- "看我画的矩形"
- "看 1710-1730"
- "看这个突破 / 扎针 / 长 range"

## Source Docs

- `docs/index.md`
- `docs/research/index.md`
- `docs/research/lrf/index.md`
- `docs/research/lrf/research-object.md`
- `docs/research/lrf/analysis-workflow.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

## Required Input

```yaml
owner_app_referent:
  owner_words: ""
  target_kind: "time | range | rectangle | cursor | selected_bar | level | area | unknown"
  target_hint:
    time_range: ""
    price_range: ""
    timestamp: ""
    object_id: ""
    symbol_hint: ""
    timeframe_hint: ""
  owner_intent: "analyze_lrf_structure"
```

## Forbidden Entry Paths

R must not start from:

- screenshot-first analysis
- image-first analysis
- raw-data-first analysis
- detached external-market-data-first analysis
- prose-only interpretation of owner words

Screenshots and owner prose may help clarify a referent, but they do not become
app facts until the FlowSight CLI/app endpoint mirror confirms the same app state
or reports a typed blocker.

## Workflow Stages

### Stage 0: Client Mirror First

Run Client Mirror First through the FlowSight CLI/app endpoint before market
interpretation. Until an executable tool exists, this is a workflow requirement,
not an `agent-system/tools/**` markdown tool.

Required result:

```yaml
client_mirror_first:
  mirror_status: "seen | partial | not_exposed"
  app_instance_id: ""
  endpoint_or_context_ref: ""
  projection_generation: ""
  symbol: ""
  venue: ""
  timeframe: ""
  visible_time_range: ""
  visible_price_range: ""
  owner_referent_exposure: "seen | partial | not_exposed"
  classification: "OK | NOT_RELEASE_APP_BOUND | APP_CLIENT_PARITY_GAP | R_APP_USAGE_GAP | OWNER_REFERENT_AMBIGUOUS"
```

If `mirror_status` is `not_exposed`, do not pretend R saw the owner referent.
Stop or continue only with explicitly bounded `partial` analysis.

### Stage 1: Locate LRF Research Object

Classify the mirrored app referent into one or more object types:

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

If the object is `unknown` or `noise`, state what context is missing before LRF
analysis can continue.

### Stage 2: Trace Antecedent / 前因

R must proactively inspect why the object matters:

- prior selloff or displacement
- prior support/resistance role
- lost zone formation
- liquidity sweep or raid
- OB / FVG / breaker context
- earlier acceptance or rejection

Do not wait for owner to remind R to inspect prior selloff, lost zone, range
cause, or state-transition context.

### Stage 3: Define Key Zone

Fieldize the key zone:

```yaml
key_zone:
  price_low: ""
  price_high: ""
  time_window: ""
  source_refs: []
  known_at_refs: []
  prior_structure_refs: []
  boundary_quality: "likely | possible | ambiguous | not_supported | blocked"
```

The key zone is the research battlefield, not an entry signal.

### Stage 4: Decompose Internal Range

Decompose the internal repricing process:

- range high / low / mid
- duration
- upper-bound touches
- lower-bound touches
- wicks / needles
- upper sweeps
- lower sweeps
- close back inside
- compression
- reclaim
- accept/reject after N bars

The target is to understand whether the area shows repricing, absorption,
liquidity clearing, inducement, rejection, or no assessable structure.

### Stage 5: Build Failure / Cost / No-Entry Ledger

Before opportunity discussion, record:

- fake breakout
- stop-out
- no-entry
- timeout
- ambiguous / not assessable event
- MAE / MFE when available
- fee/slippage model reference when available

Only reporting successful-looking opportunities is `R_METHOD_GAP`.

### Stage 6: Compare State-Transition Candidates

Compare failed acceptance candidates against true-acceptance candidates.
Examples such as `06/15 00:10` vs `06/15 10:50/10:54` are workflow patterns,
not accepted market conclusions.

Required comparison dimensions:

- boundary compression before event
- displacement size
- close position relative to range boundary
- return inside range
- pullback hold/fail
- trades delta / volume window
- OI change window
- FR context
- orderbook availability/status
- known-at feature refs

### Stage 7: Build Five-Family Evidence Map

Map every important claim to:

- OHLCV
- trades
- OI
- FR
- orderbook

Missing app primitive: `APP_BLOCKED`.
Missing or poor data coverage: `DATA_BLOCKED`.
Do not fill missing orderbook/trades/OI/FR evidence with prose.

### Stage 8: Produce LLM Causal Judgment

Judgment labels:

- `likely`
- `possible`
- `ambiguous`
- `not_supported`
- `blocked`
- `needs_data`

Judgment must separate observed facts from hypotheses.

### Stage 9: Opportunity Discussion Only After Research

Opportunity language is allowed only after stages 0-8.
Every opportunity must include:

- structure invalidation
- stop location
- cost implication
- failure alternative
- no-trade / no-entry conditions

No opportunity may be written as edge, can-trade, money-grade, Product GO, or a
research packet claim.

## Required Output Schema

```yaml
app_referent:
  mirror_status: ""
  endpoint_or_context_ref: ""
  projection_generation: ""
  symbol: ""
  timeframe: ""
  visible_time_range: ""
  visible_price_range: ""
  referent: {}

lrf_object:
  object_type: ""
  key_zone: {}
  antecedent: {}
  range_context: {}

internal_evolution:
  sweeps: []
  fake_breakouts: []
  accept_reject_events: []

failure_cost:
  stopouts: []
  no_entries: []
  cost_notes: []

evidence_map:
  ohlcv: {}
  trades: {}
  oi: {}
  funding: {}
  orderbook: {}

judgment:
  label: "likely | possible | ambiguous | not_supported | blocked | needs_data"
  observed_fact: []
  hypothesis: []
  reason: ""
  missing_evidence: []

next_action:
  tool_readback_needed: []
  no_trade_conditions: []
```

## Blocker Taxonomy Mapping

- `APP_BLOCKED`: app/CLI/projection/endpoint primitive missing.
- `DATA_BLOCKED`: required market data missing, stale, truncated, or low quality.
- `R_APP_USAGE_GAP`: app exposes the needed state, but R failed to mirror or use it.
- `R_METHOD_GAP`: R skips antecedent, key zone, failure cost, or state-transition comparison.
- `OWNER_POLICY_GAP`: owner has not authorized required next action or scope.

## Dispatcher-Owned Boundary

R and workflow steps never choose:

- `release-root`
- `endpoint-dir`
- `verifier-integrity-sha256`

These values come from dispatcher/app-side authority. This workflow does not
declare FlowSight app verifier, release, endpoint, broker, OMS, live-order, or
account authority.

## Non-Goals

- No FlowSight app source edits.
- No verifier/release/dispatcher edits.
- No endpoint-dir mutation.
- No market run.
- No research packet.
- No reveal or outcome comparison.
- No edge, Product GO, can-trade, money-grade, or trade permission claim.
- No legacy root import/archive/delete.

## Review Checklist

- Did R mirror the owner app referent before interpretation?
- Is the entry owner app referent, not screenshot/image?
- Are antecedent and key zone present before range interpretation?
- Are failure/cost/no-entry present before opportunity discussion?
- Are state-transition candidates compared under known-at discipline?
- Are observed facts separated from hypotheses?
- Are missing data/app surfaces classified with blocker taxonomy?
- Are dispatcher-owned values left to dispatcher/app-side authority?
