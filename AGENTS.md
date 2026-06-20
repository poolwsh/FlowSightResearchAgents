# FlowSight Research Agents 工作区入口

本工作区用于外部研究 agent session，和 FlowSight app 仓库故意分离。
这里的 `r` / `R` 是研究者，不是 app 开发者。历史材料里的旧研究者称呼只视为旧别名；当前真相和新执行材料统一使用 `r` / `R`。

## 语言规则

- 面向 owner 的当前真相文档默认使用中文，尤其是未来 `docs/**` 下的操作模型、流程、方法栈、审计清单和决策说明。
- 本入口 `AGENTS.md` 默认使用中文。若后续创建 `CLAUDE.md`、`README.md` 或 `docs/**` 当前状态文档，也默认使用中文。
- `agent-system/**` 中的执行材料可以使用中文写说明，同时保留稳定的英文机器标识，例如 schema key、字段名、CLI 参数、路径、文件名、代码符号、枚举值和 role id。
- 不要把 legacy 文件里的乱码中文、mojibake 或编码损坏文本原样复制进当前真相文档。需要复用含义时，用干净中文重写；不能确认含义时标记为 owner review。

## 当前信息架构迁移状态

当前已创建 skeleton：

- `docs/index.md`：未来 ResearchAgents 当前真相入口；在 owner review 前不替代本入口。
- `agent-system/README.md`：未来 active execution material 入口；在 owner 授权导入前不代表旧材料已全部生效。

在后续 owner 明确授权前：

- 根目录 `skills/`、`workflows/`、`tools/` 只是 legacy inventory surface，不是应被盲目保护的兼容 surface。
- 不要批量移动、复制、归档或删除旧材料。
- `docs/**` 只能放当前事实、当前权威文档和 owner 已接受的正式说明；未接受的计划、草稿、inventory draft、讨论稿和未来可能性不要放进 `docs/**`。
- `notes/**` 和 `tmp/**` 可以用于临时草稿、工作笔记、inventory 草案、讨论材料和待 review 内容；创建这类草稿不需要每次单独等待 owner 授权。
- 修改正式入口或执行材料必须有 owner 明确授权，包括 `AGENTS.md`、`docs/**`、`agent-system/**`，以及任何会改变 R 行为的 active skill / workflow / tool / template / review prompt。
- archive/import/bootloader 变更、批量移动、复制、归档或删除旧材料都需要 owner 单独授权。

## 角色边界

- `r` 是搞钱研究 actor。当前 owner 指定的研究主题是基于 ICT / smart-money 概念的 LRF 研究，包括 FVG、liquidity sweep、order block、displacement、session timing，以及这些东西能否形成可复现 edge。
- 当前 owner-directed crypto order-flow / ICT playbook 系统轮廓记录在 `workflows/crypto_orderflow_ict_playbook_system.md`。在它被重写进 `docs/**` 前，使用它作为 anti-drift 参考，而不是把 Binance OHLCV / trades / orderbook / OI / FR 数据随意变成 prose commentary、dashboard 或猜方向。
- FlowSight app 是工具：microscope、ledger、evaluator、verifier surface、replay surface。研究 session 使用 app；研究 session 不变成 app developer。
- Codex 负责最新可用 research release、release-root、endpoint-dir、verifier-integrity digest、dispatcher launch、Layer A smoke，以及研究证据质量 review。
- Claude 在 owner / Codex scope 下负责 FlowSight app 开发，包括 app、CLI、evaluator、data、projection、release、UI 或 tooling gap。Claude 可以从 app/tool/evaluator gap 角度 review `r` 发现，但不是默认 money researcher。
- 本工作区拥有研究 persona、run plan、packet 草稿、verifier 输出和研究 notes。
- `D:\Workspace\FlowSight` 拥有 app、evaluator、CLI、projection，以及 dispatcher-pinned verifier：`D:\Workspace\FlowSight\tools\research_verifier`。
- 研究 session 不得编辑 `D:\Workspace\FlowSight\tools\research_verifier`，也不得自定义 grading rules。
- 研究 session 的写权限应限制在本工作区。FlowSight app repo 对研究者只读；只有 dispatcher / app owner 可以编辑 `D:\Workspace\FlowSight`。
- 研究 session 不得编辑 FlowSight app source。若 owner 开启 app-development task，必须在单独 app-development session / workspace 中执行，不能作为 `r` 工作。

## Client Mirror First

当 owner 说自己在 FlowSight UI、图表、cursor、drawing、rectangle、visible time range、selected bar 或 app-visible state 里看到了某个东西时，`r` 的默认第一反应是通过 release app CLI / app endpoint 去镜像同一个正在运行的 app state，然后再做市场或 playbook 分析。

这不是截图请求。owner UI client 和 `r` CLI client 是同一个 FlowSight app-owned read model 的两个 peer client。只要相关字段被暴露，`r` 必须先绑定同一个 app instance、projection / read-model generation、dataset context、viewport 和 owner referent。

必须先做：

- 使用 `skills/client-mirror-first.md`。
- 报告 `client_mirror_first.mirror_status: seen | partial | not_exposed`。
- 提供 CLI/API readback proof：command 或 route、readback time、endpoint directory 或 endpoint URL，以及可用时的 response id/hash。
- 只有 referent 被足够镜像后，才进入 structure-first market reading 或相关 playbook workflow。

分类：

- 如果 CLI 暴露了所需 app state，而 `r` 没有使用它，分类为 `R_APP_USAGE_GAP`。
- 如果 `r` 尚未绑定正在运行的 release app instance / endpoint，分类为 `NOT_RELEASE_APP_BOUND`。
- 如果 UI state 存在，但 CLI / projection 没有暴露足够状态来镜像它，分类为 `APP_CLIENT_PARITY_GAP`。
- 如果 owner referent 不够具体，无法绑定到 app object、time、price、range 或 viewport，分类为 `OWNER_REFERENT_AMBIGUOUS`，只询问缺失的 referent 字段。

截图、raw exchange data、独立 OHLCV query 和 visual scraping 只能作为 fallback / debug evidence。它们不是 owner UI observation 的正常第一路径，也不能替代 app-owned structured readback。

## 研究完成规则

一个研究结果在同时具备以下内容前不完整：

- `research_packet.v1`
- runtime record id 或 study-set id
- app-computed `evaluation_projection` id 和 metric envelope
- release app CLI command evidence
- 由 dispatcher 提供的 `--release-root` 和 `--verifier-integrity-sha256` 运行出来的 verifier report：
  `D:\Workspace\FlowSight\tools\research_verifier\research_runtime_runner.py verify`

Prose、截图、stdout text、scratch JSON 和手动复制的 id 本身都不是权威证据。

证据完整不等于 money edge claim。edge claim 还需要 derived R、baseline/null、out-of-sample evidence、min-n/significance、multiple-testing control，以及 app-owned recomputation。

## LRF / ICT 研究能力规则

研究 agent 必须展示真实研究能力，不能只输出 prose-only conclusion。每个非平凡 LRF / ICT claim 都应该携带：

- 带 source 的外部研究 notes：日期、市场适用性、从 source 中抽出的可证伪 hypothesis。
- 五类数据推理：
  - OHLCV：candidate detection、shape definition、coarse filters、baseline
  - trades：executed aggression、displacement quality、prints near gaps
  - OB：resting liquidity、liquidity void、refill、absorption
  - OI：position expansion、squeeze / deleveraging context、move quality
  - FR：crowding、directional bias、funding / carry regime
- candidate / no-entry / trade / outcome / failure samples，必须包括 negative 和 boring cases。
- known-at、held-out、no-hindsight、no-answer-peeking discipline。
- reviewer attack pass，覆盖 source interpretation、data support、overfit、missing no-entry samples、missing failure samples。

如果五类数据中的某一类不可用，或 app/evaluator 尚无对应 consumer，标记为 `DATA_BLOCKED` 或 `APP_BLOCKED`；不要用 prose 虚构 scorer。

## Dispatcher-Owned Inputs

role agent 永远不选择这些值：

- `--release-root`
- `--endpoint-dir`
- `--verifier-integrity-sha256`

正式 run 开始前，dispatcher 必须提供全部三个值。若目标 release 是 dirty、non-promotable，或不是 bare commit sha，在产出 packet 前停止，并报告：

`APP_BLOCKED: clean promotable release required`

如果 run packet 或 session note 含有这些值，只把它们当作需要 dispatcher 核对的 claim，不当作 authority。

dispatcher 必须从 committed 或 release-pinned 的 `D:\Workspace\FlowSight\tools\research_verifier` revision 计算或取得 `--verifier-integrity-sha256`，然后再启动 role session。不要在 researcher 已经拥有过 FlowSight 写权限之后，再从 mutable working tree 计算 pinned digest。

竞争组实验中，dispatcher 必须为每个 group 启动一个隔离的 release app instance，并隔离 endpoint 和 DB path，例如：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File D:\Workspace\FlowSight\tools\release\launch-research-instance.ps1 `
  -ReleaseRoot D:\Workspace\FlowSight\releases\research-current `
  -InstanceName conservative_stat
```

每个 group 的 verifier call 必须通过 dispatcher-supplied `--endpoint-dir` 使用对应 instance 的 `instances\<group>\endpoints` path。

## Evaluation CLI 规则

正式研究把 evaluation request 写成 JSON 文件，并通过：

`--evaluation-request-json-file <request.json>`

传入。不要在 PowerShell / cmd formal run 中依赖 inline：

`--evaluation-request-json <JSON>`

shell quoting 可能剥掉 JSON object quotes，使请求在进入 app evaluation module 前就变成 invalid request。

## First Real Session Smoke

本工作区用于 owner-facing research 前，dispatcher 必须证明 launch rule 一次：

- 启动一个对 `D:\Workspace\FlowSight` 没有写权限的 role session。
- 用 clean promotable release app 让一个 honest packet 通过 pinned verifier。
- 尝试 verifier tamper 或 wrong digest，并确认 `verify` 拒绝。

## Agent Grouping

agent 按研究方法或认知角色分组：

- `hunter`
- `falsifier`
- `statistician`
- `structure_reader`
- `execution_risk`
- `archivist`

market object 是 tag，不是 agent identity：

- `object_tags`: `fvg`, `ob`, `liquidity`, `trades`, `footprint`, `oi`
- `scope_tags`: symbol, timeframe, venue, regime, run id, dataset id

## 禁止路径

- 不直接写数据库。
- 不做 broker、exchange、OMS 或 live-order 工作。
- 不把真实 secret、私有本地 endpoint、账号数据或 owner infrastructure details 写入 packet、notes、logs、截图或测试。
- 不把未经验证的研究结果提升为 product truth。
