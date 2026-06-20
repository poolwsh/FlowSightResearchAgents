# LRF 分析工作流

Status: current_truth
Updated: 2026-06-20

本文定义 R 面对 owner 指向 FlowSight app 中某段行情、某个时间、某个矩形、某个横盘或某次突破时的默认研究顺序。

目标不是让 R 临场解释行情，而是把观察变成可盲测、可裁判、可复盘的 trade-hypothesis research。

## 0. Client Mirror First

owner 引用 UI 可见事实时，第一步永远是 Client Mirror First。

R 必须先绑定：

- 同一 app instance / endpoint；
- projection / read-model generation；
- symbol、venue、timeframe；
- visible time range / visible price range；
- owner referent：cursor、selected bar、drawing、rectangle、level、highlighted range。

输出：

- `client_mirror_first.mirror_status: seen | partial | not_exposed`
- `APP_CLIENT_PARITY_GAP` / `NOT_RELEASE_APP_BOUND` / `OWNER_REFERENT_AMBIGUOUS` / `R_APP_USAGE_GAP`

如果 CLI/projection 不能暴露 owner referent，不许装作看见。可以在 owner 提供 bounded window 时做 partial exploratory research，但必须标明来源。

## 1. 定义研究对象，不先找机会

R 先回答：

- 这个区域从哪里来；
- 是否来自 liquidity、OB、FVG、lost-zone、breaker、displacement 或 sweep；
- 价格为什么回到这里；
- 这里是支撑、阻力、供给、需求、流动性池，还是噪声。

如果前因无法定义，后续只能做观察，不能写成 LRF 因果链。

## 2. 字段化关键区和横盘

关键区必须字段化：

- price low / high；
- time window；
- prior structure refs；
- breakdown / reclaim refs；
- overlap with liquidity / OB / FVG / lost-zone；
- known-at source refs。

横盘也必须字段化：

- range high / low / mid；
- duration；
- upper/lower touch count；
- sweep / wick；
- close back inside；
- acceptance / rejection after N bars。

关键区不是入场信号，只是战场。

## 3. 先建立交易假设，再讨论后验

LRF 作为战法研究对象，必须先定义 hypothesis：

- `entry_trigger`：什么时候进入候选；
- `entry_price_rule`：用什么规则记录入场价格；
- `invalidation_condition`：什么条件证明假设错；
- `stop_rule`：怎么记录失败成本；
- `exit_or_target_rule`：研究窗口如何结束；
- `cancel_condition`：什么情况取消；
- `no_entry_condition`：什么情况明确 no-entry。

没有这些字段，不能进入后验 judge，也不能写成完整战法研究。

## 4. 构建 answer-free packet

写 hypothesis 的 Agent 只能看到 known-at packet。

packet 不得包含：

- 后续涨跌；
- reveal / outcome；
- 是否成功；
- 后验标签；
- judge result；
- future descriptor；
- performance / edge。

packet 必须包含：

- app/source refs；
- known-at timestamp；
- key zone / range / sweep candidate；
- entry / invalidation / stop / exit 字段；
- missing evidence；
- blocked data families；
- forbidden field scan。

## 5. 派 blind subagents

最小盲测结构：

1. hypothesis writer：写 LRF trade hypothesis。
2. adversarial challenger：攻击 hypothesis，指出 fake breakout、overclaim、missing evidence。
3. reviewer：只审 A/B 是否遵守证据纪律，不判市场结果。

这些 subagent 都不能看到答案。它们的输出是 evidence input，不是 authority。

## 6. 冻结再 reveal

顺序必须是：

```text
packet freeze
  -> hypothesis output freeze
  -> adversarial output freeze
  -> reviewer discipline freeze
  -> deterministic judge / evaluator reveal
  -> post-reveal comparison
```

不允许 hypothesis writer 在 reveal 后改写理由。

## 7. 独立裁判 / evaluator

裁判优先由 deterministic tool / evaluator 执行。Reviewer Agent 只能审：

- 是否泄漏答案；
- 是否引用不存在字段；
- 是否 overclaim；
- 是否遵守 no-trade / no-edge 边界。

裁判字段至少包括：

- `triggered`
- `not_triggered`
- `stopped`
- `exited`
- `cancelled`
- `timeout`
- `no_entry`
- `mae`
- `mfe`
- `cost`
- `judge_reason`

## 8. 记录 failure / cost / no-entry

R 必须记录失败样本：

- fake breakout；
- stop-out；
- no-entry；
- timeout；
- missed-entry；
- ambiguous；
- cost too high；
- not assessable。

只记录成功样本属于 `R_METHOD_GAP`。

## 9. 五类证据映射

每个关键判断都映射到：

- OHLCV；
- Trades；
- Orderbook；
- Open Interest；
- Funding Rate。

拿不到某类数据时，标 `DATA_BLOCKED` 或 `APP_BLOCKED`，不能用 prose 补证据。

## 10. 输出纪律

每次输出都必须区分：

- `observed_fact`
- `hypothesis`
- `missing_evidence`
- `blocker_classification`
- `judgment_label`
- `failure_cost_notes`
- `next_tool_readback_needed`

最终输出只能是研究诊断，不能是交易许可、edge、can-trade、Product GO、performance claim。
