# LRF 方法栈

Status: current_truth
Updated: 2026-06-21

LRF 研究分成 docs、workflow、skills、templates、tools、reviews、runs 七层。docs 是当前事实源，其他执行材料必须从 docs 派生，不能从一次 dry-run、旧 S 习惯或临场判断反向定义研究方向。

## docs

docs 保存 owner/C 接受的长期研究真相：

- 研究对象；
- worker runtime；
- judgment trace；
- trade-hypothesis protocol；
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
3. bounded worker runtime；
4. brokered tool request；
5. judgment trace；
6. entry / invalidation / stop / exit / no-entry 字段化；
7. blind challenge；
8. reviewer discipline audit；
9. deterministic judge / evaluator；
10. failure / cost / no-entry ledger；
11. post-reveal comparison；
12. no edge / no trade permission boundary。

workflow 的核心职责是防止 R 跳过前因、跳过失败成本、跳过盲测、替 worker 预选答案或让 Agent 自己判自己。

## skills

skills 是大模型判断任务和规则 rubric，不是长期 persona。

可接受的 skill 形态：

- 给定 bounded objective 和 allowed registry，做结构判断；
- 根据工具事实判断 liquidity sweep 是否成立；
- 判断 fake breakout vs acceptance；
- 判断 lost-zone reaction；
- 写 blind trade hypothesis；
- 攻击 hypothesis；
- 审盲测纪律和 trace 完整性。

skills 可以输出：

- `likely`
- `possible`
- `ambiguous`
- `not_supported`
- `blocked`
- `needs_data`

skills 必须输出 evidence refs、reasoning chain、counter evidence 和 missing evidence。skills 不读 raw DB，不选择 dispatcher-owned values，不做 deterministic judge，不产生 edge / Product GO / can-trade。

## templates

templates 定义输入输出形状，不是 current truth。

候选模板：

- answer-free packet；
- worker tool request；
- worker tool response；
- judgment trace；
- blind hypothesis output；
- adversarial output；
- reviewer discipline output；
- judge output；
- failure/cost ledger。

template 可以放在 `agent-system/templates/**`，但只有当 docs 已接受字段纪律后才可创建。

## tools

tools 必须是真实 `.py` / `.ps1` / schema / config，不放 `.md` tool contract。

tools 负责：

- 可复现事实；
- app endpoint/export 输入解析；
- bars slice；
- bar lookup；
- range stats；
- wick / close-back-inside facts；
- deterministic judge；
- JSON / JSONL 输出；
- source refs；
- blocker classification。

tools 不负责：

- 解释市场；
- 写 hypothesis；
- 直接输出 smart-money 最终标签；
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
- 是否引用不存在字段；
- judgment trace 是否完整；
- reasoning chain 是否由 observed facts 支撑；
- 是否 overclaim；
- 是否跳过 failure/no-entry；
- 是否把 Reviewer Agent 当 deterministic judge；
- 是否把工具缺口、数据缺口和 R 方法缺口混在一起。

review 不替代 owner/C verdict，也不授权 app work。

## runs

`runs/**` 保存过程证据和实验产物，不是长期 truth。

run 可以保存：

- packet；
- tool request / response；
- judgment traces；
- subagent outputs；
- validation；
- summary。

run 不能直接升级为 docs truth。任何 run lesson 进入 docs 前都需要 owner/C 接受。

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
- 哪些字段、工具或 judgment trace 缺失；
- 是否有进一步统计支撑。

跨 case 统计不能直接写成交易许可、edge、money-grade、Product GO 或 can-trade。
