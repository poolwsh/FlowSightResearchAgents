# LRF Worker Agent Runtime

Status: current_truth
Updated: 2026-06-22

本文定义 LRF worker 如何在历史研究中自主取证、判断和输出 trace，同时防止看未来、被暗示、越权取数或把工具事实伪装成 smart-money 结论。

## 核心原则

Worker 不是填表员，也不是全局选题者。正确模型是：

```text
Research Director 给出 bounded task
  -> worker 自主请求允许的 deterministic facts
  -> broker 执行工具并记录 source/hash/cutoff
  -> worker 用 rubric 写 judgment_trace
  -> reviewer 审纪律
  -> freeze 后未来 judge / ledger 才看 outcome
```

R / Director 不得替 worker 预选答案，也不得把 Council 的“希望这里有戏”喂给 blind worker。

## Runtime 输入

每次 worker 任务至少包含：

- `research_objective`
- `hypothesis_ref`，可选；不得包含结论性答案
- `candidate_window`
- `decision_time_policy`
- `evidence_cutoff_policy`
- `source_data_manifest`
- `allowed_tool_registry`
- `allowed_skill_registry`
- `known_at_policy`
- `forbidden_sources`
- `forbidden_outputs`
- `required_output_shape`

允许输入：

- 历史窗口；
- 数据族可用性；
- source refs / hashes；
- worker 可请求的工具列表；
- rubric 名称；
- 需要验证的问题。

禁止输入：

- future path；
- outcome；
- win/loss；
- judge result；
- performance；
- edge / can-trade；
- Council 对该窗口的倾向性结论；
- 其他 worker 的答案。

## Tool registry

Tools 是 deterministic fact providers，不是 smart-money label generator。

当前事实工具类型：

- OHLCV：`bars_slice`、`bar_lookup`、`range_stats`、`wick_close_back_fact`。
- Trades：`slice_summary`、`adaptive_time_buckets`、`price_zone_filter`、`large_prints`，必须保留 truncation / partial / source hash 纪律。
- Funding / OI：可在明确 GOAL 中用 bounded inline deterministic parse，后续应做专门 fact tools。

工具不得输出：

- `this_is_ob`
- `this_is_fvg`
- `this_is_liquidity_sweep`
- `this_is_acceptance`
- `entry_confirmed`
- `edge`
- `can_trade`
- `performance`

工具可以输出低层事实，例如 count、price range、volume、side quantities、completed bar range、wick/close-back facts、OI/funding value changes。最终判断由 worker + rubric 做。

## Brokered tool request

Worker 不直接拿 broad shell、raw DB、external API 或 app internals。Worker 发结构化 `tool_request`，R/broker 审核后执行。

最小 `tool_request`：

```yaml
tool_request:
  request_id:
  worker_id:
  tool_id:
  reason:
  params:
  requested_start:
  requested_end:
  evidence_cutoff:
  expected_observation:
  why_allowed:
```

最小 `tool_response`：

```yaml
tool_response:
  request_id:
  tool_id:
  status: ok | denied | blocked | partial | error
  source_ref:
  output_ref:
  output_hash:
  observation_summary:
  requested_start:
  requested_end:
  evidence_cutoff:
  cutoff_respected:
  complete_or_partial:
  blocked_reason:
```

R 不得把 tool response 改写成隐藏答案再喂给 worker。R 只做边界审核、执行、记录和返回。

## Known-at policy

历史研究允许看历史数据，但每个判断必须模拟当时可知信息。

- 完整 OHLCV bar 只有在 bar close time <= evidence cutoff 时可用。
- Trades slice 只有在 app readback 证明 requested range / as_of / truncation 状态后可用。
- Truncated trades 不得作为完整 aggression confirmation。
- Funding / OI 只能按 source known-at policy 和 evidence cutoff 使用。
- Outcome / future path 只能在 freeze 后给 judge / ledger。

## Judgment trace

每个非平凡判断都必须有 trace。

最小 shape：

```yaml
judgment_trace:
  judgment_id:
  judgment_type:
  decision_time:
  evidence_cutoff:
  tool_response_refs:
  observed_facts:
  applied_rule_clauses:
    satisfied:
    not_satisfied:
    ambiguous:
  reasoning_chain:
  counter_evidence:
  alternative_explanations:
  missing_evidence:
  confidence_label: likely | possible | ambiguous | not_supported | needs_data | blocked
  invalidation_or_recheck_condition:
  forbidden_future_attestation:
```

没有 trace 的判断不能进入 hypothesis、challenge、ledger 或 cross-case 统计。

## Reviewer 边界

Reviewer 审：

- 是否偷看未来；
- refs 是否存在；
- tool response 是否被正确引用；
- trace 是否完整；
- reasoning 是否由 observed facts 支撑；
- partial/truncated 数据是否被误用；
- 是否忽略明显反证；
- 是否 overclaim；
- 是否把 tools 的低层事实伪装成 smart-money 结论；
- blind worker 是否被 Director 或 Council 暗示。

Reviewer 不审：

- 市场结果是否赚钱；
- stop/target 是否真的命中；
- win-rate、PnL、expectancy；
- edge / can-trade / Product GO。

这些只能由 future deterministic judge / evaluator / ledger 处理。
