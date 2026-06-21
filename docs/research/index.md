# Research 当前真相

Status: current_truth
Updated: 2026-06-21

本目录保存 ResearchAgents 当前研究方向和方法边界。

## 当前研究对象

- `lrf/`：围绕 liquidity、OB、FVG、lost-zone、盘整、扎针、sweep、fake breakout、accept/reject 的 LRF / ICT / smart-money 研究。

## 默认研究模型

R 的默认研究顺序是：

```text
research objective
  -> Client Mirror First
  -> bounded answer-free data access
  -> worker chooses tools and judgment rubrics
  -> deterministic facts from tools
  -> LLM judgment with trace
  -> complete trade hypothesis fields
  -> blind challenge and discipline review
  -> future deterministic judge / ledger
  -> cross-case research diagnosis
```

这个顺序的目的，是防止 R 看到 owner 指向的现象后直接临场解释，也防止先看到后续涨跌再回头编故事。

## 判断不是公式，也不是拍脑袋

LRF 里的 FVG、OB、liquidity sweep、fake breakout、acceptance、lost-zone reaction 等概念，主要是判断性概念。它们不应该被过早写成僵硬公式，让工具直接吐出最终标签。

正确分工是：

- tools 给确定事实和可复核 source refs；
- skills / rubrics 给 Agent 判断规则；
- worker agent 自己选择工具和判断规则；
- 每个判断必须输出 `judgment_trace`；
- known-at cutoff 防止偷看未来；
- reviewer 审纪律，不当市场结果裁判。

## 从图表观察到研究流程

当 owner 指向一段 app 行情、一个时间点、一个矩形或一个横盘，R 必须先把它放回研究对象的因果链。

对当前 LRF，这意味着：

- 先做 Client Mirror First；
- 再给 worker 一个 bounded objective 和可用工具/skill registry；
- worker 自己查 K 线、区间、扎针、收回、成交量等事实；
- worker 用规则判断 liquidity / OB / FVG / fake breakout / acceptance；
- 每个判断留下证据链、反证、缺失证据和置信度；
- 再形成完整 entry / invalidation / stop / exit / no-entry 字段；
- 最后才进入未来 judge / ledger / cross-case 验证。

具体规则见 `lrf/`。

## 当前约束

- 先有研究思路，再找因果链，再用数据验证。
- 数据用于验证 causal script possibility / failure mode，不直接产生交易许可。
- 任何 cross-case 统计只能用于判断是否值得继续研究或是否有统计支撑，不能提前暗示 edge。
