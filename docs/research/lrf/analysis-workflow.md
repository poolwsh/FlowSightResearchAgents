# LRF 分析工作流

Status: current_truth
Updated: 2026-06-22

本文定义 ResearchAgents 面对 LRF 历史研究任务时的默认流程。核心目标不是让 R 临场解释行情，而是让多个智能体在明确边界内提出假设、切片验证、找反例、留下可审计证据。

## 0. 明确任务类型

先区分三种任务：

1. `historical_research`：研究历史数据里是否存在可复现方法。默认任务类型。
2. `app_binding_or_capability_diagnostic`：验证 app/readback/tool 是否可用。
3. `live_trading_or_execution`：实时交易、下单、OMS、broker。当前禁止。

LRF 默认只做 `historical_research`。

## 1. App-owned source binding

研究使用 FlowSight app-owned readback。正式边界内，R 不读 raw DB、不读 external API、不编辑 app internals。

如果 owner 指向 UI 可见状态，先执行 Client Mirror First：

- 绑定同一 app instance / endpoint；
- 读取 symbol、timeframe、visible window、projection/read-model；
- 报告 `client_mirror_first.mirror_status: seen | partial | not_exposed`。

如果是历史研究批次，可以由 dispatcher / app-side 提供 clean release binding、endpoint、CLI 和数据窗口。

## 2. Global Research Council 提出候选

Council 在较大历史范围内做研究讨论，目标是提出：

- 可证伪 hypothesis；
- candidate windows；
- data family needs；
- no-entry / boring / failure 样本需求；
- 下一步验证问题。

Council 可以看较大范围历史数据，但不能输出 trade permission、edge 或 performance。Council 输出不能直接喂成 worker 答案。

## 3. Research Director 切片和派任务

Director 负责把 Council 的想法变成可执行 blind tasks：

- 选择具体 `candidate_window`；
- 决定任务粒度：事件点、短窗口、session、对照窗口或反例窗口；
- 指定 worker 可用工具和 rubric；
- 设置 `decision_time` / `evidence_cutoff`；
- 移除 Council 的倾向性结论和 outcome；
- 明确 forbidden sources / outputs。

Director 不写结构判断，不替 worker 得出结论。

## 4. Worker bounded validation

Worker 在窗口内自主请求 facts：

- OHLCV completed-bar facts；
- trades adaptive slice facts；
- OI / funding bounded low-level facts；
- 后续经过授权的 orderbook facts。

Worker 输出：

- `judgment_trace`；
- supporting facts；
- counter evidence；
- missing evidence；
- confidence；
- `needs_data` / `blocked`；
- 可选 trade hypothesis fields。

Worker 不输出 market result、edge、can-trade 或 live entry。

## 5. Falsifier / negative sample pass

如果 hypothesis 看起来有价值，必须安排 falsifier 或 negative sample pass：

- 找同样形态但失败的窗口；
- 找 boring/no-entry 样本；
- 检查是否只挑漂亮图；
- 检查 trades/OI/funding 是否反证；
- 检查规则是否太宽导致到处都能解释。

没有 negative / boring / failure 样本，不得进入 edge 讨论。

## 6. Reviewer discipline audit

Reviewer 只审纪律：

- known-at；
- source/hash refs；
- tool_response linkage；
- partial/truncated usage；
- worker 是否被暗示；
- orderbook/funding/OI 是否越权；
- overclaim / forbidden claims。

Reviewer pass 不等于市场结果正确。

## 7. Freeze 后进入 judge / ledger

顺序必须是：

```text
Council output freeze
  -> Director task freeze
  -> worker traces freeze
  -> falsifier/reviewer freeze
  -> deterministic judge / evaluator reveal
  -> ledger records
  -> cross-case statistics
```

任何 outcome、win/loss、MFE/MAE、PnL、performance 都只能在 freeze 后出现。

## 8. 下一步分类

每轮结束必须给出下一步分类：

- `continue_research`：继续验证该 hypothesis。
- `seek_counterexamples`：先补 negative / boring / failure 样本。
- `tool_goal`：缺 deterministic facts 工具。
- `app_goal`：app readback / endpoint / data family 有问题。
- `rubric_goal`：判断规则不清。
- `director_goal`：切片或任务分配不清。
- `stop_or_archive`：假设证据太弱，先归档。

不得用“智能体不会研究”这种笼统说法代替可修 blocker。
