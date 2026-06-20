# Codex Thread Message Send Tool Contract

Status: active instruction

This is the generic ResearchAgents-side contract for Codex-to-Codex session
communication. It uses host-provided Codex app thread tools. It is not a
standalone script.

## Runtime Tools

- `list_threads`
- `read_thread` when target disambiguation is needed
- `send_message_to_thread`

If these tools are unavailable, create a local outbox draft/audit and report
`delivery_status: not_sent_tool_unavailable`.

## Selection Rule

1. If owner provides `target_thread_id`, verify title/cwd/status before send.
2. Otherwise run `list_threads(query: target_session_name)`.
3. Prefer exact title/name match.
4. If multiple matches exist, disambiguate by cwd and status.
5. Use `read_thread` only when needed.
6. If still ambiguous, stop and ask owner which thread to use.

## Identity Fields

- `source_session_name`
- `source_thread_id`
- `source_cwd`
- `target_session_name`
- `target_thread_id`
- `target_thread_title`
- `target_thread_cwd`
- `target_thread_status`
- `target_role_expected`

## Delivery Fields

- `correlation_id`
- `message_type`
- `delivery_status`
- `send_tool_used`
- `send_result_thread_id`
- `sent_at`
- `fallback_outbox_path`

## Transport Boundary

- Codex session contact uses Codex thread tools.
- Claude contact uses the FlowSight Codex-Claude bridge.
- Local files are fallback/audit only.
- This contract does not authorize FlowSight app implementation, verifier,
  release, endpoint, dispatcher-owned, broker, OMS, or live-order work.
