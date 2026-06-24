# FlowSight ResearchAgents 当前真相入口

Status: current_truth
Authority: owner_accepted_researchagents_docs
Updated: 2026-06-24

本目录保存 ResearchAgents 当前被接受的市场机制假设、第一版研究框架、研究流程、方法栈和 blocker 语言。`docs/**` 是长期 current truth，不是临时草稿、单次 run 输出，也不是 FlowSight app 实现说明。

## 当前结构

- `research/lrf/`：当前 LRF / ICT / smart-money 历史研究体系，包括市场机制假设、第一版战法、研究流程、方法栈和 blocker taxonomy。

## 根本目标

ResearchAgents 的目标是做历史研究：找到、定义、反证并逐步验证可能具有赚钱价值的交易方法。它不是实时下单系统，也不是“看最新行情要不要买卖”的信号系统。

当前 LRF 研究的最高层 thesis 是：

```text
市场是拍卖和流动性重新定价过程；短周期机会来自价格位置、主动成交、被动流动性和运动接受/失败之间的相互作用，而不是来自 FVG、OB、liquidity sweep 等名词本身。
```

当前第一版 LRF 研究战法是：

```text
Price Action + CVD/Delta + Orderbook
```

它使用三层模型：

1. `price-action base layer`：走势、range、sweep/reclaim、displacement、acceptance/rejection。
2. `order-flow evidence layer`：CVD/delta/volume/trades aggression + orderbook/book depth/passive liquidity。
3. `smart-money structure hypothesis layer`：liquidity sweep、FVG candidate、displacement continuation、failed breakout/distribution candidate 等最小 hypothesis language。

## 研究不是交易许可

ResearchAgents 当前可以产生：

- hypothesis；
- candidate windows；
- deterministic facts；
- judgment traces；
- no-entry / boring / failure samples；
- falsifier / reviewer discipline audit；
- blocker diagnosis；
- frozen evidence 和下一步分类。

ResearchAgents 当前不得产生：

- live entry signal；
- broker / OMS / live-order 行为；
- edge claim；
- can-trade claim；
- Product GO；
- formal performance conclusion。

## App 边界

FlowSight app 是研究工具：microscope、readback surface、ledger/evaluator/verifier surface、replay surface。ResearchAgents 使用 app，但不拥有 app。

正式 run 所需的以下值属于 dispatcher/app-side authority：

- `--release-root`
- `--endpoint-dir`
- `--verifier-integrity-sha256`

R / ResearchAgents 不自行选择这些值，不计算 verifier integrity，不编辑 FlowSight app source、release、verifier、dispatcher 或 endpoint internals。

## 文档与执行材料

- `docs/**`：长期 current truth。只放 owner/C 已接受、适合作为方法栈的内容。
- `notes/**`：草稿、讨论、待 review GOAL、临时推理。
- `runs/**`：执行证据和实验产物，不自动升级为 truth。
- `agent-system/**`：active execution material。只有 owner 明确授权后才新增或修改。
- legacy root `skills/`、`workflows/`、`tools/`：历史材料和 anti-drift 参考，不是默认执行 surface。

权威链必须保持：

```text
research thesis
  -> research framework / docs current truth
  -> skills / rubrics / workflows
  -> tools / deterministic facts
  -> runs / evidence artifacts
```

下层材料可以提出 blocker、counterexample 或 docs-change proposal，但不能在执行中反向改写上层。

## 当前研究组织原则

ResearchAgents 不应让一个“死 worker”面对一堆数据发呆。正确组织是：

```text
Historical data universe
  -> Global Research Council
  -> Research Director
  -> Blind Worker
  -> Falsifier
  -> Reviewer
  -> Freeze
```

这是历史研究实验室，不是实时交易团队。Judge、ledger 和 performance 统计都属于未来单独授权阶段，不在当前 docs 展开。
