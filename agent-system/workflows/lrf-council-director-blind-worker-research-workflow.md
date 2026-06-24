# LRF Council / Director / Blind Worker Research Workflow

Status: active_execution_material
Source authority: accepted 7-file ResearchAgents docs current truth

This is the canonical active LRF workflow. It implements the current docs; it
does not create a new market theory during execution.

## Source Authority

Use only these docs as method authority:

- `docs/index.md`
- `docs/research/lrf/index.md`
- `docs/research/lrf/research-thesis.md`
- `docs/research/lrf/price-cvd-orderbook-strategy.md`
- `docs/research/lrf/research-process.md`
- `docs/research/lrf/method-stack.md`
- `docs/research/lrf/blocker-taxonomy.md`

Authority order:

```text
research thesis
  -> research framework / docs current truth
  -> skills / rubrics / workflows
  -> tools / deterministic facts
  -> runs / evidence artifacts
```

Lower layers may implement, verify, block, refute, or propose docs changes.
They must not rewrite the thesis or framework inside a run.

## Canonical Flow

```text
source_binding
  -> council_mechanism_hypotheses
  -> director_neutral_task_slicing
  -> blind_worker_fact_loop
  -> judgment_trace
  -> falsifier_negative_pass
  -> reviewer_discipline_audit
  -> freeze
```

The first-version framework is:

```text
Price Action + CVD/Delta + Orderbook
```

Execution order inside every worker judgment:

```text
price_action_context
  -> aggressive_flow_state
  -> passive_liquidity_state
  -> smart_money_hypothesis_status
```

Smart-money language names hypotheses; it is not proof.

## Stage 0: Source Binding

Record the app-owned source binding before any role work:

- app selector, endpoint binding method, CLI path, release metadata if supplied;
- symbol, venue, timeframe, historical window;
- bars source and hash;
- trades / CVD / delta source and hash;
- orderbook evidence status: `complete | partial | blocked | insufficient`;
- known-at / as-of policy;
- canonical response identity and hash conventions.

If binding or required source readback is unavailable, stop with a typed blocker.
Do not use raw DB, external API, screenshot guessing, app internals, or unreviewed
release discovery as substitutes.

## Stage 1: Council

Council may inspect a broad historical universe. Council starts from the market
mechanism thesis, not from indicator names.

Council outputs:

- mechanism question;
- candidate windows;
- boring / no-entry windows;
- failure or alternative-explanation windows;
- required evidence families;
- falsification questions.

Council must not output outcome, live signal, performance, edge, can-trade,
Product GO, broker action, OMS action, or live-order action.

## Stage 2: Director

Director converts Council output into neutral bounded tasks.

Director responsibilities:

- choose task windows and decision-time policy;
- assign neutral `blind_task_id` values;
- remove Council conclusion language and any future/outcome hints;
- set allowed tool and skill registries;
- define known-at and partial-evidence rules;
- ensure workers are not given global free-browse tasks or single-bar traps.

The worker-visible task asks what the evidence supports, contradicts, leaves
partial, or blocks. It must not reveal whether the task is candidate, boring,
or failure-risk.

## Stage 3: Blind Worker Fact Loop

Worker sees only its sanitized task, runtime contract, allowed tools, and facts.

Worker must request deterministic facts through the R tool broker. Every cited
fact must resolve to a `tool_responses.jsonl` entry with:

- `response_id`;
- `identity.response_id_source`;
- `request_id`;
- `output_ref`;
- `output_hash`;
- `source_hashes.raw_source_hash`;
- `source_hashes.normalized_source_hash`;
- requested bounds;
- `evidence_cutoff`;
- `cutoff_respected`;
- completeness status.

Tools provide facts only. They must not output FVG confirmed, absorption
confirmed, distribution confirmed, edge, can-trade, Product GO, or performance.

## Stage 4: Judgment Trace

Each non-trivial worker judgment records:

- `blind_task_id`;
- `price_action_context`;
- `aggressive_flow_state`;
- `passive_liquidity_state`;
- `smart_money_hypothesis_status`;
- supporting facts by canonical `response_id`;
- contradicting facts;
- partial or blocked evidence;
- alternative explanations;
- confidence label;
- forbidden claims attestation.

If deterministic facts are missing, partial, truncated, stale, or blocked, the
trace must downgrade. Missing orderbook cannot be turned into passive-liquidity
proof. Truncated trades cannot be turned into complete CVD/delta confirmation.

## Stage 5: Falsifier

Falsifier attacks the hypothesis after worker traces freeze.

Falsifier checks:

- no-entry, boring, and failure samples;
- simpler alternative explanations;
- CVD/delta caveats and truncation;
- orderbook partial, blocked, low-density, or unstable evidence;
- smart-money language that explains every chart;
- hindsight or task-label leakage.

Falsifier does not judge market result and does not compute performance.

## Stage 6: Reviewer

Reviewer audits discipline only:

- docs authority chain followed;
- Council did not start from indicator name stacking;
- Director isolation and neutral task ids;
- worker-visible artifacts did not leak sealed roles;
- known-at and cutoff discipline;
- canonical `response_id` linkage;
- raw and normalized source hashes;
- partial/truncated/orderbook downgrade;
- forbidden claims;
- reviewer did not become a market-result judge.

Reviewer pass means process discipline passed. It is not a market result.

## Stage 7: Freeze

Freeze means the process artifacts are sealed for later review:

- Council output;
- Director task packet;
- runtime contract;
- tool requests and responses;
- worker outputs and judgment traces;
- falsifier output;
- reviewer discipline output;
- validation report.

Current active workflow stops at freeze. Any later outcome comparison,
statistics, judge, ledger, performance, edge, can-trade, or Product GO stage
requires separate owner/C authorization and current-truth docs.

## Allowed End States

- `process_smoke_pass`
- `process_smoke_partial`
- `typed_blocker`
- `needs_repair`
- `docs_change_proposal`

Do not use vague labels like "agent cannot research" when a typed blocker can
name the actual gap.

## Forbidden

- raw DB or external API;
- FlowSight app source, release, verifier, dispatcher, or endpoint internals;
- app launch/readback unless explicitly authorized by the current GOAL;
- order recommendations;
- broker, OMS, exchange, or live-order work;
- performance, edge, can-trade, Product GO, or live signal claims.
