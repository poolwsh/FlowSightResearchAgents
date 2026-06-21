# LRF Blind Validation Protocol

Status: current_truth
Updated: 2026-06-21

本文定义 LRF 的盲测、冻结、worker 判断、reviewer 审计和 post-reveal comparison 顺序。

## 目标

防止 R 或 subagent 事后看答案写故事。每个 hypothesis 必须先在 answer-free known-at 环境中形成判断 trace 和交易假设，再冻结，再由独立 judge / evaluator 在未来阶段判定。

## 标准顺序

```text
Client Mirror First
  -> answer-free packet construction
  -> worker runtime contract
  -> packet and runtime freeze
  -> worker tool requests and judgment traces
  -> blind trade hypothesis
  -> blind adversarial challenge
  -> reviewer discipline audit
  -> A/B/Reviewer freeze
  -> deterministic judge / evaluator reveal
  -> post-reveal comparison
  -> failure/cost/no-entry ledger
  -> cross-case research summary
```

不能跳过 freeze 边界。

## Answer-free 要求

answer-free 不是不给数据，而是不给答案。worker 可以通过授权工具读取 known-at / cutoff 内的数据事实。

answer-free packet 和 runtime 可以包含：

- app readback refs；
- projection generation；
- bounded time window；
- client mirror limitation；
- authorized data source；
- tool registry；
- skill / rubric registry；
- known-at cursor policy；
- missing evidence；
- source hashes。

answer-free packet 和 runtime 不得包含：

- 后续走势作为答案；
- outcome；
- reveal；
- 成功/失败标签；
- judge result；
- post-reveal comparison；
- performance、edge、can-trade。

## Worker 分工

### Hypothesis worker

任务：

- 自主选择允许的 tools 和 rubrics；
- 输出 `judgment_trace`；
- 写 LRF trade hypothesis；
- 定义 entry / invalidation / stop / exit / cancel / no-entry；
- 区分 observed fact、judgment 和 hypothesis；
- 标 missing evidence。

### Adversarial worker

任务：

- 使用同一 answer-free 边界攻击 hypothesis；
- 可以独立请求允许的工具事实；
- 指出 fake breakout、overclaim、缺数据、成本和 no-entry 风险；
- 不看 reveal；
- 不判市场结果。

### Reviewer worker

任务：

- 审 A/B 是否遵守盲测纪律；
- 审 refs 是否存在；
- 审 tool response 是否被正确引用；
- 审 judgment trace 是否完整；
- 审是否有 answer leakage；
- 审是否 overclaim。

Reviewer 不负责市场结果判定。它不是 deterministic judge。

## Judge / evaluator

Judge 优先由 deterministic tool / evaluator 执行。

Judge 只能在 packet、runtime、judgment traces、A/B/Reviewer 输出冻结后运行。

Judge 判定：

- 是否触发 entry；
- 是否 no-entry；
- 是否 stop；
- 是否 exit；
- 是否 cancel；
- 是否 timeout；
- MAE / MFE / cost；
- judge reason。

Judge 不解释 smart-money 机制，只执行已定义规则。

## Post-reveal comparison

post-reveal comparison 只能回答：

- hypothesis 的哪些部分被数据支持、部分支持或不支持；
- adversarial critique 是否指出真实失败点；
- Reviewer 是否漏掉 leakage / overclaim / trace 缺口；
- ledger 是否完整；
- 下一轮 packet / runtime / tool / rubric / protocol 应修什么。

不能回答：

- 是否可以交易；
- 是否有 edge；
- 是否 Product GO；
- 是否 live-ready。
