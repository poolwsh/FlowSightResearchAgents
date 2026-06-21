# LRF 研究对象

Status: current_truth
Updated: 2026-06-21

## 一句话定义

LRF 研究的是：关键 liquidity / OB / FVG / lost-zone / breaker 附近，市场如何通过局部盘整、扎针、sweep、fake breakout、accept/reject 完成重新定价，以及这种过程能否被建模成可盲测、可反驳、可记录失败成本的交易假设。

它不是单纯问“某个 OB/FVG 有没有效”，也不是看到突破后解释行情。LRF 的核心是前因后果：

```text
前置 displacement / sweep / lost-zone / OB / FVG / breaker
  -> 价格回到关键记忆区
  -> 局部横盘和上下沿反复试探
  -> sweep / wick / fake breakout / reclaim / reject
  -> 形成可定义的入场候选或 no-entry
  -> 由未来独立 judge 判定触发、失效、出场和成本
```

## 每个关键对象都可能产生 LRF 单元

owner 的关键纠正是：流动性、OB、FVG 附近都可能出现盘整、扎针、扫流动性、假突破、接受或拒绝。这些局部变化可能才是 LRF 要研究的本质。

因此 LRF 研究单元不是“发现一个 OB”或“发现一个 FVG”就结束，而是：

```text
关键对象
  -> 回到附近
  -> 局部供需重估
  -> range / wick / sweep / fake breakout
  -> 接受、拒绝、继续盘整、失效或 no-entry
```

OB/FVG/liquidity 给出战场；盘整、扎针和失败样本暴露战场内部供需变化；entry / exit / stop / no-entry 把观察变成可检验研究对象。

## 判断性概念

以下概念主要是判断性概念，不能过早强行公式化：

- FVG 是否在当前语境里仍有意义；
- OB 是否真的构成反应区，而不是事后画框；
- liquidity sweep 是否被接受、拒绝或只是噪声；
- fake breakout 和 true acceptance 的差异；
- lost-zone reaction 是否说明供需状态切换；
- displacement quality 是否足够改变局部结构；
- no-entry 是否比勉强入场更符合规则。

这些判断应由 worker agent 根据 skill / rubric 做出。工具只给事实，不直接替 worker 下 smart-money 结论。

## 判断必须可审计

每个判断必须有 `judgment_trace`。没有 trace 的判断不能进入后续 trade hypothesis 或 cross-case 统计。

最小 trace 内容：

- `judgment_type`：判断的是 FVG、OB、liquidity sweep、fake breakout、acceptance、lost-zone reaction、displacement 还是 no-entry；
- `decision_time` 和 `evidence_cutoff`；
- `observed_facts`：事实、source refs、tool response refs；
- `applied_rule_clauses`：满足、未满足和模糊的规则条款；
- `reasoning_chain`：简洁、可复核的推理步骤；
- `counter_evidence` 和 `alternative_explanations`；
- `missing_evidence`；
- `confidence_label`；
- `invalidation_or_recheck_condition`；
- `forbidden_future_attestation`。

## 结构观察与战法研究的分界

只描述这些现象还不是完整战法研究：

- 有一个横盘；
- 上下沿有扎针；
- 价格靠近 OB/FVG；
- 突破后走了一段；
- 某个位置看起来像假突破。

完整 LRF 战法研究至少还必须定义：

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

## 五类证据

每个关键判断都要映射到五类数据；不可用时必须显式 blocked。

- OHLCV：结构、range、sweep、displacement、accept/reject 候选。
- Trades：主动成交、taker 方向、突破 / 回收时的 aggression。
- Orderbook：被动防守、吸收、撤单、补单、流动性空洞。
- Open Interest：新仓、平仓、挤压、去杠杆、仓位堆积。
- Funding Rate：拥挤、方向偏置、carry regime。

OHLCV 可以提出候选，但不能单独证明 smart-money 因果机制。
