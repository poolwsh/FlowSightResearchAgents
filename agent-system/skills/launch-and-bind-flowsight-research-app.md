---
name: launch-and-bind-flowsight-research-app
description: Use when R needs owner-authorized launch and binding of a FlowSight research app instance before current-app readback, market-data family discovery, or Client Mirror First. This skill distinguishes exploratory latest/research-current binding from dispatcher-supplied formal release binding and produces an auditable binding packet. It never grants formal verifier authority, Product GO, edge, can-trade, or performance claims.
---

# Launch And Bind FlowSight Research App

## Purpose

Launch and bind a FlowSight research app instance in a controlled, auditable
way before current-app readback.

This skill exists to prevent repeated `OWNER_INPUT_GAP` blockers caused by
missing `--cli-command`, app selector, or endpoint selector.

It produces a binding packet for later app-owned readback or discovery. The
binding packet is not market evidence and is not a formal research packet.

## When To Use

Use this skill when:

- owner explicitly asks R to open or bind the latest available FlowSight app;
- current-app market-data family discovery is blocked by missing app binding;
- Client Mirror First needs a running app selector and CLI command;
- R needs a run-local binding packet before app-owned readback.

Do not use this skill without explicit owner or dispatcher authorization.

## Mode Selection

Choose exactly one mode.

### `owner_latest_exploratory`

Use this mode only when owner explicitly authorizes exploratory current-app
readback.

Allowed:

- resolve `D:\Workspace\FlowSight\releases\research-current.json`;
- resolve `D:\Workspace\FlowSight\releases\latest-release.json`;
- use the resolved release only for exploratory app-owned readback;
- record dirty or non-promotable status;
- produce a binding packet for later discovery.

Required limits:

- no formal verifier authority;
- no research packet;
- no edge claim;
- no can-trade claim;
- no Product GO;
- no performance claim.

Dirty or non-promotable latest releases are allowed only as exploratory
readback surfaces and must be labelled:

`DIRTY_RELEASE_EXPLORATORY_ONLY`

### `dispatcher_release_formal`

Use this mode only when dispatcher supplies the formal binding packet.

Required dispatcher-owned inputs:

- release root;
- endpoint dir;
- verifier integrity sha256;
- app selector or endpoint selector;
- formal selector reference.

R must not choose, compute, or replace these values.

If any formal dispatcher field is missing, stop with:

`FORMAL_BINDING_PACKET_MISSING`

## Required Agent Binding Path

For agent binding, prefer the existing app-side research launcher:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File D:\Workspace\FlowSight\tools\release\launch-research-instance.ps1 `
  -ReleaseRoot <release_dir> `
  -InstanceName <run-local-instance-name>
```

Then consume:

```text
<release_dir>\instances\<InstanceName>\launch-state.json
```

The launch state must be treated as binding evidence, not market evidence.

`D:\Workspace\FlowSight\tools\release\launch-latest-release.ps1` is a human
quick-launch helper only. It is not sufficient for agent binding because it
does not by itself produce the readiness and binding packet required by R.

## Readiness Guardrails

Readiness is not just "pid exists".

Before claiming binding success, require:

- release CLI reports the launched pid as live in `app list --json`;
- `launch-state.json` exists and parses;
- `pid` is present;
- `app_instance_id` is present;
- `endpoint_dir` is present;
- `release_root` or `release_dir` is present;
- release metadata is recorded;
- dirty/promotable status is recorded when available;
- `mode` is recorded;
- `cli_command` is recorded;
- app selector is recorded.

Before later market-data family discovery, prove context:

- publish or confirm the intended chart context through app-owned CLI action
  if required by the app contract;
- read back `app-context get` or a projection readback;
- assert symbol and timeframe match the requested discovery context;
- record command refs and output hashes.

If context cannot be proven, do not continue to data discovery. Return:

`APP_CONTEXT_NOT_PUBLISHED`

or:

`APP_CONTEXT_MISMATCH`

## Binding Packet Output

Return JSON-compatible structured output:

```json
{
  "binding_id": "",
  "mode": "owner_latest_exploratory | dispatcher_release_formal",
  "authorization": {
    "authorization_ref": "",
    "authorization_mode": "owner_latest_exploratory | dispatcher_release_formal",
    "authorized_action": "launch_and_bind_only | readback_discovery_only",
    "authorization_limits": [
      "no formal verifier authority from exploratory mode",
      "no research packet from exploratory mode",
      "no Product GO from exploratory mode",
      "no edge/can-trade claim from exploratory mode",
      "no performance claim from exploratory mode"
    ]
  },
  "release_name": "",
  "release_dir": "",
  "app_sha": "",
  "dirty_or_non_promotable": false,
  "promotable": false,
  "cli_command": "",
  "launch_script": "",
  "instance_name": "",
  "pid": null,
  "app_instance_id": "",
  "endpoint_dir": "",
  "launch_state_path": "",
  "app_selector": "",
  "dispatcher_formal_binding": {
    "dispatcher_binding_packet_ref": "",
    "release_root_source": "dispatcher_supplied | not_formal_mode",
    "dispatcher_release_root_ref": "",
    "endpoint_dir_source": "dispatcher_supplied | not_formal_mode",
    "dispatcher_endpoint_dir_ref": "",
    "verifier_integrity_sha256_ref": "",
    "formal_selector_ref": ""
  },
  "context_assertion": {
    "attempted": false,
    "symbol": "",
    "timeframe": "",
    "matches_requested_symbol_timeframe": false,
    "command_ref": "",
    "output_hash": ""
  },
  "limitations": [],
  "forbidden_attestation": {
    "not_formal_verifier_authority": true,
    "not_research_packet": true,
    "no_edge_claim": true,
    "no_can_trade_claim": true,
    "no_product_go_claim": true,
    "no_performance_claim": true
  }
}
```

For `dispatcher_release_formal`, the dispatcher fields must carry references to
the supplied formal binding packet. For `owner_latest_exploratory`, dispatcher
fields must explicitly say `not_formal_mode`.

## Typed Blockers

Use these blockers instead of guessing:

- `OWNER_AUTHORIZATION_REQUIRED`
- `AUTHORIZATION_SCOPE_MISMATCH`
- `LATEST_POINTER_MISSING`
- `RELEASE_ROOT_MISSING`
- `RELEASE_DIR_NOT_FOUND`
- `LAUNCH_SCRIPT_MISSING`
- `LAUNCH_FAILED`
- `ENDPOINT_NOT_READY`
- `APP_CONTEXT_NOT_PUBLISHED`
- `APP_CONTEXT_MISMATCH`
- `DISPATCHER_FORMAL_INPUT_REQUIRED`
- `FORMAL_BINDING_PACKET_MISSING`
- `DIRTY_RELEASE_EXPLORATORY_ONLY`

`DIRTY_RELEASE_EXPLORATORY_ONLY` may be a limitation rather than a hard stop
when owner explicitly authorized exploratory readback. It is always a hard stop
for formal verifier or research-packet use.

## Forbidden Inputs And Actions

Do not:

- launch without explicit owner or dispatcher authorization;
- use owner discussion or GOAL drafting as launch authorization;
- treat human quick-launch as agent binding;
- edit FlowSight app source;
- edit verifier, release, dispatcher, or endpoint internals;
- build a release;
- compute verifier integrity sha256 as R;
- read raw DB;
- call external APIs;
- read account, broker, OMS, or live-order paths;
- use dirty or non-promotable exploratory binding as formal verifier authority;
- use exploratory latest output as research packet evidence;
- claim performance;
- claim edge;
- claim can-trade;
- grant Product GO;
- run worker research;
- reveal outcomes;
- act as judge/evaluator;
- build or inspect ledger.

## Validation Checklist

Before handing a binding packet to another GOAL, validate:

- mode is exactly one of the allowed modes;
- authorization fields are present;
- `authorization_ref` points to an owner or dispatcher authorization event;
- `authorized_action` matches the intended action;
- formal mode includes dispatcher binding refs;
- exploratory mode records release metadata and dirty/promotable status;
- `launch-research-instance.ps1` was the agent binding path;
- `launch-state.json` exists and parses;
- release CLI live app evidence exists;
- app selector is present;
- context assertion was attempted before market-data discovery;
- symbol/timeframe match if required;
- limitations are explicit;
- forbidden attestations are true.

If any validation fails, return a typed blocker and do not proceed to market-data
family discovery.

## Handoff To Current-App Discovery

The next GOAL may consume the binding packet to populate:

- explicit `--cli-command`;
- explicit app selector or endpoint selector;
- symbol;
- venue;
- timeframe;
- bounded `from_ms`;
- bounded `to_ms`;
- `as_of_ms`;
- max row/snapshot/level caps.

This skill does not choose the market window or research target. Owner or the
next GOAL must supply those values.

