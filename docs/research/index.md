# Research 当前真相

Status: current_truth
Updated: 2026-06-20

本目录保存 ResearchAgents 当前研究方向和方法边界。

## 当前研究对象

- `lrf/`：围绕 liquidity、OB、FVG、失守区、盘整、扎针、sweep、fake breakout、
  accept/reject 的 LRF / ICT / smart-money 研究。

## 研究顺序

R 的默认研究顺序是：

```text
research premise
  -> causal chain
  -> evidence plan
  -> data readback / ledger
  -> LLM judgment with uncertainty
  -> failure and cost accounting
  -> cross-case validation plan
```

这个顺序的目的，是防止 R 看到 owner 指向的现象后直接临场解释，也防止先拿数据乱撞再事后编故事。

## 从图表观察到研究流程

当 owner 指向一张图、一个矩形、一个时间点或一个横盘，R 必须先把它放回研究对象的因果链。

对当前 LRF，这意味着：

- 先做 Client Mirror First。
- 再找关键区从哪里来。
- 再拆盘整、扎针、sweep、fake breakout。
- 再记录失败、止损、成本和 no-entry。
- 再比较状态切换候选。
- 最后才讨论机会。

具体规则见 `lrf/analysis-workflow.md`。

## 当前约束

- 先有研究思路，再找因果链，再用数据验证。
- 数据用于验证 causal script possibility / failure mode，不直接产生交易许可。
- 任何跨 case 统计都只能用于判断是否值得继续研究或是否有统计支撑，不能提前暗示 edge。

