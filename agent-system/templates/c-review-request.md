# C Review Request

```text
R_REVIEW_FOR_C
action_id:
correlation_id:
message_type:
review_type:
source_session_name:
source_thread_id:
source_cwd:
target_session_name:
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

## Field Notes

- `action_id`: Short stable id for this R action.
- `correlation_id`: Stable id for linking request, delivery, and review.
- `message_type`: Example: `c_review_request`.
- `review_type`: Example: `authority`, `process`, `tool_boundary`,
  `app_blocker`, `migration`, or `communication`.
- `source_session_name`: Sending Codex session name, usually `r`.
- `source_thread_id`: Sending thread id when known.
- `source_cwd`: Sending thread workspace.
- `target_session_name`: Codex session name to contact, usually `c`.
- `target_thread_id`: Thread id selected by `list_threads`; leave blank until
  lookup succeeds.
- `target_thread_title`: Exact target thread title.
- `target_thread_cwd`: Target thread workspace.
- `target_thread_status`: Target thread status at send time.
- `target_role_expected`: Expected role, e.g. `Codex review lane / C`.
- `delivery_status`: `sent | not_sent_tool_unavailable | not_sent_ambiguous`.
- `send_tool_used`: Usually `send_message_to_thread`.
- `send_result_thread_id`: Thread id returned by send tool.
- `sent_at`: Send timestamp if available.
- `fallback_outbox_path`: Local audit/fallback path if created.
- `owner_authorization`: Quote or summarize owner authorization. Use `missing`
  if absent.
- `changed_paths`: Files or directories changed by R.
- `summary`: Result only, not a long process log.
- `why_this_layer`: Why this belongs in docs, skills, workflows, tools,
  templates, reviews, archive, or app-side blocker.
- `evidence`: Paths, commands, outputs, hashes, or reviewable artifacts.
- `risks_or_open_questions`: What R believes is still uncertain.
- `requested_codex_review`: What C should check.
- `next_step_r_proposes`: Next owner-authorized action R proposes.
