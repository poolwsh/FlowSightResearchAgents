---
name: diagnose-lrf-runtime-capability-gap
description: Use after an LRF runtime blocker, reviewer failure, C MODIFY, weak worker output, or suspected capability gap to diagnose whether the next repair target is app capability, app discovery, data family, tool, registry, worker behavior, skill/rubric, R orchestration, owner input, reviewer discipline, or evidence linkage. This skill diagnoses process capability only and never judges market outcome.
---

# Diagnose LRF Runtime Capability Gap

## Purpose

Diagnose why a bounded LRF worker/runtime attempt blocked, degraded, or produced
poor output.

This skill separates fixable layers. It answers: "What exactly failed, and what
kind of next GOAL would repair it?"

It does not answer whether a market structure is correct, profitable,
tradeable, or has edge.

## Non-Goals

Do not use this skill to:

- judge market result;
- decide whether a setup wins or loses;
- decide stop survival, target hit, PnL, win-rate, expectancy, performance,
  edge, can-trade, Product GO, or trade permission;
- reveal outcomes;
- replace deterministic judge/evaluator or ledger;
- write or repair the worker's market judgment;
- create app bug conclusions without evidence refs;
- run tools, read raw data, or inspect app internals.

## When To Use

Use this skill after:

- a typed `BLOCKER`;
- reviewer fail;
- C `MODIFY` caused by data, tool, registry, worker, skill, or orchestration
  gaps;
- worker output is `needs_data`, `blocked`, `inconclusive`, or visibly weak;
- R is about to say "missing tools" or "the agent cannot research" and needs
  evidence for that claim;
- owner asks whether the failure is app-side, tool-side, worker-side,
  skill-side, or R orchestration-side.

This skill is optional after a clean process pass.

## Accepted Inputs

Use only authorized ResearchAgents artifacts, such as:

- `runtime_contract.json`
- `source_data_manifest.json`
- `allowed_tool_skill_registry.json`
- `worker_task_packet.json`
- `tool_requests.jsonl`
- `tool_responses.jsonl`
- `worker_output.json`
- `judgment_traces.jsonl`
- `reviewer_runtime_discipline.json`
- `validation_report.json`
- active workflow, skill, and template refs
- relevant docs from `docs/research/lrf/**`

Prefer exact artifact refs, stable ids, hashes, field names, line refs, and
observed statuses over prose summaries.

## Forbidden Inputs

Do not read or request:

- raw DB;
- external APIs;
- FlowSight app source;
- verifier, release, dispatcher, or endpoint internals;
- account, broker, OMS, or live-order paths;
- screenshots as a substitute for app-owned structured readback;
- reveal, judge, ledger, PnL, win-rate, expectancy, performance, edge, or
  can-trade artifacts unless a future separately authorized post-reveal
  diagnostic GOAL explicitly permits them.

## Classification Taxonomy

Return exactly one `primary_classification`.

Use `secondary_classifications` for additional contributing causes. Do not put
multiple primary causes in the primary field.

Allowed classifications:

- `APP_CAPABILITY_GAP`
  - The app/read model/CLI cannot expose a needed app-owned data primitive or
    runtime primitive.
- `APP_DISCOVERY_GAP`
  - Evidence shows the app/CLI already has a route or capability, but R,
    registry, tool wrapper, or worker did not discover, expose, or use it.
  - Do not use this class merely because the capability might exist.
- `APP_CLIENT_PARITY_GAP`
  - Owner UI state exists but CLI/readback does not faithfully mirror it.
- `DATA_FAMILY_GAP`
  - Required trades/orderbook/OI/FR/footprint family is absent or not exposed.
- `TOOL_MISSING_GAP`
  - App/export has data, but ResearchAgents lacks a deterministic tool to query
    needed facts.
- `TOOL_SHAPE_GAP`
  - Data exists and a tool exists, but artifact schema/shape is incompatible.
- `TOOL_REGISTRY_GAP`
  - Tool exists but is not allowed or visible in the worker/runtime registry.
- `WORKER_TOOL_USE_GAP`
  - Tool and registry were available, but worker failed to request appropriate
    facts.
- `WORKER_SKILL_USE_GAP`
  - Relevant skill/rubric was available, but worker failed to apply it or failed
    required trace fields.
- `SKILL_RUBRIC_GAP`
  - Worker had data/tool access but the rubric lacks enough rules, evidence
    requirements, counter-evidence patterns, or examples to analyze the
    phenomenon.
- `R_ORCHESTRATION_GAP`
  - Main R gave the wrong packet, hid or revealed answers, failed broker duty,
    preselected structures, substituted worker judgment, or broke known-at
    boundaries.
- `OWNER_INPUT_GAP`
  - Owner/app selector/window/referent is missing or too ambiguous to bind.
- `REVIEWER_DISCIPLINE_GAP`
  - Reviewer failed to catch leakage, unsupported refs, overclaim, or acted as
    market judge.
- `EVIDENCE_LINKAGE_GAP`
  - tool_response, judgment_trace, source_ref, hash, requested_end, or
    evidence_cutoff linkage is missing, inconsistent, or not auditable.

## Decision Rules

### Available But Unused

Classify as an available-but-unused problem when artifacts show the data, tool,
skill, or registry entry existed and was allowed, but R or worker did not use it.

Likely classifications:

- `WORKER_TOOL_USE_GAP`
- `WORKER_SKILL_USE_GAP`
- `TOOL_REGISTRY_GAP`
- `R_ORCHESTRATION_GAP`

### Missing Or Blocked

Classify as missing or blocked when an app primitive, data family, deterministic
tool, registry entry, or skill/rubric does not exist or is explicitly
`not_exposed`, `blocked`, or absent.

Likely classifications:

- `APP_CAPABILITY_GAP`
- `DATA_FAMILY_GAP`
- `TOOL_MISSING_GAP`
- `OWNER_INPUT_GAP`

### App Discovery

Use `APP_DISCOVERY_GAP` only when there is evidence of an existing route,
command, projection, or capability.

Evidence can include:

- an app CLI help/listing that exposes the route;
- an accepted app-side note stating the capability exists;
- prior successful command evidence;
- current app-owned readback showing the route or field exists.

Do not classify as `APP_DISCOVERY_GAP` from speculation.

### Tool Shape

Use `TOOL_SHAPE_GAP` when:

- an artifact contains the required data;
- an existing deterministic tool should be the right tool;
- the tool cannot consume the artifact shape or field names.

Example pattern: source artifact contains OHLCV bars, but the fact tool expects a
different `bars` shape and returns `bar_count=0`.

### Evidence Linkage

Use `EVIDENCE_LINKAGE_GAP` when the problem is not that data or tools are absent,
but that the audit chain is broken.

Examples:

- a judgment cites a tool response id that does not exist;
- a tool response lacks output hash or source ref;
- response `requested_end` or `evidence_cutoff` exceeds trace
  `evidence_cutoff`;
- a trace uses facts without source refs;
- reviewer passed a trace despite missing linkage.

### Worker Behavior

Use `WORKER_TOOL_USE_GAP` when the worker had enough registry/tool access but
failed to request facts that the objective required.

Use `WORKER_SKILL_USE_GAP` when the worker had an applicable rubric/skill but
did not apply it or failed required trace fields.

Do not blame the worker if R did not expose the registry, if the tool was
blocked, or if app data was not available.

### Skill Or Rubric

Use `SKILL_RUBRIC_GAP` when:

- worker requested and received relevant facts;
- registry allowed the needed rubric;
- the output remains weak because the rubric lacks decision clauses, evidence
  requirements, counter-evidence patterns, confidence rules, or examples.

Do not use this class when the real issue is missing data or unavailable tools.

### R Orchestration

Use `R_ORCHESTRATION_GAP` when main R:

- preselected hidden answers;
- made the packet too thick with conclusions;
- made the packet too thin to allow tool choice;
- substituted worker judgment;
- failed to broker tool requests;
- failed to preserve known-at cutoff;
- failed to send reviewer failures back through worker/tool repair.

### Inconclusive

If evidence is insufficient, return:

```json
{
  "status": "inconclusive",
  "primary_classification": "",
  "confidence_label": "low"
}
```

Then list the exact missing evidence needed to diagnose.

Do not guess.

## Required Output Shape

Return JSON-compatible structured output:

```json
{
  "diagnosis_id": "",
  "run_ref": "",
  "status": "diagnosed | inconclusive | blocked",
  "primary_classification": "",
  "secondary_classifications": [],
  "evidence_refs": [
    {
      "artifact": "",
      "field_or_line": "",
      "observation": ""
    }
  ],
  "available_but_unused": {
    "tools": [],
    "skills": [],
    "data_families": []
  },
  "missing_or_blocked": {
    "app_primitives": [],
    "data_families": [],
    "tools": [],
    "skills_or_rubrics": []
  },
  "agent_behavior_findings": {
    "worker_requested_tools": false,
    "worker_used_available_registry": false,
    "main_r_substituted_worker": false,
    "reviewer_caught_required_issues": false
  },
  "recommended_next_goal_type": "",
  "recommended_exact_next_scope": [],
  "forbidden_next_actions": [],
  "confidence_label": "high | medium | low"
}
```

## Recommended Next Goal Types

Use exactly one of:

- `app_bug_report`
- `app_discovery_goal`
- `tool_goal`
- `tool_shape_adapter_goal`
- `registry_update_goal`
- `skill_rubric_goal`
- `worker_runtime_goal`
- `reviewer_discipline_goal`
- `current_app_export_rerun`
- `owner_input_needed`
- `no_action`

Recommendations must be narrow and repair-oriented. Do not propose broad
architecture work unless the evidence shows an orchestration or runtime design
gap.

## Confidence Labels

Use:

- `high`: direct artifact evidence supports the primary classification.
- `medium`: multiple artifacts support the classification, but one relevant
  source is missing or partial.
- `low`: evidence is incomplete; prefer `status: inconclusive`.

## Evidence Requirements

Every diagnosis must include evidence refs.

Good evidence refs identify:

- artifact path or run ref;
- field, line, id, request id, response id, trace id, or hash;
- observed fact;
- why that observation supports the classification.

Do not rely on memory or chat-only claims.

## Forbidden Claims And Actions

This skill must not:

- decide if LRF has edge;
- decide can-trade;
- grant Product GO;
- judge performance;
- compute PnL, win-rate, or expectancy;
- reveal outcomes;
- act as deterministic judge/evaluator;
- build or inspect ledger;
- inspect FlowSight app source, verifier, release, dispatcher, or endpoint
  internals;
- read raw DB;
- call external API;
- coordinate app implementation;
- mutate docs, tools, workflows, templates, runs, or app files.

If the diagnosis points to an app bug, recommend `app_bug_report` with evidence
refs. Do not patch the app from R.

## Output Discipline

- Keep `primary_classification` to one value.
- Put additional causes in `secondary_classifications`.
- If the evidence supports multiple repairs, recommend the first narrow repair
  needed to unblock the next bounded validation.
- Preserve partial mirror and missing data-family limitations.
- Do not convert process diagnosis into market analysis.
