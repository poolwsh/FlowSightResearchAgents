# LRF 研究入口

Status: current_truth
Updated: 2026-06-24

本目录定义 ResearchAgents 对 LRF / ICT / smart-money 历史研究的当前真相。这里不是单次行情结论，也不是交易指令，而是市场机制假设、第一版战法、研究流程、方法栈和 blocker 分类。

## 一句话定义

LRF 研究要回答的是：

> 在历史数据中，价格结构、主动成交和被动流动性如何共同描述局部重新定价；这些过程能否被定义成可盲测、可反证、可记录、可跨样本统计的研究假设。

上层市场机制假设是：

```text
市场是拍卖和流动性重新定价过程；短周期机会来自价格位置、主动成交、被动流动性和运动接受/失败之间的相互作用，而不是来自 FVG、OB、liquidity sweep 等名词本身。
```

Owner-facing 的核心表达是：

```text
结构告诉你去哪看；
订单流告诉你有没有真买卖；
聪明钱告诉你这类机会叫什么。
```

也就是：

```text
structure first
  -> order-flow verifies/refutes
  -> smart-money names hypotheses, not proof
```

第一版 LRF 战法固定为：

```text
Price Action + CVD/Delta + Orderbook
```

这不是让 agent 看最新图决定下单。当前目标是建立一套历史研究体系，逐步逼近可能赚钱的方法。

## 当前文件

- `research-thesis.md`：最高层市场机制假设，回答为什么这些变量值得研究。
- `price-cvd-orderbook-strategy.md`：第一版三层战法和取舍。
- `research-process.md`：Council、Director、Blind Worker、Falsifier、Reviewer 和 freeze 前研究流程。
- `method-stack.md`：docs、workflows、skills、tools、templates、reviews、runs 的职责分层。
- `blocker-taxonomy.md`：app、data、tool、worker、director、skill、orchestration、owner 等 blocker 分类。

权威链为：

```text
research thesis
  -> research framework / docs current truth
  -> skills / rubrics / workflows
  -> tools / deterministic facts
  -> runs / evidence artifacts
```

下层只能实现、验证、阻塞或反证上层；不能在执行中临场改写上层。

## 核心组织模型

```text
Historical data universe
  -> Global Research Council
  -> Research Director
  -> Blind Worker
  -> Falsifier
  -> Reviewer
  -> Freeze
```

## 当前事实层

当前已接受或正在演进的 fact/tool 能力包括：

- `ohlcv_facts.py`：支持 current app bars payload，并使用 completed-bar known-at 语义。
- `trades_facts.py`：支持 app-owned `trades get`，`max_rows=100000`，adaptive slicing，完整/partial/blocked 纪律。
- CVD/delta facts：应从 trades facts 派生，是第一版战法的核心下一步工具方向。
- Orderbook facts：第一版纳入 order-flow evidence，但必须低层、可 partial/blocker，不把 endpoint/readback 不稳定升级成战法失败。
- Funding / OI：暂缓，不进第一版最小战法。

## 禁止提升

以下内容不得写成当前研究结论：

- 单个漂亮 case 证明方法能赚钱；
- worker pass 证明 edge；
- reviewer pass 证明市场结果正确；
- trades/orderbook readback 成功证明 can-trade；
- clean release smoke 成功证明 Product GO；
- 任何未经未来单独授权统计阶段的 performance claim。
