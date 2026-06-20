# LRF 方法栈

Status: current_truth
Updated: 2026-06-20

## 四层分工

LRF 研究材料分成四层：docs、workflow、skills、tools。

docs 是事实源。workflow、skills、tools 都必须由 docs 派生，不允许旧材料、临场习惯或单次探索输出反向定义研究方向。

### docs

docs 保存当前事实和长期方法栈。

docs 只能放：

- owner/C 已接受的研究对象 framing。
- 当前研究边界。
- blocker taxonomy。
- 已接受的方法栈分工。
- 已接受的分析流程纪律。

docs 不放：

- 未 review 草稿。
- 临时计划。
- 单次探索输出。
- 未被固化的 hypothesis。

### workflow

workflow 定义研究推进顺序，不负责概率判断和精确计算。

当前 LRF workflow 必须围绕：

1. Client Mirror First。
2. premise 固化。
3. case boundary。
4. 关键区 / 失守区识别。
5. 盘整内部演化。
6. sweep / fake breakout ledger。
7. failure / cost / no-entry ledger。
8. breakout validity comparison。
9. 五类 evidence map。
10. cross-case generalization plan。

workflow 的核心职责是防止 R 跳过前因、失败成本或状态切换比较。

### skills

skills 是大模型判断能力，处理概率、因果、语境和不确定性。

候选 skill 类型：

- `lrf-premise-builder`
- `lost-zone-causal-reader`
- `range-internal-evolution-reader`
- `fake-breakout-vs-acceptance-judge`
- `orderflow-evidence-interpreter`
- `failure-cost-research-discipline`
- `cross-case-generalization-planner`

skills 可以输出：

- `likely`
- `possible`
- `ambiguous`
- `not_supported`
- `blocked`
- `needs_data`

skills 不自己读 raw data，不选择 dispatcher-owned values，不产生 edge、Product GO 或 can-trade claim。

skills 的重要职责是收敛语言：证据不足时必须写 `ambiguous`、`needs_data` 或 `blocked`，不能把可能性写成事实。

### tools

tools 负责可复现事实、定位、计算、ledger 和 source refs。

候选 tool 类型：

- `client_mirror_readback`
- `case_window_extractor`
- `lost_zone_detector`
- `range_boundary_builder`
- `sweep_false_breakout_ledger`
- `breakout_acceptance_comparator`
- `five_family_readback_matrix`
- `failure_cost_ledger`
- `cross_case_sampler`

tools 输出 JSON / JSONL / table / ledger / source refs / command evidence / blocker classification。

tools 不负责解释，不产生研究结论，不声明 app verifier / release authority。

## Dispatcher-owned boundary

R 和 tools 永远不选择：

- `release-root`
- `endpoint-dir`
- `verifier-integrity-sha256`

这些值由 dispatcher / app-side authority 提供。

如果这些值缺失或 release 不 clean / promotable，研究应停止并标记 blocker，不得靠 R 自己补。

## Cross-case 边界

跨 case 统计只能用于判断：

- 是否值得继续研究。
- 是否存在进一步统计支撑。
- 哪些 hypothesis 应该放弃、保留或改写。

跨 case 统计不能直接写成交易许可、edge、money-grade、Product GO 或 can-trade。

