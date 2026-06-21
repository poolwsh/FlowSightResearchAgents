# LRF Worker Agent Runtime

Status: current_truth
Updated: 2026-06-21

本文定义 LRF worker agent 如何自主研究，同时防止拍脑袋、偷看未来和越权取数。

## 核心原则

worker 不是填表员，R 也不替 worker 预选答案。正确模型是：

```text
R 提供目标和边界
  -> worker 自己选择工具和判断规则
  -> tools 返回 deterministic facts
  -> worker 用 rubric 做判断
  -> judgment_trace 留下证据链
  -> reviewer 审纪律
  -> future judge / ledger 才看 reveal
```

worker 可以自主探索，但必须在 bounded runtime 内运行。

## Runtime 输入

每次 worker 任务至少包含：

- `research_objective`
- `frozen_packet_path`
- `frozen_packet_hash`
- `authorized_window`
- `client_mirror_status`
- `client_mirror_limitation`
- `allowed_tool_registry`
- `allowed_skill_registry`
- `known_at_cursor_policy`
- `forbidden_sources`
- `forbidden_outputs`
- `required_output_shape`

R 不能把后验答案、成功标签、judge result、performance 或未来走势塞进 worker 输入。

## Tool registry

tools 是 deterministic fact provider，不是 smart-money 结论生成器。

最小工具类型：

- `bars_slice`：读取 cutoff 内的 OHLCV bars。
- `bar_lookup`：读取某个 timestamp 附近、cutoff 内的 bars。
- `range_stats`：计算某个 interval 的 high、low、open、close、volume。
- `wick_close_back_fact`：计算 wick extreme 和 close-back-inside 事实。

以后可以扩展：

- trades aggression facts；
- orderbook absorption / pull / replenish facts；
- OI expansion / compression facts；
- funding regime facts。

tools 不允许输出：

- `this_is_ob`
- `this_is_fvg`
- `this_is_liquidity_sweep`
- `this_is_smart_money_acceptance`
- `edge`
- `can_trade`
- `performance`

除非某个工具明确被设计为低层 proxy，也必须写清楚 proxy 限制，不能把 proxy 当最终判断。

## Skill / rubric registry

skills 是 LLM 判断规则，不是 persona，不是 data reader。

当前 LRF 最小 rubric：

- `lrf-structure-judgment-rubric`
- `liquidity-sweep-judgment-rubric`
- `fake-breakout-vs-acceptance-rubric`
- `lost-zone-reaction-rubric`
- `displacement-quality-rubric`
- `trade-hypothesis-fielding-rubric`

每个 rubric 至少定义：

- 判断对象；
- 必要支持证据；
- 反证；
- 最少 source refs；
- known-at cutoff 要求；
- confidence labels；
- missing evidence 处理；
- forbidden claims。

## Brokered tool request

worker 默认不直接拿 broad shell 或全仓库访问。worker 发结构化 `tool_request`，R 审核后执行或拒绝。

最小 `tool_request`：

```yaml
tool_request:
  request_id:
  worker_id:
  tool_id:
  reason:
  params:
  evidence_cutoff:
  expected_observation:
  why_allowed:
```

最小 `tool_response`：

```yaml
tool_response:
  request_id:
  tool_id:
  status: ok | denied | blocked | error
  source_ref:
  output_ref:
  output_hash:
  observation_summary:
  cutoff_respected:
  blocked_reason:
```

R 不能把 tool response 改写成隐藏答案再喂给 worker。R 只做边界审核、执行、记录和返回。

## Judgment trace

每个判断都必须有 trace。trace 是后续 challenge、reviewer、judge 之前唯一能审查 LLM 判断是否按规则走的证据。

最小 shape：

```yaml
judgment_trace:
  judgment_id:
  judgment_type: fvg | ob | liquidity_sweep | fake_breakout | acceptance | lost_zone_reaction | displacement | no_entry_reason
  decision_time:
  evidence_cutoff:
  observed_facts:
    - fact_id:
      source_ref:
      tool_response_ref:
      value:
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

## Known-at policy

answer-free 不是“不给数据”，而是“不给答案”。worker 可以在授权窗口里探索历史数据，但写判断和 hypothesis 时必须声明 cutoff。

两种模式：

1. `exploration_mode`：worker 可在授权窗口内查找候选现象，但不能声明 outcome、performance、win/loss 或 edge。
2. `judgment_mode`：worker 必须设置 `decision_time` 和 `evidence_cutoff`，并且支持 entry、stop、exit、no-entry 的理由只能引用 cutoff 之前的事实。

cutoff 之后的数据只能留给未来 judge / reveal / ledger，不能用于证明 worker 当时的判断正确。

## Reviewer 边界

reviewer 审：

- 是否偷看未来；
- refs 是否存在；
- tool response 是否被正确引用；
- judgment trace 是否完整；
- reasoning_chain 是否真的由 observed_facts 支撑；
- 是否忽略明显反证；
- 是否 overclaim；
- 是否把 tools 的低层事实伪装成 smart-money 结论。

reviewer 不审：

- 市场结果是否赚钱；
- stop 是否真的没被打；
- target 是否真的到达；
- win-rate、PnL、expectancy；
- edge / can-trade / Product GO。

这些只能由未来 deterministic judge / evaluator / ledger 处理。
