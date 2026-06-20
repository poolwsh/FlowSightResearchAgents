---
name: send-codex-thread-message
description: Use when R needs to contact another Codex session/thread such as C, R, or another owner-named Codex session.
---

# Send Codex Thread Message

## Purpose

Send a message from this Codex session to another Codex session using Codex
thread tools. This is the generic Codex-to-Codex transport.

Use the FlowSight Codex-Claude bridge for Claude. Do not use this skill for
Claude communication.

## Trigger

Use this skill when the owner asks R to contact, message, review with, or hand
off to another Codex session by name or thread id.

## Procedure

1. Capture source identity:
   - `source_session_name`
   - `source_thread_id`
   - `source_cwd`
2. Capture target intent:
   - `target_session_name`
   - `target_role_expected`
   - owner-provided `target_thread_id` if any
3. Select target:
   - owner-specified `target_thread_id` wins after verifying title/cwd/status
   - otherwise run `list_threads(query: target_session_name)`
   - prefer exact title/name match
   - disambiguate by cwd and status
   - use `read_thread` only when needed
   - stop and ask owner if still ambiguous
4. Send with `send_message_to_thread`.
5. Record delivery evidence:
   - `send_tool_used`
   - `send_result_thread_id`
   - `delivery_status`
   - `sent_at` if exposed
   - `fallback_outbox_path` if a local draft/audit exists

## Required Fields

- `source_session_name`
- `source_thread_id`
- `source_cwd`
- `target_session_name`
- `target_thread_id`
- `target_thread_title`
- `target_thread_cwd`
- `target_thread_status`
- `target_role_expected`
- `correlation_id`
- `message_type`
- `delivery_status`
- `send_tool_used`
- `send_result_thread_id`
- `fallback_outbox_path`

## Boundaries

- Codex session contact uses Codex thread tools.
- Claude contact uses the Codex-Claude bridge.
- Local files are audit/fallback only, not delivery.
- This skill does not authorize app source, verifier, release, endpoint, or
  dispatcher-owned edits.
