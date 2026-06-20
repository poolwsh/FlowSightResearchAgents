# FlowSight ResearchAgents Agent System

Status: active seed
Authority: active_execution_material_after_owner_authorization

This directory is the home for active ResearchAgents execution material:
skills, workflows, tools, templates, and review prompts selected by the new
method stack.

Root `skills/`, `workflows/`, `tools`, `templates/`, and `reviews/` remain
legacy inventory surfaces unless owner-authorized material is imported or
rewritten here.

## Intended Layout

```text
agent-system/
  skills/
  workflows/
  tools/
  templates/
  reviews/
```

## Active Seed Materials

- `skills/request-c-review.md`: when and how R prepares a C/Codex review
  request and sends it through Codex thread tools.
- `skills/send-codex-thread-message.md`: generic Codex-to-Codex session
  messaging skill.
- `tools/codex-thread-message-send.md`: generic thread-tool contract for
  locating a Codex session and sending a message.
- `tools/codex-thread-review-send.md`: thread-tool contract for locating C by
  session name and sending an R-to-C review request.
- `tools/draft-c-review-request.ps1`: creates a local review draft/audit file
  under `agent-system/reviews/outbox/`; this is fallback/audit, not delivery by
  itself.
- `tools/new-c-review-request.ps1`: deprecated alias for
  `draft-c-review-request.ps1`.
- `templates/c-review-request.md`: manual request format.

## Import Rule

Only material classified as current and useful by the inventory may be imported
here, and imported material should be rewritten to the new method stack rather
than copied wholesale from old root paths.

## Boundary

This directory may contain ResearchAgents-side wrappers, prompts, runbooks, and
schemas. It must not own FlowSight app source, verifier logic, release scripts,
dispatcher-owned values, broker/OMS/live-order work, or private account data.

## Next Authorized Step

Creating additional active materials, importing old materials, archiving legacy
roots, and changing root bootloaders require separate owner authorization.
