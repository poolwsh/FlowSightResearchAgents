# LRF 研究对象

Status: current_truth
Updated: 2026-06-20

## 一句话定义

LRF 研究的是关键 liquidity / OB / FVG / lost-zone / breaker 附近，市场如何通过横盘、扎针、sweep、fake breakout、accept / reject 完成局部重新定价，以及这种过程能否被建模成可盲测的交易假设。

它不是单纯问“某个 OB/FVG 有没有效”，也不是看见突破后解释行情。LRF 的核心是前因后果：

```text
前置 displacement / sweep / lost-zone / OB / FVG / breaker
  -> 价格回到关键记忆区
  -> 局部横盘和上下沿反复试探
  -> sweep / wick / fake breakout / reclaim / reject
  -> 形成一个可定义的入场候选或 no-entry
  -> 后续由独立 judge 判断触发、失效、出场和成本
```

## 结构观察与战法研究的分界

只描述这些现象还不是完整战法研究：

- 有一个横盘；
- 上下沿有扎针；
- 价格靠近 OB/FVG；
- 突破后走了一段；
- 某个位置看起来像假突破。

完整 LRF 战法研究至少还必须定义：

- `entry_trigger`：什么 known-at 条件触发候选；
- `invalidation_condition`：什么条件证明假设错了；
- `stop_rule`：研究上如何记录失败成本；
- `exit_or_target_rule`：什么条件结束研究窗口；
- `cancel_condition`：什么条件说明不再进入；
- `no_entry_condition`：什么情况必须明确标 no-entry；
- `failure_cost_model`：stop-out、timeout、missed-entry、slippage、fee、MAE/MFE 如何记录；
- `judge_rule`：谁或什么工具在 reveal 后判定结果。

没有这些字段，输出只能叫结构观察，不能叫完整战法研究。

## LRF 局部单元

每个 liquidity、OB、FVG、lost-zone 或 breaker 附近都可能出现一个局部 LRF 单元：

```text
关键价格记忆 / liquidity object
  -> 回到附近
  -> 局部盘整
  -> 上下沿 sweep / wick
  -> fake acceptance / fake breakout
  -> 真接受、拒绝、继续盘整、失效或 no-entry
```

OB/FVG/liquidity 给出战场；横盘、扎针和失败样本暴露战场内部供需变化；entry/exit/stop/no-entry 把观察变成可检验研究对象。

## 必须字段

### 前因字段

- `premise_type`
- `premise_time_window`
- `source_liquidity_object`
- `lost_zone_price_low`
- `lost_zone_price_high`
- `prior_support_or_resistance_refs`
- `displacement_or_breakdown_refs`
- `known_at_ts`
- `source_refs`

### 横盘字段

- `range_start_ts`
- `range_end_ts`
- `range_high`
- `range_low`
- `range_mid`
- `range_duration_bars`
- `upper_boundary_touches`
- `lower_boundary_touches`
- `range_overlap_with_key_zone`
- `known_at_source_refs`

### sweep / fake breakout 字段

- `event_ts`
- `side`: `upper` / `lower`
- `boundary_price`
- `sweep_price`
- `close_back_inside`
- `acceptance_after_n_bars`
- `rejection_after_n_bars`
- `returned_inside_range`
- `source_refs`

### 交易假设字段

- `entry_trigger`
- `entry_price_rule`
- `invalidation_condition`
- `stop_rule`
- `exit_or_target_rule`
- `cancel_condition`
- `no_entry_condition`
- `time_stop`
- `cost_model_ref`
- `hypothesis_confidence`: `likely | possible | ambiguous | not_supported | blocked | needs_data`

## 五类证据

每个关键判断都要映射到五类数据；不可用时必须显式 blocked。

- OHLCV：结构、range、sweep、displacement、accept/reject 候选。
- Trades：主动成交、taker 方向、突破/回收时的 aggression。
- Orderbook：被动防守、吸收、撤单、补单、流动性空洞。
- Open Interest：新仓、平仓、挤压、去杠杆、仓位堆积。
- Funding Rate：拥挤、方向偏置、carry regime。

OHLCV 可以提出候选，但不能单独证明 smart-money 因果机制。

## 当前边界

本目录接受的是研究对象和协议字段，不接受任何 edge、can-trade、Product GO、money-grade、performance 或单次 case 结论。
