# FlowSight ResearchAgents 当前真相入口

Status: current_truth
Authority: owner_accepted_researchagents_docs
Updated: 2026-06-21

本目录保存 ResearchAgents 当前被接受的研究对象、方法栈、流程边界和审计语言。`docs/**` 是当前真相，不是临时草稿、run 输出仓库，也不是 app 实现说明。

## 当前结构

- `research/`：研究对象和研究方法的当前真相。
- `research/lrf/`：当前 LRF / ICT / smart-money 研究对象、判断规则、worker runtime、盲测协议和 ledger 要求。

## 根本边界

ResearchAgents 使用 FlowSight app 作为 microscope、ledger、evaluator、verifier surface 和 replay surface，但不拥有 FlowSight app source、verifier、release artifact、endpoint directory、dispatcher-owned value、broker、OMS、exchange execution、live-order path 或 account-data path。

正式运行需要 dispatcher 提供：

- `--release-root`
- `--endpoint-dir`
- `--verifier-integrity-sha256`

R / ResearchAgents 不选择这些值，不声明 app verifier / release authority。

## 文档与执行材料

- `docs/**`：当前真相。只放 owner/C 已接受、适合作为长期方法栈的内容。
- `notes/**`：草稿、临时推理、待 review 内容和计划。
- `agent-system/**`：active execution material。只有 owner 明确授权后才能写入或修改。
- legacy root `skills/`、`workflows/`、`tools/`：不作为默认资产，不为旧 S/ss 行为做兼容。

## 当前研究原则

R 的目标是研究交易战法能否形成可复现 edge，但研究输出本身不是交易许可。当前 docs 允许定义：

- 研究对象；
- 判断规则；
- known-at / no-hindsight discipline；
- answer-free packet；
- worker agent runtime；
- judgment trace；
- blind hypothesis / challenge / reviewer；
- deterministic judge / ledger 的未来位置。

当前 docs 不产生：

- edge claim；
- can-trade claim；
- Product GO；
- formal research packet；
- playbook mutation；
- FlowSight app implementation authorization。
