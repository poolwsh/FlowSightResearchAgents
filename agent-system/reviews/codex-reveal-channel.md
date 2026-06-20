# R -> Codex Reveal / Review 通道

Status: legacy-to-active review note

本文件给 `r` 使用。当前 ResearchAgents 重构由 `r` 在 owner 授权下推进；
Codex review lane `C` 负责复核 `r` 完成的动作、边界、证据和下一步建议。

当前推荐的真实联系方式不是手工 outbox，而是：

- 通用 Codex 线程通信：`agent-system/skills/send-codex-thread-message.md`
- R -> C review 包装：`agent-system/skills/request-c-review.md`

本文件只保留 reveal/review 信息结构说明；不替代线程发送工具。

## 什么时候发给 C

`r` 完成任一 owner 授权动作后，如需 Codex 复核，应通过 Codex thread tools
联系目标 session `C`，并记录 delivery evidence。

适合 review 的动作包括：

- 新建或修改研究项目文档。
- 整理或替换 skills / workflows / tools / templates。
- 归档旧材料。
- 产出研究流程模型、工具模型、审计清单或迁移计划。
- 发现 app / CLI / evaluator / release 阻塞，需要 C 从 app 侧 review。

## Review 消息格式

```text
R_REVIEW_FOR_C
action_id:
correlation_id:
message_type:
review_type:
source_session_name: r
source_thread_id:
source_cwd:
target_session_name: C
target_thread_id:
target_thread_title:
target_thread_cwd:
target_thread_status:
target_role_expected:
delivery_status:
send_tool_used:
send_result_thread_id:
sent_at:
fallback_outbox_path:
owner_authorization:
changed_paths:
summary:
why_this_layer:
evidence:
risks_or_open_questions:
requested_codex_review:
next_step_r_proposes:
```

## 边界

C review 不等于：

- owner acceptance
- FlowSight app implementation authorization
- verifier / release / dispatcher authorization
- research packet
- Product GO、money edge、can-trade 或 live-ready claim

Claude 通信不走本通道；Claude 联系必须使用 FlowSight Codex-Claude bridge。
