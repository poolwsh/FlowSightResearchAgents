# LRF Trade-Hypothesis Protocol

Status: current_truth
Updated: 2026-06-20

本文定义 LRF 如何从结构观察升级为完整交易战法研究对象。

核心原则：研究交易战法不等于发交易指令。R 可以研究入场、出场、止损、失效、成本和失败样本，但不能把研究输出写成 edge、can-trade、Product GO 或 performance claim。

## 必须三类字段

### `hypothesis_fields`

写 hypothesis 的 blind subagent 必须输出：

- `premise`：为什么这个区域值得研究；
- `setup_context`：liquidity / OB / FVG / lost-zone / breaker / displacement 背景；
- `entry_trigger`：什么 known-at 条件触发候选；
- `entry_price_rule`：如何记录入场价格；
- `invalidation_condition`：什么条件证明假设错；
- `stop_rule`：如何记录止损 / 失败成本；
- `exit_or_target_rule`：什么条件结束研究窗口；
- `cancel_condition`：触发前什么情况取消；
- `no_entry_condition`：什么情况明确不进入；
- `time_stop`：超过多少 bars / 时间仍未触发或未确认；
- `cost_model_ref`：费用、滑点、MAE/MFE 记录模型；
- `confidence_label`: `likely | possible | ambiguous | not_supported | blocked | needs_data`。

没有这些字段，不允许称为完整 LRF trade hypothesis。

### `known_at_fields`

盲包必须只包含 entry 决策前可知信息：

- `known_at_ts`
- `source_refs`
- `app_instance_ref`
- `projection_generation`
- `symbol`
- `timeframe`
- `bounded_window`
- `key_zone`
- `range`
- `sweep_or_fake_breakout_candidates`
- `available_data_families`
- `missing_data_families`
- `forbidden_future_fields_scan`

禁止字段：

- future path；
- outcome；
- reveal；
- judge result；
- success / failure label；
- post-reveal comparison；
- performance / edge / can-trade。

### `evaluation_fields`

裁判 / evaluator 在 freeze 后才能输出：

- `triggered`
- `not_triggered`
- `entry_ts`
- `entry_price`
- `stopped`
- `stop_ts`
- `stop_price`
- `exited`
- `exit_ts`
- `exit_price`
- `cancelled`
- `timeout`
- `no_entry`
- `mae`
- `mfe`
- `cost`
- `judge_reason`
- `source_refs`

这些字段用于研究诊断和 failure/cost ledger，不是交易许可。

## 入场、出场、止损的研究含义

入场、出场和止损在 ResearchAgents 里不是实盘指令，而是让战法可检验的研究字段：

- 没有 entry，无法判断样本是否触发；
- 没有 invalidation / stop，无法记录失败和成本；
- 没有 exit / target / cancel，无法判断研究窗口何时结束；
- 没有 no-entry，研究会只挑成功图形；
- 没有 judge，hypothesis 会变成自说自话。

## 允许输出

允许输出：

- 候选假设；
- 证据缺口；
- blocker；
- failure/cost 诊断；
- 多 case 后的研究价值判断；
- 是否值得继续研究。

不允许输出：

- “这套能赚钱”；
- “这里可以交易”；
- edge；
- can-trade；
- Product GO；
- live-ready；
- broker / exchange / OMS / live-order 结论。
