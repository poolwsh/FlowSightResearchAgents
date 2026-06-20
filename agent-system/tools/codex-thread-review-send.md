# Codex Thread Review Send Tool Contract

Status: wrapper instruction

This is the R-to-C review wrapper around the generic Codex thread transport.
For the generic transport, use `agent-system/tools/codex-thread-message-send.md`.
It uses Codex app thread tools supplied by the host environment; it is not a
standalone PowerShell script.

## Required Runtime Tools

- `list_threads`
- `read_thread` when disambiguation is needed
- `send_message_to_thread`

If these tools are unavailable, write an outbox draft and report
`delivery_status: not_sent_tool_unavailable`.

## Required Target Fields

- `target_session_name`: usually `c`
- `target_thread_id`
- `target_thread_title`
- `target_thread_cwd`
- `target_thread_status`
- `target_role_expected`: `Codex review lane / C`
- `source_session_name`
- `source_thread_id`
- `source_cwd`

## Send Procedure

1. Run `list_threads(query: target_session_name)`.
2. Prefer an exact title match such as `c`.
3. If multiple matches exist, use cwd and status to disambiguate.
4. If still ambiguous, stop and ask owner which thread to use.
5. Send the review prompt with `send_message_to_thread`.
6. Report delivery evidence to owner.

## Outbox Role

`agent-system/tools/draft-c-review-request.ps1` creates local review drafts or
audit records. It does not contact C and must not be treated as delivery.
`agent-system/tools/new-c-review-request.ps1` is a deprecated alias.

## Boundary

This tool contract is for Codex session review handoff only. It must not edit
FlowSight app source, verifier logic, release artifacts, endpoint dirs, or
dispatcher-owned values.
