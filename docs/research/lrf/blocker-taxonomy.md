# LRF Blocker Taxonomy

Status: current_truth
Updated: 2026-06-22

LRF 研究必须区分不同 blocker。不能把 app 能力、数据覆盖、R 使用问题、工具缺口、worker 问题、Director 切片问题、skill/rubric 问题和 owner 授权问题混成一句“不能研究”。

## `APP_CAPABILITY_GAP`

FlowSight app / CLI / projection / endpoint 缺少必要 public primitive，或 readback 稳定性不足。

例子：

- public CLI 没有某数据族 readback route；
- endpoint 对某 route 持续 timeout；
- projection 不暴露 owner UI referent；
- evaluator primitive 不存在。

注意：只有 app-side 证据支持时才能归为 app gap。不能因为 R 不会用就怪 app。

## `APP_DISCOVERY_GAP`

App 已有能力，但 ResearchAgents 不知道 route、contract、selector 或 binding 方式。

必须有证据表明 app/CLI 已存在相关能力。不能凭“可能有”猜成 discovery gap。

## `DATA_FAMILY_GAP`

底层数据族在目标 symbol/window/source 中不可用、覆盖不足或质量不够。

例子：

- 指定窗口无 trades；
- OI / funding 覆盖不到；
- orderbook 缺失；
- app route 正常但返回 structured no data。

## `TOOL_MISSING_GAP`

ResearchAgents 缺少把 app-owned payload 转成 deterministic facts 的工具。

例子：

- trades route 可用，但没有 adaptive slicing facts；
- funding/OI payload 可读，但没有低层 facts 工具；
- orderbook route 可用后，缺少 absorption/replenishment facts。

## `TOOL_SHAPE_GAP`

工具存在，但不能消费当前 app payload shape，或 known-at / truncation / coverage 语义错误。

例子：

- `ohlcv_facts.py` 读 current app bars 得到 `bar_count=0`；
- full OHLCV bar 在 open time 被当成已知；
- saved trades payload 缺 coverage metadata 却被当 complete。

## `WORKER_TOOL_USE_GAP`

工具和 registry 已可用，但 worker 没有发出合理 tool_request，或错误使用 tool_response。

例子：

- worker 有 trades facts 工具却只写 prose；
- worker 引用不存在的 tool_response；
- worker 把 partial/truncated 当 complete。

## `SKILL_RUBRIC_GAP`

判断规则不清，导致 worker 无法区分支持、反证、ambiguous 和 no-entry。

例子：

- fake breakout vs acceptance 没有规则；
- displacement quality 没有必要证据；
- funding/OI context 被当成独立信号。

## `DIRECTOR_ORCHESTRATION_GAP`

Research Director 没有正确切片、派任务或隔离信息。

例子：

- 直接给 worker 8 天数据让它自由发挥；
- 只给单根 K 线导致上下文不足；
- 把 Council 的倾向性结论喂给 blind worker；
- 没有 negative / boring / failure 样本任务。

## `EVIDENCE_LINKAGE_GAP`

Source refs、tool responses、hash、cutoff、judgment trace 链路缺失或不一致。

例子：

- judgment trace 引用的 response 不存在；
- tool_response cutoff 晚于 trace cutoff；
- payload hash 没记录；
- request/response 没法复现。

## `OWNER_INPUT_GAP`

owner/dispatcher 尚未提供必要输入或授权。

例子：

- 没有 explicit CLI / endpoint / app selector；
- 没有授权 launch/bind；
- 没有给 bounded research window；
- 没有授权 active skill/tool/doc 变更。

## `OWNER_POLICY_GAP`

是否允许进入某阶段尚未明确。

例子：

- 是否允许 docs promotion；
- 是否允许 formal research packet；
- 是否允许 judge/ledger；
- 是否允许 app-side repair lane。

## 使用要求

每个 blocker 至少写：

- `primary_classification`，只能一个；
- `secondary_classifications`；
- evidence refs；
- 触发位置；
- 缺失字段、能力或纪律；
- 当前还能继续做什么；
- 下一步由 owner、APP Review/C、app-side、data-side 还是 R 处理。

不能用 blocker 掩盖 R 自己的研究偷懒。如果 app 已暴露能力但 R 没用，是 `APP_DISCOVERY_GAP` 或 `R_APP_USAGE_GAP`。如果 worker 被扔进一堆数据不知道研究哪，是 `DIRECTOR_ORCHESTRATION_GAP`。
