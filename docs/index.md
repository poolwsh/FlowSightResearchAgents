# FlowSight ResearchAgents 当前真相入口

Status: current_truth
Authority: owner_accepted_researchagents_docs
Updated: 2026-06-20

本目录保存 ResearchAgents 当前被接受的研究对象、方法栈、流程边界和审计语言。
它不是 `runs/**` 证据仓库，也不是 `notes/**` 草稿区。

## 当前结构

- `research/`：研究对象和研究方法的当前真相。
- `research/lrf/`：当前 LRF / ICT / smart-money 研究对象和方法栈。

## 当前边界

ResearchAgents 使用 FlowSight app 作为 microscope、ledger、evaluator、verifier
surface 和 replay surface，但不拥有 FlowSight app source、verifier、release
artifact、endpoint directory、dispatcher-owned value、broker、OMS、exchange
execution、live-order path 或 account-data path。

正式运行需要 dispatcher 提供：

- `--release-root`
- `--endpoint-dir`
- `--verifier-integrity-sha256`

R / ResearchAgents 不选择这些值，不声明 app verifier / release authority。

## 草稿与当前真相

- `docs/**`：当前真相，只放 owner/C 已接受且适合作为长期方法栈的内容。
- `notes/**`：草稿、临时推理、待 review 内容。
- `agent-system/**`：active execution material；只有 owner 明确授权后才写入或修改。
- legacy root `skills/`、`workflows/`、`tools/`：不作为默认资产，不为旧 S/ss 行为做兼容。

## 禁止误读

当前 docs 不产生：

- edge claim
- can-trade claim
- Product GO
- research packet
- playbook mutation
- FlowSight app implementation authorization

