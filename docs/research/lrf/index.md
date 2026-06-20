# LRF 研究入口

Status: current_truth
Updated: 2026-06-20

本目录是 ResearchAgents 对 LRF 的当前研究真相。这里定义的是研究对象、研究协议、盲测顺序、ledger 要求和方法栈边界，不是单次行情结论，也不是交易指令。

LRF 当前不再只是“看 liquidity / OB / FVG 附近有没有横盘和扎针”。它必须被建模为一个可盲测、可裁判、可记录失败成本的交易战法研究对象。

## 当前文件

- `research-object.md`：LRF 研究对象。定义关键 liquidity / OB / FVG / lost-zone 附近的局部重新定价过程，以及为什么没有入场、出场、止损 / 失效条件就不是完整战法研究。
- `trade-hypothesis-protocol.md`：完整交易假设协议。定义 `hypothesis_fields`、`known_at_fields`、`evaluation_fields`。
- `blind-validation-protocol.md`：盲测验证协议。定义 answer-free packet、A/B subagent、Reviewer、freeze、reveal、deterministic judge、post-reveal comparison 的顺序。
- `ledger-requirements.md`：ledger 要求。定义 entry、exit、failure/cost、no-entry、judge result 的最小字段。
- `analysis-workflow.md`：R 面对 owner 指向 app 中某段行情时的分析顺序。
- `method-stack.md`：docs / workflow / skills / tools / templates / reviews 的职责分层。
- `blocker-taxonomy.md`：APP / DATA / R usage / R method / owner policy blocker 分类。

## 核心判断

没有下面这些字段，LRF 只能是结构观察，不能算完整战法研究：

- 前因和关键区：为什么这里值得研究；
- 入场触发：什么时候这个假设进入候选；
- 止损 / 失效：什么条件证明假设错了；
- 出场 / 目标 / 取消：研究窗口如何结束；
- no-entry：什么情况明确不进入候选；
- failure / cost：失败、扫损、超时、错过、滑点和成本如何记录；
- 盲包和冻结：写 hypothesis 的 Agent 不能看答案；
- 独立裁判：写 hypothesis 的 Agent 不能自己判结果。

## 默认研究顺序

1. Client Mirror First：先绑定 owner 看到的同一个 FlowSight app state。
2. 构建 answer-free known-at packet：只包含当时可见证据。
3. 用 deterministic tools 或 app endpoint/export 生成结构字段和候选 ledger。
4. 派 Codex native subagents 写 blind hypothesis 和 blind challenge。
5. 冻结 packet 与 subagent 输出。
6. 用 deterministic judge / evaluator 判定触发、失效、出场、no-entry 和成本。
7. Reviewer 只审纪律、泄漏、overclaim 和证据边界，不替代 deterministic judge。
8. post-reveal comparison 只做研究诊断，不做 edge / can-trade / Product GO。

## 禁止提升

以下内容不得写成本目录的 current truth：

- 单次 ETH case 的方向性结论；
- “这套能赚钱”；
- “这里可以交易”；
- win-rate、expectancy、PnL、edge、can-trade、Product GO；
- 未经 owner/C 接受的 notes 草稿；
- run output 的单次观察结论；
- app source / verifier / dispatcher 规则复制。
