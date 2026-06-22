# FlowSight ResearchAgents 当前真相入口

Status: current_truth
Authority: owner_accepted_researchagents_docs
Updated: 2026-06-22

本目录保存 ResearchAgents 当前被接受的研究对象、组织方式、方法栈、执行边界和审计语言。`docs/**` 是长期 current truth，不是临时草稿、单次 run 输出，也不是 FlowSight app 实现说明。

## 当前结构

- `research/`：研究方向、研究组织方式和方法边界。
- `research/lrf/`：当前 LRF / ICT / smart-money 历史研究系统，包括研究对象、全局研究委员会、Director 切片、blind worker 验证、worker runtime、盲测协议、ledger 要求和 blocker 分类。

## 根本目标

ResearchAgents 的目标是做历史研究，找到、定义、反证并逐步验证可能具有赚钱价值的交易方法。它不是实时下单系统，也不是“看最新行情要不要买卖”的信号系统。

当前研究主题是 LRF / ICT / smart-money：围绕 liquidity、OB、FVG、sweep、reclaim、displacement、acceptance/rejection、trades、OI、funding 等历史数据，研究某些结构是否能形成可复现、可反驳、可统计、可记账的 edge 候选。

## 研究不是交易许可

ResearchAgents 可以产生：

- hypothesis；
- candidate windows；
- deterministic facts；
- judgment traces；
- no-entry / failure / boring samples；
- reviewer discipline audit；
- blocker diagnosis；
- 后续 judge / ledger 的输入材料。

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
- `agent-system/**`：active execution material。只有 owner 明确授权后才能新增或修改。
- legacy root `skills/`、`workflows/`、`tools/`：历史材料和 anti-drift 参考，不是默认执行 surface。

## 当前研究组织原则

ResearchAgents 不应该让一个“死 worker”面对一堆数据发呆。正确组织是：

```text
历史数据 universe
  -> Global Research Council 提出可证伪研究假设
  -> Research Director 选择候选窗口和验证任务
  -> Blind Workers 在看不到结论/未来结果的边界内验证
  -> Reviewer 审 known-at、证据链、overclaim 和暗示污染
  -> 后续 judge / ledger / statistics 才看 outcome 和跨样本结果
```

这是一套历史研究实验室，不是实时交易团队。
