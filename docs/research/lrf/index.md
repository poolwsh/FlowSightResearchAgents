# LRF 研究入口

Status: current_truth
Updated: 2026-06-22

本目录定义 ResearchAgents 对 LRF / ICT / smart-money 历史研究的当前真相。这里不是单次行情结论，也不是交易指令，而是研究对象、研究组织方式、worker runtime、盲测纪律、ledger 要求和 blocker 分类。

## 一句话定义

LRF 研究要回答的是：

> 在历史数据中，围绕 liquidity / OB / FVG / lost-zone / breaker 等关键区域，市场如何通过 sweep、reclaim、displacement、acceptance/rejection、trades aggression、OI/funding context 完成局部重新定价；这些过程能否被定义成可盲测、可反驳、可记账、可跨样本统计的交易假设。

这不是让 agent 看最新图决定下单。当前目标是建立一套历史研究体系，逐步逼近可能赚钱的方法。

## 当前文件

- `research-object.md`：LRF 研究对象和边界。
- `research-agent-organization.md`：Global Research Council、Research Director、Blind Worker、Reviewer、Judge/Ledger 的组织模型。
- `worker-agent-runtime.md`：worker 如何在 bounded known-at runtime 中请求工具、使用 rubric、输出 judgment_trace。
- `analysis-workflow.md`：从 app readback 到 candidate selection、blind validation、review、freeze 的默认工作流。
- `trade-hypothesis-protocol.md`：完整交易假设字段和禁止提升边界。
- `blind-validation-protocol.md`：盲测、信息隔离、freeze、post-reveal 顺序。
- `ledger-requirements.md`：未来 ledger / judge 所需字段。
- `method-stack.md`：docs、workflows、skills、tools、templates、reviews、runs 的职责分层。
- `blocker-taxonomy.md`：app、data、tool、worker、skill、orchestration、owner 等 blocker 分类。

## 核心组织模型

```text
Historical data universe
  -> Global Research Council
       提出可证伪 hypothesis、候选 playbook、candidate windows
  -> Research Director
       选择具体时间窗口、拆验证任务、控制信息隔离
  -> Blind Workers
       只看自己的窗口、工具和规则；请求 facts；写 judgment_trace
  -> Reviewer
       审 known-at、证据链、暗示污染、truncation、overclaim
  -> Freeze
  -> Future judge / ledger / statistics
       看 outcome、失败成本、跨样本表现
```

## 粒度原则

不要把全市场所有数据直接塞给 worker，也不要让 R 直接告诉 worker “这里就是 sweep”。正确粒度是：

1. Council 在较大历史范围里提出候选研究想法。
2. Director 把想法切成 bounded windows 和明确 verification tasks。
3. Worker 在窗口内自主请求更细的 bar/trade/OI/funding facts。
4. 如果 worker 需要显微镜，再由工具提供更窄 slice、price zone 或 bucket facts。

Worker 研究的是一个范围，不是无限全局；但它可以在范围内向下钻取。

## 当前可用事实层

当前已被接受的 ResearchAgents fact/tool 能力包括：

- `ohlcv_facts.py`：支持 current app bars payload，并使用 completed-bar known-at 语义。
- `trades_facts.py`：支持 app-owned `trades get`，`max_rows=100000`，adaptive slicing，完整/partial/blocked 纪律。
- Funding / OI：可在明确 GOAL 中做低层 inline deterministic parse，后续应考虑专门 fact tool。
- Orderbook：只有在单独 app-side 修复、慢读边界和 ResearchAgents GOAL 接受后才能进入；默认仍排除。

## 禁止提升

以下内容不得写成当前研究结论：

- 单个漂亮 case 证明方法能赚钱；
- worker pass 证明 edge；
- reviewer pass 证明市场结果正确；
- trades/funding/OI readback 成功证明 can-trade；
- clean release smoke 成功证明 Product GO；
- 任何未经 judge/ledger/statistics 的 performance claim。
