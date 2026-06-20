# LRF 方法栈

Status: current_truth
Updated: 2026-06-20

LRF 研究分成六层：docs、workflow、skills、templates、tools、reviews。

docs 是当前事实源。workflow、skills、templates、tools、reviews 都必须从 docs 派生，不能从一次 dry-run、旧 S 习惯或临场判断反向定义研究方向。

## docs

docs 保存 owner/C 接受的长期研究真相：

- 研究对象；
- 完整 trade-hypothesis protocol；
- blind validation protocol；
- ledger requirements；
- blocker taxonomy；
- 方法栈边界；
- 分析工作流纪律。

docs 不放：

- 未 review 草稿；
- 单次行情结论；
- run output 的后验解释；
- active tool implementation；
- edge / can-trade / Product GO。

## workflow

workflow 定义执行顺序，不负责概率判断和精确计算。

LRF workflow 必须保证：

1. Client Mirror First；
2. answer-free packet；
3. entry / invalidation / stop / exit / no-entry 字段化；
4. blind subagent dispatch；
5. freeze；
6. deterministic judge / evaluator；
7. failure / cost / no-entry ledger；
8. post-reveal comparison；
9. no edge / no trade permission boundary。

workflow 的核心职责是防止 R 跳过前因、跳过失败成本、跳过盲测、让 Agent 自己判自己。

## skills

skills 是大模型判断任务，不是长期 persona。

可接受的 skill 形态：

- 给定 answer-free packet，写 blind trade hypothesis；
- 给定同一 packet，攻击 hypothesis；
- 给定 frozen A/B 输出，审证据纪律；
- 总结 post-reveal comparison 的研究教训。

skills 可以输出：

- `likely`
- `possible`
- `ambiguous`
- `not_supported`
- `blocked`
- `needs_data`

skills 不读 raw data，不选择 dispatcher-owned values，不做 deterministic judge，不产生 edge / Product GO / can-trade。

## templates

templates 定义输入输出形状，不是 current truth。

候选模板：

- answer-free packet schema；
- blind hypothesis output schema；
- adversarial output schema；
- reviewer discipline schema；
- judge output schema；
- failure/cost ledger schema。

template 可以放在 `agent-system/templates/**`，但只有当 docs 已接受字段纪律后才可创建。

## tools

tools 必须是真实 `.py` / `.ps1` / schema / config，不放 `.md` tool contract。

tools 负责：

- 可复现事实；
- app endpoint/export 输入解析；
- range / sweep / trigger / stop / exit / no-entry ledger；
- deterministic judge；
- JSON / JSONL 输出；
- source refs；
- blocker classification。

tools 不负责：

- 解释市场；
- 写 hypothesis；
- 产生研究结论；
- 选择 dispatcher-owned values；
- 读取 raw DB；
- 读取外部 API；
- 声明 app verifier / release authority；
- 生成 edge / Product GO / can-trade。

## reviews

reviews 检查：

- 是否遵守 docs current truth；
- 是否泄漏答案；
- 是否 overclaim；
- 是否跳过 failure/no-entry；
- 是否把 Reviewer Agent 当 deterministic judge；
- 是否把工具缺口、数据缺口和 R 方法缺口混在一起。

review 不替代 owner/C verdict，也不授权 app work。

## Dispatcher-owned boundary

R、skills、tools 永远不选择：

- `release-root`
- `endpoint-dir`
- `verifier-integrity-sha256`

这些值由 dispatcher / app-side authority 提供。

## Cross-case 边界

跨 case 统计只用于判断：

- 哪些 hypothesis 值得继续研究；
- 哪些 hypothesis 应放弃；
- 哪些字段或工具缺失；
- 是否有进一步统计支撑。

跨 case 统计不能直接写成交易许可、edge、money-grade、Product GO 或 can-trade。
