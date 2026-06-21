# LRF Ledger Requirements

Status: current_truth
Updated: 2026-06-21

LRF 研究必须记录 ledger。没有 ledger，就不能比较失败、成本、no-entry，也不能做多 case 研究。

## Judgment Trace Ledger

每个判断必须记录：

- `case_id`
- `judgment_id`
- `judgment_type`
- `decision_time`
- `evidence_cutoff`
- `tool_response_refs`
- `source_refs`
- `observed_facts`
- `applied_rule_clauses`
- `reasoning_chain`
- `counter_evidence`
- `alternative_explanations`
- `missing_evidence`
- `confidence_label`
- `invalidation_or_recheck_condition`
- `forbidden_future_attestation`

没有 judgment trace ledger，不能把 Agent 判断纳入后续统计。

## Entry Ledger

每个候选必须记录：

- `case_id`
- `known_at_ts`
- `entry_trigger`
- `entry_trigger_source_refs`
- `supporting_judgment_trace_refs`
- `entry_price_rule`
- `entry_ts`
- `entry_price`
- `entry_status`: `triggered | not_triggered | cancelled | no_entry | blocked`
- `no_entry_reason`
- `cancel_reason`
- `missing_evidence`

## Stop / Invalidation Ledger

每个候选必须记录：

- `invalidation_condition`
- `stop_rule`
- `stop_price`
- `stop_ts`
- `stopped`: `true | false | not_triggered | blocked`
- `invalidated`: `true | false | not_triggered | blocked`
- `invalidated_reason`
- `source_refs`

## Exit / Target Ledger

每个候选必须记录：

- `exit_or_target_rule`
- `exit_ts`
- `exit_price`
- `exit_status`: `exited | target_reached | timeout | cancelled | stopped | blocked`
- `time_stop`
- `exit_reason`
- `source_refs`

## Failure / Cost Ledger

每个候选必须记录失败和成本，即使没有触发：

- `failure_type`: `fake_breakout | stop_out | no_entry | timeout | missed_entry | ambiguous | cost_too_high | not_assessable`
- `mae`
- `mfe`
- `fee_model_ref`
- `slippage_model_ref`
- `estimated_cost`
- `cost_notes`
- `what_would_have_failed`
- `what_data_was_missing`

## Judge Result Ledger

deterministic judge / evaluator 输出：

- `judge_id`
- `judge_input_hash`
- `hypothesis_output_hash`
- `judgment_trace_hashes`
- `reveal_source_ref`
- `triggered`
- `not_triggered`
- `stopped`
- `exited`
- `cancelled`
- `timeout`
- `no_entry`
- `mae`
- `mfe`
- `cost`
- `judge_reason`
- `blocked_reason`

## Ledger 边界

ledger 是研究证据，不是交易许可。

ledger 不允许包含：

- edge；
- can-trade；
- Product GO；
- performance claim；
- broker / exchange / OMS / live-order 指令；
- 未冻结 hypothesis 的后验改写。
