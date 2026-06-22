# LRF Trade-Hypothesis Protocol

Status: current_truth
Updated: 2026-06-22

本文定义 LRF 如何从结构观察升级为完整的历史交易假设。交易假设是研究对象，不是交易指令。

## 四类字段

### `known_at_fields`

Worker 只能使用 decision time 前可知的信息：

- `known_at_ts`
- `decision_time`
- `evidence_cutoff`
- `source_refs`
- `app_instance_ref`
- `projection_generation`
- `symbol`
- `venue`
- `timeframe`
- `bounded_window`
- `client_mirror_status`
- `candidate_window_ref`
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

所有 FVG / OB / liquidity / sweep / fake breakout / acceptance / lost-zone / displacement / no-entry 判断都必须引用 trace：

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

没有 trace 的判断不能支撑 hypothesis。

### `hypothesis_fields`

Blind worker 或 structure worker 输出完整 hypothesis 时必须包含：

- `hypothesis_id`
- `candidate_window_ref`
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
- `counter_evidence_refs`
- `missing_evidence`
- `confidence_label`: `likely | possible | ambiguous | not_supported | blocked | needs_data`

字段不完整时，输出 `needs_data` 或 `blocked`，不能硬写完整战法。

### `evaluation_fields`

这些字段只能在 freeze 后由 deterministic judge / evaluator 输出：

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

Evaluation fields 用于研究诊断和 ledger，不是交易许可。

## 入场、出场、止损的研究含义

Entry、exit、stop 在 ResearchAgents 里不是实盘指令，而是让历史假设可检验的字段：

- 没有 entry，无法判断样本是否触发；
- 没有 invalidation / stop，无法记录失败和成本；
- 没有 exit / target / cancel，无法判断研究窗口何时结束；
- 没有 no-entry，研究会只挑成功图；
- 没有 judge，hypothesis 会变成自说自话；
- 没有 judgment trace，LLM 判断无法复盘。

## Council hypothesis 与 worker hypothesis

Council 可以提出粗 hypothesis，例如“某类 sweep + reclaim + trades failure 可能值得研究”。这不是可评估交易假设。

Worker hypothesis 必须来自 bounded task 和 tool facts，并具备上述字段。Director 负责把 Council hypothesis 转成 answer-free worker task，不能把 Council 的结论性倾向喂给 worker。

## 允许输出

允许：

- 可盲测候选假设；
- judgment trace；
- evidence gap；
- blocker；
- no-entry / failure / cost 诊断；
- 是否值得继续研究。

不允许：

- “这套能赚钱”；
- “这里可以交易”；
- edge；
- can-trade；
- Product GO；
- live-ready；
- broker / exchange / OMS / live-order 结论。
