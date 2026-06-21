# LRF Blocker Taxonomy

Status: current_truth
Updated: 2026-06-21

LRF 研究必须区分不同 blocker，不能把 app 能力、数据覆盖、R 使用问题、R 方法问题和 owner 授权问题混成一句“不能研究”。

## `APP_BLOCKED`

FlowSight app / CLI / projection / endpoint 缺少必要 primitive。

例子：

- CLI 不暴露 owner UI 的 drawing / rectangle / selected bar；
- app 不暴露 orderbook readback primitive；
- projection 无法提供 required known-at feature；
- deterministic judge 所需 evaluator primitive 尚不存在。

## `DATA_BLOCKED`

底层数据缺失、覆盖不足、质量不足或目标窗口不可用。

例子：

- 指定窗口没有 trades；
- OI / FR 覆盖不到目标交易所或时间；
- orderbook 数据缺失，无法验证吸收 / 补单 / 撤单；
- reveal / evaluation window 缺少判定 trigger / stop / exit 所需字段。

## `R_APP_USAGE_GAP`

app / CLI 已有能力，但 R 没有正确使用、绑定或读回。

例子：

- owner 指向 UI rectangle，CLI 已能读 drawing state，但 R 没跑 Client Mirror First；
- app 已提供 projection generation，R 却用外部 raw bars 替代 app readback；
- app 已能读同一 symbol/timeframe/visible range，R 却把 CLI 读回当成和 UI 脱离的另一份数据。

## `R_METHOD_GAP`

R 缺研究流程、判断方法、worker runtime、case 结构或解释纪律。

例子：

- 看到突破就解释，没先定义前因、关键区和横盘；
- 只记录成功样本，不记录 fake breakout、stop-out、no-entry；
- 没有 entry / exit / stop / invalidation 就声称完成战法研究；
- hypothesis writer 看到 reveal / outcome；
- 让写 hypothesis 的 Agent 自己当裁判；
- Reviewer Agent 替代 deterministic judge 判市场结果；
- 把 OHLCV 候选直接写成 smart-money 机制验证；
- worker 没有 tool registry / skill registry，只能填表；
- worker 判断 FVG / OB / liquidity / acceptance 时没有 `judgment_trace`；
- 判断没有 evidence refs、reasoning chain、counter evidence 或 known-at cutoff；
- R 替 worker 预选答案结构，然后让 worker 补理由。

常用子类：

- `R_WORKER_RUNTIME_GAP`
- `R_TOOL_REGISTRY_GAP`
- `R_SKILL_RUBRIC_GAP`
- `R_JUDGMENT_TRACE_GAP`
- `R_KNOWN_AT_GAP`

这些子类仍属于 `R_METHOD_GAP`，不是 app gap。

## `OWNER_POLICY_GAP`

owner 尚未授权、研究边界未定，或是否可提升为正式 truth 未定。

例子：

- notes 草稿尚未授权进入 `docs/**`；
- active skill/tool 尚未授权写入 `agent-system/**`；
- 是否允许某类数据读取或跨 case 扫描尚未明确；
- 是否进入 formal research packet 尚未授权。

## 使用要求

每个 blocker 至少写：

- blocker 类型；
- 可选子类；
- 触发位置；
- 缺失字段、能力或纪律；
- 当前可以继续做什么；
- 下一步需要 owner、C、app-side、data-side 还是 R 处理。

不能用 blocker 掩盖 R 自己的研究偷懒。如果 app 已暴露能力但 R 没用，应标 `R_APP_USAGE_GAP`。如果 R 跳过 trace、known-at、entry / exit / stop / failure / no-entry / blind discipline，应标 `R_METHOD_GAP`。
