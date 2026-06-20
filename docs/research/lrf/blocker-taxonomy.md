# LRF Blocker Taxonomy

Status: current_truth
Updated: 2026-06-20

LRF 研究必须区分不同 blocker，不能把 app 能力、数据覆盖、R 使用问题和 R 方法问题混成一句“不能研究”。

## 分类

### `APP_BLOCKED`

FlowSight app / CLI / projection / endpoint 缺少必要 primitive。

例子：

- CLI 没有暴露 owner UI 中的 drawing / rectangle / selected bar。
- app 没有 orderbook readback primitive。
- projection 无法提供 required known-at feature。

### `DATA_BLOCKED`

底层数据缺失、覆盖不足、质量不足或目标窗口不可用。

例子：

- 指定窗口没有 trades。
- OI / FR 覆盖不到目标交易所或时间。
- orderbook 数据缺失，无法验证吸收 / 补单 / 撤单。

### `R_APP_USAGE_GAP`

app / CLI 已有能力，但 R 没有正确使用、绑定或读回。

例子：

- owner 指向 UI 里的 rectangle，CLI 已能读 drawing state，但 R 没跑 Client Mirror First。
- app 已提供 projection generation，R 却用外部 raw bars 代替 app readback。
- app 已能读同一 symbol/timeframe/visible range，R 却把 CLI 读回当成和 UI 脱离的另一份数据。

### `R_METHOD_GAP`

R 缺研究流程、判断方法、case 结构或解释纪律。

例子：

- 看到突破就直接解释，没有先定义关键区和盘整。
- 等 owner 提醒才去看前面暴跌、失守区、横盘前因或状态切换点。
- 只记录成功样本，不记录 fake breakout、stop-out、no-entry。
- 把事后上涨当成突破有效的理由。
- 把 `06/15 10:50/10:54` 这类状态切换候选当成普通 K 线，不比较失败突破对照。

### `OWNER_POLICY_GAP`

owner 尚未授权、研究边界未定，或是否可提升为正式 truth 未定。

例子：

- notes 草稿尚未授权进入 `docs/**`。
- active skill/tool 尚未授权写入 `agent-system/**`。
- 是否允许某类数据读取或跨 case 扫描尚未明确。

## 使用要求

每个 blocker 至少应写：

- blocker 类型。
- 触发位置。
- 缺失字段或缺失能力。
- 当前可继续做什么。
- 下一步需要 owner、C、app-side 或 data-side 哪一方处理。

不能用 blocker 来掩盖 R 自己的研究偷懒；如果 app 已暴露能力但 R 没用，应标 `R_APP_USAGE_GAP`。
如果 R 跳过前因、盘整、失败成本或状态切换比较，应标 `R_METHOD_GAP`。

