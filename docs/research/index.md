# Research 当前真相

Status: current_truth
Updated: 2026-06-22

本目录保存 ResearchAgents 的当前研究方向、研究组织方式和方法边界。

## 当前研究对象

- `lrf/`：围绕 liquidity、OB、FVG、lost-zone、sweep、fake breakout、acceptance/rejection、trades、OI、funding 的 LRF / ICT / smart-money 历史研究。

## 默认研究模型

ResearchAgents 的默认研究顺序是：

```text
historical research objective
  -> app-owned source binding / data readback
  -> Global Research Council 提出 hypothesis 和 candidate windows
  -> Research Director 把 hypothesis 拆成 blind validation tasks
  -> worker 在 bounded known-at runtime 内请求 deterministic facts
  -> worker 产出 judgment_trace
  -> reviewer 审计证据链、暗示污染、future leakage 和 overclaim
  -> freeze
  -> 后续 deterministic judge / ledger / statistics
```

这个顺序的目的，是防止两种常见失败：

1. R 或 worker 看到一段漂亮走势后回头编故事。
2. Worker 不知道该研究哪段，只能对大段数据做散文式评论。

## 历史研究和实时交易的区别

本工作区做历史研究：

- 可以在历史 universe 里找候选结构；
- 每个具体判断必须模拟当时的 known-at；
- 可以在 freeze 后用未来 outcome 做 judge / ledger；
- 目标是发现和反证可能的赚钱方法。

本工作区不做实时交易：

- 不根据最新行情发入场信号；
- 不接 broker / OMS / live-order；
- 不输出 can-trade、Product GO 或 performance claim；
- 不把单次 worker pass 当 edge。

## 数据与判断分工

- Tools 只产出 deterministic facts 和 source/hash/cutoff refs。
- Skills / rubrics 定义 LLM 判断规则。
- Global Research Council 提出候选研究方向，但不能给 blind worker 喂答案。
- Research Director 选择窗口、拆任务、控制信息隔离。
- Blind Worker 在有限窗口内自主请求 facts 并写 judgment_trace。
- Reviewer 审纪律，不审市场是否赚钱。
- Judge / ledger / statistics 只能在 freeze 后进入。

具体规则见 `lrf/`。
