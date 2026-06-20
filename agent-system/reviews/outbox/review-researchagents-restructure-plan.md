# C Review Request: review-researchagents-restructure-plan

```text
R_REVIEW_FOR_C
action_id: review-researchagents-restructure-plan
correlation_id: review-researchagents-restructure-plan
message_type: c_review_request
review_type: migration,authority,process,tool_boundary
source_session_name: r
source_thread_id: 019ee16f-7e2a-7333-907a-3027ea2cd690
source_cwd: D:\Workspace\FlowSightResearchAgents
target_session_name: c
target_thread_id: 019ee587-8117-7e52-98bf-23a1b9780231
target_thread_title: c
target_thread_cwd: D:\Workspace\FlowSight
target_thread_status: idle
target_role_expected: Codex review lane / C
delivery_status: sent
send_tool_used: send_message_to_thread
send_result_thread_id: 019ee587-8117-7e52-98bf-23a1b9780231
sent_at: 2026-06-20T15:08:23Z
fallback_outbox_path: agent-system/reviews/outbox/review-researchagents-restructure-plan.md
owner_authorization: Owner asked R to return to the notes restructuring plan and first have C review the project/restructuring plan.
changed_paths:
- none for this request; discussion/review request only
summary: Asked C to review the ResearchAgents restructuring plan, including docs/current-truth authority, agent-system active materials, legacy root inventory/archive strategy, R/r renaming, and conservative Git scope.
why_this_layer: This is ResearchAgents IA/migration review before further implementation.
evidence:
- notes/researchagents-restructure-working-notes.md
- docs/index.md
- AGENTS.md
- agent-system/README.md
- GitHub initial commit f5b2fcb tracks AGENTS.md docs/** agent-system/** only
risks_or_open_questions: Need C review on migration order, root AGENTS.md bootloader timing, inventory before archive, and FlowSight app/verifier/release boundary.
requested_codex_review: Verdict accept|modify|reject; blocking issues; recommended first implementation step; what must not be moved/copied yet; whether R/r renaming plus Git scope is acceptable.
next_step_r_proposes: If accepted or bounded modify, R will implement the next owner-authorized small step such as docs/operating-model.md plus inventory draft.
```

created_at_utc: 2026-06-20T15:08:23Z

## Boundary

This is a ResearchAgents-side review request draft/audit record for C/Codex. It
is not C approval, not proof of delivery unless delivery_status: sent is
backed by Codex thread-tool evidence, not a FlowSight app edit request by
itself, not verifier/release/dispatcher authorization, not a research packet,
and not a money-edge, can-trade, or Product GO claim.
