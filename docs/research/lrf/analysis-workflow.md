# LRF 分析工作流

Status: current_truth
Updated: 2026-06-21

本文定义 R 面对 owner 指向 FlowSight app 中某段行情、某个时间点、某个矩形、某个横盘或某次突破时的默认研究顺序。

目标不是让 R 临场解释行情，而是让 worker agent 在可控边界内自主取证、按规则判断、留下 trace，再形成可盲测的 trade hypothesis。

## 0. Client Mirror First

owner 引用 UI 可见事实时，第一步永远是 Client Mirror First。

R 必须先绑定：

- 同一 app instance / endpoint；
- projection / read-model generation；
- symbol、venue、timeframe；
- visible time range / visible price range；
- owner referent：cursor、selected bar、drawing、rectangle、level、highlighted range。

输出：

- `client_mirror_first.mirror_status: seen | partial | not_exposed`
- `APP_CLIENT_PARITY_GAP` / `NOT_RELEASE_APP_BOUND` / `OWNER_REFERENT_AMBIGUOUS` / `R_APP_USAGE_GAP`

如果 CLI/projection 不能暴露 owner referent，不许装作看见。可以在 owner 提供 bounded window 时做 partial exploratory research，但必须标明来源和限制。

## 1. 建立 bounded worker runtime

R 不预选答案，不把厚 candidate packet 塞给 worker。R 负责给 worker 一个边界清楚的运行环境：

- research objective；
- frozen packet/ref/hash；
- authorized time window；
- partial mirror limitation；
- allowed tool registry；
- allowed skill / rubric registry；
- forbidden sources and outputs；
- known-at cursor policy；
- required `judgment_trace` shape。

worker 在这个边界里自主决定查什么、用什么规则判断。

## 2. Exploration mode：先找现象，不写结果

worker 可以在授权窗口内探索结构候选：

- bars slice；
- bar lookup；
- range high / low；
- wick extreme；
- close-back-inside；
- volume facts；
- 以后可扩展 trades / orderbook / OI / FR facts。

探索模式可以寻找候选现象，但不能写 outcome、performance、win/loss、edge 或 can-trade。

## 3. Judgment mode：每个判断必须留 trace

worker 不能只说“这里是 sweep”或“这里是 OB reaction”。每个判断都必须输出 `judgment_trace`。

trace 至少回答：

- 判断类型是什么；
- `decision_time` 和 `evidence_cutoff` 是什么；
- 引用了哪些工具事实和 source refs；
- 满足了哪些规则条款；
- 哪些条款没满足或模糊；
- 推理链是什么；
- 有什么反证和替代解释；
- 缺什么证据；
- 置信度是什么；
- 什么条件会推翻或要求重查；
- 是否明确没有使用 cutoff 之后的数据支持该判断。

没有 trace 的判断不能进入 trade hypothesis。

## 4. 形成完整 trade hypothesis

只有在关键判断有 trace 后，worker 才能提出完整 LRF trade hypothesis：

- `premise`
- `setup_context`
- `entry_trigger`
- `entry_price_rule`
- `invalidation_condition`
- `stop_rule`
- `exit_or_target_rule`
- `cancel_condition`
- `no_entry_condition`
- `time_stop`
- `cost_model_ref`
- `confidence_label`

如果字段不完整，输出 `needs_data` 或 `blocked`，不能硬写完整战法。

## 5. Blind challenge and reviewer

最小盲测结构：

1. hypothesis worker：写 LRF trade hypothesis 和 judgment traces。
2. adversarial worker：使用同一 answer-free 边界和 tool/skill registry 攻击 hypothesis。
3. reviewer：只审盲测纪律、refs、leakage、trace 完整性、overclaim 和 forbidden claims。

这些 worker 都不能看 reveal / outcome / judge / performance。它们的输出是 evidence input，不是 authority。

## 6. Freeze 后才允许 future judge

顺序必须是：

```text
packet freeze
  -> worker judgment traces freeze
  -> hypothesis output freeze
  -> adversarial output freeze
  -> reviewer discipline freeze
  -> deterministic judge / evaluator reveal
  -> post-reveal comparison
  -> failure/cost/no-entry ledger
```

不允许 hypothesis worker 在 reveal 后改写理由。

## 7. 输出纪律

每次输出都必须区分：

- `observed_fact`
- `judgment_trace`
- `hypothesis`
- `counter_evidence`
- `missing_evidence`
- `blocker_classification`
- `failure_cost_notes`
- `next_tool_readback_needed`

最终输出只能是研究诊断，不能是交易许可、edge、can-trade、Product GO 或 performance claim。
