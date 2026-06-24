# LRF 研究流程

Status: current_truth
Updated: 2026-06-24

本文定义第一版 LRF 研究如何运行。它覆盖角色、流程、worker 取证、review 和 freeze 边界；未来 judge、ledger 和统计阶段不在本文展开。

## 总原则

所有研究从 `research-thesis.md` 开始：

```text
research thesis
  -> Price Action + CVD/Delta + Orderbook framework
  -> Council / Director / Blind Worker / Falsifier / Reviewer process
  -> deterministic facts
  -> frozen evidence
```

任何 actor、skill、tool 或 run 都不能在执行中临场改写 thesis 或 framework。若发现不适用，只能输出 blocker、counterexample 或 docs-change proposal。

## 角色链

```text
Historical data universe
  -> Global Research Council
  -> Research Director
  -> Blind Worker
  -> Falsifier
  -> Reviewer
  -> Freeze
```

### Global Research Council

Council 可以看较大历史范围，但它不是交易员，也不是最终 judge。

职责：

- 围绕市场机制假设提出可证伪 research hypothesis；
- 找 candidate windows、boring windows、failure windows；
- 说明要研究的机制，例如价格位置、主动成交、被动流动性和运动接受/失败；
- 只用最小 smart-money language 命名 hypothesis；
- 不输出 edge、can-trade、performance、Product GO 或 live entry。

Council 不得从 FVG、CVD、orderbook 墙等单个名词开始硬凑故事。

### Research Director

Director 把 Council 想法切成 blind tasks。

职责：

- 选择具体 `candidate_window`、contrast window、boring/failure window；
- 决定任务粒度：事件点、短窗口、session、对照窗口或反例窗口；
- 给每个任务分配 neutral `blind_task_id`；
- 指定 allowed facts、allowed tools、known-at cutoff；
- 移除 Council 的倾向性结论、future outcome 和其他 worker 暗示；
- 把任务改写成“先结构、再订单流、最后 hypothesis 状态”的问题。

Director 不写市场判断。

### Blind Worker

Worker 只看自己的 bounded task、runtime contract、allowed tools 和 facts。

Worker 必须按顺序回答：

1. `price_action_context`：价格处在什么结构位置？
2. `aggressive_flow_state`：CVD/delta/trades aggression 是否支持或背离价格动作？
3. `passive_liquidity_state`：orderbook evidence 是 complete、partial、blocked 还是 insufficient？
4. `smart_money_hypothesis_status`：最小 hypothesis 是 supported、contradicted、partial、insufficient 还是 blocked？
5. `alternative_explanations`：是否有更简单解释？

Worker 不知道：

- 后续涨跌；
- 哪个样本是成功图；
- Council 希望它证明什么；
- judge / ledger / performance。

### Falsifier

Falsifier 攻击 hypothesis，不判断最终赚钱。

职责：

- 找 no-entry、boring、failure、alternative explanation；
- 检查是否只挑漂亮样本；
- 检查 CVD/delta 是否反证；
- 检查 orderbook 是否 partial、blocked 或小样本过度解释；
- 检查 smart-money language 是否太宽，导致到处都能解释。

### Reviewer

Reviewer 只审纪律：

- known-at；
- source/hash refs；
- canonical `response_id`；
- tool_response linkage；
- partial/truncated/orderbook evidence 是否误用；
- worker 是否被暗示；
- forbidden claims。

Reviewer pass 不等于市场结果正确。

## Source binding

进入研究前必须记录：

- app/release binding；
- symbol / venue / timeframe；
- historical window；
- bars source；
- trades/CVD source；
- orderbook status；
- known-at / as-of policy；
- response identity / source hash convention。

如果 app binding、source payload 或 fact tool 不可用，停止为 typed blocker。不得用 raw DB、external API、截图视觉猜测或 app internals 代替 app-owned readback。

## Tool request 纪律

Worker 不直接执行 broad shell、raw DB、external API 或 app internals。Worker 发结构化 request，由 R/tool broker 执行并记录。

每个 tool response 至少要能证明：

- `response_id`
- `request_id`
- `output_hash`
- `source_hashes.raw_source_hash`
- `source_hashes.normalized_source_hash`
- `requested_start`
- `requested_end`
- `evidence_cutoff`
- `cutoff_respected`
- complete / partial / truncated / blocked 状态

Tools 只提供 deterministic facts。Tools 不输出 FVG confirmed、absorption confirmed、distribution confirmed、edge、can-trade 或 Product GO。

## Judgment trace

每个 worker 判断至少记录：

- `blind_task_id`
- `price_action_context`
- `aggressive_flow_state`
- `passive_liquidity_state`
- `smart_money_hypothesis`
- `supporting_facts`
- `contradicting_facts`
- `partial_or_blocked_evidence`
- `alternative_explanations`
- `confidence_label`
- `forbidden_claims_attestation`

没有 deterministic fact refs 的 smart-money 叙事必须降级为 `structure_only_hypothesis` 或 `evidence_insufficient`。

## Freeze 边界

当前 ResearchAgents 只做到 freeze 前的研究过程：

```text
Council output freeze
  -> Director task freeze
  -> worker traces freeze
  -> falsifier/reviewer freeze
```

Outcome、win/loss、MFE/MAE、PnL、statistics、judge、ledger 都是未来单独授权阶段。当前 docs 不展开这些未来文件，避免把第一版研究流程过早 formalize。

## 下一步分类

每轮结束只允许给出以下下一步：

- `continue_research`
- `seek_counterexamples`
- `tool_goal`
- `app_goal`
- `rubric_goal`
- `director_goal`
- `stop_or_archive`

不得用“智能体不会研究”这种笼统说法替代可修 blocker。
