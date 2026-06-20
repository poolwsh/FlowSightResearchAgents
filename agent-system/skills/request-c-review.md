---
name: request-c-review
description: Use when R needs to contact another Codex session named C for review of ResearchAgents-side docs, skills, workflows, tools, templates, migration steps, or app-side blocker claims.
---

# Request C Review

## Purpose

Contact C, the Codex review lane, through the generic Codex thread transport.
This is a wrapper around `send-codex-thread-message`: find the C thread by
title/name or owner-provided thread id, verify the target, and send the review
request. Local outbox files are fallback/audit artifacts only.

This skill does not contact Claude, edit FlowSight app source, or claim that C
has accepted anything.

## Trigger

Use this skill when any of these are true:

- R completed an owner-authorized change and needs C review in another Codex
  session.
- R wants C to review authority, placement, process ordering, tool boundaries,
  communication boundaries, or app-side blocker classification.
- R changed or proposes changing `docs/`, `agent-system/skills/`,
  `agent-system/workflows/`, `agent-system/tools/`, `agent-system/templates/`,
  or `agent-system/reviews/`.
- R needs a review request delivered to a Codex thread named `c`, `C`, or
  another owner-specified session name.

## Hard Boundaries

- Do not edit `D:\Workspace\FlowSight` app source, verifier, release artifacts,
  endpoint dirs, or dispatcher-owned values.
- Do not stop at an outbox file when Codex thread tools are available.
- Do not present the request as C approval.
- Do not hide missing owner authorization. If missing, write `missing`.
- Do not include private secrets, account identifiers, broker/OMS/live-order
  details, or raw app internals.
- Do not use this as a research packet or money-edge claim.

## Procedure

1. Confirm owner authorization for the action being revealed or reviewed.
2. Capture source identity: `source_session_name`, `source_thread_id`, and
   `source_cwd`.
3. Identify target C session.
   - Preferred target field: `target_session_name`, usually `c`.
   - Owner-specified `target_thread_id` wins after verifying title/cwd/status.
   - Use Codex thread tools when available:
     - `list_threads(query: target_session_name)`
     - select exact title/name match when possible
     - verify `thread_id`, `title`, `cwd`, and `status`
     - use `read_thread` only when disambiguation is needed
   - if still ambiguous, stop and ask owner rather than guessing.
4. Collect changed paths, summary, layer reason, evidence, risks/open questions,
   requested C review, and proposed next R step.
5. Send the review request with `send_message_to_thread`.
6. Record delivery evidence:
   - `source_session_name`
   - `source_thread_id`
   - `source_cwd`
   - `target_session_name`
   - `target_thread_id`
   - `target_thread_title`
   - `target_thread_cwd`
   - `target_thread_status`
   - `target_role_expected`
   - `send_tool_used`
   - `send_result_thread_id`
   - `delivery_status`
   - `sent_at` if available
   - `fallback_outbox_path` if created
7. Optionally create an outbox/audit file with
   `agent-system/tools/draft-c-review-request.ps1`. This is not delivery.
8. Tell owner the target thread and delivery status.

## Required Fields

- `action_id`
- `correlation_id`
- `message_type`
- `review_type`
- `source_session_name`
- `source_thread_id`
- `source_cwd`
- `target_session_name`
- `target_thread_id` after lookup
- `target_thread_title`
- `target_thread_cwd`
- `target_thread_status`
- `target_role_expected`
- `owner_authorization`
- `changed_paths`
- `summary`
- `why_this_layer`
- `evidence`
- `risks_or_open_questions`
- `requested_codex_review`
- `next_step_r_proposes`
- `delivery_status`
- `send_tool_used`
- `send_result_thread_id`
- `sent_at` if available
- `fallback_outbox_path` if created

## Review Type Guidance

- `authority`: Is this the right source of truth or layer?
- `process`: Does the order match owner/Codex decisions?
- `tool_boundary`: Is the tool/skill scoped correctly?
- `app_blocker`: Is this really an app/CLI/evaluator/release gap?
- `migration`: Is this safe to import/archive/create next?
- `communication`: Did R actually contact the intended Codex session rather
  than only writing local files?

## Common Mistakes

- Writing only an outbox file while thread tools are available.
- Sending to a thread without checking title/name and cwd.
- Mixing this Codex transport with the Codex-Claude bridge.
- Asking C to review without naming the owner authorization.
- Sending a narrative without paths or evidence.
- Treating C review as app implementation authorization.
- Mixing ResearchAgents process review with FlowSight app development.
- Skipping risks/open questions.
