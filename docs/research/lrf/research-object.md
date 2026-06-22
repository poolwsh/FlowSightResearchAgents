# LRF 研究对象

Status: current_truth
Updated: 2026-06-22

## 一句话定义

LRF 研究的是：在历史数据中，关键 liquidity / OB / FVG / lost-zone / breaker 附近，市场如何通过局部盘整、扫流动性、假突破、reclaim、displacement、acceptance/rejection 完成重新定价，以及这种过程能否形成可盲测、可反驳、可记账、可跨样本统计的交易假设。

LRF 不等于“看见一个 OB/FVG 就解释行情”。LRF 的核心是因果脚本：

```text
关键区域或前置结构
  -> 价格回到附近
  -> 局部供需重新评估
  -> sweep / reclaim / fake breakout / acceptance / rejection
  -> 形成 candidate / no-entry / failure
  -> freeze 后由 judge / ledger 评价结果和成本
```

## 历史研究对象，不是实时信号

每个 LRF 对象都是历史研究样本：

- 可以事后被选入研究 universe；
- 具体判断必须按 decision time / evidence cutoff 模拟当时可知事实；
- outcome 只能在 freeze 后用于 judge / ledger；
- 不输出 live entry、can-trade、Product GO 或 edge。

## 关键判断概念

以下概念主要是判断性概念，不能过早写成工具最终标签：

- FVG 是否在当前语境里仍有意义；
- OB 是否构成反应区，而不是事后画框；
- liquidity sweep 是否被接受、拒绝或只是噪声；
- fake breakout 与 true acceptance 的差异；
- lost-zone reaction 是否说明供需状态切换；
- displacement quality 是否足以改变局部结构；
- no-entry 是否比强行入场更符合规则。

工具只给事实；worker 用 rubric 判断。

## 五类证据

每个关键研究假设都应映射到五类数据。不可用时必须显式 blocked。

- OHLCV：结构、range、sweep、displacement、accept/reject 候选。
- Trades：主动成交、taker aggression、突破/回收时的成交推动与失败。
- Orderbook：被动防守、吸收、补单、撤单、接受/拒绝；默认只有经单独授权和稳定性验证后使用。
- Open Interest：新仓、平仓、挤压、去杠杆、仓位堆积。
- Funding Rate：拥挤、方向偏置、carry regime；它是背景，不是独立信号。

OHLCV 可以提出候选，但不能单独证明 smart-money 因果机制。

## 从结构观察到交易假设

只描述下面这些还不是完整研究：

- 有横盘；
- 上下沿有扎针；
- 靠近 OB/FVG；
- 突破后走了一段；
- 某个位置像 fake breakout。

完整 LRF 交易假设至少还要定义：

- `entry_trigger`
- `entry_price_rule`
- `invalidation_condition`
- `stop_rule`
- `exit_or_target_rule`
- `cancel_condition`
- `no_entry_condition`
- `failure_cost_model`
- `judge_rule`

没有这些字段，输出只能叫结构观察，不能叫完整战法研究。

## 样本要求

任何值得继续的 hypothesis 都必须逐步补齐：

- candidate samples；
- no-entry samples；
- boring samples；
- failure samples；
- counterexamples；
- out-of-sample 或 held-out 计划。

只收集漂亮成功图会直接导致过拟合。
