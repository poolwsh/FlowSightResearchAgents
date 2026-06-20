# LRF 研究对象

Status: current_truth
Updated: 2026-06-20

## 当前研究对象

LRF 当前研究对象是一条基于 smart-money / ICT / order-flow 的前因后果链：

```text
前置暴跌 / displacement
  -> 关键区域被打穿，形成失守区或流动性记忆区
  -> 价格回到该区域附近并形成盘整
  -> 盘整内部反复 sweep / 扎针 / fake breakout / accept-reject
  -> 某次突破可能是真接受，也可能是假突破
  -> 研究能否用 known-at 数据提前区分这两类情况
```

这不是结论，而是当前被接受的研究 framing。

## 更一般的 LRF 单元

每一个 liquidity、OB、FVG、失守区或 breaker 附近，都可能出现一个局部 LRF 单元：

```text
关键价格记忆 / liquidity object
  -> 价格回到附近
  -> 局部盘整
  -> 上下沿扎针 / sweep
  -> 假接受 / 假突破
  -> 真接受、拒绝、继续盘整或失效
```

因此，LRF 的本质不是“某个 OB/FVG 是否有效”，而是研究关键对象附近的流动性再分配过程。
OB/FVG/liquidity 给出战场，盘整和扎针暴露战场内部的供需变化。

## 为什么不是简单突破

单独说“突破 range high”太粗。当前研究要看突破之前的区域内部演化：

- 是否先有关键 liquidity / OB / FVG / 失守区。
- 回到该区域后是否出现持续盘整。
- 盘整中是否反复扫上下沿流动性。
- 扎针后是回收、接受，还是延续失败。
- 主动成交、OI、FR、orderbook 是否支持吸收、诱导、清算或重新接受。

如果这些前因缺失，最后突破只能是一个价格事件，不能被写成 LRF 因果链。

## 可证伪字段

### 关键区 / 失守区

需要后续 tool readback 或 ledger 固化的字段：

- `breakdown_window_start`
- `breakdown_window_end`
- `breakdown_high`
- `breakdown_low`
- `lost_zone_price_low`
- `lost_zone_price_high`
- `prior_support_or_liquidity_refs`
- `breakdown_displacement_bars`
- `known_at_ts`
- `source_refs`

判断问题：

- 该区是否真的有结构角色，而不是事后框出来的噪声区？
- 该区是否被有效打穿？
- 后续价格回到该区时是否有多次反应？

### 盘整

需要字段：

- `range_start_ts`
- `range_end_ts`
- `range_high`
- `range_low`
- `range_mid`
- `range_duration_bars`
- `range_overlap_with_lost_zone`
- `upper_boundary_touches`
- `lower_boundary_touches`
- `source_refs`

判断问题：

- 盘整是否围绕关键区发生？
- 盘整是否足够长，能构成重新定价过程？
- 上下沿是否稳定，还是事后选择出来的边界？

### sweep / fake breakout ledger

每一次 sweep / fake breakout 至少记录：

- `event_ts`
- `side`: `upper` / `lower`
- `sweep_price`
- `boundary_price`
- `close_back_inside`
- `acceptance_after_n_bars`
- `rejection_after_n_bars`
- `would_trigger_entry`
- `would_stop_out`
- `stop_price`
- `max_adverse_excursion`
- `max_favorable_excursion`
- `fee_slippage_cost_model_ref`
- `source_refs`

研究必须记录失败、成本和无入场样本，不能只记录成功突破。

### 成功候选 vs 失败候选

当前 ETH 探索 case 中，`06/15 00:10` 与 `06/15 10:50/10:54`
只作为候选比较点。它们不是已验证结论。

它们之所以重要，是因为探索S的失败说明：R 不能只把这类点当作“突破 K 线”。
R 必须比较状态切换前后的 known-at 条件：

- 失败突破是否下一根或短窗口内回到 range 内。
- 真接受候选是否在突破后不回到原矩形内。
- 突破前是否有贴近上沿压缩、反复扫流动性、失败卖压或仓位挤压。
- trades / OI / FR / orderbook 是否支持“重新接受”而不是事后看涨。

后续比较至少需要：

- `breakout_ts`
- `breakout_bar_open/high/low/close`
- `breakout_displacement_size`
- `close_position_vs_range_high`
- `next_n_bars_acceptance`
- `pullback_low_after_breakout`
- `returned_inside_range`
- `trades_delta_window`
- `trade_volume_window`
- `oi_change_window`
- `funding_context`
- `orderbook_status`
- `known_at_feature_refs`

## 五类数据用途

- OHLCV：定义结构、失守区、盘整、sweep、reclaim、displacement、accept/reject。
- Trades：验证主动成交、delta、buyer failure / seller failure。
- Open Interest：判断新仓、平仓、挤压、去杠杆或仓位堆积。
- Funding Rate：提供拥挤和方向背景，不单独作为信号。
- Orderbook：验证被动防守、吸收、撤单、补单；不可用时必须标 blocker。

## 当前边界

当前文档接受的是研究对象和字段方向，不接受任何 edge、can-trade、Product GO 或 playbook mutation。

