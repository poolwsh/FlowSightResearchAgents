---
name: restructure-researchagents-current-truth-docs
description: Use when owner asks R to restructure ResearchAgents docs current truth, especially when duplicate docs, compatibility shims, stale narratives, or premature future-stage files may need deletion or consolidation.
---

# Restructure ResearchAgents Current Truth Docs

## Purpose

Restructure `docs/**` as current truth. This skill prevents "additive patching":
adding a new doc, preserving old duplicate files, and calling that a
restructure.

Docs restructure means:

```text
define authority
  -> choose owning docs
  -> merge duplicate responsibilities
  -> delete redundant or premature files
  -> validate references and boundaries
  -> send C / APP Review
```

## When To Use

Use this skill when owner asks to:

- restructure docs;
- make docs current truth;
- clean up repeated docs;
- remove useless docs or compatibility shims;
- move from draft/legacy material into accepted docs;
- change the research framework, thesis, process, or method stack.

Do not use this skill for:

- a small typo fix;
- run artifact summaries;
- notes-only GOAL drafts;
- active `agent-system/**` skills/tools/templates unless a separate GOAL
  authorizes active execution material.

## Core Rule

Do not treat docs restructure as "write more docs."

The default outcome of a real restructure should often include deletion,
renaming, merging, or ownership reduction.

If a file has no unique current-truth responsibility, delete it or merge it
into the owning doc. Do not preserve it as a compatibility shim.

## Authority Chain

Docs must preserve this authority chain:

```text
research thesis / market mechanism
  -> research framework / docs current truth
  -> skills / rubrics / workflows
  -> tools / deterministic facts
  -> runs / evidence artifacts
```

Lower layers may reveal blockers, counterexamples, or docs-change proposals.
They must not rewrite thesis/framework during execution.

## Restructure Procedure

### 1. Inventory Current Docs

List all docs in scope with:

- path;
- title/headings;
- rough purpose;
- whether it owns unique current truth;
- whether it duplicates another file;
- whether it belongs to a future stage;
- whether it references deleted or legacy surfaces.

### 2. Choose Owning Docs

For each concept, choose one owner:

- WHY / market mechanism thesis;
- HOW / research framework;
- WHO + RUN FLOW / research process;
- method-stack authority and layer responsibilities;
- blocker taxonomy;
- root or local index.

If two docs own the same concept, merge them.

### 3. Delete Or Merge

Delete docs that are:

- duplicate navigation;
- legacy compatibility shims;
- old workflow/runtime fragments after merge;
- premature future-stage formalization;
- stale method truth that conflicts with accepted owner direction.

Examples of deletion candidates:

- middle indexes that only route to one active subtree;
- separate organization/workflow/runtime docs that all describe one process;
- future judge/ledger/formal-packet docs when current truth stops before that
  stage;
- old research-object docs replaced by a sharper strategy/thesis doc.

### 4. Keep Only Current Truth

`docs/**` should not contain:

- unreviewed draft plans;
- single-run conclusions;
- run-output hindsight;
- active tool implementation;
- Product GO, edge, can-trade, or performance approval;
- app source/release/verifier/dispatcher/endpoint implementation details.

Move drafts to `notes/**` if needed. Do not hide draft status inside docs.

### 5. Preserve Boundaries

Docs must state:

- R is research actor, not app developer;
- FlowSight app is app-owned readback/research surface;
- no raw DB or external API substitution;
- no broker, OMS, exchange, or live-order work;
- no Product GO / edge / can-trade / performance;
- judge/ledger/statistics are future separately authorized stages unless
  owner/C explicitly accepts them as current truth.

### 6. Validate

Run validation before review:

```powershell
git diff --check -- docs
rg -n "<deleted-file-name>|<old-narrative-pattern>" docs
rg -n "edge|can-trade|Product GO|performance|live-order|OMS|broker|raw DB|external API" docs
```

Forbidden-term hits are acceptable only in prohibition, boundary, future-stage,
or ResearchAgents tool-broker contexts.

Also verify:

- deleted files are absent;
- indexes do not reference deleted files;
- no mojibake / legacy corrupted text was copied into current truth;
- each remaining doc has one clear responsibility.

### 7. Send C / APP Review

Review request must include:

- review scope;
- final file set;
- deleted file set and reason for each deletion;
- SHA256 for every remaining review-scope file;
- validation commands and results;
- summary of ownership after restructure;
- boundary statement that docs accept does not authorize app work, run
  execution, active `agent-system/**` changes, Product GO, edge, can-trade,
  performance, commit, or push.

## Required Review Framing

Ask C to review as replacement cleanup, not additive patch.

The review questions should include:

1. Is the final docs set minimal?
2. Are deleted docs redundant, merged, or intentionally deferred?
3. Does each remaining file have a unique owner responsibility?
4. Are lower layers prevented from reverse-rewriting thesis/framework?
5. Are Product GO / edge / can-trade / performance boundaries preserved?

## Common Mistakes

- Adding a new "better" doc while leaving old conflicting docs alive.
- Keeping deleted concepts in indexes as vague phrases.
- Treating future judge/ledger/performance docs as current truth too early.
- Letting tools or runs define framework changes without docs review.
- Calling a stale file "legacy reference" inside docs instead of deleting it.
- Sending C a review request without deletion rationale and hash list.

## Output

After execution, report:

- files kept;
- files deleted;
- concepts merged;
- validation results;
- C review status;
- next allowed action.

Do not claim docs are current truth until C/APP Review accepts the restructure.
