# LRF 方法栈

Status: current_truth
Updated: 2026-06-22

LRF 研究分成 docs、workflows、skills、templates、tools、reviews、runs 七层。docs 是当前事实源；其他执行材料必须从 docs 派生，不能从单次 run、旧习惯或临场判断反向定义研究方向。

## docs

`docs/**` 保存长期研究真相：

- 研究对象；
- 研究智能体组织模型；
- worker runtime；
- judgment trace；
- trade-hypothesis protocol；
- blind validation protocol；
- ledger requirements；
- blocker taxonomy；
- 方法栈边界。

docs 不放：

- 未 review 草稿；
- 单次行情结论；
- run output 的后验解释；
- active tool implementation；
- edge / can-trade / Product GO。

## workflows

Workflow 定义执行顺序，不负责市场判断。

LRF workflow 必须保证：

1. app-owned source binding / Client Mirror First；
2. Council hypothesis；
3. Director task slicing；
4. answer-free worker runtime；
5. brokered tool request；
6. judgment trace；
7. falsifier / negative sample pass；
8. reviewer discipline audit；
9. freeze；
10. future deterministic judge / ledger；
11. no edge / no live trade boundary。

Workflow 的核心职责是防止 R 跳过前因、失败成本、盲测、反例和信息隔离。

## skills

Skills 是 LLM 判断规则和操作规程，不是 deterministic data reader。

可接受的 skill：

- 结构判断 rubric；
- liquidity / sweep / fake-breakout / acceptance 判断；
- Research Director 切片规程；
- Council hypothesis 讨论规程；
- reviewer discipline audit；
- capability gap diagnosis；
- launch/bind 操作 skill。

Skills 必须输出 evidence refs、reasoning chain、counter evidence 和 missing evidence。Skills 不读 raw DB、不选择 dispatcher-owned values、不当 deterministic judge、不产生 edge / Product GO / can-trade。

## tools

Tools 必须是真实 `.py` / `.ps1` / schema / config。Tools 负责可复现事实，不负责 smart-money 结论。

当前可接受 tool 类型：

- app-owned CLI/readback wrapper；
- OHLCV facts；
- trades adaptive facts；
- future funding/OI/orderbook facts；
- JSON/JSONL validation；
- deterministic judge / ledger 工具，只有未来单独授权后。

Tools 不负责：

- 写 hypothesis；
- 解释市场；
- 输出 OB/FVG/liquidity/sweep/acceptance 最终标签；
- 选择 release-root / endpoint-dir / verifier hash；
- raw DB / external API；
- edge / Product GO / can-trade。

## templates

Templates 定义输入输出形状，不是 current truth。

候选模板：

- Council hypothesis；
- Director task packet；
- worker tool request；
- worker tool response；
- judgment trace；
- adversarial output；
- reviewer output；
- judge output；
- ledger record。

字段纪律必须先在 docs 中被接受，再创建 active template。

## reviews

Reviews 检查：

- 是否遵守 docs current truth；
- 是否泄漏答案；
- refs 是否存在；
- judgment trace 是否完整；
- known-at 是否正确；
- partial/truncated 是否误用；
- 是否跳过 no-entry / failure / boring cases；
- 是否把 reviewer 当 judge；
- 是否把 tool/data/app/worker/skill/orchestration gap 混在一起。

Review 不替代 owner/C verdict，也不授权 app work。

## runs

`runs/**` 保存过程证据和实验产物。Run 可以保存：

- source manifest；
- Council output；
- Director task packet；
- tool requests/responses；
- worker output；
- judgment traces；
- reviewer audit；
- validation report；
- summary。

Run 不自动升级为 docs truth。任何 run lesson 进入 docs 前都需要 owner/C 接受。

## dispatcher-owned boundary

R、skills、tools 永远不选择：

- `release-root`
- `endpoint-dir`
- `verifier-integrity-sha256`

这些值由 dispatcher / app-side authority 提供。

## cross-case 边界

跨样本统计只能用于判断：

- 哪些 hypothesis 值得继续；
- 哪些 hypothesis 应停止；
- 哪些字段、工具或 judgment trace 缺失；
- 是否有进一步统计支持。

跨样本统计不能直接写成交易许可、edge、money-grade、Product GO 或 can-trade。
