# LRF 研究入口

Status: current_truth
Updated: 2026-06-21

本目录是 ResearchAgents 对 LRF 的当前研究真相。这里定义的是研究对象、worker 运行方式、判断规则、盲测顺序、ledger 要求和方法栈边界，不是单次行情结论，也不是交易指令。

LRF 当前被定义为：关键 liquidity / OB / FVG / lost-zone / breaker 附近，市场如何通过盘整、扎针、sweep、fake breakout、accept/reject 完成局部重新定价，以及这种过程能否被建模成可盲测、可裁判、可记录失败成本的完整交易假设。

## 当前文件

- `research-object.md`：LRF 研究对象。定义关键区、局部 repricing、判断对象和完整战法研究边界。
- `worker-agent-runtime.md`：worker agent 如何自主选择工具和判断规则，同时留下 `judgment_trace` 并遵守 known-at 防作弊。
- `analysis-workflow.md`：R 面对 owner 指向 app 某段行情时的默认研究顺序。
- `trade-hypothesis-protocol.md`：完整交易假设协议。定义 `hypothesis_fields`、`known_at_fields`、`judgment_trace_fields`、`evaluation_fields`。
- `blind-validation-protocol.md`：盲测协议。定义 answer-free、freeze、worker、challenge、reviewer、future judge 的顺序。
- `ledger-requirements.md`：ledger 要求。定义 judgment、entry、stop、exit、failure/cost、no-entry、judge result 的最小字段。
- `method-stack.md`：docs / workflow / skills / templates / tools / reviews 的职责分层。
- `blocker-taxonomy.md`：APP / DATA / R usage / R method / owner policy blocker 分类。

## 核心模型

```text
关键 liquidity / OB / FVG / lost-zone
  -> 回到关键区
  -> 局部盘整和上下沿试探
  -> sweep / wick / fake breakout / reclaim / reject
  -> worker 用工具取事实
  -> worker 用 rubric 判断
  -> judgment_trace 留证据链
  -> 完整 trade hypothesis
  -> blind challenge / reviewer
  -> future deterministic judge / ledger
```

## 工具、判断和防作弊

LRF 判断不能靠拍脑袋，也不能过早写成死公式。

- 工具只产出 deterministic facts：bars slice、range high/low、wick extreme、close-back-inside、volume facts 等。
- skill / rubric 定义判断规则：FVG、OB、liquidity sweep、fake breakout vs acceptance、lost-zone reaction、displacement quality、no-entry reason。
- worker agent 自主选择工具和 skill，但必须通过 bounded runtime 和 brokered request。
- 每个判断必须输出 `judgment_trace`：证据、source refs、工具响应、规则条款、推理链、反证、缺失证据、置信度、known-at cutoff。
- 任何 entry、stop、exit、no-entry 的支持理由都只能引用 `evidence_cutoff` 之前的事实。

## 完整战法研究的最低字段

没有下面这些字段，LRF 只能是结构观察，不能算完整战法研究：

- 前因和关键区：为什么这里值得研究；
- 判断 trace：每个 FVG / OB / liquidity / sweep / acceptance 判断为什么成立或不成立；
- 入场触发：什么时候这个假设进入候选；
- 止损 / 失效：什么条件证明假设错了；
- 出场 / 目标 / 取消：研究窗口如何结束；
- no-entry：什么情况明确不进入候选；
- failure / cost：失败、扫损、超时、错过、滑点和成本如何记录；
- 盲包和冻结：写 hypothesis 的 worker 不能看到答案；
- 独立裁判：写 hypothesis 的 worker 不能自己判断结果。

## 禁止提升

以下内容不得写成当前真相：

- 单次 ETH case 的方向性结论；
- “这套能赚钱”；
- “这里可以交易”；
- win-rate、expectancy、PnL、edge、can-trade、Product GO；
- 未经 owner/C 接受的 notes 草稿；
- run output 的单次观察结论；
- app source / verifier / dispatcher 规则复制。
