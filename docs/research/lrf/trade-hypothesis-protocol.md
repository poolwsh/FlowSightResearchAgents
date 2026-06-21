# LRF Trade-Hypothesis Protocol

Status: current_truth
Updated: 2026-06-21

本文定义 LRF 如何从结构观察升级为完整交易战法研究对象。

研究交易战法不等于发布交易指令。R 可以研究入场、出场、止损、失效、成本和失败样本，但不能把研究输出写成 edge、can-trade、Product GO 或 performance claim。

## 四类必备字段

### `known_at_fields`

worker 只能使用 decision time 前可知的信息：

- `known_at_ts`
- `decision_time`
- `evidence_cutoff`
- `source_refs`
- `app_instance_ref`
- `projection_generation`
- `symbol`
- `timeframe`
- `bounded_window`
- `client_mirror_status`
- `key_zone`
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

### `judgment_trace_fields`

所有 FVG / OB / liquidity / sweep / fake breakout / acceptance / lost-zone reaction 判断都必须引用 trace：

- `judgment_id`
- `judgment_type`
- `decision_time`
- `evidence_cutoff`
- `observed_facts`
- `tool_response_refs`
- `applied_rule_clauses`
- `reasoning_chain`
- `counter_evidence`
- `alternative_explanations`
- `missing_evidence`
- `confidence_label`
- `invalidation_or_recheck_condition`
- `forbidden_future_attestation`

没有 trace 的判断不能作为 hypothesis 支撑。

### `hypothesis_fields`

写 hypothesis 的 blind worker 必须输出：

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
- `supporting_judgment_trace_refs`
- `confidence_label`: `likely | possible | ambiguous | not_supported | blocked | needs_data`

没有这些字段，不允许称为完整 LRF trade hypothesis。

### `evaluation_fields`

这些字段只能在 freeze 后由未来 deterministic judge / evaluator 输出：

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

evaluation fields 用于研究诊断和 failure/cost ledger，不是交易许可。

## 入场、出场、止损的研究含义

入场、出场和止损在 ResearchAgents 里不是实盘指令，而是让战法可检验的研究字段：

- 没有 entry，无法判断样本是否触发；
- 没有 invalidation / stop，无法记录失败和成本；
- 没有 exit / target / cancel，无法判断研究窗口何时结束；
- 没有 no-entry，研究会只挑成功图形；
- 没有 judge，hypothesis 会变成自说自话；
- 没有 judgment trace，LLM 判断无法复盘。

## 允许输出

允许输出：

- 可盲测候选假设；
- 判断 trace；
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
