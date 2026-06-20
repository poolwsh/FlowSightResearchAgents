# LRF 分析流程纪律

Status: current_truth
Updated: 2026-06-20

本文件把探索S暴露的问题固化成 R 的默认分析顺序。
当 owner 指向 FlowSight UI 中的一张图、一个矩形、一个时间点、一个横盘或一段突破时，R 不能直接进入局部机会解释。

## 0. Client Mirror First

若 owner 引用 UI 可见事实，先执行 Client Mirror First：

- 绑定同一个 app instance / endpoint。
- 绑定 projection / read-model generation。
- 绑定 symbol、venue、timeframe、visible time range、visible price range。
- 尽量绑定 owner referent：cursor、selected bar、drawing、rectangle、level、highlighted range。
- 报告 `client_mirror_first.mirror_status: seen | partial | not_exposed`。

如果 UI 对象无法从 CLI/projection 读回，不许装作看见；按 blocker taxonomy 分类。

## 1. 先找前因，不先找机会

R 必须先回答：

- 这个区域从哪里来？
- 它是否来自前置暴跌、displacement、liquidity sweep、OB、FVG、breaker 或失守区？
- 价格为什么回到这里？
- 这个区域在前面是支撑、阻力、供给、需求、流动性池，还是纯噪声？

如果前因无法定义，后续只能做观察，不能写成 LRF 因果链。

## 2. 定义关键区

关键区必须被字段化，而不是事后凭眼睛画：

- price low / high。
- time window。
- prior structure refs。
- breakdown / reclaim refs。
- overlap with liquidity / OB / FVG / lost zone。
- known-at source refs。

关键区不是入场信号。它只是研究战场。

## 3. 拆盘整内部演化

R 必须把关键区内的盘整当作主要研究对象，而不是等待最后突破才开始分析。

至少要记录：

- range high / low / mid。
- 持续时间。
- 上沿触碰次数。
- 下沿触碰次数。
- 上扫、下扫、扎针。
- close back inside。
- acceptance / rejection after N bars。
- 失败突破序列。

这一步的目标是判断市场是否在重新定价、吸收、诱导、清算，还是没有可判断结构。

## 4. 记录失败和成本

R 必须记录失败样本：

- fake breakout。
- stop-out。
- no-entry。
- timeout。
- ambiguous / not assessable。
- fee / slippage cost model。

如果只记录成功突破，分类为 `R_METHOD_GAP`。

这条来自探索S的核心教训：同一个横盘内部可能有很多看似合理的入场，但成本和连续止损会吞掉漂亮结果。

## 5. 比较状态切换点

R 必须主动寻找“失败候选 vs 真接受候选”的对照，而不是等 owner 提醒。

例如当前 ETH 探索 case 中：

- `06/15 00:10`：失败接受候选。
- `06/15 10:50/10:54`：状态切换候选。

R 要比较的是发生前和发生后的 known-at 结构差异，而不是事后看哪一个涨了。

比较维度包括：

- 突破前是否贴近边界压缩。
- 突破是否只是刺穿，还是形成 displacement。
- 突破后是否回到 range 内。
- pullback 是否守住关键边界。
- trades / OI / FR / orderbook 是否支持接受或失败。

## 6. 五类证据验证

每个关键判断都要映射到五类数据：

- OHLCV。
- Trades。
- Open Interest。
- Funding Rate。
- Orderbook。

拿不到某类数据时必须标 `DATA_BLOCKED` 或 `APP_BLOCKED`，不能用 prose 补成证据。

## 7. 最后才谈机会

机会只能在前面步骤之后出现。

R 可以讨论的机会类型包括：

- 进入关键区失败。
- 下沿 sweep 后 reclaim。
- 上沿 fake breakout 后 reject。
- 真接受后回踩不破。

每个机会必须附带：

- structure invalidation。
- stop location。
- cost implication。
- failure alternative。
- no-trade / no-entry 条件。

不允许在图中间位置直接追逐解释。

## 8. 输出纪律

每次分析输出必须显式区分：

- `observed_fact`：app / tool 可读事实。
- `hypothesis`：因果假设。
- `likely` / `possible` / `ambiguous` / `not_supported` / `blocked`。
- `missing_evidence`。
- `failure_cost_notes`。
- `next_tool_readback_needed`。

如果 R 无法完成这些字段，就不能把输出写成成熟 LRF 分析。

